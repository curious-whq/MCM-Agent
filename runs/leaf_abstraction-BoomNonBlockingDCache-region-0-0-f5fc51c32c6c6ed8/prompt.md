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

Task ID: `leaf_abstraction-BoomNonBlockingDCache-region-0-0-f5fc51c32c6c6ed8`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache::region-0-0`
- module: `BoomNonBlockingDCache`
- kind: `region`
- instance path: `BoomNonBlockingDCache`
- leaf: `True`
- coverage complete: `True`
- raw statements: 34
- logical statements: 22
- mapped/logical source lines: 16
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

- `BoomNonBlockingDCache::auto.out.b.fire`
  - predicate: `auto.out.b.valid && auto.out.b.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['auto.out.b.bits.address', 'auto.out.b.bits.corrupt', 'auto.out.b.bits.data', 'auto.out.b.bits.mask', 'auto.out.b.bits.opcode', 'auto.out.b.bits.param', 'auto.out.b.bits.size', 'auto.out.b.bits.source']
  - immediate registers: ['lrsc_count']
  - historical registers: ['lrsc_addr', 'lrsc_count', 's1_mshr_meta_read_way_en', 's1_replay_way_en', 's1_req', 's1_send_resp_or_nack', 's1_type', 's1_valid_REG', 's1_wb_way_en', 's2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_lr_REG', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_nack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']

## Concrete local state

['lrsc_count']

## Environment/frontier signals

['_T_31', '_T_35', '_T_36', '_T_39', '_T_41', '_s2_lr_T', '_s2_lr_T_2', 'h0', 'h1', 'lrsc_count', 'lrsc_valid', 'nodeOut.b.ready', 'prober.io.req.ready', 's2_has_permission[0]', 's2_hit[0]', 's2_lr', 's2_lr_REG', 's2_lrsc_addr_match[0]', 's2_nack[0]', 's2_tag_match_0', 's2_valid[0]']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:700-702
```scala
  val lrsc_addr  = Reg(UInt())
  val s2_lr = s2_req(0).uop.mem_cmd === M_XLR && (!RegNext(s1_nack(0)) || s2_type === t_replay)
  val s2_sc = s2_req(0).uop.mem_cmd === M_XSC && (!RegNext(s1_nack(0)) || s2_type === t_replay)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:704-710
```scala
  val s2_sc_fail = s2_sc && !s2_lrsc_addr_match(0)
  when (lrsc_count > 0.U) { lrsc_count := lrsc_count - 1.U }
  when (s2_valid(0) && ((s2_type === t_lsu && s2_hit(0) && !s2_nack(0)) ||
                     (s2_type === t_replay && s2_req(0).uop.mem_cmd =/= M_FLUSH_ALL))) {
    when (s2_lr) {
      lrsc_count := (lrscCycles - 1).U
      lrsc_addr := s2_req(0).addr >> blockOffBits
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:711-714
```scala
    }
    when (lrsc_count > 0.U) {
      lrsc_count := 0.U
    }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:716-724
```scala
  for (w <- 0 until lsuWidth) {
    when (s2_valid(w)                            &&
      s2_type === t_lsu                          &&
      !s2_hit(w)                                 &&
      !(s2_has_permission(w) && s2_tag_match(w)) &&
      s2_lrsc_addr_match(w)                      &&
      !s2_nack(w)) {
      lrsc_count := 0.U
    }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:821-823
```scala
  prober.io.req.valid   := tl_out.b.valid && !lrsc_valid
  tl_out.b.ready        := prober.io.req.ready && !lrsc_valid
  prober.io.req.bits    := tl_out.b.bits
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[1801] FIRRTL:199570 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:51 KIND:node :: node _s2_lr_T_1 = eq(s2_lr_REG, UInt<1>(0h0))
[1803] FIRRTL:199572 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:72 KIND:node :: node _s2_lr_T_3 = or(_s2_lr_T_1, _s2_lr_T_2)
[1804] FIRRTL:199573 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:47 KIND:node :: node s2_lr = and(_s2_lr_T, _s2_lr_T_3)
[1819] FIRRTL:199588 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:705:20 KIND:node :: node _T_30 = gt(lrsc_count, UInt<1>(0h0))
[1820] FIRRTL:199589 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:705:27 KIND:when :: when _T_30 :
[1821] FIRRTL:199590 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:705:54 KIND:node :: node _lrsc_count_T = sub(lrsc_count, UInt<1>(0h1))
[1822] FIRRTL:199591 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:705:54 KIND:node :: node _lrsc_count_T_1 = tail(_lrsc_count_T, 1)
[1823] FIRRTL:199592 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:705:40 KIND:connect :: connect lrsc_count, _lrsc_count_T_1
[1825] FIRRTL:199594 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:44 KIND:node :: node _T_32 = and(_T_31, s2_hit[0])
[1826] FIRRTL:199595 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:60 KIND:node :: node _T_33 = eq(s2_nack[0], UInt<1>(0h0))
[1827] FIRRTL:199596 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:57 KIND:node :: node _T_34 = and(_T_32, _T_33)
[1830] FIRRTL:199599 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:707:44 KIND:node :: node _T_37 = and(_T_35, _T_36)
[1831] FIRRTL:199600 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:73 KIND:node :: node _T_38 = or(_T_34, _T_37)
[1832] FIRRTL:199601 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:21 KIND:node :: node _T_39 = and(s2_valid[0], _T_38)
[1833] FIRRTL:199602 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:707:88 KIND:when :: when _T_39 :
[1834] FIRRTL:199603 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:708:18 KIND:when :: when s2_lr :
[1835] FIRRTL:199604 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:709:18 KIND:connect :: connect lrsc_count, UInt<7>(0h4f)
[1838] FIRRTL:199607 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:712:22 KIND:node :: node _T_40 = gt(lrsc_count, UInt<1>(0h0))
[1839] FIRRTL:199608 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:712:29 KIND:when :: when _T_40 :
[1840] FIRRTL:199609 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:713:18 KIND:connect :: connect lrsc_count, UInt<1>(0h0)
[1842] FIRRTL:199611 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:717:50 KIND:node :: node _T_42 = and(s2_valid[0], _T_41)
[1843] FIRRTL:199612 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:719:7 KIND:node :: node _T_43 = eq(s2_hit[0], UInt<1>(0h0))
[1844] FIRRTL:199613 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:718:50 KIND:node :: node _T_44 = and(_T_42, _T_43)
[1845] FIRRTL:199614 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:720:30 KIND:node :: node _T_45 = and(s2_has_permission[0], s2_tag_match_0)
[1846] FIRRTL:199615 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:720:7 KIND:node :: node _T_46 = eq(_T_45, UInt<1>(0h0))
[1847] FIRRTL:199616 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:719:50 KIND:node :: node _T_47 = and(_T_44, _T_46)
[1848] FIRRTL:199617 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:720:50 KIND:node :: node _T_48 = and(_T_47, s2_lrsc_addr_match[0])
[1849] FIRRTL:199618 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:722:7 KIND:node :: node _T_49 = eq(s2_nack[0], UInt<1>(0h0))
[1850] FIRRTL:199619 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:721:50 KIND:node :: node _T_50 = and(_T_48, _T_49)
[1851] FIRRTL:199620 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:722:20 KIND:when :: when _T_50 :
[1852] FIRRTL:199621 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:723:18 KIND:connect :: connect lrsc_count, UInt<1>(0h0)
[2486] FIRRTL:200255 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:822:51 KIND:node :: node _nodeOut_b_ready_T = eq(lrsc_valid, UInt<1>(0h0))
[2487] FIRRTL:200256 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:822:48 KIND:node :: node _nodeOut_b_ready_T_1 = and(prober.io.req.ready, _nodeOut_b_ready_T)
[2488] FIRRTL:200257 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:822:25 KIND:connect :: connect nodeOut.b.ready, _nodeOut_b_ready_T_1
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-0-f5fc51c32c6c6ed8",
  "work_unit_id": "BoomNonBlockingDCache::region-0-0",
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
