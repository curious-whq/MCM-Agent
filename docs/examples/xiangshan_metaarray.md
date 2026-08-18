# `examples/xiangshan_metaarray.py`

## 文件职责

手工建模 XiangShan L1 Coh MetaArray 的真实 timing bug，用来验证 v3。

案例基于两个真实修复：

- `479d62af67bb20667ed2bec34a1dbe01ce8d6f9d`
- `63182363ed15d9b392e068d5fe34c523cbd55d5b`

第一个 commit 开启 `bypassRead`，但当时 bypass 检查的是上一拍保存下来的 `s1_way_wen/s1_way_waddr/s1_way_wdata`。

第二个 commit 增加 `s0_way_waddr/s0_way_wdata`，并让当前拍 `s0_way_wen` 也可以命中 read bypass。

## 符号事件

主要事件包括：

```text
MetaWrite(P,A,W)
MetaRead(L,A,W)
MetaResp(L,A,W)
RARRelease(P,A)
RARAlloc(L,A)
```

其中 $P$ 是 probe，$L$ 是 load。

## 公共时序背景

真实 bug 描述给出了：

- probe meta write 后一拍发生 RAR release；
- load s0 读取 meta；
- load s2 才申请进入 RAR queue；
- meta read response 在 load s1 获得。

因此手工 schedule 保留：

$$
Next(MetaWrite,RARRelease)
$$

$$
CycleDelta(MetaRead,RARAlloc,2)
$$

$$
Next(MetaRead,MetaResp)
$$

## `pre_final_fix_cases()`

比较两个 timing case。

### previous-cycle write

如果 write 比 read 早一拍：

$$
Next(MetaWrite,MetaRead)
$$

旧有 s1 bypass 能看到该 write，因此追踪的物理输出是：

$$
io.resp(L)=MetaWrite(P)
$$

### same-cycle write

如果：

$$
SameCycle(MetaWrite,MetaRead)
$$

在最终 s0 bypass 修复之前，该 write 不会进入旧的 s1 bypass 检查。

commit 说明明确指出此时 read 会拿到旧 meta，因此追踪：

$$
io.resp(L)=OldMeta(A,W)
$$

因为两个 timing case 的 boundary consequence 不同，v3 必须保留它们，不能合并。

## `final_fix_cases()`

最终 commit 增加 same-cycle s0 bypass 后，两种 timing 都得到：

$$
io.resp(L)=MetaWrite(P)
$$

因此 timing engine 可以把：

$$
\Delta(MetaWrite,MetaRead)=0
$$

和：

$$
\Delta(MetaWrite,MetaRead)=1
$$

精确合并为：

$$
\Delta(MetaWrite,MetaRead)\in\{0,1\}
$$

注意，这不是把 timing 信息全部删除，而是只删除已经证明对 boundary consequence 无影响的区分。
