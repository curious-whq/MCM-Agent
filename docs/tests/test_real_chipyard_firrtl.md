# `tests/test_real_chipyard_firrtl.py`

## 文件职责

这是可选的真实 Chipyard integration regression。

测试文件本身不把约 69 MiB 的 generated FIRRTL 提交进仓库，而是通过环境变量指定：

```bash
MCM_REAL_FIRRTL=/path/to/SmallBoomV4Config.fir \
python -m unittest tests.test_real_chipyard_firrtl -v
```

没有环境变量时自动 skip，因此普通单元测试仍很轻量。

## 关键 module coverage

要求真实 design 中至少存在并完整解析：

```text
LSU
BoomProbeUnit
BoomMSHR
BoomMSHRFile
BoomNonBlockingDCache
InclusiveCache
InclusiveCacheBankScheduler
```

## L2 B → ProbeUnit request transport

机械寻找：

```text
InclusiveCache auto.in.b
→ ...
→ BoomProbeUnit io.req
```

并要求 valid、ready 两条 path 都 `complete=true`，且真实 route 中存在 stateful queue。

## ProbeUnit response → L2 C transport

反向验证：

```text
BoomProbeUnit io.rep
→ ...
→ InclusiveCache auto.in.c
```

同样要求双向 handshake path 完整。

## L2 ownership subtree

从真实 L2 B event 做 `slice_instance_event()`，root 默认为真实 `InclusiveCache` instance。

要求 slice 完整并能够进入 L2-owned coherence engine，包括：

```text
SourceB
Directory
MSHR*
```

这验证输入不是“只看到 L2 外壳”。

## DCache ownership subtree

从真实 ProbeUnit request event 开始，把 root 提升到 enclosing DCache。

要求 slice 能包含：

```text
BoomProbeUnit
BoomMSHRFile
BoomWritebackUnit
```

同时不需要进入 whole BoomCore。

这两个 subtree regression 与 transport regression 合起来覆盖：

```text
physical L2↔L1 route
+
L2-owned semantic cone
+
DCache-owned semantic cone
```
