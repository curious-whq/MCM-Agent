from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from frontend.pipeline import StaticFrontend
from frontend.workunit import (
    WorkUnitConfig,
    build_hierarchical_work_unit,
    flatten_work_units,
    module_structural_sha256,
)

from .handoff import build_work_unit_static_handoff
from .manual import export_manual_task, import_manual_response
from .tasks import build_leaf_abstraction_task, build_parent_synthesis_task
from .composition import attach_frozen_child_summaries, work_unit_implementation_sha256
from .semantic import validate_task_dir
from .research_memory import write_current_handoff, write_run_summary


def _load(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _add_root_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--root-instance")
    group.add_argument("--root-module")
    parser.add_argument(
        "--unit-id",
        help=(
            "select a leaf from the recursive tree; defaults to the selected root"
        ),
    )


def _select_unit(root, unit_id: str | None):
    if unit_id is None:
        return root
    matches = [unit for unit in flatten_work_units(root) if unit.id == unit_id]
    if not matches:
        available = [unit.id for unit in flatten_work_units(root) if not unit.children]
        preview = "\n  ".join(available[:20])
        raise ValueError(
            f"Unknown WorkUnit {unit_id!r}. First leaf IDs include:\n  {preview}"
        )
    return matches[0]


def _leaf_task(args: argparse.Namespace) -> dict:
    text = _load(args.firrtl)
    frontend = StaticFrontend.from_firrtl(text, eager=len(text) < 8_000_000)
    root = build_hierarchical_work_unit(
        frontend.design,
        frontend.graph,
        frontend.registries,
        root_instance=args.root_instance,
        root_module=args.root_module,
        config=WorkUnitConfig(),
    )
    unit = _select_unit(root, args.unit_id)
    if unit.children:
        leaves = [child.id for child in flatten_work_units(unit) if not child.children]
        raise ValueError(
            f"Leaf abstraction requires a leaf WorkUnit; {unit.id!r} has children. "
            f"Select --unit-id from: {leaves[:20]}"
        )

    graph = frontend.graph(unit.module)
    registry = frontend.registries[unit.module]
    handoff = build_work_unit_static_handoff(
        unit,
        graph,
        registry,
        source_roots=args.source_root,
        context_lines=args.context_lines,
    )
    package = build_leaf_abstraction_task(handoff)
    task_dir = export_manual_task(package, args.run_root)
    return {
        "status": "PENDING_MANUAL_LLM",
        "task_id": package.task.task_id,
        "work_unit_id": unit.id,
        "task_dir": str(task_dir),
        "prompt": str(task_dir / "prompt.md"),
        "static_handoff": str(task_dir / "static_handoff.json"),
        "expected_output_schema": str(task_dir / "expected_output_schema.json"),
        "next_action": "Send prompt.md to the current or a new ChatGPT conversation.",
    }


def _implementation_fingerprint_cache_key(child) -> tuple[str, str, str]:
    kind = child.kind.value
    return (child.module, kind, "" if kind == "module" else child.id)



def _parent_task(args: argparse.Namespace) -> dict:
    text = _load(args.firrtl)
    frontend = StaticFrontend.from_firrtl(text, eager=len(text) < 8_000_000)
    root = build_hierarchical_work_unit(
        frontend.design,
        frontend.graph,
        frontend.registries,
        root_instance=args.root_instance,
        root_module=args.root_module,
        config=WorkUnitConfig(),
    )
    unit = _select_unit(root, args.unit_id)
    if not unit.children:
        raise ValueError(
            f"Parent synthesis requires a non-leaf WorkUnit; {unit.id!r} is a leaf"
        )

    graph = frontend.graph(unit.module)
    registry = frontend.registries[unit.module]
    handoff = build_work_unit_static_handoff(
        unit,
        graph,
        registry,
        source_roots=args.source_root,
        context_lines=args.context_lines,
    )
    slot_by_id = {
        str(slot.get("child_id")): slot
        for slot in handoff.get("children", [])
        if isinstance(slot, dict) and slot.get("child_id")
    }
    # Module instance WorkUnits with the same implementation may share one
    # instance-independent fingerprint. Region WorkUnits from the same module
    # own different statement/state/event slices and must never share the
    # first region's cached fingerprint.
    implementation_cache: dict[tuple[str, str, str], str] = {}
    structural_cache: dict[str, str] = {}
    implementation_catalog: dict[str, dict[str, str]] = {}
    for child in unit.children:
        slot = slot_by_id.get(child.id)
        if slot is None or child.module not in frontend.registries:
            continue
        cache_key = _implementation_fingerprint_cache_key(child)
        fingerprint = implementation_cache.get(cache_key)
        if fingerprint is None:
            child_handoff = build_work_unit_static_handoff(
                child,
                frontend.graph(child.module),
                frontend.registries[child.module],
            )
            fingerprint = work_unit_implementation_sha256(child_handoff)
            implementation_cache[cache_key] = fingerprint
        slot["child_module"] = child.module
        slot["implementation_sha256"] = fingerprint
        if child.kind.value == "module":
            structural = module_structural_sha256(
                frontend.design,
                frontend.graph,
                child.module,
                _cache=structural_cache,
            )
            slot["structural_implementation_sha256"] = structural
            implementation_catalog[child.module] = {
                "proof_scope_sha256": fingerprint,
                "structural_implementation_sha256": structural,
            }
    handoff["implementation_catalog"] = implementation_catalog
    child_run_roots = args.child_run_root or [args.run_root]
    handoff = attach_frozen_child_summaries(
        handoff,
        run_roots=child_run_roots,
        child_task_dirs=args.child_task_dir,
    )
    package = build_parent_synthesis_task(handoff)
    task_dir = export_manual_task(package, args.run_root)
    return {
        "status": "PENDING_MANUAL_LLM",
        "task_id": package.task.task_id,
        "work_unit_id": unit.id,
        "task_dir": str(task_dir),
        "prompt": str(task_dir / "prompt.md"),
        "static_handoff": str(task_dir / "static_handoff.json"),
        "expected_output_schema": str(task_dir / "expected_output_schema.json"),
        "children": [
            {
                "child_id": child.get("child_id"),
                "task_id": child.get("task_id"),
                "frozen_umcm_sha256": child.get("frozen_umcm_sha256"),
            }
            for child in handoff.get("composition", {}).get("child_summaries", [])
        ],
        "next_action": (
            "Send parent prompt.md to the LLM. Child RTL has been replaced by "
            "frozen child µMCM summaries."
        ),
    }


def _manual_import(args: argparse.Namespace) -> dict:
    if args.response == "-":
        response_text = sys.stdin.read()
    else:
        response_text = Path(args.response).read_text(encoding="utf-8")
    result = import_manual_response(args.task_dir, response_text)
    return {
        "status": result.status,
        "valid": result.validation["valid"],
        "errors": result.validation["errors"],
        "warnings": result.validation["warnings"],
        "validation": str(Path(args.task_dir) / "validation.json"),
        "candidate": str(Path(args.task_dir) / "response_parsed.json"),
    }



def _semantic_validate(args: argparse.Namespace) -> dict:
    semantic = validate_task_dir(args.task_dir, formal_backend=args.formal_backend)
    status_path = Path(args.task_dir) / "status.json"
    workflow_status = json.loads(status_path.read_text(encoding="utf-8"))["status"]
    return {
        "status": workflow_status,
        "counts": semantic["counts"],
        "candidate_axiom_count": semantic["candidate_axiom_count"],
        "trusted_axiom_count": semantic["trusted_axiom_count"],
        "all_axioms_structurally_supported": semantic["all_axioms_structurally_supported"],
        "all_axioms_formally_proved": semantic["all_axioms_formally_proved"],
        "has_counterexample": semantic["has_counterexample"],
        "semantic_validation": str(Path(args.task_dir) / "semantic_validation.json"),
        "property_obligations": str(Path(args.task_dir) / "property_obligations.json"),
        "trusted_umcm": str(Path(args.task_dir) / "trusted_umcm.json"),
    }


def _freeze(args: argparse.Namespace) -> dict:
    from .semantic import freeze_task_dir
    frozen = freeze_task_dir(args.task_dir)
    return {
        "status": "FROZEN_FOR_COMPOSITION",
        "trusted_axiom_count": len(frozen.get("axioms", [])),
        "frozen_umcm": str(Path(args.task_dir) / "frozen_umcm.json"),
    }


def _run_summary(args: argparse.Namespace) -> dict:
    path = write_run_summary(args.task_dir)
    return {
        "status": "SUMMARY_UPDATED",
        "task_dir": str(Path(args.task_dir)),
        "summary": str(path),
    }


def _handoff(args: argparse.Namespace) -> dict:
    path = write_current_handoff(
        args.repo_root,
        output=args.output,
        run_roots=args.run_root,
        task_dirs=args.task_dir,
        max_runs=args.max_runs,
    )
    return {
        "status": "HANDOFF_UPDATED",
        "handoff": str(path),
        "next_action": (
            "In a fresh conversation, upload/paste this handoff first; if an LLM task is pending, "
            "also upload/paste that task's prompt.md."
        ),
    }

def _status(args: argparse.Namespace) -> dict:
    directory = Path(args.task_dir)
    return json.loads((directory / "status.json").read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcm-agent",
        description=(
            "Manual-first µMCM workflow. Static/prompt/validation stages are real; "
            "LLM generation is currently supplied through a conversation."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    leaf = sub.add_parser(
        "leaf-task",
        help="export a self-contained manual LeafAbstractionTask",
    )
    leaf.add_argument("firrtl")
    _add_root_args(leaf)
    leaf.add_argument("--source-root", action="append", default=[])
    leaf.add_argument("--context-lines", type=int, default=1)
    leaf.add_argument("--run-root", default="runs")

    parent = sub.add_parser(
        "parent-task",
        help="export a self-contained parent synthesis task using frozen direct children",
    )
    parent.add_argument("firrtl")
    _add_root_args(parent)
    parent.add_argument("--source-root", action="append", default=[])
    parent.add_argument("--context-lines", type=int, default=1)
    parent.add_argument("--run-root", default="runs")
    parent.add_argument(
        "--child-run-root",
        action="append",
        default=[],
        help="search root for frozen direct-child runs; defaults to --run-root",
    )
    parent.add_argument(
        "--child-task-dir",
        action="append",
        default=[],
        help="explicit frozen direct-child task dir; repeat to disambiguate children",
    )

    manual_import = sub.add_parser(
        "manual-import",
        help="import the final JSON result from a manual ChatGPT conversation",
    )
    manual_import.add_argument("task_dir")
    manual_import.add_argument(
        "response",
        help="response markdown/JSON file, or '-' to read stdin",
    )

    semantic = sub.add_parser(
        "semantic-validate",
        help="compile grounded axioms, collect structural evidence, and invoke a formal backend",
    )
    semantic.add_argument("task_dir")
    semantic.add_argument(
        "--formal-backend",
        default="none",
        help="formal backend; bundled values: none, explicit-control",
    )


    freeze = sub.add_parser(
        "freeze",
        help="freeze a fully proved leaf µMCM for parent composition",
    )
    freeze.add_argument("task_dir")


    summary = sub.add_parser(
        "run-summary",
        help="refresh the durable SUMMARY.md for one workflow run",
    )
    summary.add_argument("task_dir")

    handoff = sub.add_parser(
        "handoff",
        help="generate a self-contained cross-conversation CURRENT_HANDOFF.md",
    )
    handoff.add_argument("--repo-root", default=".")
    handoff.add_argument("--run-root", action="append", default=["runs"])
    handoff.add_argument("--task-dir", action="append", default=[])
    handoff.add_argument("--max-runs", type=int, default=12)
    handoff.add_argument(
        "--output",
        default="docs/research/CURRENT_HANDOFF.md",
        help="output path, relative to --repo-root unless absolute",
    )

    status = sub.add_parser("status", help="show workflow status for one task")
    status.add_argument("task_dir")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "leaf-task":
            output = _leaf_task(args)
        elif args.command == "parent-task":
            output = _parent_task(args)
        elif args.command == "manual-import":
            output = _manual_import(args)
        elif args.command == "semantic-validate":
            output = _semantic_validate(args)
        elif args.command == "freeze":
            output = _freeze(args)
        elif args.command == "run-summary":
            output = _run_summary(args)
        elif args.command == "handoff":
            output = _handoff(args)
        elif args.command == "status":
            output = _status(args)
        else:  # pragma: no cover
            raise AssertionError(args.command)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
