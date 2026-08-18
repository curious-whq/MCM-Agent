# `mcm/conservation.py`

## 文件职责

实现 queue/resource token 的生命周期抽象。

它用于处理普通 `Before` 图无法独立表达的“进入队列后不能凭空消失”性质。

## `OneOfBetween`

表示父层 lifecycle consequence：

$$
start < end
\Rightarrow
\exists c \in choices.\; start < c < end
$$

## `ResourceInvariant`

描述一个 token 的内部生命周期。

关键字段：

- `enter`：token 创建事件；
- `exits`：允许 token 离开的事件；
- `empty_at`：要求 token 已消失的 barrier；
- `token_keys`：定义 token 身份，例如 `req,mshr`；
- `scope_keys`：定义 barrier scope，例如 `mshr`。

例如 token $r$ 属于 MSHR $m$，那么 `RespOut(req=s,mshr=m)` 不能作为 token $r$ 的 exit。

## `build`

构造 invariant 时检查：

- exits/barriers 非空；
- exit 与 enter 的 token identity 一致；
- barrier 与 enter 的 scope 一致。

## `_closest_boundary_predecessors`

找到 internal enter 之前最近的、并且 token identity 一致的 boundary predecessor。

## `derive_resource_summaries`

把 ordering grounding 与 `ResourceInvariant` 组合，生成 `OneOfBetween` 父层 summary。

目前 exits 和 barriers 必须已经是 boundary-visible；否则保守拒绝。
