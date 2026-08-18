# `tests/test_frontend_mshr_static.py`

## 文件职责

用 BOOM MSHR 风格 fixture 验证静态 frontend 不只适用于 ProbeUnit。

重点检查 `mem_finish.fire` slice 能回到：

```text
state
grantack_valid
rpq.io.empty
rpq.io.enq.valid
io.mem_grant.valid
```

这说明 queue barrier、Grant/GrantAck 生命周期所需的核心状态可以在 LLM 之前由静态 slice 保留下来。

同时检查 MSHR partition 的 event cone 会触达 `state` 与 `grantack_valid`。
