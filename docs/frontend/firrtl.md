# `frontend/firrtl.py`

## 文件职责

解析 v5 使用的 **textual CHIRRTL/classic FIRRTL structural subset**。

当前支持现代 Chisel CHIRRTL 中常见的：

```text
FIRRTL version ...
circuit ...
public module ...
private module ...
extmodule ...
input/output
Bundle/Vec/flip
inst ... of ...
source locator
```

v4 主要用于结构恢复，v5 的 statement dependency 解析放在 `frontend/dependency.py`。

## `FirrtlParseError`

结构输入无法被明确解析时抛出。

## `_TypeParser`

轻量递归下降 type parser。

### `from_text()`

tokenize FIRRTL type。

### `parse()`

解析 ground/bundle 后继续处理 vector suffix。

### `parse_atom()`

解析 ground type 或 bundle。

### `parse_bundle()`

解析 field 与 `flip` orientation。

## `parse_type()`

把 textual type 转换成 `GroundType/BundleType/VectorType`。

## `_split_source()`

从 statement 尾部抽取：

```text
@[path/File.scala line:column]
```

## `parse_firrtl()`

生成 `Design`，只负责：

```text
top
modules
ports
instances
source locators
```

其它功能 statement 在这里不解析，避免 structural parser 和 dependency parser 相互污染。

## 输入边界

CIRCT 的 `firrtl.circuit` / SSA FIRRTL-dialect MLIR 不是本文件当前 grammar；由 `input_contract.py` 明确区分并暂时拒绝。
