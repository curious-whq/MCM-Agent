import unittest

from examples.boom_mshr import (
    BOUNDARY,
    GRANT_ACK,
    KILL,
    M,
    REPLAY_OUT,
    REQ_ACCEPT,
    RESP_OUT,
    RPQ_CONSERVATION,
    RPQ_ENQ,
    disconnected_mshr_case,
    mshr_rpq_case,
)
from mcm.conservation import OneOfBetween, ResourceInvariant, derive_resource_summaries
from mcm.ir import Before, Case, EventRef, Guard


class MSHRConservationTests(unittest.TestCase):
    def test_rpq_conservation_projects_same_request_lifecycle(self):
        summaries = derive_resource_summaries(
            mshr_rpq_case(),
            RPQ_CONSERVATION,
            BOUNDARY,
        )

        self.assertEqual(
            summaries,
            [
                OneOfBetween(
                    start=REQ_ACCEPT,
                    choices=tuple(sorted((KILL, REPLAY_OUT, RESP_OUT))),
                    end=GRANT_ACK,
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

    def test_wrong_request_predecessor_is_not_used(self):
        wrong_req = EventRef.of("ReqAccept", req="s", mshr=M)
        case = Case.build(
            name="wrong_request",
            guard=Guard.true(),
            facts=[Before(wrong_req, RPQ_ENQ)],
        )
        summaries = derive_resource_summaries(
            case,
            RPQ_CONSERVATION,
            BOUNDARY | {wrong_req},
        )
        self.assertEqual(summaries, [])

    def test_wrong_request_exit_is_rejected(self):
        wrong_exit = EventRef.of("RespOut", req="s", mshr=M)
        with self.assertRaises(ValueError):
            ResourceInvariant.build(
                name="wrong_exit",
                resource="RPQ",
                enter=RPQ_ENQ,
                exits=(wrong_exit,),
                empty_at=(GRANT_ACK,),
                token_keys=("req", "mshr"),
                scope_keys=("mshr",),
            )

    def test_internal_exit_is_rejected_by_boundary_projection(self):
        internal_exit = EventRef.of("InternalDequeue", req="r", mshr=M)
        invariant = ResourceInvariant.build(
            name="internal_exit",
            resource="RPQ",
            enter=RPQ_ENQ,
            exits=(internal_exit,),
            empty_at=(GRANT_ACK,),
            token_keys=("req", "mshr"),
            scope_keys=("mshr",),
        )
        with self.assertRaises(ValueError):
            derive_resource_summaries(
                mshr_rpq_case(),
                invariant,
                BOUNDARY,
            )


if __name__ == "__main__":
    unittest.main()
