from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Iterable

from .boundary import discover_boundary
from .dependency import (
    DependencyKind,
    ModuleDependencyGraph,
    SignalInfo,
    SignalKind,
    build_all_dependency_graphs,
)
from .model import Design, PortDirection, SourceLoc
from .registry import ChannelDirection, PhysicalEvent, discover_boundary_events
from .slice import SourceSpan, _spans_from_sources


@dataclass(frozen=True)
class FlatSignalInfo:
    id: str
    instance_path: str
    module: str
    local_name: str
    kind: SignalKind
    source: SourceLoc | None


@dataclass(frozen=True)
class FlatStatementRef:
    instance_path: str
    module: str
    statement_id: int


@dataclass(frozen=True)
class FlatDependencyEdge:
    src: str
    dst: str
    kind: DependencyKind
    statements: tuple[FlatStatementRef, ...]
    source: SourceLoc | None = None


@dataclass
class DesignDependencyGraph:
    top: str
    signals: dict[str, FlatSignalInfo] = field(default_factory=dict)
    edges: list[FlatDependencyEdge] = field(default_factory=list)
    instances: dict[str, str] = field(default_factory=dict)
    top_inputs: set[str] = field(default_factory=set)
    module_graphs: dict[str, ModuleDependencyGraph] = field(default_factory=dict)


@dataclass(frozen=True)
class DesignEventOccurrence:
    event_id: str
    instance_path: str
    module: str
    channel: str
    direction: ChannelDirection
    predicate: str
    valid_signal: str
    ready_signal: str | None
    payload_signals: tuple[str, ...]
    local_event: PhysicalEvent

    def seeds(self, include_payload: bool = False) -> tuple[str, ...]:
        signals = {self.valid_signal}
        if self.ready_signal is not None:
            signals.add(self.ready_signal)
        if include_payload:
            signals.update(self.payload_signals)
        return tuple(sorted(signals))


@dataclass(frozen=True)
class DesignSliceResult:
    seeds: tuple[str, ...]
    signals: frozenset[str]
    edges: tuple[FlatDependencyEdge, ...]
    instances: tuple[str, ...]
    frontier: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]
    incomplete_instances: tuple[str, ...] = ()
    truncated: bool = False

    @property
    def complete(self) -> bool:
        return not self.truncated and not self.incomplete_instances


def _head_segment(ref: str) -> str:
    return ref.split(".", 1)[0].split("[", 1)[0]


def _flat_id(instance_path: str, local_name: str) -> str:
    return f"{instance_path}::{local_name}"


def _map_local_ref(
    instance_path: str,
    graph: ModuleDependencyGraph,
    local_ref: str,
) -> str:
    head = _head_segment(local_ref)
    child_module = graph.instance_modules.get(head)
    if child_module is None:
        return _flat_id(instance_path, local_ref)

    if local_ref == head:
        child_local = ""
    elif local_ref.startswith(head + "."):
        child_local = local_ref[len(head) + 1 :]
    else:
        # Vectorized instances are conservatively kept local until a later
        # elaborated-instance adapter provides concrete instance paths.
        return _flat_id(instance_path, local_ref)

    child_path = f"{instance_path}.{head}"
    return _flat_id(child_path, child_local)


def flatten_design_dependency_graph(
    text: str,
    design: Design,
    module_graphs: dict[str, ModuleDependencyGraph] | None = None,
) -> DesignDependencyGraph:
    """Instantiate module-local dependency graphs into one concrete graph.

    Parent references such as `prober.io.rep.valid` and the child module's local
    `io.rep.valid` map to the same flat signal ID. This lets a backward slice
    cross a real instance boundary without inventing semantic connector names.
    """

    module_graphs = module_graphs or build_all_dependency_graphs(text, design)
    flat = DesignDependencyGraph(
        top=design.top,
        module_graphs=module_graphs,
    )

    def instantiate(
        module_name: str,
        instance_path: str,
        stack: tuple[str, ...],
    ) -> None:
        if module_name in stack:
            raise ValueError(
                "Recursive module hierarchy detected: "
                + " -> ".join(stack + (module_name,))
            )

        flat.instances[instance_path] = module_name
        module = design.modules.get(module_name)
        graph = module_graphs.get(module_name)
        if module is None or module.external or graph is None:
            return

        for local_name, info in graph.signals.items():
            flat_name = _map_local_ref(instance_path, graph, local_name)
            candidate = FlatSignalInfo(
                id=flat_name,
                instance_path=flat_name.split("::", 1)[0],
                module=(
                    graph.instance_modules.get(_head_segment(local_name), module_name)
                    if _head_segment(local_name) in graph.instance_modules
                    else module_name
                ),
                local_name=flat_name.split("::", 1)[1],
                kind=info.kind,
                source=info.source,
            )
            previous = flat.signals.get(flat_name)
            # Parent instance-port references and child-local ports intentionally
            # share one flat identity. Prefer the child PORT definition because
            # its kind/source locator is more precise than the parent's instance
            # reference when both are available.
            if (
                previous is None
                or previous.kind in {SignalKind.UNKNOWN, SignalKind.INSTANCE_PORT}
                and candidate.kind is SignalKind.PORT
            ):
                flat.signals[flat_name] = candidate

        for edge in graph.edges:
            src = _map_local_ref(instance_path, graph, edge.src)
            dst = _map_local_ref(instance_path, graph, edge.dst)
            statements = tuple(
                FlatStatementRef(instance_path, module_name, statement_id)
                for statement_id in edge.statement_ids
            )
            flat.edges.append(
                FlatDependencyEdge(
                    src=src,
                    dst=dst,
                    kind=edge.kind,
                    statements=statements,
                    source=edge.source,
                )
            )

        if instance_path == design.top:
            for local_input in graph.input_ports:
                flat.top_inputs.add(_flat_id(instance_path, local_input))

        for instance in module.instances:
            instantiate(
                instance.module,
                f"{instance_path}.{instance.name}",
                stack + (module_name,),
            )

    instantiate(design.top, design.top, ())
    return flat


