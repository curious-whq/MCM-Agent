{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8",
  "work_unit_id": "BoomMSHR.rpq.main",
  "occurrences": [
    {
      "id": "EnqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR.rpq.main::io.enq.fire"
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
        30,
        267,
        268
      ]
    },
    {
      "id": "QueueInsert",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_enq; equivalently io.enq.fire && !incoming_branch_killed && !incoming_flush_killed",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "expr": {
          "op": "signal",
          "name": "enq_ptr_value"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 15
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
        30,
        31,
        32,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        242,
        243,
        244,
        245,
        246,
        247,
        248,
        249,
        250,
        251,
        252,
        253,
        254,
        255
      ]
    },
    {
      "id": "DeqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR.rpq.main::io.deq.fire"
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
          "end_exclusive": 15
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
        41,
        42,
        43,
        44,
        45,
        46,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        273,
        274,
        275,
        276
      ]
    },
    {
      "id": "InvalidHeadSkip",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_deq && !io.deq.valid; equivalently the queue is non-empty and valids[deq_ptr_value] is false, causing deq_ptr to advance without a dequeue handshake",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 15
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
        41,
        42,
        43,
        44,
        45,
        46,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        273,
        274,
        275
      ]
    }
  ],
  "predicates": [
    {
      "id": "QueueEmpty",
      "definition": "enq_ptr_value == deq_ptr_value && !maybe_full",
      "grounding": {
        "source_signal": "io.empty",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        25,
        26,
        27,
        28
      ]
    },
    {
      "id": "QueueFull",
      "definition": "enq_ptr_value == deq_ptr_value && maybe_full",
      "grounding": {
        "source_signal": "full",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        25,
        29,
        267,
        268
      ]
    },
    {
      "id": "IncomingBranchKilled",
      "definition": "(io.brupdate.b1.mispredict_mask & io.enq.bits.uop.br_mask) != 0",
      "grounding": {
        "source_signal": "_do_enq_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        31,
        32
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
        36
      ]
    },
    {
      "id": "HeadInvalid",
      "definition": "valids[deq_ptr_value] == 0",
      "grounding": {
        "source_signal": "_do_deq_T",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        41
      ]
    },
    {
      "id": "HeadValid",
      "definition": "valids[deq_ptr_value] != 0",
      "grounding": {
        "source_signal": "_do_deq_T",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        41
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
        "A handshaken request that is not killed on arrival is written into the current enqueue slot and advances enq_ptr."
      ],
      "evidence_statement_ids": [
        30,
        31,
        32,
        34,
        35,
        36,
        37,
        38,
        40,
        242,
        243,
        244,
        245,
        246,
        249,
        250,
        251,
        252,
        253,
        254,
        255
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
        "The boundary handshake does not become a QueueInsert when the incoming uop is killed by the current branch mispredict mask."
      ],
      "evidence_statement_ids": [
        30,
        31,
        32,
        34,
        35,
        39,
        40
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
        "The boundary handshake does not become a QueueInsert when flush kills this uses_ldq request."
      ],
      "evidence_statement_ids": [
        30,
        35,
        36,
        37,
        38,
        39,
        40
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
          "id": "HeadInvalid",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "A visible dequeue can occur only from a non-empty valid head slot."
      ],
      "evidence_statement_ids": [
        41,
        43,
        44,
        273,
        274,
        275,
        276
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
        "An invalid hole at the current non-empty head is consumed internally by advancing deq_ptr without io.deq.fire."
      ],
      "evidence_statement_ids": [
        41,
        42,
        43,
        44,
        45,
        46,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        273,
        274,
        275
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
        29,
        30,
        267,
        268
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
        30,
        31,
        32,
        34,
        35,
        39,
        40,
        242
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
        30,
        35,
        36,
        37,
        38,
        39,
        40,
        242
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
        28,
        43,
        44,
        273,
        274,
        275
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
        41,
        273,
        274,
        275
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
        28,
        41,
        42,
        43,
        44,
        45,
        46
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
        41,
        42,
        43,
        44,
        45,
        46,
        273,
        274,
        275
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
        242,
        243,
        244
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
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
        20,
        22,
        23,
        242,
        245,
        250,
        251,
        252,
        253,
        254,
        255,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        273,
        274,
        275
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "QueueInsert is separated from EnqHandshake because io.enq.fire can be accepted at the boundary yet be killed by the current branch update or flush before any queue storage/pointer update occurs.",
    "InvalidHeadSkip is retained as a derived occurrence because a previously invalidated slot can advance deq_ptr without io.deq.fire; this affects the visible path through the queue but does not warrant 15 separate per-entry kill events.",
    "No liveness or eventual-dequeue property is claimed; the candidate therefore needs no ready/valid fairness assumption.",
    "No transaction identity_key is claimed in this leaf. Payload is stored in indexed ram/uops state, uops.br_mask is intentionally rewritten on branch resolution, and the current identity_flow form has no indexed/generational carrier semantics. Omitting identity flow is a conservative over-approximation rather than an approximate claim.",
    "Cross-transaction FIFO preservation and exact inserted-entry-to-dequeued-entry conservation are deliberately omitted. They would strengthen the abstraction but are not required for this conservative candidate; if parent/system CEGAR produces spurious reorder or provenance traces, that evidence can justify a later generic queue/order-flow extension.",
    "Stored-entry branch/flush invalidation is not materialized as 15 semantic occurrences. Its externally relevant consequence is represented by the possibility of a valid slot becoming a hole and by InvalidHeadSkip; omitting stronger per-entry kill conservation allows additional behavior and is therefore conservative.",
    "The aggregate equalities out = out_MPORT and io.deq.bits = out are deliberately omitted: out.uop is overwritten from uops[deq_ptr_value], so aggregate equality would be stronger than the RTL guarantee. Exact dequeue payload provenance can be added later as leaf/indexed equalities if parent CEGAR requires it."
  ],
  "extensions": {}
}