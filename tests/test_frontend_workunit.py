import unittest
from pathlib import Path

from frontend.dependency import DependencyEdge, DependencyKind
from frontend.partition import build_event_state_interaction_graph
from frontend.pipeline import StaticFrontend
from frontend.workunit import (
    WorkUnitConfig,
    WorkUnitDecision,
    WorkUnitKind,
    build_hierarchical_work_unit,
    work_unit_stats,
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


HUB_FIRRTL = r'''
FIRRTL version 7.0.0
circuit HubTop :
  public module HubTop : @[tests/HubTop.scala 1:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip a : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, b : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, flip c : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, d : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } } } @[tests/HubTop.scala 2:1]

    reg hub : UInt<1>, clock @[tests/HubTop.scala 10:1]
    reg ra : UInt<1>, clock @[tests/HubTop.scala 11:1]
    reg rb : UInt<1>, clock @[tests/HubTop.scala 12:1]

    node a_gate = and(hub, ra) @[tests/HubTop.scala 20:1]
    node b_gate = and(hub, ra) @[tests/HubTop.scala 21:1]
    node c_gate = and(hub, rb) @[tests/HubTop.scala 22:1]
    node d_gate = and(hub, rb) @[tests/HubTop.scala 23:1]
    io.a.ready <= a_gate @[tests/HubTop.scala 24:1]
    io.b.valid <= b_gate @[tests/HubTop.scala 25:1]
    io.b.bits.data <= UInt<8>("h1") @[tests/HubTop.scala 26:1]
    io.c.ready <= c_gate @[tests/HubTop.scala 27:1]
    io.d.valid <= d_gate @[tests/HubTop.scala 28:1]
    io.d.bits.data <= UInt<8>("h2") @[tests/HubTop.scala 29:1]

    when and(io.a.valid, io.a.ready) : @[tests/HubTop.scala 40:1]
      ra <= hub @[tests/HubTop.scala 41:1]
    when and(io.c.valid, io.c.ready) : @[tests/HubTop.scala 42:1]
      rb <= hub @[tests/HubTop.scala 43:1]
    hub <= xor(ra, rb) @[tests/HubTop.scala 44:1]
'''


STATE_FALLBACK_FIRRTL = r'''
FIRRTL version 7.0.0
circuit StateFallbackTop :
  public module StateFallbackTop : @[tests/StateFallbackTop.scala 1:1]
    input clock : Clock
    input reset : UInt<1>
    input tick_a : UInt<1>
    input tick_b : UInt<1>
    output io : { flip a : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, flip b : { flip ready : UInt<1>, valid : UInt<1>, bits : { data : UInt<8> } }, state_obs : UInt<1> } @[tests/StateFallbackTop.scala 2:1]

    reg ra : UInt<1>, clock @[tests/StateFallbackTop.scala 10:1]
    reg rb : UInt<1>, clock @[tests/StateFallbackTop.scala 11:1]

    io.a.ready <= UInt<1>("h1") @[tests/StateFallbackTop.scala 20:1]
    io.b.ready <= UInt<1>("h1") @[tests/StateFallbackTop.scala 21:1]

    node ra_next = xor(ra, tick_a) @[tests/StateFallbackTop.scala 30:1]
    ra <= ra_next @[tests/StateFallbackTop.scala 31:1]
    node rb_next = xor(rb, tick_b) @[tests/StateFallbackTop.scala 40:1]
    rb <= rb_next @[tests/StateFallbackTop.scala 41:1]

    io.state_obs <= xor(ra, rb) @[tests/StateFallbackTop.scala 50:1]
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
        graph = frontend.graph("SplitTop")
        shared_lines = {
            graph.statements[statement_id].source.line
            for statement_id in root.shared_statement_ids
            if graph.statements[statement_id].source is not None
        }
        # `both_busy = and(ra, rb)` directly couples the two child-owned
        # registers and must be explicit parent shared glue, even though no
        # child boundary event consumes this observation.
        self.assertIn(60, shared_lines)
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

    def test_immediate_frontier_stops_historical_fsm_pull_in(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        plan = frontend.partition("HubTop")
        a_cone = next(
            cone for cone in plan.event_cones
            if cone.event_id == "HubTop.io.a.fire"
        )
        self.assertEqual(set(a_cone.immediate_registers), {"hub", "ra"})
        # The full historical cone may reach rb through hub's next-state logic,
        # but ownership must not.
        self.assertIn("rb", a_cone.registers)
        self.assertNotIn("rb", a_cone.immediate_registers)

    def test_hub_state_is_promoted_instead_of_gluing_event_groups(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        plan = frontend.partition("HubTop")
        interaction = build_event_state_interaction_graph(plan)

        self.assertIn("hub", interaction.hub_registers)
        same = interaction.coupling("HubTop.io.a.fire", "HubTop.io.b.fire")
        cross = interaction.coupling("HubTop.io.a.fire", "HubTop.io.c.fire")
        self.assertIsNotNone(same)
        self.assertIsNotNone(cross)
        self.assertGreater(same.state_jaccard, 0.0)
        self.assertEqual(cross.state_jaccard, 0.0)
        self.assertIn("hub", cross.shared_hub_registers)

    def test_large_scc_can_split_below_shared_hub(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        plan = frontend.partition("HubTop")
        # hub <-> ra and hub <-> rb make one register SCC. The SCC is only a
        # structural hint; it must not be an atomic WorkUnit boundary.
        self.assertEqual(len(plan.regions), 1)

        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="HubTop",
            config=WorkUnitConfig(
                max_statements=1,
                min_child_statements=1,
            ),
        )
        self.assertEqual(root.decision, WorkUnitDecision.PARTITIONED)
        regions = [
            child for child in root.children
            if child.kind is WorkUnitKind.REGION
        ]
        self.assertEqual(len(regions), 2)
        self.assertIn("hub", root.local_state)
        self.assertEqual(
            {tuple(child.owned_state) for child in regions},
            {("ra",), ("rb",)},
        )
        self.assertTrue(root.coverage.complete)

    def test_bounded_ownership_expands_through_child_state_below_hub(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="HubTop",
            config=WorkUnitConfig(
                max_statements=1,
                min_child_statements=1,
            ),
        )
        regions = [
            child for child in root.children
            if child.kind is WorkUnitKind.REGION
        ]
        ra_child = next(child for child in regions if "ra" in child.owned_state)

        graph = frontend.graph("HubTop")
        child_lines = {
            graph.statements[statement_id].source.line
            for statement_id in ra_child.scope_statement_ids
            if graph.statements[statement_id].source is not None
        }
        parent_lines = {
            graph.statements[statement_id].source.line
            for statement_id in root.local_statement_ids
            if graph.statements[statement_id].source is not None
        }

        # ra <= hub is temporal child-local logic. Reading hub is a frontier
        # input and must not force the statement back to the parent.
        self.assertIn(41, child_lines)
        # hub <= xor(ra, rb) updates shared coordinator state and must remain
        # parent glue.
        self.assertNotIn(44, child_lines)
        self.assertIn(44, parent_lines)
        self.assertTrue(root.coverage.complete)

    def test_region_edge_complexity_ignores_unowned_whole_module_fanout(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        config = WorkUnitConfig(max_statements=1, min_child_statements=1)

        baseline = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="HubTop",
            config=config,
        )
        baseline_ra = next(
            child for child in baseline.children
            if child.kind is WorkUnitKind.REGION
            and "ra" in child.owned_state
        )

        graph = frontend.graph("HubTop")
        graph.edges.extend(
            DependencyEdge(
                src="a_gate",
                dst=f"synthetic_out_{index}",
                kind=DependencyKind.ALIAS,
                statement_ids=(10_000 + index,),
            )
            for index in range(64)
        )

        mutated = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="HubTop",
            config=config,
        )
        mutated_ra = next(
            child for child in mutated.children
            if child.kind is WorkUnitKind.REGION
            and "ra" in child.owned_state
        )

        # Whole-module fanout touching one child signal is not owned by the
        # child when its statement provenance lies outside the child scope.
        self.assertEqual(
            mutated_ra.complexity.dependency_edge_count,
            baseline_ra.complexity.dependency_edge_count,
        )


    def test_logical_edge_quotient_prevents_lowering_duplication_from_forcing_split(self):
        frontend = StaticFrontend.from_firrtl(HUB_FIRRTL)
        graph = frontend.graph("HubTop")
        template = graph.edges[0]
        graph.edges.extend(
            DependencyEdge(
                src=template.src,
                dst=template.dst,
                kind=template.kind,
                statement_ids=template.statement_ids,
                source=template.source,
            )
            for _ in range(128)
        )

        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="HubTop",
            config=WorkUnitConfig(
                max_source_loc=1_000,
                max_signals=1_000,
                max_registers=100,
                max_memories=100,
                max_events=100,
                max_dependency_edges=30,
                max_statements=1_000,
                max_state_sccs=100,
            ),
        )

        self.assertGreater(root.complexity.dependency_edge_count, 30)
        self.assertLess(root.complexity.logical_dependency_edge_count, 30)
        self.assertEqual(root.decision, WorkUnitDecision.MANAGEABLE)

    def test_logical_statement_and_signal_counts_preserve_raw_diagnostics(self):
        frontend = StaticFrontend.from_firrtl(
            HIERARCHY_FIXTURE.read_text(encoding="utf-8")
        )
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="BoomProbeUnit",
        )

        self.assertLess(
            root.complexity.logical_statement_count,
            root.complexity.statement_count,
        )
        self.assertLess(
            root.complexity.logical_signal_count,
            root.complexity.signal_count,
        )
        self.assertLessEqual(
            root.complexity.logical_dependency_edge_count,
            root.complexity.dependency_edge_count,
        )

    def test_replacement_complexity_tracks_only_parent_visible_rtl(self):
        frontend = self._split_frontend()
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="SplitTop",
            config=WorkUnitConfig(max_statements=1, min_child_statements=1),
        )
        self.assertEqual(root.decision, WorkUnitDecision.PARTITIONED)
        self.assertEqual(
            root.replacement_complexity.statement_count,
            len(root.local_statement_ids),
        )
        stats = work_unit_stats(root)[0]
        self.assertEqual(stats["child_summaries"], len(root.children))
        self.assertEqual(
            stats["replacement_complexity"]["statements"],
            len(root.local_statement_ids),
        )

    def test_event_rich_unit_falls_back_to_state_hierarchy(self):
        frontend = StaticFrontend.from_firrtl(STATE_FALLBACK_FIRRTL)
        root = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="StateFallbackTop",
            config=WorkUnitConfig(
                max_source_loc=100,
                max_signals=100,
                max_registers=100,
                max_memories=100,
                max_events=100,
                max_dependency_edges=1_000,
                max_statements=1,
                max_state_sccs=100,
                min_child_statements=2,
            ),
        )

        self.assertEqual(root.decision, WorkUnitDecision.PARTITIONED)
        state_children = [
            child
            for child in root.children
            if child.kind is WorkUnitKind.REGION and child.owned_state
        ]
        self.assertEqual(len(state_children), 2)
        self.assertEqual(
            {tuple(child.owned_state) for child in state_children},
            {("ra",), ("rb",)},
        )
        self.assertTrue(
            all(not child.event_ids for child in state_children),
            "fallback children must be state/dependency units, not event slices",
        )
        self.assertTrue(root.coverage.complete)

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
