from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .abstraction_tree import abstraction_tree_dict
from .pipeline import StaticFrontend
from .slice import EventSliceMode
from .source import SourceMapper, snippet_dict


def _load(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _report(frontend: StaticFrontend) -> dict:
    report = frontend.report()
    return {
        "top": report.top,
        "input": {
            "format": frontend.input_report.format.value,
            "supported": frontend.input_report.supported,
            "has_source_locators": frontend.input_report.has_source_locators,
            "source_locator_count": frontend.input_report.source_locator_count,
            "provenance_ready": frontend.input_report.provenance_ready,
        },
        "complete": report.complete,
        "modules": [
            {
                "module": module.module,
                "complete": module.complete,
                "statement_count": module.statement_count,
                "unsupported_count": module.unsupported_count,
                "event_count": module.event_count,
            }
            for module in report.modules
        ],
    }


def _events(frontend: StaticFrontend, module: str | None) -> dict:
    modules = [module] if module else sorted(frontend.registries)
    out = {}
    for name in modules:
        registry = frontend.registries[name]
        out[name] = [
            {
                "id": event.event_id,
                "channel": event.channel,
                "direction": event.direction.value,
                "protocol": event.protocol.value,
                "predicate": event.predicate,
            }
            for event in registry.sorted_events()
        ]
    return out



def _tree(frontend: StaticFrontend) -> dict:
    return abstraction_tree_dict(frontend.abstraction_tree())

def _partition(frontend: StaticFrontend, module: str) -> dict:
    plan = frontend.partition(module)
    return {
        "module": module,
        "regions": [
            {
                "id": region.id,
                "registers": list(region.registers),
                "event_ids": list(region.event_ids),
            }
            for region in plan.regions
        ],
        "event_cones": [
            {
                "event_id": cone.event_id,
                "registers": list(cone.registers),
                "complete": cone.complete,
            }
            for cone in plan.event_cones
        ],
    }


def _slice(
    frontend: StaticFrontend,
    module: str,
    event_id: str,
    mode: str,
    source_roots: Sequence[str],
    context_lines: int,
) -> dict:
    manifest = frontend.slice_manifest(
        module,
        event_id,
        mode=EventSliceMode(mode),
    )

    if source_roots:
        result = frontend.slice_event(
            module,
            event_id,
            mode=EventSliceMode(mode),
        )
        mapper = SourceMapper.from_roots(source_roots)
        manifest["source_snippets"] = [
            snippet_dict(snippet)
            for snippet in mapper.snippets(
                result.source_spans,
                context_lines=context_lines,
            )
        ]

    return manifest



def _design_events(frontend: StaticFrontend) -> list[dict]:
    return [
        {
            "id": event.event_id,
            "instance_path": event.instance_path,
            "module": event.module,
            "channel": event.channel,
            "direction": event.direction.value,
            "protocol": event.local_event.protocol.value,
            "predicate": event.predicate,
        }
        for event in frontend.design_events()
    ]



def _connectors(frontend: StaticFrontend) -> list[dict]:
    return [
        {
            "from_event": connector.from_event,
            "to_event": connector.to_event,
            "valid_edge": list(connector.valid_edge),
            "ready_edge": list(connector.ready_edge),
        }
        for connector in frontend.design_connectors()
    ]

def _design_slice(
    frontend: StaticFrontend,
    event_id: str,
    include_payload: bool,
    source_roots: Sequence[str],
    context_lines: int,
) -> dict:
    manifest = frontend.design_slice_manifest(
        event_id,
        include_payload=include_payload,
    )
    if source_roots:
        result = frontend.slice_design_event(
            event_id,
            include_payload=include_payload,
        )
        mapper = SourceMapper.from_roots(source_roots)
        manifest["source_snippets"] = [
            snippet_dict(snippet)
            for snippet in mapper.snippets(
                result.source_spans,
                context_lines=context_lines,
            )
        ]
    return manifest

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m frontend.cli",
        description="Deterministic MCM-Agent static frontend before any LLM stage.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="summarize static coverage")
    report.add_argument("firrtl")

    events = sub.add_parser("events", help="list physical handshake events")
    events.add_argument("firrtl")
    events.add_argument("--module")

    design_events = sub.add_parser(
        "design-events",
        help="list instance-specific physical handshake events",
    )
    design_events.add_argument("firrtl")

    connectors = sub.add_parser(
        "connectors",
        help="list direct valid/ready endpoint connectors",
    )
    connectors.add_argument("firrtl")

    design_slice = sub.add_parser(
        "design-slice",
        help="emit a cross-module event-centered static manifest",
    )
    design_slice.add_argument("firrtl")
    design_slice.add_argument("--event", required=True)
    design_slice.add_argument("--payload", action="store_true")
    design_slice.add_argument("--source-root", action="append", default=[])
    design_slice.add_argument("--context-lines", type=int, default=2)

    tree = sub.add_parser(
        "tree",
        help="show physical hierarchy plus static state-region work units",
    )
    tree.add_argument("firrtl")

    partition = sub.add_parser("partition", help="show register-SCC/event-cone plan")
    partition.add_argument("firrtl")
    partition.add_argument("--module", required=True)

    slice_parser = sub.add_parser("slice", help="emit an event-centered static manifest")
    slice_parser.add_argument("firrtl")
    slice_parser.add_argument("--module", required=True)
    slice_parser.add_argument("--event", required=True)
    slice_parser.add_argument(
        "--mode",
        choices=[mode.value for mode in EventSliceMode],
        default=EventSliceMode.FULL.value,
    )
    slice_parser.add_argument(
        "--source-root",
        action="append",
        default=[],
        help="root used to resolve FIRRTL Scala source locators; repeatable",
    )
    slice_parser.add_argument("--context-lines", type=int, default=2)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    frontend = StaticFrontend.from_firrtl(_load(args.firrtl))

    if args.command == "report":
        output = _report(frontend)
    elif args.command == "events":
        output = _events(frontend, args.module)
    elif args.command == "design-events":
        output = _design_events(frontend)
    elif args.command == "connectors":
        output = _connectors(frontend)
    elif args.command == "design-slice":
        output = _design_slice(
            frontend,
            args.event,
            args.payload,
            args.source_root,
            args.context_lines,
        )
    elif args.command == "tree":
        output = _tree(frontend)
    elif args.command == "partition":
        output = _partition(frontend, args.module)
    elif args.command == "slice":
        output = _slice(
            frontend,
            args.module,
            args.event,
            args.mode,
            args.source_root,
            args.context_lines,
        )
    else:  # pragma: no cover - argparse makes this unreachable
        raise AssertionError(args.command)

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
