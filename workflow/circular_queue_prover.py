from __future__ import annotations

from collections import deque
import itertools
import re
from typing import Any

from .formal_patterns import (
    STRUCTURALLY_SUPPORTED as PATTERN_SUPPORTED,
    _and,
    _bool_expr,
    _bool_refs,
    _declared_signal_width,
    _index_info,
    _not,
    _occurrence_condition,
    _unsat,
    prove_combinational_forbid_when,
)
from .priority_select_prover import _ConcreteFIRRTLEvaluator
from .semantic import HandoffControlModel, _call, _literal


STRUCTURALLY_SUPPORTED = "STRUCTURALLY_SUPPORTED"
STRUCTURAL_UNKNOWN = "STRUCTURAL_UNKNOWN"
COUNTEREXAMPLE = "COUNTEREXAMPLE"

_REF_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_$]*(?:(?:\.[A-Za-z_][A-Za-z0-9_$]*)|(?:\[[^\[\]]+\]))*$"
)


def _occurrence_object(candidate: dict[str, Any], occurrence_id: str) -> dict[str, Any] | None:
    return next(
        (
            item
            for item in candidate.get("occurrences", [])
            if isinstance(item, dict) and item.get("id") == occurrence_id
        ),
        None,
    )


def _occurrence_literals(occurrence: dict[str, Any]) -> tuple[tuple[str, bool], ...] | None:
    grounding = occurrence.get("grounding")
    if not isinstance(grounding, dict):
        return None
    if grounding.get("state_register") is not None or grounding.get("state_values"):
        return None
    if grounding.get("value_tests"):
        return None
    positive = [str(item) for item in grounding.get("signals_true", [])]
    negative = [str(item) for item in grounding.get("signals_false", [])]
    if not positive and not negative:
        return None
    if set(positive) & set(negative):
        return None
    return tuple([(signal, True) for signal in positive] + [(signal, False) for signal in negative])


def _reset_value(model: HandoffControlModel, state: str) -> tuple[int, int] | None:
    width = _declared_signal_width(model, state)
    if width is None:
        return None
    declarations = [
        statement
        for statement in model.statements.values()
        if statement.get("kind") == "regreset"
        and state in {str(item) for item in statement.get("drives", [])}
    ]
    if len(declarations) != 1:
        return None
    reset_expr = str(declarations[0].get("text", "")).rsplit(",", 1)[-1].strip()
    value = _literal(reset_expr)
    if value is None or value < 0 or value >= (1 << width):
        return None
    return int(value), int(width)


def _under_any_state(model: HandoffControlModel, signal: str) -> bool:
    return any(
        signal == root or signal.startswith(root + ".") or signal.startswith(root + "[")
        for root in model.state_roots
    )


def _frontier_signals(
    evaluator: _ConcreteFIRRTLEvaluator,
    expressions: list[str],
) -> set[str] | None:
    frontier: set[str] = set()
    visiting: set[str] = set()

    def visit(expr: str) -> bool:
        text = expr.strip()
        if _literal(text) is not None:
            return True
        call = _call(text)
        if call is not None:
            return all(visit(argument) for argument in call[1])
        if not _REF_RE.fullmatch(text):
            return False
        if _under_any_state(evaluator.model, text):
            return True
        if text in visiting:
            return False
        writers = evaluator.writers(text)
        if writers is None:
            frontier.add(text)
            return True
        visiting.add(text)
        ok = all(
            visit(writer.rhs) and all(visit(control) for control, _ in writer.controls)
            for writer in writers
        )
        visiting.remove(text)
        return ok

    return frontier if all(visit(expression) for expression in expressions) else None


def _condition_value(
    evaluator: _ConcreteFIRRTLEvaluator,
    literals: tuple[tuple[str, bool], ...],
    env: dict[str, tuple[int, int]],
) -> bool | None:
    memo: dict[str, tuple[int, int]] = {}
    for signal, positive in literals:
        value = evaluator.eval(signal, env, memo=memo)
        if value is None:
            return None
        if (value[0] != 0) != positive:
            return False
    return True


def _pointer_action(
    evaluator: _ConcreteFIRRTLEvaluator,
    pointer: str,
) -> str | None:
    writers = evaluator.writers(pointer)
    if writers is None:
        return None
    controls = {
        control
        for writer in writers
        for control, positive in writer.controls
        if positive and re.fullmatch(r"h[0-9a-fA-F]+", control) is None
    }
    return next(iter(controls)) if len(controls) == 1 else None


def _occurrence_action_relation(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    occurrence_id: str,
    action: str,
) -> dict[str, Any] | None:
    refs = _bool_refs(model, candidate) | {action}
    for opaque in ({action}, set()):
        occurrence = _occurrence_condition(
            model,
            candidate,
            occurrence_id,
            refs,
            opaque=opaque,
        )
        action_expr = _bool_expr(model, refs, action, opaque=opaque)
        if occurrence is None or action_expr is None:
            continue
        occurrence_without_action, left_atoms = _unsat(_and(occurrence, _not(action_expr)))
        action_without_occurrence, right_atoms = _unsat(_and(action_expr, _not(occurrence)))
        result = {
            "occurrence_implies_action": occurrence_without_action is True,
            "action_implies_occurrence": action_without_occurrence is True,
            "occurrence_implies_action_atoms": left_atoms,
            "action_implies_occurrence_atoms": right_atoms,
            "action_cut": bool(opaque),
        }
        if result["occurrence_implies_action"]:
            return result
    return None


