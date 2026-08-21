from __future__ import annotations

import re
from typing import Any

from .axiom_ir import expr_to_symbolic
from .semantic import _call, _literal, _statement_rhs


STRUCTURALLY_SUPPORTED = "STRUCTURALLY_SUPPORTED"
STRUCTURAL_UNKNOWN = "STRUCTURAL_UNKNOWN"

_SIMPLE_REF_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.$]*$")
_ARRAY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.$]*)\[(.+)\]$")
_REF_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_$]*(?:(?:\.[A-Za-z_][A-Za-z0-9_$]*)|(?:\[[^\[\]]+\]))*$"
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
    arguments = tuple(
        _value_key(model, arg, opaque=opaque, seen=seen) for arg in call[1]
    )
    if call[0] in {"eq", "neq"} and len(arguments) == 2:
        arguments = tuple(sorted(arguments, key=repr))
    return (
        "call",
        call[0],
        arguments,
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


def _or_all(values: list[tuple[Any, ...]]) -> tuple[Any, ...]:
    result = _const(False)
    for value in values:
        result = _or(result, value)
    return result


def _literal_bits(text: str) -> list[tuple[Any, ...]] | None:
    value = _literal(text)
    if value is None:
        return None
    width_match = re.match(r"^UInt<(\d+)>", text.strip())
    width = int(width_match.group(1)) if width_match else max(1, int(value).bit_length())
    return [_const(bool((int(value) >> bit) & 1)) for bit in range(width)]


def _bit_vector_expr(
    model: Any,
    bool_refs: set[str],
    expr: str,
    *,
    opaque: set[str],
    seen: set[str],
) -> list[tuple[Any, ...]] | None:
    """Bit-blast the small FIRRTL integer fragment used by routing logic."""

    text = expr.strip()
    literal = _literal_bits(text)
    if literal is not None:
        return literal
    if _REF_RE.fullmatch(text):
        if text in bool_refs or _under_state(model, text):
            value = _bool_expr(model, bool_refs, text, opaque=opaque, seen=seen)
            return None if value is None else [value]
        if text in seen:
            return None
        nested = _rhs(model, text)
        if nested is None:
            return None
        return _bit_vector_expr(
            model,
            bool_refs,
            nested,
            opaque=opaque,
            seen=seen | {text},
        )
    call = _call(text)
    if call is None:
        return None
    name, args = call
    if name == "cat" and len(args) == 2:
        high = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        low = _bit_vector_expr(model, bool_refs, args[1], opaque=opaque, seen=seen)
        return None if high is None or low is None else [*low, *high]
    if name == "bits" and len(args) == 3:
        value = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        high = _literal(args[1])
        low = _literal(args[2])
        if value is None or high is None or low is None or low < 0 or high < low or high >= len(value):
            return None
        return value[int(low):int(high) + 1]
    if name == "shl" and len(args) == 2:
        value = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        amount = _literal(args[1])
        return None if value is None or amount is None or amount < 0 else [*_const_bits(int(amount)), *value]
    if name in {"and", "or", "xor"} and len(args) == 2:
        left = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        right = _bit_vector_expr(model, bool_refs, args[1], opaque=opaque, seen=seen)
        if left is None or right is None:
            return None
        width = max(len(left), len(right))
        left = [*left, *[_const(False)] * (width - len(left))]
        right = [*right, *[_const(False)] * (width - len(right))]
        if name == "and":
            return [_and(a, b) for a, b in zip(left, right)]
        if name == "or":
            return [_or(a, b) for a, b in zip(left, right)]
        return [_or(_and(a, _not(b)), _and(_not(a), b)) for a, b in zip(left, right)]
    if name == "not" and len(args) == 1:
        value = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        return None if value is None else [_not(bit) for bit in value]
    if name == "mux" and len(args) == 3:
        select = _bool_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        high = _bit_vector_expr(model, bool_refs, args[1], opaque=opaque, seen=seen)
        low = _bit_vector_expr(model, bool_refs, args[2], opaque=opaque, seen=seen)
        if select is None or high is None or low is None:
            return None
        # FIRRTL may retain a narrow literal zero on one mux arm while the
        # result is widened to the other arm.  Zero-extension is exact for a
        # known all-zero vector regardless of signedness; other width
        # mismatches remain unresolved rather than guessing extension rules.
        if len(high) != len(low):
            width = max(len(high), len(low))
            if len(high) < width and all(bit == _const(False) for bit in high):
                high = [*high, *_const_bits(width - len(high))]
            if len(low) < width and all(bit == _const(False) for bit in low):
                low = [*low, *_const_bits(width - len(low))]
        if len(high) != len(low):
            return None
        return [_or(_and(select, a), _and(_not(select), b)) for a, b in zip(high, low)]
    if name == "andr" and len(args) == 1:
        value = _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        if value is None:
            return None
        result = _const(True)
        for bit in value:
            result = _and(result, bit)
        return [result]
    if name in {"asUInt", "asSInt"} and len(args) == 1:
        return _bit_vector_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
    return None


def _const_bits(width: int) -> list[tuple[Any, ...]]:
    return [_const(False) for _ in range(width)]


def _selected_bit_expr(
    model: Any,
    bool_refs: set[str],
    expr: str,
    bit: int,
    *,
    opaque: set[str],
    seen: set[str],
) -> tuple[Any, ...] | None:
    """Resolve one bit without requiring every mux arm's complete width.

    This preserves correlations such as ``bits(mux(sc, 0, payload), 7, 7)``:
    the selected bit is known zero when ``sc`` is true even if the payload
    width/value is otherwise opaque.
    """

    text = expr.strip()
    literal = _literal(text)
    if literal is not None:
        width_match = re.match(r"^UInt<(\d+)>", text)
        if width_match is not None or bit < max(1, int(literal).bit_length()):
            return _const(bool((int(literal) >> bit) & 1))
        return ("atom", ("bit", bit, _value_key(model, text, opaque=opaque)))
    if _REF_RE.fullmatch(text):
        if text in opaque or _under_state(model, text) or text in seen:
            return ("atom", ("bit", bit, ("ref", text)))
        nested = _rhs(model, text)
        if nested is None:
            return ("atom", ("bit", bit, ("ref", text)))
        return _selected_bit_expr(
            model,
            bool_refs,
            nested,
            bit,
            opaque=opaque,
            seen=seen | {text},
        )
    call = _call(text)
    if call is None:
        return None
    name, args = call
    if name == "bits" and len(args) == 3:
        high = _literal(args[1])
        low = _literal(args[2])
        if high is None or low is None or bit < 0 or bit >= int(high) - int(low) + 1:
            return None
        return _selected_bit_expr(
            model,
            bool_refs,
            args[0],
            int(low) + bit,
            opaque=opaque,
            seen=seen,
        )
    if name == "mux" and len(args) == 3:
        select = _bool_expr(model, bool_refs, args[0], opaque=opaque, seen=seen)
        high = _selected_bit_expr(
            model, bool_refs, args[1], bit, opaque=opaque, seen=seen
        )
        low = _selected_bit_expr(
            model, bool_refs, args[2], bit, opaque=opaque, seen=seen
        )
        if select is None or high is None or low is None:
            return None
        return _or(_and(select, high), _and(_not(select), low))
    if name in {"and", "or", "xor"} and len(args) == 2:
        left = _selected_bit_expr(
            model, bool_refs, args[0], bit, opaque=opaque, seen=seen
        )
        right = _selected_bit_expr(
            model, bool_refs, args[1], bit, opaque=opaque, seen=seen
        )
        if left is None or right is None:
            return None
        if name == "and":
            return _and(left, right)
        if name == "or":
            return _or(left, right)
        return _or(_and(left, _not(right)), _and(_not(left), right))
    return ("atom", ("bit", bit, _value_key(model, text, opaque=opaque)))


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
            bits = _bit_vector_expr(
                model,
                bool_refs,
                nested,
                opaque=opaque,
                seen=seen | {text},
            )
            if bits is not None:
                return _or_all(bits)
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
    if name == "bits" and len(args) == 3:
        high = _literal(args[1])
        low = _literal(args[2])
        if high is not None and low is not None and high == low:
            return _selected_bit_expr(
                model,
                bool_refs,
                args[0],
                int(low),
                opaque=opaque,
                seen=seen,
            )
    if name in {"eq", "neq"} and len(args) == 2:
        left = _literal(args[0])
        right = _literal(args[1])
        if left is not None and right is not None:
            equal = int(left) == int(right)
            return _const(equal if name == "eq" else not equal)
        value_expr = args[1] if left is not None else args[0] if right is not None else None
        literal = left if left is not None else right
        if value_expr is not None and literal == 0:
            if value_expr.strip() in bool_refs:
                value = _bool_expr(model, bool_refs, value_expr, opaque=opaque, seen=seen)
            else:
                bits = _bit_vector_expr(
                    model,
                    bool_refs,
                    value_expr,
                    opaque=opaque,
                    seen=seen,
                )
                value = _or_all(bits) if bits is not None else (
                    "atom", ("nz", _value_key(model, value_expr, opaque=opaque))
                )
            if value is None:
                return None
            return _not(value) if name == "eq" else value
        if value_expr is not None and literal == 1:
            value = None
            if value_expr.strip() in bool_refs:
                value = _bool_expr(model, bool_refs, value_expr, opaque=opaque, seen=seen)
            else:
                bits = _bit_vector_expr(
                    model,
                    bool_refs,
                    value_expr,
                    opaque=opaque,
                    seen=seen,
                )
                if bits is not None and len(bits) == 1:
                    value = bits[0]
                else:
                    selected = _call(value_expr)
                    if (
                        selected is not None
                        and selected[0] == "bits"
                        and len(selected[1]) == 3
                        and _literal(selected[1][1]) == _literal(selected[1][2])
                    ):
                        value = _bool_expr(
                            model,
                            bool_refs,
                            value_expr,
                            opaque=opaque,
                            seen=seen,
                        )
            if value is not None:
                return value if name == "eq" else _not(value)
        return ("atom", ("pred", _value_key(model, text, opaque=opaque)))
    bits = _bit_vector_expr(model, bool_refs, text, opaque=opaque, seen=seen)
    if bits is not None:
        return _or_all(bits)
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


def _restrict(
    expr: tuple[Any, ...],
    atom: tuple[Any, ...],
    value: bool,
) -> tuple[Any, ...]:
    if expr[0] == "const":
        return expr
    if expr[0] == "atom":
        return _const(value) if expr[1] == atom else expr
    if expr[0] == "not":
        return _not(_restrict(expr[1], atom, value))
    if expr[0] == "and":
        return _and(
            _restrict(expr[1], atom, value),
            _restrict(expr[2], atom, value),
        )
    if expr[0] == "or":
        return _or(
            _restrict(expr[1], atom, value),
            _restrict(expr[2], atom, value),
        )
    raise ValueError(expr[0])


def _unsat(
    expr: tuple[Any, ...],
    max_atoms: int = 64,
    max_search_nodes: int = 20_000,
) -> tuple[bool | None, int]:
    atoms = sorted(_atoms(expr), key=repr)
    if len(atoms) > max_atoms:
        return None, len(atoms)

    # Exact Shannon expansion with simplification and memoization.  Unlike the
    # old flat truth-table loop, this closes large but highly structured mux and
    # routing cones without changing the propositional proof domain.
    memo: dict[tuple[Any, ...], bool] = {}
    search_nodes = 0

    class SearchBudgetExceeded(Exception):
        pass

    def frequencies(current: tuple[Any, ...], out: dict[tuple[Any, ...], int]) -> None:
        if current[0] == "atom":
            out[current[1]] = out.get(current[1], 0) + 1
        elif current[0] == "not":
            frequencies(current[1], out)
        elif current[0] in {"and", "or"}:
            frequencies(current[1], out)
            frequencies(current[2], out)

    def visit(current: tuple[Any, ...]) -> bool:
        nonlocal search_nodes
        search_nodes += 1
        if search_nodes > max_search_nodes:
            raise SearchBudgetExceeded
        if current[0] == "const":
            return not bool(current[1])
        cached = memo.get(current)
        if cached is not None:
            return cached
        counts: dict[tuple[Any, ...], int] = {}
        frequencies(current, counts)
        selected = min(counts, key=lambda item: (-counts[item], repr(item)))
        result = visit(_restrict(current, selected, False)) and visit(
            _restrict(current, selected, True)
        )
        memo[current] = result
        return result

    try:
        return visit(expr), len(atoms)
    except SearchBudgetExceeded:
        return None, len(atoms)


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
    # A derived occurrence may refine one physical boundary event with payload
    # tests (for example, a D-channel fire split by source ID).  In that case
    # the physical valid/ready gates are the occurrence base and the explicit
    # grounding below is its filter.  This is distinct from an ungrounded
    # internal milestone, which remains unresolved.
    if not positive and not negative:
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
    for test in grounding.get("value_tests", []):
        if not isinstance(test, dict) or not isinstance(test.get("expr"), dict):
            return None
        try:
            symbolic = expr_to_symbolic(test["expr"])
        except (KeyError, TypeError, ValueError):
            return None
        relation = test.get("relation")
        expected = test.get("value")
        if relation not in {"eq", "neq"} or not isinstance(expected, int):
            return None
        comparison = _bool_expr(
            model,
            bool_refs,
            f"eq({symbolic}, UInt({expected}))",
            opaque=opaque,
        )
        if comparison is None:
            return None
        result = _and(result, comparison if relation == "eq" else _not(comparison))
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
            "event_gate_bridge_statement_ids": sorted(
                getattr(model, "proof_context_statement_ids", set())
            ),
        }
    if unsat is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"Boolean cone exceeds atom limit ({atoms})"}
    return {
        "status": STRUCTURAL_UNKNOWN,
        "reason": "local Boolean reasoning does not prove exclusion",
        "atom_count": atoms,
    }


