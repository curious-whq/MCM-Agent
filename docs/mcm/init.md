# `mcm/__init__.py`

## 文件职责

定义 `mcm` 包的公共 API。

当前导出四类 abstraction primitive：

- ordering/FSM：`project_case`、`merge_equivalent_cases`；
- resource/token：`ResourceInvariant`、`derive_resource_summaries`；
- state case：`StateCase`、`merge_state_cases`；
- timing case：`TimingCase`、`SameCycle`、`Next`、`CycleDelta`、`merge_timing_cases`。

同时导出公共符号 IR，例如 `EventRef`、`PredicateRef` 和 `OutcomeRef`。
