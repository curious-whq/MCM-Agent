from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import re
from typing import Any, Iterable

from frontend.dependency import ModuleDependencyGraph
from frontend.model import SourceLoc
from frontend.partition import discover_partition_plan
from frontend.registry import EventRegistry, PhysicalEvent
from frontend.source import SourceMapper, SourceResolutionError, snippet_dict
from frontend.slice import SourceSpan
from frontend.workunit import HierarchicalWorkUnit, WorkUnitComplexity


HANDOFF_SCHEMA_VERSION = "workunit-static-0.4"
PLANNER_VERSION = "hierarchical-planner-v14"


def _split_call_args(text: str) -> list[str] | None:
    args: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return None
        elif char == "," and depth == 0:
            args.append(text[start:index].strip())
            start = index + 1
    if depth != 0:
        return None
    args.append(text[start:].strip())
    return args


def _expression_width(
    graph: ModuleDependencyGraph,
    expression: str,
    definitions: dict[str, str],
    memo: dict[str, int | None],
    seen: set[str],
) -> int | None:
    text = expression.strip()
    literal = re.fullmatch(r"(?:U|S)Int<(\d+)>\([^)]*\)", text)
    if literal:
        return int(literal.group(1))
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*|\[[^]]+\])*", text):
        if text in memo:
            return memo[text]
        info = graph.signals.get(text)
        if info is not None and info.type_text:
            width = re.match(r"^(?:U|S)Int<(\d+)>", info.type_text.strip())
            if width:
                memo[text] = int(width.group(1))
                return memo[text]
        if text in seen or text not in definitions:
            return None
        memo[text] = _expression_width(
            graph, definitions[text], definitions, memo, seen | {text}
        )
        return memo[text]
    call = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_$]*)\((.*)\)", text)
    if not call:
        return None
    name = call.group(1)
    args = _split_call_args(call.group(2))
    if args is None:
        return None
    if name == "bits" and len(args) == 3:
        try:
            high, low = int(args[1]), int(args[2])
        except ValueError:
            return None
        return high - low + 1 if high >= low >= 0 else None
    if name in {"eq", "neq", "lt", "leq", "gt", "geq"} and len(args) == 2:
        return 1
    widths = [
        _expression_width(graph, arg, definitions, memo, seen)
        for arg in args
    ]
    if name in {"and", "or", "xor"} and len(widths) == 2 and None not in widths:
        return max(int(widths[0]), int(widths[1]))
    if name == "not" and len(widths) == 1:
        return widths[0]
    if name == "cat" and len(widths) == 2 and None not in widths:
        return int(widths[0]) + int(widths[1])
    if name in {"mux", "validif"}:
        branches = widths[1:] if name == "mux" else widths[1:2]
        if branches and None not in branches:
            return max(int(width) for width in branches)
    if name in {"asUInt", "asSInt"} and widths:
        return widths[0]
    return None


def _inferred_signal_type(
    graph: ModuleDependencyGraph,
    signal: str,
    definitions: dict[str, str],
    memo: dict[str, int | None],
) -> str | None:
    width = _expression_width(graph, signal, definitions, memo, set())
    return f"UInt<{width}>" if width is not None else None


def _source_dict(source: SourceLoc | None) -> dict[str, Any] | None:
    if source is None:
        return None
    return {
        "file": source.file,
        "line": source.line,
        "column": source.column,
        "raw": source.raw,
    }


def _complexity_dict(complexity: WorkUnitComplexity) -> dict[str, Any]:
    return {
        "raw": {
            "source_loc": complexity.source_loc,
            "unmapped_firrtl_loc": complexity.unmapped_firrtl_loc,
            "signals": complexity.signal_count,
            "dependency_edges": complexity.dependency_edge_count,
            "statements": complexity.statement_count,
        },
        "logical": {
            "source_loc": complexity.logical_source_loc,
            "signals": complexity.logical_signal_count,
            "dependency_edges": complexity.logical_dependency_edge_count,
            "statements": complexity.logical_statement_count,
        },
        "registers": complexity.register_count,
        "memories": complexity.memory_count,
        "events": complexity.event_count,
        "state_regions": complexity.state_scc_count,
        "event_state_coupling": round(complexity.event_state_coupling, 6),
    }