def prove_unconditional_signal_equality(
    model: Any,
    candidate: dict[str, Any],
    *,
    target: str,
    source: str,
) -> dict[str, Any]:
    """Prove an unconditional one-bit equality from the exact Boolean cones."""

    refs = _bool_refs(model, candidate) | {target, source}
    _propagate_bool_refs(model, target, refs)
    _propagate_bool_refs(model, source, refs)
    left = _bool_expr(model, refs, target)
    right = _bool_expr(model, refs, source)
    if left is None or right is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no exact Boolean cone for both signals"}
    mismatch = _or(_and(left, _not(right)), _and(right, _not(left)))
    unsat, atoms = _unsat(mismatch)
    if unsat is True:
        return {
            "status": STRUCTURALLY_SUPPORTED,
            "proof": f"{target} and {source} have identical exact Boolean values",
            "proof_domain": "exact-unconditional-combinational-equality",
            "atom_count": atoms,
        }
    return {
        "status": STRUCTURAL_UNKNOWN,
        "reason": "unconditional Boolean equality is not established",
        "atom_count": atoms,
    }


def _exact_boundary_or_derived_occurrence_condition(
    model: Any,
    candidate: dict[str, Any],
    occurrence_id: str,
    bool_refs: set[str],
) -> tuple[Any, ...] | None:
    """Use physical event gates for boundaries; candidate grounding for derived events."""

    occurrence = next(
        (item for item in candidate.get("occurrences", []) if item.get("id") == occurrence_id),
        None,
    )
    if occurrence is None:
        return None
    if occurrence.get("kind") != "boundary":
        return _occurrence_condition(model, candidate, occurrence_id, bool_refs)
    physical = occurrence.get("physical_event_ids", [])
    event_fn = getattr(model, "_event_info", None)
    event = event_fn(physical[0]) if len(physical) == 1 and callable(event_fn) else None
    if not isinstance(event, dict):
        return None
    valid = event.get("valid")
    if not isinstance(valid, str) or not valid:
        return None
    # Some physical boundaries are valid-only notification interfaces rather
    # than ready/valid handshakes.  Their exact occurrence gate is simply
    # `valid`; ready is conjoined only when the registry exposes one.
    signals = [valid]
    ready = event.get("ready")
    if isinstance(ready, str) and ready:
        signals.append(ready)
    result = _const(True)
    for signal in signals:
        value = _bool_expr(model, bool_refs, signal)
        if value is None:
            return None
        result = _and(result, value)
    return result


