# `tests/test_workflow_manual.py`

## 测试目标

manual provider boundary 与 grounding validator 的回归。

覆盖：self-contained WorkUnit handoff、leaf prompt 中 Formal AST/自主完成/language-gap 规则、task export + response import、legacy `formula`/`validation` 字段拒绝、out-of-scope evidence 拒绝、derived occurrence 必须 machine-grounded、最后一个 fenced JSON 的 response parsing，以及 dynamic array `valids[index]` 只有 wildcard storage 与 index 都 grounded 时才合法。

这些测试确保“人工搬运”不会绕过 deterministic schema/grounding boundary。
