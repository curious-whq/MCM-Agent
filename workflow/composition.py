from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


FROZEN_STATUS = "FROZEN_FOR_COMPOSITION"
SEMANTIC_FIELDS = (
    "occurrences",
    "predicates",
    "identity_keys",
    "cases",
    "axioms",
)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return value


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _concrete_suffix(value: Any) -> Any:
    if not isinstance(value, str) or "::" not in value:
        return value
    return value.split("::", 1)[1]


def work_unit_implementation_sha256(handoff: dict[str, Any]) -> str:
    """Hash the instance-independent RTL/proof scope of one WorkUnit.

    Instance paths, source locations, task metadata, and composition artifacts
    are excluded.  Local FIRRTL, state/interface shape, event definitions, and
    child summary-slot shape are retained.  Consequently two concrete slots can
    share a theorem template only when their implementation-facing handoffs are
    structurally identical.
    """

    unit = handoff.get("work_unit", {})
    payload = {
        "schema": "workunit-implementation-fingerprint-v0.1",
        "module": unit.get("module"),
        "kind": unit.get("kind"),
        "is_leaf": unit.get("is_leaf"),
        "statements": [
            {
                key: statement.get(key)
                for key in ("kind", "text", "status", "drives", "reads", "control_reads", "note")
            }
            for statement in handoff.get("statements", [])
            if isinstance(statement, dict)
        ],
        "dependency_edges": sorted(
            (
                str(edge.get("src", "")),
                str(edge.get("dst", "")),
                str(edge.get("kind", "")),
            )
            for edge in handoff.get("dependency_edges", [])
            if isinstance(edge, dict)
        ),
        "state": sorted(
            (
                str(item.get("id", "")),
                str(item.get("kind", "")),
                str(item.get("type", "")),
            )
            for item in handoff.get("state", [])
            if isinstance(item, dict)
        ),
        "memory_state": sorted(str(item) for item in handoff.get("memory_state", [])),
        "frontier": sorted(
            (
                str(item.get("id", "")),
                str(item.get("kind", "")),
                str(item.get("type", "")),
            )
            for item in handoff.get("frontier", [])
            if isinstance(item, dict)
        ),
        "events": sorted(
            (
                str(event.get("registry_id", "")),
                _concrete_suffix(event.get("id")),
                str(event.get("channel", "")),
                str(event.get("direction", "")),
                str(event.get("protocol", "")),
                str(event.get("predicate", "")),
                str(event.get("valid", "")),
                str(event.get("ready", "")),
                tuple(event.get("payload", [])),
            )
            for event in handoff.get("events", [])
            if isinstance(event, dict)
        ),
        "children": sorted(
            (
                str(child.get("child_kind", "")),
                tuple(sorted(_concrete_suffix(item) for item in child.get("boundary_events", []))),
                tuple(sorted(str(item) for item in child.get("frontier_signals", []))),
            )
            for child in handoff.get("children", [])
            if isinstance(child, dict)
        ),
        "semantic_event_cones": sorted(
            (
                _concrete_suffix(cone.get("event_id")),
                tuple(sorted(str(item) for item in cone.get("historical_registers", []))),
                tuple(sorted(str(item) for item in cone.get("immediate_registers", []))),
                tuple(sorted(str(item) for item in cone.get("immediate_frontier", []))),
                bool(cone.get("complete")),
            )
            for cone in handoff.get("semantic_event_cones", [])
            if isinstance(cone, dict)
        ),
    }
    return _canonical_sha256(payload)


def _rewrite_instance_prefix(value: Any, source: str, target: str) -> Any:
    if isinstance(value, dict):
        return {
            _rewrite_instance_prefix(key, source, target): _rewrite_instance_prefix(item, source, target)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_rewrite_instance_prefix(item, source, target) for item in value]
    if not isinstance(value, str):
        return value
    if value == source or value.startswith(source + "::") or value.startswith(source + "."):
        return target + value[len(source):]
    return value


def _rehash_instantiated_imports(frozen: dict[str, Any]) -> None:
    composition = frozen.get("composition")
    if not isinstance(composition, dict):
        return
    for imported in composition.get("imports", []):
        if not isinstance(imported, dict):
            continue
        child_frozen = imported.get("frozen_umcm")
        if not isinstance(child_frozen, dict):
            continue
        _rehash_instantiated_imports(child_frozen)
        imported["frozen_umcm_sha256"] = _canonical_sha256(child_frozen)


