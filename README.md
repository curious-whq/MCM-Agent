# MCM-Agent — Prototype v3

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

The implementation is still deliberately manual: no RTL parser and no LLM Agent yet. The current goal is to validate the abstraction language and algorithms before automating the frontend.

## Implemented abstraction primitives

### v0: ordering/FSM projection

Internal event paths are closed transitively, internal events are hidden, and only boundary-equivalent cases may be merged.

### v1/v1.1: resource/token conservation and identity

Queue/token summaries preserve symbolic request and scope identity.

### v2/v2.1: exceptional state-case preservation

BOOM B1 is modeled with occurrence-bound state predicates and RTL-grounded blocking effects. The state-case minimizer is checked exhaustively over all 256 Boolean functions of three variables.

### v3: exact timing-case preservation

XiangShan MetaArray commits `479d62a...` and `6318236...` are used as the first timing-sensitive case.

The timing IR supports:

```text
SameCycle(A, B)
Next(A, B)
CycleDelta(A, B, k)
```

Internally these become finite `DeltaDomain`s whose semantics are:

```text
cycle(B) - cycle(A) ∈ allowed_deltas
```

The pre-final-fix model keeps the simultaneous write/read case separate because it returns old metadata, while a previous-cycle write is handled by the existing s1 bypass.

After the final s0-bypass fix both timing cases produce the same `io.resp` value, so they may be merged exactly into the finite timing domain `{0, 1}`.

The merge never fills timing gaps: `{0}` and `{2}` becomes `{0, 2}`, not an interval containing cycle 1.

## Run

```bash
python -m unittest discover -s tests -v
```

## Next

After v3, the prototype has exercised FSM paths, queue/token lifetime, exceptional state cases, and exact timing cases. The next phase should begin building the automated frontend: structural hierarchy discovery, boundary/event registry, and event-centered static slicing.
