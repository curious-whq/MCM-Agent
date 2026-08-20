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
from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHRFile.meta_write_arb-37cf63871121acc7"
)
META_READ_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHRFile.meta_read_arb-e5228745004b6981"
)
MMIO_ALLOC_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e"
)


def _occurrence(semantic_id: str, physical_id: str, signals: list[str]) -> dict:
    return {
        "id": semantic_id,
        "kind": "boundary",
        "physical_event_ids": [physical_id],
        "definition": " && ".join(signals),
        "multiplicity": "repeatable",
        "grounding": {"signals_true": signals, "signals_false": []},
        "evidence_statement_ids": list(range(8, 16)),
    }


def _candidate() -> dict:
    occurrences = [
        _occurrence(
            "Input0Fire",
            "BoomMSHRFile.meta_write_arb::io.in[0].fire",
            ["io.in[0].valid", "io.in[0].ready"],
        ),
        _occurrence(
            "Input1Fire",
            "BoomMSHRFile.meta_write_arb::io.in[1].fire",
            ["io.in[1].valid", "io.in[1].ready"],
        ),
        _occurrence(
            "OutputFire",
            "BoomMSHRFile.meta_write_arb::io.out.fire",
            ["io.out.valid", "io.out.ready"],
        ),
    ]
    return {
        "schema_version": "umcm-formal-0.5",
        "task_id": "occurrence-partition-regression",
        "work_unit_id": "BoomMSHRFile.meta_write_arb",
        "occurrences": occurrences,
        "predicates": [],
        "identity_keys": [],
        "cases": [],
        "axioms": [{
            "id": "A1",
            "formal": {
                "type": "occurrence_partition",
                "whole": "OutputFire",
                "parts": ["Input0Fire", "Input1Fire"],
                "relation": "same_cycle_exactly_one",
                "scope_identity": None,
            },
            "derived_from_case_ids": [],
            "evidence_statement_ids": list(range(8, 16)),
            "status": "candidate",
        }],
        "assumptions": [],
        "unresolved": [],
        "rationale": [],
        "extensions": {},
    }


class OccurrencePartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))

    def test_ast_compiles_and_renders_one_hot_same_cycle_semantics(self):
        formal = _candidate()["axioms"][0]["formal"]
        compiled = compile_formal_axiom(formal)

        self.assertEqual(compiled["checker"], "occurrence_partition")
        self.assertEqual(compiled["kind"], "conservation")
        self.assertEqual(
            compiled["references"]["occurrences"],
            ["Input0Fire", "Input1Fire", "OutputFire"],
        )
        self.assertEqual(
            render_formal_axiom(formal),
            "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
        )

    def test_shape_rejects_parity_like_or_degenerate_partitions(self):
        formal = _candidate()["axioms"][0]["formal"]

        wrong_relation = {**formal, "relation": "same_cycle_xor"}
        duplicate_parts = {**formal, "parts": ["Input0Fire", "Input0Fire"]}
        recursive_whole = {**formal, "parts": ["OutputFire", "Input0Fire"]}
        unproved_identity_scope = {**formal, "scope_identity": "Txn"}

        self.assertTrue(validate_formal_axiom_shape(wrong_relation))
        self.assertTrue(validate_formal_axiom_shape(duplicate_parts))
        self.assertTrue(validate_formal_axiom_shape(recursive_whole))
        self.assertTrue(validate_formal_axiom_shape(unproved_identity_scope))

    def test_singleton_partition_is_valid_same_cycle_equivalence(self):
        formal = {
            "type": "occurrence_partition",
            "whole": "OutputFire",
            "parts": ["InputFire"],
            "relation": "same_cycle_exactly_one",
            "scope_identity": None,
        }

        self.assertEqual(validate_formal_axiom_shape(formal), [])
        self.assertEqual(
            render_formal_axiom(formal),
            "OutputFire <=> exactly_one_same_cycle({InputFire})",
        )

    def test_real_priority_arbiter_partition_is_formally_proved(self):
        result = run_semantic_validation(
            _candidate(),
            self.handoff,
            formal_backend="explicit-control",
        )
        axiom = result["results"][0]

        self.assertEqual(axiom["validation_level"], FORMALLY_PROVED, axiom)
        self.assertEqual(
            axiom["formal"]["proof_method"],
            "exact-same-cycle-occurrence-partition",
        )
        self.assertEqual(
            axiom["formal"]["certificate"]["mutex_pairs"],
            [["Input0Fire", "Input1Fire"]],
        )

    def test_real_imported_candidate_is_grounded_and_fully_proved(self):
        task = json.loads((RUN_DIR / "task.json").read_text(encoding="utf-8"))
        candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))
        grounding = validate_candidate_grounding(candidate, task, self.handoff)

        self.assertTrue(grounding["valid"], grounding)
        result = run_semantic_validation(
            candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(result["trusted_axiom_count"], 12, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(
            by_id["A1"]["formal"]["proof_method"],
            "exact-same-cycle-occurrence-partition",
        )
        for axiom_id in ("A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"):
            self.assertEqual(
                by_id[axiom_id]["formal"]["proof_method"],
                "exact-conditional-symbolic-driver-equality",
                by_id[axiom_id],
            )

    def test_conditional_payload_proof_rejects_wrong_selected_driver(self):
        handoff = copy.deepcopy(self.handoff)
        selected_input0 = next(statement for statement in handoff["statements"] if statement["id"] == 7)
        selected_input0["text"] = "connect io.out.bits, io.in[1].bits"
        selected_input0["reads"] = ["io.in[1].bits"]
        candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))

        result = run_semantic_validation(
            candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertNotEqual(by_id["A3"]["validation_level"], FORMALLY_PROVED)
        self.assertIn("not equal", by_id["A3"]["formal"]["reason"])

    def test_partition_fails_if_output_can_drop_an_input_occurrence(self):
        handoff = copy.deepcopy(self.handoff)
        output_valid = next(statement for statement in handoff["statements"] if statement["id"] == 15)
        output_valid["text"] = "connect io.out.valid, UInt<1>(0h0)"
        output_valid["reads"] = ["h0"]

        result = run_semantic_validation(
            _candidate(),
            handoff,
            formal_backend="explicit-control",
        )["results"][0]

        self.assertNotEqual(result["validation_level"], FORMALLY_PROVED)
        self.assertEqual(
            result["formal"]["certificate"]["failed_obligation"],
            "part_without_whole",
        )

    def test_boundary_partition_ignores_llm_authored_signal_redefinition(self):
        candidate = _candidate()
        output = next(item for item in candidate["occurrences"] if item["id"] == "OutputFire")
        output["grounding"] = {
            "signals_true": ["io.in[0].valid", "io.in[0].ready"],
            "signals_false": [],
        }
        handoff = copy.deepcopy(self.handoff)
        output_valid = next(statement for statement in handoff["statements"] if statement["id"] == 15)
        output_valid["text"] = "connect io.out.valid, UInt<1>(0h0)"
        output_valid["reads"] = ["h0"]

        result = run_semantic_validation(
            candidate,
            handoff,
            formal_backend="explicit-control",
        )["results"][0]

        self.assertNotEqual(result["validation_level"], FORMALLY_PROVED)
        self.assertEqual(
            result["formal"]["certificate"]["failed_obligation"],
            "part_without_whole",
        )

    def test_partition_fails_if_two_parts_can_fire_together(self):
        handoff = copy.deepcopy(self.handoff)
        input1_ready = next(statement for statement in handoff["statements"] if statement["id"] == 11)
        input1_ready["text"] = "node _io_in_1_ready_T = and(UInt<1>(0h1), io.out.ready)"
        input1_ready["reads"] = ["h1", "io.out.ready"]

        result = run_semantic_validation(
            _candidate(),
            handoff,
            formal_backend="explicit-control",
        )["results"][0]

        self.assertNotEqual(result["validation_level"], FORMALLY_PROVED)
        self.assertEqual(
            result["formal"]["certificate"]["failed_obligation"],
            "parts_mutually_exclusive",
        )

    def test_real_meta_read_arbiter_candidate_is_fully_proved(self):
        handoff = json.loads(
            (META_READ_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        candidate = json.loads(
            (META_READ_RUN_DIR / "response_parsed.json").read_text(encoding="utf-8")
        )
        task = json.loads((META_READ_RUN_DIR / "task.json").read_text(encoding="utf-8"))

        grounding = validate_candidate_grounding(candidate, task, handoff)
        result = run_semantic_validation(
            candidate,
            handoff,
            formal_backend="explicit-control",
        )

        self.assertTrue(grounding["valid"], grounding)
        self.assertEqual(result["trusted_axiom_count"], 8, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)

    def test_real_single_input_mmio_alloc_arbiter_is_fully_proved(self):
        handoff = json.loads(
            (MMIO_ALLOC_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        candidate = json.loads(
            (MMIO_ALLOC_RUN_DIR / "response_parsed.json").read_text(encoding="utf-8")
        )
        task = json.loads((MMIO_ALLOC_RUN_DIR / "task.json").read_text(encoding="utf-8"))

        grounding = validate_candidate_grounding(candidate, task, handoff)
        result = run_semantic_validation(
            candidate,
            handoff,
            formal_backend="explicit-control",
        )

        self.assertTrue(grounding["valid"], grounding)
        self.assertEqual(result["trusted_axiom_count"], 2, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(
            by_id["A1"]["formal"]["certificate"]["mutex_pairs"],
            [],
        )


if __name__ == "__main__":
    unittest.main()
