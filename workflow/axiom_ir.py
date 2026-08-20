from __future__ import annotations

from typing import Any


FORMAL_AXIOM_IR_VERSION = "formal-axiom-ir-0.8"


def _string_list(*, min_items: int = 0) -> dict[str, Any]:
    schema: dict[str, Any] = {
        "type": "array",
        "items": {"type": "string", "minLength": 1},
        "uniqueItems": True,
    }
    if min_items:
        schema["minItems"] = min_items
    return schema


def expression_schema() -> dict[str, Any]:
    # Kept deliberately small. New expression operators should be added only
    # when a real WorkUnit requires them and a deterministic compiler exists.
    return {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "name"],
                "properties": {
                    "op": {"const": "signal"},
                    "name": {"type": "string", "minLength": 1},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "value", "hi", "lo"],
                "properties": {
                    "op": {"const": "slice"},
                    "value": {"$ref": "#/$defs/formal_expr"},
                    "hi": {"type": "integer", "minimum": 0},
                    "lo": {"type": "integer", "minimum": 0},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "value", "amount"],
                "properties": {
                    "op": {"const": "shr"},
                    "value": {"$ref": "#/$defs/formal_expr"},
                    "amount": {"type": "integer", "minimum": 0},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "value", "index"],
                "properties": {
                    "op": {"const": "bit"},
                    "value": {"$ref": "#/$defs/formal_expr"},
                    "index": {"type": "integer", "minimum": 0},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "value"],
                "properties": {
                    "op": {"const": "const"},
                    "value": {"type": "integer", "minimum": 0},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "name"],
                "properties": {
                    "op": {"const": "index_var"},
                    "name": {"type": "string", "minLength": 1},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["op", "value", "index"],
                "properties": {
                    "op": {"const": "lookup"},
                    "value": {"$ref": "#/$defs/formal_expr"},
                    "index": {"$ref": "#/$defs/formal_expr"},
                },
            },
        ]
    }


def formal_axiom_schema() -> dict[str, Any]:
    scope = {"type": ["string", "null"]}
    index_scope = {
        "oneOf": [
            {"type": "null"},
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "relation"],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "relation": {"const": "same"},
                },
            },
        ]
    }
    return {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "occurrence", "predicate", "scope_identity"],
                "properties": {
                    "type": {"const": "forbid_when"},
                    "occurrence": {"type": "string", "minLength": 1},
                    "predicate": {"type": "string", "minLength": 1},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "identity", "capture", "projections"],
                "properties": {
                    "type": {"const": "identity_flow"},
                    "identity": {"type": "string", "minLength": 1},
                    "capture": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["on", "source", "carrier"],
                        "properties": {
                            "on": {"type": "string", "minLength": 1},
                            "source": {"type": "string", "minLength": 1},
                            "carrier": {"type": "string", "minLength": 1},
                        },
                    },
                    "projections": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["on", "target", "expr"],
                            "properties": {
                                "on": {"type": "string", "minLength": 1},
                                "target": {"type": "string", "minLength": 1},
                                "expr": {"$ref": "#/$defs/formal_expr"},
                            },
                        },
                    },
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "left", "rights", "scope_identity"],
                "properties": {
                    "type": {"const": "exclusion"},
                    "left": {"type": "string", "minLength": 1},
                    "rights": _string_list(min_items=1),
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "before", "after", "required_prior", "scope_identity"],
                "properties": {
                    "type": {"const": "ordered_before"},
                    "before": {"type": "string", "minLength": 1},
                    "after": {"type": "string", "minLength": 1},
                    "required_prior": {"type": ["string", "null"]},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "sequence", "scope_identity"],
                "properties": {
                    "type": {"const": "ordered_chain"},
                    "sequence": {
                        "type": "array",
                        "minItems": 2,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "on", "target", "source", "scope_identity"],
                "properties": {
                    "type": {"const": "signal_equality"},
                    "on": {"type": ["string", "null"]},
                    "target": {"type": "string", "minLength": 1},
                    "source": {"$ref": "#/$defs/formal_expr"},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "on", "expr", "relation", "value", "scope_identity"],
                "properties": {
                    "type": {"const": "value_constraint"},
                    "on": {"type": ["string", "null"]},
                    "expr": {"$ref": "#/$defs/formal_expr"},
                    "relation": {"const": "eq"},
                    "value": {"type": "integer", "minimum": 0},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "prerequisites", "after", "scope_identity"],
                "properties": {
                    "type": {"const": "join"},
                    "prerequisites": _string_list(min_items=2),
                    "after": {"type": "string", "minLength": 1},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "whole", "parts", "relation", "scope_identity"],
                "properties": {
                    "type": {"const": "occurrence_partition"},
                    "whole": {"type": "string", "minLength": 1},
                    "parts": _string_list(min_items=1),
                    "relation": {"const": "same_cycle_exactly_one"},
                    "scope_identity": {"type": "null"},
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "type", "occurrence", "completion", "index", "domain",
                    "cardinality", "scope_identity"
                ],
                "properties": {
                    "type": {"const": "indexed_complete"},
                    "occurrence": {"type": "string", "minLength": 1},
                    "completion": {"type": "string", "minLength": 1},
                    "index": {"type": "string", "minLength": 1},
                    "domain": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["start", "end_exclusive"],
                        "properties": {
                            "start": {"type": "integer", "minimum": 0},
                            "end_exclusive": {"type": "integer", "minimum": 1},
                        },
                    },
                    "cardinality": {"const": "exactly_once"},
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["type", "on", "spec", "bindings", "scope_identity"],
                "properties": {
                    "type": {"const": "spec_relation"},
                    "on": {"type": ["string", "null"]},
                    "spec": {"const": "tilelink.ClientMetadata.onProbe"},
                    "bindings": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "param",
                            "current_state",
                            "dirty",
                            "report",
                            "next_state",
                        ],
                        "properties": {
                            "param": {"type": "string", "minLength": 1},
                            "current_state": {"type": "string", "minLength": 1},
                            "dirty": {"type": "string", "minLength": 1},
                            "report": {"type": "string", "minLength": 1},
                            "next_state": {"type": "string", "minLength": 1},
                        },
                    },
                    "scope_identity": scope,
                    "scope_index": index_scope,
                },
            },
        ]
    }


