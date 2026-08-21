# `workflow/tasks.py`

## 文件职责

定义 LLM task envelope、稳定 task id 与 leaf/parent self-contained prompt renderer。

当前版本：

```text
WORKFLOW_VERSION      = manual-first-workflow-0.9
PROMPT_VERSION        = leaf-abstraction-prompt-0.11
PARENT_PROMPT_VERSION = parent-synthesis-prompt-0.3
```

## Task 类型

`TaskKind` 包含 `leaf_abstraction`、`refinement`、`parent_synthesis`、`bug_analysis`。当前主要落地的是 leaf 与 parent synthesis。

task id 对 kind/schema/prompt/handoff 做 canonical hash，因此同一输入能稳定复现，prompt/schema/handoff 变化会产生新 task id。

## Leaf prompt

要求 LLM 自主分析完整 WorkUnit，区分 boundary occurrence、derived milestone、persistent predicate、identity 与 cases；Formal AST 是唯一 axiom source。语言不足时必须返回 `MCM-AGENT LANGUAGE GAP`，不能用近似 axiom 掩盖 gap。

## Parent prompt

只提供 frozen direct child 的 compact `prompt_interface` + parent-local RTL，并明确禁止读取/推断 child internals。完整递归 frozen artifact 只保留在 `static_handoff.json` 供 composition prover 使用，不再渲染进 prompt。接口保留 direct trusted Formal AST、必要 semantic declarations、assumptions、compact provenance 与 typed opaque descendant closure；child grounding/evidence/proof tree 被隐藏。new parent axioms 必须声明 provenance：`parent_local`、`reexported`、`lifted` 或 `emergent`。允许 parent 声明零条新 axiom。

`build_parent_synthesis_task()` 要求 non-leaf、coverage complete、每个 direct child 都有 frozen summary；`build_leaf_abstraction_task()` 要求 leaf + complete coverage。
