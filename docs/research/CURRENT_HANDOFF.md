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

Same-cycle combinational routing/merging is expressed by a generic
`occurrence_partition`: `whole <=> OR(parts)` plus pairwise exclusion of all
parts. Ordering remains a separate historical relation, and payload/identity
forwarding remains a separate equality/flow claim.

The partition is defined for every non-empty `parts` set. A singleton is the
degenerate but useful 1→1 routing case: pairwise exclusion is vacuous and the
conservation relation becomes exact same-cycle occurrence equivalence.

An occurrence-conditioned `signal_equality` retains its `on` guard through
compilation. Exact proof reconstructs FIRRTL last-connect priority and checks
all selected payload drivers reachable under that occurrence; aggregate event
payload leaves remain valid grounding even when the logical ledger compacts the
corresponding statement read to the aggregate bundle.

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

Structural control/dataflow counterexamples are conservative diagnostic evidence, not automatically concrete RTL counterexamples. When an exact certified backend proves the concrete Boolean/control obligation, that proof takes precedence; otherwise the workflow remains fail-closed.

Completeness is not assumed. Missing axioms are expected to make the µMCM an over-approximation. Later system-level counterexamples are checked against concrete RTL; spurious traces drive counterexample-guided µMCM refinement.

## Bottom-up synthesis

Parent synthesis must preserve provenance. A parent axiom can be:

- inherited from a child;
- lifted/generalized from one or more case-specific child axioms;
- emergent from multiple child contracts plus parent-local RTL/glue.

Any generalization must preserve direct theorem provenance so the user can observe how lower-level axioms became a higher-level axiom. For a trusted parent axiom, `source_axioms` is derived from the composition prover certificate and checked against the LLM declaration before entering `trusted_umcm.json` or `frozen_umcm.json`; recursive descent through each frozen parent's direct provenance recovers the complete bottom-up chain.

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
µMCM does not add module-specific "multi-beat" axioms. A repeated hardware action may carry a finite index domain, and generic `indexed_complete` axioms state exact coverage at a completion point. The same abstraction is intended for cache beats, refill beats, banks, entries, fragments or similar bounded repetitions.

As of the WritebackUnit v0.9.1 validation pass, the bundled `explicit-control` backend can formally prove a bounded indexed-completeness obligation when it can certify the relevant finite index domain, monotone counter/index progression, completion condition, and absence of skipped/duplicated indices. The same backend can also certify supported same-index relations and indexed storage lookups. These capabilities remain fail-closed: if the required counter/index or lookup structure cannot be certified, the result stays untrusted.

## D016 — Unordered prerequisites use a generic join axiom
When completion requires several events that may arrive in either order, µMCM uses a generic `join` axiom rather than inventing a module-specific completion rule. The `explicit-control` backend can formally prove such join-order obligations when the prerequisite/completion occurrences and any sticky state used to remember an earlier prerequisite are grounded in its certified abstraction.

## D017 — Manual provider is transport-only; leaf semantics are autonomous
During the manual bootstrap, the human only transports `prompt.md` to the LLM and returns the result to the workflow. The human should not choose occurrences, predicates, identities, cases or axioms for each leaf. A leaf task must autonomously produce a complete candidate JSON when the current Formal AST is sufficient, or explicitly report a necessary, grounded, reusable `MCM-AGENT LANGUAGE GAP` when it is not. A formal-backend proof limitation is not a language gap: expressible candidate axioms are still emitted and `semantic-validate` decides whether they can be certified. Optional strengthening constraints may be deferred in `rationale` for later CEGAR rather than blocking the leaf.

## D018 — Parent synthesis consumes frozen semantic imports, never child RTL
A parent-synthesis task is built only after every direct child is `FROZEN_FOR_COMPOSITION`. The parent handoff contains parent-local RTL plus self-contained frozen child µMCM summaries and qualified imported semantic IDs; child internal RTL/state is not reopened. New parent axioms must record provenance in `extensions.parent_synthesis.axiom_provenance`. A wrapper may declare zero new axioms when it adds no memory/coherence-relevant constraint; freezing such a parent is valid because the already-frozen child summaries remain embedded imports. Obligations outside the certified composition rules remain fail-closed.

