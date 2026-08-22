from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from workflow.formal_patterns import (
    STRUCTURALLY_SUPPORTED,
    declared_signal_type_from_handoff,
    prove_combinational_forbid_when,
    prove_conditional_constant_bit,
    prove_conditional_signal_equality,
    prove_same_index_valid_token_provenance,
    prove_same_cycle_occurrence_partition,
)
from workflow.manual import validate_candidate_grounding
from workflow.circular_queue_prover import prove_same_index_circular_queue_provenance
from workflow.semantic import FORMALLY_PROVED, HandoffControlModel, run_semantic_validation


RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8"
)
LOCKED_ARBITER_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8"
)
STQ_EXECUTE_QUEUE_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121"
)
RETRY_QUEUE_RUN_DIR = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "leaf_abstraction-LSU.retry_queue-4e9eb249feec6033"
)


class MshrRpqFormalPatternRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads((RUN_DIR / "static_handoff.json").read_text(encoding="utf-8"))
        candidate = json.loads((RUN_DIR / "response_parsed.json").read_text(encoding="utf-8"))
        # A9 was an over-strong aggregate equality: out.uop is overwritten from
        # the separately maintained uops array.  The refined candidate drops it.
        candidate["axioms"] = [axiom for axiom in candidate["axioms"] if axiom["id"] != "A9"]
        cls.candidate = candidate

    def test_real_mshr_rpq_candidate_is_fully_proved(self):
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}

        self.assertEqual(result["candidate_axiom_count"], 9, result)
        self.assertEqual(result["trusted_axiom_count"], 9, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)

        for axiom_id in ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]:
            self.assertEqual(by_id[axiom_id]["validation_level"], FORMALLY_PROVED, by_id[axiom_id])
            self.assertEqual(
                by_id[axiom_id]["formal"]["proof_method"],
                "exact-combinational-exclusion",
                by_id[axiom_id],
            )

        self.assertEqual(by_id["A8"]["validation_level"], FORMALLY_PROVED, by_id["A8"])
        self.assertEqual(by_id["A11"]["validation_level"], FORMALLY_PROVED, by_id["A11"])
        self.assertEqual(
            by_id["A11"]["formal"]["proof_method"],
            "exact-indexed-valid-token-provenance",
            by_id["A11"],
        )

    def test_combinational_exclusion_fails_closed_when_not_logically_forbidden(self):
        candidate = copy.deepcopy(self.candidate)
        queue_full = next(item for item in candidate["predicates"] if item["id"] == "QueueFull")
        queue_full["grounding"]["source_signal"] = "io.enq.valid"
        model = HandoffControlModel(self.handoff)

        result = prove_combinational_forbid_when(
            model,
            candidate,
            occurrence="EnqHandshake",
            predicate="QueueFull",
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)

    def test_valid_token_provenance_rejects_unaccounted_creator(self):
        handoff = copy.deepcopy(self.handoff)
        victim = next(statement for statement in handoff["statements"] if statement["id"] == 257)
        victim["text"] = "connect valids[deq_ptr_value], UInt<1>(0h1)"
        model = HandoffControlModel(handoff)

        result = prove_same_index_valid_token_provenance(
            model,
            self.candidate,
            before="QueueInsert",
            after="DeqHandshake",
            scope_index={"name": "slot", "relation": "same"},
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertIn("unaccounted writer", result.get("reason", ""))


class EventGateProofContextTests(unittest.TestCase):
    @staticmethod
    def _handoff(with_bridge: bool) -> dict:
        statement = lambda identifier, kind, text, drives, reads: {
            "id": identifier,
            "kind": kind,
            "text": text,
            "drives": drives,
            "reads": reads,
            "control_reads": [],
            "status": "supported",
            "source": None,
            "note": None,
        }
        bridge = statement(
            4,
            "connect",
            "connect auto.out.b.ready, nodeOut.b.ready",
            ["auto.out.b.ready"],
            ["nodeOut.b.ready"],
        )
        return {
            "state": [],
            "statements": [
                statement(1, "node", "node not_active = eq(active, UInt<1>(0h0))", ["not_active"], ["active"]),
                statement(2, "node", "node ready_gate = and(sink_ready, not_active)", ["ready_gate"], ["sink_ready", "not_active"]),
                statement(3, "connect", "connect nodeOut.b.ready, ready_gate", ["nodeOut.b.ready"], ["ready_gate"]),
            ],
            "events": [{
                "id": "GateRegion::auto.out.b.fire",
                "valid": "auto.out.b.valid",
                "ready": "auto.out.b.ready",
            }],
            "proof_context": {
                "policy": "exact-local-event-gate-bridges-v0.1",
                "event_gate_statement_ids": [4] if with_bridge else [],
                "event_gate_statements": [bridge] if with_bridge else [],
                "llm_evidence": False,
            },
        }

    @staticmethod
    def _candidate() -> dict:
        return {
            "occurrences": [{
                "id": "ProbeFire",
                "kind": "boundary",
                "physical_event_ids": ["GateRegion::auto.out.b.fire"],
                "grounding": {
                    "state_register": None,
                    "state_values": [],
                    "signals_true": [],
                    "signals_false": [],
                },
            }],
            "predicates": [{
                "id": "Active",
                "grounding": {
                    "source_signal": "active",
                    "negated": False,
                    "state_register": None,
                    "state_values": [],
                },
            }],
        }

    def test_prover_uses_exact_non_owned_event_gate_bridge(self):
        without = prove_combinational_forbid_when(
            HandoffControlModel(self._handoff(False)),
            self._candidate(),
            occurrence="ProbeFire",
            predicate="Active",
        )
        self.assertNotEqual(without["status"], STRUCTURALLY_SUPPORTED, without)

        with_bridge = prove_combinational_forbid_when(
            HandoffControlModel(self._handoff(True)),
            self._candidate(),
            occurrence="ProbeFire",
            predicate="Active",
        )
        self.assertEqual(with_bridge["status"], STRUCTURALLY_SUPPORTED, with_bridge)
        self.assertEqual(with_bridge["event_gate_bridge_statement_ids"], [4])


class FilteredPhysicalOccurrenceTests(unittest.TestCase):
    @staticmethod
    def _handoff() -> dict:
        def statement(identifier, kind, text, drives, reads, controls=None):
            return {
                "id": identifier,
                "kind": kind,
                "text": text,
                "drives": drives,
                "reads": reads,
                "control_reads": controls or [],
                "status": "supported",
                "source": None,
                "note": None,
            }

        return {
            "state": [],
            "statements": [
                statement(
                    1,
                    "node",
                    "node is_ack = eq(bus.d.bits.source, UInt<2>(0h2))",
                    ["is_ack"],
                    ["bus.d.bits.source", "h2"],
                ),
                statement(2, "else", "else :", [], ["is_ack"], ["is_ack"]),
                statement(
                    3,
                    "connect",
                    "connect sink.d, bus.d",
                    ["sink.d.bits.opcode"],
                    ["bus.d"],
                    ["is_ack"],
                ),
            ],
            "events": [{
                "id": "Region::bus.d.fire",
                "valid": "bus.d.valid",
                "ready": "bus.d.ready",
            }],
            "dependency_edges": [{
                "src": "is_ack",
                "dst": "sink.d.bits.opcode",
                "kind": "control",
                "statement_ids": [2, 3],
                "source": None,
            }],
        }

    @staticmethod
    def _candidate() -> dict:
        def occurrence(identifier, relation=None):
            tests = [] if relation is None else [{
                "expr": {"op": "signal", "name": "bus.d.bits.source"},
                "relation": relation,
                "value": 2,
            }]
            return {
                "id": identifier,
                "kind": "boundary" if relation is None else "derived",
                "physical_event_ids": ["Region::bus.d.fire"],
                "grounding": {
                    "signals_true": [],
                    "signals_false": [],
                    "state_values": [],
                    "value_tests": tests,
                },
            }

        return {
            "occurrences": [
                occurrence("DFire"),
                occurrence("AckFire", "eq"),
                occurrence("GrantFire", "neq"),
            ],
            "predicates": [],
        }

    def test_payload_filtered_physical_event_forms_an_exact_partition(self):
        result = prove_same_cycle_occurrence_partition(
            HandoffControlModel(self._handoff()),
            self._candidate(),
            whole="DFire",
            parts=["AckFire", "GrantFire"],
            relation="same_cycle_exactly_one",
        )

        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)

    def test_valid_only_boundary_forms_an_exact_partition(self):
        handoff = self._handoff()
        handoff["events"][0].pop("ready")
        result = prove_same_cycle_occurrence_partition(
            HandoffControlModel(handoff),
            self._candidate(),
            whole="DFire",
            parts=["AckFire", "GrantFire"],
            relation="same_cycle_exactly_one",
        )

        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)

    def test_else_branch_aggregate_forwarding_is_proved_under_filtered_event(self):
        result = prove_conditional_signal_equality(
            HandoffControlModel(self._handoff()),
            self._candidate(),
            target="sink.d.bits.opcode",
            source="bus.d.bits.opcode",
            on="GrantFire",
        )

        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        activation = result["selected_drivers"][0]["activation"]
        self.assertEqual(activation["control_polarities"], {"is_ack": "negative"})

    def test_conditionally_zero_extended_payload_is_equal_to_one_bit_source(self):
        handoff = self._handoff()
        handoff["events"] = []
        handoff["dependency_edges"] = []
        handoff["statements"] = [
            {
                "id": identifier,
                "kind": "connect" if identifier == 7 else "node",
                "text": text,
                "drives": [drive],
                "reads": reads,
                "control_reads": [],
                "status": "supported",
                "source": None,
                "note": None,
            }
            for identifier, text, drive, reads in [
                (1, "node zeroed = mux(sc, UInt<1>(0h0), payload)", "zeroed", ["sc", "h0", "payload"]),
                (2, "node sign = bits(zeroed, 7, 7)", "sign", ["zeroed"]),
                (3, "node ext = mux(sign, UInt<56>(0hffffffffffffff), UInt<56>(0h0))", "ext", ["sign", "hffffffffffffff", "h0"]),
                (4, "node packed = cat(ext, zeroed)", "packed", ["ext", "zeroed"]),
                (5, "node fail = and(sc, fail_bit)", "fail", ["sc", "fail_bit"]),
                (6, "node result = or(packed, fail)", "result", ["packed", "fail"]),
                (7, "connect resp.data, result", "resp.data", ["result"]),
            ]
        ]
        candidate = {
            "occurrences": [{
                "id": "SCResponse",
                "kind": "derived",
                "physical_event_ids": [],
                "grounding": {
                    "signals_true": ["valid", "sc"],
                    "signals_false": [],
                    "state_values": [],
                },
            }],
            "predicates": [],
        }

        result = prove_conditional_signal_equality(
            HandoffControlModel(handoff),
            candidate,
            target="resp.data",
            source="fail",
            on="SCResponse",
        )

        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)


