{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510",
  "work_unit_id": "LSU::region-0-1",
  "occurrences": [
    {
      "id": "ClearUnsafe",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.core.clr_unsafe[0].valid"
      ],
      "definition": "io.core.clr_unsafe[0].valid; the LSU notifies the core that the tracked memory operation may clear its unsafe status",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.clr_unsafe[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6093,
        6094,
        6095,
        6096,
        6097,
        6098,
        6101,
        6103,
        6104,
        6105,
        6107,
        6108,
        6109,
        6110
      ]
    },
    {
      "id": "ClearUnsafeWithStorePending",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.core.clr_unsafe[0].valid && io_core_clr_unsafe_0_valid_REG; a clear-unsafe notification while the delayed store-search contribution is present",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.clr_unsafe[0].valid",
          "io_core_clr_unsafe_0_valid_REG"
        ],
        "signals_false": [
          "io_core_clr_unsafe_0_valid_REG_3"
        ]
      },
      "evidence_statement_ids": [
        6093,
        6105,
        6107,
        6108,
        6109,
        6110
      ]
    },
    {
      "id": "ClearUnsafeLoadOnly",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.core.clr_unsafe[0].valid && !io_core_clr_unsafe_0_valid_REG; a clear-unsafe notification whose surviving source is the delayed qualified load-search path",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.clr_unsafe[0].valid",
          "io_core_clr_unsafe_0_valid_REG_2"
        ],
        "signals_false": [
          "io_core_clr_unsafe_0_valid_REG",
          "io.dmem.nack[0].valid",
          "io_core_clr_unsafe_0_valid_REG_3"
        ]
      },
      "evidence_statement_ids": [
        6094,
        6095,
        6096,
        6097,
        6098,
        6101,
        6103,
        6104,
        6105,
        6107,
        6108,
        6109,
        6110
      ]
    },
    {
      "id": "Stage1Kill",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.dmem.s1_kill[0] is asserted; the LSU cancels the memory request currently occupying DCache stage 1",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.dmem.s1_kill[0]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2377,
        3984,
        4130,
        4276,
        4422,
        4568,
        4714,
        4860,
        5006,
        5086,
        5962
      ]
    }
  ],
  "predicates": [
    {
      "id": "DelayedFailedLoad",
      "definition": "io_core_clr_unsafe_0_valid_REG_3 is asserted; failed_load from the preceding pipeline stage is retained and suppresses clear-unsafe",
      "grounding": {
        "source_signal": "io_core_clr_unsafe_0_valid_REG_3",
        "negated": false,
        "state_register": "io_core_clr_unsafe_0_valid_REG_3",
        "state_values": [
          1
        ]
      },
      "evidence_statement_ids": [
        6107,
        6108,
        6109,
        6110
      ]
    },
    {
      "id": "DCacheNack",
      "definition": "io.dmem.nack[0].valid is asserted",
      "grounding": {
        "source_signal": "io.dmem.nack[0].valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6094,
        6104
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_ClearWithStorePending",
      "trigger_occurrences": [
        "ClearUnsafeWithStorePending"
      ],
      "guard_predicates": [
        {
          "id": "DelayedFailedLoad",
          "positive": false
        }
      ],
      "emits": [
        "ClearUnsafe"
      ],
      "relations": [
        "The delayed store-search contribution can directly produce clear-unsafe and is not blocked by the current DCache nack input."
      ],
      "evidence_statement_ids": [
        6093,
        6105,
        6107,
        6108,
        6109,
        6110
      ],
      "confidence": "high"
    },
    {
      "id": "C2_ClearLoadOnly",
      "trigger_occurrences": [
        "ClearUnsafeLoadOnly"
      ],
      "guard_predicates": [
        {
          "id": "DelayedFailedLoad",
          "positive": false
        },
        {
          "id": "DCacheNack",
          "positive": false
        }
      ],
      "emits": [
        "ClearUnsafe"
      ],
      "relations": [
        "When no delayed store-search contribution is present, clear-unsafe can arise from the delayed qualified load-search path only when the current DCache request is not nacked."
      ],
      "evidence_statement_ids": [
        6094,
        6095,
        6096,
        6097,
        6098,
        6101,
        6103,
        6104,
        6105,
        6107,
        6108,
        6109,
        6110
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "ClearUnsafe",
        "parts": [
          "ClearUnsafeWithStorePending",
          "ClearUnsafeLoadOnly"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearWithStorePending",
        "C2_ClearLoadOnly"
      ],
      "evidence_statement_ids": [
        6093,
        6094,
        6095,
        6096,
        6097,
        6098,
        6101,
        6103,
        6104,
        6105,
        6107,
        6108,
        6109,
        6110
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ClearUnsafe",
        "predicate": "DelayedFailedLoad",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearWithStorePending",
        "C2_ClearLoadOnly"
      ],
      "evidence_statement_ids": [
        6107,
        6108,
        6109,
        6110
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ClearUnsafeLoadOnly",
        "predicate": "DCacheNack",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ClearLoadOnly"
      ],
      "evidence_statement_ids": [
        6094,
        6104,
        6105,
        6109,
        6110
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "ClearUnsafe",
        "target": "io.core.clr_unsafe[0].bits",
        "source": {
          "op": "signal",
          "name": "io_core_clr_unsafe_0_bits_REG"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ClearWithStorePending",
        "C2_ClearLoadOnly"
      ],
      "evidence_statement_ids": [
        6113
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "ClearUnsafe is the only physical boundary event in this WorkUnit and is memory-order relevant because it informs the core that an outstanding memory operation no longer needs to remain marked unsafe.",
    "The RTL computes clear-unsafe from two delayed contributors. io_core_clr_unsafe_0_valid_REG captures do_st_search[0]. io_core_clr_unsafe_0_valid_REG_2 captures a qualified load-search condition that already requires do_ld_search[0], no newly fired load address-generation operation, no stage-1 DCache kill, and an additional retained qualification bit.",
    "The two natural contributors can both be present in the same cycle. A1 therefore does not pretend they are intrinsically exclusive sources: it uses the exact Boolean decomposition 'store-pending' versus the residual 'no-store-pending/load-only' case, producing a genuine same-cycle partition.",
    "A2 preserves the final failed-load suppression. A delayed failed_load unconditionally prevents io.core.clr_unsafe[0].valid, regardless of which search path would otherwise request the notification.",
    "A3 preserves the asymmetry between the two paths: a current DCache nack suppresses the load-only clear path, while the delayed store-search contribution can still generate ClearUnsafe.",
    "A4 preserves the exact clr_unsafe payload value by tying it to io_core_clr_unsafe_0_bits_REG. The supplied ledger does not contain the assignment that originally establishes the semantic meaning of that retained payload register, so no stronger transaction-identity interpretation is invented.",
    "Stage1Kill is retained as an internal semantic occurrence even though it is not a planner-recognized physical handshake. Cancelling a request already resident in DCache stage 1 can change which memory operation becomes externally visible, so deleting this milestone would lose ordering/path information.",
    "The many individual disambiguation conditions that can assert Stage1Kill are deliberately not enumerated as separate cases or axioms. Leaving the cause of Stage1Kill less constrained is a safe over-approximation while preserving the kill event itself.",
    "No relation is asserted between the current-cycle Stage1Kill occurrence and ClearUnsafeLoadOnly. The latter is driven by a registered qualification containing an earlier s1_kill observation, so a same-cycle exclusion would be incorrect.",
    "No identity_key is introduced. Although clr_unsafe carries a payload, the available FIRRTL evidence only proves that the output equals io_core_clr_unsafe_0_bits_REG and does not ground what architectural or queue identity that register represents.",
    "No liveness or eventual-clear property is claimed."
  ],
  "extensions": {}
}