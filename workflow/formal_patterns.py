from __future__ import annotations

from itertools import product
import re
from typing import Any

from .semantic import _call, _literal, _statement_rhs


STRUCTURALLY_SUPPORTED = "STRUCTURALLY_SUPPORTED"
STRUCTURAL_UNKNOWN = "STRUCTURAL_UNKNOWN"

_SIMPLE_REF_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.$]*$")
_ARRAY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.$]*)\[(.+)\]$")
_REF_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_.$]*(?:\[[^\]]+\])?(?:\.[A-Za-z_][A-Za-z0-9_$]*)*$"
)


def _under_state(model: Any, ref: str) -> bool:
    text = ref.strip()
    return any(
        text == str(root)
        or text.startswith(str(root) + ".")
        or text.startswith(str(root) + "[")
        for root in getattr(model, "state_roots", set())
    )


def _rhs(model: Any, ref: str) -> str | None:
    fn = getattr(model, "rhs", None)
    if not callable(fn):
        return None
    value = fn(ref.strip())
    return value if isinstance(value, str) else None


def _value_key(
    model: Any,
    expr: str,
    *,
    opaque: set[str] | None = None,
    seen: set[str] | None = None,
) -> tuple[Any, ...]:
    text = expr.strip()
    opaque = opaque or set()
    seen = seen or set()
    lit = _literal(text)
    if lit is not None:
        return ("lit", int(lit))
    if _REF_RE.fullmatch(text):
        if text in opaque or text in seen or _under_state(model, text):
            return ("ref", text)
        nested = _rhs(model, text)
        if nested is None:
            return ("ref", text)
        return _value_key(model, nested, opaque=opaque, seen=seen | {text})
    call = _call(text)
    if call is None:
        return ("raw", text)
    return (
        "call",
        call[0],
        tuple(_value_key(model, arg, opaque=opaque, seen=seen) for arg in call[1]),
    )


