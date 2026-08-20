# `tests/test_workflow_mmios.py`

## 测试目标

真实 BOOM I/O MSHR/MMIO WorkUnit 的 FSM + transaction identity + payload proof regression。

当前 candidate 应有 9 条 axiom 全部 formally proved：主要 control ordering 使用 exhaustive-state reachability，identity capture 使用 exact symbolic transaction identity，条件 payload equality 使用 exact conditional symbolic driver equality。

负向测试分别破坏 lowered fire 的 `ready` 条件和一个 reachable mux arm 的 address driver，确认 identity/payload proof 会 fail closed。
