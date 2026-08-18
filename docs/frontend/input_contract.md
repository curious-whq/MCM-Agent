# `frontend/input_contract.py`

## 文件职责

明确 v5 静态前端的输入契约，避免“FIRRTL”这个名字同时指 classic textual FIRRTL/CHIRRTL 和 CIRCT FIRRTL-dialect MLIR 时发生误解析。

## `InputFormat`

当前检测：

- `CHIRRTL`
- `FIRRTL_DIALECT`
- `UNKNOWN`

## `InputValidationReport`

保存：

```text
format
supported
has_source_locators
source_locator_count
reason
```

### `provenance_ready`

只有：

```text
输入格式受支持
AND
存在 source locator
```

时为 true。

这比“dependency parser 能跑”更严格，因为未来 LLM 需要能够回到 Scala source。

## `detect_input_format()`

通过明确的 grammar marker 区分：

```text
circuit Top :
```

与：

```text
firrtl.circuit ...
```

## `validate_static_input()`

v5 支持 textual CHIRRTL/classic FIRRTL surface syntax。

CIRCT FIRRTL-dialect MLIR 会得到清晰的 unsupported report，而不是被当前 parser 勉强解释。

## `require_supported_static_input()`

不满足 v5 input contract 时直接抛错。

## 为什么第一版优先 CHIRRTL

我们需要保留 `when`、aggregate、source locator 等较高层结构，方便构建 guard/control cone 和回映 Scala。

未来可以新增独立 CIRCT FIRRTL-dialect adapter，但不应把两套 grammar 混进同一个模糊 parser。
