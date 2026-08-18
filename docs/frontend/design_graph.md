# `frontend/design_graph.py`

## 文件职责

把 module-local dependency graph **实例化并跨层连接**成 concrete design dependency graph。

这是 v5 支持真正 hierarchical slice 的关键。

例如 parent 中：

```text
prober.io.rep.valid
```

与 child `BoomProbeUnit` 内部：

```text
io.rep.valid
```

在 concrete instance `DCacheTop.prober` 下会映射到同一个 flat signal：

```text
DCacheTop.prober::io.rep.valid
```

因此 backward slice 可以从顶层 TileLink C 一直穿过 instance boundary 进入 ProbeUnit FSM。

## `FlatSignalInfo`

保存 concrete signal id、instance path、module、local name、kind 和 source。

## `FlatStatementRef`

一条 dependency edge 可能来自某个 module 的 statement。该类把 statement id 和 concrete instance path 绑定。

## `FlatDependencyEdge`

跨层 dependency edge。

## `DesignDependencyGraph`

保存：

- concrete flat signals；
- flat edges；
- instance path 到 module 的映射；
- top-level inputs；
- 原 module graphs。

## `DesignEventOccurrence`

物理 event 的 concrete occurrence，例如：

```text
DCacheTop.prober::io.rep.fire
```

而不是只有 module type 级别的：

```text
BoomProbeUnit.io.rep.fire
```

### `seeds()`

返回 instance-specific valid/ready，必要时加 payload。

## `DesignSliceResult`

包含跨层 slice 的 signals、edges、instances、frontier、source spans。

### `incomplete_instances`

如果 slice 触达某个 concrete instance，而它对应的 module graph 有 unsupported statement，则把 instance path 记录在这里。

### `complete`

要求：

```text
未截断
AND
没有 touched incomplete instance
```

## `flatten_design_dependency_graph()`

递归实例化 module graph。

关键规则：

> parent instance-port reference 和 child local port 共用同一个 flat ID。

当两者都存在时，优先保留 child `PORT` 的更精确 kind/source locator。

## `discover_design_events()`

把每个 module type 的物理 handshake event 实例化成 concrete design event。

它不会把 parent/child 两端擅自声明为“同一个语义事件”；是否存在 gate/arbiter 仍由 dependency graph 保留。

## `backward_design_slice()`

在 flattened graph 上做跨模块 backward fixed point。

默认在 top-level input 停止，得到整个研究子系统对外的物理 frontier。
