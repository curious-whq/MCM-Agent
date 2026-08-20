from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.composition import _canonical_sha256
from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "parent_synthesis-BoomMSHRFile-9485e49ea1c75380"
)


class BoomMshrFileParentRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))

    def _validate(self, *, candidate=None, handoff=None):
        return run_semantic_validation(
            self.candidate if candidate is None else candidate,
            self.handoff if handoff is None else handoff,
            formal_backend="explicit-control",
        )

    def test_real_boom_mshr_file_parent_is_fully_proved(self):
        result = self._validate()
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertEqual(result["trusted_axiom_count"], 25, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        self.assertEqual(
            by_id["A2"]["formal"]["provenance"]["source_axioms"],
            [
                "BoomMSHRFile.mmio_alloc_arb::A3",
                "BoomMSHRFile.mmio_alloc_arb::A4",
            ],
        )
        self.assertEqual(
            by_id["A3"]["formal"]["certificate"]["partition"]["inductive_invariants"][0]["kind"],
            "exact-inductive-onehot0-register-invariant",
        )
        self.assertEqual(
            by_id["A4"]["formal"]["certificate"]["partition"]["finite_value_consistency"]["kind"],
            "exact-finite-value-atom-consistency",
        )

    def test_mmio_bridge_requires_both_frozen_control_equalities(self):
        handoff = copy.deepcopy(self.handoff)
        summary = next(
            item for item in handoff["composition"]["child_summaries"]
            if item["child_id"] == "BoomMSHRFile.mmio_alloc_arb"
        )
        summary["frozen_umcm"]["trusted_axiom_ids"].remove("A4")
        summary["frozen_umcm_sha256"] = _canonical_sha256(summary["frozen_umcm"])

        result = self._validate(handoff=handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A2"]["validation_level"], FORMALLY_PROVED)

    def test_grant_partition_requires_formal_source_three_grounding(self):
        candidate = copy.deepcopy(self.candidate)
        occurrence = next(
            item for item in candidate["occurrences"]
            if item["id"] == "MMIOGrantDelivery"
        )
        occurrence["grounding"].pop("value_tests")

        result = self._validate(candidate=candidate)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED)


if __name__ == "__main__":
    unittest.main()
