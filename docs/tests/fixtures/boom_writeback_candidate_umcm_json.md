# `tests/fixtures/boom_writeback_candidate_umcm.json`

## Fixture 作用

真实 `BoomWritebackUnit` 的 `umcm-formal-0.5` candidate fixture，用于 WritebackUnit 的 semantic/formal regression。

它包含 boundary 与 derived occurrences、persistent predicates/identity/cases/axioms；其中多拍 writeback 数据路径使用 bounded `beat` index（例如 `data_req_cnt` / `r2_data_req_cnt`，domain `[0, 8)`），用于验证 indexed occurrence、same-index history 与 payload/identity proof。

这是候选输入，不等于 trusted summary。是否进入 `trusted_umcm.json` 仍由 grounding + semantic/formal validation 决定。
