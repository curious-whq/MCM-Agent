# Run Summary — BoomNonBlockingDCache::region-0-1

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8`
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

- occurrences: 5
- predicates: 1
- identity keys: 0
- cases: 4
- candidate axioms: 32
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 32
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 32
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] OutputCFire <=> exactly_one_same_cycle({WBStartBeat, ProbeStartBeat, WBContinuationBeat, ProbeContinuationBeat})
- `A2` [FORMALLY_PROVED] WBReleaseValid => !ProbeStartBeat
- `A3` [FORMALLY_PROVED] WBStartBeat <mu WBContinuationBeat
- `A4` [FORMALLY_PROVED] ProbeStartBeat <mu ProbeContinuationBeat
- `A5` [FORMALLY_PROVED] nodeOut.c.bits.address = wb.io.release.bits.address on WBStartBeat
- `A6` [FORMALLY_PROVED] nodeOut.c.bits.source = wb.io.release.bits.source on WBStartBeat
- `A7` [FORMALLY_PROVED] nodeOut.c.bits.size = wb.io.release.bits.size on WBStartBeat
- `A8` [FORMALLY_PROVED] nodeOut.c.bits.param = wb.io.release.bits.param on WBStartBeat
- `A9` [FORMALLY_PROVED] nodeOut.c.bits.opcode = wb.io.release.bits.opcode on WBStartBeat
- `A10` [FORMALLY_PROVED] nodeOut.c.bits.data = wb.io.release.bits.data on WBStartBeat
- `A11` [FORMALLY_PROVED] nodeOut.c.bits.corrupt = wb.io.release.bits.corrupt on WBStartBeat
- `A12` [FORMALLY_PROVED] nodeOut.c.bits.address = wb.io.release.bits.address on WBContinuationBeat
- `A13` [FORMALLY_PROVED] nodeOut.c.bits.source = wb.io.release.bits.source on WBContinuationBeat
- `A14` [FORMALLY_PROVED] nodeOut.c.bits.size = wb.io.release.bits.size on WBContinuationBeat
- `A15` [FORMALLY_PROVED] nodeOut.c.bits.param = wb.io.release.bits.param on WBContinuationBeat
- `A16` [FORMALLY_PROVED] nodeOut.c.bits.opcode = wb.io.release.bits.opcode on WBContinuationBeat
- `A17` [FORMALLY_PROVED] nodeOut.c.bits.data = wb.io.release.bits.data on WBContinuationBeat
- `A18` [FORMALLY_PROVED] nodeOut.c.bits.corrupt = wb.io.release.bits.corrupt on WBContinuationBeat
- `A19` [FORMALLY_PROVED] nodeOut.c.bits.address = prober.io.rep.bits.address on ProbeStartBeat
- `A20` [FORMALLY_PROVED] nodeOut.c.bits.source = prober.io.rep.bits.source on ProbeStartBeat
- `A21` [FORMALLY_PROVED] nodeOut.c.bits.size = prober.io.rep.bits.size on ProbeStartBeat
- `A22` [FORMALLY_PROVED] nodeOut.c.bits.param = prober.io.rep.bits.param on ProbeStartBeat
- `A23` [FORMALLY_PROVED] nodeOut.c.bits.opcode = prober.io.rep.bits.opcode on ProbeStartBeat
- `A24` [FORMALLY_PROVED] nodeOut.c.bits.data = prober.io.rep.bits.data on ProbeStartBeat
- `A25` [FORMALLY_PROVED] nodeOut.c.bits.corrupt = prober.io.rep.bits.corrupt on ProbeStartBeat
- `A26` [FORMALLY_PROVED] nodeOut.c.bits.address = prober.io.rep.bits.address on ProbeContinuationBeat
- `A27` [FORMALLY_PROVED] nodeOut.c.bits.source = prober.io.rep.bits.source on ProbeContinuationBeat
- `A28` [FORMALLY_PROVED] nodeOut.c.bits.size = prober.io.rep.bits.size on ProbeContinuationBeat
- `A29` [FORMALLY_PROVED] nodeOut.c.bits.param = prober.io.rep.bits.param on ProbeContinuationBeat
- `A30` [FORMALLY_PROVED] nodeOut.c.bits.opcode = prober.io.rep.bits.opcode on ProbeContinuationBeat
- `A31` [FORMALLY_PROVED] nodeOut.c.bits.data = prober.io.rep.bits.data on ProbeContinuationBeat
- `A32` [FORMALLY_PROVED] nodeOut.c.bits.corrupt = prober.io.rep.bits.corrupt on ProbeContinuationBeat

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
