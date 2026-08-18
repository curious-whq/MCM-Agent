# MCM-Agent — Prototype v5

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

v0-v3 validated the abstraction language with hand-written real-world cases. v4 started structural FIRRTL discovery. **v5 completes the first deterministic frontend boundary before any LLM is introduced.**

## Manual abstraction prototypes

- v0: ordering/FSM projection
- v1/v1.1: resource/token conservation and occurrence identity
- v2/v2.1: exceptional state-case preservation
- v3: exact timing-case preservation

## v4-v5: deterministic frontend

```text
Chisel
  ↓ emit CHIRRTL with source locators
Textual CHIRRTL
  ↓
Input Contract
  ↓
Module / Instance Hierarchy
  ↓
Physical Boundary Leaves
  ↓
Physical Decoupled / Valid Event Registry
  ↓
Signal Dependency Graph
  ├─ data
  ├─ control
  ├─ state
  ├─ address
  └─ memory
  ↓
Event-Centered Backward Slice
  ↓
Register SCC + Event-Cone Partition
  ↓
Cross-Module Flattened Slice
  ↓
Coverage Ledger (fail closed)
  ↓
Source Locator → Scala Snippet
  ↓
Deterministic Static Handoff Manifest
  ↓
[future LLM starts here]
```

The frontend never invents semantic event names. A physical event remains grounded as, for example:

```text
BoomProbeUnit.io.rep.fire
predicate = io.rep.valid && io.rep.ready
```

and manifests deliberately contain:

```json
"semantic_labels": []
```

## Why fail closed

If the parser sees an unknown statement that may affect functional behavior, it records it as `UNSUPPORTED`. The module and any hierarchical slice touching it are marked incomplete. `frontend.handoff` refuses to create a ready pre-LLM package from incomplete or truncated analysis.

This prevents a small slice from looking trustworthy merely because an unsupported RTL construct was silently ignored.

## BOOM-shaped validation

The fixtures cover the structures seen in BOOM v4:

- ProbeUnit: Decoupled `req/rep/meta_read/meta_write/wb_req/lsu_release` plus FSM state;
- DCache hierarchy: top-level coherence channels connected through ProbeUnit;
- MSHR: RPQ-like queue state, Grant/GrantAck-facing events, state/barrier dependencies.

These are still unit-test fixtures, not a checked-in official BOOM elaboration. The next integration task is to run the frontend on CHIRRTL emitted from a real BOOM/Chipyard build and harden unsupported syntax from coverage reports.

## CLI

Static coverage:

```bash
python -m frontend.cli report design.fir
```

Physical events:

```bash
python -m frontend.cli events design.fir --module BoomProbeUnit
python -m frontend.cli design-events design.fir
```

Local event slice:

```bash
python -m frontend.cli slice design.fir \
  --module BoomProbeUnit \
  --event BoomProbeUnit.io.rep.fire \
  --mode full
```

Direct physical endpoint connectors:

```bash
python -m frontend.cli connectors design.fir
```

Cross-module slice:

```bash
python -m frontend.cli design-slice design.fir \
  --event DCacheTop::io.tl_c.fire \
  --payload
```

Resolve FIRRTL source locators to Scala text:

```bash
python -m frontend.cli slice design.fir \
  --module BoomProbeUnit \
  --event BoomProbeUnit.io.rep.fire \
  --source-root /path/to/riscv-boom
```

Static abstraction tree:

```bash
python -m frontend.cli tree design.fir
```

Candidate static partition:

```bash
python -m frontend.cli partition design.fir --module BoomMSHR
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Static/LLM/formal responsibility split

```text
Static = completeness and grounding
LLM    = semantic interpretation and candidate cases
Formal = correctness of summaries/proofs
```

The next phase should **not** immediately implement an LLM Agent. First run v5 on real BOOM emitted CHIRRTL, use `UNSUPPORTED` coverage to harden the frontend, and verify that Probe/MSHR/TL slices remain small and source-grounded. See `docs/frontend/static_pipeline.md`.
