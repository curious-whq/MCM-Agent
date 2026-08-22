{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-0-95a6c27af3e9b19f",
  "work_unit_id": "LSU::region-0-0",
  "occurrences": [
    {
      "id": "ClearBusy",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.core.clr_bsy[0].valid"
      ],
      "definition": "io.core.clr_bsy[0].valid; the LSU tells the core that the ROB entry carried in bits may clear its busy state",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.clr_bsy[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        3459,
        3460,
        3461
      ]
    }
  ],
  "predicates": [
    {
      "id": "NoRegisteredClear",
      "definition": "clr_valid_1 is false; there is no registered clear-busy candidate in the current cycle",
      "grounding": {
        "source_signal": "clr_valid_1",
        "negated": true,
        "state_register": "clr_valid_1",
        "state_values": [
          0
        ]
      },
      "evidence_statement_ids": [
        3416,
        3459,
        3460
      ]
    },
    {
      "id": "OutputControlBlocked",
      "definition": "the registered clear-busy uop is killed in the current cycle because its branch mask intersects the mispredict mask or io.core.exception is asserted",
      "grounding": {
        "source_signal": "_io_core_clr_bsy_0_valid_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3455,
        3456,
        3457,
        3458,
        3459,
        3460
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_ClearBusyVisible",
      "trigger_occurrences": [
        "ClearBusy"
      ],
      "guard_predicates": [
        {
          "id": "NoRegisteredClear",
          "positive": false
        },
        {
          "id": "OutputControlBlocked",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "A core-visible clear-busy notification requires the registered clear candidate to remain valid after the current branch-mispredict/core-exception filter, and its payload identifies clr_uop_1.rob_idx."
      ],
      "evidence_statement_ids": [
        3455,
        3456,
        3457,
        3458,
        3459,
        3460,
        3461
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ClearBusy",
        "predicate": "NoRegisteredClear",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearBusyVisible"
      ],
      "evidence_statement_ids": [
        3459,
        3460
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ClearBusy",
        "predicate": "OutputControlBlocked",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearBusyVisible"
      ],
      "evidence_statement_ids": [
        3455,
        3456,
        3457,
        3458,
        3459,
        3460
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "signal_equality",
        "on": "ClearBusy",
        "target": "io.core.clr_bsy[0].bits",
        "source": {
          "op": "signal",
          "name": "clr_uop_1.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearBusyVisible"
      ],
      "evidence_statement_ids": [
        3461
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "ClearBusy is the only physical boundary occurrence in this WorkUnit. Its payload is the ROB index whose busy state is being cleared.",
    "A1 preserves the requirement that a visible clear-busy notification must have clr_valid_1 asserted in the current cycle.",
    "A2 preserves the second branch/core-exception suppression point. Even when clr_valid_1 is asserted, a current misprediction matching clr_uop_1.br_mask or io.core.exception prevents io.core.clr_bsy[0].valid.",
    "A3 preserves the exact identity projection visible at the boundary: io.core.clr_bsy[0].bits is clr_uop_1.rob_idx.",
    "The RTL also applies an earlier branch/core-exception filter before registering clr_valid_1: clr_valid_1 receives clr_valid && !IsKilledByBranch(..., clr_uop). clr_uop_1 simultaneously receives UpdateBrMask(clr_uop).",
    "That earlier stage is deliberately not exported as a separate occurrence because the current WorkUnit provides no reset or initialization guarantee for the RegNext registers clr_valid_1 and clr_uop_1. A global required-prior theorem from an earlier derived occurrence to every ClearBusy could therefore incorrectly exclude an initially unconstrained registered value.",
    "Omitting the first-stage causal history only widens the abstraction. It may allow a registered clear candidate without a modeled prior clr_valid event, but it does not remove a concrete RTL behavior and is therefore a safe CEGAR refinement point rather than an unresolved issue.",
    "The branch mask carried by clr_uop_1 is updated by removing resolved branch bits before the second kill check. This internal detail is retained implicitly through the exact OutputControlBlocked signal rather than exported as additional parent-facing state.",
    "No separate identity_key is required because this leaf has only one externally meaningful occurrence and A3 already preserves its ROB-index payload exactly.",
    "No liveness or eventual-clear property is claimed."
  ],
  "extensions": {}
}