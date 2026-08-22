# `workflow/formal.py`

## 文件职责

定义 formal backend API 与仓库内置的 fail-closed proof backend。当前 API 版本为 `formal-backend-api-0.23`。

## Backends

### `none`

`NoFormalBackend` 永远不会把 structural evidence 提升为 trusted proof。用于只查看 deterministic structural support 的实验。

### `explicit-control`

`ExplicitControlFormalBackend` 是 solver-free 的有限状态/精确模式 prover，覆盖：

- finite-control exhaustive reachability 的 history/order/exclusion；
- exact combinational Boolean exclusion；
- exact symbolic local signal equality / identity projection；
- scalar / same-index valid-token provenance；
- bounded indexed coverage；
- exact same-cycle occurrence partition；
- static constant bit；
- selected finite reference equivalence，例如 TileLink `ClientMetadata.onProbe`。

它会先验证 control abstraction 是否完整：reset、known states、每个 control-register writer、transition domain 与 stutter coverage 都必须可认证。超出 proof domain 时 fail closed。

在 parent synthesis 中，local backend 完成后 `workflow.semantic` 还会调用独立的 `composition_prover` 处理 imported child theorems。