def _initial_bool_refs(model: Any, candidate: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for occurrence in candidate.get("occurrences", []):
        grounding = occurrence.get("grounding", {})
        refs.update(str(x) for x in grounding.get("signals_true", []))
        refs.update(str(x) for x in grounding.get("signals_false", []))
        for physical_id in occurrence.get("physical_event_ids", []):
            event_fn = getattr(model, "_event_info", None)
            event = event_fn(physical_id) if callable(event_fn) else None
            if isinstance(event, dict):
                for key in ("valid", "ready"):
                    if isinstance(event.get(key), str):
                        refs.add(str(event[key]))
    for predicate in candidate.get("predicates", []):
        source = predicate.get("grounding", {}).get("source_signal")
        if isinstance(source, str):
            refs.add(source)
    return refs


def _is_bool_expr(
    model: Any,
    expr: str,
    bool_refs: set[str],
    seen: set[str] | None = None,
) -> bool:
    text = expr.strip()
    seen = seen or set()
    lit = _literal(text)
    if lit is not None:
        return int(lit) in {0, 1}
    if _REF_RE.fullmatch(text):
        if text in bool_refs:
            return True
        if text in seen or _under_state(model, text):
            return False
        nested = _rhs(model, text)
        return False if nested is None else _is_bool_expr(model, nested, bool_refs, seen | {text})
    call = _call(text)
    if call is None:
        return False
    name, args = call
    if name in {"eq", "neq"}:
        return True
    if name in {"and", "or"} and len(args) == 2:
        return _is_bool_expr(model, args[0], bool_refs, seen) and _is_bool_expr(
            model, args[1], bool_refs, seen
        )
    if name == "not" and len(args) == 1:
        return _is_bool_expr(model, args[0], bool_refs, seen)
    if name == "mux" and len(args) == 3:
        return all(_is_bool_expr(model, arg, bool_refs, seen) for arg in args)
    return False


def _propagate_bool_refs(
    model: Any,
    expr: str,
    bool_refs: set[str],
    seen: set[str] | None = None,
) -> None:
    text = expr.strip()
    seen = seen or set()
    if _REF_RE.fullmatch(text):
        if text in seen:
            return
        bool_refs.add(text)
        if _under_state(model, text):
            return
        nested = _rhs(model, text)
        if nested is not None:
            _propagate_bool_refs(model, nested, bool_refs, seen | {text})
        return
    call = _call(text)
    if call is None:
        return
    name, args = call
    if name in {"and", "or"} and len(args) == 2:
        for arg in args:
            _propagate_bool_refs(model, arg, bool_refs, seen)
    elif name == "not" and len(args) == 1:
        _propagate_bool_refs(model, args[0], bool_refs, seen)
    elif name == "mux" and len(args) == 3:
        for arg in args:
            _propagate_bool_refs(model, arg, bool_refs, seen)
    elif name in {"eq", "neq"} and len(args) == 2:
        left = _literal(args[0])
        right = _literal(args[1])
        other = args[1] if left is not None else args[0] if right is not None else None
        lit = left if left is not None else right
        if other is not None and lit in {0, 1} and _is_bool_expr(model, other, bool_refs):
            _propagate_bool_refs(model, other, bool_refs, seen)


def _bool_refs(model: Any, candidate: dict[str, Any]) -> set[str]:
    refs = _initial_bool_refs(model, candidate)
    while True:
        before = len(refs)
        for root in list(refs):
            if _under_state(model, root):
                continue
            nested = _rhs(model, root)
            if nested is not None:
                _propagate_bool_refs(model, nested, refs, {root})
        if len(refs) == before:
            return refs


def _const(value: bool) -> tuple[Any, ...]:
    return ("const", bool(value))


def _not(expr: tuple[Any, ...]) -> tuple[Any, ...]:
    if expr[0] == "const":
        return _const(not bool(expr[1]))
    if expr[0] == "not":
        return expr[1]
    return ("not", expr)


def _and(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[Any, ...]:
    if left == _const(False) or right == _const(False):
        return _const(False)
    if left == _const(True):
        return right
    if right == _const(True):
        return left
    if left == right:
        return left
    if left == _not(right) or right == _not(left):
        return _const(False)
    return ("and", left, right)


def _or(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[Any, ...]:
    if left == _const(True) or right == _const(True):
        return _const(True)
    if left == _const(False):
        return right
    if right == _const(False):
        return left
    if left == right:
        return left
    if left == _not(right) or right == _not(left):
        return _const(True)
    return ("or", left, right)


def _bool_expr(
    model: Any,
    bool_refs: set[str],
    expr: str,
    *,
    opaque: set[str] | None = None,
    seen: set[str] | None = None,
) -> tuple[Any, ...] | None:
    text = expr.strip()
    opaque = opaque or set()
    seen = seen or set()
    lit = _literal(text)
    if lit is not None:
        if int(lit) in {0, 1}:
            return _const(bool(lit))
        return ("atom", ("nz", _value_key(model, text, opaque=opaque)))
    if _REF_RE.fullmatch(text):
        if text in opaque or _under_state(model, text):
            return ("atom", ("nz", ("ref", text)))
        if text in seen:
            return None
        nested = _rhs(model, text)
        if nested is not None and text in bool_refs:
            return _bool_expr(model, bool_refs, nested, opaque=opaque, seen=seen | {text})
        return ("atom", ("nz", _value_key(model, text, opaque=opaque)))
    call = _call(text)
    if call is None:
        return None
    name, args = call
    if name in {"and", "or"} and len(args) == 2:
        left = _bool_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        right = _bool_expr(model, bool_refs, args[1], opaque=opaque, seen=seen)
        if left is None or right is None:
            return None
        return _and(left, right) if name == "and" else _or(left, right)
    if name == "not" and len(args) == 1:
        value = _bool_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        return None if value is None else _not(value)
    if name == "mux" and len(args) == 3:
        select = _bool_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        high = _bool_expr(model, bool_refs, args[1], opaque=opaque, seen=seen)
        low = _bool_expr(model, bool_refs, args[2], opaque=opaque, seen=seen)
        if select is None or high is None or low is None:
            return None
        return _or(_and(select, high), _and(_not(select), low))
    if name in {"eq", "neq"} and len(args) == 2:
        left = _literal(args[0])
        right = _literal(args[1])
        value_expr = args[1] if left is not None else args[0] if right is not None else None
        literal = left if left is not None else right
        if value_expr is not None and literal == 0:
            if value_expr.strip() in bool_refs:
                value = _bool_expr(model, bool_refs, value_expr, opaque=opaque, seen=seen)
            else:
                value = ("atom", ("nz", _value_key(model, value_expr, opaque=opaque)))
            if value is None:
                return None
            return _not(value) if name == "eq" else value
        if value_expr is not None and literal == 1 and value_expr.strip() in bool_refs:
            value = _bool_expr(model, bool_refs, value_expr, opaque=opaque, seen=seen)
            if value is None:
                return None
            return value if name == "eq" else _not(value)
        return ("atom", ("pred", _value_key(model, text, opaque=opaque)))
    return ("atom", ("nz", _value_key(model, text, opaque=opaque)))


def _atoms(expr: tuple[Any, ...], out: set[tuple[Any, ...]] | None = None) -> set[tuple[Any, ...]]:
    if out is None:
        out = set()
    if expr[0] == "atom":
        out.add(expr[1])
    elif expr[0] == "not":
        _atoms(expr[1], out)
    elif expr[0] in {"and", "or"}:
        _atoms(expr[1], out)
        _atoms(expr[2], out)
    return out


def _eval(expr: tuple[Any, ...], env: dict[tuple[Any, ...], bool]) -> bool:
    if expr[0] == "const":
        return bool(expr[1])
    if expr[0] == "atom":
        return env[expr[1]]
    if expr[0] == "not":
        return not _eval(expr[1], env)
    if expr[0] == "and":
        return _eval(expr[1], env) and _eval(expr[2], env)
    if expr[0] == "or":
        return _eval(expr[1], env) or _eval(expr[2], env)
    raise ValueError(expr[0])


def _unsat(expr: tuple[Any, ...], max_atoms: int = 16) -> tuple[bool | None, int]:
    atoms = sorted(_atoms(expr), key=repr)
    if len(atoms) > max_atoms:
        return None, len(atoms)
    for values in product((False, True), repeat=len(atoms)):
        if _eval(expr, dict(zip(atoms, values))):
            return False, len(atoms)
    return True, len(atoms)


def _occurrence_condition(
    model: Any,
    candidate: dict[str, Any],
    occurrence_id: str,
    bool_refs: set[str],
    *,
    opaque: set[str] | None = None,
) -> tuple[Any, ...] | None:
    occurrence = next((x for x in candidate.get("occurrences", []) if x.get("id") == occurrence_id), None)
    if occurrence is None:
        return None
    grounding = occurrence.get("grounding", {})
    positive = [str(x) for x in grounding.get("signals_true", [])]
    negative = [str(x) for x in grounding.get("signals_false", [])]
    if not positive and not negative and occurrence.get("kind") == "boundary":
        physical = occurrence.get("physical_event_ids", [])
        if len(physical) == 1:
            event_fn = getattr(model, "_event_info", None)
            event = event_fn(physical[0]) if callable(event_fn) else None
            if isinstance(event, dict):
                positive.extend(str(event[key]) for key in ("valid", "ready") if isinstance(event.get(key), str))
    if not positive and not negative:
        return None
    result = _const(True)
    for signal in positive:
        value = _bool_expr(model, bool_refs, signal, opaque=opaque)
        if value is None:
            return None
        result = _and(result, value)
    for signal in negative:
        value = _bool_expr(model, bool_refs, signal, opaque=opaque)
        if value is None:
            return None
        result = _and(result, _not(value))
    return result


def _predicate_condition(
    model: Any,
    candidate: dict[str, Any],
    predicate_id: str,
    bool_refs: set[str],
) -> tuple[Any, ...] | None:
    predicate = next((x for x in candidate.get("predicates", []) if x.get("id") == predicate_id), None)
    if predicate is None:
        return None
    grounding = predicate.get("grounding", {})
    source = grounding.get("source_signal")
    if not isinstance(source, str):
        return None
    value = _bool_expr(model, bool_refs, source)
    if value is None:
        return None
    return _not(value) if grounding.get("negated") else value


def prove_combinational_forbid_when(
    model: Any,
    candidate: dict[str, Any],
    *,
    occurrence: str,
    predicate: str,
) -> dict[str, Any]:
    """Prove occurrence && predicate is UNSAT in the exact local Boolean cone."""
    refs = _bool_refs(model, candidate)
    occ = _occurrence_condition(model, candidate, occurrence, refs)
    pred = _predicate_condition(model, candidate, predicate, refs)
    if occ is None or pred is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no exact combinational condition"}
    unsat, atoms = _unsat(_and(occ, pred))
    if unsat is True:
        return {
            "status": STRUCTURALLY_SUPPORTED,
            "proof": f"{occurrence} and {predicate} have an unsatisfiable local Boolean conjunction",
            "proof_domain": "exact-combinational-exclusion",
            "atom_count": atoms,
        }
    if unsat is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"Boolean cone exceeds atom limit ({atoms})"}
    return {
        "status": STRUCTURAL_UNKNOWN,
        "reason": "local Boolean reasoning does not prove exclusion",
        "atom_count": atoms,
    }


def _resolve_literal(model: Any, expr: str, seen: set[str] | None = None) -> int | None:
    text = expr.strip()
    value = _literal(text)
    if value is not None:
        return int(value)
    seen = seen or set()
    if text in seen or _under_state(model, text):
        return None
    nested = _rhs(model, text)
    return None if nested is None else _resolve_literal(model, nested, seen | {text})


def _index_info(occurrence: dict[str, Any], name: str) -> tuple[str, dict[str, int]] | None:
    metadata = occurrence.get("index")
    if not isinstance(metadata, dict) or metadata.get("name") != name:
        return None
    expr, domain = metadata.get("expr"), metadata.get("domain")
    if not isinstance(expr, dict) or expr.get("op") != "signal" or not isinstance(expr.get("name"), str):
        return None
    if not isinstance(domain, dict):
        return None
    start, end = domain.get("start"), domain.get("end_exclusive")
    if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
        return None
    return str(expr["name"]), {"start": start, "end_exclusive": end}


def _array_lhs(lhs: str) -> tuple[str, str] | None:
    match = _ARRAY_RE.fullmatch(lhs.strip())
    return None if match is None else (match.group(1), match.group(2).strip())


def _creator_guard_proof(
    model: Any,
    before_obj: dict[str, Any],
    creator: dict[str, Any],
    storage: str,
) -> dict[str, Any] | None:
    """Use control edges + enclosing when IDs so else polarity is never guessed."""
    handoff = getattr(model, "handoff", None)
    if not isinstance(handoff, dict):
        return None
    creator_id = int(creator.get("id", -1))
    for signal in [str(x) for x in before_obj.get("grounding", {}).get("signals_true", [])]:
        when_ids = {
            int(statement.get("id", -1))
            for statement in model.statements.values()
            if statement.get("kind") == "when"
            and re.fullmatch(rf"when\s+{re.escape(signal)}\s*:\s*", str(statement.get("text", "")).strip())
        }
        for edge in handoff.get("dependency_edges", []):
            dst = str(edge.get("dst", ""))
            ids = {int(x) for x in edge.get("statement_ids", [])}
            if (
                edge.get("kind") == "control"
                and edge.get("src") == signal
                and (dst == storage or dst.startswith(storage + "[") or dst.startswith(storage + "."))
                and creator_id in ids
                and ids & when_ids
            ):
                return {"signal": signal, "creator": creator_id, "when_ids": sorted(ids & when_ids)}
    return None


def _reset_zero(model: Any, storage: str, domain: dict[str, int]) -> dict[str, Any] | None:
    reset_expr: str | None = None
    reset_id: int | None = None
    for statement in model.statements.values():
        text = str(statement.get("text", "")).strip()
        if statement.get("kind") == "regreset" and text.startswith(f"regreset {storage} "):
            reset_expr = text.rsplit(",", 1)[-1].strip()
            reset_id = int(statement.get("id", -1))
            break
    if reset_expr is None:
        return None
    for index in range(domain["start"], domain["end_exclusive"]):
        value = _resolve_literal(model, f"{reset_expr}[{index}]")
        if value != 0:
            return None
    return {"reset_statement": reset_id, "reset_expr": reset_expr}


def prove_same_index_valid_token_provenance(
    model: Any,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
    scope_index: dict[str, str],
    required_prior: str | None = None,
) -> dict[str, Any]:
    """Prove same-index history from a bounded valid/token-array invariant."""
    if required_prior is not None or scope_index.get("relation") != "same":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported indexed history shape"}
    name = scope_index.get("name")
    if not isinstance(name, str):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "missing index name"}
    before_obj = next((x for x in candidate.get("occurrences", []) if x.get("id") == before), None)
    after_obj = next((x for x in candidate.get("occurrences", []) if x.get("id") == after), None)
    if before_obj is None or after_obj is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "before/after occurrence missing"}
    before_meta, after_meta = _index_info(before_obj, name), _index_info(after_obj, name)
    if before_meta is None or after_meta is None or before_meta[1] != after_meta[1]:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "incompatible occurrence index metadata"}
    before_index, domain = before_meta
    after_index, _ = after_meta
    before_evidence = {int(x) for x in before_obj.get("evidence_statement_ids", [])}

    creators: list[tuple[str, dict[str, Any]]] = []
    for statement in model.statements.values():
        parsed = _statement_rhs(statement)
        if parsed is None or int(statement.get("id", -1)) not in before_evidence:
            continue
        lhs, rhs = parsed
        array = _array_lhs(lhs)
        if (
            array is not None
            and _resolve_literal(model, rhs) == 1
            and _value_key(model, array[1]) == _value_key(model, before_index)
        ):
            creators.append((array[0], statement))
    storages = {storage for storage, _ in creators}
    if len(storages) != 1 or not creators:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no unique token store created by before"}
    storage = next(iter(storages))
    reset = _reset_zero(model, storage, domain)
    if reset is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"{storage} reset-to-zero not proved"}

    creator_ids: list[int] = []
    creator_guards: list[dict[str, Any]] = []
    for _, statement in creators:
        guard = _creator_guard_proof(model, before_obj, statement, storage)
        if guard is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "creator positive-branch guard not proved"}
        creator_ids.append(int(statement["id"]))
        creator_guards.append(guard)

    refs = _bool_refs(model, candidate)
    writes: list[dict[str, Any]] = []
    for statement in model.statements.values():
        parsed = _statement_rhs(statement)
        if parsed is None:
            continue
        lhs, rhs = parsed
        array = _array_lhs(lhs)
        if array is None or array[0] != storage:
            continue
        statement_id = int(statement.get("id", -1))
        value = _resolve_literal(model, rhs)
        if value == 1:
            if statement_id not in creator_ids:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": "unaccounted writer can create a valid token",
                    "statement_id": statement_id,
                }
            writes.append({"statement_id": statement_id, "kind": "creator"})
            continue
        if value == 0:
            writes.append({"statement_id": statement_id, "kind": "clear"})
            continue

        local_refs = set(refs) | {lhs}
        _propagate_bool_refs(model, rhs, local_refs)
        rhs_expr = _bool_expr(model, local_refs, rhs, opaque={lhs})
        old = ("atom", ("nz", ("ref", lhs)))
        if rhs_expr is None or _unsat(_and(rhs_expr, _not(old)))[0] is not True:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "token writer is not proved false-preserving",
                "statement_id": statement_id,
            }
        writes.append({"statement_id": statement_id, "kind": "false-preserving"})

    token = f"{storage}[{after_index}]"
    after_refs = set(refs) | {token}
    after_cond = _occurrence_condition(model, candidate, after, after_refs, opaque={token})
    token_expr = ("atom", ("nz", ("ref", token)))
    if after_cond is None or _unsat(_and(after_cond, _not(token_expr)))[0] is not True:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"{after} does not require same-slot token"}

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"{after} requires {storage}[{after_index}]; all slots reset invalid, {before} is the only "
            f"creator, and every other {storage} writer clears or preserves false"
        ),
        "proof_domain": "exact-indexed-valid-token-provenance",
        "storage": storage,
        "domain": domain,
        "before_index": before_index,
        "after_index": after_index,
        "reset_proof": reset,
        "creator_statement_ids": sorted(creator_ids),
        "creator_guard_proofs": creator_guards,
        "classified_writes": sorted(writes, key=lambda item: item["statement_id"]),
    }


