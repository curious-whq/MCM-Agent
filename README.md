# MCM-Agent — Prototype v1.1

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

The current prototype is deliberately manual: it does not parse RTL and does not use an LLM. The goal is to first determine whether the abstraction language and projection rules are sound enough on real microarchitectural patterns.

## v0: ordering/FSM projection

The BOOM L1 Probe example validates:

> Preserve internal cases, project each case to the real module boundary, and merge cases only when their boundary consequences are equivalent.

The clean and dirty Probe paths both reduce to:

```text
ProbeRecv < ReleaseNotify < ProbeResponse
```

while a synthetic exceptional ordering is kept separate.

## v1: MSHR/RPQ resource conservation

The MSHR example adds a second abstraction primitive: queue/token lifetime projection.

A request accepted into an RPQ creates an internal token. The token remains live until response, replay, or kill, while `GrantAck` is only allowed after that token is gone.

## v1.1: symbolic event identity

v1 originally represented events only by names such as `RespOut`. That was insufficient because a response for request `s` must not discharge the RPQ token of request `r`.

v1.1 introduces `EventRef`, for example:

```python
EventRef.of("ReqAccept", req="r", mshr="m")
EventRef.of("RespOut", req="r", mshr="m")
EventRef.of("GrantAck", mshr="m")
```

The generated parent summary therefore refers to the same symbolic request and MSHR scope:

$$
ReqAccept(r,m) < GrantAck(m)
\Rightarrow
\exists e \in \{RespOut(r,m), ReplayOut(r,m), Kill(r,m)\}.
ReqAccept(r,m) < e < GrantAck(m)
$$

A `RespOut(s,m)` cannot satisfy the summary for request `r`.

## Run

```bash
python -m unittest discover -s tests -v
```

Current test count: 8.

## Current abstraction primitives

- strict-order/FSM projection through internal events;
- boundary alias normalization;
- conservative equivalent-case merge;
- per-token resource-conservation projection;
- symbolic event occurrence identity.

Not implemented yet: RTL extraction, LLM generation, formal proof of leaf invariants, exact-cycle timing relations, symbolic address relations, automatic resource-invariant synthesis, general guard minimization, and the BOOM B1 timing case.