def expr_to_symbolic(expr: dict[str, Any]) -> str:
    op = expr.get("op")
    if op == "signal":
        return str(expr["name"])
    if op == "slice":
        return f"bits({expr_to_symbolic(expr['value'])}, {int(expr['hi'])}, {int(expr['lo'])})"
    if op == "shr":
        return f"shr({expr_to_symbolic(expr['value'])}, {int(expr['amount'])})"
    if op == "bit":
        return f"bits({expr_to_symbolic(expr['value'])}, {int(expr['index'])}, {int(expr['index'])})"
    if op == "const":
        return str(int(expr["value"]))
    if op == "index_var":
        return str(expr["name"])
    if op == "lookup":
        return f"{expr_to_symbolic(expr['value'])}[{expr_to_symbolic(expr['index'])}]"
    raise ValueError(f"unsupported formal expression operator: {op!r}")


def expr_signals(expr: dict[str, Any]) -> set[str]:
    op = expr.get("op")
    if op == "signal":
        return {str(expr["name"])}
    if op in {"slice", "shr", "bit"}:
        return expr_signals(expr["value"])
    if op == "const":
        return set()
    if op == "index_var":
        return set()
    if op == "lookup":
        return expr_signals(expr["value"]) | expr_signals(expr["index"])
    raise ValueError(f"unsupported formal expression operator: {op!r}")


def expr_index_vars(expr: dict[str, Any]) -> set[str]:
    op = expr.get("op")
    if op == "index_var":
        return {str(expr["name"])}
    if op in {"signal", "const"}:
        return set()
    if op in {"slice", "shr", "bit"}:
        return expr_index_vars(expr["value"])
    if op == "lookup":
        return expr_index_vars(expr["value"]) | expr_index_vars(expr["index"])
    raise ValueError(f"unsupported formal expression operator: {op!r}")