def _resolve_ref_expr(model: Any, expr: str, seen: set[str] | None = None) -> str:
    text = expr.strip()
    seen = set() if seen is None else set(seen)
    if not _REF_RE.fullmatch(text) or _under_state(model, text) or text in seen:
        return text
    nested = _rhs(model, text)
    return text if nested is None else _resolve_ref_expr(model, nested, seen | {text})


def _indexed_signal(signal: str) -> tuple[str, int] | None:
    match = re.fullmatch(r"(.+)\[(\d+)\]", signal.strip())
    return None if match is None else (match.group(1), int(match.group(2)))


def _locked_owner_certificate(
    model: Any,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
) -> dict[str, Any]:
    """Certify history and one-hot ownership for a generic locked arbiter."""

    occurrences = {str(item.get("id")): item for item in candidate.get("occurrences", [])}
    start = occurrences.get(before)
    continuation = occurrences.get(after)
    if not isinstance(start, dict) or not isinstance(continuation, dict):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked owner occurrences are missing"}
    start_ground = start.get("grounding", {})
    continuation_ground = continuation.get("grounding", {})
    start_true = {str(item) for item in start_ground.get("signals_true", [])}
    continuation_true = {str(item) for item in continuation_ground.get("signals_true", [])}
    continuation_false = {str(item) for item in continuation_ground.get("signals_false", [])}
    idle_candidates = start_true & continuation_false
    if len(idle_candidates) != 1:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked owner idle predicate is not unique"}
    idle = next(iter(idle_candidates))

    state_candidates = [
        (signal, indexed)
        for signal in continuation_true
        if (indexed := _indexed_signal(signal)) is not None
        and any(str(root) == indexed[0] for root in getattr(model, "state_roots", set()))
    ]
    if len(state_candidates) != 1:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked owner state bit is not unique"}
    state_signal, (state_root, owner_index) = state_candidates[0]
    winner_candidates = [
        signal
        for signal in start_true
        if (indexed := _indexed_signal(signal)) is not None and indexed[1] == owner_index
    ]
    if len(winner_candidates) != 1:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked owner winner bit is not unique"}
    winner_signal = winner_candidates[0]
    winner_root = _indexed_signal(winner_signal)[0]  # type: ignore[index]

    idle_expr_text = _resolve_ref_expr(model, idle)
    idle_call = _call(idle_expr_text)
    if idle_call is None or idle_call[0] != "eq" or len(idle_call[1]) != 2:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "idle is not an exact zero comparison"}
    counter = next((arg for arg in idle_call[1] if _under_state(model, arg)), None)
    zero = next((_literal(arg) for arg in idle_call[1] if _literal(arg) is not None), None)
    if counter is None or zero != 0 or _scalar_reset_zero(model, counter) is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked beat counter does not reset to idle"}

    counter_update = _call(_resolve_ref_expr(model, _rhs(model, counter) or counter))
    if counter_update is None or counter_update[0] != "mux" or len(counter_update[1]) != 3:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked beat counter update is not one mux"}
    latch, _, decrement = counter_update[1]
    latch_call = _call(_resolve_ref_expr(model, latch))
    if latch_call is None or latch_call[0] != "and" or idle not in latch_call[1]:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "lock acquisition is not idle-and-ready"}
    ready = next(arg for arg in latch_call[1] if arg != idle)
    decrement_call = _call(_resolve_ref_expr(model, decrement))
    if decrement_call is not None and decrement_call[0] == "tail":
        decrement_call = _call(_resolve_ref_expr(model, decrement_call[1][0]))
    if (
        decrement_call is None
        or decrement_call[0] != "sub"
        or len(decrement_call[1]) != 2
        or decrement_call[1][0] != counter
    ):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "non-latching counter path is not a decrement"}

    owner_bits: list[tuple[int, str, str]] = []
    for item in occurrences.values():
        grounding = item.get("grounding", {})
        positives = {str(signal) for signal in grounding.get("signals_true", [])}
        negatives = {str(signal) for signal in grounding.get("signals_false", [])}
        if idle not in negatives:
            continue
        for signal in positives:
            indexed = _indexed_signal(signal)
            if indexed is None or indexed[0] != state_root:
                continue
            index = indexed[1]
            winner = f"{winner_root}[{index}]"
            state_rhs = _call(_resolve_ref_expr(model, _rhs(model, signal) or signal))
            if (
                state_rhs is None
                or state_rhs[0] != "mux"
                or state_rhs[1] != [idle, winner, signal]
            ):
                return {"status": STRUCTURAL_UNKNOWN, "reason": f"owner state bit {signal} is not capture-or-preserve"}
            owner_bits.append((index, signal, winner))
    owner_bits = sorted(set(owner_bits))
    if not owner_bits or owner_index not in {item[0] for item in owner_bits}:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "complete locked owner bit set was not found"}

    refs = _bool_refs(model, candidate)
    for _, _, winner in owner_bits:
        refs.add(winner)
        _propagate_bool_refs(model, winner, refs)
    mutex: list[list[str]] = []
    for left_index, (_, _, left) in enumerate(owner_bits):
        left_expr = _bool_expr(model, refs, left)
        if left_expr is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": f"winner {left} is unresolved"}
        for _, _, right in owner_bits[left_index + 1:]:
            right_expr = _bool_expr(model, refs, right)
            if right_expr is None or _unsat(_and(left_expr, right_expr))[0] is not True:
                return {"status": STRUCTURAL_UNKNOWN, "reason": "winner vector is not one-hot"}
            mutex.append([left, right])

    before_condition = _occurrence_condition(model, candidate, before, refs)
    idle_expr = _bool_expr(model, refs, idle)
    ready_expr = _bool_expr(model, refs, ready)
    winner_expr = _bool_expr(model, refs, winner_signal)
    if None in {before_condition, idle_expr, ready_expr, winner_expr}:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "lock acquisition condition is unresolved"}
    assert before_condition is not None and idle_expr is not None
    assert ready_expr is not None and winner_expr is not None
    creator = _and(_and(idle_expr, ready_expr), winner_expr)
    if _unsat(_and(creator, _not(before_condition)))[0] is not True:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "owner capture does not imply the start occurrence"}

    invariant = _const(True)
    for left_index, (_, left, _) in enumerate(owner_bits):
        left_expr = ("atom", ("nz", ("ref", left)))
        for _, right, _ in owner_bits[left_index + 1:]:
            right_expr = ("atom", ("nz", ("ref", right)))
            invariant = _and(invariant, _or(idle_expr, _not(_and(left_expr, right_expr))))
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof_domain": "exact-locked-owner-provenance",
        "before": before,
        "after": after,
        "idle": idle,
        "counter": counter,
        "state_root": state_root,
        "winner_root": winner_root,
        "owner_index": owner_index,
        "owner_bits": [item[1] for item in owner_bits],
        "winner_mutex": mutex,
        "invariant": invariant,
    }


