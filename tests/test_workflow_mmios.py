from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259"
)


class BoomIOMSHRProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))

    def _validate(self, handoff=None):
        return run_semantic_validation(
            copy.deepcopy(self.candidate),
            copy.deepcopy(handoff or self.handoff),
            formal_backend="explicit-control",
        )

    def test_real_mmio_fsm_and_payload_candidate_is_fully_proved(self):
        result = self._validate()
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertTrue(result["all_axioms_formally_proved"], result)
        self.assertEqual(result["trusted_axiom_count"], 9)
        for axiom_id in ("A1", "A2", "A3", "A4"):
            self.assertEqual(
                by_id[axiom_id]["formal"]["proof_method"],
                "exhaustive-state-reachability",
                by_id[axiom_id],
            )
        self.assertEqual(
            by_id["A6"]["formal"]["proof_method"],
            "exact-symbolic-transaction-identity",
        )
        for axiom_id in ("A7", "A8"):
            self.assertEqual(
                by_id[axiom_id]["formal"]["proof_method"],
                "exact-conditional-symbolic-driver-equality",
                by_id[axiom_id],
            )

    def test_identity_capture_fails_if_lowered_fire_drops_ready(self):
        handoff = copy.deepcopy(self.handoff)
        fire = next(statement for statement in handoff["statements"] if statement["id"] == 1601)
        fire["text"] = "node _T_6 = io.req.valid"
        fire["reads"] = ["io.req.valid"]

        result = self._validate(handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertNotEqual(by_id["A6"]["validation_level"], FORMALLY_PROVED)
        self.assertIn("not guarded", by_id["A6"]["structural"]["reason"])

    def test_payload_proof_fails_if_one_reachable_mux_arm_changes_address(self):
        handoff = copy.deepcopy(self.handoff)
        put_address = next(statement for statement in handoff["statements"] if statement["id"] == 224)
        put_address["text"] = "connect put.address, UInt<32>(0h1)"
        put_address["reads"] = []

        result = self._validate(handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertNotEqual(by_id["A7"]["validation_level"], FORMALLY_PROVED)
        self.assertIn("not equal", by_id["A7"]["formal"]["reason"])


if __name__ == "__main__":
    unittest.main()
