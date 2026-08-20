from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Iterable

from .axiom_ir import render_formal_axiom


RESEARCH_DOCS = (
    "GOAL.md",
    "METHOD.md",
    "DECISIONS.md",
    "LESSONS.md",
    "ROADMAP_3W.md",
    "STATUS.md",
)

EXPERIENCE_TEMPLATE = """# Experiment Experience\n\nKeep only lessons that should survive this conversation. Delete empty bullets instead of inventing content.\n\n## INPUT_NEEDED\n\n- \n\n## PROMPT_RULE\n\n- \n\n## SCHEMA_CHANGE\n\n- \n\n## VALIDATOR_CHANGE\n\n- \n\n## MODEL_FAILURE\n\n- \n\n## GENERALIZATION\n\n- \n"""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _short(text: str, limit: int = 180) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def initialize_experience(task_dir: str | Path) -> Path:
    directory = Path(task_dir)
    path = directory / "EXPERIENCE.md"
    if not path.exists():
        path.write_text(EXPERIENCE_TEMPLATE, encoding="utf-8")
    return path


def _validation_levels(semantic: dict[str, Any]) -> dict[str, str]:
    return {
        str(result.get("axiom_id")): str(result.get("validation_level", "UNKNOWN"))
        for result in semantic.get("results", [])
        if result.get("axiom_id")
    }


def build_run_summary(task_dir: str | Path) -> str:
    directory = Path(task_dir)
    task = _load_json(directory / "task.json")
    status = _load_json(directory / "status.json")
    candidate = _load_json(directory / "response_parsed.json")
    semantic = _load_json(directory / "semantic_validation.json")
    trusted = _load_json(directory / "trusted_umcm.json")
    grounding = _load_json(directory / "validation.json")

    work_unit_id = task.get("work_unit_id") or candidate.get("work_unit_id") or directory.name
    lines = [f"# Run Summary — {work_unit_id}", ""]
    lines.extend(
        [
            "## Identity",
            "",
            f"- task: `{task.get('task_id', directory.name)}`",
            f"- kind: `{task.get('kind', 'unknown')}`",
            f"- workflow: `{task.get('workflow_version', 'unknown')}`",
            f"- prompt: `{task.get('prompt_version', 'unknown')}`",
            f"- schema: `{task.get('schema_version', candidate.get('schema_version', 'unknown'))}`",
            f"- workflow status: `{status.get('status', 'UNKNOWN')}`",
            "",
        ]
    )

    if grounding:
        lines.extend(
            [
                "## Grounding",
                "",
                f"- valid: `{grounding.get('valid', False)}`",
                f"- errors: {len(grounding.get('errors', []))}",
                f"- warnings: {len(grounding.get('warnings', []))}",
                "",
            ]
        )

    if candidate:
        lines.extend(
            [
                "## Candidate µMCM",
                "",
                f"- occurrences: {len(candidate.get('occurrences', []))}",
                f"- predicates: {len(candidate.get('predicates', []))}",
                f"- identity keys: {len(candidate.get('identity_keys', []))}",
                f"- cases: {len(candidate.get('cases', []))}",
                f"- candidate axioms: {len(candidate.get('axioms', []))}",
                f"- unresolved: {len(candidate.get('unresolved', []))}",
                "",
            ]
        )

    if semantic:
        counts = semantic.get("counts", {})
        lines.extend(["## Validation", ""])
        for level in (
            "GROUNDED",
            "PARTIALLY_SUPPORTED",
            "STRUCTURALLY_SUPPORTED",
            "FORMALLY_PROVED",
            "SPEC_PROVED",
            "REFUTED",
        ):
            if level in counts:
                lines.append(f"- {level}: {counts[level]}")
        lines.extend(
            [
                f"- trusted axioms: {semantic.get('trusted_axiom_count', len(trusted.get('axioms', [])))}",
                f"- formal backend: `{semantic.get('formal_backend', {}).get('name', 'unknown')}`",
                "",
            ]
        )

    levels = _validation_levels(semantic)
    if candidate.get("axioms"):
        lines.extend(["## Axioms", ""])
        for axiom in candidate.get("axioms", []):
            axiom_id = axiom.get("id", "<missing>")
            level = levels.get(str(axiom_id), "NOT_VALIDATED")
            formula = _short(render_formal_axiom(axiom.get("formal", {})), 220)
            lines.append(f"- `{axiom_id}` [{level}] {formula}")
        lines.append("")

    unresolved = candidate.get("unresolved", [])
    if unresolved:
        lines.extend(["## Unresolved", ""])
        for item in unresolved:
            lines.append(f"- `{item.get('id', '<missing>')}` {_short(item.get('question', ''), 220)}")
        lines.append("")

    next_action = status.get("next_action")
    lines.extend(["## Next action", ""])
    lines.append(next_action or "No next action recorded yet.")
    lines.extend(
        [
            "",
            "## Durable experiment notes",
            "",
            "See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.",
            "",
        ]
    )
    return "\n".join(lines)


