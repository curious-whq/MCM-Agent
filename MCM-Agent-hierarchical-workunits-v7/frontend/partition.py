from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations

from .dependency import DependencyKind, ModuleDependencyGraph
from .registry import EventRegistry
from .slice import EventSliceMode, SliceOptions, slice_event


@dataclass(frozen=True)
class EventCone:
    event_id: str
    registers: tuple[str, ...]
    signals: tuple[str, ...]
    complete: bool
    statement_ids: tuple[int, ...] = ()


@dataclass(frozen=True)
class StateRegion:
    id: str
    registers: tuple[str, ...]
    event_ids: tuple[str, ...]


@dataclass(frozen=True)
class PartitionPlan:
    module: str
    register_dependencies: tuple[tuple[str, str], ...]
    regions: tuple[StateRegion, ...]
    event_cones: tuple[EventCone, ...]


@dataclass(frozen=True)
class EventStateTouch:
    event_id: str
    state_region_id: str
    registers: tuple[str, ...]


@dataclass(frozen=True)
class EventCoupling:
    left_event: str
    right_event: str
    shared_state_regions: tuple[str, ...]
    shared_registers: tuple[str, ...]
    shared_statement_ids: tuple[int, ...]
    state_jaccard: float
    statement_jaccard: float
    score: float


@dataclass(frozen=True)
class EventStateInteractionGraph:
    """Bipartite event/state view used only for structural partitioning.

    `touches` encodes Event -> register-SCC relations. `couplings` is a
    deterministic projection onto event pairs, weighted by shared state and
    shared static cone statements. No semantic event names are introduced.
    """

    module: str
    event_ids: tuple[str, ...]
    state_region_ids: tuple[str, ...]
    touches: tuple[EventStateTouch, ...]
    couplings: tuple[EventCoupling, ...]

    def state_regions_for_event(self, event_id: str) -> tuple[str, ...]:
        return tuple(
            touch.state_region_id
            for touch in self.touches
            if touch.event_id == event_id
        )

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
    matches = [
        root
        for root in graph.register_roots
        if (
            signal == root
            or signal.startswith(root + ".")
            or signal.startswith(root + "[")
        )
    ]
    if not matches:
        return None
    return max(matches, key=len)


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

    for dst_root in sorted(graph.register_roots):
        destinations = [
            name
            for name in graph.signals
            if _register_root(graph, name) == dst_root
        ]
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


def discover_partition_plan(
    graph: ModuleDependencyGraph,
    registry: EventRegistry,
) -> PartitionPlan:
    """Propose static leaf regions without assigning semantic names.

    The plan is intentionally structural:
      1. compute register-to-register dependency SCCs;
      2. compute each physical boundary event's local cone;
      3. attach events to SCCs they actually touch.

    This remains a low-level primitive. Higher-level work-unit construction
    consumes the resulting event/state interaction graph rather than treating
    one event cone as the final abstraction unit.
    """

    reg_edges = register_dependency_edges(graph)
    components = _tarjan_scc(set(graph.register_roots), reg_edges)

    cones: list[EventCone] = []
    event_registers: dict[str, set[str]] = {}

    for event in registry.sorted_events():
        result = slice_event(
            graph,
            event,
            mode=EventSliceMode.FULL,
            options=SliceOptions(stop_at_module_inputs=True),
        )
        registers = {
            root
            for signal in result.signals
            if (root := _register_root(graph, signal)) is not None
        }
        event_registers[event.event_id] = registers
        cones.append(
            EventCone(
                event_id=event.event_id,
                registers=tuple(sorted(registers)),
                signals=tuple(sorted(result.signals)),
                complete=result.complete,
                statement_ids=tuple(sorted(result.statement_ids)),
            )
        )

    regions: list[StateRegion] = []
    for index, component in enumerate(components):
        component_set = set(component)
        events = [
            event_id
            for event_id, registers in event_registers.items()
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
) -> EventStateInteractionGraph:
    """Build the structural Event-State Interaction Graph.

    The graph is bipartite at its core. Event-pair coupling is a derived view
    used by deterministic recursive partitioning:
      * state overlap gets the dominant weight;
      * statement-cone overlap captures shared combinational/control logic.

    The score is intentionally heuristic and does not carry semantic meaning.
    """

    region_by_register: dict[str, str] = {}
    for region in plan.regions:
        for register in region.registers:
            region_by_register[register] = region.id

    touches: list[EventStateTouch] = []
    states_by_event: dict[str, set[str]] = defaultdict(set)
    registers_by_event: dict[str, set[str]] = defaultdict(set)
    statements_by_event: dict[str, set[int]] = defaultdict(set)

    for cone in plan.event_cones:
        grouped: dict[str, set[str]] = defaultdict(set)
        for register in cone.registers:
            region_id = region_by_register.get(register)
            if region_id is None:
                continue
            grouped[region_id].add(register)
            states_by_event[cone.event_id].add(region_id)
            registers_by_event[cone.event_id].add(register)
        statements_by_event[cone.event_id].update(cone.statement_ids)
        for region_id in sorted(grouped):
            touches.append(
                EventStateTouch(
                    event_id=cone.event_id,
                    state_region_id=region_id,
                    registers=tuple(sorted(grouped[region_id])),
                )
            )

    event_ids = tuple(sorted(cone.event_id for cone in plan.event_cones))
    couplings: list[EventCoupling] = []
    for left_event, right_event in combinations(event_ids, 2):
        left_states = states_by_event[left_event]
        right_states = states_by_event[right_event]
        left_statements = statements_by_event[left_event]
        right_statements = statements_by_event[right_event]

        state_jaccard = _jaccard(left_states, right_states)
        statement_jaccard = _jaccard(left_statements, right_statements)
        # Shared state is the primary structural signal; static cone overlap is
        # deliberately secondary so pure combinational sharing can still be
        # represented without overpowering ownership.
        score = 0.7 * state_jaccard + 0.3 * statement_jaccard

        couplings.append(
            EventCoupling(
                left_event=left_event,
                right_event=right_event,
                shared_state_regions=tuple(
                    sorted(left_states & right_states)
                ),
                shared_registers=tuple(
                    sorted(
                        registers_by_event[left_event]
                        & registers_by_event[right_event]
                    )
                ),
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
        couplings=tuple(couplings),
    )
