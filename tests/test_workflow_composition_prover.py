from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from workflow.composition import _canonical_sha256
from workflow.composition_prover import (
    _prove_onehot0_register_invariant,
    prove_composition_obligations,
)
from workflow.formal_patterns import (
    STRUCTURALLY_SUPPORTED,
    prove_scalar_valid_token_provenance,
)
from workflow.semantic import (
    FORMALLY_PROVED,
    HandoffControlModel,
    _build_trusted_umcm,
    freeze_task_dir,
    run_semantic_validation,
)


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

        trusted = _build_trusted_umcm(self.candidate, result["results"])
        self.assertEqual(
            trusted["provenance"]["A1"]["source_axioms"],
            ["BoomMSHR.rpq.main::A1"],
        )
        self.assertEqual(trusted["provenance"]["A1"]["kind"], "lifted")
        self.assertEqual(
            trusted["provenance"]["A5"]["source_axioms"],
            ["BoomMSHR.rpq.main::A11"],
        )
        self.assertEqual(trusted["provenance"]["A5"]["kind"], "emergent")

    def test_declared_provenance_must_match_the_actual_certificate(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["extensions"]["parent_synthesis"]["axiom_provenance"]["A5"]["source_axioms"] = [
            "BoomMSHR.rpq.main::A1"
        ]
        semantic = run_semantic_validation(
            candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        with self.assertRaisesRegex(ValueError, "provenance mismatch.*A5"):
            _build_trusted_umcm(candidate, semantic["results"])

    def test_freeze_preserves_certificate_derived_provenance(self):
        semantic = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        trusted = _build_trusted_umcm(self.candidate, semantic["results"])
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            values = {
                "task.json": {"kind": "parent_synthesis"},
                "response_parsed.json": self.candidate,
                "semantic_validation.json": semantic,
                "trusted_umcm.json": trusted,
                "static_handoff.json": self.handoff,
            }
            for name, value in values.items():
                directory.joinpath(name).write_text(json.dumps(value), encoding="utf-8")
            frozen = freeze_task_dir(directory)
            self.assertEqual(frozen["provenance"], trusted["provenance"])

            directory.joinpath("trusted_umcm.json").write_text(
                json.dumps({key: value for key, value in trusted.items() if key != "provenance"}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "provenance is missing or stale"):
                freeze_task_dir(directory)

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


class PredicateBridgeCompositionRegressionTests(unittest.TestCase):
    @staticmethod
    def _fixture() -> tuple[dict, dict, list[dict]]:
        frozen = {
            "work_unit_id": "Parent.child",
            "trusted_axiom_ids": ["CA1"],
            "occurrences": [{
                "id": "ChildOut",
                "kind": "boundary",
                "physical_event_ids": ["Parent.child::io.out.fire"],
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
            }],
            "predicates": [{
                "id": "ChildBlocked",
                "grounding": {
                    "source_signal": "io.blocked",
                    "negated": False,
                    "state_register": None,
                    "state_values": [],
                },
            }],
            "axioms": [{
                "id": "CA1",
                "formal": {
                    "type": "forbid_when",
                    "predicate": "ChildBlocked",
                    "occurrence": "ChildOut",
                    "scope_identity": None,
                },
            }],
            "freeze": {"status": "FROZEN_FOR_COMPOSITION"},
        }
        summary = {
            "child_id": "Parent.child",
            "boundary_events": ["Parent.child::io.out.fire"],
            "frontier_signals": ["child.io.blocked"],
            "frozen_umcm": frozen,
            "frozen_umcm_sha256": _canonical_sha256(frozen),
        }
        handoff = {
            "work_unit": {"instance_path": "Parent"},
            "composition": {
                "mode": "parent_synthesis",
                "child_summaries": [summary],
            },
            "events": [{
                "id": "Parent.child::io.out.fire",
                "valid": "child.io.out.valid",
                "ready": "child.io.out.ready",
            }],
            "statements": [{
                "id": 1,
                "kind": "connect",
                "text": "connect parent_blocked, child.io.blocked",
                "drives": ["parent_blocked"],
                "reads": ["child.io.blocked"],
                "control_reads": [],
            }],
            "dependency_edges": [
                {
                    "kind": "data",
                    "src": "child.io.blocked",
                    "dst": "parent_blocked",
                    "statement_ids": [1],
                },
                {
                    "kind": "data",
                    "src": "clock",
                    "dst": "child.clock",
                    "statement_ids": [2],
                },
            ],
        }
        candidate = {
            "occurrences": [{
                "id": "ParentOut",
                "kind": "boundary",
                "physical_event_ids": ["Parent.child::io.out.fire"],
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
            }],
            "predicates": [{
                "id": "ParentBlocked",
                "grounding": {
                    "source_signal": "parent_blocked",
                    "negated": False,
                    "state_register": None,
                    "state_values": [],
                },
            }],
            "axioms": [{
                "id": "A1",
                "formal": {
                    "type": "forbid_when",
                    "predicate": "ParentBlocked",
                    "occurrence": "ParentOut",
                    "scope_identity": None,
                },
            }],
        }
        results = [{"axiom_id": "A1", "formal": {"status": "GROUNDED"}}]
        return candidate, handoff, results

    def test_forbid_lift_uses_exact_direct_child_predicate_bridge(self):
        candidate, handoff, results = self._fixture()
        proved = prove_composition_obligations(candidate, handoff, results)
        proof = proved["A1"]
        self.assertEqual(proof["proof_method"], "trusted-child-lift")
        bridge = proof["certificate"]["predicate_bridge"]
        self.assertEqual(bridge["kind"], "exact-parent-child-predicate-equivalence")
        self.assertFalse(bridge["child_rtl_reopened"])

    def test_predicate_bridge_rejects_unexposed_child_signal(self):
        candidate, handoff, results = self._fixture()
        handoff["composition"]["child_summaries"][0]["frontier_signals"] = []
        self.assertNotIn("A1", prove_composition_obligations(candidate, handoff, results))

    def test_predicate_bridge_rejects_non_alias_parent_signal(self):
        candidate, handoff, results = self._fixture()
        statement = handoff["statements"][0]
        statement["text"] = "connect parent_blocked, unrelated"
        statement["reads"] = ["unrelated"]
        handoff["dependency_edges"][0]["src"] = "unrelated"
        self.assertNotIn("A1", prove_composition_obligations(candidate, handoff, results))

class OnehotRegisterInvariantRegressionTests(unittest.TestCase):
    @staticmethod
    def _handoff(second_winner: str = "and(not(a), b)") -> dict:
        return {
            "state": [{"id": "state", "kind": "register", "type": "UInt<1>[2]"}],
            "statements": [
                {"id": 1, "kind": "connect", "text": "connect reset_vec[0], UInt<1>(0h0)", "drives": ["reset_vec[0]"], "reads": [], "control_reads": []},
                {"id": 2, "kind": "connect", "text": "connect reset_vec[1], UInt<1>(0h0)", "drives": ["reset_vec[1]"], "reads": [], "control_reads": []},
                {"id": 3, "kind": "regreset", "text": "regreset state : UInt<1>[2], clock, reset, reset_vec", "drives": ["state"], "reads": ["clock", "reset_vec"], "control_reads": []},
                {"id": 4, "kind": "node", "text": "node muxState = mux(idle, winner, state)", "drives": ["muxState"], "reads": ["idle", "winner", "state"], "control_reads": ["idle"]},
                {"id": 5, "kind": "connect", "text": "connect winner[0], a", "drives": ["winner[0]"], "reads": ["a"], "control_reads": []},
                {"id": 6, "kind": "connect", "text": f"connect winner[1], {second_winner}", "drives": ["winner[1]"], "reads": ["a", "b"], "control_reads": []},
                {"id": 7, "kind": "connect", "text": "connect state, muxState", "drives": ["state[0]", "state[1]"], "reads": ["muxState"], "control_reads": []},
            ],
        }

    @staticmethod
    def _candidate() -> dict:
        return {
            "occurrences": [{
                "id": "Choice",
                "kind": "derived",
                "grounding": {
                    "signals_true": ["a", "b", "idle"],
                    "signals_false": [],
                    "state_register": None,
                    "state_values": [],
                },
            }],
            "predicates": [],
        }

    def test_array_projection_and_inductive_onehot0_certificate(self):
        model = HandoffControlModel(self._handoff())
        self.assertEqual(model.rhs("state[1]"), "muxState[1]")
        proof = _prove_onehot0_register_invariant(
            model,
            self._candidate(),
            "state",
            [0, 1],
        )
        self.assertIsNotNone(proof)
        self.assertEqual(proof[1]["kind"], "exact-inductive-onehot0-register-invariant")

    def test_inductive_onehot0_rejects_nonexclusive_winners(self):
        model = HandoffControlModel(self._handoff(second_winner="b"))
        proof = _prove_onehot0_register_invariant(
            model,
            self._candidate(),
            "state",
            [0, 1],
        )
        self.assertIsNone(proof)

if __name__ == "__main__":
    unittest.main()
