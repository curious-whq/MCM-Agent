# `frontend/workunit.py`

## 文件职责

该文件实现 MCM-Agent 当前的核心静态抽象边界：`HierarchicalWorkUnit`。它负责把 physical module hierarchy、event/state interaction、state dependency 与 statement ownership 组合成一个可递归、守恒且可供 bottom-up µMCM synthesis 使用的树。

## 核心类型

- `WorkUnitKind`：`MODULE` / `REGION` / `EXTERNAL`；
- `WorkUnitDecision`：`MANAGEABLE` / `PARTITIONED` / `UNSPLITTABLE`；
- `WorkUnitConfig`：结构复杂度与 coupling 阈值；
- `WorkUnitComplexity`：同时保留 raw 与 logical complexity；
- `WorkUnitCoverage`：statement/state-region/event 的 conservation ledger；
- `HierarchicalWorkUnit`：完整 scope、parent-local scope、shared glue、frontier、children 与 replacement complexity；
- `ParentAnalysisInput` / `ChildReplacement`：将 child internals 替换为 `umcm://<child-id>` summary slot 后交给父层语义综合。

## Raw、logical 与 replacement complexity

当前 planner 明确区分三种量：

```text
raw complexity
    FIRRTL lowering 后的保守物理规模

logical complexity
    quotient 掉 lowering/aggregate duplication 后的语义规模

replacement complexity
    当前 children 被 summary slot 替换后，父层仍可见的 local RTL 规模
```

是否“可管理”主要依据 logical complexity；父层是否已经通过 bottom-up replacement 变得可管理，则看 `replacement_complexity` / `replacement_exceeded_limits`。

## Ownership 与 coverage

同一 module 内的静态切分必须满足 conservation：

```text
scope statements
= local parent statements
  ∪ child-owned statements
```

并检查 missing / duplicate / unsupported statement、state region 与 event。只有 `coverage.complete == true` 的 WorkUnit 才能进入 workflow handoff。

共享协调状态与真正跨 child 的 glue 留在 parent；读取 parent frontier 不会自动把 child-local temporal logic 拉回 parent。

## Event-first + state fallback

优先使用 immediate Event-State Interaction Graph 找弱耦合 child；如果 event partition 无法产生有意义的至少两个 child，则回退到 register SCC / state-dependency hierarchy。SCC 只是强耦合提示，不是不可再分的原子边界。

## v11：transitive structural fingerprint

`module_structural_sha256()` 生成与 elaboration 产生的 module 名称无关的递归结构哈希：

- external module：端口结构；
- internal module：端口、signals、I/O、register/memory roots、statements；
- child instance 的 generated module 名会被 child 的 structural SHA-256 替代。

这使两个不同 instance path 上、甚至 generated module name 不同但结构等价的 module 可以被识别为同一个 RTL implementation shape。

注意：这个 structural hash 本身不是 proof。真正的 module theorem reuse 还会在 `workflow.composition` 中同时校验 proof-scope implementation hash，只有二者都匹配时才允许实例化 frozen module theorem。

## 相关文档

- `docs/frontend/hierarchical_work_units.md`：planner 的演进与整体设计；
- `docs/frontend/module_cli.md`：`mcm-plan` 入口；
- `docs/workflow/composition.md`：结构等价如何进入 frozen theorem reuse。
