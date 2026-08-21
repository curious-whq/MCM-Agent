# Run Summary — BoomNonBlockingDCache.dataReadArb

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.dataReadArb-8173fddc63391303`
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

- occurrences: 4
- predicates: 2
- identity keys: 0
- cases: 3
- candidate axioms: 15
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 15
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 15
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] Higher01Valid => !Input2Fire
- `A4` [FORMALLY_PROVED] io.chosen = 0 on Input0Fire
- `A5` [FORMALLY_PROVED] io.chosen = 1 on Input1Fire
- `A6` [FORMALLY_PROVED] io.chosen = 2 on Input2Fire
- `A7` [FORMALLY_PROVED] io.out.bits.req[0].addr = io.in[0].bits.req[0].addr on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[0].bits.req[0].way_en on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.valid[0] = io.in[0].bits.valid[0] on Input0Fire
- `A10` [FORMALLY_PROVED] io.out.bits.req[0].addr = io.in[1].bits.req[0].addr on Input1Fire
- `A11` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[1].bits.req[0].way_en on Input1Fire
- `A12` [FORMALLY_PROVED] io.out.bits.valid[0] = io.in[1].bits.valid[0] on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.req[0].addr = io.in[2].bits.req[0].addr on Input2Fire
- `A14` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[2].bits.req[0].way_en on Input2Fire
- `A15` [FORMALLY_PROVED] io.out.bits.valid[0] = io.in[2].bits.valid[0] on Input2Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
