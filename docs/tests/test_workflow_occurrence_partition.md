# `tests/test_workflow_occurrence_partition.py`

## 测试目标

`occurrence_partition` Formal AST 与真实 arbiter conservation proof 的回归。

覆盖：

- AST 编译/渲染为 `whole <=> exactly_one_same_cycle(parts)`；
- 非法 relation、duplicate part、recursive whole、当前不支持的 identity scope 被 shape validator 拒绝；
- singleton partition 作为 same-cycle equivalence 合法；
- 真实 priority arbiter partition 可由 exact same-cycle proof 证明；
- selected payload equality 与 partition 一起在真实 meta-write/meta-read/MMIO-alloc arbiter 上验证；
- output drop、两个 parts 同时 fire、错误 selected driver 都必须产生明确 proof failure；
- boundary occurrence 的物理 handshake 是 authoritative，不能被 LLM 自写 signal grounding 偷换。
