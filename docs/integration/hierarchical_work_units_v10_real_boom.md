# v10 hierarchical WorkUnit validation on real SmallBoomV4Config

This note records the deterministic static validation used for the v10 planner.
The input is the complete elaborated `chipyard.harness.TestHarness.SmallBoomV4Config.fir` supplied by the project owner; no hand-cut BOOM fixture is used for these measurements.

## What v10 validates

v10 separates four concerns that were conflated in earlier prototypes:

1. **Partition discovery** uses immediate event-to-register frontiers, not full historical event cones.
2. **Ownership expansion** grows a discovered child through its own state while treating parent/hub/peer state as explicit frontiers.
3. **Complexity** uses a logical quotient of source-grounded FIRRTL lowering while retaining all raw graph counts.
4. **Bottom-up manageability** is checked on the parent input after children are replaced by `umcm://...` summary slots.

If event grouping cannot expose useful children, the planner falls back to register-SCC/state groups and may repeat that fallback on the still-oversized parent residual.

## Root results

| Root | Decision | Logical source | Logical statements | Logical edges | Replacement source | Replacement statements | Replacement exceeds | Coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| BoomProbeUnit | manageable | 97 | 132 | 364 | 97 | 132 | none | complete |
| BoomMSHR | manageable | 304 | 392 | 3512 | 304 | 392 | none | complete |
| LSU | partitioned | 959 | 1499 | 5325 | 579 | 890 | none | complete |
| BoomNonBlockingDCache | partitioned | 398 | 559 | 1396 | 318 | 441 | none | complete |
| InclusiveCache | manageable | 36 | 47 | 124 | 36 | 47 | none | complete |

Raw FIRRTL counts remain much larger (for example, LSU has 8169 raw statements,
23005 raw signals and 34874 raw dependency edges). They remain present in every
manifest, but no longer force a split solely because aggregate/lowering expansion
multiplies one source-level operation.

## LSU

The LSU is the decisive recursive-partition case. The complete local module has:

```text
8169 raw statements / 1499 logical statements
23005 raw signals    / 2093 logical signals
34874 raw edges      / 5325 logical edges
959 mapped source lines
115 registers
24 boundary events
57 register state groups
```

The planner first extracts useful event-owned regions, then falls back to
state/dependency regions for the still-large residual. After 21 child summaries
are substituted, the parent-visible input becomes:

```text
5524 raw statements / 890 logical statements
13005 raw signals    / 1413 logical signals
20211 raw edges      / 3194 logical edges
579 mapped source lines
40 registers
14 local events
40 state groups
replacement_exceeded_limits = []
coverage_complete = true
```

The remaining mapped source is overwhelmingly BOOM `lsu.scala`, rather than an
artifact of utility-library source locators. The planner therefore stops instead
of forcing another unsafe cut.

## L1 DCache

`BoomNonBlockingDCache` keeps real instance hierarchy primary (MSHR file/MSHRs,
ProbeUnit, Writeback, metadata/data arrays, arbiters) and adds static local
regions only for parent-owned RTL. Its original 559 logical statements become a
441-logical-statement parent replacement input, with complete conservation.

## L2 InclusiveCache

`InclusiveCache` itself is already small. The useful hierarchy appears physically
inside the bank scheduler: Source/Sink channel engines, Directory, BankedStore,
request queues and MSHRs remain concrete child modules. v10 therefore does not
invent static partitions just to make the tree deeper.

## Regression expectations

The v10 planner should maintain all of the following simultaneously:

```text
ProbeUnit remains a leaf
BoomMSHR remains manageable once FIRRTL lowering is quotiented
BranchKillableQueue remains a strongly coupled leaf
LSU is recursively partitioned until its replacement input is manageable
DCache prefers physical hierarchy plus local static regions
L2 prefers physical Source/Sink/Directory/MSHR hierarchy
coverage.complete = true at every WorkUnit
no missing or duplicate statement/state/event ownership
```
