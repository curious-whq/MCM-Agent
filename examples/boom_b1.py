from mcm.ir import Guard, Literal, OutcomeRef, PredicateRef
from mcm.statecase import StateCase

OLDER = "O"
YOUNGER = "Y"

EXECUTED_O = PredicateRef.of("Executed", load=OLDER)
SUCCEEDED_O = PredicateRef.of("Succeeded", load=OLDER)
WILL_SUCCEED_O = PredicateRef.of("WillSucceed", load=OLDER)

# These are grounded in the body of the BOOM LSU kill branch.
# We intentionally do not model io.dmem.s1_kill here because that assignment has
# an additional runtime guard and is not guaranteed every time this branch fires.
CLEAR_EXECUTE_Y = OutcomeRef.of(
    "s1_set_execute",
    load=YOUNGER,
    value="false",
)
KILL_FORWARD_Y = OutcomeRef.of(
    "kill_forward",
    load=YOUNGER,
    value="true",
)
BLOCK_YOUNGER_EFFECTS = (CLEAR_EXECUTE_Y, KILL_FORWARD_Y)


def buggy_cases() -> list[StateCase]:
    """Minimal reachable partition for the old BOOM condition.

    Old branch condition:
        !(Executed(O) || Succeeded(O))

    The empty outcome set means this particular branch contributes none of the
    tracked blocking assignments. It does not mean a free-standing architectural
    "Allow" event exists.
    """

    return [
        StateCase.build(
            name="older_not_executed",
            guard=Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=BLOCK_YOUNGER_EFFECTS,
            provenance=[
                "Old BOOM branch: !(l_executed || l_succeeded)",
                "Tracked effects: s1_set_execute := false, kill_forward := true",
            ],
        ),
        StateCase.build(
            name="older_executed_not_succeeded_bug_hole",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, False),
            ),
            outcomes=[],
            provenance=[
                "Historical hole: executed older load has not succeeded, "
                "so the old kill branch does not fire"
            ],
        ),
        StateCase.build(
            name="older_executed_and_succeeded",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, True),
            ),
            outcomes=[],
            provenance=[
                "Completed older load also does not take the tracked kill branch"
            ],
        ),
    ]


def fixed_cases() -> list[StateCase]:
    """Reachable partition for the final BOOM PR #706 condition.

    Final branch condition:
        !(Executed(O) && (Succeeded(O) || WillSucceed(O)))

    `ldq_will_succeed` defaults from `ldq_succeeded`, so the hand-written
    reachable partition models Succeeded(O) => WillSucceed(O).
    """

    return [
        StateCase.build(
            name="older_not_executed_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
                Literal(WILL_SUCCEED_O, False),
            ),
            outcomes=BLOCK_YOUNGER_EFFECTS,
            provenance=[
                "Final BOOM condition blocks while the older load is unresolved"
            ],
        ),
        StateCase.build(
            name="older_executed_not_succeeded_not_will_succeed_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, False),
                Literal(WILL_SUCCEED_O, False),
            ),
            outcomes=BLOCK_YOUNGER_EFFECTS,
            provenance=[
                "Final fix closes the executed-but-not-succeeded hole"
            ],
        ),
        StateCase.build(
            name="older_executed_will_succeed_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, False),
                Literal(WILL_SUCCEED_O, True),
            ),
            outcomes=[],
            provenance=[
                "WillSucceed permits the current/next-cycle successful load path"
            ],
        ),
        StateCase.build(
            name="older_executed_and_succeeded_fixed",
            guard=Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, True),
                Literal(WILL_SUCCEED_O, True),
            ),
            outcomes=[],
            provenance=[
                "Succeeded implies WillSucceed in this hand-written reachable model"
            ],
        ),
    ]
