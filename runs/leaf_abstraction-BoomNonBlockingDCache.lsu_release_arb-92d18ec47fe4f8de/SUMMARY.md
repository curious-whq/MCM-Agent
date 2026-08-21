# Run Summary — BoomNonBlockingDCache.lsu_release_arb

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache.lsu_release_arb-92d18ec47fe4f8de`
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
- `A4` [FORMALLY_PROVED] io.out.bits.opcode = io.in[0].bits.opcode on Input0Fire
- `A5` [FORMALLY_PROVED] io.out.bits.param = io.in[0].bits.param on Input0Fire
- `A6` [FORMALLY_PROVED] io.out.bits.size = io.in[0].bits.size on Input0Fire
- `A7` [FORMALLY_PROVED] io.out.bits.source = io.in[0].bits.source on Input0Fire
- `A8` [FORMALLY_PROVED] io.out.bits.address = io.in[0].bits.address on Input0Fire
- `A9` [FORMALLY_PROVED] io.out.bits.data = io.in[0].bits.data on Input0Fire
- `A10` [FORMALLY_PROVED] io.out.bits.corrupt = io.in[0].bits.corrupt on Input0Fire
- `A11` [FORMALLY_PROVED] io.chosen = 1 on Input1Fire
- `A12` [FORMALLY_PROVED] io.out.bits.opcode = io.in[1].bits.opcode on Input1Fire
- `A13` [FORMALLY_PROVED] io.out.bits.param = io.in[1].bits.param on Input1Fire
- `A14` [FORMALLY_PROVED] io.out.bits.size = io.in[1].bits.size on Input1Fire
- `A15` [FORMALLY_PROVED] io.out.bits.source = io.in[1].bits.source on Input1Fire
- `A16` [FORMALLY_PROVED] io.out.bits.address = io.in[1].bits.address on Input1Fire
- `A17` [FORMALLY_PROVED] io.out.bits.data = io.in[1].bits.data on Input1Fire
- `A18` [FORMALLY_PROVED] io.out.bits.corrupt = io.in[1].bits.corrupt on Input1Fire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
