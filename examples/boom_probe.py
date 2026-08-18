from mcm.ir import AliasMap, Before, Case, Guard, Literal

BOUNDARY = {
    "ProbeRecv",
    "ReleaseNotify",
    "ProbeAck",
    "ProbeAckData",
}

ALIASES = AliasMap(
    {
        "ProbeAck": "ProbeResponse",
        "ProbeAckData": "ProbeResponse",
    }
)


def clean_case() -> Case:
    return Case.build(
        name="clean_probe",
        guard=Guard.of(Literal("Dirty", positive=False)),
        facts=[
            Before("ProbeRecv", "ProbeUnit.s_lsu_release"),
            Before("ProbeUnit.s_lsu_release", "ReleaseNotify"),
            Before("ReleaseNotify", "ProbeUnit.s_release"),
            Before("ProbeUnit.s_release", "ProbeAck"),
        ],
        provenance=["BOOM ProbeUnit clean/non-dirty path"],
    )


def dirty_case() -> Case:
    return Case.build(
        name="dirty_probe",
        guard=Guard.of(Literal("Dirty", positive=True)),
        facts=[
            Before("ProbeRecv", "ProbeUnit.wb_req"),
            Before("ProbeUnit.wb_req", "Writeback.s_lsu_release"),
            Before("Writeback.s_lsu_release", "ReleaseNotify"),
            Before("ReleaseNotify", "Writeback.s_active"),
            Before("Writeback.s_active", "ProbeAckData"),
        ],
        provenance=["BOOM ProbeUnit -> WritebackUnit dirty path"],
    )


def buggy_dirty_case() -> Case:
    return Case.build(
        name="dirty_probe_buggy",
        guard=Guard.of(Literal("Dirty", positive=True)),
        facts=[
            Before("ProbeRecv", "ProbeUnit.wb_req"),
            Before("ProbeUnit.wb_req", "Writeback.s_active"),
            Before("Writeback.s_active", "ProbeAckData"),
            Before("ProbeAckData", "ReleaseNotify"),
        ],
        provenance=["Synthetic counterexample: response before LSU notification"],
    )
