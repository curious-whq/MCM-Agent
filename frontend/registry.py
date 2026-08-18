from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .boundary import BoundaryPort
from .model import ModuleDef, PortDirection, SourceLoc


class ChannelDirection(str, Enum):
    RECEIVE = "receive"
    SEND = "send"


class EventProtocol(str, Enum):
    """Physical occurrence convention inferred only from port structure."""

    DECOUPLED = "decoupled"
    VALID = "valid"


@dataclass(frozen=True)
class PhysicalEvent:
    """A mechanically grounded physical boundary event.

    v5 deliberately uses structural names such as:
        BoomProbeUnit.io.req.fire
        BoomMSHR.io.meta_resp.valid

    Semantic aliases such as "ProbeRecv" are NOT invented here.
    """

    event_id: str
    module: str
    channel: str
    direction: ChannelDirection
    protocol: EventProtocol
    predicate: str
    valid: BoundaryPort
    ready: BoundaryPort | None
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
        return tuple(self.events[key] for key in sorted(self.events))


def _channel_prefix(path: str) -> tuple[str, str] | None:
    if "." not in path:
        return None
    prefix, leaf = path.rsplit(".", 1)
    if leaf not in {"valid", "ready"}:
        return None
    return prefix, leaf


def _unique_sources(*ports: BoundaryPort | None) -> tuple[SourceLoc, ...]:
    seen: set[SourceLoc] = set()
    out: list[SourceLoc] = []

    for port in ports:
        if port is None or port.source is None or port.source in seen:
            continue
        seen.add(port.source)
        out.append(port.source)

    return tuple(out)


def _payload_for(
    boundary: tuple[BoundaryPort, ...],
    prefix: str,
) -> tuple[BoundaryPort, ...]:
    payload_prefix = f"{prefix}.bits"
    return tuple(
        port
        for port in boundary
        if (
            port.path == payload_prefix
            or port.path.startswith(payload_prefix + ".")
            or port.path.startswith(payload_prefix + "[")
        )
    )


def discover_decoupled_events(
    module: ModuleDef,
    boundary: tuple[BoundaryPort, ...],
) -> EventRegistry:
    """Discover Decoupled-style valid/ready physical handshakes."""

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
            continue

        payload = _payload_for(boundary, prefix)
        event = PhysicalEvent(
            event_id=f"{module.name}.{prefix}.fire",
            module=module.name,
            channel=prefix,
            direction=direction,
            protocol=EventProtocol.DECOUPLED,
            predicate=f"{prefix}.valid && {prefix}.ready",
            valid=valid,
            ready=ready,
            payload=payload,
            sources=_unique_sources(valid, ready, *payload),
        )
        registry.register(event)

    return registry


def discover_valid_events(
    module: ModuleDef,
    boundary: tuple[BoundaryPort, ...],
) -> EventRegistry:
    """Discover one-way Valid-style boundary occurrences.

    A candidate requires a `.valid` leaf, no sibling `.ready`, and at least one
    `.bits` payload leaf. Nested prefixes below another channel's `.bits` are
    intentionally skipped to avoid treating payload fields as top-level events.
    """

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
        if valid is None or ready is not None:
            continue
        if ".bits." in prefix or prefix.endswith(".bits"):
            continue

        payload = _payload_for(boundary, prefix)
        if not payload:
            continue

        direction = (
            ChannelDirection.RECEIVE
            if valid.direction is PortDirection.INPUT
            else ChannelDirection.SEND
        )
        registry.register(
            PhysicalEvent(
                event_id=f"{module.name}.{prefix}.valid",
                module=module.name,
                channel=prefix,
                direction=direction,
                protocol=EventProtocol.VALID,
                predicate=f"{prefix}.valid",
                valid=valid,
                ready=None,
                payload=payload,
                sources=_unique_sources(valid, *payload),
            )
        )

    return registry


def discover_boundary_events(
    module: ModuleDef,
    boundary: tuple[BoundaryPort, ...],
) -> EventRegistry:
    """Discover all v5-supported structural boundary event conventions."""

    registry = EventRegistry.empty()
    for partial in (
        discover_decoupled_events(module, boundary),
        discover_valid_events(module, boundary),
    ):
        for event in partial.sorted_events():
            registry.register(event)
    return registry
