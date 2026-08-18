# `frontend/partition.py`

## 文件职责

为“大 module 如何进一步分层”生成**纯静态候选 partition plan**。

它不使用 LLM 给区域命名，也不声称 SCC 就是最终语义模块。

当前规则：

```text
register dependency
      ↓
state SCC
      +
每个 physical event 的 backward cone
      ↓
候选 state regions
```

## `EventCone`

保存某个 event 的：

- touched registers；
- all sliced signals；
- static completeness。

## `StateRegion`

一个 register-dependency SCC，以及触达这个 SCC 的 physical events。

## `PartitionPlan`

一个 module 的整体候选分区：

```text
register_dependencies
regions
event_cones
```

## `register_dependency_edges()`

从完整 dependency graph 反向穿过组合节点，把状态 dependency 压缩成：

$$
Reg_i \rightarrow Reg_j
$$

遇到上游 register 后停止，因此得到直接 state dependency，而不是把组合细节保留进状态图。

## `_tarjan_scc()`

标准 Tarjan SCC，用于找强耦合状态组。

## `discover_partition_plan()`

执行：

1. register dependency collapse；
2. SCC；
3. 对每个 physical event 做 `FULL` slice；
4. 统计 event cone 触达哪些 register；
5. 把 event 关联到对应 SCC。

输出只是一棵后续 abstraction hierarchy 的候选骨架。
