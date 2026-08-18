# `frontend/firrtl.py`

## 文件职责

解析 **classic textual FIRRTL/CHIRRTL 的结构子集**。

v4 不是完整 FIRRTL parser。当前只提取后续 frontend 第一阶段需要的：

```text
circuit
module / extmodule
input / output
aggregate type
inst ... of ...
source locator
```

其它 statement 当前被保守忽略，等 event-centered slicing 阶段再扩展。

## `FirrtlParseError`

结构输入不合法时抛出的异常。

## `_TypeParser`

一个轻量递归下降 parser，用于解析 FIRRTL type。

当前支持：

```text
UInt<32>
SInt<64>
Clock
Reset
{ a : UInt<1>, flip b : UInt<1> }
UInt<8>[4]
```

## `parse_type()`

把 textual FIRRTL type 转为 `GroundType / BundleType / VectorType`。

## `_split_source()`

把：

```text
output io : ... @[Foo.scala 10:2]
```

拆成声明正文和 `SourceLoc`。

## `parse_firrtl()`

解析完整 textual FIRRTL，生成 `Design`。

当前设计原则是：

> 第一阶段宁可只支持明确的结构语法，也不通过模糊正则猜测复杂 statement 的含义。

依赖/赋值/FSM statement 会在 slicing 阶段单独扩展。
