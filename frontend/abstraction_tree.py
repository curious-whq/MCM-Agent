from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .dependency import ModuleDependencyGraph
from .model import Design, SourceLoc
from .partition import PartitionPlan, discover_partition_plan
from .registry import EventRegistry


class AbstractionNodeKind(str, Enum):
    MODULE = "module"
    STATE_REGION = "state_region"
    COMBINATIONAL_EVENT_CONE = "combinational_event_cone"


@dataclass(frozen=True)
class AbstractionNode:
    """A purely structural candidate node for later hierarchical abstraction."""

    id: str
    kind: AbstractionNodeKind
    instance_path: str
    module: str
    registers: tuple[str, ...] = ()
    event_ids: tuple[str, ...] = ()
    source: SourceLoc | None = None
    children: tuple["AbstractionNode", ...] = ()


@dataclass(frozen=True)
class AbstractionTree:
    root: AbstractionNode


def _concrete_event_id(
    module_name: str,
    instance_path: str,
    local_event_id: str,
) -> str:
    prefix = module_name + "."
    if not local_event_id.startswith(prefix):
        return f"{instance_path}::{local_event_id}"
    return f"{instance_path}::{local_event_id[len(prefix):]}"


def build_abstraction_tree(
    design: Design,
    graphs: dict[str, ModuleDependencyGraph],
    registries: dict[str, EventRegistry],
) -> AbstractionTree:
    """Combine physical hierarchy with module-local state partitions.

    Physical module instances are always primary nodes. Within each analyzable
    module, register-SCC regions are attached as structural leaf work units.
    Physical events that touch no register get a combinational event-cone leaf.

    No semantic names such as "load ordering engine" are assigned here.
    """

    def build_module(
        module_name: str,
        instance_path: str,
        source: SourceLoc | None,
        stack: tuple[str, ...],
    ) -> AbstractionNode:
        if module_name in stack:
            raise ValueError(
                "Recursive module hierarchy detected: "
                + " -> ".join(stack + (module_name,))
            )

        module = design.modules.get(module_name)
        if module is None or module.external:
            return AbstractionNode(
                id=instance_path,
                kind=AbstractionNodeKind.MODULE,
                instance_path=instance_path,
                module=module_name,
                source=source,
            )

        local_children: list[AbstractionNode] = []
        graph = graphs.get(module_name)
        registry = registries.get(module_name)

        if graph is not None and registry is not None:
            plan = discover_partition_plan(graph, registry)
            touched_events: set[str] = set()

            for region in plan.regions:
                concrete_events = tuple(
                    sorted(
                        _concrete_event_id(
                            module_name,
                            instance_path,
                            event_id,
                        )
                        for event_id in region.event_ids
                    )
                )
                touched_events.update(region.event_ids)
                local_children.append(
                    AbstractionNode(
                        id=f"{instance_path}::{region.id}",
                        kind=AbstractionNodeKind.STATE_REGION,
                        instance_path=instance_path,
                        module=module_name,
                        registers=region.registers,
                        event_ids=concrete_events,
                        source=module.source,
                    )
                )

            for cone in plan.event_cones:
                if cone.event_id in touched_events or cone.registers:
                    continue
                concrete_event = _concrete_event_id(
                    module_name,
                    instance_path,
                    cone.event_id,
                )
                local_children.append(
                    AbstractionNode(
                        id=f"{instance_path}::event-cone:{cone.event_id}",
                        kind=AbstractionNodeKind.COMBINATIONAL_EVENT_CONE,
                        instance_path=instance_path,
                        module=module_name,
                        event_ids=(concrete_event,),
                        source=module.source,
                    )
                )

        module_children = [
            build_module(
                instance.module,
                f"{instance_path}.{instance.name}",
                instance.source,
                stack + (module_name,),
            )
            for instance in module.instances
        ]

        return AbstractionNode(
            id=instance_path,
            kind=AbstractionNodeKind.MODULE,
            instance_path=instance_path,
            module=module_name,
            source=source or module.source,
            children=tuple(
                sorted(
                    local_children + module_children,
                    key=lambda node: (node.kind.value, node.id),
                )
            ),
        )

    top = design.module(design.top)
    return AbstractionTree(
        root=build_module(
            design.top,
            design.top,
            top.source,
            (),
        )
    )


def abstraction_tree_dict(tree: AbstractionTree) -> dict:
    def encode(node: AbstractionNode) -> dict:
        return {
            "id": node.id,
            "kind": node.kind.value,
            "instance_path": node.instance_path,
            "module": node.module,
            "registers": list(node.registers),
            "event_ids": list(node.event_ids),
            "source": (
                {
                    "file": node.source.file,
                    "line": node.source.line,
                    "column": node.source.column,
                }
                if node.source is not None
                else None
            ),
            "children": [encode(child) for child in node.children],
        }

    return encode(tree.root)
