import unittest

from examples.boom_b1 import (
    ALLOW_Y,
    EXECUTED_O,
    KILL_Y,
    SUCCEEDED_O,
    buggy_cases,
    fixed_cases,
)
from mcm.ir import Guard, Literal, OutcomeRef, PredicateRef
from mcm.statecase import StateCase, merge_state_cases


class BOOMB1StateCaseTests(unittest.TestCase):
    def _by_outcome(self, cases, outcome):
        return [case for case in cases if case.outcomes == (outcome,)]

    def test_buggy_state_partition_preserves_distinct_boundary_behavior(self):
        summaries = merge_state_cases(buggy_cases())

        allow = self._by_outcome(summaries, ALLOW_Y)
        kill = self._by_outcome(summaries, KILL_Y)

        self.assertEqual(len(allow), 1)
        self.assertEqual(
            allow[0].guard,
            Guard.of(Literal(EXECUTED_O, True)),
        )

        self.assertEqual(len(kill), 1)
        self.assertEqual(
            kill[0].guard,
            Guard.of(
                Literal(EXECUTED_O, False),
                Literal(SUCCEEDED_O, False),
            ),
        )

    def test_fixed_partition_merges_unresolved_states_into_not_succeeded(self):
        summaries = merge_state_cases(fixed_cases())

        kill = self._by_outcome(summaries, KILL_Y)
        allow = self._by_outcome(summaries, ALLOW_Y)

        self.assertEqual(len(kill), 1)
        self.assertEqual(
            kill[0].guard,
            Guard.of(Literal(SUCCEEDED_O, False)),
        )

        self.assertEqual(len(allow), 1)
        self.assertEqual(
            allow[0].guard,
            Guard.of(
                Literal(EXECUTED_O, True),
                Literal(SUCCEEDED_O, True),
            ),
        )

    def test_predicates_for_different_loads_do_not_merge(self):
        executed_p = PredicateRef.of("Executed", load="P")
        same_outcome = OutcomeRef.of("Allow", load="Y")

        cases = [
            StateCase.build(
                "older_o",
                Guard.of(Literal(EXECUTED_O, True)),
                [same_outcome],
            ),
            StateCase.build(
                "older_p",
                Guard.of(Literal(executed_p, False)),
                [same_outcome],
            ),
        ]

        summaries = merge_state_cases(cases)
        self.assertEqual(len(summaries), 2)


if __name__ == "__main__":
    unittest.main()
