# `tests/test_probe.py`

## 文件职责

v0 ordering/FSM projection 的回归测试。

验证：

- internal FSM state 会被投影掉；
- clean/dirty equivalent case 可以 merge；
- synthetic exceptional ordering 不会被 merge。
