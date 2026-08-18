# `frontend/dependency.py`

## 文件职责

该文件实现 v5 静态前端的核心 **signal dependency IR**。

输入仍然是 textual CHIRRTL/classic FIRRTL，但分析目标从 v4 的结构信息扩展为：

```text
signal / reg / node / memory / instance-port
        +
data dependency
control dependency
state dependency
address dependency
memory dependency
```

后续 event-centered slice 只在这个图上做 fixed point，不直接让 LLM 阅读整个 RTL。

## 设计原则

### 1. fail-closed

遇到不认识、又可能影响电路行为的 FIRRTL statement 时，不静默忽略，而是记录为 `UNSUPPORTED`。

因此：

```text
parser 不认识某条可能驱动电路的语句
    -> coverage incomplete
    -> static handoff 不允许进入 LLM
```

### 2. control 和 data 分开

例如：

```text
mux(sel, a, b)
```

其中 `sel` 进入 `CONTROL` dependency，`a/b` 进入 `DATA` dependency。

这对后续提取 guarded case 很重要，因为 branch selector 往往正是 case guard。

### 3. register update 单独标记

当 destination 属于 register 时，connect 产生 `STATE` edge，而不是普通 `DATA` edge。

这样后续可以从组合图中机械恢复 register-to-register state dependency，并构建 SCC。

## `SignalKind`

区分：

- `PORT`
- `WIRE`
- `NODE`
- `REGISTER`
- `MEMORY`
- `MEMORY_PORT`
- `INSTANCE_PORT`
- `UNKNOWN`

`UNKNOWN` 不表示一定错误，只表示当前 signal 没有被声明 parser 精确分类。

## `DependencyKind`

支持：

- `DATA`
- `CONTROL`
- `STATE`
- `RESET`
- `CLOCK`
- `ADDRESS`
- `MEMORY`
- `ALIAS`

普通 slice 默认不跟 clock/reset，避免时钟树淹没语义 cone。

## `StatementStatus`

- `SUPPORTED`：当前 parser 理解其 dependency 语义；
- `NONDRIVING`：例如 assert/printf/metadata，对当前功能 backward slice 不作为 driver；
- `UNSUPPORTED`：可能影响功能，但 parser 尚未支持。

## `SignalInfo`

保存 signal 名、类型、kind、source locator，以及 aggregate root。

## `StatementRecord`

保存每条 module statement 的：

```text
id
FIRRTL line
kind
raw text
source locator
drives
reads
control_reads
status
```

这就是 coverage ledger 和 provenance 的基本单位。

## `DependencyEdge`

一条有向 dependency：

$$
src \rightarrow dst
$$

同时保存 dependency kind、对应 statement ids 和 source locator。

## `ModuleDependencyGraph`

一个 module 的完整静态 dependency graph。

主要内容：

- `signals`
- `edges`
- `statements`
- `register_roots`
- `memory_roots`
- `instance_modules`
- `input_ports/output_ports`
- `aggregate_leaves`

### `add_signal()`

登记信号；如果已有更精确类型，不用 `UNKNOWN` 覆盖它。

### `ensure_signal()`

dependency 中引用到尚未显式声明的信号时保守登记。

### `is_register()` / `is_memory()`

判断 leaf/subfield 是否属于某个 register/memory root。

### `predecessors()`

按 dependency kind 查询某个 signal 的直接前驱。

### `unsupported_statements` / `complete`

用于 fail-closed coverage 判断。

## `ExpressionDependencies`

把表达式引用拆成：

```text
data
control
address
```

### `merge()`

组合两个表达式 dependency 集合。

### `all_refs`

取得三类引用的并集。

## `extract_expression_dependencies()`

解析 FIRRTL expression dependency。

当前对 `mux`、`validif` 专门处理 control selector，其余 primop 保守作为 data dependency。

动态 vector subaccess：

```text
vec[idx]
```

会得到：

```text
data    = vec[*]
address = idx
```

即保留“由 idx 选择 element”这一事实。

## `build_module_dependency_graph()`

v5 的核心 parser。

当前支持：

```text
wire
node
reg
regreset
<= / <- connect
when / else
cmem / smem
read/write/infer mport
is invalid
```

同时：

- 展开已知 aggregate connect；
- 把 enclosing `when` condition 加入 CONTROL edge；
- register destination 产生 STATE edge；
- memory mport 保留 ADDRESS/MEMORY dependency；
- 未知 executable syntax 记为 `UNSUPPORTED`。

### Aggregate connect 与 flip

FIRRTL aggregate connect 在 flipped field 上可能反向传递。v5 只对 passive aggregate 做 leaf expansion。

如果 direct aggregate connect 的 relevant subtype 含 flip，当前 parser 记为 `UNSUPPORTED`，不使用错误的统一 $src ightarrow dst$ 近似。

这意味着真实 BOOM elaboration 如果保留大量 bidirectional aggregate connect，coverage 会明确失败，并驱动我们下一步实现完整 FIRRTL flow adapter。

## `build_all_dependency_graphs()`

对 design 中所有非 external module 构图。

## `_add_wildcard_alias_edges()`

如果同时见到：

```text
vec[*]
vec[0]
vec[1]
```

会增加保守 `ALIAS` edge，避免动态 subaccess 因具体 lane 展开而断链。

## 当前限制

v5 主要针对 CHIRRTL 高层语法。尚未完整支持：

- CIRCT FIRRTL-dialect MLIR SSA 语法；
- 所有 lowered memory attribute/block 形式；
- layer/probe/property 等高级 FIRRTL 构造；
- memory read-under-write 的精确值语义；
- 参数化 blackbox 内部行为。

这些缺口如果出现在真实 BOOM elaboration 中，会被 coverage ledger 暴露，而不会静默通过。
