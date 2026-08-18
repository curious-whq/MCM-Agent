from mcm.ir import Guard, Literal, OutcomeRef, PredicateRef
from mcm.statecase import StateCase

OLDER = "O"
YOUNGER = "Y"

EXECUTED_O = PredicateRef.of("Executed", load=OLDER)
SUCCEEDED_O = PredicateRef.of("Succeeded", load=OLDER)

KILL_Y = OutcomeRef.of("Kill", load=YOUNGER)
ALLOW_Y = OutcomeRef.of("Allow", load=YOUNGER)


def buggy_cases() -> list[StateCase]:
    """Hand-written state partition for the historical BOOM B1 behavior."""

    return [
        StateCase.build(
            name="older_not_executed",
            guard=Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=[KILL_Y],
            provenance=["Old logic kills younger only before older is executed/succeeded"],
        ),
        StateCase.build(
            name="older_executed_not_succeeded_bug_hole",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=[ALLOW_Y],
            provenance=[
                "Historical bug hole: older load executed but has not succeeded"
            ],
        ),
        StateCase.build(
            name="older_executed_and_succeeded",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, True),
            ),
            outcomes=[ALLOW_Y],
            provenance=["Normal completed older-load state"],
        ),
    ]


def fixed_cases() -> list[StateCase]:
    """Same reachable state partition after the ordering fix."""

    return [
        StateCase.build(
            name="older_not_executed_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=[KILL_Y],
            provenance=["Unresolved older load blocks/kills younger"],
        ),
        StateCase.build(
            name="older_executed_not_succeeded_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=[KILL_Y],
            provenance=["Fix closes executed-but-not-succeeded hole"],
        ),
        StateCase.build(
            name="older_executed_and_succeeded_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, True),
            ),
            outcomes=[ALLOW_Y],
            provenance=["Completed older load may allow younger"],
        ),
    ]
