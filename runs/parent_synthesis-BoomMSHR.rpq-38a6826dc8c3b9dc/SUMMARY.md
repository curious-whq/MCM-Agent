# Run Summary — BoomMSHR.rpq

## Identity

- task: `parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc`
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

- occurrences: 3
- predicates: 3
- identity keys: 0
- cases: 5
- candidate axioms: 7
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 7
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 7
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] BoomMSHR.rpq.main::QueueFull => !ParentEnqHandshake
- `A2` [FORMALLY_PROVED] OutputInvalid => !ParentDeqHandshake
- `A3` [FORMALLY_PROVED] BufferCapture <mu ParentDeqHandshake
- `A4` [FORMALLY_PROVED] BoomMSHR.rpq.main::DeqHandshake <mu ParentDeqHandshake
- `A5` [FORMALLY_PROVED] BoomMSHR.rpq.main::QueueInsert <mu ParentDeqHandshake
- `A6` [FORMALLY_PROVED] TransferBranchKilled => !BufferCapture
- `A7` [FORMALLY_PROVED] TransferFlushKilled => !BufferCapture

## Certified provenance

- `A1` [lifted; trusted-child-lift] <- `BoomMSHR.rpq.main::A1`
- `A2` [parent_local; exact-combinational-exclusion] <- parent-local proof
- `A3` [parent_local; exact-scalar-valid-token-provenance] <- parent-local proof
- `A4` [parent_local; occurrence-bridge-history-composition] <- parent-local proof
- `A5` [emergent; trusted-history-transitivity] <- `BoomMSHR.rpq.main::A11`
- `A6` [parent_local; exact-combinational-exclusion] <- parent-local proof
- `A7` [parent_local; exact-combinational-exclusion] <- parent-local proof

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
