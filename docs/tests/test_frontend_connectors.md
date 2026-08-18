# `tests/test_frontend_connectors.py`

## 文件职责

验证 direct handshake connector discovery。

测试 fixture 中：

```text
DCacheTop.io.tl_b <-> DCacheTop.prober.io.req
DCacheTop.prober.io.rep <-> DCacheTop.io.tl_c
```

都是 valid/ready 直连，因此应该生成 connector。

同时验证 `meta_read` 等无关内部 channel 不会因为处于同一个 slice 或 module 就被误连到 TL C。
