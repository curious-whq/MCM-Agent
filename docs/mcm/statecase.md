# `mcm/statecase.py`

## 文件职责

实现 v2 的“状态 case 保留与安全合并”。

它解决的问题是：某个稀有中间状态是否会在层次抽象时被错误吞掉。

## `StateCase`

表示：

$$
\frac{Guard}{Outcomes}
$$

与普通 `Case` 不同，它的 consequence 不是 ordering graph，而是一组 `OutcomeRef`。

例如：

$$
\frac{Executed(O) \land \neg Succeeded(O)}{Allow(Y)}
$$

## `_combine_adjacent_guards`

只合并两个**仅有一个 predicate polarity 不同**的布尔 cube。

例如：

$$
\neg Executed(O) \land \neg Succeeded(O)
$$

和：

$$
Executed(O) \land \neg Succeeded(O)
$$

如果 consequence 完全相同，可精确化简成：

$$
\neg Succeeded(O)
$$

这是逻辑等价变换，不是启发式猜测。

如果 predicate 绑定的是不同 load，例如 $Executed(O)$ 和 $Executed(P)$，则不会合并。

## `_minimize_guard_group`

对拥有相同 outcomes 的一组 `StateCase` 反复做上述相邻 cube 合并。

## `merge_state_cases`

先按 exact outcome set 分组，再对每组 guard 做安全最小化。

不同 outcome 的 case 永远不会被合并。
