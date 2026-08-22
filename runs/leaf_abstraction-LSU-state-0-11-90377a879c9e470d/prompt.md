# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment: the µMCM language is intentionally
experimental and may be revised after discussion. Your job is to derive a
candidate abstraction that preserves information potentially relevant to
microarchitectural memory ordering, not to summarize the module in prose.

Task ID: `leaf_abstraction-LSU-state-0-11-90377a879c9e470d`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::state-0-11`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 6
- logical statements: 4
- mapped/logical source lines: 4
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

['stq_commit_head']

## Environment/frontier signals

['_T_1150', '_T_1151', 'commit_store', 'h0', 'h1', 'stq_commit_head']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[7912] FIRRTL:374284 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_1108 = add(stq_commit_head, UInt<1>(0h1))
[7913] FIRRTL:374285 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_1109 = tail(_T_1108, 1)
[7914] FIRRTL:374286 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _T_1110 = bits(_T_1109, 3, 0)
[7915] FIRRTL:374287 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1779:31 KIND:node :: node _T_1111 = mux(commit_store, _T_1110, stq_commit_head)
[7920] FIRRTL:374292 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1787:19 KIND:connect :: connect stq_commit_head, _T_1111
[8109] FIRRTL:374481 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1937:24 KIND:connect :: connect stq_commit_head, UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-LSU-state-0-11-90377a879c9e470d",
  "work_unit_id": "LSU::state-0-11",
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
