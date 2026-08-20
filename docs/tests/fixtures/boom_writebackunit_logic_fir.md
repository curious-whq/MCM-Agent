# `tests/fixtures/boom_writebackunit_logic.fir`

## Fixture 作用

为 `BoomWritebackUnit` workflow/formal regression 提供可重复的 FIRRTL logic fixture。

该 fixture 保留 writeback request、metadata/data request、beat counter/pipeline、response/writeback completion 等与 µMCM ordering/identity/indexed conservation 相关的控制与数据依赖，使测试无需依赖完整 Chipyard build 即可重放 WritebackUnit prover 行为。

与 `boom_writeback_candidate_umcm.json` 配套使用时，前者是 concrete RTL grounding，后者是 candidate semantic abstraction；测试必须通过 validator/formal backend 才能建立 trust。
