# `examples/boom_mshr.py`

## 文件职责

Prototype v1/v1.1 的 BOOM MSHR/RPQ 手工案例。

事件现在带符号身份：

```text
ReqAccept(req=r,mshr=m)
RPQEnq(req=r,mshr=m)
RespOut(req=r,mshr=m)
GrantAck(mshr=m)
```

`mshr_rpq_case()` 只提供 boundary request 到 internal RPQ entry 的 grounding。

`RPQ_CONSERVATION` 手工描述 token 生命周期：

$$
RPQEnq(r,m)
\rightarrow
RespOut(r,m) \lor ReplayOut(r,m) \lor Kill(r,m)
$$

且 `GrantAck(m)` 只能在该 token 已离开后发生。

最终 summary 中所有 request-specific exit 都必须属于同一个 $r$。
