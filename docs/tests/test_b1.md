# `tests/test_b1.py`

## 文件职责

验证 BOOM B1 的状态 case 不会被错误抽象。

## `test_buggy_state_partition_preserves_distinct_boundary_behavior`

buggy cases 合并后应保留：

$$
Executed(O) \Rightarrow Allow(Y)
$$

以及未执行/未成功时的 $Kill(Y)$ 分支。

## `test_fixed_partition_merges_unresolved_states_into_not_succeeded`

fixed cases 应把两个 unresolved 状态精确合并成：

$$
\neg Succeeded(O) \Rightarrow Kill(Y)
$$

## `test_predicates_for_different_loads_do_not_merge`

验证 $Executed(O)$ 与 $Executed(P)$ 是两个不同 predicate，不会因为名字都叫 `Executed` 就被误合并。
