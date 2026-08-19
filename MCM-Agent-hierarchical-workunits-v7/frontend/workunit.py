from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from enum import Enum
from typing import Callable, Iterable

from .dependency import (
    DependencyKind,
    ModuleDependencyGraph,
    SignalKind,
    StatementStatus,
)
from .model import Design, ModuleDef, SourceLoc
from .partition import (
    EventStateInteractionGraph,
    PartitionPlan,
    StateRegion,
    build_event_state_interaction_graph,
    discover_partition_plan,
)
from .registry import EventRegistry
from .slice import SourceSpan


class WorkUnitKind(str, Enum):
    MODULE = "module"
    REGION = "region"
    EXTERNAL = "external"


class WorkUnitDecision(str, Enum):
    MANAGEABLE = "manageable"
    PARTITIONED = "partitioned"
    UNSPLITTABLE = "unsplittable"
    MAX_DEPTH = "max_depth"
    EXTERNAL = "external"


@dataclass(frozen=True)
class WorkUnitConfig:
    """Deterministic structural limits used to decide whether to *attempt* a cut.

    Crossing a limit never forces a partition by itself. A cut is accepted only
    when the Event-State Interaction Graph exposes at least two useful weakly
    coupled children and shared state/logic can remain at the parent.
    """

    max_source_loc: int = 450
    max_signals: int = 2_500
    max_registers: int = 96
    max_memories: int = 24
    max_events: int = 20
    max_dependency_edges: int = 6_000
    max_statements: int = 900
    max_state_sccs: int = 40
    coupling_threshold: float = 0.40
    coupling_threshold_step: float = 0.15
    max_coupling_threshold: float = 0.85
    max_depth: int = 6
    min_child_statements: int = 4


@dataclass(frozen=True)
class WorkUnitComplexity:
    source_loc: int
    signal_count: int
    register_count: int
    memory_count: int
    event_count: int
    dependency_edge_count: int
    statement_count: int
    state_scc_count: int
    event_state_coupling: float

    def exceeded(self, config: WorkUnitConfig) -> tuple[str, ...]:
        checks = (
            ("source_loc", self.source_loc, config.max_source_loc),
            ("signals", self.signal_count, config.max_signals),
            ("registers", self.register_count, config.max_registers),
            ("memories", self.memory_count, config.max_memories),
            ("events", self.event_count, config.max_events),
            (
                "dependency_edges",
                self.dependency_edge_count,
                config.max_dependency_edges,
            ),
            ("statements", self.statement_count, config.max_statements),
            ("state_sccs", self.state_scc_count, config.max_state_sccs),
        )
        return tuple(name for name, value, limit in checks if value > limit)


@dataclass(frozen=True)
class WorkUnitCoverage:
    """Conservation ledger for one same-module partition boundary."""

    scope_statement_ids: tuple[int, ...]
    local_statement_ids: tuple[int, ...]
    child_statement_ids: tuple[int, ...]
    missing_statement_ids: tuple[int, ...]
    duplicate_statement_ids: tuple[int, ...]
    unsupported_statement_ids: tuple[int, ...]
    scope_state_region_ids: tuple[str, ...]
    local_state_region_ids: tuple[str, ...]
    child_state_region_ids: tuple[str, ...]
    missing_state_region_ids: tuple[str, ...]
    duplicate_state_region_ids: tuple[str, ...]
    scope_event_ids: tuple[str, ...]
    local_event_ids: tuple[str, ...]
    child_event_ids: tuple[str, ...]
    missing_event_ids: tuple[str, ...]
    duplicate_event_ids: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not (
            self.missing_statement_ids
            or self.duplicate_statement_ids
            or self.unsupported_statement_ids
            or self.missing_state_region_ids
            or self.duplicate_state_region_ids
            or self.missing_event_ids
            or self.duplicate_event_ids
        )


@dataclass(frozen=True)
class ChildReplacement:
    child_id: str
    child_kind: WorkUnitKind
    summary_ref: str
    boundary_events: tuple[str, ...]
    frontier_signals: tuple[str, ...]


@dataclass(frozen=True)
class ParentAnalysisInput:
    """Static parent input after child internals have been removed.

    `local_statement_ids` contains only parent-local RTL. Every child appears as
    a summary slot plus its physical/static frontier. Child statement ids are
    intentionally absent from this package.
    """

    unit_id: str
    module: str
    local_statement_ids: tuple[int, ...]
    local_state: tuple[str, ...]
    local_events: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]
    children: tuple[ChildReplacement, ...]
    coverage_complete: bool


