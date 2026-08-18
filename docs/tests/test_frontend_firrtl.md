# `tests/test_frontend_firrtl.py`

## 文件职责

验证 FIRRTL structural frontend 的基础能力。

## `test_source_locator_parses_from_right`

检查包含空格的 source path 仍能正确解析行列号。

## `test_bundle_orientation_flattens_nested_flips`

验证 nested `flip` 后的 leaf physical direction。

重点检查 Flipped Decoupled：

```text
io.req.valid -> input
io.req.ready -> output
io.req.bits  -> input
```

以及普通 Decoupled：

```text
io.rep.valid -> output
io.rep.ready -> input
```

## `test_vectors_are_flattened`

验证：

```text
UInt<8>[2]
```

会展开成：

```text
lane[0]
lane[1]
```

## `test_missing_circuit_is_rejected`

没有 `circuit` 的结构输入不能被当作完整 design。
