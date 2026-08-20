# Current Method

## Static hierarchy

1. Prefer physical module/instance hierarchy.
2. If a physical module is too large, recursively create module-internal WorkUnits from immediate event-state structure and state/dependency structure.
3. Event slices are analysis primitives, not final abstraction units.
4. Shared logic/state is promoted to the parent and never copied between children.
5. Coverage is fail-closed: no statement/state/event may silently disappear or be multiply owned.
6. A parent replaces a completed child with a child µMCM summary rather than rereading child RTL during semantic synthesis.

## µMCM generation

Current experimental language uses:

- occurrences: boundary or RTL-grounded derived occurrences;
- persistent predicates;
- transaction/object identity;
- semantic cases;
- candidate axioms;
- environment assumptions and unresolved obligations.

Same-cycle combinational routing/merging is expressed by a generic
`occurrence_partition`: `whole <=> OR(parts)` plus pairwise exclusion of all
parts. Ordering remains a separate historical relation, and payload/identity
forwarding remains a separate equality/flow claim.

The partition is defined for every non-empty `parts` set. A singleton is the
degenerate but useful 1→1 routing case: pairwise exclusion is vacuous and the
conservation relation becomes exact same-cycle occurrence equivalence.

An occurrence-conditioned `signal_equality` retains its `on` guard through
compilation. Exact proof reconstructs FIRRTL last-connect priority and checks
all selected payload drivers reachable under that occurrence; aggregate event
payload leaves remain valid grounding even when the logical ledger compacts the
corresponding statement read to the aggregate bundle.

The LLM may propose candidates, but candidate axioms are not trusted by default.

## Validation and trust

Validation levels are intentionally separated:

```text
GROUNDED
  -> PARTIALLY_SUPPORTED / STRUCTURALLY_SUPPORTED
  -> FORMALLY_PROVED
  -> SPEC_PROVED
```

Only `FORMALLY_PROVED` or `SPEC_PROVED` axioms may enter `trusted_umcm.json`.

Structural control/dataflow counterexamples are conservative diagnostic evidence, not automatically concrete RTL counterexamples. When an exact certified backend proves the concrete Boolean/control obligation, that proof takes precedence; otherwise the workflow remains fail-closed.

Completeness is not assumed. Missing axioms are expected to make the µMCM an over-approximation. Later system-level counterexamples are checked against concrete RTL; spurious traces drive counterexample-guided µMCM refinement.

## Bottom-up synthesis

Parent synthesis must preserve provenance. A parent axiom can be:

- inherited from a child;
- lifted/generalized from one or more case-specific child axioms;
- emergent from multiple child contracts plus parent-local RTL/glue.

Any generalization must preserve direct theorem provenance so the user can observe how lower-level axioms became a higher-level axiom. For a trusted parent axiom, `source_axioms` is derived from the composition prover certificate and checked against the LLM declaration before entering `trusted_umcm.json` or `frozen_umcm.json`; recursive descent through each frozen parent's direct provenance recovers the complete bottom-up chain.
