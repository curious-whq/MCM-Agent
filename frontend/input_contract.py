from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class InputFormat(str, Enum):
    """Static-frontend input families that can be detected textually."""

    CHIRRTL = "chirrtl"
    FIRRTL_DIALECT = "firrtl_dialect"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class InputValidationReport:
    """Validation result for the deterministic frontend input contract.

    v5 deliberately accepts textual CHIRRTL/classic FIRRTL syntax. CIRCT's
    MLIR FIRRTL dialect is detected explicitly so users receive a precise error
    instead of a misleading structural-parse failure.
    """

    format: InputFormat
    supported: bool
    has_source_locators: bool
    source_locator_count: int
    reason: str | None = None

    @property
    def provenance_ready(self) -> bool:
        return self.supported and self.has_source_locators


_CHIRRTL_CIRCUIT_RE = re.compile(
    r"^\s*circuit\s+[A-Za-z_.$][A-Za-z0-9_.$]*\s*:",
    re.MULTILINE,
)
_FIRRTL_DIALECT_RE = re.compile(r"\bfirrtl\.circuit\b")
_SOURCE_LOCATOR_RE = re.compile(r"@\[[^\]]+\]")


def detect_input_format(text: str) -> InputFormat:
    if _FIRRTL_DIALECT_RE.search(text):
        return InputFormat.FIRRTL_DIALECT
    if _CHIRRTL_CIRCUIT_RE.search(text):
        return InputFormat.CHIRRTL
    return InputFormat.UNKNOWN


def validate_static_input(text: str) -> InputValidationReport:
    """Validate the v5 input contract without changing the design.

    Supported now:
        textual CHIRRTL/classic FIRRTL surface syntax produced by a Chisel
        elaboration path such as emitCHIRRTL.

    Detected but intentionally deferred:
        CIRCT FIRRTL dialect / MLIR text. A dedicated adapter should consume
        that form later rather than mixing two grammars in one parser.
    """

    format_ = detect_input_format(text)
    locator_count = len(_SOURCE_LOCATOR_RE.findall(text))

    if format_ is InputFormat.CHIRRTL:
        return InputValidationReport(
            format=format_,
            supported=True,
            has_source_locators=locator_count > 0,
            source_locator_count=locator_count,
        )

    if format_ is InputFormat.FIRRTL_DIALECT:
        return InputValidationReport(
            format=format_,
            supported=False,
            has_source_locators=locator_count > 0,
            source_locator_count=locator_count,
            reason=(
                "CIRCT FIRRTL-dialect MLIR is not parsed by the v5 CHIRRTL "
                "frontend; use a CHIRRTL emission for now or add a dedicated "
                "FIRRTL-dialect adapter."
            ),
        )

    return InputValidationReport(
        format=format_,
        supported=False,
        has_source_locators=locator_count > 0,
        source_locator_count=locator_count,
        reason="No textual CHIRRTL circuit declaration was detected.",
    )


def require_supported_static_input(text: str) -> InputValidationReport:
    report = validate_static_input(text)
    if not report.supported:
        raise ValueError(report.reason or "Unsupported static frontend input")
    return report
