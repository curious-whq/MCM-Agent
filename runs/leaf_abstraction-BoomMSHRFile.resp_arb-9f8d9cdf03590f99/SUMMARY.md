# Run Summary — BoomMSHRFile.resp_arb

## Identity

- task: `leaf_abstraction-BoomMSHRFile.resp_arb-9f8d9cdf03590f99`
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

- occurrences: 4
- predicates: 2
- identity keys: 0
- cases: 3
- candidate axioms: 21
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 21
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 21
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire})
- `A2` [FORMALLY_PROVED] Input0Valid => !Input1Fire
- `A3` [FORMALLY_PROVED] Higher01Valid => !Input2Fire
- `A4` [FORMALLY_PROVED] io.out.bits.data = io.in[0].bits.data on Input0Fire
- `A5` [FORMALLY_PROVED] io.out.bits.is_hella = io.in[0].bits.is_hella on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.uop.rob_idx = io.in[0].bits.uop.rob_idx on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[0].bits.uop.ldq_idx on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[0].bits.uop.stq_idx on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.uop.mem_cmd = io.in[0].bits.uop.mem_cmd on Input0Fire
- `A10` [FORMALLY_PROVED] io.out.bits.data = io.in[1].bits.data on Input1Fire
- `A11` [FORMALLY_PROVED] io.out.bits.is_hella = io.in[1].bits.is_hella on Input1Fire
- `A12` [FORMALLY_PROVED] io.out.bits.uop.rob_idx = io.in[1].bits.uop.rob_idx on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[1].bits.uop.ldq_idx on Input1Fire
- `A14` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[1].bits.uop.stq_idx on Input1Fire
- `A15` [FORMALLY_PROVED] io.out.bits.uop.mem_cmd = io.in[1].bits.uop.mem_cmd on Input1Fire
- `A16` [FORMALLY_PROVED] io.out.bits.data = io.in[2].bits.data on Input2Fire
- `A17` [FORMALLY_PROVED] io.out.bits.is_hella = io.in[2].bits.is_hella on Input2Fire
- `A18` [FORMALLY_PROVED] io.out.bits.uop.rob_idx = io.in[2].bits.uop.rob_idx on Input2Fire
- `A19` [FORMALLY_PROVED] io.out.bits.uop.ldq_idx = io.in[2].bits.uop.ldq_idx on Input2Fire
- `A20` [FORMALLY_PROVED] io.out.bits.uop.stq_idx = io.in[2].bits.uop.stq_idx on Input2Fire
- `A21` [FORMALLY_PROVED] io.out.bits.uop.mem_cmd = io.in[2].bits.uop.mem_cmd on Input2Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
