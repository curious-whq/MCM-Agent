# `examples/boom_mshr.py`

## 文件职责

该文件手工构造 BOOM MSHR/RPQ 的 resource-conservation 实验，并在 v1.1 中显式加入 request identity。

## `BOUNDARY`

父层当前可见的 event kind：

```text
ReqAccept
RespOut
ReplayOut
Kill
GrantAck
```

## 符号身份

实验定义：

```python
R = "r"
M = "m"
```

其中 $r$ 表示某个符号请求，$m$ 表示某个符号 MSHR 实例。

对应 occurrence 包括：

```text
ReqAccept(r,m)
RPQEnq(r,m)
RespOut(r,m)
ReplayOut(r,m)
Kill(r,m)
GrantAck(m)
```

## `mshr_rpq_case()`

只提供 boundary 到内部 token 创建的 grounding：

$$
ReqAccept(r,m) < RPQEnq(r,m)
$$

最终父公理并没有直接写在该 case 中。

## `RPQ_CONSERVATION`

手工提供的 resource invariant：

```text
enter: RPQEnq(r,m)
exits: RespOut(r,m) | ReplayOut(r,m) | Kill(r,m)
barrier: GrantAck(m)
token key: req
scope key: mshr
```

由此 projection 生成：

$$
ReqAccept(r,m) < GrantAck(m)
\Rightarrow
\exists e\in\{RespOut(r,m),ReplayOut(r,m),Kill(r,m)\}.
ReqAccept(r,m)<e<GrantAck(m)
$$

## `disconnected_mshr_case()`

没有 boundary event 连接到 `RPQEnq(r,m)`，因此不能生成父 summary。

## `wrong_request_predecessor_case()`

故意构造：

$$
ReqAccept(s,m) < RPQEnq(r,m)
$$

虽然图上存在一条 ordering edge，但 request identity 不匹配，所以 v1.1 必须拒绝把 `ReqAccept(s,m)` 当作 request $r$ 的 boundary start。
