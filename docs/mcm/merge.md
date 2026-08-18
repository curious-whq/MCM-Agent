# `mcm/merge.py`

## 文件职责

负责 v0 ordering case 的 alias normalization 和保守 merge。

## `normalize_case`

对 `Before` 两端做 event-kind alias，但保留 `EventRef` bindings。

因此：

```text
ProbeAck(req=r)
```

归一化后可以成为：

```text
ProbeResponse(req=r)
```

而不会变成另一个请求的 response。

## `_guards_cover_true`

当前 ordering engine 只识别最保守的：

$$
P
$$

和：

$$
\neg P
$$

两分支覆盖 $true$ 的情况。

v2 的多 literal guard 化简不在本文件实现，而放在独立 `statecase.py`。

## `merge_equivalent_cases`

只有 normalized boundary fact set 完全相同的 case 才可能合并。

这保证不同 boundary behavior 的特殊 case 不会被吞掉。
