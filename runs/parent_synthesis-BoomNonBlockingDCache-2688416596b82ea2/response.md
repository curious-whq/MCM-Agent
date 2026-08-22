{
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomNonBlockingDCache-2688416596b82ea2",
  "work_unit_id": "BoomNonBlockingDCache",
  "occurrences": [
    {
      "id": "MemAcquire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.a.fire"
      ],
      "definition": "auto.out.a.valid && auto.out.a.ready; one accepted outgoing TileLink A-channel acquire/request",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.a.valid",
          "auto.out.a.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        47,
        2480,
        2481,
        2482
      ]
    },
    {
      "id": "ProbeFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.b.fire"
      ],
      "definition": "auto.out.b.valid && auto.out.b.ready; one accepted incoming TileLink B probe",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.b.valid",
          "auto.out.b.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        47,
        2483,
        2484,
        2485
      ]
    },
    {
      "id": "CBeat",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.c.fire"
      ],
      "definition": "auto.out.c.valid && auto.out.c.ready; one accepted outgoing TileLink C beat",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.c.valid",
          "auto.out.c.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        47,
        2687
      ]
    },
    {
      "id": "DBeat",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.d.fire"
      ],
      "definition": "auto.out.d.valid && auto.out.d.ready; one accepted incoming TileLink D beat",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.d.valid",
          "auto.out.d.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        47,
        2534
      ]
    },
    {
      "id": "MemFinish",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.e.fire"
      ],
      "definition": "auto.out.e.valid && auto.out.e.ready; one accepted outgoing TileLink E-channel finish",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.e.valid",
          "auto.out.e.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        47,
        2523,
        2524,
        2525
      ]
    },
    {
      "id": "LongLatencyResp",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.ll_resp.fire"
      ],
      "definition": "io.lsu.ll_resp.valid && io.lsu.ll_resp.ready; one accepted long-latency LSU response",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.ll_resp.valid",
          "io.lsu.ll_resp.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2804,
        2805,
        2806
      ]
    },
    {
      "id": "NackValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.nack[0].valid"
      ],
      "definition": "io.lsu.nack[0].valid; an LSU request is reported as nacked",
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
        3
      ]
    },
    {
      "id": "LSURelease",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.release.fire"
      ],
      "definition": "io.lsu.release.valid && io.lsu.release.ready; one LSU-visible release message is accepted",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.release.valid",
          "io.lsu.release.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2541,
        2542,
        2543
      ]
    },
    {
      "id": "RequestAccept",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.req.fire"
      ],
      "definition": "io.lsu.req.valid && io.lsu.req.ready; one LSU request is accepted by the DCache",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.lsu.req.valid",
          "io.lsu.req.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        3,
        1296
      ]
    },
    {
      "id": "RespValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.resp[0].valid"
      ],
      "definition": "io.lsu.resp[0].valid; one direct LSU response is produced",
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
        3
      ]
    },
    {
      "id": "StoreAckValid",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::io.lsu.store_ack[0].valid"
      ],
      "definition": "io.lsu.store_ack[0].valid; one LSU store acknowledgement is produced",
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
        3
      ]
    },
    {
      "id": "MemGrant",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "DBeat with auto.out.d.bits.source != 2; accepted D traffic routed toward the miss machinery",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.d.valid",
          "auto.out.d.ready"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "signal",
              "name": "auto.out.d.bits.source"
            },
            "relation": "neq",
            "value": 2
          }
        ]
      },
      "evidence_statement_ids": [
        47,
        2534,
        2535
      ]
    },
    {
      "id": "ReleaseAck",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "DBeat with auto.out.d.bits.source == 2; accepted D traffic used as the writeback ReleaseAck path",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "auto.out.d.valid",
          "auto.out.d.ready"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "signal",
              "name": "auto.out.d.bits.source"
            },
            "relation": "eq",
            "value": 2
          }
        ]
      },
      "evidence_statement_ids": [
        47,
        2534,
        2535,
        2536,
        2537
      ]
    },
    {
      "id": "HitStoreAck",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "StoreAckValid && s2_hit[0]; store acknowledgement produced on the cache-hit path",
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
        3,
        1767
      ]
    },
    {
      "id": "MissAllocatedStoreAck",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "StoreAckValid && !s2_hit[0] && mshrs.io.req[0].valid && mshrs.io.req[0].ready; store miss acknowledged when admitted to the miss machinery",
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
        3,
        1767,
        2477
      ]
    }
  ],
  "predicates": [
    {
      "id": "LRSCValid",
      "definition": "the DCache LR/SC reservation-valid condition is asserted (lrsc_count > 3)",
      "grounding": {
        "source_signal": "lrsc_valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        1795,
        1796
      ]
    },
    {
      "id": "LongLatencyRespPending",
      "definition": "a long-latency MSHR response is currently valid at the LSU interface",
      "grounding": {
        "source_signal": "io.lsu.ll_resp.valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2805
      ]
    },
    {
      "id": "Ordered",
      "definition": "the DCache reports ordered: MSHRs are fence-ready and neither s1 nor s2 contains a valid local request",
      "grounding": {
        "source_signal": "io.lsu.ordered",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2919,
        2920,
        2921,
        2922,
        2923
      ]
    }
  ],
  "identity_keys": [],
  "cases": [],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MemAcquire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::MemAcquire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        47,
        2480,
        2481,
        2482
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MemFinish",
        "parts": [
          "BoomNonBlockingDCache.mshrs::MemFinish"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        47,
        2523,
        2524,
        2525
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "occurrence_partition",
        "whole": "LongLatencyResp",
        "parts": [
          "BoomNonBlockingDCache.mshrs::RespHandshake"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2804,
        2805,
        2806
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "occurrence_partition",
        "whole": "LSURelease",
        "parts": [
          "BoomNonBlockingDCache.lsu_release_arb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2541,
        2542,
        2543
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.lsu_release_arb::Input0Fire",
        "parts": [
          "BoomNonBlockingDCache.wb::LSURelease"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2544
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.lsu_release_arb::Input1Fire",
        "parts": [
          "BoomNonBlockingDCache.prober::LSURelease"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2545
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.wb::WritebackReq",
        "parts": [
          "BoomNonBlockingDCache.wbArb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2531
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.wbArb::Input0Fire",
        "parts": [
          "BoomNonBlockingDCache.prober::WBReq"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2529
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.wbArb::Input1Fire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::WBReq"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2530
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.meta_0::MetadataWrite",
        "parts": [
          "BoomNonBlockingDCache.metaWriteArb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        221,
        222,
        233
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.metaWriteArb::Input0Fire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::MetaWrite"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2522
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.metaWriteArb::Input1Fire",
        "parts": [
          "BoomNonBlockingDCache.prober::MetaWrite"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2499
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.meta_0::ReadRequest",
        "parts": [
          "BoomNonBlockingDCache.metaReadArb::OutputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        228,
        232
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.metaReadArb::Input3Fire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::MetaRead"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        661,
        665
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.metaReadArb::Input1Fire",
        "parts": [
          "BoomNonBlockingDCache.prober::MetaRead"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1168,
        1172
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache::region-0-3::MSHRReqFire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::RequestAccept"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2477
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "occurrence_partition",
        "whole": "BoomNonBlockingDCache.dataWriteArb::Input1Fire",
        "parts": [
          "BoomNonBlockingDCache.mshrs::Refill"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        2521
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "occurrence_partition",
        "whole": "ProbeFire",
        "parts": [
          "BoomNonBlockingDCache::region-0-0::ProbeFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        47,
        2483,
        2484,
        2485
      ],
      "status": "candidate"
    },
    {
      "id": "A19",
      "formal": {
        "type": "occurrence_partition",
        "whole": "StoreAckValid",
        "parts": [
          "BoomNonBlockingDCache::region-0-3::StoreAckValid"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3
      ],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "occurrence_partition",
        "whole": "HitStoreAck",
        "parts": [
          "BoomNonBlockingDCache::region-0-3::HitStoreAck"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3,
        1767
      ],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "occurrence_partition",
        "whole": "MissAllocatedStoreAck",
        "parts": [
          "BoomNonBlockingDCache::region-0-3::MissAllocatedStoreAck"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3,
        1767,
        2477
      ],
      "status": "candidate"
    },
    {
      "id": "A22",
      "formal": {
        "type": "occurrence_partition",
        "whole": "RequestAccept",
        "parts": [
          "BoomNonBlockingDCache::region-0-4::RequestAccept"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3,
        1296
      ],
      "status": "candidate"
    },
    {
      "id": "A23",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ProbeFire",
        "predicate": "LRSCValid",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1795,
        1796,
        2483,
        2484,
        2485
      ],
      "status": "candidate"
    },
    {
      "id": "A28",
      "formal": {
        "type": "occurrence_partition",
        "whole": "DBeat",
        "parts": [
          "ReleaseAck",
          "MemGrant"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        47,
        2534,
        2535,
        2536,
        2537
      ],
      "status": "candidate"
    },
    {
      "id": "A29",
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
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3,
        1767,
        2477
      ],
      "status": "candidate"
    },
    {
      "id": "A30",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RequestAccept",
        "predicate": "LongLatencyRespPending",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1296,
        2805
      ],
      "status": "candidate"
    },
    {
      "id": "A31",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.lsu.s1_nack_advisory[0]"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        1465
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The parent candidate separates private composition lemmas from the public contract as required by parent-synthesis-prompt-0.4. Exact child-interface routing is retained privately, while only interface-closed parent IDs are exported.",
    "A1-A17 are exact same-cycle wiring bridges for A/E, long-latency response, LSU release routing, writeback requests, metadata reads/writes, the stage-2 MSHR request, and refill traffic. They preserve composition paths without leaking qualified child IDs into the public interface.",
    "A23 preserves the LR/SC coherence exclusion at the DCache boundary: an accepted B-channel probe is impossible while the local reservation-valid condition holds.",
    "The stateful TileLink C arbiter semantics remain trusted in frozen child BoomNonBlockingDCache::region-0-1. This parent does not reconstruct its hidden idle/winner/state signals; CBeat is exported conservatively as an event-only boundary and may be refined when a certified semantic-alias export is available.",
    "A28 exposes the D-channel source discriminator. Source 2 is the writeback ReleaseAck path; every other accepted D beat is classified as miss-machinery grant traffic. No stronger public claim equates MemGrant with BoomNonBlockingDCache.mshrs::MemGrant because the retained parent-local ledger does not contain the non-source-2 ready/valid bridge needed for that handshake theorem.",
    "A29 is deliberately public because StoreAckValid is not a memory-completion event. A store hit may be acknowledged locally, while a store miss may be acknowledged in the same cycle that the miss request is admitted to the MSHR machinery.",
    "A30 publishes the request/long-latency-response serialization that is visible at the LSU boundary. It does not claim eventual acceptance or eventual response.",
    "A31 lifts the concrete data-array fact that s1_nacks[0] is permanently zero to the LSU-visible s1_nack_advisory signal.",
    "Ordered is exported as a predicate with the exact parent-local definition mshrs.io.fence_rdy && !s1_valid[0] && !s2_valid[0]. It is an observation of current quiescence/order readiness, not a liveness guarantee.",
    "The top-level A and E handshakes, long-latency response, direct response, nack, and LSU release remain event_only publicly when there is no additional interface-closed theorem worth exposing; their exact child bridges remain private.",
    "io.errors.bus.valid is intentionally omitted because the implementation invalidates that output. io.lsu.req.bits[0].valid is intentionally omitted because it is a lane offer rather than the accepted request event.",
    "No exact parent bridge is asserted from the B-channel ProbeFire to ProbeUnit::ProbeReq because the retained parent-local ledger does not include the required B ready relation. The frozen region theorem still supplies the LR/SC exclusion used by A23.",
    "Replay and WritebackUnit read paths are not equated to individual metaReadArb/dataReadArb input fires: producer readiness is a conjunction of both downstream readies, so one arbiter may perform a speculative read without a producer-level handshake.",
    "No fairness, eventual grant, eventual release, eventual response, or eventual request-acceptance property is claimed."
  ],
  "extensions": {
    "parent_synthesis": {
      "axiom_provenance": {
        "A1": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Exact A-channel Decoupled bridge from the parent boundary to the frozen MSHR-file MemAcquire occurrence."
        },
        "A2": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Exact E-channel Decoupled bridge from the parent boundary to the frozen MSHR-file MemFinish occurrence."
        },
        "A3": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "io.lsu.ll_resp is bulk-connected to mshrs.io.resp, giving an exact same-cycle handshake bridge."
        },
        "A4": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The LSU-visible release interface is exactly the output handshake of lsu_release_arb."
        },
        "A5": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "lsu_release_arb input 0 is exactly the WritebackUnit LSURelease interface."
        },
        "A6": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "lsu_release_arb input 1 is exactly the ProbeUnit LSURelease interface."
        },
        "A7": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "WritebackUnit WritebackReq is exactly the wbArb output handshake."
        },
        "A8": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "wbArb input 0 is exactly the ProbeUnit WBReq handshake."
        },
        "A9": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "wbArb input 1 is exactly the MSHR-file WBReq handshake."
        },
        "A10": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The accepted metaWriteArb output is exactly the metadata-array MetadataWrite event."
        },
        "A11": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "metaWriteArb input 0 is exactly the MSHR-file MetaWrite handshake."
        },
        "A12": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "metaWriteArb input 1 is exactly the ProbeUnit MetaWrite handshake."
        },
        "A13": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The accepted metaReadArb output is exactly the metadata-array ReadRequest event."
        },
        "A14": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "metaReadArb input 3 is exactly the MSHR-file MetaRead handshake."
        },
        "A15": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "metaReadArb input 1 is exactly the ProbeUnit MetaRead handshake."
        },
        "A16": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Both imported occurrences denote the same mshrs.io.req[0] ready/valid handshake."
        },
        "A17": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "dataWriteArb input 1 is exactly the MSHR refill handshake."
        },
        "A18": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The local public ProbeFire and the frozen region ProbeFire denote the same parent B-channel physical event."
        },
        "A19": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The local public StoreAckValid and the frozen region StoreAckValid denote the same LSU store-ack valid event."
        },
        "A20": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The local HitStoreAck uses the same store-ack/hit classification as the frozen region occurrence."
        },
        "A21": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The local MissAllocatedStoreAck uses the same miss plus MSHR-admission classification as the frozen region occurrence."
        },
        "A22": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "The local public RequestAccept and the frozen admission-region RequestAccept denote the same io.lsu.req.fire event."
        },
        "A23": {
          "kind": "lifted",
          "source_axioms": [
            "BoomNonBlockingDCache::region-0-0::A1"
          ],
          "note": "Lift the frozen LR/SC probe exclusion to parent-local public IDs; A18 bridges the boundary occurrence and lrsc_valid is parent-local."
        },
        "A28": {
          "kind": "parent_local",
          "source_axioms": [],
          "note": "Classify every accepted D beat by the exact source==2 discriminator into ReleaseAck or miss-machinery grant traffic."
        },
        "A29": {
          "kind": "emergent",
          "source_axioms": [
            "BoomNonBlockingDCache::region-0-3::A9"
          ],
          "note": "Re-export the trusted store-ack hit-versus-miss-admission partition through local public occurrences; A19-A21 are private bridges."
        },
        "A30": {
          "kind": "lifted",
          "source_axioms": [
            "BoomNonBlockingDCache::region-0-4::A1"
          ],
          "note": "Lift MSHR-response admission blocking to the public ll_resp.valid predicate using the exact ll_resp/mshrs.resp wiring and A22."
        },
        "A31": {
          "kind": "lifted",
          "source_axioms": [
            "BoomNonBlockingDCache.data::A5"
          ],
          "note": "Lift the duplicated-data-array constant s1_nacks[0]==0 through the exact LSU advisory wiring."
        }
      },
      "public_interface": {
        "policy": "explicit-public-contract-v0.1",
        "exported_axiom_ids": [
          "A23",
          "A28",
          "A29",
          "A30",
          "A31"
        ],
        "exported_occurrence_ids": [
          "MemAcquire",
          "ProbeFire",
          "CBeat",
          "DBeat",
          "MemFinish",
          "LongLatencyResp",
          "NackValid",
          "LSURelease",
          "RequestAccept",
          "RespValid",
          "StoreAckValid",
          "MemGrant",
          "ReleaseAck",
          "HitStoreAck",
          "MissAllocatedStoreAck"
        ],
        "exported_predicate_ids": [
          "LRSCValid",
          "LongLatencyRespPending",
          "Ordered"
        ],
        "exported_identity_ids": [],
        "boundary_coverage": [
          {
            "physical_event_id": "BoomNonBlockingDCache::auto.out.a.fire",
            "status": "event_only",
            "occurrence_ids": [
              "MemAcquire"
            ],
            "axiom_ids": [],
            "note": "Export the memory-acquire handshake; its exact bridge to the MSHR hierarchy is private A1."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::auto.out.b.fire",
            "status": "constrained",
            "occurrence_ids": [
              "ProbeFire"
            ],
            "axiom_ids": [
              "A23"
            ],
            "note": "Incoming probes are publicly constrained by the LR/SC reservation exclusion."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::auto.out.c.fire",
            "status": "event_only",
            "occurrence_ids": [
              "CBeat"
            ],
            "axiom_ids": [],
            "note": "Export the accepted C-channel beat. Stateful source selection and continuation locking remain trusted in frozen child region-0-1 and are not reconstructed from hidden child RTL at this parent."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::auto.out.d.fire",
            "status": "constrained",
            "occurrence_ids": [
              "DBeat"
            ],
            "axiom_ids": [
              "A28"
            ],
            "note": "Expose the exact source-based D-channel split between ReleaseAck and miss-machinery grant traffic."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::auto.out.e.fire",
            "status": "event_only",
            "occurrence_ids": [
              "MemFinish"
            ],
            "axiom_ids": [],
            "note": "Export the finish handshake; its exact MSHR bridge is private A2."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.errors.bus.valid",
            "status": "intentionally_omitted",
            "occurrence_ids": [],
            "axiom_ids": [],
            "note": "The parent RTL invalidates/DontCares this error output, so no grounded memory/coherence guarantee is available."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.ll_resp.fire",
            "status": "event_only",
            "occurrence_ids": [
              "LongLatencyResp"
            ],
            "axiom_ids": [],
            "note": "Export the accepted long-latency response; exact MSHR response wiring is private A3."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.nack[0].valid",
            "status": "event_only",
            "occurrence_ids": [
              "NackValid"
            ],
            "axiom_ids": [],
            "note": "Export the LSU nack observation; detailed stage-2 nack conditions remain in the frozen child contract."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.release.fire",
            "status": "event_only",
            "occurrence_ids": [
              "LSURelease"
            ],
            "axiom_ids": [],
            "note": "Export the LSU-visible release; private A4-A6 preserve routing from writeback/probe sources."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.req.bits[0].valid",
            "status": "intentionally_omitted",
            "occurrence_ids": [],
            "axiom_ids": [],
            "note": "This is only per-lane request offer validity, not request acceptance; RequestAccept is the semantic admission event."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.req.fire",
            "status": "constrained",
            "occurrence_ids": [
              "RequestAccept"
            ],
            "axiom_ids": [
              "A30"
            ],
            "note": "A pending long-latency response blocks acceptance of a new LSU request."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.resp[0].valid",
            "status": "event_only",
            "occurrence_ids": [
              "RespValid"
            ],
            "axiom_ids": [],
            "note": "Export the direct LSU response observation; detailed hit/forwarding semantics remain in the frozen region contract."
          },
          {
            "physical_event_id": "BoomNonBlockingDCache::io.lsu.store_ack[0].valid",
            "status": "constrained",
            "occurrence_ids": [
              "StoreAckValid"
            ],
            "axiom_ids": [
              "A29"
            ],
            "note": "Expose that a store ack is either a hit ack or a miss ack coincident with MSHR admission, not necessarily memory completion."
          }
        ]
      }
    }
  }
}
