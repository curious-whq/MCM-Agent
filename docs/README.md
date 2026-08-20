# MCM-Agent 文档

本目录按**维护型源码/测试/fixture**维护明确的文档归属。对于 run 产物、缓存、压缩快照等生成物，不强制一文件一篇 Markdown，而是在本索引中记录生成来源与维护规则。

当前 Python package 版本：`0.0.9`。

## 当前架构阶段

```text
v0-v3  µMCM ordering/conservation/state/timing prototypes
v4     structural FIRRTL frontend
v5     deterministic pre-LLM static pipeline
v6     whole-Chipyard hardening + lazy physical transport
v7-v10 recursive Hierarchical WorkUnit planner + logical/replacement complexity
v11    transitive structural implementation fingerprint

manual-first-workflow-0.9
  leaf semantic abstraction
  -> grounding
  -> Formal AST validation
  -> formal trust
  -> freeze
  -> frozen child composition
  -> parent synthesis/composition proof
```

当前 µMCM schema 为 `umcm-formal-0.5`。manual-first 表示 LLM provider 仍由人工搬运对话，不表示后续 validation/composition 是人工流程。

## Frontend 源码对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `frontend/__init__.py` | `docs/frontend/init.md` |
| `frontend/abstraction_tree.py` | `docs/frontend/abstraction_tree.md` |
| `frontend/boundary.py` | `docs/frontend/boundary.md` |
| `frontend/cli.py` | `docs/frontend/cli.md` |
| `frontend/connectors.py` | `docs/frontend/connectors.md` |
| `frontend/coverage.py` | `docs/frontend/coverage.md` |
| `frontend/dependency.py` | `docs/frontend/dependency.md` |
| `frontend/design_graph.py` | `docs/frontend/design_graph.md` |
| `frontend/export.py` | `docs/frontend/export.md` |
| `frontend/firrtl.py` | `docs/frontend/firrtl.md` |
| `frontend/handoff.py` | `docs/frontend/handoff.md` |
| `frontend/hierarchy.py` | `docs/frontend/hierarchy.md` |
| `frontend/input_contract.py` | `docs/frontend/input_contract.md` |
| `frontend/model.py` | `docs/frontend/model.md` |
| `frontend/module_cli.py` | `docs/frontend/module_cli.md` |
| `frontend/partition.py` | `docs/frontend/partition.md` |
| `frontend/pipeline.py` | `docs/frontend/pipeline.md` |
| `frontend/registry.py` | `docs/frontend/registry.md` |
| `frontend/slice.py` | `docs/frontend/slice.md` |
| `frontend/source.py` | `docs/frontend/source.md` |
| `frontend/workunit.py` | `docs/frontend/workunit.md` |

整体设计补充：`docs/frontend/hierarchical_work_units.md`。

## µMCM prototype 源码对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `mcm/__init__.py` | `docs/mcm/init.md` |
| `mcm/conservation.py` | `docs/mcm/conservation.md` |
| `mcm/ir.py` | `docs/mcm/ir.md` |
| `mcm/merge.py` | `docs/mcm/merge.md` |
| `mcm/project.py` | `docs/mcm/project.md` |
| `mcm/statecase.py` | `docs/mcm/statecase.md` |
| `mcm/timing.py` | `docs/mcm/timing.md` |

## Workflow 源码对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `workflow/__init__.py` | `docs/workflow/init.md` |
| `workflow/axiom_ir.py` | `docs/workflow/axiom_ir.md` |
| `workflow/cli.py` | `docs/workflow/cli.md` |
| `workflow/composition.py` | `docs/workflow/composition.md` |
| `workflow/composition_prover.py` | `docs/workflow/composition_prover.md` |
| `workflow/formal.py` | `docs/workflow/formal.md` |
| `workflow/formal_patterns.py` | `docs/workflow/formal_patterns.md` |
| `workflow/handoff.py` | `docs/workflow/handoff.md` |
| `workflow/manual.py` | `docs/workflow/manual.md` |
| `workflow/research_memory.py` | `docs/workflow/research_memory.md` |
| `workflow/schema.py` | `docs/workflow/schema.md` |
| `workflow/semantic.py` | `docs/workflow/semantic.md` |
| `workflow/tasks.py` | `docs/workflow/tasks.md` |

概念文档继续保留：

- `docs/workflow/manual_first_umcm.md`
- `docs/workflow/validation_trust_levels.md`
- `docs/workflow/conversation_handoff.md`

## Examples 对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `examples/boom_b1.py` | `docs/examples/boom_b1.md` |
| `examples/boom_mshr.py` | `docs/examples/boom_mshr.md` |
| `examples/boom_probe.py` | `docs/examples/boom_probe.md` |
| `examples/xiangshan_metaarray.py` | `docs/examples/xiangshan_metaarray.md` |

