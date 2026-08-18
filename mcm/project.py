from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .ir import Before, Case, EventRef, as_event_ref


def _transitive_closure(edges: Iterable[Before]) -> set[Before]:
    """Compute strict transitive closure for a finite Before graph."""

    succ: dict[EventRef, set[EventRef]] = defaultdict(set)
    nodes: set[EventRef] = set()
    for edge in edges:
        succ[edge.src].add(edge.dst)
        nodes.add(edge.src)
        nodes.add(edge.dst)

    out: set[Before] = set()
    for src in nodes:
        stack = list(succ[src])
        seen: set[EventRef] = set()
        while stack:
            dst = stack.pop()
            if dst in seen:
                continue
            seen.add(dst)
            if src != dst:
                out.add(Before(src, dst))
            stack.extend(succ[dst] - seen)
    return out


def _transitive_reduction_dag(edges: set[Before]) -> set[Before]:
    """Remove redundant edges from an acyclic strict-order graph."""

    closure = _transitive_closure(edges)
    for edge in edges:
        if Before(edge.dst, edge.src) in closure:
            raise ValueError("Cycle detected in strict Before relation")

    reduced = set(edges)
    for edge in list(edges):
        reduced.remove(edge)
        alt_closure = _transitive_closure(reduced)
        if edge not in alt_closure:
            reduced.add(edge)
    return reduced


def project_case(
    case: Case,
    boundary_events: set[EventRef | str],
) -> Case:
    """Project a leaf ordering case onto a module boundary."""

    boundary = {as_event_ref(event) for event in boundary_events}
    closure = _transitive_closure(case.facts)
    boundary_edges = {
        edge
        for edge in closure
        if edge.src in boundary and edge.dst in boundary
    }
    reduced = _transitive_reduction_dag(boundary_edges)
    return Case.build(
        name=f"{case.name}:projected",
        guard=case.guard,
        facts=reduced,
        provenance=case.provenance + (case.name,),
    )