@dataclass(frozen=True)
class HierarchicalWorkUnit:
    id: str
    kind: WorkUnitKind
    instance_path: str
    module: str
    depth: int
    decision: WorkUnitDecision
    exceeded_limits: tuple[str, ...]
    complexity: WorkUnitComplexity
    event_ids: tuple[str, ...]
    local_event_ids: tuple[str, ...]
    owned_state: tuple[str, ...]
    local_state: tuple[str, ...]
    memory_state: tuple[str, ...]
    scope_statement_ids: tuple[int, ...]
    local_statement_ids: tuple[int, ...]
    shared_statement_ids: tuple[int, ...]
    frontier_signals: tuple[str, ...]
    parent_connection_signals: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]
    coverage: WorkUnitCoverage
    interaction_graph: EventStateInteractionGraph | None = None
    partition_threshold: float | None = None
    children: tuple["HierarchicalWorkUnit", ...] = ()

    def parent_analysis_input(self) -> ParentAnalysisInput:
        replacements = tuple(
            ChildReplacement(
                child_id=child.id,
                child_kind=child.kind,
                summary_ref=f"umcm://{child.id}",
                boundary_events=child.event_ids,
                frontier_signals=(
                    child.parent_connection_signals or child.frontier_signals
                ),
            )
            for child in self.children
        )
        return ParentAnalysisInput(
            unit_id=self.id,
            module=self.module,
            local_statement_ids=self.local_statement_ids,
            local_state=self.local_state,
            local_events=self.local_event_ids,
            source_spans=self.source_spans,
            children=replacements,
            coverage_complete=self.coverage.complete,
        )


def _is_prefix(root: str, name: str) -> bool:
    return (
        name == root
        or name.startswith(root + ".")
        or name.startswith(root + "[")
    )


def _state_root(roots: Iterable[str], signal: str) -> str | None:
    matches = [root for root in roots if _is_prefix(root, signal)]
    return max(matches, key=len) if matches else None


def _statement_refs(statement) -> set[str]:
    return set(statement.drives) | set(statement.reads) | set(
        statement.control_reads
    )


def _source_spans(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
) -> tuple[SourceSpan, ...]:
    by_file: dict[str, set[int]] = defaultdict(set)
    for statement_id in sorted(statement_ids):
        if not 0 <= statement_id < len(graph.statements):
            continue
        source = graph.statements[statement_id].source
        if source is not None and source.line > 0:
            by_file[source.file].add(source.line)

    spans: list[SourceSpan] = []
    for file in sorted(by_file):
        lines = sorted(by_file[file])
        if not lines:
            continue
        start = end = lines[0]
        for line in lines[1:]:
            if line <= end + 2:
                end = line
            else:
                spans.append(SourceSpan(file=file, start_line=start, end_line=end))
                start = end = line
        spans.append(SourceSpan(file=file, start_line=start, end_line=end))
    return tuple(spans)


def _source_loc_count(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
) -> int:
    source_lines: set[tuple[str, int]] = set()
    firrtl_lines: set[int] = set()
    for statement_id in statement_ids:
        if not 0 <= statement_id < len(graph.statements):
            continue
        statement = graph.statements[statement_id]
        if statement.source is not None and statement.source.line > 0:
            source_lines.add((statement.source.file, statement.source.line))
        else:
            firrtl_lines.add(statement.firrtl_line)
    return len(source_lines) + len(firrtl_lines)


def _concrete_event_id(
    module_name: str,
    instance_path: str,
    local_event_id: str,
) -> str:
    prefix = module_name + "."
    suffix = (
        local_event_id[len(prefix):]
        if local_event_id.startswith(prefix)
        else local_event_id
    )
    return f"{instance_path}::{suffix}"


def _local_event_id(
    module_name: str,
    concrete_event_id: str,
) -> str:
    if "::" not in concrete_event_id:
        return concrete_event_id
    _, suffix = concrete_event_id.split("::", 1)
    return f"{module_name}.{suffix}"


def _event_coupling_average(
    interaction: EventStateInteractionGraph,
    event_ids: set[str],
) -> float:
    scores = [
        coupling.score
        for coupling in interaction.couplings
        if (
            coupling.left_event in event_ids
            and coupling.right_event in event_ids
        )
    ]
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def _signals_for_scope(
    graph: ModuleDependencyGraph,
    plan: PartitionPlan,
    statement_ids: set[int],
    event_ids: set[str],
    *,
    full_module: bool,
) -> set[str]:
    if full_module:
        return set(graph.signals)

    signals: set[str] = set()
    for statement_id in statement_ids:
        if 0 <= statement_id < len(graph.statements):
            signals.update(_statement_refs(graph.statements[statement_id]))
    for cone in plan.event_cones:
        if cone.event_id in event_ids:
            signals.update(cone.signals)
    return signals


