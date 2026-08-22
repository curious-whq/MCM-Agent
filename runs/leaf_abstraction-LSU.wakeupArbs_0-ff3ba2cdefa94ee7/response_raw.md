Current Formal AST is sufficient.

## FINAL MCM-AGENT RESULT

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU.wakeupArbs_0-ff3ba2cdefa94ee7",
  "work_unit_id": "LSU.wakeupArbs_0",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.wakeupArbs_0::io.in[0].fire"
      ],
      "definition": "grounded boundary occurrence LSU.wakeupArbs_0::io.in[0].fire",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.in[0].valid",
          "io.in[0].ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        9,
        10
      ]
    },
    {
      "id": "Input1Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.wakeupArbs_0::io.in[1].fire"
      ],
      "definition": "grounded boundary occurrence LSU.wakeupArbs_0::io.in[1].fire",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.in[1].valid",
          "io.in[1].ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        8,
        11,
        12
      ]
    },
    {
      "id": "OutputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.wakeupArbs_0::io.out.fire"
      ],
      "definition": "grounded boundary occurrence LSU.wakeupArbs_0::io.out.fire",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.out.valid",
          "io.out.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        8,
        13,
        14,
        15
      ]
    }
  ],
  "predicates": [
    {
      "id": "Input0Valid",
      "definition": "input 0 is valid and therefore has fixed priority over input 1",
      "grounding": {
        "source_signal": "io.in[0].valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        5,
        8
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Input0Selected",
      "trigger_occurrences": [
        "Input0Fire"
      ],
      "guard_predicates": [],
      "emits": [
        "OutputFire"
      ],
      "relations": [
        "Input 0 is the fixed-priority winner and its wakeup payload is forwarded in the same cycle."
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "confidence": "high"
    },
    {
      "id": "C2_Input1Selected",
      "trigger_occurrences": [
        "Input1Fire"
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "emits": [
        "OutputFire"
      ],
      "relations": [
        "Input 1 may win only when input 0 is not valid; its wakeup payload is forwarded in the same cycle."
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "OutputFire",
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.chosen",
        "source": {
          "op": "const",
          "value": 0
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        6
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.chosen",
        "source": {
          "op": "const",
          "value": 1
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.uop.pdst",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.uop.pdst"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.speculative_mask",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.speculative_mask"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.bypassable",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.bypassable"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.rebusy",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.rebusy"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.uop.pdst",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.uop.pdst"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.speculative_mask",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.speculative_mask"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.bypassable",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.bypassable"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.rebusy",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.rebusy"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This leaf is a stateless fixed-priority 2-to-1 Decoupled wakeup arbiter; input 0 has priority over input 1.",
    "A1-A4 preserve exact same-cycle routing, fixed priority, and the selected-source identifier io.chosen.",
    "The remaining axioms preserve the memory-ordering/scheduling-relevant wakeup projections: ROB/LDQ/STQ identity, destination physical register, speculation mask, bypassability, and rebusy state.",
    "The rest of the very large MicroOp payload is deliberately omitted as a safe over-approximation and may be added by CEGAR if a parent counterexample depends on it.",
    "There is no buffering or state, so no cross-cycle order or fairness/eventual-service claim is made; input 1 may starve under continuously valid input 0."
  ],
  "extensions": {}
}
```
