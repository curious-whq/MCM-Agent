# `workflow/handoff.py`

## 文件职责

把一个已完成静态 ownership 的 `HierarchicalWorkUnit` 转成自包含 semantic task input。当前：

```text
HANDOFF_SCHEMA_VERSION = workunit-static-0.4
PLANNER_VERSION        = hierarchical-planner-v14
```

`build_work_unit_static_handoff()` 只接受 `coverage.complete == true` 的 WorkUnit。

## Handoff 内容

包含：

- WorkUnit identity / decision；
- raw 与 replacement complexity；
- parent-local physical events；
- concrete state / memory state / frontier；
- parent child summary slots；
- parent-local FIRRTL statements 与 dependency edges；
- historical/immediate semantic event cones；
- source spans 与可选 resolved source snippets；
- grounding allowlists。

parent 的 source span 会从 **当前 handoff 可见的 statements** 重新计算，防止父层 synthesis 通过 source evidence 重新引入 child internals。

Handoff 阶段不创造 semantic occurrence 名、case 或 µMCM axiom；它只是 deterministic grounding boundary。
