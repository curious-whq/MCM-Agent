from __future__ import annotations

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Callable, Iterable

from .research_memory import write_run_summary
from .axiom_ir import compile_formal_axiom, render_formal_axiom


SEMANTIC_VALIDATOR_VERSION = "semantic-validator-0.23"
PROPERTY_COMPILER_VERSION = "formal-axiom-compiler-0.13"

# Structural/static checker outcomes. These deliberately do NOT use the word
# "proved": they are evidence about an extracted control/dataflow abstraction,
# not a bit-level proof of the concrete RTL.
STRUCTURALLY_SUPPORTED = "STRUCTURALLY_SUPPORTED"
COUNTEREXAMPLE = "COUNTEREXAMPLE"
STRUCTURAL_UNKNOWN = "STRUCTURAL_UNKNOWN"
PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"

# Validation levels exposed to the workflow. Only FORMALLY_PROVED / SPEC_PROVED
# may enter the trusted µMCM.
GROUNDED = "GROUNDED"
FORMALLY_PROVED = "FORMALLY_PROVED"
SPEC_PROVED = "SPEC_PROVED"
UNRESOLVED = "UNRESOLVED"
REFUTED = "REFUTED"


_LITERAL_RE = re.compile(r'UInt(?:<\d+>)?\((?:0h([0-9a-fA-F]+)|"h([0-9a-fA-F]+)"|(\d+))\)')
_NODE_RE = re.compile(r"^node\s+([^\s=]+)\s*=\s*(.*)$")
_CONNECT_RE = re.compile(r"^connect\s+([^,]+),\s*(.*)$")
_ASSIGN_RE = re.compile(r"^([^\s]+)\s*<=\s*(.*)$")
_REGRESET_RE = re.compile(r'^regreset\s+([^\s:]+).*UInt(?:<\d+>)?\((?:0h([0-9a-fA-F]+)|"h([0-9a-fA-F]+)"|(\d+))\)')
_LEGACY_RESET_RE = re.compile(r'^reg\s+([^\s:]+).*reset.*UInt(?:<\d+>)?\((?:0h([0-9a-fA-F]+)|"h([0-9a-fA-F]+)"|(\d+))\)')
_SIMPLE_REF_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_$]*(?:(?:\.[A-Za-z_][A-Za-z0-9_$]*)|(?:\[[^\[\]]+\]))*$"
)


def _split_args(text: str) -> list[str]:
    out: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            out.append(text[start:index].strip())
            start = index + 1
    out.append(text[start:].strip())
    return out


def _call(expr: str) -> tuple[str, list[str]] | None:
    expr = expr.strip()
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_$]*)\((.*)\)$", expr)
    if match is None:
        return None
    return match.group(1), _split_args(match.group(2))


def _literal(expr: str) -> int | None:
    text = expr.strip()
    if text.isdigit():
        return int(text)
    match = _LITERAL_RE.fullmatch(text)
    if match is None:
        return None
    if match.group(1) is not None:
        return int(match.group(1), 16)
    if match.group(2) is not None:
        return int(match.group(2), 16)
    return int(match.group(3))


@dataclass(frozen=True)
class Transition:
    src: int
    dst: int
    statement_id: int | None
    guard_leaves: frozenset[str]
    labels: frozenset[str] = frozenset()

    def to_dict(self) -> dict[str, Any]:
        return {
            "src": self.src,
            "dst": self.dst,
            "statement_id": self.statement_id,
            "guard_leaves": sorted(self.guard_leaves),
            "labels": sorted(self.labels),
        }


