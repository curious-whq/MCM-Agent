from __future__ import annotations

from typing import Any

from .formal_patterns import _declared_signal_width, _under_state
from .priority_select_prover import (
    COUNTEREXAMPLE,
    STRUCTURALLY_SUPPORTED,
    STRUCTURAL_UNKNOWN,
    _ConcreteFIRRTLEvaluator,
    _is_grounded_bool_signal,
)
from .semantic import HandoffControlModel


def _eval_expr(
    expr: dict[str, Any],
    env: dict[str, tuple[int, int]],
    width: int,
) -> int | None:
    op = expr.get("op")
    mask = (1 << width) - 1
    if op == "signal":
        value = env.get(str(expr.get("name", "")))
        return None if value is None else value[0] & mask
    if op == "const":
        return int(expr.get("value", 0)) & mask
    if op == "modular_increment":
        value = _eval_expr(expr["value"], env, width)
        modulus = int(expr.get("modulus", 0))
        if value is None or modulus < 2 or modulus > (1 << width):
            return None
        return (value + 1) % modulus
    if op == "slice":
        value = _eval_expr(expr["value"], env, width)
        high, low = int(expr.get("hi", -1)), int(expr.get("lo", -1))
        if value is None or low < 0 or high < low:
            return None
        return (value >> low) & ((1 << (high - low + 1)) - 1)
    if op == "bit" and isinstance(expr.get("index"), int):
        value = _eval_expr(expr["value"], env, width)
        return None if value is None else (value >> int(expr["index"])) & 1
    if op == "not":
        value = _eval_expr(expr["value"], env, width)
        return None if value is None else int(value == 0)
    if op in {"and", "or"}:
        values = [_eval_expr(item, env, width) for item in expr.get("args", [])]
        if any(value is None for value in values):
            return None
        return int(all(values)) if op == "and" else int(any(values))
    return None


def _signals(expr: dict[str, Any]) -> set[str]:
    op = expr.get("op")
    if op == "signal":
        return {str(expr.get("name", ""))}
    if op in {"const", "index_var"}:
        return set()
    if op in {"slice", "shr", "not", "modular_increment"}:
        return _signals(expr["value"])
    if op == "bit":
        result = _signals(expr["value"])
        if isinstance(expr.get("index"), dict):
            result |= _signals(expr["index"])
        return result
    if op in {"and", "or"}:
        return set().union(*(_signals(item) for item in expr.get("args", [])))
    return set()


def prove_register_transition(
    model: HandoffControlModel,
    candidate_model: dict[str, Any],
    *,
    register: str,
    width: int,
    updates: list[dict[str, Any]],
    priority: str,
    default: dict[str, Any],
) -> dict[str, Any]:
    """Prove one exact next-state relation by exhaustive finite equivalence."""

    del candidate_model
    if priority != "first_match":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported update priority"}
    if width < 1 or width > 12:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "exact register transition enumeration supports widths 1..12",
        }
    if register not in model.state_roots or _declared_signal_width(model, register) != width:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "declared transition register/width does not match local state",
        }

    guard_signals = set().union(*(_signals(update["guard"]) for update in updates))
    value_signals = set().union(
        *(_signals(update["next"]) for update in updates),
        _signals(default),
    )
    external_guards = guard_signals - {register}
    external_values = value_signals - {register}
    if external_guards & external_values:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "one transition input is used as both a Boolean guard and data value",
        }

    evaluator = _ConcreteFIRRTLEvaluator(model)
    for signal in sorted(external_guards):
        if not _is_grounded_bool_signal(model, signal):
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"transition guard {signal!r} is not grounded as a Bool",
            }
        if evaluator.writers(signal) is not None and not _under_state(model, signal):
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"transition guard {signal!r} is not a frontier/state value",
            }
    for signal in sorted(external_values):
        if evaluator.writers(signal) is not None and not _under_state(model, signal):
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"transition value {signal!r} is not a frontier/state value",
            }

    inputs = [(register, width)]
    inputs.extend((signal, 1) for signal in sorted(external_guards))
    inputs.extend((signal, width) for signal in sorted(external_values))
    total_bits = sum(input_width for _, input_width in inputs)
    if total_bits > 20:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "register transition exceeds the current 2^20 exact enumeration limit",
        }

    checked = 0
    writer_ids: set[int] = set()
    state_mask = (1 << width) - 1
    for valuation in range(1 << total_bits):
        env: dict[str, tuple[int, int]] = {}
        offset = 0
        for signal, input_width in inputs:
            value = (valuation >> offset) & ((1 << input_width) - 1)
            offset += input_width
            env[signal] = (value, input_width)

        expected: int | None = None
        selected_update: int | None = None
        for update_index, update in enumerate(updates):
            guard = _eval_expr(update["guard"], env, 1)
            if guard is None:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": "could not evaluate a declared transition guard",
                }
            if guard:
                expected = _eval_expr(update["next"], env, width)
                selected_update = update_index
                break
        if expected is None:
            expected = _eval_expr(default, env, width)
        if expected is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "could not evaluate a declared transition next expression",
            }

        actual = evaluator.next_state(register, env)
        if actual is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "could not evaluate the complete register writer/control cone",
                "inputs": {signal: env[signal][0] for signal, _ in inputs},
            }
        writer_ids.update(actual[1])
        actual_value = actual[0] & state_mask
        if actual_value != expected:
            return {
                "status": COUNTEREXAMPLE,
                "reason": "RTL next state differs from the declared guarded register transition",
                "counterexample": {
                    "inputs": {signal: env[signal][0] for signal, _ in inputs},
                    "selected_update": selected_update,
                    "actual_next": actual_value,
                    "expected_next": expected,
                },
            }
        checked += 1

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"exhaustive finite equivalence proves the complete {width}-bit "
            f"next-state writer priority for {register}"
        ),
        "proof_domain": "exact-guarded-register-transition",
        "register": register,
        "width": width,
        "priority": priority,
        "updates": updates,
        "default": default,
        "checked_rows": checked,
        "writer_statement_ids": sorted(writer_ids),
        "input_widths": {signal: input_width for signal, input_width in inputs},
    }