def _complexity(
    graph: ModuleDependencyGraph,
    plan: PartitionPlan,
    interaction: EventStateInteractionGraph,
    statement_ids: set[int],
    event_ids: set[str],
    state_region_ids: set[str],
    *,
    full_module: bool,
) -> WorkUnitComplexity:
    signals = _signals_for_scope(
        graph,
        plan,
        statement_ids,
        event_ids,
        full_module=full_module,
    )
    regions = {
        region.id: region
        for region in plan.regions
        if region.id in state_region_ids
    }
    registers = {
        register
        for region in regions.values()
        for register in region.registers
    }
    if full_module:
        registers = set(graph.register_roots)

    memories = {
        root
        for root in graph.memory_roots
        if any(_is_prefix(root, signal) for signal in signals)
    }
    if full_module:
        memories = set(graph.memory_roots)

    if full_module:
        edge_count = len(graph.edges)
    else:
        edge_count = sum(
            1
            for edge in graph.edges
            if (
                edge.src in signals
                or edge.dst in signals
                or bool(set(edge.statement_ids) & statement_ids)
            )
        )

    return WorkUnitComplexity(
        source_loc=_source_loc_count(graph, statement_ids),
        signal_count=len(signals),
        register_count=len(registers),
        memory_count=len(memories),
        event_count=len(event_ids),
        dependency_edge_count=edge_count,
        statement_count=len(statement_ids),
        state_scc_count=len(state_region_ids),
        event_state_coupling=_event_coupling_average(
            interaction,
            event_ids,
        ),
    )


def _statement_state_regions(
    graph: ModuleDependencyGraph,
    plan: PartitionPlan,
) -> dict[int, set[str]]:
    region_for_register = {
        register: region.id
        for region in plan.regions
        for register in region.registers
    }
    out: dict[int, set[str]] = defaultdict(set)
    register_roots = tuple(region_for_register)
    for statement in graph.statements:
        for signal in _statement_refs(statement):
            root = _state_root(register_roots, signal)
            if root is not None:
                out[statement.id].add(region_for_register[root])
    return out


def _frontier_signals(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
) -> tuple[str, ...]:
    inside = set(statement_ids)
    signal_owners: dict[str, set[bool]] = defaultdict(set)
    touched_inside: set[str] = set()

    for statement in graph.statements:
        in_scope = statement.id in inside
        for signal in _statement_refs(statement):
            signal_owners[signal].add(in_scope)
            if in_scope:
                touched_inside.add(signal)

    frontier: set[str] = set()
    for signal in touched_inside:
        info = graph.signals.get(signal)
        if len(signal_owners[signal]) > 1:
            frontier.add(signal)
        elif signal in graph.input_ports or signal in graph.output_ports:
            frontier.add(signal)
        elif info is not None and info.kind is SignalKind.INSTANCE_PORT:
            frontier.add(signal)
    return tuple(sorted(frontier))


def _coverage(
    graph: ModuleDependencyGraph,
    scope_statements: set[int],
    local_statements: set[int],
    child_statement_scopes: list[set[int]],
    scope_states: set[str],
    local_states: set[str],
    child_state_scopes: list[set[str]],
    scope_events: set[str],
    local_events: set[str],
    child_event_scopes: list[set[str]],
) -> WorkUnitCoverage:
    statement_counter = Counter(local_statements)
    for child_scope in child_statement_scopes:
        statement_counter.update(child_scope)

    state_counter = Counter(local_states)
    for child_scope in child_state_scopes:
        state_counter.update(child_scope)

    event_counter = Counter(local_events)
    for child_scope in child_event_scopes:
        event_counter.update(child_scope)

    unsupported = {
        statement_id
        for statement_id in scope_statements
        if (
            0 <= statement_id < len(graph.statements)
            and graph.statements[statement_id].status
            is StatementStatus.UNSUPPORTED
        )
    }

    return WorkUnitCoverage(
        scope_statement_ids=tuple(sorted(scope_statements)),
        local_statement_ids=tuple(sorted(local_statements)),
        child_statement_ids=tuple(
            sorted(
                set().union(*child_statement_scopes)
                if child_statement_scopes
                else set()
            )
        ),
        missing_statement_ids=tuple(
            sorted(scope_statements - set(statement_counter))
        ),
        duplicate_statement_ids=tuple(
            sorted(
                statement_id
                for statement_id, count in statement_counter.items()
                if statement_id in scope_statements and count > 1
            )
        ),
        unsupported_statement_ids=tuple(sorted(unsupported)),
        scope_state_region_ids=tuple(sorted(scope_states)),
        local_state_region_ids=tuple(sorted(local_states)),
        child_state_region_ids=tuple(
            sorted(
                set().union(*child_state_scopes)
                if child_state_scopes
                else set()
            )
        ),
        missing_state_region_ids=tuple(
            sorted(scope_states - set(state_counter))
        ),
        duplicate_state_region_ids=tuple(
            sorted(
                state_id
                for state_id, count in state_counter.items()
                if state_id in scope_states and count > 1
            )
        ),
        scope_event_ids=tuple(sorted(scope_events)),
        local_event_ids=tuple(sorted(local_events)),
        child_event_ids=tuple(
            sorted(
                set().union(*child_event_scopes)
                if child_event_scopes
                else set()
            )
        ),
        missing_event_ids=tuple(
            sorted(scope_events - set(event_counter))
        ),
        duplicate_event_ids=tuple(
            sorted(
                event_id
                for event_id, count in event_counter.items()
                if event_id in scope_events and count > 1
            )
        ),
    )


