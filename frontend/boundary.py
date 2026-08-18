from __future__ import annotations

from dataclasses import dataclass

from .model import GroundType, LeafPort, ModuleDef, PortDirection, SourceLoc


@dataclass(frozen=True, order=True)
class BoundaryPort:
    module: str
    path: str
    direction: PortDirection
    type: GroundType
    source: SourceLoc | None

    @property
    def leaf_name(self) -> str:
        if "." in self.path:
            return self.path.rsplit(".", 1)[-1]
        return self.path


_CLOCK_RESET_TYPES = {"Clock", "Reset", "AsyncReset"}


def discover_boundary(
    module: ModuleDef,
    include_clock_reset: bool = False,
) -> tuple[BoundaryPort, ...]:
    """Return physical leaf ports visible at the module boundary."""

    out: list[BoundaryPort] = []

    for leaf in module.leaf_ports():
        if (
            not include_clock_reset
            and leaf.type.name in _CLOCK_RESET_TYPES
        ):
            continue

        out.append(
            BoundaryPort(
                module=module.name,
                path=leaf.path,
                direction=leaf.direction,
                type=leaf.type,
                source=leaf.source,
            )
        )

    return tuple(sorted(out, key=lambda port: port.path))
