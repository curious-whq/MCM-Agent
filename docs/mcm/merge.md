# `mcm/merge.py`

## 文件职责

`merge.py` 在 case 完成 boundary projection 后负责 alias normalization 和保守 merge。

原则是：只有 boundary consequence 真正相同的 case 才能合并。

## `normalize_case(case, aliases)`

对每个 `Before` 的两个端点调用 `AliasMap.normalize()`。

v1.1 中 alias 保留 occurrence 参数。例如：

$$
ProbeAck(req=r) \mapsto ProbeResponse(req=r)
$$

因此不会因为 alias 而把 request $r$ 和 request $s$ 混为一谈。

如果 alias 后产生同一 occurrence 的自环，则该 relation 被删除。

## `_guards_cover_true(guards)`

当前只识别最保守的一种完整 case split：

$$
P
$$

和：

$$
\neg P
$$

如果二者 consequence 相同，则 guard 可被合并成 $true$。

一般布尔最小化暂未实现。

## `merge_equivalent_cases(cases)`

先按完整 normalized `facts` 分组。由于 `facts` 里的 endpoint 已经是 `EventRef`，身份参数也是 consequence 等价判断的一部分。

因此：

$$
RespOut(r) < X
$$

与：

$$
RespOut(s) < X
$$

不会被视为相同 consequence。

只有 fact set 完全一致，并且 guard 恰好构成当前支持的互补全集时才合并。
