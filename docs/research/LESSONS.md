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
