# MCM-Agent 文档

本目录按源码文件一一维护设计说明。

当前项目分成两个阶段：

```text
手工 abstraction prototype
    v0 ordering/FSM
    v1 resource/token
    v2 state case
    v3 timing case

自动化 frontend
    v4 FIRRTL structural frontend
```

## v4 frontend

```text
FIRRTL / CHIRRTL
      ↓
Structural Parser
      ↓
Hierarchy Discovery
      ↓
Boundary Leaf Discovery
      ↓
Physical Event Registry
      ↓
Source Locator / Scala provenance
```

v4 仍然不生成 µMCM，也不使用 LLM。

新增文件对应关系：

| 源文件 | 文档 |
| --- | --- |
| `frontend/__init__.py` | `docs/frontend/init.md` |
| `frontend/model.py` | `docs/frontend/model.md` |
| `frontend/firrtl.py` | `docs/frontend/firrtl.md` |
| `frontend/hierarchy.py` | `docs/frontend/hierarchy.md` |
| `frontend/boundary.py` | `docs/frontend/boundary.md` |
| `frontend/registry.py` | `docs/frontend/registry.md` |
| `tests/test_frontend_firrtl.py` | `docs/tests/test_frontend_firrtl.md` |
| `tests/test_frontend_probeunit.py` | `docs/tests/test_frontend_probeunit.md` |
| `tests/fixtures/boom_probeunit.fir` | `docs/tests/fixtures/boom_probeunit_fir.md` |

已有 v0-v3 文档保持不变。
