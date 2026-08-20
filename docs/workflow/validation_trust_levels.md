# µMCM validation trust levels

MCM-Agent deliberately separates candidate discovery from trust.

```text
LLM candidate
  -> GROUNDED
  -> deterministic structural evidence
  -> STRUCTURALLY_SUPPORTED / PARTIALLY_SUPPORTED / REFUTED
  -> formal backend
  -> FORMALLY_PROVED
  -> optional reference/protocol equivalence
  -> SPEC_PROVED
```

Only `FORMALLY_PROVED` and `SPEC_PROVED` axioms may constrain a parent through
`trusted_umcm.json`. Grounding and structural evidence never promote an axiom to
trusted status.

This policy makes an incomplete µMCM an over-approximation: missing constraints
may create spurious system-level counterexamples, which are later refined by
checking the counterexample against concrete RTL. The workflow does not try to
prove abstraction completeness up front.

Bundled backends:

- `none`: fail-closed; never promotes an axiom.
- `explicit-control`: proves certified finite-control/order obligations by exhaustive
  reachability, exact symbolic local/identity projections, exact constants/aliases,
  and selected finite reference-equivalence checks such as TileLink
  `ClientMetadata.onProbe`. It is not a general-purpose SMT/bit-level RTL prover.

A fully trusted leaf with no unresolved items can be explicitly frozen with:

```bash
python3 -m workflow.cli freeze runs/<task-id>
```

This writes `frozen_umcm.json` and changes the run status to
`FROZEN_FOR_COMPOSITION`. Frozen summaries may still be reopened later by CEGAR
if a spurious parent/system counterexample exposes a missing constraint.
