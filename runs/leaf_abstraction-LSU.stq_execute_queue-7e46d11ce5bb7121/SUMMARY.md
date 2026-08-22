# Run Summary — LSU.stq_execute_queue

## Identity

- task: `leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.12`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 3
- predicates: 2
- identity keys: 0
- cases: 2
- candidate axioms: 6
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 6
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 6
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] QueueFull => !EnqHandshake
- `A2` [FORMALLY_PROVED] QueueEmpty => !DeqHandshake
- `A3` [FORMALLY_PROVED] EnqHandshake <=> exactly_one_same_cycle({QueueInsert})
- `A4` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A5` [FORMALLY_PROVED] QueueInsert <mu DeqHandshake [same index slot]
- `A6` [FORMALLY_PROVED] io.deq.bits = io_deq_bits_MPORT on DeqHandshake

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