## Tests 对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `tests/test_b1.py` | `docs/tests/test_b1.md` |
| `tests/test_frontend_abstraction_tree.py` | `docs/tests/test_frontend_abstraction_tree.md` |
| `tests/test_frontend_connectors.py` | `docs/tests/test_frontend_connectors.md` |
| `tests/test_frontend_dependency.py` | `docs/tests/test_frontend_dependency.md` |
| `tests/test_frontend_design_graph.py` | `docs/tests/test_frontend_design_graph.md` |
| `tests/test_frontend_firrtl.py` | `docs/tests/test_frontend_firrtl.md` |
| `tests/test_frontend_mshr_static.py` | `docs/tests/test_frontend_mshr_static.md` |
| `tests/test_frontend_partition.py` | `docs/tests/test_frontend_partition.md` |
| `tests/test_frontend_pipeline.py` | `docs/tests/test_frontend_pipeline.md` |
| `tests/test_frontend_probeunit.py` | `docs/tests/test_frontend_probeunit.md` |
| `tests/test_frontend_static_contract.py` | `docs/tests/test_frontend_static_contract.md` |
| `tests/test_frontend_transport.py` | `docs/tests/test_frontend_transport.md` |
| `tests/test_frontend_workunit.py` | `docs/tests/test_frontend_workunit.md` |
| `tests/test_mshr.py` | `docs/tests/test_mshr.md` |
| `tests/test_probe.py` | `docs/tests/test_probe.md` |
| `tests/test_real_chipyard_firrtl.py` | `docs/tests/test_real_chipyard_firrtl.md` |
| `tests/test_workflow_boom_mshr.py` | `docs/tests/test_workflow_boom_mshr.md` |
| `tests/test_workflow_composition_prover.py` | `docs/tests/test_workflow_composition_prover.md` |
| `tests/test_workflow_formal_patterns.py` | `docs/tests/test_workflow_formal_patterns.md` |
| `tests/test_workflow_manual.py` | `docs/tests/test_workflow_manual.md` |
| `tests/test_workflow_memory.py` | `docs/tests/test_workflow_memory.md` |
| `tests/test_workflow_mmios.py` | `docs/tests/test_workflow_mmios.md` |
| `tests/test_workflow_occurrence_partition.py` | `docs/tests/test_workflow_occurrence_partition.md` |
| `tests/test_workflow_parent.py` | `docs/tests/test_workflow_parent.md` |
| `tests/test_workflow_semantic.py` | `docs/tests/test_workflow_semantic.md` |
| `tests/test_xiangshan_timing.py` | `docs/tests/test_xiangshan_timing.md` |

## Fixtures 对应关系

| 源文件 | 对应文档 |
| --- | --- |
| `tests/fixtures/boom_dcache_hierarchy.fir` | `docs/tests/fixtures/boom_dcache_hierarchy_fir.md` |
| `tests/fixtures/boom_mshr_logic.fir` | `docs/tests/fixtures/boom_mshr_logic_fir.md` |
| `tests/fixtures/boom_probeunit.fir` | `docs/tests/fixtures/boom_probeunit_fir.md` |
| `tests/fixtures/boom_probeunit_logic.fir` | `docs/tests/fixtures/boom_probeunit_logic_fir.md` |
| `tests/fixtures/boom_writeback_candidate_umcm.json` | `docs/tests/fixtures/boom_writeback_candidate_umcm_json.md` |
| `tests/fixtures/boom_writebackunit_logic.fir` | `docs/tests/fixtures/boom_writebackunit_logic_fir.md` |

## Root 配置/入口

| 文件 | 文档归属 |
| --- | --- |
| `.gitignore` | `docs/gitignore.md` |
| `pyproject.toml` | `docs/pyproject.md` |
| `README.md` | 项目总览，本身即文档入口 |

## 生成物与实验产物

以下文件/目录不采用“一文件一篇 Markdown”，因为其内容由 pipeline/run 自动产生：

- `runs/**`：每个 task directory 由 `task.json`、`prompt.md`、`static_handoff.json`、`validation.json`、`semantic_validation.json`、`trusted_umcm.json`、可选 `frozen_umcm.json`、`SUMMARY.md`、`EXPERIENCE.md` 自描述；生成/聚合逻辑见 `docs/workflow/manual_first_umcm.md` 与 `docs/workflow/research_memory.md`。
- `__pycache__/`、`*.pyc`、`.pytest_cache/`：Python/test cache，应由 `.gitignore` 排除，不建立语义文档。
- `MCMAgent.zip`：仓库快照/归档，不是维护型源码接口；若继续保留，应视为 release/snapshot artifact。
- `dcache_probe_slice.json`：static analysis 导出产物，语义归属 frontend slice/export pipeline，而不是独立 API。
- `plan.txt`、`run.txt`：实验/调试输出，不作为稳定源码接口；长期结果应迁移到 `runs/**/SUMMARY.md` 或 `docs/research/`。

## 文档同步规则

今后修改维护型文件时：

1. 新增 `frontend/`、`mcm/`、`workflow/`、`examples/`、`tests/` 或 `tests/fixtures/` 文件时，同步新增本索引中的对应文档；
2. 修改 public behavior、schema/version、proof domain、trust policy、CLI、artifact layout 或 ownership/composition 规则时，同步修改对应文档；
3. 纯重构若不改变可观察语义，可以只在审计中标记“reviewed / no doc change”；
4. generated artifacts 不复制成静态 docs，记录其生成器与 authoritative source 即可。
