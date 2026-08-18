from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Iterable, Mapping

from .firrtl import FirrtlParseError, _split_source, parse_type
from .model import (
    Design,
    FirrtlType,
    GroundType,
    ModuleDef,
    PortDirection,
    SourceLoc,
    flatten_type,
)


class SignalKind(str, Enum):
    PORT = "port"
    WIRE = "wire"
    NODE = "node"
    REGISTER = "register"
    MEMORY = "memory"
    MEMORY_PORT = "memory_port"
    INSTANCE_PORT = "instance_port"
    UNKNOWN = "unknown"


class DependencyKind(str, Enum):
    DATA = "data"
    CONTROL = "control"
    STATE = "state"
    RESET = "reset"
    CLOCK = "clock"
    ADDRESS = "address"
    MEMORY = "memory"
    ALIAS = "alias"


class StatementStatus(str, Enum):
    SUPPORTED = "supported"
    NONDRIVING = "nondriving"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class SignalInfo:
    name: str
    kind: SignalKind
    source: SourceLoc | None = None
    type_text: str | None = None
    aggregate_root: str | None = None


@dataclass(frozen=True)
class StatementRecord:
    id: int
    module: str
    firrtl_line: int
    indent: int
    kind: str
    text: str
    source: SourceLoc | None
    status: StatementStatus
    drives: tuple[str, ...] = ()
    reads: tuple[str, ...] = ()
    control_reads: tuple[str, ...] = ()
    note: str | None = None

    @property
    def potentially_driving(self) -> bool:
        return self.status is StatementStatus.UNSUPPORTED


@dataclass(frozen=True)
class DependencyEdge:
    src: str
    dst: str
    kind: DependencyKind
    statement_ids: tuple[int, ...]
    source: SourceLoc | None = None


@dataclass
class ModuleDependencyGraph:
    module: str
    signals: dict[str, SignalInfo] = field(default_factory=dict)
    edges: list[DependencyEdge] = field(default_factory=list)
    statements: list[StatementRecord] = field(default_factory=list)
    register_roots: set[str] = field(default_factory=set)
    memory_roots: set[str] = field(default_factory=set)
    instance_modules: dict[str, str] = field(default_factory=dict)
    input_ports: set[str] = field(default_factory=set)
    output_ports: set[str] = field(default_factory=set)
    aggregate_leaves: dict[str, tuple[str, ...]] = field(default_factory=dict)
    aggregate_types: dict[str, FirrtlType] = field(default_factory=dict)

    def add_signal(self, info: SignalInfo) -> None:
        previous = self.signals.get(info.name)
        if previous is None or previous.kind is SignalKind.UNKNOWN:
            self.signals[info.name] = info

    def ensure_signal(self, name: str, source: SourceLoc | None = None) -> None:
        if name not in self.signals:
            kind = (
                SignalKind.INSTANCE_PORT
                if self._instance_prefix(name) is not None
                else SignalKind.UNKNOWN
            )
            self.signals[name] = SignalInfo(name=name, kind=kind, source=source)

    def add_edge(self, edge: DependencyEdge) -> None:
        self.ensure_signal(edge.src, edge.source)
        self.ensure_signal(edge.dst, edge.source)
        self.edges.append(edge)

    def _instance_prefix(self, name: str) -> str | None:
        head = name.split(".", 1)[0].split("[", 1)[0]
        return head if head in self.instance_modules else None

    def is_register(self, name: str) -> bool:
        return any(_is_prefix(root, name) for root in self.register_roots)

    def is_memory(self, name: str) -> bool:
        return any(_is_prefix(root, name) for root in self.memory_roots)

    def predecessors(
        self,
        signal: str,
        kinds: set[DependencyKind] | None = None,
    ) -> tuple[DependencyEdge, ...]:
        return tuple(
            edge
            for edge in self.edges
            if edge.dst == signal and (kinds is None or edge.kind in kinds)
        )

    @property
    def unsupported_statements(self) -> tuple[StatementRecord, ...]:
        return tuple(
            statement
            for statement in self.statements
            if statement.status is StatementStatus.UNSUPPORTED
        )

    @property
    def complete(self) -> bool:
        return not self.unsupported_statements


