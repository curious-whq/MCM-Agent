from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.composition import _canonical_sha256
from workflow.formal_patterns import (
    STRUCTURALLY_SUPPORTED,
    prove_scalar_valid_token_provenance,
)
from workflow.semantic import FORMALLY_PROVED, HandoffControlModel, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc"
)


class MshrRpqCompositionProverRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))

    def test_real_parent_candidate_is_fully_proved(self):
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        expected = {
            "A1": "trusted-child-lift",
            "A2": "exact-combinational-exclusion",
            "A3": "exact-scalar-valid-token-provenance",
            "A4": "occurrence-bridge-history-composition",
            "A5": "trusted-history-transitivity",
            "A6": "exact-combinational-exclusion",
            "A7": "exact-combinational-exclusion",
        }

        self.assertEqual(result["trusted_axiom_count"], 7, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        for axiom_id, method in expected.items():
            self.assertEqual(by_id[axiom_id]["validation_level"], FORMALLY_PROVED, by_id[axiom_id])
            self.assertEqual(by_id[axiom_id]["formal"]["proof_method"], method, by_id[axiom_id])

    def test_scalar_provenance_rejects_an_extra_creator(self):
        handoff = copy.deepcopy(self.handoff)
        writer = next(statement for statement in handoff["statements"] if statement["id"] == 153)
        writer["text"] = "connect out_valid, UInt<1>(0h1)"
        model = HandoffControlModel(handoff)

        result = prove_scalar_valid_token_provenance(
            model,
            self.candidate,
            before="BufferCapture",
            after="ParentDeqHandshake",
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertIn("unaccounted writer", json.dumps(result), result)

    def test_untrusted_child_history_cannot_prove_parent_transitivity(self):
        handoff = copy.deepcopy(self.handoff)
        summary = handoff["composition"]["child_summaries"][0]
        frozen = summary["frozen_umcm"]
        frozen["trusted_axiom_ids"].remove("A11")
        summary["frozen_umcm_sha256"] = _canonical_sha256(frozen)

        result = run_semantic_validation(
            self.candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED, by_id["A4"])
        self.assertNotEqual(by_id["A5"]["validation_level"], FORMALLY_PROVED, by_id["A5"])

    def test_missing_same_clock_bridge_fails_closed(self):
        handoff = copy.deepcopy(self.handoff)
        handoff["dependency_edges"] = [
            edge for edge in handoff["dependency_edges"]
            if not (edge.get("src") == "clock" and edge.get("dst") == "main.clock")
        ]

        result = run_semantic_validation(
            self.candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A3"]["validation_level"], FORMALLY_PROVED, by_id["A3"])
        self.assertNotEqual(by_id["A1"]["validation_level"], FORMALLY_PROVED, by_id["A1"])
        self.assertNotEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED, by_id["A4"])
        self.assertNotEqual(by_id["A5"]["validation_level"], FORMALLY_PROVED, by_id["A5"])


if __name__ == "__main__":
    unittest.main()
