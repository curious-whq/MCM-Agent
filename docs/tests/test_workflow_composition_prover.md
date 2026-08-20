# `tests/test_workflow_composition_prover.py`

## 测试目标

验证 `composition-prover` 在真实 `BoomMSHR.rpq` parent 上的 theorem composition、certificate provenance 与 fail-closed 条件。

覆盖的 proof method 包括 trusted-child lift、exact combinational exclusion、scalar valid-token provenance、occurrence-bridge history composition、trusted history transitivity。

同时验证：

- candidate 声明的 provenance 必须与 certificate-derived provenance 一致；
- freeze 必须保留 provenance，删除/过期 provenance 会被拒绝；
- token provenance 遇到额外 creator 必须失败；
- untrusted child theorem 不能参与 parent transitivity；
- same-clock bridge 缺失时相关 child lift/history proof 失败；
- exact inductive `onehot0` register invariant 能证明互斥 winner，并拒绝 non-exclusive winner。
