import unittest

from examples.boom_mshr import (
    BOUNDARY,
    GRANT_ACK_M,
    KILL_R,
    M,
    REPLAY_R,
    REQ_ACCEPT_R,
    RESP_R,
    RPQ_CONSERVATION,
    RPQ_ENQ_R,
    disconnected_mshr_case,
    mshr_rpq_case,
    wrong_request_predecessor_case,
)
from mcm.conservation import OneOfBetween, ResourceInvariant, derive_resource_summaries
from mcm.ir import EventRef


class MSHRConservationTests(unittest.TestCase):
    def test_rpq_conservation_keeps_same_request_identity(self):
        summaries = derive_resource_summaries(
            mshr_rpq_case(),
            RPQ_CONSERVATION,
            BOUNDARY,
        )

        self.assertEqual(
            summaries,
            [
                OneOfBetween(
                    start=REQ_ACCEPT_R,
                    choices=(KILL_R, REPLAY_R, RESP_R),
                    end=GRANT_ACK_M,
                )
            ],
        )

    def test_no_boundary_predecessor_means_no_parent_summary(self):
        summaries = derive_resource_summaries(
            disconnected_mshr_case(),
            RPQ_CONSERVATION,
            BOUNDARY,
        )
        self.assertEqual(summaries, [])

    def test_other_request_cannot_ground_request_r(self):
        summaries = derive_resource_summaries(
            wrong_request_predecessor_case(),
            RPQ_CONSERVATION,
            BOUNDARY,
        )
        self.assertEqual(summaries, [])

    def test_other_request_cannot_be_an_exit_for_request_r(self):
        resp_s = EventRef.of("RespOut", req="s", mshr=M)
        with self.assertRaises(ValueError):
            ResourceInvariant.build(
                name="wrong_request_exit",
                resource="RPQ",
                enter=RPQ_ENQ_R,
                exits=(resp_s,),
                empty_at=(GRANT_ACK_M,),
                token_keys=("req",),
                scope_keys=("mshr",),
            )

    def test_v1_rejects_internal_exit_in_parent_summary(self):
        internal_exit = EventRef.of("InternalDequeue", req="r", mshr=M)
        bad = ResourceInvariant.build(
            name="bad_internal_exit",
            resource="RPQ",
            enter=RPQ_ENQ_R,
            exits=(internal_exit,),
            empty_at=(GRANT_ACK_M,),
            token_keys=("req",),
            scope_keys=("mshr",),
        )
        with self.assertRaises(ValueError):
            derive_resource_summaries(
                mshr_rpq_case(),
                bad,
                BOUNDARY,
            )


if __name__ == "__main__":
    unittest.main()
