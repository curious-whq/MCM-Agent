from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from workflow.research_memory import (
    build_current_handoff,
    initialize_experience,
    write_run_summary,
)


class WorkflowMemoryTests(unittest.TestCase):
    def _write_json(self, path: Path, value):
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def _fake_run(self, root: Path) -> Path:
        run = root / "leaf_abstraction-ProbeUnit-test"
        run.mkdir(parents=True)
        self._write_json(
            run / "task.json",
            {
                "task_id": "leaf_abstraction-ProbeUnit-test",
                "kind": "leaf_abstraction",
                "work_unit_id": "ProbeUnit",
                "workflow_version": "manual-first-workflow-0.5",
                "prompt_version": "leaf-abstraction-prompt-0.2",
                "schema_version": "umcm-experimental-0.2",
            },
        )
        self._write_json(
            run / "status.json",
            {
                "status": "PARTIALLY_FORMALLY_VALIDATED",
                "candidate_axiom_count": 2,
                "trusted_axiom_count": 1,
                "next_action": "Prove A2 or keep it outside the trusted µMCM.",
            },
        )
        self._write_json(run / "validation.json", {"valid": True, "errors": [], "warnings": []})
        self._write_json(
            run / "response_parsed.json",
            {
                "schema_version": "umcm-experimental-0.2",
                "work_unit_id": "ProbeUnit",
                "occurrences": [{"id": "Req"}],
                "predicates": [],
                "identity_keys": [{"id": "Txn"}],
                "cases": [{"id": "C0"}],
                "axioms": [
                    {"id": "A1", "formal": {"type": "forbid_when", "occurrence": "Req", "predicate": "Active", "scope_identity": None}},
                    {"id": "A2", "formal": {"type": "identity_flow", "identity": "Txn", "capture": {"on": "Req", "source": "io.req.bits", "carrier": "req"}, "projections": [{"on": "Req", "target": "io.req.bits.address", "expr": {"op": "signal", "name": "req.address"}}]}},
                ],
                "unresolved": [{"id": "U1", "question": "Need bit-level identity proof"}],
            },
        )
        self._write_json(
            run / "semantic_validation.json",
            {
                "counts": {"FORMALLY_PROVED": 1, "STRUCTURALLY_SUPPORTED": 1, "REFUTED": 0},
                "trusted_axiom_count": 1,
                "formal_backend": {"name": "explicit-control"},
                "results": [
                    {"axiom_id": "A1", "validation_level": "FORMALLY_PROVED"},
                    {"axiom_id": "A2", "validation_level": "STRUCTURALLY_SUPPORTED"},
                ],
            },
        )
        self._write_json(
            run / "trusted_umcm.json",
            {
                "axioms": [{"id": "A1"}],
                "provenance": {
                    "A1": {
                        "kind": "lifted",
                        "source_axioms": ["Child::CA1"],
                        "proof_method": "trusted-child-lift",
                    }
                },
            },
        )
        return run

    def test_run_summary_preserves_validation_and_unresolved(self):
        with tempfile.TemporaryDirectory() as td:
            run = self._fake_run(Path(td))
            path = write_run_summary(run)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Run Summary — ProbeUnit", text)
            self.assertIn("`A1` [FORMALLY_PROVED]", text)
            self.assertIn("`A2` [STRUCTURALLY_SUPPORTED]", text)
            self.assertIn("Need bit-level identity proof", text)
            self.assertIn("Certified provenance", text)
            self.assertIn("`Child::CA1`", text)
            self.assertTrue((run / "EXPERIENCE.md").exists())

    def test_experience_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            path = initialize_experience(run)
            path.write_text("# kept lesson\n", encoding="utf-8")
            initialize_experience(run)
            self.assertEqual(path.read_text(encoding="utf-8"), "# kept lesson\n")

    def test_handoff_is_self_contained_and_includes_run(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            run_root = Path(td)
            self._fake_run(run_root)
            text = build_current_handoff(repo, run_roots=[run_root])
            self.assertIn("Resume instruction for a new conversation", text)
            self.assertIn("D007 — Candidate is not trusted", text)
            self.assertIn("Run Summary — ProbeUnit", text)
            self.assertIn("FORMALLY_PROVED", text)
            self.assertIn("New-conversation operating rule", text)

    def test_research_memory_files_exist(self):
        repo = Path(__file__).resolve().parents[1]
        for name in ("GOAL.md", "METHOD.md", "DECISIONS.md", "LESSONS.md", "ROADMAP_3W.md", "STATUS.md"):
            self.assertTrue((repo / "docs" / "research" / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
