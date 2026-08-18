# `tests/test_frontend_dependency.py`

## 文件职责

验证 ProbeUnit 风格 CHIRRTL 的 dependency graph 和 local event slice。

主要覆盖：

- modern `public module`/FIRRTL version 结构；
- `mux` selector 被识别为 CONTROL；
- register update 被识别为 STATE；
- fixture 不存在静默 unsupported statement；
- `io.rep.fire` slice 能恢复 `state`、request/control 条件；
- unrelated `debug_unused` 不进入 slice；
- FULL slice 能通过 payload 回溯到 request/address source provenance。
