# `workflow/schema.py`

## 文件职责

定义 LLM candidate 的 JSON Schema 与 response parser。当前：

```text
UMCM_SCHEMA_VERSION = umcm-formal-0.5
```

## Candidate envelope

顶层必须包含：

```text
schema_version, task_id, work_unit_id,
occurrences, predicates, identity_keys, cases, axioms,
assumptions, unresolved, rationale, extensions
```

`occurrences` 可声明 bounded index metadata；`axioms[].formal` 使用 `axiom_ir` 定义的 Formal AST；parent-specific metadata 位于 `extensions.parent_synthesis`。

Schema 的职责是结构闭合，不替代 grounding 或 formal proof。

## Response parsing

`parse_candidate_response()` 接受纯 JSON，或从对话文本中选择最后一个 fenced JSON block。无法得到合法 object 时直接报错；不会从 prose 猜测缺失字段。
