# Run Summary — LSU::region-0-0

## Identity

- task: `leaf_abstraction-LSU-region-0-0-95a6c27af3e9b19f`
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

- occurrences: 1
- predicates: 2
- identity keys: 0
- cases: 1
- candidate axioms: 3
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 3
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 3
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] NoRegisteredClear => !ClearBusy
- `A2` [FORMALLY_PROVED] OutputControlBlocked => !ClearBusy
- `A3` [FORMALLY_PROVED] io.core.clr_bsy[0].bits = clr_uop_1.rob_idx on ClearBusy

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
