"""Experimental manual-first µMCM synthesis workflow.

The workflow is intentionally provider-neutral: deterministic static analysis,
prompt construction, result parsing, and validation are implemented now, while
LLM generation can be supplied either by a human conversation or a future API
provider without changing downstream stages.
"""

from .schema import (
    UMCM_SCHEMA_VERSION,
    candidate_output_schema,
    parse_candidate_response,
)
from .handoff import (
    HANDOFF_SCHEMA_VERSION,
    build_work_unit_static_handoff,
)
from .tasks import (
    PROMPT_VERSION,
    WORKFLOW_VERSION,
    LLMTask,
    PromptPackage,
    TaskKind,
    build_leaf_abstraction_task,
)
from .manual import (
    ManualImportResult,
    export_manual_task,
    import_manual_response,
    validate_candidate_grounding,
)

__all__ = [
    "UMCM_SCHEMA_VERSION",
    "candidate_output_schema",
    "parse_candidate_response",
    "HANDOFF_SCHEMA_VERSION",
    "build_work_unit_static_handoff",
    "PROMPT_VERSION",
    "WORKFLOW_VERSION",
    "LLMTask",
    "PromptPackage",
    "TaskKind",
    "build_leaf_abstraction_task",
    "ManualImportResult",
    "export_manual_task",
    "import_manual_response",
    "validate_candidate_grounding",
]
