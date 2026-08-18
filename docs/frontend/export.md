# `frontend/export.py`

## 文件职责

把静态分析结果序列化成确定性的 JSON manifest，作为未来 LLM 之前的机器接口。

当前 schema：

```text
mcm-agent.static-slice.v1
```

## 设计原则

manifest 中保留：

- physical event grounding；
- dependency graph；
- statements；
- source locators/spans；
- coverage completeness；
- boundary frontier。

同时显式保留：

```json
"semantic_labels": []
```

表示静态阶段没有擅自生成 `ProbeRecv`、`Visible` 等语义事件。

## `slice_manifest_dict()`

导出 module-local slice。

主要字段：

```text
event
analysis
signals
edges
statements
source_spans
unsupported_statements
semantic_labels
```

## `slice_manifest_json()`

生成稳定排序的 JSON 文本。

## `write_slice_manifest()`

把 local manifest 写入文件。

## `design_slice_manifest_dict()`

导出 cross-module concrete design slice。

额外保留：

```text
top
instance_path
instances
incomplete_instances
flat signal ids
concrete statement refs
```

它是未来处理 L1 内部 ProbeUnit/MSHR/Writeback 组合，乃至 L1-L2 跨模块分析的静态输入形式。
