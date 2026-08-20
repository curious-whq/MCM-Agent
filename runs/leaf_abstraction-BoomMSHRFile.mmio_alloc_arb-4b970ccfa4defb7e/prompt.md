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

Task ID: `leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.8`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomMSHRFile.mmio_alloc_arb`
- module: `Arbiter1_Bool`
- kind: `module`
- instance path: `BoomMSHRFile.mmio_alloc_arb`
- leaf: `True`
- coverage complete: `True`
- raw statements: 10
- logical statements: 8
- mapped/logical source lines: 6
- registers: 0
- physical boundary events: 2

## Non-negotiable grounding rules

1. Distinguish occurrences from persistent predicates. A boundary occurrence
   must reference one or more physical event IDs listed below. A derived
   occurrence may have no physical event ID only when it has an exact RTL
   definition, concrete grounding, and statement evidence. If one semantic
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
   The `relation` field is required and must not be omitted. Existing relation axioms may additionally use
   `scope_index: {name: <index>, relation: same}` to state that the relation is
   pointwise over the same finite index (beat/entry/bank/etc.). Formal expressions
   may use `index_var` and `lookup` to refer to the bound index and an indexed
   storage element. These constructs are protocol-agnostic and must not be
   specialized to a particular module. If a semantic property that you judge
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

- `BoomMSHRFile.mmio_alloc_arb::io.in[0].fire`
  - predicate: `io.in[0].valid && io.in[0].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[0].bits']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile.mmio_alloc_arb::io.out.fire`
  - predicate: `io.out.valid && io.out.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.out.bits']
  - immediate registers: []
  - historical registers: []

## Concrete local state

[]

## Environment/frontier signals

['io.chosen', 'io.in[0].bits', 'io.in[0].ready', 'io.in[0].valid', 'io.out.bits', 'io.out.ready', 'io.out.valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:193969 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input clock : Clock
[1] FIRRTL:193970 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input reset : Reset
[2] FIRRTL:193971 SRC:src/main/scala/chisel3/util/Arbiter.scala:140:14 KIND:structural :: output io : { flip in : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<1>}[1], out : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<1>}, chosen : UInt<0>}
[3] FIRRTL:193973 SRC:src/main/scala/chisel3/util/Arbiter.scala:142:13 KIND:connect :: connect io.chosen, UInt<1>(0h0)
[4] FIRRTL:193974 SRC:src/main/scala/chisel3/util/Arbiter.scala:143:15 KIND:connect :: connect io.out.bits, io.in[0].bits
[5] FIRRTL:193975 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_0_ready_T = and(UInt<1>(0h1), io.out.ready)
[6] FIRRTL:193976 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[0].ready, _io_in_0_ready_T
[7] FIRRTL:193977 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:19 KIND:node :: node _io_out_valid_T = eq(UInt<1>(0h1), UInt<1>(0h0))
[8] FIRRTL:193978 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:31 KIND:node :: node _io_out_valid_T_1 = or(_io_out_valid_T, io.in[0].valid)
[9] FIRRTL:193979 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:16 KIND:connect :: connect io.out.valid, _io_out_valid_T_1
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
  "task_id": "leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e",
  "work_unit_id": "BoomMSHRFile.mmio_alloc_arb",
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
