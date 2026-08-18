# `frontend/pipeline.py`

## 文件职责

提供 v5 静态前端的统一 orchestration API。

用户不需要手工依次调用 parser、registry、dependency、slice、partition。

## `ModuleStaticStatus`

一个 module 的静态状态：

```text
complete
statement_count
unsupported_count
event_count
```

## `StaticFrontendReport`

整个 design 的 module 状态汇总。

### `complete`

只有所有被解析 module 都 complete 时为 true。

## `StaticFrontend`

从一个 CHIRRTL 文本开始管理全部 deterministic stage。

### `from_firrtl()`

执行：

```text
input contract validation
→ structural parse
→ per-module dependency graphs
→ per-module physical event registries（Decoupled + Valid）
```

虽然函数名沿用 `from_firrtl`，v5 实际输入契约是 textual CHIRRTL/classic FIRRTL surface syntax；CIRCT FIRRTL dialect 会被显式拒绝。

### `report()`

返回 static coverage summary。

### `assert_complete()`

fail-closed gate。只要指定 module 有 unsupported functional statement，就拒绝继续当作完整分析。

### `event()`

按 module/event id 获取物理 event。

### `slice_event()`

module-local event-centered slice。

### `slice_manifest()`

直接生成 local static manifest。

### `partition()`

生成 register-SCC/event-cone candidate partition。

### `abstraction_tree()`

组合真实 module instance hierarchy 与每个 module 的 state-SCC/event-cone work units。

### `design_graph()`

懒构建 concrete flattened hierarchy graph。

### `design_events()` / `design_event()`

返回 instance-specific physical events。

### `design_connectors()`

机械发现 concrete endpoint 之间 valid/ready 的直接物理连接。复杂 gate/arbiter 不会被误判成 direct connector。

### `slice_design_event()`

执行跨层 backward slice。

### `design_slice_manifest()`

把 hierarchical slice 导出为 static manifest。

## LLM 边界

`StaticFrontend` 本身不调用 LLM。

真正允许跨进未来 LLM 阶段的更严格 gate 位于 `frontend/handoff.py`。