class HandoffControlModel:
    """Small fail-closed finite-control abstraction extracted from a leaf handoff.

    It deliberately reasons only about one resettable control register and
    treats data-dependent mux branches as nondeterministic.  Therefore an
    ordering/exclusion property proved on this graph is robust to *more* branch
    behaviors than the concrete RTL.  Data/value properties are handled by
    separate structural checkers or left structurally unresolved for an external formal backend.
    """

    def __init__(self, handoff: dict[str, Any], state_register: str = "state"):
        self.handoff = handoff
        self.state_register = state_register
        self.state_roots = {str(item.get("id")) for item in handoff.get("state", []) if item.get("id")}
        proof_context = handoff.get("proof_context", {})
        bridge_statements = (
            proof_context.get("event_gate_statements", [])
            if isinstance(proof_context, dict)
            else []
        )
        state_support_statements = (
            proof_context.get("state_support_statements", [])
            if isinstance(proof_context, dict)
            else []
        )
        state_writer_control_statements = (
            proof_context.get("state_writer_control_statements", [])
            if isinstance(proof_context, dict)
            else []
        )
        visible_statements = list(handoff.get("statements", []))
        visible_ids = {
            int(statement["id"])
            for statement in visible_statements
            if isinstance(statement, dict) and "id" in statement
        }
        self.proof_context_statement_ids = {
            int(statement["id"])
            for statement in [
                *bridge_statements,
                *state_support_statements,
                *state_writer_control_statements,
            ]
            if isinstance(statement, dict) and "id" in statement
        } - visible_ids
        self.statements = {
            int(statement["id"]): statement
            for statement in [
                *visible_statements,
                *bridge_statements,
                *state_support_statements,
                *state_writer_control_statements,
            ]
        }
        self.driver: dict[str, tuple[int, str]] = {}
        self.definition_statement: dict[str, int] = {}
        self._rhs_projection_cache: dict[str, str | None] = {}
        self._build_drivers()
        self.reset_state = self._find_reset_state()
        self.known_states = self._find_known_states()
        self.transitions = self._extract_transitions()
        self._label_occurrences({})

    def _build_drivers(self) -> None:
        for statement_id, statement in self.statements.items():
            text = statement.get("text", "")
            node = _NODE_RE.match(text)
            if node:
                name, rhs = node.groups()
                self.driver[name] = (statement_id, rhs)
                self.definition_statement[name] = statement_id
                continue
            connect = _CONNECT_RE.match(text) or _ASSIGN_RE.match(text)
            if not connect:
                continue
            lhs, rhs = (part.strip() for part in connect.groups())
            drives = statement.get("drives", [])
            for signal in drives:
                mapped_rhs = rhs
                if _SIMPLE_REF_RE.fullmatch(rhs):
                    if signal == lhs:
                        mapped_rhs = rhs
                    elif signal.startswith(lhs + ".") or signal.startswith(lhs + "["):
                        mapped_rhs = rhs + signal[len(lhs):]
                self.driver[signal] = (statement_id, mapped_rhs)
                self.definition_statement[signal] = statement_id

    def _project_aggregate_rhs(self, rhs: str, suffix: str) -> str | None:
        """Project an aggregate RHS onto one lowered leaf.

        FIRRTL aggregate connects such as ``io.release.bits := mux(..., a, b)``
        are recorded as leaf drivers like ``_tmp.opcode``.  The temporary itself
        is a mux over aggregate values, so exact local proofs need to push the
        leaf suffix through that mux rather than giving up at the aggregate node.
        """
        text = rhs.strip()
        if _SIMPLE_REF_RE.fullmatch(text):
            return text + suffix
        call = _call(text)
        if call is None:
            return None
        name, args = call
        if name == "mux" and len(args) == 3:
            high = self._project_aggregate_rhs(args[1], suffix)
            low = self._project_aggregate_rhs(args[2], suffix)
            if high is None or low is None:
                return None
            return f"mux({args[0]}, {high}, {low})"
        return None

    def rhs(self, signal: str) -> str | None:
        entry = self.driver.get(signal)
        if entry:
            return entry[1]
        if signal in self._rhs_projection_cache:
            return self._rhs_projection_cache[signal]
        # Recover leaf projections through a driven aggregate temporary.
        # A projection may cross both record fields and nested vector indices,
        # e.g. ``allowed[0]`` or ``foo[1].bar[2]``.
        # Enumerate only syntactic path prefixes of this signal.  Scanning and
        # sorting every driver made Boolean-cone discovery quadratic on large
        # LSU handoffs, where rhs() is queried tens of thousands of times.
        prefixes = list(reversed([
            signal[:index]
            for index, char in enumerate(signal)
            if char in ".[" and signal[:index] in self.driver
        ]))
        for base in prefixes:
            entry = self.driver[base]
            suffix = signal[len(base):]
            projected = self._project_aggregate_rhs(entry[1], suffix)
            if projected is not None:
                self._rhs_projection_cache[signal] = projected
                return projected
        self._rhs_projection_cache[signal] = None
        return None

    def _possible_ints(self, expr: str, seen: set[str] | None = None) -> set[int] | None:
        expr = expr.strip()
        value = _literal(expr)
        if value is not None:
            return {value}
        if seen is None:
            seen = set()
        if _SIMPLE_REF_RE.fullmatch(expr):
            if expr in seen:
                return None
            rhs = self.rhs(expr)
            if rhs is None:
                return None
            return self._possible_ints(rhs, seen | {expr})
        call = _call(expr)
        if call is None:
            return None
        name, args = call
        if name == "mux" and len(args) == 3:
            high = self._possible_ints(args[1], seen)
            low = self._possible_ints(args[2], seen)
            if high is None or low is None:
                return None
            return high | low
        if name == "bits" and len(args) == 3:
            values = self._possible_ints(args[0], seen)
            hi = _literal(args[1])
            lo = _literal(args[2])
            if values is None or hi is None or lo is None:
                return None
            mask = (1 << (hi - lo + 1)) - 1
            return {(value >> lo) & mask for value in values}
        return None

    def possible_signal_values(self, signal: str) -> set[int] | None:
        return self._possible_ints(signal)

    def _bool_for_state(self, expr: str, state: int, seen: set[str] | None = None) -> bool | None:
        expr = expr.strip()
        value = _literal(expr)
        if value is not None:
            return bool(value)
        if expr == self.state_register:
            return bool(state)
        if seen is None:
            seen = set()
        if _SIMPLE_REF_RE.fullmatch(expr):
            if expr in seen:
                return None
            rhs = self.rhs(expr)
            if rhs is None:
                return None
            return self._bool_for_state(rhs, state, seen | {expr})
        call = _call(expr)
        if call is None:
            return None
        name, args = call
        if name in {"eq", "neq"} and len(args) == 2:
            def int_for(arg: str) -> int | None:
                if arg.strip() == self.state_register:
                    return state
                values = self._possible_ints(arg, seen)
                if values is not None and len(values) == 1:
                    return next(iter(values))
                return None
            left = int_for(args[0])
            right = int_for(args[1])
            if left is None or right is None:
                return None
            result = left == right
            return result if name == "eq" else not result
        if name == "not" and len(args) == 1:
            value = self._bool_for_state(args[0], state, seen)
            return None if value is None else not value
        if name == "and" and len(args) == 2:
            left = self._bool_for_state(args[0], state, seen)
            right = self._bool_for_state(args[1], state, seen)
            if left is False or right is False:
                return False
            if left is True and right is True:
                return True
            return None
        if name == "or" and len(args) == 2:
            left = self._bool_for_state(args[0], state, seen)
            right = self._bool_for_state(args[1], state, seen)
            if left is True or right is True:
                return True
            if left is False and right is False:
                return False
            return None
        if name == "mux" and len(args) == 3:
            select = self._bool_for_state(args[0], state, seen)
            if select is True:
                return self._bool_for_state(args[1], state, seen)
            if select is False:
                return self._bool_for_state(args[2], state, seen)
            high = self._bool_for_state(args[1], state, seen)
            low = self._bool_for_state(args[2], state, seen)
            return high if high == low else None
        return None

    def states_where_signal_true(self, signal: str, *, negated: bool = False) -> set[int] | None:
        if not self.known_states:
            return None
        out: set[int] = set()
        for state in self.known_states:
            value = self._bool_for_state(signal, state)
            if value is None:
                return None
            if negated:
                value = not value
            if value:
                out.add(state)
        return out

    def _state_test(self, signal: str) -> tuple[int, int] | None:
        rhs = self.rhs(signal)
        if rhs is None:
            return None
        call = _call(rhs)
        if call is None or call[0] != "eq" or len(call[1]) != 2:
            return None
        args = call[1]
        for state_arg, literal_arg in ((args[0], args[1]), (args[1], args[0])):
            if state_arg.strip() != self.state_register:
                continue
            value = _literal(literal_arg)
            if value is not None:
                return self.definition_statement.get(signal, -1), value
        return None

    def _positive_state_tests(
        self,
        expr: str,
        seen: set[str] | None = None,
    ) -> list[tuple[int, int]]:
        """Recover state equalities required by a positive Boolean guard.

        Lowered Decoupled fires commonly look like ``and(ready, valid)``, with
        ``ready`` or ``valid`` in turn aliasing ``eq(state, S)``.  Looking only
        at the immediate ``control_reads`` therefore misses the FSM source
        state.  This routine follows aliases and conjunctions, but deliberately
        refuses to infer a required state through disjunction, negation, or a
        data-dependent mux.
        """

        text = expr.strip()
        seen = seen or set()
        if text in seen:
            return []

        if _SIMPLE_REF_RE.fullmatch(text):
            direct = self._state_test(text)
            if direct is not None:
                return [direct]
            rhs = self.rhs(text)
            if rhs is None:
                return []
            return self._positive_state_tests(rhs, seen | {text})

        call = _call(text)
        if call is None:
            return []
        name, args = call
        if name == "eq" and len(args) == 2:
            for state_arg, literal_arg in ((args[0], args[1]), (args[1], args[0])):
                if state_arg.strip() != self.state_register:
                    continue
                value = _literal(literal_arg)
                if value is not None:
                    return [(-1, value)]
        if name == "and" and len(args) == 2:
            return (
                self._positive_state_tests(args[0], seen)
                + self._positive_state_tests(args[1], seen)
            )
        # Equality-to-one and inequality-to-zero preserve positive Boolean
        # polarity after FIRRTL lowering.
        if name in {"eq", "neq"} and len(args) == 2:
            for value_arg, literal_arg in ((args[0], args[1]), (args[1], args[0])):
                literal = _literal(literal_arg)
                positive = (name == "eq" and literal == 1) or (name == "neq" and literal == 0)
                if positive:
                    return self._positive_state_tests(value_arg, seen)
        return []

    def _source_state(self, statement: dict[str, Any]) -> int | None:
        candidates: list[tuple[int, int]] = []
        for control in statement.get("control_reads", []):
            candidates.extend(self._positive_state_tests(control))
        if candidates:
            # In lowered else-if chains older state comparisons remain in the
            # control set with negative polarity.  The latest defining state-eq node
            # is the innermost positive `when` and therefore the active source state.
            return max(candidates)[1]

        # Legacy FIRRTL fixtures keep `when eq(state, ...)` as a direct
        # expression, so control_reads contains only `state`.  Use the nearest
        # preceding direct state guard as a conservative compatibility path.
        statement_id = int(statement.get("id", -1))
        for previous_id in range(statement_id - 1, -1, -1):
            previous = self.statements.get(previous_id)
            if previous is None or previous.get("kind") != "when":
                continue
            text = previous.get("text", "").strip()
            match = re.match(r"^when\s+eq\(([^,]+),\s*(UInt[^)]*\))\)\s*:", text)
            if match and match.group(1).strip() == self.state_register:
                value = _literal(match.group(2))
                if value is not None:
                    return value
        return None

    def _expand_leaves(self, signal: str, seen: set[str] | None = None) -> set[str]:
        if seen is None:
            seen = set()
        if signal in seen:
            return set()
        # Registers are temporal state leaves, not combinational aliases.  Inlining
        # their last syntactic write loses guards such as ``acked`` and is unsound
        # for history reasoning.
        if any(_under_root(signal, root) for root in self.state_roots):
            return {signal}
        rhs = self.rhs(signal)
        if rhs is None:
            return {signal}
        seen = seen | {signal}
        refs = re.findall(r"[A-Za-z_][A-Za-z0-9_.$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*)*", rhs)
        reserved = {
            "UInt", "SInt", "eq", "neq", "and", "or", "not", "mux", "bits",
            "cat", "shr", "shl", "orr", "andr", "asUInt", "h0", "h1", "h2",
            "h3", "h4", "h5", "h6", "h7", "h8", "h9", "ha",
        }
        out: set[str] = set()
        for ref in refs:
            if ref in reserved:
                continue
            if ref == self.state_register:
                out.add(ref)
            elif self.rhs(ref) is not None:
                out.update(self._expand_leaves(ref, seen))
            else:
                out.add(ref)
        return out

    def _find_reset_state(self) -> int | None:
        for statement in self.statements.values():
            text = statement.get("text", "")
            match = _REGRESET_RE.match(text) or _LEGACY_RESET_RE.match(text)
            if match and match.group(1) == self.state_register:
                if match.group(2):
                    return int(match.group(2), 16)
                if match.group(3):
                    return int(match.group(3), 16)
                return int(match.group(4))
        return None

    def _find_known_states(self) -> set[int]:
        states: set[int] = set()
        if self.reset_state is not None:
            states.add(self.reset_state)
        for statement in self.statements.values():
            if self.state_register not in statement.get("drives", []):
                continue
            connect = _CONNECT_RE.match(statement.get("text", "")) or _ASSIGN_RE.match(statement.get("text", ""))
            if connect is None:
                continue
            values = self._possible_ints(connect.group(2))
            if values:
                states.update(values)
        return states

    def _extract_transitions(self) -> list[Transition]:
        transitions: list[Transition] = []
        for statement_id, statement in self.statements.items():
            if self.state_register not in statement.get("drives", []):
                continue
            source = self._source_state(statement)
            if source is None:
                # reset declaration or a state write not controlled by the FSM
                continue
            connect = _CONNECT_RE.match(statement.get("text", "")) or _ASSIGN_RE.match(statement.get("text", ""))
            if connect is None:
                continue
            targets = self._possible_ints(connect.group(2))
            if not targets:
                continue
            leaves: set[str] = set()
            for control in statement.get("control_reads", []):
                leaves.update(self._expand_leaves(control))
            for target in targets:
                transitions.append(
                    Transition(source, target, statement_id, frozenset(leaves))
                )
        # Staying in a state while a ready/valid condition is false is always a
        # conservative possibility.  Unlabelled self loops preserve soundness
        # for history/order checks and avoid accidental liveness assumptions.
        for state in sorted(self.known_states):
            transitions.append(Transition(state, state, None, frozenset()))
        return transitions

    def predicate_states(self, predicate: dict[str, Any]) -> set[int] | None:
        grounding = predicate.get("grounding", {})
        explicit = grounding.get("state_values", [])
        if explicit:
            return set(int(value) for value in explicit)
        source = grounding.get("source_signal")
        if source is None:
            return None
        return self.states_where_signal_true(source, negated=bool(grounding.get("negated")))

    def _event_info(self, physical_id: str) -> dict[str, Any] | None:
        for event in self.handoff.get("events", []):
            if event.get("id") == physical_id:
                return event
        return None

    def _boundary_gate_states(self, occurrence: dict[str, Any]) -> tuple[set[int] | None, str | None]:
        physical_ids = occurrence.get("physical_event_ids", [])
        if len(physical_ids) != 1:
            return None, None
        event = self._event_info(physical_ids[0])
        if event is None:
            return None, None
        if event.get("direction") == "receive":
            gate = event.get("ready")
            counterpart = event.get("valid")
        else:
            gate = event.get("valid")
            counterpart = event.get("ready")
        if gate is None:
            return None, counterpart
        return self.states_where_signal_true(gate), counterpart

    def label_occurrences(self, occurrences: Iterable[dict[str, Any]]) -> None:
        label_map: list[set[str]] = [set(t.labels) for t in self.transitions]
        for occurrence in occurrences:
            occurrence_id = occurrence.get("id")
            if not isinstance(occurrence_id, str):
                continue
            if occurrence.get("kind") == "boundary":
                gate_states, counterpart = self._boundary_gate_states(occurrence)
                if gate_states is None or counterpart is None:
                    continue
                for index, transition in enumerate(self.transitions):
                    if transition.statement_id is None:
                        continue
                    if transition.src in gate_states and counterpart in transition.guard_leaves:
                        label_map[index].add(occurrence_id)
            elif occurrence.get("kind") == "derived":
                grounding = occurrence.get("grounding", {})
                states = set(grounding.get("state_values", []))
                required_true = set(grounding.get("signals_true", []))
                required_false = set(grounding.get("signals_false", []))
                if required_false:
                    # Negative guard polarity is not represented by the current
                    # finite-control graph; leave this occurrence unlabelled so
                    # any dependent property becomes UNKNOWN rather than unsound.
                    continue
                for index, transition in enumerate(self.transitions):
                    if transition.statement_id is None:
                        continue
                    if states and transition.src not in states:
                        continue
                    if required_true <= transition.guard_leaves:
                        label_map[index].add(occurrence_id)
        # A semantic milestone often coincides with a state write even when FIRRTL
        # lowering hides the original guard behind counter temporaries.  If the
        # candidate explicitly cites that state-write statement as evidence, label
        # the transition directly.  This is stronger grounding than trying to
        # reconstruct the source-level boolean expression from flattened leaves.
        for occurrence in occurrences:
            occurrence_id = occurrence.get("id")
            if not isinstance(occurrence_id, str):
                continue
            evidence_ids = {int(x) for x in occurrence.get("evidence_statement_ids", [])}
            grounding = occurrence.get("grounding", {})
            states = {int(x) for x in grounding.get("state_values", [])}
            for index, transition in enumerate(self.transitions):
                if transition.statement_id is None or transition.statement_id not in evidence_ids:
                    continue
                if states and transition.src not in states:
                    continue
                label_map[index].add(occurrence_id)

        # Some real occurrences (grant arrival, a non-final beat, etc.) do not write
        # the main FSM state at all.  For a derived occurrence with an explicit
        # control-state set, conservatively place it on the existing stutter edge of
        # those states.  This over-approximates *when* the event may happen, which is
        # safe for exclusion/order proofs and avoids inventing progress.  Evidence-
        # backed state transitions above are preferred whenever available.
        already_mapped = {label for labels in label_map for label in labels}
        for occurrence in occurrences:
            occurrence_id = occurrence.get("id")
            if not isinstance(occurrence_id, str) or occurrence_id in already_mapped:
                continue
            grounding = occurrence.get("grounding", {})
            if grounding.get("signals_false"):
                continue
            states = {int(x) for x in grounding.get("state_values", [])}
            if not states:
                # Boundary handshakes frequently do not change the FSM state.  Infer
                # their conservative source-state set from any source-controlled
                # evidence statement instead of requiring a state transition.
                for statement_id in occurrence.get("evidence_statement_ids", []):
                    statement = self.statements.get(int(statement_id))
                    if statement is None:
                        continue
                    source = self._source_state(statement)
                    if source is not None:
                        states.add(source)
            if not states:
                continue
            for index, transition in enumerate(self.transitions):
                if transition.statement_id is None and transition.src == transition.dst and transition.src in states:
                    label_map[index].add(occurrence_id)

        self.transitions = [
            Transition(t.src, t.dst, t.statement_id, t.guard_leaves, frozenset(label_map[i]))
            for i, t in enumerate(self.transitions)
        ]

    # compatibility no-op used during construction
    def _label_occurrences(self, _: dict[str, Any]) -> None:
        return

    def occurrence_source_states(self, occurrence_id: str) -> set[int]:
        return {
            transition.src
            for transition in self.transitions
            if occurrence_id in transition.labels
        }

    def backward_depends_on(self, target: str, root: str) -> bool:
        predecessors: dict[str, set[str]] = {}
        for edge in self.handoff.get("dependency_edges", []):
            predecessors.setdefault(edge["dst"], set()).add(edge["src"])
        queue = deque([target])
        seen: set[str] = set()
        while queue:
            signal = queue.popleft()
            if signal == root or signal.startswith(root + "."):
                return True
            if signal in seen:
                continue
            seen.add(signal)
            queue.extend(predecessors.get(signal, ()))
        return False

    def write_statements(self, root: str) -> list[dict[str, Any]]:
        return [
            statement
            for statement in self.statements.values()
            if any(drive == root or drive.startswith(root + ".") for drive in statement.get("drives", []))
            and statement.get("kind") in {"connect", "invalidate"}
        ]


def compile_candidate_properties(candidate: dict[str, Any]) -> dict[str, Any]:
    """Compile formal µMCM axiom ASTs to deterministic proof obligations.

    The candidate contains no separate LLM-authored validation program. The
    obligation, references, checker and human-readable formula are all derived
    from the same formal AST, which is the unique semantic source of truth.
    """

    obligations = []
    for axiom in candidate.get("axioms", []):
        formal = axiom.get("formal")
        compiled = compile_formal_axiom(formal)
        obligations.append(
            {
                "axiom_id": axiom.get("id"),
                "axiom_kind": compiled["kind"],
                "formal": formal,
                "rendered_formula": render_formal_axiom(formal),
                "checker": compiled["checker"],
                "arguments": compiled["arguments"],
                "references": compiled["references"],
                "evidence_statement_ids": axiom.get("evidence_statement_ids", []),
            }
        )
    return {
        "compiler": PROPERTY_COMPILER_VERSION,
        "schema_version": candidate.get("schema_version"),
        "work_unit_id": candidate.get("work_unit_id"),
        "obligations": obligations,
    }


def _trace_payload(path: list[Transition]) -> list[dict[str, Any]]:
    return [transition.to_dict() for transition in path if transition.statement_id is not None or transition.labels]


def _history_order(
    model: HandoffControlModel,
    *,
    before: str,
    after: str,
    required_prior: str | None = None,
) -> dict[str, Any]:
    if model.reset_state is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no reset state for finite-control model"}
    if not model.occurrence_source_states(before) or not model.occurrence_source_states(after):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "before/after occurrence could not be mapped to control transitions"}
    if required_prior and not model.occurrence_source_states(required_prior):
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"required_prior occurrence {required_prior!r} could not be mapped"}

    start = (model.reset_state, False, False)
    queue = deque([start])
    parent: dict[tuple[int, bool, bool], tuple[tuple[int, bool, bool], Transition] | None] = {start: None}

    while queue:
        state, seen_before, seen_required = queue.popleft()
        for transition in model.transitions:
            if transition.src != state:
                continue
            labels = transition.labels
            requirement_met = required_prior is None or seen_required or required_prior in labels
            if after in labels and requirement_met and not seen_before:
                path: list[Transition] = [transition]
                cursor = (state, seen_before, seen_required)
                while parent[cursor] is not None:
                    previous, edge = parent[cursor]
                    path.append(edge)
                    cursor = previous
                path.reverse()
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": f"{after} reachable in one transaction without prior {before}",
                    "counterexample": _trace_payload(path),
                }

            next_before = seen_before or before in labels
            next_required = seen_required or (required_prior in labels if required_prior else False)
            if transition.dst == model.reset_state and transition.src != model.reset_state:
                next_before = False
                next_required = False
            key = (transition.dst, next_before, next_required)
            if key not in parent:
                parent[key] = ((state, seen_before, seen_required), transition)
                queue.append(key)

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": "finite-control over-approximation found no transaction path violating history order",
    }



