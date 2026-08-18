# `tests/test_frontend_design_graph.py`

## 文件职责

验证 concrete hierarchy dependency graph。

主要测试：

- parent `prober.io.rep.valid` 与 child `io.rep.valid` 共用 flat identity；
- concrete design event registry；
- 从顶层 `io.tl_c.fire` 可以切入 ProbeUnit FSM；
- slice 能继续回到顶层 `io.tl_b.valid`；
- top-level inputs 被识别为 hierarchical frontier。
