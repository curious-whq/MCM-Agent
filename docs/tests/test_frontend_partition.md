# `tests/test_frontend_partition.py`

## 文件职责

验证静态 state partition primitive。

测试：

- 组合 cone 能压缩出 register-to-register dependency；
- ProbeUnit 的 `state/way_en` SCC；
- physical `io.rep.fire` event cone 会关联实际触达的 state registers；
- partition 不依赖语义命名。
