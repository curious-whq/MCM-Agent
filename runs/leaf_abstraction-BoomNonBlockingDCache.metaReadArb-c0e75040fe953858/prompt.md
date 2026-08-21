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

Task ID: `leaf_abstraction-BoomNonBlockingDCache.metaReadArb-c0e75040fe953858`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache.metaReadArb`
- module: `Arbiter6_BoomL1MetaReadReq`
- kind: `module`
- instance path: `BoomNonBlockingDCache.metaReadArb`
- leaf: `True`
- coverage complete: `True`
- raw statements: 44
- logical statements: 12
- mapped/logical source lines: 10
- registers: 0
- physical boundary events: 7

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

- `BoomNonBlockingDCache.metaReadArb::io.in[0].fire`
  - predicate: `io.in[0].valid && io.in[0].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[0].bits.req[0].idx', 'io.in[0].bits.req[0].tag', 'io.in[0].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.in[1].fire`
  - predicate: `io.in[1].valid && io.in[1].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[1].bits.req[0].idx', 'io.in[1].bits.req[0].tag', 'io.in[1].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.in[2].fire`
  - predicate: `io.in[2].valid && io.in[2].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[2].bits.req[0].idx', 'io.in[2].bits.req[0].tag', 'io.in[2].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.in[3].fire`
  - predicate: `io.in[3].valid && io.in[3].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[3].bits.req[0].idx', 'io.in[3].bits.req[0].tag', 'io.in[3].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.in[4].fire`
  - predicate: `io.in[4].valid && io.in[4].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[4].bits.req[0].idx', 'io.in[4].bits.req[0].tag', 'io.in[4].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.in[5].fire`
  - predicate: `io.in[5].valid && io.in[5].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[5].bits.req[0].idx', 'io.in[5].bits.req[0].tag', 'io.in[5].bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.metaReadArb::io.out.fire`
  - predicate: `io.out.valid && io.out.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.out.bits.req[0].idx', 'io.out.bits.req[0].tag', 'io.out.bits.req[0].way_en']
  - immediate registers: []
  - historical registers: []

## Concrete local state

[]

## Environment/frontier signals

['io.chosen', 'io.in[0].ready', 'io.in[0].valid', 'io.in[1].ready', 'io.in[1].valid', 'io.in[2].ready', 'io.in[2].valid', 'io.in[3].ready', 'io.in[3].valid', 'io.in[4].ready', 'io.in[4].valid', 'io.in[5].ready', 'io.in[5].valid', 'io.out.bits.req[0].idx', 'io.out.bits.req[0].tag', 'io.out.bits.req[0].way_en', 'io.out.ready', 'io.out.valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:197385 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197386 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197387 SRC:src/main/scala/chisel3/util/Arbiter.scala:140:14 KIND:structural :: output io : { flip in : { flip ready : UInt<1>, valid : UInt<1>, bits : { req : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}[1]}}[6], out : { flip ready : UInt<1>, valid : UInt<1>, bits : { req : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}[1]}}, chosen : UInt<3>}
[3] FIRRTL:197389 SRC:src/main/scala/chisel3/util/Arbiter.scala:142:13 KIND:connect :: connect io.chosen, UInt<3>(0h5)
[4] FIRRTL:197390 SRC:src/main/scala/chisel3/util/Arbiter.scala:143:15 KIND:connect :: connect io.out.bits, io.in[5].bits
[5] FIRRTL:197391 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[4].valid :
[6] FIRRTL:197392 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<3>(0h4)
[7] FIRRTL:197393 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[4].bits
[8] FIRRTL:197394 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[3].valid :
[9] FIRRTL:197395 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<2>(0h3)
[10] FIRRTL:197396 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[3].bits
[11] FIRRTL:197397 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[2].valid :
[12] FIRRTL:197398 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<2>(0h2)
[13] FIRRTL:197399 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[2].bits
[14] FIRRTL:197400 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[1].valid :
[15] FIRRTL:197401 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<1>(0h1)
[16] FIRRTL:197402 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[1].bits
[17] FIRRTL:197403 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[0].valid :
[18] FIRRTL:197404 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<1>(0h0)
[19] FIRRTL:197405 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[0].bits
[20] FIRRTL:197406 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:68 KIND:node :: node _grant_T = or(io.in[0].valid, io.in[1].valid)
[21] FIRRTL:197407 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:68 KIND:node :: node _grant_T_1 = or(_grant_T, io.in[2].valid)
[22] FIRRTL:197408 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:68 KIND:node :: node _grant_T_2 = or(_grant_T_1, io.in[3].valid)
[23] FIRRTL:197409 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:68 KIND:node :: node _grant_T_3 = or(_grant_T_2, io.in[4].valid)
[24] FIRRTL:197410 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_1 = eq(io.in[0].valid, UInt<1>(0h0))
[25] FIRRTL:197411 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_2 = eq(_grant_T, UInt<1>(0h0))
[26] FIRRTL:197412 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_3 = eq(_grant_T_1, UInt<1>(0h0))
[27] FIRRTL:197413 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_4 = eq(_grant_T_2, UInt<1>(0h0))
[28] FIRRTL:197414 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_5 = eq(_grant_T_3, UInt<1>(0h0))
[29] FIRRTL:197415 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_0_ready_T = and(UInt<1>(0h1), io.out.ready)
[30] FIRRTL:197416 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[0].ready, _io_in_0_ready_T
[31] FIRRTL:197417 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_1_ready_T = and(grant_1, io.out.ready)
[32] FIRRTL:197418 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[1].ready, _io_in_1_ready_T
[33] FIRRTL:197419 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_2_ready_T = and(grant_2, io.out.ready)
[34] FIRRTL:197420 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[2].ready, _io_in_2_ready_T
[35] FIRRTL:197421 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_3_ready_T = and(grant_3, io.out.ready)
[36] FIRRTL:197422 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[3].ready, _io_in_3_ready_T
[37] FIRRTL:197423 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_4_ready_T = and(grant_4, io.out.ready)
[38] FIRRTL:197424 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[4].ready, _io_in_4_ready_T
[39] FIRRTL:197425 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_5_ready_T = and(grant_5, io.out.ready)
[40] FIRRTL:197426 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[5].ready, _io_in_5_ready_T
[41] FIRRTL:197427 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:19 KIND:node :: node _io_out_valid_T = eq(grant_5, UInt<1>(0h0))
[42] FIRRTL:197428 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:31 KIND:node :: node _io_out_valid_T_1 = or(_io_out_valid_T, io.in[5].valid)
[43] FIRRTL:197429 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:16 KIND:connect :: connect io.out.valid, _io_out_valid_T_1
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.metaReadArb-c0e75040fe953858",
  "work_unit_id": "BoomNonBlockingDCache.metaReadArb",
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
