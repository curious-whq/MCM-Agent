# Run Summary — LSU.wakeupArbs_0

## Identity

- task: `leaf_abstraction-LSU.wakeupArbs_0-ff3ba2cdefa94ee7`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.14`
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
- candidate axioms: 18
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 18
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 18
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] io.chosen = 0 on Input0Fire
- `A4` [FORMALLY_PROVED] io.chosen = 1 on Input1Fire
- `A5` [FORMALLY_PROVED] io.out.bits.uop.rob_idx = io.in[0].bits.uop.rob_idx on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[0].bits.uop.ldq_idx on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[0].bits.uop.stq_idx on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.uop.pdst = io.in[0].bits.uop.pdst on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.speculative_mask = io.in[0].bits.speculative_mask on Input0Fire
- `A10` [FORMALLY_PROVED] io.out.bits.bypassable = io.in[0].bits.bypassable on Input0Fire
- `A11` [FORMALLY_PROVED] io.out.bits.rebusy = io.in[0].bits.rebusy on Input0Fire
- `A12` [FORMALLY_PROVED] io.out.bits.uop.rob_idx = io.in[1].bits.uop.rob_idx on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[1].bits.uop.ldq_idx on Input1Fire
- `A14` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[1].bits.uop.stq_idx on Input1Fire
- `A15` [FORMALLY_PROVED] io.out.bits.uop.pdst = io.in[1].bits.uop.pdst on Input1Fire
- `A16` [FORMALLY_PROVED] io.out.bits.speculative_mask = io.in[1].bits.speculative_mask on Input1Fire
- `A17` [FORMALLY_PROVED] io.out.bits.bypassable = io.in[1].bits.bypassable on Input1Fire
- `A18` [FORMALLY_PROVED] io.out.bits.rebusy = io.in[1].bits.rebusy on Input1Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
