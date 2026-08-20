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