## D019 — Frozen parent provenance is certificate-derived
The LLM provenance declaration is a claim, not a trusted source. For every trusted parent axiom, the workflow extracts direct frozen-child theorem dependencies from the actual composition proof DAG, derives the provenance kind from the certified proof rule, and requires an exact match with the declaration before trust/freeze. The frozen parent stores these direct dependencies; higher-level tracing follows provenance recursively through frozen imports rather than copying an ever-growing transitive dependency list into every axiom.

## D020 — Conservative structural counterexamples do not preempt exact proof
The finite structural abstraction may admit signal combinations that concrete local Boolean logic excludes. A structural counterexample therefore remains diagnostic when a stronger exact checker is available. A certified `FORMALLY_PROVED` or `SPEC_PROVED` result takes precedence over such an abstract counterexample; a formal counterexample still refutes the axiom, and an unresolved formal result does not gain trust.

## D021 — Same-cycle event routing uses one-hot occurrence partitions
µMCM represents exact combinational event routing/merging with the protocol-agnostic `occurrence_partition` axiom. `same_cycle_exactly_one` means `whole` is equivalent to the same-cycle disjunction of `parts`, and every pair of parts is mutually exclusive. It is one-hot conservation, not n-ary parity. The deterministic prover must establish both directions and all pairwise exclusions from exact local Boolean cones; it does not recognize arbiter/module names or assume a priority policy. Identity/payload flow remains a separate axiom, so the initial partition form requires `scope_identity: null`.

## D022 — Conditional payload equality preserves its occurrence guard
`signal_equality.on` is part of the proof obligation and may not be erased by compilation. The exact local prover reconstructs FIRRTL last-connect priority from all payload drivers and positive `when` activations, then checks every driver selection reachable under the physical boundary occurrence. If a derived occurrence has no exact Boolean guard, only an unconditional equality strengthening may discharge the claim. Physical event payload leaf paths are authoritative grounding signals even when logical compaction records only an aggregate FIRRTL read.

## D023 — Occurrence partitions include the singleton passthrough case
`occurrence_partition.parts` is non-empty rather than requiring at least two elements. For one part, `same_cycle_exactly_one` reduces to exact same-cycle equivalence between the whole and that part, while pairwise exclusion is vacuous. This keeps 1→1 routers in the same protocol-independent conservation primitive as N→1 arbiters instead of introducing a module-specific passthrough axiom.

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
- The explicit-control backend remains fail-closed. In addition to certified control/order properties, exact symbolic identity projection and selected finite reference-equivalence obligations, the WritebackUnit v0.9.1 pass adds certified bounded monotone counter/index reasoning, same-index valid/index pipeline reasoning, same-index indexed-storage lookup checks, sticky-state join reasoning, and aggregate-mux constant propagation. It is still not a general-purpose SMT/bit-level RTL prover.
- A finite protocol function can be `SPEC_PROVED` when the reference semantics are encoded independently from the FIRRTL evaluator and every legal input row is exhaustively checked. ProbeUnit `onProbe` is the first such example.
- Freezing a leaf does not prove abstraction completeness forever; the child may be reopened if later CEGAR finds a spurious parent/system trace that requires a missing axiom.

- Formal axiom AST is now the unique source of truth: ProbeUnit's same 8 axioms migrate without semantic loss, while pretty-printed formulas and proof obligations are generated from the AST rather than authored independently.

## WritebackUnit

