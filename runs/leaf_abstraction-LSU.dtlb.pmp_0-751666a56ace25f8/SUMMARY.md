# Run Summary — LSU.dtlb.pmp_0

## Identity

- task: `leaf_abstraction-LSU.dtlb.pmp_0-751666a56ace25f8`
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

- occurrences: 1
- predicates: 6
- identity keys: 0
- cases: 0
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

- `A1` [FORMALLY_PROVED] io.r = default on NoPMPEntryMatches
- `A2` [FORMALLY_PROVED] io.w = default on NoPMPEntryMatches
- `A3` [FORMALLY_PROVED] io.x = default on NoPMPEntryMatches

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
