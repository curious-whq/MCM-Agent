# MCM-Agent Current Handoff

> This file is intentionally self-contained. In a fresh conversation, upload/paste this file first, then upload the current task `prompt.md` if the next action is an LLM/manual semantic task.

## Resume instruction for a new conversation

Continue the MCM-Agent project from this handoff. Treat the recorded design decisions as established unless new RTL/formal evidence contradicts them. Do not restart partition design. Follow the Current Status and Next Action, and preserve new durable lessons back into the repository/run memory files.

Repository version: `0.0.9`

---

## Goal

# MCM-Agent Research Goal

MCM-Agent aims to turn a real elaborated microarchitecture into a recursively composable microarchitectural memory model (µMCM):

```text
whole RTL
  -> static hierarchical WorkUnits
  -> leaf candidate µMCM
  -> proof / trusted µMCM
  -> child replacement
  -> parent axiom synthesis
  -> subsystem µMCM (L1, L2, LSQ/LSU)
  -> memory-system µMCM
  -> architectural MCM checking (e.g. RVWMO)
  -> concrete RTL feasibility / real bug
```

The static planner, not the LLM, decides the WorkUnit hierarchy. The LLM proposes semantic abstractions and synthesis steps; deterministic/formal validation decides what may enter the trusted µMCM.

## Manual bootstrap constraint

For the first three weeks, human ChatGPT conversations temporarily play the role of the LLM provider. The workflow itself should already be the future automated workflow. After the bootstrap period, the manual provider should be replaceable by a real LLM provider without redesigning downstream validation or synthesis.

---

## Method

# Current Method

## Static hierarchy

1. Prefer physical module/instance hierarchy.
2. If a physical module is too large, recursively create module-internal WorkUnits from immediate event-state structure and state/dependency structure.
3. Event slices are analysis primitives, not final abstraction units.
4. Shared logic/state is promoted to the parent and never copied between children.
5. Coverage is fail-closed: no statement/state/event may silently disappear or be multiply owned.
6. A parent replaces a completed child with a child µMCM summary rather than rereading child RTL during semantic synthesis.

## µMCM generation

Current experimental language uses:

- occurrences: boundary or RTL-grounded derived occurrences;
- persistent predicates;
- transaction/object identity;
- semantic cases;
- candidate axioms;
- environment assumptions and unresolved obligations.

The LLM may propose candidates, but candidate axioms are not trusted by default.

## Validation and trust

Validation levels are intentionally separated:

```text
GROUNDED
  -> PARTIALLY_SUPPORTED / STRUCTURALLY_SUPPORTED
  -> FORMALLY_PROVED
  -> SPEC_PROVED
```

Only `FORMALLY_PROVED` or `SPEC_PROVED` axioms may enter `trusted_umcm.json`.

Completeness is not assumed. Missing axioms are expected to make the µMCM an over-approximation. Later system-level counterexamples are checked against concrete RTL; spurious traces drive counterexample-guided µMCM refinement.

## Bottom-up synthesis

Parent synthesis must preserve provenance. A parent axiom can be:

- inherited from a child;
- lifted/generalized from one or more case-specific child axioms;
- emergent from multiple child contracts plus parent-local RTL/glue.

Any generalization must record `derived_from` information so the user can observe how several lower-level axioms became one higher-level axiom.

---

## Decisions

# Design Decisions

This file records decisions that a new conversation should not casually reopen unless new evidence contradicts them.

## D001 — Static analysis owns partitioning
The LLM does not decide how RTL is partitioned. Physical hierarchy is preferred; large physical modules may be recursively split by static event/state/dependency analysis.

## D002 — Event slice is not the final WorkUnit
Full historical event cones merge unrelated FSM history. Partition discovery therefore uses an immediate event-state frontier; historical cones remain useful for later semantic extraction.

## D003 — Shared logic is parent-owned
Logic/state used across child scopes is promoted to the parent rather than duplicated. Coverage ledgers must remain complete and non-overlapping.

## D004 — Logical complexity is distinct from raw FIRRTL complexity
Raw FIRRTL lowering can inflate statement/signal/edge counts. Planner decisions use logical/source-aware complexity while preserving raw graphs for slicing and validation.

## D005 — µMCM needs occurrences and predicates
Boundary `.fire` events alone are insufficient. ProbeUnit exposed two necessary abstractions: persistent predicates such as `ActiveProbe`, and RTL-grounded internal milestones such as `WBComplete`.

## D006 — Derived occurrences are fail-closed
A derived occurrence is allowed only when it has a precise RTL definition/evidence and is necessary to retain ordering/path/visibility/exclusion information. Internal FSM states must not be mechanically dumped into the µMCM.

## D007 — Candidate is not trusted
Grounding or structural support never upgrades an axiom into the trusted abstraction. Only `FORMALLY_PROVED` or `SPEC_PROVED` axioms may constrain parent composition.

## D008 — Completeness is refined, not assumed
The project does not attempt to prove in one step that the LLM found every important axiom. Trusted axioms form a safe over-approximation; spurious system counterexamples are used to discover missing constraints.

