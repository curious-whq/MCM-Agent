Current Formal AST is sufficient.

## FINAL MCM-AGENT RESULT

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU.bkptu_0-ffd98bc059e3be37",
  "work_unit_id": "LSU.bkptu_0",
  "occurrences": [],
  "predicates": [],
  "identity_keys": [],
  "cases": [],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.xcpt_if"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.xcpt_ld"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        4
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.xcpt_st"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        5
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.debug_if"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        6
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.debug_ld"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.debug_st"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        8
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This SmallBoom configuration instantiates BreakpointUnit with no active breakpoint entries; all six exception/debug outputs are wired to zero.",
    "The six one-bit constants are preserved because they are cheap exact parent-facing facts and establish that this leaf cannot inject breakpoint exceptions or debug stops into the LSU in this configuration.",
    "No event, state, ordering, identity, or liveness claim is needed."
  ],
  "extensions": {}
}
```
