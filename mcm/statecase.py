from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .ir import Guard, Literal, OutcomeRef, PredicateRef


@dataclass(frozen=True)
class StateCase:
    """A guarded state/control case with symbolic boundary outcomes."""

    name: str
    guard: Guard
    outcomes: tuple[OutcomeRef, ...]
    provenance: tuple[str, ...] = ()

    @staticmethod
    def build(
        name: str,
        guard: Guard,
        outcomes: Iterable[OutcomeRef],
        provenance: Iterable[str] = (),
    ) -> "StateCase":
        return StateCase(
            name=name,
            guard=guard,
            outcomes=tuple(sorted(set(outcomes))),
            provenance=tuple(provenance),
        )


def _combine_adjacent_guards(left: Guard, right: Guard) -> Guard | None:
    """Combine two boolean cubes that differ in exactly one predicate polarity.

    Example:
        !Executed(O) & !Succeeded(O)
        Executed(O)  & !Succeeded(O)

    becomes:
        !Succeeded(O)

    The transformation is exact because the two cubes differ only in the value
    of one predicate.
    """

    left_map = {lit.predicate: lit.positive for lit in left.literals}
    right_map = {lit.predicate: lit.positive for lit in right.literals}

    if set(left_map) != set(right_map):
        return None

    differing = [
        predicate
        for predicate in left_map
        if left_map[predicate] != right_map[predicate]
    ]
    if len(differing) != 1:
        return None

    dropped = differing[0]
    common = [
        Literal(predicate, positive)
        for predicate, positive in left_map.items()
        if predicate != dropped
    ]
    return Guard.of(*common)


def _minimize_guard_group(
    cases: list[StateCase],
) -> list[StateCase]:
    """Iteratively combine adjacent guards with the same consequence."""

    current: dict[Guard, set[str]] = {}
    for case in cases:
        current.setdefault(case.guard, set()).update(
            case.provenance + (case.name,)
        )

    while True:
        guards = list(current)
        combined_indices: set[int] = set()
        next_map: dict[Guard, set[str]] = {}
        any_combined = False

        for i in range(len(guards)):
            for j in range(i + 1, len(guards)):
                merged = _combine_adjacent_guards(guards[i], guards[j])
                if merged is None:
                    continue
                any_combined = True
                combined_indices.add(i)
                combined_indices.add(j)
                prov = set(current[guards[i]]) | set(current[guards[j]])
                next_map.setdefault(merged, set()).update(prov)

        for i, guard in enumerate(guards):
            if i not in combined_indices:
                next_map.setdefault(guard, set()).update(current[guard])

        if not any_combined or set(next_map) == set(current):
            current = next_map
            break

        current = next_map

    outcomes = cases[0].outcomes
    return [
        StateCase.build(
            name=f"state-summary:{index}",
            guard=guard,
            outcomes=outcomes,
            provenance=sorted(provenance),
        )
        for index, (guard, provenance) in enumerate(
            sorted(current.items(), key=lambda item: str(item[0]))
        )
    ]


def merge_state_cases(cases: Iterable[StateCase]) -> list[StateCase]:
    """Merge only state cases with exactly identical boundary outcomes.

    Guard minimization is purely boolean and occurrence-aware: predicates bound
    to different loads are different variables and therefore cannot be merged.
    """

    groups: dict[tuple[OutcomeRef, ...], list[StateCase]] = defaultdict(list)
    for case in cases:
        groups[case.outcomes].append(case)

    out: list[StateCase] = []
    for group in groups.values():
        out.extend(_minimize_guard_group(group))

    return sorted(
        out,
        key=lambda case: (
            tuple(map(str, case.outcomes)),
            str(case.guard),
        ),
    )
