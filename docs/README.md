# MCM-Agent 文档

本目录按源码文件一一维护设计说明。

当前 Prototype v3 已覆盖四类 abstraction primitive：

1. ordering/FSM elimination；
2. queue/token conservation；
3. exceptional state-case preservation；
4. exact timing-case preservation。

## 对应关系

| 源文件 | 文档 |
| --- | --- |
| `.gitignore` | `docs/gitignore.md` |
| `mcm/ir.py` | `docs/mcm/ir.md` |
| `mcm/project.py` | `docs/mcm/project.md` |
| `mcm/merge.py` | `docs/mcm/merge.md` |
| `mcm/conservation.py` | `docs/mcm/conservation.md` |
| `mcm/statecase.py` | `docs/mcm/statecase.md` |
| `mcm/timing.py` | `docs/mcm/timing.md` |
| `examples/boom_probe.py` | `docs/examples/boom_probe.md` |
| `examples/boom_mshr.py` | `docs/examples/boom_mshr.md` |
| `examples/boom_b1.py` | `docs/examples/boom_b1.md` |
| `examples/xiangshan_metaarray.py` | `docs/examples/xiangshan_metaarray.md` |
| `tests/test_probe.py` | `docs/tests/test_probe.md` |
| `tests/test_mshr.py` | `docs/tests/test_mshr.md` |
| `tests/test_b1.py` | `docs/tests/test_b1.md` |
| `tests/test_xiangshan_timing.py` | `docs/tests/test_xiangshan_timing.md` |
| `pyproject.toml` | `docs/pyproject.md` |

v3 完成后，下一阶段重点应从继续扩 IR 转向自动化 frontend：层次、边界事件和静态切片。
