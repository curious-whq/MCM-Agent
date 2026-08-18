from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from .dependency import DependencyKind, ModuleDependencyGraph
from .registry import EventRegistry
from .slice import EventSliceMode, SliceOptions, slice_event


@dataclass(frozen=True)
class EventCone:
    event_id: str
    registers: tuple[str, ...]
    signals: tuple[str, ...]
    complete: bool


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

    This is a *candidate* abstraction tree input, not a semantic module split.
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
