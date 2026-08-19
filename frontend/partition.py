from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations

from .dependency import DependencyKind, ModuleDependencyGraph
from .registry import EventRegistry, PhysicalEvent
from .slice import (
    EventSliceMode,
    SliceOptions,
    event_seed_signals,
    slice_event,
)


@dataclass(frozen=True)
class EventCone:
    event_id: str
    # Historical/full semantic cone retained for compatibility and later µMCM
    # extraction. These fields may cross sequential register boundaries.
    registers: tuple[str, ...]
    signals: tuple[str, ...]
    complete: bool
    statement_ids: tuple[int, ...] = ()
    # Exact FULL event seeds retained so a later ownership pass can recover a
    # bounded semantic cone without re-discovering or semantically renaming the
    # physical boundary event.
    semantic_seed_signals: tuple[str, ...] = ()
    # Partition ownership is based on the *current-cycle* cone below. Traversal
    # stops at the first register boundary, so an event is not made to own the
    # entire historical FSM merely because that FSM can eventually affect it.
    immediate_registers: tuple[str, ...] = ()
    immediate_signals: tuple[str, ...] = ()
    immediate_statement_ids: tuple[int, ...] = ()
    immediate_frontier: tuple[str, ...] = ()


@dataclass(frozen=True)
class StateRegion:
    id: str
    registers: tuple[str, ...]
    # Events are attached by immediate/current-cycle dependence, not by the
    # historical transitive closure.
    event_ids: tuple[str, ...]


@dataclass(frozen=True)
class PartitionPlan:
    module: str
    register_dependencies: tuple[tuple[str, str], ...]
    # `regions` remains the register-SCC view. SCC membership is advisory for
    # recursive partitioning; work-unit ownership may split inside a large SCC.
    regions: tuple[StateRegion, ...]
    event_cones: tuple[EventCone, ...]


@dataclass(frozen=True)
class EventStateTouch:
    event_id: str
    state_region_id: str
    registers: tuple[str, ...]


@dataclass(frozen=True)
class RegisterIncidence:
    register: str
    event_ids: tuple[str, ...]
    event_fraction: float
    hub: bool


@dataclass(frozen=True)
class EventCoupling:
    left_event: str
    right_event: str
    shared_state_regions: tuple[str, ...]
    # Non-hub immediate registers are the ownership-bearing overlap.
    shared_registers: tuple[str, ...]
    shared_hub_registers: tuple[str, ...]
    shared_statement_ids: tuple[int, ...]
    state_jaccard: float
    statement_jaccard: float
    score: float


@dataclass(frozen=True)
class EventStateInteractionGraph:
    """Immediate event/state view used only for structural partitioning.

    Full/historical cones remain in ``PartitionPlan.event_cones`` for semantic
    analysis, but this graph deliberately uses only the current-cycle cone that
    stops at the first register boundary.
    """

    module: str
    event_ids: tuple[str, ...]
    state_region_ids: tuple[str, ...]
    touches: tuple[EventStateTouch, ...]
    register_incidence: tuple[RegisterIncidence, ...]
    hub_registers: tuple[str, ...]
    couplings: tuple[EventCoupling, ...]

    def state_regions_for_event(self, event_id: str) -> tuple[str, ...]:
        return tuple(
            touch.state_region_id
            for touch in self.touches
            if touch.event_id == event_id
        )

    def registers_for_event(
        self,
        event_id: str,
        *,
        include_hubs: bool = True,
    ) -> tuple[str, ...]:
        registers = {
            register
            for touch in self.touches
            if touch.event_id == event_id
            for register in touch.registers
        }
        if not include_hubs:
            registers -= set(self.hub_registers)
        return tuple(sorted(registers))

    def events_for_register(self, register: str) -> tuple[str, ...]:
        for incidence in self.register_incidence:
            if incidence.register == register:
                return incidence.event_ids
        return ()

    def events_for_state_region(self, state_region_id: str) -> tuple[str, ...]:
        return tuple(
            touch.event_id
            for touch in self.touches
            if touch.state_region_id == state_region_id
        )

    def coupling(self, left_event: str, right_event: str) -> EventCoupling | None:
        left, right = sorted((left_event, right_event))
        for coupling in self.couplings:
            if (
                coupling.left_event == left
                and coupling.right_event == right
            ):
                return coupling
        return None

    @property
    def average_coupling(self) -> float:
        if not self.couplings:
            return 0.0
        return sum(coupling.score for coupling in self.couplings) / len(
            self.couplings
        )


