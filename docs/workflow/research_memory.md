# `workflow/research_memory.py`

## 文件职责

把实验状态从一次 ChatGPT 会话中抽离，形成可重建的 durable research memory。

## Repository research memory

固定读取：

```text
docs/research/GOAL.md
docs/research/METHOD.md
docs/research/DECISIONS.md
docs/research/LESSONS.md
docs/research/ROADMAP_3W.md
docs/research/STATUS.md
```

## Per-run memory

每个 run 使用：

- `EXPERIENCE.md`：只保存应跨会话保留的 INPUT/PROMPT/SCHEMA/VALIDATOR/MODEL/GENERALIZATION lessons；已有内容不会被初始化覆盖；
- `SUMMARY.md`：从 task/status/grounding/candidate/semantic/trusted files 确定性重建，包括 validation level、rendered axiom、certified provenance、unresolved 与 next action。

## Current handoff

`build_current_handoff()` 把 repository research docs 与最近的 run summary/experience 拼成一个 self-contained `CURRENT_HANDOFF.md`。run discovery 只向下一层扫描，避免无界遍历大型目录。

trusted status 只来自 machine artifacts；handoff prose 不能替代 `trusted_umcm.json` / formal validation。
