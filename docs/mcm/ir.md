# `mcm/ir.py`

## 文件职责

定义整个原型共用的基础 IR。

v1.1 开始区分“事件类型”和“带身份的符号事件 occurrence”；v2 又加入带 occurrence 参数的状态 predicate 和 outcome。

## `EventRef`

表示一个符号事件 occurrence。

例如：

```python
EventRef.of("RespOut", req="r", mshr="m")
```

表示 $RespOut(r,m)$，而不是任意一个 `RespOut`。

主要方法：

- `of()`：构造带 bindings 的事件；
- `renamed()`：只替换事件 kind，保留 bindings；
- `binding()`：读取某个参数；
- `has_keys()`：检查是否拥有指定身份字段；
- `agrees_on()`：检查两个事件在指定身份字段上是否一致。

## `PredicateRef`

表示带参数的状态 predicate，例如：

```python
PredicateRef.of("Executed", load="O")
```

对应 $Executed(O)$。

因此 $Executed(O)$ 与 $Executed(P)$ 是不同的 predicate 变量。

## `OutcomeRef`

表示 case 的边界/控制结果，例如：

```python
OutcomeRef.of("Kill", load="Y")
```

对应 $Kill(Y)$。

## `Before`

表示严格顺序：

$$
src < dst
$$

构造时会把旧版字符串自动转换为无参数 `EventRef`，所以 v0 Probe 示例仍然兼容。

## `Literal`

表示 guard 中一个 predicate 的正/负文字。

例如：

```python
Literal(PredicateRef.of("Succeeded", load="O"), False)
```

对应：

$$
\neg Succeeded(O)
$$

## `Guard`

表示 Literal 的合取。

例如：

$$
Executed(O) \land \neg Succeeded(O)
$$

空 Guard 表示 $true$。

## `Case`

表示普通 ordering case：

$$
\frac{Guard}{Before\ facts}
$$

目前仍专门服务于 v0 的 ordering/FSM projection。

## `AliasMap`

对事件 kind 做纯定义性归一化，同时保留 occurrence bindings。

例如将 `ProbeAck` 和 `ProbeAckData` 都归一为 `ProbeResponse`，但不会丢失其请求/事务身份。
