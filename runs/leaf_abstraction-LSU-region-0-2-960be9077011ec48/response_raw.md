{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-region-0-2-960be9077011ec48",
  "work_unit_id": "LSU::region-0-2",
  "occurrences": [
    {
      "id": "FPResponse",
      "kind": "boundary",
      "physical_event_ids": [
        "LSU::io.core.fresp[0].valid"
      ],
      "definition": "io.core.fresp[0].valid; one floating-point LSU response is made visible to the core",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "io.core.fresp[0].valid"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        6581
      ]
    }
  ],
  "predicates": [],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_CoreVisibleFPResponse",
      "trigger_occurrences": [
        "FPResponse"
      ],
      "guard_predicates": [],
      "emits": [],
      "relations": [
        "The core-visible FP response carries the final internal fresp payload selected elsewhere in the LSU."
      ],
      "evidence_statement_ids": [
        6581
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.data",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.rob_idx",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.rob_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.ldq_idx",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.ldq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.stq_idx",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.stq_idx"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.mem_cmd",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.mem_cmd"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.mem_size",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.mem_size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.mem_signed",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.mem_signed"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "FPResponse",
        "target": "io.core.fresp[0].bits.uop.br_mask",
        "source": {
          "op": "signal",
          "name": "fresp[0].bits.uop.br_mask"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_CoreVisibleFPResponse"
      ],
      "evidence_statement_ids": [
        6581
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "FPResponse is the only physical boundary occurrence in this WorkUnit. It represents a floating-point LSU response becoming visible to the core.",
    "The parent-facing memory-relevant payload projections are preserved: returned data, ROB identity, LDQ/STQ indices, memory command, memory size, signedness, and branch mask.",
    "A1-A8 are grounded by the exact bulk connection io.core.fresp[0] := fresp[0]. They do not invent any additional response-generation semantics.",
    "The supplied ledger contains two distinct assignments to the internal fresp payload. The normal DCache-response path assigns fresp[0].bits.uop from uop and fresp[0].bits.data from resp.data.",
    "A later forwarding path assigns fresp[0].bits.uop from wb_ldst_forward_e[0].uop and computes fresp[0].bits.data from forwarded load data using address, size, and signedness.",
    "The control statements that determine when the normal-response assignment or forwarding assignment is active are not present in this WorkUnit ledger. In particular, no grounded statement here establishes an exact predicate partition for FPResponse by source.",
    "Therefore no DCacheFPResponse/ForwardedFPResponse occurrence partition is emitted. Guessing such a partition from payload assignments alone would overstate the available RTL evidence.",
    "The omission of source classification is a safe over-approximation: the abstraction may permit additional FP-response provenance or values, but it does not remove a concrete RTL behavior. A parent-level spurious counterexample may later trigger CEGAR reopening with the missing control slice.",
    "The wb_ldst_forward_e_REG register captures a branch-mask-updated LDQ entry one cycle earlier, but the current ledger does not contain enough response-valid control to soundly connect that register to every FPResponse. No cross-cycle identity or ordered_before claim is therefore made.",
    "The byte/halfword/word sign-extension network on the forwarding data path is not separately axiomatized because its applicability depends on the missing forwarding-path guard. Applying it to every FPResponse would be unsound.",
    "Floating-point flags and predication fields are omitted because this µMCM abstraction is concerned with memory-ordering/value provenance rather than floating-point arithmetic status.",
    "No liveness or eventual-response property is claimed."
  ],
  "extensions": {}
}