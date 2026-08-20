from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from workflow.composition import (
    _canonical_sha256,
    attach_frozen_child_summaries,
    instantiate_frozen_umcm,
    work_unit_implementation_sha256,
)
from workflow.manual import GROUNDING_VALID, export_manual_task, import_manual_response
from workflow.schema import UMCM_SCHEMA_VERSION
from workflow.semantic import freeze_task_dir, validate_task_dir
from workflow.tasks import build_parent_synthesis_task


def _write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _complexity(statements: int = 1):
    return {
        "raw": {
            "source_loc": statements,
            "unmapped_firrtl_loc": statements,
            "signals": 1,
            "dependency_edges": 0,
            "statements": statements,
        },
        "logical": {
            "source_loc": statements,
            "signals": 1,
            "dependency_edges": 0,
            "statements": statements,
        },
        "registers": 1,
        "memories": 0,
        "events": 0,
        "state_regions": 0,
        "event_state_coupling": 0.0,
    }


def _parent_handoff():
    return {
        "schema_version": "workunit-static-0.1",
        "planner_version": "hierarchical-planner-v10",
        "work_unit": {
            "id": "Parent",
            "kind": "module",
            "module": "ParentModule",
            "instance_path": "Parent",
            "depth": 0,
            "decision": "partitioned",
            "coverage_complete": True,
            "is_leaf": False,
            "exceeded_limits": [],
            "replacement_exceeded_limits": [],
        },
        "complexity": _complexity(),
        "replacement_complexity": _complexity(),
        "events": [],
        "state": [
            {
                "id": "state",
                "kind": "register",
                "type": "UInt<1>",
                "source": None,
            }
        ],
        "memory_state": [],
        "frontier": [],
        "parent_connection_signals": [],
        "children": [
            {
                "child_id": "Parent.child",
                "child_kind": "module",
                "summary_ref": "umcm://Parent.child",
                "boundary_events": ["Parent.child::io.out.fire"],
                "frontier_signals": ["child.io.out.valid"],
            }
        ],
        "statements": [
            {
                "id": 0,
                "firrtl_line": 1,
                "kind": "regreset",
                "text": "regreset state : UInt<1>, clock, reset, UInt<1>(0h0)",
                "source": None,
                "status": "supported",
                "drives": ["state"],
                "reads": [],
                "control_reads": [],
                "note": None,
            }
        ],
        "dependency_edges": [],
        "semantic_event_cones": [],
        "source_spans": [],
        "source_evidence": {"roots": [], "resolved": [], "unresolved": []},
        "grounding": {
            "allowed_statement_ids": [0],
            "allowed_physical_event_ids": [],
            "allowed_state_ids": ["state"],
            "semantic_labels": [],
        },
    }


def _frozen_child():
    return {
        "schema_version": UMCM_SCHEMA_VERSION,
        "task_id": "child-task",
        "work_unit_id": "Parent.child",
        "trust_policy": "formal-ast-only-v0.2",
        "trusted_axiom_ids": ["CA1"],
        "occurrences": [
            {
                "id": "ChildOut",
                "kind": "boundary",
                "physical_event_ids": ["Parent.child::io.out.fire"],
                "definition": "child output handshake",
                "multiplicity": "repeatable",
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
                "evidence_statement_ids": [7],
            }
        ],
        "predicates": [
            {
                "id": "ChildActive",
                "definition": "trusted child predicate",
                "grounding": {
                    "source_signal": "child_internal_active",
                    "negated": False,
                    "state_register": None,
                    "state_values": [],
                },
                "evidence_statement_ids": [8],
            }
        ],
        "identity_keys": [],
        "cases": [],
        "axioms": [
            {
                "id": "CA1",
                "formal": {
                    "type": "forbid_when",
                    "occurrence": "ChildOut",
                    "predicate": "ChildActive",
                    "scope_identity": None,
                },
                "derived_from_case_ids": [],
                "evidence_statement_ids": [7, 8],
                "status": "candidate",
                "rendered_formula": "ChildActive => !ChildOut",
            }
        ],
        "assumptions": [],
        "freeze": {
            "status": "FROZEN_FOR_COMPOSITION",
            "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
            "candidate_axiom_count": 1,
            "trusted_axiom_count": 1,
            "reopen_policy": "CEGAR",
        },
    }


