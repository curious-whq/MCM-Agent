# `frontend/__init__.py`

## 文件职责

定义 frontend 包的公共 API。

Prototype v4 的 frontend 暂时只负责静态结构恢复，不生成 µMCM 公理，也不调用 LLM。

当前导出：

- FIRRTL 结构模型；
- `parse_firrtl()`；
- hierarchy discovery；
- boundary discovery；
- Decoupled physical event registry。
