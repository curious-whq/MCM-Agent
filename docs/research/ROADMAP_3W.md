# Three-Week Manual Bootstrap Roadmap

## Days 1–7 — L1 representative end-to-end chain

Goal: prove the full workflow, especially parent synthesis, not manually finish every L1 WorkUnit.

Representative targets include ProbeUnit, WritebackUnit, MSHR/MSHRFile, one RPQ/Queue path, and parent-local glue. Required milestone: observe at least one real lower-level-to-parent axiom generalization with provenance.

## Days 8–14 — Broaden representative coverage

Use a small but diverse set rather than exhaustively processing every module:

- continue key L1 modules;
- sample L2 Directory/MSHR/Source-Sink behavior;
- sample one or two automatically partitioned LSQ/LSU regions.

By the end of this period, stabilize the µMCM schema, property obligation types, refinement protocol and parent synthesis result format.

## Days 15–21 — Automation cutover

Implement a real LLM provider, replay known manual cases, then evaluate held-out WorkUnits. By Day 21, start a whole-BOOM automatic run. After the cutover, humans should mainly analyze failures/counterexamples rather than manually generate every WorkUnit µMCM.
