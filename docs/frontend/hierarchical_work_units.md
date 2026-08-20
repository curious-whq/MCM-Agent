# Recursive Hierarchical Work Units

This stage changes the static frontend's primary abstraction unit from an
event-centered slice to a recursively composable **Hierarchical Work Unit**.

The low-level event slice remains available, but it is now only an internal
analysis primitive used to recover event/state interaction and statement
ownership.

## Pipeline

```text
Whole FIRRTL
  ↓
physical module/instance hierarchy
  ↓
per-module boundary events
  ↓
register dependency SCCs
  ↓
event-centered cones
  ↓
Event-State Interaction Graph
  ↓
complexity + coupling driven partition
  ↓
Hierarchical Work Units
  ↓
coverage/ownership conservation
  ↓
child summary replacement plan
```

A physical module instance is always the preferred work-unit boundary. If the
module-local RTL remains too large, the same module can be recursively
partitioned into static regions.

## Event-State Interaction Graph

For every physical boundary event, the frontend computes both a full historical
cone and an immediate current-cycle frontier. The Event-State Interaction Graph
is built from the immediate frontier only; traversal stops at the first register
boundary. The resulting bipartite graph contains:

```text
Event → State SCC
State SCC → Event
```

An event-pair projection records:

- shared state SCCs;
- shared registers;
- shared static-cone statements;
- state Jaccard overlap;
- statement Jaccard overlap;
- a deterministic structural coupling score.

The score is a partition heuristic only. It does not assign semantic names or
claim a microarchitectural protocol relation.

## Partition rule

Crossing a LOC/signal/register/event/edge/statement limit only means:

```text
attempt_partition = true
```

It does **not** mean that a cut is automatically accepted.

The frontend accepts a cut only when the interaction graph exposes at least two
useful event groups with exclusive state/logic ownership. State or statements
touched by multiple children are promoted to the parent as shared glue.

Therefore:

```text
parent RTL
=
parent-local/shared RTL
+
disjoint child RTL
```

The same rule is applied recursively.

## Coverage ledger

Each same-module partition boundary conserves three categories:

```text
statements
concrete register state
events
```

Register SCCs are retained as coupling evidence and statistics, but recursive
ownership is tracked at concrete register-root granularity so a large feedback
SCC is not an artificial atomic boundary.

The ledger checks for:

```text
missing
duplicate
unsupported
```

A work unit is coverage-complete only when no item is silently lost or assigned
to multiple children.

## Child replacement

After a child is abstracted, its internal statement IDs are intentionally absent
from the parent analysis package. The parent receives only:

```text
summary_ref = umcm://<child-id>
boundary events
frontier/connection signals
```

plus the parent's own local RTL/state/events.

This is the static representation required for the later bottom-up flow:

```text
leaf RTL
  ↓
leaf µMCM
  ↓
parent-local RTL + child µMCM slots
  ↓
parent µMCM
```

No LLM is used in this stage.

## CLI

Install editable mode:

```bash
pip install -e .
```

Show the recursive hierarchy:

```bash
mcm-plan module-tree design.fir --root-module BoomMSHR
```

Show flat per-unit complexity:

```bash
mcm-plan module-stats design.fir --root-module LSU
```

Show coverage, interaction graph, parent-local ownership, and child-summary
replacement inputs:

```bash
mcm-plan module-plan design.fir \
  --root-instance 'TestHarness....dcache'
```

For experiments, structural limits can be overridden, for example:

```bash
mcm-plan module-plan design.fir \
  --root-module LSU \
  --max-statements 500 \
  --max-signals 2500 \
  --coupling-threshold 0.45
```

A concrete `--root-instance` is preferred for a whole-SoC FIRRTL. A
`--root-module` is useful while developing one LSQ/L1/L2 module type in
isolation.

## v8: immediate ownership instead of historical closure

Real BOOM `BoomMSHR` exposed an important failure mode in the first recursive
partitioner. A full backward event cone can cross register boundaries and then
follow the next-state history of a central FSM. Different boundary events may
therefore appear to share almost the entire module even when their *current-cycle*
state dependence is different.

v8 separates the two questions:

```text
full historical event cone
  -> retained for semantic extraction / future µMCM synthesis

immediate event-state frontier
  -> used only for ownership and WorkUnit partitioning
  -> backward traversal stops at the first register boundary
```

The interaction graph is now built from immediate registers and immediate
statements. Register SCCs remain reported as structural coupling evidence, but
are no longer atomic ownership units: a recursive WorkUnit may own only part of
one large SCC.