def _action_occurrence(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    action: str,
    index_name: str,
    domain: dict[str, int],
) -> tuple[str, dict[str, Any]] | None:
    for occurrence in candidate.get("occurrences", []):
        if not isinstance(occurrence, dict):
            continue
        metadata = _index_info(occurrence, index_name)
        if metadata is None or metadata[1] != domain:
            continue
        occurrence_id = occurrence.get("id")
        if not isinstance(occurrence_id, str):
            continue
        relation = _occurrence_action_relation(model, candidate, occurrence_id, action)
        if relation and relation["occurrence_implies_action"] and relation["action_implies_occurrence"]:
            return occurrence_id, relation
    return None


def _predicate_value(
    evaluator: _ConcreteFIRRTLEvaluator,
    predicate: dict[str, Any],
    env: dict[str, tuple[int, int]],
) -> bool | None:
    grounding = predicate.get("grounding", {})
    source = grounding.get("source_signal") if isinstance(grounding, dict) else None
    if not isinstance(source, str) or grounding.get("state_register") is not None:
        return None
    value = evaluator.eval(source, env)
    if value is None:
        return None
    result = value[0] != 0
    return not result if grounding.get("negated") else result


def _action_gates(
    model: HandoffControlModel,
    evaluator: _ConcreteFIRRTLEvaluator,
    candidate: dict[str, Any],
    occurrence_id: str,
    actions: set[str],
) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for predicate in candidate.get("predicates", []):
        if not isinstance(predicate, dict) or not isinstance(predicate.get("id"), str):
            continue
        grounding = predicate.get("grounding", {})
        source = grounding.get("source_signal") if isinstance(grounding, dict) else None
        if not isinstance(source, str):
            continue
        frontier = _frontier_signals(evaluator, [source])
        if frontier is None or not frontier <= actions:
            continue
        proof = prove_combinational_forbid_when(
            model,
            candidate,
            occurrence=occurrence_id,
            predicate=str(predicate["id"]),
        )
        if proof.get("status") != PATTERN_SUPPORTED:
            continue
        gates.append({"predicate": predicate, "certificate": proof})
    return gates


