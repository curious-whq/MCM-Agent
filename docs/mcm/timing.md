# `mcm/timing.py`

## 文件职责

实现 Prototype v3 的精确 timing case IR 和安全合并。

核心原则是：

> 只有 timing case 的非时序 guard 和 boundary consequence 完全相同时，时序差异才允许被抽象合并。

同时，合并必须是精确集合运算，不能自行补齐没有观察过的 cycle。

## `DeltaDomain`

表示两个事件之间允许的 cycle 差集合。

语义为：

$$
cycle(second)-cycle(first)\in allowed
$$

例如：

```python
DeltaDomain.exact(A, B, 2)
```

表示：

$$
cycle(B)-cycle(A)=2
$$

v3 暂时只支持非负的 forward delta。

## `CycleDelta`

表示精确的 $k$ cycle 距离：

$$
cycle(B)-cycle(A)=k
$$

调用 `to_domain()` 后变成 singleton `DeltaDomain`。

## `SameCycle`

表示：

$$
cycle(B)-cycle(A)=0
$$

## `Next`

表示：

$$
cycle(B)-cycle(A)=1
$$

即 $B$ 恰好在 $A$ 下一拍发生。

## `TimingCube`

表示多个 timing constraint 的合取。

例如：

```text
SameCycle(MetaWrite, MetaRead)
Next(MetaWrite, RARRelease)
CycleDelta(MetaRead, RARAlloc, 2)
Next(MetaRead, MetaResp)
```

如果同一对事件重复出现两个 constraint，它们按照 conjunction 取允许 delta 的交集；交集为空则直接拒绝。

## `TimingCase`

表示：

$$
\frac{Guard\land TimingCube}{TrackedEffects}
$$

`Guard` 继续描述普通状态/控制条件，`TimingCube` 专门描述周期关系，`outcomes` 是当前追踪的 boundary effect。

## `_merge_timing_cubes`

只有两个 timing cube 的事件对集合相同，并且恰好只有一个 domain 不同时才合并。

不同 domain 通过集合并集精确组合。

例如：

$$
\{0\}\cup\{1\}=\{0,1\}
$$

但：

$$
\{0\}\cup\{2\}=\{0,2\}
$$

绝不会自动变成 $\{0,1,2\}$。

## `_minimize_timing_group`

反复应用 timing cube 的精确合并，同时保留 provenance。

## `merge_timing_cases`

首先按照完全相同的 `Guard` 和完全相同的 `outcomes` 分组，然后才允许 timing 合并。

因此如果 same-cycle case 和 previous-cycle case 的 boundary response 不同，它们必然保留为两个独立 case。
