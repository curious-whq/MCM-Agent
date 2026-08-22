from __future__ import annotations

import json
from pathlib import Path
import unittest

from workflow.schema import UMCM_SCHEMA_VERSION
from workflow.semantic import FORMALLY_PROVED, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "parent_synthesis-BoomNonBlockingDCache-59b0ae1731a92b08"
)


class DCacheParentCompositionRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        cls.candidate = {
            "schema_version": UMCM_SCHEMA_VERSION,
            "task_id": "cross-child-request-alias-regression",
            "work_unit_id": "BoomNonBlockingDCache",
            "occurrences": [],
            "predicates": [],
            "identity_keys": [],
            "cases": [],
            "axioms": [{
                "id": "A1",
                "formal": {
                    "type": "occurrence_partition",
                    "whole": "BoomNonBlockingDCache::region-0-3::MSHRReqFire",
                    "parts": ["BoomNonBlockingDCache.mshrs::RequestAccept"],
                    "relation": "same_cycle_exactly_one",
                    "scope_identity": None,
                },
                "derived_from_case_ids": [],
                "evidence_statement_ids": [2477],
                "status": "candidate",
            }],
            "assumptions": [],
            "unresolved": [],
            "rationale": [],
            "extensions": {"parent_synthesis": {"axiom_provenance": {
                "A1": {
                    "kind": "parent_local",
                    "source_axioms": [],
                    "note": "both occurrences are the same parent-visible handshake",
                }
            }}},
        }

    def test_cross_child_request_alias_is_certified_without_reopening_child_rtl(self):
        semantic = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        result = semantic["results"][0]
        partition = result["formal"]["certificate"]["partition"]

        self.assertTrue(semantic["all_axioms_formally_proved"], semantic["counts"])
        self.assertEqual(semantic["counts"][FORMALLY_PROVED], 1)
        self.assertEqual(
            result["formal"]["proof_method"],
            "exact-parent-child-occurrence-partition",
        )
        self.assertEqual(
            partition["occurrence_conditions"][
                "BoomNonBlockingDCache::region-0-3::MSHRReqFire"
            ]["kind"],
            "exact-imported-derived-parent-frontier-condition",
        )
        self.assertFalse(partition["child_rtl_reopened"])

    def test_parent_can_reexport_a_region_owned_public_boundary_event(self):
        candidate = {
            "schema_version": UMCM_SCHEMA_VERSION,
            "task_id": "public-region-boundary-regression",
            "work_unit_id": "BoomNonBlockingDCache",
            "occurrences": [{
                "id": "MemGrant",
                "kind": "boundary",
                "physical_event_ids": ["BoomNonBlockingDCache::auto.out.d.fire"],
                "definition": "auto.out.d.valid && auto.out.d.ready",
                "multiplicity": "repeatable",
                "index": None,
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
                "evidence_statement_ids": [],
            }],
            "predicates": [],
            "identity_keys": [],
            "cases": [],
            "axioms": [{
                "id": "A1",
                "formal": {
                    "type": "occurrence_partition",
                    "whole": "MemGrant",
                    "parts": ["BoomNonBlockingDCache::region-0-2::DFire"],
                    "relation": "same_cycle_exactly_one",
                    "scope_identity": None,
                },
                "derived_from_case_ids": [],
                "evidence_statement_ids": [],
                "status": "candidate",
            }],
            "assumptions": [],
            "unresolved": [],
            "rationale": [],
            "extensions": {"parent_synthesis": {"axiom_provenance": {
                "A1": {
                    "kind": "parent_local",
                    "source_axioms": [],
                    "note": "same physical D-channel handshake",
                }
            }}},
        }

        semantic = run_semantic_validation(
            candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        result = semantic["results"][0]

        self.assertEqual(result["validation_level"], FORMALLY_PROVED, result)
        conditions = result["formal"]["certificate"]["partition"]["occurrence_conditions"]
        self.assertEqual(
            conditions["BoomNonBlockingDCache::region-0-2::DFire"]["kind"],
            "exact-shared-physical-event-alias",
        )


if __name__ == "__main__":
    unittest.main()
