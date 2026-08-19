import unittest
from pathlib import Path

from frontend.partition import build_event_state_interaction_graph
from frontend.pipeline import StaticFrontend
from frontend.workunit import (
    WorkUnitConfig,
    WorkUnitDecision,
    WorkUnitKind,
    build_hierarchical_work_unit,
)


HIERARCHY_FIXTURE = (
    Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"
)


SPLIT_FIRRTL = r'''
FIRRTL version 7.0.0
circuit SplitTop :
  public module SplitTop : @[tests/SplitTop.scala 1:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip a : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, b : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, flip c : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, d : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, shared : UInt<1> } @[tests/SplitTop.scala 2:1]

    reg ra : UInt<1>, clock @[tests/SplitTop.scala 10:1]
    reg rb : UInt<1>, clock @[tests/SplitTop.scala 11:1]

    io.a.ready <= eq(ra, UInt<1>("h0")) @[tests/SplitTop.scala 20:1]
    io.b.valid <= eq(ra, UInt<1>("h1")) @[tests/SplitTop.scala 21:1]
    io.b.bits.data <= UInt<8>("h1") @[tests/SplitTop.scala 22:1]
    io.c.ready <= eq(rb, UInt<1>("h0")) @[tests/SplitTop.scala 30:1]
    io.d.valid <= eq(rb, UInt<1>("h1")) @[tests/SplitTop.scala 31:1]
    io.d.bits.data <= UInt<8>("h2") @[tests/SplitTop.scala 32:1]

    when and(io.a.valid, io.a.ready) : @[tests/SplitTop.scala 40:1]
      ra <= UInt<1>("h1") @[tests/SplitTop.scala 41:1]
    when and(io.b.valid, io.b.ready) : @[tests/SplitTop.scala 42:1]
      ra <= UInt<1>("h0") @[tests/SplitTop.scala 43:1]

    when and(io.c.valid, io.c.ready) : @[tests/SplitTop.scala 50:1]
      rb <= UInt<1>("h1") @[tests/SplitTop.scala 51:1]
    when and(io.d.valid, io.d.ready) : @[tests/SplitTop.scala 52:1]
      rb <= UInt<1>("h0") @[tests/SplitTop.scala 53:1]

    node both_busy = and(ra, rb) @[tests/SplitTop.scala 60:1]
    io.shared <= both_busy @[tests/SplitTop.scala 61:1]
'''


class HierarchicalWorkUnitTests(unittest.TestCase):
    def _split_frontend(self):
        return StaticFrontend.from_firrtl(SPLIT_FIRRTL)

    def test_event_state_interaction_graph_separates_independent_state(self):
        frontend = self._split_frontend()
        plan = frontend.partition("SplitTop")
        interaction = build_event_state_interaction_graph(plan)

        same_a = interaction.coupling(
            "SplitTop.io.a.fire",
            "SplitTop.io.b.fire",
        )
        cross = interaction.coupling(
            "SplitTop.io.a.fire",
            "SplitTop.io.c.fire",
        )
        self.assertIsNotNone(same_a)
        self.assertIsNotNone(cross)
        self.assertGreater(same_a.state_jaccard, 0.0)
        self.assertEqual(cross.state_jaccard, 0.0)

    def test_recursive_partition_keeps_shared_logic_at_parent(self):
        frontend = self._split_frontend()
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="SplitTop",
            config=WorkUnitConfig(
                max_source_loc=1_000,
                max_signals=1_000,
                max_registers=100,
                max_memories=100,
                max_events=100,
                max_dependency_edges=10_000,
                max_statements=1,
                max_state_sccs=100,
                coupling_threshold=0.40,
                coupling_threshold_step=0.15,
                max_coupling_threshold=0.85,
                max_depth=4,
                min_child_statements=1,
            ),
        )

        self.assertEqual(root.decision, WorkUnitDecision.PARTITIONED)
        regions = [
            child
            for child in root.children
            if child.kind is WorkUnitKind.REGION
        ]
        self.assertEqual(len(regions), 2)
        self.assertTrue(root.shared_statement_ids)
        self.assertTrue(root.coverage.complete)

        child_statements = set().union(
            *(set(child.scope_statement_ids) for child in regions)
        )
        self.assertFalse(
            child_statements & set(root.local_statement_ids)
        )
        self.assertEqual(
            set(root.scope_statement_ids),
            child_statements | set(root.local_statement_ids),
        )

    def test_parent_input_replaces_child_internals_with_summary_slots(self):
        frontend = self._split_frontend()
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="SplitTop",
            config=WorkUnitConfig(max_statements=1, min_child_statements=1),
        )
        parent_input = root.parent_analysis_input()
        self.assertTrue(parent_input.coverage_complete)
        self.assertGreaterEqual(len(parent_input.children), 2)
        self.assertTrue(
            all(
                child.summary_ref.startswith("umcm://")
                for child in parent_input.children
            )
        )

        child_statements = set().union(
            *(
                set(child.scope_statement_ids)
                for child in root.children
                if child.kind is WorkUnitKind.REGION
            )
        )
        self.assertFalse(
            child_statements & set(parent_input.local_statement_ids)
        )

    def test_physical_module_children_remain_primary_work_units(self):
        frontend = StaticFrontend.from_firrtl(
            HIERARCHY_FIXTURE.read_text(encoding="utf-8")
        )
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="DCacheTop",
        )

        prober = next(
            child
            for child in root.children
            if child.kind is WorkUnitKind.MODULE
            and child.instance_path == "DCacheTop.prober"
        )
        self.assertEqual(prober.module, "BoomProbeUnit")
        replacement = next(
            child
            for child in root.parent_analysis_input().children
            if child.child_id == "DCacheTop.prober"
        )
        self.assertEqual(replacement.summary_ref, "umcm://DCacheTop.prober")
        self.assertTrue(replacement.frontier_signals)


if __name__ == "__main__":
    unittest.main()
