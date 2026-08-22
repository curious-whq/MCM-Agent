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

Task ID: `leaf_abstraction-LSU-state-0-10-75fa875f7278b61a`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.13`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::state-0-10`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 66
- logical statements: 25
- mapped/logical source lines: 16
- registers: 2
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

['stq_cleared', 'stq_clr_head_idx']

## Environment/frontier signals

['_T_216', '_T_217', '_T_219', '_T_220', '_T_221', '_T_222', '_T_233', '_T_36', '_s_uop_T', '_stq_clr_head_idx_T', '_stq_clr_head_idx_T_1', '_stq_clr_head_idx_T_10', '_stq_clr_head_idx_T_11', '_stq_clr_head_idx_T_12', '_stq_clr_head_idx_T_13', '_stq_clr_head_idx_T_14', '_stq_clr_head_idx_T_15', '_stq_clr_head_idx_T_2', '_stq_clr_head_idx_T_3', '_stq_clr_head_idx_T_4', '_stq_clr_head_idx_T_5', '_stq_clr_head_idx_T_6', '_stq_clr_head_idx_T_7', '_stq_clr_head_idx_T_8', '_stq_clr_head_idx_T_9', 'dis_uops[0].bits.stq_idx', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'io.core.brupdate.b1.mispredict_mask', 'io.core.exception', 's_uop.br_mask', 's_uop.is_amo', 'stq_cleared[*]', 'stq_clr_head_idx', 'stq_clr_head_idx_head_base', 'stq_clr_head_idx_head_overflow']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/lsu.scala:413-415
```scala
      stq_succeeded      (stq_idx)        := false.B
      stq_cleared        (stq_idx)        := false.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1071-1073
```scala
  val stq_clr_head_idx = SafeRegNext(LSUAgePriorityEncoder((0 until numStqEntries).map(i => {
    stq_valid(i) && !stq_cleared(i)
  }), stq_commit_head))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1090-1096
```scala
           stq_addr            (clr_idx).valid  &&
           stq_data            (clr_idx).valid  &&
          !stq_addr_is_virtual (clr_idx)        &&
          !s_uop.is_amo                         &&
          !stq_cleared         (clr_idx)        &&
          !IsKilledByBranch(io.core.brupdate, io.core.exception, s_uop)) {
      clr_valid := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1098-1100
```scala

      stq_cleared(clr_idx) := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1997-2000
```scala
    val base = AgePriorityEncoder(in, head_base)
    val overflow = Mux(base >= head_base, head_overflow, ~head_overflow)
    Cat(overflow, base)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2144-2146
```scala
    val reg = Reg(chiselTypeOf(x))
    reg := x
    reg
```

### generators/boom/src/main/scala/v4/util/util.scala:60-62
```scala
  def apply(brupdate: BrUpdateInfo, flush: Bool, uop_mask: UInt): Bool = {
    return maskMatch(brupdate.b1.mispredict_mask, uop_mask) || flush
  }
```

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
```

