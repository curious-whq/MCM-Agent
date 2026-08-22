from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Any

from .semantic import HandoffControlModel, _call, _literal
from .formal_patterns import (
    _declared_signal_width,
    _projected_driver_rhs,
    _under_state,
    declared_signal_type_from_handoff,
)


STRUCTURALLY_SUPPORTED = "STRUCTURALLY_SUPPORTED"
STRUCTURAL_UNKNOWN = "STRUCTURAL_UNKNOWN"
COUNTEREXAMPLE = "COUNTEREXAMPLE"

_REF_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_$]*(?:(?:\.[A-Za-z_][A-Za-z0-9_$]*)|(?:\[[^\[\]]+\]))*$"
)


@dataclass(frozen=True)
class _Writer:
    statement_id: int
    rhs: str
    controls: tuple[tuple[str, bool], ...]
    kind: str


def _matches_target(target: str, drive: str) -> bool:
    return (
        target == drive
        or target.startswith(drive + ".")
        or target.startswith(drive + "[")
    )


class _ConcreteFIRRTLEvaluator:
    """Exact evaluator for the small combinational FIRRTL selector fragment."""

    def __init__(self, model: HandoffControlModel):
        self.model = model
        self._writer_cache: dict[str, tuple[_Writer, ...] | None] = {}

    def _controls(self, target: str, statement: dict[str, Any]) -> tuple[tuple[str, bool], ...] | None:
        if statement.get("kind") == "node":
            return ()
        statement_id = int(statement.get("id", -1))
        edges = [
            edge
            for edge in self.model.handoff.get("dependency_edges", [])
            if edge.get("kind") == "control"
            and _matches_target(target, str(edge.get("dst", "")))
            and statement_id in {int(item) for item in edge.get("statement_ids", [])}
        ]
        controls = sorted({str(edge.get("src")) for edge in edges if edge.get("src")})
        declared = {str(item) for item in statement.get("control_reads", [])}
        if declared and not controls:
            return None
        if not controls:
            return ()
        block_ids = {
            int(block_id)
            for edge in edges
            for block_id in edge.get("statement_ids", [])
            if int(block_id) != statement_id
        }
        blocks = [self.model.statements.get(block_id) for block_id in sorted(block_ids)]
        if any(block is None or block.get("kind") not in {"when", "else"} for block in blocks):
            return None
        result: list[tuple[str, bool]] = []
        for control in controls:
            kinds = {
                str(block.get("kind"))
                for block in blocks
                if block is not None
                and control in {str(item) for item in block.get("control_reads", [])}
            }
            if kinds == {"when"}:
                result.append((control, True))
            elif kinds == {"else"}:
                result.append((control, False))
            else:
                return None
        return tuple(result)

    def writers(self, target: str) -> tuple[_Writer, ...] | None:
        if target in self._writer_cache:
            return self._writer_cache[target]
        writers: list[_Writer] = []
        for statement in sorted(
            self.model.statements.values(), key=lambda item: int(item.get("id", -1))
        ):
            if statement.get("kind") not in {"connect", "node"}:
                continue
            drives = {str(item) for item in statement.get("drives", [])}
            if not any(_matches_target(target, drive) for drive in drives):
                continue
            rhs = _projected_driver_rhs(self.model, statement, target)
            controls = self._controls(target, statement)
            if rhs is None or controls is None:
                self._writer_cache[target] = None
                return None
            writers.append(
                _Writer(
                    statement_id=int(statement.get("id", -1)),
                    rhs=rhs,
                    controls=controls,
                    kind=(
                        "exact-unconditional-ssa-node"
                        if statement.get("kind") == "node"
                        else "exact-priority-connect"
                    ),
                )
            )
        result = tuple(writers) if writers else None
        self._writer_cache[target] = result
        return result

    @staticmethod
    def _literal_width(expr: str, value: int) -> int:
        match = re.match(r"^(?:U|S)Int<(\d+)>", expr.strip())
        return int(match.group(1)) if match else max(1, int(value).bit_length())

    def _active(
        self,
        writer: _Writer,
        env: dict[str, tuple[int, int]],
        memo: dict[str, tuple[int, int]],
        seen: set[str],
    ) -> bool | None:
        for control, positive in writer.controls:
            value = self.eval(control, env, memo=memo, seen=seen)
            if value is None:
                return None
            truth = value[0] != 0
            if truth != positive:
                return False
        return True

    def eval(
        self,
        expr: str,
        env: dict[str, tuple[int, int]],
        *,
        memo: dict[str, tuple[int, int]] | None = None,
        seen: set[str] | None = None,
    ) -> tuple[int, int] | None:
        text = expr.strip()
        memo = {} if memo is None else memo
        seen = set() if seen is None else set(seen)
        literal = _literal(text)
        if literal is not None:
            return int(literal), self._literal_width(text, int(literal))
        compact_literal = re.fullmatch(r"h([0-9a-fA-F]+)", text)
        if compact_literal is not None:
            value = int(compact_literal.group(1), 16)
            return value, max(1, 4 * len(compact_literal.group(1)))
        if _REF_RE.fullmatch(text):
            if text in env:
                return env[text]
            if text in memo:
                return memo[text]
            if text in seen or _under_state(self.model, text):
                return None
            writers = self.writers(text)
            if writers is None:
                return None
            selected: _Writer | None = None
            for writer in writers:
                active = self._active(writer, env, memo, seen | {text})
                if active is None:
                    return None
                if active:
                    selected = writer
            if selected is None:
                return None
            value = self.eval(selected.rhs, env, memo=memo, seen=seen | {text})
            if value is not None:
                memo[text] = value
            return value
        call = _call(text)
        if call is None:
            return None
        name, args = call
        values = [self.eval(arg, env, memo=memo, seen=seen) for arg in args]
        if any(value is None for value in values):
            return None
        resolved = [value for value in values if value is not None]
        if name == "bits" and len(resolved) == 3:
            value, _ = resolved[0]
            high, low = resolved[1][0], resolved[2][0]
            if low < 0 or high < low:
                return None
            width = high - low + 1
            return (value >> low) & ((1 << width) - 1), width
        if name == "cat" and len(resolved) == 2:
            high, low = resolved
            return (high[0] << low[1]) | low[0], high[1] + low[1]
        if name in {"and", "or", "xor"} and len(resolved) == 2:
            width = max(resolved[0][1], resolved[1][1])
            left, right = resolved[0][0], resolved[1][0]
            value = left & right if name == "and" else left | right if name == "or" else left ^ right
            return value & ((1 << width) - 1), width
        if name in {"add", "sub"} and len(resolved) == 2:
            width = max(resolved[0][1], resolved[1][1]) + 1
            left, right = resolved[0][0], resolved[1][0]
            value = left + right if name == "add" else left - right
            return value & ((1 << width) - 1), width
        if name == "tail" and len(resolved) == 2:
            amount = resolved[1][0]
            if amount < 0 or amount >= resolved[0][1]:
                return None
            width = resolved[0][1] - amount
            return resolved[0][0] & ((1 << width) - 1), width
        if name == "not" and len(resolved) == 1:
            width = resolved[0][1]
            return (~resolved[0][0]) & ((1 << width) - 1), width
        if name == "mux" and len(resolved) == 3:
            chosen = resolved[1] if resolved[0][0] != 0 else resolved[2]
            width = max(resolved[1][1], resolved[2][1])
            return chosen[0] & ((1 << width) - 1), width
        if name in {"eq", "neq", "lt", "leq", "gt", "geq"} and len(resolved) == 2:
            left, right = resolved[0][0], resolved[1][0]
            relation = {
                "eq": left == right,
                "neq": left != right,
                "lt": left < right,
                "leq": left <= right,
                "gt": left > right,
                "geq": left >= right,
            }[name]
            return int(relation), 1
        if name in {"asUInt", "asSInt", "pad"} and resolved:
            if name == "pad" and len(resolved) == 2:
                return resolved[0][0], max(resolved[0][1], resolved[1][0])
            return resolved[0]
        return None

    def next_state(
        self,
        state: str,
        env: dict[str, tuple[int, int]],
    ) -> tuple[int, tuple[int, ...]] | None:
        writers = self.writers(state)
        if writers is None:
            return None
        memo: dict[str, tuple[int, int]] = {}
        selected_value: tuple[int, int] | None = None
        selected_ids: list[int] = []
        for writer in writers:
            active = self._active(writer, env, memo, {state})
            if active is None:
                return None
            if not active:
                continue
            value = self.eval(writer.rhs, env, memo=memo, seen={state})
            if value is None:
                return None
            selected_value = value
            selected_ids.append(writer.statement_id)
        if selected_value is None:
            held = env.get(state)
            if held is None:
                return None
            return held[0], ()
        return selected_value[0], tuple(selected_ids)

    def eval_projected(
        self,
        expr: str,
        high: int,
        low: int,
        env: dict[str, tuple[int, int]],
        *,
        seen: set[str] | None = None,
    ) -> tuple[int, int] | None:
        """Evaluate a constant bit projection without forcing irrelevant cone bits."""

        if low < 0 or high < low:
            return None
        text = expr.strip()
        seen = set() if seen is None else set(seen)
        if _REF_RE.fullmatch(text) and text not in env and text not in seen:
            writers = self.writers(text)
            if writers is not None and len(writers) == 1 and not writers[0].controls:
                return self.eval_projected(
                    writers[0].rhs, high, low, env, seen=seen | {text}
                )
        call = _call(text)
        if call is not None and call[0] == "cat" and len(call[1]) == 2:
            high_expr, low_expr = call[1]
            low_value = self.eval(low_expr, env)
            if low_value is None:
                return None
            low_width = low_value[1]
            if high < low_width:
                width = high - low + 1
                return (low_value[0] >> low) & ((1 << width) - 1), width
            if low >= low_width:
                return self.eval_projected(
                    high_expr,
                    high - low_width,
                    low - low_width,
                    env,
                    seen=seen,
                )
        value = self.eval(text, env)
        if value is None or high >= value[1]:
            return None
        width = high - low + 1
        return (value[0] >> low) & ((1 << width) - 1), width

    def next_state_projected(
        self,
        state: str,
        high: int,
        low: int,
        env: dict[str, tuple[int, int]],
    ) -> tuple[int, tuple[int, ...]] | None:
        writers = self.writers(state)
        if writers is None:
            return None
        memo: dict[str, tuple[int, int]] = {}
        selected: tuple[int, int] | None = None
        selected_ids: list[int] = []
        for writer in writers:
            active = self._active(writer, env, memo, {state})
            if active is None:
                return None
            if not active:
                continue
            selected = self.eval_projected(writer.rhs, high, low, env, seen={state})
            if selected is None:
                return None
            selected_ids.append(writer.statement_id)
        if selected is None:
            held = env.get(state)
            if held is None:
                return None
            width = high - low + 1
            return (held[0] >> low) & ((1 << width) - 1), ()
        return selected[0], tuple(selected_ids)


