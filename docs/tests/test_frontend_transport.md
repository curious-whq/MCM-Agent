# `tests/test_frontend_transport.py`

## 文件职责

验证 v6 的 lazy end-to-end handshake transport primitive。

测试设计在源码内定义：

```text
Source
→ stateful Queue
→ Sink
```

因此不需要额外 fixture 文件。

## `test_lazy_route_proves_valid_and_ready_through_stateful_queue`

要求同时恢复：

$$
Source.valid \rightarrow^* Sink.valid
$$

以及：

$$
Sink.ready \rightarrow^* Source.ready
$$

并识别中间 `Top.q` 为 stateful instance。

## `test_transport_does_not_claim_semantic_alias`

确认 transport 只连接两个不同 physical event，不自动合并语义 identity。

## `test_route_cli_emits_grounded_paths_and_locked_semantics`

验证 CLI `route` 输出完整 path，并保持：

```json
"semantic_labels": []
```

## `test_signal_budget_failure_is_fail_closed`

人为把 `max_signals` 降得很小，要求结果 `complete=false` 且至少一个 path `truncated=true`。

这保证搜索预算耗尽不会被错误解释成完整分析。