- WritebackUnit introduces bounded repeated cache-line transfers: the same semantic action occurs once per beat/index rather than as one scalar occurrence.
- The useful abstraction is not a Writeback-specific beat axiom. µMCM uses a generic indexed occurrence `o(txn,i)` over a finite domain plus an `indexed_complete` conservation axiom.
- Voluntary writeback exposes an unordered completion join: all release beats must finish and a memory grant must be observed, but the grant may arrive before or after the last release beat. This is represented by the generic `join` axiom.
- WritebackUnit also requires pointwise same-index relations and indexed storage lookup, e.g. `FillIssue(txn,i) < BufferBeat(txn,i)` and `ReleaseBeat(txn,i).data = wb_buffer[i]`; these remain generic language features rather than module-specific axioms.
- The v0.9.1 formal-backend pass added reusable proofs for bounded monotone counter/index coverage, same-index valid/index pipelines, same-index storage lookup, sticky-state joins, and aggregate-mux constant propagation.
- The final WritebackUnit run closes with 10/10 candidate axioms `FORMALLY_PROVED`, 10 trusted axioms, 0 unresolved items, and status `FROZEN_FOR_COMPOSITION`.

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
- µMCM `umcm-formal-0.5` supports scalar/indexed boundary or derived occurrences, predicates, identity, cases, assumptions, generic join/indexed-completeness relations, exact same-cycle one-hot occurrence partitions, and same-index relation scopes with indexed lookup expressions; prose formulas/validation programs are no longer semantic inputs.
- Grounding validation is deterministic and fail-closed; it rejects legacy `formula`/`validation` fields and unsupported Formal AST shapes.
- Validation trust levels distinguish grounding, structural support, formal proof and reference/spec proof.
- `explicit-control` backend proves certified finite-control/order properties, exact symbolic local/identity facts, exact local Boolean exclusion and same-cycle occurrence conservation, selected finite reference equivalence checks, bounded monotone counter/index coverage (including cyclic FSM phase-entry zeroing cuts), supported same-index pipeline/storage relations, sticky-state joins, and supported aggregate-mux constant properties.
- A fully proved leaf with no unresolved items can be frozen as `frozen_umcm.json` for parent composition; it remains reopenable by later CEGAR refinement.
- Certified parent composition supports frozen theorem lift, exact parent-local/state-scoped occurrence bridges, scalar valid-token provenance, history transitivity, after-side history restriction, and safe same-index-to-unindexed weakening.
- Trusted/frozen parent provenance is derived from the composition certificate and must exactly match the LLM declaration; direct dependencies remain recursively traceable across frozen levels.

## ProbeUnit

- Candidate axioms: 8.
- Trusted axioms: 8.
- `FORMALLY_PROVED`: 7.
- `SPEC_PROVED`: 1 (`ClientMetadata.onProbe` finite reference equivalence over all 12 legal Probe cap × client-state combinations).
- Request identity preservation (A2) is now proved by exact capture plus 14 exact symbolic output projections of the latched `req` transaction.
- Unresolved items: 0.
- Status: `FROZEN_FOR_COMPOSITION`.

## WritebackUnit

- Workflow: `manual-first-workflow-0.9`; schema: `umcm-formal-0.5`.
- Candidate axioms: 10.
- Trusted axioms: 10.
- `FORMALLY_PROVED`: 10.
- `SPEC_PROVED`: 0.
- Unresolved items: 0.
- The trusted result covers bounded 8-beat completeness, same-index fill/buffer ordering, same-index release-data lookup, release ordering/exclusion, identity preservation, opcode constraint, and voluntary completion join.
- Status: `FROZEN_FOR_COMPOSITION`.

## BoomMSHR.rpq

- `BoomMSHR.rpq.main` is frozen with 9/9 trusted axioms.
- `BoomMSHR.rpq` completed the first real parent synthesis and is frozen with 7/7 `FORMALLY_PROVED`, 0 unresolved items.
- Frozen provenance records `BoomMSHR.rpq::A1` as lifted from `BoomMSHR.rpq.main::A1` and `BoomMSHR.rpq::A5` as emergent from `BoomMSHR.rpq.main::A11`, as required by their proof certificates.

## BoomMSHR