def instantiate_frozen_umcm(
    frozen: dict[str, Any],
    *,
    source_work_unit_id: str,
    target_work_unit_id: str,
) -> dict[str, Any]:
    """Instantiate one frozen theorem template at a concrete instance path."""

    instantiated = _rewrite_instance_prefix(
        deepcopy(frozen),
        source_work_unit_id,
        target_work_unit_id,
    )
    if not isinstance(instantiated, dict):
        raise ValueError("instantiated frozen µMCM is not an object")
    instantiated["work_unit_id"] = target_work_unit_id
    _rehash_instantiated_imports(instantiated)
    return instantiated


def _empty_catalog() -> dict[str, dict[str, dict[str, str]]]:
    return {field: {} for field in SEMANTIC_FIELDS}


def merge_semantic_catalogs(
    *catalogs: dict[str, Any],
) -> dict[str, dict[str, dict[str, str]]]:
    merged = _empty_catalog()
    for catalog in catalogs:
        if not isinstance(catalog, dict):
            continue
        for field in SEMANTIC_FIELDS:
            entries = catalog.get(field, {})
            if not isinstance(entries, dict):
                continue
            for qualified_id, origin in entries.items():
                if not isinstance(qualified_id, str) or not isinstance(origin, dict):
                    continue
                previous = merged[field].get(qualified_id)
                normalized = {
                    "work_unit_id": str(origin.get("work_unit_id", "")),
                    "local_id": str(origin.get("local_id", "")),
                }
                if previous is not None and previous != normalized:
                    raise ValueError(
                        f"semantic catalog collision for {field}:{qualified_id}"
                    )
                merged[field][qualified_id] = normalized
    return merged


def semantic_catalog_from_frozen(
    frozen: dict[str, Any],
    *,
    work_unit_id: str | None = None,
) -> dict[str, dict[str, dict[str, str]]]:
    """Return transitive semantic names exported by one frozen summary."""

    unit_id = work_unit_id or str(frozen.get("work_unit_id", ""))
    if not unit_id:
        raise ValueError("frozen µMCM has no work_unit_id")

    inherited = (
        frozen.get("composition", {}).get("semantic_catalog", {})
        if isinstance(frozen.get("composition"), dict)
        else {}
    )
    local = _empty_catalog()
    for field in SEMANTIC_FIELDS:
        values = frozen.get(field, [])
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            local_id = item["id"]
            qualified_id = f"{unit_id}::{local_id}"
            local[field][qualified_id] = {
                "work_unit_id": unit_id,
                "local_id": local_id,
            }
    return merge_semantic_catalogs(inherited, local)


def _load_frozen_record(task_dir: Path) -> dict[str, Any] | None:
    task_path = task_dir / "task.json"
    status_path = task_dir / "status.json"
    frozen_path = task_dir / "frozen_umcm.json"
    if not (task_path.is_file() and status_path.is_file() and frozen_path.is_file()):
        return None

    task = _read_json(task_path)
    status = _read_json(status_path)
    frozen = _read_json(frozen_path)
    static_handoff_path = task_dir / "static_handoff.json"
    static_handoff = _read_json(static_handoff_path) if static_handoff_path.is_file() else None
    if status.get("status") != FROZEN_STATUS:
        return None
    if frozen.get("freeze", {}).get("status") != FROZEN_STATUS:
        return None
    if task.get("work_unit_id") != frozen.get("work_unit_id"):
        raise ValueError(
            f"{task_dir} task/frozen WorkUnit mismatch: "
            f"{task.get('work_unit_id')!r} != {frozen.get('work_unit_id')!r}"
        )
    return {
        "task_dir": task_dir,
        "task": task,
        "status": status,
        "frozen": frozen,
        "static_handoff": static_handoff,
        "implementation_sha256": (
            work_unit_implementation_sha256(static_handoff)
            if isinstance(static_handoff, dict)
            else None
        ),
    }


