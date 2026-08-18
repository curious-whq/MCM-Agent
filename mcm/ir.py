from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, FrozenSet, Tuple


@dataclass(frozen=True, order=True)
class Event:
    """A named event in one abstraction layer.

    boundary=True means the event is externally visible at the current module
    boundary. Internal events may be used in leaf cases but are eliminated by
    projection.
    """

    name: str
    owner: str
    boundary: bool = False


@dataclass(frozen=True, order=True)
class Before:
    """Strict temporal/order relation: src occurs before dst."""

    src: str
    dst: str

    def __post_init__(self) -> None:
        if self.src == self.dst:
            raise ValueError("Before relation must be irreflexive")


@dataclass(frozen=True, order=True)
class Literal:
    """A boolean case condition such as Dirty or !Dirty.

    This first prototype deliberately does not invent semantic predicates. A
    Literal is only a symbolic condition already supplied by the leaf model.
    """

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
    """Pure boundary renaming/grouping.

    Example:
        ProbeAck -> ProbeResponse
        ProbeAckData -> ProbeResponse

    Aliases are definitional only; they do not add semantic constraints.
    """

    mapping: Mapping[str, str]

    def normalize(self, event_name: str) -> str:
        return self.mapping.get(event_name, event_name)