def _history_chain(
    model: HandoffControlModel,
    *,
    sequence: list[str],
) -> dict[str, Any]:
    if len(sequence) < 2:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "history_chain requires at least two occurrences"}
    proofs = []
    first = sequence[0]
    for index, (before, after) in enumerate(zip(sequence, sequence[1:])):
        result = _history_order(
            model,
            before=before,
            after=after,
            required_prior=(first if index > 0 else None),
        )
        proofs.append({"before": before, "after": after, **result})
        if result["status"] == COUNTEREXAMPLE:
            return {
                "status": COUNTEREXAMPLE,
                "reason": f"history chain failed at {before} < {after}",
                "subresults": proofs,
                "counterexample": result.get("counterexample"),
            }
        if result["status"] != STRUCTURALLY_SUPPORTED:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"history chain unresolved at {before} < {after}",
                "subresults": proofs,
            }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": "all adjacent strict-history obligations in the transaction chain hold",
        "subresults": proofs,
    }


def _candidate_occurrence(candidate: dict[str, Any], occurrence_id: str) -> dict[str, Any] | None:
    return next((item for item in candidate.get("occurrences", []) if item.get("id") == occurrence_id), None)


def _statement_rhs(statement: dict[str, Any]) -> tuple[str, str] | None:
    text = statement.get("text", "")
    match = _CONNECT_RE.match(text) or _ASSIGN_RE.match(text)
    if match is None:
        return None
    return tuple(part.strip() for part in match.groups())  # type: ignore[return-value]


def _control_expr_reaches(
    model: HandoffControlModel,
    controls: Iterable[str],
    predicate,
    seen: set[str] | None = None,
) -> bool:
    """Return whether a flattened control cone contains an expression predicate."""
    seen = set() if seen is None else set(seen)
    queue = deque(str(item) for item in controls)
    while queue:
        expr = queue.popleft().strip()
        if expr in seen:
            continue
        seen.add(expr)
        if predicate(expr):
            return True
        rhs = model.rhs(expr) if _SIMPLE_REF_RE.fullmatch(expr) else None
        if rhs is not None:
            queue.append(rhs)
            continue
        call = _call(expr)
        if call is not None:
            queue.extend(call[1])
    return False


def _control_has_eq(model: HandoffControlModel, statement: dict[str, Any], signal: str, value: int) -> bool:
    def matches(expr: str) -> bool:
        call = _call(expr)
        if call is None or call[0] != "eq" or len(call[1]) != 2:
            return False
        a, b = call[1]
        return ((a.strip() == signal and _literal(b) == value) or
                (b.strip() == signal and _literal(a) == value))
    return _control_expr_reaches(model, statement.get("control_reads", []), matches)


def _control_mentions(model: HandoffControlModel, statement: dict[str, Any], signal: str) -> bool:
    def matches(expr: str) -> bool:
        if expr.strip() == signal:
            return True
        call = _call(expr)
        return call is not None and any(arg.strip() == signal for arg in call[1])
    return _control_expr_reaches(model, statement.get("control_reads", []), matches)


def _identity_capture_occurrences(candidate: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for axiom in candidate.get("axioms", []):
        formal = axiom.get("formal", {})
        if formal.get("type") != "identity_flow":
            continue
        capture = formal.get("capture", {})
        if isinstance(capture.get("on"), str):
            out.add(capture["on"])
    return out


def _latched_prerequisite_proof(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    prerequisite: str,
    after: str,
) -> dict[str, Any] | None:
    """Prove a history prerequisite through a one-bit sticky state flag.

    Example: ``MemGrantSeen`` sets ``acked``; ``VoluntaryDone`` is guarded by the
    old value of ``acked``; and accepting a new transaction clears ``acked``.
    This is a generic temporal-state proof, not a Writeback-specific rule.
    """
    pre = _candidate_occurrence(candidate, prerequisite)
    post = _candidate_occurrence(candidate, after)
    if pre is None or post is None:
        return None
    pre_signals = [str(x) for x in pre.get("grounding", {}).get("signals_true", [])]
    post_signals = [str(x) for x in post.get("grounding", {}).get("signals_true", [])]
    if not pre_signals or not post_signals:
        return None
    capture_occurrences = _identity_capture_occurrences(candidate)
    capture_evidence: set[int] = set()
    for occurrence_id in capture_occurrences:
        occurrence = _candidate_occurrence(candidate, occurrence_id)
        if occurrence is not None:
            capture_evidence.update(int(x) for x in occurrence.get("evidence_statement_ids", []))

    for flag in post_signals:
        if flag not in model.state_roots:
            continue
        post_transitions = [
            t for t in model.transitions
            if after in t.labels and t.statement_id is not None
        ]
        if not post_transitions:
            continue
        if not all(flag in t.guard_leaves for t in post_transitions):
            continue

        true_writes: list[dict[str, Any]] = []
        false_writes: list[dict[str, Any]] = []
        unknown_write = False
        for statement in model.statements.values():
            if flag not in statement.get("drives", []):
                continue
            parsed = _statement_rhs(statement)
            if parsed is None:
                continue
            _, rhs = parsed
            value = _literal(rhs)
            if value == 1:
                true_writes.append(statement)
            elif value == 0:
                false_writes.append(statement)
            elif statement.get("kind") not in {"reg", "regreset"}:
                unknown_write = True
        if unknown_write or not true_writes:
            continue
        # Every way to make the sticky bit true must be controlled by at least one
        # signal defining the prerequisite occurrence.
        if not all(any(_control_mentions(model, stmt, signal) for signal in pre_signals) for stmt in true_writes):
            continue
        # A new identity scope must clear the flag, preventing history from leaking
        # across transactions.
        if capture_evidence and not any(int(stmt.get("id", -1)) in capture_evidence for stmt in false_writes):
            continue
        return {
            "flag": flag,
            "true_write_ids": sorted(int(stmt["id"]) for stmt in true_writes),
            "reset_write_ids": sorted(int(stmt["id"]) for stmt in false_writes if int(stmt.get("id", -1)) in capture_evidence),
            "prerequisite_signals": pre_signals,
            "proof": f"{after} is guarded by sticky state {flag}; every write setting {flag}=1 is controlled by {prerequisite}",
        }
    return None

def _history_join(
    model: HandoffControlModel,
    *,
    prerequisites: list[str],
    after: str,
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if model.reset_state is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no reset state for finite-control model"}
    if len(prerequisites) < 2:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "history_join requires at least two prerequisites"}
    for occurrence in [*prerequisites, after]:
        if not model.occurrence_source_states(occurrence):
            return {"status": STRUCTURAL_UNKNOWN, "reason": f"occurrence {occurrence!r} could not be mapped"}

    full_mask = (1 << len(prerequisites)) - 1
    latched: dict[int, dict[str, Any]] = {}
    if candidate is not None:
        for index, occurrence in enumerate(prerequisites):
            proof = _latched_prerequisite_proof(model, candidate, occurrence, after)
            if proof is not None:
                latched[index] = proof
    start = (model.reset_state, 0)
    queue = deque([start])
    parent: dict[tuple[int, int], tuple[tuple[int, int], Transition] | None] = {start: None}
    while queue:
        state, seen_mask = queue.popleft()
        for transition in model.transitions:
            if transition.src != state:
                continue
            labels = transition.labels
            next_mask = seen_mask
            for index, occurrence in enumerate(prerequisites):
                if occurrence in labels:
                    next_mask |= 1 << index
            effective_mask = next_mask
            if after in labels:
                for index in latched:
                    effective_mask |= 1 << index
            if after in labels and effective_mask != full_mask:
                path = [transition]
                cursor = (state, seen_mask)
                while parent[cursor] is not None:
                    previous, edge = parent[cursor]
                    path.append(edge)
                    cursor = previous
                path.reverse()
                missing = [
                    occurrence for index, occurrence in enumerate(prerequisites)
                    if not (effective_mask & (1 << index))
                ]
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": f"{after} reachable without all join prerequisites",
                    "missing_prerequisites": missing,
                    "counterexample": _trace_payload(path),
                }
            if transition.dst == model.reset_state and transition.src != model.reset_state:
                next_mask = 0
            key = (transition.dst, next_mask)
            if key not in parent:
                parent[key] = ((state, seen_mask), transition)
                queue.append(key)
    result = {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": "finite-control over-approximation found no completion before all unordered prerequisites",
    }
    if latched:
        result["latched_prerequisite_proofs"] = {prerequisites[i]: proof for i, proof in latched.items()}
    return result



_ARRAY_LOOKUP_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.$]*)\[(.+)\]$")


def _occurrence_index_signal(occurrence: dict[str, Any]) -> tuple[str, dict[str, int]] | None:
    metadata = occurrence.get("index")
    if not isinstance(metadata, dict):
        return None
    expr = metadata.get("expr")
    domain = metadata.get("domain")
    if not isinstance(expr, dict) or expr.get("op") != "signal" or not isinstance(expr.get("name"), str):
        return None
    if not isinstance(domain, dict) or not isinstance(domain.get("start"), int) or not isinstance(domain.get("end_exclusive"), int):
        return None
    return str(expr["name"]), {"start": int(domain["start"]), "end_exclusive": int(domain["end_exclusive"])}


def _is_increment_rhs(model: HandoffControlModel, rhs: str, counter: str) -> bool:
    nf = _canonical_expr(model, rhs, cut_roots=model.state_roots)
    add_nf = ("call", "add", ("ref", counter), ("lit", 1))
    add_nf_rev = ("call", "add", ("lit", 1), ("ref", counter))
    if nf in {add_nf, add_nf_rev}:
        return True
    if isinstance(nf, tuple) and len(nf) == 4 and nf[0:2] == ("call", "tail"):
        return nf[2] in {add_nf, add_nf_rev}
    return False


def _resolved_rhs(model: HandoffControlModel, rhs: str, seen: set[str] | None = None) -> str:
    text = rhs.strip()
    seen = set() if seen is None else set(seen)
    if any(_under_root(text, root) for root in model.state_roots):
        return text
    if _SIMPLE_REF_RE.fullmatch(text) and text not in seen:
        nested = model.rhs(text)
        if nested is not None:
            return _resolved_rhs(model, nested, seen | {text})
    return text


def _write_records(model: HandoffControlModel, root: str) -> list[tuple[dict[str, Any], str]]:
    out = []
    for statement in model.statements.values():
        if root not in statement.get("drives", []):
            continue
        parsed = _statement_rhs(statement)
        if parsed is None:
            continue
        lhs, rhs = parsed
        if lhs != root:
            continue
        out.append((statement, rhs))
    return out


