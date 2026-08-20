{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e",
  "work_unit_id": "BoomMSHRFile.respq",
  "occurrences": [
    {
      "id": "EnqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.respq::io.enq.fire"
      ],
      "definition": "io.enq.valid && io.enq.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.enq.valid",
          "io.enq.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        19,
        109,
        110
      ]
    },
    {
      "id": "QueueInsert",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_enq",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "expr": {
          "op": "signal",
          "name": "enq_ptr_value"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 4
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "do_enq"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99
      ]
    },
    {
      "id": "DeqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.respq::io.deq.fire"
      ],
      "definition": "io.deq.valid && io.deq.ready",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 4
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.deq.valid",
          "io.deq.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        12,
        30,
        31,
        32,
        33,
        34,
        35,
        115,
        116,
        117,
        118
      ]
    },
    {
      "id": "InvalidHeadSkip",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_deq && !io.deq.valid",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 4
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "do_deq"
        ],
        "signals_false": [
          "io.deq.valid"
        ]
      },
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
      ]
    }
  ],
  "predicates": [
    {
      "id": "QueueEmpty",
      "definition": "io.empty",
      "grounding": {
        "source_signal": "io.empty",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        14,
        15,
        16,
        17
      ]
    },
    {
      "id": "QueueFull",
      "definition": "full",
      "grounding": {
        "source_signal": "full",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        14,
        18,
        109,
        110
      ]
    },
    {
      "id": "IncomingBranchKilled",
      "definition": "(io.brupdate.b1.mispredict_mask & io.enq.bits.uop.br_mask) != 0",
      "grounding": {
        "source_signal": "_do_enq_T_3",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        20,
        21,
        22,
        23
      ]
    },
    {
      "id": "IncomingFlushKilled",
      "definition": "io.flush && io.enq.bits.uop.uses_ldq",
      "grounding": {
        "source_signal": "_do_enq_T_6",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        25,
        26,
        27
      ]
    },
    {
      "id": "HeadInvalid",
      "definition": "!valids[deq_ptr_value]",
      "grounding": {
        "source_signal": "valids[deq_ptr_value]",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        30,
        115,
        116
      ]
    },
    {
      "id": "HeadValid",
      "definition": "valids[deq_ptr_value]",
      "grounding": {
        "source_signal": "valids[deq_ptr_value]",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        30,
        115,
        116
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Admitted",
      "trigger_occurrences": [
        "EnqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "IncomingBranchKilled",
          "positive": false
        },
        {
          "id": "IncomingFlushKilled",
          "positive": false
        }
      ],
      "emits": [
        "QueueInsert"
      ],
      "relations": [
        "An enqueue handshake is admitted only when it survives both incoming branch-kill and flush-kill filters; the admitted payload is stored at the current enqueue slot."
      ],
      "evidence_statement_ids": [
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        89,
        90,
        91,
        92,
        95,
        99
      ],
      "confidence": "high"
    },
    {
      "id": "C2_BranchKilledOnArrival",
      "trigger_occurrences": [
        "EnqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "IncomingBranchKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "The external enqueue handshake may occur, but a branch-killed request is not inserted and does not advance the enqueue pointer."
      ],
      "evidence_statement_ids": [
        19,
        20,
        21,
        22,
        23,
        24,
        28,
        29,
        88,
        99
      ],
      "confidence": "high"
    },
    {
      "id": "C3_FlushKilledOnArrival",
      "trigger_occurrences": [
        "EnqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "IncomingFlushKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "An enqueue carrying uses_ldq is rejected from actual queue insertion when io.flush is asserted."
      ],
      "evidence_statement_ids": [
        19,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        99
      ],
      "confidence": "high"
    },
    {
      "id": "C4_VisibleDequeue",
      "trigger_occurrences": [
        "DeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "QueueEmpty",
          "positive": false
        },
        {
          "id": "HeadValid",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A visible dequeue handshake consumes the valid current head slot and advances the dequeue pointer."
      ],
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
      ],
      "confidence": "high"
    },
    {
      "id": "C5_InvalidHeadSkip",
      "trigger_occurrences": [
        "InvalidHeadSkip"
      ],
      "guard_predicates": [
        {
          "id": "QueueEmpty",
          "positive": false
        },
        {
          "id": "HeadInvalid",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A non-empty queue whose current head slot has been invalidated advances past that slot without producing a visible dequeue handshake."
      ],
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "EnqHandshake",
        "predicate": "QueueFull",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        18,
        19,
        109,
        110
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "QueueInsert",
        "predicate": "IncomingBranchKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Admitted",
        "C2_BranchKilledOnArrival"
      ],
      "evidence_statement_ids": [
        20,
        21,
        22,
        23,
        24,
        27,
        28,
        29
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "QueueInsert",
        "predicate": "IncomingFlushKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Admitted",
        "C3_FlushKilledOnArrival"
      ],
      "evidence_statement_ids": [
        25,
        26,
        27,
        28,
        29
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "DeqHandshake",
        "predicate": "QueueEmpty",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_VisibleDequeue"
      ],
      "evidence_statement_ids": [
        15,
        16,
        17,
        115,
        116,
        117
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "DeqHandshake",
        "predicate": "HeadInvalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_VisibleDequeue"
      ],
      "evidence_statement_ids": [
        30,
        115,
        116,
        117
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "forbid_when",
        "occurrence": "InvalidHeadSkip",
        "predicate": "QueueEmpty",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_InvalidHeadSkip"
      ],
      "evidence_statement_ids": [
        32,
        33,
        34,
        35
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "forbid_when",
        "occurrence": "InvalidHeadSkip",
        "predicate": "HeadValid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_InvalidHeadSkip"
      ],
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        115,
        116,
        117
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "QueueInsert",
        "target": "MPORT",
        "source": {
          "op": "signal",
          "name": "io.enq.bits"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Admitted"
      ],
      "evidence_statement_ids": [
        88,
        89,
        90
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "ordered_before",
        "before": "QueueInsert",
        "after": "DeqHandshake",
        "required_prior": null,
        "scope_identity": null,
        "scope_index": {
          "name": "slot",
          "relation": "same"
        }
      },
      "derived_from_case_ids": [
        "C1_Admitted",
        "C4_VisibleDequeue"
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        8,
        9,
        11,
        12,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        88,
        91,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The physical enqueue handshake is not equivalent to actual queue admission. QueueInsert is defined by do_enq, which additionally excludes an incoming request killed by the current branch-mispredict mask or by io.flush when that request's uop.uses_ldq is true.",
    "The queue has four physical slots. QueueInsert is indexed by enq_ptr_value and DeqHandshake/InvalidHeadSkip by deq_ptr_value, allowing A9 to express slot-local valid-token provenance without treating a slot number as a global transaction identity.",
    "A1-A3 preserve admission exclusion. A4-A7 preserve the distinction between a visible dequeue and the internal skip of an invalidated head slot.",
    "The valids vector is initialized false, is set true only on QueueInsert, may only remain true or be cleared by branch/flush killing, and is cleared when the dequeue pointer advances. Therefore any visible dequeue from a given slot requires some prior QueueInsert to that slot; A9 states only this safe same-slot history and does not claim a stronger cross-generation FIFO pairing.",
    "Stored entries may be invalidated after admission by branch misprediction or by io.flush for uops whose uses_ldq bit is set. No axiom requires every QueueInsert eventually to produce DeqHandshake, so this kill path remains safely represented without inventing a liveness guarantee.",
    "A8 records the exact aggregate write into the RAM port at QueueInsert. No aggregate equality is asserted between io.deq.bits and that RAM value because output construction first reads ram[deq_ptr_value] and then overwrites out.uop with uops[deq_ptr_value].",
    "The separate uops array is mutable: its br_mask is reduced by the branch resolve mask while resident. Thus even an admitted entry's dequeue uop need not be bitwise identical to the originally enqueued uop.",
    "No identity_key is declared. The RAM/uops arrays are indexed storage and slot numbers are reused after pointer wrap; without a generation-bearing transaction carrier, treating the slot index itself as request identity would be unsound.",
    "No cross-transaction FIFO ordering stronger than same-slot valid-token provenance is claimed. Such a relation would require distinguishing different generations of the circular queue.",
    "No eventual dequeue, fairness, or consumer-readiness assumption is introduced."
  ],
  "extensions": {}
}