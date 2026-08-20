# Run Summary — BoomMSHRFile

## Identity

- task: `parent_synthesis-BoomMSHRFile-9485e49ea1c75380`
- kind: `parent_synthesis`
- workflow: `manual-first-workflow-0.9`
- prompt: `parent-synthesis-prompt-0.2`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 14
- predicates: 0
- identity keys: 0
- cases: 5
- candidate axioms: 25
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 25
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 25
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] RequestAccept <=> exactly_one_same_cycle({PrimaryMSHRAccept, SecondaryMSHRAccept, MMIOAccept})
- `A2` [FORMALLY_PROVED] MMIOAccept <=> exactly_one_same_cycle({BoomMSHRFile.mmios_0::ReqAccept})
- `A3` [FORMALLY_PROVED] MemAcquire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::MemAcquire, BoomMSHRFile.mshrs_1::MemAcquire, BoomMSHRFile.mmios_0::MemAccess})
- `A4` [FORMALLY_PROVED] MemGrant <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::MemGrant, BoomMSHRFile.mshrs_1::MemGrant, MMIOGrantDelivery})
- `A5` [FORMALLY_PROVED] MemFinish <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::MemFinish, BoomMSHRFile.mshrs_1::MemFinish})
- `A6` [FORMALLY_PROVED] MetaRead <=> exactly_one_same_cycle({BoomMSHRFile.meta_read_arb::OutputFire})
- `A7` [FORMALLY_PROVED] BoomMSHRFile.meta_read_arb::Input0Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::MetaRead})
- `A8` [FORMALLY_PROVED] BoomMSHRFile.meta_read_arb::Input1Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_1::MetaRead})
- `A9` [FORMALLY_PROVED] MetaWrite <=> exactly_one_same_cycle({BoomMSHRFile.meta_write_arb::OutputFire})
- `A10` [FORMALLY_PROVED] WBReq <=> exactly_one_same_cycle({BoomMSHRFile.wb_req_arb::OutputFire})
- `A11` [FORMALLY_PROVED] BoomMSHRFile.wb_req_arb::Input0Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::WBReq})
- `A12` [FORMALLY_PROVED] BoomMSHRFile.wb_req_arb::Input1Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_1::WBReq})
- `A13` [FORMALLY_PROVED] Refill <=> exactly_one_same_cycle({BoomMSHRFile.refill_arb::OutputFire})
- `A14` [FORMALLY_PROVED] BoomMSHRFile.refill_arb::Input0Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::CommitRefillBeat})
- `A15` [FORMALLY_PROVED] BoomMSHRFile.refill_arb::Input1Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_1::CommitRefillBeat})
- `A16` [FORMALLY_PROVED] Replay <=> exactly_one_same_cycle({BoomMSHRFile.replay_arb::OutputFire})
- `A17` [FORMALLY_PROVED] BoomMSHRFile.replay_arb::Input0Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::ReplayHandshake})
- `A18` [FORMALLY_PROVED] BoomMSHRFile.replay_arb::Input1Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_1::ReplayHandshake})
- `A19` [FORMALLY_PROVED] BoomMSHRFile.resp_arb::Input0Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_0::RespHandshake})
- `A20` [FORMALLY_PROVED] BoomMSHRFile.resp_arb::Input1Fire <=> exactly_one_same_cycle({BoomMSHRFile.mshrs_1::RespHandshake})
- `A21` [FORMALLY_PROVED] BoomMSHRFile.resp_arb::Input2Fire <=> exactly_one_same_cycle({BoomMSHRFile.mmios_0::RespHandshake})
- `A22` [FORMALLY_PROVED] BoomMSHRFile.respq::EnqHandshake <=> exactly_one_same_cycle({BoomMSHRFile.resp_arb::OutputFire})
- `A23` [FORMALLY_PROVED] RespHandshake <=> exactly_one_same_cycle({BoomMSHRFile.respq::DeqHandshake})
- `A24` [FORMALLY_PROVED] BoomMSHRFile.respq::QueueInsert <mu RespHandshake
- `A25` [FORMALLY_PROVED] bits(io.prefetch.valid, 0, 0) == 0

## Certified provenance

- `A1` [parent_local; exact-same-cycle-occurrence-partition] <- parent-local proof
- `A10` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A11` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A12` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A13` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A14` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A15` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A16` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A17` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A18` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A19` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A2` [emergent; exact-parent-child-occurrence-partition] <- `BoomMSHRFile.mmio_alloc_arb::A3`, `BoomMSHRFile.mmio_alloc_arb::A4`
- `A20` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A21` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A22` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A23` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A24` [emergent; trusted-history-after-restriction] <- `BoomMSHRFile.respq::A9`
- `A25` [lifted; trusted-child-value-lift] <- `BoomMSHRFile.prefetcher::A1`
- `A3` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A4` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A5` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A6` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A7` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A8` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A9` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