def _discover_frozen_records(run_roots: Iterable[str | Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for raw_root in run_roots:
        root = Path(raw_root).expanduser()
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            record = _load_frozen_record(child)
            if record is not None:
                records.append(record)
    return records


def _template_compatible(
    record: dict[str, Any],
    slot: dict[str, Any],
    implementation_catalog: dict[str, Any],
) -> bool:
    handoff = record.get("static_handoff")
    if not isinstance(handoff, dict):
        return False
    source_unit = handoff.get("work_unit", {})
    source_id = str(record.get("task", {}).get("work_unit_id", ""))
    source_module = str(source_unit.get("module", ""))
    source_current = implementation_catalog.get(source_module, {})
    target_structural = slot.get("structural_implementation_sha256")
    return bool(
        slot.get("child_kind") == "module"
        and source_module
        and target_structural
        and source_unit.get("kind") == "module"
        and source_unit.get("id") == source_id == source_module
        and source_unit.get("instance_path") == source_module
        and source_current.get("proof_scope_sha256") == record.get("implementation_sha256")
        and source_current.get("structural_implementation_sha256") == target_structural
    )


def _record_matches_exact_slot(record: dict[str, Any], slot: dict[str, Any]) -> bool:
    source_id = str(record.get("task", {}).get("work_unit_id", ""))
    if source_id != str(slot.get("child_id", "")):
        return False
    expected = slot.get("implementation_sha256")
    actual = record.get("implementation_sha256")
    # Preserve compatibility with legacy exact-instance artifacts that predate
    # fingerprints; module-template reuse never takes this fallback.
    return not expected or not actual or expected == actual


def attach_frozen_child_summaries(
    handoff: dict[str, Any],
    *,
    run_roots: Iterable[str | Path],
    child_task_dirs: Iterable[str | Path] = (),
) -> dict[str, Any]:
    """Attach exactly one frozen summary for every direct child slot."""

    if handoff.get("work_unit", {}).get("is_leaf"):
        raise ValueError("parent synthesis requires a non-leaf WorkUnit")

    slots = handoff.get("children", [])
    if not isinstance(slots, list) or not slots:
        raise ValueError("parent synthesis WorkUnit has no child summary slots")

    direct_child_ids = {
        str(slot.get("child_id"))
        for slot in slots
        if isinstance(slot, dict) and slot.get("child_id")
    }
    if len(direct_child_ids) != len(slots):
        raise ValueError("parent child slots contain missing/duplicate child ids")
    implementation_catalog = handoff.get("implementation_catalog", {})
    if not isinstance(implementation_catalog, dict):
        implementation_catalog = {}

    slot_by_id = {str(slot["child_id"]): slot for slot in slots}
    explicit: dict[str, dict[str, Any]] = {}
    explicit_templates: list[dict[str, Any]] = []
    for raw in child_task_dirs:
        directory = Path(raw).expanduser()
        record = _load_frozen_record(directory)
        if record is None:
            raise ValueError(
                f"explicit child task dir {directory} is not FROZEN_FOR_COMPOSITION"
            )
        child_id = str(record["task"].get("work_unit_id", ""))
        if child_id in direct_child_ids:
            if not _record_matches_exact_slot(record, slot_by_id[child_id]):
                raise ValueError(
                    f"explicit child task {directory} implementation fingerprint "
                    f"does not match direct child {child_id!r}"
                )
            if child_id in explicit:
                raise ValueError(f"multiple explicit frozen task dirs for child {child_id!r}")
            explicit[child_id] = record
            continue
        compatible = [
            slot for slot in slots
            if _template_compatible(record, slot, implementation_catalog)
        ]
        if not compatible:
            raise ValueError(
                f"explicit child task {directory} belongs to {child_id!r}, "
                "and is not an implementation-equivalent module theorem template "
                f"for any direct child {sorted(direct_child_ids)}"
            )
        explicit_templates.append(record)

    discovered = _discover_frozen_records(run_roots)
    by_child: dict[str, list[dict[str, Any]]] = {}
    for record in discovered:
        child_id = str(record["task"].get("work_unit_id", ""))
        if child_id in direct_child_ids and _record_matches_exact_slot(record, slot_by_id[child_id]):
            by_child.setdefault(child_id, []).append(record)

    summaries: list[dict[str, Any]] = []
    imported_catalogs: list[dict[str, Any]] = []
    imported_boundary_events: set[str] = set()

    for slot in slots:
        child_id = str(slot["child_id"])
        reused_template = False
        if child_id in explicit:
            record = explicit[child_id]
        else:
            matches = by_child.get(child_id, [])
            if len(matches) > 1:
                choices = [str(item["task_dir"]) for item in matches]
                raise ValueError(
                    f"multiple frozen child µMCM runs found for {child_id!r}: "
                    f"{choices}. Pass the intended --child-task-dir explicitly."
                )
            if matches:
                record = matches[0]
            else:
                template_matches = [
                    item for item in explicit_templates
                    if _template_compatible(item, slot, implementation_catalog)
                ]
                if not template_matches:
                    template_matches = [
                        item for item in discovered
                        if _template_compatible(item, slot, implementation_catalog)
                    ]
                # Discovery may see the same explicit directory through run_roots.
                unique_templates = {
                    Path(item["task_dir"]).resolve(): item for item in template_matches
                }
                template_matches = list(unique_templates.values())
                if not template_matches:
                    module = slot.get("child_module")
                    fingerprint = slot.get("implementation_sha256")
                    raise ValueError(
                        f"no frozen child µMCM found for {child_id!r}, and no "
                        "implementation-equivalent module theorem template is available "
                        f"(module={module!r}, implementation_sha256={fingerprint!r})"
                    )
                if len(template_matches) > 1:
                    choices = [str(item["task_dir"]) for item in template_matches]
                    raise ValueError(
                        f"multiple implementation-equivalent module theorem templates "
                        f"found for {child_id!r}: {choices}. Pass one --child-task-dir explicitly."
                    )
                record = template_matches[0]
                reused_template = True

        source_unit_id = str(record["task"].get("work_unit_id", ""))
        template_frozen = record["frozen"]
        frozen = (
            instantiate_frozen_umcm(
                template_frozen,
                source_work_unit_id=source_unit_id,
                target_work_unit_id=child_id,
            )
            if reused_template
            else template_frozen
        )
        catalog = semantic_catalog_from_frozen(
            frozen,
            work_unit_id=child_id,
        )
        imported_catalogs.append(catalog)
        boundary_events = [
            str(x) for x in slot.get("boundary_events", [])
            if isinstance(x, str)
        ]
        imported_boundary_events.update(boundary_events)

        summaries.append(
            {
                "child_id": child_id,
                "child_kind": slot.get("child_kind"),
                "summary_ref": slot.get("summary_ref"),
                "boundary_events": boundary_events,
                "frontier_signals": list(slot.get("frontier_signals", [])),
                "task_id": record["task"].get("task_id"),
                "task_dir": str(record["task_dir"]),
                "frozen_umcm_sha256": _canonical_sha256(frozen),
                "template_frozen_umcm_sha256": _canonical_sha256(template_frozen),
                "implementation_sha256": slot.get("implementation_sha256"),
                "instance_reuse": {
                    "kind": "module-theorem-template-instantiation" if reused_template else "exact-work-unit",
                    "source_work_unit_id": source_unit_id,
                    "target_work_unit_id": child_id,
                    "module": slot.get("child_module"),
                    "implementation_sha256": slot.get("implementation_sha256"),
                    "structural_implementation_sha256": slot.get("structural_implementation_sha256"),
                    "source_module": (
                        record.get("static_handoff", {}).get("work_unit", {}).get("module")
                        if isinstance(record.get("static_handoff"), dict)
                        else None
                    ),
                    "verification": (
                        "source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1"
                        if reused_template
                        else "exact-work-unit-id"
                    ),
                },
                "semantic_catalog": catalog,
                "frozen_umcm": frozen,
            }
        )

    imported = merge_semantic_catalogs(*imported_catalogs)
    result = deepcopy(handoff)
    result["composition"] = {
        "mode": "parent_synthesis",
        "policy": "frozen-direct-children-with-verified-module-instance-reuse-v0.2",
        "child_summaries": summaries,
        "semantic_catalog": imported,
    }

    grounding = result.setdefault("grounding", {})
    allowed_events = set(grounding.get("allowed_physical_event_ids", []))
    allowed_events.update(imported_boundary_events)
    grounding["allowed_physical_event_ids"] = sorted(allowed_events)
    grounding["imported_boundary_event_ids"] = sorted(imported_boundary_events)
    grounding["imported_occurrence_ids"] = sorted(imported["occurrences"])
    grounding["imported_predicate_ids"] = sorted(imported["predicates"])
    grounding["imported_identity_ids"] = sorted(imported["identity_keys"])
    grounding["imported_case_ids"] = sorted(imported["cases"])
    grounding["imported_axiom_ids"] = sorted(imported["axioms"])
    return result
