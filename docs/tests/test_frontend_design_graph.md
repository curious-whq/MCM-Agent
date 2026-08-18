# `tests/test_frontend_design_graph.py`

## 文件职责

验证 concrete hierarchy dependency graph 和 ownership-scoped slicing。

主要测试：

- parent `prober.io.rep.valid` 与 child `io.rep.valid` 共用 flat identity；
- concrete design event registry；
- 从顶层 `io.tl_c.fire` 可以切入 ProbeUnit FSM；
- whole-design slice 能继续回到顶层 `io.tl_b.valid`；
- top-level inputs 被识别为 hierarchical frontier；
- `backward_instance_slice_lazy()` 以 `DCacheTop.prober` 为 root 时，在 ProbeUnit physical input 停止；
- 把 root 提升为 `DCacheTop` 时，同一个 event 可以继续纳入顶层 TL-B 输入。

最后两项验证 hierarchical ownership boundary 是静态、机械的，而不是 LLM 决定的。
