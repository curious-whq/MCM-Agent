# Run Summary — LSU::state-0-11

## Identity

- task: `leaf_abstraction-LSU-state-0-11-90377a879c9e470d`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.14`
- schema: `umcm-formal-0.5`
- workflow status: `VALIDATION_INCOMPLETE`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
- candidate axioms: 1
- unresolved: 0

## Validation

- GROUNDED: 1
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 0
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 0
- formal backend: `explicit-control`

## Axioms

- `A1` [GROUNDED] next(stq_commit_head) = first_match(if _T_1151: 0; if commit_store: inc_mod_16(stq_commit_head); default: stq_commit_head)

## Next action

Review unresolved/partial structural obligations and then run a real formal backend.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
