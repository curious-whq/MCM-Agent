from __future__ import annotations

import math
import re
from typing import Any

from .semantic import (
    STRUCTURALLY_SUPPORTED,
    STRUCTURAL_UNKNOWN,
    HandoffControlModel,
    _call,
    _canonical_expr,
    _literal,
    _statement_rhs,
)
from .formal_patterns import (
    _and,
    _bool_expr,
    _bool_refs,
    _not,
    _occurrence_condition,
    _or,
    _propagate_bool_refs,
    _unsat,
)


_SMEM_VECTOR_RE = re.compile(
    r"^smem\s+([^\s:]+)\s*:\s*UInt<(\d+)>\[(\d+)\]\s*\[(\d+)\]$"
)
_SMEM_SCALAR_RE = re.compile(r"^smem\s+([^\s:]+)\s*:\s*UInt<(\d+)>\s*\[(\d+)\]$")
_WRITE_MPORT_RE = re.compile(
    r"^write\s+mport\s+([^\s=]+)\s*=\s*([^\[]+)\[([^\]]+)\],\s*([^\s]+)$"
)
_READ_MPORT_RE = re.compile(
    r"^read\s+mport\s+([^\s=]+)\s*=\s*([^\[]+)\[([^\]]+)\],\s*([^\s]+)$"
)


def _nf(model: HandoffControlModel, expr: str) -> tuple[Any, ...] | None:
    return _canonical_expr(model, expr, cut_roots=model.state_roots)


def _simplify_mode(
    expr: tuple[Any, ...],
    active: tuple[Any, ...],
    enabled: bool,
) -> tuple[Any, ...]:
    if expr == active:
        return ("lit", int(enabled))
    if not expr or expr[0] != "call":
        return expr
    name = expr[1]
    args = tuple(_simplify_mode(item, active, enabled) for item in expr[2:])
    if name == "mux" and len(args) == 3 and args[0][0] == "lit":
        return args[1] if args[0][1] else args[2]
    if name in {"asSInt", "asUInt"} and len(args) == 1:
        # Casts preserve the selected bit pattern.  A one-bit signed literal 1
        # is the FIRRTL lowering used to construct an all-lanes mask.
        if name == "asSInt" and args[0] == ("lit", 1):
            return ("sign_one",)
        return args[0]
    if name == "bits" and len(args) == 3 and args[1][0] == args[2][0] == "lit":
        hi, lo = int(args[1][1]), int(args[2][1])
        if args[0] == ("sign_one",):
            return ("lit", (1 << (hi - lo + 1)) - 1)
        if args[0][0] == "lit":
            return ("lit", (int(args[0][1]) >> lo) & ((1 << (hi - lo + 1)) - 1))
    if name in {"and", "or"} and len(args) == 2:
        if args[0][0] == args[1][0] == "lit":
            value = (int(args[0][1]) & int(args[1][1])) if name == "and" else (
                int(args[0][1]) | int(args[1][1])
            )
            return ("lit", value)
        identity = 1 if name == "and" else 0
        annihilator = 0 if name == "and" else 1
        if ("lit", annihilator) in args:
            return ("lit", annihilator)
        if args[0] == ("lit", identity):
            return args[1]
        if args[1] == ("lit", identity):
            return args[0]
        return ("call", name, *sorted(args, key=repr))
    if name in {"eq", "neq"} and len(args) == 2:
        if args[0][0] == args[1][0] == "lit":
            equal = args[0][1] == args[1][1]
            return ("lit", int(equal if name == "eq" else not equal))
        if args[1] == ("lit", 0):
            if args[0] == ("lit", 0):
                return ("lit", int(name == "eq"))
            if args[0] == ("lit", 1):
                return ("lit", int(name == "neq"))
        return ("call", name, *sorted(args, key=repr))
    return ("call", name, *args)


