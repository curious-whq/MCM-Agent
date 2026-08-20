# `workflow/composition_prover.py`

## 文件职责

在 parent synthesis 阶段用 **trusted frozen child theorems + exact parent-local bridges** 关闭跨组件 proof obligation。当前版本 `composition-prover-0.4`。

它不是一般 SMT solver，也不会重开 child RTL。

## Trusted theorem collection

prover 只从 hash-verified `FROZEN_FOR_COMPOSITION` summary 中收集 trusted axioms，并保留 qualified semantic IDs。当前主要组合 theorem kind 包括 history/order、occurrence partition、value constraint 与 exclusion/forbid 相关事实。

## 组合规则

现有规则包括：

- parent/child occurrence inclusion/equivalence bridge；
- exact parent-child `occurrence_partition`；
- trusted occurrence-partition substitution；
- trusted child value lift，经 parent-local exact signal alias；
- trusted history transitivity / before/after restriction；
- safe same-index history 到 existential history 的 weakening；
- exact inductive `onehot0` register invariant，用于证明 mutually-exclusive partition。

所有规则都生成 certificate；无法恢复 exact bridge 时返回 unknown，而不是猜测。

## Provenance

`derive_composition_provenance()` 从 proof certificate 重新计算 parent axiom provenance（如 `lifted`、`emergent`、`parent_local`）及 `source_axioms`。LLM 声明的 provenance 只有与 certificate 一致才可进入 trusted/frozen parent。