def _same_control(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return set(a.get("control_reads", [])) == set(b.get("control_reads", []))


def _prove_parallel_index_pipeline(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    before: str,
    after: str,
    index_name: str,
) -> dict[str, Any] | None:
    """Recognize a lossless register pipeline carrying a valid token and its index."""
    before_obj = _candidate_occurrence(candidate, before)
    after_obj = _candidate_occurrence(candidate, after)
    if before_obj is None or after_obj is None:
        return None
    before_index = _occurrence_index_signal(before_obj)
    after_index = _occurrence_index_signal(after_obj)
    if before_index is None or after_index is None:
        return None
    if before_obj.get("index", {}).get("name") != index_name or after_obj.get("index", {}).get("name") != index_name:
        return None
    if before_index[1] != after_index[1]:
        return None
    before_signal = before_index[0]
    after_signal = after_index[0]
    before_evidence = {int(x) for x in before_obj.get("evidence_statement_ids", [])}
    gate_candidates = [
        str(x) for x in after_obj.get("grounding", {}).get("signals_true", [])
        if str(x) in model.state_roots
    ]
    if not gate_candidates:
        return None

    def search(token: str, index_signal: str, depth: int, seen: set[tuple[str, str]]) -> list[dict[str, Any]] | None:
        if depth > 8 or (token, index_signal) in seen:
            return None
        seen = seen | {(token, index_signal)}
        token_writes = _write_records(model, token)
        index_writes = _write_records(model, index_signal)

        # Terminal capture: the semantic 'before' event sets valid=1 and captures
        # its current index under the exact same control condition.
        for token_stmt, token_rhs in token_writes:
            if _literal(_resolved_rhs(model, token_rhs)) != 1 or int(token_stmt.get("id", -1)) not in before_evidence:
                continue
            for index_stmt, index_rhs in index_writes:
                if int(index_stmt.get("id", -1)) not in before_evidence or not _same_control(token_stmt, index_stmt):
                    continue
                if _resolved_rhs(model, index_rhs) == before_signal:
                    return [{
                        "token_write": int(token_stmt["id"]),
                        "index_write": int(index_stmt["id"]),
                        "token": token,
                        "index": index_signal,
                        "source_index": before_signal,
                        "terminal": True,
                    }]

        # Pipeline stage: valid and index registers are copied together under the
        # same control scope.  False/default writes are harmless and ignored.
        for token_stmt, token_rhs in token_writes:
            prev_token = _resolved_rhs(model, token_rhs)
            if prev_token not in model.state_roots:
                continue
            for index_stmt, index_rhs in index_writes:
                prev_index = _resolved_rhs(model, index_rhs)
                if prev_index not in model.state_roots or not _same_control(token_stmt, index_stmt):
                    continue
                suffix = search(prev_token, prev_index, depth + 1, seen)
                if suffix is not None:
                    return [{
                        "token_write": int(token_stmt["id"]),
                        "index_write": int(index_stmt["id"]),
                        "token": token,
                        "index": index_signal,
                        "from_token": prev_token,
                        "from_index": prev_index,
                        "terminal": False,
                    }, *suffix]
        return None

    for gate in gate_candidates:
        chain = search(gate, after_signal, 0, set())
        if chain is None:
            continue
        # Fail closed if any stage's token can be made true by an unaccounted write.
        accounted = {step["token_write"] for step in chain}
        terminal_tokens = {step["token"] for step in chain}
        unsafe = []
        for token in terminal_tokens:
            for statement, rhs in _write_records(model, token):
                value = _literal(_resolved_rhs(model, rhs))
                if value == 0:
                    continue
                if int(statement.get("id", -1)) not in accounted and _resolved_rhs(model, rhs) not in model.state_roots:
                    unsafe.append(int(statement.get("id", -1)))
        if unsafe:
            continue
        return {
            "status": STRUCTURALLY_SUPPORTED,
            "proof": f"{after} carries the same {index_name} through a lossless valid/index register pipeline from {before}",
            "proof_domain": "exact-register-token-index-pipeline",
            "pipeline": chain,
            "domain": before_index[1],
            "bijection": True,
        }
    return None


def _expr_contains_compare(
    model: HandoffControlModel,
    expr: str,
    op: str,
    signal: str,
    value: int,
    seen: set[str] | None = None,
) -> bool:
    text = expr.strip()
    seen = set() if seen is None else set(seen)
    if _SIMPLE_REF_RE.fullmatch(text) and text not in seen:
        rhs = model.rhs(text)
        if rhs is not None:
            return _expr_contains_compare(model, rhs, op, signal, value, seen | {text})
    call = _call(text)
    if call is None:
        return False
    if call[0] == op and len(call[1]) == 2:
        a, b = call[1]
        if ((a.strip() == signal and _literal(b) == value) or
            (b.strip() == signal and _literal(a) == value)):
            return True
    return any(_expr_contains_compare(model, arg, op, signal, value, seen) for arg in call[1])


def _occurrence_upper_bound_signal(model: HandoffControlModel, occurrence: dict[str, Any]) -> list[str]:
    signals = [str(x) for x in occurrence.get("grounding", {}).get("signals_true", [])]
    if occurrence.get("kind") == "boundary":
        physical = occurrence.get("physical_event_ids", [])
        if len(physical) == 1:
            event = model._event_info(physical[0])
            if event is not None:
                gate = event.get("valid") if event.get("direction") != "receive" else event.get("ready")
                if isinstance(gate, str):
                    signals.append(gate)
    return signals


def _transition_cowrite_literal(model: HandoffControlModel, transition: Transition, signal: str, value: int) -> int | None:
    if transition.statement_id is None:
        return None
    transition_stmt = model.statements.get(transition.statement_id)
    if transition_stmt is None:
        return None
    for statement, rhs in _write_records(model, signal):
        if _literal(_resolved_rhs(model, rhs)) != value:
            continue
        if model._source_state(statement) != transition.src:
            continue
        if _same_control(statement, transition_stmt):
            return int(statement["id"])
    return None


def _counter_width(model: HandoffControlModel, counter: str) -> int | None:
    for item in model.handoff.get("state", []):
        if item.get("id") != counter:
            continue
        match = re.fullmatch(r"UInt<(\d+)>", str(item.get("type", "")))
        if match is not None:
            return int(match.group(1))
    return None


def _counter_zero_on_entry(
    model: HandoffControlModel,
    phase_state: int,
    counter: str,
    *,
    wrapped_phase_exit_ids: set[int] | None = None,
) -> dict[str, Any] | None:
    incoming = [t for t in model.transitions if t.statement_id is not None and t.dst == phase_state and t.src != phase_state]
    if not incoming:
        return None

    def prove_state(state: int, seen: set[int]) -> list[dict[str, Any]] | None:
        if state in seen:
            return None
        seen = seen | {state}
        incoming_edges = [t for t in model.transitions if t.statement_id is not None and t.dst == state and t.src != state]
        if state == model.reset_state and not incoming_edges:
            # Reset declarations are enough when the counter itself is reset to zero.
            for statement in model.statements.values():
                if statement.get("kind") != "regreset" or counter not in statement.get("drives", []):
                    continue
                if _literal(statement.get("text", "").split(",")[-1].strip()) == 0:
                    return [{"state": state, "reset_declaration": int(statement["id"])}]
            return None
        proofs = []
        for edge in incoming_edges:
            zero = _transition_cowrite_literal(model, edge, counter, 0)
            if zero is not None:
                proofs.append({"src": edge.src, "dst": edge.dst, "transition": edge.statement_id, "zero_write": zero})
                continue
            # Between an earlier reset and this transition, the source state must not
            # contain any write to the counter; otherwise entry value is unknown.
            writes = [stmt for stmt, _ in _write_records(model, counter) if model._source_state(stmt) == edge.src]
            if writes:
                return None
            prefix = prove_state(edge.src, seen)
            if prefix is None:
                return None
            proofs.extend(prefix)
            proofs.append({"src": edge.src, "dst": edge.dst, "transition": edge.statement_id})
        return proofs

    proof = prove_state(phase_state, set())
    if proof is not None:
        return {"counter": counter, "phase_state": phase_state, "entry_proof": proof}

    # Cyclic FSMs cannot be certified by the recursive path proof above.  Use a
    # graph-cut invariant when (1) every write outside the counted phase is zero,
    # (2) every phase exit is a certified modulo-wrap-to-zero transition, and
    # (3) every reset-to-phase path crosses an exact zero co-write.  This reasons
    # about generic state/counter structure and does not name any RTL phase.
    wrapped = set(wrapped_phase_exit_ids or set())
    writes = _write_records(model, counter)
    outside_zero_writes: list[int] = []
    for statement, rhs in writes:
        if model._source_state(statement) == phase_state:
            continue
        if _literal(_resolved_rhs(model, rhs)) != 0:
            return None
        outside_zero_writes.append(int(statement["id"]))

    transitions = [
        transition for transition in model.transitions
        if transition.statement_id is not None and transition.src != transition.dst
    ]
    phase_exits = [transition for transition in transitions if transition.src == phase_state]
    if not phase_exits or any(int(transition.statement_id) not in wrapped for transition in phase_exits):
        return None

    zero_cut: list[dict[str, int]] = []
    zero_transition_ids: set[int] = set(wrapped)
    for transition in transitions:
        zero_write = _transition_cowrite_literal(model, transition, counter, 0)
        if zero_write is None:
            continue
        zero_transition_ids.add(int(transition.statement_id))
        zero_cut.append({
            "src": transition.src,
            "dst": transition.dst,
            "transition": int(transition.statement_id),
            "zero_write": zero_write,
        })

    if model.reset_state is None:
        return None
    reachable = {int(model.reset_state)}
    pending = deque([int(model.reset_state)])
    while pending:
        state = pending.popleft()
        for transition in transitions:
            if transition.src != state or int(transition.statement_id) in zero_transition_ids:
                continue
            if transition.dst not in reachable:
                reachable.add(transition.dst)
                pending.append(transition.dst)
    if phase_state in reachable:
        return None
    return {
        "counter": counter,
        "phase_state": phase_state,
        "proof_domain": "exact-counter-zeroing-transition-cut",
        "reset_state": int(model.reset_state),
        "zero_cut_transitions": zero_cut,
        "wrapped_phase_exit_transition_ids": sorted(wrapped),
        "outside_phase_zero_write_ids": sorted(outside_zero_writes),
        "reachable_without_zeroing": sorted(reachable),
    }


def _prove_monotone_index_occurrence(
    model: HandoffControlModel,
    occurrence: dict[str, Any],
    domain: dict[str, int],
    *,
    completion: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    metadata = _occurrence_index_signal(occurrence)
    if metadata is None or metadata[1] != domain or domain.get("start") != 0:
        return None
    counter = metadata[0]
    states = {int(x) for x in occurrence.get("grounding", {}).get("state_values", [])}
    if not states:
        states = model.occurrence_source_states(str(occurrence.get("id")))
    if len(states) != 1:
        return None
    phase_state = next(iter(states))
    evidence = {int(x) for x in occurrence.get("evidence_statement_ids", [])}
    increments = []
    for statement, rhs in _write_records(model, counter):
        if model._source_state(statement) != phase_state:
            continue
        resolved = _resolved_rhs(model, rhs)
        if _is_increment_rhs(model, resolved, counter) and int(statement.get("id", -1)) in evidence:
            increments.append(statement)
    if len(increments) != 1:
        return None
    increment = increments[0]

    completion_evidence = {int(x) for x in (completion or {}).get("evidence_statement_ids", [])}
    for statement, rhs in _write_records(model, counter):
        if model._source_state(statement) != phase_state or int(statement["id"]) == int(increment["id"]):
            continue
        value = _literal(_resolved_rhs(model, rhs))
        if value == 0 and int(statement["id"]) in completion_evidence:
            continue
        # A same-phase alternate write could skip/repeat indices.
        return None

    wrapped_exits: set[int] = set()
    if completion is not None:
        last = _completion_is_last_index(model, completion, occurrence, counter, domain)
        width = _counter_width(model, counter)
        increment_controls = {str(item) for item in increment.get("control_reads", [])}
        transition_controls_cover_increment = last is not None and all(
            increment_controls
            <= {
                str(item)
                for item in model.statements.get(int(transition_id), {}).get("control_reads", [])
            }
            for transition_id in last.get("transition_ids", [])
        )
        if (
            last is not None
            and width is not None
            and int(domain["end_exclusive"]) == (1 << width)
            and transition_controls_cover_increment
        ):
            wrapped_exits = {int(item) for item in last.get("transition_ids", [])}
    entry = _counter_zero_on_entry(
        model,
        phase_state,
        counter,
        wrapped_phase_exit_ids=wrapped_exits,
    )
    if entry is None:
        return None
    upper = int(domain["end_exclusive"])
    gate_signals = _occurrence_upper_bound_signal(model, occurrence)
    width = _counter_width(model, counter)
    explicit_bound = any(
        _expr_contains_compare(model, signal, "lt", counter, upper)
        for signal in gate_signals
    )
    implicit_width_bound = width is not None and upper == (1 << width)
    if not explicit_bound and not implicit_width_bound:
        return None
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": f"{occurrence.get('id')} index is a zero-based monotone counter incremented exactly once per occurrence and bounded by {counter} < {upper}",
        "proof_domain": "exact-bounded-monotone-counter",
        "counter": counter,
        "increment_write": int(increment["id"]),
        "entry_zero": entry,
        "upper_bound": {
            "kind": "explicit-guard" if explicit_bound else "exact-register-width",
            "counter_width": width,
            "end_exclusive": upper,
        },
        "domain": domain,
    }


def _completion_is_last_index(
    model: HandoffControlModel,
    completion: dict[str, Any],
    occurrence: dict[str, Any],
    index_signal: str,
    domain: dict[str, int],
) -> dict[str, Any] | None:
    last = int(domain["end_exclusive"]) - 1
    transitions = [t for t in model.transitions if completion.get("id") in t.labels and t.statement_id is not None]
    if not transitions:
        return None
    for transition in transitions:
        statement = model.statements.get(int(transition.statement_id))
        if statement is None or not _control_has_eq(model, statement, index_signal, last):
            return None
        # Completion must coincide with the indexed occurrence.  For derived
        # occurrences use a stateful true gate; for boundary events use ready/valid.
        required = [str(x) for x in occurrence.get("grounding", {}).get("signals_true", [])]
        if occurrence.get("kind") == "boundary":
            physical = occurrence.get("physical_event_ids", [])
            if len(physical) == 1:
                event = model._event_info(physical[0])
                if event is not None:
                    for key in ("valid", "ready"):
                        if isinstance(event.get(key), str):
                            required.append(event[key])
        meaningful = [sig for sig in required if sig != index_signal]
        if meaningful and not any(_control_mentions(model, statement, sig) for sig in meaningful):
            return None
    return {
        "completion": completion.get("id"),
        "last_index": last,
        "transition_ids": sorted(int(t.statement_id) for t in transitions if t.statement_id is not None),
    }


def _index_expr_equivalent(model: HandoffControlModel, actual: str, expected: str, domain: dict[str, int]) -> bool:
    actual_nf = _canonical_expr(model, actual, cut_roots=model.state_roots)
    expected_nf = _canonical_expr(model, expected, cut_roots=model.state_roots)
    if actual_nf == expected_nf:
        return True
    call = _call(_resolved_rhs(model, actual))
    if call is not None and call[0] == "bits" and len(call[1]) == 3:
        hi = _literal(call[1][1]); lo = _literal(call[1][2])
        if hi is not None and lo == 0 and _canonical_expr(model, call[1][0], cut_roots=model.state_roots) == expected_nf:
            return int(domain["start"]) >= 0 and int(domain["end_exclusive"]) <= (1 << (hi + 1))
    return False


def _expr_is_indexed_storage(
    model: HandoffControlModel,
    expr: str,
    storage: str,
    expected_index: str,
    domain: dict[str, int],
    seen: set[str] | None = None,
) -> bool:
    text = expr.strip()
    seen = set() if seen is None else set(seen)
    match = _ARRAY_LOOKUP_RE.match(text)
    if match is not None and match.group(1) == storage:
        return _index_expr_equivalent(model, match.group(2), expected_index, domain)
    if _SIMPLE_REF_RE.fullmatch(text) and text not in seen:
        rhs = model.rhs(text)
        if rhs is None:
            return False
        return _expr_is_indexed_storage(model, rhs, storage, expected_index, domain, seen | {text})
    call = _call(text)
    if call is not None and call[0] == "mux" and len(call[1]) == 3:
        return (_expr_is_indexed_storage(model, call[1][1], storage, expected_index, domain, seen) and
                _expr_is_indexed_storage(model, call[1][2], storage, expected_index, domain, seen))
    return False


def _same_index_signal_alias(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    on: str,
    target: str,
    source: str,
    scope_index: dict[str, str],
) -> dict[str, Any]:
    occurrence = _candidate_occurrence(candidate, on)
    if occurrence is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"occurrence {on!r} missing"}
    metadata = _occurrence_index_signal(occurrence)
    if metadata is None or occurrence.get("index", {}).get("name") != scope_index.get("name"):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "indexed occurrence metadata does not match scope_index"}
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_.$]*)\[([A-Za-z_][A-Za-z0-9_$]*)\]$", source)
    if match is None or match.group(2) != scope_index.get("name"):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "source is not a lookup by the bound index"}
    rhs = model.rhs(target)
    if rhs is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"no driver for {target!r}"}
    if not _expr_is_indexed_storage(model, rhs, match.group(1), metadata[0], metadata[1]):
        return {"status": COUNTEREXAMPLE, "reason": f"{target} is not an exact pointwise lookup of {source}"}
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": f"every combinational branch driving {target} reads {match.group(1)} at the same bounded {scope_index.get('name')} index",
        "proof_domain": "exact-symbolic-same-index-lookup",
    }