def _components_at_threshold(
    event_ids: set[str],
    interaction: EventStateInteractionGraph,
    threshold: float,
) -> list[set[str]]:
    adjacency: dict[str, set[str]] = {
        event_id: set()
        for event_id in event_ids
    }
    for coupling in interaction.couplings:
        if (
            coupling.left_event in event_ids
            and coupling.right_event in event_ids
            and coupling.score >= threshold
        ):
            adjacency[coupling.left_event].add(coupling.right_event)
            adjacency[coupling.right_event].add(coupling.left_event)

    components: list[set[str]] = []
    remaining = set(event_ids)
    while remaining:
        seed = min(remaining)
        stack = [seed]
        component: set[str] = set()
        while stack:
            event_id = stack.pop()
            if event_id in component:
                continue
            component.add(event_id)
            stack.extend(sorted(adjacency[event_id] - component, reverse=True))
        remaining -= component
        components.append(component)
    return sorted(components, key=lambda component: tuple(sorted(component)))


def _candidate_thresholds(
    config: WorkUnitConfig,
    depth: int,
) -> tuple[float, ...]:
    first = min(
        config.max_coupling_threshold,
        config.coupling_threshold
        + max(0, depth - 1) * config.coupling_threshold_step,
    )
    values: list[float] = []
    value = first
    while value <= config.max_coupling_threshold + 1e-9:
        values.append(round(value, 6))
        value += config.coupling_threshold_step
    return tuple(values)


def _owned_state_by_group(
    groups: list[set[str]],
    scope_states: set[str],
    scope_events: set[str],
    plan: PartitionPlan,
) -> tuple[list[set[str]], set[str]]:
    states_by_group = [set() for _ in groups]
    shared: set[str] = set()
    regions = {region.id: region for region in plan.regions}
    delegated_events = set().union(*groups) if groups else set()
    parent_events = scope_events - delegated_events

    for state_id in scope_states:
        region = regions[state_id]
        region_events = set(region.event_ids) & scope_events
        owners = [
            index
            for index, events in enumerate(groups)
            if region_events & events
        ]
        # If a state is also touched by an event retained at the parent, it
        # cannot be delegated even when only one child group touches it.
        parent_touches = bool(region_events & parent_events)
        if len(owners) == 1 and not parent_touches:
            states_by_group[owners[0]].add(state_id)
        else:
            # State touched by multiple children, by parent-local events, or
            # not attributable to an event is deliberately retained above.
            shared.add(state_id)
    return states_by_group, shared


def _desired_statements_by_group(
    groups: list[set[str]],
    states_by_group: list[set[str]],
    scope_statements: set[int],
    plan: PartitionPlan,
    statement_states: dict[int, set[str]],
) -> list[set[int]]:
    cone_statements = {
        cone.event_id: set(cone.statement_ids)
        for cone in plan.event_cones
    }
    desired: list[set[int]] = []
    for events, states in zip(groups, states_by_group):
        statements: set[int] = set()
        for event_id in events:
            statements.update(cone_statements.get(event_id, ()))
        for statement_id, touched_states in statement_states.items():
            if touched_states & states:
                statements.add(statement_id)
        desired.append(statements & scope_statements)
    return desired


def _exclusive_statement_scopes(
    desired: list[set[int]],
) -> tuple[list[set[int]], set[int]]:
    owners: dict[int, list[int]] = defaultdict(list)
    for index, statements in enumerate(desired):
        for statement_id in statements:
            owners[statement_id].append(index)

    exclusive = [set() for _ in desired]
    shared: set[int] = set()
    for statement_id, indexes in owners.items():
        if len(indexes) == 1:
            exclusive[indexes[0]].add(statement_id)
        else:
            shared.add(statement_id)
    return exclusive, shared


