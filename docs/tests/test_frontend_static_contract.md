# `tests/test_frontend_static_contract.py`

## 文件职责

验证 v5 “LLM 前静态契约”的 corner cases 和安全属性。

## Input contract

- CHIRRTL 能正确识别；
- source locator 存在时 provenance ready；
- CIRCT FIRRTL-dialect MLIR 被明确检测并拒绝当前 parser。

## Fail-closed coverage

人为插入未知 executable statement，以及含 flip 的 aggregate partial connect，要求：

```text
coverage complete = false
assert_complete() 抛错
```

跨模块 slice 如果触达 incomplete child，也必须 `complete=false`。

## Dependency corner cases

验证动态 subaccess：

```text
vec[idx]
```

保留：

```text
vec[*]
idx as ADDRESS dependency
```

以及 CHIRRTL memory mport 的 address/memory-state dependency。

## Source mapping

检查 exact source span 读取以及 source-root 路径逃逸保护。

## CLI

检查 `report`、`tree` 与 `design-slice` 能输出结构化 JSON；`tree` 同时保留 physical module node 和 state-region work unit，`design-slice` 不包含静态阶段擅自生成的 semantic label。

## Static handoff

- complete + source-grounded slice 可以得到 `handoff.ready=true`；
- incomplete slice 必须在 LLM boundary 之前被阻断。
