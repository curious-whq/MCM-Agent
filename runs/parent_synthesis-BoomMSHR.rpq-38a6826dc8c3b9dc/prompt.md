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

Task ID: `parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `parent-synthesis-prompt-0.1`
Output schema version: `umcm-formal-0.5`

## Parent WorkUnit

- id: `BoomMSHR.rpq`
- module: `BranchKillableQueue_1`
- kind: `module`
- instance path: `BoomMSHR.rpq`
- leaf: `False`
- coverage complete: `True`
- parent-local raw statements after child replacement: 176
- parent-local logical statements after child replacement: 36
- parent-local registers: 3
- parent-local physical boundary events: 2

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

- `BoomMSHR.rpq::io.deq.fire`
  - predicate: `io.deq.valid && io.deq.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.deq.bits.addr', 'io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.old_meta.coh.state', 'io.deq.bits.old_meta.tag', 'io.deq.bits.sdq_id', 'io.deq.bits.tag_match', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.bits.way_en']
  - immediate registers: ['out_valid']
  - historical registers: ['out_reg', 'out_uop', 'out_valid']
- `BoomMSHR.rpq::io.enq.fire`
  - predicate: `io.enq.valid && io.enq.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.enq.bits.addr', 'io.enq.bits.data', 'io.enq.bits.is_hella', 'io.enq.bits.old_meta.coh.state', 'io.enq.bits.old_meta.tag', 'io.enq.bits.sdq_id', 'io.enq.bits.tag_match', 'io.enq.bits.uop.bp_debug_if', 'io.enq.bits.uop.bp_xcpt_if', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.br_tag', 'io.enq.bits.uop.br_type', 'io.enq.bits.uop.csr_cmd', 'io.enq.bits.uop.debug_fsrc', 'io.enq.bits.uop.debug_inst', 'io.enq.bits.uop.debug_pc', 'io.enq.bits.uop.debug_tsrc', 'io.enq.bits.uop.dis_col_sel', 'io.enq.bits.uop.dst_rtype', 'io.enq.bits.uop.edge_inst', 'io.enq.bits.uop.exc_cause', 'io.enq.bits.uop.exception', 'io.enq.bits.uop.fcn_dw', 'io.enq.bits.uop.fcn_op', 'io.enq.bits.uop.flush_on_commit', 'io.enq.bits.uop.fp_ctrl.div', 'io.enq.bits.uop.fp_ctrl.fastpipe', 'io.enq.bits.uop.fp_ctrl.fma', 'io.enq.bits.uop.fp_ctrl.fromint', 'io.enq.bits.uop.fp_ctrl.ldst', 'io.enq.bits.uop.fp_ctrl.ren1', 'io.enq.bits.uop.fp_ctrl.ren2', 'io.enq.bits.uop.fp_ctrl.ren3', 'io.enq.bits.uop.fp_ctrl.sqrt', 'io.enq.bits.uop.fp_ctrl.swap12', 'io.enq.bits.uop.fp_ctrl.swap23', 'io.enq.bits.uop.fp_ctrl.toint', 'io.enq.bits.uop.fp_ctrl.typeTagIn', 'io.enq.bits.uop.fp_ctrl.typeTagOut', 'io.enq.bits.uop.fp_ctrl.vec', 'io.enq.bits.uop.fp_ctrl.wen', 'io.enq.bits.uop.fp_ctrl.wflags', 'io.enq.bits.uop.fp_rm', 'io.enq.bits.uop.fp_typ', 'io.enq.bits.uop.fp_val', 'io.enq.bits.uop.frs3_en', 'io.enq.bits.uop.ftq_idx', 'io.enq.bits.uop.fu_code[0]', 'io.enq.bits.uop.fu_code[1]', 'io.enq.bits.uop.fu_code[2]', 'io.enq.bits.uop.fu_code[3]', 'io.enq.bits.uop.fu_code[4]', 'io.enq.bits.uop.fu_code[5]', 'io.enq.bits.uop.fu_code[6]', 'io.enq.bits.uop.fu_code[7]', 'io.enq.bits.uop.fu_code[8]', 'io.enq.bits.uop.fu_code[9]', 'io.enq.bits.uop.imm_packed', 'io.enq.bits.uop.imm_rename', 'io.enq.bits.uop.imm_sel', 'io.enq.bits.uop.inst', 'io.enq.bits.uop.iq_type[0]', 'io.enq.bits.uop.iq_type[1]', 'io.enq.bits.uop.iq_type[2]', 'io.enq.bits.uop.iq_type[3]', 'io.enq.bits.uop.is_amo', 'io.enq.bits.uop.is_eret', 'io.enq.bits.uop.is_fence', 'io.enq.bits.uop.is_fencei', 'io.enq.bits.uop.is_mov', 'io.enq.bits.uop.is_rocc', 'io.enq.bits.uop.is_rvc', 'io.enq.bits.uop.is_sfb', 'io.enq.bits.uop.is_sfence', 'io.enq.bits.uop.is_sys_pc2epc', 'io.enq.bits.uop.is_unique', 'io.enq.bits.uop.iw_issued', 'io.enq.bits.uop.iw_issued_partial_agen', 'io.enq.bits.uop.iw_issued_partial_dgen', 'io.enq.bits.uop.iw_p1_bypass_hint', 'io.enq.bits.uop.iw_p1_speculative_child', 'io.enq.bits.uop.iw_p2_bypass_hint', 'io.enq.bits.uop.iw_p2_speculative_child', 'io.enq.bits.uop.iw_p3_bypass_hint', 'io.enq.bits.uop.ldq_idx', 'io.enq.bits.uop.ldst', 'io.enq.bits.uop.ldst_is_rs1', 'io.enq.bits.uop.lrs1', 'io.enq.bits.uop.lrs1_rtype', 'io.enq.bits.uop.lrs2', 'io.enq.bits.uop.lrs2_rtype', 'io.enq.bits.uop.lrs3', 'io.enq.bits.uop.mem_cmd', 'io.enq.bits.uop.mem_signed', 'io.enq.bits.uop.mem_size', 'io.enq.bits.uop.op1_sel', 'io.enq.bits.uop.op2_sel', 'io.enq.bits.uop.pc_lob', 'io.enq.bits.uop.pdst', 'io.enq.bits.uop.pimm', 'io.enq.bits.uop.ppred', 'io.enq.bits.uop.ppred_busy', 'io.enq.bits.uop.prs1', 'io.enq.bits.uop.prs1_busy', 'io.enq.bits.uop.prs2', 'io.enq.bits.uop.prs2_busy', 'io.enq.bits.uop.prs3', 'io.enq.bits.uop.prs3_busy', 'io.enq.bits.uop.rob_idx', 'io.enq.bits.uop.rxq_idx', 'io.enq.bits.uop.stale_pdst', 'io.enq.bits.uop.stq_idx', 'io.enq.bits.uop.taken', 'io.enq.bits.uop.uses_ldq', 'io.enq.bits.uop.uses_stq', 'io.enq.bits.uop.xcpt_ae_if', 'io.enq.bits.uop.xcpt_ma_if', 'io.enq.bits.uop.xcpt_pf_if', 'io.enq.bits.way_en']
  - immediate registers: []
  - historical registers: []

## Parent-local concrete state

['out_reg', 'out_uop', 'out_valid']

## Parent frontier signals

['clock', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.brupdate.b2.cfi_type', 'io.brupdate.b2.jalr_target', 'io.brupdate.b2.mispredict', 'io.brupdate.b2.pc_sel', 'io.brupdate.b2.taken', 'io.brupdate.b2.target_offset', 'io.brupdate.b2.uop.bp_debug_if', 'io.brupdate.b2.uop.bp_xcpt_if', 'io.brupdate.b2.uop.br_mask', 'io.brupdate.b2.uop.br_tag', 'io.brupdate.b2.uop.br_type', 'io.brupdate.b2.uop.csr_cmd', 'io.brupdate.b2.uop.debug_fsrc', 'io.brupdate.b2.uop.debug_inst', 'io.brupdate.b2.uop.debug_pc', 'io.brupdate.b2.uop.debug_tsrc', 'io.brupdate.b2.uop.dis_col_sel', 'io.brupdate.b2.uop.dst_rtype', 'io.brupdate.b2.uop.edge_inst', 'io.brupdate.b2.uop.exc_cause', 'io.brupdate.b2.uop.exception', 'io.brupdate.b2.uop.fcn_dw', 'io.brupdate.b2.uop.fcn_op', 'io.brupdate.b2.uop.flush_on_commit', 'io.brupdate.b2.uop.fp_ctrl.div', 'io.brupdate.b2.uop.fp_ctrl.fastpipe', 'io.brupdate.b2.uop.fp_ctrl.fma', 'io.brupdate.b2.uop.fp_ctrl.fromint', 'io.brupdate.b2.uop.fp_ctrl.ldst', 'io.brupdate.b2.uop.fp_ctrl.ren1', 'io.brupdate.b2.uop.fp_ctrl.ren2', 'io.brupdate.b2.uop.fp_ctrl.ren3', 'io.brupdate.b2.uop.fp_ctrl.sqrt', 'io.brupdate.b2.uop.fp_ctrl.swap12', 'io.brupdate.b2.uop.fp_ctrl.swap23', 'io.brupdate.b2.uop.fp_ctrl.toint', 'io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'io.brupdate.b2.uop.fp_ctrl.vec', 'io.brupdate.b2.uop.fp_ctrl.wen', 'io.brupdate.b2.uop.fp_ctrl.wflags', 'io.brupdate.b2.uop.fp_rm', 'io.brupdate.b2.uop.fp_typ', 'io.brupdate.b2.uop.fp_val', 'io.brupdate.b2.uop.frs3_en', 'io.brupdate.b2.uop.ftq_idx', 'io.brupdate.b2.uop.fu_code[0]', 'io.brupdate.b2.uop.fu_code[1]', 'io.brupdate.b2.uop.fu_code[2]', 'io.brupdate.b2.uop.fu_code[3]', 'io.brupdate.b2.uop.fu_code[4]', 'io.brupdate.b2.uop.fu_code[5]', 'io.brupdate.b2.uop.fu_code[6]', 'io.brupdate.b2.uop.fu_code[7]', 'io.brupdate.b2.uop.fu_code[8]', 'io.brupdate.b2.uop.fu_code[9]', 'io.brupdate.b2.uop.imm_packed', 'io.brupdate.b2.uop.imm_rename', 'io.brupdate.b2.uop.imm_sel', 'io.brupdate.b2.uop.inst', 'io.brupdate.b2.uop.iq_type[0]', 'io.brupdate.b2.uop.iq_type[1]', 'io.brupdate.b2.uop.iq_type[2]', 'io.brupdate.b2.uop.iq_type[3]', 'io.brupdate.b2.uop.is_amo', 'io.brupdate.b2.uop.is_eret', 'io.brupdate.b2.uop.is_fence', 'io.brupdate.b2.uop.is_fencei', 'io.brupdate.b2.uop.is_mov', 'io.brupdate.b2.uop.is_rocc', 'io.brupdate.b2.uop.is_rvc', 'io.brupdate.b2.uop.is_sfb', 'io.brupdate.b2.uop.is_sfence', 'io.brupdate.b2.uop.is_sys_pc2epc', 'io.brupdate.b2.uop.is_unique', 'io.brupdate.b2.uop.iw_issued', 'io.brupdate.b2.uop.iw_issued_partial_agen', 'io.brupdate.b2.uop.iw_issued_partial_dgen', 'io.brupdate.b2.uop.iw_p1_bypass_hint', 'io.brupdate.b2.uop.iw_p1_speculative_child', 'io.brupdate.b2.uop.iw_p2_bypass_hint', 'io.brupdate.b2.uop.iw_p2_speculative_child', 'io.brupdate.b2.uop.iw_p3_bypass_hint', 'io.brupdate.b2.uop.ldq_idx', 'io.brupdate.b2.uop.ldst', 'io.brupdate.b2.uop.ldst_is_rs1', 'io.brupdate.b2.uop.lrs1', 'io.brupdate.b2.uop.lrs1_rtype', 'io.brupdate.b2.uop.lrs2', 'io.brupdate.b2.uop.lrs2_rtype', 'io.brupdate.b2.uop.lrs3', 'io.brupdate.b2.uop.mem_cmd', 'io.brupdate.b2.uop.mem_signed', 'io.brupdate.b2.uop.mem_size', 'io.brupdate.b2.uop.op1_sel', 'io.brupdate.b2.uop.op2_sel', 'io.brupdate.b2.uop.pc_lob', 'io.brupdate.b2.uop.pdst', 'io.brupdate.b2.uop.pimm', 'io.brupdate.b2.uop.ppred', 'io.brupdate.b2.uop.ppred_busy', 'io.brupdate.b2.uop.prs1', 'io.brupdate.b2.uop.prs1_busy', 'io.brupdate.b2.uop.prs2', 'io.brupdate.b2.uop.prs2_busy', 'io.brupdate.b2.uop.prs3', 'io.brupdate.b2.uop.prs3_busy', 'io.brupdate.b2.uop.rob_idx', 'io.brupdate.b2.uop.rxq_idx', 'io.brupdate.b2.uop.stale_pdst', 'io.brupdate.b2.uop.stq_idx', 'io.brupdate.b2.uop.taken', 'io.brupdate.b2.uop.uses_ldq', 'io.brupdate.b2.uop.uses_stq', 'io.brupdate.b2.uop.xcpt_ae_if', 'io.brupdate.b2.uop.xcpt_ma_if', 'io.brupdate.b2.uop.xcpt_pf_if', 'io.count', 'io.deq.bits.addr', 'io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.old_meta.coh.state', 'io.deq.bits.old_meta.tag', 'io.deq.bits.sdq_id', 'io.deq.bits.tag_match', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.bits.way_en', 'io.deq.ready', 'io.deq.valid', 'io.empty', 'io.flush', 'main.clock', 'main.io.brupdate.b1.mispredict_mask', 'main.io.brupdate.b1.resolve_mask', 'main.io.brupdate.b2.cfi_type', 'main.io.brupdate.b2.jalr_target', 'main.io.brupdate.b2.mispredict', 'main.io.brupdate.b2.pc_sel', 'main.io.brupdate.b2.taken', 'main.io.brupdate.b2.target_offset', 'main.io.brupdate.b2.uop.bp_debug_if', 'main.io.brupdate.b2.uop.bp_xcpt_if', 'main.io.brupdate.b2.uop.br_mask', 'main.io.brupdate.b2.uop.br_tag', 'main.io.brupdate.b2.uop.br_type', 'main.io.brupdate.b2.uop.csr_cmd', 'main.io.brupdate.b2.uop.debug_fsrc', 'main.io.brupdate.b2.uop.debug_inst', 'main.io.brupdate.b2.uop.debug_pc', 'main.io.brupdate.b2.uop.debug_tsrc', 'main.io.brupdate.b2.uop.dis_col_sel', 'main.io.brupdate.b2.uop.dst_rtype', 'main.io.brupdate.b2.uop.edge_inst', 'main.io.brupdate.b2.uop.exc_cause', 'main.io.brupdate.b2.uop.exception', 'main.io.brupdate.b2.uop.fcn_dw', 'main.io.brupdate.b2.uop.fcn_op', 'main.io.brupdate.b2.uop.flush_on_commit', 'main.io.brupdate.b2.uop.fp_ctrl.div', 'main.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'main.io.brupdate.b2.uop.fp_ctrl.fma', 'main.io.brupdate.b2.uop.fp_ctrl.fromint', 'main.io.brupdate.b2.uop.fp_ctrl.ldst', 'main.io.brupdate.b2.uop.fp_ctrl.ren1', 'main.io.brupdate.b2.uop.fp_ctrl.ren2', 'main.io.brupdate.b2.uop.fp_ctrl.ren3', 'main.io.brupdate.b2.uop.fp_ctrl.sqrt', 'main.io.brupdate.b2.uop.fp_ctrl.swap12', 'main.io.brupdate.b2.uop.fp_ctrl.swap23', 'main.io.brupdate.b2.uop.fp_ctrl.toint', 'main.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'main.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'main.io.brupdate.b2.uop.fp_ctrl.vec', 'main.io.brupdate.b2.uop.fp_ctrl.wen', 'main.io.brupdate.b2.uop.fp_ctrl.wflags', 'main.io.brupdate.b2.uop.fp_rm', 'main.io.brupdate.b2.uop.fp_typ', 'main.io.brupdate.b2.uop.fp_val', 'main.io.brupdate.b2.uop.frs3_en', 'main.io.brupdate.b2.uop.ftq_idx', 'main.io.brupdate.b2.uop.fu_code[0]', 'main.io.brupdate.b2.uop.fu_code[1]', 'main.io.brupdate.b2.uop.fu_code[2]', 'main.io.brupdate.b2.uop.fu_code[3]', 'main.io.brupdate.b2.uop.fu_code[4]', 'main.io.brupdate.b2.uop.fu_code[5]', 'main.io.brupdate.b2.uop.fu_code[6]', 'main.io.brupdate.b2.uop.fu_code[7]', 'main.io.brupdate.b2.uop.fu_code[8]', 'main.io.brupdate.b2.uop.fu_code[9]', 'main.io.brupdate.b2.uop.imm_packed', 'main.io.brupdate.b2.uop.imm_rename', 'main.io.brupdate.b2.uop.imm_sel', 'main.io.brupdate.b2.uop.inst', 'main.io.brupdate.b2.uop.iq_type[0]', 'main.io.brupdate.b2.uop.iq_type[1]', 'main.io.brupdate.b2.uop.iq_type[2]', 'main.io.brupdate.b2.uop.iq_type[3]', 'main.io.brupdate.b2.uop.is_amo', 'main.io.brupdate.b2.uop.is_eret', 'main.io.brupdate.b2.uop.is_fence', 'main.io.brupdate.b2.uop.is_fencei', 'main.io.brupdate.b2.uop.is_mov', 'main.io.brupdate.b2.uop.is_rocc', 'main.io.brupdate.b2.uop.is_rvc', 'main.io.brupdate.b2.uop.is_sfb', 'main.io.brupdate.b2.uop.is_sfence', 'main.io.brupdate.b2.uop.is_sys_pc2epc', 'main.io.brupdate.b2.uop.is_unique', 'main.io.brupdate.b2.uop.iw_issued', 'main.io.brupdate.b2.uop.iw_issued_partial_agen', 'main.io.brupdate.b2.uop.iw_issued_partial_dgen', 'main.io.brupdate.b2.uop.iw_p1_bypass_hint', 'main.io.brupdate.b2.uop.iw_p1_speculative_child', 'main.io.brupdate.b2.uop.iw_p2_bypass_hint', 'main.io.brupdate.b2.uop.iw_p2_speculative_child', 'main.io.brupdate.b2.uop.iw_p3_bypass_hint', 'main.io.brupdate.b2.uop.ldq_idx', 'main.io.brupdate.b2.uop.ldst', 'main.io.brupdate.b2.uop.ldst_is_rs1', 'main.io.brupdate.b2.uop.lrs1', 'main.io.brupdate.b2.uop.lrs1_rtype', 'main.io.brupdate.b2.uop.lrs2', 'main.io.brupdate.b2.uop.lrs2_rtype', 'main.io.brupdate.b2.uop.lrs3', 'main.io.brupdate.b2.uop.mem_cmd', 'main.io.brupdate.b2.uop.mem_signed', 'main.io.brupdate.b2.uop.mem_size', 'main.io.brupdate.b2.uop.op1_sel', 'main.io.brupdate.b2.uop.op2_sel', 'main.io.brupdate.b2.uop.pc_lob', 'main.io.brupdate.b2.uop.pdst', 'main.io.brupdate.b2.uop.pimm', 'main.io.brupdate.b2.uop.ppred', 'main.io.brupdate.b2.uop.ppred_busy', 'main.io.brupdate.b2.uop.prs1', 'main.io.brupdate.b2.uop.prs1_busy', 'main.io.brupdate.b2.uop.prs2', 'main.io.brupdate.b2.uop.prs2_busy', 'main.io.brupdate.b2.uop.prs3', 'main.io.brupdate.b2.uop.prs3_busy', 'main.io.brupdate.b2.uop.rob_idx', 'main.io.brupdate.b2.uop.rxq_idx', 'main.io.brupdate.b2.uop.stale_pdst', 'main.io.brupdate.b2.uop.stq_idx', 'main.io.brupdate.b2.uop.taken', 'main.io.brupdate.b2.uop.uses_ldq', 'main.io.brupdate.b2.uop.uses_stq', 'main.io.brupdate.b2.uop.xcpt_ae_if', 'main.io.brupdate.b2.uop.xcpt_ma_if', 'main.io.brupdate.b2.uop.xcpt_pf_if', 'main.io.count', 'main.io.deq.bits.uop.br_mask', 'main.io.deq.bits.uop.uses_ldq', 'main.io.deq.ready', 'main.io.deq.valid', 'main.io.empty', 'main.io.enq.bits.addr', 'main.io.enq.bits.data', 'main.io.enq.bits.is_hella', 'main.io.enq.bits.old_meta.coh.state', 'main.io.enq.bits.old_meta.tag', 'main.io.enq.bits.sdq_id', 'main.io.enq.bits.tag_match', 'main.io.enq.bits.uop.bp_debug_if', 'main.io.enq.bits.uop.bp_xcpt_if', 'main.io.enq.bits.uop.br_mask', 'main.io.enq.bits.uop.br_tag', 'main.io.enq.bits.uop.br_type', 'main.io.enq.bits.uop.csr_cmd', 'main.io.enq.bits.uop.debug_fsrc', 'main.io.enq.bits.uop.debug_inst', 'main.io.enq.bits.uop.debug_pc', 'main.io.enq.bits.uop.debug_tsrc', 'main.io.enq.bits.uop.dis_col_sel', 'main.io.enq.bits.uop.dst_rtype', 'main.io.enq.bits.uop.edge_inst', 'main.io.enq.bits.uop.exc_cause', 'main.io.enq.bits.uop.exception', 'main.io.enq.bits.uop.fcn_dw', 'main.io.enq.bits.uop.fcn_op', 'main.io.enq.bits.uop.flush_on_commit', 'main.io.enq.bits.uop.fp_ctrl.div', 'main.io.enq.bits.uop.fp_ctrl.fastpipe', 'main.io.enq.bits.uop.fp_ctrl.fma', 'main.io.enq.bits.uop.fp_ctrl.fromint', 'main.io.enq.bits.uop.fp_ctrl.ldst', 'main.io.enq.bits.uop.fp_ctrl.ren1', 'main.io.enq.bits.uop.fp_ctrl.ren2', 'main.io.enq.bits.uop.fp_ctrl.ren3', 'main.io.enq.bits.uop.fp_ctrl.sqrt', 'main.io.enq.bits.uop.fp_ctrl.swap12', 'main.io.enq.bits.uop.fp_ctrl.swap23', 'main.io.enq.bits.uop.fp_ctrl.toint', 'main.io.enq.bits.uop.fp_ctrl.typeTagIn', 'main.io.enq.bits.uop.fp_ctrl.typeTagOut', 'main.io.enq.bits.uop.fp_ctrl.vec', 'main.io.enq.bits.uop.fp_ctrl.wen', 'main.io.enq.bits.uop.fp_ctrl.wflags', 'main.io.enq.bits.uop.fp_rm', 'main.io.enq.bits.uop.fp_typ', 'main.io.enq.bits.uop.fp_val', 'main.io.enq.bits.uop.frs3_en', 'main.io.enq.bits.uop.ftq_idx', 'main.io.enq.bits.uop.fu_code[0]', 'main.io.enq.bits.uop.fu_code[1]', 'main.io.enq.bits.uop.fu_code[2]', 'main.io.enq.bits.uop.fu_code[3]', 'main.io.enq.bits.uop.fu_code[4]', 'main.io.enq.bits.uop.fu_code[5]', 'main.io.enq.bits.uop.fu_code[6]', 'main.io.enq.bits.uop.fu_code[7]', 'main.io.enq.bits.uop.fu_code[8]', 'main.io.enq.bits.uop.fu_code[9]', 'main.io.enq.bits.uop.imm_packed', 'main.io.enq.bits.uop.imm_rename', 'main.io.enq.bits.uop.imm_sel', 'main.io.enq.bits.uop.inst', 'main.io.enq.bits.uop.iq_type[0]', 'main.io.enq.bits.uop.iq_type[1]', 'main.io.enq.bits.uop.iq_type[2]', 'main.io.enq.bits.uop.iq_type[3]', 'main.io.enq.bits.uop.is_amo', 'main.io.enq.bits.uop.is_eret', 'main.io.enq.bits.uop.is_fence', 'main.io.enq.bits.uop.is_fencei', 'main.io.enq.bits.uop.is_mov', 'main.io.enq.bits.uop.is_rocc', 'main.io.enq.bits.uop.is_rvc', 'main.io.enq.bits.uop.is_sfb', 'main.io.enq.bits.uop.is_sfence', 'main.io.enq.bits.uop.is_sys_pc2epc', 'main.io.enq.bits.uop.is_unique', 'main.io.enq.bits.uop.iw_issued', 'main.io.enq.bits.uop.iw_issued_partial_agen', 'main.io.enq.bits.uop.iw_issued_partial_dgen', 'main.io.enq.bits.uop.iw_p1_bypass_hint', 'main.io.enq.bits.uop.iw_p1_speculative_child', 'main.io.enq.bits.uop.iw_p2_bypass_hint', 'main.io.enq.bits.uop.iw_p2_speculative_child', 'main.io.enq.bits.uop.iw_p3_bypass_hint', 'main.io.enq.bits.uop.ldq_idx', 'main.io.enq.bits.uop.ldst', 'main.io.enq.bits.uop.ldst_is_rs1', 'main.io.enq.bits.uop.lrs1', 'main.io.enq.bits.uop.lrs1_rtype', 'main.io.enq.bits.uop.lrs2', 'main.io.enq.bits.uop.lrs2_rtype', 'main.io.enq.bits.uop.lrs3', 'main.io.enq.bits.uop.mem_cmd', 'main.io.enq.bits.uop.mem_signed', 'main.io.enq.bits.uop.mem_size', 'main.io.enq.bits.uop.op1_sel', 'main.io.enq.bits.uop.op2_sel', 'main.io.enq.bits.uop.pc_lob', 'main.io.enq.bits.uop.pdst', 'main.io.enq.bits.uop.pimm', 'main.io.enq.bits.uop.ppred', 'main.io.enq.bits.uop.ppred_busy', 'main.io.enq.bits.uop.prs1', 'main.io.enq.bits.uop.prs1_busy', 'main.io.enq.bits.uop.prs2', 'main.io.enq.bits.uop.prs2_busy', 'main.io.enq.bits.uop.prs3', 'main.io.enq.bits.uop.prs3_busy', 'main.io.enq.bits.uop.rob_idx', 'main.io.enq.bits.uop.rxq_idx', 'main.io.enq.bits.uop.stale_pdst', 'main.io.enq.bits.uop.stq_idx', 'main.io.enq.bits.uop.taken', 'main.io.enq.bits.uop.uses_ldq', 'main.io.enq.bits.uop.uses_stq', 'main.io.enq.bits.uop.xcpt_ae_if', 'main.io.enq.bits.uop.xcpt_ma_if', 'main.io.enq.bits.uop.xcpt_pf_if', 'main.io.enq.bits.way_en', 'main.io.enq.ready', 'main.io.enq.valid', 'main.io.flush', 'main.reset']

## Frozen child summaries

### Child `BoomMSHR.rpq.main`
- summary ref: `umcm://BoomMSHR.rpq.main`
- frozen task: `leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8`
- frozen SHA-256: `d79c2389d52d6e60f76113d837d619dc94e00e7184c466434d6697cfad97dad8`
- exposed boundary events: ['BoomMSHR.rpq.main::io.deq.fire', 'BoomMSHR.rpq.main::io.enq.fire']
- frontier signals: ['main.clock', 'main.io', 'main.io.brupdate.b1.mispredict_mask', 'main.io.brupdate.b1.resolve_mask', 'main.io.brupdate.b2.cfi_type', 'main.io.brupdate.b2.jalr_target', 'main.io.brupdate.b2.mispredict', 'main.io.brupdate.b2.pc_sel', 'main.io.brupdate.b2.taken', 'main.io.brupdate.b2.target_offset', 'main.io.brupdate.b2.uop.bp_debug_if', 'main.io.brupdate.b2.uop.bp_xcpt_if', 'main.io.brupdate.b2.uop.br_mask', 'main.io.brupdate.b2.uop.br_tag', 'main.io.brupdate.b2.uop.br_type', 'main.io.brupdate.b2.uop.csr_cmd', 'main.io.brupdate.b2.uop.debug_fsrc', 'main.io.brupdate.b2.uop.debug_inst', 'main.io.brupdate.b2.uop.debug_pc', 'main.io.brupdate.b2.uop.debug_tsrc', 'main.io.brupdate.b2.uop.dis_col_sel', 'main.io.brupdate.b2.uop.dst_rtype', 'main.io.brupdate.b2.uop.edge_inst', 'main.io.brupdate.b2.uop.exc_cause', 'main.io.brupdate.b2.uop.exception', 'main.io.brupdate.b2.uop.fcn_dw', 'main.io.brupdate.b2.uop.fcn_op', 'main.io.brupdate.b2.uop.flush_on_commit', 'main.io.brupdate.b2.uop.fp_ctrl.div', 'main.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'main.io.brupdate.b2.uop.fp_ctrl.fma', 'main.io.brupdate.b2.uop.fp_ctrl.fromint', 'main.io.brupdate.b2.uop.fp_ctrl.ldst', 'main.io.brupdate.b2.uop.fp_ctrl.ren1', 'main.io.brupdate.b2.uop.fp_ctrl.ren2', 'main.io.brupdate.b2.uop.fp_ctrl.ren3', 'main.io.brupdate.b2.uop.fp_ctrl.sqrt', 'main.io.brupdate.b2.uop.fp_ctrl.swap12', 'main.io.brupdate.b2.uop.fp_ctrl.swap23', 'main.io.brupdate.b2.uop.fp_ctrl.toint', 'main.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'main.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'main.io.brupdate.b2.uop.fp_ctrl.vec', 'main.io.brupdate.b2.uop.fp_ctrl.wen', 'main.io.brupdate.b2.uop.fp_ctrl.wflags', 'main.io.brupdate.b2.uop.fp_rm', 'main.io.brupdate.b2.uop.fp_typ', 'main.io.brupdate.b2.uop.fp_val', 'main.io.brupdate.b2.uop.frs3_en', 'main.io.brupdate.b2.uop.ftq_idx', 'main.io.brupdate.b2.uop.fu_code[0]', 'main.io.brupdate.b2.uop.fu_code[1]', 'main.io.brupdate.b2.uop.fu_code[2]', 'main.io.brupdate.b2.uop.fu_code[3]', 'main.io.brupdate.b2.uop.fu_code[4]', 'main.io.brupdate.b2.uop.fu_code[5]', 'main.io.brupdate.b2.uop.fu_code[6]', 'main.io.brupdate.b2.uop.fu_code[7]', 'main.io.brupdate.b2.uop.fu_code[8]', 'main.io.brupdate.b2.uop.fu_code[9]', 'main.io.brupdate.b2.uop.imm_packed', 'main.io.brupdate.b2.uop.imm_rename', 'main.io.brupdate.b2.uop.imm_sel', 'main.io.brupdate.b2.uop.inst', 'main.io.brupdate.b2.uop.iq_type[0]', 'main.io.brupdate.b2.uop.iq_type[1]', 'main.io.brupdate.b2.uop.iq_type[2]', 'main.io.brupdate.b2.uop.iq_type[3]', 'main.io.brupdate.b2.uop.is_amo', 'main.io.brupdate.b2.uop.is_eret', 'main.io.brupdate.b2.uop.is_fence', 'main.io.brupdate.b2.uop.is_fencei', 'main.io.brupdate.b2.uop.is_mov', 'main.io.brupdate.b2.uop.is_rocc', 'main.io.brupdate.b2.uop.is_rvc', 'main.io.brupdate.b2.uop.is_sfb', 'main.io.brupdate.b2.uop.is_sfence', 'main.io.brupdate.b2.uop.is_sys_pc2epc', 'main.io.brupdate.b2.uop.is_unique', 'main.io.brupdate.b2.uop.iw_issued', 'main.io.brupdate.b2.uop.iw_issued_partial_agen', 'main.io.brupdate.b2.uop.iw_issued_partial_dgen', 'main.io.brupdate.b2.uop.iw_p1_bypass_hint', 'main.io.brupdate.b2.uop.iw_p1_speculative_child', 'main.io.brupdate.b2.uop.iw_p2_bypass_hint', 'main.io.brupdate.b2.uop.iw_p2_speculative_child', 'main.io.brupdate.b2.uop.iw_p3_bypass_hint', 'main.io.brupdate.b2.uop.ldq_idx', 'main.io.brupdate.b2.uop.ldst', 'main.io.brupdate.b2.uop.ldst_is_rs1', 'main.io.brupdate.b2.uop.lrs1', 'main.io.brupdate.b2.uop.lrs1_rtype', 'main.io.brupdate.b2.uop.lrs2', 'main.io.brupdate.b2.uop.lrs2_rtype', 'main.io.brupdate.b2.uop.lrs3', 'main.io.brupdate.b2.uop.mem_cmd', 'main.io.brupdate.b2.uop.mem_signed', 'main.io.brupdate.b2.uop.mem_size', 'main.io.brupdate.b2.uop.op1_sel', 'main.io.brupdate.b2.uop.op2_sel', 'main.io.brupdate.b2.uop.pc_lob', 'main.io.brupdate.b2.uop.pdst', 'main.io.brupdate.b2.uop.pimm', 'main.io.brupdate.b2.uop.ppred', 'main.io.brupdate.b2.uop.ppred_busy', 'main.io.brupdate.b2.uop.prs1', 'main.io.brupdate.b2.uop.prs1_busy', 'main.io.brupdate.b2.uop.prs2', 'main.io.brupdate.b2.uop.prs2_busy', 'main.io.brupdate.b2.uop.prs3', 'main.io.brupdate.b2.uop.prs3_busy', 'main.io.brupdate.b2.uop.rob_idx', 'main.io.brupdate.b2.uop.rxq_idx', 'main.io.brupdate.b2.uop.stale_pdst', 'main.io.brupdate.b2.uop.stq_idx', 'main.io.brupdate.b2.uop.taken', 'main.io.brupdate.b2.uop.uses_ldq', 'main.io.brupdate.b2.uop.uses_stq', 'main.io.brupdate.b2.uop.xcpt_ae_if', 'main.io.brupdate.b2.uop.xcpt_ma_if', 'main.io.brupdate.b2.uop.xcpt_pf_if', 'main.io.count', 'main.io.deq.bits.addr', 'main.io.deq.bits.data', 'main.io.deq.bits.is_hella', 'main.io.deq.bits.old_meta.coh.state', 'main.io.deq.bits.old_meta.tag', 'main.io.deq.bits.sdq_id', 'main.io.deq.bits.tag_match', 'main.io.deq.bits.uop.bp_debug_if', 'main.io.deq.bits.uop.bp_xcpt_if', 'main.io.deq.bits.uop.br_mask', 'main.io.deq.bits.uop.br_tag', 'main.io.deq.bits.uop.br_type', 'main.io.deq.bits.uop.csr_cmd', 'main.io.deq.bits.uop.debug_fsrc', 'main.io.deq.bits.uop.debug_inst', 'main.io.deq.bits.uop.debug_pc', 'main.io.deq.bits.uop.debug_tsrc', 'main.io.deq.bits.uop.dis_col_sel', 'main.io.deq.bits.uop.dst_rtype', 'main.io.deq.bits.uop.edge_inst', 'main.io.deq.bits.uop.exc_cause', 'main.io.deq.bits.uop.exception', 'main.io.deq.bits.uop.fcn_dw', 'main.io.deq.bits.uop.fcn_op', 'main.io.deq.bits.uop.flush_on_commit', 'main.io.deq.bits.uop.fp_ctrl.div', 'main.io.deq.bits.uop.fp_ctrl.fastpipe', 'main.io.deq.bits.uop.fp_ctrl.fma', 'main.io.deq.bits.uop.fp_ctrl.fromint', 'main.io.deq.bits.uop.fp_ctrl.ldst', 'main.io.deq.bits.uop.fp_ctrl.ren1', 'main.io.deq.bits.uop.fp_ctrl.ren2', 'main.io.deq.bits.uop.fp_ctrl.ren3', 'main.io.deq.bits.uop.fp_ctrl.sqrt', 'main.io.deq.bits.uop.fp_ctrl.swap12', 'main.io.deq.bits.uop.fp_ctrl.swap23', 'main.io.deq.bits.uop.fp_ctrl.toint', 'main.io.deq.bits.uop.fp_ctrl.typeTagIn', 'main.io.deq.bits.uop.fp_ctrl.typeTagOut', 'main.io.deq.bits.uop.fp_ctrl.vec', 'main.io.deq.bits.uop.fp_ctrl.wen', 'main.io.deq.bits.uop.fp_ctrl.wflags', 'main.io.deq.bits.uop.fp_rm', 'main.io.deq.bits.uop.fp_typ', 'main.io.deq.bits.uop.fp_val', 'main.io.deq.bits.uop.frs3_en', 'main.io.deq.bits.uop.ftq_idx', 'main.io.deq.bits.uop.fu_code[0]', 'main.io.deq.bits.uop.fu_code[1]', 'main.io.deq.bits.uop.fu_code[2]', 'main.io.deq.bits.uop.fu_code[3]', 'main.io.deq.bits.uop.fu_code[4]', 'main.io.deq.bits.uop.fu_code[5]', 'main.io.deq.bits.uop.fu_code[6]', 'main.io.deq.bits.uop.fu_code[7]', 'main.io.deq.bits.uop.fu_code[8]', 'main.io.deq.bits.uop.fu_code[9]', 'main.io.deq.bits.uop.imm_packed', 'main.io.deq.bits.uop.imm_rename', 'main.io.deq.bits.uop.imm_sel', 'main.io.deq.bits.uop.inst', 'main.io.deq.bits.uop.iq_type[0]', 'main.io.deq.bits.uop.iq_type[1]', 'main.io.deq.bits.uop.iq_type[2]', 'main.io.deq.bits.uop.iq_type[3]', 'main.io.deq.bits.uop.is_amo', 'main.io.deq.bits.uop.is_eret', 'main.io.deq.bits.uop.is_fence', 'main.io.deq.bits.uop.is_fencei', 'main.io.deq.bits.uop.is_mov', 'main.io.deq.bits.uop.is_rocc', 'main.io.deq.bits.uop.is_rvc', 'main.io.deq.bits.uop.is_sfb', 'main.io.deq.bits.uop.is_sfence', 'main.io.deq.bits.uop.is_sys_pc2epc', 'main.io.deq.bits.uop.is_unique', 'main.io.deq.bits.uop.iw_issued', 'main.io.deq.bits.uop.iw_issued_partial_agen', 'main.io.deq.bits.uop.iw_issued_partial_dgen', 'main.io.deq.bits.uop.iw_p1_bypass_hint', 'main.io.deq.bits.uop.iw_p1_speculative_child', 'main.io.deq.bits.uop.iw_p2_bypass_hint', 'main.io.deq.bits.uop.iw_p2_speculative_child', 'main.io.deq.bits.uop.iw_p3_bypass_hint', 'main.io.deq.bits.uop.ldq_idx', 'main.io.deq.bits.uop.ldst', 'main.io.deq.bits.uop.ldst_is_rs1', 'main.io.deq.bits.uop.lrs1', 'main.io.deq.bits.uop.lrs1_rtype', 'main.io.deq.bits.uop.lrs2', 'main.io.deq.bits.uop.lrs2_rtype', 'main.io.deq.bits.uop.lrs3', 'main.io.deq.bits.uop.mem_cmd', 'main.io.deq.bits.uop.mem_signed', 'main.io.deq.bits.uop.mem_size', 'main.io.deq.bits.uop.op1_sel', 'main.io.deq.bits.uop.op2_sel', 'main.io.deq.bits.uop.pc_lob', 'main.io.deq.bits.uop.pdst', 'main.io.deq.bits.uop.pimm', 'main.io.deq.bits.uop.ppred', 'main.io.deq.bits.uop.ppred_busy', 'main.io.deq.bits.uop.prs1', 'main.io.deq.bits.uop.prs1_busy', 'main.io.deq.bits.uop.prs2', 'main.io.deq.bits.uop.prs2_busy', 'main.io.deq.bits.uop.prs3', 'main.io.deq.bits.uop.prs3_busy', 'main.io.deq.bits.uop.rob_idx', 'main.io.deq.bits.uop.rxq_idx', 'main.io.deq.bits.uop.stale_pdst', 'main.io.deq.bits.uop.stq_idx', 'main.io.deq.bits.uop.taken', 'main.io.deq.bits.uop.uses_ldq', 'main.io.deq.bits.uop.uses_stq', 'main.io.deq.bits.uop.xcpt_ae_if', 'main.io.deq.bits.uop.xcpt_ma_if', 'main.io.deq.bits.uop.xcpt_pf_if', 'main.io.deq.bits.way_en', 'main.io.deq.ready', 'main.io.deq.valid', 'main.io.empty', 'main.io.enq.bits.addr', 'main.io.enq.bits.data', 'main.io.enq.bits.is_hella', 'main.io.enq.bits.old_meta.coh.state', 'main.io.enq.bits.old_meta.tag', 'main.io.enq.bits.sdq_id', 'main.io.enq.bits.tag_match', 'main.io.enq.bits.uop.bp_debug_if', 'main.io.enq.bits.uop.bp_xcpt_if', 'main.io.enq.bits.uop.br_mask', 'main.io.enq.bits.uop.br_tag', 'main.io.enq.bits.uop.br_type', 'main.io.enq.bits.uop.csr_cmd', 'main.io.enq.bits.uop.debug_fsrc', 'main.io.enq.bits.uop.debug_inst', 'main.io.enq.bits.uop.debug_pc', 'main.io.enq.bits.uop.debug_tsrc', 'main.io.enq.bits.uop.dis_col_sel', 'main.io.enq.bits.uop.dst_rtype', 'main.io.enq.bits.uop.edge_inst', 'main.io.enq.bits.uop.exc_cause', 'main.io.enq.bits.uop.exception', 'main.io.enq.bits.uop.fcn_dw', 'main.io.enq.bits.uop.fcn_op', 'main.io.enq.bits.uop.flush_on_commit', 'main.io.enq.bits.uop.fp_ctrl.div', 'main.io.enq.bits.uop.fp_ctrl.fastpipe', 'main.io.enq.bits.uop.fp_ctrl.fma', 'main.io.enq.bits.uop.fp_ctrl.fromint', 'main.io.enq.bits.uop.fp_ctrl.ldst', 'main.io.enq.bits.uop.fp_ctrl.ren1', 'main.io.enq.bits.uop.fp_ctrl.ren2', 'main.io.enq.bits.uop.fp_ctrl.ren3', 'main.io.enq.bits.uop.fp_ctrl.sqrt', 'main.io.enq.bits.uop.fp_ctrl.swap12', 'main.io.enq.bits.uop.fp_ctrl.swap23', 'main.io.enq.bits.uop.fp_ctrl.toint', 'main.io.enq.bits.uop.fp_ctrl.typeTagIn', 'main.io.enq.bits.uop.fp_ctrl.typeTagOut', 'main.io.enq.bits.uop.fp_ctrl.vec', 'main.io.enq.bits.uop.fp_ctrl.wen', 'main.io.enq.bits.uop.fp_ctrl.wflags', 'main.io.enq.bits.uop.fp_rm', 'main.io.enq.bits.uop.fp_typ', 'main.io.enq.bits.uop.fp_val', 'main.io.enq.bits.uop.frs3_en', 'main.io.enq.bits.uop.ftq_idx', 'main.io.enq.bits.uop.fu_code[0]', 'main.io.enq.bits.uop.fu_code[1]', 'main.io.enq.bits.uop.fu_code[2]', 'main.io.enq.bits.uop.fu_code[3]', 'main.io.enq.bits.uop.fu_code[4]', 'main.io.enq.bits.uop.fu_code[5]', 'main.io.enq.bits.uop.fu_code[6]', 'main.io.enq.bits.uop.fu_code[7]', 'main.io.enq.bits.uop.fu_code[8]', 'main.io.enq.bits.uop.fu_code[9]', 'main.io.enq.bits.uop.imm_packed', 'main.io.enq.bits.uop.imm_rename', 'main.io.enq.bits.uop.imm_sel', 'main.io.enq.bits.uop.inst', 'main.io.enq.bits.uop.iq_type[0]', 'main.io.enq.bits.uop.iq_type[1]', 'main.io.enq.bits.uop.iq_type[2]', 'main.io.enq.bits.uop.iq_type[3]', 'main.io.enq.bits.uop.is_amo', 'main.io.enq.bits.uop.is_eret', 'main.io.enq.bits.uop.is_fence', 'main.io.enq.bits.uop.is_fencei', 'main.io.enq.bits.uop.is_mov', 'main.io.enq.bits.uop.is_rocc', 'main.io.enq.bits.uop.is_rvc', 'main.io.enq.bits.uop.is_sfb', 'main.io.enq.bits.uop.is_sfence', 'main.io.enq.bits.uop.is_sys_pc2epc', 'main.io.enq.bits.uop.is_unique', 'main.io.enq.bits.uop.iw_issued', 'main.io.enq.bits.uop.iw_issued_partial_agen', 'main.io.enq.bits.uop.iw_issued_partial_dgen', 'main.io.enq.bits.uop.iw_p1_bypass_hint', 'main.io.enq.bits.uop.iw_p1_speculative_child', 'main.io.enq.bits.uop.iw_p2_bypass_hint', 'main.io.enq.bits.uop.iw_p2_speculative_child', 'main.io.enq.bits.uop.iw_p3_bypass_hint', 'main.io.enq.bits.uop.ldq_idx', 'main.io.enq.bits.uop.ldst', 'main.io.enq.bits.uop.ldst_is_rs1', 'main.io.enq.bits.uop.lrs1', 'main.io.enq.bits.uop.lrs1_rtype', 'main.io.enq.bits.uop.lrs2', 'main.io.enq.bits.uop.lrs2_rtype', 'main.io.enq.bits.uop.lrs3', 'main.io.enq.bits.uop.mem_cmd', 'main.io.enq.bits.uop.mem_signed', 'main.io.enq.bits.uop.mem_size', 'main.io.enq.bits.uop.op1_sel', 'main.io.enq.bits.uop.op2_sel', 'main.io.enq.bits.uop.pc_lob', 'main.io.enq.bits.uop.pdst', 'main.io.enq.bits.uop.pimm', 'main.io.enq.bits.uop.ppred', 'main.io.enq.bits.uop.ppred_busy', 'main.io.enq.bits.uop.prs1', 'main.io.enq.bits.uop.prs1_busy', 'main.io.enq.bits.uop.prs2', 'main.io.enq.bits.uop.prs2_busy', 'main.io.enq.bits.uop.prs3', 'main.io.enq.bits.uop.prs3_busy', 'main.io.enq.bits.uop.rob_idx', 'main.io.enq.bits.uop.rxq_idx', 'main.io.enq.bits.uop.stale_pdst', 'main.io.enq.bits.uop.stq_idx', 'main.io.enq.bits.uop.taken', 'main.io.enq.bits.uop.uses_ldq', 'main.io.enq.bits.uop.uses_stq', 'main.io.enq.bits.uop.xcpt_ae_if', 'main.io.enq.bits.uop.xcpt_ma_if', 'main.io.enq.bits.uop.xcpt_pf_if', 'main.io.enq.bits.way_en', 'main.io.enq.ready', 'main.io.enq.valid', 'main.io.flush', 'main.reset']

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
}
```

Trusted frozen child µMCM:
```json
{
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
}
```

## Parent-local source evidence

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

### generators/boom/src/main/scala/v4/util/util.scala:103-106
```scala
  def apply(brupdate: BrUpdateInfo, uop: MicroOp): MicroOp = {
    val out = WireInit(uop)
    out.br_mask := GetNewBrMask(brupdate, uop)
    out
```

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
```

### generators/boom/src/main/scala/v4/util/util.scala:476-478
```scala
 */
class BranchKillableQueue[T <: boom.v4.common.HasBoomUOP](gen: T, entries: Int, flush_fn: boom.v4.common.MicroOp => Bool = u => true.B, fastDeq: Boolean = false)
  (implicit p: org.chipsalliance.cde.config.Parameters)
```

### generators/boom/src/main/scala/v4/util/util.scala:481-483
```scala
{
  val io = IO(new Bundle {
    val enq     = Flipped(Decoupled(gen))
```

### generators/boom/src/main/scala/v4/util/util.scala:494-519
```scala
    // Pipeline dequeue selection so the mux gets an entire cycle
    val main = Module(new BranchKillableQueue(gen, entries-1, flush_fn, false))
    val out_reg = Reg(gen)
    val out_valid = RegInit(false.B)
    val out_uop = Reg(new MicroOp)

    main.io.enq <> io.enq
    main.io.brupdate := io.brupdate
    main.io.flush := io.flush
    io.empty := main.io.empty && !out_valid
    io.count := main.io.count + out_valid

    io.deq.valid := out_valid
    io.deq.bits := out_reg
    io.deq.bits.uop := out_uop

    out_uop := UpdateBrMask(io.brupdate, out_uop)
    out_valid := out_valid && !IsKilledByBranch(io.brupdate, false.B, out_uop) && !(io.flush && flush_fn(out_uop))

    main.io.deq.ready := false.B
    when (io.deq.fire || !out_valid) {
      out_valid := main.io.deq.valid && !IsKilledByBranch(io.brupdate, false.B, main.io.deq.bits.uop) && !(io.flush && flush_fn(main.io.deq.bits.uop))
      out_reg := main.io.deq.bits
      out_uop := UpdateBrMask(io.brupdate, main.io.deq.bits.uop)
      main.io.deq.ready := true.B
    }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Parent-local FIRRTL statement ledger

Only these parent-local statement IDs may appear in `evidence_statement_ids`.

```text
[0] FIRRTL:188880 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input clock : Clock
[1] FIRRTL:188881 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input reset : Reset
[2] FIRRTL:188882 SRC:generators/boom/src/main/scala/v4/util/util.scala:482:14 KIND:structural :: output io : { flip enq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip flush : UInt<1>, empty : UInt<1>, count : UInt<4>}
[3] FIRRTL:188884 SRC:generators/boom/src/main/scala/v4/util/util.scala:495:22 KIND:structural :: inst main of BranchKillableQueue
[4] FIRRTL:188885 SRC:<no-source-locator> KIND:connect :: connect main.clock, clock
[5] FIRRTL:188886 SRC:<no-source-locator> KIND:connect :: connect main.reset, reset
[6] FIRRTL:188887 SRC:generators/boom/src/main/scala/v4/util/util.scala:496:22 KIND:reg :: reg out_reg : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}, clock
[7] FIRRTL:188888 SRC:generators/boom/src/main/scala/v4/util/util.scala:497:28 KIND:regreset :: regreset out_valid : UInt<1>, clock, reset, UInt<1>(0h0)
[8] FIRRTL:188889 SRC:generators/boom/src/main/scala/v4/util/util.scala:498:22 KIND:reg :: reg out_uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, clock
[9] FIRRTL:188890 SRC:generators/boom/src/main/scala/v4/util/util.scala:500:17 KIND:connect :: connect main.io.enq, io.enq
[10] FIRRTL:188891 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.target_offset, io.brupdate.b2.target_offset
[11] FIRRTL:188892 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.jalr_target, io.brupdate.b2.jalr_target
[12] FIRRTL:188893 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.pc_sel, io.brupdate.b2.pc_sel
[13] FIRRTL:188894 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.cfi_type, io.brupdate.b2.cfi_type
[14] FIRRTL:188895 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.taken, io.brupdate.b2.taken
[15] FIRRTL:188896 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.mispredict, io.brupdate.b2.mispredict
[16] FIRRTL:188897 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.debug_tsrc, io.brupdate.b2.uop.debug_tsrc
[17] FIRRTL:188898 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.debug_fsrc, io.brupdate.b2.uop.debug_fsrc
[18] FIRRTL:188899 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.bp_xcpt_if, io.brupdate.b2.uop.bp_xcpt_if
[19] FIRRTL:188900 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.bp_debug_if, io.brupdate.b2.uop.bp_debug_if
[20] FIRRTL:188901 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.xcpt_ma_if, io.brupdate.b2.uop.xcpt_ma_if
[21] FIRRTL:188902 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.xcpt_ae_if, io.brupdate.b2.uop.xcpt_ae_if
[22] FIRRTL:188903 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.xcpt_pf_if, io.brupdate.b2.uop.xcpt_pf_if
[23] FIRRTL:188904 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_typ, io.brupdate.b2.uop.fp_typ
[24] FIRRTL:188905 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_rm, io.brupdate.b2.uop.fp_rm
[25] FIRRTL:188906 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_val, io.brupdate.b2.uop.fp_val
[26] FIRRTL:188907 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fcn_op, io.brupdate.b2.uop.fcn_op
[27] FIRRTL:188908 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fcn_dw, io.brupdate.b2.uop.fcn_dw
[28] FIRRTL:188909 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.frs3_en, io.brupdate.b2.uop.frs3_en
[29] FIRRTL:188910 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.lrs2_rtype, io.brupdate.b2.uop.lrs2_rtype
[30] FIRRTL:188911 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.lrs1_rtype, io.brupdate.b2.uop.lrs1_rtype
[31] FIRRTL:188912 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.dst_rtype, io.brupdate.b2.uop.dst_rtype
[32] FIRRTL:188913 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.lrs3, io.brupdate.b2.uop.lrs3
[33] FIRRTL:188914 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.lrs2, io.brupdate.b2.uop.lrs2
[34] FIRRTL:188915 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.lrs1, io.brupdate.b2.uop.lrs1
[35] FIRRTL:188916 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ldst, io.brupdate.b2.uop.ldst
[36] FIRRTL:188917 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ldst_is_rs1, io.brupdate.b2.uop.ldst_is_rs1
[37] FIRRTL:188918 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.csr_cmd, io.brupdate.b2.uop.csr_cmd
[38] FIRRTL:188919 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.flush_on_commit, io.brupdate.b2.uop.flush_on_commit
[39] FIRRTL:188920 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_unique, io.brupdate.b2.uop.is_unique
[40] FIRRTL:188921 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.uses_stq, io.brupdate.b2.uop.uses_stq
[41] FIRRTL:188922 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.uses_ldq, io.brupdate.b2.uop.uses_ldq
[42] FIRRTL:188923 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.mem_signed, io.brupdate.b2.uop.mem_signed
[43] FIRRTL:188924 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.mem_size, io.brupdate.b2.uop.mem_size
[44] FIRRTL:188925 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.mem_cmd, io.brupdate.b2.uop.mem_cmd
[45] FIRRTL:188926 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.exc_cause, io.brupdate.b2.uop.exc_cause
[46] FIRRTL:188927 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.exception, io.brupdate.b2.uop.exception
[47] FIRRTL:188928 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.stale_pdst, io.brupdate.b2.uop.stale_pdst
[48] FIRRTL:188929 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ppred_busy, io.brupdate.b2.uop.ppred_busy
[49] FIRRTL:188930 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs3_busy, io.brupdate.b2.uop.prs3_busy
[50] FIRRTL:188931 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs2_busy, io.brupdate.b2.uop.prs2_busy
[51] FIRRTL:188932 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs1_busy, io.brupdate.b2.uop.prs1_busy
[52] FIRRTL:188933 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ppred, io.brupdate.b2.uop.ppred
[53] FIRRTL:188934 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs3, io.brupdate.b2.uop.prs3
[54] FIRRTL:188935 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs2, io.brupdate.b2.uop.prs2
[55] FIRRTL:188936 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.prs1, io.brupdate.b2.uop.prs1
[56] FIRRTL:188937 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.pdst, io.brupdate.b2.uop.pdst
[57] FIRRTL:188938 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.rxq_idx, io.brupdate.b2.uop.rxq_idx
[58] FIRRTL:188939 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.stq_idx, io.brupdate.b2.uop.stq_idx
[59] FIRRTL:188940 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ldq_idx, io.brupdate.b2.uop.ldq_idx
[60] FIRRTL:188941 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.rob_idx, io.brupdate.b2.uop.rob_idx
[61] FIRRTL:188942 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.vec, io.brupdate.b2.uop.fp_ctrl.vec
[62] FIRRTL:188943 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.wflags, io.brupdate.b2.uop.fp_ctrl.wflags
[63] FIRRTL:188944 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.sqrt, io.brupdate.b2.uop.fp_ctrl.sqrt
[64] FIRRTL:188945 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.div, io.brupdate.b2.uop.fp_ctrl.div
[65] FIRRTL:188946 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.fma, io.brupdate.b2.uop.fp_ctrl.fma
[66] FIRRTL:188947 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.brupdate.b2.uop.fp_ctrl.fastpipe
[67] FIRRTL:188948 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.toint, io.brupdate.b2.uop.fp_ctrl.toint
[68] FIRRTL:188949 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.fromint, io.brupdate.b2.uop.fp_ctrl.fromint
[69] FIRRTL:188950 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.brupdate.b2.uop.fp_ctrl.typeTagOut
[70] FIRRTL:188951 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.brupdate.b2.uop.fp_ctrl.typeTagIn
[71] FIRRTL:188952 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.swap23, io.brupdate.b2.uop.fp_ctrl.swap23
[72] FIRRTL:188953 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.swap12, io.brupdate.b2.uop.fp_ctrl.swap12
[73] FIRRTL:188954 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.ren3, io.brupdate.b2.uop.fp_ctrl.ren3
[74] FIRRTL:188955 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.ren2, io.brupdate.b2.uop.fp_ctrl.ren2
[75] FIRRTL:188956 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.ren1, io.brupdate.b2.uop.fp_ctrl.ren1
[76] FIRRTL:188957 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.wen, io.brupdate.b2.uop.fp_ctrl.wen
[77] FIRRTL:188958 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fp_ctrl.ldst, io.brupdate.b2.uop.fp_ctrl.ldst
[78] FIRRTL:188959 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.op2_sel, io.brupdate.b2.uop.op2_sel
[79] FIRRTL:188960 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.op1_sel, io.brupdate.b2.uop.op1_sel
[80] FIRRTL:188961 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.imm_packed, io.brupdate.b2.uop.imm_packed
[81] FIRRTL:188962 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.pimm, io.brupdate.b2.uop.pimm
[82] FIRRTL:188963 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.imm_sel, io.brupdate.b2.uop.imm_sel
[83] FIRRTL:188964 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.imm_rename, io.brupdate.b2.uop.imm_rename
[84] FIRRTL:188965 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.taken, io.brupdate.b2.uop.taken
[85] FIRRTL:188966 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.pc_lob, io.brupdate.b2.uop.pc_lob
[86] FIRRTL:188967 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.edge_inst, io.brupdate.b2.uop.edge_inst
[87] FIRRTL:188968 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.ftq_idx, io.brupdate.b2.uop.ftq_idx
[88] FIRRTL:188969 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_mov, io.brupdate.b2.uop.is_mov
[89] FIRRTL:188970 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_rocc, io.brupdate.b2.uop.is_rocc
[90] FIRRTL:188971 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_sys_pc2epc, io.brupdate.b2.uop.is_sys_pc2epc
[91] FIRRTL:188972 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_eret, io.brupdate.b2.uop.is_eret
[92] FIRRTL:188973 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_amo, io.brupdate.b2.uop.is_amo
[93] FIRRTL:188974 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_sfence, io.brupdate.b2.uop.is_sfence
[94] FIRRTL:188975 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_fencei, io.brupdate.b2.uop.is_fencei
[95] FIRRTL:188976 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_fence, io.brupdate.b2.uop.is_fence
[96] FIRRTL:188977 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_sfb, io.brupdate.b2.uop.is_sfb
[97] FIRRTL:188978 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.br_type, io.brupdate.b2.uop.br_type
[98] FIRRTL:188979 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.br_tag, io.brupdate.b2.uop.br_tag
[99] FIRRTL:188980 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.br_mask, io.brupdate.b2.uop.br_mask
[100] FIRRTL:188981 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.dis_col_sel, io.brupdate.b2.uop.dis_col_sel
[101] FIRRTL:188982 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_p3_bypass_hint, io.brupdate.b2.uop.iw_p3_bypass_hint
[102] FIRRTL:188983 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_p2_bypass_hint, io.brupdate.b2.uop.iw_p2_bypass_hint
[103] FIRRTL:188984 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_p1_bypass_hint, io.brupdate.b2.uop.iw_p1_bypass_hint
[104] FIRRTL:188985 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_p2_speculative_child, io.brupdate.b2.uop.iw_p2_speculative_child
[105] FIRRTL:188986 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_p1_speculative_child, io.brupdate.b2.uop.iw_p1_speculative_child
[106] FIRRTL:188987 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_issued_partial_dgen, io.brupdate.b2.uop.iw_issued_partial_dgen
[107] FIRRTL:188988 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_issued_partial_agen, io.brupdate.b2.uop.iw_issued_partial_agen
[108] FIRRTL:188989 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iw_issued, io.brupdate.b2.uop.iw_issued
[109] FIRRTL:188990 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[0], io.brupdate.b2.uop.fu_code[0]
[110] FIRRTL:188991 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[1], io.brupdate.b2.uop.fu_code[1]
[111] FIRRTL:188992 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[2], io.brupdate.b2.uop.fu_code[2]
[112] FIRRTL:188993 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[3], io.brupdate.b2.uop.fu_code[3]
[113] FIRRTL:188994 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[4], io.brupdate.b2.uop.fu_code[4]
[114] FIRRTL:188995 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[5], io.brupdate.b2.uop.fu_code[5]
[115] FIRRTL:188996 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[6], io.brupdate.b2.uop.fu_code[6]
[116] FIRRTL:188997 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[7], io.brupdate.b2.uop.fu_code[7]
[117] FIRRTL:188998 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[8], io.brupdate.b2.uop.fu_code[8]
[118] FIRRTL:188999 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.fu_code[9], io.brupdate.b2.uop.fu_code[9]
[119] FIRRTL:189000 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iq_type[0], io.brupdate.b2.uop.iq_type[0]
[120] FIRRTL:189001 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iq_type[1], io.brupdate.b2.uop.iq_type[1]
[121] FIRRTL:189002 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iq_type[2], io.brupdate.b2.uop.iq_type[2]
[122] FIRRTL:189003 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.iq_type[3], io.brupdate.b2.uop.iq_type[3]
[123] FIRRTL:189004 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.debug_pc, io.brupdate.b2.uop.debug_pc
[124] FIRRTL:189005 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.is_rvc, io.brupdate.b2.uop.is_rvc
[125] FIRRTL:189006 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.debug_inst, io.brupdate.b2.uop.debug_inst
[126] FIRRTL:189007 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b2.uop.inst, io.brupdate.b2.uop.inst
[127] FIRRTL:189008 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b1.mispredict_mask, io.brupdate.b1.mispredict_mask
[128] FIRRTL:189009 SRC:generators/boom/src/main/scala/v4/util/util.scala:501:22 KIND:connect :: connect main.io.brupdate.b1.resolve_mask, io.brupdate.b1.resolve_mask
[129] FIRRTL:189010 SRC:generators/boom/src/main/scala/v4/util/util.scala:502:19 KIND:connect :: connect main.io.flush, io.flush
[130] FIRRTL:189011 SRC:generators/boom/src/main/scala/v4/util/util.scala:503:34 KIND:node :: node _io_empty_T = eq(out_valid, UInt<1>(0h0))
[131] FIRRTL:189012 SRC:generators/boom/src/main/scala/v4/util/util.scala:503:31 KIND:node :: node _io_empty_T_1 = and(main.io.empty, _io_empty_T)
[132] FIRRTL:189013 SRC:generators/boom/src/main/scala/v4/util/util.scala:503:14 KIND:connect :: connect io.empty, _io_empty_T_1
[133] FIRRTL:189014 SRC:generators/boom/src/main/scala/v4/util/util.scala:504:31 KIND:node :: node _io_count_T = add(main.io.count, out_valid)
[134] FIRRTL:189015 SRC:generators/boom/src/main/scala/v4/util/util.scala:504:31 KIND:node :: node _io_count_T_1 = tail(_io_count_T, 1)
[135] FIRRTL:189016 SRC:generators/boom/src/main/scala/v4/util/util.scala:504:14 KIND:connect :: connect io.count, _io_count_T_1
[136] FIRRTL:189017 SRC:generators/boom/src/main/scala/v4/util/util.scala:506:18 KIND:connect :: connect io.deq.valid, out_valid
[137] FIRRTL:189018 SRC:generators/boom/src/main/scala/v4/util/util.scala:507:17 KIND:connect :: connect io.deq.bits, out_reg
[138] FIRRTL:189019 SRC:generators/boom/src/main/scala/v4/util/util.scala:508:21 KIND:connect :: connect io.deq.bits.uop, out_uop
[139] FIRRTL:189020 SRC:generators/boom/src/main/scala/v4/util/util.scala:104:23 KIND:wire :: wire out_uop_out : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}
[140] FIRRTL:189021 SRC:generators/boom/src/main/scala/v4/util/util.scala:104:23 KIND:connect :: connect out_uop_out, out_uop
[141] FIRRTL:189022 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _out_uop_out_br_mask_T = not(io.brupdate.b1.resolve_mask)
[142] FIRRTL:189023 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _out_uop_out_br_mask_T_1 = and(out_uop.br_mask, _out_uop_out_br_mask_T)
[143] FIRRTL:189024 SRC:generators/boom/src/main/scala/v4/util/util.scala:105:17 KIND:connect :: connect out_uop_out.br_mask, _out_uop_out_br_mask_T_1
[144] FIRRTL:189025 SRC:generators/boom/src/main/scala/v4/util/util.scala:510:13 KIND:connect :: connect out_uop, out_uop_out
[145] FIRRTL:189026 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _out_valid_T = and(io.brupdate.b1.mispredict_mask, out_uop.br_mask)
[146] FIRRTL:189027 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _out_valid_T_1 = neq(_out_valid_T, UInt<1>(0h0))
[147] FIRRTL:189028 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _out_valid_T_2 = or(_out_valid_T_1, UInt<1>(0h0))
[148] FIRRTL:189029 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:31 KIND:node :: node _out_valid_T_3 = eq(_out_valid_T_2, UInt<1>(0h0))
[149] FIRRTL:189030 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:28 KIND:node :: node _out_valid_T_4 = and(out_valid, _out_valid_T_3)
[150] FIRRTL:189031 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:94 KIND:node :: node _out_valid_T_5 = and(io.flush, out_uop.uses_ldq)
[151] FIRRTL:189032 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:83 KIND:node :: node _out_valid_T_6 = eq(_out_valid_T_5, UInt<1>(0h0))
[152] FIRRTL:189033 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:80 KIND:node :: node _out_valid_T_7 = and(_out_valid_T_4, _out_valid_T_6)
[153] FIRRTL:189034 SRC:generators/boom/src/main/scala/v4/util/util.scala:511:15 KIND:connect :: connect out_valid, _out_valid_T_7
[154] FIRRTL:189035 SRC:generators/boom/src/main/scala/v4/util/util.scala:513:23 KIND:connect :: connect main.io.deq.ready, UInt<1>(0h0)
[155] FIRRTL:189036 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T = and(io.deq.ready, io.deq.valid)
[156] FIRRTL:189037 SRC:generators/boom/src/main/scala/v4/util/util.scala:514:26 KIND:node :: node _T_1 = eq(out_valid, UInt<1>(0h0))
[157] FIRRTL:189038 SRC:generators/boom/src/main/scala/v4/util/util.scala:514:23 KIND:node :: node _T_2 = or(_T, _T_1)
[158] FIRRTL:189039 SRC:generators/boom/src/main/scala/v4/util/util.scala:514:38 KIND:when :: when _T_2 :
[159] FIRRTL:189040 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _out_valid_T_8 = and(io.brupdate.b1.mispredict_mask, main.io.deq.bits.uop.br_mask)
[160] FIRRTL:189041 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _out_valid_T_9 = neq(_out_valid_T_8, UInt<1>(0h0))
[161] FIRRTL:189042 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _out_valid_T_10 = or(_out_valid_T_9, UInt<1>(0h0))
[162] FIRRTL:189043 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:41 KIND:node :: node _out_valid_T_11 = eq(_out_valid_T_10, UInt<1>(0h0))
[163] FIRRTL:189044 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:38 KIND:node :: node _out_valid_T_12 = and(main.io.deq.valid, _out_valid_T_11)
[164] FIRRTL:189045 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:117 KIND:node :: node _out_valid_T_13 = and(io.flush, main.io.deq.bits.uop.uses_ldq)
[165] FIRRTL:189046 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:106 KIND:node :: node _out_valid_T_14 = eq(_out_valid_T_13, UInt<1>(0h0))
[166] FIRRTL:189047 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:103 KIND:node :: node _out_valid_T_15 = and(_out_valid_T_12, _out_valid_T_14)
[167] FIRRTL:189048 SRC:generators/boom/src/main/scala/v4/util/util.scala:515:17 KIND:connect :: connect out_valid, _out_valid_T_15
[168] FIRRTL:189049 SRC:generators/boom/src/main/scala/v4/util/util.scala:516:15 KIND:connect :: connect out_reg, main.io.deq.bits
[169] FIRRTL:189050 SRC:generators/boom/src/main/scala/v4/util/util.scala:104:23 KIND:wire :: wire out_uop_out_1 : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}
[170] FIRRTL:189051 SRC:generators/boom/src/main/scala/v4/util/util.scala:104:23 KIND:connect :: connect out_uop_out_1, main.io.deq.bits.uop
[171] FIRRTL:189052 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _out_uop_out_br_mask_T_2 = not(io.brupdate.b1.resolve_mask)
[172] FIRRTL:189053 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _out_uop_out_br_mask_T_3 = and(main.io.deq.bits.uop.br_mask, _out_uop_out_br_mask_T_2)
[173] FIRRTL:189054 SRC:generators/boom/src/main/scala/v4/util/util.scala:105:17 KIND:connect :: connect out_uop_out_1.br_mask, _out_uop_out_br_mask_T_3
[174] FIRRTL:189055 SRC:generators/boom/src/main/scala/v4/util/util.scala:517:15 KIND:connect :: connect out_uop, out_uop_out_1
[175] FIRRTL:189056 SRC:generators/boom/src/main/scala/v4/util/util.scala:518:25 KIND:connect :: connect main.io.deq.ready, UInt<1>(0h1)
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
  "task_id": "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc",
  "work_unit_id": "BoomMSHR.rpq",
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