### Parent hub-state promotion

For event-rich modules, a register directly touched by a high fraction of
boundary events is marked as coordinator/hub state. Hub state is retained at the
parent and is not allowed to glue otherwise distinct event groups together.
The default structural rule is:

```text
module events >= 4
and register touches >= 3 events
and event fraction >= 0.60
    => parent hub state
```

This rule is intentionally disabled for two-event queue-like structures, where
shared enqueue/dequeue state is often the actual component identity.

### Pure combinational events

Events with no immediate register dependence are not discarded. Their immediate
statement cone participates in coupling/ownership, and sufficiently large
exclusive combinational cones may form children. Small or ambiguous cones remain
parent-local rather than being duplicated.

### Expected real-BOOM regression

The intended regression is:

```text
BoomProbeUnit
  -> remains manageable leaf

BranchKillableQueue
  -> remains strongly coupled leaf

BoomMSHR
  -> no longer becomes unsplittable merely because the historical cone reaches
     one central FSM SCC; hub/shared state stays at parent while local immediate
     state can seed multiple internal regions
```


## v9: scoped complexity + bounded ownership expansion

v8 fixed *partition discovery*: immediate state dependence can now separate
event groups below shared/hub coordinator state. Real `BoomMSHR` then exposed a
second failure mode: the tree could be structurally partitioned while most RTL
statements still remained at the parent, and tiny regions inherited inflated
whole-module dependency-edge counts.

v9 separates discovery from ownership explicitly:

```text
Stage A: discover child identity
  immediate Event-State frontier
  + hub promotion
  + coupling groups

Stage B: expand child ownership
  child events + child-owned state
  ↓
  bounded historical backward cone
  ↓
  may cross child-owned registers
  ↓
  STOP at every non-child register
```

This makes a parent/hub register an explicit **frontier value**, not an ownership
barrier for all logic that reads it. In particular:

```text
read parent/hub state
  -> allowed inside child as a frontier input

write parent/hub state
  -> parent-local

read peer-child state directly
  -> cross-child parent glue

write peer-child state
  -> parent-local
```

Statements selected by more than one child are also retained at the parent.
Coverage conservation remains exact after this expansion.

### Scope-aware complexity

Region edge complexity is no longer computed by counting every whole-module
edge that merely touches one region signal. For a non-module WorkUnit:

```text
statement-backed edge
  -> counted only if its statement belongs to the region

provenance-free alias/synthetic edge
  -> counted only if both endpoints are in the region signal scope
```

This prevents a five-statement region from being classified as oversized merely
because one signal has thousands of aliases/fanout edges elsewhere in the
module.

### Primary v9 regression metric

For a successfully partitioned module, the important metric is no longer just:

```text
decision = partitioned
```

but also:

```text
parent_local_statements / total_statements
```

The ratio should fall materially while all conservation checks remain true:

```text
coverage.complete = true
missing_statement_ids = []
duplicate_statement_ids = []
missing_event_ids = []
duplicate_event_ids = []
```

This is the condition required before child µMCM summaries can actually reduce
the parent analysis input.

## v10: logical/effective complexity and recursive state fallback

Real whole-Chipyard FIRRTL exposed two remaining problems after v9: FIRRTL
lowering can multiply one source-level object into thousands of leaf signals and
dependency edges, and an event-based cut can leave a still-large parent whose
remaining structure is primarily state/dependency based. v10 addresses both
without changing the fail-closed dependency graph used for slicing or coverage.

### Raw graph versus logical complexity

The dependency graph remains exact and leaf-level. Complexity decisions use a
separate quotient view:

```text
raw FIRRTL graph                         logical complexity quotient
----------------                         ---------------------------
req.uop.rob_idx      ┐
req.uop.ldq_idx      ├─> many leaves  -> req.uop
req.uop.mem_cmd      ┘

many lowered edges from one source op -> one (source, kind, logical-src,
                                            logical-dst) dependency
```

Register and memory descendants collapse to their state root. Aggregate leaves
collapse to the nearest proper aggregate parent already recovered by the FIRRTL
parser. Lowered temporary nodes with source provenance are grouped by source
location and kind. No semantic names are invented.

Every report keeps both values:

```text
signals / logical_signals
dependency_edges / logical_dependency_edges
statements / logical_statements
source_loc / logical_source_loc / unmapped_firrtl_loc
```

`WorkUnitComplexity.exceeded()` uses the logical values. Raw values remain
available for debugging, grounding and fail-closed coverage.