def prove_locked_owner_provenance(
    model: Any,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
    required_prior: str | None = None,
) -> dict[str, Any]:
    if required_prior is not None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "locked owner required_prior is unsupported"}
    certificate = _locked_owner_certificate(
        model,
        candidate,
        before=before,
        after=after,
    )
    if certificate.get("status") == STRUCTURALLY_SUPPORTED:
        certificate["proof"] = (
            f"{after} requires a preserved locked owner bit whose only non-idle "
            f"capture implies {before}"
        )
    return certificate


def _locked_invariants(model: Any, candidate: dict[str, Any]) -> tuple[tuple[Any, ...], list[dict[str, Any]]]:
    combined = _const(True)
    certificates: list[dict[str, Any]] = []
    occurrences = candidate.get("occurrences", [])
    for after in occurrences:
        negatives = set(after.get("grounding", {}).get("signals_false", []))
        if not negatives:
            continue
        for before in occurrences:
            if not negatives & set(before.get("grounding", {}).get("signals_true", [])):
                continue
            certificate = _locked_owner_certificate(
                model,
                candidate,
                before=str(before.get("id")),
                after=str(after.get("id")),
            )
            if certificate.get("status") != STRUCTURALLY_SUPPORTED:
                continue
            key = (certificate["state_root"], certificate["idle"])
            if any((item["state_root"], item["idle"]) == key for item in certificates):
                continue
            combined = _and(combined, certificate["invariant"])
            certificates.append(certificate)
    return combined, certificates


