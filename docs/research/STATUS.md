# Current Project Status

## Static planner

- Real-BOOM hierarchical planner is implemented and validated on the uploaded SmallBoomV4Config FIRRTL.
- L1, L2 and LSU roots have recursive WorkUnit plans with complete coverage.

## Workflow

- Manual-first leaf task export/import is implemented.
- µMCM `umcm-formal-0.5` supports scalar/indexed boundary or derived occurrences, predicates, identity, cases, assumptions, generic join/indexed-completeness relations, and same-index relation scopes with indexed lookup expressions; prose formulas/validation programs are no longer semantic inputs.
- Grounding validation is deterministic and fail-closed; it rejects legacy `formula`/`validation` fields and unsupported Formal AST shapes.
- Validation trust levels distinguish grounding, structural support, formal proof and reference/spec proof.
- `explicit-control` backend proves certified finite-control/order properties, exact symbolic local/identity facts, selected finite reference equivalence checks, bounded monotone counter/index coverage, supported same-index pipeline/storage relations, sticky-state joins, and supported aggregate-mux constant properties.
- A fully proved leaf with no unresolved items can be frozen as `frozen_umcm.json` for parent composition; it remains reopenable by later CEGAR refinement.

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

## Current phase

Manual Bootstrap, Week-1 style objective: continue the representative L1 bottom-up chain. ProbeUnit and WritebackUnit are both frozen and may be consumed by later parent composition, but the larger L1 parent is not ready because other representative children remain unfinished.

Current semantic target: `BoomMSHR`.

Next Action: construct and validate the `BoomMSHR` leaf µMCM, reusing the existing transaction/occurrence/predicate/case/indexed-occurrence/same-index/join language. Extend the language or prover only when new RTL semantics require a reusable general abstraction; do not reopen ProbeUnit or WritebackUnit unless counterexample-guided refinement requires it.
