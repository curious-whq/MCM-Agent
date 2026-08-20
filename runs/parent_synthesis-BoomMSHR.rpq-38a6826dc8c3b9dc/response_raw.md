{
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc",
  "work_unit_id": "BoomMSHR.rpq",
  "occurrences": [
    {
      "id": "ParentEnqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR.rpq::io.enq.fire"
      ],
      "definition": "io.enq.valid && io.enq.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        9
      ]
    },
    {
      "id": "ParentDeqHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR.rpq::io.deq.fire"
      ],
      "definition": "io.deq.valid && io.deq.ready",
      "multiplicity": "repeatable",
      "index": null,
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
        136,
        155
      ]
    },
    {
      "id": "BufferCapture",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "_T_2 && _out_valid_T_15; the wrapper refill window is active and the exposed child dequeue is valid and survives branch/flush filtering, so the child payload is captured into the output buffer and out_valid is set",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "_T_2",
          "_out_valid_T_15"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        170,
        171,
        172,
        173,
        174,
        175
      ]
    }
  ],
  "predicates": [
    {
      "id": "OutputInvalid",
      "definition": "out_valid == 0",
      "grounding": {
        "source_signal": "out_valid",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        7,
        136,
        156
      ]
    },
    {
      "id": "TransferBranchKilled",
      "definition": "(io.brupdate.b1.mispredict_mask & main.io.deq.bits.uop.br_mask) != 0",
      "grounding": {
        "source_signal": "_out_valid_T_9",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        159,
        160
      ]
    },
    {
      "id": "TransferFlushKilled",
      "definition": "io.flush && main.io.deq.bits.uop.uses_ldq",
      "grounding": {
        "source_signal": "_out_valid_T_13",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        164
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_EnqueueForwarded",
      "trigger_occurrences": [
        "ParentEnqHandshake"
      ],
      "guard_predicates": [],
      "emits": [
        "BoomMSHR.rpq.main::EnqHandshake"
      ],
      "relations": [
        "The parent enqueue interface is directly connected to the frozen child enqueue interface, so the parent handshake is the same forwarded enqueue transaction observed by the child."
      ],
      "evidence_statement_ids": [
        9
      ],
      "confidence": "high"
    },
    {
      "id": "C2_ChildDequeueCaptured",
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "TransferBranchKilled",
          "positive": false
        },
        {
          "id": "TransferFlushKilled",
          "positive": false
        }
      ],
      "emits": [
        "BufferCapture"
      ],
      "relations": [
        "A child dequeue accepted during the refill window becomes a valid buffered parent-visible item when it survives the parent-local branch and flush filters."
      ],
      "evidence_statement_ids": [
        154,
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        170,
        171,
        172,
        173,
        174,
        175
      ],
      "confidence": "high"
    },
    {
      "id": "C3_ChildDequeueBranchKilled",
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "TransferBranchKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A child dequeue may be consumed by the wrapper without becoming a valid buffered output when its uop is killed by the current branch update."
      ],
      "evidence_statement_ids": [
        158,
        159,
        160,
        161,
        162,
        163,
        167,
        175
      ],
      "confidence": "high"
    },
    {
      "id": "C4_ChildDequeueFlushKilled",
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "TransferFlushKilled",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A child dequeue may be consumed by the wrapper without becoming a valid buffered output when flush kills the dequeued uses_ldq uop."
      ],
      "evidence_statement_ids": [
        158,
        163,
        164,
        165,
        166,
        167,
        175
      ],
      "confidence": "high"
    },
    {
      "id": "C5_VisibleParentDequeue",
      "trigger_occurrences": [
        "ParentDeqHandshake"
      ],
      "guard_predicates": [
        {
          "id": "OutputInvalid",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "A parent-visible dequeue consumes a previously valid output-buffer entry; reset initializes the output buffer invalid."
      ],
      "evidence_statement_ids": [
        7,
        136,
        155
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ParentEnqHandshake",
        "predicate": "BoomMSHR.rpq.main::QueueFull",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_EnqueueForwarded"
      ],
      "evidence_statement_ids": [
        9
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ParentDeqHandshake",
        "predicate": "OutputInvalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        155
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "ordered_before",
        "before": "BufferCapture",
        "after": "ParentDeqHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        153,
        157,
        158,
        167,
        175
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "ordered_before",
        "before": "BoomMSHR.rpq.main::DeqHandshake",
        "after": "ParentDeqHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        154,
        155,
        157,
        158,
        167,
        175
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "ordered_before",
        "before": "BoomMSHR.rpq.main::QueueInsert",
        "after": "ParentDeqHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        154,
        155,
        157,
        158,
        167,
        175
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "forbid_when",
        "occurrence": "BufferCapture",
        "predicate": "TransferBranchKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C3_ChildDequeueBranchKilled"
      ],
      "evidence_statement_ids": [
        159,
        160,
        161,
        162,
        163,
        166,
        167
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "forbid_when",
        "occurrence": "BufferCapture",
        "predicate": "TransferFlushKilled",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C4_ChildDequeueFlushKilled"
      ],
      "evidence_statement_ids": [
        163,
        164,
        165,
        166,
        167
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The parent wrapper adds a one-entry output buffer in front of the frozen child. Parent enqueue is directly forwarded to the child, while parent-visible dequeue is driven only by out_valid.",
    "A child dequeue is not guaranteed to become parent-visible: the wrapper may consume the child transfer while suppressing out_valid when the transferred uop is killed by the current branch update or flush. Therefore no liveness or one-for-one child-dequeue-to-parent-dequeue conservation axiom is claimed.",
    "A3 captures the parent-local valid-token provenance of the output buffer. A4 exposes the corresponding child-to-parent path explicitly so higher-level composition does not treat parent dequeues as unrelated to the frozen child dequeue stream.",
    "A5 is an emergent weakening of the frozen child A11: the child proves same-slot QueueInsert-before-DeqHandshake, while the parent wrapper hides the child slot index. Dropping the slot scope yields the conservative parent-facing fact that every visible parent dequeue has some prior frozen-child QueueInsert.",
    "No new transaction identity_key is claimed. The frozen child has no trusted identity key, and the wrapper splits payload state between out_reg and a separately rewritten out_uop whose br_mask changes under branch resolution. Claiming exact same-request identity across the complete queue would therefore exceed the trusted child semantics.",
    "Exact parent-output aggregate equality is deliberately omitted. io.deq.bits is sourced from out_reg but its uop subaggregate is overwritten by out_uop, and out_uop.br_mask is updated over time. Omitting stronger field-level payload equalities is a safe over-approximation that can be refined later by CEGAR if needed."
  ],
  "extensions": {
    "parent_synthesis": {
      "axiom_provenance": {
        "A1": {
          "kind": "lifted",
          "source_axioms": [
            "BoomMSHR.rpq.main::A1"
          ],
          "note": "Lift the frozen child QueueFull exclusion to the parent enqueue boundary through the direct parent-child enqueue connection."
        },
        "A2": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Parent dequeue valid is exactly out_valid, which is reset false."
        },
        "A3": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The parent-local one-entry buffer can produce a visible dequeue only after a surviving BufferCapture created its valid token."
        },
        "A4": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Uses the exposed frozen-child dequeue occurrence plus the parent-local refill/valid protocol; no child axiom is needed for this path fact."
        },
        "A5": {
          "kind": "emergent",
          "source_axioms": [
            "BoomMSHR.rpq.main::A11"
          ],
          "note": "Compose the child's same-slot QueueInsert-before-DeqHandshake guarantee with the parent output-buffer path, weakening away the hidden child slot index at the parent boundary."
        },
        "A6": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The parent-local capture-valid expression explicitly excludes a branch-killed child transfer."
        },
        "A7": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The parent-local capture-valid expression explicitly excludes a flush-killed child transfer."
        }
      }
    }
  }
}