def _state_alias(
    evaluator: _ConcreteFIRRTLEvaluator,
    signal: str,
) -> tuple[str, list[dict[str, Any]]] | None:
    current = signal
    seen: set[str] = set()
    aliases: list[dict[str, Any]] = []
    while current not in seen:
        seen.add(current)
        if current in evaluator.model.state_roots:
            return current, aliases
        writers = evaluator.writers(current)
        if writers is None or len(writers) != 1 or writers[0].controls:
            return None
        writer = writers[0]
        if not _REF_RE.fullmatch(writer.rhs):
            return None
        aliases.append(
            {
                "target": current,
                "source": writer.rhs,
                "statement_id": writer.statement_id,
            }
        )
        current = writer.rhs
    return None


def _result_index_target(
    evaluator: _ConcreteFIRRTLEvaluator,
    result_index: Any,
) -> tuple[str, list[dict[str, Any]], tuple[int, int] | None] | None:
    projection: tuple[int, int] | None = None
    signal: str | None = None
    if isinstance(result_index, str):
        signal = result_index
    elif isinstance(result_index, dict) and result_index.get("op") == "signal":
        signal = str(result_index.get("name", ""))
    elif isinstance(result_index, dict) and result_index.get("op") in {"slice", "bit"}:
        value = result_index.get("value")
        if not isinstance(value, dict) or value.get("op") != "signal":
            return None
        signal = str(value.get("name", ""))
        if result_index["op"] == "slice":
            projection = (int(result_index.get("hi", -1)), int(result_index.get("lo", -1)))
        else:
            bit_index = result_index.get("index")
            if not isinstance(bit_index, int):
                return None
            projection = (bit_index, bit_index)
    if not signal:
        return None
    alias = _state_alias(evaluator, signal)
    if alias is None:
        return None
    state, chain = alias
    return state, chain, projection


