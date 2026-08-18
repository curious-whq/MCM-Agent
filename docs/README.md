# MCM-Agent 文档

本目录按源码文件一一维护简要设计说明。每个文档说明文件职责、核心设计和主要类/方法。

## 当前对应关系

| 源文件 | 文档 |
| --- | --- |
| `mcm/__init__.py` | `docs/mcm/init.md` |
| `mcm/ir.py` | `docs/mcm/ir.md` |
| `mcm/project.py` | `docs/mcm/project.md` |
| `mcm/merge.py` | `docs/mcm/merge.md` |
| `mcm/conservation.py` | `docs/mcm/conservation.md` |
| `mcm/statecase.py` | `docs/mcm/statecase.md` |
| `examples/boom_probe.py` | `docs/examples/boom_probe.md` |
| `examples/boom_mshr.py` | `docs/examples/boom_mshr.md` |
| `examples/boom_b1.py` | `docs/examples/boom_b1.md` |
| `tests/test_probe.py` | `docs/tests/test_probe.md` |
| `tests/test_mshr.py` | `docs/tests/test_mshr.md` |
| `tests/test_b1.py` | `docs/tests/test_b1.md` |
| `pyproject.toml` | `docs/pyproject.md` |

## 当前三类抽象能力

1. ordering/FSM elimination；
2. queue/token conservation；
3. exceptional state-case preservation。

当前仍是手工构造 leaf case。RTL 抽取、LLM Agent 和形式化证明尚未接入。
