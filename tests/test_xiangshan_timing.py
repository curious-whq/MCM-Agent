import unittest

from examples.xiangshan_metaarray import (
    META_READ,
    META_WRITE,
    RESP_OLD_META,
    RESP_WRITE_DATA,
    final_fix_cases,
    pre_final_fix_cases,
)
from mcm.ir import EventRef, Guard, OutcomeRef
from mcm.timing import (
    CycleDelta,
    DeltaDomain,
    Next,
    SameCycle,
    TimingCase,
    TimingCube,
    merge_timing_cases,
)


class XiangShanTimingTests(unittest.TestCase):
    def test_same_cycle_and_next_have_exact_cycle_meaning(self):
        same = SameCycle(META_WRITE, META_READ).to_domain()
        next_cycle = Next(META_WRITE, META_READ).to_domain()

        self.assertEqual(same.allowed, frozenset({0}))
        self.assertEqual(next_cycle.allowed, frozenset({1}))

    def test_pre_final_fix_preserves_same_cycle_corner_case(self):
        summaries = merge_timing_cases(pre_final_fix_cases())

        self.assertEqual(len(summaries), 2)

        by_outcome = {
            case.outcomes: case
            for case in summaries
        }

        same_cycle = by_outcome[(RESP_OLD_META,)].timing.domain_for(
            META_WRITE,
            META_READ,
        )
        previous_cycle = by_outcome[(RESP_WRITE_DATA,)].timing.domain_for(
            META_WRITE,
            META_READ,
        )

        self.assertEqual(same_cycle.allowed, frozenset({0}))
        self.assertEqual(previous_cycle.allowed, frozenset({1}))

    def test_final_fix_merges_equivalent_timing_cases_without_filling_gaps(self):
        summaries = merge_timing_cases(final_fix_cases())

        self.assertEqual(len(summaries), 1)
        summary = summaries[0]
        self.assertEqual(summary.outcomes, (RESP_WRITE_DATA,))

        domain = summary.timing.domain_for(META_WRITE, META_READ)
        self.assertEqual(domain.allowed, frozenset({0, 1}))

    def test_union_is_exact_not_interval_generalization(self):
        response = OutcomeRef.of("resp", value="write")
        a = EventRef.of("A")
        b = EventRef.of("B")

        cases = [
            TimingCase.build(
                "delta0",
                Guard.true(),
                TimingCube.of(CycleDelta(a, b, 0)),
                [response],
            ),
            TimingCase.build(
                "delta2",
                Guard.true(),
                TimingCube.of(CycleDelta(a, b, 2)),
                [response],
            ),
        ]

        summaries = merge_timing_cases(cases)
        self.assertEqual(len(summaries), 1)
        domain = summaries[0].timing.domain_for(a, b)

        self.assertEqual(domain.allowed, frozenset({0, 2}))
        self.assertNotIn(1, domain.allowed)

    def test_different_occurrences_do_not_merge(self):
        other_read = EventRef.of(
            "MetaRead",
            load="OtherLoad",
            line="A",
            way="W",
        )

        response = OutcomeRef.of("io.resp", value="write")
        cases = [
            TimingCase.build(
                "read_L",
                Guard.true(),
                TimingCube.of(SameCycle(META_WRITE, META_READ)),
                [response],
            ),
            TimingCase.build(
                "read_other",
                Guard.true(),
                TimingCube.of(SameCycle(META_WRITE, other_read)),
                [response],
            ),
        ]

        summaries = merge_timing_cases(cases)
        self.assertEqual(len(summaries), 2)


if __name__ == "__main__":
    unittest.main()
