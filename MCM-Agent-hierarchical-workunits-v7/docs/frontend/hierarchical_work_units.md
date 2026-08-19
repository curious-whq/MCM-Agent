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

For every physical boundary event, the frontend computes the register SCCs and
static statements touched by its full local cone. The resulting bipartite graph
contains:

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
state SCCs
events
```

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
