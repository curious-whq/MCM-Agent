from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class PortDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"

    def flipped(self) -> "PortDirection":
        return (
            PortDirection.OUTPUT
            if self is PortDirection.INPUT
            else PortDirection.INPUT
        )


@dataclass(frozen=True, order=True)
class SourceLoc:
    """A source locator preserved from FIRRTL/CIRCT textual IR."""

    file: str
    line: int
    column: int | None = None
    raw: str | None = None

    @staticmethod
    def parse(text: str | None) -> "SourceLoc | None":
        if text is None:
            return None

        raw = text.strip()
        if not raw:
            return None

        # FIRRTL source info commonly looks like:
        #   @[src/Foo.scala 12:34]
        # We parse from the right so paths containing spaces remain usable.
        import re

        match = re.match(r"^(.*)\s+(\d+)(?::(\d+))?$", raw)
        if match is None:
            return SourceLoc(file=raw, line=0, column=None, raw=raw)

        file, line, column = match.groups()
        return SourceLoc(
            file=file,
            line=int(line),
            column=int(column) if column is not None else None,
            raw=raw,
        )


class FirrtlType:
    pass


@dataclass(frozen=True)
class GroundType(FirrtlType):
    name: str
    width: str | None = None

    def __str__(self) -> str:
        return self.name if self.width is None else f"{self.name}<{self.width}>"


@dataclass(frozen=True)
class BundleField:
    name: str
    type: FirrtlType
    flipped: bool = False


@dataclass(frozen=True)
class BundleType(FirrtlType):
    fields: tuple[BundleField, ...]


@dataclass(frozen=True)
class VectorType(FirrtlType):
    element: FirrtlType
    size: int


@dataclass(frozen=True)
class Port:
    name: str
    direction: PortDirection
    type: FirrtlType
    source: SourceLoc | None = None


@dataclass(frozen=True)
class LeafPort:
    """A flattened physical leaf of a possibly aggregate FIRRTL port."""

    path: str
    direction: PortDirection
    type: GroundType
    source: SourceLoc | None = None

    @property
    def leaf_name(self) -> str:
        if "." in self.path:
            return self.path.rsplit(".", 1)[-1]
        return self.path


@dataclass(frozen=True)
class Instance:
    name: str
    module: str
    source: SourceLoc | None = None


@dataclass(frozen=True)
class ModuleDef:
    name: str
    ports: tuple[Port, ...]
    instances: tuple[Instance, ...]
    source: SourceLoc | None = None
    external: bool = False

    def leaf_ports(self) -> tuple[LeafPort, ...]:
        out: list[LeafPort] = []
        for port in self.ports:
            out.extend(
                flatten_type(
                    port.type,
                    prefix=port.name,
                    direction=port.direction,
                    source=port.source,
                )
            )
        return tuple(out)


@dataclass(frozen=True)
class Design:
    top: str
    modules: dict[str, ModuleDef]
    source: SourceLoc | None = None

    def module(self, name: str) -> ModuleDef:
        try:
            return self.modules[name]
        except KeyError as exc:
            raise KeyError(f"Unknown module: {name}") from exc


def flatten_type(
    type_: FirrtlType,
    prefix: str,
    direction: PortDirection,
    source: SourceLoc | None,
) -> list[LeafPort]:
    """Flatten FIRRTL aggregate orientation into physical module directions."""

    if isinstance(type_, GroundType):
        return [
            LeafPort(
                path=prefix,
                direction=direction,
                type=type_,
                source=source,
            )
        ]

    if isinstance(type_, BundleType):
        out: list[LeafPort] = []
        for field in type_.fields:
            field_direction = direction.flipped() if field.flipped else direction
            out.extend(
                flatten_type(
                    field.type,
                    prefix=f"{prefix}.{field.name}",
                    direction=field_direction,
                    source=source,
                )
            )
        return out

    if isinstance(type_, VectorType):
        out: list[LeafPort] = []
        for index in range(type_.size):
            out.extend(
                flatten_type(
                    type_.element,
                    prefix=f"{prefix}[{index}]",
                    direction=direction,
                    source=source,
                )
            )
        return out

    raise TypeError(f"Unsupported FIRRTL type: {type(type_).__name__}")
