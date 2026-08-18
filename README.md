# MCM-Agent — Prototype v2

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

The current implementation is deliberately manual: no RTL parser and no LLM Agent yet. The goal is to validate the abstraction language and algorithms first.

## Implemented abstraction primitives

### v0: ordering/FSM projection

Internal paths are closed transitively, internal events are hidden, and boundary-equivalent guarded cases may be merged.

### v1/v1.1: resource/token conservation

A manually supplied queue/token invariant can be projected into a boundary lifecycle summary. Symbolic event occurrences carry request/scope identity such as:

```text
ReqAccept(req=r,mshr=m)
RespOut(req=r,mshr=m)
GrantAck(mshr=m)
```

This prevents an event for request `s` from satisfying an obligation for request `r`.

### v2: exceptional state-case preservation

BOOM B1 is hand-modeled with predicates bound to a concrete symbolic load:

```text
Executed(load=O)
Succeeded(load=O)
```

and boundary/control outcomes:

```text
Kill(load=Y)
Allow(load=Y)
```

For the buggy state partition, the executed-but-not-succeeded state has the same outcome as completed execution and therefore summarizes to:

```text
Executed(O) -> Allow(Y)
```

For the fixed partition, unresolved states safely merge to:

```text
!Succeeded(O) -> Kill(Y)
```

The merge is exact boolean cube combination and never combines predicates belonging to different symbolic loads.

## Run

```bash
python -m unittest discover -s tests -v
```

## Next

The next stress test is a timing-sensitive XiangShan case, which will require exact timing relations such as `SameCycle` and `Next`.
