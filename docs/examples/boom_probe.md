# `examples/boom_probe.py`

## 文件职责

Prototype v0 的 BOOM L1 Probe 手工案例。

clean 与 dirty path 内部实现不同，但投影后都具有：

$$
ProbeRecv < ReleaseNotify < ProbeResponse
$$

因此可以安全 merge。

`buggy_dirty_case()` 故意构造相反 boundary ordering，用于验证异常 case 不会被错误合并。
