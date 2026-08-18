# `frontend/cli.py`

## 文件职责

提供 deterministic static frontend 的终端接口。

安装后可使用：

```bash
mcm-static <command> ...
```

也可以：

```bash
python -m frontend.cli <command> ...
```

## 大设计 lazy mode

CLI 读取 large FIRRTL 后自动选择 lazy frontend，避免命令一启动就构造整个 Chipyard dependency graph。

## `report`

```bash
mcm-static report design.fir \
  --module BoomProbeUnit \
  --module BoomMSHR \
  --module InclusiveCache
```

`--module` 可重复，用于 coverage-driven hardening。

## `events` / `design-events`

分别列 module-type event 和 concrete instance event。

## `route`

v6 新增：

```bash
mcm-static route design.fir \
  --from-event 'SEND_EVENT_ID' \
  --to-event 'RECEIVE_EVENT_ID'
```

输出：

```text
valid dependency path
ready/backpressure dependency path
visited signal count
truncation status
incomplete instances
all route instances
stateful route instances
source locators
semantic_labels = []
```

可用：

```bash
--max-signals 250000
--source-root /path/to/chipyard
```

`--max-signals` 达到上限仍未找到路径时，结果会 `truncated=true` / `complete=false`，不会把 budget exhaustion 当作“不存在路径”的证明。

## `slice` / `design-slice`

`slice` 做 local event cone，`design-slice` 做跨 module semantic cone。

对完整 Chipyard，`design-slice` CLI 默认使用 5,000-signal fail-closed budget；如果 cone 更大，会返回 `truncated=true`，用户可显式调高 `--max-signals`。这比默认无界增长更安全。

它们和 `route` 的职责不同：route 证明 transport，slice 恢复所有 upstream influence。

## `connectors`

列出 direct valid/ready connectors。对大 whole-system design，如果只是想证明某两个远端 endpoint 的连接，优先使用 `route`。

## `tree` / `partition`

输出 physical hierarchy + state-region work units，以及 register-SCC/event-cone partition。

所有 CLI command 都只执行 deterministic static analysis，不调用 LLM。

## `instance-slice`

v6 真实 SoC 集成新增的推荐 semantic-cone 命令：

```bash
mcm-static instance-slice design.fir \
  --event 'FULL_CONCRETE_EVENT_ID' \
  --root 'OWNING_INSTANCE_PATH' \
  --payload
```

`--root` 可以省略，此时默认以 event 自己的 concrete instance 为 ownership root。

例如 ProbeUnit event：

```text
root = ...dcache.prober
```

只分析 ProbeUnit；如果希望把 DCache 作为当前 hierarchical work unit，则：

```text
root = ...dcache
```

允许 slice 进入 DCache-owned children，但在 DCache physical inputs 停止。

默认 `--max-signals 20000`。budget 耗尽时 manifest 显式 `truncated=true` / `complete=false`。

在完整 Chipyard 上，推荐优先级是：

```text
route
→ instance-slice
→ local slice/partition
```

而不是直接无界 `design-slice`。
