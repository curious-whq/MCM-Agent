{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac",
  "work_unit_id": "BoomMSHRFile.prefetcher",
  "occurrences": [
    {
      "id": "PrefetchHandshake",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.prefetcher::io.prefetch.fire"
      ],
      "definition": "io.prefetch.valid && io.prefetch.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        3
      ]
    }
  ],
  "predicates": [
    {
      "id": "PrefetchDisabled",
      "definition": "io.prefetch.valid == 0",
      "grounding": {
        "source_signal": "io.prefetch.valid",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        3
      ]
    }
  ],
  "identity_keys": [],
  "cases": [],
  "axioms": [
    {
      "id": "A1",
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
        3
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "PrefetchHandshake",
        "predicate": "PrefetchDisabled",
        "scope_identity": null
      },
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "NullPrefetcher has no concrete local state and unconditionally drives io.prefetch.valid to zero, so it cannot emit a valid prefetch transaction.",
    "A1 is the substantive parent-facing guarantee: the prefetch valid signal is permanently zero. Because PrefetchHandshake is the physical Decoupled fire event, this makes the boundary occurrence unreachable for every value of io.prefetch.ready.",
    "A2 retains the physical PrefetchHandshake occurrence and its explicit exclusion under PrefetchDisabled in the trusted semantic interface. It is redundant with the boundary handshake definition plus A1, but preserves the otherwise unreachable boundary occurrence for hierarchical composition.",
    "All io.prefetch.bits fields are invalidated by DontCare. No payload equality, transaction identity, or ordering fact is claimed because valid is permanently zero and no payload can participate in a real transaction.",
    "No liveness or environment readiness assumption is needed because the implementation disables prefetch generation independently of io.prefetch.ready, mshr_avail, req_val, req_addr, and req_coh."
  ],
  "extensions": {}
}