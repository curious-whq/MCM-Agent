from pathlib import Path
import unittest

from frontend.boundary import discover_boundary
from frontend.dependency import build_module_dependency_graph
from frontend.firrtl import parse_firrtl
from frontend.partition import discover_partition_plan, register_dependency_edges
from frontend.registry import discover_decoupled_events


FIXTURE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"


class PartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = FIXTURE.read_text(encoding="utf-8")
        cls.design = parse_firrtl(cls.text)
        cls.module = cls.design.module("BoomProbeUnit")
        cls.graph = build_module_dependency_graph(
            cls.text, cls.design, "BoomProbeUnit"
        )
        cls.registry = discover_decoupled_events(
            cls.module, discover_boundary(cls.module)
        )

    def test_register_dependency_collapses_combinational_cones(self):
        edges = register_dependency_edges(self.graph)
        self.assertIn(("way_en", "state"), edges)
        self.assertIn(("state", "way_en"), edges)

    def test_state_scc_and_event_cones_are_structural(self):
        plan = discover_partition_plan(self.graph, self.registry)

        state_regions = [
            region
            for region in plan.regions
            if "state" in region.registers
        ]
        self.assertEqual(len(state_regions), 1)
        self.assertIn("way_en", state_regions[0].registers)
        self.assertIn(
            "BoomProbeUnit.io.rep.fire",
            state_regions[0].event_ids,
        )

        rep_cone = next(
            cone
            for cone in plan.event_cones
            if cone.event_id == "BoomProbeUnit.io.rep.fire"
        )
        self.assertIn("state", rep_cone.registers)
        self.assertIn("req", rep_cone.registers)
        self.assertTrue(rep_cone.complete)


if __name__ == "__main__":
    unittest.main()
