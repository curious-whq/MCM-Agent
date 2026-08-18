# `frontend/model.py`

## 文件职责

定义 FIRRTL frontend 的结构化数据模型。

目标是把 Chisel/FIRRTL 中与后续分析有关的结构信息先固定下来，并且保留 source locator。

## `SourceLoc`

保存 FIRRTL 中的源码定位信息：

```text
file
line
column
raw
```

例如：

```text
src/main/scala/v4/lsu/dcache.scala 146:12
```

`parse()` 从字符串右侧解析行列号，因此文件路径包含空格时也可以处理。

需要注意：v4 只保留**输入 FIRRTL 本身提供的 locator 精度**。如果某个 aggregate port 只有一个 locator，那么由它展开出的 leaf port 会继承这个 locator；v4 不会凭空猜测更精细的 Scala 行号。

## FIRRTL type

当前支持：

- `GroundType`
- `BundleType`
- `VectorType`

`BundleField.flipped` 保存 FIRRTL orientation。

## `PortDirection`

只有 `input/output` 两种模块物理方向，并提供 `flipped()`。

## `Port`

保存 aggregate FIRRTL port。

## `LeafPort`

把 aggregate port 展开到真实 leaf，例如：

```text
io.req.valid
io.req.ready
io.req.bits.address
```

## `flatten_type()`

递归展开 Bundle/Vector，并按照 `flip` 传播真实物理方向。

例如一个 `Flipped(Decoupled)` 最终应得到：

```text
valid -> input
ready -> output
bits  -> input
```

## `Instance`

保存 `inst child of Module`。

## `ModuleDef`

保存模块的 ports、instances、source locator，以及是否是 `extmodule`。

## `Design`

保存 circuit top 和所有 module definitions。
