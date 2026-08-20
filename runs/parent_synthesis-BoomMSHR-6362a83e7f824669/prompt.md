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

Task ID: `parent_synthesis-BoomMSHR-6362a83e7f824669`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `parent-synthesis-prompt-0.1`
Output schema version: `umcm-formal-0.5`

## Parent WorkUnit

- id: `BoomMSHR`
- module: `BoomMSHR`
- kind: `module`
- instance path: `BoomMSHR`
- leaf: `False`
- coverage complete: `True`
- parent-local raw statements after child replacement: 2216
- parent-local logical statements after child replacement: 392
- parent-local registers: 11
- parent-local physical boundary events: 15

## Composition rules

1. Frozen child axioms are already trusted and remain imported automatically when
   this parent is frozen. Do **not** mechanically copy every child axiom into the
   parent candidate. Grounding signals/state/evidence stored inside a frozen child
   summary are provenance only: do not treat them as parent-local RTL evidence or
   infer new child behavior beyond the trusted frozen semantics.
2. Child semantic objects may be referenced by the exact qualified IDs shown in
   each child's semantic catalog. Do not redeclare an imported occurrence,
   predicate, identity, case, or axiom under the same qualified ID.
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
     axiom catalogs;
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

- `BoomMSHR::io.idx.valid`
  - predicate: `io.idx.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.idx.bits']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.lb_write.valid`
  - predicate: `io.lb_write.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.lb_write.bits.data', 'io.lb_write.bits.offset']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.mem_acquire.fire`
  - predicate: `io.mem_acquire.valid && io.mem_acquire.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.mem_acquire.bits.address', 'io.mem_acquire.bits.corrupt', 'io.mem_acquire.bits.data', 'io.mem_acquire.bits.mask', 'io.mem_acquire.bits.opcode', 'io.mem_acquire.bits.param', 'io.mem_acquire.bits.size', 'io.mem_acquire.bits.source']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.mem_finish.fire`
  - predicate: `io.mem_finish.valid && io.mem_finish.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.mem_finish.bits.sink']
  - immediate registers: ['grantack', 'state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.mem_grant.fire`
  - predicate: `io.mem_grant.valid && io.mem_grant.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.mem_grant.bits.corrupt', 'io.mem_grant.bits.data', 'io.mem_grant.bits.denied', 'io.mem_grant.bits.opcode', 'io.mem_grant.bits.param', 'io.mem_grant.bits.sink', 'io.mem_grant.bits.size', 'io.mem_grant.bits.source']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.meta_read.fire`
  - predicate: `io.meta_read.valid && io.meta_read.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en']
  - immediate registers: ['grantack', 'req', 'state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.meta_resp.valid`
  - predicate: `io.meta_resp.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.meta_resp.bits.coh.state', 'io.meta_resp.bits.tag']
  - immediate registers: []
  - historical registers: []
- `BoomMSHR::io.meta_write.fire`
  - predicate: `io.meta_write.valid && io.meta_write.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.prober_state.valid`
  - predicate: `io.prober_state.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.prober_state.bits']
  - immediate registers: []
  - historical registers: []
- `BoomMSHR::io.refill.fire`
  - predicate: `io.refill.valid && io.refill.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.refill.bits.addr', 'io.refill.bits.data', 'io.refill.bits.way_en', 'io.refill.bits.wmask']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.replay.fire`
  - predicate: `io.replay.valid && io.replay.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.replay.bits.addr', 'io.replay.bits.data', 'io.replay.bits.is_hella', 'io.replay.bits.old_meta.coh.state', 'io.replay.bits.old_meta.tag', 'io.replay.bits.sdq_id', 'io.replay.bits.tag_match', 'io.replay.bits.uop.bp_debug_if', 'io.replay.bits.uop.bp_xcpt_if', 'io.replay.bits.uop.br_mask', 'io.replay.bits.uop.br_tag', 'io.replay.bits.uop.br_type', 'io.replay.bits.uop.csr_cmd', 'io.replay.bits.uop.debug_fsrc', 'io.replay.bits.uop.debug_inst', 'io.replay.bits.uop.debug_pc', 'io.replay.bits.uop.debug_tsrc', 'io.replay.bits.uop.dis_col_sel', 'io.replay.bits.uop.dst_rtype', 'io.replay.bits.uop.edge_inst', 'io.replay.bits.uop.exc_cause', 'io.replay.bits.uop.exception', 'io.replay.bits.uop.fcn_dw', 'io.replay.bits.uop.fcn_op', 'io.replay.bits.uop.flush_on_commit', 'io.replay.bits.uop.fp_ctrl.div', 'io.replay.bits.uop.fp_ctrl.fastpipe', 'io.replay.bits.uop.fp_ctrl.fma', 'io.replay.bits.uop.fp_ctrl.fromint', 'io.replay.bits.uop.fp_ctrl.ldst', 'io.replay.bits.uop.fp_ctrl.ren1', 'io.replay.bits.uop.fp_ctrl.ren2', 'io.replay.bits.uop.fp_ctrl.ren3', 'io.replay.bits.uop.fp_ctrl.sqrt', 'io.replay.bits.uop.fp_ctrl.swap12', 'io.replay.bits.uop.fp_ctrl.swap23', 'io.replay.bits.uop.fp_ctrl.toint', 'io.replay.bits.uop.fp_ctrl.typeTagIn', 'io.replay.bits.uop.fp_ctrl.typeTagOut', 'io.replay.bits.uop.fp_ctrl.vec', 'io.replay.bits.uop.fp_ctrl.wen', 'io.replay.bits.uop.fp_ctrl.wflags', 'io.replay.bits.uop.fp_rm', 'io.replay.bits.uop.fp_typ', 'io.replay.bits.uop.fp_val', 'io.replay.bits.uop.frs3_en', 'io.replay.bits.uop.ftq_idx', 'io.replay.bits.uop.fu_code[0]', 'io.replay.bits.uop.fu_code[1]', 'io.replay.bits.uop.fu_code[2]', 'io.replay.bits.uop.fu_code[3]', 'io.replay.bits.uop.fu_code[4]', 'io.replay.bits.uop.fu_code[5]', 'io.replay.bits.uop.fu_code[6]', 'io.replay.bits.uop.fu_code[7]', 'io.replay.bits.uop.fu_code[8]', 'io.replay.bits.uop.fu_code[9]', 'io.replay.bits.uop.imm_packed', 'io.replay.bits.uop.imm_rename', 'io.replay.bits.uop.imm_sel', 'io.replay.bits.uop.inst', 'io.replay.bits.uop.iq_type[0]', 'io.replay.bits.uop.iq_type[1]', 'io.replay.bits.uop.iq_type[2]', 'io.replay.bits.uop.iq_type[3]', 'io.replay.bits.uop.is_amo', 'io.replay.bits.uop.is_eret', 'io.replay.bits.uop.is_fence', 'io.replay.bits.uop.is_fencei', 'io.replay.bits.uop.is_mov', 'io.replay.bits.uop.is_rocc', 'io.replay.bits.uop.is_rvc', 'io.replay.bits.uop.is_sfb', 'io.replay.bits.uop.is_sfence', 'io.replay.bits.uop.is_sys_pc2epc', 'io.replay.bits.uop.is_unique', 'io.replay.bits.uop.iw_issued', 'io.replay.bits.uop.iw_issued_partial_agen', 'io.replay.bits.uop.iw_issued_partial_dgen', 'io.replay.bits.uop.iw_p1_bypass_hint', 'io.replay.bits.uop.iw_p1_speculative_child', 'io.replay.bits.uop.iw_p2_bypass_hint', 'io.replay.bits.uop.iw_p2_speculative_child', 'io.replay.bits.uop.iw_p3_bypass_hint', 'io.replay.bits.uop.ldq_idx', 'io.replay.bits.uop.ldst', 'io.replay.bits.uop.ldst_is_rs1', 'io.replay.bits.uop.lrs1', 'io.replay.bits.uop.lrs1_rtype', 'io.replay.bits.uop.lrs2', 'io.replay.bits.uop.lrs2_rtype', 'io.replay.bits.uop.lrs3', 'io.replay.bits.uop.mem_cmd', 'io.replay.bits.uop.mem_signed', 'io.replay.bits.uop.mem_size', 'io.replay.bits.uop.op1_sel', 'io.replay.bits.uop.op2_sel', 'io.replay.bits.uop.pc_lob', 'io.replay.bits.uop.pdst', 'io.replay.bits.uop.pimm', 'io.replay.bits.uop.ppred', 'io.replay.bits.uop.ppred_busy', 'io.replay.bits.uop.prs1', 'io.replay.bits.uop.prs1_busy', 'io.replay.bits.uop.prs2', 'io.replay.bits.uop.prs2_busy', 'io.replay.bits.uop.prs3', 'io.replay.bits.uop.prs3_busy', 'io.replay.bits.uop.rob_idx', 'io.replay.bits.uop.rxq_idx', 'io.replay.bits.uop.stale_pdst', 'io.replay.bits.uop.stq_idx', 'io.replay.bits.uop.taken', 'io.replay.bits.uop.uses_ldq', 'io.replay.bits.uop.uses_stq', 'io.replay.bits.uop.xcpt_ae_if', 'io.replay.bits.uop.xcpt_ma_if', 'io.replay.bits.uop.xcpt_pf_if', 'io.replay.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.resp.fire`
  - predicate: `io.resp.valid && io.resp.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.tag.valid`
  - predicate: `io.tag.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.tag.bits']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.way.valid`
  - predicate: `io.way.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.way.bits']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']
- `BoomMSHR::io.wb_req.fire`
  - predicate: `io.wb_req.valid && io.wb_req.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'state']

## Parent-local concrete state

['commit_line', 'finish_to_prefetch', 'grant_had_data', 'grantack', 'meta_hazard', 'new_coh', 'r_counter', 'refill_ctr', 'req', 'req_needs_wb', 'state']

## Parent frontier signals

['clock', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.brupdate.b2.cfi_type', 'io.brupdate.b2.jalr_target', 'io.brupdate.b2.mispredict', 'io.brupdate.b2.pc_sel', 'io.brupdate.b2.taken', 'io.brupdate.b2.target_offset', 'io.brupdate.b2.uop.bp_debug_if', 'io.brupdate.b2.uop.bp_xcpt_if', 'io.brupdate.b2.uop.br_mask', 'io.brupdate.b2.uop.br_tag', 'io.brupdate.b2.uop.br_type', 'io.brupdate.b2.uop.csr_cmd', 'io.brupdate.b2.uop.debug_fsrc', 'io.brupdate.b2.uop.debug_inst', 'io.brupdate.b2.uop.debug_pc', 'io.brupdate.b2.uop.debug_tsrc', 'io.brupdate.b2.uop.dis_col_sel', 'io.brupdate.b2.uop.dst_rtype', 'io.brupdate.b2.uop.edge_inst', 'io.brupdate.b2.uop.exc_cause', 'io.brupdate.b2.uop.exception', 'io.brupdate.b2.uop.fcn_dw', 'io.brupdate.b2.uop.fcn_op', 'io.brupdate.b2.uop.flush_on_commit', 'io.brupdate.b2.uop.fp_ctrl.div', 'io.brupdate.b2.uop.fp_ctrl.fastpipe', 'io.brupdate.b2.uop.fp_ctrl.fma', 'io.brupdate.b2.uop.fp_ctrl.fromint', 'io.brupdate.b2.uop.fp_ctrl.ldst', 'io.brupdate.b2.uop.fp_ctrl.ren1', 'io.brupdate.b2.uop.fp_ctrl.ren2', 'io.brupdate.b2.uop.fp_ctrl.ren3', 'io.brupdate.b2.uop.fp_ctrl.sqrt', 'io.brupdate.b2.uop.fp_ctrl.swap12', 'io.brupdate.b2.uop.fp_ctrl.swap23', 'io.brupdate.b2.uop.fp_ctrl.toint', 'io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'io.brupdate.b2.uop.fp_ctrl.vec', 'io.brupdate.b2.uop.fp_ctrl.wen', 'io.brupdate.b2.uop.fp_ctrl.wflags', 'io.brupdate.b2.uop.fp_rm', 'io.brupdate.b2.uop.fp_typ', 'io.brupdate.b2.uop.fp_val', 'io.brupdate.b2.uop.frs3_en', 'io.brupdate.b2.uop.ftq_idx', 'io.brupdate.b2.uop.fu_code[0]', 'io.brupdate.b2.uop.fu_code[1]', 'io.brupdate.b2.uop.fu_code[2]', 'io.brupdate.b2.uop.fu_code[3]', 'io.brupdate.b2.uop.fu_code[4]', 'io.brupdate.b2.uop.fu_code[5]', 'io.brupdate.b2.uop.fu_code[6]', 'io.brupdate.b2.uop.fu_code[7]', 'io.brupdate.b2.uop.fu_code[8]', 'io.brupdate.b2.uop.fu_code[9]', 'io.brupdate.b2.uop.imm_packed', 'io.brupdate.b2.uop.imm_rename', 'io.brupdate.b2.uop.imm_sel', 'io.brupdate.b2.uop.inst', 'io.brupdate.b2.uop.iq_type[0]', 'io.brupdate.b2.uop.iq_type[1]', 'io.brupdate.b2.uop.iq_type[2]', 'io.brupdate.b2.uop.iq_type[3]', 'io.brupdate.b2.uop.is_amo', 'io.brupdate.b2.uop.is_eret', 'io.brupdate.b2.uop.is_fence', 'io.brupdate.b2.uop.is_fencei', 'io.brupdate.b2.uop.is_mov', 'io.brupdate.b2.uop.is_rocc', 'io.brupdate.b2.uop.is_rvc', 'io.brupdate.b2.uop.is_sfb', 'io.brupdate.b2.uop.is_sfence', 'io.brupdate.b2.uop.is_sys_pc2epc', 'io.brupdate.b2.uop.is_unique', 'io.brupdate.b2.uop.iw_issued', 'io.brupdate.b2.uop.iw_issued_partial_agen', 'io.brupdate.b2.uop.iw_issued_partial_dgen', 'io.brupdate.b2.uop.iw_p1_bypass_hint', 'io.brupdate.b2.uop.iw_p1_speculative_child', 'io.brupdate.b2.uop.iw_p2_bypass_hint', 'io.brupdate.b2.uop.iw_p2_speculative_child', 'io.brupdate.b2.uop.iw_p3_bypass_hint', 'io.brupdate.b2.uop.ldq_idx', 'io.brupdate.b2.uop.ldst', 'io.brupdate.b2.uop.ldst_is_rs1', 'io.brupdate.b2.uop.lrs1', 'io.brupdate.b2.uop.lrs1_rtype', 'io.brupdate.b2.uop.lrs2', 'io.brupdate.b2.uop.lrs2_rtype', 'io.brupdate.b2.uop.lrs3', 'io.brupdate.b2.uop.mem_cmd', 'io.brupdate.b2.uop.mem_signed', 'io.brupdate.b2.uop.mem_size', 'io.brupdate.b2.uop.op1_sel', 'io.brupdate.b2.uop.op2_sel', 'io.brupdate.b2.uop.pc_lob', 'io.brupdate.b2.uop.pdst', 'io.brupdate.b2.uop.pimm', 'io.brupdate.b2.uop.ppred', 'io.brupdate.b2.uop.ppred_busy', 'io.brupdate.b2.uop.prs1', 'io.brupdate.b2.uop.prs1_busy', 'io.brupdate.b2.uop.prs2', 'io.brupdate.b2.uop.prs2_busy', 'io.brupdate.b2.uop.prs3', 'io.brupdate.b2.uop.prs3_busy', 'io.brupdate.b2.uop.rob_idx', 'io.brupdate.b2.uop.rxq_idx', 'io.brupdate.b2.uop.stale_pdst', 'io.brupdate.b2.uop.stq_idx', 'io.brupdate.b2.uop.taken', 'io.brupdate.b2.uop.uses_ldq', 'io.brupdate.b2.uop.uses_stq', 'io.brupdate.b2.uop.xcpt_ae_if', 'io.brupdate.b2.uop.xcpt_ma_if', 'io.brupdate.b2.uop.xcpt_pf_if', 'io.clear_prefetch', 'io.commit_addr', 'io.commit_coh.state', 'io.commit_val', 'io.exception', 'io.id', 'io.idx.bits', 'io.idx.valid', 'io.lb_read.offset', 'io.lb_resp', 'io.lb_write.bits.data', 'io.lb_write.bits.offset', 'io.lb_write.valid', 'io.mem_acquire.bits.address', 'io.mem_acquire.bits.corrupt', 'io.mem_acquire.bits.data', 'io.mem_acquire.bits.mask', 'io.mem_acquire.bits.opcode', 'io.mem_acquire.bits.param', 'io.mem_acquire.bits.size', 'io.mem_acquire.bits.source', 'io.mem_acquire.ready', 'io.mem_acquire.valid', 'io.mem_finish.bits.sink', 'io.mem_finish.ready', 'io.mem_finish.valid', 'io.mem_grant.bits.data', 'io.mem_grant.bits.opcode', 'io.mem_grant.bits.param', 'io.mem_grant.bits.sink', 'io.mem_grant.bits.size', 'io.mem_grant.ready', 'io.mem_grant.valid', 'io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en', 'io.meta_read.ready', 'io.meta_read.valid', 'io.meta_resp.bits.coh.state', 'io.meta_resp.valid', 'io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en', 'io.meta_write.ready', 'io.meta_write.valid', 'io.probe_rdy', 'io.prober_state.bits', 'io.prober_state.valid', 'io.refill.bits.addr', 'io.refill.bits.data', 'io.refill.bits.way_en', 'io.refill.bits.wmask', 'io.refill.ready', 'io.refill.valid', 'io.replay.bits.addr', 'io.replay.bits.data', 'io.replay.bits.is_hella', 'io.replay.bits.old_meta.coh.state', 'io.replay.bits.old_meta.tag', 'io.replay.bits.sdq_id', 'io.replay.bits.tag_match', 'io.replay.bits.uop.bp_debug_if', 'io.replay.bits.uop.bp_xcpt_if', 'io.replay.bits.uop.br_mask', 'io.replay.bits.uop.br_tag', 'io.replay.bits.uop.br_type', 'io.replay.bits.uop.csr_cmd', 'io.replay.bits.uop.debug_fsrc', 'io.replay.bits.uop.debug_inst', 'io.replay.bits.uop.debug_pc', 'io.replay.bits.uop.debug_tsrc', 'io.replay.bits.uop.dis_col_sel', 'io.replay.bits.uop.dst_rtype', 'io.replay.bits.uop.edge_inst', 'io.replay.bits.uop.exc_cause', 'io.replay.bits.uop.exception', 'io.replay.bits.uop.fcn_dw', 'io.replay.bits.uop.fcn_op', 'io.replay.bits.uop.flush_on_commit', 'io.replay.bits.uop.fp_ctrl.div', 'io.replay.bits.uop.fp_ctrl.fastpipe', 'io.replay.bits.uop.fp_ctrl.fma', 'io.replay.bits.uop.fp_ctrl.fromint', 'io.replay.bits.uop.fp_ctrl.ldst', 'io.replay.bits.uop.fp_ctrl.ren1', 'io.replay.bits.uop.fp_ctrl.ren2', 'io.replay.bits.uop.fp_ctrl.ren3', 'io.replay.bits.uop.fp_ctrl.sqrt', 'io.replay.bits.uop.fp_ctrl.swap12', 'io.replay.bits.uop.fp_ctrl.swap23', 'io.replay.bits.uop.fp_ctrl.toint', 'io.replay.bits.uop.fp_ctrl.typeTagIn', 'io.replay.bits.uop.fp_ctrl.typeTagOut', 'io.replay.bits.uop.fp_ctrl.vec', 'io.replay.bits.uop.fp_ctrl.wen', 'io.replay.bits.uop.fp_ctrl.wflags', 'io.replay.bits.uop.fp_rm', 'io.replay.bits.uop.fp_typ', 'io.replay.bits.uop.fp_val', 'io.replay.bits.uop.frs3_en', 'io.replay.bits.uop.ftq_idx', 'io.replay.bits.uop.fu_code[0]', 'io.replay.bits.uop.fu_code[1]', 'io.replay.bits.uop.fu_code[2]', 'io.replay.bits.uop.fu_code[3]', 'io.replay.bits.uop.fu_code[4]', 'io.replay.bits.uop.fu_code[5]', 'io.replay.bits.uop.fu_code[6]', 'io.replay.bits.uop.fu_code[7]', 'io.replay.bits.uop.fu_code[8]', 'io.replay.bits.uop.fu_code[9]', 'io.replay.bits.uop.imm_packed', 'io.replay.bits.uop.imm_rename', 'io.replay.bits.uop.imm_sel', 'io.replay.bits.uop.inst', 'io.replay.bits.uop.iq_type[0]', 'io.replay.bits.uop.iq_type[1]', 'io.replay.bits.uop.iq_type[2]', 'io.replay.bits.uop.iq_type[3]', 'io.replay.bits.uop.is_amo', 'io.replay.bits.uop.is_eret', 'io.replay.bits.uop.is_fence', 'io.replay.bits.uop.is_fencei', 'io.replay.bits.uop.is_mov', 'io.replay.bits.uop.is_rocc', 'io.replay.bits.uop.is_rvc', 'io.replay.bits.uop.is_sfb', 'io.replay.bits.uop.is_sfence', 'io.replay.bits.uop.is_sys_pc2epc', 'io.replay.bits.uop.is_unique', 'io.replay.bits.uop.iw_issued', 'io.replay.bits.uop.iw_issued_partial_agen', 'io.replay.bits.uop.iw_issued_partial_dgen', 'io.replay.bits.uop.iw_p1_bypass_hint', 'io.replay.bits.uop.iw_p1_speculative_child', 'io.replay.bits.uop.iw_p2_bypass_hint', 'io.replay.bits.uop.iw_p2_speculative_child', 'io.replay.bits.uop.iw_p3_bypass_hint', 'io.replay.bits.uop.ldq_idx', 'io.replay.bits.uop.ldst', 'io.replay.bits.uop.ldst_is_rs1', 'io.replay.bits.uop.lrs1', 'io.replay.bits.uop.lrs1_rtype', 'io.replay.bits.uop.lrs2', 'io.replay.bits.uop.lrs2_rtype', 'io.replay.bits.uop.lrs3', 'io.replay.bits.uop.mem_cmd', 'io.replay.bits.uop.mem_signed', 'io.replay.bits.uop.mem_size', 'io.replay.bits.uop.op1_sel', 'io.replay.bits.uop.op2_sel', 'io.replay.bits.uop.pc_lob', 'io.replay.bits.uop.pdst', 'io.replay.bits.uop.pimm', 'io.replay.bits.uop.ppred', 'io.replay.bits.uop.ppred_busy', 'io.replay.bits.uop.prs1', 'io.replay.bits.uop.prs1_busy', 'io.replay.bits.uop.prs2', 'io.replay.bits.uop.prs2_busy', 'io.replay.bits.uop.prs3', 'io.replay.bits.uop.prs3_busy', 'io.replay.bits.uop.rob_idx', 'io.replay.bits.uop.rxq_idx', 'io.replay.bits.uop.stale_pdst', 'io.replay.bits.uop.stq_idx', 'io.replay.bits.uop.taken', 'io.replay.bits.uop.uses_ldq', 'io.replay.bits.uop.uses_stq', 'io.replay.bits.uop.xcpt_ae_if', 'io.replay.bits.uop.xcpt_ma_if', 'io.replay.bits.uop.xcpt_pf_if', 'io.replay.bits.way_en', 'io.replay.ready', 'io.replay.valid', 'io.req.addr', 'io.req.data', 'io.req.is_hella', 'io.req.old_meta.coh.state', 'io.req.old_meta.tag', 'io.req.sdq_id', 'io.req.tag_match', 'io.req.uop.bp_debug_if', 'io.req.uop.bp_xcpt_if', 'io.req.uop.br_mask', 'io.req.uop.br_tag', 'io.req.uop.br_type', 'io.req.uop.csr_cmd', 'io.req.uop.debug_fsrc', 'io.req.uop.debug_inst', 'io.req.uop.debug_pc', 'io.req.uop.debug_tsrc', 'io.req.uop.dis_col_sel', 'io.req.uop.dst_rtype', 'io.req.uop.edge_inst', 'io.req.uop.exc_cause', 'io.req.uop.exception', 'io.req.uop.fcn_dw', 'io.req.uop.fcn_op', 'io.req.uop.flush_on_commit', 'io.req.uop.fp_ctrl.div', 'io.req.uop.fp_ctrl.fastpipe', 'io.req.uop.fp_ctrl.fma', 'io.req.uop.fp_ctrl.fromint', 'io.req.uop.fp_ctrl.ldst', 'io.req.uop.fp_ctrl.ren1', 'io.req.uop.fp_ctrl.ren2', 'io.req.uop.fp_ctrl.ren3', 'io.req.uop.fp_ctrl.sqrt', 'io.req.uop.fp_ctrl.swap12', 'io.req.uop.fp_ctrl.swap23', 'io.req.uop.fp_ctrl.toint', 'io.req.uop.fp_ctrl.typeTagIn', 'io.req.uop.fp_ctrl.typeTagOut', 'io.req.uop.fp_ctrl.vec', 'io.req.uop.fp_ctrl.wen', 'io.req.uop.fp_ctrl.wflags', 'io.req.uop.fp_rm', 'io.req.uop.fp_typ', 'io.req.uop.fp_val', 'io.req.uop.frs3_en', 'io.req.uop.ftq_idx', 'io.req.uop.fu_code[0]', 'io.req.uop.fu_code[1]', 'io.req.uop.fu_code[2]', 'io.req.uop.fu_code[3]', 'io.req.uop.fu_code[4]', 'io.req.uop.fu_code[5]', 'io.req.uop.fu_code[6]', 'io.req.uop.fu_code[7]', 'io.req.uop.fu_code[8]', 'io.req.uop.fu_code[9]', 'io.req.uop.imm_packed', 'io.req.uop.imm_rename', 'io.req.uop.imm_sel', 'io.req.uop.inst', 'io.req.uop.iq_type[0]', 'io.req.uop.iq_type[1]', 'io.req.uop.iq_type[2]', 'io.req.uop.iq_type[3]', 'io.req.uop.is_amo', 'io.req.uop.is_eret', 'io.req.uop.is_fence', 'io.req.uop.is_fencei', 'io.req.uop.is_mov', 'io.req.uop.is_rocc', 'io.req.uop.is_rvc', 'io.req.uop.is_sfb', 'io.req.uop.is_sfence', 'io.req.uop.is_sys_pc2epc', 'io.req.uop.is_unique', 'io.req.uop.iw_issued', 'io.req.uop.iw_issued_partial_agen', 'io.req.uop.iw_issued_partial_dgen', 'io.req.uop.iw_p1_bypass_hint', 'io.req.uop.iw_p1_speculative_child', 'io.req.uop.iw_p2_bypass_hint', 'io.req.uop.iw_p2_speculative_child', 'io.req.uop.iw_p3_bypass_hint', 'io.req.uop.ldq_idx', 'io.req.uop.ldst', 'io.req.uop.ldst_is_rs1', 'io.req.uop.lrs1', 'io.req.uop.lrs1_rtype', 'io.req.uop.lrs2', 'io.req.uop.lrs2_rtype', 'io.req.uop.lrs3', 'io.req.uop.mem_cmd', 'io.req.uop.mem_signed', 'io.req.uop.mem_size', 'io.req.uop.op1_sel', 'io.req.uop.op2_sel', 'io.req.uop.pc_lob', 'io.req.uop.pdst', 'io.req.uop.pimm', 'io.req.uop.ppred', 'io.req.uop.ppred_busy', 'io.req.uop.prs1', 'io.req.uop.prs1_busy', 'io.req.uop.prs2', 'io.req.uop.prs2_busy', 'io.req.uop.prs3', 'io.req.uop.prs3_busy', 'io.req.uop.rob_idx', 'io.req.uop.rxq_idx', 'io.req.uop.stale_pdst', 'io.req.uop.stq_idx', 'io.req.uop.taken', 'io.req.uop.uses_ldq', 'io.req.uop.uses_stq', 'io.req.uop.xcpt_ae_if', 'io.req.uop.xcpt_ma_if', 'io.req.uop.xcpt_pf_if', 'io.req.way_en', 'io.req_is_probe', 'io.req_pri_rdy', 'io.req_pri_val', 'io.req_sec_rdy', 'io.req_sec_val', 'io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if', 'io.resp.ready', 'io.resp.valid', 'io.tag.bits', 'io.tag.valid', 'io.way.bits', 'io.way.valid', 'io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en', 'io.wb_req.ready', 'io.wb_req.valid', 'io.wb_resp', 'rpq.clock', 'rpq.io.brupdate.b1.mispredict_mask', 'rpq.io.brupdate.b1.resolve_mask', 'rpq.io.brupdate.b2.cfi_type', 'rpq.io.brupdate.b2.jalr_target', 'rpq.io.brupdate.b2.mispredict', 'rpq.io.brupdate.b2.pc_sel', 'rpq.io.brupdate.b2.taken', 'rpq.io.brupdate.b2.target_offset', 'rpq.io.brupdate.b2.uop.bp_debug_if', 'rpq.io.brupdate.b2.uop.bp_xcpt_if', 'rpq.io.brupdate.b2.uop.br_mask', 'rpq.io.brupdate.b2.uop.br_tag', 'rpq.io.brupdate.b2.uop.br_type', 'rpq.io.brupdate.b2.uop.csr_cmd', 'rpq.io.brupdate.b2.uop.debug_fsrc', 'rpq.io.brupdate.b2.uop.debug_inst', 'rpq.io.brupdate.b2.uop.debug_pc', 'rpq.io.brupdate.b2.uop.debug_tsrc', 'rpq.io.brupdate.b2.uop.dis_col_sel', 'rpq.io.brupdate.b2.uop.dst_rtype', 'rpq.io.brupdate.b2.uop.edge_inst', 'rpq.io.brupdate.b2.uop.exc_cause', 'rpq.io.brupdate.b2.uop.exception', 'rpq.io.brupdate.b2.uop.fcn_dw', 'rpq.io.brupdate.b2.uop.fcn_op', 'rpq.io.brupdate.b2.uop.flush_on_commit', 'rpq.io.brupdate.b2.uop.fp_ctrl.div', 'rpq.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'rpq.io.brupdate.b2.uop.fp_ctrl.fma', 'rpq.io.brupdate.b2.uop.fp_ctrl.fromint', 'rpq.io.brupdate.b2.uop.fp_ctrl.ldst', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren1', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren2', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren3', 'rpq.io.brupdate.b2.uop.fp_ctrl.sqrt', 'rpq.io.brupdate.b2.uop.fp_ctrl.swap12', 'rpq.io.brupdate.b2.uop.fp_ctrl.swap23', 'rpq.io.brupdate.b2.uop.fp_ctrl.toint', 'rpq.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'rpq.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'rpq.io.brupdate.b2.uop.fp_ctrl.vec', 'rpq.io.brupdate.b2.uop.fp_ctrl.wen', 'rpq.io.brupdate.b2.uop.fp_ctrl.wflags', 'rpq.io.brupdate.b2.uop.fp_rm', 'rpq.io.brupdate.b2.uop.fp_typ', 'rpq.io.brupdate.b2.uop.fp_val', 'rpq.io.brupdate.b2.uop.frs3_en', 'rpq.io.brupdate.b2.uop.ftq_idx', 'rpq.io.brupdate.b2.uop.fu_code[0]', 'rpq.io.brupdate.b2.uop.fu_code[1]', 'rpq.io.brupdate.b2.uop.fu_code[2]', 'rpq.io.brupdate.b2.uop.fu_code[3]', 'rpq.io.brupdate.b2.uop.fu_code[4]', 'rpq.io.brupdate.b2.uop.fu_code[5]', 'rpq.io.brupdate.b2.uop.fu_code[6]', 'rpq.io.brupdate.b2.uop.fu_code[7]', 'rpq.io.brupdate.b2.uop.fu_code[8]', 'rpq.io.brupdate.b2.uop.fu_code[9]', 'rpq.io.brupdate.b2.uop.imm_packed', 'rpq.io.brupdate.b2.uop.imm_rename', 'rpq.io.brupdate.b2.uop.imm_sel', 'rpq.io.brupdate.b2.uop.inst', 'rpq.io.brupdate.b2.uop.iq_type[0]', 'rpq.io.brupdate.b2.uop.iq_type[1]', 'rpq.io.brupdate.b2.uop.iq_type[2]', 'rpq.io.brupdate.b2.uop.iq_type[3]', 'rpq.io.brupdate.b2.uop.is_amo', 'rpq.io.brupdate.b2.uop.is_eret', 'rpq.io.brupdate.b2.uop.is_fence', 'rpq.io.brupdate.b2.uop.is_fencei', 'rpq.io.brupdate.b2.uop.is_mov', 'rpq.io.brupdate.b2.uop.is_rocc', 'rpq.io.brupdate.b2.uop.is_rvc', 'rpq.io.brupdate.b2.uop.is_sfb', 'rpq.io.brupdate.b2.uop.is_sfence', 'rpq.io.brupdate.b2.uop.is_sys_pc2epc', 'rpq.io.brupdate.b2.uop.is_unique', 'rpq.io.brupdate.b2.uop.iw_issued', 'rpq.io.brupdate.b2.uop.iw_issued_partial_agen', 'rpq.io.brupdate.b2.uop.iw_issued_partial_dgen', 'rpq.io.brupdate.b2.uop.iw_p1_bypass_hint', 'rpq.io.brupdate.b2.uop.iw_p1_speculative_child', 'rpq.io.brupdate.b2.uop.iw_p2_bypass_hint', 'rpq.io.brupdate.b2.uop.iw_p2_speculative_child', 'rpq.io.brupdate.b2.uop.iw_p3_bypass_hint', 'rpq.io.brupdate.b2.uop.ldq_idx', 'rpq.io.brupdate.b2.uop.ldst', 'rpq.io.brupdate.b2.uop.ldst_is_rs1', 'rpq.io.brupdate.b2.uop.lrs1', 'rpq.io.brupdate.b2.uop.lrs1_rtype', 'rpq.io.brupdate.b2.uop.lrs2', 'rpq.io.brupdate.b2.uop.lrs2_rtype', 'rpq.io.brupdate.b2.uop.lrs3', 'rpq.io.brupdate.b2.uop.mem_cmd', 'rpq.io.brupdate.b2.uop.mem_signed', 'rpq.io.brupdate.b2.uop.mem_size', 'rpq.io.brupdate.b2.uop.op1_sel', 'rpq.io.brupdate.b2.uop.op2_sel', 'rpq.io.brupdate.b2.uop.pc_lob', 'rpq.io.brupdate.b2.uop.pdst', 'rpq.io.brupdate.b2.uop.pimm', 'rpq.io.brupdate.b2.uop.ppred', 'rpq.io.brupdate.b2.uop.ppred_busy', 'rpq.io.brupdate.b2.uop.prs1', 'rpq.io.brupdate.b2.uop.prs1_busy', 'rpq.io.brupdate.b2.uop.prs2', 'rpq.io.brupdate.b2.uop.prs2_busy', 'rpq.io.brupdate.b2.uop.prs3', 'rpq.io.brupdate.b2.uop.prs3_busy', 'rpq.io.brupdate.b2.uop.rob_idx', 'rpq.io.brupdate.b2.uop.rxq_idx', 'rpq.io.brupdate.b2.uop.stale_pdst', 'rpq.io.brupdate.b2.uop.stq_idx', 'rpq.io.brupdate.b2.uop.taken', 'rpq.io.brupdate.b2.uop.uses_ldq', 'rpq.io.brupdate.b2.uop.uses_stq', 'rpq.io.brupdate.b2.uop.xcpt_ae_if', 'rpq.io.brupdate.b2.uop.xcpt_ma_if', 'rpq.io.brupdate.b2.uop.xcpt_pf_if', 'rpq.io.deq.bits.addr', 'rpq.io.deq.bits.data', 'rpq.io.deq.bits.is_hella', 'rpq.io.deq.bits.uop.mem_cmd', 'rpq.io.deq.bits.uop.mem_signed', 'rpq.io.deq.bits.uop.mem_size', 'rpq.io.deq.ready', 'rpq.io.deq.valid', 'rpq.io.empty', 'rpq.io.enq.bits.addr', 'rpq.io.enq.bits.data', 'rpq.io.enq.bits.is_hella', 'rpq.io.enq.bits.old_meta.coh.state', 'rpq.io.enq.bits.old_meta.tag', 'rpq.io.enq.bits.sdq_id', 'rpq.io.enq.bits.tag_match', 'rpq.io.enq.bits.uop.bp_debug_if', 'rpq.io.enq.bits.uop.bp_xcpt_if', 'rpq.io.enq.bits.uop.br_mask', 'rpq.io.enq.bits.uop.br_tag', 'rpq.io.enq.bits.uop.br_type', 'rpq.io.enq.bits.uop.csr_cmd', 'rpq.io.enq.bits.uop.debug_fsrc', 'rpq.io.enq.bits.uop.debug_inst', 'rpq.io.enq.bits.uop.debug_pc', 'rpq.io.enq.bits.uop.debug_tsrc', 'rpq.io.enq.bits.uop.dis_col_sel', 'rpq.io.enq.bits.uop.dst_rtype', 'rpq.io.enq.bits.uop.edge_inst', 'rpq.io.enq.bits.uop.exc_cause', 'rpq.io.enq.bits.uop.exception', 'rpq.io.enq.bits.uop.fcn_dw', 'rpq.io.enq.bits.uop.fcn_op', 'rpq.io.enq.bits.uop.flush_on_commit', 'rpq.io.enq.bits.uop.fp_ctrl.div', 'rpq.io.enq.bits.uop.fp_ctrl.fastpipe', 'rpq.io.enq.bits.uop.fp_ctrl.fma', 'rpq.io.enq.bits.uop.fp_ctrl.fromint', 'rpq.io.enq.bits.uop.fp_ctrl.ldst', 'rpq.io.enq.bits.uop.fp_ctrl.ren1', 'rpq.io.enq.bits.uop.fp_ctrl.ren2', 'rpq.io.enq.bits.uop.fp_ctrl.ren3', 'rpq.io.enq.bits.uop.fp_ctrl.sqrt', 'rpq.io.enq.bits.uop.fp_ctrl.swap12', 'rpq.io.enq.bits.uop.fp_ctrl.swap23', 'rpq.io.enq.bits.uop.fp_ctrl.toint', 'rpq.io.enq.bits.uop.fp_ctrl.typeTagIn', 'rpq.io.enq.bits.uop.fp_ctrl.typeTagOut', 'rpq.io.enq.bits.uop.fp_ctrl.vec', 'rpq.io.enq.bits.uop.fp_ctrl.wen', 'rpq.io.enq.bits.uop.fp_ctrl.wflags', 'rpq.io.enq.bits.uop.fp_rm', 'rpq.io.enq.bits.uop.fp_typ', 'rpq.io.enq.bits.uop.fp_val', 'rpq.io.enq.bits.uop.frs3_en', 'rpq.io.enq.bits.uop.ftq_idx', 'rpq.io.enq.bits.uop.fu_code[0]', 'rpq.io.enq.bits.uop.fu_code[1]', 'rpq.io.enq.bits.uop.fu_code[2]', 'rpq.io.enq.bits.uop.fu_code[3]', 'rpq.io.enq.bits.uop.fu_code[4]', 'rpq.io.enq.bits.uop.fu_code[5]', 'rpq.io.enq.bits.uop.fu_code[6]', 'rpq.io.enq.bits.uop.fu_code[7]', 'rpq.io.enq.bits.uop.fu_code[8]', 'rpq.io.enq.bits.uop.fu_code[9]', 'rpq.io.enq.bits.uop.imm_packed', 'rpq.io.enq.bits.uop.imm_rename', 'rpq.io.enq.bits.uop.imm_sel', 'rpq.io.enq.bits.uop.inst', 'rpq.io.enq.bits.uop.iq_type[0]', 'rpq.io.enq.bits.uop.iq_type[1]', 'rpq.io.enq.bits.uop.iq_type[2]', 'rpq.io.enq.bits.uop.iq_type[3]', 'rpq.io.enq.bits.uop.is_amo', 'rpq.io.enq.bits.uop.is_eret', 'rpq.io.enq.bits.uop.is_fence', 'rpq.io.enq.bits.uop.is_fencei', 'rpq.io.enq.bits.uop.is_mov', 'rpq.io.enq.bits.uop.is_rocc', 'rpq.io.enq.bits.uop.is_rvc', 'rpq.io.enq.bits.uop.is_sfb', 'rpq.io.enq.bits.uop.is_sfence', 'rpq.io.enq.bits.uop.is_sys_pc2epc', 'rpq.io.enq.bits.uop.is_unique', 'rpq.io.enq.bits.uop.iw_issued', 'rpq.io.enq.bits.uop.iw_issued_partial_agen', 'rpq.io.enq.bits.uop.iw_issued_partial_dgen', 'rpq.io.enq.bits.uop.iw_p1_bypass_hint', 'rpq.io.enq.bits.uop.iw_p1_speculative_child', 'rpq.io.enq.bits.uop.iw_p2_bypass_hint', 'rpq.io.enq.bits.uop.iw_p2_speculative_child', 'rpq.io.enq.bits.uop.iw_p3_bypass_hint', 'rpq.io.enq.bits.uop.ldq_idx', 'rpq.io.enq.bits.uop.ldst', 'rpq.io.enq.bits.uop.ldst_is_rs1', 'rpq.io.enq.bits.uop.lrs1', 'rpq.io.enq.bits.uop.lrs1_rtype', 'rpq.io.enq.bits.uop.lrs2', 'rpq.io.enq.bits.uop.lrs2_rtype', 'rpq.io.enq.bits.uop.lrs3', 'rpq.io.enq.bits.uop.mem_cmd', 'rpq.io.enq.bits.uop.mem_signed', 'rpq.io.enq.bits.uop.mem_size', 'rpq.io.enq.bits.uop.op1_sel', 'rpq.io.enq.bits.uop.op2_sel', 'rpq.io.enq.bits.uop.pc_lob', 'rpq.io.enq.bits.uop.pdst', 'rpq.io.enq.bits.uop.pimm', 'rpq.io.enq.bits.uop.ppred', 'rpq.io.enq.bits.uop.ppred_busy', 'rpq.io.enq.bits.uop.prs1', 'rpq.io.enq.bits.uop.prs1_busy', 'rpq.io.enq.bits.uop.prs2', 'rpq.io.enq.bits.uop.prs2_busy', 'rpq.io.enq.bits.uop.prs3', 'rpq.io.enq.bits.uop.prs3_busy', 'rpq.io.enq.bits.uop.rob_idx', 'rpq.io.enq.bits.uop.rxq_idx', 'rpq.io.enq.bits.uop.stale_pdst', 'rpq.io.enq.bits.uop.stq_idx', 'rpq.io.enq.bits.uop.taken', 'rpq.io.enq.bits.uop.uses_ldq', 'rpq.io.enq.bits.uop.uses_stq', 'rpq.io.enq.bits.uop.xcpt_ae_if', 'rpq.io.enq.bits.uop.xcpt_ma_if', 'rpq.io.enq.bits.uop.xcpt_pf_if', 'rpq.io.enq.bits.way_en', 'rpq.io.enq.ready', 'rpq.io.enq.valid', 'rpq.io.flush', 'rpq.reset']

## Frozen child summaries

### Child `BoomMSHR.rpq`
- summary ref: `umcm://BoomMSHR.rpq`
- frozen task: `parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc`
- frozen SHA-256: `aed0cfe9f29f2265257f685ad7af73abb30de23f47bc06a1ec35318e74370e9d`
- exposed boundary events: ['BoomMSHR.rpq::io.deq.fire', 'BoomMSHR.rpq::io.enq.fire']
- frontier signals: ['rpq.clock', 'rpq.io', 'rpq.io.brupdate.b1.mispredict_mask', 'rpq.io.brupdate.b1.resolve_mask', 'rpq.io.brupdate.b2.cfi_type', 'rpq.io.brupdate.b2.jalr_target', 'rpq.io.brupdate.b2.mispredict', 'rpq.io.brupdate.b2.pc_sel', 'rpq.io.brupdate.b2.taken', 'rpq.io.brupdate.b2.target_offset', 'rpq.io.brupdate.b2.uop.bp_debug_if', 'rpq.io.brupdate.b2.uop.bp_xcpt_if', 'rpq.io.brupdate.b2.uop.br_mask', 'rpq.io.brupdate.b2.uop.br_tag', 'rpq.io.brupdate.b2.uop.br_type', 'rpq.io.brupdate.b2.uop.csr_cmd', 'rpq.io.brupdate.b2.uop.debug_fsrc', 'rpq.io.brupdate.b2.uop.debug_inst', 'rpq.io.brupdate.b2.uop.debug_pc', 'rpq.io.brupdate.b2.uop.debug_tsrc', 'rpq.io.brupdate.b2.uop.dis_col_sel', 'rpq.io.brupdate.b2.uop.dst_rtype', 'rpq.io.brupdate.b2.uop.edge_inst', 'rpq.io.brupdate.b2.uop.exc_cause', 'rpq.io.brupdate.b2.uop.exception', 'rpq.io.brupdate.b2.uop.fcn_dw', 'rpq.io.brupdate.b2.uop.fcn_op', 'rpq.io.brupdate.b2.uop.flush_on_commit', 'rpq.io.brupdate.b2.uop.fp_ctrl.div', 'rpq.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'rpq.io.brupdate.b2.uop.fp_ctrl.fma', 'rpq.io.brupdate.b2.uop.fp_ctrl.fromint', 'rpq.io.brupdate.b2.uop.fp_ctrl.ldst', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren1', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren2', 'rpq.io.brupdate.b2.uop.fp_ctrl.ren3', 'rpq.io.brupdate.b2.uop.fp_ctrl.sqrt', 'rpq.io.brupdate.b2.uop.fp_ctrl.swap12', 'rpq.io.brupdate.b2.uop.fp_ctrl.swap23', 'rpq.io.brupdate.b2.uop.fp_ctrl.toint', 'rpq.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'rpq.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'rpq.io.brupdate.b2.uop.fp_ctrl.vec', 'rpq.io.brupdate.b2.uop.fp_ctrl.wen', 'rpq.io.brupdate.b2.uop.fp_ctrl.wflags', 'rpq.io.brupdate.b2.uop.fp_rm', 'rpq.io.brupdate.b2.uop.fp_typ', 'rpq.io.brupdate.b2.uop.fp_val', 'rpq.io.brupdate.b2.uop.frs3_en', 'rpq.io.brupdate.b2.uop.ftq_idx', 'rpq.io.brupdate.b2.uop.fu_code[0]', 'rpq.io.brupdate.b2.uop.fu_code[1]', 'rpq.io.brupdate.b2.uop.fu_code[2]', 'rpq.io.brupdate.b2.uop.fu_code[3]', 'rpq.io.brupdate.b2.uop.fu_code[4]', 'rpq.io.brupdate.b2.uop.fu_code[5]', 'rpq.io.brupdate.b2.uop.fu_code[6]', 'rpq.io.brupdate.b2.uop.fu_code[7]', 'rpq.io.brupdate.b2.uop.fu_code[8]', 'rpq.io.brupdate.b2.uop.fu_code[9]', 'rpq.io.brupdate.b2.uop.imm_packed', 'rpq.io.brupdate.b2.uop.imm_rename', 'rpq.io.brupdate.b2.uop.imm_sel', 'rpq.io.brupdate.b2.uop.inst', 'rpq.io.brupdate.b2.uop.iq_type[0]', 'rpq.io.brupdate.b2.uop.iq_type[1]', 'rpq.io.brupdate.b2.uop.iq_type[2]', 'rpq.io.brupdate.b2.uop.iq_type[3]', 'rpq.io.brupdate.b2.uop.is_amo', 'rpq.io.brupdate.b2.uop.is_eret', 'rpq.io.brupdate.b2.uop.is_fence', 'rpq.io.brupdate.b2.uop.is_fencei', 'rpq.io.brupdate.b2.uop.is_mov', 'rpq.io.brupdate.b2.uop.is_rocc', 'rpq.io.brupdate.b2.uop.is_rvc', 'rpq.io.brupdate.b2.uop.is_sfb', 'rpq.io.brupdate.b2.uop.is_sfence', 'rpq.io.brupdate.b2.uop.is_sys_pc2epc', 'rpq.io.brupdate.b2.uop.is_unique', 'rpq.io.brupdate.b2.uop.iw_issued', 'rpq.io.brupdate.b2.uop.iw_issued_partial_agen', 'rpq.io.brupdate.b2.uop.iw_issued_partial_dgen', 'rpq.io.brupdate.b2.uop.iw_p1_bypass_hint', 'rpq.io.brupdate.b2.uop.iw_p1_speculative_child', 'rpq.io.brupdate.b2.uop.iw_p2_bypass_hint', 'rpq.io.brupdate.b2.uop.iw_p2_speculative_child', 'rpq.io.brupdate.b2.uop.iw_p3_bypass_hint', 'rpq.io.brupdate.b2.uop.ldq_idx', 'rpq.io.brupdate.b2.uop.ldst', 'rpq.io.brupdate.b2.uop.ldst_is_rs1', 'rpq.io.brupdate.b2.uop.lrs1', 'rpq.io.brupdate.b2.uop.lrs1_rtype', 'rpq.io.brupdate.b2.uop.lrs2', 'rpq.io.brupdate.b2.uop.lrs2_rtype', 'rpq.io.brupdate.b2.uop.lrs3', 'rpq.io.brupdate.b2.uop.mem_cmd', 'rpq.io.brupdate.b2.uop.mem_signed', 'rpq.io.brupdate.b2.uop.mem_size', 'rpq.io.brupdate.b2.uop.op1_sel', 'rpq.io.brupdate.b2.uop.op2_sel', 'rpq.io.brupdate.b2.uop.pc_lob', 'rpq.io.brupdate.b2.uop.pdst', 'rpq.io.brupdate.b2.uop.pimm', 'rpq.io.brupdate.b2.uop.ppred', 'rpq.io.brupdate.b2.uop.ppred_busy', 'rpq.io.brupdate.b2.uop.prs1', 'rpq.io.brupdate.b2.uop.prs1_busy', 'rpq.io.brupdate.b2.uop.prs2', 'rpq.io.brupdate.b2.uop.prs2_busy', 'rpq.io.brupdate.b2.uop.prs3', 'rpq.io.brupdate.b2.uop.prs3_busy', 'rpq.io.brupdate.b2.uop.rob_idx', 'rpq.io.brupdate.b2.uop.rxq_idx', 'rpq.io.brupdate.b2.uop.stale_pdst', 'rpq.io.brupdate.b2.uop.stq_idx', 'rpq.io.brupdate.b2.uop.taken', 'rpq.io.brupdate.b2.uop.uses_ldq', 'rpq.io.brupdate.b2.uop.uses_stq', 'rpq.io.brupdate.b2.uop.xcpt_ae_if', 'rpq.io.brupdate.b2.uop.xcpt_ma_if', 'rpq.io.brupdate.b2.uop.xcpt_pf_if', 'rpq.io.count', 'rpq.io.deq.bits.addr', 'rpq.io.deq.bits.data', 'rpq.io.deq.bits.is_hella', 'rpq.io.deq.bits.old_meta.coh.state', 'rpq.io.deq.bits.old_meta.tag', 'rpq.io.deq.bits.sdq_id', 'rpq.io.deq.bits.tag_match', 'rpq.io.deq.bits.uop.bp_debug_if', 'rpq.io.deq.bits.uop.bp_xcpt_if', 'rpq.io.deq.bits.uop.br_mask', 'rpq.io.deq.bits.uop.br_tag', 'rpq.io.deq.bits.uop.br_type', 'rpq.io.deq.bits.uop.csr_cmd', 'rpq.io.deq.bits.uop.debug_fsrc', 'rpq.io.deq.bits.uop.debug_inst', 'rpq.io.deq.bits.uop.debug_pc', 'rpq.io.deq.bits.uop.debug_tsrc', 'rpq.io.deq.bits.uop.dis_col_sel', 'rpq.io.deq.bits.uop.dst_rtype', 'rpq.io.deq.bits.uop.edge_inst', 'rpq.io.deq.bits.uop.exc_cause', 'rpq.io.deq.bits.uop.exception', 'rpq.io.deq.bits.uop.fcn_dw', 'rpq.io.deq.bits.uop.fcn_op', 'rpq.io.deq.bits.uop.flush_on_commit', 'rpq.io.deq.bits.uop.fp_ctrl.div', 'rpq.io.deq.bits.uop.fp_ctrl.fastpipe', 'rpq.io.deq.bits.uop.fp_ctrl.fma', 'rpq.io.deq.bits.uop.fp_ctrl.fromint', 'rpq.io.deq.bits.uop.fp_ctrl.ldst', 'rpq.io.deq.bits.uop.fp_ctrl.ren1', 'rpq.io.deq.bits.uop.fp_ctrl.ren2', 'rpq.io.deq.bits.uop.fp_ctrl.ren3', 'rpq.io.deq.bits.uop.fp_ctrl.sqrt', 'rpq.io.deq.bits.uop.fp_ctrl.swap12', 'rpq.io.deq.bits.uop.fp_ctrl.swap23', 'rpq.io.deq.bits.uop.fp_ctrl.toint', 'rpq.io.deq.bits.uop.fp_ctrl.typeTagIn', 'rpq.io.deq.bits.uop.fp_ctrl.typeTagOut', 'rpq.io.deq.bits.uop.fp_ctrl.vec', 'rpq.io.deq.bits.uop.fp_ctrl.wen', 'rpq.io.deq.bits.uop.fp_ctrl.wflags', 'rpq.io.deq.bits.uop.fp_rm', 'rpq.io.deq.bits.uop.fp_typ', 'rpq.io.deq.bits.uop.fp_val', 'rpq.io.deq.bits.uop.frs3_en', 'rpq.io.deq.bits.uop.ftq_idx', 'rpq.io.deq.bits.uop.fu_code[0]', 'rpq.io.deq.bits.uop.fu_code[1]', 'rpq.io.deq.bits.uop.fu_code[2]', 'rpq.io.deq.bits.uop.fu_code[3]', 'rpq.io.deq.bits.uop.fu_code[4]', 'rpq.io.deq.bits.uop.fu_code[5]', 'rpq.io.deq.bits.uop.fu_code[6]', 'rpq.io.deq.bits.uop.fu_code[7]', 'rpq.io.deq.bits.uop.fu_code[8]', 'rpq.io.deq.bits.uop.fu_code[9]', 'rpq.io.deq.bits.uop.imm_packed', 'rpq.io.deq.bits.uop.imm_rename', 'rpq.io.deq.bits.uop.imm_sel', 'rpq.io.deq.bits.uop.inst', 'rpq.io.deq.bits.uop.iq_type[0]', 'rpq.io.deq.bits.uop.iq_type[1]', 'rpq.io.deq.bits.uop.iq_type[2]', 'rpq.io.deq.bits.uop.iq_type[3]', 'rpq.io.deq.bits.uop.is_amo', 'rpq.io.deq.bits.uop.is_eret', 'rpq.io.deq.bits.uop.is_fence', 'rpq.io.deq.bits.uop.is_fencei', 'rpq.io.deq.bits.uop.is_mov', 'rpq.io.deq.bits.uop.is_rocc', 'rpq.io.deq.bits.uop.is_rvc', 'rpq.io.deq.bits.uop.is_sfb', 'rpq.io.deq.bits.uop.is_sfence', 'rpq.io.deq.bits.uop.is_sys_pc2epc', 'rpq.io.deq.bits.uop.is_unique', 'rpq.io.deq.bits.uop.iw_issued', 'rpq.io.deq.bits.uop.iw_issued_partial_agen', 'rpq.io.deq.bits.uop.iw_issued_partial_dgen', 'rpq.io.deq.bits.uop.iw_p1_bypass_hint', 'rpq.io.deq.bits.uop.iw_p1_speculative_child', 'rpq.io.deq.bits.uop.iw_p2_bypass_hint', 'rpq.io.deq.bits.uop.iw_p2_speculative_child', 'rpq.io.deq.bits.uop.iw_p3_bypass_hint', 'rpq.io.deq.bits.uop.ldq_idx', 'rpq.io.deq.bits.uop.ldst', 'rpq.io.deq.bits.uop.ldst_is_rs1', 'rpq.io.deq.bits.uop.lrs1', 'rpq.io.deq.bits.uop.lrs1_rtype', 'rpq.io.deq.bits.uop.lrs2', 'rpq.io.deq.bits.uop.lrs2_rtype', 'rpq.io.deq.bits.uop.lrs3', 'rpq.io.deq.bits.uop.mem_cmd', 'rpq.io.deq.bits.uop.mem_signed', 'rpq.io.deq.bits.uop.mem_size', 'rpq.io.deq.bits.uop.op1_sel', 'rpq.io.deq.bits.uop.op2_sel', 'rpq.io.deq.bits.uop.pc_lob', 'rpq.io.deq.bits.uop.pdst', 'rpq.io.deq.bits.uop.pimm', 'rpq.io.deq.bits.uop.ppred', 'rpq.io.deq.bits.uop.ppred_busy', 'rpq.io.deq.bits.uop.prs1', 'rpq.io.deq.bits.uop.prs1_busy', 'rpq.io.deq.bits.uop.prs2', 'rpq.io.deq.bits.uop.prs2_busy', 'rpq.io.deq.bits.uop.prs3', 'rpq.io.deq.bits.uop.prs3_busy', 'rpq.io.deq.bits.uop.rob_idx', 'rpq.io.deq.bits.uop.rxq_idx', 'rpq.io.deq.bits.uop.stale_pdst', 'rpq.io.deq.bits.uop.stq_idx', 'rpq.io.deq.bits.uop.taken', 'rpq.io.deq.bits.uop.uses_ldq', 'rpq.io.deq.bits.uop.uses_stq', 'rpq.io.deq.bits.uop.xcpt_ae_if', 'rpq.io.deq.bits.uop.xcpt_ma_if', 'rpq.io.deq.bits.uop.xcpt_pf_if', 'rpq.io.deq.bits.way_en', 'rpq.io.deq.ready', 'rpq.io.deq.valid', 'rpq.io.empty', 'rpq.io.enq.bits.addr', 'rpq.io.enq.bits.data', 'rpq.io.enq.bits.is_hella', 'rpq.io.enq.bits.old_meta.coh.state', 'rpq.io.enq.bits.old_meta.tag', 'rpq.io.enq.bits.sdq_id', 'rpq.io.enq.bits.tag_match', 'rpq.io.enq.bits.uop.bp_debug_if', 'rpq.io.enq.bits.uop.bp_xcpt_if', 'rpq.io.enq.bits.uop.br_mask', 'rpq.io.enq.bits.uop.br_tag', 'rpq.io.enq.bits.uop.br_type', 'rpq.io.enq.bits.uop.csr_cmd', 'rpq.io.enq.bits.uop.debug_fsrc', 'rpq.io.enq.bits.uop.debug_inst', 'rpq.io.enq.bits.uop.debug_pc', 'rpq.io.enq.bits.uop.debug_tsrc', 'rpq.io.enq.bits.uop.dis_col_sel', 'rpq.io.enq.bits.uop.dst_rtype', 'rpq.io.enq.bits.uop.edge_inst', 'rpq.io.enq.bits.uop.exc_cause', 'rpq.io.enq.bits.uop.exception', 'rpq.io.enq.bits.uop.fcn_dw', 'rpq.io.enq.bits.uop.fcn_op', 'rpq.io.enq.bits.uop.flush_on_commit', 'rpq.io.enq.bits.uop.fp_ctrl.div', 'rpq.io.enq.bits.uop.fp_ctrl.fastpipe', 'rpq.io.enq.bits.uop.fp_ctrl.fma', 'rpq.io.enq.bits.uop.fp_ctrl.fromint', 'rpq.io.enq.bits.uop.fp_ctrl.ldst', 'rpq.io.enq.bits.uop.fp_ctrl.ren1', 'rpq.io.enq.bits.uop.fp_ctrl.ren2', 'rpq.io.enq.bits.uop.fp_ctrl.ren3', 'rpq.io.enq.bits.uop.fp_ctrl.sqrt', 'rpq.io.enq.bits.uop.fp_ctrl.swap12', 'rpq.io.enq.bits.uop.fp_ctrl.swap23', 'rpq.io.enq.bits.uop.fp_ctrl.toint', 'rpq.io.enq.bits.uop.fp_ctrl.typeTagIn', 'rpq.io.enq.bits.uop.fp_ctrl.typeTagOut', 'rpq.io.enq.bits.uop.fp_ctrl.vec', 'rpq.io.enq.bits.uop.fp_ctrl.wen', 'rpq.io.enq.bits.uop.fp_ctrl.wflags', 'rpq.io.enq.bits.uop.fp_rm', 'rpq.io.enq.bits.uop.fp_typ', 'rpq.io.enq.bits.uop.fp_val', 'rpq.io.enq.bits.uop.frs3_en', 'rpq.io.enq.bits.uop.ftq_idx', 'rpq.io.enq.bits.uop.fu_code[0]', 'rpq.io.enq.bits.uop.fu_code[1]', 'rpq.io.enq.bits.uop.fu_code[2]', 'rpq.io.enq.bits.uop.fu_code[3]', 'rpq.io.enq.bits.uop.fu_code[4]', 'rpq.io.enq.bits.uop.fu_code[5]', 'rpq.io.enq.bits.uop.fu_code[6]', 'rpq.io.enq.bits.uop.fu_code[7]', 'rpq.io.enq.bits.uop.fu_code[8]', 'rpq.io.enq.bits.uop.fu_code[9]', 'rpq.io.enq.bits.uop.imm_packed', 'rpq.io.enq.bits.uop.imm_rename', 'rpq.io.enq.bits.uop.imm_sel', 'rpq.io.enq.bits.uop.inst', 'rpq.io.enq.bits.uop.iq_type[0]', 'rpq.io.enq.bits.uop.iq_type[1]', 'rpq.io.enq.bits.uop.iq_type[2]', 'rpq.io.enq.bits.uop.iq_type[3]', 'rpq.io.enq.bits.uop.is_amo', 'rpq.io.enq.bits.uop.is_eret', 'rpq.io.enq.bits.uop.is_fence', 'rpq.io.enq.bits.uop.is_fencei', 'rpq.io.enq.bits.uop.is_mov', 'rpq.io.enq.bits.uop.is_rocc', 'rpq.io.enq.bits.uop.is_rvc', 'rpq.io.enq.bits.uop.is_sfb', 'rpq.io.enq.bits.uop.is_sfence', 'rpq.io.enq.bits.uop.is_sys_pc2epc', 'rpq.io.enq.bits.uop.is_unique', 'rpq.io.enq.bits.uop.iw_issued', 'rpq.io.enq.bits.uop.iw_issued_partial_agen', 'rpq.io.enq.bits.uop.iw_issued_partial_dgen', 'rpq.io.enq.bits.uop.iw_p1_bypass_hint', 'rpq.io.enq.bits.uop.iw_p1_speculative_child', 'rpq.io.enq.bits.uop.iw_p2_bypass_hint', 'rpq.io.enq.bits.uop.iw_p2_speculative_child', 'rpq.io.enq.bits.uop.iw_p3_bypass_hint', 'rpq.io.enq.bits.uop.ldq_idx', 'rpq.io.enq.bits.uop.ldst', 'rpq.io.enq.bits.uop.ldst_is_rs1', 'rpq.io.enq.bits.uop.lrs1', 'rpq.io.enq.bits.uop.lrs1_rtype', 'rpq.io.enq.bits.uop.lrs2', 'rpq.io.enq.bits.uop.lrs2_rtype', 'rpq.io.enq.bits.uop.lrs3', 'rpq.io.enq.bits.uop.mem_cmd', 'rpq.io.enq.bits.uop.mem_signed', 'rpq.io.enq.bits.uop.mem_size', 'rpq.io.enq.bits.uop.op1_sel', 'rpq.io.enq.bits.uop.op2_sel', 'rpq.io.enq.bits.uop.pc_lob', 'rpq.io.enq.bits.uop.pdst', 'rpq.io.enq.bits.uop.pimm', 'rpq.io.enq.bits.uop.ppred', 'rpq.io.enq.bits.uop.ppred_busy', 'rpq.io.enq.bits.uop.prs1', 'rpq.io.enq.bits.uop.prs1_busy', 'rpq.io.enq.bits.uop.prs2', 'rpq.io.enq.bits.uop.prs2_busy', 'rpq.io.enq.bits.uop.prs3', 'rpq.io.enq.bits.uop.prs3_busy', 'rpq.io.enq.bits.uop.rob_idx', 'rpq.io.enq.bits.uop.rxq_idx', 'rpq.io.enq.bits.uop.stale_pdst', 'rpq.io.enq.bits.uop.stq_idx', 'rpq.io.enq.bits.uop.taken', 'rpq.io.enq.bits.uop.uses_ldq', 'rpq.io.enq.bits.uop.uses_stq', 'rpq.io.enq.bits.uop.xcpt_ae_if', 'rpq.io.enq.bits.uop.xcpt_ma_if', 'rpq.io.enq.bits.uop.xcpt_pf_if', 'rpq.io.enq.bits.way_en', 'rpq.io.enq.ready', 'rpq.io.enq.valid', 'rpq.io.flush', 'rpq.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHR.rpq.main::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHR.rpq"
    }
  },
  "cases": {
    "BoomMSHR.rpq.main::C1_Admitted": {
      "local_id": "C1_Admitted",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::C2_BranchKilledOnArrival": {
      "local_id": "C2_BranchKilledOnArrival",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::C3_FlushKilledOnArrival": {
      "local_id": "C3_FlushKilledOnArrival",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::C4_VisibleDequeue": {
      "local_id": "C4_VisibleDequeue",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::C5_InvalidHeadSkip": {
      "local_id": "C5_InvalidHeadSkip",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq::C1_EnqueueForwarded": {
      "local_id": "C1_EnqueueForwarded",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::C2_ChildDequeueCaptured": {
      "local_id": "C2_ChildDequeueCaptured",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::C3_ChildDequeueBranchKilled": {
      "local_id": "C3_ChildDequeueBranchKilled",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::C4_ChildDequeueFlushKilled": {
      "local_id": "C4_ChildDequeueFlushKilled",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::C5_VisibleParentDequeue": {
      "local_id": "C5_VisibleParentDequeue",
      "work_unit_id": "BoomMSHR.rpq"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHR.rpq.main::DeqHandshake": {
      "local_id": "DeqHandshake",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::EnqHandshake": {
      "local_id": "EnqHandshake",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::InvalidHeadSkip": {
      "local_id": "InvalidHeadSkip",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::QueueInsert": {
      "local_id": "QueueInsert",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq::BufferCapture": {
      "local_id": "BufferCapture",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::ParentDeqHandshake": {
      "local_id": "ParentDeqHandshake",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::ParentEnqHandshake": {
      "local_id": "ParentEnqHandshake",
      "work_unit_id": "BoomMSHR.rpq"
    }
  },
  "predicates": {
    "BoomMSHR.rpq.main::HeadInvalid": {
      "local_id": "HeadInvalid",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::HeadValid": {
      "local_id": "HeadValid",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::IncomingBranchKilled": {
      "local_id": "IncomingBranchKilled",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::IncomingFlushKilled": {
      "local_id": "IncomingFlushKilled",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::QueueEmpty": {
      "local_id": "QueueEmpty",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq.main::QueueFull": {
      "local_id": "QueueFull",
      "work_unit_id": "BoomMSHR.rpq.main"
    },
    "BoomMSHR.rpq::OutputInvalid": {
      "local_id": "OutputInvalid",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::TransferBranchKilled": {
      "local_id": "TransferBranchKilled",
      "work_unit_id": "BoomMSHR.rpq"
    },
    "BoomMSHR.rpq::TransferFlushKilled": {
      "local_id": "TransferFlushKilled",
      "work_unit_id": "BoomMSHR.rpq"
    }
  }
}
```

Trusted frozen child µMCM:
```json
{
  "assumptions": [],
  "axioms": [
    {
      "derived_from_case_ids": [
        "C1_EnqueueForwarded"
      ],
      "evidence_statement_ids": [
        9
      ],
      "formal": {
        "occurrence": "ParentEnqHandshake",
        "predicate": "BoomMSHR.rpq.main::QueueFull",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A1",
      "rendered_formula": "BoomMSHR.rpq.main::QueueFull => !ParentEnqHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        155
      ],
      "formal": {
        "occurrence": "ParentDeqHandshake",
        "predicate": "OutputInvalid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "OutputInvalid => !ParentDeqHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        153,
        157,
        158,
        167,
        175
      ],
      "formal": {
        "after": "ParentDeqHandshake",
        "before": "BufferCapture",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A3",
      "rendered_formula": "BufferCapture <mu ParentDeqHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        154,
        155,
        157,
        158,
        167,
        175
      ],
      "formal": {
        "after": "ParentDeqHandshake",
        "before": "BoomMSHR.rpq.main::DeqHandshake",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A4",
      "rendered_formula": "BoomMSHR.rpq.main::DeqHandshake <mu ParentDeqHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C5_VisibleParentDequeue"
      ],
      "evidence_statement_ids": [
        7,
        136,
        154,
        155,
        157,
        158,
        167,
        175
      ],
      "formal": {
        "after": "ParentDeqHandshake",
        "before": "BoomMSHR.rpq.main::QueueInsert",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A5",
      "rendered_formula": "BoomMSHR.rpq.main::QueueInsert <mu ParentDeqHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C3_ChildDequeueBranchKilled"
      ],
      "evidence_statement_ids": [
        159,
        160,
        161,
        162,
        163,
        166,
        167
      ],
      "formal": {
        "occurrence": "BufferCapture",
        "predicate": "TransferBranchKilled",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A6",
      "rendered_formula": "TransferBranchKilled => !BufferCapture",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ChildDequeueCaptured",
        "C4_ChildDequeueFlushKilled"
      ],
      "evidence_statement_ids": [
        163,
        164,
        165,
        166,
        167
      ],
      "formal": {
        "occurrence": "BufferCapture",
        "predicate": "TransferFlushKilled",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A7",
      "rendered_formula": "TransferFlushKilled => !BufferCapture",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "BoomMSHR.rpq.main::EnqHandshake"
      ],
      "evidence_statement_ids": [
        9
      ],
      "guard_predicates": [],
      "id": "C1_EnqueueForwarded",
      "relations": [
        "The parent enqueue interface is directly connected to the frozen child enqueue interface, so the parent handshake is the same forwarded enqueue transaction observed by the child."
      ],
      "trigger_occurrences": [
        "ParentEnqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "BufferCapture"
      ],
      "evidence_statement_ids": [
        154,
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        170,
        171,
        172,
        173,
        174,
        175
      ],
      "guard_predicates": [
        {
          "id": "TransferBranchKilled",
          "positive": false
        },
        {
          "id": "TransferFlushKilled",
          "positive": false
        }
      ],
      "id": "C2_ChildDequeueCaptured",
      "relations": [
        "A child dequeue accepted during the refill window becomes a valid buffered parent-visible item when it survives the parent-local branch and flush filters."
      ],
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        158,
        159,
        160,
        161,
        162,
        163,
        167,
        175
      ],
      "guard_predicates": [
        {
          "id": "TransferBranchKilled",
          "positive": true
        }
      ],
      "id": "C3_ChildDequeueBranchKilled",
      "relations": [
        "A child dequeue may be consumed by the wrapper without becoming a valid buffered output when its uop is killed by the current branch update."
      ],
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        158,
        163,
        164,
        165,
        166,
        167,
        175
      ],
      "guard_predicates": [
        {
          "id": "TransferFlushKilled",
          "positive": true
        }
      ],
      "id": "C4_ChildDequeueFlushKilled",
      "relations": [
        "A child dequeue may be consumed by the wrapper without becoming a valid buffered output when flush kills the dequeued uses_ldq uop."
      ],
      "trigger_occurrences": [
        "BoomMSHR.rpq.main::DeqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        7,
        136,
        155
      ],
      "guard_predicates": [
        {
          "id": "OutputInvalid",
          "positive": false
        }
      ],
      "id": "C5_VisibleParentDequeue",
      "relations": [
        "A parent-visible dequeue consumes a previously valid output-buffer entry; reset initializes the output buffer invalid."
      ],
      "trigger_occurrences": [
        "ParentDeqHandshake"
      ]
    }
  ],
  "composition": {
    "imports": [
      {
        "child_id": "BoomMSHR.rpq.main",
        "child_kind": "module",
        "frozen_umcm": {
          "assumptions": [],
          "axioms": [
            {
              "derived_from_case_ids": [],
              "evidence_statement_ids": [
                29,
                30,
                267,
                268
              ],
              "formal": {
                "occurrence": "EnqHandshake",
                "predicate": "QueueFull",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A1",
              "rendered_formula": "QueueFull => !EnqHandshake",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C1_Admitted",
                "C2_BranchKilledOnArrival"
              ],
              "evidence_statement_ids": [
                30,
                31,
                32,
                34,
                35,
                39,
                40,
                242
              ],
              "formal": {
                "occurrence": "QueueInsert",
                "predicate": "IncomingBranchKilled",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A2",
              "rendered_formula": "IncomingBranchKilled => !QueueInsert",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C1_Admitted",
                "C3_FlushKilledOnArrival"
              ],
              "evidence_statement_ids": [
                30,
                35,
                36,
                37,
                38,
                39,
                40,
                242
              ],
              "formal": {
                "occurrence": "QueueInsert",
                "predicate": "IncomingFlushKilled",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A3",
              "rendered_formula": "IncomingFlushKilled => !QueueInsert",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C4_VisibleDequeue"
              ],
              "evidence_statement_ids": [
                28,
                43,
                44,
                273,
                274,
                275
              ],
              "formal": {
                "occurrence": "DeqHandshake",
                "predicate": "QueueEmpty",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A4",
              "rendered_formula": "QueueEmpty => !DeqHandshake",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C4_VisibleDequeue"
              ],
              "evidence_statement_ids": [
                41,
                273,
                274,
                275
              ],
              "formal": {
                "occurrence": "DeqHandshake",
                "predicate": "HeadInvalid",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A5",
              "rendered_formula": "HeadInvalid => !DeqHandshake",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C5_InvalidHeadSkip"
              ],
              "evidence_statement_ids": [
                28,
                41,
                42,
                43,
                44,
                45,
                46
              ],
              "formal": {
                "occurrence": "InvalidHeadSkip",
                "predicate": "QueueEmpty",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A6",
              "rendered_formula": "QueueEmpty => !InvalidHeadSkip",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C5_InvalidHeadSkip"
              ],
              "evidence_statement_ids": [
                41,
                42,
                43,
                44,
                45,
                46,
                273,
                274,
                275
              ],
              "formal": {
                "occurrence": "InvalidHeadSkip",
                "predicate": "HeadValid",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A7",
              "rendered_formula": "HeadValid => !InvalidHeadSkip",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C1_Admitted"
              ],
              "evidence_statement_ids": [
                242,
                243,
                244
              ],
              "formal": {
                "on": "QueueInsert",
                "scope_identity": null,
                "source": {
                  "name": "io.enq.bits",
                  "op": "signal"
                },
                "target": "MPORT",
                "type": "signal_equality"
              },
              "id": "A8",
              "rendered_formula": "MPORT = io.enq.bits on QueueInsert",
              "status": "candidate"
            },
            {
              "derived_from_case_ids": [
                "C1_Admitted",
                "C4_VisibleDequeue"
              ],
              "evidence_statement_ids": [
                20,
                22,
                23,
                242,
                245,
                250,
                251,
                252,
                253,
                254,
                255,
                257,
                258,
                259,
                260,
                261,
                262,
                263,
                273,
                274,
                275
              ],
              "formal": {
                "after": "DeqHandshake",
                "before": "QueueInsert",
                "required_prior": null,
                "scope_identity": null,
                "scope_index": {
                  "name": "slot",
                  "relation": "same"
                },
                "type": "ordered_before"
              },
              "id": "A11",
              "rendered_formula": "QueueInsert <mu DeqHandshake [same index slot]",
              "status": "candidate"
            }
          ],
          "cases": [
            {
              "confidence": "high",
              "emits": [
                "QueueInsert"
              ],
              "evidence_statement_ids": [
                30,
                31,
                32,
                34,
                35,
                36,
                37,
                38,
                40,
                242,
                243,
                244,
                245,
                246,
                249,
                250,
                251,
                252,
                253,
                254,
                255
              ],
              "guard_predicates": [
                {
                  "id": "IncomingBranchKilled",
                  "positive": false
                },
                {
                  "id": "IncomingFlushKilled",
                  "positive": false
                }
              ],
              "id": "C1_Admitted",
              "relations": [
                "A handshaken request that is not killed on arrival is written into the current enqueue slot and advances enq_ptr."
              ],
              "trigger_occurrences": [
                "EnqHandshake"
              ]
            },
            {
              "confidence": "high",
              "emits": [],
              "evidence_statement_ids": [
                30,
                31,
                32,
                34,
                35,
                39,
                40
              ],
              "guard_predicates": [
                {
                  "id": "IncomingBranchKilled",
                  "positive": true
                }
              ],
              "id": "C2_BranchKilledOnArrival",
              "relations": [
                "The boundary handshake does not become a QueueInsert when the incoming uop is killed by the current branch mispredict mask."
              ],
              "trigger_occurrences": [
                "EnqHandshake"
              ]
            },
            {
              "confidence": "high",
              "emits": [],
              "evidence_statement_ids": [
                30,
                35,
                36,
                37,
                38,
                39,
                40
              ],
              "guard_predicates": [
                {
                  "id": "IncomingFlushKilled",
                  "positive": true
                }
              ],
              "id": "C3_FlushKilledOnArrival",
              "relations": [
                "The boundary handshake does not become a QueueInsert when flush kills this uses_ldq request."
              ],
              "trigger_occurrences": [
                "EnqHandshake"
              ]
            },
            {
              "confidence": "high",
              "emits": [],
              "evidence_statement_ids": [
                41,
                43,
                44,
                273,
                274,
                275,
                276
              ],
              "guard_predicates": [
                {
                  "id": "QueueEmpty",
                  "positive": false
                },
                {
                  "id": "HeadInvalid",
                  "positive": false
                }
              ],
              "id": "C4_VisibleDequeue",
              "relations": [
                "A visible dequeue can occur only from a non-empty valid head slot."
              ],
              "trigger_occurrences": [
                "DeqHandshake"
              ]
            },
            {
              "confidence": "high",
              "emits": [],
              "evidence_statement_ids": [
                41,
                42,
                43,
                44,
                45,
                46,
                256,
                257,
                258,
                259,
                260,
                261,
                262,
                263,
                273,
                274,
                275
              ],
              "guard_predicates": [
                {
                  "id": "QueueEmpty",
                  "positive": false
                },
                {
                  "id": "HeadInvalid",
                  "positive": true
                }
              ],
              "id": "C5_InvalidHeadSkip",
              "relations": [
                "An invalid hole at the current non-empty head is consumed internally by advancing deq_ptr without io.deq.fire."
              ],
              "trigger_occurrences": [
                "InvalidHeadSkip"
              ]
            }
          ],
          "freeze": {
            "candidate_axiom_count": 9,
            "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
            "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
            "status": "FROZEN_FOR_COMPOSITION",
            "trusted_axiom_count": 9
          },
          "identity_keys": [],
          "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
          "occurrences": [
            {
              "definition": "io.enq.valid && io.enq.ready",
              "evidence_statement_ids": [
                30,
                267,
                268
              ],
              "grounding": {
                "signals_false": [],
                "signals_true": [
                  "io.enq.valid",
                  "io.enq.ready"
                ],
                "state_register": null,
                "state_values": []
              },
              "id": "EnqHandshake",
              "index": null,
              "kind": "boundary",
              "multiplicity": "repeatable",
              "physical_event_ids": [
                "BoomMSHR.rpq.main::io.enq.fire"
              ]
            },
            {
              "definition": "do_enq; equivalently io.enq.fire && !incoming_branch_killed && !incoming_flush_killed",
              "evidence_statement_ids": [
                30,
                31,
                32,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                242,
                243,
                244,
                245,
                246,
                247,
                248,
                249,
                250,
                251,
                252,
                253,
                254,
                255
              ],
              "grounding": {
                "signals_false": [],
                "signals_true": [
                  "do_enq"
                ],
                "state_register": null,
                "state_values": []
              },
              "id": "QueueInsert",
              "index": {
                "domain": {
                  "end_exclusive": 15,
                  "start": 0
                },
                "expr": {
                  "name": "enq_ptr_value",
                  "op": "signal"
                },
                "name": "slot"
              },
              "kind": "derived",
              "multiplicity": "repeatable",
              "physical_event_ids": []
            },
            {
              "definition": "io.deq.valid && io.deq.ready",
              "evidence_statement_ids": [
                41,
                42,
                43,
                44,
                45,
                46,
                256,
                257,
                258,
                259,
                260,
                261,
                262,
                263,
                273,
                274,
                275,
                276
              ],
              "grounding": {
                "signals_false": [],
                "signals_true": [
                  "io.deq.valid",
                  "io.deq.ready"
                ],
                "state_register": null,
                "state_values": []
              },
              "id": "DeqHandshake",
              "index": {
                "domain": {
                  "end_exclusive": 15,
                  "start": 0
                },
                "expr": {
                  "name": "deq_ptr_value",
                  "op": "signal"
                },
                "name": "slot"
              },
              "kind": "boundary",
              "multiplicity": "repeatable",
              "physical_event_ids": [
                "BoomMSHR.rpq.main::io.deq.fire"
              ]
            },
            {
              "definition": "do_deq && !io.deq.valid; equivalently the queue is non-empty and valids[deq_ptr_value] is false, causing deq_ptr to advance without a dequeue handshake",
              "evidence_statement_ids": [
                41,
                42,
                43,
                44,
                45,
                46,
                256,
                257,
                258,
                259,
                260,
                261,
                262,
                263,
                273,
                274,
                275
              ],
              "grounding": {
                "signals_false": [
                  "io.deq.valid"
                ],
                "signals_true": [
                  "do_deq"
                ],
                "state_register": null,
                "state_values": []
              },
              "id": "InvalidHeadSkip",
              "index": {
                "domain": {
                  "end_exclusive": 15,
                  "start": 0
                },
                "expr": {
                  "name": "deq_ptr_value",
                  "op": "signal"
                },
                "name": "slot"
              },
              "kind": "derived",
              "multiplicity": "repeatable",
              "physical_event_ids": []
            }
          ],
          "predicates": [
            {
              "definition": "enq_ptr_value == deq_ptr_value && !maybe_full",
              "evidence_statement_ids": [
                25,
                26,
                27,
                28
              ],
              "grounding": {
                "negated": false,
                "source_signal": "io.empty",
                "state_register": null,
                "state_values": []
              },
              "id": "QueueEmpty"
            },
            {
              "definition": "enq_ptr_value == deq_ptr_value && maybe_full",
              "evidence_statement_ids": [
                25,
                29,
                267,
                268
              ],
              "grounding": {
                "negated": false,
                "source_signal": "full",
                "state_register": null,
                "state_values": []
              },
              "id": "QueueFull"
            },
            {
              "definition": "(io.brupdate.b1.mispredict_mask & io.enq.bits.uop.br_mask) != 0",
              "evidence_statement_ids": [
                31,
                32
              ],
              "grounding": {
                "negated": false,
                "source_signal": "_do_enq_T_2",
                "state_register": null,
                "state_values": []
              },
              "id": "IncomingBranchKilled"
            },
            {
              "definition": "io.flush && io.enq.bits.uop.uses_ldq",
              "evidence_statement_ids": [
                36
              ],
              "grounding": {
                "negated": false,
                "source_signal": "_do_enq_T_6",
                "state_register": null,
                "state_values": []
              },
              "id": "IncomingFlushKilled"
            },
            {
              "definition": "valids[deq_ptr_value] == 0",
              "evidence_statement_ids": [
                41
              ],
              "grounding": {
                "negated": false,
                "source_signal": "_do_deq_T",
                "state_register": null,
                "state_values": []
              },
              "id": "HeadInvalid"
            },
            {
              "definition": "valids[deq_ptr_value] != 0",
              "evidence_statement_ids": [
                41
              ],
              "grounding": {
                "negated": true,
                "source_signal": "_do_deq_T",
                "state_register": null,
                "state_values": []
              },
              "id": "HeadValid"
            }
          ],
          "schema_version": "umcm-formal-0.5",
          "task_id": "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8",
          "trust_policy": "formal-ast-only-v0.2",
          "trusted_axiom_ids": [
            "A1",
            "A11",
            "A2",
            "A3",
            "A4",
            "A5",
            "A6",
            "A7",
            "A8"
          ],
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "frozen_umcm_sha256": "d79c2389d52d6e60f76113d837d619dc94e00e7184c466434d6697cfad97dad8",
        "semantic_catalog": {
          "axioms": {
            "BoomMSHR.rpq.main::A1": {
              "local_id": "A1",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A11": {
              "local_id": "A11",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A2": {
              "local_id": "A2",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A3": {
              "local_id": "A3",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A4": {
              "local_id": "A4",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A5": {
              "local_id": "A5",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A6": {
              "local_id": "A6",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A7": {
              "local_id": "A7",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::A8": {
              "local_id": "A8",
              "work_unit_id": "BoomMSHR.rpq.main"
            }
          },
          "cases": {
            "BoomMSHR.rpq.main::C1_Admitted": {
              "local_id": "C1_Admitted",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::C2_BranchKilledOnArrival": {
              "local_id": "C2_BranchKilledOnArrival",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::C3_FlushKilledOnArrival": {
              "local_id": "C3_FlushKilledOnArrival",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::C4_VisibleDequeue": {
              "local_id": "C4_VisibleDequeue",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::C5_InvalidHeadSkip": {
              "local_id": "C5_InvalidHeadSkip",
              "work_unit_id": "BoomMSHR.rpq.main"
            }
          },
          "identity_keys": {},
          "occurrences": {
            "BoomMSHR.rpq.main::DeqHandshake": {
              "local_id": "DeqHandshake",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::EnqHandshake": {
              "local_id": "EnqHandshake",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::InvalidHeadSkip": {
              "local_id": "InvalidHeadSkip",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::QueueInsert": {
              "local_id": "QueueInsert",
              "work_unit_id": "BoomMSHR.rpq.main"
            }
          },
          "predicates": {
            "BoomMSHR.rpq.main::HeadInvalid": {
              "local_id": "HeadInvalid",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::HeadValid": {
              "local_id": "HeadValid",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::IncomingBranchKilled": {
              "local_id": "IncomingBranchKilled",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::IncomingFlushKilled": {
              "local_id": "IncomingFlushKilled",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::QueueEmpty": {
              "local_id": "QueueEmpty",
              "work_unit_id": "BoomMSHR.rpq.main"
            },
            "BoomMSHR.rpq.main::QueueFull": {
              "local_id": "QueueFull",
              "work_unit_id": "BoomMSHR.rpq.main"
            }
          }
        },
        "summary_ref": "umcm://BoomMSHR.rpq.main",
        "task_id": "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8"
      }
    ],
    "mode": "parent_synthesis",
    "note": "Child RTL is not part of this frozen parent. Imported child \u00b5MCMs remain frozen semantic components; descendant semantic names are transparently propagated in v0.1 for higher-level synthesis.",
    "policy": "transparent-frozen-child-imports-v0.1",
    "semantic_catalog": {
      "axioms": {
        "BoomMSHR.rpq.main::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A11": {
          "local_id": "A11",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::A8": {
          "local_id": "A8",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHR.rpq"
        }
      },
      "cases": {
        "BoomMSHR.rpq.main::C1_Admitted": {
          "local_id": "C1_Admitted",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::C2_BranchKilledOnArrival": {
          "local_id": "C2_BranchKilledOnArrival",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::C3_FlushKilledOnArrival": {
          "local_id": "C3_FlushKilledOnArrival",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::C4_VisibleDequeue": {
          "local_id": "C4_VisibleDequeue",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::C5_InvalidHeadSkip": {
          "local_id": "C5_InvalidHeadSkip",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq::C1_EnqueueForwarded": {
          "local_id": "C1_EnqueueForwarded",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::C2_ChildDequeueCaptured": {
          "local_id": "C2_ChildDequeueCaptured",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::C3_ChildDequeueBranchKilled": {
          "local_id": "C3_ChildDequeueBranchKilled",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::C4_ChildDequeueFlushKilled": {
          "local_id": "C4_ChildDequeueFlushKilled",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::C5_VisibleParentDequeue": {
          "local_id": "C5_VisibleParentDequeue",
          "work_unit_id": "BoomMSHR.rpq"
        }
      },
      "identity_keys": {},
      "occurrences": {
        "BoomMSHR.rpq.main::DeqHandshake": {
          "local_id": "DeqHandshake",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::EnqHandshake": {
          "local_id": "EnqHandshake",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::InvalidHeadSkip": {
          "local_id": "InvalidHeadSkip",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::QueueInsert": {
          "local_id": "QueueInsert",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq::BufferCapture": {
          "local_id": "BufferCapture",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::ParentDeqHandshake": {
          "local_id": "ParentDeqHandshake",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::ParentEnqHandshake": {
          "local_id": "ParentEnqHandshake",
          "work_unit_id": "BoomMSHR.rpq"
        }
      },
      "predicates": {
        "BoomMSHR.rpq.main::HeadInvalid": {
          "local_id": "HeadInvalid",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::HeadValid": {
          "local_id": "HeadValid",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::IncomingBranchKilled": {
          "local_id": "IncomingBranchKilled",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::IncomingFlushKilled": {
          "local_id": "IncomingFlushKilled",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::QueueEmpty": {
          "local_id": "QueueEmpty",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq.main::QueueFull": {
          "local_id": "QueueFull",
          "work_unit_id": "BoomMSHR.rpq.main"
        },
        "BoomMSHR.rpq::OutputInvalid": {
          "local_id": "OutputInvalid",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::TransferBranchKilled": {
          "local_id": "TransferBranchKilled",
          "work_unit_id": "BoomMSHR.rpq"
        },
        "BoomMSHR.rpq::TransferFlushKilled": {
          "local_id": "TransferFlushKilled",
          "work_unit_id": "BoomMSHR.rpq"
        }
      }
    }
  },
  "freeze": {
    "candidate_axiom_count": 7,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 7
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.enq.valid && io.enq.ready",
      "evidence_statement_ids": [
        9
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "ParentEnqHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHR.rpq::io.enq.fire"
      ]
    },
    {
      "definition": "io.deq.valid && io.deq.ready",
      "evidence_statement_ids": [
        136,
        155
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.deq.valid",
          "io.deq.ready"
        ],
        "state_register": null,
        "state_values": []
      },
      "id": "ParentDeqHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHR.rpq::io.deq.fire"
      ]
    },
    {
      "definition": "_T_2 && _out_valid_T_15; the wrapper refill window is active and the exposed child dequeue is valid and survives branch/flush filtering, so the child payload is captured into the output buffer and out_valid is set",
      "evidence_statement_ids": [
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        170,
        171,
        172,
        173,
        174,
        175
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "_T_2",
          "_out_valid_T_15"
        ],
        "state_register": null,
        "state_values": []
      },
      "id": "BufferCapture",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    }
  ],
  "predicates": [
    {
      "definition": "out_valid == 0",
      "evidence_statement_ids": [
        7,
        136,
        156
      ],
      "grounding": {
        "negated": true,
        "source_signal": "out_valid",
        "state_register": null,
        "state_values": []
      },
      "id": "OutputInvalid"
    },
    {
      "definition": "(io.brupdate.b1.mispredict_mask & main.io.deq.bits.uop.br_mask) != 0",
      "evidence_statement_ids": [
        159,
        160
      ],
      "grounding": {
        "negated": false,
        "source_signal": "_out_valid_T_9",
        "state_register": null,
        "state_values": []
      },
      "id": "TransferBranchKilled"
    },
    {
      "definition": "io.flush && main.io.deq.bits.uop.uses_ldq",
      "evidence_statement_ids": [
        164
      ],
      "grounding": {
        "negated": false,
        "source_signal": "_out_valid_T_13",
        "state_register": null,
        "state_values": []
      },
      "id": "TransferFlushKilled"
    }
  ],
  "provenance": {
    "A1": {
      "derivation": "formal-certificate-v0.1",
      "kind": "lifted",
      "proof_method": "trusted-child-lift",
      "source_axioms": [
        "BoomMSHR.rpq.main::A1"
      ]
    },
    "A2": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-combinational-exclusion",
      "source_axioms": []
    },
    "A3": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-scalar-valid-token-provenance",
      "source_axioms": []
    },
    "A4": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "occurrence-bridge-history-composition",
      "source_axioms": []
    },
    "A5": {
      "derivation": "formal-certificate-v0.1",
      "kind": "emergent",
      "proof_method": "trusted-history-transitivity",
      "source_axioms": [
        "BoomMSHR.rpq.main::A11"
      ]
    },
    "A6": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-combinational-exclusion",
      "source_axioms": []
    },
    "A7": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-combinational-exclusion",
      "source_axioms": []
    }
  },
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7"
  ],
  "work_unit_id": "BoomMSHR.rpq"
}
```

## Parent-local source evidence

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:35-37
```scala

class BoomMSHR(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
  with HasL1HellaCacheParameters
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:38-40
```scala
{
  val io = IO(new Bundle {
    val id = Input(UInt())
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:106-116
```scala
  val s_invalid :: s_refill_req :: s_refill_resp :: s_drain_rpq_loads :: s_meta_read :: s_meta_resp_1 :: s_meta_resp_2 :: s_meta_clear :: s_wb_meta_read :: s_wb_req :: s_wb_resp :: s_commit_line :: s_drain_rpq :: s_meta_write_req :: s_mem_finish_1 :: s_mem_finish_2 :: s_prefetched :: s_prefetch :: Nil = Enum(18)
  val state = RegInit(s_invalid)

  val req     = Reg(new BoomDCacheReqInternal)
  val req_idx = req.addr(untagBits-1, blockOffBits)
  val req_tag = req.addr >> untagBits
  val req_block_addr = (req.addr >> blockOffBits) << blockOffBits
  val req_needs_wb = RegInit(false.B)

  val new_coh = RegInit(ClientMetadata.onReset)
  val (_, shrink_param, coh_on_clear) = req.old_meta.coh.onCacheControl(M_FLUSH)
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:124-136
```scala
  val (_, _, refill_done, refill_address_inc) = edge.addr_inc(io.mem_grant)
  val sec_rdy = (!cmd_requires_second_acquire && !io.req_is_probe &&
                 !state.isOneOf(s_invalid, s_meta_write_req, s_mem_finish_1, s_mem_finish_2))// Always accept secondary misses

  val rpq = Module(new BranchKillableQueue(new BoomDCacheReqInternal, cfg.nRPQ, u => u.uses_ldq, fastDeq=true))
  rpq.io.brupdate := io.brupdate
  rpq.io.flush  := io.exception
  assert(!(state === s_invalid && !rpq.io.empty))

  rpq.io.enq.valid := ((io.req_pri_val && io.req_pri_rdy) || (io.req_sec_val && io.req_sec_rdy)) && !isPrefetch(io.req.uop.mem_cmd)
  rpq.io.enq.bits  := io.req
  rpq.io.deq.ready := false.B
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:137-143
```scala

  val grantack = Reg(Valid(new TLBundleE(edge.bundle)))
  val refill_ctr  = Reg(UInt(log2Ceil(cacheDataBeats).W))
  val commit_line = Reg(Bool())
  val grant_had_data = Reg(Bool())
  val finish_to_prefetch = Reg(Bool())
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:144-169
```scala
  // Block probes if a tag write we started is still in the pipeline
  val meta_hazard = RegInit(0.U(2.W))
  when (meta_hazard =/= 0.U) { meta_hazard := meta_hazard + 1.U }
  when (io.meta_write.fire) { meta_hazard := 1.U }
  io.probe_rdy   := (meta_hazard === 0.U && (state.isOneOf(s_invalid, s_refill_req, s_refill_resp, s_drain_rpq_loads) || (state === s_meta_read && grantack.valid)))
  io.idx.valid := state =/= s_invalid
  io.tag.valid := state =/= s_invalid
  io.way.valid := !state.isOneOf(s_invalid, s_prefetch)
  io.idx.bits := req_idx
  io.tag.bits := req_tag
  io.way.bits := req.way_en

  io.meta_write.valid    := false.B
  io.meta_write.bits.idx      := req_idx
  io.meta_write.bits.data.coh := coh_on_clear
  io.meta_write.bits.data.tag := req_tag
  io.meta_write.bits.way_en   := req.way_en
  io.meta_write.bits.tag      := req_tag
  io.req_pri_rdy         := false.B
  io.req_sec_rdy         := sec_rdy && rpq.io.enq.ready
  io.mem_acquire.valid   := false.B
  // TODO: Use AcquirePerm if just doing permissions acquire
  io.mem_acquire.bits  := edge.AcquireBlock(
    fromSource      = io.id,
    toAddress       = Cat(req_tag, req_idx) << blockOffBits,
    lgSize          = lgCacheBlockBytes.U,
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:170-206
```scala
    growPermissions = grow_param)._2
  io.refill.valid        := false.B
  io.refill.bits.addr   := req_block_addr | (refill_ctr << rowOffBits)
  io.refill.bits.way_en := req.way_en
  io.refill.bits.wmask  := ~(0.U(rowWords.W))
  io.refill.bits.data   := io.lb_resp
  io.replay.valid        := false.B
  io.replay.bits         := rpq.io.deq.bits
  io.wb_req.valid        := false.B
  io.wb_req.bits.tag       := req.old_meta.tag
  io.wb_req.bits.idx       := req_idx
  io.wb_req.bits.param     := shrink_param
  io.wb_req.bits.way_en    := req.way_en
  io.wb_req.bits.source    := io.id
  io.wb_req.bits.voluntary := true.B
  io.resp.valid          := false.B
  io.resp.bits           := rpq.io.deq.bits
  io.commit_val          := false.B
  io.commit_addr         := req.addr
  io.commit_coh          := coh_on_grant
  io.meta_read.valid     := false.B
  io.meta_read.bits.idx := req_idx
  io.meta_read.bits.tag := req_tag
  io.meta_read.bits.way_en := req.way_en
  io.mem_finish.valid    := false.B
  io.mem_finish.bits  := grantack.bits
  io.lb_write.valid      := false.B
  io.lb_write.bits.offset := refill_address_inc >> rowOffBits
  io.lb_write.bits.data   := io.mem_grant.bits.data
  io.mem_grant.ready := false.B
  io.lb_read.offset := rpq.io.deq.bits.addr >> rowOffBits

  when (io.req_sec_val && io.req_sec_rdy) {
    req.uop.mem_cmd := dirtier_cmd
    when (is_hit_again) {
      new_coh := dirtier_coh
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:209-226
```scala
  def handle_pri_req(old_state: UInt): UInt = {
    val new_state = WireInit(old_state)
    grantack.valid := false.B
    refill_ctr := 0.U
    assert(rpq.io.enq.ready)
    req := io.req
    val old_coh   = io.req.old_meta.coh
    req_needs_wb := old_coh.onCacheControl(M_FLUSH)._1 // does the line we are evicting need to be written back
    when (io.req.tag_match) {
      val (is_hit, _, coh_on_hit) = old_coh.onAccess(io.req.uop.mem_cmd)
      when (is_hit) { // set dirty bit
        assert(isWrite(io.req.uop.mem_cmd))
        new_coh     := coh_on_hit
        new_state   := s_drain_rpq
      } .otherwise { // upgrade permissions
        new_coh     := old_coh
        new_state   := s_refill_req
      }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:227-230
```scala
    } .otherwise { // refill and writeback if necessary
      new_coh     := ClientMetadata.onReset
      new_state   := s_refill_req
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:233-252
```scala

  when (state === s_invalid) {
    io.req_pri_rdy := true.B
    grant_had_data := false.B

    when (io.req_pri_val && io.req_pri_rdy) {
      state := handle_pri_req(state)
    }
  } .elsewhen (state === s_refill_req) {
    io.mem_acquire.valid := true.B
    when (io.mem_acquire.fire) {
      state := s_refill_resp
    }
  } .elsewhen (state === s_refill_resp) {
    io.mem_grant.ready := true.B
    when (edge.hasData(io.mem_grant.bits)) {
      io.lb_write.valid       := io.mem_grant.valid
    } .otherwise {
      io.mem_grant.ready      := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:253-264
```scala

    when (io.mem_grant.fire) {
      grant_had_data := edge.hasData(io.mem_grant.bits)
    }
    when (refill_done) {
      grantack.valid := edge.isRequest(io.mem_grant.bits)
      grantack.bits := edge.GrantAck(io.mem_grant.bits)
      state := Mux(grant_had_data, s_drain_rpq_loads, s_drain_rpq)
      assert(!(!grant_had_data && req_needs_wb))
      commit_line := false.B
      new_coh := coh_on_grant
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:265-272
```scala
    }
  } .elsewhen (state === s_drain_rpq_loads) {
    val drain_load = (isRead(rpq.io.deq.bits.uop.mem_cmd) &&
                     !isWrite(rpq.io.deq.bits.uop.mem_cmd) &&
                     (rpq.io.deq.bits.uop.mem_cmd =/= M_XLR)) // LR should go through replay
    // drain all loads for now
    val rp_addr = Cat(req_tag, req_idx, rpq.io.deq.bits.addr(blockOffBits-1,0))
    val word_idx  = if (rowWords == 1) 0.U else rp_addr(log2Up(rowWords*coreDataBytes)-1, log2Up(wordBytes))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:273-277
```scala
    val data      = io.lb_resp
    val data_word = data >> Cat(word_idx, 0.U(log2Up(coreDataBits).W))
    val loadgen = new LoadGen(rpq.io.deq.bits.uop.mem_size, rpq.io.deq.bits.uop.mem_signed,
      Cat(req_tag, req_idx, rpq.io.deq.bits.addr(blockOffBits-1,0)),
      data_word, false.B, wordBytes)
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:279-297
```scala

    rpq.io.deq.ready  := io.resp.ready && drain_load

    io.lb_read.offset := rpq.io.deq.bits.addr >> rowOffBits

    io.resp.valid     := rpq.io.deq.valid && drain_load
    io.resp.bits.data := loadgen.data
    io.resp.bits.is_hella := rpq.io.deq.bits.is_hella
    when (rpq.io.deq.fire) {
      commit_line   := true.B
    }
      .elsewhen (rpq.io.empty && !commit_line)
    {
      when (!rpq.io.enq.fire) {
        state := s_mem_finish_1
        finish_to_prefetch := enablePrefetching.B
      }
    } .elsewhen (rpq.io.empty || (rpq.io.deq.valid && !drain_load)) {
      // io.commit_val is for the prefetcher. it tells the prefetcher that this line was correctly acquired
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:298-336
```scala
      // The prefetcher should consider fetching the next line
      io.commit_val := true.B
      state := s_meta_read
    }
  } .elsewhen (state === s_meta_read) {
    io.meta_read.valid := !io.prober_state.valid || !grantack.valid || (io.prober_state.bits(untagBits-1,blockOffBits) =/= req_idx)
    when (io.meta_read.fire) {
      state := s_meta_resp_1
    }
  } .elsewhen (state === s_meta_resp_1) {
    state := s_meta_resp_2
  } .elsewhen (state === s_meta_resp_2) {
    val needs_wb = io.meta_resp.bits.coh.onCacheControl(M_FLUSH)._1
    state := Mux(!io.meta_resp.valid, s_meta_read, // Prober could have nack'd this read
             Mux(needs_wb, s_meta_clear, s_commit_line))
  } .elsewhen (state === s_meta_clear) {
    io.meta_write.valid         := true.B

    when (io.meta_write.fire) {
      state      := s_wb_req
    }
  } .elsewhen (state === s_wb_req) {
    io.wb_req.valid          := true.B
    when (io.wb_req.fire) {
      state := s_wb_resp
    }
  } .elsewhen (state === s_wb_resp) {
    when (io.wb_resp) {
      state := s_commit_line
    }
  } .elsewhen (state === s_commit_line) {
    io.lb_read.offset := refill_ctr

    io.refill.valid       := true.B
    when (io.refill.fire) {
      refill_ctr := refill_ctr + 1.U
      when (refill_ctr === (cacheDataBeats - 1).U) {
        state := s_drain_rpq
      }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:337-343
```scala
    }
  } .elsewhen (state === s_drain_rpq) {
    io.replay <> rpq.io.deq
    io.replay.bits.way_en    := req.way_en
    io.replay.bits.addr := Cat(req_tag, req_idx, rpq.io.deq.bits.addr(blockOffBits-1,0))
    when (io.replay.fire && isWrite(rpq.io.deq.bits.uop.mem_cmd)) {
      // Set dirty bit
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:344-385
```scala
      val (is_hit, _, coh_on_hit) = new_coh.onAccess(rpq.io.deq.bits.uop.mem_cmd)
      assert(is_hit, "We still don't have permissions for this store")
      new_coh := coh_on_hit
    }
    when (rpq.io.empty && !rpq.io.enq.valid) {
      state := s_meta_write_req
    }
  } .elsewhen (state === s_meta_write_req) {
    io.meta_write.valid         := true.B
    io.meta_write.bits.idx      := req_idx
    io.meta_write.bits.data.coh := new_coh
    io.meta_write.bits.data.tag := req_tag
    io.meta_write.bits.way_en   := req.way_en
    when (io.meta_write.fire) {
      state := s_mem_finish_1
      finish_to_prefetch := false.B
    }
  } .elsewhen (state === s_mem_finish_1) {
    io.mem_finish.valid := grantack.valid
    when (io.mem_finish.fire || !grantack.valid) {
      grantack.valid := false.B
      state := s_mem_finish_2
    }
  } .elsewhen (state === s_mem_finish_2) {
    state := Mux(finish_to_prefetch, s_prefetch, s_invalid)
  } .elsewhen (state === s_prefetch) {
    io.req_pri_rdy := true.B
    when ((io.req_sec_val && !io.req_sec_rdy) || io.clear_prefetch) {
      state := s_invalid
    } .elsewhen (io.req_sec_val && io.req_sec_rdy) {
      val (is_hit, _, coh_on_hit) = new_coh.onAccess(io.req.uop.mem_cmd)
      when (is_hit) { // Proceed with refill
        new_coh := coh_on_hit
        state := s_meta_read
      } .otherwise { // Reacquire this line
        new_coh := ClientMetadata.onReset
        state := s_refill_req
      }
    } .elsewhen (io.req_pri_val && io.req_pri_rdy) {
      grant_had_data := false.B
      state := handle_pri_req(state)
    }
```

### generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:92-94
```scala
    if (none) false.B
    else if (min == max) { log2Ceil(min).U === x }
    else { log2Ceil(min).U <= x && x <= log2Ceil(max).U }
```

### generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:138-140
```scala
  def contains(x: BigInt) = ((x ^ base) & ~mask) == 0
  def contains(x: UInt) = ((x ^ base.U).zext & (~mask).S) === 0.S
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:10-13
```scala
class StoreGen(typ: UInt, addr: UInt, dat: UInt, maxSize: Int) {
  val size = Wire(UInt(log2Up(log2Up(maxSize)+1).W))
  size := typ
  val dat_padded = dat.pad(maxSize*8)
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:41-46
```scala
      val pos = 8 << i
      val shifted = Mux(addr(i), res(2*pos-1,pos), res(pos-1,0))
      val doZero = (i == 0).B && zero
      val zeroed = Mux(doZero, 0.U, shifted)
      res = Cat(Mux(size === i.U || doZero, Fill(8*maxSize-pos, signed && zeroed(pos-1)), res(8*maxSize-1,pos)), zeroed)
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

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:70-72
```scala
        //    opcode === TLMessages.ReleaseData
      case d: TLBundleD => d.opcode(2) && !d.opcode(1)
        //    opcode === TLMessages.Grant     ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:105-107
```scala
        //    opcode === TLMessages.ReleaseData
      case d: TLBundleD => d.opcode(0)
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

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:268-270
```scala
    val r = firstlastHelper(bits, fire)
    (r._1, r._2, r._3, r._4 << log2Ceil(manager.beatBytes))
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:345-352
```scala
    val legal = manager.supportsAcquireBFast(toAddress, lgSize)
    val a = Wire(new TLBundleA(bundle))
    a.opcode  := TLMessages.AcquireBlock
    a.param   := growPermissions
    a.size    := lgSize
    a.source  := fromSource
    a.address := toAddress
    a.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:353-357
```scala
    a.echo    := DontCare
    a.mask    := mask(toAddress, lgSize)
    a.data    := DontCare
    a.corrupt := false.B
    (legal, a)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:450-453
```scala
  def GrantAck(toSink: UInt): TLBundleE = {
    val e = Wire(new TLBundleE(bundle))
    e.sink := toSink
    e
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

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:83-90
```scala
    //assert(c === rd || param === toT, "Client was expecting trunk permissions.")
    MuxLookup(Cat(c, param), Nothing)(Seq(
    //(effect param) -> (next)
      Cat(rd, toB)   -> Branch,
      Cat(rd, toT)   -> Trunk,
      Cat(wi, toT)   -> Trunk,
      Cat(wr, toT)   -> Dirty))
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:103-110
```scala
    val r2 = growStarter(second_cmd)
    val needs_second_acq = isWriteIntent(second_cmd) && !isWriteIntent(first_cmd)
    val hit_again = r1._1 && r2._1
    val dirties = categorize(second_cmd) === wr
    val biggest_grow_param = Mux(dirties, r2._2, r1._2)
    val dirtiest_state = ClientMetadata(biggest_grow_param)
    val dirtiest_cmd = Mux(dirties, second_cmd, first_cmd)
    (needs_second_acq, hit_again, biggest_grow_param, dirtiest_state, dirtiest_cmd)
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:119-134
```scala
    import TLPermissions._
    MuxTLookup(Cat(param, state), (false.B, 0.U, 0.U), Seq(
    //(wanted, am now)  -> (hasDirtyData resp, next)
      Cat(toT, Dirty)   -> (true.B,  TtoT, Trunk),
      Cat(toT, Trunk)   -> (false.B, TtoT, Trunk),
      Cat(toT, Branch)  -> (false.B, BtoB, Branch),
      Cat(toT, Nothing) -> (false.B, NtoN, Nothing),
      Cat(toB, Dirty)   -> (true.B,  TtoB, Branch),
      Cat(toB, Trunk)   -> (false.B, TtoB, Branch),  // Policy: Don't notify on clean downgrade
      Cat(toB, Branch)  -> (false.B, BtoB, Branch),
      Cat(toB, Nothing) -> (false.B, NtoN, Nothing),
      Cat(toN, Dirty)   -> (true.B,  TtoN, Nothing),
      Cat(toN, Trunk)   -> (false.B, TtoN, Nothing), // Policy: Don't notify on clean downgrade
      Cat(toN, Branch)  -> (false.B, BtoN, Nothing), // Policy: Don't notify on clean downgrade
      Cat(toN, Nothing) -> (false.B, NtoN, Nothing)))
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:139-141
```scala
    import TLPermissions._
    MuxLookup(cmd, toN)(Seq(
      M_FLUSH   -> toN,
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:159-162
```scala
  def apply(perm: UInt) = {
    val meta = Wire(new ClientMetadata)
    meta.state := perm
    meta
```

### generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:683-687
```scala
    // We return an or-reduction of all the cases, checking whether any contains both the dynamic size and dynamic address on the wire.
      ((Some(s) == range).B || s.containsLg(lgSize)) &&
      a.map(_.contains(address)).reduce(_||_)
    }.foldLeft(false.B)(_||_)
  }
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:34-36
```scala
  def apply[T <: Data, U <: Data](cond: Bool, con: (T, U), alt: (T, U)): (T, U) =
    (Mux(cond, con._1, alt._1), Mux(cond, con._2, alt._2))
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:37-39
```scala
  def apply[T <: Data, U <: Data, W <: Data](cond: Bool, con: (T, U, W), alt: (T, U, W)): (T, U, W) =
    (Mux(cond, con._1, alt._1), Mux(cond, con._2, alt._2), Mux(cond, con._3, alt._3))
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:48-50
```scala
    for ((k, v) <- mapping.reverse)
      res = MuxT(k === key, v, res)
    res
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:55-57
```scala
    for ((k, v) <- mapping.reverse)
      res = MuxT(k === key, v, res)
    res
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:201-203
```scala
    val lgBytes = log2Ceil(beatBytes)
    val sizeOH = UIntToOH(lgSize | 0.U(log2Up(beatBytes).W), log2Up(beatBytes)) | (groupBy*2 - 1).U
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:205-207
```scala
      if (i == 0) {
        Seq((lgSize >= lgBytes.asUInt, true.B))
      } else {
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:208-212
```scala
        val sub = helper(i-1)
        val size = sizeOH(lgBytes - i)
        val bit = addr_lo(lgBytes - i)
        val nbit = !bit
        Seq.tabulate (1 << i) { j =>
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:213-216
```scala
          val (sub_acc, sub_eq) = sub(j/2)
          val eq = sub_eq && (if (j % 2 == 1) bit else nbit)
          val acc = sub_acc || (size && eq)
          (acc, eq)
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:221-223
```scala
    if (groupBy == beatBytes) 1.U else
      Cat(helper(lgBytes-log2Ceil(groupBy)).map(_._1).reverse)
  }
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
[0] FIRRTL:189060 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:36:7 KIND:structural :: input clock : Clock
[1] FIRRTL:189061 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:36:7 KIND:structural :: input reset : Reset
[2] FIRRTL:189062 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:39:14 KIND:structural :: output io : { flip id : UInt, flip req_pri_val : UInt<1>, req_pri_rdy : UInt<1>, flip req_sec_val : UInt<1>, req_sec_rdy : UInt<1>, flip clear_prefetch : UInt<1>, flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip exception : UInt<1>, flip rob_pnr_idx : UInt<5>, flip rob_head_idx : UInt<5>, flip req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}, flip req_is_probe : UInt<1>, idx : { valid : UInt<1>, bits : UInt}, way : { valid : UInt<1>, bits : UInt}, tag : { valid : UInt<1>, bits : UInt}, mem_acquire : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, flip mem_grant : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, sink : UInt<3>, denied : UInt<1>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, mem_finish : { flip ready : UInt<1>, valid : UInt<1>, bits : { sink : UInt<3>}}, flip prober_state : { valid : UInt<1>, bits : UInt<40>}, refill : { flip ready : UInt<1>, valid : UInt<1>, bits : { way_en : UInt<4>, addr : UInt<12>, wmask : UInt<1>, data : UInt<64>}}, meta_write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>, data : { coh : { state : UInt<2>}, tag : UInt<20>}}}, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}}, flip meta_resp : { valid : UInt<1>, bits : { coh : { state : UInt<2>}, tag : UInt<20>}}, wb_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { tag : UInt<20>, idx : UInt<6>, source : UInt<2>, param : UInt<3>, way_en : UInt<4>, voluntary : UInt<1>}}, commit_val : UInt<1>, commit_addr : UInt<40>, commit_coh : { state : UInt<2>}, lb_read : { offset : UInt<3>}, flip lb_resp : UInt<64>, lb_write : { valid : UInt<1>, bits : { offset : UInt<3>, data : UInt<64>}}, replay : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, resp : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, flip wb_resp : UInt<1>, probe_rdy : UInt<1>}
[3] FIRRTL:189064 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:107:22 KIND:regreset :: regreset state : UInt<5>, clock, reset, UInt<5>(0h0)
[4] FIRRTL:189065 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:109:20 KIND:reg :: reg req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}, clock
[5] FIRRTL:189066 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:110:25 KIND:node :: node req_idx = bits(req.addr, 11, 6)
[6] FIRRTL:189067 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:111:26 KIND:node :: node req_tag = shr(req.addr, 12)
[7] FIRRTL:189068 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:112:34 KIND:node :: node _req_block_addr_T = shr(req.addr, 6)
[8] FIRRTL:189069 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:112:51 KIND:node :: node req_block_addr = shl(_req_block_addr_T, 6)
[9] FIRRTL:189070 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:113:29 KIND:regreset :: regreset req_needs_wb : UInt<1>, clock, reset, UInt<1>(0h0)
[10] FIRRTL:189071 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire new_coh_meta : { state : UInt<2>}
[11] FIRRTL:189072 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect new_coh_meta.state, UInt<2>(0h0)
[12] FIRRTL:189073 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:115:24 KIND:regreset :: regreset new_coh : { state : UInt<2>}, clock, reset, new_coh_meta
[13] FIRRTL:189074 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T = eq(UInt<5>(0h10), UInt<5>(0h10))
[14] FIRRTL:189075 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T_1 = mux(_r_T, UInt<2>(0h2), UInt<2>(0h2))
[15] FIRRTL:189076 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T_2 = eq(UInt<5>(0h12), UInt<5>(0h10))
[16] FIRRTL:189077 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T_3 = mux(_r_T_2, UInt<2>(0h1), _r_T_1)
[17] FIRRTL:189078 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T_4 = eq(UInt<5>(0h13), UInt<5>(0h10))
[18] FIRRTL:189079 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _r_T_5 = mux(_r_T_4, UInt<2>(0h0), _r_T_3)
[19] FIRRTL:189080 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:120:19 KIND:node :: node _r_T_6 = cat(_r_T_5, req.old_meta.coh.state)
[20] FIRRTL:189081 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:122:10 KIND:node :: node _r_T_7 = cat(UInt<2>(0h0), UInt<2>(0h3))
[21] FIRRTL:189082 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:123:10 KIND:node :: node _r_T_8 = cat(UInt<2>(0h0), UInt<2>(0h2))
[22] FIRRTL:189083 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:124:10 KIND:node :: node _r_T_9 = cat(UInt<2>(0h0), UInt<2>(0h1))
[23] FIRRTL:189084 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:125:10 KIND:node :: node _r_T_10 = cat(UInt<2>(0h0), UInt<2>(0h0))
[24] FIRRTL:189085 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:126:10 KIND:node :: node _r_T_11 = cat(UInt<2>(0h1), UInt<2>(0h3))
[25] FIRRTL:189086 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:127:10 KIND:node :: node _r_T_12 = cat(UInt<2>(0h1), UInt<2>(0h2))
[26] FIRRTL:189087 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:128:10 KIND:node :: node _r_T_13 = cat(UInt<2>(0h1), UInt<2>(0h1))
[27] FIRRTL:189088 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:129:10 KIND:node :: node _r_T_14 = cat(UInt<2>(0h1), UInt<2>(0h0))
[28] FIRRTL:189089 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:130:10 KIND:node :: node _r_T_15 = cat(UInt<2>(0h2), UInt<2>(0h3))
[29] FIRRTL:189090 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:131:10 KIND:node :: node _r_T_16 = cat(UInt<2>(0h2), UInt<2>(0h2))
[30] FIRRTL:189091 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:132:10 KIND:node :: node _r_T_17 = cat(UInt<2>(0h2), UInt<2>(0h1))
[31] FIRRTL:189092 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:133:10 KIND:node :: node _r_T_18 = cat(UInt<2>(0h2), UInt<2>(0h0))
[32] FIRRTL:189093 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_19 = eq(_r_T_18, _r_T_6)
[33] FIRRTL:189094 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_20 = mux(_r_T_19, UInt<1>(0h0), UInt<1>(0h0))
[34] FIRRTL:189095 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_21 = mux(_r_T_19, UInt<3>(0h5), UInt<1>(0h0))
[35] FIRRTL:189096 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_22 = mux(_r_T_19, UInt<2>(0h0), UInt<1>(0h0))
[36] FIRRTL:189097 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_23 = eq(_r_T_17, _r_T_6)
[37] FIRRTL:189098 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_24 = mux(_r_T_23, UInt<1>(0h0), _r_T_20)
[38] FIRRTL:189099 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_25 = mux(_r_T_23, UInt<3>(0h2), _r_T_21)
[39] FIRRTL:189100 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_26 = mux(_r_T_23, UInt<2>(0h0), _r_T_22)
[40] FIRRTL:189101 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_27 = eq(_r_T_16, _r_T_6)
[41] FIRRTL:189102 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_28 = mux(_r_T_27, UInt<1>(0h0), _r_T_24)
[42] FIRRTL:189103 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_29 = mux(_r_T_27, UInt<3>(0h1), _r_T_25)
[43] FIRRTL:189104 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_30 = mux(_r_T_27, UInt<2>(0h0), _r_T_26)
[44] FIRRTL:189105 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_31 = eq(_r_T_15, _r_T_6)
[45] FIRRTL:189106 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_32 = mux(_r_T_31, UInt<1>(0h1), _r_T_28)
[46] FIRRTL:189107 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_33 = mux(_r_T_31, UInt<3>(0h1), _r_T_29)
[47] FIRRTL:189108 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_34 = mux(_r_T_31, UInt<2>(0h0), _r_T_30)
[48] FIRRTL:189109 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_35 = eq(_r_T_14, _r_T_6)
[49] FIRRTL:189110 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_36 = mux(_r_T_35, UInt<1>(0h0), _r_T_32)
[50] FIRRTL:189111 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_37 = mux(_r_T_35, UInt<3>(0h5), _r_T_33)
[51] FIRRTL:189112 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_38 = mux(_r_T_35, UInt<2>(0h0), _r_T_34)
[52] FIRRTL:189113 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_39 = eq(_r_T_13, _r_T_6)
[53] FIRRTL:189114 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_40 = mux(_r_T_39, UInt<1>(0h0), _r_T_36)
[54] FIRRTL:189115 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_41 = mux(_r_T_39, UInt<3>(0h4), _r_T_37)
[55] FIRRTL:189116 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_42 = mux(_r_T_39, UInt<2>(0h1), _r_T_38)
[56] FIRRTL:189117 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_43 = eq(_r_T_12, _r_T_6)
[57] FIRRTL:189118 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_44 = mux(_r_T_43, UInt<1>(0h0), _r_T_40)
[58] FIRRTL:189119 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_45 = mux(_r_T_43, UInt<3>(0h0), _r_T_41)
[59] FIRRTL:189120 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_46 = mux(_r_T_43, UInt<2>(0h1), _r_T_42)
[60] FIRRTL:189121 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_47 = eq(_r_T_11, _r_T_6)
[61] FIRRTL:189122 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_48 = mux(_r_T_47, UInt<1>(0h1), _r_T_44)
[62] FIRRTL:189123 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_49 = mux(_r_T_47, UInt<3>(0h0), _r_T_45)
[63] FIRRTL:189124 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_50 = mux(_r_T_47, UInt<2>(0h1), _r_T_46)
[64] FIRRTL:189125 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_51 = eq(_r_T_10, _r_T_6)
[65] FIRRTL:189126 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_52 = mux(_r_T_51, UInt<1>(0h0), _r_T_48)
[66] FIRRTL:189127 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_53 = mux(_r_T_51, UInt<3>(0h5), _r_T_49)
[67] FIRRTL:189128 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_54 = mux(_r_T_51, UInt<2>(0h0), _r_T_50)
[68] FIRRTL:189129 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_55 = eq(_r_T_9, _r_T_6)
[69] FIRRTL:189130 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_56 = mux(_r_T_55, UInt<1>(0h0), _r_T_52)
[70] FIRRTL:189131 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_57 = mux(_r_T_55, UInt<3>(0h4), _r_T_53)
[71] FIRRTL:189132 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_58 = mux(_r_T_55, UInt<2>(0h1), _r_T_54)
[72] FIRRTL:189133 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_59 = eq(_r_T_8, _r_T_6)
[73] FIRRTL:189134 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_60 = mux(_r_T_59, UInt<1>(0h0), _r_T_56)
[74] FIRRTL:189135 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_61 = mux(_r_T_59, UInt<3>(0h3), _r_T_57)
[75] FIRRTL:189136 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_62 = mux(_r_T_59, UInt<2>(0h2), _r_T_58)
[76] FIRRTL:189137 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_63 = eq(_r_T_7, _r_T_6)
[77] FIRRTL:189138 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node r_1 = mux(_r_T_63, UInt<1>(0h1), _r_T_60)
[78] FIRRTL:189139 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node shrink_param = mux(_r_T_63, UInt<3>(0h3), _r_T_61)
[79] FIRRTL:189140 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node r_3 = mux(_r_T_63, UInt<2>(0h2), _r_T_62)
[80] FIRRTL:189141 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire coh_on_clear : { state : UInt<2>}
[81] FIRRTL:189142 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect coh_on_clear.state, r_3
[82] FIRRTL:189143 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _grow_param_r_c_cat_T = eq(req.uop.mem_cmd, UInt<1>(0h1))
[83] FIRRTL:189144 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _grow_param_r_c_cat_T_1 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[84] FIRRTL:189145 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _grow_param_r_c_cat_T_2 = or(_grow_param_r_c_cat_T, _grow_param_r_c_cat_T_1)
[85] FIRRTL:189146 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _grow_param_r_c_cat_T_3 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[86] FIRRTL:189147 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _grow_param_r_c_cat_T_4 = or(_grow_param_r_c_cat_T_2, _grow_param_r_c_cat_T_3)
[87] FIRRTL:189148 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_5 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[88] FIRRTL:189149 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_6 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[89] FIRRTL:189150 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_7 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[90] FIRRTL:189151 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_8 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[91] FIRRTL:189152 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_9 = or(_grow_param_r_c_cat_T_5, _grow_param_r_c_cat_T_6)
[92] FIRRTL:189153 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_10 = or(_grow_param_r_c_cat_T_9, _grow_param_r_c_cat_T_7)
[93] FIRRTL:189154 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_11 = or(_grow_param_r_c_cat_T_10, _grow_param_r_c_cat_T_8)
[94] FIRRTL:189155 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_12 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[95] FIRRTL:189156 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_13 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[96] FIRRTL:189157 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_14 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[97] FIRRTL:189158 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_15 = eq(req.uop.mem_cmd, UInt<4>(0he))
[98] FIRRTL:189159 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_16 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[99] FIRRTL:189160 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_17 = or(_grow_param_r_c_cat_T_12, _grow_param_r_c_cat_T_13)
[100] FIRRTL:189161 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_18 = or(_grow_param_r_c_cat_T_17, _grow_param_r_c_cat_T_14)
[101] FIRRTL:189162 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_19 = or(_grow_param_r_c_cat_T_18, _grow_param_r_c_cat_T_15)
[102] FIRRTL:189163 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_20 = or(_grow_param_r_c_cat_T_19, _grow_param_r_c_cat_T_16)
[103] FIRRTL:189164 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _grow_param_r_c_cat_T_21 = or(_grow_param_r_c_cat_T_11, _grow_param_r_c_cat_T_20)
[104] FIRRTL:189165 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _grow_param_r_c_cat_T_22 = or(_grow_param_r_c_cat_T_4, _grow_param_r_c_cat_T_21)
[105] FIRRTL:189166 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _grow_param_r_c_cat_T_23 = eq(req.uop.mem_cmd, UInt<1>(0h1))
[106] FIRRTL:189167 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _grow_param_r_c_cat_T_24 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[107] FIRRTL:189168 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _grow_param_r_c_cat_T_25 = or(_grow_param_r_c_cat_T_23, _grow_param_r_c_cat_T_24)
[108] FIRRTL:189169 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _grow_param_r_c_cat_T_26 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[109] FIRRTL:189170 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _grow_param_r_c_cat_T_27 = or(_grow_param_r_c_cat_T_25, _grow_param_r_c_cat_T_26)
[110] FIRRTL:189171 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_28 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[111] FIRRTL:189172 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_29 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[112] FIRRTL:189173 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_30 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[113] FIRRTL:189174 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_31 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[114] FIRRTL:189175 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_32 = or(_grow_param_r_c_cat_T_28, _grow_param_r_c_cat_T_29)
[115] FIRRTL:189176 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_33 = or(_grow_param_r_c_cat_T_32, _grow_param_r_c_cat_T_30)
[116] FIRRTL:189177 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_34 = or(_grow_param_r_c_cat_T_33, _grow_param_r_c_cat_T_31)
[117] FIRRTL:189178 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_35 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[118] FIRRTL:189179 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_36 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[119] FIRRTL:189180 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_37 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[120] FIRRTL:189181 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_38 = eq(req.uop.mem_cmd, UInt<4>(0he))
[121] FIRRTL:189182 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _grow_param_r_c_cat_T_39 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[122] FIRRTL:189183 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_40 = or(_grow_param_r_c_cat_T_35, _grow_param_r_c_cat_T_36)
[123] FIRRTL:189184 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_41 = or(_grow_param_r_c_cat_T_40, _grow_param_r_c_cat_T_37)
[124] FIRRTL:189185 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_42 = or(_grow_param_r_c_cat_T_41, _grow_param_r_c_cat_T_38)
[125] FIRRTL:189186 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _grow_param_r_c_cat_T_43 = or(_grow_param_r_c_cat_T_42, _grow_param_r_c_cat_T_39)
[126] FIRRTL:189187 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _grow_param_r_c_cat_T_44 = or(_grow_param_r_c_cat_T_34, _grow_param_r_c_cat_T_43)
[127] FIRRTL:189188 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _grow_param_r_c_cat_T_45 = or(_grow_param_r_c_cat_T_27, _grow_param_r_c_cat_T_44)
[128] FIRRTL:189189 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _grow_param_r_c_cat_T_46 = eq(req.uop.mem_cmd, UInt<2>(0h3))
[129] FIRRTL:189190 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _grow_param_r_c_cat_T_47 = or(_grow_param_r_c_cat_T_45, _grow_param_r_c_cat_T_46)
[130] FIRRTL:189191 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _grow_param_r_c_cat_T_48 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[131] FIRRTL:189192 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _grow_param_r_c_cat_T_49 = or(_grow_param_r_c_cat_T_47, _grow_param_r_c_cat_T_48)
[132] FIRRTL:189193 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node grow_param_r_c = cat(_grow_param_r_c_cat_T_22, _grow_param_r_c_cat_T_49)
[133] FIRRTL:189194 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _grow_param_r_T = cat(grow_param_r_c, new_coh.state)
[134] FIRRTL:189195 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _grow_param_r_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[135] FIRRTL:189196 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _grow_param_r_T_2 = cat(_grow_param_r_T_1, UInt<2>(0h3))
[136] FIRRTL:189197 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _grow_param_r_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[137] FIRRTL:189198 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _grow_param_r_T_4 = cat(_grow_param_r_T_3, UInt<2>(0h2))
[138] FIRRTL:189199 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _grow_param_r_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[139] FIRRTL:189200 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _grow_param_r_T_6 = cat(_grow_param_r_T_5, UInt<2>(0h1))
[140] FIRRTL:189201 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _grow_param_r_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[141] FIRRTL:189202 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _grow_param_r_T_8 = cat(_grow_param_r_T_7, UInt<2>(0h3))
[142] FIRRTL:189203 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _grow_param_r_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[143] FIRRTL:189204 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _grow_param_r_T_10 = cat(_grow_param_r_T_9, UInt<2>(0h2))
[144] FIRRTL:189205 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _grow_param_r_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[145] FIRRTL:189206 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _grow_param_r_T_12 = cat(_grow_param_r_T_11, UInt<2>(0h3))
[146] FIRRTL:189207 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _grow_param_r_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[147] FIRRTL:189208 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _grow_param_r_T_14 = cat(_grow_param_r_T_13, UInt<2>(0h2))
[148] FIRRTL:189209 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _grow_param_r_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[149] FIRRTL:189210 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _grow_param_r_T_16 = cat(_grow_param_r_T_15, UInt<2>(0h0))
[150] FIRRTL:189211 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _grow_param_r_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[151] FIRRTL:189212 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _grow_param_r_T_18 = cat(_grow_param_r_T_17, UInt<2>(0h1))
[152] FIRRTL:189213 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _grow_param_r_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[153] FIRRTL:189214 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _grow_param_r_T_20 = cat(_grow_param_r_T_19, UInt<2>(0h0))
[154] FIRRTL:189215 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _grow_param_r_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[155] FIRRTL:189216 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _grow_param_r_T_22 = cat(_grow_param_r_T_21, UInt<2>(0h1))
[156] FIRRTL:189217 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _grow_param_r_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[157] FIRRTL:189218 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _grow_param_r_T_24 = cat(_grow_param_r_T_23, UInt<2>(0h0))
[158] FIRRTL:189219 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_25 = eq(_grow_param_r_T_24, _grow_param_r_T)
[159] FIRRTL:189220 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_26 = mux(_grow_param_r_T_25, UInt<1>(0h0), UInt<1>(0h0))
[160] FIRRTL:189221 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_27 = mux(_grow_param_r_T_25, UInt<2>(0h1), UInt<1>(0h0))
[161] FIRRTL:189222 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_28 = eq(_grow_param_r_T_22, _grow_param_r_T)
[162] FIRRTL:189223 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_29 = mux(_grow_param_r_T_28, UInt<1>(0h0), _grow_param_r_T_26)
[163] FIRRTL:189224 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_30 = mux(_grow_param_r_T_28, UInt<2>(0h2), _grow_param_r_T_27)
[164] FIRRTL:189225 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_31 = eq(_grow_param_r_T_20, _grow_param_r_T)
[165] FIRRTL:189226 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_32 = mux(_grow_param_r_T_31, UInt<1>(0h0), _grow_param_r_T_29)
[166] FIRRTL:189227 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_33 = mux(_grow_param_r_T_31, UInt<2>(0h1), _grow_param_r_T_30)
[167] FIRRTL:189228 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_34 = eq(_grow_param_r_T_18, _grow_param_r_T)
[168] FIRRTL:189229 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_35 = mux(_grow_param_r_T_34, UInt<1>(0h0), _grow_param_r_T_32)
[169] FIRRTL:189230 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_36 = mux(_grow_param_r_T_34, UInt<2>(0h2), _grow_param_r_T_33)
[170] FIRRTL:189231 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_37 = eq(_grow_param_r_T_16, _grow_param_r_T)
[171] FIRRTL:189232 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_38 = mux(_grow_param_r_T_37, UInt<1>(0h0), _grow_param_r_T_35)
[172] FIRRTL:189233 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_39 = mux(_grow_param_r_T_37, UInt<2>(0h0), _grow_param_r_T_36)
[173] FIRRTL:189234 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_40 = eq(_grow_param_r_T_14, _grow_param_r_T)
[174] FIRRTL:189235 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_41 = mux(_grow_param_r_T_40, UInt<1>(0h1), _grow_param_r_T_38)
[175] FIRRTL:189236 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_42 = mux(_grow_param_r_T_40, UInt<2>(0h3), _grow_param_r_T_39)
[176] FIRRTL:189237 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_43 = eq(_grow_param_r_T_12, _grow_param_r_T)
[177] FIRRTL:189238 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_44 = mux(_grow_param_r_T_43, UInt<1>(0h1), _grow_param_r_T_41)
[178] FIRRTL:189239 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_45 = mux(_grow_param_r_T_43, UInt<2>(0h3), _grow_param_r_T_42)
[179] FIRRTL:189240 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_46 = eq(_grow_param_r_T_10, _grow_param_r_T)
[180] FIRRTL:189241 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_47 = mux(_grow_param_r_T_46, UInt<1>(0h1), _grow_param_r_T_44)
[181] FIRRTL:189242 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_48 = mux(_grow_param_r_T_46, UInt<2>(0h2), _grow_param_r_T_45)
[182] FIRRTL:189243 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_49 = eq(_grow_param_r_T_8, _grow_param_r_T)
[183] FIRRTL:189244 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_50 = mux(_grow_param_r_T_49, UInt<1>(0h1), _grow_param_r_T_47)
[184] FIRRTL:189245 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_51 = mux(_grow_param_r_T_49, UInt<2>(0h3), _grow_param_r_T_48)
[185] FIRRTL:189246 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_52 = eq(_grow_param_r_T_6, _grow_param_r_T)
[186] FIRRTL:189247 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_53 = mux(_grow_param_r_T_52, UInt<1>(0h1), _grow_param_r_T_50)
[187] FIRRTL:189248 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_54 = mux(_grow_param_r_T_52, UInt<2>(0h1), _grow_param_r_T_51)
[188] FIRRTL:189249 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_55 = eq(_grow_param_r_T_4, _grow_param_r_T)
[189] FIRRTL:189250 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _grow_param_r_T_56 = mux(_grow_param_r_T_55, UInt<1>(0h1), _grow_param_r_T_53)
[190] FIRRTL:189251 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _grow_param_r_T_57 = mux(_grow_param_r_T_55, UInt<2>(0h2), _grow_param_r_T_54)
[191] FIRRTL:189252 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _grow_param_r_T_58 = eq(_grow_param_r_T_2, _grow_param_r_T)
[192] FIRRTL:189253 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node grow_param_r_1 = mux(_grow_param_r_T_58, UInt<1>(0h1), _grow_param_r_T_56)
[193] FIRRTL:189254 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node grow_param = mux(_grow_param_r_T_58, UInt<2>(0h3), _grow_param_r_T_57)
[194] FIRRTL:189255 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire grow_param_meta : { state : UInt<2>}
[195] FIRRTL:189256 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect grow_param_meta.state, grow_param
[196] FIRRTL:189257 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _coh_on_grant_c_cat_T = eq(req.uop.mem_cmd, UInt<1>(0h1))
[197] FIRRTL:189258 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _coh_on_grant_c_cat_T_1 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[198] FIRRTL:189259 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _coh_on_grant_c_cat_T_2 = or(_coh_on_grant_c_cat_T, _coh_on_grant_c_cat_T_1)
[199] FIRRTL:189260 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _coh_on_grant_c_cat_T_3 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[200] FIRRTL:189261 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _coh_on_grant_c_cat_T_4 = or(_coh_on_grant_c_cat_T_2, _coh_on_grant_c_cat_T_3)
[201] FIRRTL:189262 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_5 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[202] FIRRTL:189263 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_6 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[203] FIRRTL:189264 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_7 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[204] FIRRTL:189265 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_8 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[205] FIRRTL:189266 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_9 = or(_coh_on_grant_c_cat_T_5, _coh_on_grant_c_cat_T_6)
[206] FIRRTL:189267 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_10 = or(_coh_on_grant_c_cat_T_9, _coh_on_grant_c_cat_T_7)
[207] FIRRTL:189268 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_11 = or(_coh_on_grant_c_cat_T_10, _coh_on_grant_c_cat_T_8)
[208] FIRRTL:189269 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_12 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[209] FIRRTL:189270 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_13 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[210] FIRRTL:189271 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_14 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[211] FIRRTL:189272 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_15 = eq(req.uop.mem_cmd, UInt<4>(0he))
[212] FIRRTL:189273 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_16 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[213] FIRRTL:189274 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_17 = or(_coh_on_grant_c_cat_T_12, _coh_on_grant_c_cat_T_13)
[214] FIRRTL:189275 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_18 = or(_coh_on_grant_c_cat_T_17, _coh_on_grant_c_cat_T_14)
[215] FIRRTL:189276 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_19 = or(_coh_on_grant_c_cat_T_18, _coh_on_grant_c_cat_T_15)
[216] FIRRTL:189277 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_20 = or(_coh_on_grant_c_cat_T_19, _coh_on_grant_c_cat_T_16)
[217] FIRRTL:189278 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _coh_on_grant_c_cat_T_21 = or(_coh_on_grant_c_cat_T_11, _coh_on_grant_c_cat_T_20)
[218] FIRRTL:189279 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _coh_on_grant_c_cat_T_22 = or(_coh_on_grant_c_cat_T_4, _coh_on_grant_c_cat_T_21)
[219] FIRRTL:189280 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _coh_on_grant_c_cat_T_23 = eq(req.uop.mem_cmd, UInt<1>(0h1))
[220] FIRRTL:189281 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _coh_on_grant_c_cat_T_24 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[221] FIRRTL:189282 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _coh_on_grant_c_cat_T_25 = or(_coh_on_grant_c_cat_T_23, _coh_on_grant_c_cat_T_24)
[222] FIRRTL:189283 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _coh_on_grant_c_cat_T_26 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[223] FIRRTL:189284 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _coh_on_grant_c_cat_T_27 = or(_coh_on_grant_c_cat_T_25, _coh_on_grant_c_cat_T_26)
[224] FIRRTL:189285 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_28 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[225] FIRRTL:189286 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_29 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[226] FIRRTL:189287 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_30 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[227] FIRRTL:189288 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_31 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[228] FIRRTL:189289 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_32 = or(_coh_on_grant_c_cat_T_28, _coh_on_grant_c_cat_T_29)
[229] FIRRTL:189290 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_33 = or(_coh_on_grant_c_cat_T_32, _coh_on_grant_c_cat_T_30)
[230] FIRRTL:189291 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_34 = or(_coh_on_grant_c_cat_T_33, _coh_on_grant_c_cat_T_31)
[231] FIRRTL:189292 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_35 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[232] FIRRTL:189293 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_36 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[233] FIRRTL:189294 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_37 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[234] FIRRTL:189295 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_38 = eq(req.uop.mem_cmd, UInt<4>(0he))
[235] FIRRTL:189296 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _coh_on_grant_c_cat_T_39 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[236] FIRRTL:189297 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_40 = or(_coh_on_grant_c_cat_T_35, _coh_on_grant_c_cat_T_36)
[237] FIRRTL:189298 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_41 = or(_coh_on_grant_c_cat_T_40, _coh_on_grant_c_cat_T_37)
[238] FIRRTL:189299 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_42 = or(_coh_on_grant_c_cat_T_41, _coh_on_grant_c_cat_T_38)
[239] FIRRTL:189300 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _coh_on_grant_c_cat_T_43 = or(_coh_on_grant_c_cat_T_42, _coh_on_grant_c_cat_T_39)
[240] FIRRTL:189301 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _coh_on_grant_c_cat_T_44 = or(_coh_on_grant_c_cat_T_34, _coh_on_grant_c_cat_T_43)
[241] FIRRTL:189302 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _coh_on_grant_c_cat_T_45 = or(_coh_on_grant_c_cat_T_27, _coh_on_grant_c_cat_T_44)
[242] FIRRTL:189303 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _coh_on_grant_c_cat_T_46 = eq(req.uop.mem_cmd, UInt<2>(0h3))
[243] FIRRTL:189304 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _coh_on_grant_c_cat_T_47 = or(_coh_on_grant_c_cat_T_45, _coh_on_grant_c_cat_T_46)
[244] FIRRTL:189305 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _coh_on_grant_c_cat_T_48 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[245] FIRRTL:189306 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _coh_on_grant_c_cat_T_49 = or(_coh_on_grant_c_cat_T_47, _coh_on_grant_c_cat_T_48)
[246] FIRRTL:189307 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node coh_on_grant_c = cat(_coh_on_grant_c_cat_T_22, _coh_on_grant_c_cat_T_49)
[247] FIRRTL:189308 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:18 KIND:node :: node _coh_on_grant_T = cat(coh_on_grant_c, io.mem_grant.bits.param)
[248] FIRRTL:189309 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _coh_on_grant_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[249] FIRRTL:189310 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:86:10 KIND:node :: node _coh_on_grant_T_2 = cat(_coh_on_grant_T_1, UInt<2>(0h1))
[250] FIRRTL:189311 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _coh_on_grant_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[251] FIRRTL:189312 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:87:10 KIND:node :: node _coh_on_grant_T_4 = cat(_coh_on_grant_T_3, UInt<2>(0h0))
[252] FIRRTL:189313 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _coh_on_grant_T_5 = cat(UInt<1>(0h0), UInt<1>(0h1))
[253] FIRRTL:189314 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:88:10 KIND:node :: node _coh_on_grant_T_6 = cat(_coh_on_grant_T_5, UInt<2>(0h0))
[254] FIRRTL:189315 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _coh_on_grant_T_7 = cat(UInt<1>(0h1), UInt<1>(0h1))
[255] FIRRTL:189316 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:89:10 KIND:node :: node _coh_on_grant_T_8 = cat(_coh_on_grant_T_7, UInt<2>(0h0))
[256] FIRRTL:189317 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_9 = eq(_coh_on_grant_T_2, _coh_on_grant_T)
[257] FIRRTL:189318 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_10 = mux(_coh_on_grant_T_9, UInt<2>(0h1), UInt<2>(0h0))
[258] FIRRTL:189319 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_11 = eq(_coh_on_grant_T_4, _coh_on_grant_T)
[259] FIRRTL:189320 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_12 = mux(_coh_on_grant_T_11, UInt<2>(0h2), _coh_on_grant_T_10)
[260] FIRRTL:189321 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_13 = eq(_coh_on_grant_T_6, _coh_on_grant_T)
[261] FIRRTL:189322 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_14 = mux(_coh_on_grant_T_13, UInt<2>(0h2), _coh_on_grant_T_12)
[262] FIRRTL:189323 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_15 = eq(_coh_on_grant_T_8, _coh_on_grant_T)
[263] FIRRTL:189324 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:84:38 KIND:node :: node _coh_on_grant_T_16 = mux(_coh_on_grant_T_15, UInt<2>(0h3), _coh_on_grant_T_14)
[264] FIRRTL:189325 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire coh_on_grant : { state : UInt<2>}
[265] FIRRTL:189326 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect coh_on_grant.state, _coh_on_grant_T_16
[266] FIRRTL:189327 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r1_c_cat_T = eq(req.uop.mem_cmd, UInt<1>(0h1))
[267] FIRRTL:189328 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r1_c_cat_T_1 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[268] FIRRTL:189329 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r1_c_cat_T_2 = or(_r1_c_cat_T, _r1_c_cat_T_1)
[269] FIRRTL:189330 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r1_c_cat_T_3 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[270] FIRRTL:189331 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r1_c_cat_T_4 = or(_r1_c_cat_T_2, _r1_c_cat_T_3)
[271] FIRRTL:189332 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_5 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[272] FIRRTL:189333 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_6 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[273] FIRRTL:189334 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_7 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[274] FIRRTL:189335 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_8 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[275] FIRRTL:189336 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_9 = or(_r1_c_cat_T_5, _r1_c_cat_T_6)
[276] FIRRTL:189337 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_10 = or(_r1_c_cat_T_9, _r1_c_cat_T_7)
[277] FIRRTL:189338 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_11 = or(_r1_c_cat_T_10, _r1_c_cat_T_8)
[278] FIRRTL:189339 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_12 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[279] FIRRTL:189340 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_13 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[280] FIRRTL:189341 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_14 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[281] FIRRTL:189342 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_15 = eq(req.uop.mem_cmd, UInt<4>(0he))
[282] FIRRTL:189343 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_16 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[283] FIRRTL:189344 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_17 = or(_r1_c_cat_T_12, _r1_c_cat_T_13)
[284] FIRRTL:189345 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_18 = or(_r1_c_cat_T_17, _r1_c_cat_T_14)
[285] FIRRTL:189346 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_19 = or(_r1_c_cat_T_18, _r1_c_cat_T_15)
[286] FIRRTL:189347 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_20 = or(_r1_c_cat_T_19, _r1_c_cat_T_16)
[287] FIRRTL:189348 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r1_c_cat_T_21 = or(_r1_c_cat_T_11, _r1_c_cat_T_20)
[288] FIRRTL:189349 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r1_c_cat_T_22 = or(_r1_c_cat_T_4, _r1_c_cat_T_21)
[289] FIRRTL:189350 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r1_c_cat_T_23 = eq(req.uop.mem_cmd, UInt<1>(0h1))
[290] FIRRTL:189351 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r1_c_cat_T_24 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[291] FIRRTL:189352 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r1_c_cat_T_25 = or(_r1_c_cat_T_23, _r1_c_cat_T_24)
[292] FIRRTL:189353 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r1_c_cat_T_26 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[293] FIRRTL:189354 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r1_c_cat_T_27 = or(_r1_c_cat_T_25, _r1_c_cat_T_26)
[294] FIRRTL:189355 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_28 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[295] FIRRTL:189356 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_29 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[296] FIRRTL:189357 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_30 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[297] FIRRTL:189358 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_31 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[298] FIRRTL:189359 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_32 = or(_r1_c_cat_T_28, _r1_c_cat_T_29)
[299] FIRRTL:189360 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_33 = or(_r1_c_cat_T_32, _r1_c_cat_T_30)
[300] FIRRTL:189361 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_34 = or(_r1_c_cat_T_33, _r1_c_cat_T_31)
[301] FIRRTL:189362 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_35 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[302] FIRRTL:189363 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_36 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[303] FIRRTL:189364 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_37 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[304] FIRRTL:189365 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_38 = eq(req.uop.mem_cmd, UInt<4>(0he))
[305] FIRRTL:189366 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r1_c_cat_T_39 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[306] FIRRTL:189367 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_40 = or(_r1_c_cat_T_35, _r1_c_cat_T_36)
[307] FIRRTL:189368 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_41 = or(_r1_c_cat_T_40, _r1_c_cat_T_37)
[308] FIRRTL:189369 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_42 = or(_r1_c_cat_T_41, _r1_c_cat_T_38)
[309] FIRRTL:189370 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r1_c_cat_T_43 = or(_r1_c_cat_T_42, _r1_c_cat_T_39)
[310] FIRRTL:189371 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r1_c_cat_T_44 = or(_r1_c_cat_T_34, _r1_c_cat_T_43)
[311] FIRRTL:189372 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r1_c_cat_T_45 = or(_r1_c_cat_T_27, _r1_c_cat_T_44)
[312] FIRRTL:189373 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _r1_c_cat_T_46 = eq(req.uop.mem_cmd, UInt<2>(0h3))
[313] FIRRTL:189374 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _r1_c_cat_T_47 = or(_r1_c_cat_T_45, _r1_c_cat_T_46)
[314] FIRRTL:189375 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _r1_c_cat_T_48 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[315] FIRRTL:189376 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _r1_c_cat_T_49 = or(_r1_c_cat_T_47, _r1_c_cat_T_48)
[316] FIRRTL:189377 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node r1_c = cat(_r1_c_cat_T_22, _r1_c_cat_T_49)
[317] FIRRTL:189378 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _r1_T = cat(r1_c, new_coh.state)
[318] FIRRTL:189379 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r1_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[319] FIRRTL:189380 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _r1_T_2 = cat(_r1_T_1, UInt<2>(0h3))
[320] FIRRTL:189381 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r1_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[321] FIRRTL:189382 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _r1_T_4 = cat(_r1_T_3, UInt<2>(0h2))
[322] FIRRTL:189383 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r1_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[323] FIRRTL:189384 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _r1_T_6 = cat(_r1_T_5, UInt<2>(0h1))
[324] FIRRTL:189385 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r1_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[325] FIRRTL:189386 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _r1_T_8 = cat(_r1_T_7, UInt<2>(0h3))
[326] FIRRTL:189387 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r1_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[327] FIRRTL:189388 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _r1_T_10 = cat(_r1_T_9, UInt<2>(0h2))
[328] FIRRTL:189389 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r1_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[329] FIRRTL:189390 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _r1_T_12 = cat(_r1_T_11, UInt<2>(0h3))
[330] FIRRTL:189391 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r1_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[331] FIRRTL:189392 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _r1_T_14 = cat(_r1_T_13, UInt<2>(0h2))
[332] FIRRTL:189393 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r1_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[333] FIRRTL:189394 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _r1_T_16 = cat(_r1_T_15, UInt<2>(0h0))
[334] FIRRTL:189395 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r1_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[335] FIRRTL:189396 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _r1_T_18 = cat(_r1_T_17, UInt<2>(0h1))
[336] FIRRTL:189397 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r1_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[337] FIRRTL:189398 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _r1_T_20 = cat(_r1_T_19, UInt<2>(0h0))
[338] FIRRTL:189399 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r1_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[339] FIRRTL:189400 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _r1_T_22 = cat(_r1_T_21, UInt<2>(0h1))
[340] FIRRTL:189401 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r1_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[341] FIRRTL:189402 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _r1_T_24 = cat(_r1_T_23, UInt<2>(0h0))
[342] FIRRTL:189403 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_25 = eq(_r1_T_24, _r1_T)
[343] FIRRTL:189404 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_26 = mux(_r1_T_25, UInt<1>(0h0), UInt<1>(0h0))
[344] FIRRTL:189405 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_27 = mux(_r1_T_25, UInt<2>(0h1), UInt<1>(0h0))
[345] FIRRTL:189406 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_28 = eq(_r1_T_22, _r1_T)
[346] FIRRTL:189407 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_29 = mux(_r1_T_28, UInt<1>(0h0), _r1_T_26)
[347] FIRRTL:189408 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_30 = mux(_r1_T_28, UInt<2>(0h2), _r1_T_27)
[348] FIRRTL:189409 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_31 = eq(_r1_T_20, _r1_T)
[349] FIRRTL:189410 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_32 = mux(_r1_T_31, UInt<1>(0h0), _r1_T_29)
[350] FIRRTL:189411 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_33 = mux(_r1_T_31, UInt<2>(0h1), _r1_T_30)
[351] FIRRTL:189412 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_34 = eq(_r1_T_18, _r1_T)
[352] FIRRTL:189413 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_35 = mux(_r1_T_34, UInt<1>(0h0), _r1_T_32)
[353] FIRRTL:189414 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_36 = mux(_r1_T_34, UInt<2>(0h2), _r1_T_33)
[354] FIRRTL:189415 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_37 = eq(_r1_T_16, _r1_T)
[355] FIRRTL:189416 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_38 = mux(_r1_T_37, UInt<1>(0h0), _r1_T_35)
[356] FIRRTL:189417 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_39 = mux(_r1_T_37, UInt<2>(0h0), _r1_T_36)
[357] FIRRTL:189418 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_40 = eq(_r1_T_14, _r1_T)
[358] FIRRTL:189419 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_41 = mux(_r1_T_40, UInt<1>(0h1), _r1_T_38)
[359] FIRRTL:189420 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_42 = mux(_r1_T_40, UInt<2>(0h3), _r1_T_39)
[360] FIRRTL:189421 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_43 = eq(_r1_T_12, _r1_T)
[361] FIRRTL:189422 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_44 = mux(_r1_T_43, UInt<1>(0h1), _r1_T_41)
[362] FIRRTL:189423 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_45 = mux(_r1_T_43, UInt<2>(0h3), _r1_T_42)
[363] FIRRTL:189424 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_46 = eq(_r1_T_10, _r1_T)
[364] FIRRTL:189425 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_47 = mux(_r1_T_46, UInt<1>(0h1), _r1_T_44)
[365] FIRRTL:189426 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_48 = mux(_r1_T_46, UInt<2>(0h2), _r1_T_45)
[366] FIRRTL:189427 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_49 = eq(_r1_T_8, _r1_T)
[367] FIRRTL:189428 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_50 = mux(_r1_T_49, UInt<1>(0h1), _r1_T_47)
[368] FIRRTL:189429 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_51 = mux(_r1_T_49, UInt<2>(0h3), _r1_T_48)
[369] FIRRTL:189430 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_52 = eq(_r1_T_6, _r1_T)
[370] FIRRTL:189431 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_53 = mux(_r1_T_52, UInt<1>(0h1), _r1_T_50)
[371] FIRRTL:189432 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_54 = mux(_r1_T_52, UInt<2>(0h1), _r1_T_51)
[372] FIRRTL:189433 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_55 = eq(_r1_T_4, _r1_T)
[373] FIRRTL:189434 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r1_T_56 = mux(_r1_T_55, UInt<1>(0h1), _r1_T_53)
[374] FIRRTL:189435 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r1_T_57 = mux(_r1_T_55, UInt<2>(0h2), _r1_T_54)
[375] FIRRTL:189436 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r1_T_58 = eq(_r1_T_2, _r1_T)
[376] FIRRTL:189437 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node r1_1 = mux(_r1_T_58, UInt<1>(0h1), _r1_T_56)
[377] FIRRTL:189438 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node r1_2 = mux(_r1_T_58, UInt<2>(0h3), _r1_T_57)
[378] FIRRTL:189439 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r2_c_cat_T = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[379] FIRRTL:189440 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r2_c_cat_T_1 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[380] FIRRTL:189441 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r2_c_cat_T_2 = or(_r2_c_cat_T, _r2_c_cat_T_1)
[381] FIRRTL:189442 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r2_c_cat_T_3 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[382] FIRRTL:189443 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r2_c_cat_T_4 = or(_r2_c_cat_T_2, _r2_c_cat_T_3)
[383] FIRRTL:189444 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_5 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[384] FIRRTL:189445 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_6 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[385] FIRRTL:189446 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_7 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[386] FIRRTL:189447 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_8 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[387] FIRRTL:189448 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_9 = or(_r2_c_cat_T_5, _r2_c_cat_T_6)
[388] FIRRTL:189449 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_10 = or(_r2_c_cat_T_9, _r2_c_cat_T_7)
[389] FIRRTL:189450 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_11 = or(_r2_c_cat_T_10, _r2_c_cat_T_8)
[390] FIRRTL:189451 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_12 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[391] FIRRTL:189452 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_13 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[392] FIRRTL:189453 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_14 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[393] FIRRTL:189454 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_15 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[394] FIRRTL:189455 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_16 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[395] FIRRTL:189456 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_17 = or(_r2_c_cat_T_12, _r2_c_cat_T_13)
[396] FIRRTL:189457 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_18 = or(_r2_c_cat_T_17, _r2_c_cat_T_14)
[397] FIRRTL:189458 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_19 = or(_r2_c_cat_T_18, _r2_c_cat_T_15)
[398] FIRRTL:189459 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_20 = or(_r2_c_cat_T_19, _r2_c_cat_T_16)
[399] FIRRTL:189460 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r2_c_cat_T_21 = or(_r2_c_cat_T_11, _r2_c_cat_T_20)
[400] FIRRTL:189461 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r2_c_cat_T_22 = or(_r2_c_cat_T_4, _r2_c_cat_T_21)
[401] FIRRTL:189462 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r2_c_cat_T_23 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[402] FIRRTL:189463 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r2_c_cat_T_24 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[403] FIRRTL:189464 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r2_c_cat_T_25 = or(_r2_c_cat_T_23, _r2_c_cat_T_24)
[404] FIRRTL:189465 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r2_c_cat_T_26 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[405] FIRRTL:189466 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r2_c_cat_T_27 = or(_r2_c_cat_T_25, _r2_c_cat_T_26)
[406] FIRRTL:189467 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_28 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[407] FIRRTL:189468 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_29 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[408] FIRRTL:189469 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_30 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[409] FIRRTL:189470 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_31 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[410] FIRRTL:189471 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_32 = or(_r2_c_cat_T_28, _r2_c_cat_T_29)
[411] FIRRTL:189472 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_33 = or(_r2_c_cat_T_32, _r2_c_cat_T_30)
[412] FIRRTL:189473 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_34 = or(_r2_c_cat_T_33, _r2_c_cat_T_31)
[413] FIRRTL:189474 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_35 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[414] FIRRTL:189475 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_36 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[415] FIRRTL:189476 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_37 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[416] FIRRTL:189477 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_38 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[417] FIRRTL:189478 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r2_c_cat_T_39 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[418] FIRRTL:189479 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_40 = or(_r2_c_cat_T_35, _r2_c_cat_T_36)
[419] FIRRTL:189480 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_41 = or(_r2_c_cat_T_40, _r2_c_cat_T_37)
[420] FIRRTL:189481 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_42 = or(_r2_c_cat_T_41, _r2_c_cat_T_38)
[421] FIRRTL:189482 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r2_c_cat_T_43 = or(_r2_c_cat_T_42, _r2_c_cat_T_39)
[422] FIRRTL:189483 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r2_c_cat_T_44 = or(_r2_c_cat_T_34, _r2_c_cat_T_43)
[423] FIRRTL:189484 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r2_c_cat_T_45 = or(_r2_c_cat_T_27, _r2_c_cat_T_44)
[424] FIRRTL:189485 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _r2_c_cat_T_46 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[425] FIRRTL:189486 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _r2_c_cat_T_47 = or(_r2_c_cat_T_45, _r2_c_cat_T_46)
[426] FIRRTL:189487 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _r2_c_cat_T_48 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[427] FIRRTL:189488 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _r2_c_cat_T_49 = or(_r2_c_cat_T_47, _r2_c_cat_T_48)
[428] FIRRTL:189489 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node r2_c = cat(_r2_c_cat_T_22, _r2_c_cat_T_49)
[429] FIRRTL:189490 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _r2_T = cat(r2_c, new_coh.state)
[430] FIRRTL:189491 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r2_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[431] FIRRTL:189492 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _r2_T_2 = cat(_r2_T_1, UInt<2>(0h3))
[432] FIRRTL:189493 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r2_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[433] FIRRTL:189494 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _r2_T_4 = cat(_r2_T_3, UInt<2>(0h2))
[434] FIRRTL:189495 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r2_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[435] FIRRTL:189496 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _r2_T_6 = cat(_r2_T_5, UInt<2>(0h1))
[436] FIRRTL:189497 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r2_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[437] FIRRTL:189498 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _r2_T_8 = cat(_r2_T_7, UInt<2>(0h3))
[438] FIRRTL:189499 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r2_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[439] FIRRTL:189500 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _r2_T_10 = cat(_r2_T_9, UInt<2>(0h2))
[440] FIRRTL:189501 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r2_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[441] FIRRTL:189502 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _r2_T_12 = cat(_r2_T_11, UInt<2>(0h3))
[442] FIRRTL:189503 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r2_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[443] FIRRTL:189504 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _r2_T_14 = cat(_r2_T_13, UInt<2>(0h2))
[444] FIRRTL:189505 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r2_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[445] FIRRTL:189506 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _r2_T_16 = cat(_r2_T_15, UInt<2>(0h0))
[446] FIRRTL:189507 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r2_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[447] FIRRTL:189508 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _r2_T_18 = cat(_r2_T_17, UInt<2>(0h1))
[448] FIRRTL:189509 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r2_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[449] FIRRTL:189510 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _r2_T_20 = cat(_r2_T_19, UInt<2>(0h0))
[450] FIRRTL:189511 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r2_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[451] FIRRTL:189512 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _r2_T_22 = cat(_r2_T_21, UInt<2>(0h1))
[452] FIRRTL:189513 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r2_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[453] FIRRTL:189514 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _r2_T_24 = cat(_r2_T_23, UInt<2>(0h0))
[454] FIRRTL:189515 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_25 = eq(_r2_T_24, _r2_T)
[455] FIRRTL:189516 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_26 = mux(_r2_T_25, UInt<1>(0h0), UInt<1>(0h0))
[456] FIRRTL:189517 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_27 = mux(_r2_T_25, UInt<2>(0h1), UInt<1>(0h0))
[457] FIRRTL:189518 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_28 = eq(_r2_T_22, _r2_T)
[458] FIRRTL:189519 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_29 = mux(_r2_T_28, UInt<1>(0h0), _r2_T_26)
[459] FIRRTL:189520 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_30 = mux(_r2_T_28, UInt<2>(0h2), _r2_T_27)
[460] FIRRTL:189521 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_31 = eq(_r2_T_20, _r2_T)
[461] FIRRTL:189522 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_32 = mux(_r2_T_31, UInt<1>(0h0), _r2_T_29)
[462] FIRRTL:189523 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_33 = mux(_r2_T_31, UInt<2>(0h1), _r2_T_30)
[463] FIRRTL:189524 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_34 = eq(_r2_T_18, _r2_T)
[464] FIRRTL:189525 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_35 = mux(_r2_T_34, UInt<1>(0h0), _r2_T_32)
[465] FIRRTL:189526 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_36 = mux(_r2_T_34, UInt<2>(0h2), _r2_T_33)
[466] FIRRTL:189527 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_37 = eq(_r2_T_16, _r2_T)
[467] FIRRTL:189528 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_38 = mux(_r2_T_37, UInt<1>(0h0), _r2_T_35)
[468] FIRRTL:189529 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_39 = mux(_r2_T_37, UInt<2>(0h0), _r2_T_36)
[469] FIRRTL:189530 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_40 = eq(_r2_T_14, _r2_T)
[470] FIRRTL:189531 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_41 = mux(_r2_T_40, UInt<1>(0h1), _r2_T_38)
[471] FIRRTL:189532 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_42 = mux(_r2_T_40, UInt<2>(0h3), _r2_T_39)
[472] FIRRTL:189533 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_43 = eq(_r2_T_12, _r2_T)
[473] FIRRTL:189534 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_44 = mux(_r2_T_43, UInt<1>(0h1), _r2_T_41)
[474] FIRRTL:189535 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_45 = mux(_r2_T_43, UInt<2>(0h3), _r2_T_42)
[475] FIRRTL:189536 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_46 = eq(_r2_T_10, _r2_T)
[476] FIRRTL:189537 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_47 = mux(_r2_T_46, UInt<1>(0h1), _r2_T_44)
[477] FIRRTL:189538 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_48 = mux(_r2_T_46, UInt<2>(0h2), _r2_T_45)
[478] FIRRTL:189539 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_49 = eq(_r2_T_8, _r2_T)
[479] FIRRTL:189540 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_50 = mux(_r2_T_49, UInt<1>(0h1), _r2_T_47)
[480] FIRRTL:189541 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_51 = mux(_r2_T_49, UInt<2>(0h3), _r2_T_48)
[481] FIRRTL:189542 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_52 = eq(_r2_T_6, _r2_T)
[482] FIRRTL:189543 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_53 = mux(_r2_T_52, UInt<1>(0h1), _r2_T_50)
[483] FIRRTL:189544 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_54 = mux(_r2_T_52, UInt<2>(0h1), _r2_T_51)
[484] FIRRTL:189545 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_55 = eq(_r2_T_4, _r2_T)
[485] FIRRTL:189546 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r2_T_56 = mux(_r2_T_55, UInt<1>(0h1), _r2_T_53)
[486] FIRRTL:189547 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r2_T_57 = mux(_r2_T_55, UInt<2>(0h2), _r2_T_54)
[487] FIRRTL:189548 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r2_T_58 = eq(_r2_T_2, _r2_T)
[488] FIRRTL:189549 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node r2_1 = mux(_r2_T_58, UInt<1>(0h1), _r2_T_56)
[489] FIRRTL:189550 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node r2_2 = mux(_r2_T_58, UInt<2>(0h3), _r2_T_57)
[490] FIRRTL:189551 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _needs_second_acq_T = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[491] FIRRTL:189552 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _needs_second_acq_T_1 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[492] FIRRTL:189553 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _needs_second_acq_T_2 = or(_needs_second_acq_T, _needs_second_acq_T_1)
[493] FIRRTL:189554 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _needs_second_acq_T_3 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[494] FIRRTL:189555 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _needs_second_acq_T_4 = or(_needs_second_acq_T_2, _needs_second_acq_T_3)
[495] FIRRTL:189556 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_5 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[496] FIRRTL:189557 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_6 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[497] FIRRTL:189558 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_7 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[498] FIRRTL:189559 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_8 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[499] FIRRTL:189560 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_9 = or(_needs_second_acq_T_5, _needs_second_acq_T_6)
[500] FIRRTL:189561 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_10 = or(_needs_second_acq_T_9, _needs_second_acq_T_7)
[501] FIRRTL:189562 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_11 = or(_needs_second_acq_T_10, _needs_second_acq_T_8)
[502] FIRRTL:189563 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_12 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[503] FIRRTL:189564 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_13 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[504] FIRRTL:189565 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_14 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[505] FIRRTL:189566 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_15 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[506] FIRRTL:189567 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_16 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[507] FIRRTL:189568 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_17 = or(_needs_second_acq_T_12, _needs_second_acq_T_13)
[508] FIRRTL:189569 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_18 = or(_needs_second_acq_T_17, _needs_second_acq_T_14)
[509] FIRRTL:189570 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_19 = or(_needs_second_acq_T_18, _needs_second_acq_T_15)
[510] FIRRTL:189571 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_20 = or(_needs_second_acq_T_19, _needs_second_acq_T_16)
[511] FIRRTL:189572 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _needs_second_acq_T_21 = or(_needs_second_acq_T_11, _needs_second_acq_T_20)
[512] FIRRTL:189573 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _needs_second_acq_T_22 = or(_needs_second_acq_T_4, _needs_second_acq_T_21)
[513] FIRRTL:189574 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _needs_second_acq_T_23 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[514] FIRRTL:189575 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _needs_second_acq_T_24 = or(_needs_second_acq_T_22, _needs_second_acq_T_23)
[515] FIRRTL:189576 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _needs_second_acq_T_25 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[516] FIRRTL:189577 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _needs_second_acq_T_26 = or(_needs_second_acq_T_24, _needs_second_acq_T_25)
[517] FIRRTL:189578 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _needs_second_acq_T_27 = eq(req.uop.mem_cmd, UInt<1>(0h1))
[518] FIRRTL:189579 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _needs_second_acq_T_28 = eq(req.uop.mem_cmd, UInt<5>(0h11))
[519] FIRRTL:189580 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _needs_second_acq_T_29 = or(_needs_second_acq_T_27, _needs_second_acq_T_28)
[520] FIRRTL:189581 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _needs_second_acq_T_30 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[521] FIRRTL:189582 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _needs_second_acq_T_31 = or(_needs_second_acq_T_29, _needs_second_acq_T_30)
[522] FIRRTL:189583 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_32 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[523] FIRRTL:189584 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_33 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[524] FIRRTL:189585 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_34 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[525] FIRRTL:189586 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_35 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[526] FIRRTL:189587 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_36 = or(_needs_second_acq_T_32, _needs_second_acq_T_33)
[527] FIRRTL:189588 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_37 = or(_needs_second_acq_T_36, _needs_second_acq_T_34)
[528] FIRRTL:189589 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_38 = or(_needs_second_acq_T_37, _needs_second_acq_T_35)
[529] FIRRTL:189590 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_39 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[530] FIRRTL:189591 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_40 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[531] FIRRTL:189592 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_41 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[532] FIRRTL:189593 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_42 = eq(req.uop.mem_cmd, UInt<4>(0he))
[533] FIRRTL:189594 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _needs_second_acq_T_43 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[534] FIRRTL:189595 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_44 = or(_needs_second_acq_T_39, _needs_second_acq_T_40)
[535] FIRRTL:189596 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_45 = or(_needs_second_acq_T_44, _needs_second_acq_T_41)
[536] FIRRTL:189597 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_46 = or(_needs_second_acq_T_45, _needs_second_acq_T_42)
[537] FIRRTL:189598 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _needs_second_acq_T_47 = or(_needs_second_acq_T_46, _needs_second_acq_T_43)
[538] FIRRTL:189599 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _needs_second_acq_T_48 = or(_needs_second_acq_T_38, _needs_second_acq_T_47)
[539] FIRRTL:189600 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _needs_second_acq_T_49 = or(_needs_second_acq_T_31, _needs_second_acq_T_48)
[540] FIRRTL:189601 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _needs_second_acq_T_50 = eq(req.uop.mem_cmd, UInt<2>(0h3))
[541] FIRRTL:189602 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _needs_second_acq_T_51 = or(_needs_second_acq_T_49, _needs_second_acq_T_50)
[542] FIRRTL:189603 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _needs_second_acq_T_52 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[543] FIRRTL:189604 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _needs_second_acq_T_53 = or(_needs_second_acq_T_51, _needs_second_acq_T_52)
[544] FIRRTL:189605 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:104:57 KIND:node :: node _needs_second_acq_T_54 = eq(_needs_second_acq_T_53, UInt<1>(0h0))
[545] FIRRTL:189606 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:104:54 KIND:node :: node cmd_requires_second_acquire = and(_needs_second_acq_T_26, _needs_second_acq_T_54)
[546] FIRRTL:189607 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:105:27 KIND:node :: node is_hit_again = and(r1_1, r2_1)
[547] FIRRTL:189608 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _dirties_cat_T = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[548] FIRRTL:189609 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _dirties_cat_T_1 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[549] FIRRTL:189610 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _dirties_cat_T_2 = or(_dirties_cat_T, _dirties_cat_T_1)
[550] FIRRTL:189611 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _dirties_cat_T_3 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[551] FIRRTL:189612 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _dirties_cat_T_4 = or(_dirties_cat_T_2, _dirties_cat_T_3)
[552] FIRRTL:189613 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_5 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[553] FIRRTL:189614 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_6 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[554] FIRRTL:189615 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_7 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[555] FIRRTL:189616 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_8 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[556] FIRRTL:189617 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_9 = or(_dirties_cat_T_5, _dirties_cat_T_6)
[557] FIRRTL:189618 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_10 = or(_dirties_cat_T_9, _dirties_cat_T_7)
[558] FIRRTL:189619 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_11 = or(_dirties_cat_T_10, _dirties_cat_T_8)
[559] FIRRTL:189620 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_12 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[560] FIRRTL:189621 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_13 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[561] FIRRTL:189622 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_14 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[562] FIRRTL:189623 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_15 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[563] FIRRTL:189624 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_16 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[564] FIRRTL:189625 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_17 = or(_dirties_cat_T_12, _dirties_cat_T_13)
[565] FIRRTL:189626 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_18 = or(_dirties_cat_T_17, _dirties_cat_T_14)
[566] FIRRTL:189627 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_19 = or(_dirties_cat_T_18, _dirties_cat_T_15)
[567] FIRRTL:189628 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_20 = or(_dirties_cat_T_19, _dirties_cat_T_16)
[568] FIRRTL:189629 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _dirties_cat_T_21 = or(_dirties_cat_T_11, _dirties_cat_T_20)
[569] FIRRTL:189630 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _dirties_cat_T_22 = or(_dirties_cat_T_4, _dirties_cat_T_21)
[570] FIRRTL:189631 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _dirties_cat_T_23 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[571] FIRRTL:189632 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _dirties_cat_T_24 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[572] FIRRTL:189633 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _dirties_cat_T_25 = or(_dirties_cat_T_23, _dirties_cat_T_24)
[573] FIRRTL:189634 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _dirties_cat_T_26 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[574] FIRRTL:189635 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _dirties_cat_T_27 = or(_dirties_cat_T_25, _dirties_cat_T_26)
[575] FIRRTL:189636 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_28 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[576] FIRRTL:189637 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_29 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[577] FIRRTL:189638 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_30 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[578] FIRRTL:189639 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_31 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[579] FIRRTL:189640 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_32 = or(_dirties_cat_T_28, _dirties_cat_T_29)
[580] FIRRTL:189641 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_33 = or(_dirties_cat_T_32, _dirties_cat_T_30)
[581] FIRRTL:189642 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_34 = or(_dirties_cat_T_33, _dirties_cat_T_31)
[582] FIRRTL:189643 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_35 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[583] FIRRTL:189644 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_36 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[584] FIRRTL:189645 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_37 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[585] FIRRTL:189646 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_38 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[586] FIRRTL:189647 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _dirties_cat_T_39 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[587] FIRRTL:189648 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_40 = or(_dirties_cat_T_35, _dirties_cat_T_36)
[588] FIRRTL:189649 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_41 = or(_dirties_cat_T_40, _dirties_cat_T_37)
[589] FIRRTL:189650 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_42 = or(_dirties_cat_T_41, _dirties_cat_T_38)
[590] FIRRTL:189651 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _dirties_cat_T_43 = or(_dirties_cat_T_42, _dirties_cat_T_39)
[591] FIRRTL:189652 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _dirties_cat_T_44 = or(_dirties_cat_T_34, _dirties_cat_T_43)
[592] FIRRTL:189653 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _dirties_cat_T_45 = or(_dirties_cat_T_27, _dirties_cat_T_44)
[593] FIRRTL:189654 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _dirties_cat_T_46 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[594] FIRRTL:189655 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _dirties_cat_T_47 = or(_dirties_cat_T_45, _dirties_cat_T_46)
[595] FIRRTL:189656 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _dirties_cat_T_48 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[596] FIRRTL:189657 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _dirties_cat_T_49 = or(_dirties_cat_T_47, _dirties_cat_T_48)
[597] FIRRTL:189658 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node dirties_cat = cat(_dirties_cat_T_22, _dirties_cat_T_49)
[598] FIRRTL:189659 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _dirties_T = cat(UInt<1>(0h1), UInt<1>(0h1))
[599] FIRRTL:189660 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:106:42 KIND:node :: node dirties = eq(dirties_cat, _dirties_T)
[600] FIRRTL:189661 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:107:33 KIND:node :: node biggest_grow_param = mux(dirties, r2_2, r1_2)
[601] FIRRTL:189662 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire dirtier_coh : { state : UInt<2>}
[602] FIRRTL:189663 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect dirtier_coh.state, biggest_grow_param
[603] FIRRTL:189664 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:109:27 KIND:node :: node dirtier_cmd = mux(dirties, io.req.uop.mem_cmd, req.uop.mem_cmd)
[604] FIRRTL:189665 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T = and(io.mem_grant.ready, io.mem_grant.valid)
[605] FIRRTL:189666 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _r_beats1_decode_T = dshl(UInt<12>(0hfff), io.mem_grant.bits.size)
[606] FIRRTL:189667 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _r_beats1_decode_T_1 = bits(_r_beats1_decode_T, 11, 0)
[607] FIRRTL:189668 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _r_beats1_decode_T_2 = not(_r_beats1_decode_T_1)
[608] FIRRTL:189669 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node r_beats1_decode = shr(_r_beats1_decode_T_2, 3)
[609] FIRRTL:189670 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:106:36 KIND:node :: node r_beats1_opdata = bits(io.mem_grant.bits.opcode, 0, 0)
[610] FIRRTL:189671 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node r_beats1 = mux(r_beats1_opdata, r_beats1_decode, UInt<1>(0h0))
[611] FIRRTL:189672 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:229:27 KIND:regreset :: regreset r_counter : UInt<9>, clock, reset, UInt<9>(0h0)
[612] FIRRTL:189673 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node _r_counter1_T = sub(r_counter, UInt<1>(0h1))
[613] FIRRTL:189674 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node r_counter1 = tail(_r_counter1_T, 1)
[614] FIRRTL:189675 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:231:25 KIND:node :: node r_1_1 = eq(r_counter, UInt<1>(0h0))
[615] FIRRTL:189676 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:25 KIND:node :: node _r_last_T = eq(r_counter, UInt<1>(0h1))
[616] FIRRTL:189677 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:43 KIND:node :: node _r_last_T_1 = eq(r_beats1, UInt<1>(0h0))
[617] FIRRTL:189678 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:33 KIND:node :: node r_2 = or(_r_last_T, _r_last_T_1)
[618] FIRRTL:189679 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:233:22 KIND:node :: node refill_done = and(r_2, _T)
[619] FIRRTL:189680 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:27 KIND:node :: node _r_count_T = not(r_counter1)
[620] FIRRTL:189681 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:25 KIND:node :: node r_4 = and(r_beats1, _r_count_T)
[621] FIRRTL:189682 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:235:17 KIND:when :: when _T :
[622] FIRRTL:189683 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:21 KIND:node :: node _r_counter_T = mux(r_1_1, r_beats1, r_counter1)
[623] FIRRTL:189684 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:15 KIND:connect :: connect r_counter, _r_counter_T
[624] FIRRTL:189685 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:269:29 KIND:node :: node refill_address_inc = shl(r_4, 3)
[625] FIRRTL:189686 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:125:18 KIND:node :: node _sec_rdy_T = eq(cmd_requires_second_acquire, UInt<1>(0h0))
[626] FIRRTL:189687 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:125:50 KIND:node :: node _sec_rdy_T_1 = eq(io.req_is_probe, UInt<1>(0h0))
[627] FIRRTL:189688 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:125:47 KIND:node :: node _sec_rdy_T_2 = and(_sec_rdy_T, _sec_rdy_T_1)
[628] FIRRTL:189689 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sec_rdy_T_3 = eq(state, UInt<5>(0h0))
[629] FIRRTL:189690 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sec_rdy_T_4 = eq(state, UInt<5>(0hd))
[630] FIRRTL:189691 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sec_rdy_T_5 = eq(state, UInt<5>(0he))
[631] FIRRTL:189692 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sec_rdy_T_6 = eq(state, UInt<5>(0hf))
[632] FIRRTL:189693 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sec_rdy_T_7 = or(_sec_rdy_T_3, _sec_rdy_T_4)
[633] FIRRTL:189694 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sec_rdy_T_8 = or(_sec_rdy_T_7, _sec_rdy_T_5)
[634] FIRRTL:189695 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sec_rdy_T_9 = or(_sec_rdy_T_8, _sec_rdy_T_6)
[635] FIRRTL:189696 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:126:18 KIND:node :: node _sec_rdy_T_10 = eq(_sec_rdy_T_9, UInt<1>(0h0))
[636] FIRRTL:189697 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:125:67 KIND:node :: node sec_rdy = and(_sec_rdy_T_2, _sec_rdy_T_10)
[637] FIRRTL:189698 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:128:19 KIND:structural :: inst rpq of BranchKillableQueue_1
[638] FIRRTL:189699 SRC:<no-source-locator> KIND:connect :: connect rpq.clock, clock
[639] FIRRTL:189700 SRC:<no-source-locator> KIND:connect :: connect rpq.reset, reset
[640] FIRRTL:189701 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.target_offset, io.brupdate.b2.target_offset
[641] FIRRTL:189702 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.jalr_target, io.brupdate.b2.jalr_target
[642] FIRRTL:189703 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.pc_sel, io.brupdate.b2.pc_sel
[643] FIRRTL:189704 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.cfi_type, io.brupdate.b2.cfi_type
[644] FIRRTL:189705 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.taken, io.brupdate.b2.taken
[645] FIRRTL:189706 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.mispredict, io.brupdate.b2.mispredict
[646] FIRRTL:189707 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.debug_tsrc, io.brupdate.b2.uop.debug_tsrc
[647] FIRRTL:189708 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.debug_fsrc, io.brupdate.b2.uop.debug_fsrc
[648] FIRRTL:189709 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.bp_xcpt_if, io.brupdate.b2.uop.bp_xcpt_if
[649] FIRRTL:189710 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.bp_debug_if, io.brupdate.b2.uop.bp_debug_if
[650] FIRRTL:189711 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.xcpt_ma_if, io.brupdate.b2.uop.xcpt_ma_if
[651] FIRRTL:189712 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.xcpt_ae_if, io.brupdate.b2.uop.xcpt_ae_if
[652] FIRRTL:189713 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.xcpt_pf_if, io.brupdate.b2.uop.xcpt_pf_if
[653] FIRRTL:189714 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_typ, io.brupdate.b2.uop.fp_typ
[654] FIRRTL:189715 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_rm, io.brupdate.b2.uop.fp_rm
[655] FIRRTL:189716 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_val, io.brupdate.b2.uop.fp_val
[656] FIRRTL:189717 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fcn_op, io.brupdate.b2.uop.fcn_op
[657] FIRRTL:189718 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fcn_dw, io.brupdate.b2.uop.fcn_dw
[658] FIRRTL:189719 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.frs3_en, io.brupdate.b2.uop.frs3_en
[659] FIRRTL:189720 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.lrs2_rtype, io.brupdate.b2.uop.lrs2_rtype
[660] FIRRTL:189721 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.lrs1_rtype, io.brupdate.b2.uop.lrs1_rtype
[661] FIRRTL:189722 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.dst_rtype, io.brupdate.b2.uop.dst_rtype
[662] FIRRTL:189723 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.lrs3, io.brupdate.b2.uop.lrs3
[663] FIRRTL:189724 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.lrs2, io.brupdate.b2.uop.lrs2
[664] FIRRTL:189725 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.lrs1, io.brupdate.b2.uop.lrs1
[665] FIRRTL:189726 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ldst, io.brupdate.b2.uop.ldst
[666] FIRRTL:189727 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ldst_is_rs1, io.brupdate.b2.uop.ldst_is_rs1
[667] FIRRTL:189728 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.csr_cmd, io.brupdate.b2.uop.csr_cmd
[668] FIRRTL:189729 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.flush_on_commit, io.brupdate.b2.uop.flush_on_commit
[669] FIRRTL:189730 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_unique, io.brupdate.b2.uop.is_unique
[670] FIRRTL:189731 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.uses_stq, io.brupdate.b2.uop.uses_stq
[671] FIRRTL:189732 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.uses_ldq, io.brupdate.b2.uop.uses_ldq
[672] FIRRTL:189733 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.mem_signed, io.brupdate.b2.uop.mem_signed
[673] FIRRTL:189734 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.mem_size, io.brupdate.b2.uop.mem_size
[674] FIRRTL:189735 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.mem_cmd, io.brupdate.b2.uop.mem_cmd
[675] FIRRTL:189736 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.exc_cause, io.brupdate.b2.uop.exc_cause
[676] FIRRTL:189737 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.exception, io.brupdate.b2.uop.exception
[677] FIRRTL:189738 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.stale_pdst, io.brupdate.b2.uop.stale_pdst
[678] FIRRTL:189739 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ppred_busy, io.brupdate.b2.uop.ppred_busy
[679] FIRRTL:189740 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs3_busy, io.brupdate.b2.uop.prs3_busy
[680] FIRRTL:189741 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs2_busy, io.brupdate.b2.uop.prs2_busy
[681] FIRRTL:189742 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs1_busy, io.brupdate.b2.uop.prs1_busy
[682] FIRRTL:189743 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ppred, io.brupdate.b2.uop.ppred
[683] FIRRTL:189744 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs3, io.brupdate.b2.uop.prs3
[684] FIRRTL:189745 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs2, io.brupdate.b2.uop.prs2
[685] FIRRTL:189746 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.prs1, io.brupdate.b2.uop.prs1
[686] FIRRTL:189747 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.pdst, io.brupdate.b2.uop.pdst
[687] FIRRTL:189748 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.rxq_idx, io.brupdate.b2.uop.rxq_idx
[688] FIRRTL:189749 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.stq_idx, io.brupdate.b2.uop.stq_idx
[689] FIRRTL:189750 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ldq_idx, io.brupdate.b2.uop.ldq_idx
[690] FIRRTL:189751 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.rob_idx, io.brupdate.b2.uop.rob_idx
[691] FIRRTL:189752 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.vec, io.brupdate.b2.uop.fp_ctrl.vec
[692] FIRRTL:189753 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.wflags, io.brupdate.b2.uop.fp_ctrl.wflags
[693] FIRRTL:189754 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.sqrt, io.brupdate.b2.uop.fp_ctrl.sqrt
[694] FIRRTL:189755 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.div, io.brupdate.b2.uop.fp_ctrl.div
[695] FIRRTL:189756 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.fma, io.brupdate.b2.uop.fp_ctrl.fma
[696] FIRRTL:189757 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.brupdate.b2.uop.fp_ctrl.fastpipe
[697] FIRRTL:189758 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.toint, io.brupdate.b2.uop.fp_ctrl.toint
[698] FIRRTL:189759 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.fromint, io.brupdate.b2.uop.fp_ctrl.fromint
[699] FIRRTL:189760 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.brupdate.b2.uop.fp_ctrl.typeTagOut
[700] FIRRTL:189761 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.brupdate.b2.uop.fp_ctrl.typeTagIn
[701] FIRRTL:189762 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.swap23, io.brupdate.b2.uop.fp_ctrl.swap23
[702] FIRRTL:189763 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.swap12, io.brupdate.b2.uop.fp_ctrl.swap12
[703] FIRRTL:189764 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.ren3, io.brupdate.b2.uop.fp_ctrl.ren3
[704] FIRRTL:189765 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.ren2, io.brupdate.b2.uop.fp_ctrl.ren2
[705] FIRRTL:189766 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.ren1, io.brupdate.b2.uop.fp_ctrl.ren1
[706] FIRRTL:189767 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.wen, io.brupdate.b2.uop.fp_ctrl.wen
[707] FIRRTL:189768 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fp_ctrl.ldst, io.brupdate.b2.uop.fp_ctrl.ldst
[708] FIRRTL:189769 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.op2_sel, io.brupdate.b2.uop.op2_sel
[709] FIRRTL:189770 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.op1_sel, io.brupdate.b2.uop.op1_sel
[710] FIRRTL:189771 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.imm_packed, io.brupdate.b2.uop.imm_packed
[711] FIRRTL:189772 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.pimm, io.brupdate.b2.uop.pimm
[712] FIRRTL:189773 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.imm_sel, io.brupdate.b2.uop.imm_sel
[713] FIRRTL:189774 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.imm_rename, io.brupdate.b2.uop.imm_rename
[714] FIRRTL:189775 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.taken, io.brupdate.b2.uop.taken
[715] FIRRTL:189776 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.pc_lob, io.brupdate.b2.uop.pc_lob
[716] FIRRTL:189777 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.edge_inst, io.brupdate.b2.uop.edge_inst
[717] FIRRTL:189778 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.ftq_idx, io.brupdate.b2.uop.ftq_idx
[718] FIRRTL:189779 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_mov, io.brupdate.b2.uop.is_mov
[719] FIRRTL:189780 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_rocc, io.brupdate.b2.uop.is_rocc
[720] FIRRTL:189781 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_sys_pc2epc, io.brupdate.b2.uop.is_sys_pc2epc
[721] FIRRTL:189782 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_eret, io.brupdate.b2.uop.is_eret
[722] FIRRTL:189783 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_amo, io.brupdate.b2.uop.is_amo
[723] FIRRTL:189784 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_sfence, io.brupdate.b2.uop.is_sfence
[724] FIRRTL:189785 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_fencei, io.brupdate.b2.uop.is_fencei
[725] FIRRTL:189786 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_fence, io.brupdate.b2.uop.is_fence
[726] FIRRTL:189787 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_sfb, io.brupdate.b2.uop.is_sfb
[727] FIRRTL:189788 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.br_type, io.brupdate.b2.uop.br_type
[728] FIRRTL:189789 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.br_tag, io.brupdate.b2.uop.br_tag
[729] FIRRTL:189790 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.br_mask, io.brupdate.b2.uop.br_mask
[730] FIRRTL:189791 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.dis_col_sel, io.brupdate.b2.uop.dis_col_sel
[731] FIRRTL:189792 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_p3_bypass_hint, io.brupdate.b2.uop.iw_p3_bypass_hint
[732] FIRRTL:189793 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_p2_bypass_hint, io.brupdate.b2.uop.iw_p2_bypass_hint
[733] FIRRTL:189794 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_p1_bypass_hint, io.brupdate.b2.uop.iw_p1_bypass_hint
[734] FIRRTL:189795 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_p2_speculative_child, io.brupdate.b2.uop.iw_p2_speculative_child
[735] FIRRTL:189796 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_p1_speculative_child, io.brupdate.b2.uop.iw_p1_speculative_child
[736] FIRRTL:189797 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_issued_partial_dgen, io.brupdate.b2.uop.iw_issued_partial_dgen
[737] FIRRTL:189798 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_issued_partial_agen, io.brupdate.b2.uop.iw_issued_partial_agen
[738] FIRRTL:189799 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iw_issued, io.brupdate.b2.uop.iw_issued
[739] FIRRTL:189800 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[0], io.brupdate.b2.uop.fu_code[0]
[740] FIRRTL:189801 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[1], io.brupdate.b2.uop.fu_code[1]
[741] FIRRTL:189802 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[2], io.brupdate.b2.uop.fu_code[2]
[742] FIRRTL:189803 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[3], io.brupdate.b2.uop.fu_code[3]
[743] FIRRTL:189804 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[4], io.brupdate.b2.uop.fu_code[4]
[744] FIRRTL:189805 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[5], io.brupdate.b2.uop.fu_code[5]
[745] FIRRTL:189806 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[6], io.brupdate.b2.uop.fu_code[6]
[746] FIRRTL:189807 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[7], io.brupdate.b2.uop.fu_code[7]
[747] FIRRTL:189808 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[8], io.brupdate.b2.uop.fu_code[8]
[748] FIRRTL:189809 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.fu_code[9], io.brupdate.b2.uop.fu_code[9]
[749] FIRRTL:189810 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iq_type[0], io.brupdate.b2.uop.iq_type[0]
[750] FIRRTL:189811 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iq_type[1], io.brupdate.b2.uop.iq_type[1]
[751] FIRRTL:189812 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iq_type[2], io.brupdate.b2.uop.iq_type[2]
[752] FIRRTL:189813 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.iq_type[3], io.brupdate.b2.uop.iq_type[3]
[753] FIRRTL:189814 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.debug_pc, io.brupdate.b2.uop.debug_pc
[754] FIRRTL:189815 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.is_rvc, io.brupdate.b2.uop.is_rvc
[755] FIRRTL:189816 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.debug_inst, io.brupdate.b2.uop.debug_inst
[756] FIRRTL:189817 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b2.uop.inst, io.brupdate.b2.uop.inst
[757] FIRRTL:189818 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b1.mispredict_mask, io.brupdate.b1.mispredict_mask
[758] FIRRTL:189819 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:129:19 KIND:connect :: connect rpq.io.brupdate.b1.resolve_mask, io.brupdate.b1.resolve_mask
[759] FIRRTL:189820 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:130:17 KIND:connect :: connect rpq.io.flush, io.exception
[760] FIRRTL:189821 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:18 KIND:node :: node _T_1 = eq(state, UInt<5>(0h0))
[761] FIRRTL:189822 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:35 KIND:node :: node _T_2 = eq(rpq.io.empty, UInt<1>(0h0))
[762] FIRRTL:189823 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:32 KIND:node :: node _T_3 = and(_T_1, _T_2)
[763] FIRRTL:189824 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:10 KIND:node :: node _T_4 = eq(_T_3, UInt<1>(0h0))
[764] FIRRTL:189825 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:node :: node _T_5 = asUInt(reset)
[765] FIRRTL:189826 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:node :: node _T_6 = eq(_T_5, UInt<1>(0h0))
[766] FIRRTL:189827 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:when :: when _T_6 :
[767] FIRRTL:189828 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:node :: node _T_7 = eq(_T_4, UInt<1>(0h0))
[768] FIRRTL:189829 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:when :: when _T_7 :
[769] FIRRTL:189830 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:131 assert(!(state === s_invalid && !rpq.io.empty))\n") : printf
[770] FIRRTL:189831 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:131:9 KIND:nondriving :: assert(clock, _T_4, UInt<1>(0h1), "") : assert
[771] FIRRTL:189832 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:40 KIND:node :: node _rpq_io_enq_valid_T = and(io.req_pri_val, io.req_pri_rdy)
[772] FIRRTL:189833 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:78 KIND:node :: node _rpq_io_enq_valid_T_1 = and(io.req_sec_val, io.req_sec_rdy)
[773] FIRRTL:189834 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:59 KIND:node :: node _rpq_io_enq_valid_T_2 = or(_rpq_io_enq_valid_T, _rpq_io_enq_valid_T_1)
[774] FIRRTL:189835 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:35 KIND:node :: node _rpq_io_enq_valid_T_3 = eq(io.req.uop.mem_cmd, UInt<2>(0h2))
[775] FIRRTL:189836 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:52 KIND:node :: node _rpq_io_enq_valid_T_4 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[776] FIRRTL:189837 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:45 KIND:node :: node _rpq_io_enq_valid_T_5 = or(_rpq_io_enq_valid_T_3, _rpq_io_enq_valid_T_4)
[777] FIRRTL:189838 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:101 KIND:node :: node _rpq_io_enq_valid_T_6 = eq(_rpq_io_enq_valid_T_5, UInt<1>(0h0))
[778] FIRRTL:189839 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:98 KIND:node :: node _rpq_io_enq_valid_T_7 = and(_rpq_io_enq_valid_T_2, _rpq_io_enq_valid_T_6)
[779] FIRRTL:189840 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:133:20 KIND:connect :: connect rpq.io.enq.valid, _rpq_io_enq_valid_T_7
[780] FIRRTL:189841 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.sdq_id, io.req.sdq_id
[781] FIRRTL:189842 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.way_en, io.req.way_en
[782] FIRRTL:189843 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.old_meta.tag, io.req.old_meta.tag
[783] FIRRTL:189844 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.old_meta.coh.state, io.req.old_meta.coh.state
[784] FIRRTL:189845 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.tag_match, io.req.tag_match
[785] FIRRTL:189846 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.is_hella, io.req.is_hella
[786] FIRRTL:189847 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.data, io.req.data
[787] FIRRTL:189848 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.addr, io.req.addr
[788] FIRRTL:189849 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.debug_tsrc, io.req.uop.debug_tsrc
[789] FIRRTL:189850 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.debug_fsrc, io.req.uop.debug_fsrc
[790] FIRRTL:189851 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.bp_xcpt_if, io.req.uop.bp_xcpt_if
[791] FIRRTL:189852 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.bp_debug_if, io.req.uop.bp_debug_if
[792] FIRRTL:189853 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.xcpt_ma_if, io.req.uop.xcpt_ma_if
[793] FIRRTL:189854 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.xcpt_ae_if, io.req.uop.xcpt_ae_if
[794] FIRRTL:189855 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.xcpt_pf_if, io.req.uop.xcpt_pf_if
[795] FIRRTL:189856 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_typ, io.req.uop.fp_typ
[796] FIRRTL:189857 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_rm, io.req.uop.fp_rm
[797] FIRRTL:189858 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_val, io.req.uop.fp_val
[798] FIRRTL:189859 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fcn_op, io.req.uop.fcn_op
[799] FIRRTL:189860 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fcn_dw, io.req.uop.fcn_dw
[800] FIRRTL:189861 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.frs3_en, io.req.uop.frs3_en
[801] FIRRTL:189862 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.lrs2_rtype, io.req.uop.lrs2_rtype
[802] FIRRTL:189863 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.lrs1_rtype, io.req.uop.lrs1_rtype
[803] FIRRTL:189864 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.dst_rtype, io.req.uop.dst_rtype
[804] FIRRTL:189865 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.lrs3, io.req.uop.lrs3
[805] FIRRTL:189866 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.lrs2, io.req.uop.lrs2
[806] FIRRTL:189867 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.lrs1, io.req.uop.lrs1
[807] FIRRTL:189868 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ldst, io.req.uop.ldst
[808] FIRRTL:189869 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ldst_is_rs1, io.req.uop.ldst_is_rs1
[809] FIRRTL:189870 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.csr_cmd, io.req.uop.csr_cmd
[810] FIRRTL:189871 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.flush_on_commit, io.req.uop.flush_on_commit
[811] FIRRTL:189872 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_unique, io.req.uop.is_unique
[812] FIRRTL:189873 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.uses_stq, io.req.uop.uses_stq
[813] FIRRTL:189874 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.uses_ldq, io.req.uop.uses_ldq
[814] FIRRTL:189875 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.mem_signed, io.req.uop.mem_signed
[815] FIRRTL:189876 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.mem_size, io.req.uop.mem_size
[816] FIRRTL:189877 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.mem_cmd, io.req.uop.mem_cmd
[817] FIRRTL:189878 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.exc_cause, io.req.uop.exc_cause
[818] FIRRTL:189879 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.exception, io.req.uop.exception
[819] FIRRTL:189880 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.stale_pdst, io.req.uop.stale_pdst
[820] FIRRTL:189881 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ppred_busy, io.req.uop.ppred_busy
[821] FIRRTL:189882 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs3_busy, io.req.uop.prs3_busy
[822] FIRRTL:189883 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs2_busy, io.req.uop.prs2_busy
[823] FIRRTL:189884 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs1_busy, io.req.uop.prs1_busy
[824] FIRRTL:189885 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ppred, io.req.uop.ppred
[825] FIRRTL:189886 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs3, io.req.uop.prs3
[826] FIRRTL:189887 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs2, io.req.uop.prs2
[827] FIRRTL:189888 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.prs1, io.req.uop.prs1
[828] FIRRTL:189889 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.pdst, io.req.uop.pdst
[829] FIRRTL:189890 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.rxq_idx, io.req.uop.rxq_idx
[830] FIRRTL:189891 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.stq_idx, io.req.uop.stq_idx
[831] FIRRTL:189892 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ldq_idx, io.req.uop.ldq_idx
[832] FIRRTL:189893 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.rob_idx, io.req.uop.rob_idx
[833] FIRRTL:189894 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.vec, io.req.uop.fp_ctrl.vec
[834] FIRRTL:189895 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.wflags, io.req.uop.fp_ctrl.wflags
[835] FIRRTL:189896 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.sqrt, io.req.uop.fp_ctrl.sqrt
[836] FIRRTL:189897 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.div, io.req.uop.fp_ctrl.div
[837] FIRRTL:189898 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.fma, io.req.uop.fp_ctrl.fma
[838] FIRRTL:189899 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.fastpipe, io.req.uop.fp_ctrl.fastpipe
[839] FIRRTL:189900 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.toint, io.req.uop.fp_ctrl.toint
[840] FIRRTL:189901 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.fromint, io.req.uop.fp_ctrl.fromint
[841] FIRRTL:189902 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.typeTagOut, io.req.uop.fp_ctrl.typeTagOut
[842] FIRRTL:189903 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.typeTagIn, io.req.uop.fp_ctrl.typeTagIn
[843] FIRRTL:189904 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.swap23, io.req.uop.fp_ctrl.swap23
[844] FIRRTL:189905 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.swap12, io.req.uop.fp_ctrl.swap12
[845] FIRRTL:189906 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.ren3, io.req.uop.fp_ctrl.ren3
[846] FIRRTL:189907 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.ren2, io.req.uop.fp_ctrl.ren2
[847] FIRRTL:189908 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.ren1, io.req.uop.fp_ctrl.ren1
[848] FIRRTL:189909 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.wen, io.req.uop.fp_ctrl.wen
[849] FIRRTL:189910 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fp_ctrl.ldst, io.req.uop.fp_ctrl.ldst
[850] FIRRTL:189911 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.op2_sel, io.req.uop.op2_sel
[851] FIRRTL:189912 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.op1_sel, io.req.uop.op1_sel
[852] FIRRTL:189913 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.imm_packed, io.req.uop.imm_packed
[853] FIRRTL:189914 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.pimm, io.req.uop.pimm
[854] FIRRTL:189915 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.imm_sel, io.req.uop.imm_sel
[855] FIRRTL:189916 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.imm_rename, io.req.uop.imm_rename
[856] FIRRTL:189917 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.taken, io.req.uop.taken
[857] FIRRTL:189918 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.pc_lob, io.req.uop.pc_lob
[858] FIRRTL:189919 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.edge_inst, io.req.uop.edge_inst
[859] FIRRTL:189920 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.ftq_idx, io.req.uop.ftq_idx
[860] FIRRTL:189921 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_mov, io.req.uop.is_mov
[861] FIRRTL:189922 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_rocc, io.req.uop.is_rocc
[862] FIRRTL:189923 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_sys_pc2epc, io.req.uop.is_sys_pc2epc
[863] FIRRTL:189924 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_eret, io.req.uop.is_eret
[864] FIRRTL:189925 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_amo, io.req.uop.is_amo
[865] FIRRTL:189926 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_sfence, io.req.uop.is_sfence
[866] FIRRTL:189927 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_fencei, io.req.uop.is_fencei
[867] FIRRTL:189928 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_fence, io.req.uop.is_fence
[868] FIRRTL:189929 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_sfb, io.req.uop.is_sfb
[869] FIRRTL:189930 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.br_type, io.req.uop.br_type
[870] FIRRTL:189931 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.br_tag, io.req.uop.br_tag
[871] FIRRTL:189932 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.br_mask, io.req.uop.br_mask
[872] FIRRTL:189933 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.dis_col_sel, io.req.uop.dis_col_sel
[873] FIRRTL:189934 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_p3_bypass_hint, io.req.uop.iw_p3_bypass_hint
[874] FIRRTL:189935 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_p2_bypass_hint, io.req.uop.iw_p2_bypass_hint
[875] FIRRTL:189936 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_p1_bypass_hint, io.req.uop.iw_p1_bypass_hint
[876] FIRRTL:189937 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_p2_speculative_child, io.req.uop.iw_p2_speculative_child
[877] FIRRTL:189938 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_p1_speculative_child, io.req.uop.iw_p1_speculative_child
[878] FIRRTL:189939 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_issued_partial_dgen, io.req.uop.iw_issued_partial_dgen
[879] FIRRTL:189940 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_issued_partial_agen, io.req.uop.iw_issued_partial_agen
[880] FIRRTL:189941 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iw_issued, io.req.uop.iw_issued
[881] FIRRTL:189942 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[0], io.req.uop.fu_code[0]
[882] FIRRTL:189943 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[1], io.req.uop.fu_code[1]
[883] FIRRTL:189944 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[2], io.req.uop.fu_code[2]
[884] FIRRTL:189945 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[3], io.req.uop.fu_code[3]
[885] FIRRTL:189946 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[4], io.req.uop.fu_code[4]
[886] FIRRTL:189947 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[5], io.req.uop.fu_code[5]
[887] FIRRTL:189948 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[6], io.req.uop.fu_code[6]
[888] FIRRTL:189949 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[7], io.req.uop.fu_code[7]
[889] FIRRTL:189950 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[8], io.req.uop.fu_code[8]
[890] FIRRTL:189951 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.fu_code[9], io.req.uop.fu_code[9]
[891] FIRRTL:189952 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iq_type[0], io.req.uop.iq_type[0]
[892] FIRRTL:189953 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iq_type[1], io.req.uop.iq_type[1]
[893] FIRRTL:189954 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iq_type[2], io.req.uop.iq_type[2]
[894] FIRRTL:189955 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.iq_type[3], io.req.uop.iq_type[3]
[895] FIRRTL:189956 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.debug_pc, io.req.uop.debug_pc
[896] FIRRTL:189957 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.is_rvc, io.req.uop.is_rvc
[897] FIRRTL:189958 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.debug_inst, io.req.uop.debug_inst
[898] FIRRTL:189959 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:134:20 KIND:connect :: connect rpq.io.enq.bits.uop.inst, io.req.uop.inst
[899] FIRRTL:189960 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:135:20 KIND:connect :: connect rpq.io.deq.ready, UInt<1>(0h0)
[900] FIRRTL:189961 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:138:21 KIND:reg :: reg grantack : { valid : UInt<1>, bits : { sink : UInt<3>}}, clock
[901] FIRRTL:189962 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:139:24 KIND:reg :: reg refill_ctr : UInt<3>, clock
[902] FIRRTL:189963 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:140:24 KIND:reg :: reg commit_line : UInt<1>, clock
[903] FIRRTL:189964 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:141:27 KIND:reg :: reg grant_had_data : UInt<1>, clock
[904] FIRRTL:189965 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:142:31 KIND:reg :: reg finish_to_prefetch : UInt<1>, clock
[905] FIRRTL:189966 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:145:28 KIND:regreset :: regreset meta_hazard : UInt<2>, clock, reset, UInt<2>(0h0)
[906] FIRRTL:189967 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:146:21 KIND:node :: node _T_8 = neq(meta_hazard, UInt<1>(0h0))
[907] FIRRTL:189968 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:146:30 KIND:when :: when _T_8 :
[908] FIRRTL:189969 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:146:59 KIND:node :: node _meta_hazard_T = add(meta_hazard, UInt<1>(0h1))
[909] FIRRTL:189970 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:146:59 KIND:node :: node _meta_hazard_T_1 = tail(_meta_hazard_T, 1)
[910] FIRRTL:189971 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:146:44 KIND:connect :: connect meta_hazard, _meta_hazard_T_1
[911] FIRRTL:189972 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_9 = and(io.meta_write.ready, io.meta_write.valid)
[912] FIRRTL:189973 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:147:29 KIND:when :: when _T_9 :
[913] FIRRTL:189974 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:147:43 KIND:connect :: connect meta_hazard, UInt<1>(0h1)
[914] FIRRTL:189975 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:34 KIND:node :: node _io_probe_rdy_T = eq(meta_hazard, UInt<1>(0h0))
[915] FIRRTL:189976 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_probe_rdy_T_1 = eq(state, UInt<5>(0h0))
[916] FIRRTL:189977 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_probe_rdy_T_2 = eq(state, UInt<5>(0h1))
[917] FIRRTL:189978 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_probe_rdy_T_3 = eq(state, UInt<5>(0h2))
[918] FIRRTL:189979 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_probe_rdy_T_4 = eq(state, UInt<5>(0h3))
[919] FIRRTL:189980 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_probe_rdy_T_5 = or(_io_probe_rdy_T_1, _io_probe_rdy_T_2)
[920] FIRRTL:189981 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_probe_rdy_T_6 = or(_io_probe_rdy_T_5, _io_probe_rdy_T_3)
[921] FIRRTL:189982 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_probe_rdy_T_7 = or(_io_probe_rdy_T_6, _io_probe_rdy_T_4)
[922] FIRRTL:189983 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:129 KIND:node :: node _io_probe_rdy_T_8 = eq(state, UInt<5>(0h4))
[923] FIRRTL:189984 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:145 KIND:node :: node _io_probe_rdy_T_9 = and(_io_probe_rdy_T_8, grantack.valid)
[924] FIRRTL:189985 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:119 KIND:node :: node _io_probe_rdy_T_10 = or(_io_probe_rdy_T_7, _io_probe_rdy_T_9)
[925] FIRRTL:189986 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:42 KIND:node :: node _io_probe_rdy_T_11 = and(_io_probe_rdy_T, _io_probe_rdy_T_10)
[926] FIRRTL:189987 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:148:18 KIND:connect :: connect io.probe_rdy, _io_probe_rdy_T_11
[927] FIRRTL:189988 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:149:25 KIND:node :: node _io_idx_valid_T = neq(state, UInt<5>(0h0))
[928] FIRRTL:189989 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:149:16 KIND:connect :: connect io.idx.valid, _io_idx_valid_T
[929] FIRRTL:189990 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:150:25 KIND:node :: node _io_tag_valid_T = neq(state, UInt<5>(0h0))
[930] FIRRTL:189991 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:150:16 KIND:connect :: connect io.tag.valid, _io_tag_valid_T
[931] FIRRTL:189992 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_way_valid_T = eq(state, UInt<5>(0h0))
[932] FIRRTL:189993 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_way_valid_T_1 = eq(state, UInt<5>(0h11))
[933] FIRRTL:189994 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_way_valid_T_2 = or(_io_way_valid_T, _io_way_valid_T_1)
[934] FIRRTL:189995 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:151:19 KIND:node :: node _io_way_valid_T_3 = eq(_io_way_valid_T_2, UInt<1>(0h0))
[935] FIRRTL:189996 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:151:16 KIND:connect :: connect io.way.valid, _io_way_valid_T_3
[936] FIRRTL:189997 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:152:15 KIND:connect :: connect io.idx.bits, req_idx
[937] FIRRTL:189998 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:153:15 KIND:connect :: connect io.tag.bits, req_tag
[938] FIRRTL:189999 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:154:15 KIND:connect :: connect io.way.bits, req.way_en
[939] FIRRTL:190000 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:156:26 KIND:connect :: connect io.meta_write.valid, UInt<1>(0h0)
[940] FIRRTL:190001 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:157:31 KIND:connect :: connect io.meta_write.bits.idx, req_idx
[941] FIRRTL:190002 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:158:31 KIND:connect :: connect io.meta_write.bits.data.coh, coh_on_clear
[942] FIRRTL:190003 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:159:31 KIND:connect :: connect io.meta_write.bits.data.tag, req_tag
[943] FIRRTL:190004 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:160:31 KIND:connect :: connect io.meta_write.bits.way_en, req.way_en
[944] FIRRTL:190005 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:161:31 KIND:connect :: connect io.meta_write.bits.tag, req_tag
[945] FIRRTL:190006 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:162:26 KIND:connect :: connect io.req_pri_rdy, UInt<1>(0h0)
[946] FIRRTL:190007 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:163:37 KIND:node :: node _io_req_sec_rdy_T = and(sec_rdy, rpq.io.enq.ready)
[947] FIRRTL:190008 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:163:26 KIND:connect :: connect io.req_sec_rdy, _io_req_sec_rdy_T
[948] FIRRTL:190009 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:164:26 KIND:connect :: connect io.mem_acquire.valid, UInt<1>(0h0)
[949] FIRRTL:190010 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:168:26 KIND:node :: node _io_mem_acquire_bits_T = cat(req_tag, req_idx)
[950] FIRRTL:190011 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:168:45 KIND:node :: node _io_mem_acquire_bits_T_1 = shl(_io_mem_acquire_bits_T, 6)
[951] FIRRTL:190012 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _io_mem_acquire_bits_legal_T = or(UInt<1>(0h0), UInt<1>(0h0))
[952] FIRRTL:190013 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _io_mem_acquire_bits_legal_T_1 = xor(_io_mem_acquire_bits_T_1, UInt<1>(0h0))
[953] FIRRTL:190014 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _io_mem_acquire_bits_legal_T_2 = cvt(_io_mem_acquire_bits_legal_T_1)
[954] FIRRTL:190015 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_3 = and(_io_mem_acquire_bits_legal_T_2, asSInt(UInt<33>(0h8c000000)))
[955] FIRRTL:190016 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_4 = asSInt(_io_mem_acquire_bits_legal_T_3)
[956] FIRRTL:190017 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _io_mem_acquire_bits_legal_T_5 = eq(_io_mem_acquire_bits_legal_T_4, asSInt(UInt<1>(0h0)))
[957] FIRRTL:190018 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _io_mem_acquire_bits_legal_T_6 = xor(_io_mem_acquire_bits_T_1, UInt<17>(0h10000))
[958] FIRRTL:190019 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _io_mem_acquire_bits_legal_T_7 = cvt(_io_mem_acquire_bits_legal_T_6)
[959] FIRRTL:190020 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_8 = and(_io_mem_acquire_bits_legal_T_7, asSInt(UInt<33>(0h8c011000)))
[960] FIRRTL:190021 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_9 = asSInt(_io_mem_acquire_bits_legal_T_8)
[961] FIRRTL:190022 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _io_mem_acquire_bits_legal_T_10 = eq(_io_mem_acquire_bits_legal_T_9, asSInt(UInt<1>(0h0)))
[962] FIRRTL:190023 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _io_mem_acquire_bits_legal_T_11 = xor(_io_mem_acquire_bits_T_1, UInt<28>(0hc000000))
[963] FIRRTL:190024 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _io_mem_acquire_bits_legal_T_12 = cvt(_io_mem_acquire_bits_legal_T_11)
[964] FIRRTL:190025 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_13 = and(_io_mem_acquire_bits_legal_T_12, asSInt(UInt<33>(0h8c000000)))
[965] FIRRTL:190026 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_14 = asSInt(_io_mem_acquire_bits_legal_T_13)
[966] FIRRTL:190027 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _io_mem_acquire_bits_legal_T_15 = eq(_io_mem_acquire_bits_legal_T_14, asSInt(UInt<1>(0h0)))
[967] FIRRTL:190028 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _io_mem_acquire_bits_legal_T_16 = or(_io_mem_acquire_bits_legal_T_5, _io_mem_acquire_bits_legal_T_10)
[968] FIRRTL:190029 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _io_mem_acquire_bits_legal_T_17 = or(_io_mem_acquire_bits_legal_T_16, _io_mem_acquire_bits_legal_T_15)
[969] FIRRTL:190030 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _io_mem_acquire_bits_legal_T_18 = and(_io_mem_acquire_bits_legal_T, _io_mem_acquire_bits_legal_T_17)
[970] FIRRTL:190031 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:93:44 KIND:node :: node _io_mem_acquire_bits_legal_T_19 = eq(UInt<3>(0h6), UInt<3>(0h6))
[971] FIRRTL:190032 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _io_mem_acquire_bits_legal_T_20 = or(UInt<1>(0h0), _io_mem_acquire_bits_legal_T_19)
[972] FIRRTL:190033 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _io_mem_acquire_bits_legal_T_21 = xor(_io_mem_acquire_bits_T_1, UInt<28>(0h8000000))
[973] FIRRTL:190034 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _io_mem_acquire_bits_legal_T_22 = cvt(_io_mem_acquire_bits_legal_T_21)
[974] FIRRTL:190035 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_23 = and(_io_mem_acquire_bits_legal_T_22, asSInt(UInt<33>(0h8c010000)))
[975] FIRRTL:190036 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_24 = asSInt(_io_mem_acquire_bits_legal_T_23)
[976] FIRRTL:190037 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _io_mem_acquire_bits_legal_T_25 = eq(_io_mem_acquire_bits_legal_T_24, asSInt(UInt<1>(0h0)))
[977] FIRRTL:190038 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _io_mem_acquire_bits_legal_T_26 = xor(_io_mem_acquire_bits_T_1, UInt<32>(0h80000000))
[978] FIRRTL:190039 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _io_mem_acquire_bits_legal_T_27 = cvt(_io_mem_acquire_bits_legal_T_26)
[979] FIRRTL:190040 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_28 = and(_io_mem_acquire_bits_legal_T_27, asSInt(UInt<33>(0h80000000)))
[980] FIRRTL:190041 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _io_mem_acquire_bits_legal_T_29 = asSInt(_io_mem_acquire_bits_legal_T_28)
[981] FIRRTL:190042 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _io_mem_acquire_bits_legal_T_30 = eq(_io_mem_acquire_bits_legal_T_29, asSInt(UInt<1>(0h0)))
[982] FIRRTL:190043 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _io_mem_acquire_bits_legal_T_31 = or(_io_mem_acquire_bits_legal_T_25, _io_mem_acquire_bits_legal_T_30)
[983] FIRRTL:190044 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _io_mem_acquire_bits_legal_T_32 = and(_io_mem_acquire_bits_legal_T_20, _io_mem_acquire_bits_legal_T_31)
[984] FIRRTL:190045 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _io_mem_acquire_bits_legal_T_33 = or(UInt<1>(0h0), _io_mem_acquire_bits_legal_T_18)
[985] FIRRTL:190046 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node io_mem_acquire_bits_legal = or(_io_mem_acquire_bits_legal_T_33, _io_mem_acquire_bits_legal_T_32)
[986] FIRRTL:190047 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:346:17 KIND:wire :: wire io_mem_acquire_bits_a : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[987] FIRRTL:190048 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:347:15 KIND:connect :: connect io_mem_acquire_bits_a.opcode, UInt<3>(0h6)
[988] FIRRTL:190049 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:348:15 KIND:connect :: connect io_mem_acquire_bits_a.param, grow_param
[989] FIRRTL:190050 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:349:15 KIND:connect :: connect io_mem_acquire_bits_a.size, UInt<3>(0h6)
[990] FIRRTL:190051 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:350:15 KIND:connect :: connect io_mem_acquire_bits_a.source, io.id
[991] FIRRTL:190052 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:351:15 KIND:connect :: connect io_mem_acquire_bits_a.address, _io_mem_acquire_bits_T_1
[992] FIRRTL:190053 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _io_mem_acquire_bits_a_mask_sizeOH_T = or(UInt<3>(0h6), UInt<3>(0h0))
[993] FIRRTL:190054 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node io_mem_acquire_bits_a_mask_sizeOH_shiftAmount = bits(_io_mem_acquire_bits_a_mask_sizeOH_T, 1, 0)
[994] FIRRTL:190055 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _io_mem_acquire_bits_a_mask_sizeOH_T_1 = dshl(UInt<1>(0h1), io_mem_acquire_bits_a_mask_sizeOH_shiftAmount)
[995] FIRRTL:190056 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _io_mem_acquire_bits_a_mask_sizeOH_T_2 = bits(_io_mem_acquire_bits_a_mask_sizeOH_T_1, 2, 0)
[996] FIRRTL:190057 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node io_mem_acquire_bits_a_mask_sizeOH = or(_io_mem_acquire_bits_a_mask_sizeOH_T_2, UInt<1>(0h1))
[997] FIRRTL:190058 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_sub_0_1 = geq(UInt<3>(0h6), UInt<2>(0h3))
[998] FIRRTL:190059 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_size = bits(io_mem_acquire_bits_a_mask_sizeOH, 2, 2)
[999] FIRRTL:190060 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_bit = bits(_io_mem_acquire_bits_T_1, 2, 2)
[1000] FIRRTL:190061 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_nbit = eq(io_mem_acquire_bits_a_mask_sub_sub_bit, UInt<1>(0h0))
[1001] FIRRTL:190062 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_0_2 = and(UInt<1>(0h1), io_mem_acquire_bits_a_mask_sub_sub_nbit)
[1002] FIRRTL:190063 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_sub_acc_T = and(io_mem_acquire_bits_a_mask_sub_sub_size, io_mem_acquire_bits_a_mask_sub_sub_0_2)
[1003] FIRRTL:190064 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_0_1 = or(io_mem_acquire_bits_a_mask_sub_sub_sub_0_1, _io_mem_acquire_bits_a_mask_sub_sub_acc_T)
[1004] FIRRTL:190065 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_1_2 = and(UInt<1>(0h1), io_mem_acquire_bits_a_mask_sub_sub_bit)
[1005] FIRRTL:190066 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_sub_acc_T_1 = and(io_mem_acquire_bits_a_mask_sub_sub_size, io_mem_acquire_bits_a_mask_sub_sub_1_2)
[1006] FIRRTL:190067 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_sub_1_1 = or(io_mem_acquire_bits_a_mask_sub_sub_sub_0_1, _io_mem_acquire_bits_a_mask_sub_sub_acc_T_1)
[1007] FIRRTL:190068 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node io_mem_acquire_bits_a_mask_sub_size = bits(io_mem_acquire_bits_a_mask_sizeOH, 1, 1)
[1008] FIRRTL:190069 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node io_mem_acquire_bits_a_mask_sub_bit = bits(_io_mem_acquire_bits_T_1, 1, 1)
[1009] FIRRTL:190070 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node io_mem_acquire_bits_a_mask_sub_nbit = eq(io_mem_acquire_bits_a_mask_sub_bit, UInt<1>(0h0))
[1010] FIRRTL:190071 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_0_2 = and(io_mem_acquire_bits_a_mask_sub_sub_0_2, io_mem_acquire_bits_a_mask_sub_nbit)
[1011] FIRRTL:190072 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_acc_T = and(io_mem_acquire_bits_a_mask_sub_size, io_mem_acquire_bits_a_mask_sub_0_2)
[1012] FIRRTL:190073 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_0_1 = or(io_mem_acquire_bits_a_mask_sub_sub_0_1, _io_mem_acquire_bits_a_mask_sub_acc_T)
[1013] FIRRTL:190074 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_1_2 = and(io_mem_acquire_bits_a_mask_sub_sub_0_2, io_mem_acquire_bits_a_mask_sub_bit)
[1014] FIRRTL:190075 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_acc_T_1 = and(io_mem_acquire_bits_a_mask_sub_size, io_mem_acquire_bits_a_mask_sub_1_2)
[1015] FIRRTL:190076 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_1_1 = or(io_mem_acquire_bits_a_mask_sub_sub_0_1, _io_mem_acquire_bits_a_mask_sub_acc_T_1)
[1016] FIRRTL:190077 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_2_2 = and(io_mem_acquire_bits_a_mask_sub_sub_1_2, io_mem_acquire_bits_a_mask_sub_nbit)
[1017] FIRRTL:190078 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_acc_T_2 = and(io_mem_acquire_bits_a_mask_sub_size, io_mem_acquire_bits_a_mask_sub_2_2)
[1018] FIRRTL:190079 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_2_1 = or(io_mem_acquire_bits_a_mask_sub_sub_1_1, _io_mem_acquire_bits_a_mask_sub_acc_T_2)
[1019] FIRRTL:190080 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_sub_3_2 = and(io_mem_acquire_bits_a_mask_sub_sub_1_2, io_mem_acquire_bits_a_mask_sub_bit)
[1020] FIRRTL:190081 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_sub_acc_T_3 = and(io_mem_acquire_bits_a_mask_sub_size, io_mem_acquire_bits_a_mask_sub_3_2)
[1021] FIRRTL:190082 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_sub_3_1 = or(io_mem_acquire_bits_a_mask_sub_sub_1_1, _io_mem_acquire_bits_a_mask_sub_acc_T_3)
[1022] FIRRTL:190083 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node io_mem_acquire_bits_a_mask_size = bits(io_mem_acquire_bits_a_mask_sizeOH, 0, 0)
[1023] FIRRTL:190084 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node io_mem_acquire_bits_a_mask_bit = bits(_io_mem_acquire_bits_T_1, 0, 0)
[1024] FIRRTL:190085 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node io_mem_acquire_bits_a_mask_nbit = eq(io_mem_acquire_bits_a_mask_bit, UInt<1>(0h0))
[1025] FIRRTL:190086 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq = and(io_mem_acquire_bits_a_mask_sub_0_2, io_mem_acquire_bits_a_mask_nbit)
[1026] FIRRTL:190087 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq)
[1027] FIRRTL:190088 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc = or(io_mem_acquire_bits_a_mask_sub_0_1, _io_mem_acquire_bits_a_mask_acc_T)
[1028] FIRRTL:190089 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_1 = and(io_mem_acquire_bits_a_mask_sub_0_2, io_mem_acquire_bits_a_mask_bit)
[1029] FIRRTL:190090 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_1 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_1)
[1030] FIRRTL:190091 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_1 = or(io_mem_acquire_bits_a_mask_sub_0_1, _io_mem_acquire_bits_a_mask_acc_T_1)
[1031] FIRRTL:190092 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_2 = and(io_mem_acquire_bits_a_mask_sub_1_2, io_mem_acquire_bits_a_mask_nbit)
[1032] FIRRTL:190093 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_2 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_2)
[1033] FIRRTL:190094 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_2 = or(io_mem_acquire_bits_a_mask_sub_1_1, _io_mem_acquire_bits_a_mask_acc_T_2)
[1034] FIRRTL:190095 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_3 = and(io_mem_acquire_bits_a_mask_sub_1_2, io_mem_acquire_bits_a_mask_bit)
[1035] FIRRTL:190096 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_3 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_3)
[1036] FIRRTL:190097 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_3 = or(io_mem_acquire_bits_a_mask_sub_1_1, _io_mem_acquire_bits_a_mask_acc_T_3)
[1037] FIRRTL:190098 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_4 = and(io_mem_acquire_bits_a_mask_sub_2_2, io_mem_acquire_bits_a_mask_nbit)
[1038] FIRRTL:190099 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_4 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_4)
[1039] FIRRTL:190100 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_4 = or(io_mem_acquire_bits_a_mask_sub_2_1, _io_mem_acquire_bits_a_mask_acc_T_4)
[1040] FIRRTL:190101 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_5 = and(io_mem_acquire_bits_a_mask_sub_2_2, io_mem_acquire_bits_a_mask_bit)
[1041] FIRRTL:190102 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_5 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_5)
[1042] FIRRTL:190103 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_5 = or(io_mem_acquire_bits_a_mask_sub_2_1, _io_mem_acquire_bits_a_mask_acc_T_5)
[1043] FIRRTL:190104 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_6 = and(io_mem_acquire_bits_a_mask_sub_3_2, io_mem_acquire_bits_a_mask_nbit)
[1044] FIRRTL:190105 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_6 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_6)
[1045] FIRRTL:190106 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_6 = or(io_mem_acquire_bits_a_mask_sub_3_1, _io_mem_acquire_bits_a_mask_acc_T_6)
[1046] FIRRTL:190107 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node io_mem_acquire_bits_a_mask_eq_7 = and(io_mem_acquire_bits_a_mask_sub_3_2, io_mem_acquire_bits_a_mask_bit)
[1047] FIRRTL:190108 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _io_mem_acquire_bits_a_mask_acc_T_7 = and(io_mem_acquire_bits_a_mask_size, io_mem_acquire_bits_a_mask_eq_7)
[1048] FIRRTL:190109 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node io_mem_acquire_bits_a_mask_acc_7 = or(io_mem_acquire_bits_a_mask_sub_3_1, _io_mem_acquire_bits_a_mask_acc_T_7)
[1049] FIRRTL:190110 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_lo_lo = cat(io_mem_acquire_bits_a_mask_acc_1, io_mem_acquire_bits_a_mask_acc)
[1050] FIRRTL:190111 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_lo_hi = cat(io_mem_acquire_bits_a_mask_acc_3, io_mem_acquire_bits_a_mask_acc_2)
[1051] FIRRTL:190112 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_lo = cat(io_mem_acquire_bits_a_mask_lo_hi, io_mem_acquire_bits_a_mask_lo_lo)
[1052] FIRRTL:190113 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_hi_lo = cat(io_mem_acquire_bits_a_mask_acc_5, io_mem_acquire_bits_a_mask_acc_4)
[1053] FIRRTL:190114 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_hi_hi = cat(io_mem_acquire_bits_a_mask_acc_7, io_mem_acquire_bits_a_mask_acc_6)
[1054] FIRRTL:190115 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node io_mem_acquire_bits_a_mask_hi = cat(io_mem_acquire_bits_a_mask_hi_hi, io_mem_acquire_bits_a_mask_hi_lo)
[1055] FIRRTL:190116 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _io_mem_acquire_bits_a_mask_T = cat(io_mem_acquire_bits_a_mask_hi, io_mem_acquire_bits_a_mask_lo)
[1056] FIRRTL:190117 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:354:15 KIND:connect :: connect io_mem_acquire_bits_a.mask, _io_mem_acquire_bits_a_mask_T
[1057] FIRRTL:190118 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:355:15 KIND:invalidate :: invalidate io_mem_acquire_bits_a.data
[1058] FIRRTL:190119 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:356:15 KIND:connect :: connect io_mem_acquire_bits_a.corrupt, UInt<1>(0h0)
[1059] FIRRTL:190120 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:166:24 KIND:connect :: connect io.mem_acquire.bits, io_mem_acquire_bits_a
[1060] FIRRTL:190121 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:171:26 KIND:connect :: connect io.refill.valid, UInt<1>(0h0)
[1061] FIRRTL:190122 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:172:57 KIND:node :: node _io_refill_bits_addr_T = shl(refill_ctr, 3)
[1062] FIRRTL:190123 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:172:43 KIND:node :: node _io_refill_bits_addr_T_1 = or(req_block_addr, _io_refill_bits_addr_T)
[1063] FIRRTL:190124 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:172:25 KIND:connect :: connect io.refill.bits.addr, _io_refill_bits_addr_T_1
[1064] FIRRTL:190125 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:173:25 KIND:connect :: connect io.refill.bits.way_en, req.way_en
[1065] FIRRTL:190126 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:174:28 KIND:node :: node _io_refill_bits_wmask_T = not(UInt<1>(0h0))
[1066] FIRRTL:190127 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:174:25 KIND:connect :: connect io.refill.bits.wmask, _io_refill_bits_wmask_T
[1067] FIRRTL:190128 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:175:25 KIND:connect :: connect io.refill.bits.data, io.lb_resp
[1068] FIRRTL:190129 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:176:26 KIND:connect :: connect io.replay.valid, UInt<1>(0h0)
[1069] FIRRTL:190130 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:177:26 KIND:connect :: connect io.replay.bits, rpq.io.deq.bits
[1070] FIRRTL:190131 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:178:26 KIND:connect :: connect io.wb_req.valid, UInt<1>(0h0)
[1071] FIRRTL:190132 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:179:28 KIND:connect :: connect io.wb_req.bits.tag, req.old_meta.tag
[1072] FIRRTL:190133 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:180:28 KIND:connect :: connect io.wb_req.bits.idx, req_idx
[1073] FIRRTL:190134 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:181:28 KIND:connect :: connect io.wb_req.bits.param, shrink_param
[1074] FIRRTL:190135 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:182:28 KIND:connect :: connect io.wb_req.bits.way_en, req.way_en
[1075] FIRRTL:190136 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:183:28 KIND:connect :: connect io.wb_req.bits.source, io.id
[1076] FIRRTL:190137 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:184:28 KIND:connect :: connect io.wb_req.bits.voluntary, UInt<1>(0h1)
[1077] FIRRTL:190138 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:185:26 KIND:connect :: connect io.resp.valid, UInt<1>(0h0)
[1078] FIRRTL:190139 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:186:26 KIND:connect :: connect io.resp.bits.is_hella, rpq.io.deq.bits.is_hella
[1079] FIRRTL:190140 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:186:26 KIND:connect :: connect io.resp.bits.data, rpq.io.deq.bits.data
[1080] FIRRTL:190141 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:186:26 KIND:connect :: connect io.resp.bits.uop, rpq.io.deq.bits.uop
[1081] FIRRTL:190142 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:187:26 KIND:connect :: connect io.commit_val, UInt<1>(0h0)
[1082] FIRRTL:190143 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:188:26 KIND:connect :: connect io.commit_addr, req.addr
[1083] FIRRTL:190144 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:189:26 KIND:connect :: connect io.commit_coh, coh_on_grant
[1084] FIRRTL:190145 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:190:26 KIND:connect :: connect io.meta_read.valid, UInt<1>(0h0)
[1085] FIRRTL:190146 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:191:25 KIND:connect :: connect io.meta_read.bits.idx, req_idx
[1086] FIRRTL:190147 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:192:25 KIND:connect :: connect io.meta_read.bits.tag, req_tag
[1087] FIRRTL:190148 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:193:28 KIND:connect :: connect io.meta_read.bits.way_en, req.way_en
[1088] FIRRTL:190149 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:194:26 KIND:connect :: connect io.mem_finish.valid, UInt<1>(0h0)
[1089] FIRRTL:190150 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:195:23 KIND:connect :: connect io.mem_finish.bits, grantack.bits
[1090] FIRRTL:190151 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:196:26 KIND:connect :: connect io.lb_write.valid, UInt<1>(0h0)
[1091] FIRRTL:190152 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:197:49 KIND:node :: node _io_lb_write_bits_offset_T = shr(refill_address_inc, 3)
[1092] FIRRTL:190153 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:197:27 KIND:connect :: connect io.lb_write.bits.offset, _io_lb_write_bits_offset_T
[1093] FIRRTL:190154 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:198:27 KIND:connect :: connect io.lb_write.bits.data, io.mem_grant.bits.data
[1094] FIRRTL:190155 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:199:22 KIND:connect :: connect io.mem_grant.ready, UInt<1>(0h0)
[1095] FIRRTL:190156 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:200:45 KIND:node :: node _io_lb_read_offset_T = shr(rpq.io.deq.bits.addr, 3)
[1096] FIRRTL:190157 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:200:21 KIND:connect :: connect io.lb_read.offset, _io_lb_read_offset_T
[1097] FIRRTL:190158 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:202:24 KIND:node :: node _T_10 = and(io.req_sec_val, io.req_sec_rdy)
[1098] FIRRTL:190159 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:202:43 KIND:when :: when _T_10 :
[1099] FIRRTL:190160 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:203:21 KIND:connect :: connect req.uop.mem_cmd, dirtier_cmd
[1100] FIRRTL:190161 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:204:25 KIND:when :: when is_hit_again :
[1101] FIRRTL:190162 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:205:15 KIND:connect :: connect new_coh, dirtier_coh
[1102] FIRRTL:190163 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:234:15 KIND:node :: node _T_11 = eq(state, UInt<5>(0h0))
[1103] FIRRTL:190164 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:234:30 KIND:when :: when _T_11 :
[1104] FIRRTL:190165 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:235:20 KIND:connect :: connect io.req_pri_rdy, UInt<1>(0h1)
[1105] FIRRTL:190166 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:236:20 KIND:connect :: connect grant_had_data, UInt<1>(0h0)
[1106] FIRRTL:190167 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:238:26 KIND:node :: node _T_12 = and(io.req_pri_val, io.req_pri_rdy)
[1107] FIRRTL:190168 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:238:45 KIND:when :: when _T_12 :
[1108] FIRRTL:190169 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:210:29 KIND:wire :: wire state_new_state : UInt
[1109] FIRRTL:190170 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:210:29 KIND:connect :: connect state_new_state, state
[1110] FIRRTL:190171 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:211:20 KIND:connect :: connect grantack.valid, UInt<1>(0h0)
[1111] FIRRTL:190172 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:212:16 KIND:connect :: connect refill_ctr, UInt<1>(0h0)
[1112] FIRRTL:190173 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T = asUInt(reset)
[1113] FIRRTL:190174 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T_1 = eq(_state_T, UInt<1>(0h0))
[1114] FIRRTL:190175 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:when :: when _state_T_1 :
[1115] FIRRTL:190176 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T_2 = eq(rpq.io.enq.ready, UInt<1>(0h0))
[1116] FIRRTL:190177 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:when :: when _state_T_2 :
[1117] FIRRTL:190178 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:213 assert(rpq.io.enq.ready)\n") : state_printf
[1118] FIRRTL:190179 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:nondriving :: assert(clock, rpq.io.enq.ready, UInt<1>(0h1), "") : state_assert
[1119] FIRRTL:190180 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:214:9 KIND:connect :: connect req, io.req
[1120] FIRRTL:190181 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T = eq(UInt<5>(0h10), UInt<5>(0h10))
[1121] FIRRTL:190182 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_1 = mux(_state_req_needs_wb_r_T, UInt<2>(0h2), UInt<2>(0h2))
[1122] FIRRTL:190183 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_2 = eq(UInt<5>(0h12), UInt<5>(0h10))
[1123] FIRRTL:190184 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_3 = mux(_state_req_needs_wb_r_T_2, UInt<2>(0h1), _state_req_needs_wb_r_T_1)
[1124] FIRRTL:190185 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_4 = eq(UInt<5>(0h13), UInt<5>(0h10))
[1125] FIRRTL:190186 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_5 = mux(_state_req_needs_wb_r_T_4, UInt<2>(0h0), _state_req_needs_wb_r_T_3)
[1126] FIRRTL:190187 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:120:19 KIND:node :: node _state_req_needs_wb_r_T_6 = cat(_state_req_needs_wb_r_T_5, io.req.old_meta.coh.state)
[1127] FIRRTL:190188 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:122:10 KIND:node :: node _state_req_needs_wb_r_T_7 = cat(UInt<2>(0h0), UInt<2>(0h3))
[1128] FIRRTL:190189 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:123:10 KIND:node :: node _state_req_needs_wb_r_T_8 = cat(UInt<2>(0h0), UInt<2>(0h2))
[1129] FIRRTL:190190 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:124:10 KIND:node :: node _state_req_needs_wb_r_T_9 = cat(UInt<2>(0h0), UInt<2>(0h1))
[1130] FIRRTL:190191 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:125:10 KIND:node :: node _state_req_needs_wb_r_T_10 = cat(UInt<2>(0h0), UInt<2>(0h0))
[1131] FIRRTL:190192 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:126:10 KIND:node :: node _state_req_needs_wb_r_T_11 = cat(UInt<2>(0h1), UInt<2>(0h3))
[1132] FIRRTL:190193 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:127:10 KIND:node :: node _state_req_needs_wb_r_T_12 = cat(UInt<2>(0h1), UInt<2>(0h2))
[1133] FIRRTL:190194 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:128:10 KIND:node :: node _state_req_needs_wb_r_T_13 = cat(UInt<2>(0h1), UInt<2>(0h1))
[1134] FIRRTL:190195 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:129:10 KIND:node :: node _state_req_needs_wb_r_T_14 = cat(UInt<2>(0h1), UInt<2>(0h0))
[1135] FIRRTL:190196 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:130:10 KIND:node :: node _state_req_needs_wb_r_T_15 = cat(UInt<2>(0h2), UInt<2>(0h3))
[1136] FIRRTL:190197 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:131:10 KIND:node :: node _state_req_needs_wb_r_T_16 = cat(UInt<2>(0h2), UInt<2>(0h2))
[1137] FIRRTL:190198 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:132:10 KIND:node :: node _state_req_needs_wb_r_T_17 = cat(UInt<2>(0h2), UInt<2>(0h1))
[1138] FIRRTL:190199 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:133:10 KIND:node :: node _state_req_needs_wb_r_T_18 = cat(UInt<2>(0h2), UInt<2>(0h0))
[1139] FIRRTL:190200 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_19 = eq(_state_req_needs_wb_r_T_18, _state_req_needs_wb_r_T_6)
[1140] FIRRTL:190201 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_20 = mux(_state_req_needs_wb_r_T_19, UInt<1>(0h0), UInt<1>(0h0))
[1141] FIRRTL:190202 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_21 = mux(_state_req_needs_wb_r_T_19, UInt<3>(0h5), UInt<1>(0h0))
[1142] FIRRTL:190203 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_22 = mux(_state_req_needs_wb_r_T_19, UInt<2>(0h0), UInt<1>(0h0))
[1143] FIRRTL:190204 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_23 = eq(_state_req_needs_wb_r_T_17, _state_req_needs_wb_r_T_6)
[1144] FIRRTL:190205 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_24 = mux(_state_req_needs_wb_r_T_23, UInt<1>(0h0), _state_req_needs_wb_r_T_20)
[1145] FIRRTL:190206 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_25 = mux(_state_req_needs_wb_r_T_23, UInt<3>(0h2), _state_req_needs_wb_r_T_21)
[1146] FIRRTL:190207 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_26 = mux(_state_req_needs_wb_r_T_23, UInt<2>(0h0), _state_req_needs_wb_r_T_22)
[1147] FIRRTL:190208 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_27 = eq(_state_req_needs_wb_r_T_16, _state_req_needs_wb_r_T_6)
[1148] FIRRTL:190209 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_28 = mux(_state_req_needs_wb_r_T_27, UInt<1>(0h0), _state_req_needs_wb_r_T_24)
[1149] FIRRTL:190210 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_29 = mux(_state_req_needs_wb_r_T_27, UInt<3>(0h1), _state_req_needs_wb_r_T_25)
[1150] FIRRTL:190211 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_30 = mux(_state_req_needs_wb_r_T_27, UInt<2>(0h0), _state_req_needs_wb_r_T_26)
[1151] FIRRTL:190212 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_31 = eq(_state_req_needs_wb_r_T_15, _state_req_needs_wb_r_T_6)
[1152] FIRRTL:190213 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_32 = mux(_state_req_needs_wb_r_T_31, UInt<1>(0h1), _state_req_needs_wb_r_T_28)
[1153] FIRRTL:190214 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_33 = mux(_state_req_needs_wb_r_T_31, UInt<3>(0h1), _state_req_needs_wb_r_T_29)
[1154] FIRRTL:190215 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_34 = mux(_state_req_needs_wb_r_T_31, UInt<2>(0h0), _state_req_needs_wb_r_T_30)
[1155] FIRRTL:190216 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_35 = eq(_state_req_needs_wb_r_T_14, _state_req_needs_wb_r_T_6)
[1156] FIRRTL:190217 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_36 = mux(_state_req_needs_wb_r_T_35, UInt<1>(0h0), _state_req_needs_wb_r_T_32)
[1157] FIRRTL:190218 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_37 = mux(_state_req_needs_wb_r_T_35, UInt<3>(0h5), _state_req_needs_wb_r_T_33)
[1158] FIRRTL:190219 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_38 = mux(_state_req_needs_wb_r_T_35, UInt<2>(0h0), _state_req_needs_wb_r_T_34)
[1159] FIRRTL:190220 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_39 = eq(_state_req_needs_wb_r_T_13, _state_req_needs_wb_r_T_6)
[1160] FIRRTL:190221 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_40 = mux(_state_req_needs_wb_r_T_39, UInt<1>(0h0), _state_req_needs_wb_r_T_36)
[1161] FIRRTL:190222 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_41 = mux(_state_req_needs_wb_r_T_39, UInt<3>(0h4), _state_req_needs_wb_r_T_37)
[1162] FIRRTL:190223 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_42 = mux(_state_req_needs_wb_r_T_39, UInt<2>(0h1), _state_req_needs_wb_r_T_38)
[1163] FIRRTL:190224 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_43 = eq(_state_req_needs_wb_r_T_12, _state_req_needs_wb_r_T_6)
[1164] FIRRTL:190225 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_44 = mux(_state_req_needs_wb_r_T_43, UInt<1>(0h0), _state_req_needs_wb_r_T_40)
[1165] FIRRTL:190226 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_45 = mux(_state_req_needs_wb_r_T_43, UInt<3>(0h0), _state_req_needs_wb_r_T_41)
[1166] FIRRTL:190227 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_46 = mux(_state_req_needs_wb_r_T_43, UInt<2>(0h1), _state_req_needs_wb_r_T_42)
[1167] FIRRTL:190228 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_47 = eq(_state_req_needs_wb_r_T_11, _state_req_needs_wb_r_T_6)
[1168] FIRRTL:190229 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_48 = mux(_state_req_needs_wb_r_T_47, UInt<1>(0h1), _state_req_needs_wb_r_T_44)
[1169] FIRRTL:190230 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_49 = mux(_state_req_needs_wb_r_T_47, UInt<3>(0h0), _state_req_needs_wb_r_T_45)
[1170] FIRRTL:190231 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_50 = mux(_state_req_needs_wb_r_T_47, UInt<2>(0h1), _state_req_needs_wb_r_T_46)
[1171] FIRRTL:190232 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_51 = eq(_state_req_needs_wb_r_T_10, _state_req_needs_wb_r_T_6)
[1172] FIRRTL:190233 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_52 = mux(_state_req_needs_wb_r_T_51, UInt<1>(0h0), _state_req_needs_wb_r_T_48)
[1173] FIRRTL:190234 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_53 = mux(_state_req_needs_wb_r_T_51, UInt<3>(0h5), _state_req_needs_wb_r_T_49)
[1174] FIRRTL:190235 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_54 = mux(_state_req_needs_wb_r_T_51, UInt<2>(0h0), _state_req_needs_wb_r_T_50)
[1175] FIRRTL:190236 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_55 = eq(_state_req_needs_wb_r_T_9, _state_req_needs_wb_r_T_6)
[1176] FIRRTL:190237 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_56 = mux(_state_req_needs_wb_r_T_55, UInt<1>(0h0), _state_req_needs_wb_r_T_52)
[1177] FIRRTL:190238 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_57 = mux(_state_req_needs_wb_r_T_55, UInt<3>(0h4), _state_req_needs_wb_r_T_53)
[1178] FIRRTL:190239 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_58 = mux(_state_req_needs_wb_r_T_55, UInt<2>(0h1), _state_req_needs_wb_r_T_54)
[1179] FIRRTL:190240 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_59 = eq(_state_req_needs_wb_r_T_8, _state_req_needs_wb_r_T_6)
[1180] FIRRTL:190241 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_60 = mux(_state_req_needs_wb_r_T_59, UInt<1>(0h0), _state_req_needs_wb_r_T_56)
[1181] FIRRTL:190242 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_61 = mux(_state_req_needs_wb_r_T_59, UInt<3>(0h3), _state_req_needs_wb_r_T_57)
[1182] FIRRTL:190243 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_62 = mux(_state_req_needs_wb_r_T_59, UInt<2>(0h2), _state_req_needs_wb_r_T_58)
[1183] FIRRTL:190244 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_63 = eq(_state_req_needs_wb_r_T_7, _state_req_needs_wb_r_T_6)
[1184] FIRRTL:190245 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node state_req_needs_wb_r_1 = mux(_state_req_needs_wb_r_T_63, UInt<1>(0h1), _state_req_needs_wb_r_T_60)
[1185] FIRRTL:190246 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node state_req_needs_wb_r_2 = mux(_state_req_needs_wb_r_T_63, UInt<3>(0h3), _state_req_needs_wb_r_T_61)
[1186] FIRRTL:190247 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node state_req_needs_wb_r_3 = mux(_state_req_needs_wb_r_T_63, UInt<2>(0h2), _state_req_needs_wb_r_T_62)
[1187] FIRRTL:190248 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_req_needs_wb_meta : { state : UInt<2>}
[1188] FIRRTL:190249 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_req_needs_wb_meta.state, state_req_needs_wb_r_3
[1189] FIRRTL:190250 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:216:18 KIND:connect :: connect req_needs_wb, state_req_needs_wb_r_1
[1190] FIRRTL:190251 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:217:29 KIND:when :: when io.req.tag_match :
[1191] FIRRTL:190252 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_r_c_cat_T = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[1192] FIRRTL:190253 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_r_c_cat_T_1 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[1193] FIRRTL:190254 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_r_c_cat_T_2 = or(_state_r_c_cat_T, _state_r_c_cat_T_1)
[1194] FIRRTL:190255 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_r_c_cat_T_3 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[1195] FIRRTL:190256 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_r_c_cat_T_4 = or(_state_r_c_cat_T_2, _state_r_c_cat_T_3)
[1196] FIRRTL:190257 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_5 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[1197] FIRRTL:190258 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_6 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[1198] FIRRTL:190259 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_7 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[1199] FIRRTL:190260 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_8 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[1200] FIRRTL:190261 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_9 = or(_state_r_c_cat_T_5, _state_r_c_cat_T_6)
[1201] FIRRTL:190262 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_10 = or(_state_r_c_cat_T_9, _state_r_c_cat_T_7)
[1202] FIRRTL:190263 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_11 = or(_state_r_c_cat_T_10, _state_r_c_cat_T_8)
[1203] FIRRTL:190264 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_12 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[1204] FIRRTL:190265 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_13 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[1205] FIRRTL:190266 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_14 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[1206] FIRRTL:190267 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_15 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[1207] FIRRTL:190268 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_16 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[1208] FIRRTL:190269 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_17 = or(_state_r_c_cat_T_12, _state_r_c_cat_T_13)
[1209] FIRRTL:190270 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_18 = or(_state_r_c_cat_T_17, _state_r_c_cat_T_14)
[1210] FIRRTL:190271 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_19 = or(_state_r_c_cat_T_18, _state_r_c_cat_T_15)
[1211] FIRRTL:190272 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_20 = or(_state_r_c_cat_T_19, _state_r_c_cat_T_16)
[1212] FIRRTL:190273 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_r_c_cat_T_21 = or(_state_r_c_cat_T_11, _state_r_c_cat_T_20)
[1213] FIRRTL:190274 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_r_c_cat_T_22 = or(_state_r_c_cat_T_4, _state_r_c_cat_T_21)
[1214] FIRRTL:190275 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_r_c_cat_T_23 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[1215] FIRRTL:190276 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_r_c_cat_T_24 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[1216] FIRRTL:190277 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_r_c_cat_T_25 = or(_state_r_c_cat_T_23, _state_r_c_cat_T_24)
[1217] FIRRTL:190278 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_r_c_cat_T_26 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[1218] FIRRTL:190279 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_r_c_cat_T_27 = or(_state_r_c_cat_T_25, _state_r_c_cat_T_26)
[1219] FIRRTL:190280 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_28 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[1220] FIRRTL:190281 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_29 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[1221] FIRRTL:190282 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_30 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[1222] FIRRTL:190283 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_31 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[1223] FIRRTL:190284 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_32 = or(_state_r_c_cat_T_28, _state_r_c_cat_T_29)
[1224] FIRRTL:190285 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_33 = or(_state_r_c_cat_T_32, _state_r_c_cat_T_30)
[1225] FIRRTL:190286 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_34 = or(_state_r_c_cat_T_33, _state_r_c_cat_T_31)
[1226] FIRRTL:190287 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_35 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[1227] FIRRTL:190288 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_36 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[1228] FIRRTL:190289 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_37 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[1229] FIRRTL:190290 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_38 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[1230] FIRRTL:190291 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_39 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[1231] FIRRTL:190292 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_40 = or(_state_r_c_cat_T_35, _state_r_c_cat_T_36)
[1232] FIRRTL:190293 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_41 = or(_state_r_c_cat_T_40, _state_r_c_cat_T_37)
[1233] FIRRTL:190294 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_42 = or(_state_r_c_cat_T_41, _state_r_c_cat_T_38)
[1234] FIRRTL:190295 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_43 = or(_state_r_c_cat_T_42, _state_r_c_cat_T_39)
[1235] FIRRTL:190296 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_r_c_cat_T_44 = or(_state_r_c_cat_T_34, _state_r_c_cat_T_43)
[1236] FIRRTL:190297 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_r_c_cat_T_45 = or(_state_r_c_cat_T_27, _state_r_c_cat_T_44)
[1237] FIRRTL:190298 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _state_r_c_cat_T_46 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[1238] FIRRTL:190299 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _state_r_c_cat_T_47 = or(_state_r_c_cat_T_45, _state_r_c_cat_T_46)
[1239] FIRRTL:190300 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _state_r_c_cat_T_48 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[1240] FIRRTL:190301 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _state_r_c_cat_T_49 = or(_state_r_c_cat_T_47, _state_r_c_cat_T_48)
[1241] FIRRTL:190302 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node state_r_c = cat(_state_r_c_cat_T_22, _state_r_c_cat_T_49)
[1242] FIRRTL:190303 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _state_r_T = cat(state_r_c, io.req.old_meta.coh.state)
[1243] FIRRTL:190304 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_1 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1244] FIRRTL:190305 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _state_r_T_2 = cat(_state_r_T_1, UInt<2>(0h3))
[1245] FIRRTL:190306 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_3 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1246] FIRRTL:190307 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _state_r_T_4 = cat(_state_r_T_3, UInt<2>(0h2))
[1247] FIRRTL:190308 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_5 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1248] FIRRTL:190309 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _state_r_T_6 = cat(_state_r_T_5, UInt<2>(0h1))
[1249] FIRRTL:190310 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_7 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1250] FIRRTL:190311 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _state_r_T_8 = cat(_state_r_T_7, UInt<2>(0h3))
[1251] FIRRTL:190312 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_9 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1252] FIRRTL:190313 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _state_r_T_10 = cat(_state_r_T_9, UInt<2>(0h2))
[1253] FIRRTL:190314 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_11 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1254] FIRRTL:190315 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _state_r_T_12 = cat(_state_r_T_11, UInt<2>(0h3))
[1255] FIRRTL:190316 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_13 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1256] FIRRTL:190317 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _state_r_T_14 = cat(_state_r_T_13, UInt<2>(0h2))
[1257] FIRRTL:190318 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_15 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1258] FIRRTL:190319 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _state_r_T_16 = cat(_state_r_T_15, UInt<2>(0h0))
[1259] FIRRTL:190320 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_17 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1260] FIRRTL:190321 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _state_r_T_18 = cat(_state_r_T_17, UInt<2>(0h1))
[1261] FIRRTL:190322 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_19 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1262] FIRRTL:190323 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _state_r_T_20 = cat(_state_r_T_19, UInt<2>(0h0))
[1263] FIRRTL:190324 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_21 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1264] FIRRTL:190325 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _state_r_T_22 = cat(_state_r_T_21, UInt<2>(0h1))
[1265] FIRRTL:190326 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_23 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1266] FIRRTL:190327 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _state_r_T_24 = cat(_state_r_T_23, UInt<2>(0h0))
[1267] FIRRTL:190328 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_25 = eq(_state_r_T_24, _state_r_T)
[1268] FIRRTL:190329 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_26 = mux(_state_r_T_25, UInt<1>(0h0), UInt<1>(0h0))
[1269] FIRRTL:190330 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_27 = mux(_state_r_T_25, UInt<2>(0h1), UInt<1>(0h0))
[1270] FIRRTL:190331 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_28 = eq(_state_r_T_22, _state_r_T)
[1271] FIRRTL:190332 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_29 = mux(_state_r_T_28, UInt<1>(0h0), _state_r_T_26)
[1272] FIRRTL:190333 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_30 = mux(_state_r_T_28, UInt<2>(0h2), _state_r_T_27)
[1273] FIRRTL:190334 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_31 = eq(_state_r_T_20, _state_r_T)
[1274] FIRRTL:190335 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_32 = mux(_state_r_T_31, UInt<1>(0h0), _state_r_T_29)
[1275] FIRRTL:190336 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_33 = mux(_state_r_T_31, UInt<2>(0h1), _state_r_T_30)
[1276] FIRRTL:190337 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_34 = eq(_state_r_T_18, _state_r_T)
[1277] FIRRTL:190338 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_35 = mux(_state_r_T_34, UInt<1>(0h0), _state_r_T_32)
[1278] FIRRTL:190339 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_36 = mux(_state_r_T_34, UInt<2>(0h2), _state_r_T_33)
[1279] FIRRTL:190340 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_37 = eq(_state_r_T_16, _state_r_T)
[1280] FIRRTL:190341 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_38 = mux(_state_r_T_37, UInt<1>(0h0), _state_r_T_35)
[1281] FIRRTL:190342 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_39 = mux(_state_r_T_37, UInt<2>(0h0), _state_r_T_36)
[1282] FIRRTL:190343 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_40 = eq(_state_r_T_14, _state_r_T)
[1283] FIRRTL:190344 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_41 = mux(_state_r_T_40, UInt<1>(0h1), _state_r_T_38)
[1284] FIRRTL:190345 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_42 = mux(_state_r_T_40, UInt<2>(0h3), _state_r_T_39)
[1285] FIRRTL:190346 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_43 = eq(_state_r_T_12, _state_r_T)
[1286] FIRRTL:190347 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_44 = mux(_state_r_T_43, UInt<1>(0h1), _state_r_T_41)
[1287] FIRRTL:190348 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_45 = mux(_state_r_T_43, UInt<2>(0h3), _state_r_T_42)
[1288] FIRRTL:190349 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_46 = eq(_state_r_T_10, _state_r_T)
[1289] FIRRTL:190350 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_47 = mux(_state_r_T_46, UInt<1>(0h1), _state_r_T_44)
[1290] FIRRTL:190351 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_48 = mux(_state_r_T_46, UInt<2>(0h2), _state_r_T_45)
[1291] FIRRTL:190352 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_49 = eq(_state_r_T_8, _state_r_T)
[1292] FIRRTL:190353 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_50 = mux(_state_r_T_49, UInt<1>(0h1), _state_r_T_47)
[1293] FIRRTL:190354 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_51 = mux(_state_r_T_49, UInt<2>(0h3), _state_r_T_48)
[1294] FIRRTL:190355 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_52 = eq(_state_r_T_6, _state_r_T)
[1295] FIRRTL:190356 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_53 = mux(_state_r_T_52, UInt<1>(0h1), _state_r_T_50)
[1296] FIRRTL:190357 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_54 = mux(_state_r_T_52, UInt<2>(0h1), _state_r_T_51)
[1297] FIRRTL:190358 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_55 = eq(_state_r_T_4, _state_r_T)
[1298] FIRRTL:190359 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_56 = mux(_state_r_T_55, UInt<1>(0h1), _state_r_T_53)
[1299] FIRRTL:190360 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_57 = mux(_state_r_T_55, UInt<2>(0h2), _state_r_T_54)
[1300] FIRRTL:190361 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_58 = eq(_state_r_T_2, _state_r_T)
[1301] FIRRTL:190362 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node state_is_hit = mux(_state_r_T_58, UInt<1>(0h1), _state_r_T_56)
[1302] FIRRTL:190363 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node state_r_2 = mux(_state_r_T_58, UInt<2>(0h3), _state_r_T_57)
[1303] FIRRTL:190364 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_coh_on_hit : { state : UInt<2>}
[1304] FIRRTL:190365 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_coh_on_hit.state, state_r_2
[1305] FIRRTL:190366 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:219:21 KIND:when :: when state_is_hit :
[1306] FIRRTL:190367 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_T_3 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[1307] FIRRTL:190368 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_T_4 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[1308] FIRRTL:190369 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_T_5 = or(_state_T_3, _state_T_4)
[1309] FIRRTL:190370 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_T_6 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[1310] FIRRTL:190371 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_T_7 = or(_state_T_5, _state_T_6)
[1311] FIRRTL:190372 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_8 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[1312] FIRRTL:190373 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_9 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[1313] FIRRTL:190374 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_10 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[1314] FIRRTL:190375 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_11 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[1315] FIRRTL:190376 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_12 = or(_state_T_8, _state_T_9)
[1316] FIRRTL:190377 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_13 = or(_state_T_12, _state_T_10)
[1317] FIRRTL:190378 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_14 = or(_state_T_13, _state_T_11)
[1318] FIRRTL:190379 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_15 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[1319] FIRRTL:190380 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_16 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[1320] FIRRTL:190381 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_17 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[1321] FIRRTL:190382 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_18 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[1322] FIRRTL:190383 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_19 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[1323] FIRRTL:190384 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_20 = or(_state_T_15, _state_T_16)
[1324] FIRRTL:190385 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_21 = or(_state_T_20, _state_T_17)
[1325] FIRRTL:190386 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_22 = or(_state_T_21, _state_T_18)
[1326] FIRRTL:190387 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_23 = or(_state_T_22, _state_T_19)
[1327] FIRRTL:190388 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_T_24 = or(_state_T_14, _state_T_23)
[1328] FIRRTL:190389 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_T_25 = or(_state_T_7, _state_T_24)
[1329] FIRRTL:190390 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_26 = asUInt(reset)
[1330] FIRRTL:190391 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_27 = eq(_state_T_26, UInt<1>(0h0))
[1331] FIRRTL:190392 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:when :: when _state_T_27 :
[1332] FIRRTL:190393 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_28 = eq(_state_T_25, UInt<1>(0h0))
[1333] FIRRTL:190394 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:when :: when _state_T_28 :
[1334] FIRRTL:190395 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:220 assert(isWrite(io.req.uop.mem_cmd))\n") : state_printf_1
[1335] FIRRTL:190396 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:nondriving :: assert(clock, _state_T_25, UInt<1>(0h1), "") : state_assert_1
[1336] FIRRTL:190397 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:221:21 KIND:connect :: connect new_coh, state_coh_on_hit
[1337] FIRRTL:190398 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:222:21 KIND:connect :: connect state_new_state, UInt<5>(0hc)
[1338] FIRRTL:190399 SRC:<no-source-locator> KIND:else :: else :
[1339] FIRRTL:190400 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:224:21 KIND:connect :: connect new_coh, io.req.old_meta.coh
[1340] FIRRTL:190401 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:225:21 KIND:connect :: connect state_new_state, UInt<5>(0h1)
[1341] FIRRTL:190402 SRC:<no-source-locator> KIND:else :: else :
[1342] FIRRTL:190403 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_new_coh_meta : { state : UInt<2>}
[1343] FIRRTL:190404 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_new_coh_meta.state, UInt<2>(0h0)
[1344] FIRRTL:190405 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:228:19 KIND:connect :: connect new_coh, state_new_coh_meta
[1345] FIRRTL:190406 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:229:19 KIND:connect :: connect state_new_state, UInt<5>(0h1)
[1346] FIRRTL:190407 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:239:13 KIND:connect :: connect state, state_new_state
[1347] FIRRTL:190408 SRC:<no-source-locator> KIND:else :: else :
[1348] FIRRTL:190409 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:241:22 KIND:node :: node _T_13 = eq(state, UInt<5>(0h1))
[1349] FIRRTL:190410 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:241:40 KIND:when :: when _T_13 :
[1350] FIRRTL:190411 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:242:26 KIND:connect :: connect io.mem_acquire.valid, UInt<1>(0h1)
[1351] FIRRTL:190412 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_14 = and(io.mem_acquire.ready, io.mem_acquire.valid)
[1352] FIRRTL:190413 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:243:32 KIND:when :: when _T_14 :
[1353] FIRRTL:190414 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:244:13 KIND:connect :: connect state, UInt<5>(0h2)
[1354] FIRRTL:190415 SRC:<no-source-locator> KIND:else :: else :
[1355] FIRRTL:190416 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:246:22 KIND:node :: node _T_15 = eq(state, UInt<5>(0h2))
[1356] FIRRTL:190417 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:246:41 KIND:when :: when _T_15 :
[1357] FIRRTL:190418 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:247:24 KIND:connect :: connect io.mem_grant.ready, UInt<1>(0h1)
[1358] FIRRTL:190419 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:106:36 KIND:node :: node opdata = bits(io.mem_grant.bits.opcode, 0, 0)
[1359] FIRRTL:190420 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:248:44 KIND:when :: when opdata :
[1360] FIRRTL:190421 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:249:31 KIND:connect :: connect io.lb_write.valid, io.mem_grant.valid
[1361] FIRRTL:190422 SRC:<no-source-locator> KIND:else :: else :
[1362] FIRRTL:190423 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:251:31 KIND:connect :: connect io.mem_grant.ready, UInt<1>(0h1)
[1363] FIRRTL:190424 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_16 = and(io.mem_grant.ready, io.mem_grant.valid)
[1364] FIRRTL:190425 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:254:30 KIND:when :: when _T_16 :
[1365] FIRRTL:190426 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:106:36 KIND:node :: node grant_had_data_opdata = bits(io.mem_grant.bits.opcode, 0, 0)
[1366] FIRRTL:190427 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:255:22 KIND:connect :: connect grant_had_data, grant_had_data_opdata
[1367] FIRRTL:190428 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:257:24 KIND:when :: when refill_done :
[1368] FIRRTL:190429 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:71:36 KIND:node :: node _grantack_valid_T = bits(io.mem_grant.bits.opcode, 2, 2)
[1369] FIRRTL:190430 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:71:52 KIND:node :: node _grantack_valid_T_1 = bits(io.mem_grant.bits.opcode, 1, 1)
[1370] FIRRTL:190431 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:71:43 KIND:node :: node _grantack_valid_T_2 = eq(_grantack_valid_T_1, UInt<1>(0h0))
[1371] FIRRTL:190432 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:71:40 KIND:node :: node _grantack_valid_T_3 = and(_grantack_valid_T, _grantack_valid_T_2)
[1372] FIRRTL:190433 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:258:22 KIND:connect :: connect grantack.valid, _grantack_valid_T_3
[1373] FIRRTL:190434 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:451:17 KIND:wire :: wire grantack_bits_e : { sink : UInt<3>}
[1374] FIRRTL:190435 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:452:12 KIND:connect :: connect grantack_bits_e.sink, io.mem_grant.bits.sink
[1375] FIRRTL:190436 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:259:21 KIND:connect :: connect grantack.bits, grantack_bits_e
[1376] FIRRTL:190437 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:260:19 KIND:node :: node _state_T_29 = mux(grant_had_data, UInt<5>(0h3), UInt<5>(0hc))
[1377] FIRRTL:190438 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:260:13 KIND:connect :: connect state, _state_T_29
[1378] FIRRTL:190439 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:16 KIND:node :: node _T_17 = eq(grant_had_data, UInt<1>(0h0))
[1379] FIRRTL:190440 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:32 KIND:node :: node _T_18 = and(_T_17, req_needs_wb)
[1380] FIRRTL:190441 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:14 KIND:node :: node _T_19 = eq(_T_18, UInt<1>(0h0))
[1381] FIRRTL:190442 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:node :: node _T_20 = asUInt(reset)
[1382] FIRRTL:190443 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:node :: node _T_21 = eq(_T_20, UInt<1>(0h0))
[1383] FIRRTL:190444 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:when :: when _T_21 :
[1384] FIRRTL:190445 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:node :: node _T_22 = eq(_T_19, UInt<1>(0h0))
[1385] FIRRTL:190446 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:when :: when _T_22 :
[1386] FIRRTL:190447 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:261 assert(!(!grant_had_data && req_needs_wb))\n") : printf_1
[1387] FIRRTL:190448 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:261:13 KIND:nondriving :: assert(clock, _T_19, UInt<1>(0h1), "") : assert_1
[1388] FIRRTL:190449 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:262:19 KIND:connect :: connect commit_line, UInt<1>(0h0)
[1389] FIRRTL:190450 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:263:15 KIND:connect :: connect new_coh, coh_on_grant
[1390] FIRRTL:190451 SRC:<no-source-locator> KIND:else :: else :
[1391] FIRRTL:190452 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:266:22 KIND:node :: node _T_23 = eq(state, UInt<5>(0h3))
[1392] FIRRTL:190453 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:266:45 KIND:when :: when _T_23 :
[1393] FIRRTL:190454 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<1>(0h0))
[1394] FIRRTL:190455 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_1 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<5>(0h10))
[1395] FIRRTL:190456 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_2 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h6))
[1396] FIRRTL:190457 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_3 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h7))
[1397] FIRRTL:190458 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_4 = or(_drain_load_T, _drain_load_T_1)
[1398] FIRRTL:190459 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_5 = or(_drain_load_T_4, _drain_load_T_2)
[1399] FIRRTL:190460 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_6 = or(_drain_load_T_5, _drain_load_T_3)
[1400] FIRRTL:190461 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_7 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h4))
[1401] FIRRTL:190462 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_8 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h9))
[1402] FIRRTL:190463 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_9 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0ha))
[1403] FIRRTL:190464 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_10 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hb))
[1404] FIRRTL:190465 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_11 = or(_drain_load_T_7, _drain_load_T_8)
[1405] FIRRTL:190466 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_12 = or(_drain_load_T_11, _drain_load_T_9)
[1406] FIRRTL:190467 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_13 = or(_drain_load_T_12, _drain_load_T_10)
[1407] FIRRTL:190468 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_14 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h8))
[1408] FIRRTL:190469 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_15 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hc))
[1409] FIRRTL:190470 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_16 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hd))
[1410] FIRRTL:190471 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_17 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0he))
[1411] FIRRTL:190472 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_18 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hf))
[1412] FIRRTL:190473 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_19 = or(_drain_load_T_14, _drain_load_T_15)
[1413] FIRRTL:190474 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_20 = or(_drain_load_T_19, _drain_load_T_16)
[1414] FIRRTL:190475 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_21 = or(_drain_load_T_20, _drain_load_T_17)
[1415] FIRRTL:190476 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_22 = or(_drain_load_T_21, _drain_load_T_18)
[1416] FIRRTL:190477 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _drain_load_T_23 = or(_drain_load_T_13, _drain_load_T_22)
[1417] FIRRTL:190478 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _drain_load_T_24 = or(_drain_load_T_6, _drain_load_T_23)
[1418] FIRRTL:190479 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _drain_load_T_25 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<1>(0h1))
[1419] FIRRTL:190480 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _drain_load_T_26 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<5>(0h11))
[1420] FIRRTL:190481 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _drain_load_T_27 = or(_drain_load_T_25, _drain_load_T_26)
[1421] FIRRTL:190482 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _drain_load_T_28 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h7))
[1422] FIRRTL:190483 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _drain_load_T_29 = or(_drain_load_T_27, _drain_load_T_28)
[1423] FIRRTL:190484 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_30 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h4))
[1424] FIRRTL:190485 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_31 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h9))
[1425] FIRRTL:190486 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_32 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0ha))
[1426] FIRRTL:190487 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_33 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hb))
[1427] FIRRTL:190488 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_34 = or(_drain_load_T_30, _drain_load_T_31)
[1428] FIRRTL:190489 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_35 = or(_drain_load_T_34, _drain_load_T_32)
[1429] FIRRTL:190490 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_36 = or(_drain_load_T_35, _drain_load_T_33)
[1430] FIRRTL:190491 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_37 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h8))
[1431] FIRRTL:190492 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_38 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hc))
[1432] FIRRTL:190493 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_39 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hd))
[1433] FIRRTL:190494 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_40 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0he))
[1434] FIRRTL:190495 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _drain_load_T_41 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hf))
[1435] FIRRTL:190496 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_42 = or(_drain_load_T_37, _drain_load_T_38)
[1436] FIRRTL:190497 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_43 = or(_drain_load_T_42, _drain_load_T_39)
[1437] FIRRTL:190498 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_44 = or(_drain_load_T_43, _drain_load_T_40)
[1438] FIRRTL:190499 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _drain_load_T_45 = or(_drain_load_T_44, _drain_load_T_41)
[1439] FIRRTL:190500 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _drain_load_T_46 = or(_drain_load_T_36, _drain_load_T_45)
[1440] FIRRTL:190501 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _drain_load_T_47 = or(_drain_load_T_29, _drain_load_T_46)
[1441] FIRRTL:190502 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:268:22 KIND:node :: node _drain_load_T_48 = eq(_drain_load_T_47, UInt<1>(0h0))
[1442] FIRRTL:190503 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:267:59 KIND:node :: node _drain_load_T_49 = and(_drain_load_T_24, _drain_load_T_48)
[1443] FIRRTL:190504 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:269:51 KIND:node :: node _drain_load_T_50 = neq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h6))
[1444] FIRRTL:190505 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:268:60 KIND:node :: node drain_load = and(_drain_load_T_49, _drain_load_T_50)
[1445] FIRRTL:190506 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:271:61 KIND:node :: node _rp_addr_T = bits(rpq.io.deq.bits.addr, 5, 0)
[1446] FIRRTL:190507 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:271:22 KIND:node :: node rp_addr_hi = cat(req_tag, req_idx)
[1447] FIRRTL:190508 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:271:22 KIND:node :: node rp_addr = cat(rp_addr_hi, _rp_addr_T)
[1448] FIRRTL:190509 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:274:32 KIND:node :: node _data_word_T = cat(UInt<1>(0h0), UInt<6>(0h0))
[1449] FIRRTL:190510 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:274:26 KIND:node :: node data_word = dshr(io.lb_resp, _data_word_T)
[1450] FIRRTL:190511 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:276:49 KIND:node :: node _T_24 = bits(rpq.io.deq.bits.addr, 5, 0)
[1451] FIRRTL:190512 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:276:10 KIND:node :: node hi = cat(req_tag, req_idx)
[1452] FIRRTL:190513 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:276:10 KIND:node :: node _T_25 = cat(hi, _T_24)
[1453] FIRRTL:190514 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11:18 KIND:wire :: wire size : UInt<2>
[1454] FIRRTL:190515 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect size, rpq.io.deq.bits.uop.mem_size
[1455] FIRRTL:190516 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:280:40 KIND:node :: node _rpq_io_deq_ready_T = and(io.resp.ready, drain_load)
[1456] FIRRTL:190517 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:280:23 KIND:connect :: connect rpq.io.deq.ready, _rpq_io_deq_ready_T
[1457] FIRRTL:190518 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:282:47 KIND:node :: node _io_lb_read_offset_T_1 = shr(rpq.io.deq.bits.addr, 3)
[1458] FIRRTL:190519 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:282:23 KIND:connect :: connect io.lb_read.offset, _io_lb_read_offset_T_1
[1459] FIRRTL:190520 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:284:43 KIND:node :: node _io_resp_valid_T = and(rpq.io.deq.valid, drain_load)
[1460] FIRRTL:190521 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:284:23 KIND:connect :: connect io.resp.valid, _io_resp_valid_T
[1461] FIRRTL:190522 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T = bits(_T_25, 2, 2)
[1462] FIRRTL:190523 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_1 = bits(data_word, 63, 32)
[1463] FIRRTL:190524 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_2 = bits(data_word, 31, 0)
[1464] FIRRTL:190525 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted = mux(_io_resp_bits_data_shifted_T, _io_resp_bits_data_shifted_T_1, _io_resp_bits_data_shifted_T_2)
[1465] FIRRTL:190526 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero = and(UInt<1>(0h0), UInt<1>(0h0))
[1466] FIRRTL:190527 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed = mux(io_resp_bits_data_doZero, UInt<1>(0h0), io_resp_bits_data_shifted)
[1467] FIRRTL:190528 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T = eq(size, UInt<2>(0h2))
[1468] FIRRTL:190529 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_1 = or(_io_resp_bits_data_T, io_resp_bits_data_doZero)
[1469] FIRRTL:190530 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_2 = bits(io_resp_bits_data_zeroed, 31, 31)
[1470] FIRRTL:190531 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_3 = and(rpq.io.deq.bits.uop.mem_signed, _io_resp_bits_data_T_2)
[1471] FIRRTL:190532 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_4 = mux(_io_resp_bits_data_T_3, UInt<32>(0hffffffff), UInt<32>(0h0))
[1472] FIRRTL:190533 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_5 = bits(data_word, 63, 32)
[1473] FIRRTL:190534 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_6 = mux(_io_resp_bits_data_T_1, _io_resp_bits_data_T_4, _io_resp_bits_data_T_5)
[1474] FIRRTL:190535 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_7 = cat(_io_resp_bits_data_T_6, io_resp_bits_data_zeroed)
[1475] FIRRTL:190536 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T_3 = bits(_T_25, 1, 1)
[1476] FIRRTL:190537 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_4 = bits(_io_resp_bits_data_T_7, 31, 16)
[1477] FIRRTL:190538 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_5 = bits(_io_resp_bits_data_T_7, 15, 0)
[1478] FIRRTL:190539 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted_1 = mux(_io_resp_bits_data_shifted_T_3, _io_resp_bits_data_shifted_T_4, _io_resp_bits_data_shifted_T_5)
[1479] FIRRTL:190540 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero_1 = and(UInt<1>(0h0), UInt<1>(0h0))
[1480] FIRRTL:190541 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed_1 = mux(io_resp_bits_data_doZero_1, UInt<1>(0h0), io_resp_bits_data_shifted_1)
[1481] FIRRTL:190542 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T_8 = eq(size, UInt<1>(0h1))
[1482] FIRRTL:190543 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_9 = or(_io_resp_bits_data_T_8, io_resp_bits_data_doZero_1)
[1483] FIRRTL:190544 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_10 = bits(io_resp_bits_data_zeroed_1, 15, 15)
[1484] FIRRTL:190545 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_11 = and(rpq.io.deq.bits.uop.mem_signed, _io_resp_bits_data_T_10)
[1485] FIRRTL:190546 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_12 = mux(_io_resp_bits_data_T_11, UInt<48>(0hffffffffffff), UInt<48>(0h0))
[1486] FIRRTL:190547 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_13 = bits(_io_resp_bits_data_T_7, 63, 16)
[1487] FIRRTL:190548 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_14 = mux(_io_resp_bits_data_T_9, _io_resp_bits_data_T_12, _io_resp_bits_data_T_13)
[1488] FIRRTL:190549 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_15 = cat(_io_resp_bits_data_T_14, io_resp_bits_data_zeroed_1)
[1489] FIRRTL:190550 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T_6 = bits(_T_25, 0, 0)
[1490] FIRRTL:190551 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_7 = bits(_io_resp_bits_data_T_15, 15, 8)
[1491] FIRRTL:190552 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_8 = bits(_io_resp_bits_data_T_15, 7, 0)
[1492] FIRRTL:190553 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted_2 = mux(_io_resp_bits_data_shifted_T_6, _io_resp_bits_data_shifted_T_7, _io_resp_bits_data_shifted_T_8)
[1493] FIRRTL:190554 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero_2 = and(UInt<1>(0h1), UInt<1>(0h0))
[1494] FIRRTL:190555 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed_2 = mux(io_resp_bits_data_doZero_2, UInt<1>(0h0), io_resp_bits_data_shifted_2)
[1495] FIRRTL:190556 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T_16 = eq(size, UInt<1>(0h0))
[1496] FIRRTL:190557 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_17 = or(_io_resp_bits_data_T_16, io_resp_bits_data_doZero_2)
[1497] FIRRTL:190558 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_18 = bits(io_resp_bits_data_zeroed_2, 7, 7)
[1498] FIRRTL:190559 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_19 = and(rpq.io.deq.bits.uop.mem_signed, _io_resp_bits_data_T_18)
[1499] FIRRTL:190560 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_20 = mux(_io_resp_bits_data_T_19, UInt<56>(0hffffffffffffff), UInt<56>(0h0))
[1500] FIRRTL:190561 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_21 = bits(_io_resp_bits_data_T_15, 63, 8)
[1501] FIRRTL:190562 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_22 = mux(_io_resp_bits_data_T_17, _io_resp_bits_data_T_20, _io_resp_bits_data_T_21)
[1502] FIRRTL:190563 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_23 = cat(_io_resp_bits_data_T_22, io_resp_bits_data_zeroed_2)
[1503] FIRRTL:190564 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:285:23 KIND:connect :: connect io.resp.bits.data, _io_resp_bits_data_T_23
[1504] FIRRTL:190565 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:286:27 KIND:connect :: connect io.resp.bits.is_hella, rpq.io.deq.bits.is_hella
[1505] FIRRTL:190566 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_26 = and(rpq.io.deq.ready, rpq.io.deq.valid)
[1506] FIRRTL:190567 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:287:28 KIND:when :: when _T_26 :
[1507] FIRRTL:190568 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:288:21 KIND:connect :: connect commit_line, UInt<1>(0h1)
[1508] FIRRTL:190569 SRC:<no-source-locator> KIND:else :: else :
[1509] FIRRTL:190570 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:290:34 KIND:node :: node _T_27 = eq(commit_line, UInt<1>(0h0))
[1510] FIRRTL:190571 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:290:31 KIND:node :: node _T_28 = and(rpq.io.empty, _T_27)
[1511] FIRRTL:190572 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:291:5 KIND:when :: when _T_28 :
[1512] FIRRTL:190573 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_29 = and(rpq.io.enq.ready, rpq.io.enq.valid)
[1513] FIRRTL:190574 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:292:13 KIND:node :: node _T_30 = eq(_T_29, UInt<1>(0h0))
[1514] FIRRTL:190575 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:292:31 KIND:when :: when _T_30 :
[1515] FIRRTL:190576 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:293:15 KIND:connect :: connect state, UInt<5>(0he)
[1516] FIRRTL:190577 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:294:28 KIND:connect :: connect finish_to_prefetch, UInt<1>(0h0)
[1517] FIRRTL:190578 SRC:<no-source-locator> KIND:else :: else :
[1518] FIRRTL:190579 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:296:55 KIND:node :: node _T_31 = eq(drain_load, UInt<1>(0h0))
[1519] FIRRTL:190580 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:296:52 KIND:node :: node _T_32 = and(rpq.io.deq.valid, _T_31)
[1520] FIRRTL:190581 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:296:31 KIND:node :: node _T_33 = or(rpq.io.empty, _T_32)
[1521] FIRRTL:190582 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:296:69 KIND:when :: when _T_33 :
[1522] FIRRTL:190583 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:299:21 KIND:connect :: connect io.commit_val, UInt<1>(0h1)
[1523] FIRRTL:190584 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:300:13 KIND:connect :: connect state, UInt<5>(0h4)
[1524] FIRRTL:190585 SRC:<no-source-locator> KIND:else :: else :
[1525] FIRRTL:190586 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:302:22 KIND:node :: node _T_34 = eq(state, UInt<5>(0h4))
[1526] FIRRTL:190587 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:302:39 KIND:when :: when _T_34 :
[1527] FIRRTL:190588 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:27 KIND:node :: node _io_meta_read_valid_T = eq(io.prober_state.valid, UInt<1>(0h0))
[1528] FIRRTL:190589 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:53 KIND:node :: node _io_meta_read_valid_T_1 = eq(grantack.valid, UInt<1>(0h0))
[1529] FIRRTL:190590 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:50 KIND:node :: node _io_meta_read_valid_T_2 = or(_io_meta_read_valid_T, _io_meta_read_valid_T_1)
[1530] FIRRTL:190591 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:93 KIND:node :: node _io_meta_read_valid_T_3 = bits(io.prober_state.bits, 11, 6)
[1531] FIRRTL:190592 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:120 KIND:node :: node _io_meta_read_valid_T_4 = neq(_io_meta_read_valid_T_3, req_idx)
[1532] FIRRTL:190593 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:69 KIND:node :: node _io_meta_read_valid_T_5 = or(_io_meta_read_valid_T_2, _io_meta_read_valid_T_4)
[1533] FIRRTL:190594 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:303:24 KIND:connect :: connect io.meta_read.valid, _io_meta_read_valid_T_5
[1534] FIRRTL:190595 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_35 = and(io.meta_read.ready, io.meta_read.valid)
[1535] FIRRTL:190596 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:304:30 KIND:when :: when _T_35 :
[1536] FIRRTL:190597 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:305:13 KIND:connect :: connect state, UInt<5>(0h5)
[1537] FIRRTL:190598 SRC:<no-source-locator> KIND:else :: else :
[1538] FIRRTL:190599 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:307:22 KIND:node :: node _T_36 = eq(state, UInt<5>(0h5))
[1539] FIRRTL:190600 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:307:41 KIND:when :: when _T_36 :
[1540] FIRRTL:190601 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:308:11 KIND:connect :: connect state, UInt<5>(0h6)
[1541] FIRRTL:190602 SRC:<no-source-locator> KIND:else :: else :
[1542] FIRRTL:190603 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:309:22 KIND:node :: node _T_37 = eq(state, UInt<5>(0h6))
[1543] FIRRTL:190604 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:309:41 KIND:when :: when _T_37 :
[1544] FIRRTL:190605 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T = eq(UInt<5>(0h10), UInt<5>(0h10))
[1545] FIRRTL:190606 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T_1 = mux(_needs_wb_r_T, UInt<2>(0h2), UInt<2>(0h2))
[1546] FIRRTL:190607 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T_2 = eq(UInt<5>(0h12), UInt<5>(0h10))
[1547] FIRRTL:190608 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T_3 = mux(_needs_wb_r_T_2, UInt<2>(0h1), _needs_wb_r_T_1)
[1548] FIRRTL:190609 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T_4 = eq(UInt<5>(0h13), UInt<5>(0h10))
[1549] FIRRTL:190610 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _needs_wb_r_T_5 = mux(_needs_wb_r_T_4, UInt<2>(0h0), _needs_wb_r_T_3)
[1550] FIRRTL:190611 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:120:19 KIND:node :: node _needs_wb_r_T_6 = cat(_needs_wb_r_T_5, io.meta_resp.bits.coh.state)
[1551] FIRRTL:190612 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:122:10 KIND:node :: node _needs_wb_r_T_7 = cat(UInt<2>(0h0), UInt<2>(0h3))
[1552] FIRRTL:190613 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:123:10 KIND:node :: node _needs_wb_r_T_8 = cat(UInt<2>(0h0), UInt<2>(0h2))
[1553] FIRRTL:190614 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:124:10 KIND:node :: node _needs_wb_r_T_9 = cat(UInt<2>(0h0), UInt<2>(0h1))
[1554] FIRRTL:190615 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:125:10 KIND:node :: node _needs_wb_r_T_10 = cat(UInt<2>(0h0), UInt<2>(0h0))
[1555] FIRRTL:190616 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:126:10 KIND:node :: node _needs_wb_r_T_11 = cat(UInt<2>(0h1), UInt<2>(0h3))
[1556] FIRRTL:190617 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:127:10 KIND:node :: node _needs_wb_r_T_12 = cat(UInt<2>(0h1), UInt<2>(0h2))
[1557] FIRRTL:190618 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:128:10 KIND:node :: node _needs_wb_r_T_13 = cat(UInt<2>(0h1), UInt<2>(0h1))
[1558] FIRRTL:190619 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:129:10 KIND:node :: node _needs_wb_r_T_14 = cat(UInt<2>(0h1), UInt<2>(0h0))
[1559] FIRRTL:190620 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:130:10 KIND:node :: node _needs_wb_r_T_15 = cat(UInt<2>(0h2), UInt<2>(0h3))
[1560] FIRRTL:190621 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:131:10 KIND:node :: node _needs_wb_r_T_16 = cat(UInt<2>(0h2), UInt<2>(0h2))
[1561] FIRRTL:190622 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:132:10 KIND:node :: node _needs_wb_r_T_17 = cat(UInt<2>(0h2), UInt<2>(0h1))
[1562] FIRRTL:190623 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:133:10 KIND:node :: node _needs_wb_r_T_18 = cat(UInt<2>(0h2), UInt<2>(0h0))
[1563] FIRRTL:190624 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_19 = eq(_needs_wb_r_T_18, _needs_wb_r_T_6)
[1564] FIRRTL:190625 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_20 = mux(_needs_wb_r_T_19, UInt<1>(0h0), UInt<1>(0h0))
[1565] FIRRTL:190626 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_21 = mux(_needs_wb_r_T_19, UInt<3>(0h5), UInt<1>(0h0))
[1566] FIRRTL:190627 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_22 = mux(_needs_wb_r_T_19, UInt<2>(0h0), UInt<1>(0h0))
[1567] FIRRTL:190628 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_23 = eq(_needs_wb_r_T_17, _needs_wb_r_T_6)
[1568] FIRRTL:190629 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_24 = mux(_needs_wb_r_T_23, UInt<1>(0h0), _needs_wb_r_T_20)
[1569] FIRRTL:190630 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_25 = mux(_needs_wb_r_T_23, UInt<3>(0h2), _needs_wb_r_T_21)
[1570] FIRRTL:190631 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_26 = mux(_needs_wb_r_T_23, UInt<2>(0h0), _needs_wb_r_T_22)
[1571] FIRRTL:190632 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_27 = eq(_needs_wb_r_T_16, _needs_wb_r_T_6)
[1572] FIRRTL:190633 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_28 = mux(_needs_wb_r_T_27, UInt<1>(0h0), _needs_wb_r_T_24)
[1573] FIRRTL:190634 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_29 = mux(_needs_wb_r_T_27, UInt<3>(0h1), _needs_wb_r_T_25)
[1574] FIRRTL:190635 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_30 = mux(_needs_wb_r_T_27, UInt<2>(0h0), _needs_wb_r_T_26)
[1575] FIRRTL:190636 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_31 = eq(_needs_wb_r_T_15, _needs_wb_r_T_6)
[1576] FIRRTL:190637 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_32 = mux(_needs_wb_r_T_31, UInt<1>(0h1), _needs_wb_r_T_28)
[1577] FIRRTL:190638 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_33 = mux(_needs_wb_r_T_31, UInt<3>(0h1), _needs_wb_r_T_29)
[1578] FIRRTL:190639 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_34 = mux(_needs_wb_r_T_31, UInt<2>(0h0), _needs_wb_r_T_30)
[1579] FIRRTL:190640 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_35 = eq(_needs_wb_r_T_14, _needs_wb_r_T_6)
[1580] FIRRTL:190641 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_36 = mux(_needs_wb_r_T_35, UInt<1>(0h0), _needs_wb_r_T_32)
[1581] FIRRTL:190642 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_37 = mux(_needs_wb_r_T_35, UInt<3>(0h5), _needs_wb_r_T_33)
[1582] FIRRTL:190643 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_38 = mux(_needs_wb_r_T_35, UInt<2>(0h0), _needs_wb_r_T_34)
[1583] FIRRTL:190644 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_39 = eq(_needs_wb_r_T_13, _needs_wb_r_T_6)
[1584] FIRRTL:190645 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_40 = mux(_needs_wb_r_T_39, UInt<1>(0h0), _needs_wb_r_T_36)
[1585] FIRRTL:190646 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_41 = mux(_needs_wb_r_T_39, UInt<3>(0h4), _needs_wb_r_T_37)
[1586] FIRRTL:190647 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_42 = mux(_needs_wb_r_T_39, UInt<2>(0h1), _needs_wb_r_T_38)
[1587] FIRRTL:190648 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_43 = eq(_needs_wb_r_T_12, _needs_wb_r_T_6)
[1588] FIRRTL:190649 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_44 = mux(_needs_wb_r_T_43, UInt<1>(0h0), _needs_wb_r_T_40)
[1589] FIRRTL:190650 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_45 = mux(_needs_wb_r_T_43, UInt<3>(0h0), _needs_wb_r_T_41)
[1590] FIRRTL:190651 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_46 = mux(_needs_wb_r_T_43, UInt<2>(0h1), _needs_wb_r_T_42)
[1591] FIRRTL:190652 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_47 = eq(_needs_wb_r_T_11, _needs_wb_r_T_6)
[1592] FIRRTL:190653 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_48 = mux(_needs_wb_r_T_47, UInt<1>(0h1), _needs_wb_r_T_44)
[1593] FIRRTL:190654 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_49 = mux(_needs_wb_r_T_47, UInt<3>(0h0), _needs_wb_r_T_45)
[1594] FIRRTL:190655 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_50 = mux(_needs_wb_r_T_47, UInt<2>(0h1), _needs_wb_r_T_46)
[1595] FIRRTL:190656 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_51 = eq(_needs_wb_r_T_10, _needs_wb_r_T_6)
[1596] FIRRTL:190657 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_52 = mux(_needs_wb_r_T_51, UInt<1>(0h0), _needs_wb_r_T_48)
[1597] FIRRTL:190658 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_53 = mux(_needs_wb_r_T_51, UInt<3>(0h5), _needs_wb_r_T_49)
[1598] FIRRTL:190659 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_54 = mux(_needs_wb_r_T_51, UInt<2>(0h0), _needs_wb_r_T_50)
[1599] FIRRTL:190660 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_55 = eq(_needs_wb_r_T_9, _needs_wb_r_T_6)
[1600] FIRRTL:190661 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_56 = mux(_needs_wb_r_T_55, UInt<1>(0h0), _needs_wb_r_T_52)
[1601] FIRRTL:190662 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_57 = mux(_needs_wb_r_T_55, UInt<3>(0h4), _needs_wb_r_T_53)
[1602] FIRRTL:190663 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_58 = mux(_needs_wb_r_T_55, UInt<2>(0h1), _needs_wb_r_T_54)
[1603] FIRRTL:190664 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_59 = eq(_needs_wb_r_T_8, _needs_wb_r_T_6)
[1604] FIRRTL:190665 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _needs_wb_r_T_60 = mux(_needs_wb_r_T_59, UInt<1>(0h0), _needs_wb_r_T_56)
[1605] FIRRTL:190666 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _needs_wb_r_T_61 = mux(_needs_wb_r_T_59, UInt<3>(0h3), _needs_wb_r_T_57)
[1606] FIRRTL:190667 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _needs_wb_r_T_62 = mux(_needs_wb_r_T_59, UInt<2>(0h2), _needs_wb_r_T_58)
[1607] FIRRTL:190668 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _needs_wb_r_T_63 = eq(_needs_wb_r_T_7, _needs_wb_r_T_6)
[1608] FIRRTL:190669 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node needs_wb = mux(_needs_wb_r_T_63, UInt<1>(0h1), _needs_wb_r_T_60)
[1609] FIRRTL:190670 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node needs_wb_r_2 = mux(_needs_wb_r_T_63, UInt<3>(0h3), _needs_wb_r_T_61)
[1610] FIRRTL:190671 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node needs_wb_r_3 = mux(_needs_wb_r_T_63, UInt<2>(0h2), _needs_wb_r_T_62)
[1611] FIRRTL:190672 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire needs_wb_meta : { state : UInt<2>}
[1612] FIRRTL:190673 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect needs_wb_meta.state, needs_wb_r_3
[1613] FIRRTL:190674 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:311:18 KIND:node :: node _state_T_30 = eq(io.meta_resp.valid, UInt<1>(0h0))
[1614] FIRRTL:190675 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:312:17 KIND:node :: node _state_T_31 = mux(needs_wb, UInt<5>(0h7), UInt<5>(0hb))
[1615] FIRRTL:190676 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:311:17 KIND:node :: node _state_T_32 = mux(_state_T_30, UInt<5>(0h4), _state_T_31)
[1616] FIRRTL:190677 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:311:11 KIND:connect :: connect state, _state_T_32
[1617] FIRRTL:190678 SRC:<no-source-locator> KIND:else :: else :
[1618] FIRRTL:190679 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:313:22 KIND:node :: node _T_38 = eq(state, UInt<5>(0h7))
[1619] FIRRTL:190680 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:313:40 KIND:when :: when _T_38 :
[1620] FIRRTL:190681 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:314:33 KIND:connect :: connect io.meta_write.valid, UInt<1>(0h1)
[1621] FIRRTL:190682 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_39 = and(io.meta_write.ready, io.meta_write.valid)
[1622] FIRRTL:190683 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:316:31 KIND:when :: when _T_39 :
[1623] FIRRTL:190684 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:317:18 KIND:connect :: connect state, UInt<5>(0h9)
[1624] FIRRTL:190685 SRC:<no-source-locator> KIND:else :: else :
[1625] FIRRTL:190686 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:319:22 KIND:node :: node _T_40 = eq(state, UInt<5>(0h9))
[1626] FIRRTL:190687 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:319:36 KIND:when :: when _T_40 :
[1627] FIRRTL:190688 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:320:30 KIND:connect :: connect io.wb_req.valid, UInt<1>(0h1)
[1628] FIRRTL:190689 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_41 = and(io.wb_req.ready, io.wb_req.valid)
[1629] FIRRTL:190690 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:321:27 KIND:when :: when _T_41 :
[1630] FIRRTL:190691 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:322:13 KIND:connect :: connect state, UInt<5>(0ha)
[1631] FIRRTL:190692 SRC:<no-source-locator> KIND:else :: else :
[1632] FIRRTL:190693 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:324:22 KIND:node :: node _T_42 = eq(state, UInt<5>(0ha))
[1633] FIRRTL:190694 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:324:37 KIND:when :: when _T_42 :
[1634] FIRRTL:190695 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:325:23 KIND:when :: when io.wb_resp :
[1635] FIRRTL:190696 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:326:13 KIND:connect :: connect state, UInt<5>(0hb)
[1636] FIRRTL:190697 SRC:<no-source-locator> KIND:else :: else :
[1637] FIRRTL:190698 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:328:22 KIND:node :: node _T_43 = eq(state, UInt<5>(0hb))
[1638] FIRRTL:190699 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:328:41 KIND:when :: when _T_43 :
[1639] FIRRTL:190700 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:329:23 KIND:connect :: connect io.lb_read.offset, refill_ctr
[1640] FIRRTL:190701 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:331:27 KIND:connect :: connect io.refill.valid, UInt<1>(0h1)
[1641] FIRRTL:190702 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_44 = and(io.refill.ready, io.refill.valid)
[1642] FIRRTL:190703 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:332:27 KIND:when :: when _T_44 :
[1643] FIRRTL:190704 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:333:32 KIND:node :: node _refill_ctr_T = add(refill_ctr, UInt<1>(0h1))
[1644] FIRRTL:190705 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:333:32 KIND:node :: node _refill_ctr_T_1 = tail(_refill_ctr_T, 1)
[1645] FIRRTL:190706 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:333:18 KIND:connect :: connect refill_ctr, _refill_ctr_T_1
[1646] FIRRTL:190707 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:334:24 KIND:node :: node _T_45 = eq(refill_ctr, UInt<3>(0h7))
[1647] FIRRTL:190708 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:334:52 KIND:when :: when _T_45 :
[1648] FIRRTL:190709 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:335:15 KIND:connect :: connect state, UInt<5>(0hc)
[1649] FIRRTL:190710 SRC:<no-source-locator> KIND:else :: else :
[1650] FIRRTL:190711 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:338:22 KIND:node :: node _T_46 = eq(state, UInt<5>(0hc))
[1651] FIRRTL:190712 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:338:39 KIND:when :: when _T_46 :
[1652] FIRRTL:190713 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:339:15 KIND:connect :: connect io.replay.bits, rpq.io.deq.bits
[1653] FIRRTL:190714 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:339:15 KIND:connect :: connect io.replay.valid, rpq.io.deq.valid
[1654] FIRRTL:190715 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:339:15 KIND:connect :: connect rpq.io.deq.ready, io.replay.ready
[1655] FIRRTL:190716 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:340:30 KIND:connect :: connect io.replay.bits.way_en, req.way_en
[1656] FIRRTL:190717 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:341:70 KIND:node :: node _io_replay_bits_addr_T = bits(rpq.io.deq.bits.addr, 5, 0)
[1657] FIRRTL:190718 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:341:31 KIND:node :: node io_replay_bits_addr_hi = cat(req_tag, req_idx)
[1658] FIRRTL:190719 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:341:31 KIND:node :: node _io_replay_bits_addr_T_1 = cat(io_replay_bits_addr_hi, _io_replay_bits_addr_T)
[1659] FIRRTL:190720 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:341:25 KIND:connect :: connect io.replay.bits.addr, _io_replay_bits_addr_T_1
[1660] FIRRTL:190721 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_47 = and(io.replay.ready, io.replay.valid)
[1661] FIRRTL:190722 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _T_48 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<1>(0h1))
[1662] FIRRTL:190723 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _T_49 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<5>(0h11))
[1663] FIRRTL:190724 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _T_50 = or(_T_48, _T_49)
[1664] FIRRTL:190725 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _T_51 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h7))
[1665] FIRRTL:190726 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _T_52 = or(_T_50, _T_51)
[1666] FIRRTL:190727 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_53 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h4))
[1667] FIRRTL:190728 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_54 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h9))
[1668] FIRRTL:190729 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_55 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0ha))
[1669] FIRRTL:190730 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_56 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hb))
[1670] FIRRTL:190731 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_57 = or(_T_53, _T_54)
[1671] FIRRTL:190732 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_58 = or(_T_57, _T_55)
[1672] FIRRTL:190733 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_59 = or(_T_58, _T_56)
[1673] FIRRTL:190734 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_60 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h8))
[1674] FIRRTL:190735 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_61 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hc))
[1675] FIRRTL:190736 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_62 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hd))
[1676] FIRRTL:190737 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_63 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0he))
[1677] FIRRTL:190738 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_64 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hf))
[1678] FIRRTL:190739 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_65 = or(_T_60, _T_61)
[1679] FIRRTL:190740 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_66 = or(_T_65, _T_62)
[1680] FIRRTL:190741 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_67 = or(_T_66, _T_63)
[1681] FIRRTL:190742 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_68 = or(_T_67, _T_64)
[1682] FIRRTL:190743 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _T_69 = or(_T_59, _T_68)
[1683] FIRRTL:190744 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _T_70 = or(_T_52, _T_69)
[1684] FIRRTL:190745 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:342:26 KIND:node :: node _T_71 = and(_T_47, _T_70)
[1685] FIRRTL:190746 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:342:67 KIND:when :: when _T_71 :
[1686] FIRRTL:190747 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r_c_cat_T = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<1>(0h1))
[1687] FIRRTL:190748 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r_c_cat_T_1 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<5>(0h11))
[1688] FIRRTL:190749 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r_c_cat_T_2 = or(_r_c_cat_T, _r_c_cat_T_1)
[1689] FIRRTL:190750 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r_c_cat_T_3 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h7))
[1690] FIRRTL:190751 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r_c_cat_T_4 = or(_r_c_cat_T_2, _r_c_cat_T_3)
[1691] FIRRTL:190752 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_5 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h4))
[1692] FIRRTL:190753 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_6 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h9))
[1693] FIRRTL:190754 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_7 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0ha))
[1694] FIRRTL:190755 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_8 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hb))
[1695] FIRRTL:190756 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_9 = or(_r_c_cat_T_5, _r_c_cat_T_6)
[1696] FIRRTL:190757 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_10 = or(_r_c_cat_T_9, _r_c_cat_T_7)
[1697] FIRRTL:190758 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_11 = or(_r_c_cat_T_10, _r_c_cat_T_8)
[1698] FIRRTL:190759 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_12 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h8))
[1699] FIRRTL:190760 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_13 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hc))
[1700] FIRRTL:190761 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_14 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hd))
[1701] FIRRTL:190762 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_15 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0he))
[1702] FIRRTL:190763 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_16 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hf))
[1703] FIRRTL:190764 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_17 = or(_r_c_cat_T_12, _r_c_cat_T_13)
[1704] FIRRTL:190765 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_18 = or(_r_c_cat_T_17, _r_c_cat_T_14)
[1705] FIRRTL:190766 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_19 = or(_r_c_cat_T_18, _r_c_cat_T_15)
[1706] FIRRTL:190767 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_20 = or(_r_c_cat_T_19, _r_c_cat_T_16)
[1707] FIRRTL:190768 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r_c_cat_T_21 = or(_r_c_cat_T_11, _r_c_cat_T_20)
[1708] FIRRTL:190769 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r_c_cat_T_22 = or(_r_c_cat_T_4, _r_c_cat_T_21)
[1709] FIRRTL:190770 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r_c_cat_T_23 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<1>(0h1))
[1710] FIRRTL:190771 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r_c_cat_T_24 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<5>(0h11))
[1711] FIRRTL:190772 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r_c_cat_T_25 = or(_r_c_cat_T_23, _r_c_cat_T_24)
[1712] FIRRTL:190773 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r_c_cat_T_26 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h7))
[1713] FIRRTL:190774 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r_c_cat_T_27 = or(_r_c_cat_T_25, _r_c_cat_T_26)
[1714] FIRRTL:190775 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_28 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h4))
[1715] FIRRTL:190776 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_29 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h9))
[1716] FIRRTL:190777 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_30 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0ha))
[1717] FIRRTL:190778 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_31 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hb))
[1718] FIRRTL:190779 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_32 = or(_r_c_cat_T_28, _r_c_cat_T_29)
[1719] FIRRTL:190780 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_33 = or(_r_c_cat_T_32, _r_c_cat_T_30)
[1720] FIRRTL:190781 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_34 = or(_r_c_cat_T_33, _r_c_cat_T_31)
[1721] FIRRTL:190782 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_35 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0h8))
[1722] FIRRTL:190783 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_36 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hc))
[1723] FIRRTL:190784 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_37 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hd))
[1724] FIRRTL:190785 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_38 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0he))
[1725] FIRRTL:190786 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_39 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<4>(0hf))
[1726] FIRRTL:190787 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_40 = or(_r_c_cat_T_35, _r_c_cat_T_36)
[1727] FIRRTL:190788 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_41 = or(_r_c_cat_T_40, _r_c_cat_T_37)
[1728] FIRRTL:190789 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_42 = or(_r_c_cat_T_41, _r_c_cat_T_38)
[1729] FIRRTL:190790 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_43 = or(_r_c_cat_T_42, _r_c_cat_T_39)
[1730] FIRRTL:190791 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r_c_cat_T_44 = or(_r_c_cat_T_34, _r_c_cat_T_43)
[1731] FIRRTL:190792 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r_c_cat_T_45 = or(_r_c_cat_T_27, _r_c_cat_T_44)
[1732] FIRRTL:190793 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _r_c_cat_T_46 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<2>(0h3))
[1733] FIRRTL:190794 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _r_c_cat_T_47 = or(_r_c_cat_T_45, _r_c_cat_T_46)
[1734] FIRRTL:190795 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _r_c_cat_T_48 = eq(rpq.io.deq.bits.uop.mem_cmd, UInt<3>(0h6))
[1735] FIRRTL:190796 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _r_c_cat_T_49 = or(_r_c_cat_T_47, _r_c_cat_T_48)
[1736] FIRRTL:190797 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node r_c = cat(_r_c_cat_T_22, _r_c_cat_T_49)
[1737] FIRRTL:190798 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _r_T_64 = cat(r_c, new_coh.state)
[1738] FIRRTL:190799 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_65 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1739] FIRRTL:190800 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _r_T_66 = cat(_r_T_65, UInt<2>(0h3))
[1740] FIRRTL:190801 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_67 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1741] FIRRTL:190802 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _r_T_68 = cat(_r_T_67, UInt<2>(0h2))
[1742] FIRRTL:190803 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_69 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1743] FIRRTL:190804 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _r_T_70 = cat(_r_T_69, UInt<2>(0h1))
[1744] FIRRTL:190805 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_71 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1745] FIRRTL:190806 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _r_T_72 = cat(_r_T_71, UInt<2>(0h3))
[1746] FIRRTL:190807 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_73 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1747] FIRRTL:190808 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _r_T_74 = cat(_r_T_73, UInt<2>(0h2))
[1748] FIRRTL:190809 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_75 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1749] FIRRTL:190810 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _r_T_76 = cat(_r_T_75, UInt<2>(0h3))
[1750] FIRRTL:190811 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_77 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1751] FIRRTL:190812 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _r_T_78 = cat(_r_T_77, UInt<2>(0h2))
[1752] FIRRTL:190813 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_79 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1753] FIRRTL:190814 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _r_T_80 = cat(_r_T_79, UInt<2>(0h0))
[1754] FIRRTL:190815 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_81 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1755] FIRRTL:190816 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _r_T_82 = cat(_r_T_81, UInt<2>(0h1))
[1756] FIRRTL:190817 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_83 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1757] FIRRTL:190818 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _r_T_84 = cat(_r_T_83, UInt<2>(0h0))
[1758] FIRRTL:190819 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_85 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1759] FIRRTL:190820 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _r_T_86 = cat(_r_T_85, UInt<2>(0h1))
[1760] FIRRTL:190821 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_87 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1761] FIRRTL:190822 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _r_T_88 = cat(_r_T_87, UInt<2>(0h0))
[1762] FIRRTL:190823 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_89 = eq(_r_T_88, _r_T_64)
[1763] FIRRTL:190824 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_90 = mux(_r_T_89, UInt<1>(0h0), UInt<1>(0h0))
[1764] FIRRTL:190825 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_91 = mux(_r_T_89, UInt<2>(0h1), UInt<1>(0h0))
[1765] FIRRTL:190826 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_92 = eq(_r_T_86, _r_T_64)
[1766] FIRRTL:190827 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_93 = mux(_r_T_92, UInt<1>(0h0), _r_T_90)
[1767] FIRRTL:190828 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_94 = mux(_r_T_92, UInt<2>(0h2), _r_T_91)
[1768] FIRRTL:190829 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_95 = eq(_r_T_84, _r_T_64)
[1769] FIRRTL:190830 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_96 = mux(_r_T_95, UInt<1>(0h0), _r_T_93)
[1770] FIRRTL:190831 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_97 = mux(_r_T_95, UInt<2>(0h1), _r_T_94)
[1771] FIRRTL:190832 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_98 = eq(_r_T_82, _r_T_64)
[1772] FIRRTL:190833 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_99 = mux(_r_T_98, UInt<1>(0h0), _r_T_96)
[1773] FIRRTL:190834 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_100 = mux(_r_T_98, UInt<2>(0h2), _r_T_97)
[1774] FIRRTL:190835 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_101 = eq(_r_T_80, _r_T_64)
[1775] FIRRTL:190836 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_102 = mux(_r_T_101, UInt<1>(0h0), _r_T_99)
[1776] FIRRTL:190837 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_103 = mux(_r_T_101, UInt<2>(0h0), _r_T_100)
[1777] FIRRTL:190838 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_104 = eq(_r_T_78, _r_T_64)
[1778] FIRRTL:190839 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_105 = mux(_r_T_104, UInt<1>(0h1), _r_T_102)
[1779] FIRRTL:190840 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_106 = mux(_r_T_104, UInt<2>(0h3), _r_T_103)
[1780] FIRRTL:190841 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_107 = eq(_r_T_76, _r_T_64)
[1781] FIRRTL:190842 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_108 = mux(_r_T_107, UInt<1>(0h1), _r_T_105)
[1782] FIRRTL:190843 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_109 = mux(_r_T_107, UInt<2>(0h3), _r_T_106)
[1783] FIRRTL:190844 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_110 = eq(_r_T_74, _r_T_64)
[1784] FIRRTL:190845 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_111 = mux(_r_T_110, UInt<1>(0h1), _r_T_108)
[1785] FIRRTL:190846 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_112 = mux(_r_T_110, UInt<2>(0h2), _r_T_109)
[1786] FIRRTL:190847 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_113 = eq(_r_T_72, _r_T_64)
[1787] FIRRTL:190848 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_114 = mux(_r_T_113, UInt<1>(0h1), _r_T_111)
[1788] FIRRTL:190849 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_115 = mux(_r_T_113, UInt<2>(0h3), _r_T_112)
[1789] FIRRTL:190850 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_116 = eq(_r_T_70, _r_T_64)
[1790] FIRRTL:190851 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_117 = mux(_r_T_116, UInt<1>(0h1), _r_T_114)
[1791] FIRRTL:190852 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_118 = mux(_r_T_116, UInt<2>(0h1), _r_T_115)
[1792] FIRRTL:190853 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_119 = eq(_r_T_68, _r_T_64)
[1793] FIRRTL:190854 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_120 = mux(_r_T_119, UInt<1>(0h1), _r_T_117)
[1794] FIRRTL:190855 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_121 = mux(_r_T_119, UInt<2>(0h2), _r_T_118)
[1795] FIRRTL:190856 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_122 = eq(_r_T_66, _r_T_64)
[1796] FIRRTL:190857 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node is_hit = mux(_r_T_122, UInt<1>(0h1), _r_T_120)
[1797] FIRRTL:190858 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node r_2_1 = mux(_r_T_122, UInt<2>(0h3), _r_T_121)
[1798] FIRRTL:190859 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire coh_on_hit : { state : UInt<2>}
[1799] FIRRTL:190860 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect coh_on_hit.state, r_2_1
[1800] FIRRTL:190861 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:node :: node _T_72 = asUInt(reset)
[1801] FIRRTL:190862 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:node :: node _T_73 = eq(_T_72, UInt<1>(0h0))
[1802] FIRRTL:190863 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:when :: when _T_73 :
[1803] FIRRTL:190864 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:node :: node _T_74 = eq(is_hit, UInt<1>(0h0))
[1804] FIRRTL:190865 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:when :: when _T_74 :
[1805] FIRRTL:190866 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: We still don't have permissions for this store\n    at mshrs.scala:345 assert(is_hit, \"We still don't have permissions for this store\")\n") : printf_2
[1806] FIRRTL:190867 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:345:13 KIND:nondriving :: assert(clock, is_hit, UInt<1>(0h1), "") : assert_2
[1807] FIRRTL:190868 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:346:15 KIND:connect :: connect new_coh, coh_on_hit
[1808] FIRRTL:190869 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:348:27 KIND:node :: node _T_75 = eq(rpq.io.enq.valid, UInt<1>(0h0))
[1809] FIRRTL:190870 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:348:24 KIND:node :: node _T_76 = and(rpq.io.empty, _T_75)
[1810] FIRRTL:190871 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:348:46 KIND:when :: when _T_76 :
[1811] FIRRTL:190872 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:349:13 KIND:connect :: connect state, UInt<5>(0hd)
[1812] FIRRTL:190873 SRC:<no-source-locator> KIND:else :: else :
[1813] FIRRTL:190874 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:351:22 KIND:node :: node _T_77 = eq(state, UInt<5>(0hd))
[1814] FIRRTL:190875 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:351:44 KIND:when :: when _T_77 :
[1815] FIRRTL:190876 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:352:33 KIND:connect :: connect io.meta_write.valid, UInt<1>(0h1)
[1816] FIRRTL:190877 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:353:33 KIND:connect :: connect io.meta_write.bits.idx, req_idx
[1817] FIRRTL:190878 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:354:33 KIND:connect :: connect io.meta_write.bits.data.coh, new_coh
[1818] FIRRTL:190879 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:355:33 KIND:connect :: connect io.meta_write.bits.data.tag, req_tag
[1819] FIRRTL:190880 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:356:33 KIND:connect :: connect io.meta_write.bits.way_en, req.way_en
[1820] FIRRTL:190881 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_78 = and(io.meta_write.ready, io.meta_write.valid)
[1821] FIRRTL:190882 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:357:31 KIND:when :: when _T_78 :
[1822] FIRRTL:190883 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:358:13 KIND:connect :: connect state, UInt<5>(0he)
[1823] FIRRTL:190884 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:359:26 KIND:connect :: connect finish_to_prefetch, UInt<1>(0h0)
[1824] FIRRTL:190885 SRC:<no-source-locator> KIND:else :: else :
[1825] FIRRTL:190886 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:361:22 KIND:node :: node _T_79 = eq(state, UInt<5>(0he))
[1826] FIRRTL:190887 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:361:42 KIND:when :: when _T_79 :
[1827] FIRRTL:190888 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:362:25 KIND:connect :: connect io.mem_finish.valid, grantack.valid
[1828] FIRRTL:190889 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_80 = and(io.mem_finish.ready, io.mem_finish.valid)
[1829] FIRRTL:190890 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:363:33 KIND:node :: node _T_81 = eq(grantack.valid, UInt<1>(0h0))
[1830] FIRRTL:190891 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:363:30 KIND:node :: node _T_82 = or(_T_80, _T_81)
[1831] FIRRTL:190892 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:363:50 KIND:when :: when _T_82 :
[1832] FIRRTL:190893 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:364:22 KIND:connect :: connect grantack.valid, UInt<1>(0h0)
[1833] FIRRTL:190894 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:365:13 KIND:connect :: connect state, UInt<5>(0hf)
[1834] FIRRTL:190895 SRC:<no-source-locator> KIND:else :: else :
[1835] FIRRTL:190896 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:367:22 KIND:node :: node _T_83 = eq(state, UInt<5>(0hf))
[1836] FIRRTL:190897 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:367:42 KIND:when :: when _T_83 :
[1837] FIRRTL:190898 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:368:17 KIND:node :: node _state_T_33 = mux(finish_to_prefetch, UInt<5>(0h11), UInt<5>(0h0))
[1838] FIRRTL:190899 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:368:11 KIND:connect :: connect state, _state_T_33
[1839] FIRRTL:190900 SRC:<no-source-locator> KIND:else :: else :
[1840] FIRRTL:190901 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:369:22 KIND:node :: node _T_84 = eq(state, UInt<5>(0h11))
[1841] FIRRTL:190902 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:369:38 KIND:when :: when _T_84 :
[1842] FIRRTL:190903 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:370:20 KIND:connect :: connect io.req_pri_rdy, UInt<1>(0h1)
[1843] FIRRTL:190904 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:371:30 KIND:node :: node _T_85 = eq(io.req_sec_rdy, UInt<1>(0h0))
[1844] FIRRTL:190905 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:371:27 KIND:node :: node _T_86 = and(io.req_sec_val, _T_85)
[1845] FIRRTL:190906 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:371:47 KIND:node :: node _T_87 = or(_T_86, io.clear_prefetch)
[1846] FIRRTL:190907 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:371:69 KIND:when :: when _T_87 :
[1847] FIRRTL:190908 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:372:13 KIND:connect :: connect state, UInt<5>(0h0)
[1848] FIRRTL:190909 SRC:<no-source-locator> KIND:else :: else :
[1849] FIRRTL:190910 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:373:33 KIND:node :: node _T_88 = and(io.req_sec_val, io.req_sec_rdy)
[1850] FIRRTL:190911 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:373:52 KIND:when :: when _T_88 :
[1851] FIRRTL:190912 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r_c_cat_T_50 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[1852] FIRRTL:190913 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r_c_cat_T_51 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[1853] FIRRTL:190914 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r_c_cat_T_52 = or(_r_c_cat_T_50, _r_c_cat_T_51)
[1854] FIRRTL:190915 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r_c_cat_T_53 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[1855] FIRRTL:190916 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r_c_cat_T_54 = or(_r_c_cat_T_52, _r_c_cat_T_53)
[1856] FIRRTL:190917 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_55 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[1857] FIRRTL:190918 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_56 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[1858] FIRRTL:190919 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_57 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[1859] FIRRTL:190920 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_58 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[1860] FIRRTL:190921 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_59 = or(_r_c_cat_T_55, _r_c_cat_T_56)
[1861] FIRRTL:190922 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_60 = or(_r_c_cat_T_59, _r_c_cat_T_57)
[1862] FIRRTL:190923 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_61 = or(_r_c_cat_T_60, _r_c_cat_T_58)
[1863] FIRRTL:190924 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_62 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[1864] FIRRTL:190925 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_63 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[1865] FIRRTL:190926 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_64 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[1866] FIRRTL:190927 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_65 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[1867] FIRRTL:190928 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_66 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[1868] FIRRTL:190929 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_67 = or(_r_c_cat_T_62, _r_c_cat_T_63)
[1869] FIRRTL:190930 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_68 = or(_r_c_cat_T_67, _r_c_cat_T_64)
[1870] FIRRTL:190931 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_69 = or(_r_c_cat_T_68, _r_c_cat_T_65)
[1871] FIRRTL:190932 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_70 = or(_r_c_cat_T_69, _r_c_cat_T_66)
[1872] FIRRTL:190933 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r_c_cat_T_71 = or(_r_c_cat_T_61, _r_c_cat_T_70)
[1873] FIRRTL:190934 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r_c_cat_T_72 = or(_r_c_cat_T_54, _r_c_cat_T_71)
[1874] FIRRTL:190935 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _r_c_cat_T_73 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[1875] FIRRTL:190936 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _r_c_cat_T_74 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[1876] FIRRTL:190937 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _r_c_cat_T_75 = or(_r_c_cat_T_73, _r_c_cat_T_74)
[1877] FIRRTL:190938 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _r_c_cat_T_76 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[1878] FIRRTL:190939 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _r_c_cat_T_77 = or(_r_c_cat_T_75, _r_c_cat_T_76)
[1879] FIRRTL:190940 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_78 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[1880] FIRRTL:190941 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_79 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[1881] FIRRTL:190942 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_80 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[1882] FIRRTL:190943 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_81 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[1883] FIRRTL:190944 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_82 = or(_r_c_cat_T_78, _r_c_cat_T_79)
[1884] FIRRTL:190945 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_83 = or(_r_c_cat_T_82, _r_c_cat_T_80)
[1885] FIRRTL:190946 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_84 = or(_r_c_cat_T_83, _r_c_cat_T_81)
[1886] FIRRTL:190947 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_85 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[1887] FIRRTL:190948 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_86 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[1888] FIRRTL:190949 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_87 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[1889] FIRRTL:190950 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_88 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[1890] FIRRTL:190951 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _r_c_cat_T_89 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[1891] FIRRTL:190952 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_90 = or(_r_c_cat_T_85, _r_c_cat_T_86)
[1892] FIRRTL:190953 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_91 = or(_r_c_cat_T_90, _r_c_cat_T_87)
[1893] FIRRTL:190954 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_92 = or(_r_c_cat_T_91, _r_c_cat_T_88)
[1894] FIRRTL:190955 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _r_c_cat_T_93 = or(_r_c_cat_T_92, _r_c_cat_T_89)
[1895] FIRRTL:190956 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _r_c_cat_T_94 = or(_r_c_cat_T_84, _r_c_cat_T_93)
[1896] FIRRTL:190957 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _r_c_cat_T_95 = or(_r_c_cat_T_77, _r_c_cat_T_94)
[1897] FIRRTL:190958 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _r_c_cat_T_96 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[1898] FIRRTL:190959 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _r_c_cat_T_97 = or(_r_c_cat_T_95, _r_c_cat_T_96)
[1899] FIRRTL:190960 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _r_c_cat_T_98 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[1900] FIRRTL:190961 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _r_c_cat_T_99 = or(_r_c_cat_T_97, _r_c_cat_T_98)
[1901] FIRRTL:190962 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node r_c_1 = cat(_r_c_cat_T_72, _r_c_cat_T_99)
[1902] FIRRTL:190963 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _r_T_123 = cat(r_c_1, new_coh.state)
[1903] FIRRTL:190964 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_124 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1904] FIRRTL:190965 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _r_T_125 = cat(_r_T_124, UInt<2>(0h3))
[1905] FIRRTL:190966 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_126 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1906] FIRRTL:190967 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _r_T_127 = cat(_r_T_126, UInt<2>(0h2))
[1907] FIRRTL:190968 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_128 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1908] FIRRTL:190969 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _r_T_129 = cat(_r_T_128, UInt<2>(0h1))
[1909] FIRRTL:190970 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_130 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1910] FIRRTL:190971 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _r_T_131 = cat(_r_T_130, UInt<2>(0h3))
[1911] FIRRTL:190972 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_132 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1912] FIRRTL:190973 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _r_T_133 = cat(_r_T_132, UInt<2>(0h2))
[1913] FIRRTL:190974 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_134 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1914] FIRRTL:190975 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _r_T_135 = cat(_r_T_134, UInt<2>(0h3))
[1915] FIRRTL:190976 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_136 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1916] FIRRTL:190977 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _r_T_137 = cat(_r_T_136, UInt<2>(0h2))
[1917] FIRRTL:190978 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _r_T_138 = cat(UInt<1>(0h0), UInt<1>(0h0))
[1918] FIRRTL:190979 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _r_T_139 = cat(_r_T_138, UInt<2>(0h0))
[1919] FIRRTL:190980 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_140 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1920] FIRRTL:190981 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _r_T_141 = cat(_r_T_140, UInt<2>(0h1))
[1921] FIRRTL:190982 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _r_T_142 = cat(UInt<1>(0h0), UInt<1>(0h1))
[1922] FIRRTL:190983 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _r_T_143 = cat(_r_T_142, UInt<2>(0h0))
[1923] FIRRTL:190984 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_144 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1924] FIRRTL:190985 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _r_T_145 = cat(_r_T_144, UInt<2>(0h1))
[1925] FIRRTL:190986 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _r_T_146 = cat(UInt<1>(0h1), UInt<1>(0h1))
[1926] FIRRTL:190987 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _r_T_147 = cat(_r_T_146, UInt<2>(0h0))
[1927] FIRRTL:190988 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_148 = eq(_r_T_147, _r_T_123)
[1928] FIRRTL:190989 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_149 = mux(_r_T_148, UInt<1>(0h0), UInt<1>(0h0))
[1929] FIRRTL:190990 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_150 = mux(_r_T_148, UInt<2>(0h1), UInt<1>(0h0))
[1930] FIRRTL:190991 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_151 = eq(_r_T_145, _r_T_123)
[1931] FIRRTL:190992 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_152 = mux(_r_T_151, UInt<1>(0h0), _r_T_149)
[1932] FIRRTL:190993 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_153 = mux(_r_T_151, UInt<2>(0h2), _r_T_150)
[1933] FIRRTL:190994 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_154 = eq(_r_T_143, _r_T_123)
[1934] FIRRTL:190995 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_155 = mux(_r_T_154, UInt<1>(0h0), _r_T_152)
[1935] FIRRTL:190996 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_156 = mux(_r_T_154, UInt<2>(0h1), _r_T_153)
[1936] FIRRTL:190997 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_157 = eq(_r_T_141, _r_T_123)
[1937] FIRRTL:190998 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_158 = mux(_r_T_157, UInt<1>(0h0), _r_T_155)
[1938] FIRRTL:190999 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_159 = mux(_r_T_157, UInt<2>(0h2), _r_T_156)
[1939] FIRRTL:191000 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_160 = eq(_r_T_139, _r_T_123)
[1940] FIRRTL:191001 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_161 = mux(_r_T_160, UInt<1>(0h0), _r_T_158)
[1941] FIRRTL:191002 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_162 = mux(_r_T_160, UInt<2>(0h0), _r_T_159)
[1942] FIRRTL:191003 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_163 = eq(_r_T_137, _r_T_123)
[1943] FIRRTL:191004 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_164 = mux(_r_T_163, UInt<1>(0h1), _r_T_161)
[1944] FIRRTL:191005 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_165 = mux(_r_T_163, UInt<2>(0h3), _r_T_162)
[1945] FIRRTL:191006 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_166 = eq(_r_T_135, _r_T_123)
[1946] FIRRTL:191007 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_167 = mux(_r_T_166, UInt<1>(0h1), _r_T_164)
[1947] FIRRTL:191008 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_168 = mux(_r_T_166, UInt<2>(0h3), _r_T_165)
[1948] FIRRTL:191009 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_169 = eq(_r_T_133, _r_T_123)
[1949] FIRRTL:191010 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_170 = mux(_r_T_169, UInt<1>(0h1), _r_T_167)
[1950] FIRRTL:191011 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_171 = mux(_r_T_169, UInt<2>(0h2), _r_T_168)
[1951] FIRRTL:191012 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_172 = eq(_r_T_131, _r_T_123)
[1952] FIRRTL:191013 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_173 = mux(_r_T_172, UInt<1>(0h1), _r_T_170)
[1953] FIRRTL:191014 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_174 = mux(_r_T_172, UInt<2>(0h3), _r_T_171)
[1954] FIRRTL:191015 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_175 = eq(_r_T_129, _r_T_123)
[1955] FIRRTL:191016 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_176 = mux(_r_T_175, UInt<1>(0h1), _r_T_173)
[1956] FIRRTL:191017 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_177 = mux(_r_T_175, UInt<2>(0h1), _r_T_174)
[1957] FIRRTL:191018 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_178 = eq(_r_T_127, _r_T_123)
[1958] FIRRTL:191019 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _r_T_179 = mux(_r_T_178, UInt<1>(0h1), _r_T_176)
[1959] FIRRTL:191020 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _r_T_180 = mux(_r_T_178, UInt<2>(0h2), _r_T_177)
[1960] FIRRTL:191021 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _r_T_181 = eq(_r_T_125, _r_T_123)
[1961] FIRRTL:191022 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node is_hit_1 = mux(_r_T_181, UInt<1>(0h1), _r_T_179)
[1962] FIRRTL:191023 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node r_2_2 = mux(_r_T_181, UInt<2>(0h3), _r_T_180)
[1963] FIRRTL:191024 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire coh_on_hit_1 : { state : UInt<2>}
[1964] FIRRTL:191025 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect coh_on_hit_1.state, r_2_2
[1965] FIRRTL:191026 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:375:21 KIND:when :: when is_hit_1 :
[1966] FIRRTL:191027 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:376:17 KIND:connect :: connect new_coh, coh_on_hit_1
[1967] FIRRTL:191028 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:377:15 KIND:connect :: connect state, UInt<5>(0h4)
[1968] FIRRTL:191029 SRC:<no-source-locator> KIND:else :: else :
[1969] FIRRTL:191030 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire new_coh_meta_1 : { state : UInt<2>}
[1970] FIRRTL:191031 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect new_coh_meta_1.state, UInt<2>(0h0)
[1971] FIRRTL:191032 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:379:17 KIND:connect :: connect new_coh, new_coh_meta_1
[1972] FIRRTL:191033 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:380:15 KIND:connect :: connect state, UInt<5>(0h1)
[1973] FIRRTL:191034 SRC:<no-source-locator> KIND:else :: else :
[1974] FIRRTL:191035 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:382:33 KIND:node :: node _T_89 = and(io.req_pri_val, io.req_pri_rdy)
[1975] FIRRTL:191036 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:382:52 KIND:when :: when _T_89 :
[1976] FIRRTL:191037 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:383:22 KIND:connect :: connect grant_had_data, UInt<1>(0h0)
[1977] FIRRTL:191038 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:210:29 KIND:wire :: wire state_new_state_1 : UInt
[1978] FIRRTL:191039 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:210:29 KIND:connect :: connect state_new_state_1, state
[1979] FIRRTL:191040 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:211:20 KIND:connect :: connect grantack.valid, UInt<1>(0h0)
[1980] FIRRTL:191041 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:212:16 KIND:connect :: connect refill_ctr, UInt<1>(0h0)
[1981] FIRRTL:191042 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T_34 = asUInt(reset)
[1982] FIRRTL:191043 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T_35 = eq(_state_T_34, UInt<1>(0h0))
[1983] FIRRTL:191044 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:when :: when _state_T_35 :
[1984] FIRRTL:191045 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:node :: node _state_T_36 = eq(rpq.io.enq.ready, UInt<1>(0h0))
[1985] FIRRTL:191046 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:when :: when _state_T_36 :
[1986] FIRRTL:191047 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:213 assert(rpq.io.enq.ready)\n") : state_printf_2
[1987] FIRRTL:191048 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:213:11 KIND:nondriving :: assert(clock, rpq.io.enq.ready, UInt<1>(0h1), "") : state_assert_2
[1988] FIRRTL:191049 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:214:9 KIND:connect :: connect req, io.req
[1989] FIRRTL:191050 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_64 = eq(UInt<5>(0h10), UInt<5>(0h10))
[1990] FIRRTL:191051 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_65 = mux(_state_req_needs_wb_r_T_64, UInt<2>(0h2), UInt<2>(0h2))
[1991] FIRRTL:191052 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_66 = eq(UInt<5>(0h12), UInt<5>(0h10))
[1992] FIRRTL:191053 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_67 = mux(_state_req_needs_wb_r_T_66, UInt<2>(0h1), _state_req_needs_wb_r_T_65)
[1993] FIRRTL:191054 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_68 = eq(UInt<5>(0h13), UInt<5>(0h10))
[1994] FIRRTL:191055 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:140:24 KIND:node :: node _state_req_needs_wb_r_T_69 = mux(_state_req_needs_wb_r_T_68, UInt<2>(0h0), _state_req_needs_wb_r_T_67)
[1995] FIRRTL:191056 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:120:19 KIND:node :: node _state_req_needs_wb_r_T_70 = cat(_state_req_needs_wb_r_T_69, io.req.old_meta.coh.state)
[1996] FIRRTL:191057 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:122:10 KIND:node :: node _state_req_needs_wb_r_T_71 = cat(UInt<2>(0h0), UInt<2>(0h3))
[1997] FIRRTL:191058 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:123:10 KIND:node :: node _state_req_needs_wb_r_T_72 = cat(UInt<2>(0h0), UInt<2>(0h2))
[1998] FIRRTL:191059 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:124:10 KIND:node :: node _state_req_needs_wb_r_T_73 = cat(UInt<2>(0h0), UInt<2>(0h1))
[1999] FIRRTL:191060 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:125:10 KIND:node :: node _state_req_needs_wb_r_T_74 = cat(UInt<2>(0h0), UInt<2>(0h0))
[2000] FIRRTL:191061 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:126:10 KIND:node :: node _state_req_needs_wb_r_T_75 = cat(UInt<2>(0h1), UInt<2>(0h3))
[2001] FIRRTL:191062 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:127:10 KIND:node :: node _state_req_needs_wb_r_T_76 = cat(UInt<2>(0h1), UInt<2>(0h2))
[2002] FIRRTL:191063 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:128:10 KIND:node :: node _state_req_needs_wb_r_T_77 = cat(UInt<2>(0h1), UInt<2>(0h1))
[2003] FIRRTL:191064 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:129:10 KIND:node :: node _state_req_needs_wb_r_T_78 = cat(UInt<2>(0h1), UInt<2>(0h0))
[2004] FIRRTL:191065 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:130:10 KIND:node :: node _state_req_needs_wb_r_T_79 = cat(UInt<2>(0h2), UInt<2>(0h3))
[2005] FIRRTL:191066 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:131:10 KIND:node :: node _state_req_needs_wb_r_T_80 = cat(UInt<2>(0h2), UInt<2>(0h2))
[2006] FIRRTL:191067 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:132:10 KIND:node :: node _state_req_needs_wb_r_T_81 = cat(UInt<2>(0h2), UInt<2>(0h1))
[2007] FIRRTL:191068 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:133:10 KIND:node :: node _state_req_needs_wb_r_T_82 = cat(UInt<2>(0h2), UInt<2>(0h0))
[2008] FIRRTL:191069 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_83 = eq(_state_req_needs_wb_r_T_82, _state_req_needs_wb_r_T_70)
[2009] FIRRTL:191070 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_84 = mux(_state_req_needs_wb_r_T_83, UInt<1>(0h0), UInt<1>(0h0))
[2010] FIRRTL:191071 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_85 = mux(_state_req_needs_wb_r_T_83, UInt<3>(0h5), UInt<1>(0h0))
[2011] FIRRTL:191072 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_86 = mux(_state_req_needs_wb_r_T_83, UInt<2>(0h0), UInt<1>(0h0))
[2012] FIRRTL:191073 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_87 = eq(_state_req_needs_wb_r_T_81, _state_req_needs_wb_r_T_70)
[2013] FIRRTL:191074 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_88 = mux(_state_req_needs_wb_r_T_87, UInt<1>(0h0), _state_req_needs_wb_r_T_84)
[2014] FIRRTL:191075 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_89 = mux(_state_req_needs_wb_r_T_87, UInt<3>(0h2), _state_req_needs_wb_r_T_85)
[2015] FIRRTL:191076 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_90 = mux(_state_req_needs_wb_r_T_87, UInt<2>(0h0), _state_req_needs_wb_r_T_86)
[2016] FIRRTL:191077 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_91 = eq(_state_req_needs_wb_r_T_80, _state_req_needs_wb_r_T_70)
[2017] FIRRTL:191078 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_92 = mux(_state_req_needs_wb_r_T_91, UInt<1>(0h0), _state_req_needs_wb_r_T_88)
[2018] FIRRTL:191079 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_93 = mux(_state_req_needs_wb_r_T_91, UInt<3>(0h1), _state_req_needs_wb_r_T_89)
[2019] FIRRTL:191080 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_94 = mux(_state_req_needs_wb_r_T_91, UInt<2>(0h0), _state_req_needs_wb_r_T_90)
[2020] FIRRTL:191081 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_95 = eq(_state_req_needs_wb_r_T_79, _state_req_needs_wb_r_T_70)
[2021] FIRRTL:191082 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_96 = mux(_state_req_needs_wb_r_T_95, UInt<1>(0h1), _state_req_needs_wb_r_T_92)
[2022] FIRRTL:191083 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_97 = mux(_state_req_needs_wb_r_T_95, UInt<3>(0h1), _state_req_needs_wb_r_T_93)
[2023] FIRRTL:191084 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_98 = mux(_state_req_needs_wb_r_T_95, UInt<2>(0h0), _state_req_needs_wb_r_T_94)
[2024] FIRRTL:191085 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_99 = eq(_state_req_needs_wb_r_T_78, _state_req_needs_wb_r_T_70)
[2025] FIRRTL:191086 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_100 = mux(_state_req_needs_wb_r_T_99, UInt<1>(0h0), _state_req_needs_wb_r_T_96)
[2026] FIRRTL:191087 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_101 = mux(_state_req_needs_wb_r_T_99, UInt<3>(0h5), _state_req_needs_wb_r_T_97)
[2027] FIRRTL:191088 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_102 = mux(_state_req_needs_wb_r_T_99, UInt<2>(0h0), _state_req_needs_wb_r_T_98)
[2028] FIRRTL:191089 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_103 = eq(_state_req_needs_wb_r_T_77, _state_req_needs_wb_r_T_70)
[2029] FIRRTL:191090 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_104 = mux(_state_req_needs_wb_r_T_103, UInt<1>(0h0), _state_req_needs_wb_r_T_100)
[2030] FIRRTL:191091 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_105 = mux(_state_req_needs_wb_r_T_103, UInt<3>(0h4), _state_req_needs_wb_r_T_101)
[2031] FIRRTL:191092 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_106 = mux(_state_req_needs_wb_r_T_103, UInt<2>(0h1), _state_req_needs_wb_r_T_102)
[2032] FIRRTL:191093 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_107 = eq(_state_req_needs_wb_r_T_76, _state_req_needs_wb_r_T_70)
[2033] FIRRTL:191094 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_108 = mux(_state_req_needs_wb_r_T_107, UInt<1>(0h0), _state_req_needs_wb_r_T_104)
[2034] FIRRTL:191095 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_109 = mux(_state_req_needs_wb_r_T_107, UInt<3>(0h0), _state_req_needs_wb_r_T_105)
[2035] FIRRTL:191096 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_110 = mux(_state_req_needs_wb_r_T_107, UInt<2>(0h1), _state_req_needs_wb_r_T_106)
[2036] FIRRTL:191097 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_111 = eq(_state_req_needs_wb_r_T_75, _state_req_needs_wb_r_T_70)
[2037] FIRRTL:191098 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_112 = mux(_state_req_needs_wb_r_T_111, UInt<1>(0h1), _state_req_needs_wb_r_T_108)
[2038] FIRRTL:191099 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_113 = mux(_state_req_needs_wb_r_T_111, UInt<3>(0h0), _state_req_needs_wb_r_T_109)
[2039] FIRRTL:191100 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_114 = mux(_state_req_needs_wb_r_T_111, UInt<2>(0h1), _state_req_needs_wb_r_T_110)
[2040] FIRRTL:191101 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_115 = eq(_state_req_needs_wb_r_T_74, _state_req_needs_wb_r_T_70)
[2041] FIRRTL:191102 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_116 = mux(_state_req_needs_wb_r_T_115, UInt<1>(0h0), _state_req_needs_wb_r_T_112)
[2042] FIRRTL:191103 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_117 = mux(_state_req_needs_wb_r_T_115, UInt<3>(0h5), _state_req_needs_wb_r_T_113)
[2043] FIRRTL:191104 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_118 = mux(_state_req_needs_wb_r_T_115, UInt<2>(0h0), _state_req_needs_wb_r_T_114)
[2044] FIRRTL:191105 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_119 = eq(_state_req_needs_wb_r_T_73, _state_req_needs_wb_r_T_70)
[2045] FIRRTL:191106 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_120 = mux(_state_req_needs_wb_r_T_119, UInt<1>(0h0), _state_req_needs_wb_r_T_116)
[2046] FIRRTL:191107 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_121 = mux(_state_req_needs_wb_r_T_119, UInt<3>(0h4), _state_req_needs_wb_r_T_117)
[2047] FIRRTL:191108 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_122 = mux(_state_req_needs_wb_r_T_119, UInt<2>(0h1), _state_req_needs_wb_r_T_118)
[2048] FIRRTL:191109 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_123 = eq(_state_req_needs_wb_r_T_72, _state_req_needs_wb_r_T_70)
[2049] FIRRTL:191110 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _state_req_needs_wb_r_T_124 = mux(_state_req_needs_wb_r_T_123, UInt<1>(0h0), _state_req_needs_wb_r_T_120)
[2050] FIRRTL:191111 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _state_req_needs_wb_r_T_125 = mux(_state_req_needs_wb_r_T_123, UInt<3>(0h3), _state_req_needs_wb_r_T_121)
[2051] FIRRTL:191112 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _state_req_needs_wb_r_T_126 = mux(_state_req_needs_wb_r_T_123, UInt<2>(0h2), _state_req_needs_wb_r_T_122)
[2052] FIRRTL:191113 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _state_req_needs_wb_r_T_127 = eq(_state_req_needs_wb_r_T_71, _state_req_needs_wb_r_T_70)
[2053] FIRRTL:191114 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node state_req_needs_wb_r_1_1 = mux(_state_req_needs_wb_r_T_127, UInt<1>(0h1), _state_req_needs_wb_r_T_124)
[2054] FIRRTL:191115 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node state_req_needs_wb_r_2_1 = mux(_state_req_needs_wb_r_T_127, UInt<3>(0h3), _state_req_needs_wb_r_T_125)
[2055] FIRRTL:191116 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node state_req_needs_wb_r_3_1 = mux(_state_req_needs_wb_r_T_127, UInt<2>(0h2), _state_req_needs_wb_r_T_126)
[2056] FIRRTL:191117 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_req_needs_wb_meta_1 : { state : UInt<2>}
[2057] FIRRTL:191118 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_req_needs_wb_meta_1.state, state_req_needs_wb_r_3_1
[2058] FIRRTL:191119 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:216:18 KIND:connect :: connect req_needs_wb, state_req_needs_wb_r_1_1
[2059] FIRRTL:191120 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:217:29 KIND:when :: when io.req.tag_match :
[2060] FIRRTL:191121 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_r_c_cat_T_50 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[2061] FIRRTL:191122 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_r_c_cat_T_51 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[2062] FIRRTL:191123 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_r_c_cat_T_52 = or(_state_r_c_cat_T_50, _state_r_c_cat_T_51)
[2063] FIRRTL:191124 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_r_c_cat_T_53 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[2064] FIRRTL:191125 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_r_c_cat_T_54 = or(_state_r_c_cat_T_52, _state_r_c_cat_T_53)
[2065] FIRRTL:191126 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_55 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[2066] FIRRTL:191127 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_56 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[2067] FIRRTL:191128 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_57 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[2068] FIRRTL:191129 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_58 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[2069] FIRRTL:191130 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_59 = or(_state_r_c_cat_T_55, _state_r_c_cat_T_56)
[2070] FIRRTL:191131 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_60 = or(_state_r_c_cat_T_59, _state_r_c_cat_T_57)
[2071] FIRRTL:191132 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_61 = or(_state_r_c_cat_T_60, _state_r_c_cat_T_58)
[2072] FIRRTL:191133 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_62 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[2073] FIRRTL:191134 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_63 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[2074] FIRRTL:191135 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_64 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[2075] FIRRTL:191136 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_65 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[2076] FIRRTL:191137 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_66 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[2077] FIRRTL:191138 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_67 = or(_state_r_c_cat_T_62, _state_r_c_cat_T_63)
[2078] FIRRTL:191139 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_68 = or(_state_r_c_cat_T_67, _state_r_c_cat_T_64)
[2079] FIRRTL:191140 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_69 = or(_state_r_c_cat_T_68, _state_r_c_cat_T_65)
[2080] FIRRTL:191141 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_70 = or(_state_r_c_cat_T_69, _state_r_c_cat_T_66)
[2081] FIRRTL:191142 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_r_c_cat_T_71 = or(_state_r_c_cat_T_61, _state_r_c_cat_T_70)
[2082] FIRRTL:191143 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_r_c_cat_T_72 = or(_state_r_c_cat_T_54, _state_r_c_cat_T_71)
[2083] FIRRTL:191144 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_r_c_cat_T_73 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[2084] FIRRTL:191145 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_r_c_cat_T_74 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[2085] FIRRTL:191146 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_r_c_cat_T_75 = or(_state_r_c_cat_T_73, _state_r_c_cat_T_74)
[2086] FIRRTL:191147 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_r_c_cat_T_76 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[2087] FIRRTL:191148 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_r_c_cat_T_77 = or(_state_r_c_cat_T_75, _state_r_c_cat_T_76)
[2088] FIRRTL:191149 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_78 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[2089] FIRRTL:191150 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_79 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[2090] FIRRTL:191151 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_80 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[2091] FIRRTL:191152 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_81 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[2092] FIRRTL:191153 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_82 = or(_state_r_c_cat_T_78, _state_r_c_cat_T_79)
[2093] FIRRTL:191154 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_83 = or(_state_r_c_cat_T_82, _state_r_c_cat_T_80)
[2094] FIRRTL:191155 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_84 = or(_state_r_c_cat_T_83, _state_r_c_cat_T_81)
[2095] FIRRTL:191156 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_85 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[2096] FIRRTL:191157 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_86 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[2097] FIRRTL:191158 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_87 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[2098] FIRRTL:191159 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_88 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[2099] FIRRTL:191160 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_r_c_cat_T_89 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[2100] FIRRTL:191161 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_90 = or(_state_r_c_cat_T_85, _state_r_c_cat_T_86)
[2101] FIRRTL:191162 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_91 = or(_state_r_c_cat_T_90, _state_r_c_cat_T_87)
[2102] FIRRTL:191163 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_92 = or(_state_r_c_cat_T_91, _state_r_c_cat_T_88)
[2103] FIRRTL:191164 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_r_c_cat_T_93 = or(_state_r_c_cat_T_92, _state_r_c_cat_T_89)
[2104] FIRRTL:191165 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_r_c_cat_T_94 = or(_state_r_c_cat_T_84, _state_r_c_cat_T_93)
[2105] FIRRTL:191166 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_r_c_cat_T_95 = or(_state_r_c_cat_T_77, _state_r_c_cat_T_94)
[2106] FIRRTL:191167 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:54 KIND:node :: node _state_r_c_cat_T_96 = eq(io.req.uop.mem_cmd, UInt<2>(0h3))
[2107] FIRRTL:191168 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:47 KIND:node :: node _state_r_c_cat_T_97 = or(_state_r_c_cat_T_95, _state_r_c_cat_T_96)
[2108] FIRRTL:191169 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:71 KIND:node :: node _state_r_c_cat_T_98 = eq(io.req.uop.mem_cmd, UInt<3>(0h6))
[2109] FIRRTL:191170 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:91:64 KIND:node :: node _state_r_c_cat_T_99 = or(_state_r_c_cat_T_97, _state_r_c_cat_T_98)
[2110] FIRRTL:191171 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:29:18 KIND:node :: node state_r_c_1 = cat(_state_r_c_cat_T_72, _state_r_c_cat_T_99)
[2111] FIRRTL:191172 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:58:19 KIND:node :: node _state_r_T_59 = cat(state_r_c_1, io.req.old_meta.coh.state)
[2112] FIRRTL:191173 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_60 = cat(UInt<1>(0h0), UInt<1>(0h0))
[2113] FIRRTL:191174 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:60:10 KIND:node :: node _state_r_T_61 = cat(_state_r_T_60, UInt<2>(0h3))
[2114] FIRRTL:191175 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_62 = cat(UInt<1>(0h0), UInt<1>(0h0))
[2115] FIRRTL:191176 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:61:10 KIND:node :: node _state_r_T_63 = cat(_state_r_T_62, UInt<2>(0h2))
[2116] FIRRTL:191177 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_64 = cat(UInt<1>(0h0), UInt<1>(0h0))
[2117] FIRRTL:191178 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:62:10 KIND:node :: node _state_r_T_65 = cat(_state_r_T_64, UInt<2>(0h1))
[2118] FIRRTL:191179 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_66 = cat(UInt<1>(0h0), UInt<1>(0h1))
[2119] FIRRTL:191180 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:63:10 KIND:node :: node _state_r_T_67 = cat(_state_r_T_66, UInt<2>(0h3))
[2120] FIRRTL:191181 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_68 = cat(UInt<1>(0h0), UInt<1>(0h1))
[2121] FIRRTL:191182 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:64:10 KIND:node :: node _state_r_T_69 = cat(_state_r_T_68, UInt<2>(0h2))
[2122] FIRRTL:191183 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_70 = cat(UInt<1>(0h1), UInt<1>(0h1))
[2123] FIRRTL:191184 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:65:10 KIND:node :: node _state_r_T_71 = cat(_state_r_T_70, UInt<2>(0h3))
[2124] FIRRTL:191185 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_72 = cat(UInt<1>(0h1), UInt<1>(0h1))
[2125] FIRRTL:191186 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:66:10 KIND:node :: node _state_r_T_73 = cat(_state_r_T_72, UInt<2>(0h2))
[2126] FIRRTL:191187 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:26:15 KIND:node :: node _state_r_T_74 = cat(UInt<1>(0h0), UInt<1>(0h0))
[2127] FIRRTL:191188 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:68:10 KIND:node :: node _state_r_T_75 = cat(_state_r_T_74, UInt<2>(0h0))
[2128] FIRRTL:191189 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_76 = cat(UInt<1>(0h0), UInt<1>(0h1))
[2129] FIRRTL:191190 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:69:10 KIND:node :: node _state_r_T_77 = cat(_state_r_T_76, UInt<2>(0h1))
[2130] FIRRTL:191191 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:25:15 KIND:node :: node _state_r_T_78 = cat(UInt<1>(0h0), UInt<1>(0h1))
[2131] FIRRTL:191192 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:70:10 KIND:node :: node _state_r_T_79 = cat(_state_r_T_78, UInt<2>(0h0))
[2132] FIRRTL:191193 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_80 = cat(UInt<1>(0h1), UInt<1>(0h1))
[2133] FIRRTL:191194 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:71:10 KIND:node :: node _state_r_T_81 = cat(_state_r_T_80, UInt<2>(0h1))
[2134] FIRRTL:191195 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:24:15 KIND:node :: node _state_r_T_82 = cat(UInt<1>(0h1), UInt<1>(0h1))
[2135] FIRRTL:191196 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:72:10 KIND:node :: node _state_r_T_83 = cat(_state_r_T_82, UInt<2>(0h0))
[2136] FIRRTL:191197 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_84 = eq(_state_r_T_83, _state_r_T_59)
[2137] FIRRTL:191198 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_85 = mux(_state_r_T_84, UInt<1>(0h0), UInt<1>(0h0))
[2138] FIRRTL:191199 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_86 = mux(_state_r_T_84, UInt<2>(0h1), UInt<1>(0h0))
[2139] FIRRTL:191200 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_87 = eq(_state_r_T_81, _state_r_T_59)
[2140] FIRRTL:191201 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_88 = mux(_state_r_T_87, UInt<1>(0h0), _state_r_T_85)
[2141] FIRRTL:191202 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_89 = mux(_state_r_T_87, UInt<2>(0h2), _state_r_T_86)
[2142] FIRRTL:191203 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_90 = eq(_state_r_T_79, _state_r_T_59)
[2143] FIRRTL:191204 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_91 = mux(_state_r_T_90, UInt<1>(0h0), _state_r_T_88)
[2144] FIRRTL:191205 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_92 = mux(_state_r_T_90, UInt<2>(0h1), _state_r_T_89)
[2145] FIRRTL:191206 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_93 = eq(_state_r_T_77, _state_r_T_59)
[2146] FIRRTL:191207 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_94 = mux(_state_r_T_93, UInt<1>(0h0), _state_r_T_91)
[2147] FIRRTL:191208 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_95 = mux(_state_r_T_93, UInt<2>(0h2), _state_r_T_92)
[2148] FIRRTL:191209 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_96 = eq(_state_r_T_75, _state_r_T_59)
[2149] FIRRTL:191210 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_97 = mux(_state_r_T_96, UInt<1>(0h0), _state_r_T_94)
[2150] FIRRTL:191211 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_98 = mux(_state_r_T_96, UInt<2>(0h0), _state_r_T_95)
[2151] FIRRTL:191212 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_99 = eq(_state_r_T_73, _state_r_T_59)
[2152] FIRRTL:191213 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_100 = mux(_state_r_T_99, UInt<1>(0h1), _state_r_T_97)
[2153] FIRRTL:191214 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_101 = mux(_state_r_T_99, UInt<2>(0h3), _state_r_T_98)
[2154] FIRRTL:191215 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_102 = eq(_state_r_T_71, _state_r_T_59)
[2155] FIRRTL:191216 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_103 = mux(_state_r_T_102, UInt<1>(0h1), _state_r_T_100)
[2156] FIRRTL:191217 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_104 = mux(_state_r_T_102, UInt<2>(0h3), _state_r_T_101)
[2157] FIRRTL:191218 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_105 = eq(_state_r_T_69, _state_r_T_59)
[2158] FIRRTL:191219 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_106 = mux(_state_r_T_105, UInt<1>(0h1), _state_r_T_103)
[2159] FIRRTL:191220 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_107 = mux(_state_r_T_105, UInt<2>(0h2), _state_r_T_104)
[2160] FIRRTL:191221 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_108 = eq(_state_r_T_67, _state_r_T_59)
[2161] FIRRTL:191222 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_109 = mux(_state_r_T_108, UInt<1>(0h1), _state_r_T_106)
[2162] FIRRTL:191223 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_110 = mux(_state_r_T_108, UInt<2>(0h3), _state_r_T_107)
[2163] FIRRTL:191224 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_111 = eq(_state_r_T_65, _state_r_T_59)
[2164] FIRRTL:191225 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_112 = mux(_state_r_T_111, UInt<1>(0h1), _state_r_T_109)
[2165] FIRRTL:191226 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_113 = mux(_state_r_T_111, UInt<2>(0h1), _state_r_T_110)
[2166] FIRRTL:191227 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_114 = eq(_state_r_T_63, _state_r_T_59)
[2167] FIRRTL:191228 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node _state_r_T_115 = mux(_state_r_T_114, UInt<1>(0h1), _state_r_T_112)
[2168] FIRRTL:191229 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node _state_r_T_116 = mux(_state_r_T_114, UInt<2>(0h2), _state_r_T_113)
[2169] FIRRTL:191230 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:49:20 KIND:node :: node _state_r_T_117 = eq(_state_r_T_61, _state_r_T_59)
[2170] FIRRTL:191231 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:9 KIND:node :: node state_is_hit_1 = mux(_state_r_T_117, UInt<1>(0h1), _state_r_T_115)
[2171] FIRRTL:191232 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:35:36 KIND:node :: node state_r_2_1 = mux(_state_r_T_117, UInt<2>(0h3), _state_r_T_116)
[2172] FIRRTL:191233 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_coh_on_hit_1 : { state : UInt<2>}
[2173] FIRRTL:191234 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_coh_on_hit_1.state, state_r_2_1
[2174] FIRRTL:191235 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:219:21 KIND:when :: when state_is_hit_1 :
[2175] FIRRTL:191236 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _state_T_37 = eq(io.req.uop.mem_cmd, UInt<1>(0h1))
[2176] FIRRTL:191237 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _state_T_38 = eq(io.req.uop.mem_cmd, UInt<5>(0h11))
[2177] FIRRTL:191238 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _state_T_39 = or(_state_T_37, _state_T_38)
[2178] FIRRTL:191239 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _state_T_40 = eq(io.req.uop.mem_cmd, UInt<3>(0h7))
[2179] FIRRTL:191240 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _state_T_41 = or(_state_T_39, _state_T_40)
[2180] FIRRTL:191241 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_42 = eq(io.req.uop.mem_cmd, UInt<3>(0h4))
[2181] FIRRTL:191242 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_43 = eq(io.req.uop.mem_cmd, UInt<4>(0h9))
[2182] FIRRTL:191243 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_44 = eq(io.req.uop.mem_cmd, UInt<4>(0ha))
[2183] FIRRTL:191244 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_45 = eq(io.req.uop.mem_cmd, UInt<4>(0hb))
[2184] FIRRTL:191245 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_46 = or(_state_T_42, _state_T_43)
[2185] FIRRTL:191246 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_47 = or(_state_T_46, _state_T_44)
[2186] FIRRTL:191247 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_48 = or(_state_T_47, _state_T_45)
[2187] FIRRTL:191248 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_49 = eq(io.req.uop.mem_cmd, UInt<4>(0h8))
[2188] FIRRTL:191249 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_50 = eq(io.req.uop.mem_cmd, UInt<4>(0hc))
[2189] FIRRTL:191250 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_51 = eq(io.req.uop.mem_cmd, UInt<4>(0hd))
[2190] FIRRTL:191251 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_52 = eq(io.req.uop.mem_cmd, UInt<4>(0he))
[2191] FIRRTL:191252 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _state_T_53 = eq(io.req.uop.mem_cmd, UInt<4>(0hf))
[2192] FIRRTL:191253 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_54 = or(_state_T_49, _state_T_50)
[2193] FIRRTL:191254 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_55 = or(_state_T_54, _state_T_51)
[2194] FIRRTL:191255 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_56 = or(_state_T_55, _state_T_52)
[2195] FIRRTL:191256 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _state_T_57 = or(_state_T_56, _state_T_53)
[2196] FIRRTL:191257 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _state_T_58 = or(_state_T_48, _state_T_57)
[2197] FIRRTL:191258 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _state_T_59 = or(_state_T_41, _state_T_58)
[2198] FIRRTL:191259 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_60 = asUInt(reset)
[2199] FIRRTL:191260 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_61 = eq(_state_T_60, UInt<1>(0h0))
[2200] FIRRTL:191261 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:when :: when _state_T_61 :
[2201] FIRRTL:191262 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:node :: node _state_T_62 = eq(_state_T_59, UInt<1>(0h0))
[2202] FIRRTL:191263 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:when :: when _state_T_62 :
[2203] FIRRTL:191264 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:220 assert(isWrite(io.req.uop.mem_cmd))\n") : state_printf_3
[2204] FIRRTL:191265 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:220:15 KIND:nondriving :: assert(clock, _state_T_59, UInt<1>(0h1), "") : state_assert_3
[2205] FIRRTL:191266 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:221:21 KIND:connect :: connect new_coh, state_coh_on_hit_1
[2206] FIRRTL:191267 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:222:21 KIND:connect :: connect state_new_state_1, UInt<5>(0hc)
[2207] FIRRTL:191268 SRC:<no-source-locator> KIND:else :: else :
[2208] FIRRTL:191269 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:224:21 KIND:connect :: connect new_coh, io.req.old_meta.coh
[2209] FIRRTL:191270 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:225:21 KIND:connect :: connect state_new_state_1, UInt<5>(0h1)
[2210] FIRRTL:191271 SRC:<no-source-locator> KIND:else :: else :
[2211] FIRRTL:191272 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire state_new_coh_meta_1 : { state : UInt<2>}
[2212] FIRRTL:191273 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect state_new_coh_meta_1.state, UInt<2>(0h0)
[2213] FIRRTL:191274 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:228:19 KIND:connect :: connect new_coh, state_new_coh_meta_1
[2214] FIRRTL:191275 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:229:19 KIND:connect :: connect state_new_state_1, UInt<5>(0h1)
[2215] FIRRTL:191276 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:384:13 KIND:connect :: connect state, state_new_state_1
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
  "task_id": "parent_synthesis-BoomMSHR-6362a83e7f824669",
  "work_unit_id": "BoomMSHR",
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