class PriorityAggregateProjectionTests(unittest.TestCase):
    @staticmethod
    def _handoff() -> dict:
        def statement(identifier, kind, text, drives, reads, controls=None):
            return {
                "id": identifier,
                "kind": kind,
                "text": text,
                "drives": drives,
                "reads": reads,
                "control_reads": controls or [],
                "status": "supported",
                "source": None,
                "note": None,
            }

        return {
            "state": [],
            "statements": [
                statement(1, "connect", "connect lo_req[0].flag, UInt<1>(0h0)", ["lo_req[0].flag"], []),
                statement(2, "connect", "connect hi_req[0].flag, UInt<1>(0h1)", ["hi_req[0].flag"], []),
                statement(3, "connect", "connect selected, lo_req", ["selected[0].addr", "selected[0].flag"], ["lo_req"]),
                statement(4, "when", "when choose :", [], ["choose"], ["choose"]),
                statement(5, "connect", "connect selected, hi_req", ["selected[0].addr", "selected[0].flag"], ["hi_req"], ["choose"]),
                statement(6, "connect", "connect out, selected", ["out[0].addr", "out[0].flag"], ["selected"]),
            ],
            "events": [],
            "dependency_edges": [
                {
                    "src": "choose",
                    "dst": field,
                    "kind": "control",
                    "statement_ids": [4, 5],
                    "source": None,
                }
                for field in ("selected[0].addr", "selected[0].flag")
            ],
        }

    @staticmethod
    def _candidate() -> dict:
        def occurrence(identifier, *, positive):
            return {
                "id": identifier,
                "kind": "derived",
                "physical_event_ids": [],
                "grounding": {
                    "signals_true": ["choose"] if positive else [],
                    "signals_false": [] if positive else ["choose"],
                    "state_values": [],
                },
            }

        return {
            "occurrences": [
                occurrence("LowSelected", positive=False),
                occurrence("HighSelected", positive=True),
            ],
            "predicates": [],
        }

    def test_vector_aggregate_alias_and_last_connect_are_projected_exactly(self):
        result = prove_conditional_signal_equality(
            HandoffControlModel(self._handoff()),
            self._candidate(),
            target="out[0].addr",
            source="lo_req[0].addr",
            on="LowSelected",
        )

        self.assertEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertEqual(result["resolved_target"], "selected[0].addr")
        self.assertEqual(result["alias_chain"][0]["source"], "selected[0].addr")

    def test_conditional_constant_bit_checks_only_the_selected_priority_writer(self):
        model = HandoffControlModel(self._handoff())
        candidate = self._candidate()
        low = prove_conditional_constant_bit(
            model,
            candidate,
            signal="out[0].flag",
            bit=0,
            expected=0,
            on="LowSelected",
        )
        wrong_high = prove_conditional_constant_bit(
            model,
            candidate,
            signal="out[0].flag",
            bit=0,
            expected=0,
            on="HighSelected",
        )

        self.assertEqual(low["status"], STRUCTURALLY_SUPPORTED, low)
        self.assertNotEqual(wrong_high["status"], STRUCTURALLY_SUPPORTED, wrong_high)

    def test_ssa_node_is_an_exact_driver_and_supports_aggregate_projection(self):
        handoff = self._handoff()
        handoff["statements"] = [
            statement for statement in handoff["statements"]
            if int(statement["id"]) in {1, 2, 6}
        ]
        handoff["statements"].extend([
            {
                "id": 7,
                "kind": "node",
                "text": "node selected = mux(choose, hi_req, lo_req)",
                "drives": ["selected"],
                "reads": ["choose", "hi_req", "lo_req"],
                "control_reads": ["choose"],
                "status": "supported",
                "source": None,
                "note": None,
            },
            {
                "id": 8,
                "kind": "node",
                "text": "node cause = mux(choose, UInt<5>(0h10), UInt<5>(0h3))",
                "drives": ["cause"],
                "reads": ["choose"],
                "control_reads": ["choose"],
                "status": "supported",
                "source": None,
                "note": None,
            },
        ])
        handoff["dependency_edges"] = []
        model = HandoffControlModel(handoff)
        candidate = self._candidate()

        projection = prove_conditional_signal_equality(
            model,
            candidate,
            target="out[0].addr",
            source="hi_req[0].addr",
            on="HighSelected",
        )
        bit = prove_conditional_constant_bit(
            model,
            candidate,
            signal="cause",
            bit=4,
            expected=1,
            on="HighSelected",
        )

        self.assertEqual(projection["status"], STRUCTURALLY_SUPPORTED, projection)
        self.assertEqual(bit["status"], STRUCTURALLY_SUPPORTED, bit)
        self.assertEqual(
            projection["selected_drivers"][0]["activation"]["kind"],
            "exact-unconditional-ssa-node",
        )


class LockedOwnerProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads(
            (LOCKED_ARBITER_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        cls.candidate = json.loads(
            (LOCKED_ARBITER_RUN_DIR / "response_parsed.json").read_text(encoding="utf-8")
        )

    @staticmethod
    def _without_reset_bridge(handoff: dict) -> dict:
        result = copy.deepcopy(handoff)
        context = result.setdefault("proof_context", {})
        context["state_support_statement_ids"] = []
        context["state_support_statements"] = []
        return result

    def test_real_locked_tilelink_arbiter_proves_partition_history_and_payload(self):
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        self.assertEqual(result["trusted_axiom_count"], 32, result)
        self.assertTrue(result["all_axioms_formally_proved"], result)
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(
            by_id["A3"]["formal"]["proof_method"],
            "exact-locked-owner-provenance",
        )
        self.assertEqual(
            by_id["A5"]["formal"]["certificate"]["proof_domain"],
            "exact-conditional-symbolic-driver-equality",
        )

    def test_locked_owner_proof_fails_closed_without_counter_reset(self):
        result = run_semantic_validation(
            self.candidate,
            self._without_reset_bridge(self.handoff),
            formal_backend="explicit-control",
        )
        self.assertFalse(result["all_axioms_formally_proved"], result)


class AggregateBundleEqualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = json.loads(
            (STQ_EXECUTE_QUEUE_RUN_DIR / "task.json").read_text(encoding="utf-8")
        )
        cls.handoff = json.loads(
            (STQ_EXECUTE_QUEUE_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        cls.candidate = json.loads(
            (STQ_EXECUTE_QUEUE_RUN_DIR / "response_parsed.json").read_text(encoding="utf-8")
        )

    def test_declared_io_and_memory_port_aggregate_types_are_recovered(self):
        for signal in ("io.enq.bits", "MPORT", "io.deq.bits", "io_deq_bits_MPORT"):
            recovered = declared_signal_type_from_handoff(self.handoff, signal)
            self.assertIsNotNone(recovered, signal)
            self.assertIn("debug_wb_data", recovered)

    def test_real_queue_aggregate_references_ground_and_prove(self):
        grounding = validate_candidate_grounding(
            self.candidate,
            self.task,
            self.handoff,
        )
        self.assertTrue(grounding["valid"], grounding)

        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED, by_id["A4"])
        self.assertEqual(
            by_id["A4"]["formal"]["proof_method"],
            "exact-conditional-aggregate-equality",
        )
        self.assertEqual(by_id["A6"]["validation_level"], FORMALLY_PROVED, by_id["A6"])
        self.assertEqual(by_id["A5"]["validation_level"], FORMALLY_PROVED, by_id["A5"])
        self.assertEqual(
            by_id["A5"]["formal"]["proof_method"],
            "exact-circular-queue-slot-provenance",
        )
        self.assertGreater(
            by_id["A5"]["formal"]["certificate"]["checked_transitions"],
            0,
        )

    def test_aggregate_equality_fails_closed_when_one_field_is_missing(self):
        handoff = copy.deepcopy(self.handoff)
        handoff["statements"] = [
            statement
            for statement in handoff["statements"]
            if statement.get("id") != 19
        ]
        result = run_semantic_validation(
            self.candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A4"]["validation_level"], FORMALLY_PROVED, by_id["A4"])

    def test_queue_provenance_returns_counterexample_if_empty_dequeue_is_enabled(self):
        handoff = copy.deepcopy(self.handoff)
        valid = next(statement for statement in handoff["statements"] if statement.get("id") == 46)
        valid["text"] = "connect io.deq.valid, UInt<1>(0h1)"
        result = prove_same_index_circular_queue_provenance(
            HandoffControlModel(handoff),
            self.candidate,
            before="QueueInsert",
            after="DeqHandshake",
            scope_index={"name": "slot", "relation": "same"},
        )
        self.assertNotEqual(result["status"], STRUCTURALLY_SUPPORTED, result)
        self.assertIn("gate", result.get("reason", ""))
        semantic = run_semantic_validation(
            self.candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in semantic["results"]}
        self.assertNotEqual(by_id["A5"]["validation_level"], FORMALLY_PROVED, by_id["A5"])


class FilteredCircularQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = json.loads(
            (RETRY_QUEUE_RUN_DIR / "static_handoff.json").read_text(encoding="utf-8")
        )
        cls.candidate = json.loads(
            (RETRY_QUEUE_RUN_DIR / "response_parsed.json").read_text(encoding="utf-8")
        )

    def test_invalid_head_skip_uses_pointer_advance_provenance(self):
        result = run_semantic_validation(
            self.candidate,
            self.handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertTrue(result["all_axioms_formally_proved"], result)
        self.assertEqual(by_id["A11"]["validation_level"], FORMALLY_PROVED, by_id["A11"])
        certificate = by_id["A11"]["formal"]["certificate"]
        self.assertEqual(certificate["proof_domain"], "exact-circular-queue-slot-provenance")
        self.assertEqual(certificate["after_action_occurrence"], "HeadAdvance")
        self.assertEqual(certificate["reachable_ghost_states"], 128)
        self.assertEqual(certificate["checked_transitions"], 480)
        self.assertNotIn("valids", {item["signal"] for item in certificate["rtl_state"]})
        self.assertNotIn("uops", {item["signal"] for item in certificate["rtl_state"]})

    def test_filtered_queue_proof_fails_closed_without_empty_gate(self):
        handoff = copy.deepcopy(self.handoff)
        gate = next(statement for statement in handoff["statements"] if statement.get("id") == 37)
        gate["text"] = "node _do_deq_T_3 = _do_deq_T_1"
        result = run_semantic_validation(
            self.candidate,
            handoff,
            formal_backend="explicit-control",
        )
        by_id = {item["axiom_id"]: item for item in result["results"]}
        self.assertNotEqual(by_id["A11"]["validation_level"], FORMALLY_PROVED, by_id["A11"])


if __name__ == "__main__":
    unittest.main()
