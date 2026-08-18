from mcm.conservation import ResourceInvariant
from mcm.ir import Before, Case, EventRef, Guard

BOUNDARY = {
    "ReqAccept",
    "RespOut",
    "ReplayOut",
    "Kill",
    "GrantAck",
}

# Symbolic identities used by this hand-written experiment.
R = "r"
M = "m"

REQ_ACCEPT_R = EventRef.of("ReqAccept", req=R, mshr=M)
RPQ_ENQ_R = EventRef.of("RPQEnq", req=R, mshr=M)
RESP_R = EventRef.of("RespOut", req=R, mshr=M)
REPLAY_R = EventRef.of("ReplayOut", req=R, mshr=M)
KILL_R = EventRef.of("Kill", req=R, mshr=M)
GRANT_ACK_M = EventRef.of("GrantAck", mshr=M)


def mshr_rpq_case() -> Case:
    """One symbolic request r admitted into RPQ of MSHR m."""

    return Case.build(
        name="mshr_rpq_request",
        guard=Guard.true(),
        facts=[Before(REQ_ACCEPT_R, RPQ_ENQ_R)],
        provenance=[
            "BOOM MSHR/RPQ hand-written experiment",
            "ReqAccept(r,m) creates RPQ token (r,m)",
        ],
    )


RPQ_CONSERVATION = ResourceInvariant.build(
    name="rpq_request_lifetime",
    resource="RPQ",
    enter=RPQ_ENQ_R,
    exits=(RESP_R, REPLAY_R, KILL_R),
    empty_at=(GRANT_ACK_M,),
    token_keys=("req",),
    scope_keys=("mshr",),
    provenance=(
        "An accepted RPQ request remains live until response/replay/kill",
        "GrantAck(m) is emitted only after request r has left RPQ(m)",
    ),
)


def disconnected_mshr_case() -> Case:
    """Negative example: no boundary event is linked to RPQEnq(r,m)."""

    return Case.build(
        name="mshr_rpq_disconnected",
        guard=Guard.true(),
        facts=[],
        provenance=["Synthetic negative example"],
    )


def wrong_request_predecessor_case() -> Case:
    """Negative example: request s cannot ground the token for request r."""

    req_accept_s = EventRef.of("ReqAccept", req="s", mshr=M)
    return Case.build(
        name="mshr_rpq_wrong_request",
        guard=Guard.true(),
        facts=[Before(req_accept_s, RPQ_ENQ_R)],
        provenance=["Synthetic identity-mismatch example"],
    )
