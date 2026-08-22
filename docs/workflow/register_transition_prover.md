# `workflow/register_transition_prover.py`

## 文件职责

为 `register_transition` 提供 fail-closed deterministic proof。该 AST 表达的是 `register(t+1)`，不是同周期 signal equality。

证明器恢复本地寄存器的完整 FIRRTL last-connect writer cone，并将 Formal AST 中最高到最低的 `first_match` guarded updates 与 `default` 逐项比较。当前支持 1–12 bit 寄存器、`signal`/Boolean guards、常量、保持和 `modular_increment`。

枚举采用 guard-partitioned exact strategy：先完整枚举寄存器状态与 Boolean guards，再只在当前 first-match 分支实际读取 data-valued redirect input 时枚举该数据。总实际 checked rows 仍 fail-closed 限制为 `2^20`。这避免多个互斥 writer 的宽 payload 做无意义笛卡尔积，同时保持逐 valuation 的完整等价证明；若 RTL 选择了需要未声明数据的不同 writer，求值失败并返回 unknown，而不会误证。

对 BOOM LSU 的 `ldq_tail`，完整优先级是：清零 writer、branch-recovery redirect、正常 enqueue modular increment、默认保持。Handoff 的 proof-only `state_writer_control_statements` 保存跨 WorkUnit 边界的 enclosing `when/else`，用于证明 writer polarity，但不进入 LLM evidence 或 leaf 所有权。

缺少 writer control context 时返回 unknown；错误的 writer 顺序或 next expression 返回带输入 valuation 的 counterexample。