def _same_index_history_order(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    before: str,
    after: str,
    scope_index: dict[str, str],
    required_prior: str | None = None,
) -> dict[str, Any]:
    if required_prior is not None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "same-index required_prior is not yet supported"}
    if scope_index.get("relation") != "same" or not isinstance(scope_index.get("name"), str):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported scope_index relation"}
    proof = _prove_parallel_index_pipeline(model, candidate, before, after, str(scope_index["name"]))
    if proof is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no exact lossless valid/index register pipeline was found"}
    return proof

def _indexed_coverage(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    occurrence: str,
    completion: str,
    index: str,
    domain: dict[str, int],
    cardinality: str,
) -> dict[str, Any]:
    occurrence_obj = _candidate_occurrence(candidate, occurrence)
    completion_obj = _candidate_occurrence(candidate, completion)
    if occurrence_obj is None or completion_obj is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "indexed occurrence or completion is missing"}
    metadata = occurrence_obj.get("index")
    if not isinstance(metadata, dict):
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"occurrence {occurrence!r} has no index metadata"}
    if metadata.get("name") != index or metadata.get("domain") != domain:
        return {
            "status": COUNTEREXAMPLE,
            "reason": "indexed axiom domain/index disagrees with occurrence declaration",
            "occurrence_index": metadata,
            "axiom_index": {"name": index, "domain": domain},
        }
    if cardinality != "exactly_once":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "only exactly_once indexed coverage is defined"}
    if not model.occurrence_source_states(completion):
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"completion {completion!r} could not be mapped to control"}

    # Direct form: the occurrence itself is indexed by a bounded monotone counter
    # that starts at zero on phase entry, increments once per occurrence, and the
    # completion transition is guarded by the final index.
    direct = _prove_monotone_index_occurrence(model, occurrence_obj, domain, completion=completion_obj)
    occurrence_meta = _occurrence_index_signal(occurrence_obj)
    if direct is not None and occurrence_meta is not None:
        last = _completion_is_last_index(model, completion_obj, occurrence_obj, occurrence_meta[0], domain)
        if last is not None:
            return {
                "status": STRUCTURALLY_SUPPORTED,
                "proof": f"{occurrence} covers every {index} exactly once before {completion}",
                "proof_domain": "exact-bounded-indexed-occurrence",
                "counter_proof": direct,
                "completion_proof": last,
            }

    # Pipelined form: the indexed occurrence is a lossless valid/index pipeline
    # image of an earlier occurrence.  Prove the source index is monotone and that
    # the completion coincides with the final pipelined index.
    for axiom in candidate.get("axioms", []):
        formal = axiom.get("formal", {})
        scope_index = formal.get("scope_index")
        if (formal.get("type") != "ordered_before" or formal.get("after") != occurrence or
                not isinstance(scope_index, dict) or scope_index.get("name") != index or
                scope_index.get("relation") != "same"):
            continue
        source_id = formal.get("before")
        if not isinstance(source_id, str):
            continue
        pipeline = _prove_parallel_index_pipeline(model, candidate, source_id, occurrence, index)
        source_obj = _candidate_occurrence(candidate, source_id)
        if pipeline is None or source_obj is None:
            continue
        source_counter = _prove_monotone_index_occurrence(model, source_obj, domain, completion=completion_obj)
        after_meta = _occurrence_index_signal(occurrence_obj)
        if source_counter is None or after_meta is None:
            continue
        last = _completion_is_last_index(model, completion_obj, occurrence_obj, after_meta[0], domain)
        if last is None:
            continue
        return {
            "status": STRUCTURALLY_SUPPORTED,
            "proof": f"{occurrence} is a lossless same-index pipeline of {source_id}; the source counter visits every index once before final completion",
            "proof_domain": "exact-bounded-indexed-pipeline",
            "pipeline_proof": pipeline,
            "source_counter_proof": source_counter,
            "completion_proof": last,
        }

    return {
        "status": PARTIALLY_SUPPORTED,
        "proof": (
            f"indexed occurrence {occurrence} declares {index} over "
            f"[{domain['start']}, {domain['end_exclusive']}); completion {completion} is grounded"
        ),
        "reason": (
            "no exact bounded monotone-counter or lossless valid/index pipeline certificate was recovered"
        ),
    }


def _transaction_exclusion(
    model: HandoffControlModel,
    *,
    left: str,
    rights: list[str],
) -> dict[str, Any]:
    if model.reset_state is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "no reset state for finite-control model"}
    if not model.occurrence_source_states(left):
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"occurrence {left!r} could not be mapped"}
    if any(not model.occurrence_source_states(right) for right in rights):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "one or more excluded occurrences could not be mapped"}

    start = (model.reset_state, False, False)
    queue = deque([start])
    parent: dict[tuple[int, bool, bool], tuple[tuple[int, bool, bool], Transition] | None] = {start: None}
    while queue:
        state, seen_left, seen_right = queue.popleft()
        for transition in model.transitions:
            if transition.src != state:
                continue
            labels = transition.labels
            next_left = seen_left or left in labels
            next_right = seen_right or any(right in labels for right in rights)
            if next_left and next_right:
                path = [transition]
                cursor = (state, seen_left, seen_right)
                while parent[cursor] is not None:
                    previous, edge = parent[cursor]
                    path.append(edge)
                    cursor = previous
                path.reverse()
                return {
                    "status": COUNTEREXAMPLE,
                    "reason": f"transaction can contain both {left} and one of {rights}",
                    "counterexample": _trace_payload(path),
                }
            if transition.dst == model.reset_state and transition.src != model.reset_state:
                next_left = next_right = False
            key = (transition.dst, next_left, next_right)
            if key not in parent:
                parent[key] = ((state, seen_left, seen_right), transition)
                queue.append(key)
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": "finite-control over-approximation keeps excluded occurrences on disjoint transaction paths",
    }


def _forbid_when(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    occurrence: str,
    predicate: str,
) -> dict[str, Any]:
    predicate_obj = next((p for p in candidate.get("predicates", []) if p.get("id") == predicate), None)
    if predicate_obj is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"predicate {predicate!r} not found"}
    predicate_states = model.predicate_states(predicate_obj)
    occurrence_states = model.occurrence_source_states(occurrence)
    if predicate_states is None or not occurrence_states:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "predicate or occurrence control states could not be resolved"}
    bad = sorted(predicate_states & occurrence_states)
    if bad:
        return {
            "status": COUNTEREXAMPLE,
            "reason": f"{occurrence} is possible while {predicate} holds",
            "counterexample_states": bad,
        }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": f"occurrence source states {sorted(occurrence_states)} are disjoint from predicate states {sorted(predicate_states)}",
    }


def _identity_carrier(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    identity_key: str,
    accepted_by: str,
    dependent_signals: list[str],
) -> dict[str, Any]:
    identity = next((item for item in candidate.get("identity_keys", []) if item.get("id") == identity_key), None)
    occurrence = next((item for item in candidate.get("occurrences", []) if item.get("id") == accepted_by), None)
    if identity is None or occurrence is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "identity or accepting occurrence not found"}
    carrier = identity.get("carrier_state")
    writes = model.write_statements(carrier)
    if not writes:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"no writes to carrier {carrier!r} found"}

    # Compare exact same-cycle Boolean conditions.  This recognizes lowered
    # aliases such as ``when and(io.req.ready, io.req.valid)`` without trusting
    # candidate-authored state annotations or protocol-specific signal names.
    from .formal_patterns import (
        _and,
        _bool_refs,
        _exact_boundary_or_derived_occurrence_condition,
        _not,
        _unsat,
        _writer_activation,
    )

    bool_refs = _bool_refs(model, candidate)
    accepted_condition = _exact_boundary_or_derived_occurrence_condition(
        model,
        candidate,
        accepted_by,
        bool_refs,
    )
    if accepted_condition is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "accepting occurrence has no exact Boolean condition"}
    for statement in writes:
        activation_info = _writer_activation(model, str(carrier), statement, bool_refs)
        if activation_info is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"carrier {carrier!r} writer activation is not exact",
                "statement_id": statement.get("id"),
            }
        activation, activation_certificate = activation_info
        outside_accept, atom_count = _unsat(_and(activation, _not(accepted_condition)))
        if outside_accept is not True:
            return {
                "status": COUNTEREXAMPLE,
                "reason": f"carrier {carrier!r} has a write not guarded by {accepted_by}",
                "statement_id": statement.get("id"),
                "atom_count": atom_count,
                "activation": activation_certificate,
            }

    missing = [
        signal for signal in dependent_signals if not model.backward_depends_on(signal, carrier)
    ]
    if missing:
        return {
            "status": COUNTEREXAMPLE,
            "reason": "identity-bearing outputs missing dependency on latched carrier",
            "signals": missing,
        }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"all writes to carrier {carrier!r} are guarded by {accepted_by}; "
            f"{len(dependent_signals)} listed identity-bearing outputs depend on the carrier"
        ),
        "limitation": "dependency proves functional grounding, not full bit-level equality for transformed fields",
    }


def _signal_alias(model: HandoffControlModel, *, target: str, source: str) -> dict[str, Any]:
    rhs = model.rhs(target)
    if rhs is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"no driver for {target!r}"}
    if rhs == source:
        return {"status": STRUCTURALLY_SUPPORTED, "proof": f"{target} is directly connected to {source}"}
    # Permit a one-hop aggregate/alias chain if both sides are exact symbolic refs.
    if _SIMPLE_REF_RE.fullmatch(rhs) and model.rhs(rhs) == source:
        return {"status": STRUCTURALLY_SUPPORTED, "proof": f"{target} aliases {source} through {rhs}"}
    if model.backward_depends_on(target, source):
        return {
            "status": PARTIALLY_SUPPORTED,
            "proof": f"{target} structurally depends on {source}",
            "reason": "dependency is not enough to prove equality",
        }
    return {"status": COUNTEREXAMPLE, "reason": f"{target} does not derive from {source}"}


def _constant_bit(model: HandoffControlModel, *, signal: str, bit: int, expected: int) -> dict[str, Any]:
    values = model.possible_signal_values(signal)
    if values is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"could not constant-propagate {signal}"}
    observed = {(value >> bit) & 1 for value in values}
    if observed == {expected}:
        return {"status": STRUCTURALLY_SUPPORTED, "proof": f"bit {bit} of {signal} is statically {expected}"}
    return {
        "status": COUNTEREXAMPLE,
        "reason": f"bit {bit} of {signal} can be {sorted(observed)}, expected only {expected}",
    }



def _under_root(signal: str, root: str) -> bool:
    return (
        signal == root
        or signal.startswith(root + ".")
        or signal.startswith(root + "[")
    )


def _canonical_expr(
    model: HandoffControlModel,
    expr: str,
    *,
    cut_roots: set[str] | None = None,
    seen: set[str] | None = None,
) -> tuple[Any, ...] | None:
    """Return an exact symbolic DAG normal form after alias/node expansion.

    Register roots listed in ``cut_roots`` are treated as symbolic state leaves.
    This is important for temporal identity proofs: ``req.address`` denotes the
    latched request field and must not be inlined back to the *current* input
    ``io.req.bits.address`` through its register write.
    """

    text = expr.strip()
    cut_roots = cut_roots or set()
    cut_key = tuple(sorted(str(root) for root in cut_roots))
    cache = getattr(model, "_canonical_expr_cache", None)
    if not isinstance(cache, dict):
        cache = {}
        setattr(model, "_canonical_expr_cache", cache)
    cache_key = (text, cut_key)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    cut_cache = getattr(model, "_canonical_cut_cache", None)
    if not isinstance(cut_cache, dict):
        cut_cache = {}
        setattr(model, "_canonical_cut_cache", cut_cache)
    under_cut = cut_cache.get(cache_key)
    if under_cut is None:
        under_cut = any(_under_root(text, root) for root in cut_key)
        cut_cache[cache_key] = under_cut
    if under_cut:
        result = ("ref", text)
        cache[cache_key] = result
        return result

    value = _literal(text)
    if value is not None:
        result = ("lit", value)
        cache[cache_key] = result
        return result
    if seen is None:
        seen = set()
    if _SIMPLE_REF_RE.fullmatch(text):
        if text in seen:
            return None
        rhs = model.rhs(text)
        if rhs is None:
            result = ("ref", text)
        else:
            result = _canonical_expr(model, rhs, cut_roots=cut_roots, seen=seen | {text})
        # Do not cache cycle-dependent failures.  Successful normalization is
        # path independent and safely shares large FIRRTL expression DAGs.
        if result is not None:
            cache[cache_key] = result
        return result
    call = _call(text)
    if call is None:
        return None
    name, args = call
    normalized: list[tuple[Any, ...]] = []
    for arg in args:
        item = _canonical_expr(model, arg, cut_roots=cut_roots, seen=seen)
        if item is None:
            return None
        normalized.append(item)
    result = ("call", name, *normalized)
    cache[cache_key] = result
    return result