@dataclass(frozen=True)
class ExpressionDependencies:
    data: frozenset[str] = frozenset()
    control: frozenset[str] = frozenset()
    address: frozenset[str] = frozenset()

    def merge(self, other: "ExpressionDependencies") -> "ExpressionDependencies":
        return ExpressionDependencies(
            data=self.data | other.data,
            control=self.control | other.control,
            address=self.address | other.address,
        )

    @property
    def all_refs(self) -> frozenset[str]:
        return self.data | self.control | self.address


# Classic FIRRTL/CHIRRTL names plus subfield/subindex/subaccess spellings.
_REFERENCE_RE = re.compile(
    r"[A-Za-z_][A-Za-z0-9_$]*(?:"
    r"\.[A-Za-z_][A-Za-z0-9_$]*|"
    r"\[[^\[\]]+\]"
    r")*"
)

_STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')

_RESERVED = {
    # types / literals
    "UInt", "SInt", "Clock", "Reset", "AsyncReset", "Analog", "Fixed",
    # expression forms / primops
    "mux", "validif", "add", "sub", "mul", "div", "rem", "lt", "leq",
    "gt", "geq", "eq", "neq", "pad", "asUInt", "asSInt", "asClock",
    "asAsyncReset", "shl", "shr", "dshl", "dshr", "cvt", "neg", "not",
    "and", "or", "xor", "andr", "orr", "xorr", "cat", "bits", "head",
    "tail", "andr", "orr", "xorr", "read", "write", "rdwr",
    # statement keywords which may occur in fallback tokenization
    "when", "else", "node", "wire", "reg", "with", "reset", "is", "invalid",
    "inst", "of", "skip", "printf", "stop", "assert", "assume", "cover",
    "cmem", "smem", "mport", "infer",
}


def _strip_strings(text: str) -> str:
    return _STRING_RE.sub("", text)


def _is_prefix(root: str, name: str) -> bool:
    return (
        name == root
        or name.startswith(root + ".")
        or name.startswith(root + "[")
    )


def _canonicalize_reference(ref: str) -> tuple[str, set[str]]:
    """Normalize dynamic subaccesses and return index dependencies.

    Numeric indices remain precise. Dynamic indices are replaced by `[*]` and
    their index expressions are returned as address dependencies.
    """

    address_refs: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        content = match.group(1).strip()
        if content.isdigit():
            return f"[{content}]"
        deps = extract_expression_dependencies(content)
        address_refs.update(deps.all_refs)
        return "[*]"

    canonical = re.sub(r"\[([^\[\]]+)\]", replace, ref)
    return canonical, address_refs


def _simple_references(text: str) -> ExpressionDependencies:
    cleaned = _strip_strings(text)
    data: set[str] = set()
    address: set[str] = set()

    for match in _REFERENCE_RE.finditer(cleaned):
        token = match.group(0)
        if token in _RESERVED:
            continue
        # Width suffixes and base literal spelling are filtered because they do
        # not start with an identifier after quoted strings are removed.
        canonical, index_refs = _canonicalize_reference(token)
        if canonical in _RESERVED:
            continue
        data.add(canonical)
        address.update(index_refs)

    # Index refs are not also considered ordinary data for this expression.
    data -= address
    return ExpressionDependencies(
        data=frozenset(data),
        address=frozenset(address),
    )


def _split_top_level_args(text: str) -> list[str]:
    args: list[str] = []
    start = 0
    paren = bracket = brace = angle = 0
    in_string = False
    escape = False

    for index, char in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "(":
            paren += 1
        elif char == ")":
            paren -= 1
        elif char == "[":
            bracket += 1
        elif char == "]":
            bracket -= 1
        elif char == "{":
            brace += 1
        elif char == "}":
            brace -= 1
        elif char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "," and paren == bracket == brace == angle == 0:
            args.append(text[start:index].strip())
            start = index + 1

    args.append(text[start:].strip())
    return [arg for arg in args if arg]


