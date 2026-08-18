# `tests/test_b1.py`

## 文件职责

验证 v2.1 BOOM B1 model 和 state-case minimizer。

## `test_buggy_partition_keeps_executed_hole_as_no_blocking_effect`

确认旧逻辑中：

$$
Executed(O)
$$

这一组 case 不产生当前跟踪的 blocking effect。

## `test_fixed_partition_uses_will_succeed`

确认修复后 blocking case 可化简为：

$$
\neg Succeeded(O)\land\neg WillSucceed(O)
$$

而当前/下一拍成功路径可化简为：

$$
Executed(O)\land WillSucceed(O)
$$

## `test_predicates_for_different_loads_do_not_merge`

确认 $Executed(O)$ 与 $Executed(P)$ 是不同 predicate。

## `test_guard_minimizer_preserves_truth_table_for_all_three_var_functions`

这是 v2.1 新增的性质测试。

对三个布尔变量共有 $8$ 个输入 assignment，因此所有可能布尔函数数量为：

$$
2^8=256
$$

测试为每一个布尔函数构造完整 minterm case set，执行 `merge_state_cases()` 后，再检查全部 $8$ 个输入 assignment 的 consequence 是否与原始 case 完全一致。

因此它不是只测试一个手写例子，而是在三变量范围内穷举验证 minimizer 的语义保持性。