def _scalar_reset_zero(model: Any, storage: str) -> dict[str, Any] | None:
    for statement in model.statements.values():
        text = str(statement.get("text", "")).strip()
        if statement.get("kind") != "regreset" or not text.startswith(f"regreset {storage} "):
            continue
        reset_expr = text.rsplit(",", 1)[-1].strip()
        if _resolve_literal(model, reset_expr) != 0:
            return None
        return {
            "reset_statement": int(statement.get("id", -1)),
            "reset_expr": reset_expr,
        }
    return None


def _writer_activation(
    model: Any,
    storage: str,
    statement: dict[str, Any],
    bool_refs: set[str],
) -> tuple[tuple[Any, ...], dict[str, Any]] | None:
    """Recover an exact positive-`when` activation for one scalar writer.

    The dependency ledger does not encode negative `else` polarity.  Such a
    writer is therefore rejected instead of guessing its activation.
    """

    statement_id = int(statement.get("id", -1))
    handoff = getattr(model, "handoff", None)
    if not isinstance(handoff, dict):
        return None
    edges = [
        edge
        for edge in handoff.get("dependency_edges", [])
        if edge.get("kind") == "control"
        and edge.get("dst") == storage
        and statement_id in {int(x) for x in edge.get("statement_ids", [])}
    ]
    controls = sorted({str(edge.get("src")) for edge in edges if edge.get("src")})
    declared_controls = {str(x) for x in statement.get("control_reads", [])}
    if declared_controls and not controls:
        return None
    if not controls:
        return _const(True), {"kind": "unconditional", "control_signals": []}

    block_ids = {
        int(block_id)
        for edge in edges
        for block_id in edge.get("statement_ids", [])
        if int(block_id) != statement_id
    }
    blocks = [model.statements.get(block_id) for block_id in sorted(block_ids)]
    if any(block is None or block.get("kind") != "when" for block in blocks):
        return None

    activation = _const(True)
    for control in controls:
        expr = _bool_expr(model, bool_refs, control)
        if expr is None:
            return None
        activation = _and(activation, expr)
    return activation, {
        "kind": "positive-when-conjunction",
        "control_signals": controls,
        "control_statement_ids": sorted(block_ids),
    }


