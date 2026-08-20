# Run Summary — BoomMSHRFile.prefetcher

## Identity

- task: `leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.6`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 1
- predicates: 1
- identity keys: 0
- cases: 0
- candidate axioms: 2
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 2
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 2
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] bits(io.prefetch.valid, 0, 0) == 0
- `A2` [FORMALLY_PROVED] PrefetchDisabled => !PrefetchHandshake

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
