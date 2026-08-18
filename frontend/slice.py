from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .coverage import CoverageLedger, build_coverage_ledger
from .dependency import DependencyEdge, DependencyKind, ModuleDependencyGraph
from .model import SourceLoc
from .registry import PhysicalEvent


class EventSliceMode(str, Enum):
    OCCURRENCE = "occurrence"
    FULL = "full"


@dataclass(frozen=True)
class SliceOptions:
    include_clock: bool = False
    include_reset: bool = False
    stop_at_module_inputs: bool = True
    max_signals: int | None = None

    def allowed_kinds(self) -> set[DependencyKind]:
        kinds = {
            DependencyKind.DATA,
            DependencyKind.CONTROL,
            DependencyKind.STATE,
            DependencyKind.ADDRESS,
            DependencyKind.MEMORY,
            DependencyKind.ALIAS,
        }
        if self.include_clock:
            kinds.add(DependencyKind.CLOCK)
        if self.include_reset:
            kinds.add(DependencyKind.RESET)
        return kinds


@dataclass(frozen=True, order=True)
class SourceSpan:
    file: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class SliceResult:
    module: str
    seeds: tuple[str, ...]
    signals: frozenset[str]
    edges: tuple[DependencyEdge, ...]
    statement_ids: frozenset[int]
    boundary_frontier: tuple[str, ...]
    source_spans: tuple[SourceSpan, ...]
    ledger: CoverageLedger
    truncated: bool = False

    @property
    def complete(self) -> bool:
        return self.ledger.complete and not self.truncated


def _spans_from_sources(
    sources: Iterable[SourceLoc],
    context: int = 0,
    merge_gap: int = 1,
) -> tuple[SourceSpan, ...]:
    by_file: dict[str, set[int]] = defaultdict(set)
    for source in sources:
        if source.line <= 0:
            continue
        by_file[source.file].add(source.line)

    spans: list[SourceSpan] = []
    for file in sorted(by_file):
        lines = sorted(by_file[file])
        if not lines:
            continue
        start = end = lines[0]
        for line in lines[1:]:
            if line <= end + merge_gap + 1:
                end = line
            else:
                spans.append(
                    SourceSpan(
                        file=file,
                        start_line=max(1, start - context),
                        end_line=end + context,
                    )
                )
                start = end = line
        spans.append(
            SourceSpan(
                file=file,
                start_line=max(1, start - context),
                end_line=end + context,
            )
        )
    return tuple(spans)


def backward_slice(
    graph: ModuleDependencyGraph,
    seeds: Iterable[str],
    options: SliceOptions | None = None,
) -> SliceResult:
    """Compute a finite backward fixed point over data/control/state edges."""

    options = options or SliceOptions()
    allowed = options.allowed_kinds()

    predecessors: dict[str, list[DependencyEdge]] = defaultdict(list)
    for edge in graph.edges:
        if edge.kind in allowed:
            predecessors[edge.dst].append(edge)

    seed_tuple = tuple(sorted(set(seeds)))
    visited: set[str] = set(seed_tuple)
    selected_edges: set[DependencyEdge] = set()
    statement_ids: set[int] = set()
    frontier: set[str] = set()
    queue = deque(seed_tuple)
    truncated = False

    while queue:
        signal = queue.popleft()

        if options.stop_at_module_inputs and signal in graph.input_ports:
            frontier.add(signal)
            continue

        for edge in predecessors.get(signal, ()):
            selected_edges.add(edge)
            statement_ids.update(edge.statement_ids)
            if edge.src not in visited:
                if options.max_signals is not None and len(visited) >= options.max_signals:
                    truncated = True
                    continue
                visited.add(edge.src)
                queue.append(edge.src)

        # A signal with no local predecessor is an explicit frontier. This
        # includes child-instance outputs and unresolved/external sources.
        if not predecessors.get(signal):
            frontier.add(signal)

    sources: list[SourceLoc] = []
    for statement_id in sorted(statement_ids):
        if 0 <= statement_id < len(graph.statements):
            source = graph.statements[statement_id].source
            if source is not None:
                sources.append(source)
    for signal in visited:
        info = graph.signals.get(signal)
        if info is not None and info.source is not None:
            sources.append(info.source)

    ledger = build_coverage_ledger(graph, statement_ids)

    return SliceResult(
        module=graph.module,
        seeds=seed_tuple,
        signals=frozenset(visited),
        edges=tuple(
            sorted(
                selected_edges,
                key=lambda edge: (
                    edge.dst,
                    edge.src,
                    edge.kind.value,
                    edge.statement_ids,
                ),
            )
        ),
        statement_ids=frozenset(statement_ids),
        boundary_frontier=tuple(sorted(frontier)),
        source_spans=_spans_from_sources(sources),
        ledger=ledger,
        truncated=truncated,
    )


def event_seed_signals(
    event: PhysicalEvent,
    mode: EventSliceMode = EventSliceMode.OCCURRENCE,
) -> tuple[str, ...]:
    seeds = {event.valid.path}
    if event.ready is not None:
        seeds.add(event.ready.path)
    if mode is EventSliceMode.FULL:
        seeds.update(port.path for port in event.payload)
    return tuple(sorted(seeds))


def slice_event(
    graph: ModuleDependencyGraph,
    event: PhysicalEvent,
    mode: EventSliceMode = EventSliceMode.OCCURRENCE,
    options: SliceOptions | None = None,
) -> SliceResult:
    if event.module != graph.module:
        raise ValueError(
            f"Event belongs to {event.module}, graph belongs to {graph.module}"
        )
    return backward_slice(
        graph,
        event_seed_signals(event, mode),
        options=options,
    )
