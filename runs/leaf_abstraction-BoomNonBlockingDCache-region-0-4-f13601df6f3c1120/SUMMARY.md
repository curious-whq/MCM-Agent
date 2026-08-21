# Run Summary — BoomNonBlockingDCache::region-0-4

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache-region-0-4-f13601df6f3c1120`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 1
- predicates: 3
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

- `A1` [FORMALLY_PROVED] MSHRResponsePending => !RequestAccept
- `A2` [FORMALLY_PROVED] MetaReadUnavailable => !RequestAccept
- `A3` [FORMALLY_PROVED] DataReadUnavailable => !RequestAccept

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