def _registry_id(unit: HierarchicalWorkUnit, concrete_event_id: str) -> str:
    if concrete_event_id.startswith(unit.module + "."):
        return concrete_event_id
    if "::" in concrete_event_id:
        suffix = concrete_event_id.split("::", 1)[1]
        return f"{unit.module}.{suffix}"
    return concrete_event_id


def _event_dict(event: PhysicalEvent, concrete_id: str) -> dict[str, Any]:
    return {
        "id": concrete_id,
        "registry_id": event.event_id,
        "channel": event.channel,
        "direction": event.direction.value,
        "protocol": event.protocol.value,
        "predicate": event.predicate,
        "valid": event.valid.path,
        "ready": event.ready.path if event.ready is not None else None,
        "payload": [port.path for port in event.payload],
        "sources": [_source_dict(source) for source in event.sources],
    }


def _statement_dict(statement) -> dict[str, Any]:
    return {
        "id": statement.id,
        "firrtl_line": statement.firrtl_line,
        "kind": statement.kind,
        "text": statement.text,
        "source": _source_dict(statement.source),
        "status": statement.status.value,
        "drives": list(statement.drives),
        "reads": list(statement.reads),
        "control_reads": list(statement.control_reads),
        "note": statement.note,
    }



def _local_source_spans(statements: list[dict[str, Any]]) -> tuple[SourceSpan, ...]:
    # Rebuild source spans from only the statements visible in this handoff.
    # Parent synthesis must not reintroduce child implementation source text.
    by_file: dict[str, set[int]] = {}
    for statement in statements:
        source = statement.get("source") if isinstance(statement, dict) else None
        if not isinstance(source, dict):
            continue
        file = source.get("file")
        line = source.get("line")
        if isinstance(file, str) and isinstance(line, int) and line > 0:
            by_file.setdefault(file, set()).add(line)

    spans: list[SourceSpan] = []
    for file in sorted(by_file):
        lines = sorted(by_file[file])
        if not lines:
            continue
        start = end = lines[0]
        for line in lines[1:]:
            if line <= end + 2:
                end = line
            else:
                spans.append(SourceSpan(file=file, start_line=start, end_line=end))
                start = end = line
        spans.append(SourceSpan(file=file, start_line=start, end_line=end))
    return tuple(spans)


def _resolve_source_snippets(
    spans,
    source_roots: Iterable[str | Path],
    *,
    context_lines: int,
) -> dict[str, Any]:
    roots = tuple(source_roots)
    if not roots:
        return {
            "roots": [],
            "resolved": [],
            "unresolved": [
                {
                    "file": span.file,
                    "start_line": span.start_line,
                    "end_line": span.end_line,
                }
                for span in spans
            ],
        }

    mapper = SourceMapper.from_roots(roots)
    resolved: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for span in spans:
        try:
            resolved.append(
                snippet_dict(
                    mapper.snippet(span, context_lines=context_lines)
                )
            )
        except SourceResolutionError as exc:
            unresolved.append(
                {
                    "file": span.file,
                    "start_line": span.start_line,
                    "end_line": span.end_line,
                    "error": str(exc),
                }
            )
    return {
        "roots": [str(Path(root).expanduser()) for root in roots],
        "resolved": resolved,
        "unresolved": unresolved,
    }


