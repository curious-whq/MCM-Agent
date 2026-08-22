from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.axiom_ir import compile_formal_axiom, validate_formal_axiom_shape
from workflow.manual import validate_candidate_grounding
from workflow.schema import UMCM_SCHEMA_VERSION, parse_candidate_response
from workflow.semantic import FORMALLY_PROVED, REFUTED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-LSU-state-0-9-e3ad39242c816d77"
)


def _formal() -> dict:
    return {
        "type": "register_transition",
        "register": "ldq_tail",
        "width": 4,
        "updates": [
            {
                "guard": {"op": "signal", "name": "_T_1150"},
                "next": {"op": "const", "value": 0},
            },
            {
                "guard": {"op": "signal", "name": "_T_1092"},
                "next": {
                    "op": "signal",
                    "name": "io.core.brupdate.b2.uop.ldq_idx",
                },
            },
            {
                "guard": {"op": "signal", "name": "dis_ld_val"},
                "next": {
                    "op": "modular_increment",
                    "value": {"op": "signal", "name": "ldq_tail"},
                    "modulus": 16,
                },
            },
        ],
        "priority": "first_match",
        "default": {"op": "signal", "name": "ldq_tail"},
        "scope_identity": None,
    }


def _candidate(task: dict, handoff: dict) -> dict:
    return {
        "schema_version": UMCM_SCHEMA_VERSION,
        "task_id": task["task_id"],
        "work_unit_id": task["work_unit_id"],
        "occurrences": [],
        "predicates": [],
        "identity_keys": [],
        "cases": [],
        "axioms": [
            {
                "id": "A1",
                "formal": _formal(),
                "derived_from_case_ids": [],
                "evidence_statement_ids": list(
                    handoff["grounding"]["allowed_statement_ids"]
                ),
                "status": "candidate",
            }
        ],
        "assumptions": [],
        "unresolved": [],
        "rationale": ["Complete priority next-state semantics for ldq_tail."],
        "extensions": {},
    }


def _with_state_writer_controls(handoff: dict) -> dict:
    result = copy.deepcopy(handoff)
    blocks = [
        {
            "id": 900001,
            "kind": "when",
            "text": "when _T_1092 :",
            "drives": [],
            "reads": ["_T_1092"],
            "control_reads": ["_T_1092"],
        },
        {
            "id": 900002,
            "kind": "when",
            "text": "when _T_1150 :",
            "drives": [],
            "reads": ["_T_1150"],
            "control_reads": ["_T_1150"],
        },
    ]
    context = result.setdefault("proof_context", {})
    context["state_writer_control_statement_ids"] = [900001, 900002]
    context["state_writer_control_statements"] = blocks
    for edge in result["dependency_edges"]:
        if edge.get("kind") != "control" or edge.get("dst") != "ldq_tail":
            continue
        if edge.get("src") == "_T_1092":
            edge["statement_ids"] = sorted(set(edge["statement_ids"]) | {900001})
        if edge.get("src") == "_T_1150":
            edge["statement_ids"] = sorted(set(edge["statement_ids"]) | {900002})
    return result


class RegisterTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((RUN_DIR / "task.json").read_text(encoding="utf-8"))
        cls.raw_handoff = json.loads(
            (RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        cls.handoff = _with_state_writer_controls(cls.raw_handoff)

    def test_ast_schema_compiler_and_grounding(self):
        formal = _formal()
        self.assertEqual(validate_formal_axiom_shape(formal), [])
        compiled = compile_formal_axiom(formal)
        self.assertEqual(compiled["checker"], "register_transition")
        self.assertEqual(compiled["kind"], "state_transition")
        candidate = _candidate(self.task, self.handoff)
        self.assertEqual(
            parse_candidate_response(json.dumps(candidate))["axioms"][0]["formal"],
            formal,
        )
        grounding = validate_candidate_grounding(candidate, self.task, self.handoff)
        self.assertTrue(grounding["valid"], grounding)

    def test_real_ldq_tail_complete_transition_is_formally_proved(self):
        result = run_semantic_validation(
            _candidate(self.task, self.handoff),
            self.handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]
        self.assertEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)
        self.assertEqual(
            axiom["formal"]["proof_method"],
            "exact-guard-partitioned-register-transition",
        )
        # Full Cartesian enumeration was 2^11=2048 rows.  Partitioned exact
        # enumeration checks the 4-bit redirect value only when its branch is
        # selected, reducing this to 608 without changing semantics.
        self.assertEqual(axiom["formal"]["certificate"]["checked_rows"], 608)

    def test_wrong_writer_priority_is_refuted(self):
        candidate = _candidate(self.task, self.handoff)
        updates = candidate["axioms"][0]["formal"]["updates"]
        updates[0], updates[1] = updates[1], updates[0]
        result = run_semantic_validation(
            candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(result["results"][0]["validation_level"], REFUTED)

    def test_missing_writer_control_context_fails_closed(self):
        result = run_semantic_validation(
            _candidate(self.task, self.raw_handoff),
            self.raw_handoff,
            formal_backend="explicit-control",
        )
        self.assertNotEqual(result["results"][0]["validation_level"], FORMALLY_PROVED)


if __name__ == "__main__":
    unittest.main()
