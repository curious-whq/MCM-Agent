from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from frontend.pipeline import StaticFrontend
from frontend.workunit import build_hierarchical_work_unit
from workflow.handoff import build_work_unit_static_handoff
from workflow.schema import UMCM_SCHEMA_VERSION
from workflow.semantic import (
    STRUCTURALLY_SUPPORTED, COUNTEREXAMPLE, FORMALLY_PROVED,
    run_semantic_validation,
    HandoffControlModel,
    _tilelink_on_probe_spec,
    _build_trusted_umcm,
    compile_candidate_properties,
    freeze_task_dir,
)


FIXTURE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"


def _empty_grounding():
    return {
        "state_register": None,
        "state_values": [],
        "signals_true": [],
        "signals_false": [],
    }


class SemanticWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = FIXTURE.read_text(encoding="utf-8")
        frontend = StaticFrontend.from_firrtl(text)
        unit = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="BoomProbeUnit",
        )
        cls.handoff = build_work_unit_static_handoff(
            unit,
            frontend.graph("BoomProbeUnit"),
            frontend.registries["BoomProbeUnit"],
        )
        cls.event_by_suffix = {
            event["id"].split("::", 1)[1]: event["id"]
            for event in cls.handoff["events"]
        }

    def _candidate(self):
        def boundary(identifier, suffix):
            return {
                "id": identifier,
                "kind": "boundary",
                "physical_event_ids": [self.event_by_suffix[suffix]],
                "definition": suffix,
                "multiplicity": "unspecified",
                "grounding": _empty_grounding(),
                "evidence_statement_ids": [0],
            }

        occurrences = [
            boundary("ProbeReq", "io.req.fire"),
            boundary("MetaRead", "io.meta_read.fire"),
            boundary("LSURelease", "io.lsu_release.fire"),
            boundary("ProbeAck", "io.rep.fire"),
            boundary("WBReq", "io.wb_req.fire"),
            boundary("MetaWrite", "io.meta_write.fire"),
            {
                "id": "WBComplete",
                "kind": "derived",
                "physical_event_ids": [],
                "definition": "state == 8 && io.wb_req.ready",
                "multiplicity": "at_most_once",
                "grounding": {
                    "state_register": "state",
                    "state_values": [8],
                    "signals_true": ["io.wb_req.ready"],
                    "signals_false": [],
                },
                "evidence_statement_ids": [44, 45, 46],
            },
        ]
        predicates = [
            {
                "id": "ActiveProbe",
                "definition": "state != 0",
                "grounding": {
                    "source_signal": None,
                    "negated": False,
                    "state_register": "state",
                    "state_values": list(range(1, 11)),
                },
                "evidence_statement_ids": [8],
            }
        ]
        identity = [
            {
                "id": "ProbeTxn",
                "carrier_state": "req",
                "fields": ["address", "source"],
                "description": "latched probe request",
                "evidence_statement_ids": [23, 24],
            }
        ]

        def sig(name):
            return {"op": "signal", "name": name}

        def ax(identifier, formal):
            return {
                "id": identifier,
                "formal": formal,
                "derived_from_case_ids": [],
                "evidence_statement_ids": [0],
                "status": "candidate",
            }

        axioms = [
            ax(
                "A1",
                {
                    "type": "forbid_when",
                    "occurrence": "ProbeReq",
                    "predicate": "ActiveProbe",
                    "scope_identity": None,
                },
            ),
            ax(
                "A2",
                {
                    "type": "identity_flow",
                    "identity": "ProbeTxn",
                    "capture": {"on": "ProbeReq", "source": "io.req.bits", "carrier": "req"},
                    "projections": [
                        {"on": "ProbeAck", "target": "io.rep.bits.address", "expr": sig("req.address")},
                        {"on": "ProbeAck", "target": "io.rep.bits.source", "expr": sig("req.source")},
                        {"on": "LSURelease", "target": "io.lsu_release.bits.address", "expr": sig("req.address")},
                        {"on": "LSURelease", "target": "io.lsu_release.bits.source", "expr": sig("req.source")},
                    ],
                },
            ),
            ax(
                "A3",
                {
                    "type": "exclusion",
                    "left": "WBReq",
                    "rights": ["LSURelease", "ProbeAck"],
                    "scope_identity": "ProbeTxn",
                },
            ),
            ax(
                "A4",
                {
                    "type": "ordered_before",
                    "before": "LSURelease",
                    "after": "ProbeAck",
                    "required_prior": None,
                    "scope_identity": "ProbeTxn",
                },
            ),
            ax(
                "A5",
                {
                    "type": "ordered_before",
                    "before": "ProbeAck",
                    "after": "MetaWrite",
                    "required_prior": "LSURelease",
                    "scope_identity": "ProbeTxn",
                },
            ),
            ax(
                "A6a",
                {
                    "type": "ordered_before",
                    "before": "WBReq",
                    "after": "WBComplete",
                    "required_prior": None,
                    "scope_identity": "ProbeTxn",
                },
            ),
            ax(
                "A6b",
                {
                    "type": "ordered_before",
                    "before": "WBComplete",
                    "after": "MetaWrite",
                    "required_prior": "WBReq",
                    "scope_identity": "ProbeTxn",
                },
            ),
            ax(
                "A8",
                {
                    "type": "value_constraint",
                    "on": "ProbeAck",
                    "expr": {"op": "bit", "value": sig("io.rep.bits.opcode"), "index": 0},
                    "relation": "eq",
                    "value": 0,
                    "scope_identity": None,
                },
            ),
        ]
        return {
            "schema_version": UMCM_SCHEMA_VERSION,
            "task_id": "test",
            "work_unit_id": "BoomProbeUnit",
            "occurrences": occurrences,
            "predicates": predicates,
            "identity_keys": identity,
            "cases": [],
            "axioms": axioms,
            "assumptions": [],
            "unresolved": [],
            "rationale": [],
            "extensions": {},
        }


    def test_formal_ast_is_single_source_for_rendering_and_obligation(self):
        candidate = self._candidate()
        compiled = compile_candidate_properties(candidate)
        a4 = next(item for item in compiled["obligations"] if item["axiom_id"] == "A4")
        self.assertEqual(a4["checker"], "history_order")
        self.assertEqual(a4["arguments"], {"before": "LSURelease", "after": "ProbeAck"})
        self.assertIn("LSURelease <mu ProbeAck", a4["rendered_formula"])
        self.assertEqual(a4["formal"], next(x for x in candidate["axioms"] if x["id"] == "A4")["formal"])

    def test_probe_control_axioms_are_structurally_supported(self):
        result = run_semantic_validation(self._candidate(), self.handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        for axiom in ("A1", "A3", "A4", "A5", "A6a", "A6b", "A8"):
            self.assertEqual(by_id[axiom]["structural"]["status"], STRUCTURALLY_SUPPORTED, by_id[axiom])
            self.assertEqual(by_id[axiom]["validation_level"], STRUCTURALLY_SUPPORTED)
            self.assertFalse(by_id[axiom]["trusted"])

    def test_identity_projection_is_structurally_grounded(self):
        result = run_semantic_validation(self._candidate(), self.handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A2"]["structural"]["status"], STRUCTURALLY_SUPPORTED, by_id["A2"])
        self.assertEqual(by_id["A2"]["validation_level"], STRUCTURALLY_SUPPORTED)
        self.assertFalse(by_id["A2"]["trusted"])

    def test_identity_projection_mismatch_is_refuted(self):
        candidate = self._candidate()
        axiom = next(item for item in candidate["axioms"] if item["id"] == "A2")
        axiom["formal"]["projections"][0]["expr"] = {"op": "signal", "name": "req.source"}
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A2"]["validation_level"], "REFUTED")
        self.assertFalse(by_id["A2"]["trusted"])

    def test_reversed_order_produces_counterexample(self):
        candidate = self._candidate()
        axiom = next(item for item in candidate["axioms"] if item["id"] == "A4")
        axiom["formal"] = {
            "type": "ordered_before",
            "before": "ProbeAck",
            "after": "LSURelease",
            "required_prior": None,
            "scope_identity": "ProbeTxn",
        }
        result = run_semantic_validation(candidate, self.handoff)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A4"]["structural"]["status"], COUNTEREXAMPLE)
        self.assertEqual(by_id["A4"]["validation_level"], "REFUTED")
        self.assertTrue(by_id["A4"]["structural"].get("counterexample"))


    def test_no_formal_backend_never_promotes_structural_support_to_trusted(self):
        result = run_semantic_validation(self._candidate(), self.handoff, formal_backend="none")
        self.assertTrue(result["all_axioms_structurally_supported"])
        self.assertFalse(result["all_axioms_formally_proved"])
        self.assertEqual(result["trusted_axiom_count"], 0)
        self.assertTrue(all(not item["trusted"] for item in result["results"]))
        self.assertTrue(all(item["formal"]["status"] == "FORMAL_UNKNOWN" for item in result["results"]))


    def test_explicit_control_backend_promotes_certified_control_axioms(self):
        result = run_semantic_validation(self._candidate(), self.handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        for axiom in ("A1", "A3", "A4", "A5", "A6a", "A6b", "A8"):
            self.assertEqual(by_id[axiom]["validation_level"], FORMALLY_PROVED, by_id[axiom])
            self.assertTrue(by_id[axiom]["trusted"])
        self.assertEqual(by_id["A2"]["validation_level"], FORMALLY_PROVED, by_id["A2"])
        self.assertTrue(by_id["A2"]["trusted"])
        self.assertEqual(result["trusted_axiom_count"], 8)
        self.assertTrue(result["all_axioms_formally_proved"])

    def test_tilelink_on_probe_reference_checker_matches_all_legal_rows(self):
        report = (
            "mux(eq(req.param, UInt<2>(0h0)), "
            "mux(eq(reply_coh.state, UInt<2>(0h0)), UInt<3>(0h5), "
            "mux(eq(reply_coh.state, UInt<2>(0h1)), UInt<3>(0h4), UInt<3>(0h3))), "
            "mux(eq(req.param, UInt<2>(0h1)), "
            "mux(eq(reply_coh.state, UInt<2>(0h0)), UInt<3>(0h5), "
            "mux(eq(reply_coh.state, UInt<2>(0h1)), UInt<3>(0h4), UInt<3>(0h0))), "
            "mux(eq(reply_coh.state, UInt<2>(0h0)), UInt<3>(0h5), "
            "mux(eq(reply_coh.state, UInt<2>(0h1)), UInt<3>(0h2), UInt<3>(0h1)))))"
        )
        next_state = (
            "mux(eq(req.param, UInt<2>(0h0)), "
            "mux(eq(reply_coh.state, UInt<2>(0h0)), UInt<2>(0h0), "
            "mux(eq(reply_coh.state, UInt<2>(0h1)), UInt<2>(0h1), UInt<2>(0h2))), "
            "mux(eq(req.param, UInt<2>(0h1)), "
            "mux(eq(reply_coh.state, UInt<2>(0h0)), UInt<2>(0h0), UInt<2>(0h1)), UInt<2>(0h0)))"
        )
        handoff = {
            "statements": [
                {"id": 0, "text": "node is_dirty = eq(reply_coh.state, UInt<2>(0h3))", "drives": ["is_dirty"]},
                {"id": 1, "text": "node report_param = " + report, "drives": ["report_param"]},
                {"id": 2, "text": "node new_state = " + next_state, "drives": ["new_state"]},
            ]
        }
        model = HandoffControlModel(handoff)
        result = _tilelink_on_probe_spec(
            model,
            param_signal="req.param",
            current_state_signal="reply_coh.state",
            dirty_signal="is_dirty",
            report_signal="report_param",
            next_state_signal="new_state",
        )
        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertEqual(len(result["checked_rows"]), 12)

        bad_handoff = {"statements": [dict(item) for item in handoff["statements"]]}
        bad_handoff["statements"][2]["text"] = bad_handoff["statements"][2]["text"].replace(
            "UInt<2>(0h2)", "UInt<2>(0h3)", 1
        )
        bad_model = HandoffControlModel(bad_handoff)
        bad = _tilelink_on_probe_spec(
            bad_model,
            param_signal="req.param",
            current_state_signal="reply_coh.state",
            dirty_signal="is_dirty",
            report_signal="report_param",
            next_state_signal="new_state",
        )
        self.assertEqual(bad["status"], COUNTEREXAMPLE)

    def test_fully_proved_leaf_can_be_frozen_for_composition(self):
        candidate = self._candidate()
        semantic = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        trusted = _build_trusted_umcm(candidate, semantic["results"])
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "response_parsed.json").write_text(json.dumps(candidate), encoding="utf-8")
            (directory / "semantic_validation.json").write_text(json.dumps(semantic), encoding="utf-8")
            (directory / "trusted_umcm.json").write_text(json.dumps(trusted), encoding="utf-8")
            (directory / "validation.json").write_text(json.dumps({"valid": True, "errors": [], "warnings": []}), encoding="utf-8")
            frozen = freeze_task_dir(directory)
            self.assertEqual(frozen["freeze"]["status"], "FROZEN_FOR_COMPOSITION")
            self.assertEqual(len(frozen["axioms"]), len(candidate["axioms"]))
            status = json.loads((directory / "status.json").read_text())
            self.assertEqual(status["status"], "FROZEN_FOR_COMPOSITION")

    def test_freeze_refuses_unproved_leaf(self):
        candidate = self._candidate()
        semantic = run_semantic_validation(candidate, self.handoff, formal_backend="none")
        trusted = _build_trusted_umcm(candidate, semantic["results"])
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "response_parsed.json").write_text(json.dumps(candidate), encoding="utf-8")
            (directory / "semantic_validation.json").write_text(json.dumps(semantic), encoding="utf-8")
            (directory / "trusted_umcm.json").write_text(json.dumps(trusted), encoding="utf-8")
            with self.assertRaises(ValueError):
                freeze_task_dir(directory)

    def test_explicit_control_backend_refuses_uncertified_control_model(self):
        handoff = dict(self.handoff)
        handoff["statements"] = [dict(item) for item in self.handoff["statements"]]
        # Corrupt one concrete state write so its target cannot be finitely resolved.
        # A fail-closed backend must refuse promotion instead of silently ignoring it.
        victim = next(item for item in handoff["statements"] if "state" in item.get("drives", []) and item.get("kind") == "connect")
        victim["text"] = "connect state, mystery_next_state"
        victim["reads"] = ["mystery_next_state"]
        result = run_semantic_validation(self._candidate(), handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED)
        self.assertFalse(by_id["A4"]["trusted"])
        self.assertEqual(by_id["A4"]["formal"]["status"], "FORMAL_UNKNOWN")



if __name__ == "__main__":
    unittest.main()

class IndexedOccurrenceLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = FIXTURE.read_text(encoding="utf-8")
        frontend = StaticFrontend.from_firrtl(text)
        unit = build_hierarchical_work_unit(
            frontend.design, frontend.graph, frontend.registries, root_module="BoomProbeUnit"
        )
        cls.handoff = build_work_unit_static_handoff(
            unit, frontend.graph("BoomProbeUnit"), frontend.registries["BoomProbeUnit"]
        )
        cls.event_by_suffix = {
            event["id"].split("::", 1)[1]: event["id"] for event in cls.handoff["events"]
        }

    def _candidate(self):
        return SemanticWorkflowTests._candidate(self)
    def test_join_axiom_is_formal_and_provable(self):
        candidate = self._candidate()
        candidate["axioms"].append({
            "id": "AJOIN",
            "formal": {
                "type": "join",
                "prerequisites": ["ProbeReq", "LSURelease"],
                "after": "ProbeAck",
                "scope_identity": "ProbeTxn",
            },
            "derived_from_case_ids": [],
            "evidence_statement_ids": [0],
            "status": "candidate",
        })
        compiled = compile_candidate_properties(candidate)
        obligation = next(x for x in compiled["obligations"] if x["axiom_id"] == "AJOIN")
        self.assertEqual(obligation["checker"], "history_join")
        self.assertIn("ProbeReq", obligation["rendered_formula"])
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["AJOIN"]["validation_level"], "FORMALLY_PROVED")
        self.assertTrue(by_id["AJOIN"]["trusted"])

    def test_same_index_order_is_formal_and_fail_closed_without_index_backend(self):
        candidate = self._candidate()
        for occurrence_id in ("MetaRead", "WBReq"):
            occurrence = next(x for x in candidate["occurrences"] if x["id"] == occurrence_id)
            occurrence["index"] = {
                "name": "beat",
                "expr": {"op": "signal", "name": "req.address"},
                "domain": {"start": 0, "end_exclusive": 2},
            }
        candidate["axioms"].append({
            "id": "ASAMEIDX",
            "formal": {
                "type": "ordered_before",
                "before": "MetaRead",
                "after": "WBReq",
                "required_prior": None,
                "scope_identity": "ProbeTxn",
                "scope_index": {"name": "beat", "relation": "same"},
            },
            "derived_from_case_ids": [],
            "evidence_statement_ids": [0],
            "status": "candidate",
        })
        compiled = compile_candidate_properties(candidate)
        obligation = next(x for x in compiled["obligations"] if x["axiom_id"] == "ASAMEIDX")
        self.assertEqual(obligation["arguments"]["scope_index"], {"name": "beat", "relation": "same"})
        self.assertIn("same index beat", obligation["rendered_formula"])
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["ASAMEIDX"]["validation_level"], "GROUNDED")
        self.assertFalse(by_id["ASAMEIDX"]["trusted"])
        self.assertEqual(by_id["ASAMEIDX"]["formal"]["status"], "FORMAL_UNKNOWN")
        self.assertEqual(by_id["ASAMEIDX"]["formal"]["required_backend_capability"], "same-index-relation")

    def test_same_index_lookup_expression_is_preserved_in_obligation(self):
        candidate = self._candidate()
        meta = next(x for x in candidate["occurrences"] if x["id"] == "MetaRead")
        meta["index"] = {
            "name": "beat",
            "expr": {"op": "signal", "name": "req.address"},
            "domain": {"start": 0, "end_exclusive": 2},
        }
        candidate["axioms"].append({
            "id": "ALOOKUP",
            "formal": {
                "type": "signal_equality",
                "on": "MetaRead",
                "target": "io.meta_read.bits.idx",
                "source": {
                    "op": "lookup",
                    "value": {"op": "signal", "name": "req.address"},
                    "index": {"op": "index_var", "name": "beat"}
                },
                "scope_identity": "ProbeTxn",
                "scope_index": {"name": "beat", "relation": "same"},
            },
            "derived_from_case_ids": [],
            "evidence_statement_ids": [0],
            "status": "candidate",
        })
        compiled = compile_candidate_properties(candidate)
        obligation = next(x for x in compiled["obligations"] if x["axiom_id"] == "ALOOKUP")
        self.assertEqual(obligation["arguments"]["source"], "req.address[beat]")
        self.assertIn("same index beat", obligation["rendered_formula"])

    def test_indexed_complete_is_formal_but_fail_closed_without_index_backend(self):
        candidate = self._candidate()
        meta = next(x for x in candidate["occurrences"] if x["id"] == "MetaRead")
        meta["index"] = {
            "name": "i",
            "expr": {"op": "signal", "name": "req.address"},
            "domain": {"start": 0, "end_exclusive": 2},
        }
        candidate["axioms"].append({
            "id": "AINDEX",
            "formal": {
                "type": "indexed_complete",
                "occurrence": "MetaRead",
                "completion": "ProbeAck",
                "index": "i",
                "domain": {"start": 0, "end_exclusive": 2},
                "cardinality": "exactly_once",
                "scope_identity": "ProbeTxn",
            },
            "derived_from_case_ids": [],
            "evidence_statement_ids": [0],
            "status": "candidate",
        })
        compiled = compile_candidate_properties(candidate)
        obligation = next(x for x in compiled["obligations"] if x["axiom_id"] == "AINDEX")
        self.assertEqual(obligation["checker"], "indexed_coverage")
        self.assertIn("forall i", obligation["rendered_formula"])
        result = run_semantic_validation(candidate, self.handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["AINDEX"]["validation_level"], "PARTIALLY_SUPPORTED")
        self.assertFalse(by_id["AINDEX"]["trusted"])
        self.assertEqual(by_id["AINDEX"]["formal"]["status"], "FORMAL_UNKNOWN")

