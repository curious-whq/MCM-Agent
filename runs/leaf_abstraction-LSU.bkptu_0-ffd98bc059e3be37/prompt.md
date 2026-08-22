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

Task ID: `leaf_abstraction-LSU.bkptu_0-ffd98bc059e3be37`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.bkptu_0`
- module: `BreakpointUnit_4`
- kind: `module`
- instance path: `LSU.bkptu_0`
- leaf: `True`
- coverage complete: `True`
- raw statements: 9
- logical statements: 8
- mapped/logical source lines: 8
- registers: 0
- physical boundary events: 0

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
   before the colliding real write in `co`. For a finite candidate vector whose unique winner is chosen by an indexed
   linear or rotated order and exposed after a fixed register delay, use
   `indexed_priority_select`. Its `candidate` is an indexed Boolean expression:
   use `bit(vector, index_var)` for a packed candidate vector, or compose
   `lookup(array, index_var)` terms with `and` / `or` / `not` when eligibility
   is computed from several indexed arrays. If lowering exposes the finite
   candidate vector as separate scalar frontier signals, use
   `indexed_cases(index_var; [candidate_0, ..., candidate_n])`; its value count
   must equal `index.count`. Do not reference a source-level array that is not
   listed in this WorkUnit's state/frontier; preserve the partition boundary by
   using the exposed scalar frontier candidates and leave their parent-local
   construction to composition;
   `priority.kind` is `linear_min`, `linear_max`, `cyclic_predecessor`, or
   `cyclic_successor`, with a `pivot` expression on cyclic forms. The cyclic
   forms use optional `pivot_position`: `last` (the backward-compatible default)
   is strict around the pivot, while `first` visits the pivot itself before
   moving in the predecessor/successor direction. `result.index` names the
   selected-index output, or uses a constant `bit`/`slice` projection when a
   register also carries an epoch bit; `result.found` is optional when RTL exposes a separate
   nonempty flag. `latency_cycles` records the
   exact sampling delay, and unreset result registers use
   `initialization: {"kind":"implicit_unconstrained"}`.
   For a scalar register whose complete one-cycle next state is selected from
   priority guarded writers, use `register_transition`. List updates in
   highest-to-lowest priority order with `priority: "first_match"`, then give
   the exact hold/fallback expression in `default`. Guards may use scalar
   Boolean `signal`/`and`/`or`/`not` expressions. For a circular pointer increment
   use `modular_increment(value, modulus)`; this means the selected expression
   is sampled at cycle t and assigned to the register at t+1, never a same-cycle
   equality. Include every RTL writer: if a writer's enclosing control is not
   grounded in the handoff, report a grounding gap rather than omitting it.
   If a semantic property that you judge **necessary** for a sound/useful
   parent-facing abstraction cannot be faithfully
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



## Concrete local state

[]

## Environment/frontier signals

['io.debug_if', 'io.debug_ld', 'io.debug_st', 'io.xcpt_if', 'io.xcpt_ld', 'io.xcpt_st']

## Source evidence

### generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:78-81
```scala

class BreakpointUnit(n: Int)(implicit val p: Parameters) extends Module with HasCoreParameters {
  val io = IO(new Bundle {
    val status = Input(new MStatus())
```

### generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:95-102
```scala

  io.xcpt_if := false.B
  io.xcpt_ld := false.B
  io.xcpt_st := false.B
  io.debug_if := false.B
  io.debug_ld := false.B
  io.debug_st := false.B
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:366098 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:79:7 KIND:structural :: input clock : Clock
[1] FIRRTL:366099 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:79:7 KIND:structural :: input reset : Reset
[2] FIRRTL:366100 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:80:14 KIND:structural :: output io : { flip status : { debug : UInt<1>, cease : UInt<1>, wfi : UInt<1>, isa : UInt<32>, dprv : UInt<2>, dv : UInt<1>, prv : UInt<2>, v : UInt<1>, sd : UInt<1>, zero2 : UInt<23>, mpv : UInt<1>, gva : UInt<1>, mbe : UInt<1>, sbe : UInt<1>, sxl : UInt<2>, uxl : UInt<2>, sd_rv32 : UInt<1>, zero1 : UInt<8>, tsr : UInt<1>, tw : UInt<1>, tvm : UInt<1>, mxr : UInt<1>, sum : UInt<1>, mprv : UInt<1>, xs : UInt<2>, fs : UInt<2>, mpp : UInt<2>, vs : UInt<2>, spp : UInt<1>, mpie : UInt<1>, ube : UInt<1>, spie : UInt<1>, upie : UInt<1>, mie : UInt<1>, hie : UInt<1>, sie : UInt<1>, uie : UInt<1>}, flip bp : { control : { ttype : UInt<4>, dmode : UInt<1>, maskmax : UInt<6>, reserved : UInt<40>, action : UInt<1>, chain : UInt<1>, zero : UInt<2>, tmatch : UInt<2>, m : UInt<1>, h : UInt<1>, s : UInt<1>, u : UInt<1>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, address : UInt<39>, textra : { mvalue : UInt<0>, mselect : UInt<1>, pad2 : UInt<48>, svalue : UInt<0>, pad1 : UInt<1>, sselect : UInt<1>}}[0], flip pc : UInt<39>, flip ea : UInt<39>, flip mcontext : UInt<0>, flip scontext : UInt<0>, xcpt_if : UInt<1>, xcpt_ld : UInt<1>, xcpt_st : UInt<1>, debug_if : UInt<1>, debug_ld : UInt<1>, debug_st : UInt<1>, bpwatch : { valid : UInt<1>[1], rvalid : UInt<1>[1], wvalid : UInt<1>[1], ivalid : UInt<1>[1], action : UInt<3>}[0]}
[3] FIRRTL:366102 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:96:14 KIND:connect :: connect io.xcpt_if, UInt<1>(0h0)
[4] FIRRTL:366103 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:97:14 KIND:connect :: connect io.xcpt_ld, UInt<1>(0h0)
[5] FIRRTL:366104 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:98:14 KIND:connect :: connect io.xcpt_st, UInt<1>(0h0)
[6] FIRRTL:366105 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:99:15 KIND:connect :: connect io.debug_if, UInt<1>(0h0)
[7] FIRRTL:366106 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:100:15 KIND:connect :: connect io.debug_ld, UInt<1>(0h0)
[8] FIRRTL:366107 SRC:generators/rocket-chip/src/main/scala/rocket/Breakpoint.scala:101:15 KIND:connect :: connect io.debug_st, UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-LSU.bkptu_0-ffd98bc059e3be37",
  "work_unit_id": "LSU.bkptu_0",
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
