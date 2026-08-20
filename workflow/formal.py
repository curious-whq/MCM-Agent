from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .semantic import (
    FORMALLY_PROVED,
    SPEC_PROVED,
    STRUCTURALLY_SUPPORTED,
    HandoffControlModel,
    _forbid_when,
    _history_chain,
    _history_join,
    _indexed_coverage,
    _same_index_history_order,
    _same_index_signal_alias,
    _history_order,
    _transaction_exclusion,
    _signal_alias,
    _constant_bit,
    _identity_projection,
    _tilelink_on_probe_spec,
)
from .formal_patterns import (
    prove_combinational_forbid_when,
    prove_same_index_valid_token_provenance,
)


FORMAL_BACKEND_API_VERSION = "formal-backend-api-0.7"
FORMAL_UNKNOWN = "FORMAL_UNKNOWN"
FORMAL_COUNTEREXAMPLE = "FORMAL_COUNTEREXAMPLE"


class FormalBackend(Protocol):
    name: str

    def describe(self) -> dict[str, Any]: ...

    def prove(
        self,
        obligation: dict[str, Any],
        *,
        candidate: dict[str, Any],
        handoff: dict[str, Any],
    ) -> dict[str, Any]: ...


@dataclass(frozen=True)
class NoFormalBackend:
    """Explicit fail-closed backend used when no formal engine is configured."""

    name: str = "none"

    def describe(self) -> dict[str, Any]:
        return {
            "api_version": FORMAL_BACKEND_API_VERSION,
            "name": self.name,
            "available": False,
            "trusted_proof_levels": [FORMALLY_PROVED, SPEC_PROVED],
            "note": (
                "No formal engine is configured. Structural support is not promoted "
                "to formal proof."
            ),
        }

    def prove(
        self,
        obligation: dict[str, Any],
        *,
        candidate: dict[str, Any],
        handoff: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "status": FORMAL_UNKNOWN,
            "backend": self.name,
            "reason": "no formal backend configured",
        }


def _state_register_for(candidate: dict[str, Any]) -> str:
    for occurrence in candidate.get("occurrences", []):
        register = occurrence.get("grounding", {}).get("state_register")
        if register:
            return str(register)
    for predicate in candidate.get("predicates", []):
        register = predicate.get("grounding", {}).get("state_register")
        if register:
            return str(register)
    return "state"


def _referenced_occurrences(obligation: dict[str, Any]) -> set[str]:
    refs = set(obligation.get("references", {}).get("occurrences", []))
    args = obligation.get("arguments", {})
    for key in ("occurrence", "completion", "before", "after", "required_prior", "left"):
        value = args.get(key)
        if isinstance(value, str):
            refs.add(value)
    for key in ("rights", "sequence", "prerequisites"):
        value = args.get(key)
        if isinstance(value, list):
            refs.update(x for x in value if isinstance(x, str))
    return refs


def _certify_control_overapprox(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    obligation: dict[str, Any],
) -> dict[str, Any]:
    """Fail-closed certificate for the finite-control over-approximation.

    The proof argument is intentionally small and inspectable:
    * the reset value of the control register is known;
    * every concrete write to that register in the WorkUnit ledger is accounted for;
    * each write has a resolved source control state and a finite set of target states;
    * data-dependent muxes are expanded to *all* possible target constants, so the graph
      over-approximates branch behavior rather than choosing a branch;
    * unlabelled self-loops are present, preventing accidental progress assumptions;
    * every occurrence referenced by the obligation has at least one grounded transition.

    If any of these checks fails, this backend refuses to produce FORMALLY_PROVED.
    """

    if model.reset_state is None:
        return {"certified": False, "reason": "control register reset state is unknown"}
    if not model.known_states:
        return {"certified": False, "reason": "no finite control-state domain was recovered"}

    state_writes: list[int] = []
    captured_writes: list[int] = []
    for statement_id, statement in sorted(model.statements.items()):
        if model.state_register not in statement.get("drives", []):
            continue
        if statement.get("kind") in {"regreset", "reg"}:
            continue
        state_writes.append(statement_id)
        source = model._source_state(statement)
        text = statement.get("text", "")
        connect = model.__class__.__module__  # keep certificate independent of parser internals
        del connect
        # The transition extractor already accepts only connect/assignment writes.
        matching = [t for t in model.transitions if t.statement_id == statement_id]
        if source is None or not matching:
            return {
                "certified": False,
                "reason": "a control-register write could not be conservatively translated",
                "statement_id": statement_id,
                "statement": text,
            }
        if any(t.src != source for t in matching):
            return {
                "certified": False,
                "reason": "control transition source mismatch",
                "statement_id": statement_id,
            }
        if any(t.dst not in model.known_states for t in matching):
            return {
                "certified": False,
                "reason": "control transition targets state outside recovered domain",
                "statement_id": statement_id,
            }
        captured_writes.append(statement_id)

    if state_writes != captured_writes:
        return {
            "certified": False,
            "reason": "not every control-register write is represented in the transition graph",
            "state_writes": state_writes,
            "captured_writes": captured_writes,
        }

    self_loop_states = {
        t.src for t in model.transitions
        if t.statement_id is None and t.src == t.dst
    }
    if self_loop_states != set(model.known_states):
        return {
            "certified": False,
            "reason": "conservative stutter closure is incomplete",
            "missing_states": sorted(set(model.known_states) - self_loop_states),
        }

    occurrences = {item.get("id"): item for item in candidate.get("occurrences", [])}
    for occurrence_id in sorted(_referenced_occurrences(obligation)):
        occurrence = occurrences.get(occurrence_id)
        if occurrence is None:
            return {"certified": False, "reason": f"referenced occurrence {occurrence_id!r} is missing"}
        if not model.occurrence_source_states(occurrence_id):
            return {
                "certified": False,
                "reason": f"referenced occurrence {occurrence_id!r} has no grounded transition",
            }
        if occurrence.get("kind") == "derived":
            grounding = occurrence.get("grounding", {})
            if grounding.get("signals_false"):
                return {
                    "certified": False,
                    "reason": f"derived occurrence {occurrence_id!r} uses unsupported negative guards",
                }

    return {
        "certified": True,
        "proof_domain": "conservative-finite-control-abstraction",
        "state_register": model.state_register,
        "reset_state": model.reset_state,
        "known_states": sorted(model.known_states),
        "accounted_state_write_ids": state_writes,
        "stutter_closed_states": sorted(self_loop_states),
        "note": (
            "This is a formal exhaustive proof over a fail-closed conservative control abstraction "
            "derived from the FIRRTL ledger. It is not a full bit-level proof of arbitrary datapath semantics."
        ),
    }


