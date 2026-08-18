from __future__ import annotations

from dataclasses import dataclass

from .dependency import DependencyKind
from .design_graph import (
    DesignDependencyGraph,
    DesignEventOccurrence,
    FlatDependencyEdge,
)


@dataclass(frozen=True, order=True)
class HandshakeConnector:
    """A mechanically proven direct valid/ready connector between endpoints.

    `valid_from -> valid_to` and `ready_to -> ready_from` must both be direct
    DATA/ALIAS dependencies in the concrete design graph. If gates, arbiters or
    combinational nodes intervene, v5 does not call it a direct connector.
    """

    from_event: str
    to_event: str
    valid_edge: tuple[str, str]
    ready_edge: tuple[str, str]


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
) -> HandshakeConnector | None:
    if source.ready_signal is None or sink.ready_signal is None:
        return None
    valid = _direct_edge(graph, source.valid_signal, sink.valid_signal)
    ready = _direct_edge(graph, sink.ready_signal, source.ready_signal)
    if valid is None or ready is None:
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

    for index, left in enumerate(events):
        for right in events[index + 1 :]:
            forward = _link_orientation(graph, left, right)
            reverse = _link_orientation(graph, right, left)
            if forward is not None:
                out.add(forward)
            if reverse is not None:
                out.add(reverse)

    return tuple(sorted(out))
