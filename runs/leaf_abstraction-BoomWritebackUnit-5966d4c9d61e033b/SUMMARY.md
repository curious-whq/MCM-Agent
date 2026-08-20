# Run Summary — BoomWritebackUnit

## Identity

- task: `leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.5`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 9
- predicates: 4
- identity keys: 1
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

- `A1` [FORMALLY_PROVED] ActiveWriteback => !WritebackReq [same WritebackTxn]
- `A2` [FORMALLY_PROVED] capture WritebackTxn := io.req.bits on WritebackReq; preserve 6 exact identity projections
- `A3` [FORMALLY_PROVED] BufferFilled => forall beat in [0, 8): count(BufferBeat(beat)) = 1 [same WritebackTxn]
- `A4` [FORMALLY_PROVED] FillIssue <mu BufferBeat [same WritebackTxn] [same index beat]
- `A5` [FORMALLY_PROVED] BufferFilled <mu LSURelease [same WritebackTxn]
- `A6` [FORMALLY_PROVED] BeforeNetworkRelease => !ReleaseBeat [same WritebackTxn]
- `A7` [FORMALLY_PROVED] ReleaseComplete => forall beat in [0, 8): count(ReleaseBeat(beat)) = 1 [same WritebackTxn]
- `A8` [FORMALLY_PROVED] io.release.bits.data = wb_buffer[beat] on ReleaseBeat [same WritebackTxn] [same index beat]
- `A9` [FORMALLY_PROVED] bits(io.release.bits.opcode, 0, 0) == 1 on ReleaseBeat [same WritebackTxn]
- `A10` [FORMALLY_PROVED] {ReleaseComplete, MemGrantSeen} <mu VoluntaryDone [same WritebackTxn]

## Next action

Parent synthesis may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
