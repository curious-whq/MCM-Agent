# MCM-Agent Research Goal

MCM-Agent aims to turn a real elaborated microarchitecture into a recursively composable microarchitectural memory model (µMCM):

```text
whole RTL
  -> static hierarchical WorkUnits
  -> leaf candidate µMCM
  -> proof / trusted µMCM
  -> child replacement
  -> parent axiom synthesis
  -> subsystem µMCM (L1, L2, LSQ/LSU)
  -> memory-system µMCM
  -> architectural MCM checking (e.g. RVWMO)
  -> concrete RTL feasibility / real bug
```

The static planner, not the LLM, decides the WorkUnit hierarchy. The LLM proposes semantic abstractions and synthesis steps; deterministic/formal validation decides what may enter the trusted µMCM.

## Manual bootstrap constraint

For the first three weeks, human ChatGPT conversations temporarily play the role of the LLM provider. The workflow itself should already be the future automated workflow. After the bootstrap period, the manual provider should be replaceable by a real LLM provider without redesigning downstream validation or synthesis.
