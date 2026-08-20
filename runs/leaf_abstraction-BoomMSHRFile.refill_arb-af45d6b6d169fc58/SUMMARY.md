# Run Summary — BoomMSHRFile.refill_arb

## Identity

- task: `leaf_abstraction-BoomMSHRFile.refill_arb-af45d6b6d169fc58`
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

- occurrences: 3
- predicates: 1
- identity keys: 0
- cases: 2
- candidate axioms: 10
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 10
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 10
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] io.out.bits.addr = io.in[0].bits.addr on Input0Fire
- `A4` [FORMALLY_PROVED] io.out.bits.data = io.in[0].bits.data on Input0Fire
- `A5` [FORMALLY_PROVED] io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.wmask = io.in[0].bits.wmask on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.addr = io.in[1].bits.addr on Input1Fire
- `A8` [FORMALLY_PROVED] io.out.bits.data = io.in[1].bits.data on Input1Fire
- `A9` [FORMALLY_PROVED] io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire
- `A10` [FORMALLY_PROVED] io.out.bits.wmask = io.in[1].bits.wmask on Input1Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