def _is_unreset_register(model: HandoffControlModel, state: str) -> bool:
    declarations = [
        statement
        for statement in model.statements.values()
        if state in {str(item) for item in statement.get("drives", [])}
        and statement.get("kind") in {"reg", "regreset"}
    ]
    return len(declarations) == 1 and declarations[0].get("kind") == "reg"


def _selected_index(
    candidates: list[int],
    kind: str,
    pivot: int | None,
    pivot_position: str = "last",
) -> int:
    if kind == "linear_min":
        return min(candidates)
    if kind == "linear_max":
        return max(candidates)
    if kind == "cyclic_predecessor":
        prior = [
            index
            for index in candidates
            if index < int(pivot)
            or (pivot_position == "first" and index == int(pivot))
        ]
        return max(prior) if prior else max(candidates)
    if kind == "cyclic_successor":
        following = [
            index
            for index in candidates
            if index > int(pivot)
            or (pivot_position == "first" and index == int(pivot))
        ]
        return min(following) if following else min(candidates)
    raise ValueError(kind)


def _candidate_leaf_specs(
    expr: dict[str, Any],
    index_name: str,
    count: int,
) -> dict[str, str] | None:
    """Return independent candidate sources as packed-vector or indexed-array roots."""

    specs: dict[str, str] = {}

    def add(name: str, kind: str) -> bool:
        previous = specs.get(name)
        if previous is not None and previous != kind:
            return False
        specs[name] = kind
        return True

    def visit(node: Any) -> bool:
        if not isinstance(node, dict):
            return False
        op = node.get("op")
        if op == "bit":
            value = node.get("value")
            return (
                isinstance(value, dict)
                and value.get("op") == "signal"
                and node.get("index") == {"op": "index_var", "name": index_name}
                and add(str(value.get("name", "")), "packed")
            )
        if op == "lookup":
            value = node.get("value")
            return (
                isinstance(value, dict)
                and value.get("op") == "signal"
                and node.get("index") == {"op": "index_var", "name": index_name}
                and add(str(value.get("name", "")), "array")
            )
        if op == "not":
            return visit(node.get("value"))
        if op in {"and", "or"}:
            args = node.get("args")
            return isinstance(args, list) and len(args) >= 2 and all(visit(item) for item in args)
        if op == "indexed_cases":
            if (
                node.get("index") != {"op": "index_var", "name": index_name}
                or not isinstance(node.get("values"), list)
                or len(node["values"]) != count
            ):
                return False

            def visit_scalar(item: Any) -> bool:
                if not isinstance(item, dict):
                    return False
                scalar_op = item.get("op")
                if scalar_op == "signal":
                    return add(str(item.get("name", "")), "scalar")
                if scalar_op == "not":
                    return visit_scalar(item.get("value"))
                if scalar_op in {"and", "or"}:
                    args = item.get("args")
                    return (
                        isinstance(args, list)
                        and len(args) >= 2
                        and all(visit_scalar(arg) for arg in args)
                    )
                if scalar_op == "const":
                    return item.get("value") in {0, 1}
                return False

            return all(visit_scalar(item) for item in node["values"])
        return False

    return specs if visit(expr) and specs else None


