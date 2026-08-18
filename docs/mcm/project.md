# `mcm/project.py`

## 文件职责

把普通 ordering case 从内部事件图投影到父模块 boundary。

核心流程：

```text
transitive closure
→ remove internal endpoints
→ transitive reduction
```

## `_transitive_closure`

若有：

$$
A < B
$$

和：

$$
B < C
$$

则补出：

$$
A < C
$$

v1.1 后图节点是 `EventRef`，因此 occurrence identity 会随 ordering 一起保留。

## `_transitive_reduction_dag`

删除可由其它边推出的冗余 ordering，并拒绝严格顺序 cycle。

## `project_case`

输入一个 `Case` 和 boundary event 集合，输出只含 boundary ordering 的新 `Case`。

guard 在当前版本中不会被这里抽象。
