# `frontend/module_cli.py`

## 文件职责

`frontend.module_cli` 是递归 Hierarchical WorkUnit planner 的独立 CLI，安装后入口为 `mcm-plan`。

它不生成 µMCM，也不调用 LLM；它只把 FIRRTL 解析结果转成可检查的层次化静态规划结果。

## 命令

```bash
mcm-plan module-tree <design.fir> [root/options]
mcm-plan module-stats <design.fir> [root/options]
mcm-plan module-plan <design.fir> [root/options]
```

- `module-tree`：输出 physical module + static region 的递归 WorkUnit 树；
- `module-stats`：输出每个 WorkUnit 的 raw/logical/replacement complexity；
- `module-plan`：输出 ownership、coverage、child summary replacement 等父层组合信息。

根节点必须在 `--root-instance` 与 `--root-module` 中二选一（也可以不显式指定时交给 planner 的默认约束处理）。完整 SoC FIRRTL 推荐使用 concrete `--root-instance`；模块级研究可用 `--root-module`。

## 复杂度配置

CLI 暴露 `WorkUnitConfig` 的主要阈值：source LOC、signals、registers、memories、events、dependency edges、statements、state SCC、coupling threshold 和 max depth。

超过阈值只代表“需要尝试切分”，并不意味着强制切分；真正的 cut 仍由 `frontend.workunit` 的结构与 ownership 规则决定。

## 大 FIRRTL

读取 FIRRTL 后调用：

```python
StaticFrontend.from_firrtl(text, eager=len(text) < 8_000_000)
```

因此超大输入会自动避开 eager 路径，保持与 whole-SoC frontend 的可扩展性策略一致。

## 与 workflow 的关系

`workflow.cli` 的 `leaf-task` / `parent-task` 也调用同一套 `build_hierarchical_work_unit()`。所以 `mcm-plan` 是可观察/调试入口，而不是另一套 planner 实现。
