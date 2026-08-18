# `mcm/__init__.py`

## 文件职责

定义 `mcm` 包的公共 API。

v1.1 新增导出 `EventRef`，使外部代码可以直接构造带 request/scope 身份的符号事件 occurrence。

## 当前导出

IR：`Event`、`EventRef`、`Before`、`Literal`、`Guard`、`Case`、`AliasMap`。

Ordering projection：`project_case`。

Case merge：`normalize_case`、`merge_equivalent_cases`。

Resource conservation：`OneOfBetween`、`ResourceInvariant`、`derive_resource_summaries`。