## D009 — Manual-first and automated modes share one workflow
During the bootstrap period, LLM nodes export self-contained prompts for manual conversations. Future API providers must implement the same task/result interface so validation, synthesis and provenance do not change.

## D010 — Three-week manual bootstrap
The manual phase is time-boxed. Week 1 builds an L1 representative end-to-end synthesis chain; Week 2 broadens to representative L1/L2/LSQ cases and stabilizes schema/validators; Week 3 replaces the manual provider and runs held-out/whole-BOOM automation.

## D011 — A leaf is frozen only after all declared axioms are trusted
A leaf may produce `frozen_umcm.json` only when every currently declared candidate axiom is `FORMALLY_PROVED` or `SPEC_PROVED` and the candidate has no unresolved items. "Frozen" means ready for parent composition, not permanently complete: a later spurious parent/system counterexample may reopen it through CEGAR.

## D012 — Identity claims should be exact projections when possible
Generic dependency is insufficient for a trusted transaction-identity axiom. For ProbeUnit, the accepted request must be captured exactly into the carrier and each declared identity-bearing output must reduce to an exact symbolic projection of the latched carrier.

## D013 — Protocol semantic checks may use an explicit independent finite reference table
For small finite protocol functions such as TileLink `ClientMetadata.onProbe`, a trusted reference table is kept separate from the FIRRTL evaluator and all legal input combinations are exhaustively compared. Such results are marked `SPEC_PROVED` relative to that encoded reference, not as a theorem about every possible protocol implementation.


## D014 — Formal axiom AST is the single semantic source of truth
Every µMCM axiom is represented as a structured formal AST. The LLM may not provide a separate prose formula or validation program. Human-readable formulas, referenced semantic objects, proof-obligation checker type, and checker arguments are all generated deterministically from the same AST. This removes the trust gap where prose could claim more than the verifier actually proved.

## D015 — Finite repetition is modeled generically as indexed occurrences
µMCM does not add module-specific "multi-beat" axioms. A repeated hardware action may carry a finite index domain, and generic `indexed_complete` axioms state exact coverage at a completion point. The same abstraction is intended for cache beats, refill beats, banks, entries, fragments or similar bounded repetitions. The bundled explicit-control backend intentionally leaves exact indexed completeness untrusted until a counter/index-capable proof backend is available.

## D016 — Unordered prerequisites use a generic join axiom
When completion requires several events that may arrive in either order, µMCM uses a generic `join` axiom rather than inventing a module-specific completion rule. The current explicit-control backend can formally prove such join-order obligations when the occurrences are grounded in the certified finite-control abstraction.

---

## Lessons

# Research Lessons

## ProbeUnit

- The leaf contains about 97 mapped source lines, 132 logical statements, 209 raw FIRRTL statements, 4 registers and 7 physical boundary events.
- Eleven FSM states compress naturally into three protocol cases: no-match, matched-clean and matched-dirty. The µMCM should not copy the FSM verbatim.
- `req` acts as a transaction identity carrier: the incoming Probe request is latched and later output fields derive from it.
- `MetaRead` may repeat because the controller can retry when MSHR/writeback readiness is unavailable; event cardinality cannot always be assumed to be exactly once.
- `ActiveProbe` is better modeled as a persistent predicate than as an occurrence.
- The dirty path requires an internal `WBComplete` milestone to express the important order `WBReq < WBComplete < MetaWrite`.
- Clean/non-dirty and dirty paths motivate later axiom synthesis: case-specific constraints such as `ProbeAck < MetaWrite` and `WBComplete < MetaWrite` may be lifted into a higher-level `ProbeResponseComplete < MetaWrite` axiom, with explicit provenance.
- ProbeUnit now closes with 8/8 trusted axioms: 7 `FORMALLY_PROVED` and 1 `SPEC_PROVED`. A2 identity preservation is proved by exact capture of `io.req.bits` into `req` plus 14 exact symbolic output projections; A7 is checked exhaustively against the separate 12-row TileLink `onProbe` reference table.

## Validation

- A structural path check is useful evidence but must not be called a complete semantic proof.
- The explicit-control backend remains fail-closed for control/order properties, but now also supports exact symbolic identity projection and selected finite reference-equivalence obligations. It is still not a general-purpose SMT/bit-level RTL prover.
- A finite protocol function can be `SPEC_PROVED` when the reference semantics are encoded independently from the FIRRTL evaluator and every legal input row is exhaustively checked. ProbeUnit `onProbe` is the first such example.
- Freezing a leaf does not prove abstraction completeness forever; the child may be reopened if later CEGAR finds a spurious parent/system trace that requires a missing axiom.

- Formal axiom AST is now the unique source of truth: ProbeUnit's same 8 axioms migrate without semantic loss, while pretty-printed formulas and proof obligations are generated from the AST rather than authored independently.

## WritebackUnit (language-discovery pass)

