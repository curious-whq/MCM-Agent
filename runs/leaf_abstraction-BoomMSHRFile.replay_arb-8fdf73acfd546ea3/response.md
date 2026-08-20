{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.replay_arb-8fdf73acfd546ea3",
  "work_unit_id": "BoomMSHRFile.replay_arb",
  "occurrences": [
    {
      "id": "Input0Fire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.replay_arb::io.in[0].fire"
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
        "BoomMSHRFile.replay_arb::io.in[1].fire"
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
        "BoomMSHRFile.replay_arb::io.out.fire"
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
        "Input 0 has fixed priority and the accepted replay request is forwarded to the output in the same cycle."
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
        "Input 1 can be accepted only while input 0 is not valid, and its replay request is forwarded to the output in the same cycle."
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
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
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
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
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
        7
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.sdq_id",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.sdq_id"
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
        "target": "io.out.bits.old_meta.tag",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.old_meta.tag"
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
        "on": "Input0Fire",
        "target": "io.out.bits.old_meta.coh.state",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.old_meta.coh.state"
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
      "id": "A10",
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
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "Input0Fire",
        "target": "io.out.bits.tag_match",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits.tag_match"
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
      "id": "A12",
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
      "id": "A13",
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
        "target": "io.out.bits.sdq_id",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.sdq_id"
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
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.old_meta.tag",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.old_meta.tag"
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
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.old_meta.coh.state",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.old_meta.coh.state"
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
      "id": "A19",
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
      "id": "A20",
      "formal": {
        "type": "signal_equality",
        "on": "Input1Fire",
        "target": "io.out.bits.tag_match",
        "source": {
          "op": "signal",
          "name": "io.in[1].bits.tag_match"
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
    "The replay arbiter is purely combinational and has no local registers, so it carries no cross-cycle transaction identity of its own.",
    "A1 captures the essential conservation/routing behavior: OutputFire is exactly the same-cycle partition of Input0Fire and Input1Fire.",
    "A2 captures fixed input-0 priority. Since io.in[1].ready = !io.in[0].valid && io.out.ready, input 1 cannot fire while input 0 is valid.",
    "A3-A11 and A12-A20 retain only memory/replay-critical payload projections on each selected route: address, memory command, load/store queue indices, store-data queue id, prior cache metadata, way selection, and tag-match state.",
    "The complete BoomDCacheReqInternal aggregate is in fact selected wholesale by io.out.bits := io.in[1].bits with an io.in[0].valid override to io.in[0].bits. Hundreds of additional payload leaf equalities are deliberately omitted because they only strengthen the abstraction; they can be added by CEGAR if a higher-level counterexample depends on one of those fields.",
    "No aggregate signal_equality is claimed because current practice is to use exact field projections rather than rely on aggregate equality semantics.",
    "No historical ordered_before relation is emitted because input acceptance and output forwarding are the same physical cycle.",
    "No liveness or output-readiness fairness property is claimed."
  ],
  "extensions": {}
}