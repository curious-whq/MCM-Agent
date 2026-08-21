# Run Summary — BoomNonBlockingDCache::region-0-2

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache-region-0-2-05c1013f696ad6ab`
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
- predicates: 2
- identity keys: 0
- cases: 2
- candidate axioms: 11
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 11
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 11
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] DFire <=> exactly_one_same_cycle({ReleaseAckFire, MSHRGrantFire})
- `A2` [FORMALLY_PROVED] NonReleaseAckSource => !ReleaseAckFire
- `A3` [FORMALLY_PROVED] ReleaseAckSource => !MSHRGrantFire
- `A4` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.opcode = nodeOut.d.bits.opcode on MSHRGrantFire
- `A5` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.param = nodeOut.d.bits.param on MSHRGrantFire
- `A6` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.size = nodeOut.d.bits.size on MSHRGrantFire
- `A7` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.source = nodeOut.d.bits.source on MSHRGrantFire
- `A8` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.sink = nodeOut.d.bits.sink on MSHRGrantFire
- `A9` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.denied = nodeOut.d.bits.denied on MSHRGrantFire
- `A10` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.data = nodeOut.d.bits.data on MSHRGrantFire
- `A11` [FORMALLY_PROVED] mshrs.io.mem_grant.bits.corrupt = nodeOut.d.bits.corrupt on MSHRGrantFire

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
