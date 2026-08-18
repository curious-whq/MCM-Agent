from __future__ import annotations

from dataclasses import dataclass, field

from .abstraction_tree import AbstractionTree, build_abstraction_tree
from .boundary import discover_boundary
from .coverage import build_coverage_ledger
from .connectors import (
    HandshakeConnector,
    HandshakeTransportPath,
    discover_direct_handshake_connectors,
    discover_handshake_transport_path,
)
from .dependency import (
    ModuleDependencyGraph,
    ModuleGraphProvider,
    build_all_dependency_graphs,
)
from .design_graph import (
    DesignDependencyGraph,
    DesignEventOccurrence,
    DesignSliceResult,
    backward_design_slice,
    backward_design_slice_lazy,
    backward_instance_slice_lazy,
    discover_design_events,
    flatten_design_dependency_graph,
)
from .export import design_slice_manifest_dict, slice_manifest_dict
from .firrtl import parse_firrtl
from .input_contract import InputValidationReport, require_supported_static_input
from .model import Design
from .partition import PartitionPlan, discover_partition_plan
from .registry import EventRegistry, PhysicalEvent, discover_boundary_events
from .slice import EventSliceMode, SliceOptions, SliceResult, slice_event


@dataclass(frozen=True)
class ModuleStaticStatus:
    module: str
    complete: bool
    statement_count: int
    unsupported_count: int
    event_count: int


@dataclass(frozen=True)
class StaticFrontendReport:
    top: str
    modules: tuple[ModuleStaticStatus, ...]

    @property
    def complete(self) -> bool:
        return all(module.complete for module in self.modules)


