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

Task ID: `leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-1`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 67
- logical statements: 22
- mapped/logical source lines: 16
- registers: 3
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

- `LSU::io.core.clr_unsafe[0].valid`
  - predicate: `io.core.clr_unsafe[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.core.clr_unsafe[0].bits']
  - immediate registers: ['io_core_clr_unsafe_0_valid_REG', 'io_core_clr_unsafe_0_valid_REG_2', 'io_core_clr_unsafe_0_valid_REG_3']
  - historical registers: ['REG_1', 'REG_10', 'REG_11', 'REG_2', 'REG_3', 'REG_4', 'REG_5', 'REG_6', 'REG_7', 'REG_8', 'REG_9', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'io_core_clr_unsafe_0_bits_REG', 'io_core_clr_unsafe_0_valid_REG', 'io_core_clr_unsafe_0_valid_REG_1', 'io_core_clr_unsafe_0_valid_REG_2', 'io_core_clr_unsafe_0_valid_REG_3', 'io_dmem_s1_kill_0_REG', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

['io_core_clr_unsafe_0_valid_REG', 'io_core_clr_unsafe_0_valid_REG_2', 'io_core_clr_unsafe_0_valid_REG_3']

## Environment/frontier signals

['REG_1', 'REG_10', 'REG_2', 'REG_3', 'REG_4', 'REG_5', 'REG_6', 'REG_7', 'REG_8', 'REG_9', '_T_258', '_T_266', '_T_272', '_T_281', '_T_284', '_T_310', '_T_318', '_T_324', '_T_333', '_T_336', '_T_362', '_T_370', '_T_376', '_T_385', '_T_388', '_T_414', '_T_422', '_T_428', '_T_437', '_T_440', '_T_466', '_T_474', '_T_480', '_T_489', '_T_492', '_T_518', '_T_526', '_T_532', '_T_541', '_T_544', '_T_570', '_T_578', '_T_584', '_T_593', '_T_596', '_T_622', '_T_630', '_T_636', '_T_645', '_T_648', '_T_681', '_T_714', '_T_727', '_T_867', 'do_ld_search[0]', 'do_st_search[0]', 'failed_load', 'fired_load_agen[0]', 'h0', 'h1', 'io.core.clr_unsafe[0].bits', 'io.core.clr_unsafe[0].valid', 'io.dmem.nack[0].valid', 'io.dmem.s1_kill[0]', 'io_core_clr_unsafe_0_bits_REG', 'io_core_clr_unsafe_0_valid_REG', 'io_core_clr_unsafe_0_valid_REG_1', 'io_core_clr_unsafe_0_valid_REG_2', 'io_core_clr_unsafe_0_valid_REG_3', 'io_dmem_s1_kill_0_REG', 'lcam_younger_load_mask[0][0]', 'lcam_younger_load_mask[0][1]', 'lcam_younger_load_mask[0][2]', 'lcam_younger_load_mask[0][3]', 'lcam_younger_load_mask[0][4]', 'lcam_younger_load_mask[0][5]', 'lcam_younger_load_mask[0][6]', 'lcam_younger_load_mask[0][7]']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[2377] FIRRTL:368749 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:888:24 KIND:connect :: connect io.dmem.s1_kill[0], io_dmem_s1_kill_0_REG
[3839] FIRRTL:370211 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1181:29 KIND:connect :: connect failed_load, UInt<1>(0h0)
[3946] FIRRTL:370318 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[3981] FIRRTL:370353 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_288 = eq(fired_load_agen[0], UInt<1>(0h0))
[3982] FIRRTL:370354 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_289 = and(REG_1, _T_288)
[3983] FIRRTL:370355 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_289 :
[3984] FIRRTL:370356 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4092] FIRRTL:370464 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4127] FIRRTL:370499 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_340 = eq(fired_load_agen[0], UInt<1>(0h0))
[4128] FIRRTL:370500 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_341 = and(REG_2, _T_340)
[4129] FIRRTL:370501 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_341 :
[4130] FIRRTL:370502 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4238] FIRRTL:370610 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4273] FIRRTL:370645 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_392 = eq(fired_load_agen[0], UInt<1>(0h0))
[4274] FIRRTL:370646 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_393 = and(REG_3, _T_392)
[4275] FIRRTL:370647 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_393 :
[4276] FIRRTL:370648 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4384] FIRRTL:370756 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4419] FIRRTL:370791 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_444 = eq(fired_load_agen[0], UInt<1>(0h0))
[4420] FIRRTL:370792 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_445 = and(REG_4, _T_444)
[4421] FIRRTL:370793 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_445 :
[4422] FIRRTL:370794 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4530] FIRRTL:370902 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4565] FIRRTL:370937 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_496 = eq(fired_load_agen[0], UInt<1>(0h0))
[4566] FIRRTL:370938 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_497 = and(REG_5, _T_496)
[4567] FIRRTL:370939 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_497 :
[4568] FIRRTL:370940 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4676] FIRRTL:371048 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4711] FIRRTL:371083 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_548 = eq(fired_load_agen[0], UInt<1>(0h0))
[4712] FIRRTL:371084 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_549 = and(REG_6, _T_548)
[4713] FIRRTL:371085 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_549 :
[4714] FIRRTL:371086 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4822] FIRRTL:371194 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[4857] FIRRTL:371229 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_600 = eq(fired_load_agen[0], UInt<1>(0h0))
[4858] FIRRTL:371230 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_601 = and(REG_7, _T_600)
[4859] FIRRTL:371231 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_601 :
[4860] FIRRTL:371232 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[4968] FIRRTL:371340 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1235:23 KIND:connect :: connect failed_load, UInt<1>(0h1)
[5003] FIRRTL:371375 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:64 KIND:node :: node _T_652 = eq(fired_load_agen[0], UInt<1>(0h0))
[5004] FIRRTL:371376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:61 KIND:node :: node _T_653 = and(REG_8, _T_652)
[5005] FIRRTL:371377 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1263:85 KIND:when :: when _T_653 :
[5006] FIRRTL:371378 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1264:48 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[5083] FIRRTL:371455 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1288:60 KIND:node :: node _T_685 = eq(fired_load_agen[0], UInt<1>(0h0))
[5084] FIRRTL:371456 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1288:57 KIND:node :: node _T_686 = and(REG_9, _T_685)
[5085] FIRRTL:371457 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1288:81 KIND:when :: when _T_686 :
[5086] FIRRTL:371458 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1289:30 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[5159] FIRRTL:371531 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1307:21 KIND:connect :: connect failed_load, UInt<1>(0h1)
[5222] FIRRTL:371594 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1320:21 KIND:connect :: connect failed_load, UInt<1>(0h1)
[5959] FIRRTL:372331 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1376:58 KIND:node :: node _T_870 = eq(fired_load_agen[0], UInt<1>(0h0))
[5960] FIRRTL:372332 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1376:55 KIND:node :: node _T_871 = and(REG_10, _T_870)
[5961] FIRRTL:372333 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1376:79 KIND:when :: when _T_871 :
[5962] FIRRTL:372334 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1377:42 KIND:connect :: connect io.dmem.s1_kill[0], UInt<1>(0h1)
[6093] FIRRTL:372465 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1444:14 KIND:connect :: connect io_core_clr_unsafe_0_valid_REG, do_st_search[0]
[6094] FIRRTL:372466 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:8 KIND:node :: node _io_core_clr_unsafe_0_valid_T = eq(io.dmem.nack[0].valid, UInt<1>(0h0))
[6095] FIRRTL:372467 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:61 KIND:node :: node _io_core_clr_unsafe_0_valid_T_1 = eq(fired_load_agen[0], UInt<1>(0h0))
[6096] FIRRTL:372468 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:58 KIND:node :: node _io_core_clr_unsafe_0_valid_T_2 = and(do_ld_search[0], _io_core_clr_unsafe_0_valid_T_1)
[6097] FIRRTL:372469 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:84 KIND:node :: node _io_core_clr_unsafe_0_valid_T_3 = eq(io.dmem.s1_kill[0], UInt<1>(0h0))
[6098] FIRRTL:372470 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:81 KIND:node :: node _io_core_clr_unsafe_0_valid_T_4 = and(_io_core_clr_unsafe_0_valid_T_2, _io_core_clr_unsafe_0_valid_T_3)
[6101] FIRRTL:372473 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:104 KIND:node :: node _io_core_clr_unsafe_0_valid_T_5 = and(_io_core_clr_unsafe_0_valid_T_4, io_core_clr_unsafe_0_valid_REG_1)
[6103] FIRRTL:372475 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:41 KIND:connect :: connect io_core_clr_unsafe_0_valid_REG_2, _io_core_clr_unsafe_0_valid_T_5
[6104] FIRRTL:372476 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1445:31 KIND:node :: node _io_core_clr_unsafe_0_valid_T_6 = and(_io_core_clr_unsafe_0_valid_T, io_core_clr_unsafe_0_valid_REG_2)
[6105] FIRRTL:372477 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1444:32 KIND:node :: node _io_core_clr_unsafe_0_valid_T_7 = or(io_core_clr_unsafe_0_valid_REG, _io_core_clr_unsafe_0_valid_T_6)
[6107] FIRRTL:372479 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1446:18 KIND:connect :: connect io_core_clr_unsafe_0_valid_REG_3, failed_load
[6108] FIRRTL:372480 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1446:10 KIND:node :: node _io_core_clr_unsafe_0_valid_T_8 = eq(io_core_clr_unsafe_0_valid_REG_3, UInt<1>(0h0))
[6109] FIRRTL:372481 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1446:7 KIND:node :: node _io_core_clr_unsafe_0_valid_T_9 = and(_io_core_clr_unsafe_0_valid_T_7, _io_core_clr_unsafe_0_valid_T_8)
[6110] FIRRTL:372482 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1443:33 KIND:connect :: connect io.core.clr_unsafe[0].valid, _io_core_clr_unsafe_0_valid_T_9
[6113] FIRRTL:372485 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1447:33 KIND:connect :: connect io.core.clr_unsafe[0].bits, io_core_clr_unsafe_0_bits_REG
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
  "task_id": "leaf_abstraction-LSU-region-0-1-5c5dc0e312bfb510",
  "work_unit_id": "LSU::region-0-1",
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
