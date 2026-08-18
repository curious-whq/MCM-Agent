# `mcm/conservation.py`

## 文件职责

该文件实现 Prototype v1/v1.1 的第二类 abstraction primitive：resource/token conservation。

v1.1 的关键修复是：资源 token 不再只通过事件名字关联，而是显式携带 request identity 和 resource scope。

对 BOOM MSHR/RPQ，我们希望表达：

$$
ReqAccept(r,m)
\rightarrow RPQEnq(r,m)
$$

request $r$ 进入 MSHR $m$ 的 RPQ 后，只能通过：

$$
RespOut(r,m),\ ReplayOut(r,m),\ Kill(r,m)
$$

离开；而：

$$
GrantAck(m)
$$

要求该 token 已经离开。

最终父层 summary 是：

$$
ReqAccept(r,m) < GrantAck(m)
\Rightarrow
\exists e\in\{RespOut(r,m),ReplayOut(r,m),Kill(r,m)\}.
ReqAccept(r,m)<e<GrantAck(m)
$$

这里数学上的 $e$ 不对应代码里的一个自由变量，而对应 `OneOfBetween.choices` 中实际满足条件的某个 `EventRef`。

## `_same_bindings(left, right, keys, require_present=True)`

比较两个 `EventRef` 在指定参数键上的绑定是否相同。

例如在 `req` 键上：

$$
RespOut(r,m) \text{ 与 } RPQEnq(r,m)
$$

匹配；而：

$$
RespOut(s,m) \text{ 与 } RPQEnq(r,m)
$$

不匹配。

这是 v1.1 防止“别的请求替 request $r$ 出队”的基础检查。

## `OneOfBetween`

```python
OneOfBetween(
    start=ReqAccept(r,m),
    choices=(Kill(r,m), ReplayOut(r,m), RespOut(r,m)),
    end=GrantAck(m),
)
```

语义为：

$$
start < end
\Rightarrow
\exists c\in choices.\ start<c<end
$$

### 字段

- `start`：父层起始 occurrence；
- `choices`：允许满足 token exit 的 occurrence 集合；
- `end`：父层 barrier occurrence。

因为字段类型是 `EventRef`，request/scope identity 是公理本身的一部分，不再是注释中的隐含条件。

### `__post_init__()`

检查 choices 非空、start/end 不相同，并避免 choice 与 start/end 重合。

## `ResourceInvariant`

描述一个内部资源上的单 token 生命周期。

### 字段

- `enter`：创建 token 的内部 occurrence；
- `exits`：允许 token 离开的 occurrence；
- `empty_at`：要求 token 已不存在的 barrier occurrence；
- `token_keys`：token 身份字段，例如 `("req",)`；
- `scope_keys`：资源实例字段，例如 `("mshr",)`。

对于 RPQ：

```text
token_keys = ("req",)
scope_keys = ("mshr",)
```

因此 exit 必须同时匹配相同 request 和相同 MSHR；barrier 只要求匹配相同 MSHR，因为 `GrantAck(m)` 本身不是 per-request event。

## `ResourceInvariant.build(...)`

除了去重和基本合法性检查外，v1.1 新增身份一致性验证。

每个 exit 必须满足：

$$
exit.req = enter.req
$$

且：

$$
exit.mshr = enter.mshr
$$

每个 barrier 必须满足：

$$
barrier.mshr = enter.mshr
$$

因此把 `RespOut(s,m)` 填进 request $r$ 的 invariant 会直接抛出 `ValueError`。

## `_closest_boundary_predecessors(...)`

寻找 internal `enter` 上游最近的 boundary occurrence，同时要求它携带与 `enter` 相同的 token/scope bindings。

因此即使输入图中有人错误写出：

$$
ReqAccept(s,m) < RPQEnq(r,m)
$$

也不会用 request $s$ 去生成 request $r$ 的父 summary。

## `derive_resource_summaries(...)`

核心 projection API。

步骤：

1. 检查 exits/barriers 的 kind 是否父层可见；
2. 对 case ordering 求闭包；
3. 找到与 internal enter 相同 token/scope 的最近 boundary start；
4. 为每个合法 barrier 生成 `OneOfBetween`。

## 当前限制

`ResourceInvariant` 仍是手工提供的 leaf invariant。当前代码没有从 RTL 证明“RPQ token 一定保持到某个 exit”这一事实。v1.1 解决的是**身份表达正确性**，不是 leaf invariant 自动证明问题。
