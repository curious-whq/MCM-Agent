# `frontend/boundary.py`

## 文件职责

把一个 `ModuleDef` 的 aggregate FIRRTL ports 展开成真正的 physical boundary leaf ports。

## `BoundaryPort`

保存：

```text
module
path
direction
type
source
```

例如：

```text
BoomProbeUnit
io.req.valid
input
UInt<1>
dcache.scala:146
```

## `discover_boundary()`

调用 `ModuleDef.leaf_ports()` 展开 Bundle/Vector。

默认过滤 FIRRTL type 为：

```text
Clock
Reset
AsyncReset
```

的 clock/reset leaf。

这一阶段的原则是：

> Boundary 首先由物理 module port 决定，而不是由 LLM 选择“看起来重要”的信号。
