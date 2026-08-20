from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from frontend.dependency import ModuleDependencyGraph
from frontend.model import SourceLoc
from frontend.partition import discover_partition_plan
from frontend.registry import EventRegistry, PhysicalEvent
from frontend.source import SourceMapper, SourceResolutionError, snippet_dict
from frontend.workunit import HierarchicalWorkUnit, WorkUnitComplexity


HANDOFF_SCHEMA_VERSION = "workunit-static-0.1"
PLANNER_VERSION = "hierarchical-planner-v10"


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
        statements.append(
            {
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
        )

    edges = []
    for edge in graph.edges:
        owned_statement_ids = sorted(set(edge.statement_ids) & statement_ids)
        if not owned_statement_ids:
            continue
        edges.append(
            {
                "src": edge.src,
                "dst": edge.dst,
                "kind": edge.kind.value,
                "statement_ids": owned_statement_ids,
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

    frontier = []
    for signal in sorted(unit.frontier_signals):
        info = graph.signals.get(signal)
        frontier.append(
            {
                "id": signal,
                "kind": info.kind.value if info is not None else "unknown",
                "type": info.type_text if info is not None else None,
                "source": _source_dict(info.source) if info is not None else None,
            }
        )

    plan = discover_partition_plan(graph, registry)
    semantic_cones = []
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

    children = [
        {
            "child_id": child.child_id,
            "child_kind": child.child_kind.value,
            "summary_ref": child.summary_ref,
            "boundary_events": list(child.boundary_events),
            "frontier_signals": list(child.frontier_signals),
        }
        for child in unit.parent_analysis_input().children
    ]

    source_evidence = _resolve_source_snippets(
        unit.source_spans,
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
        "source_spans": [asdict(span) for span in unit.source_spans],
        "source_evidence": source_evidence,
        "grounding": {
            "allowed_statement_ids": sorted(statement_ids),
            "allowed_physical_event_ids": sorted(unit.local_event_ids),
            "allowed_state_ids": sorted(unit.local_state),
            "semantic_labels": [],
        },
    }
