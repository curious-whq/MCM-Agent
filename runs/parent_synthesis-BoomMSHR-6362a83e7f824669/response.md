{
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHR-6362a83e7f824669",
  "work_unit_id": "BoomMSHR",
  "occurrences": [
    {
      "id": "PrimaryAccept",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "(state == s_invalid || state == s_prefetch) && io.req_pri_val && io.req_pri_rdy; a primary request is accepted and becomes the current MSHR request",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          0,
          17
        ],
        "signals_true": [
          "io.req_pri_val",
          "io.req_pri_rdy"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1102,
        1103,
        1104,
        1106,
        1107,
        1119,
        1346,
        1840,
        1841,
        1842,
        1974,
        1975,
        1988,
        2215
      ]
    },
    {
      "id": "MemAcquire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.mem_acquire.fire"
      ],
      "definition": "state == s_refill_req && io.mem_acquire.valid && io.mem_acquire.ready",
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
        1348,
        1349,
        1350,
        1351,
        1352,
        1353
      ]
    },
    {
      "id": "MemGrant",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.mem_grant.fire"
      ],
      "definition": "state == s_refill_resp && io.mem_grant.valid && io.mem_grant.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          2
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1355,
        1356,
        1357,
        1363,
        1364
      ]
    },
    {
      "id": "GrantDataWrite",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.lb_write.valid"
      ],
      "definition": "state == s_refill_resp && io.lb_write.valid; a data-bearing memory Grant is forwarded into the line buffer",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          2
        ],
        "signals_true": [
          "io.lb_write.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1355,
        1356,
        1358,
        1359,
        1360
      ]
    },
    {
      "id": "GrantComplete",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_refill_resp && refill_done; the final accepted TileLink Grant beat completes the memory response and captures GrantAck/coherence state",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          2
        ],
        "signals_true": [
          "refill_done"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        604,
        614,
        615,
        616,
        617,
        618,
        1367,
        1372,
        1375,
        1377
      ]
    },
    {
      "id": "MetaRead",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.meta_read.fire"
      ],
      "definition": "state == s_meta_read && io.meta_read.valid && io.meta_read.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          4
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1525,
        1526,
        1527,
        1528,
        1529,
        1530,
        1531,
        1532,
        1533,
        1534,
        1535,
        1536
      ]
    },
    {
      "id": "MetaClearWrite",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_meta_clear && io.meta_write.valid && io.meta_write.ready; the victim metadata is cleared before writeback",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          7
        ],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1618,
        1619,
        1620,
        1621,
        1622,
        1623
      ]
    },
    {
      "id": "WBReq",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.wb_req.fire"
      ],
      "definition": "state == s_wb_req && io.wb_req.valid && io.wb_req.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          9
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1625,
        1626,
        1627,
        1628,
        1629,
        1630
      ]
    },
    {
      "id": "WBComplete",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_wb_resp && io.wb_resp; the requested victim writeback has completed",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          10
        ],
        "signals_true": [
          "io.wb_resp"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1632,
        1633,
        1634,
        1635
      ]
    },
    {
      "id": "CommitRefillBeat",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.refill.fire"
      ],
      "definition": "state == s_commit_line && io.refill.valid && io.refill.ready; one cache-line commit beat is accepted",
      "multiplicity": "repeatable",
      "index": {
        "name": "beat",
        "expr": {
          "op": "signal",
          "name": "refill_ctr"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 8
        }
      },
      "grounding": {
        "state_register": "state",
        "state_values": [
          11
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1637,
        1638,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645
      ]
    },
    {
      "id": "CommitRefillDone",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_commit_line && io.refill.fire && refill_ctr == 7; the eighth and final commit refill beat is accepted and the MSHR enters replay drain",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          11
        ],
        "signals_true": [
          "_T_44",
          "_T_45"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ]
    },
    {
      "id": "RespHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.resp.fire"
      ],
      "definition": "state == s_drain_rpq_loads && io.resp.valid && io.resp.ready; a load replay-queue entry is returned directly as a load response",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          3
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ]
    },
    {
      "id": "ReplayHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.replay.fire"
      ],
      "definition": "state == s_drain_rpq && io.replay.valid && io.replay.ready; an RPQ entry is emitted through the replay interface",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          12
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1650,
        1651,
        1652,
        1653,
        1654,
        1660
      ]
    },
    {
      "id": "RPQDrained",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_drain_rpq && rpq.io.empty && !rpq.io.enq.valid; no queued or concurrently incoming replay remains, so the MSHR may proceed to final metadata commit",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          12
        ],
        "signals_true": [
          "_T_76"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811
      ]
    },
    {
      "id": "FinalMetaWrite",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_meta_write_req && io.meta_write.valid && io.meta_write.ready; the final acquired-line metadata is committed after RPQ drain",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          13
        ],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1813,
        1814,
        1815,
        1816,
        1817,
        1818,
        1819,
        1820,
        1821,
        1822
      ]
    },
    {
      "id": "MemFinish",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHR::io.mem_finish.fire"
      ],
      "definition": "state == s_mem_finish_1 && io.mem_finish.valid && io.mem_finish.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": "state",
        "state_values": [
          14
        ],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1089,
        1825,
        1826,
        1827,
        1828
      ]
    }
  ],
  "predicates": [
    {
      "id": "GrantAckAbsent",
      "definition": "grantack.valid == 0",
      "grounding": {
        "source_signal": "grantack.valid",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        900,
        1110,
        1372,
        1827,
        1832
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_GrantCompleted",
      "trigger_occurrences": [
        "GrantComplete"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The memory response completes only after the MSHR has issued its current Acquire; the completed Grant may subsequently feed direct load responses, metadata processing, or replay drain."
      ],
      "evidence_statement_ids": [
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364,
        1367,
        1372,
        1375,
        1377
      ],
      "confidence": "high"
    },
    {
      "id": "C2_LoadResponse",
      "trigger_occurrences": [
        "RespHandshake"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "A direct load response occurs only on the post-Grant load-drain path and consumes an entry from the frozen RPQ dequeue stream."
      ],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ],
      "confidence": "high"
    },
    {
      "id": "C3_VictimWriteback",
      "trigger_occurrences": [
        "WBComplete"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The victim-writeback path performs a metadata read, clears the victim metadata, issues a writeback request, and waits for io.wb_resp before entering line commit."
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "confidence": "high"
    },
    {
      "id": "C4_CommitLineRefill",
      "trigger_occurrences": [
        "CommitRefillDone"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The commit-line phase emits exactly the eight refill indices 0 through 7 before entering replay drain."
      ],
      "evidence_statement_ids": [
        1637,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ],
      "confidence": "high"
    },
    {
      "id": "C5_ReplayDrain",
      "trigger_occurrences": [
        "ReplayHandshake"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "Replay handshakes are direct parent-local exposures of the frozen RPQ dequeue stream while state is s_drain_rpq."
      ],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "confidence": "high"
    },
    {
      "id": "C6_FinalMetadataCommit",
      "trigger_occurrences": [
        "FinalMetaWrite"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The final metadata update is reached only after the replay queue is observed empty with no concurrent enqueue."
      ],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "confidence": "high"
    },
    {
      "id": "C7_GrantFinish",
      "trigger_occurrences": [
        "MemFinish"
      ],
      "guard_predicates": [
        {
          "id": "GrantAckAbsent",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "A visible TileLink GrantAck handshake requires a valid stored grant acknowledgement derived from an earlier completed Grant."
      ],
      "evidence_statement_ids": [
        1089,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "ordered_before",
        "before": "PrimaryAccept",
        "after": "MemAcquire",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1102,
        1104,
        1106,
        1107,
        1119,
        1346,
        1348,
        1350,
        1351,
        1352,
        1353,
        1840,
        1842,
        1974,
        1975,
        1988,
        2215
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "ordered_before",
        "before": "MemAcquire",
        "after": "MemGrant",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1348,
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "ordered_before",
        "before": "GrantComplete",
        "after": "RespHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1444,
        1455,
        1456,
        1459,
        1460
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "ordered_before",
        "before": "GrantComplete",
        "after": "MetaRead",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1525,
        1526,
        1533,
        1534,
        1535,
        1536
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "ordered_chain",
        "sequence": [
          "MetaRead",
          "MetaClearWrite",
          "WBReq",
          "WBComplete"
        ],
        "scope_identity": null,
        "scope_index": null
      },
      "derived_from_case_ids": [
        "C3_VictimWriteback"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "ordered_before",
        "before": "MetaRead",
        "after": "CommitRefillBeat",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1637,
        1640,
        1641,
        1642
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "indexed_complete",
        "occurrence": "CommitRefillBeat",
        "completion": "CommitRefillDone",
        "index": "beat",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "cardinality": "exactly_once",
        "scope_identity": null,
        "scope_index": null
      },
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1111,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648,
        1980
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "ordered_before",
        "before": "RPQDrained",
        "after": "FinalMetaWrite",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C6_FinalMetadataCommit"
      ],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "ordered_before",
        "before": "GrantComplete",
        "after": "MemFinish",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1367,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MemFinish",
        "predicate": "GrantAckAbsent",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1825,
        1827,
        1828,
        1829,
        1830,
        1831,
        1832
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "GrantDataWrite",
        "target": "io.lb_write.bits.data",
        "source": {
          "op": "signal",
          "name": "io.mem_grant.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1093,
        1358,
        1359,
        1360
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "CommitRefillBeat",
        "target": "io.refill.bits.data",
        "source": {
          "op": "signal",
          "name": "io.lb_resp"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1067,
        1637,
        1640,
        1641
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "MemFinish",
        "target": "io.mem_finish.bits.sink",
        "source": {
          "op": "signal",
          "name": "grantack.bits.sink"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1089,
        1374,
        1375,
        1827,
        1828
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "ordered_before",
        "before": "BoomMSHR.rpq.main::QueueInsert",
        "after": "RespHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "ordered_before",
        "before": "BoomMSHR.rpq.main::QueueInsert",
        "after": "ReplayHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_ReplayDrain"
      ],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The frozen BoomMSHR.rpq child is imported rather than copied. Parent-local semantics retain only the MSHR-level paths that connect request acceptance, TileLink Acquire/Grant traffic, metadata/writeback processing, line refill, RPQ response/replay consumption, and GrantAck completion.",
    "PrimaryAccept is retained as a derived occurrence because the MSHR has no physical request-fire boundary event in this WorkUnit, yet request acceptance is the transaction-start milestone that grounds later Acquire ordering.",
    "GrantComplete is retained because a single Acquire may receive multiple Grant beats and only refill_done closes that response sequence, captures GrantAck/coherence information, and permits progression beyond s_refill_resp.",
    "MetaClearWrite and FinalMetaWrite intentionally distinguish the two uses of the same physical io.meta_write.fire interface: the first clears victim metadata before writeback, while the second commits final acquired-line metadata only after RPQ drain.",
    "CommitRefillBeat uses the existing generic indexed-occurrence language. refill_ctr is initialized to zero for a new primary request and advances once per accepted refill beat; the last accepted value 7 moves the MSHR to replay drain, giving an eight-element domain [0,8).",
    "RPQDrained is retained as a parent-local milestone instead of attempting universal quantification over every replay entry. The exact transition condition rpq.io.empty && !rpq.io.enq.valid is sufficient to preserve the important fact that final metadata commit cannot begin while queued or concurrently arriving replay work remains.",
    "A14 and A15 lift the frozen RPQ queue provenance to the two parent-visible consumption paths. BoomMSHR.rpq::A5 already guarantees a prior descendant QueueInsert for every frozen-child dequeue; parent-local wiring makes RespHandshake and ReplayHandshake restricted subsets of that dequeue stream. If the current composition prover cannot restrict the after-event of a trusted history theorem, that is a reusable composition-prover gap rather than a language gap.",
    "No new parent identity_key is claimed. The current request register may be modified by accepted secondary misses, especially req.uop.mem_cmd, while the frozen RPQ exposes no trusted transaction identity key. Omitting stronger same-request claims is therefore conservative.",
    "Probe blocking through meta_hazard is intentionally not promoted into a mandatory parent axiom. It is coherence-relevant, but omitting that strengthening only allows additional probe behavior in the abstraction and can be revisited through CEGAR if a spurious system trace depends on it.",
    "AcquireBlock opcode/source/address constants and the voluntary bit on wb_req are also omitted as optional local strengthenings. The retained abstraction focuses on ordering, visibility, conservation, replay provenance, and data-transfer facts needed by higher-level memory-model composition.",
    "No liveness or eventual response/replay/refill/finish property is claimed; no ready/valid fairness assumption is required."
  ],
  "extensions": {
    "parent_synthesis": {
      "axiom_provenance": {
        "A1": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Primary request acceptance is the only parent-local path that establishes a request before later s_refill_req Acquire traffic."
        },
        "A2": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The MSHR enters s_refill_resp only after an accepted Acquire, so every accepted Grant has a prior Acquire in the same MSHR lifecycle."
        },
        "A3": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Direct load responses occur only in s_drain_rpq_loads, which is reachable from the completed data-Grant path."
        },
        "A4": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Metadata-read processing is downstream of a completed Grant, including the retained-prefetch path whose acquired line remains live across s_prefetch."
        },
        "A5": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The victim-writeback control path orders successful MetaRead before victim metadata clear, writeback request, and writeback response."
        },
        "A6": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The s_commit_line refill phase is entered only through metadata-response processing, with optional victim writeback in between."
        },
        "A7": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The three-bit refill_ctr and last-beat transition establish exact bounded eight-beat commit-line coverage."
        },
        "A8": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The only transition into s_meta_write_req requires rpq.io.empty and no concurrent RPQ enqueue."
        },
        "A9": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "A visible MemFinish requires the GrantAck valid token, which is created from the completed TileLink Grant response."
        },
        "A10": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.mem_finish.valid is driven by grantack.valid, making a finish handshake impossible when the stored GrantAck is absent."
        },
        "A11": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The line-buffer write payload is directly driven from the current memory Grant data."
        },
        "A12": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Every commit-line refill beat takes its data directly from io.lb_resp."
        },
        "A13": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The MemFinish sink is the sink captured into grantack.bits from the completed Grant."
        },
        "A14": {
          "kind": "emergent",
          "source_axioms": [
            "BoomMSHR.rpq::A5"
          ],
          "note": "Compose frozen RPQ QueueInsert-before-dequeue provenance with the parent-local direct-load response subset of the RPQ dequeue stream."
        },
        "A15": {
          "kind": "emergent",
          "source_axioms": [
            "BoomMSHR.rpq::A5"
          ],
          "note": "Compose frozen RPQ QueueInsert-before-dequeue provenance with the parent-local replay handshake subset of the RPQ dequeue stream."
        }
      }
    }
  }
}