def _equivalent_address(
    actual: tuple[Any, ...],
    expected: tuple[Any, ...],
    domain: dict[str, int],
) -> bool:
    if actual == expected:
        return True
    if (
        len(actual) == 5
        and actual[:2] == ("call", "bits")
        and actual[2] == expected
        and actual[3][0] == actual[4][0] == "lit"
        and int(actual[4][1]) == 0
    ):
        width = int(actual[3][1]) + 1
        return int(domain["start"]) >= 0 and int(domain["end_exclusive"]) <= (1 << width)
    return False


def _flatten_cat(expr: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    if len(expr) == 4 and expr[:2] == ("call", "cat"):
        return _flatten_cat(expr[2]) + _flatten_cat(expr[3])
    return [expr]


def _packed_values(
    model: HandoffControlModel,
    fields: list[dict[str, Any]],
    key: str,
) -> tuple[list[tuple[Any, ...]], list[dict[str, Any]]] | None:
    ordered = sorted(fields, key=lambda item: int(item["storage_bits"]["hi"]), reverse=True)
    values: list[tuple[Any, ...]] = []
    layout = []
    for field in ordered:
        value = _nf(model, str(field[key]))
        if value is None:
            return None
        values.append(value)
        layout.append({"name": field["name"], **field["storage_bits"]})
    return values, layout


def _memory_shape(
    model: HandoffControlModel,
    storage: str,
) -> tuple[int, int, int, dict[str, Any]] | None:
    matches = []
    for statement in model.statements.values():
        if statement.get("kind") != "memory":
            continue
        text = str(statement.get("text", ""))
        vector = _SMEM_VECTOR_RE.match(text)
        scalar = _SMEM_SCALAR_RE.match(text)
        if vector and vector.group(1) == storage:
            matches.append((int(vector.group(2)), int(vector.group(3)), int(vector.group(4)), statement))
        elif scalar and scalar.group(1) == storage:
            matches.append((int(scalar.group(2)), 1, int(scalar.group(3)), statement))
    return matches[0] if len(matches) == 1 else None


def _mports(
    model: HandoffControlModel,
    storage: str,
    *,
    read: bool,
) -> list[tuple[str, str, str, dict[str, Any]]]:
    pattern = _READ_MPORT_RE if read else _WRITE_MPORT_RE
    kind = "read_mport" if read else "write_mport"
    result = []
    for statement in model.statements.values():
        if statement.get("kind") != kind:
            continue
        match = pattern.match(str(statement.get("text", "")))
        if match and match.group(2).strip() == storage:
            result.append((match.group(1), match.group(3).strip(), match.group(4), statement))
    return result


def _event(model: HandoffControlModel, candidate: dict[str, Any], occurrence: str) -> dict[str, Any] | None:
    obj = next((item for item in candidate.get("occurrences", []) if item.get("id") == occurrence), None)
    if not isinstance(obj, dict) or obj.get("kind") != "boundary":
        return None
    physical = obj.get("physical_event_ids", [])
    return model._event_info(physical[0]) if len(physical) == 1 else None


def _controls_equal_event(
    model: HandoffControlModel,
    statement: dict[str, Any],
    event: dict[str, Any],
    active: tuple[Any, ...],
    mode: bool,
) -> bool:
    controls = [str(item) for item in statement.get("control_reads", [])]
    if not controls:
        return False
    actual = _nf(model, controls[-1])
    valid = event.get("valid")
    ready = event.get("ready")
    if actual is None or not isinstance(valid, str) or not isinstance(ready, str):
        return False
    expected = _nf(model, f"and({valid}, {ready})")
    return expected is not None and _simplify_mode(actual, active, mode) == _simplify_mode(expected, active, mode)


def _controls_equal_occurrence(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    statement: dict[str, Any],
    occurrence: str,
) -> tuple[bool, int]:
    refs = _bool_refs(model, candidate)
    controls = [str(item) for item in statement.get("control_reads", [])]
    for control in controls:
        refs.add(control)
        _propagate_bool_refs(model, control, refs)
    expected = _occurrence_condition(model, candidate, occurrence, refs)
    if expected is None or not controls:
        return False, 0
    actual: tuple[Any, ...] = ("const", True)
    for control in controls:
        value = _bool_expr(model, refs, control)
        if value is None:
            return False, 0
        actual = _and(actual, value)
    mismatch = _or(_and(actual, _not(expected)), _and(expected, _not(actual)))
    proved, atoms = _unsat(mismatch)
    return proved is True, atoms


def _read_target_value(
    model: HandoffControlModel,
    expr: str,
    seen: set[str] | None = None,
) -> tuple[tuple[Any, ...], int] | None:
    """Resolve aliases while counting explicit register stages after an smem read."""

    text = expr.strip()
    seen = set() if seen is None else set(seen)
    value = _literal(text)
    if value is not None:
        return ("lit", value), 0
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*(?:(?:\.[A-Za-z_][A-Za-z0-9_$]*)|(?:\[[^\[\]]+\]))*", text):
        if text in seen:
            return None
        rhs = model.rhs(text)
        if rhs is None:
            return ("ref", text), 0
        nested = _read_target_value(model, rhs, seen | {text})
        if nested is None:
            return None
        is_register = any(
            text == root or text.startswith(root + ".") or text.startswith(root + "[")
            for root in model.state_roots
        )
        return nested[0], nested[1] + int(is_register)
    call = _call(text)
    if call is None:
        return None
    name, args = call
    normalized = []
    stages = 0
    for arg in args:
        nested = _read_target_value(model, arg, seen)
        if nested is None:
            return None
        normalized.append(nested[0])
        stages = max(stages, nested[1])
    return ("call", name, *normalized), stages


def _full_width_equivalent(
    actual: tuple[Any, ...],
    expected: tuple[Any, ...],
    width: int,
) -> bool:
    return actual == expected or (
        len(actual) == 5
        and actual[:2] == ("call", "bits")
        and actual[2] == expected
        and actual[3:] == (("lit", width - 1), ("lit", 0))
    )


def _mask_bit_is_one(mask: tuple[Any, ...], index: int) -> bool:
    """Return whether one declared lane-mask bit is statically enabled."""

    return mask[0] == "lit" and bool((int(mask[1]) >> index) & 1)


def _counter_initialization_certificate(
    model: HandoffControlModel,
    active: tuple[Any, ...],
    address: tuple[Any, ...],
    domain: dict[str, int],
) -> dict[str, Any] | None:
    if address[0] != "ref" or int(domain["start"]) != 0:
        return None
    counter = str(address[1])
    expected_active = ("call", "lt", ("ref", counter), ("lit", int(domain["end_exclusive"])))
    if active != expected_active:
        return None
    declarations = [
        statement for statement in model.statements.values()
        if statement.get("kind") == "regreset" and counter in statement.get("drives", [])
    ]
    if len(declarations) != 1 or _literal(str(declarations[0].get("text", "")).rsplit(",", 1)[-1]) != 0:
        return None
    writes = []
    for statement in model.statements.values():
        if statement.get("kind") in {"reg", "regreset"} or counter not in statement.get("drives", []):
            continue
        parsed = _statement_rhs(statement)
        if parsed is not None and parsed[0] == counter:
            writes.append((statement, parsed[1]))
    if len(writes) != 1:
        return None
    statement, rhs = writes[0]
    rhs_nf = _nf(model, rhs)
    increment = ("call", "add", ("ref", counter), ("lit", 1))
    valid_increment = rhs_nf == increment or (
        isinstance(rhs_nf, tuple)
        and len(rhs_nf) == 4
        and rhs_nf[:2] == ("call", "tail")
        and rhs_nf[2] == increment
    )
    controls = [_nf(model, str(item)) for item in statement.get("control_reads", [])]
    if not valid_increment or active not in controls:
        return None
    match = re.search(r"UInt<(\d+)>", str(declarations[0].get("text", "")))
    width = int(match.group(1)) if match else None
    if width is None or width < math.ceil(math.log2(int(domain["end_exclusive"]) + 1)):
        return None
    return {
        "kind": "exact-reset-initialization-sweep",
        "counter": counter,
        "counter_width": width,
        "reset_value": 0,
        "domain": dict(domain),
        "increment_statement_id": int(statement["id"]),
        "active_guard": f"{counter} < {domain['end_exclusive']}",
    }


def prove_indexed_storage_flow(
    model: HandoffControlModel,
    candidate: dict[str, Any],
    *,
    storage: str,
    key: dict[str, Any],
    write: dict[str, Any],
    read: dict[str, Any],
    value_fields: list[dict[str, Any]],
    initialization: dict[str, Any],
    resolution: str,
    relations: dict[str, str],
    read_write_collision: str = "exclusive",
) -> dict[str, Any]:
    """Certify rf/co/fr semantics from one exact synchronous indexed memory."""

    if resolution != "latest_prior_write_same_key":
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported storage resolution"}
    domain = key.get("address_domain", {})
    lane = key.get("lane", {})
    if not isinstance(domain, dict) or not isinstance(lane, dict):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "invalid storage key metadata"}
    lane_count = lane.get("count")
    shape = _memory_shape(model, storage)
    if shape is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "exact FIRRTL memory declaration not found"}
    width, actual_lanes, depth, memory_statement = shape
    if actual_lanes != lane_count or depth != int(domain.get("end_exclusive", -1)) or int(domain.get("start", -1)) != 0:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "declared key domain does not match memory shape"}

    ranges = []
    for field in value_fields:
        bits = field.get("storage_bits", {})
        ranges.extend(range(int(bits.get("lo", -1)), int(bits.get("hi", -1)) + 1))
        if len(field.get("read_targets", [])) != actual_lanes:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "read target count does not match lane count"}
    if sorted(ranges) != list(range(width)) or len(set(ranges)) != width:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "value fields must exactly partition the stored word"}

    write_ports = _mports(model, storage, read=False)
    read_ports = _mports(model, storage, read=True)
    if len(write_ports) != 1 or len(read_ports) != 1:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "prover requires one exact read and write mport"}
    write_port, write_address_actual, write_clock, write_statement = write_ports[0]
    read_port, read_address_actual, read_clock, read_statement = read_ports[0]
    if write_clock != read_clock or write_clock != "clock" or int(read.get("latency_cycles", -1)) < 1:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "memory is not a certified synchronous RAM"}

    initialization_kind = str(initialization.get("kind", "explicit"))
    if initialization_kind not in {"explicit", "implicit_unconstrained"}:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported initialization kind"}
    explicit_initialization = initialization_kind == "explicit"
    active = _nf(model, str(initialization["active"])) if explicit_initialization else None
    init_address = _nf(model, str(initialization["address"])) if explicit_initialization else None
    write_address = _nf(model, str(write["address"]))
    read_address = _nf(model, str(read["address"]))
    actual_write_address = _nf(model, write_address_actual)
    actual_read_address = _nf(model, read_address_actual)
    required_expressions = {write_address, read_address, actual_write_address, actual_read_address}
    if explicit_initialization:
        required_expressions.update({active, init_address})
    if None in required_expressions:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "address or initialization expression is unresolved"}
    assert write_address is not None and read_address is not None
    assert actual_write_address is not None and actual_read_address is not None
    normal_write_address = (
        _simplify_mode(actual_write_address, active, False)
        if active is not None
        else actual_write_address
    )
    if not _equivalent_address(normal_write_address, write_address, domain):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "normal write address does not match the declared key"}
    if explicit_initialization:
        assert active is not None and init_address is not None
        if not _equivalent_address(_simplify_mode(actual_write_address, active, True), init_address, domain):
            return {"status": STRUCTURAL_UNKNOWN, "reason": "initialization address does not match the declared key"}
    if not _equivalent_address(actual_read_address, read_address, domain):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "sampled read address does not match the declared key"}

    read_control_proved, read_control_atoms = _controls_equal_occurrence(
        model, candidate, read_statement, str(read["request"])
    )
    if not read_control_proved:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "read mport is not enabled exactly by the read request"}

    write_control_atoms = 0
    write_port_control_proved = False
    write_occurrence_binding: dict[str, Any]
    if explicit_initialization:
        write_event = _event(model, candidate, str(write["on"]))
        if write_event is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "explicit storage write is not one boundary handshake"}
        write_controls = [_nf(model, str(item)) for item in write_statement.get("control_reads", [])]
        valid = write_event.get("valid")
        ready = write_event.get("ready")
        if not isinstance(valid, str) or not isinstance(ready, str):
            return {"status": STRUCTURAL_UNKNOWN, "reason": "explicit storage write boundary is incomplete"}
        normal_write = _nf(model, f"and({valid}, {ready})")
        assert active is not None
        if normal_write is None or not any(
            item is not None
            and _simplify_mode(item, active, False) == _simplify_mode(normal_write, active, False)
            and _simplify_mode(item, active, True) == ("lit", 1)
            for item in write_controls
        ):
            return {"status": STRUCTURAL_UNKNOWN, "reason": "shared write mport enable does not match init-or-write behavior"}
        write_occurrence_binding = {
            "kind": "shared-initialization-or-boundary-write",
            "write_mport_statement_id": int(write_statement["id"]),
        }
    else:
        write_port_control_proved, write_control_atoms = _controls_equal_occurrence(
            model, candidate, write_statement, str(write["on"])
        )
        write_occurrence_binding = {}

    lane_writers: dict[int, dict[str, Any]] = {}
    for statement in model.statements.values():
        for index in range(actual_lanes):
            if f"{write_port}[{index}]" in statement.get("drives", []):
                if index in lane_writers:
                    return {"status": STRUCTURAL_UNKNOWN, "reason": "multiple writers target one memory lane"}
                lane_writers[index] = statement
    if set(lane_writers) != set(range(actual_lanes)):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "not every memory lane has one exact writer"}

    external_mask = _nf(model, str(write["lane_mask"]))
    init_mask = _nf(model, str(initialization["lane_mask"])) if explicit_initialization else None
    packed_write = _packed_values(model, value_fields, "write_value")
    packed_init = _packed_values(model, value_fields, "initial_value") if explicit_initialization else None
    if external_mask is None or packed_write is None or (explicit_initialization and (init_mask is None or packed_init is None)):
        return {"status": STRUCTURAL_UNKNOWN, "reason": "mask or packed value expression is unresolved"}
    write_values, layout = packed_write
    init_values = packed_init[0] if packed_init is not None else []
    ordered_fields = sorted(value_fields, key=lambda item: int(item["storage_bits"]["hi"]), reverse=True)
    lane_certificates = []
    cell_write_atoms: dict[int, int] = {}
    for index, statement in sorted(lane_writers.items()):
        parsed = _statement_rhs(statement)
        if parsed is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "memory lane writer has no exact RHS"}
        actual_value = _nf(model, parsed[1])
        if actual_value is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "memory lane value cone is unresolved"}
        normal_value = _simplify_mode(actual_value, active, False) if active is not None else actual_value
        normal_parts = _flatten_cat(normal_value)
        normal_matches = len(normal_parts) == len(write_values) and all(
            _full_width_equivalent(actual, expected, int(field["storage_bits"]["hi"]) - int(field["storage_bits"]["lo"]) + 1)
            for actual, expected, field in zip(normal_parts, write_values, ordered_fields)
        )
        init_parts = _flatten_cat(_simplify_mode(actual_value, active, True)) if active is not None else []
        if not normal_matches or (explicit_initialization and init_parts != init_values):
            return {"status": STRUCTURAL_UNKNOWN, "reason": f"memory lane {index} value layout mismatch"}
        masks = [_nf(model, str(item)) for item in statement.get("control_reads", [])]
        expected_external = ("call", "bits", external_mask, ("lit", index), ("lit", index))
        expected_init = ("call", "bits", init_mask, ("lit", index), ("lit", index))
        if not explicit_initialization and not write_port_control_proved:
            # The occurrence may denote the physical cell write, with the RTL
            # lane mask already absorbed into its condition. In that exact
            # normalization the declared residual mask must be statically one.
            cell_control_proved, atom_count = _controls_equal_occurrence(
                model, candidate, statement, str(write["on"])
            )
            if not cell_control_proved or not _mask_bit_is_one(external_mask, index):
                return {
                    "status": STRUCTURAL_UNKNOWN,
                    "reason": (
                        "write occurrence matches neither the write mport plus lane mask "
                        f"nor exact memory lane {index} activation"
                    ),
                }
            cell_write_atoms[index] = atom_count
            external_mask_matches = True
        else:
            external_mask_matches = any(
                item is not None
                and (
                    _simplify_mode(item, active, False) if active is not None else item
                ) == (
                    _simplify_mode(expected_external, active, False) if active is not None else expected_external
                )
                for item in masks
            )
        init_mask_matches = not explicit_initialization or any(
            item is not None
            and _simplify_mode(item, active, True) == _simplify_mode(expected_init, active, True) == ("lit", 1)
            for item in masks
        )
        if not external_mask_matches or not init_mask_matches:
            return {"status": STRUCTURAL_UNKNOWN, "reason": f"memory lane {index} mask mismatch"}
        lane_certificates.append({
            "lane": index,
            "statement_id": int(statement["id"]),
            "normal_mask_bit": index,
            "initialized": explicit_initialization,
        })

    if not explicit_initialization:
        if write_port_control_proved:
            write_occurrence_binding = {
                "kind": "exact-write-mport-occurrence-with-lane-mask",
                "write_mport_statement_id": int(write_statement["id"]),
                "atom_count": write_control_atoms,
            }
        else:
            write_occurrence_binding = {
                "kind": "exact-cell-write-occurrence",
                "lane_statement_ids": [
                    int(lane_writers[index]["id"]) for index in sorted(lane_writers)
                ],
                "declared_lane_mask": "statically-enabled",
                "atom_count_by_lane": {
                    str(index): cell_write_atoms[index] for index in sorted(cell_write_atoms)
                },
            }

    read_bindings = []
    observed_latencies: set[int] = set()
    for field in value_fields:
        hi = int(field["storage_bits"]["hi"])
        lo = int(field["storage_bits"]["lo"])
        for index, target in enumerate(field["read_targets"]):
            resolved_target = _read_target_value(model, str(target))
            if resolved_target is None:
                return {"status": STRUCTURAL_UNKNOWN, "reason": f"read target {target!r} is unresolved"}
            target_nf, register_stages = resolved_target
            source = ("ref", f"{read_port}[{index}]")
            expected = source if lo == 0 and hi == width - 1 else (
                "call", "bits", source, ("lit", hi), ("lit", lo)
            )
            if target_nf != expected:
                return {"status": STRUCTURAL_UNKNOWN, "reason": f"read target {target!r} is not the declared storage slice"}
            observed_latencies.add(1 + register_stages)
            read_bindings.append({
                "lane": index,
                "field": field["name"],
                "target": target,
                "storage_bits": {"hi": hi, "lo": lo},
                "post_memory_register_stages": register_stages,
            })

    declared_latency = int(read["latency_cycles"])
    if observed_latencies != {declared_latency}:
        return {
            "status": STRUCTURAL_UNKNOWN,
            "reason": (
                f"declared read latency {declared_latency} does not match exact paths "
                f"{sorted(observed_latencies)}"
            ),
        }

    if explicit_initialization:
        assert active is not None and init_address is not None
        init_certificate = _counter_initialization_certificate(model, active, init_address, domain)
        if init_certificate is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "initialization is not an exact complete counter sweep"}
        read_event = _event(model, candidate, str(read["request"]))
        write_event = _event(model, candidate, str(write["on"]))
        if read_event is None or write_event is None:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "explicit storage accesses must be boundary handshakes"}
        for event in (read_event, write_event):
            ready = event.get("ready")
            ready_nf = _nf(model, str(ready)) if isinstance(ready, str) else None
            if ready_nf is None or _simplify_mode(ready_nf, active, True) != ("lit", 0):
                return {"status": STRUCTURAL_UNKNOWN, "reason": "external access is not blocked during initialization"}
    else:
        init_certificate = {
            "kind": "implicit-unconstrained-initial-writes",
            "per_key": True,
            "value": "fresh unconstrained nu_k",
            "co_position": "before every real write to the same key",
        }

    bool_refs = _bool_refs(model, candidate)
    for signal in (
        *([initialization["active"]] if explicit_initialization else []),
        *[item for occurrence in (read["request"], write["on"]) for item in (
            (_event(model, candidate, str(occurrence)) or {}).get("valid"),
            (_event(model, candidate, str(occurrence)) or {}).get("ready"),
        )],
    ):
        if isinstance(signal, str):
            bool_refs.add(signal)
            _propagate_bool_refs(model, signal, bool_refs)
    read_condition = _occurrence_condition(model, candidate, str(read["request"]), bool_refs)
    write_condition = _occurrence_condition(model, candidate, str(write["on"]), bool_refs)
    if read_condition is None or write_condition is None:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "read/write handshake condition is unresolved"}
    collision_free, collision_atoms = _unsat(_and(read_condition, write_condition))
    if read_write_collision == "exclusive":
        if collision_free is not True:
            return {"status": STRUCTURAL_UNKNOWN, "reason": "same-cycle read/write collision is possible or unresolved"}
        collision_certificate = {
            "kind": "exact-combinational-exclusion",
            "read": read["request"],
            "write": write["on"],
            "atom_count": collision_atoms,
        }
    elif read_write_collision == "implicit_unconstrained":
        collision_certificate = {
            "kind": "implicit-unconstrained-collision-write",
            "read": read["request"],
            "write": write["on"],
            "possible": collision_free is not True,
            "value": "fresh unconstrained chi_r",
            "co_position": "after prior writes and before the colliding real write",
            "rf_source_for_collision_read": True,
        }
    else:
        return {"status": STRUCTURAL_UNKNOWN, "reason": "unsupported read/write collision semantics"}

    return {
        "status": STRUCTURALLY_SUPPORTED,
        "proof": (
            f"{storage} is one {initialization_kind} synchronous indexed store; "
            "each read returns the value of its co-latest prior same-key write"
        ),
        "proof_domain": "exact-indexed-storage-rf-co-fr",
        "storage": {
            "name": storage,
            "statement_id": int(memory_statement["id"]),
            "word_width": width,
            "depth": depth,
            "lanes": actual_lanes,
            "clock": write_clock,
            "write_mport_statement_id": int(write_statement["id"]),
            "read_mport_statement_id": int(read_statement["id"]),
            "read_latency_cycles": declared_latency,
        },
        "key": {
            "address_domain": dict(domain),
            "lane": dict(lane),
        },
        "value_layout": layout,
        "write_lanes": lane_certificates,
        "write_occurrence_binding": write_occurrence_binding,
        "read_bindings": read_bindings,
        "initialization": init_certificate,
        "relations": {
            "rf": {
                "id": relations["rf"],
                "definition": "same-key write selected by the read, with no co-later write before the sampled request",
                "properties": ["same_key", "same_value", "functional_per_read", "latest_prior"],
                "initial_source": (
                    "explicit initialization write"
                    if explicit_initialization
                    else "implicit per-key write Init_k(k, nu_k)"
                ),
            },
            "co": {
                "id": relations["co"],
                "definition": "strict total order of committed writes per (address,lane)",
                "properties": ["per_key", "irreflexive", "transitive", "total_on_writes"],
            },
            "fr": {
                "id": relations["fr"],
                "definition": "rf^-1 ; co",
                "derived_from": [relations["rf"], relations["co"]],
            },
        },
        "collision_policy": read_write_collision,
        "collision_certificate": collision_certificate,
        "semantic_basis": "FIRRTL smem synchronous read/write semantics",
    }
