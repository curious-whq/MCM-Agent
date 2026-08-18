from __future__ import annotations

from dataclasses import dataclass

from .dependency import DependencyKind, ModuleGraphProvider, SignalKind
from .design_graph import (
    DependencyPath,
    DesignDependencyGraph,
    DesignEventOccurrence,
    FlatDependencyEdge,
    LazyDesignExplorer,
)
from .model import Design
from .registry import ChannelDirection


@dataclass(frozen=True, order=True)
class HandshakeConnector:
    """A mechanically proven direct valid/ready connector between endpoints.

    `valid_from -> valid_to` and `ready_to -> ready_from` must both be direct
    DATA/ALIAS dependencies in the concrete design graph. If gates, arbiters or
    combinational nodes intervene, this class deliberately refuses to skip them.
    """

    from_event: str
    to_event: str
    valid_edge: tuple[str, str]
    ready_edge: tuple[str, str]


@dataclass(frozen=True)
class HandshakeTransportPath:
    """A mechanically recovered end-to-end Decoupled transport route.

    Unlike :class:`HandshakeConnector`, a transport path is allowed to cross
    buffers, arbiters, width widgets and hierarchy boundaries.  It does *not*
    assert that two endpoint events are the same semantic transaction.  It only
    proves physical dependency reachability for both halves of a Decoupled
    handshake:

      source.valid -> ... -> sink.valid
      sink.ready   -> ... -> source.ready

    This distinction is important for whole-Chipyard analysis: a giant event
    cone is often unnecessary when the immediate question is simply which
    physical interconnect chain carries a message between two endpoints.
    """

    from_event: str
    to_event: str
    valid_path: DependencyPath
    ready_path: DependencyPath
    instances: tuple[str, ...]
    stateful_instances: tuple[str, ...]

    @property
    def found(self) -> bool:
        return self.valid_path.found and self.ready_path.found

    @property
    def complete(self) -> bool:
        return self.valid_path.complete and self.ready_path.complete



def _direct_edge(
    graph: DesignDependencyGraph,
    src: str,
    dst: str,
) -> FlatDependencyEdge | None:
    for edge in graph.edges:
        if (
            edge.src == src
            and edge.dst == dst
            and edge.kind in {DependencyKind.DATA, DependencyKind.ALIAS}
        ):
            return edge
    return None



def _link_orientation(
    graph: DesignDependencyGraph,
    source: DesignEventOccurrence,
    sink: DesignEventOccurrence,
    direct_pairs: set[tuple[str, str]] | None = None,
) -> HandshakeConnector | None:
    if source.ready_signal is None or sink.ready_signal is None:
        return None
    if direct_pairs is None:
        valid_ok = _direct_edge(graph, source.valid_signal, sink.valid_signal) is not None
        ready_ok = _direct_edge(graph, sink.ready_signal, source.ready_signal) is not None
    else:
        valid_ok = (source.valid_signal, sink.valid_signal) in direct_pairs
        ready_ok = (sink.ready_signal, source.ready_signal) in direct_pairs
    if not valid_ok or not ready_ok:
        return None
    return HandshakeConnector(
        from_event=source.event_id,
        to_event=sink.event_id,
        valid_edge=(source.valid_signal, sink.valid_signal),
        ready_edge=(sink.ready_signal, source.ready_signal),
    )



def discover_direct_handshake_connectors(
    graph: DesignDependencyGraph,
    events: tuple[DesignEventOccurrence, ...],
) -> tuple[HandshakeConnector, ...]:
    """Discover direct physical endpoint links without semantic naming.

    Two endpoint events are linked only when both halves of the Decoupled
    handshake are directly wired in opposite flow directions. This is stricter
    than reachability and intentionally refuses to skip over gates/arbiters.
    """

    out: set[HandshakeConnector] = set()
    # v5 scanned every flat edge for every event pair, which is fine for a
    # tiny fixture but becomes pathological for a 10k-signal real slice.
    # Index direct DATA/ALIAS edges once so endpoint checks are O(1).
    direct_pairs = {
        (edge.src, edge.dst)
        for edge in graph.edges
        if edge.kind in {DependencyKind.DATA, DependencyKind.ALIAS}
    }

    for index, left in enumerate(events):
        for right in events[index + 1 :]:
            forward = _link_orientation(graph, left, right, direct_pairs)
            reverse = _link_orientation(graph, right, left, direct_pairs)
            if forward is not None:
                out.add(forward)
            if reverse is not None:
                out.add(reverse)

    return tuple(sorted(out))



def _stateful_instances_on_paths(
    explorer: LazyDesignExplorer,
    *paths: DependencyPath,
) -> tuple[str, ...]:
    """Return route instances whose selected path touches state/memory leaves."""

    out: set[str] = set()
    for path in paths:
        for edge in path.edges:
            for signal in (edge.src, edge.dst):
                info = explorer.graph.signals.get(signal)
                if info is None:
                    continue
                if info.kind in {SignalKind.REGISTER, SignalKind.MEMORY}:
                    out.add(info.instance_path)
    return tuple(sorted(out))



def discover_handshake_transport_path(
    design: Design,
    provider: ModuleGraphProvider,
    source: DesignEventOccurrence,
    sink: DesignEventOccurrence,
    *,
    max_signals: int = 250_000,
) -> HandshakeTransportPath:
    """Recover one physical end-to-end path for both valid and ready.

    This routine is designed for large elaborated systems.  It uses lazy module
    graph materialization and path search instead of building the complete
    flattened graph or computing the union of an entire event cone.

    The endpoint direction is structural and must be a send -> receive pair.
    Semantic equality, transaction identity, and protocol meaning are expressly
    outside this static primitive.
    """

    if source.direction is not ChannelDirection.SEND:
        raise ValueError(
            f"Transport source must be a send event, got {source.direction.value}: "
            f"{source.event_id}"
        )
    if sink.direction is not ChannelDirection.RECEIVE:
        raise ValueError(
            f"Transport sink must be a receive event, got {sink.direction.value}: "
            f"{sink.event_id}"
        )
    if source.ready_signal is None or sink.ready_signal is None:
        raise ValueError("Transport path requires Decoupled valid/ready endpoints")

    explorer = LazyDesignExplorer(design, provider)

    def search_from_shallower(physical_source: str, physical_target: str) -> DependencyPath:
        source_instance = physical_source.split("::", 1)[0]
        target_instance = physical_target.split("::", 1)[0]
        source_depth = source_instance.count(".")
        target_depth = target_instance.count(".")
        # Interconnect-side endpoints are usually structurally shallower than
        # core-internal endpoints. Searching from that side avoids exploding
        # into the entire BOOM core through an arbiter before reaching the
        # narrow physical route. Edge orientation is unchanged.
        direction = "forward" if source_depth <= target_depth else "reverse"
        return explorer.find_path(
            physical_source,
            physical_target,
            direction=direction,
            max_signals=max_signals,
        )

    valid = search_from_shallower(
        source.valid_signal,
        sink.valid_signal,
    )
    ready = search_from_shallower(
        sink.ready_signal,
        source.ready_signal,
    )

    instances = tuple(
        sorted(set(valid.instances) | set(ready.instances))
    )
    return HandshakeTransportPath(
        from_event=source.event_id,
        to_event=sink.event_id,
        valid_path=valid,
        ready_path=ready,
        instances=instances,
        stateful_instances=_stateful_instances_on_paths(explorer, valid, ready),
    )
