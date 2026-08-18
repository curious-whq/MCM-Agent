# `frontend/handoff.py`

## 文件职责

定义 **LLM 之前最后一道静态 gate**。

未来即使加入 LLM，也不应该把任意 parser 输出直接发送给模型；必须先通过这里的 completeness、provenance 和 scope 条件。

## `HandoffNotReadyError`

静态信息不完整、slice 被 budget 截断，或 provenance 不足时抛出。

## `_require_provenance()`

要求输入存在 source locators。

没有 source locator 时，dependency analysis 仍可能用于诊断，但不能进入 grounded LLM handoff。

## `build_local_static_handoff()`

生成单个 module-type 的 pre-LLM package。

必须满足：

```text
input provenance ready
AND
local slice complete
AND
local slice not truncated
AND
slice 至少有一个 source-mapped span
```

## `build_instance_static_handoff()`

v6 新增，生成 **concrete ownership subtree** 的 pre-LLM package。

这是完整 SoC 上优先使用的 hierarchical handoff。例如：

```text
event = ...dcache.prober::io.req.fire
root  = ...dcache
```

则静态 slice 可以进入 DCache 自己拥有的：

```text
ProbeUnit
MSHRFile / MSHR
WritebackUnit
arbiter / metadata/data-array control
```

但不会因为 `ready` 或其它 parent-side dependency 自动逃进整个 BoomCore/SystemBus。

readiness 额外要求 ownership-scoped slice `complete=true`。输出会标记：

```json
"handoff": {
  "ready": true,
  "stage": "pre-llm-static",
  "semantic_labels_locked": true,
  "ownership_scoped": true
}
```

并保留：

```text
scope = instance_subtree
subtree_root = <concrete instance path>
semantic_labels = []
```

如果 `max_signals` 耗尽，slice 会 `truncated=true`，本函数直接拒绝 handoff。

## `build_design_static_handoff()`

whole-design hierarchical 版本。

它适合确实需要全系统 semantic cone 的情况，但在完整 Chipyard 上不应作为默认第一 primitive，因为 `ready/control` 可能把 cone 扩展到很大的 core/system state。

默认同样有 fail-closed `max_signals` budget。

## Source snippets

三个 handoff builder 都可以接 `SourceMapper`，将 FIRRTL source span 还原成真实 Scala snippets。

因此未来 LLM 接收到的不是只有 lowering 后 signal 名，而是：

```text
physical event
+ dependency/scope evidence
+ source locator
+ exact source snippets
+ coverage/truncation status
```

## `semantic_labels_locked`

它不是说未来永远不能出现语义 alias，而是：

> 进入 LLM 时 physical event registry 已经固定；LLM 只能提出有 grounding 的语义解释，不能重写物理事件事实，也不能把 incomplete 静态结果说成完整。
