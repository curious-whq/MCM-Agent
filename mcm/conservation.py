from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set, Tuple

from .ir import Before, Case, EventRef
from .project import _transitive_closure


def _same_bindings(
    left: EventRef,
    right: EventRef,
    keys: Iterable[str],
    *,
    require_present: bool = True,
) -> bool:
    for key in keys:
        left_value = left.get(key)
        right_value = right.get(key)
        if require_present and (left_value is None or right_value is None):
            return False
        if left_value != right_value:
            return False
    return True


@dataclass(frozen=True, order=True)
class OneOfBetween:
    """Boundary lifecycle axiom over symbolic event occurrences.

    Semantics:
        start < end
          =>
        exists c in choices . start < c < end

    Because choices are EventRef objects, request/scope identity is part of the
    axiom rather than an informal side condition.
    """

    start: EventRef
    choices: Tuple[EventRef, ...]
    end: EventRef

    def __post_init__(self) -> None:
        if not self.choices:
            raise ValueError("OneOfBetween requires at least one choice")
        if self.start == self.end:
            raise ValueError("OneOfBetween start and end must differ")
        if self.start in self.choices or self.end in self.choices:
            raise ValueError("Choice events must differ from start/end")


@dataclass(frozen=True)
class ResourceInvariant:
    """Per-token conservation rule for an internal resource.

    token_keys identify the logical token, e.g. ("req",).
    scope_keys identify the containing resource instance, e.g. ("mshr",).

    Every exit must carry the same token and scope bindings as enter. Barriers
    need only carry the same scope binding because GrantAck(m) is per MSHR, not
    per request r.
    """

    name: str
    resource: str
    enter: EventRef
    exits: Tuple[EventRef, ...]
    empty_at: Tuple[EventRef, ...]
    token_keys: Tuple[str, ...]
    scope_keys: Tuple[str, ...]
    provenance: Tuple[str, ...] = ()

    @staticmethod
    def build(
        name: str,
        resource: str,
        enter: EventRef | str,
        exits: Iterable[EventRef | str],
        empty_at: Iterable[EventRef | str],
        token_keys: Iterable[str] = (),
        scope_keys: Iterable[str] = (),
        provenance: Iterable[str] = (),
    ) -> "ResourceInvariant":
        enter_ref = EventRef.coerce(enter)
        exits_tuple = tuple(sorted({EventRef.coerce(x) for x in exits}))
        empty_tuple = tuple(sorted({EventRef.coerce(x) for x in empty_at}))
        token_tuple = tuple(sorted(set(token_keys)))
        scope_tuple = tuple(sorted(set(scope_keys)))

        if not exits_tuple:
            raise ValueError("ResourceInvariant requires at least one exit")
        if not empty_tuple:
            raise ValueError("ResourceInvariant requires at least one empty barrier")
        if set(token_tuple) & set(scope_tuple):
            raise ValueError("token_keys and scope_keys must be disjoint")
        if enter_ref in exits_tuple or enter_ref in empty_tuple:
            raise ValueError("enter must be distinct from exits/barriers")

        for key in token_tuple + scope_tuple:
            if enter_ref.get(key) is None:
                raise ValueError(f"enter is missing identity binding: {key}")

        identity_keys = token_tuple + scope_tuple
        for exit_ref in exits_tuple:
            if not _same_bindings(exit_ref, enter_ref, identity_keys):
                raise ValueError(
                    "resource exit does not match enter token/scope: "
                    f"enter={enter_ref}, exit={exit_ref}"
                )

        for barrier in empty_tuple:
            if not _same_bindings(barrier, enter_ref, scope_tuple):
                raise ValueError(
                    "resource barrier does not match enter scope: "
                    f"enter={enter_ref}, barrier={barrier}"
                )

        return ResourceInvariant(
            name=name,
            resource=resource,
            enter=enter_ref,
            exits=exits_tuple,
            empty_at=empty_tuple,
            token_keys=token_tuple,
            scope_keys=scope_tuple,
            provenance=tuple(provenance),
        )


def _closest_boundary_predecessors(
    enter: EventRef,
    closure: set[Before],
    boundary_event_kinds: Set[str],
    identity_keys: Tuple[str, ...],
) -> set[EventRef]:
    """Find the closest boundary predecessors that name the same token/scope."""

    nodes: set[EventRef] = {enter}
    for edge in closure:
        nodes.add(edge.src)
        nodes.add(edge.dst)

    candidates = {
        node
        for node in nodes
        if node.kind in boundary_event_kinds
        and (node == enter or Before(node, enter) in closure)
        and _same_bindings(node, enter, identity_keys)
    }

    closest: set[EventRef] = set()
    for candidate in candidates:
        shadowed = False
        for other in candidates:
            if candidate == other:
                continue
            if Before(candidate, other) in closure and (
                other == enter or Before(other, enter) in closure
            ):
                shadowed = True
                break
        if not shadowed:
            closest.add(candidate)
    return closest


def derive_resource_summaries(
    case: Case,
    invariant: ResourceInvariant,
    boundary_events: Set[str],
) -> list[OneOfBetween]:
    """Project a same-token resource invariant to the module boundary.

    v1.1 requires all exits and barriers to already be boundary-visible and
    requires the boundary start to carry the same token/scope bindings as the
    internal enter event.
    """

    missing_exits = {
        ref.kind for ref in invariant.exits if ref.kind not in boundary_events
    }
    missing_barriers = {
        ref.kind for ref in invariant.empty_at if ref.kind not in boundary_events
    }
    if missing_exits:
        raise ValueError(
            "v1.1 requires boundary-visible resource exits; missing: "
            f"{sorted(missing_exits)}"
        )
    if missing_barriers:
        raise ValueError(
            "v1.1 requires boundary-visible barriers; missing: "
            f"{sorted(missing_barriers)}"
        )

    closure = _transitive_closure(case.facts)
    identity_keys = invariant.token_keys + invariant.scope_keys
    starts = _closest_boundary_predecessors(
        invariant.enter,
        closure,
        boundary_events,
        identity_keys,
    )

    out: list[OneOfBetween] = []
    for start in sorted(starts):
        for end in invariant.empty_at:
            if start == end:
                continue
            out.append(
                OneOfBetween(
                    start=start,
                    choices=invariant.exits,
                    end=end,
                )
            )
    return out
