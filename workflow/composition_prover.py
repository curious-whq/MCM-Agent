from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .composition import FROZEN_STATUS, _canonical_sha256
from .formal_patterns import (
    _and,
    _atoms,
    _bool_expr,
    _bool_refs,
    _const,
    _exact_boundary_or_derived_occurrence_condition,
    _not,
    _occurrence_condition,
    _or,
    _propagate_bool_refs,
    _unsat,
    _writer_activation,
)
from .semantic import (
    FORMALLY_PROVED,
    SPEC_PROVED,
    HandoffControlModel,
    _call,
    _canonical_expr,
    _statement_rhs,
)


COMPOSITION_PROVER_VERSION = "composition-prover-0.4"


@dataclass(frozen=True)
class Theorem:
    kind: str
    formal: dict[str, Any]
    source_id: str
    certificate: dict[str, Any]


def frozen_theorem_dependencies(value: Any) -> list[str]:
    """Return the direct frozen axioms actually consumed by a proof DAG.

    Composed/local theorem nodes are traversed, but an imported frozen theorem is
    treated as one direct dependency.  Its own frozen provenance remains the
    authoritative route to lower descendants.
    """

    found: set[str] = set()

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("kind") == "frozen-theorem":
                unit_id = node.get("work_unit_id")
                axiom_id = node.get("axiom_id")
                if isinstance(unit_id, str) and unit_id and isinstance(axiom_id, str) and axiom_id:
                    found.add(f"{unit_id}::{axiom_id}")
                return
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return sorted(found)


def derive_composition_provenance(formal_proof: dict[str, Any]) -> dict[str, Any]:
    """Derive parent-axiom provenance from the certified composition proof."""

    if formal_proof.get("backend") != "composition-prover":
        raise ValueError("composition provenance requires a composition-prover result")
    method = str(formal_proof.get("proof_method", ""))
    source_axioms = frozen_theorem_dependencies(formal_proof.get("certificate", {}))
    if method == "trusted-child-lift":
        kind = "lifted" if source_axioms else "parent_local"
    elif method == "trusted-history-transitivity":
        kind = "emergent" if source_axioms else "parent_local"
    elif method == "occurrence-bridge-history-composition":
        kind = "lifted" if source_axioms else "parent_local"
    elif method == "trusted-history-after-restriction":
        kind = "emergent" if source_axioms else "parent_local"
    elif method == "exact-parent-child-occurrence-partition":
        kind = "parent_local"
    elif method == "trusted-occurrence-partition-substitution":
        kind = "emergent" if source_axioms else "parent_local"
    elif method == "trusted-child-value-lift":
        kind = "lifted" if source_axioms else "parent_local"
    else:
        raise ValueError(f"unsupported composition proof method for provenance: {method!r}")
    return {
        "kind": kind,
        "source_axioms": source_axioms,
        "proof_method": method,
        "derivation": "formal-certificate-v0.1",
    }


def _qualify(unit_id: str, object_id: Any) -> Any:
    if not isinstance(object_id, str) or "::" in object_id:
        return object_id
    return f"{unit_id}::{object_id}"


def _qualified_formal(unit_id: str, formal: dict[str, Any]) -> dict[str, Any]:
    result = dict(formal)
    for key in ("occurrence", "before", "after", "required_prior", "predicate", "whole"):
        if result.get(key) is not None:
            result[key] = _qualify(unit_id, result[key])
    if isinstance(result.get("parts"), list):
        result["parts"] = [_qualify(unit_id, item) for item in result["parts"]]
    return result


def _theorem(formal: dict[str, Any], source_id: str, certificate: dict[str, Any]) -> Theorem | None:
    kind = str(formal.get("type", ""))
    if kind not in {"forbid_when", "ordered_before", "occurrence_partition", "value_constraint"}:
        return None
    return Theorem(kind=kind, formal=dict(formal), source_id=source_id, certificate=certificate)


