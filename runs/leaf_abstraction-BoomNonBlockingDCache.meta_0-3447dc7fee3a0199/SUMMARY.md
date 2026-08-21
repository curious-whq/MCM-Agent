# Run Summary — BoomNonBlockingDCache.meta_0

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.meta_0-3447dc7fee3a0199`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.10`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 2
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

- `A1` [FORMALLY_PROVED] tag_array[way] latest-write storage flow with explicit initialization; MetaRF=rf, MetaCO=co, MetaFR=rf^-1;co
- `A2` [FORMALLY_PROVED] ResetActive => !ReadRequest
- `A3` [FORMALLY_PROVED] ResetActive => !MetadataWrite
- `A4` [FORMALLY_PROVED] WriteRequested => !ReadRequest

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
