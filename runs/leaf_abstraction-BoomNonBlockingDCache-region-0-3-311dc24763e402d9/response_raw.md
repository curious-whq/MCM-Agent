{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-3-311dc24763e402d9",
  "work_unit_id": "BoomNonBlockingDCache::region-0-3",
  "occurrences": [
    {
      "id": "NackValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.nack[0].valid"
      ],
      "definition": "io.lsu.nack[0].valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.nack[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2787,
        2788
      ]
    },
    {
      "id": "RespValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.resp[0].valid"
      ],
      "definition": "io.lsu.resp[0].valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2739,
        2740
      ]
    },
    {
      "id": "StoreAckValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.store_ack[0].valid"
      ],
      "definition": "io.lsu.store_ack[0].valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.store_ack[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2800,
        2801,
        2802
      ]
    },
    {
      "id": "MSHRReqFire",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "mshrs.io.req[0].valid && mshrs.io.req[0].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "mshrs.io.req[0].valid",
          "mshrs.io.req[0].ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2093,
        2187
      ]
    },
    {
      "id": "HitStoreAck",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.store_ack[0].valid && s2_hit[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.store_ack[0].valid",
          "s2_hit[0]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2067,
        2068,
        2092,
        2094,
        2095,
        2097,
        2800,
        2801,
        2802
      ]
    },
    {
      "id": "MissAllocatedStoreAck",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.store_ack[0].valid && !s2_hit[0] && mshrs.io.req[0].valid && mshrs.io.req[0].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.store_ack[0].valid",
          "mshrs.io.req[0].valid",
          "mshrs.io.req[0].ready"
        ],
        "signals_false": [
          "s2_hit[0]"
        ]
      },
      "evidence_statement_ids": [
        2093,
        2094,
        2095,
        2116,
        2117,
        2187,
        2800,
        2801,
        2802
      ]
    },
    {
      "id": "RespFromS3",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.resp[0].valid && s3_bypass[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid",
          "s3_bypass[0]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2739,
        2740,
        2853,
        2854,
        2855,
        2856,
        2858,
        2873,
        2874
      ]
    },
    {
      "id": "RespFromS4",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.resp[0].valid && !s3_bypass[0] && s4_bypass[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid",
          "s4_bypass[0]"
        ],
        "signals_false": [
          "s3_bypass[0]"
        ]
      },
      "evidence_statement_ids": [
        2739,
        2740,
        2859,
        2860,
        2861,
        2862,
        2864,
        2872,
        2873,
        2874
      ]
    },
    {
      "id": "RespFromS5",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.resp[0].valid && !s3_bypass[0] && !s4_bypass[0] && s5_bypass[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid",
          "s5_bypass[0]"
        ],
        "signals_false": [
          "s3_bypass[0]",
          "s4_bypass[0]"
        ]
      },
      "evidence_statement_ids": [
        2739,
        2740,
        2865,
        2866,
        2867,
        2868,
        2870,
        2871,
        2872,
        2873,
        2874
      ]
    },
    {
      "id": "RespFromArray",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.resp[0].valid && !s3_bypass[0] && !s4_bypass[0] && !s5_bypass[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid"
        ],
        "signals_false": [
          "s3_bypass[0]",
          "s4_bypass[0]",
          "s5_bypass[0]"
        ]
      },
      "evidence_statement_ids": [
        2739,
        2740,
        2871,
        2872,
        2873,
        2874
      ]
    },
    {
      "id": "SCResponse",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.lsu.resp[0].valid && s2_sc",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.resp[0].valid",
          "s2_sc"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1805,
        1808,
        1809,
        1810,
        1811,
        2735,
        2739,
        2740,
        2774,
        2775,
        2784,
        2785
      ]
    }
  ],
  "predicates": [
    {
      "id": "S2Invalid",
      "definition": "!s2_valid[0]",
      "grounding": {
        "source_signal": "s2_valid[0]",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2739,
        2787,
        2800
      ]
    },
    {
      "id": "S2Hit",
      "definition": "s2_hit[0]",
      "grounding": {
        "source_signal": "s2_hit[0]",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2036,
        2094,
        2116
      ]
    },
    {
      "id": "S2Miss",
      "definition": "!s2_hit[0]",
      "grounding": {
        "source_signal": "s2_hit[0]",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2036,
        2116,
        2117
      ]
    },
    {
      "id": "S2Nack",
      "definition": "s2_nack[0]",
      "grounding": {
        "source_signal": "s2_nack[0]",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2067,
        2100,
        2112
      ]
    },
    {
      "id": "S2NoNack",
      "definition": "!s2_nack[0]",
      "grounding": {
        "source_signal": "s2_nack[0]",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2067,
        2068,
        2100
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Nack",
      "trigger_occurrences": [
        "NackValid"
      ],
      "guard_predicates": [
        {
          "id": "S2Nack",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A valid stage-2 request on a nack path is returned to the LSU as the same request identity and address."
      ],
      "evidence_statement_ids": [
        2099,
        2100,
        2102,
        2787,
        2788,
        2789
      ],
      "confidence": "high"
    },
    {
      "id": "C2_Response",
      "trigger_occurrences": [
        "RespValid"
      ],
      "guard_predicates": [
        {
          "id": "S2Hit",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "The direct LSU response path is a cache-hit read response carrying the stage-2 request identity."
      ],
      "evidence_statement_ids": [
        2029,
        2030,
        2031,
        2032,
        2033,
        2034,
        2035,
        2036,
        2062,
        2064,
        2739,
        2740,
        2741
      ],
      "confidence": "high"
    },
    {
      "id": "C3_HitStoreAck",
      "trigger_occurrences": [
        "HitStoreAck"
      ],
      "guard_predicates": [
        {
          "id": "S2Hit",
          "positive": true
        },
        {
          "id": "S2NoNack",
          "positive": true
        }
      ],
      "emits": [
        "StoreAckValid"
      ],
      "relations": [
        "A non-nacked write hit may be acknowledged immediately to the LSU."
      ],
      "evidence_statement_ids": [
        2066,
        2067,
        2068,
        2092,
        2094,
        2095,
        2097,
        2800,
        2801,
        2802,
        2803
      ],
      "confidence": "high"
    },
    {
      "id": "C4_MissAllocatedStoreAck",
      "trigger_occurrences": [
        "MissAllocatedStoreAck"
      ],
      "guard_predicates": [
        {
          "id": "S2Miss",
          "positive": true
        },
        {
          "id": "S2NoNack",
          "positive": true
        }
      ],
      "emits": [
        "StoreAckValid"
      ],
      "relations": [
        "A non-nacked write miss may be acknowledged when its MSHR request handshakes; this acknowledgement is admission into the miss machinery rather than downstream memory completion."
      ],
      "evidence_statement_ids": [
        2066,
        2067,
        2068,
        2092,
        2093,
        2094,
        2095,
        2097,
        2116,
        2117,
        2187,
        2800,
        2801,
        2802,
        2803
      ],
      "confidence": "high"
    },
    {
      "id": "C5_MSHRRequest",
      "trigger_occurrences": [
        "MSHRReqFire"
      ],
      "guard_predicates": [
        {
          "id": "S2Miss",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "An MSHR request handshake can occur only on the miss path represented by this region."
      ],
      "evidence_statement_ids": [
        2116,
        2117,
        2118,
        2119,
        2120,
        2121,
        2122,
        2123,
        2124,
        2125,
        2126,
        2127,
        2128,
        2129,
        2130,
        2131,
        2132,
        2187
      ],
      "confidence": "high"
    },
    {
      "id": "C6_RespFromS3",
      "trigger_occurrences": [
        "RespFromS3"
      ],
      "guard_predicates": [],
      "emits": [
        "RespValid"
      ],
      "relations": [
        "The youngest in-flight matching store in s3 has first forwarding priority for the response data word."
      ],
      "evidence_statement_ids": [
        2853,
        2854,
        2855,
        2856,
        2858,
        2873,
        2874
      ],
      "confidence": "high"
    },
    {
      "id": "C7_RespFromS4",
      "trigger_occurrences": [
        "RespFromS4"
      ],
      "guard_predicates": [],
      "emits": [
        "RespValid"
      ],
      "relations": [
        "s4 forwarding is used only when no matching s3 forwarding path is active."
      ],
      "evidence_statement_ids": [
        2859,
        2860,
        2861,
        2862,
        2864,
        2872,
        2873,
        2874
      ],
      "confidence": "high"
    },
    {
      "id": "C8_RespFromS5",
      "trigger_occurrences": [
        "RespFromS5"
      ],
      "guard_predicates": [],
      "emits": [
        "RespValid"
      ],
      "relations": [
        "s5 forwarding is used only when neither s3 nor s4 supplies a matching store value."
      ],
      "evidence_statement_ids": [
        2865,
        2866,
        2867,
        2868,
        2870,
        2871,
        2872,
        2873,
        2874
      ],
      "confidence": "high"
    },
    {
      "id": "C9_RespFromArray",
      "trigger_occurrences": [
        "RespFromArray"
      ],
      "guard_predicates": [],
      "emits": [
        "RespValid"
      ],
      "relations": [
        "When no s3/s4/s5 forwarding match exists, the response data word comes from the cache-array path."
      ],
      "evidence_statement_ids": [
        2730,
        2731,
        2733,
        2871,
        2872,
        2873,
        2874
      ],
      "confidence": "high"
    },
    {
      "id": "C10_SCResponse",
      "trigger_occurrences": [
        "SCResponse"
      ],
      "guard_predicates": [],
      "emits": [
        "RespValid"
      ],
      "relations": [
        "For an SC response, LoadGen is zeroed and the externally returned value is exactly the SC-failure bit."
      ],
      "evidence_statement_ids": [
        1805,
        1808,
        1809,
        1810,
        1811,
        1817,
        1818,
        2735,
        2774,
        2775,
        2776,
        2777,
        2778,
        2779,
        2780,
        2781,
        2782,
        2783,
        2784,
        2785
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RespValid",
        "predicate": "S2Invalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2739,
        2740
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "NackValid",
        "predicate": "S2Invalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2787,
        2788
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreAckValid",
        "predicate": "S2Invalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2800,
        2801,
        2802
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MSHRReqFire",
        "predicate": "S2Invalid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_MSHRRequest"
      ],
      "evidence_statement_ids": [
        2117,
        2187
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RespValid",
        "predicate": "S2Miss",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2036,
        2062,
        2739,
        2740
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "forbid_when",
        "occurrence": "NackValid",
        "predicate": "S2NoNack",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2099,
        2100,
        2102,
        2787,
        2788
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "forbid_when",
        "occurrence": "StoreAckValid",
        "predicate": "S2Nack",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2067,
        2068,
        2092,
        2095,
        2097,
        2800,
        2801,
        2802
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MSHRReqFire",
        "predicate": "S2Hit",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_MSHRRequest"
      ],
      "evidence_statement_ids": [
        2116,
        2117,
        2187
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "occurrence_partition",
        "whole": "StoreAckValid",
        "parts": [
          "HitStoreAck",
          "MissAllocatedStoreAck"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2066,
        2067,
        2068,
        2092,
        2093,
        2094,
        2095,
        2097,
        2116,
        2117,
        2187,
        2800,
        2801,
        2802
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "occurrence_partition",
        "whole": "RespValid",
        "parts": [
          "RespFromS3",
          "RespFromS4",
          "RespFromS5",
          "RespFromArray"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C6_RespFromS3",
        "C7_RespFromS4",
        "C8_RespFromS5",
        "C9_RespFromArray"
      ],
      "evidence_statement_ids": [
        2739,
        2740,
        2858,
        2864,
        2870,
        2871,
        2872,
        2873,
        2874
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "RespFromS3",
        "target": "s2_data_word[0]",
        "source": {
          "op": "signal",
          "name": "s3_req.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C6_RespFromS3"
      ],
      "evidence_statement_ids": [
        2858,
        2873,
        2874
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "RespFromS4",
        "target": "s2_data_word[0]",
        "source": {
          "op": "signal",
          "name": "s4_req.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C7_RespFromS4"
      ],
      "evidence_statement_ids": [
        2864,
        2872,
        2873,
        2874
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "RespFromS5",
        "target": "s2_data_word[0]",
        "source": {
          "op": "signal",
          "name": "s5_req.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C8_RespFromS5"
      ],
      "evidence_statement_ids": [
        2870,
        2871,
        2872,
        2873,
        2874
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "RespFromArray",
        "target": "s2_data_word[0]",
        "source": {
          "op": "signal",
          "name": "s2_data_word_prebypass[0]"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C9_RespFromArray"
      ],
      "evidence_statement_ids": [
        2730,
        2731,
        2733,
        2871,
        2872,
        2873,
        2874
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "SCResponse",
        "target": "io.lsu.resp[0].bits.data",
        "source": {
          "op": "signal",
          "name": "s2_sc_fail"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C10_SCResponse"
      ],
      "evidence_statement_ids": [
        1817,
        1818,
        2735,
        2774,
        2775,
        2776,
        2777,
        2778,
        2779,
        2780,
        2781,
        2782,
        2783,
        2784,
        2785
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.addr",
        "source": {
          "op": "signal",
          "name": "s2_req[0].addr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.data",
        "source": {
          "op": "signal",
          "name": "s2_req[0].data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A19",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "signal_equality",
        "on": "NackValid",
        "target": "io.lsu.nack[0].bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Nack"
      ],
      "evidence_statement_ids": [
        2789
      ],
      "status": "candidate"
    },
    {
      "id": "A22",
      "formal": {
        "type": "signal_equality",
        "on": "StoreAckValid",
        "target": "io.lsu.store_ack[0].bits.addr",
        "source": {
          "op": "signal",
          "name": "s2_req[0].addr"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2803
      ],
      "status": "candidate"
    },
    {
      "id": "A23",
      "formal": {
        "type": "signal_equality",
        "on": "StoreAckValid",
        "target": "io.lsu.store_ack[0].bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2803
      ],
      "status": "candidate"
    },
    {
      "id": "A24",
      "formal": {
        "type": "signal_equality",
        "on": "StoreAckValid",
        "target": "io.lsu.store_ack[0].bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2803
      ],
      "status": "candidate"
    },
    {
      "id": "A25",
      "formal": {
        "type": "signal_equality",
        "on": "StoreAckValid",
        "target": "io.lsu.store_ack[0].bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_HitStoreAck",
        "C4_MissAllocatedStoreAck"
      ],
      "evidence_statement_ids": [
        2803
      ],
      "status": "candidate"
    },
    {
      "id": "A26",
      "formal": {
        "type": "signal_equality",
        "on": "RespValid",
        "target": "io.lsu.resp[0].bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2741
      ],
      "status": "candidate"
    },
    {
      "id": "A27",
      "formal": {
        "type": "signal_equality",
        "on": "RespValid",
        "target": "io.lsu.resp[0].bits.uop.mem_size",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.mem_size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2741
      ],
      "status": "candidate"
    },
    {
      "id": "A28",
      "formal": {
        "type": "signal_equality",
        "on": "RespValid",
        "target": "io.lsu.resp[0].bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2741
      ],
      "status": "candidate"
    },
    {
      "id": "A29",
      "formal": {
        "type": "signal_equality",
        "on": "RespValid",
        "target": "io.lsu.resp[0].bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2741
      ],
      "status": "candidate"
    },
    {
      "id": "A30",
      "formal": {
        "type": "signal_equality",
        "on": "RespValid",
        "target": "io.lsu.resp[0].bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "s2_req[0].uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_Response"
      ],
      "evidence_statement_ids": [
        2741
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region is the stage-2 LSU outcome-selection and local data-forwarding region. It should not be abstracted as a single mutually-exclusive response state machine because the command classes overlap: SC and AMO are both read-like and write-like operations.",
    "A1-A4 preserve the common validity gate: killed, excepted, branch-killed, or otherwise invalidated requests represented by s2_valid[0] cannot produce an LSU response, nack, store acknowledgement, or MSHR request handshake.",
    "A5 preserves that the direct LSU response path is hit-only. Misses are handled through MSHR/replay rather than producing the immediate hit response represented here.",
    "A6 and A7 preserve the opposite nack polarity of NackValid and StoreAckValid. A nack result requires s2_nack; a store acknowledgement requires the request not to be nacked.",
    "A8 preserves that an MSHR allocation handshake occurs only on the miss path.",
    "A9 is especially important: StoreAckValid is exactly divided between a cache-hit acknowledgement and a miss acknowledgement caused by a same-cycle MSHR request handshake. Therefore StoreAckValid must not be interpreted by a parent as proof that a store miss has completed at the memory system.",
    "A10-A14 preserve the exact store-to-load forwarding priority s3 > s4 > s5 > cache-array data. The bypass comparisons operate at the 8-byte word address granularity and the nested mux implements the stated priority.",
    "The exact general LoadGen byte/halfword/word extraction and sign-extension function is deliberately not encoded. Leaving ordinary response data less constrained is a safe over-approximation and can be refined by CEGAR if architectural-value reasoning later requires it.",
    "SC is retained as an exception to that omission. The zero flag passed to LoadGen makes the normal SC response value zero, after which s2_sc_fail is ORed into the result; consequently SCResponse returns exactly 0 on success and 1 on failure. A15 preserves this architecturally significant atomic result.",
    "A16-A30 preserve the request projections needed to correlate LSU-visible results with the stage-2 request: address and store data where present, memory command and size, ROB identity, and LDQ/STQ identity. The many unrelated decode, floating-point, debug, and branch-control fields in the MicroOp payload are deliberately omitted.",
    "No identity_key object is introduced because this region already exposes the relevant request identity through exact same-cycle payload projections, while the supplied schema evidence does not require an additional cross-generation identity relation.",
    "No liveness or fairness property is claimed. In particular, MSHR readiness and subsequent miss completion are outside this local result-selection guarantee."
  ],
  "extensions": {}
}