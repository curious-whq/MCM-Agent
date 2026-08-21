{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29",
  "work_unit_id": "BoomNonBlockingDCache.data",
  "occurrences": [
    {
      "id": "ReadRequest",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.data::io.read[0].valid"
      ],
      "definition": "io.read[0].valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.read[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        4,
        18,
        19,
        20,
        37,
        38,
        39,
        56,
        57,
        58,
        75,
        76,
        77
      ]
    },
    {
      "id": "WriteRequest",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache.data::io.write.valid"
      ],
      "definition": "io.write.valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        3,
        7,
        26,
        45,
        64
      ]
    },
    {
      "id": "Way0Write",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.write.valid && io.write.bits.way_en[0] && io.write.bits.wmask[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.way_en"
              },
              "index": 0
            },
            "relation": "eq",
            "value": 1
          },
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.wmask"
              },
              "index": 0
            },
            "relation": "eq",
            "value": 1
          }
        ]
      },
      "evidence_statement_ids": [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ]
    },
    {
      "id": "Way1Write",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.write.valid && io.write.bits.way_en[1] && io.write.bits.wmask[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.way_en"
              },
              "index": 1
            },
            "relation": "eq",
            "value": 1
          },
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.wmask"
              },
              "index": 0
            },
            "relation": "eq",
            "value": 1
          }
        ]
      },
      "evidence_statement_ids": [
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34
      ]
    },
    {
      "id": "Way2Write",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.write.valid && io.write.bits.way_en[2] && io.write.bits.wmask[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.way_en"
              },
              "index": 2
            },
            "relation": "eq",
            "value": 1
          },
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.wmask"
              },
              "index": 0
            },
            "relation": "eq",
            "value": 1
          }
        ]
      },
      "evidence_statement_ids": [
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53
      ]
    },
    {
      "id": "Way3Write",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "io.write.valid && io.write.bits.way_en[3] && io.write.bits.wmask[0]",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.write.valid"
        ],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.way_en"
              },
              "index": 3
            },
            "relation": "eq",
            "value": 1
          },
          {
            "expr": {
              "op": "bit",
              "value": {
                "op": "signal",
                "name": "io.write.bits.wmask"
              },
              "index": 0
            },
            "relation": "eq",
            "value": 1
          }
        ]
      },
      "evidence_statement_ids": [
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72
      ]
    }
  ],
  "predicates": [],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_DataRead",
      "trigger_occurrences": [
        "ReadRequest"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "A read samples row address io.read[0].bits.addr >> 3 into all four independent way SRAMs; each selected SRAM value is exposed through an additional register stage."
      ],
      "evidence_statement_ids": [
        4,
        5,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80
      ],
      "confidence": "high"
    },
    {
      "id": "C2_Way0Write",
      "trigger_occurrences": [
        "Way0Write"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "Way 0 at row io.write.bits.addr >> 3 is updated with io.write.bits.data."
      ],
      "evidence_statement_ids": [
        3,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "confidence": "high"
    },
    {
      "id": "C3_Way1Write",
      "trigger_occurrences": [
        "Way1Write"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "Way 1 at row io.write.bits.addr >> 3 is updated with io.write.bits.data."
      ],
      "evidence_statement_ids": [
        3,
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
        34
      ],
      "confidence": "high"
    },
    {
      "id": "C4_Way2Write",
      "trigger_occurrences": [
        "Way2Write"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "Way 2 at row io.write.bits.addr >> 3 is updated with io.write.bits.data."
      ],
      "evidence_statement_ids": [
        3,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53
      ],
      "confidence": "high"
    },
    {
      "id": "C5_Way3Write",
      "trigger_occurrences": [
        "Way3Write"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "Way 3 at row io.write.bits.addr >> 3 is updated with io.write.bits.data."
      ],
      "evidence_statement_ids": [
        3,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "indexed_storage_flow",
        "storage": "array_0_0",
        "key": {
          "address_domain": {
            "start": 0,
            "end_exclusive": 512
          },
          "lane": {
            "name": "word",
            "count": 1
          }
        },
        "write": {
          "on": "Way0Write",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.write.bits.addr"
            },
            "amount": 3
          },
          "lane_mask": {
            "op": "const",
            "value": 1
          }
        },
        "read": {
          "request": "ReadRequest",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.read[0].bits.addr"
            },
            "amount": 3
          },
          "latency_cycles": 2
        },
        "value_fields": [
          {
            "name": "data",
            "storage_bits": {
              "hi": 63,
              "lo": 0
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0][0]"
              }
            ]
          }
        ],
        "initialization": {
          "kind": "implicit_unconstrained"
        },
        "read_write_collision": "implicit_unconstrained",
        "resolution": "latest_prior_write_same_key",
        "relations": {
          "rf": "DataWay0RF",
          "co": "DataWay0CO",
          "fr": "DataWay0FR"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_DataRead",
        "C2_Way0Write"
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
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "indexed_storage_flow",
        "storage": "array_1_0",
        "key": {
          "address_domain": {
            "start": 0,
            "end_exclusive": 512
          },
          "lane": {
            "name": "word",
            "count": 1
          }
        },
        "write": {
          "on": "Way1Write",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.write.bits.addr"
            },
            "amount": 3
          },
          "lane_mask": {
            "op": "const",
            "value": 1
          }
        },
        "read": {
          "request": "ReadRequest",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.read[0].bits.addr"
            },
            "amount": 3
          },
          "latency_cycles": 2
        },
        "value_fields": [
          {
            "name": "data",
            "storage_bits": {
              "hi": 63,
              "lo": 0
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0][1]"
              }
            ]
          }
        ],
        "initialization": {
          "kind": "implicit_unconstrained"
        },
        "read_write_collision": "implicit_unconstrained",
        "resolution": "latest_prior_write_same_key",
        "relations": {
          "rf": "DataWay1RF",
          "co": "DataWay1CO",
          "fr": "DataWay1FR"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_DataRead",
        "C3_Way1Write"
      ],
      "evidence_statement_ids": [
        3,
        4,
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
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "indexed_storage_flow",
        "storage": "array_2_0",
        "key": {
          "address_domain": {
            "start": 0,
            "end_exclusive": 512
          },
          "lane": {
            "name": "word",
            "count": 1
          }
        },
        "write": {
          "on": "Way2Write",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.write.bits.addr"
            },
            "amount": 3
          },
          "lane_mask": {
            "op": "const",
            "value": 1
          }
        },
        "read": {
          "request": "ReadRequest",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.read[0].bits.addr"
            },
            "amount": 3
          },
          "latency_cycles": 2
        },
        "value_fields": [
          {
            "name": "data",
            "storage_bits": {
              "hi": 63,
              "lo": 0
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0][2]"
              }
            ]
          }
        ],
        "initialization": {
          "kind": "implicit_unconstrained"
        },
        "read_write_collision": "implicit_unconstrained",
        "resolution": "latest_prior_write_same_key",
        "relations": {
          "rf": "DataWay2RF",
          "co": "DataWay2CO",
          "fr": "DataWay2FR"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_DataRead",
        "C4_Way2Write"
      ],
      "evidence_statement_ids": [
        3,
        4,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "indexed_storage_flow",
        "storage": "array_3_0",
        "key": {
          "address_domain": {
            "start": 0,
            "end_exclusive": 512
          },
          "lane": {
            "name": "word",
            "count": 1
          }
        },
        "write": {
          "on": "Way3Write",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.write.bits.addr"
            },
            "amount": 3
          },
          "lane_mask": {
            "op": "const",
            "value": 1
          }
        },
        "read": {
          "request": "ReadRequest",
          "address": {
            "op": "shr",
            "value": {
              "op": "signal",
              "name": "io.read[0].bits.addr"
            },
            "amount": 3
          },
          "latency_cycles": 2
        },
        "value_fields": [
          {
            "name": "data",
            "storage_bits": {
              "hi": 63,
              "lo": 0
            },
            "write_value": {
              "op": "signal",
              "name": "io.write.bits.data"
            },
            "read_targets": [
              {
                "op": "signal",
                "name": "io.resp[0][3]"
              }
            ]
          }
        ],
        "initialization": {
          "kind": "implicit_unconstrained"
        },
        "read_write_collision": "implicit_unconstrained",
        "resolution": "latest_prior_write_same_key",
        "relations": {
          "rf": "DataWay3RF",
          "co": "DataWay3CO",
          "fr": "DataWay3FR"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_DataRead",
        "C5_Way3Write"
      ],
      "evidence_statement_ids": [
        3,
        4,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "value_constraint",
        "on": null,
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.s1_nacks[0]"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        81
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The data array is implemented as four independent 512-entry synchronous SRAMs, one per cache way, rather than one four-lane Vec memory. Modeling one indexed_storage_flow per physical SRAM avoids inventing a non-existent monolithic storage object.",
    "The storage key for each physical SRAM is its 9-bit row address, obtained by shifting the 12-bit cache-data address right by rowOffBits=3. The cache way is represented by the choice of physical storage object rather than by a four-valued lane index.",
    "Way0Write through Way3Write are actual storage-update occurrences rather than aliases of io.write.valid. A real SRAM update additionally requires the corresponding io.write.bits.way_en bit and the single row-word mask bit io.write.bits.wmask[0].",
    "Each SRAM contains one 64-bit row word. Therefore once the actual per-way write occurrence is established, the indexed_storage_flow lane mask is the constant one and io.write.bits.data is the complete stored word.",
    "There is no reset or power-up initialization for any of the four data SRAMs. Each storage therefore uses implicit_unconstrained initialization: each row begins with a fresh unconstrained abstract initial write rather than an invented zero value.",
    "ReadRequest simultaneously samples the same shifted row address into all four physical SRAM read ports. io.read[0].bits.way_en does not gate these reads in the supplied RTL and is deliberately omitted from the storage key or read enable.",
    "The final parent-visible data has two cycles of latency from ReadRequest: SyncReadMem supplies a synchronous read result and the RTL then applies an additional RegNext before driving io.resp[0][way].",
    "A read and write are not mutually excluded. When ReadRequest and a WayNWrite target the same row in the same cycle, SyncReadMem read-during-write data is not specified by this RTL. read_write_collision=implicit_unconstrained therefore allows that read to source from a transient unconstrained abstract write while keeping the real write ordered in co.",
    "For non-collision reads, DataWayNRF selects the co-latest prior same-row write for that physical way; DataWayNCO is the per-row write order and DataWayNFR is derived as rf^-1 ; co.",
    "A5 preserves the exact architectural control fact that this data-array implementation never generates an s1 nack.",
    "No liveness or fairness assumptions are required because both interfaces are Valid rather than ready/valid handshakes."
  ],
  "extensions": {}
}