# `workflow/manual.py`

## 文件职责

实现 manual provider boundary：导出 prompt package、导入 ChatGPT 最终结果，并在进入 semantic proof 之前做 deterministic grounding validation。

## 导出

`export_manual_task()` 创建 run directory，并写出：

```text
task.json
static_handoff.json
expected_output_schema.json
prompt.md
status.json
EXPERIENCE.md
SUMMARY.md
```

初始状态为 `PENDING_MANUAL_LLM`。

## 导入与 grounding

`validate_candidate_grounding()` fail closed 检查：

- schema/task/WorkUnit identity；
- IDs 唯一；
- evidence statement 必须属于当前 WorkUnit；
- physical event / state / signal 引用必须在 grounding universe；
- derived occurrence 必须有 concrete machine grounding；
- dynamic array selection 只有 wildcard storage 与 symbolic index 都被 grounding 时才允许；
- imported child semantic ID 不能被 parent redeclare；
- case/formal AST references 必须闭合；
- parent axiom provenance 结构必须完整。

该阶段只证明“候选引用了合法 concrete evidence”，不证明 axiom 语义正确。
