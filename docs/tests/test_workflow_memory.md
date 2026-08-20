# `tests/test_workflow_memory.py`

## 测试目标

验证 experiment memory 与跨会话 handoff 不依赖聊天上下文。

覆盖：

- `SUMMARY.md` 保留 validation levels、rendered axioms、unresolved 与 certified provenance；
- 初始化不会覆盖已有 `EXPERIENCE.md`；
- `CURRENT_HANDOFF` 包含 repository research decisions + recent run summary，并带 new-conversation operating rule；
- `GOAL/METHOD/DECISIONS/LESSONS/ROADMAP_3W/STATUS` 六个 research memory 文件必须存在。
