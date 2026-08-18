# `tests/test_mshr.py`

## 文件职责

验证 v1/v1.1 resource conservation 与 event identity。

主要测试：

- RPQ lifecycle 能生成父层 `OneOfBetween`；
- 无 boundary predecessor 时不生成 summary；
- request $s$ 的 predecessor 不能用于 request $r$；
- request $s$ 的 exit 不能清除 request $r$ 的 token；
- internal exit 未投影到 boundary 时直接拒绝。
