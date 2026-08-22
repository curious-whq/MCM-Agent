# Run Summary — LSU::region-0-5

## Identity

- task: `leaf_abstraction-LSU-region-0-5-7aada22dd0e23995`
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
- predicates: 0
- identity keys: 0
- cases: 1
- candidate axioms: 6
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 6
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 6
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] bits(io.hellacache.resp.bits.replay, 0, 0) == 0 on HellaResponse
- `A2` [FORMALLY_PROVED] bits(io.hellacache.resp.bits.has_data, 0, 0) == 1 on HellaResponse
- `A3` [FORMALLY_PROVED] io.hellacache.resp.bits.dprv = io.ptw.status.prv on HellaResponse
- `A4` [FORMALLY_PROVED] io.hellacache.resp.bits.dv = io.ptw.status.v on HellaResponse
- `A5` [FORMALLY_PROVED] io.hellacache.resp.bits.data_word_bypass = io.dmem.ll_resp.bits.data on HellaResponse
- `A6` [FORMALLY_PROVED] io.hellacache.resp.bits.data_raw = io.dmem.ll_resp.bits.data on HellaResponse

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
