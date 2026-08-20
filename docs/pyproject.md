# `pyproject.toml`

## 文件职责

Python 项目配置与命令行入口定义。

当前项目版本为 `0.0.9`，要求 Python 3.11+。核心运行时仍只依赖 Python 标准库；`pytest>=8` 作为可选开发依赖。

## `[project.scripts]`

安装项目后提供三个入口：

```bash
mcm-static
mcm-plan
mcm-agent
```

分别等价于：

```bash
python -m frontend.cli
python -m frontend.module_cli
python -m workflow.cli
```

职责划分如下：

- `mcm-static`：底层 FIRRTL/static frontend 调试与导出入口；
- `mcm-plan`：递归 Hierarchical WorkUnit planner，输出 module tree / stats / plan；
- `mcm-agent`：manual-first µMCM 工作流，负责 leaf/parent task、manual import、semantic/formal validation、freeze、run summary 与跨会话 handoff。

因此当前工程已经不再是旧文档所描述的“仅 v6 static frontend”。`pyproject.toml` 同时暴露静态 planner 与完整 manual-first workflow。