@dataclass(frozen=True)
class ExplicitControlFormalBackend:
    """Exhaustive finite-state prover for control/order obligations.

    This backend is solver-free: the recovered finite control graph is exhaustively
    explored.  It promotes an obligation only after certifying that the graph is a
    conservative, stutter-closed abstraction of every control-register write relevant
    to the WorkUnit.  Payload/reference-spec semantics remain outside this backend.
    """

    name: str = "explicit-control"

    def describe(self) -> dict[str, Any]:
        return {
            "api_version": FORMAL_BACKEND_API_VERSION,
            "name": self.name,
            "available": True,
            "trusted_proof_levels": [FORMALLY_PROVED, SPEC_PROVED],
            "proof_domain": (
                "control + exact symbolic local + exact combinational exclusion + "
                "indexed token provenance + finite reference equivalence"
            ),
            "supported_checkers": [
                "forbid_when",
                "history_order",
                "history_chain",
                "history_join",
                "indexed_coverage",
                "transaction_exclusion",
                "signal_alias",
                "constant_bit",
                "identity_projection",
                "tilelink_on_probe_spec",
            ],
            "note": (
                "Exhaustive formal proof for certified finite-control/order properties, exact symbolic "
                "local/identity facts, exact local Boolean exclusions, bounded indexed token provenance, "
                "and selected finite reference equivalence checks. It is not a general bit-level SMT backend."
            ),
        }

    def prove(
        self,
        obligation: dict[str, Any],
        *,
        candidate: dict[str, Any],
        handoff: dict[str, Any],
    ) -> dict[str, Any]:
        checker = obligation.get("checker")
        args = obligation.get("arguments", {})
        if args.get("scope_index") and checker not in {"history_order", "signal_alias"}:
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": (
                    "same-index relation is represented, but this checker has no certified index-aware proof rule"
                ),
                "scope_index": args.get("scope_index"),
                "required_backend_capability": "same-index-relation",
            }
        state_register = _state_register_for(candidate)
        model = HandoffControlModel(handoff, state_register=state_register)
        model.label_occurrences(candidate.get("occurrences", []))

        # Some leaves (queues, arbiters, kill/flush gates) have no single FSM
        # state register.  Prove purely local forbid_when obligations directly
        # from their exact Boolean cones before falling back to finite-control.
        if checker == "forbid_when":
            local = prove_combinational_forbid_when(model, candidate, **args)
            if local.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": local.get("proof_domain"),
                    "proof": local.get("proof"),
                    "certificate": local,
                }

        # A same-index order can also be proved without an FSM when a bounded
        # valid/token array establishes exact provenance: reset invalid, one
        # token creator, all other writes clear/preserve false, and after(i)
        # requires the same token.  If the recognizer cannot certify that shape,
        # retain the existing control/pipeline proof path below.
        if checker == "history_order" and args.get("scope_index"):
            provenance = prove_same_index_valid_token_provenance(
                model,
                candidate,
                **args,
            )
            if provenance.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": provenance.get("proof_domain"),
                    "proof": provenance.get("proof"),
                    "certificate": provenance,
                }

        if checker in {"history_order", "history_chain", "history_join", "transaction_exclusion", "forbid_when"}:
            certificate = _certify_control_overapprox(model, candidate, obligation)
            if not certificate.get("certified"):
                return {
                    "status": FORMAL_UNKNOWN,
                    "backend": self.name,
                    "reason": "control abstraction could not be certified",
                    "certificate": certificate,
                }
            if checker == "history_order":
                if args.get("scope_index"):
                    result = _same_index_history_order(model, candidate, **args)
                else:
                    result = _history_order(model, **args)
            elif checker == "history_chain":
                result = _history_chain(model, **args)
            elif checker == "history_join":
                result = _history_join(model, candidate=candidate, **args)
            elif checker == "transaction_exclusion":
                result = _transaction_exclusion(model, **args)
            else:
                result = _forbid_when(model, candidate, **args)

            if result.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": "exhaustive-state-reachability",
                    "certificate": certificate,
                    "proof": result.get("proof"),
                }
            if result.get("status") == "COUNTEREXAMPLE":
                return {
                    "status": FORMAL_COUNTEREXAMPLE,
                    "backend": self.name,
                    "counterexample": result.get("counterexample") or result.get("counterexample_states"),
                    "reason": result.get("reason"),
                    "certificate": certificate,
                }
            unresolved = {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "control obligation unresolved"),
                "certificate": certificate,
            }
            if args.get("scope_index"):
                unresolved["scope_index"] = args.get("scope_index")
                unresolved["required_backend_capability"] = "same-index-relation"
            return unresolved


        if checker == "indexed_coverage":
            result = _indexed_coverage(model, candidate, **args)
            if result.get("status") == STRUCTURALLY_SUPPORTED and str(result.get("proof_domain", "")).startswith("exact-bounded-indexed"):
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": result.get("proof_domain"),
                    "proof": result.get("proof"),
                    "certificate": result,
                }
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "bounded indexed proof unresolved"),
                "structural_evidence": result,
                "required_backend_capability": "bounded-indexed-occurrence",
            }

        if checker == "identity_projection":
            result = _identity_projection(model, candidate, **args)
            if result.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": "exact-symbolic-transaction-identity",
                    "proof": result.get("proof"),
                    "proof_domain": result.get("proof_domain"),
                    "capture_statement_ids": result.get("capture_statement_ids", []),
                    "projection_proofs": result.get("projection_proofs", []),
                }
            if result.get("status") == "COUNTEREXAMPLE":
                return {
                    "status": FORMAL_COUNTEREXAMPLE,
                    "backend": self.name,
                    "reason": result.get("reason"),
                    "counterexample": result.get("mismatches"),
                }
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "identity projection proof unresolved"),
            }

        if checker == "tilelink_on_probe_spec":
            result = _tilelink_on_probe_spec(model, **args)
            if result.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": SPEC_PROVED,
                    "backend": self.name,
                    "proof_method": "exhaustive-finite-reference-equivalence",
                    "proof": result.get("proof"),
                    "proof_domain": result.get("proof_domain"),
                    "reference": result.get("reference"),
                    "checked_rows": result.get("checked_rows", []),
                    "reference_note": (
                        "SPEC_PROVED here is relative to the separately encoded TileLink "
                        "TLPermissions/ClientMetadata.onProbe reference table, not a theorem about "
                        "all TileLink implementations."
                    ),
                }
            if result.get("status") == "COUNTEREXAMPLE":
                return {
                    "status": FORMAL_COUNTEREXAMPLE,
                    "backend": self.name,
                    "reason": result.get("reason"),
                    "counterexample": result.get("mismatches"),
                }
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "TileLink reference equivalence unresolved"),
            }

        # Exact local combinational facts can be proved without the control abstraction.
        if checker == "signal_alias":
            if args.get("scope_index"):
                result = _same_index_signal_alias(model, candidate, on=obligation.get("formal", {}).get("on"), **args)
            else:
                result = _signal_alias(model, **args)
            if result.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": "exact-symbolic-driver-equality",
                    "proof": result.get("proof"),
                    "proof_domain": "local-combinational-equality",
                }
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "alias is not an exact symbolic equality"),
            }

        if checker == "constant_bit":
            result = _constant_bit(model, **args)
            if result.get("status") == STRUCTURALLY_SUPPORTED:
                return {
                    "status": FORMALLY_PROVED,
                    "backend": self.name,
                    "proof_method": "exact-constant-propagation",
                    "proof": result.get("proof"),
                    "proof_domain": "local-combinational-constant",
                }
            if result.get("status") == "COUNTEREXAMPLE":
                return {
                    "status": FORMAL_COUNTEREXAMPLE,
                    "backend": self.name,
                    "reason": result.get("reason"),
                }
            return {
                "status": FORMAL_UNKNOWN,
                "backend": self.name,
                "reason": result.get("reason", "constant property unresolved"),
            }

        return {
            "status": FORMAL_UNKNOWN,
            "backend": self.name,
            "reason": (
                f"checker {checker!r} is outside the explicit-control proof domain; "
                "use a bit-level SMT/RTL or protocol-spec backend"
            ),
        }


def get_formal_backend(name: str) -> FormalBackend:
    normalized = name.strip().lower()
    if normalized in {"", "none"}:
        return NoFormalBackend()
    if normalized in {"explicit-control", "explicit_control", "control"}:
        return ExplicitControlFormalBackend()
    raise ValueError(
        f"Unknown formal backend {name!r}. Bundled backends: 'none', 'explicit-control'."
    )
