# LLM 之前的静态前端：v6 完整规划与真实集成状态

## 总体原则

职责保持：

$$
\text{Static = completeness + physical grounding}
$$

$$
\text{LLM = semantics}
$$

$$
\text{Formal = correctness}
$$

LLM 不能负责决定物理层次、边界事件、真实连接、slice completeness，也不能因为“看起来不重要”而删除 RTL dependency。

# S0：Input Contract 与 Provenance

输入是 Chisel/Chipyard elaboration 得到的 textual FIRRTL/CHIRRTL，并保留 source locators：

```text
FIRRTL object
→ Scala file
→ line/column
```

CIRCT FIRRTL-dialect MLIR 使用独立 adapter，不与 textual grammar 混解析。

# S1：Physical Hierarchy

从 module/instance 机械恢复 concrete hierarchy。

完整 Chipyard 输入可以直接分析，不要求用户事先裁成 ProbeUnit、MSHR、L2 等小文件。

# S2：Physical Boundary

真实 elaborated port leaf 就是第一层 physical boundary。

Bundle/Vec/flip 只做机械 orientation 展开。

# S3：Physical Event Registry

自动发现：

- Decoupled：`valid && ready`；
- Valid：`valid`。

物理 event 固定 concrete endpoint、direction、payload 和 source locator。

静态阶段不产生 `ProbeRecv` 等语义名称。

# S4：Dependency IR

构建：

$$
G=(V,E_D\cup E_C\cup E_S\cup E_A\cup E_M\cup E_X)
$$

分别表示：

- data；
- control；
- state；
- address；
- memory；
- conservative alias。

v6 已支持真实 Chipyard FIRRTL 3.x `connect`/`invalidate` spelling，以及 aggregate flip flow。

# S5：Event-Centered Local Semantic Cone

从一个 physical event 的 occurrence/payload backward fixed point，恢复所有可能影响它的 local state/control/data。

这个 cone 的目标是 completeness，不是强行小到某个 token 数。

# S6：大 Module 的静态 Work Unit

先从：

```text
register dependency
→ SCC
+
event-cone incidence
```

形成结构 work unit。

physical module hierarchy 始终是主树；state region 是大 module 内部的机械细分，不由 LLM 自由划模块。

# S7：Concrete Hierarchical Identity

parent instance-port 和 child local port 映射到同一个 concrete signal identity。

这样 dependency 可以自然跨 module boundary。

# S7.5：Direct Connector

只有当：

$$
A.valid \rightarrow B.valid
$$

与：

$$
B.ready \rightarrow A.ready
$$

都属于 direct DATA/ALIAS edge，才声明 `HandshakeConnector`。

中间有 gate、buffer、arbiter 时不伪装成 direct。

# S7.6：End-to-End Handshake Transport

真实 L1↔L2 的 TileLink route 会穿过：

```text
buffer
queue
width widget
xbar
fifo fixer
coupler
crossing
```

因此 v6 新增 `HandshakeTransportPath`。

完整 transport 同时要求：

$$
source.valid \rightarrow^* sink.valid
$$

以及：

$$
sink.ready \rightarrow^* source.ready
$$

它解决的问题是：

> 两个远端 physical endpoint 是否真的通过当前 elaborated design 相连，路径是什么？

它不解决：

> 这个事件的所有 guard/state 是什么？

后者仍由 semantic cone slice 负责。

# S8：Coverage Ledger

任何 potentially-driving unknown statement 都会使相关 module incomplete。

路径/slice 如果触及 incomplete instance，同样不能标 `complete=true`。

搜索预算耗尽也显式 `truncated=true`，不能把“没搜到”误当成“证明不存在”。

# S9：Source Reconstruction

source spans 可映射回真实 Scala context。

未来 LLM 的输入应该是：

```text
physical graph
+
exact Scala snippets
+
coverage/provenance
```

而不是只有 lowering 后的临时 signal 名。

# S10：Pre-LLM Handoff

静态 output 应包含：

```text
physical events
signals/edge kinds
statements/state regions
boundary frontier
physical transport evidence
source spans/snippets
coverage/truncation
semantic_labels = []
```

LLM 从这里之后才允许解释：

```text
design intent
semantic aliases
guarded leaf cases
```

但不能重新定义 physical EventKind，也不能把 incomplete 静态结果说成已经证明。