def build_work_unit_static_handoff(
    unit: HierarchicalWorkUnit,
    graph: ModuleDependencyGraph,
    registry: EventRegistry,
    *,
    source_roots: Iterable[str | Path] = (),
    context_lines: int = 1,
) -> dict[str, Any]:
    """Build a self-contained deterministic package for semantic abstraction.

    Unlike the older event-specific handoff, this package is WorkUnit-centered.
    It preserves all local RTL statements owned by the unit, physical events,
    state/frontier facts, historical event cones, and optional source snippets.
    No semantic event name or µMCM axiom is invented here.
    """

    if not unit.coverage.complete:
        raise ValueError(f"WorkUnit {unit.id!r} has incomplete ownership coverage")

    statement_ids = set(unit.local_statement_ids)
    statements = []
    statement_by_id = {statement.id: statement for statement in graph.statements}
    for statement_id in sorted(statement_ids):
        statement = statement_by_id.get(statement_id)
        if statement is None:
            raise ValueError(
                f"WorkUnit {unit.id!r} references unknown statement {statement_id}"
            )
        statements.append(_statement_dict(statement))

    local_state_roots = {str(root) for root in unit.local_state}

    def local_state_target(signal: str) -> bool:
        return any(
            signal == root
            or signal.startswith(root + ".")
            or signal.startswith(root + "[")
            for root in local_state_roots
        )

    state_writer_control_ids: set[int] = set()
    edges = []
    for edge in graph.edges:
        owned_statement_ids = sorted(set(edge.statement_ids) & statement_ids)
        if not owned_statement_ids:
            continue
        statement_support_ids: set[int] = set()
        if edge.kind.value == "control" and local_state_target(edge.dst):
            statement_support_ids = {
                statement_id
                for statement_id in set(edge.statement_ids) - statement_ids
                if statement_id in statement_by_id
                and statement_by_id[statement_id].kind in {"when", "else"}
            }
            state_writer_control_ids.update(statement_support_ids)
        edges.append(
            {
                "src": edge.src,
                "dst": edge.dst,
                "kind": edge.kind.value,
                "statement_ids": sorted(
                    set(owned_statement_ids) | statement_support_ids
                ),
                "source": _source_dict(edge.source),
            }
        )

    events: list[dict[str, Any]] = []
    local_registry_ids: set[str] = set()
    for concrete_id in unit.local_event_ids:
        registry_id = _registry_id(unit, concrete_id)
        event = registry.events.get(registry_id)
        if event is None:
            raise ValueError(
                f"Could not map WorkUnit event {concrete_id!r} to {unit.module!r} registry"
            )
        local_registry_ids.add(registry_id)
        events.append(_event_dict(event, concrete_id))

    state = []
    for register in sorted(unit.local_state):
        info = graph.signals.get(register)
        state.append(
            {
                "id": register,
                "kind": info.kind.value if info is not None else "register",
                "type": info.type_text if info is not None else None,
                "source": _source_dict(info.source) if info is not None else None,
            }
        )

    node_definitions: dict[str, str] = {}
    for statement in graph.statements:
        match = re.match(
            r"^node\s+([A-Za-z_][A-Za-z0-9_$]*)\s*=\s*(.+)$",
            statement.text.strip(),
        )
        if match:
            node_definitions[match.group(1)] = match.group(2).strip()
    inferred_widths: dict[str, int | None] = {}

    frontier = []
    for signal in sorted(unit.frontier_signals):
        info = graph.signals.get(signal)
        frontier.append(
            {
                "id": signal,
                "kind": info.kind.value if info is not None else "unknown",
                "type": (
                    info.type_text
                    if info is not None and info.type_text
                    else _inferred_signal_type(
                        graph, signal, node_definitions, inferred_widths
                    )
                ),
                "source": _source_dict(info.source) if info is not None else None,
            }
        )

    plan = discover_partition_plan(graph, registry)
    semantic_cones = []
    event_gate_bridge_ids: set[int] = set()
    for cone in plan.event_cones:
        if cone.event_id not in local_registry_ids:
            continue
        concrete_id = next(
            event["id"]
            for event in events
            if event["registry_id"] == cone.event_id
        )
        semantic_cones.append(
            {
                "event_id": concrete_id,
                "historical_registers": list(cone.registers),
                "historical_statement_ids": [
                    statement_id
                    for statement_id in cone.statement_ids
                    if statement_id in statement_ids
                ],
                "immediate_registers": list(cone.immediate_registers),
                "immediate_statement_ids": [
                    statement_id
                    for statement_id in cone.immediate_statement_ids
                    if statement_id in statement_ids
                ],
                "immediate_frontier": list(cone.immediate_frontier),
                "complete": cone.complete,
            }
        )
        # A static region may own the state/gate logic for a module boundary
        # event while the final module-port connector remains parent-owned
        # shared glue. Keep ownership disjoint, but export that exact
        # current-cycle connector cone as prover-only context so the physical
        # event does not become an unrelated opaque atom.
        event_gate_bridge_ids.update(
            set(cone.immediate_statement_ids) - statement_ids
        )

    event_gate_bridges = []
    for statement_id in sorted(event_gate_bridge_ids):
        statement = statement_by_id.get(statement_id)
        if statement is None:
            raise ValueError(
                f"WorkUnit {unit.id!r} event gate references unknown bridge statement {statement_id}"
            )
        event_gate_bridges.append(_statement_dict(statement))

    state_support_ids: set[int] = set()
    for statement in graph.statements:
        if statement.kind not in {"reg", "regreset"}:
            continue
        if any(
            drive == root
            or drive.startswith(root + ".")
            or drive.startswith(root + "[")
            for drive in statement.drives
            for root in local_state_roots
        ):
            state_support_ids.add(statement.id)
    state_support_ids -= statement_ids
    state_support_statements = [
        _statement_dict(statement_by_id[statement_id])
        for statement_id in sorted(state_support_ids)
    ]
    state_writer_control_statements = [
        _statement_dict(statement_by_id[statement_id])
        for statement_id in sorted(state_writer_control_ids)
    ]

    children = [
        {
            "child_id": child.child_id,
            "child_kind": child.child_kind.value,
            "child_module": child.child_module,
            "summary_ref": child.summary_ref,
            "boundary_events": list(child.boundary_events),
            "frontier_signals": list(child.frontier_signals),
        }
        for child in unit.parent_analysis_input().children
    ]

    local_source_spans = _local_source_spans(statements)
    source_evidence = _resolve_source_snippets(
        local_source_spans,
        source_roots,
        context_lines=context_lines,
    )

    return {
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "planner_version": PLANNER_VERSION,
        "work_unit": {
            "id": unit.id,
            "kind": unit.kind.value,
            "module": unit.module,
            "instance_path": unit.instance_path,
            "depth": unit.depth,
            "decision": unit.decision.value,
            "coverage_complete": unit.coverage.complete,
            "is_leaf": not bool(unit.children),
            "exceeded_limits": list(unit.exceeded_limits),
            "replacement_exceeded_limits": list(unit.replacement_exceeded_limits),
        },
        "complexity": _complexity_dict(unit.complexity),
        "replacement_complexity": _complexity_dict(unit.replacement_complexity),
        "events": events,
        "state": state,
        "memory_state": list(unit.memory_state),
        "frontier": frontier,
        "parent_connection_signals": list(unit.parent_connection_signals),
        "children": children,
        "statements": statements,
        "dependency_edges": edges,
        "semantic_event_cones": semantic_cones,
        "proof_context": {
            "policy": "exact-local-proof-context-v0.2",
            "event_gate_statement_ids": sorted(event_gate_bridge_ids),
            "event_gate_statements": event_gate_bridges,
            "state_support_statement_ids": sorted(state_support_ids),
            "state_support_statements": state_support_statements,
            "state_writer_control_statement_ids": sorted(
                state_writer_control_ids
            ),
            "state_writer_control_statements": state_writer_control_statements,
            "llm_evidence": False,
        },
        "source_spans": [asdict(span) for span in local_source_spans],
        "source_evidence": source_evidence,
        "grounding": {
            "allowed_statement_ids": sorted(statement_ids),
            "allowed_physical_event_ids": sorted(unit.local_event_ids),
            "allowed_state_ids": sorted(unit.local_state),
            "semantic_labels": [],
        },
    }
