# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment: the µMCM language is intentionally
experimental and may be revised after discussion. Your job is to derive a
candidate abstraction that preserves information potentially relevant to
microarchitectural memory ordering, not to summarize the module in prose.

Task ID: `leaf_abstraction-LSU-state-0-13-6709bdbe9122e581`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::state-0-13`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 10
- logical statements: 6
- mapped/logical source lines: 6
- registers: 1
- physical boundary events: 0

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
   finite indexed occurrence sets. Existing relation axioms may additionally use
   `scope_index: {name: <index>, relation: same}` to state that the relation is
   pointwise over the same finite index (beat/entry/bank/etc.). Formal expressions
   may use `index_var` and `lookup` to refer to the bound index and an indexed
   storage element. These constructs are protocol-agnostic and must not be
   specialized to a particular module. If the required concept still cannot be
   expressed, put it in `extensions` or `unresolved` instead of approximating it.
For a scalar register whose complete one-cycle next state is selected from priority guarded writers, use `register_transition`. List updates in highest-to-lowest priority order with `priority: "first_match"`, then give the exact hold/fallback expression in `default`. Guards may use scalar Boolean `signal`/`and`/`or`/`not` expressions. For a circular pointer increment use `modular_increment(value, modulus)`; this means the selected expression is sampled at cycle t and assigned to the register at t+1, never a same-cycle equality. Include every RTL writer.

9. This stage proposes **candidate** axioms. Do not assert that formal validation
   has already proved them.

## Physical boundary events



## Concrete local state

['stq_tail']

## Environment/frontier signals

['_T_1092', '_T_1150', '_T_1151', 'dis_st_val', 'h0', 'h1', 'io.core.brupdate.b2.uop.stq_idx', 'io.core.dis_uops[0].bits.exception', 'io.core.dis_uops[0].bits.uses_stq', 'io.core.dis_uops[0].valid', 'stq_tail']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[163] FIRRTL:366535 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:376:48 KIND:node :: node _dis_st_val_T = and(io.core.dis_uops[0].valid, io.core.dis_uops[0].bits.uses_stq)
[164] FIRRTL:366536 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:376:88 KIND:node :: node _dis_st_val_T_1 = eq(io.core.dis_uops[0].bits.exception, UInt<1>(0h0))
[165] FIRRTL:366537 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:376:85 KIND:node :: node dis_st_val = and(_dis_st_val_T, _dis_st_val_T_1)
[283] FIRRTL:366655 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_52 = add(stq_tail, UInt<1>(0h1))
[284] FIRRTL:366656 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_53 = tail(_T_52, 1)
[285] FIRRTL:366657 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _T_54 = bits(_T_53, 3, 0)
[286] FIRRTL:366658 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:423:21 KIND:node :: node _T_55 = mux(dis_st_val, _T_54, stq_tail)
[313] FIRRTL:366685 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:436:12 KIND:connect :: connect stq_tail, _T_55
[7873] FIRRTL:374245 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1735:14 KIND:connect :: connect stq_tail, io.core.brupdate.b2.uop.stq_idx
[8108] FIRRTL:374480 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1936:16 KIND:connect :: connect stq_tail, UInt<1>(0h0)
```

## What to do in the conversation

First reason about the WorkUnit and propose whatever semantic decomposition is
most useful. We may discuss, challenge, and revise it interactively. The current
v0.2 µMCM idea (occurrences, persistent predicates, identity, guarded cases,
axioms, assumptions) is a working hypothesis, not a sacred final design.

Focus on questions such as:

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

Only when the discussion has converged, emit a final section named
`FINAL MCM-AGENT RESULT` followed by one fenced JSON object. The object must
match `expected_output_schema.json`. Use this exact envelope as the starting
shape:

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-LSU-state-0-13-6709bdbe9122e581",
  "work_unit_id": "LSU::state-0-13",
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