def prove_same_index_circular_queue_provenance(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
    scope_index: dict[str, str],
    required_prior: str | None = None,
) -> dict[str, Any]:
    """Prove strict same-slot history with exhaustive RTL control + ghost tokens.

    The RTL state transition is evaluated exactly for every finite Boolean
    frontier valuation.  A proof-only token bit is created by `before(i)` and
    consumed by `after(i)`.  Checking consumption before same-cycle creation
    establishes strict `<mu`, including simultaneous enqueue/dequeue cycles.
    """

    if required_prior is not None or scope_index.get("relation") != "same":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported indexed history shape"}
    name = scope_index.get("name")
    if not isinstance(name, str) or not name:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "missing scope index name"}
    before_obj = _occurrence_object(candidate, before)
    after_obj = _occurrence_object(candidate, after)
    if before_obj is None or after_obj is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "before/after occurrence missing"}
    before_meta = _index_info(before_obj, name)
    after_meta = _index_info(after_obj, name)
    if before_meta is None or after_meta is None or before_meta[1] != after_meta[1]:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "incompatible occurrence index metadata"}
    before_index, domain = before_meta
    after_index, _ = after_meta
    count = domain["end_exclusive"] - domain["start"]
    if domain["start"] != 0 or count < 1 or count > 16:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "exact ghost-token reachability supports zero-based domains of 1..16 slots",
        }

    evaluator = _ConcreteFIRRTLEvaluator(model)
    before_action = _pointer_action(evaluator, before_index)
    after_action = _pointer_action(evaluator, after_index)
    if before_action is None or after_action is None or before_action == after_action:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "could not recover distinct enqueue/dequeue pointer-advance actions",
        }
    before_relation = _occurrence_action_relation(model, candidate, before, before_action)
    after_relation = _occurrence_action_relation(model, candidate, after, after_action)
    if not before_relation or not (
        before_relation["occurrence_implies_action"]
        and before_relation["action_implies_occurrence"]
    ):
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "before occurrence is not exactly the enqueue pointer-advance action",
        }
    if not after_relation or not after_relation["occurrence_implies_action"]:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "after occurrence does not imply dequeue pointer advance",
        }
    before_action_occurrence = _action_occurrence(
        model, candidate, before_action, name, domain
    )
    after_action_occurrence = _action_occurrence(
        model, candidate, after_action, name, domain
    )
    if before_action_occurrence is None or after_action_occurrence is None:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "pointer action lacks an exact indexed occurrence object",
        }

    reset_candidates = {
        state: _reset_value(model, state)
        for state in sorted(model.state_roots)
        if _declared_signal_width(model, state) is not None
    }
    states = sorted(state for state, value in reset_candidates.items() if value is not None)
    reset: dict[str, tuple[int, int]] = {}
    for state in states:
        reset[state] = reset_candidates[state]  # type: ignore[assignment]
    total_state_bits = sum(width for _, width in reset.values())
    if total_state_bits > 16:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": f"RTL control state exceeds exact reachability bound ({total_state_bits} bits)",
        }
    for pointer in (before_index, after_index):
        width = _declared_signal_width(model, pointer)
        if pointer not in reset or width is None or (1 << width) != count:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "occurrence indices are not full-domain resettable circular pointers",
                "pointer": pointer,
            }

    actions = {before_action, after_action}
    before_gates = _action_gates(
        model,
        evaluator,
        candidate,
        before_action_occurrence[0],
        actions,
    )
    after_gates = _action_gates(
        model,
        evaluator,
        candidate,
        after_action_occurrence[0],
        actions,
    )
    if not before_gates or not after_gates:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": "pointer actions lack exact state-only full/empty exclusion gates",
        }

    state_widths = {state: reset[state][1] for state in states}
    initial_values = tuple(reset[state][0] for state in states)
    initial = (initial_values, 0)
    work = deque([initial])
    depth = {initial: 0}
    transition_count = 0
    writer_ids: dict[str, set[int]] = {state: set() for state in states}
    input_names = sorted(actions)
    while work:
        state_values, token_mask = work.popleft()
        for input_values in itertools.product((0, 1), repeat=len(input_names)):
            env = {
                state: (value, state_widths[state])
                for state, value in zip(states, state_values)
            }
            env.update({signal: (value, 1) for signal, value in zip(input_names, input_values)})
            before_fire = bool(env[before_action][0])
            after_fire = bool(env[after_action][0])
            skip = False
            for fire, gates in ((before_fire, before_gates), (after_fire, after_gates)):
                if not fire:
                    continue
                for gate in gates:
                    blocked = _predicate_value(evaluator, gate["predicate"], env)
                    if blocked is None:
                        return {
                            "status": STRUCTURAL_UNKNOWN,
                            "reason": "a certified pointer-action gate could not be evaluated",
                            "predicate": gate["predicate"].get("id"),
                        }
                    if blocked:
                        skip = True
                        break
                if skip:
                    break
            if skip:
                continue
            before_slot = env[before_index][0]
            after_slot = env[after_index][0]
            if before_slot >= count or after_slot >= count:
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": "reachable occurrence index is outside its declared domain",
                    "counterexample": {
                        "depth": depth[(state_values, token_mask)],
                        "state": dict(zip(states, state_values)),
                        "inputs": dict(zip(input_names, input_values)),
                        "before_index": before_slot,
                        "after_index": after_slot,
                    },
                }
            if after_fire and not ((token_mask >> after_slot) & 1):
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": f"{after} can consume a slot with no prior unmatched {before}",
                    "counterexample": {
                        "depth": depth[(state_values, token_mask)],
                        "state": dict(zip(states, state_values)),
                        "ghost_token_mask": token_mask,
                        "inputs": dict(zip(input_names, input_values)),
                        "after_index": after_slot,
                        "before_same_cycle": bool(before_fire),
                    },
                }

            next_values: list[int] = []
            for state in states:
                result = evaluator.next_state(state, env)
                if result is None:
                    return {
                        "status": STRUCTURAL_UNKNOWN,
                        "reason": f"could not evaluate complete next-state cone for {state!r}",
                    }
                next_values.append(result[0])
                writer_ids[state].update(result[1])
            next_mask = token_mask
            if after_fire:
                next_mask &= ~(1 << after_slot)
            if before_fire:
                next_mask |= 1 << before_slot
            successor = (tuple(next_values), next_mask)
            transition_count += 1
            if successor not in depth:
                if len(depth) >= 200_000:
                    return {
                        "status": STRUCTURAL_UNKNOWN,
                        "reason": "ghost-token reachability exceeds 200000-state bound",
                    }
                depth[successor] = depth[(state_values, token_mask)] + 1
                work.append(successor)

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"exhaustive post-reset reachability proves every {after}({name}) consumes a "
            f"ghost token created by a strictly prior {before}({name})"
        ),
        "proof_domain": "exact-circular-queue-slot-provenance",
        "before": before,
        "after": after,
        "index": {"name": name, "domain": domain},
        "before_index_signal": before_index,
        "after_index_signal": after_index,
        "before_action": before_action,
        "after_action": after_action,
        "before_action_occurrence": before_action_occurrence[0],
        "after_action_occurrence": after_action_occurrence[0],
        "before_action_relation": before_relation,
        "after_action_relation": after_relation,
        "before_gate_certificates": before_gates,
        "after_gate_certificates": after_gates,
        "rtl_state": [
            {
                "signal": state,
                "width": state_widths[state],
                "reset": reset[state][0],
                "writer_statement_ids": sorted(writer_ids[state]),
            }
            for state in states
        ],
        "frontier_inputs": input_names,
        "reachable_ghost_states": len(depth),
        "checked_transitions": transition_count,
        "strict_same_cycle_rule": "consume-old-token-before-create-new-token",
    }
