from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.axiom_ir import compile_formal_axiom, render_formal_axiom
from workflow.manual import validate_candidate_grounding
from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomNonBlockingDCache.meta_0-42629071bfba9ff5"
)


def _sig(name: str) -> dict:
    return {"op": "signal", "name": name}


def _const(value: int) -> dict:
    return {"op": "const", "value": value}


def _candidate(task_id: str) -> dict:
    formal = {
        "type": "indexed_storage_flow",
        "storage": "tag_array",
        "key": {
            "address_domain": {"start": 0, "end_exclusive": 64},
            "lane": {"name": "way", "count": 4},
        },
        "write": {
            "on": "MetadataWrite",
            "address": _sig("io.write.bits.idx"),
            "lane_mask": _sig("io.write.bits.way_en"),
        },
        "read": {
            "request": "ReadRequest",
            "address": _sig("io.read.bits.idx"),
            "latency_cycles": 1,
        },
        "value_fields": [
            {
                "name": "coh.state",
                "storage_bits": {"hi": 21, "lo": 20},
                "write_value": _sig("io.write.bits.data.coh.state"),
                "read_targets": [_sig(f"io.resp[{index}].coh.state") for index in range(4)],
                "initial_value": _const(0),
            },
            {
                "name": "tag",
                "storage_bits": {"hi": 19, "lo": 0},
                "write_value": _sig("io.write.bits.data.tag"),
                "read_targets": [_sig(f"io.resp[{index}].tag") for index in range(4)],
                "initial_value": _const(0),
            },
        ],
        "initialization": {
            "active": _sig("rst"),
            "address": _sig("rst_cnt"),
            "lane_mask": _const(15),
        },
        "resolution": "latest_prior_write_same_key",
        "relations": {"rf": "MetaRF", "co": "MetaCO", "fr": "MetaFR"},
        "scope_identity": None,
    }
    return {
        "schema_version": "umcm-formal-0.5",
        "task_id": task_id,
        "work_unit_id": "BoomNonBlockingDCache.meta_0",
        "occurrences": [
            {
                "id": "ReadRequest",
                "kind": "boundary",
                "physical_event_ids": ["BoomNonBlockingDCache.meta_0::io.read.fire"],
                "definition": "accepted metadata read request",
                "multiplicity": "repeatable",
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
                "evidence_statement_ids": [49, 52, 53, 54, 88],
            },
            {
                "id": "MetadataWrite",
                "kind": "boundary",
                "physical_event_ids": ["BoomNonBlockingDCache.meta_0::io.write.fire"],
                "definition": "accepted metadata write",
                "multiplicity": "repeatable",
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
                "evidence_statement_ids": [10, 11, 12, 14, 15, 16, 17, 18, 19, 32, 40, 42, 44, 46, 48, 90],
            },
        ],
        "predicates": [],
        "identity_keys": [],
        "cases": [{
            "id": "C1",
            "trigger_occurrences": ["ReadRequest", "MetadataWrite"],
            "guard_predicates": [],
            "emits": ["ReadRequest", "MetadataWrite"],
            "relations": ["persistent indexed metadata storage"],
            "evidence_statement_ids": list(range(4, 91)),
            "confidence": "high",
        }],
        "axioms": [{
            "id": "A1",
            "formal": formal,
            "derived_from_case_ids": ["C1"],
            "evidence_statement_ids": list(range(4, 91)),
            "status": "candidate",
        }],
        "assumptions": [],
        "unresolved": [],
        "rationale": "exact synchronous metadata storage semantics",
        "extensions": {},
    }


class IndexedStorageFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((RUN_DIR / "task.json").read_text(encoding="utf-8"))
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = _candidate(cls.task["task_id"])

    def test_ast_compiles_standard_memory_relations(self):
        formal = self.candidate["axioms"][0]["formal"]
        compiled = compile_formal_axiom(formal)
        self.assertEqual(compiled["checker"], "indexed_storage_flow")
        self.assertEqual(compiled["arguments"]["relations"]["rf"], "MetaRF")
        self.assertIn("MetaFR=rf^-1;co", render_formal_axiom(formal))

    def test_real_metadata_array_proves_rf_co_fr(self):
        grounding = validate_candidate_grounding(self.candidate, self.task, self.handoff)
        self.assertTrue(grounding["valid"], grounding)
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(result["trusted_axiom_count"], 1, result)
        proof = result["results"][0]["formal"]
        self.assertEqual(proof["status"], FORMALLY_PROVED)
        certificate = proof["certificate"]
        self.assertEqual(certificate["relations"]["fr"]["definition"], "rf^-1 ; co")
        self.assertEqual(certificate["initialization"]["kind"], "exact-reset-initialization-sweep")
        self.assertEqual(certificate["collision_policy"], "read_write_exclusive")

    def test_wrong_read_lane_binding_fails_closed(self):
        candidate = copy.deepcopy(self.candidate)
        targets = candidate["axioms"][0]["formal"]["value_fields"][1]["read_targets"]
        targets[0], targets[1] = targets[1], targets[0]
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)

    def test_incomplete_initialization_sweep_fails_closed(self):
        handoff = copy.deepcopy(self.handoff)
        handoff["statements"] = [item for item in handoff["statements"] if item["id"] != 30]
        result = run_semantic_validation(self.candidate, handoff, formal_backend="explicit-control")
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)

    def test_wrong_sync_latency_fails_closed(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["axioms"][0]["formal"]["read"]["latency_cycles"] = 0
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)


if __name__ == "__main__":
    unittest.main()
