from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .slice import SourceSpan


class SourceResolutionError(FileNotFoundError):
    pass


@dataclass(frozen=True)
class SourceSnippet:
    """A source fragment resolved from FIRRTL source-locator provenance."""

    logical_file: str
    resolved_file: str
    start_line: int
    end_line: int
    text: str


@dataclass(frozen=True)
class SourceMapper:
    """Resolve source-locator paths against explicitly supplied source roots.

    The mapper never searches the network and never guesses a different file.
    Relative locator paths must resolve underneath one of the supplied roots.
    Absolute locator paths are accepted only when they are contained in a root.
    """

    roots: tuple[Path, ...]

    @staticmethod
    def from_roots(roots: Iterable[str | Path]) -> "SourceMapper":
        normalized = tuple(Path(root).expanduser().resolve() for root in roots)
        if not normalized:
            raise ValueError("SourceMapper requires at least one source root")
        return SourceMapper(normalized)

    @staticmethod
    def _within(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            return False

    def resolve(self, logical_file: str) -> Path:
        raw = Path(logical_file)

        for root in self.roots:
            candidate = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
            if not self._within(candidate, root):
                continue
            if candidate.is_file():
                return candidate

        raise SourceResolutionError(
            f"Could not resolve source locator {logical_file!r} under roots: "
            + ", ".join(str(root) for root in self.roots)
        )

    def snippet(
        self,
        span: SourceSpan,
        *,
        context_lines: int = 0,
    ) -> SourceSnippet:
        if context_lines < 0:
            raise ValueError("context_lines must be non-negative")

        path = self.resolve(span.file)
        lines = path.read_text(encoding="utf-8").splitlines()

        requested_start = max(1, span.start_line - context_lines)
        requested_end = min(len(lines), span.end_line + context_lines)

        if span.start_line <= 0 or span.start_line > len(lines):
            raise SourceResolutionError(
                f"Source span {span.file}:{span.start_line}-{span.end_line} "
                f"is outside file with {len(lines)} line(s)"
            )

        text = "\n".join(lines[requested_start - 1 : requested_end])
        if text:
            text += "\n"

        return SourceSnippet(
            logical_file=span.file,
            resolved_file=str(path),
            start_line=requested_start,
            end_line=requested_end,
            text=text,
        )

    def snippets(
        self,
        spans: Iterable[SourceSpan],
        *,
        context_lines: int = 0,
    ) -> tuple[SourceSnippet, ...]:
        return tuple(
            self.snippet(span, context_lines=context_lines)
            for span in spans
        )


def snippet_dict(snippet: SourceSnippet) -> dict:
    return {
        "logical_file": snippet.logical_file,
        "resolved_file": snippet.resolved_file,
        "start_line": snippet.start_line,
        "end_line": snippet.end_line,
        "text": snippet.text,
    }