def _partition_scopes_for_groups(
    groups: list[set[str]],
    scope_statements: set[int],
    scope_events: set[str],
    scope_states: set[str],
    plan: PartitionPlan,
    statement_states: dict[int, set[str]],
    min_child_statements: int,
) -> tuple[list[set[str]], list[set[str]], list[set[int]], set[int]] | None:
    """Turn event groups into exclusive child ownership scopes.

    The loop is intentionally conservative. If dropping a weak/empty child
    makes one of its events parent-local, state and statements touched by that
    event are reclassified as parent glue before the cut is accepted.
    """

    active = [set(group) for group in groups if group]
    cone_statements = {
        cone.event_id: set(cone.statement_ids)
        for cone in plan.event_cones
    }

    while len(active) >= 2:
        states_by_group, _ = _owned_state_by_group(
            active,
            scope_states,
            scope_events,
            plan,
        )
        desired = _desired_statements_by_group(
            active,
            states_by_group,
            scope_statements,
            plan,
            statement_states,
        )
        exclusive, shared = _exclusive_statement_scopes(desired)

        delegated_events = set().union(*active)
        parent_events = scope_events - delegated_events
        delegated_states = (
            set().union(*states_by_group) if states_by_group else set()
        )
        parent_states = scope_states - delegated_states

        protected: set[int] = set()
        for event_id in parent_events:
            protected.update(cone_statements.get(event_id, ()))
        for statement_id, touched_states in statement_states.items():
            if touched_states & parent_states:
                protected.add(statement_id)
        protected &= scope_statements

        for statements in exclusive:
            statements -= protected
        shared |= protected & set().union(*desired) if desired else set()

        useful = [
            index
            for index, statements in enumerate(exclusive)
            if (
                len(statements) >= min_child_statements
                or bool(states_by_group[index])
            )
        ]
        if len(useful) < 2:
            return None
        if len(useful) == len(active):
            return active, states_by_group, exclusive, shared
        active = [active[index] for index in useful]

    return None


def _resolve_root_instance(
    design: Design,
    root_instance: str | None,
    root_module: str | None,
) -> tuple[str, str, SourceLoc | None]:
    if root_instance is not None and root_module is not None:
        raise ValueError("Choose either root_instance or root_module, not both")

    if root_module is not None:
        module = design.module(root_module)
        return root_module, root_module, module.source

    if root_instance is None:
        module = design.module(design.top)
        return design.top, design.top, module.source

    parts = root_instance.split(".")
    if not parts or parts[0] != design.top:
        raise KeyError(
            f"Concrete root {root_instance!r} must start at design top "
            f"{design.top!r}; use root_module for a module-type root"
        )

    module_name = design.top
    source = design.module(module_name).source
    path = design.top
    for instance_name in parts[1:]:
        module = design.module(module_name)
        instance = next(
            (
                candidate
                for candidate in module.instances
                if candidate.name == instance_name
            ),
            None,
        )
        if instance is None:
            raise KeyError(f"Unknown instance path component: {path}.{instance_name}")
        module_name = instance.module
        source = instance.source
        path = f"{path}.{instance_name}"
    return module_name, path, source


