# Run Summary — BoomNonBlockingDCache.wbArb

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.wbArb-351ef42d13b9ab57`
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

- occurrences: 3
- predicates: 1
- identity keys: 0
- cases: 2
- candidate axioms: 16
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 16
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 16
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] io.chosen = 0 on Input0Fire
- `A4` [FORMALLY_PROVED] io.out.bits.tag = io.in[0].bits.tag on Input0Fire
- `A5` [FORMALLY_PROVED] io.out.bits.idx = io.in[0].bits.idx on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.source = io.in[0].bits.source on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.param = io.in[0].bits.param on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.voluntary = io.in[0].bits.voluntary on Input0Fire
- `A10` [FORMALLY_PROVED] io.chosen = 1 on Input1Fire
- `A11` [FORMALLY_PROVED] io.out.bits.tag = io.in[1].bits.tag on Input1Fire
- `A12` [FORMALLY_PROVED] io.out.bits.idx = io.in[1].bits.idx on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.source = io.in[1].bits.source on Input1Fire
- `A14` [FORMALLY_PROVED] io.out.bits.param = io.in[1].bits.param on Input1Fire
- `A15` [FORMALLY_PROVED] io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire
- `A16` [FORMALLY_PROVED] io.out.bits.voluntary = io.in[1].bits.voluntary on Input1Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
