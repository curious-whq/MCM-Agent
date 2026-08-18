# `mcm/__init__.py`

## 文件职责

定义 `mcm` 包的公共 API。

当前导出三类 abstraction primitive：

- ordering/FSM：`project_case`、`merge_equivalent_cases`；
- resource/token：`ResourceInvariant`、`derive_resource_summaries`；
- state case：`StateCase`、`merge_state_cases`。

同时导出基础 IR：`EventRef`、`PredicateRef`、`OutcomeRef`、`Before`、`Guard` 等。
