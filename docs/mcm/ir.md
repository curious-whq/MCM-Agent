# `mcm/ir.py`

## 文件职责

定义公共符号 IR，包括 `EventRef`、`PredicateRef`、`OutcomeRef`、`Before`、`Literal`、`Guard` 和 `Case`。

v2.1 没有改变 IR 结构，但收紧了 `OutcomeRef` 的使用约定：

> 对真实 RTL case，`OutcomeRef` 应优先对应可追溯的 RTL effect，而不是自由创造诸如 `Allow` 这样的语义结果。

例如 BOOM B1 现在使用：

```text
s1_set_execute(load=Y,value=false)
kill_forward(load=Y,value=true)
```

它们对应被分析分支中的真实 assignment。

## `PredicateRef`

用于表示带 occurrence 身份的 predicate，例如：

$$
Executed(O)
$$

$$
Succeeded(O)
$$

$$
WillSucceed(O)
$$

不同 load 的 predicate 不会混合。

## `OutcomeRef`

表示被当前 case 跟踪的 effect。

`StateCase` 允许 `outcomes=()`。这只表示：

> 当前分支不产生我们正在跟踪的这些 effect。

它不自动创造一个“Allow”事件，也不意味着系统其它位置不会产生其它 effect。
