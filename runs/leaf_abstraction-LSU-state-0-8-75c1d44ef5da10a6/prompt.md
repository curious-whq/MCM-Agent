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

Task ID: `leaf_abstraction-LSU-state-0-8-75c1d44ef5da10a6`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::state-0-8`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 1338
- logical statements: 260
- mapped/logical source lines: 197
- registers: 40
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



## Concrete local state

['fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_ldq_idx_reg', 'ldq_debug_wb_data', 'ldq_enq_retry_idx', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_ld_byte_mask', 'ldq_observed', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_xcpt_uops', 'mem_xcpt_valids', 's1_executing_loads', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_data', 'stq_enq_retry_idx', 'stq_succeeded', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Environment/frontier signals

['_T_1009', '_T_1021', '_T_1033', '_T_1045', '_T_1057', '_T_1121', '_T_1122', '_T_1123', '_T_1124', '_T_1127', '_T_1128', '_T_1136', '_T_1138', '_T_1141', '_T_1143', '_T_1150', '_T_1151', '_T_145', '_T_164', '_T_176', '_T_268', '_T_269', '_T_27', '_T_272', '_T_281', '_T_283', '_T_284', '_T_320', '_T_321', '_T_324', '_T_333', '_T_335', '_T_336', '_T_36', '_T_372', '_T_373', '_T_376', '_T_385', '_T_387', '_T_388', '_T_424', '_T_425', '_T_428', '_T_437', '_T_439', '_T_440', '_T_476', '_T_477', '_T_480', '_T_489', '_T_491', '_T_492', '_T_528', '_T_529', '_T_532', '_T_541', '_T_543', '_T_544', '_T_580', '_T_581', '_T_584', '_T_593', '_T_595', '_T_596', '_T_632', '_T_633', '_T_636', '_T_645', '_T_647', '_T_648', '_T_681', '_T_72', '_T_867', '_T_924', '_T_942', '_T_944', '_T_973', '_T_985', '_T_997', '_WIRE_10', '_WIRE_8', '_WIRE_9', '_block_addr_matches_T_1', '_block_addr_matches_T_10', '_block_addr_matches_T_13', '_block_addr_matches_T_16', '_block_addr_matches_T_19', '_block_addr_matches_T_22', '_block_addr_matches_T_4', '_block_addr_matches_T_7', '_dmem_resp_fired_WIRE', '_dword_addr_matches_T_1', '_dword_addr_matches_T_13', '_dword_addr_matches_T_17', '_dword_addr_matches_T_21', '_dword_addr_matches_T_25', '_dword_addr_matches_T_29', '_dword_addr_matches_T_5', '_dword_addr_matches_T_9', '_kill_forward_WIRE', '_lcam_uop_WIRE', '_ldq_enq_retry_idx_T', '_ldq_enq_retry_idx_T_12', '_ldq_enq_retry_idx_T_16', '_ldq_enq_retry_idx_T_20', '_ldq_enq_retry_idx_T_24', '_ldq_enq_retry_idx_T_28', '_ldq_enq_retry_idx_T_4', '_ldq_enq_retry_idx_T_8', '_mem_ldq_e_WIRE', '_mem_paddr_WIRE', '_mem_xcpt_valids_WIRE', '_stq_almost_full_WIRE', '_stq_almost_full_WIRE_1', '_stq_almost_full_WIRE_2', '_stq_tail_plus_T', '_uop_T', 'addr_matches[0][0]', 'addr_matches[0][1]', 'addr_matches[0][2]', 'addr_matches[0][3]', 'addr_matches[0][4]', 'addr_matches[0][5]', 'addr_matches[0][6]', 'addr_matches[0][7]', 'ae_ld[0]', 'ae_st[0]', 'age1_age_10', 'age1_age_9', 'age1_overflow_10', 'age1_overflow_9', 'age_matches[0][0]', 'age_matches[0][1]', 'age_matches[0][2]', 'age_matches[0][3]', 'age_matches[0][4]', 'age_matches[0][5]', 'age_matches[0][6]', 'age_matches[0][7]', 'age_matches_0_0_head_carry', 'age_matches_0_0_real_head_idx', 'age_matches_0_1_head_carry', 'age_matches_0_1_real_head_idx', 'age_matches_0_2_head_carry', 'age_matches_0_2_real_head_idx', 'age_matches_0_3_head_carry', 'age_matches_0_3_real_head_idx', 'age_matches_0_4_head_carry', 'age_matches_0_4_real_head_idx', 'age_matches_0_5_head_carry', 'age_matches_0_5_real_head_idx', 'age_matches_0_6_head_carry', 'age_matches_0_6_real_head_idx', 'age_matches_0_7_head_carry', 'age_matches_0_7_real_head_idx', 'bkptu_0.io.debug_ld', 'bkptu_0.io.debug_st', 'bkptu_0.io.xcpt_ld', 'bkptu_0.io.xcpt_st', 'block_addr_matches[0]', 'block_addr_matches_1[0]', 'block_addr_matches_2[0]', 'block_addr_matches_3[0]', 'block_addr_matches_4[0]', 'block_addr_matches_5[0]', 'block_addr_matches_6[0]', 'block_addr_matches_7[0]', 'bp[0]', 'clear_store', 'dbg_bp[0]', 'dis_uops[0].bits.br_mask', 'dis_uops[0].bits.ldq_idx', 'dis_uops[0].bits.stq_idx', 'dis_uops[0].bits.uses_ldq', 'dis_uops[0].valid', 'dmem_req[0].bits.addr', 'dmem_req_fire[0]', 'do_ld_search[0]', 'do_st_search[0]', 'dtlb.io.resp[0].ae.ld', 'dtlb.io.resp[0].ae.st', 'dtlb.io.resp[0].gf.ld', 'dtlb.io.resp[0].gf.st', 'dtlb.io.resp[0].ma.ld', 'dtlb.io.resp[0].ma.st', 'dtlb.io.resp[0].pf.ld', 'dtlb.io.resp[0].pf.st', 'dword_addr_matches[0]', 'dword_addr_matches_1[0]', 'dword_addr_matches_2[0]', 'dword_addr_matches_3[0]', 'dword_addr_matches_4[0]', 'dword_addr_matches_5[0]', 'dword_addr_matches_6[0]', 'dword_addr_matches_7[0]', 'exe_agen_killed[0]', 'exe_tlb_miss', 'exe_tlb_miss[0]', 'exe_tlb_paddr[0]', 'exe_tlb_uop[0].br_mask', 'exe_tlb_uop[0].is_fence', 'exe_tlb_uop[0].mem_size', 'exe_tlb_uop[0].uses_ldq', 'exe_tlb_uop[0].uses_stq', 'exe_tlb_vaddr[0]', 'exe_tlb_valid[0]', 'fast_stq_valids', 'fired_load_agen[0]', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release[0]', 'fired_store_agen[0]', 'fired_store_agen_REG', 'fired_store_retry[0]', 'fired_store_retry_REG', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'ha', 'hb', 'hc', 'hd', 'he', 'hella_paddr', 'hella_state', 'hf', 'hf0', 'hff', 'io.core.agen[0].bits.uop.stq_idx', 'io.core.brupdate.b1.mispredict_mask', 'io.core.brupdate.b1.resolve_mask', 'io.core.exception', 'io.dmem.ll_resp.bits.is_hella', 'io.dmem.ll_resp.ready', 'io.dmem.ll_resp.valid', 'io.dmem.nack[0].bits.addr', 'io.dmem.nack[0].bits.is_hella', 'io.dmem.nack[0].bits.uop.ldq_idx', 'io.dmem.nack[0].bits.uop.mem_size', 'io.dmem.nack[0].bits.uop.uses_ldq', 'io.dmem.nack[0].valid', 'io.dmem.resp[0].bits.is_hella', 'io.dmem.resp[0].valid', 'io.dmem.s1_nack_advisory[0]', 'io.dmem.store_ack[0].bits.uop.stq_idx', 'io.dmem.store_ack[0].valid', 'io.hellacache.req.ready', 'io.hellacache.s1_kill', 'io.hellacache.s2_kill', 'iresp[0].valid', 'lcam_addr[0]', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx', 'lcam_ldq_idx[0]', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_mask[0]', 'lcam_mask_mask', 'lcam_uop[0].pdst', 'lcam_uop[0].rob_idx', 'lcam_uop[0].stq_idx', 'lcam_younger_load_mask[0][0]', 'lcam_younger_load_mask[0][1]', 'lcam_younger_load_mask[0][2]', 'lcam_younger_load_mask[0][3]', 'lcam_younger_load_mask[0][4]', 'lcam_younger_load_mask[0][5]', 'lcam_younger_load_mask[0][6]', 'lcam_younger_load_mask[0][7]', 'lcam_younger_load_mask_0_0_real_tail_idx', 'lcam_younger_load_mask_0_0_tail_carry', 'lcam_younger_load_mask_0_1_real_tail_idx', 'lcam_younger_load_mask_0_1_tail_carry', 'lcam_younger_load_mask_0_2_real_tail_idx', 'lcam_younger_load_mask_0_2_tail_carry', 'lcam_younger_load_mask_0_3_real_tail_idx', 'lcam_younger_load_mask_0_3_tail_carry', 'lcam_younger_load_mask_0_4_real_tail_idx', 'lcam_younger_load_mask_0_4_tail_carry', 'lcam_younger_load_mask_0_5_real_tail_idx', 'lcam_younger_load_mask_0_5_tail_carry', 'lcam_younger_load_mask_0_6_real_tail_idx', 'lcam_younger_load_mask_0_6_tail_carry', 'lcam_younger_load_mask_0_7_real_tail_idx', 'lcam_younger_load_mask_0_7_tail_carry', 'ldq_enq_retry_idx', 'ldq_enq_retry_idx_head_base', 'ldq_enq_retry_idx_head_overflow', 'ldq_idx', 'ldq_ld_byte_mask[*]', 'ldq_ld_byte_mask[0]', 'ldq_ld_byte_mask[1]', 'ldq_ld_byte_mask[2]', 'ldq_ld_byte_mask[3]', 'ldq_ld_byte_mask[4]', 'ldq_ld_byte_mask[5]', 'ldq_ld_byte_mask[6]', 'ldq_ld_byte_mask[7]', 'ldq_ld_byte_mask_mask', 'ldq_wakeup_e', 'ldq_wakeup_e.bits.uop.br_mask', 'ldst_addr_matches[0]', 'ma_ld[0]', 'ma_st[0]', 'mask_overlap[0]', 'mask_overlap_1[0]', 'mask_overlap_2[0]', 'mask_overlap_3[0]', 'mask_overlap_4[0]', 'mask_overlap_5[0]', 'mask_overlap_6[0]', 'mask_overlap_7[0]', 'mask_union', 'mask_union_1', 'mask_union_2', 'mask_union_3', 'mask_union_4', 'mask_union_5', 'mask_union_6', 'mask_union_7', 'mem_incoming_uop[0].br_mask', 'mem_incoming_uop[0].fp_val', 'mem_incoming_uop[0].ldq_idx', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_ldq_wakeup_e_out', 'mem_ldq_wakeup_e_out.bits.uop.br_mask', 'mem_ldq_wakeup_e_out.valid', 'mem_tlb_uncacheable[0]', 'mem_xcpt_valids[0]', 'nack_mask', 'pf_ld[0]', 'pf_st[0]', 'resp.uop.ldq_idx', 'resp.uop.uses_ldq', 'resp.uop.uses_stq', 'retry_queue.io.deq.bits.uop.br_mask', 'retry_queue.io.deq.bits.uop.stq_idx', 's_uop_1.lrs2_rtype', 's_uop_1.prs2', 's_uop_2.lrs2_rtype', 's_uop_2.prs2', 's_uop_3.lrs2_rtype', 's_uop_3.prs2', 's_uop_4.lrs2_rtype', 's_uop_4.prs2', 's_uop_5.lrs2_rtype', 's_uop_5.prs2', 's_uop_6.lrs2_rtype', 's_uop_6.prs2', 's_uop_7.lrs2_rtype', 's_uop_7.prs2', 's_uop_8.lrs2_rtype', 's_uop_8.prs2', 'send_fresp', 'send_iresp', 'stq_addr[*].valid', 'stq_addr_is_virtual[*]', 'stq_almost_full', 'stq_almost_full_age1_age_1', 'stq_almost_full_age1_age_2', 'stq_almost_full_age1_overflow_1', 'stq_almost_full_age1_overflow_2', 'stq_almost_full_age2_age', 'stq_almost_full_age2_age_1', 'stq_almost_full_age2_overflow', 'stq_almost_full_age2_overflow_1', 'stq_committed[0]', 'stq_committed[1]', 'stq_committed[2]', 'stq_committed[3]', 'stq_committed[4]', 'stq_committed[5]', 'stq_committed[6]', 'stq_committed[7]', 'stq_enq_retry_idx', 'stq_enq_retry_idx_head_base', 'stq_enq_retry_idx_head_overflow', 'stq_execute_queue.io.deq.bits.uop.stq_idx', 'stq_idx', 'stq_incoming_idx[0]', 'stq_succeeded[*]', 'stq_uop[0].br_mask', 'stq_uop[1].br_mask', 'stq_uop[2].br_mask', 'stq_uop[3].br_mask', 'stq_uop[4].br_mask', 'stq_uop[5].br_mask', 'stq_uop[6].br_mask', 'stq_uop[7].br_mask', 'stq_valid[*]', 'stq_valid[0]', 'stq_valid[1]', 'stq_valid[2]', 'stq_valid[3]', 'stq_valid[4]', 'stq_valid[5]', 'stq_valid[6]', 'stq_valid[7]', 'uop.dst_rtype', 'w1', 'w1.valid', 'wakeupArbs_0.io.in[1].bits.uop.br_mask', 'wakeupArbs_0.io.in[1].ready', 'wakeupArbs_0.io.in[1].valid', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e[0].uop.dst_rtype', 'wb_ldst_forward_ldq_idx[0]', 'wb_ldst_forward_valid[0]', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1', 'will_fire_hella_incoming[0]', 'will_fire_hella_wakeup[0]', 'will_fire_load_agen[0]', 'will_fire_load_agen_exec[0]', 'will_fire_load_retry[0]', 'will_fire_load_wakeup[0]', 'will_fire_release', 'will_fire_release[0]', 'will_fire_release_0_will_fire', 'will_fire_store_agen[0]', 'will_fire_store_retry[0]', 'write_mask', 'write_mask_1', 'write_mask_2', 'write_mask_3', 'write_mask_4', 'write_mask_5', 'write_mask_6', 'write_mask_7']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[222] FIRRTL:366594 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:394:29 KIND:node :: node _T_27 = and(dis_uops[0].valid, dis_uops[0].bits.uses_ldq)
[223] FIRRTL:366595 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:394:59 KIND:when :: when _T_27 :
[241] FIRRTL:366613 SRC:<no-source-locator> KIND:node :: node _T_32 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[242] FIRRTL:366614 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:400:42 KIND:connect :: connect ldq_will_succeed[_T_32], UInt<1>(0h0)
[251] FIRRTL:366623 SRC:<no-source-locator> KIND:node :: node _T_37 = bits(dis_uops[0].bits.stq_idx, 2, 0)
[252] FIRRTL:366624 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _stq_valid_T = and(io.core.brupdate.b1.mispredict_mask, dis_uops[0].bits.br_mask)
[253] FIRRTL:366625 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _stq_valid_T_1 = neq(_stq_valid_T, UInt<1>(0h0))
[254] FIRRTL:366626 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _stq_valid_T_2 = or(_stq_valid_T_1, io.core.exception)
[255] FIRRTL:366627 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:407:46 KIND:node :: node _stq_valid_T_3 = eq(_stq_valid_T_2, UInt<1>(0h0))
[256] FIRRTL:366628 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:407:43 KIND:connect :: connect stq_valid[_T_37], _stq_valid_T_3
[264] FIRRTL:366636 SRC:<no-source-locator> KIND:node :: node _T_39 = bits(dis_uops[0].bits.stq_idx, 2, 0)
[265] FIRRTL:366637 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:409:43 KIND:connect :: connect stq_addr[_T_39].valid, UInt<1>(0h0)
[272] FIRRTL:366644 SRC:<no-source-locator> KIND:node :: node _T_43 = bits(dis_uops[0].bits.stq_idx, 2, 0)
[273] FIRRTL:366645 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:413:43 KIND:connect :: connect stq_succeeded[_T_43], UInt<1>(0h0)
[350] FIRRTL:366722 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2176:14 KIND:node :: node _stq_tail_plus_T_1 = tail(_stq_tail_plus_T, 1)
[351] FIRRTL:366723 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2176:20 KIND:node :: node stq_tail_plus = bits(_stq_tail_plus_T_1, 3, 0)
[352] FIRRTL:366724 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node stq_almost_full_age1_overflow = bits(stq_tail_plus, 3, 3)
[354] FIRRTL:366726 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node stq_almost_full_age1_age = bits(stq_tail_plus, 2, 0)
[356] FIRRTL:366728 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _stq_almost_full_T = eq(stq_almost_full_age1_overflow, stq_almost_full_age2_overflow)
[357] FIRRTL:366729 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _stq_almost_full_T_1 = gt(stq_almost_full_age1_age, stq_almost_full_age2_age)
[358] FIRRTL:366730 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _stq_almost_full_T_2 = neq(stq_almost_full_age1_overflow, stq_almost_full_age2_overflow)
[359] FIRRTL:366731 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _stq_almost_full_T_3 = lt(stq_almost_full_age1_age, stq_almost_full_age2_age)
[360] FIRRTL:366732 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_4 = mux(_stq_almost_full_T, _stq_almost_full_T_1, UInt<1>(0h0))
[361] FIRRTL:366733 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_5 = mux(_stq_almost_full_T_2, _stq_almost_full_T_3, UInt<1>(0h0))
[362] FIRRTL:366734 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_6 = or(_stq_almost_full_T_4, _stq_almost_full_T_5)
[364] FIRRTL:366736 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _stq_almost_full_WIRE, _stq_almost_full_T_6
[369] FIRRTL:366741 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _stq_almost_full_T_7 = eq(stq_almost_full_age1_overflow_1, stq_almost_full_age2_overflow_1)
[370] FIRRTL:366742 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _stq_almost_full_T_8 = gt(stq_almost_full_age1_age_1, stq_almost_full_age2_age_1)
[371] FIRRTL:366743 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _stq_almost_full_T_9 = neq(stq_almost_full_age1_overflow_1, stq_almost_full_age2_overflow_1)
[372] FIRRTL:366744 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _stq_almost_full_T_10 = lt(stq_almost_full_age1_age_1, stq_almost_full_age2_age_1)
[373] FIRRTL:366745 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_11 = mux(_stq_almost_full_T_7, _stq_almost_full_T_8, UInt<1>(0h0))
[374] FIRRTL:366746 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_12 = mux(_stq_almost_full_T_9, _stq_almost_full_T_10, UInt<1>(0h0))
[375] FIRRTL:366747 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_13 = or(_stq_almost_full_T_11, _stq_almost_full_T_12)
[377] FIRRTL:366749 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _stq_almost_full_WIRE_1, _stq_almost_full_T_13
[378] FIRRTL:366750 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:22 KIND:node :: node _stq_almost_full_T_14 = xor(_stq_almost_full_WIRE, _stq_almost_full_WIRE_1)
[380] FIRRTL:366752 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node stq_almost_full_age2_overflow_2 = bits(stq_tail_plus, 3, 3)
[382] FIRRTL:366754 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node stq_almost_full_age2_age_2 = bits(stq_tail_plus, 2, 0)
[383] FIRRTL:366755 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _stq_almost_full_T_15 = eq(stq_almost_full_age1_overflow_2, stq_almost_full_age2_overflow_2)
[384] FIRRTL:366756 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _stq_almost_full_T_16 = gt(stq_almost_full_age1_age_2, stq_almost_full_age2_age_2)
[385] FIRRTL:366757 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _stq_almost_full_T_17 = neq(stq_almost_full_age1_overflow_2, stq_almost_full_age2_overflow_2)
[386] FIRRTL:366758 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _stq_almost_full_T_18 = lt(stq_almost_full_age1_age_2, stq_almost_full_age2_age_2)
[387] FIRRTL:366759 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_19 = mux(_stq_almost_full_T_15, _stq_almost_full_T_16, UInt<1>(0h0))
[388] FIRRTL:366760 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_20 = mux(_stq_almost_full_T_17, _stq_almost_full_T_18, UInt<1>(0h0))
[389] FIRRTL:366761 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _stq_almost_full_T_21 = or(_stq_almost_full_T_19, _stq_almost_full_T_20)
[391] FIRRTL:366763 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _stq_almost_full_WIRE_2, _stq_almost_full_T_21
[392] FIRRTL:366764 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:43 KIND:node :: node _stq_almost_full_T_22 = xor(_stq_almost_full_T_14, _stq_almost_full_WIRE_2)
[394] FIRRTL:366766 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2145:9 KIND:connect :: connect stq_almost_full, _stq_almost_full_T_22
[433] FIRRTL:366805 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect stq_incoming_idx[0], io.core.agen[0].bits.uop.stq_idx
[606] FIRRTL:366978 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_1 = bits(ldq_enq_retry_idx, 2, 0)
[607] FIRRTL:366979 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_2 = neq(UInt<1>(0h0), _ldq_enq_retry_idx_T_1)
[608] FIRRTL:366980 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_3 = and(_ldq_enq_retry_idx_T, _ldq_enq_retry_idx_T_2)
[610] FIRRTL:366982 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_5 = bits(ldq_enq_retry_idx, 2, 0)
[611] FIRRTL:366983 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_6 = neq(UInt<1>(0h1), _ldq_enq_retry_idx_T_5)
[612] FIRRTL:366984 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_7 = and(_ldq_enq_retry_idx_T_4, _ldq_enq_retry_idx_T_6)
[614] FIRRTL:366986 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_9 = bits(ldq_enq_retry_idx, 2, 0)
[615] FIRRTL:366987 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_10 = neq(UInt<2>(0h2), _ldq_enq_retry_idx_T_9)
[616] FIRRTL:366988 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_11 = and(_ldq_enq_retry_idx_T_8, _ldq_enq_retry_idx_T_10)
[618] FIRRTL:366990 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_13 = bits(ldq_enq_retry_idx, 2, 0)
[619] FIRRTL:366991 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_14 = neq(UInt<2>(0h3), _ldq_enq_retry_idx_T_13)
[620] FIRRTL:366992 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_15 = and(_ldq_enq_retry_idx_T_12, _ldq_enq_retry_idx_T_14)
[622] FIRRTL:366994 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_17 = bits(ldq_enq_retry_idx, 2, 0)
[623] FIRRTL:366995 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_18 = neq(UInt<3>(0h4), _ldq_enq_retry_idx_T_17)
[624] FIRRTL:366996 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_19 = and(_ldq_enq_retry_idx_T_16, _ldq_enq_retry_idx_T_18)
[626] FIRRTL:366998 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_21 = bits(ldq_enq_retry_idx, 2, 0)
[627] FIRRTL:366999 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_22 = neq(UInt<3>(0h5), _ldq_enq_retry_idx_T_21)
[628] FIRRTL:367000 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_23 = and(_ldq_enq_retry_idx_T_20, _ldq_enq_retry_idx_T_22)
[630] FIRRTL:367002 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_25 = bits(ldq_enq_retry_idx, 2, 0)
[631] FIRRTL:367003 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_26 = neq(UInt<3>(0h6), _ldq_enq_retry_idx_T_25)
[632] FIRRTL:367004 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_27 = and(_ldq_enq_retry_idx_T_24, _ldq_enq_retry_idx_T_26)
[634] FIRRTL:367006 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _ldq_enq_retry_idx_T_29 = bits(ldq_enq_retry_idx, 2, 0)
[635] FIRRTL:367007 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:57 KIND:node :: node _ldq_enq_retry_idx_T_30 = neq(UInt<3>(0h7), _ldq_enq_retry_idx_T_29)
[636] FIRRTL:367008 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:509:49 KIND:node :: node _ldq_enq_retry_idx_T_31 = and(_ldq_enq_retry_idx_T_28, _ldq_enq_retry_idx_T_30)
[639] FIRRTL:367011 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T = geq(UInt<1>(0h0), ldq_enq_retry_idx_head_base)
[640] FIRRTL:367012 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_0 = and(_ldq_enq_retry_idx_T_3, _ldq_enq_retry_idx_base_temp_vec_T)
[641] FIRRTL:367013 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_1 = geq(UInt<1>(0h1), ldq_enq_retry_idx_head_base)
[642] FIRRTL:367014 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_1 = and(_ldq_enq_retry_idx_T_7, _ldq_enq_retry_idx_base_temp_vec_T_1)
[643] FIRRTL:367015 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_2 = geq(UInt<2>(0h2), ldq_enq_retry_idx_head_base)
[644] FIRRTL:367016 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_2 = and(_ldq_enq_retry_idx_T_11, _ldq_enq_retry_idx_base_temp_vec_T_2)
[645] FIRRTL:367017 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_3 = geq(UInt<2>(0h3), ldq_enq_retry_idx_head_base)
[646] FIRRTL:367018 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_3 = and(_ldq_enq_retry_idx_T_15, _ldq_enq_retry_idx_base_temp_vec_T_3)
[647] FIRRTL:367019 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_4 = geq(UInt<3>(0h4), ldq_enq_retry_idx_head_base)
[648] FIRRTL:367020 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_4 = and(_ldq_enq_retry_idx_T_19, _ldq_enq_retry_idx_base_temp_vec_T_4)
[649] FIRRTL:367021 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_5 = geq(UInt<3>(0h5), ldq_enq_retry_idx_head_base)
[650] FIRRTL:367022 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_5 = and(_ldq_enq_retry_idx_T_23, _ldq_enq_retry_idx_base_temp_vec_T_5)
[651] FIRRTL:367023 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_6 = geq(UInt<3>(0h6), ldq_enq_retry_idx_head_base)
[652] FIRRTL:367024 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_6 = and(_ldq_enq_retry_idx_T_27, _ldq_enq_retry_idx_base_temp_vec_T_6)
[653] FIRRTL:367025 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_enq_retry_idx_base_temp_vec_T_7 = geq(UInt<3>(0h7), ldq_enq_retry_idx_head_base)
[654] FIRRTL:367026 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_enq_retry_idx_base_temp_vec_7 = and(_ldq_enq_retry_idx_T_31, _ldq_enq_retry_idx_base_temp_vec_T_7)
[655] FIRRTL:367027 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T = mux(_ldq_enq_retry_idx_T_27, UInt<4>(0he), UInt<4>(0hf))
[656] FIRRTL:367028 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_1 = mux(_ldq_enq_retry_idx_T_23, UInt<4>(0hd), _ldq_enq_retry_idx_base_idx_T)
[657] FIRRTL:367029 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_2 = mux(_ldq_enq_retry_idx_T_19, UInt<4>(0hc), _ldq_enq_retry_idx_base_idx_T_1)
[658] FIRRTL:367030 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_3 = mux(_ldq_enq_retry_idx_T_15, UInt<4>(0hb), _ldq_enq_retry_idx_base_idx_T_2)
[659] FIRRTL:367031 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_4 = mux(_ldq_enq_retry_idx_T_11, UInt<4>(0ha), _ldq_enq_retry_idx_base_idx_T_3)
[660] FIRRTL:367032 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_5 = mux(_ldq_enq_retry_idx_T_7, UInt<4>(0h9), _ldq_enq_retry_idx_base_idx_T_4)
[661] FIRRTL:367033 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_6 = mux(_ldq_enq_retry_idx_T_3, UInt<4>(0h8), _ldq_enq_retry_idx_base_idx_T_5)
[662] FIRRTL:367034 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_7 = mux(ldq_enq_retry_idx_base_temp_vec_7, UInt<3>(0h7), _ldq_enq_retry_idx_base_idx_T_6)
[663] FIRRTL:367035 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_8 = mux(ldq_enq_retry_idx_base_temp_vec_6, UInt<3>(0h6), _ldq_enq_retry_idx_base_idx_T_7)
[664] FIRRTL:367036 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_9 = mux(ldq_enq_retry_idx_base_temp_vec_5, UInt<3>(0h5), _ldq_enq_retry_idx_base_idx_T_8)
[665] FIRRTL:367037 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_10 = mux(ldq_enq_retry_idx_base_temp_vec_4, UInt<3>(0h4), _ldq_enq_retry_idx_base_idx_T_9)
[666] FIRRTL:367038 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_11 = mux(ldq_enq_retry_idx_base_temp_vec_3, UInt<2>(0h3), _ldq_enq_retry_idx_base_idx_T_10)
[667] FIRRTL:367039 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_12 = mux(ldq_enq_retry_idx_base_temp_vec_2, UInt<2>(0h2), _ldq_enq_retry_idx_base_idx_T_11)
[668] FIRRTL:367040 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_enq_retry_idx_base_idx_T_13 = mux(ldq_enq_retry_idx_base_temp_vec_1, UInt<1>(0h1), _ldq_enq_retry_idx_base_idx_T_12)
[669] FIRRTL:367041 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node ldq_enq_retry_idx_base_idx = mux(ldq_enq_retry_idx_base_temp_vec_0, UInt<1>(0h0), _ldq_enq_retry_idx_base_idx_T_13)
[670] FIRRTL:367042 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node ldq_enq_retry_idx_base = bits(ldq_enq_retry_idx_base_idx, 2, 0)
[671] FIRRTL:367043 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:29 KIND:node :: node _ldq_enq_retry_idx_overflow_T = geq(ldq_enq_retry_idx_base, ldq_enq_retry_idx_head_base)
[672] FIRRTL:367044 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:58 KIND:node :: node _ldq_enq_retry_idx_overflow_T_1 = not(ldq_enq_retry_idx_head_overflow)
[673] FIRRTL:367045 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:23 KIND:node :: node ldq_enq_retry_idx_overflow = mux(_ldq_enq_retry_idx_overflow_T, ldq_enq_retry_idx_head_overflow, _ldq_enq_retry_idx_overflow_T_1)
[674] FIRRTL:367046 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1999:8 KIND:node :: node _ldq_enq_retry_idx_T_32 = cat(ldq_enq_retry_idx_overflow, ldq_enq_retry_idx_base)
[675] FIRRTL:367047 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:508:21 KIND:connect :: connect ldq_enq_retry_idx, _ldq_enq_retry_idx_T_32
[708] FIRRTL:367080 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T = and(stq_addr[0].valid, stq_addr_is_virtual[0])
[709] FIRRTL:367081 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_1 = bits(stq_enq_retry_idx, 2, 0)
[710] FIRRTL:367082 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_2 = neq(UInt<1>(0h0), _stq_enq_retry_idx_T_1)
[711] FIRRTL:367083 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_3 = and(_stq_enq_retry_idx_T, _stq_enq_retry_idx_T_2)
[712] FIRRTL:367084 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_4 = and(stq_addr[1].valid, stq_addr_is_virtual[1])
[713] FIRRTL:367085 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_5 = bits(stq_enq_retry_idx, 2, 0)
[714] FIRRTL:367086 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_6 = neq(UInt<1>(0h1), _stq_enq_retry_idx_T_5)
[715] FIRRTL:367087 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_7 = and(_stq_enq_retry_idx_T_4, _stq_enq_retry_idx_T_6)
[716] FIRRTL:367088 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_8 = and(stq_addr[2].valid, stq_addr_is_virtual[2])
[717] FIRRTL:367089 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_9 = bits(stq_enq_retry_idx, 2, 0)
[718] FIRRTL:367090 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_10 = neq(UInt<2>(0h2), _stq_enq_retry_idx_T_9)
[719] FIRRTL:367091 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_11 = and(_stq_enq_retry_idx_T_8, _stq_enq_retry_idx_T_10)
[720] FIRRTL:367092 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_12 = and(stq_addr[3].valid, stq_addr_is_virtual[3])
[721] FIRRTL:367093 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_13 = bits(stq_enq_retry_idx, 2, 0)
[722] FIRRTL:367094 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_14 = neq(UInt<2>(0h3), _stq_enq_retry_idx_T_13)
[723] FIRRTL:367095 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_15 = and(_stq_enq_retry_idx_T_12, _stq_enq_retry_idx_T_14)
[724] FIRRTL:367096 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_16 = and(stq_addr[4].valid, stq_addr_is_virtual[4])
[725] FIRRTL:367097 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_17 = bits(stq_enq_retry_idx, 2, 0)
[726] FIRRTL:367098 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_18 = neq(UInt<3>(0h4), _stq_enq_retry_idx_T_17)
[727] FIRRTL:367099 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_19 = and(_stq_enq_retry_idx_T_16, _stq_enq_retry_idx_T_18)
[728] FIRRTL:367100 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_20 = and(stq_addr[5].valid, stq_addr_is_virtual[5])
[729] FIRRTL:367101 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_21 = bits(stq_enq_retry_idx, 2, 0)
[730] FIRRTL:367102 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_22 = neq(UInt<3>(0h5), _stq_enq_retry_idx_T_21)
[731] FIRRTL:367103 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_23 = and(_stq_enq_retry_idx_T_20, _stq_enq_retry_idx_T_22)
[732] FIRRTL:367104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_24 = and(stq_addr[6].valid, stq_addr_is_virtual[6])
[733] FIRRTL:367105 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_25 = bits(stq_enq_retry_idx, 2, 0)
[734] FIRRTL:367106 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_26 = neq(UInt<3>(0h6), _stq_enq_retry_idx_T_25)
[735] FIRRTL:367107 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_27 = and(_stq_enq_retry_idx_T_24, _stq_enq_retry_idx_T_26)
[736] FIRRTL:367108 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:23 KIND:node :: node _stq_enq_retry_idx_T_28 = and(stq_addr[7].valid, stq_addr_is_virtual[7])
[737] FIRRTL:367109 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _stq_enq_retry_idx_T_29 = bits(stq_enq_retry_idx, 2, 0)
[738] FIRRTL:367110 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:57 KIND:node :: node _stq_enq_retry_idx_T_30 = neq(UInt<3>(0h7), _stq_enq_retry_idx_T_29)
[739] FIRRTL:367111 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:515:49 KIND:node :: node _stq_enq_retry_idx_T_31 = and(_stq_enq_retry_idx_T_28, _stq_enq_retry_idx_T_30)
[742] FIRRTL:367114 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T = geq(UInt<1>(0h0), stq_enq_retry_idx_head_base)
[743] FIRRTL:367115 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_0 = and(_stq_enq_retry_idx_T_3, _stq_enq_retry_idx_base_temp_vec_T)
[744] FIRRTL:367116 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_1 = geq(UInt<1>(0h1), stq_enq_retry_idx_head_base)
[745] FIRRTL:367117 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_1 = and(_stq_enq_retry_idx_T_7, _stq_enq_retry_idx_base_temp_vec_T_1)
[746] FIRRTL:367118 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_2 = geq(UInt<2>(0h2), stq_enq_retry_idx_head_base)
[747] FIRRTL:367119 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_2 = and(_stq_enq_retry_idx_T_11, _stq_enq_retry_idx_base_temp_vec_T_2)
[748] FIRRTL:367120 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_3 = geq(UInt<2>(0h3), stq_enq_retry_idx_head_base)
[749] FIRRTL:367121 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_3 = and(_stq_enq_retry_idx_T_15, _stq_enq_retry_idx_base_temp_vec_T_3)
[750] FIRRTL:367122 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_4 = geq(UInt<3>(0h4), stq_enq_retry_idx_head_base)
[751] FIRRTL:367123 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_4 = and(_stq_enq_retry_idx_T_19, _stq_enq_retry_idx_base_temp_vec_T_4)
[752] FIRRTL:367124 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_5 = geq(UInt<3>(0h5), stq_enq_retry_idx_head_base)
[753] FIRRTL:367125 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_5 = and(_stq_enq_retry_idx_T_23, _stq_enq_retry_idx_base_temp_vec_T_5)
[754] FIRRTL:367126 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_6 = geq(UInt<3>(0h6), stq_enq_retry_idx_head_base)
[755] FIRRTL:367127 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_6 = and(_stq_enq_retry_idx_T_27, _stq_enq_retry_idx_base_temp_vec_T_6)
[756] FIRRTL:367128 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _stq_enq_retry_idx_base_temp_vec_T_7 = geq(UInt<3>(0h7), stq_enq_retry_idx_head_base)
[757] FIRRTL:367129 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node stq_enq_retry_idx_base_temp_vec_7 = and(_stq_enq_retry_idx_T_31, _stq_enq_retry_idx_base_temp_vec_T_7)
[758] FIRRTL:367130 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T = mux(_stq_enq_retry_idx_T_27, UInt<4>(0he), UInt<4>(0hf))
[759] FIRRTL:367131 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_1 = mux(_stq_enq_retry_idx_T_23, UInt<4>(0hd), _stq_enq_retry_idx_base_idx_T)
[760] FIRRTL:367132 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_2 = mux(_stq_enq_retry_idx_T_19, UInt<4>(0hc), _stq_enq_retry_idx_base_idx_T_1)
[761] FIRRTL:367133 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_3 = mux(_stq_enq_retry_idx_T_15, UInt<4>(0hb), _stq_enq_retry_idx_base_idx_T_2)
[762] FIRRTL:367134 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_4 = mux(_stq_enq_retry_idx_T_11, UInt<4>(0ha), _stq_enq_retry_idx_base_idx_T_3)
[763] FIRRTL:367135 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_5 = mux(_stq_enq_retry_idx_T_7, UInt<4>(0h9), _stq_enq_retry_idx_base_idx_T_4)
[764] FIRRTL:367136 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_6 = mux(_stq_enq_retry_idx_T_3, UInt<4>(0h8), _stq_enq_retry_idx_base_idx_T_5)
[765] FIRRTL:367137 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_7 = mux(stq_enq_retry_idx_base_temp_vec_7, UInt<3>(0h7), _stq_enq_retry_idx_base_idx_T_6)
[766] FIRRTL:367138 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_8 = mux(stq_enq_retry_idx_base_temp_vec_6, UInt<3>(0h6), _stq_enq_retry_idx_base_idx_T_7)
[767] FIRRTL:367139 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_9 = mux(stq_enq_retry_idx_base_temp_vec_5, UInt<3>(0h5), _stq_enq_retry_idx_base_idx_T_8)
[768] FIRRTL:367140 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_10 = mux(stq_enq_retry_idx_base_temp_vec_4, UInt<3>(0h4), _stq_enq_retry_idx_base_idx_T_9)
[769] FIRRTL:367141 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_11 = mux(stq_enq_retry_idx_base_temp_vec_3, UInt<2>(0h3), _stq_enq_retry_idx_base_idx_T_10)
[770] FIRRTL:367142 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_12 = mux(stq_enq_retry_idx_base_temp_vec_2, UInt<2>(0h2), _stq_enq_retry_idx_base_idx_T_11)
[771] FIRRTL:367143 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _stq_enq_retry_idx_base_idx_T_13 = mux(stq_enq_retry_idx_base_temp_vec_1, UInt<1>(0h1), _stq_enq_retry_idx_base_idx_T_12)
[772] FIRRTL:367144 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node stq_enq_retry_idx_base_idx = mux(stq_enq_retry_idx_base_temp_vec_0, UInt<1>(0h0), _stq_enq_retry_idx_base_idx_T_13)
[773] FIRRTL:367145 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node stq_enq_retry_idx_base = bits(stq_enq_retry_idx_base_idx, 2, 0)
[774] FIRRTL:367146 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:29 KIND:node :: node _stq_enq_retry_idx_overflow_T = geq(stq_enq_retry_idx_base, stq_enq_retry_idx_head_base)
[775] FIRRTL:367147 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:58 KIND:node :: node _stq_enq_retry_idx_overflow_T_1 = not(stq_enq_retry_idx_head_overflow)
[776] FIRRTL:367148 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:23 KIND:node :: node stq_enq_retry_idx_overflow = mux(_stq_enq_retry_idx_overflow_T, stq_enq_retry_idx_head_overflow, _stq_enq_retry_idx_overflow_T_1)
[777] FIRRTL:367149 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1999:8 KIND:node :: node _stq_enq_retry_idx_T_32 = cat(stq_enq_retry_idx_overflow, stq_enq_retry_idx_base)
[778] FIRRTL:367150 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:514:21 KIND:connect :: connect stq_enq_retry_idx, _stq_enq_retry_idx_T_32
[1167] FIRRTL:367539 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:539:57 KIND:when :: when _T_72 :
[1168] FIRRTL:367540 SRC:<no-source-locator> KIND:node :: node _T_73 = bits(stq_enq_retry_idx, 2, 0)
[1169] FIRRTL:367541 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:540:39 KIND:connect :: connect stq_addr[_T_73].valid, UInt<1>(0h0)
[1576] FIRRTL:367948 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:673:36 KIND:connect :: connect will_fire_release[0], will_fire_release_0_will_fire
[2090] FIRRTL:368462 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:777:52 KIND:node :: node _ma_ld_T = and(dtlb.io.resp[0].ma.ld, exe_tlb_uop[0].uses_ldq)
[2092] FIRRTL:368464 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect ma_ld[0], _ma_ld_T
[2093] FIRRTL:368465 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:778:52 KIND:node :: node _ma_st_T = and(dtlb.io.resp[0].ma.st, exe_tlb_uop[0].uses_stq)
[2094] FIRRTL:368466 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:778:82 KIND:node :: node _ma_st_T_1 = eq(exe_tlb_uop[0].is_fence, UInt<1>(0h0))
[2095] FIRRTL:368467 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:778:79 KIND:node :: node _ma_st_T_2 = and(_ma_st_T, _ma_st_T_1)
[2097] FIRRTL:368469 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect ma_st[0], _ma_st_T_2
[2098] FIRRTL:368470 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:779:52 KIND:node :: node _pf_ld_T = and(dtlb.io.resp[0].pf.ld, exe_tlb_uop[0].uses_ldq)
[2100] FIRRTL:368472 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect pf_ld[0], _pf_ld_T
[2101] FIRRTL:368473 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:780:52 KIND:node :: node _pf_st_T = and(dtlb.io.resp[0].pf.st, exe_tlb_uop[0].uses_stq)
[2103] FIRRTL:368475 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect pf_st[0], _pf_st_T
[2104] FIRRTL:368476 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:781:52 KIND:node :: node _ae_ld_T = and(dtlb.io.resp[0].ae.ld, exe_tlb_uop[0].uses_ldq)
[2106] FIRRTL:368478 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect ae_ld[0], _ae_ld_T
[2107] FIRRTL:368479 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:782:52 KIND:node :: node _ae_st_T = and(dtlb.io.resp[0].ae.st, exe_tlb_uop[0].uses_stq)
[2109] FIRRTL:368481 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect ae_st[0], _ae_st_T
[2110] FIRRTL:368482 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:783:80 KIND:node :: node _dbg_bp_T = and(exe_tlb_uop[0].uses_ldq, bkptu_0.io.debug_ld)
[2111] FIRRTL:368483 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:784:80 KIND:node :: node _dbg_bp_T_1 = and(exe_tlb_uop[0].uses_stq, bkptu_0.io.debug_st)
[2112] FIRRTL:368484 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:784:107 KIND:node :: node _dbg_bp_T_2 = eq(exe_tlb_uop[0].is_fence, UInt<1>(0h0))
[2113] FIRRTL:368485 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:784:104 KIND:node :: node _dbg_bp_T_3 = and(_dbg_bp_T_1, _dbg_bp_T_2)
[2114] FIRRTL:368486 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:783:105 KIND:node :: node _dbg_bp_T_4 = or(_dbg_bp_T, _dbg_bp_T_3)
[2115] FIRRTL:368487 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:783:51 KIND:node :: node _dbg_bp_T_5 = and(bkptu_0.io.debug_st, _dbg_bp_T_4)
[2117] FIRRTL:368489 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dbg_bp[0], _dbg_bp_T_5
[2118] FIRRTL:368490 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:785:80 KIND:node :: node _bp_T = and(exe_tlb_uop[0].uses_ldq, bkptu_0.io.xcpt_ld)
[2119] FIRRTL:368491 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:786:80 KIND:node :: node _bp_T_1 = and(exe_tlb_uop[0].uses_stq, bkptu_0.io.xcpt_st)
[2120] FIRRTL:368492 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:786:106 KIND:node :: node _bp_T_2 = eq(exe_tlb_uop[0].is_fence, UInt<1>(0h0))
[2121] FIRRTL:368493 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:786:103 KIND:node :: node _bp_T_3 = and(_bp_T_1, _bp_T_2)
[2122] FIRRTL:368494 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:785:104 KIND:node :: node _bp_T_4 = or(_bp_T, _bp_T_3)
[2123] FIRRTL:368495 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:785:51 KIND:node :: node _bp_T_5 = and(bkptu_0.io.debug_st, _bp_T_4)
[2125] FIRRTL:368497 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect bp[0], _bp_T_5
[2126] FIRRTL:368498 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:32 KIND:node :: node _mem_xcpt_valids_T = or(pf_ld[0], pf_st[0])
[2127] FIRRTL:368499 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:44 KIND:node :: node _mem_xcpt_valids_T_1 = or(_mem_xcpt_valids_T, ae_ld[0])
[2128] FIRRTL:368500 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:56 KIND:node :: node _mem_xcpt_valids_T_2 = or(_mem_xcpt_valids_T_1, ae_st[0])
[2129] FIRRTL:368501 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:68 KIND:node :: node _mem_xcpt_valids_T_3 = or(_mem_xcpt_valids_T_2, ma_ld[0])
[2130] FIRRTL:368502 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:80 KIND:node :: node _mem_xcpt_valids_T_4 = or(_mem_xcpt_valids_T_3, ma_st[0])
[2131] FIRRTL:368503 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:92 KIND:node :: node _mem_xcpt_valids_T_5 = or(_mem_xcpt_valids_T_4, dbg_bp[0])
[2132] FIRRTL:368504 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:105 KIND:node :: node _mem_xcpt_valids_T_6 = or(_mem_xcpt_valids_T_5, bp[0])
[2133] FIRRTL:368505 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:791:39 KIND:node :: node _mem_xcpt_valids_T_7 = and(exe_tlb_valid[0], _mem_xcpt_valids_T_6)
[2134] FIRRTL:368506 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _mem_xcpt_valids_T_8 = and(io.core.brupdate.b1.mispredict_mask, exe_tlb_uop[0].br_mask)
[2135] FIRRTL:368507 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _mem_xcpt_valids_T_9 = neq(_mem_xcpt_valids_T_8, UInt<1>(0h0))
[2136] FIRRTL:368508 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _mem_xcpt_valids_T_10 = or(_mem_xcpt_valids_T_9, io.core.exception)
[2137] FIRRTL:368509 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:793:22 KIND:node :: node _mem_xcpt_valids_T_11 = eq(_mem_xcpt_valids_T_10, UInt<1>(0h0))
[2138] FIRRTL:368510 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:792:115 KIND:node :: node _mem_xcpt_valids_T_12 = and(_mem_xcpt_valids_T_7, _mem_xcpt_valids_T_11)
[2140] FIRRTL:368512 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _mem_xcpt_valids_WIRE[0], _mem_xcpt_valids_T_12
[2142] FIRRTL:368514 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:790:32 KIND:connect :: connect mem_xcpt_valids, _mem_xcpt_valids_WIRE
[2441] FIRRTL:368813 SRC:<no-source-locator> KIND:node :: node _T_147 = bits(stq_execute_queue.io.deq.bits.uop.stq_idx, 2, 0)
[2442] FIRRTL:368814 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:920:52 KIND:connect :: connect stq_succeeded[_T_147], UInt<1>(0h0)
[2498] FIRRTL:368870 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:943:19 KIND:connect :: connect hella_paddr, exe_tlb_paddr[0]
[2545] FIRRTL:368917 SRC:<no-source-locator> KIND:node :: node _T_167 = bits(ldq_idx, 2, 0)
[2547] FIRRTL:368919 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _ldq_ld_byte_mask_mask_T = eq(exe_tlb_uop[0].mem_size, UInt<1>(0h0))
[2548] FIRRTL:368920 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _ldq_ld_byte_mask_mask_T_1 = bits(exe_tlb_vaddr[0], 2, 0)
[2549] FIRRTL:368921 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _ldq_ld_byte_mask_mask_T_2 = dshl(UInt<8>(0h1), _ldq_ld_byte_mask_mask_T_1)
[2550] FIRRTL:368922 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _ldq_ld_byte_mask_mask_T_3 = eq(exe_tlb_uop[0].mem_size, UInt<1>(0h1))
[2551] FIRRTL:368923 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _ldq_ld_byte_mask_mask_T_4 = bits(exe_tlb_vaddr[0], 2, 1)
[2552] FIRRTL:368924 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _ldq_ld_byte_mask_mask_T_5 = dshl(_ldq_ld_byte_mask_mask_T_4, UInt<1>(0h1))
[2553] FIRRTL:368925 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _ldq_ld_byte_mask_mask_T_6 = dshl(UInt<8>(0h3), _ldq_ld_byte_mask_mask_T_5)
[2554] FIRRTL:368926 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _ldq_ld_byte_mask_mask_T_7 = eq(exe_tlb_uop[0].mem_size, UInt<2>(0h2))
[2555] FIRRTL:368927 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _ldq_ld_byte_mask_mask_T_8 = bits(exe_tlb_vaddr[0], 2, 2)
[2556] FIRRTL:368928 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _ldq_ld_byte_mask_mask_T_9 = mux(_ldq_ld_byte_mask_mask_T_8, UInt<8>(0hf0), UInt<8>(0hf))
[2557] FIRRTL:368929 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _ldq_ld_byte_mask_mask_T_10 = eq(exe_tlb_uop[0].mem_size, UInt<2>(0h3))
[2558] FIRRTL:368930 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _ldq_ld_byte_mask_mask_T_11 = mux(_ldq_ld_byte_mask_mask_T_10, UInt<8>(0hff), UInt<8>(0hff))
[2559] FIRRTL:368931 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _ldq_ld_byte_mask_mask_T_12 = mux(_ldq_ld_byte_mask_mask_T_7, _ldq_ld_byte_mask_mask_T_9, _ldq_ld_byte_mask_mask_T_11)
[2560] FIRRTL:368932 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _ldq_ld_byte_mask_mask_T_13 = mux(_ldq_ld_byte_mask_mask_T_3, _ldq_ld_byte_mask_mask_T_6, _ldq_ld_byte_mask_mask_T_12)
[2561] FIRRTL:368933 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _ldq_ld_byte_mask_mask_T_14 = mux(_ldq_ld_byte_mask_mask_T, _ldq_ld_byte_mask_mask_T_2, _ldq_ld_byte_mask_mask_T_13)
[2562] FIRRTL:368934 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect ldq_ld_byte_mask_mask, _ldq_ld_byte_mask_mask_T_14
[2563] FIRRTL:368935 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:967:47 KIND:connect :: connect ldq_ld_byte_mask[_T_167], ldq_ld_byte_mask_mask
[2581] FIRRTL:368953 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:976:35 KIND:node :: node _T_176 = or(will_fire_store_agen[0], will_fire_store_retry[0])
[2582] FIRRTL:368954 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:977:5 KIND:when :: when _T_176 :
[2583] FIRRTL:368955 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:978:24 KIND:node :: node stq_idx = mux(will_fire_store_agen[0], stq_incoming_idx[0], retry_queue.io.deq.bits.uop.stq_idx)
[2584] FIRRTL:368956 SRC:<no-source-locator> KIND:node :: node _T_177 = bits(stq_idx, 2, 0)
[2585] FIRRTL:368957 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:981:46 KIND:node :: node _stq_addr_valid_T = eq(exe_agen_killed[0], UInt<1>(0h0))
[2586] FIRRTL:368958 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:981:66 KIND:node :: node _stq_addr_valid_T_1 = or(_stq_addr_valid_T, will_fire_store_retry[0])
[2587] FIRRTL:368959 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:981:98 KIND:node :: node _stq_addr_valid_T_2 = eq(pf_st[0], UInt<1>(0h0))
[2588] FIRRTL:368960 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:981:95 KIND:node :: node _stq_addr_valid_T_3 = and(_stq_addr_valid_T_1, _stq_addr_valid_T_2)
[2589] FIRRTL:368961 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:981:42 KIND:connect :: connect stq_addr[_T_177].valid, _stq_addr_valid_T_3
[2590] FIRRTL:368962 SRC:<no-source-locator> KIND:node :: node _T_178 = bits(stq_idx, 2, 0)
[2591] FIRRTL:368963 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:982:48 KIND:node :: node _stq_addr_bits_T = mux(exe_tlb_miss[0], exe_tlb_vaddr[0], exe_tlb_paddr[0])
[2592] FIRRTL:368964 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:982:42 KIND:connect :: connect stq_addr[_T_178].bits, _stq_addr_bits_T
[2595] FIRRTL:368967 SRC:<no-source-locator> KIND:node :: node _T_180 = bits(stq_idx, 2, 0)
[2596] FIRRTL:368968 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:984:42 KIND:connect :: connect stq_addr_is_virtual[_T_180], exe_tlb_miss[0]
[2895] FIRRTL:369267 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1036:83 KIND:node :: node _fired_load_agen_exec_T = eq(exe_agen_killed[0], UInt<1>(0h0))
[2896] FIRRTL:369268 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1036:80 KIND:node :: node _fired_load_agen_exec_T_1 = and(will_fire_load_agen_exec[0], _fired_load_agen_exec_T)
[2898] FIRRTL:369270 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1036:51 KIND:connect :: connect fired_load_agen_exec_REG, _fired_load_agen_exec_T_1
[2900] FIRRTL:369272 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_load_agen_exec[0], fired_load_agen_exec_REG
[2901] FIRRTL:369273 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1037:83 KIND:node :: node _fired_load_agen_T = eq(exe_agen_killed[0], UInt<1>(0h0))
[2902] FIRRTL:369274 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1037:80 KIND:node :: node _fired_load_agen_T_1 = and(will_fire_load_agen[0], _fired_load_agen_T)
[2904] FIRRTL:369276 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1037:51 KIND:connect :: connect fired_load_agen_REG, _fired_load_agen_T_1
[2906] FIRRTL:369278 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_load_agen[0], fired_load_agen_REG
[2907] FIRRTL:369279 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1038:83 KIND:node :: node _fired_store_agen_T = eq(exe_agen_killed[0], UInt<1>(0h0))
[2908] FIRRTL:369280 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1038:80 KIND:node :: node _fired_store_agen_T_1 = and(will_fire_store_agen[0], _fired_store_agen_T)
[2910] FIRRTL:369282 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1038:51 KIND:connect :: connect fired_store_agen_REG, _fired_store_agen_T_1
[2912] FIRRTL:369284 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_store_agen[0], fired_store_agen_REG
[2916] FIRRTL:369288 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1040:37 KIND:connect :: connect fired_release, will_fire_release
[2917] FIRRTL:369289 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _fired_load_retry_T = and(io.core.brupdate.b1.mispredict_mask, retry_queue.io.deq.bits.uop.br_mask)
[2918] FIRRTL:369290 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _fired_load_retry_T_1 = neq(_fired_load_retry_T, UInt<1>(0h0))
[2919] FIRRTL:369291 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _fired_load_retry_T_2 = or(_fired_load_retry_T_1, io.core.exception)
[2920] FIRRTL:369292 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1041:82 KIND:node :: node _fired_load_retry_T_3 = eq(_fired_load_retry_T_2, UInt<1>(0h0))
[2921] FIRRTL:369293 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1041:79 KIND:node :: node _fired_load_retry_T_4 = and(will_fire_load_retry[0], _fired_load_retry_T_3)
[2923] FIRRTL:369295 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1041:51 KIND:connect :: connect fired_load_retry_REG, _fired_load_retry_T_4
[2925] FIRRTL:369297 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_load_retry[0], fired_load_retry_REG
[2926] FIRRTL:369298 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _fired_store_retry_T = and(io.core.brupdate.b1.mispredict_mask, retry_queue.io.deq.bits.uop.br_mask)
[2927] FIRRTL:369299 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _fired_store_retry_T_1 = neq(_fired_store_retry_T, UInt<1>(0h0))
[2928] FIRRTL:369300 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _fired_store_retry_T_2 = or(_fired_store_retry_T_1, io.core.exception)
[2929] FIRRTL:369301 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1042:82 KIND:node :: node _fired_store_retry_T_3 = eq(_fired_store_retry_T_2, UInt<1>(0h0))
[2930] FIRRTL:369302 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1042:79 KIND:node :: node _fired_store_retry_T_4 = and(will_fire_store_retry[0], _fired_store_retry_T_3)
[2932] FIRRTL:369304 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1042:51 KIND:connect :: connect fired_store_retry_REG, _fired_store_retry_T_4
[2934] FIRRTL:369306 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_store_retry[0], fired_store_retry_REG
[2940] FIRRTL:369312 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _fired_load_wakeup_T = and(io.core.brupdate.b1.mispredict_mask, ldq_wakeup_e.bits.uop.br_mask)
[2941] FIRRTL:369313 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _fired_load_wakeup_T_1 = neq(_fired_load_wakeup_T, UInt<1>(0h0))
[2942] FIRRTL:369314 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _fired_load_wakeup_T_2 = or(_fired_load_wakeup_T_1, io.core.exception)
[2943] FIRRTL:369315 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1044:82 KIND:node :: node _fired_load_wakeup_T_3 = eq(_fired_load_wakeup_T_2, UInt<1>(0h0))
[2944] FIRRTL:369316 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1044:79 KIND:node :: node _fired_load_wakeup_T_4 = and(will_fire_load_wakeup[0], _fired_load_wakeup_T_3)
[2946] FIRRTL:369318 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1044:51 KIND:connect :: connect fired_load_wakeup_REG, _fired_load_wakeup_T_4
[2948] FIRRTL:369320 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect fired_load_wakeup[0], fired_load_wakeup_REG
[2993] FIRRTL:369365 SRC:generators/boom/src/main/scala/v4/util/util.scala:114:23 KIND:connect :: connect mem_ldq_wakeup_e_out, ldq_wakeup_e
[3004] FIRRTL:369376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1051:37 KIND:connect :: connect mem_ldq_wakeup_e, mem_ldq_wakeup_e_out
[3083] FIRRTL:369455 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1055:58 KIND:node :: node _mem_ldq_e_T = or(fired_load_agen[0], fired_load_agen_exec[0])
[3210] FIRRTL:369582 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1058:33 KIND:node :: node _mem_ldq_e_T_1 = mux(fired_load_wakeup[0], mem_ldq_wakeup_e, _mem_ldq_e_WIRE)
[3211] FIRRTL:369583 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1057:33 KIND:node :: node _mem_ldq_e_T_2 = mux(fired_load_retry[0], mem_ldq_retry_e, _mem_ldq_e_T_1)
[3212] FIRRTL:369584 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1055:33 KIND:node :: node _mem_ldq_e_T_3 = mux(_mem_ldq_e_T, mem_ldq_incoming_e[0], _mem_ldq_e_T_2)
[3214] FIRRTL:369586 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mem_ldq_e[0], _mem_ldq_e_T_3
[3344] FIRRTL:369716 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1065:41 KIND:connect :: connect mem_tlb_miss, exe_tlb_miss
[3348] FIRRTL:369720 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _mem_paddr_WIRE[0], dmem_req[0].bits.addr
[3350] FIRRTL:369722 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1067:41 KIND:connect :: connect mem_paddr, _mem_paddr_WIRE
[3465] FIRRTL:369837 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1117:57 KIND:node :: node _do_st_search_T = or(fired_store_agen[0], fired_store_retry[0])
[3466] FIRRTL:369838 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1117:85 KIND:node :: node _do_st_search_T_1 = eq(mem_tlb_miss[0], UInt<1>(0h0))
[3467] FIRRTL:369839 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1117:82 KIND:node :: node _do_st_search_T_2 = and(_do_st_search_T, _do_st_search_T_1)
[3469] FIRRTL:369841 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect do_st_search[0], _do_st_search_T_2
[3470] FIRRTL:369842 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1119:57 KIND:node :: node _do_ld_search_T = or(fired_load_agen[0], fired_load_agen_exec[0])
[3471] FIRRTL:369843 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1119:84 KIND:node :: node _do_ld_search_T_1 = or(_do_ld_search_T, fired_load_retry[0])
[3472] FIRRTL:369844 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1119:111 KIND:node :: node _do_ld_search_T_2 = eq(mem_tlb_miss[0], UInt<1>(0h0))
[3473] FIRRTL:369845 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1119:108 KIND:node :: node _do_ld_search_T_3 = and(_do_ld_search_T_1, _do_ld_search_T_2)
[3474] FIRRTL:369846 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1119:129 KIND:node :: node _do_ld_search_T_4 = or(_do_ld_search_T_3, fired_load_wakeup[0])
[3476] FIRRTL:369848 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect do_ld_search[0], _do_ld_search_T_4
[3479] FIRRTL:369851 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1128:58 KIND:node :: node _lcam_addr_T = or(fired_store_agen[0], fired_store_retry[0])
[3480] FIRRTL:369852 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1128:82 KIND:node :: node _lcam_addr_T_1 = or(_lcam_addr_T, fired_load_agen[0])
[3481] FIRRTL:369853 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1128:104 KIND:node :: node _lcam_addr_T_2 = or(_lcam_addr_T_1, fired_load_agen_exec[0])
[3483] FIRRTL:369855 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1129:45 KIND:connect :: connect lcam_addr_REG, exe_tlb_paddr[0]
[3486] FIRRTL:369858 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1130:41 KIND:node :: node _lcam_addr_T_3 = mux(fired_release[0], lcam_addr_REG_1, mem_paddr[0])
[3487] FIRRTL:369859 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1128:37 KIND:node :: node _lcam_addr_T_4 = mux(_lcam_addr_T_2, lcam_addr_REG, _lcam_addr_T_3)
[3489] FIRRTL:369861 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect lcam_addr[0], _lcam_addr_T_4
[3602] FIRRTL:369974 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1133:37 KIND:node :: node _lcam_uop_T = mux(do_ld_search[0], mem_ldq_e[0].bits.uop, _lcam_uop_WIRE)
[3603] FIRRTL:369975 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1132:37 KIND:node :: node _lcam_uop_T_1 = mux(do_st_search[0], mem_stq_e[0].bits.uop, _lcam_uop_T)
[3605] FIRRTL:369977 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect lcam_uop[0], _lcam_uop_T_1
[3607] FIRRTL:369979 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _lcam_mask_mask_T = eq(lcam_uop[0].mem_size, UInt<1>(0h0))
[3608] FIRRTL:369980 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _lcam_mask_mask_T_1 = bits(lcam_addr[0], 2, 0)
[3609] FIRRTL:369981 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _lcam_mask_mask_T_2 = dshl(UInt<8>(0h1), _lcam_mask_mask_T_1)
[3610] FIRRTL:369982 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _lcam_mask_mask_T_3 = eq(lcam_uop[0].mem_size, UInt<1>(0h1))
[3611] FIRRTL:369983 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _lcam_mask_mask_T_4 = bits(lcam_addr[0], 2, 1)
[3612] FIRRTL:369984 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _lcam_mask_mask_T_5 = dshl(_lcam_mask_mask_T_4, UInt<1>(0h1))
[3613] FIRRTL:369985 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _lcam_mask_mask_T_6 = dshl(UInt<8>(0h3), _lcam_mask_mask_T_5)
[3614] FIRRTL:369986 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _lcam_mask_mask_T_7 = eq(lcam_uop[0].mem_size, UInt<2>(0h2))
[3615] FIRRTL:369987 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _lcam_mask_mask_T_8 = bits(lcam_addr[0], 2, 2)
[3616] FIRRTL:369988 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _lcam_mask_mask_T_9 = mux(_lcam_mask_mask_T_8, UInt<8>(0hf0), UInt<8>(0hf))
[3617] FIRRTL:369989 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _lcam_mask_mask_T_10 = eq(lcam_uop[0].mem_size, UInt<2>(0h3))
[3618] FIRRTL:369990 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _lcam_mask_mask_T_11 = mux(_lcam_mask_mask_T_10, UInt<8>(0hff), UInt<8>(0hff))
[3619] FIRRTL:369991 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _lcam_mask_mask_T_12 = mux(_lcam_mask_mask_T_7, _lcam_mask_mask_T_9, _lcam_mask_mask_T_11)
[3620] FIRRTL:369992 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _lcam_mask_mask_T_13 = mux(_lcam_mask_mask_T_3, _lcam_mask_mask_T_6, _lcam_mask_mask_T_12)
[3621] FIRRTL:369993 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _lcam_mask_mask_T_14 = mux(_lcam_mask_mask_T, _lcam_mask_mask_T_2, _lcam_mask_mask_T_13)
[3622] FIRRTL:369994 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect lcam_mask_mask, _lcam_mask_mask_T_14
[3624] FIRRTL:369996 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect lcam_mask[0], lcam_mask_mask
[3626] FIRRTL:369998 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect lcam_next_stq_idx[0], mem_ldq_e[0].bits.next_stq_idx
[3629] FIRRTL:370001 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1139:51 KIND:node :: node _lcam_ldq_idx_T = or(fired_load_agen[0], fired_load_agen_exec[0])
[3634] FIRRTL:370006 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1142:26 KIND:node :: node _lcam_ldq_idx_T_1 = mux(fired_load_retry[0], lcam_ldq_idx_reg_1, UInt<4>(0h0))
[3635] FIRRTL:370007 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1141:26 KIND:node :: node _lcam_ldq_idx_T_2 = mux(fired_load_wakeup[0], lcam_ldq_idx_reg, _lcam_ldq_idx_T_1)
[3636] FIRRTL:370008 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1139:26 KIND:node :: node _lcam_ldq_idx_T_3 = mux(_lcam_ldq_idx_T, mem_incoming_uop[0].ldq_idx, _lcam_ldq_idx_T_2)
[3638] FIRRTL:370010 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect lcam_ldq_idx[0], _lcam_ldq_idx_T_3
[3646] FIRRTL:370018 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_0_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3648] FIRRTL:370020 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_0_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3650] FIRRTL:370022 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_0_T = eq(lcam_younger_load_mask_0_0_head_carry, lcam_younger_load_mask_0_0_tail_carry)
[3651] FIRRTL:370023 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_0_T_1 = geq(UInt<3>(0h0), lcam_younger_load_mask_0_0_real_head_idx)
[3652] FIRRTL:370024 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_0_T_2 = lt(UInt<3>(0h0), lcam_younger_load_mask_0_0_real_tail_idx)
[3653] FIRRTL:370025 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_0_T_3 = and(_lcam_younger_load_mask_0_0_T_1, _lcam_younger_load_mask_0_0_T_2)
[3654] FIRRTL:370026 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_0_T_4 = geq(UInt<3>(0h0), lcam_younger_load_mask_0_0_real_head_idx)
[3655] FIRRTL:370027 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_0_T_5 = lt(UInt<3>(0h0), lcam_younger_load_mask_0_0_real_tail_idx)
[3656] FIRRTL:370028 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_0_T_6 = or(_lcam_younger_load_mask_0_0_T_4, _lcam_younger_load_mask_0_0_T_5)
[3657] FIRRTL:370029 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_0_T_7 = mux(_lcam_younger_load_mask_0_0_T, _lcam_younger_load_mask_0_0_T_3, _lcam_younger_load_mask_0_0_T_6)
[3658] FIRRTL:370030 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_0_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3659] FIRRTL:370031 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_0_T_9 = neq(UInt<1>(0h0), _lcam_younger_load_mask_0_0_T_8)
[3660] FIRRTL:370032 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_0_T_10 = and(_lcam_younger_load_mask_0_0_T_7, _lcam_younger_load_mask_0_0_T_9)
[3661] FIRRTL:370033 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][0], _lcam_younger_load_mask_0_0_T_10
[3662] FIRRTL:370034 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_1_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3664] FIRRTL:370036 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_1_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3666] FIRRTL:370038 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_1_T = eq(lcam_younger_load_mask_0_1_head_carry, lcam_younger_load_mask_0_1_tail_carry)
[3667] FIRRTL:370039 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_1_T_1 = geq(UInt<3>(0h1), lcam_younger_load_mask_0_1_real_head_idx)
[3668] FIRRTL:370040 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_1_T_2 = lt(UInt<3>(0h1), lcam_younger_load_mask_0_1_real_tail_idx)
[3669] FIRRTL:370041 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_1_T_3 = and(_lcam_younger_load_mask_0_1_T_1, _lcam_younger_load_mask_0_1_T_2)
[3670] FIRRTL:370042 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_1_T_4 = geq(UInt<3>(0h1), lcam_younger_load_mask_0_1_real_head_idx)
[3671] FIRRTL:370043 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_1_T_5 = lt(UInt<3>(0h1), lcam_younger_load_mask_0_1_real_tail_idx)
[3672] FIRRTL:370044 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_1_T_6 = or(_lcam_younger_load_mask_0_1_T_4, _lcam_younger_load_mask_0_1_T_5)
[3673] FIRRTL:370045 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_1_T_7 = mux(_lcam_younger_load_mask_0_1_T, _lcam_younger_load_mask_0_1_T_3, _lcam_younger_load_mask_0_1_T_6)
[3674] FIRRTL:370046 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_1_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3675] FIRRTL:370047 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_1_T_9 = neq(UInt<1>(0h1), _lcam_younger_load_mask_0_1_T_8)
[3676] FIRRTL:370048 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_1_T_10 = and(_lcam_younger_load_mask_0_1_T_7, _lcam_younger_load_mask_0_1_T_9)
[3677] FIRRTL:370049 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][1], _lcam_younger_load_mask_0_1_T_10
[3678] FIRRTL:370050 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_2_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3680] FIRRTL:370052 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_2_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3682] FIRRTL:370054 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_2_T = eq(lcam_younger_load_mask_0_2_head_carry, lcam_younger_load_mask_0_2_tail_carry)
[3683] FIRRTL:370055 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_2_T_1 = geq(UInt<3>(0h2), lcam_younger_load_mask_0_2_real_head_idx)
[3684] FIRRTL:370056 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_2_T_2 = lt(UInt<3>(0h2), lcam_younger_load_mask_0_2_real_tail_idx)
[3685] FIRRTL:370057 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_2_T_3 = and(_lcam_younger_load_mask_0_2_T_1, _lcam_younger_load_mask_0_2_T_2)
[3686] FIRRTL:370058 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_2_T_4 = geq(UInt<3>(0h2), lcam_younger_load_mask_0_2_real_head_idx)
[3687] FIRRTL:370059 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_2_T_5 = lt(UInt<3>(0h2), lcam_younger_load_mask_0_2_real_tail_idx)
[3688] FIRRTL:370060 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_2_T_6 = or(_lcam_younger_load_mask_0_2_T_4, _lcam_younger_load_mask_0_2_T_5)
[3689] FIRRTL:370061 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_2_T_7 = mux(_lcam_younger_load_mask_0_2_T, _lcam_younger_load_mask_0_2_T_3, _lcam_younger_load_mask_0_2_T_6)
[3690] FIRRTL:370062 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_2_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3691] FIRRTL:370063 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_2_T_9 = neq(UInt<2>(0h2), _lcam_younger_load_mask_0_2_T_8)
[3692] FIRRTL:370064 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_2_T_10 = and(_lcam_younger_load_mask_0_2_T_7, _lcam_younger_load_mask_0_2_T_9)
[3693] FIRRTL:370065 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][2], _lcam_younger_load_mask_0_2_T_10
[3694] FIRRTL:370066 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_3_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3696] FIRRTL:370068 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_3_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3698] FIRRTL:370070 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_3_T = eq(lcam_younger_load_mask_0_3_head_carry, lcam_younger_load_mask_0_3_tail_carry)
[3699] FIRRTL:370071 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_3_T_1 = geq(UInt<3>(0h3), lcam_younger_load_mask_0_3_real_head_idx)
[3700] FIRRTL:370072 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_3_T_2 = lt(UInt<3>(0h3), lcam_younger_load_mask_0_3_real_tail_idx)
[3701] FIRRTL:370073 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_3_T_3 = and(_lcam_younger_load_mask_0_3_T_1, _lcam_younger_load_mask_0_3_T_2)
[3702] FIRRTL:370074 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_3_T_4 = geq(UInt<3>(0h3), lcam_younger_load_mask_0_3_real_head_idx)
[3703] FIRRTL:370075 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_3_T_5 = lt(UInt<3>(0h3), lcam_younger_load_mask_0_3_real_tail_idx)
[3704] FIRRTL:370076 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_3_T_6 = or(_lcam_younger_load_mask_0_3_T_4, _lcam_younger_load_mask_0_3_T_5)
[3705] FIRRTL:370077 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_3_T_7 = mux(_lcam_younger_load_mask_0_3_T, _lcam_younger_load_mask_0_3_T_3, _lcam_younger_load_mask_0_3_T_6)
[3706] FIRRTL:370078 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_3_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3707] FIRRTL:370079 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_3_T_9 = neq(UInt<2>(0h3), _lcam_younger_load_mask_0_3_T_8)
[3708] FIRRTL:370080 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_3_T_10 = and(_lcam_younger_load_mask_0_3_T_7, _lcam_younger_load_mask_0_3_T_9)
[3709] FIRRTL:370081 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][3], _lcam_younger_load_mask_0_3_T_10
[3710] FIRRTL:370082 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_4_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3712] FIRRTL:370084 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_4_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3714] FIRRTL:370086 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_4_T = eq(lcam_younger_load_mask_0_4_head_carry, lcam_younger_load_mask_0_4_tail_carry)
[3715] FIRRTL:370087 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_4_T_1 = geq(UInt<3>(0h4), lcam_younger_load_mask_0_4_real_head_idx)
[3716] FIRRTL:370088 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_4_T_2 = lt(UInt<3>(0h4), lcam_younger_load_mask_0_4_real_tail_idx)
[3717] FIRRTL:370089 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_4_T_3 = and(_lcam_younger_load_mask_0_4_T_1, _lcam_younger_load_mask_0_4_T_2)
[3718] FIRRTL:370090 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_4_T_4 = geq(UInt<3>(0h4), lcam_younger_load_mask_0_4_real_head_idx)
[3719] FIRRTL:370091 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_4_T_5 = lt(UInt<3>(0h4), lcam_younger_load_mask_0_4_real_tail_idx)
[3720] FIRRTL:370092 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_4_T_6 = or(_lcam_younger_load_mask_0_4_T_4, _lcam_younger_load_mask_0_4_T_5)
[3721] FIRRTL:370093 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_4_T_7 = mux(_lcam_younger_load_mask_0_4_T, _lcam_younger_load_mask_0_4_T_3, _lcam_younger_load_mask_0_4_T_6)
[3722] FIRRTL:370094 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_4_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3723] FIRRTL:370095 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_4_T_9 = neq(UInt<3>(0h4), _lcam_younger_load_mask_0_4_T_8)
[3724] FIRRTL:370096 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_4_T_10 = and(_lcam_younger_load_mask_0_4_T_7, _lcam_younger_load_mask_0_4_T_9)
[3725] FIRRTL:370097 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][4], _lcam_younger_load_mask_0_4_T_10
[3726] FIRRTL:370098 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_5_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3728] FIRRTL:370100 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_5_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3730] FIRRTL:370102 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_5_T = eq(lcam_younger_load_mask_0_5_head_carry, lcam_younger_load_mask_0_5_tail_carry)
[3731] FIRRTL:370103 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_5_T_1 = geq(UInt<3>(0h5), lcam_younger_load_mask_0_5_real_head_idx)
[3732] FIRRTL:370104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_5_T_2 = lt(UInt<3>(0h5), lcam_younger_load_mask_0_5_real_tail_idx)
[3733] FIRRTL:370105 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_5_T_3 = and(_lcam_younger_load_mask_0_5_T_1, _lcam_younger_load_mask_0_5_T_2)
[3734] FIRRTL:370106 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_5_T_4 = geq(UInt<3>(0h5), lcam_younger_load_mask_0_5_real_head_idx)
[3735] FIRRTL:370107 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_5_T_5 = lt(UInt<3>(0h5), lcam_younger_load_mask_0_5_real_tail_idx)
[3736] FIRRTL:370108 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_5_T_6 = or(_lcam_younger_load_mask_0_5_T_4, _lcam_younger_load_mask_0_5_T_5)
[3737] FIRRTL:370109 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_5_T_7 = mux(_lcam_younger_load_mask_0_5_T, _lcam_younger_load_mask_0_5_T_3, _lcam_younger_load_mask_0_5_T_6)
[3738] FIRRTL:370110 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_5_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3739] FIRRTL:370111 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_5_T_9 = neq(UInt<3>(0h5), _lcam_younger_load_mask_0_5_T_8)
[3740] FIRRTL:370112 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_5_T_10 = and(_lcam_younger_load_mask_0_5_T_7, _lcam_younger_load_mask_0_5_T_9)
[3741] FIRRTL:370113 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][5], _lcam_younger_load_mask_0_5_T_10
[3742] FIRRTL:370114 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_6_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3744] FIRRTL:370116 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_6_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3746] FIRRTL:370118 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_6_T = eq(lcam_younger_load_mask_0_6_head_carry, lcam_younger_load_mask_0_6_tail_carry)
[3747] FIRRTL:370119 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_6_T_1 = geq(UInt<3>(0h6), lcam_younger_load_mask_0_6_real_head_idx)
[3748] FIRRTL:370120 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_6_T_2 = lt(UInt<3>(0h6), lcam_younger_load_mask_0_6_real_tail_idx)
[3749] FIRRTL:370121 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_6_T_3 = and(_lcam_younger_load_mask_0_6_T_1, _lcam_younger_load_mask_0_6_T_2)
[3750] FIRRTL:370122 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_6_T_4 = geq(UInt<3>(0h6), lcam_younger_load_mask_0_6_real_head_idx)
[3751] FIRRTL:370123 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_6_T_5 = lt(UInt<3>(0h6), lcam_younger_load_mask_0_6_real_tail_idx)
[3752] FIRRTL:370124 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_6_T_6 = or(_lcam_younger_load_mask_0_6_T_4, _lcam_younger_load_mask_0_6_T_5)
[3753] FIRRTL:370125 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_6_T_7 = mux(_lcam_younger_load_mask_0_6_T, _lcam_younger_load_mask_0_6_T_3, _lcam_younger_load_mask_0_6_T_6)
[3754] FIRRTL:370126 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_6_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3755] FIRRTL:370127 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_6_T_9 = neq(UInt<3>(0h6), _lcam_younger_load_mask_0_6_T_8)
[3756] FIRRTL:370128 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_6_T_10 = and(_lcam_younger_load_mask_0_6_T_7, _lcam_younger_load_mask_0_6_T_9)
[3757] FIRRTL:370129 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][6], _lcam_younger_load_mask_0_6_T_10
[3758] FIRRTL:370130 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node lcam_younger_load_mask_0_7_real_head_idx = bits(lcam_ldq_idx[0], 2, 0)
[3760] FIRRTL:370132 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node lcam_younger_load_mask_0_7_head_carry = bits(lcam_ldq_idx[0], 3, 3)
[3762] FIRRTL:370134 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _lcam_younger_load_mask_0_7_T = eq(lcam_younger_load_mask_0_7_head_carry, lcam_younger_load_mask_0_7_tail_carry)
[3763] FIRRTL:370135 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _lcam_younger_load_mask_0_7_T_1 = geq(UInt<3>(0h7), lcam_younger_load_mask_0_7_real_head_idx)
[3764] FIRRTL:370136 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _lcam_younger_load_mask_0_7_T_2 = lt(UInt<3>(0h7), lcam_younger_load_mask_0_7_real_tail_idx)
[3765] FIRRTL:370137 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _lcam_younger_load_mask_0_7_T_3 = and(_lcam_younger_load_mask_0_7_T_1, _lcam_younger_load_mask_0_7_T_2)
[3766] FIRRTL:370138 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _lcam_younger_load_mask_0_7_T_4 = geq(UInt<3>(0h7), lcam_younger_load_mask_0_7_real_head_idx)
[3767] FIRRTL:370139 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _lcam_younger_load_mask_0_7_T_5 = lt(UInt<3>(0h7), lcam_younger_load_mask_0_7_real_tail_idx)
[3768] FIRRTL:370140 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _lcam_younger_load_mask_0_7_T_6 = or(_lcam_younger_load_mask_0_7_T_4, _lcam_younger_load_mask_0_7_T_5)
[3769] FIRRTL:370141 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _lcam_younger_load_mask_0_7_T_7 = mux(_lcam_younger_load_mask_0_7_T, _lcam_younger_load_mask_0_7_T_3, _lcam_younger_load_mask_0_7_T_6)
[3770] FIRRTL:370142 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _lcam_younger_load_mask_0_7_T_8 = bits(lcam_ldq_idx[0], 2, 0)
[3771] FIRRTL:370143 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:113 KIND:node :: node _lcam_younger_load_mask_0_7_T_9 = neq(UInt<3>(0h7), _lcam_younger_load_mask_0_7_T_8)
[3772] FIRRTL:370144 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:106 KIND:node :: node _lcam_younger_load_mask_0_7_T_10 = and(_lcam_younger_load_mask_0_7_T_7, _lcam_younger_load_mask_0_7_T_9)
[3773] FIRRTL:370145 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1152:36 KIND:connect :: connect lcam_younger_load_mask[0][7], _lcam_younger_load_mask_0_7_T_10
[3774] FIRRTL:370146 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1157:58 KIND:node :: node _can_forward_T = or(fired_load_agen[0], fired_load_agen_exec[0])
[3775] FIRRTL:370147 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1157:85 KIND:node :: node _can_forward_T_1 = or(_can_forward_T, fired_load_retry[0])
[3776] FIRRTL:370148 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1158:5 KIND:node :: node _can_forward_T_2 = eq(mem_tlb_uncacheable[0], UInt<1>(0h0))
[3777] FIRRTL:370149 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1159:5 KIND:node :: node _can_forward_T_3 = eq(mem_ldq_wakeup_e.bits.addr_is_uncacheable, UInt<1>(0h0))
[3778] FIRRTL:370150 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1157:38 KIND:node :: node _can_forward_T_4 = mux(_can_forward_T_1, _can_forward_T_2, _can_forward_T_3)
[3780] FIRRTL:370152 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect can_forward[0], _can_forward_T_4
[3782] FIRRTL:370154 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _kill_forward_WIRE[0], UInt<1>(0h0)
[3784] FIRRTL:370156 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1162:30 KIND:connect :: connect kill_forward, _kill_forward_WIRE
[3834] FIRRTL:370206 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2145:9 KIND:connect :: connect wb_ldst_forward_ldq_idx, lcam_ldq_idx
[3842] FIRRTL:370214 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T = shr(lcam_addr[0], 6)
[3844] FIRRTL:370216 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_2 = eq(_block_addr_matches_T, _block_addr_matches_T_1)
[3846] FIRRTL:370218 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches[0], _block_addr_matches_T_2
[3847] FIRRTL:370219 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T = bits(lcam_addr[0], 5, 3)
[3849] FIRRTL:370221 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_2 = eq(_dword_addr_matches_T, _dword_addr_matches_T_1)
[3850] FIRRTL:370222 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_3 = and(block_addr_matches[0], _dword_addr_matches_T_2)
[3852] FIRRTL:370224 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches[0], _dword_addr_matches_T_3
[3857] FIRRTL:370229 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T = and(ldq_ld_byte_mask[0], lcam_mask[0])
[3858] FIRRTL:370230 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_1 = orr(_mask_overlap_T)
[3860] FIRRTL:370232 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap[0], _mask_overlap_T_1
[3950] FIRRTL:370322 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_270 = and(_T_268, _T_269)
[3951] FIRRTL:370323 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_271 = and(_T_270, dword_addr_matches[0])
[3952] FIRRTL:370324 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_272 = and(_T_271, mask_overlap[0])
[3953] FIRRTL:370325 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_272 :
[3967] FIRRTL:370339 SRC:<no-source-locator> KIND:else :: else :
[3968] FIRRTL:370340 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_280 = bits(lcam_ldq_idx[0], 2, 0)
[3969] FIRRTL:370341 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_281 = neq(_T_280, UInt<1>(0h0))
[3970] FIRRTL:370342 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_281 :
[3973] FIRRTL:370345 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_284 = eq(_T_283, UInt<1>(0h0))
[3974] FIRRTL:370346 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_284 :
[3985] FIRRTL:370357 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[3988] FIRRTL:370360 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_3 = shr(lcam_addr[0], 6)
[3990] FIRRTL:370362 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_5 = eq(_block_addr_matches_T_3, _block_addr_matches_T_4)
[3992] FIRRTL:370364 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_1[0], _block_addr_matches_T_5
[3993] FIRRTL:370365 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_4 = bits(lcam_addr[0], 5, 3)
[3995] FIRRTL:370367 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_6 = eq(_dword_addr_matches_T_4, _dword_addr_matches_T_5)
[3996] FIRRTL:370368 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_7 = and(block_addr_matches_1[0], _dword_addr_matches_T_6)
[3998] FIRRTL:370370 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_1[0], _dword_addr_matches_T_7
[4003] FIRRTL:370375 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_2 = and(ldq_ld_byte_mask[1], lcam_mask[0])
[4004] FIRRTL:370376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_3 = orr(_mask_overlap_T_2)
[4006] FIRRTL:370378 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_1[0], _mask_overlap_T_3
[4096] FIRRTL:370468 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_322 = and(_T_320, _T_321)
[4097] FIRRTL:370469 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_323 = and(_T_322, dword_addr_matches_1[0])
[4098] FIRRTL:370470 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_324 = and(_T_323, mask_overlap_1[0])
[4099] FIRRTL:370471 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_324 :
[4113] FIRRTL:370485 SRC:<no-source-locator> KIND:else :: else :
[4114] FIRRTL:370486 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_332 = bits(lcam_ldq_idx[0], 2, 0)
[4115] FIRRTL:370487 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_333 = neq(_T_332, UInt<1>(0h1))
[4116] FIRRTL:370488 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_333 :
[4119] FIRRTL:370491 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_336 = eq(_T_335, UInt<1>(0h0))
[4120] FIRRTL:370492 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_336 :
[4131] FIRRTL:370503 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4134] FIRRTL:370506 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_6 = shr(lcam_addr[0], 6)
[4136] FIRRTL:370508 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_8 = eq(_block_addr_matches_T_6, _block_addr_matches_T_7)
[4138] FIRRTL:370510 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_2[0], _block_addr_matches_T_8
[4139] FIRRTL:370511 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_8 = bits(lcam_addr[0], 5, 3)
[4141] FIRRTL:370513 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_10 = eq(_dword_addr_matches_T_8, _dword_addr_matches_T_9)
[4142] FIRRTL:370514 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_11 = and(block_addr_matches_2[0], _dword_addr_matches_T_10)
[4144] FIRRTL:370516 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_2[0], _dword_addr_matches_T_11
[4149] FIRRTL:370521 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_4 = and(ldq_ld_byte_mask[2], lcam_mask[0])
[4150] FIRRTL:370522 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_5 = orr(_mask_overlap_T_4)
[4152] FIRRTL:370524 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_2[0], _mask_overlap_T_5
[4242] FIRRTL:370614 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_374 = and(_T_372, _T_373)
[4243] FIRRTL:370615 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_375 = and(_T_374, dword_addr_matches_2[0])
[4244] FIRRTL:370616 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_376 = and(_T_375, mask_overlap_2[0])
[4245] FIRRTL:370617 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_376 :
[4259] FIRRTL:370631 SRC:<no-source-locator> KIND:else :: else :
[4260] FIRRTL:370632 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_384 = bits(lcam_ldq_idx[0], 2, 0)
[4261] FIRRTL:370633 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_385 = neq(_T_384, UInt<2>(0h2))
[4262] FIRRTL:370634 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_385 :
[4265] FIRRTL:370637 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_388 = eq(_T_387, UInt<1>(0h0))
[4266] FIRRTL:370638 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_388 :
[4277] FIRRTL:370649 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4280] FIRRTL:370652 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_9 = shr(lcam_addr[0], 6)
[4282] FIRRTL:370654 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_11 = eq(_block_addr_matches_T_9, _block_addr_matches_T_10)
[4284] FIRRTL:370656 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_3[0], _block_addr_matches_T_11
[4285] FIRRTL:370657 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_12 = bits(lcam_addr[0], 5, 3)
[4287] FIRRTL:370659 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_14 = eq(_dword_addr_matches_T_12, _dword_addr_matches_T_13)
[4288] FIRRTL:370660 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_15 = and(block_addr_matches_3[0], _dword_addr_matches_T_14)
[4290] FIRRTL:370662 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_3[0], _dword_addr_matches_T_15
[4295] FIRRTL:370667 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_6 = and(ldq_ld_byte_mask[3], lcam_mask[0])
[4296] FIRRTL:370668 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_7 = orr(_mask_overlap_T_6)
[4298] FIRRTL:370670 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_3[0], _mask_overlap_T_7
[4388] FIRRTL:370760 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_426 = and(_T_424, _T_425)
[4389] FIRRTL:370761 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_427 = and(_T_426, dword_addr_matches_3[0])
[4390] FIRRTL:370762 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_428 = and(_T_427, mask_overlap_3[0])
[4391] FIRRTL:370763 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_428 :
[4405] FIRRTL:370777 SRC:<no-source-locator> KIND:else :: else :
[4406] FIRRTL:370778 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_436 = bits(lcam_ldq_idx[0], 2, 0)
[4407] FIRRTL:370779 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_437 = neq(_T_436, UInt<2>(0h3))
[4408] FIRRTL:370780 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_437 :
[4411] FIRRTL:370783 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_440 = eq(_T_439, UInt<1>(0h0))
[4412] FIRRTL:370784 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_440 :
[4423] FIRRTL:370795 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4426] FIRRTL:370798 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_12 = shr(lcam_addr[0], 6)
[4428] FIRRTL:370800 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_14 = eq(_block_addr_matches_T_12, _block_addr_matches_T_13)
[4430] FIRRTL:370802 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_4[0], _block_addr_matches_T_14
[4431] FIRRTL:370803 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_16 = bits(lcam_addr[0], 5, 3)
[4433] FIRRTL:370805 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_18 = eq(_dword_addr_matches_T_16, _dword_addr_matches_T_17)
[4434] FIRRTL:370806 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_19 = and(block_addr_matches_4[0], _dword_addr_matches_T_18)
[4436] FIRRTL:370808 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_4[0], _dword_addr_matches_T_19
[4441] FIRRTL:370813 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_8 = and(ldq_ld_byte_mask[4], lcam_mask[0])
[4442] FIRRTL:370814 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_9 = orr(_mask_overlap_T_8)
[4444] FIRRTL:370816 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_4[0], _mask_overlap_T_9
[4534] FIRRTL:370906 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_478 = and(_T_476, _T_477)
[4535] FIRRTL:370907 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_479 = and(_T_478, dword_addr_matches_4[0])
[4536] FIRRTL:370908 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_480 = and(_T_479, mask_overlap_4[0])
[4537] FIRRTL:370909 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_480 :
[4551] FIRRTL:370923 SRC:<no-source-locator> KIND:else :: else :
[4552] FIRRTL:370924 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_488 = bits(lcam_ldq_idx[0], 2, 0)
[4553] FIRRTL:370925 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_489 = neq(_T_488, UInt<3>(0h4))
[4554] FIRRTL:370926 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_489 :
[4557] FIRRTL:370929 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_492 = eq(_T_491, UInt<1>(0h0))
[4558] FIRRTL:370930 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_492 :
[4569] FIRRTL:370941 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4572] FIRRTL:370944 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_15 = shr(lcam_addr[0], 6)
[4574] FIRRTL:370946 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_17 = eq(_block_addr_matches_T_15, _block_addr_matches_T_16)
[4576] FIRRTL:370948 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_5[0], _block_addr_matches_T_17
[4577] FIRRTL:370949 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_20 = bits(lcam_addr[0], 5, 3)
[4579] FIRRTL:370951 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_22 = eq(_dword_addr_matches_T_20, _dword_addr_matches_T_21)
[4580] FIRRTL:370952 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_23 = and(block_addr_matches_5[0], _dword_addr_matches_T_22)
[4582] FIRRTL:370954 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_5[0], _dword_addr_matches_T_23
[4587] FIRRTL:370959 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_10 = and(ldq_ld_byte_mask[5], lcam_mask[0])
[4588] FIRRTL:370960 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_11 = orr(_mask_overlap_T_10)
[4590] FIRRTL:370962 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_5[0], _mask_overlap_T_11
[4680] FIRRTL:371052 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_530 = and(_T_528, _T_529)
[4681] FIRRTL:371053 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_531 = and(_T_530, dword_addr_matches_5[0])
[4682] FIRRTL:371054 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_532 = and(_T_531, mask_overlap_5[0])
[4683] FIRRTL:371055 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_532 :
[4697] FIRRTL:371069 SRC:<no-source-locator> KIND:else :: else :
[4698] FIRRTL:371070 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_540 = bits(lcam_ldq_idx[0], 2, 0)
[4699] FIRRTL:371071 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_541 = neq(_T_540, UInt<3>(0h5))
[4700] FIRRTL:371072 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_541 :
[4703] FIRRTL:371075 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_544 = eq(_T_543, UInt<1>(0h0))
[4704] FIRRTL:371076 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_544 :
[4715] FIRRTL:371087 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4718] FIRRTL:371090 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_18 = shr(lcam_addr[0], 6)
[4720] FIRRTL:371092 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_20 = eq(_block_addr_matches_T_18, _block_addr_matches_T_19)
[4722] FIRRTL:371094 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_6[0], _block_addr_matches_T_20
[4723] FIRRTL:371095 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_24 = bits(lcam_addr[0], 5, 3)
[4725] FIRRTL:371097 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_26 = eq(_dword_addr_matches_T_24, _dword_addr_matches_T_25)
[4726] FIRRTL:371098 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_27 = and(block_addr_matches_6[0], _dword_addr_matches_T_26)
[4728] FIRRTL:371100 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_6[0], _dword_addr_matches_T_27
[4733] FIRRTL:371105 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_12 = and(ldq_ld_byte_mask[6], lcam_mask[0])
[4734] FIRRTL:371106 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_13 = orr(_mask_overlap_T_12)
[4736] FIRRTL:371108 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_6[0], _mask_overlap_T_13
[4826] FIRRTL:371198 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_582 = and(_T_580, _T_581)
[4827] FIRRTL:371199 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_583 = and(_T_582, dword_addr_matches_6[0])
[4828] FIRRTL:371200 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_584 = and(_T_583, mask_overlap_6[0])
[4829] FIRRTL:371201 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_584 :
[4843] FIRRTL:371215 SRC:<no-source-locator> KIND:else :: else :
[4844] FIRRTL:371216 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_592 = bits(lcam_ldq_idx[0], 2, 0)
[4845] FIRRTL:371217 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_593 = neq(_T_592, UInt<3>(0h6))
[4846] FIRRTL:371218 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_593 :
[4849] FIRRTL:371221 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_596 = eq(_T_595, UInt<1>(0h0))
[4850] FIRRTL:371222 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_596 :
[4861] FIRRTL:371233 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[4864] FIRRTL:371236 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:57 KIND:node :: node _block_addr_matches_T_21 = shr(lcam_addr[0], 6)
[4866] FIRRTL:371238 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1198:73 KIND:node :: node _block_addr_matches_T_23 = eq(_block_addr_matches_T_21, _block_addr_matches_T_22)
[4868] FIRRTL:371240 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect block_addr_matches_7[0], _block_addr_matches_T_23
[4869] FIRRTL:371241 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:81 KIND:node :: node _dword_addr_matches_T_28 = bits(lcam_addr[0], 5, 3)
[4871] FIRRTL:371243 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:100 KIND:node :: node _dword_addr_matches_T_30 = eq(_dword_addr_matches_T_28, _dword_addr_matches_T_29)
[4872] FIRRTL:371244 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1199:66 KIND:node :: node _dword_addr_matches_T_31 = and(block_addr_matches_7[0], _dword_addr_matches_T_30)
[4874] FIRRTL:371246 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect dword_addr_matches_7[0], _dword_addr_matches_T_31
[4879] FIRRTL:371251 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:46 KIND:node :: node _mask_overlap_T_14 = and(ldq_ld_byte_mask[7], lcam_mask[0])
[4880] FIRRTL:371252 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1201:62 KIND:node :: node _mask_overlap_T_15 = orr(_mask_overlap_T_14)
[4882] FIRRTL:371254 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect mask_overlap_7[0], _mask_overlap_T_15
[4972] FIRRTL:371344 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1240:42 KIND:node :: node _T_634 = and(_T_632, _T_633)
[4973] FIRRTL:371345 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1241:42 KIND:node :: node _T_635 = and(_T_634, dword_addr_matches_7[0])
[4974] FIRRTL:371346 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1242:42 KIND:node :: node _T_636 = and(_T_635, mask_overlap_7[0])
[4975] FIRRTL:371347 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1243:37 KIND:when :: when _T_636 :
[4989] FIRRTL:371361 SRC:<no-source-locator> KIND:else :: else :
[4990] FIRRTL:371362 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node _T_644 = bits(lcam_ldq_idx[0], 2, 0)
[4991] FIRRTL:371363 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:53 KIND:node :: node _T_645 = neq(_T_644, UInt<3>(0h7))
[4992] FIRRTL:371364 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1257:62 KIND:when :: when _T_645 :
[4995] FIRRTL:371367 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:17 KIND:node :: node _T_648 = eq(_T_647, UInt<1>(0h0))
[4996] FIRRTL:371368 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1261:67 KIND:when :: when _T_648 :
[5007] FIRRTL:371379 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1266:48 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[5008] FIRRTL:371380 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1278:51 KIND:node :: node _nack_dword_addr_matches_T = shr(lcam_addr[0], 3)
[5009] FIRRTL:371381 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1278:89 KIND:node :: node _nack_dword_addr_matches_T_1 = shr(io.dmem.nack[0].bits.addr, 3)
[5010] FIRRTL:371382 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1278:57 KIND:node :: node nack_dword_addr_matches = eq(_nack_dword_addr_matches_T, _nack_dword_addr_matches_T_1)
[5012] FIRRTL:371384 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _nack_mask_mask_T = eq(io.dmem.nack[0].bits.uop.mem_size, UInt<1>(0h0))
[5013] FIRRTL:371385 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _nack_mask_mask_T_1 = bits(io.dmem.nack[0].bits.addr, 2, 0)
[5014] FIRRTL:371386 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _nack_mask_mask_T_2 = dshl(UInt<8>(0h1), _nack_mask_mask_T_1)
[5015] FIRRTL:371387 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _nack_mask_mask_T_3 = eq(io.dmem.nack[0].bits.uop.mem_size, UInt<1>(0h1))
[5016] FIRRTL:371388 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _nack_mask_mask_T_4 = bits(io.dmem.nack[0].bits.addr, 2, 1)
[5017] FIRRTL:371389 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _nack_mask_mask_T_5 = dshl(_nack_mask_mask_T_4, UInt<1>(0h1))
[5018] FIRRTL:371390 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _nack_mask_mask_T_6 = dshl(UInt<8>(0h3), _nack_mask_mask_T_5)
[5019] FIRRTL:371391 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _nack_mask_mask_T_7 = eq(io.dmem.nack[0].bits.uop.mem_size, UInt<2>(0h2))
[5020] FIRRTL:371392 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _nack_mask_mask_T_8 = bits(io.dmem.nack[0].bits.addr, 2, 2)
[5021] FIRRTL:371393 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _nack_mask_mask_T_9 = mux(_nack_mask_mask_T_8, UInt<8>(0hf0), UInt<8>(0hf))
[5022] FIRRTL:371394 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _nack_mask_mask_T_10 = eq(io.dmem.nack[0].bits.uop.mem_size, UInt<2>(0h3))
[5023] FIRRTL:371395 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _nack_mask_mask_T_11 = mux(_nack_mask_mask_T_10, UInt<8>(0hff), UInt<8>(0hff))
[5024] FIRRTL:371396 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _nack_mask_mask_T_12 = mux(_nack_mask_mask_T_7, _nack_mask_mask_T_9, _nack_mask_mask_T_11)
[5025] FIRRTL:371397 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _nack_mask_mask_T_13 = mux(_nack_mask_mask_T_3, _nack_mask_mask_T_6, _nack_mask_mask_T_12)
[5026] FIRRTL:371398 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _nack_mask_mask_T_14 = mux(_nack_mask_mask_T, _nack_mask_mask_T_2, _nack_mask_mask_T_13)
[5027] FIRRTL:371399 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect nack_mask, _nack_mask_mask_T_14
[5028] FIRRTL:371400 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1280:42 KIND:node :: node _nack_mask_overlap_T = and(nack_mask, lcam_mask[0])
[5029] FIRRTL:371401 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1280:58 KIND:node :: node nack_mask_overlap = neq(_nack_mask_overlap_T, UInt<1>(0h0))
[5030] FIRRTL:371402 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1281:48 KIND:node :: node _T_654 = and(do_ld_search[0], io.dmem.nack[0].valid)
[5031] FIRRTL:371403 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1282:48 KIND:node :: node _T_655 = and(_T_654, io.dmem.nack[0].bits.uop.uses_ldq)
[5032] FIRRTL:371404 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1283:48 KIND:node :: node _T_656 = and(_T_655, nack_dword_addr_matches)
[5033] FIRRTL:371405 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1284:48 KIND:node :: node _T_657 = and(_T_656, nack_mask_overlap)
[5034] FIRRTL:371406 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age1_overflow_8 = bits(lcam_ldq_idx[0], 3, 3)
[5035] FIRRTL:371407 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_8 = bits(io.dmem.nack[0].bits.uop.ldq_idx, 3, 3)
[5036] FIRRTL:371408 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age1_age_8 = bits(lcam_ldq_idx[0], 2, 0)
[5037] FIRRTL:371409 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_8 = bits(io.dmem.nack[0].bits.uop.ldq_idx, 2, 0)
[5038] FIRRTL:371410 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_658 = eq(age1_overflow_8, age2_overflow_8)
[5039] FIRRTL:371411 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_659 = gt(age1_age_8, age2_age_8)
[5040] FIRRTL:371412 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_660 = neq(age1_overflow_8, age2_overflow_8)
[5041] FIRRTL:371413 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_661 = lt(age1_age_8, age2_age_8)
[5042] FIRRTL:371414 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_662 = mux(_T_658, _T_659, UInt<1>(0h0))
[5043] FIRRTL:371415 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_663 = mux(_T_660, _T_661, UInt<1>(0h0))
[5044] FIRRTL:371416 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_664 = or(_T_662, _T_663)
[5046] FIRRTL:371418 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_8, _T_664
[5048] FIRRTL:371420 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_9 = bits(io.dmem.nack[0].bits.uop.ldq_idx, 3, 3)
[5050] FIRRTL:371422 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_9 = bits(io.dmem.nack[0].bits.uop.ldq_idx, 2, 0)
[5051] FIRRTL:371423 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_665 = eq(age1_overflow_9, age2_overflow_9)
[5052] FIRRTL:371424 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_666 = gt(age1_age_9, age2_age_9)
[5053] FIRRTL:371425 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_667 = neq(age1_overflow_9, age2_overflow_9)
[5054] FIRRTL:371426 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_668 = lt(age1_age_9, age2_age_9)
[5055] FIRRTL:371427 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_669 = mux(_T_665, _T_666, UInt<1>(0h0))
[5056] FIRRTL:371428 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_670 = mux(_T_667, _T_668, UInt<1>(0h0))
[5057] FIRRTL:371429 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_671 = or(_T_669, _T_670)
[5059] FIRRTL:371431 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_9, _T_671
[5060] FIRRTL:371432 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:22 KIND:node :: node _T_672 = xor(_WIRE_8, _WIRE_9)
[5062] FIRRTL:371434 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_10 = bits(lcam_ldq_idx[0], 3, 3)
[5064] FIRRTL:371436 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_10 = bits(lcam_ldq_idx[0], 2, 0)
[5065] FIRRTL:371437 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_673 = eq(age1_overflow_10, age2_overflow_10)
[5066] FIRRTL:371438 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_674 = gt(age1_age_10, age2_age_10)
[5067] FIRRTL:371439 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_675 = neq(age1_overflow_10, age2_overflow_10)
[5068] FIRRTL:371440 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_676 = lt(age1_age_10, age2_age_10)
[5069] FIRRTL:371441 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_677 = mux(_T_673, _T_674, UInt<1>(0h0))
[5070] FIRRTL:371442 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_678 = mux(_T_675, _T_676, UInt<1>(0h0))
[5071] FIRRTL:371443 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_679 = or(_T_677, _T_678)
[5073] FIRRTL:371445 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_10, _T_679
[5074] FIRRTL:371446 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:43 KIND:node :: node _T_680 = xor(_T_672, _WIRE_10)
[5075] FIRRTL:371447 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1285:48 KIND:node :: node _T_681 = and(_T_657, _T_680)
[5076] FIRRTL:371448 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1286:87 KIND:when :: when _T_681 :
[5087] FIRRTL:371459 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1291:25 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[5228] FIRRTL:371600 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_1, stq_uop[0]
[5231] FIRRTL:371603 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T = eq(s_uop_1.mem_size, UInt<1>(0h0))
[5232] FIRRTL:371604 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_1 = bits(stq_addr[0].bits, 2, 0)
[5233] FIRRTL:371605 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_2 = dshl(UInt<8>(0h1), _write_mask_mask_T_1)
[5234] FIRRTL:371606 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_3 = eq(s_uop_1.mem_size, UInt<1>(0h1))
[5235] FIRRTL:371607 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_4 = bits(stq_addr[0].bits, 2, 1)
[5236] FIRRTL:371608 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_5 = dshl(_write_mask_mask_T_4, UInt<1>(0h1))
[5237] FIRRTL:371609 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_6 = dshl(UInt<8>(0h3), _write_mask_mask_T_5)
[5238] FIRRTL:371610 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_7 = eq(s_uop_1.mem_size, UInt<2>(0h2))
[5239] FIRRTL:371611 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_8 = bits(stq_addr[0].bits, 2, 2)
[5240] FIRRTL:371612 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_9 = mux(_write_mask_mask_T_8, UInt<8>(0hf0), UInt<8>(0hf))
[5241] FIRRTL:371613 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_10 = eq(s_uop_1.mem_size, UInt<2>(0h3))
[5242] FIRRTL:371614 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_11 = mux(_write_mask_mask_T_10, UInt<8>(0hff), UInt<8>(0hff))
[5243] FIRRTL:371615 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_12 = mux(_write_mask_mask_T_7, _write_mask_mask_T_9, _write_mask_mask_T_11)
[5244] FIRRTL:371616 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_13 = mux(_write_mask_mask_T_3, _write_mask_mask_T_6, _write_mask_mask_T_12)
[5245] FIRRTL:371617 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_14 = mux(_write_mask_mask_T, _write_mask_mask_T_2, _write_mask_mask_T_13)
[5246] FIRRTL:371618 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask, _write_mask_mask_T_14
[5247] FIRRTL:371619 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_32 = eq(s_uop_1.is_amo, UInt<1>(0h0))
[5248] FIRRTL:371620 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_33 = and(stq_addr[0].valid, _dword_addr_matches_T_32)
[5249] FIRRTL:371621 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_34 = eq(stq_addr_is_virtual[0], UInt<1>(0h0))
[5250] FIRRTL:371622 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_35 = and(_dword_addr_matches_T_33, _dword_addr_matches_T_34)
[5251] FIRRTL:371623 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_36 = bits(stq_addr[0].bits, 31, 3)
[5252] FIRRTL:371624 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_37 = bits(lcam_addr[0], 31, 3)
[5253] FIRRTL:371625 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_38 = eq(_dword_addr_matches_T_36, _dword_addr_matches_T_37)
[5254] FIRRTL:371626 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_8 = and(_dword_addr_matches_T_35, _dword_addr_matches_T_38)
[5255] FIRRTL:371627 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union = and(lcam_mask[0], write_mask)
[5256] FIRRTL:371628 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_0_T = neq(mask_union, UInt<1>(0h0))
[5257] FIRRTL:371629 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_0_T_1 = and(_addr_matches_0_0_T, dword_addr_matches_8)
[5258] FIRRTL:371630 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][0], _addr_matches_0_0_T_1
[5294] FIRRTL:371666 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_0_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5296] FIRRTL:371668 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_0_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5297] FIRRTL:371669 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_0_T = eq(age_matches_0_0_head_carry, age_matches_0_0_tail_carry)
[5298] FIRRTL:371670 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_0_T_1 = geq(UInt<3>(0h0), age_matches_0_0_real_head_idx)
[5299] FIRRTL:371671 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_0_T_2 = lt(UInt<3>(0h0), age_matches_0_0_real_tail_idx)
[5300] FIRRTL:371672 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_0_T_3 = and(_age_matches_0_0_T_1, _age_matches_0_0_T_2)
[5301] FIRRTL:371673 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_0_T_4 = geq(UInt<3>(0h0), age_matches_0_0_real_head_idx)
[5302] FIRRTL:371674 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_0_T_5 = lt(UInt<3>(0h0), age_matches_0_0_real_tail_idx)
[5303] FIRRTL:371675 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_0_T_6 = or(_age_matches_0_0_T_4, _age_matches_0_0_T_5)
[5304] FIRRTL:371676 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_0_T_7 = mux(_age_matches_0_0_T, _age_matches_0_0_T_3, _age_matches_0_0_T_6)
[5305] FIRRTL:371677 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][0], _age_matches_0_0_T_7
[5307] FIRRTL:371679 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_2, stq_uop[1]
[5310] FIRRTL:371682 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_15 = eq(s_uop_2.mem_size, UInt<1>(0h0))
[5311] FIRRTL:371683 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_16 = bits(stq_addr[1].bits, 2, 0)
[5312] FIRRTL:371684 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_17 = dshl(UInt<8>(0h1), _write_mask_mask_T_16)
[5313] FIRRTL:371685 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_18 = eq(s_uop_2.mem_size, UInt<1>(0h1))
[5314] FIRRTL:371686 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_19 = bits(stq_addr[1].bits, 2, 1)
[5315] FIRRTL:371687 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_20 = dshl(_write_mask_mask_T_19, UInt<1>(0h1))
[5316] FIRRTL:371688 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_21 = dshl(UInt<8>(0h3), _write_mask_mask_T_20)
[5317] FIRRTL:371689 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_22 = eq(s_uop_2.mem_size, UInt<2>(0h2))
[5318] FIRRTL:371690 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_23 = bits(stq_addr[1].bits, 2, 2)
[5319] FIRRTL:371691 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_24 = mux(_write_mask_mask_T_23, UInt<8>(0hf0), UInt<8>(0hf))
[5320] FIRRTL:371692 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_25 = eq(s_uop_2.mem_size, UInt<2>(0h3))
[5321] FIRRTL:371693 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_26 = mux(_write_mask_mask_T_25, UInt<8>(0hff), UInt<8>(0hff))
[5322] FIRRTL:371694 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_27 = mux(_write_mask_mask_T_22, _write_mask_mask_T_24, _write_mask_mask_T_26)
[5323] FIRRTL:371695 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_28 = mux(_write_mask_mask_T_18, _write_mask_mask_T_21, _write_mask_mask_T_27)
[5324] FIRRTL:371696 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_29 = mux(_write_mask_mask_T_15, _write_mask_mask_T_17, _write_mask_mask_T_28)
[5325] FIRRTL:371697 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_1, _write_mask_mask_T_29
[5326] FIRRTL:371698 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_39 = eq(s_uop_2.is_amo, UInt<1>(0h0))
[5327] FIRRTL:371699 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_40 = and(stq_addr[1].valid, _dword_addr_matches_T_39)
[5328] FIRRTL:371700 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_41 = eq(stq_addr_is_virtual[1], UInt<1>(0h0))
[5329] FIRRTL:371701 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_42 = and(_dword_addr_matches_T_40, _dword_addr_matches_T_41)
[5330] FIRRTL:371702 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_43 = bits(stq_addr[1].bits, 31, 3)
[5331] FIRRTL:371703 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_44 = bits(lcam_addr[0], 31, 3)
[5332] FIRRTL:371704 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_45 = eq(_dword_addr_matches_T_43, _dword_addr_matches_T_44)
[5333] FIRRTL:371705 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_9 = and(_dword_addr_matches_T_42, _dword_addr_matches_T_45)
[5334] FIRRTL:371706 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_1 = and(lcam_mask[0], write_mask_1)
[5335] FIRRTL:371707 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_1_T = neq(mask_union_1, UInt<1>(0h0))
[5336] FIRRTL:371708 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_1_T_1 = and(_addr_matches_0_1_T, dword_addr_matches_9)
[5337] FIRRTL:371709 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][1], _addr_matches_0_1_T_1
[5373] FIRRTL:371745 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_1_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5375] FIRRTL:371747 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_1_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5376] FIRRTL:371748 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_1_T = eq(age_matches_0_1_head_carry, age_matches_0_1_tail_carry)
[5377] FIRRTL:371749 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_1_T_1 = geq(UInt<3>(0h1), age_matches_0_1_real_head_idx)
[5378] FIRRTL:371750 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_1_T_2 = lt(UInt<3>(0h1), age_matches_0_1_real_tail_idx)
[5379] FIRRTL:371751 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_1_T_3 = and(_age_matches_0_1_T_1, _age_matches_0_1_T_2)
[5380] FIRRTL:371752 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_1_T_4 = geq(UInt<3>(0h1), age_matches_0_1_real_head_idx)
[5381] FIRRTL:371753 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_1_T_5 = lt(UInt<3>(0h1), age_matches_0_1_real_tail_idx)
[5382] FIRRTL:371754 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_1_T_6 = or(_age_matches_0_1_T_4, _age_matches_0_1_T_5)
[5383] FIRRTL:371755 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_1_T_7 = mux(_age_matches_0_1_T, _age_matches_0_1_T_3, _age_matches_0_1_T_6)
[5384] FIRRTL:371756 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][1], _age_matches_0_1_T_7
[5386] FIRRTL:371758 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_3, stq_uop[2]
[5389] FIRRTL:371761 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_30 = eq(s_uop_3.mem_size, UInt<1>(0h0))
[5390] FIRRTL:371762 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_31 = bits(stq_addr[2].bits, 2, 0)
[5391] FIRRTL:371763 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_32 = dshl(UInt<8>(0h1), _write_mask_mask_T_31)
[5392] FIRRTL:371764 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_33 = eq(s_uop_3.mem_size, UInt<1>(0h1))
[5393] FIRRTL:371765 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_34 = bits(stq_addr[2].bits, 2, 1)
[5394] FIRRTL:371766 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_35 = dshl(_write_mask_mask_T_34, UInt<1>(0h1))
[5395] FIRRTL:371767 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_36 = dshl(UInt<8>(0h3), _write_mask_mask_T_35)
[5396] FIRRTL:371768 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_37 = eq(s_uop_3.mem_size, UInt<2>(0h2))
[5397] FIRRTL:371769 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_38 = bits(stq_addr[2].bits, 2, 2)
[5398] FIRRTL:371770 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_39 = mux(_write_mask_mask_T_38, UInt<8>(0hf0), UInt<8>(0hf))
[5399] FIRRTL:371771 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_40 = eq(s_uop_3.mem_size, UInt<2>(0h3))
[5400] FIRRTL:371772 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_41 = mux(_write_mask_mask_T_40, UInt<8>(0hff), UInt<8>(0hff))
[5401] FIRRTL:371773 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_42 = mux(_write_mask_mask_T_37, _write_mask_mask_T_39, _write_mask_mask_T_41)
[5402] FIRRTL:371774 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_43 = mux(_write_mask_mask_T_33, _write_mask_mask_T_36, _write_mask_mask_T_42)
[5403] FIRRTL:371775 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_44 = mux(_write_mask_mask_T_30, _write_mask_mask_T_32, _write_mask_mask_T_43)
[5404] FIRRTL:371776 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_2, _write_mask_mask_T_44
[5405] FIRRTL:371777 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_46 = eq(s_uop_3.is_amo, UInt<1>(0h0))
[5406] FIRRTL:371778 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_47 = and(stq_addr[2].valid, _dword_addr_matches_T_46)
[5407] FIRRTL:371779 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_48 = eq(stq_addr_is_virtual[2], UInt<1>(0h0))
[5408] FIRRTL:371780 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_49 = and(_dword_addr_matches_T_47, _dword_addr_matches_T_48)
[5409] FIRRTL:371781 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_50 = bits(stq_addr[2].bits, 31, 3)
[5410] FIRRTL:371782 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_51 = bits(lcam_addr[0], 31, 3)
[5411] FIRRTL:371783 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_52 = eq(_dword_addr_matches_T_50, _dword_addr_matches_T_51)
[5412] FIRRTL:371784 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_10 = and(_dword_addr_matches_T_49, _dword_addr_matches_T_52)
[5413] FIRRTL:371785 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_2 = and(lcam_mask[0], write_mask_2)
[5414] FIRRTL:371786 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_2_T = neq(mask_union_2, UInt<1>(0h0))
[5415] FIRRTL:371787 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_2_T_1 = and(_addr_matches_0_2_T, dword_addr_matches_10)
[5416] FIRRTL:371788 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][2], _addr_matches_0_2_T_1
[5452] FIRRTL:371824 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_2_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5454] FIRRTL:371826 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_2_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5455] FIRRTL:371827 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_2_T = eq(age_matches_0_2_head_carry, age_matches_0_2_tail_carry)
[5456] FIRRTL:371828 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_2_T_1 = geq(UInt<3>(0h2), age_matches_0_2_real_head_idx)
[5457] FIRRTL:371829 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_2_T_2 = lt(UInt<3>(0h2), age_matches_0_2_real_tail_idx)
[5458] FIRRTL:371830 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_2_T_3 = and(_age_matches_0_2_T_1, _age_matches_0_2_T_2)
[5459] FIRRTL:371831 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_2_T_4 = geq(UInt<3>(0h2), age_matches_0_2_real_head_idx)
[5460] FIRRTL:371832 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_2_T_5 = lt(UInt<3>(0h2), age_matches_0_2_real_tail_idx)
[5461] FIRRTL:371833 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_2_T_6 = or(_age_matches_0_2_T_4, _age_matches_0_2_T_5)
[5462] FIRRTL:371834 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_2_T_7 = mux(_age_matches_0_2_T, _age_matches_0_2_T_3, _age_matches_0_2_T_6)
[5463] FIRRTL:371835 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][2], _age_matches_0_2_T_7
[5465] FIRRTL:371837 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_4, stq_uop[3]
[5468] FIRRTL:371840 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_45 = eq(s_uop_4.mem_size, UInt<1>(0h0))
[5469] FIRRTL:371841 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_46 = bits(stq_addr[3].bits, 2, 0)
[5470] FIRRTL:371842 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_47 = dshl(UInt<8>(0h1), _write_mask_mask_T_46)
[5471] FIRRTL:371843 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_48 = eq(s_uop_4.mem_size, UInt<1>(0h1))
[5472] FIRRTL:371844 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_49 = bits(stq_addr[3].bits, 2, 1)
[5473] FIRRTL:371845 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_50 = dshl(_write_mask_mask_T_49, UInt<1>(0h1))
[5474] FIRRTL:371846 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_51 = dshl(UInt<8>(0h3), _write_mask_mask_T_50)
[5475] FIRRTL:371847 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_52 = eq(s_uop_4.mem_size, UInt<2>(0h2))
[5476] FIRRTL:371848 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_53 = bits(stq_addr[3].bits, 2, 2)
[5477] FIRRTL:371849 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_54 = mux(_write_mask_mask_T_53, UInt<8>(0hf0), UInt<8>(0hf))
[5478] FIRRTL:371850 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_55 = eq(s_uop_4.mem_size, UInt<2>(0h3))
[5479] FIRRTL:371851 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_56 = mux(_write_mask_mask_T_55, UInt<8>(0hff), UInt<8>(0hff))
[5480] FIRRTL:371852 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_57 = mux(_write_mask_mask_T_52, _write_mask_mask_T_54, _write_mask_mask_T_56)
[5481] FIRRTL:371853 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_58 = mux(_write_mask_mask_T_48, _write_mask_mask_T_51, _write_mask_mask_T_57)
[5482] FIRRTL:371854 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_59 = mux(_write_mask_mask_T_45, _write_mask_mask_T_47, _write_mask_mask_T_58)
[5483] FIRRTL:371855 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_3, _write_mask_mask_T_59
[5484] FIRRTL:371856 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_53 = eq(s_uop_4.is_amo, UInt<1>(0h0))
[5485] FIRRTL:371857 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_54 = and(stq_addr[3].valid, _dword_addr_matches_T_53)
[5486] FIRRTL:371858 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_55 = eq(stq_addr_is_virtual[3], UInt<1>(0h0))
[5487] FIRRTL:371859 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_56 = and(_dword_addr_matches_T_54, _dword_addr_matches_T_55)
[5488] FIRRTL:371860 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_57 = bits(stq_addr[3].bits, 31, 3)
[5489] FIRRTL:371861 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_58 = bits(lcam_addr[0], 31, 3)
[5490] FIRRTL:371862 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_59 = eq(_dword_addr_matches_T_57, _dword_addr_matches_T_58)
[5491] FIRRTL:371863 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_11 = and(_dword_addr_matches_T_56, _dword_addr_matches_T_59)
[5492] FIRRTL:371864 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_3 = and(lcam_mask[0], write_mask_3)
[5493] FIRRTL:371865 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_3_T = neq(mask_union_3, UInt<1>(0h0))
[5494] FIRRTL:371866 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_3_T_1 = and(_addr_matches_0_3_T, dword_addr_matches_11)
[5495] FIRRTL:371867 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][3], _addr_matches_0_3_T_1
[5531] FIRRTL:371903 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_3_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5533] FIRRTL:371905 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_3_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5534] FIRRTL:371906 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_3_T = eq(age_matches_0_3_head_carry, age_matches_0_3_tail_carry)
[5535] FIRRTL:371907 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_3_T_1 = geq(UInt<3>(0h3), age_matches_0_3_real_head_idx)
[5536] FIRRTL:371908 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_3_T_2 = lt(UInt<3>(0h3), age_matches_0_3_real_tail_idx)
[5537] FIRRTL:371909 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_3_T_3 = and(_age_matches_0_3_T_1, _age_matches_0_3_T_2)
[5538] FIRRTL:371910 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_3_T_4 = geq(UInt<3>(0h3), age_matches_0_3_real_head_idx)
[5539] FIRRTL:371911 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_3_T_5 = lt(UInt<3>(0h3), age_matches_0_3_real_tail_idx)
[5540] FIRRTL:371912 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_3_T_6 = or(_age_matches_0_3_T_4, _age_matches_0_3_T_5)
[5541] FIRRTL:371913 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_3_T_7 = mux(_age_matches_0_3_T, _age_matches_0_3_T_3, _age_matches_0_3_T_6)
[5542] FIRRTL:371914 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][3], _age_matches_0_3_T_7
[5544] FIRRTL:371916 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_5, stq_uop[4]
[5547] FIRRTL:371919 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_60 = eq(s_uop_5.mem_size, UInt<1>(0h0))
[5548] FIRRTL:371920 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_61 = bits(stq_addr[4].bits, 2, 0)
[5549] FIRRTL:371921 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_62 = dshl(UInt<8>(0h1), _write_mask_mask_T_61)
[5550] FIRRTL:371922 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_63 = eq(s_uop_5.mem_size, UInt<1>(0h1))
[5551] FIRRTL:371923 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_64 = bits(stq_addr[4].bits, 2, 1)
[5552] FIRRTL:371924 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_65 = dshl(_write_mask_mask_T_64, UInt<1>(0h1))
[5553] FIRRTL:371925 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_66 = dshl(UInt<8>(0h3), _write_mask_mask_T_65)
[5554] FIRRTL:371926 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_67 = eq(s_uop_5.mem_size, UInt<2>(0h2))
[5555] FIRRTL:371927 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_68 = bits(stq_addr[4].bits, 2, 2)
[5556] FIRRTL:371928 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_69 = mux(_write_mask_mask_T_68, UInt<8>(0hf0), UInt<8>(0hf))
[5557] FIRRTL:371929 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_70 = eq(s_uop_5.mem_size, UInt<2>(0h3))
[5558] FIRRTL:371930 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_71 = mux(_write_mask_mask_T_70, UInt<8>(0hff), UInt<8>(0hff))
[5559] FIRRTL:371931 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_72 = mux(_write_mask_mask_T_67, _write_mask_mask_T_69, _write_mask_mask_T_71)
[5560] FIRRTL:371932 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_73 = mux(_write_mask_mask_T_63, _write_mask_mask_T_66, _write_mask_mask_T_72)
[5561] FIRRTL:371933 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_74 = mux(_write_mask_mask_T_60, _write_mask_mask_T_62, _write_mask_mask_T_73)
[5562] FIRRTL:371934 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_4, _write_mask_mask_T_74
[5563] FIRRTL:371935 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_60 = eq(s_uop_5.is_amo, UInt<1>(0h0))
[5564] FIRRTL:371936 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_61 = and(stq_addr[4].valid, _dword_addr_matches_T_60)
[5565] FIRRTL:371937 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_62 = eq(stq_addr_is_virtual[4], UInt<1>(0h0))
[5566] FIRRTL:371938 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_63 = and(_dword_addr_matches_T_61, _dword_addr_matches_T_62)
[5567] FIRRTL:371939 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_64 = bits(stq_addr[4].bits, 31, 3)
[5568] FIRRTL:371940 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_65 = bits(lcam_addr[0], 31, 3)
[5569] FIRRTL:371941 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_66 = eq(_dword_addr_matches_T_64, _dword_addr_matches_T_65)
[5570] FIRRTL:371942 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_12 = and(_dword_addr_matches_T_63, _dword_addr_matches_T_66)
[5571] FIRRTL:371943 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_4 = and(lcam_mask[0], write_mask_4)
[5572] FIRRTL:371944 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_4_T = neq(mask_union_4, UInt<1>(0h0))
[5573] FIRRTL:371945 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_4_T_1 = and(_addr_matches_0_4_T, dword_addr_matches_12)
[5574] FIRRTL:371946 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][4], _addr_matches_0_4_T_1
[5610] FIRRTL:371982 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_4_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5612] FIRRTL:371984 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_4_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5613] FIRRTL:371985 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_4_T = eq(age_matches_0_4_head_carry, age_matches_0_4_tail_carry)
[5614] FIRRTL:371986 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_4_T_1 = geq(UInt<3>(0h4), age_matches_0_4_real_head_idx)
[5615] FIRRTL:371987 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_4_T_2 = lt(UInt<3>(0h4), age_matches_0_4_real_tail_idx)
[5616] FIRRTL:371988 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_4_T_3 = and(_age_matches_0_4_T_1, _age_matches_0_4_T_2)
[5617] FIRRTL:371989 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_4_T_4 = geq(UInt<3>(0h4), age_matches_0_4_real_head_idx)
[5618] FIRRTL:371990 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_4_T_5 = lt(UInt<3>(0h4), age_matches_0_4_real_tail_idx)
[5619] FIRRTL:371991 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_4_T_6 = or(_age_matches_0_4_T_4, _age_matches_0_4_T_5)
[5620] FIRRTL:371992 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_4_T_7 = mux(_age_matches_0_4_T, _age_matches_0_4_T_3, _age_matches_0_4_T_6)
[5621] FIRRTL:371993 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][4], _age_matches_0_4_T_7
[5623] FIRRTL:371995 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_6, stq_uop[5]
[5626] FIRRTL:371998 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_75 = eq(s_uop_6.mem_size, UInt<1>(0h0))
[5627] FIRRTL:371999 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_76 = bits(stq_addr[5].bits, 2, 0)
[5628] FIRRTL:372000 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_77 = dshl(UInt<8>(0h1), _write_mask_mask_T_76)
[5629] FIRRTL:372001 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_78 = eq(s_uop_6.mem_size, UInt<1>(0h1))
[5630] FIRRTL:372002 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_79 = bits(stq_addr[5].bits, 2, 1)
[5631] FIRRTL:372003 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_80 = dshl(_write_mask_mask_T_79, UInt<1>(0h1))
[5632] FIRRTL:372004 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_81 = dshl(UInt<8>(0h3), _write_mask_mask_T_80)
[5633] FIRRTL:372005 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_82 = eq(s_uop_6.mem_size, UInt<2>(0h2))
[5634] FIRRTL:372006 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_83 = bits(stq_addr[5].bits, 2, 2)
[5635] FIRRTL:372007 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_84 = mux(_write_mask_mask_T_83, UInt<8>(0hf0), UInt<8>(0hf))
[5636] FIRRTL:372008 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_85 = eq(s_uop_6.mem_size, UInt<2>(0h3))
[5637] FIRRTL:372009 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_86 = mux(_write_mask_mask_T_85, UInt<8>(0hff), UInt<8>(0hff))
[5638] FIRRTL:372010 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_87 = mux(_write_mask_mask_T_82, _write_mask_mask_T_84, _write_mask_mask_T_86)
[5639] FIRRTL:372011 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_88 = mux(_write_mask_mask_T_78, _write_mask_mask_T_81, _write_mask_mask_T_87)
[5640] FIRRTL:372012 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_89 = mux(_write_mask_mask_T_75, _write_mask_mask_T_77, _write_mask_mask_T_88)
[5641] FIRRTL:372013 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_5, _write_mask_mask_T_89
[5642] FIRRTL:372014 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_67 = eq(s_uop_6.is_amo, UInt<1>(0h0))
[5643] FIRRTL:372015 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_68 = and(stq_addr[5].valid, _dword_addr_matches_T_67)
[5644] FIRRTL:372016 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_69 = eq(stq_addr_is_virtual[5], UInt<1>(0h0))
[5645] FIRRTL:372017 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_70 = and(_dword_addr_matches_T_68, _dword_addr_matches_T_69)
[5646] FIRRTL:372018 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_71 = bits(stq_addr[5].bits, 31, 3)
[5647] FIRRTL:372019 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_72 = bits(lcam_addr[0], 31, 3)
[5648] FIRRTL:372020 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_73 = eq(_dword_addr_matches_T_71, _dword_addr_matches_T_72)
[5649] FIRRTL:372021 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_13 = and(_dword_addr_matches_T_70, _dword_addr_matches_T_73)
[5650] FIRRTL:372022 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_5 = and(lcam_mask[0], write_mask_5)
[5651] FIRRTL:372023 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_5_T = neq(mask_union_5, UInt<1>(0h0))
[5652] FIRRTL:372024 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_5_T_1 = and(_addr_matches_0_5_T, dword_addr_matches_13)
[5653] FIRRTL:372025 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][5], _addr_matches_0_5_T_1
[5689] FIRRTL:372061 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_5_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5691] FIRRTL:372063 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_5_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5692] FIRRTL:372064 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_5_T = eq(age_matches_0_5_head_carry, age_matches_0_5_tail_carry)
[5693] FIRRTL:372065 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_5_T_1 = geq(UInt<3>(0h5), age_matches_0_5_real_head_idx)
[5694] FIRRTL:372066 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_5_T_2 = lt(UInt<3>(0h5), age_matches_0_5_real_tail_idx)
[5695] FIRRTL:372067 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_5_T_3 = and(_age_matches_0_5_T_1, _age_matches_0_5_T_2)
[5696] FIRRTL:372068 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_5_T_4 = geq(UInt<3>(0h5), age_matches_0_5_real_head_idx)
[5697] FIRRTL:372069 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_5_T_5 = lt(UInt<3>(0h5), age_matches_0_5_real_tail_idx)
[5698] FIRRTL:372070 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_5_T_6 = or(_age_matches_0_5_T_4, _age_matches_0_5_T_5)
[5699] FIRRTL:372071 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_5_T_7 = mux(_age_matches_0_5_T, _age_matches_0_5_T_3, _age_matches_0_5_T_6)
[5700] FIRRTL:372072 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][5], _age_matches_0_5_T_7
[5702] FIRRTL:372074 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_7, stq_uop[6]
[5705] FIRRTL:372077 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_90 = eq(s_uop_7.mem_size, UInt<1>(0h0))
[5706] FIRRTL:372078 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_91 = bits(stq_addr[6].bits, 2, 0)
[5707] FIRRTL:372079 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_92 = dshl(UInt<8>(0h1), _write_mask_mask_T_91)
[5708] FIRRTL:372080 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_93 = eq(s_uop_7.mem_size, UInt<1>(0h1))
[5709] FIRRTL:372081 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_94 = bits(stq_addr[6].bits, 2, 1)
[5710] FIRRTL:372082 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_95 = dshl(_write_mask_mask_T_94, UInt<1>(0h1))
[5711] FIRRTL:372083 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_96 = dshl(UInt<8>(0h3), _write_mask_mask_T_95)
[5712] FIRRTL:372084 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_97 = eq(s_uop_7.mem_size, UInt<2>(0h2))
[5713] FIRRTL:372085 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_98 = bits(stq_addr[6].bits, 2, 2)
[5714] FIRRTL:372086 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_99 = mux(_write_mask_mask_T_98, UInt<8>(0hf0), UInt<8>(0hf))
[5715] FIRRTL:372087 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_100 = eq(s_uop_7.mem_size, UInt<2>(0h3))
[5716] FIRRTL:372088 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_101 = mux(_write_mask_mask_T_100, UInt<8>(0hff), UInt<8>(0hff))
[5717] FIRRTL:372089 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_102 = mux(_write_mask_mask_T_97, _write_mask_mask_T_99, _write_mask_mask_T_101)
[5718] FIRRTL:372090 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_103 = mux(_write_mask_mask_T_93, _write_mask_mask_T_96, _write_mask_mask_T_102)
[5719] FIRRTL:372091 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_104 = mux(_write_mask_mask_T_90, _write_mask_mask_T_92, _write_mask_mask_T_103)
[5720] FIRRTL:372092 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_6, _write_mask_mask_T_104
[5721] FIRRTL:372093 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_74 = eq(s_uop_7.is_amo, UInt<1>(0h0))
[5722] FIRRTL:372094 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_75 = and(stq_addr[6].valid, _dword_addr_matches_T_74)
[5723] FIRRTL:372095 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_76 = eq(stq_addr_is_virtual[6], UInt<1>(0h0))
[5724] FIRRTL:372096 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_77 = and(_dword_addr_matches_T_75, _dword_addr_matches_T_76)
[5725] FIRRTL:372097 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_78 = bits(stq_addr[6].bits, 31, 3)
[5726] FIRRTL:372098 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_79 = bits(lcam_addr[0], 31, 3)
[5727] FIRRTL:372099 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_80 = eq(_dword_addr_matches_T_78, _dword_addr_matches_T_79)
[5728] FIRRTL:372100 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_14 = and(_dword_addr_matches_T_77, _dword_addr_matches_T_80)
[5729] FIRRTL:372101 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_6 = and(lcam_mask[0], write_mask_6)
[5730] FIRRTL:372102 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_6_T = neq(mask_union_6, UInt<1>(0h0))
[5731] FIRRTL:372103 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_6_T_1 = and(_addr_matches_0_6_T, dword_addr_matches_14)
[5732] FIRRTL:372104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][6], _addr_matches_0_6_T_1
[5768] FIRRTL:372140 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_6_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5770] FIRRTL:372142 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_6_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5771] FIRRTL:372143 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_6_T = eq(age_matches_0_6_head_carry, age_matches_0_6_tail_carry)
[5772] FIRRTL:372144 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_6_T_1 = geq(UInt<3>(0h6), age_matches_0_6_real_head_idx)
[5773] FIRRTL:372145 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_6_T_2 = lt(UInt<3>(0h6), age_matches_0_6_real_tail_idx)
[5774] FIRRTL:372146 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_6_T_3 = and(_age_matches_0_6_T_1, _age_matches_0_6_T_2)
[5775] FIRRTL:372147 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_6_T_4 = geq(UInt<3>(0h6), age_matches_0_6_real_head_idx)
[5776] FIRRTL:372148 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_6_T_5 = lt(UInt<3>(0h6), age_matches_0_6_real_tail_idx)
[5777] FIRRTL:372149 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_6_T_6 = or(_age_matches_0_6_T_4, _age_matches_0_6_T_5)
[5778] FIRRTL:372150 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_6_T_7 = mux(_age_matches_0_6_T, _age_matches_0_6_T_3, _age_matches_0_6_T_6)
[5779] FIRRTL:372151 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][6], _age_matches_0_6_T_7
[5781] FIRRTL:372153 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1337:37 KIND:connect :: connect s_uop_8, stq_uop[7]
[5784] FIRRTL:372156 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:26 KIND:node :: node _write_mask_mask_T_105 = eq(s_uop_8.mem_size, UInt<1>(0h0))
[5785] FIRRTL:372157 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:55 KIND:node :: node _write_mask_mask_T_106 = bits(stq_addr[7].bits, 2, 0)
[5786] FIRRTL:372158 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1978:48 KIND:node :: node _write_mask_mask_T_107 = dshl(UInt<8>(0h1), _write_mask_mask_T_106)
[5787] FIRRTL:372159 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:26 KIND:node :: node _write_mask_mask_T_108 = eq(s_uop_8.mem_size, UInt<1>(0h1))
[5788] FIRRTL:372160 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:56 KIND:node :: node _write_mask_mask_T_109 = bits(stq_addr[7].bits, 2, 1)
[5789] FIRRTL:372161 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:62 KIND:node :: node _write_mask_mask_T_110 = dshl(_write_mask_mask_T_109, UInt<1>(0h1))
[5790] FIRRTL:372162 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1979:48 KIND:node :: node _write_mask_mask_T_111 = dshl(UInt<8>(0h3), _write_mask_mask_T_110)
[5791] FIRRTL:372163 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:26 KIND:node :: node _write_mask_mask_T_112 = eq(s_uop_8.mem_size, UInt<2>(0h2))
[5792] FIRRTL:372164 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:46 KIND:node :: node _write_mask_mask_T_113 = bits(stq_addr[7].bits, 2, 2)
[5793] FIRRTL:372165 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1980:41 KIND:node :: node _write_mask_mask_T_114 = mux(_write_mask_mask_T_113, UInt<8>(0hf0), UInt<8>(0hf))
[5794] FIRRTL:372166 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1981:26 KIND:node :: node _write_mask_mask_T_115 = eq(s_uop_8.mem_size, UInt<2>(0h3))
[5795] FIRRTL:372167 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_116 = mux(_write_mask_mask_T_115, UInt<8>(0hff), UInt<8>(0hff))
[5796] FIRRTL:372168 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_117 = mux(_write_mask_mask_T_112, _write_mask_mask_T_114, _write_mask_mask_T_116)
[5797] FIRRTL:372169 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_118 = mux(_write_mask_mask_T_108, _write_mask_mask_T_111, _write_mask_mask_T_117)
[5798] FIRRTL:372170 SRC:src/main/scala/chisel3/util/Mux.scala:126:16 KIND:node :: node _write_mask_mask_T_119 = mux(_write_mask_mask_T_105, _write_mask_mask_T_107, _write_mask_mask_T_118)
[5799] FIRRTL:372171 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1977:12 KIND:connect :: connect write_mask_7, _write_mask_mask_T_119
[5800] FIRRTL:372172 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:33 KIND:node :: node _dword_addr_matches_T_81 = eq(s_uop_8.is_amo, UInt<1>(0h0))
[5801] FIRRTL:372173 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1342:52 KIND:node :: node _dword_addr_matches_T_82 = and(stq_addr[7].valid, _dword_addr_matches_T_81)
[5802] FIRRTL:372174 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:33 KIND:node :: node _dword_addr_matches_T_83 = eq(stq_addr_is_virtual[7], UInt<1>(0h0))
[5803] FIRRTL:372175 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1343:52 KIND:node :: node _dword_addr_matches_T_84 = and(_dword_addr_matches_T_82, _dword_addr_matches_T_83)
[5804] FIRRTL:372176 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:45 KIND:node :: node _dword_addr_matches_T_85 = bits(stq_addr[7].bits, 31, 3)
[5805] FIRRTL:372177 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:81 KIND:node :: node _dword_addr_matches_T_86 = bits(lcam_addr[0], 31, 3)
[5806] FIRRTL:372178 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1345:65 KIND:node :: node _dword_addr_matches_T_87 = eq(_dword_addr_matches_T_85, _dword_addr_matches_T_86)
[5807] FIRRTL:372179 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1344:52 KIND:node :: node dword_addr_matches_15 = and(_dword_addr_matches_T_84, _dword_addr_matches_T_87)
[5808] FIRRTL:372180 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1346:37 KIND:node :: node mask_union_7 = and(lcam_mask[0], write_mask_7)
[5809] FIRRTL:372181 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:44 KIND:node :: node _addr_matches_0_7_T = neq(mask_union_7, UInt<1>(0h0))
[5810] FIRRTL:372182 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:53 KIND:node :: node _addr_matches_0_7_T_1 = and(_addr_matches_0_7_T, dword_addr_matches_15)
[5811] FIRRTL:372183 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1348:29 KIND:connect :: connect addr_matches[0][7], _addr_matches_0_7_T_1
[5847] FIRRTL:372219 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age_matches_0_7_real_tail_idx = bits(lcam_next_stq_idx[0], 2, 0)
[5849] FIRRTL:372221 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age_matches_0_7_tail_carry = bits(lcam_next_stq_idx[0], 3, 3)
[5850] FIRRTL:372222 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:20 KIND:node :: node _age_matches_0_7_T = eq(age_matches_0_7_head_carry, age_matches_0_7_tail_carry)
[5851] FIRRTL:372223 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:21 KIND:node :: node _age_matches_0_7_T_1 = geq(UInt<3>(0h7), age_matches_0_7_real_head_idx)
[5852] FIRRTL:372224 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:55 KIND:node :: node _age_matches_0_7_T_2 = lt(UInt<3>(0h7), age_matches_0_7_real_tail_idx)
[5853] FIRRTL:372225 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2166:39 KIND:node :: node _age_matches_0_7_T_3 = and(_age_matches_0_7_T_1, _age_matches_0_7_T_2)
[5854] FIRRTL:372226 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:21 KIND:node :: node _age_matches_0_7_T_4 = geq(UInt<3>(0h7), age_matches_0_7_real_head_idx)
[5855] FIRRTL:372227 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:55 KIND:node :: node _age_matches_0_7_T_5 = lt(UInt<3>(0h7), age_matches_0_7_real_tail_idx)
[5856] FIRRTL:372228 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2167:39 KIND:node :: node _age_matches_0_7_T_6 = or(_age_matches_0_7_T_4, _age_matches_0_7_T_5)
[5857] FIRRTL:372229 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2165:8 KIND:node :: node _age_matches_0_7_T_7 = mux(_age_matches_0_7_T, _age_matches_0_7_T_3, _age_matches_0_7_T_6)
[5858] FIRRTL:372230 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1358:29 KIND:connect :: connect age_matches[0][7], _age_matches_0_7_T_7
[5859] FIRRTL:372231 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_lo_lo = cat(stq_valid[1], stq_valid[0])
[5860] FIRRTL:372232 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_lo_hi = cat(stq_valid[3], stq_valid[2])
[5861] FIRRTL:372233 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_lo = cat(fast_stq_valids_lo_hi, fast_stq_valids_lo_lo)
[5862] FIRRTL:372234 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_hi_lo = cat(stq_valid[5], stq_valid[4])
[5863] FIRRTL:372235 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_hi_hi = cat(stq_valid[7], stq_valid[6])
[5864] FIRRTL:372236 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids_hi = cat(fast_stq_valids_hi_hi, fast_stq_valids_hi_lo)
[5865] FIRRTL:372237 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1363:35 KIND:node :: node fast_stq_valids = cat(fast_stq_valids_hi, fast_stq_valids_lo)
[5866] FIRRTL:372238 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_lo_lo = cat(addr_matches[0][1], addr_matches[0][0])
[5867] FIRRTL:372239 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_lo_hi = cat(addr_matches[0][3], addr_matches[0][2])
[5868] FIRRTL:372240 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_lo = cat(ldst_addr_matches_0_lo_hi, ldst_addr_matches_0_lo_lo)
[5869] FIRRTL:372241 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_hi_lo = cat(addr_matches[0][5], addr_matches[0][4])
[5870] FIRRTL:372242 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_hi_hi = cat(addr_matches[0][7], addr_matches[0][6])
[5871] FIRRTL:372243 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node ldst_addr_matches_0_hi = cat(ldst_addr_matches_0_hi_hi, ldst_addr_matches_0_hi_lo)
[5872] FIRRTL:372244 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:49 KIND:node :: node _ldst_addr_matches_0_T = cat(ldst_addr_matches_0_hi, ldst_addr_matches_0_lo)
[5873] FIRRTL:372245 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_lo_lo_1 = cat(age_matches[0][1], age_matches[0][0])
[5874] FIRRTL:372246 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_lo_hi_1 = cat(age_matches[0][3], age_matches[0][2])
[5875] FIRRTL:372247 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_lo_1 = cat(ldst_addr_matches_0_lo_hi_1, ldst_addr_matches_0_lo_lo_1)
[5876] FIRRTL:372248 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_hi_lo_1 = cat(age_matches[0][5], age_matches[0][4])
[5877] FIRRTL:372249 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_hi_hi_1 = cat(age_matches[0][7], age_matches[0][6])
[5878] FIRRTL:372250 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node ldst_addr_matches_0_hi_1 = cat(ldst_addr_matches_0_hi_hi_1, ldst_addr_matches_0_hi_lo_1)
[5879] FIRRTL:372251 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:73 KIND:node :: node _ldst_addr_matches_0_T_1 = cat(ldst_addr_matches_0_hi_1, ldst_addr_matches_0_lo_1)
[5880] FIRRTL:372252 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:56 KIND:node :: node _ldst_addr_matches_0_T_2 = and(_ldst_addr_matches_0_T, _ldst_addr_matches_0_T_1)
[5881] FIRRTL:372253 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:81 KIND:node :: node _ldst_addr_matches_0_T_3 = and(_ldst_addr_matches_0_T_2, fast_stq_valids)
[5882] FIRRTL:372254 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1366:29 KIND:connect :: connect ldst_addr_matches[0], _ldst_addr_matches_0_T_3
[5918] FIRRTL:372290 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T = or(stq_uop[0].is_fence, stq_uop[0].is_amo)
[5919] FIRRTL:372291 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_1 = or(stq_uop[1].is_fence, stq_uop[1].is_amo)
[5920] FIRRTL:372292 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_2 = or(stq_uop[2].is_fence, stq_uop[2].is_amo)
[5921] FIRRTL:372293 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_3 = or(stq_uop[3].is_fence, stq_uop[3].is_amo)
[5922] FIRRTL:372294 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_4 = or(stq_uop[4].is_fence, stq_uop[4].is_amo)
[5923] FIRRTL:372295 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_5 = or(stq_uop[5].is_fence, stq_uop[5].is_amo)
[5924] FIRRTL:372296 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_6 = or(stq_uop[6].is_fence, stq_uop[6].is_amo)
[5925] FIRRTL:372297 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:54 KIND:node :: node _stq_amos_T_7 = or(stq_uop[7].is_fence, stq_uop[7].is_amo)
[5927] FIRRTL:372299 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[0], _stq_amos_T
[5928] FIRRTL:372300 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[1], _stq_amos_T_1
[5929] FIRRTL:372301 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[2], _stq_amos_T_2
[5930] FIRRTL:372302 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[3], _stq_amos_T_3
[5931] FIRRTL:372303 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[4], _stq_amos_T_4
[5932] FIRRTL:372304 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[5], _stq_amos_T_5
[5933] FIRRTL:372305 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[6], _stq_amos_T_6
[5934] FIRRTL:372306 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1371:25 KIND:connect :: connect stq_amos[7], _stq_amos_T_7
[5935] FIRRTL:372307 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_lo_lo = cat(stq_amos[1], stq_amos[0])
[5936] FIRRTL:372308 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_lo_hi = cat(stq_amos[3], stq_amos[2])
[5937] FIRRTL:372309 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_lo = cat(has_older_amo_lo_hi, has_older_amo_lo_lo)
[5938] FIRRTL:372310 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_hi_lo = cat(stq_amos[5], stq_amos[4])
[5939] FIRRTL:372311 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_hi_hi = cat(stq_amos[7], stq_amos[6])
[5940] FIRRTL:372312 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node has_older_amo_hi = cat(has_older_amo_hi_hi, has_older_amo_hi_lo)
[5941] FIRRTL:372313 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:35 KIND:node :: node _has_older_amo_T = cat(has_older_amo_hi, has_older_amo_lo)
[5942] FIRRTL:372314 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_lo_lo_1 = cat(age_matches[0][1], age_matches[0][0])
[5943] FIRRTL:372315 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_lo_hi_1 = cat(age_matches[0][3], age_matches[0][2])
[5944] FIRRTL:372316 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_lo_1 = cat(has_older_amo_lo_hi_1, has_older_amo_lo_lo_1)
[5945] FIRRTL:372317 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_hi_lo_1 = cat(age_matches[0][5], age_matches[0][4])
[5946] FIRRTL:372318 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_hi_hi_1 = cat(age_matches[0][7], age_matches[0][6])
[5947] FIRRTL:372319 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node has_older_amo_hi_1 = cat(has_older_amo_hi_hi_1, has_older_amo_hi_lo_1)
[5948] FIRRTL:372320 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:59 KIND:node :: node _has_older_amo_T_1 = cat(has_older_amo_hi_1, has_older_amo_lo_1)
[5949] FIRRTL:372321 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:42 KIND:node :: node _has_older_amo_T_2 = and(_has_older_amo_T, _has_older_amo_T_1)
[5950] FIRRTL:372322 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1373:67 KIND:node :: node has_older_amo = neq(_has_older_amo_T_2, UInt<1>(0h0))
[5951] FIRRTL:372323 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1375:70 KIND:node :: node _T_865 = neq(ldst_addr_matches[0], UInt<1>(0h0))
[5952] FIRRTL:372324 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1375:45 KIND:node :: node _T_866 = or(has_older_amo, _T_865)
[5953] FIRRTL:372325 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1375:27 KIND:node :: node _T_867 = and(do_ld_search[0], _T_866)
[5954] FIRRTL:372326 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1375:81 KIND:when :: when _T_867 :
[5965] FIRRTL:372337 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1380:28 KIND:when :: when has_older_amo :
[5966] FIRRTL:372338 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1381:25 KIND:connect :: connect kill_forward[0], UInt<1>(0h1)
[5999] FIRRTL:372371 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1403:63 KIND:node :: node _wb_ldst_forward_valid_0_T_3 = eq(kill_forward[0], UInt<1>(0h0))
[6000] FIRRTL:372372 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1403:60 KIND:node :: node _wb_ldst_forward_valid_0_T_4 = and(can_forward[0], _wb_ldst_forward_valid_0_T_3)
[6001] FIRRTL:372373 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1403:80 KIND:node :: node _wb_ldst_forward_valid_0_T_5 = and(_wb_ldst_forward_valid_0_T_4, do_ld_search[0])
[6003] FIRRTL:372375 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1403:44 KIND:connect :: connect wb_ldst_forward_valid_0_REG, _wb_ldst_forward_valid_0_T_5
[6005] FIRRTL:372377 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _wb_ldst_forward_valid_0_T_7 = and(io.core.brupdate.b1.mispredict_mask, lcam_uop[0].br_mask)
[6006] FIRRTL:372378 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _wb_ldst_forward_valid_0_T_8 = neq(_wb_ldst_forward_valid_0_T_7, UInt<1>(0h0))
[6007] FIRRTL:372379 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _wb_ldst_forward_valid_0_T_9 = or(_wb_ldst_forward_valid_0_T_8, io.core.exception)
[6009] FIRRTL:372381 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1404:45 KIND:connect :: connect wb_ldst_forward_valid_0_REG_1, _wb_ldst_forward_valid_0_T_9
[6212] FIRRTL:372584 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1482:47 KIND:connect :: connect wakeupArbs_0_io_in_1_valid_REG, dmem_req_fire[0]
[6213] FIRRTL:372585 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1481:69 KIND:node :: node _wakeupArbs_0_io_in_1_valid_T = and(fired_load_agen_exec[0], wakeupArbs_0_io_in_1_valid_REG)
[6214] FIRRTL:372586 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1483:40 KIND:node :: node _wakeupArbs_0_io_in_1_valid_T_1 = eq(io.dmem.s1_nack_advisory[0], UInt<1>(0h0))
[6215] FIRRTL:372587 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1482:69 KIND:node :: node _wakeupArbs_0_io_in_1_valid_T_2 = and(_wakeupArbs_0_io_in_1_valid_T, _wakeupArbs_0_io_in_1_valid_T_1)
[6216] FIRRTL:372588 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1484:40 KIND:node :: node _wakeupArbs_0_io_in_1_valid_T_3 = eq(mem_incoming_uop[0].fp_val, UInt<1>(0h0))
[6217] FIRRTL:372589 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1483:69 KIND:node :: node _wakeupArbs_0_io_in_1_valid_T_4 = and(_wakeupArbs_0_io_in_1_valid_T_2, _wakeupArbs_0_io_in_1_valid_T_3)
[6218] FIRRTL:372590 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1481:36 KIND:connect :: connect wakeupArbs_0.io.in[1].valid, _wakeupArbs_0_io_in_1_valid_T_4
[6302] FIRRTL:372674 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1485:39 KIND:connect :: connect wakeupArbs_0.io.in[1].bits.uop.br_mask, mem_incoming_uop[0].br_mask
[6335] FIRRTL:372707 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1505:20 KIND:connect :: connect iresp[0].valid, UInt<1>(0h0)
[6451] FIRRTL:372823 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1507:20 KIND:connect :: connect fresp[0].valid, UInt<1>(0h0)
[6587] FIRRTL:372959 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _dmem_resp_fired_WIRE[0], UInt<1>(0h0)
[6589] FIRRTL:372961 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1521:33 KIND:connect :: connect dmem_resp_fired, _dmem_resp_fired_WIRE
[6591] FIRRTL:372963 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _w1_valid_T = and(wakeupArbs_0.io.in[1].ready, wakeupArbs_0.io.in[1].valid)
[6592] FIRRTL:372964 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _w1_valid_T_1 = and(io.core.brupdate.b1.mispredict_mask, wakeupArbs_0.io.in[1].bits.uop.br_mask)
[6593] FIRRTL:372965 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _w1_valid_T_2 = neq(_w1_valid_T_1, UInt<1>(0h0))
[6594] FIRRTL:372966 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _w1_valid_T_3 = or(_w1_valid_T_2, io.core.exception)
[6595] FIRRTL:372967 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1524:48 KIND:node :: node _w1_valid_T_4 = eq(_w1_valid_T_3, UInt<1>(0h0))
[6596] FIRRTL:372968 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1524:45 KIND:node :: node _w1_valid_T_5 = and(_w1_valid_T, _w1_valid_T_4)
[6597] FIRRTL:372969 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1524:14 KIND:connect :: connect w1.valid, _w1_valid_T_5
[6732] FIRRTL:373104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1535:24 KIND:connect :: connect wb_spec_wakeups[0], w1
[6927] FIRRTL:373299 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1561:32 KIND:node :: node _io_dmem_ll_resp_ready_T = eq(io.dmem.resp[0].valid, UInt<1>(0h0))
[6928] FIRRTL:373300 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1561:58 KIND:node :: node _io_dmem_ll_resp_ready_T_1 = eq(wb_spec_wakeups[0].valid, UInt<1>(0h0))
[6929] FIRRTL:373301 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1561:55 KIND:node :: node _io_dmem_ll_resp_ready_T_2 = and(_io_dmem_ll_resp_ready_T, _io_dmem_ll_resp_ready_T_1)
[6930] FIRRTL:373302 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1561:29 KIND:connect :: connect io.dmem.ll_resp.ready, _io_dmem_ll_resp_ready_T_2
[6931] FIRRTL:373303 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_922 = and(io.dmem.ll_resp.ready, io.dmem.ll_resp.valid)
[6932] FIRRTL:373304 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1563:57 KIND:node :: node _T_923 = and(UInt<1>(0h1), _T_922)
[6933] FIRRTL:373305 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1563:33 KIND:node :: node _T_924 = or(io.dmem.resp[0].valid, _T_923)
[6934] FIRRTL:373306 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1563:83 KIND:when :: when _T_924 :
[6935] FIRRTL:373307 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1564:32 KIND:when :: when resp.uop.uses_ldq :
[6944] FIRRTL:373316 SRC:<no-source-locator> KIND:node :: node _uop_T = bits(resp.uop.ldq_idx, 2, 0)
[6947] FIRRTL:373319 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1568:40 KIND:node :: node send_iresp = eq(uop.dst_rtype, UInt<2>(0h0))
[6948] FIRRTL:373320 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1569:40 KIND:node :: node send_fresp = eq(uop.dst_rtype, UInt<2>(0h1))
[6951] FIRRTL:373323 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1573:28 KIND:connect :: connect iresp[0].valid, send_iresp
[6953] FIRRTL:373325 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1578:28 KIND:connect :: connect fresp[0].valid, send_fresp
[6963] FIRRTL:373335 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1582:28 KIND:connect :: connect dmem_resp_fired[0], UInt<1>(0h1)
[6964] FIRRTL:373336 SRC:<no-source-locator> KIND:node :: node _T_933 = bits(resp.uop.ldq_idx, 2, 0)
[6965] FIRRTL:373337 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1584:54 KIND:node :: node _ldq_will_succeed_T = or(iresp[0].valid, fresp[0].valid)
[6966] FIRRTL:373338 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1584:36 KIND:connect :: connect ldq_will_succeed[_T_933], _ldq_will_succeed_T
[6974] FIRRTL:373346 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1595:7 KIND:when :: when resp.uop.uses_stq :
[6985] FIRRTL:373357 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1598:28 KIND:connect :: connect dmem_resp_fired[0], UInt<1>(0h1)
[6986] FIRRTL:373358 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1599:28 KIND:connect :: connect iresp[0].valid, UInt<1>(0h1)
[6996] FIRRTL:373368 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1613:39 KIND:when :: when io.dmem.store_ack[0].valid :
[6997] FIRRTL:373369 SRC:<no-source-locator> KIND:node :: node _T_941 = bits(io.dmem.store_ack[0].bits.uop.stq_idx, 2, 0)
[6998] FIRRTL:373370 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1614:60 KIND:connect :: connect stq_succeeded[_T_941], UInt<1>(0h1)
[6999] FIRRTL:373371 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1618:30 KIND:node :: node _T_942 = and(dmem_resp_fired[0], wb_ldst_forward_valid[0])
[7002] FIRRTL:373374 SRC:<no-source-locator> KIND:else :: else :
[7003] FIRRTL:373375 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1622:18 KIND:node :: node _T_943 = eq(dmem_resp_fired[0], UInt<1>(0h0))
[7004] FIRRTL:373376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1622:38 KIND:node :: node _T_944 = and(_T_943, wb_ldst_forward_valid[0])
[7005] FIRRTL:373377 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1623:5 KIND:when :: when _T_944 :
[7051] FIRRTL:373423 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1643:48 KIND:node :: node _iresp_0_valid_T = eq(wb_ldst_forward_e[0].uop.dst_rtype, UInt<2>(0h0))
[7052] FIRRTL:373424 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1643:22 KIND:connect :: connect iresp[0].valid, _iresp_0_valid_T
[7053] FIRRTL:373425 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1644:48 KIND:node :: node _fresp_0_valid_T = eq(wb_ldst_forward_e[0].uop.dst_rtype, UInt<2>(0h1))
[7054] FIRRTL:373426 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1644:22 KIND:connect :: connect fresp[0].valid, _fresp_0_valid_T
[7143] FIRRTL:373515 SRC:<no-source-locator> KIND:node :: node _T_963 = bits(wb_ldst_forward_ldq_idx[0], 2, 0)
[7144] FIRRTL:373516 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1650:34 KIND:connect :: connect ldq_will_succeed[_T_963], UInt<1>(0h1)
[7566] FIRRTL:373938 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[0] :
[7568] FIRRTL:373940 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_1, stq_uop[0]
[7569] FIRRTL:373941 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_0_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7570] FIRRTL:373942 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_0_br_mask_T_1 = and(uop_1.br_mask, _stq_uop_0_br_mask_T)
[7571] FIRRTL:373943 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[0].br_mask, _stq_uop_0_br_mask_T_1
[7572] FIRRTL:373944 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_971 = and(io.core.brupdate.b1.mispredict_mask, uop_1.br_mask)
[7573] FIRRTL:373945 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_972 = neq(_T_971, UInt<1>(0h0))
[7574] FIRRTL:373946 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_973 = or(_T_972, UInt<1>(0h0))
[7575] FIRRTL:373947 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_973 :
[7576] FIRRTL:373948 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[0], UInt<1>(0h0)
[7577] FIRRTL:373949 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[0].valid, UInt<1>(0h0)
[7592] FIRRTL:373964 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[1] :
[7594] FIRRTL:373966 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_2, stq_uop[1]
[7595] FIRRTL:373967 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_1_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7596] FIRRTL:373968 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_1_br_mask_T_1 = and(uop_2.br_mask, _stq_uop_1_br_mask_T)
[7597] FIRRTL:373969 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[1].br_mask, _stq_uop_1_br_mask_T_1
[7598] FIRRTL:373970 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_983 = and(io.core.brupdate.b1.mispredict_mask, uop_2.br_mask)
[7599] FIRRTL:373971 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_984 = neq(_T_983, UInt<1>(0h0))
[7600] FIRRTL:373972 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_985 = or(_T_984, UInt<1>(0h0))
[7601] FIRRTL:373973 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_985 :
[7602] FIRRTL:373974 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[1], UInt<1>(0h0)
[7603] FIRRTL:373975 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[1].valid, UInt<1>(0h0)
[7618] FIRRTL:373990 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[2] :
[7620] FIRRTL:373992 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_3, stq_uop[2]
[7621] FIRRTL:373993 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_2_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7622] FIRRTL:373994 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_2_br_mask_T_1 = and(uop_3.br_mask, _stq_uop_2_br_mask_T)
[7623] FIRRTL:373995 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[2].br_mask, _stq_uop_2_br_mask_T_1
[7624] FIRRTL:373996 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_995 = and(io.core.brupdate.b1.mispredict_mask, uop_3.br_mask)
[7625] FIRRTL:373997 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_996 = neq(_T_995, UInt<1>(0h0))
[7626] FIRRTL:373998 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_997 = or(_T_996, UInt<1>(0h0))
[7627] FIRRTL:373999 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_997 :
[7628] FIRRTL:374000 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[2], UInt<1>(0h0)
[7629] FIRRTL:374001 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[2].valid, UInt<1>(0h0)
[7644] FIRRTL:374016 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[3] :
[7646] FIRRTL:374018 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_4, stq_uop[3]
[7647] FIRRTL:374019 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_3_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7648] FIRRTL:374020 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_3_br_mask_T_1 = and(uop_4.br_mask, _stq_uop_3_br_mask_T)
[7649] FIRRTL:374021 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[3].br_mask, _stq_uop_3_br_mask_T_1
[7650] FIRRTL:374022 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1007 = and(io.core.brupdate.b1.mispredict_mask, uop_4.br_mask)
[7651] FIRRTL:374023 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1008 = neq(_T_1007, UInt<1>(0h0))
[7652] FIRRTL:374024 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1009 = or(_T_1008, UInt<1>(0h0))
[7653] FIRRTL:374025 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_1009 :
[7654] FIRRTL:374026 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[3], UInt<1>(0h0)
[7655] FIRRTL:374027 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[3].valid, UInt<1>(0h0)
[7670] FIRRTL:374042 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[4] :
[7672] FIRRTL:374044 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_5, stq_uop[4]
[7673] FIRRTL:374045 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_4_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7674] FIRRTL:374046 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_4_br_mask_T_1 = and(uop_5.br_mask, _stq_uop_4_br_mask_T)
[7675] FIRRTL:374047 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[4].br_mask, _stq_uop_4_br_mask_T_1
[7676] FIRRTL:374048 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1019 = and(io.core.brupdate.b1.mispredict_mask, uop_5.br_mask)
[7677] FIRRTL:374049 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1020 = neq(_T_1019, UInt<1>(0h0))
[7678] FIRRTL:374050 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1021 = or(_T_1020, UInt<1>(0h0))
[7679] FIRRTL:374051 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_1021 :
[7680] FIRRTL:374052 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[4], UInt<1>(0h0)
[7681] FIRRTL:374053 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[4].valid, UInt<1>(0h0)
[7696] FIRRTL:374068 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[5] :
[7698] FIRRTL:374070 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_6, stq_uop[5]
[7699] FIRRTL:374071 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_5_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7700] FIRRTL:374072 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_5_br_mask_T_1 = and(uop_6.br_mask, _stq_uop_5_br_mask_T)
[7701] FIRRTL:374073 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[5].br_mask, _stq_uop_5_br_mask_T_1
[7702] FIRRTL:374074 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1031 = and(io.core.brupdate.b1.mispredict_mask, uop_6.br_mask)
[7703] FIRRTL:374075 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1032 = neq(_T_1031, UInt<1>(0h0))
[7704] FIRRTL:374076 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1033 = or(_T_1032, UInt<1>(0h0))
[7705] FIRRTL:374077 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_1033 :
[7706] FIRRTL:374078 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[5], UInt<1>(0h0)
[7707] FIRRTL:374079 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[5].valid, UInt<1>(0h0)
[7722] FIRRTL:374094 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[6] :
[7724] FIRRTL:374096 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_7, stq_uop[6]
[7725] FIRRTL:374097 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_6_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7726] FIRRTL:374098 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_6_br_mask_T_1 = and(uop_7.br_mask, _stq_uop_6_br_mask_T)
[7727] FIRRTL:374099 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[6].br_mask, _stq_uop_6_br_mask_T_1
[7728] FIRRTL:374100 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1043 = and(io.core.brupdate.b1.mispredict_mask, uop_7.br_mask)
[7729] FIRRTL:374101 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1044 = neq(_T_1043, UInt<1>(0h0))
[7730] FIRRTL:374102 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1045 = or(_T_1044, UInt<1>(0h0))
[7731] FIRRTL:374103 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_1045 :
[7732] FIRRTL:374104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[6], UInt<1>(0h0)
[7733] FIRRTL:374105 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[6].valid, UInt<1>(0h0)
[7748] FIRRTL:374120 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1702:5 KIND:when :: when stq_valid[7] :
[7750] FIRRTL:374122 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1703:25 KIND:connect :: connect uop_8, stq_uop[7]
[7751] FIRRTL:374123 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _stq_uop_7_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[7752] FIRRTL:374124 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _stq_uop_7_br_mask_T_1 = and(uop_8.br_mask, _stq_uop_7_br_mask_T)
[7753] FIRRTL:374125 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1704:26 KIND:connect :: connect stq_uop[7].br_mask, _stq_uop_7_br_mask_T_1
[7754] FIRRTL:374126 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1055 = and(io.core.brupdate.b1.mispredict_mask, uop_8.br_mask)
[7755] FIRRTL:374127 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1056 = neq(_T_1055, UInt<1>(0h0))
[7756] FIRRTL:374128 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1057 = or(_T_1056, UInt<1>(0h0))
[7757] FIRRTL:374129 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1707:7 KIND:when :: when _T_1057 :
[7758] FIRRTL:374130 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1708:28 KIND:connect :: connect stq_valid[7], UInt<1>(0h0)
[7759] FIRRTL:374131 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1709:28 KIND:connect :: connect stq_addr[7].valid, UInt<1>(0h0)
[7937] FIRRTL:374309 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1804:35 KIND:connect :: connect stq_valid[_T_1121], UInt<1>(0h0)
[7947] FIRRTL:374319 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1817:27 KIND:connect :: connect io.hellacache.req.ready, UInt<1>(0h0)
[8001] FIRRTL:374373 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1846:34 KIND:when :: when _T_1122 :
[8002] FIRRTL:374374 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1847:29 KIND:connect :: connect io.hellacache.req.ready, UInt<1>(0h1)
[8006] FIRRTL:374378 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1850:19 KIND:connect :: connect hella_state, UInt<3>(0h1)
[8012] FIRRTL:374384 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.ae.st, dtlb.io.resp[0].ae.st
[8013] FIRRTL:374385 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.ae.ld, dtlb.io.resp[0].ae.ld
[8014] FIRRTL:374386 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.gf.st, dtlb.io.resp[0].gf.st
[8015] FIRRTL:374387 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.gf.ld, dtlb.io.resp[0].gf.ld
[8016] FIRRTL:374388 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.pf.st, dtlb.io.resp[0].pf.st
[8017] FIRRTL:374389 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.pf.ld, dtlb.io.resp[0].pf.ld
[8018] FIRRTL:374390 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.ma.st, dtlb.io.resp[0].ma.st
[8019] FIRRTL:374391 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1856:16 KIND:connect :: connect hella_xcpt.ma.ld, dtlb.io.resp[0].ma.ld
[8020] FIRRTL:374392 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1858:34 KIND:when :: when io.hellacache.s1_kill :
[8021] FIRRTL:374393 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1859:41 KIND:node :: node _T_1125 = and(will_fire_hella_incoming[0], dmem_req_fire[0])
[8022] FIRRTL:374394 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1859:62 KIND:when :: when _T_1125 :
[8023] FIRRTL:374395 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1860:21 KIND:connect :: connect hella_state, UInt<3>(0h6)
[8024] FIRRTL:374396 SRC:<no-source-locator> KIND:else :: else :
[8025] FIRRTL:374397 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1862:21 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8026] FIRRTL:374398 SRC:<no-source-locator> KIND:else :: else :
[8027] FIRRTL:374399 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1864:46 KIND:node :: node _T_1126 = and(will_fire_hella_incoming[0], dmem_req_fire[0])
[8028] FIRRTL:374400 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1864:67 KIND:when :: when _T_1126 :
[8029] FIRRTL:374401 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1865:19 KIND:connect :: connect hella_state, UInt<3>(0h2)
[8030] FIRRTL:374402 SRC:<no-source-locator> KIND:else :: else :
[8031] FIRRTL:374403 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1867:19 KIND:connect :: connect hella_state, UInt<3>(0h3)
[8034] FIRRTL:374406 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1869:43 KIND:when :: when _T_1127 :
[8036] FIRRTL:374408 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1871:17 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8039] FIRRTL:374411 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1872:38 KIND:when :: when _T_1128 :
[8041] FIRRTL:374413 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node _T_1129 = cat(hella_xcpt.ae.ld, hella_xcpt.ae.st)
[8042] FIRRTL:374414 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node _T_1130 = cat(hella_xcpt.gf.ld, hella_xcpt.gf.st)
[8043] FIRRTL:374415 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node _T_1131 = cat(hella_xcpt.pf.ld, hella_xcpt.pf.st)
[8044] FIRRTL:374416 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node _T_1132 = cat(hella_xcpt.ma.ld, hella_xcpt.ma.st)
[8045] FIRRTL:374417 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node lo = cat(_T_1130, _T_1129)
[8046] FIRRTL:374418 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node hi = cat(_T_1132, _T_1131)
[8047] FIRRTL:374419 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:47 KIND:node :: node _T_1133 = cat(hi, lo)
[8048] FIRRTL:374420 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:54 KIND:node :: node _T_1134 = neq(_T_1133, UInt<1>(0h0))
[8049] FIRRTL:374421 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:33 KIND:node :: node _T_1135 = or(io.hellacache.s2_kill, _T_1134)
[8050] FIRRTL:374422 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1874:63 KIND:when :: when _T_1135 :
[8051] FIRRTL:374423 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1875:19 KIND:connect :: connect hella_state, UInt<3>(0h6)
[8052] FIRRTL:374424 SRC:<no-source-locator> KIND:else :: else :
[8053] FIRRTL:374425 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1877:19 KIND:connect :: connect hella_state, UInt<3>(0h4)
[8060] FIRRTL:374432 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1881:19 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8072] FIRRTL:374444 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1894:21 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8080] FIRRTL:374452 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1904:35 KIND:node :: node _T_1142 = and(io.dmem.nack[0].valid, io.dmem.nack[0].bits.is_hella)
[8081] FIRRTL:374453 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1904:69 KIND:when :: when _T_1142 :
[8082] FIRRTL:374454 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1905:21 KIND:connect :: connect hella_state, UInt<3>(0h5)
[8087] FIRRTL:374459 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1911:37 KIND:node :: node _T_1144 = and(will_fire_hella_wakeup[0], dmem_req_fire[0])
[8088] FIRRTL:374460 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1911:58 KIND:when :: when _T_1144 :
[8089] FIRRTL:374461 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1912:19 KIND:connect :: connect hella_state, UInt<3>(0h4)
[8090] FIRRTL:374462 SRC:<no-source-locator> KIND:else :: else :
[8091] FIRRTL:374463 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1914:28 KIND:node :: node _T_1145 = eq(hella_state, UInt<3>(0h6))
[8092] FIRRTL:374464 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1914:40 KIND:when :: when _T_1145 :
[8093] FIRRTL:374465 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_1146 = and(io.dmem.ll_resp.ready, io.dmem.ll_resp.valid)
[8094] FIRRTL:374466 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1915:32 KIND:node :: node _T_1147 = and(_T_1146, io.dmem.ll_resp.bits.is_hella)
[8095] FIRRTL:374467 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1915:66 KIND:when :: when _T_1147 :
[8096] FIRRTL:374468 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1916:19 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8097] FIRRTL:374469 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1919:35 KIND:node :: node _T_1148 = and(io.dmem.resp[0].valid, io.dmem.resp[0].bits.is_hella)
[8098] FIRRTL:374470 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1919:69 KIND:when :: when _T_1148 :
[8099] FIRRTL:374471 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1920:21 KIND:connect :: connect hella_state, UInt<3>(0h0)
[8111] FIRRTL:374483 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[0], UInt<1>(0h0)
[8112] FIRRTL:374484 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[1], UInt<1>(0h0)
[8113] FIRRTL:374485 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[2], UInt<1>(0h0)
[8114] FIRRTL:374486 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[3], UInt<1>(0h0)
[8115] FIRRTL:374487 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[4], UInt<1>(0h0)
[8116] FIRRTL:374488 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[5], UInt<1>(0h0)
[8117] FIRRTL:374489 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[6], UInt<1>(0h0)
[8118] FIRRTL:374490 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1942:32 KIND:connect :: connect stq_valid[7], UInt<1>(0h0)
[8121] FIRRTL:374493 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1152 = eq(stq_committed[0], UInt<1>(0h0))
[8122] FIRRTL:374494 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1153 = eq(stq_succeeded[0], UInt<1>(0h0))
[8123] FIRRTL:374495 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1154 = and(_T_1152, _T_1153)
[8124] FIRRTL:374496 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1154 :
[8125] FIRRTL:374497 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[0], UInt<1>(0h0)
[8126] FIRRTL:374498 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1155 = eq(stq_committed[1], UInt<1>(0h0))
[8127] FIRRTL:374499 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1156 = eq(stq_succeeded[1], UInt<1>(0h0))
[8128] FIRRTL:374500 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1157 = and(_T_1155, _T_1156)
[8129] FIRRTL:374501 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1157 :
[8130] FIRRTL:374502 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[1], UInt<1>(0h0)
[8131] FIRRTL:374503 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1158 = eq(stq_committed[2], UInt<1>(0h0))
[8132] FIRRTL:374504 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1159 = eq(stq_succeeded[2], UInt<1>(0h0))
[8133] FIRRTL:374505 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1160 = and(_T_1158, _T_1159)
[8134] FIRRTL:374506 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1160 :
[8135] FIRRTL:374507 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[2], UInt<1>(0h0)
[8136] FIRRTL:374508 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1161 = eq(stq_committed[3], UInt<1>(0h0))
[8137] FIRRTL:374509 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1162 = eq(stq_succeeded[3], UInt<1>(0h0))
[8138] FIRRTL:374510 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1163 = and(_T_1161, _T_1162)
[8139] FIRRTL:374511 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1163 :
[8140] FIRRTL:374512 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[3], UInt<1>(0h0)
[8141] FIRRTL:374513 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1164 = eq(stq_committed[4], UInt<1>(0h0))
[8142] FIRRTL:374514 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1165 = eq(stq_succeeded[4], UInt<1>(0h0))
[8143] FIRRTL:374515 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1166 = and(_T_1164, _T_1165)
[8144] FIRRTL:374516 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1166 :
[8145] FIRRTL:374517 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[4], UInt<1>(0h0)
[8146] FIRRTL:374518 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1167 = eq(stq_committed[5], UInt<1>(0h0))
[8147] FIRRTL:374519 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1168 = eq(stq_succeeded[5], UInt<1>(0h0))
[8148] FIRRTL:374520 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1169 = and(_T_1167, _T_1168)
[8149] FIRRTL:374521 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1169 :
[8150] FIRRTL:374522 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[5], UInt<1>(0h0)
[8151] FIRRTL:374523 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1170 = eq(stq_committed[6], UInt<1>(0h0))
[8152] FIRRTL:374524 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1171 = eq(stq_succeeded[6], UInt<1>(0h0))
[8153] FIRRTL:374525 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1172 = and(_T_1170, _T_1171)
[8154] FIRRTL:374526 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1172 :
[8155] FIRRTL:374527 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[6], UInt<1>(0h0)
[8156] FIRRTL:374528 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:15 KIND:node :: node _T_1173 = eq(stq_committed[7], UInt<1>(0h0))
[8157] FIRRTL:374529 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:36 KIND:node :: node _T_1174 = eq(stq_succeeded[7], UInt<1>(0h0))
[8158] FIRRTL:374530 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1951:33 KIND:node :: node _T_1175 = and(_T_1173, _T_1174)
[8159] FIRRTL:374531 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1952:9 KIND:when :: when _T_1175 :
[8160] FIRRTL:374532 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1953:33 KIND:connect :: connect stq_valid[7], UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-LSU-state-0-8-75c1d44ef5da10a6",
  "work_unit_id": "LSU::state-0-8",
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