@dataclass
class StaticFrontend:
    """Orchestrates every deterministic stage before any LLM is invoked."""

    text: str
    design: Design
    graphs: dict[str, ModuleDependencyGraph]
    registries: dict[str, EventRegistry]
    input_report: InputValidationReport
    graph_provider: ModuleGraphProvider | None = None
    eager: bool = True
    _design_graph: DesignDependencyGraph | None = field(default=None, init=False)
    _scoped_design_graph: DesignDependencyGraph | None = field(default=None, init=False)
    _design_events: tuple[DesignEventOccurrence, ...] | None = field(default=None, init=False)
    _design_connectors: tuple[HandshakeConnector, ...] | None = field(default=None, init=False)
    _abstraction_tree: AbstractionTree | None = field(default=None, init=False)

    @staticmethod
    def from_firrtl(
        text: str,
        *,
        eager: bool = True,
    ) -> "StaticFrontend":
        input_report = require_supported_static_input(text)
        design = parse_firrtl(text)
        provider = ModuleGraphProvider.create(text, design)
        graphs = (
            build_all_dependency_graphs(text, design)
            if eager
            else provider.cache
        )
        registries: dict[str, EventRegistry] = {}

        for module_name, module in design.modules.items():
            if module.external:
                continue
            registries[module_name] = discover_boundary_events(
                module,
                discover_boundary(module),
            )

        return StaticFrontend(
            text=text,
            design=design,
            graphs=graphs,
            registries=registries,
            input_report=input_report,
            graph_provider=provider,
            eager=eager,
        )

    def graph(self, module_name: str) -> ModuleDependencyGraph:
        cached = self.graphs.get(module_name)
        if cached is not None:
            return cached
        if self.graph_provider is None:
            raise KeyError(f"No graph for module {module_name!r}")
        graph = self.graph_provider.require(module_name)
        self.graphs[module_name] = graph
        return graph

    def report(
        self,
        module_names: tuple[str, ...] | None = None,
    ) -> StaticFrontendReport:
        modules: list[ModuleStaticStatus] = []
        if module_names is None:
            names = (
                tuple(sorted(self.graphs))
                if self.eager
                else tuple(sorted(self.graphs))
            )
        else:
            names = tuple(sorted(set(module_names)))
        for module_name in names:
            graph = self.graph(module_name)
            ledger = build_coverage_ledger(graph)
            registry = self.registries[module_name]
            modules.append(
                ModuleStaticStatus(
                    module=module_name,
                    complete=ledger.complete,
                    statement_count=len(graph.statements),
                    unsupported_count=len(ledger.unsupported),
                    event_count=len(registry.events),
                )
            )
        return StaticFrontendReport(
            top=self.design.top,
            modules=tuple(modules),
        )

    def assert_complete(self, *module_names: str) -> None:
        names = module_names or tuple(sorted(self.graphs))
        errors: list[str] = []
        for name in names:
            graph = self.graph(name)
            unsupported = graph.unsupported_statements
            if unsupported:
                preview = "; ".join(
                    f"line {statement.firrtl_line}: {statement.text}"
                    for statement in unsupported[:5]
                )
                errors.append(
                    f"{name}: {len(unsupported)} unsupported statement(s): {preview}"
                )
        if errors:
            raise ValueError("Static frontend is incomplete:\n" + "\n".join(errors))

    def event(self, module_name: str, event_id: str) -> PhysicalEvent:
        try:
            return self.registries[module_name].events[event_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown event {event_id!r} in module {module_name!r}"
            ) from exc

    def slice_event(
        self,
        module_name: str,
        event_id: str,
        *,
        mode: EventSliceMode = EventSliceMode.OCCURRENCE,
        options: SliceOptions | None = None,
    ) -> SliceResult:
        return slice_event(
            self.graph(module_name),
            self.event(module_name, event_id),
            mode=mode,
            options=options,
        )

    def slice_manifest(
        self,
        module_name: str,
        event_id: str,
        *,
        mode: EventSliceMode = EventSliceMode.FULL,
        options: SliceOptions | None = None,
    ) -> dict:
        event = self.event(module_name, event_id)
        graph = self.graph(module_name)
        result = slice_event(
            graph,
            event,
            mode=mode,
            options=options,
        )
        return slice_manifest_dict(
            graph,
            event,
            result,
        )

    def partition(self, module_name: str) -> PartitionPlan:
        return discover_partition_plan(
            self.graph(module_name),
            self.registries[module_name],
        )

    def abstraction_tree(self) -> AbstractionTree:
        if self._abstraction_tree is None:
            if not self.eager:
                for name, module in self.design.modules.items():
                    if not module.external:
                        self.graph(name)
            self._abstraction_tree = build_abstraction_tree(
                self.design,
                self.graphs,
                self.registries,
            )
        return self._abstraction_tree

    def design_graph(self) -> DesignDependencyGraph:
        if self._design_graph is None:
            if not self.eager:
                for name, module in self.design.modules.items():
                    if not module.external:
                        self.graph(name)
            self._design_graph = flatten_design_dependency_graph(
                self.text,
                self.design,
                self.graphs,
            )
        return self._design_graph

    def design_events(self) -> tuple[DesignEventOccurrence, ...]:
        if self._design_events is None:
            self._design_events = discover_design_events(self.design)
        return self._design_events

    def design_event(self, event_id: str) -> DesignEventOccurrence:
        for event in self.design_events():
            if event.event_id == event_id:
                return event
        raise KeyError(f"Unknown design event: {event_id}")

    def design_connectors(self) -> tuple[HandshakeConnector, ...]:
        if self._design_connectors is None:
            self._design_connectors = discover_direct_handshake_connectors(
                self.design_graph(),
                self.design_events(),
            )
        return self._design_connectors

    def handshake_transport(
        self,
        from_event_id: str,
        to_event_id: str,
        *,
        max_signals: int = 250_000,
    ) -> HandshakeTransportPath:
        """Recover an end-to-end physical Decoupled route lazily.

        This operation intentionally avoids materializing the entire design
        graph.  It is therefore the preferred primitive for answering a
        connectivity question in full Chipyard FIRRTL before computing any
        potentially huge semantic event cone.
        """

        if self.graph_provider is None:
            raise RuntimeError("Static frontend has no module graph provider")
        source = self.design_event(from_event_id)
        sink = self.design_event(to_event_id)
        return discover_handshake_transport_path(
            self.design,
            self.graph_provider,
            source,
            sink,
            max_signals=max_signals,
        )

    def _slice_instance_event_with_graph(
        self,
        event_id: str,
        *,
        root_instance: str | None = None,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> tuple[DesignDependencyGraph, DesignSliceResult]:
        """Slice one concrete ownership subtree without escaping to its parent."""

        if self.graph_provider is None:
            raise RuntimeError("Static frontend has no module graph provider")
        event = self.design_event(event_id)
        graph, result = backward_instance_slice_lazy(
            self.design,
            self.graph_provider,
            event,
            root_instance=root_instance,
            include_payload=include_payload,
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        self.graphs.update(self.graph_provider.cache)
        return graph, result

    def slice_instance_event(
        self,
        event_id: str,
        *,
        root_instance: str | None = None,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> DesignSliceResult:
        _, result = self._slice_instance_event_with_graph(
            event_id,
            root_instance=root_instance,
            include_payload=include_payload,
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        return result

    def instance_slice_manifest(
        self,
        event_id: str,
        *,
        root_instance: str | None = None,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> dict:
        event = self.design_event(event_id)
        graph, result = self._slice_instance_event_with_graph(
            event_id,
            root_instance=root_instance,
            include_payload=include_payload,
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        manifest = design_slice_manifest_dict(graph, event, result)
        root = root_instance or event.instance_path
        manifest["scope"] = "instance_subtree"
        manifest["subtree_root"] = root
        touched_events = tuple(
            candidate
            for candidate in self.design_events()
            if candidate.instance_path in result.instances
        )
        manifest["direct_connectors"] = [
            {
                "from_event": connector.from_event,
                "to_event": connector.to_event,
                "valid_edge": list(connector.valid_edge),
                "ready_edge": list(connector.ready_edge),
            }
            for connector in discover_direct_handshake_connectors(
                graph, touched_events
            )
        ]
        return manifest

    def _slice_design_event_with_graph(
        self,
        event_id: str,
        *,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> tuple[DesignDependencyGraph, DesignSliceResult]:
        event = self.design_event(event_id)
        if not self.eager and self.graph_provider is not None:
            graph, result = backward_design_slice_lazy(
                self.design,
                self.graph_provider,
                event,
                include_payload=include_payload,
                include_clock=include_clock,
                include_reset=include_reset,
                max_signals=max_signals,
            )
            self.graphs.update(self.graph_provider.cache)
            self._scoped_design_graph = graph
            return graph, result

        graph = self.design_graph()
        result = backward_design_slice(
            graph,
            event.seeds(include_payload=include_payload),
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        return graph, result

    def slice_design_event(
        self,
        event_id: str,
        *,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> DesignSliceResult:
        _, result = self._slice_design_event_with_graph(
            event_id,
            include_payload=include_payload,
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        return result

    def design_slice_manifest(
        self,
        event_id: str,
        *,
        include_payload: bool = False,
        include_clock: bool = False,
        include_reset: bool = False,
        max_signals: int | None = None,
    ) -> dict:
        event = self.design_event(event_id)
        graph, result = self._slice_design_event_with_graph(
            event_id,
            include_payload=include_payload,
            include_clock=include_clock,
            include_reset=include_reset,
            max_signals=max_signals,
        )
        manifest = design_slice_manifest_dict(
            graph,
            event,
            result,
        )
        touched_events = tuple(
            candidate
            for candidate in self.design_events()
            if candidate.instance_path in result.instances
        )
        touched_event_ids = {candidate.event_id for candidate in touched_events}
        scoped_connectors = discover_direct_handshake_connectors(
            graph, touched_events
        )
        manifest["direct_connectors"] = [
            {
                "from_event": connector.from_event,
                "to_event": connector.to_event,
                "valid_edge": list(connector.valid_edge),
                "ready_edge": list(connector.ready_edge),
            }
            for connector in scoped_connectors
            if (
                connector.from_event in touched_event_ids
                and connector.to_event in touched_event_ids
            )
        ]
        return manifest
