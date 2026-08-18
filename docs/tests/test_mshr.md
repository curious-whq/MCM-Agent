# `tests/test_mshr.py`

## 文件职责

验证 v1.1 的 resource-conservation projection 和 request identity 约束。

## `test_rpq_conservation_keeps_same_request_identity`

验证生成的 `OneOfBetween` 明确包含：

```text
start   = ReqAccept(r,m)
choices = Kill(r,m), ReplayOut(r,m), RespOut(r,m)
end     = GrantAck(m)
```

因此数学上的 $e$ 只能从 request $r$ 的三个 exit occurrence 中选择。

## `test_no_boundary_predecessor_means_no_parent_summary`

若 `RPQEnq(r,m)` 没有 boundary grounding，则不生成 summary。

## `test_other_request_cannot_ground_request_r`

故意输入：

$$
ReqAccept(s,m) < RPQEnq(r,m)
$$

期望输出为空，证明 request $s$ 不能作为 request $r$ 的 start。

## `test_other_request_cannot_be_an_exit_for_request_r`

尝试为 request $r$ 的 invariant 配置：

$$
RespOut(s,m)
$$

作为 exit。`ResourceInvariant.build()` 必须抛出 `ValueError`。

## `test_v1_rejects_internal_exit_in_parent_summary`

如果 exit kind 仍然是 parent boundary 不可见的 `InternalDequeue`，`derive_resource_summaries()` 拒绝生成父 summary。