def write_run_summary(task_dir: str | Path) -> Path:
    directory = Path(task_dir)
    initialize_experience(directory)
    path = directory / "SUMMARY.md"
    path.write_text(build_run_summary(directory), encoding="utf-8")
    return path


def _repo_version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists():
        return "unknown"
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else "unknown"


def _discover_task_dirs(run_roots: Iterable[str | Path]) -> list[Path]:
    found: dict[str, Path] = {}
    for root_value in run_roots:
        root = Path(root_value).expanduser()
        if not root.exists():
            continue
        if (root / "task.json").exists():
            found[str(root.resolve())] = root
            continue
        # Task directories are expected one level below a run root. Keep this
        # bounded so a repository-wide handoff cannot accidentally crawl a huge tree.
        for task_file in root.glob("*/task.json"):
            task_dir = task_file.parent
            found[str(task_dir.resolve())] = task_dir
    return sorted(found.values(), key=lambda p: p.stat().st_mtime, reverse=True)


def _read_research_doc(repo_root: Path, name: str) -> str:
    path = repo_root / "docs" / "research" / name
    if not path.exists():
        return f"# Missing {name}\n\nThis research-memory file has not been created."
    return path.read_text(encoding="utf-8").strip()


def build_current_handoff(
    repo_root: str | Path,
    *,
    run_roots: Iterable[str | Path] = (),
    task_dirs: Iterable[str | Path] = (),
    max_runs: int = 12,
) -> str:
    repo = Path(repo_root).expanduser().resolve()
    discovered = _discover_task_dirs(run_roots)
    for task_dir in task_dirs:
        path = Path(task_dir).expanduser()
        if (path / "task.json").exists() and all(path.resolve() != x.resolve() for x in discovered):
            discovered.append(path)
    discovered.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    discovered = discovered[:max_runs]

    lines = [
        "# MCM-Agent Current Handoff",
        "",
        "> This file is intentionally self-contained. In a fresh conversation, upload/paste this file first, then upload the current task `prompt.md` if the next action is an LLM/manual semantic task.",
        "",
        "## Resume instruction for a new conversation",
        "",
        "Continue the MCM-Agent project from this handoff. Treat the recorded design decisions as established unless new RTL/formal evidence contradicts them. Do not restart partition design. Follow the Current Status and Next Action, and preserve new durable lessons back into the repository/run memory files.",
        "",
        f"Repository version: `{_repo_version(repo)}`",
        "",
    ]

    for name in RESEARCH_DOCS:
        title = name.removesuffix(".md").replace("_", " ").title()
        lines.extend([f"---\n\n## {title}\n", _read_research_doc(repo, name), ""])

    lines.extend(["---", "", "## Recent WorkUnit Runs", ""])
    if not discovered:
        lines.append("No run directories were supplied/discovered. Use `--run-root` or `--task-dir` when generating this handoff.")
        lines.append("")
    for task_dir in discovered:
        write_run_summary(task_dir)
        summary = (task_dir / "SUMMARY.md").read_text(encoding="utf-8").strip()
        experience = initialize_experience(task_dir).read_text(encoding="utf-8").strip()
        lines.extend(
            [
                f"### Run: `{task_dir.name}`",
                "",
                summary,
                "",
                "### Experiment experience",
                "",
                experience,
                "",
            ]
        )

    lines.extend(
        [
            "---",
            "",
            "## New-conversation operating rule",
            "",
            "1. Read this handoff before analyzing a new WorkUnit.",
            "2. If a WorkUnit LLM task is pending, also read that run's `prompt.md`; it remains the authoritative task-specific grounding package.",
            "3. Do not infer trusted axioms from prose. Use `trusted_umcm.json` / formal validation status.",
            "4. After a meaningful experiment, update the run `EXPERIENCE.md`, regenerate `SUMMARY.md`, and regenerate this handoff.",
            "",
        ]
    )
    return "\n".join(lines)


def write_current_handoff(
    repo_root: str | Path,
    *,
    output: str | Path,
    run_roots: Iterable[str | Path] = (),
    task_dirs: Iterable[str | Path] = (),
    max_runs: int = 12,
) -> Path:
    path = Path(output).expanduser()
    if not path.is_absolute():
        path = Path(repo_root).expanduser() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        build_current_handoff(
            repo_root,
            run_roots=run_roots,
            task_dirs=task_dirs,
            max_runs=max_runs,
        ),
        encoding="utf-8",
    )
    return path