def _outer_call(expr: str) -> tuple[str, list[str]] | None:
    expr = expr.strip()
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_$]*)\s*\(", expr)
    if match is None:
        return None

    name = match.group(1)
    open_index = expr.find("(", match.start(1) + len(name))
    depth = 0
    in_string = False
    escape = False
    close_index: int | None = None

    for index in range(open_index, len(expr)):
        char = expr[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                close_index = index
                break

    if close_index is None or expr[close_index + 1 :].strip():
        return None

    return name, _split_top_level_args(expr[open_index + 1 : close_index])


def extract_expression_dependencies(expr: str) -> ExpressionDependencies:
    """Extract conservative data/control/address dependencies from FIRRTL expr.

    `mux` and `validif` selectors are marked CONTROL. Generic primops are data
    dependencies. Dynamic vector indices are marked ADDRESS and canonicalized
    to wildcard element references.
    """

    expr = expr.strip()
    call = _outer_call(expr)
    if call is None:
        return _simple_references(expr)

    name, args = call

    if name == "mux" and len(args) == 3:
        select = extract_expression_dependencies(args[0])
        high = extract_expression_dependencies(args[1])
        low = extract_expression_dependencies(args[2])
        return ExpressionDependencies(
            data=high.data | low.data,
            control=(
                select.data
                | select.control
                | select.address
                | high.control
                | low.control
            ),
            address=high.address | low.address,
        )

    if name == "validif" and len(args) == 2:
        cond = extract_expression_dependencies(args[0])
        value = extract_expression_dependencies(args[1])
        return ExpressionDependencies(
            data=value.data,
            control=cond.all_refs | value.control,
            address=value.address,
        )

    # Constants such as UInt<...>(...) do not match _outer_call due to width
    # syntax; if a future spelling does, filtering the type name here avoids a
    # fake dependency.
    if name in {"UInt", "SInt"}:
        return ExpressionDependencies()

    combined = ExpressionDependencies()
    for arg in args:
        combined = combined.merge(extract_expression_dependencies(arg))
    return combined


@dataclass(frozen=True)
class _ControlBlock:
    indent: int
    condition_refs: frozenset[str]
    statement_id: int


_MODULE_START_RE = re.compile(
    r"^\s*(?:(?:public|private)\s+)?(?:module|extmodule)\s+"
    r"([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:"
)
_PORT_RE = re.compile(r"^\s*(input|output)\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$")
_INST_RE = re.compile(
    r"^\s*inst\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s+of\s+"
    r"([A-Za-z_.$][A-Za-z0-9_.$]*)\s*$"
)
_WIRE_RE = re.compile(r"^\s*wire\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$")
_NODE_RE = re.compile(r"^\s*node\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*=\s*(.+)$")
_CONNECT_RE = re.compile(r"^\s*(.+?)\s*(<=|<-)\s*(.+)$")
_INVALID_RE = re.compile(r"^\s*(.+?)\s+is\s+invalid\s*$")
_WHEN_RE = re.compile(r"^\s*when\s+(.+?)\s*:\s*$")
_ELSE_RE = re.compile(r"^\s*else\s*:\s*$")
_CMEM_RE = re.compile(r"^\s*(cmem|smem)\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$")
_MPORT_RE = re.compile(
    r"^\s*(read|write|infer)\s+mport\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*=\s*"
    r"([A-Za-z_.$][A-Za-z0-9_.$]*)\[(.+)\]\s*,\s*(.+)$"
)

_NONDRIVING_PREFIXES = (
    "skip",
    "printf",
    "stop",
    "assert",
    "assume",
    "cover",
)

_METADATA_PREFIXES = (
    "FIRRTL version",
    "%[[",
    "]]",
    "layer ",
    "option ",
)


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _strip_trailing_source(text: str) -> tuple[str, SourceLoc | None]:
    body, source = _split_source(text)
    return body.rstrip(), source


def _split_type_and_rest(text: str) -> tuple[str, str]:
    """Split a declaration at its first top-level comma."""
    parts = _split_top_level_args(text)
    if len(parts) < 2:
        raise FirrtlParseError(f"Expected type and clock: {text!r}")
    return parts[0], ",".join(parts[1:]).strip()


def _reg_decl(body: str) -> tuple[str, str, str, str | None, str | None] | None:
    match = re.match(r"^\s*reg\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$", body)
    if match is None:
        return None

    name = match.group(1)
    type_text, rest = _split_type_and_rest(match.group(2))

    # The clock is the first expression before optional `with :` reset syntax.
    if " with :" in rest:
        clock_text, reset_text = rest.split(" with :", 1)
        reset_match = re.search(
            r"\(\s*reset\s*=>\s*\((.+),\s*(.+)\)\s*\)\s*$",
            reset_text.strip(),
        )
        if reset_match:
            return name, type_text, clock_text.strip(), reset_match.group(1).strip(), reset_match.group(2).strip()
        return name, type_text, clock_text.strip(), None, None

    return name, type_text, rest.strip(), None, None


def _regreset_decl(body: str) -> tuple[str, str, str, str, str] | None:
    match = re.match(r"^\s*regreset\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$", body)
    if match is None:
        return None
    name = match.group(1)
    parts = _split_top_level_args(match.group(2))
    if len(parts) < 4:
        return None
    type_text, clock_text, reset_signal, reset_value = parts[0], parts[1], parts[2], ",".join(parts[3:])
    return name, type_text, clock_text, reset_signal, reset_value


def _leaf_names_for_type(root: str, type_: FirrtlType) -> tuple[str, ...]:
    leaves = flatten_type(
        type_,
        prefix=root,
        direction=PortDirection.INPUT,
        source=None,
    )
    return tuple(leaf.path for leaf in leaves)


def _relative_suffix(root: str, leaf: str) -> str:
    if leaf == root:
        return ""
    return leaf[len(root):]


def _root_for_signal(name: str, aggregate_leaves: Mapping[str, tuple[str, ...]]) -> str | None:
    candidates = [root for root in aggregate_leaves if _is_prefix(root, name)]
    if not candidates:
        return None
    return max(candidates, key=len)


def _expand_connect_pairs(
    dst: str,
    src: str,
    aggregate_leaves: Mapping[str, tuple[str, ...]],
) -> list[tuple[str, str]]:
    """Expand aggregate connects when leaf structure is known.

    If both roots are known, equal relative suffixes are paired. If only the
    destination is known, each destination leaf conservatively depends on the
    source aggregate. If neither is known, a scalar/root edge is emitted.
    """

    dst_root = _root_for_signal(dst, aggregate_leaves)
    src_root = _root_for_signal(src, aggregate_leaves)

    dst_is_root = dst in aggregate_leaves
    src_is_root = src in aggregate_leaves

    if dst_is_root and src_is_root:
        dst_by_suffix = {
            _relative_suffix(dst, leaf): leaf
            for leaf in aggregate_leaves[dst]
        }
        src_by_suffix = {
            _relative_suffix(src, leaf): leaf
            for leaf in aggregate_leaves[src]
        }
        common = sorted(set(dst_by_suffix) & set(src_by_suffix))
        if common:
            return [(dst_by_suffix[suffix], src_by_suffix[suffix]) for suffix in common]

    if dst_is_root:
        return [(leaf, src) for leaf in aggregate_leaves[dst]]

    # A connect to a known aggregate sub-prefix (for example io.bits) can be
    # expanded by selecting descendants underneath that prefix.
    dst_desc = [
        leaf
        for root, leaves in aggregate_leaves.items()
        if _is_prefix(root, dst) or _is_prefix(dst, root)
        for leaf in leaves
        if _is_prefix(dst, leaf)
    ]
    dst_desc = sorted(set(dst_desc))
    if dst_desc:
        if src_is_root:
            src_by_suffix = {
                _relative_suffix(src, leaf): leaf
                for leaf in aggregate_leaves[src]
            }
            pairs: list[tuple[str, str]] = []
            for leaf in dst_desc:
                suffix = leaf[len(dst):]
                matching = src_by_suffix.get(suffix)
                pairs.append((leaf, matching or src))
            return pairs
        return [(leaf, src) for leaf in dst_desc]

    return [(dst, src)]


def _type_contains_flip(type_: FirrtlType) -> bool:
    from .model import BundleType, VectorType
    if isinstance(type_, BundleType):
        return any(
            field.flipped or _type_contains_flip(field.type)
            for field in type_.fields
        )
    if isinstance(type_, VectorType):
        return _type_contains_flip(type_.element)
    return False


def _register_subaggregate_types(
    graph: ModuleDependencyGraph,
    prefix: str,
    type_: FirrtlType,
) -> None:
    from .model import BundleType, VectorType
    if isinstance(type_, BundleType):
        graph.aggregate_types[prefix] = type_
        for field in type_.fields:
            _register_subaggregate_types(
                graph,
                f"{prefix}.{field.name}",
                field.type,
            )
    elif isinstance(type_, VectorType):
        graph.aggregate_types[prefix] = type_
        for index in range(type_.size):
            _register_subaggregate_types(
                graph,
                f"{prefix}[{index}]",
                type_.element,
            )


def _register_aggregate(
    graph: ModuleDependencyGraph,
    root: str,
    type_text: str,
    kind: SignalKind,
    source: SourceLoc | None,
) -> None:
    try:
        type_ = parse_type(type_text)
    except Exception:
        graph.add_signal(
            SignalInfo(root, kind=kind, source=source, type_text=type_text)
        )
        return

    _register_subaggregate_types(graph, root, type_)
    leaves = _leaf_names_for_type(root, type_)
    graph.aggregate_leaves[root] = leaves
    graph.add_signal(
        SignalInfo(root, kind=kind, source=source, type_text=type_text)
    )
    for leaf in leaves:
        graph.add_signal(
            SignalInfo(
                name=leaf,
                kind=kind,
                source=source,
                type_text=None,
                aggregate_root=root,
            )
        )


def _add_expr_edges(
    graph: ModuleDependencyGraph,
    dst: str,
    deps: ExpressionDependencies,
    default_kind: DependencyKind,
    statement_ids: tuple[int, ...],
    source: SourceLoc | None,
    enclosing_controls: frozenset[str] = frozenset(),
) -> None:
    for ref in sorted(deps.data):
        graph.add_edge(
            DependencyEdge(ref, dst, default_kind, statement_ids, source)
        )
    for ref in sorted(deps.address):
        graph.add_edge(
            DependencyEdge(ref, dst, DependencyKind.ADDRESS, statement_ids, source)
        )
    for ref in sorted(deps.control | enclosing_controls):
        graph.add_edge(
            DependencyEdge(ref, dst, DependencyKind.CONTROL, statement_ids, source)
        )


def _module_body_lines(text: str, module_name: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    start: int | None = None
    module_indent: int | None = None

    for index, line in enumerate(lines):
        body, _ = _strip_trailing_source(line)
        match = _MODULE_START_RE.match(body)
        if match and match.group(1) == module_name:
            start = index + 1
            module_indent = _indent_of(line)
            break

    if start is None or module_indent is None:
        raise FirrtlParseError(f"Module {module_name!r} not found")

    out: list[tuple[int, str]] = []
    for index in range(start, len(lines)):
        line = lines[index]
        body, _ = _strip_trailing_source(line)
        match = _MODULE_START_RE.match(body)
        if match and _indent_of(line) <= module_indent:
            break
        out.append((index + 1, line))
    return out


def build_module_dependency_graph(
    text: str,
    design: Design,
    module_name: str,
) -> ModuleDependencyGraph:
    """Build a conservative signal-dependency graph from classic FIRRTL/CHIRRTL.

    Supported driving constructs in v5:
      * wire/node/reg/regreset
      * scalar and known aggregate connects
      * when/else control dependencies
      * cmem/smem + read/write/infer mport skeletons
      * source locators

    Unknown executable statements are retained as UNSUPPORTED ledger entries;
    they are never silently dropped from completeness accounting.
    """

    module = design.module(module_name)
    graph = ModuleDependencyGraph(module=module_name)
    graph.instance_modules = {inst.name: inst.module for inst in module.instances}

    # Register physical module ports and their aggregate shape.
    for port in module.ports:
        _register_aggregate(
            graph,
            root=port.name,
            type_text=_type_to_text(port.type),
            kind=SignalKind.PORT,
            source=port.source,
        )
        for leaf in flatten_type(port.type, port.name, port.direction, port.source):
            if leaf.direction is PortDirection.INPUT:
                graph.input_ports.add(leaf.path)
            else:
                graph.output_ports.add(leaf.path)

    # Register child instance port shapes so parent aggregate connects can be
    # lowered to leaf dependencies without guessing.
    for instance in module.instances:
        child = design.modules.get(instance.module)
        if child is None:
            continue
        for port in child.ports:
            root = f"{instance.name}.{port.name}"
            _register_aggregate(
                graph,
                root=root,
                type_text=_type_to_text(port.type),
                kind=SignalKind.INSTANCE_PORT,
                source=instance.source or port.source,
            )

    statement_id = 0
    active_blocks: list[_ControlBlock] = []
    last_when_at_indent: dict[int, _ControlBlock] = {}
    memory_mports: dict[str, tuple[str, str]] = {}

    def next_statement(
        *,
        line_number: int,
        indent: int,
        kind: str,
        text_body: str,
        source: SourceLoc | None,
        status: StatementStatus,
        drives: Iterable[str] = (),
        reads: Iterable[str] = (),
        control_reads: Iterable[str] = (),
        note: str | None = None,
    ) -> StatementRecord:
        nonlocal statement_id
        record = StatementRecord(
            id=statement_id,
            module=module_name,
            firrtl_line=line_number,
            indent=indent,
            kind=kind,
            text=text_body.strip(),
            source=source,
            status=status,
            drives=tuple(sorted(set(drives))),
            reads=tuple(sorted(set(reads))),
            control_reads=tuple(sorted(set(control_reads))),
            note=note,
        )
        graph.statements.append(record)
        statement_id += 1
        return record

    for line_number, raw_line in _module_body_lines(text, module_name):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(";"):
            continue

        body, source = _strip_trailing_source(raw_line)
        stripped_body = body.strip()
        indent = _indent_of(raw_line)

        # Drop finished control blocks before interpreting this statement. `else`
        # at the same indent can still retrieve the previous when from the map.
        while active_blocks and indent <= active_blocks[-1].indent:
            active_blocks.pop()

        if stripped_body.startswith(_METADATA_PREFIXES):
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="metadata",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.NONDRIVING,
            )
            continue

        # Port and instance declarations are already handled structurally.
        if _PORT_RE.match(body) or _INST_RE.match(body):
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="structural",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.NONDRIVING,
            )
            continue

        when_match = _WHEN_RE.match(body)
        if when_match:
            deps = extract_expression_dependencies(when_match.group(1))
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="when",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                reads=deps.all_refs,
                control_reads=deps.all_refs,
            )
            block = _ControlBlock(indent, deps.all_refs, record.id)
            active_blocks.append(block)
            last_when_at_indent[indent] = block
            continue

        if _ELSE_RE.match(body):
            previous = last_when_at_indent.get(indent)
            if previous is None:
                next_statement(
                    line_number=line_number,
                    indent=indent,
                    kind="else",
                    text_body=stripped_body,
                    source=source,
                    status=StatementStatus.UNSUPPORTED,
                    note="else without matching when at same indentation",
                )
                continue
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="else",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                reads=previous.condition_refs,
                control_reads=previous.condition_refs,
            )
            active_blocks.append(
                _ControlBlock(indent, previous.condition_refs, record.id)
            )
            continue

        enclosing_controls = frozenset(
            ref
            for block in active_blocks
            for ref in block.condition_refs
        )
        enclosing_statement_ids = tuple(block.statement_id for block in active_blocks)

        wire_match = _WIRE_RE.match(body)
        if wire_match:
            name, type_text = wire_match.groups()
            _register_aggregate(graph, name, type_text, SignalKind.WIRE, source)
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="wire",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(name,),
            )
            continue

        reg = _reg_decl(body)
        if reg is not None:
            name, type_text, clock_expr, reset_expr, reset_value = reg
            graph.register_roots.add(name)
            _register_aggregate(graph, name, type_text, SignalKind.REGISTER, source)
            clock_deps = extract_expression_dependencies(clock_expr)
            reset_signal_deps = (
                extract_expression_dependencies(reset_expr)
                if reset_expr is not None
                else ExpressionDependencies()
            )
            reset_value_deps = (
                extract_expression_dependencies(reset_value)
                if reset_value is not None
                else ExpressionDependencies()
            )
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="reg",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(name,),
                reads=clock_deps.all_refs | reset_signal_deps.all_refs | reset_value_deps.all_refs,
            )
            for ref in sorted(clock_deps.all_refs):
                graph.add_edge(
                    DependencyEdge(ref, name, DependencyKind.CLOCK, (record.id,), source)
                )
            for ref in sorted(reset_signal_deps.all_refs | reset_value_deps.all_refs):
                graph.add_edge(
                    DependencyEdge(ref, name, DependencyKind.RESET, (record.id,), source)
                )
            continue

        regreset = _regreset_decl(body)
        if regreset is not None:
            name, type_text, clock_expr, reset_expr, reset_value = regreset
            graph.register_roots.add(name)
            _register_aggregate(graph, name, type_text, SignalKind.REGISTER, source)
            clock_deps = extract_expression_dependencies(clock_expr)
            reset_deps = extract_expression_dependencies(reset_expr).merge(
                extract_expression_dependencies(reset_value)
            )
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="regreset",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(name,),
                reads=clock_deps.all_refs | reset_deps.all_refs,
            )
            for ref in sorted(clock_deps.all_refs):
                graph.add_edge(DependencyEdge(ref, name, DependencyKind.CLOCK, (record.id,), source))
            for ref in sorted(reset_deps.all_refs):
                graph.add_edge(DependencyEdge(ref, name, DependencyKind.RESET, (record.id,), source))
            continue

        node_match = _NODE_RE.match(body)
        if node_match:
            name, expr = node_match.groups()
            deps = extract_expression_dependencies(expr)
            graph.add_signal(SignalInfo(name, SignalKind.NODE, source=source))
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="node",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(name,),
                reads=deps.all_refs,
                control_reads=deps.control,
            )
            _add_expr_edges(
                graph,
                name,
                deps,
                DependencyKind.DATA,
                (record.id,) + enclosing_statement_ids,
                source,
                enclosing_controls,
            )
            continue

        cmem_match = _CMEM_RE.match(body)
        if cmem_match:
            _, name, type_text = cmem_match.groups()
            graph.memory_roots.add(name)
            _register_aggregate(graph, name, type_text, SignalKind.MEMORY, source)
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="memory",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(name,),
            )
            continue

        mport_match = _MPORT_RE.match(body)
        if mport_match:
            direction, port_name, memory_name, address_expr, clock_expr = mport_match.groups()
            graph.add_signal(SignalInfo(port_name, SignalKind.MEMORY_PORT, source=source))
            memory_mports[port_name] = (direction, memory_name)
            addr_deps = extract_expression_dependencies(address_expr)
            clock_deps = extract_expression_dependencies(clock_expr)
            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind=f"{direction}_mport",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(port_name,),
                reads=addr_deps.all_refs | clock_deps.all_refs | {memory_name},
                control_reads=enclosing_controls,
            )
            # Reads depend on memory state and address; write ports are treated as
            # a state update handle and their subsequent connects carry data.
            if direction in {"read", "infer"}:
                graph.add_edge(DependencyEdge(memory_name, port_name, DependencyKind.MEMORY, (record.id,), source))
            for ref in sorted(addr_deps.all_refs):
                graph.add_edge(DependencyEdge(ref, port_name, DependencyKind.ADDRESS, (record.id,), source))
            for ref in sorted(clock_deps.all_refs):
                graph.add_edge(DependencyEdge(ref, port_name, DependencyKind.CLOCK, (record.id,), source))
            for ref in sorted(enclosing_controls):
                graph.add_edge(DependencyEdge(ref, port_name, DependencyKind.CONTROL, (record.id,) + enclosing_statement_ids, source))
            continue

        invalid_match = _INVALID_RE.match(body)
        if invalid_match:
            dst, _ = _canonicalize_reference(invalid_match.group(1).strip())
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="invalidate",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=(dst,),
                control_reads=enclosing_controls,
            )
            continue

        connect_match = _CONNECT_RE.match(body)
        if connect_match:
            raw_dst, connect_op, expr = connect_match.groups()
            dst, dst_index_refs = _canonicalize_reference(raw_dst.strip())
            deps = extract_expression_dependencies(expr)
            # Destination subaccess index controls which storage element is written.
            deps = ExpressionDependencies(
                data=deps.data,
                control=deps.control,
                address=deps.address | frozenset(dst_index_refs),
            )

            # Direct aggregate reference on RHS can be expanded against a known
            # aggregate destination. More complex aggregate expressions fall back
            # to conservative root dependencies.
            direct_src_match = re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*|\[[^\[\]]+\])*",
                expr.strip(),
            )
            direct_src = None
            if direct_src_match:
                direct_src, _ = _canonicalize_reference(expr.strip())

            # Aggregate connect flow can reverse through flipped fields. v5
            # handles passive aggregates but refuses to guess bidirectional
            # aggregate flow until a full FIRRTL flow adapter is implemented.
            dst_type = graph.aggregate_types.get(dst)
            src_type = graph.aggregate_types.get(direct_src) if direct_src is not None else None
            if (
                direct_src is not None
                and (
                    (dst_type is not None and _type_contains_flip(dst_type))
                    or (src_type is not None and _type_contains_flip(src_type))
                )
            ):
                next_statement(
                    line_number=line_number,
                    indent=indent,
                    kind="aggregate_connect_with_flips",
                    text_body=stripped_body,
                    source=source,
                    status=StatementStatus.UNSUPPORTED,
                    note=(
                        "aggregate connect contains flipped fields; v5 refuses "
                        "to approximate FIRRTL bidirectional flow"
                    ),
                )
                continue

            pairs = (
                _expand_connect_pairs(dst, direct_src, graph.aggregate_leaves)
                if direct_src is not None
                else [(dst, None)]
            )
            drives = [pair[0] for pair in pairs]

            record = next_statement(
                line_number=line_number,
                indent=indent,
                kind="connect",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.SUPPORTED,
                drives=drives,
                reads=deps.all_refs,
                control_reads=deps.control | enclosing_controls,
            )

            for leaf_dst, leaf_src in pairs:
                default_kind = (
                    DependencyKind.STATE
                    if graph.is_register(leaf_dst)
                    else DependencyKind.DATA
                )

                if leaf_src is not None:
                    graph.add_edge(
                        DependencyEdge(
                            leaf_src,
                            leaf_dst,
                            default_kind,
                            (record.id,) + enclosing_statement_ids,
                            source,
                        )
                    )
                    for ref in sorted(enclosing_controls | deps.address | deps.control):
                        kind = DependencyKind.ADDRESS if ref in deps.address else DependencyKind.CONTROL
                        graph.add_edge(
                            DependencyEdge(
                                ref,
                                leaf_dst,
                                kind,
                                (record.id,) + enclosing_statement_ids,
                                source,
                            )
                        )
                else:
                    _add_expr_edges(
                        graph,
                        leaf_dst,
                        deps,
                        default_kind,
                        (record.id,) + enclosing_statement_ids,
                        source,
                        enclosing_controls,
                    )

                # A write/infer mport assignment updates memory state.
                port_root = leaf_dst.split(".", 1)[0].split("[", 1)[0]
                if port_root in memory_mports:
                    direction, memory_name = memory_mports[port_root]
                    if direction in {"write", "infer"}:
                        graph.add_edge(
                            DependencyEdge(
                                leaf_dst,
                                memory_name,
                                DependencyKind.STATE,
                                (record.id,) + enclosing_statement_ids,
                                source,
                            )
                        )
            continue

        if stripped_body.startswith(_NONDRIVING_PREFIXES):
            next_statement(
                line_number=line_number,
                indent=indent,
                kind="nondriving",
                text_body=stripped_body,
                source=source,
                status=StatementStatus.NONDRIVING,
            )
            continue

        # Memory attribute blocks from lowered FIRRTL are not supported by this
        # CHIRRTL-oriented parser, but are kept visible in the ledger. Likewise
        # any unknown executable syntax is fail-closed rather than ignored.
        next_statement(
            line_number=line_number,
            indent=indent,
            kind="unknown",
            text_body=stripped_body,
            source=source,
            status=StatementStatus.UNSUPPORTED,
            note="unrecognized potentially dependency-bearing FIRRTL statement",
        )

    _add_wildcard_alias_edges(graph)
    return graph


