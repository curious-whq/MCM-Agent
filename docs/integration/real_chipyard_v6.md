# Real Chipyard `SmallBoomV4Config.fir` — v6 integration result

## 输入

实际分析的 generated FIRRTL：

```text
523,408 lines
约 69 MiB
FIRRTL version 3.3.0
Top = TestHarness
```

静态结构恢复得到：

```text
1,858 module definitions
2,170 concrete physical events
502,974 source locators
```

## 目标 memory-system module coverage

| Module | Statements | Physical events | Unsupported |
| --- | ---: | ---: | ---: |
| `LSU` | 8,169 | 24 | 0 |
| `BoomCore` | 10,539 | 26 | 0 |
| `BoomNonBlockingDCache` | 2,924 | 13 | 0 |
| `BoomProbeUnit` | 209 | 7 | 0 |
| `BoomMSHR` | 2,216 | 15 | 0 |
| `BoomMSHRFile` | 1,507 | 13 | 0 |
| `InclusiveCache` | 220 | 12 | 0 |
| `InclusiveCacheBankScheduler` | 2,499 | 12 | 0 |
| `InclusiveCacheControl` | 798 | 3 | 0 |

这些数字只表示当前 dependency language 对这些 module 的 statement coverage 完整，不表示已经完成 µMCM 证明。

## Route 1：L2 Probe B → L1 ProbeUnit request

Endpoint：

```text
TestHarness...coh_wrapper.l2::auto.in.b.fire
→
TestHarness...boom_tile.dcache.prober::io.req.fire
```

结果：

```text
found = true
complete = true
valid path = 112 edges, 5,784 searched signals
ready path = 115 edges, 341 searched signals
25 concrete instances on route
3 stateful B-channel Queue instances
```

物理 route 穿过的主要结构包括：

```text
InclusiveCache
TLBuffer
TLFilter
TLJbar
SystemBus
TLWidthWidget
TLXbar
TLFIFOFixer
Tile crossing/buffers
BoomTile TL master xbar
Boom DCache
BoomProbeUnit
```

因此它不是把 L2 与 L1 endpoint 直接 alias，而是保留真实 interconnect 路径。

## Route 2：L1 ProbeUnit response → L2 C

Endpoint：

```text
TestHarness...boom_tile.dcache.prober::io.rep.fire
→
TestHarness...coh_wrapper.l2::auto.in.c.fire
```

结果：

```text
found = true
complete = true
valid path = 113 edges, 331 searched signals
ready path = 112 edges, 4,945 searched signals
25 concrete instances on route
3 stateful C-channel Queue instances
```

## 一个重要的 scalability 结论

直接对顶层 `TL-B.fire` 做完整 occurrence backward cone，会因为 `ready`、arbiter 和 core control 的高 fan-in 快速增长。

因此 v6 不把“route recovery”和“semantic cone extraction”混为一件事：

```text
route
  固定 hierarchy/physical transport

slice
  恢复真正影响 event 的所有状态与控制
```

这个分离不是性能 hack，而是 hierarchy abstraction 的语义边界：parent/child composition 需要先知道 physical connector，case extraction 才需要完整 local semantic cone。

## Ownership slice 1：真实 L2 内部 semantic cone

从真实：

```text
TestHarness.chiptop0.system.coh_wrapper.l2::auto.in.b.fire
```

开始，以该 `InclusiveCache` concrete instance 自身作为 ownership root。

结果：

```text
complete = true
5,252 signals
11,852 dependency edges
36 concrete instances
295 boundary/frontier signals
195 source spans
```

slice 自动进入 L2 自己拥有的真实 coherence engine，包括：

```text
SourceB
Directory
MSHR*
SinkA / SinkC / SinkD / SinkE
SourceA / SourceC / SourceD / SourceE
queues / control
```

这说明当前分析不是只把 `InclusiveCache.auto.in.b` 当作一个黑盒边界，而是可以从完整 Chipyard FIRRTL 中恢复 L2 内部状态和控制 cone。

## Ownership slice 2：DCache-owned Probe semantic cone

从真实：

```text
...boom_tile.dcache.prober::io.req.fire
```

开始，但把 ownership root 提升为 enclosing：

```text
...boom_tile.dcache
```

结果：

```text
complete = true
4,716 signals
25,529 dependency edges
29 concrete instances
272 boundary/frontier signals
195 source spans
```

slice 自动包含：

```text
BoomProbeUnit
BoomMSHRFile
BoomMSHR
BoomWritebackUnit
相关 arbiter / array control
```

同时不进入 whole `BoomCore`。

这不是手工裁 DCache 文件：输入仍然是完整 `TestHarness` FIRRTL。ownership root 来自恢复出的 concrete instance hierarchy，root physical inputs 被保留成 parent boundary frontier。

## v6 最终推荐的静态分析单元

真实集成后，LLM 之前的组合不再是一个无界 whole-SoC cone，而是：

```text
Whole-system FIRRTL
  ↓
Physical transport route
  固定 L2↔L1 / L1↔LSQ 的真实 connector chain
  ↓
Ownership-scoped instance slice
  恢复当前 parent work unit 拥有的完整 state/control/data cone
  ↓
Local module slice + register-SCC/event-cone partition
  形成 child work units
  ↓
Pre-LLM static handoff
```

因此“完整 BOOM 是否能直接分析”的答案是：**输入直接是完整 BOOM+L1+L2 系统；切片边界则由静态 hierarchy/ownership 自动产生，而不是要求用户手工拆文件。**