For source complexity, `source_loc` remains conservative and includes unmapped
FIRRTL lines. `logical_source_loc` uses real mapped source lines whenever the
scope has provenance, and falls back to FIRRTL lines only for a completely
unmapped scope.

### Replacement complexity

Every WorkUnit now reports a second complexity record:

```text
complexity
    = complete RTL scope owned by this WorkUnit

replacement_complexity
    = parent-local RTL remaining after all current children are replaced
      by umcm://<child-id> summary slots
```

The second quantity is what a parent semantic-synthesis stage will actually
consume. `replacement_exceeded_limits` therefore answers whether bottom-up
replacement has made the parent manageable, even if the original scope was
large.

### State/dependency fallback

Event grouping remains the preferred first cut, but is no longer the only cut.
If an oversized unit has multiple boundary events whose immediate cones cannot
produce at least two useful children, v10 falls back automatically to the
register-SCC/state-dependency hierarchy:

```text
boundary events
      ↓
immediate Event-State partition
      ↓ cannot expose useful children
register SCC / state groups
      ↓
bounded ownership expansion
      ↓
state/dependency children + parent glue
```

An SCC is still only a strong-coupling hint. When necessary it can be refined to
individual register roots. Event-rich modules are therefore not forced to use
an event partition merely because events exist.

After an initial cut, v10 repeats this state fallback on the still-visible
parent residual while `replacement_complexity` exceeds its limits. State already
owned by existing children is protected as peer-summary state. A statement
previously classified as shared glue is not frozen forever: a deeper partition
may re-prove exclusive ownership, after which it is delegated and removed from
the current parent shared ledger. True multi-child state glue is reclassified as
shared at the final boundary.

### Scalability

The state-root lookup and register dependency construction now use prefix
ownership indices instead of repeatedly scanning every register against every
signal. On the uploaded real BOOM LSU, `register_dependency_edges()` dropped
from roughly 26.7 seconds to about 0.075 seconds and local partition discovery
to roughly 1.35 seconds on the same environment.

### Real SmallBoomV4Config validation

The uploaded complete `SmallBoomV4Config.fir` was used directly as the v10
regression input. Representative root results are:

| WorkUnit | Decision | Raw / logical source | Raw / logical statements | Raw / logical edges | Replacement logical source | Replacement logical statements | Children | Coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| BoomProbeUnit | manageable | 107 / 97 | 209 / 132 | 533 / 364 | 97 | 132 | 0 | complete |
| BoomMSHR | manageable | 331 / 304 | 2216 / 392 | 19374 / 3512 | 304 | 392 | 1 physical | complete |
| LSU | partitioned | 1231 / 959 | 8169 / 1499 | 34874 / 5325 | 579 | 890 | 21 | complete |
| BoomNonBlockingDCache | partitioned | 427 raw / 398 logical | 2924 / 559 | 4945 / 1396 | 318 | 441 | 18 | complete |
| InclusiveCache | manageable | 42 / 36 | 220 / 47 | 308 / 124 | 36 | 47 | 3 physical | complete |

The key LSU condition is:

```text
original logical complexity:
  959 mapped source lines
  1499 logical statements
  115 registers
  24 events

bottom-up replacement input:
  579 mapped source lines
  890 logical statements
  40 registers
  14 local events
  replacement_exceeded_limits = []
  coverage.complete = true
```

Thus v10 reaches the intended structural fixed point: a genuinely large LSU is
recursively decomposed, child internals are replaced by summary slots, and the
remaining parent input becomes manageable without dropping or duplicating RTL.

## v11: structural implementation identity for theorem reuse

The planner now exports a transitive structural implementation fingerprint via
`module_structural_sha256()`. The hash deliberately replaces generated child
module names with the recursively computed child structural hash, so the
identity is stable across elaborations that rename generated modules while
preserving the actual implementation structure.

The structural fingerprint is **not** a proof by itself. Parent composition
uses two independent identities:

```text
proof-scope implementation SHA-256
    = instance-path-independent hash of the exact WorkUnit proof surface

transitive structural implementation SHA-256
    = generated-module-name-independent recursive RTL structure hash
```

A frozen generic module theorem may be instantiated for a concrete child slot
only when `workflow.composition` verifies both the source proof scope and the
target transitive structural fingerprint. Exact child-id matches remain the
simplest reuse path. Ambiguous or mismatched templates fail closed.

This v11 addition connects the static planner to reusable bottom-up proofs: a
parent can consume a theorem proved once for a generic module WorkUnit without
reopening the equivalent child RTL, while still rejecting reuse after a real
implementation change.
