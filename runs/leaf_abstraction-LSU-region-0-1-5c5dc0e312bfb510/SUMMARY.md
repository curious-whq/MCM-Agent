# Run Summary — LSU::region-0-1

## Identity

- task: `leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 4
- predicates: 2
- identity keys: 0
- cases: 2
- candidate axioms: 4
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 4
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 4
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] ClearUnsafe <=> exactly_one_same_cycle({ClearUnsafeWithStorePending, ClearUnsafeLoadOnly})
- `A2` [FORMALLY_PROVED] DelayedFailedLoad => !ClearUnsafe
- `A3` [FORMALLY_PROVED] DCacheNack => !ClearUnsafeLoadOnly
- `A4` [FORMALLY_PROVED] io.core.clr_unsafe[0].bits = io_core_clr_unsafe_0_bits_REG on ClearUnsafe

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
