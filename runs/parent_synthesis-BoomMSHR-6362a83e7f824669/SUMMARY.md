# Run Summary — BoomMSHR

## Identity

- task: `parent_synthesis-BoomMSHR-6362a83e7f824669`
- kind: `parent_synthesis`
- workflow: `manual-first-workflow-0.9`
- prompt: `parent-synthesis-prompt-0.1`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 16
- predicates: 1
- identity keys: 0
- cases: 7
- candidate axioms: 15
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 15
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 15
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] PrimaryAccept <mu MemAcquire
- `A2` [FORMALLY_PROVED] MemAcquire <mu MemGrant
- `A3` [FORMALLY_PROVED] GrantComplete <mu RespHandshake
- `A4` [FORMALLY_PROVED] GrantComplete <mu MetaRead
- `A5` [FORMALLY_PROVED] MetaRead <mu MetaClearWrite <mu WBReq <mu WBComplete
- `A6` [FORMALLY_PROVED] MetaRead <mu CommitRefillBeat
- `A7` [FORMALLY_PROVED] CommitRefillDone => forall beat in [0, 8): count(CommitRefillBeat(beat)) = 1
- `A8` [FORMALLY_PROVED] RPQDrained <mu FinalMetaWrite
- `A9` [FORMALLY_PROVED] GrantComplete <mu MemFinish
- `A10` [FORMALLY_PROVED] GrantAckAbsent => !MemFinish
- `A11` [FORMALLY_PROVED] io.lb_write.bits.data = io.mem_grant.bits.data on GrantDataWrite
- `A12` [FORMALLY_PROVED] io.refill.bits.data = io.lb_resp on CommitRefillBeat
- `A13` [FORMALLY_PROVED] io.mem_finish.bits.sink = grantack.bits.sink on MemFinish
- `A14` [FORMALLY_PROVED] BoomMSHR.rpq.main::QueueInsert <mu RespHandshake
- `A15` [FORMALLY_PROVED] BoomMSHR.rpq.main::QueueInsert <mu ReplayHandshake

## Certified provenance

- `A1` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A10` [parent_local; exact-combinational-exclusion] <- parent-local proof
- `A11` [parent_local; exact-symbolic-driver-equality] <- parent-local proof
- `A12` [parent_local; exact-symbolic-driver-equality] <- parent-local proof
- `A13` [parent_local; exact-symbolic-driver-equality] <- parent-local proof
- `A14` [emergent; trusted-history-after-restriction] <- `BoomMSHR.rpq::A5`
- `A15` [emergent; trusted-history-after-restriction] <- `BoomMSHR.rpq::A5`
- `A2` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A3` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A4` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A5` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A6` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A7` [parent_local; exact-bounded-indexed-occurrence] <- parent-local proof
- `A8` [parent_local; exhaustive-state-reachability] <- parent-local proof
- `A9` [parent_local; exhaustive-state-reachability] <- parent-local proof

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
