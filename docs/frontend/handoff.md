# `frontend/handoff.py`

## 文件职责

定义 **LLM 之前最后一道静态 gate**。

未来即使加入 LLM，也不应该直接把任意 parser 输出发送给模型；必须先通过这里的 readiness 条件。

## `HandoffNotReadyError`

静态信息不完整或 provenance 不足时抛出。

## `_require_provenance()`

要求输入存在 source locators。

没有 source locator 时，虽然某些 dependency analysis 可能仍然能运行，但不允许作为 grounded LLM handoff。

## `build_local_static_handoff()`

生成 module-local pre-LLM package。

必须满足：

```text
input provenance ready
AND
slice complete
AND
slice not truncated
AND
slice 至少有一个 source-mapped span
```

输出 manifest 会增加：

```json
"handoff": {
  "ready": true,
  "stage": "pre-llm-static",
  "semantic_labels_locked": true
}
```

如果提供 `SourceMapper`，还会嵌入真实 Scala snippets。

## `build_design_static_handoff()`

hierarchical 版本。

除了上述条件，还要求所有 touched concrete instances 的 module dependency graph 都 complete。

## `semantic_labels_locked`

其含义不是说未来永远不能出现语义 alias，而是：

> 进入 LLM 时，physical event registry 已经固定；LLM 只能提出有 grounding 的语义解释，不能重写物理事件事实。
