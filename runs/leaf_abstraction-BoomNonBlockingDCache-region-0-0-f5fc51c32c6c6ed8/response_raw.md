{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-0-f5fc51c32c6c6ed8",
  "work_unit_id": "BoomNonBlockingDCache::region-0-0",
  "occurrences": [
    {
      "id": "ProbeFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.b.fire"
      ],
      "definition": "auto.out.b.valid && auto.out.b.ready; an accepted incoming TileLink B probe",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2486,
        2487,
        2488
      ]
    }
  ],
  "predicates": [
    {
      "id": "LRSCValid",
      "definition": "lrsc_valid is asserted",
      "grounding": {
        "source_signal": "lrsc_valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2486,
        2487,
        2488
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_ProbeAccepted",
      "trigger_occurrences": [
        "ProbeFire"
      ],
      "guard_predicates": [
        {
          "id": "LRSCValid",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "An incoming TileLink B probe can handshake only when lrsc_valid is false."
      ],
      "evidence_statement_ids": [
        2486,
        2487,
        2488
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ProbeFire",
        "predicate": "LRSCValid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_ProbeAccepted"
      ],
      "evidence_statement_ids": [
        2486,
        2487,
        2488
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "The parent-facing memory/coherence fact in this region is the exact exclusion between lrsc_valid and acceptance of an incoming TileLink B probe.",
    "A1 follows directly from nodeOut.b.ready = prober.io.req.ready && !lrsc_valid. Therefore ProbeFire is impossible whenever LRSCValid holds, independent of the value of prober.io.req.ready.",
    "lrsc_count is updated locally: it decrements while nonzero, is loaded to 79 on the grounded LR path, and is cleared by several local conditions. These details are not promoted to semantic milestones because this WorkUnit does not contain an exact grounded definition relating lrsc_valid to lrsc_count.",
    "LRSCValid is therefore modeled directly from the frontier signal lrsc_valid rather than reconstructed from lrsc_count. This avoids inventing a relation not present in the supplied FIRRTL statement ledger.",
    "No LR, SC, reservation-install, reservation-expire, or reservation-clear occurrence is introduced. Their exact event definitions would require additional RTL evidence beyond this WorkUnit and are not necessary to state the exact probe exclusion available here.",
    "The TileLink B payload is not transformed by the local behavior represented in this region, so no additional payload-flow axiom is necessary.",
    "No liveness property is claimed: in particular, the abstraction does not claim that LRSCValid eventually clears or that a blocked probe is eventually accepted.",
    "No transaction identity key is required for A1 because the exclusion is global with respect to the current lrsc_valid state rather than scoped to a particular probe transaction."
  ],
  "extensions": {}
}