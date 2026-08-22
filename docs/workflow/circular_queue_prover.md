# `workflow/circular_queue_prover.py`

## 文件职责

为没有 per-slot valid array、而使用 enqueue/dequeue pointer 加 full/empty discriminator 的有限 circular FIFO 提供 strict same-index history proof。

prover 不匹配模块名或接口名。它从 candidate occurrence 的 index metadata 与 pointer writer 恢复 enqueue/dequeue advance action，只保留有限、显式 reset 的 scalar control state，然后穷举 FIRRTL next-state transition。同时维护只存在于 certificate 中的 slot-token mask：

```text
before(i)  -> create ghost token i
after(i)   -> require and consume existing ghost token i
```

同周期先检查/消费旧 token，再创建新 token，因此证明的是严格 `before(i) <mu after(i)`，不会把同周期 occurrence 当作历史来源。

对于 filtered queue，目标 occurrence 可以是 dequeue advance 的子事件，例如 invalid-head skip。prover 会独立证明 `target => dequeue_advance`，并要求存在与 pointer action 精确等价的 indexed occurrence，以及 action 与 full/empty predicate 的 exact exclusion certificate。这样可以安全排除未 reset payload、branch mask 和 per-slot valid data，而不丢掉 occupancy history。

## Fail-closed bounds

- zero-based 1–16 slot index domain；
- circular pointer bit-domain必须与 slot domain 完全一致；
- 所有参与状态必须有显式有限 reset value；
- 总 RTL control state 不超过 16 bit；
- input frontier 必须是最多 8 个 Boolean signals；
- ghost reachability 最多 200000 states。

超出边界、无法闭合 writer/control cone 或发现无 token dequeue 时分别返回 `STRUCTURAL_UNKNOWN` 或具体 `COUNTEREXAMPLE`。
