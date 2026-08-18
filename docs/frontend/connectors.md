# `frontend/connectors.py`

## 文件职责

提供两种不同强度的物理连接证据：

```text
Direct Handshake Connector
Handshake Transport Path
```

它们都不做语义命名。

## `HandshakeConnector`

要求两个 endpoint 之间同时存在直接：

$$
A.valid \rightarrow B.valid
$$

以及：

$$
B.ready \rightarrow A.ready
$$

且中间不能跳过 gate、arbiter 或 register。

适合 parent/child 的简单直连。

## `discover_direct_handshake_connectors()`

对 concrete design events 两两检查 direct `DATA/ALIAS` edge。

“reachable”不会被误报成“direct”。

## `HandshakeTransportPath`

v6 新增，用于真实 Chipyard 中跨很多中间模块的 Decoupled channel。

保存：

```text
from_event
to_event
valid_path
ready_path
instances
stateful_instances
```

完整 transport 必须同时证明：

$$
source.valid \rightarrow^* sink.valid
$$

以及：

$$
sink.ready \rightarrow^* source.ready
$$

只找到 valid 而找不到 ready/backpressure 不算完整 connector。

## `discover_handshake_transport_path()`

约束 source 必须是结构上的 `SEND` event，sink 必须是 `RECEIVE` event。

内部使用 `LazyDesignExplorer`，而不是完整 flatten whole design。

为了避免 BOOM core 的巨大 fanout/fanin，搜索从两个 endpoint 中 hierarchy 较浅的一侧开始：

- 如果 physical source 更浅，forward search；
- 如果 physical target 更浅，reverse search。

这不改变 edge 方向，只改变 BFS 的起点。

## `stateful_instances`

如果选中的 valid/ready path 经过 register 或 memory leaf，记录对应 concrete instance。

真实 `SmallBoomV4Config` 的 B/C transport 会经过多个 TileLink Queue，因此 route 不是“同周期 wire alias”，而包含真实 buffering/backpressure state。

## 语义边界

即使 route 完整，也只证明：

> 两个 physical endpoint 由这条硬件依赖链连接。

它**不证明**：

- 两端 occurrence 是同一个 cycle；
- 两端是同一个 architectural transaction；
- source/sink 的 opcode 语义相同；
- 可以把它们直接 alias 成一个 µMCM event。

这些更强语义必须在后续协议/形式层证明。
