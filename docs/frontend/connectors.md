# `frontend/connectors.py`

## 文件职责

静态发现 concrete design 中两个 Decoupled endpoint 之间的**直接 handshake connector**。

这一层用于解决后续全局事件一致性问题：如果 parent/child 之间只是 valid/ready 直接连线，我们不需要让 LLM 猜它们是否属于同一条物理传递链。

## `HandshakeConnector`

记录：

```text
from_event
to_event
valid_edge
ready_edge
```

一个 connector 必须同时满足：

```text
from.valid -> to.valid
```

以及反向 ready flow：

```text
to.ready -> from.ready
```

## `_direct_edge()`

只接受 `DATA` 或 `ALIAS` 的直接 dependency edge。

不会跳过：

- mux；
- gate；
- arbiter；
- register；
- 未知组合逻辑。

## `_link_orientation()`

检查一对 endpoint 的 valid/ready 是否形成完整 Decoupled 传递方向。

## `discover_direct_handshake_connectors()`

对 concrete design events 两两检查 direct connector。

关键保守性：

> reachability 不等于 direct connector。

如果 BOOM 的某条 channel 中间有 `lrsc_valid` gate 或 TL arbiter，v5 不会错误把两个 endpoint 声明成 direct connector；这些控制条件留在 hierarchical dependency slice 中。

因此 connector discovery 负责“可以机械证明的直连”，复杂协议传递仍由静态 dependency graph 表达。