def prove_same_cycle_occurrence_partition(
    model: Any,
    candidate: dict[str, Any],
    *,
    whole: str,
    parts: list[str],
    relation: str,
) -> dict[str, Any]:
    """Prove one-hot same-cycle occurrence conservation from exact Boolean cones.

    `same_cycle_exactly_one` is `whole <=> OR(parts)` plus pairwise exclusion
    of the parts.  It is intentionally not n-ary parity/XOR semantics.
    """

    if relation != "same_cycle_exactly_one":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported partition relation"}
    if not parts or len(set(parts)) != len(parts) or whole in parts:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "invalid occurrence partition shape"}

    refs = _bool_refs(model, candidate)
    reachable_invariant, lock_certificates = _locked_invariants(model, candidate)

    whole_expr = _exact_boundary_or_derived_occurrence_condition(model, candidate, whole, refs)
    part_exprs = {
        part: _exact_boundary_or_derived_occurrence_condition(model, candidate, part, refs)
        for part in parts
    }
    missing = [part for part, expr in part_exprs.items() if expr is None]
    if whole_expr is None:
        missing.insert(0, whole)
    if missing:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "no exact combinational condition for every partition occurrence",
            "missing_occurrences": missing,
        }

    any_part = _const(False)
    for part in parts:
        any_part = _or(any_part, part_exprs[part])

    obligations: list[dict[str, Any]] = []
    for name, expression in (
        ("whole_without_part", _and(whole_expr, _not(any_part))),
        ("part_without_whole", _and(any_part, _not(whole_expr))),
    ):
        unsat, atoms = _unsat(_and(reachable_invariant, expression))
        obligations.append({"kind": name, "unsat": unsat, "atom_count": atoms})
        if unsat is not True:
            reason = (
                f"Boolean cone exceeds atom limit ({atoms})"
                if unsat is None
                else f"same-cycle partition obligation {name!r} is satisfiable"
            )
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": reason,
                "failed_obligation": name,
                "obligations": obligations,
            }

    mutex_pairs: list[list[str]] = []
    for index, left in enumerate(parts):
        for right in parts[index + 1:]:
            unsat, atoms = _unsat(
                _and(reachable_invariant, _and(part_exprs[left], part_exprs[right]))
            )
            obligations.append({
                "kind": "parts_mutually_exclusive",
                "parts": [left, right],
                "unsat": unsat,
                "atom_count": atoms,
            })
            if unsat is not True:
                reason = (
                    f"Boolean cone exceeds atom limit ({atoms})"
                    if unsat is None
                    else f"partition parts {left!r} and {right!r} can occur together"
                )
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": reason,
                    "failed_obligation": "parts_mutually_exclusive",
                    "failed_parts": [left, right],
                    "obligations": obligations,
                }
            mutex_pairs.append([left, right])

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"{whole} is equivalent to the same-cycle disjunction of its parts, "
            "and every pair of parts has an unsatisfiable conjunction"
        ),
        "proof_domain": "exact-same-cycle-occurrence-partition",
        "whole": whole,
        "parts": list(parts),
        "mutex_pairs": mutex_pairs,
        "obligations": obligations,
        "reachable_lock_certificates": lock_certificates,
    }


