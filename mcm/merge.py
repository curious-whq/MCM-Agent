from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .ir import AliasMap, Before, Case, Guard
from .project import _transitive_reduction_dag


def normalize_case(case: Case, aliases: AliasMap) -> Case:
    """Normalize boundary event kinds while preserving occurrence bindings."""

    normalized: set[Before] = set()
    for fact in case.facts:
        src = aliases.normalize(fact.src)
        dst = aliases.normalize(fact.dst)
        if src == dst:
            continue
        normalized.add(Before(src, dst))

    normalized = _transitive_reduction_dag(normalized)
    return Case.build(
        name=f"{case.name}:normalized",
        guard=case.guard,
        facts=normalized,
        provenance=case.provenance,
    )


def _guards_cover_true(guards: list[Guard]) -> bool:
    """Recognize the conservative v0 pattern P / !P."""

    if len(guards) != 2:
        return False
    g1, g2 = guards
    if len(g1.literals) != 1 or len(g2.literals) != 1:
        return False
    l1 = next(iter(g1.literals))
    l2 = next(iter(g2.literals))
    return l1.predicate == l2.predicate and l1.positive != l2.positive


def merge_equivalent_cases(cases: Iterable[Case]) -> list[Case]:
    """Merge ordering cases only when normalized consequences are identical."""

    groups: dict[tuple[Before, ...], list[Case]] = defaultdict(list)
    for case in cases:
        groups[case.facts].append(case)

    out: list[Case] = []
    for facts, group in groups.items():
        guards = [case.guard for case in group]
        if _guards_cover_true(guards):
            provenance: list[str] = []
            for case in group:
                provenance.extend(case.provenance + (case.name,))
            out.append(
                Case.build(
                    name="merged:" + "+".join(case.name for case in group),
                    guard=Guard.true(),
                    facts=facts,
                    provenance=provenance,
                )
            )
        else:
            out.extend(group)

    return sorted(out, key=lambda c: c.name)
