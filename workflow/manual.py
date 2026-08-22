from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .schema import UMCM_SCHEMA_VERSION, parse_candidate_response
from .axiom_ir import compile_formal_axiom, expr_index_vars, expr_signals, validate_formal_expr_shape
from .composition import prompt_semantic_catalog, public_boundary_event_ids
from .tasks import PromptPackage
from .research_memory import initialize_experience, write_run_summary
from .formal_patterns import declared_signal_type_from_handoff


PENDING = "PENDING_MANUAL_LLM"
GROUNDING_VALID = "GROUNDING_VALID"
REFINEMENT_NEEDED = "REFINEMENT_NEEDED"


_INDEX_REF_RE = re.compile(r"\[([^\]]+)\]")
_SIMPLE_INDEX_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_.$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*)*$"
)


def _parent_prompt_minor(task: dict[str, Any]) -> int | None:
    match = re.fullmatch(r"parent-synthesis-prompt-0\.(\d+)", str(task.get("prompt_version", "")))
    return int(match.group(1)) if match else None


def _uses_compact_parent_interface(task: dict[str, Any]) -> bool:
    minor = _parent_prompt_minor(task)
    return task.get("kind") == "parent_synthesis" and minor is not None and minor >= 3


def _requires_explicit_public_interface(task: dict[str, Any]) -> bool:
    minor = _parent_prompt_minor(task)
    return task.get("kind") == "parent_synthesis" and minor is not None and minor >= 4


def _is_allowed_signal_reference(
    signal: str,
    allowed_signals: set[str],
    handoff: dict[str, Any] | None = None,
) -> bool:
    """Accept exact signals and grounded dynamic selections of compacted arrays.

    The frontend deliberately compacts a read such as ``valids[deq_ptr]`` to
    ``valids[*]`` in dependency summaries.  A candidate may retain the exact
    FIRRTL selection only when the wildcarded array path and every symbolic
    index are independently present in the WorkUnit grounding universe.
    """

    if signal in allowed_signals:
        return True
    if handoff is not None and declared_signal_type_from_handoff(handoff, signal) is not None:
        return True
    # FIRRTL aggregate connects/reads are often preserved in the handoff as an
    # aggregate root (for example ``connect dst.d, src.d``), while a µMCM
    # payload axiom necessarily names one of its leaf fields.  An exact
    # aggregate grounding therefore authorizes its dot-selected descendants;
    # it does not authorize siblings of that aggregate.
    if any(signal.startswith(root + ".") for root in allowed_signals):
        return True
    indices = _INDEX_REF_RE.findall(signal)
    if not indices:
        return False
    wildcard = _INDEX_REF_RE.sub("[*]", signal)
    if wildcard not in allowed_signals:
        return False
    for index in indices:
        text = index.strip()
        if text.isdigit():
            continue
        if not _SIMPLE_INDEX_RE.fullmatch(text) or text not in allowed_signals:
            return False
    return True


@dataclass(frozen=True)
class ManualImportResult:
    candidate: dict[str, Any]
    validation: dict[str, Any]
    status: str


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def export_manual_task(package: PromptPackage, run_root: str | Path) -> Path:
    root = Path(run_root).expanduser()
    task_dir = root / package.task.task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    _write_json(task_dir / "task.json", package.task.to_dict())
    _write_json(task_dir / "static_handoff.json", package.static_handoff)
    _write_json(task_dir / "expected_output_schema.json", package.expected_output_schema)
    (task_dir / "prompt.md").write_text(package.prompt, encoding="utf-8")
    _write_json(
        task_dir / "status.json",
        {
            "status": PENDING,
            "task_id": package.task.task_id,
            "next_action": "Send prompt.md to a ChatGPT conversation, converge on a candidate, then import the final response.",
        },
    )
    initialize_experience(task_dir)
    write_run_summary(task_dir)
    return task_dir