def _split_bundle_fields(text: str) -> list[str]:
    body = text.strip()
    if not (body.startswith("{") and body.endswith("}")):
        return []
    body = body[1:-1]
    fields: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(body):
        if char in "{[(":
            depth += 1
        elif char in "}])":
            depth -= 1
        elif char == "," and depth == 0:
            fields.append(body[start:index].strip())
            start = index + 1
    fields.append(body[start:].strip())
    return [field for field in fields if field]


def _bundle_field_type(type_text: str, field_name: str) -> str | None:
    for field in _split_bundle_fields(type_text):
        depth = 0
        for index, char in enumerate(field):
            if char in "{[(":
                depth += 1
            elif char in "}])":
                depth -= 1
            elif char == ":" and depth == 0:
                name = field[:index].strip()
                if name == field_name:
                    return field[index + 1:].strip()
                break
    return None


def _declared_signal_width(model: Any, signal: str) -> int | None:
    """Recover a leaf width from FIRRTL state/wire declarations when available."""

    root_types: dict[str, str] = {
        str(item.get("id")): str(item.get("type"))
        for item in getattr(model, "handoff", {}).get("state", [])
        if item.get("id") and item.get("type")
    }
    for statement in getattr(model, "statements", {}).values():
        match = re.match(r"^wire\s+([^\s:]+)\s*:\s*(.+)$", str(statement.get("text", "")).strip())
        if match:
            root_types[match.group(1)] = match.group(2).strip()

    root = next(
        (
            name for name in sorted(root_types, key=len, reverse=True)
            if signal == name or signal.startswith(name + ".") or signal.startswith(name + "[")
        ),
        None,
    )
    if root is None:
        return None
    current = root_types[root]
    suffix = signal[len(root):]
    for component in [item for item in suffix.split(".") if item]:
        name = component.split("[", 1)[0]
        current = _bundle_field_type(current, name) or ""
        if not current:
            return None
    match = re.match(r"^(?:U|S)Int<(\d+)>", current.strip())
    return int(match.group(1)) if match else None


def _slice_matches_sink_width(
    actual: tuple[Any, ...] | None,
    expected: tuple[Any, ...],
    sink_width: int | None,
) -> bool:
    if actual is None or sink_width is None or len(expected) != 5:
        return False
    if expected[0:2] != ("call", "bits") or expected[2] != actual:
        return False
    high, low = expected[3], expected[4]
    return high == ("lit", sink_width - 1) and low == ("lit", 0)


def _value_equal_under_condition(
    model: Any,
    bool_refs: set[str],
    *,
    actual: str,
    expected: tuple[Any, ...],
    condition: tuple[Any, ...],
    state_roots: set[str],
    sink_width: int | None = None,
    seen: set[str] | None = None,
) -> tuple[bool, dict[str, Any]]:
    """Prove muxed value equality by splitting only reachable Boolean branches."""

    from .semantic import _canonical_expr

    unsat, atoms = _unsat(condition)
    if unsat is True:
        return True, {"kind": "unreachable-branch", "atom_count": atoms}
    if unsat is None:
        return False, {"kind": "atom-limit", "atom_count": atoms}

    text = actual.strip()
    seen = seen or set()
    normal = _canonical_expr(model, text, cut_roots=state_roots)
    if normal == expected:
        return True, {"kind": "symbolic-normal-form-equality"}
    if _slice_matches_sink_width(normal, expected, sink_width):
        return True, {
            "kind": "firrtl-sink-width-truncation",
            "sink_width": sink_width,
        }

    if _REF_RE.fullmatch(text) and text not in seen and not _under_state(model, text):
        nested = _rhs(model, text)
        if nested is not None:
            return _value_equal_under_condition(
                model,
                bool_refs,
                actual=nested,
                expected=expected,
                condition=condition,
                state_roots=state_roots,
                sink_width=_declared_signal_width(model, text) or sink_width,
                seen=seen | {text},
            )

    call = _call(text)
    if call is not None and call[0] == "or" and len(call[1]) == 2:
        left, right = call[1]
        attempts = []
        for value_branch, zero_branch in ((left, right), (right, left)):
            value_proved, value_proof = _value_equal_under_condition(
                model,
                bool_refs,
                actual=value_branch,
                expected=expected,
                condition=condition,
                state_roots=state_roots,
                sink_width=sink_width,
                seen=seen,
            )
            zero_proved, zero_proof = _value_zero_under_condition(
                model,
                bool_refs,
                actual=zero_branch,
                condition=condition,
                state_roots=state_roots,
                seen=seen,
            )
            attempts.append({"value": value_proof, "zero": zero_proof})
            if value_proved and zero_proved:
                return True, {
                    "kind": "one-hot-masked-or-equality",
                    "value_proof": value_proof,
                    "zero_proof": zero_proof,
                }
        return False, {"kind": "masked-or-mismatch", "attempts": attempts}
    if call is None or call[0] != "mux" or len(call[1]) != 3:
        return False, {
            "kind": "value-mismatch",
            "actual_normal_form": repr(normal),
            "expected_normal_form": repr(expected),
            "sink_width": sink_width,
        }

    select, high, low = call[1]
    local_bool_refs = set(bool_refs)
    if _is_bool_expr(model, select, local_bool_refs):
        _propagate_bool_refs(model, select, local_bool_refs)
    select_expr = _bool_expr(model, local_bool_refs, select)
    if select_expr is None:
        return False, {"kind": "unresolved-mux-select", "select": select}

    branch_proofs: list[dict[str, Any]] = []
    for branch_name, branch_value, branch_condition in (
        ("high", high, _and(condition, select_expr)),
        ("low", low, _and(condition, _not(select_expr))),
    ):
        proved, proof = _value_equal_under_condition(
            model,
            local_bool_refs,
            actual=branch_value,
            expected=expected,
            condition=branch_condition,
            state_roots=state_roots,
            sink_width=sink_width,
            seen=seen,
        )
        branch_proofs.append({"branch": branch_name, "proof": proof})
        if not proved:
            return False, {
                "kind": "conditional-mux-equality",
                "select": select,
                "branches": branch_proofs,
            }
    return True, {
        "kind": "conditional-mux-equality",
        "select": select,
        "branches": branch_proofs,
    }


