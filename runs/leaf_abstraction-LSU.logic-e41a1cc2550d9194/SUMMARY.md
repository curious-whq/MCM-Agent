# Run Summary — LSU.logic

## Identity

- task: `leaf_abstraction-LSU.logic-e41a1cc2550d9194`
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

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
- candidate axioms: 1
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 1
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 1
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] after 1 cycle(s), {io.found, io.found_idx} = select_cyclic_predecessor(io.youngest), pivot=last(bits(io.matches, i, i), i in [0, 8))

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
