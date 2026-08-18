# LLM 之前的静态前端完整规划

## 总体原则

当前系统把职责固定为：

$$
\text{Static = completeness}
$$

$$
\text{LLM = semantics}
$$

$$
\text{Formal = correctness}
$$

因此在任何 LLM case extraction 之前，以下信息都应由静态工具固定，而不是让模型猜。

## S0：Input Contract 与 Provenance

输入优先采用 Chisel elaboration 得到的 textual CHIRRTL/classic FIRRTL surface form，并保留 source locators。

静态记录：

```text
FIRRTL module/signal
→ source file
→ line/column
```

v5 已实现。

CIRCT FIRRTL-dialect MLIR 以后使用独立 adapter，不混用 grammar。

## S1：Physical Hierarchy Discovery

从 module/instance 关系机械恢复 concrete hierarchy：

```text
DCache
├── ProbeUnit
├── WritebackUnit
├── MSHRFile
└── arrays/arbiters/...
```

v4 已实现。

## S2：Physical Boundary Discovery

模块边界首先就是 elaborated design 的真实 port leaf。

Bundle/Vec/flip 只做机械展开。

v4 已实现。

## S3：Global Physical Event Registry

从 Decoupled `valid/ready` 和 Valid `valid+bits` 结构构造 physical event：

```text
BoomProbeUnit.io.req.fire
BoomProbeUnit.io.rep.fire
```

并固定：

```text
predicate
payload leaves
direction
source locator
```

这一阶段不产生 `ProbeRecv` 等语义名称。

v4 已实现。

## S4：Dependency IR

从 CHIRRTL statement 构建：

$$
G=(V,E_D\cup E_C\cup E_S\cup E_A\cup E_M)
$$

其中分别表示：

- data；
- control；
- next-state；
- address；
- memory dependency。

v5 已实现核心语法。

## S5：Event-Centered Local Slice

从每个 physical event 的 `valid/ready/payload` 做 backward fixed point。

目标不是“尽量小”，而是：

> 在 parser 支持的 dependency 语义下，不漏掉任何能够影响该 event 的 upstream state/control/data。

v5 已实现。

## S6：静态细粒度分层候选

大 module 不直接送给 LLM。

先做：

```text
register-to-register dependency
→ SCC
+
event cone incidence
```

得到 state regions。

这些 region 只是 candidate，不由静态工具强行命名成“RAR ordering engine”等语义模块。

v5 已实现，并通过 `AbstractionTree` 把 physical hierarchy 和 state regions 合成一个静态 work-unit tree。

## S7：Hierarchical Flattening / Connector Grounding

把 parent instance port 与 child local port 映射到同一个 concrete flat identity。

例如：

```text
parent: prober.io.rep.valid
child:  io.rep.valid
```

变成：

```text
DCache.prober::io.rep.valid
```

从而可以从顶层 TL C event 一直反向切到 ProbeUnit 内部 state。

v5 已实现。

注意：有 gate/arbiter 时不把两端武断认成“同一个语义 event”；dependency graph 保留 gating condition。

## S7.5：Direct Handshake Connector Discovery

对两个 concrete physical events，如果能机械证明：

```text
A.valid -> B.valid
B.ready -> A.ready
```

都是 direct DATA/ALIAS connection，则建立 physical connector。

这可以固定 parent/child endpoint 的物理传递关系，而不依赖 LLM。

如果中间有 gate/arbiter，则不建立 direct connector，仍由 dependency slice 保留真实条件。

v5 已实现。

## S8：Coverage Ledger

这是防止静态 slice 产生虚假完整性的关键。

每条 statement 都必须是：

```text
included
supported outside slice
nondriving
unsupported
```

只要出现未知的 potentially-driving statement，分析 fail-closed。

v5 已实现。

## S9：Source Reconstruction

把 slice 的 source spans 映射回真实 Scala snippets。

LLM 不应该只看到被 lowering 后的临时 signal 名；它应该同时拿到：

```text
physical FIRRTL graph
+
exact Scala context
```

v5 已实现 `SourceMapper`。

## S10：Deterministic Handoff Manifest

静态 frontend 输出：

```text
physical event
signals
edge kinds
statements
state SCC / cone
boundary frontier
source spans/snippets
coverage
unsupported list
```