def compile_formal_axiom(formal: dict[str, Any]) -> dict[str, Any]:
    """Compile one formal axiom AST into the deterministic proof-obligation DSL.

    This function is the semantic bridge by construction: there is no separate
    LLM-authored validation program. Unsupported forms fail closed.
    """

    shape_errors = validate_formal_axiom_shape(formal)
    if shape_errors:
        raise ValueError("; ".join(shape_errors))

    axiom_type = formal.get("type")
    occurrences: set[str] = set()
    predicates: set[str] = set()
    identities: set[str] = set()
    signals: set[str] = set()

    def add_scope() -> None:
        identity = formal.get("scope_identity")
        if identity:
            identities.add(str(identity))

    def scoped_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
        scope_index = formal.get("scope_index")
        if scope_index:
            arguments = dict(arguments)
            arguments["scope_index"] = dict(scope_index)
        return arguments

    if axiom_type == "forbid_when":
        occurrences.add(formal["occurrence"])
        predicates.add(formal["predicate"])
        add_scope()
        return {
            "checker": "forbid_when",
            "arguments": scoped_arguments({
                "occurrence": formal["occurrence"],
                "predicate": formal["predicate"],
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "conservation",
        }

    if axiom_type == "identity_flow":
        identities.add(formal["identity"])
        capture = formal["capture"]
        occurrences.add(capture["on"])
        signals.add(capture["source"])
        signals.add(capture["carrier"])
        projections = []
        for projection in formal["projections"]:
            occurrences.add(projection["on"])
            signals.add(projection["target"])
            signals.update(expr_signals(projection["expr"]))
            projections.append(
                {
                    "target": projection["target"],
                    "source": expr_to_symbolic(projection["expr"]),
                }
            )
        return {
            "checker": "identity_projection",
            "arguments": {
                "identity_key": formal["identity"],
                "accepted_by": capture["on"],
                "capture_source": capture["source"],
                "projections": projections,
            },
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "identity_flow",
        }

    if axiom_type == "exclusion":
        occurrences.add(formal["left"])
        occurrences.update(formal["rights"])
        add_scope()
        return {
            "checker": "transaction_exclusion",
            "arguments": scoped_arguments({"left": formal["left"], "rights": list(formal["rights"])}),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "exclusion",
        }

    if axiom_type == "ordered_before":
        occurrences.update([formal["before"], formal["after"]])
        required_prior = formal.get("required_prior")
        if required_prior:
            occurrences.add(required_prior)
        add_scope()
        return {
            "checker": "history_order",
            "arguments": scoped_arguments({
                "before": formal["before"],
                "after": formal["after"],
                **({"required_prior": required_prior} if required_prior else {}),
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "ordering",
        }

    if axiom_type == "ordered_chain":
        occurrences.update(formal["sequence"])
        add_scope()
        return {
            "checker": "history_chain",
            "arguments": scoped_arguments({"sequence": list(formal["sequence"])}),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "ordering",
        }

    if axiom_type == "signal_equality":
        if formal.get("on"):
            occurrences.add(formal["on"])
        add_scope()
        signals.add(formal["target"])
        signals.update(expr_signals(formal["source"]))
        source = expr_to_symbolic(formal["source"])
        return {
            "checker": "signal_alias",
            "arguments": scoped_arguments({
                "target": formal["target"],
                "source": source,
                **({"on": formal["on"]} if formal.get("on") else {}),
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "state_update",
        }

    if axiom_type == "value_constraint":
        if formal.get("on"):
            occurrences.add(formal["on"])
        add_scope()
        expr = formal["expr"]
        signals.update(expr_signals(expr))
        if formal["relation"] != "eq" or expr.get("op") != "bit" or expr["value"].get("op") != "signal":
            raise ValueError("value_constraint currently supports equality on one bit of one signal")
        return {
            "checker": "constant_bit",
            "arguments": scoped_arguments({
                "signal": expr["value"]["name"],
                "bit": int(expr["index"]),
                "expected": int(formal["value"]),
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "payload_constraint",
        }

    if axiom_type == "join":
        occurrences.update(formal["prerequisites"])
        occurrences.add(formal["after"])
        add_scope()
        return {
            "checker": "history_join",
            "arguments": scoped_arguments({
                "prerequisites": list(formal["prerequisites"]),
                "after": formal["after"],
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "ordering",
        }

    if axiom_type == "occurrence_partition":
        occurrences.add(formal["whole"])
        occurrences.update(formal["parts"])
        add_scope()
        return {
            "checker": "occurrence_partition",
            "arguments": {
                "whole": formal["whole"],
                "parts": list(formal["parts"]),
                "relation": formal["relation"],
            },
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "conservation",
        }

    if axiom_type == "indexed_complete":
        occurrences.update([formal["occurrence"], formal["completion"]])
        add_scope()
        return {
            "checker": "indexed_coverage",
            "arguments": scoped_arguments({
                "occurrence": formal["occurrence"],
                "completion": formal["completion"],
                "index": formal["index"],
                "domain": dict(formal["domain"]),
                "cardinality": formal["cardinality"],
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "conservation",
        }

    if axiom_type == "spec_relation":
        if formal.get("on"):
            occurrences.add(formal["on"])
        add_scope()
        if formal["spec"] != "tilelink.ClientMetadata.onProbe":
            raise ValueError(f"unsupported reference spec: {formal['spec']!r}")
        bindings = formal["bindings"]
        signals.update(bindings.values())
        return {
            "checker": "tilelink_on_probe_spec",
            "arguments": scoped_arguments({
                "param_signal": bindings["param"],
                "current_state_signal": bindings["current_state"],
                "dirty_signal": bindings["dirty"],
                "report_signal": bindings["report"],
                "next_state_signal": bindings["next_state"],
            }),
            "references": _refs(occurrences, predicates, identities, signals),
            "kind": "state_update",
        }

    raise ValueError(f"unsupported formal axiom type: {axiom_type!r}")


def _refs(
    occurrences: set[str], predicates: set[str], identities: set[str], signals: set[str]
) -> dict[str, list[str]]:
    return {
        "occurrences": sorted(occurrences),
        "predicates": sorted(predicates),
        "identities": sorted(identities),
        "signals": sorted(signals),
    }


def render_formal_axiom(formal: dict[str, Any]) -> str:
    """Human-readable rendering derived only from the formal AST."""

    t = formal.get("type")
    scope = formal.get("scope_identity")
    suffix = f" [same {scope}]" if scope else ""
    scope_index = formal.get("scope_index")
    if scope_index:
        suffix += f" [same index {scope_index['name']}]"
    if t == "forbid_when":
        return f"{formal['predicate']} => !{formal['occurrence']}{suffix}"
    if t == "identity_flow":
        capture = formal["capture"]
        return (
            f"capture {formal['identity']} := {capture['source']} on {capture['on']}; "
            f"preserve {len(formal['projections'])} exact identity projections"
        )
    if t == "exclusion":
        return f"{formal['left']} excludes {{{', '.join(formal['rights'])}}}{suffix}"
    if t == "ordered_before":
        prior = f" after {formal['required_prior']}" if formal.get("required_prior") else ""
        return f"{formal['before']} <mu {formal['after']}{prior}{suffix}"
    if t == "ordered_chain":
        return " <mu ".join(formal["sequence"]) + suffix
    if t == "signal_equality":
        on = f" on {formal['on']}" if formal.get("on") else ""
        return f"{formal['target']} = {expr_to_symbolic(formal['source'])}{on}{suffix}"
    if t == "value_constraint":
        on = f" on {formal['on']}" if formal.get("on") else ""
        return f"{expr_to_symbolic(formal['expr'])} == {formal['value']}{on}{suffix}"
    if t == "join":
        return f"{{{', '.join(formal['prerequisites'])}}} <mu {formal['after']}{suffix}"
    if t == "occurrence_partition":
        return (
            f"{formal['whole']} <=> exactly_one_same_cycle"
            f"({{{', '.join(formal['parts'])}}}){suffix}"
        )
    if t == "indexed_complete":
        domain = formal["domain"]
        return (
            f"{formal['completion']} => forall {formal['index']} in "
            f"[{domain['start']}, {domain['end_exclusive']}): "
            f"count({formal['occurrence']}({formal['index']})) = 1{suffix}"
        )
    if t == "spec_relation":
        on = f" on {formal['on']}" if formal.get("on") else ""
        return f"bindings satisfy {formal['spec']}{on}{suffix}"
    return f"<unsupported formal axiom {t!r}>"


def validate_formal_expr_shape(expr: Any, path: str = "expr") -> list[str]:
    if not isinstance(expr, dict):
        return [f"{path} must be an object"]
    op = expr.get("op")
    specs: dict[str, tuple[set[str], set[str]]] = {
        "signal": ({"op", "name"}, {"op", "name"}),
        "slice": ({"op", "value", "hi", "lo"}, {"op", "value", "hi", "lo"}),
        "shr": ({"op", "value", "amount"}, {"op", "value", "amount"}),
        "bit": ({"op", "value", "index"}, {"op", "value", "index"}),
        "const": ({"op", "value"}, {"op", "value"}),
        "index_var": ({"op", "name"}, {"op", "name"}),
        "lookup": ({"op", "value", "index"}, {"op", "value", "index"}),
    }
    if op not in specs:
        return [f"{path}.op {op!r} is unsupported"]
    required, allowed = specs[op]
    errors = [f"{path} missing {key!r}" for key in sorted(required - set(expr))]
    errors.extend(f"{path} has unsupported field {key!r}" for key in sorted(set(expr) - allowed))
    if op in {"slice", "shr", "bit"} and "value" in expr:
        errors.extend(validate_formal_expr_shape(expr["value"], f"{path}.value"))
    if op == "lookup":
        if "value" in expr:
            errors.extend(validate_formal_expr_shape(expr["value"], f"{path}.value"))
        if "index" in expr:
            errors.extend(validate_formal_expr_shape(expr["index"], f"{path}.index"))
    return errors


def validate_formal_axiom_shape(formal: Any) -> list[str]:
    if not isinstance(formal, dict):
        return ["formal axiom must be an object"]
    t = formal.get("type")
    specs: dict[str, tuple[set[str], set[str]]] = {
        "forbid_when": (
            {"type", "occurrence", "predicate", "scope_identity"},
            {"type", "occurrence", "predicate", "scope_identity", "scope_index"},
        ),
        "identity_flow": (
            {"type", "identity", "capture", "projections"},
            {"type", "identity", "capture", "projections"},
        ),
        "exclusion": (
            {"type", "left", "rights", "scope_identity"},
            {"type", "left", "rights", "scope_identity", "scope_index"},
        ),
        "ordered_before": (
            {"type", "before", "after", "required_prior", "scope_identity"},
            {"type", "before", "after", "required_prior", "scope_identity", "scope_index"},
        ),
        "ordered_chain": (
            {"type", "sequence", "scope_identity"},
            {"type", "sequence", "scope_identity", "scope_index"},
        ),
        "signal_equality": (
            {"type", "on", "target", "source", "scope_identity"},
            {"type", "on", "target", "source", "scope_identity", "scope_index"},
        ),
        "value_constraint": (
            {"type", "on", "expr", "relation", "value", "scope_identity"},
            {"type", "on", "expr", "relation", "value", "scope_identity", "scope_index"},
        ),
        "join": (
            {"type", "prerequisites", "after", "scope_identity"},
            {"type", "prerequisites", "after", "scope_identity", "scope_index"},
        ),
        "occurrence_partition": (
            {"type", "whole", "parts", "relation", "scope_identity"},
            {"type", "whole", "parts", "relation", "scope_identity"},
        ),
        "indexed_complete": (
            {"type", "occurrence", "completion", "index", "domain", "cardinality", "scope_identity"},
            {"type", "occurrence", "completion", "index", "domain", "cardinality", "scope_identity", "scope_index"},
        ),
        "spec_relation": (
            {"type", "on", "spec", "bindings", "scope_identity"},
            {"type", "on", "spec", "bindings", "scope_identity", "scope_index"},
        ),
    }
    if t not in specs:
        return [f"formal axiom type {t!r} is unsupported"]
    required, allowed = specs[t]
    errors = [f"formal axiom missing {key!r}" for key in sorted(required - set(formal))]
    errors.extend(f"formal axiom has unsupported field {key!r}" for key in sorted(set(formal) - allowed))

    scope_index = formal.get("scope_index")
    if scope_index is not None:
        if not isinstance(scope_index, dict):
            errors.append("scope_index must be an object or null")
        elif set(scope_index) != {"name", "relation"}:
            errors.append("scope_index must contain exactly name/relation")
        else:
            if not isinstance(scope_index.get("name"), str) or not scope_index.get("name"):
                errors.append("scope_index.name must be a non-empty string")
            if scope_index.get("relation") != "same":
                errors.append("scope_index.relation currently supports only 'same'")

    if t == "identity_flow":
        capture = formal.get("capture")
        if not isinstance(capture, dict):
            errors.append("identity_flow.capture must be an object")
        else:
            capture_allowed = {"on", "source", "carrier"}
            errors.extend(
                f"identity_flow.capture has unsupported field {key!r}"
                for key in sorted(set(capture) - capture_allowed)
            )
            errors.extend(
                f"identity_flow.capture missing {key!r}"
                for key in sorted(capture_allowed - set(capture))
            )
        projections = formal.get("projections")
        if not isinstance(projections, list) or not projections:
            errors.append("identity_flow.projections must be a non-empty list")
        else:
            for index, projection in enumerate(projections):
                path = f"identity_flow.projections[{index}]"
                if not isinstance(projection, dict):
                    errors.append(f"{path} must be an object")
                    continue
                allowed_projection = {"on", "target", "expr"}
                errors.extend(
                    f"{path} has unsupported field {key!r}"
                    for key in sorted(set(projection) - allowed_projection)
                )
                errors.extend(
                    f"{path} missing {key!r}"
                    for key in sorted(allowed_projection - set(projection))
                )
                if "expr" in projection:
                    errors.extend(validate_formal_expr_shape(projection["expr"], f"{path}.expr"))
    elif t == "signal_equality" and "source" in formal:
        errors.extend(validate_formal_expr_shape(formal["source"], "signal_equality.source"))
    elif t == "value_constraint" and "expr" in formal:
        errors.extend(validate_formal_expr_shape(formal["expr"], "value_constraint.expr"))
    elif t == "join":
        prerequisites = formal.get("prerequisites")
        if not isinstance(prerequisites, list) or len(prerequisites) < 2:
            errors.append("join.prerequisites must contain at least two occurrences")
        elif len(set(prerequisites)) != len(prerequisites):
            errors.append("join.prerequisites must be unique")
    elif t == "occurrence_partition":
        parts = formal.get("parts")
        if formal.get("scope_identity") is not None:
            errors.append(
                "occurrence_partition.scope_identity is currently required to be null; "
                "payload identity flow must be stated separately"
            )
        if formal.get("relation") != "same_cycle_exactly_one":
            errors.append(
                "occurrence_partition.relation currently supports only "
                "'same_cycle_exactly_one'"
            )
        if not isinstance(parts, list) or not parts:
            errors.append("occurrence_partition.parts must contain at least one occurrence")
        elif len(set(parts)) != len(parts):
            errors.append("occurrence_partition.parts must be unique")
        elif formal.get("whole") in parts:
            errors.append("occurrence_partition.whole must not also be a part")
    elif t == "indexed_complete":
        domain = formal.get("domain")
        if formal.get("cardinality") != "exactly_once":
            errors.append("indexed_complete.cardinality currently supports only 'exactly_once'")
        if not isinstance(domain, dict):
            errors.append("indexed_complete.domain must be an object")
        else:
            if set(domain) != {"start", "end_exclusive"}:
                errors.append("indexed_complete.domain must contain exactly start/end_exclusive")
            else:
                start = domain.get("start")
                end = domain.get("end_exclusive")
                if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
                    errors.append("indexed_complete.domain must satisfy 0 <= start < end_exclusive")
    elif t == "spec_relation":
        bindings = formal.get("bindings")
        required_bindings = {"param", "current_state", "dirty", "report", "next_state"}
        if not isinstance(bindings, dict):
            errors.append("spec_relation.bindings must be an object")
        else:
            errors.extend(
                f"spec_relation.bindings has unsupported field {key!r}"
                for key in sorted(set(bindings) - required_bindings)
            )
            errors.extend(
                f"spec_relation.bindings missing {key!r}"
                for key in sorted(required_bindings - set(bindings))
            )
    return errors
