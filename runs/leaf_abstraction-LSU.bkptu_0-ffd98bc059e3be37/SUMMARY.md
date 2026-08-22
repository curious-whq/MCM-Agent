# Run Summary — LSU.bkptu_0

## Identity

- task: `leaf_abstraction-LSU.bkptu_0-ffd98bc059e3be37`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.14`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
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

- `A1` [FORMALLY_PROVED] bits(io.xcpt_if, 0, 0) == 0
- `A2` [FORMALLY_PROVED] bits(io.xcpt_ld, 0, 0) == 0
- `A3` [FORMALLY_PROVED] bits(io.xcpt_st, 0, 0) == 0
- `A4` [FORMALLY_PROVED] bits(io.debug_if, 0, 0) == 0
- `A5` [FORMALLY_PROVED] bits(io.debug_ld, 0, 0) == 0
- `A6` [FORMALLY_PROVED] bits(io.debug_st, 0, 0) == 0

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
