# Run Summary — BoomMSHRFile.mmios_0

## Identity

- task: `leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.9`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 5
- predicates: 2
- identity keys: 1
- cases: 3
- candidate axioms: 9
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 9
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 9
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] Busy => !ReqAccept
- `A2` [FORMALLY_PROVED] ReqAccept <mu MemAccess
- `A3` [FORMALLY_PROVED] MemAccess <mu AckConsumed
- `A4` [FORMALLY_PROVED] AckConsumed <mu RespHandshake
- `A5` [FORMALLY_PROVED] NoResponseRequired => !RespHandshake
- `A6` [FORMALLY_PROVED] capture RequestIdentity := io.req.bits on ReqAccept; preserve 5 exact identity projections
- `A7` [FORMALLY_PROVED] io.mem_access.bits.address = bits(req.addr, 31, 0) on MemAccess
- `A8` [FORMALLY_PROVED] io.mem_access.bits.size = req.uop.mem_size on MemAccess
- `A9` [FORMALLY_PROVED] io.resp.bits.is_hella = req.is_hella on RespHandshake

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
