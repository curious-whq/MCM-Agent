# `tests/test_workflow_indexed_priority_select.py`

覆盖 `indexed_priority_select` 的 AST shape/compiler/renderer、index-variable grounding、四种 order 定义，以及真实 `ForwardingAgeLogic` 的 2048-row exact proof。负例会篡改一个 priority writer 并要求返回具体反例，也会检查 `implicit_unconstrained` 不能用于带 reset 的结果寄存器。
