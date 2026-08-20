from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.formal_patterns import (
    STRUCTURALLY_SUPPORTED,
    prove_combinational_forbid_when,
    prove_same_index_valid_token_provenance,
)
from workflow.semantic import FORMALLY_PROVED, HandoffControlModel, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8"
)


class MshrRpqFormalPatternRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))
        # A9 was an over-strong aggregate equality: out.uop is overwritten from
        # the separately maintained uops array.  The refined candidate drops it.
        candidate["axioms"] = [axiom for axiom in candidate["axioms"] if axiom["id"] != "A9"]
        cls.candidate = candidate

    def test_real_mshr_rpq_candidate_is_fully_proved(self):
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertEqual(result["candidate_axiom_count"], 9, result)
        self.assertEqual(result["trusted_axiom_count"], 9, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)

        for axiom_id in ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]:
            self.assertEqual(by_id[axiom_id]["validation_level"], FORMALLY_PROVED, by_id[axiom_id])
            self.assertEqual(
                by_id[axiom_id]["formal"]["proof_method"],
                "exact-combinational-exclusion",
                by_id[axiom_id],
            )

        self.assertEqual(by_id["A8"]["validation_level"], FORMALLY_PROVED, by_id["A8"])
        self.assertEqual(by_id["A11"]["validation_level"], FORMALLY_PROVED, by_id["A11"])
        self.assertEqual(
            by_id["A11"]["formal"]["proof_method"],
            "exact-indexed-valid-token-provenance",
            by_id["A11"],
        )

    def test_combinational_exclusion_fails_closed_when_not_logically_forbidden(self):
        candidate = copy.deepcopy(self.candidate)
        queue_full = next(item for item in candidate["predicates"] if item["id"] == "QueueFull")
        queue_full["grounding"]["source_signal"] = "io.enq.valid"
        model = HandoffControlModel(self.handoff)

        result = prove_combinational_forbid_when(
            model,
            candidate,
            occurrence="EnqHandshake",
            predicate="QueueFull",
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)

    def test_valid_token_provenance_rejects_unaccounted_creator(self):
        handoff = copy.deepcopy(self.handoff)
        victim = next(statement for statement in handoff["statements"] if statement["id"] == 257)
        victim["text"] = "connect valids[deq_ptr_value], UInt<1>(0h1)"
        model = HandoffControlModel(handoff)

        result = prove_same_index_valid_token_provenance(
            model,
            self.candidate,
            before="QueueInsert",
            after="DeqHandshake",
            scope_index={"name": "slot", "relation": "same"},
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertIn("unaccounted writer", result.get("reason", ""))


if __name__ == "__main__":
    unittest.main()