def build_hierarchical_work_unit(
    design: Design,
    graph_for_module: Callable[[str], ModuleDependencyGraph],
    registries: dict[str, EventRegistry],
    *,
    root_instance: str | None = None,
    root_module: str | None = None,
    config: WorkUnitConfig | None = None,
) -> HierarchicalWorkUnit:
    """Build a recursive physical + state/dependency work-unit hierarchy."""

    config = config or WorkUnitConfig()
    root_module_name, root_path, root_source = _resolve_root_instance(
        design,
        root_instance,
        root_module,
    )

    def build_module(
        module_name: str,
        instance_path: str,
        source: SourceLoc | None,
        depth: int,
        stack: tuple[str, ...],
        parent_connection_signals: tuple[str, ...] = (),
    ) -> HierarchicalWorkUnit:
        if module_name in stack:
            raise ValueError(
                "Recursive module hierarchy detected: "
                + " -> ".join(stack + (module_name,))
            )

        module = design.modules.get(module_name)
        if module is None or module.external:
            empty_complexity = WorkUnitComplexity(
                source_loc=0,
                signal_count=0,
                register_count=0,
                memory_count=0,
                event_count=0,
                dependency_edge_count=0,
                statement_count=0,
                state_scc_count=0,
                event_state_coupling=0.0,
            )
            empty_coverage = WorkUnitCoverage(
                scope_statement_ids=(),
                local_statement_ids=(),
                child_statement_ids=(),
                missing_statement_ids=(),
                duplicate_statement_ids=(),
                unsupported_statement_ids=(),
                scope_state_region_ids=(),
                local_state_region_ids=(),
                child_state_region_ids=(),
                missing_state_region_ids=(),
                duplicate_state_region_ids=(),
                scope_event_ids=(),
                local_event_ids=(),
                child_event_ids=(),
                missing_event_ids=(),
                duplicate_event_ids=(),
            )
            return HierarchicalWorkUnit(
                id=instance_path,
                kind=WorkUnitKind.EXTERNAL,
                instance_path=instance_path,
                module=module_name,
                depth=depth,
                decision=WorkUnitDecision.EXTERNAL,
                exceeded_limits=(),
                complexity=empty_complexity,
                event_ids=(),
                local_event_ids=(),
                owned_state=(),
                local_state=(),
                memory_state=(),
                scope_statement_ids=(),
                local_statement_ids=(),
                shared_statement_ids=(),
                frontier_signals=(),
                parent_connection_signals=parent_connection_signals,
                source_spans=(),
                coverage=empty_coverage,
                children=(),
            )

        graph = graph_for_module(module_name)
        registry = registries[module_name]
        plan = discover_partition_plan(graph, registry)
        interaction = build_event_state_interaction_graph(plan)
        regions = {region.id: region for region in plan.regions}
        statement_states = _statement_state_regions(graph, plan)

        all_statement_ids = set(range(len(graph.statements)))
        all_event_ids = set(interaction.event_ids)
        all_state_ids = set(interaction.state_region_ids)

        def build_region(
            unit_id: str,
            scope_statements: set[int],
            scope_events: set[str],
            scope_states: set[str],
            region_depth: int,
            *,
            kind: WorkUnitKind,
            full_module: bool,
        ) -> HierarchicalWorkUnit:
            metrics = _complexity(
                graph,
                plan,
                interaction,
                scope_statements,
                scope_events,
                scope_states,
                full_module=full_module,
            )
            exceeded = metrics.exceeded(config)

            child_specs: list[
                tuple[str, set[int], set[str], set[str], set[int], float]
            ] = []
            shared_statement_ids: set[int] = set()
            threshold_used: float | None = None
            decision = WorkUnitDecision.MANAGEABLE

            if exceeded:
                if region_depth >= config.max_depth:
                    decision = WorkUnitDecision.MAX_DEPTH
                elif len(scope_events) >= 2:
                    for threshold in _candidate_thresholds(config, region_depth):
                        groups = _components_at_threshold(
                            scope_events,
                            interaction,
                            threshold,
                        )
                        if len(groups) < 2:
                            continue

                        scopes = _partition_scopes_for_groups(
                            groups,
                            scope_statements,
                            scope_events,
                            scope_states,
                            plan,
                            statement_states,
                            config.min_child_statements,
                        )
                        if scopes is None:
                            continue
                        (
                            groups,
                            states_by_group,
                            exclusive,
                            shared,
                        ) = scopes

                        for ordinal, (
                            child_events,
                            child_states,
                            child_statements,
                        ) in enumerate(
                            zip(groups, states_by_group, exclusive)
                        ):
                            child_specs.append(
                                (
                                    f"{unit_id}::region-{region_depth}-{ordinal}",
                                    child_statements,
                                    child_events,
                                    child_states,
                                    set(),
                                    threshold,
                                )
                            )
                        shared_statement_ids = shared & scope_statements
                        threshold_used = threshold
                        decision = WorkUnitDecision.PARTITIONED
                        break

                    if not child_specs:
                        decision = WorkUnitDecision.UNSPLITTABLE
                elif len(scope_states) >= 2:
                    # Event-less / single-event fallback: independent state
                    # SCCs may still form useful children. Any statement
                    # touching multiple SCCs is retained as parent glue.
                    groups = [{state_id} for state_id in sorted(scope_states)]
                    desired = []
                    for state_group in groups:
                        desired.append(
                            {
                                statement_id
                                for statement_id, states in statement_states.items()
                                if states & state_group
                            }
                            & scope_statements
                        )
                    exclusive, shared = _exclusive_statement_scopes(desired)
                    useful = [
                        index
                        for index, statements in enumerate(exclusive)
                        if len(statements) >= config.min_child_statements
                    ]
                    if len(useful) >= 2:
                        for ordinal, index in enumerate(useful):
                            child_specs.append(
                                (
                                    f"{unit_id}::region-{region_depth}-{ordinal}",
                                    exclusive[index],
                                    set(),
                                    groups[index],
                                    set(),
                                    1.0,
                                )
                            )
                        shared_statement_ids = shared & scope_statements
                        threshold_used = 1.0
                        decision = WorkUnitDecision.PARTITIONED
                    else:
                        decision = WorkUnitDecision.UNSPLITTABLE
                else:
                    decision = WorkUnitDecision.UNSPLITTABLE

            child_statement_scopes = [spec[1] for spec in child_specs]
            child_event_scopes = [spec[2] for spec in child_specs]
            child_state_scopes = [spec[3] for spec in child_specs]

            delegated_statements = set().union(*child_statement_scopes) if child_statement_scopes else set()
            delegated_events = set().union(*child_event_scopes) if child_event_scopes else set()
            delegated_states = set().union(*child_state_scopes) if child_state_scopes else set()

            local_statements = scope_statements - delegated_statements
            local_events = scope_events - delegated_events
            local_states = scope_states - delegated_states

            children = tuple(
                build_region(
                    child_id,
                    child_statements,
                    child_events,
                    child_states,
                    region_depth + 1,
                    kind=WorkUnitKind.REGION,
                    full_module=False,
                )
                for (
                    child_id,
                    child_statements,
                    child_events,
                    child_states,
                    _,
                    _,
                ) in child_specs
            )

            coverage = _coverage(
                graph,
                scope_statements,
                local_statements,
                child_statement_scopes,
                scope_states,
                local_states,
                child_state_scopes,
                scope_events,
                local_events,
                child_event_scopes,
            )

            scope_registers = tuple(
                sorted(
                    register
                    for state_id in scope_states
                    for register in regions[state_id].registers
                )
            )
            local_registers = tuple(
                sorted(
                    register
                    for state_id in local_states
                    for register in regions[state_id].registers
                )
            )
            signals = _signals_for_scope(
                graph,
                plan,
                scope_statements,
                scope_events,
                full_module=full_module,
            )
            memories = tuple(
                sorted(
                    root
                    for root in graph.memory_roots
                    if (
                        full_module
                        or any(_is_prefix(root, signal) for signal in signals)
                    )
                )
            )

            return HierarchicalWorkUnit(
                id=unit_id,
                kind=kind,
                instance_path=instance_path,
                module=module_name,
                depth=region_depth,
                decision=decision,
                exceeded_limits=exceeded,
                complexity=metrics,
                event_ids=tuple(
                    sorted(
                        _concrete_event_id(
                            module_name,
                            instance_path,
                            event_id,
                        )
                        for event_id in scope_events
                    )
                ),
                local_event_ids=tuple(
                    sorted(
                        _concrete_event_id(
                            module_name,
                            instance_path,
                            event_id,
                        )
                        for event_id in local_events
                    )
                ),
                owned_state=scope_registers,
                local_state=local_registers,
                memory_state=memories,
                scope_statement_ids=tuple(sorted(scope_statements)),
                local_statement_ids=tuple(sorted(local_statements)),
                shared_statement_ids=tuple(sorted(shared_statement_ids)),
                frontier_signals=_frontier_signals(graph, scope_statements),
                parent_connection_signals=(),
                source_spans=_source_spans(graph, scope_statements),
                coverage=coverage,
                interaction_graph=interaction if kind is WorkUnitKind.MODULE else None,
                partition_threshold=threshold_used,
                children=children,
            )

        local_root = build_region(
            instance_path,
            all_statement_ids,
            all_event_ids,
            all_state_ids,
            depth,
            kind=WorkUnitKind.MODULE,
            full_module=True,
        )

        physical_children: list[HierarchicalWorkUnit] = []
        for instance in module.instances:
            child_path = f"{instance_path}.{instance.name}"
            parent_signals = tuple(
                sorted(
                    signal
                    for signal in graph.signals
                    if (
                        signal == instance.name
                        or signal.startswith(instance.name + ".")
                        or signal.startswith(instance.name + "[")
                    )
                )
            )
            child = build_module(
                instance.module,
                child_path,
                instance.source,
                depth + 1,
                stack + (module_name,),
                parent_connection_signals=parent_signals,
            )
            physical_children.append(child)

        if parent_connection_signals:
            local_root = replace(
                local_root,
                parent_connection_signals=parent_connection_signals,
            )

        return replace(
            local_root,
            children=tuple(
                sorted(
                    local_root.children + tuple(physical_children),
                    key=lambda child: (child.kind.value, child.id),
                )
            ),
        )

    return build_module(
        root_module_name,
        root_path,
        root_source,
        0,
        (),
    )


