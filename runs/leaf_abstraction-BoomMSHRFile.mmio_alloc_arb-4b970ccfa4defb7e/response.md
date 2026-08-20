{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e",
  "work_unit_id": "BoomMSHRFile.mmio_alloc_arb",
  "occurrences": [
    {
      "id": "InputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmio_alloc_arb::io.in[0].fire"
      ],
      "definition": "io.in[0].valid && io.in[0].ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        5,
        6
      ]
    },
    {
      "id": "OutputFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomMSHRFile.mmio_alloc_arb::io.out.fire"
      ],
      "definition": "io.out.valid && io.out.ready",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        7,
        8,
        9
      ]
    }
  ],
  "predicates": [],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_Passthrough",
      "trigger_occurrences": [
        "InputFire"
      ],
      "guard_predicates": [],
      "emits": [
        "OutputFire"
      ],
      "relations": [
        "The single accepted MMIO-allocation input is forwarded to the output in exactly the same cycle."
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        8,
        9
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "OutputFire",
        "parts": [
          "InputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Passthrough"
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        8,
        9
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "signal_equality",
        "on": "InputFire",
        "target": "io.out.bits",
        "source": {
          "op": "signal",
          "name": "io.in[0].bits"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_Passthrough"
      ],
      "evidence_statement_ids": [
        4
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "Arbiter1_Bool contains only one input and no local state, so it is semantically a combinational Decoupled passthrough rather than a genuine competing-request arbiter.",
    "A1 uses occurrence_partition with a singleton parts set. Pairwise exclusion is vacuous, while whole-equivalence reduces exactly to OutputFire iff InputFire in the same cycle.",
    "The RTL establishes handshake equivalence because io.in[0].ready is exactly io.out.ready and io.out.valid simplifies exactly to io.in[0].valid.",
    "A2 retains the complete one-bit MMIO-allocation payload; there is no reason to project or weaken a single Boolean field.",
    "No priority predicate or exclusion axiom is needed because there is no competing input.",
    "No cross-cycle identity key exists because the module has no registers and stores no transaction state.",
    "No ordered_before relation is emitted because input acceptance and output emission are the same-cycle routed transaction.",
    "No liveness or output-readiness fairness property is claimed."
  ],
  "extensions": {}
}