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