def _identity_projection(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    identity_key: str,
    accepted_by: str,
    capture_source: str,
    projections: list[dict[str, str]],
) -> dict[str, Any]:
    """Check exact symbolic preservation of a latched transaction identity.

    This is stronger than generic dependency checking.  It requires (1) every
    write to the carrier to occur only on the accepting occurrence, (2) the
    carrier capture itself to be an exact aggregate assignment from
    ``capture_source``, and (3) every listed output projection to reduce exactly
    to the declared expression over the latched carrier.
    """

    identity = next((item for item in candidate.get("identity_keys", []) if item.get("id") == identity_key), None)
    if identity is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"identity {identity_key!r} not found"}
    carrier = str(identity.get("carrier_state", ""))
    if not carrier:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "identity carrier is missing"}

    base = _identity_carrier(
        model,
        candidate,
        identity_key=identity_key,
        accepted_by=accepted_by,
        dependent_signals=[str(item.get("target", "")) for item in projections],
    )
    if base.get("status") != STRUCTURALLY_SUPPORTED:
        return base

    writes = model.write_statements(carrier)
    exact_capture_ids: list[int] = []
    for statement in writes:
        text = statement.get("text", "")
        connect = _CONNECT_RE.match(text) or _ASSIGN_RE.match(text)
        if connect is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": f"carrier write {statement.get('id')} is not an exact assignment",
            }
        lhs, rhs = (part.strip() for part in connect.groups())
        exact_aggregate = lhs == carrier and rhs == capture_source
        exact_leaf = lhs.startswith(carrier + ".") and rhs == capture_source + lhs[len(carrier):]
        if not (exact_aggregate or exact_leaf):
            return {
                "status": COUNTEREXAMPLE,
                "reason": f"carrier {carrier!r} is not always captured exactly from {capture_source!r}",
                "statement_id": statement.get("id"),
                "statement": text,
            }
        exact_capture_ids.append(int(statement.get("id")))

    mismatches: list[dict[str, Any]] = []
    proofs: list[dict[str, Any]] = []
    for projection in projections:
        target = str(projection.get("target", ""))
        expected = str(projection.get("source", ""))
        if not target or not expected:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "identity projection target/source is missing"}
        actual_nf = _canonical_expr(model, target, cut_roots={carrier})
        expected_nf = _canonical_expr(model, expected, cut_roots={carrier})
        if actual_nf is None or expected_nf is None:
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "a projection expression could not be normalized exactly",
                "target": target,
                "expected": expected,
            }
        if actual_nf != expected_nf:
            mismatches.append(
                {
                    "target": target,
                    "expected": expected,
                    "actual_normal_form": repr(actual_nf),
                    "expected_normal_form": repr(expected_nf),
                }
            )
        else:
            proofs.append({"target": target, "source": expected, "normal_form": repr(actual_nf)})

    if mismatches:
        return {
            "status": COUNTEREXAMPLE,
            "reason": "one or more identity projections are not exact symbolic functions of the latched carrier",
            "mismatches": mismatches,
        }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"carrier {carrier!r} is captured exactly from {capture_source!r} only on {accepted_by}; "
            f"all {len(projections)} declared projections are exact symbolic functions of the latched carrier"
        ),
        "capture_statement_ids": exact_capture_ids,
        "projection_proofs": proofs,
        "proof_domain": "exact-symbolic-transaction-identity",
    }


_TYPED_UINT_RE = re.compile(
    r'UInt(?:<(\d+)>)?\((?:0h([0-9a-fA-F]+)|"h([0-9a-fA-F]+)"|(\d+))\)'
)


def _typed_literal(expr: str) -> tuple[int, int] | None:
    text = expr.strip()
    if text.isdigit():
        value = int(text)
        return value, max(1, value.bit_length())
    match = _TYPED_UINT_RE.fullmatch(text)
    if match is None:
        return None
    width = int(match.group(1)) if match.group(1) else None
    if match.group(2) is not None:
        value = int(match.group(2), 16)
    elif match.group(3) is not None:
        value = int(match.group(3), 16)
    else:
        value = int(match.group(4))
    return value, width or max(1, value.bit_length())


def _eval_typed_expr(
    model: HandoffControlModel,
    expr: str,
    env: dict[str, tuple[int, int]],
    seen: set[str] | None = None,
) -> tuple[int, int] | None:
    """Evaluate the small FIRRTL expression subset used by ClientMetadata.onProbe."""

    text = expr.strip()
    if text in env:
        return env[text]
    literal = _typed_literal(text)
    if literal is not None:
        return literal
    if seen is None:
        seen = set()
    if _SIMPLE_REF_RE.fullmatch(text):
        if text in seen:
            return None
        rhs = model.rhs(text)
        if rhs is None:
            return None
        return _eval_typed_expr(model, rhs, env, seen | {text})
    call = _call(text)
    if call is None:
        return None
    name, args = call
    if name == "mux" and len(args) == 3:
        select = _eval_typed_expr(model, args[0], env, seen)
        if select is None:
            return None
        return _eval_typed_expr(model, args[1] if select[0] else args[2], env, seen)
    if name in {"eq", "neq"} and len(args) == 2:
        left = _eval_typed_expr(model, args[0], env, seen)
        right = _eval_typed_expr(model, args[1], env, seen)
        if left is None or right is None:
            return None
        value = int(left[0] == right[0])
        if name == "neq":
            value = 1 - value
        return value, 1
    if name == "cat" and len(args) == 2:
        high = _eval_typed_expr(model, args[0], env, seen)
        low = _eval_typed_expr(model, args[1], env, seen)
        if high is None or low is None:
            return None
        return ((high[0] << low[1]) | low[0], high[1] + low[1])
    if name == "bits" and len(args) == 3:
        value = _eval_typed_expr(model, args[0], env, seen)
        hi = _literal(args[1])
        lo = _literal(args[2])
        if value is None or hi is None or lo is None:
            return None
        width = hi - lo + 1
        return ((value[0] >> lo) & ((1 << width) - 1), width)
    if name == "shr" and len(args) == 2:
        value = _eval_typed_expr(model, args[0], env, seen)
        shift = _literal(args[1])
        if value is None or shift is None:
            return None
        return value[0] >> shift, max(1, value[1] - shift)
    if name == "not" and len(args) == 1:
        value = _eval_typed_expr(model, args[0], env, seen)
        if value is None:
            return None
        mask = (1 << value[1]) - 1
        return (~value[0]) & mask, value[1]
    if name in {"and", "or"} and len(args) == 2:
        left = _eval_typed_expr(model, args[0], env, seen)
        right = _eval_typed_expr(model, args[1], env, seen)
        if left is None or right is None:
            return None
        width = max(left[1], right[1])
        value = left[0] & right[0] if name == "and" else left[0] | right[0]
        return value, width
    return None


# Independent finite reference table for the legal TileLink Probe cap values.
# Numeric encodings follow TLPermissions / ClientStates; the semantic mapping is
# ClientMetadata.onProbe (shrinkHelper).  This table is deliberately separate
# from the FIRRTL expression evaluator so equivalence is a genuine reference
# check rather than re-reading the implementation's mux choices as expectations.
_TILELINK_ON_PROBE_REFERENCE: dict[tuple[int, int], tuple[int, int, int]] = {
    # (cap, current_state): (has_dirty_data, report_param, next_state)
    (0, 3): (1, 3, 2),  # toT, Dirty -> TtoT, Trunk
    (0, 2): (0, 3, 2),  # toT, Trunk -> TtoT, Trunk
    (0, 1): (0, 4, 1),  # toT, Branch -> BtoB, Branch
    (0, 0): (0, 5, 0),  # toT, Nothing -> NtoN, Nothing
    (1, 3): (1, 0, 1),  # toB, Dirty -> TtoB, Branch
    (1, 2): (0, 0, 1),  # toB, Trunk -> TtoB, Branch
    (1, 1): (0, 4, 1),  # toB, Branch -> BtoB, Branch
    (1, 0): (0, 5, 0),  # toB, Nothing -> NtoN, Nothing
    (2, 3): (1, 1, 0),  # toN, Dirty -> TtoN, Nothing
    (2, 2): (0, 1, 0),  # toN, Trunk -> TtoN, Nothing
    (2, 1): (0, 2, 0),  # toN, Branch -> BtoN, Nothing
    (2, 0): (0, 5, 0),  # toN, Nothing -> NtoN, Nothing
}


def _tilelink_on_probe_spec(
    model: HandoffControlModel,
    *,
    param_signal: str,
    current_state_signal: str,
    dirty_signal: str,
    report_signal: str,
    next_state_signal: str,
) -> dict[str, Any]:
    mismatches: list[dict[str, Any]] = []
    checked: list[dict[str, Any]] = []
    for (param, state), expected in sorted(_TILELINK_ON_PROBE_REFERENCE.items()):
        env = {
            param_signal: (param, 2),
            current_state_signal: (state, 2),
        }
        values = []
        for signal in (dirty_signal, report_signal, next_state_signal):
            result = _eval_typed_expr(model, signal, env)
            if result is None:
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": "TileLink onProbe expression could not be evaluated exactly",
                    "signal": signal,
                    "param": param,
                    "state": state,
                }
            values.append(result[0])
        actual = tuple(values)
        row = {"param": param, "state": state, "expected": list(expected), "actual": list(actual)}
        checked.append(row)
        if actual != expected:
            mismatches.append(row)
    if mismatches:
        return {
            "status": COUNTEREXAMPLE,
            "reason": "FIRRTL ClientMetadata.onProbe behavior differs from the trusted TileLink reference table",
            "mismatches": mismatches,
        }
    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": "all 12 legal Probe cap/current-state combinations match the TileLink ClientMetadata.onProbe reference table",
        "checked_rows": checked,
        "reference": "TileLink TLPermissions + ClientMetadata.onProbe/shrinkHelper",
        "proof_domain": "finite-reference-equivalence",
    }

def _validation_level(structural_status: str, formal_status: str) -> str:
    if formal_status == "FORMAL_COUNTEREXAMPLE":
        return REFUTED
    if formal_status == SPEC_PROVED:
        return SPEC_PROVED
    if formal_status == FORMALLY_PROVED:
        return FORMALLY_PROVED
    if structural_status == COUNTEREXAMPLE:
        return REFUTED
    if structural_status == STRUCTURALLY_SUPPORTED:
        return STRUCTURALLY_SUPPORTED
    if structural_status == PARTIALLY_SUPPORTED:
        return PARTIALLY_SUPPORTED
    return GROUNDED


def _run_structural_checker(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    obligation: dict[str, Any],
) -> dict[str, Any]:
    checker = obligation.get("checker")
    args = obligation.get("arguments", {})
    if args.get("scope_index"):
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": (
                "same-index relation is formally represented but requires an index-aware backend; "
                "scalar structural checkers intentionally do not erase the index scope"
            ),
            "scope_index": args.get("scope_index"),
        }
    try:
        if checker == "forbid_when":
            return _forbid_when(model, candidate, **args)
        if checker == "history_order":
            return _history_order(model, **args)
        if checker == "history_chain":
            return _history_chain(model, **args)
        if checker == "history_join":
            return _history_join(model, candidate=candidate, **args)
        if checker == "indexed_coverage":
            return _indexed_coverage(model, candidate, **args)
        if checker == "occurrence_partition":
            from .formal_patterns import prove_same_cycle_occurrence_partition

            return prove_same_cycle_occurrence_partition(model, candidate, **args)
        if checker == "indexed_storage_flow":
            from .storage_prover import prove_indexed_storage_flow

            return prove_indexed_storage_flow(model, candidate, **args)
        if checker == "indexed_priority_select":
            from .priority_select_prover import prove_indexed_priority_select

            return prove_indexed_priority_select(model, candidate, **args)
        if checker == "register_transition":
            from .register_transition_prover import prove_register_transition

            return prove_register_transition(model, candidate, **args)
        if checker == "transaction_exclusion":
            return _transaction_exclusion(model, **args)
        if checker == "identity_carrier":
            return _identity_carrier(model, candidate, **args)
        if checker == "identity_projection":
            return _identity_projection(model, candidate, **args)
        if checker == "tilelink_on_probe_spec":
            return _tilelink_on_probe_spec(model, **args)
        if checker == "signal_alias":
            if args.get("on"):
                from .formal_patterns import prove_conditional_signal_equality

                return prove_conditional_signal_equality(model, candidate, **args)
            return _signal_alias(model, **args)
        if checker == "constant_bit":
            if args.get("on"):
                from .formal_patterns import prove_conditional_constant_bit

                return prove_conditional_constant_bit(model, candidate, **args)
            return _constant_bit(model, **args)
        if checker == "external_formal":
            return {
                "status": STRUCTURAL_UNKNOWN,
                "reason": "obligation is intentionally delegated to a bit-level formal backend",
            }
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"unsupported checker {checker!r}"}
    except (KeyError, TypeError, ValueError) as exc:
        return {"status": STRUCTURAL_UNKNOWN, "reason": f"checker arguments invalid: {exc}"}


