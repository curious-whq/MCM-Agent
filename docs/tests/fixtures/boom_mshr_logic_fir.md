# `tests/fixtures/boom_mshr_logic.fir`

## 文件职责

根据真实 BOOM `BoomMSHR` 结构手工构造的 CHIRRTL fixture。

保留：

```text
state
grantack_valid
RPQ instance/enq/empty
mem_acquire
mem_grant
mem_finish
```

用于验证 `mem_finish` backward slice 和 MSHR state partition。

该 fixture 的目的不是模拟完整 MSHR 值语义，而是验证 LLM 前静态 cone 能否保留我们手工 v1 案例所需的 queue/barrier/state dependency。