def _value_zero_under_condition(
    model: Any,
    bool_refs: set[str],
    *,
    actual: str,
    condition: tuple[Any, ...],
    state_roots: set[str],
    seen: set[str] | None = None,
) -> tuple[bool, dict[str, Any]]:
    unsat, atoms = _unsat(condition)
    if unsat is True:
        return True, {"kind": "unreachable-zero-branch", "atom_count": atoms}
    text = actual.strip()
    seen = set() if seen is None else set(seen)
    literal = _literal(text)
    if literal == 0:
        return True, {"kind": "literal-zero"}
    if _REF_RE.fullmatch(text) and text not in seen and not _under_state(model, text):
        nested = _rhs(model, text)
        if nested is not None:
            return _value_zero_under_condition(
                model,
                bool_refs,
                actual=nested,
                condition=condition,
                state_roots=state_roots,
                seen=seen | {text},
            )
    call = _call(text)
    if call is None:
        return False, {"kind": "nonzero-value", "actual": text}
    if call[0] in {"or", "cat"} and len(call[1]) == 2:
        proofs = [
            _value_zero_under_condition(
                model,
                bool_refs,
                actual=branch,
                condition=condition,
                state_roots=state_roots,
                seen=seen,
            )
            for branch in call[1]
        ]
        return all(item[0] for item in proofs), {
            "kind": f"{call[0]}-of-zero-values",
            "branches": [item[1] for item in proofs],
        }
    if call[0] == "bits" and len(call[1]) == 3:
        proved, proof = _value_zero_under_condition(
            model,
            bool_refs,
            actual=call[1][0],
            condition=condition,
            state_roots=state_roots,
            seen=seen,
        )
        return proved, {"kind": "slice-of-zero-value", "source": proof}
    if call[0] != "mux" or len(call[1]) != 3:
        return False, {"kind": "nonzero-expression", "actual": text}
    select, high, low = call[1]
    local_refs = set(bool_refs)
    _propagate_bool_refs(model, select, local_refs)
    select_expr = _bool_expr(model, local_refs, select)
    if select_expr is None:
        return False, {"kind": "unresolved-zero-mux-select", "select": select}
    branch_proofs = []
    for name, value, branch_condition in (
        ("high", high, _and(condition, select_expr)),
        ("low", low, _and(condition, _not(select_expr))),
    ):
        proved, proof = _value_zero_under_condition(
            model,
            local_refs,
            actual=value,
            condition=branch_condition,
            state_roots=state_roots,
            seen=seen,
        )
        branch_proofs.append({"branch": name, "proof": proof})
        if not proved:
            return False, {"kind": "conditional-mux-zero", "branches": branch_proofs}
    return True, {"kind": "conditional-mux-zero", "branches": branch_proofs}


