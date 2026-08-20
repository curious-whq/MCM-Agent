# `tests/test_frontend_workunit.py`

## 测试目标

回归 `frontend.workunit` 的递归切分、ownership conservation 与 complexity quotient。

主要覆盖：

- independent event/state group 可以被分开；
- shared state/statement 保留在 parent；
- child internals 被 `umcm://...` summary slot 替换；
- immediate frontier 不会把完整历史 FSM 误拉进 child ownership；
- high-degree hub state 晋升到 parent，避免把所有 event group 粘死；
- 大 SCC 可以在 shared hub 下继续细分；
- child 读取 parent frontier 时，child-local temporal statement 仍可归 child；
- unowned whole-module fanout 不计入 child edge complexity；
- lowering duplication 被 logical edge/statement/signal quotient 消除；
- replacement complexity 只计算 parent-visible RTL；
- event cut 失败时回退到 state/dependency hierarchy；
- physical module child 仍是 primary WorkUnit，并暴露 parent replacement frontier。

这些测试保证 planner 的“可扩展性优化”不会破坏 statement/state/event conservation。
