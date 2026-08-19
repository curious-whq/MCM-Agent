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

    max_source_loc: int = 600
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
    # High-degree immediate state in event-rich modules is coordination glue.
    # It remains at the parent instead of gluing all event groups together.
    hub_event_ratio: float = 0.60
    hub_min_touch_events: int = 3
    hub_min_module_events: int = 4


@dataclass(frozen=True)
class WorkUnitComplexity:
    # `source_loc` is the raw conservative count (mapped source lines plus
    # unmapped FIRRTL lines). `logical_source_loc` uses mapped source lines
    # when provenance exists, falling back to FIRRTL lines only for an
    # entirely unmapped scope.
    source_loc: int
    logical_source_loc: int
    unmapped_firrtl_loc: int
    # Raw FIRRTL counts remain available for debugging/provenance.  Structural
    # manageability decisions use the logical quotient counts below so Chisel
    # aggregate/lowering expansion does not masquerade as semantic complexity.
    signal_count: int
    logical_signal_count: int
    register_count: int
    memory_count: int
    event_count: int
    dependency_edge_count: int
    logical_dependency_edge_count: int
    statement_count: int
    logical_statement_count: int
    state_scc_count: int
    event_state_coupling: float

    def exceeded(self, config: WorkUnitConfig) -> tuple[str, ...]:
        checks = (
            (
                "source_loc",
                self.logical_source_loc,
                config.max_source_loc,
            ),
            ("signals", self.logical_signal_count, config.max_signals),
            ("registers", self.register_count, config.max_registers),
            ("memories", self.memory_count, config.max_memories),
            ("events", self.event_count, config.max_events),
            (
                "dependency_edges",
                self.logical_dependency_edge_count,
                config.max_dependency_edges,
            ),
            (
                "statements",
                self.logical_statement_count,
                config.max_statements,
            ),
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
    # Complexity of the RTL that remains visible at this level after static
    # children are replaced by summary slots.  This is the quantity a parent
    # semantic synthesis stage actually consumes.
    replacement_complexity: WorkUnitComplexity
    replacement_exceeded_limits: tuple[str, ...]
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
    """Longest state-root ancestor without scanning every register root."""

    root_set = roots if isinstance(roots, (set, frozenset)) else set(roots)
    if signal in root_set:
        return signal
    best: str | None = None
    for index, char in enumerate(signal):
        if char not in ".[":
            continue
        prefix = signal[:index]
        if prefix in root_set:
            best = prefix
    return best


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


def _source_loc_breakdown(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
) -> tuple[int, int, int]:
    """Return (raw, logical, unmapped) source-location complexity.

    Raw keeps the old fail-conservative accounting.  Logical source complexity
    reflects the source-grounded text a later semantic stage can actually
    consume.  If a scope has no source provenance at all, FIRRTL lines are used
    as the logical fallback rather than pretending the scope has zero size.
    """

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

    raw = len(source_lines) + len(firrtl_lines)
    logical = len(source_lines) if source_lines else len(firrtl_lines)
    return raw, logical, len(firrtl_lines)


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
            # WorkUnit ownership/complexity is current-cycle structural scope.
            # Full historical cone signals remain available in `cone.signals`
            # for later semantic extraction but do not inflate partition size.
            signals.update(cone.immediate_signals)
    return signals


def _aggregate_parent(graph: ModuleDependencyGraph, signal: str) -> str | None:
    """Return the nearest proper aggregate ancestor of `signal`.

    `aggregate_leaves` contains every recursively registered FIRRTL
    sub-aggregate, not only the top-level port/register bundle.  Walking the
    syntax prefixes therefore gives a deterministic quotient such as:

      req.uop.rob_idx              -> req.uop
      io.mem_acquire.bits.address  -> io.mem_acquire.bits

    without collapsing the whole `io` bundle into one node.
    """

    candidates: list[str] = []
    for index, char in enumerate(signal):
        if char not in ".[":
            continue
        prefix = signal[:index]
        if prefix in graph.aggregate_leaves:
            candidates.append(prefix)
    return max(candidates, key=len) if candidates else None


def _logical_signal_key(graph: ModuleDependencyGraph, signal: str) -> tuple:
    """Map one lowered FIRRTL leaf to a source/aggregate-level logical node."""

    state = _state_root(graph.register_roots, signal)
    if state is not None:
        return ("state", state)

    memory = _state_root(graph.memory_roots, signal)
    if memory is not None:
        return ("memory", memory)

    aggregate = _aggregate_parent(graph, signal)
    if aggregate is not None:
        return ("aggregate", aggregate)

    info = graph.signals.get(signal)
    if (
        info is not None
        and info.kind in {SignalKind.NODE, SignalKind.WIRE, SignalKind.UNKNOWN}
        and info.source is not None
        and info.source.line > 0
    ):
        # CIRCT/Chisel can lower one source expression into many `_T_*` nodes.
        # They are one logical source operation for manageability purposes.
        return (
            info.kind.value,
            info.source.file,
            info.source.line,
            info.source.column or 0,
        )

    return ("signal", signal)


def _scope_edges(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
    signals: set[str],
    *,
    full_module: bool,
):
    if full_module:
        return tuple(graph.edges)

    return tuple(
        edge
        for edge in graph.edges
        if (
            (
                bool(edge.statement_ids)
                and bool(set(edge.statement_ids) & statement_ids)
            )
            or (
                not edge.statement_ids
                and edge.src in signals
                and edge.dst in signals
            )
        )
    )


def _edge_locator_key(
    graph: ModuleDependencyGraph,
    edge,
    statement_ids: set[int],
) -> tuple[str, int, int]:
    if edge.source is not None and edge.source.line > 0:
        return (
            edge.source.file,
            edge.source.line,
            edge.source.column or 0,
        )

    for statement_id in edge.statement_ids:
        if statement_id not in statement_ids:
            continue
        if not 0 <= statement_id < len(graph.statements):
            continue
        statement = graph.statements[statement_id]
        if statement.source is not None and statement.source.line > 0:
            return (
                statement.source.file,
                statement.source.line,
                statement.source.column or 0,
            )
        return ("<firrtl>", statement.firrtl_line, 0)

    return ("<synthetic>", 0, 0)


def _logical_dependency_edge_count(
    graph: ModuleDependencyGraph,
    edges,
    statement_ids: set[int],
) -> int:
    """Count source-level dependency facts, not lowered leaf-edge multiplicity.

    The complete raw edge set is preserved in the dependency graph.  This
    quotient is used *only* for WorkUnit manageability decisions.
    """

    logical = {
        (
            _edge_locator_key(graph, edge, statement_ids),
            edge.kind.value,
            _logical_signal_key(graph, edge.src),
            _logical_signal_key(graph, edge.dst),
        )
        for edge in edges
    }
    return len(logical)


def _logical_statement_count(
    graph: ModuleDependencyGraph,
    statement_ids: set[int],
) -> int:
    """Count source-grounded operations instead of lowering multiplicity.

    Multiple FIRRTL statements emitted from the same Chisel source line and
    statement class are one logical operation for manageability purposes.
    Unmapped FIRRTL remains conservative because its own FIRRTL line is used.
    """

    logical: set[tuple] = set()
    for statement_id in statement_ids:
        if not 0 <= statement_id < len(graph.statements):
            continue
        statement = graph.statements[statement_id]
        if statement.source is not None and statement.source.line > 0:
            locator = (statement.source.file, statement.source.line)
        else:
            locator = ("<firrtl>", statement.firrtl_line)
        logical.add((locator, statement.kind))
    return len(logical)


def _complexity(
    graph: ModuleDependencyGraph,
    plan: PartitionPlan,
    interaction: EventStateInteractionGraph,
    statement_ids: set[int],
    event_ids: set[str],
    state_ids: set[str],
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
    registers = set(graph.register_roots) if full_module else set(state_ids)

    memories = {
        root
        for root in graph.memory_roots
        if any(_is_prefix(root, signal) for signal in signals)
    }
    if full_module:
        memories = set(graph.memory_roots)

    # Raw counts are retained for diagnostics.  The logical quotient below is
    # the decision metric: one Chisel/FIRRTL source dependency should not count
    # hundreds of times merely because an aggregate was leaf-expanded.
    scoped_edges = _scope_edges(
        graph,
        statement_ids,
        signals,
        full_module=full_module,
    )
    edge_count = len(scoped_edges)
    logical_signals = {
        _logical_signal_key(graph, signal) for signal in signals
    }
    logical_edge_count = _logical_dependency_edge_count(
        graph,
        scoped_edges,
        statement_ids,
    )

    source_loc, logical_source_loc, unmapped_firrtl_loc = (
        _source_loc_breakdown(graph, statement_ids)
    )

    # SCCs are complexity/coupling evidence, not atomic ownership. A child may
    # legitimately own only part of a large SCC.
    touched_sccs = {
        region.id
        for region in plan.regions
        if set(region.registers) & registers
    }

    return WorkUnitComplexity(
        source_loc=source_loc,
        logical_source_loc=logical_source_loc,
        unmapped_firrtl_loc=unmapped_firrtl_loc,
        signal_count=len(signals),
        logical_signal_count=len(logical_signals),
        register_count=len(registers),
        memory_count=len(memories),
        event_count=len(event_ids),
        dependency_edge_count=edge_count,
        logical_dependency_edge_count=logical_edge_count,
        statement_count=len(statement_ids),
        logical_statement_count=_logical_statement_count(
            graph, statement_ids
        ),
        state_scc_count=len(touched_sccs),
        event_state_coupling=_event_coupling_average(
            interaction,
            event_ids,
        ),
    )


def _statement_state_registers(
    graph: ModuleDependencyGraph,
) -> dict[int, set[str]]:
    """Map statements to concrete register roots they read or drive.

    Register-level ownership is necessary because a large feedback SCC is not
    automatically an indivisible hierarchical WorkUnit.
    """

    out: dict[int, set[str]] = defaultdict(set)
    register_roots = graph.register_roots
    for statement in graph.statements:
        for signal in _statement_refs(statement):
            root = _state_root(register_roots, signal)
            if root is not None:
                out[statement.id].add(root)
    return out

def _statement_state_accesses(
    graph: ModuleDependencyGraph,
) -> tuple[dict[int, set[str]], dict[int, set[str]]]:
    """Return per-statement register reads and drives separately.

    A parent/hub register may be *read* by child-local logic and therefore act
    as an explicit frontier input. Writing parent state, or directly reading
    another child's owned state, is cross-boundary behavior and stays at the
    parent. Keeping reads and drives separate is what allows bounded ownership
    expansion to move useful RTL below a shared coordinator without moving the
    coordinator itself.
    """

    reads: dict[int, set[str]] = defaultdict(set)
    drives: dict[int, set[str]] = defaultdict(set)
    register_roots = graph.register_roots

    for statement in graph.statements:
        for signal in set(statement.reads) | set(statement.control_reads):
            root = _state_root(register_roots, signal)
            if root is not None:
                reads[statement.id].add(root)
        for signal in statement.drives:
            root = _state_root(register_roots, signal)
            if root is not None:
                drives[statement.id].add(root)

    return reads, drives


def _bounded_ownership_statements(
    graph: ModuleDependencyGraph,
    seeds: Iterable[str],
    owned_states: set[str],
    scope_statements: set[int],
) -> set[int]:
    """Recover a child's semantic RTL while stopping at foreign state.

    Unlike the immediate partition cone, this traversal is allowed to cross a
    child-owned register and follow its next-state/history logic. Any register
    not owned by the child is a hard frontier: its *value* may be consumed as a
    parent/peer summary input, but its update cone is never pulled into the
    child. This is the ownership analogue of replacing already-abstracted
    children with summaries during bottom-up composition.
    """

    allowed = {
        DependencyKind.DATA,
        DependencyKind.CONTROL,
        DependencyKind.STATE,
        DependencyKind.ADDRESS,
        DependencyKind.MEMORY,
        DependencyKind.ALIAS,
    }
    predecessors: dict[str, list] = defaultdict(list)
    for edge in graph.edges:
        if edge.kind in allowed:
            predecessors[edge.dst].append(edge)

    register_roots = graph.register_roots
    queue = list(dict.fromkeys(seeds))
    visited: set[str] = set(queue)
    selected: set[int] = set()

    while queue:
        signal = queue.pop()
        root = _state_root(register_roots, signal)
        if root is not None and root not in owned_states:
            # Parent/hub or peer-child state is a summary/frontier value.
            continue

        if signal in graph.input_ports:
            continue

        for edge in predecessors.get(signal, ()):
            selected.update(set(edge.statement_ids) & scope_statements)

            source_root = _state_root(register_roots, edge.src)
            if source_root is not None and source_root not in owned_states:
                # Consume the current value, but never traverse its update cone.
                visited.add(edge.src)
                continue

            if edge.src not in visited:
                visited.add(edge.src)
                queue.append(edge.src)

    return selected & scope_statements


def _cone_by_event(plan: PartitionPlan) -> dict[str, object]:
    return {cone.event_id: cone for cone in plan.event_cones}


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


def _cross_child_glue_statements(
    local_statement_ids: set[int],
    child_state_scopes: list[set[str]],
    statement_reads: dict[int, set[str]],
    statement_drives: dict[int, set[str]],
) -> set[int]:
    """Identify parent-local statements that directly couple child state.

    Bounded ownership intentionally leaves cross-child logic at the parent.
    Such statements must also be *marked* as shared glue even when no child
    event cone requests them (for example a parent observation ``and(ra, rb)``).
    Otherwise conservation is correct but the hierarchy loses the distinction
    between ordinary unassigned parent logic and explicit child interaction.
    """

    shared: set[int] = set()
    for statement_id in local_statement_ids:
        touched = (
            statement_reads.get(statement_id, set())
            | statement_drives.get(statement_id, set())
        )
        owners = sum(
            1 for states in child_state_scopes
            if touched & states
        )
        if owners >= 2:
            shared.add(statement_id)
    return shared


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
    interaction: EventStateInteractionGraph,
) -> tuple[list[set[str]], set[str]]:
    """Assign concrete register roots to one child or retain them at parent.

    Register SCC membership is deliberately ignored here. High-degree hub
    registers are always parent coordination state. A non-hub register is
    delegated only when its immediate event incidence points to exactly one
    active child and no parent-local event.
    """

    states_by_group = [set() for _ in groups]
    shared: set[str] = set()
    delegated_events = set().union(*groups) if groups else set()
    parent_events = scope_events - delegated_events
    hubs = set(interaction.hub_registers)

    for register in scope_states:
        register_events = set(interaction.events_for_register(register)) & scope_events
        owners = [
            index
            for index, events in enumerate(groups)
            if register_events & events
        ]
        parent_touches = bool(register_events & parent_events)

        if register in hubs:
            shared.add(register)
        elif len(owners) == 1 and not parent_touches:
            states_by_group[owners[0]].add(register)
        else:
            # Multi-child, parent-touched, and event-unattributed registers are
            # explicit parent glue. This also conservatively handles local
            # bookkeeping state with no boundary-event incidence.
            shared.add(register)

    return states_by_group, shared


def _desired_statements_by_group(
    graph: ModuleDependencyGraph,
    groups: list[set[str]],
    states_by_group: list[set[str]],
    scope_statements: set[int],
    plan: PartitionPlan,
) -> list[set[int]]:
    """Expand each discovered child from partition seeds into semantic RTL.

    Immediate cones decide *which events belong together*. Once a group exists,
    ownership is expanded with a bounded historical cone: child-owned state may
    be traversed through time, while every other register becomes an explicit
    frontier value. This recovers the child's real local control/datapath instead
    of leaving nearly all RTL at the parent.
    """

    cones = _cone_by_event(plan)
    desired: list[set[int]] = []

    for events, states in zip(groups, states_by_group):
        seeds: set[str] = set(states)
        for event_id in events:
            cone = cones.get(event_id)
            if cone is not None:
                seeds.update(cone.semantic_seed_signals)

        desired.append(
            _bounded_ownership_statements(
                graph,
                seeds,
                states,
                scope_statements,
            )
        )

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
    graph: ModuleDependencyGraph,
    groups: list[set[str]],
    scope_statements: set[int],
    scope_events: set[str],
    scope_states: set[str],
    plan: PartitionPlan,
    interaction: EventStateInteractionGraph,
    statement_reads: dict[int, set[str]],
    statement_drives: dict[int, set[str]],
    min_child_statements: int,
) -> tuple[list[set[str]], list[set[str]], list[set[int]], set[int]] | None:
    """Turn event groups into exclusive, bounded semantic ownership scopes.

    Partition discovery and ownership are intentionally separate:

      * immediate Event-State coupling discovers the child identities;
      * bounded ownership expansion grows each child through its own state;
      * parent/hub state is readable as a frontier input but never writable;
      * direct peer-child state use is cross-child glue and remains at parent;
      * statements needed by multiple children remain shared parent logic.

    Coverage is still checked later as an exact conservation equation.
    """

    active = [set(group) for group in groups if group]
    cones = _cone_by_event(plan)

    while len(active) >= 2:
        states_by_group, _ = _owned_state_by_group(
            active,
            scope_states,
            scope_events,
            interaction,
        )
        desired = _desired_statements_by_group(
            graph,
            active,
            states_by_group,
            scope_statements,
            plan,
        )

        delegated_events = set().union(*active)
        parent_events = scope_events - delegated_events
        delegated_states = (
            set().union(*states_by_group) if states_by_group else set()
        )
        parent_states = scope_states - delegated_states

        protected: set[int] = set()

        # Parent-local event logic stays at the parent, but only its bounded
        # current semantic cone is protected. We intentionally do not use a
        # full historical cone here because that would re-introduce the v7
        # "central FSM owns everything" pathology.
        for event_id in parent_events:
            cone = cones.get(event_id)
            if cone is None:
                continue
            protected.update(
                _bounded_ownership_statements(
                    graph,
                    cone.semantic_seed_signals,
                    set(),
                    scope_statements,
                )
            )

        # Ownership boundary rules are asymmetric:
        #   - reading parent/hub state is allowed (frontier input);
        #   - writing any state outside the child is not;
        #   - reading another child's state is explicit cross-child glue.
        for index, statements in enumerate(desired):
            own_states = states_by_group[index]
            peer_states = delegated_states - own_states
            for statement_id in tuple(statements):
                drives = statement_drives.get(statement_id, set())
                reads = statement_reads.get(statement_id, set())

                if drives - own_states:
                    protected.add(statement_id)
                    continue
                if reads & peer_states:
                    protected.add(statement_id)

        # Statements that actively update parent coordination state must remain
        # parent-local even if an event cone happens to visit them.
        for statement_id, drives in statement_drives.items():
            if drives & parent_states:
                protected.add(statement_id)

        for statements in desired:
            statements -= protected

        exclusive, shared = _exclusive_statement_scopes(desired)
        shared |= protected & scope_statements

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
            return active, states_by_group, exclusive, shared & scope_statements
        active = [active[index] for index in useful]

    return None


