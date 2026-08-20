{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.refill_arb-af45d6b6d169fc58",
  "work_unit_id": "BoomMSHRFile.refill_arb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.refill_arb::io.in[0].fire"
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
        "BoomMSHRFile.refill_arb::io.in[1].fire"
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
        "BoomMSHRFile.refill_arb::io.out.fire"
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
        "Input 0 has fixed priority; an accepted input-0 refill/data-write request is forwarded to the output in the same cycle."
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
        "Input 1 can be accepted only while input 0 is not valid, and the accepted refill/data-write request is forwarded to the output in the same cycle."
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
        "target": "io.out.bits.addr",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.addr"
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
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
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
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.wmask",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.wmask"
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
        "on": "Input1Fire",
        "target": "io.out.bits.addr",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.addr"
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
      "id": "A8",
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
        "target": "io.out.bits.wmask",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.wmask"
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
    "The refill arbiter is purely combinational and has no local state, so it introduces no cross-cycle transaction identity or persistent storage.",
    "A1 captures exact same-cycle conservation: OutputFire is equivalent to exactly one of Input0Fire and Input1Fire.",
    "A2 captures fixed input-0 priority. io.in[1].ready is gated by grant_1 = !io.in[0].valid, so input 1 cannot fire whenever input 0 is valid.",
    "A3-A6 preserve all four data-write payload leaves on the input-0 route: addr, data, way_en, and wmask.",
    "A7-A10 preserve all four data-write payload leaves on the input-1 route. Unlike the much larger replay request aggregate, every field here directly affects the cache data write, so no payload projection is deliberately omitted.",
    "The default io.out.bits := io.in[1].bits assignment is overridden by io.out.bits := io.in[0].bits when io.in[0].valid; Input1Fire itself implies io.in[0].valid is false, making both route-specific payload equalities exact.",
    "No ordered_before axiom is emitted because input acceptance and output forwarding are the same-cycle routed transaction.",
    "No liveness or io.out.ready fairness property is claimed."
  ],
  "extensions": {}
}