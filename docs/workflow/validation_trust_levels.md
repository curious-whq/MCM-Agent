# µMCM validation trust levels

MCM-Agent deliberately separates candidate discovery, structural evidence and trusted proof.

```text
LLM candidate
  -> GROUNDED
  -> deterministic structural evidence
     STRUCTURALLY_SUPPORTED / PARTIALLY_SUPPORTED / REFUTED
  -> formal backend
     FORMALLY_PROVED / SPEC_PROVED
  -> trusted_umcm.json
  -> freeze gate
     FROZEN_FOR_COMPOSITION
```

## Trust boundary

只有 `FORMALLY_PROVED` 和 `SPEC_PROVED` axioms 能约束父层。`GROUNDED`、`PARTIALLY_SUPPORTED`、`STRUCTURALLY_SUPPORTED` 都只是 evidence，不能进入 trusted set。

这使不完整 abstraction 保持为安全 over-approximation：缺少 constraint 可能产生 spurious parent/system counterexample，但不会因为“结构看起来对”而静默排除真实行为。

## Bundled proof engines

- `none`：fail closed，不提升任何 axiom；
- `explicit-control`：有限状态 exhaustive reachability + exact local symbolic/pattern certificates；不是通用 SMT/bit-level RTL prover；
- `composition-prover`：parent-only theorem composition。它只使用 hash-verified frozen child theorems 与 exact parent-local bridges，不重开 child RTL。

## Structural counterexample vs exact proof

structural model 可以有意 over-approximate data-dependent behavior，因此 structural `COUNTEREXAMPLE` 可能是 spurious。若 exact formal backend 能证明 concrete obligation，最终 validation level 可以仍为 `FORMALLY_PROVED`。反之，只有 structural support 而没有 formal certificate 仍不 trusted。

## Parent provenance

parent candidate 为新 axiom 声明 `parent_local` / `reexported` / `lifted` / `emergent` provenance 与 source child axioms。该声明不是 trust source。

对于 composition proof，workflow 会从 proof certificate 重新推导实际 `kind` 与 `source_axioms`；声明与 certificate 不一致时 `trusted_umcm` / freeze fail closed。

## Freeze gate

```bash
python3 -m workflow.cli freeze runs/<task-id>
```

要求：

- 无 refuted axiom；
- 所有 declared candidate axioms 均 `FORMALLY_PROVED` / `SPEC_PROVED`；
- `unresolved` 为空；
- trusted projection 完整；
- parent certified provenance 最新且匹配。

成功后状态为 `FROZEN_FOR_COMPOSITION`。frozen summary 仍可在未来 CEGAR 中 reopen，但 reopen 的理由必须来自更高层 counterexample 暴露的 abstraction weakness，而不是 prose 猜测。
