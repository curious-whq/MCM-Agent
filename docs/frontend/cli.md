# `frontend/cli.py`

## 文件职责

提供不写 Python 脚本也能运行的静态 frontend CLI。

运行方式：

```bash
python -m frontend.cli <command> ...
```

## `report`

```bash
python -m frontend.cli report design.fir
```

输出：

- input format/provenance；
- module coverage；
- unsupported statement 数量；
- event 数量。

## `events`

```bash
python -m frontend.cli events design.fir --module BoomProbeUnit
```

列出 module type 级别 physical handshake events。

## `design-events`

列出 concrete instance 级 event。

## `connectors`

```bash
python -m frontend.cli connectors design.fir
```

列出可以静态证明的 direct valid/ready endpoint connector。

## `tree`

```bash
python -m frontend.cli tree design.fir
```

输出 physical module hierarchy 加静态 state-region work units。

## `partition`

```bash
python -m frontend.cli partition design.fir --module BoomMSHR
```

输出 register SCC 和 event-cone candidate partition。

## `slice`

```bash
python -m frontend.cli slice design.fir \
  --module BoomProbeUnit \
  --event BoomProbeUnit.io.rep.fire \
  --mode full
```

生成 local static manifest。

可用：

```bash
--source-root /path/to/boom
```

把 source locator 解析成 Scala snippets。

## `design-slice`

```bash
python -m frontend.cli design-slice design.fir \
  --event DCacheTop::io.tl_c.fire \
  --payload
```

执行 concrete cross-module slice。

CLI 只调用 deterministic static pipeline，不包含 LLM。