def _collect_frozen_theorems(
    handoff: dict[str, Any],
) -> tuple[list[Theorem], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Load trusted theorem roots and semantic objects without opening child RTL."""

    facts: list[Theorem] = []
    occurrences: dict[str, dict[str, Any]] = {}
    predicates: dict[str, dict[str, Any]] = {}
    visited: set[tuple[str, str]] = set()

    def visit(summary: dict[str, Any], *, direct: bool) -> None:
        frozen = summary.get("frozen_umcm")
        if not isinstance(frozen, dict):
            return
        unit_id = str(summary.get("child_id") or frozen.get("work_unit_id") or "")
        expected_hash = summary.get("frozen_umcm_sha256")
        actual_hash = _canonical_sha256(frozen)
        if not unit_id or expected_hash != actual_hash:
            return
        if frozen.get("freeze", {}).get("status") != FROZEN_STATUS:
            return
        visit_key = (unit_id, actual_hash)
        if visit_key in visited:
            return
        visited.add(visit_key)

        direct_events = {
            str(item) for item in summary.get("boundary_events", []) if isinstance(item, str)
        } if direct else set()
        for item in frozen.get("occurrences", []):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            qualified = str(_qualify(unit_id, item["id"]))
            occurrences[qualified] = {
                "object": item,
                "unit_id": unit_id,
                "frozen_hash": actual_hash,
                "direct_boundary_events": direct_events,
            }
        for item in frozen.get("predicates", []):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            predicates[str(_qualify(unit_id, item["id"]))] = {
                "object": item,
                "unit_id": unit_id,
                "frozen_hash": actual_hash,
            }

        trusted_ids = {str(item) for item in frozen.get("trusted_axiom_ids", [])}
        for axiom in frozen.get("axioms", []):
            if not isinstance(axiom, dict) or str(axiom.get("id")) not in trusted_ids:
                continue
            formal = axiom.get("formal")
            if not isinstance(formal, dict):
                continue
            qualified_id = str(_qualify(unit_id, axiom["id"]))
            fact = _theorem(
                _qualified_formal(unit_id, formal),
                qualified_id,
                {
                    "kind": "frozen-theorem",
                    "work_unit_id": unit_id,
                    "axiom_id": str(axiom["id"]),
                    "frozen_umcm_sha256": actual_hash,
                },
            )
            if fact is not None:
                facts.append(fact)

        composition = frozen.get("composition")
        if isinstance(composition, dict):
            for imported in composition.get("imports", []):
                if isinstance(imported, dict):
                    visit(imported, direct=False)

    composition = handoff.get("composition", {})
    for summary in composition.get("child_summaries", []) if isinstance(composition, dict) else []:
        if isinstance(summary, dict):
            visit(summary, direct=True)
    return facts, occurrences, predicates


def _statement_target_rhs(model: HandoffControlModel, statement: dict[str, Any], target: str) -> str | None:
    parsed = _statement_rhs(statement)
    if parsed is None:
        return None
    lhs, rhs = (part.strip() for part in parsed)
    if target == lhs:
        return rhs
    if target.startswith(lhs + "."):
        suffix = target[len(lhs):]
        projected = model._project_aggregate_rhs(rhs, suffix)
        return projected if projected is not None else rhs + suffix
    # Aggregate connects with flipped leaves are represented by exact dependency
    # edges even when the textual aggregate direction points the other way.
    for edge in model.handoff.get("dependency_edges", []):
        ids = {int(item) for item in edge.get("statement_ids", [])}
        if int(statement.get("id", -1)) not in ids or edge.get("kind") != "data":
            continue
        if edge.get("src") == target:
            return str(edge.get("dst"))
        if edge.get("dst") == target:
            return str(edge.get("src"))
    return None


def _state_case_activation_certificate(
    model: HandoffControlModel,
    signal: str,
    statement: dict[str, Any],
    source_state: int,
) -> dict[str, Any] | None:
    controls = [str(item) for item in statement.get("control_reads", [])]
    tests = [(control, model._state_test(control)) for control in controls]
    if not controls or any(test is None for _, test in tests):
        return None
    typed = [(control, test) for control, test in tests if test is not None]
    positive_control, positive_test = max(typed, key=lambda item: item[1][0])
    if positive_test[1] != source_state:
        return None

    statement_id = int(statement.get("id", -1))
    polarities = []
    for control, test in typed:
        edges = [
            edge for edge in model.handoff.get("dependency_edges", [])
            if edge.get("kind") == "control"
            and edge.get("dst") == signal
            and edge.get("src") == control
            and statement_id in {int(item) for item in edge.get("statement_ids", [])}
        ]
        blocks = {
            int(block_id): model.statements.get(int(block_id))
            for edge in edges
            for block_id in edge.get("statement_ids", [])
            if int(block_id) != statement_id
        }
        direct = [
            block for block in blocks.values()
            if isinstance(block, dict)
            and block.get("kind") in {"when", "else"}
            and control in {str(item) for item in block.get("control_reads", [])}
        ]
        expected = "when" if control == positive_control else "else"
        if len(direct) != 1 or direct[0].get("kind") != expected:
            return None
        polarities.append({
            "control": control,
            "state_value": int(test[1]),
            "polarity": "positive" if expected == "when" else "negative",
            "block_statement_id": int(direct[0].get("id", -1)),
        })
    return {
        "kind": "exact-lowered-state-case-activation",
        "state_value": source_state,
        "controls": polarities,
    }


def _effective_signal_condition(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    signal: str,
    *,
    source_occurrence: dict[str, Any] | None = None,
) -> tuple[tuple[Any, ...], dict[str, Any]] | None:
    refs = _bool_refs(model, candidate)
    writers = [
        statement
        for statement in model.statements.values()
        if signal in {str(item) for item in statement.get("drives", [])}
        and statement.get("kind") not in {"node", "reg", "regreset", "when"}
    ]
    if not writers:
        incoming = [
            edge for edge in model.handoff.get("dependency_edges", [])
            if edge.get("kind") == "data" and edge.get("dst") == signal
            and isinstance(edge.get("src"), str)
        ]
        sources = {str(edge["src"]) for edge in incoming}
        if len(sources) == 1:
            source = next(iter(sources))
            expr = _bool_expr(model, refs | {source}, source, opaque={source})
            if expr is not None:
                return expr, {
                    "signal": signal,
                    "kind": "exact-directed-dependency-alias",
                    "source": source,
                    "statement_ids": sorted({
                        int(item) for edge in incoming for item in edge.get("statement_ids", [])
                    }),
                }
        expr = _bool_expr(model, refs | {signal}, signal, opaque={signal})
        return None if expr is None else (expr, {"signal": signal, "kind": "frontier-input"})

    source_states = {
        int(item)
        for item in (source_occurrence or {}).get("grounding", {}).get("state_values", [])
    }
    state_register = (source_occurrence or {}).get("grounding", {}).get("state_register")
    if len(source_states) == 1 and state_register == model.state_register:
        source_state = next(iter(source_states))
        scoped = [statement for statement in writers if model._source_state(statement) == source_state]
        if len(scoped) == 1:
            statement = scoped[0]
            # A lowered else-if state case carries earlier state comparisons with
            # negative polarity and the latest comparison with positive polarity.
            # Accept only a pure state-discriminator chain with no extra guard.
            activation = _state_case_activation_certificate(
                model,
                signal,
                statement,
                source_state,
            )
            if activation is not None:
                statement_id = int(statement.get("id", -1))
                if not any(
                    int(other.get("id", -1)) > statement_id
                    and model._source_state(other) in {None, source_state}
                    for other in writers
                ):
                    rhs = _statement_target_rhs(model, statement, signal)
                    if rhs is not None:
                        refs = _bool_refs(model, candidate)
                        _propagate_bool_refs(model, rhs, refs)
                        value = _bool_expr(model, refs, rhs)
                        if value is not None:
                            return value, {
                                "signal": signal,
                                "kind": "exact-state-scoped-writer",
                                "state_register": model.state_register,
                                "state_value": source_state,
                                "statement_id": statement_id,
                                "rhs": rhs,
                                "activation": activation,
                            }

    current: tuple[Any, ...] | None = None
    records: list[dict[str, Any]] = []
    for statement in sorted(writers, key=lambda item: int(item.get("id", -1))):
        rhs = _statement_target_rhs(model, statement, signal)
        if rhs is None:
            return None
        activation_info = _writer_activation(model, signal, statement, refs)
        if activation_info is None:
            return None
        activation, activation_certificate = activation_info
        writer_refs = set(refs)
        _propagate_bool_refs(model, rhs, writer_refs)
        value = _bool_expr(model, writer_refs, rhs)
        if value is None:
            return None
        if current is None:
            if activation != _const(True):
                return None
            current = value
        else:
            current = _or(_and(activation, value), _and(_not(activation), current))
        records.append({
            "statement_id": int(statement.get("id", -1)),
            "rhs": rhs,
            "activation": activation_certificate,
        })
    return None if current is None else (current, {
        "signal": signal,
        "kind": "exact-priority-writer-cone",
        "writers": records,
    })


def _child_boundary_signals(
    handoff: dict[str, Any],
    imported: dict[str, Any],
) -> tuple[list[str], dict[str, Any]] | None:
    occurrence = imported["object"]
    if occurrence.get("kind") != "boundary":
        return None
    physical = [str(item) for item in occurrence.get("physical_event_ids", [])]
    if len(physical) != 1 or physical[0] not in imported.get("direct_boundary_events", set()):
        return None
    unit_id = str(imported["unit_id"])
    prefix = unit_id + "::"
    if not physical[0].startswith(prefix) or not physical[0].endswith(".fire"):
        return None
    channel = physical[0][len(prefix):-len(".fire")]

    parent_path = str(handoff.get("work_unit", {}).get("instance_path", ""))
    if unit_id == parent_path:
        relative = ""
    elif parent_path and unit_id.startswith(parent_path + "."):
        relative = unit_id[len(parent_path) + 1:]
    else:
        return None
    base = f"{relative}.{channel}" if relative else channel

    if relative:
        clock_target = f"{relative}.clock"
        clock_edges = [
            edge for edge in handoff.get("dependency_edges", [])
            if edge.get("src") == "clock" and edge.get("dst") == clock_target
            and edge.get("kind") == "data"
        ]
        if not clock_edges:
            return None
        clock_certificate = {
            "parent_clock": "clock",
            "child_clock": clock_target,
            "statement_ids": sorted({
                int(item) for edge in clock_edges for item in edge.get("statement_ids", [])
            }),
        }
    else:
        clock_certificate = {"parent_clock": "clock", "child_clock": "clock", "statement_ids": []}
    return [f"{base}.valid", f"{base}.ready"], {
        "physical_event_id": physical[0],
        "clock": clock_certificate,
    }


def _prove_occurrence_inclusion(
    before_id: str,
    after_id: str,
    *,
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    model: HandoffControlModel,
    imported_occurrences: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Prove every local `before_id` occurrence is an exposed child boundary event."""

    local_ids = {str(item.get("id")) for item in candidate.get("occurrences", [])}
    if before_id not in local_ids or after_id not in imported_occurrences:
        return None
    target = _child_boundary_signals(handoff, imported_occurrences[after_id])
    if target is None:
        return None
    signals, boundary_certificate = target
    refs = _bool_refs(model, candidate)
    source = _occurrence_condition(model, candidate, before_id, refs)
    if source is None:
        return None

    source_occurrence = next(
        (item for item in candidate.get("occurrences", []) if item.get("id") == before_id),
        None,
    )

    def conjuncts(expr: tuple[Any, ...]) -> set[tuple[Any, ...]]:
        if expr[0] == "and":
            return conjuncts(expr[1]) | conjuncts(expr[2])
        return {expr}

    def implies(antecedent: tuple[Any, ...], consequent: tuple[Any, ...]) -> bool:
        available = conjuncts(antecedent)
        required = conjuncts(consequent)
        if required <= available:
            return True
        proved, _ = _unsat(_and(antecedent, _not(consequent)))
        return proved is True

    signal_proofs = []
    for signal in signals:
        effective = _effective_signal_condition(
            model,
            candidate,
            signal,
            source_occurrence=source_occurrence,
        )
        if effective is None:
            return None
        condition, certificate = effective
        if not implies(source, condition):
            return None
        signal_proofs.append(certificate)
    return {
        "kind": "exact-occurrence-bridge",
        "relation": "occurrence-inclusion",
        "subset": before_id,
        "superset": after_id,
        "boundary": boundary_certificate,
        "signal_proofs": signal_proofs,
        "local_rtl_only": True,
    }


def _parent_occurrence_condition(
    occurrence_id: str,
    *,
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    model: HandoffControlModel,
    imported_occurrences: dict[str, dict[str, Any]],
) -> tuple[tuple[Any, ...], dict[str, Any]] | None:
    """Expose an occurrence as an exact Boolean condition at the parent boundary."""

    refs = _bool_refs(model, candidate)
    local_ids = {str(item.get("id")) for item in candidate.get("occurrences", [])}
    if occurrence_id in local_ids:
        condition = _exact_boundary_or_derived_occurrence_condition(
            model,
            candidate,
            occurrence_id,
            refs,
        )
        if condition is None:
            return None
        return condition, {
            "kind": "exact-parent-local-occurrence-condition",
            "occurrence": occurrence_id,
        }

    imported = imported_occurrences.get(occurrence_id)
    if imported is None:
        return None
    target = _child_boundary_signals(handoff, imported)
    if target is None:
        return None
    signals, boundary = target
    condition = _const(True)
    signal_proofs: list[dict[str, Any]] = []
    for signal in signals:
        outgoing = [
            edge for edge in handoff.get("dependency_edges", [])
            if edge.get("kind") == "data" and edge.get("src") == signal
        ]
        incoming = [
            edge for edge in handoff.get("dependency_edges", [])
            if edge.get("kind") == "data" and edge.get("dst") == signal
        ]
        # A child output is a semantic frontier value, even if a lowered bulk
        # connect also lists it among syntactic drives.  Its parent-side use is
        # exact, but its producer remains hidden inside the frozen child.
        if outgoing and not incoming:
            value = _bool_expr(model, refs | {signal}, signal, opaque={signal})
            effective = None if value is None else (
                value,
                {
                    "signal": signal,
                    "kind": "exposed-child-frontier-output",
                    "dependency_statement_ids": sorted({
                        int(item)
                        for edge in outgoing
                        for item in edge.get("statement_ids", [])
                    }),
                },
            )
        else:
            effective = _effective_signal_condition(model, candidate, signal)
        if effective is None:
            return None
        value, certificate = effective
        condition = _and(condition, value)
        signal_proofs.append(certificate)
    return condition, {
        "kind": "exact-imported-boundary-occurrence-condition",
        "occurrence": occurrence_id,
        "boundary": boundary,
        "signal_proofs": signal_proofs,
        "child_rtl_reopened": False,
    }


def _prove_parent_occurrence_equivalence(
    left: str,
    right: str,
    *,
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    model: HandoffControlModel,
    imported_occurrences: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    left_info = _parent_occurrence_condition(
        left,
        candidate=candidate,
        handoff=handoff,
        model=model,
        imported_occurrences=imported_occurrences,
    )
    right_info = _parent_occurrence_condition(
        right,
        candidate=candidate,
        handoff=handoff,
        model=model,
        imported_occurrences=imported_occurrences,
    )
    if left_info is None or right_info is None:
        return None
    left_expr, left_certificate = left_info
    right_expr, right_certificate = right_info
    mismatch = _or(
        _and(left_expr, _not(right_expr)),
        _and(right_expr, _not(left_expr)),
    )
    unsat, atoms = _unsat(mismatch)
    if unsat is not True:
        return None
    return {
        "kind": "exact-parent-boundary-occurrence-equivalence",
        "left": left,
        "right": right,
        "atom_count": atoms,
        "left_condition": left_certificate,
        "right_condition": right_certificate,
    }


def _prove_onehot0_register_invariant(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    root: str,
    indices: list[int],
) -> tuple[tuple[Any, ...], dict[str, Any]] | None:
    """Certify a reset-preserved onehot-or-zero vector register invariant."""

    reset_statement = next(
        (
            statement for statement in model.statements.values()
            if statement.get("kind") == "regreset"
            and root in {str(item) for item in statement.get("drives", [])}
        ),
        None,
    )
    if reset_statement is None:
        return None
    reset_text = str(reset_statement.get("text", ""))
    if "," not in reset_text:
        return None
    reset_value = reset_text.rsplit(",", 1)[1].strip()

    refs = _bool_refs(model, candidate)
    reset_proofs: list[dict[str, Any]] = []
    update_select: str | None = None
    winner_exprs: dict[int, tuple[Any, ...]] = {}
    update_proofs: list[dict[str, Any]] = []

    def expand_alias(expr: str, seen: set[str] | None = None) -> str | None:
        text = expr.strip()
        seen = seen or set()
        call = _call(text)
        if call is not None:
            return text
        if text in seen:
            return None
        rhs = model.rhs(text)
        return text if rhs is None else expand_alias(rhs, seen | {text})

    for index in indices:
        reset_leaf = model._project_aggregate_rhs(reset_value, f"[{index}]")
        if reset_leaf is None:
            reset_leaf = f"{reset_value}[{index}]"
        _propagate_bool_refs(model, reset_leaf, refs)
        reset_expr = _bool_expr(model, refs, reset_leaf)
        reset_unsat, reset_atoms = _unsat(reset_expr) if reset_expr is not None else (None, 0)
        if reset_unsat is not True:
            return None
        reset_proofs.append({"index": index, "reset_to_zero": True, "atom_count": reset_atoms})

        update = expand_alias(f"{root}[{index}]")
        parsed = _call(update) if update is not None else None
        if parsed is None or parsed[0] != "mux" or len(parsed[1]) != 3:
            return None
        select, winner, hold = parsed[1]
        if hold.strip() != f"{root}[{index}]":
            return None
        if update_select is None:
            update_select = select.strip()
        elif update_select != select.strip():
            return None
        _propagate_bool_refs(model, winner, refs)
        winner_expr = _bool_expr(model, refs, winner)
        if winner_expr is None:
            return None
        winner_exprs[index] = winner_expr
        update_proofs.append({
            "index": index,
            "next": update,
            "select": select.strip(),
            "winner": winner.strip(),
            "hold": hold.strip(),
        })

    winner_exclusion: list[dict[str, Any]] = []
    invariant = _const(True)
    for position, left in enumerate(indices):
        for right in indices[position + 1:]:
            unsat, atoms = _unsat(_and(winner_exprs[left], winner_exprs[right]))
            if unsat is not True:
                return None
            invariant = _and(
                invariant,
                _not(_and(
                    ("atom", ("nz", ("ref", f"{root}[{left}]"))),
                    ("atom", ("nz", ("ref", f"{root}[{right}]"))),
                )),
            )
            winner_exclusion.append({"indices": [left, right], "atom_count": atoms})

    return invariant, {
        "kind": "exact-inductive-onehot0-register-invariant",
        "register": root,
        "indices": indices,
        "reset_statement_id": int(reset_statement.get("id", -1)),
        "reset_proofs": reset_proofs,
        "update_select": update_select,
        "update_proofs": update_proofs,
        "winner_mutual_exclusion": winner_exclusion,
        "induction": "reset is onehot0; common mux selects pairwise-exclusive winners or holds prior onehot0 state",
    }


def _prove_parent_occurrence_partition(
    formal: dict[str, Any],
    *,
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    model: HandoffControlModel,
    imported_occurrences: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    if formal.get("relation") != "same_cycle_exactly_one":
        return None
    whole = str(formal.get("whole", ""))
    parts = [str(item) for item in formal.get("parts", [])]
    if not whole or not parts:
        return None
    resolved = {
        occurrence: _parent_occurrence_condition(
            occurrence,
            candidate=candidate,
            handoff=handoff,
            model=model,
            imported_occurrences=imported_occurrences,
        )
        for occurrence in [whole, *parts]
    }
    if any(value is None for value in resolved.values()):
        return None
    expressions = {key: value[0] for key, value in resolved.items() if value is not None}
    invariant = _const(True)
    invariant_certificates: list[dict[str, Any]] = []
    referenced_atoms = {
        atom
        for expression in expressions.values()
        for atom in _atoms(expression)
    }
    referenced_signals = {
        str(atom[1][1])
        for atom in referenced_atoms
        if len(atom) == 2 and atom[0] == "nz"
        and isinstance(atom[1], tuple) and atom[1][0] == "ref"
    }
    for root in sorted(str(item) for item in model.state_roots):
        indices = sorted({
            int(match.group(1))
            for signal in referenced_signals
            if (match := re.fullmatch(re.escape(root) + r"\[(\d+)\]", signal))
        })
        if len(indices) < 2:
            continue
        invariant_info = _prove_onehot0_register_invariant(
            model,
            candidate,
            root,
            indices,
        )
        if invariant_info is None:
            continue
        constraint, certificate = invariant_info
        invariant = _and(invariant, constraint)
        invariant_certificates.append(certificate)
    any_part = _const(False)
    for part in parts:
        any_part = _or(any_part, expressions[part])
    obligations: list[dict[str, Any]] = []
    for name, expression in (
        ("whole_without_part", _and(expressions[whole], _not(any_part))),
        ("part_without_whole", _and(any_part, _not(expressions[whole]))),
    ):
        unsat, atoms = _unsat(_and(invariant, expression))
        obligations.append({"kind": name, "unsat": unsat, "atom_count": atoms})
        if unsat is not True:
            return None
    for index, left in enumerate(parts):
        for right in parts[index + 1:]:
            unsat, atoms = _unsat(_and(invariant, _and(expressions[left], expressions[right])))
            obligations.append({
                "kind": "parts_mutually_exclusive",
                "parts": [left, right],
                "unsat": unsat,
                "atom_count": atoms,
            })
            if unsat is not True:
                return None
    return {
        "kind": "exact-parent-child-occurrence-partition",
        "whole": whole,
        "parts": parts,
        "occurrence_conditions": {
            key: value[1] for key, value in resolved.items() if value is not None
        },
        "obligations": obligations,
        "inductive_invariants": invariant_certificates,
        "child_rtl_reopened": False,
    }


def _partition_substitution_certificate(
    target: dict[str, Any],
    source: Theorem,
    *,
    equivalence: Any,
) -> dict[str, Any] | None:
    if source.kind != "occurrence_partition":
        return None
    if target.get("relation") != source.formal.get("relation"):
        return None
    target_parts = [str(item) for item in target.get("parts", [])]
    source_parts = [str(item) for item in source.formal.get("parts", [])]
    if len(target_parts) != len(source_parts):
        return None

    def match_parts(left: list[str], right: list[str]) -> list[dict[str, Any]] | None:
        remaining = list(right)
        certificates: list[dict[str, Any]] = []
        for item in left:
            matched = None
            for candidate_item in remaining:
                certificate = equivalence(item, candidate_item)
                if certificate is not None:
                    matched = (candidate_item, certificate)
                    break
            if matched is None:
                return None
            remaining.remove(matched[0])
            certificates.append(matched[1])
        return certificates

    whole_bridge = equivalence(str(target.get("whole")), str(source.formal.get("whole")))
    part_bridges = match_parts(target_parts, source_parts) if whole_bridge is not None else None
    orientation = "preserved"
    if whole_bridge is None or part_bridges is None:
        if len(target_parts) != 1:
            return None
        whole_bridge = equivalence(str(target.get("whole")), source_parts[0])
        reverse = equivalence(target_parts[0], str(source.formal.get("whole")))
        if whole_bridge is None or reverse is None:
            return None
        part_bridges = [reverse]
        orientation = "singleton-equivalence-reversed"
    return {
        "kind": "trusted-occurrence-partition-substitution",
        "source_theorem": source.certificate,
        "whole_bridge": whole_bridge,
        "part_bridges": part_bridges,
        "orientation": orientation,
    }


def _bit_signal(expr: Any) -> tuple[str, int] | None:
    if not isinstance(expr, dict) or expr.get("op") != "bit":
        return None
    value = expr.get("value")
    index = expr.get("index")
    if (
        not isinstance(value, dict)
        or value.get("op") != "signal"
        or not isinstance(value.get("name"), str)
        or not isinstance(index, int)
    ):
        return None
    return str(value["name"]), index


def _trusted_child_value_lift(
    target: dict[str, Any],
    source: Theorem,
    *,
    handoff: dict[str, Any],
    model: HandoffControlModel,
) -> dict[str, Any] | None:
    if source.kind != "value_constraint" or target.get("type") != "value_constraint":
        return None
    for key in ("relation", "value", "on", "scope_identity"):
        if target.get(key) != source.formal.get(key):
            return None
    target_signal = _bit_signal(target.get("expr"))
    source_signal = _bit_signal(source.formal.get("expr"))
    if target_signal is None or source_signal is None or target_signal[1] != source_signal[1]:
        return None

    unit_id = str(source.certificate.get("work_unit_id", ""))
    summaries = handoff.get("composition", {}).get("child_summaries", [])
    summary = next(
        (
            item for item in summaries
            if isinstance(item, dict) and str(item.get("child_id", "")) == unit_id
        ),
        None,
    )
    if summary is None:
        return None
    parent_path = str(handoff.get("work_unit", {}).get("instance_path", ""))
    if not parent_path or not unit_id.startswith(parent_path + "."):
        return None
    relative = unit_id[len(parent_path) + 1:]
    child_parent_signal = f"{relative}.{source_signal[0]}"
    if child_parent_signal not in {
        str(item) for item in summary.get("frontier_signals", [])
    }:
        return None
    target_nf = _canonical_expr(model, target_signal[0])
    child_nf = _canonical_expr(model, child_parent_signal)
    if target_nf is None or target_nf != child_nf:
        return None
    return {
        "kind": "trusted-child-value-lift",
        "source_theorem": source.certificate,
        "signal_bridge": {
            "kind": "exact-parent-local-signal-alias",
            "target_signal": target_signal[0],
            "child_frontier_signal": child_parent_signal,
            "normal_form": repr(target_nf),
        },
        "child_rtl_reopened": False,
    }


def _same_scope(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("scope_index") == right.get("scope_index")


def _index_projection_certificate(
    fact: Theorem,
    imported_occurrences: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    scope = fact.formal.get("scope_index")
    if not isinstance(scope, dict) or scope.get("relation") != "same" or not scope.get("name"):
        return None
    before = imported_occurrences.get(str(fact.formal.get("before")))
    after = imported_occurrences.get(str(fact.formal.get("after")))
    if before is None or after is None:
        return None
    before_index = before["object"].get("index")
    after_index = after["object"].get("index")
    if not isinstance(before_index, dict) or not isinstance(after_index, dict):
        return None
    if before_index.get("name") != scope["name"] or after_index.get("name") != scope["name"]:
        return None
    if before_index.get("domain") != after_index.get("domain"):
        return None
    return {
        "kind": "safe-existential-index-weakening",
        "index_name": scope["name"],
        "domain": before_index.get("domain"),
        "from": "same-index history",
        "to": "unindexed occurrence history",
    }


def prove_composition_obligations(
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    results: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Close parent obligations over trusted child theorems and exact local bridges."""

    if handoff.get("composition", {}).get("mode") != "parent_synthesis":
        return {}
    facts, imported_occurrences, _ = _collect_frozen_theorems(handoff)
    for result in results:
        if result.get("formal", {}).get("status") not in {FORMALLY_PROVED, SPEC_PROVED}:
            continue
        # Compiled obligations keep the formal AST in `formal`; their proof result
        # is stored in the same key only after semantic packaging, so use the AST
        # copied alongside the obligation when available.
        ast = result.get("formal_ast")
        if not isinstance(ast, dict):
            ast = result.get("compiled_formal")
        if not isinstance(ast, dict):
            axiom = next((x for x in candidate.get("axioms", []) if x.get("id") == result.get("axiom_id")), None)
            ast = axiom.get("formal") if isinstance(axiom, dict) else None
        fact = _theorem(ast, str(result.get("axiom_id")), {
            "kind": "local-proved-theorem",
            "proof": result.get("formal"),
        }) if isinstance(ast, dict) else None
        if fact is not None:
            facts.append(fact)

    model = HandoffControlModel(handoff)
    model.label_occurrences(candidate.get("occurrences", []))
    targets = {
        str(result.get("axiom_id")): result
        for result in results
        if result.get("formal", {}).get("status") not in {FORMALLY_PROVED, SPEC_PROVED}
    }
    proved: dict[str, dict[str, Any]] = {}
    bridge_cache: dict[tuple[str, str], dict[str, Any] | None] = {}
    equivalence_cache: dict[tuple[str, str], dict[str, Any] | None] = {}

    def bridge(subset: str, superset: str) -> dict[str, Any] | None:
        key = (subset, superset)
        if key not in bridge_cache:
            bridge_cache[key] = _prove_occurrence_inclusion(
                subset,
                superset,
                candidate=candidate,
                handoff=handoff,
                model=model,
                imported_occurrences=imported_occurrences,
            )
        return bridge_cache[key]

    def equivalence(left: str, right: str) -> dict[str, Any] | None:
        key = (left, right)
        if key not in equivalence_cache:
            equivalence_cache[key] = _prove_parent_occurrence_equivalence(
                left,
                right,
                candidate=candidate,
                handoff=handoff,
                model=model,
                imported_occurrences=imported_occurrences,
            )
        return equivalence_cache[key]

    progress = True
    while progress:
        progress = False
        for axiom_id, result in list(targets.items()):
            axiom = next((x for x in candidate.get("axioms", []) if x.get("id") == axiom_id), None)
            target = axiom.get("formal") if isinstance(axiom, dict) else None
            if not isinstance(target, dict):
                continue

            proof: dict[str, Any] | None = None
            if target.get("type") == "occurrence_partition":
                partition = _prove_parent_occurrence_partition(
                    target,
                    candidate=candidate,
                    handoff=handoff,
                    model=model,
                    imported_occurrences=imported_occurrences,
                )
                if partition is not None:
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "exact-parent-child-occurrence-partition",
                        "proof": "same-cycle occurrence partition proved from exact parent-local and exposed child-boundary conditions",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "partition": partition,
                        },
                    }
                declared = (
                    candidate.get("extensions", {})
                    .get("parent_synthesis", {})
                    .get("axiom_provenance", {})
                    .get(axiom_id, {})
                )
                declared_sources = {
                    str(item) for item in declared.get("source_axioms", [])
                } if isinstance(declared, dict) else set()
                partition_sources = [
                    source for source in facts
                    if not declared_sources or source.source_id in declared_sources
                ]
                if isinstance(declared, dict) and declared.get("kind") == "parent_local":
                    partition_sources = []
                for source in partition_sources if proof is None else []:
                    substitution = _partition_substitution_certificate(
                        target,
                        source,
                        equivalence=equivalence,
                    )
                    if substitution is None:
                        continue
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "trusted-occurrence-partition-substitution",
                        "proof": "trusted occurrence partition transported through exact parent-boundary occurrence equivalences",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "partition_substitution": substitution,
                        },
                    }
                    break

            elif target.get("type") == "value_constraint":
                for source in facts:
                    lift = _trusted_child_value_lift(
                        target,
                        source,
                        handoff=handoff,
                        model=model,
                    )
                    if lift is None:
                        continue
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "trusted-child-value-lift",
                        "proof": "trusted child value constraint lifted through an exact parent-local signal alias",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "value_lift": lift,
                        },
                    }
                    break

            elif target.get("type") == "forbid_when":
                for source in facts:
                    if source.kind != "forbid_when":
                        continue
                    if source.formal.get("predicate") != target.get("predicate"):
                        continue
                    occurrence_bridge = bridge(str(target.get("occurrence")), str(source.formal.get("occurrence")))
                    if occurrence_bridge is None:
                        continue
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "trusted-child-lift",
                        "proof": "trusted forbid theorem lifted across an exact parent-local occurrence bridge",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "source_theorem": source.certificate,
                            "occurrence_bridge": occurrence_bridge,
                        },
                    }
                    break

            elif target.get("type") == "ordered_before":
                # After-side restriction: X < Y and Z is a subset of Y imply
                # X < Z.  This is the dual of before-side weakening below.
                for source in facts:
                    if source.kind != "ordered_before" or source.formal.get("before") != target.get("before"):
                        continue
                    projection = None
                    if not _same_scope(source.formal, target):
                        if target.get("scope_index") is not None:
                            continue
                        projection = _index_projection_certificate(source, imported_occurrences)
                        if projection is None:
                            continue
                    occurrence_bridge = bridge(str(target.get("after")), str(source.formal.get("after")))
                    if occurrence_bridge is None:
                        continue
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "trusted-history-after-restriction",
                        "proof": "trusted history theorem restricted to an exact parent-local subset of its after occurrence",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "history_theorem": source.certificate,
                            "occurrence_bridge": occurrence_bridge,
                            "index_projection": projection,
                        },
                    }
                    break

                # History weakening: A < C and A is a subset of B imply B < C.
                for source in facts if proof is None else []:
                    if source.kind != "ordered_before" or source.formal.get("after") != target.get("after"):
                        continue
                    if target.get("scope_index") is not None or source.formal.get("scope_index") is not None:
                        continue
                    occurrence_bridge = bridge(str(source.formal.get("before")), str(target.get("before")))
                    if occurrence_bridge is None:
                        continue
                    proof = {
                        "status": FORMALLY_PROVED,
                        "backend": "composition-prover",
                        "proof_method": "occurrence-bridge-history-composition",
                        "proof": "local history theorem weakened through an exact occurrence inclusion bridge",
                        "certificate": {
                            "prover": COMPOSITION_PROVER_VERSION,
                            "history_theorem": source.certificate,
                            "occurrence_bridge": occurrence_bridge,
                        },
                    }
                    break

                # Transitivity, optionally erasing a matched same-index witness.
                if proof is None:
                    for left in facts:
                        if left.kind != "ordered_before" or left.formal.get("before") != target.get("before"):
                            continue
                        for right in facts:
                            if right.kind != "ordered_before":
                                continue
                            if left.formal.get("after") != right.formal.get("before"):
                                continue
                            if right.formal.get("after") != target.get("after"):
                                continue
                            projection = None
                            if _same_scope(left.formal, target):
                                if not _same_scope(right.formal, target):
                                    continue
                            elif target.get("scope_index") is None and right.formal.get("scope_index") is None:
                                projection = _index_projection_certificate(left, imported_occurrences)
                                if projection is None:
                                    continue
                            else:
                                continue
                            proof = {
                                "status": FORMALLY_PROVED,
                                "backend": "composition-prover",
                                "proof_method": "trusted-history-transitivity",
                                "proof": "history order composed transitively over trusted theorem premises",
                                "certificate": {
                                    "prover": COMPOSITION_PROVER_VERSION,
                                    "left_theorem": left.certificate,
                                    "right_theorem": right.certificate,
                                    "index_projection": projection,
                                },
                            }
                            break
                        if proof is not None:
                            break

            if proof is None:
                continue
            proof["provenance"] = derive_composition_provenance(proof)
            proved[axiom_id] = proof
            fact = _theorem(target, axiom_id, {
                "kind": "composed-theorem",
                "axiom_id": axiom_id,
                "proof_method": proof["proof_method"],
                "certificate": proof["certificate"],
            })
            if fact is not None:
                facts.append(fact)
            del targets[axiom_id]
            progress = True
    return proved
