# `workflow/priority_select_prover.py`

## 文件职责

为 `indexed_priority_select` 提供 fail-closed deterministic proof。它从 handoff 恢复 FIRRTL last-connect writer priority、组合 selector cone、无 reset 结果寄存器和输出 alias，并验证输入采样到寄存输出的固定一拍关系。

当前 exact backend 支持 1–12 个候选与一拍寄存输出；cyclic order 还要求 pivot 的完整 bit-domain 与 `index.count` 相同。非二次幂环形域在没有显式 domain constraint 时保持 `UNKNOWN`，不会把无效 pivot 编码静默当成合法索引。

## 当前证明域

- 1–12 个有限候选；
- `linear_min` / `linear_max`；
- `cyclic_predecessor` / `cyclic_successor`，支持 pivot-first 与 strict/pivot-last；
- packed bit-vector 或由 indexed arrays 通过 `and/or/not` 构造的 candidate；
- `{found,index}` 或仅 `index` 的寄存结果；index 可使用常量 bit/slice 投影；
- `latency_cycles: 1`；
- `implicit_unconstrained` result-register initialization。

证明器对 candidate source values 与完整 pivot bit-domain 做 exhaustive finite equivalence。候选为空时，若存在 `found` 则要求 `found=0`，index 不受约束；非空时要求可选 `found=1` 且 index 等于声明优先序的唯一 winner。无法恢复完整 writer/control cone 时返回 unknown；精确不一致时返回带 candidate source values、candidate mask、pivot 和实际/期望结果的 counterexample。

该实现不检查模块名、LSU 信号名或固定的 8-entry 结构。
