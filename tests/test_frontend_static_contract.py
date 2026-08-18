from __future__ import annotations

import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout

from frontend.cli import main as cli_main
from frontend.coverage import build_coverage_ledger
from frontend.dependency import (
    DependencyKind,
    build_module_dependency_graph,
    extract_expression_dependencies,
)
from frontend.design_graph import backward_design_slice, flatten_design_dependency_graph
from frontend.firrtl import parse_firrtl
from frontend.handoff import (
    HandoffNotReadyError,
    build_instance_static_handoff,
    build_local_static_handoff,
)
from frontend.input_contract import (
    InputFormat,
    detect_input_format,
    validate_static_input,
)
from frontend.pipeline import StaticFrontend
from frontend.source import SourceMapper, SourceResolutionError
from frontend.slice import SourceSpan


PROBE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"
HIER = Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"


class StaticInputContractTests(unittest.TestCase):
    def test_chirrtl_input_is_supported_and_source_mapped(self):
        text = PROBE.read_text(encoding="utf-8")
        report = validate_static_input(text)
        self.assertEqual(report.format, InputFormat.CHIRRTL)
        self.assertTrue(report.supported)
        self.assertTrue(report.provenance_ready)
        self.assertGreater(report.source_locator_count, 0)

    def test_firrtl_dialect_is_detected_but_not_silently_misparsed(self):
        text = 'firrtl.circuit "Top" {\n  firrtl.module @Top() {\n  }\n}\n'
        report = validate_static_input(text)
        self.assertEqual(report.format, InputFormat.FIRRTL_DIALECT)
        self.assertFalse(report.supported)
        with self.assertRaisesRegex(ValueError, "FIRRTL-dialect"):
            StaticFrontend.from_firrtl(text)


class FailClosedCoverageTests(unittest.TestCase):
    def test_unknown_executable_statement_makes_analysis_incomplete(self):
        text = """\
circuit Bad :
  module Bad :
    input x : UInt<1>
    output y : UInt<1>
    mysterious_drive y, x
"""
        design = parse_firrtl(text)
        graph = build_module_dependency_graph(text, design, "Bad")
        ledger = build_coverage_ledger(graph)

        self.assertFalse(ledger.complete)
        self.assertEqual(len(ledger.unsupported), 1)
        self.assertIn("mysterious_drive", ledger.unsupported[0].statement.text)

        frontend = StaticFrontend.from_firrtl(text)
        with self.assertRaisesRegex(ValueError, "Static frontend is incomplete"):
            frontend.assert_complete("Bad")

    def test_flipped_aggregate_connect_uses_leaf_flow_direction(self):
        text = """\
circuit FlipAgg :
  module FlipAgg :
    wire a : { flip ready : UInt<1>, valid : UInt<1> }
    wire b : { flip ready : UInt<1>, valid : UInt<1> }
    connect b, a
"""
        design = parse_firrtl(text)
        graph = build_module_dependency_graph(text, design, "FlipAgg")
        self.assertTrue(graph.complete)
        edges = {(edge.src, edge.dst, edge.kind) for edge in graph.edges}
        self.assertIn(("a.valid", "b.valid", DependencyKind.DATA), edges)
        self.assertIn(("b.ready", "a.ready", DependencyKind.DATA), edges)

    def test_firrtl_3_keyword_invalidate_is_supported(self):
        text = """\
FIRRTL version 3.3.0
circuit Modern :
  module Modern :
    input x : UInt<1>
    output y : UInt<1>
    connect y, x
    invalidate y
"""
        design = parse_firrtl(text)
        graph = build_module_dependency_graph(text, design, "Modern")
        self.assertTrue(graph.complete)
        self.assertTrue(any(s.kind == "invalidate" for s in graph.statements))
        self.assertTrue(
            any(edge.src == "x" and edge.dst == "y" for edge in graph.edges)
        )

    def test_hierarchical_slice_reports_touched_incomplete_child(self):
        text = """\
circuit Top :
  module Top :
    input in : UInt<1>
    output out : UInt<1>
    inst child of Child
    child.io.in <= in
    out <= child.io.out
  module Child :
    input io : { in : UInt<1> }
    output out : UInt<1>
    mysterious_drive out, io.in
"""
        design = parse_firrtl(text)
        local = {
            name: build_module_dependency_graph(text, design, name)
            for name in ("Top", "Child")
        }
        flat = flatten_design_dependency_graph(text, design, local)
        result = backward_design_slice(flat, ["Top::out"])
        self.assertFalse(result.complete)
        self.assertIn("Top.child", result.incomplete_instances)


