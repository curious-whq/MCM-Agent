# `workflow/__init__.py`

## 文件职责

`workflow` 包的公共 API 汇总。包级 docstring 明确当前是 **provider-neutral manual-first µMCM synthesis workflow**：静态分析、prompt construction、结果解析与 validation 已经固定，当前 provider 是人工搬运 ChatGPT 对话，未来可以替换为 API provider 而不改变下游语义边界。

当前对外导出四组能力：

- schema：`UMCM_SCHEMA_VERSION`、candidate schema、response parser；
- handoff/task：static handoff、leaf task、parent task、版本常量；
- composition：frozen child summary attachment 与 semantic catalog；
- manual：task export/import 与 deterministic grounding validation。

内部 formal/semantic/composition prover 没有全部从包根导出，调用者应通过对应子模块使用。
