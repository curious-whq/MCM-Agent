# `tests/test_xiangshan_timing.py`

## 文件职责

验证 v3 timing IR 的基本语义和 XiangShan case。

## `test_same_cycle_and_next_have_exact_cycle_meaning`

检查：

$$
SameCycle(A,B)\Rightarrow \Delta(A,B)=0
$$

以及：

$$
Next(A,B)\Rightarrow \Delta(A,B)=1
$$

## `test_pre_final_fix_preserves_same_cycle_corner_case`

在最终 s0 bypass 修复之前：

- $\Delta=1$ 的 previous-cycle write 返回 write data；
- $\Delta=0$ 的 same-cycle write 返回 old meta。

因为 consequence 不同，merge 后必须仍保留两个 case。

## `test_final_fix_merges_equivalent_timing_cases_without_filling_gaps`

最终修复后两个 case 都返回 write data，因此可以合并为：

$$
\Delta(MetaWrite,MetaRead)\in\{0,1\}
$$

## `test_union_is_exact_not_interval_generalization`

专门验证：

$$
\{0\}\cup\{2\}=\{0,2\}
$$

而不是错误地推成：

$$
\{0,1,2\}
$$

这防止抽象阶段凭空创造未验证的 timing case。

## `test_different_occurrences_do_not_merge`

不同 load occurrence 的 timing relation 不能因为 EventKind 相同而被合并。
