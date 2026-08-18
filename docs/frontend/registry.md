# `frontend/registry.py`

## 文件职责

从 physical boundary leaf ports 中机械发现 Decoupled-style handshake event，并建立第一版 Event Registry。

v4 不尝试理解 `req` 到底是不是 Probe，也不会直接创造 `ProbeRecv` 这样的语义名称。

## `PhysicalEvent`

保存：

```text
event_id
module
channel
direction
predicate
valid
ready
payload
sources
```

例如：

```text
event_id:
  BoomProbeUnit.io.req.fire

predicate:
  io.req.valid && io.req.ready
```

这是一个**物理事件**，能够直接回到真实接口信号。

## `ChannelDirection`

根据 leaf port 方向机械确定：

### receive

```text
valid = input
ready = output
```

### send

```text
valid = output
ready = input
```

## `EventRegistry`

保存全局唯一的 `PhysicalEvent`。

重复 `event_id` 会直接报错。

## `discover_decoupled_events()`

对于每个相同 prefix：

```text
<prefix>.valid
<prefix>.ready
```

如果两者都存在且方向互补，则建立：

```text
<Module>.<prefix>.fire
```

predicate 固定为：

```text
<prefix>.valid && <prefix>.ready
```

并把：

```text
<prefix>.bits...
```

下面的 leaf 全部登记为 payload。

这一阶段完全静态。以后 LLM 若要把：

```text
BoomProbeUnit.io.req.fire
```

解释为 `ProbeRecv`，只能增加一个带 provenance 的语义 alias，不能修改这个 physical event 的 grounding。
