# `tests/fixtures/boom_probeunit.fir`

## 文件职责

这是 Prototype v4 的 FIRRTL structural fixture。

它不是 BOOM 官方生成产物，而是根据真实 BOOM v4 `BoomProbeUnit` 的 Chisel interface 手工构造，用于在暂未把 BOOM 完整 elaboration 接进测试环境之前验证 frontend 算法。

真实 Chisel 中 `BoomProbeUnit` 的 `io` 包含：

```text
req
rep
meta_read
meta_write
wb_req
way_en
wb_rdy
mshr_rdy
mshr_wb_rdy
block_state
lsu_release
state
```

fixture 保留这些关键接口，并给 aggregate `io` 添加：

```text
@[src/main/scala/v4/lsu/dcache.scala 146:12]
```

用于测试 source locator 传播。

它还使用一个很小的 `ProbeHarness` 实例化 `BoomProbeUnit`，用于验证 hierarchy discovery。

后续一旦接入真实 BOOM elaboration，这个 fixture 应继续保留作为快速单元测试，而 integration test 改为读取真实 emitted FIRRTL。