def prove_conditional_signal_equality(
    model: Any,
    candidate: dict[str, Any],
    *,
    target: str,
    source: str,
    on: str,
) -> dict[str, Any]:
    """Prove a payload equality under one exact occurrence condition.

    FIRRTL last-connect semantics are reconstructed from every local driver of
    `target`. Positive `when` guards become priority selections in statement
    order. The proof checks every driver selection reachable while `on` holds;
    no mux, arbiter, channel, or payload field name is special-cased.
    """

    from .semantic import _canonical_expr

    refs = _bool_refs(model, candidate)
    on_expr = _exact_boundary_or_derived_occurrence_condition(model, candidate, on, refs)
    unconditional_strengthening = on_expr is None
    if on_expr is None:
        # If the occurrence guard is not representable as an exact Boolean
        # condition (for example a state-only derived milestone), proving the
        # equality for every combinational valuation is a sound strengthening.
        on_expr = _const(True)
    reachable_invariant, lock_certificates = _locked_invariants(model, candidate)
    on_expr = _and(reachable_invariant, on_expr)

    drivers: list[dict[str, Any]] = []
    for statement in sorted(model.statements.values(), key=lambda item: int(item.get("id", -1))):
        if target not in {str(item) for item in statement.get("drives", [])}:
            continue
        if statement.get("kind") == "infer_mport":
            # FIRRTL memory-port inference declares the selected storage/index;
            # the following connect is the actual payload writer.
            continue
        parsed = _statement_rhs(statement)
        if parsed is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"unparsed driver for {target!r}",
                "statement_id": int(statement.get("id", -1)),
            }
        lhs, rhs = parsed
        if target == lhs:
            projected_rhs = rhs
        elif target.startswith(lhs + ".") and _REF_RE.fullmatch(rhs):
            projected_rhs = rhs + target[len(lhs):]
        else:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"could not project aggregate driver for {target!r}",
                "statement_id": int(statement.get("id", -1)),
            }
        activation_info = _writer_activation(model, target, statement, refs)
        if activation_info is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"driver activation is not exact for {target!r}",
                "statement_id": int(statement.get("id", -1)),
            }
        activation, activation_certificate = activation_info
        drivers.append({
            "statement_id": int(statement.get("id", -1)),
            "rhs": projected_rhs,
            "activation": activation,
            "activation_certificate": activation_certificate,
        })

    if not drivers:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"no drivers for {target!r}"}

    state_roots = {str(root) for root in getattr(model, "state_roots", set())}
    source_expr = _canonical_expr(model, source, cut_roots=state_roots)
    selected: list[dict[str, Any]] = []
    any_selected = _const(False)
    for index, driver in enumerate(drivers):
        effective = driver["activation"]
        for later in drivers[index + 1:]:
            effective = _and(effective, _not(later["activation"]))
        any_selected = _or(any_selected, effective)
        reachable, atoms = _unsat(_and(on_expr, effective))
        if reachable is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"conditional equality Boolean cone exceeds atom limit ({atoms})",
            }
        if reachable is True:
            continue
        rhs_expr = _canonical_expr(model, driver["rhs"], cut_roots=state_roots)
        exact_value = driver["rhs"] == source or (
            rhs_expr is not None and rhs_expr == source_expr
        )
        branch_certificate: dict[str, Any] | None = None
        if not exact_value and source_expr is not None:
            exact_value, branch_certificate = _value_equal_under_condition(
                model,
                refs,
                actual=driver["rhs"],
                expected=source_expr,
                condition=_and(on_expr, effective),
                state_roots=state_roots,
            )
        if not exact_value:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"reachable driver of {target!r} is not equal to {source!r} on {on!r}",
                "statement_id": driver["statement_id"],
                "driver_rhs": driver["rhs"],
                "branch_certificate": branch_certificate,
            }
        selected.append({
            "statement_id": driver["statement_id"],
            "rhs": driver["rhs"],
            "activation": driver["activation_certificate"],
            "atom_count": atoms,
            "value_proof": branch_certificate or {"kind": "symbolic-normal-form-equality"},
        })

    uncovered, atoms = _unsat(_and(on_expr, _not(any_selected)))
    if uncovered is not True:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": f"{target!r} has no exact active driver for every {on!r} occurrence",
            "atom_count": atoms,
        }
    if not selected:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": f"no reachable driver of {target!r} while {on!r} holds",
        }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": f"every last-connect driver of {target} reachable on {on} equals {source}",
        "proof_domain": "exact-conditional-symbolic-driver-equality",
        "on": on,
        "target": target,
        "source": source,
        "unconditional_strengthening": unconditional_strengthening,
        "selected_drivers": selected,
        "all_driver_statement_ids": [driver["statement_id"] for driver in drivers],
        "reachable_lock_certificates": lock_certificates,
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
    """Recover an exact branch activation for one scalar or aggregate writer.

    Control dependency edges identify the enclosing branch statements.  A
    ``when`` contributes its condition and an ``else`` contributes the exact
    negation of the condition recorded on that block.  Ambiguous/mixed branch
    polarity remains fail-closed.
    """

    statement_id = int(statement.get("id", -1))
    handoff = getattr(model, "handoff", None)
    if not isinstance(handoff, dict):
        return None
    edges = [
        edge
        for edge in handoff.get("dependency_edges", [])
        if edge.get("kind") == "control"
        and (
            edge.get("dst") == storage
            or str(edge.get("dst", "")).startswith(storage + ".")
            or str(edge.get("dst", "")).startswith(storage + "[")
        )
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
    if any(block is None or block.get("kind") not in {"when", "else"} for block in blocks):
        return None

    activation = _const(True)
    polarities: dict[str, str] = {}
    for control in controls:
        related_kinds = {
            str(block.get("kind"))
            for block in blocks
            if block is not None
            and control in {str(item) for item in block.get("control_reads", [])}
        }
        if related_kinds == {"when"}:
            polarity = "positive"
        elif related_kinds == {"else"}:
            polarity = "negative"
        else:
            return None
        local_bool_refs = set(bool_refs)
        if _is_bool_expr(model, control, local_bool_refs):
            _propagate_bool_refs(model, control, local_bool_refs)
        expr = _bool_expr(model, local_bool_refs, control)
        if expr is None:
            return None
        activation = _and(activation, expr if polarity == "positive" else _not(expr))
        polarities[control] = polarity
    return activation, {
        "kind": "exact-branch-conjunction",
        "control_signals": controls,
        "control_statement_ids": sorted(block_ids),
        "control_polarities": polarities,
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
