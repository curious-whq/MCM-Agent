# Manual-first µMCM workflow

## Purpose

MCM-Agent 当前已经具备真实的 bottom-up µMCM abstraction/composition workflow；“manual-first”只表示 provider 仍由人工把自包含 prompt 送入 ChatGPT，再把最终 JSON 搬回 run directory。静态 handoff、schema、grounding、formal validation、freeze 与 parent composition 都是确定性的 provider-independent pipeline。

```text
Hierarchical WorkUnit
    -> static_handoff.json
    -> LeafAbstractionTask / ParentSynthesisTask
    -> provider
       current: manual ChatGPT conversation
       future : API provider
    -> candidate µMCM (umcm-formal-0.5)
    -> grounding validation
    -> Formal AST compiler
    -> deterministic structural evidence
    -> explicit formal backend
    -> parent composition prover when needed
    -> trusted_umcm.json
    -> frozen_umcm.json
```

## Current versions

```text
workflow          manual-first-workflow-0.9
leaf prompt       leaf-abstraction-prompt-0.11
parent prompt     parent-synthesis-prompt-0.4
µMCM schema       umcm-formal-0.5
handoff schema    workunit-static-0.1
planner           hierarchical-planner-v11
```

## Formal schema

`axioms[].formal` 是唯一语义源。当前 AST 支持 ordering/exclusion/identity/value、join、same-cycle `occurrence_partition`、bounded indexed coverage、index-variable lookup 与 reference-spec relations。human-readable formula、references 与 checker/proof obligation 都由 workflow 确定性派生。

LLM 不再提供 legacy `formula` / `validation` 双轨字段；导入时会拒绝这些字段。

## Leaf task

例如：

```bash
python3 -m workflow.cli leaf-task SmallBoomV4Config.fir \
  --root-module BoomProbeUnit \
  --source-root /path/to/chipyard \
  --run-root runs
```

run directory 至少包含：

```text
task.json
prompt.md
static_handoff.json
expected_output_schema.json
status.json
EXPERIENCE.md
SUMMARY.md
```

`prompt.md` 自包含 WorkUnit evidence；source root 可解析时带 source snippets，否则保留 exact FIRRTL statement ledger。

Parent prompt 使用由 frozen child artifact 确定性生成的 compact semantic interface。LLM 只看到 child 显式 exported theorem contract；private bridge lemmas 与完整递归 proof artifact 仍留在 `static_handoff.json` 中供 composition prover 校验证书、hash 与 theorem ancestry。Parent response 必须声明 public interface 与逐项 boundary coverage，使“内部证明充分”和“上层抽象充分”成为两个独立、可审计的条件。

## Manual import

```bash
python3 -m workflow.cli manual-import runs/<task-id> response.md
# 或
cat response.md | python3 -m workflow.cli manual-import runs/<task-id> -
```

Grounding validator 检查 task/work-unit/schema identity、IDs、evidence scope、physical event/state/signal、derived occurrence machine grounding、dynamic indexed selection、case/axiom closure，以及 parent imported semantic namespace/provenance。

Grounding valid 只说明候选可追溯到当前 WorkUnit，不代表 axiom 已被证明。

## Semantic/formal validation

```bash
python3 -m workflow.cli semantic-validate \
  runs/<task-id> --formal-backend explicit-control
```

写出：

```text
property_obligations.json
semantic_validation.json
trusted_umcm.json
status.json
SUMMARY.md
```

`explicit-control` 当前覆盖 finite-control exhaustive reachability、exact combinational exclusion、exact symbolic equality/identity、scalar/same-index token provenance、bounded indexed coverage、same-cycle occurrence partition、constant-bit 与 selected reference-spec proofs。

在 parent synthesis 中，涉及 imported child semantics 的 obligation 不会被 parent-local checker 重开 child RTL；随后由 `composition-prover-0.4` 使用 trusted frozen theorems 与 exact parent-local bridges 尝试关闭。

## Trust policy

候选与 trust 严格分离：

```text
GROUNDED
  -> PARTIALLY_SUPPORTED / STRUCTURALLY_SUPPORTED / REFUTED
  -> FORMALLY_PROVED / SPEC_PROVED
```

只有 `FORMALLY_PROVED` / `SPEC_PROVED` 能进入 `trusted_umcm.json`。

## Freeze

```bash
python3 -m workflow.cli freeze runs/<task-id>
```

要求：所有 declared candidate axioms trusted、无 unresolved、无 counterexample。parent 还要求 certificate-derived provenance 与 candidate declaration 一致。

成功后写 `frozen_umcm.json` 并进入 `FROZEN_FOR_COMPOSITION`。parent frozen summary 会透明保留 child imports；后续更高层只消费 frozen semantics，不重开 child RTL。

## Parent synthesis and theorem reuse

`parent-task` 为每个 direct child attach 一个 frozen summary。优先 exact child-id；对于 generic module theorem，可在 proof-scope SHA-256 与 transitive structural SHA-256 都匹配后实例化到 concrete child slot。多个匹配或结构变化均 fail closed。

因此当前 manual-first workflow 已经覆盖：

```text
leaf abstraction
  -> formal trust
  -> freeze
  -> verified child reuse/import
  -> parent synthesis
  -> composition proof
  -> parent freeze
```

未来把 manual provider 替换为 API provider，不需要改变这条验证链。
