# `frontend/hierarchy.py`

## 文件职责

从 FIRRTL 的 `module` 和 `inst ... of ...` 自动恢复 concrete instance tree。

整个过程完全静态，不使用 LLM。

## `HierarchyNode`

保存：

```text
path
module
instance_name
source
external
children
```

例如：

```text
ProbeHarness
└── ProbeHarness.probe : BoomProbeUnit
```

## `discover_hierarchy()`

从 circuit top 开始递归展开实例。

行为：

- 已定义的普通 module：继续展开；
- `extmodule`：作为 external leaf；
- 未解析到 definition 的 module target：保守视为 external leaf；
- 发现递归 module cycle：直接报错。

这里得到的是**物理设计层次**，不是由 LLM 推测的逻辑分组。
