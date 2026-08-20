from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .composition import FROZEN_STATUS, _canonical_sha256
from .formal_patterns import (
    _and,
    _bool_expr,
    _bool_refs,
    _const,
    _not,
    _occurrence_condition,
    _or,
    _propagate_bool_refs,
    _unsat,
    _writer_activation,
)
from .semantic import FORMALLY_PROVED, SPEC_PROVED, HandoffControlModel, _statement_rhs


COMPOSITION_PROVER_VERSION = "composition-prover-0.1"


@dataclass(frozen=True)
class Theorem:
    kind: str
    formal: dict[str, Any]
    source_id: str
    certificate: dict[str, Any]


def _qualify(unit_id: str, object_id: Any) -> Any:
    if not isinstance(object_id, str) or "::" in object_id:
        return object_id
    return f"{unit_id}::{object_id}"


def _qualified_formal(unit_id: str, formal: dict[str, Any]) -> dict[str, Any]:
    result = dict(formal)
    for key in ("occurrence", "before", "after", "required_prior", "predicate"):
        if result.get(key) is not None:
            result[key] = _qualify(unit_id, result[key])
    return result


def _theorem(formal: dict[str, Any], source_id: str, certificate: dict[str, Any]) -> Theorem | None:
    kind = str(formal.get("type", ""))
    if kind not in {"forbid_when", "ordered_before"}:
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


def _effective_signal_condition(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    signal: str,
) -> tuple[tuple[Any, ...], dict[str, Any]] | None:
    refs = _bool_refs(model, candidate)
    writers = [
        statement
        for statement in model.statements.values()
        if signal in {str(item) for item in statement.get("drives", [])}
        and statement.get("kind") not in {"node", "reg", "regreset", "when"}
    ]
    if not writers:
        expr = _bool_expr(model, refs | {signal}, signal, opaque={signal})
        return None if expr is None else (expr, {"signal": signal, "kind": "frontier-input"})

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

    signal_proofs = []
    for signal in signals:
        effective = _effective_signal_condition(model, candidate, signal)
        if effective is None:
            return None
        condition, certificate = effective
        implied, _ = _unsat(_and(source, _not(condition)))
        if implied is not True:
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

    progress = True
    while progress:
        progress = False
        for axiom_id, result in list(targets.items()):
            axiom = next((x for x in candidate.get("axioms", []) if x.get("id") == axiom_id), None)
            target = axiom.get("formal") if isinstance(axiom, dict) else None
            if not isinstance(target, dict):
                continue

            proof: dict[str, Any] | None = None
            if target.get("type") == "forbid_when":
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
                # History weakening: A < C and A is a subset of B imply B < C.
                for source in facts:
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
