# MCM-Agent 文档

本目录与源码一一对应维护设计说明。每个源码/配置文件的文档说明：文件职责、设计思路、类与方法、当前限制。

当前版本为 Prototype v1.1，重点修复 v1 中“事件只有名字、没有动态请求身份”的问题。

## 源码与文档对应关系

| 源文件 | 文档 |
| --- | --- |
| `pyproject.toml` | `docs/pyproject.md` |
| `mcm/__init__.py` | `docs/mcm/init.md` |
| `mcm/ir.py` | `docs/mcm/ir.md` |
| `mcm/project.py` | `docs/mcm/project.md` |
| `mcm/merge.py` | `docs/mcm/merge.md` |
| `mcm/conservation.py` | `docs/mcm/conservation.md` |
| `examples/boom_probe.py` | `docs/examples/boom_probe.md` |
| `examples/boom_mshr.py` | `docs/examples/boom_mshr.md` |
| `tests/test_probe.py` | `docs/tests/test_probe.md` |
| `tests/test_mshr.py` | `docs/tests/test_mshr.md` |

`__pycache__` 等自动生成文件不维护对应文档。

## 当前三项关键设计

第一类是 ordering/FSM elimination：

$$
A < x < y < B
$$

若 $x,y$ 是内部事件，则父层可只保留 $A<B$。

第二类是 queue/token conservation：一个请求进入内部资源后不能凭空消失，父层 barrier 出现前必须经过允许的 exit。

第三项是 v1.1 新增的 symbolic event identity。我们不再把所有 `RespOut` 当成同一个事件，而是显式区分：

$$
RespOut(r,m) \neq RespOut(s,m)
$$

因此 request $s$ 的 response 不能被拿来证明 request $r$ 已离开 RPQ。
