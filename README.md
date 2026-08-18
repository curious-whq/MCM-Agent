# MCM-Agent — Prototype v0

This repository studies bottom-up synthesis of hierarchical microarchitectural memory-model axioms.

The first prototype is deliberately manual. It does **not** parse RTL and does **not** use an LLM. It tests one core idea:

> Preserve internal cases, project each case to the real module boundary, and merge cases only when their boundary consequences are equivalent.

## First example: BOOM L1 Probe handling

We manually encode two internal paths:

- non-dirty Probe path: `ReleaseNotify < ProbeAck`
- dirty writeback path: `ReleaseNotify < ProbeAckData`

At the L1 boundary, `ProbeAck` and `ProbeAckData` are definitional variants of `ProbeResponse`. If the projected clean and dirty cases have the same boundary ordering, complementary guards `Dirty` / `!Dirty` may be merged into an unconditional parent case.

A synthetic buggy dirty path is also included. Its boundary order differs, so the merge engine must keep it separate.

## Run

```bash
python -m unittest discover -s tests -v
```

## Current scope

Implemented:

- `Event`, `Before`, boolean `Guard`, and guarded `Case` IR
- transitive boundary projection that removes internal events
- definitional boundary aliases
- conservative merge of complementary cases with identical consequences
- BOOM Probe clean/dirty example
- negative test: exceptional boundary behavior is not merged

Not implemented yet:

- RTL extraction
- LLM generation
- SMT/formal proof
- exact cycle relations (`Next`, `SameCycle`)
- symbolic addresses / transactions
- queue conservation rules
- general guard minimization

The next intended stress tests are MSHR/RPQ, BOOM B1 load-load ordering, and XiangShan timing-sensitive cases.
