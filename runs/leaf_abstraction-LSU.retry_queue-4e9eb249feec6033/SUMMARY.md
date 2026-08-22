# Run Summary — LSU.retry_queue

## Identity

- task: `leaf_abstraction-LSU.retry_queue-4e9eb249feec6033`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.12`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 7
- predicates: 6
- identity keys: 0
- cases: 5
- candidate axioms: 12
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 12
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 12
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] QueueFull => !EnqHandshake
- `A2` [FORMALLY_PROVED] EnqHandshake <=> exactly_one_same_cycle({QueueInsert, BranchKilledEnqueue, FlushKilledEnqueue})
- `A3` [FORMALLY_PROVED] IncomingBranchKilled => !QueueInsert
- `A4` [FORMALLY_PROVED] IncomingFlushKilled => !QueueInsert
- `A5` [FORMALLY_PROVED] QueueEmpty => !HeadAdvance
- `A6` [FORMALLY_PROVED] HeadAdvance <=> exactly_one_same_cycle({DeqHandshake, InvalidHeadSkip})
- `A7` [FORMALLY_PROVED] HeadInvalid => !DeqHandshake
- `A8` [FORMALLY_PROVED] HeadValid => !InvalidHeadSkip
- `A9` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A10` [FORMALLY_PROVED] QueueInsert <mu DeqHandshake [same index slot]
- `A11` [FORMALLY_PROVED] QueueInsert <mu InvalidHeadSkip [same index slot]
- `A12` [FORMALLY_PROVED] io.deq.bits = out on DeqHandshake

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
