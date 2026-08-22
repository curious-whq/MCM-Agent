# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment: the µMCM language is intentionally
experimental and may be revised after discussion. Your job is to derive a
candidate abstraction that preserves information potentially relevant to
microarchitectural memory ordering, not to summarize the module in prose.

Task ID: `leaf_abstraction-LSU-state-0-12-4546b851920dd645`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::state-0-12`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 70
- logical statements: 35
- mapped/logical source lines: 25
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

['stq_execute_head']

## Environment/frontier signals

['_T_1150', '_T_1151', '_T_145', '_T_146', '_T_921', '_WIRE_15', '_WIRE_16', '_WIRE_17', '_stq_enq_e_e_bits_addr_T', '_stq_enq_e_e_bits_addr_is_virtual_T', '_stq_enq_e_e_bits_data_T', '_stq_enq_e_e_bits_uop_T', '_stq_enq_e_e_valid_T', '_stq_execute_head_T_5', 'age1_age_16', 'age1_age_17', 'age1_overflow_16', 'age1_overflow_17', 'dmem_req_fire[0]', 'h0', 'h1', 'io.dmem.nack[0].bits.is_hella', 'io.dmem.nack[0].bits.uop.stq_idx', 'io.dmem.nack[0].bits.uop.uses_ldq', 'io.dmem.nack[0].valid', 'stq_committed[*]', 'stq_enq_e.bits.addr.bits', 'stq_enq_e.bits.addr.valid', 'stq_enq_e.bits.addr_is_virtual', 'stq_enq_e.bits.can_execute', 'stq_enq_e.bits.cleared', 'stq_enq_e.bits.committed', 'stq_enq_e.bits.data.bits', 'stq_enq_e.bits.data.valid', 'stq_enq_e.bits.debug_wb_data', 'stq_enq_e.bits.next_ldq_idx', 'stq_enq_e.bits.succeeded', 'stq_enq_e.bits.uop.bp_debug_if', 'stq_enq_e.bits.uop.bp_xcpt_if', 'stq_enq_e.bits.uop.br_mask', 'stq_enq_e.bits.uop.br_tag', 'stq_enq_e.bits.uop.br_type', 'stq_enq_e.bits.uop.csr_cmd', 'stq_enq_e.bits.uop.debug_fsrc', 'stq_enq_e.bits.uop.debug_inst', 'stq_enq_e.bits.uop.debug_pc', 'stq_enq_e.bits.uop.debug_tsrc', 'stq_enq_e.bits.uop.dis_col_sel', 'stq_enq_e.bits.uop.dst_rtype', 'stq_enq_e.bits.uop.edge_inst', 'stq_enq_e.bits.uop.exc_cause', 'stq_enq_e.bits.uop.exception', 'stq_enq_e.bits.uop.fcn_dw', 'stq_enq_e.bits.uop.fcn_op', 'stq_enq_e.bits.uop.flush_on_commit', 'stq_enq_e.bits.uop.fp_ctrl.div', 'stq_enq_e.bits.uop.fp_ctrl.fastpipe', 'stq_enq_e.bits.uop.fp_ctrl.fma', 'stq_enq_e.bits.uop.fp_ctrl.fromint', 'stq_enq_e.bits.uop.fp_ctrl.ldst', 'stq_enq_e.bits.uop.fp_ctrl.ren1', 'stq_enq_e.bits.uop.fp_ctrl.ren2', 'stq_enq_e.bits.uop.fp_ctrl.ren3', 'stq_enq_e.bits.uop.fp_ctrl.sqrt', 'stq_enq_e.bits.uop.fp_ctrl.swap12', 'stq_enq_e.bits.uop.fp_ctrl.swap23', 'stq_enq_e.bits.uop.fp_ctrl.toint', 'stq_enq_e.bits.uop.fp_ctrl.typeTagIn', 'stq_enq_e.bits.uop.fp_ctrl.typeTagOut', 'stq_enq_e.bits.uop.fp_ctrl.vec', 'stq_enq_e.bits.uop.fp_ctrl.wen', 'stq_enq_e.bits.uop.fp_ctrl.wflags', 'stq_enq_e.bits.uop.fp_rm', 'stq_enq_e.bits.uop.fp_typ', 'stq_enq_e.bits.uop.fp_val', 'stq_enq_e.bits.uop.frs3_en', 'stq_enq_e.bits.uop.ftq_idx', 'stq_enq_e.bits.uop.fu_code[0]', 'stq_enq_e.bits.uop.fu_code[1]', 'stq_enq_e.bits.uop.fu_code[2]', 'stq_enq_e.bits.uop.fu_code[3]', 'stq_enq_e.bits.uop.fu_code[4]', 'stq_enq_e.bits.uop.fu_code[5]', 'stq_enq_e.bits.uop.fu_code[6]', 'stq_enq_e.bits.uop.fu_code[7]', 'stq_enq_e.bits.uop.fu_code[8]', 'stq_enq_e.bits.uop.fu_code[9]', 'stq_enq_e.bits.uop.imm_packed', 'stq_enq_e.bits.uop.imm_rename', 'stq_enq_e.bits.uop.imm_sel', 'stq_enq_e.bits.uop.inst', 'stq_enq_e.bits.uop.iq_type[0]', 'stq_enq_e.bits.uop.iq_type[1]', 'stq_enq_e.bits.uop.iq_type[2]', 'stq_enq_e.bits.uop.iq_type[3]', 'stq_enq_e.bits.uop.is_amo', 'stq_enq_e.bits.uop.is_eret', 'stq_enq_e.bits.uop.is_fence', 'stq_enq_e.bits.uop.is_fencei', 'stq_enq_e.bits.uop.is_mov', 'stq_enq_e.bits.uop.is_rocc', 'stq_enq_e.bits.uop.is_rvc', 'stq_enq_e.bits.uop.is_sfb', 'stq_enq_e.bits.uop.is_sfence', 'stq_enq_e.bits.uop.is_sys_pc2epc', 'stq_enq_e.bits.uop.is_unique', 'stq_enq_e.bits.uop.iw_issued', 'stq_enq_e.bits.uop.iw_issued_partial_agen', 'stq_enq_e.bits.uop.iw_issued_partial_dgen', 'stq_enq_e.bits.uop.iw_p1_bypass_hint', 'stq_enq_e.bits.uop.iw_p1_speculative_child', 'stq_enq_e.bits.uop.iw_p2_bypass_hint', 'stq_enq_e.bits.uop.iw_p2_speculative_child', 'stq_enq_e.bits.uop.iw_p3_bypass_hint', 'stq_enq_e.bits.uop.ldq_idx', 'stq_enq_e.bits.uop.ldst', 'stq_enq_e.bits.uop.ldst_is_rs1', 'stq_enq_e.bits.uop.lrs1', 'stq_enq_e.bits.uop.lrs1_rtype', 'stq_enq_e.bits.uop.lrs2', 'stq_enq_e.bits.uop.lrs2_rtype', 'stq_enq_e.bits.uop.lrs3', 'stq_enq_e.bits.uop.mem_cmd', 'stq_enq_e.bits.uop.mem_signed', 'stq_enq_e.bits.uop.mem_size', 'stq_enq_e.bits.uop.op1_sel', 'stq_enq_e.bits.uop.op2_sel', 'stq_enq_e.bits.uop.pc_lob', 'stq_enq_e.bits.uop.pdst', 'stq_enq_e.bits.uop.pimm', 'stq_enq_e.bits.uop.ppred', 'stq_enq_e.bits.uop.ppred_busy', 'stq_enq_e.bits.uop.prs1', 'stq_enq_e.bits.uop.prs1_busy', 'stq_enq_e.bits.uop.prs2', 'stq_enq_e.bits.uop.prs2_busy', 'stq_enq_e.bits.uop.prs3', 'stq_enq_e.bits.uop.prs3_busy', 'stq_enq_e.bits.uop.rob_idx', 'stq_enq_e.bits.uop.rxq_idx', 'stq_enq_e.bits.uop.stale_pdst', 'stq_enq_e.bits.uop.stq_idx', 'stq_enq_e.bits.uop.taken', 'stq_enq_e.bits.uop.uses_ldq', 'stq_enq_e.bits.uop.uses_stq', 'stq_enq_e.bits.uop.xcpt_ae_if', 'stq_enq_e.bits.uop.xcpt_ma_if', 'stq_enq_e.bits.uop.xcpt_pf_if', 'stq_enq_e_e', 'stq_execute_head', 'stq_execute_queue.io.deq.bits.uop.stq_idx', 'stq_execute_queue.io.enq.ready', 'stq_execute_queue.io.enq.valid', 'will_fire_load_agen_exec[0]', 'will_fire_load_retry[0]']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[1186] FIRRTL:367558 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_valid_T = bits(stq_execute_head, 2, 0)
[1188] FIRRTL:367560 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_bits_uop_T = bits(stq_execute_head, 2, 0)
[1190] FIRRTL:367562 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_bits_addr_T = bits(stq_execute_head, 2, 0)
[1192] FIRRTL:367564 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_bits_addr_is_virtual_T = bits(stq_execute_head, 2, 0)
[1194] FIRRTL:367566 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_bits_data_T = bits(stq_execute_head, 2, 0)
[1196] FIRRTL:367568 SRC:<no-source-locator> KIND:node :: node _stq_enq_e_e_bits_committed_T = bits(stq_execute_head, 2, 0)
[1197] FIRRTL:367569 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:273:32 KIND:connect :: connect stq_enq_e_e.bits.committed, stq_committed[_stq_enq_e_e_bits_committed_T]
[1209] FIRRTL:367581 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:555:27 KIND:connect :: connect stq_enq_e, stq_enq_e_e
[1335] FIRRTL:367707 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:562:21 KIND:node :: node _can_enq_store_execute_T = and(stq_enq_e.valid, stq_enq_e.bits.addr.valid)
[1336] FIRRTL:367708 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:563:31 KIND:node :: node _can_enq_store_execute_T_1 = and(_can_enq_store_execute_T, stq_enq_e.bits.data.valid)
[1337] FIRRTL:367709 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:565:4 KIND:node :: node _can_enq_store_execute_T_2 = eq(stq_enq_e.bits.addr_is_virtual, UInt<1>(0h0))
[1338] FIRRTL:367710 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:564:31 KIND:node :: node _can_enq_store_execute_T_3 = and(_can_enq_store_execute_T_1, _can_enq_store_execute_T_2)
[1339] FIRRTL:367711 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:566:4 KIND:node :: node _can_enq_store_execute_T_4 = eq(stq_enq_e.bits.uop.exception, UInt<1>(0h0))
[1340] FIRRTL:367712 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:565:36 KIND:node :: node _can_enq_store_execute_T_5 = and(_can_enq_store_execute_T_3, _can_enq_store_execute_T_4)
[1341] FIRRTL:367713 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:567:4 KIND:node :: node _can_enq_store_execute_T_6 = eq(stq_enq_e.bits.uop.is_fence, UInt<1>(0h0))
[1342] FIRRTL:367714 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:566:34 KIND:node :: node _can_enq_store_execute_T_7 = and(_can_enq_store_execute_T_5, _can_enq_store_execute_T_6)
[1343] FIRRTL:367715 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:568:30 KIND:node :: node _can_enq_store_execute_T_8 = or(stq_enq_e.bits.committed, stq_enq_e.bits.uop.is_amo)
[1344] FIRRTL:367716 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:567:33 KIND:node :: node can_enq_store_execute = and(_can_enq_store_execute_T_7, _can_enq_store_execute_T_8)
[1345] FIRRTL:367717 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:570:34 KIND:connect :: connect stq_execute_queue.io.enq.valid, can_enq_store_execute
[1346] FIRRTL:367718 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_79 = and(stq_execute_queue.io.enq.ready, stq_execute_queue.io.enq.valid)
[1347] FIRRTL:367719 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:572:31 KIND:node :: node _T_80 = and(can_enq_store_execute, _T_79)
[1348] FIRRTL:367720 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:572:65 KIND:when :: when _T_80 :
[1349] FIRRTL:367721 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_execute_head_T = add(stq_execute_head, UInt<1>(0h1))
[1350] FIRRTL:367722 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_execute_head_T_1 = tail(_stq_execute_head_T, 1)
[1351] FIRRTL:367723 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _stq_execute_head_T_2 = bits(_stq_execute_head_T_1, 3, 0)
[1352] FIRRTL:367724 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:573:22 KIND:connect :: connect stq_execute_head, _stq_execute_head_T_2
[2437] FIRRTL:368809 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:915:13 KIND:node :: node _T_146 = eq(dmem_req_fire[0], UInt<1>(0h0))
[2438] FIRRTL:368810 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:915:32 KIND:when :: when _T_146 :
[2440] FIRRTL:368812 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:917:26 KIND:connect :: connect stq_execute_head, stq_execute_queue.io.deq.bits.uop.stq_idx
[6872] FIRRTL:373244 SRC:<no-source-locator> KIND:else :: else :
[6880] FIRRTL:373252 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age1_overflow_15 = bits(stq_execute_head, 3, 3)
[6881] FIRRTL:373253 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_15 = bits(io.dmem.nack[0].bits.uop.stq_idx, 3, 3)
[6882] FIRRTL:373254 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age1_age_15 = bits(stq_execute_head, 2, 0)
[6883] FIRRTL:373255 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_15 = bits(io.dmem.nack[0].bits.uop.stq_idx, 2, 0)
[6884] FIRRTL:373256 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_899 = eq(age1_overflow_15, age2_overflow_15)
[6885] FIRRTL:373257 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_900 = gt(age1_age_15, age2_age_15)
[6886] FIRRTL:373258 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_901 = neq(age1_overflow_15, age2_overflow_15)
[6887] FIRRTL:373259 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_902 = lt(age1_age_15, age2_age_15)
[6888] FIRRTL:373260 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_903 = mux(_T_899, _T_900, UInt<1>(0h0))
[6889] FIRRTL:373261 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_904 = mux(_T_901, _T_902, UInt<1>(0h0))
[6890] FIRRTL:373262 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_905 = or(_T_903, _T_904)
[6892] FIRRTL:373264 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_15, _T_905
[6894] FIRRTL:373266 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_16 = bits(io.dmem.nack[0].bits.uop.stq_idx, 3, 3)
[6896] FIRRTL:373268 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_16 = bits(io.dmem.nack[0].bits.uop.stq_idx, 2, 0)
[6897] FIRRTL:373269 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_906 = eq(age1_overflow_16, age2_overflow_16)
[6898] FIRRTL:373270 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_907 = gt(age1_age_16, age2_age_16)
[6899] FIRRTL:373271 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_908 = neq(age1_overflow_16, age2_overflow_16)
[6900] FIRRTL:373272 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_909 = lt(age1_age_16, age2_age_16)
[6901] FIRRTL:373273 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_910 = mux(_T_906, _T_907, UInt<1>(0h0))
[6902] FIRRTL:373274 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_911 = mux(_T_908, _T_909, UInt<1>(0h0))
[6903] FIRRTL:373275 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_912 = or(_T_910, _T_911)
[6905] FIRRTL:373277 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_16, _T_912
[6906] FIRRTL:373278 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:22 KIND:node :: node _T_913 = xor(_WIRE_15, _WIRE_16)
[6908] FIRRTL:373280 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node age2_overflow_17 = bits(stq_execute_head, 3, 3)
[6910] FIRRTL:373282 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node age2_age_17 = bits(stq_execute_head, 2, 0)
[6911] FIRRTL:373283 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _T_914 = eq(age1_overflow_17, age2_overflow_17)
[6912] FIRRTL:373284 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _T_915 = gt(age1_age_17, age2_age_17)
[6913] FIRRTL:373285 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _T_916 = neq(age1_overflow_17, age2_overflow_17)
[6914] FIRRTL:373286 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _T_917 = lt(age1_age_17, age2_age_17)
[6915] FIRRTL:373287 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_918 = mux(_T_914, _T_915, UInt<1>(0h0))
[6916] FIRRTL:373288 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_919 = mux(_T_916, _T_917, UInt<1>(0h0))
[6917] FIRRTL:373289 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _T_920 = or(_T_918, _T_919)
[6919] FIRRTL:373291 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _WIRE_17, _T_920
[6920] FIRRTL:373292 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2138:43 KIND:node :: node _T_921 = xor(_T_913, _WIRE_17)
[6921] FIRRTL:373293 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1551:89 KIND:when :: when _T_921 :
[6923] FIRRTL:373295 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1553:28 KIND:connect :: connect stq_execute_head, io.dmem.nack[0].bits.uop.stq_idx
[7943] FIRRTL:374315 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_execute_head_T_3 = add(stq_execute_head, UInt<1>(0h1))
[7944] FIRRTL:374316 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_execute_head_T_4 = tail(_stq_execute_head_T_3, 1)
[7945] FIRRTL:374317 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _stq_execute_head_T_5 = bits(_stq_execute_head_T_4, 3, 0)
[8110] FIRRTL:374482 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1938:24 KIND:connect :: connect stq_execute_head, UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-LSU-state-0-12-4546b851920dd645",
  "work_unit_id": "LSU::state-0-12",
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