# 真实 Chipyard integration

v6 已第一次直接使用完整 `SmallBoomV4Config.fir`，而不是 toy-only fixture。

输入：

```text
523,408 lines
~69 MiB
1,858 module definitions
2,170 concrete events
502,974 source locators
```

以下关键 module 的当前 dependency coverage 均为 complete，unsupported 为 0：

```text
LSU
BoomCore
BoomNonBlockingDCache
BoomProbeUnit
BoomMSHR
BoomMSHRFile
InclusiveCache
InclusiveCacheBankScheduler
InclusiveCacheControl
```

更详细统计见 `docs/integration/real_chipyard_v6.md`。

# 已验证的真实 L2↔L1 coherence transport

## L2 B → ProbeUnit

从：

```text
InclusiveCache auto.in.b.fire
```

机械找到到：

```text
BoomProbeUnit io.req.fire
```

的完整 valid + ready path。

路径穿过真实 system bus、TLJbar、TLFilter、TLXbar、TLFIFOFixer、多个 TLBuffer/Queue、BoomTile master xbar 和 DCache。

## ProbeUnit C → L2

从：

```text
BoomProbeUnit io.rep.fire
```

机械找到到：

```text
InclusiveCache auto.in.c.fire
```

的完整 valid + ready path。

因此当前 frontend 已经不是“能看到 L2 module”，而是能够证明真实 Probe/ProbeAck physical transport 跨过完整 Chipyard hierarchy。

# Scalability 结论

第一次真实运行发现：直接把远端 event 的整个 occurrence cone 做成一个巨型 union slice，会被 ready/control 高 fan-in 放大。

因此 v6 确立两个分开的静态 primitive：

```text
Transport Route
  → hierarchy composition / physical connector grounding

Semantic Cone
  → guarded case extraction / state-control analysis
```

这也是后续递归 µMCM abstraction 应采用的边界：先机械固定“模块怎么连”，再在每个局部 cone 内提取/投影 cases，而不是让 LLM 从整颗 SoC 自由检索。

# 进入 LLM 前剩余的工程

静态架构已经成型，后续主要是 coverage-driven，而不是继续凭空扩 IR：

1. 对更多真实 memory/coherence endpoints 跑 route/slice；
2. 遇到目标 cone 内新的 unsupported FIRRTL syntax，再补 parser；
3. 对 LSU、DCache、L2 scheduler 建立 source-grounded local work units；
4. 统计 whole-module 与 slice 的 reduction；
5. 固定未来 LLM handoff schema 中的 physical connector evidence；
6. 然后开始 LLM leaf-case extraction。

仍 deferred：

- semantic transaction identity；
- protocol opcode 的高层 alias；
- parent µMCM summary synthesis；
- formal certificate/composition proof。

这些不能由当前 transport reachability 替代。

# v6 真实集成后的 ownership-scoped semantic cone

真实 whole-SoC 实验进一步说明，semantic cone 也需要区分“系统输入范围”和“当前抽象 ownership”。

系统输入始终是完整 FIRRTL，但 parent work unit 可以指定一个 concrete hierarchy root：

```text
InclusiveCache instance
DCache instance
ProbeUnit instance
MSHR instance
...
```

`backward_instance_slice_lazy()` 允许进入该 root 拥有的所有 children，但在 root physical input boundary 停止。

因此推荐组合变成：

```text
Route
  证明 parent work units 之间怎么物理连接

Instance-subtree Slice
  恢复一个 parent work unit 拥有的 semantic cone

Local Slice / SCC Partition
  继续生成 child work units
```

真实 `SmallBoomV4Config.fir` 已验证：

```text
L2 B ownership cone:
  5,252 signals / 11,852 edges / 36 instances / complete

DCache-owned Probe cone:
  4,716 signals / 25,529 edges / 29 instances / complete
```

前者进入 `SourceB`、`Directory`、`MSHR*` 等 L2 coherence engine；后者进入 `BoomProbeUnit`、`BoomMSHRFile/MSHR`、`BoomWritebackUnit`，但不进入 whole BoomCore。

这把最初的研究目标具体化为：

$$
\text{Whole-System Input}
+
\text{Static Ownership Boundary}
+
\text{Recursive Case Abstraction}
$$

而不是人工裁剪 RTL，也不是让 LLM 决定层次。
