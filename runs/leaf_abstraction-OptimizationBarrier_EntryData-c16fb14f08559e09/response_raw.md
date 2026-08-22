{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-OptimizationBarrier_EntryData-c16fb14f08559e09",
  "work_unit_id": "OptimizationBarrier_EntryData",
  "occurrences": [],
  "predicates": [],
  "identity_keys": [],
  "cases": [],
  "axioms": [],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This WorkUnit is a covered stateless combinational OptimizationBarrier with no physical boundary events, no registers, and no mutable memory state.",
    "Its only behavioral statement is the exact aggregate combinational connection io.y := io.x.",
    "The parent-facing frontier exposes only io.y fields. The corresponding io.x source fields are not exposed by this WorkUnit, so adding signal_equality axioms that reference io.x would cross the static WorkUnit abstraction boundary.",
    "Leaving the io.y fields unconstrained is a safe over-approximation: it admits additional behaviors while excluding no concrete RTL behavior.",
    "The EntryData fields may carry translation or permission information used by an enclosing TLB/PMP component, but this OptimizationBarrier itself introduces no memory ordering, visibility, arbitration, identity, or state-transition semantics.",
    "If a later parent/system counterexample requires exact preservation of EntryData through this barrier, the leaf can be reopened by CEGAR or the source-side io.x fields can be exposed explicitly by the static interface.",
    "No fairness or liveness assumption is applicable."
  ],
  "extensions": {}
}