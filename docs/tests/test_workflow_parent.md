# `tests/test_workflow_parent.py`

## 测试目标

parent workflow 从 frozen child attachment 到 parent freeze 的完整回归。

主要覆盖：

- parent prompt 消费 frozen child semantics 而不含 child RTL；
- qualified child semantic IDs 可被 parent candidate 引用；
- parent 可以声明零条新 axiom，并仍冻结/保留 child import；
- 多个 frozen child 候选时 fail closed；
- proof-scope implementation fingerprint 与 instance path 无关；
- generic module theorem 可以在 verified equivalent child slots 上实例化；
- structural/proof-scope mismatch、ambiguous template 等 reuse 错误被拒绝；
- frozen parent 保持 transparent child semantic catalog 与 provenance。

该测试是 module theorem reuse 与 bottom-up parent synthesis 的主要 contract regression。
