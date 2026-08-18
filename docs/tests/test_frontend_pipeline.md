# `tests/test_frontend_pipeline.py`

## 文件职责

验证 `StaticFrontend` 的端到端 orchestration。

覆盖：

```text
parse
→ coverage report
→ event registry
→ local manifest
→ hierarchical design slice
```

并检查 manifest 中 `semantic_labels` 保持为空。

另外验证 v5 会机械登记没有 ready 的 `Valid` boundary occurrence，而不把任意 Bool 信号都当成 event。
