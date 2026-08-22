# `workflow/semantic.py`

## 文件职责

µMCM candidate 的 deterministic semantic validation、proof orchestration、trusted projection 与 freeze gate。当前：

```text
SEMANTIC_VALIDATOR_VERSION = semantic-validator-0.23
PROPERTY_COMPILER_VERSION  = formal-axiom-compiler-0.13
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

`forbid_when` 的 child lift 同时要求 occurrence bridge 与 predicate bridge。predicate bridge 只接受两种情况：同一个 frozen semantic object，或 direct child predicate 的完整 grounding signal 已暴露在 frontier，且 parent-local Boolean cone 能证明两者精确等价。证书记录 frozen hash，并明确 `child_rtl_reopened: false`；未暴露信号或非等价 alias 均 fail closed。

对于 FIRRTL bundle，grounding 会从 IO、memory 与 inferred mport declaration 恢复 aggregate path，而不是只依赖 lowered leaf `drives`。conditional `signal_equality` 可以把没有单一 aggregate writer 的 bundle 按完整 declared field set 分解证明；任何缺失或不等价字段都会 fail closed。

## Trusted projection

`_build_trusted_umcm()` 保留全部 trusted axioms 作为可供 composition prover 使用的 lemma closure；对于新版 parent，它另外保存显式 `public_interface`。下一层 LLM 只看到 exported axioms/objects，private bridge lemmas 仍保留在完整 artifact 中。parent provenance 必须由 certificate 推导结果验证，public axiom 必须全部 trusted 且不能引用未导出的 child/internal semantic object。

## `validate_task_dir()`

grounding 必须先 valid。随后写：

```text
property_obligations.json
semantic_validation.json
trusted_umcm.json
status.json
SUMMARY.md
```

CLI 在交互式终端默认把逐 axiom 进度条写到 stderr，显示当前 checker、`structural` / `formal` / `composition` 阶段、trusted 数量和累计耗时；最终 JSON 仍单独写到 stdout。重定向环境可用 `--progress` 强制开启，或用 `--no-progress` 关闭：

```bash
python3 -m workflow.cli semantic-validate \
  "$TASK" \
  --formal-backend explicit-control \
  --progress
```

## `freeze_task_dir()`

只有同时满足以下条件才能 `FROZEN_FOR_COMPOSITION`：

- 无 refuted axiom；
- 每条 declared candidate axiom 都是 `FORMALLY_PROVED` 或 `SPEC_PROVED`；
- `unresolved` 为空；
- trusted µMCM 与 candidate axiom 集一致；
- parent 的 certified provenance 不缺失且不过时。

frozen parent 会保留 child frozen imports 与 merged semantic catalog。后续若 system counterexample 暴露 abstraction 太弱，可通过 CEGAR reopen。
