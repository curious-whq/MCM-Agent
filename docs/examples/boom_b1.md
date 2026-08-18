# `examples/boom_b1.py`

## 文件职责

手工构造 BOOM B1 load-load ordering bug 的最小状态 partition，用于测试 v2 state-case abstraction。

定义 older load $O$ 与 younger load $Y$。

状态 predicate：

- $Executed(O)$；
- $Succeeded(O)$。

结果：

- $Kill(Y)$；
- $Allow(Y)$。

## `buggy_cases`

三个可达状态：

$$
\frac{\neg Executed(O) \land \neg Succeeded(O)}{Kill(Y)}
$$

$$
\frac{Executed(O) \land \neg Succeeded(O)}{Allow(Y)}
$$

$$
\frac{Executed(O) \land Succeeded(O)}{Allow(Y)}
$$

其中第二条就是关键 hole。

因为后两条 consequence 相同，它们可安全合并为：

$$
\frac{Executed(O)}{Allow(Y)}
$$

## `fixed_cases`

修复后，`Executed(O) && !Succeeded(O)` 也变成 $Kill(Y)$。

于是前两条可安全合并为：

$$
\frac{\neg Succeeded(O)}{Kill(Y)}
$$

这正是 v2 要验证的：只有 boundary outcome 相同的状态 case 才能被抽象合并。