class WritebackIndexedFormalRegressionTests(unittest.TestCase):
    def test_real_writeback_patterns_are_fully_proved(self):
        fixture = Path(__file__).parent / "fixtures" / "boom_writebackunit_logic.fir"
        candidate_path = Path(__file__).parent / "fixtures" / "boom_writeback_candidate_umcm.json"
        frontend = StaticFrontend.from_firrtl(fixture.read_text(encoding="utf-8"))
        unit = build_hierarchical_work_unit(
            frontend.design,
            frontend.graph,
            frontend.registries,
            root_module="BoomWritebackUnit",
        )
        handoff = build_work_unit_static_handoff(
            unit,
            frontend.graph("BoomWritebackUnit"),
            frontend.registries["BoomWritebackUnit"],
        )
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        result = run_semantic_validation(candidate, handoff, formal_backend="explicit-control")
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(result["trusted_axiom_count"], 10, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        for axiom_id in [f"A{i}" for i in range(1, 11)]:
            self.assertEqual(by_id[axiom_id]["validation_level"], FORMALLY_PROVED, by_id[axiom_id])
            self.assertTrue(by_id[axiom_id]["trusted"])

        self.assertEqual(
            by_id["A3"]["formal"]["certificate"]["proof_domain"],
            "exact-bounded-indexed-pipeline",
        )
        self.assertEqual(
            by_id["A7"]["formal"]["certificate"]["proof_domain"],
            "exact-bounded-indexed-occurrence",
        )
        self.assertEqual(
            by_id["A8"]["formal"]["proof_domain"],
            "local-combinational-equality",
        )