def build_all_dependency_graphs(
    text: str,
    design: Design,
) -> dict[str, ModuleDependencyGraph]:
    return {
        name: build_module_dependency_graph(text, design, name)
        for name, module in design.modules.items()
        if not module.external
    }


def _add_wildcard_alias_edges(graph: ModuleDependencyGraph) -> None:
    """Conservatively connect wildcard dynamic subaccesses to seen static lanes."""
    names = set(graph.signals)
    wildcard_names = [name for name in names if "[*]" in name]
    for wildcard in wildcard_names:
        pattern = re.escape(wildcard).replace(re.escape("[*]"), r"\[[0-9]+\]")
        regex = re.compile(rf"^{pattern}$")
        for candidate in names:
            if regex.match(candidate):
                graph.add_edge(
                    DependencyEdge(
                        candidate,
                        wildcard,
                        DependencyKind.ALIAS,
                        (),
                        graph.signals.get(candidate, SignalInfo(candidate, SignalKind.UNKNOWN)).source,
                    )
                )
                graph.add_edge(
                    DependencyEdge(
                        wildcard,
                        candidate,
                        DependencyKind.ALIAS,
                        (),
                        graph.signals.get(candidate, SignalInfo(candidate, SignalKind.UNKNOWN)).source,
                    )
                )


def _type_to_text(type_: FirrtlType) -> str:
    if isinstance(type_, GroundType):
        return str(type_)
    from .model import BundleType, VectorType
    if isinstance(type_, BundleType):
        fields = []
        for field in type_.fields:
            prefix = "flip " if field.flipped else ""
            fields.append(f"{prefix}{field.name} : {_type_to_text(field.type)}")
        return "{ " + ", ".join(fields) + " }"
    if isinstance(type_, VectorType):
        return f"{_type_to_text(type_.element)}[{type_.size}]"
    raise TypeError(type(type_))
