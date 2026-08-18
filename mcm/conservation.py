from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .ir import Before, Case, EventRef, as_event_ref
from .project import _transitive_closure


@dataclass(frozen=True, order=True)
class OneOfBetween:
    """A resource-lifecycle boundary consequence.

    Semantics:
        start < end
          =>
        at least one event in choices occurs strictly between them.
    """

    start: EventRef
    choices: tuple[EventRef, ...]
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

    token_keys identify the logical token, for example (req, mshr).
    scope_keys identify the context that a barrier belongs to, for example mshr.
    """

    name: str
    resource: str
    enter: EventRef
    exits: tuple[EventRef, ...]
    empty_at: tuple[EventRef, ...]
    token_keys: tuple[str, ...]
    scope_keys: tuple[str, ...]
    provenance: tuple[str, ...] = ()

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
        enter_ref = as_event_ref(enter)
        exit_refs = tuple(sorted({as_event_ref(event) for event in exits}))
        barrier_refs = tuple(sorted({as_event_ref(event) for event in empty_at}))
        token_keys_tuple = tuple(token_keys)
        scope_keys_tuple = tuple(scope_keys)

        if not exit_refs:
            raise ValueError("ResourceInvariant requires at least one exit")
        if not barrier_refs:
            raise ValueError("ResourceInvariant requires at least one empty barrier")
        if enter_ref in exit_refs or enter_ref in barrier_refs:
            raise ValueError("enter must differ from exits/barriers")

        if token_keys_tuple and not enter_ref.has_keys(token_keys_tuple):
            raise ValueError("enter is missing token identity bindings")
        for event in exit_refs:
            if token_keys_tuple and not event.agrees_on(enter_ref, token_keys_tuple):
                raise ValueError(
                    f"exit {event} does not belong to the same token as {enter_ref}"
                )

        if scope_keys_tuple and not enter_ref.has_keys(scope_keys_tuple):
            raise ValueError("enter is missing scope bindings")
        for event in barrier_refs:
            if scope_keys_tuple and not event.agrees_on(enter_ref, scope_keys_tuple):
                raise ValueError(
                    f"barrier {event} does not belong to the same scope as {enter_ref}"
                )

        return ResourceInvariant(
            name=name,
            resource=resource,
            enter=enter_ref,
            exits=exit_refs,
            empty_at=barrier_refs,
            token_keys=token_keys_tuple,
            scope_keys=scope_keys_tuple,
            provenance=tuple(provenance),
        )


def _closest_boundary_predecessors(
    enter: EventRef,
    closure: set[Before],
    boundary_events: set[EventRef],
    token_keys: tuple[str, ...],
) -> set[EventRef]:
    """Find the nearest token-compatible boundary frontier before enter."""

    candidates = {
        event
        for event in boundary_events
        if (
            event == enter or Before(event, enter) in closure
        )
        and (
            not token_keys or event.agrees_on(enter, token_keys)
        )
    }

    closest: set[EventRef] = set()
    for candidate in candidates:
        shadowed = False
        for other in candidates:
            if candidate == other:
                continue
            if (
                Before(candidate, other) in closure
                and (other == enter or Before(other, enter) in closure)
            ):
                shadowed = True
                break
        if not shadowed:
            closest.add(candidate)
    return closest


def derive_resource_summaries(
    case: Case,
    invariant: ResourceInvariant,
    boundary_events: set[EventRef | str],
) -> list[OneOfBetween]:
    """Project a manually supplied token-conservation invariant to the boundary."""

    boundary = {as_event_ref(event) for event in boundary_events}

    missing_exits = set(invariant.exits) - boundary
    missing_barriers = set(invariant.empty_at) - boundary
    if missing_exits:
        raise ValueError(
            f"v1.1 requires boundary-visible resource exits; missing: "
            f"{sorted(map(str, missing_exits))}"
        )
    if missing_barriers:
        raise ValueError(
            f"v1.1 requires boundary-visible barriers; missing: "
            f"{sorted(map(str, missing_barriers))}"
        )

    closure = _transitive_closure(case.facts)
    starts = _closest_boundary_predecessors(
        invariant.enter,
        closure,
        boundary,
        invariant.token_keys,
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
