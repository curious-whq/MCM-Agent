# `frontend/pipeline.py`

## 文件职责

统一编排 LLM 之前的 deterministic static frontend。

## `StaticFrontend.from_firrtl()`

执行：

```text
input contract
→ structural parse
→ physical registries
→ eager or lazy dependency provider
```

对小 fixture 默认 eager；CLI 对大于阈值的 whole-system FIRRTL 自动用 lazy mode。

## `graph(module_name)`

在 lazy mode 下按需 materialize 一个 module dependency graph，并缓存。

## `report()` / `assert_complete()`

提供 fail-closed coverage gate。

完整设计时推荐 `report --module` 只先检查研究相关 module，避免无意义地把所有外设一次构图。

## Local API

- `event()`
- `slice_event()`
- `slice_manifest()`
- `partition()`

处理 module-type 级 work unit。

## Whole-design API

- `design_events()` / `design_event()`
- `design_graph()`
- `design_connectors()`
- `slice_design_event()`
- `design_slice_manifest()`

其中 `design_graph()` / 全量 `design_connectors()` 仍可能 materialize 整个设计，适合小设计或离线全量任务。

## `handshake_transport()`

v6 新增的 whole-design 大规模首选连接 API。

输入两个 concrete event id：

```text
SEND endpoint
RECEIVE endpoint
```

输出 `HandshakeTransportPath`。

它不需要完整 flattened design，只对真实路径上的 module 做 lazy materialization，因此可以用于 69 MiB、1,800+ module definition 的 Chipyard FIRRTL。

## 为什么不把 route 合并进 slice

`slice_design_event()` 支持 `max_signals` fail-closed budget；CLI 对 whole-system semantic cone 默认给出有限预算，避免大设计无界展开。

`slice_design_event()` 回答：

> 哪些状态/控制/数据可以影响这个 event？

`handshake_transport()` 回答：

> 这个 physical channel 通过哪些模块从 A 到 B？

前者是 semantic cone，后者是 hierarchy connector evidence。真实 BOOM 中二者规模差异非常大，因此必须保持独立 primitive。

## LLM 边界

本文件仍不调用 LLM。

只有静态 coverage、source provenance、slice/route 完整性达到要求后，才允许构造未来的 semantic handoff。

## Ownership-scoped API

v6 真实 SoC 集成新增：

- `slice_instance_event()`
- `instance_slice_manifest()`

它们调用 `backward_instance_slice_lazy()`，对一个 concrete ownership subtree 生成 semantic cone。

推荐的大设计分析顺序是：

```text
handshake_transport()
  固定远端 physical connector

slice_instance_event()
  恢复一个 ownership subtree 内的完整状态/控制语义

slice_event()
  继续细分到 module-type local work unit
```

只有确实需要跨越 ownership root 的 semantic question，才调用 whole-design `slice_design_event()`。

这样静态阶段同时保证：

```text
不手工裁 RTL
不让 LLM 自由选模块
不把 entire SoC cone 当作默认工作单元
不隐藏 parent boundary dependency
```
