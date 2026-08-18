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
    ModuleGraphProvider,
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


@dataclass(frozen=True)
class InstanceHierarchyIndex:
    instances: dict[str, str]
    parents: dict[str, str | None]
    children: dict[str, tuple[str, ...]]

    def ancestors(self, instance_path: str) -> tuple[str, ...]:
        out: list[str] = []
        current: str | None = instance_path
        while current is not None:
            out.append(current)
            current = self.parents.get(current)
        return tuple(out)


def build_instance_hierarchy_index(design: Design) -> InstanceHierarchyIndex:
    instances: dict[str, str] = {}
    parents: dict[str, str | None] = {}
    children: dict[str, tuple[str, ...]] = {}

    def visit(
        module_name: str,
        instance_path: str,
        parent: str | None,
        stack: tuple[str, ...],
    ) -> None:
        if module_name in stack:
            raise ValueError(
                "Recursive module hierarchy detected: "
                + " -> ".join(stack + (module_name,))
            )
        instances[instance_path] = module_name
        parents[instance_path] = parent
        module = design.modules.get(module_name)
        if module is None or module.external:
            children[instance_path] = ()
            return
        child_paths = tuple(
            f"{instance_path}.{instance.name}"
            for instance in module.instances
        )
        children[instance_path] = child_paths
        for instance, child_path in zip(module.instances, child_paths):
            visit(
                instance.module,
                child_path,
                instance_path,
                stack + (module_name,),
            )

    visit(design.top, design.top, None, ())
    return InstanceHierarchyIndex(instances, parents, children)


def _add_instance_to_flat_graph(
    flat: DesignDependencyGraph,
    design: Design,
    provider: ModuleGraphProvider,
    hierarchy: InstanceHierarchyIndex,
    instance_path: str,
) -> bool:
    """Materialize exactly one concrete module instance into `flat`."""

    if instance_path in flat.instances:
        return True

    module_name = hierarchy.instances.get(instance_path)
    if module_name is None:
        return False

    flat.instances[instance_path] = module_name
    module = design.modules.get(module_name)
    graph = provider.get(module_name)
    if module is None or module.external or graph is None:
        return False

    flat.module_graphs[module_name] = graph

    for local_name, info in graph.signals.items():
        flat_name = _map_local_ref(instance_path, graph, local_name)
        head = _head_segment(local_name)
        candidate = FlatSignalInfo(
            id=flat_name,
            instance_path=flat_name.split("::", 1)[0],
            module=(
                graph.instance_modules.get(head, module_name)
                if head in graph.instance_modules
                else module_name
            ),
            local_name=flat_name.split("::", 1)[1],
            kind=info.kind,
            source=info.source,
        )
        previous = flat.signals.get(flat_name)
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
    return True


