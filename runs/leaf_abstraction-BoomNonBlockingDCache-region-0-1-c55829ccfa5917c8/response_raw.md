{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8",
  "work_unit_id": "BoomNonBlockingDCache::region-0-1",
  "occurrences": [
    {
      "id": "OutputCFire",
      "kind": "boundary",
      "physical_event_ids": [
        "BoomNonBlockingDCache::auto.out.c.fire"
      ],
      "definition": "auto.out.c.valid && auto.out.c.ready; one accepted TileLink C output beat",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2609,
        2625,
        2626,
        2627,
        2628,
        2630,
        2631,
        2632
      ]
    },
    {
      "id": "WBStartBeat",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "nodeOut.c.fire && idle && winner[0]; first/only accepted beat of a writeback-release transaction",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "nodeOut.c.valid",
          "nodeOut.c.ready",
          "idle",
          "winner[0]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2559,
        2560,
        2561,
        2569,
        2572,
        2574,
        2577,
        2609,
        2618,
        2625,
        2631,
        2632
      ]
    },
    {
      "id": "ProbeStartBeat",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "nodeOut.c.fire && idle && winner[1]; first/only accepted beat of a probe-reply transaction",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "nodeOut.c.valid",
          "nodeOut.c.ready",
          "idle",
          "winner[1]"
        ],
        "signals_false": []
      },
      "evidence_statement_ids": [
        2559,
        2560,
        2561,
        2570,
        2573,
        2575,
        2578,
        2609,
        2618,
        2625,
        2631,
        2632
      ]
    },
    {
      "id": "WBContinuationBeat",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "nodeOut.c.fire && !idle && state[0]; an accepted continuation beat while the multibeat arbiter is locked to writeback release",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "nodeOut.c.valid",
          "nodeOut.c.ready",
          "state[0]"
        ],
        "signals_false": [
          "idle"
        ]
      },
      "evidence_statement_ids": [
        2559,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619,
        2626,
        2628,
        2630,
        2631,
        2632
      ]
    },
    {
      "id": "ProbeContinuationBeat",
      "kind": "derived",
      "physical_event_ids": [],
      "definition": "nodeOut.c.fire && !idle && state[1]; an accepted continuation beat while the multibeat arbiter is locked to probe reply",
      "multiplicity": "repeatable",
      "index": null,
      "grounding": {
        "state_register": null,
        "state_values": [],
        "signals_true": [
          "nodeOut.c.valid",
          "nodeOut.c.ready",
          "state[1]"
        ],
        "signals_false": [
          "idle"
        ]
      },
      "evidence_statement_ids": [
        2559,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619,
        2627,
        2628,
        2630,
        2631,
        2632
      ]
    }
  ],
  "predicates": [
    {
      "id": "WBReleaseValid",
      "definition": "wb.io.release.valid",
      "grounding": {
        "source_signal": "wb.io.release.valid",
        "negated": false,
        "state_register": null,
        "state_values": []
      },
      "evidence_statement_ids": [
        2561,
        2574,
        2625,
        2626
      ]
    }
  ],
  "identity_keys": [],
  "cases": [
    {
      "id": "C1_WBStart",
      "trigger_occurrences": [
        "WBStartBeat"
      ],
      "guard_predicates": [],
      "emits": [
        "OutputCFire"
      ],
      "relations": [
        "When idle, source 0 may win the TileLink C arbiter and the accepted output beat carries wb.io.release payload."
      ],
      "evidence_statement_ids": [
        2559,
        2560,
        2561,
        2569,
        2572,
        2574,
        2577,
        2618,
        2631,
        2632,
        2634,
        2640,
        2650,
        2656,
        2662,
        2668,
        2674,
        2680,
        2681,
        2682,
        2683,
        2684,
        2685,
        2686
      ],
      "confidence": "high"
    },
    {
      "id": "C2_ProbeStart",
      "trigger_occurrences": [
        "ProbeStartBeat"
      ],
      "guard_predicates": [
        {
          "id": "WBReleaseValid",
          "positive": false
        }
      ],
      "emits": [
        "OutputCFire"
      ],
      "relations": [
        "When idle, source 1 may begin only when the higher-priority writeback source is not valid; the output carries prober.io.rep payload."
      ],
      "evidence_statement_ids": [
        2561,
        2562,
        2563,
        2564,
        2565,
        2566,
        2567,
        2568,
        2570,
        2573,
        2575,
        2578,
        2618,
        2631,
        2632,
        2635,
        2641,
        2651,
        2657,
        2663,
        2669,
        2675,
        2680,
        2681,
        2682,
        2683,
        2684,
        2685,
        2686
      ],
      "confidence": "high"
    },
    {
      "id": "C3_WBContinuation",
      "trigger_occurrences": [
        "WBContinuationBeat"
      ],
      "guard_predicates": [],
      "emits": [
        "OutputCFire"
      ],
      "relations": [
        "While beatsLeft is nonzero and state[0] is retained, continuation output beats remain selected from wb.io.release regardless of newly competing probe traffic."
      ],
      "evidence_statement_ids": [
        2559,
        2606,
        2607,
        2608,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619,
        2626,
        2628,
        2630,
        2631,
        2632
      ],
      "confidence": "high"
    },
    {
      "id": "C4_ProbeContinuation",
      "trigger_occurrences": [
        "ProbeContinuationBeat"
      ],
      "guard_predicates": [],
      "emits": [
        "OutputCFire"
      ],
      "relations": [
        "While beatsLeft is nonzero and state[1] is retained, continuation output beats remain selected from prober.io.rep regardless of newly competing writeback traffic."
      ],
      "evidence_statement_ids": [
        2559,
        2606,
        2607,
        2608,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619,
        2627,
        2628,
        2630,
        2631,
        2632
      ],
      "confidence": "high"
    }
  ],
  "axioms": [
    {
      "id": "A1",
      "formal": {
        "type": "occurrence_partition",
        "whole": "OutputCFire",
        "parts": [
          "WBStartBeat",
          "ProbeStartBeat",
          "WBContinuationBeat",
          "ProbeContinuationBeat"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart",
        "C2_ProbeStart",
        "C3_WBContinuation",
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2559,
        2560,
        2561,
        2569,
        2570,
        2572,
        2573,
        2574,
        2575,
        2577,
        2578,
        2609,
        2618,
        2619,
        2625,
        2626,
        2627,
        2628,
        2630,
        2631,
        2632
      ],
      "status": "candidate"
    },
    {
      "id": "A2",
      "formal": {
        "type": "forbid_when",
        "occurrence": "ProbeStartBeat",
        "predicate": "WBReleaseValid",
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2561,
        2562,
        2563,
        2564,
        2565,
        2566,
        2567,
        2568,
        2570,
        2573,
        2575,
        2578
      ],
      "status": "candidate"
    },
    {
      "id": "A3",
      "formal": {
        "type": "ordered_before",
        "before": "WBStartBeat",
        "after": "WBContinuationBeat",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart",
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2559,
        2606,
        2608,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619
      ],
      "status": "candidate"
    },
    {
      "id": "A4",
      "formal": {
        "type": "ordered_before",
        "before": "ProbeStartBeat",
        "after": "ProbeContinuationBeat",
        "required_prior": null,
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart",
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2559,
        2607,
        2608,
        2609,
        2610,
        2611,
        2612,
        2613,
        2618,
        2619
      ],
      "status": "candidate"
    },
    {
      "id": "A5",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.address",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.address"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2650,
        2652,
        2654,
        2655,
        2682
      ],
      "status": "candidate"
    },
    {
      "id": "A6",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.source",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.source"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2656,
        2658,
        2660,
        2661,
        2683
      ],
      "status": "candidate"
    },
    {
      "id": "A7",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.size",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2662,
        2664,
        2666,
        2667,
        2684
      ],
      "status": "candidate"
    },
    {
      "id": "A8",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.param",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.param"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2668,
        2670,
        2672,
        2673,
        2685
      ],
      "status": "candidate"
    },
    {
      "id": "A9",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.opcode",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.opcode"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2674,
        2676,
        2678,
        2679,
        2686
      ],
      "status": "candidate"
    },
    {
      "id": "A10",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.data",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2640,
        2642,
        2644,
        2645,
        2681
      ],
      "status": "candidate"
    },
    {
      "id": "A11",
      "formal": {
        "type": "signal_equality",
        "on": "WBStartBeat",
        "target": "nodeOut.c.bits.corrupt",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.corrupt"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C1_WBStart"
      ],
      "evidence_statement_ids": [
        2618,
        2634,
        2636,
        2638,
        2639,
        2680
      ],
      "status": "candidate"
    },
    {
      "id": "A12",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.address",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.address"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2650,
        2652,
        2654,
        2655,
        2682
      ],
      "status": "candidate"
    },
    {
      "id": "A13",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.source",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.source"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2656,
        2658,
        2660,
        2661,
        2683
      ],
      "status": "candidate"
    },
    {
      "id": "A14",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.size",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2662,
        2664,
        2666,
        2667,
        2684
      ],
      "status": "candidate"
    },
    {
      "id": "A15",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.param",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.param"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2668,
        2670,
        2672,
        2673,
        2685
      ],
      "status": "candidate"
    },
    {
      "id": "A16",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.opcode",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.opcode"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2674,
        2676,
        2678,
        2679,
        2686
      ],
      "status": "candidate"
    },
    {
      "id": "A17",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.data",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2640,
        2642,
        2644,
        2645,
        2681
      ],
      "status": "candidate"
    },
    {
      "id": "A18",
      "formal": {
        "type": "signal_equality",
        "on": "WBContinuationBeat",
        "target": "nodeOut.c.bits.corrupt",
        "source": {
          "op": "signal",
          "name": "wb.io.release.bits.corrupt"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C3_WBContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2634,
        2636,
        2638,
        2639,
        2680
      ],
      "status": "candidate"
    },
    {
      "id": "A19",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.address",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.address"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2651,
        2652,
        2654,
        2655,
        2682
      ],
      "status": "candidate"
    },
    {
      "id": "A20",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.source",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.source"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2657,
        2658,
        2660,
        2661,
        2683
      ],
      "status": "candidate"
    },
    {
      "id": "A21",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.size",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2663,
        2664,
        2666,
        2667,
        2684
      ],
      "status": "candidate"
    },
    {
      "id": "A22",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.param",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.param"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2669,
        2670,
        2672,
        2673,
        2685
      ],
      "status": "candidate"
    },
    {
      "id": "A23",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.opcode",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.opcode"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2675,
        2676,
        2678,
        2679,
        2686
      ],
      "status": "candidate"
    },
    {
      "id": "A24",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.data",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2641,
        2642,
        2644,
        2645,
        2681
      ],
      "status": "candidate"
    },
    {
      "id": "A25",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeStartBeat",
        "target": "nodeOut.c.bits.corrupt",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.corrupt"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C2_ProbeStart"
      ],
      "evidence_statement_ids": [
        2618,
        2635,
        2636,
        2638,
        2639,
        2680
      ],
      "status": "candidate"
    },
    {
      "id": "A26",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.address",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.address"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2651,
        2652,
        2654,
        2655,
        2682
      ],
      "status": "candidate"
    },
    {
      "id": "A27",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.source",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.source"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2657,
        2658,
        2660,
        2661,
        2683
      ],
      "status": "candidate"
    },
    {
      "id": "A28",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.size",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.size"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2663,
        2664,
        2666,
        2667,
        2684
      ],
      "status": "candidate"
    },
    {
      "id": "A29",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.param",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.param"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2669,
        2670,
        2672,
        2673,
        2685
      ],
      "status": "candidate"
    },
    {
      "id": "A30",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.opcode",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.opcode"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2675,
        2676,
        2678,
        2679,
        2686
      ],
      "status": "candidate"
    },
    {
      "id": "A31",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.data",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.data"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2641,
        2642,
        2644,
        2645,
        2681
      ],
      "status": "candidate"
    },
    {
      "id": "A32",
      "formal": {
        "type": "signal_equality",
        "on": "ProbeContinuationBeat",
        "target": "nodeOut.c.bits.corrupt",
        "source": {
          "op": "signal",
          "name": "prober.io.rep.bits.corrupt"
        },
        "scope_identity": null
      },
      "derived_from_case_ids": [
        "C4_ProbeContinuation"
      ],
      "evidence_statement_ids": [
        2618,
        2619,
        2635,
        2636,
        2638,
        2639,
        2680
      ],
      "status": "candidate"
    }
  ],
  "assumptions": [],
  "unresolved": [],
  "rationale": [
    "This region is a stateful two-source TileLink C arbiter rather than an ordinary combinational Chisel Arbiter. Source 0 is wb.io.release and source 1 is prober.io.rep.",
    "The lowestIndexFirst policy gives source 0 priority over source 1 only when a new transaction starts while the arbiter is idle. ProbeStartBeat is therefore forbidden when WBReleaseValid holds, but no such exclusion is imposed on ProbeContinuationBeat.",
    "A1 partitions every accepted C-channel beat into exactly one of four paths: writeback start, probe-reply start, writeback continuation, or probe-reply continuation.",
    "When idle, muxState is winner. When beatsLeft is nonzero, muxState is the stored state vector. The state register therefore locks the selected source across continuation beats of a multibeat TileLink transaction.",
    "A3 and A4 preserve the grounded history fact that a continuation beat from either source requires a prior start beat from that source. No stronger generation-scoped claim is made because this WorkUnit does not expose a reusable transaction-generation identifier.",
    "A5-A32 preserve the complete non-empty TileLink C payload for both sources in both start and continuation phases: opcode, param, source, address, size, data, and corrupt.",
    "No exact indexed_complete beat-count axiom is emitted. Transaction length depends dynamically on opcode/hasData and size rather than one static finite index domain; omitting exact beat completeness is a safe over-approximation.",
    "No liveness or fairness property is claimed. Backpressure can stall start or continuation beats indefinitely."
  ],
  "extensions": {}
}