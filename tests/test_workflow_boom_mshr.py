from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.semantic import COUNTEREXAMPLE, FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "parent_synthesis-BoomMSHR-6362a83e7f824669"
)


class BoomMshrParentRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))

    def _validate(self, handoff=None):
        return run_semantic_validation(
            self.candidate,
            self.handoff if handoff is None else handoff,
            formal_backend="explicit-control",
        )

    def test_real_boom_mshr_parent_is_fully_proved(self):
        result = self._validate()
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(result["trusted_axiom_count"], 15, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        self.assertEqual(by_id["A7"]["formal"]["proof_method"], "exact-bounded-indexed-occurrence")
        self.assertEqual(by_id["A10"]["formal"]["proof_method"], "exact-combinational-exclusion")
        self.assertEqual(by_id["A14"]["formal"]["proof_method"], "trusted-history-after-restriction")
        self.assertEqual(by_id["A15"]["formal"]["proof_method"], "trusted-history-after-restriction")

    def test_exact_formal_proof_can_discharge_a_structural_overapproximation(self):
        result = self._validate()
        axiom = next(item for item in result["results"] if item["axiom_id"] == "A10")
        self.assertEqual(axiom["structural"]["status"], COUNTEREXAMPLE, axiom)
        self.assertEqual(axiom["formal"]["status"], FORMALLY_PROVED, axiom)
        self.assertEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)

    def test_indexed_counter_proof_requires_a_zeroing_entry_cut(self):
        handoff = copy.deepcopy(self.handoff)
        writer = next(item for item in handoff["statements"] if item["id"] == 1111)
        writer["text"] = "connect refill_ctr, UInt<1>(0h1)"
        result = self._validate(handoff)
        axiom = next(item for item in result["results"] if item["axiom_id"] == "A7")
        self.assertNotEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)

    def test_after_restriction_requires_the_direct_child_clock_bridge(self):
        handoff = copy.deepcopy(self.handoff)
        handoff["dependency_edges"] = [
            edge for edge in handoff["dependency_edges"]
            if not (edge.get("src") == "clock" and edge.get("dst") == "rpq.clock")
        ]
        result = self._validate(handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A14"]["validation_level"], FORMALLY_PROVED, by_id["A14"])
        self.assertNotEqual(by_id["A15"]["validation_level"], FORMALLY_PROVED, by_id["A15"])

    def test_state_scoped_bridge_rejects_an_unmodelled_extra_guard(self):
        handoff = copy.deepcopy(self.handoff)
        writer = next(item for item in handoff["statements"] if item["id"] == 1456)
        writer["control_reads"].append("external_extra_guard")
        result = self._validate(handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A14"]["validation_level"], FORMALLY_PROVED, by_id["A14"])
        self.assertEqual(by_id["A15"]["validation_level"], FORMALLY_PROVED, by_id["A15"])


if __name__ == "__main__":
    unittest.main()
