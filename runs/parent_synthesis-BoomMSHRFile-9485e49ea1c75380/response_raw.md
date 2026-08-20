{
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHRFile-9485e49ea1c75380",
  "work_unit_id": "BoomMSHRFile",
  "occurrences": [
    {
      "id": "RequestAccept",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.req[0].fire"
      ],
      "definition": "io.req[0].valid && io.req[0].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.req[0].valid",
          "io.req[0].ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        4,
        5,
        6,
        1395
      ]
    },
    {
      "id": "PrimaryMSHRAccept",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.req[0].valid && io.req[0].ready && cacheable && !idx_match[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.req[0].valid",
          "io.req[0].ready",
          "cacheable"
        ],
        "signals_false": [
          "idx_match[0]"
        ]
      },
      "evidence_statement_ids": [
        5,
        48,
        128,
        129,
        130,
        1391,
        1392,
        1393,
        1394,
        1395
      ]
    },
    {
      "id": "SecondaryMSHRAccept",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.req[0].valid && io.req[0].ready && cacheable && idx_match[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.req[0].valid",
          "io.req[0].ready",
          "cacheable",
          "idx_match[0]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        5,
        48,
        128,
        129,
        130,
        1390,
        1391,
        1392,
        1393,
        1394,
        1395
      ]
    },
    {
      "id": "MMIOAccept",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.req[0].valid && io.req[0].ready && !cacheable",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.req[0].valid",
          "io.req[0].ready"
        ],
        "signals_false": [
          "cacheable"
        ]
      },
      "evidence_statement_ids": [
        5,
        48,
        960,
        1389,
        1393,
        1394,
        1395
      ]
    },
    {
      "id": "MemAcquire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.mem_acquire.fire"
      ],
      "definition": "io.mem_acquire.valid && io.mem_acquire.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.mem_acquire.valid",
          "io.mem_acquire.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1003,
        1004,
        1071,
        1100
      ]
    },
    {
      "id": "MemGrant",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.mem_grant.fire"
      ],
      "definition": "io.mem_grant.valid && io.mem_grant.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.mem_grant.valid",
          "io.mem_grant.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        162,
        476,
        478,
        796,
        798,
        969,
        974
      ]
    },
    {
      "id": "MMIOGrantDelivery",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.mem_grant.valid && io.mem_grant.ready && io.mem_grant.bits.source == 3",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.mem_grant.valid",
          "io.mem_grant.ready"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "signal",
              "name": "io.mem_grant.bits.source"
            },
            "relation": "eq",
            "value": 3
          }
        ]
      },
      "evidence_statement_ids": [
        162,
        969,
        970,
        971,
        972,
        973,
        974
      ]
    },
    {
      "id": "MemFinish",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.mem_finish.fire"
      ],
      "definition": "io.mem_finish.valid && io.mem_finish.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.mem_finish.valid",
          "io.mem_finish.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1178,
        1229,
        1252
      ]
    },
    {
      "id": "MetaRead",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.meta_read.fire"
      ],
      "definition": "io.meta_read.valid && io.meta_read.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.meta_read.valid",
          "io.meta_read.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        831,
        832,
        833
      ]
    },
    {
      "id": "MetaWrite",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.meta_write.fire"
      ],
      "definition": "io.meta_write.valid && io.meta_write.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        828,
        829,
        830
      ]
    },
    {
      "id": "WBReq",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.wb_req.fire"
      ],
      "definition": "io.wb_req.valid && io.wb_req.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.wb_req.valid",
          "io.wb_req.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        834,
        835,
        836
      ]
    },
    {
      "id": "Refill",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.refill.fire"
      ],
      "definition": "io.refill.valid && io.refill.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.refill.valid",
          "io.refill.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1402,
        1403,
        1404
      ]
    },
    {
      "id": "Replay",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.replay.fire"
      ],
      "definition": "io.replay.valid && io.replay.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.replay.valid",
          "io.replay.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1430,
        1431,
        1432
      ]
    },
    {
      "id": "RespHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile::io.resp.fire"
      ],
      "definition": "io.resp.valid && io.resp.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.resp.valid",
          "io.resp.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        1385,
        1386,
        1387
      ]
    }
  ],
  "predicates": [],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_PrimaryMSHRAccepted",
      "trigger_occurrences": [
        "PrimaryMSHRAccept"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "A cacheable accepted request with no current index match takes the primary-MSHR allocation path."
      ],
      "evidence_statement_ids": [
        128,
        130,
        166,
        169,
        186,
        188,
        506,
        508,
        1388,
        1391,
        1395
      ],
      "confidence": "high"
    },
    {
      "id": "C2_SecondaryMSHRAccepted",
      "trigger_occurrences": [
        "SecondaryMSHRAccept"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "A cacheable accepted request with an existing index match takes a matching secondary-MSHR path."
      ],
      "evidence_statement_ids": [
        128,
        130,
        192,
        196,
        479,
        512,
        516,
        799,
        800,
        1390,
        1391,
        1395
      ],
      "confidence": "high"
    },
    {
      "id": "C3_MMIOAccepted",
      "trigger_occurrences": [
        "MMIOAccept"
      ],
      "guard_predicates": [],
      "emits": [
        "BoomMSHRFile.mmios_0::ReqAccept"
      ],
      "relations": [
        "A non-cacheable accepted request crosses the singleton MMIO allocation arbiter into the frozen BoomIOMSHR."
      ],
      "evidence_statement_ids": [
        843,
        845,
        960,
        979,
        981,
        1389,
        1393,
        1395
      ],
      "confidence": "high"
    },
    {
      "id": "C4_ResponseBuffered",
      "trigger_occurrences": [
        "BoomMSHRFile.resp_arb::OutputFire"
      ],
      "guard_predicates": [],
      "emits": [
        "BoomMSHRFile.respq::EnqHandshake"
      ],
      "relations": [
        "The response-arbiter output is the response-queue enqueue handshake; response-queue kill filtering determines whether it becomes QueueInsert."
      ],
      "evidence_statement_ids": [
        1383,
        1384
      ],
      "confidence": "high"
    },
    {
      "id": "C5_VisibleResponse",
      "trigger_occurrences": [
        "RespHandshake"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The top response handshake is exactly the frozen response-queue dequeue handshake."
      ],
      "evidence_statement_ids": [
        1385,
        1386,
        1387
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "RequestAccept",
        "parts": [
          "PrimaryMSHRAccept",
          "SecondaryMSHRAccept",
          "MMIOAccept"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_PrimaryMSHRAccepted",
        "C2_SecondaryMSHRAccepted",
        "C3_MMIOAccepted"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        48,
        128,
        130,
        1388,
        1389,
        1390,
        1391,
        1392,
        1393,
        1395
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MMIOAccept",
        "parts": [
          "BoomMSHRFile.mmios_0::ReqAccept"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_MMIOAccepted"
      ],
      "evidence_statement_ids": [
        5,
        6,
        843,
        845,
        960,
        979,
        981,
        1389,
        1393,
        1395
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MemAcquire",
        "parts": [
          "BoomMSHRFile.mshrs_0::MemAcquire",
          "BoomMSHRFile.mshrs_1::MemAcquire",
          "BoomMSHRFile.mmios_0::MemAccess"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1003,
        1004,
        1006,
        1007,
        1025,
        1026,
        1027,
        1029,
        1030,
        1031,
        1083,
        1084,
        1085,
        1086,
        1087,
        1088,
        1089,
        1090,
        1091,
        1099,
        1100
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MemGrant",
        "parts": [
          "BoomMSHRFile.mshrs_0::MemGrant",
          "BoomMSHRFile.mshrs_1::MemGrant",
          "MMIOGrantDelivery"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        162,
        467,
        476,
        478,
        787,
        796,
        798,
        969,
        970,
        971,
        972,
        974
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MemFinish",
        "parts": [
          "BoomMSHRFile.mshrs_0::MemFinish",
          "BoomMSHRFile.mshrs_1::MemFinish"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1178,
        1179,
        1181,
        1194,
        1195,
        1197,
        1198,
        1240,
        1241,
        1242,
        1243,
        1244,
        1245,
        1251,
        1252
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MetaRead",
        "parts": [
          "BoomMSHRFile.meta_read_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        831,
        832,
        833
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.meta_read_arb::Input0Fire",
        "parts": [
          "BoomMSHRFile.mshrs_0::MetaRead"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        454
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.meta_read_arb::Input1Fire",
        "parts": [
          "BoomMSHRFile.mshrs_1::MetaRead"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        774
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MetaWrite",
        "parts": [
          "BoomMSHRFile.meta_write_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        828,
        829,
        830
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "occurrence_partition",
        "whole": "WBReq",
        "parts": [
          "BoomMSHRFile.wb_req_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        834,
        835,
        836
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.wb_req_arb::Input0Fire",
        "parts": [
          "BoomMSHRFile.mshrs_0::WBReq"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        458
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.wb_req_arb::Input1Fire",
        "parts": [
          "BoomMSHRFile.mshrs_1::WBReq"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        778
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "occurrence_partition",
        "whole": "Refill",
        "parts": [
          "BoomMSHRFile.refill_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1402,
        1403,
        1404
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.refill_arb::Input0Fire",
        "parts": [
          "BoomMSHRFile.mshrs_0::CommitRefillBeat"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        460
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.refill_arb::Input1Fire",
        "parts": [
          "BoomMSHRFile.mshrs_1::CommitRefillBeat"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        780
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "occurrence_partition",
        "whole": "Replay",
        "parts": [
          "BoomMSHRFile.replay_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1430,
        1431,
        1432
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.replay_arb::Input0Fire",
        "parts": [
          "BoomMSHRFile.mshrs_0::ReplayHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        459
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.replay_arb::Input1Fire",
        "parts": [
          "BoomMSHRFile.mshrs_1::ReplayHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        779
      ],
      "status": "candidate"
    },
    {
      "id": "A19",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.resp_arb::Input0Fire",
        "parts": [
          "BoomMSHRFile.mshrs_0::RespHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        481
      ],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.resp_arb::Input1Fire",
        "parts": [
          "BoomMSHRFile.mshrs_1::RespHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        801
      ],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.resp_arb::Input2Fire",
        "parts": [
          "BoomMSHRFile.mmios_0::RespHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        975
      ],
      "status": "candidate"
    },
    {
      "id": "A22",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomMSHRFile.respq::EnqHandshake",
        "parts": [
          "BoomMSHRFile.resp_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ResponseBuffered"
      ],
      "evidence_statement_ids": [
        1384
      ],
      "status": "candidate"
    },
    {
      "id": "A23",
      "formal": {
        "type": "occurrence_partition",
        "whole": "RespHandshake",
        "parts": [
          "BoomMSHRFile.respq::DeqHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_VisibleResponse"
      ],
      "evidence_statement_ids": [
        1385,
        1386,
        1387
      ],
      "status": "candidate"
    },
    {
      "id": "A24",
      "formal": {
        "type": "ordered_before",
        "before": "BoomMSHRFile.respq::QueueInsert",
        "after": "RespHandshake",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C5_VisibleResponse"
      ],
      "evidence_statement_ids": [
        1385,
        1386,
        1387
      ],
      "status": "candidate"
    },
    {
      "id": "A25",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.prefetch.valid"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        12
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "BoomMSHRFile contributes shared routing and buffering around already-frozen MSHR/MMIO components; child lifecycle axioms remain imported instead of being copied.",
    "A1 preserves the accepted-request split into primary cached allocation, secondary cached merge, and non-cacheable MMIO allocation. It deliberately does not invent a cached-MSHR accept occurrence that the frozen child catalogs do not expose.",
    "A2 composes the non-cacheable path with the frozen singleton MMIO allocation arbiter and the imported BoomIOMSHR ReqAccept occurrence.",
    "A3/A5 are exact same-cycle conservation facts for the parent-local TileLink Acquire/Finish arbiters. A4 is exact Grant source routing: source 0 to MSHR0, source 1 to MSHR1, source 3 to MMIO; source 2 cannot handshake.",
    "MMIOGrantDelivery is not equated with BoomMSHRFile.mmios_0::AckConsumed: source-3 ready is forced by the parent independently of the child internal ack-wait state.",
    "A6-A23 are same-cycle routing bridges needed to keep frozen child events connected to the shared parent interfaces.",
    "A24 preserves the response queue's essential killable-buffer semantics: a visible top response needs a prior actual QueueInsert, not merely a response-arbiter output handshake.",
    "Replay data is overwritten after arbitration by an SDQ lookup. Exact SDQ allocation/free/data-flow is deliberately omitted as a safe over-approximation and possible CEGAR refinement.",
    "A25 lifts the frozen NullPrefetcher constant-valid-zero guarantee to the top prefetch interface.",
    "No new global identity key or liveness/fairness claim is introduced."
  ],
  "extensions": {
    "parent_synthesis": {
      "axiom_provenance": {
        "A1": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Classifies every accepted top request into exactly one of primary cached, secondary cached, or non-cacheable MMIO paths using parent-local cacheability/index-match logic."
        },
        "A2": {
          "kind": "emergent",
          "source_axioms": [
            "BoomMSHRFile.mmio_alloc_arb::A3",
            "BoomMSHRFile.mmio_alloc_arb::A4"
          ],
          "note": "The parent composes the frozen singleton arbiter valid/ready equalities with local request routing to establish the MMIO request handshake equivalence."
        },
        "A3": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The inlined three-source TileLink arbiter makes every top mem_acquire handshake exactly one child source handshake."
        },
        "A4": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Parent-local source decoding routes each top mem_grant handshake to MSHR0, MSHR1, or the source-3 MMIO delivery path."
        },
        "A5": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The inlined two-source TileLink arbiter makes every top mem_finish handshake exactly one cached-MSHR finish handshake."
        },
        "A6": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.meta_read is directly connected to meta_read_arb.io.out."
        },
        "A7": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "meta_read_arb input 0 is directly connected to MSHR0 meta_read."
        },
        "A8": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "meta_read_arb input 1 is directly connected to MSHR1 meta_read."
        },
        "A9": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.meta_write is directly connected to meta_write_arb.io.out."
        },
        "A10": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.wb_req is directly connected to wb_req_arb.io.out."
        },
        "A11": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "wb_req_arb input 0 is directly connected to MSHR0 wb_req."
        },
        "A12": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "wb_req_arb input 1 is directly connected to MSHR1 wb_req."
        },
        "A13": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.refill is directly connected to refill_arb.io.out."
        },
        "A14": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "refill_arb input 0 is directly connected to MSHR0 refill."
        },
        "A15": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "refill_arb input 1 is directly connected to MSHR1 refill."
        },
        "A16": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.replay is directly connected to replay_arb.io.out; only payload data is subsequently overridden, which does not change the handshake."
        },
        "A17": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "replay_arb input 0 is directly connected to MSHR0 replay."
        },
        "A18": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "replay_arb input 1 is directly connected to MSHR1 replay."
        },
        "A19": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "resp_arb input 0 is directly connected to MSHR0 response."
        },
        "A20": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "resp_arb input 1 is directly connected to MSHR1 response."
        },
        "A21": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "resp_arb input 2 is directly connected to the MMIO MSHR response."
        },
        "A22": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "resp_arb output is directly connected to respq enqueue."
        },
        "A23": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Top io.resp is directly connected to respq dequeue."
        },
        "A24": {
          "kind": "emergent",
          "source_axioms": [
            "BoomMSHRFile.respq::A9"
          ],
          "note": "The frozen response queue requires a prior same-slot QueueInsert before its dequeue; the parent directly exposes that dequeue as io.resp.fire."
        },
        "A25": {
          "kind": "lifted",
          "source_axioms": [
            "BoomMSHRFile.prefetcher::A1"
          ],
          "note": "Top io.prefetch.valid is directly driven by the frozen NullPrefetcher valid signal, which is permanently zero."
        }
      }
    }
  }
}
