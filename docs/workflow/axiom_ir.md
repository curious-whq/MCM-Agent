# `workflow/axiom_ir.py`

## 文件职责

定义 µMCM Formal Axiom AST 的确定性编译与渲染层。当前 `FORMAL_AXIOM_IR_VERSION` 为 `formal-axiom-ir-0.13`。

核心原则是：`axioms[].formal` 是唯一语义源。LLM 不再同时提供一个自由文本公式和另一个 checker 描述；workflow 从 AST 自动派生：

```text
formal AST
  -> shape validation
  -> semantic references
  -> deterministic checker/proof obligation
  -> human-readable formula
```

## 表达式

值表达式支持 `signal`、`slice`、`shr`、`bit`、`const`、`index_var`、`lookup`、`and`、`or`、`not`、`indexed_cases`、`modular_increment` 等；helper 会提取 signal/index variable 引用并检查 AST shape。`indexed_cases` 用于 lowering/partition 将一个有限 vector 暴露为多个 scalar frontier 的情况。

## Axiom 类型

当前 IR 包括：

- `forbid_when`
- `identity_flow`
- `exclusion`
- `ordered_before`
- `ordered_chain`
- `signal_equality`
- `value_constraint`
- `join`
- `occurrence_partition`
- `indexed_complete`
- `indexed_priority_select`
- `register_transition`
- `indexed_storage_flow`
- `spec_relation`

其中 `occurrence_partition` 表达 same-cycle exactly-one conservation；`indexed_priority_select` 表达有限候选集合按 linear/cyclic order 唯一选择并在固定延迟后输出；`register_transition` 表达带 first-match writer priority 的完整单周期寄存器 next-state；`indexed_storage_flow` 表达带标准 `rf/co/fr` 的 indexed mutable storage；`spec_relation` 当前可承载 TileLink `ClientMetadata.onProbe` 一类参考规格关系。

未知/不完整 AST fail closed，不会降级为近似 prose checker。
