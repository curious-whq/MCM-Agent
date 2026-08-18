# `frontend/coverage.py`

## 文件职责

维护静态分析的 **Coverage Ledger**，解决“切片很小，但我们是否因为 parser 不认识某段 RTL 而错误漏掉 corner case”的问题。

核心原则：

> slice 可以只包含少量语句，但 parser 对当前 module 的功能语句不能悄悄失明。

## `CoverageStatus`

每条 statement 分成：

- `INCLUDED`：进入当前 slice；
- `SUPPORTED_OUTSIDE_SLICE`：parser 支持，但与当前 event cone 无关；
- `NONDRIVING`：当前分析不认为它驱动功能信号；
- `UNSUPPORTED`：可能驱动行为但 parser 未支持。

## `LedgerEntry`

把一个 `StatementRecord` 和它的 coverage status 绑定。

## `CoverageLedger`

一个 module 的 statement coverage 结果。

### `complete`

只有不存在 `UNSUPPORTED` statement 时为 true。

### `unsupported`

列出所有未支持语句，方便后续补 parser。

### `included`

列出进入当前 event slice 的 statement。

### `counts()`

生成各状态数量，写入 static manifest。

## `build_coverage_ledger()`

输入 module graph 和当前 slice 的 statement ids，构造完整账本。

注意：即使 unsupported statement 当前没有被图上的已知 edge 连进 slice，ledger 仍然把分析标成 incomplete。原因是我们并不知道这条未知语句是否本来应该产生一条通向 seed 的 dependency。

这是 v5 的 fail-closed 选择。
