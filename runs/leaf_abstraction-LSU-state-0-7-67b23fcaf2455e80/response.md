Current Formal AST is sufficient.

## FINAL MCM-AGENT RESULT

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-state-0-7-67b23fcaf2455e80",
  "work_unit_id": "LSU::state-0-7",
  "occurrences": [],
  "predicates": [],
  "identity_keys": [],
  "cases": [],
  "axioms": [],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "REG is a one-cycle helper used only by assertion/debug instrumentation around the memory-exception check; the owned cone does not drive a functional LSU boundary event or memory/coherence state transition.",
    "This leaf is therefore intentionally an explicit empty µMCM over-approximation. The concrete helper register remains unconstrained at the parent boundary and can be reopened by CEGAR, but no functional memory-ordering behavior is excluded."
  ],
  "extensions": {}
}
```