- Parent-synthesis candidate: 15 axioms, 15 `FORMALLY_PROVED`, 0 unresolved, 0 refuted.
- Refill completeness is certified through the three-bit counter, final-index transition, modulo wrap, and a zeroing-transition cut across the cyclic FSM.
- `MemFinish` exclusion is proved by its exact Boolean cone even though the conservative structural state abstraction admits a spurious state-only counterexample.
- Response/replay provenance is composed from frozen `BoomMSHR.rpq::A5` through exact state-scoped subsets of the RPQ dequeue boundary.
- Status: `FORMALLY_VALIDATED`; not yet frozen.

## BoomMSHRFile.meta_write_arb

- Candidate axioms: 12; trusted axioms: 12; unresolved: 0.
- `A1` proves exact same-cycle one-hot conservation from the two input handshakes to the output handshake.
- `A2` proves input-0 priority exclusion.
- `A3`–`A12` prove conditional forwarding of every exposed payload leaf through exact last-connect/`when` driver reconstruction.
- Status: `FROZEN_FOR_COMPOSITION`.

## BoomMSHRFile.meta_read_arb

- Candidate axioms: 8; trusted axioms: 8; unresolved: 0.
- The same generic occurrence-partition, priority-exclusion, and conditional payload-forwarding rules certify the three-field metadata read arbiter without module-specific logic.
- Status: `FROZEN_FOR_COMPOSITION`.

## BoomMSHRFile.mmio_alloc_arb

- Candidate axioms: 2; trusted axioms: 2; unresolved: 0.
- The one-input arbiter is modeled as a singleton occurrence partition, reducing exactly to `OutputFire <=> InputFire`, plus conditional payload equality.
- Status: `FROZEN_FOR_COMPOSITION`.

## Current phase

Manual Bootstrap, Week-1 style objective: continue the representative L1 bottom-up chain. ProbeUnit, WritebackUnit, `BoomMSHR.rpq.main`, and the composite `BoomMSHR.rpq` are frozen and may be consumed by later parent composition.

Current semantic target: the next unfinished `BoomMSHRFile` child/parent WorkUnit.

Next Action: audit direct-child freeze readiness for `BoomMSHRFile`, freeze any already validated prerequisite such as `BoomMSHR` when appropriate, then export the next planner-selected task.

---

## Recent WorkUnit Runs

### Run: `leaf_abstraction-LSU-state-0-9-943f5c2db0171922`

# Run Summary — LSU::state-0-9

## Identity

