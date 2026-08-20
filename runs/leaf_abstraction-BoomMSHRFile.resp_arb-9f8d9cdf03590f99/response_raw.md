{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.resp_arb-9f8d9cdf03590f99",
  "work_unit_id": "BoomMSHRFile.resp_arb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[0].fire"
      ],
      "definition": "io.in[0].valid && io.in[0].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        14,
        15
      ]
    },
    {
      "id": "Input1Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[1].fire"
      ],
      "definition": "io.in[1].valid && io.in[1].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        12,
        16,
        17
      ]
    },
    {
      "id": "Input2Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[2].fire"
      ],
      "definition": "io.in[2].valid && io.in[2].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        11,
        13,
        18,
        19
      ]
    },
    {
      "id": "OutputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.out.fire"
      ],
      "definition": "io.out.valid && io.out.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        20,
        21,
        22
      ]
    }
  ],
  "predicates": [
    {
      "id": "Input0Valid",
      "definition": "io.in[0].valid",
      "grounding": {
        "source_signal": "io.in[0].valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        8,
        12
      ]
    },
    {
      "id": "Higher01Valid",
      "definition": "io.in[0].valid || io.in[1].valid",
      "grounding": {
        "source_signal": "_grant_T",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        11,
        13
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
        "Input 0 has highest fixed priority and an accepted input-0 response is forwarded to the output in the same cycle."
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        9,
        10,
        14,
        15,
        20,
        21,
        22
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
        "Input 1 can be accepted only when input 0 is not valid; the response is forwarded to the output in the same cycle."
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        8,
        12,
        16,
        17,
        20,
        21,
        22
      ],
      "confidence": "high"
    },
    {
      "id": "C3_Input2Selected",
      "trigger_occurrences": [
        "Input2Fire"
      ],
      "guard_predicates": [
        {
          "id": "Higher01Valid",
          "positive": false
        }
      ],
      "emits": [
        "OutputFire"
      ],
      "relations": [
        "Input 2 can be accepted only when neither input 0 nor input 1 is valid; the response is forwarded to the output in the same cycle."
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        13,
        18,
        19,
        20,
        21,
        22
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
          "Input1Fire",
          "Input2Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected",
        "C2_Input1Selected",
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22
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
        12,
        16,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "Input2Fire",
        "predicate": "Higher01Valid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.data",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.is_hella",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.is_hella"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
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
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
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
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
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
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.data",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.is_hella",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.is_hella"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
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
        4,
        5,
        7,
        8,
        12,
        16,
        17
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
        4,
        5,
        7,
        8,
        12,
        16,
        17
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
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.data",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.is_hella",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.is_hella"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A19",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The response arbiter is purely combinational and contains no local state, so it introduces no cross-cycle transaction identity.",
    "A1 generalizes the same occurrence_partition abstraction used by the two-input arbiters: OutputFire is exactly the same-cycle partition of Input0Fire, Input1Fire, and Input2Fire.",
    "A2 and A3 preserve the full fixed-priority structure. Input 1 is blocked whenever input 0 is valid; input 2 is blocked whenever either higher-priority input 0 or input 1 is valid.",
    "The priority chain is grounded directly by grant_1 = !io.in[0].valid and grant_2 = !(io.in[0].valid || io.in[1].valid).",
    "A4-A21 preserve a deliberately selected memory-response interface on every route: returned data, Hella-cache classification, ROB identity, load/store queue identity, and memory command.",
    "The complete BoomDCacheResp aggregate is selected wholesale by the RTL, so many additional payload equalities are also true. They are omitted because adding them only strengthens the abstraction and would turn this µMCM into a mechanical dump of the MicroOp structure; they remain available for later CEGAR refinement.",
    "No aggregate equality is claimed because field-level projections give explicit semantics to the values that higher-level memory-ordering composition is expected to consume.",
    "No ordered_before relation is emitted: input acceptance and output response are the same-cycle routed occurrence.",
    "No liveness or output-readiness fairness assumption is claimed."
  ],
  "extensions": {}
}