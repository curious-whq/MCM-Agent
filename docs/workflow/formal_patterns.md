# `workflow/formal_patterns.py`

## 文件职责

提供 `explicit-control` 与 composition prover 共用的 exact symbolic pattern proofs。

该模块实现 FIRRTL alias/call 展开、Boolean normal form、有限 bit-vector bitblast、writer activation 与简单 SAT/UNSAT 枚举。它只在能够给出 exact structural certificate 时返回成功。

## 主要 proof helpers

- `prove_combinational_forbid_when()`
- `prove_conditional_signal_equality()`
- `prove_same_cycle_occurrence_partition()`
- `prove_scalar_valid_token_provenance()`
- `prove_same_index_valid_token_provenance()`

内部 Boolean helpers 也被 `composition_prover` 用来构造 parent-local occurrence bridge 和 onehot invariant。

典型 fail-closed 条件包括：额外 token creator、未知 writer activation、无法证明 mutually exclusive 的 mux arm、无法精确展开的 driver 或未建模的 guard。
