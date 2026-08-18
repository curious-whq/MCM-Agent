from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .boundary import BoundaryPort
from .model import ModuleDef, PortDirection, SourceLoc


class ChannelDirection(str, Enum):
    RECEIVE = "receive"
    SEND = "send"


@dataclass(frozen=True)
class PhysicalEvent:
    """A mechanically grounded physical handshake event.

    v4 deliberately uses structural names such as:
        BoomProbeUnit.io.req.fire

    Semantic aliases such as "ProbeRecv" are NOT invented here.
    """

    event_id: str
    module: str
    channel: str
    direction: ChannelDirection
    predicate: str
    valid: BoundaryPort
    ready: BoundaryPort
    payload: tuple[BoundaryPort, ...]
    sources: tuple[SourceLoc, ...]


@dataclass
class EventRegistry:
    events: dict[str, PhysicalEvent]

    @staticmethod
    def empty() -> "EventRegistry":
        return EventRegistry(events={})

    def register(self, event: PhysicalEvent) -> None:
        if event.event_id in self.events:
            raise ValueError(f"Duplicate physical event: {event.event_id}")
        self.events[event.event_id] = event

    def sorted_events(self) -> tuple[PhysicalEvent, ...]:
        return tuple(
            self.events[key]
            for key in sorted(self.events)
        )


def _channel_prefix(path: str) -> tuple[str, str] | None:
    if "." not in path:
        return None
    prefix, leaf = path.rsplit(".", 1)
    if leaf not in {"valid", "ready"}:
        return None
    return prefix, leaf


def _unique_sources(
    *ports: BoundaryPort,
) -> tuple[SourceLoc, ...]:
    seen: set[SourceLoc] = set()
    out: list[SourceLoc] = []

    for port in ports:
        if port.source is None or port.source in seen:
            continue
        seen.add(port.source)
        out.append(port.source)

    return tuple(out)


def discover_decoupled_events(
    module: ModuleDef,
    boundary: tuple[BoundaryPort, ...],
) -> EventRegistry:
    """Discover Decoupled-style physical handshakes from leaf directions.

    A channel is recognized only if the same prefix has both `.valid` and
    `.ready` leaves and their directions are opposite.

    receive:
        valid is input, ready is output

    send:
        valid is output, ready is input
    """

    by_path = {port.path: port for port in boundary}

    channel_members: dict[str, dict[str, BoundaryPort]] = {}

    for port in boundary:
        split = _channel_prefix(port.path)
        if split is None:
            continue
        prefix, leaf = split
        channel_members.setdefault(prefix, {})[leaf] = port

    registry = EventRegistry.empty()

    for prefix in sorted(channel_members):
        members = channel_members[prefix]
        valid = members.get("valid")
        ready = members.get("ready")

        if valid is None or ready is None:
            continue

        if (
            valid.direction is PortDirection.INPUT
            and ready.direction is PortDirection.OUTPUT
        ):
            direction = ChannelDirection.RECEIVE
        elif (
            valid.direction is PortDirection.OUTPUT
            and ready.direction is PortDirection.INPUT
        ):
            direction = ChannelDirection.SEND
        else:
            # Same-direction valid/ready is not a Decoupled boundary channel.
            continue

        payload_prefix = f"{prefix}.bits"
        payload = tuple(
            port
            for port in boundary
            if (
                port.path == payload_prefix
                or port.path.startswith(payload_prefix + ".")
                or port.path.startswith(payload_prefix + "[")
            )
        )

        event_id = f"{module.name}.{prefix}.fire"
        event = PhysicalEvent(
            event_id=event_id,
            module=module.name,
            channel=prefix,
            direction=direction,
            predicate=f"{prefix}.valid && {prefix}.ready",
            valid=valid,
            ready=ready,
            payload=payload,
            sources=_unique_sources(valid, ready, *payload),
        )
        registry.register(event)

    return registry
