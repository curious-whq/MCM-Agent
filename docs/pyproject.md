# `pyproject.toml`

## 文件职责

Python 项目配置。

Prototype v5 版本为 `0.0.7`。

当前 static frontend 仍只使用 Python 标准库，核心运行时没有第三方依赖。

要求 Python 3.11+，`pytest` 继续作为可选开发依赖。

## `[project.scripts]`

安装项目后提供：

```bash
mcm-static
```

它等价于：

```bash
python -m frontend.cli
```
