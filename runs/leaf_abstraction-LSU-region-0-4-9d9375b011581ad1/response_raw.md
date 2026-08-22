{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-4-9d9375b011581ad1",
  "work_unit_id": "LSU::region-0-4",
  "occurrences": [
    {
      "id": "ExceptionRegister",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "_r_xcpt_valid_T_5; a surviving load-side or memory exception is selected and written into the r_xcpt pipeline register",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "_r_xcpt_valid_T_5"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6190,
        6191,
        6192,
        6193,
        6194,
        6195,
        6196
      ]
    },
    {
      "id": "MemExceptionRegister",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "_r_xcpt_valid_T_5 && use_mem_xcpt; the exception selected for r_xcpt comes from the memory/TLB exception candidate",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "_r_xcpt_valid_T_5",
          "use_mem_xcpt"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6181,
        6182,
        6183,
        6184,
        6185,
        6186,
        6187,
        6188,
        6189,
        6190,
        6191,
        6192,
        6193,
        6194,
        6195,
        6196,
        6201
      ]
    },
    {
      "id": "LoadExceptionRegister",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "_r_xcpt_valid_T_5 && !use_mem_xcpt; the exception selected for r_xcpt comes from the load-side exception candidate",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "_r_xcpt_valid_T_5"
        ],
        "signals_false": [
          "use_mem_xcpt"
        ]
      },
      "evidence_statement_ids": [
        6131,
        6181,
        6182,
        6183,
        6184,
        6185,
        6186,
        6187,
        6188,
        6189,
        6190,
        6191,
        6192,
        6193,
        6194,
        6195,
        6196,
        6201
      ]
    },
    {
      "id": "LoadExceptionVisible",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.core.lxcpt.valid"
      ],
      "definition": "io.core.lxcpt.valid; a registered LSU exception is exposed to the core",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.lxcpt.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6204,
        6205,
        6206,
        6207,
        6208,
        6209,
        6210
      ]
    }
  ],
  "predicates": [
    {
      "id": "NoMemExceptionPending",
      "definition": "mem_xcpt_valid is false",
      "grounding": {
        "source_signal": "mem_xcpt_valid",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6186,
        6188,
        6190
      ]
    },
    {
      "id": "NoLoadExceptionPending",
      "definition": "ld_xcpt_valid is false",
      "grounding": {
        "source_signal": "ld_xcpt_valid",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6131,
        6187,
        6188,
        6190
      ]
    },
    {
      "id": "RegisterControlBlocked",
      "definition": "the currently selected exception is killed by the matching branch misprediction or by io.core.exception before being registered",
      "grounding": {
        "source_signal": "_r_xcpt_valid_T_3",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6191,
        6192,
        6193,
        6194,
        6195
      ]
    },
    {
      "id": "NoRegisteredException",
      "definition": "r_xcpt_valid is false",
      "grounding": {
        "source_signal": "r_xcpt_valid",
        "negated": true,
        "state_register": "r_xcpt_valid",
        "state_values": [
          0
        ]
      },
      "evidence_statement_ids": [
        6196,
        6208,
        6209
      ]
    },
    {
      "id": "OutputControlBlocked",
      "definition": "the registered exception is suppressed at the core interface by a matching branch misprediction or io.core.exception",
      "grounding": {
        "source_signal": "_io_core_lxcpt_valid_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6204,
        6205,
        6206,
        6207,
        6208,
        6209
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_MemExceptionSelected",
      "trigger_occurrences": [
        "MemExceptionRegister"
      ],
      "guard_predicates": [
        {
          "id": "NoMemExceptionPending",
          "positive": false
        },
        {
          "id": "RegisterControlBlocked",
          "positive": false
        }
      ],
      "emits": [
        "ExceptionRegister"
      ],
      "relations": [
        "The selected exception uop comes from mem_xcpt_uop and its exception cause comes from mem_xcpt_cause."
      ],
      "evidence_statement_ids": [
        2176,
        2177,
        2178,
        6181,
        6182,
        6183,
        6184,
        6185,
        6186,
        6187,
        6188,
        6189,
        6190,
        6191,
        6192,
        6193,
        6194,
        6195,
        6201
      ],
      "confidence": "high"
    },
    {
      "id": "C2_LoadExceptionSelected",
      "trigger_occurrences": [
        "LoadExceptionRegister"
      ],
      "guard_predicates": [
        {
          "id": "NoLoadExceptionPending",
          "positive": false
        },
        {
          "id": "RegisterControlBlocked",
          "positive": false
        }
      ],
      "emits": [
        "ExceptionRegister"
      ],
      "relations": [
        "The selected exception uop comes from ld_xcpt_uop and the registered cause-selection expression is the fixed value 16."
      ],
      "evidence_statement_ids": [
        6131,
        6187,
        6188,
        6189,
        6190,
        6191,
        6192,
        6193,
        6194,
        6195,
        6201
      ],
      "confidence": "high"
    },
    {
      "id": "C3_ExceptionVisible",
      "trigger_occurrences": [
        "LoadExceptionVisible"
      ],
      "guard_predicates": [
        {
          "id": "NoRegisteredException",
          "positive": false
        },
        {
          "id": "OutputControlBlocked",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "The core-visible exception is exactly the currently registered r_xcpt payload."
      ],
      "evidence_statement_ids": [
        6204,
        6205,
        6206,
        6207,
        6208,
        6209,
        6210
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "ExceptionRegister",
        "parts": [
          "MemExceptionRegister",
          "LoadExceptionRegister"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MemExceptionSelected",
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6189,
        6190,
        6195
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ExceptionRegister",
        "predicate": "RegisterControlBlocked",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MemExceptionSelected",
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6190,
        6191,
        6192,
        6193,
        6194,
        6195
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MemExceptionRegister",
        "predicate": "NoMemExceptionPending",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MemExceptionSelected"
      ],
      "evidence_statement_ids": [
        6186,
        6187,
        6188,
        6190,
        6195
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "LoadExceptionRegister",
        "predicate": "NoLoadExceptionPending",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6131,
        6187,
        6188,
        6190,
        6195
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "MemExceptionRegister",
        "target": "xcpt_uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "mem_xcpt_uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MemExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6189
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionRegister",
        "target": "xcpt_uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "ld_xcpt_uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6189
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "MemExceptionRegister",
        "target": "_r_xcpt_cause_T",
        "source": {
          "op": "signal",
          "name": "mem_xcpt_cause"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MemExceptionSelected"
      ],
      "evidence_statement_ids": [
        2176,
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "value_constraint",
        "on": "LoadExceptionRegister",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "_r_xcpt_cause_T"
          },
          "index": 4
        },
        "relation": "eq",
        "value": 1,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A8b",
      "formal": {
        "type": "value_constraint",
        "on": "LoadExceptionRegister",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "_r_xcpt_cause_T"
          },
          "index": 3
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A8c",
      "formal": {
        "type": "value_constraint",
        "on": "LoadExceptionRegister",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "_r_xcpt_cause_T"
          },
          "index": 2
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A8d",
      "formal": {
        "type": "value_constraint",
        "on": "LoadExceptionRegister",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "_r_xcpt_cause_T"
          },
          "index": 1
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A8e",
      "formal": {
        "type": "value_constraint",
        "on": "LoadExceptionRegister",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "_r_xcpt_cause_T"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadExceptionSelected"
      ],
      "evidence_statement_ids": [
        6188,
        6201
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "forbid_when",
        "occurrence": "LoadExceptionVisible",
        "predicate": "NoRegisteredException",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6208,
        6209
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "forbid_when",
        "occurrence": "LoadExceptionVisible",
        "predicate": "OutputControlBlocked",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6204,
        6205,
        6206,
        6207,
        6208,
        6209
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.cause",
        "source": {
          "op": "signal",
          "name": "r_xcpt.cause"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.badvaddr",
        "source": {
          "op": "signal",
          "name": "r_xcpt.badvaddr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "r_xcpt.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "r_xcpt.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "r_xcpt.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "LoadExceptionVisible",
        "target": "io.core.lxcpt.bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "r_xcpt.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_ExceptionVisible"
      ],
      "evidence_statement_ids": [
        6210
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region implements exception arbitration and a one-stage registered exception interface. The physical boundary occurrence is io.core.lxcpt.valid; ExceptionRegister is retained as an internal semantic milestone because it determines which memory exception can later become architecturally visible.",
    "A1 preserves the exact source split at the registration point. use_mem_xcpt chooses the memory exception path; its negation chooses the load-side exception path.",
    "The memory-versus-load selection is not a simple fixed priority. The RTL compares mem_xcpt_uop.rob_idx and ld_xcpt_uop.rob_idx relative to io.core.rob_head_idx, and selects the memory candidate when it is the older valid candidate or when no load exception exists.",
    "A2 preserves the first control-squash point: a branch misprediction matching the selected uop or io.core.exception prevents the candidate exception from being registered.",
    "A3 and A4 preserve that each selected registration path requires a valid candidate of the corresponding source.",
    "A5 and A6 preserve ROB identity at the combinational arbitration point without inventing a new cross-cycle identity object.",
    "A7 and A8-A8e preserve the source-dependent cause rule. A selected memory exception uses mem_xcpt_cause; a selected load-side exception uses the fixed 5-bit cause value 16 (binary 10000). The load-side constant is expressed bitwise because the current value_constraint AST only supports equality on one bit of one signal.",
    "A9 and A10 preserve the second output gate. A core-visible exception requires the registered-valid state and is again suppressed by a matching branch misprediction or io.core.exception.",
    "A11-A16 preserve the memory-relevant and identity-relevant projections of the registered exception payload exposed to the core: cause, bad virtual address, ROB index, LDQ index, STQ index, and memory command. The many unrelated MicroOp fields are intentionally omitted.",
    "No ordered_before relation is asserted from ExceptionRegister to LoadExceptionVisible. r_xcpt_valid is a concrete register, but the supplied WorkUnit contains no reset or initialization guarantee for that register; a global required-prior theorem could therefore incorrectly exclude an initially valid register state.",
    "For the same reason, no identity_key is used to connect a current ExceptionRegister source directly to a later LoadExceptionVisible event. The boundary ROB/LDQ/STQ projections remain available for higher-level composition without inventing ungrounded generation history.",
    "The exact internal construction of ld_xcpt_uop from the eight load-queue exception candidates is not fully present in this ledger. The candidate therefore preserves ld_xcpt_valid and the already-selected ld_xcpt_uop as grounded inputs to this region rather than guessing the per-entry winner.",
    "No liveness or eventual-exception-delivery property is claimed."
  ],
  "extensions": {}
}
