# `workflow/cli.py`

## 文件职责

`mcm-agent` 的命令行编排入口。它把 static planner、manual provider boundary、semantic/formal validation、freeze 与 research-memory 串成同一条可复现实验流程。

## 主要命令

```text
leaf-task          生成 leaf WorkUnit 的自包含 prompt package
parent-task        attach frozen direct children 后生成 parent synthesis task
manual-import      导入对话结果并做 grounding validation
semantic-validate  编译 Formal AST 并运行 structural/formal validation
freeze             将 fully trusted WorkUnit 冻结为 composition input
run-summary        重建单次实验 SUMMARY.md
handoff            生成跨对话 CURRENT_HANDOFF.md
status             查看 run 状态
```

`semantic-validate` 当前支持 `none` 与 `explicit-control` backend。

`parent-task` 还负责计算 child proof-scope implementation fingerprint 与 transitive structural fingerprint，并将 implementation catalog 交给 `workflow.composition`，因此 module theorem reuse 的安全校验发生在 parent prompt 创建之前。
