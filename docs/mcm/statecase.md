# `mcm/statecase.py`

## 文件职责

负责状态 case 的保留和安全布尔化简。

一个 `StateCase` 表示：

$$
\frac{Guard}{TrackedEffects}
$$

## `StateCase`

包含：

- `guard`：状态条件；
- `outcomes`：当前追踪的 effect 集合；
- `provenance`：来源。

`outcomes=()` 是合法 consequence，含义是这个分支没有产生当前跟踪的 effect。

## `_combine_adjacent_guards`

只对 consequence 完全相同、且仅差一个互补 predicate 的两个 cube 做精确合并。

例如：

$$
\neg Executed(O)\land\neg Succeeded(O)
$$

与：

$$
Executed(O)\land\neg Succeeded(O)
$$

如果 effect 完全相同，则可化简为：

$$
\neg Succeeded(O)
$$

## `_minimize_guard_group`

反复应用上述布尔 cube 合并。

## `merge_state_cases`

先按 exact effect set 分组，再做 guard 最小化。

v2.1 的测试会穷举三个布尔变量的全部 $2^{2^3}=256$ 个布尔函数，确认最小化前后每个 assignment 的 consequence 完全一致。
