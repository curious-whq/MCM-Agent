# `tests/test_workflow_boom_mshr.py`

## 测试目标

真实 `BoomMSHR` parent synthesis 的 end-to-end formal regression。

当前 frozen run 应有 15 条 trusted axioms，全部 `FORMALLY_PROVED`。测试特别锁定：

- bounded indexed occurrence proof；
- exact combinational exclusion；
- trusted child history 的 after-restriction composition；
- structural over-approximation 即使产生 counterexample，也可由 exact formal proof 正确 discharge；
- indexed counter 必须有 zeroing entry cut；
- child-history lift 依赖 exact same-clock bridge；
- 多出的未建模 guard 会让相关 bridge fail closed，而不会污染无关 axiom。

这是 MSHR bottom-up composition 当前最重要的真实 RTL 回归之一。