def _eval_candidate_expr(
    expr: dict[str, Any],
    index_value: int,
    env: dict[str, tuple[int, int]],
) -> int | None:
    op = expr.get("op")
    if op == "bit":
        value = expr.get("value")
        if not isinstance(value, dict) or value.get("op") != "signal":
            return None
        packed = env.get(str(value.get("name", "")))
        return None if packed is None else (packed[0] >> index_value) & 1
    if op == "lookup":
        value = expr.get("value")
        if not isinstance(value, dict) or value.get("op") != "signal":
            return None
        item = env.get(f"{value.get('name')}[{index_value}]")
        return None if item is None else int(item[0] != 0)
    if op == "not":
        value = _eval_candidate_expr(expr["value"], index_value, env)
        return None if value is None else int(not value)
    if op in {"and", "or"}:
        values = [
            _eval_candidate_expr(item, index_value, env)
            for item in expr.get("args", [])
        ]
        if any(value is None for value in values):
            return None
        return int(all(values)) if op == "and" else int(any(values))
    if op == "indexed_cases":
        values = expr.get("values", [])
        if not 0 <= index_value < len(values):
            return None

        def eval_scalar(node: dict[str, Any]) -> int | None:
            scalar_op = node.get("op")
            if scalar_op == "signal":
                value = env.get(str(node.get("name", "")))
                return None if value is None else int(value[0] != 0)
            if scalar_op == "const":
                return int(node.get("value", 0) != 0)
            if scalar_op == "not":
                value = eval_scalar(node["value"])
                return None if value is None else int(not value)
            if scalar_op in {"and", "or"}:
                items = [eval_scalar(item) for item in node.get("args", [])]
                if any(item is None for item in items):
                    return None
                return int(all(items)) if scalar_op == "and" else int(any(items))
            return None

        return eval_scalar(values[index_value])
    return None