同时保持：

```text
semantic_labels = []
```

`handoff.py` 只有在 coverage complete、slice 未截断、source provenance 存在且当前 slice 至少有 source-mapped span 时才允许 `ready=true`。

v5 已实现。

# LLM 从哪里开始

LLM 应从 **S10 之后**才出现。

它的第一项工作应该是：

```text
static slice + source context
        ↓
解释 state/control 的设计语义
        ↓
提出 guarded leaf cases / semantic aliases
```

但 LLM 不允许：

- 删除 static slice 中的信号；
- 发明新的 physical EventKind；
- 修改 source grounding；
- 把 coverage incomplete 的 slice 当作完整 case；
- 自己决定一个 parent summary 已经被证明。

之后的 case equivalence / projection / proof 仍回到机械/形式方法。

# BOOM 可行性核对

我们已经针对 BOOM v4 实际源码检查了这套静态设计是否匹配。

## ProbeUnit

`src/main/scala/v4/lsu/dcache.scala` 中 `BoomProbeUnit` 有：

```text
req
rep
meta_read
meta_write
wb_req
lsu_release
```

等真实 Decoupled boundary，并有显式 FSM `state`。

`rep.valid` 和 `lsu_release.valid` 都直接由 state 控制，因此 event-centered dependency slice 能自然进入 FSM。

## DCache hierarchy

`BoomNonBlockingDCacheModule` 真实实例化：

```text
BoomWritebackUnit
BoomProbeUnit
BoomMSHRFile
```

并把 ProbeUnit 连到 TL B、TL C、MSHR、writeback 和 LSU release arbiter。

因此 cross-instance flattening 不是人为构造的需求，而是 BOOM 的真实结构。

## MSHR

`src/main/scala/v4/lsu/mshrs.scala` 的 `BoomMSHR` 包含：

```text
18-state FSM
BranchKillableQueue RPQ
meta_hazard
probe_rdy
mem_acquire/mem_grant/mem_finish
replay/resp
```

这正好覆盖我们需要的：

- state dependency；
- queue/memory-like state；
- timing-sensitive hazard register；
- multiple boundary events。

因此 state-SCC + event cone 是合理的第一版 static partition primitive。

# v5 之后仍需完成的静态工程

在真正打开 LLM Agent 前，建议下一阶段不是继续发明 IR，而是跑 **真实 BOOM elaboration** 并做 coverage-driven hardening：

1. 用 BOOM/Chipyard 实际 build 生成 CHIRRTL；
2. 对 `BoomProbeUnit`、`BoomMSHR`、DCache top 跑 `report`；
3. 收集所有 `UNSUPPORTED` statement；
4. 逐类补 parser，直到目标 cone/module `complete=true`；
5. 检查 source locator 解析率；
6. 检查 TL B/C → ProbeUnit、MSHR Grant/Ack 等 hierarchical slices；
7. 统计原始 RTL/FIRRTL 行数与 slice 行数，验证 token reduction；
8. 再开始 LLM leaf-case extraction。

仍明确 deferred 的能力：

- CIRCT FIRRTL-dialect MLIR adapter；
- 所有 advanced memory/layer/probe/property semantics；
- blackbox 内部 dependency；
- protocol opcode 的最终语义命名；
- formal proof/certificate。

其中前三项应由真实 coverage 结果决定优先级，而不是现在提前实现全部 FIRRTL 语言。

## LSU / BOOM B1 对 static frontend 的额外核对

当前 BOOM v4 LSU 的 load-ordering search 仍然使用：

```text
ldq_executed
ldq_succeeded
ldq_will_succeed
ldq_observed
nested when
RegNext
Vec/entry indexing
```

这说明后续真实 LSU slice 至少需要：

- register/state dependency；
- nested control dependency；
- next-cycle register chain；
- vector/subaccess address dependency。

v5 已分别用 `STATE`、`CONTROL`、register update 和动态 `[*] + ADDRESS` dependency 建立对应静态表示。

但是当前结论仍需要通过**真实 BOOM emitted CHIRRTL coverage**确认，因为 Scala loop/elaboration 后的具体命名和 aggregate lowering 取决于编译输出。若出现新 FIRRTL statement，fail-closed ledger 会阻止它直接进入 LLM。
