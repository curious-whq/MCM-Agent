# MCM-Agent manual semantic task: parent µMCM synthesis

You are performing one bottom-up semantic-composition step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a parent-synthesis task. Every direct child listed below is already
`FROZEN_FOR_COMPOSITION`. Child RTL is **not an input** to this task and must not
be reconstructed, guessed, or re-read. Treat each frozen child µMCM as a trusted
semantic component and combine it only with the parent-local RTL evidence below.

The human is transport-only. Analyze the parent autonomously. If the current
µMCM Formal AST is sufficient, emit the complete candidate in this response. If
a necessary parent-level semantic concept cannot be represented faithfully,
report `MCM-AGENT LANGUAGE GAP`. If the AST can express a property but the current
formal backend may not prove a relation spanning imported child semantics, still
emit the candidate; that is a composition-prover gap, not a language gap.

Task ID: `parent_synthesis-BoomNonBlockingDCache-59b0ae1731a92b08`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `parent-synthesis-prompt-0.3`
Output schema version: `umcm-formal-0.5`

## Parent WorkUnit

- id: `BoomNonBlockingDCache`
- module: `BoomNonBlockingDCache`
- kind: `module`
- instance path: `BoomNonBlockingDCache`
- leaf: `False`
- coverage complete: `True`
- parent-local raw statements after child replacement: 2459
- parent-local logical statements after child replacement: 441
- parent-local registers: 31
- parent-local physical boundary events: 6

## Composition rules

1. Frozen child axioms are already trusted and remain imported automatically when
   this parent is frozen. Do **not** mechanically copy every child axiom into the
   parent candidate. Grounding signals/state/evidence stored inside a frozen child
   summary are provenance only: do not treat them as parent-local RTL evidence or
   infer new child behavior beyond the trusted frozen semantics.
2. Child semantic objects may be referenced only by the exact qualified IDs in
   each compact child interface's `exported_ids`. A direct theorem's Formal AST
   uses child-local IDs for local declarations; use their `qualified_id` from the
   interface when referencing them in the parent candidate. Opaque imports are
   usable only as typed semantic atoms: do not infer their hidden definitions.
   Do not redeclare an imported occurrence, predicate, identity, or axiom.
3. New boundary occurrences may reference parent-local physical events and the
   exposed child boundary events. New derived occurrences must be grounded only
   in parent-local RTL; child internal state/signals are not available.
4. `evidence_statement_ids` in this result may cite only the parent-local statement
   ledger below. Child provenance belongs in `extensions`, not in fabricated
   parent statement evidence.
5. For every new parent axiom, fill:
   `extensions.parent_synthesis.axiom_provenance[<axiom-id>]` with:
   - `kind`: one of `parent_local`, `reexported`, `lifted`, `emergent`;
   - `source_axioms`: zero or more exact qualified IDs from the imported child
     `exported_ids.axioms` lists;
   - `note`: a short explanation.
   `parent_local` normally has no child source axioms. `lifted`, `emergent`, or
   `reexported` must cite at least one imported source axiom.
6. It is valid for this parent to declare **zero new axioms** when the wrapper adds
   no additional memory/coherence-relevant constraint. The frozen parent will
   still retain the frozen child imports. Do not invent redundant axioms merely
   to avoid an empty parent-local candidate.
7. The trusted child summaries are not assumed complete forever. Omitting an
   optional strengthening is a safe over-approximation and may be recorded in
   `rationale` for later CEGAR refinement.
8. Do not claim liveness without an explicit environment assumption.
9. Candidate axioms remain candidates until deterministic/formal validation.

## Parent-local physical events

- `BoomNonBlockingDCache::auto.out.a.fire`
  - predicate: `auto.out.a.valid && auto.out.a.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['auto.out.a.bits.address', 'auto.out.a.bits.corrupt', 'auto.out.a.bits.data', 'auto.out.a.bits.mask', 'auto.out.a.bits.opcode', 'auto.out.a.bits.param', 'auto.out.a.bits.size', 'auto.out.a.bits.source']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache::auto.out.e.fire`
  - predicate: `auto.out.e.valid && auto.out.e.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['auto.out.e.bits.sink']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache::io.errors.bus.valid`
  - predicate: `io.errors.bus.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.errors.bus.bits']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache::io.lsu.ll_resp.fire`
  - predicate: `io.lsu.ll_resp.valid && io.lsu.ll_resp.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.lsu.ll_resp.bits.data', 'io.lsu.ll_resp.bits.is_hella', 'io.lsu.ll_resp.bits.uop.bp_debug_if', 'io.lsu.ll_resp.bits.uop.bp_xcpt_if', 'io.lsu.ll_resp.bits.uop.br_mask', 'io.lsu.ll_resp.bits.uop.br_tag', 'io.lsu.ll_resp.bits.uop.br_type', 'io.lsu.ll_resp.bits.uop.csr_cmd', 'io.lsu.ll_resp.bits.uop.debug_fsrc', 'io.lsu.ll_resp.bits.uop.debug_inst', 'io.lsu.ll_resp.bits.uop.debug_pc', 'io.lsu.ll_resp.bits.uop.debug_tsrc', 'io.lsu.ll_resp.bits.uop.dis_col_sel', 'io.lsu.ll_resp.bits.uop.dst_rtype', 'io.lsu.ll_resp.bits.uop.edge_inst', 'io.lsu.ll_resp.bits.uop.exc_cause', 'io.lsu.ll_resp.bits.uop.exception', 'io.lsu.ll_resp.bits.uop.fcn_dw', 'io.lsu.ll_resp.bits.uop.fcn_op', 'io.lsu.ll_resp.bits.uop.flush_on_commit', 'io.lsu.ll_resp.bits.uop.fp_ctrl.div', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fastpipe', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fma', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fromint', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ldst', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren1', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren2', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren3', 'io.lsu.ll_resp.bits.uop.fp_ctrl.sqrt', 'io.lsu.ll_resp.bits.uop.fp_ctrl.swap12', 'io.lsu.ll_resp.bits.uop.fp_ctrl.swap23', 'io.lsu.ll_resp.bits.uop.fp_ctrl.toint', 'io.lsu.ll_resp.bits.uop.fp_ctrl.typeTagIn', 'io.lsu.ll_resp.bits.uop.fp_ctrl.typeTagOut', 'io.lsu.ll_resp.bits.uop.fp_ctrl.vec', 'io.lsu.ll_resp.bits.uop.fp_ctrl.wen', 'io.lsu.ll_resp.bits.uop.fp_ctrl.wflags', 'io.lsu.ll_resp.bits.uop.fp_rm', 'io.lsu.ll_resp.bits.uop.fp_typ', 'io.lsu.ll_resp.bits.uop.fp_val', 'io.lsu.ll_resp.bits.uop.frs3_en', 'io.lsu.ll_resp.bits.uop.ftq_idx', 'io.lsu.ll_resp.bits.uop.fu_code[0]', 'io.lsu.ll_resp.bits.uop.fu_code[1]', 'io.lsu.ll_resp.bits.uop.fu_code[2]', 'io.lsu.ll_resp.bits.uop.fu_code[3]', 'io.lsu.ll_resp.bits.uop.fu_code[4]', 'io.lsu.ll_resp.bits.uop.fu_code[5]', 'io.lsu.ll_resp.bits.uop.fu_code[6]', 'io.lsu.ll_resp.bits.uop.fu_code[7]', 'io.lsu.ll_resp.bits.uop.fu_code[8]', 'io.lsu.ll_resp.bits.uop.fu_code[9]', 'io.lsu.ll_resp.bits.uop.imm_packed', 'io.lsu.ll_resp.bits.uop.imm_rename', 'io.lsu.ll_resp.bits.uop.imm_sel', 'io.lsu.ll_resp.bits.uop.inst', 'io.lsu.ll_resp.bits.uop.iq_type[0]', 'io.lsu.ll_resp.bits.uop.iq_type[1]', 'io.lsu.ll_resp.bits.uop.iq_type[2]', 'io.lsu.ll_resp.bits.uop.iq_type[3]', 'io.lsu.ll_resp.bits.uop.is_amo', 'io.lsu.ll_resp.bits.uop.is_eret', 'io.lsu.ll_resp.bits.uop.is_fence', 'io.lsu.ll_resp.bits.uop.is_fencei', 'io.lsu.ll_resp.bits.uop.is_mov', 'io.lsu.ll_resp.bits.uop.is_rocc', 'io.lsu.ll_resp.bits.uop.is_rvc', 'io.lsu.ll_resp.bits.uop.is_sfb', 'io.lsu.ll_resp.bits.uop.is_sfence', 'io.lsu.ll_resp.bits.uop.is_sys_pc2epc', 'io.lsu.ll_resp.bits.uop.is_unique', 'io.lsu.ll_resp.bits.uop.iw_issued', 'io.lsu.ll_resp.bits.uop.iw_issued_partial_agen', 'io.lsu.ll_resp.bits.uop.iw_issued_partial_dgen', 'io.lsu.ll_resp.bits.uop.iw_p1_bypass_hint', 'io.lsu.ll_resp.bits.uop.iw_p1_speculative_child', 'io.lsu.ll_resp.bits.uop.iw_p2_bypass_hint', 'io.lsu.ll_resp.bits.uop.iw_p2_speculative_child', 'io.lsu.ll_resp.bits.uop.iw_p3_bypass_hint', 'io.lsu.ll_resp.bits.uop.ldq_idx', 'io.lsu.ll_resp.bits.uop.ldst', 'io.lsu.ll_resp.bits.uop.ldst_is_rs1', 'io.lsu.ll_resp.bits.uop.lrs1', 'io.lsu.ll_resp.bits.uop.lrs1_rtype', 'io.lsu.ll_resp.bits.uop.lrs2', 'io.lsu.ll_resp.bits.uop.lrs2_rtype', 'io.lsu.ll_resp.bits.uop.lrs3', 'io.lsu.ll_resp.bits.uop.mem_cmd', 'io.lsu.ll_resp.bits.uop.mem_signed', 'io.lsu.ll_resp.bits.uop.mem_size', 'io.lsu.ll_resp.bits.uop.op1_sel', 'io.lsu.ll_resp.bits.uop.op2_sel', 'io.lsu.ll_resp.bits.uop.pc_lob', 'io.lsu.ll_resp.bits.uop.pdst', 'io.lsu.ll_resp.bits.uop.pimm', 'io.lsu.ll_resp.bits.uop.ppred', 'io.lsu.ll_resp.bits.uop.ppred_busy', 'io.lsu.ll_resp.bits.uop.prs1', 'io.lsu.ll_resp.bits.uop.prs1_busy', 'io.lsu.ll_resp.bits.uop.prs2', 'io.lsu.ll_resp.bits.uop.prs2_busy', 'io.lsu.ll_resp.bits.uop.prs3', 'io.lsu.ll_resp.bits.uop.prs3_busy', 'io.lsu.ll_resp.bits.uop.rob_idx', 'io.lsu.ll_resp.bits.uop.rxq_idx', 'io.lsu.ll_resp.bits.uop.stale_pdst', 'io.lsu.ll_resp.bits.uop.stq_idx', 'io.lsu.ll_resp.bits.uop.taken', 'io.lsu.ll_resp.bits.uop.uses_ldq', 'io.lsu.ll_resp.bits.uop.uses_stq', 'io.lsu.ll_resp.bits.uop.xcpt_ae_if', 'io.lsu.ll_resp.bits.uop.xcpt_ma_if', 'io.lsu.ll_resp.bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache::io.lsu.release.fire`
  - predicate: `io.lsu.release.valid && io.lsu.release.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.lsu.release.bits.address', 'io.lsu.release.bits.corrupt', 'io.lsu.release.bits.data', 'io.lsu.release.bits.opcode', 'io.lsu.release.bits.param', 'io.lsu.release.bits.size', 'io.lsu.release.bits.source']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache::io.lsu.req.bits[0].valid`
  - predicate: `io.lsu.req.bits[0].valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.lsu.req.bits[0].bits.addr', 'io.lsu.req.bits[0].bits.data', 'io.lsu.req.bits[0].bits.is_hella', 'io.lsu.req.bits[0].bits.uop.bp_debug_if', 'io.lsu.req.bits[0].bits.uop.bp_xcpt_if', 'io.lsu.req.bits[0].bits.uop.br_mask', 'io.lsu.req.bits[0].bits.uop.br_tag', 'io.lsu.req.bits[0].bits.uop.br_type', 'io.lsu.req.bits[0].bits.uop.csr_cmd', 'io.lsu.req.bits[0].bits.uop.debug_fsrc', 'io.lsu.req.bits[0].bits.uop.debug_inst', 'io.lsu.req.bits[0].bits.uop.debug_pc', 'io.lsu.req.bits[0].bits.uop.debug_tsrc', 'io.lsu.req.bits[0].bits.uop.dis_col_sel', 'io.lsu.req.bits[0].bits.uop.dst_rtype', 'io.lsu.req.bits[0].bits.uop.edge_inst', 'io.lsu.req.bits[0].bits.uop.exc_cause', 'io.lsu.req.bits[0].bits.uop.exception', 'io.lsu.req.bits[0].bits.uop.fcn_dw', 'io.lsu.req.bits[0].bits.uop.fcn_op', 'io.lsu.req.bits[0].bits.uop.flush_on_commit', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.div', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fma', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fromint', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ldst', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren1', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren2', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren3', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.swap12', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.swap23', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.toint', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.vec', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.wen', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.wflags', 'io.lsu.req.bits[0].bits.uop.fp_rm', 'io.lsu.req.bits[0].bits.uop.fp_typ', 'io.lsu.req.bits[0].bits.uop.fp_val', 'io.lsu.req.bits[0].bits.uop.frs3_en', 'io.lsu.req.bits[0].bits.uop.ftq_idx', 'io.lsu.req.bits[0].bits.uop.fu_code[0]', 'io.lsu.req.bits[0].bits.uop.fu_code[1]', 'io.lsu.req.bits[0].bits.uop.fu_code[2]', 'io.lsu.req.bits[0].bits.uop.fu_code[3]', 'io.lsu.req.bits[0].bits.uop.fu_code[4]', 'io.lsu.req.bits[0].bits.uop.fu_code[5]', 'io.lsu.req.bits[0].bits.uop.fu_code[6]', 'io.lsu.req.bits[0].bits.uop.fu_code[7]', 'io.lsu.req.bits[0].bits.uop.fu_code[8]', 'io.lsu.req.bits[0].bits.uop.fu_code[9]', 'io.lsu.req.bits[0].bits.uop.imm_packed', 'io.lsu.req.bits[0].bits.uop.imm_rename', 'io.lsu.req.bits[0].bits.uop.imm_sel', 'io.lsu.req.bits[0].bits.uop.inst', 'io.lsu.req.bits[0].bits.uop.iq_type[0]', 'io.lsu.req.bits[0].bits.uop.iq_type[1]', 'io.lsu.req.bits[0].bits.uop.iq_type[2]', 'io.lsu.req.bits[0].bits.uop.iq_type[3]', 'io.lsu.req.bits[0].bits.uop.is_amo', 'io.lsu.req.bits[0].bits.uop.is_eret', 'io.lsu.req.bits[0].bits.uop.is_fence', 'io.lsu.req.bits[0].bits.uop.is_fencei', 'io.lsu.req.bits[0].bits.uop.is_mov', 'io.lsu.req.bits[0].bits.uop.is_rocc', 'io.lsu.req.bits[0].bits.uop.is_rvc', 'io.lsu.req.bits[0].bits.uop.is_sfb', 'io.lsu.req.bits[0].bits.uop.is_sfence', 'io.lsu.req.bits[0].bits.uop.is_sys_pc2epc', 'io.lsu.req.bits[0].bits.uop.is_unique', 'io.lsu.req.bits[0].bits.uop.iw_issued', 'io.lsu.req.bits[0].bits.uop.iw_issued_partial_agen', 'io.lsu.req.bits[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.req.bits[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.req.bits[0].bits.uop.iw_p1_speculative_child', 'io.lsu.req.bits[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.req.bits[0].bits.uop.iw_p2_speculative_child', 'io.lsu.req.bits[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.req.bits[0].bits.uop.ldq_idx', 'io.lsu.req.bits[0].bits.uop.ldst', 'io.lsu.req.bits[0].bits.uop.ldst_is_rs1', 'io.lsu.req.bits[0].bits.uop.lrs1', 'io.lsu.req.bits[0].bits.uop.lrs1_rtype', 'io.lsu.req.bits[0].bits.uop.lrs2', 'io.lsu.req.bits[0].bits.uop.lrs2_rtype', 'io.lsu.req.bits[0].bits.uop.lrs3', 'io.lsu.req.bits[0].bits.uop.mem_cmd', 'io.lsu.req.bits[0].bits.uop.mem_signed', 'io.lsu.req.bits[0].bits.uop.mem_size', 'io.lsu.req.bits[0].bits.uop.op1_sel', 'io.lsu.req.bits[0].bits.uop.op2_sel', 'io.lsu.req.bits[0].bits.uop.pc_lob', 'io.lsu.req.bits[0].bits.uop.pdst', 'io.lsu.req.bits[0].bits.uop.pimm', 'io.lsu.req.bits[0].bits.uop.ppred', 'io.lsu.req.bits[0].bits.uop.ppred_busy', 'io.lsu.req.bits[0].bits.uop.prs1', 'io.lsu.req.bits[0].bits.uop.prs1_busy', 'io.lsu.req.bits[0].bits.uop.prs2', 'io.lsu.req.bits[0].bits.uop.prs2_busy', 'io.lsu.req.bits[0].bits.uop.prs3', 'io.lsu.req.bits[0].bits.uop.prs3_busy', 'io.lsu.req.bits[0].bits.uop.rob_idx', 'io.lsu.req.bits[0].bits.uop.rxq_idx', 'io.lsu.req.bits[0].bits.uop.stale_pdst', 'io.lsu.req.bits[0].bits.uop.stq_idx', 'io.lsu.req.bits[0].bits.uop.taken', 'io.lsu.req.bits[0].bits.uop.uses_ldq', 'io.lsu.req.bits[0].bits.uop.uses_stq', 'io.lsu.req.bits[0].bits.uop.xcpt_ae_if', 'io.lsu.req.bits[0].bits.uop.xcpt_ma_if', 'io.lsu.req.bits[0].bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []

## Parent-local concrete state

['REG', 'REG_1', 'amoalu_io_rhs_REG', 'debug_sc_fail_addr', 'debug_sc_fail_cnt', 'io_lsu_perf_acquire_counter', 'io_lsu_perf_release_counter', 'lrsc_addr', 'mshrs_io_meta_resp_bits_REG', 's1_mshr_meta_read_way_en', 's1_replay_way_en', 's1_req', 's1_send_resp_or_nack', 's1_type', 's1_valid_REG', 's1_wb_way_en', 's2_lr_REG', 's2_repl_meta_REG', 's2_repl_meta_REG_1', 's2_repl_meta_REG_2', 's2_repl_meta_REG_3', 's2_replaced_way_en_REG', 's2_sc_REG', 's3_data_word', 's3_req_REG', 's3_valid', 's3_way', 's4_req', 's4_valid', 's5_req', 's5_valid']

## Parent frontier signals

['amoalu.clock', 'amoalu.io.cmd', 'amoalu.io.lhs', 'amoalu.io.mask', 'amoalu.io.out', 'amoalu.io.rhs', 'amoalu.reset', 'auto.out.a.bits.address', 'auto.out.a.bits.corrupt', 'auto.out.a.bits.data', 'auto.out.a.bits.mask', 'auto.out.a.bits.opcode', 'auto.out.a.bits.param', 'auto.out.a.bits.size', 'auto.out.a.bits.source', 'auto.out.a.ready', 'auto.out.a.valid', 'auto.out.b.bits.address', 'auto.out.b.bits.corrupt', 'auto.out.b.bits.data', 'auto.out.b.bits.mask', 'auto.out.b.bits.opcode', 'auto.out.b.bits.param', 'auto.out.b.bits.size', 'auto.out.b.bits.source', 'auto.out.b.ready', 'auto.out.b.valid', 'auto.out.c.bits.address', 'auto.out.c.bits.corrupt', 'auto.out.c.bits.data', 'auto.out.c.bits.opcode', 'auto.out.c.bits.param', 'auto.out.c.bits.size', 'auto.out.c.bits.source', 'auto.out.c.ready', 'auto.out.c.valid', 'auto.out.d.bits.corrupt', 'auto.out.d.bits.data', 'auto.out.d.bits.denied', 'auto.out.d.bits.opcode', 'auto.out.d.bits.param', 'auto.out.d.bits.sink', 'auto.out.d.bits.size', 'auto.out.d.bits.source', 'auto.out.d.ready', 'auto.out.d.valid', 'auto.out.e.bits.sink', 'auto.out.e.ready', 'auto.out.e.valid', 'clock', 'data.clock', 'data.io.read[0].bits.addr', 'data.io.read[0].bits.way_en', 'data.io.read[0].valid', 'data.io.resp[0][0]', 'data.io.resp[0][1]', 'data.io.resp[0][2]', 'data.io.resp[0][3]', 'data.io.s1_nacks[0]', 'data.io.write.bits.addr', 'data.io.write.bits.data', 'data.io.write.bits.way_en', 'data.io.write.bits.wmask', 'data.io.write.valid', 'data.reset', 'dataReadArb.clock', 'dataReadArb.io.in[0].bits.req[0].addr', 'dataReadArb.io.in[0].bits.req[0].way_en', 'dataReadArb.io.in[0].bits.valid[0]', 'dataReadArb.io.in[0].ready', 'dataReadArb.io.in[0].valid', 'dataReadArb.io.in[1].bits.req[0].addr', 'dataReadArb.io.in[1].bits.req[0].way_en', 'dataReadArb.io.in[1].bits.valid[0]', 'dataReadArb.io.in[1].ready', 'dataReadArb.io.in[1].valid', 'dataReadArb.io.in[2].bits.req[0].addr', 'dataReadArb.io.in[2].bits.req[0].way_en', 'dataReadArb.io.in[2].bits.valid[0]', 'dataReadArb.io.in[2].ready', 'dataReadArb.io.in[2].valid', 'dataReadArb.io.out.bits.req[0].addr', 'dataReadArb.io.out.bits.req[0].way_en', 'dataReadArb.io.out.bits.valid[0]', 'dataReadArb.io.out.ready', 'dataReadArb.io.out.valid', 'dataReadArb.reset', 'dataWriteArb.clock', 'dataWriteArb.io.in[0].bits.addr', 'dataWriteArb.io.in[0].bits.data', 'dataWriteArb.io.in[0].bits.way_en', 'dataWriteArb.io.in[0].bits.wmask', 'dataWriteArb.io.in[0].valid', 'dataWriteArb.io.in[1].bits.addr', 'dataWriteArb.io.in[1].bits.data', 'dataWriteArb.io.in[1].bits.way_en', 'dataWriteArb.io.in[1].bits.wmask', 'dataWriteArb.io.in[1].ready', 'dataWriteArb.io.in[1].valid', 'dataWriteArb.io.out.bits.addr', 'dataWriteArb.io.out.bits.data', 'dataWriteArb.io.out.bits.way_en', 'dataWriteArb.io.out.bits.wmask', 'dataWriteArb.io.out.ready', 'dataWriteArb.io.out.valid', 'dataWriteArb.reset', 'io.errors.bus.bits', 'io.errors.bus.valid', 'io.lsu.brupdate.b1.mispredict_mask', 'io.lsu.brupdate.b1.resolve_mask', 'io.lsu.brupdate.b2.cfi_type', 'io.lsu.brupdate.b2.jalr_target', 'io.lsu.brupdate.b2.mispredict', 'io.lsu.brupdate.b2.pc_sel', 'io.lsu.brupdate.b2.taken', 'io.lsu.brupdate.b2.target_offset', 'io.lsu.brupdate.b2.uop.bp_debug_if', 'io.lsu.brupdate.b2.uop.bp_xcpt_if', 'io.lsu.brupdate.b2.uop.br_mask', 'io.lsu.brupdate.b2.uop.br_tag', 'io.lsu.brupdate.b2.uop.br_type', 'io.lsu.brupdate.b2.uop.csr_cmd', 'io.lsu.brupdate.b2.uop.debug_fsrc', 'io.lsu.brupdate.b2.uop.debug_inst', 'io.lsu.brupdate.b2.uop.debug_pc', 'io.lsu.brupdate.b2.uop.debug_tsrc', 'io.lsu.brupdate.b2.uop.dis_col_sel', 'io.lsu.brupdate.b2.uop.dst_rtype', 'io.lsu.brupdate.b2.uop.edge_inst', 'io.lsu.brupdate.b2.uop.exc_cause', 'io.lsu.brupdate.b2.uop.exception', 'io.lsu.brupdate.b2.uop.fcn_dw', 'io.lsu.brupdate.b2.uop.fcn_op', 'io.lsu.brupdate.b2.uop.flush_on_commit', 'io.lsu.brupdate.b2.uop.fp_ctrl.div', 'io.lsu.brupdate.b2.uop.fp_ctrl.fastpipe', 'io.lsu.brupdate.b2.uop.fp_ctrl.fma', 'io.lsu.brupdate.b2.uop.fp_ctrl.fromint', 'io.lsu.brupdate.b2.uop.fp_ctrl.ldst', 'io.lsu.brupdate.b2.uop.fp_ctrl.ren1', 'io.lsu.brupdate.b2.uop.fp_ctrl.ren2', 'io.lsu.brupdate.b2.uop.fp_ctrl.ren3', 'io.lsu.brupdate.b2.uop.fp_ctrl.sqrt', 'io.lsu.brupdate.b2.uop.fp_ctrl.swap12', 'io.lsu.brupdate.b2.uop.fp_ctrl.swap23', 'io.lsu.brupdate.b2.uop.fp_ctrl.toint', 'io.lsu.brupdate.b2.uop.fp_ctrl.typeTagIn', 'io.lsu.brupdate.b2.uop.fp_ctrl.typeTagOut', 'io.lsu.brupdate.b2.uop.fp_ctrl.vec', 'io.lsu.brupdate.b2.uop.fp_ctrl.wen', 'io.lsu.brupdate.b2.uop.fp_ctrl.wflags', 'io.lsu.brupdate.b2.uop.fp_rm', 'io.lsu.brupdate.b2.uop.fp_typ', 'io.lsu.brupdate.b2.uop.fp_val', 'io.lsu.brupdate.b2.uop.frs3_en', 'io.lsu.brupdate.b2.uop.ftq_idx', 'io.lsu.brupdate.b2.uop.fu_code[0]', 'io.lsu.brupdate.b2.uop.fu_code[1]', 'io.lsu.brupdate.b2.uop.fu_code[2]', 'io.lsu.brupdate.b2.uop.fu_code[3]', 'io.lsu.brupdate.b2.uop.fu_code[4]', 'io.lsu.brupdate.b2.uop.fu_code[5]', 'io.lsu.brupdate.b2.uop.fu_code[6]', 'io.lsu.brupdate.b2.uop.fu_code[7]', 'io.lsu.brupdate.b2.uop.fu_code[8]', 'io.lsu.brupdate.b2.uop.fu_code[9]', 'io.lsu.brupdate.b2.uop.imm_packed', 'io.lsu.brupdate.b2.uop.imm_rename', 'io.lsu.brupdate.b2.uop.imm_sel', 'io.lsu.brupdate.b2.uop.inst', 'io.lsu.brupdate.b2.uop.iq_type[0]', 'io.lsu.brupdate.b2.uop.iq_type[1]', 'io.lsu.brupdate.b2.uop.iq_type[2]', 'io.lsu.brupdate.b2.uop.iq_type[3]', 'io.lsu.brupdate.b2.uop.is_amo', 'io.lsu.brupdate.b2.uop.is_eret', 'io.lsu.brupdate.b2.uop.is_fence', 'io.lsu.brupdate.b2.uop.is_fencei', 'io.lsu.brupdate.b2.uop.is_mov', 'io.lsu.brupdate.b2.uop.is_rocc', 'io.lsu.brupdate.b2.uop.is_rvc', 'io.lsu.brupdate.b2.uop.is_sfb', 'io.lsu.brupdate.b2.uop.is_sfence', 'io.lsu.brupdate.b2.uop.is_sys_pc2epc', 'io.lsu.brupdate.b2.uop.is_unique', 'io.lsu.brupdate.b2.uop.iw_issued', 'io.lsu.brupdate.b2.uop.iw_issued_partial_agen', 'io.lsu.brupdate.b2.uop.iw_issued_partial_dgen', 'io.lsu.brupdate.b2.uop.iw_p1_bypass_hint', 'io.lsu.brupdate.b2.uop.iw_p1_speculative_child', 'io.lsu.brupdate.b2.uop.iw_p2_bypass_hint', 'io.lsu.brupdate.b2.uop.iw_p2_speculative_child', 'io.lsu.brupdate.b2.uop.iw_p3_bypass_hint', 'io.lsu.brupdate.b2.uop.ldq_idx', 'io.lsu.brupdate.b2.uop.ldst', 'io.lsu.brupdate.b2.uop.ldst_is_rs1', 'io.lsu.brupdate.b2.uop.lrs1', 'io.lsu.brupdate.b2.uop.lrs1_rtype', 'io.lsu.brupdate.b2.uop.lrs2', 'io.lsu.brupdate.b2.uop.lrs2_rtype', 'io.lsu.brupdate.b2.uop.lrs3', 'io.lsu.brupdate.b2.uop.mem_cmd', 'io.lsu.brupdate.b2.uop.mem_signed', 'io.lsu.brupdate.b2.uop.mem_size', 'io.lsu.brupdate.b2.uop.op1_sel', 'io.lsu.brupdate.b2.uop.op2_sel', 'io.lsu.brupdate.b2.uop.pc_lob', 'io.lsu.brupdate.b2.uop.pdst', 'io.lsu.brupdate.b2.uop.pimm', 'io.lsu.brupdate.b2.uop.ppred', 'io.lsu.brupdate.b2.uop.ppred_busy', 'io.lsu.brupdate.b2.uop.prs1', 'io.lsu.brupdate.b2.uop.prs1_busy', 'io.lsu.brupdate.b2.uop.prs2', 'io.lsu.brupdate.b2.uop.prs2_busy', 'io.lsu.brupdate.b2.uop.prs3', 'io.lsu.brupdate.b2.uop.prs3_busy', 'io.lsu.brupdate.b2.uop.rob_idx', 'io.lsu.brupdate.b2.uop.rxq_idx', 'io.lsu.brupdate.b2.uop.stale_pdst', 'io.lsu.brupdate.b2.uop.stq_idx', 'io.lsu.brupdate.b2.uop.taken', 'io.lsu.brupdate.b2.uop.uses_ldq', 'io.lsu.brupdate.b2.uop.uses_stq', 'io.lsu.brupdate.b2.uop.xcpt_ae_if', 'io.lsu.brupdate.b2.uop.xcpt_ma_if', 'io.lsu.brupdate.b2.uop.xcpt_pf_if', 'io.lsu.exception', 'io.lsu.force_order', 'io.lsu.ll_resp.bits.data', 'io.lsu.ll_resp.bits.is_hella', 'io.lsu.ll_resp.bits.uop.bp_debug_if', 'io.lsu.ll_resp.bits.uop.bp_xcpt_if', 'io.lsu.ll_resp.bits.uop.br_mask', 'io.lsu.ll_resp.bits.uop.br_tag', 'io.lsu.ll_resp.bits.uop.br_type', 'io.lsu.ll_resp.bits.uop.csr_cmd', 'io.lsu.ll_resp.bits.uop.debug_fsrc', 'io.lsu.ll_resp.bits.uop.debug_inst', 'io.lsu.ll_resp.bits.uop.debug_pc', 'io.lsu.ll_resp.bits.uop.debug_tsrc', 'io.lsu.ll_resp.bits.uop.dis_col_sel', 'io.lsu.ll_resp.bits.uop.dst_rtype', 'io.lsu.ll_resp.bits.uop.edge_inst', 'io.lsu.ll_resp.bits.uop.exc_cause', 'io.lsu.ll_resp.bits.uop.exception', 'io.lsu.ll_resp.bits.uop.fcn_dw', 'io.lsu.ll_resp.bits.uop.fcn_op', 'io.lsu.ll_resp.bits.uop.flush_on_commit', 'io.lsu.ll_resp.bits.uop.fp_ctrl.div', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fastpipe', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fma', 'io.lsu.ll_resp.bits.uop.fp_ctrl.fromint', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ldst', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren1', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren2', 'io.lsu.ll_resp.bits.uop.fp_ctrl.ren3', 'io.lsu.ll_resp.bits.uop.fp_ctrl.sqrt', 'io.lsu.ll_resp.bits.uop.fp_ctrl.swap12', 'io.lsu.ll_resp.bits.uop.fp_ctrl.swap23', 'io.lsu.ll_resp.bits.uop.fp_ctrl.toint', 'io.lsu.ll_resp.bits.uop.fp_ctrl.typeTagIn', 'io.lsu.ll_resp.bits.uop.fp_ctrl.typeTagOut', 'io.lsu.ll_resp.bits.uop.fp_ctrl.vec', 'io.lsu.ll_resp.bits.uop.fp_ctrl.wen', 'io.lsu.ll_resp.bits.uop.fp_ctrl.wflags', 'io.lsu.ll_resp.bits.uop.fp_rm', 'io.lsu.ll_resp.bits.uop.fp_typ', 'io.lsu.ll_resp.bits.uop.fp_val', 'io.lsu.ll_resp.bits.uop.frs3_en', 'io.lsu.ll_resp.bits.uop.ftq_idx', 'io.lsu.ll_resp.bits.uop.fu_code[0]', 'io.lsu.ll_resp.bits.uop.fu_code[1]', 'io.lsu.ll_resp.bits.uop.fu_code[2]', 'io.lsu.ll_resp.bits.uop.fu_code[3]', 'io.lsu.ll_resp.bits.uop.fu_code[4]', 'io.lsu.ll_resp.bits.uop.fu_code[5]', 'io.lsu.ll_resp.bits.uop.fu_code[6]', 'io.lsu.ll_resp.bits.uop.fu_code[7]', 'io.lsu.ll_resp.bits.uop.fu_code[8]', 'io.lsu.ll_resp.bits.uop.fu_code[9]', 'io.lsu.ll_resp.bits.uop.imm_packed', 'io.lsu.ll_resp.bits.uop.imm_rename', 'io.lsu.ll_resp.bits.uop.imm_sel', 'io.lsu.ll_resp.bits.uop.inst', 'io.lsu.ll_resp.bits.uop.iq_type[0]', 'io.lsu.ll_resp.bits.uop.iq_type[1]', 'io.lsu.ll_resp.bits.uop.iq_type[2]', 'io.lsu.ll_resp.bits.uop.iq_type[3]', 'io.lsu.ll_resp.bits.uop.is_amo', 'io.lsu.ll_resp.bits.uop.is_eret', 'io.lsu.ll_resp.bits.uop.is_fence', 'io.lsu.ll_resp.bits.uop.is_fencei', 'io.lsu.ll_resp.bits.uop.is_mov', 'io.lsu.ll_resp.bits.uop.is_rocc', 'io.lsu.ll_resp.bits.uop.is_rvc', 'io.lsu.ll_resp.bits.uop.is_sfb', 'io.lsu.ll_resp.bits.uop.is_sfence', 'io.lsu.ll_resp.bits.uop.is_sys_pc2epc', 'io.lsu.ll_resp.bits.uop.is_unique', 'io.lsu.ll_resp.bits.uop.iw_issued', 'io.lsu.ll_resp.bits.uop.iw_issued_partial_agen', 'io.lsu.ll_resp.bits.uop.iw_issued_partial_dgen', 'io.lsu.ll_resp.bits.uop.iw_p1_bypass_hint', 'io.lsu.ll_resp.bits.uop.iw_p1_speculative_child', 'io.lsu.ll_resp.bits.uop.iw_p2_bypass_hint', 'io.lsu.ll_resp.bits.uop.iw_p2_speculative_child', 'io.lsu.ll_resp.bits.uop.iw_p3_bypass_hint', 'io.lsu.ll_resp.bits.uop.ldq_idx', 'io.lsu.ll_resp.bits.uop.ldst', 'io.lsu.ll_resp.bits.uop.ldst_is_rs1', 'io.lsu.ll_resp.bits.uop.lrs1', 'io.lsu.ll_resp.bits.uop.lrs1_rtype', 'io.lsu.ll_resp.bits.uop.lrs2', 'io.lsu.ll_resp.bits.uop.lrs2_rtype', 'io.lsu.ll_resp.bits.uop.lrs3', 'io.lsu.ll_resp.bits.uop.mem_cmd', 'io.lsu.ll_resp.bits.uop.mem_signed', 'io.lsu.ll_resp.bits.uop.mem_size', 'io.lsu.ll_resp.bits.uop.op1_sel', 'io.lsu.ll_resp.bits.uop.op2_sel', 'io.lsu.ll_resp.bits.uop.pc_lob', 'io.lsu.ll_resp.bits.uop.pdst', 'io.lsu.ll_resp.bits.uop.pimm', 'io.lsu.ll_resp.bits.uop.ppred', 'io.lsu.ll_resp.bits.uop.ppred_busy', 'io.lsu.ll_resp.bits.uop.prs1', 'io.lsu.ll_resp.bits.uop.prs1_busy', 'io.lsu.ll_resp.bits.uop.prs2', 'io.lsu.ll_resp.bits.uop.prs2_busy', 'io.lsu.ll_resp.bits.uop.prs3', 'io.lsu.ll_resp.bits.uop.prs3_busy', 'io.lsu.ll_resp.bits.uop.rob_idx', 'io.lsu.ll_resp.bits.uop.rxq_idx', 'io.lsu.ll_resp.bits.uop.stale_pdst', 'io.lsu.ll_resp.bits.uop.stq_idx', 'io.lsu.ll_resp.bits.uop.taken', 'io.lsu.ll_resp.bits.uop.uses_ldq', 'io.lsu.ll_resp.bits.uop.uses_stq', 'io.lsu.ll_resp.bits.uop.xcpt_ae_if', 'io.lsu.ll_resp.bits.uop.xcpt_ma_if', 'io.lsu.ll_resp.bits.uop.xcpt_pf_if', 'io.lsu.ll_resp.ready', 'io.lsu.ll_resp.valid', 'io.lsu.nack[0].bits.addr', 'io.lsu.nack[0].bits.data', 'io.lsu.nack[0].bits.is_hella', 'io.lsu.nack[0].bits.uop.bp_debug_if', 'io.lsu.nack[0].bits.uop.bp_xcpt_if', 'io.lsu.nack[0].bits.uop.br_mask', 'io.lsu.nack[0].bits.uop.br_tag', 'io.lsu.nack[0].bits.uop.br_type', 'io.lsu.nack[0].bits.uop.csr_cmd', 'io.lsu.nack[0].bits.uop.debug_fsrc', 'io.lsu.nack[0].bits.uop.debug_inst', 'io.lsu.nack[0].bits.uop.debug_pc', 'io.lsu.nack[0].bits.uop.debug_tsrc', 'io.lsu.nack[0].bits.uop.dis_col_sel', 'io.lsu.nack[0].bits.uop.dst_rtype', 'io.lsu.nack[0].bits.uop.edge_inst', 'io.lsu.nack[0].bits.uop.exc_cause', 'io.lsu.nack[0].bits.uop.exception', 'io.lsu.nack[0].bits.uop.fcn_dw', 'io.lsu.nack[0].bits.uop.fcn_op', 'io.lsu.nack[0].bits.uop.flush_on_commit', 'io.lsu.nack[0].bits.uop.fp_ctrl.div', 'io.lsu.nack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.nack[0].bits.uop.fp_ctrl.fma', 'io.lsu.nack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.nack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.nack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.nack[0].bits.uop.fp_ctrl.toint', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.nack[0].bits.uop.fp_ctrl.vec', 'io.lsu.nack[0].bits.uop.fp_ctrl.wen', 'io.lsu.nack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.nack[0].bits.uop.fp_rm', 'io.lsu.nack[0].bits.uop.fp_typ', 'io.lsu.nack[0].bits.uop.fp_val', 'io.lsu.nack[0].bits.uop.frs3_en', 'io.lsu.nack[0].bits.uop.ftq_idx', 'io.lsu.nack[0].bits.uop.fu_code[0]', 'io.lsu.nack[0].bits.uop.fu_code[1]', 'io.lsu.nack[0].bits.uop.fu_code[2]', 'io.lsu.nack[0].bits.uop.fu_code[3]', 'io.lsu.nack[0].bits.uop.fu_code[4]', 'io.lsu.nack[0].bits.uop.fu_code[5]', 'io.lsu.nack[0].bits.uop.fu_code[6]', 'io.lsu.nack[0].bits.uop.fu_code[7]', 'io.lsu.nack[0].bits.uop.fu_code[8]', 'io.lsu.nack[0].bits.uop.fu_code[9]', 'io.lsu.nack[0].bits.uop.imm_packed', 'io.lsu.nack[0].bits.uop.imm_rename', 'io.lsu.nack[0].bits.uop.imm_sel', 'io.lsu.nack[0].bits.uop.inst', 'io.lsu.nack[0].bits.uop.iq_type[0]', 'io.lsu.nack[0].bits.uop.iq_type[1]', 'io.lsu.nack[0].bits.uop.iq_type[2]', 'io.lsu.nack[0].bits.uop.iq_type[3]', 'io.lsu.nack[0].bits.uop.is_amo', 'io.lsu.nack[0].bits.uop.is_eret', 'io.lsu.nack[0].bits.uop.is_fence', 'io.lsu.nack[0].bits.uop.is_fencei', 'io.lsu.nack[0].bits.uop.is_mov', 'io.lsu.nack[0].bits.uop.is_rocc', 'io.lsu.nack[0].bits.uop.is_rvc', 'io.lsu.nack[0].bits.uop.is_sfb', 'io.lsu.nack[0].bits.uop.is_sfence', 'io.lsu.nack[0].bits.uop.is_sys_pc2epc', 'io.lsu.nack[0].bits.uop.is_unique', 'io.lsu.nack[0].bits.uop.iw_issued', 'io.lsu.nack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.nack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.nack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.nack[0].bits.uop.ldq_idx', 'io.lsu.nack[0].bits.uop.ldst', 'io.lsu.nack[0].bits.uop.ldst_is_rs1', 'io.lsu.nack[0].bits.uop.lrs1', 'io.lsu.nack[0].bits.uop.lrs1_rtype', 'io.lsu.nack[0].bits.uop.lrs2', 'io.lsu.nack[0].bits.uop.lrs2_rtype', 'io.lsu.nack[0].bits.uop.lrs3', 'io.lsu.nack[0].bits.uop.mem_cmd', 'io.lsu.nack[0].bits.uop.mem_signed', 'io.lsu.nack[0].bits.uop.mem_size', 'io.lsu.nack[0].bits.uop.op1_sel', 'io.lsu.nack[0].bits.uop.op2_sel', 'io.lsu.nack[0].bits.uop.pc_lob', 'io.lsu.nack[0].bits.uop.pdst', 'io.lsu.nack[0].bits.uop.pimm', 'io.lsu.nack[0].bits.uop.ppred', 'io.lsu.nack[0].bits.uop.ppred_busy', 'io.lsu.nack[0].bits.uop.prs1', 'io.lsu.nack[0].bits.uop.prs1_busy', 'io.lsu.nack[0].bits.uop.prs2', 'io.lsu.nack[0].bits.uop.prs2_busy', 'io.lsu.nack[0].bits.uop.prs3', 'io.lsu.nack[0].bits.uop.prs3_busy', 'io.lsu.nack[0].bits.uop.rob_idx', 'io.lsu.nack[0].bits.uop.rxq_idx', 'io.lsu.nack[0].bits.uop.stale_pdst', 'io.lsu.nack[0].bits.uop.stq_idx', 'io.lsu.nack[0].bits.uop.taken', 'io.lsu.nack[0].bits.uop.uses_ldq', 'io.lsu.nack[0].bits.uop.uses_stq', 'io.lsu.nack[0].bits.uop.xcpt_ae_if', 'io.lsu.nack[0].bits.uop.xcpt_ma_if', 'io.lsu.nack[0].bits.uop.xcpt_pf_if', 'io.lsu.nack[0].valid', 'io.lsu.ordered', 'io.lsu.perf.acquire', 'io.lsu.perf.release', 'io.lsu.release.bits.address', 'io.lsu.release.bits.corrupt', 'io.lsu.release.bits.data', 'io.lsu.release.bits.opcode', 'io.lsu.release.bits.param', 'io.lsu.release.bits.size', 'io.lsu.release.bits.source', 'io.lsu.release.ready', 'io.lsu.release.valid', 'io.lsu.req.bits[0].bits.addr', 'io.lsu.req.bits[0].valid', 'io.lsu.req.ready', 'io.lsu.req.valid', 'io.lsu.resp[0].bits.data', 'io.lsu.resp[0].bits.is_hella', 'io.lsu.resp[0].bits.uop.bp_debug_if', 'io.lsu.resp[0].bits.uop.bp_xcpt_if', 'io.lsu.resp[0].bits.uop.br_mask', 'io.lsu.resp[0].bits.uop.br_tag', 'io.lsu.resp[0].bits.uop.br_type', 'io.lsu.resp[0].bits.uop.csr_cmd', 'io.lsu.resp[0].bits.uop.debug_fsrc', 'io.lsu.resp[0].bits.uop.debug_inst', 'io.lsu.resp[0].bits.uop.debug_pc', 'io.lsu.resp[0].bits.uop.debug_tsrc', 'io.lsu.resp[0].bits.uop.dis_col_sel', 'io.lsu.resp[0].bits.uop.dst_rtype', 'io.lsu.resp[0].bits.uop.edge_inst', 'io.lsu.resp[0].bits.uop.exc_cause', 'io.lsu.resp[0].bits.uop.exception', 'io.lsu.resp[0].bits.uop.fcn_dw', 'io.lsu.resp[0].bits.uop.fcn_op', 'io.lsu.resp[0].bits.uop.flush_on_commit', 'io.lsu.resp[0].bits.uop.fp_ctrl.div', 'io.lsu.resp[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.resp[0].bits.uop.fp_ctrl.fma', 'io.lsu.resp[0].bits.uop.fp_ctrl.fromint', 'io.lsu.resp[0].bits.uop.fp_ctrl.ldst', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren1', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren2', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren3', 'io.lsu.resp[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap12', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap23', 'io.lsu.resp[0].bits.uop.fp_ctrl.toint', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.resp[0].bits.uop.fp_ctrl.vec', 'io.lsu.resp[0].bits.uop.fp_ctrl.wen', 'io.lsu.resp[0].bits.uop.fp_ctrl.wflags', 'io.lsu.resp[0].bits.uop.fp_rm', 'io.lsu.resp[0].bits.uop.fp_typ', 'io.lsu.resp[0].bits.uop.fp_val', 'io.lsu.resp[0].bits.uop.frs3_en', 'io.lsu.resp[0].bits.uop.ftq_idx', 'io.lsu.resp[0].bits.uop.fu_code[0]', 'io.lsu.resp[0].bits.uop.fu_code[1]', 'io.lsu.resp[0].bits.uop.fu_code[2]', 'io.lsu.resp[0].bits.uop.fu_code[3]', 'io.lsu.resp[0].bits.uop.fu_code[4]', 'io.lsu.resp[0].bits.uop.fu_code[5]', 'io.lsu.resp[0].bits.uop.fu_code[6]', 'io.lsu.resp[0].bits.uop.fu_code[7]', 'io.lsu.resp[0].bits.uop.fu_code[8]', 'io.lsu.resp[0].bits.uop.fu_code[9]', 'io.lsu.resp[0].bits.uop.imm_packed', 'io.lsu.resp[0].bits.uop.imm_rename', 'io.lsu.resp[0].bits.uop.imm_sel', 'io.lsu.resp[0].bits.uop.inst', 'io.lsu.resp[0].bits.uop.iq_type[0]', 'io.lsu.resp[0].bits.uop.iq_type[1]', 'io.lsu.resp[0].bits.uop.iq_type[2]', 'io.lsu.resp[0].bits.uop.iq_type[3]', 'io.lsu.resp[0].bits.uop.is_amo', 'io.lsu.resp[0].bits.uop.is_eret', 'io.lsu.resp[0].bits.uop.is_fence', 'io.lsu.resp[0].bits.uop.is_fencei', 'io.lsu.resp[0].bits.uop.is_mov', 'io.lsu.resp[0].bits.uop.is_rocc', 'io.lsu.resp[0].bits.uop.is_rvc', 'io.lsu.resp[0].bits.uop.is_sfb', 'io.lsu.resp[0].bits.uop.is_sfence', 'io.lsu.resp[0].bits.uop.is_sys_pc2epc', 'io.lsu.resp[0].bits.uop.is_unique', 'io.lsu.resp[0].bits.uop.iw_issued', 'io.lsu.resp[0].bits.uop.iw_issued_partial_agen', 'io.lsu.resp[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.resp[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p1_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p2_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.resp[0].bits.uop.ldq_idx', 'io.lsu.resp[0].bits.uop.ldst', 'io.lsu.resp[0].bits.uop.ldst_is_rs1', 'io.lsu.resp[0].bits.uop.lrs1', 'io.lsu.resp[0].bits.uop.lrs1_rtype', 'io.lsu.resp[0].bits.uop.lrs2', 'io.lsu.resp[0].bits.uop.lrs2_rtype', 'io.lsu.resp[0].bits.uop.lrs3', 'io.lsu.resp[0].bits.uop.mem_cmd', 'io.lsu.resp[0].bits.uop.mem_signed', 'io.lsu.resp[0].bits.uop.mem_size', 'io.lsu.resp[0].bits.uop.op1_sel', 'io.lsu.resp[0].bits.uop.op2_sel', 'io.lsu.resp[0].bits.uop.pc_lob', 'io.lsu.resp[0].bits.uop.pdst', 'io.lsu.resp[0].bits.uop.pimm', 'io.lsu.resp[0].bits.uop.ppred', 'io.lsu.resp[0].bits.uop.ppred_busy', 'io.lsu.resp[0].bits.uop.prs1', 'io.lsu.resp[0].bits.uop.prs1_busy', 'io.lsu.resp[0].bits.uop.prs2', 'io.lsu.resp[0].bits.uop.prs2_busy', 'io.lsu.resp[0].bits.uop.prs3', 'io.lsu.resp[0].bits.uop.prs3_busy', 'io.lsu.resp[0].bits.uop.rob_idx', 'io.lsu.resp[0].bits.uop.rxq_idx', 'io.lsu.resp[0].bits.uop.stale_pdst', 'io.lsu.resp[0].bits.uop.stq_idx', 'io.lsu.resp[0].bits.uop.taken', 'io.lsu.resp[0].bits.uop.uses_ldq', 'io.lsu.resp[0].bits.uop.uses_stq', 'io.lsu.resp[0].bits.uop.xcpt_ae_if', 'io.lsu.resp[0].bits.uop.xcpt_ma_if', 'io.lsu.resp[0].bits.uop.xcpt_pf_if', 'io.lsu.resp[0].valid', 'io.lsu.rob_head_idx', 'io.lsu.rob_pnr_idx', 'io.lsu.s1_kill[0]', 'io.lsu.s1_nack_advisory[0]', 'io.lsu.store_ack[0].bits.addr', 'io.lsu.store_ack[0].bits.data', 'io.lsu.store_ack[0].bits.is_hella', 'io.lsu.store_ack[0].bits.uop.bp_debug_if', 'io.lsu.store_ack[0].bits.uop.bp_xcpt_if', 'io.lsu.store_ack[0].bits.uop.br_mask', 'io.lsu.store_ack[0].bits.uop.br_tag', 'io.lsu.store_ack[0].bits.uop.br_type', 'io.lsu.store_ack[0].bits.uop.csr_cmd', 'io.lsu.store_ack[0].bits.uop.debug_fsrc', 'io.lsu.store_ack[0].bits.uop.debug_inst', 'io.lsu.store_ack[0].bits.uop.debug_pc', 'io.lsu.store_ack[0].bits.uop.debug_tsrc', 'io.lsu.store_ack[0].bits.uop.dis_col_sel', 'io.lsu.store_ack[0].bits.uop.dst_rtype', 'io.lsu.store_ack[0].bits.uop.edge_inst', 'io.lsu.store_ack[0].bits.uop.exc_cause', 'io.lsu.store_ack[0].bits.uop.exception', 'io.lsu.store_ack[0].bits.uop.fcn_dw', 'io.lsu.store_ack[0].bits.uop.fcn_op', 'io.lsu.store_ack[0].bits.uop.flush_on_commit', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.div', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fma', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.toint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.vec', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wen', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.store_ack[0].bits.uop.fp_rm', 'io.lsu.store_ack[0].bits.uop.fp_typ', 'io.lsu.store_ack[0].bits.uop.fp_val', 'io.lsu.store_ack[0].bits.uop.frs3_en', 'io.lsu.store_ack[0].bits.uop.ftq_idx', 'io.lsu.store_ack[0].bits.uop.fu_code[0]', 'io.lsu.store_ack[0].bits.uop.fu_code[1]', 'io.lsu.store_ack[0].bits.uop.fu_code[2]', 'io.lsu.store_ack[0].bits.uop.fu_code[3]', 'io.lsu.store_ack[0].bits.uop.fu_code[4]', 'io.lsu.store_ack[0].bits.uop.fu_code[5]', 'io.lsu.store_ack[0].bits.uop.fu_code[6]', 'io.lsu.store_ack[0].bits.uop.fu_code[7]', 'io.lsu.store_ack[0].bits.uop.fu_code[8]', 'io.lsu.store_ack[0].bits.uop.fu_code[9]', 'io.lsu.store_ack[0].bits.uop.imm_packed', 'io.lsu.store_ack[0].bits.uop.imm_rename', 'io.lsu.store_ack[0].bits.uop.imm_sel', 'io.lsu.store_ack[0].bits.uop.inst', 'io.lsu.store_ack[0].bits.uop.iq_type[0]', 'io.lsu.store_ack[0].bits.uop.iq_type[1]', 'io.lsu.store_ack[0].bits.uop.iq_type[2]', 'io.lsu.store_ack[0].bits.uop.iq_type[3]', 'io.lsu.store_ack[0].bits.uop.is_amo', 'io.lsu.store_ack[0].bits.uop.is_eret', 'io.lsu.store_ack[0].bits.uop.is_fence', 'io.lsu.store_ack[0].bits.uop.is_fencei', 'io.lsu.store_ack[0].bits.uop.is_mov', 'io.lsu.store_ack[0].bits.uop.is_rocc', 'io.lsu.store_ack[0].bits.uop.is_rvc', 'io.lsu.store_ack[0].bits.uop.is_sfb', 'io.lsu.store_ack[0].bits.uop.is_sfence', 'io.lsu.store_ack[0].bits.uop.is_sys_pc2epc', 'io.lsu.store_ack[0].bits.uop.is_unique', 'io.lsu.store_ack[0].bits.uop.iw_issued', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.store_ack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.store_ack[0].bits.uop.ldq_idx', 'io.lsu.store_ack[0].bits.uop.ldst', 'io.lsu.store_ack[0].bits.uop.ldst_is_rs1', 'io.lsu.store_ack[0].bits.uop.lrs1', 'io.lsu.store_ack[0].bits.uop.lrs1_rtype', 'io.lsu.store_ack[0].bits.uop.lrs2', 'io.lsu.store_ack[0].bits.uop.lrs2_rtype', 'io.lsu.store_ack[0].bits.uop.lrs3', 'io.lsu.store_ack[0].bits.uop.mem_cmd', 'io.lsu.store_ack[0].bits.uop.mem_signed', 'io.lsu.store_ack[0].bits.uop.mem_size', 'io.lsu.store_ack[0].bits.uop.op1_sel', 'io.lsu.store_ack[0].bits.uop.op2_sel', 'io.lsu.store_ack[0].bits.uop.pc_lob', 'io.lsu.store_ack[0].bits.uop.pdst', 'io.lsu.store_ack[0].bits.uop.pimm', 'io.lsu.store_ack[0].bits.uop.ppred', 'io.lsu.store_ack[0].bits.uop.ppred_busy', 'io.lsu.store_ack[0].bits.uop.prs1', 'io.lsu.store_ack[0].bits.uop.prs1_busy', 'io.lsu.store_ack[0].bits.uop.prs2', 'io.lsu.store_ack[0].bits.uop.prs2_busy', 'io.lsu.store_ack[0].bits.uop.prs3', 'io.lsu.store_ack[0].bits.uop.prs3_busy', 'io.lsu.store_ack[0].bits.uop.rob_idx', 'io.lsu.store_ack[0].bits.uop.rxq_idx', 'io.lsu.store_ack[0].bits.uop.stale_pdst', 'io.lsu.store_ack[0].bits.uop.stq_idx', 'io.lsu.store_ack[0].bits.uop.taken', 'io.lsu.store_ack[0].bits.uop.uses_ldq', 'io.lsu.store_ack[0].bits.uop.uses_stq', 'io.lsu.store_ack[0].bits.uop.xcpt_ae_if', 'io.lsu.store_ack[0].bits.uop.xcpt_ma_if', 'io.lsu.store_ack[0].bits.uop.xcpt_pf_if', 'io.lsu.store_ack[0].valid', 'lfsr_prng.clock', 'lfsr_prng.io.increment', 'lfsr_prng.io.out[0]', 'lfsr_prng.io.out[10]', 'lfsr_prng.io.out[11]', 'lfsr_prng.io.out[12]', 'lfsr_prng.io.out[13]', 'lfsr_prng.io.out[14]', 'lfsr_prng.io.out[15]', 'lfsr_prng.io.out[1]', 'lfsr_prng.io.out[2]', 'lfsr_prng.io.out[3]', 'lfsr_prng.io.out[4]', 'lfsr_prng.io.out[5]', 'lfsr_prng.io.out[6]', 'lfsr_prng.io.out[7]', 'lfsr_prng.io.out[8]', 'lfsr_prng.io.out[9]', 'lfsr_prng.io.seed.bits[0]', 'lfsr_prng.io.seed.bits[10]', 'lfsr_prng.io.seed.bits[11]', 'lfsr_prng.io.seed.bits[12]', 'lfsr_prng.io.seed.bits[13]', 'lfsr_prng.io.seed.bits[14]', 'lfsr_prng.io.seed.bits[15]', 'lfsr_prng.io.seed.bits[1]', 'lfsr_prng.io.seed.bits[2]', 'lfsr_prng.io.seed.bits[3]', 'lfsr_prng.io.seed.bits[4]', 'lfsr_prng.io.seed.bits[5]', 'lfsr_prng.io.seed.bits[6]', 'lfsr_prng.io.seed.bits[7]', 'lfsr_prng.io.seed.bits[8]', 'lfsr_prng.io.seed.bits[9]', 'lfsr_prng.io.seed.valid', 'lfsr_prng.reset', 'lsu_release_arb.clock', 'lsu_release_arb.io.in[0].bits.address', 'lsu_release_arb.io.in[0].bits.corrupt', 'lsu_release_arb.io.in[0].bits.data', 'lsu_release_arb.io.in[0].bits.opcode', 'lsu_release_arb.io.in[0].bits.param', 'lsu_release_arb.io.in[0].bits.size', 'lsu_release_arb.io.in[0].bits.source', 'lsu_release_arb.io.in[0].ready', 'lsu_release_arb.io.in[0].valid', 'lsu_release_arb.io.in[1].bits.address', 'lsu_release_arb.io.in[1].bits.corrupt', 'lsu_release_arb.io.in[1].bits.data', 'lsu_release_arb.io.in[1].bits.opcode', 'lsu_release_arb.io.in[1].bits.param', 'lsu_release_arb.io.in[1].bits.size', 'lsu_release_arb.io.in[1].bits.source', 'lsu_release_arb.io.in[1].ready', 'lsu_release_arb.io.in[1].valid', 'lsu_release_arb.io.out.ready', 'lsu_release_arb.io.out.valid', 'lsu_release_arb.reset', 'metaReadArb.clock', 'metaReadArb.io.in[0].bits.req[0].idx', 'metaReadArb.io.in[0].bits.req[0].tag', 'metaReadArb.io.in[0].bits.req[0].way_en', 'metaReadArb.io.in[0].ready', 'metaReadArb.io.in[0].valid', 'metaReadArb.io.in[1].bits.req[0].idx', 'metaReadArb.io.in[1].bits.req[0].tag', 'metaReadArb.io.in[1].bits.req[0].way_en', 'metaReadArb.io.in[1].ready', 'metaReadArb.io.in[1].valid', 'metaReadArb.io.in[2].bits.req[0].idx', 'metaReadArb.io.in[2].bits.req[0].tag', 'metaReadArb.io.in[2].bits.req[0].way_en', 'metaReadArb.io.in[2].ready', 'metaReadArb.io.in[2].valid', 'metaReadArb.io.in[3].bits.req[0].idx', 'metaReadArb.io.in[3].bits.req[0].tag', 'metaReadArb.io.in[3].bits.req[0].way_en', 'metaReadArb.io.in[3].ready', 'metaReadArb.io.in[3].valid', 'metaReadArb.io.in[4].bits.req[0].idx', 'metaReadArb.io.in[4].bits.req[0].tag', 'metaReadArb.io.in[4].bits.req[0].way_en', 'metaReadArb.io.in[4].ready', 'metaReadArb.io.in[4].valid', 'metaReadArb.io.in[5].bits.req[0].idx', 'metaReadArb.io.in[5].bits.req[0].tag', 'metaReadArb.io.in[5].bits.req[0].way_en', 'metaReadArb.io.in[5].ready', 'metaReadArb.io.in[5].valid', 'metaReadArb.io.out.bits.req[0].idx', 'metaReadArb.io.out.bits.req[0].tag', 'metaReadArb.io.out.bits.req[0].way_en', 'metaReadArb.io.out.ready', 'metaReadArb.io.out.valid', 'metaReadArb.reset', 'metaWriteArb.clock', 'metaWriteArb.io.in[0].bits.data.coh.state', 'metaWriteArb.io.in[0].bits.data.tag', 'metaWriteArb.io.in[0].bits.idx', 'metaWriteArb.io.in[0].bits.tag', 'metaWriteArb.io.in[0].bits.way_en', 'metaWriteArb.io.in[0].ready', 'metaWriteArb.io.in[0].valid', 'metaWriteArb.io.in[1].bits.data.coh.state', 'metaWriteArb.io.in[1].bits.data.tag', 'metaWriteArb.io.in[1].bits.idx', 'metaWriteArb.io.in[1].bits.tag', 'metaWriteArb.io.in[1].bits.way_en', 'metaWriteArb.io.in[1].ready', 'metaWriteArb.io.in[1].valid', 'metaWriteArb.io.out.bits.data.coh.state', 'metaWriteArb.io.out.bits.data.tag', 'metaWriteArb.io.out.bits.idx', 'metaWriteArb.io.out.bits.tag', 'metaWriteArb.io.out.bits.way_en', 'metaWriteArb.io.out.ready', 'metaWriteArb.io.out.valid', 'metaWriteArb.reset', 'meta_0.clock', 'meta_0.io.read.bits.idx', 'meta_0.io.read.bits.tag', 'meta_0.io.read.bits.way_en', 'meta_0.io.read.ready', 'meta_0.io.read.valid', 'meta_0.io.resp[0].coh.state', 'meta_0.io.resp[0].tag', 'meta_0.io.resp[1].coh.state', 'meta_0.io.resp[1].tag', 'meta_0.io.resp[2].coh.state', 'meta_0.io.resp[2].tag', 'meta_0.io.resp[3].coh.state', 'meta_0.io.resp[3].tag', 'meta_0.io.write.bits.data.coh.state', 'meta_0.io.write.bits.data.tag', 'meta_0.io.write.bits.idx', 'meta_0.io.write.bits.tag', 'meta_0.io.write.bits.way_en', 'meta_0.io.write.ready', 'meta_0.io.write.valid', 'meta_0.reset', 'mshrs.clock', 'mshrs.io.block_hit[0]', 'mshrs.io.brupdate.b1.mispredict_mask', 'mshrs.io.brupdate.b1.resolve_mask', 'mshrs.io.brupdate.b2.cfi_type', 'mshrs.io.brupdate.b2.jalr_target', 'mshrs.io.brupdate.b2.mispredict', 'mshrs.io.brupdate.b2.pc_sel', 'mshrs.io.brupdate.b2.taken', 'mshrs.io.brupdate.b2.target_offset', 'mshrs.io.brupdate.b2.uop.bp_debug_if', 'mshrs.io.brupdate.b2.uop.bp_xcpt_if', 'mshrs.io.brupdate.b2.uop.br_mask', 'mshrs.io.brupdate.b2.uop.br_tag', 'mshrs.io.brupdate.b2.uop.br_type', 'mshrs.io.brupdate.b2.uop.csr_cmd', 'mshrs.io.brupdate.b2.uop.debug_fsrc', 'mshrs.io.brupdate.b2.uop.debug_inst', 'mshrs.io.brupdate.b2.uop.debug_pc', 'mshrs.io.brupdate.b2.uop.debug_tsrc', 'mshrs.io.brupdate.b2.uop.dis_col_sel', 'mshrs.io.brupdate.b2.uop.dst_rtype', 'mshrs.io.brupdate.b2.uop.edge_inst', 'mshrs.io.brupdate.b2.uop.exc_cause', 'mshrs.io.brupdate.b2.uop.exception', 'mshrs.io.brupdate.b2.uop.fcn_dw', 'mshrs.io.brupdate.b2.uop.fcn_op', 'mshrs.io.brupdate.b2.uop.flush_on_commit', 'mshrs.io.brupdate.b2.uop.fp_ctrl.div', 'mshrs.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'mshrs.io.brupdate.b2.uop.fp_ctrl.fma', 'mshrs.io.brupdate.b2.uop.fp_ctrl.fromint', 'mshrs.io.brupdate.b2.uop.fp_ctrl.ldst', 'mshrs.io.brupdate.b2.uop.fp_ctrl.ren1', 'mshrs.io.brupdate.b2.uop.fp_ctrl.ren2', 'mshrs.io.brupdate.b2.uop.fp_ctrl.ren3', 'mshrs.io.brupdate.b2.uop.fp_ctrl.sqrt', 'mshrs.io.brupdate.b2.uop.fp_ctrl.swap12', 'mshrs.io.brupdate.b2.uop.fp_ctrl.swap23', 'mshrs.io.brupdate.b2.uop.fp_ctrl.toint', 'mshrs.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'mshrs.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'mshrs.io.brupdate.b2.uop.fp_ctrl.vec', 'mshrs.io.brupdate.b2.uop.fp_ctrl.wen', 'mshrs.io.brupdate.b2.uop.fp_ctrl.wflags', 'mshrs.io.brupdate.b2.uop.fp_rm', 'mshrs.io.brupdate.b2.uop.fp_typ', 'mshrs.io.brupdate.b2.uop.fp_val', 'mshrs.io.brupdate.b2.uop.frs3_en', 'mshrs.io.brupdate.b2.uop.ftq_idx', 'mshrs.io.brupdate.b2.uop.fu_code[0]', 'mshrs.io.brupdate.b2.uop.fu_code[1]', 'mshrs.io.brupdate.b2.uop.fu_code[2]', 'mshrs.io.brupdate.b2.uop.fu_code[3]', 'mshrs.io.brupdate.b2.uop.fu_code[4]', 'mshrs.io.brupdate.b2.uop.fu_code[5]', 'mshrs.io.brupdate.b2.uop.fu_code[6]', 'mshrs.io.brupdate.b2.uop.fu_code[7]', 'mshrs.io.brupdate.b2.uop.fu_code[8]', 'mshrs.io.brupdate.b2.uop.fu_code[9]', 'mshrs.io.brupdate.b2.uop.imm_packed', 'mshrs.io.brupdate.b2.uop.imm_rename', 'mshrs.io.brupdate.b2.uop.imm_sel', 'mshrs.io.brupdate.b2.uop.inst', 'mshrs.io.brupdate.b2.uop.iq_type[0]', 'mshrs.io.brupdate.b2.uop.iq_type[1]', 'mshrs.io.brupdate.b2.uop.iq_type[2]', 'mshrs.io.brupdate.b2.uop.iq_type[3]', 'mshrs.io.brupdate.b2.uop.is_amo', 'mshrs.io.brupdate.b2.uop.is_eret', 'mshrs.io.brupdate.b2.uop.is_fence', 'mshrs.io.brupdate.b2.uop.is_fencei', 'mshrs.io.brupdate.b2.uop.is_mov', 'mshrs.io.brupdate.b2.uop.is_rocc', 'mshrs.io.brupdate.b2.uop.is_rvc', 'mshrs.io.brupdate.b2.uop.is_sfb', 'mshrs.io.brupdate.b2.uop.is_sfence', 'mshrs.io.brupdate.b2.uop.is_sys_pc2epc', 'mshrs.io.brupdate.b2.uop.is_unique', 'mshrs.io.brupdate.b2.uop.iw_issued', 'mshrs.io.brupdate.b2.uop.iw_issued_partial_agen', 'mshrs.io.brupdate.b2.uop.iw_issued_partial_dgen', 'mshrs.io.brupdate.b2.uop.iw_p1_bypass_hint', 'mshrs.io.brupdate.b2.uop.iw_p1_speculative_child', 'mshrs.io.brupdate.b2.uop.iw_p2_bypass_hint', 'mshrs.io.brupdate.b2.uop.iw_p2_speculative_child', 'mshrs.io.brupdate.b2.uop.iw_p3_bypass_hint', 'mshrs.io.brupdate.b2.uop.ldq_idx', 'mshrs.io.brupdate.b2.uop.ldst', 'mshrs.io.brupdate.b2.uop.ldst_is_rs1', 'mshrs.io.brupdate.b2.uop.lrs1', 'mshrs.io.brupdate.b2.uop.lrs1_rtype', 'mshrs.io.brupdate.b2.uop.lrs2', 'mshrs.io.brupdate.b2.uop.lrs2_rtype', 'mshrs.io.brupdate.b2.uop.lrs3', 'mshrs.io.brupdate.b2.uop.mem_cmd', 'mshrs.io.brupdate.b2.uop.mem_signed', 'mshrs.io.brupdate.b2.uop.mem_size', 'mshrs.io.brupdate.b2.uop.op1_sel', 'mshrs.io.brupdate.b2.uop.op2_sel', 'mshrs.io.brupdate.b2.uop.pc_lob', 'mshrs.io.brupdate.b2.uop.pdst', 'mshrs.io.brupdate.b2.uop.pimm', 'mshrs.io.brupdate.b2.uop.ppred', 'mshrs.io.brupdate.b2.uop.ppred_busy', 'mshrs.io.brupdate.b2.uop.prs1', 'mshrs.io.brupdate.b2.uop.prs1_busy', 'mshrs.io.brupdate.b2.uop.prs2', 'mshrs.io.brupdate.b2.uop.prs2_busy', 'mshrs.io.brupdate.b2.uop.prs3', 'mshrs.io.brupdate.b2.uop.prs3_busy', 'mshrs.io.brupdate.b2.uop.rob_idx', 'mshrs.io.brupdate.b2.uop.rxq_idx', 'mshrs.io.brupdate.b2.uop.stale_pdst', 'mshrs.io.brupdate.b2.uop.stq_idx', 'mshrs.io.brupdate.b2.uop.taken', 'mshrs.io.brupdate.b2.uop.uses_ldq', 'mshrs.io.brupdate.b2.uop.uses_stq', 'mshrs.io.brupdate.b2.uop.xcpt_ae_if', 'mshrs.io.brupdate.b2.uop.xcpt_ma_if', 'mshrs.io.brupdate.b2.uop.xcpt_pf_if', 'mshrs.io.clear_all', 'mshrs.io.exception', 'mshrs.io.fence_rdy', 'mshrs.io.mem_acquire.ready', 'mshrs.io.mem_acquire.valid', 'mshrs.io.mem_finish.ready', 'mshrs.io.mem_finish.valid', 'mshrs.io.mem_grant.bits.corrupt', 'mshrs.io.mem_grant.bits.data', 'mshrs.io.mem_grant.bits.denied', 'mshrs.io.mem_grant.bits.opcode', 'mshrs.io.mem_grant.bits.param', 'mshrs.io.mem_grant.bits.sink', 'mshrs.io.mem_grant.bits.size', 'mshrs.io.mem_grant.bits.source', 'mshrs.io.mem_grant.ready', 'mshrs.io.mem_grant.valid', 'mshrs.io.meta_read.bits.idx', 'mshrs.io.meta_read.bits.tag', 'mshrs.io.meta_read.bits.way_en', 'mshrs.io.meta_read.ready', 'mshrs.io.meta_read.valid', 'mshrs.io.meta_resp.bits.coh.state', 'mshrs.io.meta_resp.bits.tag', 'mshrs.io.meta_resp.valid', 'mshrs.io.prefetch.bits.addr', 'mshrs.io.prefetch.ready', 'mshrs.io.prefetch.valid', 'mshrs.io.probe_rdy', 'mshrs.io.prober_state.bits', 'mshrs.io.prober_state.valid', 'mshrs.io.replay.bits.addr', 'mshrs.io.replay.bits.data', 'mshrs.io.replay.bits.is_hella', 'mshrs.io.replay.bits.uop.mem_cmd', 'mshrs.io.replay.bits.way_en', 'mshrs.io.replay.ready', 'mshrs.io.replay.valid', 'mshrs.io.req[0].bits.addr', 'mshrs.io.req[0].bits.data', 'mshrs.io.req[0].bits.is_hella', 'mshrs.io.req[0].bits.old_meta.coh.state', 'mshrs.io.req[0].bits.old_meta.tag', 'mshrs.io.req[0].bits.sdq_id', 'mshrs.io.req[0].bits.tag_match', 'mshrs.io.req[0].bits.uop.bp_debug_if', 'mshrs.io.req[0].bits.uop.bp_xcpt_if', 'mshrs.io.req[0].bits.uop.br_mask', 'mshrs.io.req[0].bits.uop.br_tag', 'mshrs.io.req[0].bits.uop.br_type', 'mshrs.io.req[0].bits.uop.csr_cmd', 'mshrs.io.req[0].bits.uop.debug_fsrc', 'mshrs.io.req[0].bits.uop.debug_inst', 'mshrs.io.req[0].bits.uop.debug_pc', 'mshrs.io.req[0].bits.uop.debug_tsrc', 'mshrs.io.req[0].bits.uop.dis_col_sel', 'mshrs.io.req[0].bits.uop.dst_rtype', 'mshrs.io.req[0].bits.uop.edge_inst', 'mshrs.io.req[0].bits.uop.exc_cause', 'mshrs.io.req[0].bits.uop.exception', 'mshrs.io.req[0].bits.uop.fcn_dw', 'mshrs.io.req[0].bits.uop.fcn_op', 'mshrs.io.req[0].bits.uop.flush_on_commit', 'mshrs.io.req[0].bits.uop.fp_ctrl.div', 'mshrs.io.req[0].bits.uop.fp_ctrl.fastpipe', 'mshrs.io.req[0].bits.uop.fp_ctrl.fma', 'mshrs.io.req[0].bits.uop.fp_ctrl.fromint', 'mshrs.io.req[0].bits.uop.fp_ctrl.ldst', 'mshrs.io.req[0].bits.uop.fp_ctrl.ren1', 'mshrs.io.req[0].bits.uop.fp_ctrl.ren2', 'mshrs.io.req[0].bits.uop.fp_ctrl.ren3', 'mshrs.io.req[0].bits.uop.fp_ctrl.sqrt', 'mshrs.io.req[0].bits.uop.fp_ctrl.swap12', 'mshrs.io.req[0].bits.uop.fp_ctrl.swap23', 'mshrs.io.req[0].bits.uop.fp_ctrl.toint', 'mshrs.io.req[0].bits.uop.fp_ctrl.typeTagIn', 'mshrs.io.req[0].bits.uop.fp_ctrl.typeTagOut', 'mshrs.io.req[0].bits.uop.fp_ctrl.vec', 'mshrs.io.req[0].bits.uop.fp_ctrl.wen', 'mshrs.io.req[0].bits.uop.fp_ctrl.wflags', 'mshrs.io.req[0].bits.uop.fp_rm', 'mshrs.io.req[0].bits.uop.fp_typ', 'mshrs.io.req[0].bits.uop.fp_val', 'mshrs.io.req[0].bits.uop.frs3_en', 'mshrs.io.req[0].bits.uop.ftq_idx', 'mshrs.io.req[0].bits.uop.fu_code[0]', 'mshrs.io.req[0].bits.uop.fu_code[1]', 'mshrs.io.req[0].bits.uop.fu_code[2]', 'mshrs.io.req[0].bits.uop.fu_code[3]', 'mshrs.io.req[0].bits.uop.fu_code[4]', 'mshrs.io.req[0].bits.uop.fu_code[5]', 'mshrs.io.req[0].bits.uop.fu_code[6]', 'mshrs.io.req[0].bits.uop.fu_code[7]', 'mshrs.io.req[0].bits.uop.fu_code[8]', 'mshrs.io.req[0].bits.uop.fu_code[9]', 'mshrs.io.req[0].bits.uop.imm_packed', 'mshrs.io.req[0].bits.uop.imm_rename', 'mshrs.io.req[0].bits.uop.imm_sel', 'mshrs.io.req[0].bits.uop.inst', 'mshrs.io.req[0].bits.uop.iq_type[0]', 'mshrs.io.req[0].bits.uop.iq_type[1]', 'mshrs.io.req[0].bits.uop.iq_type[2]', 'mshrs.io.req[0].bits.uop.iq_type[3]', 'mshrs.io.req[0].bits.uop.is_amo', 'mshrs.io.req[0].bits.uop.is_eret', 'mshrs.io.req[0].bits.uop.is_fence', 'mshrs.io.req[0].bits.uop.is_fencei', 'mshrs.io.req[0].bits.uop.is_mov', 'mshrs.io.req[0].bits.uop.is_rocc', 'mshrs.io.req[0].bits.uop.is_rvc', 'mshrs.io.req[0].bits.uop.is_sfb', 'mshrs.io.req[0].bits.uop.is_sfence', 'mshrs.io.req[0].bits.uop.is_sys_pc2epc', 'mshrs.io.req[0].bits.uop.is_unique', 'mshrs.io.req[0].bits.uop.iw_issued', 'mshrs.io.req[0].bits.uop.iw_issued_partial_agen', 'mshrs.io.req[0].bits.uop.iw_issued_partial_dgen', 'mshrs.io.req[0].bits.uop.iw_p1_bypass_hint', 'mshrs.io.req[0].bits.uop.iw_p1_speculative_child', 'mshrs.io.req[0].bits.uop.iw_p2_bypass_hint', 'mshrs.io.req[0].bits.uop.iw_p2_speculative_child', 'mshrs.io.req[0].bits.uop.iw_p3_bypass_hint', 'mshrs.io.req[0].bits.uop.ldq_idx', 'mshrs.io.req[0].bits.uop.ldst', 'mshrs.io.req[0].bits.uop.ldst_is_rs1', 'mshrs.io.req[0].bits.uop.lrs1', 'mshrs.io.req[0].bits.uop.lrs1_rtype', 'mshrs.io.req[0].bits.uop.lrs2', 'mshrs.io.req[0].bits.uop.lrs2_rtype', 'mshrs.io.req[0].bits.uop.lrs3', 'mshrs.io.req[0].bits.uop.mem_cmd', 'mshrs.io.req[0].bits.uop.mem_signed', 'mshrs.io.req[0].bits.uop.mem_size', 'mshrs.io.req[0].bits.uop.op1_sel', 'mshrs.io.req[0].bits.uop.op2_sel', 'mshrs.io.req[0].bits.uop.pc_lob', 'mshrs.io.req[0].bits.uop.pdst', 'mshrs.io.req[0].bits.uop.pimm', 'mshrs.io.req[0].bits.uop.ppred', 'mshrs.io.req[0].bits.uop.ppred_busy', 'mshrs.io.req[0].bits.uop.prs1', 'mshrs.io.req[0].bits.uop.prs1_busy', 'mshrs.io.req[0].bits.uop.prs2', 'mshrs.io.req[0].bits.uop.prs2_busy', 'mshrs.io.req[0].bits.uop.prs3', 'mshrs.io.req[0].bits.uop.prs3_busy', 'mshrs.io.req[0].bits.uop.rob_idx', 'mshrs.io.req[0].bits.uop.rxq_idx', 'mshrs.io.req[0].bits.uop.stale_pdst', 'mshrs.io.req[0].bits.uop.stq_idx', 'mshrs.io.req[0].bits.uop.taken', 'mshrs.io.req[0].bits.uop.uses_ldq', 'mshrs.io.req[0].bits.uop.uses_stq', 'mshrs.io.req[0].bits.uop.xcpt_ae_if', 'mshrs.io.req[0].bits.uop.xcpt_ma_if', 'mshrs.io.req[0].bits.uop.xcpt_pf_if', 'mshrs.io.req[0].bits.way_en', 'mshrs.io.req[0].ready', 'mshrs.io.req[0].valid', 'mshrs.io.req_is_probe[0]', 'mshrs.io.resp.ready', 'mshrs.io.resp.valid', 'mshrs.io.rob_head_idx', 'mshrs.io.rob_pnr_idx', 'mshrs.io.secondary_miss[0]', 'mshrs.io.wb_resp', 'mshrs.reset', 'prober.clock', 'prober.io.block_state.state', 'prober.io.meta_read.bits.idx', 'prober.io.meta_read.bits.tag', 'prober.io.meta_read.bits.way_en', 'prober.io.meta_read.ready', 'prober.io.meta_read.valid', 'prober.io.meta_write.bits.idx', 'prober.io.mshr_rdy', 'prober.io.mshr_wb_rdy', 'prober.io.rep.bits.address', 'prober.io.rep.bits.corrupt', 'prober.io.rep.bits.data', 'prober.io.rep.bits.opcode', 'prober.io.rep.bits.param', 'prober.io.rep.bits.size', 'prober.io.rep.bits.source', 'prober.io.rep.ready', 'prober.io.rep.valid', 'prober.io.req.bits.address', 'prober.io.req.bits.corrupt', 'prober.io.req.bits.data', 'prober.io.req.bits.mask', 'prober.io.req.bits.opcode', 'prober.io.req.bits.param', 'prober.io.req.bits.size', 'prober.io.req.bits.source', 'prober.io.req.ready', 'prober.io.req.valid', 'prober.io.state.bits', 'prober.io.state.valid', 'prober.io.way_en', 'prober.io.wb_rdy', 'prober.reset', 'wb.clock', 'wb.io.data_req.bits.addr', 'wb.io.data_req.bits.way_en', 'wb.io.data_req.ready', 'wb.io.data_req.valid', 'wb.io.data_resp', 'wb.io.idx.bits', 'wb.io.idx.valid', 'wb.io.mem_grant', 'wb.io.meta_read.bits.idx', 'wb.io.meta_read.bits.tag', 'wb.io.meta_read.bits.way_en', 'wb.io.meta_read.ready', 'wb.io.meta_read.valid', 'wb.io.release.bits.address', 'wb.io.release.bits.corrupt', 'wb.io.release.bits.data', 'wb.io.release.bits.opcode', 'wb.io.release.bits.param', 'wb.io.release.bits.size', 'wb.io.release.bits.source', 'wb.io.release.ready', 'wb.io.release.valid', 'wb.io.req.bits.idx', 'wb.io.req.bits.param', 'wb.io.req.bits.source', 'wb.io.req.bits.tag', 'wb.io.req.bits.voluntary', 'wb.io.req.bits.way_en', 'wb.io.req.ready', 'wb.io.req.valid', 'wb.io.resp', 'wb.reset', 'wbArb.clock', 'wbArb.io.in[0].bits.idx', 'wbArb.io.in[0].bits.param', 'wbArb.io.in[0].bits.source', 'wbArb.io.in[0].bits.tag', 'wbArb.io.in[0].bits.voluntary', 'wbArb.io.in[0].bits.way_en', 'wbArb.io.in[0].ready', 'wbArb.io.in[0].valid', 'wbArb.io.in[1].bits.idx', 'wbArb.io.in[1].bits.param', 'wbArb.io.in[1].bits.source', 'wbArb.io.in[1].bits.tag', 'wbArb.io.in[1].bits.voluntary', 'wbArb.io.in[1].bits.way_en', 'wbArb.io.in[1].ready', 'wbArb.io.in[1].valid', 'wbArb.reset']

## Frozen child summaries

### Child `BoomNonBlockingDCache.amoalu`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":[],"child_id":"BoomNonBlockingDCache.amoalu","exported_ids":{"axioms":[],"identity_keys":[],"occurrences":[],"predicates":[]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":[],"semantic_objects":{"identity_keys":[],"occurrences":[],"predicates":[]},"semantic_signals":[],"summary_ref":"umcm://BoomNonBlockingDCache.amoalu","task_id":"leaf_abstraction-BoomNonBlockingDCache.amoalu-9d11028de14b5b4d","trust":{"frozen_sha256":"f233dd25434ab79bc466aec6c62cbef8305eaad5f5cd513fad32a74e2ec35522","instance_reuse":{"implementation_sha256":"f78688aa27970fbcb70462f4a7480f2164e18f852907627da0a6673943637468","kind":"exact-work-unit","module":"AMOALU","source_module":"AMOALU","source_work_unit_id":"BoomNonBlockingDCache.amoalu","structural_implementation_sha256":"85ba636b6a7008706c2ec4ca32599ca4deb2b94d643fbd2cf4830277bfe74b10","target_work_unit_id":"BoomNonBlockingDCache.amoalu","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":0},"trusted_axioms":[]}
```

### Child `BoomNonBlockingDCache.data`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.data::io.read[0].valid","BoomNonBlockingDCache.data::io.write.valid"],"child_id":"BoomNonBlockingDCache.data","exported_ids":{"axioms":["BoomNonBlockingDCache.data::A1","BoomNonBlockingDCache.data::A2","BoomNonBlockingDCache.data::A3","BoomNonBlockingDCache.data::A4","BoomNonBlockingDCache.data::A5"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.data::ReadRequest","BoomNonBlockingDCache.data::Way0Write","BoomNonBlockingDCache.data::Way1Write","BoomNonBlockingDCache.data::Way2Write","BoomNonBlockingDCache.data::Way3Write"],"predicates":[]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["data.io.read[0].bits.addr","data.io.resp[0][0]","data.io.resp[0][1]","data.io.resp[0][2]","data.io.resp[0][3]","data.io.s1_nacks[0]","data.io.write.bits.addr","data.io.write.bits.data"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.read[0].valid","id":"ReadRequest","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.data::io.read[0].valid"],"qualified_id":"BoomNonBlockingDCache.data::ReadRequest"},{"definition":"io.write.valid && io.write.bits.way_en[0] && io.write.bits.wmask[0]","id":"Way0Write","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.data::Way0Write"},{"definition":"io.write.valid && io.write.bits.way_en[1] && io.write.bits.wmask[0]","id":"Way1Write","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.data::Way1Write"},{"definition":"io.write.valid && io.write.bits.way_en[2] && io.write.bits.wmask[0]","id":"Way2Write","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.data::Way2Write"},{"definition":"io.write.valid && io.write.bits.way_en[3] && io.write.bits.wmask[0]","id":"Way3Write","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.data::Way3Write"}],"predicates":[]},"semantic_signals":[{"id":"io.read[0].bits.addr","parent_frontier_signal":"data.io.read[0].bits.addr","visibility":"direct_frontier"},{"id":"io.resp[0][0]","parent_frontier_signal":"data.io.resp[0][0]","visibility":"direct_frontier"},{"id":"io.resp[0][1]","parent_frontier_signal":"data.io.resp[0][1]","visibility":"direct_frontier"},{"id":"io.resp[0][2]","parent_frontier_signal":"data.io.resp[0][2]","visibility":"direct_frontier"},{"id":"io.resp[0][3]","parent_frontier_signal":"data.io.resp[0][3]","visibility":"direct_frontier"},{"id":"io.s1_nacks[0]","parent_frontier_signal":"data.io.s1_nacks[0]","visibility":"direct_frontier"},{"id":"io.write.bits.addr","parent_frontier_signal":"data.io.write.bits.addr","visibility":"direct_frontier"},{"id":"io.write.bits.data","parent_frontier_signal":"data.io.write.bits.data","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.data","task_id":"leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29","trust":{"frozen_sha256":"fc97cfb35907c609be09edb13f062b529bd975e0906ecddf6e5c68c0f0d257ea","instance_reuse":{"implementation_sha256":"600e39cf8d7d8f6e68f344fd6996fe6fc6ea1219e11361dbdb2878cf1d6892b4","kind":"exact-work-unit","module":"BoomDuplicatedDataArray","source_module":"BoomDuplicatedDataArray","source_work_unit_id":"BoomNonBlockingDCache.data","structural_implementation_sha256":"f860a8e39180e24638c8367aa8563a15654c2fc2b75c61b8ea9d0a6d42209151","target_work_unit_id":"BoomNonBlockingDCache.data","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":5},"trusted_axioms":[{"formal":{"initialization":{"kind":"implicit_unconstrained"},"key":{"address_domain":{"end_exclusive":512,"start":0},"lane":{"count":1,"name":"word"}},"read":{"address":{"amount":3,"op":"shr","value":{"name":"io.read[0].bits.addr","op":"signal"}},"latency_cycles":2,"request":"ReadRequest"},"read_write_collision":"implicit_unconstrained","relations":{"co":"DataWay0CO","fr":"DataWay0FR","rf":"DataWay0RF"},"resolution":"latest_prior_write_same_key","scope_identity":null,"storage":"array_0_0","type":"indexed_storage_flow","value_fields":[{"name":"data","read_targets":[{"name":"io.resp[0][0]","op":"signal"}],"storage_bits":{"hi":63,"lo":0},"write_value":{"name":"io.write.bits.data","op":"signal"}}],"write":{"address":{"amount":3,"op":"shr","value":{"name":"io.write.bits.addr","op":"signal"}},"lane_mask":{"op":"const","value":1},"on":"Way0Write"}},"id":"A1","qualified_id":"BoomNonBlockingDCache.data::A1","rendered_formula":"array_0_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay0RF=rf, DataWay0CO=co, DataWay0FR=rf^-1;co"},{"formal":{"initialization":{"kind":"implicit_unconstrained"},"key":{"address_domain":{"end_exclusive":512,"start":0},"lane":{"count":1,"name":"word"}},"read":{"address":{"amount":3,"op":"shr","value":{"name":"io.read[0].bits.addr","op":"signal"}},"latency_cycles":2,"request":"ReadRequest"},"read_write_collision":"implicit_unconstrained","relations":{"co":"DataWay1CO","fr":"DataWay1FR","rf":"DataWay1RF"},"resolution":"latest_prior_write_same_key","scope_identity":null,"storage":"array_1_0","type":"indexed_storage_flow","value_fields":[{"name":"data","read_targets":[{"name":"io.resp[0][1]","op":"signal"}],"storage_bits":{"hi":63,"lo":0},"write_value":{"name":"io.write.bits.data","op":"signal"}}],"write":{"address":{"amount":3,"op":"shr","value":{"name":"io.write.bits.addr","op":"signal"}},"lane_mask":{"op":"const","value":1},"on":"Way1Write"}},"id":"A2","qualified_id":"BoomNonBlockingDCache.data::A2","rendered_formula":"array_1_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay1RF=rf, DataWay1CO=co, DataWay1FR=rf^-1;co"},{"formal":{"initialization":{"kind":"implicit_unconstrained"},"key":{"address_domain":{"end_exclusive":512,"start":0},"lane":{"count":1,"name":"word"}},"read":{"address":{"amount":3,"op":"shr","value":{"name":"io.read[0].bits.addr","op":"signal"}},"latency_cycles":2,"request":"ReadRequest"},"read_write_collision":"implicit_unconstrained","relations":{"co":"DataWay2CO","fr":"DataWay2FR","rf":"DataWay2RF"},"resolution":"latest_prior_write_same_key","scope_identity":null,"storage":"array_2_0","type":"indexed_storage_flow","value_fields":[{"name":"data","read_targets":[{"name":"io.resp[0][2]","op":"signal"}],"storage_bits":{"hi":63,"lo":0},"write_value":{"name":"io.write.bits.data","op":"signal"}}],"write":{"address":{"amount":3,"op":"shr","value":{"name":"io.write.bits.addr","op":"signal"}},"lane_mask":{"op":"const","value":1},"on":"Way2Write"}},"id":"A3","qualified_id":"BoomNonBlockingDCache.data::A3","rendered_formula":"array_2_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay2RF=rf, DataWay2CO=co, DataWay2FR=rf^-1;co"},{"formal":{"initialization":{"kind":"implicit_unconstrained"},"key":{"address_domain":{"end_exclusive":512,"start":0},"lane":{"count":1,"name":"word"}},"read":{"address":{"amount":3,"op":"shr","value":{"name":"io.read[0].bits.addr","op":"signal"}},"latency_cycles":2,"request":"ReadRequest"},"read_write_collision":"implicit_unconstrained","relations":{"co":"DataWay3CO","fr":"DataWay3FR","rf":"DataWay3RF"},"resolution":"latest_prior_write_same_key","scope_identity":null,"storage":"array_3_0","type":"indexed_storage_flow","value_fields":[{"name":"data","read_targets":[{"name":"io.resp[0][3]","op":"signal"}],"storage_bits":{"hi":63,"lo":0},"write_value":{"name":"io.write.bits.data","op":"signal"}}],"write":{"address":{"amount":3,"op":"shr","value":{"name":"io.write.bits.addr","op":"signal"}},"lane_mask":{"op":"const","value":1},"on":"Way3Write"}},"id":"A4","qualified_id":"BoomNonBlockingDCache.data::A4","rendered_formula":"array_3_0[word] latest-write storage flow with implicit_unconstrained initialization; DataWay3RF=rf, DataWay3CO=co, DataWay3FR=rf^-1;co"},{"formal":{"expr":{"index":0,"op":"bit","value":{"name":"io.s1_nacks[0]","op":"signal"}},"on":null,"relation":"eq","scope_identity":null,"type":"value_constraint","value":0},"id":"A5","qualified_id":"BoomNonBlockingDCache.data::A5","rendered_formula":"bits(io.s1_nacks[0], 0, 0) == 0"}]}
```

### Child `BoomNonBlockingDCache.dataReadArb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.dataReadArb::io.in[0].fire","BoomNonBlockingDCache.dataReadArb::io.in[1].fire","BoomNonBlockingDCache.dataReadArb::io.in[2].fire","BoomNonBlockingDCache.dataReadArb::io.out.fire"],"child_id":"BoomNonBlockingDCache.dataReadArb","exported_ids":{"axioms":["BoomNonBlockingDCache.dataReadArb::A1","BoomNonBlockingDCache.dataReadArb::A10","BoomNonBlockingDCache.dataReadArb::A11","BoomNonBlockingDCache.dataReadArb::A12","BoomNonBlockingDCache.dataReadArb::A13","BoomNonBlockingDCache.dataReadArb::A14","BoomNonBlockingDCache.dataReadArb::A15","BoomNonBlockingDCache.dataReadArb::A2","BoomNonBlockingDCache.dataReadArb::A3","BoomNonBlockingDCache.dataReadArb::A4","BoomNonBlockingDCache.dataReadArb::A5","BoomNonBlockingDCache.dataReadArb::A6","BoomNonBlockingDCache.dataReadArb::A7","BoomNonBlockingDCache.dataReadArb::A8","BoomNonBlockingDCache.dataReadArb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.dataReadArb::Input0Fire","BoomNonBlockingDCache.dataReadArb::Input1Fire","BoomNonBlockingDCache.dataReadArb::Input2Fire","BoomNonBlockingDCache.dataReadArb::OutputFire"],"predicates":["BoomNonBlockingDCache.dataReadArb::Higher01Valid","BoomNonBlockingDCache.dataReadArb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["dataReadArb.io.chosen","dataReadArb.io.in[0].bits.req[0].addr","dataReadArb.io.in[0].bits.req[0].way_en","dataReadArb.io.in[0].bits.valid[0]","dataReadArb.io.in[1].bits.req[0].addr","dataReadArb.io.in[1].bits.req[0].way_en","dataReadArb.io.in[1].bits.valid[0]","dataReadArb.io.in[2].bits.req[0].addr","dataReadArb.io.in[2].bits.req[0].way_en","dataReadArb.io.in[2].bits.valid[0]","dataReadArb.io.out.bits.req[0].addr","dataReadArb.io.out.bits.req[0].way_en","dataReadArb.io.out.bits.valid[0]"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataReadArb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.dataReadArb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataReadArb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.dataReadArb::Input1Fire"},{"definition":"io.in[2].valid && io.in[2].ready","id":"Input2Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataReadArb::io.in[2].fire"],"qualified_id":"BoomNonBlockingDCache.dataReadArb::Input2Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataReadArb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.dataReadArb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid || io.in[1].valid","id":"Higher01Valid","qualified_id":"BoomNonBlockingDCache.dataReadArb::Higher01Valid"},{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.dataReadArb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"dataReadArb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.req[0].addr","parent_frontier_signal":"dataReadArb.io.in[0].bits.req[0].addr","visibility":"direct_frontier"},{"id":"io.in[0].bits.req[0].way_en","parent_frontier_signal":"dataReadArb.io.in[0].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[0].bits.valid[0]","parent_frontier_signal":"dataReadArb.io.in[0].bits.valid[0]","visibility":"direct_frontier"},{"id":"io.in[1].bits.req[0].addr","parent_frontier_signal":"dataReadArb.io.in[1].bits.req[0].addr","visibility":"direct_frontier"},{"id":"io.in[1].bits.req[0].way_en","parent_frontier_signal":"dataReadArb.io.in[1].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[1].bits.valid[0]","parent_frontier_signal":"dataReadArb.io.in[1].bits.valid[0]","visibility":"direct_frontier"},{"id":"io.in[2].bits.req[0].addr","parent_frontier_signal":"dataReadArb.io.in[2].bits.req[0].addr","visibility":"direct_frontier"},{"id":"io.in[2].bits.req[0].way_en","parent_frontier_signal":"dataReadArb.io.in[2].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[2].bits.valid[0]","parent_frontier_signal":"dataReadArb.io.in[2].bits.valid[0]","visibility":"direct_frontier"},{"id":"io.out.bits.req[0].addr","parent_frontier_signal":"dataReadArb.io.out.bits.req[0].addr","visibility":"direct_frontier"},{"id":"io.out.bits.req[0].way_en","parent_frontier_signal":"dataReadArb.io.out.bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.out.bits.valid[0]","parent_frontier_signal":"dataReadArb.io.out.bits.valid[0]","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.dataReadArb","task_id":"leaf_abstraction-BoomNonBlockingDCache.dataReadArb-8173fddc63391303","trust":{"frozen_sha256":"fd6c4daee91d6c487bf109c441c7f3fe5106d527e4e058fb53582183d87b094d","instance_reuse":{"implementation_sha256":"ad8407b22997a085e1e48da12c305a0bca11432a830a34420c6a82cb16a244cd","kind":"exact-work-unit","module":"Arbiter3_BoomL1DataReadReq","source_module":"Arbiter3_BoomL1DataReadReq","source_work_unit_id":"BoomNonBlockingDCache.dataReadArb","structural_implementation_sha256":"982e94f1bd1f9582ebe7206bc491560dba32233ee0201b08346343018ae494f7","target_work_unit_id":"BoomNonBlockingDCache.dataReadArb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":15},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire","Input2Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.dataReadArb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.dataReadArb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"occurrence":"Input2Fire","predicate":"Higher01Valid","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache.dataReadArb::A3","rendered_formula":"Higher01Valid => !Input2Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache.dataReadArb::A4","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache.dataReadArb::A5","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"op":"const","value":2},"target":"io.chosen","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache.dataReadArb::A6","rendered_formula":"io.chosen = 2 on Input2Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.req[0].addr","op":"signal"},"target":"io.out.bits.req[0].addr","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.dataReadArb::A7","rendered_formula":"io.out.bits.req[0].addr = io.in[0].bits.req[0].addr on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.dataReadArb::A8","rendered_formula":"io.out.bits.req[0].way_en = io.in[0].bits.req[0].way_en on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.valid[0]","op":"signal"},"target":"io.out.bits.valid[0]","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.dataReadArb::A9","rendered_formula":"io.out.bits.valid[0] = io.in[0].bits.valid[0] on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.req[0].addr","op":"signal"},"target":"io.out.bits.req[0].addr","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.dataReadArb::A10","rendered_formula":"io.out.bits.req[0].addr = io.in[1].bits.req[0].addr on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.dataReadArb::A11","rendered_formula":"io.out.bits.req[0].way_en = io.in[1].bits.req[0].way_en on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.valid[0]","op":"signal"},"target":"io.out.bits.valid[0]","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.dataReadArb::A12","rendered_formula":"io.out.bits.valid[0] = io.in[1].bits.valid[0] on Input1Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.req[0].addr","op":"signal"},"target":"io.out.bits.req[0].addr","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache.dataReadArb::A13","rendered_formula":"io.out.bits.req[0].addr = io.in[2].bits.req[0].addr on Input2Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache.dataReadArb::A14","rendered_formula":"io.out.bits.req[0].way_en = io.in[2].bits.req[0].way_en on Input2Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.valid[0]","op":"signal"},"target":"io.out.bits.valid[0]","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache.dataReadArb::A15","rendered_formula":"io.out.bits.valid[0] = io.in[2].bits.valid[0] on Input2Fire"}]}
```

### Child `BoomNonBlockingDCache.dataWriteArb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.dataWriteArb::io.in[0].fire","BoomNonBlockingDCache.dataWriteArb::io.in[1].fire","BoomNonBlockingDCache.dataWriteArb::io.out.fire"],"child_id":"BoomNonBlockingDCache.dataWriteArb","exported_ids":{"axioms":["BoomNonBlockingDCache.dataWriteArb::A1","BoomNonBlockingDCache.dataWriteArb::A10","BoomNonBlockingDCache.dataWriteArb::A11","BoomNonBlockingDCache.dataWriteArb::A12","BoomNonBlockingDCache.dataWriteArb::A2","BoomNonBlockingDCache.dataWriteArb::A3","BoomNonBlockingDCache.dataWriteArb::A4","BoomNonBlockingDCache.dataWriteArb::A5","BoomNonBlockingDCache.dataWriteArb::A6","BoomNonBlockingDCache.dataWriteArb::A7","BoomNonBlockingDCache.dataWriteArb::A8","BoomNonBlockingDCache.dataWriteArb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.dataWriteArb::Input0Fire","BoomNonBlockingDCache.dataWriteArb::Input1Fire","BoomNonBlockingDCache.dataWriteArb::OutputFire"],"predicates":["BoomNonBlockingDCache.dataWriteArb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["dataWriteArb.io.chosen","dataWriteArb.io.in[0].bits.addr","dataWriteArb.io.in[0].bits.data","dataWriteArb.io.in[0].bits.way_en","dataWriteArb.io.in[0].bits.wmask","dataWriteArb.io.in[1].bits.addr","dataWriteArb.io.in[1].bits.data","dataWriteArb.io.in[1].bits.way_en","dataWriteArb.io.in[1].bits.wmask","dataWriteArb.io.out.bits.addr","dataWriteArb.io.out.bits.data","dataWriteArb.io.out.bits.way_en","dataWriteArb.io.out.bits.wmask"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataWriteArb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.dataWriteArb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataWriteArb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.dataWriteArb::Input1Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.dataWriteArb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.dataWriteArb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.dataWriteArb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"dataWriteArb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.addr","parent_frontier_signal":"dataWriteArb.io.in[0].bits.addr","visibility":"direct_frontier"},{"id":"io.in[0].bits.data","parent_frontier_signal":"dataWriteArb.io.in[0].bits.data","visibility":"direct_frontier"},{"id":"io.in[0].bits.way_en","parent_frontier_signal":"dataWriteArb.io.in[0].bits.way_en","visibility":"direct_frontier"},{"id":"io.in[0].bits.wmask","parent_frontier_signal":"dataWriteArb.io.in[0].bits.wmask","visibility":"direct_frontier"},{"id":"io.in[1].bits.addr","parent_frontier_signal":"dataWriteArb.io.in[1].bits.addr","visibility":"direct_frontier"},{"id":"io.in[1].bits.data","parent_frontier_signal":"dataWriteArb.io.in[1].bits.data","visibility":"direct_frontier"},{"id":"io.in[1].bits.way_en","parent_frontier_signal":"dataWriteArb.io.in[1].bits.way_en","visibility":"direct_frontier"},{"id":"io.in[1].bits.wmask","parent_frontier_signal":"dataWriteArb.io.in[1].bits.wmask","visibility":"direct_frontier"},{"id":"io.out.bits.addr","parent_frontier_signal":"dataWriteArb.io.out.bits.addr","visibility":"direct_frontier"},{"id":"io.out.bits.data","parent_frontier_signal":"dataWriteArb.io.out.bits.data","visibility":"direct_frontier"},{"id":"io.out.bits.way_en","parent_frontier_signal":"dataWriteArb.io.out.bits.way_en","visibility":"direct_frontier"},{"id":"io.out.bits.wmask","parent_frontier_signal":"dataWriteArb.io.out.bits.wmask","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.dataWriteArb","task_id":"leaf_abstraction-BoomNonBlockingDCache.dataWriteArb-0f7f2a170c31ec11","trust":{"frozen_sha256":"9354c8a1a4404f632dbe3527ba5a55bb0e324cd335b36d49ebe1965de9c83019","instance_reuse":{"implementation_sha256":"fde62692c84449405f67ac6f121b87f783978735d0b07b1fad9e2951a6e21007","kind":"exact-work-unit","module":"Arbiter2_L1DataWriteReq_1","source_module":"Arbiter2_L1DataWriteReq_1","source_work_unit_id":"BoomNonBlockingDCache.dataWriteArb","structural_implementation_sha256":"0ee0ce62e7c42e5388c1cc87b47807d546882acccc1be9c75866c45f4636f74c","target_work_unit_id":"BoomNonBlockingDCache.dataWriteArb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":12},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A3","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A3","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.addr","op":"signal"},"target":"io.out.bits.addr","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A4","rendered_formula":"io.out.bits.addr = io.in[0].bits.addr on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.data","op":"signal"},"target":"io.out.bits.data","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A5","rendered_formula":"io.out.bits.data = io.in[0].bits.data on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A6","rendered_formula":"io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.wmask","op":"signal"},"target":"io.out.bits.wmask","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A7","rendered_formula":"io.out.bits.wmask = io.in[0].bits.wmask on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A8","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.addr","op":"signal"},"target":"io.out.bits.addr","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A9","rendered_formula":"io.out.bits.addr = io.in[1].bits.addr on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.data","op":"signal"},"target":"io.out.bits.data","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A10","rendered_formula":"io.out.bits.data = io.in[1].bits.data on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A11","rendered_formula":"io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.wmask","op":"signal"},"target":"io.out.bits.wmask","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.dataWriteArb::A12","rendered_formula":"io.out.bits.wmask = io.in[1].bits.wmask on Input1Fire"}]}
```

### Child `BoomNonBlockingDCache.lfsr_prng`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.lfsr_prng::io.seed.valid"],"child_id":"BoomNonBlockingDCache.lfsr_prng","exported_ids":{"axioms":[],"identity_keys":[],"occurrences":[],"predicates":[]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":[],"semantic_objects":{"identity_keys":[],"occurrences":[],"predicates":[]},"semantic_signals":[],"summary_ref":"umcm://BoomNonBlockingDCache.lfsr_prng","task_id":"leaf_abstraction-BoomNonBlockingDCache.lfsr_prng-80cbcb83351fc3e0","trust":{"frozen_sha256":"4c7707ead1361151e7467eea37032e427d4a8026822bb10dfd1fdf00f234ebd7","instance_reuse":{"implementation_sha256":"cf6c24c567979770b28441c4551b360e2e9665da150978199f87183fed63f1ad","kind":"exact-work-unit","module":"MaxPeriodFibonacciLFSR_1","source_module":"MaxPeriodFibonacciLFSR_1","source_work_unit_id":"BoomNonBlockingDCache.lfsr_prng","structural_implementation_sha256":"631c7039b9de0b20b2bc40ba84adb1f3fc71943baab7cf37c77f804218ac9423","target_work_unit_id":"BoomNonBlockingDCache.lfsr_prng","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":0},"trusted_axioms":[]}
```

### Child `BoomNonBlockingDCache.lsu_release_arb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.lsu_release_arb::io.in[0].fire","BoomNonBlockingDCache.lsu_release_arb::io.in[1].fire","BoomNonBlockingDCache.lsu_release_arb::io.out.fire"],"child_id":"BoomNonBlockingDCache.lsu_release_arb","exported_ids":{"axioms":["BoomNonBlockingDCache.lsu_release_arb::A1","BoomNonBlockingDCache.lsu_release_arb::A10","BoomNonBlockingDCache.lsu_release_arb::A11","BoomNonBlockingDCache.lsu_release_arb::A12","BoomNonBlockingDCache.lsu_release_arb::A13","BoomNonBlockingDCache.lsu_release_arb::A14","BoomNonBlockingDCache.lsu_release_arb::A15","BoomNonBlockingDCache.lsu_release_arb::A16","BoomNonBlockingDCache.lsu_release_arb::A17","BoomNonBlockingDCache.lsu_release_arb::A18","BoomNonBlockingDCache.lsu_release_arb::A2","BoomNonBlockingDCache.lsu_release_arb::A3","BoomNonBlockingDCache.lsu_release_arb::A4","BoomNonBlockingDCache.lsu_release_arb::A5","BoomNonBlockingDCache.lsu_release_arb::A6","BoomNonBlockingDCache.lsu_release_arb::A7","BoomNonBlockingDCache.lsu_release_arb::A8","BoomNonBlockingDCache.lsu_release_arb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.lsu_release_arb::Input0Fire","BoomNonBlockingDCache.lsu_release_arb::Input1Fire","BoomNonBlockingDCache.lsu_release_arb::OutputFire"],"predicates":["BoomNonBlockingDCache.lsu_release_arb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["lsu_release_arb.io.chosen","lsu_release_arb.io.in[0].bits.address","lsu_release_arb.io.in[0].bits.corrupt","lsu_release_arb.io.in[0].bits.data","lsu_release_arb.io.in[0].bits.opcode","lsu_release_arb.io.in[0].bits.param","lsu_release_arb.io.in[0].bits.size","lsu_release_arb.io.in[0].bits.source","lsu_release_arb.io.in[1].bits.address","lsu_release_arb.io.in[1].bits.corrupt","lsu_release_arb.io.in[1].bits.data","lsu_release_arb.io.in[1].bits.opcode","lsu_release_arb.io.in[1].bits.param","lsu_release_arb.io.in[1].bits.size","lsu_release_arb.io.in[1].bits.source","lsu_release_arb.io.out.bits.address","lsu_release_arb.io.out.bits.corrupt","lsu_release_arb.io.out.bits.data","lsu_release_arb.io.out.bits.opcode","lsu_release_arb.io.out.bits.param","lsu_release_arb.io.out.bits.size","lsu_release_arb.io.out.bits.source"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.lsu_release_arb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.lsu_release_arb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.lsu_release_arb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.lsu_release_arb::Input1Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.lsu_release_arb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.lsu_release_arb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"lsu_release_arb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.address","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.address","visibility":"direct_frontier"},{"id":"io.in[0].bits.corrupt","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.corrupt","visibility":"direct_frontier"},{"id":"io.in[0].bits.data","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.data","visibility":"direct_frontier"},{"id":"io.in[0].bits.opcode","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.opcode","visibility":"direct_frontier"},{"id":"io.in[0].bits.param","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.param","visibility":"direct_frontier"},{"id":"io.in[0].bits.size","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.size","visibility":"direct_frontier"},{"id":"io.in[0].bits.source","parent_frontier_signal":"lsu_release_arb.io.in[0].bits.source","visibility":"direct_frontier"},{"id":"io.in[1].bits.address","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.address","visibility":"direct_frontier"},{"id":"io.in[1].bits.corrupt","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.corrupt","visibility":"direct_frontier"},{"id":"io.in[1].bits.data","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.data","visibility":"direct_frontier"},{"id":"io.in[1].bits.opcode","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.opcode","visibility":"direct_frontier"},{"id":"io.in[1].bits.param","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.param","visibility":"direct_frontier"},{"id":"io.in[1].bits.size","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.size","visibility":"direct_frontier"},{"id":"io.in[1].bits.source","parent_frontier_signal":"lsu_release_arb.io.in[1].bits.source","visibility":"direct_frontier"},{"id":"io.out.bits.address","parent_frontier_signal":"lsu_release_arb.io.out.bits.address","visibility":"direct_frontier"},{"id":"io.out.bits.corrupt","parent_frontier_signal":"lsu_release_arb.io.out.bits.corrupt","visibility":"direct_frontier"},{"id":"io.out.bits.data","parent_frontier_signal":"lsu_release_arb.io.out.bits.data","visibility":"direct_frontier"},{"id":"io.out.bits.opcode","parent_frontier_signal":"lsu_release_arb.io.out.bits.opcode","visibility":"direct_frontier"},{"id":"io.out.bits.param","parent_frontier_signal":"lsu_release_arb.io.out.bits.param","visibility":"direct_frontier"},{"id":"io.out.bits.size","parent_frontier_signal":"lsu_release_arb.io.out.bits.size","visibility":"direct_frontier"},{"id":"io.out.bits.source","parent_frontier_signal":"lsu_release_arb.io.out.bits.source","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.lsu_release_arb","task_id":"leaf_abstraction-BoomNonBlockingDCache.lsu_release_arb-92d18ec47fe4f8de","trust":{"frozen_sha256":"e5d9d6cbbf34a7cf69a43aaf6058221096ffdd6de0048a395af93ae613985f8e","instance_reuse":{"implementation_sha256":"46c665790cb6cad7a6fc74931f5019e80ec7b364c037a6a922bbe1c44e6043ec","kind":"exact-work-unit","module":"Arbiter2_TLBundleC_a32d64s2k3z4c","source_module":"Arbiter2_TLBundleC_a32d64s2k3z4c","source_work_unit_id":"BoomNonBlockingDCache.lsu_release_arb","structural_implementation_sha256":"34fff86c911855f52eaa6e57ac3e1553c513e518d684a917922829c51c282f39","target_work_unit_id":"BoomNonBlockingDCache.lsu_release_arb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":18},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A3","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A3","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.opcode","op":"signal"},"target":"io.out.bits.opcode","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A4","rendered_formula":"io.out.bits.opcode = io.in[0].bits.opcode on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.param","op":"signal"},"target":"io.out.bits.param","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A5","rendered_formula":"io.out.bits.param = io.in[0].bits.param on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.size","op":"signal"},"target":"io.out.bits.size","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A6","rendered_formula":"io.out.bits.size = io.in[0].bits.size on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.source","op":"signal"},"target":"io.out.bits.source","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A7","rendered_formula":"io.out.bits.source = io.in[0].bits.source on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.address","op":"signal"},"target":"io.out.bits.address","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A8","rendered_formula":"io.out.bits.address = io.in[0].bits.address on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.data","op":"signal"},"target":"io.out.bits.data","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A9","rendered_formula":"io.out.bits.data = io.in[0].bits.data on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.corrupt","op":"signal"},"target":"io.out.bits.corrupt","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A10","rendered_formula":"io.out.bits.corrupt = io.in[0].bits.corrupt on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A11","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.opcode","op":"signal"},"target":"io.out.bits.opcode","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A12","rendered_formula":"io.out.bits.opcode = io.in[1].bits.opcode on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.param","op":"signal"},"target":"io.out.bits.param","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A13","rendered_formula":"io.out.bits.param = io.in[1].bits.param on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.size","op":"signal"},"target":"io.out.bits.size","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A14","rendered_formula":"io.out.bits.size = io.in[1].bits.size on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.source","op":"signal"},"target":"io.out.bits.source","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A15","rendered_formula":"io.out.bits.source = io.in[1].bits.source on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.address","op":"signal"},"target":"io.out.bits.address","type":"signal_equality"},"id":"A16","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A16","rendered_formula":"io.out.bits.address = io.in[1].bits.address on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.data","op":"signal"},"target":"io.out.bits.data","type":"signal_equality"},"id":"A17","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A17","rendered_formula":"io.out.bits.data = io.in[1].bits.data on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.corrupt","op":"signal"},"target":"io.out.bits.corrupt","type":"signal_equality"},"id":"A18","qualified_id":"BoomNonBlockingDCache.lsu_release_arb::A18","rendered_formula":"io.out.bits.corrupt = io.in[1].bits.corrupt on Input1Fire"}]}
```

### Child `BoomNonBlockingDCache.metaReadArb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.metaReadArb::io.in[0].fire","BoomNonBlockingDCache.metaReadArb::io.in[1].fire","BoomNonBlockingDCache.metaReadArb::io.in[2].fire","BoomNonBlockingDCache.metaReadArb::io.in[3].fire","BoomNonBlockingDCache.metaReadArb::io.in[4].fire","BoomNonBlockingDCache.metaReadArb::io.in[5].fire","BoomNonBlockingDCache.metaReadArb::io.out.fire"],"child_id":"BoomNonBlockingDCache.metaReadArb","exported_ids":{"axioms":["BoomNonBlockingDCache.metaReadArb::A1","BoomNonBlockingDCache.metaReadArb::A10","BoomNonBlockingDCache.metaReadArb::A11","BoomNonBlockingDCache.metaReadArb::A12","BoomNonBlockingDCache.metaReadArb::A13","BoomNonBlockingDCache.metaReadArb::A14","BoomNonBlockingDCache.metaReadArb::A15","BoomNonBlockingDCache.metaReadArb::A16","BoomNonBlockingDCache.metaReadArb::A17","BoomNonBlockingDCache.metaReadArb::A18","BoomNonBlockingDCache.metaReadArb::A19","BoomNonBlockingDCache.metaReadArb::A2","BoomNonBlockingDCache.metaReadArb::A20","BoomNonBlockingDCache.metaReadArb::A21","BoomNonBlockingDCache.metaReadArb::A22","BoomNonBlockingDCache.metaReadArb::A23","BoomNonBlockingDCache.metaReadArb::A24","BoomNonBlockingDCache.metaReadArb::A25","BoomNonBlockingDCache.metaReadArb::A26","BoomNonBlockingDCache.metaReadArb::A27","BoomNonBlockingDCache.metaReadArb::A28","BoomNonBlockingDCache.metaReadArb::A29","BoomNonBlockingDCache.metaReadArb::A3","BoomNonBlockingDCache.metaReadArb::A30","BoomNonBlockingDCache.metaReadArb::A4","BoomNonBlockingDCache.metaReadArb::A5","BoomNonBlockingDCache.metaReadArb::A6","BoomNonBlockingDCache.metaReadArb::A7","BoomNonBlockingDCache.metaReadArb::A8","BoomNonBlockingDCache.metaReadArb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.metaReadArb::Input0Fire","BoomNonBlockingDCache.metaReadArb::Input1Fire","BoomNonBlockingDCache.metaReadArb::Input2Fire","BoomNonBlockingDCache.metaReadArb::Input3Fire","BoomNonBlockingDCache.metaReadArb::Input4Fire","BoomNonBlockingDCache.metaReadArb::Input5Fire","BoomNonBlockingDCache.metaReadArb::OutputFire"],"predicates":["BoomNonBlockingDCache.metaReadArb::Higher01234Valid","BoomNonBlockingDCache.metaReadArb::Higher0123Valid","BoomNonBlockingDCache.metaReadArb::Higher012Valid","BoomNonBlockingDCache.metaReadArb::Higher01Valid","BoomNonBlockingDCache.metaReadArb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["metaReadArb.io.chosen","metaReadArb.io.in[0].bits.req[0].idx","metaReadArb.io.in[0].bits.req[0].tag","metaReadArb.io.in[0].bits.req[0].way_en","metaReadArb.io.in[1].bits.req[0].idx","metaReadArb.io.in[1].bits.req[0].tag","metaReadArb.io.in[1].bits.req[0].way_en","metaReadArb.io.in[2].bits.req[0].idx","metaReadArb.io.in[2].bits.req[0].tag","metaReadArb.io.in[2].bits.req[0].way_en","metaReadArb.io.in[3].bits.req[0].idx","metaReadArb.io.in[3].bits.req[0].tag","metaReadArb.io.in[3].bits.req[0].way_en","metaReadArb.io.in[4].bits.req[0].idx","metaReadArb.io.in[4].bits.req[0].tag","metaReadArb.io.in[4].bits.req[0].way_en","metaReadArb.io.in[5].bits.req[0].idx","metaReadArb.io.in[5].bits.req[0].tag","metaReadArb.io.in[5].bits.req[0].way_en","metaReadArb.io.out.bits.req[0].idx","metaReadArb.io.out.bits.req[0].tag","metaReadArb.io.out.bits.req[0].way_en"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input1Fire"},{"definition":"io.in[2].valid && io.in[2].ready","id":"Input2Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[2].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input2Fire"},{"definition":"io.in[3].valid && io.in[3].ready","id":"Input3Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[3].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input3Fire"},{"definition":"io.in[4].valid && io.in[4].ready","id":"Input4Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[4].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input4Fire"},{"definition":"io.in[5].valid && io.in[5].ready","id":"Input5Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.in[5].fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::Input5Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaReadArb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.metaReadArb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid || io.in[1].valid || io.in[2].valid || io.in[3].valid || io.in[4].valid","id":"Higher01234Valid","qualified_id":"BoomNonBlockingDCache.metaReadArb::Higher01234Valid"},{"definition":"io.in[0].valid || io.in[1].valid || io.in[2].valid || io.in[3].valid","id":"Higher0123Valid","qualified_id":"BoomNonBlockingDCache.metaReadArb::Higher0123Valid"},{"definition":"io.in[0].valid || io.in[1].valid || io.in[2].valid","id":"Higher012Valid","qualified_id":"BoomNonBlockingDCache.metaReadArb::Higher012Valid"},{"definition":"io.in[0].valid || io.in[1].valid","id":"Higher01Valid","qualified_id":"BoomNonBlockingDCache.metaReadArb::Higher01Valid"},{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.metaReadArb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"metaReadArb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[0].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[0].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[0].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[0].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[0].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[1].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[1].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[1].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[1].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[1].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[1].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[2].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[2].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[2].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[2].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[2].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[2].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[3].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[3].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[3].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[3].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[3].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[3].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[4].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[4].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[4].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[4].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[4].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[4].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.in[5].bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.in[5].bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.in[5].bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.in[5].bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.in[5].bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.in[5].bits.req[0].way_en","visibility":"direct_frontier"},{"id":"io.out.bits.req[0].idx","parent_frontier_signal":"metaReadArb.io.out.bits.req[0].idx","visibility":"direct_frontier"},{"id":"io.out.bits.req[0].tag","parent_frontier_signal":"metaReadArb.io.out.bits.req[0].tag","visibility":"direct_frontier"},{"id":"io.out.bits.req[0].way_en","parent_frontier_signal":"metaReadArb.io.out.bits.req[0].way_en","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.metaReadArb","task_id":"leaf_abstraction-BoomNonBlockingDCache.metaReadArb-c0e75040fe953858","trust":{"frozen_sha256":"1359236bb512c224cb823b95d4a59aa243f37538537b4662ed93121909aa01a3","instance_reuse":{"implementation_sha256":"d82b7a07b5180a67f463d4b4e90c3326be9ad9d8b382745f9dad30d6af751a97","kind":"exact-work-unit","module":"Arbiter6_BoomL1MetaReadReq","source_module":"Arbiter6_BoomL1MetaReadReq","source_work_unit_id":"BoomNonBlockingDCache.metaReadArb","structural_implementation_sha256":"170f52141d1bb9e9a1a3e27c4ea7d09c8bf35aeede8e7ff5059e3f478fcfaec3","target_work_unit_id":"BoomNonBlockingDCache.metaReadArb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":30},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire","Input2Fire","Input3Fire","Input4Fire","Input5Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.metaReadArb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire, Input3Fire, Input4Fire, Input5Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.metaReadArb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"occurrence":"Input2Fire","predicate":"Higher01Valid","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache.metaReadArb::A3","rendered_formula":"Higher01Valid => !Input2Fire"},{"formal":{"occurrence":"Input3Fire","predicate":"Higher012Valid","scope_identity":null,"type":"forbid_when"},"id":"A4","qualified_id":"BoomNonBlockingDCache.metaReadArb::A4","rendered_formula":"Higher012Valid => !Input3Fire"},{"formal":{"occurrence":"Input4Fire","predicate":"Higher0123Valid","scope_identity":null,"type":"forbid_when"},"id":"A5","qualified_id":"BoomNonBlockingDCache.metaReadArb::A5","rendered_formula":"Higher0123Valid => !Input4Fire"},{"formal":{"occurrence":"Input5Fire","predicate":"Higher01234Valid","scope_identity":null,"type":"forbid_when"},"id":"A6","qualified_id":"BoomNonBlockingDCache.metaReadArb::A6","rendered_formula":"Higher01234Valid => !Input5Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.metaReadArb::A7","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.metaReadArb::A8","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"op":"const","value":2},"target":"io.chosen","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.metaReadArb::A9","rendered_formula":"io.chosen = 2 on Input2Fire"},{"formal":{"on":"Input3Fire","scope_identity":null,"source":{"op":"const","value":3},"target":"io.chosen","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.metaReadArb::A10","rendered_formula":"io.chosen = 3 on Input3Fire"},{"formal":{"on":"Input4Fire","scope_identity":null,"source":{"op":"const","value":4},"target":"io.chosen","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.metaReadArb::A11","rendered_formula":"io.chosen = 4 on Input4Fire"},{"formal":{"on":"Input5Fire","scope_identity":null,"source":{"op":"const","value":5},"target":"io.chosen","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.metaReadArb::A12","rendered_formula":"io.chosen = 5 on Input5Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache.metaReadArb::A13","rendered_formula":"io.out.bits.req[0].idx = io.in[0].bits.req[0].idx on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache.metaReadArb::A14","rendered_formula":"io.out.bits.req[0].tag = io.in[0].bits.req[0].tag on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache.metaReadArb::A15","rendered_formula":"io.out.bits.req[0].way_en = io.in[0].bits.req[0].way_en on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A16","qualified_id":"BoomNonBlockingDCache.metaReadArb::A16","rendered_formula":"io.out.bits.req[0].idx = io.in[1].bits.req[0].idx on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A17","qualified_id":"BoomNonBlockingDCache.metaReadArb::A17","rendered_formula":"io.out.bits.req[0].tag = io.in[1].bits.req[0].tag on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A18","qualified_id":"BoomNonBlockingDCache.metaReadArb::A18","rendered_formula":"io.out.bits.req[0].way_en = io.in[1].bits.req[0].way_en on Input1Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A19","qualified_id":"BoomNonBlockingDCache.metaReadArb::A19","rendered_formula":"io.out.bits.req[0].idx = io.in[2].bits.req[0].idx on Input2Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A20","qualified_id":"BoomNonBlockingDCache.metaReadArb::A20","rendered_formula":"io.out.bits.req[0].tag = io.in[2].bits.req[0].tag on Input2Fire"},{"formal":{"on":"Input2Fire","scope_identity":null,"source":{"name":"io.in[2].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A21","qualified_id":"BoomNonBlockingDCache.metaReadArb::A21","rendered_formula":"io.out.bits.req[0].way_en = io.in[2].bits.req[0].way_en on Input2Fire"},{"formal":{"on":"Input3Fire","scope_identity":null,"source":{"name":"io.in[3].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A22","qualified_id":"BoomNonBlockingDCache.metaReadArb::A22","rendered_formula":"io.out.bits.req[0].idx = io.in[3].bits.req[0].idx on Input3Fire"},{"formal":{"on":"Input3Fire","scope_identity":null,"source":{"name":"io.in[3].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A23","qualified_id":"BoomNonBlockingDCache.metaReadArb::A23","rendered_formula":"io.out.bits.req[0].tag = io.in[3].bits.req[0].tag on Input3Fire"},{"formal":{"on":"Input3Fire","scope_identity":null,"source":{"name":"io.in[3].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A24","qualified_id":"BoomNonBlockingDCache.metaReadArb::A24","rendered_formula":"io.out.bits.req[0].way_en = io.in[3].bits.req[0].way_en on Input3Fire"},{"formal":{"on":"Input4Fire","scope_identity":null,"source":{"name":"io.in[4].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A25","qualified_id":"BoomNonBlockingDCache.metaReadArb::A25","rendered_formula":"io.out.bits.req[0].idx = io.in[4].bits.req[0].idx on Input4Fire"},{"formal":{"on":"Input4Fire","scope_identity":null,"source":{"name":"io.in[4].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A26","qualified_id":"BoomNonBlockingDCache.metaReadArb::A26","rendered_formula":"io.out.bits.req[0].tag = io.in[4].bits.req[0].tag on Input4Fire"},{"formal":{"on":"Input4Fire","scope_identity":null,"source":{"name":"io.in[4].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A27","qualified_id":"BoomNonBlockingDCache.metaReadArb::A27","rendered_formula":"io.out.bits.req[0].way_en = io.in[4].bits.req[0].way_en on Input4Fire"},{"formal":{"on":"Input5Fire","scope_identity":null,"source":{"name":"io.in[5].bits.req[0].idx","op":"signal"},"target":"io.out.bits.req[0].idx","type":"signal_equality"},"id":"A28","qualified_id":"BoomNonBlockingDCache.metaReadArb::A28","rendered_formula":"io.out.bits.req[0].idx = io.in[5].bits.req[0].idx on Input5Fire"},{"formal":{"on":"Input5Fire","scope_identity":null,"source":{"name":"io.in[5].bits.req[0].tag","op":"signal"},"target":"io.out.bits.req[0].tag","type":"signal_equality"},"id":"A29","qualified_id":"BoomNonBlockingDCache.metaReadArb::A29","rendered_formula":"io.out.bits.req[0].tag = io.in[5].bits.req[0].tag on Input5Fire"},{"formal":{"on":"Input5Fire","scope_identity":null,"source":{"name":"io.in[5].bits.req[0].way_en","op":"signal"},"target":"io.out.bits.req[0].way_en","type":"signal_equality"},"id":"A30","qualified_id":"BoomNonBlockingDCache.metaReadArb::A30","rendered_formula":"io.out.bits.req[0].way_en = io.in[5].bits.req[0].way_en on Input5Fire"}]}
```

### Child `BoomNonBlockingDCache.metaWriteArb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.metaWriteArb::io.in[0].fire","BoomNonBlockingDCache.metaWriteArb::io.in[1].fire","BoomNonBlockingDCache.metaWriteArb::io.out.fire"],"child_id":"BoomNonBlockingDCache.metaWriteArb","exported_ids":{"axioms":["BoomNonBlockingDCache.metaWriteArb::A1","BoomNonBlockingDCache.metaWriteArb::A10","BoomNonBlockingDCache.metaWriteArb::A11","BoomNonBlockingDCache.metaWriteArb::A12","BoomNonBlockingDCache.metaWriteArb::A13","BoomNonBlockingDCache.metaWriteArb::A14","BoomNonBlockingDCache.metaWriteArb::A2","BoomNonBlockingDCache.metaWriteArb::A3","BoomNonBlockingDCache.metaWriteArb::A4","BoomNonBlockingDCache.metaWriteArb::A5","BoomNonBlockingDCache.metaWriteArb::A6","BoomNonBlockingDCache.metaWriteArb::A7","BoomNonBlockingDCache.metaWriteArb::A8","BoomNonBlockingDCache.metaWriteArb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.metaWriteArb::Input0Fire","BoomNonBlockingDCache.metaWriteArb::Input1Fire","BoomNonBlockingDCache.metaWriteArb::OutputFire"],"predicates":["BoomNonBlockingDCache.metaWriteArb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["metaWriteArb.io.chosen","metaWriteArb.io.in[0].bits.data.coh.state","metaWriteArb.io.in[0].bits.data.tag","metaWriteArb.io.in[0].bits.idx","metaWriteArb.io.in[0].bits.tag","metaWriteArb.io.in[0].bits.way_en","metaWriteArb.io.in[1].bits.data.coh.state","metaWriteArb.io.in[1].bits.data.tag","metaWriteArb.io.in[1].bits.idx","metaWriteArb.io.in[1].bits.tag","metaWriteArb.io.in[1].bits.way_en","metaWriteArb.io.out.bits.data.coh.state","metaWriteArb.io.out.bits.data.tag","metaWriteArb.io.out.bits.idx","metaWriteArb.io.out.bits.tag","metaWriteArb.io.out.bits.way_en"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaWriteArb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.metaWriteArb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaWriteArb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.metaWriteArb::Input1Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.metaWriteArb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.metaWriteArb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.metaWriteArb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"metaWriteArb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.data.coh.state","parent_frontier_signal":"metaWriteArb.io.in[0].bits.data.coh.state","visibility":"direct_frontier"},{"id":"io.in[0].bits.data.tag","parent_frontier_signal":"metaWriteArb.io.in[0].bits.data.tag","visibility":"direct_frontier"},{"id":"io.in[0].bits.idx","parent_frontier_signal":"metaWriteArb.io.in[0].bits.idx","visibility":"direct_frontier"},{"id":"io.in[0].bits.tag","parent_frontier_signal":"metaWriteArb.io.in[0].bits.tag","visibility":"direct_frontier"},{"id":"io.in[0].bits.way_en","parent_frontier_signal":"metaWriteArb.io.in[0].bits.way_en","visibility":"direct_frontier"},{"id":"io.in[1].bits.data.coh.state","parent_frontier_signal":"metaWriteArb.io.in[1].bits.data.coh.state","visibility":"direct_frontier"},{"id":"io.in[1].bits.data.tag","parent_frontier_signal":"metaWriteArb.io.in[1].bits.data.tag","visibility":"direct_frontier"},{"id":"io.in[1].bits.idx","parent_frontier_signal":"metaWriteArb.io.in[1].bits.idx","visibility":"direct_frontier"},{"id":"io.in[1].bits.tag","parent_frontier_signal":"metaWriteArb.io.in[1].bits.tag","visibility":"direct_frontier"},{"id":"io.in[1].bits.way_en","parent_frontier_signal":"metaWriteArb.io.in[1].bits.way_en","visibility":"direct_frontier"},{"id":"io.out.bits.data.coh.state","parent_frontier_signal":"metaWriteArb.io.out.bits.data.coh.state","visibility":"direct_frontier"},{"id":"io.out.bits.data.tag","parent_frontier_signal":"metaWriteArb.io.out.bits.data.tag","visibility":"direct_frontier"},{"id":"io.out.bits.idx","parent_frontier_signal":"metaWriteArb.io.out.bits.idx","visibility":"direct_frontier"},{"id":"io.out.bits.tag","parent_frontier_signal":"metaWriteArb.io.out.bits.tag","visibility":"direct_frontier"},{"id":"io.out.bits.way_en","parent_frontier_signal":"metaWriteArb.io.out.bits.way_en","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.metaWriteArb","task_id":"leaf_abstraction-BoomNonBlockingDCache.metaWriteArb-e1b0f852adc22811","trust":{"frozen_sha256":"8f69b118c1ebfcf02f7ca7655662c5a6f65b2bd0411ec81e0f4cb640432b6169","instance_reuse":{"implementation_sha256":"05098cd523f6b9e3483782c65570147f5a86b79bbeddb23764ee3bff8d4c8c00","kind":"exact-work-unit","module":"Arbiter2_L1MetaWriteReq_1","source_module":"Arbiter2_L1MetaWriteReq_1","source_work_unit_id":"BoomNonBlockingDCache.metaWriteArb","structural_implementation_sha256":"54c2255e9e33b87d9055a6ef61bc5d083684d3ad24a3454ca0d02b54c5caee8c","target_work_unit_id":"BoomNonBlockingDCache.metaWriteArb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":14},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A3","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A3","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.idx","op":"signal"},"target":"io.out.bits.idx","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A4","rendered_formula":"io.out.bits.idx = io.in[0].bits.idx on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A5","rendered_formula":"io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.tag","op":"signal"},"target":"io.out.bits.tag","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A6","rendered_formula":"io.out.bits.tag = io.in[0].bits.tag on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.data.tag","op":"signal"},"target":"io.out.bits.data.tag","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A7","rendered_formula":"io.out.bits.data.tag = io.in[0].bits.data.tag on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.data.coh.state","op":"signal"},"target":"io.out.bits.data.coh.state","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A8","rendered_formula":"io.out.bits.data.coh.state = io.in[0].bits.data.coh.state on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A9","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.idx","op":"signal"},"target":"io.out.bits.idx","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A10","rendered_formula":"io.out.bits.idx = io.in[1].bits.idx on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A11","rendered_formula":"io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.tag","op":"signal"},"target":"io.out.bits.tag","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A12","rendered_formula":"io.out.bits.tag = io.in[1].bits.tag on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.data.tag","op":"signal"},"target":"io.out.bits.data.tag","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A13","rendered_formula":"io.out.bits.data.tag = io.in[1].bits.data.tag on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.data.coh.state","op":"signal"},"target":"io.out.bits.data.coh.state","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache.metaWriteArb::A14","rendered_formula":"io.out.bits.data.coh.state = io.in[1].bits.data.coh.state on Input1Fire"}]}
```

### Child `BoomNonBlockingDCache.meta_0`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.meta_0::io.read.fire","BoomNonBlockingDCache.meta_0::io.write.fire"],"child_id":"BoomNonBlockingDCache.meta_0","exported_ids":{"axioms":["BoomNonBlockingDCache.meta_0::A1","BoomNonBlockingDCache.meta_0::A2","BoomNonBlockingDCache.meta_0::A3","BoomNonBlockingDCache.meta_0::A4"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.meta_0::MetadataWrite","BoomNonBlockingDCache.meta_0::ReadRequest"],"predicates":["BoomNonBlockingDCache.meta_0::ResetActive","BoomNonBlockingDCache.meta_0::WriteRequested"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["meta_0.io.read.bits.idx","meta_0.io.resp[0].coh.state","meta_0.io.resp[0].tag","meta_0.io.resp[1].coh.state","meta_0.io.resp[1].tag","meta_0.io.resp[2].coh.state","meta_0.io.resp[2].tag","meta_0.io.resp[3].coh.state","meta_0.io.resp[3].tag","meta_0.io.write.bits.data.coh.state","meta_0.io.write.bits.data.tag","meta_0.io.write.bits.idx","meta_0.io.write.bits.way_en"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.write.valid && io.write.ready; an accepted external metadata write that updates the ways selected by io.write.bits.way_en at io.write.bits.idx","id":"MetadataWrite","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.meta_0::io.write.fire"],"qualified_id":"BoomNonBlockingDCache.meta_0::MetadataWrite"},{"definition":"io.read.valid && io.read.ready; an accepted synchronous metadata-array read whose set index is sampled by the SyncReadMem read port","id":"ReadRequest","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.meta_0::io.read.fire"],"qualified_id":"BoomNonBlockingDCache.meta_0::ReadRequest"}],"predicates":[{"definition":"rst_cnt < 64","id":"ResetActive","qualified_id":"BoomNonBlockingDCache.meta_0::ResetActive"},{"definition":"io.write.valid","id":"WriteRequested","qualified_id":"BoomNonBlockingDCache.meta_0::WriteRequested"}]},"semantic_signals":[{"id":"io.read.bits.idx","parent_frontier_signal":"meta_0.io.read.bits.idx","visibility":"direct_frontier"},{"id":"io.resp[0].coh.state","parent_frontier_signal":"meta_0.io.resp[0].coh.state","visibility":"direct_frontier"},{"id":"io.resp[0].tag","parent_frontier_signal":"meta_0.io.resp[0].tag","visibility":"direct_frontier"},{"id":"io.resp[1].coh.state","parent_frontier_signal":"meta_0.io.resp[1].coh.state","visibility":"direct_frontier"},{"id":"io.resp[1].tag","parent_frontier_signal":"meta_0.io.resp[1].tag","visibility":"direct_frontier"},{"id":"io.resp[2].coh.state","parent_frontier_signal":"meta_0.io.resp[2].coh.state","visibility":"direct_frontier"},{"id":"io.resp[2].tag","parent_frontier_signal":"meta_0.io.resp[2].tag","visibility":"direct_frontier"},{"id":"io.resp[3].coh.state","parent_frontier_signal":"meta_0.io.resp[3].coh.state","visibility":"direct_frontier"},{"id":"io.resp[3].tag","parent_frontier_signal":"meta_0.io.resp[3].tag","visibility":"direct_frontier"},{"id":"io.write.bits.data.coh.state","parent_frontier_signal":"meta_0.io.write.bits.data.coh.state","visibility":"direct_frontier"},{"id":"io.write.bits.data.tag","parent_frontier_signal":"meta_0.io.write.bits.data.tag","visibility":"direct_frontier"},{"id":"io.write.bits.idx","parent_frontier_signal":"meta_0.io.write.bits.idx","visibility":"direct_frontier"},{"id":"io.write.bits.way_en","parent_frontier_signal":"meta_0.io.write.bits.way_en","visibility":"direct_frontier"},{"id":"rst","visibility":"opaque_child_signal"},{"id":"rst_cnt","visibility":"opaque_child_signal"}],"summary_ref":"umcm://BoomNonBlockingDCache.meta_0","task_id":"leaf_abstraction-BoomNonBlockingDCache.meta_0-3447dc7fee3a0199","trust":{"frozen_sha256":"c8ecb5290f7ae6622b20c00ecf41bc25413a5f2cb341831a4a7311a3ea899d2f","instance_reuse":{"implementation_sha256":"a41c0d556d22f23eb920943ffe3cd4a0c55d8106ee40ac78029e67e01d12a820","kind":"exact-work-unit","module":"L1MetadataArray","source_module":"L1MetadataArray","source_work_unit_id":"BoomNonBlockingDCache.meta_0","structural_implementation_sha256":"f52761fd6b231d0ad4d13c068f39cb466e76a1de8df109d4d3ba58f0529cd522","target_work_unit_id":"BoomNonBlockingDCache.meta_0","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":4},"trusted_axioms":[{"formal":{"initialization":{"active":{"name":"rst","op":"signal"},"address":{"name":"rst_cnt","op":"signal"},"lane_mask":{"op":"const","value":15}},"key":{"address_domain":{"end_exclusive":64,"start":0},"lane":{"count":4,"name":"way"}},"read":{"address":{"name":"io.read.bits.idx","op":"signal"},"latency_cycles":1,"request":"ReadRequest"},"relations":{"co":"MetaCO","fr":"MetaFR","rf":"MetaRF"},"resolution":"latest_prior_write_same_key","scope_identity":null,"storage":"tag_array","type":"indexed_storage_flow","value_fields":[{"initial_value":{"op":"const","value":0},"name":"coh.state","read_targets":[{"name":"io.resp[0].coh.state","op":"signal"},{"name":"io.resp[1].coh.state","op":"signal"},{"name":"io.resp[2].coh.state","op":"signal"},{"name":"io.resp[3].coh.state","op":"signal"}],"storage_bits":{"hi":21,"lo":20},"write_value":{"name":"io.write.bits.data.coh.state","op":"signal"}},{"initial_value":{"op":"const","value":0},"name":"tag","read_targets":[{"name":"io.resp[0].tag","op":"signal"},{"name":"io.resp[1].tag","op":"signal"},{"name":"io.resp[2].tag","op":"signal"},{"name":"io.resp[3].tag","op":"signal"}],"storage_bits":{"hi":19,"lo":0},"write_value":{"name":"io.write.bits.data.tag","op":"signal"}}],"write":{"address":{"name":"io.write.bits.idx","op":"signal"},"lane_mask":{"name":"io.write.bits.way_en","op":"signal"},"on":"MetadataWrite"}},"id":"A1","qualified_id":"BoomNonBlockingDCache.meta_0::A1","rendered_formula":"tag_array[way] latest-write storage flow with explicit initialization; MetaRF=rf, MetaCO=co, MetaFR=rf^-1;co"},{"formal":{"occurrence":"ReadRequest","predicate":"ResetActive","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.meta_0::A2","rendered_formula":"ResetActive => !ReadRequest"},{"formal":{"occurrence":"MetadataWrite","predicate":"ResetActive","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache.meta_0::A3","rendered_formula":"ResetActive => !MetadataWrite"},{"formal":{"occurrence":"ReadRequest","predicate":"WriteRequested","scope_identity":null,"type":"forbid_when"},"id":"A4","qualified_id":"BoomNonBlockingDCache.meta_0::A4","rendered_formula":"WriteRequested => !ReadRequest"}]}
```

### Child `BoomNonBlockingDCache.mshrs`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.mshrs::io.mem_acquire.fire","BoomNonBlockingDCache.mshrs::io.mem_finish.fire","BoomNonBlockingDCache.mshrs::io.mem_grant.fire","BoomNonBlockingDCache.mshrs::io.meta_read.fire","BoomNonBlockingDCache.mshrs::io.meta_resp.valid","BoomNonBlockingDCache.mshrs::io.meta_write.fire","BoomNonBlockingDCache.mshrs::io.prefetch.fire","BoomNonBlockingDCache.mshrs::io.prober_state.valid","BoomNonBlockingDCache.mshrs::io.refill.fire","BoomNonBlockingDCache.mshrs::io.replay.fire","BoomNonBlockingDCache.mshrs::io.req[0].fire","BoomNonBlockingDCache.mshrs::io.resp.fire","BoomNonBlockingDCache.mshrs::io.wb_req.fire"],"child_id":"BoomNonBlockingDCache.mshrs","exported_ids":{"axioms":["BoomNonBlockingDCache.mshrs::A1","BoomNonBlockingDCache.mshrs::A10","BoomNonBlockingDCache.mshrs::A11","BoomNonBlockingDCache.mshrs::A12","BoomNonBlockingDCache.mshrs::A13","BoomNonBlockingDCache.mshrs::A14","BoomNonBlockingDCache.mshrs::A15","BoomNonBlockingDCache.mshrs::A16","BoomNonBlockingDCache.mshrs::A17","BoomNonBlockingDCache.mshrs::A18","BoomNonBlockingDCache.mshrs::A19","BoomNonBlockingDCache.mshrs::A2","BoomNonBlockingDCache.mshrs::A20","BoomNonBlockingDCache.mshrs::A21","BoomNonBlockingDCache.mshrs::A22","BoomNonBlockingDCache.mshrs::A23","BoomNonBlockingDCache.mshrs::A24","BoomNonBlockingDCache.mshrs::A25","BoomNonBlockingDCache.mshrs::A3","BoomNonBlockingDCache.mshrs::A4","BoomNonBlockingDCache.mshrs::A5","BoomNonBlockingDCache.mshrs::A6","BoomNonBlockingDCache.mshrs::A7","BoomNonBlockingDCache.mshrs::A8","BoomNonBlockingDCache.mshrs::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.mshrs.meta_read_arb::Input0Fire","BoomNonBlockingDCache.mshrs.meta_read_arb::Input1Fire","BoomNonBlockingDCache.mshrs.meta_read_arb::OutputFire","BoomNonBlockingDCache.mshrs.meta_write_arb::OutputFire","BoomNonBlockingDCache.mshrs.mmios_0::MemAccess","BoomNonBlockingDCache.mshrs.mmios_0::ReqAccept","BoomNonBlockingDCache.mshrs.mmios_0::RespHandshake","BoomNonBlockingDCache.mshrs.mshrs_0::CommitRefillBeat","BoomNonBlockingDCache.mshrs.mshrs_0::MemAcquire","BoomNonBlockingDCache.mshrs.mshrs_0::MemFinish","BoomNonBlockingDCache.mshrs.mshrs_0::MemGrant","BoomNonBlockingDCache.mshrs.mshrs_0::MetaRead","BoomNonBlockingDCache.mshrs.mshrs_0::ReplayHandshake","BoomNonBlockingDCache.mshrs.mshrs_0::RespHandshake","BoomNonBlockingDCache.mshrs.mshrs_0::WBReq","BoomNonBlockingDCache.mshrs.mshrs_1::CommitRefillBeat","BoomNonBlockingDCache.mshrs.mshrs_1::MemAcquire","BoomNonBlockingDCache.mshrs.mshrs_1::MemFinish","BoomNonBlockingDCache.mshrs.mshrs_1::MemGrant","BoomNonBlockingDCache.mshrs.mshrs_1::MetaRead","BoomNonBlockingDCache.mshrs.mshrs_1::ReplayHandshake","BoomNonBlockingDCache.mshrs.mshrs_1::RespHandshake","BoomNonBlockingDCache.mshrs.mshrs_1::WBReq","BoomNonBlockingDCache.mshrs.refill_arb::Input0Fire","BoomNonBlockingDCache.mshrs.refill_arb::Input1Fire","BoomNonBlockingDCache.mshrs.refill_arb::OutputFire","BoomNonBlockingDCache.mshrs.replay_arb::Input0Fire","BoomNonBlockingDCache.mshrs.replay_arb::Input1Fire","BoomNonBlockingDCache.mshrs.replay_arb::OutputFire","BoomNonBlockingDCache.mshrs.resp_arb::Input0Fire","BoomNonBlockingDCache.mshrs.resp_arb::Input1Fire","BoomNonBlockingDCache.mshrs.resp_arb::Input2Fire","BoomNonBlockingDCache.mshrs.resp_arb::OutputFire","BoomNonBlockingDCache.mshrs.respq::DeqHandshake","BoomNonBlockingDCache.mshrs.respq::EnqHandshake","BoomNonBlockingDCache.mshrs.respq::QueueInsert","BoomNonBlockingDCache.mshrs.wb_req_arb::Input0Fire","BoomNonBlockingDCache.mshrs.wb_req_arb::Input1Fire","BoomNonBlockingDCache.mshrs.wb_req_arb::OutputFire","BoomNonBlockingDCache.mshrs::MMIOAccept","BoomNonBlockingDCache.mshrs::MMIOGrantDelivery","BoomNonBlockingDCache.mshrs::MemAcquire","BoomNonBlockingDCache.mshrs::MemFinish","BoomNonBlockingDCache.mshrs::MemGrant","BoomNonBlockingDCache.mshrs::MetaRead","BoomNonBlockingDCache.mshrs::MetaWrite","BoomNonBlockingDCache.mshrs::PrimaryMSHRAccept","BoomNonBlockingDCache.mshrs::Refill","BoomNonBlockingDCache.mshrs::Replay","BoomNonBlockingDCache.mshrs::RequestAccept","BoomNonBlockingDCache.mshrs::RespHandshake","BoomNonBlockingDCache.mshrs::SecondaryMSHRAccept","BoomNonBlockingDCache.mshrs::WBReq"],"predicates":[]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[{"id":"BoomNonBlockingDCache.mshrs.mmio_alloc_arb::A3","kind":"axiom"},{"id":"BoomNonBlockingDCache.mshrs.mmio_alloc_arb::A4","kind":"axiom"},{"id":"BoomNonBlockingDCache.mshrs.prefetcher::A1","kind":"axiom"},{"id":"BoomNonBlockingDCache.mshrs.respq::A9","kind":"axiom"},{"id":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input0Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input1Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.meta_read_arb::OutputFire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.meta_write_arb::OutputFire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mmios_0::MemAccess","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mmios_0::ReqAccept","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mmios_0::RespHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::CommitRefillBeat","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::MemAcquire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::MemFinish","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::MemGrant","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::MetaRead","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::ReplayHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::RespHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_0::WBReq","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::CommitRefillBeat","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::MemAcquire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::MemFinish","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::MemGrant","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::MetaRead","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::ReplayHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::RespHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.mshrs_1::WBReq","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.refill_arb::Input0Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.refill_arb::Input1Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.refill_arb::OutputFire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.replay_arb::Input0Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.replay_arb::Input1Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.replay_arb::OutputFire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.resp_arb::Input0Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.resp_arb::Input1Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.resp_arb::Input2Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.resp_arb::OutputFire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.respq::DeqHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.respq::EnqHandshake","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.respq::QueueInsert","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input0Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input1Fire","kind":"occurrence"},{"id":"BoomNonBlockingDCache.mshrs.wb_req_arb::OutputFire","kind":"occurrence"}],"relevant_frontier_signals":["mshrs.io.prefetch.valid"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.req[0].valid && io.req[0].ready && !cacheable","id":"MMIOAccept","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.mshrs::MMIOAccept"},{"definition":"io.mem_grant.valid && io.mem_grant.ready && io.mem_grant.bits.source == 3","id":"MMIOGrantDelivery","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.mshrs::MMIOGrantDelivery"},{"definition":"io.mem_acquire.valid && io.mem_acquire.ready","id":"MemAcquire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.mem_acquire.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::MemAcquire"},{"definition":"io.mem_finish.valid && io.mem_finish.ready","id":"MemFinish","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.mem_finish.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::MemFinish"},{"definition":"io.mem_grant.valid && io.mem_grant.ready","id":"MemGrant","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.mem_grant.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::MemGrant"},{"definition":"io.meta_read.valid && io.meta_read.ready","id":"MetaRead","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.meta_read.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::MetaRead"},{"definition":"io.meta_write.valid && io.meta_write.ready","id":"MetaWrite","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.meta_write.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::MetaWrite"},{"definition":"io.req[0].valid && io.req[0].ready && cacheable && !idx_match[0]","id":"PrimaryMSHRAccept","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.mshrs::PrimaryMSHRAccept"},{"definition":"io.refill.valid && io.refill.ready","id":"Refill","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.refill.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::Refill"},{"definition":"io.replay.valid && io.replay.ready","id":"Replay","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.replay.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::Replay"},{"definition":"io.req[0].valid && io.req[0].ready","id":"RequestAccept","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.req[0].fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::RequestAccept"},{"definition":"io.resp.valid && io.resp.ready","id":"RespHandshake","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.resp.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::RespHandshake"},{"definition":"io.req[0].valid && io.req[0].ready && cacheable && idx_match[0]","id":"SecondaryMSHRAccept","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.mshrs::SecondaryMSHRAccept"},{"definition":"io.wb_req.valid && io.wb_req.ready","id":"WBReq","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.mshrs::io.wb_req.fire"],"qualified_id":"BoomNonBlockingDCache.mshrs::WBReq"}],"predicates":[]},"semantic_signals":[{"id":"io.prefetch.valid","parent_frontier_signal":"mshrs.io.prefetch.valid","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.mshrs","task_id":"parent_synthesis-BoomMSHRFile-9485e49ea1c75380","trust":{"frozen_sha256":"76aaf4bf43959d504ae77b5138516b1a083b0e6bc38a81e4bda739699876c9bf","instance_reuse":{"implementation_sha256":"cc3acf9fccc2a966bb74086a49fa68bff5b0544f43982c49f6a5f9242c945279","kind":"module-theorem-template-instantiation","module":"BoomMSHRFile","source_module":"BoomMSHRFile","source_work_unit_id":"BoomMSHRFile","structural_implementation_sha256":"a0e26913b822e1c6f3f619d539c1957fb684082ee222c6c24f1de77838388404","target_work_unit_id":"BoomNonBlockingDCache.mshrs","verification":"source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":25},"trusted_axioms":[{"formal":{"parts":["PrimaryMSHRAccept","SecondaryMSHRAccept","MMIOAccept"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"RequestAccept"},"id":"A1","provenance":{"kind":"parent_local","proof_method":"exact-same-cycle-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A1","rendered_formula":"RequestAccept <=> exactly_one_same_cycle({PrimaryMSHRAccept, SecondaryMSHRAccept, MMIOAccept})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mmios_0::ReqAccept"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MMIOAccept"},"id":"A2","provenance":{"kind":"emergent","proof_method":"exact-parent-child-occurrence-partition","source_axioms":["BoomNonBlockingDCache.mshrs.mmio_alloc_arb::A3","BoomNonBlockingDCache.mshrs.mmio_alloc_arb::A4"]},"qualified_id":"BoomNonBlockingDCache.mshrs::A2","rendered_formula":"MMIOAccept <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mmios_0::ReqAccept})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::MemAcquire","BoomNonBlockingDCache.mshrs.mshrs_1::MemAcquire","BoomNonBlockingDCache.mshrs.mmios_0::MemAccess"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MemAcquire"},"id":"A3","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A3","rendered_formula":"MemAcquire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::MemAcquire, BoomNonBlockingDCache.mshrs.mshrs_1::MemAcquire, BoomNonBlockingDCache.mshrs.mmios_0::MemAccess})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::MemGrant","BoomNonBlockingDCache.mshrs.mshrs_1::MemGrant","MMIOGrantDelivery"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MemGrant"},"id":"A4","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A4","rendered_formula":"MemGrant <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::MemGrant, BoomNonBlockingDCache.mshrs.mshrs_1::MemGrant, MMIOGrantDelivery})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::MemFinish","BoomNonBlockingDCache.mshrs.mshrs_1::MemFinish"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MemFinish"},"id":"A5","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A5","rendered_formula":"MemFinish <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::MemFinish, BoomNonBlockingDCache.mshrs.mshrs_1::MemFinish})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.meta_read_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MetaRead"},"id":"A6","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A6","rendered_formula":"MetaRead <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.meta_read_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::MetaRead"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input0Fire"},"id":"A7","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A7","rendered_formula":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::MetaRead})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_1::MetaRead"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input1Fire"},"id":"A8","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A8","rendered_formula":"BoomNonBlockingDCache.mshrs.meta_read_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_1::MetaRead})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.meta_write_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"MetaWrite"},"id":"A9","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A9","rendered_formula":"MetaWrite <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.meta_write_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.wb_req_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"WBReq"},"id":"A10","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A10","rendered_formula":"WBReq <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.wb_req_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::WBReq"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input0Fire"},"id":"A11","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A11","rendered_formula":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::WBReq})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_1::WBReq"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input1Fire"},"id":"A12","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A12","rendered_formula":"BoomNonBlockingDCache.mshrs.wb_req_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_1::WBReq})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.refill_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"Refill"},"id":"A13","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A13","rendered_formula":"Refill <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.refill_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::CommitRefillBeat"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.refill_arb::Input0Fire"},"id":"A14","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A14","rendered_formula":"BoomNonBlockingDCache.mshrs.refill_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::CommitRefillBeat})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_1::CommitRefillBeat"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.refill_arb::Input1Fire"},"id":"A15","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A15","rendered_formula":"BoomNonBlockingDCache.mshrs.refill_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_1::CommitRefillBeat})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.replay_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"Replay"},"id":"A16","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A16","rendered_formula":"Replay <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.replay_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::ReplayHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.replay_arb::Input0Fire"},"id":"A17","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A17","rendered_formula":"BoomNonBlockingDCache.mshrs.replay_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::ReplayHandshake})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_1::ReplayHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.replay_arb::Input1Fire"},"id":"A18","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A18","rendered_formula":"BoomNonBlockingDCache.mshrs.replay_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_1::ReplayHandshake})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_0::RespHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.resp_arb::Input0Fire"},"id":"A19","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A19","rendered_formula":"BoomNonBlockingDCache.mshrs.resp_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_0::RespHandshake})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mshrs_1::RespHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.resp_arb::Input1Fire"},"id":"A20","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A20","rendered_formula":"BoomNonBlockingDCache.mshrs.resp_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mshrs_1::RespHandshake})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.mmios_0::RespHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.resp_arb::Input2Fire"},"id":"A21","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A21","rendered_formula":"BoomNonBlockingDCache.mshrs.resp_arb::Input2Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.mmios_0::RespHandshake})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.resp_arb::OutputFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"BoomNonBlockingDCache.mshrs.respq::EnqHandshake"},"id":"A22","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A22","rendered_formula":"BoomNonBlockingDCache.mshrs.respq::EnqHandshake <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.resp_arb::OutputFire})"},{"formal":{"parts":["BoomNonBlockingDCache.mshrs.respq::DeqHandshake"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"RespHandshake"},"id":"A23","provenance":{"kind":"parent_local","proof_method":"exact-parent-child-occurrence-partition","source_axioms":[]},"qualified_id":"BoomNonBlockingDCache.mshrs::A23","rendered_formula":"RespHandshake <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs.respq::DeqHandshake})"},{"formal":{"after":"RespHandshake","before":"BoomNonBlockingDCache.mshrs.respq::QueueInsert","required_prior":null,"scope_identity":null,"type":"ordered_before"},"id":"A24","provenance":{"kind":"emergent","proof_method":"trusted-history-after-restriction","source_axioms":["BoomNonBlockingDCache.mshrs.respq::A9"]},"qualified_id":"BoomNonBlockingDCache.mshrs::A24","rendered_formula":"BoomNonBlockingDCache.mshrs.respq::QueueInsert <mu RespHandshake"},{"formal":{"expr":{"index":0,"op":"bit","value":{"name":"io.prefetch.valid","op":"signal"}},"on":null,"relation":"eq","scope_identity":null,"type":"value_constraint","value":0},"id":"A25","provenance":{"kind":"lifted","proof_method":"trusted-child-value-lift","source_axioms":["BoomNonBlockingDCache.mshrs.prefetcher::A1"]},"qualified_id":"BoomNonBlockingDCache.mshrs::A25","rendered_formula":"bits(io.prefetch.valid, 0, 0) == 0"}]}
```

### Child `BoomNonBlockingDCache.prober`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.prober::io.lsu_release.fire","BoomNonBlockingDCache.prober::io.meta_read.fire","BoomNonBlockingDCache.prober::io.meta_write.fire","BoomNonBlockingDCache.prober::io.rep.fire","BoomNonBlockingDCache.prober::io.req.fire","BoomNonBlockingDCache.prober::io.state.valid","BoomNonBlockingDCache.prober::io.wb_req.fire"],"child_id":"BoomNonBlockingDCache.prober","exported_ids":{"axioms":["BoomNonBlockingDCache.prober::A1","BoomNonBlockingDCache.prober::A2","BoomNonBlockingDCache.prober::A3","BoomNonBlockingDCache.prober::A4","BoomNonBlockingDCache.prober::A5","BoomNonBlockingDCache.prober::A6","BoomNonBlockingDCache.prober::A7","BoomNonBlockingDCache.prober::A8"],"identity_keys":["BoomNonBlockingDCache.prober::ProbeTxn"],"occurrences":["BoomNonBlockingDCache.prober::LSURelease","BoomNonBlockingDCache.prober::MetaRead","BoomNonBlockingDCache.prober::MetaWrite","BoomNonBlockingDCache.prober::ProbeAck","BoomNonBlockingDCache.prober::ProbeReq","BoomNonBlockingDCache.prober::WBComplete","BoomNonBlockingDCache.prober::WBReq"],"predicates":["BoomNonBlockingDCache.prober::ActiveProbe"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["prober.io.lsu_release.bits.address","prober.io.lsu_release.bits.size","prober.io.lsu_release.bits.source","prober.io.meta_read.bits.idx","prober.io.meta_read.bits.tag","prober.io.meta_write.bits.data.coh.state","prober.io.meta_write.bits.data.tag","prober.io.meta_write.bits.idx","prober.io.meta_write.bits.tag","prober.io.rep.bits.address","prober.io.rep.bits.opcode","prober.io.rep.bits.size","prober.io.rep.bits.source","prober.io.wb_req.bits.idx","prober.io.wb_req.bits.source","prober.io.wb_req.bits.tag"],"semantic_objects":{"identity_keys":[{"description":"The accepted TileLink-B request is latched in req and carries Probe identity through the transaction.","fields":["address","source","size","param"],"id":"ProbeTxn","qualified_id":"BoomNonBlockingDCache.prober::ProbeTxn"}],"occurrences":[{"definition":"io.lsu_release.fire","id":"LSURelease","kind":"boundary","multiplicity":"at_most_once","physical_event_ids":["BoomNonBlockingDCache.prober::io.lsu_release.fire"],"qualified_id":"BoomNonBlockingDCache.prober::LSURelease"},{"definition":"io.meta_read.fire","id":"MetaRead","kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.prober::io.meta_read.fire"],"qualified_id":"BoomNonBlockingDCache.prober::MetaRead"},{"definition":"io.meta_write.fire","id":"MetaWrite","kind":"boundary","multiplicity":"at_most_once","physical_event_ids":["BoomNonBlockingDCache.prober::io.meta_write.fire"],"qualified_id":"BoomNonBlockingDCache.prober::MetaWrite"},{"definition":"io.rep.fire","id":"ProbeAck","kind":"boundary","multiplicity":"at_most_once","physical_event_ids":["BoomNonBlockingDCache.prober::io.rep.fire"],"qualified_id":"BoomNonBlockingDCache.prober::ProbeAck"},{"definition":"io.req.fire","id":"ProbeReq","kind":"boundary","multiplicity":"exactly_once","physical_event_ids":["BoomNonBlockingDCache.prober::io.req.fire"],"qualified_id":"BoomNonBlockingDCache.prober::ProbeReq"},{"definition":"state == s_writeback_resp (8) && io.wb_req.ready","id":"WBComplete","kind":"derived","multiplicity":"at_most_once","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.prober::WBComplete"},{"definition":"io.wb_req.fire","id":"WBReq","kind":"boundary","multiplicity":"at_most_once","physical_event_ids":["BoomNonBlockingDCache.prober::io.wb_req.fire"],"qualified_id":"BoomNonBlockingDCache.prober::WBReq"}],"predicates":[{"definition":"state != s_invalid","id":"ActiveProbe","qualified_id":"BoomNonBlockingDCache.prober::ActiveProbe"}]},"semantic_signals":[{"id":"io.lsu_release.bits.address","parent_frontier_signal":"prober.io.lsu_release.bits.address","visibility":"direct_frontier"},{"id":"io.lsu_release.bits.size","parent_frontier_signal":"prober.io.lsu_release.bits.size","visibility":"direct_frontier"},{"id":"io.lsu_release.bits.source","parent_frontier_signal":"prober.io.lsu_release.bits.source","visibility":"direct_frontier"},{"id":"io.meta_read.bits.idx","parent_frontier_signal":"prober.io.meta_read.bits.idx","visibility":"direct_frontier"},{"id":"io.meta_read.bits.tag","parent_frontier_signal":"prober.io.meta_read.bits.tag","visibility":"direct_frontier"},{"id":"io.meta_write.bits.data.coh.state","parent_frontier_signal":"prober.io.meta_write.bits.data.coh.state","visibility":"direct_frontier"},{"id":"io.meta_write.bits.data.tag","parent_frontier_signal":"prober.io.meta_write.bits.data.tag","visibility":"direct_frontier"},{"id":"io.meta_write.bits.idx","parent_frontier_signal":"prober.io.meta_write.bits.idx","visibility":"direct_frontier"},{"id":"io.meta_write.bits.tag","parent_frontier_signal":"prober.io.meta_write.bits.tag","visibility":"direct_frontier"},{"id":"io.rep.bits.address","parent_frontier_signal":"prober.io.rep.bits.address","visibility":"direct_frontier"},{"id":"io.rep.bits.opcode","parent_frontier_signal":"prober.io.rep.bits.opcode","visibility":"direct_frontier"},{"id":"io.rep.bits.size","parent_frontier_signal":"prober.io.rep.bits.size","visibility":"direct_frontier"},{"id":"io.rep.bits.source","parent_frontier_signal":"prober.io.rep.bits.source","visibility":"direct_frontier"},{"id":"io.req.bits","visibility":"opaque_child_signal"},{"id":"io.wb_req.bits.idx","parent_frontier_signal":"prober.io.wb_req.bits.idx","visibility":"direct_frontier"},{"id":"io.wb_req.bits.source","parent_frontier_signal":"prober.io.wb_req.bits.source","visibility":"direct_frontier"},{"id":"io.wb_req.bits.tag","parent_frontier_signal":"prober.io.wb_req.bits.tag","visibility":"direct_frontier"},{"id":"is_dirty","visibility":"opaque_child_signal"},{"id":"reply_coh.state","visibility":"opaque_child_signal"},{"id":"report_param","visibility":"opaque_child_signal"},{"id":"req","visibility":"opaque_child_signal"},{"id":"req.address","visibility":"opaque_child_signal"},{"id":"req.param","visibility":"opaque_child_signal"},{"id":"req.size","visibility":"opaque_child_signal"},{"id":"req.source","visibility":"opaque_child_signal"}],"summary_ref":"umcm://BoomNonBlockingDCache.prober","task_id":"leaf_abstraction-BoomProbeUnit-6a11da8fc6b94afe","trust":{"frozen_sha256":"cee8ffbc1ab3ff5d19268df8fd5b5eb8e9f5fddae52d964e138f365949760d02","instance_reuse":{"implementation_sha256":"bf3247523d50ae9e76538398e4a66e3aa94bf8652aba4bdbdd76095bec1f194c","kind":"module-theorem-template-instantiation","module":"BoomProbeUnit","source_module":"BoomProbeUnit","source_work_unit_id":"BoomProbeUnit","structural_implementation_sha256":"ad723e31ef148648469f13bc8d91cb5e54ccf5d6a64d33725f8f27a8035edded","target_work_unit_id":"BoomNonBlockingDCache.prober","verification":"source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":8},"trusted_axioms":[{"formal":{"occurrence":"ProbeReq","predicate":"ActiveProbe","scope_identity":"ProbeTxn","type":"forbid_when"},"id":"A1","qualified_id":"BoomNonBlockingDCache.prober::A1","rendered_formula":"ActiveProbe => !ProbeReq [same ProbeTxn]"},{"formal":{"capture":{"carrier":"req","on":"ProbeReq","source":"io.req.bits"},"identity":"ProbeTxn","projections":[{"expr":{"hi":11,"lo":6,"op":"slice","value":{"name":"req.address","op":"signal"}},"on":"MetaRead","target":"io.meta_read.bits.idx"},{"expr":{"amount":12,"op":"shr","value":{"name":"req.address","op":"signal"}},"on":"MetaRead","target":"io.meta_read.bits.tag"},{"expr":{"name":"req.address","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.address"},{"expr":{"name":"req.source","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.source"},{"expr":{"name":"req.size","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.size"},{"expr":{"name":"req.address","op":"signal"},"on":"ProbeAck","target":"io.rep.bits.address"},{"expr":{"name":"req.source","op":"signal"},"on":"ProbeAck","target":"io.rep.bits.source"},{"expr":{"name":"req.size","op":"signal"},"on":"ProbeAck","target":"io.rep.bits.size"},{"expr":{"name":"req.source","op":"signal"},"on":"WBReq","target":"io.wb_req.bits.source"},{"expr":{"hi":11,"lo":6,"op":"slice","value":{"name":"req.address","op":"signal"}},"on":"WBReq","target":"io.wb_req.bits.idx"},{"expr":{"amount":12,"op":"shr","value":{"name":"req.address","op":"signal"}},"on":"WBReq","target":"io.wb_req.bits.tag"},{"expr":{"hi":11,"lo":6,"op":"slice","value":{"name":"req.address","op":"signal"}},"on":"MetaWrite","target":"io.meta_write.bits.idx"},{"expr":{"amount":12,"op":"shr","value":{"name":"req.address","op":"signal"}},"on":"MetaWrite","target":"io.meta_write.bits.tag"},{"expr":{"amount":12,"op":"shr","value":{"name":"req.address","op":"signal"}},"on":"MetaWrite","target":"io.meta_write.bits.data.tag"}],"type":"identity_flow"},"id":"A2","qualified_id":"BoomNonBlockingDCache.prober::A2","rendered_formula":"capture ProbeTxn := io.req.bits on ProbeReq; preserve 14 exact identity projections"},{"formal":{"left":"WBReq","rights":["LSURelease","ProbeAck"],"scope_identity":"ProbeTxn","type":"exclusion"},"id":"A3","qualified_id":"BoomNonBlockingDCache.prober::A3","rendered_formula":"WBReq excludes {LSURelease, ProbeAck} [same ProbeTxn]"},{"formal":{"after":"ProbeAck","before":"LSURelease","required_prior":null,"scope_identity":"ProbeTxn","type":"ordered_before"},"id":"A4","qualified_id":"BoomNonBlockingDCache.prober::A4","rendered_formula":"LSURelease <mu ProbeAck [same ProbeTxn]"},{"formal":{"scope_identity":"ProbeTxn","sequence":["LSURelease","ProbeAck","MetaWrite"],"type":"ordered_chain"},"id":"A5","qualified_id":"BoomNonBlockingDCache.prober::A5","rendered_formula":"LSURelease <mu ProbeAck <mu MetaWrite [same ProbeTxn]"},{"formal":{"scope_identity":"ProbeTxn","sequence":["WBReq","WBComplete","MetaWrite"],"type":"ordered_chain"},"id":"A6","qualified_id":"BoomNonBlockingDCache.prober::A6","rendered_formula":"WBReq <mu WBComplete <mu MetaWrite [same ProbeTxn]"},{"formal":{"bindings":{"current_state":"reply_coh.state","dirty":"is_dirty","next_state":"io.meta_write.bits.data.coh.state","param":"req.param","report":"report_param"},"on":"MetaWrite","scope_identity":"ProbeTxn","spec":"tilelink.ClientMetadata.onProbe","type":"spec_relation"},"id":"A7","qualified_id":"BoomNonBlockingDCache.prober::A7","rendered_formula":"bindings satisfy tilelink.ClientMetadata.onProbe on MetaWrite [same ProbeTxn]"},{"formal":{"expr":{"index":0,"op":"bit","value":{"name":"io.rep.bits.opcode","op":"signal"}},"on":"ProbeAck","relation":"eq","scope_identity":"ProbeTxn","type":"value_constraint","value":0},"id":"A8","qualified_id":"BoomNonBlockingDCache.prober::A8","rendered_formula":"bits(io.rep.bits.opcode, 0, 0) == 0 on ProbeAck [same ProbeTxn]"}]}
```

### Child `BoomNonBlockingDCache.wb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.wb::io.data_req.fire","BoomNonBlockingDCache.wb::io.idx.valid","BoomNonBlockingDCache.wb::io.lsu_release.fire","BoomNonBlockingDCache.wb::io.meta_read.fire","BoomNonBlockingDCache.wb::io.release.fire","BoomNonBlockingDCache.wb::io.req.fire"],"child_id":"BoomNonBlockingDCache.wb","exported_ids":{"axioms":["BoomNonBlockingDCache.wb::A1","BoomNonBlockingDCache.wb::A10","BoomNonBlockingDCache.wb::A2","BoomNonBlockingDCache.wb::A3","BoomNonBlockingDCache.wb::A4","BoomNonBlockingDCache.wb::A5","BoomNonBlockingDCache.wb::A6","BoomNonBlockingDCache.wb::A7","BoomNonBlockingDCache.wb::A8","BoomNonBlockingDCache.wb::A9"],"identity_keys":["BoomNonBlockingDCache.wb::WritebackTxn"],"occurrences":["BoomNonBlockingDCache.wb::BufferBeat","BoomNonBlockingDCache.wb::BufferFilled","BoomNonBlockingDCache.wb::FillIssue","BoomNonBlockingDCache.wb::LSURelease","BoomNonBlockingDCache.wb::MemGrantSeen","BoomNonBlockingDCache.wb::ReleaseBeat","BoomNonBlockingDCache.wb::ReleaseComplete","BoomNonBlockingDCache.wb::VoluntaryDone","BoomNonBlockingDCache.wb::WritebackReq"],"predicates":["BoomNonBlockingDCache.wb::ActiveWriteback","BoomNonBlockingDCache.wb::BeforeNetworkRelease"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["wb.io.data_req.bits.way_en","wb.io.lsu_release.bits.address","wb.io.lsu_release.bits.param","wb.io.lsu_release.bits.source","wb.io.meta_read.bits.idx","wb.io.meta_read.bits.tag","wb.io.release.bits.data","wb.io.release.bits.opcode"],"semantic_objects":{"identity_keys":[{"description":"The accepted WritebackReq is latched in req and carries the cache-line identity and writeback mode through the transaction.","fields":["tag","idx","source","param","way_en","voluntary"],"id":"WritebackTxn","qualified_id":"BoomNonBlockingDCache.wb::WritebackTxn"}],"occurrences":[{"definition":"r2_data_req_fired && wb_buffer[r2_data_req_cnt] := io.data_resp","id":"BufferBeat","index":{"domain":{"end_exclusive":8,"start":0},"expr":{"name":"r2_data_req_cnt","op":"signal"},"name":"beat"},"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::BufferBeat"},{"definition":"last buffer beat is captured (r2_data_req_cnt == 7), io.resp is asserted, and state enters s_lsu_release","id":"BufferFilled","kind":"derived","multiplicity":"at_most_once","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::BufferFilled"},{"definition":"io.data_req.fire && io.meta_read.fire","id":"FillIssue","index":{"domain":{"end_exclusive":8,"start":0},"expr":{"name":"data_req_cnt","op":"signal"},"name":"beat"},"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::FillIssue"},{"definition":"io.lsu_release.fire","id":"LSURelease","kind":"boundary","multiplicity":"at_most_once","physical_event_ids":["BoomNonBlockingDCache.wb::io.lsu_release.fire"],"qualified_id":"BoomNonBlockingDCache.wb::LSURelease"},{"definition":"io.mem_grant while the writeback transaction is in active/grant processing","id":"MemGrantSeen","kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::MemGrantSeen"},{"definition":"io.release.fire","id":"ReleaseBeat","index":{"domain":{"end_exclusive":8,"start":0},"expr":{"name":"data_req_cnt","op":"signal"},"name":"beat"},"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.wb::io.release.fire"],"qualified_id":"BoomNonBlockingDCache.wb::ReleaseBeat"},{"definition":"state == s_active && data_req_cnt == 7 && io.release.fire; the last network release beat is accepted","id":"ReleaseComplete","kind":"derived","multiplicity":"at_most_once","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::ReleaseComplete"},{"definition":"state == s_grant && acked; state returns to s_invalid","id":"VoluntaryDone","kind":"derived","multiplicity":"at_most_once","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache.wb::VoluntaryDone"},{"definition":"io.req.fire","id":"WritebackReq","kind":"boundary","multiplicity":"exactly_once","physical_event_ids":["BoomNonBlockingDCache.wb::io.req.fire"],"qualified_id":"BoomNonBlockingDCache.wb::WritebackReq"}],"predicates":[{"definition":"state != s_invalid","id":"ActiveWriteback","qualified_id":"BoomNonBlockingDCache.wb::ActiveWriteback"},{"definition":"state is s_fill_buffer or s_lsu_release","id":"BeforeNetworkRelease","qualified_id":"BoomNonBlockingDCache.wb::BeforeNetworkRelease"}]},"semantic_signals":[{"id":"io.data_req.bits.way_en","parent_frontier_signal":"wb.io.data_req.bits.way_en","visibility":"direct_frontier"},{"id":"io.lsu_release.bits.address","parent_frontier_signal":"wb.io.lsu_release.bits.address","visibility":"direct_frontier"},{"id":"io.lsu_release.bits.param","parent_frontier_signal":"wb.io.lsu_release.bits.param","visibility":"direct_frontier"},{"id":"io.lsu_release.bits.source","parent_frontier_signal":"wb.io.lsu_release.bits.source","visibility":"direct_frontier"},{"id":"io.meta_read.bits.idx","parent_frontier_signal":"wb.io.meta_read.bits.idx","visibility":"direct_frontier"},{"id":"io.meta_read.bits.tag","parent_frontier_signal":"wb.io.meta_read.bits.tag","visibility":"direct_frontier"},{"id":"io.release.bits.data","parent_frontier_signal":"wb.io.release.bits.data","visibility":"direct_frontier"},{"id":"io.release.bits.opcode","parent_frontier_signal":"wb.io.release.bits.opcode","visibility":"direct_frontier"},{"id":"io.req.bits","visibility":"opaque_child_signal"},{"id":"r_address","visibility":"opaque_child_signal"},{"id":"req","visibility":"opaque_child_signal"},{"id":"req.idx","visibility":"opaque_child_signal"},{"id":"req.param","visibility":"opaque_child_signal"},{"id":"req.source","visibility":"opaque_child_signal"},{"id":"req.tag","visibility":"opaque_child_signal"},{"id":"req.way_en","visibility":"opaque_child_signal"},{"id":"wb_buffer","visibility":"opaque_child_signal"}],"summary_ref":"umcm://BoomNonBlockingDCache.wb","task_id":"leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b","trust":{"frozen_sha256":"42872eaadbaf154adae4cf2a06c50651e536ae39d7ffb38faf608a4b33d2e368","instance_reuse":{"implementation_sha256":"9e8a9ce450daa072ddcf23345a9d3e68b8d17b7da108744543307360810d3c72","kind":"module-theorem-template-instantiation","module":"BoomWritebackUnit","source_module":"BoomWritebackUnit","source_work_unit_id":"BoomWritebackUnit","structural_implementation_sha256":"30f49d3e367fd3cc6254ff2669485289dee9b0f44931a91fe8b49e586960ec39","target_work_unit_id":"BoomNonBlockingDCache.wb","verification":"source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":10},"trusted_axioms":[{"formal":{"occurrence":"WritebackReq","predicate":"ActiveWriteback","scope_identity":"WritebackTxn","scope_index":null,"type":"forbid_when"},"id":"A1","qualified_id":"BoomNonBlockingDCache.wb::A1","rendered_formula":"ActiveWriteback => !WritebackReq [same WritebackTxn]"},{"formal":{"capture":{"carrier":"req","on":"WritebackReq","source":"io.req.bits"},"identity":"WritebackTxn","projections":[{"expr":{"name":"req.idx","op":"signal"},"on":"FillIssue","target":"io.meta_read.bits.idx"},{"expr":{"name":"req.tag","op":"signal"},"on":"FillIssue","target":"io.meta_read.bits.tag"},{"expr":{"name":"req.way_en","op":"signal"},"on":"FillIssue","target":"io.data_req.bits.way_en"},{"expr":{"name":"r_address","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.address"},{"expr":{"name":"req.param","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.param"},{"expr":{"name":"req.source","op":"signal"},"on":"LSURelease","target":"io.lsu_release.bits.source"}],"type":"identity_flow"},"id":"A2","qualified_id":"BoomNonBlockingDCache.wb::A2","rendered_formula":"capture WritebackTxn := io.req.bits on WritebackReq; preserve 6 exact identity projections"},{"formal":{"cardinality":"exactly_once","completion":"BufferFilled","domain":{"end_exclusive":8,"start":0},"index":"beat","occurrence":"BufferBeat","scope_identity":"WritebackTxn","scope_index":null,"type":"indexed_complete"},"id":"A3","qualified_id":"BoomNonBlockingDCache.wb::A3","rendered_formula":"BufferFilled => forall beat in [0, 8): count(BufferBeat(beat)) = 1 [same WritebackTxn]"},{"formal":{"after":"BufferBeat","before":"FillIssue","required_prior":null,"scope_identity":"WritebackTxn","scope_index":{"name":"beat","relation":"same"},"type":"ordered_before"},"id":"A4","qualified_id":"BoomNonBlockingDCache.wb::A4","rendered_formula":"FillIssue <mu BufferBeat [same WritebackTxn] [same index beat]"},{"formal":{"after":"LSURelease","before":"BufferFilled","required_prior":null,"scope_identity":"WritebackTxn","scope_index":null,"type":"ordered_before"},"id":"A5","qualified_id":"BoomNonBlockingDCache.wb::A5","rendered_formula":"BufferFilled <mu LSURelease [same WritebackTxn]"},{"formal":{"occurrence":"ReleaseBeat","predicate":"BeforeNetworkRelease","scope_identity":"WritebackTxn","scope_index":null,"type":"forbid_when"},"id":"A6","qualified_id":"BoomNonBlockingDCache.wb::A6","rendered_formula":"BeforeNetworkRelease => !ReleaseBeat [same WritebackTxn]"},{"formal":{"cardinality":"exactly_once","completion":"ReleaseComplete","domain":{"end_exclusive":8,"start":0},"index":"beat","occurrence":"ReleaseBeat","scope_identity":"WritebackTxn","scope_index":null,"type":"indexed_complete"},"id":"A7","qualified_id":"BoomNonBlockingDCache.wb::A7","rendered_formula":"ReleaseComplete => forall beat in [0, 8): count(ReleaseBeat(beat)) = 1 [same WritebackTxn]"},{"formal":{"on":"ReleaseBeat","scope_identity":"WritebackTxn","scope_index":{"name":"beat","relation":"same"},"source":{"index":{"name":"beat","op":"index_var"},"op":"lookup","value":{"name":"wb_buffer","op":"signal"}},"target":"io.release.bits.data","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.wb::A8","rendered_formula":"io.release.bits.data = wb_buffer[beat] on ReleaseBeat [same WritebackTxn] [same index beat]"},{"formal":{"expr":{"index":0,"op":"bit","value":{"name":"io.release.bits.opcode","op":"signal"}},"on":"ReleaseBeat","relation":"eq","scope_identity":"WritebackTxn","scope_index":null,"type":"value_constraint","value":1},"id":"A9","qualified_id":"BoomNonBlockingDCache.wb::A9","rendered_formula":"bits(io.release.bits.opcode, 0, 0) == 1 on ReleaseBeat [same WritebackTxn]"},{"formal":{"after":"VoluntaryDone","prerequisites":["ReleaseComplete","MemGrantSeen"],"scope_identity":"WritebackTxn","scope_index":null,"type":"join"},"id":"A10","qualified_id":"BoomNonBlockingDCache.wb::A10","rendered_formula":"{ReleaseComplete, MemGrantSeen} <mu VoluntaryDone [same WritebackTxn]"}]}
```

### Child `BoomNonBlockingDCache.wbArb`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache.wbArb::io.in[0].fire","BoomNonBlockingDCache.wbArb::io.in[1].fire","BoomNonBlockingDCache.wbArb::io.out.fire"],"child_id":"BoomNonBlockingDCache.wbArb","exported_ids":{"axioms":["BoomNonBlockingDCache.wbArb::A1","BoomNonBlockingDCache.wbArb::A10","BoomNonBlockingDCache.wbArb::A11","BoomNonBlockingDCache.wbArb::A12","BoomNonBlockingDCache.wbArb::A13","BoomNonBlockingDCache.wbArb::A14","BoomNonBlockingDCache.wbArb::A15","BoomNonBlockingDCache.wbArb::A16","BoomNonBlockingDCache.wbArb::A2","BoomNonBlockingDCache.wbArb::A3","BoomNonBlockingDCache.wbArb::A4","BoomNonBlockingDCache.wbArb::A5","BoomNonBlockingDCache.wbArb::A6","BoomNonBlockingDCache.wbArb::A7","BoomNonBlockingDCache.wbArb::A8","BoomNonBlockingDCache.wbArb::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache.wbArb::Input0Fire","BoomNonBlockingDCache.wbArb::Input1Fire","BoomNonBlockingDCache.wbArb::OutputFire"],"predicates":["BoomNonBlockingDCache.wbArb::Input0Valid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["wbArb.io.chosen","wbArb.io.in[0].bits.idx","wbArb.io.in[0].bits.param","wbArb.io.in[0].bits.source","wbArb.io.in[0].bits.tag","wbArb.io.in[0].bits.voluntary","wbArb.io.in[0].bits.way_en","wbArb.io.in[1].bits.idx","wbArb.io.in[1].bits.param","wbArb.io.in[1].bits.source","wbArb.io.in[1].bits.tag","wbArb.io.in[1].bits.voluntary","wbArb.io.in[1].bits.way_en","wbArb.io.out.bits.idx","wbArb.io.out.bits.param","wbArb.io.out.bits.source","wbArb.io.out.bits.tag","wbArb.io.out.bits.voluntary","wbArb.io.out.bits.way_en"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.in[0].valid && io.in[0].ready","id":"Input0Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.wbArb::io.in[0].fire"],"qualified_id":"BoomNonBlockingDCache.wbArb::Input0Fire"},{"definition":"io.in[1].valid && io.in[1].ready","id":"Input1Fire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.wbArb::io.in[1].fire"],"qualified_id":"BoomNonBlockingDCache.wbArb::Input1Fire"},{"definition":"io.out.valid && io.out.ready","id":"OutputFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache.wbArb::io.out.fire"],"qualified_id":"BoomNonBlockingDCache.wbArb::OutputFire"}],"predicates":[{"definition":"io.in[0].valid","id":"Input0Valid","qualified_id":"BoomNonBlockingDCache.wbArb::Input0Valid"}]},"semantic_signals":[{"id":"io.chosen","parent_frontier_signal":"wbArb.io.chosen","visibility":"direct_frontier"},{"id":"io.in[0].bits.idx","parent_frontier_signal":"wbArb.io.in[0].bits.idx","visibility":"direct_frontier"},{"id":"io.in[0].bits.param","parent_frontier_signal":"wbArb.io.in[0].bits.param","visibility":"direct_frontier"},{"id":"io.in[0].bits.source","parent_frontier_signal":"wbArb.io.in[0].bits.source","visibility":"direct_frontier"},{"id":"io.in[0].bits.tag","parent_frontier_signal":"wbArb.io.in[0].bits.tag","visibility":"direct_frontier"},{"id":"io.in[0].bits.voluntary","parent_frontier_signal":"wbArb.io.in[0].bits.voluntary","visibility":"direct_frontier"},{"id":"io.in[0].bits.way_en","parent_frontier_signal":"wbArb.io.in[0].bits.way_en","visibility":"direct_frontier"},{"id":"io.in[1].bits.idx","parent_frontier_signal":"wbArb.io.in[1].bits.idx","visibility":"direct_frontier"},{"id":"io.in[1].bits.param","parent_frontier_signal":"wbArb.io.in[1].bits.param","visibility":"direct_frontier"},{"id":"io.in[1].bits.source","parent_frontier_signal":"wbArb.io.in[1].bits.source","visibility":"direct_frontier"},{"id":"io.in[1].bits.tag","parent_frontier_signal":"wbArb.io.in[1].bits.tag","visibility":"direct_frontier"},{"id":"io.in[1].bits.voluntary","parent_frontier_signal":"wbArb.io.in[1].bits.voluntary","visibility":"direct_frontier"},{"id":"io.in[1].bits.way_en","parent_frontier_signal":"wbArb.io.in[1].bits.way_en","visibility":"direct_frontier"},{"id":"io.out.bits.idx","parent_frontier_signal":"wbArb.io.out.bits.idx","visibility":"direct_frontier"},{"id":"io.out.bits.param","parent_frontier_signal":"wbArb.io.out.bits.param","visibility":"direct_frontier"},{"id":"io.out.bits.source","parent_frontier_signal":"wbArb.io.out.bits.source","visibility":"direct_frontier"},{"id":"io.out.bits.tag","parent_frontier_signal":"wbArb.io.out.bits.tag","visibility":"direct_frontier"},{"id":"io.out.bits.voluntary","parent_frontier_signal":"wbArb.io.out.bits.voluntary","visibility":"direct_frontier"},{"id":"io.out.bits.way_en","parent_frontier_signal":"wbArb.io.out.bits.way_en","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache.wbArb","task_id":"leaf_abstraction-BoomNonBlockingDCache.wbArb-351ef42d13b9ab57","trust":{"frozen_sha256":"e96cd8303b8b9716a519e7984d435c898c7581aed9c09828b32aca31608e2c79","instance_reuse":{"implementation_sha256":"0f59a94237789b8c52672b24cd281683bc72772359de0e04c02b7d9a1c6b7062","kind":"exact-work-unit","module":"Arbiter2_WritebackReq_1","source_module":"Arbiter2_WritebackReq_1","source_work_unit_id":"BoomNonBlockingDCache.wbArb","structural_implementation_sha256":"6761f40baa091fa90e386915c5aed710d78c4db5f10c2686708f7846ed655000","target_work_unit_id":"BoomNonBlockingDCache.wbArb","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":16},"trusted_axioms":[{"formal":{"parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache.wbArb::A1","rendered_formula":"OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})"},{"formal":{"occurrence":"Input1Fire","predicate":"Input0Valid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache.wbArb::A2","rendered_formula":"Input0Valid => !Input1Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"op":"const","value":0},"target":"io.chosen","type":"signal_equality"},"id":"A3","qualified_id":"BoomNonBlockingDCache.wbArb::A3","rendered_formula":"io.chosen = 0 on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.tag","op":"signal"},"target":"io.out.bits.tag","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache.wbArb::A4","rendered_formula":"io.out.bits.tag = io.in[0].bits.tag on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.idx","op":"signal"},"target":"io.out.bits.idx","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache.wbArb::A5","rendered_formula":"io.out.bits.idx = io.in[0].bits.idx on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.source","op":"signal"},"target":"io.out.bits.source","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache.wbArb::A6","rendered_formula":"io.out.bits.source = io.in[0].bits.source on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.param","op":"signal"},"target":"io.out.bits.param","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache.wbArb::A7","rendered_formula":"io.out.bits.param = io.in[0].bits.param on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache.wbArb::A8","rendered_formula":"io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire"},{"formal":{"on":"Input0Fire","scope_identity":null,"source":{"name":"io.in[0].bits.voluntary","op":"signal"},"target":"io.out.bits.voluntary","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache.wbArb::A9","rendered_formula":"io.out.bits.voluntary = io.in[0].bits.voluntary on Input0Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"op":"const","value":1},"target":"io.chosen","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache.wbArb::A10","rendered_formula":"io.chosen = 1 on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.tag","op":"signal"},"target":"io.out.bits.tag","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache.wbArb::A11","rendered_formula":"io.out.bits.tag = io.in[1].bits.tag on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.idx","op":"signal"},"target":"io.out.bits.idx","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache.wbArb::A12","rendered_formula":"io.out.bits.idx = io.in[1].bits.idx on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.source","op":"signal"},"target":"io.out.bits.source","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache.wbArb::A13","rendered_formula":"io.out.bits.source = io.in[1].bits.source on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.param","op":"signal"},"target":"io.out.bits.param","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache.wbArb::A14","rendered_formula":"io.out.bits.param = io.in[1].bits.param on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.way_en","op":"signal"},"target":"io.out.bits.way_en","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache.wbArb::A15","rendered_formula":"io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire"},{"formal":{"on":"Input1Fire","scope_identity":null,"source":{"name":"io.in[1].bits.voluntary","op":"signal"},"target":"io.out.bits.voluntary","type":"signal_equality"},"id":"A16","qualified_id":"BoomNonBlockingDCache.wbArb::A16","rendered_formula":"io.out.bits.voluntary = io.in[1].bits.voluntary on Input1Fire"}]}
```

### Child `BoomNonBlockingDCache::region-0-0`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache::auto.out.b.fire"],"child_id":"BoomNonBlockingDCache::region-0-0","exported_ids":{"axioms":["BoomNonBlockingDCache::region-0-0::A1"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache::region-0-0::ProbeFire"],"predicates":["BoomNonBlockingDCache::region-0-0::LRSCValid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":[],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"auto.out.b.valid && auto.out.b.ready; an accepted incoming TileLink B probe","id":"ProbeFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::auto.out.b.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-0::ProbeFire"}],"predicates":[{"definition":"lrsc_valid is asserted","id":"LRSCValid","qualified_id":"BoomNonBlockingDCache::region-0-0::LRSCValid"}]},"semantic_signals":[],"summary_ref":"umcm://BoomNonBlockingDCache::region-0-0","task_id":"leaf_abstraction-BoomNonBlockingDCache-region-0-0-f5fc51c32c6c6ed8","trust":{"frozen_sha256":"9cdbc62f6095c3802a56764179b8069f5f24f05d51520d8e6c801b402fe95074","instance_reuse":{"implementation_sha256":"450c3ddf40b1e7f97ef584c5e62da4490be4ee148a86d8a0658f0617fc52eb77","kind":"exact-work-unit","module":"BoomNonBlockingDCache","source_module":"BoomNonBlockingDCache","source_work_unit_id":"BoomNonBlockingDCache::region-0-0","structural_implementation_sha256":null,"target_work_unit_id":"BoomNonBlockingDCache::region-0-0","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":1},"trusted_axioms":[{"formal":{"occurrence":"ProbeFire","predicate":"LRSCValid","scope_identity":null,"type":"forbid_when"},"id":"A1","qualified_id":"BoomNonBlockingDCache::region-0-0::A1","rendered_formula":"LRSCValid => !ProbeFire"}]}
```

### Child `BoomNonBlockingDCache::region-0-1`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache::auto.out.c.fire"],"child_id":"BoomNonBlockingDCache::region-0-1","exported_ids":{"axioms":["BoomNonBlockingDCache::region-0-1::A1","BoomNonBlockingDCache::region-0-1::A10","BoomNonBlockingDCache::region-0-1::A11","BoomNonBlockingDCache::region-0-1::A12","BoomNonBlockingDCache::region-0-1::A13","BoomNonBlockingDCache::region-0-1::A14","BoomNonBlockingDCache::region-0-1::A15","BoomNonBlockingDCache::region-0-1::A16","BoomNonBlockingDCache::region-0-1::A17","BoomNonBlockingDCache::region-0-1::A18","BoomNonBlockingDCache::region-0-1::A19","BoomNonBlockingDCache::region-0-1::A2","BoomNonBlockingDCache::region-0-1::A20","BoomNonBlockingDCache::region-0-1::A21","BoomNonBlockingDCache::region-0-1::A22","BoomNonBlockingDCache::region-0-1::A23","BoomNonBlockingDCache::region-0-1::A24","BoomNonBlockingDCache::region-0-1::A25","BoomNonBlockingDCache::region-0-1::A26","BoomNonBlockingDCache::region-0-1::A27","BoomNonBlockingDCache::region-0-1::A28","BoomNonBlockingDCache::region-0-1::A29","BoomNonBlockingDCache::region-0-1::A3","BoomNonBlockingDCache::region-0-1::A30","BoomNonBlockingDCache::region-0-1::A31","BoomNonBlockingDCache::region-0-1::A32","BoomNonBlockingDCache::region-0-1::A4","BoomNonBlockingDCache::region-0-1::A5","BoomNonBlockingDCache::region-0-1::A6","BoomNonBlockingDCache::region-0-1::A7","BoomNonBlockingDCache::region-0-1::A8","BoomNonBlockingDCache::region-0-1::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache::region-0-1::OutputCFire","BoomNonBlockingDCache::region-0-1::ProbeContinuationBeat","BoomNonBlockingDCache::region-0-1::ProbeStartBeat","BoomNonBlockingDCache::region-0-1::WBContinuationBeat","BoomNonBlockingDCache::region-0-1::WBStartBeat"],"predicates":["BoomNonBlockingDCache::region-0-1::WBReleaseValid"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["nodeOut.c.bits.address","nodeOut.c.bits.corrupt","nodeOut.c.bits.data","nodeOut.c.bits.opcode","nodeOut.c.bits.param","nodeOut.c.bits.size","nodeOut.c.bits.source","prober.io.rep.bits.address","prober.io.rep.bits.corrupt","prober.io.rep.bits.data","prober.io.rep.bits.opcode","prober.io.rep.bits.param","prober.io.rep.bits.size","prober.io.rep.bits.source","wb.io.release.bits.address","wb.io.release.bits.corrupt","wb.io.release.bits.data","wb.io.release.bits.opcode","wb.io.release.bits.param","wb.io.release.bits.size","wb.io.release.bits.source"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"auto.out.c.valid && auto.out.c.ready; one accepted TileLink C output beat","id":"OutputCFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::auto.out.c.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-1::OutputCFire"},{"definition":"nodeOut.c.fire && !idle && state[1]; an accepted continuation beat while the multibeat arbiter is locked to probe reply","id":"ProbeContinuationBeat","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-1::ProbeContinuationBeat"},{"definition":"nodeOut.c.fire && idle && winner[1]; first/only accepted beat of a probe-reply transaction","id":"ProbeStartBeat","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-1::ProbeStartBeat"},{"definition":"nodeOut.c.fire && !idle && state[0]; an accepted continuation beat while the multibeat arbiter is locked to writeback release","id":"WBContinuationBeat","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-1::WBContinuationBeat"},{"definition":"nodeOut.c.fire && idle && winner[0]; first/only accepted beat of a writeback-release transaction","id":"WBStartBeat","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-1::WBStartBeat"}],"predicates":[{"definition":"wb.io.release.valid","id":"WBReleaseValid","qualified_id":"BoomNonBlockingDCache::region-0-1::WBReleaseValid"}]},"semantic_signals":[{"id":"nodeOut.c.bits.address","parent_frontier_signal":"nodeOut.c.bits.address","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.corrupt","parent_frontier_signal":"nodeOut.c.bits.corrupt","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.data","parent_frontier_signal":"nodeOut.c.bits.data","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.opcode","parent_frontier_signal":"nodeOut.c.bits.opcode","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.param","parent_frontier_signal":"nodeOut.c.bits.param","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.size","parent_frontier_signal":"nodeOut.c.bits.size","visibility":"direct_frontier"},{"id":"nodeOut.c.bits.source","parent_frontier_signal":"nodeOut.c.bits.source","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.address","parent_frontier_signal":"prober.io.rep.bits.address","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.corrupt","parent_frontier_signal":"prober.io.rep.bits.corrupt","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.data","parent_frontier_signal":"prober.io.rep.bits.data","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.opcode","parent_frontier_signal":"prober.io.rep.bits.opcode","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.param","parent_frontier_signal":"prober.io.rep.bits.param","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.size","parent_frontier_signal":"prober.io.rep.bits.size","visibility":"direct_frontier"},{"id":"prober.io.rep.bits.source","parent_frontier_signal":"prober.io.rep.bits.source","visibility":"direct_frontier"},{"id":"wb.io.release.bits.address","parent_frontier_signal":"wb.io.release.bits.address","visibility":"direct_frontier"},{"id":"wb.io.release.bits.corrupt","parent_frontier_signal":"wb.io.release.bits.corrupt","visibility":"direct_frontier"},{"id":"wb.io.release.bits.data","parent_frontier_signal":"wb.io.release.bits.data","visibility":"direct_frontier"},{"id":"wb.io.release.bits.opcode","parent_frontier_signal":"wb.io.release.bits.opcode","visibility":"direct_frontier"},{"id":"wb.io.release.bits.param","parent_frontier_signal":"wb.io.release.bits.param","visibility":"direct_frontier"},{"id":"wb.io.release.bits.size","parent_frontier_signal":"wb.io.release.bits.size","visibility":"direct_frontier"},{"id":"wb.io.release.bits.source","parent_frontier_signal":"wb.io.release.bits.source","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache::region-0-1","task_id":"leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8","trust":{"frozen_sha256":"3b11ea9f6bdc0950ce42a75cc15252c184ec9a2c68bdecf32334c5d8b4c5a32e","instance_reuse":{"implementation_sha256":"0177a81ed0b02d30c2b82b9d65a7361976230a28ec60095f73111422978dd413","kind":"exact-work-unit","module":"BoomNonBlockingDCache","source_module":"BoomNonBlockingDCache","source_work_unit_id":"BoomNonBlockingDCache::region-0-1","structural_implementation_sha256":null,"target_work_unit_id":"BoomNonBlockingDCache::region-0-1","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":32},"trusted_axioms":[{"formal":{"parts":["WBStartBeat","ProbeStartBeat","WBContinuationBeat","ProbeContinuationBeat"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"OutputCFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache::region-0-1::A1","rendered_formula":"OutputCFire <=> exactly_one_same_cycle({WBStartBeat, ProbeStartBeat, WBContinuationBeat, ProbeContinuationBeat})"},{"formal":{"occurrence":"ProbeStartBeat","predicate":"WBReleaseValid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache::region-0-1::A2","rendered_formula":"WBReleaseValid => !ProbeStartBeat"},{"formal":{"after":"WBContinuationBeat","before":"WBStartBeat","required_prior":null,"scope_identity":null,"type":"ordered_before"},"id":"A3","qualified_id":"BoomNonBlockingDCache::region-0-1::A3","rendered_formula":"WBStartBeat <mu WBContinuationBeat"},{"formal":{"after":"ProbeContinuationBeat","before":"ProbeStartBeat","required_prior":null,"scope_identity":null,"type":"ordered_before"},"id":"A4","qualified_id":"BoomNonBlockingDCache::region-0-1::A4","rendered_formula":"ProbeStartBeat <mu ProbeContinuationBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.address","op":"signal"},"target":"nodeOut.c.bits.address","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache::region-0-1::A5","rendered_formula":"nodeOut.c.bits.address = wb.io.release.bits.address on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.source","op":"signal"},"target":"nodeOut.c.bits.source","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache::region-0-1::A6","rendered_formula":"nodeOut.c.bits.source = wb.io.release.bits.source on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.size","op":"signal"},"target":"nodeOut.c.bits.size","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache::region-0-1::A7","rendered_formula":"nodeOut.c.bits.size = wb.io.release.bits.size on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.param","op":"signal"},"target":"nodeOut.c.bits.param","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache::region-0-1::A8","rendered_formula":"nodeOut.c.bits.param = wb.io.release.bits.param on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.opcode","op":"signal"},"target":"nodeOut.c.bits.opcode","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache::region-0-1::A9","rendered_formula":"nodeOut.c.bits.opcode = wb.io.release.bits.opcode on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.data","op":"signal"},"target":"nodeOut.c.bits.data","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache::region-0-1::A10","rendered_formula":"nodeOut.c.bits.data = wb.io.release.bits.data on WBStartBeat"},{"formal":{"on":"WBStartBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.corrupt","op":"signal"},"target":"nodeOut.c.bits.corrupt","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache::region-0-1::A11","rendered_formula":"nodeOut.c.bits.corrupt = wb.io.release.bits.corrupt on WBStartBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.address","op":"signal"},"target":"nodeOut.c.bits.address","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache::region-0-1::A12","rendered_formula":"nodeOut.c.bits.address = wb.io.release.bits.address on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.source","op":"signal"},"target":"nodeOut.c.bits.source","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache::region-0-1::A13","rendered_formula":"nodeOut.c.bits.source = wb.io.release.bits.source on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.size","op":"signal"},"target":"nodeOut.c.bits.size","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache::region-0-1::A14","rendered_formula":"nodeOut.c.bits.size = wb.io.release.bits.size on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.param","op":"signal"},"target":"nodeOut.c.bits.param","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache::region-0-1::A15","rendered_formula":"nodeOut.c.bits.param = wb.io.release.bits.param on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.opcode","op":"signal"},"target":"nodeOut.c.bits.opcode","type":"signal_equality"},"id":"A16","qualified_id":"BoomNonBlockingDCache::region-0-1::A16","rendered_formula":"nodeOut.c.bits.opcode = wb.io.release.bits.opcode on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.data","op":"signal"},"target":"nodeOut.c.bits.data","type":"signal_equality"},"id":"A17","qualified_id":"BoomNonBlockingDCache::region-0-1::A17","rendered_formula":"nodeOut.c.bits.data = wb.io.release.bits.data on WBContinuationBeat"},{"formal":{"on":"WBContinuationBeat","scope_identity":null,"source":{"name":"wb.io.release.bits.corrupt","op":"signal"},"target":"nodeOut.c.bits.corrupt","type":"signal_equality"},"id":"A18","qualified_id":"BoomNonBlockingDCache::region-0-1::A18","rendered_formula":"nodeOut.c.bits.corrupt = wb.io.release.bits.corrupt on WBContinuationBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.address","op":"signal"},"target":"nodeOut.c.bits.address","type":"signal_equality"},"id":"A19","qualified_id":"BoomNonBlockingDCache::region-0-1::A19","rendered_formula":"nodeOut.c.bits.address = prober.io.rep.bits.address on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.source","op":"signal"},"target":"nodeOut.c.bits.source","type":"signal_equality"},"id":"A20","qualified_id":"BoomNonBlockingDCache::region-0-1::A20","rendered_formula":"nodeOut.c.bits.source = prober.io.rep.bits.source on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.size","op":"signal"},"target":"nodeOut.c.bits.size","type":"signal_equality"},"id":"A21","qualified_id":"BoomNonBlockingDCache::region-0-1::A21","rendered_formula":"nodeOut.c.bits.size = prober.io.rep.bits.size on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.param","op":"signal"},"target":"nodeOut.c.bits.param","type":"signal_equality"},"id":"A22","qualified_id":"BoomNonBlockingDCache::region-0-1::A22","rendered_formula":"nodeOut.c.bits.param = prober.io.rep.bits.param on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.opcode","op":"signal"},"target":"nodeOut.c.bits.opcode","type":"signal_equality"},"id":"A23","qualified_id":"BoomNonBlockingDCache::region-0-1::A23","rendered_formula":"nodeOut.c.bits.opcode = prober.io.rep.bits.opcode on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.data","op":"signal"},"target":"nodeOut.c.bits.data","type":"signal_equality"},"id":"A24","qualified_id":"BoomNonBlockingDCache::region-0-1::A24","rendered_formula":"nodeOut.c.bits.data = prober.io.rep.bits.data on ProbeStartBeat"},{"formal":{"on":"ProbeStartBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.corrupt","op":"signal"},"target":"nodeOut.c.bits.corrupt","type":"signal_equality"},"id":"A25","qualified_id":"BoomNonBlockingDCache::region-0-1::A25","rendered_formula":"nodeOut.c.bits.corrupt = prober.io.rep.bits.corrupt on ProbeStartBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.address","op":"signal"},"target":"nodeOut.c.bits.address","type":"signal_equality"},"id":"A26","qualified_id":"BoomNonBlockingDCache::region-0-1::A26","rendered_formula":"nodeOut.c.bits.address = prober.io.rep.bits.address on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.source","op":"signal"},"target":"nodeOut.c.bits.source","type":"signal_equality"},"id":"A27","qualified_id":"BoomNonBlockingDCache::region-0-1::A27","rendered_formula":"nodeOut.c.bits.source = prober.io.rep.bits.source on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.size","op":"signal"},"target":"nodeOut.c.bits.size","type":"signal_equality"},"id":"A28","qualified_id":"BoomNonBlockingDCache::region-0-1::A28","rendered_formula":"nodeOut.c.bits.size = prober.io.rep.bits.size on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.param","op":"signal"},"target":"nodeOut.c.bits.param","type":"signal_equality"},"id":"A29","qualified_id":"BoomNonBlockingDCache::region-0-1::A29","rendered_formula":"nodeOut.c.bits.param = prober.io.rep.bits.param on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.opcode","op":"signal"},"target":"nodeOut.c.bits.opcode","type":"signal_equality"},"id":"A30","qualified_id":"BoomNonBlockingDCache::region-0-1::A30","rendered_formula":"nodeOut.c.bits.opcode = prober.io.rep.bits.opcode on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.data","op":"signal"},"target":"nodeOut.c.bits.data","type":"signal_equality"},"id":"A31","qualified_id":"BoomNonBlockingDCache::region-0-1::A31","rendered_formula":"nodeOut.c.bits.data = prober.io.rep.bits.data on ProbeContinuationBeat"},{"formal":{"on":"ProbeContinuationBeat","scope_identity":null,"source":{"name":"prober.io.rep.bits.corrupt","op":"signal"},"target":"nodeOut.c.bits.corrupt","type":"signal_equality"},"id":"A32","qualified_id":"BoomNonBlockingDCache::region-0-1::A32","rendered_formula":"nodeOut.c.bits.corrupt = prober.io.rep.bits.corrupt on ProbeContinuationBeat"}]}
```

### Child `BoomNonBlockingDCache::region-0-2`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache::auto.out.d.fire"],"child_id":"BoomNonBlockingDCache::region-0-2","exported_ids":{"axioms":["BoomNonBlockingDCache::region-0-2::A1","BoomNonBlockingDCache::region-0-2::A10","BoomNonBlockingDCache::region-0-2::A11","BoomNonBlockingDCache::region-0-2::A2","BoomNonBlockingDCache::region-0-2::A3","BoomNonBlockingDCache::region-0-2::A4","BoomNonBlockingDCache::region-0-2::A5","BoomNonBlockingDCache::region-0-2::A6","BoomNonBlockingDCache::region-0-2::A7","BoomNonBlockingDCache::region-0-2::A8","BoomNonBlockingDCache::region-0-2::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache::region-0-2::DFire","BoomNonBlockingDCache::region-0-2::MSHRGrantFire","BoomNonBlockingDCache::region-0-2::ReleaseAckFire"],"predicates":["BoomNonBlockingDCache::region-0-2::NonReleaseAckSource","BoomNonBlockingDCache::region-0-2::ReleaseAckSource"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["mshrs.io.mem_grant.bits.corrupt","mshrs.io.mem_grant.bits.data","mshrs.io.mem_grant.bits.denied","mshrs.io.mem_grant.bits.opcode","mshrs.io.mem_grant.bits.param","mshrs.io.mem_grant.bits.sink","mshrs.io.mem_grant.bits.size","mshrs.io.mem_grant.bits.source","nodeOut.d.bits.source"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"auto.out.d.valid && auto.out.d.ready; one accepted incoming TileLink D beat","id":"DFire","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::auto.out.d.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-2::DFire"},{"definition":"DFire with nodeOut.d.bits.source != 2; this accepted D beat is forwarded through mshrs.io.mem_grant","id":"MSHRGrantFire","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::auto.out.d.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-2::MSHRGrantFire"},{"definition":"DFire with nodeOut.d.bits.source == 2; this D beat follows the local ReleaseAck path","id":"ReleaseAckFire","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::auto.out.d.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-2::ReleaseAckFire"}],"predicates":[{"definition":"nodeOut.d.bits.source != 2","id":"NonReleaseAckSource","qualified_id":"BoomNonBlockingDCache::region-0-2::NonReleaseAckSource"},{"definition":"nodeOut.d.bits.source == 2","id":"ReleaseAckSource","qualified_id":"BoomNonBlockingDCache::region-0-2::ReleaseAckSource"}]},"semantic_signals":[{"id":"mshrs.io.mem_grant.bits.corrupt","parent_frontier_signal":"mshrs.io.mem_grant.bits.corrupt","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.data","parent_frontier_signal":"mshrs.io.mem_grant.bits.data","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.denied","parent_frontier_signal":"mshrs.io.mem_grant.bits.denied","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.opcode","parent_frontier_signal":"mshrs.io.mem_grant.bits.opcode","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.param","parent_frontier_signal":"mshrs.io.mem_grant.bits.param","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.sink","parent_frontier_signal":"mshrs.io.mem_grant.bits.sink","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.size","parent_frontier_signal":"mshrs.io.mem_grant.bits.size","visibility":"direct_frontier"},{"id":"mshrs.io.mem_grant.bits.source","parent_frontier_signal":"mshrs.io.mem_grant.bits.source","visibility":"direct_frontier"},{"id":"nodeOut.d.bits.corrupt","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.data","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.denied","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.opcode","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.param","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.sink","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.size","visibility":"opaque_child_signal"},{"id":"nodeOut.d.bits.source","parent_frontier_signal":"nodeOut.d.bits.source","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache::region-0-2","task_id":"leaf_abstraction-BoomNonBlockingDCache-region-0-2-05c1013f696ad6ab","trust":{"frozen_sha256":"69ea55e98f4ea1f86d7dcb708afb63a5b5159989beedb9eaf3fd5c7217e237d3","instance_reuse":{"implementation_sha256":"040ef786a4af559ca3e43d7604266b8c2c0c039ef24e77d7450a87586adc1791","kind":"exact-work-unit","module":"BoomNonBlockingDCache","source_module":"BoomNonBlockingDCache","source_work_unit_id":"BoomNonBlockingDCache::region-0-2","structural_implementation_sha256":null,"target_work_unit_id":"BoomNonBlockingDCache::region-0-2","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":11},"trusted_axioms":[{"formal":{"parts":["ReleaseAckFire","MSHRGrantFire"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"DFire"},"id":"A1","qualified_id":"BoomNonBlockingDCache::region-0-2::A1","rendered_formula":"DFire <=> exactly_one_same_cycle({ReleaseAckFire, MSHRGrantFire})"},{"formal":{"occurrence":"ReleaseAckFire","predicate":"NonReleaseAckSource","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache::region-0-2::A2","rendered_formula":"NonReleaseAckSource => !ReleaseAckFire"},{"formal":{"occurrence":"MSHRGrantFire","predicate":"ReleaseAckSource","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache::region-0-2::A3","rendered_formula":"ReleaseAckSource => !MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.opcode","op":"signal"},"target":"mshrs.io.mem_grant.bits.opcode","type":"signal_equality"},"id":"A4","qualified_id":"BoomNonBlockingDCache::region-0-2::A4","rendered_formula":"mshrs.io.mem_grant.bits.opcode = nodeOut.d.bits.opcode on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.param","op":"signal"},"target":"mshrs.io.mem_grant.bits.param","type":"signal_equality"},"id":"A5","qualified_id":"BoomNonBlockingDCache::region-0-2::A5","rendered_formula":"mshrs.io.mem_grant.bits.param = nodeOut.d.bits.param on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.size","op":"signal"},"target":"mshrs.io.mem_grant.bits.size","type":"signal_equality"},"id":"A6","qualified_id":"BoomNonBlockingDCache::region-0-2::A6","rendered_formula":"mshrs.io.mem_grant.bits.size = nodeOut.d.bits.size on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.source","op":"signal"},"target":"mshrs.io.mem_grant.bits.source","type":"signal_equality"},"id":"A7","qualified_id":"BoomNonBlockingDCache::region-0-2::A7","rendered_formula":"mshrs.io.mem_grant.bits.source = nodeOut.d.bits.source on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.sink","op":"signal"},"target":"mshrs.io.mem_grant.bits.sink","type":"signal_equality"},"id":"A8","qualified_id":"BoomNonBlockingDCache::region-0-2::A8","rendered_formula":"mshrs.io.mem_grant.bits.sink = nodeOut.d.bits.sink on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.denied","op":"signal"},"target":"mshrs.io.mem_grant.bits.denied","type":"signal_equality"},"id":"A9","qualified_id":"BoomNonBlockingDCache::region-0-2::A9","rendered_formula":"mshrs.io.mem_grant.bits.denied = nodeOut.d.bits.denied on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.data","op":"signal"},"target":"mshrs.io.mem_grant.bits.data","type":"signal_equality"},"id":"A10","qualified_id":"BoomNonBlockingDCache::region-0-2::A10","rendered_formula":"mshrs.io.mem_grant.bits.data = nodeOut.d.bits.data on MSHRGrantFire"},{"formal":{"on":"MSHRGrantFire","scope_identity":null,"source":{"name":"nodeOut.d.bits.corrupt","op":"signal"},"target":"mshrs.io.mem_grant.bits.corrupt","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache::region-0-2::A11","rendered_formula":"mshrs.io.mem_grant.bits.corrupt = nodeOut.d.bits.corrupt on MSHRGrantFire"}]}
```

### Child `BoomNonBlockingDCache::region-0-3`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache::io.lsu.nack[0].valid","BoomNonBlockingDCache::io.lsu.resp[0].valid","BoomNonBlockingDCache::io.lsu.store_ack[0].valid"],"child_id":"BoomNonBlockingDCache::region-0-3","exported_ids":{"axioms":["BoomNonBlockingDCache::region-0-3::A1","BoomNonBlockingDCache::region-0-3::A10","BoomNonBlockingDCache::region-0-3::A11","BoomNonBlockingDCache::region-0-3::A12","BoomNonBlockingDCache::region-0-3::A13","BoomNonBlockingDCache::region-0-3::A14","BoomNonBlockingDCache::region-0-3::A15","BoomNonBlockingDCache::region-0-3::A16","BoomNonBlockingDCache::region-0-3::A17","BoomNonBlockingDCache::region-0-3::A18","BoomNonBlockingDCache::region-0-3::A19","BoomNonBlockingDCache::region-0-3::A2","BoomNonBlockingDCache::region-0-3::A20","BoomNonBlockingDCache::region-0-3::A21","BoomNonBlockingDCache::region-0-3::A22","BoomNonBlockingDCache::region-0-3::A23","BoomNonBlockingDCache::region-0-3::A24","BoomNonBlockingDCache::region-0-3::A25","BoomNonBlockingDCache::region-0-3::A26","BoomNonBlockingDCache::region-0-3::A27","BoomNonBlockingDCache::region-0-3::A28","BoomNonBlockingDCache::region-0-3::A29","BoomNonBlockingDCache::region-0-3::A3","BoomNonBlockingDCache::region-0-3::A30","BoomNonBlockingDCache::region-0-3::A4","BoomNonBlockingDCache::region-0-3::A5","BoomNonBlockingDCache::region-0-3::A6","BoomNonBlockingDCache::region-0-3::A7","BoomNonBlockingDCache::region-0-3::A8","BoomNonBlockingDCache::region-0-3::A9"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache::region-0-3::HitStoreAck","BoomNonBlockingDCache::region-0-3::MSHRReqFire","BoomNonBlockingDCache::region-0-3::MissAllocatedStoreAck","BoomNonBlockingDCache::region-0-3::NackValid","BoomNonBlockingDCache::region-0-3::RespFromArray","BoomNonBlockingDCache::region-0-3::RespFromS3","BoomNonBlockingDCache::region-0-3::RespFromS4","BoomNonBlockingDCache::region-0-3::RespFromS5","BoomNonBlockingDCache::region-0-3::RespValid","BoomNonBlockingDCache::region-0-3::SCResponse","BoomNonBlockingDCache::region-0-3::StoreAckValid"],"predicates":["BoomNonBlockingDCache::region-0-3::S2Hit","BoomNonBlockingDCache::region-0-3::S2Invalid","BoomNonBlockingDCache::region-0-3::S2Miss","BoomNonBlockingDCache::region-0-3::S2Nack","BoomNonBlockingDCache::region-0-3::S2NoNack"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":["io.lsu.nack[0].bits.addr","io.lsu.nack[0].bits.data","io.lsu.nack[0].bits.uop.ldq_idx","io.lsu.nack[0].bits.uop.mem_cmd","io.lsu.nack[0].bits.uop.rob_idx","io.lsu.nack[0].bits.uop.stq_idx","io.lsu.resp[0].bits.data","io.lsu.resp[0].bits.uop.ldq_idx","io.lsu.resp[0].bits.uop.mem_cmd","io.lsu.resp[0].bits.uop.mem_size","io.lsu.resp[0].bits.uop.rob_idx","io.lsu.resp[0].bits.uop.stq_idx","io.lsu.store_ack[0].bits.addr","io.lsu.store_ack[0].bits.uop.mem_cmd","io.lsu.store_ack[0].bits.uop.rob_idx","io.lsu.store_ack[0].bits.uop.stq_idx","s2_data_word[0]","s2_req[0].addr","s2_req[0].data","s2_req[0].uop.ldq_idx","s2_req[0].uop.mem_cmd","s2_req[0].uop.mem_size","s2_req[0].uop.rob_idx","s2_req[0].uop.stq_idx","s2_sc_fail","s3_req.data","s4_req.data","s5_req.data"],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.lsu.store_ack[0].valid && s2_hit[0]","id":"HitStoreAck","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::HitStoreAck"},{"definition":"mshrs.io.req[0].valid && mshrs.io.req[0].ready","id":"MSHRReqFire","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::MSHRReqFire"},{"definition":"io.lsu.store_ack[0].valid && !s2_hit[0] && mshrs.io.req[0].valid && mshrs.io.req[0].ready","id":"MissAllocatedStoreAck","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::MissAllocatedStoreAck"},{"definition":"io.lsu.nack[0].valid","id":"NackValid","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::io.lsu.nack[0].valid"],"qualified_id":"BoomNonBlockingDCache::region-0-3::NackValid"},{"definition":"io.lsu.resp[0].valid && !s3_bypass[0] && !s4_bypass[0] && !s5_bypass[0]","id":"RespFromArray","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::RespFromArray"},{"definition":"io.lsu.resp[0].valid && s3_bypass[0]","id":"RespFromS3","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::RespFromS3"},{"definition":"io.lsu.resp[0].valid && !s3_bypass[0] && s4_bypass[0]","id":"RespFromS4","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::RespFromS4"},{"definition":"io.lsu.resp[0].valid && !s3_bypass[0] && !s4_bypass[0] && s5_bypass[0]","id":"RespFromS5","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::RespFromS5"},{"definition":"io.lsu.resp[0].valid","id":"RespValid","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::io.lsu.resp[0].valid"],"qualified_id":"BoomNonBlockingDCache::region-0-3::RespValid"},{"definition":"io.lsu.resp[0].valid && s2_sc","id":"SCResponse","index":null,"kind":"derived","multiplicity":"repeatable","physical_event_ids":[],"qualified_id":"BoomNonBlockingDCache::region-0-3::SCResponse"},{"definition":"io.lsu.store_ack[0].valid","id":"StoreAckValid","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::io.lsu.store_ack[0].valid"],"qualified_id":"BoomNonBlockingDCache::region-0-3::StoreAckValid"}],"predicates":[{"definition":"s2_hit[0]","id":"S2Hit","qualified_id":"BoomNonBlockingDCache::region-0-3::S2Hit"},{"definition":"!s2_valid[0]","id":"S2Invalid","qualified_id":"BoomNonBlockingDCache::region-0-3::S2Invalid"},{"definition":"!s2_hit[0]","id":"S2Miss","qualified_id":"BoomNonBlockingDCache::region-0-3::S2Miss"},{"definition":"s2_nack[0]","id":"S2Nack","qualified_id":"BoomNonBlockingDCache::region-0-3::S2Nack"},{"definition":"!s2_nack[0]","id":"S2NoNack","qualified_id":"BoomNonBlockingDCache::region-0-3::S2NoNack"}]},"semantic_signals":[{"id":"io.lsu.nack[0].bits.addr","parent_frontier_signal":"io.lsu.nack[0].bits.addr","visibility":"direct_frontier"},{"id":"io.lsu.nack[0].bits.data","parent_frontier_signal":"io.lsu.nack[0].bits.data","visibility":"direct_frontier"},{"id":"io.lsu.nack[0].bits.uop.ldq_idx","parent_frontier_signal":"io.lsu.nack[0].bits.uop.ldq_idx","visibility":"direct_frontier"},{"id":"io.lsu.nack[0].bits.uop.mem_cmd","parent_frontier_signal":"io.lsu.nack[0].bits.uop.mem_cmd","visibility":"direct_frontier"},{"id":"io.lsu.nack[0].bits.uop.rob_idx","parent_frontier_signal":"io.lsu.nack[0].bits.uop.rob_idx","visibility":"direct_frontier"},{"id":"io.lsu.nack[0].bits.uop.stq_idx","parent_frontier_signal":"io.lsu.nack[0].bits.uop.stq_idx","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.data","parent_frontier_signal":"io.lsu.resp[0].bits.data","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.uop.ldq_idx","parent_frontier_signal":"io.lsu.resp[0].bits.uop.ldq_idx","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.uop.mem_cmd","parent_frontier_signal":"io.lsu.resp[0].bits.uop.mem_cmd","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.uop.mem_size","parent_frontier_signal":"io.lsu.resp[0].bits.uop.mem_size","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.uop.rob_idx","parent_frontier_signal":"io.lsu.resp[0].bits.uop.rob_idx","visibility":"direct_frontier"},{"id":"io.lsu.resp[0].bits.uop.stq_idx","parent_frontier_signal":"io.lsu.resp[0].bits.uop.stq_idx","visibility":"direct_frontier"},{"id":"io.lsu.store_ack[0].bits.addr","parent_frontier_signal":"io.lsu.store_ack[0].bits.addr","visibility":"direct_frontier"},{"id":"io.lsu.store_ack[0].bits.uop.mem_cmd","parent_frontier_signal":"io.lsu.store_ack[0].bits.uop.mem_cmd","visibility":"direct_frontier"},{"id":"io.lsu.store_ack[0].bits.uop.rob_idx","parent_frontier_signal":"io.lsu.store_ack[0].bits.uop.rob_idx","visibility":"direct_frontier"},{"id":"io.lsu.store_ack[0].bits.uop.stq_idx","parent_frontier_signal":"io.lsu.store_ack[0].bits.uop.stq_idx","visibility":"direct_frontier"},{"id":"s2_data_word[0]","parent_frontier_signal":"s2_data_word[0]","visibility":"direct_frontier"},{"id":"s2_data_word_prebypass[0]","visibility":"opaque_child_signal"},{"id":"s2_req[0].addr","parent_frontier_signal":"s2_req[0].addr","visibility":"direct_frontier"},{"id":"s2_req[0].data","parent_frontier_signal":"s2_req[0].data","visibility":"direct_frontier"},{"id":"s2_req[0].uop.ldq_idx","parent_frontier_signal":"s2_req[0].uop.ldq_idx","visibility":"direct_frontier"},{"id":"s2_req[0].uop.mem_cmd","parent_frontier_signal":"s2_req[0].uop.mem_cmd","visibility":"direct_frontier"},{"id":"s2_req[0].uop.mem_size","parent_frontier_signal":"s2_req[0].uop.mem_size","visibility":"direct_frontier"},{"id":"s2_req[0].uop.rob_idx","parent_frontier_signal":"s2_req[0].uop.rob_idx","visibility":"direct_frontier"},{"id":"s2_req[0].uop.stq_idx","parent_frontier_signal":"s2_req[0].uop.stq_idx","visibility":"direct_frontier"},{"id":"s2_sc_fail","parent_frontier_signal":"s2_sc_fail","visibility":"direct_frontier"},{"id":"s3_req.data","parent_frontier_signal":"s3_req.data","visibility":"direct_frontier"},{"id":"s4_req.data","parent_frontier_signal":"s4_req.data","visibility":"direct_frontier"},{"id":"s5_req.data","parent_frontier_signal":"s5_req.data","visibility":"direct_frontier"}],"summary_ref":"umcm://BoomNonBlockingDCache::region-0-3","task_id":"leaf_abstraction-BoomNonBlockingDCache-region-0-3-311dc24763e402d9","trust":{"frozen_sha256":"c03dd7b87e1306b866e203cb234333b78bf3089737226fe99068ba117cb7922b","instance_reuse":{"implementation_sha256":"9a5400d82d787b4fe706495a13dde4f3528095fa96848d79780146a0332fe269","kind":"exact-work-unit","module":"BoomNonBlockingDCache","source_module":"BoomNonBlockingDCache","source_work_unit_id":"BoomNonBlockingDCache::region-0-3","structural_implementation_sha256":null,"target_work_unit_id":"BoomNonBlockingDCache::region-0-3","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":30},"trusted_axioms":[{"formal":{"occurrence":"RespValid","predicate":"S2Invalid","scope_identity":null,"type":"forbid_when"},"id":"A1","qualified_id":"BoomNonBlockingDCache::region-0-3::A1","rendered_formula":"S2Invalid => !RespValid"},{"formal":{"occurrence":"NackValid","predicate":"S2Invalid","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache::region-0-3::A2","rendered_formula":"S2Invalid => !NackValid"},{"formal":{"occurrence":"StoreAckValid","predicate":"S2Invalid","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache::region-0-3::A3","rendered_formula":"S2Invalid => !StoreAckValid"},{"formal":{"occurrence":"MSHRReqFire","predicate":"S2Invalid","scope_identity":null,"type":"forbid_when"},"id":"A4","qualified_id":"BoomNonBlockingDCache::region-0-3::A4","rendered_formula":"S2Invalid => !MSHRReqFire"},{"formal":{"occurrence":"RespValid","predicate":"S2Miss","scope_identity":null,"type":"forbid_when"},"id":"A5","qualified_id":"BoomNonBlockingDCache::region-0-3::A5","rendered_formula":"S2Miss => !RespValid"},{"formal":{"occurrence":"NackValid","predicate":"S2NoNack","scope_identity":null,"type":"forbid_when"},"id":"A6","qualified_id":"BoomNonBlockingDCache::region-0-3::A6","rendered_formula":"S2NoNack => !NackValid"},{"formal":{"occurrence":"StoreAckValid","predicate":"S2Nack","scope_identity":null,"type":"forbid_when"},"id":"A7","qualified_id":"BoomNonBlockingDCache::region-0-3::A7","rendered_formula":"S2Nack => !StoreAckValid"},{"formal":{"occurrence":"MSHRReqFire","predicate":"S2Hit","scope_identity":null,"type":"forbid_when"},"id":"A8","qualified_id":"BoomNonBlockingDCache::region-0-3::A8","rendered_formula":"S2Hit => !MSHRReqFire"},{"formal":{"parts":["HitStoreAck","MissAllocatedStoreAck"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"StoreAckValid"},"id":"A9","qualified_id":"BoomNonBlockingDCache::region-0-3::A9","rendered_formula":"StoreAckValid <=> exactly_one_same_cycle({HitStoreAck, MissAllocatedStoreAck})"},{"formal":{"parts":["RespFromS3","RespFromS4","RespFromS5","RespFromArray"],"relation":"same_cycle_exactly_one","scope_identity":null,"type":"occurrence_partition","whole":"RespValid"},"id":"A10","qualified_id":"BoomNonBlockingDCache::region-0-3::A10","rendered_formula":"RespValid <=> exactly_one_same_cycle({RespFromS3, RespFromS4, RespFromS5, RespFromArray})"},{"formal":{"on":"RespFromS3","scope_identity":null,"source":{"name":"s3_req.data","op":"signal"},"target":"s2_data_word[0]","type":"signal_equality"},"id":"A11","qualified_id":"BoomNonBlockingDCache::region-0-3::A11","rendered_formula":"s2_data_word[0] = s3_req.data on RespFromS3"},{"formal":{"on":"RespFromS4","scope_identity":null,"source":{"name":"s4_req.data","op":"signal"},"target":"s2_data_word[0]","type":"signal_equality"},"id":"A12","qualified_id":"BoomNonBlockingDCache::region-0-3::A12","rendered_formula":"s2_data_word[0] = s4_req.data on RespFromS4"},{"formal":{"on":"RespFromS5","scope_identity":null,"source":{"name":"s5_req.data","op":"signal"},"target":"s2_data_word[0]","type":"signal_equality"},"id":"A13","qualified_id":"BoomNonBlockingDCache::region-0-3::A13","rendered_formula":"s2_data_word[0] = s5_req.data on RespFromS5"},{"formal":{"on":"RespFromArray","scope_identity":null,"source":{"name":"s2_data_word_prebypass[0]","op":"signal"},"target":"s2_data_word[0]","type":"signal_equality"},"id":"A14","qualified_id":"BoomNonBlockingDCache::region-0-3::A14","rendered_formula":"s2_data_word[0] = s2_data_word_prebypass[0] on RespFromArray"},{"formal":{"on":"SCResponse","scope_identity":null,"source":{"name":"s2_sc_fail","op":"signal"},"target":"io.lsu.resp[0].bits.data","type":"signal_equality"},"id":"A15","qualified_id":"BoomNonBlockingDCache::region-0-3::A15","rendered_formula":"io.lsu.resp[0].bits.data = s2_sc_fail on SCResponse"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].addr","op":"signal"},"target":"io.lsu.nack[0].bits.addr","type":"signal_equality"},"id":"A16","qualified_id":"BoomNonBlockingDCache::region-0-3::A16","rendered_formula":"io.lsu.nack[0].bits.addr = s2_req[0].addr on NackValid"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].data","op":"signal"},"target":"io.lsu.nack[0].bits.data","type":"signal_equality"},"id":"A17","qualified_id":"BoomNonBlockingDCache::region-0-3::A17","rendered_formula":"io.lsu.nack[0].bits.data = s2_req[0].data on NackValid"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].uop.mem_cmd","op":"signal"},"target":"io.lsu.nack[0].bits.uop.mem_cmd","type":"signal_equality"},"id":"A18","qualified_id":"BoomNonBlockingDCache::region-0-3::A18","rendered_formula":"io.lsu.nack[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on NackValid"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].uop.rob_idx","op":"signal"},"target":"io.lsu.nack[0].bits.uop.rob_idx","type":"signal_equality"},"id":"A19","qualified_id":"BoomNonBlockingDCache::region-0-3::A19","rendered_formula":"io.lsu.nack[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on NackValid"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].uop.ldq_idx","op":"signal"},"target":"io.lsu.nack[0].bits.uop.ldq_idx","type":"signal_equality"},"id":"A20","qualified_id":"BoomNonBlockingDCache::region-0-3::A20","rendered_formula":"io.lsu.nack[0].bits.uop.ldq_idx = s2_req[0].uop.ldq_idx on NackValid"},{"formal":{"on":"NackValid","scope_identity":null,"source":{"name":"s2_req[0].uop.stq_idx","op":"signal"},"target":"io.lsu.nack[0].bits.uop.stq_idx","type":"signal_equality"},"id":"A21","qualified_id":"BoomNonBlockingDCache::region-0-3::A21","rendered_formula":"io.lsu.nack[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on NackValid"},{"formal":{"on":"StoreAckValid","scope_identity":null,"source":{"name":"s2_req[0].addr","op":"signal"},"target":"io.lsu.store_ack[0].bits.addr","type":"signal_equality"},"id":"A22","qualified_id":"BoomNonBlockingDCache::region-0-3::A22","rendered_formula":"io.lsu.store_ack[0].bits.addr = s2_req[0].addr on StoreAckValid"},{"formal":{"on":"StoreAckValid","scope_identity":null,"source":{"name":"s2_req[0].uop.mem_cmd","op":"signal"},"target":"io.lsu.store_ack[0].bits.uop.mem_cmd","type":"signal_equality"},"id":"A23","qualified_id":"BoomNonBlockingDCache::region-0-3::A23","rendered_formula":"io.lsu.store_ack[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on StoreAckValid"},{"formal":{"on":"StoreAckValid","scope_identity":null,"source":{"name":"s2_req[0].uop.rob_idx","op":"signal"},"target":"io.lsu.store_ack[0].bits.uop.rob_idx","type":"signal_equality"},"id":"A24","qualified_id":"BoomNonBlockingDCache::region-0-3::A24","rendered_formula":"io.lsu.store_ack[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on StoreAckValid"},{"formal":{"on":"StoreAckValid","scope_identity":null,"source":{"name":"s2_req[0].uop.stq_idx","op":"signal"},"target":"io.lsu.store_ack[0].bits.uop.stq_idx","type":"signal_equality"},"id":"A25","qualified_id":"BoomNonBlockingDCache::region-0-3::A25","rendered_formula":"io.lsu.store_ack[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on StoreAckValid"},{"formal":{"on":"RespValid","scope_identity":null,"source":{"name":"s2_req[0].uop.mem_cmd","op":"signal"},"target":"io.lsu.resp[0].bits.uop.mem_cmd","type":"signal_equality"},"id":"A26","qualified_id":"BoomNonBlockingDCache::region-0-3::A26","rendered_formula":"io.lsu.resp[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on RespValid"},{"formal":{"on":"RespValid","scope_identity":null,"source":{"name":"s2_req[0].uop.mem_size","op":"signal"},"target":"io.lsu.resp[0].bits.uop.mem_size","type":"signal_equality"},"id":"A27","qualified_id":"BoomNonBlockingDCache::region-0-3::A27","rendered_formula":"io.lsu.resp[0].bits.uop.mem_size = s2_req[0].uop.mem_size on RespValid"},{"formal":{"on":"RespValid","scope_identity":null,"source":{"name":"s2_req[0].uop.rob_idx","op":"signal"},"target":"io.lsu.resp[0].bits.uop.rob_idx","type":"signal_equality"},"id":"A28","qualified_id":"BoomNonBlockingDCache::region-0-3::A28","rendered_formula":"io.lsu.resp[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on RespValid"},{"formal":{"on":"RespValid","scope_identity":null,"source":{"name":"s2_req[0].uop.ldq_idx","op":"signal"},"target":"io.lsu.resp[0].bits.uop.ldq_idx","type":"signal_equality"},"id":"A29","qualified_id":"BoomNonBlockingDCache::region-0-3::A29","rendered_formula":"io.lsu.resp[0].bits.uop.ldq_idx = s2_req[0].uop.ldq_idx on RespValid"},{"formal":{"on":"RespValid","scope_identity":null,"source":{"name":"s2_req[0].uop.stq_idx","op":"signal"},"target":"io.lsu.resp[0].bits.uop.stq_idx","type":"signal_equality"},"id":"A30","qualified_id":"BoomNonBlockingDCache::region-0-3::A30","rendered_formula":"io.lsu.resp[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on RespValid"}]}
```

### Child `BoomNonBlockingDCache::region-0-4`
This is the complete LLM-visible semantic contract for this child. Opaque imports are typed atoms referenced by a direct trusted theorem; do not infer their hidden definitions or proof history.
```json
{"assumptions":[],"boundary_events":["BoomNonBlockingDCache::io.lsu.req.fire"],"child_id":"BoomNonBlockingDCache::region-0-4","exported_ids":{"axioms":["BoomNonBlockingDCache::region-0-4::A1","BoomNonBlockingDCache::region-0-4::A2","BoomNonBlockingDCache::region-0-4::A3"],"identity_keys":[],"occurrences":["BoomNonBlockingDCache::region-0-4::RequestAccept"],"predicates":["BoomNonBlockingDCache::region-0-4::DataReadUnavailable","BoomNonBlockingDCache::region-0-4::MSHRResponsePending","BoomNonBlockingDCache::region-0-4::MetaReadUnavailable"]},"interface_version":"frozen-child-prompt-interface-v0.1","opaque_imports":[],"relevant_frontier_signals":[],"semantic_objects":{"identity_keys":[],"occurrences":[{"definition":"io.lsu.req.valid && io.lsu.req.ready; one LSU request is accepted by the DCache","id":"RequestAccept","index":null,"kind":"boundary","multiplicity":"repeatable","physical_event_ids":["BoomNonBlockingDCache::io.lsu.req.fire"],"qualified_id":"BoomNonBlockingDCache::region-0-4::RequestAccept"}],"predicates":[{"definition":"!dataReadArb.io.in[2].ready","id":"DataReadUnavailable","qualified_id":"BoomNonBlockingDCache::region-0-4::DataReadUnavailable"},{"definition":"mshrs.io.resp.valid","id":"MSHRResponsePending","qualified_id":"BoomNonBlockingDCache::region-0-4::MSHRResponsePending"},{"definition":"!metaReadArb.io.in[4].ready","id":"MetaReadUnavailable","qualified_id":"BoomNonBlockingDCache::region-0-4::MetaReadUnavailable"}]},"semantic_signals":[],"summary_ref":"umcm://BoomNonBlockingDCache::region-0-4","task_id":"leaf_abstraction-BoomNonBlockingDCache-region-0-4-f13601df6f3c1120","trust":{"frozen_sha256":"2ff1a22d672f9f1f6f6f06609efae7cc5f81f0084c6a34edcffed1b86bb0ef95","instance_reuse":{"implementation_sha256":"248b44ffaba4b60aaefe9784ed8a72cf1a012b073c7873754122d329a81429a0","kind":"exact-work-unit","module":"BoomNonBlockingDCache","source_module":"BoomNonBlockingDCache","source_work_unit_id":"BoomNonBlockingDCache::region-0-4","structural_implementation_sha256":null,"target_work_unit_id":"BoomNonBlockingDCache::region-0-4","verification":"exact-work-unit-id"},"status":"FROZEN_FOR_COMPOSITION","trusted_axiom_count":3},"trusted_axioms":[{"formal":{"occurrence":"RequestAccept","predicate":"MSHRResponsePending","scope_identity":null,"type":"forbid_when"},"id":"A1","qualified_id":"BoomNonBlockingDCache::region-0-4::A1","rendered_formula":"MSHRResponsePending => !RequestAccept"},{"formal":{"occurrence":"RequestAccept","predicate":"MetaReadUnavailable","scope_identity":null,"type":"forbid_when"},"id":"A2","qualified_id":"BoomNonBlockingDCache::region-0-4::A2","rendered_formula":"MetaReadUnavailable => !RequestAccept"},{"formal":{"occurrence":"RequestAccept","predicate":"DataReadUnavailable","scope_identity":null,"type":"forbid_when"},"id":"A3","qualified_id":"BoomNonBlockingDCache::region-0-4::A3","rendered_formula":"DataReadUnavailable => !RequestAccept"}]}
```

## Parent-local source evidence

### generators/boom/src/main/scala/v4/common/consts.scala:140-142
```scala

  def NullMicroOp(implicit p: Parameters) = 0.U.asTypeOf(new boom.v4.common.MicroOp)
}
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:437-439
```scala

class BoomNonBlockingDCacheModule(outer: BoomNonBlockingDCache) extends LazyModuleImp(outer)
  with HasL1HellaCacheParameters
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:443-447
```scala
  val (tl_out, _) = outer.node.out(0)
  val io = IO(new BoomDCacheBundle)

  io.errors := DontCare
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:453-455
```scala

  def widthMap[T <: Data](f: Int => T) = VecInit((0 until lsuWidth).map(f))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:457-466
```scala

  val wb = Module(new BoomWritebackUnit)
  val prober = Module(new BoomProbeUnit)
  val mshrs = Module(new BoomMSHRFile)
  mshrs.io.clear_all    := io.lsu.force_order
  mshrs.io.brupdate       := io.lsu.brupdate
  mshrs.io.exception    := io.lsu.exception
  mshrs.io.rob_pnr_idx  := io.lsu.rob_pnr_idx
  mshrs.io.rob_head_idx := io.lsu.rob_head_idx
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:468-473
```scala
  def onReset = L1Metadata(0.U, ClientMetadata.onReset)
  val meta = Seq.fill(lsuWidth) { Module(new L1MetadataArray(onReset _)) }
  val metaWriteArb = Module(new Arbiter(new L1MetaWriteReq, 2))
  // 0 goes to MSHR refills, 1 goes to prober
  val metaReadArb = Module(new Arbiter(new BoomL1MetaReadReq, 6))
  // 0 goes to MSHR replays, 1 goes to prober, 2 goes to wb, 3 goes to MSHR meta read,
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:475-485
```scala

  metaReadArb.io.in := DontCare
  for (w <- 0 until lsuWidth) {
    meta(w).io.write.valid := metaWriteArb.io.out.fire
    meta(w).io.write.bits  := metaWriteArb.io.out.bits
    meta(w).io.read.valid  := metaReadArb.io.out.valid
    meta(w).io.read.bits   := metaReadArb.io.out.bits.req(w)
  }
  metaReadArb.io.out.ready  := meta.map(_.io.read.ready).reduce(_||_)
  metaWriteArb.io.out.ready := meta.map(_.io.write.ready).reduce(_||_)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:486-493
```scala
  // data
  val data = Module(if (boomParams.numDCacheBanks == 1) new BoomDuplicatedDataArray else new BoomBankedDataArray)
  val dataWriteArb = Module(new Arbiter(new L1DataWriteReq, 2))
  // 0 goes to pipeline, 1 goes to MSHR refills
  val dataReadArb = Module(new Arbiter(new BoomL1DataReadReq, 3))
  // 0 goes to MSHR replays, 1 goes to wb, 2 goes to pipeline
  dataReadArb.io.in := DontCare
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:494-504
```scala
  for (w <- 0 until lsuWidth) {
    data.io.read(w).valid := dataReadArb.io.out.bits.valid(w) && dataReadArb.io.out.valid
    data.io.read(w).bits  := dataReadArb.io.out.bits.req(w)
  }
  dataReadArb.io.out.ready := true.B

  data.io.write.valid := dataWriteArb.io.out.fire
  data.io.write.bits  := dataWriteArb.io.out.bits
  dataWriteArb.io.out.ready := true.B
  val singlePortedDCacheWrite = data.io.write.valid && dcacheSinglePorted.B
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:511-514
```scala
  io.lsu.req.ready := metaReadArb.io.in(4).ready && dataReadArb.io.in(2).ready && !block_incoming_reqs
  metaReadArb.io.in(4).valid := io.lsu.req.valid && !block_incoming_reqs
  dataReadArb.io.in(2).valid := io.lsu.req.valid && !block_incoming_reqs
  for (w <- 0 until lsuWidth) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:515-523
```scala
    // Tag read for new requests
    metaReadArb.io.in(4).bits.req(w).idx    := io.lsu.req.bits(w).bits.addr >> blockOffBits
    metaReadArb.io.in(4).bits.req(w).way_en := DontCare
    metaReadArb.io.in(4).bits.req(w).tag    := DontCare
    // Data read for new requests
    dataReadArb.io.in(2).bits.valid(w)      := io.lsu.req.bits(w).valid
    dataReadArb.io.in(2).bits.req(w).addr   := io.lsu.req.bits(w).bits.addr
    dataReadArb.io.in(2).bits.req(w).way_en := ~0.U(nWays.W)
  }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:526-535
```scala
  // MSHR Replays
  val replay_req = Wire(Vec(lsuWidth, new BoomDCacheReq))
  replay_req               := DontCare
  replay_req(0).uop        := mshrs.io.replay.bits.uop
  replay_req(0).addr       := mshrs.io.replay.bits.addr
  replay_req(0).data       := mshrs.io.replay.bits.data
  replay_req(0).is_hella   := mshrs.io.replay.bits.is_hella
  // Don't let replays get nacked due to conflict with dcache write
  mshrs.io.replay.ready    := metaReadArb.io.in(0).ready && dataReadArb.io.in(0).ready && !singlePortedDCacheWrite
  // Tag read for MSHR replays
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:536-546
```scala
  // We don't actually need to read the metadata, for replays we already know our way
  metaReadArb.io.in(0).valid              := mshrs.io.replay.valid && !singlePortedDCacheWrite
  metaReadArb.io.in(0).bits.req(0).idx    := mshrs.io.replay.bits.addr >> blockOffBits
  metaReadArb.io.in(0).bits.req(0).way_en := DontCare
  metaReadArb.io.in(0).bits.req(0).tag    := DontCare
  // Data read for MSHR replays
  dataReadArb.io.in(0).valid              := mshrs.io.replay.valid && !singlePortedDCacheWrite
  dataReadArb.io.in(0).bits.req(0).addr   := mshrs.io.replay.bits.addr
  dataReadArb.io.in(0).bits.req(0).way_en := mshrs.io.replay.bits.way_en
  dataReadArb.io.in(0).bits.valid         := widthMap(w => (w == 0).B)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:548-558
```scala
  // MSHR Meta read
  val mshr_read_req = Wire(Vec(lsuWidth, new BoomDCacheReq))
  mshr_read_req             := DontCare
  mshr_read_req(0).uop      := NullMicroOp
  mshr_read_req(0).addr     := Cat(mshrs.io.meta_read.bits.tag, mshrs.io.meta_read.bits.idx) << blockOffBits
  mshr_read_req(0).data     := DontCare
  mshr_read_req(0).is_hella := false.B
  metaReadArb.io.in(3).valid       := mshrs.io.meta_read.valid
  metaReadArb.io.in(3).bits.req(0) := mshrs.io.meta_read.bits
  mshrs.io.meta_read.ready         := metaReadArb.io.in(3).ready
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:562-570
```scala
  // Write-backs
  val wb_fire = wb.io.meta_read.fire && wb.io.data_req.fire
  val wb_req = Wire(Vec(lsuWidth, new BoomDCacheReq))
  wb_req             := DontCare
  wb_req(0).uop      := NullMicroOp
  wb_req(0).addr     := Cat(wb.io.meta_read.bits.tag, wb.io.data_req.bits.addr)
  wb_req(0).data     := DontCare
  wb_req(0).is_hella := false.B
  // Couple the two decoupled interfaces of the WBUnit's meta_read and data_read
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:572-582
```scala
  // Tag read for write-back
  metaReadArb.io.in(2).valid        := wb.io.meta_read.valid && !singlePortedDCacheWrite
  metaReadArb.io.in(2).bits.req(0)  := wb.io.meta_read.bits
  wb.io.meta_read.ready := metaReadArb.io.in(2).ready && dataReadArb.io.in(1).ready && !singlePortedDCacheWrite
  // Data read for write-back
  dataReadArb.io.in(1).valid        := wb.io.data_req.valid && !singlePortedDCacheWrite
  dataReadArb.io.in(1).bits.req(0)  := wb.io.data_req.bits
  dataReadArb.io.in(1).bits.valid   := widthMap(w => (w == 0).B)
  wb.io.data_req.ready  := metaReadArb.io.in(2).ready && dataReadArb.io.in(1).ready && !singlePortedDCacheWrite
  assert(!(wb.io.meta_read.fire ^ wb.io.data_req.fire))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:585-596
```scala
  val prober_fire  = prober.io.meta_read.fire
  val prober_req   = Wire(Vec(lsuWidth, new BoomDCacheReq))
  prober_req             := DontCare
  prober_req(0).uop      := NullMicroOp
  prober_req(0).addr     := Cat(prober.io.meta_read.bits.tag, prober.io.meta_read.bits.idx) << blockOffBits
  prober_req(0).data     := DontCare
  prober_req(0).is_hella := false.B
  // Tag read for prober
  metaReadArb.io.in(1).valid       := prober.io.meta_read.valid
  metaReadArb.io.in(1).bits.req(0) := prober.io.meta_read.bits
  prober.io.meta_read.ready := metaReadArb.io.in(1).ready
  // Prober does not need to read data array
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:600-610
```scala
  val prefetch_fire = mshrs.io.prefetch.fire
  val prefetch_req  = Wire(Vec(lsuWidth, new BoomDCacheReq))
  prefetch_req    := DontCare
  prefetch_req(0) := mshrs.io.prefetch.bits
  // Tag read for prefetch
  metaReadArb.io.in(5).valid              := mshrs.io.prefetch.valid
  metaReadArb.io.in(5).bits.req(0).idx    := mshrs.io.prefetch.bits.addr >> blockOffBits
  metaReadArb.io.in(5).bits.req(0).way_en := DontCare
  metaReadArb.io.in(5).bits.req(0).tag    := DontCare
  mshrs.io.prefetch.ready := metaReadArb.io.in(5).ready
  // Prefetch does not need to read data array
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:611-626
```scala

  val s0_valid = Mux(io.lsu.req.fire, VecInit(io.lsu.req.bits.map(_.valid)),
                 Mux(mshrs.io.replay.fire || wb_fire || prober_fire || prefetch_fire || mshrs.io.meta_read.fire,
                                        VecInit(1.U(lsuWidth.W).asBools), VecInit(0.U(lsuWidth.W).asBools)))
  val s0_req   = Mux(io.lsu.req.fire          , VecInit(io.lsu.req.bits.map(_.bits)),
                 Mux(wb_fire                  , wb_req,
                 Mux(prober_fire              , prober_req,
                 Mux(prefetch_fire            , prefetch_req,
                 Mux(mshrs.io.meta_read.fire, mshr_read_req
                                              , replay_req)))))
  val s0_type  = Mux(io.lsu.req.fire        , t_lsu,
                 Mux(wb_fire                  , t_wb,
                 Mux(prober_fire              , t_probe,
                 Mux(prefetch_fire            , t_prefetch,
                 Mux(mshrs.io.meta_read.fire, t_mshr_meta_read
                                              , t_replay)))))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:628-631
```scala
  // Does this request need to send a response or nack
  val s0_send_resp_or_nack = Mux(io.lsu.req.fire, s0_valid,
    VecInit(Mux(mshrs.io.replay.fire && isRead(mshrs.io.replay.bits.uop.mem_cmd), 1.U(lsuWidth.W), 0.U(lsuWidth.W)).asBools))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:632-642
```scala

  val s1_req          = RegNext(s0_req)
  for (w <- 0 until lsuWidth)
    s1_req(w).uop.br_mask := GetNewBrMask(io.lsu.brupdate, s0_req(w).uop)
  val s2_store_failed = Wire(Bool())
  val s1_valid = widthMap(w =>
                 RegNext(s0_valid(w)                                     &&
                         !IsKilledByBranch(io.lsu.brupdate, false.B, s0_req(w).uop) &&
                         !(io.lsu.exception && s0_req(w).uop.uses_ldq)   &&
                         !(s2_store_failed && io.lsu.req.fire && s0_req(w).uop.uses_stq),
                         init=false.B))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:644-646
```scala
  for (w <- 0 until lsuWidth)
    assert(!(io.lsu.s1_kill(w) && !RegNext(io.lsu.req.fire) && !RegNext(io.lsu.req.bits(w).valid)))
  val s1_addr         = s1_req.map(_.addr)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:647-654
```scala
  val s1_nack         = s1_addr.map(a => a(idxMSB,idxLSB) === prober.io.meta_write.bits.idx && !prober.io.req.ready)
  val s1_send_resp_or_nack = RegNext(s0_send_resp_or_nack)
  val s1_type         = RegNext(s0_type)

  val s1_mshr_meta_read_way_en = RegNext(mshrs.io.meta_read.bits.way_en)
  val s1_replay_way_en         = RegNext(mshrs.io.replay.bits.way_en) // For replays, the metadata isn't written yet
  val s1_wb_way_en             = RegNext(wb.io.data_req.bits.way_en)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:655-657
```scala
  // tag check
  def wayMap[T <: Data](f: Int => T) = VecInit((0 until nWays).map(f))
  val s1_tag_eq_way = widthMap(i => wayMap((w: Int) => meta(i).io.resp(w).tag === (s1_addr(i) >> untagBits)).asUInt)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:666-668
```scala
  for (w <- 0 until lsuWidth) {
    io.lsu.s1_nack_advisory(w) := data.io.s1_nacks(w)
  }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:669-674
```scala

  val s2_req   = RegNext(s1_req)
  val s2_type  = RegNext(s1_type)
  val s2_valid = widthMap(w =>
                  RegNext(s1_valid(w) &&
                         !io.lsu.s1_kill(w) &&
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:680-684
```scala

  val s2_tag_match_way = RegNext(s1_tag_match_way)
  val s2_tag_match     = s2_tag_match_way.map(_.orR)
  val s2_hit_state     = widthMap(i => Mux1H(s2_tag_match_way(i), wayMap((w: Int) => RegNext(meta(i).io.resp(w).coh))))
  val s2_has_permission = widthMap(w => s2_hit_state(w).onAccess(s2_req(w).uop.mem_cmd)._1)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:686-693
```scala

  val s2_hit = widthMap(w => (s2_tag_match(w) && s2_has_permission(w) && s2_hit_state(w) === s2_new_hit_state(w) && !mshrs.io.block_hit(w)) || s2_type.isOneOf(t_replay, t_wb))
  val s2_nack = Wire(Vec(lsuWidth, Bool()))
  assert(!(s2_type === t_replay && !s2_hit(0)), "Replays should always hit")
  assert(!(s2_type === t_wb && !s2_hit(0)), "Writeback should always see data hit")

  val s2_wb_idx_matches = RegNext(s1_wb_idx_matches)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:694-704
```scala
  // lr/sc
  val debug_sc_fail_addr = RegInit(0.U)
  val debug_sc_fail_cnt  = RegInit(0.U(8.W))

  val lrsc_count = RegInit(0.U(log2Ceil(lrscCycles).W))
  val lrsc_valid = lrsc_count > lrscBackoff.U
  val lrsc_addr  = Reg(UInt())
  val s2_lr = s2_req(0).uop.mem_cmd === M_XLR && (!RegNext(s1_nack(0)) || s2_type === t_replay)
  val s2_sc = s2_req(0).uop.mem_cmd === M_XSC && (!RegNext(s1_nack(0)) || s2_type === t_replay)
  val s2_lrsc_addr_match = widthMap(w => lrsc_valid && lrsc_addr === (s2_req(w).addr >> blockOffBits))
  val s2_sc_fail = s2_sc && !s2_lrsc_addr_match(0)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:705-708
```scala
  when (lrsc_count > 0.U) { lrsc_count := lrsc_count - 1.U }
  when (s2_valid(0) && ((s2_type === t_lsu && s2_hit(0) && !s2_nack(0)) ||
                     (s2_type === t_replay && s2_req(0).uop.mem_cmd =/= M_FLUSH_ALL))) {
    when (s2_lr) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:709-711
```scala
      lrsc_count := (lrscCycles - 1).U
      lrsc_addr := s2_req(0).addr >> blockOffBits
    }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:717-719
```scala
    when (s2_valid(w)                            &&
      s2_type === t_lsu                          &&
      !s2_hit(w)                                 &&
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:726-733
```scala

  when (s2_valid(0)) {
    when (s2_req(0).addr === debug_sc_fail_addr) {
      when (s2_sc_fail) {
        debug_sc_fail_cnt := debug_sc_fail_cnt + 1.U
      } .elsewhen (s2_sc) {
        debug_sc_fail_cnt := 0.U
      }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:734-738
```scala
    } .otherwise {
      when (s2_sc_fail) {
        debug_sc_fail_addr := s2_req(0).addr
        debug_sc_fail_cnt  := 1.U
      }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:740-744
```scala
  }
  assert(debug_sc_fail_cnt < 100.U, "L1DCache failed too many SCs in a row")

  val s2_data = Wire(Vec(lsuWidth, Vec(nWays, UInt(encRowBits.W))))
  for (i <- 0 until lsuWidth) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:755-758
```scala
  val s1_replaced_way_en = UIntToOH(replacer.way)
  val s2_replaced_way_en = UIntToOH(RegNext(replacer.way))
  val s2_repl_meta = widthMap(i => Mux1H(s2_replaced_way_en, wayMap((w: Int) => RegNext(meta(i).io.resp(w))).toSeq))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:759-774
```scala
  // nack because of incoming probe
  val s2_nack_hit    = RegNext(VecInit(s1_nack))
  // Nack when we hit something currently being evicted
  val s2_nack_victim = widthMap(w => s2_valid(w) &&  s2_hit(w) && mshrs.io.secondary_miss(w))
  // MSHRs not ready for request
  val s2_nack_miss   = widthMap(w => s2_valid(w) && !s2_hit(w) && !mshrs.io.req(w).ready)
  // Bank conflict on data arrays
  val s2_nack_data   = widthMap(w => s2_valid(w) && RegNext(data.io.s1_nacks(w)))
  // Can't allocate MSHR for same set currently being written back
  val s2_nack_wb     = widthMap(w => s2_valid(w) && !s2_hit(w) && s2_wb_idx_matches(w))

  s2_nack           := widthMap(w => (s2_nack_miss(w) || s2_nack_hit(w) || s2_nack_victim(w) || s2_nack_data(w) || s2_nack_wb(w)) && s2_type =/= t_replay)
  assert(!(s2_nack_data.reduce(_||_) && s2_type.isOneOf(t_replay, t_wb)))
  val s2_send_resp = widthMap(w => (
    RegNext(s1_send_resp_or_nack(w)) &&
      (!(s2_nack_hit(w) || s2_nack_victim(w) || s2_nack_data(w)) || s2_type === t_replay) &&
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:777-783
```scala
  val s2_send_store_ack = widthMap(w => (
    RegNext(s1_send_resp_or_nack(w)) && !s2_nack(w) && isWrite(s2_req(w).uop.mem_cmd) &&
      (s2_hit(w) || mshrs.io.req(w).fire)))
  val s2_send_nack = widthMap(w => (RegNext(s1_send_resp_or_nack(w)) && s2_nack(w)))
  for (w <- 0 until lsuWidth)
    assert(!(s2_send_resp(w) && s2_send_nack(w)))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:801-813
```scala
                              isWrite(s2_req(w).uop.mem_cmd))
    assert(!(mshrs.io.req(w).valid && s2_type === t_replay), "Replays should not need to go back into MSHRs")
    mshrs.io.req(w).bits             := DontCare
    mshrs.io.req(w).bits.uop         := s2_req(w).uop
    mshrs.io.req(w).bits.addr        := s2_req(w).addr
    mshrs.io.req(w).bits.tag_match   := s2_tag_match(w)
    mshrs.io.req(w).bits.old_meta    := Mux(s2_tag_match(w), L1Metadata(s2_repl_meta(w).tag, s2_hit_state(w)), s2_repl_meta(w))
    mshrs.io.req(w).bits.way_en      := Mux(s2_tag_match(w), s2_tag_match_way(w), s2_replaced_way_en)

    mshrs.io.req(w).bits.data        := s2_req(w).data
    mshrs.io.req(w).bits.is_hella    := s2_req(w).is_hella
    mshrs.io.req_is_probe(w)         := s2_type === t_probe && s2_valid(w)
  }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:814-819
```scala

  mshrs.io.meta_resp.valid      := !s2_nack_hit(0) || prober.io.mshr_wb_rdy
  mshrs.io.meta_resp.bits       := Mux1H(s2_tag_match_way(0), RegNext(meta(0).io.resp))
  when (mshrs.io.req.map(_.fire).reduce(_||_)) { replacer.miss }
  tl_out.a <> mshrs.io.mem_acquire
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:820-830
```scala
  // probes and releases
  prober.io.req.valid   := tl_out.b.valid && !lrsc_valid
  tl_out.b.ready        := prober.io.req.ready && !lrsc_valid
  prober.io.req.bits    := tl_out.b.bits
  prober.io.way_en      := s2_tag_match_way(0)
  prober.io.block_state := s2_hit_state(0)
  metaWriteArb.io.in(1) <> prober.io.meta_write
  prober.io.mshr_rdy    := mshrs.io.probe_rdy
  prober.io.wb_rdy      := (prober.io.meta_write.bits.idx =/= wb.io.idx.bits) || !wb.io.idx.valid
  mshrs.io.prober_state := prober.io.state
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:834-837
```scala
    tl_out.d.ready := true.B
    mshrs.io.mem_grant.valid := false.B
    mshrs.io.mem_grant.bits  := DontCare
  } .otherwise {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:841-846
```scala

  dataWriteArb.io.in(1) <> mshrs.io.refill
  metaWriteArb.io.in(0) <> mshrs.io.meta_write

  tl_out.e <> mshrs.io.mem_finish
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:847-861
```scala
  // writebacks
  val wbArb = Module(new Arbiter(new WritebackReq(edge.bundle), 2))
  // 0 goes to prober, 1 goes to MSHR evictions
  wbArb.io.in(0)       <> prober.io.wb_req
  wbArb.io.in(1)       <> mshrs.io.wb_req
  wb.io.req            <> wbArb.io.out
  wb.io.data_resp       := s2_data_muxed(0)
  mshrs.io.wb_resp      := wb.io.resp
  wb.io.mem_grant       := tl_out.d.fire && tl_out.d.bits.source === cfg.nMSHRs.U

  val lsu_release_arb = Module(new Arbiter(new TLBundleC(edge.bundle), 2))
  io.lsu.release <> lsu_release_arb.io.out
  lsu_release_arb.io.in(0) <> wb.io.lsu_release
  lsu_release_arb.io.in(1) <> prober.io.lsu_release
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:863-866
```scala

  io.lsu.perf.release := edge.done(tl_out.c)
  io.lsu.perf.acquire := edge.done(tl_out.a)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:868-870
```scala
  val s2_data_word_prebypass = widthMap(w => s2_data_muxed(w) >> Cat(s2_word_idx(w), 0.U(log2Ceil(coreDataBits).W)))
  val s2_data_word = Wire(Vec(lsuWidth, UInt()))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:885-887
```scala
    io.lsu.nack(w).bits  := s2_req(w)
    assert(!(io.lsu.nack(w).valid && s2_type =/= t_lsu))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:891-893
```scala

  io.lsu.ll_resp <> mshrs.io.resp
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:894-900
```scala
  // Store/amo hits
  val s3_req   = Wire(new BoomDCacheReq)
  s3_req := RegNext(s2_req(0))
  val s3_valid = RegNext(s2_valid(0) && s2_hit(0) && isWrite(s2_req(0).uop.mem_cmd) &&
                         !s2_sc_fail && !(s2_send_nack(0) && s2_nack(0)))
  val s3_data_word = RegNext(s2_data_word(0))
  for (w <- 1 until lsuWidth) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:907-912
```scala
  // For bypassing
  val s4_req   = RegNext(s3_req)
  val s4_valid = RegNext(s3_valid)
  val s5_req   = RegNext(s4_req)
  val s5_valid = RegNext(s4_valid)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:923-929
```scala
  }
  val amoalu   = Module(new AMOALU(xLen))
  amoalu.io.mask := new StoreGen(s3_req.uop.mem_size, s3_req.addr, 0.U, xLen/8).mask
  amoalu.io.cmd  := s3_req.uop.mem_cmd
  amoalu.io.lhs  := s3_data_word
  amoalu.io.rhs  := RegNext(s2_req(0).data)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:931-939
```scala
  s3_req.data := amoalu.io.out
  val s3_way   = RegNext(s2_tag_match_way(0))

  dataWriteArb.io.in(0).valid       := s3_valid
  dataWriteArb.io.in(0).bits.addr   := s3_req.addr
  dataWriteArb.io.in(0).bits.wmask  := UIntToOH(s3_req.addr.extract(rowOffBits-1,offsetlsb))
  dataWriteArb.io.in(0).bits.data   := Fill(rowWords, s3_req.data)
  dataWriteArb.io.in(0).bits.way_en := s3_way
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:940-942
```scala

  io.lsu.ordered := mshrs.io.fence_rdy && !s1_valid.reduce(_||_) && !s2_valid.reduce(_||_)
}
```

### generators/boom/src/main/scala/v4/util/util.scala:60-62
```scala
  def apply(brupdate: BrUpdateInfo, flush: Bool, uop_mask: UInt): Bool = {
    return maskMatch(brupdate.b1.mispredict_mask, uop_mask) || flush
  }
```

### generators/boom/src/main/scala/v4/util/util.scala:92-94
```scala
   def apply(brupdate: BrUpdateInfo, uop: MicroOp): UInt = {
     return uop.br_mask & ~brupdate.b1.resolve_mask
   }
```

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
```

### generators/diplomacy/diplomacy/src/diplomacy/lazymodule/LazyModuleImp.scala:106-108
```scala
    // Generate [[AutoBundle]] IO from [[forward]].
    val auto        = IO(new AutoBundle(forward.map { d => (d.name, d.data, d.flipped) }: _*))
    // Pass the [[Dangle]]s which remained and were used to generate the [[AutoBundle]] I/O ports up to the [[parent]] [[LazyModule]]
```

### generators/diplomacy/diplomacy/src/diplomacy/lazymodule/LazyModuleImp.scala:112-114
```scala
      } else {
        io <> d.data
      }
```

### generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:542-544
```scala
  protected[diplomacy] lazy val bundleOut: Seq[BO] = edgesOut.map { e =>
    val x = Wire(outer.bundleO(e)).suggestName(s"${valName.value}Out")
    // TODO: Don't care unconnected forwarded diplomatic signals for compatibility issue,
```

### generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:545-547
```scala
    //       In the future, we should add an option to decide whether allowing unconnected in the LazyModule
    x := DontCare
    x
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:10-14
```scala
class StoreGen(typ: UInt, addr: UInt, dat: UInt, maxSize: Int) {
  val size = Wire(UInt(log2Up(log2Up(maxSize)+1).W))
  size := typ
  val dat_padded = dat.pad(maxSize*8)
  def misaligned: Bool =
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:19-23
```scala
    for (i <- 0 until log2Up(maxSize)) {
      val upper = Mux(addr(i), res, 0.U) | Mux(size >= (i+1).U, ((BigInt(1) << (1 << i))-1).U, 0.U)
      val lower = Mux(addr(i), 0.U, res)
      res = Cat(upper, lower)
    }
```

### generators/rocket-chip/src/main/scala/rocket/Consts.scala:86-92
```scala
  def isAMOArithmetic(cmd: UInt) = cmd.isOneOf(M_XA_ADD, M_XA_MIN, M_XA_MAX, M_XA_MINU, M_XA_MAXU)
  def isAMO(cmd: UInt) = isAMOLogical(cmd) || isAMOArithmetic(cmd)
  def isPrefetch(cmd: UInt) = cmd === M_PFR || cmd === M_PFW
  def isRead(cmd: UInt) = cmd.isOneOf(M_XRD, M_HLVX, M_XLR, M_XSC) || isAMO(cmd)
  def isWrite(cmd: UInt) = cmd === M_XWR || cmd === M_PWR || cmd === M_XSC || isAMO(cmd)
  def isWriteIntent(cmd: UInt) = isWrite(cmd) || cmd === M_PFW || cmd === M_XLR
}
```

### generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:304-308
```scala
  def apply(tag: Bits, coh: ClientMetadata)(implicit p: Parameters) = {
    val meta = Wire(new L1Metadata)
    meta.tag := tag
    meta.coh := coh
    meta
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:59-61
```scala
      // The number of beats which remain to be sent
      val beatsLeft = RegInit(0.U)
      val idle = beatsLeft === 0.U
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:67-69
```scala
      // Arbitrate amongst the requests
      val readys = VecInit(policy(valids.size, Cat(valids.reverse), latch).asBools)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:70-72
```scala
      // Which request wins arbitration?
      val winner = VecInit((readys zip valids) map { case (r,v) => r&&v })
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:75-80
```scala
      // Never two winners
      val prefixOR = winner.scanLeft(false.B)(_||_).init
      assert((prefixOR zip winner) map { case (p,w) => !p || !w } reduce {_ && _})
      // If there was any request, there is a winner
      assert (!valids.reduce(_||_) || winner.reduce(_||_))
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:87-89
```scala
      // The one-hot source granted access in the previous cycle
      val state = RegInit(VecInit(Seq.fill(sources.size)(false.B)))
      val muxState = Mux(idle, winner, state)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:91-95
```scala

      val allowed = Mux(idle, readys, state)
      (sourcesIn zip allowed) foreach { case (s, r) =>
        s.ready := sink.ready && r
      }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:91-93
```scala
    val opdata = x match {
      case a: TLBundleA => !a.opcode(2)
        //    opcode === TLMessages.PutFullData    ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:101-103
```scala
        //    opcode === TLMessages.LogicalData
      case c: TLBundleC => c.opcode(0)
        //    opcode === TLMessages.AccessAckData ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:219-222
```scala
        } else {
          val decode = UIntToOH1(size(bundle), maxLgSize) >> log2Ceil(manager.beatBytes)
          Mux(hasData(bundle), decode, 0.U)
        }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:228-237
```scala
    val beats1   = numBeats1(bits)
    val counter  = RegInit(0.U(log2Up(maxTransfer / manager.beatBytes).W))
    val counter1 = counter - 1.U
    val first = counter === 0.U
    val last  = counter === 1.U || beats1 === 0.U
    val done  = last && fire
    val count = (beats1 & ~counter1)
    when (fire) {
      counter := Mux(first, beats1, counter1)
    }
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:23-27
```scala
object MemoryOpCategories extends MemoryOpConstants {
  def wr = Cat(true.B, true.B)   // Op actually writes
  def wi = Cat(false.B, true.B)  // Future op will write
  def rd = Cat(false.B, false.B) // Op only reads
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:28-30
```scala
  def categorize(cmd: UInt): UInt = {
    val cat = Cat(isWrite(cmd), isWriteIntent(cmd))
    //assert(cat.isOneOf(wr,wi,rd), "Could not categorize command.")
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:45-47
```scala
  def ===(rhs: UInt): Bool = state === rhs
  def ===(rhs: ClientMetadata): Bool = state === rhs.state
  def =/=(rhs: ClientMetadata): Bool = !this.===(rhs)
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:57-73
```scala
    val c = categorize(cmd)
    MuxTLookup(Cat(c, state), (false.B, 0.U), Seq(
    //(effect, am now) -> (was a hit,   next)
      Cat(rd, Dirty)   -> (true.B,  Dirty),
      Cat(rd, Trunk)   -> (true.B,  Trunk),
      Cat(rd, Branch)  -> (true.B,  Branch),
      Cat(wi, Dirty)   -> (true.B,  Dirty),
      Cat(wi, Trunk)   -> (true.B,  Trunk),
      Cat(wr, Dirty)   -> (true.B,  Dirty),
      Cat(wr, Trunk)   -> (true.B,  Dirty),
    //(effect, am now) -> (was a miss,  param)
      Cat(rd, Nothing) -> (false.B, NtoB),
      Cat(wi, Branch)  -> (false.B, BtoT),
      Cat(wi, Nothing) -> (false.B, NtoT),
      Cat(wr, Branch)  -> (false.B, BtoT),
      Cat(wr, Nothing) -> (false.B, NtoT)))
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:159-162
```scala
  def apply(perm: UInt) = {
    val meta = Wire(new ClientMetadata)
    meta.state := perm
    meta
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:34-36
```scala
  def apply[T <: Data, U <: Data](cond: Bool, con: (T, U), alt: (T, U)): (T, U) =
    (Mux(cond, con._1, alt._1), Mux(cond, con._2, alt._2))
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:48-50
```scala
    for ((k, v) <- mapping.reverse)
      res = MuxT(k === key, v, res)
    res
```

### generators/rocket-chip/src/main/scala/util/Replacement.scala:36-39
```scala
class RandomReplacement(n_ways: Int) extends ReplacementPolicy {
  private val replace = Wire(Bool())
  replace := false.B
  def nBits = 16
```

### generators/rocket-chip/src/main/scala/util/Replacement.scala:44-46
```scala
  def way = Random(n_ways, lfsr)
  def miss = replace := true.B
  def hit = {}
```

### generators/rocket-chip/src/main/scala/util/package.scala:16-18
```scala
  implicit class UIntIsOneOf(private val x: UInt) extends AnyVal {
    def isOneOf(s: Seq[UInt]): Bool = s.map(x === _).orR
```

### generators/rocket-chip/src/main/scala/util/package.scala:81-83
```scala
    def andR: Bool = if (x.isEmpty) true.B else x.reduce(_&&_)
    def orR: Bool = if (x.isEmpty) false.B else x.reduce(_||_)
    def xorR: Bool = if (x.isEmpty) false.B else x.reduce(_^_)
```

### generators/rocket-chip/src/main/scala/util/package.scala:163-165
```scala
      if (hi == lo-1) 0.U
      else x(hi, lo)
    }
```

### generators/rocket-chip/src/main/scala/util/package.scala:243-245
```scala
  def OH1ToUInt(x: UInt): UInt = OHToUInt(OH1ToOH(x))
  def UIntToOH1(x: UInt, width: Int): UInt = ~((-1).S(width.W).asUInt << x)(width-1, 0)
  def UIntToOH1(x: UInt): UInt = UIntToOH1(x, (1 << x.getWidth) - 1)
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Parent-local FIRRTL statement ledger

Only these parent-local statement IDs may appear in `evidence_statement_ids`.

```text
[0] FIRRTL:197768 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:438:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197769 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:438:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197770 SRC:generators/diplomacy/diplomacy/src/diplomacy/lazymodule/LazyModuleImp.scala:107:25 KIND:structural :: output auto : { out : { a : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, flip b : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, address : UInt<32>, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, c : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, flip d : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, sink : UInt<3>, denied : UInt<1>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, e : { flip ready : UInt<1>, valid : UInt<1>, bits : { sink : UInt<3>}}}}
[3] FIRRTL:197771 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:444:14 KIND:structural :: output io : { errors : { bus : { valid : UInt<1>, bits : UInt<32>}}, flip lsu : { req : { flip ready : UInt<1>, valid : UInt<1>, bits : { valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}[1]}, s1_kill : UInt<1>[1], flip s1_nack_advisory : UInt<1>[1], flip resp : { valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}[1], flip store_ack : { valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}[1], flip nack : { valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}[1], flip ll_resp : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, exception : UInt<1>, rob_pnr_idx : UInt<5>, rob_head_idx : UInt<5>, flip release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, force_order : UInt<1>, flip ordered : UInt<1>, flip perf : { acquire : UInt<1>, release : UInt<1>}}}
[4] FIRRTL:197773 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:543:17 KIND:wire :: wire nodeOut : { a : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, flip b : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, address : UInt<32>, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, c : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, flip d : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, sink : UInt<3>, denied : UInt<1>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, e : { flip ready : UInt<1>, valid : UInt<1>, bits : { sink : UInt<3>}}}
[5] FIRRTL:197774 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.e.bits.sink
[6] FIRRTL:197775 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.e.valid
[7] FIRRTL:197776 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.e.ready
[8] FIRRTL:197777 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.corrupt
[9] FIRRTL:197778 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.data
[10] FIRRTL:197779 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.denied
[11] FIRRTL:197780 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.sink
[12] FIRRTL:197781 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.source
[13] FIRRTL:197782 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.size
[14] FIRRTL:197783 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.param
[15] FIRRTL:197784 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.bits.opcode
[16] FIRRTL:197785 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.valid
[17] FIRRTL:197786 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.d.ready
[18] FIRRTL:197787 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.corrupt
[19] FIRRTL:197788 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.data
[20] FIRRTL:197789 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.address
[21] FIRRTL:197790 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.source
[22] FIRRTL:197791 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.size
[23] FIRRTL:197792 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.param
[24] FIRRTL:197793 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.bits.opcode
[25] FIRRTL:197794 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.valid
[26] FIRRTL:197795 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.c.ready
[27] FIRRTL:197796 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.corrupt
[28] FIRRTL:197797 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.data
[29] FIRRTL:197798 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.mask
[30] FIRRTL:197799 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.address
[31] FIRRTL:197800 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.source
[32] FIRRTL:197801 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.size
[33] FIRRTL:197802 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.param
[34] FIRRTL:197803 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.bits.opcode
[35] FIRRTL:197804 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.valid
[36] FIRRTL:197805 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.b.ready
[37] FIRRTL:197806 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.corrupt
[38] FIRRTL:197807 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.data
[39] FIRRTL:197808 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.mask
[40] FIRRTL:197809 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.address
[41] FIRRTL:197810 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.source
[42] FIRRTL:197811 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.size
[43] FIRRTL:197812 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.param
[44] FIRRTL:197813 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.bits.opcode
[45] FIRRTL:197814 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.valid
[46] FIRRTL:197815 SRC:generators/diplomacy/diplomacy/src/diplomacy/nodes/MixedNode.scala:546:7 KIND:invalidate :: invalidate nodeOut.a.ready
[47] FIRRTL:197816 SRC:generators/diplomacy/diplomacy/src/diplomacy/lazymodule/LazyModuleImp.scala:113:12 KIND:connect :: connect auto.out, nodeOut
[48] FIRRTL:197817 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:446:13 KIND:invalidate :: invalidate io.errors.bus.bits
[49] FIRRTL:197818 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:446:13 KIND:invalidate :: invalidate io.errors.bus.valid
[50] FIRRTL:197819 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:458:18 KIND:structural :: inst wb of BoomWritebackUnit
[51] FIRRTL:197820 SRC:<no-source-locator> KIND:connect :: connect wb.clock, clock
[52] FIRRTL:197821 SRC:<no-source-locator> KIND:connect :: connect wb.reset, reset
[53] FIRRTL:197822 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:459:22 KIND:structural :: inst prober of BoomProbeUnit
[54] FIRRTL:197823 SRC:<no-source-locator> KIND:connect :: connect prober.clock, clock
[55] FIRRTL:197824 SRC:<no-source-locator> KIND:connect :: connect prober.reset, reset
[56] FIRRTL:197825 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:460:21 KIND:structural :: inst mshrs of BoomMSHRFile
[57] FIRRTL:197826 SRC:<no-source-locator> KIND:connect :: connect mshrs.clock, clock
[58] FIRRTL:197827 SRC:<no-source-locator> KIND:connect :: connect mshrs.reset, reset
[59] FIRRTL:197828 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:461:25 KIND:connect :: connect mshrs.io.clear_all, io.lsu.force_order
[60] FIRRTL:197829 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.target_offset, io.lsu.brupdate.b2.target_offset
[61] FIRRTL:197830 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.jalr_target, io.lsu.brupdate.b2.jalr_target
[62] FIRRTL:197831 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.pc_sel, io.lsu.brupdate.b2.pc_sel
[63] FIRRTL:197832 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.cfi_type, io.lsu.brupdate.b2.cfi_type
[64] FIRRTL:197833 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.taken, io.lsu.brupdate.b2.taken
[65] FIRRTL:197834 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.mispredict, io.lsu.brupdate.b2.mispredict
[66] FIRRTL:197835 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.debug_tsrc, io.lsu.brupdate.b2.uop.debug_tsrc
[67] FIRRTL:197836 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.debug_fsrc, io.lsu.brupdate.b2.uop.debug_fsrc
[68] FIRRTL:197837 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.bp_xcpt_if, io.lsu.brupdate.b2.uop.bp_xcpt_if
[69] FIRRTL:197838 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.bp_debug_if, io.lsu.brupdate.b2.uop.bp_debug_if
[70] FIRRTL:197839 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.xcpt_ma_if, io.lsu.brupdate.b2.uop.xcpt_ma_if
[71] FIRRTL:197840 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.xcpt_ae_if, io.lsu.brupdate.b2.uop.xcpt_ae_if
[72] FIRRTL:197841 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.xcpt_pf_if, io.lsu.brupdate.b2.uop.xcpt_pf_if
[73] FIRRTL:197842 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_typ, io.lsu.brupdate.b2.uop.fp_typ
[74] FIRRTL:197843 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_rm, io.lsu.brupdate.b2.uop.fp_rm
[75] FIRRTL:197844 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_val, io.lsu.brupdate.b2.uop.fp_val
[76] FIRRTL:197845 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fcn_op, io.lsu.brupdate.b2.uop.fcn_op
[77] FIRRTL:197846 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fcn_dw, io.lsu.brupdate.b2.uop.fcn_dw
[78] FIRRTL:197847 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.frs3_en, io.lsu.brupdate.b2.uop.frs3_en
[79] FIRRTL:197848 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.lrs2_rtype, io.lsu.brupdate.b2.uop.lrs2_rtype
[80] FIRRTL:197849 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.lrs1_rtype, io.lsu.brupdate.b2.uop.lrs1_rtype
[81] FIRRTL:197850 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.dst_rtype, io.lsu.brupdate.b2.uop.dst_rtype
[82] FIRRTL:197851 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.lrs3, io.lsu.brupdate.b2.uop.lrs3
[83] FIRRTL:197852 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.lrs2, io.lsu.brupdate.b2.uop.lrs2
[84] FIRRTL:197853 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.lrs1, io.lsu.brupdate.b2.uop.lrs1
[85] FIRRTL:197854 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ldst, io.lsu.brupdate.b2.uop.ldst
[86] FIRRTL:197855 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ldst_is_rs1, io.lsu.brupdate.b2.uop.ldst_is_rs1
[87] FIRRTL:197856 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.csr_cmd, io.lsu.brupdate.b2.uop.csr_cmd
[88] FIRRTL:197857 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.flush_on_commit, io.lsu.brupdate.b2.uop.flush_on_commit
[89] FIRRTL:197858 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_unique, io.lsu.brupdate.b2.uop.is_unique
[90] FIRRTL:197859 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.uses_stq, io.lsu.brupdate.b2.uop.uses_stq
[91] FIRRTL:197860 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.uses_ldq, io.lsu.brupdate.b2.uop.uses_ldq
[92] FIRRTL:197861 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.mem_signed, io.lsu.brupdate.b2.uop.mem_signed
[93] FIRRTL:197862 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.mem_size, io.lsu.brupdate.b2.uop.mem_size
[94] FIRRTL:197863 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.mem_cmd, io.lsu.brupdate.b2.uop.mem_cmd
[95] FIRRTL:197864 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.exc_cause, io.lsu.brupdate.b2.uop.exc_cause
[96] FIRRTL:197865 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.exception, io.lsu.brupdate.b2.uop.exception
[97] FIRRTL:197866 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.stale_pdst, io.lsu.brupdate.b2.uop.stale_pdst
[98] FIRRTL:197867 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ppred_busy, io.lsu.brupdate.b2.uop.ppred_busy
[99] FIRRTL:197868 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs3_busy, io.lsu.brupdate.b2.uop.prs3_busy
[100] FIRRTL:197869 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs2_busy, io.lsu.brupdate.b2.uop.prs2_busy
[101] FIRRTL:197870 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs1_busy, io.lsu.brupdate.b2.uop.prs1_busy
[102] FIRRTL:197871 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ppred, io.lsu.brupdate.b2.uop.ppred
[103] FIRRTL:197872 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs3, io.lsu.brupdate.b2.uop.prs3
[104] FIRRTL:197873 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs2, io.lsu.brupdate.b2.uop.prs2
[105] FIRRTL:197874 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.prs1, io.lsu.brupdate.b2.uop.prs1
[106] FIRRTL:197875 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.pdst, io.lsu.brupdate.b2.uop.pdst
[107] FIRRTL:197876 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.rxq_idx, io.lsu.brupdate.b2.uop.rxq_idx
[108] FIRRTL:197877 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.stq_idx, io.lsu.brupdate.b2.uop.stq_idx
[109] FIRRTL:197878 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ldq_idx, io.lsu.brupdate.b2.uop.ldq_idx
[110] FIRRTL:197879 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.rob_idx, io.lsu.brupdate.b2.uop.rob_idx
[111] FIRRTL:197880 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.vec, io.lsu.brupdate.b2.uop.fp_ctrl.vec
[112] FIRRTL:197881 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.wflags, io.lsu.brupdate.b2.uop.fp_ctrl.wflags
[113] FIRRTL:197882 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.sqrt, io.lsu.brupdate.b2.uop.fp_ctrl.sqrt
[114] FIRRTL:197883 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.div, io.lsu.brupdate.b2.uop.fp_ctrl.div
[115] FIRRTL:197884 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.fma, io.lsu.brupdate.b2.uop.fp_ctrl.fma
[116] FIRRTL:197885 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.lsu.brupdate.b2.uop.fp_ctrl.fastpipe
[117] FIRRTL:197886 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.toint, io.lsu.brupdate.b2.uop.fp_ctrl.toint
[118] FIRRTL:197887 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.fromint, io.lsu.brupdate.b2.uop.fp_ctrl.fromint
[119] FIRRTL:197888 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.lsu.brupdate.b2.uop.fp_ctrl.typeTagOut
[120] FIRRTL:197889 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.lsu.brupdate.b2.uop.fp_ctrl.typeTagIn
[121] FIRRTL:197890 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.swap23, io.lsu.brupdate.b2.uop.fp_ctrl.swap23
[122] FIRRTL:197891 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.swap12, io.lsu.brupdate.b2.uop.fp_ctrl.swap12
[123] FIRRTL:197892 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.ren3, io.lsu.brupdate.b2.uop.fp_ctrl.ren3
[124] FIRRTL:197893 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.ren2, io.lsu.brupdate.b2.uop.fp_ctrl.ren2
[125] FIRRTL:197894 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.ren1, io.lsu.brupdate.b2.uop.fp_ctrl.ren1
[126] FIRRTL:197895 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.wen, io.lsu.brupdate.b2.uop.fp_ctrl.wen
[127] FIRRTL:197896 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fp_ctrl.ldst, io.lsu.brupdate.b2.uop.fp_ctrl.ldst
[128] FIRRTL:197897 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.op2_sel, io.lsu.brupdate.b2.uop.op2_sel
[129] FIRRTL:197898 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.op1_sel, io.lsu.brupdate.b2.uop.op1_sel
[130] FIRRTL:197899 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.imm_packed, io.lsu.brupdate.b2.uop.imm_packed
[131] FIRRTL:197900 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.pimm, io.lsu.brupdate.b2.uop.pimm
[132] FIRRTL:197901 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.imm_sel, io.lsu.brupdate.b2.uop.imm_sel
[133] FIRRTL:197902 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.imm_rename, io.lsu.brupdate.b2.uop.imm_rename
[134] FIRRTL:197903 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.taken, io.lsu.brupdate.b2.uop.taken
[135] FIRRTL:197904 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.pc_lob, io.lsu.brupdate.b2.uop.pc_lob
[136] FIRRTL:197905 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.edge_inst, io.lsu.brupdate.b2.uop.edge_inst
[137] FIRRTL:197906 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.ftq_idx, io.lsu.brupdate.b2.uop.ftq_idx
[138] FIRRTL:197907 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_mov, io.lsu.brupdate.b2.uop.is_mov
[139] FIRRTL:197908 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_rocc, io.lsu.brupdate.b2.uop.is_rocc
[140] FIRRTL:197909 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_sys_pc2epc, io.lsu.brupdate.b2.uop.is_sys_pc2epc
[141] FIRRTL:197910 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_eret, io.lsu.brupdate.b2.uop.is_eret
[142] FIRRTL:197911 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_amo, io.lsu.brupdate.b2.uop.is_amo
[143] FIRRTL:197912 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_sfence, io.lsu.brupdate.b2.uop.is_sfence
[144] FIRRTL:197913 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_fencei, io.lsu.brupdate.b2.uop.is_fencei
[145] FIRRTL:197914 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_fence, io.lsu.brupdate.b2.uop.is_fence
[146] FIRRTL:197915 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_sfb, io.lsu.brupdate.b2.uop.is_sfb
[147] FIRRTL:197916 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.br_type, io.lsu.brupdate.b2.uop.br_type
[148] FIRRTL:197917 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.br_tag, io.lsu.brupdate.b2.uop.br_tag
[149] FIRRTL:197918 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.br_mask, io.lsu.brupdate.b2.uop.br_mask
[150] FIRRTL:197919 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.dis_col_sel, io.lsu.brupdate.b2.uop.dis_col_sel
[151] FIRRTL:197920 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_p3_bypass_hint, io.lsu.brupdate.b2.uop.iw_p3_bypass_hint
[152] FIRRTL:197921 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_p2_bypass_hint, io.lsu.brupdate.b2.uop.iw_p2_bypass_hint
[153] FIRRTL:197922 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_p1_bypass_hint, io.lsu.brupdate.b2.uop.iw_p1_bypass_hint
[154] FIRRTL:197923 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_p2_speculative_child, io.lsu.brupdate.b2.uop.iw_p2_speculative_child
[155] FIRRTL:197924 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_p1_speculative_child, io.lsu.brupdate.b2.uop.iw_p1_speculative_child
[156] FIRRTL:197925 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_issued_partial_dgen, io.lsu.brupdate.b2.uop.iw_issued_partial_dgen
[157] FIRRTL:197926 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_issued_partial_agen, io.lsu.brupdate.b2.uop.iw_issued_partial_agen
[158] FIRRTL:197927 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iw_issued, io.lsu.brupdate.b2.uop.iw_issued
[159] FIRRTL:197928 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[0], io.lsu.brupdate.b2.uop.fu_code[0]
[160] FIRRTL:197929 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[1], io.lsu.brupdate.b2.uop.fu_code[1]
[161] FIRRTL:197930 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[2], io.lsu.brupdate.b2.uop.fu_code[2]
[162] FIRRTL:197931 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[3], io.lsu.brupdate.b2.uop.fu_code[3]
[163] FIRRTL:197932 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[4], io.lsu.brupdate.b2.uop.fu_code[4]
[164] FIRRTL:197933 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[5], io.lsu.brupdate.b2.uop.fu_code[5]
[165] FIRRTL:197934 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[6], io.lsu.brupdate.b2.uop.fu_code[6]
[166] FIRRTL:197935 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[7], io.lsu.brupdate.b2.uop.fu_code[7]
[167] FIRRTL:197936 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[8], io.lsu.brupdate.b2.uop.fu_code[8]
[168] FIRRTL:197937 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.fu_code[9], io.lsu.brupdate.b2.uop.fu_code[9]
[169] FIRRTL:197938 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iq_type[0], io.lsu.brupdate.b2.uop.iq_type[0]
[170] FIRRTL:197939 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iq_type[1], io.lsu.brupdate.b2.uop.iq_type[1]
[171] FIRRTL:197940 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iq_type[2], io.lsu.brupdate.b2.uop.iq_type[2]
[172] FIRRTL:197941 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.iq_type[3], io.lsu.brupdate.b2.uop.iq_type[3]
[173] FIRRTL:197942 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.debug_pc, io.lsu.brupdate.b2.uop.debug_pc
[174] FIRRTL:197943 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.is_rvc, io.lsu.brupdate.b2.uop.is_rvc
[175] FIRRTL:197944 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.debug_inst, io.lsu.brupdate.b2.uop.debug_inst
[176] FIRRTL:197945 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b2.uop.inst, io.lsu.brupdate.b2.uop.inst
[177] FIRRTL:197946 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b1.mispredict_mask, io.lsu.brupdate.b1.mispredict_mask
[178] FIRRTL:197947 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:462:27 KIND:connect :: connect mshrs.io.brupdate.b1.resolve_mask, io.lsu.brupdate.b1.resolve_mask
[179] FIRRTL:197948 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:463:25 KIND:connect :: connect mshrs.io.exception, io.lsu.exception
[180] FIRRTL:197949 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:464:25 KIND:connect :: connect mshrs.io.rob_pnr_idx, io.lsu.rob_pnr_idx
[181] FIRRTL:197950 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:465:25 KIND:connect :: connect mshrs.io.rob_head_idx, io.lsu.rob_head_idx
[182] FIRRTL:197951 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:469:41 KIND:structural :: inst meta_0 of L1MetadataArray
[183] FIRRTL:197952 SRC:<no-source-locator> KIND:connect :: connect meta_0.clock, clock
[184] FIRRTL:197953 SRC:<no-source-locator> KIND:connect :: connect meta_0.reset, reset
[185] FIRRTL:197954 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:470:28 KIND:structural :: inst metaWriteArb of Arbiter2_L1MetaWriteReq_1
[186] FIRRTL:197955 SRC:<no-source-locator> KIND:connect :: connect metaWriteArb.clock, clock
[187] FIRRTL:197956 SRC:<no-source-locator> KIND:connect :: connect metaWriteArb.reset, reset
[188] FIRRTL:197957 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:472:27 KIND:structural :: inst metaReadArb of Arbiter6_BoomL1MetaReadReq
[189] FIRRTL:197958 SRC:<no-source-locator> KIND:connect :: connect metaReadArb.clock, clock
[190] FIRRTL:197959 SRC:<no-source-locator> KIND:connect :: connect metaReadArb.reset, reset
[191] FIRRTL:197960 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[0].bits.req[0].tag
[192] FIRRTL:197961 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[0].bits.req[0].way_en
[193] FIRRTL:197962 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[0].bits.req[0].idx
[194] FIRRTL:197963 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[0].valid
[195] FIRRTL:197964 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[0].ready
[196] FIRRTL:197965 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[1].bits.req[0].tag
[197] FIRRTL:197966 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[1].bits.req[0].way_en
[198] FIRRTL:197967 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[1].bits.req[0].idx
[199] FIRRTL:197968 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[1].valid
[200] FIRRTL:197969 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[1].ready
[201] FIRRTL:197970 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[2].bits.req[0].tag
[202] FIRRTL:197971 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[2].bits.req[0].way_en
[203] FIRRTL:197972 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[2].bits.req[0].idx
[204] FIRRTL:197973 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[2].valid
[205] FIRRTL:197974 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[2].ready
[206] FIRRTL:197975 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[3].bits.req[0].tag
[207] FIRRTL:197976 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[3].bits.req[0].way_en
[208] FIRRTL:197977 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[3].bits.req[0].idx
[209] FIRRTL:197978 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[3].valid
[210] FIRRTL:197979 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[3].ready
[211] FIRRTL:197980 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[4].bits.req[0].tag
[212] FIRRTL:197981 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[4].bits.req[0].way_en
[213] FIRRTL:197982 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[4].bits.req[0].idx
[214] FIRRTL:197983 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[4].valid
[215] FIRRTL:197984 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[4].ready
[216] FIRRTL:197985 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[5].bits.req[0].tag
[217] FIRRTL:197986 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[5].bits.req[0].way_en
[218] FIRRTL:197987 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[5].bits.req[0].idx
[219] FIRRTL:197988 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[5].valid
[220] FIRRTL:197989 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:476:21 KIND:invalidate :: invalidate metaReadArb.io.in[5].ready
[221] FIRRTL:197990 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _meta_0_io_write_valid_T = and(metaWriteArb.io.out.ready, metaWriteArb.io.out.valid)
[222] FIRRTL:197991 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:478:28 KIND:connect :: connect meta_0.io.write.valid, _meta_0_io_write_valid_T
[223] FIRRTL:197992 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:479:28 KIND:connect :: connect meta_0.io.write.bits.data.tag, metaWriteArb.io.out.bits.data.tag
[224] FIRRTL:197993 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:479:28 KIND:connect :: connect meta_0.io.write.bits.data.coh.state, metaWriteArb.io.out.bits.data.coh.state
[225] FIRRTL:197994 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:479:28 KIND:connect :: connect meta_0.io.write.bits.tag, metaWriteArb.io.out.bits.tag
[226] FIRRTL:197995 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:479:28 KIND:connect :: connect meta_0.io.write.bits.way_en, metaWriteArb.io.out.bits.way_en
[227] FIRRTL:197996 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:479:28 KIND:connect :: connect meta_0.io.write.bits.idx, metaWriteArb.io.out.bits.idx
[228] FIRRTL:197997 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:480:28 KIND:connect :: connect meta_0.io.read.valid, metaReadArb.io.out.valid
[229] FIRRTL:197998 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:481:28 KIND:connect :: connect meta_0.io.read.bits.tag, metaReadArb.io.out.bits.req[0].tag
[230] FIRRTL:197999 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:481:28 KIND:connect :: connect meta_0.io.read.bits.way_en, metaReadArb.io.out.bits.req[0].way_en
[231] FIRRTL:198000 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:481:28 KIND:connect :: connect meta_0.io.read.bits.idx, metaReadArb.io.out.bits.req[0].idx
[232] FIRRTL:198001 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:483:29 KIND:connect :: connect metaReadArb.io.out.ready, meta_0.io.read.ready
[233] FIRRTL:198002 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:484:29 KIND:connect :: connect metaWriteArb.io.out.ready, meta_0.io.write.ready
[234] FIRRTL:198003 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:487:20 KIND:structural :: inst data of BoomDuplicatedDataArray
[235] FIRRTL:198004 SRC:<no-source-locator> KIND:connect :: connect data.clock, clock
[236] FIRRTL:198005 SRC:<no-source-locator> KIND:connect :: connect data.reset, reset
[237] FIRRTL:198006 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:488:28 KIND:structural :: inst dataWriteArb of Arbiter2_L1DataWriteReq_1
[238] FIRRTL:198007 SRC:<no-source-locator> KIND:connect :: connect dataWriteArb.clock, clock
[239] FIRRTL:198008 SRC:<no-source-locator> KIND:connect :: connect dataWriteArb.reset, reset
[240] FIRRTL:198009 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:490:27 KIND:structural :: inst dataReadArb of Arbiter3_BoomL1DataReadReq
[241] FIRRTL:198010 SRC:<no-source-locator> KIND:connect :: connect dataReadArb.clock, clock
[242] FIRRTL:198011 SRC:<no-source-locator> KIND:connect :: connect dataReadArb.reset, reset
[243] FIRRTL:198012 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[0].bits.valid[0]
[244] FIRRTL:198013 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[0].bits.req[0].addr
[245] FIRRTL:198014 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[0].bits.req[0].way_en
[246] FIRRTL:198015 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[0].valid
[247] FIRRTL:198016 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[0].ready
[248] FIRRTL:198017 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[1].bits.valid[0]
[249] FIRRTL:198018 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[1].bits.req[0].addr
[250] FIRRTL:198019 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[1].bits.req[0].way_en
[251] FIRRTL:198020 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[1].valid
[252] FIRRTL:198021 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[1].ready
[253] FIRRTL:198022 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[2].bits.valid[0]
[254] FIRRTL:198023 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[2].bits.req[0].addr
[255] FIRRTL:198024 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[2].bits.req[0].way_en
[256] FIRRTL:198025 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[2].valid
[257] FIRRTL:198026 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:492:21 KIND:invalidate :: invalidate dataReadArb.io.in[2].ready
[258] FIRRTL:198027 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:495:63 KIND:node :: node _data_io_read_0_valid_T = and(dataReadArb.io.out.bits.valid[0], dataReadArb.io.out.valid)
[259] FIRRTL:198028 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:495:27 KIND:connect :: connect data.io.read[0].valid, _data_io_read_0_valid_T
[260] FIRRTL:198029 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:496:27 KIND:connect :: connect data.io.read[0].bits.addr, dataReadArb.io.out.bits.req[0].addr
[261] FIRRTL:198030 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:496:27 KIND:connect :: connect data.io.read[0].bits.way_en, dataReadArb.io.out.bits.req[0].way_en
[262] FIRRTL:198031 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:498:28 KIND:connect :: connect dataReadArb.io.out.ready, UInt<1>(0h1)
[263] FIRRTL:198032 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _data_io_write_valid_T = and(dataWriteArb.io.out.ready, dataWriteArb.io.out.valid)
[264] FIRRTL:198033 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:500:23 KIND:connect :: connect data.io.write.valid, _data_io_write_valid_T
[265] FIRRTL:198034 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:501:23 KIND:connect :: connect data.io.write.bits.data, dataWriteArb.io.out.bits.data
[266] FIRRTL:198035 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:501:23 KIND:connect :: connect data.io.write.bits.wmask, dataWriteArb.io.out.bits.wmask
[267] FIRRTL:198036 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:501:23 KIND:connect :: connect data.io.write.bits.addr, dataWriteArb.io.out.bits.addr
[268] FIRRTL:198037 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:501:23 KIND:connect :: connect data.io.write.bits.way_en, dataWriteArb.io.out.bits.way_en
[269] FIRRTL:198038 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:502:29 KIND:connect :: connect dataWriteArb.io.out.ready, UInt<1>(0h1)
[270] FIRRTL:198039 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:503:53 KIND:node :: node singlePortedDCacheWrite = and(data.io.write.valid, UInt<1>(0h0))
[276] FIRRTL:198045 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:512:53 KIND:node :: node _metaReadArb_io_in_4_valid_T = eq(block_incoming_reqs, UInt<1>(0h0))
[277] FIRRTL:198046 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:512:50 KIND:node :: node _metaReadArb_io_in_4_valid_T_1 = and(io.lsu.req.valid, _metaReadArb_io_in_4_valid_T)
[278] FIRRTL:198047 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:512:30 KIND:connect :: connect metaReadArb.io.in[4].valid, _metaReadArb_io_in_4_valid_T_1
[279] FIRRTL:198048 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:513:53 KIND:node :: node _dataReadArb_io_in_2_valid_T = eq(block_incoming_reqs, UInt<1>(0h0))
[280] FIRRTL:198049 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:513:50 KIND:node :: node _dataReadArb_io_in_2_valid_T_1 = and(io.lsu.req.valid, _dataReadArb_io_in_2_valid_T)
[281] FIRRTL:198050 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:513:30 KIND:connect :: connect dataReadArb.io.in[2].valid, _dataReadArb_io_in_2_valid_T_1
[282] FIRRTL:198051 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:516:77 KIND:node :: node _metaReadArb_io_in_4_bits_req_0_idx_T = shr(io.lsu.req.bits[0].bits.addr, 6)
[283] FIRRTL:198052 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:516:45 KIND:connect :: connect metaReadArb.io.in[4].bits.req[0].idx, _metaReadArb_io_in_4_bits_req_0_idx_T
[284] FIRRTL:198053 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:517:45 KIND:invalidate :: invalidate metaReadArb.io.in[4].bits.req[0].way_en
[285] FIRRTL:198054 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:518:45 KIND:invalidate :: invalidate metaReadArb.io.in[4].bits.req[0].tag
[286] FIRRTL:198055 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:520:45 KIND:connect :: connect dataReadArb.io.in[2].bits.valid[0], io.lsu.req.bits[0].valid
[287] FIRRTL:198056 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:521:45 KIND:connect :: connect dataReadArb.io.in[2].bits.req[0].addr, io.lsu.req.bits[0].bits.addr
[288] FIRRTL:198057 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:522:48 KIND:node :: node _dataReadArb_io_in_2_bits_req_0_way_en_T = not(UInt<4>(0h0))
[289] FIRRTL:198058 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:522:45 KIND:connect :: connect dataReadArb.io.in[2].bits.req[0].way_en, _dataReadArb_io_in_2_bits_req_0_way_en_T
[290] FIRRTL:198059 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:527:24 KIND:wire :: wire replay_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[291] FIRRTL:198060 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].is_hella
[292] FIRRTL:198061 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].data
[293] FIRRTL:198062 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].addr
[294] FIRRTL:198063 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.debug_tsrc
[295] FIRRTL:198064 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.debug_fsrc
[296] FIRRTL:198065 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.bp_xcpt_if
[297] FIRRTL:198066 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.bp_debug_if
[298] FIRRTL:198067 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.xcpt_ma_if
[299] FIRRTL:198068 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.xcpt_ae_if
[300] FIRRTL:198069 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.xcpt_pf_if
[301] FIRRTL:198070 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_typ
[302] FIRRTL:198071 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_rm
[303] FIRRTL:198072 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_val
[304] FIRRTL:198073 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fcn_op
[305] FIRRTL:198074 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fcn_dw
[306] FIRRTL:198075 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.frs3_en
[307] FIRRTL:198076 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.lrs2_rtype
[308] FIRRTL:198077 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.lrs1_rtype
[309] FIRRTL:198078 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.dst_rtype
[310] FIRRTL:198079 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.lrs3
[311] FIRRTL:198080 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.lrs2
[312] FIRRTL:198081 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.lrs1
[313] FIRRTL:198082 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ldst
[314] FIRRTL:198083 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ldst_is_rs1
[315] FIRRTL:198084 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.csr_cmd
[316] FIRRTL:198085 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.flush_on_commit
[317] FIRRTL:198086 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_unique
[318] FIRRTL:198087 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.uses_stq
[319] FIRRTL:198088 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.uses_ldq
[320] FIRRTL:198089 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.mem_signed
[321] FIRRTL:198090 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.mem_size
[322] FIRRTL:198091 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.mem_cmd
[323] FIRRTL:198092 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.exc_cause
[324] FIRRTL:198093 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.exception
[325] FIRRTL:198094 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.stale_pdst
[326] FIRRTL:198095 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ppred_busy
[327] FIRRTL:198096 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs3_busy
[328] FIRRTL:198097 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs2_busy
[329] FIRRTL:198098 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs1_busy
[330] FIRRTL:198099 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ppred
[331] FIRRTL:198100 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs3
[332] FIRRTL:198101 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs2
[333] FIRRTL:198102 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.prs1
[334] FIRRTL:198103 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.pdst
[335] FIRRTL:198104 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.rxq_idx
[336] FIRRTL:198105 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.stq_idx
[337] FIRRTL:198106 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ldq_idx
[338] FIRRTL:198107 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.rob_idx
[339] FIRRTL:198108 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.vec
[340] FIRRTL:198109 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.wflags
[341] FIRRTL:198110 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.sqrt
[342] FIRRTL:198111 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.div
[343] FIRRTL:198112 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.fma
[344] FIRRTL:198113 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.fastpipe
[345] FIRRTL:198114 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.toint
[346] FIRRTL:198115 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.fromint
[347] FIRRTL:198116 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.typeTagOut
[348] FIRRTL:198117 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.typeTagIn
[349] FIRRTL:198118 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.swap23
[350] FIRRTL:198119 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.swap12
[351] FIRRTL:198120 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.ren3
[352] FIRRTL:198121 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.ren2
[353] FIRRTL:198122 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.ren1
[354] FIRRTL:198123 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.wen
[355] FIRRTL:198124 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fp_ctrl.ldst
[356] FIRRTL:198125 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.op2_sel
[357] FIRRTL:198126 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.op1_sel
[358] FIRRTL:198127 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.imm_packed
[359] FIRRTL:198128 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.pimm
[360] FIRRTL:198129 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.imm_sel
[361] FIRRTL:198130 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.imm_rename
[362] FIRRTL:198131 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.taken
[363] FIRRTL:198132 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.pc_lob
[364] FIRRTL:198133 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.edge_inst
[365] FIRRTL:198134 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.ftq_idx
[366] FIRRTL:198135 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_mov
[367] FIRRTL:198136 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_rocc
[368] FIRRTL:198137 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_sys_pc2epc
[369] FIRRTL:198138 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_eret
[370] FIRRTL:198139 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_amo
[371] FIRRTL:198140 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_sfence
[372] FIRRTL:198141 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_fencei
[373] FIRRTL:198142 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_fence
[374] FIRRTL:198143 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_sfb
[375] FIRRTL:198144 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.br_type
[376] FIRRTL:198145 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.br_tag
[377] FIRRTL:198146 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.br_mask
[378] FIRRTL:198147 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.dis_col_sel
[379] FIRRTL:198148 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_p3_bypass_hint
[380] FIRRTL:198149 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_p2_bypass_hint
[381] FIRRTL:198150 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_p1_bypass_hint
[382] FIRRTL:198151 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_p2_speculative_child
[383] FIRRTL:198152 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_p1_speculative_child
[384] FIRRTL:198153 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_issued_partial_dgen
[385] FIRRTL:198154 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_issued_partial_agen
[386] FIRRTL:198155 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iw_issued
[387] FIRRTL:198156 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[0]
[388] FIRRTL:198157 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[1]
[389] FIRRTL:198158 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[2]
[390] FIRRTL:198159 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[3]
[391] FIRRTL:198160 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[4]
[392] FIRRTL:198161 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[5]
[393] FIRRTL:198162 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[6]
[394] FIRRTL:198163 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[7]
[395] FIRRTL:198164 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[8]
[396] FIRRTL:198165 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.fu_code[9]
[397] FIRRTL:198166 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iq_type[0]
[398] FIRRTL:198167 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iq_type[1]
[399] FIRRTL:198168 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iq_type[2]
[400] FIRRTL:198169 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.iq_type[3]
[401] FIRRTL:198170 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.debug_pc
[402] FIRRTL:198171 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.is_rvc
[403] FIRRTL:198172 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.debug_inst
[404] FIRRTL:198173 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:528:28 KIND:invalidate :: invalidate replay_req[0].uop.inst
[405] FIRRTL:198174 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:529:28 KIND:connect :: connect replay_req[0].uop, mshrs.io.replay.bits.uop
[406] FIRRTL:198175 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:530:28 KIND:connect :: connect replay_req[0].addr, mshrs.io.replay.bits.addr
[407] FIRRTL:198176 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:531:28 KIND:connect :: connect replay_req[0].data, mshrs.io.replay.bits.data
[408] FIRRTL:198177 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:532:28 KIND:connect :: connect replay_req[0].is_hella, mshrs.io.replay.bits.is_hella
[409] FIRRTL:198178 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:534:58 KIND:node :: node _mshrs_io_replay_ready_T = and(metaReadArb.io.in[0].ready, dataReadArb.io.in[0].ready)
[410] FIRRTL:198179 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:534:91 KIND:node :: node _mshrs_io_replay_ready_T_1 = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[411] FIRRTL:198180 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:534:88 KIND:node :: node _mshrs_io_replay_ready_T_2 = and(_mshrs_io_replay_ready_T, _mshrs_io_replay_ready_T_1)
[412] FIRRTL:198181 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:534:28 KIND:connect :: connect mshrs.io.replay.ready, _mshrs_io_replay_ready_T_2
[413] FIRRTL:198182 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:537:71 KIND:node :: node _metaReadArb_io_in_0_valid_T = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[414] FIRRTL:198183 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:537:68 KIND:node :: node _metaReadArb_io_in_0_valid_T_1 = and(mshrs.io.replay.valid, _metaReadArb_io_in_0_valid_T)
[415] FIRRTL:198184 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:537:43 KIND:connect :: connect metaReadArb.io.in[0].valid, _metaReadArb_io_in_0_valid_T_1
[416] FIRRTL:198185 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:538:72 KIND:node :: node _metaReadArb_io_in_0_bits_req_0_idx_T = shr(mshrs.io.replay.bits.addr, 6)
[417] FIRRTL:198186 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:538:43 KIND:connect :: connect metaReadArb.io.in[0].bits.req[0].idx, _metaReadArb_io_in_0_bits_req_0_idx_T
[418] FIRRTL:198187 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:539:43 KIND:invalidate :: invalidate metaReadArb.io.in[0].bits.req[0].way_en
[419] FIRRTL:198188 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:540:43 KIND:invalidate :: invalidate metaReadArb.io.in[0].bits.req[0].tag
[420] FIRRTL:198189 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:542:71 KIND:node :: node _dataReadArb_io_in_0_valid_T = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[421] FIRRTL:198190 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:542:68 KIND:node :: node _dataReadArb_io_in_0_valid_T_1 = and(mshrs.io.replay.valid, _dataReadArb_io_in_0_valid_T)
[422] FIRRTL:198191 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:542:43 KIND:connect :: connect dataReadArb.io.in[0].valid, _dataReadArb_io_in_0_valid_T_1
[423] FIRRTL:198192 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:543:43 KIND:connect :: connect dataReadArb.io.in[0].bits.req[0].addr, mshrs.io.replay.bits.addr
[424] FIRRTL:198193 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:544:43 KIND:connect :: connect dataReadArb.io.in[0].bits.req[0].way_en, mshrs.io.replay.bits.way_en
[425] FIRRTL:198194 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire _WIRE : UInt<1>[1]
[426] FIRRTL:198195 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect _WIRE[0], UInt<1>(0h1)
[427] FIRRTL:198196 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:545:43 KIND:connect :: connect dataReadArb.io.in[0].bits.valid[0], _WIRE[0]
[428] FIRRTL:198197 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:549:27 KIND:wire :: wire mshr_read_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[429] FIRRTL:198198 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].is_hella
[430] FIRRTL:198199 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].data
[431] FIRRTL:198200 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].addr
[432] FIRRTL:198201 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.debug_tsrc
[433] FIRRTL:198202 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.debug_fsrc
[434] FIRRTL:198203 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.bp_xcpt_if
[435] FIRRTL:198204 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.bp_debug_if
[436] FIRRTL:198205 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.xcpt_ma_if
[437] FIRRTL:198206 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.xcpt_ae_if
[438] FIRRTL:198207 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.xcpt_pf_if
[439] FIRRTL:198208 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_typ
[440] FIRRTL:198209 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_rm
[441] FIRRTL:198210 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_val
[442] FIRRTL:198211 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fcn_op
[443] FIRRTL:198212 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fcn_dw
[444] FIRRTL:198213 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.frs3_en
[445] FIRRTL:198214 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.lrs2_rtype
[446] FIRRTL:198215 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.lrs1_rtype
[447] FIRRTL:198216 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.dst_rtype
[448] FIRRTL:198217 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.lrs3
[449] FIRRTL:198218 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.lrs2
[450] FIRRTL:198219 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.lrs1
[451] FIRRTL:198220 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ldst
[452] FIRRTL:198221 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ldst_is_rs1
[453] FIRRTL:198222 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.csr_cmd
[454] FIRRTL:198223 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.flush_on_commit
[455] FIRRTL:198224 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_unique
[456] FIRRTL:198225 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.uses_stq
[457] FIRRTL:198226 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.uses_ldq
[458] FIRRTL:198227 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.mem_signed
[459] FIRRTL:198228 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.mem_size
[460] FIRRTL:198229 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.mem_cmd
[461] FIRRTL:198230 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.exc_cause
[462] FIRRTL:198231 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.exception
[463] FIRRTL:198232 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.stale_pdst
[464] FIRRTL:198233 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ppred_busy
[465] FIRRTL:198234 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs3_busy
[466] FIRRTL:198235 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs2_busy
[467] FIRRTL:198236 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs1_busy
[468] FIRRTL:198237 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ppred
[469] FIRRTL:198238 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs3
[470] FIRRTL:198239 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs2
[471] FIRRTL:198240 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.prs1
[472] FIRRTL:198241 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.pdst
[473] FIRRTL:198242 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.rxq_idx
[474] FIRRTL:198243 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.stq_idx
[475] FIRRTL:198244 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ldq_idx
[476] FIRRTL:198245 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.rob_idx
[477] FIRRTL:198246 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.vec
[478] FIRRTL:198247 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.wflags
[479] FIRRTL:198248 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.sqrt
[480] FIRRTL:198249 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.div
[481] FIRRTL:198250 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.fma
[482] FIRRTL:198251 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.fastpipe
[483] FIRRTL:198252 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.toint
[484] FIRRTL:198253 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.fromint
[485] FIRRTL:198254 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.typeTagOut
[486] FIRRTL:198255 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.typeTagIn
[487] FIRRTL:198256 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.swap23
[488] FIRRTL:198257 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.swap12
[489] FIRRTL:198258 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.ren3
[490] FIRRTL:198259 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.ren2
[491] FIRRTL:198260 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.ren1
[492] FIRRTL:198261 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.wen
[493] FIRRTL:198262 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fp_ctrl.ldst
[494] FIRRTL:198263 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.op2_sel
[495] FIRRTL:198264 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.op1_sel
[496] FIRRTL:198265 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.imm_packed
[497] FIRRTL:198266 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.pimm
[498] FIRRTL:198267 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.imm_sel
[499] FIRRTL:198268 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.imm_rename
[500] FIRRTL:198269 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.taken
[501] FIRRTL:198270 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.pc_lob
[502] FIRRTL:198271 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.edge_inst
[503] FIRRTL:198272 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.ftq_idx
[504] FIRRTL:198273 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_mov
[505] FIRRTL:198274 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_rocc
[506] FIRRTL:198275 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_sys_pc2epc
[507] FIRRTL:198276 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_eret
[508] FIRRTL:198277 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_amo
[509] FIRRTL:198278 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_sfence
[510] FIRRTL:198279 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_fencei
[511] FIRRTL:198280 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_fence
[512] FIRRTL:198281 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_sfb
[513] FIRRTL:198282 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.br_type
[514] FIRRTL:198283 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.br_tag
[515] FIRRTL:198284 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.br_mask
[516] FIRRTL:198285 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.dis_col_sel
[517] FIRRTL:198286 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_p3_bypass_hint
[518] FIRRTL:198287 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_p2_bypass_hint
[519] FIRRTL:198288 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_p1_bypass_hint
[520] FIRRTL:198289 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_p2_speculative_child
[521] FIRRTL:198290 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_p1_speculative_child
[522] FIRRTL:198291 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_issued_partial_dgen
[523] FIRRTL:198292 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_issued_partial_agen
[524] FIRRTL:198293 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iw_issued
[525] FIRRTL:198294 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[0]
[526] FIRRTL:198295 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[1]
[527] FIRRTL:198296 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[2]
[528] FIRRTL:198297 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[3]
[529] FIRRTL:198298 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[4]
[530] FIRRTL:198299 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[5]
[531] FIRRTL:198300 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[6]
[532] FIRRTL:198301 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[7]
[533] FIRRTL:198302 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[8]
[534] FIRRTL:198303 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.fu_code[9]
[535] FIRRTL:198304 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iq_type[0]
[536] FIRRTL:198305 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iq_type[1]
[537] FIRRTL:198306 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iq_type[2]
[538] FIRRTL:198307 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.iq_type[3]
[539] FIRRTL:198308 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.debug_pc
[540] FIRRTL:198309 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.is_rvc
[541] FIRRTL:198310 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.debug_inst
[542] FIRRTL:198311 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:550:29 KIND:invalidate :: invalidate mshr_read_req[0].uop.inst
[543] FIRRTL:198312 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:wire :: wire _mshr_read_req_0_uop_WIRE : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}
[544] FIRRTL:198313 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.debug_tsrc, UInt<3>(0h0)
[545] FIRRTL:198314 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.debug_fsrc, UInt<3>(0h0)
[546] FIRRTL:198315 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.bp_xcpt_if, UInt<1>(0h0)
[547] FIRRTL:198316 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.bp_debug_if, UInt<1>(0h0)
[548] FIRRTL:198317 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.xcpt_ma_if, UInt<1>(0h0)
[549] FIRRTL:198318 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.xcpt_ae_if, UInt<1>(0h0)
[550] FIRRTL:198319 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.xcpt_pf_if, UInt<1>(0h0)
[551] FIRRTL:198320 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_typ, UInt<2>(0h0)
[552] FIRRTL:198321 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_rm, UInt<3>(0h0)
[553] FIRRTL:198322 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_val, UInt<1>(0h0)
[554] FIRRTL:198323 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fcn_op, UInt<5>(0h0)
[555] FIRRTL:198324 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fcn_dw, UInt<1>(0h0)
[556] FIRRTL:198325 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.frs3_en, UInt<1>(0h0)
[557] FIRRTL:198326 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.lrs2_rtype, UInt<2>(0h0)
[558] FIRRTL:198327 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.lrs1_rtype, UInt<2>(0h0)
[559] FIRRTL:198328 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.dst_rtype, UInt<2>(0h0)
[560] FIRRTL:198329 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.lrs3, UInt<6>(0h0)
[561] FIRRTL:198330 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.lrs2, UInt<6>(0h0)
[562] FIRRTL:198331 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.lrs1, UInt<6>(0h0)
[563] FIRRTL:198332 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ldst, UInt<6>(0h0)
[564] FIRRTL:198333 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ldst_is_rs1, UInt<1>(0h0)
[565] FIRRTL:198334 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.csr_cmd, UInt<3>(0h0)
[566] FIRRTL:198335 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.flush_on_commit, UInt<1>(0h0)
[567] FIRRTL:198336 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_unique, UInt<1>(0h0)
[568] FIRRTL:198337 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.uses_stq, UInt<1>(0h0)
[569] FIRRTL:198338 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.uses_ldq, UInt<1>(0h0)
[570] FIRRTL:198339 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.mem_signed, UInt<1>(0h0)
[571] FIRRTL:198340 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.mem_size, UInt<2>(0h0)
[572] FIRRTL:198341 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.mem_cmd, UInt<5>(0h0)
[573] FIRRTL:198342 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.exc_cause, UInt<64>(0h0)
[574] FIRRTL:198343 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.exception, UInt<1>(0h0)
[575] FIRRTL:198344 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.stale_pdst, UInt<6>(0h0)
[576] FIRRTL:198345 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ppred_busy, UInt<1>(0h0)
[577] FIRRTL:198346 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs3_busy, UInt<1>(0h0)
[578] FIRRTL:198347 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs2_busy, UInt<1>(0h0)
[579] FIRRTL:198348 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs1_busy, UInt<1>(0h0)
[580] FIRRTL:198349 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ppred, UInt<4>(0h0)
[581] FIRRTL:198350 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs3, UInt<6>(0h0)
[582] FIRRTL:198351 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs2, UInt<6>(0h0)
[583] FIRRTL:198352 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.prs1, UInt<6>(0h0)
[584] FIRRTL:198353 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.pdst, UInt<6>(0h0)
[585] FIRRTL:198354 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.rxq_idx, UInt<2>(0h0)
[586] FIRRTL:198355 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.stq_idx, UInt<4>(0h0)
[587] FIRRTL:198356 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ldq_idx, UInt<4>(0h0)
[588] FIRRTL:198357 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.rob_idx, UInt<5>(0h0)
[589] FIRRTL:198358 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.vec, UInt<1>(0h0)
[590] FIRRTL:198359 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.wflags, UInt<1>(0h0)
[591] FIRRTL:198360 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.sqrt, UInt<1>(0h0)
[592] FIRRTL:198361 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.div, UInt<1>(0h0)
[593] FIRRTL:198362 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.fma, UInt<1>(0h0)
[594] FIRRTL:198363 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.fastpipe, UInt<1>(0h0)
[595] FIRRTL:198364 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.toint, UInt<1>(0h0)
[596] FIRRTL:198365 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.fromint, UInt<1>(0h0)
[597] FIRRTL:198366 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.typeTagOut, UInt<2>(0h0)
[598] FIRRTL:198367 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.typeTagIn, UInt<2>(0h0)
[599] FIRRTL:198368 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.swap23, UInt<1>(0h0)
[600] FIRRTL:198369 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.swap12, UInt<1>(0h0)
[601] FIRRTL:198370 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.ren3, UInt<1>(0h0)
[602] FIRRTL:198371 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.ren2, UInt<1>(0h0)
[603] FIRRTL:198372 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.ren1, UInt<1>(0h0)
[604] FIRRTL:198373 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.wen, UInt<1>(0h0)
[605] FIRRTL:198374 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fp_ctrl.ldst, UInt<1>(0h0)
[606] FIRRTL:198375 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.op2_sel, UInt<3>(0h0)
[607] FIRRTL:198376 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.op1_sel, UInt<2>(0h0)
[608] FIRRTL:198377 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.imm_packed, UInt<20>(0h0)
[609] FIRRTL:198378 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.pimm, UInt<5>(0h0)
[610] FIRRTL:198379 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.imm_sel, UInt<3>(0h0)
[611] FIRRTL:198380 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.imm_rename, UInt<1>(0h0)
[612] FIRRTL:198381 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.taken, UInt<1>(0h0)
[613] FIRRTL:198382 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.pc_lob, UInt<6>(0h0)
[614] FIRRTL:198383 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.edge_inst, UInt<1>(0h0)
[615] FIRRTL:198384 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.ftq_idx, UInt<4>(0h0)
[616] FIRRTL:198385 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_mov, UInt<1>(0h0)
[617] FIRRTL:198386 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_rocc, UInt<1>(0h0)
[618] FIRRTL:198387 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_sys_pc2epc, UInt<1>(0h0)
[619] FIRRTL:198388 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_eret, UInt<1>(0h0)
[620] FIRRTL:198389 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_amo, UInt<1>(0h0)
[621] FIRRTL:198390 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_sfence, UInt<1>(0h0)
[622] FIRRTL:198391 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_fencei, UInt<1>(0h0)
[623] FIRRTL:198392 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_fence, UInt<1>(0h0)
[624] FIRRTL:198393 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_sfb, UInt<1>(0h0)
[625] FIRRTL:198394 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.br_type, UInt<4>(0h0)
[626] FIRRTL:198395 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.br_tag, UInt<3>(0h0)
[627] FIRRTL:198396 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.br_mask, UInt<8>(0h0)
[628] FIRRTL:198397 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.dis_col_sel, UInt<1>(0h0)
[629] FIRRTL:198398 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_p3_bypass_hint, UInt<1>(0h0)
[630] FIRRTL:198399 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_p2_bypass_hint, UInt<1>(0h0)
[631] FIRRTL:198400 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_p1_bypass_hint, UInt<1>(0h0)
[632] FIRRTL:198401 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_p2_speculative_child, UInt<1>(0h0)
[633] FIRRTL:198402 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_p1_speculative_child, UInt<1>(0h0)
[634] FIRRTL:198403 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_issued_partial_dgen, UInt<1>(0h0)
[635] FIRRTL:198404 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_issued_partial_agen, UInt<1>(0h0)
[636] FIRRTL:198405 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iw_issued, UInt<1>(0h0)
[637] FIRRTL:198406 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[0], UInt<1>(0h0)
[638] FIRRTL:198407 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[1], UInt<1>(0h0)
[639] FIRRTL:198408 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[2], UInt<1>(0h0)
[640] FIRRTL:198409 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[3], UInt<1>(0h0)
[641] FIRRTL:198410 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[4], UInt<1>(0h0)
[642] FIRRTL:198411 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[5], UInt<1>(0h0)
[643] FIRRTL:198412 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[6], UInt<1>(0h0)
[644] FIRRTL:198413 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[7], UInt<1>(0h0)
[645] FIRRTL:198414 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[8], UInt<1>(0h0)
[646] FIRRTL:198415 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.fu_code[9], UInt<1>(0h0)
[647] FIRRTL:198416 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iq_type[0], UInt<1>(0h0)
[648] FIRRTL:198417 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iq_type[1], UInt<1>(0h0)
[649] FIRRTL:198418 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iq_type[2], UInt<1>(0h0)
[650] FIRRTL:198419 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.iq_type[3], UInt<1>(0h0)
[651] FIRRTL:198420 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.debug_pc, UInt<40>(0h0)
[652] FIRRTL:198421 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.is_rvc, UInt<1>(0h0)
[653] FIRRTL:198422 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.debug_inst, UInt<32>(0h0)
[654] FIRRTL:198423 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _mshr_read_req_0_uop_WIRE.inst, UInt<32>(0h0)
[655] FIRRTL:198424 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:551:29 KIND:connect :: connect mshr_read_req[0].uop, _mshr_read_req_0_uop_WIRE
[656] FIRRTL:198425 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:552:35 KIND:node :: node _mshr_read_req_0_addr_T = cat(mshrs.io.meta_read.bits.tag, mshrs.io.meta_read.bits.idx)
[657] FIRRTL:198426 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:552:94 KIND:node :: node _mshr_read_req_0_addr_T_1 = shl(_mshr_read_req_0_addr_T, 6)
[658] FIRRTL:198427 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:552:29 KIND:connect :: connect mshr_read_req[0].addr, _mshr_read_req_0_addr_T_1
[659] FIRRTL:198428 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:553:29 KIND:invalidate :: invalidate mshr_read_req[0].data
[660] FIRRTL:198429 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:554:29 KIND:connect :: connect mshr_read_req[0].is_hella, UInt<1>(0h0)
[661] FIRRTL:198430 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:555:36 KIND:connect :: connect metaReadArb.io.in[3].valid, mshrs.io.meta_read.valid
[662] FIRRTL:198431 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:556:36 KIND:connect :: connect metaReadArb.io.in[3].bits.req[0].tag, mshrs.io.meta_read.bits.tag
[663] FIRRTL:198432 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:556:36 KIND:connect :: connect metaReadArb.io.in[3].bits.req[0].way_en, mshrs.io.meta_read.bits.way_en
[664] FIRRTL:198433 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:556:36 KIND:connect :: connect metaReadArb.io.in[3].bits.req[0].idx, mshrs.io.meta_read.bits.idx
[665] FIRRTL:198434 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:557:36 KIND:connect :: connect mshrs.io.meta_read.ready, metaReadArb.io.in[3].ready
[666] FIRRTL:198435 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _wb_fire_T = and(wb.io.meta_read.ready, wb.io.meta_read.valid)
[667] FIRRTL:198436 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _wb_fire_T_1 = and(wb.io.data_req.ready, wb.io.data_req.valid)
[668] FIRRTL:198437 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:563:38 KIND:node :: node wb_fire = and(_wb_fire_T, _wb_fire_T_1)
[669] FIRRTL:198438 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:564:20 KIND:wire :: wire wb_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[670] FIRRTL:198439 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].is_hella
[671] FIRRTL:198440 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].data
[672] FIRRTL:198441 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].addr
[673] FIRRTL:198442 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.debug_tsrc
[674] FIRRTL:198443 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.debug_fsrc
[675] FIRRTL:198444 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.bp_xcpt_if
[676] FIRRTL:198445 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.bp_debug_if
[677] FIRRTL:198446 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.xcpt_ma_if
[678] FIRRTL:198447 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.xcpt_ae_if
[679] FIRRTL:198448 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.xcpt_pf_if
[680] FIRRTL:198449 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_typ
[681] FIRRTL:198450 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_rm
[682] FIRRTL:198451 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_val
[683] FIRRTL:198452 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fcn_op
[684] FIRRTL:198453 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fcn_dw
[685] FIRRTL:198454 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.frs3_en
[686] FIRRTL:198455 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.lrs2_rtype
[687] FIRRTL:198456 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.lrs1_rtype
[688] FIRRTL:198457 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.dst_rtype
[689] FIRRTL:198458 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.lrs3
[690] FIRRTL:198459 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.lrs2
[691] FIRRTL:198460 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.lrs1
[692] FIRRTL:198461 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ldst
[693] FIRRTL:198462 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ldst_is_rs1
[694] FIRRTL:198463 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.csr_cmd
[695] FIRRTL:198464 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.flush_on_commit
[696] FIRRTL:198465 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_unique
[697] FIRRTL:198466 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.uses_stq
[698] FIRRTL:198467 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.uses_ldq
[699] FIRRTL:198468 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.mem_signed
[700] FIRRTL:198469 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.mem_size
[701] FIRRTL:198470 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.mem_cmd
[702] FIRRTL:198471 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.exc_cause
[703] FIRRTL:198472 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.exception
[704] FIRRTL:198473 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.stale_pdst
[705] FIRRTL:198474 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ppred_busy
[706] FIRRTL:198475 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs3_busy
[707] FIRRTL:198476 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs2_busy
[708] FIRRTL:198477 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs1_busy
[709] FIRRTL:198478 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ppred
[710] FIRRTL:198479 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs3
[711] FIRRTL:198480 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs2
[712] FIRRTL:198481 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.prs1
[713] FIRRTL:198482 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.pdst
[714] FIRRTL:198483 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.rxq_idx
[715] FIRRTL:198484 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.stq_idx
[716] FIRRTL:198485 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ldq_idx
[717] FIRRTL:198486 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.rob_idx
[718] FIRRTL:198487 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.vec
[719] FIRRTL:198488 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.wflags
[720] FIRRTL:198489 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.sqrt
[721] FIRRTL:198490 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.div
[722] FIRRTL:198491 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.fma
[723] FIRRTL:198492 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.fastpipe
[724] FIRRTL:198493 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.toint
[725] FIRRTL:198494 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.fromint
[726] FIRRTL:198495 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.typeTagOut
[727] FIRRTL:198496 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.typeTagIn
[728] FIRRTL:198497 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.swap23
[729] FIRRTL:198498 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.swap12
[730] FIRRTL:198499 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.ren3
[731] FIRRTL:198500 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.ren2
[732] FIRRTL:198501 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.ren1
[733] FIRRTL:198502 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.wen
[734] FIRRTL:198503 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fp_ctrl.ldst
[735] FIRRTL:198504 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.op2_sel
[736] FIRRTL:198505 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.op1_sel
[737] FIRRTL:198506 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.imm_packed
[738] FIRRTL:198507 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.pimm
[739] FIRRTL:198508 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.imm_sel
[740] FIRRTL:198509 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.imm_rename
[741] FIRRTL:198510 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.taken
[742] FIRRTL:198511 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.pc_lob
[743] FIRRTL:198512 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.edge_inst
[744] FIRRTL:198513 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.ftq_idx
[745] FIRRTL:198514 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_mov
[746] FIRRTL:198515 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_rocc
[747] FIRRTL:198516 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_sys_pc2epc
[748] FIRRTL:198517 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_eret
[749] FIRRTL:198518 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_amo
[750] FIRRTL:198519 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_sfence
[751] FIRRTL:198520 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_fencei
[752] FIRRTL:198521 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_fence
[753] FIRRTL:198522 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_sfb
[754] FIRRTL:198523 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.br_type
[755] FIRRTL:198524 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.br_tag
[756] FIRRTL:198525 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.br_mask
[757] FIRRTL:198526 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.dis_col_sel
[758] FIRRTL:198527 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_p3_bypass_hint
[759] FIRRTL:198528 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_p2_bypass_hint
[760] FIRRTL:198529 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_p1_bypass_hint
[761] FIRRTL:198530 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_p2_speculative_child
[762] FIRRTL:198531 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_p1_speculative_child
[763] FIRRTL:198532 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_issued_partial_dgen
[764] FIRRTL:198533 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_issued_partial_agen
[765] FIRRTL:198534 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iw_issued
[766] FIRRTL:198535 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[0]
[767] FIRRTL:198536 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[1]
[768] FIRRTL:198537 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[2]
[769] FIRRTL:198538 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[3]
[770] FIRRTL:198539 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[4]
[771] FIRRTL:198540 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[5]
[772] FIRRTL:198541 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[6]
[773] FIRRTL:198542 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[7]
[774] FIRRTL:198543 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[8]
[775] FIRRTL:198544 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.fu_code[9]
[776] FIRRTL:198545 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iq_type[0]
[777] FIRRTL:198546 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iq_type[1]
[778] FIRRTL:198547 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iq_type[2]
[779] FIRRTL:198548 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.iq_type[3]
[780] FIRRTL:198549 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.debug_pc
[781] FIRRTL:198550 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.is_rvc
[782] FIRRTL:198551 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.debug_inst
[783] FIRRTL:198552 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:565:22 KIND:invalidate :: invalidate wb_req[0].uop.inst
[784] FIRRTL:198553 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:wire :: wire _wb_req_0_uop_WIRE : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}
[785] FIRRTL:198554 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.debug_tsrc, UInt<3>(0h0)
[786] FIRRTL:198555 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.debug_fsrc, UInt<3>(0h0)
[787] FIRRTL:198556 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.bp_xcpt_if, UInt<1>(0h0)
[788] FIRRTL:198557 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.bp_debug_if, UInt<1>(0h0)
[789] FIRRTL:198558 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.xcpt_ma_if, UInt<1>(0h0)
[790] FIRRTL:198559 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.xcpt_ae_if, UInt<1>(0h0)
[791] FIRRTL:198560 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.xcpt_pf_if, UInt<1>(0h0)
[792] FIRRTL:198561 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_typ, UInt<2>(0h0)
[793] FIRRTL:198562 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_rm, UInt<3>(0h0)
[794] FIRRTL:198563 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_val, UInt<1>(0h0)
[795] FIRRTL:198564 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fcn_op, UInt<5>(0h0)
[796] FIRRTL:198565 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fcn_dw, UInt<1>(0h0)
[797] FIRRTL:198566 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.frs3_en, UInt<1>(0h0)
[798] FIRRTL:198567 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.lrs2_rtype, UInt<2>(0h0)
[799] FIRRTL:198568 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.lrs1_rtype, UInt<2>(0h0)
[800] FIRRTL:198569 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.dst_rtype, UInt<2>(0h0)
[801] FIRRTL:198570 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.lrs3, UInt<6>(0h0)
[802] FIRRTL:198571 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.lrs2, UInt<6>(0h0)
[803] FIRRTL:198572 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.lrs1, UInt<6>(0h0)
[804] FIRRTL:198573 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ldst, UInt<6>(0h0)
[805] FIRRTL:198574 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ldst_is_rs1, UInt<1>(0h0)
[806] FIRRTL:198575 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.csr_cmd, UInt<3>(0h0)
[807] FIRRTL:198576 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.flush_on_commit, UInt<1>(0h0)
[808] FIRRTL:198577 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_unique, UInt<1>(0h0)
[809] FIRRTL:198578 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.uses_stq, UInt<1>(0h0)
[810] FIRRTL:198579 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.uses_ldq, UInt<1>(0h0)
[811] FIRRTL:198580 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.mem_signed, UInt<1>(0h0)
[812] FIRRTL:198581 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.mem_size, UInt<2>(0h0)
[813] FIRRTL:198582 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.mem_cmd, UInt<5>(0h0)
[814] FIRRTL:198583 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.exc_cause, UInt<64>(0h0)
[815] FIRRTL:198584 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.exception, UInt<1>(0h0)
[816] FIRRTL:198585 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.stale_pdst, UInt<6>(0h0)
[817] FIRRTL:198586 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ppred_busy, UInt<1>(0h0)
[818] FIRRTL:198587 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs3_busy, UInt<1>(0h0)
[819] FIRRTL:198588 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs2_busy, UInt<1>(0h0)
[820] FIRRTL:198589 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs1_busy, UInt<1>(0h0)
[821] FIRRTL:198590 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ppred, UInt<4>(0h0)
[822] FIRRTL:198591 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs3, UInt<6>(0h0)
[823] FIRRTL:198592 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs2, UInt<6>(0h0)
[824] FIRRTL:198593 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.prs1, UInt<6>(0h0)
[825] FIRRTL:198594 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.pdst, UInt<6>(0h0)
[826] FIRRTL:198595 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.rxq_idx, UInt<2>(0h0)
[827] FIRRTL:198596 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.stq_idx, UInt<4>(0h0)
[828] FIRRTL:198597 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ldq_idx, UInt<4>(0h0)
[829] FIRRTL:198598 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.rob_idx, UInt<5>(0h0)
[830] FIRRTL:198599 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.vec, UInt<1>(0h0)
[831] FIRRTL:198600 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.wflags, UInt<1>(0h0)
[832] FIRRTL:198601 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.sqrt, UInt<1>(0h0)
[833] FIRRTL:198602 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.div, UInt<1>(0h0)
[834] FIRRTL:198603 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.fma, UInt<1>(0h0)
[835] FIRRTL:198604 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.fastpipe, UInt<1>(0h0)
[836] FIRRTL:198605 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.toint, UInt<1>(0h0)
[837] FIRRTL:198606 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.fromint, UInt<1>(0h0)
[838] FIRRTL:198607 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.typeTagOut, UInt<2>(0h0)
[839] FIRRTL:198608 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.typeTagIn, UInt<2>(0h0)
[840] FIRRTL:198609 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.swap23, UInt<1>(0h0)
[841] FIRRTL:198610 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.swap12, UInt<1>(0h0)
[842] FIRRTL:198611 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.ren3, UInt<1>(0h0)
[843] FIRRTL:198612 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.ren2, UInt<1>(0h0)
[844] FIRRTL:198613 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.ren1, UInt<1>(0h0)
[845] FIRRTL:198614 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.wen, UInt<1>(0h0)
[846] FIRRTL:198615 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fp_ctrl.ldst, UInt<1>(0h0)
[847] FIRRTL:198616 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.op2_sel, UInt<3>(0h0)
[848] FIRRTL:198617 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.op1_sel, UInt<2>(0h0)
[849] FIRRTL:198618 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.imm_packed, UInt<20>(0h0)
[850] FIRRTL:198619 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.pimm, UInt<5>(0h0)
[851] FIRRTL:198620 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.imm_sel, UInt<3>(0h0)
[852] FIRRTL:198621 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.imm_rename, UInt<1>(0h0)
[853] FIRRTL:198622 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.taken, UInt<1>(0h0)
[854] FIRRTL:198623 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.pc_lob, UInt<6>(0h0)
[855] FIRRTL:198624 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.edge_inst, UInt<1>(0h0)
[856] FIRRTL:198625 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.ftq_idx, UInt<4>(0h0)
[857] FIRRTL:198626 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_mov, UInt<1>(0h0)
[858] FIRRTL:198627 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_rocc, UInt<1>(0h0)
[859] FIRRTL:198628 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_sys_pc2epc, UInt<1>(0h0)
[860] FIRRTL:198629 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_eret, UInt<1>(0h0)
[861] FIRRTL:198630 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_amo, UInt<1>(0h0)
[862] FIRRTL:198631 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_sfence, UInt<1>(0h0)
[863] FIRRTL:198632 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_fencei, UInt<1>(0h0)
[864] FIRRTL:198633 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_fence, UInt<1>(0h0)
[865] FIRRTL:198634 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_sfb, UInt<1>(0h0)
[866] FIRRTL:198635 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.br_type, UInt<4>(0h0)
[867] FIRRTL:198636 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.br_tag, UInt<3>(0h0)
[868] FIRRTL:198637 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.br_mask, UInt<8>(0h0)
[869] FIRRTL:198638 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.dis_col_sel, UInt<1>(0h0)
[870] FIRRTL:198639 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_p3_bypass_hint, UInt<1>(0h0)
[871] FIRRTL:198640 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_p2_bypass_hint, UInt<1>(0h0)
[872] FIRRTL:198641 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_p1_bypass_hint, UInt<1>(0h0)
[873] FIRRTL:198642 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_p2_speculative_child, UInt<1>(0h0)
[874] FIRRTL:198643 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_p1_speculative_child, UInt<1>(0h0)
[875] FIRRTL:198644 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_issued_partial_dgen, UInt<1>(0h0)
[876] FIRRTL:198645 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_issued_partial_agen, UInt<1>(0h0)
[877] FIRRTL:198646 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iw_issued, UInt<1>(0h0)
[878] FIRRTL:198647 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[0], UInt<1>(0h0)
[879] FIRRTL:198648 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[1], UInt<1>(0h0)
[880] FIRRTL:198649 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[2], UInt<1>(0h0)
[881] FIRRTL:198650 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[3], UInt<1>(0h0)
[882] FIRRTL:198651 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[4], UInt<1>(0h0)
[883] FIRRTL:198652 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[5], UInt<1>(0h0)
[884] FIRRTL:198653 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[6], UInt<1>(0h0)
[885] FIRRTL:198654 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[7], UInt<1>(0h0)
[886] FIRRTL:198655 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[8], UInt<1>(0h0)
[887] FIRRTL:198656 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.fu_code[9], UInt<1>(0h0)
[888] FIRRTL:198657 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iq_type[0], UInt<1>(0h0)
[889] FIRRTL:198658 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iq_type[1], UInt<1>(0h0)
[890] FIRRTL:198659 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iq_type[2], UInt<1>(0h0)
[891] FIRRTL:198660 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.iq_type[3], UInt<1>(0h0)
[892] FIRRTL:198661 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.debug_pc, UInt<40>(0h0)
[893] FIRRTL:198662 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.is_rvc, UInt<1>(0h0)
[894] FIRRTL:198663 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.debug_inst, UInt<32>(0h0)
[895] FIRRTL:198664 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _wb_req_0_uop_WIRE.inst, UInt<32>(0h0)
[896] FIRRTL:198665 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:566:22 KIND:connect :: connect wb_req[0].uop, _wb_req_0_uop_WIRE
[897] FIRRTL:198666 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:567:28 KIND:node :: node _wb_req_0_addr_T = cat(wb.io.meta_read.bits.tag, wb.io.data_req.bits.addr)
[898] FIRRTL:198667 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:567:22 KIND:connect :: connect wb_req[0].addr, _wb_req_0_addr_T
[899] FIRRTL:198668 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:568:22 KIND:invalidate :: invalidate wb_req[0].data
[900] FIRRTL:198669 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:569:22 KIND:connect :: connect wb_req[0].is_hella, UInt<1>(0h0)
[901] FIRRTL:198670 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:573:65 KIND:node :: node _metaReadArb_io_in_2_valid_T = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[902] FIRRTL:198671 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:573:62 KIND:node :: node _metaReadArb_io_in_2_valid_T_1 = and(wb.io.meta_read.valid, _metaReadArb_io_in_2_valid_T)
[903] FIRRTL:198672 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:573:37 KIND:connect :: connect metaReadArb.io.in[2].valid, _metaReadArb_io_in_2_valid_T_1
[904] FIRRTL:198673 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:574:37 KIND:connect :: connect metaReadArb.io.in[2].bits.req[0].tag, wb.io.meta_read.bits.tag
[905] FIRRTL:198674 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:574:37 KIND:connect :: connect metaReadArb.io.in[2].bits.req[0].way_en, wb.io.meta_read.bits.way_en
[906] FIRRTL:198675 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:574:37 KIND:connect :: connect metaReadArb.io.in[2].bits.req[0].idx, wb.io.meta_read.bits.idx
[907] FIRRTL:198676 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:575:55 KIND:node :: node _wb_io_meta_read_ready_T = and(metaReadArb.io.in[2].ready, dataReadArb.io.in[1].ready)
[908] FIRRTL:198677 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:575:88 KIND:node :: node _wb_io_meta_read_ready_T_1 = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[909] FIRRTL:198678 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:575:85 KIND:node :: node _wb_io_meta_read_ready_T_2 = and(_wb_io_meta_read_ready_T, _wb_io_meta_read_ready_T_1)
[910] FIRRTL:198679 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:575:25 KIND:connect :: connect wb.io.meta_read.ready, _wb_io_meta_read_ready_T_2
[911] FIRRTL:198680 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:577:64 KIND:node :: node _dataReadArb_io_in_1_valid_T = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[912] FIRRTL:198681 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:577:61 KIND:node :: node _dataReadArb_io_in_1_valid_T_1 = and(wb.io.data_req.valid, _dataReadArb_io_in_1_valid_T)
[913] FIRRTL:198682 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:577:37 KIND:connect :: connect dataReadArb.io.in[1].valid, _dataReadArb_io_in_1_valid_T_1
[914] FIRRTL:198683 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:578:37 KIND:connect :: connect dataReadArb.io.in[1].bits.req[0].addr, wb.io.data_req.bits.addr
[915] FIRRTL:198684 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:578:37 KIND:connect :: connect dataReadArb.io.in[1].bits.req[0].way_en, wb.io.data_req.bits.way_en
[916] FIRRTL:198685 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire _WIRE_1 : UInt<1>[1]
[917] FIRRTL:198686 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect _WIRE_1[0], UInt<1>(0h1)
[918] FIRRTL:198687 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:579:37 KIND:connect :: connect dataReadArb.io.in[1].bits.valid[0], _WIRE_1[0]
[919] FIRRTL:198688 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:580:55 KIND:node :: node _wb_io_data_req_ready_T = and(metaReadArb.io.in[2].ready, dataReadArb.io.in[1].ready)
[920] FIRRTL:198689 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:580:88 KIND:node :: node _wb_io_data_req_ready_T_1 = eq(singlePortedDCacheWrite, UInt<1>(0h0))
[921] FIRRTL:198690 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:580:85 KIND:node :: node _wb_io_data_req_ready_T_2 = and(_wb_io_data_req_ready_T, _wb_io_data_req_ready_T_1)
[922] FIRRTL:198691 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:580:25 KIND:connect :: connect wb.io.data_req.ready, _wb_io_data_req_ready_T_2
[923] FIRRTL:198692 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T = and(wb.io.meta_read.ready, wb.io.meta_read.valid)
[924] FIRRTL:198693 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_1 = and(wb.io.data_req.ready, wb.io.data_req.valid)
[925] FIRRTL:198694 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:33 KIND:node :: node _T_2 = xor(_T, _T_1)
[926] FIRRTL:198695 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:10 KIND:node :: node _T_3 = eq(_T_2, UInt<1>(0h0))
[927] FIRRTL:198696 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:node :: node _T_4 = asUInt(reset)
[928] FIRRTL:198697 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:node :: node _T_5 = eq(_T_4, UInt<1>(0h0))
[929] FIRRTL:198698 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:when :: when _T_5 :
[930] FIRRTL:198699 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:node :: node _T_6 = eq(_T_3, UInt<1>(0h0))
[931] FIRRTL:198700 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:when :: when _T_6 :
[932] FIRRTL:198701 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at dcache.scala:581 assert(!(wb.io.meta_read.fire ^ wb.io.data_req.fire))\n") : printf
[933] FIRRTL:198702 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:581:9 KIND:nondriving :: assert(clock, _T_3, UInt<1>(0h1), "") : assert
[934] FIRRTL:198703 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node prober_fire = and(prober.io.meta_read.ready, prober.io.meta_read.valid)
[935] FIRRTL:198704 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:586:26 KIND:wire :: wire prober_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[936] FIRRTL:198705 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].is_hella
[937] FIRRTL:198706 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].data
[938] FIRRTL:198707 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].addr
[939] FIRRTL:198708 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.debug_tsrc
[940] FIRRTL:198709 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.debug_fsrc
[941] FIRRTL:198710 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.bp_xcpt_if
[942] FIRRTL:198711 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.bp_debug_if
[943] FIRRTL:198712 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.xcpt_ma_if
[944] FIRRTL:198713 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.xcpt_ae_if
[945] FIRRTL:198714 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.xcpt_pf_if
[946] FIRRTL:198715 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_typ
[947] FIRRTL:198716 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_rm
[948] FIRRTL:198717 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_val
[949] FIRRTL:198718 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fcn_op
[950] FIRRTL:198719 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fcn_dw
[951] FIRRTL:198720 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.frs3_en
[952] FIRRTL:198721 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.lrs2_rtype
[953] FIRRTL:198722 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.lrs1_rtype
[954] FIRRTL:198723 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.dst_rtype
[955] FIRRTL:198724 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.lrs3
[956] FIRRTL:198725 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.lrs2
[957] FIRRTL:198726 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.lrs1
[958] FIRRTL:198727 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ldst
[959] FIRRTL:198728 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ldst_is_rs1
[960] FIRRTL:198729 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.csr_cmd
[961] FIRRTL:198730 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.flush_on_commit
[962] FIRRTL:198731 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_unique
[963] FIRRTL:198732 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.uses_stq
[964] FIRRTL:198733 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.uses_ldq
[965] FIRRTL:198734 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.mem_signed
[966] FIRRTL:198735 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.mem_size
[967] FIRRTL:198736 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.mem_cmd
[968] FIRRTL:198737 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.exc_cause
[969] FIRRTL:198738 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.exception
[970] FIRRTL:198739 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.stale_pdst
[971] FIRRTL:198740 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ppred_busy
[972] FIRRTL:198741 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs3_busy
[973] FIRRTL:198742 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs2_busy
[974] FIRRTL:198743 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs1_busy
[975] FIRRTL:198744 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ppred
[976] FIRRTL:198745 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs3
[977] FIRRTL:198746 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs2
[978] FIRRTL:198747 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.prs1
[979] FIRRTL:198748 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.pdst
[980] FIRRTL:198749 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.rxq_idx
[981] FIRRTL:198750 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.stq_idx
[982] FIRRTL:198751 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ldq_idx
[983] FIRRTL:198752 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.rob_idx
[984] FIRRTL:198753 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.vec
[985] FIRRTL:198754 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.wflags
[986] FIRRTL:198755 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.sqrt
[987] FIRRTL:198756 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.div
[988] FIRRTL:198757 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.fma
[989] FIRRTL:198758 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.fastpipe
[990] FIRRTL:198759 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.toint
[991] FIRRTL:198760 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.fromint
[992] FIRRTL:198761 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.typeTagOut
[993] FIRRTL:198762 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.typeTagIn
[994] FIRRTL:198763 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.swap23
[995] FIRRTL:198764 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.swap12
[996] FIRRTL:198765 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.ren3
[997] FIRRTL:198766 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.ren2
[998] FIRRTL:198767 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.ren1
[999] FIRRTL:198768 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.wen
[1000] FIRRTL:198769 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fp_ctrl.ldst
[1001] FIRRTL:198770 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.op2_sel
[1002] FIRRTL:198771 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.op1_sel
[1003] FIRRTL:198772 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.imm_packed
[1004] FIRRTL:198773 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.pimm
[1005] FIRRTL:198774 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.imm_sel
[1006] FIRRTL:198775 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.imm_rename
[1007] FIRRTL:198776 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.taken
[1008] FIRRTL:198777 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.pc_lob
[1009] FIRRTL:198778 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.edge_inst
[1010] FIRRTL:198779 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.ftq_idx
[1011] FIRRTL:198780 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_mov
[1012] FIRRTL:198781 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_rocc
[1013] FIRRTL:198782 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_sys_pc2epc
[1014] FIRRTL:198783 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_eret
[1015] FIRRTL:198784 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_amo
[1016] FIRRTL:198785 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_sfence
[1017] FIRRTL:198786 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_fencei
[1018] FIRRTL:198787 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_fence
[1019] FIRRTL:198788 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_sfb
[1020] FIRRTL:198789 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.br_type
[1021] FIRRTL:198790 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.br_tag
[1022] FIRRTL:198791 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.br_mask
[1023] FIRRTL:198792 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.dis_col_sel
[1024] FIRRTL:198793 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_p3_bypass_hint
[1025] FIRRTL:198794 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_p2_bypass_hint
[1026] FIRRTL:198795 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_p1_bypass_hint
[1027] FIRRTL:198796 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_p2_speculative_child
[1028] FIRRTL:198797 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_p1_speculative_child
[1029] FIRRTL:198798 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_issued_partial_dgen
[1030] FIRRTL:198799 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_issued_partial_agen
[1031] FIRRTL:198800 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iw_issued
[1032] FIRRTL:198801 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[0]
[1033] FIRRTL:198802 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[1]
[1034] FIRRTL:198803 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[2]
[1035] FIRRTL:198804 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[3]
[1036] FIRRTL:198805 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[4]
[1037] FIRRTL:198806 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[5]
[1038] FIRRTL:198807 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[6]
[1039] FIRRTL:198808 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[7]
[1040] FIRRTL:198809 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[8]
[1041] FIRRTL:198810 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.fu_code[9]
[1042] FIRRTL:198811 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iq_type[0]
[1043] FIRRTL:198812 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iq_type[1]
[1044] FIRRTL:198813 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iq_type[2]
[1045] FIRRTL:198814 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.iq_type[3]
[1046] FIRRTL:198815 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.debug_pc
[1047] FIRRTL:198816 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.is_rvc
[1048] FIRRTL:198817 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.debug_inst
[1049] FIRRTL:198818 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:587:26 KIND:invalidate :: invalidate prober_req[0].uop.inst
[1050] FIRRTL:198819 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:wire :: wire _prober_req_0_uop_WIRE : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}
[1051] FIRRTL:198820 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.debug_tsrc, UInt<3>(0h0)
[1052] FIRRTL:198821 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.debug_fsrc, UInt<3>(0h0)
[1053] FIRRTL:198822 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.bp_xcpt_if, UInt<1>(0h0)
[1054] FIRRTL:198823 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.bp_debug_if, UInt<1>(0h0)
[1055] FIRRTL:198824 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.xcpt_ma_if, UInt<1>(0h0)
[1056] FIRRTL:198825 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.xcpt_ae_if, UInt<1>(0h0)
[1057] FIRRTL:198826 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.xcpt_pf_if, UInt<1>(0h0)
[1058] FIRRTL:198827 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_typ, UInt<2>(0h0)
[1059] FIRRTL:198828 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_rm, UInt<3>(0h0)
[1060] FIRRTL:198829 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_val, UInt<1>(0h0)
[1061] FIRRTL:198830 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fcn_op, UInt<5>(0h0)
[1062] FIRRTL:198831 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fcn_dw, UInt<1>(0h0)
[1063] FIRRTL:198832 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.frs3_en, UInt<1>(0h0)
[1064] FIRRTL:198833 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.lrs2_rtype, UInt<2>(0h0)
[1065] FIRRTL:198834 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.lrs1_rtype, UInt<2>(0h0)
[1066] FIRRTL:198835 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.dst_rtype, UInt<2>(0h0)
[1067] FIRRTL:198836 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.lrs3, UInt<6>(0h0)
[1068] FIRRTL:198837 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.lrs2, UInt<6>(0h0)
[1069] FIRRTL:198838 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.lrs1, UInt<6>(0h0)
[1070] FIRRTL:198839 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ldst, UInt<6>(0h0)
[1071] FIRRTL:198840 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ldst_is_rs1, UInt<1>(0h0)
[1072] FIRRTL:198841 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.csr_cmd, UInt<3>(0h0)
[1073] FIRRTL:198842 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.flush_on_commit, UInt<1>(0h0)
[1074] FIRRTL:198843 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_unique, UInt<1>(0h0)
[1075] FIRRTL:198844 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.uses_stq, UInt<1>(0h0)
[1076] FIRRTL:198845 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.uses_ldq, UInt<1>(0h0)
[1077] FIRRTL:198846 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.mem_signed, UInt<1>(0h0)
[1078] FIRRTL:198847 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.mem_size, UInt<2>(0h0)
[1079] FIRRTL:198848 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.mem_cmd, UInt<5>(0h0)
[1080] FIRRTL:198849 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.exc_cause, UInt<64>(0h0)
[1081] FIRRTL:198850 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.exception, UInt<1>(0h0)
[1082] FIRRTL:198851 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.stale_pdst, UInt<6>(0h0)
[1083] FIRRTL:198852 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ppred_busy, UInt<1>(0h0)
[1084] FIRRTL:198853 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs3_busy, UInt<1>(0h0)
[1085] FIRRTL:198854 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs2_busy, UInt<1>(0h0)
[1086] FIRRTL:198855 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs1_busy, UInt<1>(0h0)
[1087] FIRRTL:198856 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ppred, UInt<4>(0h0)
[1088] FIRRTL:198857 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs3, UInt<6>(0h0)
[1089] FIRRTL:198858 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs2, UInt<6>(0h0)
[1090] FIRRTL:198859 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.prs1, UInt<6>(0h0)
[1091] FIRRTL:198860 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.pdst, UInt<6>(0h0)
[1092] FIRRTL:198861 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.rxq_idx, UInt<2>(0h0)
[1093] FIRRTL:198862 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.stq_idx, UInt<4>(0h0)
[1094] FIRRTL:198863 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ldq_idx, UInt<4>(0h0)
[1095] FIRRTL:198864 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.rob_idx, UInt<5>(0h0)
[1096] FIRRTL:198865 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.vec, UInt<1>(0h0)
[1097] FIRRTL:198866 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.wflags, UInt<1>(0h0)
[1098] FIRRTL:198867 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.sqrt, UInt<1>(0h0)
[1099] FIRRTL:198868 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.div, UInt<1>(0h0)
[1100] FIRRTL:198869 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.fma, UInt<1>(0h0)
[1101] FIRRTL:198870 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.fastpipe, UInt<1>(0h0)
[1102] FIRRTL:198871 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.toint, UInt<1>(0h0)
[1103] FIRRTL:198872 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.fromint, UInt<1>(0h0)
[1104] FIRRTL:198873 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.typeTagOut, UInt<2>(0h0)
[1105] FIRRTL:198874 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.typeTagIn, UInt<2>(0h0)
[1106] FIRRTL:198875 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.swap23, UInt<1>(0h0)
[1107] FIRRTL:198876 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.swap12, UInt<1>(0h0)
[1108] FIRRTL:198877 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.ren3, UInt<1>(0h0)
[1109] FIRRTL:198878 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.ren2, UInt<1>(0h0)
[1110] FIRRTL:198879 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.ren1, UInt<1>(0h0)
[1111] FIRRTL:198880 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.wen, UInt<1>(0h0)
[1112] FIRRTL:198881 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fp_ctrl.ldst, UInt<1>(0h0)
[1113] FIRRTL:198882 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.op2_sel, UInt<3>(0h0)
[1114] FIRRTL:198883 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.op1_sel, UInt<2>(0h0)
[1115] FIRRTL:198884 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.imm_packed, UInt<20>(0h0)
[1116] FIRRTL:198885 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.pimm, UInt<5>(0h0)
[1117] FIRRTL:198886 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.imm_sel, UInt<3>(0h0)
[1118] FIRRTL:198887 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.imm_rename, UInt<1>(0h0)
[1119] FIRRTL:198888 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.taken, UInt<1>(0h0)
[1120] FIRRTL:198889 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.pc_lob, UInt<6>(0h0)
[1121] FIRRTL:198890 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.edge_inst, UInt<1>(0h0)
[1122] FIRRTL:198891 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.ftq_idx, UInt<4>(0h0)
[1123] FIRRTL:198892 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_mov, UInt<1>(0h0)
[1124] FIRRTL:198893 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_rocc, UInt<1>(0h0)
[1125] FIRRTL:198894 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_sys_pc2epc, UInt<1>(0h0)
[1126] FIRRTL:198895 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_eret, UInt<1>(0h0)
[1127] FIRRTL:198896 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_amo, UInt<1>(0h0)
[1128] FIRRTL:198897 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_sfence, UInt<1>(0h0)
[1129] FIRRTL:198898 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_fencei, UInt<1>(0h0)
[1130] FIRRTL:198899 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_fence, UInt<1>(0h0)
[1131] FIRRTL:198900 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_sfb, UInt<1>(0h0)
[1132] FIRRTL:198901 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.br_type, UInt<4>(0h0)
[1133] FIRRTL:198902 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.br_tag, UInt<3>(0h0)
[1134] FIRRTL:198903 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.br_mask, UInt<8>(0h0)
[1135] FIRRTL:198904 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.dis_col_sel, UInt<1>(0h0)
[1136] FIRRTL:198905 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_p3_bypass_hint, UInt<1>(0h0)
[1137] FIRRTL:198906 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_p2_bypass_hint, UInt<1>(0h0)
[1138] FIRRTL:198907 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_p1_bypass_hint, UInt<1>(0h0)
[1139] FIRRTL:198908 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_p2_speculative_child, UInt<1>(0h0)
[1140] FIRRTL:198909 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_p1_speculative_child, UInt<1>(0h0)
[1141] FIRRTL:198910 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_issued_partial_dgen, UInt<1>(0h0)
[1142] FIRRTL:198911 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_issued_partial_agen, UInt<1>(0h0)
[1143] FIRRTL:198912 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iw_issued, UInt<1>(0h0)
[1144] FIRRTL:198913 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[0], UInt<1>(0h0)
[1145] FIRRTL:198914 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[1], UInt<1>(0h0)
[1146] FIRRTL:198915 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[2], UInt<1>(0h0)
[1147] FIRRTL:198916 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[3], UInt<1>(0h0)
[1148] FIRRTL:198917 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[4], UInt<1>(0h0)
[1149] FIRRTL:198918 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[5], UInt<1>(0h0)
[1150] FIRRTL:198919 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[6], UInt<1>(0h0)
[1151] FIRRTL:198920 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[7], UInt<1>(0h0)
[1152] FIRRTL:198921 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[8], UInt<1>(0h0)
[1153] FIRRTL:198922 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.fu_code[9], UInt<1>(0h0)
[1154] FIRRTL:198923 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iq_type[0], UInt<1>(0h0)
[1155] FIRRTL:198924 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iq_type[1], UInt<1>(0h0)
[1156] FIRRTL:198925 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iq_type[2], UInt<1>(0h0)
[1157] FIRRTL:198926 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.iq_type[3], UInt<1>(0h0)
[1158] FIRRTL:198927 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.debug_pc, UInt<40>(0h0)
[1159] FIRRTL:198928 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.is_rvc, UInt<1>(0h0)
[1160] FIRRTL:198929 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.debug_inst, UInt<32>(0h0)
[1161] FIRRTL:198930 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _prober_req_0_uop_WIRE.inst, UInt<32>(0h0)
[1162] FIRRTL:198931 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:588:26 KIND:connect :: connect prober_req[0].uop, _prober_req_0_uop_WIRE
[1163] FIRRTL:198932 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:589:32 KIND:node :: node _prober_req_0_addr_T = cat(prober.io.meta_read.bits.tag, prober.io.meta_read.bits.idx)
[1164] FIRRTL:198933 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:589:93 KIND:node :: node _prober_req_0_addr_T_1 = shl(_prober_req_0_addr_T, 6)
[1165] FIRRTL:198934 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:589:26 KIND:connect :: connect prober_req[0].addr, _prober_req_0_addr_T_1
[1166] FIRRTL:198935 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:590:26 KIND:invalidate :: invalidate prober_req[0].data
[1167] FIRRTL:198936 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:591:26 KIND:connect :: connect prober_req[0].is_hella, UInt<1>(0h0)
[1168] FIRRTL:198937 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:593:36 KIND:connect :: connect metaReadArb.io.in[1].valid, prober.io.meta_read.valid
[1169] FIRRTL:198938 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:594:36 KIND:connect :: connect metaReadArb.io.in[1].bits.req[0].tag, prober.io.meta_read.bits.tag
[1170] FIRRTL:198939 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:594:36 KIND:connect :: connect metaReadArb.io.in[1].bits.req[0].way_en, prober.io.meta_read.bits.way_en
[1171] FIRRTL:198940 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:594:36 KIND:connect :: connect metaReadArb.io.in[1].bits.req[0].idx, prober.io.meta_read.bits.idx
[1172] FIRRTL:198941 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:595:29 KIND:connect :: connect prober.io.meta_read.ready, metaReadArb.io.in[1].ready
[1173] FIRRTL:198942 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node prefetch_fire = and(mshrs.io.prefetch.ready, mshrs.io.prefetch.valid)
[1174] FIRRTL:198943 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:601:27 KIND:wire :: wire prefetch_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[1175] FIRRTL:198944 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].is_hella
[1176] FIRRTL:198945 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].data
[1177] FIRRTL:198946 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].addr
[1178] FIRRTL:198947 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.debug_tsrc
[1179] FIRRTL:198948 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.debug_fsrc
[1180] FIRRTL:198949 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.bp_xcpt_if
[1181] FIRRTL:198950 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.bp_debug_if
[1182] FIRRTL:198951 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.xcpt_ma_if
[1183] FIRRTL:198952 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.xcpt_ae_if
[1184] FIRRTL:198953 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.xcpt_pf_if
[1185] FIRRTL:198954 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_typ
[1186] FIRRTL:198955 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_rm
[1187] FIRRTL:198956 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_val
[1188] FIRRTL:198957 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fcn_op
[1189] FIRRTL:198958 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fcn_dw
[1190] FIRRTL:198959 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.frs3_en
[1191] FIRRTL:198960 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.lrs2_rtype
[1192] FIRRTL:198961 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.lrs1_rtype
[1193] FIRRTL:198962 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.dst_rtype
[1194] FIRRTL:198963 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.lrs3
[1195] FIRRTL:198964 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.lrs2
[1196] FIRRTL:198965 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.lrs1
[1197] FIRRTL:198966 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ldst
[1198] FIRRTL:198967 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ldst_is_rs1
[1199] FIRRTL:198968 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.csr_cmd
[1200] FIRRTL:198969 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.flush_on_commit
[1201] FIRRTL:198970 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_unique
[1202] FIRRTL:198971 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.uses_stq
[1203] FIRRTL:198972 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.uses_ldq
[1204] FIRRTL:198973 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.mem_signed
[1205] FIRRTL:198974 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.mem_size
[1206] FIRRTL:198975 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.mem_cmd
[1207] FIRRTL:198976 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.exc_cause
[1208] FIRRTL:198977 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.exception
[1209] FIRRTL:198978 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.stale_pdst
[1210] FIRRTL:198979 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ppred_busy
[1211] FIRRTL:198980 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs3_busy
[1212] FIRRTL:198981 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs2_busy
[1213] FIRRTL:198982 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs1_busy
[1214] FIRRTL:198983 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ppred
[1215] FIRRTL:198984 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs3
[1216] FIRRTL:198985 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs2
[1217] FIRRTL:198986 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.prs1
[1218] FIRRTL:198987 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.pdst
[1219] FIRRTL:198988 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.rxq_idx
[1220] FIRRTL:198989 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.stq_idx
[1221] FIRRTL:198990 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ldq_idx
[1222] FIRRTL:198991 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.rob_idx
[1223] FIRRTL:198992 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.vec
[1224] FIRRTL:198993 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.wflags
[1225] FIRRTL:198994 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.sqrt
[1226] FIRRTL:198995 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.div
[1227] FIRRTL:198996 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.fma
[1228] FIRRTL:198997 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.fastpipe
[1229] FIRRTL:198998 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.toint
[1230] FIRRTL:198999 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.fromint
[1231] FIRRTL:199000 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.typeTagOut
[1232] FIRRTL:199001 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.typeTagIn
[1233] FIRRTL:199002 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.swap23
[1234] FIRRTL:199003 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.swap12
[1235] FIRRTL:199004 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.ren3
[1236] FIRRTL:199005 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.ren2
[1237] FIRRTL:199006 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.ren1
[1238] FIRRTL:199007 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.wen
[1239] FIRRTL:199008 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fp_ctrl.ldst
[1240] FIRRTL:199009 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.op2_sel
[1241] FIRRTL:199010 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.op1_sel
[1242] FIRRTL:199011 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.imm_packed
[1243] FIRRTL:199012 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.pimm
[1244] FIRRTL:199013 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.imm_sel
[1245] FIRRTL:199014 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.imm_rename
[1246] FIRRTL:199015 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.taken
[1247] FIRRTL:199016 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.pc_lob
[1248] FIRRTL:199017 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.edge_inst
[1249] FIRRTL:199018 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.ftq_idx
[1250] FIRRTL:199019 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_mov
[1251] FIRRTL:199020 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_rocc
[1252] FIRRTL:199021 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_sys_pc2epc
[1253] FIRRTL:199022 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_eret
[1254] FIRRTL:199023 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_amo
[1255] FIRRTL:199024 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_sfence
[1256] FIRRTL:199025 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_fencei
[1257] FIRRTL:199026 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_fence
[1258] FIRRTL:199027 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_sfb
[1259] FIRRTL:199028 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.br_type
[1260] FIRRTL:199029 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.br_tag
[1261] FIRRTL:199030 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.br_mask
[1262] FIRRTL:199031 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.dis_col_sel
[1263] FIRRTL:199032 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_p3_bypass_hint
[1264] FIRRTL:199033 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_p2_bypass_hint
[1265] FIRRTL:199034 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_p1_bypass_hint
[1266] FIRRTL:199035 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_p2_speculative_child
[1267] FIRRTL:199036 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_p1_speculative_child
[1268] FIRRTL:199037 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_issued_partial_dgen
[1269] FIRRTL:199038 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_issued_partial_agen
[1270] FIRRTL:199039 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iw_issued
[1271] FIRRTL:199040 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[0]
[1272] FIRRTL:199041 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[1]
[1273] FIRRTL:199042 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[2]
[1274] FIRRTL:199043 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[3]
[1275] FIRRTL:199044 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[4]
[1276] FIRRTL:199045 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[5]
[1277] FIRRTL:199046 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[6]
[1278] FIRRTL:199047 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[7]
[1279] FIRRTL:199048 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[8]
[1280] FIRRTL:199049 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.fu_code[9]
[1281] FIRRTL:199050 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iq_type[0]
[1282] FIRRTL:199051 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iq_type[1]
[1283] FIRRTL:199052 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iq_type[2]
[1284] FIRRTL:199053 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.iq_type[3]
[1285] FIRRTL:199054 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.debug_pc
[1286] FIRRTL:199055 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.is_rvc
[1287] FIRRTL:199056 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.debug_inst
[1288] FIRRTL:199057 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:602:19 KIND:invalidate :: invalidate prefetch_req[0].uop.inst
[1289] FIRRTL:199058 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:603:19 KIND:connect :: connect prefetch_req[0], mshrs.io.prefetch.bits
[1290] FIRRTL:199059 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:605:43 KIND:connect :: connect metaReadArb.io.in[5].valid, mshrs.io.prefetch.valid
[1291] FIRRTL:199060 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:606:74 KIND:node :: node _metaReadArb_io_in_5_bits_req_0_idx_T = shr(mshrs.io.prefetch.bits.addr, 6)
[1292] FIRRTL:199061 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:606:43 KIND:connect :: connect metaReadArb.io.in[5].bits.req[0].idx, _metaReadArb_io_in_5_bits_req_0_idx_T
[1293] FIRRTL:199062 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:607:43 KIND:invalidate :: invalidate metaReadArb.io.in[5].bits.req[0].way_en
[1294] FIRRTL:199063 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:608:43 KIND:invalidate :: invalidate metaReadArb.io.in[5].bits.req[0].tag
[1295] FIRRTL:199064 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:609:27 KIND:connect :: connect mshrs.io.prefetch.ready, metaReadArb.io.in[5].ready
[1296] FIRRTL:199065 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_valid_T = and(io.lsu.req.ready, io.lsu.req.valid)
[1297] FIRRTL:199066 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:612:46 KIND:wire :: wire _s0_valid_WIRE : UInt<1>[1]
[1298] FIRRTL:199067 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:612:46 KIND:connect :: connect _s0_valid_WIRE[0], io.lsu.req.bits[0].valid
[1299] FIRRTL:199068 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_valid_T_1 = and(mshrs.io.replay.ready, mshrs.io.replay.valid)
[1300] FIRRTL:199069 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:613:43 KIND:node :: node _s0_valid_T_2 = or(_s0_valid_T_1, wb_fire)
[1301] FIRRTL:199070 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:613:54 KIND:node :: node _s0_valid_T_3 = or(_s0_valid_T_2, prober_fire)
[1302] FIRRTL:199071 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:613:69 KIND:node :: node _s0_valid_T_4 = or(_s0_valid_T_3, prefetch_fire)
[1303] FIRRTL:199072 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_valid_T_5 = and(mshrs.io.meta_read.ready, mshrs.io.meta_read.valid)
[1304] FIRRTL:199073 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:613:86 KIND:node :: node _s0_valid_T_6 = or(_s0_valid_T_4, _s0_valid_T_5)
[1305] FIRRTL:199074 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:614:48 KIND:wire :: wire _s0_valid_WIRE_1 : UInt<1>[1]
[1306] FIRRTL:199075 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:614:48 KIND:connect :: connect _s0_valid_WIRE_1[0], UInt<1>(0h1)
[1307] FIRRTL:199076 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:614:82 KIND:wire :: wire _s0_valid_WIRE_2 : UInt<1>[1]
[1308] FIRRTL:199077 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:614:82 KIND:connect :: connect _s0_valid_WIRE_2[0], UInt<1>(0h0)
[1309] FIRRTL:199078 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:613:21 KIND:node :: node _s0_valid_T_7 = mux(_s0_valid_T_6, _s0_valid_WIRE_1, _s0_valid_WIRE_2)
[1310] FIRRTL:199079 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:612:21 KIND:node :: node s0_valid = mux(_s0_valid_T, _s0_valid_WIRE, _s0_valid_T_7)
[1311] FIRRTL:199080 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_req_T = and(io.lsu.req.ready, io.lsu.req.valid)
[1312] FIRRTL:199081 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:615:56 KIND:wire :: wire _s0_req_WIRE : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1]
[1313] FIRRTL:199082 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:615:56 KIND:connect :: connect _s0_req_WIRE[0], io.lsu.req.bits[0].bits
[1314] FIRRTL:199083 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_req_T_1 = and(mshrs.io.meta_read.ready, mshrs.io.meta_read.valid)
[1315] FIRRTL:199084 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:619:21 KIND:node :: node _s0_req_T_2 = mux(_s0_req_T_1, mshr_read_req, replay_req)
[1316] FIRRTL:199085 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:618:21 KIND:node :: node _s0_req_T_3 = mux(prefetch_fire, prefetch_req, _s0_req_T_2)
[1317] FIRRTL:199086 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:617:21 KIND:node :: node _s0_req_T_4 = mux(prober_fire, prober_req, _s0_req_T_3)
[1318] FIRRTL:199087 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:616:21 KIND:node :: node _s0_req_T_5 = mux(wb_fire, wb_req, _s0_req_T_4)
[1319] FIRRTL:199088 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:615:21 KIND:node :: node s0_req = mux(_s0_req_T, _s0_req_WIRE, _s0_req_T_5)
[1320] FIRRTL:199089 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_type_T = and(io.lsu.req.ready, io.lsu.req.valid)
[1321] FIRRTL:199090 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_type_T_1 = and(mshrs.io.meta_read.ready, mshrs.io.meta_read.valid)
[1322] FIRRTL:199091 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:625:21 KIND:node :: node _s0_type_T_2 = mux(_s0_type_T_1, UInt<3>(0h3), UInt<3>(0h0))
[1323] FIRRTL:199092 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:624:21 KIND:node :: node _s0_type_T_3 = mux(prefetch_fire, UInt<3>(0h5), _s0_type_T_2)
[1324] FIRRTL:199093 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:623:21 KIND:node :: node _s0_type_T_4 = mux(prober_fire, UInt<3>(0h1), _s0_type_T_3)
[1325] FIRRTL:199094 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:622:21 KIND:node :: node _s0_type_T_5 = mux(wb_fire, UInt<3>(0h2), _s0_type_T_4)
[1326] FIRRTL:199095 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:621:21 KIND:node :: node s0_type = mux(_s0_type_T, UInt<3>(0h4), _s0_type_T_5)
[1327] FIRRTL:199096 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_send_resp_or_nack_T = and(io.lsu.req.ready, io.lsu.req.valid)
[1328] FIRRTL:199097 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s0_send_resp_or_nack_T_1 = and(mshrs.io.replay.ready, mshrs.io.replay.valid)
[1329] FIRRTL:199098 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_2 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<1>(0h0))
[1330] FIRRTL:199099 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_3 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<5>(0h10))
[1331] FIRRTL:199100 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_4 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<3>(0h6))
[1332] FIRRTL:199101 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_5 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<3>(0h7))
[1333] FIRRTL:199102 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_6 = or(_s0_send_resp_or_nack_T_2, _s0_send_resp_or_nack_T_3)
[1334] FIRRTL:199103 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_7 = or(_s0_send_resp_or_nack_T_6, _s0_send_resp_or_nack_T_4)
[1335] FIRRTL:199104 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_8 = or(_s0_send_resp_or_nack_T_7, _s0_send_resp_or_nack_T_5)
[1336] FIRRTL:199105 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_9 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<3>(0h4))
[1337] FIRRTL:199106 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_10 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0h9))
[1338] FIRRTL:199107 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_11 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0ha))
[1339] FIRRTL:199108 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_12 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0hb))
[1340] FIRRTL:199109 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_13 = or(_s0_send_resp_or_nack_T_9, _s0_send_resp_or_nack_T_10)
[1341] FIRRTL:199110 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_14 = or(_s0_send_resp_or_nack_T_13, _s0_send_resp_or_nack_T_11)
[1342] FIRRTL:199111 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_15 = or(_s0_send_resp_or_nack_T_14, _s0_send_resp_or_nack_T_12)
[1343] FIRRTL:199112 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_16 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0h8))
[1344] FIRRTL:199113 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_17 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0hc))
[1345] FIRRTL:199114 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_18 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0hd))
[1346] FIRRTL:199115 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_19 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0he))
[1347] FIRRTL:199116 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s0_send_resp_or_nack_T_20 = eq(mshrs.io.replay.bits.uop.mem_cmd, UInt<4>(0hf))
[1348] FIRRTL:199117 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_21 = or(_s0_send_resp_or_nack_T_16, _s0_send_resp_or_nack_T_17)
[1349] FIRRTL:199118 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_22 = or(_s0_send_resp_or_nack_T_21, _s0_send_resp_or_nack_T_18)
[1350] FIRRTL:199119 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_23 = or(_s0_send_resp_or_nack_T_22, _s0_send_resp_or_nack_T_19)
[1351] FIRRTL:199120 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s0_send_resp_or_nack_T_24 = or(_s0_send_resp_or_nack_T_23, _s0_send_resp_or_nack_T_20)
[1352] FIRRTL:199121 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s0_send_resp_or_nack_T_25 = or(_s0_send_resp_or_nack_T_15, _s0_send_resp_or_nack_T_24)
[1353] FIRRTL:199122 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _s0_send_resp_or_nack_T_26 = or(_s0_send_resp_or_nack_T_8, _s0_send_resp_or_nack_T_25)
[1354] FIRRTL:199123 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:630:38 KIND:node :: node _s0_send_resp_or_nack_T_27 = and(_s0_send_resp_or_nack_T_1, _s0_send_resp_or_nack_T_26)
[1355] FIRRTL:199124 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:630:16 KIND:node :: node _s0_send_resp_or_nack_T_28 = mux(_s0_send_resp_or_nack_T_27, UInt<1>(0h1), UInt<1>(0h0))
[1356] FIRRTL:199125 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:630:117 KIND:node :: node _s0_send_resp_or_nack_T_29 = bits(_s0_send_resp_or_nack_T_28, 0, 0)
[1357] FIRRTL:199126 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:630:12 KIND:wire :: wire _s0_send_resp_or_nack_WIRE : UInt<1>[1]
[1358] FIRRTL:199127 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:630:12 KIND:connect :: connect _s0_send_resp_or_nack_WIRE[0], _s0_send_resp_or_nack_T_29
[1359] FIRRTL:199128 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:629:33 KIND:node :: node s0_send_resp_or_nack = mux(_s0_send_resp_or_nack_T, s0_valid, _s0_send_resp_or_nack_WIRE)
[1360] FIRRTL:199129 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:633:32 KIND:reg :: reg s1_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1], clock
[1361] FIRRTL:199130 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:633:32 KIND:connect :: connect s1_req, s0_req
[1362] FIRRTL:199131 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _s1_req_0_uop_br_mask_T = not(io.lsu.brupdate.b1.resolve_mask)
[1363] FIRRTL:199132 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _s1_req_0_uop_br_mask_T_1 = and(s0_req[0].uop.br_mask, _s1_req_0_uop_br_mask_T)
[1364] FIRRTL:199133 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:635:27 KIND:connect :: connect s1_req[0].uop.br_mask, _s1_req_0_uop_br_mask_T_1
[1365] FIRRTL:199134 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:636:29 KIND:wire :: wire s2_store_failed : UInt<1>
[1366] FIRRTL:199135 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _s1_valid_T = and(io.lsu.brupdate.b1.mispredict_mask, s0_req[0].uop.br_mask)
[1367] FIRRTL:199136 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _s1_valid_T_1 = neq(_s1_valid_T, UInt<1>(0h0))
[1368] FIRRTL:199137 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _s1_valid_T_2 = or(_s1_valid_T_1, UInt<1>(0h0))
[1369] FIRRTL:199138 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:639:26 KIND:node :: node _s1_valid_T_3 = eq(_s1_valid_T_2, UInt<1>(0h0))
[1370] FIRRTL:199139 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:638:74 KIND:node :: node _s1_valid_T_4 = and(s0_valid[0], _s1_valid_T_3)
[1371] FIRRTL:199140 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:640:45 KIND:node :: node _s1_valid_T_5 = and(io.lsu.exception, s0_req[0].uop.uses_ldq)
[1372] FIRRTL:199141 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:640:26 KIND:node :: node _s1_valid_T_6 = eq(_s1_valid_T_5, UInt<1>(0h0))
[1373] FIRRTL:199142 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:639:85 KIND:node :: node _s1_valid_T_7 = and(_s1_valid_T_4, _s1_valid_T_6)
[1374] FIRRTL:199143 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s1_valid_T_8 = and(io.lsu.req.ready, io.lsu.req.valid)
[1375] FIRRTL:199144 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:641:44 KIND:node :: node _s1_valid_T_9 = and(s2_store_failed, _s1_valid_T_8)
[1376] FIRRTL:199145 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:641:63 KIND:node :: node _s1_valid_T_10 = and(_s1_valid_T_9, s0_req[0].uop.uses_stq)
[1377] FIRRTL:199146 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:641:26 KIND:node :: node _s1_valid_T_11 = eq(_s1_valid_T_10, UInt<1>(0h0))
[1378] FIRRTL:199147 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:640:74 KIND:node :: node _s1_valid_T_12 = and(_s1_valid_T_7, _s1_valid_T_11)
[1379] FIRRTL:199148 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:638:25 KIND:regreset :: regreset s1_valid_REG : UInt<1>, clock, reset, UInt<1>(0h0)
[1380] FIRRTL:199149 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:638:25 KIND:connect :: connect s1_valid_REG, _s1_valid_T_12
[1381] FIRRTL:199150 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s1_valid : UInt<1>[1]
[1383] FIRRTL:199152 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_7 = and(io.lsu.req.ready, io.lsu.req.valid)
[1384] FIRRTL:199153 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:43 KIND:reg :: reg REG : UInt<1>, clock
[1385] FIRRTL:199154 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:43 KIND:connect :: connect REG, _T_7
[1386] FIRRTL:199155 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:35 KIND:node :: node _T_8 = eq(REG, UInt<1>(0h0))
[1387] FIRRTL:199156 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:32 KIND:node :: node _T_9 = and(io.lsu.s1_kill[0], _T_8)
[1388] FIRRTL:199157 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:72 KIND:reg :: reg REG_1 : UInt<1>, clock
[1389] FIRRTL:199158 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:72 KIND:connect :: connect REG_1, io.lsu.req.bits[0].valid
[1390] FIRRTL:199159 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:64 KIND:node :: node _T_10 = eq(REG_1, UInt<1>(0h0))
[1391] FIRRTL:199160 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:61 KIND:node :: node _T_11 = and(_T_9, _T_10)
[1392] FIRRTL:199161 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:12 KIND:node :: node _T_12 = eq(_T_11, UInt<1>(0h0))
[1393] FIRRTL:199162 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:node :: node _T_13 = asUInt(reset)
[1394] FIRRTL:199163 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:node :: node _T_14 = eq(_T_13, UInt<1>(0h0))
[1395] FIRRTL:199164 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:when :: when _T_14 :
[1396] FIRRTL:199165 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:node :: node _T_15 = eq(_T_12, UInt<1>(0h0))
[1397] FIRRTL:199166 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:when :: when _T_15 :
[1398] FIRRTL:199167 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at dcache.scala:645 assert(!(io.lsu.s1_kill(w) && !RegNext(io.lsu.req.fire) && !RegNext(io.lsu.req.bits(w).valid)))\n") : printf_1
[1399] FIRRTL:199168 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:645:11 KIND:nondriving :: assert(clock, _T_12, UInt<1>(0h1), "") : assert_1
[1404] FIRRTL:199173 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:648:37 KIND:reg :: reg s1_send_resp_or_nack : UInt<1>[1], clock
[1405] FIRRTL:199174 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:648:37 KIND:connect :: connect s1_send_resp_or_nack, s0_send_resp_or_nack
[1406] FIRRTL:199175 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:649:32 KIND:reg :: reg s1_type : UInt, clock
[1407] FIRRTL:199176 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:649:32 KIND:connect :: connect s1_type, s0_type
[1408] FIRRTL:199177 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:651:41 KIND:reg :: reg s1_mshr_meta_read_way_en : UInt, clock
[1409] FIRRTL:199178 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:651:41 KIND:connect :: connect s1_mshr_meta_read_way_en, mshrs.io.meta_read.bits.way_en
[1410] FIRRTL:199179 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:652:41 KIND:reg :: reg s1_replay_way_en : UInt, clock
[1411] FIRRTL:199180 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:652:41 KIND:connect :: connect s1_replay_way_en, mshrs.io.replay.bits.way_en
[1412] FIRRTL:199181 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:653:41 KIND:reg :: reg s1_wb_way_en : UInt, clock
[1413] FIRRTL:199182 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:653:41 KIND:connect :: connect s1_wb_way_en, wb.io.data_req.bits.way_en
[1422] FIRRTL:199191 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:wire :: wire _s1_tag_eq_way_WIRE : UInt<1>[4]
[1430] FIRRTL:199199 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s1_tag_eq_way : UInt<4>[1]
[1447] FIRRTL:199216 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:wire :: wire _s1_tag_match_way_WIRE : UInt<1>[4]
[1458] FIRRTL:199227 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s1_tag_match_way : UInt[1]
[1463] FIRRTL:199232 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s1_wb_idx_matches : UInt<1>[1]
[1465] FIRRTL:199234 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:667:32 KIND:connect :: connect io.lsu.s1_nack_advisory[0], data.io.s1_nacks[0]
[1466] FIRRTL:199235 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:670:25 KIND:reg :: reg s2_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}[1], clock
[1468] FIRRTL:199237 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:671:25 KIND:reg :: reg s2_type : UInt, clock
[1485] FIRRTL:199254 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:673:26 KIND:reg :: reg s2_valid_REG : UInt<1>, clock
[1487] FIRRTL:199256 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_valid : UInt<1>[1]
[1488] FIRRTL:199257 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_valid[0], s2_valid_REG
[1492] FIRRTL:199261 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:681:33 KIND:reg :: reg s2_tag_match_way : UInt[1], clock
[1494] FIRRTL:199263 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:682:49 KIND:node :: node s2_tag_match_0 = orr(s2_tag_match_way[0])
[1495] FIRRTL:199264 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:reg :: reg s2_hit_state_REG : { state : UInt<2>}, clock
[1497] FIRRTL:199266 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:reg :: reg s2_hit_state_REG_1 : { state : UInt<2>}, clock
[1499] FIRRTL:199268 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:reg :: reg s2_hit_state_REG_2 : { state : UInt<2>}, clock
[1501] FIRRTL:199270 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:reg :: reg s2_hit_state_REG_3 : { state : UInt<2>}, clock
[1503] FIRRTL:199272 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:wire :: wire _s2_hit_state_WIRE : { state : UInt<2>}[4]
[1504] FIRRTL:199273 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_hit_state_WIRE[0], s2_hit_state_REG
[1505] FIRRTL:199274 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_hit_state_WIRE[1], s2_hit_state_REG_1
[1506] FIRRTL:199275 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_hit_state_WIRE[2], s2_hit_state_REG_2
[1507] FIRRTL:199276 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_hit_state_WIRE[3], s2_hit_state_REG_3
[1508] FIRRTL:199277 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_hit_state_T = bits(s2_tag_match_way[0], 0, 0)
[1509] FIRRTL:199278 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_hit_state_T_1 = bits(s2_tag_match_way[0], 1, 1)
[1510] FIRRTL:199279 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_hit_state_T_2 = bits(s2_tag_match_way[0], 2, 2)
[1511] FIRRTL:199280 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_hit_state_T_3 = bits(s2_tag_match_way[0], 3, 3)
[1512] FIRRTL:199281 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_hit_state_WIRE_1 : { state : UInt<2>}
[1513] FIRRTL:199282 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_4 = mux(_s2_hit_state_T, _s2_hit_state_WIRE[0].state, UInt<1>(0h0))
[1514] FIRRTL:199283 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_5 = mux(_s2_hit_state_T_1, _s2_hit_state_WIRE[1].state, UInt<1>(0h0))
[1515] FIRRTL:199284 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_6 = mux(_s2_hit_state_T_2, _s2_hit_state_WIRE[2].state, UInt<1>(0h0))
[1516] FIRRTL:199285 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_7 = mux(_s2_hit_state_T_3, _s2_hit_state_WIRE[3].state, UInt<1>(0h0))
[1517] FIRRTL:199286 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_8 = or(_s2_hit_state_T_4, _s2_hit_state_T_5)
[1518] FIRRTL:199287 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_9 = or(_s2_hit_state_T_8, _s2_hit_state_T_6)
[1519] FIRRTL:199288 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_hit_state_T_10 = or(_s2_hit_state_T_9, _s2_hit_state_T_7)
[1520] FIRRTL:199289 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_hit_state_WIRE_2 : UInt<2>
[1521] FIRRTL:199290 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_hit_state_WIRE_2, _s2_hit_state_T_10
[1522] FIRRTL:199291 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_hit_state_WIRE_1.state, _s2_hit_state_WIRE_2
[1523] FIRRTL:199292 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_hit_state : { state : UInt<2>}[1]
[1524] FIRRTL:199293 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_hit_state[0], _s2_hit_state_WIRE_1
[1525] FIRRTL:199294 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s2_has_permission_r_c_cat_T = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[1526] FIRRTL:199295 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s2_has_permission_r_c_cat_T_1 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[1527] FIRRTL:199296 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s2_has_permission_r_c_cat_T_2 = or(_s2_has_permission_r_c_cat_T, _s2_has_permission_r_c_cat_T_1)
[1528] FIRRTL:199297 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s2_has_permission_r_c_cat_T_3 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[1529] FIRRTL:199298 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s2_has_permission_r_c_cat_T_4 = or(_s2_has_permission_r_c_cat_T_2, _s2_has_permission_r_c_cat_T_3)
[1530] FIRRTL:199299 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_5 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[1531] FIRRTL:199300 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_6 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[1532] FIRRTL:199301 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_7 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[1533] FIRRTL:199302 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_8 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[1534] FIRRTL:199303 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_9 = or(_s2_has_permission_r_c_cat_T_5, _s2_has_permission_r_c_cat_T_6)
[1535] FIRRTL:199304 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_10 = or(_s2_has_permission_r_c_cat_T_9, _s2_has_permission_r_c_cat_T_7)
[1536] FIRRTL:199305 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_11 = or(_s2_has_permission_r_c_cat_T_10, _s2_has_permission_r_c_cat_T_8)
[1537] FIRRTL:199306 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_12 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[1538] FIRRTL:199307 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_13 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[1539] FIRRTL:199308 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_14 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[1540] FIRRTL:199309 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_15 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[1541] FIRRTL:199310 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_16 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[1542] FIRRTL:199311 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_17 = or(_s2_has_permission_r_c_cat_T_12, _s2_has_permission_r_c_cat_T_13)
[1543] FIRRTL:199312 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_18 = or(_s2_has_permission_r_c_cat_T_17, _s2_has_permission_r_c_cat_T_14)
[1544] FIRRTL:199313 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_19 = or(_s2_has_permission_r_c_cat_T_18, _s2_has_permission_r_c_cat_T_15)
[1545] FIRRTL:199314 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_20 = or(_s2_has_permission_r_c_cat_T_19, _s2_has_permission_r_c_cat_T_16)
[1546] FIRRTL:199315 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_has_permission_r_c_cat_T_21 = or(_s2_has_permission_r_c_cat_T_11, _s2_has_permission_r_c_cat_T_20)
[1547] FIRRTL:199316 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s2_has_permission_r_c_cat_T_22 = or(_s2_has_permission_r_c_cat_T_4, _s2_has_permission_r_c_cat_T_21)
[1548] FIRRTL:199317 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s2_has_permission_r_c_cat_T_23 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[1549] FIRRTL:199318 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s2_has_permission_r_c_cat_T_24 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[1550] FIRRTL:199319 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s2_has_permission_r_c_cat_T_25 = or(_s2_has_permission_r_c_cat_T_23, _s2_has_permission_r_c_cat_T_24)
[1551] FIRRTL:199320 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s2_has_permission_r_c_cat_T_26 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[1552] FIRRTL:199321 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s2_has_permission_r_c_cat_T_27 = or(_s2_has_permission_r_c_cat_T_25, _s2_has_permission_r_c_cat_T_26)
[1553] FIRRTL:199322 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_28 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[1554] FIRRTL:199323 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_29 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[1555] FIRRTL:199324 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_30 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[1556] FIRRTL:199325 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_31 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[1557] FIRRTL:199326 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_32 = or(_s2_has_permission_r_c_cat_T_28, _s2_has_permission_r_c_cat_T_29)
[1558] FIRRTL:199327 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_33 = or(_s2_has_permission_r_c_cat_T_32, _s2_has_permission_r_c_cat_T_30)
[1559] FIRRTL:199328 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_34 = or(_s2_has_permission_r_c_cat_T_33, _s2_has_permission_r_c_cat_T_31)
[1560] FIRRTL:199329 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_35 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[1561] FIRRTL:199330 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_36 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[1562] FIRRTL:199331 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_37 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[1563] FIRRTL:199332 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_38 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[1564] FIRRTL:199333 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_has_permission_r_c_cat_T_39 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[1565] FIRRTL:199334 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_40 = or(_s2_has_permission_r_c_cat_T_35, _s2_has_permission_r_c_cat_T_36)
[1566] FIRRTL:199335 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_41 = or(_s2_has_permission_r_c_cat_T_40, _s2_has_permission_r_c_cat_T_37)
[1567] FIRRTL:199336 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_42 = or(_s2_has_permission_r_c_cat_T_41, _s2_has_permission_r_c_cat_T_38)
[1568] FIRRTL:199337 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_has_permission_r_c_cat_T_43 = or(_s2_has_permission_r_c_cat_T_42, _s2_has_permission_r_c_cat_T_39)
[1569] FIRRTL:199338 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_has_permission_r_c_cat_T_44 = or(_s2_has_permission_r_c_cat_T_34, _s2_has_permission_r_c_cat_T_43)
[1570] FIRRTL:199339 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s2_has_permission_r_c_cat_T_45 = or(_s2_has_permission_r_c_cat_T_27, _s2_has_permission_r_c_cat_T_44)
[1571] FIRRTL:199340 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _s2_has_permission_r_c_cat_T_46 = eq(s2_req[0].uop.mem_cmd, UInt<2>(0h3))
[1572] FIRRTL:199341 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _s2_has_permission_r_c_cat_T_47 = or(_s2_has_permission_r_c_cat_T_45, _s2_has_permission_r_c_cat_T_46)
[1573] FIRRTL:199342 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _s2_has_permission_r_c_cat_T_48 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h6))
[1574] FIRRTL:199343 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _s2_has_permission_r_c_cat_T_49 = or(_s2_has_permission_r_c_cat_T_47, _s2_has_permission_r_c_cat_T_48)
[1575] FIRRTL:199344 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node s2_has_permission_r_c = cat(_s2_has_permission_r_c_cat_T_22, _s2_has_permission_r_c_cat_T_49)
[1576] FIRRTL:199345 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _s2_has_permission_r_T = cat(s2_has_permission_r_c, s2_hit_state[0].state)
[1577] FIRRTL:199346 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_has_permission_r_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1578] FIRRTL:199347 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _s2_has_permission_r_T_2 = cat(_s2_has_permission_r_T_1, UInt<2>(0h3))
[1579] FIRRTL:199348 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_has_permission_r_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1580] FIRRTL:199349 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _s2_has_permission_r_T_4 = cat(_s2_has_permission_r_T_3, UInt<2>(0h2))
[1581] FIRRTL:199350 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_has_permission_r_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1582] FIRRTL:199351 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _s2_has_permission_r_T_6 = cat(_s2_has_permission_r_T_5, UInt<2>(0h1))
[1583] FIRRTL:199352 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_has_permission_r_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1584] FIRRTL:199353 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _s2_has_permission_r_T_8 = cat(_s2_has_permission_r_T_7, UInt<2>(0h3))
[1585] FIRRTL:199354 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_has_permission_r_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1586] FIRRTL:199355 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _s2_has_permission_r_T_10 = cat(_s2_has_permission_r_T_9, UInt<2>(0h2))
[1587] FIRRTL:199356 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_has_permission_r_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1588] FIRRTL:199357 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _s2_has_permission_r_T_12 = cat(_s2_has_permission_r_T_11, UInt<2>(0h3))
[1589] FIRRTL:199358 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_has_permission_r_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1590] FIRRTL:199359 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _s2_has_permission_r_T_14 = cat(_s2_has_permission_r_T_13, UInt<2>(0h2))
[1591] FIRRTL:199360 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_has_permission_r_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1592] FIRRTL:199361 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _s2_has_permission_r_T_16 = cat(_s2_has_permission_r_T_15, UInt<2>(0h0))
[1593] FIRRTL:199362 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_has_permission_r_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1594] FIRRTL:199363 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _s2_has_permission_r_T_18 = cat(_s2_has_permission_r_T_17, UInt<2>(0h1))
[1595] FIRRTL:199364 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_has_permission_r_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1596] FIRRTL:199365 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _s2_has_permission_r_T_20 = cat(_s2_has_permission_r_T_19, UInt<2>(0h0))
[1597] FIRRTL:199366 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_has_permission_r_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1598] FIRRTL:199367 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _s2_has_permission_r_T_22 = cat(_s2_has_permission_r_T_21, UInt<2>(0h1))
[1599] FIRRTL:199368 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_has_permission_r_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1600] FIRRTL:199369 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _s2_has_permission_r_T_24 = cat(_s2_has_permission_r_T_23, UInt<2>(0h0))
[1601] FIRRTL:199370 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_25 = eq(_s2_has_permission_r_T_24, _s2_has_permission_r_T)
[1602] FIRRTL:199371 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_26 = mux(_s2_has_permission_r_T_25, UInt<1>(0h0), UInt<1>(0h0))
[1603] FIRRTL:199372 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_27 = mux(_s2_has_permission_r_T_25, UInt<2>(0h1), UInt<1>(0h0))
[1604] FIRRTL:199373 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_28 = eq(_s2_has_permission_r_T_22, _s2_has_permission_r_T)
[1605] FIRRTL:199374 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_29 = mux(_s2_has_permission_r_T_28, UInt<1>(0h0), _s2_has_permission_r_T_26)
[1606] FIRRTL:199375 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_30 = mux(_s2_has_permission_r_T_28, UInt<2>(0h2), _s2_has_permission_r_T_27)
[1607] FIRRTL:199376 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_31 = eq(_s2_has_permission_r_T_20, _s2_has_permission_r_T)
[1608] FIRRTL:199377 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_32 = mux(_s2_has_permission_r_T_31, UInt<1>(0h0), _s2_has_permission_r_T_29)
[1609] FIRRTL:199378 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_33 = mux(_s2_has_permission_r_T_31, UInt<2>(0h1), _s2_has_permission_r_T_30)
[1610] FIRRTL:199379 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_34 = eq(_s2_has_permission_r_T_18, _s2_has_permission_r_T)
[1611] FIRRTL:199380 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_35 = mux(_s2_has_permission_r_T_34, UInt<1>(0h0), _s2_has_permission_r_T_32)
[1612] FIRRTL:199381 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_36 = mux(_s2_has_permission_r_T_34, UInt<2>(0h2), _s2_has_permission_r_T_33)
[1613] FIRRTL:199382 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_37 = eq(_s2_has_permission_r_T_16, _s2_has_permission_r_T)
[1614] FIRRTL:199383 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_38 = mux(_s2_has_permission_r_T_37, UInt<1>(0h0), _s2_has_permission_r_T_35)
[1615] FIRRTL:199384 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_39 = mux(_s2_has_permission_r_T_37, UInt<2>(0h0), _s2_has_permission_r_T_36)
[1616] FIRRTL:199385 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_40 = eq(_s2_has_permission_r_T_14, _s2_has_permission_r_T)
[1617] FIRRTL:199386 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_41 = mux(_s2_has_permission_r_T_40, UInt<1>(0h1), _s2_has_permission_r_T_38)
[1618] FIRRTL:199387 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_42 = mux(_s2_has_permission_r_T_40, UInt<2>(0h3), _s2_has_permission_r_T_39)
[1619] FIRRTL:199388 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_43 = eq(_s2_has_permission_r_T_12, _s2_has_permission_r_T)
[1620] FIRRTL:199389 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_44 = mux(_s2_has_permission_r_T_43, UInt<1>(0h1), _s2_has_permission_r_T_41)
[1621] FIRRTL:199390 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_45 = mux(_s2_has_permission_r_T_43, UInt<2>(0h3), _s2_has_permission_r_T_42)
[1622] FIRRTL:199391 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_46 = eq(_s2_has_permission_r_T_10, _s2_has_permission_r_T)
[1623] FIRRTL:199392 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_47 = mux(_s2_has_permission_r_T_46, UInt<1>(0h1), _s2_has_permission_r_T_44)
[1624] FIRRTL:199393 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_48 = mux(_s2_has_permission_r_T_46, UInt<2>(0h2), _s2_has_permission_r_T_45)
[1625] FIRRTL:199394 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_49 = eq(_s2_has_permission_r_T_8, _s2_has_permission_r_T)
[1626] FIRRTL:199395 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_50 = mux(_s2_has_permission_r_T_49, UInt<1>(0h1), _s2_has_permission_r_T_47)
[1627] FIRRTL:199396 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_51 = mux(_s2_has_permission_r_T_49, UInt<2>(0h3), _s2_has_permission_r_T_48)
[1628] FIRRTL:199397 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_52 = eq(_s2_has_permission_r_T_6, _s2_has_permission_r_T)
[1629] FIRRTL:199398 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_53 = mux(_s2_has_permission_r_T_52, UInt<1>(0h1), _s2_has_permission_r_T_50)
[1630] FIRRTL:199399 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_54 = mux(_s2_has_permission_r_T_52, UInt<2>(0h1), _s2_has_permission_r_T_51)
[1631] FIRRTL:199400 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_55 = eq(_s2_has_permission_r_T_4, _s2_has_permission_r_T)
[1632] FIRRTL:199401 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_has_permission_r_T_56 = mux(_s2_has_permission_r_T_55, UInt<1>(0h1), _s2_has_permission_r_T_53)
[1633] FIRRTL:199402 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_has_permission_r_T_57 = mux(_s2_has_permission_r_T_55, UInt<2>(0h2), _s2_has_permission_r_T_54)
[1634] FIRRTL:199403 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_has_permission_r_T_58 = eq(_s2_has_permission_r_T_2, _s2_has_permission_r_T)
[1635] FIRRTL:199404 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node s2_has_permission_r_1 = mux(_s2_has_permission_r_T_58, UInt<1>(0h1), _s2_has_permission_r_T_56)
[1636] FIRRTL:199405 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node s2_has_permission_r_2 = mux(_s2_has_permission_r_T_58, UInt<2>(0h3), _s2_has_permission_r_T_57)
[1637] FIRRTL:199406 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire s2_has_permission_meta : { state : UInt<2>}
[1638] FIRRTL:199407 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect s2_has_permission_meta.state, s2_has_permission_r_2
[1639] FIRRTL:199408 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_has_permission : UInt<1>[1]
[1640] FIRRTL:199409 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_has_permission[0], s2_has_permission_r_1
[1641] FIRRTL:199410 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s2_new_hit_state_r_c_cat_T = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[1642] FIRRTL:199411 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s2_new_hit_state_r_c_cat_T_1 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[1643] FIRRTL:199412 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s2_new_hit_state_r_c_cat_T_2 = or(_s2_new_hit_state_r_c_cat_T, _s2_new_hit_state_r_c_cat_T_1)
[1644] FIRRTL:199413 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s2_new_hit_state_r_c_cat_T_3 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[1645] FIRRTL:199414 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_4 = or(_s2_new_hit_state_r_c_cat_T_2, _s2_new_hit_state_r_c_cat_T_3)
[1646] FIRRTL:199415 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_5 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[1647] FIRRTL:199416 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_6 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[1648] FIRRTL:199417 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_7 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[1649] FIRRTL:199418 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_8 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[1650] FIRRTL:199419 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_9 = or(_s2_new_hit_state_r_c_cat_T_5, _s2_new_hit_state_r_c_cat_T_6)
[1651] FIRRTL:199420 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_10 = or(_s2_new_hit_state_r_c_cat_T_9, _s2_new_hit_state_r_c_cat_T_7)
[1652] FIRRTL:199421 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_11 = or(_s2_new_hit_state_r_c_cat_T_10, _s2_new_hit_state_r_c_cat_T_8)
[1653] FIRRTL:199422 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_12 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[1654] FIRRTL:199423 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_13 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[1655] FIRRTL:199424 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_14 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[1656] FIRRTL:199425 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_15 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[1657] FIRRTL:199426 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_16 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[1658] FIRRTL:199427 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_17 = or(_s2_new_hit_state_r_c_cat_T_12, _s2_new_hit_state_r_c_cat_T_13)
[1659] FIRRTL:199428 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_18 = or(_s2_new_hit_state_r_c_cat_T_17, _s2_new_hit_state_r_c_cat_T_14)
[1660] FIRRTL:199429 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_19 = or(_s2_new_hit_state_r_c_cat_T_18, _s2_new_hit_state_r_c_cat_T_15)
[1661] FIRRTL:199430 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_20 = or(_s2_new_hit_state_r_c_cat_T_19, _s2_new_hit_state_r_c_cat_T_16)
[1662] FIRRTL:199431 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_new_hit_state_r_c_cat_T_21 = or(_s2_new_hit_state_r_c_cat_T_11, _s2_new_hit_state_r_c_cat_T_20)
[1663] FIRRTL:199432 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s2_new_hit_state_r_c_cat_T_22 = or(_s2_new_hit_state_r_c_cat_T_4, _s2_new_hit_state_r_c_cat_T_21)
[1664] FIRRTL:199433 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s2_new_hit_state_r_c_cat_T_23 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[1665] FIRRTL:199434 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s2_new_hit_state_r_c_cat_T_24 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[1666] FIRRTL:199435 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s2_new_hit_state_r_c_cat_T_25 = or(_s2_new_hit_state_r_c_cat_T_23, _s2_new_hit_state_r_c_cat_T_24)
[1667] FIRRTL:199436 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s2_new_hit_state_r_c_cat_T_26 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[1668] FIRRTL:199437 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_27 = or(_s2_new_hit_state_r_c_cat_T_25, _s2_new_hit_state_r_c_cat_T_26)
[1669] FIRRTL:199438 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_28 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[1670] FIRRTL:199439 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_29 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[1671] FIRRTL:199440 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_30 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[1672] FIRRTL:199441 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_31 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[1673] FIRRTL:199442 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_32 = or(_s2_new_hit_state_r_c_cat_T_28, _s2_new_hit_state_r_c_cat_T_29)
[1674] FIRRTL:199443 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_33 = or(_s2_new_hit_state_r_c_cat_T_32, _s2_new_hit_state_r_c_cat_T_30)
[1675] FIRRTL:199444 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_34 = or(_s2_new_hit_state_r_c_cat_T_33, _s2_new_hit_state_r_c_cat_T_31)
[1676] FIRRTL:199445 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_35 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[1677] FIRRTL:199446 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_36 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[1678] FIRRTL:199447 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_37 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[1679] FIRRTL:199448 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_38 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[1680] FIRRTL:199449 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_39 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[1681] FIRRTL:199450 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_40 = or(_s2_new_hit_state_r_c_cat_T_35, _s2_new_hit_state_r_c_cat_T_36)
[1682] FIRRTL:199451 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_41 = or(_s2_new_hit_state_r_c_cat_T_40, _s2_new_hit_state_r_c_cat_T_37)
[1683] FIRRTL:199452 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_42 = or(_s2_new_hit_state_r_c_cat_T_41, _s2_new_hit_state_r_c_cat_T_38)
[1684] FIRRTL:199453 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_new_hit_state_r_c_cat_T_43 = or(_s2_new_hit_state_r_c_cat_T_42, _s2_new_hit_state_r_c_cat_T_39)
[1685] FIRRTL:199454 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_new_hit_state_r_c_cat_T_44 = or(_s2_new_hit_state_r_c_cat_T_34, _s2_new_hit_state_r_c_cat_T_43)
[1686] FIRRTL:199455 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s2_new_hit_state_r_c_cat_T_45 = or(_s2_new_hit_state_r_c_cat_T_27, _s2_new_hit_state_r_c_cat_T_44)
[1687] FIRRTL:199456 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _s2_new_hit_state_r_c_cat_T_46 = eq(s2_req[0].uop.mem_cmd, UInt<2>(0h3))
[1688] FIRRTL:199457 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _s2_new_hit_state_r_c_cat_T_47 = or(_s2_new_hit_state_r_c_cat_T_45, _s2_new_hit_state_r_c_cat_T_46)
[1689] FIRRTL:199458 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _s2_new_hit_state_r_c_cat_T_48 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h6))
[1690] FIRRTL:199459 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _s2_new_hit_state_r_c_cat_T_49 = or(_s2_new_hit_state_r_c_cat_T_47, _s2_new_hit_state_r_c_cat_T_48)
[1691] FIRRTL:199460 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node s2_new_hit_state_r_c = cat(_s2_new_hit_state_r_c_cat_T_22, _s2_new_hit_state_r_c_cat_T_49)
[1692] FIRRTL:199461 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _s2_new_hit_state_r_T = cat(s2_new_hit_state_r_c, s2_hit_state[0].state)
[1693] FIRRTL:199462 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_new_hit_state_r_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1694] FIRRTL:199463 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _s2_new_hit_state_r_T_2 = cat(_s2_new_hit_state_r_T_1, UInt<2>(0h3))
[1695] FIRRTL:199464 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_new_hit_state_r_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1696] FIRRTL:199465 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _s2_new_hit_state_r_T_4 = cat(_s2_new_hit_state_r_T_3, UInt<2>(0h2))
[1697] FIRRTL:199466 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_new_hit_state_r_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1698] FIRRTL:199467 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _s2_new_hit_state_r_T_6 = cat(_s2_new_hit_state_r_T_5, UInt<2>(0h1))
[1699] FIRRTL:199468 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_new_hit_state_r_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1700] FIRRTL:199469 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _s2_new_hit_state_r_T_8 = cat(_s2_new_hit_state_r_T_7, UInt<2>(0h3))
[1701] FIRRTL:199470 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_new_hit_state_r_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1702] FIRRTL:199471 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _s2_new_hit_state_r_T_10 = cat(_s2_new_hit_state_r_T_9, UInt<2>(0h2))
[1703] FIRRTL:199472 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_new_hit_state_r_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1704] FIRRTL:199473 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _s2_new_hit_state_r_T_12 = cat(_s2_new_hit_state_r_T_11, UInt<2>(0h3))
[1705] FIRRTL:199474 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_new_hit_state_r_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1706] FIRRTL:199475 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _s2_new_hit_state_r_T_14 = cat(_s2_new_hit_state_r_T_13, UInt<2>(0h2))
[1707] FIRRTL:199476 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _s2_new_hit_state_r_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1708] FIRRTL:199477 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _s2_new_hit_state_r_T_16 = cat(_s2_new_hit_state_r_T_15, UInt<2>(0h0))
[1709] FIRRTL:199478 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_new_hit_state_r_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1710] FIRRTL:199479 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _s2_new_hit_state_r_T_18 = cat(_s2_new_hit_state_r_T_17, UInt<2>(0h1))
[1711] FIRRTL:199480 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _s2_new_hit_state_r_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1712] FIRRTL:199481 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _s2_new_hit_state_r_T_20 = cat(_s2_new_hit_state_r_T_19, UInt<2>(0h0))
[1713] FIRRTL:199482 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_new_hit_state_r_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1714] FIRRTL:199483 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _s2_new_hit_state_r_T_22 = cat(_s2_new_hit_state_r_T_21, UInt<2>(0h1))
[1715] FIRRTL:199484 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _s2_new_hit_state_r_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1716] FIRRTL:199485 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _s2_new_hit_state_r_T_24 = cat(_s2_new_hit_state_r_T_23, UInt<2>(0h0))
[1717] FIRRTL:199486 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_25 = eq(_s2_new_hit_state_r_T_24, _s2_new_hit_state_r_T)
[1718] FIRRTL:199487 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_26 = mux(_s2_new_hit_state_r_T_25, UInt<1>(0h0), UInt<1>(0h0))
[1719] FIRRTL:199488 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_27 = mux(_s2_new_hit_state_r_T_25, UInt<2>(0h1), UInt<1>(0h0))
[1720] FIRRTL:199489 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_28 = eq(_s2_new_hit_state_r_T_22, _s2_new_hit_state_r_T)
[1721] FIRRTL:199490 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_29 = mux(_s2_new_hit_state_r_T_28, UInt<1>(0h0), _s2_new_hit_state_r_T_26)
[1722] FIRRTL:199491 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_30 = mux(_s2_new_hit_state_r_T_28, UInt<2>(0h2), _s2_new_hit_state_r_T_27)
[1723] FIRRTL:199492 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_31 = eq(_s2_new_hit_state_r_T_20, _s2_new_hit_state_r_T)
[1724] FIRRTL:199493 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_32 = mux(_s2_new_hit_state_r_T_31, UInt<1>(0h0), _s2_new_hit_state_r_T_29)
[1725] FIRRTL:199494 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_33 = mux(_s2_new_hit_state_r_T_31, UInt<2>(0h1), _s2_new_hit_state_r_T_30)
[1726] FIRRTL:199495 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_34 = eq(_s2_new_hit_state_r_T_18, _s2_new_hit_state_r_T)
[1727] FIRRTL:199496 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_35 = mux(_s2_new_hit_state_r_T_34, UInt<1>(0h0), _s2_new_hit_state_r_T_32)
[1728] FIRRTL:199497 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_36 = mux(_s2_new_hit_state_r_T_34, UInt<2>(0h2), _s2_new_hit_state_r_T_33)
[1729] FIRRTL:199498 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_37 = eq(_s2_new_hit_state_r_T_16, _s2_new_hit_state_r_T)
[1730] FIRRTL:199499 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_38 = mux(_s2_new_hit_state_r_T_37, UInt<1>(0h0), _s2_new_hit_state_r_T_35)
[1731] FIRRTL:199500 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_39 = mux(_s2_new_hit_state_r_T_37, UInt<2>(0h0), _s2_new_hit_state_r_T_36)
[1732] FIRRTL:199501 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_40 = eq(_s2_new_hit_state_r_T_14, _s2_new_hit_state_r_T)
[1733] FIRRTL:199502 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_41 = mux(_s2_new_hit_state_r_T_40, UInt<1>(0h1), _s2_new_hit_state_r_T_38)
[1734] FIRRTL:199503 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_42 = mux(_s2_new_hit_state_r_T_40, UInt<2>(0h3), _s2_new_hit_state_r_T_39)
[1735] FIRRTL:199504 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_43 = eq(_s2_new_hit_state_r_T_12, _s2_new_hit_state_r_T)
[1736] FIRRTL:199505 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_44 = mux(_s2_new_hit_state_r_T_43, UInt<1>(0h1), _s2_new_hit_state_r_T_41)
[1737] FIRRTL:199506 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_45 = mux(_s2_new_hit_state_r_T_43, UInt<2>(0h3), _s2_new_hit_state_r_T_42)
[1738] FIRRTL:199507 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_46 = eq(_s2_new_hit_state_r_T_10, _s2_new_hit_state_r_T)
[1739] FIRRTL:199508 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_47 = mux(_s2_new_hit_state_r_T_46, UInt<1>(0h1), _s2_new_hit_state_r_T_44)
[1740] FIRRTL:199509 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_48 = mux(_s2_new_hit_state_r_T_46, UInt<2>(0h2), _s2_new_hit_state_r_T_45)
[1741] FIRRTL:199510 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_49 = eq(_s2_new_hit_state_r_T_8, _s2_new_hit_state_r_T)
[1742] FIRRTL:199511 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_50 = mux(_s2_new_hit_state_r_T_49, UInt<1>(0h1), _s2_new_hit_state_r_T_47)
[1743] FIRRTL:199512 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_51 = mux(_s2_new_hit_state_r_T_49, UInt<2>(0h3), _s2_new_hit_state_r_T_48)
[1744] FIRRTL:199513 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_52 = eq(_s2_new_hit_state_r_T_6, _s2_new_hit_state_r_T)
[1745] FIRRTL:199514 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_53 = mux(_s2_new_hit_state_r_T_52, UInt<1>(0h1), _s2_new_hit_state_r_T_50)
[1746] FIRRTL:199515 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_54 = mux(_s2_new_hit_state_r_T_52, UInt<2>(0h1), _s2_new_hit_state_r_T_51)
[1747] FIRRTL:199516 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_55 = eq(_s2_new_hit_state_r_T_4, _s2_new_hit_state_r_T)
[1748] FIRRTL:199517 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _s2_new_hit_state_r_T_56 = mux(_s2_new_hit_state_r_T_55, UInt<1>(0h1), _s2_new_hit_state_r_T_53)
[1749] FIRRTL:199518 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _s2_new_hit_state_r_T_57 = mux(_s2_new_hit_state_r_T_55, UInt<2>(0h2), _s2_new_hit_state_r_T_54)
[1750] FIRRTL:199519 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _s2_new_hit_state_r_T_58 = eq(_s2_new_hit_state_r_T_2, _s2_new_hit_state_r_T)
[1751] FIRRTL:199520 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node s2_new_hit_state_r_1 = mux(_s2_new_hit_state_r_T_58, UInt<1>(0h1), _s2_new_hit_state_r_T_56)
[1752] FIRRTL:199521 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node s2_new_hit_state_r_2 = mux(_s2_new_hit_state_r_T_58, UInt<2>(0h3), _s2_new_hit_state_r_T_57)
[1753] FIRRTL:199522 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire s2_new_hit_state_meta : { state : UInt<2>}
[1754] FIRRTL:199523 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect s2_new_hit_state_meta.state, s2_new_hit_state_r_2
[1755] FIRRTL:199524 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_new_hit_state : { state : UInt<2>}[1]
[1756] FIRRTL:199525 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_new_hit_state[0], s2_new_hit_state_meta
[1757] FIRRTL:199526 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:687:47 KIND:node :: node _s2_hit_T = and(s2_tag_match_0, s2_has_permission[0])
[1758] FIRRTL:199527 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:46:46 KIND:node :: node _s2_hit_T_1 = eq(s2_hit_state[0].state, s2_new_hit_state[0].state)
[1759] FIRRTL:199528 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:687:71 KIND:node :: node _s2_hit_T_2 = and(_s2_hit_T, _s2_hit_T_1)
[1760] FIRRTL:199529 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:687:117 KIND:node :: node _s2_hit_T_3 = eq(mshrs.io.block_hit[0], UInt<1>(0h0))
[1761] FIRRTL:199530 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:687:114 KIND:node :: node _s2_hit_T_4 = and(_s2_hit_T_2, _s2_hit_T_3)
[1762] FIRRTL:199531 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_hit_T_5 = eq(s2_type, UInt<3>(0h0))
[1763] FIRRTL:199532 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_hit_T_6 = eq(s2_type, UInt<3>(0h2))
[1764] FIRRTL:199533 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_hit_T_7 = or(_s2_hit_T_5, _s2_hit_T_6)
[1765] FIRRTL:199534 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:687:141 KIND:node :: node _s2_hit_T_8 = or(_s2_hit_T_4, _s2_hit_T_7)
[1766] FIRRTL:199535 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_hit : UInt<1>[1]
[1767] FIRRTL:199536 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_hit[0], _s2_hit_T_8
[1768] FIRRTL:199537 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:688:21 KIND:wire :: wire s2_nack : UInt<1>[1]
[1769] FIRRTL:199538 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:20 KIND:node :: node _T_16 = eq(s2_type, UInt<3>(0h0))
[1770] FIRRTL:199539 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:36 KIND:node :: node _T_17 = eq(s2_hit[0], UInt<1>(0h0))
[1771] FIRRTL:199540 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:33 KIND:node :: node _T_18 = and(_T_16, _T_17)
[1772] FIRRTL:199541 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:10 KIND:node :: node _T_19 = eq(_T_18, UInt<1>(0h0))
[1773] FIRRTL:199542 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:node :: node _T_20 = asUInt(reset)
[1774] FIRRTL:199543 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:node :: node _T_21 = eq(_T_20, UInt<1>(0h0))
[1775] FIRRTL:199544 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:when :: when _T_21 :
[1776] FIRRTL:199545 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:node :: node _T_22 = eq(_T_19, UInt<1>(0h0))
[1777] FIRRTL:199546 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:when :: when _T_22 :
[1778] FIRRTL:199547 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: Replays should always hit\n    at dcache.scala:689 assert(!(s2_type === t_replay && !s2_hit(0)), \"Replays should always hit\")\n") : printf_2
[1779] FIRRTL:199548 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:689:9 KIND:nondriving :: assert(clock, _T_19, UInt<1>(0h1), "") : assert_2
[1780] FIRRTL:199549 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:20 KIND:node :: node _T_23 = eq(s2_type, UInt<3>(0h2))
[1781] FIRRTL:199550 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:32 KIND:node :: node _T_24 = eq(s2_hit[0], UInt<1>(0h0))
[1782] FIRRTL:199551 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:29 KIND:node :: node _T_25 = and(_T_23, _T_24)
[1783] FIRRTL:199552 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:10 KIND:node :: node _T_26 = eq(_T_25, UInt<1>(0h0))
[1784] FIRRTL:199553 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:node :: node _T_27 = asUInt(reset)
[1785] FIRRTL:199554 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:node :: node _T_28 = eq(_T_27, UInt<1>(0h0))
[1786] FIRRTL:199555 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:when :: when _T_28 :
[1787] FIRRTL:199556 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:node :: node _T_29 = eq(_T_26, UInt<1>(0h0))
[1788] FIRRTL:199557 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:when :: when _T_29 :
[1789] FIRRTL:199558 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: Writeback should always see data hit\n    at dcache.scala:690 assert(!(s2_type === t_wb && !s2_hit(0)), \"Writeback should always see data hit\")\n") : printf_3
[1790] FIRRTL:199559 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:690:9 KIND:nondriving :: assert(clock, _T_26, UInt<1>(0h1), "") : assert_3
[1791] FIRRTL:199560 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:692:34 KIND:reg :: reg s2_wb_idx_matches : UInt<1>[1], clock
[1793] FIRRTL:199562 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:695:35 KIND:regreset :: regreset debug_sc_fail_addr : UInt, clock, reset, UInt<1>(0h0)
[1794] FIRRTL:199563 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:696:35 KIND:regreset :: regreset debug_sc_fail_cnt : UInt<8>, clock, reset, UInt<8>(0h0)
[1795] FIRRTL:199564 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:698:27 KIND:regreset :: regreset lrsc_count : UInt<7>, clock, reset, UInt<7>(0h0)
[1796] FIRRTL:199565 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:699:31 KIND:node :: node lrsc_valid = gt(lrsc_count, UInt<2>(0h3))
[1797] FIRRTL:199566 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:700:23 KIND:reg :: reg lrsc_addr : UInt, clock
[1798] FIRRTL:199567 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:37 KIND:node :: node _s2_lr_T = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h6))
[1799] FIRRTL:199568 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:59 KIND:reg :: reg s2_lr_REG : UInt<1>, clock
[1800] FIRRTL:199569 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:59 KIND:connect :: connect s2_lr_REG, s1_nack_0
[1802] FIRRTL:199571 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:701:83 KIND:node :: node _s2_lr_T_2 = eq(s2_type, UInt<3>(0h0))
[1806] FIRRTL:199575 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:59 KIND:reg :: reg s2_sc_REG : UInt<1>, clock
[1807] FIRRTL:199576 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:59 KIND:connect :: connect s2_sc_REG, s1_nack_0
[1812] FIRRTL:199581 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:703:86 KIND:node :: node _s2_lrsc_addr_match_T = shr(s2_req[0].addr, 6)
[1813] FIRRTL:199582 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:703:66 KIND:node :: node _s2_lrsc_addr_match_T_1 = eq(lrsc_addr, _s2_lrsc_addr_match_T)
[1814] FIRRTL:199583 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:703:53 KIND:node :: node _s2_lrsc_addr_match_T_2 = and(lrsc_valid, _s2_lrsc_addr_match_T_1)
[1815] FIRRTL:199584 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_lrsc_addr_match : UInt<1>[1]
[1816] FIRRTL:199585 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_lrsc_addr_match[0], _s2_lrsc_addr_match_T_2
[1824] FIRRTL:199593 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:706:34 KIND:node :: node _T_31 = eq(s2_type, UInt<3>(0h4))
[1828] FIRRTL:199597 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:707:31 KIND:node :: node _T_35 = eq(s2_type, UInt<3>(0h0))
[1829] FIRRTL:199598 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:707:69 KIND:node :: node _T_36 = neq(s2_req[0].uop.mem_cmd, UInt<3>(0h5))
[1836] FIRRTL:199605 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:710:35 KIND:node :: node _lrsc_addr_T = shr(s2_req[0].addr, 6)
[1837] FIRRTL:199606 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:710:17 KIND:connect :: connect lrsc_addr, _lrsc_addr_T
[1841] FIRRTL:199610 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:718:15 KIND:node :: node _T_41 = eq(s2_type, UInt<3>(0h4))
[1853] FIRRTL:199622 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:727:22 KIND:when :: when s2_valid[0] :
[1854] FIRRTL:199623 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:728:26 KIND:node :: node _T_51 = eq(s2_req[0].addr, debug_sc_fail_addr)
[1855] FIRRTL:199624 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:728:50 KIND:when :: when _T_51 :
[1856] FIRRTL:199625 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:729:25 KIND:when :: when s2_sc_fail :
[1857] FIRRTL:199626 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:730:48 KIND:node :: node _debug_sc_fail_cnt_T = add(debug_sc_fail_cnt, UInt<1>(0h1))
[1858] FIRRTL:199627 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:730:48 KIND:node :: node _debug_sc_fail_cnt_T_1 = tail(_debug_sc_fail_cnt_T, 1)
[1859] FIRRTL:199628 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:730:27 KIND:connect :: connect debug_sc_fail_cnt, _debug_sc_fail_cnt_T_1
[1860] FIRRTL:199629 SRC:<no-source-locator> KIND:else :: else :
[1861] FIRRTL:199630 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:731:27 KIND:when :: when s2_sc :
[1862] FIRRTL:199631 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:732:27 KIND:connect :: connect debug_sc_fail_cnt, UInt<1>(0h0)
[1863] FIRRTL:199632 SRC:<no-source-locator> KIND:else :: else :
[1864] FIRRTL:199633 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:735:25 KIND:when :: when s2_sc_fail :
[1865] FIRRTL:199634 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:736:28 KIND:connect :: connect debug_sc_fail_addr, s2_req[0].addr
[1866] FIRRTL:199635 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:737:28 KIND:connect :: connect debug_sc_fail_cnt, UInt<1>(0h1)
[1867] FIRRTL:199636 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:28 KIND:node :: node _T_52 = lt(debug_sc_fail_cnt, UInt<7>(0h64))
[1868] FIRRTL:199637 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:node :: node _T_53 = asUInt(reset)
[1869] FIRRTL:199638 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:node :: node _T_54 = eq(_T_53, UInt<1>(0h0))
[1870] FIRRTL:199639 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:when :: when _T_54 :
[1871] FIRRTL:199640 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:node :: node _T_55 = eq(_T_52, UInt<1>(0h0))
[1872] FIRRTL:199641 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:when :: when _T_55 :
[1873] FIRRTL:199642 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: L1DCache failed too many SCs in a row\n    at dcache.scala:741 assert(debug_sc_fail_cnt < 100.U, \"L1DCache failed too many SCs in a row\")\n") : printf_4
[1874] FIRRTL:199643 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:741:9 KIND:nondriving :: assert(clock, _T_52, UInt<1>(0h1), "") : assert_4
[1875] FIRRTL:199644 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:743:21 KIND:wire :: wire s2_data : UInt<64>[4][1]
[1891] FIRRTL:199660 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_data_muxed_WIRE : UInt<64>
[1893] FIRRTL:199662 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_data_muxed : UInt<64>[1]
[1895] FIRRTL:199664 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_word_idx : UInt<1>[1]
[1897] FIRRTL:199666 SRC:generators/rocket-chip/src/main/scala/util/Replacement.scala:37:29 KIND:wire :: wire replace : UInt<1>
[1898] FIRRTL:199667 SRC:generators/rocket-chip/src/main/scala/util/Replacement.scala:38:11 KIND:connect :: connect replace, UInt<1>(0h0)
[1899] FIRRTL:199668 SRC:src/main/scala/chisel3/util/random/PRNG.scala:91:22 KIND:structural :: inst lfsr_prng of MaxPeriodFibonacciLFSR_1
[1900] FIRRTL:199669 SRC:<no-source-locator> KIND:connect :: connect lfsr_prng.clock, clock
[1901] FIRRTL:199670 SRC:<no-source-locator> KIND:connect :: connect lfsr_prng.reset, reset
[1902] FIRRTL:199671 SRC:src/main/scala/chisel3/util/random/PRNG.scala:92:24 KIND:connect :: connect lfsr_prng.io.seed.valid, UInt<1>(0h0)
[1903] FIRRTL:199672 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[0]
[1904] FIRRTL:199673 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[1]
[1905] FIRRTL:199674 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[2]
[1906] FIRRTL:199675 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[3]
[1907] FIRRTL:199676 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[4]
[1908] FIRRTL:199677 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[5]
[1909] FIRRTL:199678 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[6]
[1910] FIRRTL:199679 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[7]
[1911] FIRRTL:199680 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[8]
[1912] FIRRTL:199681 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[9]
[1913] FIRRTL:199682 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[10]
[1914] FIRRTL:199683 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[11]
[1915] FIRRTL:199684 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[12]
[1916] FIRRTL:199685 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[13]
[1917] FIRRTL:199686 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[14]
[1918] FIRRTL:199687 SRC:src/main/scala/chisel3/util/random/PRNG.scala:93:23 KIND:invalidate :: invalidate lfsr_prng.io.seed.bits[15]
[1919] FIRRTL:199688 SRC:src/main/scala/chisel3/util/random/PRNG.scala:94:23 KIND:connect :: connect lfsr_prng.io.increment, replace
[1920] FIRRTL:199689 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_lo_lo = cat(lfsr_prng.io.out[1], lfsr_prng.io.out[0])
[1921] FIRRTL:199690 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_lo_hi = cat(lfsr_prng.io.out[3], lfsr_prng.io.out[2])
[1922] FIRRTL:199691 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_lo = cat(lfsr_lo_lo_hi, lfsr_lo_lo_lo)
[1923] FIRRTL:199692 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_hi_lo = cat(lfsr_prng.io.out[5], lfsr_prng.io.out[4])
[1924] FIRRTL:199693 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_hi_hi = cat(lfsr_prng.io.out[7], lfsr_prng.io.out[6])
[1925] FIRRTL:199694 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo_hi = cat(lfsr_lo_hi_hi, lfsr_lo_hi_lo)
[1926] FIRRTL:199695 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_lo = cat(lfsr_lo_hi, lfsr_lo_lo)
[1927] FIRRTL:199696 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_lo_lo = cat(lfsr_prng.io.out[9], lfsr_prng.io.out[8])
[1928] FIRRTL:199697 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_lo_hi = cat(lfsr_prng.io.out[11], lfsr_prng.io.out[10])
[1929] FIRRTL:199698 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_lo = cat(lfsr_hi_lo_hi, lfsr_hi_lo_lo)
[1930] FIRRTL:199699 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_hi_lo = cat(lfsr_prng.io.out[13], lfsr_prng.io.out[12])
[1931] FIRRTL:199700 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_hi_hi = cat(lfsr_prng.io.out[15], lfsr_prng.io.out[14])
[1932] FIRRTL:199701 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi_hi = cat(lfsr_hi_hi_hi, lfsr_hi_hi_lo)
[1933] FIRRTL:199702 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr_hi = cat(lfsr_hi_hi, lfsr_hi_lo)
[1934] FIRRTL:199703 SRC:src/main/scala/chisel3/util/random/PRNG.scala:95:17 KIND:node :: node lfsr = cat(lfsr_hi, lfsr_lo)
[1935] FIRRTL:199704 SRC:generators/rocket-chip/src/main/scala/util/package.scala:164:13 KIND:node :: node _s1_replaced_way_en_T = bits(lfsr, 1, 0)
[1936] FIRRTL:199705 SRC:src/main/scala/chisel3/util/OneHot.scala:58:35 KIND:node :: node s1_replaced_way_en = dshl(UInt<1>(0h1), _s1_replaced_way_en_T)
[1937] FIRRTL:199706 SRC:generators/rocket-chip/src/main/scala/util/package.scala:164:13 KIND:node :: node _s2_replaced_way_en_T = bits(lfsr, 1, 0)
[1938] FIRRTL:199707 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:756:44 KIND:reg :: reg s2_replaced_way_en_REG : UInt, clock
[1939] FIRRTL:199708 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:756:44 KIND:connect :: connect s2_replaced_way_en_REG, _s2_replaced_way_en_T
[1940] FIRRTL:199709 SRC:src/main/scala/chisel3/util/OneHot.scala:58:35 KIND:node :: node s2_replaced_way_en = dshl(UInt<1>(0h1), s2_replaced_way_en_REG)
[1941] FIRRTL:199710 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:reg :: reg s2_repl_meta_REG : { coh : { state : UInt<2>}, tag : UInt<20>}, clock
[1942] FIRRTL:199711 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:connect :: connect s2_repl_meta_REG, meta_0.io.resp[0]
[1943] FIRRTL:199712 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:reg :: reg s2_repl_meta_REG_1 : { coh : { state : UInt<2>}, tag : UInt<20>}, clock
[1944] FIRRTL:199713 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:connect :: connect s2_repl_meta_REG_1, meta_0.io.resp[1]
[1945] FIRRTL:199714 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:reg :: reg s2_repl_meta_REG_2 : { coh : { state : UInt<2>}, tag : UInt<20>}, clock
[1946] FIRRTL:199715 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:connect :: connect s2_repl_meta_REG_2, meta_0.io.resp[2]
[1947] FIRRTL:199716 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:reg :: reg s2_repl_meta_REG_3 : { coh : { state : UInt<2>}, tag : UInt<20>}, clock
[1948] FIRRTL:199717 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:757:88 KIND:connect :: connect s2_repl_meta_REG_3, meta_0.io.resp[3]
[1949] FIRRTL:199718 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:wire :: wire _s2_repl_meta_WIRE : { coh : { state : UInt<2>}, tag : UInt<20>}[4]
[1950] FIRRTL:199719 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_repl_meta_WIRE[0], s2_repl_meta_REG
[1951] FIRRTL:199720 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_repl_meta_WIRE[1], s2_repl_meta_REG_1
[1952] FIRRTL:199721 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_repl_meta_WIRE[2], s2_repl_meta_REG_2
[1953] FIRRTL:199722 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s2_repl_meta_WIRE[3], s2_repl_meta_REG_3
[1954] FIRRTL:199723 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_repl_meta_T = bits(s2_replaced_way_en, 0, 0)
[1955] FIRRTL:199724 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_repl_meta_T_1 = bits(s2_replaced_way_en, 1, 1)
[1956] FIRRTL:199725 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_repl_meta_T_2 = bits(s2_replaced_way_en, 2, 2)
[1957] FIRRTL:199726 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_repl_meta_T_3 = bits(s2_replaced_way_en, 3, 3)
[1958] FIRRTL:199727 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_repl_meta_WIRE_1 : { coh : { state : UInt<2>}, tag : UInt<20>}
[1959] FIRRTL:199728 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_4 = mux(_s2_repl_meta_T, _s2_repl_meta_WIRE[0].tag, UInt<1>(0h0))
[1960] FIRRTL:199729 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_5 = mux(_s2_repl_meta_T_1, _s2_repl_meta_WIRE[1].tag, UInt<1>(0h0))
[1961] FIRRTL:199730 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_6 = mux(_s2_repl_meta_T_2, _s2_repl_meta_WIRE[2].tag, UInt<1>(0h0))
[1962] FIRRTL:199731 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_7 = mux(_s2_repl_meta_T_3, _s2_repl_meta_WIRE[3].tag, UInt<1>(0h0))
[1963] FIRRTL:199732 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_8 = or(_s2_repl_meta_T_4, _s2_repl_meta_T_5)
[1964] FIRRTL:199733 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_9 = or(_s2_repl_meta_T_8, _s2_repl_meta_T_6)
[1965] FIRRTL:199734 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_10 = or(_s2_repl_meta_T_9, _s2_repl_meta_T_7)
[1966] FIRRTL:199735 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_repl_meta_WIRE_2 : UInt<20>
[1967] FIRRTL:199736 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_repl_meta_WIRE_2, _s2_repl_meta_T_10
[1968] FIRRTL:199737 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_repl_meta_WIRE_1.tag, _s2_repl_meta_WIRE_2
[1969] FIRRTL:199738 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_repl_meta_WIRE_3 : { state : UInt<2>}
[1970] FIRRTL:199739 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_11 = mux(_s2_repl_meta_T, _s2_repl_meta_WIRE[0].coh.state, UInt<1>(0h0))
[1971] FIRRTL:199740 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_12 = mux(_s2_repl_meta_T_1, _s2_repl_meta_WIRE[1].coh.state, UInt<1>(0h0))
[1972] FIRRTL:199741 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_13 = mux(_s2_repl_meta_T_2, _s2_repl_meta_WIRE[2].coh.state, UInt<1>(0h0))
[1973] FIRRTL:199742 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_14 = mux(_s2_repl_meta_T_3, _s2_repl_meta_WIRE[3].coh.state, UInt<1>(0h0))
[1974] FIRRTL:199743 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_15 = or(_s2_repl_meta_T_11, _s2_repl_meta_T_12)
[1975] FIRRTL:199744 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_16 = or(_s2_repl_meta_T_15, _s2_repl_meta_T_13)
[1976] FIRRTL:199745 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_repl_meta_T_17 = or(_s2_repl_meta_T_16, _s2_repl_meta_T_14)
[1977] FIRRTL:199746 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _s2_repl_meta_WIRE_4 : UInt<2>
[1978] FIRRTL:199747 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_repl_meta_WIRE_4, _s2_repl_meta_T_17
[1979] FIRRTL:199748 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_repl_meta_WIRE_3.state, _s2_repl_meta_WIRE_4
[1980] FIRRTL:199749 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_repl_meta_WIRE_1.coh, _s2_repl_meta_WIRE_3
[1981] FIRRTL:199750 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_repl_meta : { coh : { state : UInt<2>}, tag : UInt<20>}[1]
[1982] FIRRTL:199751 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_repl_meta[0], _s2_repl_meta_WIRE_1
[1983] FIRRTL:199752 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:760:39 KIND:wire :: wire _s2_nack_hit_WIRE : UInt<1>[1]
[1985] FIRRTL:199754 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:760:31 KIND:reg :: reg s2_nack_hit : UInt<1>[1], clock
[1987] FIRRTL:199756 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:762:50 KIND:node :: node _s2_nack_victim_T = and(s2_valid[0], s2_hit[0])
[1988] FIRRTL:199757 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:762:64 KIND:node :: node _s2_nack_victim_T_1 = and(_s2_nack_victim_T, mshrs.io.secondary_miss[0])
[1989] FIRRTL:199758 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_nack_victim : UInt<1>[1]
[1990] FIRRTL:199759 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_nack_victim[0], _s2_nack_victim_T_1
[1991] FIRRTL:199760 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:764:53 KIND:node :: node _s2_nack_miss_T = eq(s2_hit[0], UInt<1>(0h0))
[1992] FIRRTL:199761 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:764:50 KIND:node :: node _s2_nack_miss_T_1 = and(s2_valid[0], _s2_nack_miss_T)
[1993] FIRRTL:199762 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:764:67 KIND:node :: node _s2_nack_miss_T_2 = eq(mshrs.io.req[0].ready, UInt<1>(0h0))
[1994] FIRRTL:199763 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:764:64 KIND:node :: node _s2_nack_miss_T_3 = and(_s2_nack_miss_T_1, _s2_nack_miss_T_2)
[1995] FIRRTL:199764 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_nack_miss : UInt<1>[1]
[1996] FIRRTL:199765 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_nack_miss[0], _s2_nack_miss_T_3
[1997] FIRRTL:199766 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:766:60 KIND:reg :: reg s2_nack_data_REG : UInt<1>, clock
[1999] FIRRTL:199768 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:766:50 KIND:node :: node _s2_nack_data_T = and(s2_valid[0], s2_nack_data_REG)
[2000] FIRRTL:199769 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_nack_data : UInt<1>[1]
[2001] FIRRTL:199770 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_nack_data[0], _s2_nack_data_T
[2002] FIRRTL:199771 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:768:53 KIND:node :: node _s2_nack_wb_T = eq(s2_hit[0], UInt<1>(0h0))
[2003] FIRRTL:199772 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:768:50 KIND:node :: node _s2_nack_wb_T_1 = and(s2_valid[0], _s2_nack_wb_T)
[2004] FIRRTL:199773 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:768:64 KIND:node :: node _s2_nack_wb_T_2 = and(_s2_nack_wb_T_1, s2_wb_idx_matches[0])
[2005] FIRRTL:199774 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_nack_wb : UInt<1>[1]
[2006] FIRRTL:199775 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_nack_wb[0], _s2_nack_wb_T_2
[2007] FIRRTL:199776 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:55 KIND:node :: node _T_56 = or(s2_nack_miss[0], s2_nack_hit[0])
[2008] FIRRTL:199777 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:73 KIND:node :: node _T_57 = or(_T_56, s2_nack_victim[0])
[2009] FIRRTL:199778 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:94 KIND:node :: node _T_58 = or(_T_57, s2_nack_data[0])
[2010] FIRRTL:199779 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:113 KIND:node :: node _T_59 = or(_T_58, s2_nack_wb[0])
[2011] FIRRTL:199780 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:142 KIND:node :: node _T_60 = neq(s2_type, UInt<3>(0h0))
[2012] FIRRTL:199781 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:131 KIND:node :: node _T_61 = and(_T_59, _T_60)
[2013] FIRRTL:199782 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire _WIRE_2 : UInt<1>[1]
[2014] FIRRTL:199783 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect _WIRE_2[0], _T_61
[2015] FIRRTL:199784 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:770:21 KIND:connect :: connect s2_nack, _WIRE_2
[2016] FIRRTL:199785 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_62 = eq(s2_type, UInt<3>(0h0))
[2017] FIRRTL:199786 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_63 = eq(s2_type, UInt<3>(0h2))
[2018] FIRRTL:199787 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_64 = or(_T_62, _T_63)
[2019] FIRRTL:199788 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:38 KIND:node :: node _T_65 = and(s2_nack_data[0], _T_64)
[2020] FIRRTL:199789 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:10 KIND:node :: node _T_66 = eq(_T_65, UInt<1>(0h0))
[2021] FIRRTL:199790 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:node :: node _T_67 = asUInt(reset)
[2022] FIRRTL:199791 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:node :: node _T_68 = eq(_T_67, UInt<1>(0h0))
[2023] FIRRTL:199792 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:when :: when _T_68 :
[2024] FIRRTL:199793 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:node :: node _T_69 = eq(_T_66, UInt<1>(0h0))
[2025] FIRRTL:199794 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:when :: when _T_69 :
[2026] FIRRTL:199795 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at dcache.scala:771 assert(!(s2_nack_data.reduce(_||_) && s2_type.isOneOf(t_replay, t_wb)))\n") : printf_5
[2027] FIRRTL:199796 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:771:9 KIND:nondriving :: assert(clock, _T_66, UInt<1>(0h1), "") : assert_5
[2028] FIRRTL:199797 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:773:12 KIND:reg :: reg s2_send_resp_REG : UInt<1>, clock
[2063] FIRRTL:199832 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_send_resp : UInt<1>[1]
[2065] FIRRTL:199834 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:12 KIND:reg :: reg s2_send_store_ack_REG : UInt<1>, clock
[2096] FIRRTL:199865 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_send_store_ack : UInt<1>[1]
[2098] FIRRTL:199867 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:780:44 KIND:reg :: reg s2_send_nack_REG : UInt<1>, clock
[2101] FIRRTL:199870 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_send_nack : UInt<1>[1]
[2103] FIRRTL:199872 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:30 KIND:node :: node _T_70 = and(s2_send_resp[0], s2_send_nack[0])
[2104] FIRRTL:199873 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:12 KIND:node :: node _T_71 = eq(_T_70, UInt<1>(0h0))
[2105] FIRRTL:199874 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:node :: node _T_72 = asUInt(reset)
[2106] FIRRTL:199875 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:node :: node _T_73 = eq(_T_72, UInt<1>(0h0))
[2107] FIRRTL:199876 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:when :: when _T_73 :
[2108] FIRRTL:199877 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:node :: node _T_74 = eq(_T_71, UInt<1>(0h0))
[2109] FIRRTL:199878 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:when :: when _T_74 :
[2110] FIRRTL:199879 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at dcache.scala:782 assert(!(s2_send_resp(w) && s2_send_nack(w)))\n") : printf_6
[2111] FIRRTL:199880 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:782:11 KIND:nondriving :: assert(clock, _T_71, UInt<1>(0h1), "") : assert_6
[2188] FIRRTL:199957 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:47 KIND:node :: node _T_75 = eq(s2_type, UInt<3>(0h0))
[2189] FIRRTL:199958 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:36 KIND:node :: node _T_76 = and(mshrs.io.req[0].valid, _T_75)
[2190] FIRRTL:199959 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:12 KIND:node :: node _T_77 = eq(_T_76, UInt<1>(0h0))
[2191] FIRRTL:199960 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:node :: node _T_78 = asUInt(reset)
[2192] FIRRTL:199961 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:node :: node _T_79 = eq(_T_78, UInt<1>(0h0))
[2193] FIRRTL:199962 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:when :: when _T_79 :
[2194] FIRRTL:199963 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:node :: node _T_80 = eq(_T_77, UInt<1>(0h0))
[2195] FIRRTL:199964 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:when :: when _T_80 :
[2196] FIRRTL:199965 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: Replays should not need to go back into MSHRs\n    at dcache.scala:802 assert(!(mshrs.io.req(w).valid && s2_type === t_replay), \"Replays should not need to go back into MSHRs\")\n") : printf_7
[2197] FIRRTL:199966 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:802:11 KIND:nondriving :: assert(clock, _T_77, UInt<1>(0h1), "") : assert_7
[2198] FIRRTL:199967 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.sdq_id
[2199] FIRRTL:199968 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.way_en
[2200] FIRRTL:199969 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.old_meta.tag
[2201] FIRRTL:199970 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.old_meta.coh.state
[2202] FIRRTL:199971 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.tag_match
[2203] FIRRTL:199972 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.is_hella
[2204] FIRRTL:199973 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.data
[2205] FIRRTL:199974 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.addr
[2206] FIRRTL:199975 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.debug_tsrc
[2207] FIRRTL:199976 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.debug_fsrc
[2208] FIRRTL:199977 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.bp_xcpt_if
[2209] FIRRTL:199978 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.bp_debug_if
[2210] FIRRTL:199979 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.xcpt_ma_if
[2211] FIRRTL:199980 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.xcpt_ae_if
[2212] FIRRTL:199981 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.xcpt_pf_if
[2213] FIRRTL:199982 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_typ
[2214] FIRRTL:199983 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_rm
[2215] FIRRTL:199984 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_val
[2216] FIRRTL:199985 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fcn_op
[2217] FIRRTL:199986 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fcn_dw
[2218] FIRRTL:199987 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.frs3_en
[2219] FIRRTL:199988 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.lrs2_rtype
[2220] FIRRTL:199989 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.lrs1_rtype
[2221] FIRRTL:199990 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.dst_rtype
[2222] FIRRTL:199991 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.lrs3
[2223] FIRRTL:199992 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.lrs2
[2224] FIRRTL:199993 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.lrs1
[2225] FIRRTL:199994 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ldst
[2226] FIRRTL:199995 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ldst_is_rs1
[2227] FIRRTL:199996 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.csr_cmd
[2228] FIRRTL:199997 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.flush_on_commit
[2229] FIRRTL:199998 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_unique
[2230] FIRRTL:199999 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.uses_stq
[2231] FIRRTL:200000 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.uses_ldq
[2232] FIRRTL:200001 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.mem_signed
[2233] FIRRTL:200002 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.mem_size
[2234] FIRRTL:200003 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.mem_cmd
[2235] FIRRTL:200004 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.exc_cause
[2236] FIRRTL:200005 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.exception
[2237] FIRRTL:200006 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.stale_pdst
[2238] FIRRTL:200007 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ppred_busy
[2239] FIRRTL:200008 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs3_busy
[2240] FIRRTL:200009 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs2_busy
[2241] FIRRTL:200010 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs1_busy
[2242] FIRRTL:200011 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ppred
[2243] FIRRTL:200012 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs3
[2244] FIRRTL:200013 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs2
[2245] FIRRTL:200014 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.prs1
[2246] FIRRTL:200015 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.pdst
[2247] FIRRTL:200016 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.rxq_idx
[2248] FIRRTL:200017 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.stq_idx
[2249] FIRRTL:200018 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ldq_idx
[2250] FIRRTL:200019 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.rob_idx
[2251] FIRRTL:200020 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.vec
[2252] FIRRTL:200021 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.wflags
[2253] FIRRTL:200022 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.sqrt
[2254] FIRRTL:200023 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.div
[2255] FIRRTL:200024 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.fma
[2256] FIRRTL:200025 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.fastpipe
[2257] FIRRTL:200026 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.toint
[2258] FIRRTL:200027 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.fromint
[2259] FIRRTL:200028 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.typeTagOut
[2260] FIRRTL:200029 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.typeTagIn
[2261] FIRRTL:200030 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.swap23
[2262] FIRRTL:200031 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.swap12
[2263] FIRRTL:200032 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.ren3
[2264] FIRRTL:200033 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.ren2
[2265] FIRRTL:200034 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.ren1
[2266] FIRRTL:200035 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.wen
[2267] FIRRTL:200036 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fp_ctrl.ldst
[2268] FIRRTL:200037 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.op2_sel
[2269] FIRRTL:200038 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.op1_sel
[2270] FIRRTL:200039 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.imm_packed
[2271] FIRRTL:200040 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.pimm
[2272] FIRRTL:200041 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.imm_sel
[2273] FIRRTL:200042 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.imm_rename
[2274] FIRRTL:200043 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.taken
[2275] FIRRTL:200044 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.pc_lob
[2276] FIRRTL:200045 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.edge_inst
[2277] FIRRTL:200046 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.ftq_idx
[2278] FIRRTL:200047 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_mov
[2279] FIRRTL:200048 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_rocc
[2280] FIRRTL:200049 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_sys_pc2epc
[2281] FIRRTL:200050 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_eret
[2282] FIRRTL:200051 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_amo
[2283] FIRRTL:200052 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_sfence
[2284] FIRRTL:200053 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_fencei
[2285] FIRRTL:200054 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_fence
[2286] FIRRTL:200055 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_sfb
[2287] FIRRTL:200056 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.br_type
[2288] FIRRTL:200057 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.br_tag
[2289] FIRRTL:200058 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.br_mask
[2290] FIRRTL:200059 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.dis_col_sel
[2291] FIRRTL:200060 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_p3_bypass_hint
[2292] FIRRTL:200061 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_p2_bypass_hint
[2293] FIRRTL:200062 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_p1_bypass_hint
[2294] FIRRTL:200063 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_p2_speculative_child
[2295] FIRRTL:200064 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_p1_speculative_child
[2296] FIRRTL:200065 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_issued_partial_dgen
[2297] FIRRTL:200066 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_issued_partial_agen
[2298] FIRRTL:200067 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iw_issued
[2299] FIRRTL:200068 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[0]
[2300] FIRRTL:200069 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[1]
[2301] FIRRTL:200070 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[2]
[2302] FIRRTL:200071 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[3]
[2303] FIRRTL:200072 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[4]
[2304] FIRRTL:200073 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[5]
[2305] FIRRTL:200074 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[6]
[2306] FIRRTL:200075 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[7]
[2307] FIRRTL:200076 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[8]
[2308] FIRRTL:200077 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.fu_code[9]
[2309] FIRRTL:200078 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iq_type[0]
[2310] FIRRTL:200079 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iq_type[1]
[2311] FIRRTL:200080 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iq_type[2]
[2312] FIRRTL:200081 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.iq_type[3]
[2313] FIRRTL:200082 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.debug_pc
[2314] FIRRTL:200083 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.is_rvc
[2315] FIRRTL:200084 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.debug_inst
[2316] FIRRTL:200085 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:803:38 KIND:invalidate :: invalidate mshrs.io.req[0].bits.uop.inst
[2317] FIRRTL:200086 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.debug_tsrc, s2_req[0].uop.debug_tsrc
[2318] FIRRTL:200087 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.debug_fsrc, s2_req[0].uop.debug_fsrc
[2319] FIRRTL:200088 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.bp_xcpt_if, s2_req[0].uop.bp_xcpt_if
[2320] FIRRTL:200089 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.bp_debug_if, s2_req[0].uop.bp_debug_if
[2321] FIRRTL:200090 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.xcpt_ma_if, s2_req[0].uop.xcpt_ma_if
[2322] FIRRTL:200091 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.xcpt_ae_if, s2_req[0].uop.xcpt_ae_if
[2323] FIRRTL:200092 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.xcpt_pf_if, s2_req[0].uop.xcpt_pf_if
[2324] FIRRTL:200093 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_typ, s2_req[0].uop.fp_typ
[2325] FIRRTL:200094 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_rm, s2_req[0].uop.fp_rm
[2326] FIRRTL:200095 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_val, s2_req[0].uop.fp_val
[2327] FIRRTL:200096 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fcn_op, s2_req[0].uop.fcn_op
[2328] FIRRTL:200097 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fcn_dw, s2_req[0].uop.fcn_dw
[2329] FIRRTL:200098 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.frs3_en, s2_req[0].uop.frs3_en
[2330] FIRRTL:200099 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.lrs2_rtype, s2_req[0].uop.lrs2_rtype
[2331] FIRRTL:200100 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.lrs1_rtype, s2_req[0].uop.lrs1_rtype
[2332] FIRRTL:200101 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.dst_rtype, s2_req[0].uop.dst_rtype
[2333] FIRRTL:200102 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.lrs3, s2_req[0].uop.lrs3
[2334] FIRRTL:200103 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.lrs2, s2_req[0].uop.lrs2
[2335] FIRRTL:200104 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.lrs1, s2_req[0].uop.lrs1
[2336] FIRRTL:200105 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ldst, s2_req[0].uop.ldst
[2337] FIRRTL:200106 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ldst_is_rs1, s2_req[0].uop.ldst_is_rs1
[2338] FIRRTL:200107 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.csr_cmd, s2_req[0].uop.csr_cmd
[2339] FIRRTL:200108 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.flush_on_commit, s2_req[0].uop.flush_on_commit
[2340] FIRRTL:200109 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_unique, s2_req[0].uop.is_unique
[2341] FIRRTL:200110 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.uses_stq, s2_req[0].uop.uses_stq
[2342] FIRRTL:200111 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.uses_ldq, s2_req[0].uop.uses_ldq
[2343] FIRRTL:200112 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.mem_signed, s2_req[0].uop.mem_signed
[2344] FIRRTL:200113 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.mem_size, s2_req[0].uop.mem_size
[2345] FIRRTL:200114 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.mem_cmd, s2_req[0].uop.mem_cmd
[2346] FIRRTL:200115 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.exc_cause, s2_req[0].uop.exc_cause
[2347] FIRRTL:200116 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.exception, s2_req[0].uop.exception
[2348] FIRRTL:200117 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.stale_pdst, s2_req[0].uop.stale_pdst
[2349] FIRRTL:200118 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ppred_busy, s2_req[0].uop.ppred_busy
[2350] FIRRTL:200119 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs3_busy, s2_req[0].uop.prs3_busy
[2351] FIRRTL:200120 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs2_busy, s2_req[0].uop.prs2_busy
[2352] FIRRTL:200121 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs1_busy, s2_req[0].uop.prs1_busy
[2353] FIRRTL:200122 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ppred, s2_req[0].uop.ppred
[2354] FIRRTL:200123 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs3, s2_req[0].uop.prs3
[2355] FIRRTL:200124 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs2, s2_req[0].uop.prs2
[2356] FIRRTL:200125 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.prs1, s2_req[0].uop.prs1
[2357] FIRRTL:200126 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.pdst, s2_req[0].uop.pdst
[2358] FIRRTL:200127 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.rxq_idx, s2_req[0].uop.rxq_idx
[2359] FIRRTL:200128 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.stq_idx, s2_req[0].uop.stq_idx
[2360] FIRRTL:200129 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ldq_idx, s2_req[0].uop.ldq_idx
[2361] FIRRTL:200130 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.rob_idx, s2_req[0].uop.rob_idx
[2362] FIRRTL:200131 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.vec, s2_req[0].uop.fp_ctrl.vec
[2363] FIRRTL:200132 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.wflags, s2_req[0].uop.fp_ctrl.wflags
[2364] FIRRTL:200133 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.sqrt, s2_req[0].uop.fp_ctrl.sqrt
[2365] FIRRTL:200134 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.div, s2_req[0].uop.fp_ctrl.div
[2366] FIRRTL:200135 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.fma, s2_req[0].uop.fp_ctrl.fma
[2367] FIRRTL:200136 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.fastpipe, s2_req[0].uop.fp_ctrl.fastpipe
[2368] FIRRTL:200137 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.toint, s2_req[0].uop.fp_ctrl.toint
[2369] FIRRTL:200138 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.fromint, s2_req[0].uop.fp_ctrl.fromint
[2370] FIRRTL:200139 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.typeTagOut, s2_req[0].uop.fp_ctrl.typeTagOut
[2371] FIRRTL:200140 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.typeTagIn, s2_req[0].uop.fp_ctrl.typeTagIn
[2372] FIRRTL:200141 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.swap23, s2_req[0].uop.fp_ctrl.swap23
[2373] FIRRTL:200142 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.swap12, s2_req[0].uop.fp_ctrl.swap12
[2374] FIRRTL:200143 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.ren3, s2_req[0].uop.fp_ctrl.ren3
[2375] FIRRTL:200144 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.ren2, s2_req[0].uop.fp_ctrl.ren2
[2376] FIRRTL:200145 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.ren1, s2_req[0].uop.fp_ctrl.ren1
[2377] FIRRTL:200146 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.wen, s2_req[0].uop.fp_ctrl.wen
[2378] FIRRTL:200147 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fp_ctrl.ldst, s2_req[0].uop.fp_ctrl.ldst
[2379] FIRRTL:200148 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.op2_sel, s2_req[0].uop.op2_sel
[2380] FIRRTL:200149 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.op1_sel, s2_req[0].uop.op1_sel
[2381] FIRRTL:200150 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.imm_packed, s2_req[0].uop.imm_packed
[2382] FIRRTL:200151 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.pimm, s2_req[0].uop.pimm
[2383] FIRRTL:200152 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.imm_sel, s2_req[0].uop.imm_sel
[2384] FIRRTL:200153 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.imm_rename, s2_req[0].uop.imm_rename
[2385] FIRRTL:200154 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.taken, s2_req[0].uop.taken
[2386] FIRRTL:200155 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.pc_lob, s2_req[0].uop.pc_lob
[2387] FIRRTL:200156 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.edge_inst, s2_req[0].uop.edge_inst
[2388] FIRRTL:200157 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.ftq_idx, s2_req[0].uop.ftq_idx
[2389] FIRRTL:200158 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_mov, s2_req[0].uop.is_mov
[2390] FIRRTL:200159 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_rocc, s2_req[0].uop.is_rocc
[2391] FIRRTL:200160 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_sys_pc2epc, s2_req[0].uop.is_sys_pc2epc
[2392] FIRRTL:200161 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_eret, s2_req[0].uop.is_eret
[2393] FIRRTL:200162 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_amo, s2_req[0].uop.is_amo
[2394] FIRRTL:200163 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_sfence, s2_req[0].uop.is_sfence
[2395] FIRRTL:200164 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_fencei, s2_req[0].uop.is_fencei
[2396] FIRRTL:200165 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_fence, s2_req[0].uop.is_fence
[2397] FIRRTL:200166 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_sfb, s2_req[0].uop.is_sfb
[2398] FIRRTL:200167 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.br_type, s2_req[0].uop.br_type
[2399] FIRRTL:200168 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.br_tag, s2_req[0].uop.br_tag
[2400] FIRRTL:200169 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.br_mask, s2_req[0].uop.br_mask
[2401] FIRRTL:200170 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.dis_col_sel, s2_req[0].uop.dis_col_sel
[2402] FIRRTL:200171 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_p3_bypass_hint, s2_req[0].uop.iw_p3_bypass_hint
[2403] FIRRTL:200172 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_p2_bypass_hint, s2_req[0].uop.iw_p2_bypass_hint
[2404] FIRRTL:200173 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_p1_bypass_hint, s2_req[0].uop.iw_p1_bypass_hint
[2405] FIRRTL:200174 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_p2_speculative_child, s2_req[0].uop.iw_p2_speculative_child
[2406] FIRRTL:200175 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_p1_speculative_child, s2_req[0].uop.iw_p1_speculative_child
[2407] FIRRTL:200176 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_issued_partial_dgen, s2_req[0].uop.iw_issued_partial_dgen
[2408] FIRRTL:200177 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_issued_partial_agen, s2_req[0].uop.iw_issued_partial_agen
[2409] FIRRTL:200178 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iw_issued, s2_req[0].uop.iw_issued
[2410] FIRRTL:200179 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[0], s2_req[0].uop.fu_code[0]
[2411] FIRRTL:200180 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[1], s2_req[0].uop.fu_code[1]
[2412] FIRRTL:200181 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[2], s2_req[0].uop.fu_code[2]
[2413] FIRRTL:200182 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[3], s2_req[0].uop.fu_code[3]
[2414] FIRRTL:200183 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[4], s2_req[0].uop.fu_code[4]
[2415] FIRRTL:200184 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[5], s2_req[0].uop.fu_code[5]
[2416] FIRRTL:200185 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[6], s2_req[0].uop.fu_code[6]
[2417] FIRRTL:200186 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[7], s2_req[0].uop.fu_code[7]
[2418] FIRRTL:200187 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[8], s2_req[0].uop.fu_code[8]
[2419] FIRRTL:200188 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.fu_code[9], s2_req[0].uop.fu_code[9]
[2420] FIRRTL:200189 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iq_type[0], s2_req[0].uop.iq_type[0]
[2421] FIRRTL:200190 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iq_type[1], s2_req[0].uop.iq_type[1]
[2422] FIRRTL:200191 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iq_type[2], s2_req[0].uop.iq_type[2]
[2423] FIRRTL:200192 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.iq_type[3], s2_req[0].uop.iq_type[3]
[2424] FIRRTL:200193 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.debug_pc, s2_req[0].uop.debug_pc
[2425] FIRRTL:200194 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.is_rvc, s2_req[0].uop.is_rvc
[2426] FIRRTL:200195 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.debug_inst, s2_req[0].uop.debug_inst
[2427] FIRRTL:200196 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:804:38 KIND:connect :: connect mshrs.io.req[0].bits.uop.inst, s2_req[0].uop.inst
[2428] FIRRTL:200197 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:805:38 KIND:connect :: connect mshrs.io.req[0].bits.addr, s2_req[0].addr
[2429] FIRRTL:200198 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:806:38 KIND:connect :: connect mshrs.io.req[0].bits.tag_match, s2_tag_match_0
[2430] FIRRTL:200199 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:305:20 KIND:wire :: wire mshrs_io_req_0_bits_old_meta_meta : { coh : { state : UInt<2>}, tag : UInt<20>}
[2431] FIRRTL:200200 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:306:14 KIND:connect :: connect mshrs_io_req_0_bits_old_meta_meta.tag, s2_repl_meta[0].tag
[2432] FIRRTL:200201 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:307:14 KIND:connect :: connect mshrs_io_req_0_bits_old_meta_meta.coh, s2_hit_state[0]
[2433] FIRRTL:200202 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:807:44 KIND:node :: node _mshrs_io_req_0_bits_old_meta_T = mux(s2_tag_match_0, mshrs_io_req_0_bits_old_meta_meta, s2_repl_meta[0])
[2434] FIRRTL:200203 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:807:38 KIND:connect :: connect mshrs.io.req[0].bits.old_meta.tag, _mshrs_io_req_0_bits_old_meta_T.tag
[2435] FIRRTL:200204 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:807:38 KIND:connect :: connect mshrs.io.req[0].bits.old_meta.coh.state, _mshrs_io_req_0_bits_old_meta_T.coh.state
[2436] FIRRTL:200205 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:808:44 KIND:node :: node _mshrs_io_req_0_bits_way_en_T = mux(s2_tag_match_0, s2_tag_match_way[0], s2_replaced_way_en)
[2437] FIRRTL:200206 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:808:38 KIND:connect :: connect mshrs.io.req[0].bits.way_en, _mshrs_io_req_0_bits_way_en_T
[2438] FIRRTL:200207 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:810:38 KIND:connect :: connect mshrs.io.req[0].bits.data, s2_req[0].data
[2439] FIRRTL:200208 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:811:38 KIND:connect :: connect mshrs.io.req[0].bits.is_hella, s2_req[0].is_hella
[2440] FIRRTL:200209 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:812:49 KIND:node :: node _mshrs_io_req_is_probe_0_T = eq(s2_type, UInt<3>(0h1))
[2441] FIRRTL:200210 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:812:61 KIND:node :: node _mshrs_io_req_is_probe_0_T_1 = and(_mshrs_io_req_is_probe_0_T, s2_valid[0])
[2442] FIRRTL:200211 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:812:38 KIND:connect :: connect mshrs.io.req_is_probe[0], _mshrs_io_req_is_probe_0_T_1
[2443] FIRRTL:200212 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:815:36 KIND:node :: node _mshrs_io_meta_resp_valid_T = eq(s2_nack_hit[0], UInt<1>(0h0))
[2444] FIRRTL:200213 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:815:52 KIND:node :: node _mshrs_io_meta_resp_valid_T_1 = or(_mshrs_io_meta_resp_valid_T, prober.io.mshr_wb_rdy)
[2445] FIRRTL:200214 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:815:33 KIND:connect :: connect mshrs.io.meta_resp.valid, _mshrs_io_meta_resp_valid_T_1
[2446] FIRRTL:200215 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:816:70 KIND:reg :: reg mshrs_io_meta_resp_bits_REG : { coh : { state : UInt<2>}, tag : UInt<20>}[4], clock
[2447] FIRRTL:200216 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:816:70 KIND:connect :: connect mshrs_io_meta_resp_bits_REG, meta_0.io.resp
[2448] FIRRTL:200217 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _mshrs_io_meta_resp_bits_T = bits(s2_tag_match_way[0], 0, 0)
[2449] FIRRTL:200218 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _mshrs_io_meta_resp_bits_T_1 = bits(s2_tag_match_way[0], 1, 1)
[2450] FIRRTL:200219 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _mshrs_io_meta_resp_bits_T_2 = bits(s2_tag_match_way[0], 2, 2)
[2451] FIRRTL:200220 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _mshrs_io_meta_resp_bits_T_3 = bits(s2_tag_match_way[0], 3, 3)
[2452] FIRRTL:200221 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _mshrs_io_meta_resp_bits_WIRE : { coh : { state : UInt<2>}, tag : UInt<20>}
[2453] FIRRTL:200222 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_4 = mux(_mshrs_io_meta_resp_bits_T, mshrs_io_meta_resp_bits_REG[0].tag, UInt<1>(0h0))
[2454] FIRRTL:200223 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_5 = mux(_mshrs_io_meta_resp_bits_T_1, mshrs_io_meta_resp_bits_REG[1].tag, UInt<1>(0h0))
[2455] FIRRTL:200224 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_6 = mux(_mshrs_io_meta_resp_bits_T_2, mshrs_io_meta_resp_bits_REG[2].tag, UInt<1>(0h0))
[2456] FIRRTL:200225 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_7 = mux(_mshrs_io_meta_resp_bits_T_3, mshrs_io_meta_resp_bits_REG[3].tag, UInt<1>(0h0))
[2457] FIRRTL:200226 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_8 = or(_mshrs_io_meta_resp_bits_T_4, _mshrs_io_meta_resp_bits_T_5)
[2458] FIRRTL:200227 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_9 = or(_mshrs_io_meta_resp_bits_T_8, _mshrs_io_meta_resp_bits_T_6)
[2459] FIRRTL:200228 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_10 = or(_mshrs_io_meta_resp_bits_T_9, _mshrs_io_meta_resp_bits_T_7)
[2460] FIRRTL:200229 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _mshrs_io_meta_resp_bits_WIRE_1 : UInt<20>
[2461] FIRRTL:200230 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _mshrs_io_meta_resp_bits_WIRE_1, _mshrs_io_meta_resp_bits_T_10
[2462] FIRRTL:200231 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _mshrs_io_meta_resp_bits_WIRE.tag, _mshrs_io_meta_resp_bits_WIRE_1
[2463] FIRRTL:200232 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _mshrs_io_meta_resp_bits_WIRE_2 : { state : UInt<2>}
[2464] FIRRTL:200233 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_11 = mux(_mshrs_io_meta_resp_bits_T, mshrs_io_meta_resp_bits_REG[0].coh.state, UInt<1>(0h0))
[2465] FIRRTL:200234 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_12 = mux(_mshrs_io_meta_resp_bits_T_1, mshrs_io_meta_resp_bits_REG[1].coh.state, UInt<1>(0h0))
[2466] FIRRTL:200235 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_13 = mux(_mshrs_io_meta_resp_bits_T_2, mshrs_io_meta_resp_bits_REG[2].coh.state, UInt<1>(0h0))
[2467] FIRRTL:200236 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_14 = mux(_mshrs_io_meta_resp_bits_T_3, mshrs_io_meta_resp_bits_REG[3].coh.state, UInt<1>(0h0))
[2468] FIRRTL:200237 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_15 = or(_mshrs_io_meta_resp_bits_T_11, _mshrs_io_meta_resp_bits_T_12)
[2469] FIRRTL:200238 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_16 = or(_mshrs_io_meta_resp_bits_T_15, _mshrs_io_meta_resp_bits_T_13)
[2470] FIRRTL:200239 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _mshrs_io_meta_resp_bits_T_17 = or(_mshrs_io_meta_resp_bits_T_16, _mshrs_io_meta_resp_bits_T_14)
[2471] FIRRTL:200240 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _mshrs_io_meta_resp_bits_WIRE_3 : UInt<2>
[2472] FIRRTL:200241 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _mshrs_io_meta_resp_bits_WIRE_3, _mshrs_io_meta_resp_bits_T_17
[2473] FIRRTL:200242 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _mshrs_io_meta_resp_bits_WIRE_2.state, _mshrs_io_meta_resp_bits_WIRE_3
[2474] FIRRTL:200243 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _mshrs_io_meta_resp_bits_WIRE.coh, _mshrs_io_meta_resp_bits_WIRE_2
[2475] FIRRTL:200244 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:816:33 KIND:connect :: connect mshrs.io.meta_resp.bits.tag, _mshrs_io_meta_resp_bits_WIRE.tag
[2476] FIRRTL:200245 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:816:33 KIND:connect :: connect mshrs.io.meta_resp.bits.coh.state, _mshrs_io_meta_resp_bits_WIRE.coh.state
[2477] FIRRTL:200246 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_81 = and(mshrs.io.req[0].ready, mshrs.io.req[0].valid)
[2478] FIRRTL:200247 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:817:48 KIND:when :: when _T_81 :
[2479] FIRRTL:200248 SRC:generators/rocket-chip/src/main/scala/util/Replacement.scala:45:22 KIND:connect :: connect replace, UInt<1>(0h1)
[2480] FIRRTL:200249 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:818:12 KIND:connect :: connect nodeOut.a.bits, mshrs.io.mem_acquire.bits
[2481] FIRRTL:200250 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:818:12 KIND:connect :: connect nodeOut.a.valid, mshrs.io.mem_acquire.valid
[2482] FIRRTL:200251 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:818:12 KIND:connect :: connect mshrs.io.mem_acquire.ready, nodeOut.a.ready
[2483] FIRRTL:200252 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:821:46 KIND:node :: node _prober_io_req_valid_T = eq(lrsc_valid, UInt<1>(0h0))
[2484] FIRRTL:200253 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:821:43 KIND:node :: node _prober_io_req_valid_T_1 = and(nodeOut.b.valid, _prober_io_req_valid_T)
[2485] FIRRTL:200254 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:821:25 KIND:connect :: connect prober.io.req.valid, _prober_io_req_valid_T_1
[2489] FIRRTL:200258 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.corrupt, nodeOut.b.bits.corrupt
[2490] FIRRTL:200259 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.data, nodeOut.b.bits.data
[2491] FIRRTL:200260 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.mask, nodeOut.b.bits.mask
[2492] FIRRTL:200261 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.address, nodeOut.b.bits.address
[2493] FIRRTL:200262 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.source, nodeOut.b.bits.source
[2494] FIRRTL:200263 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.size, nodeOut.b.bits.size
[2495] FIRRTL:200264 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.param, nodeOut.b.bits.param
[2496] FIRRTL:200265 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:823:25 KIND:connect :: connect prober.io.req.bits.opcode, nodeOut.b.bits.opcode
[2497] FIRRTL:200266 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:824:25 KIND:connect :: connect prober.io.way_en, s2_tag_match_way[0]
[2498] FIRRTL:200267 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:825:25 KIND:connect :: connect prober.io.block_state.state, s2_hit_state[0].state
[2499] FIRRTL:200268 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:826:25 KIND:connect :: connect metaWriteArb.io.in[1], prober.io.meta_write
[2500] FIRRTL:200269 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:827:25 KIND:connect :: connect prober.io.mshr_rdy, mshrs.io.probe_rdy
[2501] FIRRTL:200270 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:828:59 KIND:node :: node _prober_io_wb_rdy_T = neq(prober.io.meta_write.bits.idx, wb.io.idx.bits)
[2502] FIRRTL:200271 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:828:82 KIND:node :: node _prober_io_wb_rdy_T_1 = eq(wb.io.idx.valid, UInt<1>(0h0))
[2503] FIRRTL:200272 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:828:79 KIND:node :: node _prober_io_wb_rdy_T_2 = or(_prober_io_wb_rdy_T, _prober_io_wb_rdy_T_1)
[2504] FIRRTL:200273 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:828:25 KIND:connect :: connect prober.io.wb_rdy, _prober_io_wb_rdy_T_2
[2505] FIRRTL:200274 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:829:25 KIND:connect :: connect mshrs.io.prober_state.bits, prober.io.state.bits
[2506] FIRRTL:200275 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:829:25 KIND:connect :: connect mshrs.io.prober_state.valid, prober.io.state.valid
[2510] FIRRTL:200279 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:835:30 KIND:connect :: connect mshrs.io.mem_grant.valid, UInt<1>(0h0)
[2511] FIRRTL:200280 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.corrupt
[2512] FIRRTL:200281 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.data
[2513] FIRRTL:200282 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.denied
[2514] FIRRTL:200283 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.sink
[2515] FIRRTL:200284 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.source
[2516] FIRRTL:200285 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.size
[2517] FIRRTL:200286 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.param
[2518] FIRRTL:200287 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:836:30 KIND:invalidate :: invalidate mshrs.io.mem_grant.bits.opcode
[2521] FIRRTL:200290 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:842:25 KIND:connect :: connect dataWriteArb.io.in[1], mshrs.io.refill
[2522] FIRRTL:200291 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:843:25 KIND:connect :: connect metaWriteArb.io.in[0], mshrs.io.meta_write
[2523] FIRRTL:200292 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:845:12 KIND:connect :: connect nodeOut.e.bits, mshrs.io.mem_finish.bits
[2524] FIRRTL:200293 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:845:12 KIND:connect :: connect nodeOut.e.valid, mshrs.io.mem_finish.valid
[2525] FIRRTL:200294 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:845:12 KIND:connect :: connect mshrs.io.mem_finish.ready, nodeOut.e.ready
[2526] FIRRTL:200295 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:848:21 KIND:structural :: inst wbArb of Arbiter2_WritebackReq_1
[2527] FIRRTL:200296 SRC:<no-source-locator> KIND:connect :: connect wbArb.clock, clock
[2528] FIRRTL:200297 SRC:<no-source-locator> KIND:connect :: connect wbArb.reset, reset
[2529] FIRRTL:200298 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:850:24 KIND:connect :: connect wbArb.io.in[0], prober.io.wb_req
[2530] FIRRTL:200299 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:851:24 KIND:connect :: connect wbArb.io.in[1], mshrs.io.wb_req
[2531] FIRRTL:200300 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:852:24 KIND:connect :: connect wb.io.req, wbArb.io.out
[2532] FIRRTL:200301 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:853:25 KIND:connect :: connect wb.io.data_resp, s2_data_muxed[0]
[2533] FIRRTL:200302 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:854:25 KIND:connect :: connect mshrs.io.wb_resp, wb.io.resp
[2534] FIRRTL:200303 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _wb_io_mem_grant_T = and(nodeOut.d.ready, nodeOut.d.valid)
[2535] FIRRTL:200304 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:855:66 KIND:node :: node _wb_io_mem_grant_T_1 = eq(nodeOut.d.bits.source, UInt<2>(0h2))
[2536] FIRRTL:200305 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:855:42 KIND:node :: node _wb_io_mem_grant_T_2 = and(_wb_io_mem_grant_T, _wb_io_mem_grant_T_1)
[2537] FIRRTL:200306 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:855:25 KIND:connect :: connect wb.io.mem_grant, _wb_io_mem_grant_T_2
[2538] FIRRTL:200307 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:857:31 KIND:structural :: inst lsu_release_arb of Arbiter2_TLBundleC_a32d64s2k3z4c
[2539] FIRRTL:200308 SRC:<no-source-locator> KIND:connect :: connect lsu_release_arb.clock, clock
[2540] FIRRTL:200309 SRC:<no-source-locator> KIND:connect :: connect lsu_release_arb.reset, reset
[2541] FIRRTL:200310 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:858:18 KIND:connect :: connect io.lsu.release.bits, lsu_release_arb.io.out.bits
[2542] FIRRTL:200311 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:858:18 KIND:connect :: connect io.lsu.release.valid, lsu_release_arb.io.out.valid
[2543] FIRRTL:200312 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:858:18 KIND:connect :: connect lsu_release_arb.io.out.ready, io.lsu.release.ready
[2544] FIRRTL:200313 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:859:28 KIND:connect :: connect lsu_release_arb.io.in[0], wb.io.lsu_release
[2545] FIRRTL:200314 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:860:28 KIND:connect :: connect lsu_release_arb.io.in[1], prober.io.lsu_release
[2558] FIRRTL:200327 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:60:30 KIND:regreset :: regreset beatsLeft : UInt, clock, reset, UInt<1>(0h0)
[2571] FIRRTL:200340 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:wire :: wire readys : UInt<1>[2]
[2576] FIRRTL:200345 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:wire :: wire winner : UInt<1>[2]
[2579] FIRRTL:200348 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node prefixOR_1 = or(UInt<1>(0h0), winner[0])
[2580] FIRRTL:200349 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node _prefixOR_T = or(prefixOR_1, winner[1])
[2581] FIRRTL:200350 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_85 = eq(UInt<1>(0h0), UInt<1>(0h0))
[2582] FIRRTL:200351 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_86 = eq(winner[0], UInt<1>(0h0))
[2583] FIRRTL:200352 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_87 = or(_T_85, _T_86)
[2584] FIRRTL:200353 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_88 = eq(prefixOR_1, UInt<1>(0h0))
[2585] FIRRTL:200354 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_89 = eq(winner[1], UInt<1>(0h0))
[2586] FIRRTL:200355 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_90 = or(_T_88, _T_89)
[2587] FIRRTL:200356 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:77 KIND:node :: node _T_91 = and(_T_87, _T_90)
[2588] FIRRTL:200357 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_92 = asUInt(reset)
[2589] FIRRTL:200358 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_93 = eq(_T_92, UInt<1>(0h0))
[2590] FIRRTL:200359 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_93 :
[2591] FIRRTL:200360 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_94 = eq(_T_91, UInt<1>(0h0))
[2592] FIRRTL:200361 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_94 :
[2593] FIRRTL:200362 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:77 assert((prefixOR zip winner) map { case (p,w) => !p || !w } reduce {_ && _})\n") : printf_8
[2594] FIRRTL:200363 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: assert(clock, _T_91, UInt<1>(0h1), "") : assert_8
[2595] FIRRTL:200364 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:31 KIND:node :: node _T_95 = or(wb.io.release.valid, prober.io.rep.valid)
[2596] FIRRTL:200365 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:15 KIND:node :: node _T_96 = eq(_T_95, UInt<1>(0h0))
[2597] FIRRTL:200366 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:54 KIND:node :: node _T_97 = or(winner[0], winner[1])
[2598] FIRRTL:200367 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:36 KIND:node :: node _T_98 = or(_T_96, _T_97)
[2599] FIRRTL:200368 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_99 = asUInt(reset)
[2600] FIRRTL:200369 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_100 = eq(_T_99, UInt<1>(0h0))
[2601] FIRRTL:200370 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_100 :
[2602] FIRRTL:200371 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_101 = eq(_T_98, UInt<1>(0h0))
[2603] FIRRTL:200372 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_101 :
[2604] FIRRTL:200373 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:79 assert (!valids.reduce(_||_) || winner.reduce(_||_))\n") : printf_9
[2605] FIRRTL:200374 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: assert(clock, _T_98, UInt<1>(0h1), "") : assert_9
[2614] FIRRTL:200383 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:wire :: wire _state_WIRE : UInt<1>[2]
[2615] FIRRTL:200384 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE[0], UInt<1>(0h0)
[2616] FIRRTL:200385 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE[1], UInt<1>(0h0)
[2617] FIRRTL:200386 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:26 KIND:regreset :: regreset state : UInt<1>[2], clock, reset, _state_WIRE
[2620] FIRRTL:200389 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:92:24 KIND:node :: node allowed = mux(idle, readys, state)
[2621] FIRRTL:200390 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _wb_io_release_ready_T = and(nodeOut.c.ready, allowed[0])
[2622] FIRRTL:200391 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect wb.io.release.ready, _wb_io_release_ready_T
[2623] FIRRTL:200392 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _prober_io_rep_ready_T = and(nodeOut.c.ready, allowed[1])
[2624] FIRRTL:200393 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect prober.io.rep.ready, _prober_io_rep_ready_T
[2629] FIRRTL:200398 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_valid_WIRE : UInt<1>
[2633] FIRRTL:200402 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}
[2637] FIRRTL:200406 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_1 : UInt<1>
[2643] FIRRTL:200412 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_2 : UInt<64>
[2646] FIRRTL:200415 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_3 : { }
[2647] FIRRTL:200416 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.echo, _nodeOut_c_bits_WIRE_3
[2648] FIRRTL:200417 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_4 : { }
[2649] FIRRTL:200418 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.user, _nodeOut_c_bits_WIRE_4
[2653] FIRRTL:200422 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_5 : UInt<32>
[2659] FIRRTL:200428 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_6 : UInt<2>
[2665] FIRRTL:200434 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_7 : UInt<4>
[2671] FIRRTL:200440 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_8 : UInt<3>
[2677] FIRRTL:200446 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _nodeOut_c_bits_WIRE_9 : UInt<3>
[2687] FIRRTL:200456 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _io_lsu_perf_release_T = and(nodeOut.c.ready, nodeOut.c.valid)
[2688] FIRRTL:200457 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _io_lsu_perf_release_beats1_decode_T = dshl(UInt<12>(0hfff), nodeOut.c.bits.size)
[2689] FIRRTL:200458 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _io_lsu_perf_release_beats1_decode_T_1 = bits(_io_lsu_perf_release_beats1_decode_T, 11, 0)
[2690] FIRRTL:200459 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _io_lsu_perf_release_beats1_decode_T_2 = not(_io_lsu_perf_release_beats1_decode_T_1)
[2691] FIRRTL:200460 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node io_lsu_perf_release_beats1_decode = shr(_io_lsu_perf_release_beats1_decode_T_2, 3)
[2692] FIRRTL:200461 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:102:36 KIND:node :: node io_lsu_perf_release_beats1_opdata = bits(nodeOut.c.bits.opcode, 0, 0)
[2693] FIRRTL:200462 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node io_lsu_perf_release_beats1 = mux(io_lsu_perf_release_beats1_opdata, io_lsu_perf_release_beats1_decode, UInt<1>(0h0))
[2694] FIRRTL:200463 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:229:27 KIND:regreset :: regreset io_lsu_perf_release_counter : UInt<9>, clock, reset, UInt<9>(0h0)
[2695] FIRRTL:200464 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node _io_lsu_perf_release_counter1_T = sub(io_lsu_perf_release_counter, UInt<1>(0h1))
[2696] FIRRTL:200465 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node io_lsu_perf_release_counter1 = tail(_io_lsu_perf_release_counter1_T, 1)
[2697] FIRRTL:200466 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:231:25 KIND:node :: node io_lsu_perf_release_first = eq(io_lsu_perf_release_counter, UInt<1>(0h0))
[2698] FIRRTL:200467 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:25 KIND:node :: node _io_lsu_perf_release_last_T = eq(io_lsu_perf_release_counter, UInt<1>(0h1))
[2699] FIRRTL:200468 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:43 KIND:node :: node _io_lsu_perf_release_last_T_1 = eq(io_lsu_perf_release_beats1, UInt<1>(0h0))
[2700] FIRRTL:200469 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:33 KIND:node :: node io_lsu_perf_release_last = or(_io_lsu_perf_release_last_T, _io_lsu_perf_release_last_T_1)
[2701] FIRRTL:200470 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:233:22 KIND:node :: node io_lsu_perf_release_done = and(io_lsu_perf_release_last, _io_lsu_perf_release_T)
[2702] FIRRTL:200471 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:27 KIND:node :: node _io_lsu_perf_release_count_T = not(io_lsu_perf_release_counter1)
[2703] FIRRTL:200472 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:25 KIND:node :: node io_lsu_perf_release_count = and(io_lsu_perf_release_beats1, _io_lsu_perf_release_count_T)
[2704] FIRRTL:200473 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:235:17 KIND:when :: when _io_lsu_perf_release_T :
[2705] FIRRTL:200474 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:21 KIND:node :: node _io_lsu_perf_release_counter_T = mux(io_lsu_perf_release_first, io_lsu_perf_release_beats1, io_lsu_perf_release_counter1)
[2706] FIRRTL:200475 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:15 KIND:connect :: connect io_lsu_perf_release_counter, _io_lsu_perf_release_counter_T
[2707] FIRRTL:200476 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:864:23 KIND:connect :: connect io.lsu.perf.release, io_lsu_perf_release_done
[2708] FIRRTL:200477 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _io_lsu_perf_acquire_T = and(nodeOut.a.ready, nodeOut.a.valid)
[2709] FIRRTL:200478 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _io_lsu_perf_acquire_beats1_decode_T = dshl(UInt<12>(0hfff), nodeOut.a.bits.size)
[2710] FIRRTL:200479 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _io_lsu_perf_acquire_beats1_decode_T_1 = bits(_io_lsu_perf_acquire_beats1_decode_T, 11, 0)
[2711] FIRRTL:200480 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _io_lsu_perf_acquire_beats1_decode_T_2 = not(_io_lsu_perf_acquire_beats1_decode_T_1)
[2712] FIRRTL:200481 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node io_lsu_perf_acquire_beats1_decode = shr(_io_lsu_perf_acquire_beats1_decode_T_2, 3)
[2713] FIRRTL:200482 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:37 KIND:node :: node _io_lsu_perf_acquire_beats1_opdata_T = bits(nodeOut.a.bits.opcode, 2, 2)
[2714] FIRRTL:200483 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:28 KIND:node :: node io_lsu_perf_acquire_beats1_opdata = eq(_io_lsu_perf_acquire_beats1_opdata_T, UInt<1>(0h0))
[2715] FIRRTL:200484 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node io_lsu_perf_acquire_beats1 = mux(io_lsu_perf_acquire_beats1_opdata, io_lsu_perf_acquire_beats1_decode, UInt<1>(0h0))
[2716] FIRRTL:200485 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:229:27 KIND:regreset :: regreset io_lsu_perf_acquire_counter : UInt<9>, clock, reset, UInt<9>(0h0)
[2717] FIRRTL:200486 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node _io_lsu_perf_acquire_counter1_T = sub(io_lsu_perf_acquire_counter, UInt<1>(0h1))
[2718] FIRRTL:200487 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node io_lsu_perf_acquire_counter1 = tail(_io_lsu_perf_acquire_counter1_T, 1)
[2719] FIRRTL:200488 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:231:25 KIND:node :: node io_lsu_perf_acquire_first = eq(io_lsu_perf_acquire_counter, UInt<1>(0h0))
[2720] FIRRTL:200489 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:25 KIND:node :: node _io_lsu_perf_acquire_last_T = eq(io_lsu_perf_acquire_counter, UInt<1>(0h1))
[2721] FIRRTL:200490 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:43 KIND:node :: node _io_lsu_perf_acquire_last_T_1 = eq(io_lsu_perf_acquire_beats1, UInt<1>(0h0))
[2722] FIRRTL:200491 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:33 KIND:node :: node io_lsu_perf_acquire_last = or(_io_lsu_perf_acquire_last_T, _io_lsu_perf_acquire_last_T_1)
[2723] FIRRTL:200492 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:233:22 KIND:node :: node io_lsu_perf_acquire_done = and(io_lsu_perf_acquire_last, _io_lsu_perf_acquire_T)
[2724] FIRRTL:200493 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:27 KIND:node :: node _io_lsu_perf_acquire_count_T = not(io_lsu_perf_acquire_counter1)
[2725] FIRRTL:200494 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:25 KIND:node :: node io_lsu_perf_acquire_count = and(io_lsu_perf_acquire_beats1, _io_lsu_perf_acquire_count_T)
[2726] FIRRTL:200495 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:235:17 KIND:when :: when _io_lsu_perf_acquire_T :
[2727] FIRRTL:200496 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:21 KIND:node :: node _io_lsu_perf_acquire_counter_T = mux(io_lsu_perf_acquire_first, io_lsu_perf_acquire_beats1, io_lsu_perf_acquire_counter1)
[2728] FIRRTL:200497 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:15 KIND:connect :: connect io_lsu_perf_acquire_counter, _io_lsu_perf_acquire_counter_T
[2729] FIRRTL:200498 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:865:23 KIND:connect :: connect io.lsu.perf.acquire, io_lsu_perf_acquire_done
[2732] FIRRTL:200501 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s2_data_word_prebypass : UInt<64>[1]
[2734] FIRRTL:200503 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:869:26 KIND:wire :: wire s2_data_word : UInt[1]
[2736] FIRRTL:200505 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11:18 KIND:wire :: wire size : UInt<2>
[2738] FIRRTL:200507 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:13:27 KIND:node :: node size_dat_padded = pad(s2_data_word[0], 64)
[2790] FIRRTL:200559 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:46 KIND:node :: node _T_103 = neq(s2_type, UInt<3>(0h4))
[2791] FIRRTL:200560 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:35 KIND:node :: node _T_104 = and(io.lsu.nack[0].valid, _T_103)
[2792] FIRRTL:200561 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:12 KIND:node :: node _T_105 = eq(_T_104, UInt<1>(0h0))
[2793] FIRRTL:200562 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:node :: node _T_106 = asUInt(reset)
[2794] FIRRTL:200563 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:node :: node _T_107 = eq(_T_106, UInt<1>(0h0))
[2795] FIRRTL:200564 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:when :: when _T_107 :
[2796] FIRRTL:200565 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:node :: node _T_108 = eq(_T_105, UInt<1>(0h0))
[2797] FIRRTL:200566 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:when :: when _T_108 :
[2798] FIRRTL:200567 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at dcache.scala:886 assert(!(io.lsu.nack(w).valid && s2_type =/= t_lsu))\n") : printf_10
[2799] FIRRTL:200568 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:886:11 KIND:nondriving :: assert(clock, _T_105, UInt<1>(0h1), "") : assert_10
[2804] FIRRTL:200573 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:892:18 KIND:connect :: connect io.lsu.ll_resp.bits, mshrs.io.resp.bits
[2805] FIRRTL:200574 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:892:18 KIND:connect :: connect io.lsu.ll_resp.valid, mshrs.io.resp.valid
[2806] FIRRTL:200575 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:892:18 KIND:connect :: connect mshrs.io.resp.ready, io.lsu.ll_resp.ready
[2807] FIRRTL:200576 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:895:22 KIND:wire :: wire s3_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}
[2808] FIRRTL:200577 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:896:20 KIND:reg :: reg s3_req_REG : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}, clock
[2809] FIRRTL:200578 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:896:20 KIND:connect :: connect s3_req_REG, s2_req[0]
[2811] FIRRTL:200580 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:897:38 KIND:node :: node _s3_valid_T = and(s2_valid[0], s2_hit[0])
[2812] FIRRTL:200581 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s3_valid_T_1 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[2813] FIRRTL:200582 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s3_valid_T_2 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[2814] FIRRTL:200583 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s3_valid_T_3 = or(_s3_valid_T_1, _s3_valid_T_2)
[2815] FIRRTL:200584 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s3_valid_T_4 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[2816] FIRRTL:200585 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s3_valid_T_5 = or(_s3_valid_T_3, _s3_valid_T_4)
[2817] FIRRTL:200586 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_6 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[2818] FIRRTL:200587 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_7 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[2819] FIRRTL:200588 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_8 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[2820] FIRRTL:200589 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_9 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[2821] FIRRTL:200590 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_10 = or(_s3_valid_T_6, _s3_valid_T_7)
[2822] FIRRTL:200591 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_11 = or(_s3_valid_T_10, _s3_valid_T_8)
[2823] FIRRTL:200592 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_12 = or(_s3_valid_T_11, _s3_valid_T_9)
[2824] FIRRTL:200593 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_13 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[2825] FIRRTL:200594 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_14 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[2826] FIRRTL:200595 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_15 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[2827] FIRRTL:200596 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_16 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[2828] FIRRTL:200597 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s3_valid_T_17 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[2829] FIRRTL:200598 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_18 = or(_s3_valid_T_13, _s3_valid_T_14)
[2830] FIRRTL:200599 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_19 = or(_s3_valid_T_18, _s3_valid_T_15)
[2831] FIRRTL:200600 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_20 = or(_s3_valid_T_19, _s3_valid_T_16)
[2832] FIRRTL:200601 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s3_valid_T_21 = or(_s3_valid_T_20, _s3_valid_T_17)
[2833] FIRRTL:200602 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s3_valid_T_22 = or(_s3_valid_T_12, _s3_valid_T_21)
[2834] FIRRTL:200603 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s3_valid_T_23 = or(_s3_valid_T_5, _s3_valid_T_22)
[2835] FIRRTL:200604 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:897:51 KIND:node :: node _s3_valid_T_24 = and(_s3_valid_T, _s3_valid_T_23)
[2836] FIRRTL:200605 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:898:26 KIND:node :: node _s3_valid_T_25 = eq(s2_sc_fail, UInt<1>(0h0))
[2837] FIRRTL:200606 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:897:85 KIND:node :: node _s3_valid_T_26 = and(_s3_valid_T_24, _s3_valid_T_25)
[2838] FIRRTL:200607 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:898:59 KIND:node :: node _s3_valid_T_27 = and(s2_send_nack[0], s2_nack[0])
[2839] FIRRTL:200608 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:898:41 KIND:node :: node _s3_valid_T_28 = eq(_s3_valid_T_27, UInt<1>(0h0))
[2840] FIRRTL:200609 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:898:38 KIND:node :: node _s3_valid_T_29 = and(_s3_valid_T_26, _s3_valid_T_28)
[2841] FIRRTL:200610 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:897:25 KIND:reg :: reg s3_valid : UInt<1>, clock
[2842] FIRRTL:200611 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:897:25 KIND:connect :: connect s3_valid, _s3_valid_T_29
[2843] FIRRTL:200612 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:899:29 KIND:reg :: reg s3_data_word : UInt, clock
[2844] FIRRTL:200613 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:899:29 KIND:connect :: connect s3_data_word, s2_data_word[0]
[2845] FIRRTL:200614 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:908:25 KIND:reg :: reg s4_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}, clock
[2846] FIRRTL:200615 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:908:25 KIND:connect :: connect s4_req, s3_req
[2847] FIRRTL:200616 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:909:25 KIND:reg :: reg s4_valid : UInt<1>, clock
[2848] FIRRTL:200617 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:909:25 KIND:connect :: connect s4_valid, s3_valid
[2849] FIRRTL:200618 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:910:25 KIND:reg :: reg s5_req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}, clock
[2850] FIRRTL:200619 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:910:25 KIND:connect :: connect s5_req, s4_req
[2851] FIRRTL:200620 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:911:25 KIND:reg :: reg s5_valid : UInt<1>, clock
[2852] FIRRTL:200621 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:911:25 KIND:connect :: connect s5_valid, s4_valid
[2857] FIRRTL:200626 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s3_bypass : UInt<1>[1]
[2863] FIRRTL:200632 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s4_bypass : UInt<1>[1]
[2869] FIRRTL:200638 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:wire :: wire s5_bypass : UInt<1>[1]
[2875] FIRRTL:200644 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:924:24 KIND:structural :: inst amoalu of AMOALU
[2876] FIRRTL:200645 SRC:<no-source-locator> KIND:connect :: connect amoalu.clock, clock
[2877] FIRRTL:200646 SRC:<no-source-locator> KIND:connect :: connect amoalu.reset, reset
[2878] FIRRTL:200647 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11:18 KIND:wire :: wire amoalu_io_mask_size : UInt<2>
[2879] FIRRTL:200648 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect amoalu_io_mask_size, s3_req.uop.mem_size
[2880] FIRRTL:200649 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:27 KIND:node :: node _amoalu_io_mask_upper_T = bits(s3_req.addr, 0, 0)
[2881] FIRRTL:200650 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:22 KIND:node :: node _amoalu_io_mask_upper_T_1 = mux(_amoalu_io_mask_upper_T, UInt<1>(0h1), UInt<1>(0h0))
[2882] FIRRTL:200651 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:53 KIND:node :: node _amoalu_io_mask_upper_T_2 = geq(amoalu_io_mask_size, UInt<1>(0h1))
[2883] FIRRTL:200652 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:47 KIND:node :: node _amoalu_io_mask_upper_T_3 = mux(_amoalu_io_mask_upper_T_2, UInt<1>(0h1), UInt<1>(0h0))
[2884] FIRRTL:200653 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:42 KIND:node :: node amoalu_io_mask_upper = or(_amoalu_io_mask_upper_T_1, _amoalu_io_mask_upper_T_3)
[2885] FIRRTL:200654 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:27 KIND:node :: node _amoalu_io_mask_lower_T = bits(s3_req.addr, 0, 0)
[2886] FIRRTL:200655 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:22 KIND:node :: node amoalu_io_mask_lower = mux(_amoalu_io_mask_lower_T, UInt<1>(0h0), UInt<1>(0h1))
[2887] FIRRTL:200656 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:22:16 KIND:node :: node _amoalu_io_mask_T = cat(amoalu_io_mask_upper, amoalu_io_mask_lower)
[2888] FIRRTL:200657 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:27 KIND:node :: node _amoalu_io_mask_upper_T_4 = bits(s3_req.addr, 1, 1)
[2889] FIRRTL:200658 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:22 KIND:node :: node _amoalu_io_mask_upper_T_5 = mux(_amoalu_io_mask_upper_T_4, _amoalu_io_mask_T, UInt<1>(0h0))
[2890] FIRRTL:200659 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:53 KIND:node :: node _amoalu_io_mask_upper_T_6 = geq(amoalu_io_mask_size, UInt<2>(0h2))
[2891] FIRRTL:200660 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:47 KIND:node :: node _amoalu_io_mask_upper_T_7 = mux(_amoalu_io_mask_upper_T_6, UInt<2>(0h3), UInt<1>(0h0))
[2892] FIRRTL:200661 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:42 KIND:node :: node amoalu_io_mask_upper_1 = or(_amoalu_io_mask_upper_T_5, _amoalu_io_mask_upper_T_7)
[2893] FIRRTL:200662 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:27 KIND:node :: node _amoalu_io_mask_lower_T_1 = bits(s3_req.addr, 1, 1)
[2894] FIRRTL:200663 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:22 KIND:node :: node amoalu_io_mask_lower_1 = mux(_amoalu_io_mask_lower_T_1, UInt<1>(0h0), _amoalu_io_mask_T)
[2895] FIRRTL:200664 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:22:16 KIND:node :: node _amoalu_io_mask_T_1 = cat(amoalu_io_mask_upper_1, amoalu_io_mask_lower_1)
[2896] FIRRTL:200665 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:27 KIND:node :: node _amoalu_io_mask_upper_T_8 = bits(s3_req.addr, 2, 2)
[2897] FIRRTL:200666 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:22 KIND:node :: node _amoalu_io_mask_upper_T_9 = mux(_amoalu_io_mask_upper_T_8, _amoalu_io_mask_T_1, UInt<1>(0h0))
[2898] FIRRTL:200667 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:53 KIND:node :: node _amoalu_io_mask_upper_T_10 = geq(amoalu_io_mask_size, UInt<2>(0h3))
[2899] FIRRTL:200668 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:47 KIND:node :: node _amoalu_io_mask_upper_T_11 = mux(_amoalu_io_mask_upper_T_10, UInt<4>(0hf), UInt<1>(0h0))
[2900] FIRRTL:200669 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:20:42 KIND:node :: node amoalu_io_mask_upper_2 = or(_amoalu_io_mask_upper_T_9, _amoalu_io_mask_upper_T_11)
[2901] FIRRTL:200670 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:27 KIND:node :: node _amoalu_io_mask_lower_T_2 = bits(s3_req.addr, 2, 2)
[2902] FIRRTL:200671 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:21:22 KIND:node :: node amoalu_io_mask_lower_2 = mux(_amoalu_io_mask_lower_T_2, UInt<1>(0h0), _amoalu_io_mask_T_1)
[2903] FIRRTL:200672 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:22:16 KIND:node :: node _amoalu_io_mask_T_2 = cat(amoalu_io_mask_upper_2, amoalu_io_mask_lower_2)
[2904] FIRRTL:200673 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:925:18 KIND:connect :: connect amoalu.io.mask, _amoalu_io_mask_T_2
[2905] FIRRTL:200674 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:926:18 KIND:connect :: connect amoalu.io.cmd, s3_req.uop.mem_cmd
[2906] FIRRTL:200675 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:927:18 KIND:connect :: connect amoalu.io.lhs, s3_data_word
[2907] FIRRTL:200676 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:928:28 KIND:reg :: reg amoalu_io_rhs_REG : UInt, clock
[2908] FIRRTL:200677 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:928:28 KIND:connect :: connect amoalu_io_rhs_REG, s2_req[0].data
[2909] FIRRTL:200678 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:928:18 KIND:connect :: connect amoalu.io.rhs, amoalu_io_rhs_REG
[2911] FIRRTL:200680 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:932:25 KIND:reg :: reg s3_way : UInt, clock
[2912] FIRRTL:200681 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:932:25 KIND:connect :: connect s3_way, s2_tag_match_way[0]
[2913] FIRRTL:200682 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:934:37 KIND:connect :: connect dataWriteArb.io.in[0].valid, s3_valid
[2914] FIRRTL:200683 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:935:37 KIND:connect :: connect dataWriteArb.io.in[0].bits.addr, s3_req.addr
[2915] FIRRTL:200684 SRC:src/main/scala/chisel3/util/OneHot.scala:58:35 KIND:node :: node _dataWriteArb_io_in_0_bits_wmask_T = dshl(UInt<1>(0h1), UInt<1>(0h0))
[2916] FIRRTL:200685 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:936:37 KIND:connect :: connect dataWriteArb.io.in[0].bits.wmask, _dataWriteArb_io_in_0_bits_wmask_T
[2917] FIRRTL:200686 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:937:37 KIND:connect :: connect dataWriteArb.io.in[0].bits.data, s3_req.data
[2918] FIRRTL:200687 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:938:37 KIND:connect :: connect dataWriteArb.io.in[0].bits.way_en, s3_way
[2919] FIRRTL:200688 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:941:43 KIND:node :: node _io_lsu_ordered_T = eq(s1_valid[0], UInt<1>(0h0))
[2920] FIRRTL:200689 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:941:40 KIND:node :: node _io_lsu_ordered_T_1 = and(mshrs.io.fence_rdy, _io_lsu_ordered_T)
[2921] FIRRTL:200690 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:941:69 KIND:node :: node _io_lsu_ordered_T_2 = eq(s2_valid[0], UInt<1>(0h0))
[2922] FIRRTL:200691 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:941:66 KIND:node :: node _io_lsu_ordered_T_3 = and(_io_lsu_ordered_T_1, _io_lsu_ordered_T_2)
[2923] FIRRTL:200692 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:941:18 KIND:connect :: connect io.lsu.ordered, _io_lsu_ordered_T_3
```

## Autonomous decision procedure

Synthesize the most conservative parent-facing abstraction that preserves
memory/coherence ordering, visibility, identity, exclusion, conservation, and
path facts contributed by the combination of frozen children plus parent-local
RTL.

There are exactly two expected outcomes:

1. **Current language is sufficient.** Emit `FINAL MCM-AGENT RESULT` followed by
   one fenced JSON object matching `expected_output_schema.json` in this response.
2. **Current language has a real gap.** Emit `MCM-AGENT LANGUAGE GAP` and explain
   the grounded missing concept, why existing AST forms change its meaning, and
   the minimal reusable extension. A missing composition proof capability is not
   a language gap.

For the normal JSON outcome, use this exact envelope:

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomNonBlockingDCache-59b0ae1731a92b08",
  "work_unit_id": "BoomNonBlockingDCache",
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

For a parent result, `extensions` should normally have this shape:

```json
{
  "parent_synthesis": {
    "axiom_provenance": {
      "A1": {
        "kind": "parent_local",
        "source_axioms": [],
        "note": "..."
      }
    }
  }
}
```

IDs inside each list must be unique and stable. Physical references and
parent-local evidence must use exact IDs from this prompt.
