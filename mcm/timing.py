from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .ir import EventRef, Guard, OutcomeRef, as_event_ref


@dataclass(frozen=True, order=True)
class DeltaDomain:
    """Allowed cycle distances between two symbolic event occurrences.

    Semantics:
        cycle(second) - cycle(first) is in allowed

    A finite set is used deliberately. Merging domains takes exact set union,
    so v3 never fills timing gaps by assumption.
    """

    first: EventRef
    second: EventRef
    allowed: frozenset[int]

    def __post_init__(self) -> None:
        if self.first == self.second:
            raise ValueError("Timing relation endpoints must differ")
        if not self.allowed:
            raise ValueError("DeltaDomain requires at least one allowed delta")
        if any(delta < 0 for delta in self.allowed):
            raise ValueError("v3 only supports non-negative forward cycle deltas")

    @staticmethod
    def exact(
        first: EventRef | str,
        second: EventRef | str,
        cycles: int,
    ) -> "DeltaDomain":
        return DeltaDomain(
            first=as_event_ref(first),
            second=as_event_ref(second),
            allowed=frozenset({cycles}),
        )

    def key(self) -> tuple[EventRef, EventRef]:
        return self.first, self.second


@dataclass(frozen=True, order=True)
class CycleDelta:
    """Exact relation: second occurs `cycles` cycles after first."""

    first: EventRef | str
    second: EventRef | str
    cycles: int

    def to_domain(self) -> DeltaDomain:
        return DeltaDomain.exact(self.first, self.second, self.cycles)


@dataclass(frozen=True, order=True)
class SameCycle:
    """Exact relation: two events occur in the same cycle."""

    first: EventRef | str
    second: EventRef | str

    def to_domain(self) -> DeltaDomain:
        return DeltaDomain.exact(self.first, self.second, 0)


@dataclass(frozen=True, order=True)
class Next:
    """Exact relation: second occurs exactly one cycle after first."""

    first: EventRef | str
    second: EventRef | str

    def to_domain(self) -> DeltaDomain:
        return DeltaDomain.exact(self.first, self.second, 1)


TimingRelation = DeltaDomain | CycleDelta | SameCycle | Next


def _as_domain(relation: TimingRelation) -> DeltaDomain:
    if isinstance(relation, DeltaDomain):
        return relation
    return relation.to_domain()


@dataclass(frozen=True)
class TimingCube:
    """Conjunction of exact/finite timing constraints."""

    domains: tuple[DeltaDomain, ...] = ()

    @staticmethod
    def of(*relations: TimingRelation) -> "TimingCube":
        by_key: dict[tuple[EventRef, EventRef], frozenset[int]] = {}

        for relation in relations:
            domain = _as_domain(relation)
            key = domain.key()

            if key in by_key:
                # Two constraints on the same pair are a conjunction, so their
                # allowed sets must intersect.
                intersection = by_key[key] & domain.allowed
                if not intersection:
                    raise ValueError(
                        f"Contradictory timing constraints for "
                        f"{domain.first} -> {domain.second}"
                    )
                by_key[key] = intersection
            else:
                by_key[key] = domain.allowed

        domains = tuple(
            DeltaDomain(first, second, allowed)
            for (first, second), allowed in sorted(by_key.items())
        )
        return TimingCube(domains)

    def domain_for(
        self,
        first: EventRef | str,
        second: EventRef | str,
    ) -> DeltaDomain | None:
        first_ref = as_event_ref(first)
        second_ref = as_event_ref(second)
        for domain in self.domains:
            if domain.first == first_ref and domain.second == second_ref:
                return domain
        return None


@dataclass(frozen=True)
class TimingCase:
    """A guarded timing case with a set of tracked boundary effects."""

    name: str
    guard: Guard
    timing: TimingCube
    outcomes: tuple[OutcomeRef, ...]
    provenance: tuple[str, ...] = ()

    @staticmethod
    def build(
        name: str,
        guard: Guard,
        timing: TimingCube,
        outcomes: Iterable[OutcomeRef],
        provenance: Iterable[str] = (),
    ) -> "TimingCase":
        return TimingCase(
            name=name,
            guard=guard,
            timing=timing,
            outcomes=tuple(sorted(set(outcomes))),
            provenance=tuple(provenance),
        )


def _merge_timing_cubes(
    left: TimingCube,
    right: TimingCube,
) -> TimingCube | None:
    """Exactly combine cubes that differ in only one timing domain.

    The differing domain is merged by finite set union. No missing cycle is
    inserted, so {0} and {2} becomes {0, 2}, never the interval [0, 2].
    """

    left_map = {domain.key(): domain.allowed for domain in left.domains}
    right_map = {domain.key(): domain.allowed for domain in right.domains}

    if set(left_map) != set(right_map):
        return None

    differing = [
        key
        for key in left_map
        if left_map[key] != right_map[key]
    ]
    if len(differing) != 1:
        return None

    merged_key = differing[0]
    merged_domains: list[DeltaDomain] = []

    for key in sorted(left_map):
        allowed = (
            left_map[key] | right_map[key]
            if key == merged_key
            else left_map[key]
        )
        merged_domains.append(
            DeltaDomain(key[0], key[1], frozenset(allowed))
        )

    return TimingCube(tuple(merged_domains))


def _minimize_timing_group(cases: list[TimingCase]) -> list[TimingCase]:
    current: dict[TimingCube, set[str]] = {}

    for case in cases:
        current.setdefault(case.timing, set()).update(
            case.provenance + (case.name,)
        )

    while True:
        cubes = list(current)
        combined_indices: set[int] = set()
        next_map: dict[TimingCube, set[str]] = {}
        any_combined = False

        for i in range(len(cubes)):
            for j in range(i + 1, len(cubes)):
                merged = _merge_timing_cubes(cubes[i], cubes[j])
                if merged is None:
                    continue

                any_combined = True
                combined_indices.add(i)
                combined_indices.add(j)
                provenance = set(current[cubes[i]]) | set(current[cubes[j]])
                next_map.setdefault(merged, set()).update(provenance)

        for index, cube in enumerate(cubes):
            if index not in combined_indices:
                next_map.setdefault(cube, set()).update(current[cube])

        if not any_combined or set(next_map) == set(current):
            current = next_map
            break

        current = next_map

    reference = cases[0]
    return [
        TimingCase.build(
            name=f"timing-summary:{index}",
            guard=reference.guard,
            timing=cube,
            outcomes=reference.outcomes,
            provenance=sorted(provenance),
        )
        for index, (cube, provenance) in enumerate(
            sorted(current.items(), key=lambda item: repr(item[0]))
        )
    ]


def merge_timing_cases(cases: Iterable[TimingCase]) -> list[TimingCase]:
    """Merge timing cases only when non-timing guard and outcomes are identical."""

    groups: dict[
        tuple[Guard, tuple[OutcomeRef, ...]],
        list[TimingCase],
    ] = {}

    for case in cases:
        key = (case.guard, case.outcomes)
        groups.setdefault(key, []).append(case)

    out: list[TimingCase] = []
    for group in groups.values():
        out.extend(_minimize_timing_group(group))

    return sorted(
        out,
        key=lambda case: (
            tuple(map(str, case.outcomes)),
            str(case.guard),
            repr(case.timing),
        ),
    )
