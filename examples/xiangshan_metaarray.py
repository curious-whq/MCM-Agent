from mcm.ir import EventRef, Guard, OutcomeRef
from mcm.timing import CycleDelta, Next, SameCycle, TimingCase, TimingCube

LOAD = "L"
PROBE = "P"
LINE = "A"
WAY = "W"

META_WRITE = EventRef.of(
    "MetaWrite",
    probe=PROBE,
    line=LINE,
    way=WAY,
)
META_READ = EventRef.of(
    "MetaRead",
    load=LOAD,
    line=LINE,
    way=WAY,
)
META_RESP = EventRef.of(
    "MetaResp",
    load=LOAD,
    line=LINE,
    way=WAY,
)
RAR_RELEASE = EventRef.of(
    "RARRelease",
    probe=PROBE,
    line=LINE,
)
RAR_ALLOC = EventRef.of(
    "RARAlloc",
    load=LOAD,
    line=LINE,
)

# Track the physical MetaArray output value, not a synthetic "safe/unsafe" event.
RESP_WRITE_DATA = OutcomeRef.of(
    "io.resp",
    load=LOAD,
    line=LINE,
    way=WAY,
    value="MetaWrite(P)",
)
RESP_OLD_META = OutcomeRef.of(
    "io.resp",
    load=LOAD,
    line=LINE,
    way=WAY,
    value="OldMeta(A,W)",
)


def _timing(write_to_read) -> TimingCube:
    """Common schedule described by the XiangShan bug report.

    The bug report states:
      * Probe meta write at s0.
      * RAR release one cycle after the probe meta write.
      * Load s0 reads meta.
      * Load enters RAR at s2, two cycles after the s0 read.

    `write_to_read` selects whether the write is in the previous cycle (s1
    bypass can see it) or in the same cycle (the historical missing s0 bypass).
    """

    return TimingCube.of(
        write_to_read,
        Next(META_WRITE, RAR_RELEASE),
        CycleDelta(META_READ, RAR_ALLOC, 2),
        Next(META_READ, META_RESP),
    )


def pre_final_fix_cases() -> list[TimingCase]:
    """Behavior after 479d... but before the final 6318... s0-bypass fix."""

    return [
        TimingCase.build(
            name="previous_cycle_write_hits_s1_bypass",
            guard=Guard.true(),
            timing=_timing(Next(META_WRITE, META_READ)),
            outcomes=[RESP_WRITE_DATA],
            provenance=[
                "Commit 479d enables bypassRead",
                "Existing logic checks s1_way_wen/s1_way_waddr/s1_way_wdata",
            ],
        ),
        TimingCase.build(
            name="same_cycle_write_misses_s0_bypass",
            guard=Guard.true(),
            timing=_timing(SameCycle(META_WRITE, META_READ)),
            outcomes=[RESP_OLD_META],
            provenance=[
                "479d commit message: simultaneous probe meta write and load s0 "
                "read obtains old data without s0 bypass"
            ],
        ),
    ]


def final_fix_cases() -> list[TimingCase]:
    """Behavior after 6318... adds s0 write address/data bypass."""

    return [
        TimingCase.build(
            name="previous_cycle_write_hits_s1_bypass_fixed",
            guard=Guard.true(),
            timing=_timing(Next(META_WRITE, META_READ)),
            outcomes=[RESP_WRITE_DATA],
            provenance=[
                "s1 bypass remains supported"
            ],
        ),
        TimingCase.build(
            name="same_cycle_write_hits_s0_bypass_fixed",
            guard=Guard.true(),
            timing=_timing(SameCycle(META_WRITE, META_READ)),
            outcomes=[RESP_WRITE_DATA],
            provenance=[
                "Commit 6318 adds s0_way_waddr/s0_way_wdata and checks "
                "s0_way_wen against the current read index"
            ],
        ),
    ]
