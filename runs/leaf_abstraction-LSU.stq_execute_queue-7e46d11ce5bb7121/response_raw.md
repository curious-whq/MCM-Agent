{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121",
  "work_unit_id": "LSU.stq_execute_queue",
  "occurrences": [
    {
      "id": "EnqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.stq_execute_queue::io.enq.fire"
      ],
      "definition": "io.enq.valid && io.enq.ready; one STQ execute entry is accepted into the queue",
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
        11,
        12,
        13,
        47,
        48
      ]
    },
    {
      "id": "QueueInsert",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "do_enq; the accepted STQ execute entry is written into ram at the current enqueue slot",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 4
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
        11,
        12,
        13,
        17,
        18,
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
        30,
        31,
        32
      ]
    },
    {
      "id": "DeqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU.stq_execute_queue::io.deq.fire"
      ],
      "definition": "io.deq.valid && io.deq.ready; the current head STQ execute entry is accepted by the consumer",
      "multiplicity": "repeatable",
      "index": {
        "name": "slot",
        "domain": {
          "start": 0,
          "end_exclusive": 4
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
        14,
        15,
        16,
        33,
        34,
        35,
        36,
        37,
        45,
        46,
        49,
        50
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
        7,
        10,
        47,
        48
      ]
    },
    {
      "id": "QueueEmpty",
      "definition": "empty; enqueue and dequeue pointers match while maybe_full is clear",
      "grounding": {
        "source_signal": "empty",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        7,
        8,
        9,
        45,
        46
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Enqueue",
      "trigger_occurrences": [
        "EnqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "QueueFull",
          "positive": false
        }
      ],
      "emits": [
        "QueueInsert"
      ],
      "relations": [
        "Every accepted enqueue is written into the current enqueue slot and advances the enqueue pointer modulo four."
      ],
      "evidence_statement_ids": [
        11,
        12,
        13,
        17,
        18,
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
        30,
        31,
        32,
        47,
        48
      ],
      "confidence": "high"
    },
    {
      "id": "C2_Dequeue",
      "trigger_occurrences": [
        "DeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "QueueEmpty",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "Every accepted dequeue reads the current dequeue slot and advances the dequeue pointer modulo four."
      ],
      "evidence_statement_ids": [
        14,
        15,
        16,
        33,
        34,
        35,
        36,
        37,
        45,
        46,
        49,
        50
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
      "derived_from_case_ids": [
        "C1_Enqueue"
      ],
      "evidence_statement_ids": [
        7,
        10,
        11,
        12,
        13,
        47,
        48
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "DeqHandshake",
        "predicate": "QueueEmpty",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Dequeue"
      ],
      "evidence_statement_ids": [
        7,
        8,
        9,
        14,
        15,
        16,
        45,
        46
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "occurrence_partition",
        "whole": "EnqHandshake",
        "parts": [
          "QueueInsert"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Enqueue"
      ],
      "evidence_statement_ids": [
        11,
        12,
        13,
        17
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
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
        "C1_Enqueue"
      ],
      "evidence_statement_ids": [
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
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
        "C1_Enqueue",
        "C2_Dequeue"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        17,
        18,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        45,
        46,
        47,
        48,
        49,
        50
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "DeqHandshake",
        "source": {
          "op": "signal",
          "name": "io_deq_bits_MPORT"
        },
        "target": "io.deq.bits",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Dequeue"
      ],
      "evidence_statement_ids": [
        49,
        50
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This is a conventional four-entry Decoupled FIFO used for STQ execute entries. The semantically relevant milestones are acceptance at the enqueue boundary, the concrete RAM insertion, and acceptance at the dequeue boundary.",
    "QueueInsert is separated from EnqHandshake so that it can carry the physical queue-slot index enq_ptr_value. In this unfiltered standard Queue implementation the two occur exactly together, expressed by A3.",
    "QueueFull and QueueEmpty are persistent implementation predicates derived from the pointer equality and maybe_full state. A1 and A2 preserve the exact no-overflow/no-underflow exclusions implemented by io.enq.ready and io.deq.valid.",
    "A4 preserves the entire STQEntry payload written into the current queue RAM slot rather than enumerating the large MicroOp bundle field by field.",
    "DeqHandshake is indexed by deq_ptr_value. A5 preserves the grounded same-slot history guarantee: a physical slot cannot be dequeued before that slot has been populated by a QueueInsert.",
    "A6 preserves that the dequeue payload comes directly from the queue RAM read port selected by deq_ptr_value.",
    "The queue RAM has no grounded reset initialization. No initial payload value is therefore claimed; the reset guarantees arise only from enq_ptr_value=0, deq_ptr_value=0, and maybe_full=0, which make the queue empty and prevent any dequeue until an insertion occurs.",
    "The candidate intentionally does not introduce an architectural transaction identity from rob_idx, stq_idx, or other payload fields. This leaf does not itself guarantee uniqueness of those values.",
    "A global cross-slot FIFO-order theorem between arbitrary pairs of enqueue/dequeue events is not emitted. The pointer implementation enforces it concretely, but omitting that stronger relational summary only widens the µMCM and can be refined later by CEGAR if a parent counterexample depends on cross-slot ordering.",
    "io.count and the exact occupancy arithmetic are omitted because full/empty plus slot history preserve the ordering-relevant behavior needed at this abstraction boundary.",
    "No fairness, eventual dequeue, or eventual enqueue property is claimed."
  ],
  "extensions": {}
}