- task: `leaf_abstraction-LSU-state-0-9-943f5c2db0171922`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.14`
- schema: `umcm-formal-0.5`
- workflow status: `VALIDATION_INCOMPLETE`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
- candidate axioms: 0
- unresolved: 1

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 0
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 0
- formal backend: `explicit-control`

## Unresolved

- `U1` Grounding gap: the complete priority-guarded next-state relation for ldq_tail cannot be instantiated because the handoff exposes writer 7874 (ldq_tail := io.core.brupdate.b2.uop.ldq_idx) and writer 8104 (ldq_tail := 0) …

## Next action

Review unresolved/partial structural obligations and then run a real formal backend.

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

### Run: `leaf_abstraction-LSU-state-0-10-75fa875f7278b61a`

# Run Summary — LSU::state-0-10

## Identity

- task: `leaf_abstraction-LSU-state-0-10-75fa875f7278b61a`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.13`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 1
- predicates: 4
- identity keys: 0
- cases: 1
- candidate axioms: 5
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 5
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 5
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] after 1 cycle(s), bits(stq_clr_head_idx, 2, 0) = select_cyclic_successor(stq_clr_head_idx_head_base), pivot=first(index_cases(i; _stq_clr_head_idx_T_1, _stq_clr_head_idx_T_3, _stq_clr_head_idx_T_5, _stq_clr_head_idx_T_7…
- `A2` [FORMALLY_PROVED] ClearGateClosed => !StoreClear
- `A3` [FORMALLY_PROVED] SelectedIsAMO => !StoreClear
- `A4` [FORMALLY_PROVED] SelectedAlreadyCleared => !StoreClear
- `A5` [FORMALLY_PROVED] SelectedControlBlocked => !StoreClear

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

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

### Run: `leaf_abstraction-LSU-region-0-0-95a6c27af3e9b19f`

# Run Summary — LSU::region-0-0

## Identity

- task: `leaf_abstraction-LSU-region-0-0-95a6c27af3e9b19f`
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
- predicates: 2
- identity keys: 0
- cases: 1
- candidate axioms: 3
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 3
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 3
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] NoRegisteredClear => !ClearBusy
- `A2` [FORMALLY_PROVED] OutputControlBlocked => !ClearBusy
- `A3` [FORMALLY_PROVED] io.core.clr_bsy[0].bits = clr_uop_1.rob_idx on ClearBusy

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

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

### Run: `leaf_abstraction-LSU-region-0-3-085cd341e222b4b9`

# Run Summary — LSU::region-0-3

## Identity

- task: `leaf_abstraction-LSU-region-0-3-085cd341e222b4b9`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.12`
- schema: `umcm-formal-0.5`
- workflow status: `PENDING_MANUAL_LLM`

## Next action

Send prompt.md to a ChatGPT conversation, converge on a candidate, then import the final response.

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

### Run: `leaf_abstraction-LSU-region-0-2-960be9077011ec48`

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

### Run: `leaf_abstraction-LSU.retry_queue-4e9eb249feec6033`

# Run Summary — LSU.retry_queue

## Identity

- task: `leaf_abstraction-LSU.retry_queue-4e9eb249feec6033`
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

- occurrences: 7
- predicates: 6
- identity keys: 0
- cases: 5
- candidate axioms: 12
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 12
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 12
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] QueueFull => !EnqHandshake
- `A2` [FORMALLY_PROVED] EnqHandshake <=> exactly_one_same_cycle({QueueInsert, BranchKilledEnqueue, FlushKilledEnqueue})
- `A3` [FORMALLY_PROVED] IncomingBranchKilled => !QueueInsert
- `A4` [FORMALLY_PROVED] IncomingFlushKilled => !QueueInsert
- `A5` [FORMALLY_PROVED] QueueEmpty => !HeadAdvance
- `A6` [FORMALLY_PROVED] HeadAdvance <=> exactly_one_same_cycle({DeqHandshake, InvalidHeadSkip})
- `A7` [FORMALLY_PROVED] HeadInvalid => !DeqHandshake
- `A8` [FORMALLY_PROVED] HeadValid => !InvalidHeadSkip
- `A9` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A10` [FORMALLY_PROVED] QueueInsert <mu DeqHandshake [same index slot]
- `A11` [FORMALLY_PROVED] QueueInsert <mu InvalidHeadSkip [same index slot]
- `A12` [FORMALLY_PROVED] io.deq.bits = out on DeqHandshake

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

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

### Run: `leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121`

# Run Summary — LSU.stq_execute_queue

## Identity

- task: `leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.12`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 3
- predicates: 2
- identity keys: 0
- cases: 2
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

- `A1` [FORMALLY_PROVED] QueueFull => !EnqHandshake
- `A2` [FORMALLY_PROVED] QueueEmpty => !DeqHandshake
- `A3` [FORMALLY_PROVED] EnqHandshake <=> exactly_one_same_cycle({QueueInsert})
- `A4` [FORMALLY_PROVED] MPORT = io.enq.bits on QueueInsert
- `A5` [FORMALLY_PROVED] QueueInsert <mu DeqHandshake [same index slot]
- `A6` [FORMALLY_PROVED] io.deq.bits = io_deq_bits_MPORT on DeqHandshake

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

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

### Run: `leaf_abstraction-LSU.logic-e41a1cc2550d9194`

# Run Summary — LSU.logic

## Identity

- task: `leaf_abstraction-LSU.logic-e41a1cc2550d9194`
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

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
- candidate axioms: 1
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 1
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 1
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] after 1 cycle(s), {io.found, io.found_idx} = select_cyclic_predecessor(io.youngest), pivot=last(bits(io.matches, i, i), i in [0, 8))

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

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

