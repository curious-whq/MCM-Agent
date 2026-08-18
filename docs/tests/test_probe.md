# `tests/test_probe.py`

## 文件职责

保留 Prototype v0 的 Probe 回归测试，确保引入 `EventRef` 后原 ordering/FSM abstraction 没有回归。

## `_project_normalize(case)`

执行：

```text
project_case
-> normalize_case
```

## `test_clean_projects_internal_states_away`

验证 internal FSM state 被隐藏，并仍得到：

$$
ReleaseNotify < ProbeResponse
$$

v1.1 中检查 endpoint 的 `EventRef.kind`，而不是直接拿字符串比较。

## `test_clean_and_dirty_merge_to_unconditional_boundary_case`

验证 clean/dirty 投影后 consequence 相同，并由互补 guard 合并为 unconditional parent case。

## `test_special_boundary_behavior_is_not_merged`

验证异常 dirty ordering 不会被错误 merge。
