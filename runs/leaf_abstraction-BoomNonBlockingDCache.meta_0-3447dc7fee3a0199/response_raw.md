{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.meta_0-3447dc7fee3a0199",
  "work_unit_id": "BoomNonBlockingDCache.meta_0",
  "occurrences": [
    {
      "id": "ReadRequest",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.meta_0::io.read.fire"
      ],
      "definition": "io.read.valid && io.read.ready; an accepted synchronous metadata-array read whose set index is sampled by the SyncReadMem read port",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.read.valid",
          "io.read.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        49,
        52,
        53,
        54,
        87,
        88
      ]
    },
    {
      "id": "MetadataWrite",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.meta_0::io.write.fire"
      ],
      "definition": "io.write.valid && io.write.ready; an accepted external metadata write that updates the ways selected by io.write.bits.way_en at io.write.bits.idx",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid",
          "io.write.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        10,
        11,
        12,
        14,
        15,
        16,
        17,
        18,
        19,
        32,
        33,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        89,
        90
      ]
    }
  ],
  "predicates": [
    {
      "id": "ResetActive",
      "definition": "rst_cnt < 64",
      "grounding": {
        "source_signal": "rst",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        8,
        9
      ]
    },
    {
      "id": "WriteRequested",
      "definition": "io.write.valid",
      "grounding": {
        "source_signal": "io.write.valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2,
        32,
        87,
        88
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_MetadataRead",
      "trigger_occurrences": [
        "ReadRequest"
      ],
      "guard_predicates": [
        {
          "id": "ResetActive",
          "positive": false
        },
        {
          "id": "WriteRequested",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "An accepted metadata read samples io.read.bits.idx into the synchronous array read port and returns all four ways one cycle later. Each returned lane observes the value of the co-latest prior write to the same set and way."
      ],
      "evidence_statement_ids": [
        31,
        32,
        49,
        52,
        53,
        54,
        57,
        58,
        59,
        60,
        61,
        64,
        65,
        66,
        67,
        68,
        71,
        72,
        73,
        74,
        75,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88
      ],
      "confidence": "high"
    },
    {
      "id": "C2_MetadataWrite",
      "trigger_occurrences": [
        "MetadataWrite"
      ],
      "guard_predicates": [
        {
          "id": "ResetActive",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "An accepted external write updates exactly the ways enabled by io.write.bits.way_en at io.write.bits.idx, storing io.write.bits.data.coh.state and io.write.bits.data.tag."
      ],
      "evidence_statement_ids": [
        9,
        10,
        11,
        12,
        14,
        15,
        16,
        17,
        18,
        19,
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
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        89,
        90
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "indexed_storage_flow",
        "storage": "tag_array",
        "key": {
          "address_domain": {
            "start": 0,
            "end_exclusive": 64
          },
          "lane": {
            "name": "way",
            "count": 4
          }
        },
        "write": {
          "on": "MetadataWrite",
          "address": {
            "op": "signal",
            "name": "io.write.bits.idx"
          },
          "lane_mask": {
            "op": "signal",
            "name": "io.write.bits.way_en"
          }
        },
        "read": {
          "request": "ReadRequest",
          "address": {
            "op": "signal",
            "name": "io.read.bits.idx"
          },
          "latency_cycles": 1
        },
        "value_fields": [
          {
            "name": "coh.state",
            "storage_bits": {
              "hi": 21,
              "lo": 20
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data.coh.state"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0].coh.state"
              },
              {
                "op": "signal",
                "name": "io.resp[1].coh.state"
              },
              {
                "op": "signal",
                "name": "io.resp[2].coh.state"
              },
              {
                "op": "signal",
                "name": "io.resp[3].coh.state"
              }
            ],
            "initial_value": {
              "op": "const",
              "value": 0
            }
          },
          {
            "name": "tag",
            "storage_bits": {
              "hi": 19,
              "lo": 0
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data.tag"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0].tag"
              },
              {
                "op": "signal",
                "name": "io.resp[1].tag"
              },
              {
                "op": "signal",
                "name": "io.resp[2].tag"
              },
              {
                "op": "signal",
                "name": "io.resp[3].tag"
              }
            ],
            "initial_value": {
              "op": "const",
              "value": 0
            }
          }
        ],
        "initialization": {
          "active": {
            "op": "signal",
            "name": "rst"
          },
          "address": {
            "op": "signal",
            "name": "rst_cnt"
          },
          "lane_mask": {
            "op": "const",
            "value": 15
          }
        },
        "resolution": "latest_prior_write_same_key",
        "relations": {
          "rf": "MetaRF",
          "co": "MetaCO",
          "fr": "MetaFR"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MetadataRead",
        "C2_MetadataWrite"
      ],
      "evidence_statement_ids": [
        4,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        27,
        28,
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
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        52,
        53,
        54,
        57,
        58,
        59,
        60,
        61,
        64,
        65,
        66,
        67,
        68,
        71,
        72,
        73,
        74,
        75,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ReadRequest",
        "predicate": "ResetActive",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MetadataRead"
      ],
      "evidence_statement_ids": [
        9,
        32,
        49,
        87,
        88
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MetadataWrite",
        "predicate": "ResetActive",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MetadataWrite"
      ],
      "evidence_statement_ids": [
        9,
        89,
        90
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ReadRequest",
        "predicate": "WriteRequested",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_MetadataRead",
        "C2_MetadataWrite"
      ],
      "evidence_statement_ids": [
        32,
        49,
        87,
        88
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "A1 is the central abstraction. It models tag_array as a 64-set by 4-way persistent metadata store rather than reducing the module to unrelated read and write handshakes.",
    "MetaRF, MetaCO, and MetaFR are exported as one coherent storage relation family. MetaRF relates each returned metadata lane to the co-latest prior write of the same (set, way); MetaCO orders writes to each storage key; MetaFR is derived as MetaRF^-1 ; MetaCO.",
    "Reset is modeled as initialization of every set and all four ways with coh.state=0 and tag=0. rst_cnt starts at zero, advances while rst is active, and rst remains true while rst_cnt < 64.",
    "External writes are masked by io.write.bits.way_en. The actual stored metadata is io.write.bits.data.coh.state and io.write.bits.data.tag; the separate io.write.bits.tag field is not used by the array write and is therefore deliberately omitted.",
    "The read request samples io.read.bits.idx at io.read.fire and has one-cycle synchronous-array latency. The four io.resp lanes correspond positionally to ways 0 through 3.",
    "io.read.bits.way_en is deliberately not used as a read-lane mask in A1. Although rmask is computed by the RTL, the supplied tag_array.read operation returns the complete Vec of four ways and the response wiring exposes all four lanes.",
    "A2 and A3 retain reset access exclusion: reset-generated initialization owns the array while rst is active, so neither external read nor external write can handshake.",
    "A4 retains write-over-read port priority. io.read.ready is false whenever wen = rst || io.write.valid is true, so an asserted external write request prevents an accepted metadata read in that cycle.",
    "No liveness property is claimed. A read or write is modeled only when its boundary handshake actually occurs.",
    "No separate transaction identity key is needed: persistent object identity is already represented by the indexed-storage key (set, way)."
  ],
  "extensions": {}
}