def backward_design_slice_lazy(
    design: Design,
    provider: ModuleGraphProvider,
    event: DesignEventOccurrence,
    *,
    include_payload: bool = False,
    include_clock: bool = False,
    include_reset: bool = False,
    stop_at_top_inputs: bool = True,
    max_signals: int | None = None,
    seed_signals: Iterable[str] | None = None,
) -> tuple[DesignDependencyGraph, DesignSliceResult]:
    """Cross-module backward slice that materializes RTL modules on demand.

    The event's module and all of its ancestors are loaded first so physical
    boundary drivers in parent modules are present.  When traversal reaches an
    output of a sibling/descendant instance, that instance is loaded only then.
    This keeps whole-Chipyard analysis proportional to the event cone instead
    of the entire 500k-line design.
    """

    hierarchy = build_instance_hierarchy_index(design)
    if event.instance_path not in hierarchy.instances:
        raise KeyError(f"Unknown event instance path: {event.instance_path}")

    flat = DesignDependencyGraph(
        top=design.top,
        module_graphs={},
    )

    # Parent logic can drive child inputs, so ancestors must exist before BFS.
    for path in reversed(hierarchy.ancestors(event.instance_path)):
        _add_instance_to_flat_graph(flat, design, provider, hierarchy, path)

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

    # `pred` is extended whenever a newly reached child instance is loaded.
    pred: dict[str, list[FlatDependencyEdge]] = defaultdict(list)
    indexed_edges = 0

    def index_new_edges() -> None:
        nonlocal indexed_edges
        while indexed_edges < len(flat.edges):
            edge = flat.edges[indexed_edges]
            indexed_edges += 1
            if edge.kind in allowed:
                pred[edge.dst].append(edge)

    index_new_edges()

    seed_tuple = tuple(
        sorted(
            set(
                seed_signals
                if seed_signals is not None
                else event.seeds(include_payload=include_payload)
            )
        )
    )
    visited = set(seed_tuple)
    processed: set[str] = set()
    selected: set[FlatDependencyEdge] = set()
    frontier: set[str] = set()
    queue = deque(seed_tuple)
    truncated = False

    while queue:
        signal = queue.popleft()
        if signal in processed:
            continue

        instance_path = signal.split("::", 1)[0] if "::" in signal else None
        if instance_path and instance_path not in flat.instances:
            parent = hierarchy.parents.get(instance_path)
            # Signals from a child instance appear only after its parent graph
            # has exposed a physical instance-port reference.
            if parent is not None and parent not in flat.instances:
                for ancestor in reversed(hierarchy.ancestors(parent)):
                    _add_instance_to_flat_graph(
                        flat, design, provider, hierarchy, ancestor
                    )
            _add_instance_to_flat_graph(
                flat, design, provider, hierarchy, instance_path
            )
            index_new_edges()

        processed.add(signal)

        if stop_at_top_inputs and signal in flat.top_inputs:
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
    incomplete_instances: set[str] = set()
    for instance_path in touched_instances:
        module_name = hierarchy.instances.get(instance_path)
        if module_name is None:
            continue
        graph = provider.get(module_name)
        if graph is not None and not graph.complete:
            incomplete_instances.add(instance_path)

    sources = [edge.source for edge in selected if edge.source is not None]
    result = DesignSliceResult(
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
    return flat, result



def backward_instance_slice_lazy(
    design: Design,
    provider: ModuleGraphProvider,
    event: DesignEventOccurrence,
    *,
    root_instance: str | None = None,
    include_payload: bool = False,
    include_clock: bool = False,
    include_reset: bool = False,
    max_signals: int | None = None,
) -> tuple[DesignDependencyGraph, DesignSliceResult]:
    """Backward slice inside one concrete hierarchical subtree.

    Whole-design cones can escape through an endpoint's `ready` input and pull
    in unrelated upstream/downstream system logic.  Hierarchical abstraction
    instead needs a *module-scoped* semantic cone: cross into children owned by
    the chosen instance, but stop at that instance's physical input boundary.

    `root_instance` defaults to the event's own concrete instance.  It may also
    name an ancestor, e.g. slice a ProbeUnit event inside the enclosing DCache
    subtree while refusing to escape into the rest of the BoomTile/system bus.
    """

    hierarchy = build_instance_hierarchy_index(design)
    if event.instance_path not in hierarchy.instances:
        raise KeyError(f"Unknown event instance path: {event.instance_path}")

    root = root_instance or event.instance_path
    if root not in hierarchy.instances:
        raise KeyError(f"Unknown subtree root instance: {root}")
    if not (
        event.instance_path == root
        or event.instance_path.startswith(root + ".")
    ):
        raise ValueError(
            f"Event {event.event_id} is outside requested subtree {root}"
        )

    flat = DesignDependencyGraph(top=design.top, module_graphs={})

    def in_scope(path: str) -> bool:
        return path == root or path.startswith(root + ".")

    # Materialize the ownership chain from the subtree root to the event.
    chain = [
        path
        for path in reversed(hierarchy.ancestors(event.instance_path))
        if in_scope(path)
    ]
    for path in chain:
        _add_instance_to_flat_graph(flat, design, provider, hierarchy, path)

    root_module = hierarchy.instances[root]
    root_graph = provider.require(root_module)
    scope_inputs = {
        _flat_id(root, local_input)
        for local_input in root_graph.input_ports
    }

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
    indexed_edges = 0

    def index_new_edges() -> None:
        nonlocal indexed_edges
        while indexed_edges < len(flat.edges):
            edge = flat.edges[indexed_edges]
            indexed_edges += 1
            if edge.kind in allowed:
                pred[edge.dst].append(edge)

    index_new_edges()

    seed_tuple = tuple(sorted(set(event.seeds(include_payload=include_payload))))
    visited = set(seed_tuple)
    processed: set[str] = set()
    selected: set[FlatDependencyEdge] = set()
    frontier: set[str] = set()
    queue = deque(seed_tuple)
    truncated = False

    while queue:
        signal = queue.popleft()
        if signal in processed:
            continue

        instance_path = signal.split("::", 1)[0] if "::" in signal else None
        if instance_path is not None and not in_scope(instance_path):
            # No dependency is allowed to leak outside the declared ownership
            # subtree. The signal itself remains explicit boundary frontier.
            processed.add(signal)
            frontier.add(signal)
            continue

        if instance_path and instance_path not in flat.instances:
            # Materialize only the missing in-scope chain. Parent modules expose
            # child instance ports, so order is root -> ... -> child.
            chain_to_child = [
                path
                for path in reversed(hierarchy.ancestors(instance_path))
                if in_scope(path)
            ]
            for path in chain_to_child:
                _add_instance_to_flat_graph(
                    flat, design, provider, hierarchy, path
                )
            index_new_edges()

        processed.add(signal)

        if signal in scope_inputs:
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
        if "::" in signal and in_scope(signal.split("::", 1)[0])
    }
    incomplete_instances: set[str] = set()
    for instance_path in touched_instances:
        module_name = hierarchy.instances.get(instance_path)
        if module_name is None:
            continue
        graph = provider.get(module_name)
        if graph is not None and not graph.complete:
            incomplete_instances.add(instance_path)

    sources = [edge.source for edge in selected if edge.source is not None]
    result = DesignSliceResult(
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
    return flat, result


@dataclass(frozen=True)
class DependencyPath:
    source: str
    target: str
    edges: tuple[FlatDependencyEdge, ...]
    instances: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]
    incomplete_instances: tuple[str, ...] = ()
    visited_signals: int = 0
    truncated: bool = False

    @property
    def found(self) -> bool:
        return self.source == self.target or bool(self.edges)

    @property
    def complete(self) -> bool:
        return self.found and not self.incomplete_instances and not self.truncated


