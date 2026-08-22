{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU.retry_queue-4e9eb249feec6033",
  "work_unit_id": "LSU.retry_queue",
  "occurrences": [
    {
      "id": "EnqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.retry_queue::io.enq.fire"
      ],
      "definition": "io.enq.valid && io.enq.ready; one retry request is accepted at the external enqueue interface",
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
        23,
        165,
        166
      ]
    },
    {
      "id": "QueueInsert",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_enq; the accepted retry request survives current branch/flush killing and is inserted into the current enqueue slot",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "expr": {
          "op": "signal",
          "name": "enq_ptr_value"
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
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        144,
        145,
        146,
        147,
        148,
        149,
        150,
        151,
        152,
        153,
        154,
        155
      ]
    },
    {
      "id": "BranchKilledEnqueue",
      "kind": "derived",
      "physical_event_ids": [
        "LSU.retry_queue::io.enq.fire"
      ],
      "definition": "io.enq.fire && incoming branch-mispredict mask overlaps io.enq.bits.uop.br_mask",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.enq.valid",
          "io.enq.ready",
          "_do_enq_T_2"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28
      ]
    },
    {
      "id": "FlushKilledEnqueue",
      "kind": "derived",
      "physical_event_ids": [
        "LSU.retry_queue::io.enq.fire"
      ],
      "definition": "io.enq.fire && !incoming_branch_killed && io.flush; a handshaken retry request is discarded by flush",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.enq.valid",
          "io.enq.ready",
          "io.flush"
        ],
        "signals_false": [
          "_do_enq_T_2"
        ]
      },
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33
      ]
    },
    {
      "id": "HeadAdvance",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_deq; the retry queue advances its dequeue pointer either because a valid head is consumed or because an invalid head is skipped",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "do_deq"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        34,
        35,
        36,
        37,
        38,
        39,
        156,
        157,
        158,
        159,
        160,
        161
      ]
    },
    {
      "id": "DeqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.retry_queue::io.deq.fire"
      ],
      "definition": "io.deq.valid && io.deq.ready; one still-valid retry request is accepted by the consumer",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
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
        34,
        35,
        36,
        37,
        171,
        172,
        173,
        174
      ]
    },
    {
      "id": "InvalidHeadSkip",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_deq && !io.deq.valid; the current physical head slot is invalid and is skipped without an externally visible dequeue",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "expr": {
          "op": "signal",
          "name": "deq_ptr_value"
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
        34,
        35,
        36,
        37,
        38,
        39,
        156,
        157,
        158,
        159,
        160,
        161,
        171,
        172,
        173
      ]
    }
  ],
  "predicates": [
    {
      "id": "QueueFull",
      "definition": "full; enqueue and dequeue pointers match while maybe_full is asserted",
      "grounding": {
        "source_signal": "full",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        18,
        22,
        165,
        166
      ]
    },
    {
      "id": "QueueEmpty",
      "definition": "io.empty; enqueue and dequeue pointers match while maybe_full is clear",
      "grounding": {
        "source_signal": "io.empty",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        18,
        19,
        20,
        21,
        36,
        37
      ]
    },
    {
      "id": "IncomingBranchKilled",
      "definition": "the current branch mispredict mask overlaps the enqueue uop branch mask",
      "grounding": {
        "source_signal": "_do_enq_T_2",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        24,
        25
      ]
    },
    {
      "id": "IncomingFlushKilled",
      "definition": "io.flush is asserted; this queue's flush_fn is true for the retry entry type",
      "grounding": {
        "source_signal": "io.flush",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        29,
        30
      ]
    },
    {
      "id": "HeadValid",
      "definition": "valids[deq_ptr_value] is asserted",
      "grounding": {
        "source_signal": "valids[deq_ptr_value]",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        34,
        171,
        172,
        173
      ]
    },
    {
      "id": "HeadInvalid",
      "definition": "valids[deq_ptr_value] is clear",
      "grounding": {
        "source_signal": "valids[deq_ptr_value]",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        34,
        35,
        171,
        172,
        173
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_EnqueueAdmitted",
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
        "A handshaken retry request that survives branch and flush filtering is inserted at the current enqueue slot."
      ],
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        144,
        145,
        146,
        147,
        148,
        149,
        150,
        151,
        155
      ],
      "confidence": "high"
    },
    {
      "id": "C2_EnqueueBranchKilled",
      "trigger_occurrences": [
        "BranchKilledEnqueue"
      ],
      "guard_predicates": [
        {
          "id": "IncomingBranchKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "The external enqueue handshake occurs but no queue insertion or enqueue-pointer advance occurs."
      ],
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28,
        32,
        33,
        144
      ],
      "confidence": "high"
    },
    {
      "id": "C3_EnqueueFlushKilled",
      "trigger_occurrences": [
        "FlushKilledEnqueue"
      ],
      "guard_predicates": [
        {
          "id": "IncomingBranchKilled",
          "positive": false
        },
        {
          "id": "IncomingFlushKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "The external enqueue handshake occurs but the flush filter prevents actual insertion."
      ],
      "evidence_statement_ids": [
        23,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        144
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
      "emits": [
        "HeadAdvance"
      ],
      "relations": [
        "A valid head entry is externally consumed and the dequeue pointer advances."
      ],
      "evidence_statement_ids": [
        34,
        35,
        36,
        37,
        38,
        39,
        156,
        157,
        158,
        159,
        160,
        161,
        171,
        172,
        173,
        174
      ],
      "confidence": "high"
    },
    {
      "id": "C5_InvalidHeadSkipped",
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
      "emits": [
        "HeadAdvance"
      ],
      "relations": [
        "An invalidated head entry is silently discarded by advancing the dequeue pointer without io.deq.fire."
      ],
      "evidence_statement_ids": [
        34,
        35,
        36,
        37,
        38,
        39,
        156,
        157,
        158,
        159,
        160,
        161,
        171,
        172,
        173
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
        22,
        23,
        165,
        166
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "occurrence_partition",
        "whole": "EnqHandshake",
        "parts": [
          "QueueInsert",
          "BranchKilledEnqueue",
          "FlushKilledEnqueue"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_EnqueueAdmitted",
        "C2_EnqueueBranchKilled",
        "C3_EnqueueFlushKilled"
      ],
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "QueueInsert",
        "predicate": "IncomingBranchKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_EnqueueAdmitted",
        "C2_EnqueueBranchKilled"
      ],
      "evidence_statement_ids": [
        23,
        24,
        25,
        26,
        27,
        28,
        32,
        33
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "QueueInsert",
        "predicate": "IncomingFlushKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_EnqueueAdmitted",
        "C3_EnqueueFlushKilled"
      ],
      "evidence_statement_ids": [
        23,
        27,
        28,
        29,
        30,
        31,
        32,
        33
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "HeadAdvance",
        "predicate": "QueueEmpty",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_VisibleDequeue",
        "C5_InvalidHeadSkipped"
      ],
      "evidence_statement_ids": [
        34,
        35,
        36,
        37,
        38,
        39
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "occurrence_partition",
        "whole": "HeadAdvance",
        "parts": [
          "DeqHandshake",
          "InvalidHeadSkip"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_VisibleDequeue",
        "C5_InvalidHeadSkipped"
      ],
      "evidence_statement_ids": [
        34,
        35,
        36,
        37,
        38,
        39,
        156,
        157,
        171,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
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
        34,
        171,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "forbid_when",
        "occurrence": "InvalidHeadSkip",
        "predicate": "HeadValid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_InvalidHeadSkipped"
      ],
      "evidence_statement_ids": [
        34,
        35,
        171,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "QueueInsert",
        "source": {
          "op": "signal",
          "name": "io.enq.bits"
        },
        "target": "MPORT",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_EnqueueAdmitted"
      ],
      "evidence_statement_ids": [
        144,
        145,
        146
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
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
        "C1_EnqueueAdmitted",
        "C4_VisibleDequeue"
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        15,
        16,
        17,
        18,
        20,
        21,
        22,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        144,
        145,
        147,
        152,
        153,
        154,
        155,
        156,
        157,
        158,
        159,
        160,
        161,
        165,
        166,
        171,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "ordered_before",
        "before": "QueueInsert",
        "after": "InvalidHeadSkip",
        "required_prior": null,
        "scope_identity": null,
        "scope_index": {
          "name": "slot",
          "relation": "same"
        }
      },
      "derived_from_case_ids": [
        "C1_EnqueueAdmitted",
        "C5_InvalidHeadSkipped"
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        15,
        16,
        17,
        18,
        20,
        21,
        22,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        53,
        54,
        55,
        56,
        57,
        58,
        60,
        61,
        66,
        67,
        68,
        69,
        70,
        71,
        73,
        74,
        79,
        80,
        81,
        82,
        83,
        84,
        86,
        87,
        92,
        93,
        94,
        95,
        96,
        97,
        99,
        100,
        105,
        106,
        107,
        108,
        109,
        110,
        112,
        113,
        118,
        119,
        120,
        121,
        122,
        123,
        125,
        126,
        131,
        132,
        133,
        134,
        135,
        136,
        138,
        139,
        144,
        145,
        147,
        152,
        153,
        154,
        155,
        156,
        157,
        158,
        159,
        160,
        161,
        171,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "DeqHandshake",
        "source": {
          "op": "signal",
          "name": "out"
        },
        "target": "io.deq.bits",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_VisibleDequeue"
      ],
      "evidence_statement_ids": [
        167,
        168,
        169,
        170,
        174
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This BranchKillableQueue has two distinct notions of enqueue: EnqHandshake is the external Decoupled acceptance event, while QueueInsert is the internal surviving insertion after branch-mispredict and flush filtering.",
    "A2 gives an exact disjoint classification of every external enqueue handshake. QueueInsert covers the surviving case; BranchKilledEnqueue classifies every handshake whose branch mask intersects the current mispredict mask; FlushKilledEnqueue is the residual flush-killed case when branch killing did not already classify the handshake.",
    "The residual definition of FlushKilledEnqueue is intentional because branch kill and flush may be asserted simultaneously. Using two independent killed occurrences would violate the pairwise-exclusion requirement of occurrence_partition.",
    "A3 and A4 make the branch/flush insertion exclusion explicit even though it is also embedded in the exact QueueInsert grounding.",
    "Already-resident entries have independent valid bits. Each valid bit is cleared when its stored uop branch mask intersects the current mispredict mask or whenever io.flush is asserted. Stored uop branch masks are also reduced by the resolve mask while valid.",
    "The per-entry branch/flush invalidation transition is not exported as eight separate semantic events. Its memory-order-relevant consequence is preserved by HeadInvalid and InvalidHeadSkip: killed retry operations disappear without generating a visible dequeue.",
    "HeadAdvance is required because this queue can advance the physical dequeue pointer without io.deq.fire. A6 exactly divides every pointer advance into either a visible DeqHandshake or an InvalidHeadSkip.",
    "A7 and A8 preserve the visible-versus-silent distinction at the head: only valid entries may generate DeqHandshake, while only invalid entries may be silently skipped.",
    "QueueFull and QueueEmpty preserve the pointer/maybe_full occupancy exclusions without exposing the raw pointer arithmetic as parent-visible semantics.",
    "A9 preserves the full retry payload written to RAM at insertion. The separately stored uops array is intentionally not equated to the original uop for all future cycles because its br_mask is legitimately rewritten as resolved branches are removed.",
    "A10 preserves same-slot history for visible retry delivery. Since all valid bits reset to false, a slot cannot generate a visible dequeue before some prior QueueInsert has populated that physical slot.",
    "A11 similarly preserves that an invalid slot skipped by the dequeue pointer must derive from a previously populated slot that later became invalid. This prevents abstract invalid-head skips from appearing out of never-used reset slots.",
    "A12 preserves the current dequeue payload wiring. The uop portion comes from the mutable uops array rather than directly from the original RAM copy so that branch-mask resolution is reflected at output.",
    "No architectural identity key is introduced from rob_idx, ldq_idx, or stq_idx because this queue does not itself establish global uniqueness of those fields.",
    "A stronger global FIFO-order theorem across different physical slots is omitted. The concrete ring pointers enforce it, but omitting it only widens the abstraction and is a valid future CEGAR refinement if a parent-level counterexample depends on cross-slot order.",
    "No fairness, eventual retry, eventual dequeue, or eventual head cleanup property is claimed."
  ],
  "extensions": {}
}