def _certified_parent_provenance(result: dict[str, Any]) -> dict[str, Any]:
    from .composition_prover import derive_composition_provenance, frozen_theorem_dependencies

    formal = result.get("formal", {})
    if not isinstance(formal, dict) or formal.get("status") not in {FORMALLY_PROVED, SPEC_PROVED}:
        raise ValueError(f"axiom {result.get('axiom_id')!r} has no trusted formal result")
    if formal.get("backend") == "composition-prover":
        derived = derive_composition_provenance(formal)
        recorded = formal.get("provenance")
        if recorded != derived:
            raise ValueError(
                f"axiom {result.get('axiom_id')!r} composition provenance does not match its certificate"
            )
        return derived

    unexpected = frozen_theorem_dependencies(formal.get("certificate", {}))
    if unexpected:
        raise ValueError(
            f"axiom {result.get('axiom_id')!r} consumed frozen theorems outside the composition prover: {unexpected}"
        )
    return {
        "kind": "parent_local",
        "source_axioms": [],
        "proof_method": str(formal.get("proof_method", "")),
        "derivation": "formal-certificate-v0.1",
    }


def _trusted_parent_provenance(
    candidate: dict[str, Any],
    results: list[dict[str, Any]],
    trusted_ids: set[str],
) -> dict[str, dict[str, Any]] | None:
    extensions = candidate.get("extensions")
    if not isinstance(extensions, dict) or "parent_synthesis" not in extensions:
        return None
    parent = extensions.get("parent_synthesis")
    declared = parent.get("axiom_provenance") if isinstance(parent, dict) else None
    if not isinstance(declared, dict):
        raise ValueError("parent candidate has no axiom_provenance declaration")
    by_id = {str(result.get("axiom_id")): result for result in results}
    certified: dict[str, dict[str, Any]] = {}
    for axiom_id in sorted(trusted_ids):
        result = by_id.get(axiom_id)
        if result is None:
            raise ValueError(f"trusted parent axiom {axiom_id!r} has no validation result")
        actual = _certified_parent_provenance(result)
        claim = declared.get(axiom_id)
        if not isinstance(claim, dict):
            raise ValueError(f"trusted parent axiom {axiom_id!r} has no declared provenance")
        claimed_sources = claim.get("source_axioms", [])
        if not isinstance(claimed_sources, list) or not all(
            isinstance(item, str) for item in claimed_sources
        ) or len(claimed_sources) != len(set(claimed_sources)):
            raise ValueError(f"parent provenance mismatch for {axiom_id!r}: invalid source_axioms list")
        normalized_sources = sorted(claimed_sources)
        if claim.get("kind") != actual["kind"] or normalized_sources != actual["source_axioms"]:
            raise ValueError(
                f"parent provenance mismatch for {axiom_id!r}: declared "
                f"kind={claim.get('kind')!r}, source_axioms={normalized_sources!r}; "
                f"certificate requires kind={actual['kind']!r}, "
                f"source_axioms={actual['source_axioms']!r}"
            )
        certified[axiom_id] = actual
    return certified


def _declared_public_interface(candidate: dict[str, Any]) -> dict[str, Any] | None:
    extensions = candidate.get("extensions")
    parent = extensions.get("parent_synthesis") if isinstance(extensions, dict) else None
    interface = parent.get("public_interface") if isinstance(parent, dict) else None
    return deepcopy(interface) if isinstance(interface, dict) else None


