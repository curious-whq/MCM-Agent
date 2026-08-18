from pathlib import Path
import unittest

from frontend.dependency import build_all_dependency_graphs
from frontend.design_graph import (
    backward_design_slice,
    discover_design_events,
    flatten_design_dependency_graph,
)
from frontend.firrtl import parse_firrtl


FIXTURE = Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"


class DesignGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = FIXTURE.read_text(encoding="utf-8")
        cls.design = parse_firrtl(cls.text)
        cls.local = build_all_dependency_graphs(cls.text, cls.design)
        cls.graph = flatten_design_dependency_graph(
            cls.text,
            cls.design,
            cls.local,
        )
        cls.events = {
            event.event_id: event
            for event in discover_design_events(cls.design)
        }

    def test_parent_instance_port_and_child_port_share_flat_identity(self):
        signal = "DCacheTop.prober::io.rep.valid"
        self.assertIn(signal, self.graph.signals)
        self.assertEqual(self.graph.signals[signal].module, "BoomProbeUnit")
        self.assertEqual(self.graph.signals[signal].kind.value, "port")
        self.assertTrue(
            any(
                edge.src == "DCacheTop.prober::state"
                and edge.dst == signal
                for edge in self.graph.edges
            )
        )
        self.assertTrue(
            any(
                edge.src == signal
                and edge.dst == "DCacheTop::io.tl_c.valid"
                for edge in self.graph.edges
            )
        )

    def test_design_registry_instantiates_endpoint_events(self):
        self.assertIn("DCacheTop::io.tl_c.fire", self.events)
        self.assertIn("DCacheTop.prober::io.rep.fire", self.events)
        self.assertIn("DCacheTop.prober::io.req.fire", self.events)

    def test_top_c_response_slice_crosses_into_probeunit_fsm(self):
        event = self.events["DCacheTop::io.tl_c.fire"]
        result = backward_design_slice(
            self.graph,
            event.seeds(include_payload=False),
        )

        self.assertIn("DCacheTop.prober::state", result.signals)
        self.assertIn("DCacheTop.prober::io.lsu_release.ready", result.signals)
        self.assertIn("DCacheTop::io.tl_b.valid", result.signals)
        self.assertIn("DCacheTop.prober", result.instances)
        self.assertIn("DCacheTop", result.instances)

    def test_top_input_is_a_hierarchical_frontier(self):
        event = self.events["DCacheTop::io.tl_c.fire"]
        result = backward_design_slice(self.graph, event.seeds())
        self.assertIn("DCacheTop::io.tl_c.ready", result.frontier)
        self.assertIn("DCacheTop::io.tl_b.valid", result.frontier)


if __name__ == "__main__":
    unittest.main()
