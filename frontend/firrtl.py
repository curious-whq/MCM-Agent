from __future__ import annotations

import re
from dataclasses import dataclass

from .model import (
    BundleField,
    BundleType,
    Design,
    FirrtlType,
    GroundType,
    Instance,
    ModuleDef,
    Port,
    PortDirection,
    SourceLoc,
    VectorType,
)


_TOKEN_RE = re.compile(
    r"""
    [A-Za-z_.$][A-Za-z0-9_.$]* |
    \d+ |
    \? |
    [{}\[\]:,<>\(\)]
    """,
    re.VERBOSE,
)


class FirrtlParseError(ValueError):
    pass


@dataclass
class _TypeParser:
    tokens: list[str]
    index: int = 0

    @staticmethod
    def from_text(text: str) -> "_TypeParser":
        tokens = _TOKEN_RE.findall(text)
        if not tokens:
            raise FirrtlParseError(f"Empty FIRRTL type: {text!r}")
        return _TypeParser(tokens)

    def peek(self) -> str | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def pop(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None:
            raise FirrtlParseError("Unexpected end of FIRRTL type")
        if expected is not None and token != expected:
            raise FirrtlParseError(
                f"Expected token {expected!r}, got {token!r}"
            )
        self.index += 1
        return token

    def parse(self) -> FirrtlType:
        type_ = self.parse_atom()

        while self.peek() == "[":
            self.pop("[")
            size_text = self.pop()
            self.pop("]")
            try:
                size = int(size_text)
            except ValueError as exc:
                raise FirrtlParseError(
                    f"Vector size must be an integer, got {size_text!r}"
                ) from exc
            type_ = VectorType(type_, size)

        return type_

    def parse_atom(self) -> FirrtlType:
        if self.peek() == "{":
            return self.parse_bundle()

        name = self.pop()
        width: str | None = None

        if self.peek() == "<":
            self.pop("<")
            parts: list[str] = []
            depth = 1
            while depth:
                token = self.pop()
                if token == "<":
                    depth += 1
                elif token == ">":
                    depth -= 1
                    if depth == 0:
                        break
                parts.append(token)
            width = "".join(parts)

        return GroundType(name=name, width=width)

    def parse_bundle(self) -> BundleType:
        self.pop("{")
        fields: list[BundleField] = []

        while self.peek() != "}":
            flipped = False
            if self.peek() == "flip":
                self.pop("flip")
                flipped = True

            name = self.pop()
            self.pop(":")
            field_type = self.parse()
            fields.append(
                BundleField(
                    name=name,
                    type=field_type,
                    flipped=flipped,
                )
            )

            if self.peek() == ",":
                self.pop(",")
            elif self.peek() != "}":
                raise FirrtlParseError(
                    f"Expected ',' or '}}', got {self.peek()!r}"
                )

        self.pop("}")
        return BundleType(tuple(fields))


def parse_type(text: str) -> FirrtlType:
    parser = _TypeParser.from_text(text)
    type_ = parser.parse()
    if parser.peek() is not None:
        raise FirrtlParseError(
            f"Unexpected trailing FIRRTL type tokens: "
            f"{parser.tokens[parser.index:]}"
        )
    return type_


_SOURCE_RE = re.compile(r"\s+@\[(.*)\]\s*$")


def _split_source(text: str) -> tuple[str, SourceLoc | None]:
    match = _SOURCE_RE.search(text)
    if match is None:
        return text.rstrip(), None
    source = SourceLoc.parse(match.group(1))
    return text[:match.start()].rstrip(), source


_CIRCUIT_RE = re.compile(
    r"^\s*circuit\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:"
)
_MODULE_RE = re.compile(
    r"^\s*(?:(?:public|private)\s+)?(module|extmodule)\s+"
    r"([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:"
)
_PORT_RE = re.compile(
    r"^\s*(input|output)\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.+)$"
)
_INST_RE = re.compile(
    r"^\s*inst\s+([A-Za-z_.$][A-Za-z0-9_.$]*)\s+of\s+"
    r"([A-Za-z_.$][A-Za-z0-9_.$]*)\s*$"
)


def parse_firrtl(text: str) -> Design:
    """Parse the structural subset of classic textual FIRRTL/CHIRRTL.

    v4 intentionally extracts only:
      * circuit/top
      * modules/extmodules
      * ports and aggregate directions
      * instances
      * source locators

    Other statements are ignored for now; dependency slicing is a later phase.
    """

    top: str | None = None
    circuit_source: SourceLoc | None = None

    modules: dict[str, ModuleDef] = {}

    current_name: str | None = None
    current_source: SourceLoc | None = None
    current_external = False
    current_ports: list[Port] = []
    current_instances: list[Instance] = []

    def finish_module() -> None:
        nonlocal current_name, current_source, current_external
        nonlocal current_ports, current_instances

        if current_name is None:
            return

        if current_name in modules:
            raise FirrtlParseError(f"Duplicate module: {current_name}")

        modules[current_name] = ModuleDef(
            name=current_name,
            ports=tuple(current_ports),
            instances=tuple(current_instances),
            source=current_source,
            external=current_external,
        )

        current_name = None
        current_source = None
        current_external = False
        current_ports = []
        current_instances = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(";"):
            continue

        body, source = _split_source(raw_line)

        circuit_match = _CIRCUIT_RE.match(body)
        if circuit_match:
            if top is not None:
                raise FirrtlParseError("Multiple circuit declarations")
            top = circuit_match.group(1)
            circuit_source = source
            continue

        module_match = _MODULE_RE.match(body)
        if module_match:
            finish_module()
            current_external = module_match.group(1) == "extmodule"
            current_name = module_match.group(2)
            current_source = source
            continue

        if current_name is None:
            # Ignore non-structural text outside a module.
            continue

        port_match = _PORT_RE.match(body)
        if port_match:
            direction = PortDirection(port_match.group(1))
            port_name = port_match.group(2)
            type_text = port_match.group(3)
            try:
                type_ = parse_type(type_text)
            except FirrtlParseError as exc:
                raise FirrtlParseError(
                    f"Line {line_number}: invalid port {port_name}: {exc}"
                ) from exc
            current_ports.append(
                Port(
                    name=port_name,
                    direction=direction,
                    type=type_,
                    source=source,
                )
            )
            continue

        inst_match = _INST_RE.match(body)
        if inst_match:
            current_instances.append(
                Instance(
                    name=inst_match.group(1),
                    module=inst_match.group(2),
                    source=source,
                )
            )
            continue

        # All other FIRRTL statements are intentionally ignored by v4.

    finish_module()

    if top is None:
        raise FirrtlParseError("No circuit declaration found")
    if top not in modules:
        raise FirrtlParseError(
            f"Circuit top {top!r} has no matching module declaration"
        )

    return Design(
        top=top,
        modules=modules,
        source=circuit_source,
    )