def _build_trusted_umcm(candidate: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    trusted_ids = {
        result["axiom_id"]
        for result in results
        if result.get("validation_level") in {FORMALLY_PROVED, SPEC_PROVED}
    }
    trusted_axioms = [
        axiom for axiom in candidate.get("axioms", []) if axiom.get("id") in trusted_ids
    ]

    public_interface = _declared_public_interface(candidate)
    if public_interface is None:
        # A leaf has no separate public/private contract: every grounded
        # semantic declaration is part of the compositional interface, even
        # when it is only an observation point and no axiom mentions it yet.
        # Dropping such declarations here makes owned boundary events and
        # useful CEGAR handles silently disappear at freeze time.
        occurrence_ids = {
            str(item["id"])
            for item in candidate.get("occurrences", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        predicate_ids = {
            str(item["id"])
            for item in candidate.get("predicates", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        identity_ids = {
            str(item["id"])
            for item in candidate.get("identity_keys", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    else:
        # Parent summaries have an explicit public contract.  Preserve only
        # the declared exports plus the dependency closure of trusted axioms.
        occurrence_ids = {
            str(item) for item in public_interface.get("exported_occurrence_ids", [])
        }
        predicate_ids = {
            str(item) for item in public_interface.get("exported_predicate_ids", [])
        }
        identity_ids = {
            str(item) for item in public_interface.get("exported_identity_ids", [])
        }
    case_ids: set[str] = set()
    rendered_axioms = []
    for axiom in trusted_axioms:
        compiled = compile_formal_axiom(axiom["formal"])
        refs = compiled["references"]
        occurrence_ids.update(refs.get("occurrences", []))
        predicate_ids.update(refs.get("predicates", []))
        identity_ids.update(refs.get("identities", []))
        case_ids.update(axiom.get("derived_from_case_ids", []))
        rendered_axioms.append({**axiom, "rendered_formula": render_formal_axiom(axiom["formal"])})

    # Cases are part of the trusted semantic interface too. Pull in the
    # occurrence/predicate closure they reference so the trusted summary never
    # contains dangling case guards or emitted occurrences.
    selected_cases = [x for x in candidate.get("cases", []) if x.get("id") in case_ids]
    for case in selected_cases:
        occurrence_ids.update(case.get("trigger_occurrences", []))
        occurrence_ids.update(case.get("emits", []))
        for guard in case.get("guard_predicates", []):
            if isinstance(guard, dict) and guard.get("id"):
                predicate_ids.add(guard["id"])

    trusted = {
        "schema_version": candidate.get("schema_version"),
        "task_id": candidate.get("task_id"),
        "work_unit_id": candidate.get("work_unit_id"),
        "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
        "trusted_axiom_ids": sorted(trusted_ids),
        "occurrences": [x for x in candidate.get("occurrences", []) if x.get("id") in occurrence_ids],
        "predicates": [x for x in candidate.get("predicates", []) if x.get("id") in predicate_ids],
        "identity_keys": [x for x in candidate.get("identity_keys", []) if x.get("id") in identity_ids],
        "cases": selected_cases,
        "axioms": rendered_axioms,
        "assumptions": candidate.get("assumptions", []),
        "note": (
            "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. "
            "Grounded/structurally-supported candidate axioms remain outside the trusted abstraction."
        ),
    }
    provenance = _trusted_parent_provenance(candidate, results, trusted_ids)
    if provenance is not None:
        trusted["provenance"] = provenance
    if public_interface is not None:
        declared_public_axioms = {
            str(item) for item in public_interface.get("exported_axiom_ids", [])
        }
        trusted_public_axioms = sorted(declared_public_axioms & trusted_ids)
        trusted["public_interface"] = {
            "policy": public_interface.get("policy"),
            "exported_axiom_ids": trusted_public_axioms,
            "private_axiom_ids": sorted(trusted_ids - set(trusted_public_axioms)),
            "exported_occurrence_ids": sorted(occurrence_ids),
            "exported_predicate_ids": sorted(predicate_ids),
            "exported_identity_ids": sorted(identity_ids),
            "boundary_coverage": deepcopy(public_interface.get("boundary_coverage", [])),
            "all_exported_axioms_trusted": declared_public_axioms <= trusted_ids,
        }
    return trusted


def _certified_empty_leaf_abstraction(
    candidate: dict[str, Any],
    handoff: dict[str, Any],
) -> dict[str, Any] | None:
    """Certify a deliberately empty µMCM for a semantically inert leaf.

    Empty abstractions are safe over-approximations even for stateful leaves:
    they constrain nothing and therefore cannot remove a concrete RTL behavior.
    The certificate requires complete WorkUnit coverage, an explicit rationale,
    and no semantic declarations, assumptions, or unresolved questions.  Owned
    state/events are counted in the artifact so the intentional omission stays
    auditable and can be reopened by CEGAR.
    """

    unit = handoff.get("work_unit", {})
    if not isinstance(unit, dict) or not unit.get("is_leaf") or not unit.get("coverage_complete"):
        return None
    if any(
        candidate.get(field)
        for field in (
            "occurrences",
            "predicates",
            "identity_keys",
            "cases",
            "axioms",
            "assumptions",
            "unresolved",
        )
    ):
        return None
    rationale = candidate.get("rationale", [])
    if not isinstance(rationale, list) or not any(
        isinstance(item, str) and item.strip() for item in rationale
    ):
        return None
    return {
        "policy": "covered-explicit-empty-leaf-overapproximation-v0.1",
        "work_unit_id": candidate.get("work_unit_id"),
        "coverage_complete": True,
        "owned_event_count": len(handoff.get("events", [])),
        "owned_state_count": len(handoff.get("state", [])),
        "owned_memory_state_count": len(handoff.get("memory_state", [])),
        "semantic_object_count": 0,
        "assumption_count": 0,
        "unresolved_count": 0,
        "interpretation": (
            "The leaf contributes no µMCM constraint. Its combinational outputs "
            "remain unconstrained as a safe over-approximation and may be reopened by CEGAR."
        ),
    }


def run_semantic_validation(
    candidate: dict[str, Any],
    handoff: dict[str, Any],
    *,
    formal_backend: str = "none",
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    from .formal import get_formal_backend

    state_register = "state"
    for occurrence in candidate.get("occurrences", []):
        register = occurrence.get("grounding", {}).get("state_register")
        if register:
            state_register = register
            break
    else:
        for predicate in candidate.get("predicates", []):
            register = predicate.get("grounding", {}).get("state_register")
            if register:
                state_register = register
                break

    model = HandoffControlModel(handoff, state_register=state_register)
    model.label_occurrences(candidate.get("occurrences", []))
    compiled = compile_candidate_properties(candidate)
    backend = get_formal_backend(formal_backend)
    obligations = compiled["obligations"]

    def report(stage: str, **details: Any) -> None:
        if progress_callback is not None:
            progress_callback({"stage": stage, **details})

    report(
        "validation_started",
        total=len(obligations),
        backend=backend.name,
        work_unit_id=candidate.get("work_unit_id"),
    )

    imported_refs = {
        "occurrences": set(handoff.get("grounding", {}).get("imported_occurrence_ids", [])),
        "predicates": set(handoff.get("grounding", {}).get("imported_predicate_ids", [])),
        "identities": set(handoff.get("grounding", {}).get("imported_identity_ids", [])),
    }

    results: list[dict[str, Any]] = []
    for index, obligation in enumerate(obligations, start=1):
        progress_details = {
            "index": index,
            "total": len(obligations),
            "axiom_id": str(obligation.get("axiom_id", "")),
            "checker": str(obligation.get("checker", "")),
        }
        report("obligation_started", **progress_details)
        references = obligation.get("references", {})
        uses_imported = any(
            set(references.get(kind, [])) & imported_refs[kind]
            for kind in ("occurrences", "predicates", "identities")
        )
        if uses_imported:
            report("phase_started", phase="imported-deferred", **progress_details)
            structural = {
                "status": STRUCTURAL_UNKNOWN,
                "reason": (
                    "obligation references frozen child semantic objects; "
                    "parent-local RTL checkers must not reopen child RTL"
                ),
                "proof_domain": "composition-summary-boundary",
            }
            formal = {
                "status": "NOT_RUN",
                "backend": backend.name,
                "reason": (
                    "current formal backend has no certified composition rule for "
                    "axioms spanning imported child µMCM objects"
                ),
            }
        else:
            report("phase_started", phase="structural", **progress_details)
            structural = _run_structural_checker(model, candidate, obligation)
            # Structural control/dataflow checkers are conservative abstractions.
            # Their counterexamples may therefore be spurious; an exact formal
            # proof is allowed to discharge the concrete obligation.
            report("phase_started", phase="formal", **progress_details)
            formal = backend.prove(
                obligation,
                candidate=candidate,
                handoff=handoff,
                model=model,
                structural=structural,
            )

        level = _validation_level(structural.get("status", STRUCTURAL_UNKNOWN), formal.get("status", "NOT_RUN"))
        results.append(
            {
                **obligation,
                "grounding_status": GROUNDED,
                "structural": structural,
                "formal": formal,
                "validation_level": level,
                "trusted": level in {FORMALLY_PROVED, SPEC_PROVED},
            }
        )
        report(
            "obligation_completed",
            validation_level=level,
            formal_status=str(formal.get("status", "NOT_RUN")),
            **progress_details,
        )

    if backend.name != "none" and handoff.get("composition", {}).get("mode") == "parent_synthesis":
        from .composition_prover import prove_composition_obligations

        report("composition_started", total=len(obligations))
        composed = prove_composition_obligations(candidate, handoff, results)
        for result in results:
            proof = composed.get(str(result.get("axiom_id")))
            if proof is None:
                continue
            result["formal"] = proof
            level = _validation_level(
                result.get("structural", {}).get("status", STRUCTURAL_UNKNOWN),
                proof.get("status", "NOT_RUN"),
            )
            result["validation_level"] = level
            result["trusted"] = level in {FORMALLY_PROVED, SPEC_PROVED}
        report(
            "composition_completed",
            total=len(obligations),
            proved_axiom_ids=sorted(composed),
        )

    level_order = [GROUNDED, PARTIALLY_SUPPORTED, STRUCTURALLY_SUPPORTED, FORMALLY_PROVED, SPEC_PROVED, REFUTED]
    counts = {
        level: sum(1 for result in results if result.get("validation_level") == level)
        for level in level_order
    }
    has_counterexample = counts[REFUTED] > 0
    is_parent = handoff.get("composition", {}).get("mode") == "parent_synthesis"
    empty_leaf_certificate = _certified_empty_leaf_abstraction(candidate, handoff)
    all_structural = ((is_parent and not results) or empty_leaf_certificate is not None) or (
        bool(results)
        and all(
            result.get("validation_level")
            in {STRUCTURALLY_SUPPORTED, FORMALLY_PROVED, SPEC_PROVED}
            for result in results
        )
    )
    all_formal = ((is_parent and not results) or empty_leaf_certificate is not None) or (
        bool(results)
        and all(
            result.get("validation_level") in {FORMALLY_PROVED, SPEC_PROVED}
            for result in results
        )
    )
    declared_public = _declared_public_interface(candidate)
    public_validation = None
    if declared_public is not None:
        exported = {
            str(item) for item in declared_public.get("exported_axiom_ids", [])
        }
        trusted_result_ids = {
            str(result.get("axiom_id")) for result in results if result.get("trusted")
        }
        public_validation = {
            "policy": declared_public.get("policy"),
            "exported_axiom_count": len(exported),
            "trusted_exported_axiom_count": len(exported & trusted_result_ids),
            "private_axiom_count": len(results) - len(exported),
            "all_exported_axioms_trusted": exported <= trusted_result_ids,
            "boundary_coverage_count": len(declared_public.get("boundary_coverage", [])),
        }

    report(
        "validation_completed",
        total=len(obligations),
        counts=counts,
        trusted_axiom_count=sum(1 for result in results if result.get("trusted")),
    )

    return {
        "validator": SEMANTIC_VALIDATOR_VERSION,
        "property_compiler": PROPERTY_COMPILER_VERSION,
        "formal_backend": backend.describe(),
        "work_unit_id": candidate.get("work_unit_id"),
        "control_model": {
            "state_register": state_register,
            "reset_state": model.reset_state,
            "known_states": sorted(model.known_states),
            "transitions": [transition.to_dict() for transition in model.transitions],
        },
        "results": results,
        "counts": counts,
        "candidate_axiom_count": len(results),
        "trusted_axiom_count": sum(1 for result in results if result.get("trusted")),
        "all_axioms_structurally_supported": all_structural,
        "all_axioms_formally_proved": all_formal,
        "has_counterexample": has_counterexample,
        "empty_abstraction_certificate": empty_leaf_certificate,
        "public_interface_validation": public_validation,
        "validation_policy": (
            "Grounding and deterministic finite-control/dataflow checks provide evidence only. "
            "They do not make an axiom trusted. Only FORMALLY_PROVED or SPEC_PROVED axioms "
            "may constrain parent composition. Missing axioms are handled later by counterexample-guided refinement."
        ),
    }


def validate_task_dir(
    task_dir: str | Path,
    *,
    formal_backend: str = "none",
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    directory = Path(task_dir)
    task = json.loads((directory / "task.json").read_text(encoding="utf-8"))
    candidate = json.loads((directory / "response_parsed.json").read_text(encoding="utf-8"))
    grounding = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    if not grounding.get("valid"):
        raise ValueError("candidate grounding is invalid; semantic validation is fail-closed")
    handoff = json.loads((directory / "static_handoff.json").read_text(encoding="utf-8"))
    compiled = compile_candidate_properties(candidate)
    semantic = run_semantic_validation(
        candidate,
        handoff,
        formal_backend=formal_backend,
        progress_callback=progress_callback,
    )
    trusted = _build_trusted_umcm(candidate, semantic["results"])
    if semantic.get("empty_abstraction_certificate") is not None:
        trusted["empty_abstraction"] = semantic["empty_abstraction_certificate"]

    (directory / "property_obligations.json").write_text(
        json.dumps(compiled, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "semantic_validation.json").write_text(
        json.dumps(semantic, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "trusted_umcm.json").write_text(
        json.dumps(trusted, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    if semantic["has_counterexample"]:
        status = "AXIOM_COUNTEREXAMPLE"
        next_action = "Return the counterexample to the conversation and refine the candidate axiom."
    elif semantic["all_axioms_formally_proved"]:
        status = "FORMALLY_VALIDATED"
        if task.get("kind") == "parent_synthesis":
            next_action = (
                "All newly declared parent axioms are trusted (possibly vacuously zero); "
                "freeze the composite parent while retaining frozen child imports."
            )
        else:
            next_action = "The formally proved axioms may be frozen into the trusted leaf µMCM."
    elif semantic["trusted_axiom_count"] > 0:
        status = "PARTIALLY_FORMALLY_VALIDATED"
        next_action = (
            "Freeze only the proved axioms already present in trusted_umcm.json; "
            "keep the remaining candidate axioms outside the trusted abstraction until a stronger backend proves them."
        )
    elif semantic["all_axioms_structurally_supported"]:
        status = "STRUCTURAL_SUPPORT_COMPLETE"
        next_action = "Run a formal backend before any axiom enters trusted_umcm.json."
    else:
        status = "VALIDATION_INCOMPLETE"
        next_action = "Review unresolved/partial structural obligations and then run a real formal backend."

    status_payload = {
        "status": status,
        "task_id": candidate.get("task_id"),
        "candidate_axiom_count": semantic["candidate_axiom_count"],
        "trusted_axiom_count": semantic["trusted_axiom_count"],
        "next_action": next_action,
    }
    (directory / "status.json").write_text(
        json.dumps(status_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_run_summary(directory)
    return semantic

def freeze_task_dir(task_dir: str | Path) -> dict[str, Any]:
    """Freeze a fully validated WorkUnit summary for composition.

    Closure means all currently declared *new* candidate axioms are trusted and
    no unresolved item remains. Parent summaries additionally retain their
    already-frozen child imports; no child RTL is reopened.
    """

    directory = Path(task_dir)

    # Backward compatibility: older leaf-level freeze tests and callers construct
    # only response_parsed.json / semantic_validation.json / trusted_umcm.json.
    # Parent synthesis, however, requires task/static-handoff composition metadata
    # and remains fail-closed.
    task_path = directory / "task.json"
    task = (
        json.loads(task_path.read_text(encoding="utf-8"))
        if task_path.is_file()
        else {"kind": "leaf_abstraction"}
    )

    handoff_path = directory / "static_handoff.json"
    if task.get("kind") == "parent_synthesis":
        if not handoff_path.is_file():
            raise ValueError(
                "parent_synthesis freeze requires static_handoff.json with frozen child composition metadata"
            )
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    else:
        handoff = (
            json.loads(handoff_path.read_text(encoding="utf-8"))
            if handoff_path.is_file()
            else {}
        )

    candidate = json.loads((directory / "response_parsed.json").read_text(encoding="utf-8"))
    semantic = json.loads((directory / "semantic_validation.json").read_text(encoding="utf-8"))
    trusted = json.loads((directory / "trusted_umcm.json").read_text(encoding="utf-8"))
    if semantic.get("has_counterexample"):
        raise ValueError("cannot freeze a WorkUnit with a refuted candidate axiom")
    if not semantic.get("all_axioms_formally_proved"):
        raise ValueError("cannot freeze until every declared candidate axiom is FORMALLY_PROVED or SPEC_PROVED")
    if candidate.get("unresolved"):
        raise ValueError("cannot freeze while candidate unresolved items remain")
    if len(trusted.get("axioms", [])) != len(candidate.get("axioms", [])):
        raise ValueError("trusted µMCM does not contain every declared candidate axiom")

    if task.get("kind") == "parent_synthesis":
        prompt_match = re.fullmatch(
            r"parent-synthesis-prompt-0\.(\d+)",
            str(task.get("prompt_version", "")),
        )
        prompt_minor = int(prompt_match.group(1)) if prompt_match else None
        if prompt_minor is not None and prompt_minor >= 3 and _declared_public_interface(candidate) is None:
            raise ValueError(
                "cannot freeze a compact parent task without an explicit public interface; "
                "regenerate it with parent-synthesis-prompt-0.4 or newer"
            )

    empty_leaf_certificate = _certified_empty_leaf_abstraction(candidate, handoff)
    if task.get("kind") != "parent_synthesis" and not candidate.get("axioms"):
        if empty_leaf_certificate is None:
            raise ValueError(
                "cannot freeze an empty leaf abstraction without a covered explicit-overapproximation certificate"
            )
        if (
            semantic.get("empty_abstraction_certificate") != empty_leaf_certificate
            or trusted.get("empty_abstraction") != empty_leaf_certificate
        ):
            raise ValueError(
                "empty leaf abstraction certificate is missing or stale; rerun semantic validation"
            )

    if task.get("kind") == "parent_synthesis":
        expected_trusted = _build_trusted_umcm(candidate, semantic.get("results", []))
        if trusted.get("provenance") != expected_trusted.get("provenance"):
            raise ValueError(
                "trusted parent provenance is missing or stale; rerun semantic validation before freezing"
            )
        if trusted.get("public_interface") != expected_trusted.get("public_interface"):
            raise ValueError(
                "trusted parent public interface is missing or stale; rerun semantic validation before freezing"
            )

    frozen = dict(trusted)
    if task.get("kind") == "parent_synthesis":
        from .composition import merge_semantic_catalogs, semantic_catalog_from_frozen

        composition = handoff.get("composition", {})
        child_summaries = (
            composition.get("child_summaries", [])
            if isinstance(composition, dict)
            else []
        )
        if not child_summaries:
            raise ValueError("cannot freeze parent without frozen child summaries")

        portable_imports = []
        imported_catalogs = []
        for child in child_summaries:
            child_frozen = child.get("frozen_umcm")
            child_catalog = child.get("semantic_catalog")
            if not isinstance(child_frozen, dict) or not isinstance(child_catalog, dict):
                raise ValueError("parent child summary is incomplete")
            imported_catalogs.append(child_catalog)
            portable_imports.append(
                {
                    "child_id": child.get("child_id"),
                    "child_kind": child.get("child_kind"),
                    "summary_ref": child.get("summary_ref"),
                    "task_id": child.get("task_id"),
                    "frozen_umcm_sha256": child.get("frozen_umcm_sha256"),
                    "template_frozen_umcm_sha256": child.get("template_frozen_umcm_sha256"),
                    "implementation_sha256": child.get("implementation_sha256"),
                    "instance_reuse": child.get("instance_reuse"),
                    "semantic_catalog": child_catalog,
                    "frozen_umcm": child_frozen,
                }
            )

        local_catalog = semantic_catalog_from_frozen(
            frozen,
            work_unit_id=str(candidate.get("work_unit_id")),
        )
        semantic_catalog = merge_semantic_catalogs(
            *imported_catalogs,
            local_catalog,
        )
        frozen["composition"] = {
            "mode": "parent_synthesis",
            "policy": "transparent-frozen-child-imports-v0.1",
            "imports": portable_imports,
            "semantic_catalog": semantic_catalog,
            "note": (
                "Child RTL is not part of this frozen parent. Imported child µMCMs "
                "remain frozen semantic components; descendant semantic names are "
                "transparently propagated in v0.1 for higher-level synthesis."
            ),
        }

    frozen["freeze"] = {
        "status": "FROZEN_FOR_COMPOSITION",
        "policy": (
            "all-declared-axioms-trusted-plus-explicit-public-interface-v0.2"
            if isinstance(trusted.get("public_interface"), dict)
            else "all-declared-axioms-trusted-and-no-unresolved-v0.1"
        ),
        "candidate_axiom_count": len(candidate.get("axioms", [])),
        "trusted_axiom_count": len(trusted.get("axioms", [])),
        "exported_axiom_count": len(
            trusted.get("public_interface", {}).get("exported_axiom_ids", [])
            if isinstance(trusted.get("public_interface"), dict)
            else trusted.get("trusted_axiom_ids", [])
        ),
        "private_axiom_count": len(
            trusted.get("public_interface", {}).get("private_axiom_ids", [])
            if isinstance(trusted.get("public_interface"), dict)
            else []
        ),
        "empty_abstraction": empty_leaf_certificate is not None,
        "reopen_policy": (
            "This summary may be reopened if later parent/system counterexample validation "
            "shows the abstraction is too weak and a missing concrete constraint must be synthesized."
        ),
    }
    (directory / "frozen_umcm.json").write_text(
        json.dumps(frozen, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    status_payload = {
        "status": "FROZEN_FOR_COMPOSITION",
        "task_id": candidate.get("task_id"),
        "candidate_axiom_count": len(candidate.get("axioms", [])),
        "trusted_axiom_count": len(trusted.get("axioms", [])),
        "next_action": (
            "A higher parent synthesis step may consume frozen_umcm.json; "
            "reopen only through counterexample-guided refinement."
        ),
    }
    (directory / "status.json").write_text(
        json.dumps(status_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_run_summary(directory)
    return frozen
