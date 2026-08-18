import itertools
import unittest

from examples.boom_b1 import (
    BLOCK_YOUNGER_EFFECTS,
    EXECUTED_O,
    SUCCEEDED_O,
    WILL_SUCCEED_O,
    buggy_cases,
    fixed_cases,
)
from mcm.ir import Guard, Literal, OutcomeRef, PredicateRef
from mcm.statecase import StateCase, merge_state_cases


def _guard_matches(guard: Guard, assignment: dict[PredicateRef, bool]) -> bool:
    return all(
        assignment[literal.predicate] == literal.positive
        for literal in guard.literals
    )


def _outcomes_for(cases: list[StateCase], assignment: dict[PredicateRef, bool]):
    return {
        case.outcomes
        for case in cases
        if _guard_matches(case.guard, assignment)
    }


class BOOMB1StateCaseTests(unittest.TestCase):
    def _by_outcomes(self, cases, outcomes):
        outcomes = tuple(sorted(outcomes))
        return [case for case in cases if case.outcomes == outcomes]

    def test_buggy_partition_keeps_executed_hole_as_no_blocking_effect(self):
        summaries = merge_state_cases(buggy_cases())

        no_block = self._by_outcomes(summaries, ())
        blocked = self._by_outcomes(summaries, BLOCK_YOUNGER_EFFECTS)

        self.assertEqual(len(no_block), 1)
        self.assertEqual(
            no_block[0].guard,
            Guard.of(Literal(EXECUTED_O, True)),
        )

        self.assertEqual(len(blocked), 1)
        self.assertEqual(
            blocked[0].guard,
            Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
            ),
        )

    def test_fixed_partition_uses_will_succeed(self):
        summaries = merge_state_cases(fixed_cases())

        blocked = self._by_outcomes(summaries, BLOCK_YOUNGER_EFFECTS)
        no_block = self._by_outcomes(summaries, ())

        self.assertEqual(len(blocked), 1)
        self.assertEqual(
            blocked[0].guard,
            Guard.of(
                Literal(SUCCEEDED_O, False),
                Literal(WILL_SUCCEED_O, False),
            ),
        )

        self.assertEqual(len(no_block), 1)
        self.assertEqual(
            no_block[0].guard,
            Guard.of(
                Literal(EXECUTED_O, True),
                Literal(WILL_SUCCEED_O, True),
            ),
        )

    def test_predicates_for_different_loads_do_not_merge(self):
        executed_p = PredicateRef.of("Executed", load="P")
        effect = OutcomeRef.of("kill_forward", load="Y", value="true")

        cases = [
            StateCase.build(
                "older_o",
                Guard.of(Literal(EXECUTED_O, True)),
                [effect],
            ),
            StateCase.build(
                "older_p",
                Guard.of(Literal(executed_p, False)),
                [effect],
            ),
        ]

        summaries = merge_state_cases(cases)
        self.assertEqual(len(summaries), 2)

    def test_guard_minimizer_preserves_truth_table_for_all_three_var_functions(self):
        """Exhaustively check all 2^(2^3) Boolean truth tables.

        Each minterm is mapped either to one concrete effect or to the empty
        tracked-effect set. After minimization, every one of the 8 assignments
        must still map to exactly the same consequence.
        """

        predicates = [
            PredicateRef.of("A"),
            PredicateRef.of("B"),
            PredicateRef.of("C"),
        ]
        effect = OutcomeRef.of("effect", value="true")

        assignments = [
            dict(zip(predicates, values))
            for values in itertools.product((False, True), repeat=3)
        ]

        for truth_table in range(1 << len(assignments)):
            original: list[StateCase] = []

            for index, assignment in enumerate(assignments):
                guard = Guard.of(
                    *[
                        Literal(predicate, assignment[predicate])
                        for predicate in predicates
                    ]
                )
                outcomes = [effect] if (truth_table >> index) & 1 else []
                original.append(
                    StateCase.build(
                        name=f"minterm_{index}",
                        guard=guard,
                        outcomes=outcomes,
                    )
                )

            minimized = merge_state_cases(original)

            for assignment in assignments:
                self.assertEqual(
                    _outcomes_for(original, assignment),
                    _outcomes_for(minimized, assignment),
                    msg=(
                        f"truth_table={truth_table:08b}, "
                        f"assignment={assignment}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