def prove_scalar_valid_token_provenance(
    model: Any,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
    required_prior: str | None = None,
) -> dict[str, Any]:
    """Prove scalar history from a reset-false Boolean token invariant.

    A successful certificate establishes that `after` requires one scalar
    token, the token resets false, every writer is accounted for, and every
    possible false-to-true transition implies `before`.  No module, signal, or
    protocol name is special-cased.
    """

    if required_prior is not None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "required_prior scalar provenance is unsupported"}
    before_obj = next((x for x in candidate.get("occurrences", []) if x.get("id") == before), None)
    after_obj = next((x for x in candidate.get("occurrences", []) if x.get("id") == after), None)
    if before_obj is None or after_obj is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "before/after occurrence missing"}

    refs = _bool_refs(model, candidate)
    before_cond = _occurrence_condition(model, candidate, before, refs)
    if before_cond is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"{before} has no exact Boolean occurrence condition"}

    successes: list[dict[str, Any]] = []
    rejected: dict[str, str] = {}
    for storage in sorted(str(root) for root in getattr(model, "state_roots", set())):
        if "[" in storage:
            continue
        token = ("atom", ("nz", ("ref", storage)))
        after_cond = _occurrence_condition(model, candidate, after, refs, opaque={storage})
        if after_cond is None or _unsat(_and(after_cond, _not(token)))[0] is not True:
            continue
        reset = _scalar_reset_zero(model, storage)
        if reset is None:
            rejected[storage] = "reset-to-zero not proved"
            continue

        writes: list[dict[str, Any]] = []
        creators: list[int] = []
        failed: str | None = None
        for statement in model.statements.values():
            if storage not in {str(x) for x in statement.get("drives", [])}:
                continue
            if statement.get("kind") in {"reg", "regreset"}:
                continue
            parsed = _statement_rhs(statement)
            if parsed is None or parsed[0].strip() != storage:
                failed = f"unparsed or non-scalar writer {statement.get('id')}"
                break
            statement_id = int(statement.get("id", -1))
            activation_info = _writer_activation(model, storage, statement, refs)
            if activation_info is None:
                failed = f"writer activation is not exact for statement {statement_id}"
                break
            activation, activation_certificate = activation_info
            writer_refs = set(refs) | {storage}
            _propagate_bool_refs(model, parsed[1], writer_refs)
            rhs_expr = _bool_expr(model, writer_refs, parsed[1], opaque={storage})
            if rhs_expr is None:
                failed = f"writer RHS is not an exact Boolean expression at statement {statement_id}"
                break

            false_to_true = _and(_and(activation, rhs_expr), _not(token))
            impossible, _ = _unsat(false_to_true)
            if impossible is True:
                writes.append({
                    "statement_id": statement_id,
                    "kind": "false-preserving",
                    "activation": activation_certificate,
                })
                continue

            implies_before, _ = _unsat(_and(false_to_true, _not(before_cond)))
            if implies_before is not True:
                failed = f"unaccounted writer can create a scalar token at statement {statement_id}"
                break
            creators.append(statement_id)
            writes.append({
                "statement_id": statement_id,
                "kind": "creator",
                "activation": activation_certificate,
            })

        if failed is not None:
            rejected[storage] = failed
            continue
        if not creators:
            rejected[storage] = "no false-to-true creator was found"
            continue
        successes.append({
            "status": STRUCTURALLY_SUPPORTED,
            "proof": (
                f"{after} requires scalar token {storage}; it resets false, every writer is accounted "
                f"for, and every false-to-true transition implies {before}"
            ),
            "proof_domain": "exact-scalar-valid-token-provenance",
            "storage": storage,
            "reset_proof": reset,
            "creator_statement_ids": sorted(creators),
            "classified_writes": sorted(writes, key=lambda item: item["statement_id"]),
        })

    if len(successes) == 1:
        return successes[0]
    if len(successes) > 1:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "multiple scalar token invariants can explain the requested history",
            "storages": sorted(item["storage"] for item in successes),
        }
    return {
        "status": STRUCTURAL_UNKNOWN,
        "reason": "no certified scalar valid-token provenance invariant was found",
        "rejected_storages": rejected,
    }
