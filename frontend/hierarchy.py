from __future__ import annotations

from dataclasses import dataclass

from .model import Design, SourceLoc


@dataclass(frozen=True)
class HierarchyNode:
    path: str
    module: str
    instance_name: str | None
    source: SourceLoc | None
    external: bool
    children: tuple["HierarchyNode", ...] = ()


def discover_hierarchy(
    design: Design,
    top: str | None = None,
) -> HierarchyNode:
    """Build a concrete instance tree from FIRRTL module/instance structure."""

    root_module = top or design.top

    if root_module not in design.modules:
        raise KeyError(f"Unknown hierarchy root module: {root_module}")

    def build(
        module_name: str,
        path: str,
        instance_name: str | None,
        source: SourceLoc | None,
        stack: tuple[str, ...],
    ) -> HierarchyNode:
        if module_name in stack:
            cycle = " -> ".join(stack + (module_name,))
            raise ValueError(f"Recursive module hierarchy detected: {cycle}")

        module = design.modules.get(module_name)
        if module is None:
            # An unresolved target is treated conservatively as an external leaf.
            return HierarchyNode(
                path=path,
                module=module_name,
                instance_name=instance_name,
                source=source,
                external=True,
                children=(),
            )

        if module.external:
            return HierarchyNode(
                path=path,
                module=module_name,
                instance_name=instance_name,
                source=source or module.source,
                external=True,
                children=(),
            )

        children = tuple(
            build(
                module_name=instance.module,
                path=f"{path}.{instance.name}",
                instance_name=instance.name,
                source=instance.source,
                stack=stack + (module_name,),
            )
            for instance in module.instances
        )

        return HierarchyNode(
            path=path,
            module=module_name,
            instance_name=instance_name,
            source=source or module.source,
            external=False,
            children=children,
        )

    root_def = design.module(root_module)
    return build(
        module_name=root_module,
        path=root_module,
        instance_name=None,
        source=root_def.source,
        stack=(),
    )
