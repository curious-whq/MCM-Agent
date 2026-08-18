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
v5  complete pre-LLM static pipeline skeleton
```

v5 的完整架构说明见：

```text
docs/frontend/static_pipeline.md
```

## v5 新增/扩展源码对应关系

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

## v5 测试对应关系

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
| `tests/fixtures/boom_probeunit_logic.fir` | `docs/tests/fixtures/boom_probeunit_logic_fir.md` |
| `tests/fixtures/boom_dcache_hierarchy.fir` | `docs/tests/fixtures/boom_dcache_hierarchy_fir.md` |
| `tests/fixtures/boom_mshr_logic.fir` | `docs/tests/fixtures/boom_mshr_logic_fir.md` |

v0-v4 已有文件的对应文档继续保留。

## LLM 边界

v5 仍不调用 LLM。

只有 `frontend/handoff.py` 判断：

```text
coverage complete
+ slice not truncated
+ source provenance available
```

后，才会输出 `handoff.ready=true` 的 deterministic package。

这使后续 Agent 的输入成为被静态分析约束的 slice，而不是整仓库代码或未经验证的 LLM 自由检索结果。
