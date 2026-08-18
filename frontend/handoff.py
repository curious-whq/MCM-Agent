from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .source import SourceMapper, snippet_dict
from .slice import EventSliceMode, SliceOptions

if TYPE_CHECKING:
    from .pipeline import StaticFrontend


class HandoffNotReadyError(RuntimeError):
    pass


def _require_provenance(frontend: "StaticFrontend") -> None:
    if not frontend.input_report.provenance_ready:
        raise HandoffNotReadyError(
            "Static input has no source locators; the LLM handoff would not be "
            "grounded back to source code."
        )


def build_local_static_handoff(
    frontend: "StaticFrontend",
    module_name: str,
    event_id: str,
    *,
    source_mapper: SourceMapper | None = None,
    context_lines: int = 2,
    mode: EventSliceMode = EventSliceMode.FULL,
    options: SliceOptions | None = None,
) -> dict:
    """Build the deterministic package allowed to cross the future LLM boundary."""

    _require_provenance(frontend)
    result = frontend.slice_event(
        module_name,
        event_id,
        mode=mode,
        options=options,
    )
    if not result.complete:
        raise HandoffNotReadyError(
            f"Static slice for {event_id} is incomplete or truncated; "
            "unsupported RTL must be handled before LLM use."
        )
    if not result.source_spans:
        raise HandoffNotReadyError(
            f"Static slice for {event_id} has no source-mapped statements/signals."
        )

    manifest = frontend.slice_manifest(
        module_name,
        event_id,
        mode=mode,
        options=options,
    )
    manifest["input"] = {
        "format": frontend.input_report.format.value,
        "has_source_locators": frontend.input_report.has_source_locators,
        "source_locator_count": frontend.input_report.source_locator_count,
    }
    manifest["handoff"] = {
        "ready": True,
        "stage": "pre-llm-static",
        "semantic_labels_locked": True,
    }

    if source_mapper is not None:
        manifest["source_snippets"] = [
            snippet_dict(snippet)
            for snippet in source_mapper.snippets(
                result.source_spans,
                context_lines=context_lines,
            )
        ]

    return manifest


def build_design_static_handoff(
    frontend: "StaticFrontend",
    event_id: str,
    *,
    source_mapper: SourceMapper | None = None,
    context_lines: int = 2,
    include_payload: bool = True,
) -> dict:
    """Build a cross-module deterministic package before future LLM analysis."""

    _require_provenance(frontend)
    result = frontend.slice_design_event(
        event_id,
        include_payload=include_payload,
    )
    if not result.complete:
        details = ", ".join(result.incomplete_instances) or "truncated slice"
        raise HandoffNotReadyError(
            f"Hierarchical static slice for {event_id} is incomplete: {details}"
        )
    if not result.source_spans:
        raise HandoffNotReadyError(
            f"Hierarchical static slice for {event_id} has no source mapping."
        )

    manifest = frontend.design_slice_manifest(
        event_id,
        include_payload=include_payload,
    )
    manifest["input"] = {
        "format": frontend.input_report.format.value,
        "has_source_locators": frontend.input_report.has_source_locators,
        "source_locator_count": frontend.input_report.source_locator_count,
    }
    manifest["handoff"] = {
        "ready": True,
        "stage": "pre-llm-static",
        "semantic_labels_locked": True,
    }

    if source_mapper is not None:
        manifest["source_snippets"] = [
            snippet_dict(snippet)
            for snippet in source_mapper.snippets(
                result.source_spans,
                context_lines=context_lines,
            )
        ]

    return manifest
