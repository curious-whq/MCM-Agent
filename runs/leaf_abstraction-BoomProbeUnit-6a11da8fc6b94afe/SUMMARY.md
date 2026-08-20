# Run Summary — BoomProbeUnit

## Identity

- task: `leaf_abstraction-BoomProbeUnit-6a11da8fc6b94afe`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.7`
- prompt: `leaf-abstraction-prompt-0.3`
- schema: `umcm-formal-0.3`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 7
- predicates: 4
- identity keys: 1
- cases: 3
- candidate axioms: 8
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 7
- SPEC_PROVED: 1
- REFUTED: 0
- trusted axioms: 8
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] ActiveProbe => !ProbeReq [same ProbeTxn]
- `A2` [FORMALLY_PROVED] capture ProbeTxn := io.req.bits on ProbeReq; preserve 14 exact identity projections
- `A3` [FORMALLY_PROVED] WBReq excludes {LSURelease, ProbeAck} [same ProbeTxn]
- `A4` [FORMALLY_PROVED] LSURelease <mu ProbeAck [same ProbeTxn]
- `A5` [FORMALLY_PROVED] LSURelease <mu ProbeAck <mu MetaWrite [same ProbeTxn]
- `A6` [FORMALLY_PROVED] WBReq <mu WBComplete <mu MetaWrite [same ProbeTxn]
- `A7` [SPEC_PROVED] bindings satisfy tilelink.ClientMetadata.onProbe on MetaWrite [same ProbeTxn]
- `A8` [FORMALLY_PROVED] bits(io.rep.bits.opcode, 0, 0) == 0 on ProbeAck [same ProbeTxn]

## Next action

Parent synthesis may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