def _duplicates(items: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return sorted(duplicates)


def _all_evidence(candidate: dict[str, Any]) -> list[tuple[str, int]]:
    refs: list[tuple[str, int]] = []
    for field in (
        "occurrences",
        "predicates",
        "identity_keys",
        "cases",
        "axioms",
        "assumptions",
        "unresolved",
    ):
        for item in candidate.get(field, []):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id", "<missing-id>")
            for statement_id in item.get("evidence_statement_ids", []):
                if isinstance(statement_id, int):
                    refs.append((f"{field}:{item_id}", statement_id))
    return refs


def _id_set(candidate: dict[str, Any], field: str) -> set[str]:
    return {
        item["id"]
        for item in candidate.get(field, [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _validate_parent_public_interface(
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    parent_ext: dict[str, Any],
    *,
    errors: list[str],
    warnings: list[str],
) -> None:
    interface = parent_ext.get("public_interface")
    if not isinstance(interface, dict):
        errors.append("extensions.parent_synthesis.public_interface must be an object")
        return
    allowed_fields = {
        "policy",
        "exported_axiom_ids",
        "exported_occurrence_ids",
        "exported_predicate_ids",
        "exported_identity_ids",
        "boundary_coverage",
    }
    extra_fields = sorted(set(interface) - allowed_fields)
    if extra_fields:
        errors.append(f"public_interface has unsupported fields: {extra_fields}")
    if interface.get("policy") != "explicit-public-contract-v0.1":
        errors.append("public_interface.policy must be 'explicit-public-contract-v0.1'")

    declared_fields = {
        "exported_axiom_ids": _id_set(candidate, "axioms"),
        "exported_occurrence_ids": _id_set(candidate, "occurrences"),
        "exported_predicate_ids": _id_set(candidate, "predicates"),
        "exported_identity_ids": _id_set(candidate, "identity_keys"),
    }
    exports: dict[str, set[str]] = {}
    for field, available in declared_fields.items():
        values = interface.get(field)
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            errors.append(f"public_interface.{field} must be a string list")
            values = []
        elif len(values) != len(set(values)):
            errors.append(f"public_interface.{field} must contain unique IDs")
        exports[field] = {str(item) for item in values}
        unknown = sorted(exports[field] - available)
        if unknown:
            errors.append(f"public_interface.{field} references unknown local IDs: {unknown}")
        qualified = sorted(item for item in exports[field] if "::" in item)
        if qualified:
            errors.append(
                f"public_interface.{field} must contain parent-local IDs, not imported IDs: {qualified}"
            )

    public_occurrences = exports["exported_occurrence_ids"]
    public_predicates = exports["exported_predicate_ids"]
    public_identities = exports["exported_identity_ids"]
    public_axioms = exports["exported_axiom_ids"]
    axioms_by_id = {
        str(item["id"]): item
        for item in candidate.get("axioms", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    compiled_public: dict[str, dict[str, Any]] = {}
    for axiom_id in sorted(public_axioms):
        axiom = axioms_by_id.get(axiom_id)
        formal = axiom.get("formal") if isinstance(axiom, dict) else None
        if not isinstance(formal, dict):
            continue
        try:
            compiled = compile_formal_axiom(formal)
        except ValueError:
            continue
        compiled_public[axiom_id] = compiled
        refs = compiled["references"]
        hidden = {
            "occurrences": sorted(set(refs.get("occurrences", [])) - public_occurrences),
            "predicates": sorted(set(refs.get("predicates", [])) - public_predicates),
            "identities": sorted(set(refs.get("identities", [])) - public_identities),
        }
        hidden = {kind: values for kind, values in hidden.items() if values}
        if hidden:
            errors.append(
                f"public axiom {axiom_id!r} is not interface-closed; references non-public objects: {hidden}"
            )

    coverage = interface.get("boundary_coverage")
    if not isinstance(coverage, list):
        errors.append("public_interface.boundary_coverage must be a list")
        coverage = []
    required_events = set(public_boundary_event_ids(handoff))
    occurrences_by_id = {
        str(item["id"]): item
        for item in candidate.get("occurrences", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    seen_events: set[str] = set()
    for index, entry in enumerate(coverage):
        label = f"public_interface.boundary_coverage[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        allowed_entry_fields = {
            "physical_event_id", "status", "occurrence_ids", "axiom_ids", "note"
        }
        extra = sorted(set(entry) - allowed_entry_fields)
        if extra:
            errors.append(f"{label} has unsupported fields: {extra}")
        event_id = entry.get("physical_event_id")
        if not isinstance(event_id, str):
            errors.append(f"{label}.physical_event_id must be a string")
            continue
        if event_id in seen_events:
            errors.append(f"public boundary event {event_id!r} is classified more than once")
        seen_events.add(event_id)
        if event_id not in required_events:
            errors.append(f"{label} references non-public boundary event {event_id!r}")
        status = entry.get("status")
        if status not in {"constrained", "event_only", "intentionally_omitted"}:
            errors.append(
                f"{label}.status must be constrained, event_only, or intentionally_omitted"
            )
        occurrence_ids = entry.get("occurrence_ids")
        axiom_ids = entry.get("axiom_ids")
        if not isinstance(occurrence_ids, list) or not all(
            isinstance(item, str) for item in occurrence_ids
        ):
            errors.append(f"{label}.occurrence_ids must be a string list")
            occurrence_ids = []
        if not isinstance(axiom_ids, list) or not all(isinstance(item, str) for item in axiom_ids):
            errors.append(f"{label}.axiom_ids must be a string list")
            axiom_ids = []
        if len(occurrence_ids) != len(set(occurrence_ids)):
            errors.append(f"{label}.occurrence_ids must contain unique IDs")
        if len(axiom_ids) != len(set(axiom_ids)):
            errors.append(f"{label}.axiom_ids must contain unique IDs")
        unknown_occurrences = sorted(set(occurrence_ids) - public_occurrences)
        unknown_axioms = sorted(set(axiom_ids) - public_axioms)
        if unknown_occurrences:
            errors.append(f"{label} references non-public occurrences: {unknown_occurrences}")
        if unknown_axioms:
            errors.append(f"{label} references non-public axioms: {unknown_axioms}")
        for occurrence_id in occurrence_ids:
            occurrence = occurrences_by_id.get(occurrence_id)
            if isinstance(occurrence, dict) and event_id not in occurrence.get("physical_event_ids", []):
                errors.append(
                    f"{label} occurrence {occurrence_id!r} is not grounded in {event_id!r}"
                )
        if status == "constrained":
            if not occurrence_ids or not axiom_ids:
                errors.append(f"{label} constrained coverage needs occurrence_ids and axiom_ids")
            for axiom_id in axiom_ids:
                refs = compiled_public.get(axiom_id, {}).get("references", {})
                if occurrence_ids and not (set(occurrence_ids) & set(refs.get("occurrences", []))):
                    errors.append(
                        f"{label} axiom {axiom_id!r} does not constrain a listed occurrence"
                    )
        elif status == "event_only":
            if not occurrence_ids or axiom_ids:
                errors.append(f"{label} event_only coverage needs occurrences and no axioms")
        elif status == "intentionally_omitted":
            if occurrence_ids or axiom_ids:
                errors.append(f"{label} intentionally_omitted coverage must not cite objects")
        if status in {"event_only", "intentionally_omitted"} and not str(entry.get("note", "")).strip():
            errors.append(f"{label} {status} coverage requires a non-empty note")

    missing_events = sorted(required_events - seen_events)
    if missing_events:
        errors.append(f"public_interface.boundary_coverage misses public events: {missing_events}")
    if required_events and not public_axioms:
        warnings.append(
            "public interface exports no axioms; all boundary behavior is event-only or omitted"
        )


def validate_candidate_grounding(
    candidate: dict[str, Any],
    task: dict[str, Any],
    handoff: dict[str, Any],
) -> dict[str, Any]:
    """Fail-closed deterministic grounding checks for µMCM v0.2.

    This is intentionally not semantic proof.  It verifies that every concrete
    reference belongs to the WorkUnit and that occurrence/predicate/case/axiom
    references are internally well formed before a property compiler is run.
    """

    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "schema_version",
        "task_id",
        "work_unit_id",
        "occurrences",
        "predicates",
        "identity_keys",
        "cases",
        "axioms",
        "assumptions",
        "unresolved",
        "rationale",
        "extensions",
    ]
    for field in required:
        if field not in candidate:
            errors.append(f"missing top-level field: {field}")

    if candidate.get("schema_version") != UMCM_SCHEMA_VERSION:
        errors.append(
            f"schema_version mismatch: {candidate.get('schema_version')!r} != {UMCM_SCHEMA_VERSION!r}"
        )
    if candidate.get("task_id") != task.get("task_id"):
        errors.append("task_id does not match task.json")
    if candidate.get("work_unit_id") != handoff["work_unit"]["id"]:
        errors.append("work_unit_id does not match static_handoff.json")

    list_fields = [
        "occurrences",
        "predicates",
        "identity_keys",
        "cases",
        "axioms",
        "assumptions",
        "unresolved",
    ]
    for field in list_fields:
        value = candidate.get(field, [])
        if not isinstance(value, list):
            errors.append(f"{field} must be a list")
            continue
        duplicates = _duplicates(value)
        if duplicates:
            errors.append(f"duplicate IDs in {field}: {duplicates}")

    allowed_statements = set(handoff["grounding"]["allowed_statement_ids"])
    for owner, statement_id in _all_evidence(candidate):
        if statement_id not in allowed_statements:
            errors.append(
                f"{owner} cites statement {statement_id}, which is outside this WorkUnit"
            )

    allowed_events = set(handoff["grounding"]["allowed_physical_event_ids"])
    allowed_state = set(handoff["grounding"]["allowed_state_ids"])
    allowed_signals = {
        entry["id"] for entry in handoff.get("frontier", []) if isinstance(entry, dict)
    }
    # Physical boundary events are authoritative grounding objects. Their
    # valid/ready and leaf payload paths remain legal even when logical FIRRTL
    # compaction records an aggregate read such as ``io.in[0].bits``.
    for event in handoff.get("events", []):
        if not isinstance(event, dict):
            continue
        allowed_signals.update(
            signal
            for signal in (event.get("valid"), event.get("ready"))
            if isinstance(signal, str)
        )
        allowed_signals.update(
            signal for signal in event.get("payload", []) if isinstance(signal, str)
        )
    for statement in handoff.get("statements", []):
        if not isinstance(statement, dict):
            continue
        allowed_signals.update(statement.get("drives", []))
        allowed_signals.update(statement.get("reads", []))

    imported_occurrence_ids = set(
        handoff.get("grounding", {}).get("imported_occurrence_ids", [])
    )
    imported_predicate_ids = set(
        handoff.get("grounding", {}).get("imported_predicate_ids", [])
    )
    imported_identity_ids = set(
        handoff.get("grounding", {}).get("imported_identity_ids", [])
    )
    imported_case_ids = set(
        handoff.get("grounding", {}).get("imported_case_ids", [])
    )
    imported_axiom_ids = set(
        handoff.get("grounding", {}).get("imported_axiom_ids", [])
    )
    # Parent prompt v0.3 deliberately exposes a non-recursive child contract.
    # Keep the validator's legal imported namespace identical to what the LLM
    # could actually see, while retaining the full catalog in static_handoff for
    # the composition prover and for backward compatibility with older tasks.
    if _uses_compact_parent_interface(task):
        visible = prompt_semantic_catalog(handoff)
        imported_occurrence_ids = visible["occurrences"]
        imported_predicate_ids = visible["predicates"]
        imported_identity_ids = visible["identity_keys"]
        imported_case_ids = set()
        imported_axiom_ids = visible["axioms"]

    local_occurrence_ids = _id_set(candidate, "occurrences")
    local_predicate_ids = _id_set(candidate, "predicates")
    local_identity_ids = _id_set(candidate, "identity_keys")
    local_case_ids = _id_set(candidate, "cases")

    for field, local_ids, imported_ids in (
        ("occurrences", local_occurrence_ids, imported_occurrence_ids),
        ("predicates", local_predicate_ids, imported_predicate_ids),
        ("identity_keys", local_identity_ids, imported_identity_ids),
        ("cases", local_case_ids, imported_case_ids),
    ):
        shadowed = sorted(local_ids & imported_ids)
        if shadowed:
            errors.append(
                f"{field} redeclare imported child semantic IDs: {shadowed}"
            )

    occurrence_ids = local_occurrence_ids | imported_occurrence_ids
    predicate_ids = local_predicate_ids | imported_predicate_ids
    identity_ids = local_identity_ids | imported_identity_ids
    case_ids = local_case_ids | imported_case_ids

    for occurrence in candidate.get("occurrences", []):
        if not isinstance(occurrence, dict):
            errors.append("occurrences entries must be objects")
            continue
        index = occurrence.get("index")
        if index is not None:
            if not isinstance(index, dict):
                errors.append(f"occurrence {occurrence.get('id')!r} index must be an object or null")
            else:
                expr = index.get("expr")
                shape_errors = validate_formal_expr_shape(expr, f"occurrence {occurrence.get('id')!r}.index.expr")
                errors.extend(shape_errors)
                if not shape_errors:
                    for signal in sorted(expr_signals(expr)):
                        if not _is_allowed_signal_reference(signal, allowed_signals, handoff):
                            errors.append(f"occurrence {occurrence.get('id')!r} index references unknown signal {signal!r}")
                domain = index.get("domain")
                if isinstance(domain, dict):
                    start, end = domain.get("start"), domain.get("end_exclusive")
                    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
                        errors.append(f"occurrence {occurrence.get('id')!r} index domain is invalid")
        occurrence_id = occurrence.get("id")
        kind = occurrence.get("kind")
        physical = occurrence.get("physical_event_ids", [])
        if not isinstance(physical, list):
            errors.append(f"occurrence {occurrence_id!r} physical_event_ids must be a list")
            physical = []
        for physical_id in physical:
            if physical_id not in allowed_events:
                errors.append(
                    f"occurrence {occurrence_id!r} references unknown physical event {physical_id!r}"
                )
        if kind == "boundary" and not physical:
            errors.append(f"boundary occurrence {occurrence_id!r} has no physical_event_ids")
        if kind == "derived":
            grounding = occurrence.get("grounding", {})
            has_filter = isinstance(grounding, dict) and bool(
                grounding.get("signals_true")
                or grounding.get("signals_false")
                or grounding.get("state_values")
                or grounding.get("value_tests")
            )
            if physical and not has_filter:
                warnings.append(
                    f"derived occurrence {occurrence_id!r} also references physical events; consider boundary kind if no internal milestone is needed"
                )
            if not occurrence.get("definition"):
                errors.append(f"derived occurrence {occurrence_id!r} has no definition")
            if not occurrence.get("evidence_statement_ids"):
                errors.append(f"derived occurrence {occurrence_id!r} has no statement evidence")
            if not isinstance(grounding, dict) or not (
                grounding.get("state_values")
                or grounding.get("signals_true")
                or grounding.get("signals_false")
                or grounding.get("value_tests")
            ):
                errors.append(
                    f"derived occurrence {occurrence_id!r} needs concrete state/signal grounding"
                )
        grounding = occurrence.get("grounding", {})
        if isinstance(grounding, dict):
            state_register = grounding.get("state_register")
            if state_register is not None and state_register not in allowed_state:
                errors.append(
                    f"occurrence {occurrence_id!r} references unknown state register {state_register!r}"
                )
            for signal in grounding.get("signals_true", []) + grounding.get("signals_false", []):
                if not _is_allowed_signal_reference(signal, allowed_signals, handoff):
                    errors.append(
                        f"occurrence {occurrence_id!r} references unknown signal {signal!r}"
                    )
            value_tests = grounding.get("value_tests", [])
            if not isinstance(value_tests, list):
                errors.append(f"occurrence {occurrence_id!r} value_tests must be a list")
            else:
                for index, test in enumerate(value_tests):
                    if not isinstance(test, dict):
                        errors.append(f"occurrence {occurrence_id!r} value_tests[{index}] must be an object")
                        continue
                    expr = test.get("expr")
                    shape_errors = validate_formal_expr_shape(
                        expr,
                        f"occurrence {occurrence_id!r}.value_tests[{index}].expr",
                    )
                    errors.extend(shape_errors)
                    if not shape_errors:
                        for signal in sorted(expr_signals(expr)):
                            if not _is_allowed_signal_reference(signal, allowed_signals, handoff):
                                errors.append(
                                    f"occurrence {occurrence_id!r} value test references unknown signal {signal!r}"
                                )
                    if test.get("relation") not in {"eq", "neq"}:
                        errors.append(
                            f"occurrence {occurrence_id!r} value_tests[{index}] relation must be 'eq' or 'neq'"
                        )
                    if not isinstance(test.get("value"), int) or int(test["value"]) < 0:
                        errors.append(
                            f"occurrence {occurrence_id!r} value_tests[{index}] value must be a non-negative integer"
                        )

    for predicate in candidate.get("predicates", []):
        if not isinstance(predicate, dict):
            errors.append("predicates entries must be objects")
            continue
        predicate_id = predicate.get("id")
        grounding = predicate.get("grounding", {})
        if not isinstance(grounding, dict):
            errors.append(f"predicate {predicate_id!r} grounding must be an object")
            continue
        source_signal = grounding.get("source_signal")
        state_register = grounding.get("state_register")
        if source_signal is not None and not _is_allowed_signal_reference(source_signal, allowed_signals, handoff):
            errors.append(
                f"predicate {predicate_id!r} references unknown source signal {source_signal!r}"
            )
        if state_register is not None and state_register not in allowed_state:
            errors.append(
                f"predicate {predicate_id!r} references unknown state register {state_register!r}"
            )
        if source_signal is None and not grounding.get("state_values"):
            warnings.append(
                f"predicate {predicate_id!r} has no machine-checkable source signal/state set; semantic validation may be UNKNOWN"
            )

    for identity in candidate.get("identity_keys", []):
        if not isinstance(identity, dict):
            errors.append("identity_keys entries must be objects")
            continue
        identity_id = identity.get("id")
        carrier = identity.get("carrier_state")
        if carrier not in allowed_state:
            errors.append(
                f"identity {identity_id!r} references unknown carrier state {carrier!r}"
            )

    for case in candidate.get("cases", []):
        if not isinstance(case, dict):
            errors.append("cases entries must be objects")
            continue
        case_id = case.get("id")
        for ref in case.get("trigger_occurrences", []):
            if ref not in occurrence_ids:
                errors.append(f"case {case_id!r} references undefined occurrence {ref!r}")
        for ref in case.get("emits", []):
            if ref not in occurrence_ids:
                errors.append(f"case {case_id!r} emits undefined occurrence {ref!r}")
        for guard in case.get("guard_predicates", []):
            if not isinstance(guard, dict) or guard.get("id") not in predicate_ids:
                errors.append(
                    f"case {case_id!r} references undefined predicate {guard.get('id') if isinstance(guard, dict) else guard!r}"
                )

    if task.get("kind") == "parent_synthesis":
        composition = handoff.get("composition", {})
        child_summaries = (
            composition.get("child_summaries", [])
            if isinstance(composition, dict)
            else []
        )
        if not child_summaries:
            errors.append("parent_synthesis task has no frozen child summaries")

        extensions = candidate.get("extensions", {})
        parent_ext = (
            extensions.get("parent_synthesis", {})
            if isinstance(extensions, dict)
            else {}
        )
        if _requires_explicit_public_interface(task) or (
            isinstance(parent_ext, dict) and "public_interface" in parent_ext
        ):
            if isinstance(parent_ext, dict):
                _validate_parent_public_interface(
                    candidate,
                    handoff,
                    parent_ext,
                    errors=errors,
                    warnings=warnings,
                )
            else:
                errors.append("extensions.parent_synthesis must be an object")
        provenance = (
            parent_ext.get("axiom_provenance", {})
            if isinstance(parent_ext, dict)
            else {}
        )
        if not isinstance(provenance, dict):
            errors.append(
                "extensions.parent_synthesis.axiom_provenance must be an object"
            )
            provenance = {}

        candidate_axiom_ids = _id_set(candidate, "axioms")
        missing_provenance = sorted(candidate_axiom_ids - set(provenance))
        extra_provenance = sorted(set(provenance) - candidate_axiom_ids)
        if missing_provenance:
            errors.append(
                f"parent axioms missing provenance entries: {missing_provenance}"
            )
        if extra_provenance:
            errors.append(
                f"parent provenance references unknown candidate axioms: {extra_provenance}"
            )

        for axiom_id, entry in provenance.items():
            if not isinstance(entry, dict):
                errors.append(
                    f"parent provenance for axiom {axiom_id!r} must be an object"
                )
                continue
            kind = entry.get("kind")
            if kind not in {"parent_local", "reexported", "lifted", "emergent"}:
                errors.append(
                    f"parent provenance for axiom {axiom_id!r} has invalid kind {kind!r}"
                )
            source_axioms = entry.get("source_axioms", [])
            if not isinstance(source_axioms, list) or not all(
                isinstance(item, str) for item in source_axioms
            ):
                errors.append(
                    f"parent provenance for axiom {axiom_id!r} source_axioms must be a string list"
                )
                source_axioms = []
            unknown_sources = sorted(set(source_axioms) - imported_axiom_ids)
            if unknown_sources:
                errors.append(
                    f"parent provenance for axiom {axiom_id!r} references unknown imported "
                    f"axioms: {unknown_sources}"
                )
            if kind in {"reexported", "lifted", "emergent"} and not source_axioms:
                errors.append(
                    f"parent provenance for {kind} axiom {axiom_id!r} must cite source_axioms"
                )
            if not isinstance(entry.get("note", ""), str):
                errors.append(
                    f"parent provenance for axiom {axiom_id!r} note must be a string"
                )

    for axiom in candidate.get("axioms", []):
        if not isinstance(axiom, dict):
            errors.append("axioms entries must be objects")
            continue
        axiom_id = axiom.get("id")
        allowed_axiom_fields = {"id", "formal", "derived_from_case_ids", "evidence_statement_ids", "status"}
        for extra in sorted(set(axiom) - allowed_axiom_fields):
            errors.append(f"axiom {axiom_id!r} has unsupported legacy/extra field {extra!r}")
        if axiom.get("status") != "candidate":
            errors.append(f"axiom {axiom_id!r} status must be 'candidate'")
        for case_id in axiom.get("derived_from_case_ids", []):
            if case_id not in case_ids:
                errors.append(f"axiom {axiom_id!r} references undefined case {case_id!r}")
        formal = axiom.get("formal")
        if not isinstance(formal, dict):
            errors.append(f"axiom {axiom_id!r} has no formal AST")
            continue
        try:
            compiled = compile_formal_axiom(formal)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"axiom {axiom_id!r} formal AST is invalid/unsupported: {exc}")
            continue
        refs = compiled["references"]
        for ref in refs.get("occurrences", []):
            if ref not in occurrence_ids:
                errors.append(f"axiom {axiom_id!r} references undefined occurrence {ref!r}")
        for ref in refs.get("predicates", []):
            if ref not in predicate_ids:
                errors.append(f"axiom {axiom_id!r} references undefined predicate {ref!r}")
        for ref in refs.get("identities", []):
            if ref not in identity_ids:
                errors.append(f"axiom {axiom_id!r} references undefined identity {ref!r}")
        for signal in refs.get("signals", []):
            if not _is_allowed_signal_reference(signal, allowed_signals, handoff):
                errors.append(f"axiom {axiom_id!r} references unknown signal {signal!r}")

        scope_index = formal.get("scope_index")
        if scope_index:
            index_name = scope_index.get("name")
            referenced = refs.get("occurrences", [])
            by_id = {item.get("id"): item for item in candidate.get("occurrences", []) if isinstance(item, dict)}
            formal_type = formal.get("type")
            if formal_type in {"ordered_before", "ordered_chain", "exclusion", "join", "forbid_when"}:
                for occurrence_id in referenced:
                    occurrence = by_id.get(occurrence_id, {})
                    index = occurrence.get("index")
                    if not isinstance(index, dict) or index.get("name") != index_name:
                        errors.append(
                            f"axiom {axiom_id!r} scope_index {index_name!r} requires indexed occurrence "
                            f"{occurrence_id!r} with the same index name"
                        )
            elif formal_type in {"signal_equality", "value_constraint", "spec_relation"}:
                on = formal.get("on")
                if on:
                    occurrence = by_id.get(on, {})
                    index = occurrence.get("index")
                    if not isinstance(index, dict) or index.get("name") != index_name:
                        errors.append(
                            f"axiom {axiom_id!r} scope_index {index_name!r} requires indexed trigger "
                            f"{on!r} with the same index name"
                        )
            expression_vars = set()
            if formal_type == "signal_equality":
                expression_vars.update(expr_index_vars(formal.get("source", {})))
            elif formal_type == "value_constraint":
                expression_vars.update(expr_index_vars(formal.get("expr", {})))
            unknown_vars = expression_vars - {index_name}
            if unknown_vars:
                errors.append(
                    f"axiom {axiom_id!r} uses index variables outside scope_index {index_name!r}: "
                    f"{sorted(unknown_vars)}"
                )

        if formal.get("type") == "identity_flow":
            identity = next((x for x in candidate.get("identity_keys", []) if x.get("id") == formal.get("identity")), None)
            capture = formal.get("capture", {})
            if identity is not None and capture.get("carrier") != identity.get("carrier_state"):
                errors.append(
                    f"axiom {axiom_id!r} capture carrier {capture.get('carrier')!r} does not match identity carrier {identity.get('carrier_state')!r}"
                )
        if formal.get("type") == "indexed_storage_flow":
            storage = formal.get("storage")
            if storage not in set(handoff.get("memory_state", [])):
                errors.append(
                    f"axiom {axiom_id!r} references unknown storage object {storage!r}"
                )
            lane = formal.get("key", {}).get("lane", {})
            lane_name = lane.get("name") if isinstance(lane, dict) else None
            expressions = []
            for owner, fields in (
                (formal.get("write", {}), ("address", "lane_mask")),
                (formal.get("read", {}), ("address",)),
                (formal.get("initialization", {}), ("active", "address", "lane_mask")),
            ):
                if isinstance(owner, dict):
                    expressions.extend(owner.get(field) for field in fields)
            for field in formal.get("value_fields", []):
                if not isinstance(field, dict):
                    continue
                expressions.extend([field.get("write_value"), field.get("initial_value")])
                expressions.extend(field.get("read_targets", []))
            variables = {
                variable
                for expression in expressions
                if isinstance(expression, dict)
                for variable in expr_index_vars(expression)
            }
            unknown = variables - ({str(lane_name)} if lane_name else set())
            if unknown:
                errors.append(
                    f"axiom {axiom_id!r} indexed_storage_flow uses unbound index variables: "
                    f"{sorted(unknown)}"
                )
        if formal.get("type") == "indexed_priority_select":
            index = formal.get("index", {})
            index_name = index.get("name") if isinstance(index, dict) else None
            expressions = [formal.get("candidate")]
            priority = formal.get("priority", {})
            if isinstance(priority, dict):
                expressions.append(priority.get("pivot"))
            variables = {
                variable
                for expression in expressions
                if isinstance(expression, dict)
                for variable in expr_index_vars(expression)
            }
            unknown = variables - ({str(index_name)} if index_name else set())
            if unknown:
                errors.append(
                    f"axiom {axiom_id!r} indexed_priority_select uses unbound index variables: "
                    f"{sorted(unknown)}"
                )


    unit = handoff.get("work_unit", {})
    certified_empty_shape = bool(
        isinstance(unit, dict)
        and unit.get("is_leaf")
        and unit.get("coverage_complete")
        and not any(
            candidate.get(field)
            for field in (
                "occurrences",
                "predicates",
                "identity_keys",
                "cases",
                "axioms",
                "assumptions",
                "unresolved",
            )
        )
        and any(
            isinstance(item, str) and item.strip()
            for item in candidate.get("rationale", [])
        )
    )
    if not candidate.get("axioms") and not candidate.get("unresolved") and not certified_empty_shape:
        warnings.append(
            "candidate has neither axioms nor unresolved questions; likely not useful for semantic validation"
        )

    return {
        "validator": "deterministic-grounding-0.8",
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "semantic_proof_performed": False,
        "next_validator": "formal-axiom-compiler-0.13/semantic-validator-0.23 + formal-backend-api-0.23",
    }


def import_manual_response(task_dir: str | Path, response_text: str) -> ManualImportResult:
    directory = Path(task_dir)
    task = json.loads((directory / "task.json").read_text(encoding="utf-8"))
    handoff = json.loads((directory / "static_handoff.json").read_text(encoding="utf-8"))

    candidate = parse_candidate_response(response_text)
    validation = validate_candidate_grounding(candidate, task, handoff)
    status = GROUNDING_VALID if validation["valid"] else REFINEMENT_NEEDED

    (directory / "response_raw.md").write_text(response_text, encoding="utf-8")
    _write_json(directory / "response_parsed.json", candidate)
    _write_json(directory / "validation.json", validation)
    _write_json(
        directory / "status.json",
        {
            "status": status,
            "task_id": task["task_id"],
            "next_action": (
                "Run `mcm-agent semantic-validate <task_dir>`; grounding is complete, but no axiom is trusted until formal proof."
                if validation["valid"]
                else "Return validation.json to the conversation and refine the candidate."
            ),
        },
    )
    write_run_summary(directory)
    return ManualImportResult(candidate=candidate, validation=validation, status=status)
