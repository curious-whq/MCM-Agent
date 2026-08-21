from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.axiom_ir import compile_formal_axiom
from workflow.manual import validate_candidate_grounding
from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29"
)


def _sig(name: str) -> dict:
    return {"op": "signal", "name": name}


def _shr(name: str, amount: int) -> dict:
    return {"op": "shr", "value": _sig(name), "amount": amount}


def _candidate(task_id: str) -> dict:
    selectors = ["_T_1", "_T_4", "_T_7", "_T_10"]
    write_evidence = [[6, 7, 8, 13, 15], [25, 26, 27, 32, 34], [44, 45, 46, 51, 53], [63, 64, 65, 70, 72]]
    read_evidence = [[18, 19, 20, 21, 22, 23], [37, 38, 39, 40, 41, 42], [56, 57, 58, 59, 60, 61], [75, 76, 77, 78, 79, 80]]
    occurrences = [{
        "id": "ReadRequest",
        "kind": "boundary",
        "physical_event_ids": ["BoomNonBlockingDCache.data::io.read[0].valid"],
        "definition": "accepted synchronous data-array read request",
        "multiplicity": "repeatable",
        "grounding": {
            "state_register": None,
            "state_values": [],
            "signals_true": [],
            "signals_false": [],
        },
        "evidence_statement_ids": [4, 18, 19, 20, 37, 38, 39, 56, 57, 58, 75, 76, 77],
    }]
    axioms = []
    for way in range(4):
        occurrence = f"Way{way}WritePort"
        occurrences.append({
            "id": occurrence,
            "kind": "derived",
            "physical_event_ids": [],
            "definition": f"write port for physical way {way} is selected",
            "multiplicity": "repeatable",
            "grounding": {
                "state_register": None,
                "state_values": [],
                "signals_true": [selectors[way]],
                "signals_false": [],
            },
            "evidence_statement_ids": write_evidence[way],
        })
        axioms.append({
            "id": f"A{way + 1}",
            "formal": {
                "type": "indexed_storage_flow",
                "storage": f"array_{way}_0",
                "key": {
                    "address_domain": {"start": 0, "end_exclusive": 512},
                    "lane": {"name": "lane", "count": 1},
                },
                "write": {
                    "on": occurrence,
                    "address": _shr("io.write.bits.addr", 3),
                    "lane_mask": _sig("io.write.bits.wmask"),
                },
                "read": {
                    "request": "ReadRequest",
                    "address": _shr("io.read[0].bits.addr", 3),
                    "latency_cycles": 2,
                },
                "value_fields": [{
                    "name": "data",
                    "storage_bits": {"hi": 63, "lo": 0},
                    "write_value": _sig("io.write.bits.data"),
                    "read_targets": [_sig(f"io.resp[0][{way}]")],
                }],
                "initialization": {"kind": "implicit_unconstrained"},
                "resolution": "latest_prior_write_same_key",
                "relations": {
                    "rf": f"Way{way}RF",
                    "co": f"Way{way}CO",
                    "fr": f"Way{way}FR",
                },
                "read_write_collision": "implicit_unconstrained",
                "scope_identity": None,
            },
            "derived_from_case_ids": ["C1"],
            "evidence_statement_ids": sorted(set([3, 4, 5 + 19 * way, *write_evidence[way], *read_evidence[way]])),
            "status": "candidate",
        })
    return {
        "schema_version": "umcm-formal-0.5",
        "task_id": task_id,
        "work_unit_id": "BoomNonBlockingDCache.data",
        "occurrences": occurrences,
        "predicates": [],
        "identity_keys": [],
        "cases": [{
            "id": "C1",
            "trigger_occurrences": ["ReadRequest", *[f"Way{way}WritePort" for way in range(4)]],
            "guard_predicates": [],
            "emits": ["ReadRequest", *[f"Way{way}WritePort" for way in range(4)]],
            "relations": ["four physical SRAMs implement persistent data storage"],
            "evidence_statement_ids": list(range(3, 81)),
            "confidence": "high",
        }],
        "axioms": axioms,
        "assumptions": [],
        "unresolved": [],
        "rationale": "uninitialized cells are unconstrained; written cells retain latest-write semantics",
        "extensions": {},
    }


class UninitializedIndexedStorageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((RUN_DIR / "task.json").read_text(encoding="utf-8"))
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = _candidate(cls.task["task_id"])

    def test_implicit_initialization_compiles_without_a_fixed_value(self):
        compiled = compile_formal_axiom(self.candidate["axioms"][0]["formal"])
        self.assertEqual(
            compiled["arguments"]["initialization"],
            {"kind": "implicit_unconstrained"},
        )
        self.assertNotIn("initial_value", compiled["arguments"]["value_fields"][0])

    def test_fixed_initial_value_is_rejected_for_uninitialized_storage(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["axioms"][0]["formal"]["value_fields"][0]["initial_value"] = {
            "op": "const",
            "value": 0,
        }
        grounding = validate_candidate_grounding(candidate, self.task, self.handoff)
        self.assertFalse(grounding["valid"], grounding)
        self.assertTrue(any("must be omitted" in item for item in grounding["errors"]))

    def test_real_duplicated_data_array_proves_all_four_storage_flows(self):
        grounding = validate_candidate_grounding(self.candidate, self.task, self.handoff)
        self.assertTrue(grounding["valid"], grounding)
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(result["trusted_axiom_count"], 4, result)
        for item in result["results"]:
            self.assertEqual(item["formal"]["status"], FORMALLY_PROVED)
            certificate = item["formal"]["certificate"]
            self.assertEqual(
                certificate["initialization"]["kind"],
                "implicit-unconstrained-initial-writes",
            )
            self.assertEqual(certificate["storage"]["read_latency_cycles"], 2)
            self.assertEqual(
                certificate["collision_certificate"]["kind"],
                "implicit-unconstrained-collision-write",
            )

    def test_cell_write_occurrence_can_absorb_the_lane_mask(self):
        candidate = copy.deepcopy(self.candidate)
        occurrence = next(
            item for item in candidate["occurrences"] if item["id"] == "Way0WritePort"
        )
        occurrence["grounding"] = {
            "state_register": None,
            "state_values": [],
            "signals_true": ["io.write.valid"],
            "signals_false": [],
            "value_tests": [
                {
                    "expr": {"op": "bit", "value": _sig("io.write.bits.way_en"), "index": 0},
                    "relation": "eq",
                    "value": 1,
                },
                {
                    "expr": {"op": "bit", "value": _sig("io.write.bits.wmask"), "index": 0},
                    "relation": "eq",
                    "value": 1,
                },
            ],
        }
        candidate["axioms"][0]["formal"]["write"]["lane_mask"] = {
            "op": "const",
            "value": 1,
        }

        grounding = validate_candidate_grounding(candidate, self.task, self.handoff)
        self.assertTrue(grounding["valid"], grounding)
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        first = result["results"][0]
        self.assertEqual(first["formal"]["status"], FORMALLY_PROVED, first)
        self.assertEqual(
            first["formal"]["certificate"]["write_occurrence_binding"]["kind"],
            "exact-cell-write-occurrence",
        )

    def test_claiming_one_cycle_latency_fails_closed(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["axioms"][0]["formal"]["read"]["latency_cycles"] = 1
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)

    def test_claiming_collision_exclusion_fails_closed(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["axioms"][0]["formal"]["read_write_collision"] = "exclusive"
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)


if __name__ == "__main__":
    unittest.main()
