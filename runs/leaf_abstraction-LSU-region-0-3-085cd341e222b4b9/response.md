{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-3-085cd341e222b4b9",
  "work_unit_id": "LSU::region-0-3",
  "occurrences": [
    {
      "id": "IntegerResponse",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.core.iresp[0].valid"
      ],
      "definition": "io.core.iresp[0].valid; one registered integer LSU response is visible to the core",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.iresp[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6579,
        6580
      ]
    },
    {
      "id": "PreRegisterResponse",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io_core_iresp_0_out.valid; an internal integer response survives branch-mispredict and core-exception filtering and is presented to the output register",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io_core_iresp_0_out.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6568,
        6569,
        6570,
        6571,
        6572,
        6573,
        6574,
        6575,
        6576,
        6577
      ]
    }
  ],
  "predicates": [
    {
      "id": "ResponseControlBlocked",
      "definition": "the current internal integer response is killed because its branch mask intersects the current mispredict mask or io.core.exception is asserted",
      "grounding": {
        "source_signal": "_io_core_iresp_0_out_valid_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        6572,
        6573,
        6574,
        6575,
        6576,
        6577
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_PreRegisterResponseSurvives",
      "trigger_occurrences": [
        "PreRegisterResponse"
      ],
      "guard_predicates": [
        {
          "id": "ResponseControlBlocked",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "The internal iresp response survives the branch-mispredict/core-exception filter and is presented to the one-cycle output register."
      ],
      "evidence_statement_ids": [
        6568,
        6569,
        6570,
        6571,
        6572,
        6573,
        6574,
        6575,
        6576,
        6577,
        6579
      ],
      "confidence": "high"
    },
    {
      "id": "C2_CoreVisibleIntegerResponse",
      "trigger_occurrences": [
        "IntegerResponse"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The core-visible response is exactly the current contents of io_core_iresp_0_REG."
      ],
      "evidence_statement_ids": [
        6579,
        6580
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "PreRegisterResponse",
        "predicate": "ResponseControlBlocked",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6572,
        6573,
        6574,
        6575,
        6576,
        6577
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.data",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.mem_size",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.mem_size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "PreRegisterResponse",
        "target": "io_core_iresp_0_out.bits.uop.mem_signed",
        "source": {
          "op": "signal",
          "name": "iresp[0].bits.uop.mem_signed"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PreRegisterResponseSurvives"
      ],
      "evidence_statement_ids": [
        6568
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.data",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.mem_size",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.mem_size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.mem_signed",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.mem_signed"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "IntegerResponse",
        "target": "io.core.iresp[0].bits.uop.br_mask",
        "source": {
          "op": "signal",
          "name": "io_core_iresp_0_REG.bits.uop.br_mask"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_CoreVisibleIntegerResponse"
      ],
      "evidence_statement_ids": [
        6580
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "IntegerResponse is the sole physical boundary event in this WorkUnit and represents a registered integer LSU response becoming visible to the core.",
    "Unlike the floating-point response path, io.core.iresp[0] is not directly driven by the internal iresp bundle in this elaboration. The internal response is first passed through UpdateBrMask with io.core.exception and then captured by io_core_iresp_0_REG.",
    "PreRegisterResponse preserves the memory-order-relevant branch/core-exception suppression point. Its exact valid equation requires iresp[0].valid and excludes both a branch-mispredict-mask overlap and io.core.exception.",
    "A1 explicitly records that a response killed by the current branch/core control state cannot be presented to the output register.",
    "A2-A8 preserve the data and memory/identity projections that pass unchanged through UpdateBrMask. The br_mask field itself is intentionally not equated because UpdateBrMask rewrites it by removing resolved branch bits.",
    "A9-A16 preserve the corresponding projections of the actual registered bundle exposed at the architectural core-facing boundary.",
    "The internal iresp bundle has several possible producers in the supplied ledger: an ordinary memory response using uop/resp.data, a store-related response using stq_uop/resp.data, and a store-to-load forwarding response using wb_ldst_forward_e plus load-data extraction.",
    "The control statements that select among those internal iresp producers are not fully retained in this WorkUnit ledger. No exact DCache/store/forwarding provenance partition is therefore claimed.",
    "Omitting that source partition is a safe over-approximation and may be refined later through CEGAR if a parent-level counterexample depends on response provenance.",
    "No ordered_before or exact one-cycle relation is asserted between PreRegisterResponse and IntegerResponse. io_core_iresp_0_REG is an unreset RegNext value in the supplied evidence, so an initial core-visible valid value cannot be excluded by this leaf. A global required-prior theorem would therefore impose an unsupported initialization guarantee.",
    "The one-cycle implementation latency is nevertheless documented in the rationale rather than approximated with a semantically different temporal axiom.",
    "No architectural identity_key is introduced from rob_idx, ldq_idx, or stq_idx because this region does not establish global uniqueness for those fields.",
    "Floating-point status fields and predication metadata are not relevant to this integer memory-response abstraction and are omitted.",
    "No liveness or eventual-response property is claimed."
  ],
  "extensions": {}
}