class LazyDesignExplorer:
    """Incrementally materialize a whole-design signal graph as paths need it."""

    def __init__(self, design: Design, provider: ModuleGraphProvider):
        self.design = design
        self.provider = provider
        self.hierarchy = build_instance_hierarchy_index(design)
        self.graph = DesignDependencyGraph(top=design.top, module_graphs={})
        self._succ: dict[str, list[FlatDependencyEdge]] = defaultdict(list)
        self._pred: dict[str, list[FlatDependencyEdge]] = defaultdict(list)
        self._indexed_edges = 0
        self._allowed = {
            DependencyKind.DATA,
            DependencyKind.CONTROL,
            DependencyKind.STATE,
            DependencyKind.ADDRESS,
            DependencyKind.MEMORY,
            DependencyKind.ALIAS,
        }

    def _index_new_edges(self) -> None:
        while self._indexed_edges < len(self.graph.edges):
            edge = self.graph.edges[self._indexed_edges]
            self._indexed_edges += 1
            if edge.kind not in self._allowed:
                continue
            self._succ[edge.src].append(edge)
            self._pred[edge.dst].append(edge)

    def load_instance(self, instance_path: str) -> None:
        if instance_path in self.graph.instances:
            return
        parent = self.hierarchy.parents.get(instance_path)
        if parent is not None and parent not in self.graph.instances:
            for ancestor in reversed(self.hierarchy.ancestors(parent)):
                _add_instance_to_flat_graph(
                    self.graph,
                    self.design,
                    self.provider,
                    self.hierarchy,
                    ancestor,
                )
        _add_instance_to_flat_graph(
            self.graph,
            self.design,
            self.provider,
            self.hierarchy,
            instance_path,
        )
        self._index_new_edges()

    def prepare_endpoint(self, signal: str) -> None:
        if "::" not in signal:
            return
        instance_path = signal.split("::", 1)[0]
        for ancestor in reversed(self.hierarchy.ancestors(instance_path)):
            _add_instance_to_flat_graph(
                self.graph,
                self.design,
                self.provider,
                self.hierarchy,
                ancestor,
            )
        self._index_new_edges()

    def _path_result(
        self,
        source: str,
        target: str,
        edges: list[FlatDependencyEdge],
        *,
        visited_signals: int = 0,
        truncated: bool = False,
    ) -> DependencyPath:
        instances = {
            signal.split("::", 1)[0]
            for edge in edges
            for signal in (edge.src, edge.dst)
            if "::" in signal
        }
        incomplete: set[str] = set()
        for instance_path in instances:
            module_name = self.hierarchy.instances.get(instance_path)
            if module_name is None:
                continue
            graph = self.provider.get(module_name)
            if graph is not None and not graph.complete:
                incomplete.add(instance_path)
        return DependencyPath(
            source=source,
            target=target,
            edges=tuple(edges),
            instances=tuple(sorted(instances)),
            source_spans=_spans_from_sources(
                [edge.source for edge in edges if edge.source is not None]
            ),
            incomplete_instances=tuple(sorted(incomplete)),
            visited_signals=visited_signals,
            truncated=truncated,
        )

    def find_path(
        self,
        source: str,
        target: str,
        *,
        direction: str = "forward",
        max_signals: int = 250_000,
    ) -> DependencyPath:
        """Find one dependency path without enumerating the complete cone.

        `direction` changes only the search strategy, not edge orientation.
        `auto` performs lazy bidirectional BFS and is the default choice for
        whole-Chipyard routes where arbiters make one direction unpredictable.
        Explicit forward/reverse modes remain useful for diagnostics.
        """
        if direction not in {"forward", "reverse", "auto"}:
            raise ValueError("direction must be 'forward', 'reverse', or 'auto'")
        self.prepare_endpoint(source)
        self.prepare_endpoint(target)

        if source == target:
            return self._path_result(
                source, target, [], visited_signals=1, truncated=False
            )

        if direction == "auto":
            forward_queue = deque([source])
            reverse_queue = deque([target])
            previous: dict[str, str | None] = {source: None}
            previous_edge: dict[str, FlatDependencyEdge] = {}
            next_signal: dict[str, str | None] = {target: None}
            next_edge: dict[str, FlatDependencyEdge] = {}
            meeting: str | None = None

            def visited_count() -> int:
                return len(set(previous) | set(next_signal))

            while (
                forward_queue
                and reverse_queue
                and meeting is None
                and visited_count() < max_signals
            ):
                # Expand the smaller active frontier. This prevents a wide
                # arbiter/fanout cone on one side from dominating the route
                # query before the narrow opposite side reaches it.
                expand_forward = len(forward_queue) <= len(reverse_queue)

                if expand_forward:
                    signal = forward_queue.popleft()
                    if "::" in signal:
                        self.load_instance(signal.split("::", 1)[0])
                    for edge in self._succ.get(signal, ()):
                        nxt = edge.dst
                        if nxt in previous:
                            continue
                        previous[nxt] = signal
                        previous_edge[nxt] = edge
                        if nxt in next_signal:
                            meeting = nxt
                            break
                        forward_queue.append(nxt)
                        if visited_count() >= max_signals:
                            break
                else:
                    signal = reverse_queue.popleft()
                    if "::" in signal:
                        self.load_instance(signal.split("::", 1)[0])
                    for edge in self._pred.get(signal, ()):
                        prev = edge.src
                        if prev in next_signal:
                            continue
                        next_signal[prev] = signal
                        next_edge[prev] = edge
                        if prev in previous:
                            meeting = prev
                            break
                        reverse_queue.append(prev)
                        if visited_count() >= max_signals:
                            break

            count = visited_count()
            if meeting is None:
                return self._path_result(
                    source,
                    target,
                    [],
                    visited_signals=count,
                    truncated=(
                        bool(forward_queue)
                        and bool(reverse_queue)
                        and count >= max_signals
                    ),
                )

            prefix: list[FlatDependencyEdge] = []
            cursor = meeting
            while cursor != source:
                edge = previous_edge[cursor]
                prefix.append(edge)
                cursor = previous[cursor]  # type: ignore[assignment]
            prefix.reverse()

            suffix: list[FlatDependencyEdge] = []
            cursor = meeting
            while cursor != target:
                edge = next_edge[cursor]
                suffix.append(edge)
                cursor = next_signal[cursor]  # type: ignore[assignment]

            return self._path_result(
                source,
                target,
                prefix + suffix,
                visited_signals=count,
            )

        if direction == "forward":
            queue = deque([source])
            previous: dict[str, str | None] = {source: None}
            previous_edge: dict[str, FlatDependencyEdge] = {}

            while queue and target not in previous and len(previous) < max_signals:
                signal = queue.popleft()
                if "::" in signal:
                    self.load_instance(signal.split("::", 1)[0])
                for edge in self._succ.get(signal, ()):
                    nxt = edge.dst
                    if nxt in previous:
                        continue
                    previous[nxt] = signal
                    previous_edge[nxt] = edge
                    queue.append(nxt)

            if target not in previous:
                return self._path_result(
                    source,
                    target,
                    [],
                    visited_signals=len(previous),
                    truncated=(bool(queue) and len(previous) >= max_signals),
                )

            edges: list[FlatDependencyEdge] = []
            cursor = target
            while cursor != source:
                edge = previous_edge[cursor]
                edges.append(edge)
                cursor = previous[cursor]  # type: ignore[assignment]
            edges.reverse()
            return self._path_result(
                source, target, edges, visited_signals=len(previous)
            )

        queue = deque([target])
        next_signal: dict[str, str | None] = {target: None}
        next_edge: dict[str, FlatDependencyEdge] = {}

        while queue and source not in next_signal and len(next_signal) < max_signals:
            signal = queue.popleft()
            if "::" in signal:
                self.load_instance(signal.split("::", 1)[0])
            for edge in self._pred.get(signal, ()):
                prev = edge.src
                if prev in next_signal:
                    continue
                next_signal[prev] = signal
                next_edge[prev] = edge
                queue.append(prev)

        if source not in next_signal:
            return self._path_result(
                source,
                target,
                [],
                visited_signals=len(next_signal),
                truncated=(bool(queue) and len(next_signal) >= max_signals),
            )

        edges = []
        cursor = source
        while cursor != target:
            edge = next_edge[cursor]
            edges.append(edge)
            cursor = next_signal[cursor]  # type: ignore[assignment]
        return self._path_result(
            source, target, edges, visited_signals=len(next_signal)
        )
