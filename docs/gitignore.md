# `.gitignore`

## 文件职责

避免 Python 自动生成文件进入 Git 仓库。

当前忽略：

```text
__pycache__/
*.py[cod]
.pytest_cache/
```

已经被 Git 跟踪的 `__pycache__` 不会因为新增 `.gitignore` 自动消失，需要额外执行：

```bash
git rm -r --cached mcm/__pycache__ examples/__pycache__ tests/__pycache__
```

如果某个目录不存在，可以只删除实际存在的目录。