### generators/boom/src/main/scala/v4/util/util.scala:370-374
```scala
    val n_padded = 1 << width
    val temp_vec = (0 until n_padded).map(i => if (i < n) in(i) && i.U >= head else false.B) ++ in
    val idx = PriorityEncoder(temp_vec)
    idx(width-1, 0) //discard msb
  }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[274] FIRRTL:366646 SRC:<no-source-locator> KIND:node :: node _T_44 = bits(dis_uops[0].bits.stq_idx, 2, 0)
[275] FIRRTL:366647 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:414:43 KIND:connect :: connect stq_cleared[_T_44], UInt<1>(0h0)
[3351] FIRRTL:369723 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T = eq(stq_cleared[0], UInt<1>(0h0))
[3353] FIRRTL:369725 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_2 = eq(stq_cleared[1], UInt<1>(0h0))
[3355] FIRRTL:369727 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_4 = eq(stq_cleared[2], UInt<1>(0h0))
[3357] FIRRTL:369729 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_6 = eq(stq_cleared[3], UInt<1>(0h0))
[3359] FIRRTL:369731 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_8 = eq(stq_cleared[4], UInt<1>(0h0))
[3361] FIRRTL:369733 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_10 = eq(stq_cleared[5], UInt<1>(0h0))
[3363] FIRRTL:369735 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_12 = eq(stq_cleared[6], UInt<1>(0h0))
[3365] FIRRTL:369737 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1072:21 KIND:node :: node _stq_clr_head_idx_T_14 = eq(stq_cleared[7], UInt<1>(0h0))
[3369] FIRRTL:369741 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T = geq(UInt<1>(0h0), stq_clr_head_idx_head_base)
[3370] FIRRTL:369742 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_0 = and(_stq_clr_head_idx_T_1, _stq_clr_head_idx_base_temp_vec_T)
[3371] FIRRTL:369743 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_1 = geq(UInt<1>(0h1), stq_clr_head_idx_head_base)
[3372] FIRRTL:369744 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_1 = and(_stq_clr_head_idx_T_3, _stq_clr_head_idx_base_temp_vec_T_1)
[3373] FIRRTL:369745 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_2 = geq(UInt<2>(0h2), stq_clr_head_idx_head_base)
[3374] FIRRTL:369746 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_2 = and(_stq_clr_head_idx_T_5, _stq_clr_head_idx_base_temp_vec_T_2)
[3375] FIRRTL:369747 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_3 = geq(UInt<2>(0h3), stq_clr_head_idx_head_base)
[3376] FIRRTL:369748 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_3 = and(_stq_clr_head_idx_T_7, _stq_clr_head_idx_base_temp_vec_T_3)
[3377] FIRRTL:369749 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_4 = geq(UInt<3>(0h4), stq_clr_head_idx_head_base)
[3378] FIRRTL:369750 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_4 = and(_stq_clr_head_idx_T_9, _stq_clr_head_idx_base_temp_vec_T_4)
[3379] FIRRTL:369751 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_5 = geq(UInt<3>(0h5), stq_clr_head_idx_head_base)
[3380] FIRRTL:369752 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_5 = and(_stq_clr_head_idx_T_11, _stq_clr_head_idx_base_temp_vec_T_5)
[3381] FIRRTL:369753 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_6 = geq(UInt<3>(0h6), stq_clr_head_idx_head_base)
[3382] FIRRTL:369754 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_6 = and(_stq_clr_head_idx_T_13, _stq_clr_head_idx_base_temp_vec_T_6)
[3383] FIRRTL:369755 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_clr_head_idx_base_temp_vec_T_7 = geq(UInt<3>(0h7), stq_clr_head_idx_head_base)
[3384] FIRRTL:369756 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_clr_head_idx_base_temp_vec_7 = and(_stq_clr_head_idx_T_15, _stq_clr_head_idx_base_temp_vec_T_7)
[3385] FIRRTL:369757 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T = mux(_stq_clr_head_idx_T_13, UInt<4>(0he), UInt<4>(0hf))
[3386] FIRRTL:369758 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_1 = mux(_stq_clr_head_idx_T_11, UInt<4>(0hd), _stq_clr_head_idx_base_idx_T)
[3387] FIRRTL:369759 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_2 = mux(_stq_clr_head_idx_T_9, UInt<4>(0hc), _stq_clr_head_idx_base_idx_T_1)
[3388] FIRRTL:369760 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_3 = mux(_stq_clr_head_idx_T_7, UInt<4>(0hb), _stq_clr_head_idx_base_idx_T_2)
[3389] FIRRTL:369761 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_4 = mux(_stq_clr_head_idx_T_5, UInt<4>(0ha), _stq_clr_head_idx_base_idx_T_3)
[3390] FIRRTL:369762 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_5 = mux(_stq_clr_head_idx_T_3, UInt<4>(0h9), _stq_clr_head_idx_base_idx_T_4)
[3391] FIRRTL:369763 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_6 = mux(_stq_clr_head_idx_T_1, UInt<4>(0h8), _stq_clr_head_idx_base_idx_T_5)
[3392] FIRRTL:369764 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_7 = mux(stq_clr_head_idx_base_temp_vec_7, UInt<3>(0h7), _stq_clr_head_idx_base_idx_T_6)
[3393] FIRRTL:369765 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_8 = mux(stq_clr_head_idx_base_temp_vec_6, UInt<3>(0h6), _stq_clr_head_idx_base_idx_T_7)
[3394] FIRRTL:369766 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_9 = mux(stq_clr_head_idx_base_temp_vec_5, UInt<3>(0h5), _stq_clr_head_idx_base_idx_T_8)
[3395] FIRRTL:369767 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_10 = mux(stq_clr_head_idx_base_temp_vec_4, UInt<3>(0h4), _stq_clr_head_idx_base_idx_T_9)
[3396] FIRRTL:369768 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_11 = mux(stq_clr_head_idx_base_temp_vec_3, UInt<2>(0h3), _stq_clr_head_idx_base_idx_T_10)
[3397] FIRRTL:369769 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_12 = mux(stq_clr_head_idx_base_temp_vec_2, UInt<2>(0h2), _stq_clr_head_idx_base_idx_T_11)
[3398] FIRRTL:369770 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_clr_head_idx_base_idx_T_13 = mux(stq_clr_head_idx_base_temp_vec_1, UInt<1>(0h1), _stq_clr_head_idx_base_idx_T_12)
[3399] FIRRTL:369771 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node stq_clr_head_idx_base_idx = mux(stq_clr_head_idx_base_temp_vec_0, UInt<1>(0h0), _stq_clr_head_idx_base_idx_T_13)
[3400] FIRRTL:369772 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node stq_clr_head_idx_base = bits(stq_clr_head_idx_base_idx, 2, 0)
[3401] FIRRTL:369773 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:29 KIND:node :: node _stq_clr_head_idx_overflow_T = geq(stq_clr_head_idx_base, stq_clr_head_idx_head_base)
[3402] FIRRTL:369774 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:58 KIND:node :: node _stq_clr_head_idx_overflow_T_1 = not(stq_clr_head_idx_head_overflow)
[3403] FIRRTL:369775 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:23 KIND:node :: node stq_clr_head_idx_overflow = mux(_stq_clr_head_idx_overflow_T, stq_clr_head_idx_head_overflow, _stq_clr_head_idx_overflow_T_1)
[3404] FIRRTL:369776 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1999:8 KIND:node :: node _stq_clr_head_idx_T_16 = cat(stq_clr_head_idx_overflow, stq_clr_head_idx_base)
[3406] FIRRTL:369778 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2145:9 KIND:connect :: connect stq_clr_head_idx, _stq_clr_head_idx_T_16
[3424] FIRRTL:369796 SRC:<no-source-locator> KIND:node :: node _s_uop_T = bits(stq_clr_head_idx, 2, 0)
[3427] FIRRTL:369799 SRC:<no-source-locator> KIND:node :: node _T_216 = bits(stq_clr_head_idx, 2, 0)
[3428] FIRRTL:369800 SRC:<no-source-locator> KIND:node :: node _T_217 = bits(stq_clr_head_idx, 2, 0)
[3430] FIRRTL:369802 SRC:<no-source-locator> KIND:node :: node _T_219 = bits(stq_clr_head_idx, 2, 0)
[3432] FIRRTL:369804 SRC:<no-source-locator> KIND:node :: node _T_221 = bits(stq_clr_head_idx, 2, 0)
[3434] FIRRTL:369806 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1091:49 KIND:node :: node _T_223 = and(_T_220, _T_222)
[3435] FIRRTL:369807 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1093:11 KIND:node :: node _T_224 = eq(s_uop.is_amo, UInt<1>(0h0))
[3436] FIRRTL:369808 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1092:49 KIND:node :: node _T_225 = and(_T_223, _T_224)
[3437] FIRRTL:369809 SRC:<no-source-locator> KIND:node :: node _T_226 = bits(stq_clr_head_idx, 2, 0)
[3438] FIRRTL:369810 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1094:11 KIND:node :: node _T_227 = eq(stq_cleared[_T_226], UInt<1>(0h0))
[3439] FIRRTL:369811 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1093:49 KIND:node :: node _T_228 = and(_T_225, _T_227)
[3440] FIRRTL:369812 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_229 = and(io.core.brupdate.b1.mispredict_mask, s_uop.br_mask)
[3441] FIRRTL:369813 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_230 = neq(_T_229, UInt<1>(0h0))
[3442] FIRRTL:369814 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_231 = or(_T_230, io.core.exception)
[3443] FIRRTL:369815 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1095:11 KIND:node :: node _T_232 = eq(_T_231, UInt<1>(0h0))
[3444] FIRRTL:369816 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1094:49 KIND:node :: node _T_233 = and(_T_228, _T_232)
[3445] FIRRTL:369817 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1095:74 KIND:when :: when _T_233 :
[3453] FIRRTL:369825 SRC:<no-source-locator> KIND:node :: node _T_234 = bits(stq_clr_head_idx, 2, 0)
[3454] FIRRTL:369826 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1099:28 KIND:connect :: connect stq_cleared[_T_234], UInt<1>(0h1)
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
  "task_id": "leaf_abstraction-LSU-state-0-10-75fa875f7278b61a",
  "work_unit_id": "LSU::state-0-10",
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
