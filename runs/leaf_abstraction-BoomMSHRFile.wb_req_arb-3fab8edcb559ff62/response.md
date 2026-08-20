{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.wb_req_arb-3fab8edcb559ff62",
  "work_unit_id": "BoomMSHRFile.wb_req_arb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.wb_req_arb::io.in[0].fire"
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
        "BoomMSHRFile.wb_req_arb::io.in[1].fire"
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
        "BoomMSHRFile.wb_req_arb::io.out.fire"
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
        "Input 0 has fixed priority; an accepted input-0 writeback request is forwarded to the output in the same cycle."
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
        "Input 1 can be accepted only when input 0 is not valid; the accepted writeback request is forwarded to the output in the same cycle."
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
      "id": "A4",
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
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.source",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.source"
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
        "target": "io.out.bits.param",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.param"
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
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.voluntary",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.voluntary"
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
      "id": "A9",
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
      "id": "A10",
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
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.source",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.source"
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
        "target": "io.out.bits.param",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.param"
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
      "id": "A13",
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
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.voluntary",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.voluntary"
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
    "The arbiter is purely combinational and has no local state, so no persistent transaction carrier or cross-cycle identity key is declared.",
    "A1 is the essential conservation/routing axiom: OutputFire is exactly the same-cycle partition of Input0Fire and Input1Fire. The two input handshakes cannot coexist in one cycle.",
    "A2 captures the fixed priority of input 0. grant_1 is exactly !io.in[0].valid, and io.in[1].ready is grant_1 && io.out.ready, so input 1 cannot be accepted while input 0 is valid.",
    "A3-A8 preserve all six WritebackReq payload leaves across the input-0 route: tag, idx, source, param, way_en, and voluntary.",
    "A9-A14 preserve the same six payload leaves across the input-1 route. Input1Fire itself implies io.in[0].valid is false, so the default io.out.bits := io.in[1].bits assignment is the selected value on that route.",
    "The voluntary bit is retained because it changes downstream writeback semantics and completion requirements, while tag/idx/source/param/way_en preserve cache-line, source, permission, and way information across arbitration.",
    "No historical ordering relation is emitted: the accepted input and output transaction are the same-cycle routed transaction, not distinct temporally ordered milestones.",
    "The internal io.chosen signal is not promoted into the parent-facing µMCM because occurrence partition, fixed-priority exclusion, and payload forwarding already preserve its memory/coherence-relevant meaning.",
    "No liveness or output-readiness fairness property is claimed."
  ],
  "extensions": {}
}