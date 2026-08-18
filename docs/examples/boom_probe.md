# `examples/boom_probe.py`

## 文件职责

Prototype v0 的 BOOM L1 Probe clean/dirty 手工案例，也是 v1.1 的回归案例。

## `BOUNDARY`

定义 `ProbeRecv`、`ReleaseNotify`、`ProbeAck`、`ProbeAckData` 为当前父层可见 event kind。

## `ALIASES`

定义：

```text
ProbeAck     -> ProbeResponse
ProbeAckData -> ProbeResponse
```

v1.1 的 `AliasMap` 会保留 `EventRef` 参数；该示例目前使用无参数 occurrence，所以行为与 v0 一致。

## `clean_case()`

手工描述 non-dirty 路径：

$$
ProbeRecv < ProbeUnit.s\_lsu\_release < ReleaseNotify < ProbeUnit.s\_release < ProbeAck
$$

## `dirty_case()`

手工描述 dirty/writeback 路径：

$$
ProbeRecv < ProbeUnit.wb\_req < Writeback.s\_lsu\_release < ReleaseNotify < Writeback.s\_active < ProbeAckData
$$

两条路径投影并 alias 后具有相同 boundary consequence，因此可安全 merge。

## `buggy_dirty_case()`

故意构造：

$$
ProbeAckData < ReleaseNotify
$$

其 boundary behavior 与 clean case 不同，因此必须保留下来。
