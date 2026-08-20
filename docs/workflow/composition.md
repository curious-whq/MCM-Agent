# `workflow/composition.py`

## 文件职责

实现 frozen child µMCM 的发现、校验、语义命名空间导入，以及 verified module-instance theorem reuse。

## 两类 implementation identity

`work_unit_implementation_sha256()` 对当前 WorkUnit 的 proof surface 做 instance-path-independent canonical hash，保留 local FIRRTL、state/interface、event definition 与 child summary-slot shape，同时排除 source location、task metadata 和 composition artifact。

`frontend.workunit.module_structural_sha256()` 则给出 transitive generated-module-name-independent RTL hash。

generic module theorem template 只有在 source proof-scope hash 与 target structural hash 同时通过时才能复用。

## Frozen summary attachment

`attach_frozen_child_summaries()` 要求非 leaf parent 的每个 direct child slot 恰好得到一个 frozen summary：

- exact WorkUnit id 可以直接匹配；
- generic module theorem 可以在验证等价后实例化到 concrete child id；
- 多个候选、fingerprint mismatch、未冻结 summary 都 fail closed。

导入后产生 qualified semantic catalog，并把 imported boundary occurrences / predicates / identities / cases / axioms 写入 handoff grounding universe。

## 不重开 child RTL

parent synthesis 只消费 frozen semantics + parent-local RTL。template instantiation 会改写 instance prefix 与 nested imports，但不会重新分析 child implementation。
