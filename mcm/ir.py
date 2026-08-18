from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Iterable, Mapping, Tuple


@dataclass(frozen=True, order=True)
class Event:
    """A named event kind in one abstraction layer.

    Event describes the static event kind/owner. Dynamic or symbolic occurrences
    are represented by EventRef below.
    """

    name: str
    owner: str
    boundary: bool = False


@dataclass(frozen=True, order=True)
class EventRef:
    """A symbolic occurrence of an event kind with identity bindings.

    Example:
        EventRef.of("RespOut", req="r", mshr="m")

    represents RespOut(r, m). The parameter values are symbolic names in the
    hand-written prototype; later frontends may bind them to RTL transaction IDs
    or proof variables.
    """

    kind: str
    params: Tuple[Tuple[str, str], ...] = ()

    @staticmethod
    def of(kind: str, **params: str) -> "EventRef":
        return EventRef(kind=kind, params=tuple(sorted(params.items())))

    @staticmethod
    def coerce(value: "EventRef | str") -> "EventRef":
        if isinstance(value, EventRef):
            return value
        if isinstance(value, str):
            return EventRef(value)
        raise TypeError(f"Expected EventRef or str, got {type(value).__name__}")

    def get(self, key: str) -> str | None:
        for name, value in self.params:
            if name == key:
                return value
        return None

    def with_kind(self, kind: str) -> "EventRef":
        return EventRef(kind=kind, params=self.params)

    def __str__(self) -> str:
        if not self.params:
            return self.kind
        args = ", ".join(f"{key}={value}" for key, value in self.params)
        return f"{self.kind}({args})"


@dataclass(frozen=True, order=True)
class Before:
    """Strict temporal/order relation: src occurs before dst.

    String endpoints are accepted as shorthand for unparameterized EventRef
    objects, preserving the v0 Probe example syntax.
    """

    src: EventRef | str
    dst: EventRef | str

    def __post_init__(self) -> None:
        src = EventRef.coerce(self.src)
        dst = EventRef.coerce(self.dst)
        object.__setattr__(self, "src", src)
        object.__setattr__(self, "dst", dst)
        if src == dst:
            raise ValueError("Before relation must be irreflexive")


@dataclass(frozen=True, order=True)
class Literal:
    """A boolean case condition such as Dirty or !Dirty."""

    name: str
    positive: bool = True

    def negate(self) -> "Literal":
        return Literal(self.name, not self.positive)

    def __str__(self) -> str:
        return self.name if self.positive else f"!{self.name}"


@dataclass(frozen=True)
class Guard:
    """Conjunction of boolean literals.

    The empty conjunction denotes True. Contradictory conjunctions are rejected.
    """

    literals: FrozenSet[Literal] = field(default_factory=frozenset)

    @staticmethod
    def true() -> "Guard":
        return Guard()

    @staticmethod
    def of(*literals: Literal) -> "Guard":
        guard = Guard(frozenset(literals))
        guard._validate()
        return guard

    def _validate(self) -> None:
        by_name: dict[str, set[bool]] = {}
        for lit in self.literals:
            by_name.setdefault(lit.name, set()).add(lit.positive)
        bad = [name for name, signs in by_name.items() if len(signs) > 1]
        if bad:
            raise ValueError(f"Contradictory guard literals: {bad}")

    def is_true(self) -> bool:
        return not self.literals

    def __str__(self) -> str:
        if self.is_true():
            return "true"
        return " & ".join(sorted(map(str, self.literals)))


@dataclass(frozen=True)
class Case:
    """A guarded set of microarchitectural ordering facts."""

    name: str
    guard: Guard
    facts: Tuple[Before, ...]
    provenance: Tuple[str, ...] = ()

    @staticmethod
    def build(
        name: str,
        guard: Guard,
        facts: Iterable[Before],
        provenance: Iterable[str] = (),
    ) -> "Case":
        unique = tuple(sorted(set(facts)))
        return Case(name, guard, unique, tuple(provenance))


@dataclass(frozen=True)
class AliasMap:
    """Pure event-kind renaming/grouping that preserves identity parameters.

    Example:
        ProbeAck(req=r)     -> ProbeResponse(req=r)
        ProbeAckData(req=r) -> ProbeResponse(req=r)
    """

    mapping: Mapping[str, str]

    def normalize(self, event: EventRef | str) -> EventRef:
        ref = EventRef.coerce(event)
        return ref.with_kind(self.mapping.get(ref.kind, ref.kind))
