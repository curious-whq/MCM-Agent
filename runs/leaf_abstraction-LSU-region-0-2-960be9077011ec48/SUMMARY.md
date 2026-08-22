# Run Summary — LSU::region-0-2

## Identity

- task: `leaf_abstraction-LSU-region-0-2-960be9077011ec48`
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

- occurrences: 1
- predicates: 0
- identity keys: 0
- cases: 1
- candidate axioms: 8
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 8
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 8
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] io.core.fresp[0].bits.data = fresp[0].bits.data on FPResponse
- `A2` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.rob_idx = fresp[0].bits.uop.rob_idx on FPResponse
- `A3` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.ldq_idx = fresp[0].bits.uop.ldq_idx on FPResponse
- `A4` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.stq_idx = fresp[0].bits.uop.stq_idx on FPResponse
- `A5` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.mem_cmd = fresp[0].bits.uop.mem_cmd on FPResponse
- `A6` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.mem_size = fresp[0].bits.uop.mem_size on FPResponse
- `A7` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.mem_signed = fresp[0].bits.uop.mem_signed on FPResponse
- `A8` [FORMALLY_PROVED] io.core.fresp[0].bits.uop.br_mask = fresp[0].bits.uop.br_mask on FPResponse

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
