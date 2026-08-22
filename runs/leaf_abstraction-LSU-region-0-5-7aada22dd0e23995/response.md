Current Formal AST is sufficient.

## FINAL MCM-AGENT RESULT

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-5-7aada22dd0e23995",
  "work_unit_id": "LSU::region-0-5",
  "occurrences": [
    {
      "id": "HellaRequest",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.hellacache.req.fire"
      ],
      "definition": "grounded boundary occurrence LSU::io.hellacache.req.fire",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.hellacache.req.valid",
          "io.hellacache.req.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": []
    },
    {
      "id": "LowLatencyResponse",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.dmem.ll_resp.fire"
      ],
      "definition": "grounded boundary occurrence LSU::io.dmem.ll_resp.fire",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.dmem.ll_resp.valid",
          "io.dmem.ll_resp.ready"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        8057
      ]
    },
    {
      "id": "HellaResponse",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.hellacache.resp.valid"
      ],
      "definition": "grounded boundary occurrence LSU::io.hellacache.resp.valid",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.hellacache.resp.valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        7985,
        8061,
        8073
      ]
    }
  ],
  "predicates": [],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_HellaResponse",
      "trigger_occurrences": [
        "HellaResponse"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The shim exposes a HellaCache response whose invariant metadata is wired locally; the exact data-source split is intentionally left unconstrained in this leaf abstraction."
      ],
      "evidence_statement_ids": [
        7985,
        7992,
        7993,
        7994,
        7995,
        7997,
        7998,
        7999,
        8056,
        8057,
        8058,
        8059,
        8061,
        8067,
        8068,
        8069,
        8070,
        8071,
        8073,
        8079
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "value_constraint",
        "on": "HellaResponse",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.hellacache.resp.bits.replay"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 0,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7992
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "value_constraint",
        "on": "HellaResponse",
        "expr": {
          "op": "bit",
          "value": {
            "op": "signal",
            "name": "io.hellacache.resp.bits.has_data"
          },
          "index": 0
        },
        "relation": "eq",
        "value": 1,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7993
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "signal_equality",
        "on": "HellaResponse",
        "target": "io.hellacache.resp.bits.dprv",
        "source": {
          "op": "signal",
          "name": "io.ptw.status.prv"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7997
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "HellaResponse",
        "target": "io.hellacache.resp.bits.dv",
        "source": {
          "op": "signal",
          "name": "io.ptw.status.v"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7998
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "HellaResponse",
        "target": "io.hellacache.resp.bits.data_word_bypass",
        "source": {
          "op": "signal",
          "name": "io.dmem.ll_resp.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7994
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "HellaResponse",
        "target": "io.hellacache.resp.bits.data_raw",
        "source": {
          "op": "signal",
          "name": "io.dmem.ll_resp.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_HellaResponse"
      ],
      "evidence_statement_ids": [
        7995
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region owns only the combinational Hella/uncached response shim, not the Hella FSM/request-capture state that orders a request with its eventual response.",
    "All three physical boundary occurrences owned by the WorkUnit are exported: HellaRequest, LowLatencyResponse, and HellaResponse. Their cross-cycle lifecycle is intentionally left for parent synthesis, where hella_state and hella_req are available.",
    "A1-A6 preserve exact response metadata and raw/bypass wiring that is invariant across the locally visible response paths.",
    "The final response data field can be written either from io.dmem.ll_resp.bits.data or, on a later same-cycle override, from io.dmem.resp[0].bits.data. The complete Hella FSM/source-selection history spans parent-owned state, so this first leaf summary deliberately leaves final data-source classification unconstrained rather than inventing a local request-to-response theorem.",
    "Omitting that source split widens the model safely and is an explicit CEGAR refinement point; no fairness or response-liveness claim is made."
  ],
  "extensions": {}
}
```
