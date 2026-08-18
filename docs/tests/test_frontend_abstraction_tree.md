# `tests/test_frontend_abstraction_tree.py`

## 文件职责

验证物理 hierarchy 与 state-SCC partition 可以稳定组合。

测试要求：

- `DCacheTop` 保持 root physical module；
- `DCacheTop.prober : BoomProbeUnit` 保持真实 child instance；
- ProbeUnit child 下存在包含 `state/way_en` 的 static state region；
- region 中关联 concrete `DCacheTop.prober::io.rep.fire`；
- export 不出现人为语义区域名称。
