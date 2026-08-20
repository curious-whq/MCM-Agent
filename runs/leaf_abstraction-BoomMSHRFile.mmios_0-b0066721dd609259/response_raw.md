{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259",
  "work_unit_id": "BoomMSHRFile.mmios_0",
  "occurrences": [
    {
      "id": "ReqAccept",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.req.fire"
      ],
      "definition": "io.req.valid && io.req.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          0
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6,
        7,
        1601,
        1602
      ]
    },
    {
      "id": "MemAccess",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.mem_access.fire"
      ],
      "definition": "io.mem_access.valid && io.mem_access.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          1
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1481,
        1482,
        1605,
        1606
      ]
    },
    {
      "id": "MemAckValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.mem_ack.valid"
      ],
      "definition": "io.mem_ack.valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.mem_ack.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1609
      ]
    },
    {
      "id": "AckConsumed",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == 2 && io.mem_ack.valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          2
        ],
        "signals_true": [
          "io.mem_ack.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1608,
        1609,
        1610,
        1611
      ]
    },
    {
      "id": "RespHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.resp.fire"
      ],
      "definition": "io.resp.valid && io.resp.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          3
        ],
        "signals_true": [
          "send_resp"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1645
      ]
    }
  ],
  "predicates": [
    {
      "id": "Busy",
      "definition": "state != 0",
      "grounding": {
        "source_signal": null,
        "negated": false,
        "state_register": "state",
        "state_values": [
          1,
          2,
          3
        ]
      },
      "evidence_statement_ids": [
        5,
        1604,
        1607,
        1611,
        1648
      ]
    },
    {
      "id": "NoResponseRequired",
      "definition": "!send_resp",
      "grounding": {
        "source_signal": "send_resp",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        1528,
        1529,
        1530,
        1531,
        1532,
        1533,
        1534,
        1535,
        1536,
        1537,
        1538,
        1539,
        1540,
        1541,
        1542,
        1543,
        1544,
        1545,
        1546,
        1547,
        1548,
        1549,
        1550,
        1551,
        1552
      ]
    }
  ],
  "identity_keys": [
    {
      "id": "RequestIdentity",
      "carrier_state": "req",
      "fields": [
        "addr",
        "uop.rob_idx",
        "uop.ldq_idx",
        "uop.stq_idx",
        "uop.mem_cmd",
        "uop.mem_size"
      ],
      "description": "The accepted MMIO request is stored in req and remains the single outstanding transaction context until the MSHR returns to idle.",
      "evidence_statement_ids": [
        3,
        1603
      ]
    }
  ],
  "cases": [
    {
      "id": "C1_RequestCaptured",
      "trigger_occurrences": [
        "ReqAccept"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The accepted request is captured into req and the FSM enters the memory-access state."
      ],
      "evidence_statement_ids": [
        1601,
        1602,
        1603,
        1604
      ],
      "confidence": "high"
    },
    {
      "id": "C2_ResponseProducingAck",
      "trigger_occurrences": [
        "AckConsumed"
      ],
      "guard_predicates": [
        {
          "id": "NoResponseRequired",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "A consumed acknowledgement for a read-like request moves the FSM to the response state; read-return data is captured into grant_word and io.resp.valid is asserted from that state."
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1608,
        1609,
        1610,
        1611,
        1637,
        1638,
        1639,
        1640,
        1641
      ],
      "confidence": "high"
    },
    {
      "id": "C3_NoResponseAck",
      "trigger_occurrences": [
        "AckConsumed"
      ],
      "guard_predicates": [
        {
          "id": "NoResponseRequired",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A consumed acknowledgement for a request with send_resp false reaches the response state but cannot produce RespHandshake and returns to idle without waiting for io.resp.ready."
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1608,
        1609,
        1610,
        1611,
        1642,
        1643,
        1644,
        1646,
        1647,
        1648
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ReqAccept",
        "predicate": "Busy",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        6,
        7,
        1601
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "ordered_before",
        "before": "ReqAccept",
        "after": "MemAccess",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        1481,
        1482,
        1601,
        1602,
        1603,
        1604,
        1605,
        1606,
        1607
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "ordered_before",
        "before": "MemAccess",
        "after": "AckConsumed",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ResponseProducingAck",
        "C3_NoResponseAck"
      ],
      "evidence_statement_ids": [
        1605,
        1606,
        1607,
        1608,
        1609,
        1610,
        1611
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "ordered_before",
        "before": "AckConsumed",
        "after": "RespHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1611,
        1642,
        1643,
        1645
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RespHandshake",
        "predicate": "NoResponseRequired",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_NoResponseAck"
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "identity_flow",
        "identity": "RequestIdentity",
        "capture": {
          "on": "ReqAccept",
          "source": "io.req.bits",
          "carrier": "req"
        },
        "projections": [
          {
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.rob_idx",
            "expr": {
              "op": "signal",
              "name": "req.uop.rob_idx"
            }
          },
          {
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.ldq_idx",
            "expr": {
              "op": "signal",
              "name": "req.uop.ldq_idx"
            }
          },
          {
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.stq_idx",
            "expr": {
              "op": "signal",
              "name": "req.uop.stq_idx"
            }
          },
          {
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.mem_cmd",
            "expr": {
              "op": "signal",
              "name": "req.uop.mem_cmd"
            }
          },
          {
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.mem_size",
            "expr": {
              "op": "signal",
              "name": "req.uop.mem_size"
            }
          }
        ]
      },
      "derived_from_case_ids": [
        "C1_RequestCaptured",
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1603,
        1556
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "MemAccess",
        "target": "io.mem_access.bits.address",
        "source": {
          "op": "slice",
          "value": {
            "op": "signal",
            "name": "req.addr"
          },
          "hi": 31,
          "lo": 0
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        79,
        224,
        361,
        489,
        617,
        745,
        873,
        1001,
        1129,
        1257,
        1385,
        1525,
        1526,
        1527
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "MemAccess",
        "target": "io.mem_access.bits.size",
        "source": {
          "op": "signal",
          "name": "req.uop.mem_size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        77,
        222,
        359,
        487,
        615,
        743,
        871,
        999,
        1127,
        1255,
        1383,
        1525,
        1526,
        1527
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "RespHandshake",
        "target": "io.resp.bits.is_hella",
        "source": {
          "op": "signal",
          "name": "req.is_hella"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1600
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [
    {
      "id": "E1_NoAcceptedXSC",
      "statement": "The environment must not supply an accepted request whose req.uop.mem_cmd is M_XSC (numeric value 7); after such a request leaves s_idle, the module-local assertion state === s_idle || req.uop.mem_cmd =/= M_XSC would fail.",
      "evidence_statement_ids": [
        1471,
        1472,
        1473,
        1474,
        1475,
        1476,
        1477,
        1478,
        1480,
        1603,
        1604
      ]
    }
  ],
  "unresolved": [],
  "rationale": [
    "BoomIOMSHR is a single-outstanding transaction machine. ReqAccept is possible only in state 0; acceptance captures io.req.bits into req and moves to state 1. MemAccess advances state 1 to state 2, and only a mem_ack.valid observed in state 2 is consumed and advances the machine to state 3.",
    "The raw physical MemAckValid occurrence is intentionally kept separate from the derived AckConsumed occurrence. io.mem_ack.valid may be asserted while the MSHR is in another state, but such a pulse is ignored by this RTL and therefore must not participate in the request lifecycle ordering.",
    "A2-A4 preserve the essential lifecycle ordering ReqAccept < MemAccess < AckConsumed < RespHandshake without asserting eventual progress. Any of the Decoupled stages may stall indefinitely if its environment does not provide readiness or acknowledgement.",
    "A1 captures the single-outstanding exclusion property: while state is 1, 2, or 3, io.req.ready is false and a second request cannot be accepted.",
    "send_resp is the RTL isRead(req.uop.mem_cmd) classification. A5 therefore preserves the important path distinction that requests for which send_resp is false cannot produce a core response handshake; those transactions return to idle directly from state 3.",
    "The req register is the persistent transaction carrier. A6 preserves architectural request identity across the multi-cycle transaction for ROB, LDQ, STQ, command, and size fields. The address is also retained in req and separately projected onto the memory-access boundary by A7.",
    "A7 and A8 retain the MMIO memory-object address and access size. The exact TileLink opcode/param/mask/data selection is command-dependent; omitting the complete mapping is a safe over-approximation and can be added later by CEGAR if a parent-level counterexample depends on operation-class details.",
    "For read-like requests, grant_word is captured from io.mem_ack.bits.data at AckConsumed and the response data is then transformed through LoadGen using req.addr, req.uop.mem_size, and req.uop.mem_signed. The current candidate deliberately omits this exact returned-data transformation because unconstrained response data is a safe over-approximation for this ordering abstraction; it is not treated as a language blocker.",
    "A9 preserves is_hella exactly because it is directly forwarded from the stored request and can change how the parent interprets the response.",
    "The module assertion excluding M_XSC outside idle is not an internally enforced input filter: io.req can physically accept such a request in s_idle. It is therefore recorded as an explicit environment assumption rather than misclassified as an RTL guarantee."
  ],
  "extensions": {}
}