# `frontend/design_graph.py`

## 文件职责

把 module-local dependency 绑定到 concrete instance hierarchy，使分析能够真正跨：

```text
LSQ / LSU
↔ L1 DCache
↔ TileLink interconnect
↔ InclusiveCache L2
```

## Concrete signal identity

parent instance-port 与 child local port 映射到同一个 flat signal ID。

例如：

```text
parent: prober.io.rep.valid
child:  io.rep.valid
```

统一成：

```text
...dcache.prober::io.rep.valid
```

因此跨 module 不需要 LLM 猜 connector。

## `DesignDependencyGraph`

保存 concrete signals、edges、instances、top inputs 和已经 materialize 的 module graphs。

## `DesignEventOccurrence`

把 module-type event 实例化，例如：

```text
...dcache.prober::io.req.fire
```

仍然只表示物理 occurrence，不表示语义 transaction identity。

## `DesignSliceResult`

跨层 backward slice，带：

```text
signals
edges
instances
frontier
source spans
incomplete instances
truncated
```

`complete` 要求既未截断，也没有碰到 incomplete module。

## `backward_design_slice()`

适合已经 materialize 的中小设计。

## `ModuleGraphProvider` + `backward_design_slice_lazy()`

v6 对完整 Chipyard 采用 lazy traversal：只有 slice 真正进入某个 concrete instance 时才构建其 module graph。

这避免一开始实例化 1,800+ module definition 的全部 dependency。

## `InstanceHierarchyIndex`

预先恢复：

```text
instance path -> module
instance -> parent
parent -> children
```

lazy traversal 据此知道什么时候跨入 child module。

## `DependencyPath`

表示两个 concrete signals 之间的一条机械 dependency path。

字段包括：

```text
source / target
edges
instances
source spans
incomplete instances
visited_signals
truncated
```

`complete` 只有在：

```text
path found
AND no incomplete instance
AND not truncated
```

时成立。

## `LazyDesignExplorer`

这是 v6 为完整 Chipyard 增加的 path-oriented explorer。

它维护一个逐步 materialize 的 flat graph，并提供 `find_path()`。

显式搜索模式：

- `forward`
- `reverse`
- `auto`

`auto` 是 lazy bidirectional BFS，主要用于诊断；handshake transport 还会利用 hierarchy depth 从更接近 interconnect 的一侧搜索，以避免过早进入 BOOM core 的高 fan-in/fan-out cone。

## 为什么 path 和 cone 要分开

真实 `TL-B.fire` 的完整 occurrence cone 如果同时从 valid/ready 做 union backward fixed point，会沿 ready/control 进入非常大的 core 状态空间。

但“L2 的 B channel 是否物理到达 ProbeUnit”只需要证明一条 transport path。

因此 v6 明确区分：

$$
\text{Transport Path} \neq \text{Semantic Event Cone}
$$

前者用于 hierarchy/connector grounding；后者用于后续 case extraction。两者都保留 source locator 和 coverage 信息。

## `backward_instance_slice_lazy()`

v6 在真实 Chipyard 集成后增加的 ownership-scoped semantic cone。

输入一个 concrete event，并指定可选的 `root_instance`。默认 root 就是事件自己的 concrete instance。

算法允许：

```text
root instance
→ owned child
→ owned grandchild
```

但把 root module 的 physical input leaves 当作 frontier，因此不会向 parent/environment 继续扩张。

例如：

```text
root = ...dcache.prober
```

得到 ProbeUnit 自身 FSM cone；而：

```text
root = ...dcache
```

可以进入 ProbeUnit、MSHRFile、Writeback 等 DCache-owned children，但不会进入整个 BOOM core。

这和 whole-design `backward_design_slice_lazy()` 的区别是：

$$
\text{Instance Subtree Cone}
=
\text{Semantic Cone constrained by physical ownership}
$$

它不是为了丢掉 dependency，而是把 parent-side dependency 显式变成模块 boundary frontier，正好对应后续递归 µMCM abstraction 的 parent/child 边界。

`max_signals` 耗尽时仍 fail closed：`truncated=true`，不能进入 pre-LLM handoff。
