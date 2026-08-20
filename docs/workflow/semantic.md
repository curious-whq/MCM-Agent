# `workflow/semantic.py`

## 文件职责

µMCM candidate 的 deterministic semantic validation、proof orchestration、trusted projection 与 freeze gate。当前：

```text
SEMANTIC_VALIDATOR_VERSION = semantic-validator-0.14
PROPERTY_COMPILER_VERSION  = formal-axiom-compiler-0.7
```

## `HandoffControlModel`

从 static handoff 提取一个 fail-closed finite-control/dataflow abstraction。对 data-dependent mux branch 采用 over-approximation；同时支持 alias、aggregate projection、constant propagation、state transitions 与 occurrence labeling。

## Validation flow

```text
candidate Formal AST
  -> compile proof obligations
  -> structural checker
  -> selected formal backend
  -> parent composition prover (parent synthesis only)
  -> validation level
  -> trusted_umcm projection
```

structural evidence 包括 `STRUCTURALLY_SUPPORTED`、`PARTIALLY_SUPPORTED`、`COUNTEREXAMPLE`、`STRUCTURAL_UNKNOWN`。只有 `FORMALLY_PROVED` / `SPEC_PROVED` 进入 trusted set。

如果 obligation 引用了 frozen child semantic object，parent-local structural/formal checker 不允许重开 child RTL；跨 child 关系由 `composition_prover` 基于 frozen theorem + exact local bridge 处理。

## Trusted projection

`_build_trusted_umcm()` 只保留 trusted axioms 以及它们引用到的 occurrence/predicate/identity/case closure。parent provenance 必须由 certificate 推导结果验证。

## `validate_task_dir()`

grounding 必须先 valid。随后写：

```text
property_obligations.json
semantic_validation.json
trusted_umcm.json
status.json
SUMMARY.md
```

## `freeze_task_dir()`

只有同时满足以下条件才能 `FROZEN_FOR_COMPOSITION`：

- 无 refuted axiom；
- 每条 declared candidate axiom 都是 `FORMALLY_PROVED` 或 `SPEC_PROVED`；
- `unresolved` 为空；
- trusted µMCM 与 candidate axiom 集一致；
- parent 的 certified provenance 不缺失且不过时。

frozen parent 会保留 child frozen imports 与 merged semantic catalog。后续若 system counterexample 暴露 abstraction 太弱，可通过 CEGAR reopen。
