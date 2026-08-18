# `mcm/ir.py`

## 文件职责

`ir.py` 定义 MCM-Agent 当前最基础的中间表示，包括静态事件类型、带身份参数的符号事件 occurrence、严格 ordering、guarded case 和 boundary alias。

v1.1 的核心变化是新增 `EventRef`。之前 `Before("ReqAccept", "RespOut")` 只能表达事件种类之间的关系，无法说明它们是否属于同一个动态请求。现在可以写：

```python
req = EventRef.of("ReqAccept", req="r", mshr="m")
resp = EventRef.of("RespOut", req="r", mshr="m")
Before(req, resp)
```

数学上对应：

$$
ReqAccept(r,m) < RespOut(r,m)
$$

## `Event`

```python
@dataclass(frozen=True, order=True)
class Event:
    name: str
    owner: str
    boundary: bool = False
```

表示**静态 event kind 的元数据**。例如事件属于哪个模块，以及它是否是当前层的边界事件。

它不是某次动态发生的事件；动态/符号 occurrence 由 `EventRef` 表示。

## `EventRef`

```python
@dataclass(frozen=True, order=True)
class EventRef:
    kind: str
    params: Tuple[Tuple[str, str], ...] = ()
```

表示一个带身份绑定的符号事件 occurrence。

例如：

```python
EventRef.of("RespOut", req="r", mshr="m")
```

表示 $RespOut(r,m)$。

### `EventRef.of(kind, **params)`

便捷构造方法。参数会排序后保存，使同一组绑定具有稳定、可比较的表示。

### `EventRef.coerce(value)`

将 `EventRef` 或普通字符串统一转换为 `EventRef`。

因此旧代码：

```python
Before("ProbeRecv", "ProbeAck")
```

仍然合法，并被解释为两个**无参数 EventRef**。

### `get(key)`

读取身份参数。例如：

```python
ref.get("req")
```

对 $RespOut(r,m)$ 返回 `"r"`。

### `with_kind(kind)`

只替换 event kind，保留全部身份参数。该方法主要用于 alias normalization。

### `__str__()`

把 occurrence 输出成可读形式，例如：

```text
RespOut(mshr=m, req=r)
```

## `Before`

表示严格顺序：

$$
src < dst
$$

`src` 和 `dst` 最终都会转换成 `EventRef`。

### `__post_init__()`

完成两件事：

1. 将字符串端点转换为无参数 `EventRef`；
2. 禁止 $A<A$。

## `Literal`

表示 guard 中一个布尔文字，例如 `Dirty` 或 `!Dirty`。

### `negate()`

返回该 literal 的逻辑反面。

### `__str__()`

生成可读字符串。

## `Guard`

表示若干 `Literal` 的合取。空合取表示 $true$。

### `Guard.true()`

返回 unconditional guard。

### `Guard.of(...)`

构造 guard 并执行矛盾检查。

### `_validate()`

拒绝类似：

$$
P \land \neg P
$$

的 guard。

### `is_true()`

检查 guard 是否为空合取。

## `Case`

```python
Case(name, guard, facts, provenance)
```

表示：在 `guard` 成立时，`facts` 中的 ordering facts 同时成立。

形式上可以理解为：

$$
\frac{Guard}{Facts}
$$

### `Case.build(...)`

对 facts 去重、排序，并固定 provenance，得到 deterministic representation。

## `AliasMap`

定义纯粹的 event-kind 归一化。例如：

```text
ProbeAck     -> ProbeResponse
ProbeAckData -> ProbeResponse
```

v1.1 中 alias **只改变 kind，不丢失身份参数**。因此：

$$
ProbeAck(r) \mapsto ProbeResponse(r)
$$

而不是丢成一个无身份的 `ProbeResponse`。

### `normalize(event)`

返回归一化后的 `EventRef`。

## 当前限制

`EventRef` 里的参数值当前仍是手工提供的符号字符串，例如 `r`、`m`。它们还不是 SMT 变量，也没有自动连接到 RTL transaction ID。v1.1 只是先把“同一个请求/同一个 MSHR”这个语义位置明确放进 IR。
