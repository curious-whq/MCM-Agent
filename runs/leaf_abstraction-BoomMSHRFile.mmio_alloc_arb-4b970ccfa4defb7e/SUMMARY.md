# Run Summary — BoomMSHRFile.mmio_alloc_arb

## Identity

- task: `leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.8`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 2
- predicates: 0
- identity keys: 0
- cases: 1
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

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({InputFire})
- `A2` [FORMALLY_PROVED] io.out.bits = io.in[0].bits on InputFire
- `A3` [FORMALLY_PROVED] io.out.valid = io.in[0].valid
- `A4` [FORMALLY_PROVED] io.in[0].ready = io.out.ready

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
