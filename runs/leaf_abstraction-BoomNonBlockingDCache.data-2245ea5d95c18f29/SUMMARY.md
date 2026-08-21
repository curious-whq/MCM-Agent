# Run Summary — BoomNonBlockingDCache.data

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29`
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

- occurrences: 6
- predicates: 0
- identity keys: 0
- cases: 5
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

- `A1` [FORMALLY_PROVED] array_0_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay0RF=rf, DataWay0CO=co, DataWay0FR=rf^-1;co
- `A2` [FORMALLY_PROVED] array_1_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay1RF=rf, DataWay1CO=co, DataWay1FR=rf^-1;co
- `A3` [FORMALLY_PROVED] array_2_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay2RF=rf, DataWay2CO=co, DataWay2FR=rf^-1;co
- `A4` [FORMALLY_PROVED] array_3_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay3RF=rf, DataWay3CO=co, DataWay3FR=rf^-1;co
- `A5` [FORMALLY_PROVED] bits(io.s1_nacks[0], 0, 0) == 0

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
