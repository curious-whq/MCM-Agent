# BoomProbeUnit µMCM v0.2 experiment

The first manual-first semantic experiment used the real BOOM `BoomProbeUnit`
from `SmallBoomV4Config`. The WorkUnit contains 209 raw FIRRTL statements, 132
logical statements, 97 mapped source lines, four registers and seven physical
boundary events.

The conversation-driven candidate compressed the implementation to:

- six boundary occurrences: `ProbeReq`, `MetaRead`, `LSURelease`, `ProbeAck`,
  `WBReq`, `MetaWrite`;
- one derived occurrence: `WBComplete`;
- four persistent predicates: `ActiveProbe`, `TagMatch`,
  `DirtyResponseNeeded`, `BlocksMSHRWriteback`;
- one latched transaction identity (`req`);
- three semantic paths: no-match, matched-clean, matched-dirty;
- eight candidate axioms.

The eight current obligations are:

1. active Probe transactions are single-flight;
2. the latched request is the identity carrier for listed response/request fields;
3. the dirty writeback path excludes the local release/ProbeAck path;
4. `LSURelease < ProbeAck`;
5. release path: `LSURelease < ProbeAck < MetaWrite` when the metadata update occurs;
6. dirty path: `WBReq < WBComplete < MetaWrite`;
7. `MetaWrite` writes the computed `new_coh` state;
8. the local ProbeAck has TileLink-C opcode bit 0 equal to zero (no data).

`semantic-validator-0.2` reports all eight encoded obligations as
`STRUCTURALLY_SUPPORTED` on the real ProbeUnit handoff. This is deterministic
evidence from the finite-control/static model, **not** a bit-level proof of the
concrete RTL. With the bundled `none` formal backend, zero axioms are placed in
`trusted_umcm.json`. A real RTL formal backend is required before an axiom can be
`FORMALLY_PROVED`; the full TileLink `onProbe` truth-table equivalence additionally
requires reference-spec semantics before it can be `SPEC_PROVED`.

This experiment is why schema v0.2 separates persistent predicates from
occurrences and allows a strictly RTL-grounded internal milestone such as
`WBComplete`.