def flatten_work_units(
    root: HierarchicalWorkUnit,
) -> tuple[HierarchicalWorkUnit, ...]:
    out: list[HierarchicalWorkUnit] = []

    def visit(unit: HierarchicalWorkUnit) -> None:
        out.append(unit)
        for child in unit.children:
            visit(child)

    visit(root)
    return tuple(out)


def _complexity_dict(complexity: WorkUnitComplexity) -> dict:
    return {
        "source_loc": complexity.source_loc,
        "signals": complexity.signal_count,
        "registers": complexity.register_count,
        "memories": complexity.memory_count,
        "events": complexity.event_count,
        "dependency_edges": complexity.dependency_edge_count,
        "statements": complexity.statement_count,
        "state_sccs": complexity.state_scc_count,
        "event_state_coupling": round(complexity.event_state_coupling, 6),
    }


def _coverage_dict(coverage: WorkUnitCoverage) -> dict:
    return {
        "complete": coverage.complete,
        "scope_statements": len(coverage.scope_statement_ids),
        "local_statements": len(coverage.local_statement_ids),
        "child_statements": len(coverage.child_statement_ids),
        "missing_statement_ids": list(coverage.missing_statement_ids),
        "duplicate_statement_ids": list(coverage.duplicate_statement_ids),
        "unsupported_statement_ids": list(coverage.unsupported_statement_ids),
        "scope_state_regions": len(coverage.scope_state_region_ids),
        "local_state_regions": len(coverage.local_state_region_ids),
        "child_state_regions": len(coverage.child_state_region_ids),
        "missing_state_region_ids": list(coverage.missing_state_region_ids),
        "duplicate_state_region_ids": list(coverage.duplicate_state_region_ids),
        "scope_events": len(coverage.scope_event_ids),
        "local_events": len(coverage.local_event_ids),
        "child_events": len(coverage.child_event_ids),
        "missing_event_ids": list(coverage.missing_event_ids),
        "duplicate_event_ids": list(coverage.duplicate_event_ids),
    }


