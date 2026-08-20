# Run Summary — BoomMSHRFile.respq

## Identity

- task: `leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.9`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 4
- predicates: 6
- identity keys: 0
- cases: 5
- candidate axioms: 9
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 9
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 9
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] QueueFull => !EnqHandshake
- `A2` [FORMALLY_PROVED] IncomingBranchKilled => !QueueInsert
- `A3` [FORMALLY_PROVED] IncomingFlushKilled => !QueueInsert
- `A4` [FORMALLY_PROVED] QueueEmpty => !DeqHandshake
- `A5` [FORMALLY_PROVED] HeadInvalid => !DeqHandshake
- `A6` [FORMALLY_PROVED] QueueEmpty => !InvalidHeadSkip
- `A7` [FORMALLY_PROVED] HeadValid => !InvalidHeadSkip
- `A8` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A9` [FORMALLY_PROVED] QueueInsert <mu DeqHandshake [same index slot]

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
