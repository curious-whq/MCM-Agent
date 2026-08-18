# `frontend/__init__.py`

## 文件职责

统一导出当前 static frontend 的公共 API。

v5 已覆盖：

```text
input contract
structural model/parser
hierarchy
boundary/event registry (Decoupled + Valid)
dependency graph
coverage ledger
local slice
hierarchical design graph
direct handshake connectors
state partition
physical hierarchy + state-region abstraction tree
manifest export
source mapping
pre-LLM handoff
pipeline orchestration
```

CLI 通过：

```bash
python -m frontend.cli
```

单独使用，不作为 `__init__` 的核心库接口导出。
