{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.dataReadArb-8173fddc63391303",
  "work_unit_id": "BoomNonBlockingDCache.dataReadArb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.dataReadArb::io.in[0].fire"
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
        "BoomNonBlockingDCache.dataReadArb::io.in[1].fire"
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
        "BoomNonBlockingDCache.dataReadArb::io.in[2].fire"
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
        "BoomNonBlockingDCache.dataReadArb::io.out.fire"
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
        11,
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
        11
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
        "Input 0 has highest priority. When it fires, the output fires in the same cycle, chosen is 0, and the output read-request payload comes from input 0."
      ],
      "evidence_statement_ids": [
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
        "Input 1 may fire only when input 0 is not valid; then chosen is 1 and the output payload comes from input 1."
      ],
      "evidence_statement_ids": [
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
        "Input 2 may fire only when neither input 0 nor input 1 is valid; then chosen remains 2 and the default output payload from input 2 is selected."
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
        8,
        9
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
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
        5,
        6,
        8,
        12,
        16,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.chosen",
        "source": {
          "op": "const",
          "value": 2
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        3,
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
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.req[0].addr",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.req[0].addr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
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
        "target": "io.out.bits.req[0].way_en",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.req[0].way_en"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
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
        "target": "io.out.bits.valid[0]",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.valid[0]"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
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
        "target": "io.out.bits.req[0].addr",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.req[0].addr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
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
        "target": "io.out.bits.req[0].way_en",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.req[0].way_en"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
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
        "target": "io.out.bits.valid[0]",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.valid[0]"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
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
        "on": "Input2Fire",
        "target": "io.out.bits.req[0].addr",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.req[0].addr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        3,
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
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.req[0].way_en"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        3,
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
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.valid[0]",
        "source": {
          "op": "signal",
          "name": "io.in[2].bits.valid[0]"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        3,
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
    "The module is a stateless fixed-priority 3-to-1 Decoupled arbiter. Input 0 has highest priority, input 1 is eligible only when input 0 is not valid, and input 2 is eligible only when neither higher-priority input is valid.",
    "A1 captures exact same-cycle event conservation: every output handshake corresponds to exactly one accepted input handshake and every accepted input handshake produces the output handshake in that cycle.",
    "A2 and A3 preserve arbitration policy separately from conservation so the abstraction does not merely say that some input won; it preserves which higher-priority requests suppress lower-priority requests.",
    "A4-A6 preserve io.chosen because it is an exposed parent frontier signal and is an exact encoding of the selected input.",
    "A7-A15 preserve the complete memory-relevant data-read request payload: row address, way enable mask, and the per-lane valid bit.",
    "No transaction identity is needed because the arbiter contains no state and all routing is same-cycle.",
    "No ordered_before relation is introduced because there is no cross-cycle staging.",
    "No fairness or eventual-service property is claimed; a continuously valid lower-priority input may be starved by higher-priority traffic."
  ],
  "extensions": {}
}