def work_unit_tree_dict(root: HierarchicalWorkUnit) -> dict:
    def encode(unit: HierarchicalWorkUnit) -> dict:
        return {
            "id": unit.id,
            "kind": unit.kind.value,
            "instance_path": unit.instance_path,
            "module": unit.module,
            "depth": unit.depth,
            "decision": unit.decision.value,
            "exceeded_limits": list(unit.exceeded_limits),
            "complexity": _complexity_dict(unit.complexity),
            "events": list(unit.event_ids),
            "owned_state": list(unit.owned_state),
            "local_state": list(unit.local_state),
            "shared_statement_ids": list(unit.shared_statement_ids),
            "coverage": _coverage_dict(unit.coverage),
            "children": [encode(child) for child in unit.children],
        }

    return encode(root)


def work_unit_stats(root: HierarchicalWorkUnit) -> list[dict]:
    return [
        {
            "id": unit.id,
            "kind": unit.kind.value,
            "instance_path": unit.instance_path,
            "module": unit.module,
            "depth": unit.depth,
            "decision": unit.decision.value,
            "exceeded_limits": list(unit.exceeded_limits),
            **_complexity_dict(unit.complexity),
            "local_statements": len(unit.local_statement_ids),
            "shared_statements": len(unit.shared_statement_ids),
            "frontier_signals": len(unit.frontier_signals),
            "coverage_complete": unit.coverage.complete,
        }
        for unit in flatten_work_units(root)
    ]


def _source_span_dict(span: SourceSpan) -> dict:
    return {
        "file": span.file,
        "start_line": span.start_line,
        "end_line": span.end_line,
    }


def _interaction_dict(
    graph: EventStateInteractionGraph | None,
) -> dict | None:
    if graph is None:
        return None
    return {
        "module": graph.module,
        "event_ids": list(graph.event_ids),
        "state_region_ids": list(graph.state_region_ids),
        "touches": [
            {
                "event_id": touch.event_id,
                "state_region_id": touch.state_region_id,
                "registers": list(touch.registers),
            }
            for touch in graph.touches
        ],
        "couplings": [
            {
                "left_event": coupling.left_event,
                "right_event": coupling.right_event,
                "shared_state_regions": list(coupling.shared_state_regions),
                "shared_registers": list(coupling.shared_registers),
                "shared_statement_count": len(coupling.shared_statement_ids),
                "state_jaccard": round(coupling.state_jaccard, 6),
                "statement_jaccard": round(coupling.statement_jaccard, 6),
                "score": round(coupling.score, 6),
            }
            for coupling in graph.couplings
            if coupling.score > 0.0
        ],
        "average_coupling": round(graph.average_coupling, 6),
    }


def work_unit_plan_dict(root: HierarchicalWorkUnit) -> dict:
    def encode(unit: HierarchicalWorkUnit) -> dict:
        parent_input = unit.parent_analysis_input()
        return {
            "id": unit.id,
            "kind": unit.kind.value,
            "instance_path": unit.instance_path,
            "module": unit.module,
            "decision": unit.decision.value,
            "partition_threshold": unit.partition_threshold,
            "complexity": _complexity_dict(unit.complexity),
            "scope": {
                "events": list(unit.event_ids),
                "owned_state": list(unit.owned_state),
                "memory_state": list(unit.memory_state),
                "statement_ids": list(unit.scope_statement_ids),
                "frontier_signals": list(unit.frontier_signals),
                "source_spans": [
                    _source_span_dict(span)
                    for span in unit.source_spans
                ],
            },
            "parent_local": {
                "events": list(unit.local_event_ids),
                "state": list(unit.local_state),
                "statement_ids": list(unit.local_statement_ids),
                "shared_statement_ids": list(unit.shared_statement_ids),
            },
            "coverage": _coverage_dict(unit.coverage),
            "interaction_graph": _interaction_dict(unit.interaction_graph),
            "replacement_input": {
                "local_statement_ids": list(parent_input.local_statement_ids),
                "local_state": list(parent_input.local_state),
                "local_events": list(parent_input.local_events),
                "coverage_complete": parent_input.coverage_complete,
                "children": [
                    {
                        "child_id": child.child_id,
                        "child_kind": child.child_kind.value,
                        "summary_ref": child.summary_ref,
                        "boundary_events": list(child.boundary_events),
                        "frontier_signals": list(child.frontier_signals),
                    }
                    for child in parent_input.children
                ],
            },
            "children": [encode(child) for child in unit.children],
        }

    return encode(root)
