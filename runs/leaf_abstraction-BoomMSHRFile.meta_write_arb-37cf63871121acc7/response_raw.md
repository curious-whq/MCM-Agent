{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.meta_write_arb-37cf63871121acc7",
  "work_unit_id": "BoomMSHRFile.meta_write_arb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.in[0].fire"
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
        9,
        10
      ]
    },
    {
      "id": "Input1Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.in[1].fire"
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
        8,
        11,
        12
      ]
    },
    {
      "id": "OutputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.out.fire"
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
        13,
        14,
        15
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
        "Input 0 has priority and an accepted input-0 metadata write is forwarded to the output in the same cycle."
      ],
      "evidence_statement_ids": [
        4,
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
        "Input 1 can be accepted only while input 0 is not valid, and the accepted metadata write is forwarded to the output in the same cycle."
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
        "target": "io.out.bits.idx",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.way_en",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.way_en"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.tag",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.tag"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
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
        "target": "io.out.bits.data.coh.state",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.data.coh.state"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
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
        "target": "io.out.bits.data.tag",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.data.tag"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.idx",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.way_en",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.way_en"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.tag",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.tag"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.data.coh.state",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.data.coh.state"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.data.tag",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.data.tag"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
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
    "The arbiter is completely combinational and has no local state, so there is no persistent transaction carrier and no cross-cycle identity key to declare.",
    "A1 captures the essential conservation/routing semantics: every output handshake is exactly one of the two input handshakes in the same cycle, and every accepted input handshake is simultaneously an output handshake.",
    "A2 preserves the fixed-priority policy. Because io.in[1].ready is gated by grant_1 = !io.in[0].valid, input 1 cannot fire in any cycle in which input 0 is valid.",
    "A3-A12 preserve all five metadata payload leaves across the selected combinational route. This is necessary to retain cache-index, way, tag, and coherence-state identity across arbitration without inventing a stored identity carrier.",
    "The default io.out.bits := io.in[1].bits assignment is overridden by io.out.bits := io.in[0].bits exactly when io.in[0].valid. Input1Fire itself proves io.in[0].valid is false, so the input-1 payload forwarding claims are exact.",
    "No historical ordered_before relation is emitted because input and output handshakes occur in the same cycle; representing this arbiter with temporal ordering would change its meaning.",
    "No progress or fairness assumption is needed. The abstraction constrains what happens when handshakes occur but does not claim that io.out.ready will eventually become true."
  ],
  "extensions": {}
}
