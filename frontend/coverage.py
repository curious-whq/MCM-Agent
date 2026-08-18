from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum

from .dependency import ModuleDependencyGraph, StatementRecord, StatementStatus


class CoverageStatus(str, Enum):
    INCLUDED = "included"
    SUPPORTED_OUTSIDE_SLICE = "supported_outside_slice"
    NONDRIVING = "nondriving"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class LedgerEntry:
    statement: StatementRecord
    status: CoverageStatus


@dataclass(frozen=True)
class CoverageLedger:
    module: str
    entries: tuple[LedgerEntry, ...]

    @property
    def complete(self) -> bool:
        return all(
            entry.status is not CoverageStatus.UNSUPPORTED
            for entry in self.entries
        )

    @property
    def unsupported(self) -> tuple[LedgerEntry, ...]:
        return tuple(
            entry
            for entry in self.entries
            if entry.status is CoverageStatus.UNSUPPORTED
        )

    @property
    def included(self) -> tuple[LedgerEntry, ...]:
        return tuple(
            entry
            for entry in self.entries
            if entry.status is CoverageStatus.INCLUDED
        )

    def counts(self) -> dict[str, int]:
        counter = Counter(entry.status.value for entry in self.entries)
        return dict(sorted(counter.items()))


def build_coverage_ledger(
    graph: ModuleDependencyGraph,
    included_statement_ids: set[int] | frozenset[int] = frozenset(),
) -> CoverageLedger:
    entries: list[LedgerEntry] = []

    for statement in graph.statements:
        if statement.status is StatementStatus.UNSUPPORTED:
            status = CoverageStatus.UNSUPPORTED
        elif statement.status is StatementStatus.NONDRIVING:
            status = CoverageStatus.NONDRIVING
        elif statement.id in included_statement_ids:
            status = CoverageStatus.INCLUDED
        else:
            status = CoverageStatus.SUPPORTED_OUTSIDE_SLICE

        entries.append(LedgerEntry(statement=statement, status=status))

    return CoverageLedger(module=graph.module, entries=tuple(entries))
