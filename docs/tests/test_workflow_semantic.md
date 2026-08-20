# `tests/test_workflow_semantic.py`

## 测试目标

semantic compiler、structural model、formal backend、trusted projection 与 freeze gate 的综合回归。

使用 BoomProbeUnit fixture 覆盖 forbid/order/exclusion/identity/value 等 axiom：Formal AST 必须同时驱动 rendered formula 与 proof obligation；无 formal backend 时 structural support 不能 trusted；`explicit-control` 能把 certified obligations 提升为 `FORMALLY_PROVED`；错误 identity projection 或反向 ordering 会被 refute。

还覆盖 TileLink `ClientMetadata.onProbe` reference checker 的合法状态表与故意错误行，以及 fully proved leaf freeze/trusted µMCM 相关 fail-closed 条件。

这组测试锁定整个 trust policy：candidate/structural evidence 与 trusted proof 不得混淆。
