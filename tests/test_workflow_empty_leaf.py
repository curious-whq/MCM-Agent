from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from workflow.schema import UMCM_SCHEMA_VERSION
from workflow.semantic import freeze_task_dir, run_semantic_validation, validate_task_dir


def _candidate() -> dict:
    return {
        "schema_version": UMCM_SCHEMA_VERSION,
        "task_id": "empty-leaf-task",
        "work_unit_id": "Parent.comb",
        "occurrences": [],
        "predicates": [],
        "identity_keys": [],
        "cases": [],
        "axioms": [],
        "assumptions": [],
        "unresolved": [],
        "rationale": [
            "This covered combinational leaf is intentionally left unconstrained as a safe over-approximation."
        ],
        "extensions": {},
    }


def _handoff() -> dict:
    return {
        "work_unit": {
            "id": "Parent.comb",
            "instance_path": "Parent.comb",
            "module": "Comb",
            "kind": "module",
            "is_leaf": True,
            "coverage_complete": True,
        },
        "events": [],
        "state": [],
        "memory_state": [],
        "statements": [{
            "id": 1,
            "kind": "connect",
            "text": "connect io.out, io.in",
            "drives": ["io.out"],
            "reads": ["io.in"],
            "control_reads": [],
        }],
    }


class EmptyLeafAbstractionTests(unittest.TestCase):
    def test_covered_stateless_eventless_leaf_is_vacuously_validated(self):
        result = run_semantic_validation(
            _candidate(),
            _handoff(),
            formal_backend="explicit-control",
        )

        self.assertTrue(result["all_axioms_formally_proved"], result)
        self.assertEqual(result["candidate_axiom_count"], 0)
        self.assertEqual(
            result["empty_abstraction_certificate"]["policy"],
            "covered-explicit-empty-leaf-overapproximation-v0.1",
        )

    def test_stateful_eventful_empty_leaf_remains_auditable_overapproximation(self):
        handoff = copy.deepcopy(_handoff())
        handoff["events"] = [{"id": "Parent.comb::io.out.valid"}]
        handoff["state"] = [{"id": "state"}]
        handoff["memory_state"] = ["mem"]

        result = run_semantic_validation(
            _candidate(),
            handoff,
            formal_backend="explicit-control",
        )

        self.assertTrue(result["all_axioms_formally_proved"], result)
        certificate = result["empty_abstraction_certificate"]
        self.assertEqual(certificate["owned_event_count"], 1)
        self.assertEqual(certificate["owned_state_count"], 1)
        self.assertEqual(certificate["owned_memory_state_count"], 1)

    def test_empty_leaf_is_fail_closed_if_coverage_or_declaration_is_incomplete(self):
        for field, value in (
            ("coverage_complete", False),
            ("unresolved", [{"id": "U1"}]),
            ("assumptions", [{"id": "S1"}]),
        ):
            with self.subTest(field=field):
                handoff = copy.deepcopy(_handoff())
                candidate = _candidate()
                if field == "coverage_complete":
                    handoff["work_unit"][field] = value
                else:
                    candidate[field] = value
                result = run_semantic_validation(
                    candidate,
                    handoff,
                    formal_backend="explicit-control",
                )
                self.assertFalse(result["all_axioms_formally_proved"], result)
                self.assertIsNone(result["empty_abstraction_certificate"])

    def test_certified_empty_leaf_can_freeze_for_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp)
            task_dir.joinpath("task.json").write_text(
                json.dumps({
                    "task_id": "empty-leaf-task",
                    "kind": "leaf_abstraction",
                    "work_unit_id": "Parent.comb",
                }),
                encoding="utf-8",
            )
            task_dir.joinpath("response_parsed.json").write_text(
                json.dumps(_candidate()), encoding="utf-8"
            )
            task_dir.joinpath("validation.json").write_text(
                json.dumps({"valid": True}), encoding="utf-8"
            )
            task_dir.joinpath("static_handoff.json").write_text(
                json.dumps(_handoff()), encoding="utf-8"
            )

            semantic = validate_task_dir(task_dir, formal_backend="explicit-control")
            frozen = freeze_task_dir(task_dir)

            self.assertTrue(semantic["all_axioms_formally_proved"])
            self.assertTrue(frozen["freeze"]["empty_abstraction"])
            self.assertEqual(frozen["axioms"], [])
            self.assertIn("empty_abstraction", frozen)


if __name__ == "__main__":
    unittest.main()
