# `tests/test_workflow_formal_patterns.py`

## 测试目标

真实 `BoomMSHR.rpq.main` 上 exact formal pattern prover 的回归。

当前 refined candidate（删除已知过强的 aggregate equality A9）应有 9 条 axiom 全部 formally proved，其中 combinational exclusions 使用 `exact-combinational-exclusion`，indexed queue history 使用 `exact-indexed-valid-token-provenance`。

负向测试把 QueueFull grounding 或 `valids[...]` writer 改坏，确认：逻辑上不再互斥时不能给结构 certificate；出现 unaccounted token creator 时 same-index provenance 必须 fail closed。

测试同时覆盖 `LSU.stq_execute_queue` 的 aggregate bundle equality 与 pointer/full-empty circular queue provenance。真实 Queue4 必须得到 `exact-circular-queue-slot-provenance`；若破坏 empty gate，该证明必须 fail closed。

`LSU.retry_queue` 覆盖 filtered circular queue：`InvalidHeadSkip` 被提升到同 slot 的 `HeadAdvance` 来证明，因此 branch/flush 清掉的 valid bit 和未 reset 的 payload/uop state 不会被错误纳入 occupancy proof。破坏 `HeadAdvance => !QueueEmpty` 后 A11 必须不再 trusted。
