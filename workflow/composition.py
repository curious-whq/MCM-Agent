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

    explicit: dict[str, dict[str, Any]] = {}
    for raw in child_task_dirs:
        directory = Path(raw).expanduser()
        record = _load_frozen_record(directory)
        if record is None:
            raise ValueError(
                f"explicit child task dir {directory} is not FROZEN_FOR_COMPOSITION"
            )
        child_id = str(record["task"].get("work_unit_id", ""))
        if child_id not in direct_child_ids:
            raise ValueError(
                f"explicit child task {directory} belongs to {child_id!r}, "
                f"not one of direct children {sorted(direct_child_ids)}"
            )
        if child_id in explicit:
            raise ValueError(f"multiple explicit frozen task dirs for child {child_id!r}")
        explicit[child_id] = record

    discovered = _discover_frozen_records(run_roots)
    by_child: dict[str, list[dict[str, Any]]] = {}
    for record in discovered:
        child_id = str(record["task"].get("work_unit_id", ""))
        if child_id in direct_child_ids:
            by_child.setdefault(child_id, []).append(record)

    summaries: list[dict[str, Any]] = []
    imported_catalogs: list[dict[str, Any]] = []
    imported_boundary_events: set[str] = set()

    for slot in slots:
        child_id = str(slot["child_id"])
        if child_id in explicit:
            record = explicit[child_id]
        else:
            matches = by_child.get(child_id, [])
            if not matches:
                raise ValueError(
                    f"no frozen child µMCM found for {child_id!r}; "
                    "freeze the child first or pass --child-task-dir"
                )
            if len(matches) > 1:
                choices = [str(item["task_dir"]) for item in matches]
                raise ValueError(
                    f"multiple frozen child µMCM runs found for {child_id!r}: "
                    f"{choices}. Pass the intended --child-task-dir explicitly."
                )
            record = matches[0]

        frozen = record["frozen"]
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
                "semantic_catalog": catalog,
                "frozen_umcm": frozen,
            }
        )

    imported = merge_semantic_catalogs(*imported_catalogs)
    result = deepcopy(handoff)
    result["composition"] = {
        "mode": "parent_synthesis",
        "policy": "frozen-direct-children-no-child-rtl-v0.1",
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