- WritebackUnit introduces bounded repeated cache-line transfers: the same semantic action occurs once per beat/index rather than as one scalar occurrence.
- The useful abstraction is not a Writeback-specific beat axiom. µMCM now permits a generic indexed occurrence `o(txn,i)` over a finite domain plus an `indexed_complete` conservation axiom.
- Voluntary writeback also exposes an unordered completion join: all release beats must finish and a memory grant must be observed, but the grant may arrive before or after the last release beat. This is represented by the generic `join` axiom.
- Exact indexed completeness is intentionally not promoted by the current explicit-control backend because that backend does not track counter/index values. The AST and proof obligation exist now; trust requires a later bounded-index/counter-capable backend.

---

## Roadmap 3W

# Three-Week Manual Bootstrap Roadmap

## Days 1–7 — L1 representative end-to-end chain

Goal: prove the full workflow, especially parent synthesis, not manually finish every L1 WorkUnit.

Representative targets include ProbeUnit, WritebackUnit, MSHR/MSHRFile, one RPQ/Queue path, and parent-local glue. Required milestone: observe at least one real lower-level-to-parent axiom generalization with provenance.

## Days 8–14 — Broaden representative coverage

Use a small but diverse set rather than exhaustively processing every module:

- continue key L1 modules;
- sample L2 Directory/MSHR/Source-Sink behavior;
- sample one or two automatically partitioned LSQ/LSU regions.

By the end of this period, stabilize the µMCM schema, property obligation types, refinement protocol and parent synthesis result format.

## Days 15–21 — Automation cutover

Implement a real LLM provider, replay known manual cases, then evaluate held-out WorkUnits. By Day 21, start a whole-BOOM automatic run. After the cutover, humans should mainly analyze failures/counterexamples rather than manually generate every WorkUnit µMCM.

---

## Status

# Current Project Status

## Static planner

- Real-BOOM hierarchical planner is implemented and validated on the uploaded SmallBoomV4Config FIRRTL.
- L1, L2 and LSU roots have recursive WorkUnit plans with complete coverage.

## Workflow

- Manual-first leaf task export/import is implemented.
- µMCM `umcm-formal-0.5` supports scalar/indexed boundary or derived occurrences, predicates, identity, cases, assumptions, generic join/indexed-completeness relations, and same-index relation scopes with indexed lookup expressions; prose formulas/validation programs are no longer semantic inputs.
- Grounding validation is deterministic and fail-closed; it rejects legacy `formula`/`validation` fields and unsupported Formal AST shapes.
- Validation trust levels distinguish grounding, structural support, formal proof and reference/spec proof.
- `explicit-control` backend proves certified finite-control/order properties, exact symbolic local/identity facts, and selected finite reference equivalence checks.
- A fully proved leaf with no unresolved items can be frozen as `frozen_umcm.json` for parent composition; it remains reopenable by later CEGAR refinement.

## ProbeUnit

- Candidate axioms: 8.
- Trusted axioms: 8.
- `FORMALLY_PROVED`: 7.
- `SPEC_PROVED`: 1 (`ClientMetadata.onProbe` finite reference equivalence over all 12 legal Probe cap × client-state combinations).
- Request identity preservation (A2) is now proved by exact capture plus 14 exact symbolic output projections of the latched `req` transaction.
- Unresolved items: 0.
- Status: `FROZEN_FOR_COMPOSITION`.

## Current phase

Manual Bootstrap, Week-1 style objective: continue the representative L1 chain. Current semantic target is WritebackUnit. Its language-discovery passes added generic indexed occurrences, join/indexed-completeness axioms, and same-index relation scopes; next regenerate the WritebackUnit task under v0.9 and produce/validate the candidate µMCM before deciding whether a bounded-index proof backend is required.

---

## Recent WorkUnit Runs

### Run: `leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b`

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

### Experiment experience

# Experiment Experience

Keep only lessons that should survive this conversation. Delete empty bullets instead of inventing content.

## INPUT_NEEDED

- 

## PROMPT_RULE

- 

## SCHEMA_CHANGE

- 

## VALIDATOR_CHANGE

- 

## MODEL_FAILURE

- 

## GENERALIZATION

-

### Run: `leaf_abstraction-BoomProbeUnit-6a11da8fc6b94afe`

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

### Experiment experience

# Experiment Experience

Keep only lessons that should survive this conversation. Delete empty bullets instead of inventing content.

## INPUT_NEEDED

- 

## PROMPT_RULE

- 

## SCHEMA_CHANGE

- 

## VALIDATOR_CHANGE

- 

## MODEL_FAILURE

- 

## GENERALIZATION

-

---

## New-conversation operating rule

1. Read this handoff before analyzing a new WorkUnit.
2. If a WorkUnit LLM task is pending, also read that run's `prompt.md`; it remains the authoritative task-specific grounding package.
3. Do not infer trusted axioms from prose. Use `trusted_umcm.json` / formal validation status.
4. After a meaningful experiment, update the run `EXPERIENCE.md`, regenerate `SUMMARY.md`, and regenerate this handoff.
