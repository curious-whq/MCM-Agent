from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Set

from .ir import Before, Case


def _transitive_closure(edges: Iterable[Before]) -> set[Before]:
    """Compute strict transitive closure for a finite Before graph."""

    succ: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set()
    for edge in edges:
        succ[edge.src].add(edge.dst)
        nodes.add(edge.src)
        nodes.add(edge.dst)

    out: set[Before] = set()
    for src in nodes:
        stack = list(succ[src])
        seen: set[str] = set()
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
    """Remove redundant edges from an acyclic strict-order graph.

    The prototype expects per-case Before facts to be acyclic. If a cycle is
    present, the case is rejected because it cannot represent a strict order.
    """

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


def project_case(case: Case, boundary_events: Set[str]) -> Case:
    """Project a leaf case onto a module boundary.

    1. Close Before transitively so paths through internal events are preserved.
    2. Drop facts whose endpoints are not both boundary-visible.
    3. Reduce redundant boundary edges while preserving the same strict order.

    The guard is deliberately preserved in v0; guard abstraction is a separate
    future problem.
    """

    closure = _transitive_closure(case.facts)
    boundary_edges = {
        edge
        for edge in closure
        if edge.src in boundary_events and edge.dst in boundary_events
    }
    reduced = _transitive_reduction_dag(boundary_edges)
    return Case.build(
        name=f"{case.name}:projected",
        guard=case.guard,
        facts=reduced,
        provenance=case.provenance + (case.name,),
    )
