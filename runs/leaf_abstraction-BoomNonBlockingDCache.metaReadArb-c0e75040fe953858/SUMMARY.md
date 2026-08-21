# Run Summary — BoomNonBlockingDCache.metaReadArb

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.metaReadArb-c0e75040fe953858`
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

- occurrences: 7
- predicates: 5
- identity keys: 0
- cases: 6
- candidate axioms: 30
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 30
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 30
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire, Input3Fire, Input4Fire, Input5Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] Higher01Valid => !Input2Fire
- `A4` [FORMALLY_PROVED] Higher012Valid => !Input3Fire
- `A5` [FORMALLY_PROVED] Higher0123Valid => !Input4Fire
- `A6` [FORMALLY_PROVED] Higher01234Valid => !Input5Fire
- `A7` [FORMALLY_PROVED] io.chosen = 0 on Input0Fire
- `A8` [FORMALLY_PROVED] io.chosen = 1 on Input1Fire
- `A9` [FORMALLY_PROVED] io.chosen = 2 on Input2Fire
- `A10` [FORMALLY_PROVED] io.chosen = 3 on Input3Fire
- `A11` [FORMALLY_PROVED] io.chosen = 4 on Input4Fire
- `A12` [FORMALLY_PROVED] io.chosen = 5 on Input5Fire
- `A13` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[0].bits.req[0].idx on Input0Fire
- `A14` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[0].bits.req[0].tag on Input0Fire
- `A15` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[0].bits.req[0].way_en on Input0Fire
- `A16` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[1].bits.req[0].idx on Input1Fire
- `A17` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[1].bits.req[0].tag on Input1Fire
- `A18` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[1].bits.req[0].way_en on Input1Fire
- `A19` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[2].bits.req[0].idx on Input2Fire
- `A20` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[2].bits.req[0].tag on Input2Fire
- `A21` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[2].bits.req[0].way_en on Input2Fire
- `A22` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[3].bits.req[0].idx on Input3Fire
- `A23` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[3].bits.req[0].tag on Input3Fire
- `A24` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[3].bits.req[0].way_en on Input3Fire
- `A25` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[4].bits.req[0].idx on Input4Fire
- `A26` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[4].bits.req[0].tag on Input4Fire
- `A27` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[4].bits.req[0].way_en on Input4Fire
- `A28` [FORMALLY_PROVED] io.out.bits.req[0].idx = io.in[5].bits.req[0].idx on Input5Fire
- `A29` [FORMALLY_PROVED] io.out.bits.req[0].tag = io.in[5].bits.req[0].tag on Input5Fire
- `A30` [FORMALLY_PROVED] io.out.bits.req[0].way_en = io.in[5].bits.req[0].way_en on Input5Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
