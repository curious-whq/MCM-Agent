# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment, but "manual" only means that a human transports
the exported prompt and returned result between the workflow and the LLM. The
human is **not** expected to co-design each leaf abstraction. Analyze this WorkUnit
autonomously and derive the most conservative grounded candidate abstraction that
preserves information potentially relevant to microarchitectural memory ordering.
The µMCM language remains experimental and may be revised when new RTL/formal
evidence exposes a real reusable gap.

Task ID: `leaf_abstraction-BoomNonBlockingDCache.lfsr_prng-80cbcb83351fc3e0`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache.lfsr_prng`
- module: `MaxPeriodFibonacciLFSR_1`
- kind: `module`
- instance path: `BoomNonBlockingDCache.lfsr_prng`
- leaf: `True`
- coverage complete: `True`
- raw statements: 59
- logical statements: 11
- mapped/logical source lines: 10
- registers: 1
- physical boundary events: 1

## Non-negotiable grounding rules

1. Distinguish occurrences from persistent predicates. A boundary occurrence
   must reference one or more physical event IDs listed below. A derived
   occurrence may have no physical event ID only when it has an exact RTL
   definition, concrete grounding, and statement evidence. If one semantic
   occurrence depends on a multi-bit comparison, record it in grounding as
   `value_tests`, for example
   `{"expr":{"op":"signal","name":"io.source"},"relation":"eq","value":3}`;
   prose in `definition` is not formal grounding.
   occurrence repeats over a finite hardware index (beat/entry/bank/etc.), use
   the optional occurrence `index` metadata instead of inventing N separate IDs. Do not turn ordinary
   FSM staging states into milestones unless deleting the milestone would lose
   memory/coherence ordering, path, visibility, identity, or exclusion facts.
2. Persistent predicates describe facts that can remain true across cycles. They
   must have a grounded RTL definition/source signal or explicit state set.
3. Every candidate case/axiom/predicate/identity claim must cite supporting
   FIRRTL statement IDs from the ledger. If evidence is insufficient, put the
   issue in `unresolved` rather than guessing.
4. Distinguish an RTL guarantee from an environment assumption. In particular,
   do not claim eventual progress from a ready/valid interface without stating
   the fairness/readiness assumption required for it.
5. Preserve transaction/object identity when an ordering claim is only true for
   the same request/cache line/source/transaction.
6. Do not dump every FSM transition. Keep predicates/cases only when they affect which
   memory/coherence event can occur, object identity, exclusion/conservation, or
   ordering/visibility-relevant paths.
7. Every axiom must be expressed in the structured `formal` AST defined by
   `expected_output_schema.json`. The formal AST is the only semantic source of
   truth. Do **not** provide a separate natural-language `formula` or an LLM-authored
   `validation` program; both the human rendering and proof obligations are
   generated deterministically from the AST.
8. Use only formal axiom forms supported by the schema. The language includes
   generic `join` and `indexed_complete` forms for unordered prerequisites and
   finite indexed occurrence sets. For exact same-cycle event routing or merging,
   use `occurrence_partition`: `whole` is equivalent to the disjunction of `parts`,
   and the parts are pairwise mutually exclusive in that cycle. Its exact shape is:
   `{"type":"occurrence_partition","whole":"OutputFire","parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null}`.
   The `relation` field is required and must not be omitted. `parts` may contain
   one occurrence for an exact 1-to-1 passthrough; pairwise exclusion is then
   vacuous and the relation reduces to same-cycle equivalence. Existing relation axioms may additionally use
   `scope_index: {name: <index>, relation: same}` to state that the relation is
   pointwise over the same finite index (beat/entry/bank/etc.). Formal expressions
   may use `index_var` and `lookup` to refer to the bound index and an indexed
   storage element. These constructs are protocol-agnostic and must not be
   specialized to a particular module. For a synchronous mutable array whose
   read returns the latest prior same-key write, use `indexed_storage_flow`.
   It binds address/lane keys, masked writes, sampled reads, initialization, and
   the stored value layout, and exports the standard relations: `rf` selects the
   co-latest prior same-key write, `co` is a strict total order over writes to
   each key, and `fr` is derived as `rf^-1 ; co`. Relation names must be distinct;
   do not state `rf`, `co`, and `fr` as unrelated ordering approximations.
   Use `initialization.kind: explicit` only for a grounded initialization sweep,
   with `initial_value` on every value field. For RAM without a specified
   power-up/reset value, use `initialization: {"kind":"implicit_unconstrained"}`
   and omit every `initial_value`; this creates one fresh unconstrained initial
   write per key while preserving the same `rf/co/fr` definitions. The optional
   `read_write_collision` is `exclusive` by default; use
   `implicit_unconstrained` only when same-key synchronous read/write collision
   is possible and the RAM result is unspecified. This introduces a transient
   unconstrained abstract write as the collision read's `rf` source, immediately
   before the colliding real write in `co`. If a semantic property that you judge
   **necessary** for a sound/useful parent-facing abstraction cannot be faithfully
   represented by the current Formal AST, do not approximate it with a different
   or weaker axiom. Report a `MCM-AGENT LANGUAGE GAP` using the procedure below.
   A limitation of the current formal prover is **not** a language gap: if the AST
   can express the property, emit the candidate axiom and let `semantic-validate`
   determine whether the backend can certify it.
9. This stage proposes **candidate** axioms. Do not assert that formal validation
   has already proved them.
10. Do not treat every potentially useful strengthening as a blocker. If omitting
    a constraint merely makes the candidate µMCM a safer over-approximation, you
    may omit it and record the deliberate omission in `rationale` as a possible
    later CEGAR refinement. Reserve `unresolved` for genuine grounding/semantic
    uncertainty that prevents you from making a responsible candidate claim.

## Physical boundary events

- `BoomNonBlockingDCache.lfsr_prng::io.seed.valid`
  - predicate: `io.seed.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.seed.bits[0]', 'io.seed.bits[10]', 'io.seed.bits[11]', 'io.seed.bits[12]', 'io.seed.bits[13]', 'io.seed.bits[14]', 'io.seed.bits[15]', 'io.seed.bits[1]', 'io.seed.bits[2]', 'io.seed.bits[3]', 'io.seed.bits[4]', 'io.seed.bits[5]', 'io.seed.bits[6]', 'io.seed.bits[7]', 'io.seed.bits[8]', 'io.seed.bits[9]']
  - immediate registers: []
  - historical registers: []

## Concrete local state

['state']

## Environment/frontier signals

['clock', 'io.increment', 'io.out[0]', 'io.out[10]', 'io.out[11]', 'io.out[12]', 'io.out[13]', 'io.out[14]', 'io.out[15]', 'io.out[1]', 'io.out[2]', 'io.out[3]', 'io.out[4]', 'io.out[5]', 'io.out[6]', 'io.out[7]', 'io.out[8]', 'io.out[9]', 'io.seed.bits[0]', 'io.seed.bits[10]', 'io.seed.bits[11]', 'io.seed.bits[12]', 'io.seed.bits[13]', 'io.seed.bits[14]', 'io.seed.bits[15]', 'io.seed.bits[1]', 'io.seed.bits[2]', 'io.seed.bits[3]', 'io.seed.bits[4]', 'io.seed.bits[5]', 'io.seed.bits[6]', 'io.seed.bits[7]', 'io.seed.bits[8]', 'io.seed.bits[9]', 'io.seed.valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:197562 SRC:src/main/scala/chisel3/util/random/FibonacciLFSR.scala:65:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197563 SRC:src/main/scala/chisel3/util/random/FibonacciLFSR.scala:65:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197564 SRC:src/main/scala/chisel3/util/random/PRNG.scala:42:22 KIND:structural :: output io : { flip seed : { valid : UInt<1>, bits : UInt<1>[16]}, flip increment : UInt<1>, out : UInt<1>[16]}
[3] FIRRTL:197566 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:wire :: wire _state_WIRE : UInt<1>[16]
[4] FIRRTL:197567 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[0], UInt<1>(0h1)
[5] FIRRTL:197568 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[1], UInt<1>(0h0)
[6] FIRRTL:197569 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[2], UInt<1>(0h0)
[7] FIRRTL:197570 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[3], UInt<1>(0h0)
[8] FIRRTL:197571 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[4], UInt<1>(0h0)
[9] FIRRTL:197572 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[5], UInt<1>(0h0)
[10] FIRRTL:197573 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[6], UInt<1>(0h0)
[11] FIRRTL:197574 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[7], UInt<1>(0h0)
[12] FIRRTL:197575 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[8], UInt<1>(0h0)
[13] FIRRTL:197576 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[9], UInt<1>(0h0)
[14] FIRRTL:197577 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[10], UInt<1>(0h0)
[15] FIRRTL:197578 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[11], UInt<1>(0h0)
[16] FIRRTL:197579 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[12], UInt<1>(0h0)
[17] FIRRTL:197580 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[13], UInt<1>(0h0)
[18] FIRRTL:197581 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[14], UInt<1>(0h0)
[19] FIRRTL:197582 SRC:src/main/scala/chisel3/util/random/PRNG.scala:46:28 KIND:connect :: connect _state_WIRE[15], UInt<1>(0h0)
[20] FIRRTL:197583 SRC:src/main/scala/chisel3/util/random/PRNG.scala:55:49 KIND:regreset :: regreset state : UInt<1>[16], clock, reset, _state_WIRE
[21] FIRRTL:197584 SRC:src/main/scala/chisel3/util/random/PRNG.scala:69:22 KIND:when :: when io.increment :
[22] FIRRTL:197585 SRC:src/main/scala/chisel3/util/random/LFSR.scala:15:41 KIND:node :: node _T = xor(state[10], state[12])
[23] FIRRTL:197586 SRC:src/main/scala/chisel3/util/random/LFSR.scala:15:41 KIND:node :: node _T_1 = xor(_T, state[13])
[24] FIRRTL:197587 SRC:src/main/scala/chisel3/util/random/LFSR.scala:15:41 KIND:node :: node _T_2 = xor(_T_1, state[15])
[25] FIRRTL:197588 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[0], _T_2
[26] FIRRTL:197589 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[1], state[0]
[27] FIRRTL:197590 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[2], state[1]
[28] FIRRTL:197591 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[3], state[2]
[29] FIRRTL:197592 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[4], state[3]
[30] FIRRTL:197593 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[5], state[4]
[31] FIRRTL:197594 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[6], state[5]
[32] FIRRTL:197595 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[7], state[6]
[33] FIRRTL:197596 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[8], state[7]
[34] FIRRTL:197597 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[9], state[8]
[35] FIRRTL:197598 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[10], state[9]
[36] FIRRTL:197599 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[11], state[10]
[37] FIRRTL:197600 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[12], state[11]
[38] FIRRTL:197601 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[13], state[12]
[39] FIRRTL:197602 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[14], state[13]
[40] FIRRTL:197603 SRC:src/main/scala/chisel3/util/random/PRNG.scala:70:11 KIND:connect :: connect state[15], state[14]
[41] FIRRTL:197604 SRC:src/main/scala/chisel3/util/random/PRNG.scala:73:22 KIND:when :: when io.seed.valid :
[42] FIRRTL:197605 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[0], io.seed.bits[0]
[43] FIRRTL:197606 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[1], io.seed.bits[1]
[44] FIRRTL:197607 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[2], io.seed.bits[2]
[45] FIRRTL:197608 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[3], io.seed.bits[3]
[46] FIRRTL:197609 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[4], io.seed.bits[4]
[47] FIRRTL:197610 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[5], io.seed.bits[5]
[48] FIRRTL:197611 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[6], io.seed.bits[6]
[49] FIRRTL:197612 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[7], io.seed.bits[7]
[50] FIRRTL:197613 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[8], io.seed.bits[8]
[51] FIRRTL:197614 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[9], io.seed.bits[9]
[52] FIRRTL:197615 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[10], io.seed.bits[10]
[53] FIRRTL:197616 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[11], io.seed.bits[11]
[54] FIRRTL:197617 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[12], io.seed.bits[12]
[55] FIRRTL:197618 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[13], io.seed.bits[13]
[56] FIRRTL:197619 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[14], io.seed.bits[14]
[57] FIRRTL:197620 SRC:src/main/scala/chisel3/util/random/PRNG.scala:74:11 KIND:connect :: connect state[15], io.seed.bits[15]
[58] FIRRTL:197621 SRC:src/main/scala/chisel3/util/random/PRNG.scala:78:10 KIND:connect :: connect io.out, state
```

## Autonomous decision procedure

Analyze the entire WorkUnit autonomously. Do **not** stop after proposing a
semantic decomposition, and do **not** ask the human to choose occurrences,
predicates, identities, cases, axioms, or assumptions. When several abstractions
are plausible, choose the most conservative one that is grounded by the supplied
RTL evidence.

There are exactly two expected outcomes for this task:

1. **Current language is sufficient.** Build the complete candidate with the
   current schema and emit `FINAL MCM-AGENT RESULT` in this same response. Do this
   even when you are unsure whether the current prover can certify every candidate
   axiom; prover capability is decided later by `semantic-validate`.
2. **Current language has a real gap.** Use this outcome only when a
   memory/coherence-relevant semantic property is necessary for the abstraction
   but cannot be faithfully expressed by any current Formal AST form. Emit a
   section named `MCM-AGENT LANGUAGE GAP` and state:
   - the missing semantic concept;
   - the grounded RTL behavior that requires it;
   - why the current AST cannot express it without changing meaning;
   - the minimal **generic/reusable** extension you propose;
   - representative other hardware patterns that could reuse the extension.
   Do not emit an approximate candidate axiom just to avoid reporting the gap.

While analyzing, answer questions such as:

- Which physical events correspond to meaningful boundary occurrences, and is
  any RTL-grounded internal milestone needed to preserve an ordering fact?
- Which facts are persistent predicates rather than instantaneous occurrences?
- What stored state carries request/cache-line/transaction identity across cycles?
- Which case distinctions change the event path or ordering constraints?
- Which ordering, exclusion, flow, or conservation properties are actually
  supported by RTL?
- Which apparent liveness properties require environment assumptions?
- Which RTL details can be dropped without losing bug-relevant behavior?

## Formal axiom rule

Each `axioms[].formal` object is the axiom itself. The workflow derives its
human-readable formula, references, checker, and proof obligation from that AST.
This prevents a prose axiom from silently diverging from what the verifier proves.
Consult `expected_output_schema.json` for the exact allowed AST variants.

## Final machine result

If the current language is sufficient, this response **must** include a final
section named `FINAL MCM-AGENT RESULT` followed by one fenced JSON object. Do not
wait for another human turn before emitting it. The object must match
`expected_output_schema.json`. Use this exact envelope as the starting shape.

If and only if the current language has a necessary semantic gap, emit
`MCM-AGENT LANGUAGE GAP` instead of fabricating an approximate final JSON. A
formal-backend proof limitation alone never selects this path.

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.lfsr_prng-80cbcb83351fc3e0",
  "work_unit_id": "BoomNonBlockingDCache.lfsr_prng",
  "occurrences": [],
  "predicates": [],
  "identity_keys": [],
  "cases": [],
  "axioms": [],
  "assumptions": [],
  "unresolved": [],
  "rationale": [],
  "extensions": {}
}
```

IDs inside each list must be unique and stable within this result. Physical
references must use the exact IDs from this prompt. Evidence must use integer
statement IDs from the ledger.