def discover_design_events(
    design: Design,
) -> tuple[DesignEventOccurrence, ...]:
    out: list[DesignEventOccurrence] = []

    def visit(module_name: str, instance_path: str, stack: tuple[str, ...]) -> None:
        if module_name in stack:
            raise ValueError("Recursive module hierarchy")
        module = design.modules.get(module_name)
        if module is None or module.external:
            return

        boundary = discover_boundary(module)
        registry = discover_boundary_events(module, boundary)
        for event in registry.sorted_events():
            out.append(
                DesignEventOccurrence(
                    event_id=f"{instance_path}::{event.channel}.fire",
                    instance_path=instance_path,
                    module=module_name,
                    channel=event.channel,
                    direction=event.direction,
                    predicate=event.predicate,
                    valid_signal=_flat_id(instance_path, event.valid.path),
                    ready_signal=(
                        _flat_id(instance_path, event.ready.path)
                        if event.ready is not None
                        else None
                    ),
                    payload_signals=tuple(
                        _flat_id(instance_path, port.path)
                        for port in event.payload
                    ),
                    local_event=event,
                )
            )

        for instance in module.instances:
            visit(
                instance.module,
                f"{instance_path}.{instance.name}",
                stack + (module_name,),
            )

    visit(design.top, design.top, ())
    return tuple(sorted(out, key=lambda event: event.event_id))


def backward_design_slice(
    graph: DesignDependencyGraph,
    seeds: Iterable[str],
    *,
    include_clock: bool = False,
    include_reset: bool = False,
    stop_at_top_inputs: bool = True,
    max_signals: int | None = None,
) -> DesignSliceResult:
    allowed = {
        DependencyKind.DATA,
        DependencyKind.CONTROL,
        DependencyKind.STATE,
        DependencyKind.ADDRESS,
        DependencyKind.MEMORY,
        DependencyKind.ALIAS,
    }
    if include_clock:
        allowed.add(DependencyKind.CLOCK)
    if include_reset:
        allowed.add(DependencyKind.RESET)

    pred: dict[str, list[FlatDependencyEdge]] = defaultdict(list)
    for edge in graph.edges:
        if edge.kind in allowed:
            pred[edge.dst].append(edge)

    seed_tuple = tuple(sorted(set(seeds)))
    visited = set(seed_tuple)
    selected: set[FlatDependencyEdge] = set()
    frontier: set[str] = set()
    queue = deque(seed_tuple)
    truncated = False

    while queue:
        signal = queue.popleft()
        if stop_at_top_inputs and signal in graph.top_inputs:
            frontier.add(signal)
            continue

        incoming = pred.get(signal, ())
        if not incoming:
            frontier.add(signal)
            continue

        for edge in incoming:
            selected.add(edge)
            if edge.src not in visited:
                if max_signals is not None and len(visited) >= max_signals:
                    truncated = True
                    continue
                visited.add(edge.src)
                queue.append(edge.src)

    touched_instances = {
        signal.split("::", 1)[0]
        for signal in visited
        if "::" in signal
    }
    incomplete_instances = {
        instance_path
        for instance_path in touched_instances
        if (
            graph.instances.get(instance_path) in graph.module_graphs
            and not graph.module_graphs[graph.instances[instance_path]].complete
        )
    }
    sources = [
        edge.source
        for edge in selected
        if edge.source is not None
    ]

    return DesignSliceResult(
        seeds=seed_tuple,
        signals=frozenset(visited),
        edges=tuple(
            sorted(
                selected,
                key=lambda edge: (edge.dst, edge.src, edge.kind.value),
            )
        ),
        instances=tuple(sorted(touched_instances)),
        frontier=tuple(sorted(frontier)),
        source_spans=_spans_from_sources(sources),
        incomplete_instances=tuple(sorted(incomplete_instances)),
        truncated=truncated,
    )
