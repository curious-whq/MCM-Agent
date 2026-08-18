# `tests/fixtures/boom_dcache_hierarchy.fir`

## 文件职责

在 `BoomProbeUnit` fixture 外增加一个 `DCacheTop`，用于验证 hierarchical flattening。

顶层模拟真实 BOOM 的连接形态：

```text
TL B -> prober.req
prober.rep -> TL C
```

因此可以测试：

```text
top physical event
→ parent instance port
→ child boundary
→ child FSM
```

这是跨模块 slice 的单元测试 fixture，不是官方生成产物。
