from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.axiom_ir import (
    compile_formal_axiom,
    render_formal_axiom,
    validate_formal_axiom_shape,
)
from workflow.manual import validate_candidate_grounding
from workflow.priority_select_prover import (
    STRUCTURALLY_SUPPORTED,
    _selected_index,
    prove_indexed_priority_select,
)
from workflow.schema import UMCM_SCHEMA_VERSION, parse_candidate_response
from workflow.semantic import (
    FORMALLY_PROVED,
    REFUTED,
    HandoffControlModel,
    run_semantic_validation,
)


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-LSU.logic-e41a1cc2550d9194"
)
STQ_CLEAR_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-LSU-state-0-10-75fa875f7278b61a"
)


def _formal() -> dict:
    return {
        "type": "indexed_priority_select",
        "index": {"name": "i", "count": 8},
        "candidate": {
            "op": "bit",
            "value": {"op": "signal", "name": "io.matches"},
            "index": {"op": "index_var", "name": "i"},
        },
        "priority": {
            "kind": "cyclic_predecessor",
            "pivot": {"op": "signal", "name": "io.youngest"},
        },
        "result": {"found": "io.found", "index": "io.found_idx"},
        "latency_cycles": 1,
        "initialization": {"kind": "implicit_unconstrained"},
        "scope_identity": None,
    }


def _candidate(task: dict) -> dict:
    return {
        "schema_version": UMCM_SCHEMA_VERSION,
        "task_id": task["task_id"],
        "work_unit_id": task["work_unit_id"],
        "occurrences": [],
        "predicates": [],
        "identity_keys": [],
        "cases": [],
        "axioms": [{
            "id": "A1",
            "formal": _formal(),
            "derived_from_case_ids": [],
            "evidence_statement_ids": list(range(3, 117)),
            "status": "candidate",
        }],
        "assumptions": [],
        "unresolved": [],
        "rationale": [
            "The leaf is a registered finite cyclic-priority selector and has no physical boundary event."
        ],
        "extensions": {},
    }


class IndexedPrioritySelectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads((RUN_DIR / "task.json").read_text(encoding="utf-8"))
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))

    def test_ast_compiles_renders_and_binds_all_signals(self):
        formal = _formal()
        self.assertEqual(validate_formal_axiom_shape(formal), [])
        compiled = compile_formal_axiom(formal)

        self.assertEqual(compiled["checker"], "indexed_priority_select")
        self.assertEqual(compiled["kind"], "selection")
        self.assertEqual(
            compiled["references"]["signals"],
            ["io.found", "io.found_idx", "io.matches", "io.youngest"],
        )
        self.assertIn("select_cyclic_predecessor", render_formal_axiom(formal))

    def test_candidate_schema_accepts_indexed_bit_expression(self):
        candidate = _candidate(self.task)
        parsed = parse_candidate_response(json.dumps(candidate))
        self.assertEqual(parsed["axioms"][0]["formal"], _formal())

    def test_value_constraint_keeps_literal_bit_index_contract(self):
        formal = {
            "type": "value_constraint",
            "on": None,
            "expr": {
                "op": "bit",
                "value": {"op": "signal", "name": "io.matches"},
                "index": {"op": "index_var", "name": "i"},
            },
            "relation": "eq",
            "value": 1,
            "scope_identity": None,
        }
        self.assertTrue(validate_formal_axiom_shape(formal))

    def test_shape_rejects_unbound_candidate_index_and_wrong_priority_fields(self):
        unbound = copy.deepcopy(_formal())
        unbound["candidate"]["index"]["name"] = "j"
        linear_with_pivot = copy.deepcopy(_formal())
        linear_with_pivot["priority"]["kind"] = "linear_max"

        self.assertTrue(validate_formal_axiom_shape(unbound))
        self.assertTrue(validate_formal_axiom_shape(linear_with_pivot))

    def test_priority_orders_have_strict_pivot_and_wrap_semantics(self):
        candidates = [1, 3, 6]
        self.assertEqual(_selected_index(candidates, "linear_min", None), 1)
        self.assertEqual(_selected_index(candidates, "linear_max", None), 6)
        self.assertEqual(_selected_index(candidates, "cyclic_predecessor", 5), 3)
        self.assertEqual(_selected_index(candidates, "cyclic_predecessor", 1), 6)
        self.assertEqual(_selected_index(candidates, "cyclic_successor", 3), 6)
        self.assertEqual(_selected_index(candidates, "cyclic_successor", 6), 1)

    def test_priority_orders_can_include_pivot_first(self):
        candidates = [1, 3, 6]
        self.assertEqual(
            _selected_index(
                candidates, "cyclic_successor", 3, pivot_position="first"
            ),
            3,
        )
        self.assertEqual(
            _selected_index(
                candidates, "cyclic_predecessor", 3, pivot_position="first"
            ),
            3,
        )

    def test_indexed_boolean_candidate_and_index_only_result_are_proved(self):
        def statement(statement_id, kind, text, drives=()):
            return {
                "id": statement_id,
                "kind": kind,
                "text": text,
                "drives": list(drives),
                "reads": [],
                "control_reads": [],
            }

        handoff = {
            "state": [
                {"id": "valid", "type": "UInt<1>[2]"},
                {"id": "cleared", "type": "UInt<1>[2]"},
                {"id": "result_idx", "type": "UInt<1>"},
            ],
            "frontier": [{"id": "pivot", "type": "UInt<1>"}],
            "dependency_edges": [],
            "statements": [
                statement(0, "reg", "reg result_idx : UInt<1>, clock", ("result_idx",)),
                statement(11, "input", "input pivot : UInt<1>", ("pivot",)),
                statement(1, "node", "node nc0 = not(cleared[0])", ("nc0",)),
                statement(2, "node", "node c0 = and(valid[0], nc0)", ("c0",)),
                statement(3, "node", "node nc1 = not(cleared[1])", ("nc1",)),
                statement(4, "node", "node c1 = and(valid[1], nc1)", ("c1",)),
                statement(5, "node", "node tail0 = mux(c1, UInt<1>(0h1), UInt<1>(0h0))", ("tail0",)),
                statement(6, "node", "node sel0 = mux(c0, UInt<1>(0h0), tail0)", ("sel0",)),
                statement(7, "node", "node tail1 = mux(c0, UInt<1>(0h0), UInt<1>(0h0))", ("tail1",)),
                statement(8, "node", "node sel1 = mux(c1, UInt<1>(0h1), tail1)", ("sel1",)),
                statement(9, "node", "node selected = mux(pivot, sel1, sel0)", ("selected",)),
                statement(10, "connect", "connect result_idx, selected", ("result_idx",)),
            ],
        }
        formal = {
            "type": "indexed_priority_select",
            "index": {"name": "i", "count": 2},
            "candidate": {
                "op": "and",
                "args": [
                    {
                        "op": "lookup",
                        "value": {"op": "signal", "name": "valid"},
                        "index": {"op": "index_var", "name": "i"},
                    },
                    {
                        "op": "not",
                        "value": {
                            "op": "lookup",
                            "value": {"op": "signal", "name": "cleared"},
                            "index": {"op": "index_var", "name": "i"},
                        },
                    },
                ],
            },
            "priority": {
                "kind": "cyclic_successor",
                "pivot": {"op": "signal", "name": "pivot"},
                "pivot_position": "first",
            },
            "result": {"index": "result_idx"},
            "latency_cycles": 1,
            "initialization": {"kind": "implicit_unconstrained"},
            "scope_identity": None,
        }
        self.assertEqual(validate_formal_axiom_shape(formal), [])
        compiled = compile_formal_axiom(formal)
        payload = _candidate(self.task)
        payload["axioms"][0]["formal"] = formal
        self.assertEqual(
            parse_candidate_response(json.dumps(payload))["axioms"][0]["formal"],
            formal,
        )
        self.assertEqual(
            compiled["references"]["signals"],
            ["cleared", "pivot", "result_idx", "valid"],
        )
        proof = prove_indexed_priority_select(
            HandoffControlModel(handoff), {}, **compiled["arguments"]
        )
        self.assertEqual(proof["status"], STRUCTURALLY_SUPPORTED, proof)
        self.assertEqual(proof["checked_rows"], 32)

    def test_real_forwarding_age_logic_is_grounded_and_formally_proved(self):
        candidate = _candidate(self.task)
        grounding = validate_candidate_grounding(candidate, self.task, self.handoff)
        self.assertTrue(grounding["valid"], grounding)

        result = run_semantic_validation(
            candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]
        self.assertEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)
        self.assertEqual(
            axiom["formal"]["proof_method"],
            "exact-registered-indexed-priority-select",
        )
        self.assertEqual(axiom["formal"]["certificate"]["checked_rows"], 2048)

    def test_real_stq_clear_selector_supports_scalar_frontier_and_index_projection(self):
        task = json.loads((STQ_CLEAR_RUN_DIR / "task.json").read_text(encoding="utf-8"))
        handoff = json.loads(
            (STQ_CLEAR_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        candidate_signals = [
            f"_stq_clr_head_idx_T_{2 * entry + 1}" for entry in range(8)
        ]
        for frontier in handoff["frontier"]:
            if frontier["id"] == "stq_clr_head_idx_head_base":
                frontier["type"] = "UInt<3>"
        formal = {
            "type": "indexed_priority_select",
            "index": {"name": "i", "count": 8},
            "candidate": {
                "op": "indexed_cases",
                "index": {"op": "index_var", "name": "i"},
                "values": [
                    {"op": "signal", "name": signal}
                    for signal in candidate_signals
                ],
            },
            "priority": {
                "kind": "cyclic_successor",
                "pivot": {
                    "op": "signal",
                    "name": "stq_clr_head_idx_head_base",
                },
                "pivot_position": "first",
            },
            "result": {
                "index": {
                    "op": "slice",
                    "value": {"op": "signal", "name": "stq_clr_head_idx"},
                    "hi": 2,
                    "lo": 0,
                }
            },
            "latency_cycles": 1,
            "initialization": {"kind": "implicit_unconstrained"},
            "scope_identity": None,
        }
        candidate = _candidate(task)
        candidate["axioms"][0]["formal"] = formal
        candidate["axioms"][0]["evidence_statement_ids"] = list(
            handoff["grounding"]["allowed_statement_ids"]
        )
        self.assertEqual(
            parse_candidate_response(json.dumps(candidate))["axioms"][0]["formal"],
            formal,
        )
        grounding = validate_candidate_grounding(candidate, task, handoff)
        self.assertTrue(grounding["valid"], grounding)

        result = run_semantic_validation(
            candidate,
            handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]
        self.assertEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)
        self.assertEqual(axiom["formal"]["certificate"]["checked_rows"], 2048)

        wrong = copy.deepcopy(candidate)
        wrong["axioms"][0]["formal"]["priority"]["pivot_position"] = "last"
        wrong_result = run_semantic_validation(
            wrong,
            handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(
            wrong_result["results"][0]["validation_level"],
            REFUTED,
            wrong_result["results"][0],
        )

    def test_wrong_priority_writer_produces_a_concrete_counterexample(self):
        handoff = copy.deepcopy(self.handoff)
        writer = next(item for item in handoff["statements"] if item["id"] == 112)
        writer["text"] = "connect found_idx, UInt<3>(0h5)"

        result = run_semantic_validation(
            _candidate(self.task),
            handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]
        self.assertEqual(axiom["validation_level"], REFUTED, axiom)
        self.assertIsNotNone(axiom["formal"].get("counterexample"))

    def test_unreset_initialization_claim_fails_closed_for_reset_registers(self):
        handoff = copy.deepcopy(self.handoff)
        declaration = next(item for item in handoff["statements"] if item["id"] == 47)
        declaration["kind"] = "regreset"

        result = run_semantic_validation(
            _candidate(self.task),
            handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]
        self.assertNotEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)


if __name__ == "__main__":
    unittest.main()
