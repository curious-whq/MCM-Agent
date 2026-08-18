from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .dependency import ModuleDependencyGraph
from .registry import PhysicalEvent
from .slice import SliceResult


MANIFEST_SCHEMA_VERSION = "mcm-agent.static-slice.v1"


def _source_dict(source) -> dict[str, Any] | None:
    if source is None:
        return None
    return {
        "file": source.file,
        "line": source.line,
        "column": source.column,
        "raw": source.raw,
    }


def slice_manifest_dict(
    graph: ModuleDependencyGraph,
    event: PhysicalEvent,
    result: SliceResult,
) -> dict[str, Any]:
    """Create deterministic LLM-ready *static* input without semantic labels."""

    included_statements = [
        graph.statements[statement_id]
        for statement_id in sorted(result.statement_ids)
        if 0 <= statement_id < len(graph.statements)
    ]

    unsupported = [entry.statement for entry in result.ledger.unsupported]

    return {
        "schema": MANIFEST_SCHEMA_VERSION,
        "module": graph.module,
        "event": {
            "id": event.event_id,
            "channel": event.channel,
            "direction": event.direction.value,
            "protocol": event.protocol.value,
            "predicate": event.predicate,
            "valid": event.valid.path,
            "ready": event.ready.path if event.ready is not None else None,
            "payload": [port.path for port in event.payload],
            "sources": [_source_dict(source) for source in event.sources],
        },
        "analysis": {
            "complete": result.complete,
            "truncated": result.truncated,
            "seeds": list(result.seeds),
            "boundary_frontier": list(result.boundary_frontier),
            "coverage": result.ledger.counts(),
            "provenance": {
                "included_statement_count": len(included_statements),
                "included_statements_with_source": sum(
                    statement.source is not None
                    for statement in included_statements
                ),
                "source_span_count": len(result.source_spans),
            },
        },
        "signals": [
            {
                "name": signal,
                "kind": (
                    graph.signals[signal].kind.value
                    if signal in graph.signals
                    else "unknown"
                ),
                "source": (
                    _source_dict(graph.signals[signal].source)
                    if signal in graph.signals
                    else None
                ),
            }
            for signal in sorted(result.signals)
        ],
        "edges": [
            {
                "src": edge.src,
                "dst": edge.dst,
                "kind": edge.kind.value,
                "statement_ids": list(edge.statement_ids),
                "source": _source_dict(edge.source),
            }
            for edge in result.edges
        ],
        "statements": [
            {
                "id": statement.id,
                "firrtl_line": statement.firrtl_line,
                "kind": statement.kind,
                "text": statement.text,
                "source": _source_dict(statement.source),
                "drives": list(statement.drives),
                "reads": list(statement.reads),
                "control_reads": list(statement.control_reads),
            }
            for statement in included_statements
        ],
        "source_spans": [
            {
                "file": span.file,
                "start_line": span.start_line,
                "end_line": span.end_line,
            }
            for span in result.source_spans
        ],
        "unsupported_statements": [
            {
                "id": statement.id,
                "firrtl_line": statement.firrtl_line,
                "text": statement.text,
                "source": _source_dict(statement.source),
                "note": statement.note,
            }
            for statement in unsupported
        ],
        "semantic_labels": [],
    }


def slice_manifest_json(
    graph: ModuleDependencyGraph,
    event: PhysicalEvent,
    result: SliceResult,
    *,
    indent: int = 2,
) -> str:
    return json.dumps(
        slice_manifest_dict(graph, event, result),
        indent=indent,
        sort_keys=True,
    ) + "\n"


def write_slice_manifest(
    path: str | Path,
    graph: ModuleDependencyGraph,
    event: PhysicalEvent,
    result: SliceResult,
) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        slice_manifest_json(graph, event, result),
        encoding="utf-8",
    )
    return output


def design_slice_manifest_dict(
    graph,
    event,
    result,
) -> dict:
    """Export a deterministic cross-module static slice.

    Imports are intentionally local to keep the local-module exporter free of
    a design_graph import cycle.
    """

    return {
        "schema": MANIFEST_SCHEMA_VERSION,
        "scope": "design",
        "top": graph.top,
        "event": {
            "id": event.event_id,
            "instance_path": event.instance_path,
            "module": event.module,
            "channel": event.channel,
            "direction": event.direction.value,
            "protocol": event.local_event.protocol.value,
            "predicate": event.predicate,
            "valid_signal": event.valid_signal,
            "ready_signal": event.ready_signal,
            "payload_signals": list(event.payload_signals),
        },
        "analysis": {
            "complete": result.complete,
            "truncated": result.truncated,
            "seeds": list(result.seeds),
            "frontier": list(result.frontier),
            "instances": list(result.instances),
            "incomplete_instances": list(result.incomplete_instances),
            "source_span_count": len(result.source_spans),
        },
        "signals": [
            {
                "id": signal,
                "instance_path": graph.signals[signal].instance_path,
                "module": graph.signals[signal].module,
                "local_name": graph.signals[signal].local_name,
                "kind": graph.signals[signal].kind.value,
                "source": _source_dict(graph.signals[signal].source),
            }
            for signal in sorted(result.signals)
            if signal in graph.signals
        ],
        "edges": [
            {
                "src": edge.src,
                "dst": edge.dst,
                "kind": edge.kind.value,
                "statements": [
                    {
                        "instance_path": statement.instance_path,
                        "module": statement.module,
                        "statement_id": statement.statement_id,
                    }
                    for statement in edge.statements
                ],
                "source": _source_dict(edge.source),
            }
            for edge in result.edges
        ],
        "source_spans": [
            {
                "file": span.file,
                "start_line": span.start_line,
                "end_line": span.end_line,
            }
            for span in result.source_spans
        ],
        "semantic_labels": [],
    }
