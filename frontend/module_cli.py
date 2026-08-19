from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .pipeline import StaticFrontend
from .workunit import (
    WorkUnitConfig,
    build_hierarchical_work_unit,
    work_unit_plan_dict,
    work_unit_stats,
    work_unit_tree_dict,
)


def _load(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _add_root_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--root-instance",
        help=(
            "concrete instance path rooted at design top; recommended for a "
            "whole-SoC FIRRTL"
        ),
    )
    group.add_argument(
        "--root-module",
        help=(
            "analyze one module type as a standalone hierarchical root; useful "
            "for LSQ/L1/L2 development before selecting a concrete instance"
        ),
    )


def _add_limit_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--max-loc", type=int)
    parser.add_argument("--max-signals", type=int)
    parser.add_argument("--max-registers", type=int)
    parser.add_argument("--max-memories", type=int)
    parser.add_argument("--max-events", type=int)
    parser.add_argument("--max-edges", type=int)
    parser.add_argument("--max-statements", type=int)
    parser.add_argument("--max-state-sccs", type=int)
    parser.add_argument("--coupling-threshold", type=float)
    parser.add_argument("--max-depth", type=int)


def _config(args: argparse.Namespace) -> WorkUnitConfig:
    defaults = WorkUnitConfig()
    return WorkUnitConfig(
        max_source_loc=(
            args.max_loc if args.max_loc is not None else defaults.max_source_loc
        ),
        max_signals=(
            args.max_signals
            if args.max_signals is not None
            else defaults.max_signals
        ),
        max_registers=(
            args.max_registers
            if args.max_registers is not None
            else defaults.max_registers
        ),
        max_memories=(
            args.max_memories
            if args.max_memories is not None
            else defaults.max_memories
        ),
        max_events=(
            args.max_events
            if args.max_events is not None
            else defaults.max_events
        ),
        max_dependency_edges=(
            args.max_edges
            if args.max_edges is not None
            else defaults.max_dependency_edges
        ),
        max_statements=(
            args.max_statements
            if args.max_statements is not None
            else defaults.max_statements
        ),
        max_state_sccs=(
            args.max_state_sccs
            if args.max_state_sccs is not None
            else defaults.max_state_sccs
        ),
        coupling_threshold=(
            args.coupling_threshold
            if args.coupling_threshold is not None
            else defaults.coupling_threshold
        ),
        coupling_threshold_step=defaults.coupling_threshold_step,
        max_coupling_threshold=defaults.max_coupling_threshold,
        max_depth=(
            args.max_depth
            if args.max_depth is not None
            else defaults.max_depth
        ),
        min_child_statements=defaults.min_child_statements,
    )


def _build(
    frontend: StaticFrontend,
    args: argparse.Namespace,
):
    return build_hierarchical_work_unit(
        frontend.design,
        frontend.graph,
        frontend.registries,
        root_instance=args.root_instance,
        root_module=args.root_module,
        config=_config(args),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcm-plan",
        description=(
            "Recursive static hierarchical work-unit planner. Event slices are "
            "internal primitives; the exported unit is an ownership-preserving "
            "physical/state hierarchy."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for command, help_text in (
        (
            "module-tree",
            "show the recursive physical + static work-unit tree",
        ),
        (
            "module-stats",
            "show LOC/signal/register/event/coupling statistics per work unit",
        ),
        (
            "module-plan",
            "show ownership, coverage and child-summary replacement inputs",
        ),
    ):
        command_parser = sub.add_parser(command, help=help_text)
        command_parser.add_argument("firrtl")
        _add_root_args(command_parser)
        _add_limit_args(command_parser)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = _load(args.firrtl)
    frontend = StaticFrontend.from_firrtl(
        text,
        eager=len(text) < 8_000_000,
    )
    root = _build(frontend, args)

    if args.command == "module-tree":
        output = work_unit_tree_dict(root)
    elif args.command == "module-stats":
        output = {
            "root": root.id,
            "work_units": work_unit_stats(root),
        }
    elif args.command == "module-plan":
        output = work_unit_plan_dict(root)
    else:  # pragma: no cover - argparse makes this unreachable
        raise AssertionError(args.command)

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