### Run: `leaf_abstraction-LSU-region-0-4-9d9375b011581ad1`

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

### Run: `leaf_abstraction-LSU-state-0-8-75c1d44ef5da10a6`

# Run Summary — LSU::state-0-8

## Identity

- task: `leaf_abstraction-LSU-state-0-8-75c1d44ef5da10a6`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 5
- predicates: 5
- identity keys: 0
- cases: 4
- candidate axioms: 5
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 5
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 5
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] LoadSearch <=> exactly_one_same_cycle({LoadSearchPass, LoadSearchNonForwardable, LoadSearchConflictBlocked})
- `A2` [FORMALLY_PROVED] ForwardingKilled => !LoadSearchPass
- `A3` [FORMALLY_PROVED] ForwardingDisallowed => !LoadSearchPass
- `A4` [FORMALLY_PROVED] HasOlderAMOOrFence => !LoadSearchPass
- `A5` [FORMALLY_PROVED] NackOrderingConflict => !LoadSearchPass

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

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

### Run: `leaf_abstraction-LSU-region-0-6-664eff0e43733fd6`

# Run Summary — LSU::region-0-6

## Identity

- task: `leaf_abstraction-LSU-region-0-6-664eff0e43733fd6`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 7
- predicates: 5
- identity keys: 0
- cases: 0
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

- `A1` [FORMALLY_PROVED] DCacheRequest <=> exactly_one_same_cycle({LoadExecuteRequest, LoadRetryRequest, StoreCommitRequest, LoadWakeupRequest, HellaIncomingRequest, HellaWakeupRequest})
- `A2` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on LoadExecuteRequest
- `A3` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on LoadRetryRequest
- `A4` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = stq_execute_queue.io.deq.bits.addr.bits on StoreCommitRequest
- `A5` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = ldq_wakeup_e.bits.addr.bits on LoadWakeupRequest
- `A6` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on HellaIncomingRequest
- `A7` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = hella_paddr on HellaWakeupRequest
- `A8` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadExecuteRequest
- `A9` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadRetryRequest
- `A10` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on StoreCommitRequest
- `A11` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadWakeupRequest
- `A12` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 1 on HellaIncomingRequest
- `A13` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 1 on HellaWakeupRequest
- `A14` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_cmd = hella_req.cmd on HellaIncomingRequest
- `A15` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_cmd = hella_req.cmd on HellaWakeupRequest
- `A16` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_size = hella_req.size on HellaIncomingRequest
- `A17` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_size = hella_req.size on HellaWakeupRequest
- `A18` [FORMALLY_PROVED] RetryOrderBlock => !LoadRetryRequest
- `A19` [FORMALLY_PROVED] WakeupOrderBlock => !LoadWakeupRequest
- `A20` [FORMALLY_PROVED] UncacheableWakeupOrderBlocked => !LoadWakeupRequest

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

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

### Run: `leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510`

# Run Summary — LSU::region-0-1

## Identity

- task: `leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 4
- predicates: 2
- identity keys: 0
- cases: 2
- candidate axioms: 4
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 4
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 4
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] ClearUnsafe <=> exactly_one_same_cycle({ClearUnsafeWithStorePending, ClearUnsafeLoadOnly})
- `A2` [FORMALLY_PROVED] DelayedFailedLoad => !ClearUnsafe
- `A3` [FORMALLY_PROVED] DCacheNack => !ClearUnsafeLoadOnly
- `A4` [FORMALLY_PROVED] io.core.clr_unsafe[0].bits = io_core_clr_unsafe_0_bits_REG on ClearUnsafe

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

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
