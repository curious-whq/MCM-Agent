# `mcm/project.py`

## 文件职责

`project.py` 负责普通 strict-order case 的 boundary projection。

核心模式是：

$$
A < x < y < B
$$

其中 $x,y$ 是内部事件。通过传递闭包恢复 $A<B$，然后隐藏内部端点。

v1.1 中 projection 同时保留 `EventRef` 的身份参数。例如：

$$
Req(r) < Internal(r) < Resp(r)
$$

投影后得到：

$$
Req(r) < Resp(r)
$$

不会变成无参数的 `Req < Resp`。

## `_transitive_closure(edges)`

计算有限 `Before` 图的严格传递闭包。

若：

$$
A<B,\quad B<C
$$

则加入：

$$
A<C
$$

图节点现在是 `EventRef`，所以不同 request occurrence 是不同节点。

## `_transitive_reduction_dag(edges)`

删除可由其它路径推出的冗余边，并检测 strict-order cycle。

若同时存在：

$$
A<B,\quad B<C,\quad A<C
$$

则显式的 $A<C$ 可被删除。

如果形成：

$$
A<B<C<A
$$

则抛出 `ValueError`。

## `_is_boundary(ref, boundary_event_kinds)`

根据 `EventRef.kind` 判断一个 occurrence 是否属于当前父模块边界。

例如 `RespOut(req=r,mshr=m)` 的 kind 是 `RespOut`，因此只要 `RespOut` 在 boundary kind 集合中，该 occurrence 就是边界可见的。

## `project_case(case, boundary_events)`

流程：

1. 对 `case.facts` 求传递闭包；
2. 只保留两个端点 kind 都属于 boundary 的 `Before`；
3. 做传递约简；
4. 保留原 guard；
5. 更新 provenance。

## 当前限制

该文件仍然只处理 strict-order DAG。queue/token conservation 由 `mcm/conservation.py` 单独处理；精确 cycle、value flow、地址关系等尚未进入该 projector。
