from pathlib import Path
import unittest

from frontend.boundary import discover_boundary
from frontend.coverage import CoverageStatus, build_coverage_ledger
from frontend.dependency import (
    DependencyKind,
    SignalKind,
    build_module_dependency_graph,
    extract_expression_dependencies,
)
from frontend.firrtl import parse_firrtl
from frontend.registry import discover_decoupled_events
from frontend.slice import EventSliceMode, slice_event


FIXTURE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"


class DependencyFrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = FIXTURE.read_text(encoding="utf-8")
        cls.design = parse_firrtl(cls.text)
        cls.module = cls.design.module("BoomProbeUnit")
        cls.graph = build_module_dependency_graph(
            cls.text,
            cls.design,
            "BoomProbeUnit",
        )

    def test_modern_public_chirrtl_structure_is_accepted(self):
        self.assertEqual(self.design.top, "ProbeHarness")
        self.assertIn("BoomProbeUnit", self.design.modules)

    def test_mux_selector_is_control_dependency(self):
        deps = extract_expression_dependencies("mux(and(a, b), x, y)")
        self.assertEqual(deps.control, frozenset({"a", "b"}))
        self.assertEqual(deps.data, frozenset({"x", "y"}))

    def test_register_next_state_edges_are_marked_state_or_control(self):
        self.assertIn("state", self.graph.register_roots)
        to_state = [edge for edge in self.graph.edges if edge.dst == "state"]
        self.assertTrue(to_state)
        self.assertTrue(
            any(
                edge.kind is DependencyKind.CONTROL
                and edge.src == "io.mshr_rdy"
                for edge in to_state
            )
        )
        self.assertTrue(
            any(
                edge.kind is DependencyKind.CONTROL
                and edge.src == "io.lsu_release.ready"
                for edge in to_state
            )
        )

    def test_parser_has_no_silent_unsupported_logic_for_fixture(self):
        ledger = build_coverage_ledger(self.graph)
        self.assertTrue(ledger.complete)
        self.assertFalse(ledger.unsupported)

    def test_rep_event_slice_recovers_fsm_and_ignores_unrelated_node(self):
        registry = discover_decoupled_events(
            self.module,
            discover_boundary(self.module),
        )
        event = registry.events["BoomProbeUnit.io.rep.fire"]
        result = slice_event(
            self.graph,
            event,
            mode=EventSliceMode.OCCURRENCE,
        )

        self.assertTrue(result.complete)
        self.assertIn("state", result.signals)
        self.assertIn("io.req.valid", result.signals)
        self.assertIn("io.lsu_release.ready", result.signals)
        self.assertIn("io.mshr_rdy", result.signals)
        self.assertIn("tag_matches", result.signals)
        self.assertIn("is_dirty", result.signals)
        self.assertNotIn("debug_unused", result.signals)

    def test_full_rep_slice_includes_payload_provenance(self):
        registry = discover_decoupled_events(
            self.module,
            discover_boundary(self.module),
        )
        event = registry.events["BoomProbeUnit.io.rep.fire"]
        result = slice_event(
            self.graph,
            event,
            mode=EventSliceMode.FULL,
        )
        self.assertIn("req.address", result.signals)
        self.assertIn("io.req.bits.address", result.signals)
        self.assertTrue(
            any(
                span.file.endswith("dcache.scala")
                and span.start_line <= 183 <= span.end_line
                for span in result.source_spans
            )
        )


if __name__ == "__main__":
    unittest.main()
