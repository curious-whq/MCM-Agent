{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b",
  "work_unit_id": "BoomWritebackUnit",
  "occurrences": [
    {
      "id": "WritebackReq",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomWritebackUnit::io.req.fire"
      ],
      "definition": "io.req.fire",
      "multiplicity": "exactly_once",
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
        123
      ]
    },
    {
      "id": "FillIssue",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.data_req.fire && io.meta_read.fire",
      "multiplicity": "repeatable",
      "index": {
        "name": "beat",
        "expr": {
          "op": "signal",
          "name": "data_req_cnt"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 8
        }
      },
      "grounding": {
        "state_register": "state",
        "state_values": [
          1
        ],
        "signals_true": [
          "io.data_req.valid",
          "io.data_req.ready",
          "io.meta_read.valid",
          "io.meta_read.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        127,
        128,
        131,
        132,
        142,
        143,
        144,
        145,
        146,
        147,
        148,
        149,
        150
      ]
    },
    {
      "id": "BufferBeat",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "r2_data_req_fired && wb_buffer[r2_data_req_cnt] := io.data_resp",
      "multiplicity": "repeatable",
      "index": {
        "name": "beat",
        "expr": {
          "op": "signal",
          "name": "r2_data_req_cnt"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 8
        }
      },
      "grounding": {
        "state_register": "state",
        "state_values": [
          1
        ],
        "signals_true": [
          "r2_data_req_fired"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        140,
        141,
        151,
        152,
        153
      ]
    },
    {
      "id": "BufferFilled",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "last buffer beat is captured (r2_data_req_cnt == 7), io.resp is asserted, and state enters s_lsu_release",
      "multiplicity": "at_most_once",
      "grounding": {
        "state_register": "state",
        "state_values": [
          1
        ],
        "signals_true": [
          "r2_data_req_fired"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        151,
        152,
        153,
        154,
        155,
        156,
        157,
        158
      ]
    },
    {
      "id": "LSURelease",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomWritebackUnit::io.lsu_release.fire"
      ],
      "definition": "io.lsu_release.fire",
      "multiplicity": "at_most_once",
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        160,
        161,
        162,
        163,
        164,
        165,
        166
      ]
    },
    {
      "id": "ReleaseBeat",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomWritebackUnit::io.release.fire"
      ],
      "definition": "io.release.fire",
      "multiplicity": "repeatable",
      "index": {
        "name": "beat",
        "expr": {
          "op": "signal",
          "name": "data_req_cnt"
        },
        "domain": {
          "start": 0,
          "end_exclusive": 8
        }
      },
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        168,
        169,
        170,
        171,
        172,
        173,
        176,
        177,
        178,
        179,
        180
      ]
    },
    {
      "id": "ReleaseComplete",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_active && data_req_cnt == 7 && io.release.fire; the last network release beat is accepted",
      "multiplicity": "at_most_once",
      "grounding": {
        "state_register": "state",
        "state_values": [
          3
        ],
        "signals_true": [
          "io.release.valid",
          "io.release.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        181,
        182,
        183,
        184,
        185,
        186
      ]
    },
    {
      "id": "MemGrantSeen",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.mem_grant while the writeback transaction is in active/grant processing",
      "multiplicity": "repeatable",
      "grounding": {
        "state_register": "state",
        "state_values": [
          3,
          4
        ],
        "signals_true": [
          "io.mem_grant"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        174,
        175,
        188,
        189,
        190,
        191
      ]
    },
    {
      "id": "VoluntaryDone",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "state == s_grant && acked; state returns to s_invalid",
      "multiplicity": "at_most_once",
      "grounding": {
        "state_register": "state",
        "state_values": [
          4
        ],
        "signals_true": [
          "acked"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        188,
        189,
        190,
        191,
        192,
        193
      ]
    }
  ],
  "predicates": [
    {
      "id": "ActiveWriteback",
      "definition": "state != s_invalid",
      "grounding": {
        "source_signal": "io.idx.valid",
        "negated": false,
        "state_register": "state",
        "state_values": [
          1,
          2,
          3,
          4
        ]
      },
      "evidence_statement_ids": [
        32,
        33,
        34,
        115,
        116,
        120,
        125,
        126,
        160,
        161,
        168,
        169,
        188,
        189
      ]
    },
    {
      "id": "Voluntary",
      "definition": "req.voluntary",
      "grounding": {
        "source_signal": "req.voluntary",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3,
        122,
        172,
        185,
        186
      ]
    },
    {
      "id": "BeforeNetworkRelease",
      "definition": "state is s_fill_buffer or s_lsu_release",
      "grounding": {
        "source_signal": null,
        "negated": false,
        "state_register": "state",
        "state_values": [
          1,
          2
        ]
      },
      "evidence_statement_ids": [
        125,
        126,
        160,
        161,
        166
      ]
    },
    {
      "id": "GrantObserved",
      "definition": "acked",
      "grounding": {
        "source_signal": "acked",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        31,
        123,
        174,
        175,
        190,
        191,
        192,
        193
      ]
    }
  ],
  "identity_keys": [
    {
      "id": "WritebackTxn",
      "carrier_state": "req",
      "fields": [
        "tag",
        "idx",
        "source",
        "param",
        "way_en",
        "voluntary"
      ],
      "description": "The accepted WritebackReq is latched in req and carries the cache-line identity and writeback mode through the transaction.",
      "evidence_statement_ids": [
        3,
        60,
        61,
        118,
        119,
        120,
        122
      ]
    }
  ],
  "cases": [
    {
      "id": "ProbeWriteback",
      "trigger_occurrences": [
        "WritebackReq"
      ],
      "guard_predicates": [
        {
          "id": "Voluntary",
          "positive": false
        }
      ],
      "emits": [
        "FillIssue",
        "BufferBeat",
        "BufferFilled",
        "LSURelease",
        "ReleaseBeat",
        "ReleaseComplete"
      ],
      "relations": [
        "all buffer beats precede LSURelease",
        "network release beats use the non-voluntary probe-response path"
      ],
      "evidence_statement_ids": [
        120,
        122,
        125,
        126,
        127,
        128,
        131,
        132,
        145,
        150,
        151,
        153,
        154,
        155,
        156,
        157,
        160,
        162,
        163,
        164,
        165,
        166,
        168,
        170,
        171,
        172,
        173,
        176,
        180,
        181,
        183,
        184,
        185,
        186
      ],
      "confidence": "high"
    },
    {
      "id": "VoluntaryWriteback",
      "trigger_occurrences": [
        "WritebackReq"
      ],
      "guard_predicates": [
        {
          "id": "Voluntary",
          "positive": true
        }
      ],
      "emits": [
        "FillIssue",
        "BufferBeat",
        "BufferFilled",
        "LSURelease",
        "ReleaseBeat",
        "ReleaseComplete",
        "MemGrantSeen",
        "VoluntaryDone"
      ],
      "relations": [
        "all buffer beats precede LSURelease",
        "network release beats use the voluntary release path",
        "VoluntaryDone requires both ReleaseComplete and MemGrantSeen"
      ],
      "evidence_statement_ids": [
        120,
        122,
        125,
        126,
        127,
        128,
        131,
        132,
        145,
        150,
        151,
        153,
        154,
        155,
        156,
        157,
        160,
        162,
        163,
        164,
        165,
        166,
        168,
        170,
        171,
        172,
        173,
        174,
        175,
        176,
        180,
        181,
        183,
        184,
        185,
        186,
        188,
        190,
        191,
        192,
        193
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "WritebackReq",
        "predicate": "ActiveWriteback",
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        32,
        33,
        43,
        115,
        116,
        117,
        118,
        119,
        120,
        122
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "identity_flow",
        "identity": "WritebackTxn",
        "capture": {
          "on": "WritebackReq",
          "source": "io.req.bits",
          "carrier": "req"
        },
        "projections": [
          {
            "on": "FillIssue",
            "target": "io.meta_read.bits.idx",
            "expr": {
              "op": "signal",
              "name": "req.idx"
            }
          },
          {
            "on": "FillIssue",
            "target": "io.meta_read.bits.tag",
            "expr": {
              "op": "signal",
              "name": "req.tag"
            }
          },
          {
            "on": "FillIssue",
            "target": "io.data_req.bits.way_en",
            "expr": {
              "op": "signal",
              "name": "req.way_en"
            }
          },
          {
            "on": "LSURelease",
            "target": "io.lsu_release.bits.address",
            "expr": {
              "op": "signal",
              "name": "r_address"
            }
          },
          {
            "on": "LSURelease",
            "target": "io.lsu_release.bits.param",
            "expr": {
              "op": "signal",
              "name": "req.param"
            }
          },
          {
            "on": "LSURelease",
            "target": "io.lsu_release.bits.source",
            "expr": {
              "op": "signal",
              "name": "req.source"
            }
          }
        ]
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        3,
        60,
        61,
        65,
        67,
        68,
        109,
        112,
        118,
        122,
        129,
        130,
        133,
        163,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "indexed_complete",
        "occurrence": "BufferBeat",
        "completion": "BufferFilled",
        "index": "beat",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "cardinality": "exactly_once",
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        140,
        141,
        151,
        152,
        153,
        154,
        155,
        156,
        157
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "ordered_before",
        "before": "FillIssue",
        "after": "BufferBeat",
        "required_prior": null,
        "scope_identity": "WritebackTxn",
        "scope_index": {
          "name": "beat",
          "relation": "same"
        }
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        142,
        143,
        144,
        145,
        146,
        147,
        150,
        151,
        152,
        153
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "ordered_before",
        "before": "BufferFilled",
        "after": "LSURelease",
        "required_prior": null,
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        154,
        155,
        156,
        157,
        160,
        161,
        162,
        164,
        165,
        166
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ReleaseBeat",
        "predicate": "BeforeNetworkRelease",
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        160,
        161,
        166,
        168,
        169,
        170,
        171,
        176,
        177,
        180
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "indexed_complete",
        "occurrence": "ReleaseBeat",
        "completion": "ReleaseComplete",
        "index": "beat",
        "domain": {
          "start": 0,
          "end_exclusive": 8
        },
        "cardinality": "exactly_once",
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        168,
        170,
        171,
        176,
        177,
        178,
        179,
        180,
        181,
        182,
        183,
        184,
        185,
        186
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "ReleaseBeat",
        "target": "io.release.bits.data",
        "source": {
          "op": "lookup",
          "value": {
            "op": "signal",
            "name": "wb_buffer"
          },
          "index": {
            "op": "index_var",
            "name": "beat"
          }
        },
        "scope_identity": "WritebackTxn",
        "scope_index": {
          "name": "beat",
          "relation": "same"
        }
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        62,
        63,
        69,
        71,
        107,
        113,
        168,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "value_constraint",
        "on": "ReleaseBeat",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.release.bits.opcode"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 1,
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "ProbeWriteback",
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        15,
        63,
        64,
        107,
        108,
        168,
        172,
        173
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "join",
        "prerequisites": [
          "ReleaseComplete",
          "MemGrantSeen"
        ],
        "after": "VoluntaryDone",
        "scope_identity": "WritebackTxn",
        "scope_index": null
      },
      "derived_from_case_ids": [
        "VoluntaryWriteback"
      ],
      "evidence_statement_ids": [
        174,
        175,
        181,
        182,
        183,
        184,
        185,
        186,
        188,
        189,
        190,
        191,
        192,
        193
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The five-state FSM is compressed into a common fill phase plus two writeback modes distinguished by req.voluntary.",
    "FillIssue, BufferBeat, and ReleaseBeat are modeled as indexed occurrences over the eight cache-line beats instead of eight separate event IDs.",
    "The abstraction intentionally preserves completion, same-index ordering, and release-data correspondence while omitting liveness assumptions about ready/grant arrival.",
    "The exact ProbeAckData-versus-ReleaseData opcode distinction is not asserted as a trusted axiom in this candidate; omitting it keeps the abstraction conservative and it can be refined later if a system counterexample requires it."
  ],
  "extensions": {}
}