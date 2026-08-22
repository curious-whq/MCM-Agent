Current Formal AST is sufficient.

## FINAL MCM-AGENT RESULT

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-state-0-13-6709bdbe9122e581",
  "work_unit_id": "LSU::state-0-13",
  "occurrences": [],
  "predicates": [],
  "identity_keys": [],
  "cases": [],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "register_transition",
        "register": "stq_tail",
        "width": 4,
        "updates": [
          {
            "guard": {
              "op": "signal",
              "name": "_T_1151"
            },
            "next": {
              "op": "const",
              "value": 0
            }
          },
          {
            "guard": {
              "op": "signal",
              "name": "_T_1092"
            },
            "next": {
              "op": "signal",
              "name": "io.core.brupdate.b2.uop.stq_idx"
            }
          },
          {
            "guard": {
              "op": "signal",
              "name": "dis_st_val"
            },
            "next": {
              "op": "modular_increment",
              "value": {
                "op": "signal",
                "name": "stq_tail"
              },
              "modulus": 16
            }
          }
        ],
        "priority": "first_match",
        "default": {
          "op": "signal",
          "name": "stq_tail"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        163,
        164,
        165,
        283,
        284,
        285,
        286,
        313,
        7873,
        8108
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "Complete one-cycle next-state semantics of the STQ allocation tail. Reset dominates branch-recovery redirect, which dominates ordinary store dispatch advancement; otherwise the pointer holds."
  ],
  "extensions": {}
}
```