def _array_shape(type_text: str | None) -> tuple[int, int] | None:
    if not type_text:
        return None
    match = re.fullmatch(r"UInt<(\d+)>\s*\[(\d+)\]", type_text.strip())
    return (int(match.group(1)), int(match.group(2))) if match else None


def _is_grounded_bool_signal(
    model: HandoffControlModel,
    signal: str,
    *,
    seen: set[str] | None = None,
) -> bool:
    """Recover Bool width through exact Boolean-preserving lowered nodes."""

    if _declared_signal_width(model, signal) == 1:
        return True
    seen = set() if seen is None else set(seen)
    if signal in seen:
        return False
    if any(
        edge.get("kind") == "control" and str(edge.get("src")) == signal
        for edge in model.handoff.get("dependency_edges", [])
    ):
        return True
    for edge in model.handoff.get("dependency_edges", []):
        if edge.get("kind") != "data" or str(edge.get("src")) != signal:
            continue
        destination = str(edge.get("dst", ""))
        statement_ids = {int(item) for item in edge.get("statement_ids", [])}
        statements = [
            model.statements.get(statement_id) for statement_id in statement_ids
        ]
        if not statements or any(statement is None for statement in statements):
            continue
        boolean_preserving = True
        for statement in statements:
            text = str(statement.get("text", ""))
            node = re.match(
                r"^node\s+[^=]+\s*=\s*(and|or|xor|not)\(",
                text,
            )
            if node is None:
                boolean_preserving = False
                break
        if boolean_preserving and _is_grounded_bool_signal(
            model, destination, seen=seen | {signal}
        ):
            return True
    return False


