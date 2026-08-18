# `frontend/source.py`

## 文件职责

把 FIRRTL source locator 真正解析成用户本地仓库里的 Scala source snippet。

静态 manifest 里的：

```text
src/main/scala/v4/lsu/dcache.scala:145-210
```

只有经过这个 mapper 才变成未来 LLM 可以读取的真实源码文本。

## `SourceResolutionError`

locator 无法安全映射到给定 source roots 时抛出。

## `SourceSnippet`

保存：

```text
logical_file
resolved_file
start_line
end_line
text
```

## `SourceMapper`

### `from_roots()`

显式指定一个或多个 source root，例如 BOOM repo root / Chipyard generated source root。

### `resolve()`

只在指定 root 内解析 locator。

它不会：

- 网络搜索同名文件；
- 猜另一个路径；
- 允许 `../../` 跳出 source root。

### `snippet()`

读取一个 `SourceSpan`，可以增加固定 context lines。

### `snippets()`

批量读取 slice 中所有 source spans。

## `snippet_dict()`

把 snippet 转成 JSON-ready dictionary。

这个模块是我们所说的：

```text
FIRRTL node
→ source locator
→ exact Scala context
```

映射链的最后一步。