class DependencyCornerCaseTests(unittest.TestCase):
    def test_dynamic_subaccess_preserves_address_dependency(self):
        deps = extract_expression_dependencies("vec[idx]")
        self.assertIn("vec[*]", deps.data)
        self.assertIn("idx", deps.address)

    def test_memory_mport_slice_keeps_address_and_memory_state(self):
        text = """\
circuit MemTop :
  module MemTop :
    input clock : Clock
    input addr : UInt<2>
    output out : UInt<8>
    cmem mem : UInt<8>[4]
    read mport r = mem[addr], clock
    out <= r
"""
        design = parse_firrtl(text)
        graph = build_module_dependency_graph(text, design, "MemTop")
        kinds = {(edge.src, edge.dst, edge.kind) for edge in graph.edges}
        self.assertIn(("mem", "r", DependencyKind.MEMORY), kinds)
        self.assertIn(("addr", "r", DependencyKind.ADDRESS), kinds)


class SourceMappingTests(unittest.TestCase):
    def test_source_mapper_resolves_exact_locator_span(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src" / "Foo.scala"
            source.parent.mkdir(parents=True)
            source.write_text("line1\nline2\nline3\nline4\n", encoding="utf-8")

            mapper = SourceMapper.from_roots([root])
            snippet = mapper.snippet(
                SourceSpan("src/Foo.scala", 2, 3),
                context_lines=1,
            )

            self.assertEqual(snippet.start_line, 1)
            self.assertEqual(snippet.end_line, 4)
            self.assertEqual(snippet.text, "line1\nline2\nline3\nline4\n")

    def test_source_mapper_does_not_escape_declared_root(self):
        with tempfile.TemporaryDirectory() as directory:
            mapper = SourceMapper.from_roots([directory])
            with self.assertRaises(SourceResolutionError):
                mapper.resolve("../../outside.scala")


class StaticFrontendCLITests(unittest.TestCase):
    def _run(self, *args: str):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            rc = cli_main(list(args))
        self.assertEqual(rc, 0)
        return json.loads(stdout.getvalue())

    def test_report_cli_exposes_input_and_coverage(self):
        result = self._run("report", str(PROBE))
        self.assertEqual(result["input"]["format"], "chirrtl")
        self.assertTrue(result["input"]["provenance_ready"])
        self.assertTrue(result["complete"])

    def test_design_events_cli_accepts_one_firrtl_positional(self):
        result = self._run("design-events", str(HIER))
        ids = {item["id"] for item in result}
        self.assertIn("DCacheTop.prober::io.req.fire", ids)

    def test_connectors_cli_exposes_direct_physical_links(self):
        result = self._run("connectors", str(HIER))
        pairs = {(item["from_event"], item["to_event"]) for item in result}
        self.assertIn(
            (
                "DCacheTop::io.tl_b.fire",
                "DCacheTop.prober::io.req.fire",
            ),
            pairs,
        )

    def test_tree_cli_exposes_physical_and_state_region_nodes(self):
        result = self._run("tree", str(HIER))
        self.assertEqual(result["kind"], "module")
        self.assertEqual(result["instance_path"], "DCacheTop")
        kinds = {child["kind"] for child in result["children"]}
        self.assertIn("module", kinds)
        probe = next(
            child
            for child in result["children"]
            if child["kind"] == "module"
            and child["instance_path"] == "DCacheTop.prober"
        )
        self.assertTrue(
            any(child["kind"] == "state_region" for child in probe["children"])
        )

    def test_instance_slice_cli_respects_subtree_boundary(self):
        result = self._run(
            "instance-slice",
            str(HIER),
            "--event",
            "DCacheTop.prober::io.req.fire",
            "--root",
            "DCacheTop.prober",
        )
        self.assertEqual(result["scope"], "instance_subtree")
        self.assertEqual(result["subtree_root"], "DCacheTop.prober")
        self.assertTrue(result["analysis"]["complete"])
        ids = {signal["id"] for signal in result["signals"]}
        self.assertNotIn("DCacheTop::io.tl_b.valid", ids)
        self.assertEqual(result["semantic_labels"], [])

    def test_design_slice_cli_emits_no_semantic_labels(self):
        result = self._run(
            "design-slice",
            str(HIER),
            "--event",
            "DCacheTop::io.tl_c.fire",
        )
        self.assertTrue(result["analysis"]["complete"])
        self.assertEqual(result["semantic_labels"], [])
        connector_pairs = {
            (item["from_event"], item["to_event"])
            for item in result["direct_connectors"]
        }
        self.assertIn(
            (
                "DCacheTop.prober::io.rep.fire",
                "DCacheTop::io.tl_c.fire",
            ),
            connector_pairs,
        )
        signal_ids = {signal["id"] for signal in result["signals"]}
        self.assertIn("DCacheTop.prober::state", signal_ids)


class StaticHandoffTests(unittest.TestCase):
    def test_complete_grounded_slice_can_cross_pre_llm_boundary(self):
        frontend = StaticFrontend.from_firrtl(PROBE.read_text(encoding="utf-8"))
        handoff = build_local_static_handoff(
            frontend,
            "BoomProbeUnit",
            "BoomProbeUnit.io.rep.fire",
        )
        self.assertTrue(handoff["handoff"]["ready"])
        self.assertTrue(handoff["handoff"]["semantic_labels_locked"])
        self.assertEqual(handoff["semantic_labels"], [])

    def test_incomplete_slice_is_blocked_before_llm_boundary(self):
        text = """\
circuit Bad : @[Bad.scala 1:1]
  module Bad : @[Bad.scala 2:1]
    input io : { flip ready : UInt<1>, valid : UInt<1> } @[Bad.scala 3:1]
    mysterious_drive io.valid, io.ready @[Bad.scala 4:1]
"""
        frontend = StaticFrontend.from_firrtl(text)
        with self.assertRaises(HandoffNotReadyError):
            build_local_static_handoff(
                frontend,
                "Bad",
                "Bad.io.fire",
            )

    def test_instance_subtree_handoff_is_ownership_scoped_and_locked(self):
        frontend = StaticFrontend.from_firrtl(
            HIER.read_text(encoding="utf-8"),
            eager=False,
        )
        handoff = build_instance_static_handoff(
            frontend,
            "DCacheTop.prober::io.req.fire",
            root_instance="DCacheTop.prober",
        )
        self.assertTrue(handoff["handoff"]["ready"])
        self.assertTrue(handoff["handoff"]["ownership_scoped"])
        self.assertTrue(handoff["handoff"]["semantic_labels_locked"])
        self.assertEqual(handoff["scope"], "instance_subtree")
        self.assertEqual(handoff["subtree_root"], "DCacheTop.prober")
        self.assertEqual(handoff["semantic_labels"], [])

    def test_instance_subtree_handoff_budget_failure_is_blocked(self):
        frontend = StaticFrontend.from_firrtl(
            HIER.read_text(encoding="utf-8"),
            eager=False,
        )
        with self.assertRaises(HandoffNotReadyError):
            build_instance_static_handoff(
                frontend,
                "DCacheTop.prober::io.req.fire",
                root_instance="DCacheTop.prober",
                max_signals=1,
            )


if __name__ == "__main__":
    unittest.main()
