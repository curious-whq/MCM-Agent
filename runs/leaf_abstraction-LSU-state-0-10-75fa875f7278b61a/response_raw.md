{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-state-0-10-75fa875f7278b61a",
  "work_unit_id": "LSU::state-0-10",
  "occurrences": [
    {
      "id": "StoreClear",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "_T_233; the currently selected STQ entry satisfies the clear gate and its stq_cleared bit is set",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "expr": {
          "op": "slice",
          "value": {
            "op": "signal",
            "name": "stq_clr_head_idx"
          },
          "hi": 2,
          "lo": 0
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "_T_233"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        3424,
        3427,
        3428,
        3430,
        3432,
        3434,
        3435,
        3436,
        3437,
        3438,
        3439,
        3440,
        3441,
        3442,
        3443,
        3444,
        3445,
        3453,
        3454
      ]
    }
  ],
  "predicates": [
    {
      "id": "ClearGateClosed",
      "definition": "the complete selected-entry clear condition _T_233 is false",
      "grounding": {
        "source_signal": "_T_233",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3434,
        3435,
        3436,
        3437,
        3438,
        3439,
        3440,
        3441,
        3442,
        3443,
        3444,
        3445
      ]
    },
    {
      "id": "SelectedIsAMO",
      "definition": "the uop of the currently selected STQ slot is an AMO",
      "grounding": {
        "source_signal": "s_uop.is_amo",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3435,
        3436
      ]
    },
    {
      "id": "SelectedAlreadyCleared",
      "definition": "the currently selected STQ slot already has stq_cleared asserted",
      "grounding": {
        "source_signal": "_T_227",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3437,
        3438,
        3439
      ]
    },
    {
      "id": "SelectedControlBlocked",
      "definition": "the selected store uop is killed by the current branch mispredict mask or io.core.exception",
      "grounding": {
        "source_signal": "_T_231",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3440,
        3441,
        3442,
        3443,
        3444
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_StoreClear",
      "trigger_occurrences": [
        "StoreClear"
      ],
      "guard_predicates": [
        {
          "id": "ClearGateClosed",
          "positive": false
        },
        {
          "id": "SelectedIsAMO",
          "positive": false
        },
        {
          "id": "SelectedAlreadyCleared",
          "positive": false
        },
        {
          "id": "SelectedControlBlocked",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "The low three bits of stq_clr_head_idx identify the STQ slot whose stq_cleared state is set. The selected store must satisfy the complete clear gate, including non-AMO, not-already-cleared and branch/core-exception survival conditions."
      ],
      "evidence_statement_ids": [
        3424,
        3427,
        3428,
        3430,
        3432,
        3434,
        3435,
        3436,
        3437,
        3438,
        3439,
        3440,
        3441,
        3442,
        3443,
        3444,
        3445,
        3453,
        3454
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "indexed_priority_select",
        "index": {
          "name": "i",
          "count": 8
        },
        "candidate": {
          "op": "indexed_cases",
          "index": {
            "op": "index_var",
            "name": "i"
          },
          "values": [
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_1"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_3"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_5"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_7"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_9"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_11"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_13"
            },
            {
              "op": "signal",
              "name": "_stq_clr_head_idx_T_15"
            }
          ]
        },
        "priority": {
          "kind": "cyclic_successor",
          "pivot": {
            "op": "signal",
            "name": "stq_clr_head_idx_head_base"
          },
          "pivot_position": "first"
        },
        "result": {
          "index": {
            "op": "slice",
            "value": {
              "op": "signal",
              "name": "stq_clr_head_idx"
            },
            "hi": 2,
            "lo": 0
          }
        },
        "latency_cycles": 1,
        "initialization": {
          "kind": "implicit_unconstrained"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3369,
        3370,
        3371,
        3372,
        3373,
        3374,
        3375,
        3376,
        3377,
        3378,
        3379,
        3380,
        3381,
        3382,
        3383,
        3384,
        3385,
        3386,
        3387,
        3388,
        3389,
        3390,
        3391,
        3392,
        3393,
        3394,
        3395,
        3396,
        3397,
        3398,
        3399,
        3400,
        3401,
        3402,
        3403,
        3404,
        3406
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreClear",
        "predicate": "ClearGateClosed",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_StoreClear"
      ],
      "evidence_statement_ids": [
        3444,
        3445,
        3453,
        3454
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreClear",
        "predicate": "SelectedIsAMO",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_StoreClear"
      ],
      "evidence_statement_ids": [
        3435,
        3436,
        3439,
        3444,
        3445,
        3454
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreClear",
        "predicate": "SelectedAlreadyCleared",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_StoreClear"
      ],
      "evidence_statement_ids": [
        3437,
        3438,
        3439,
        3444,
        3445,
        3454
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreClear",
        "predicate": "SelectedControlBlocked",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_StoreClear"
      ],
      "evidence_statement_ids": [
        3440,
        3441,
        3442,
        3443,
        3444,
        3445,
        3454
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This WorkUnit has no physical boundary events. StoreClear is retained as a derived memory-order-relevant milestone because it changes the persistent per-STQ-entry stq_cleared state and therefore affects which stores remain eligible for subsequent clearing/progress.",
    "A1 uses the prompt-0.13 indexed_cases form because lowering exposes the eight selector candidates as separate scalar frontier signals rather than exposing the source-level stq_valid array inside this WorkUnit. The candidate list therefore preserves the planner partition boundary instead of illegally referring to stq_valid.",
    "The eight indexed_cases values correspond to the eight lowered eligibility signals consumed by the age-priority network: _stq_clr_head_idx_T_1, _T_3, _T_5, _T_7, _T_9, _T_11, _T_13 and _T_15.",
    "The RTL AgePriorityEncoder scans from the current head base itself toward increasing indices and then wraps to zero. A1 therefore uses cyclic_successor with pivot_position first, not the strict/default pivot-last successor semantics.",
    "stq_clr_head_idx is produced by SafeRegNext, so the selected index is exposed one cycle after the candidate vector and head pivot are sampled. latency_cycles is therefore exactly one.",
    "stq_clr_head_idx contains an additional overflow/epoch bit, but every clear-path lookup in this WorkUnit uses only bits [2:0]. A1 therefore constrains the selected result through the constant slice stq_clr_head_idx[2:0]; the epoch bit is intentionally omitted because it does not affect which physical STQ slot is cleared here.",
    "SafeRegNext uses an unreset register in the supplied evidence. The selector result therefore uses implicit_unconstrained initialization rather than inventing a reset index.",
    "The selector does not expose a separate found/nonempty signal. result.found is therefore omitted as allowed by prompt-0.13. No claim is made that a candidate necessarily exists in every cycle.",
    "StoreClear is indexed by the low three bits of the registered selector result. When _T_233 is true, statement 3454 writes one to stq_cleared at exactly that selected physical slot.",
    "A2 preserves the complete clear gate collectively. A3-A5 additionally retain three semantically important reasons that independently prohibit clearing: the selected uop is an AMO, the selected slot is already cleared, or the uop is killed by branch misprediction/core exception.",
    "The remaining address/data/physical-address prerequisites inside _T_233 are not split into separate exported predicates. A2 still preserves their combined exclusion exactly through ClearGateClosed, while omitting their individual names keeps the abstraction small.",
    "Statement 275 can reset stq_cleared for a dispatched STQ index, but this WorkUnit does not contain the complete trigger cone for that write. No synthetic reset occurrence is invented. Omitting that additional state transition from the parent-facing event vocabulary is a safe over-approximation and may be refined later through CEGAR.",
    "No ordering claim is made from a particular candidate-producing store transaction to StoreClear beyond the exact indexed selector relation. The supplied region does not itself establish a globally unique ROB/STQ transaction identity suitable for an identity_key.",
    "No fairness, eventual-clear, or eventual-store-progress property is claimed."
  ],
  "extensions": {}
}
