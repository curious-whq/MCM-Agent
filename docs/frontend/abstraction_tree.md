# `frontend/abstraction_tree.py`

## 文件职责

把两种静态信息合成一个后续 Agent 可直接消费的**候选 abstraction tree**：

```text
真实 physical instance hierarchy
+
module 内 register-SCC/event-cone partition
```

主层次始终来自 elaborated design 的 module instance tree；SCC 只作为大模块内部的静态叶级 work unit。

## `AbstractionNodeKind`

### `MODULE`

真实 module instance。

### `STATE_REGION`

register dependency SCC。

### `COMBINATIONAL_EVENT_CONE`

某个 physical event 没有触达 register 时，用纯组合 event cone 作为 work unit。

## `AbstractionNode`

保存：

```text
id
kind
instance_path
module
registers
event_ids
source
children
```

节点名称全部结构化生成，不在静态阶段出现“load ordering engine”“probe controller”等语义命名。

## `AbstractionTree`

只保存 root `AbstractionNode`。

## `_concrete_event_id()`

把 module-type event：

```text
BoomProbeUnit.io.rep.fire
```

实例化成：

```text
DCacheTop.prober::io.rep.fire
```

## `build_abstraction_tree()`

递归过程：

1. 从 design top 建真实 module instance node；
2. 对可分析 module 调用 `discover_partition_plan()`；
3. 把 register SCC 作为 `STATE_REGION` child；
4. 把没有状态的 event cone 作为 `COMBINATIONAL_EVENT_CONE` child；
5. 再挂真实 child module instances。

这棵树是后续“按层生成 leaf case / parent summary”的**静态任务骨架**，不是已经证明正确的语义模块分解。

## `abstraction_tree_dict()`

导出 JSON-ready tree，便于 CLI、后续调度器和实验统计使用。
