# `frontend/__init__.py`

## 文件职责

统一导出 static frontend 的公共 Python API。

当前覆盖：

```text
input contract
structural model/parser
hierarchy
boundary/event registry
lazy/eager dependency graph
coverage ledger
local slice
hierarchical design graph
lazy dependency path explorer
direct handshake connector
end-to-end handshake transport
state partition
abstraction tree
manifest/source mapping
pre-LLM handoff
pipeline orchestration
```

v6 新增导出的关键接口包括：

```text
ModuleGraphProvider
DependencyPath
LazyDesignExplorer
HandshakeTransportPath
discover_handshake_transport_path
backward_design_slice_lazy
build_instance_hierarchy_index
```

这些对象仍然都是 deterministic static primitives，不包含 LLM 调用。

v6 真实 SoC hardening 还导出：

```text
backward_instance_slice_lazy
build_instance_static_handoff
```

前者固定 concrete ownership subtree 的 semantic cone，后者把 complete + source-grounded 的 subtree package 作为未来 LLM 的推荐输入。
