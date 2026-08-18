from pathlib import Path
import unittest

from frontend.abstraction_tree import AbstractionNodeKind, abstraction_tree_dict
from frontend.pipeline import StaticFrontend


FIXTURE = Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"


class AbstractionTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frontend = StaticFrontend.from_firrtl(
            FIXTURE.read_text(encoding="utf-8")
        )
        cls.tree = cls.frontend.abstraction_tree()

    def test_physical_instance_hierarchy_remains_primary(self):
        root = self.tree.root
        self.assertEqual(root.id, "DCacheTop")
        self.assertEqual(root.kind, AbstractionNodeKind.MODULE)

        probe_nodes = [
            child
            for child in root.children
            if child.kind is AbstractionNodeKind.MODULE
            and child.instance_path == "DCacheTop.prober"
        ]
        self.assertEqual(len(probe_nodes), 1)
        self.assertEqual(probe_nodes[0].module, "BoomProbeUnit")

    def test_probe_module_contains_static_state_region_work_unit(self):
        probe = next(
            child
            for child in self.tree.root.children
            if child.instance_path == "DCacheTop.prober"
            and child.kind is AbstractionNodeKind.MODULE
        )
        regions = [
            child
            for child in probe.children
            if child.kind is AbstractionNodeKind.STATE_REGION
        ]
        state_region = next(
            region for region in regions if "state" in region.registers
        )
        self.assertIn("way_en", state_region.registers)
        self.assertIn(
            "DCacheTop.prober::io.rep.fire",
            state_region.event_ids,
        )

    def test_tree_export_contains_no_semantic_region_name(self):
        data = abstraction_tree_dict(self.tree)
        serialized = repr(data)
        self.assertIn("state_region", serialized)
        self.assertNotIn("load ordering engine", serialized.lower())
        self.assertNotIn("probe controller", serialized.lower())


if __name__ == "__main__":
    unittest.main()
