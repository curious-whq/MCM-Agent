from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from frontend.pipeline import StaticFrontend
from frontend.workunit import build_hierarchical_work_unit
from workflow.handoff import build_work_unit_static_handoff
from workflow.manual import (
    GROUNDING_VALID,
    REFINEMENT_NEEDED,
    _is_allowed_signal_reference,
    export_manual_task,
    import_manual_response,
)
from workflow.schema import UMCM_SCHEMA_VERSION, parse_candidate_response
from workflow.tasks import build_leaf_abstraction_task


FIXTURE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"


class ManualWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = FIXTURE.read_text(encoding="utf-8")
        cls.frontend = StaticFrontend.from_firrtl(cls.text)
        cls.unit = build_hierarchical_work_unit(
            cls.frontend.design,
            cls.frontend.graph,
            cls.frontend.registries,
            root_module="BoomProbeUnit",
        )
        cls.handoff = build_work_unit_static_handoff(
            cls.unit,
            cls.frontend.graph("BoomProbeUnit"),
            cls.frontend.registries["BoomProbeUnit"],
        )
        cls.package = build_leaf_abstraction_task(cls.handoff)

    def _candidate(self):
        event_id = self.handoff["events"][0]["id"]
        statement_id = self.handoff["statements"][0]["id"]
        state_id = self.handoff["state"][0]["id"]
        return {
            "schema_version": UMCM_SCHEMA_VERSION,
            "task_id": self.package.task.task_id,
            "work_unit_id": self.unit.id,
            "occurrences": [
                {
                    "id": "E0",
                    "kind": "boundary",
                    "physical_event_ids": [event_id],
                    "definition": "physical boundary fire",
                    "multiplicity": "unspecified",
                    "grounding": {
                        "state_register": None,
                        "state_values": [],
                        "signals_true": [],
                        "signals_false": [],
                    },
                    "evidence_statement_ids": [statement_id],
                },
                {
                    "id": "D0",
                    "kind": "derived",
                    "physical_event_ids": [],
                    "definition": "state milestone",
                    "multiplicity": "at_most_once",
                    "grounding": {
                        "state_register": "state",
                        "state_values": [8],
                        "signals_true": ["io.wb_req.ready"],
                        "signals_false": [],
                    },
                    "evidence_statement_ids": [44, 45, 46],
                },
            ],
            "predicates": [
                {
                    "id": "P0",
                    "definition": "active control states",
                    "grounding": {
                        "source_signal": None,
                        "negated": False,
                        "state_register": "state",
                        "state_values": list(range(1, 11)),
                    },
                    "evidence_statement_ids": [statement_id],
                }
            ],
            "identity_keys": [
                {
                    "id": "I0",
                    "carrier_state": state_id,
                    "fields": [],
                    "description": "test identity",
                    "evidence_statement_ids": [statement_id],
                }
            ],
            "cases": [
                {
                    "id": "C0",
                    "trigger_occurrences": ["E0"],
                    "guard_predicates": [{"id": "P0", "positive": False}],
                    "emits": [],
                    "relations": [],
                    "evidence_statement_ids": [statement_id],
                    "confidence": "medium",
                }
            ],
            "axioms": [
                {
                    "id": "A0",
                    "formal": {
                        "type": "forbid_when",
                        "occurrence": "E0",
                        "predicate": "P0",
                        "scope_identity": None,
                    },
                    "derived_from_case_ids": ["C0"],
                    "evidence_statement_ids": [statement_id],
                    "status": "candidate",
                }
            ],
            "assumptions": [],
            "unresolved": [],
            "rationale": ["test candidate"],
            "extensions": {},
        }

    def test_workunit_handoff_is_self_contained_and_grounded(self):
        self.assertTrue(self.handoff["work_unit"]["is_leaf"])
        self.assertTrue(self.handoff["work_unit"]["coverage_complete"])
        self.assertEqual(
            {event["id"] for event in self.handoff["events"]},
            set(self.unit.local_event_ids),
        )
        self.assertTrue(self.handoff["events"])
        self.assertTrue(self.handoff["statements"])
        self.assertEqual(
            self.handoff["grounding"]["allowed_statement_ids"],
            sorted(self.unit.local_statement_ids),
        )

    def test_prompt_contains_formal_axiom_language(self):
        prompt = self.package.prompt
        self.assertIn("Grounded FIRRTL statement ledger", prompt)
        self.assertIn("A derived", prompt)
        self.assertIn("Persistent predicates", prompt)
        self.assertIn("formal AST is the only semantic source", prompt)
        self.assertIn("FINAL MCM-AGENT RESULT", prompt)
        self.assertIn(UMCM_SCHEMA_VERSION, prompt)
        self.assertIn('"relation":"same_cycle_exactly_one"', prompt)
        self.assertIn("The `relation` field is required", prompt)

    def test_prompt_requires_autonomous_completion_or_language_gap(self):
        prompt = self.package.prompt
        self.assertIn("Analyze the entire WorkUnit autonomously", prompt)
        self.assertIn("do **not** ask the human to choose", prompt)
        self.assertIn("MCM-AGENT LANGUAGE GAP", prompt)
        self.assertIn("prover capability is decided later by `semantic-validate`", prompt)
        self.assertIn("safer over-approximation", prompt)
        self.assertNotIn("We may discuss, challenge, and revise it interactively", prompt)
        self.assertNotIn("Only when the discussion has converged", prompt)

    def test_manual_export_and_import_grounded_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = export_manual_task(self.package, tmp)
            candidate = self._candidate()
            response = (
                "Some discussion first.\n\nFINAL MCM-AGENT RESULT\n```json\n"
                + json.dumps(candidate, indent=2)
                + "\n```\n"
            )
            result = import_manual_response(task_dir, response)
            self.assertEqual(result.status, GROUNDING_VALID)
            self.assertTrue(result.validation["valid"])


    def test_manual_import_rejects_legacy_formula_or_validation_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = export_manual_task(self.package, tmp)
            candidate = self._candidate()
            candidate["axioms"][0]["formula"] = "P0 => !E0"
            candidate["axioms"][0]["validation"] = {"checker": "forbid_when"}
            result = import_manual_response(task_dir, json.dumps(candidate))
            self.assertFalse(result.validation["valid"])
            self.assertTrue(any("unsupported legacy/extra field 'formula'" in e for e in result.validation["errors"]))
            self.assertTrue(any("unsupported legacy/extra field 'validation'" in e for e in result.validation["errors"]))

    def test_manual_import_rejects_out_of_scope_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = export_manual_task(self.package, tmp)
            candidate = self._candidate()
            candidate["axioms"][0]["evidence_statement_ids"] = [999999]
            result = import_manual_response(task_dir, json.dumps(candidate))
            self.assertEqual(result.status, REFINEMENT_NEEDED)
            self.assertFalse(result.validation["valid"])
            self.assertTrue(any("outside this WorkUnit" in e for e in result.validation["errors"]))

    def test_derived_occurrence_requires_machine_grounding(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = export_manual_task(self.package, tmp)
            candidate = self._candidate()
            candidate["occurrences"][1]["grounding"] = {
                "state_register": "state",
                "state_values": [],
                "signals_true": [],
                "signals_false": [],
            }
            result = import_manual_response(task_dir, json.dumps(candidate))
            self.assertFalse(result.validation["valid"])
            self.assertTrue(any("needs concrete" in e for e in result.validation["errors"]))

    def test_response_parser_uses_last_fenced_json(self):
        candidate = self._candidate()
        response = (
            "```json\n{\"example\": true}\n```\n"
            "FINAL MCM-AGENT RESULT\n```json\n"
            + json.dumps(candidate)
            + "\n```"
        )
        parsed = parse_candidate_response(response)
        self.assertEqual(parsed["task_id"], self.package.task.task_id)

    def test_dynamic_array_signal_requires_grounded_wildcard_and_index(self):
        allowed = {"valids[*]", "deq_ptr_value", "valids[0]"}

        self.assertTrue(
            _is_allowed_signal_reference("valids[deq_ptr_value]", allowed)
        )
        self.assertFalse(
            _is_allowed_signal_reference("valids[unknown_ptr]", allowed)
        )
        self.assertFalse(
            _is_allowed_signal_reference("other[deq_ptr_value]", allowed)
        )


if __name__ == "__main__":
    unittest.main()