def _module_template_handoff(instance_path: str = "ChildModule"):
    return {
        "schema_version": "workunit-static-0.1",
        "planner_version": "hierarchical-planner-v11",
        "work_unit": {
            "id": instance_path,
            "kind": "module",
            "module": "ChildModule",
            "instance_path": instance_path,
            "is_leaf": True,
        },
        "statements": [{
            "id": 7,
            "kind": "connect",
            "text": "connect io.out.valid, child_internal_active",
            "status": "supported",
            "drives": ["io.out.valid"],
            "reads": ["child_internal_active"],
            "control_reads": [],
            "note": None,
        }],
        "dependency_edges": [{
            "src": "child_internal_active",
            "dst": "io.out.valid",
            "kind": "data",
            "statement_ids": [7],
        }],
        "state": [],
        "memory_state": [],
        "frontier": [],
        "events": [{
            "id": f"{instance_path}::io.out.fire",
            "registry_id": "ChildModule.io.out.fire",
            "channel": "io.out",
            "direction": "send",
            "protocol": "decoupled",
            "predicate": "io.out.valid && io.out.ready",
            "valid": "io.out.valid",
            "ready": "io.out.ready",
            "payload": [],
        }],
        "children": [],
        "semantic_event_cones": [],
    }


class ParentWorkflowTests(unittest.TestCase):
    def _child_run(self, root: Path) -> Path:
        task_dir = root / "leaf-child"
        task_dir.mkdir(parents=True)
        _write_json(
            task_dir / "task.json",
            {
                "task_id": "child-task",
                "kind": "leaf_abstraction",
                "work_unit_id": "Parent.child",
                "schema_version": UMCM_SCHEMA_VERSION,
                "prompt_version": "leaf-abstraction-prompt-0.6",
                "workflow_version": "manual-first-workflow-0.9",
                "provider_mode": "manual_conversation",
            },
        )
        _write_json(
            task_dir / "status.json",
            {"status": "FROZEN_FOR_COMPOSITION", "task_id": "child-task"},
        )
        _write_json(task_dir / "frozen_umcm.json", _frozen_child())
        return task_dir

    def _module_template_run(self, root: Path) -> Path:
        task_dir = root / "module-template"
        task_dir.mkdir(parents=True)
        frozen = _frozen_child()
        frozen["task_id"] = "child-module-template"
        frozen["work_unit_id"] = "ChildModule"
        frozen["occurrences"][0]["physical_event_ids"] = ["ChildModule::io.out.fire"]
        _write_json(
            task_dir / "task.json",
            {
                "task_id": "child-module-template",
                "kind": "leaf_abstraction",
                "work_unit_id": "ChildModule",
                "schema_version": UMCM_SCHEMA_VERSION,
                "prompt_version": "leaf-abstraction-prompt-0.9",
                "workflow_version": "manual-first-workflow-0.9",
                "provider_mode": "manual_conversation",
            },
        )
        _write_json(
            task_dir / "status.json",
            {"status": "FROZEN_FOR_COMPOSITION", "task_id": "child-module-template"},
        )
        _write_json(task_dir / "static_handoff.json", _module_template_handoff())
        _write_json(task_dir / "frozen_umcm.json", frozen)
        return task_dir

    def _parent_with_template_slot(self, child_id: str = "Parent.child"):
        handoff = _parent_handoff()
        slot = handoff["children"][0]
        slot["child_id"] = child_id
        slot["child_module"] = "ChildModule"
        slot["boundary_events"] = [f"{child_id}::io.out.fire"]
        slot["implementation_sha256"] = work_unit_implementation_sha256(
            _module_template_handoff(child_id)
        )
        slot["structural_implementation_sha256"] = "1" * 64
        handoff["implementation_catalog"] = {
            "ChildModule": {
                "proof_scope_sha256": work_unit_implementation_sha256(
                    _module_template_handoff("ChildModule")
                ),
                "structural_implementation_sha256": "1" * 64,
            }
        }
        return handoff

    def test_parent_prompt_consumes_frozen_child_without_child_rtl(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child_dir = self._child_run(root)
            handoff = attach_frozen_child_summaries(
                _parent_handoff(),
                run_roots=[root],
                child_task_dirs=[child_dir],
            )
            package = build_parent_synthesis_task(handoff)
            self.assertEqual(package.task.kind.value, "parent_synthesis")
            self.assertIn("Child RTL is **not an input**", package.prompt)
            self.assertIn("Parent.child::ChildOut", package.prompt)
            self.assertIn("Parent.child::CA1", package.prompt)
            self.assertEqual(
                handoff["grounding"]["imported_occurrence_ids"],
                ["Parent.child::ChildOut"],
            )
            self.assertEqual(
                handoff["grounding"]["imported_axiom_ids"],
                ["Parent.child::CA1"],
            )

    def test_parent_manual_import_accepts_qualified_child_semantic_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child_dir = self._child_run(root)
            handoff = attach_frozen_child_summaries(
                _parent_handoff(),
                run_roots=[root],
                child_task_dirs=[child_dir],
            )
            package = build_parent_synthesis_task(handoff)
            task_dir = export_manual_task(package, root / "out")
            candidate = {
                "schema_version": UMCM_SCHEMA_VERSION,
                "task_id": package.task.task_id,
                "work_unit_id": "Parent",
                "occurrences": [],
                "predicates": [],
                "identity_keys": [],
                "cases": [],
                "axioms": [
                    {
                        "id": "A1",
                        "formal": {
                            "type": "forbid_when",
                            "occurrence": "Parent.child::ChildOut",
                            "predicate": "Parent.child::ChildActive",
                            "scope_identity": None,
                        },
                        "derived_from_case_ids": [],
                        "evidence_statement_ids": [],
                        "status": "candidate",
                    }
                ],
                "assumptions": [],
                "unresolved": [],
                "rationale": [],
                "extensions": {
                    "parent_synthesis": {
                        "axiom_provenance": {
                            "A1": {
                                "kind": "reexported",
                                "source_axioms": ["Parent.child::CA1"],
                                "note": "explicit re-export test",
                            }
                        }
                    }
                },
            }
            result = import_manual_response(task_dir, json.dumps(candidate))
            self.assertEqual(result.status, GROUNDING_VALID)
            self.assertTrue(result.validation["valid"])

    def test_zero_new_axiom_parent_freezes_and_retains_child_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child_dir = self._child_run(root)
            handoff = attach_frozen_child_summaries(
                _parent_handoff(),
                run_roots=[root],
                child_task_dirs=[child_dir],
            )
            package = build_parent_synthesis_task(handoff)
            task_dir = export_manual_task(package, root / "out")
            candidate = {
                "schema_version": UMCM_SCHEMA_VERSION,
                "task_id": package.task.task_id,
                "work_unit_id": "Parent",
                "occurrences": [],
                "predicates": [],
                "identity_keys": [],
                "cases": [],
                "axioms": [],
                "assumptions": [],
                "unresolved": [],
                "rationale": [
                    "No additional parent-local ordering constraint is required."
                ],
                "extensions": {
                    "parent_synthesis": {
                        "axiom_provenance": {}
                    }
                },
            }
            result = import_manual_response(task_dir, json.dumps(candidate))
            self.assertEqual(result.status, GROUNDING_VALID)
            semantic = validate_task_dir(task_dir, formal_backend="none")
            self.assertEqual(semantic["candidate_axiom_count"], 0)
            self.assertTrue(semantic["all_axioms_formally_proved"])

            frozen = freeze_task_dir(task_dir)
            self.assertEqual(
                frozen["freeze"]["status"],
                "FROZEN_FOR_COMPOSITION",
            )
            imports = frozen["composition"]["imports"]
            self.assertEqual(len(imports), 1)
            self.assertEqual(frozen["provenance"], {})
            self.assertEqual(imports[0]["child_id"], "Parent.child")
            self.assertIn(
                "Parent.child::ChildOut",
                frozen["composition"]["semantic_catalog"]["occurrences"],
            )

    def test_parent_resolution_is_fail_closed_on_ambiguous_frozen_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._child_run(root)
            second = root / "leaf-child-2"
            second.mkdir()
            for filename in ("task.json", "status.json", "frozen_umcm.json"):
                second.joinpath(filename).write_text(
                    first.joinpath(filename).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            with self.assertRaisesRegex(ValueError, "multiple frozen child"):
                attach_frozen_child_summaries(
                    _parent_handoff(),
                    run_roots=[root],
                )

    def test_module_template_fingerprint_is_instance_path_independent(self):
        self.assertEqual(
            work_unit_implementation_sha256(_module_template_handoff("ChildModule")),
            work_unit_implementation_sha256(_module_template_handoff("Parent.child")),
        )

    def test_module_template_is_instantiated_for_two_equivalent_child_slots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._module_template_run(root)
            handoff = self._parent_with_template_slot("Parent.child0")
            second = dict(handoff["children"][0])
            second["child_id"] = "Parent.child1"
            second["summary_ref"] = "umcm://Parent.child1"
            second["boundary_events"] = ["Parent.child1::io.out.fire"]
            handoff["children"].append(second)

            result = attach_frozen_child_summaries(handoff, run_roots=[root])
            summaries = result["composition"]["child_summaries"]

            self.assertEqual([item["child_id"] for item in summaries], ["Parent.child0", "Parent.child1"])
            self.assertEqual(
                summaries[0]["instance_reuse"]["kind"],
                "module-theorem-template-instantiation",
            )
            self.assertEqual(summaries[0]["frozen_umcm"]["work_unit_id"], "Parent.child0")
            self.assertEqual(
                summaries[0]["frozen_umcm"]["occurrences"][0]["physical_event_ids"],
                ["Parent.child0::io.out.fire"],
            )
            self.assertIn(
                "Parent.child0::ChildOut",
                result["grounding"]["imported_occurrence_ids"],
            )
            self.assertIn(
                "Parent.child1::ChildOut",
                result["grounding"]["imported_occurrence_ids"],
            )

    def test_module_template_reuse_rejects_implementation_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._module_template_run(root)
            handoff = self._parent_with_template_slot()
            handoff["children"][0]["structural_implementation_sha256"] = "0" * 64

            with self.assertRaisesRegex(ValueError, "no implementation-equivalent module theorem template"):
                attach_frozen_child_summaries(handoff, run_roots=[root])

    def test_template_instantiation_rewrites_and_rehashes_descendant_imports(self):
        descendant = {
            "work_unit_id": "ChildModule.inner",
            "occurrences": [{"id": "Done", "physical_event_ids": ["ChildModule.inner::io.out.fire"]}],
            "predicates": [],
            "identity_keys": [],
            "cases": [],
            "axioms": [],
            "trusted_axiom_ids": [],
            "freeze": {"status": "FROZEN_FOR_COMPOSITION"},
        }
        template = _frozen_child()
        template["work_unit_id"] = "ChildModule"
        template["composition"] = {
            "imports": [{
                "child_id": "ChildModule.inner",
                "frozen_umcm_sha256": _canonical_sha256(descendant),
                "frozen_umcm": descendant,
            }],
            "semantic_catalog": {
                "occurrences": {
                    "ChildModule.inner::Done": {
                        "work_unit_id": "ChildModule.inner",
                        "local_id": "Done",
                    }
                }
            },
        }

        instantiated = instantiate_frozen_umcm(
            template,
            source_work_unit_id="ChildModule",
            target_work_unit_id="Parent.child0",
        )
        imported = instantiated["composition"]["imports"][0]

        self.assertEqual(imported["child_id"], "Parent.child0.inner")
        self.assertEqual(imported["frozen_umcm"]["work_unit_id"], "Parent.child0.inner")
        self.assertEqual(
            imported["frozen_umcm_sha256"],
            _canonical_sha256(imported["frozen_umcm"]),
        )
        self.assertIn(
            "Parent.child0.inner::Done",
            instantiated["composition"]["semantic_catalog"]["occurrences"],
        )


if __name__ == "__main__":
    unittest.main()
