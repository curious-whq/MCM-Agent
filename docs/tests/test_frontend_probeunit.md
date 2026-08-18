# `tests/test_frontend_probeunit.py`

## 文件职责

使用一个按真实 BOOM `BoomProbeUnit` 接口构造的 FIRRTL fixture，测试完整 frontend 第一阶段：

```text
FIRRTL
→ hierarchy
→ boundary
→ physical event registry
→ Scala source mapping
```

## `test_hierarchy_discovers_probe_instance`

要求自动得到：

```text
ProbeHarness.probe : BoomProbeUnit
```

## `test_boundary_recovers_req_and_rep_directions`

检查：

```text
io.req.valid = input
io.req.ready = output

io.rep.valid = output
io.rep.ready = input
```

## `test_registry_finds_all_decoupled_channels`

当前 fixture 应机械发现：

```text
io.req.fire
io.rep.fire
io.meta_read.fire
io.meta_write.fire
io.wb_req.fire
io.lsu_release.fire
```

注意这里没有 `ProbeRecv` 等语义命名。

## `test_registry_direction_is_mechanical`

检查 `req` 是 receive，其余上述输出 Decoupled channel 是 send。

## `test_event_predicate_and_payload_are_grounded`

检查 event predicate 真正由：

```text
valid && ready
```

组成，并保留 `bits` payload leaf。

## `test_event_source_maps_back_to_boom_scala`

fixture 的 `io` port locator 指向真实：

```text
src/main/scala/v4/lsu/dcache.scala:146
```

测试保证 registry event 会保留这个 source mapping。
