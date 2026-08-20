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
