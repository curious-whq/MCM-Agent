# Run Summary — LSU::state-0-10

## Identity

- task: `leaf_abstraction-LSU-state-0-10-75fa875f7278b61a`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.13`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 1
- predicates: 4
- identity keys: 0
- cases: 1
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

- `A1` [FORMALLY_PROVED] after 1 cycle(s), bits(stq_clr_head_idx, 2, 0) = select_cyclic_successor(stq_clr_head_idx_head_base), pivot=first(index_cases(i; _stq_clr_head_idx_T_1, _stq_clr_head_idx_T_3, _stq_clr_head_idx_T_5, _stq_clr_head_idx_T_7…
- `A2` [FORMALLY_PROVED] ClearGateClosed => !StoreClear
- `A3` [FORMALLY_PROVED] SelectedIsAMO => !StoreClear
- `A4` [FORMALLY_PROVED] SelectedAlreadyCleared => !StoreClear
- `A5` [FORMALLY_PROVED] SelectedControlBlocked => !StoreClear

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
