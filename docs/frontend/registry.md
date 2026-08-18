# `frontend/registry.py`

## 文件职责

从 physical boundary leaf ports 中机械发现第一版 **Global Physical Event Registry**。

v5 支持两种结构化 occurrence convention：

```text
Decoupled: valid && ready
Valid:     valid
```

这里仍然只生成物理名称，不生成 `ProbeRecv`、`Grant` 等语义名称。

## `ChannelDirection`

相对当前 module：

- `RECEIVE`
- `SEND`

## `EventProtocol`

### `DECOUPLED`

有 valid/ready 双向 handshake。

### `VALID`

只有 valid + bits 的单向 occurrence。

## `PhysicalEvent`

保存：

```text
event_id
module
channel
direction
protocol
predicate
valid
ready(optional)
payload
sources
```

Decoupled 例子：

```text
BoomProbeUnit.io.req.fire
predicate = io.req.valid && io.req.ready
```

Valid 例子：

```text
Module.io.state.valid
predicate = io.state.valid
```

## `EventRegistry`

维护 event id 唯一性。

### `empty()`

构造空 registry。

### `register()`

重复 event id 直接拒绝。

### `sorted_events()`

稳定排序输出，保证 manifest/test 可复现。

## `discover_decoupled_events()`

要求同一 prefix 同时存在：

```text
.valid
.ready
```

并且方向互补。

receive：

```text
valid = input
ready = output
```

send：

```text
valid = output
ready = input
```

payload 为同 prefix 下所有 `.bits...` leaf。

## `discover_valid_events()`

识别：

```text
.valid
.bits...
```

但没有 sibling `.ready` 的 Valid-style channel。

为降低 payload 内部字段误识别，v5 不从其它 channel 的 `.bits...` 内部再提升新的 top-level Valid event。

## `discover_boundary_events()`

组合当前支持的 Decoupled 和 Valid event convention。

`StaticFrontend` 使用这个函数建立 registry；旧的 `discover_decoupled_events()` 继续保留用于只关心 handshake 的测试/API。

## 还没有自动 event 化的信号

普通 Bool input/output 不会仅因为是 Bool 就被当作 event，因为静态结构无法判断它是 pulse、level state 还是配置位。

需要这类 event 时，后续可以增加新的**机械 occurrence convention**，或者由语义阶段提出候选后再做 grounding 验证。