def _register_root(graph: ModuleDependencyGraph, signal: str) -> str | None:
    """Return the longest register root prefix in O(len(signal)).

    The previous implementation scanned every register root for every queried
    signal.  That is harmless on ProbeUnit/MSHR but becomes the dominant cost
    on LSU (100+ registers and tens of thousands of lowered signals).  FIRRTL
    aggregate descendants are separated only by `.` / `[`, so ancestor-prefix
    lookup is exact and deterministic.
    """

    roots = graph.register_roots
    if signal in roots:
        return signal

    best: str | None = None
    for index, char in enumerate(signal):
        if char not in ".[":
            continue
        prefix = signal[:index]
        if prefix in roots:
            best = prefix
    return best


def register_dependency_edges(
    graph: ModuleDependencyGraph,
) -> set[tuple[str, str]]:
    """Collapse combinational cones into direct register-to-register edges."""

    incoming: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.kind in {DependencyKind.CLOCK, DependencyKind.RESET}:
            continue
        incoming[edge.dst].append(edge.src)

    result: set[tuple[str, str]] = set()

    # Build register ownership once.  The previous per-destination full signal
    # scan was O(R*S) and alone took ~27 s on the real BOOM LSU.
    destinations_by_root: dict[str, list[str]] = defaultdict(list)
    for name in graph.signals:
        root = _register_root(graph, name)
        if root is not None:
            destinations_by_root[root].append(name)

    for dst_root in sorted(graph.register_roots):
        destinations = list(destinations_by_root.get(dst_root, ()))
        if dst_root not in destinations:
            destinations.append(dst_root)

        queue = deque(destinations)
        visited = set(destinations)

        while queue:
            node = queue.popleft()
            for source in incoming.get(node, ()):
                src_root = _register_root(graph, source)
                if src_root is not None:
                    result.add((src_root, dst_root))
                    # Stop at the register boundary: this is the direct state
                    # dependence we wanted to expose.
                    continue
                if source not in visited:
                    visited.add(source)
                    queue.append(source)

    return result


def _tarjan_scc(
    nodes: set[str],
    edges: set[tuple[str, str]],
) -> list[tuple[str, ...]]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        adjacency[src].append(dst)

    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    components: list[tuple[str, ...]] = []

    def strongconnect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for successor in adjacency.get(node, ()):
            if successor not in indices:
                strongconnect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in on_stack:
                lowlink[node] = min(lowlink[node], indices[successor])

        if lowlink[node] == indices[node]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(tuple(sorted(component)))

    for node in sorted(nodes):
        if node not in indices:
            strongconnect(node)

    return sorted(components)


@dataclass(frozen=True)
class ImmediateEventFrontier:
    registers: tuple[str, ...]
    signals: tuple[str, ...]
    statement_ids: tuple[int, ...]
    frontier: tuple[str, ...]


