# `frontend/slice.py`

## 文件职责

实现 module 内部的 **Event-Centered Backward Slice**。

给定一个物理 event，例如：

```text
BoomProbeUnit.io.rep.fire
```

从 event 的 valid/ready/payload 出发，沿 dependency graph 反向做 fixed point，得到与这个 event 有关的：

```text
state
control guard
request state
boundary inputs
source locations
```

而不是把整个大文件送入 LLM。

## `EventSliceMode`

### `OCCURRENCE`

seed 只包含：

```text
valid
ready
```

用于回答“这个 event 什么时候发生”。

### `FULL`

额外加入所有 payload leaf。

用于回答“这个 event 什么时候发生，以及它携带什么内容”。

未来 LLM handoff 默认使用 `FULL`。

## `SliceOptions`

支持：

- `include_clock`
- `include_reset`
- `stop_at_module_inputs`
- `max_signals`

默认跟踪：

$$
DATA \cup CONTROL \cup STATE \cup ADDRESS \cup MEMORY \cup ALIAS
$$

不默认跟 clock/reset。

## `SourceSpan`

把 slice 内离散的 source locator 合并成源码行区间：

```text
file
start_line
end_line
```

## `SliceResult`

包含：

```text
seeds
signals
edges
statement_ids
boundary_frontier
source_spans
coverage ledger
truncated
```

### `complete`

要求：

```text
coverage complete
AND
slice 未因 max_signals 截断
```

## `_spans_from_sources()`

按文件归并相邻 source locator，生成较紧凑的 source spans。

## `backward_slice()`

核心 fixed-point 算法。

从 seeds 开始不断访问 predecessor edge，直到：

- 到达 module input；
- 没有更多 predecessor；
- 或达到用户设置的 signal 上限。

module input / unresolved source 会进入 `boundary_frontier`。

## `event_seed_signals()`

根据 `OCCURRENCE/FULL` 决定 event seed。

## `slice_event()`

对 `PhysicalEvent` 的方便封装，并检查 event 和 graph 属于同一个 module。
