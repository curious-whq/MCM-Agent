{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-4-f13601df6f3c1120",
  "work_unit_id": "BoomNonBlockingDCache::region-0-4",
  "occurrences": [
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
        272,
        273,
        274,
        275
      ]
    }
  ],
  "predicates": [
    {
      "id": "MSHRResponsePending",
      "definition": "mshrs.io.resp.valid",
      "grounding": {
        "source_signal": "mshrs.io.resp.valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        271
      ]
    },
    {
      "id": "MetaReadUnavailable",
      "definition": "!metaReadArb.io.in[4].ready",
      "grounding": {
        "source_signal": "metaReadArb.io.in[4].ready",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        272
      ]
    },
    {
      "id": "DataReadUnavailable",
      "definition": "!dataReadArb.io.in[2].ready",
      "grounding": {
        "source_signal": "dataReadArb.io.in[2].ready",
        "negated": true,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        272
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_RequestAccepted",
      "trigger_occurrences": [
        "RequestAccept"
      ],
      "guard_predicates": [
        {
          "id": "MSHRResponsePending",
          "positive": false
        },
        {
          "id": "MetaReadUnavailable",
          "positive": false
        },
        {
          "id": "DataReadUnavailable",
          "positive": false
        }
      ],
      "emits": [],
      "relations": [
        "An LSU request can be accepted only when no MSHR response is blocking admission and both the metadata-read and data-read arbitration inputs are ready."
      ],
      "evidence_statement_ids": [
        271,
        272,
        273,
        274,
        275
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RequestAccept",
        "predicate": "MSHRResponsePending",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestAccepted"
      ],
      "evidence_statement_ids": [
        271,
        273,
        274,
        275
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RequestAccept",
        "predicate": "MetaReadUnavailable",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestAccepted"
      ],
      "evidence_statement_ids": [
        272,
        274,
        275
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "forbid_when",
        "occurrence": "RequestAccept",
        "predicate": "DataReadUnavailable",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_RequestAccepted"
      ],
      "evidence_statement_ids": [
        272,
        274,
        275
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region is a stateless admission-control fragment. Its only physical semantic occurrence is acceptance of an LSU request.",
    "Because lsuWidth is one in this elaboration, block_incoming_reqs is exactly mshrs.io.resp.valid. A1 therefore preserves the explicit design rule that a returning MSHR response blocks acceptance of a new LSU request.",
    "A2 and A3 preserve the two independent downstream resource requirements: the metadata-read arbiter input and data-read arbiter input must both be ready before io.lsu.req.ready can assert.",
    "The conjunction implemented by RTL is io.lsu.req.ready = metaReadArb.io.in[4].ready && dataReadArb.io.in[2].ready && !mshrs.io.resp.valid.",
    "The candidate intentionally records only the necessary admission exclusions rather than a stronger valid-implies-fire rule. Omitting sufficiency permits extra abstract stalls and is therefore a safe over-approximation.",
    "No request payload axioms are emitted. This region does not transform the LSU request payload, and the supplied FIRRTL ledger contains only the ready-path logic; inventing downstream payload forwarding claims would exceed the available evidence.",
    "No transaction identity key is needed because there is no local state or cross-cycle request retention in this WorkUnit.",
    "No fairness or eventual-acceptance property is claimed. Either downstream arbiter may remain not ready indefinitely, and an MSHR response may delay admission."
  ],
  "extensions": {}
}