# Run Summary — LSU::state-0-8

## Identity

- task: `leaf_abstraction-LSU-state-0-8-75c1d44ef5da10a6`
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

- occurrences: 5
- predicates: 5
- identity keys: 0
- cases: 4
- candidate axioms: 5
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 5
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 5
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] LoadSearch <=> exactly_one_same_cycle({LoadSearchPass, LoadSearchNonForwardable, LoadSearchConflictBlocked})
- `A2` [FORMALLY_PROVED] ForwardingKilled => !LoadSearchPass
- `A3` [FORMALLY_PROVED] ForwardingDisallowed => !LoadSearchPass
- `A4` [FORMALLY_PROVED] HasOlderAMOOrFence => !LoadSearchPass
- `A5` [FORMALLY_PROVED] NackOrderingConflict => !LoadSearchPass

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
