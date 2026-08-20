# `.gitignore`

## 文件职责

避免 Python 自动生成文件和本地工具目录进入 Git 仓库。

当前忽略：

```text
__pycache__/
*.py[cod]
.pytest_cache/
tools/
```

其中 `tools/` 用于本地工具/外部依赖，不应作为 MCM-Agent 源码的一部分提交。

注意：已经被 Git 跟踪的缓存文件不会因为修改 `.gitignore` 自动消失。如果仓库历史中已有 `__pycache__`，需要显式移出索引，例如：

```bash
git rm -r --cached mcm/__pycache__ examples/__pycache__ tests/__pycache__
```

只对实际存在且已经被跟踪的目录执行即可。
