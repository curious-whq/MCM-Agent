from __future__ import annotations

import json
import re
from typing import Any

from .axiom_ir import expression_schema, formal_axiom_schema


# v0.3 makes the formal axiom AST the unique semantic source of truth.
# Occurrences/predicates remain grounded as in v0.2, but prose formulas and
# LLM-authored validation programs are no longer part of an axiom.
UMCM_SCHEMA_VERSION = "umcm-formal-0.5"


def _evidence_schema() -> dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "integer", "minimum": 0},
        "uniqueItems": True,
    }


def _string_list() -> dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "string"},
        "uniqueItems": True,
    }


def candidate_output_schema() -> dict[str, Any]:
    """Return the formal-axiom µMCM candidate envelope.

    The axiom `formal` AST is the single source of truth. Human-readable
    formulas and proof obligations are derived deterministically from it; the
    LLM is not allowed to supply a second validation program.
    """

    evidence = _evidence_schema()
    strings = _string_list()
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Formal µMCM candidate v0.5",
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "formal_expr": expression_schema(),
            "formal_axiom": formal_axiom_schema(),
        },
        "required": [
            "schema_version",
            "task_id",
            "work_unit_id",
            "occurrences",
            "predicates",
            "identity_keys",
            "cases",
            "axioms",
            "assumptions",
            "unresolved",
            "rationale",
            "extensions",
        ],
        "properties": {
            "schema_version": {"const": UMCM_SCHEMA_VERSION},
            "task_id": {"type": "string", "minLength": 1},
            "work_unit_id": {"type": "string", "minLength": 1},
            "occurrences": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "kind",
                        "physical_event_ids",
                        "definition",
                        "multiplicity",
                        "grounding",
                        "evidence_statement_ids",
                    ],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "kind": {"enum": ["boundary", "derived"]},
                        "physical_event_ids": strings,
                        "definition": {"type": "string", "minLength": 1},
                        "multiplicity": {
                            "enum": [
                                "exactly_once",
                                "at_most_once",
                                "repeatable",
                                "unspecified",
                            ]
                        },
                        "index": {
                            "oneOf": [
                                {"type": "null"},
                                {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["name", "expr", "domain"],
                                    "properties": {
                                        "name": {"type": "string", "minLength": 1},
                                        "expr": {"$ref": "#/$defs/formal_expr"},
                                        "domain": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["start", "end_exclusive"],
                                            "properties": {
                                                "start": {"type": "integer", "minimum": 0},
                                                "end_exclusive": {"type": "integer", "minimum": 1}
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                        "grounding": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "state_register",
                                "state_values",
                                "signals_true",
                                "signals_false",
                            ],
                            "properties": {
                                "state_register": {
                                    "type": ["string", "null"]
                                },
                                "state_values": {
                                    "type": "array",
                                    "items": {"type": "integer", "minimum": 0},
                                    "uniqueItems": True,
                                },
                                "signals_true": strings,
                                "signals_false": strings,
                            },
                        },
                        "evidence_statement_ids": evidence,
                    },
                },
            },
            "predicates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "definition",
                        "grounding",
                        "evidence_statement_ids",
                    ],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "definition": {"type": "string", "minLength": 1},
                        "grounding": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "source_signal",
                                "negated",
                                "state_register",
                                "state_values",
                            ],
                            "properties": {
                                "source_signal": {"type": ["string", "null"]},
                                "negated": {"type": "boolean"},
                                "state_register": {"type": ["string", "null"]},
                                "state_values": {
                                    "type": "array",
                                    "items": {"type": "integer", "minimum": 0},
                                    "uniqueItems": True,
                                },
                            },
                        },
                        "evidence_statement_ids": evidence,
                    },
                },
            },
            "identity_keys": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "carrier_state",
                        "fields",
                        "description",
                        "evidence_statement_ids",
                    ],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "carrier_state": {"type": "string", "minLength": 1},
                        "fields": strings,
                        "description": {"type": "string"},
                        "evidence_statement_ids": evidence,
                    },
                },
            },
            "cases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "trigger_occurrences",
                        "guard_predicates",
                        "emits",
                        "relations",
                        "evidence_statement_ids",
                        "confidence",
                    ],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "trigger_occurrences": strings,
                        "guard_predicates": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["id", "positive"],
                                "properties": {
                                    "id": {"type": "string", "minLength": 1},
                                    "positive": {"type": "boolean"},
                                },
                            },
                        },
                        "emits": strings,
                        "relations": {"type": "array", "items": {"type": "string"}},
                        "evidence_statement_ids": evidence,
                        "confidence": {"enum": ["high", "medium", "low"]},
                    },
                },
            },
            "axioms": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "id",
                        "formal",
                        "derived_from_case_ids",
                        "evidence_statement_ids",
                        "status",
                    ],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "formal": {"$ref": "#/$defs/formal_axiom"},
                        "derived_from_case_ids": strings,
                        "evidence_statement_ids": evidence,
                        "status": {"const": "candidate"},
                    },
                },
            },
            "assumptions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "statement", "evidence_statement_ids"],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "statement": {"type": "string"},
                        "evidence_statement_ids": evidence,
                    },
                },
            },
            "unresolved": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "question", "evidence_statement_ids"],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "question": {"type": "string"},
                        "evidence_statement_ids": evidence,
                    },
                },
            },
            "rationale": {"type": "array", "items": {"type": "string"}},
            "extensions": {"type": "object"},
        },
    }


def _extract_fenced_json(text: str) -> str | None:
    matches = list(
        re.finditer(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    )
    if not matches:
        return None
    return matches[-1].group(1).strip()


def parse_candidate_response(text: str) -> dict[str, Any]:
    """Parse a manual conversation result without requiring prose-free output."""

    raw = text.strip()
    if not raw:
        raise ValueError("Manual response is empty")

    candidates = [raw]
    fenced = _extract_fenced_json(raw)
    if fenced is not None:
        candidates.insert(0, fenced)

    errors: list[str] = []
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(parsed, dict):
            errors.append("top-level JSON value is not an object")
            continue
        return parsed

    raise ValueError(
        "Could not parse a JSON candidate from the manual response: "
        + "; ".join(errors[:2])
    )
