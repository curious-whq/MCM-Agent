# Run Summary — BoomMSHRFile.replay_arb

## Identity

- task: `leaf_abstraction-BoomMSHRFile.replay_arb-8fdf73acfd546ea3`
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
- candidate axioms: 20
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 20
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 20
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] io.out.bits.addr = io.in[0].bits.addr on Input0Fire
- `A4` [FORMALLY_PROVED] io.out.bits.uop.mem_cmd = io.in[0].bits.uop.mem_cmd on Input0Fire
- `A5` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[0].bits.uop.ldq_idx on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[0].bits.uop.stq_idx on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.sdq_id = io.in[0].bits.sdq_id on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.old_meta.tag = io.in[0].bits.old_meta.tag on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.old_meta.coh.state = io.in[0].bits.old_meta.coh.state on Input0Fire
- `A10` [FORMALLY_PROVED] io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire
- `A11` [FORMALLY_PROVED] io.out.bits.tag_match = io.in[0].bits.tag_match on Input0Fire
- `A12` [FORMALLY_PROVED] io.out.bits.addr = io.in[1].bits.addr on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.uop.mem_cmd = io.in[1].bits.uop.mem_cmd on Input1Fire
- `A14` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[1].bits.uop.ldq_idx on Input1Fire
- `A15` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[1].bits.uop.stq_idx on Input1Fire
- `A16` [FORMALLY_PROVED] io.out.bits.sdq_id = io.in[1].bits.sdq_id on Input1Fire
- `A17` [FORMALLY_PROVED] io.out.bits.old_meta.tag = io.in[1].bits.old_meta.tag on Input1Fire
- `A18` [FORMALLY_PROVED] io.out.bits.old_meta.coh.state = io.in[1].bits.old_meta.coh.state on Input1Fire
- `A19` [FORMALLY_PROVED] io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire
- `A20` [FORMALLY_PROVED] io.out.bits.tag_match = io.in[1].bits.tag_match on Input1Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
