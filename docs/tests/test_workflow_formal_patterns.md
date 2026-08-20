# `tests/test_workflow_formal_patterns.py`

## 测试目标

真实 `BoomMSHR.rpq.main` 上 exact formal pattern prover 的回归。

当前 refined candidate（删除已知过强的 aggregate equality A9）应有 9 条 axiom 全部 formally proved，其中 combinational exclusions 使用 `exact-combinational-exclusion`，indexed queue history 使用 `exact-indexed-valid-token-provenance`。

负向测试把 QueueFull grounding 或 `valids[...]` writer 改坏，确认：逻辑上不再互斥时不能给结构 certificate；出现 unaccounted token creator 时 same-index provenance 必须 fail closed。
