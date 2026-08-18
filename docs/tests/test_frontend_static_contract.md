# `tests/test_frontend_static_contract.py`

## 文件职责

验证“LLM 前静态契约”的 corner cases 和 fail-closed 安全属性。

## Input contract

- textual CHIRRTL/classic FIRRTL 能识别；
- source locator 存在时 provenance ready；
- CIRCT FIRRTL-dialect MLIR 被显式检测并拒绝当前 textual parser。

## Fail-closed coverage

未知 executable statement 必须使：

```text
coverage complete = false
assert_complete() 抛错
```

跨模块 slice 如果触达 incomplete child，也必须 `complete=false`。

## v6 aggregate flow

旧版把含 `flip` 的 aggregate connect 直接判 unsupported。

v6 的测试改为验证 leaf orientation：

```text
connect b, a
```

对普通 `valid`：

$$
a.valid \rightarrow b.valid
$$

对 flipped `ready`：

$$
b.ready \rightarrow a.ready
$$

这样才能正确解析真实 TileLink/Diplomacy aggregate connect。

## FIRRTL 3.x spelling

测试：

```text
connect y, x
invalidate y
```

确保真实 Chipyard FIRRTL 3.x textual syntax 不会被误报 unsupported。

## Dependency corner cases

动态 subaccess：

```text
vec[idx]
```

必须保留：

```text
vec[*]
idx as ADDRESS dependency
```

同时验证 memory mport 的 address/memory-state dependency。

## Source mapping

检查 exact source span 读取以及 source-root 路径逃逸保护。

## CLI

检查 `report`、`tree`、`connectors`、`design-slice` 输出结构化 JSON，并保持静态阶段没有 semantic label。

`route` 的专门测试位于 `tests/test_frontend_transport.py`。

## Static handoff

- complete + source-grounded slice 可以得到 `handoff.ready=true`；
- incomplete slice 必须在 LLM boundary 前被阻断。

## Ownership-scoped pre-LLM handoff

v6 追加验证：

- `build_instance_static_handoff()` 对 complete、source-grounded subtree 产生 `ownership_scoped=true`；
- manifest 仍然保持 `semantic_labels=[]`；
- 人为把 `max_signals` 降到不足时，必须抛出 `HandoffNotReadyError`，不能把被截断的 subtree 交给 LLM。

CLI regression 还检查 `design-events` 只接受一个 FIRRTL positional argument，避免大设计命令行 schema 意外重复参数。