def immediate_event_state_frontier(
    graph: ModuleDependencyGraph,
    event: PhysicalEvent,
) -> ImmediateEventFrontier:
    """Recover current-cycle event dependence and stop at first state boundary.

    This is intentionally different from ``slice_event(FULL)``. The latter is
    allowed to traverse a register's next-state cone and therefore answers a
    historical reachability question. Partitioning needs the much narrower
    question: *which current state can directly gate/shape this occurrence?*
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

    # Partition ownership is about occurrence/gating. Payload data is left to
    # the historical semantic cone and does not pull unrelated datapath state
    # into the ownership decision.
    seeds = event_seed_signals(event, EventSliceMode.OCCURRENCE)
    queue = deque(seeds)
    visited: set[str] = set(seeds)
    registers: set[str] = set()
    statement_ids: set[int] = set()
    frontier: set[str] = set()

    while queue:
        signal = queue.popleft()
        signal_root = _register_root(graph, signal)
        if signal_root is not None:
            registers.add(signal_root)
            frontier.add(signal_root)
            continue

        if signal in graph.input_ports:
            frontier.add(signal)
            continue

        incoming = predecessors.get(signal, ())
        if not incoming:
            frontier.add(signal)
            continue

        for edge in incoming:
            statement_ids.update(edge.statement_ids)
            source_root = _register_root(graph, edge.src)
            if source_root is not None:
                registers.add(source_root)
                frontier.add(source_root)
                visited.add(edge.src)
                # The defining difference from a historical slice: never walk
                # through the register into its next-state/history cone.
                continue
            if edge.src not in visited:
                visited.add(edge.src)
                queue.append(edge.src)

    return ImmediateEventFrontier(
        registers=tuple(sorted(registers)),
        signals=tuple(sorted(visited)),
        statement_ids=tuple(sorted(statement_ids)),
        frontier=tuple(sorted(frontier)),
    )


def discover_partition_plan(
    graph: ModuleDependencyGraph,
    registry: EventRegistry,
) -> PartitionPlan:
    """Propose deterministic structural regions without semantic names.

    Two cones are intentionally kept per event:
      1. historical/full cone for later semantic extraction;
      2. immediate cone, stopped at registers, for ownership/partitioning.

    Register SCCs remain useful coupling evidence but are no longer treated as
    atomic ownership units by the recursive WorkUnit builder.
    """

    reg_edges = register_dependency_edges(graph)
    components = _tarjan_scc(set(graph.register_roots), reg_edges)

    cones: list[EventCone] = []
    immediate_event_registers: dict[str, set[str]] = {}

    for event in registry.sorted_events():
        historical = slice_event(
            graph,
            event,
            mode=EventSliceMode.FULL,
            options=SliceOptions(stop_at_module_inputs=True),
        )
        historical_registers = {
            root
            for signal in historical.signals
            if (root := _register_root(graph, signal)) is not None
        }
        immediate = immediate_event_state_frontier(graph, event)
        immediate_event_registers[event.event_id] = set(immediate.registers)
        cones.append(
            EventCone(
                event_id=event.event_id,
                registers=tuple(sorted(historical_registers)),
                signals=tuple(sorted(historical.signals)),
                complete=historical.complete,
                statement_ids=tuple(sorted(historical.statement_ids)),
                semantic_seed_signals=event_seed_signals(
                    event, EventSliceMode.FULL
                ),
                immediate_registers=immediate.registers,
                immediate_signals=immediate.signals,
                immediate_statement_ids=immediate.statement_ids,
                immediate_frontier=immediate.frontier,
            )
        )

    regions: list[StateRegion] = []
    for index, component in enumerate(components):
        component_set = set(component)
        events = [
            event_id
            for event_id, registers in immediate_event_registers.items()
            if registers & component_set
        ]
        regions.append(
            StateRegion(
                id=f"state-scc-{index}",
                registers=component,
                event_ids=tuple(sorted(events)),
            )
        )

    return PartitionPlan(
        module=graph.module,
        register_dependencies=tuple(sorted(reg_edges)),
        regions=tuple(regions),
        event_cones=tuple(sorted(cones, key=lambda cone: cone.event_id)),
    )


def _jaccard(left: set[object], right: set[object]) -> float:
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def build_event_state_interaction_graph(
    plan: PartitionPlan,
    *,
    hub_event_ratio: float = 0.60,
    hub_min_touch_events: int = 3,
    hub_min_module_events: int = 4,
) -> EventStateInteractionGraph:
    """Build the immediate Event-State Interaction Graph.

    High-degree registers in sufficiently event-rich modules are marked as hub
    coordinator state. Hubs stay visible and are later promoted to the parent,
    but they do not by themselves glue every event into one child.

    Small two-event structures (e.g. ordinary enqueue/dequeue queues) never
    apply hub suppression, preserving genuinely shared queue state.
    """

    region_by_register: dict[str, str] = {}
    for region in plan.regions:
        for register in region.registers:
            region_by_register[register] = region.id

    event_ids = tuple(sorted(cone.event_id for cone in plan.event_cones))
    registers_by_event: dict[str, set[str]] = {
        cone.event_id: set(cone.immediate_registers)
        for cone in plan.event_cones
    }
    statements_by_event: dict[str, set[int]] = {
        cone.event_id: set(cone.immediate_statement_ids)
        for cone in plan.event_cones
    }

    events_by_register: dict[str, set[str]] = defaultdict(set)
    for event_id, registers in registers_by_event.items():
        for register in registers:
            events_by_register[register].add(event_id)

    incidence: list[RegisterIncidence] = []
    hubs: set[str] = set()
    total_events = len(event_ids)
    for register in sorted(region_by_register):
        touching = events_by_register.get(register, set())
        fraction = len(touching) / total_events if total_events else 0.0
        is_hub = (
            total_events >= hub_min_module_events
            and len(touching) >= hub_min_touch_events
            and fraction >= hub_event_ratio
        )
        if is_hub:
            hubs.add(register)
        incidence.append(
            RegisterIncidence(
                register=register,
                event_ids=tuple(sorted(touching)),
                event_fraction=fraction,
                hub=is_hub,
            )
        )

    touches: list[EventStateTouch] = []
    for cone in plan.event_cones:
        grouped: dict[str, set[str]] = defaultdict(set)
        for register in cone.immediate_registers:
            region_id = region_by_register.get(register)
            if region_id is not None:
                grouped[region_id].add(register)
        for region_id in sorted(grouped):
            touches.append(
                EventStateTouch(
                    event_id=cone.event_id,
                    state_region_id=region_id,
                    registers=tuple(sorted(grouped[region_id])),
                )
            )

    couplings: list[EventCoupling] = []
    for left_event, right_event in combinations(event_ids, 2):
        left_all = registers_by_event[left_event]
        right_all = registers_by_event[right_event]
        left_local = left_all - hubs
        right_local = right_all - hubs
        left_statements = statements_by_event[left_event]
        right_statements = statements_by_event[right_event]

        state_jaccard = _jaccard(left_local, right_local)
        statement_jaccard = _jaccard(left_statements, right_statements)

        if left_local and right_local:
            # Both events have ownership-bearing state. State overlap dominates.
            score = 0.80 * state_jaccard + 0.20 * statement_jaccard
        else:
            # For combinational-only events, local statement affinity is the
            # only useful structural ownership clue. Immediate statements are
            # deliberately used here, never the historical cone.
            score = 0.35 * state_jaccard + 0.65 * statement_jaccard

        shared_local = left_local & right_local
        shared_hubs = (left_all & right_all) & hubs
        shared_regions = {
            region_by_register[register]
            for register in shared_local
            if register in region_by_register
        }

        couplings.append(
            EventCoupling(
                left_event=left_event,
                right_event=right_event,
                shared_state_regions=tuple(sorted(shared_regions)),
                shared_registers=tuple(sorted(shared_local)),
                shared_hub_registers=tuple(sorted(shared_hubs)),
                shared_statement_ids=tuple(
                    sorted(left_statements & right_statements)
                ),
                state_jaccard=state_jaccard,
                statement_jaccard=statement_jaccard,
                score=score,
            )
        )

    return EventStateInteractionGraph(
        module=plan.module,
        event_ids=event_ids,
        state_region_ids=tuple(sorted(region.id for region in plan.regions)),
        touches=tuple(
            sorted(
                touches,
                key=lambda touch: (
                    touch.event_id,
                    touch.state_region_id,
                    touch.registers,
                ),
            )
        ),
        register_incidence=tuple(incidence),
        hub_registers=tuple(sorted(hubs)),
        couplings=tuple(couplings),
    )
