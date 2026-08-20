# Run Summary — BoomMSHR.rpq.main

## Identity

- task: `leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.6`
- schema: `umcm-formal-0.5`
- workflow status: `PARTIALLY_FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 4
- predicates: 6
- identity keys: 0
- cases: 5
- candidate axioms: 10
- unresolved: 0

## Validation

- GROUNDED: 9
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 1
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 1
- formal backend: `explicit-control`

## Axioms

- `A1` [GROUNDED] QueueFull => !EnqHandshake
- `A2` [GROUNDED] IncomingBranchKilled => !QueueInsert
- `A3` [GROUNDED] IncomingFlushKilled => !QueueInsert
- `A4` [GROUNDED] QueueEmpty => !DeqHandshake
- `A5` [GROUNDED] HeadInvalid => !DeqHandshake
- `A6` [GROUNDED] QueueEmpty => !InvalidHeadSkip
- `A7` [GROUNDED] HeadValid => !InvalidHeadSkip
- `A8` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A9` [GROUNDED] out = out_MPORT on DeqHandshake
- `A11` [GROUNDED] QueueInsert <mu DeqHandshake [same index slot]

## Next action

Freeze only the proved axioms already present in trusted_umcm.json; keep the remaining candidate axioms outside the trusted abstraction until a stronger backend proves them.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
