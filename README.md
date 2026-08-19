# MCM-Agent — Prototype v10

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

v0-v3 validated the abstraction language with hand-written real-world cases. v4-v6 built and hardened the deterministic pre-LLM frontend on a complete Chipyard design. **v7-v10 add the recursive hierarchical verification planner: immediate Event-State partitioning, state/dependency fallback, shared-parent ownership, true child replacement, and logical/effective complexity validated directly on real BOOM LSU/L1/L2 FIRRTL.**

## Manual abstraction prototypes

- v0: ordering/FSM projection
- v1/v1.1: resource/token conservation and occurrence identity
- v2/v2.1: exceptional state-case preservation
- v3: exact timing-case preservation

## Deterministic frontend

```text
Chisel / Chipyard
  ↓ emit textual FIRRTL with source locators
Whole-system FIRRTL
  ↓
Input Contract
  ↓
Module / Instance Hierarchy
  ↓
Physical Boundary Leaves
  ↓
Physical Decoupled / Valid Event Registry
  ↓
Lazy Module Dependency Graphs
  ├─ data
  ├─ control
  ├─ state
  ├─ address
  ├─ memory
  └─ aggregate-flow aliases
  ↓
Local Event-Centered Backward Slice
  +
Ownership-Scoped Instance-Subtree Slice
  +
Lazy Handshake Transport Route
  ↓
Immediate Event-State Interaction Graph
  ↓
Recursive Hierarchical WorkUnit Planner
  ├─ physical child hierarchy first
  ├─ event-coupled regions
  ├─ register-SCC/state fallback
  └─ shared parent glue promotion
  ↓
Child RTL → umcm://child summary replacement
  ↓
Logical + replacement complexity
  ↓
Coverage Ledger (fail closed)
  ↓
Source Locator → Scala Snippet
  ↓
Deterministic Static Handoff
  ↓
[future LLM starts here]
```

The frontend never invents semantic event names. A physical event remains grounded, for example:

```text
BoomProbeUnit.io.rep.fire
predicate = io.rep.valid && io.rep.ready
```

and static outputs deliberately keep:

```json
"semantic_labels": []
```

## v10: recursive hierarchical verification plan

The static frontend no longer treats an event slice as the final abstraction unit. A large module is recursively decomposed until the RTL that remains after child-summary replacement is manageable. Event slices are internal partition evidence; state/dependency regions are used when event grouping cannot expose the remaining structure.

Complexity reports keep both raw FIRRTL counts and a source-grounded logical quotient, so aggregate/lowering expansion cannot force artificial partitions. The complete uploaded SmallBoomV4Config validates the intended behavior: ProbeUnit and BoomMSHR remain manageable leaves at their own level, LSU and DCache partition recursively, and InclusiveCache primarily follows the real Source/Sink/Directory/MSHR physical hierarchy.

The decisive LSU result is `1499` logical statements / `959` mapped source lines before partitioning and `890` logical statements / `579` mapped source lines after 21 child summaries are substituted, with `replacement_exceeded_limits=[]` and complete ownership conservation. See `docs/frontend/hierarchical_work_units.md` and `docs/integration/hierarchical_work_units_v10_real_boom.md`.

Useful commands:

```bash
python3 -m frontend.module_cli module-stats design.fir --root-module LSU
python3 -m frontend.module_cli module-tree  design.fir --root-module BoomNonBlockingDCache
python3 -m frontend.module_cli module-plan  design.fir --root-module InclusiveCache
```

## v6: real whole-Chipyard hardening

The real uploaded `SmallBoomV4Config.fir` used for v6 contains:

```text
523,408 FIRRTL lines
1,858 module definitions
2,170 concrete physical events
502,974 source locators
```

Selected memory-system modules now parse with fail-closed coverage complete and zero unsupported statements:

```text
LSU                           8,169 statements
BoomCore                     10,539 statements
BoomNonBlockingDCache         2,924 statements
BoomProbeUnit                   209 statements
BoomMSHR                       2,216 statements
BoomMSHRFile                   1,507 statements
InclusiveCache                   220 statements
InclusiveCacheBankScheduler    2,499 statements
InclusiveCacheControl            798 statements
```

v6 also mechanically recovers two real coherence transport routes without semantic aliases:

```text
L2 InclusiveCache TL-B
→ system interconnect / buffers / xbars
→ BOOM DCache
→ BoomProbeUnit.req
```

and:

```text
BoomProbeUnit.rep
→ DCache TL-C / arbiters
→ system interconnect / buffers / xbars
→ L2 InclusiveCache TL-C
```

Both valid and ready/backpressure paths are required. The recovered paths cross real queue state, so this is stronger than just finding a combinational `valid` wire.

v6 also runs complete ownership-scoped semantic cones on the same whole-system file:

```text
L2 B event, rooted at the real InclusiveCache instance
  5,252 signals
  11,852 dependency edges
  36 concrete instances
  complete = true
  reaches SourceB + Directory + MSHR* + Sink/Source channel engines

Probe request, rooted at the enclosing BOOM DCache
  4,716 signals
  25,529 dependency edges
  29 concrete instances
  complete = true
  reaches ProbeUnit + MSHRFile/MSHR + Writeback
  does not enter the whole BoomCore
```

This is the intended hierarchical work unit: analyze the complete design as input, but constrain semantic cones by statically recovered physical ownership rather than manually cutting RTL files.

## Why route and slice are separate

A whole-event backward cone can legitimately become very large because `ready`, arbiters and core state have high fan-in. That does not mean the design cannot be analyzed.

v6 therefore distinguishes:

```text
transport route
    = prove how one physical channel travels between two endpoints

semantic event cone
    = recover every state/control/data dependency that may influence one event
```

The first is used to ground hierarchy composition; the second is used later for case extraction. Neither is replaced by LLM inference.

## CLI

Install the local command once:

```bash
pip install -e .
```

Coverage on selected modules in a very large design:

```bash
mcm-static report design.fir \
  --module BoomProbeUnit \
  --module BoomMSHR \
  --module InclusiveCache
```

List concrete events:

```bash
mcm-static design-events design.fir
```

Recover an end-to-end physical Decoupled route:

```bash
mcm-static route design.fir \
  --from-event 'TestHarness....l2::auto.in.b.fire' \
  --to-event 'TestHarness....dcache.prober::io.req.fire'
```

Ownership-scoped semantic cone, recommended for a full SoC:

```bash
mcm-static instance-slice design.fir \
  --event 'FULL_CONCRETE_EVENT_ID' \
  --root 'OWNING_INSTANCE_PATH' \
  --payload
```

Whole-design semantic cone, only when the question truly crosses the ownership boundary:

```bash
mcm-static design-slice design.fir \
  --event 'FULL_CONCRETE_EVENT_ID' \
  --payload
```

Local event slice:

```bash
mcm-static slice design.fir \
  --module BoomProbeUnit \
  --event BoomProbeUnit.io.rep.fire \
  --mode full
```

## Tests

Fast unit tests:

```bash
python -m unittest discover -s tests -p 'test_frontend*.py' -v
```

Real Chipyard integration regression, when a local `.fir` is available:

```bash
MCM_REAL_FIRRTL=/path/to/SmallBoomV4Config.fir \
python -m unittest tests.test_real_chipyard_firrtl -v
```

## Static / LLM / formal split

```text
Static = completeness, physical grounding and slicing
LLM    = semantic interpretation and candidate guarded cases
Formal = correctness of summaries and composition
```

v6 still contains no LLM Agent. The next stage can now consume source-grounded static work units rather than raw whole-system RTL.
