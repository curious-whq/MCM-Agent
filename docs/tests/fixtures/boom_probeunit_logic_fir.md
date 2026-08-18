# `tests/fixtures/boom_probeunit_logic.fir`

## 文件职责

ProbeUnit 风格的高层 CHIRRTL fixture，用于 dependency/slice 测试。

它保留：

- `public module`；
- source locators；
- Decoupled boundary；
- `state/req/way_en` registers；
- `tag_matches/is_dirty` control；
- ProbeUnit 风格状态转移；
- 一个与目标 event 无关的 `debug_unused`。

该 fixture 不是官方 BOOM emitted CHIRRTL，而是根据真实 `BoomProbeUnit` RTL 结构手工建立的测试输入。真实 BOOM integration 仍需要用户本地 elaboration。
