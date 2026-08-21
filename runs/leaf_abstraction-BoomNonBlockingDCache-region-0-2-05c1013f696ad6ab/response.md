{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-2-05c1013f696ad6ab",
  "work_unit_id": "BoomNonBlockingDCache::region-0-2",
  "occurrences": [
    {
      "id": "DFire",
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
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2507,
        2508,
        2509,
        2519,
        2520
      ]
    },
    {
      "id": "ReleaseAckFire",
      "kind": "derived",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.d.fire"
      ],
      "definition": "DFire with nodeOut.d.bits.source == 2; this D beat follows the local ReleaseAck path",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "signal",
              "name": "nodeOut.d.bits.source"
            },
            "relation": "eq",
            "value": 2
          }
        ]
      },
      "evidence_statement_ids": [
        2507,
        2508,
        2509
      ]
    },
    {
      "id": "MSHRGrantFire",
      "kind": "derived",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.d.fire"
      ],
      "definition": "DFire with nodeOut.d.bits.source != 2; this accepted D beat is forwarded through mshrs.io.mem_grant",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": [],
        "value_tests": [
          {
            "expr": {
              "op": "signal",
              "name": "nodeOut.d.bits.source"
            },
            "relation": "neq",
            "value": 2
          }
        ]
      },
      "evidence_statement_ids": [
        2507,
        2508,
        2519,
        2520
      ]
    }
  ],
  "predicates": [
    {
      "id": "ReleaseAckSource",
      "definition": "nodeOut.d.bits.source == 2",
      "grounding": {
        "source_signal": "_T_82",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2507
      ]
    },
    {
      "id": "NonReleaseAckSource",
      "definition": "nodeOut.d.bits.source != 2",
      "grounding": {
        "source_signal": "_T_82",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2507
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_ReleaseAckConsumed",
      "trigger_occurrences": [
        "ReleaseAckFire"
      ],
      "guard_predicates": [
        {
          "id": "ReleaseAckSource",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A D-channel beat whose source is 2 is accepted on the local ReleaseAck path rather than being routed through the MSHR grant interface."
      ],
      "evidence_statement_ids": [
        2507,
        2508,
        2509
      ],
      "confidence": "high"
    },
    {
      "id": "C2_MSHRGrantForwarded",
      "trigger_occurrences": [
        "MSHRGrantFire"
      ],
      "guard_predicates": [
        {
          "id": "NonReleaseAckSource",
          "positive": true
        }
      ],
      "emits": [],
      "relations": [
        "A D-channel beat whose source is not 2 is forwarded through mshrs.io.mem_grant with the complete TileLink D payload preserved."
      ],
      "evidence_statement_ids": [
        2507,
        2508,
        2519,
        2520
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "DFire",
        "parts": [
          "ReleaseAckFire",
          "MSHRGrantFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ReleaseAckConsumed",
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2507,
        2508,
        2509,
        2519,
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ReleaseAckFire",
        "predicate": "NonReleaseAckSource",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ReleaseAckConsumed"
      ],
      "evidence_statement_ids": [
        2507,
        2508,
        2509
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "MSHRGrantFire",
        "predicate": "ReleaseAckSource",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2507,
        2508,
        2519,
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.opcode",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.opcode"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.param",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.param"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.size",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.source",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.source"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.sink",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.sink"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.denied",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.denied"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.data",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "MSHRGrantFire",
        "target": "mshrs.io.mem_grant.bits.corrupt",
        "source": {
          "op": "signal",
          "name": "nodeOut.d.bits.corrupt"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_MSHRGrantForwarded"
      ],
      "evidence_statement_ids": [
        2520
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region performs an exact source-based split of accepted TileLink D traffic. Source value 2 is the local ReleaseAck path; every other source is handled by the MSHR grant path.",
    "A1 preserves exact same-cycle conservation: every accepted D beat belongs to exactly one of ReleaseAckFire or MSHRGrantFire.",
    "A2 and A3 preserve the source discriminator independently of the partition, preventing the abstraction from exchanging the ReleaseAck and MSHR-grant paths.",
    "For source 2 the RTL forces nodeOut.d.ready to one. The candidate deliberately does not encode the stronger valid-to-fire implication. Omitting this combinational no-backpressure fact can only introduce extra abstract stalling and is therefore a safe over-approximation for memory-order analysis.",
    "For source values other than 2, the bulk connection mshrs.io.mem_grant <> nodeOut.d forwards the full non-empty TileLink D payload. A4-A11 preserve opcode, param, size, source, sink, denied, data, and corrupt.",
    "No claim is made that non-2 sources are limited to specific numerical MSHR IDs; the supplied RTL forwards every source value other than 2 through the else path.",
    "No transaction identity key is introduced because this region contains no state and performs only same-cycle classification/routing.",
    "No liveness or fairness property is required. Backpressure on the MSHRGrant path is inherited from mshrs.io.mem_grant.ready, while the stronger no-backpressure property of the ReleaseAck path is deliberately omitted as a safe strengthening candidate for later CEGAR."
  ],
  "extensions": {}
}