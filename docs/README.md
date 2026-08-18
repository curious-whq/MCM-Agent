# MCM-Agent 文档

本目录按源码文件一一维护设计说明；每个主要源码、测试和 fixture 都有对应 Markdown。

Markdown 公式统一使用 `$...$` 或 `$$...$$`。

## 项目阶段

```text
v0  ordering/FSM abstraction
v1  queue/token conservation
v2  exceptional state cases
v3  exact timing cases
v4  structural FIRRTL frontend
v5  deterministic pre-LLM static pipeline
v6  real whole-Chipyard hardening + lazy physical transport routes
```

完整静态架构见：

```text
docs/frontend/static_pipeline.md
```

真实 `SmallBoomV4Config.fir` integration 结果见：

```text
docs/integration/real_chipyard_v6.md
```

## Frontend 源码对应关系

| 源文件 | 文档 |
| --- | --- |
| `frontend/__init__.py` | `docs/frontend/init.md` |
| `frontend/abstraction_tree.py` | `docs/frontend/abstraction_tree.md` |
| `frontend/input_contract.py` | `docs/frontend/input_contract.md` |
| `frontend/dependency.py` | `docs/frontend/dependency.md` |
| `frontend/connectors.py` | `docs/frontend/connectors.md` |
| `frontend/coverage.py` | `docs/frontend/coverage.md` |
| `frontend/slice.py` | `docs/frontend/slice.md` |
| `frontend/design_graph.py` | `docs/frontend/design_graph.md` |
| `frontend/partition.py` | `docs/frontend/partition.md` |
| `frontend/export.py` | `docs/frontend/export.md` |
| `frontend/source.py` | `docs/frontend/source.md` |
| `frontend/handoff.py` | `docs/frontend/handoff.md` |
| `frontend/pipeline.py` | `docs/frontend/pipeline.md` |
| `frontend/cli.py` | `docs/frontend/cli.md` |
| `frontend/firrtl.py` | `docs/frontend/firrtl.md` |

## Frontend 测试对应关系

| 测试/fixture | 文档 |
| --- | --- |
| `tests/test_frontend_abstraction_tree.py` | `docs/tests/test_frontend_abstraction_tree.md` |
| `tests/test_frontend_connectors.py` | `docs/tests/test_frontend_connectors.md` |
| `tests/test_frontend_dependency.py` | `docs/tests/test_frontend_dependency.md` |
| `tests/test_frontend_design_graph.py` | `docs/tests/test_frontend_design_graph.md` |
| `tests/test_frontend_partition.py` | `docs/tests/test_frontend_partition.md` |
| `tests/test_frontend_pipeline.py` | `docs/tests/test_frontend_pipeline.md` |
| `tests/test_frontend_mshr_static.py` | `docs/tests/test_frontend_mshr_static.md` |
| `tests/test_frontend_static_contract.py` | `docs/tests/test_frontend_static_contract.md` |
| `tests/test_frontend_transport.py` | `docs/tests/test_frontend_transport.md` |
| `tests/test_real_chipyard_firrtl.py` | `docs/tests/test_real_chipyard_firrtl.md` |
| `tests/fixtures/boom_probeunit_logic.fir` | `docs/tests/fixtures/boom_probeunit_logic_fir.md` |
| `tests/fixtures/boom_dcache_hierarchy.fir` | `docs/tests/fixtures/boom_dcache_hierarchy_fir.md` |
| `tests/fixtures/boom_mshr_logic.fir` | `docs/tests/fixtures/boom_mshr_logic_fir.md` |

v0-v4 已有文件的对应文档继续保留。

## LLM 边界

v6 仍不调用 LLM。

静态阶段先固定：

```text
physical hierarchy
physical event registry
signal/control/state dependencies
local semantic cones
end-to-end physical transport paths
coverage/provenance
```

只有静态 package 达到完整性要求后，未来 LLM 才允许解释 guarded cases 和 semantic aliases。
