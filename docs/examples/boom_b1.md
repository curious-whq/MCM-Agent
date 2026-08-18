# `examples/boom_b1.py`

## 文件职责

手工建模 BOOM PR #706 所修复的 load-load ordering 状态 hole。

older load 记为 $O$，younger load 记为 $Y$。

## 状态 predicate

v2.1 使用三个真实状态概念：

$$
Executed(O)
$$

$$
Succeeded(O)
$$

$$
WillSucceed(O)
$$

其中 `WillSucceed` 对应最终修复里新增的 `ldq_will_succeed` next-state wire。

## tracked effects

v2.1 删除了人为构造的 `Allow(Y)`。

现在只跟踪 kill branch 中无条件执行的两个真实 effect：

```text
s1_set_execute(Y) := false
kill_forward(Y) := true
```

`io.dmem.s1_kill` 还有额外运行时 guard，因此暂时不作为该分支每次都保证的 effect。

## `buggy_cases()`

旧条件是：

```text
!(l_executed || l_succeeded)
```

关键 hole：

$$
Executed(O)\land\neg Succeeded(O)
$$

在旧逻辑中不会进入 tracked kill branch，因此该 case 的 `outcomes=()`。

## `fixed_cases()`

最终 PR 条件是：

```text
!(l_executed && (l_succeeded || l_will_succeed))
```

因此：

$$
Executed(O)\land\neg Succeeded(O)\land\neg WillSucceed(O)
$$

现在会产生 blocking effects。

而：

$$
Executed(O)\land WillSucceed(O)
$$

不会产生这两个 tracked blocking effect。

该手工 reachable partition 还利用 `ldq_will_succeed` 默认取自 `ldq_succeeded` 的关系，因此把 succeeded 状态建模为 `WillSucceed=true`。
