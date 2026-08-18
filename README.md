# MCM-Agent — Prototype v4

MCM-Agent studies bottom-up synthesis of hierarchical microarchitectural memory-model summaries.

v0-v3 validated the abstraction language manually. v4 starts the automated frontend.

## Manual abstraction prototypes

- v0: ordering/FSM projection
- v1/v1.1: resource/token conservation and occurrence identity
- v2/v2.1: exceptional state-case preservation
- v3: exact timing-case preservation

## v4: FIRRTL structural frontend

v4 does **not** generate µMCM axioms yet and does **not** use an LLM.

It statically extracts:

```text
FIRRTL / CHIRRTL
      ↓
module / instance hierarchy
      ↓
physical boundary leaf ports
      ↓
Decoupled-style valid/ready handshake events
      ↓
source locator provenance
```

A physical event uses a structural name such as:

```text
BoomProbeUnit.io.req.fire
```

with a grounded predicate:

```text
io.req.valid && io.req.ready
```

The frontend deliberately does not rename this to a semantic event such as
`ProbeRecv`. Semantic interpretation will be a later, provenance-constrained
layer.

### First BOOM target

The v4 fixture mirrors the real BOOM v4 `BoomProbeUnit` interface and checks
that the frontend recovers its `req`, `rep`, `meta_read`, `meta_write`,
`wb_req`, and `lsu_release` Decoupled channels.

## Run

```bash
python -m unittest discover -s tests -v
```

## Next

The next frontend milestone is event-centered dependency slicing. That phase
will extend the FIRRTL parser from structural declarations to connects,
register next-state dependencies, mux/control dependencies, and source-covered
slice output.