def prove_indexed_priority_select(
    model: HandoffControlModel,
    candidate_model: dict[str, Any],
    *,
    index: dict[str, Any],
    candidate: dict[str, Any],
    priority: dict[str, Any],
    result: dict[str, Any],
    latency_cycles: int,
    initialization: dict[str, Any],
) -> dict[str, Any]:
    """Prove a registered finite priority selector by exhaustive input equivalence."""

    del candidate_model  # The formal AST and grounded handoff fully determine this proof.
    count = int(index.get("count", 0))
    if count < 1 or count > 12:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "exact indexed priority enumeration currently supports 1..12 candidates",
        }
    if latency_cycles != 1:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "current deterministic indexed priority prover supports exactly one registered cycle",
        }
    if initialization != {"kind": "implicit_unconstrained"}:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "current indexed priority prover requires implicit_unconstrained initialization",
        }
    index_name = str(index.get("name", ""))
    candidate_sources = _candidate_leaf_specs(candidate, index_name, count)
    if candidate_sources is None:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "candidate is not a supported indexed Boolean expression",
        }
    kind = str(priority.get("kind", ""))
    pivot_position = str(priority.get("pivot_position", "last"))
    pivot_signal: str | None = None
    if kind.startswith("cyclic_"):
        pivot = priority.get("pivot")
        if not isinstance(pivot, dict) or pivot.get("op") != "signal":
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "current cyclic priority prover requires a signal pivot",
            }
        pivot_signal = str(pivot["name"])

    evaluator = _ConcreteFIRRTLEvaluator(model)
    for source, source_kind in candidate_sources.items():
        if evaluator.writers(source) is not None and not _under_state(model, source):
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": (
                    f"candidate source {source!r} must be a local state value or "
                    "parent-visible input/frontier signal"
                ),
            }
        if source_kind == "packed":
            if _declared_signal_width(model, source) != count:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": (
                        f"packed candidate source {source!r} width is unknown or "
                        "differs from index.count"
                    ),
                }
        elif source_kind == "array":
            shape = _array_shape(declared_signal_type_from_handoff(model.handoff, source))
            if shape != (1, count):
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": (
                        f"indexed candidate source {source!r} must have exact type "
                        f"UInt<1>[{count}]"
                    ),
                }
        elif not _is_grounded_bool_signal(model, source):
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": (
                    f"scalar candidate source {source!r} is not grounded as a Bool"
                ),
            }
    if pivot_signal is not None and evaluator.writers(pivot_signal) is not None:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "priority pivot must be a parent-visible input/frontier signal",
        }

    found_signal = result.get("found")
    found_alias = (
        _state_alias(evaluator, str(found_signal))
        if found_signal is not None
        else None
    )
    index_target = _result_index_target(evaluator, result["index"])
    if (found_signal is not None and found_alias is None) or index_target is None:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "result signals are not exact aliases of local registers",
        }
    found_state: str | None = None
    found_alias_chain: list[dict[str, Any]] = []
    if found_alias is not None:
        found_state, found_alias_chain = found_alias
    index_state, index_alias_chain, index_projection = index_target
    if found_state is not None and found_state == index_state:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "found and index must resolve to distinct state registers",
        }
    if (
        (found_state is not None and not _is_unreset_register(model, found_state))
        or not _is_unreset_register(model, index_state)
    ):
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "implicit_unconstrained initialization requires unreset result registers",
        }
    found_width = _declared_signal_width(model, found_state) if found_state else None
    index_state_width = _declared_signal_width(model, index_state)
    index_width = (
        index_projection[0] - index_projection[1] + 1
        if index_projection is not None
        else index_state_width
    )
    pivot_width = _declared_signal_width(model, pivot_signal) if pivot_signal else None
    required_index_width = max(1, math.ceil(math.log2(count)))
    if (
        index_projection is not None
        and (
            index_state_width is None
            or index_projection[1] < 0
            or index_projection[0] < index_projection[1]
            or index_projection[0] >= index_state_width
        )
    ):
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "result index projection is outside the grounded register width",
        }
    if (
        (found_state is not None and found_width != 1)
        or index_width is None
        or index_width < required_index_width
    ):
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "result register widths do not cover the declared found/index fields",
        }
    if pivot_signal is not None and pivot_width is None:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "could not recover cyclic pivot width",
        }
    if pivot_signal is not None and (1 << int(pivot_width)) != count:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": (
                "cyclic priority currently requires the pivot bit-domain to equal "
                "index.count; non-power-of-two domains need an explicit pivot-domain constraint"
            ),
        }

    pivot_values: list[int | None] = [None]
    if pivot_signal is not None:
        pivot_values = list(range(1 << int(pivot_width)))
    source_items = sorted(candidate_sources.items())
    source_widths = [count if kind in {"packed", "array"} else 1 for _, kind in source_items]
    independent_bits = sum(source_widths)
    pivot_bits = int(pivot_width or 0)
    if independent_bits + pivot_bits > 20:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": (
                "indexed Boolean candidate equivalence would exceed the current "
                "2^20 exact enumeration limit"
            ),
        }

    checked = 0
    found_writer_ids: set[int] = set()
    index_writer_ids: set[int] = set()
    for valuation in range(1 << independent_bits):
        env: dict[str, tuple[int, int]] = {}
        source_values: dict[str, int] = {}
        offset = 0
        for (source, source_kind), source_width in zip(source_items, source_widths):
            mask = (valuation >> offset) & ((1 << source_width) - 1)
            offset += source_width
            source_values[source] = mask
            if source_kind == "packed":
                env[source] = (mask, count)
            elif source_kind == "array":
                for entry in range(count):
                    env[f"{source}[{entry}]"] = ((mask >> entry) & 1, 1)
            else:
                env[source] = (mask, 1)
        candidate_mask = 0
        for entry in range(count):
            value = _eval_candidate_expr(candidate, entry, env)
            if value is None:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": "could not evaluate the declared indexed Boolean candidate",
                }
            candidate_mask |= int(value != 0) << entry
        candidates = [
            entry for entry in range(count) if (candidate_mask >> entry) & 1
        ]
        for pivot_value in pivot_values:
            row_env = dict(env)
            if pivot_signal is not None and pivot_value is not None:
                row_env[pivot_signal] = (pivot_value, int(pivot_width))
            actual_found = (
                evaluator.next_state(found_state, row_env)
                if found_state is not None
                else None
            )
            actual_index = (
                evaluator.next_state_projected(
                    index_state,
                    index_projection[0],
                    index_projection[1],
                    row_env,
                )
                if index_projection is not None
                else evaluator.next_state(index_state, row_env)
            )
            if (found_state is not None and actual_found is None) or actual_index is None:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": "could not evaluate the complete result-register writer cone",
                    "candidate_mask": candidate_mask,
                    "candidate_source_values": source_values,
                    "pivot": pivot_value,
                }
            if actual_found is not None:
                found_writer_ids.update(actual_found[1])
            index_writer_ids.update(actual_index[1])
            expected_found = int(bool(candidates))
            expected_index = (
                _selected_index(
                    candidates,
                    kind,
                    pivot_value,
                    pivot_position=pivot_position,
                )
                if candidates
                else None
            )
            if (
                actual_found is not None
                and actual_found[0] != expected_found
            ) or (
                expected_index is not None and actual_index[0] != expected_index
            ):
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": "registered selector result differs from the declared finite priority order",
                    "counterexample": {
                        "candidate_mask": candidate_mask,
                        "candidate_source_values": source_values,
                        "pivot": pivot_value,
                        "actual_found": actual_found[0] if actual_found is not None else None,
                        "actual_index": actual_index[0],
                        "expected_found": expected_found,
                        "expected_index": expected_index,
                    },
                }
            checked += 1

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"exhaustive finite equivalence proves the {count}-candidate {kind} selector; "
            "the selected result is captured by unreset register(s) and exposed one cycle later"
        ),
        "proof_domain": "exact-registered-indexed-priority-select",
        "index": {"name": index_name, "count": count},
        "candidate_expression": candidate,
        "candidate_sources": [
            {"signal": source, "kind": source_kind}
            for source, source_kind in source_items
        ],
        "priority": priority,
        "result": {
            "found_signal": found_signal,
            "index_signal": result["index"],
            "found_state": found_state,
            "index_state": index_state,
            "found_alias_chain": found_alias_chain,
            "index_alias_chain": index_alias_chain,
            "index_projection": (
                {"hi": index_projection[0], "lo": index_projection[1]}
                if index_projection is not None
                else None
            ),
        },
        "latency_cycles": 1,
        "initialization": {"kind": "implicit_unconstrained"},
        "checked_rows": checked,
        "found_writer_statement_ids": sorted(found_writer_ids),
        "index_writer_statement_ids": sorted(index_writer_ids),
    }
