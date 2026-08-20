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
