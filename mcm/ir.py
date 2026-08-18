from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Iterable, Mapping, Tuple


Bindings = Tuple[Tuple[str, str], ...]


def _normalize_bindings(bindings: Mapping[str, object] | Iterable[tuple[str, object]] = ()) -> Bindings:
    if isinstance(bindings, Mapping):
        items = bindings.items()
    else:
        items = bindings
    return tuple(sorted((str(key), str(value)) for key, value in items))


@dataclass(frozen=True, order=True)
class EventRef:
    """A symbolic occurrence of an event kind.

    Examples:
        ProbeRecv
        ReqAccept(req=r, mshr=m)
        RespOut(req=r, mshr=m)

    The bindings distinguish occurrences that belong to different logical
    requests/transactions.
    """

    kind: str
    bindings: Bindings = ()

    @staticmethod
    def of(kind: str, **bindings: object) -> "EventRef":
        return EventRef(kind, _normalize_bindings(bindings))

    def renamed(self, kind: str) -> "EventRef":
        return EventRef(kind, self.bindings)

    def binding(self, key: str) -> str | None:
        for name, value in self.bindings:
            if name == key:
                return value
        return None

    def has_keys(self, keys: Iterable[str]) -> bool:
        available = {key for key, _ in self.bindings}
        return all(key in available for key in keys)

    def agrees_on(self, other: "EventRef", keys: Iterable[str]) -> bool:
        for key in keys:
            left = self.binding(key)
            right = other.binding(key)
            if left is None or right is None or left != right:
                return False
        return True

    def __str__(self) -> str:
        if not self.bindings:
            return self.kind
        args = ", ".join(f"{key}={value}" for key, value in self.bindings)
        return f"{self.kind}({args})"


def as_event_ref(value: EventRef | str) -> EventRef:
    if isinstance(value, EventRef):
        return value
    if isinstance(value, str):
        return EventRef(value)
    raise TypeError(f"Expected EventRef or str, got {type(value)!r}")


@dataclass(frozen=True, order=True)
class PredicateRef:
    """A symbolic state/control predicate, optionally bound to an occurrence."""

    name: str
    bindings: Bindings = ()

    @staticmethod
    def of(name: str, **bindings: object) -> "PredicateRef":
        return PredicateRef(name, _normalize_bindings(bindings))

    def __str__(self) -> str:
        if not self.bindings:
            return self.name
        args = ", ".join(f"{key}={value}" for key, value in self.bindings)
        return f"{self.name}({args})"


def as_predicate_ref(value: PredicateRef | str) -> PredicateRef:
    if isinstance(value, PredicateRef):
        return value
    if isinstance(value, str):
        return PredicateRef(value)
    raise TypeError(f"Expected PredicateRef or str, got {type(value)!r}")


@dataclass(frozen=True, order=True)
class OutcomeRef:
    """A symbolic boundary/control consequence such as Kill(load=Y)."""

    name: str
    bindings: Bindings = ()

    @staticmethod
    def of(name: str, **bindings: object) -> "OutcomeRef":
        return OutcomeRef(name, _normalize_bindings(bindings))

    def __str__(self) -> str:
        if not self.bindings:
            return self.name
        args = ", ".join(f"{key}={value}" for key, value in self.bindings)
        return f"{self.name}({args})"


@dataclass(frozen=True, order=True)
class Event:
    """Metadata for an event kind in one abstraction layer."""

    name: str
    owner: str
    boundary: bool = False


@dataclass(frozen=True, order=True)
class Before:
    """Strict temporal/order relation: src occurs before dst."""

    src: EventRef | str
    dst: EventRef | str

    def __post_init__(self) -> None:
        object.__setattr__(self, "src", as_event_ref(self.src))
        object.__setattr__(self, "dst", as_event_ref(self.dst))
        if self.src == self.dst:
            raise ValueError("Before relation must be irreflexive")


@dataclass(frozen=True, order=True)
class Literal:
    """A boolean case condition such as Dirty or !Executed(load=O)."""

    predicate: PredicateRef | str
    positive: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "predicate", as_predicate_ref(self.predicate))

    @property
    def name(self) -> str:
        """Compatibility accessor for unparameterized v0 code."""
        return self.predicate.name

    def negate(self) -> "Literal":
        return Literal(self.predicate, not self.positive)

    def __str__(self) -> str:
        return str(self.predicate) if self.positive else f"!{self.predicate}"


@dataclass(frozen=True)
class Guard:
    """Conjunction of boolean literals. The empty conjunction denotes True."""

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
        by_predicate: dict[PredicateRef, set[bool]] = {}
        for lit in self.literals:
            by_predicate.setdefault(lit.predicate, set()).add(lit.positive)
        bad = [str(pred) for pred, signs in by_predicate.items() if len(signs) > 1]
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
    """Pure event-kind renaming/grouping that preserves occurrence bindings."""

    mapping: Mapping[str, str]

    def normalize(self, event: EventRef | str) -> EventRef:
        ref = as_event_ref(event)
        return ref.renamed(self.mapping.get(ref.kind, ref.kind))
