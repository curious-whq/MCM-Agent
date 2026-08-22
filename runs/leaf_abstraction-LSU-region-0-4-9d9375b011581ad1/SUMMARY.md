# Run Summary — LSU::region-0-4

## Identity

- task: `leaf_abstraction-LSU-region-0-4-9d9375b011581ad1`
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
- predicates: 5
- identity keys: 0
- cases: 3
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

- `A1` [FORMALLY_PROVED] ExceptionRegister <=> exactly_one_same_cycle({MemExceptionRegister, LoadExceptionRegister})
- `A2` [FORMALLY_PROVED] RegisterControlBlocked => !ExceptionRegister
- `A3` [FORMALLY_PROVED] NoMemExceptionPending => !MemExceptionRegister
- `A4` [FORMALLY_PROVED] NoLoadExceptionPending => !LoadExceptionRegister
- `A5` [FORMALLY_PROVED] xcpt_uop.rob_idx = mem_xcpt_uop.rob_idx on MemExceptionRegister
- `A6` [FORMALLY_PROVED] xcpt_uop.rob_idx = ld_xcpt_uop.rob_idx on LoadExceptionRegister
- `A7` [FORMALLY_PROVED] _r_xcpt_cause_T = mem_xcpt_cause on MemExceptionRegister
- `A8` [FORMALLY_PROVED] bits(_r_xcpt_cause_T, 4, 4) == 1 on LoadExceptionRegister
- `A8b` [FORMALLY_PROVED] bits(_r_xcpt_cause_T, 3, 3) == 0 on LoadExceptionRegister
- `A8c` [FORMALLY_PROVED] bits(_r_xcpt_cause_T, 2, 2) == 0 on LoadExceptionRegister
- `A8d` [FORMALLY_PROVED] bits(_r_xcpt_cause_T, 1, 1) == 0 on LoadExceptionRegister
- `A8e` [FORMALLY_PROVED] bits(_r_xcpt_cause_T, 0, 0) == 0 on LoadExceptionRegister
- `A9` [FORMALLY_PROVED] NoRegisteredException => !LoadExceptionVisible
- `A10` [FORMALLY_PROVED] OutputControlBlocked => !LoadExceptionVisible
- `A11` [FORMALLY_PROVED] io.core.lxcpt.bits.cause = r_xcpt.cause on LoadExceptionVisible
- `A12` [FORMALLY_PROVED] io.core.lxcpt.bits.badvaddr = r_xcpt.badvaddr on LoadExceptionVisible
- `A13` [FORMALLY_PROVED] io.core.lxcpt.bits.uop.rob_idx = r_xcpt.uop.rob_idx on LoadExceptionVisible
- `A14` [FORMALLY_PROVED] io.core.lxcpt.bits.uop.ldq_idx = r_xcpt.uop.ldq_idx on LoadExceptionVisible
- `A15` [FORMALLY_PROVED] io.core.lxcpt.bits.uop.stq_idx = r_xcpt.uop.stq_idx on LoadExceptionVisible
- `A16` [FORMALLY_PROVED] io.core.lxcpt.bits.uop.mem_cmd = r_xcpt.uop.mem_cmd on LoadExceptionVisible

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