def _state_groups_from_plan(
    plan: PartitionPlan,
    scope_states: set[str],
) -> list[set[str]]:
    groups = [
        set(region.registers) & scope_states
        for region in plan.regions
        if set(region.registers) & scope_states
    ]
    covered = set().union(*groups) if groups else set()
    groups.extend({state} for state in sorted(scope_states - covered))
    return [group for group in groups if group]


def _partition_scopes_for_state_groups(
    graph: ModuleDependencyGraph,
    plan: PartitionPlan,
    scope_statements: set[int],
    scope_states: set[str],
    statement_reads: dict[int, set[str]],
    statement_drives: dict[int, set[str]],
    min_child_statements: int,
    *,
    foreign_child_states: set[str] | None = None,
) -> tuple[list[set[str]], list[set[int]], set[int]] | None:
    """Fallback partition when boundary events do not expose internal structure.

    Register SCCs are used as the first structural grouping.  They are not
    atomic: if SCC grouping yields fewer than two useful children, individual
    registers are tried as a last structural refinement.  This is the
    state/dependency half of the hierarchical planner and prevents event-poor
    LSU/LSQ internals from remaining one giant parent merely because their
    boundary observations are combinational.
    """

    foreign_child_states = set(foreign_child_states or ())

    def evaluate(
        groups: list[set[str]],
    ) -> tuple[list[set[str]], list[set[int]], set[int]] | None:
        active = [set(group) for group in groups if group]

        # Prune structurally empty state groups and recompute after every prune.
        # A rejected SCC remains parent state; it must not permanently make
        # unrelated child logic look like cross-child shared glue.
        while len(active) >= 2:
            desired = [
                _bounded_ownership_statements(
                    graph,
                    states,
                    states,
                    scope_statements,
                )
                for states in active
            ]
            delegated_states = set().union(*active)
            parent_states = scope_states - delegated_states
            protected: set[int] = set()

            for index, statements in enumerate(desired):
                own_states = active[index]
                peer_states = (
                    delegated_states - own_states
                ) | foreign_child_states
                for statement_id in tuple(statements):
                    drives = statement_drives.get(statement_id, set())
                    reads = statement_reads.get(statement_id, set())
                    if drives - own_states:
                        protected.add(statement_id)
                        continue
                    if reads & peer_states:
                        protected.add(statement_id)

            for statement_id, drives in statement_drives.items():
                if drives & parent_states:
                    protected.add(statement_id)

            for statements in desired:
                statements -= protected

            exclusive, shared = _exclusive_statement_scopes(desired)
            shared |= protected & scope_statements
            useful = [
                index
                for index, statements in enumerate(exclusive)
                if len(statements) >= min_child_statements
            ]
            if len(useful) < 2:
                return None
            if len(useful) == len(active):
                return active, exclusive, shared & scope_statements
            active = [active[index] for index in useful]

        return None

    scc_groups = _state_groups_from_plan(plan, scope_states)
    result = evaluate(scc_groups)
    if result is not None:
        return result

    # A single oversized feedback SCC may still contain separable ownership
    # below shared coordination state; register granularity is conservative
    # because every cross-register statement is promoted to parent glue.
    if len(scope_states) >= 2:
        return evaluate([{state} for state in sorted(scope_states)])
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
                logical_source_loc=0,
                unmapped_firrtl_loc=0,
                signal_count=0,
                logical_signal_count=0,
                register_count=0,
                memory_count=0,
                event_count=0,
                dependency_edge_count=0,
                logical_dependency_edge_count=0,
                statement_count=0,
                logical_statement_count=0,
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
                replacement_complexity=empty_complexity,
                replacement_exceeded_limits=(),
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
        interaction = build_event_state_interaction_graph(
            plan,
            hub_event_ratio=config.hub_event_ratio,
            hub_min_touch_events=config.hub_min_touch_events,
            hub_min_module_events=config.hub_min_module_events,
        )
        statement_states = _statement_state_registers(graph)
        statement_reads, statement_drives = _statement_state_accesses(graph)

        all_statement_ids = set(range(len(graph.statements)))
        all_event_ids = set(interaction.event_ids)
        # Register SCCs are advisory only; recursive ownership is register-level.
        all_state_ids = set(graph.register_roots)

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
                            graph,
                            groups,
                            scope_statements,
                            scope_events,
                            scope_states,
                            plan,
                            interaction,
                            statement_reads,
                            statement_drives,
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
                else:
                    decision = WorkUnitDecision.UNSPLITTABLE

                # Event grouping is only the preferred first cut.  If it did
                # not expose at least two useful children, fall back to the
                # register-SCC/state-dependency hierarchy even when the module
                # has many boundary events.
                if not child_specs and len(scope_states) >= 2:
                    state_scopes = _partition_scopes_for_state_groups(
                        graph,
                        plan,
                        scope_statements,
                        scope_states,
                        statement_reads,
                        statement_drives,
                        config.min_child_statements,
                    )
                    if state_scopes is not None:
                        state_groups, exclusive, shared = state_scopes
                        for ordinal, (states, statements) in enumerate(
                            zip(state_groups, exclusive)
                        ):
                            child_specs.append(
                                (
                                    f"{unit_id}::state-{region_depth}-{ordinal}",
                                    statements,
                                    set(),
                                    states,
                                    set(),
                                    1.0,
                                )
                            )
                        shared_statement_ids = shared & scope_statements
                        threshold_used = 1.0
                        decision = WorkUnitDecision.PARTITIONED

            child_statement_scopes = [spec[1] for spec in child_specs]
            child_event_scopes = [spec[2] for spec in child_specs]
            child_state_scopes = [spec[3] for spec in child_specs]

            delegated_statements = set().union(*child_statement_scopes) if child_statement_scopes else set()
            delegated_events = set().union(*child_event_scopes) if child_event_scopes else set()
            delegated_states = set().union(*child_state_scopes) if child_state_scopes else set()

            local_statements = scope_statements - delegated_statements
            local_events = scope_events - delegated_events
            local_states = scope_states - delegated_states

            replacement_metrics = _complexity(
                graph,
                plan,
                interaction,
                local_statements,
                local_events,
                local_states,
                full_module=False,
            )
            replacement_exceeded = replacement_metrics.exceeded(config)

            # A first event-based cut may peel only the externally visible
            # cones while leaving a still-oversized LSU/LSQ residual.  Keep
            # refining that parent residual through the state/dependency
            # hierarchy until it is manageable or no further conservative cut
            # exists. Already-delegated child state is protected as peer
            # summary state; previously identified shared glue is never
            # re-delegated.
            while (
                replacement_exceeded
                and len(local_states) >= 2
                and region_depth < config.max_depth
            ):
                # Shared is a property of the *current* partition boundary,
                # not a permanent ownership ban. Parent glue may itself become
                # a later state-child if a deeper cut proves exclusive
                # ownership. Any statement that is actually delegated is
                # removed from the shared ledger after recomputation below.
                residual_state_scopes = _partition_scopes_for_state_groups(
                    graph,
                    plan,
                    local_statements,
                    local_states,
                    statement_reads,
                    statement_drives,
                    config.min_child_statements,
                    foreign_child_states=delegated_states,
                )
                if residual_state_scopes is None:
                    break

                (
                    residual_groups,
                    residual_exclusive,
                    residual_shared,
                ) = residual_state_scopes
                added_statement_count = sum(
                    len(statements) for statements in residual_exclusive
                )
                if added_statement_count == 0:
                    break

                start = len(child_specs)
                for offset, (states, statements) in enumerate(
                    zip(residual_groups, residual_exclusive)
                ):
                    child_specs.append(
                        (
                            f"{unit_id}::state-{region_depth}-{start + offset}",
                            statements,
                            set(),
                            states,
                            set(),
                            1.0,
                        )
                    )
                shared_statement_ids |= residual_shared & local_statements
                decision = WorkUnitDecision.PARTITIONED
                if threshold_used is None:
                    threshold_used = 1.0

                # Recompute the conservation split and replacement complexity
                # after every promoted residual state batch.
                child_statement_scopes = [spec[1] for spec in child_specs]
                child_event_scopes = [spec[2] for spec in child_specs]
                child_state_scopes = [spec[3] for spec in child_specs]
                delegated_statements = (
                    set().union(*child_statement_scopes)
                    if child_statement_scopes
                    else set()
                )
                delegated_events = (
                    set().union(*child_event_scopes)
                    if child_event_scopes
                    else set()
                )
                delegated_states = (
                    set().union(*child_state_scopes)
                    if child_state_scopes
                    else set()
                )
                local_statements = scope_statements - delegated_statements
                local_events = scope_events - delegated_events
                local_states = scope_states - delegated_states
                shared_statement_ids &= local_statements
                replacement_metrics = _complexity(
                    graph,
                    plan,
                    interaction,
                    local_statements,
                    local_events,
                    local_states,
                    full_module=False,
                )
                replacement_exceeded = replacement_metrics.exceeded(config)

            # v9.1: a statement can be cross-child glue even when it is not
            # requested by multiple event ownership cones.  Mark direct
            # multi-child state interactions explicitly so `shared logic
            # promotion` remains visible in the WorkUnit contract.
            shared_statement_ids |= _cross_child_glue_statements(
                local_statements,
                child_state_scopes,
                statement_reads,
                statement_drives,
            )

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

            scope_registers = tuple(sorted(scope_states))
            local_registers = tuple(sorted(local_states))
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
                replacement_complexity=replacement_metrics,
                replacement_exceeded_limits=replacement_exceeded,
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
        "logical_source_loc": complexity.logical_source_loc,
        "unmapped_firrtl_loc": complexity.unmapped_firrtl_loc,
        "signals": complexity.signal_count,
        "logical_signals": complexity.logical_signal_count,
        "registers": complexity.register_count,
        "memories": complexity.memory_count,
        "events": complexity.event_count,
        "dependency_edges": complexity.dependency_edge_count,
        "logical_dependency_edges": complexity.logical_dependency_edge_count,
        "statements": complexity.statement_count,
        "logical_statements": complexity.logical_statement_count,
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
            "replacement_complexity": _complexity_dict(
                unit.replacement_complexity
            ),
            "replacement_exceeded_limits": list(
                unit.replacement_exceeded_limits
            ),
            "child_summaries": len(unit.children),
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
            "replacement_complexity": _complexity_dict(
                unit.replacement_complexity
            ),
            "replacement_exceeded_limits": list(
                unit.replacement_exceeded_limits
            ),
            "child_summaries": len(unit.children),
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
        "hub_registers": list(graph.hub_registers),
        "register_incidence": [
            {
                "register": incidence.register,
                "event_ids": list(incidence.event_ids),
                "event_fraction": round(incidence.event_fraction, 6),
                "hub": incidence.hub,
            }
            for incidence in graph.register_incidence
        ],
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
                "shared_hub_registers": list(coupling.shared_hub_registers),
                "shared_statement_count": len(coupling.shared_statement_ids),
                "state_jaccard": round(coupling.state_jaccard, 6),
                "statement_jaccard": round(coupling.statement_jaccard, 6),
                "score": round(coupling.score, 6),
            }
            for coupling in graph.couplings
            if coupling.score > 0.0 or coupling.shared_hub_registers
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
