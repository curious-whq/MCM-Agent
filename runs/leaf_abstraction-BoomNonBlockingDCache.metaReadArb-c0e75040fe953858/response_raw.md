{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.metaReadArb-c0e75040fe953858",
  "work_unit_id": "BoomNonBlockingDCache.metaReadArb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[0].fire"
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
      "evidence_statement_ids": [17, 29, 30]
    },
    {
      "id": "Input1Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[1].fire"
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
      "evidence_statement_ids": [14, 24, 31, 32]
    },
    {
      "id": "Input2Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[2].fire"
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
      "evidence_statement_ids": [11, 20, 25, 33, 34]
    },
    {
      "id": "Input3Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[3].fire"
      ],
      "definition": "io.in[3].valid && io.in[3].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [8, 21, 26, 35, 36]
    },
    {
      "id": "Input4Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[4].fire"
      ],
      "definition": "io.in[4].valid && io.in[4].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [5, 22, 27, 37, 38]
    },
    {
      "id": "Input5Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.in[5].fire"
      ],
      "definition": "io.in[5].valid && io.in[5].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [23, 28, 39, 40]
    },
    {
      "id": "OutputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.metaReadArb::io.out.fire"
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
      "evidence_statement_ids": [41, 42, 43]
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
      "evidence_statement_ids": [17, 20, 24]
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
      "evidence_statement_ids": [20, 25]
    },
    {
      "id": "Higher012Valid",
      "definition": "io.in[0].valid || io.in[1].valid || io.in[2].valid",
      "grounding": {
        "source_signal": "_grant_T_1",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [20, 21, 26]
    },
    {
      "id": "Higher0123Valid",
      "definition": "io.in[0].valid || io.in[1].valid || io.in[2].valid || io.in[3].valid",
      "grounding": {
        "source_signal": "_grant_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [20, 21, 22, 27]
    },
    {
      "id": "Higher01234Valid",
      "definition": "io.in[0].valid || io.in[1].valid || io.in[2].valid || io.in[3].valid || io.in[4].valid",
      "grounding": {
        "source_signal": "_grant_T_3",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [20, 21, 22, 23, 28]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Input0Selected",
      "trigger_occurrences": ["Input0Fire"],
      "guard_predicates": [],
      "emits": ["OutputFire"],
      "relations": [
        "Input 0 is the highest-priority metadata-read source; its idx, tag, and way_en are forwarded to the output and io.chosen is 0."
      ],
      "evidence_statement_ids": [17, 18, 19, 29, 30, 41, 42, 43],
      "confidence": "high"
    },
    {
      "id": "C2_Input1Selected",
      "trigger_occurrences": ["Input1Fire"],
      "guard_predicates": [
        {"id": "Input0Valid", "positive": false}
      ],
      "emits": ["OutputFire"],
      "relations": [
        "Input 1 is selected only when input 0 is not valid; its payload is forwarded and io.chosen is 1."
      ],
      "evidence_statement_ids": [14, 15, 16, 17, 24, 31, 32, 41, 42, 43],
      "confidence": "high"
    },
    {
      "id": "C3_Input2Selected",
      "trigger_occurrences": ["Input2Fire"],
      "guard_predicates": [
        {"id": "Higher01Valid", "positive": false}
      ],
      "emits": ["OutputFire"],
      "relations": [
        "Input 2 is selected only when neither input 0 nor input 1 is valid; its payload is forwarded and io.chosen is 2."
      ],
      "evidence_statement_ids": [11, 12, 13, 20, 25, 33, 34, 41, 42, 43],
      "confidence": "high"
    },
    {
      "id": "C4_Input3Selected",
      "trigger_occurrences": ["Input3Fire"],
      "guard_predicates": [
        {"id": "Higher012Valid", "positive": false}
      ],
      "emits": ["OutputFire"],
      "relations": [
        "Input 3 is selected only when inputs 0 through 2 are all not valid; its payload is forwarded and io.chosen is 3."
      ],
      "evidence_statement_ids": [8, 9, 10, 21, 26, 35, 36, 41, 42, 43],
      "confidence": "high"
    },
    {
      "id": "C5_Input4Selected",
      "trigger_occurrences": ["Input4Fire"],
      "guard_predicates": [
        {"id": "Higher0123Valid", "positive": false}
      ],
      "emits": ["OutputFire"],
      "relations": [
        "Input 4 is selected only when inputs 0 through 3 are all not valid; its payload is forwarded and io.chosen is 4."
      ],
      "evidence_statement_ids": [5, 6, 7, 22, 27, 37, 38, 41, 42, 43],
      "confidence": "high"
    },
    {
      "id": "C6_Input5Selected",
      "trigger_occurrences": ["Input5Fire"],
      "guard_predicates": [
        {"id": "Higher01234Valid", "positive": false}
      ],
      "emits": ["OutputFire"],
      "relations": [
        "Input 5 is the lowest-priority default source and is selected only when inputs 0 through 4 are all not valid; its payload is forwarded and io.chosen is 5."
      ],
      "evidence_statement_ids": [3, 4, 23, 28, 39, 40, 41, 42, 43],
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
          "Input2Fire",
          "Input3Fire",
          "Input4Fire",
          "Input5Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected",
        "C2_Input1Selected",
        "C3_Input2Selected",
        "C4_Input3Selected",
        "C5_Input4Selected",
        "C6_Input5Selected"
      ],
      "evidence_statement_ids": [
        20, 21, 22, 23, 24, 25, 26, 27, 28,
        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43
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
      "derived_from_case_ids": ["C2_Input1Selected"],
      "evidence_statement_ids": [24, 31, 32],
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
      "derived_from_case_ids": ["C3_Input2Selected"],
      "evidence_statement_ids": [20, 25, 33, 34],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "Input3Fire",
        "predicate": "Higher012Valid",
        "scope_identity": null
      },
      "derived_from_case_ids": ["C4_Input3Selected"],
      "evidence_statement_ids": [20, 21, 26, 35, 36],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "Input4Fire",
        "predicate": "Higher0123Valid",
        "scope_identity": null
      },
      "derived_from_case_ids": ["C5_Input4Selected"],
      "evidence_statement_ids": [20, 21, 22, 27, 37, 38],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "forbid_when",
        "occurrence": "Input5Fire",
        "predicate": "Higher01234Valid",
        "scope_identity": null
      },
      "derived_from_case_ids": ["C6_Input5Selected"],
      "evidence_statement_ids": [20, 21, 22, 23, 28, 39, 40],
      "status": "candidate"
    },

    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 0},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C1_Input0Selected"],
      "evidence_statement_ids": [17, 18],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 1},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C2_Input1Selected"],
      "evidence_statement_ids": [14, 15, 24, 31, 32],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 2},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C3_Input2Selected"],
      "evidence_statement_ids": [11, 12, 20, 25, 33, 34],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "Input3Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 3},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C4_Input3Selected"],
      "evidence_statement_ids": [8, 9, 21, 26, 35, 36],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input4Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 4},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C5_Input4Selected"],
      "evidence_statement_ids": [5, 6, 22, 27, 37, 38],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "Input5Fire",
        "target": "io.chosen",
        "source": {"op": "const", "value": 5},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C6_Input5Selected"],
      "evidence_statement_ids": [3, 23, 28, 39, 40],
      "status": "candidate"
    },

    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[0].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C1_Input0Selected"],
      "evidence_statement_ids": [17, 19],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[0].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C1_Input0Selected"],
      "evidence_statement_ids": [17, 19],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[0].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C1_Input0Selected"],
      "evidence_statement_ids": [17, 19],
      "status": "candidate"
    },

    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[1].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C2_Input1Selected"],
      "evidence_statement_ids": [14, 16, 24, 31, 32],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[1].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C2_Input1Selected"],
      "evidence_statement_ids": [14, 16, 24, 31, 32],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[1].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C2_Input1Selected"],
      "evidence_statement_ids": [14, 16, 24, 31, 32],
      "status": "candidate"
    },

    {
      "id": "A19",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[2].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C3_Input2Selected"],
      "evidence_statement_ids": [11, 13, 20, 25, 33, 34],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[2].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C3_Input2Selected"],
      "evidence_statement_ids": [11, 13, 20, 25, 33, 34],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "signal_equality",
        "on": "Input2Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[2].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C3_Input2Selected"],
      "evidence_statement_ids": [11, 13, 20, 25, 33, 34],
      "status": "candidate"
    },

    {
      "id": "A22",
      "formal": {
        "type": "signal_equality",
        "on": "Input3Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[3].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C4_Input3Selected"],
      "evidence_statement_ids": [8, 10, 21, 26, 35, 36],
      "status": "candidate"
    },
    {
      "id": "A23",
      "formal": {
        "type": "signal_equality",
        "on": "Input3Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[3].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C4_Input3Selected"],
      "evidence_statement_ids": [8, 10, 21, 26, 35, 36],
      "status": "candidate"
    },
    {
      "id": "A24",
      "formal": {
        "type": "signal_equality",
        "on": "Input3Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[3].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C4_Input3Selected"],
      "evidence_statement_ids": [8, 10, 21, 26, 35, 36],
      "status": "candidate"
    },

    {
      "id": "A25",
      "formal": {
        "type": "signal_equality",
        "on": "Input4Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[4].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C5_Input4Selected"],
      "evidence_statement_ids": [5, 7, 22, 27, 37, 38],
      "status": "candidate"
    },
    {
      "id": "A26",
      "formal": {
        "type": "signal_equality",
        "on": "Input4Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[4].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C5_Input4Selected"],
      "evidence_statement_ids": [5, 7, 22, 27, 37, 38],
      "status": "candidate"
    },
    {
      "id": "A27",
      "formal": {
        "type": "signal_equality",
        "on": "Input4Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[4].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C5_Input4Selected"],
      "evidence_statement_ids": [5, 7, 22, 27, 37, 38],
      "status": "candidate"
    },

    {
      "id": "A28",
      "formal": {
        "type": "signal_equality",
        "on": "Input5Fire",
        "target": "io.out.bits.req[0].idx",
        "source": {"op": "signal", "name": "io.in[5].bits.req[0].idx"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C6_Input5Selected"],
      "evidence_statement_ids": [3, 4, 23, 28, 39, 40],
      "status": "candidate"
    },
    {
      "id": "A29",
      "formal": {
        "type": "signal_equality",
        "on": "Input5Fire",
        "target": "io.out.bits.req[0].tag",
        "source": {"op": "signal", "name": "io.in[5].bits.req[0].tag"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C6_Input5Selected"],
      "evidence_statement_ids": [3, 4, 23, 28, 39, 40],
      "status": "candidate"
    },
    {
      "id": "A30",
      "formal": {
        "type": "signal_equality",
        "on": "Input5Fire",
        "target": "io.out.bits.req[0].way_en",
        "source": {"op": "signal", "name": "io.in[5].bits.req[0].way_en"},
        "scope_identity": null
      },
      "derived_from_case_ids": ["C6_Input5Selected"],
      "evidence_statement_ids": [3, 4, 23, 28, 39, 40],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The module is a stateless fixed-priority 6-to-1 Decoupled arbiter. FIRRTL assignment precedence and the grant chain establish priority Input0 > Input1 > Input2 > Input3 > Input4 > Input5.",
    "A1 preserves exact same-cycle conservation: every output metadata-read handshake is exactly one of the six input handshakes.",
    "A2-A6 preserve the actual priority policy. Each lower-priority input is forbidden from firing whenever any higher-priority input is valid.",
    "A7-A12 preserve io.chosen because it is an exposed parent frontier signal and gives the exact winning source.",
    "A13-A30 preserve the complete metadata-read request payload for each route: idx identifies the metadata set, way_en carries the way-selection information, and tag is retained because it is an exposed request field and may be used by the parent even though the metadata SRAM itself primarily indexes by idx.",
    "No transaction identity key is needed because the arbiter contains no state and performs only same-cycle routing.",
    "No historical ordered_before relation is introduced because there is no buffering or cross-cycle staging.",
    "No fairness or eventual-service property is claimed. Any lower-priority input may be indefinitely starved by continuously valid higher-priority traffic."
  ],
  "extensions": {}
}