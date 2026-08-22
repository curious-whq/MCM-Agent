# `workflow/formal_patterns.py`

## 文件职责

提供 `explicit-control` 与 composition prover 共用的 exact symbolic pattern proofs。

该模块实现 FIRRTL alias/call 展开、Boolean normal form、有限 bit-vector bitblast、writer activation 与简单 SAT/UNSAT 枚举。它只在能够给出 exact structural certificate 时返回成功。

## 主要 proof helpers

- `prove_combinational_forbid_when()`
- `prove_conditional_signal_equality()`
- `prove_conditional_constant_bit()`
- `prove_same_cycle_occurrence_partition()`
- `prove_scalar_valid_token_provenance()`
- `prove_same_index_valid_token_provenance()`

pointer/full-empty 型 circular FIFO 的 same-slot history 由 `circular_queue_prover.py` 负责；它与这里的 valid-bit token provenance 是两种独立、互补的 certificate shape。

内部 Boolean helpers 也被 `composition_prover` 用来构造 parent-local occurrence bridge 和 onehot invariant。

conditional payload proof 会按 FIRRTL last-connect priority 收集所有 writer，并支持 record/vector aggregate projection 与透明 alias chain。对于 lowered handoff 只保留 leaf drives 的 bundle connect，它从 IO/memory/mport declaration 恢复完整字段集合，再逐字段生成 exact equality certificate；缺少任何字段都不会把局部相等提升成整包相等。高扇出的已 grounding Boolean control 可以作为保守 abstraction cut，避免反复展开大型 LSU cone。

典型 fail-closed 条件包括：额外 token creator、未知 writer activation、无法证明 mutually exclusive 的 mux arm、无法精确展开的 driver 或未建模的 guard。
