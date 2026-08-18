# `frontend/dependency.py`

## 文件职责

实现 LLM 之前的 signal dependency IR，并在 v6 中针对真实 Chipyard FIRRTL 做性能和语法 hardening。

图包含：

```text
signal / reg / node / memory / instance-port
        +
data dependency
control dependency
state dependency
address dependency
memory dependency
alias dependency
```

后续 slice、route、partition 都只消费这个静态图。

## Fail-closed 原则

任何 parser 不认识、又可能影响功能的 statement 都记为 `UNSUPPORTED`：

```text
unknown potentially-driving statement
→ coverage incomplete
→ static handoff blocked
```

因此“不认识”不会被误解释为“不相关”。

## `SignalKind`

支持：

- `PORT`
- `WIRE`
- `NODE`
- `REGISTER`
- `MEMORY`
- `MEMORY_PORT`
- `INSTANCE_PORT`
- `UNKNOWN`

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

普通 memory-model slice 默认不跟 clock/reset，避免时钟树淹没语义 cone。

## `StatementRecord`

记录 FIRRTL line、statement kind、source locator、drives/reads/control reads 和 coverage status。

这是 Coverage Ledger 的基本单位。

## `ModuleDependencyGraph`

保存一个 module 的：

```text
signals
edges
statements
register roots
memory roots
instance modules
ports
aggregate type/leaf index
```

`complete` 当且仅当不存在 unsupported functional statement。

## Expression dependency

`extract_expression_dependencies()` 区分 data/control/address。

例如：

```text
mux(sel, a, b)
```

得到：

```text
sel -> CONTROL
a,b -> DATA
```

动态 subaccess：

```text
vec[idx]
```

保留：

```text
vec[*] -> DATA
idx    -> ADDRESS
```

## FIRRTL 3.x textual syntax

v6 除旧 spelling 外，还支持真实 Chipyard 使用的：

```text
connect dst, src
invalidate target
```

并继续兼容：

```text
dst <= src
dst <- src
target is invalid
```

`parameter` / `defname` 被识别为 non-driving metadata，而不是未知 executable logic。

## Aggregate connect 与 flip

v5 对含 `flip` 的 aggregate connect 只能 fail-closed。

v6 已实现 leaf-level orientation parity。对于：

```text
connect B, A
```

普通 leaf 保持：

$$
A.valid \rightarrow B.valid
$$

而 flipped `ready` leaf 反向：

$$
B.ready \rightarrow A.ready
$$

这对 TileLink/Diplomacy aggregate connect 是必要的。

此外，真实 FIRRTL 经常连接 aggregate 子前缀，例如：

```text
connect widget.auto.anon_in, dcache.auto.out
```

v6 会按相同 relative leaf suffix 对齐，而不是把几十个 leaf 压成一个 synthetic aggregate signal。

## `ModuleGraphProvider`

完整 Chipyard FIRRTL 有上千个 module。预先构建所有 dependency graph 会浪费大量内存和时间。

`ModuleGraphProvider` 保存：

```text
whole FIRRTL text
module line/span index
lazy graph cache
```

调用 `get()/require()` 时只构造当前真正需要的 module graph。

## 性能 hardening

v6 做了三项关键优化：

1. **module span index**：不再为每个 module 重扫整个 69 MiB FIRRTL；
2. **subaggregate index**：aggregate descendant 查询不再扫描全 module；
3. **dynamic wildcard shape buckets**：`vec[*]` alias 不再做二次方 regex 比较。

真实 BOOM `LSU`、`BoomCore` 等大 module 因此可以按秒级构图。

## 当前限制

仍未声称支持所有可能的 FIRRTL/CIRCT 语言：

- FIRRTL-dialect MLIR SSA 使用独立 adapter；
- blackbox 内部行为不可从 textual boundary 推断；
- memory read-under-write 仍是依赖级而非完整值语义；
- advanced property/layer/probe construct 必须由真实 coverage 决定是否实现。

只要这些构造进入相关 cone，Coverage Ledger 仍会 fail-closed。
