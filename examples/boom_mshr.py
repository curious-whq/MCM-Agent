from mcm.conservation import ResourceInvariant
from mcm.ir import Before, Case, EventRef, Guard

R = "r"
M = "m"

REQ_ACCEPT = EventRef.of("ReqAccept", req=R, mshr=M)
RPQ_ENQ = EventRef.of("RPQEnq", req=R, mshr=M)
RESP_OUT = EventRef.of("RespOut", req=R, mshr=M)
REPLAY_OUT = EventRef.of("ReplayOut", req=R, mshr=M)
KILL = EventRef.of("Kill", req=R, mshr=M)
GRANT_ACK = EventRef.of("GrantAck", mshr=M)

BOUNDARY = {
    REQ_ACCEPT,
    RESP_OUT,
    REPLAY_OUT,
    KILL,
    GRANT_ACK,
}


def mshr_rpq_case() -> Case:
    return Case.build(
        name="mshr_rpq_request",
        guard=Guard.true(),
        facts=[
            Before(REQ_ACCEPT, RPQ_ENQ),
        ],
        provenance=[
            "BOOM MSHR/RPQ hand-written experiment",
            "ReqAccept(req=r,mshr=m) creates RPQEnq(req=r,mshr=m)",
        ],
    )


RPQ_CONSERVATION = ResourceInvariant.build(
    name="rpq_request_lifetime",
    resource="RPQ",
    enter=RPQ_ENQ,
    exits=(RESP_OUT, REPLAY_OUT, KILL),
    empty_at=(GRANT_ACK,),
    token_keys=("req", "mshr"),
    scope_keys=("mshr",),
    provenance=(
        "Accepted request token remains live until response/replay/kill",
        "GrantAck(mshr=m) requires the RPQ token to be gone",
    ),
)


def disconnected_mshr_case() -> Case:
    return Case.build(
        name="mshr_rpq_disconnected",
        guard=Guard.true(),
        facts=[],
        provenance=["Synthetic negative example"],
    )
