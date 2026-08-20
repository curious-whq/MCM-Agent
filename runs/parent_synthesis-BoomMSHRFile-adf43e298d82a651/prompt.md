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

Task ID: `parent_synthesis-BoomMSHRFile-adf43e298d82a651`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `parent-synthesis-prompt-0.2`
Output schema version: `umcm-formal-0.5`

## Parent WorkUnit

- id: `BoomMSHRFile`
- module: `BoomMSHRFile`
- kind: `module`
- instance path: `BoomMSHRFile`
- leaf: `False`
- coverage complete: `True`
- parent-local raw statements after child replacement: 1507
- parent-local logical statements after child replacement: 234
- parent-local registers: 12
- parent-local physical boundary events: 13

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

- `BoomMSHRFile::io.mem_acquire.fire`
  - predicate: `io.mem_acquire.valid && io.mem_acquire.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.mem_acquire.bits.address', 'io.mem_acquire.bits.corrupt', 'io.mem_acquire.bits.data', 'io.mem_acquire.bits.mask', 'io.mem_acquire.bits.opcode', 'io.mem_acquire.bits.param', 'io.mem_acquire.bits.size', 'io.mem_acquire.bits.source']
  - immediate registers: ['beatsLeft', 'state']
  - historical registers: ['beatsLeft', 'state']
- `BoomMSHRFile::io.mem_finish.fire`
  - predicate: `io.mem_finish.valid && io.mem_finish.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.mem_finish.bits.sink']
  - immediate registers: ['beatsLeft_1', 'state_1']
  - historical registers: ['beatsLeft_1', 'state_1']
- `BoomMSHRFile::io.mem_grant.fire`
  - predicate: `io.mem_grant.valid && io.mem_grant.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.mem_grant.bits.corrupt', 'io.mem_grant.bits.data', 'io.mem_grant.bits.denied', 'io.mem_grant.bits.opcode', 'io.mem_grant.bits.param', 'io.mem_grant.bits.sink', 'io.mem_grant.bits.size', 'io.mem_grant.bits.source']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.meta_read.fire`
  - predicate: `io.meta_read.valid && io.meta_read.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.meta_resp.valid`
  - predicate: `io.meta_resp.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.meta_resp.bits.coh.state', 'io.meta_resp.bits.tag']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.meta_write.fire`
  - predicate: `io.meta_write.valid && io.meta_write.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.prefetch.fire`
  - predicate: `io.prefetch.valid && io.prefetch.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.prefetch.bits.addr', 'io.prefetch.bits.data', 'io.prefetch.bits.is_hella', 'io.prefetch.bits.uop.bp_debug_if', 'io.prefetch.bits.uop.bp_xcpt_if', 'io.prefetch.bits.uop.br_mask', 'io.prefetch.bits.uop.br_tag', 'io.prefetch.bits.uop.br_type', 'io.prefetch.bits.uop.csr_cmd', 'io.prefetch.bits.uop.debug_fsrc', 'io.prefetch.bits.uop.debug_inst', 'io.prefetch.bits.uop.debug_pc', 'io.prefetch.bits.uop.debug_tsrc', 'io.prefetch.bits.uop.dis_col_sel', 'io.prefetch.bits.uop.dst_rtype', 'io.prefetch.bits.uop.edge_inst', 'io.prefetch.bits.uop.exc_cause', 'io.prefetch.bits.uop.exception', 'io.prefetch.bits.uop.fcn_dw', 'io.prefetch.bits.uop.fcn_op', 'io.prefetch.bits.uop.flush_on_commit', 'io.prefetch.bits.uop.fp_ctrl.div', 'io.prefetch.bits.uop.fp_ctrl.fastpipe', 'io.prefetch.bits.uop.fp_ctrl.fma', 'io.prefetch.bits.uop.fp_ctrl.fromint', 'io.prefetch.bits.uop.fp_ctrl.ldst', 'io.prefetch.bits.uop.fp_ctrl.ren1', 'io.prefetch.bits.uop.fp_ctrl.ren2', 'io.prefetch.bits.uop.fp_ctrl.ren3', 'io.prefetch.bits.uop.fp_ctrl.sqrt', 'io.prefetch.bits.uop.fp_ctrl.swap12', 'io.prefetch.bits.uop.fp_ctrl.swap23', 'io.prefetch.bits.uop.fp_ctrl.toint', 'io.prefetch.bits.uop.fp_ctrl.typeTagIn', 'io.prefetch.bits.uop.fp_ctrl.typeTagOut', 'io.prefetch.bits.uop.fp_ctrl.vec', 'io.prefetch.bits.uop.fp_ctrl.wen', 'io.prefetch.bits.uop.fp_ctrl.wflags', 'io.prefetch.bits.uop.fp_rm', 'io.prefetch.bits.uop.fp_typ', 'io.prefetch.bits.uop.fp_val', 'io.prefetch.bits.uop.frs3_en', 'io.prefetch.bits.uop.ftq_idx', 'io.prefetch.bits.uop.fu_code[0]', 'io.prefetch.bits.uop.fu_code[1]', 'io.prefetch.bits.uop.fu_code[2]', 'io.prefetch.bits.uop.fu_code[3]', 'io.prefetch.bits.uop.fu_code[4]', 'io.prefetch.bits.uop.fu_code[5]', 'io.prefetch.bits.uop.fu_code[6]', 'io.prefetch.bits.uop.fu_code[7]', 'io.prefetch.bits.uop.fu_code[8]', 'io.prefetch.bits.uop.fu_code[9]', 'io.prefetch.bits.uop.imm_packed', 'io.prefetch.bits.uop.imm_rename', 'io.prefetch.bits.uop.imm_sel', 'io.prefetch.bits.uop.inst', 'io.prefetch.bits.uop.iq_type[0]', 'io.prefetch.bits.uop.iq_type[1]', 'io.prefetch.bits.uop.iq_type[2]', 'io.prefetch.bits.uop.iq_type[3]', 'io.prefetch.bits.uop.is_amo', 'io.prefetch.bits.uop.is_eret', 'io.prefetch.bits.uop.is_fence', 'io.prefetch.bits.uop.is_fencei', 'io.prefetch.bits.uop.is_mov', 'io.prefetch.bits.uop.is_rocc', 'io.prefetch.bits.uop.is_rvc', 'io.prefetch.bits.uop.is_sfb', 'io.prefetch.bits.uop.is_sfence', 'io.prefetch.bits.uop.is_sys_pc2epc', 'io.prefetch.bits.uop.is_unique', 'io.prefetch.bits.uop.iw_issued', 'io.prefetch.bits.uop.iw_issued_partial_agen', 'io.prefetch.bits.uop.iw_issued_partial_dgen', 'io.prefetch.bits.uop.iw_p1_bypass_hint', 'io.prefetch.bits.uop.iw_p1_speculative_child', 'io.prefetch.bits.uop.iw_p2_bypass_hint', 'io.prefetch.bits.uop.iw_p2_speculative_child', 'io.prefetch.bits.uop.iw_p3_bypass_hint', 'io.prefetch.bits.uop.ldq_idx', 'io.prefetch.bits.uop.ldst', 'io.prefetch.bits.uop.ldst_is_rs1', 'io.prefetch.bits.uop.lrs1', 'io.prefetch.bits.uop.lrs1_rtype', 'io.prefetch.bits.uop.lrs2', 'io.prefetch.bits.uop.lrs2_rtype', 'io.prefetch.bits.uop.lrs3', 'io.prefetch.bits.uop.mem_cmd', 'io.prefetch.bits.uop.mem_signed', 'io.prefetch.bits.uop.mem_size', 'io.prefetch.bits.uop.op1_sel', 'io.prefetch.bits.uop.op2_sel', 'io.prefetch.bits.uop.pc_lob', 'io.prefetch.bits.uop.pdst', 'io.prefetch.bits.uop.pimm', 'io.prefetch.bits.uop.ppred', 'io.prefetch.bits.uop.ppred_busy', 'io.prefetch.bits.uop.prs1', 'io.prefetch.bits.uop.prs1_busy', 'io.prefetch.bits.uop.prs2', 'io.prefetch.bits.uop.prs2_busy', 'io.prefetch.bits.uop.prs3', 'io.prefetch.bits.uop.prs3_busy', 'io.prefetch.bits.uop.rob_idx', 'io.prefetch.bits.uop.rxq_idx', 'io.prefetch.bits.uop.stale_pdst', 'io.prefetch.bits.uop.stq_idx', 'io.prefetch.bits.uop.taken', 'io.prefetch.bits.uop.uses_ldq', 'io.prefetch.bits.uop.uses_stq', 'io.prefetch.bits.uop.xcpt_ae_if', 'io.prefetch.bits.uop.xcpt_ma_if', 'io.prefetch.bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.prober_state.valid`
  - predicate: `io.prober_state.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.prober_state.bits']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.refill.fire`
  - predicate: `io.refill.valid && io.refill.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.refill.bits.addr', 'io.refill.bits.data', 'io.refill.bits.way_en', 'io.refill.bits.wmask']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.replay.fire`
  - predicate: `io.replay.valid && io.replay.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.replay.bits.addr', 'io.replay.bits.data', 'io.replay.bits.is_hella', 'io.replay.bits.old_meta.coh.state', 'io.replay.bits.old_meta.tag', 'io.replay.bits.sdq_id', 'io.replay.bits.tag_match', 'io.replay.bits.uop.bp_debug_if', 'io.replay.bits.uop.bp_xcpt_if', 'io.replay.bits.uop.br_mask', 'io.replay.bits.uop.br_tag', 'io.replay.bits.uop.br_type', 'io.replay.bits.uop.csr_cmd', 'io.replay.bits.uop.debug_fsrc', 'io.replay.bits.uop.debug_inst', 'io.replay.bits.uop.debug_pc', 'io.replay.bits.uop.debug_tsrc', 'io.replay.bits.uop.dis_col_sel', 'io.replay.bits.uop.dst_rtype', 'io.replay.bits.uop.edge_inst', 'io.replay.bits.uop.exc_cause', 'io.replay.bits.uop.exception', 'io.replay.bits.uop.fcn_dw', 'io.replay.bits.uop.fcn_op', 'io.replay.bits.uop.flush_on_commit', 'io.replay.bits.uop.fp_ctrl.div', 'io.replay.bits.uop.fp_ctrl.fastpipe', 'io.replay.bits.uop.fp_ctrl.fma', 'io.replay.bits.uop.fp_ctrl.fromint', 'io.replay.bits.uop.fp_ctrl.ldst', 'io.replay.bits.uop.fp_ctrl.ren1', 'io.replay.bits.uop.fp_ctrl.ren2', 'io.replay.bits.uop.fp_ctrl.ren3', 'io.replay.bits.uop.fp_ctrl.sqrt', 'io.replay.bits.uop.fp_ctrl.swap12', 'io.replay.bits.uop.fp_ctrl.swap23', 'io.replay.bits.uop.fp_ctrl.toint', 'io.replay.bits.uop.fp_ctrl.typeTagIn', 'io.replay.bits.uop.fp_ctrl.typeTagOut', 'io.replay.bits.uop.fp_ctrl.vec', 'io.replay.bits.uop.fp_ctrl.wen', 'io.replay.bits.uop.fp_ctrl.wflags', 'io.replay.bits.uop.fp_rm', 'io.replay.bits.uop.fp_typ', 'io.replay.bits.uop.fp_val', 'io.replay.bits.uop.frs3_en', 'io.replay.bits.uop.ftq_idx', 'io.replay.bits.uop.fu_code[0]', 'io.replay.bits.uop.fu_code[1]', 'io.replay.bits.uop.fu_code[2]', 'io.replay.bits.uop.fu_code[3]', 'io.replay.bits.uop.fu_code[4]', 'io.replay.bits.uop.fu_code[5]', 'io.replay.bits.uop.fu_code[6]', 'io.replay.bits.uop.fu_code[7]', 'io.replay.bits.uop.fu_code[8]', 'io.replay.bits.uop.fu_code[9]', 'io.replay.bits.uop.imm_packed', 'io.replay.bits.uop.imm_rename', 'io.replay.bits.uop.imm_sel', 'io.replay.bits.uop.inst', 'io.replay.bits.uop.iq_type[0]', 'io.replay.bits.uop.iq_type[1]', 'io.replay.bits.uop.iq_type[2]', 'io.replay.bits.uop.iq_type[3]', 'io.replay.bits.uop.is_amo', 'io.replay.bits.uop.is_eret', 'io.replay.bits.uop.is_fence', 'io.replay.bits.uop.is_fencei', 'io.replay.bits.uop.is_mov', 'io.replay.bits.uop.is_rocc', 'io.replay.bits.uop.is_rvc', 'io.replay.bits.uop.is_sfb', 'io.replay.bits.uop.is_sfence', 'io.replay.bits.uop.is_sys_pc2epc', 'io.replay.bits.uop.is_unique', 'io.replay.bits.uop.iw_issued', 'io.replay.bits.uop.iw_issued_partial_agen', 'io.replay.bits.uop.iw_issued_partial_dgen', 'io.replay.bits.uop.iw_p1_bypass_hint', 'io.replay.bits.uop.iw_p1_speculative_child', 'io.replay.bits.uop.iw_p2_bypass_hint', 'io.replay.bits.uop.iw_p2_speculative_child', 'io.replay.bits.uop.iw_p3_bypass_hint', 'io.replay.bits.uop.ldq_idx', 'io.replay.bits.uop.ldst', 'io.replay.bits.uop.ldst_is_rs1', 'io.replay.bits.uop.lrs1', 'io.replay.bits.uop.lrs1_rtype', 'io.replay.bits.uop.lrs2', 'io.replay.bits.uop.lrs2_rtype', 'io.replay.bits.uop.lrs3', 'io.replay.bits.uop.mem_cmd', 'io.replay.bits.uop.mem_signed', 'io.replay.bits.uop.mem_size', 'io.replay.bits.uop.op1_sel', 'io.replay.bits.uop.op2_sel', 'io.replay.bits.uop.pc_lob', 'io.replay.bits.uop.pdst', 'io.replay.bits.uop.pimm', 'io.replay.bits.uop.ppred', 'io.replay.bits.uop.ppred_busy', 'io.replay.bits.uop.prs1', 'io.replay.bits.uop.prs1_busy', 'io.replay.bits.uop.prs2', 'io.replay.bits.uop.prs2_busy', 'io.replay.bits.uop.prs3', 'io.replay.bits.uop.prs3_busy', 'io.replay.bits.uop.rob_idx', 'io.replay.bits.uop.rxq_idx', 'io.replay.bits.uop.stale_pdst', 'io.replay.bits.uop.stq_idx', 'io.replay.bits.uop.taken', 'io.replay.bits.uop.uses_ldq', 'io.replay.bits.uop.uses_stq', 'io.replay.bits.uop.xcpt_ae_if', 'io.replay.bits.uop.xcpt_ma_if', 'io.replay.bits.uop.xcpt_pf_if', 'io.replay.bits.way_en']
  - immediate registers: []
  - historical registers: ['mshr_alloc_idx_REG', 'mshr_head', 'sdq_val']
- `BoomMSHRFile::io.req[0].fire`
  - predicate: `io.req[0].valid && io.req[0].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.req[0].bits.addr', 'io.req[0].bits.data', 'io.req[0].bits.is_hella', 'io.req[0].bits.old_meta.coh.state', 'io.req[0].bits.old_meta.tag', 'io.req[0].bits.sdq_id', 'io.req[0].bits.tag_match', 'io.req[0].bits.uop.bp_debug_if', 'io.req[0].bits.uop.bp_xcpt_if', 'io.req[0].bits.uop.br_mask', 'io.req[0].bits.uop.br_tag', 'io.req[0].bits.uop.br_type', 'io.req[0].bits.uop.csr_cmd', 'io.req[0].bits.uop.debug_fsrc', 'io.req[0].bits.uop.debug_inst', 'io.req[0].bits.uop.debug_pc', 'io.req[0].bits.uop.debug_tsrc', 'io.req[0].bits.uop.dis_col_sel', 'io.req[0].bits.uop.dst_rtype', 'io.req[0].bits.uop.edge_inst', 'io.req[0].bits.uop.exc_cause', 'io.req[0].bits.uop.exception', 'io.req[0].bits.uop.fcn_dw', 'io.req[0].bits.uop.fcn_op', 'io.req[0].bits.uop.flush_on_commit', 'io.req[0].bits.uop.fp_ctrl.div', 'io.req[0].bits.uop.fp_ctrl.fastpipe', 'io.req[0].bits.uop.fp_ctrl.fma', 'io.req[0].bits.uop.fp_ctrl.fromint', 'io.req[0].bits.uop.fp_ctrl.ldst', 'io.req[0].bits.uop.fp_ctrl.ren1', 'io.req[0].bits.uop.fp_ctrl.ren2', 'io.req[0].bits.uop.fp_ctrl.ren3', 'io.req[0].bits.uop.fp_ctrl.sqrt', 'io.req[0].bits.uop.fp_ctrl.swap12', 'io.req[0].bits.uop.fp_ctrl.swap23', 'io.req[0].bits.uop.fp_ctrl.toint', 'io.req[0].bits.uop.fp_ctrl.typeTagIn', 'io.req[0].bits.uop.fp_ctrl.typeTagOut', 'io.req[0].bits.uop.fp_ctrl.vec', 'io.req[0].bits.uop.fp_ctrl.wen', 'io.req[0].bits.uop.fp_ctrl.wflags', 'io.req[0].bits.uop.fp_rm', 'io.req[0].bits.uop.fp_typ', 'io.req[0].bits.uop.fp_val', 'io.req[0].bits.uop.frs3_en', 'io.req[0].bits.uop.ftq_idx', 'io.req[0].bits.uop.fu_code[0]', 'io.req[0].bits.uop.fu_code[1]', 'io.req[0].bits.uop.fu_code[2]', 'io.req[0].bits.uop.fu_code[3]', 'io.req[0].bits.uop.fu_code[4]', 'io.req[0].bits.uop.fu_code[5]', 'io.req[0].bits.uop.fu_code[6]', 'io.req[0].bits.uop.fu_code[7]', 'io.req[0].bits.uop.fu_code[8]', 'io.req[0].bits.uop.fu_code[9]', 'io.req[0].bits.uop.imm_packed', 'io.req[0].bits.uop.imm_rename', 'io.req[0].bits.uop.imm_sel', 'io.req[0].bits.uop.inst', 'io.req[0].bits.uop.iq_type[0]', 'io.req[0].bits.uop.iq_type[1]', 'io.req[0].bits.uop.iq_type[2]', 'io.req[0].bits.uop.iq_type[3]', 'io.req[0].bits.uop.is_amo', 'io.req[0].bits.uop.is_eret', 'io.req[0].bits.uop.is_fence', 'io.req[0].bits.uop.is_fencei', 'io.req[0].bits.uop.is_mov', 'io.req[0].bits.uop.is_rocc', 'io.req[0].bits.uop.is_rvc', 'io.req[0].bits.uop.is_sfb', 'io.req[0].bits.uop.is_sfence', 'io.req[0].bits.uop.is_sys_pc2epc', 'io.req[0].bits.uop.is_unique', 'io.req[0].bits.uop.iw_issued', 'io.req[0].bits.uop.iw_issued_partial_agen', 'io.req[0].bits.uop.iw_issued_partial_dgen', 'io.req[0].bits.uop.iw_p1_bypass_hint', 'io.req[0].bits.uop.iw_p1_speculative_child', 'io.req[0].bits.uop.iw_p2_bypass_hint', 'io.req[0].bits.uop.iw_p2_speculative_child', 'io.req[0].bits.uop.iw_p3_bypass_hint', 'io.req[0].bits.uop.ldq_idx', 'io.req[0].bits.uop.ldst', 'io.req[0].bits.uop.ldst_is_rs1', 'io.req[0].bits.uop.lrs1', 'io.req[0].bits.uop.lrs1_rtype', 'io.req[0].bits.uop.lrs2', 'io.req[0].bits.uop.lrs2_rtype', 'io.req[0].bits.uop.lrs3', 'io.req[0].bits.uop.mem_cmd', 'io.req[0].bits.uop.mem_signed', 'io.req[0].bits.uop.mem_size', 'io.req[0].bits.uop.op1_sel', 'io.req[0].bits.uop.op2_sel', 'io.req[0].bits.uop.pc_lob', 'io.req[0].bits.uop.pdst', 'io.req[0].bits.uop.pimm', 'io.req[0].bits.uop.ppred', 'io.req[0].bits.uop.ppred_busy', 'io.req[0].bits.uop.prs1', 'io.req[0].bits.uop.prs1_busy', 'io.req[0].bits.uop.prs2', 'io.req[0].bits.uop.prs2_busy', 'io.req[0].bits.uop.prs3', 'io.req[0].bits.uop.prs3_busy', 'io.req[0].bits.uop.rob_idx', 'io.req[0].bits.uop.rxq_idx', 'io.req[0].bits.uop.stale_pdst', 'io.req[0].bits.uop.stq_idx', 'io.req[0].bits.uop.taken', 'io.req[0].bits.uop.uses_ldq', 'io.req[0].bits.uop.uses_stq', 'io.req[0].bits.uop.xcpt_ae_if', 'io.req[0].bits.uop.xcpt_ma_if', 'io.req[0].bits.uop.xcpt_pf_if', 'io.req[0].bits.way_en']
  - immediate registers: ['mshr_alloc_idx_REG', 'sdq_val']
  - historical registers: ['mshr_alloc_idx_REG', 'mshr_head', 'sdq_val']
- `BoomMSHRFile::io.resp.fire`
  - predicate: `io.resp.valid && io.resp.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile::io.wb_req.fire`
  - predicate: `io.wb_req.valid && io.wb_req.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en']
  - immediate registers: []
  - historical registers: []

## Parent-local concrete state

['beatsLeft', 'beatsLeft_1', 'lb', 'mshr_alloc_idx_REG', 'mshr_head', 'prefetcher_io_mshr_avail_REG', 'prefetcher_io_req_addr_REG', 'prefetcher_io_req_coh_REG', 'prefetcher_io_req_val_REG', 'sdq_val', 'state', 'state_1']

## Parent frontier signals

['clock', 'io.block_hit[0]', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.brupdate.b2.cfi_type', 'io.brupdate.b2.jalr_target', 'io.brupdate.b2.mispredict', 'io.brupdate.b2.pc_sel', 'io.brupdate.b2.taken', 'io.brupdate.b2.target_offset', 'io.brupdate.b2.uop.bp_debug_if', 'io.brupdate.b2.uop.bp_xcpt_if', 'io.brupdate.b2.uop.br_mask', 'io.brupdate.b2.uop.br_tag', 'io.brupdate.b2.uop.br_type', 'io.brupdate.b2.uop.csr_cmd', 'io.brupdate.b2.uop.debug_fsrc', 'io.brupdate.b2.uop.debug_inst', 'io.brupdate.b2.uop.debug_pc', 'io.brupdate.b2.uop.debug_tsrc', 'io.brupdate.b2.uop.dis_col_sel', 'io.brupdate.b2.uop.dst_rtype', 'io.brupdate.b2.uop.edge_inst', 'io.brupdate.b2.uop.exc_cause', 'io.brupdate.b2.uop.exception', 'io.brupdate.b2.uop.fcn_dw', 'io.brupdate.b2.uop.fcn_op', 'io.brupdate.b2.uop.flush_on_commit', 'io.brupdate.b2.uop.fp_ctrl.div', 'io.brupdate.b2.uop.fp_ctrl.fastpipe', 'io.brupdate.b2.uop.fp_ctrl.fma', 'io.brupdate.b2.uop.fp_ctrl.fromint', 'io.brupdate.b2.uop.fp_ctrl.ldst', 'io.brupdate.b2.uop.fp_ctrl.ren1', 'io.brupdate.b2.uop.fp_ctrl.ren2', 'io.brupdate.b2.uop.fp_ctrl.ren3', 'io.brupdate.b2.uop.fp_ctrl.sqrt', 'io.brupdate.b2.uop.fp_ctrl.swap12', 'io.brupdate.b2.uop.fp_ctrl.swap23', 'io.brupdate.b2.uop.fp_ctrl.toint', 'io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'io.brupdate.b2.uop.fp_ctrl.vec', 'io.brupdate.b2.uop.fp_ctrl.wen', 'io.brupdate.b2.uop.fp_ctrl.wflags', 'io.brupdate.b2.uop.fp_rm', 'io.brupdate.b2.uop.fp_typ', 'io.brupdate.b2.uop.fp_val', 'io.brupdate.b2.uop.frs3_en', 'io.brupdate.b2.uop.ftq_idx', 'io.brupdate.b2.uop.fu_code[0]', 'io.brupdate.b2.uop.fu_code[1]', 'io.brupdate.b2.uop.fu_code[2]', 'io.brupdate.b2.uop.fu_code[3]', 'io.brupdate.b2.uop.fu_code[4]', 'io.brupdate.b2.uop.fu_code[5]', 'io.brupdate.b2.uop.fu_code[6]', 'io.brupdate.b2.uop.fu_code[7]', 'io.brupdate.b2.uop.fu_code[8]', 'io.brupdate.b2.uop.fu_code[9]', 'io.brupdate.b2.uop.imm_packed', 'io.brupdate.b2.uop.imm_rename', 'io.brupdate.b2.uop.imm_sel', 'io.brupdate.b2.uop.inst', 'io.brupdate.b2.uop.iq_type[0]', 'io.brupdate.b2.uop.iq_type[1]', 'io.brupdate.b2.uop.iq_type[2]', 'io.brupdate.b2.uop.iq_type[3]', 'io.brupdate.b2.uop.is_amo', 'io.brupdate.b2.uop.is_eret', 'io.brupdate.b2.uop.is_fence', 'io.brupdate.b2.uop.is_fencei', 'io.brupdate.b2.uop.is_mov', 'io.brupdate.b2.uop.is_rocc', 'io.brupdate.b2.uop.is_rvc', 'io.brupdate.b2.uop.is_sfb', 'io.brupdate.b2.uop.is_sfence', 'io.brupdate.b2.uop.is_sys_pc2epc', 'io.brupdate.b2.uop.is_unique', 'io.brupdate.b2.uop.iw_issued', 'io.brupdate.b2.uop.iw_issued_partial_agen', 'io.brupdate.b2.uop.iw_issued_partial_dgen', 'io.brupdate.b2.uop.iw_p1_bypass_hint', 'io.brupdate.b2.uop.iw_p1_speculative_child', 'io.brupdate.b2.uop.iw_p2_bypass_hint', 'io.brupdate.b2.uop.iw_p2_speculative_child', 'io.brupdate.b2.uop.iw_p3_bypass_hint', 'io.brupdate.b2.uop.ldq_idx', 'io.brupdate.b2.uop.ldst', 'io.brupdate.b2.uop.ldst_is_rs1', 'io.brupdate.b2.uop.lrs1', 'io.brupdate.b2.uop.lrs1_rtype', 'io.brupdate.b2.uop.lrs2', 'io.brupdate.b2.uop.lrs2_rtype', 'io.brupdate.b2.uop.lrs3', 'io.brupdate.b2.uop.mem_cmd', 'io.brupdate.b2.uop.mem_signed', 'io.brupdate.b2.uop.mem_size', 'io.brupdate.b2.uop.op1_sel', 'io.brupdate.b2.uop.op2_sel', 'io.brupdate.b2.uop.pc_lob', 'io.brupdate.b2.uop.pdst', 'io.brupdate.b2.uop.pimm', 'io.brupdate.b2.uop.ppred', 'io.brupdate.b2.uop.ppred_busy', 'io.brupdate.b2.uop.prs1', 'io.brupdate.b2.uop.prs1_busy', 'io.brupdate.b2.uop.prs2', 'io.brupdate.b2.uop.prs2_busy', 'io.brupdate.b2.uop.prs3', 'io.brupdate.b2.uop.prs3_busy', 'io.brupdate.b2.uop.rob_idx', 'io.brupdate.b2.uop.rxq_idx', 'io.brupdate.b2.uop.stale_pdst', 'io.brupdate.b2.uop.stq_idx', 'io.brupdate.b2.uop.taken', 'io.brupdate.b2.uop.uses_ldq', 'io.brupdate.b2.uop.uses_stq', 'io.brupdate.b2.uop.xcpt_ae_if', 'io.brupdate.b2.uop.xcpt_ma_if', 'io.brupdate.b2.uop.xcpt_pf_if', 'io.clear_all', 'io.exception', 'io.fence_rdy', 'io.mem_acquire.bits.address', 'io.mem_acquire.bits.corrupt', 'io.mem_acquire.bits.data', 'io.mem_acquire.bits.mask', 'io.mem_acquire.bits.opcode', 'io.mem_acquire.bits.param', 'io.mem_acquire.bits.size', 'io.mem_acquire.bits.source', 'io.mem_acquire.ready', 'io.mem_acquire.valid', 'io.mem_finish.bits.sink', 'io.mem_finish.ready', 'io.mem_finish.valid', 'io.mem_grant.bits.corrupt', 'io.mem_grant.bits.data', 'io.mem_grant.bits.denied', 'io.mem_grant.bits.opcode', 'io.mem_grant.bits.param', 'io.mem_grant.bits.sink', 'io.mem_grant.bits.size', 'io.mem_grant.bits.source', 'io.mem_grant.ready', 'io.mem_grant.valid', 'io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en', 'io.meta_read.ready', 'io.meta_read.valid', 'io.meta_resp.bits.coh.state', 'io.meta_resp.bits.tag', 'io.meta_resp.valid', 'io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en', 'io.meta_write.ready', 'io.meta_write.valid', 'io.prefetch.bits.addr', 'io.prefetch.bits.data', 'io.prefetch.bits.is_hella', 'io.prefetch.bits.uop.bp_debug_if', 'io.prefetch.bits.uop.bp_xcpt_if', 'io.prefetch.bits.uop.br_mask', 'io.prefetch.bits.uop.br_tag', 'io.prefetch.bits.uop.br_type', 'io.prefetch.bits.uop.csr_cmd', 'io.prefetch.bits.uop.debug_fsrc', 'io.prefetch.bits.uop.debug_inst', 'io.prefetch.bits.uop.debug_pc', 'io.prefetch.bits.uop.debug_tsrc', 'io.prefetch.bits.uop.dis_col_sel', 'io.prefetch.bits.uop.dst_rtype', 'io.prefetch.bits.uop.edge_inst', 'io.prefetch.bits.uop.exc_cause', 'io.prefetch.bits.uop.exception', 'io.prefetch.bits.uop.fcn_dw', 'io.prefetch.bits.uop.fcn_op', 'io.prefetch.bits.uop.flush_on_commit', 'io.prefetch.bits.uop.fp_ctrl.div', 'io.prefetch.bits.uop.fp_ctrl.fastpipe', 'io.prefetch.bits.uop.fp_ctrl.fma', 'io.prefetch.bits.uop.fp_ctrl.fromint', 'io.prefetch.bits.uop.fp_ctrl.ldst', 'io.prefetch.bits.uop.fp_ctrl.ren1', 'io.prefetch.bits.uop.fp_ctrl.ren2', 'io.prefetch.bits.uop.fp_ctrl.ren3', 'io.prefetch.bits.uop.fp_ctrl.sqrt', 'io.prefetch.bits.uop.fp_ctrl.swap12', 'io.prefetch.bits.uop.fp_ctrl.swap23', 'io.prefetch.bits.uop.fp_ctrl.toint', 'io.prefetch.bits.uop.fp_ctrl.typeTagIn', 'io.prefetch.bits.uop.fp_ctrl.typeTagOut', 'io.prefetch.bits.uop.fp_ctrl.vec', 'io.prefetch.bits.uop.fp_ctrl.wen', 'io.prefetch.bits.uop.fp_ctrl.wflags', 'io.prefetch.bits.uop.fp_rm', 'io.prefetch.bits.uop.fp_typ', 'io.prefetch.bits.uop.fp_val', 'io.prefetch.bits.uop.frs3_en', 'io.prefetch.bits.uop.ftq_idx', 'io.prefetch.bits.uop.fu_code[0]', 'io.prefetch.bits.uop.fu_code[1]', 'io.prefetch.bits.uop.fu_code[2]', 'io.prefetch.bits.uop.fu_code[3]', 'io.prefetch.bits.uop.fu_code[4]', 'io.prefetch.bits.uop.fu_code[5]', 'io.prefetch.bits.uop.fu_code[6]', 'io.prefetch.bits.uop.fu_code[7]', 'io.prefetch.bits.uop.fu_code[8]', 'io.prefetch.bits.uop.fu_code[9]', 'io.prefetch.bits.uop.imm_packed', 'io.prefetch.bits.uop.imm_rename', 'io.prefetch.bits.uop.imm_sel', 'io.prefetch.bits.uop.inst', 'io.prefetch.bits.uop.iq_type[0]', 'io.prefetch.bits.uop.iq_type[1]', 'io.prefetch.bits.uop.iq_type[2]', 'io.prefetch.bits.uop.iq_type[3]', 'io.prefetch.bits.uop.is_amo', 'io.prefetch.bits.uop.is_eret', 'io.prefetch.bits.uop.is_fence', 'io.prefetch.bits.uop.is_fencei', 'io.prefetch.bits.uop.is_mov', 'io.prefetch.bits.uop.is_rocc', 'io.prefetch.bits.uop.is_rvc', 'io.prefetch.bits.uop.is_sfb', 'io.prefetch.bits.uop.is_sfence', 'io.prefetch.bits.uop.is_sys_pc2epc', 'io.prefetch.bits.uop.is_unique', 'io.prefetch.bits.uop.iw_issued', 'io.prefetch.bits.uop.iw_issued_partial_agen', 'io.prefetch.bits.uop.iw_issued_partial_dgen', 'io.prefetch.bits.uop.iw_p1_bypass_hint', 'io.prefetch.bits.uop.iw_p1_speculative_child', 'io.prefetch.bits.uop.iw_p2_bypass_hint', 'io.prefetch.bits.uop.iw_p2_speculative_child', 'io.prefetch.bits.uop.iw_p3_bypass_hint', 'io.prefetch.bits.uop.ldq_idx', 'io.prefetch.bits.uop.ldst', 'io.prefetch.bits.uop.ldst_is_rs1', 'io.prefetch.bits.uop.lrs1', 'io.prefetch.bits.uop.lrs1_rtype', 'io.prefetch.bits.uop.lrs2', 'io.prefetch.bits.uop.lrs2_rtype', 'io.prefetch.bits.uop.lrs3', 'io.prefetch.bits.uop.mem_cmd', 'io.prefetch.bits.uop.mem_signed', 'io.prefetch.bits.uop.mem_size', 'io.prefetch.bits.uop.op1_sel', 'io.prefetch.bits.uop.op2_sel', 'io.prefetch.bits.uop.pc_lob', 'io.prefetch.bits.uop.pdst', 'io.prefetch.bits.uop.pimm', 'io.prefetch.bits.uop.ppred', 'io.prefetch.bits.uop.ppred_busy', 'io.prefetch.bits.uop.prs1', 'io.prefetch.bits.uop.prs1_busy', 'io.prefetch.bits.uop.prs2', 'io.prefetch.bits.uop.prs2_busy', 'io.prefetch.bits.uop.prs3', 'io.prefetch.bits.uop.prs3_busy', 'io.prefetch.bits.uop.rob_idx', 'io.prefetch.bits.uop.rxq_idx', 'io.prefetch.bits.uop.stale_pdst', 'io.prefetch.bits.uop.stq_idx', 'io.prefetch.bits.uop.taken', 'io.prefetch.bits.uop.uses_ldq', 'io.prefetch.bits.uop.uses_stq', 'io.prefetch.bits.uop.xcpt_ae_if', 'io.prefetch.bits.uop.xcpt_ma_if', 'io.prefetch.bits.uop.xcpt_pf_if', 'io.prefetch.ready', 'io.prefetch.valid', 'io.probe_rdy', 'io.prober_state.bits', 'io.prober_state.valid', 'io.refill.bits.addr', 'io.refill.bits.data', 'io.refill.bits.way_en', 'io.refill.bits.wmask', 'io.refill.ready', 'io.refill.valid', 'io.replay.bits.addr', 'io.replay.bits.data', 'io.replay.bits.is_hella', 'io.replay.bits.old_meta.coh.state', 'io.replay.bits.old_meta.tag', 'io.replay.bits.sdq_id', 'io.replay.bits.tag_match', 'io.replay.bits.uop.bp_debug_if', 'io.replay.bits.uop.bp_xcpt_if', 'io.replay.bits.uop.br_mask', 'io.replay.bits.uop.br_tag', 'io.replay.bits.uop.br_type', 'io.replay.bits.uop.csr_cmd', 'io.replay.bits.uop.debug_fsrc', 'io.replay.bits.uop.debug_inst', 'io.replay.bits.uop.debug_pc', 'io.replay.bits.uop.debug_tsrc', 'io.replay.bits.uop.dis_col_sel', 'io.replay.bits.uop.dst_rtype', 'io.replay.bits.uop.edge_inst', 'io.replay.bits.uop.exc_cause', 'io.replay.bits.uop.exception', 'io.replay.bits.uop.fcn_dw', 'io.replay.bits.uop.fcn_op', 'io.replay.bits.uop.flush_on_commit', 'io.replay.bits.uop.fp_ctrl.div', 'io.replay.bits.uop.fp_ctrl.fastpipe', 'io.replay.bits.uop.fp_ctrl.fma', 'io.replay.bits.uop.fp_ctrl.fromint', 'io.replay.bits.uop.fp_ctrl.ldst', 'io.replay.bits.uop.fp_ctrl.ren1', 'io.replay.bits.uop.fp_ctrl.ren2', 'io.replay.bits.uop.fp_ctrl.ren3', 'io.replay.bits.uop.fp_ctrl.sqrt', 'io.replay.bits.uop.fp_ctrl.swap12', 'io.replay.bits.uop.fp_ctrl.swap23', 'io.replay.bits.uop.fp_ctrl.toint', 'io.replay.bits.uop.fp_ctrl.typeTagIn', 'io.replay.bits.uop.fp_ctrl.typeTagOut', 'io.replay.bits.uop.fp_ctrl.vec', 'io.replay.bits.uop.fp_ctrl.wen', 'io.replay.bits.uop.fp_ctrl.wflags', 'io.replay.bits.uop.fp_rm', 'io.replay.bits.uop.fp_typ', 'io.replay.bits.uop.fp_val', 'io.replay.bits.uop.frs3_en', 'io.replay.bits.uop.ftq_idx', 'io.replay.bits.uop.fu_code[0]', 'io.replay.bits.uop.fu_code[1]', 'io.replay.bits.uop.fu_code[2]', 'io.replay.bits.uop.fu_code[3]', 'io.replay.bits.uop.fu_code[4]', 'io.replay.bits.uop.fu_code[5]', 'io.replay.bits.uop.fu_code[6]', 'io.replay.bits.uop.fu_code[7]', 'io.replay.bits.uop.fu_code[8]', 'io.replay.bits.uop.fu_code[9]', 'io.replay.bits.uop.imm_packed', 'io.replay.bits.uop.imm_rename', 'io.replay.bits.uop.imm_sel', 'io.replay.bits.uop.inst', 'io.replay.bits.uop.iq_type[0]', 'io.replay.bits.uop.iq_type[1]', 'io.replay.bits.uop.iq_type[2]', 'io.replay.bits.uop.iq_type[3]', 'io.replay.bits.uop.is_amo', 'io.replay.bits.uop.is_eret', 'io.replay.bits.uop.is_fence', 'io.replay.bits.uop.is_fencei', 'io.replay.bits.uop.is_mov', 'io.replay.bits.uop.is_rocc', 'io.replay.bits.uop.is_rvc', 'io.replay.bits.uop.is_sfb', 'io.replay.bits.uop.is_sfence', 'io.replay.bits.uop.is_sys_pc2epc', 'io.replay.bits.uop.is_unique', 'io.replay.bits.uop.iw_issued', 'io.replay.bits.uop.iw_issued_partial_agen', 'io.replay.bits.uop.iw_issued_partial_dgen', 'io.replay.bits.uop.iw_p1_bypass_hint', 'io.replay.bits.uop.iw_p1_speculative_child', 'io.replay.bits.uop.iw_p2_bypass_hint', 'io.replay.bits.uop.iw_p2_speculative_child', 'io.replay.bits.uop.iw_p3_bypass_hint', 'io.replay.bits.uop.ldq_idx', 'io.replay.bits.uop.ldst', 'io.replay.bits.uop.ldst_is_rs1', 'io.replay.bits.uop.lrs1', 'io.replay.bits.uop.lrs1_rtype', 'io.replay.bits.uop.lrs2', 'io.replay.bits.uop.lrs2_rtype', 'io.replay.bits.uop.lrs3', 'io.replay.bits.uop.mem_cmd', 'io.replay.bits.uop.mem_signed', 'io.replay.bits.uop.mem_size', 'io.replay.bits.uop.op1_sel', 'io.replay.bits.uop.op2_sel', 'io.replay.bits.uop.pc_lob', 'io.replay.bits.uop.pdst', 'io.replay.bits.uop.pimm', 'io.replay.bits.uop.ppred', 'io.replay.bits.uop.ppred_busy', 'io.replay.bits.uop.prs1', 'io.replay.bits.uop.prs1_busy', 'io.replay.bits.uop.prs2', 'io.replay.bits.uop.prs2_busy', 'io.replay.bits.uop.prs3', 'io.replay.bits.uop.prs3_busy', 'io.replay.bits.uop.rob_idx', 'io.replay.bits.uop.rxq_idx', 'io.replay.bits.uop.stale_pdst', 'io.replay.bits.uop.stq_idx', 'io.replay.bits.uop.taken', 'io.replay.bits.uop.uses_ldq', 'io.replay.bits.uop.uses_stq', 'io.replay.bits.uop.xcpt_ae_if', 'io.replay.bits.uop.xcpt_ma_if', 'io.replay.bits.uop.xcpt_pf_if', 'io.replay.bits.way_en', 'io.replay.ready', 'io.replay.valid', 'io.req[0].bits.addr', 'io.req[0].bits.way_en', 'io.req[0].ready', 'io.req[0].valid', 'io.req_is_probe[0]', 'io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if', 'io.resp.ready', 'io.resp.valid', 'io.rob_head_idx', 'io.rob_pnr_idx', 'io.secondary_miss[0]', 'io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en', 'io.wb_req.ready', 'io.wb_req.valid', 'io.wb_resp', 'meta_read_arb.clock', 'meta_read_arb.io.in[0].bits.idx', 'meta_read_arb.io.in[0].bits.tag', 'meta_read_arb.io.in[0].bits.way_en', 'meta_read_arb.io.in[0].ready', 'meta_read_arb.io.in[0].valid', 'meta_read_arb.io.in[1].bits.idx', 'meta_read_arb.io.in[1].bits.tag', 'meta_read_arb.io.in[1].bits.way_en', 'meta_read_arb.io.in[1].ready', 'meta_read_arb.io.in[1].valid', 'meta_read_arb.io.out.ready', 'meta_read_arb.io.out.valid', 'meta_read_arb.reset', 'meta_write_arb.clock', 'meta_write_arb.io.in[0].bits.data.coh.state', 'meta_write_arb.io.in[0].bits.data.tag', 'meta_write_arb.io.in[0].bits.idx', 'meta_write_arb.io.in[0].bits.tag', 'meta_write_arb.io.in[0].bits.way_en', 'meta_write_arb.io.in[0].ready', 'meta_write_arb.io.in[0].valid', 'meta_write_arb.io.in[1].bits.data.coh.state', 'meta_write_arb.io.in[1].bits.data.tag', 'meta_write_arb.io.in[1].bits.idx', 'meta_write_arb.io.in[1].bits.tag', 'meta_write_arb.io.in[1].bits.way_en', 'meta_write_arb.io.in[1].ready', 'meta_write_arb.io.in[1].valid', 'meta_write_arb.io.out.ready', 'meta_write_arb.io.out.valid', 'meta_write_arb.reset', 'mmio_alloc_arb.clock', 'mmio_alloc_arb.io.in[0].bits', 'mmio_alloc_arb.io.in[0].ready', 'mmio_alloc_arb.io.in[0].valid', 'mmio_alloc_arb.io.out.ready', 'mmio_alloc_arb.reset', 'mmios_0.clock', 'mmios_0.io.mem_access.bits.address', 'mmios_0.io.mem_access.bits.corrupt', 'mmios_0.io.mem_access.bits.data', 'mmios_0.io.mem_access.bits.mask', 'mmios_0.io.mem_access.bits.opcode', 'mmios_0.io.mem_access.bits.param', 'mmios_0.io.mem_access.bits.size', 'mmios_0.io.mem_access.bits.source', 'mmios_0.io.mem_access.ready', 'mmios_0.io.mem_access.valid', 'mmios_0.io.mem_ack.bits.corrupt', 'mmios_0.io.mem_ack.bits.data', 'mmios_0.io.mem_ack.bits.denied', 'mmios_0.io.mem_ack.bits.opcode', 'mmios_0.io.mem_ack.bits.param', 'mmios_0.io.mem_ack.bits.sink', 'mmios_0.io.mem_ack.bits.size', 'mmios_0.io.mem_ack.bits.source', 'mmios_0.io.mem_ack.valid', 'mmios_0.io.req.bits.addr', 'mmios_0.io.req.bits.data', 'mmios_0.io.req.bits.is_hella', 'mmios_0.io.req.bits.uop.bp_debug_if', 'mmios_0.io.req.bits.uop.bp_xcpt_if', 'mmios_0.io.req.bits.uop.br_mask', 'mmios_0.io.req.bits.uop.br_tag', 'mmios_0.io.req.bits.uop.br_type', 'mmios_0.io.req.bits.uop.csr_cmd', 'mmios_0.io.req.bits.uop.debug_fsrc', 'mmios_0.io.req.bits.uop.debug_inst', 'mmios_0.io.req.bits.uop.debug_pc', 'mmios_0.io.req.bits.uop.debug_tsrc', 'mmios_0.io.req.bits.uop.dis_col_sel', 'mmios_0.io.req.bits.uop.dst_rtype', 'mmios_0.io.req.bits.uop.edge_inst', 'mmios_0.io.req.bits.uop.exc_cause', 'mmios_0.io.req.bits.uop.exception', 'mmios_0.io.req.bits.uop.fcn_dw', 'mmios_0.io.req.bits.uop.fcn_op', 'mmios_0.io.req.bits.uop.flush_on_commit', 'mmios_0.io.req.bits.uop.fp_ctrl.div', 'mmios_0.io.req.bits.uop.fp_ctrl.fastpipe', 'mmios_0.io.req.bits.uop.fp_ctrl.fma', 'mmios_0.io.req.bits.uop.fp_ctrl.fromint', 'mmios_0.io.req.bits.uop.fp_ctrl.ldst', 'mmios_0.io.req.bits.uop.fp_ctrl.ren1', 'mmios_0.io.req.bits.uop.fp_ctrl.ren2', 'mmios_0.io.req.bits.uop.fp_ctrl.ren3', 'mmios_0.io.req.bits.uop.fp_ctrl.sqrt', 'mmios_0.io.req.bits.uop.fp_ctrl.swap12', 'mmios_0.io.req.bits.uop.fp_ctrl.swap23', 'mmios_0.io.req.bits.uop.fp_ctrl.toint', 'mmios_0.io.req.bits.uop.fp_ctrl.typeTagIn', 'mmios_0.io.req.bits.uop.fp_ctrl.typeTagOut', 'mmios_0.io.req.bits.uop.fp_ctrl.vec', 'mmios_0.io.req.bits.uop.fp_ctrl.wen', 'mmios_0.io.req.bits.uop.fp_ctrl.wflags', 'mmios_0.io.req.bits.uop.fp_rm', 'mmios_0.io.req.bits.uop.fp_typ', 'mmios_0.io.req.bits.uop.fp_val', 'mmios_0.io.req.bits.uop.frs3_en', 'mmios_0.io.req.bits.uop.ftq_idx', 'mmios_0.io.req.bits.uop.fu_code[0]', 'mmios_0.io.req.bits.uop.fu_code[1]', 'mmios_0.io.req.bits.uop.fu_code[2]', 'mmios_0.io.req.bits.uop.fu_code[3]', 'mmios_0.io.req.bits.uop.fu_code[4]', 'mmios_0.io.req.bits.uop.fu_code[5]', 'mmios_0.io.req.bits.uop.fu_code[6]', 'mmios_0.io.req.bits.uop.fu_code[7]', 'mmios_0.io.req.bits.uop.fu_code[8]', 'mmios_0.io.req.bits.uop.fu_code[9]', 'mmios_0.io.req.bits.uop.imm_packed', 'mmios_0.io.req.bits.uop.imm_rename', 'mmios_0.io.req.bits.uop.imm_sel', 'mmios_0.io.req.bits.uop.inst', 'mmios_0.io.req.bits.uop.iq_type[0]', 'mmios_0.io.req.bits.uop.iq_type[1]', 'mmios_0.io.req.bits.uop.iq_type[2]', 'mmios_0.io.req.bits.uop.iq_type[3]', 'mmios_0.io.req.bits.uop.is_amo', 'mmios_0.io.req.bits.uop.is_eret', 'mmios_0.io.req.bits.uop.is_fence', 'mmios_0.io.req.bits.uop.is_fencei', 'mmios_0.io.req.bits.uop.is_mov', 'mmios_0.io.req.bits.uop.is_rocc', 'mmios_0.io.req.bits.uop.is_rvc', 'mmios_0.io.req.bits.uop.is_sfb', 'mmios_0.io.req.bits.uop.is_sfence', 'mmios_0.io.req.bits.uop.is_sys_pc2epc', 'mmios_0.io.req.bits.uop.is_unique', 'mmios_0.io.req.bits.uop.iw_issued', 'mmios_0.io.req.bits.uop.iw_issued_partial_agen', 'mmios_0.io.req.bits.uop.iw_issued_partial_dgen', 'mmios_0.io.req.bits.uop.iw_p1_bypass_hint', 'mmios_0.io.req.bits.uop.iw_p1_speculative_child', 'mmios_0.io.req.bits.uop.iw_p2_bypass_hint', 'mmios_0.io.req.bits.uop.iw_p2_speculative_child', 'mmios_0.io.req.bits.uop.iw_p3_bypass_hint', 'mmios_0.io.req.bits.uop.ldq_idx', 'mmios_0.io.req.bits.uop.ldst', 'mmios_0.io.req.bits.uop.ldst_is_rs1', 'mmios_0.io.req.bits.uop.lrs1', 'mmios_0.io.req.bits.uop.lrs1_rtype', 'mmios_0.io.req.bits.uop.lrs2', 'mmios_0.io.req.bits.uop.lrs2_rtype', 'mmios_0.io.req.bits.uop.lrs3', 'mmios_0.io.req.bits.uop.mem_cmd', 'mmios_0.io.req.bits.uop.mem_signed', 'mmios_0.io.req.bits.uop.mem_size', 'mmios_0.io.req.bits.uop.op1_sel', 'mmios_0.io.req.bits.uop.op2_sel', 'mmios_0.io.req.bits.uop.pc_lob', 'mmios_0.io.req.bits.uop.pdst', 'mmios_0.io.req.bits.uop.pimm', 'mmios_0.io.req.bits.uop.ppred', 'mmios_0.io.req.bits.uop.ppred_busy', 'mmios_0.io.req.bits.uop.prs1', 'mmios_0.io.req.bits.uop.prs1_busy', 'mmios_0.io.req.bits.uop.prs2', 'mmios_0.io.req.bits.uop.prs2_busy', 'mmios_0.io.req.bits.uop.prs3', 'mmios_0.io.req.bits.uop.prs3_busy', 'mmios_0.io.req.bits.uop.rob_idx', 'mmios_0.io.req.bits.uop.rxq_idx', 'mmios_0.io.req.bits.uop.stale_pdst', 'mmios_0.io.req.bits.uop.stq_idx', 'mmios_0.io.req.bits.uop.taken', 'mmios_0.io.req.bits.uop.uses_ldq', 'mmios_0.io.req.bits.uop.uses_stq', 'mmios_0.io.req.bits.uop.xcpt_ae_if', 'mmios_0.io.req.bits.uop.xcpt_ma_if', 'mmios_0.io.req.bits.uop.xcpt_pf_if', 'mmios_0.io.req.ready', 'mmios_0.io.req.valid', 'mmios_0.reset', 'mshrs_0.clock', 'mshrs_0.io.brupdate.b1.mispredict_mask', 'mshrs_0.io.brupdate.b1.resolve_mask', 'mshrs_0.io.brupdate.b2.cfi_type', 'mshrs_0.io.brupdate.b2.jalr_target', 'mshrs_0.io.brupdate.b2.mispredict', 'mshrs_0.io.brupdate.b2.pc_sel', 'mshrs_0.io.brupdate.b2.taken', 'mshrs_0.io.brupdate.b2.target_offset', 'mshrs_0.io.brupdate.b2.uop.bp_debug_if', 'mshrs_0.io.brupdate.b2.uop.bp_xcpt_if', 'mshrs_0.io.brupdate.b2.uop.br_mask', 'mshrs_0.io.brupdate.b2.uop.br_tag', 'mshrs_0.io.brupdate.b2.uop.br_type', 'mshrs_0.io.brupdate.b2.uop.csr_cmd', 'mshrs_0.io.brupdate.b2.uop.debug_fsrc', 'mshrs_0.io.brupdate.b2.uop.debug_inst', 'mshrs_0.io.brupdate.b2.uop.debug_pc', 'mshrs_0.io.brupdate.b2.uop.debug_tsrc', 'mshrs_0.io.brupdate.b2.uop.dis_col_sel', 'mshrs_0.io.brupdate.b2.uop.dst_rtype', 'mshrs_0.io.brupdate.b2.uop.edge_inst', 'mshrs_0.io.brupdate.b2.uop.exc_cause', 'mshrs_0.io.brupdate.b2.uop.exception', 'mshrs_0.io.brupdate.b2.uop.fcn_dw', 'mshrs_0.io.brupdate.b2.uop.fcn_op', 'mshrs_0.io.brupdate.b2.uop.flush_on_commit', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.div', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fma', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fromint', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ldst', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren1', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren2', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren3', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.sqrt', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap12', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap23', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.toint', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.vec', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.wen', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.wflags', 'mshrs_0.io.brupdate.b2.uop.fp_rm', 'mshrs_0.io.brupdate.b2.uop.fp_typ', 'mshrs_0.io.brupdate.b2.uop.fp_val', 'mshrs_0.io.brupdate.b2.uop.frs3_en', 'mshrs_0.io.brupdate.b2.uop.ftq_idx', 'mshrs_0.io.brupdate.b2.uop.fu_code[0]', 'mshrs_0.io.brupdate.b2.uop.fu_code[1]', 'mshrs_0.io.brupdate.b2.uop.fu_code[2]', 'mshrs_0.io.brupdate.b2.uop.fu_code[3]', 'mshrs_0.io.brupdate.b2.uop.fu_code[4]', 'mshrs_0.io.brupdate.b2.uop.fu_code[5]', 'mshrs_0.io.brupdate.b2.uop.fu_code[6]', 'mshrs_0.io.brupdate.b2.uop.fu_code[7]', 'mshrs_0.io.brupdate.b2.uop.fu_code[8]', 'mshrs_0.io.brupdate.b2.uop.fu_code[9]', 'mshrs_0.io.brupdate.b2.uop.imm_packed', 'mshrs_0.io.brupdate.b2.uop.imm_rename', 'mshrs_0.io.brupdate.b2.uop.imm_sel', 'mshrs_0.io.brupdate.b2.uop.inst', 'mshrs_0.io.brupdate.b2.uop.iq_type[0]', 'mshrs_0.io.brupdate.b2.uop.iq_type[1]', 'mshrs_0.io.brupdate.b2.uop.iq_type[2]', 'mshrs_0.io.brupdate.b2.uop.iq_type[3]', 'mshrs_0.io.brupdate.b2.uop.is_amo', 'mshrs_0.io.brupdate.b2.uop.is_eret', 'mshrs_0.io.brupdate.b2.uop.is_fence', 'mshrs_0.io.brupdate.b2.uop.is_fencei', 'mshrs_0.io.brupdate.b2.uop.is_mov', 'mshrs_0.io.brupdate.b2.uop.is_rocc', 'mshrs_0.io.brupdate.b2.uop.is_rvc', 'mshrs_0.io.brupdate.b2.uop.is_sfb', 'mshrs_0.io.brupdate.b2.uop.is_sfence', 'mshrs_0.io.brupdate.b2.uop.is_sys_pc2epc', 'mshrs_0.io.brupdate.b2.uop.is_unique', 'mshrs_0.io.brupdate.b2.uop.iw_issued', 'mshrs_0.io.brupdate.b2.uop.iw_issued_partial_agen', 'mshrs_0.io.brupdate.b2.uop.iw_issued_partial_dgen', 'mshrs_0.io.brupdate.b2.uop.iw_p1_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.iw_p1_speculative_child', 'mshrs_0.io.brupdate.b2.uop.iw_p2_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.iw_p2_speculative_child', 'mshrs_0.io.brupdate.b2.uop.iw_p3_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.ldq_idx', 'mshrs_0.io.brupdate.b2.uop.ldst', 'mshrs_0.io.brupdate.b2.uop.ldst_is_rs1', 'mshrs_0.io.brupdate.b2.uop.lrs1', 'mshrs_0.io.brupdate.b2.uop.lrs1_rtype', 'mshrs_0.io.brupdate.b2.uop.lrs2', 'mshrs_0.io.brupdate.b2.uop.lrs2_rtype', 'mshrs_0.io.brupdate.b2.uop.lrs3', 'mshrs_0.io.brupdate.b2.uop.mem_cmd', 'mshrs_0.io.brupdate.b2.uop.mem_signed', 'mshrs_0.io.brupdate.b2.uop.mem_size', 'mshrs_0.io.brupdate.b2.uop.op1_sel', 'mshrs_0.io.brupdate.b2.uop.op2_sel', 'mshrs_0.io.brupdate.b2.uop.pc_lob', 'mshrs_0.io.brupdate.b2.uop.pdst', 'mshrs_0.io.brupdate.b2.uop.pimm', 'mshrs_0.io.brupdate.b2.uop.ppred', 'mshrs_0.io.brupdate.b2.uop.ppred_busy', 'mshrs_0.io.brupdate.b2.uop.prs1', 'mshrs_0.io.brupdate.b2.uop.prs1_busy', 'mshrs_0.io.brupdate.b2.uop.prs2', 'mshrs_0.io.brupdate.b2.uop.prs2_busy', 'mshrs_0.io.brupdate.b2.uop.prs3', 'mshrs_0.io.brupdate.b2.uop.prs3_busy', 'mshrs_0.io.brupdate.b2.uop.rob_idx', 'mshrs_0.io.brupdate.b2.uop.rxq_idx', 'mshrs_0.io.brupdate.b2.uop.stale_pdst', 'mshrs_0.io.brupdate.b2.uop.stq_idx', 'mshrs_0.io.brupdate.b2.uop.taken', 'mshrs_0.io.brupdate.b2.uop.uses_ldq', 'mshrs_0.io.brupdate.b2.uop.uses_stq', 'mshrs_0.io.brupdate.b2.uop.xcpt_ae_if', 'mshrs_0.io.brupdate.b2.uop.xcpt_ma_if', 'mshrs_0.io.brupdate.b2.uop.xcpt_pf_if', 'mshrs_0.io.clear_prefetch', 'mshrs_0.io.commit_addr', 'mshrs_0.io.commit_val', 'mshrs_0.io.exception', 'mshrs_0.io.id', 'mshrs_0.io.idx.bits', 'mshrs_0.io.idx.valid', 'mshrs_0.io.lb_read.offset', 'mshrs_0.io.lb_resp', 'mshrs_0.io.lb_write.bits.data', 'mshrs_0.io.lb_write.bits.offset', 'mshrs_0.io.lb_write.valid', 'mshrs_0.io.mem_acquire.bits.address', 'mshrs_0.io.mem_acquire.bits.corrupt', 'mshrs_0.io.mem_acquire.bits.data', 'mshrs_0.io.mem_acquire.bits.mask', 'mshrs_0.io.mem_acquire.bits.opcode', 'mshrs_0.io.mem_acquire.bits.param', 'mshrs_0.io.mem_acquire.bits.size', 'mshrs_0.io.mem_acquire.bits.source', 'mshrs_0.io.mem_acquire.ready', 'mshrs_0.io.mem_acquire.valid', 'mshrs_0.io.mem_finish.bits.sink', 'mshrs_0.io.mem_finish.ready', 'mshrs_0.io.mem_finish.valid', 'mshrs_0.io.mem_grant.bits.corrupt', 'mshrs_0.io.mem_grant.bits.data', 'mshrs_0.io.mem_grant.bits.denied', 'mshrs_0.io.mem_grant.bits.opcode', 'mshrs_0.io.mem_grant.bits.param', 'mshrs_0.io.mem_grant.bits.sink', 'mshrs_0.io.mem_grant.bits.size', 'mshrs_0.io.mem_grant.bits.source', 'mshrs_0.io.mem_grant.ready', 'mshrs_0.io.mem_grant.valid', 'mshrs_0.io.meta_resp.bits.coh.state', 'mshrs_0.io.meta_resp.bits.tag', 'mshrs_0.io.meta_resp.valid', 'mshrs_0.io.probe_rdy', 'mshrs_0.io.prober_state.bits', 'mshrs_0.io.prober_state.valid', 'mshrs_0.io.req.addr', 'mshrs_0.io.req.data', 'mshrs_0.io.req.is_hella', 'mshrs_0.io.req.old_meta.coh.state', 'mshrs_0.io.req.old_meta.tag', 'mshrs_0.io.req.sdq_id', 'mshrs_0.io.req.tag_match', 'mshrs_0.io.req.uop.bp_debug_if', 'mshrs_0.io.req.uop.bp_xcpt_if', 'mshrs_0.io.req.uop.br_mask', 'mshrs_0.io.req.uop.br_tag', 'mshrs_0.io.req.uop.br_type', 'mshrs_0.io.req.uop.csr_cmd', 'mshrs_0.io.req.uop.debug_fsrc', 'mshrs_0.io.req.uop.debug_inst', 'mshrs_0.io.req.uop.debug_pc', 'mshrs_0.io.req.uop.debug_tsrc', 'mshrs_0.io.req.uop.dis_col_sel', 'mshrs_0.io.req.uop.dst_rtype', 'mshrs_0.io.req.uop.edge_inst', 'mshrs_0.io.req.uop.exc_cause', 'mshrs_0.io.req.uop.exception', 'mshrs_0.io.req.uop.fcn_dw', 'mshrs_0.io.req.uop.fcn_op', 'mshrs_0.io.req.uop.flush_on_commit', 'mshrs_0.io.req.uop.fp_ctrl.div', 'mshrs_0.io.req.uop.fp_ctrl.fastpipe', 'mshrs_0.io.req.uop.fp_ctrl.fma', 'mshrs_0.io.req.uop.fp_ctrl.fromint', 'mshrs_0.io.req.uop.fp_ctrl.ldst', 'mshrs_0.io.req.uop.fp_ctrl.ren1', 'mshrs_0.io.req.uop.fp_ctrl.ren2', 'mshrs_0.io.req.uop.fp_ctrl.ren3', 'mshrs_0.io.req.uop.fp_ctrl.sqrt', 'mshrs_0.io.req.uop.fp_ctrl.swap12', 'mshrs_0.io.req.uop.fp_ctrl.swap23', 'mshrs_0.io.req.uop.fp_ctrl.toint', 'mshrs_0.io.req.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.req.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.req.uop.fp_ctrl.vec', 'mshrs_0.io.req.uop.fp_ctrl.wen', 'mshrs_0.io.req.uop.fp_ctrl.wflags', 'mshrs_0.io.req.uop.fp_rm', 'mshrs_0.io.req.uop.fp_typ', 'mshrs_0.io.req.uop.fp_val', 'mshrs_0.io.req.uop.frs3_en', 'mshrs_0.io.req.uop.ftq_idx', 'mshrs_0.io.req.uop.fu_code[0]', 'mshrs_0.io.req.uop.fu_code[1]', 'mshrs_0.io.req.uop.fu_code[2]', 'mshrs_0.io.req.uop.fu_code[3]', 'mshrs_0.io.req.uop.fu_code[4]', 'mshrs_0.io.req.uop.fu_code[5]', 'mshrs_0.io.req.uop.fu_code[6]', 'mshrs_0.io.req.uop.fu_code[7]', 'mshrs_0.io.req.uop.fu_code[8]', 'mshrs_0.io.req.uop.fu_code[9]', 'mshrs_0.io.req.uop.imm_packed', 'mshrs_0.io.req.uop.imm_rename', 'mshrs_0.io.req.uop.imm_sel', 'mshrs_0.io.req.uop.inst', 'mshrs_0.io.req.uop.iq_type[0]', 'mshrs_0.io.req.uop.iq_type[1]', 'mshrs_0.io.req.uop.iq_type[2]', 'mshrs_0.io.req.uop.iq_type[3]', 'mshrs_0.io.req.uop.is_amo', 'mshrs_0.io.req.uop.is_eret', 'mshrs_0.io.req.uop.is_fence', 'mshrs_0.io.req.uop.is_fencei', 'mshrs_0.io.req.uop.is_mov', 'mshrs_0.io.req.uop.is_rocc', 'mshrs_0.io.req.uop.is_rvc', 'mshrs_0.io.req.uop.is_sfb', 'mshrs_0.io.req.uop.is_sfence', 'mshrs_0.io.req.uop.is_sys_pc2epc', 'mshrs_0.io.req.uop.is_unique', 'mshrs_0.io.req.uop.iw_issued', 'mshrs_0.io.req.uop.iw_issued_partial_agen', 'mshrs_0.io.req.uop.iw_issued_partial_dgen', 'mshrs_0.io.req.uop.iw_p1_bypass_hint', 'mshrs_0.io.req.uop.iw_p1_speculative_child', 'mshrs_0.io.req.uop.iw_p2_bypass_hint', 'mshrs_0.io.req.uop.iw_p2_speculative_child', 'mshrs_0.io.req.uop.iw_p3_bypass_hint', 'mshrs_0.io.req.uop.ldq_idx', 'mshrs_0.io.req.uop.ldst', 'mshrs_0.io.req.uop.ldst_is_rs1', 'mshrs_0.io.req.uop.lrs1', 'mshrs_0.io.req.uop.lrs1_rtype', 'mshrs_0.io.req.uop.lrs2', 'mshrs_0.io.req.uop.lrs2_rtype', 'mshrs_0.io.req.uop.lrs3', 'mshrs_0.io.req.uop.mem_cmd', 'mshrs_0.io.req.uop.mem_signed', 'mshrs_0.io.req.uop.mem_size', 'mshrs_0.io.req.uop.op1_sel', 'mshrs_0.io.req.uop.op2_sel', 'mshrs_0.io.req.uop.pc_lob', 'mshrs_0.io.req.uop.pdst', 'mshrs_0.io.req.uop.pimm', 'mshrs_0.io.req.uop.ppred', 'mshrs_0.io.req.uop.ppred_busy', 'mshrs_0.io.req.uop.prs1', 'mshrs_0.io.req.uop.prs1_busy', 'mshrs_0.io.req.uop.prs2', 'mshrs_0.io.req.uop.prs2_busy', 'mshrs_0.io.req.uop.prs3', 'mshrs_0.io.req.uop.prs3_busy', 'mshrs_0.io.req.uop.rob_idx', 'mshrs_0.io.req.uop.rxq_idx', 'mshrs_0.io.req.uop.stale_pdst', 'mshrs_0.io.req.uop.stq_idx', 'mshrs_0.io.req.uop.taken', 'mshrs_0.io.req.uop.uses_ldq', 'mshrs_0.io.req.uop.uses_stq', 'mshrs_0.io.req.uop.xcpt_ae_if', 'mshrs_0.io.req.uop.xcpt_ma_if', 'mshrs_0.io.req.uop.xcpt_pf_if', 'mshrs_0.io.req.way_en', 'mshrs_0.io.req_is_probe', 'mshrs_0.io.req_pri_rdy', 'mshrs_0.io.req_pri_val', 'mshrs_0.io.req_sec_rdy', 'mshrs_0.io.req_sec_val', 'mshrs_0.io.rob_head_idx', 'mshrs_0.io.rob_pnr_idx', 'mshrs_0.io.tag.bits', 'mshrs_0.io.tag.valid', 'mshrs_0.io.way.bits', 'mshrs_0.io.way.valid', 'mshrs_0.io.wb_req.bits.tag', 'mshrs_0.io.wb_resp', 'mshrs_0.reset', 'mshrs_1.clock', 'mshrs_1.io.brupdate.b1.mispredict_mask', 'mshrs_1.io.brupdate.b1.resolve_mask', 'mshrs_1.io.brupdate.b2.cfi_type', 'mshrs_1.io.brupdate.b2.jalr_target', 'mshrs_1.io.brupdate.b2.mispredict', 'mshrs_1.io.brupdate.b2.pc_sel', 'mshrs_1.io.brupdate.b2.taken', 'mshrs_1.io.brupdate.b2.target_offset', 'mshrs_1.io.brupdate.b2.uop.bp_debug_if', 'mshrs_1.io.brupdate.b2.uop.bp_xcpt_if', 'mshrs_1.io.brupdate.b2.uop.br_mask', 'mshrs_1.io.brupdate.b2.uop.br_tag', 'mshrs_1.io.brupdate.b2.uop.br_type', 'mshrs_1.io.brupdate.b2.uop.csr_cmd', 'mshrs_1.io.brupdate.b2.uop.debug_fsrc', 'mshrs_1.io.brupdate.b2.uop.debug_inst', 'mshrs_1.io.brupdate.b2.uop.debug_pc', 'mshrs_1.io.brupdate.b2.uop.debug_tsrc', 'mshrs_1.io.brupdate.b2.uop.dis_col_sel', 'mshrs_1.io.brupdate.b2.uop.dst_rtype', 'mshrs_1.io.brupdate.b2.uop.edge_inst', 'mshrs_1.io.brupdate.b2.uop.exc_cause', 'mshrs_1.io.brupdate.b2.uop.exception', 'mshrs_1.io.brupdate.b2.uop.fcn_dw', 'mshrs_1.io.brupdate.b2.uop.fcn_op', 'mshrs_1.io.brupdate.b2.uop.flush_on_commit', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.div', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fma', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fromint', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ldst', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren1', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren2', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren3', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.sqrt', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap12', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap23', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.toint', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.vec', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.wen', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.wflags', 'mshrs_1.io.brupdate.b2.uop.fp_rm', 'mshrs_1.io.brupdate.b2.uop.fp_typ', 'mshrs_1.io.brupdate.b2.uop.fp_val', 'mshrs_1.io.brupdate.b2.uop.frs3_en', 'mshrs_1.io.brupdate.b2.uop.ftq_idx', 'mshrs_1.io.brupdate.b2.uop.fu_code[0]', 'mshrs_1.io.brupdate.b2.uop.fu_code[1]', 'mshrs_1.io.brupdate.b2.uop.fu_code[2]', 'mshrs_1.io.brupdate.b2.uop.fu_code[3]', 'mshrs_1.io.brupdate.b2.uop.fu_code[4]', 'mshrs_1.io.brupdate.b2.uop.fu_code[5]', 'mshrs_1.io.brupdate.b2.uop.fu_code[6]', 'mshrs_1.io.brupdate.b2.uop.fu_code[7]', 'mshrs_1.io.brupdate.b2.uop.fu_code[8]', 'mshrs_1.io.brupdate.b2.uop.fu_code[9]', 'mshrs_1.io.brupdate.b2.uop.imm_packed', 'mshrs_1.io.brupdate.b2.uop.imm_rename', 'mshrs_1.io.brupdate.b2.uop.imm_sel', 'mshrs_1.io.brupdate.b2.uop.inst', 'mshrs_1.io.brupdate.b2.uop.iq_type[0]', 'mshrs_1.io.brupdate.b2.uop.iq_type[1]', 'mshrs_1.io.brupdate.b2.uop.iq_type[2]', 'mshrs_1.io.brupdate.b2.uop.iq_type[3]', 'mshrs_1.io.brupdate.b2.uop.is_amo', 'mshrs_1.io.brupdate.b2.uop.is_eret', 'mshrs_1.io.brupdate.b2.uop.is_fence', 'mshrs_1.io.brupdate.b2.uop.is_fencei', 'mshrs_1.io.brupdate.b2.uop.is_mov', 'mshrs_1.io.brupdate.b2.uop.is_rocc', 'mshrs_1.io.brupdate.b2.uop.is_rvc', 'mshrs_1.io.brupdate.b2.uop.is_sfb', 'mshrs_1.io.brupdate.b2.uop.is_sfence', 'mshrs_1.io.brupdate.b2.uop.is_sys_pc2epc', 'mshrs_1.io.brupdate.b2.uop.is_unique', 'mshrs_1.io.brupdate.b2.uop.iw_issued', 'mshrs_1.io.brupdate.b2.uop.iw_issued_partial_agen', 'mshrs_1.io.brupdate.b2.uop.iw_issued_partial_dgen', 'mshrs_1.io.brupdate.b2.uop.iw_p1_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.iw_p1_speculative_child', 'mshrs_1.io.brupdate.b2.uop.iw_p2_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.iw_p2_speculative_child', 'mshrs_1.io.brupdate.b2.uop.iw_p3_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.ldq_idx', 'mshrs_1.io.brupdate.b2.uop.ldst', 'mshrs_1.io.brupdate.b2.uop.ldst_is_rs1', 'mshrs_1.io.brupdate.b2.uop.lrs1', 'mshrs_1.io.brupdate.b2.uop.lrs1_rtype', 'mshrs_1.io.brupdate.b2.uop.lrs2', 'mshrs_1.io.brupdate.b2.uop.lrs2_rtype', 'mshrs_1.io.brupdate.b2.uop.lrs3', 'mshrs_1.io.brupdate.b2.uop.mem_cmd', 'mshrs_1.io.brupdate.b2.uop.mem_signed', 'mshrs_1.io.brupdate.b2.uop.mem_size', 'mshrs_1.io.brupdate.b2.uop.op1_sel', 'mshrs_1.io.brupdate.b2.uop.op2_sel', 'mshrs_1.io.brupdate.b2.uop.pc_lob', 'mshrs_1.io.brupdate.b2.uop.pdst', 'mshrs_1.io.brupdate.b2.uop.pimm', 'mshrs_1.io.brupdate.b2.uop.ppred', 'mshrs_1.io.brupdate.b2.uop.ppred_busy', 'mshrs_1.io.brupdate.b2.uop.prs1', 'mshrs_1.io.brupdate.b2.uop.prs1_busy', 'mshrs_1.io.brupdate.b2.uop.prs2', 'mshrs_1.io.brupdate.b2.uop.prs2_busy', 'mshrs_1.io.brupdate.b2.uop.prs3', 'mshrs_1.io.brupdate.b2.uop.prs3_busy', 'mshrs_1.io.brupdate.b2.uop.rob_idx', 'mshrs_1.io.brupdate.b2.uop.rxq_idx', 'mshrs_1.io.brupdate.b2.uop.stale_pdst', 'mshrs_1.io.brupdate.b2.uop.stq_idx', 'mshrs_1.io.brupdate.b2.uop.taken', 'mshrs_1.io.brupdate.b2.uop.uses_ldq', 'mshrs_1.io.brupdate.b2.uop.uses_stq', 'mshrs_1.io.brupdate.b2.uop.xcpt_ae_if', 'mshrs_1.io.brupdate.b2.uop.xcpt_ma_if', 'mshrs_1.io.brupdate.b2.uop.xcpt_pf_if', 'mshrs_1.io.clear_prefetch', 'mshrs_1.io.commit_addr', 'mshrs_1.io.commit_val', 'mshrs_1.io.exception', 'mshrs_1.io.id', 'mshrs_1.io.idx.bits', 'mshrs_1.io.idx.valid', 'mshrs_1.io.lb_read.offset', 'mshrs_1.io.lb_resp', 'mshrs_1.io.lb_write.bits.data', 'mshrs_1.io.lb_write.bits.offset', 'mshrs_1.io.lb_write.valid', 'mshrs_1.io.mem_acquire.bits.address', 'mshrs_1.io.mem_acquire.bits.corrupt', 'mshrs_1.io.mem_acquire.bits.data', 'mshrs_1.io.mem_acquire.bits.mask', 'mshrs_1.io.mem_acquire.bits.opcode', 'mshrs_1.io.mem_acquire.bits.param', 'mshrs_1.io.mem_acquire.bits.size', 'mshrs_1.io.mem_acquire.bits.source', 'mshrs_1.io.mem_acquire.ready', 'mshrs_1.io.mem_acquire.valid', 'mshrs_1.io.mem_finish.bits.sink', 'mshrs_1.io.mem_finish.ready', 'mshrs_1.io.mem_finish.valid', 'mshrs_1.io.mem_grant.bits.corrupt', 'mshrs_1.io.mem_grant.bits.data', 'mshrs_1.io.mem_grant.bits.denied', 'mshrs_1.io.mem_grant.bits.opcode', 'mshrs_1.io.mem_grant.bits.param', 'mshrs_1.io.mem_grant.bits.sink', 'mshrs_1.io.mem_grant.bits.size', 'mshrs_1.io.mem_grant.bits.source', 'mshrs_1.io.mem_grant.ready', 'mshrs_1.io.mem_grant.valid', 'mshrs_1.io.meta_resp.bits.coh.state', 'mshrs_1.io.meta_resp.bits.tag', 'mshrs_1.io.meta_resp.valid', 'mshrs_1.io.probe_rdy', 'mshrs_1.io.prober_state.bits', 'mshrs_1.io.prober_state.valid', 'mshrs_1.io.req.addr', 'mshrs_1.io.req.data', 'mshrs_1.io.req.is_hella', 'mshrs_1.io.req.old_meta.coh.state', 'mshrs_1.io.req.old_meta.tag', 'mshrs_1.io.req.sdq_id', 'mshrs_1.io.req.tag_match', 'mshrs_1.io.req.uop.bp_debug_if', 'mshrs_1.io.req.uop.bp_xcpt_if', 'mshrs_1.io.req.uop.br_mask', 'mshrs_1.io.req.uop.br_tag', 'mshrs_1.io.req.uop.br_type', 'mshrs_1.io.req.uop.csr_cmd', 'mshrs_1.io.req.uop.debug_fsrc', 'mshrs_1.io.req.uop.debug_inst', 'mshrs_1.io.req.uop.debug_pc', 'mshrs_1.io.req.uop.debug_tsrc', 'mshrs_1.io.req.uop.dis_col_sel', 'mshrs_1.io.req.uop.dst_rtype', 'mshrs_1.io.req.uop.edge_inst', 'mshrs_1.io.req.uop.exc_cause', 'mshrs_1.io.req.uop.exception', 'mshrs_1.io.req.uop.fcn_dw', 'mshrs_1.io.req.uop.fcn_op', 'mshrs_1.io.req.uop.flush_on_commit', 'mshrs_1.io.req.uop.fp_ctrl.div', 'mshrs_1.io.req.uop.fp_ctrl.fastpipe', 'mshrs_1.io.req.uop.fp_ctrl.fma', 'mshrs_1.io.req.uop.fp_ctrl.fromint', 'mshrs_1.io.req.uop.fp_ctrl.ldst', 'mshrs_1.io.req.uop.fp_ctrl.ren1', 'mshrs_1.io.req.uop.fp_ctrl.ren2', 'mshrs_1.io.req.uop.fp_ctrl.ren3', 'mshrs_1.io.req.uop.fp_ctrl.sqrt', 'mshrs_1.io.req.uop.fp_ctrl.swap12', 'mshrs_1.io.req.uop.fp_ctrl.swap23', 'mshrs_1.io.req.uop.fp_ctrl.toint', 'mshrs_1.io.req.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.req.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.req.uop.fp_ctrl.vec', 'mshrs_1.io.req.uop.fp_ctrl.wen', 'mshrs_1.io.req.uop.fp_ctrl.wflags', 'mshrs_1.io.req.uop.fp_rm', 'mshrs_1.io.req.uop.fp_typ', 'mshrs_1.io.req.uop.fp_val', 'mshrs_1.io.req.uop.frs3_en', 'mshrs_1.io.req.uop.ftq_idx', 'mshrs_1.io.req.uop.fu_code[0]', 'mshrs_1.io.req.uop.fu_code[1]', 'mshrs_1.io.req.uop.fu_code[2]', 'mshrs_1.io.req.uop.fu_code[3]', 'mshrs_1.io.req.uop.fu_code[4]', 'mshrs_1.io.req.uop.fu_code[5]', 'mshrs_1.io.req.uop.fu_code[6]', 'mshrs_1.io.req.uop.fu_code[7]', 'mshrs_1.io.req.uop.fu_code[8]', 'mshrs_1.io.req.uop.fu_code[9]', 'mshrs_1.io.req.uop.imm_packed', 'mshrs_1.io.req.uop.imm_rename', 'mshrs_1.io.req.uop.imm_sel', 'mshrs_1.io.req.uop.inst', 'mshrs_1.io.req.uop.iq_type[0]', 'mshrs_1.io.req.uop.iq_type[1]', 'mshrs_1.io.req.uop.iq_type[2]', 'mshrs_1.io.req.uop.iq_type[3]', 'mshrs_1.io.req.uop.is_amo', 'mshrs_1.io.req.uop.is_eret', 'mshrs_1.io.req.uop.is_fence', 'mshrs_1.io.req.uop.is_fencei', 'mshrs_1.io.req.uop.is_mov', 'mshrs_1.io.req.uop.is_rocc', 'mshrs_1.io.req.uop.is_rvc', 'mshrs_1.io.req.uop.is_sfb', 'mshrs_1.io.req.uop.is_sfence', 'mshrs_1.io.req.uop.is_sys_pc2epc', 'mshrs_1.io.req.uop.is_unique', 'mshrs_1.io.req.uop.iw_issued', 'mshrs_1.io.req.uop.iw_issued_partial_agen', 'mshrs_1.io.req.uop.iw_issued_partial_dgen', 'mshrs_1.io.req.uop.iw_p1_bypass_hint', 'mshrs_1.io.req.uop.iw_p1_speculative_child', 'mshrs_1.io.req.uop.iw_p2_bypass_hint', 'mshrs_1.io.req.uop.iw_p2_speculative_child', 'mshrs_1.io.req.uop.iw_p3_bypass_hint', 'mshrs_1.io.req.uop.ldq_idx', 'mshrs_1.io.req.uop.ldst', 'mshrs_1.io.req.uop.ldst_is_rs1', 'mshrs_1.io.req.uop.lrs1', 'mshrs_1.io.req.uop.lrs1_rtype', 'mshrs_1.io.req.uop.lrs2', 'mshrs_1.io.req.uop.lrs2_rtype', 'mshrs_1.io.req.uop.lrs3', 'mshrs_1.io.req.uop.mem_cmd', 'mshrs_1.io.req.uop.mem_signed', 'mshrs_1.io.req.uop.mem_size', 'mshrs_1.io.req.uop.op1_sel', 'mshrs_1.io.req.uop.op2_sel', 'mshrs_1.io.req.uop.pc_lob', 'mshrs_1.io.req.uop.pdst', 'mshrs_1.io.req.uop.pimm', 'mshrs_1.io.req.uop.ppred', 'mshrs_1.io.req.uop.ppred_busy', 'mshrs_1.io.req.uop.prs1', 'mshrs_1.io.req.uop.prs1_busy', 'mshrs_1.io.req.uop.prs2', 'mshrs_1.io.req.uop.prs2_busy', 'mshrs_1.io.req.uop.prs3', 'mshrs_1.io.req.uop.prs3_busy', 'mshrs_1.io.req.uop.rob_idx', 'mshrs_1.io.req.uop.rxq_idx', 'mshrs_1.io.req.uop.stale_pdst', 'mshrs_1.io.req.uop.stq_idx', 'mshrs_1.io.req.uop.taken', 'mshrs_1.io.req.uop.uses_ldq', 'mshrs_1.io.req.uop.uses_stq', 'mshrs_1.io.req.uop.xcpt_ae_if', 'mshrs_1.io.req.uop.xcpt_ma_if', 'mshrs_1.io.req.uop.xcpt_pf_if', 'mshrs_1.io.req.way_en', 'mshrs_1.io.req_is_probe', 'mshrs_1.io.req_pri_rdy', 'mshrs_1.io.req_pri_val', 'mshrs_1.io.req_sec_rdy', 'mshrs_1.io.req_sec_val', 'mshrs_1.io.rob_head_idx', 'mshrs_1.io.rob_pnr_idx', 'mshrs_1.io.tag.bits', 'mshrs_1.io.tag.valid', 'mshrs_1.io.way.bits', 'mshrs_1.io.way.valid', 'mshrs_1.io.wb_req.bits.tag', 'mshrs_1.io.wb_resp', 'mshrs_1.reset', 'prefetcher.clock', 'prefetcher.io.mshr_avail', 'prefetcher.io.prefetch.ready', 'prefetcher.io.prefetch.valid', 'prefetcher.io.req_addr', 'prefetcher.io.req_coh.state', 'prefetcher.io.req_val', 'prefetcher.reset', 'refill_arb.clock', 'refill_arb.io.in[0].bits.addr', 'refill_arb.io.in[0].bits.data', 'refill_arb.io.in[0].bits.way_en', 'refill_arb.io.in[0].bits.wmask', 'refill_arb.io.in[0].ready', 'refill_arb.io.in[0].valid', 'refill_arb.io.in[1].bits.addr', 'refill_arb.io.in[1].bits.data', 'refill_arb.io.in[1].bits.way_en', 'refill_arb.io.in[1].bits.wmask', 'refill_arb.io.in[1].ready', 'refill_arb.io.in[1].valid', 'refill_arb.io.out.ready', 'refill_arb.io.out.valid', 'refill_arb.reset', 'replay_arb.clock', 'replay_arb.io.in[0].bits.addr', 'replay_arb.io.in[0].bits.data', 'replay_arb.io.in[0].bits.is_hella', 'replay_arb.io.in[0].bits.old_meta.coh.state', 'replay_arb.io.in[0].bits.old_meta.tag', 'replay_arb.io.in[0].bits.sdq_id', 'replay_arb.io.in[0].bits.tag_match', 'replay_arb.io.in[0].bits.uop.bp_debug_if', 'replay_arb.io.in[0].bits.uop.bp_xcpt_if', 'replay_arb.io.in[0].bits.uop.br_mask', 'replay_arb.io.in[0].bits.uop.br_tag', 'replay_arb.io.in[0].bits.uop.br_type', 'replay_arb.io.in[0].bits.uop.csr_cmd', 'replay_arb.io.in[0].bits.uop.debug_fsrc', 'replay_arb.io.in[0].bits.uop.debug_inst', 'replay_arb.io.in[0].bits.uop.debug_pc', 'replay_arb.io.in[0].bits.uop.debug_tsrc', 'replay_arb.io.in[0].bits.uop.dis_col_sel', 'replay_arb.io.in[0].bits.uop.dst_rtype', 'replay_arb.io.in[0].bits.uop.edge_inst', 'replay_arb.io.in[0].bits.uop.exc_cause', 'replay_arb.io.in[0].bits.uop.exception', 'replay_arb.io.in[0].bits.uop.fcn_dw', 'replay_arb.io.in[0].bits.uop.fcn_op', 'replay_arb.io.in[0].bits.uop.flush_on_commit', 'replay_arb.io.in[0].bits.uop.fp_ctrl.div', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fastpipe', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fma', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fromint', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ldst', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren1', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren2', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren3', 'replay_arb.io.in[0].bits.uop.fp_ctrl.sqrt', 'replay_arb.io.in[0].bits.uop.fp_ctrl.swap12', 'replay_arb.io.in[0].bits.uop.fp_ctrl.swap23', 'replay_arb.io.in[0].bits.uop.fp_ctrl.toint', 'replay_arb.io.in[0].bits.uop.fp_ctrl.typeTagIn', 'replay_arb.io.in[0].bits.uop.fp_ctrl.typeTagOut', 'replay_arb.io.in[0].bits.uop.fp_ctrl.vec', 'replay_arb.io.in[0].bits.uop.fp_ctrl.wen', 'replay_arb.io.in[0].bits.uop.fp_ctrl.wflags', 'replay_arb.io.in[0].bits.uop.fp_rm', 'replay_arb.io.in[0].bits.uop.fp_typ', 'replay_arb.io.in[0].bits.uop.fp_val', 'replay_arb.io.in[0].bits.uop.frs3_en', 'replay_arb.io.in[0].bits.uop.ftq_idx', 'replay_arb.io.in[0].bits.uop.fu_code[0]', 'replay_arb.io.in[0].bits.uop.fu_code[1]', 'replay_arb.io.in[0].bits.uop.fu_code[2]', 'replay_arb.io.in[0].bits.uop.fu_code[3]', 'replay_arb.io.in[0].bits.uop.fu_code[4]', 'replay_arb.io.in[0].bits.uop.fu_code[5]', 'replay_arb.io.in[0].bits.uop.fu_code[6]', 'replay_arb.io.in[0].bits.uop.fu_code[7]', 'replay_arb.io.in[0].bits.uop.fu_code[8]', 'replay_arb.io.in[0].bits.uop.fu_code[9]', 'replay_arb.io.in[0].bits.uop.imm_packed', 'replay_arb.io.in[0].bits.uop.imm_rename', 'replay_arb.io.in[0].bits.uop.imm_sel', 'replay_arb.io.in[0].bits.uop.inst', 'replay_arb.io.in[0].bits.uop.iq_type[0]', 'replay_arb.io.in[0].bits.uop.iq_type[1]', 'replay_arb.io.in[0].bits.uop.iq_type[2]', 'replay_arb.io.in[0].bits.uop.iq_type[3]', 'replay_arb.io.in[0].bits.uop.is_amo', 'replay_arb.io.in[0].bits.uop.is_eret', 'replay_arb.io.in[0].bits.uop.is_fence', 'replay_arb.io.in[0].bits.uop.is_fencei', 'replay_arb.io.in[0].bits.uop.is_mov', 'replay_arb.io.in[0].bits.uop.is_rocc', 'replay_arb.io.in[0].bits.uop.is_rvc', 'replay_arb.io.in[0].bits.uop.is_sfb', 'replay_arb.io.in[0].bits.uop.is_sfence', 'replay_arb.io.in[0].bits.uop.is_sys_pc2epc', 'replay_arb.io.in[0].bits.uop.is_unique', 'replay_arb.io.in[0].bits.uop.iw_issued', 'replay_arb.io.in[0].bits.uop.iw_issued_partial_agen', 'replay_arb.io.in[0].bits.uop.iw_issued_partial_dgen', 'replay_arb.io.in[0].bits.uop.iw_p1_bypass_hint', 'replay_arb.io.in[0].bits.uop.iw_p1_speculative_child', 'replay_arb.io.in[0].bits.uop.iw_p2_bypass_hint', 'replay_arb.io.in[0].bits.uop.iw_p2_speculative_child', 'replay_arb.io.in[0].bits.uop.iw_p3_bypass_hint', 'replay_arb.io.in[0].bits.uop.ldq_idx', 'replay_arb.io.in[0].bits.uop.ldst', 'replay_arb.io.in[0].bits.uop.ldst_is_rs1', 'replay_arb.io.in[0].bits.uop.lrs1', 'replay_arb.io.in[0].bits.uop.lrs1_rtype', 'replay_arb.io.in[0].bits.uop.lrs2', 'replay_arb.io.in[0].bits.uop.lrs2_rtype', 'replay_arb.io.in[0].bits.uop.lrs3', 'replay_arb.io.in[0].bits.uop.mem_cmd', 'replay_arb.io.in[0].bits.uop.mem_signed', 'replay_arb.io.in[0].bits.uop.mem_size', 'replay_arb.io.in[0].bits.uop.op1_sel', 'replay_arb.io.in[0].bits.uop.op2_sel', 'replay_arb.io.in[0].bits.uop.pc_lob', 'replay_arb.io.in[0].bits.uop.pdst', 'replay_arb.io.in[0].bits.uop.pimm', 'replay_arb.io.in[0].bits.uop.ppred', 'replay_arb.io.in[0].bits.uop.ppred_busy', 'replay_arb.io.in[0].bits.uop.prs1', 'replay_arb.io.in[0].bits.uop.prs1_busy', 'replay_arb.io.in[0].bits.uop.prs2', 'replay_arb.io.in[0].bits.uop.prs2_busy', 'replay_arb.io.in[0].bits.uop.prs3', 'replay_arb.io.in[0].bits.uop.prs3_busy', 'replay_arb.io.in[0].bits.uop.rob_idx', 'replay_arb.io.in[0].bits.uop.rxq_idx', 'replay_arb.io.in[0].bits.uop.stale_pdst', 'replay_arb.io.in[0].bits.uop.stq_idx', 'replay_arb.io.in[0].bits.uop.taken', 'replay_arb.io.in[0].bits.uop.uses_ldq', 'replay_arb.io.in[0].bits.uop.uses_stq', 'replay_arb.io.in[0].bits.uop.xcpt_ae_if', 'replay_arb.io.in[0].bits.uop.xcpt_ma_if', 'replay_arb.io.in[0].bits.uop.xcpt_pf_if', 'replay_arb.io.in[0].bits.way_en', 'replay_arb.io.in[0].ready', 'replay_arb.io.in[0].valid', 'replay_arb.io.in[1].bits.addr', 'replay_arb.io.in[1].bits.data', 'replay_arb.io.in[1].bits.is_hella', 'replay_arb.io.in[1].bits.old_meta.coh.state', 'replay_arb.io.in[1].bits.old_meta.tag', 'replay_arb.io.in[1].bits.sdq_id', 'replay_arb.io.in[1].bits.tag_match', 'replay_arb.io.in[1].bits.uop.bp_debug_if', 'replay_arb.io.in[1].bits.uop.bp_xcpt_if', 'replay_arb.io.in[1].bits.uop.br_mask', 'replay_arb.io.in[1].bits.uop.br_tag', 'replay_arb.io.in[1].bits.uop.br_type', 'replay_arb.io.in[1].bits.uop.csr_cmd', 'replay_arb.io.in[1].bits.uop.debug_fsrc', 'replay_arb.io.in[1].bits.uop.debug_inst', 'replay_arb.io.in[1].bits.uop.debug_pc', 'replay_arb.io.in[1].bits.uop.debug_tsrc', 'replay_arb.io.in[1].bits.uop.dis_col_sel', 'replay_arb.io.in[1].bits.uop.dst_rtype', 'replay_arb.io.in[1].bits.uop.edge_inst', 'replay_arb.io.in[1].bits.uop.exc_cause', 'replay_arb.io.in[1].bits.uop.exception', 'replay_arb.io.in[1].bits.uop.fcn_dw', 'replay_arb.io.in[1].bits.uop.fcn_op', 'replay_arb.io.in[1].bits.uop.flush_on_commit', 'replay_arb.io.in[1].bits.uop.fp_ctrl.div', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fastpipe', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fma', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fromint', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ldst', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren1', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren2', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren3', 'replay_arb.io.in[1].bits.uop.fp_ctrl.sqrt', 'replay_arb.io.in[1].bits.uop.fp_ctrl.swap12', 'replay_arb.io.in[1].bits.uop.fp_ctrl.swap23', 'replay_arb.io.in[1].bits.uop.fp_ctrl.toint', 'replay_arb.io.in[1].bits.uop.fp_ctrl.typeTagIn', 'replay_arb.io.in[1].bits.uop.fp_ctrl.typeTagOut', 'replay_arb.io.in[1].bits.uop.fp_ctrl.vec', 'replay_arb.io.in[1].bits.uop.fp_ctrl.wen', 'replay_arb.io.in[1].bits.uop.fp_ctrl.wflags', 'replay_arb.io.in[1].bits.uop.fp_rm', 'replay_arb.io.in[1].bits.uop.fp_typ', 'replay_arb.io.in[1].bits.uop.fp_val', 'replay_arb.io.in[1].bits.uop.frs3_en', 'replay_arb.io.in[1].bits.uop.ftq_idx', 'replay_arb.io.in[1].bits.uop.fu_code[0]', 'replay_arb.io.in[1].bits.uop.fu_code[1]', 'replay_arb.io.in[1].bits.uop.fu_code[2]', 'replay_arb.io.in[1].bits.uop.fu_code[3]', 'replay_arb.io.in[1].bits.uop.fu_code[4]', 'replay_arb.io.in[1].bits.uop.fu_code[5]', 'replay_arb.io.in[1].bits.uop.fu_code[6]', 'replay_arb.io.in[1].bits.uop.fu_code[7]', 'replay_arb.io.in[1].bits.uop.fu_code[8]', 'replay_arb.io.in[1].bits.uop.fu_code[9]', 'replay_arb.io.in[1].bits.uop.imm_packed', 'replay_arb.io.in[1].bits.uop.imm_rename', 'replay_arb.io.in[1].bits.uop.imm_sel', 'replay_arb.io.in[1].bits.uop.inst', 'replay_arb.io.in[1].bits.uop.iq_type[0]', 'replay_arb.io.in[1].bits.uop.iq_type[1]', 'replay_arb.io.in[1].bits.uop.iq_type[2]', 'replay_arb.io.in[1].bits.uop.iq_type[3]', 'replay_arb.io.in[1].bits.uop.is_amo', 'replay_arb.io.in[1].bits.uop.is_eret', 'replay_arb.io.in[1].bits.uop.is_fence', 'replay_arb.io.in[1].bits.uop.is_fencei', 'replay_arb.io.in[1].bits.uop.is_mov', 'replay_arb.io.in[1].bits.uop.is_rocc', 'replay_arb.io.in[1].bits.uop.is_rvc', 'replay_arb.io.in[1].bits.uop.is_sfb', 'replay_arb.io.in[1].bits.uop.is_sfence', 'replay_arb.io.in[1].bits.uop.is_sys_pc2epc', 'replay_arb.io.in[1].bits.uop.is_unique', 'replay_arb.io.in[1].bits.uop.iw_issued', 'replay_arb.io.in[1].bits.uop.iw_issued_partial_agen', 'replay_arb.io.in[1].bits.uop.iw_issued_partial_dgen', 'replay_arb.io.in[1].bits.uop.iw_p1_bypass_hint', 'replay_arb.io.in[1].bits.uop.iw_p1_speculative_child', 'replay_arb.io.in[1].bits.uop.iw_p2_bypass_hint', 'replay_arb.io.in[1].bits.uop.iw_p2_speculative_child', 'replay_arb.io.in[1].bits.uop.iw_p3_bypass_hint', 'replay_arb.io.in[1].bits.uop.ldq_idx', 'replay_arb.io.in[1].bits.uop.ldst', 'replay_arb.io.in[1].bits.uop.ldst_is_rs1', 'replay_arb.io.in[1].bits.uop.lrs1', 'replay_arb.io.in[1].bits.uop.lrs1_rtype', 'replay_arb.io.in[1].bits.uop.lrs2', 'replay_arb.io.in[1].bits.uop.lrs2_rtype', 'replay_arb.io.in[1].bits.uop.lrs3', 'replay_arb.io.in[1].bits.uop.mem_cmd', 'replay_arb.io.in[1].bits.uop.mem_signed', 'replay_arb.io.in[1].bits.uop.mem_size', 'replay_arb.io.in[1].bits.uop.op1_sel', 'replay_arb.io.in[1].bits.uop.op2_sel', 'replay_arb.io.in[1].bits.uop.pc_lob', 'replay_arb.io.in[1].bits.uop.pdst', 'replay_arb.io.in[1].bits.uop.pimm', 'replay_arb.io.in[1].bits.uop.ppred', 'replay_arb.io.in[1].bits.uop.ppred_busy', 'replay_arb.io.in[1].bits.uop.prs1', 'replay_arb.io.in[1].bits.uop.prs1_busy', 'replay_arb.io.in[1].bits.uop.prs2', 'replay_arb.io.in[1].bits.uop.prs2_busy', 'replay_arb.io.in[1].bits.uop.prs3', 'replay_arb.io.in[1].bits.uop.prs3_busy', 'replay_arb.io.in[1].bits.uop.rob_idx', 'replay_arb.io.in[1].bits.uop.rxq_idx', 'replay_arb.io.in[1].bits.uop.stale_pdst', 'replay_arb.io.in[1].bits.uop.stq_idx', 'replay_arb.io.in[1].bits.uop.taken', 'replay_arb.io.in[1].bits.uop.uses_ldq', 'replay_arb.io.in[1].bits.uop.uses_stq', 'replay_arb.io.in[1].bits.uop.xcpt_ae_if', 'replay_arb.io.in[1].bits.uop.xcpt_ma_if', 'replay_arb.io.in[1].bits.uop.xcpt_pf_if', 'replay_arb.io.in[1].bits.way_en', 'replay_arb.io.in[1].ready', 'replay_arb.io.in[1].valid', 'replay_arb.io.out.bits.sdq_id', 'replay_arb.io.out.ready', 'replay_arb.io.out.valid', 'replay_arb.reset', 'resp_arb.clock', 'resp_arb.io.in[0].bits.data', 'resp_arb.io.in[0].bits.is_hella', 'resp_arb.io.in[0].bits.uop.bp_debug_if', 'resp_arb.io.in[0].bits.uop.bp_xcpt_if', 'resp_arb.io.in[0].bits.uop.br_mask', 'resp_arb.io.in[0].bits.uop.br_tag', 'resp_arb.io.in[0].bits.uop.br_type', 'resp_arb.io.in[0].bits.uop.csr_cmd', 'resp_arb.io.in[0].bits.uop.debug_fsrc', 'resp_arb.io.in[0].bits.uop.debug_inst', 'resp_arb.io.in[0].bits.uop.debug_pc', 'resp_arb.io.in[0].bits.uop.debug_tsrc', 'resp_arb.io.in[0].bits.uop.dis_col_sel', 'resp_arb.io.in[0].bits.uop.dst_rtype', 'resp_arb.io.in[0].bits.uop.edge_inst', 'resp_arb.io.in[0].bits.uop.exc_cause', 'resp_arb.io.in[0].bits.uop.exception', 'resp_arb.io.in[0].bits.uop.fcn_dw', 'resp_arb.io.in[0].bits.uop.fcn_op', 'resp_arb.io.in[0].bits.uop.flush_on_commit', 'resp_arb.io.in[0].bits.uop.fp_ctrl.div', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[0].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[0].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[0].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[0].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[0].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[0].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[0].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[0].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[0].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[0].bits.uop.fp_rm', 'resp_arb.io.in[0].bits.uop.fp_typ', 'resp_arb.io.in[0].bits.uop.fp_val', 'resp_arb.io.in[0].bits.uop.frs3_en', 'resp_arb.io.in[0].bits.uop.ftq_idx', 'resp_arb.io.in[0].bits.uop.fu_code[0]', 'resp_arb.io.in[0].bits.uop.fu_code[1]', 'resp_arb.io.in[0].bits.uop.fu_code[2]', 'resp_arb.io.in[0].bits.uop.fu_code[3]', 'resp_arb.io.in[0].bits.uop.fu_code[4]', 'resp_arb.io.in[0].bits.uop.fu_code[5]', 'resp_arb.io.in[0].bits.uop.fu_code[6]', 'resp_arb.io.in[0].bits.uop.fu_code[7]', 'resp_arb.io.in[0].bits.uop.fu_code[8]', 'resp_arb.io.in[0].bits.uop.fu_code[9]', 'resp_arb.io.in[0].bits.uop.imm_packed', 'resp_arb.io.in[0].bits.uop.imm_rename', 'resp_arb.io.in[0].bits.uop.imm_sel', 'resp_arb.io.in[0].bits.uop.inst', 'resp_arb.io.in[0].bits.uop.iq_type[0]', 'resp_arb.io.in[0].bits.uop.iq_type[1]', 'resp_arb.io.in[0].bits.uop.iq_type[2]', 'resp_arb.io.in[0].bits.uop.iq_type[3]', 'resp_arb.io.in[0].bits.uop.is_amo', 'resp_arb.io.in[0].bits.uop.is_eret', 'resp_arb.io.in[0].bits.uop.is_fence', 'resp_arb.io.in[0].bits.uop.is_fencei', 'resp_arb.io.in[0].bits.uop.is_mov', 'resp_arb.io.in[0].bits.uop.is_rocc', 'resp_arb.io.in[0].bits.uop.is_rvc', 'resp_arb.io.in[0].bits.uop.is_sfb', 'resp_arb.io.in[0].bits.uop.is_sfence', 'resp_arb.io.in[0].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[0].bits.uop.is_unique', 'resp_arb.io.in[0].bits.uop.iw_issued', 'resp_arb.io.in[0].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[0].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[0].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[0].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[0].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[0].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[0].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[0].bits.uop.ldq_idx', 'resp_arb.io.in[0].bits.uop.ldst', 'resp_arb.io.in[0].bits.uop.ldst_is_rs1', 'resp_arb.io.in[0].bits.uop.lrs1', 'resp_arb.io.in[0].bits.uop.lrs1_rtype', 'resp_arb.io.in[0].bits.uop.lrs2', 'resp_arb.io.in[0].bits.uop.lrs2_rtype', 'resp_arb.io.in[0].bits.uop.lrs3', 'resp_arb.io.in[0].bits.uop.mem_cmd', 'resp_arb.io.in[0].bits.uop.mem_signed', 'resp_arb.io.in[0].bits.uop.mem_size', 'resp_arb.io.in[0].bits.uop.op1_sel', 'resp_arb.io.in[0].bits.uop.op2_sel', 'resp_arb.io.in[0].bits.uop.pc_lob', 'resp_arb.io.in[0].bits.uop.pdst', 'resp_arb.io.in[0].bits.uop.pimm', 'resp_arb.io.in[0].bits.uop.ppred', 'resp_arb.io.in[0].bits.uop.ppred_busy', 'resp_arb.io.in[0].bits.uop.prs1', 'resp_arb.io.in[0].bits.uop.prs1_busy', 'resp_arb.io.in[0].bits.uop.prs2', 'resp_arb.io.in[0].bits.uop.prs2_busy', 'resp_arb.io.in[0].bits.uop.prs3', 'resp_arb.io.in[0].bits.uop.prs3_busy', 'resp_arb.io.in[0].bits.uop.rob_idx', 'resp_arb.io.in[0].bits.uop.rxq_idx', 'resp_arb.io.in[0].bits.uop.stale_pdst', 'resp_arb.io.in[0].bits.uop.stq_idx', 'resp_arb.io.in[0].bits.uop.taken', 'resp_arb.io.in[0].bits.uop.uses_ldq', 'resp_arb.io.in[0].bits.uop.uses_stq', 'resp_arb.io.in[0].bits.uop.xcpt_ae_if', 'resp_arb.io.in[0].bits.uop.xcpt_ma_if', 'resp_arb.io.in[0].bits.uop.xcpt_pf_if', 'resp_arb.io.in[0].ready', 'resp_arb.io.in[0].valid', 'resp_arb.io.in[1].bits.data', 'resp_arb.io.in[1].bits.is_hella', 'resp_arb.io.in[1].bits.uop.bp_debug_if', 'resp_arb.io.in[1].bits.uop.bp_xcpt_if', 'resp_arb.io.in[1].bits.uop.br_mask', 'resp_arb.io.in[1].bits.uop.br_tag', 'resp_arb.io.in[1].bits.uop.br_type', 'resp_arb.io.in[1].bits.uop.csr_cmd', 'resp_arb.io.in[1].bits.uop.debug_fsrc', 'resp_arb.io.in[1].bits.uop.debug_inst', 'resp_arb.io.in[1].bits.uop.debug_pc', 'resp_arb.io.in[1].bits.uop.debug_tsrc', 'resp_arb.io.in[1].bits.uop.dis_col_sel', 'resp_arb.io.in[1].bits.uop.dst_rtype', 'resp_arb.io.in[1].bits.uop.edge_inst', 'resp_arb.io.in[1].bits.uop.exc_cause', 'resp_arb.io.in[1].bits.uop.exception', 'resp_arb.io.in[1].bits.uop.fcn_dw', 'resp_arb.io.in[1].bits.uop.fcn_op', 'resp_arb.io.in[1].bits.uop.flush_on_commit', 'resp_arb.io.in[1].bits.uop.fp_ctrl.div', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[1].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[1].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[1].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[1].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[1].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[1].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[1].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[1].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[1].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[1].bits.uop.fp_rm', 'resp_arb.io.in[1].bits.uop.fp_typ', 'resp_arb.io.in[1].bits.uop.fp_val', 'resp_arb.io.in[1].bits.uop.frs3_en', 'resp_arb.io.in[1].bits.uop.ftq_idx', 'resp_arb.io.in[1].bits.uop.fu_code[0]', 'resp_arb.io.in[1].bits.uop.fu_code[1]', 'resp_arb.io.in[1].bits.uop.fu_code[2]', 'resp_arb.io.in[1].bits.uop.fu_code[3]', 'resp_arb.io.in[1].bits.uop.fu_code[4]', 'resp_arb.io.in[1].bits.uop.fu_code[5]', 'resp_arb.io.in[1].bits.uop.fu_code[6]', 'resp_arb.io.in[1].bits.uop.fu_code[7]', 'resp_arb.io.in[1].bits.uop.fu_code[8]', 'resp_arb.io.in[1].bits.uop.fu_code[9]', 'resp_arb.io.in[1].bits.uop.imm_packed', 'resp_arb.io.in[1].bits.uop.imm_rename', 'resp_arb.io.in[1].bits.uop.imm_sel', 'resp_arb.io.in[1].bits.uop.inst', 'resp_arb.io.in[1].bits.uop.iq_type[0]', 'resp_arb.io.in[1].bits.uop.iq_type[1]', 'resp_arb.io.in[1].bits.uop.iq_type[2]', 'resp_arb.io.in[1].bits.uop.iq_type[3]', 'resp_arb.io.in[1].bits.uop.is_amo', 'resp_arb.io.in[1].bits.uop.is_eret', 'resp_arb.io.in[1].bits.uop.is_fence', 'resp_arb.io.in[1].bits.uop.is_fencei', 'resp_arb.io.in[1].bits.uop.is_mov', 'resp_arb.io.in[1].bits.uop.is_rocc', 'resp_arb.io.in[1].bits.uop.is_rvc', 'resp_arb.io.in[1].bits.uop.is_sfb', 'resp_arb.io.in[1].bits.uop.is_sfence', 'resp_arb.io.in[1].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[1].bits.uop.is_unique', 'resp_arb.io.in[1].bits.uop.iw_issued', 'resp_arb.io.in[1].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[1].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[1].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[1].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[1].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[1].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[1].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[1].bits.uop.ldq_idx', 'resp_arb.io.in[1].bits.uop.ldst', 'resp_arb.io.in[1].bits.uop.ldst_is_rs1', 'resp_arb.io.in[1].bits.uop.lrs1', 'resp_arb.io.in[1].bits.uop.lrs1_rtype', 'resp_arb.io.in[1].bits.uop.lrs2', 'resp_arb.io.in[1].bits.uop.lrs2_rtype', 'resp_arb.io.in[1].bits.uop.lrs3', 'resp_arb.io.in[1].bits.uop.mem_cmd', 'resp_arb.io.in[1].bits.uop.mem_signed', 'resp_arb.io.in[1].bits.uop.mem_size', 'resp_arb.io.in[1].bits.uop.op1_sel', 'resp_arb.io.in[1].bits.uop.op2_sel', 'resp_arb.io.in[1].bits.uop.pc_lob', 'resp_arb.io.in[1].bits.uop.pdst', 'resp_arb.io.in[1].bits.uop.pimm', 'resp_arb.io.in[1].bits.uop.ppred', 'resp_arb.io.in[1].bits.uop.ppred_busy', 'resp_arb.io.in[1].bits.uop.prs1', 'resp_arb.io.in[1].bits.uop.prs1_busy', 'resp_arb.io.in[1].bits.uop.prs2', 'resp_arb.io.in[1].bits.uop.prs2_busy', 'resp_arb.io.in[1].bits.uop.prs3', 'resp_arb.io.in[1].bits.uop.prs3_busy', 'resp_arb.io.in[1].bits.uop.rob_idx', 'resp_arb.io.in[1].bits.uop.rxq_idx', 'resp_arb.io.in[1].bits.uop.stale_pdst', 'resp_arb.io.in[1].bits.uop.stq_idx', 'resp_arb.io.in[1].bits.uop.taken', 'resp_arb.io.in[1].bits.uop.uses_ldq', 'resp_arb.io.in[1].bits.uop.uses_stq', 'resp_arb.io.in[1].bits.uop.xcpt_ae_if', 'resp_arb.io.in[1].bits.uop.xcpt_ma_if', 'resp_arb.io.in[1].bits.uop.xcpt_pf_if', 'resp_arb.io.in[1].ready', 'resp_arb.io.in[1].valid', 'resp_arb.io.in[2].bits.data', 'resp_arb.io.in[2].bits.is_hella', 'resp_arb.io.in[2].bits.uop.bp_debug_if', 'resp_arb.io.in[2].bits.uop.bp_xcpt_if', 'resp_arb.io.in[2].bits.uop.br_mask', 'resp_arb.io.in[2].bits.uop.br_tag', 'resp_arb.io.in[2].bits.uop.br_type', 'resp_arb.io.in[2].bits.uop.csr_cmd', 'resp_arb.io.in[2].bits.uop.debug_fsrc', 'resp_arb.io.in[2].bits.uop.debug_inst', 'resp_arb.io.in[2].bits.uop.debug_pc', 'resp_arb.io.in[2].bits.uop.debug_tsrc', 'resp_arb.io.in[2].bits.uop.dis_col_sel', 'resp_arb.io.in[2].bits.uop.dst_rtype', 'resp_arb.io.in[2].bits.uop.edge_inst', 'resp_arb.io.in[2].bits.uop.exc_cause', 'resp_arb.io.in[2].bits.uop.exception', 'resp_arb.io.in[2].bits.uop.fcn_dw', 'resp_arb.io.in[2].bits.uop.fcn_op', 'resp_arb.io.in[2].bits.uop.flush_on_commit', 'resp_arb.io.in[2].bits.uop.fp_ctrl.div', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[2].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[2].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[2].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[2].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[2].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[2].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[2].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[2].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[2].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[2].bits.uop.fp_rm', 'resp_arb.io.in[2].bits.uop.fp_typ', 'resp_arb.io.in[2].bits.uop.fp_val', 'resp_arb.io.in[2].bits.uop.frs3_en', 'resp_arb.io.in[2].bits.uop.ftq_idx', 'resp_arb.io.in[2].bits.uop.fu_code[0]', 'resp_arb.io.in[2].bits.uop.fu_code[1]', 'resp_arb.io.in[2].bits.uop.fu_code[2]', 'resp_arb.io.in[2].bits.uop.fu_code[3]', 'resp_arb.io.in[2].bits.uop.fu_code[4]', 'resp_arb.io.in[2].bits.uop.fu_code[5]', 'resp_arb.io.in[2].bits.uop.fu_code[6]', 'resp_arb.io.in[2].bits.uop.fu_code[7]', 'resp_arb.io.in[2].bits.uop.fu_code[8]', 'resp_arb.io.in[2].bits.uop.fu_code[9]', 'resp_arb.io.in[2].bits.uop.imm_packed', 'resp_arb.io.in[2].bits.uop.imm_rename', 'resp_arb.io.in[2].bits.uop.imm_sel', 'resp_arb.io.in[2].bits.uop.inst', 'resp_arb.io.in[2].bits.uop.iq_type[0]', 'resp_arb.io.in[2].bits.uop.iq_type[1]', 'resp_arb.io.in[2].bits.uop.iq_type[2]', 'resp_arb.io.in[2].bits.uop.iq_type[3]', 'resp_arb.io.in[2].bits.uop.is_amo', 'resp_arb.io.in[2].bits.uop.is_eret', 'resp_arb.io.in[2].bits.uop.is_fence', 'resp_arb.io.in[2].bits.uop.is_fencei', 'resp_arb.io.in[2].bits.uop.is_mov', 'resp_arb.io.in[2].bits.uop.is_rocc', 'resp_arb.io.in[2].bits.uop.is_rvc', 'resp_arb.io.in[2].bits.uop.is_sfb', 'resp_arb.io.in[2].bits.uop.is_sfence', 'resp_arb.io.in[2].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[2].bits.uop.is_unique', 'resp_arb.io.in[2].bits.uop.iw_issued', 'resp_arb.io.in[2].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[2].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[2].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[2].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[2].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[2].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[2].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[2].bits.uop.ldq_idx', 'resp_arb.io.in[2].bits.uop.ldst', 'resp_arb.io.in[2].bits.uop.ldst_is_rs1', 'resp_arb.io.in[2].bits.uop.lrs1', 'resp_arb.io.in[2].bits.uop.lrs1_rtype', 'resp_arb.io.in[2].bits.uop.lrs2', 'resp_arb.io.in[2].bits.uop.lrs2_rtype', 'resp_arb.io.in[2].bits.uop.lrs3', 'resp_arb.io.in[2].bits.uop.mem_cmd', 'resp_arb.io.in[2].bits.uop.mem_signed', 'resp_arb.io.in[2].bits.uop.mem_size', 'resp_arb.io.in[2].bits.uop.op1_sel', 'resp_arb.io.in[2].bits.uop.op2_sel', 'resp_arb.io.in[2].bits.uop.pc_lob', 'resp_arb.io.in[2].bits.uop.pdst', 'resp_arb.io.in[2].bits.uop.pimm', 'resp_arb.io.in[2].bits.uop.ppred', 'resp_arb.io.in[2].bits.uop.ppred_busy', 'resp_arb.io.in[2].bits.uop.prs1', 'resp_arb.io.in[2].bits.uop.prs1_busy', 'resp_arb.io.in[2].bits.uop.prs2', 'resp_arb.io.in[2].bits.uop.prs2_busy', 'resp_arb.io.in[2].bits.uop.prs3', 'resp_arb.io.in[2].bits.uop.prs3_busy', 'resp_arb.io.in[2].bits.uop.rob_idx', 'resp_arb.io.in[2].bits.uop.rxq_idx', 'resp_arb.io.in[2].bits.uop.stale_pdst', 'resp_arb.io.in[2].bits.uop.stq_idx', 'resp_arb.io.in[2].bits.uop.taken', 'resp_arb.io.in[2].bits.uop.uses_ldq', 'resp_arb.io.in[2].bits.uop.uses_stq', 'resp_arb.io.in[2].bits.uop.xcpt_ae_if', 'resp_arb.io.in[2].bits.uop.xcpt_ma_if', 'resp_arb.io.in[2].bits.uop.xcpt_pf_if', 'resp_arb.io.in[2].ready', 'resp_arb.io.in[2].valid', 'resp_arb.reset', 'respq.clock', 'respq.io.brupdate.b1.mispredict_mask', 'respq.io.brupdate.b1.resolve_mask', 'respq.io.brupdate.b2.cfi_type', 'respq.io.brupdate.b2.jalr_target', 'respq.io.brupdate.b2.mispredict', 'respq.io.brupdate.b2.pc_sel', 'respq.io.brupdate.b2.taken', 'respq.io.brupdate.b2.target_offset', 'respq.io.brupdate.b2.uop.bp_debug_if', 'respq.io.brupdate.b2.uop.bp_xcpt_if', 'respq.io.brupdate.b2.uop.br_mask', 'respq.io.brupdate.b2.uop.br_tag', 'respq.io.brupdate.b2.uop.br_type', 'respq.io.brupdate.b2.uop.csr_cmd', 'respq.io.brupdate.b2.uop.debug_fsrc', 'respq.io.brupdate.b2.uop.debug_inst', 'respq.io.brupdate.b2.uop.debug_pc', 'respq.io.brupdate.b2.uop.debug_tsrc', 'respq.io.brupdate.b2.uop.dis_col_sel', 'respq.io.brupdate.b2.uop.dst_rtype', 'respq.io.brupdate.b2.uop.edge_inst', 'respq.io.brupdate.b2.uop.exc_cause', 'respq.io.brupdate.b2.uop.exception', 'respq.io.brupdate.b2.uop.fcn_dw', 'respq.io.brupdate.b2.uop.fcn_op', 'respq.io.brupdate.b2.uop.flush_on_commit', 'respq.io.brupdate.b2.uop.fp_ctrl.div', 'respq.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'respq.io.brupdate.b2.uop.fp_ctrl.fma', 'respq.io.brupdate.b2.uop.fp_ctrl.fromint', 'respq.io.brupdate.b2.uop.fp_ctrl.ldst', 'respq.io.brupdate.b2.uop.fp_ctrl.ren1', 'respq.io.brupdate.b2.uop.fp_ctrl.ren2', 'respq.io.brupdate.b2.uop.fp_ctrl.ren3', 'respq.io.brupdate.b2.uop.fp_ctrl.sqrt', 'respq.io.brupdate.b2.uop.fp_ctrl.swap12', 'respq.io.brupdate.b2.uop.fp_ctrl.swap23', 'respq.io.brupdate.b2.uop.fp_ctrl.toint', 'respq.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'respq.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'respq.io.brupdate.b2.uop.fp_ctrl.vec', 'respq.io.brupdate.b2.uop.fp_ctrl.wen', 'respq.io.brupdate.b2.uop.fp_ctrl.wflags', 'respq.io.brupdate.b2.uop.fp_rm', 'respq.io.brupdate.b2.uop.fp_typ', 'respq.io.brupdate.b2.uop.fp_val', 'respq.io.brupdate.b2.uop.frs3_en', 'respq.io.brupdate.b2.uop.ftq_idx', 'respq.io.brupdate.b2.uop.fu_code[0]', 'respq.io.brupdate.b2.uop.fu_code[1]', 'respq.io.brupdate.b2.uop.fu_code[2]', 'respq.io.brupdate.b2.uop.fu_code[3]', 'respq.io.brupdate.b2.uop.fu_code[4]', 'respq.io.brupdate.b2.uop.fu_code[5]', 'respq.io.brupdate.b2.uop.fu_code[6]', 'respq.io.brupdate.b2.uop.fu_code[7]', 'respq.io.brupdate.b2.uop.fu_code[8]', 'respq.io.brupdate.b2.uop.fu_code[9]', 'respq.io.brupdate.b2.uop.imm_packed', 'respq.io.brupdate.b2.uop.imm_rename', 'respq.io.brupdate.b2.uop.imm_sel', 'respq.io.brupdate.b2.uop.inst', 'respq.io.brupdate.b2.uop.iq_type[0]', 'respq.io.brupdate.b2.uop.iq_type[1]', 'respq.io.brupdate.b2.uop.iq_type[2]', 'respq.io.brupdate.b2.uop.iq_type[3]', 'respq.io.brupdate.b2.uop.is_amo', 'respq.io.brupdate.b2.uop.is_eret', 'respq.io.brupdate.b2.uop.is_fence', 'respq.io.brupdate.b2.uop.is_fencei', 'respq.io.brupdate.b2.uop.is_mov', 'respq.io.brupdate.b2.uop.is_rocc', 'respq.io.brupdate.b2.uop.is_rvc', 'respq.io.brupdate.b2.uop.is_sfb', 'respq.io.brupdate.b2.uop.is_sfence', 'respq.io.brupdate.b2.uop.is_sys_pc2epc', 'respq.io.brupdate.b2.uop.is_unique', 'respq.io.brupdate.b2.uop.iw_issued', 'respq.io.brupdate.b2.uop.iw_issued_partial_agen', 'respq.io.brupdate.b2.uop.iw_issued_partial_dgen', 'respq.io.brupdate.b2.uop.iw_p1_bypass_hint', 'respq.io.brupdate.b2.uop.iw_p1_speculative_child', 'respq.io.brupdate.b2.uop.iw_p2_bypass_hint', 'respq.io.brupdate.b2.uop.iw_p2_speculative_child', 'respq.io.brupdate.b2.uop.iw_p3_bypass_hint', 'respq.io.brupdate.b2.uop.ldq_idx', 'respq.io.brupdate.b2.uop.ldst', 'respq.io.brupdate.b2.uop.ldst_is_rs1', 'respq.io.brupdate.b2.uop.lrs1', 'respq.io.brupdate.b2.uop.lrs1_rtype', 'respq.io.brupdate.b2.uop.lrs2', 'respq.io.brupdate.b2.uop.lrs2_rtype', 'respq.io.brupdate.b2.uop.lrs3', 'respq.io.brupdate.b2.uop.mem_cmd', 'respq.io.brupdate.b2.uop.mem_signed', 'respq.io.brupdate.b2.uop.mem_size', 'respq.io.brupdate.b2.uop.op1_sel', 'respq.io.brupdate.b2.uop.op2_sel', 'respq.io.brupdate.b2.uop.pc_lob', 'respq.io.brupdate.b2.uop.pdst', 'respq.io.brupdate.b2.uop.pimm', 'respq.io.brupdate.b2.uop.ppred', 'respq.io.brupdate.b2.uop.ppred_busy', 'respq.io.brupdate.b2.uop.prs1', 'respq.io.brupdate.b2.uop.prs1_busy', 'respq.io.brupdate.b2.uop.prs2', 'respq.io.brupdate.b2.uop.prs2_busy', 'respq.io.brupdate.b2.uop.prs3', 'respq.io.brupdate.b2.uop.prs3_busy', 'respq.io.brupdate.b2.uop.rob_idx', 'respq.io.brupdate.b2.uop.rxq_idx', 'respq.io.brupdate.b2.uop.stale_pdst', 'respq.io.brupdate.b2.uop.stq_idx', 'respq.io.brupdate.b2.uop.taken', 'respq.io.brupdate.b2.uop.uses_ldq', 'respq.io.brupdate.b2.uop.uses_stq', 'respq.io.brupdate.b2.uop.xcpt_ae_if', 'respq.io.brupdate.b2.uop.xcpt_ma_if', 'respq.io.brupdate.b2.uop.xcpt_pf_if', 'respq.io.deq.ready', 'respq.io.deq.valid', 'respq.io.enq.bits.data', 'respq.io.enq.bits.is_hella', 'respq.io.enq.bits.uop.bp_debug_if', 'respq.io.enq.bits.uop.bp_xcpt_if', 'respq.io.enq.bits.uop.br_mask', 'respq.io.enq.bits.uop.br_tag', 'respq.io.enq.bits.uop.br_type', 'respq.io.enq.bits.uop.csr_cmd', 'respq.io.enq.bits.uop.debug_fsrc', 'respq.io.enq.bits.uop.debug_inst', 'respq.io.enq.bits.uop.debug_pc', 'respq.io.enq.bits.uop.debug_tsrc', 'respq.io.enq.bits.uop.dis_col_sel', 'respq.io.enq.bits.uop.dst_rtype', 'respq.io.enq.bits.uop.edge_inst', 'respq.io.enq.bits.uop.exc_cause', 'respq.io.enq.bits.uop.exception', 'respq.io.enq.bits.uop.fcn_dw', 'respq.io.enq.bits.uop.fcn_op', 'respq.io.enq.bits.uop.flush_on_commit', 'respq.io.enq.bits.uop.fp_ctrl.div', 'respq.io.enq.bits.uop.fp_ctrl.fastpipe', 'respq.io.enq.bits.uop.fp_ctrl.fma', 'respq.io.enq.bits.uop.fp_ctrl.fromint', 'respq.io.enq.bits.uop.fp_ctrl.ldst', 'respq.io.enq.bits.uop.fp_ctrl.ren1', 'respq.io.enq.bits.uop.fp_ctrl.ren2', 'respq.io.enq.bits.uop.fp_ctrl.ren3', 'respq.io.enq.bits.uop.fp_ctrl.sqrt', 'respq.io.enq.bits.uop.fp_ctrl.swap12', 'respq.io.enq.bits.uop.fp_ctrl.swap23', 'respq.io.enq.bits.uop.fp_ctrl.toint', 'respq.io.enq.bits.uop.fp_ctrl.typeTagIn', 'respq.io.enq.bits.uop.fp_ctrl.typeTagOut', 'respq.io.enq.bits.uop.fp_ctrl.vec', 'respq.io.enq.bits.uop.fp_ctrl.wen', 'respq.io.enq.bits.uop.fp_ctrl.wflags', 'respq.io.enq.bits.uop.fp_rm', 'respq.io.enq.bits.uop.fp_typ', 'respq.io.enq.bits.uop.fp_val', 'respq.io.enq.bits.uop.frs3_en', 'respq.io.enq.bits.uop.ftq_idx', 'respq.io.enq.bits.uop.fu_code[0]', 'respq.io.enq.bits.uop.fu_code[1]', 'respq.io.enq.bits.uop.fu_code[2]', 'respq.io.enq.bits.uop.fu_code[3]', 'respq.io.enq.bits.uop.fu_code[4]', 'respq.io.enq.bits.uop.fu_code[5]', 'respq.io.enq.bits.uop.fu_code[6]', 'respq.io.enq.bits.uop.fu_code[7]', 'respq.io.enq.bits.uop.fu_code[8]', 'respq.io.enq.bits.uop.fu_code[9]', 'respq.io.enq.bits.uop.imm_packed', 'respq.io.enq.bits.uop.imm_rename', 'respq.io.enq.bits.uop.imm_sel', 'respq.io.enq.bits.uop.inst', 'respq.io.enq.bits.uop.iq_type[0]', 'respq.io.enq.bits.uop.iq_type[1]', 'respq.io.enq.bits.uop.iq_type[2]', 'respq.io.enq.bits.uop.iq_type[3]', 'respq.io.enq.bits.uop.is_amo', 'respq.io.enq.bits.uop.is_eret', 'respq.io.enq.bits.uop.is_fence', 'respq.io.enq.bits.uop.is_fencei', 'respq.io.enq.bits.uop.is_mov', 'respq.io.enq.bits.uop.is_rocc', 'respq.io.enq.bits.uop.is_rvc', 'respq.io.enq.bits.uop.is_sfb', 'respq.io.enq.bits.uop.is_sfence', 'respq.io.enq.bits.uop.is_sys_pc2epc', 'respq.io.enq.bits.uop.is_unique', 'respq.io.enq.bits.uop.iw_issued', 'respq.io.enq.bits.uop.iw_issued_partial_agen', 'respq.io.enq.bits.uop.iw_issued_partial_dgen', 'respq.io.enq.bits.uop.iw_p1_bypass_hint', 'respq.io.enq.bits.uop.iw_p1_speculative_child', 'respq.io.enq.bits.uop.iw_p2_bypass_hint', 'respq.io.enq.bits.uop.iw_p2_speculative_child', 'respq.io.enq.bits.uop.iw_p3_bypass_hint', 'respq.io.enq.bits.uop.ldq_idx', 'respq.io.enq.bits.uop.ldst', 'respq.io.enq.bits.uop.ldst_is_rs1', 'respq.io.enq.bits.uop.lrs1', 'respq.io.enq.bits.uop.lrs1_rtype', 'respq.io.enq.bits.uop.lrs2', 'respq.io.enq.bits.uop.lrs2_rtype', 'respq.io.enq.bits.uop.lrs3', 'respq.io.enq.bits.uop.mem_cmd', 'respq.io.enq.bits.uop.mem_signed', 'respq.io.enq.bits.uop.mem_size', 'respq.io.enq.bits.uop.op1_sel', 'respq.io.enq.bits.uop.op2_sel', 'respq.io.enq.bits.uop.pc_lob', 'respq.io.enq.bits.uop.pdst', 'respq.io.enq.bits.uop.pimm', 'respq.io.enq.bits.uop.ppred', 'respq.io.enq.bits.uop.ppred_busy', 'respq.io.enq.bits.uop.prs1', 'respq.io.enq.bits.uop.prs1_busy', 'respq.io.enq.bits.uop.prs2', 'respq.io.enq.bits.uop.prs2_busy', 'respq.io.enq.bits.uop.prs3', 'respq.io.enq.bits.uop.prs3_busy', 'respq.io.enq.bits.uop.rob_idx', 'respq.io.enq.bits.uop.rxq_idx', 'respq.io.enq.bits.uop.stale_pdst', 'respq.io.enq.bits.uop.stq_idx', 'respq.io.enq.bits.uop.taken', 'respq.io.enq.bits.uop.uses_ldq', 'respq.io.enq.bits.uop.uses_stq', 'respq.io.enq.bits.uop.xcpt_ae_if', 'respq.io.enq.bits.uop.xcpt_ma_if', 'respq.io.enq.bits.uop.xcpt_pf_if', 'respq.io.enq.ready', 'respq.io.enq.valid', 'respq.io.flush', 'respq.reset', 'wb_req_arb.clock', 'wb_req_arb.io.in[0].bits.idx', 'wb_req_arb.io.in[0].bits.param', 'wb_req_arb.io.in[0].bits.source', 'wb_req_arb.io.in[0].bits.tag', 'wb_req_arb.io.in[0].bits.voluntary', 'wb_req_arb.io.in[0].bits.way_en', 'wb_req_arb.io.in[0].ready', 'wb_req_arb.io.in[0].valid', 'wb_req_arb.io.in[1].bits.idx', 'wb_req_arb.io.in[1].bits.param', 'wb_req_arb.io.in[1].bits.source', 'wb_req_arb.io.in[1].bits.tag', 'wb_req_arb.io.in[1].bits.voluntary', 'wb_req_arb.io.in[1].bits.way_en', 'wb_req_arb.io.in[1].ready', 'wb_req_arb.io.in[1].valid', 'wb_req_arb.io.out.ready', 'wb_req_arb.io.out.valid', 'wb_req_arb.reset']

## Frozen child summaries

### Child `BoomMSHRFile.meta_read_arb`
- summary ref: `umcm://BoomMSHRFile.meta_read_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.meta_read_arb-e5228745004b6981`
- frozen SHA-256: `8928ec1e9ece960dcf21673a763e9ae18f10acb797f2edc0c4832bb94d50b922`
- implementation SHA-256: `82720b497039efffdb034ea50b60f73f44f254b40a1d013599733c6bbf1c8a3c`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.meta_read_arb', 'target_work_unit_id': 'BoomMSHRFile.meta_read_arb', 'module': 'Arbiter2_L1MetaReadReq', 'implementation_sha256': '82720b497039efffdb034ea50b60f73f44f254b40a1d013599733c6bbf1c8a3c', 'structural_implementation_sha256': '2702ab156a41f90b3e429ec92dcda423e5e8f079b76d0b57a6ec71b3fa209426', 'source_module': 'Arbiter2_L1MetaReadReq', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.meta_read_arb::io.in[0].fire', 'BoomMSHRFile.meta_read_arb::io.in[1].fire', 'BoomMSHRFile.meta_read_arb::io.out.fire']
- frontier signals: ['meta_read_arb.clock', 'meta_read_arb.io', 'meta_read_arb.io.chosen', 'meta_read_arb.io.in[0].bits.idx', 'meta_read_arb.io.in[0].bits.tag', 'meta_read_arb.io.in[0].bits.way_en', 'meta_read_arb.io.in[0].ready', 'meta_read_arb.io.in[0].valid', 'meta_read_arb.io.in[1].bits.idx', 'meta_read_arb.io.in[1].bits.tag', 'meta_read_arb.io.in[1].bits.way_en', 'meta_read_arb.io.in[1].ready', 'meta_read_arb.io.in[1].valid', 'meta_read_arb.io.out.bits.idx', 'meta_read_arb.io.out.bits.tag', 'meta_read_arb.io.out.bits.way_en', 'meta_read_arb.io.out.ready', 'meta_read_arb.io.out.valid', 'meta_read_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.meta_read_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.meta_read_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.meta_read_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    },
    "BoomMSHRFile.meta_read_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.meta_read_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.meta_read_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A3",
      "rendered_formula": "io.out.bits.idx = io.in[0].bits.idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.tag = io.in[0].bits.tag on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.idx = io.in[1].bits.idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.tag = io.in[1].bits.tag on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has fixed priority; an accepted input-0 metadata-read request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only when input 0 is not valid; the accepted metadata-read request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 8,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 8
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        9,
        10
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_read_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_read_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        13,
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_read_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        5,
        8
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.meta_read_arb-e5228745004b6981",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8"
  ],
  "work_unit_id": "BoomMSHRFile.meta_read_arb"
}
```

### Child `BoomMSHRFile.meta_write_arb`
- summary ref: `umcm://BoomMSHRFile.meta_write_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.meta_write_arb-37cf63871121acc7`
- frozen SHA-256: `8f9a6e37619a0b0b0e9d18501b4e7064c0b5d72ef992b574d2e6b4bf66ddeedd`
- implementation SHA-256: `b876c438adeb159dec9a0cee68b09d9d46ce72a10a5595858c0ff7097d9d9c86`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.meta_write_arb', 'target_work_unit_id': 'BoomMSHRFile.meta_write_arb', 'module': 'Arbiter2_L1MetaWriteReq', 'implementation_sha256': 'b876c438adeb159dec9a0cee68b09d9d46ce72a10a5595858c0ff7097d9d9c86', 'structural_implementation_sha256': '54c2255e9e33b87d9055a6ef61bc5d083684d3ad24a3454ca0d02b54c5caee8c', 'source_module': 'Arbiter2_L1MetaWriteReq', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.meta_write_arb::io.in[0].fire', 'BoomMSHRFile.meta_write_arb::io.in[1].fire', 'BoomMSHRFile.meta_write_arb::io.out.fire']
- frontier signals: ['meta_write_arb.clock', 'meta_write_arb.io', 'meta_write_arb.io.chosen', 'meta_write_arb.io.in[0].bits.data.coh.state', 'meta_write_arb.io.in[0].bits.data.tag', 'meta_write_arb.io.in[0].bits.idx', 'meta_write_arb.io.in[0].bits.tag', 'meta_write_arb.io.in[0].bits.way_en', 'meta_write_arb.io.in[0].ready', 'meta_write_arb.io.in[0].valid', 'meta_write_arb.io.in[1].bits.data.coh.state', 'meta_write_arb.io.in[1].bits.data.tag', 'meta_write_arb.io.in[1].bits.idx', 'meta_write_arb.io.in[1].bits.tag', 'meta_write_arb.io.in[1].bits.way_en', 'meta_write_arb.io.in[1].ready', 'meta_write_arb.io.in[1].valid', 'meta_write_arb.io.out.bits.data.coh.state', 'meta_write_arb.io.out.bits.data.tag', 'meta_write_arb.io.out.bits.idx', 'meta_write_arb.io.out.bits.tag', 'meta_write_arb.io.out.bits.way_en', 'meta_write_arb.io.out.ready', 'meta_write_arb.io.out.valid', 'meta_write_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.meta_write_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.meta_write_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.meta_write_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    },
    "BoomMSHRFile.meta_write_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.meta_write_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.meta_write_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A3",
      "rendered_formula": "io.out.bits.idx = io.in[0].bits.idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.tag = io.in[0].bits.tag on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.data.coh.state",
          "op": "signal"
        },
        "target": "io.out.bits.data.coh.state",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.data.coh.state = io.in[0].bits.data.coh.state on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.data.tag",
          "op": "signal"
        },
        "target": "io.out.bits.data.tag",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.data.tag = io.in[0].bits.data.tag on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.idx = io.in[1].bits.idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A10",
      "rendered_formula": "io.out.bits.tag = io.in[1].bits.tag on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.data.coh.state",
          "op": "signal"
        },
        "target": "io.out.bits.data.coh.state",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.out.bits.data.coh.state = io.in[1].bits.data.coh.state on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.data.tag",
          "op": "signal"
        },
        "target": "io.out.bits.data.tag",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.out.bits.data.tag = io.in[1].bits.data.tag on Input1Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has priority and an accepted input-0 metadata write is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only while input 0 is not valid, and the accepted metadata write is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 12,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 12
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        9,
        10
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        13,
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.meta_write_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        5,
        8
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.meta_write_arb-37cf63871121acc7",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.meta_write_arb"
}
```

### Child `BoomMSHRFile.mmio_alloc_arb`
- summary ref: `umcm://BoomMSHRFile.mmio_alloc_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e`
- frozen SHA-256: `d4186ed9b2d0d4e4c37afe21f1fe2dd460be260048e2b8579be5f3c47f541ba6`
- implementation SHA-256: `3ff0ecb79178396eda917b958b3cfcf8b524ae83b7df3366b5017131fb62ce70`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.mmio_alloc_arb', 'target_work_unit_id': 'BoomMSHRFile.mmio_alloc_arb', 'module': 'Arbiter1_Bool', 'implementation_sha256': '3ff0ecb79178396eda917b958b3cfcf8b524ae83b7df3366b5017131fb62ce70', 'structural_implementation_sha256': '588357332a49b222910e5a52fa1ed8adc6442e4c59fdceccb81b4f6e1ae97493', 'source_module': 'Arbiter1_Bool', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.mmio_alloc_arb::io.in[0].fire', 'BoomMSHRFile.mmio_alloc_arb::io.out.fire']
- frontier signals: ['mmio_alloc_arb.clock', 'mmio_alloc_arb.io', 'mmio_alloc_arb.io.chosen', 'mmio_alloc_arb.io.in[0].bits', 'mmio_alloc_arb.io.in[0].ready', 'mmio_alloc_arb.io.in[0].valid', 'mmio_alloc_arb.io.out.bits', 'mmio_alloc_arb.io.out.ready', 'mmio_alloc_arb.io.out.valid', 'mmio_alloc_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.mmio_alloc_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
    },
    "BoomMSHRFile.mmio_alloc_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.mmio_alloc_arb::C1_Passthrough": {
      "local_id": "C1_Passthrough",
      "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.mmio_alloc_arb::InputFire": {
      "local_id": "InputFire",
      "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
    },
    "BoomMSHRFile.mmio_alloc_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
    }
  },
  "predicates": {}
}
```

Trusted frozen child µMCM:
```json
{
  "assumptions": [],
  "axioms": [
    {
      "derived_from_case_ids": [
        "C1_Passthrough"
      ],
      "evidence_statement_ids": [
        5,
        6,
        7,
        8,
        9
      ],
      "formal": {
        "parts": [
          "InputFire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({InputFire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Passthrough"
      ],
      "evidence_statement_ids": [
        4
      ],
      "formal": {
        "on": "InputFire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits",
          "op": "signal"
        },
        "target": "io.out.bits",
        "type": "signal_equality"
      },
      "id": "A2",
      "rendered_formula": "io.out.bits = io.in[0].bits on InputFire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        8,
        9
      ],
      "guard_predicates": [],
      "id": "C1_Passthrough",
      "relations": [
        "The single accepted MMIO-allocation input is forwarded to the output in exactly the same cycle."
      ],
      "trigger_occurrences": [
        "InputFire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 2,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 2
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        5,
        6
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "InputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mmio_alloc_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        7,
        8,
        9
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mmio_alloc_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.mmio_alloc_arb-4b970ccfa4defb7e",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2"
  ],
  "work_unit_id": "BoomMSHRFile.mmio_alloc_arb"
}
```

### Child `BoomMSHRFile.mmios_0`
- summary ref: `umcm://BoomMSHRFile.mmios_0`
- frozen task: `leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259`
- frozen SHA-256: `b5bd13530e15dcb11ca5e6f1fc3324013adf75118283d96f6dea838435c453bb`
- implementation SHA-256: `b1e018ee7d68a5971dee2568bf47f5af3e80576af306f1e0672f21a647539aeb`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.mmios_0', 'target_work_unit_id': 'BoomMSHRFile.mmios_0', 'module': 'BoomIOMSHR', 'implementation_sha256': 'b1e018ee7d68a5971dee2568bf47f5af3e80576af306f1e0672f21a647539aeb', 'structural_implementation_sha256': 'e198275722a4bdfc31facda652c6602513a53876fae4c38005c64b4017a55e50', 'source_module': 'BoomIOMSHR', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.mmios_0::io.mem_access.fire', 'BoomMSHRFile.mmios_0::io.mem_ack.valid', 'BoomMSHRFile.mmios_0::io.req.fire', 'BoomMSHRFile.mmios_0::io.resp.fire']
- frontier signals: ['mmios_0.clock', 'mmios_0.io', 'mmios_0.io.mem_access.bits.address', 'mmios_0.io.mem_access.bits.corrupt', 'mmios_0.io.mem_access.bits.data', 'mmios_0.io.mem_access.bits.mask', 'mmios_0.io.mem_access.bits.opcode', 'mmios_0.io.mem_access.bits.param', 'mmios_0.io.mem_access.bits.size', 'mmios_0.io.mem_access.bits.source', 'mmios_0.io.mem_access.ready', 'mmios_0.io.mem_access.valid', 'mmios_0.io.mem_ack.bits.corrupt', 'mmios_0.io.mem_ack.bits.data', 'mmios_0.io.mem_ack.bits.denied', 'mmios_0.io.mem_ack.bits.opcode', 'mmios_0.io.mem_ack.bits.param', 'mmios_0.io.mem_ack.bits.sink', 'mmios_0.io.mem_ack.bits.size', 'mmios_0.io.mem_ack.bits.source', 'mmios_0.io.mem_ack.valid', 'mmios_0.io.req.bits.addr', 'mmios_0.io.req.bits.data', 'mmios_0.io.req.bits.is_hella', 'mmios_0.io.req.bits.uop.bp_debug_if', 'mmios_0.io.req.bits.uop.bp_xcpt_if', 'mmios_0.io.req.bits.uop.br_mask', 'mmios_0.io.req.bits.uop.br_tag', 'mmios_0.io.req.bits.uop.br_type', 'mmios_0.io.req.bits.uop.csr_cmd', 'mmios_0.io.req.bits.uop.debug_fsrc', 'mmios_0.io.req.bits.uop.debug_inst', 'mmios_0.io.req.bits.uop.debug_pc', 'mmios_0.io.req.bits.uop.debug_tsrc', 'mmios_0.io.req.bits.uop.dis_col_sel', 'mmios_0.io.req.bits.uop.dst_rtype', 'mmios_0.io.req.bits.uop.edge_inst', 'mmios_0.io.req.bits.uop.exc_cause', 'mmios_0.io.req.bits.uop.exception', 'mmios_0.io.req.bits.uop.fcn_dw', 'mmios_0.io.req.bits.uop.fcn_op', 'mmios_0.io.req.bits.uop.flush_on_commit', 'mmios_0.io.req.bits.uop.fp_ctrl.div', 'mmios_0.io.req.bits.uop.fp_ctrl.fastpipe', 'mmios_0.io.req.bits.uop.fp_ctrl.fma', 'mmios_0.io.req.bits.uop.fp_ctrl.fromint', 'mmios_0.io.req.bits.uop.fp_ctrl.ldst', 'mmios_0.io.req.bits.uop.fp_ctrl.ren1', 'mmios_0.io.req.bits.uop.fp_ctrl.ren2', 'mmios_0.io.req.bits.uop.fp_ctrl.ren3', 'mmios_0.io.req.bits.uop.fp_ctrl.sqrt', 'mmios_0.io.req.bits.uop.fp_ctrl.swap12', 'mmios_0.io.req.bits.uop.fp_ctrl.swap23', 'mmios_0.io.req.bits.uop.fp_ctrl.toint', 'mmios_0.io.req.bits.uop.fp_ctrl.typeTagIn', 'mmios_0.io.req.bits.uop.fp_ctrl.typeTagOut', 'mmios_0.io.req.bits.uop.fp_ctrl.vec', 'mmios_0.io.req.bits.uop.fp_ctrl.wen', 'mmios_0.io.req.bits.uop.fp_ctrl.wflags', 'mmios_0.io.req.bits.uop.fp_rm', 'mmios_0.io.req.bits.uop.fp_typ', 'mmios_0.io.req.bits.uop.fp_val', 'mmios_0.io.req.bits.uop.frs3_en', 'mmios_0.io.req.bits.uop.ftq_idx', 'mmios_0.io.req.bits.uop.fu_code[0]', 'mmios_0.io.req.bits.uop.fu_code[1]', 'mmios_0.io.req.bits.uop.fu_code[2]', 'mmios_0.io.req.bits.uop.fu_code[3]', 'mmios_0.io.req.bits.uop.fu_code[4]', 'mmios_0.io.req.bits.uop.fu_code[5]', 'mmios_0.io.req.bits.uop.fu_code[6]', 'mmios_0.io.req.bits.uop.fu_code[7]', 'mmios_0.io.req.bits.uop.fu_code[8]', 'mmios_0.io.req.bits.uop.fu_code[9]', 'mmios_0.io.req.bits.uop.imm_packed', 'mmios_0.io.req.bits.uop.imm_rename', 'mmios_0.io.req.bits.uop.imm_sel', 'mmios_0.io.req.bits.uop.inst', 'mmios_0.io.req.bits.uop.iq_type[0]', 'mmios_0.io.req.bits.uop.iq_type[1]', 'mmios_0.io.req.bits.uop.iq_type[2]', 'mmios_0.io.req.bits.uop.iq_type[3]', 'mmios_0.io.req.bits.uop.is_amo', 'mmios_0.io.req.bits.uop.is_eret', 'mmios_0.io.req.bits.uop.is_fence', 'mmios_0.io.req.bits.uop.is_fencei', 'mmios_0.io.req.bits.uop.is_mov', 'mmios_0.io.req.bits.uop.is_rocc', 'mmios_0.io.req.bits.uop.is_rvc', 'mmios_0.io.req.bits.uop.is_sfb', 'mmios_0.io.req.bits.uop.is_sfence', 'mmios_0.io.req.bits.uop.is_sys_pc2epc', 'mmios_0.io.req.bits.uop.is_unique', 'mmios_0.io.req.bits.uop.iw_issued', 'mmios_0.io.req.bits.uop.iw_issued_partial_agen', 'mmios_0.io.req.bits.uop.iw_issued_partial_dgen', 'mmios_0.io.req.bits.uop.iw_p1_bypass_hint', 'mmios_0.io.req.bits.uop.iw_p1_speculative_child', 'mmios_0.io.req.bits.uop.iw_p2_bypass_hint', 'mmios_0.io.req.bits.uop.iw_p2_speculative_child', 'mmios_0.io.req.bits.uop.iw_p3_bypass_hint', 'mmios_0.io.req.bits.uop.ldq_idx', 'mmios_0.io.req.bits.uop.ldst', 'mmios_0.io.req.bits.uop.ldst_is_rs1', 'mmios_0.io.req.bits.uop.lrs1', 'mmios_0.io.req.bits.uop.lrs1_rtype', 'mmios_0.io.req.bits.uop.lrs2', 'mmios_0.io.req.bits.uop.lrs2_rtype', 'mmios_0.io.req.bits.uop.lrs3', 'mmios_0.io.req.bits.uop.mem_cmd', 'mmios_0.io.req.bits.uop.mem_signed', 'mmios_0.io.req.bits.uop.mem_size', 'mmios_0.io.req.bits.uop.op1_sel', 'mmios_0.io.req.bits.uop.op2_sel', 'mmios_0.io.req.bits.uop.pc_lob', 'mmios_0.io.req.bits.uop.pdst', 'mmios_0.io.req.bits.uop.pimm', 'mmios_0.io.req.bits.uop.ppred', 'mmios_0.io.req.bits.uop.ppred_busy', 'mmios_0.io.req.bits.uop.prs1', 'mmios_0.io.req.bits.uop.prs1_busy', 'mmios_0.io.req.bits.uop.prs2', 'mmios_0.io.req.bits.uop.prs2_busy', 'mmios_0.io.req.bits.uop.prs3', 'mmios_0.io.req.bits.uop.prs3_busy', 'mmios_0.io.req.bits.uop.rob_idx', 'mmios_0.io.req.bits.uop.rxq_idx', 'mmios_0.io.req.bits.uop.stale_pdst', 'mmios_0.io.req.bits.uop.stq_idx', 'mmios_0.io.req.bits.uop.taken', 'mmios_0.io.req.bits.uop.uses_ldq', 'mmios_0.io.req.bits.uop.uses_stq', 'mmios_0.io.req.bits.uop.xcpt_ae_if', 'mmios_0.io.req.bits.uop.xcpt_ma_if', 'mmios_0.io.req.bits.uop.xcpt_pf_if', 'mmios_0.io.req.ready', 'mmios_0.io.req.valid', 'mmios_0.io.resp.bits.data', 'mmios_0.io.resp.bits.is_hella', 'mmios_0.io.resp.bits.uop.bp_debug_if', 'mmios_0.io.resp.bits.uop.bp_xcpt_if', 'mmios_0.io.resp.bits.uop.br_mask', 'mmios_0.io.resp.bits.uop.br_tag', 'mmios_0.io.resp.bits.uop.br_type', 'mmios_0.io.resp.bits.uop.csr_cmd', 'mmios_0.io.resp.bits.uop.debug_fsrc', 'mmios_0.io.resp.bits.uop.debug_inst', 'mmios_0.io.resp.bits.uop.debug_pc', 'mmios_0.io.resp.bits.uop.debug_tsrc', 'mmios_0.io.resp.bits.uop.dis_col_sel', 'mmios_0.io.resp.bits.uop.dst_rtype', 'mmios_0.io.resp.bits.uop.edge_inst', 'mmios_0.io.resp.bits.uop.exc_cause', 'mmios_0.io.resp.bits.uop.exception', 'mmios_0.io.resp.bits.uop.fcn_dw', 'mmios_0.io.resp.bits.uop.fcn_op', 'mmios_0.io.resp.bits.uop.flush_on_commit', 'mmios_0.io.resp.bits.uop.fp_ctrl.div', 'mmios_0.io.resp.bits.uop.fp_ctrl.fastpipe', 'mmios_0.io.resp.bits.uop.fp_ctrl.fma', 'mmios_0.io.resp.bits.uop.fp_ctrl.fromint', 'mmios_0.io.resp.bits.uop.fp_ctrl.ldst', 'mmios_0.io.resp.bits.uop.fp_ctrl.ren1', 'mmios_0.io.resp.bits.uop.fp_ctrl.ren2', 'mmios_0.io.resp.bits.uop.fp_ctrl.ren3', 'mmios_0.io.resp.bits.uop.fp_ctrl.sqrt', 'mmios_0.io.resp.bits.uop.fp_ctrl.swap12', 'mmios_0.io.resp.bits.uop.fp_ctrl.swap23', 'mmios_0.io.resp.bits.uop.fp_ctrl.toint', 'mmios_0.io.resp.bits.uop.fp_ctrl.typeTagIn', 'mmios_0.io.resp.bits.uop.fp_ctrl.typeTagOut', 'mmios_0.io.resp.bits.uop.fp_ctrl.vec', 'mmios_0.io.resp.bits.uop.fp_ctrl.wen', 'mmios_0.io.resp.bits.uop.fp_ctrl.wflags', 'mmios_0.io.resp.bits.uop.fp_rm', 'mmios_0.io.resp.bits.uop.fp_typ', 'mmios_0.io.resp.bits.uop.fp_val', 'mmios_0.io.resp.bits.uop.frs3_en', 'mmios_0.io.resp.bits.uop.ftq_idx', 'mmios_0.io.resp.bits.uop.fu_code[0]', 'mmios_0.io.resp.bits.uop.fu_code[1]', 'mmios_0.io.resp.bits.uop.fu_code[2]', 'mmios_0.io.resp.bits.uop.fu_code[3]', 'mmios_0.io.resp.bits.uop.fu_code[4]', 'mmios_0.io.resp.bits.uop.fu_code[5]', 'mmios_0.io.resp.bits.uop.fu_code[6]', 'mmios_0.io.resp.bits.uop.fu_code[7]', 'mmios_0.io.resp.bits.uop.fu_code[8]', 'mmios_0.io.resp.bits.uop.fu_code[9]', 'mmios_0.io.resp.bits.uop.imm_packed', 'mmios_0.io.resp.bits.uop.imm_rename', 'mmios_0.io.resp.bits.uop.imm_sel', 'mmios_0.io.resp.bits.uop.inst', 'mmios_0.io.resp.bits.uop.iq_type[0]', 'mmios_0.io.resp.bits.uop.iq_type[1]', 'mmios_0.io.resp.bits.uop.iq_type[2]', 'mmios_0.io.resp.bits.uop.iq_type[3]', 'mmios_0.io.resp.bits.uop.is_amo', 'mmios_0.io.resp.bits.uop.is_eret', 'mmios_0.io.resp.bits.uop.is_fence', 'mmios_0.io.resp.bits.uop.is_fencei', 'mmios_0.io.resp.bits.uop.is_mov', 'mmios_0.io.resp.bits.uop.is_rocc', 'mmios_0.io.resp.bits.uop.is_rvc', 'mmios_0.io.resp.bits.uop.is_sfb', 'mmios_0.io.resp.bits.uop.is_sfence', 'mmios_0.io.resp.bits.uop.is_sys_pc2epc', 'mmios_0.io.resp.bits.uop.is_unique', 'mmios_0.io.resp.bits.uop.iw_issued', 'mmios_0.io.resp.bits.uop.iw_issued_partial_agen', 'mmios_0.io.resp.bits.uop.iw_issued_partial_dgen', 'mmios_0.io.resp.bits.uop.iw_p1_bypass_hint', 'mmios_0.io.resp.bits.uop.iw_p1_speculative_child', 'mmios_0.io.resp.bits.uop.iw_p2_bypass_hint', 'mmios_0.io.resp.bits.uop.iw_p2_speculative_child', 'mmios_0.io.resp.bits.uop.iw_p3_bypass_hint', 'mmios_0.io.resp.bits.uop.ldq_idx', 'mmios_0.io.resp.bits.uop.ldst', 'mmios_0.io.resp.bits.uop.ldst_is_rs1', 'mmios_0.io.resp.bits.uop.lrs1', 'mmios_0.io.resp.bits.uop.lrs1_rtype', 'mmios_0.io.resp.bits.uop.lrs2', 'mmios_0.io.resp.bits.uop.lrs2_rtype', 'mmios_0.io.resp.bits.uop.lrs3', 'mmios_0.io.resp.bits.uop.mem_cmd', 'mmios_0.io.resp.bits.uop.mem_signed', 'mmios_0.io.resp.bits.uop.mem_size', 'mmios_0.io.resp.bits.uop.op1_sel', 'mmios_0.io.resp.bits.uop.op2_sel', 'mmios_0.io.resp.bits.uop.pc_lob', 'mmios_0.io.resp.bits.uop.pdst', 'mmios_0.io.resp.bits.uop.pimm', 'mmios_0.io.resp.bits.uop.ppred', 'mmios_0.io.resp.bits.uop.ppred_busy', 'mmios_0.io.resp.bits.uop.prs1', 'mmios_0.io.resp.bits.uop.prs1_busy', 'mmios_0.io.resp.bits.uop.prs2', 'mmios_0.io.resp.bits.uop.prs2_busy', 'mmios_0.io.resp.bits.uop.prs3', 'mmios_0.io.resp.bits.uop.prs3_busy', 'mmios_0.io.resp.bits.uop.rob_idx', 'mmios_0.io.resp.bits.uop.rxq_idx', 'mmios_0.io.resp.bits.uop.stale_pdst', 'mmios_0.io.resp.bits.uop.stq_idx', 'mmios_0.io.resp.bits.uop.taken', 'mmios_0.io.resp.bits.uop.uses_ldq', 'mmios_0.io.resp.bits.uop.uses_stq', 'mmios_0.io.resp.bits.uop.xcpt_ae_if', 'mmios_0.io.resp.bits.uop.xcpt_ma_if', 'mmios_0.io.resp.bits.uop.xcpt_pf_if', 'mmios_0.io.resp.ready', 'mmios_0.io.resp.valid', 'mmios_0.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.mmios_0::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    }
  },
  "cases": {
    "BoomMSHRFile.mmios_0::C1_RequestCaptured": {
      "local_id": "C1_RequestCaptured",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::C2_ResponseProducingAck": {
      "local_id": "C2_ResponseProducingAck",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::C3_NoResponseAck": {
      "local_id": "C3_NoResponseAck",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    }
  },
  "identity_keys": {
    "BoomMSHRFile.mmios_0::RequestIdentity": {
      "local_id": "RequestIdentity",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    }
  },
  "occurrences": {
    "BoomMSHRFile.mmios_0::AckConsumed": {
      "local_id": "AckConsumed",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::MemAccess": {
      "local_id": "MemAccess",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::ReqAccept": {
      "local_id": "ReqAccept",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::RespHandshake": {
      "local_id": "RespHandshake",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    }
  },
  "predicates": {
    "BoomMSHRFile.mmios_0::Busy": {
      "local_id": "Busy",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    },
    "BoomMSHRFile.mmios_0::NoResponseRequired": {
      "local_id": "NoResponseRequired",
      "work_unit_id": "BoomMSHRFile.mmios_0"
    }
  }
}
```

Trusted frozen child µMCM:
```json
{
  "assumptions": [
    {
      "evidence_statement_ids": [
        1471,
        1472,
        1473,
        1474,
        1475,
        1476,
        1477,
        1478,
        1480,
        1603,
        1604
      ],
      "id": "E1_NoAcceptedXSC",
      "statement": "The environment must not supply an accepted request whose req.uop.mem_cmd is M_XSC (numeric value 7); after such a request leaves s_idle, the module-local assertion state === s_idle || req.uop.mem_cmd =/= M_XSC would fail."
    }
  ],
  "axioms": [
    {
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        6,
        7,
        1601
      ],
      "formal": {
        "occurrence": "ReqAccept",
        "predicate": "Busy",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A1",
      "rendered_formula": "Busy => !ReqAccept",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        1481,
        1482,
        1601,
        1602,
        1603,
        1604,
        1605,
        1606,
        1607
      ],
      "formal": {
        "after": "MemAccess",
        "before": "ReqAccept",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A2",
      "rendered_formula": "ReqAccept <mu MemAccess",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ResponseProducingAck",
        "C3_NoResponseAck"
      ],
      "evidence_statement_ids": [
        1605,
        1606,
        1607,
        1608,
        1609,
        1610,
        1611
      ],
      "formal": {
        "after": "AckConsumed",
        "before": "MemAccess",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A3",
      "rendered_formula": "MemAccess <mu AckConsumed",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1611,
        1642,
        1643,
        1645
      ],
      "formal": {
        "after": "RespHandshake",
        "before": "AckConsumed",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A4",
      "rendered_formula": "AckConsumed <mu RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_NoResponseAck"
      ],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555
      ],
      "formal": {
        "occurrence": "RespHandshake",
        "predicate": "NoResponseRequired",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A5",
      "rendered_formula": "NoResponseRequired => !RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_RequestCaptured",
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1603,
        1556
      ],
      "formal": {
        "capture": {
          "carrier": "req",
          "on": "ReqAccept",
          "source": "io.req.bits"
        },
        "identity": "RequestIdentity",
        "projections": [
          {
            "expr": {
              "name": "req.uop.rob_idx",
              "op": "signal"
            },
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.rob_idx"
          },
          {
            "expr": {
              "name": "req.uop.ldq_idx",
              "op": "signal"
            },
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.ldq_idx"
          },
          {
            "expr": {
              "name": "req.uop.stq_idx",
              "op": "signal"
            },
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.stq_idx"
          },
          {
            "expr": {
              "name": "req.uop.mem_cmd",
              "op": "signal"
            },
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.mem_cmd"
          },
          {
            "expr": {
              "name": "req.uop.mem_size",
              "op": "signal"
            },
            "on": "RespHandshake",
            "target": "io.resp.bits.uop.mem_size"
          }
        ],
        "type": "identity_flow"
      },
      "id": "A6",
      "rendered_formula": "capture RequestIdentity := io.req.bits on ReqAccept; preserve 5 exact identity projections",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        79,
        224,
        361,
        489,
        617,
        745,
        873,
        1001,
        1129,
        1257,
        1385,
        1525,
        1526,
        1527
      ],
      "formal": {
        "on": "MemAccess",
        "scope_identity": null,
        "source": {
          "hi": 31,
          "lo": 0,
          "op": "slice",
          "value": {
            "name": "req.addr",
            "op": "signal"
          }
        },
        "target": "io.mem_access.bits.address",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.mem_access.bits.address = bits(req.addr, 31, 0) on MemAccess",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_RequestCaptured"
      ],
      "evidence_statement_ids": [
        77,
        222,
        359,
        487,
        615,
        743,
        871,
        999,
        1127,
        1255,
        1383,
        1525,
        1526,
        1527
      ],
      "formal": {
        "on": "MemAccess",
        "scope_identity": null,
        "source": {
          "name": "req.uop.mem_size",
          "op": "signal"
        },
        "target": "io.mem_access.bits.size",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.mem_access.bits.size = req.uop.mem_size on MemAccess",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_ResponseProducingAck"
      ],
      "evidence_statement_ids": [
        1600
      ],
      "formal": {
        "on": "RespHandshake",
        "scope_identity": null,
        "source": {
          "name": "req.is_hella",
          "op": "signal"
        },
        "target": "io.resp.bits.is_hella",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.resp.bits.is_hella = req.is_hella on RespHandshake",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1601,
        1602,
        1603,
        1604
      ],
      "guard_predicates": [],
      "id": "C1_RequestCaptured",
      "relations": [
        "The accepted request is captured into req and the FSM enters the memory-access state."
      ],
      "trigger_occurrences": [
        "ReqAccept"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1608,
        1609,
        1610,
        1611,
        1637,
        1638,
        1639,
        1640,
        1641
      ],
      "guard_predicates": [
        {
          "id": "NoResponseRequired",
          "positive": false
        }
      ],
      "id": "C2_ResponseProducingAck",
      "relations": [
        "A consumed acknowledgement for a read-like request moves the FSM to the response state; read-return data is captured into grant_word and io.resp.valid is asserted from that state."
      ],
      "trigger_occurrences": [
        "AckConsumed"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1608,
        1609,
        1610,
        1611,
        1642,
        1643,
        1644,
        1646,
        1647,
        1648
      ],
      "guard_predicates": [
        {
          "id": "NoResponseRequired",
          "positive": true
        }
      ],
      "id": "C3_NoResponseAck",
      "relations": [
        "A consumed acknowledgement for a request with send_resp false reaches the response state but cannot produce RespHandshake and returns to idle without waiting for io.resp.ready."
      ],
      "trigger_occurrences": [
        "AckConsumed"
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
  "identity_keys": [
    {
      "carrier_state": "req",
      "description": "The accepted MMIO request is stored in req and remains the single outstanding transaction context until the MSHR returns to idle.",
      "evidence_statement_ids": [
        3,
        1603
      ],
      "fields": [
        "addr",
        "uop.rob_idx",
        "uop.ldq_idx",
        "uop.stq_idx",
        "uop.mem_cmd",
        "uop.mem_size"
      ],
      "id": "RequestIdentity"
    }
  ],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.req.valid && io.req.ready",
      "evidence_statement_ids": [
        6,
        7,
        1601,
        1602
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          0
        ]
      },
      "id": "ReqAccept",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.req.fire"
      ]
    },
    {
      "definition": "io.mem_access.valid && io.mem_access.ready",
      "evidence_statement_ids": [
        1481,
        1482,
        1605,
        1606
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          1
        ]
      },
      "id": "MemAccess",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.mem_access.fire"
      ]
    },
    {
      "definition": "state == 2 && io.mem_ack.valid",
      "evidence_statement_ids": [
        1608,
        1609,
        1610,
        1611
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.mem_ack.valid"
        ],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "AckConsumed",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "io.resp.valid && io.resp.ready",
      "evidence_statement_ids": [
        1552,
        1553,
        1554,
        1555,
        1645
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "send_resp"
        ],
        "state_register": "state",
        "state_values": [
          3
        ]
      },
      "id": "RespHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mmios_0::io.resp.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "state != 0",
      "evidence_statement_ids": [
        5,
        1604,
        1607,
        1611,
        1648
      ],
      "grounding": {
        "negated": false,
        "source_signal": null,
        "state_register": "state",
        "state_values": [
          1,
          2,
          3
        ]
      },
      "id": "Busy"
    },
    {
      "definition": "!send_resp",
      "evidence_statement_ids": [
        1528,
        1529,
        1530,
        1531,
        1532,
        1533,
        1534,
        1535,
        1536,
        1537,
        1538,
        1539,
        1540,
        1541,
        1542,
        1543,
        1544,
        1545,
        1546,
        1547,
        1548,
        1549,
        1550,
        1551,
        1552
      ],
      "grounding": {
        "negated": true,
        "source_signal": "send_resp",
        "state_register": null,
        "state_values": []
      },
      "id": "NoResponseRequired"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.mmios_0"
}
```

### Child `BoomMSHRFile.mshrs_0`
- summary ref: `umcm://BoomMSHRFile.mshrs_0`
- frozen task: `parent_synthesis-BoomMSHR-6362a83e7f824669`
- frozen SHA-256: `2b3de6e6d96a83514e4a743defd9ed698b6d3fad9fcd4060a0c9150de242a14b`
- implementation SHA-256: `2976194baa527415e97023702c9b66e8b5f10fd8bb6a226b6d3945e9120efbab`
- instance reuse certificate: `{'kind': 'module-theorem-template-instantiation', 'source_work_unit_id': 'BoomMSHR', 'target_work_unit_id': 'BoomMSHRFile.mshrs_0', 'module': 'BoomMSHR', 'implementation_sha256': '2976194baa527415e97023702c9b66e8b5f10fd8bb6a226b6d3945e9120efbab', 'structural_implementation_sha256': '976a59a277cde914bcc9b2c10fd08b16f63a666901c2093837633353cce0e6fa', 'source_module': 'BoomMSHR', 'verification': 'source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1'}`
- exposed boundary events: ['BoomMSHRFile.mshrs_0::io.idx.valid', 'BoomMSHRFile.mshrs_0::io.lb_write.valid', 'BoomMSHRFile.mshrs_0::io.mem_acquire.fire', 'BoomMSHRFile.mshrs_0::io.mem_finish.fire', 'BoomMSHRFile.mshrs_0::io.mem_grant.fire', 'BoomMSHRFile.mshrs_0::io.meta_read.fire', 'BoomMSHRFile.mshrs_0::io.meta_resp.valid', 'BoomMSHRFile.mshrs_0::io.meta_write.fire', 'BoomMSHRFile.mshrs_0::io.prober_state.valid', 'BoomMSHRFile.mshrs_0::io.refill.fire', 'BoomMSHRFile.mshrs_0::io.replay.fire', 'BoomMSHRFile.mshrs_0::io.resp.fire', 'BoomMSHRFile.mshrs_0::io.tag.valid', 'BoomMSHRFile.mshrs_0::io.way.valid', 'BoomMSHRFile.mshrs_0::io.wb_req.fire']
- frontier signals: ['mshrs_0.clock', 'mshrs_0.io', 'mshrs_0.io.brupdate.b1.mispredict_mask', 'mshrs_0.io.brupdate.b1.resolve_mask', 'mshrs_0.io.brupdate.b2.cfi_type', 'mshrs_0.io.brupdate.b2.jalr_target', 'mshrs_0.io.brupdate.b2.mispredict', 'mshrs_0.io.brupdate.b2.pc_sel', 'mshrs_0.io.brupdate.b2.taken', 'mshrs_0.io.brupdate.b2.target_offset', 'mshrs_0.io.brupdate.b2.uop.bp_debug_if', 'mshrs_0.io.brupdate.b2.uop.bp_xcpt_if', 'mshrs_0.io.brupdate.b2.uop.br_mask', 'mshrs_0.io.brupdate.b2.uop.br_tag', 'mshrs_0.io.brupdate.b2.uop.br_type', 'mshrs_0.io.brupdate.b2.uop.csr_cmd', 'mshrs_0.io.brupdate.b2.uop.debug_fsrc', 'mshrs_0.io.brupdate.b2.uop.debug_inst', 'mshrs_0.io.brupdate.b2.uop.debug_pc', 'mshrs_0.io.brupdate.b2.uop.debug_tsrc', 'mshrs_0.io.brupdate.b2.uop.dis_col_sel', 'mshrs_0.io.brupdate.b2.uop.dst_rtype', 'mshrs_0.io.brupdate.b2.uop.edge_inst', 'mshrs_0.io.brupdate.b2.uop.exc_cause', 'mshrs_0.io.brupdate.b2.uop.exception', 'mshrs_0.io.brupdate.b2.uop.fcn_dw', 'mshrs_0.io.brupdate.b2.uop.fcn_op', 'mshrs_0.io.brupdate.b2.uop.flush_on_commit', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.div', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fma', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.fromint', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ldst', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren1', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren2', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren3', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.sqrt', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap12', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap23', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.toint', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.vec', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.wen', 'mshrs_0.io.brupdate.b2.uop.fp_ctrl.wflags', 'mshrs_0.io.brupdate.b2.uop.fp_rm', 'mshrs_0.io.brupdate.b2.uop.fp_typ', 'mshrs_0.io.brupdate.b2.uop.fp_val', 'mshrs_0.io.brupdate.b2.uop.frs3_en', 'mshrs_0.io.brupdate.b2.uop.ftq_idx', 'mshrs_0.io.brupdate.b2.uop.fu_code[0]', 'mshrs_0.io.brupdate.b2.uop.fu_code[1]', 'mshrs_0.io.brupdate.b2.uop.fu_code[2]', 'mshrs_0.io.brupdate.b2.uop.fu_code[3]', 'mshrs_0.io.brupdate.b2.uop.fu_code[4]', 'mshrs_0.io.brupdate.b2.uop.fu_code[5]', 'mshrs_0.io.brupdate.b2.uop.fu_code[6]', 'mshrs_0.io.brupdate.b2.uop.fu_code[7]', 'mshrs_0.io.brupdate.b2.uop.fu_code[8]', 'mshrs_0.io.brupdate.b2.uop.fu_code[9]', 'mshrs_0.io.brupdate.b2.uop.imm_packed', 'mshrs_0.io.brupdate.b2.uop.imm_rename', 'mshrs_0.io.brupdate.b2.uop.imm_sel', 'mshrs_0.io.brupdate.b2.uop.inst', 'mshrs_0.io.brupdate.b2.uop.iq_type[0]', 'mshrs_0.io.brupdate.b2.uop.iq_type[1]', 'mshrs_0.io.brupdate.b2.uop.iq_type[2]', 'mshrs_0.io.brupdate.b2.uop.iq_type[3]', 'mshrs_0.io.brupdate.b2.uop.is_amo', 'mshrs_0.io.brupdate.b2.uop.is_eret', 'mshrs_0.io.brupdate.b2.uop.is_fence', 'mshrs_0.io.brupdate.b2.uop.is_fencei', 'mshrs_0.io.brupdate.b2.uop.is_mov', 'mshrs_0.io.brupdate.b2.uop.is_rocc', 'mshrs_0.io.brupdate.b2.uop.is_rvc', 'mshrs_0.io.brupdate.b2.uop.is_sfb', 'mshrs_0.io.brupdate.b2.uop.is_sfence', 'mshrs_0.io.brupdate.b2.uop.is_sys_pc2epc', 'mshrs_0.io.brupdate.b2.uop.is_unique', 'mshrs_0.io.brupdate.b2.uop.iw_issued', 'mshrs_0.io.brupdate.b2.uop.iw_issued_partial_agen', 'mshrs_0.io.brupdate.b2.uop.iw_issued_partial_dgen', 'mshrs_0.io.brupdate.b2.uop.iw_p1_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.iw_p1_speculative_child', 'mshrs_0.io.brupdate.b2.uop.iw_p2_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.iw_p2_speculative_child', 'mshrs_0.io.brupdate.b2.uop.iw_p3_bypass_hint', 'mshrs_0.io.brupdate.b2.uop.ldq_idx', 'mshrs_0.io.brupdate.b2.uop.ldst', 'mshrs_0.io.brupdate.b2.uop.ldst_is_rs1', 'mshrs_0.io.brupdate.b2.uop.lrs1', 'mshrs_0.io.brupdate.b2.uop.lrs1_rtype', 'mshrs_0.io.brupdate.b2.uop.lrs2', 'mshrs_0.io.brupdate.b2.uop.lrs2_rtype', 'mshrs_0.io.brupdate.b2.uop.lrs3', 'mshrs_0.io.brupdate.b2.uop.mem_cmd', 'mshrs_0.io.brupdate.b2.uop.mem_signed', 'mshrs_0.io.brupdate.b2.uop.mem_size', 'mshrs_0.io.brupdate.b2.uop.op1_sel', 'mshrs_0.io.brupdate.b2.uop.op2_sel', 'mshrs_0.io.brupdate.b2.uop.pc_lob', 'mshrs_0.io.brupdate.b2.uop.pdst', 'mshrs_0.io.brupdate.b2.uop.pimm', 'mshrs_0.io.brupdate.b2.uop.ppred', 'mshrs_0.io.brupdate.b2.uop.ppred_busy', 'mshrs_0.io.brupdate.b2.uop.prs1', 'mshrs_0.io.brupdate.b2.uop.prs1_busy', 'mshrs_0.io.brupdate.b2.uop.prs2', 'mshrs_0.io.brupdate.b2.uop.prs2_busy', 'mshrs_0.io.brupdate.b2.uop.prs3', 'mshrs_0.io.brupdate.b2.uop.prs3_busy', 'mshrs_0.io.brupdate.b2.uop.rob_idx', 'mshrs_0.io.brupdate.b2.uop.rxq_idx', 'mshrs_0.io.brupdate.b2.uop.stale_pdst', 'mshrs_0.io.brupdate.b2.uop.stq_idx', 'mshrs_0.io.brupdate.b2.uop.taken', 'mshrs_0.io.brupdate.b2.uop.uses_ldq', 'mshrs_0.io.brupdate.b2.uop.uses_stq', 'mshrs_0.io.brupdate.b2.uop.xcpt_ae_if', 'mshrs_0.io.brupdate.b2.uop.xcpt_ma_if', 'mshrs_0.io.brupdate.b2.uop.xcpt_pf_if', 'mshrs_0.io.clear_prefetch', 'mshrs_0.io.commit_addr', 'mshrs_0.io.commit_coh.state', 'mshrs_0.io.commit_val', 'mshrs_0.io.exception', 'mshrs_0.io.id', 'mshrs_0.io.idx.bits', 'mshrs_0.io.idx.valid', 'mshrs_0.io.lb_read.offset', 'mshrs_0.io.lb_resp', 'mshrs_0.io.lb_write.bits.data', 'mshrs_0.io.lb_write.bits.offset', 'mshrs_0.io.lb_write.valid', 'mshrs_0.io.mem_acquire.bits.address', 'mshrs_0.io.mem_acquire.bits.corrupt', 'mshrs_0.io.mem_acquire.bits.data', 'mshrs_0.io.mem_acquire.bits.mask', 'mshrs_0.io.mem_acquire.bits.opcode', 'mshrs_0.io.mem_acquire.bits.param', 'mshrs_0.io.mem_acquire.bits.size', 'mshrs_0.io.mem_acquire.bits.source', 'mshrs_0.io.mem_acquire.ready', 'mshrs_0.io.mem_acquire.valid', 'mshrs_0.io.mem_finish.bits.sink', 'mshrs_0.io.mem_finish.ready', 'mshrs_0.io.mem_finish.valid', 'mshrs_0.io.mem_grant.bits.corrupt', 'mshrs_0.io.mem_grant.bits.data', 'mshrs_0.io.mem_grant.bits.denied', 'mshrs_0.io.mem_grant.bits.opcode', 'mshrs_0.io.mem_grant.bits.param', 'mshrs_0.io.mem_grant.bits.sink', 'mshrs_0.io.mem_grant.bits.size', 'mshrs_0.io.mem_grant.bits.source', 'mshrs_0.io.mem_grant.ready', 'mshrs_0.io.mem_grant.valid', 'mshrs_0.io.meta_read.bits.idx', 'mshrs_0.io.meta_read.bits.tag', 'mshrs_0.io.meta_read.bits.way_en', 'mshrs_0.io.meta_read.ready', 'mshrs_0.io.meta_read.valid', 'mshrs_0.io.meta_resp.bits.coh.state', 'mshrs_0.io.meta_resp.bits.tag', 'mshrs_0.io.meta_resp.valid', 'mshrs_0.io.meta_write.bits.data.coh.state', 'mshrs_0.io.meta_write.bits.data.tag', 'mshrs_0.io.meta_write.bits.idx', 'mshrs_0.io.meta_write.bits.tag', 'mshrs_0.io.meta_write.bits.way_en', 'mshrs_0.io.meta_write.ready', 'mshrs_0.io.meta_write.valid', 'mshrs_0.io.probe_rdy', 'mshrs_0.io.prober_state.bits', 'mshrs_0.io.prober_state.valid', 'mshrs_0.io.refill.bits.addr', 'mshrs_0.io.refill.bits.data', 'mshrs_0.io.refill.bits.way_en', 'mshrs_0.io.refill.bits.wmask', 'mshrs_0.io.refill.ready', 'mshrs_0.io.refill.valid', 'mshrs_0.io.replay.bits.addr', 'mshrs_0.io.replay.bits.data', 'mshrs_0.io.replay.bits.is_hella', 'mshrs_0.io.replay.bits.old_meta.coh.state', 'mshrs_0.io.replay.bits.old_meta.tag', 'mshrs_0.io.replay.bits.sdq_id', 'mshrs_0.io.replay.bits.tag_match', 'mshrs_0.io.replay.bits.uop.bp_debug_if', 'mshrs_0.io.replay.bits.uop.bp_xcpt_if', 'mshrs_0.io.replay.bits.uop.br_mask', 'mshrs_0.io.replay.bits.uop.br_tag', 'mshrs_0.io.replay.bits.uop.br_type', 'mshrs_0.io.replay.bits.uop.csr_cmd', 'mshrs_0.io.replay.bits.uop.debug_fsrc', 'mshrs_0.io.replay.bits.uop.debug_inst', 'mshrs_0.io.replay.bits.uop.debug_pc', 'mshrs_0.io.replay.bits.uop.debug_tsrc', 'mshrs_0.io.replay.bits.uop.dis_col_sel', 'mshrs_0.io.replay.bits.uop.dst_rtype', 'mshrs_0.io.replay.bits.uop.edge_inst', 'mshrs_0.io.replay.bits.uop.exc_cause', 'mshrs_0.io.replay.bits.uop.exception', 'mshrs_0.io.replay.bits.uop.fcn_dw', 'mshrs_0.io.replay.bits.uop.fcn_op', 'mshrs_0.io.replay.bits.uop.flush_on_commit', 'mshrs_0.io.replay.bits.uop.fp_ctrl.div', 'mshrs_0.io.replay.bits.uop.fp_ctrl.fastpipe', 'mshrs_0.io.replay.bits.uop.fp_ctrl.fma', 'mshrs_0.io.replay.bits.uop.fp_ctrl.fromint', 'mshrs_0.io.replay.bits.uop.fp_ctrl.ldst', 'mshrs_0.io.replay.bits.uop.fp_ctrl.ren1', 'mshrs_0.io.replay.bits.uop.fp_ctrl.ren2', 'mshrs_0.io.replay.bits.uop.fp_ctrl.ren3', 'mshrs_0.io.replay.bits.uop.fp_ctrl.sqrt', 'mshrs_0.io.replay.bits.uop.fp_ctrl.swap12', 'mshrs_0.io.replay.bits.uop.fp_ctrl.swap23', 'mshrs_0.io.replay.bits.uop.fp_ctrl.toint', 'mshrs_0.io.replay.bits.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.replay.bits.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.replay.bits.uop.fp_ctrl.vec', 'mshrs_0.io.replay.bits.uop.fp_ctrl.wen', 'mshrs_0.io.replay.bits.uop.fp_ctrl.wflags', 'mshrs_0.io.replay.bits.uop.fp_rm', 'mshrs_0.io.replay.bits.uop.fp_typ', 'mshrs_0.io.replay.bits.uop.fp_val', 'mshrs_0.io.replay.bits.uop.frs3_en', 'mshrs_0.io.replay.bits.uop.ftq_idx', 'mshrs_0.io.replay.bits.uop.fu_code[0]', 'mshrs_0.io.replay.bits.uop.fu_code[1]', 'mshrs_0.io.replay.bits.uop.fu_code[2]', 'mshrs_0.io.replay.bits.uop.fu_code[3]', 'mshrs_0.io.replay.bits.uop.fu_code[4]', 'mshrs_0.io.replay.bits.uop.fu_code[5]', 'mshrs_0.io.replay.bits.uop.fu_code[6]', 'mshrs_0.io.replay.bits.uop.fu_code[7]', 'mshrs_0.io.replay.bits.uop.fu_code[8]', 'mshrs_0.io.replay.bits.uop.fu_code[9]', 'mshrs_0.io.replay.bits.uop.imm_packed', 'mshrs_0.io.replay.bits.uop.imm_rename', 'mshrs_0.io.replay.bits.uop.imm_sel', 'mshrs_0.io.replay.bits.uop.inst', 'mshrs_0.io.replay.bits.uop.iq_type[0]', 'mshrs_0.io.replay.bits.uop.iq_type[1]', 'mshrs_0.io.replay.bits.uop.iq_type[2]', 'mshrs_0.io.replay.bits.uop.iq_type[3]', 'mshrs_0.io.replay.bits.uop.is_amo', 'mshrs_0.io.replay.bits.uop.is_eret', 'mshrs_0.io.replay.bits.uop.is_fence', 'mshrs_0.io.replay.bits.uop.is_fencei', 'mshrs_0.io.replay.bits.uop.is_mov', 'mshrs_0.io.replay.bits.uop.is_rocc', 'mshrs_0.io.replay.bits.uop.is_rvc', 'mshrs_0.io.replay.bits.uop.is_sfb', 'mshrs_0.io.replay.bits.uop.is_sfence', 'mshrs_0.io.replay.bits.uop.is_sys_pc2epc', 'mshrs_0.io.replay.bits.uop.is_unique', 'mshrs_0.io.replay.bits.uop.iw_issued', 'mshrs_0.io.replay.bits.uop.iw_issued_partial_agen', 'mshrs_0.io.replay.bits.uop.iw_issued_partial_dgen', 'mshrs_0.io.replay.bits.uop.iw_p1_bypass_hint', 'mshrs_0.io.replay.bits.uop.iw_p1_speculative_child', 'mshrs_0.io.replay.bits.uop.iw_p2_bypass_hint', 'mshrs_0.io.replay.bits.uop.iw_p2_speculative_child', 'mshrs_0.io.replay.bits.uop.iw_p3_bypass_hint', 'mshrs_0.io.replay.bits.uop.ldq_idx', 'mshrs_0.io.replay.bits.uop.ldst', 'mshrs_0.io.replay.bits.uop.ldst_is_rs1', 'mshrs_0.io.replay.bits.uop.lrs1', 'mshrs_0.io.replay.bits.uop.lrs1_rtype', 'mshrs_0.io.replay.bits.uop.lrs2', 'mshrs_0.io.replay.bits.uop.lrs2_rtype', 'mshrs_0.io.replay.bits.uop.lrs3', 'mshrs_0.io.replay.bits.uop.mem_cmd', 'mshrs_0.io.replay.bits.uop.mem_signed', 'mshrs_0.io.replay.bits.uop.mem_size', 'mshrs_0.io.replay.bits.uop.op1_sel', 'mshrs_0.io.replay.bits.uop.op2_sel', 'mshrs_0.io.replay.bits.uop.pc_lob', 'mshrs_0.io.replay.bits.uop.pdst', 'mshrs_0.io.replay.bits.uop.pimm', 'mshrs_0.io.replay.bits.uop.ppred', 'mshrs_0.io.replay.bits.uop.ppred_busy', 'mshrs_0.io.replay.bits.uop.prs1', 'mshrs_0.io.replay.bits.uop.prs1_busy', 'mshrs_0.io.replay.bits.uop.prs2', 'mshrs_0.io.replay.bits.uop.prs2_busy', 'mshrs_0.io.replay.bits.uop.prs3', 'mshrs_0.io.replay.bits.uop.prs3_busy', 'mshrs_0.io.replay.bits.uop.rob_idx', 'mshrs_0.io.replay.bits.uop.rxq_idx', 'mshrs_0.io.replay.bits.uop.stale_pdst', 'mshrs_0.io.replay.bits.uop.stq_idx', 'mshrs_0.io.replay.bits.uop.taken', 'mshrs_0.io.replay.bits.uop.uses_ldq', 'mshrs_0.io.replay.bits.uop.uses_stq', 'mshrs_0.io.replay.bits.uop.xcpt_ae_if', 'mshrs_0.io.replay.bits.uop.xcpt_ma_if', 'mshrs_0.io.replay.bits.uop.xcpt_pf_if', 'mshrs_0.io.replay.bits.way_en', 'mshrs_0.io.replay.ready', 'mshrs_0.io.replay.valid', 'mshrs_0.io.req.addr', 'mshrs_0.io.req.data', 'mshrs_0.io.req.is_hella', 'mshrs_0.io.req.old_meta.coh.state', 'mshrs_0.io.req.old_meta.tag', 'mshrs_0.io.req.sdq_id', 'mshrs_0.io.req.tag_match', 'mshrs_0.io.req.uop.bp_debug_if', 'mshrs_0.io.req.uop.bp_xcpt_if', 'mshrs_0.io.req.uop.br_mask', 'mshrs_0.io.req.uop.br_tag', 'mshrs_0.io.req.uop.br_type', 'mshrs_0.io.req.uop.csr_cmd', 'mshrs_0.io.req.uop.debug_fsrc', 'mshrs_0.io.req.uop.debug_inst', 'mshrs_0.io.req.uop.debug_pc', 'mshrs_0.io.req.uop.debug_tsrc', 'mshrs_0.io.req.uop.dis_col_sel', 'mshrs_0.io.req.uop.dst_rtype', 'mshrs_0.io.req.uop.edge_inst', 'mshrs_0.io.req.uop.exc_cause', 'mshrs_0.io.req.uop.exception', 'mshrs_0.io.req.uop.fcn_dw', 'mshrs_0.io.req.uop.fcn_op', 'mshrs_0.io.req.uop.flush_on_commit', 'mshrs_0.io.req.uop.fp_ctrl.div', 'mshrs_0.io.req.uop.fp_ctrl.fastpipe', 'mshrs_0.io.req.uop.fp_ctrl.fma', 'mshrs_0.io.req.uop.fp_ctrl.fromint', 'mshrs_0.io.req.uop.fp_ctrl.ldst', 'mshrs_0.io.req.uop.fp_ctrl.ren1', 'mshrs_0.io.req.uop.fp_ctrl.ren2', 'mshrs_0.io.req.uop.fp_ctrl.ren3', 'mshrs_0.io.req.uop.fp_ctrl.sqrt', 'mshrs_0.io.req.uop.fp_ctrl.swap12', 'mshrs_0.io.req.uop.fp_ctrl.swap23', 'mshrs_0.io.req.uop.fp_ctrl.toint', 'mshrs_0.io.req.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.req.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.req.uop.fp_ctrl.vec', 'mshrs_0.io.req.uop.fp_ctrl.wen', 'mshrs_0.io.req.uop.fp_ctrl.wflags', 'mshrs_0.io.req.uop.fp_rm', 'mshrs_0.io.req.uop.fp_typ', 'mshrs_0.io.req.uop.fp_val', 'mshrs_0.io.req.uop.frs3_en', 'mshrs_0.io.req.uop.ftq_idx', 'mshrs_0.io.req.uop.fu_code[0]', 'mshrs_0.io.req.uop.fu_code[1]', 'mshrs_0.io.req.uop.fu_code[2]', 'mshrs_0.io.req.uop.fu_code[3]', 'mshrs_0.io.req.uop.fu_code[4]', 'mshrs_0.io.req.uop.fu_code[5]', 'mshrs_0.io.req.uop.fu_code[6]', 'mshrs_0.io.req.uop.fu_code[7]', 'mshrs_0.io.req.uop.fu_code[8]', 'mshrs_0.io.req.uop.fu_code[9]', 'mshrs_0.io.req.uop.imm_packed', 'mshrs_0.io.req.uop.imm_rename', 'mshrs_0.io.req.uop.imm_sel', 'mshrs_0.io.req.uop.inst', 'mshrs_0.io.req.uop.iq_type[0]', 'mshrs_0.io.req.uop.iq_type[1]', 'mshrs_0.io.req.uop.iq_type[2]', 'mshrs_0.io.req.uop.iq_type[3]', 'mshrs_0.io.req.uop.is_amo', 'mshrs_0.io.req.uop.is_eret', 'mshrs_0.io.req.uop.is_fence', 'mshrs_0.io.req.uop.is_fencei', 'mshrs_0.io.req.uop.is_mov', 'mshrs_0.io.req.uop.is_rocc', 'mshrs_0.io.req.uop.is_rvc', 'mshrs_0.io.req.uop.is_sfb', 'mshrs_0.io.req.uop.is_sfence', 'mshrs_0.io.req.uop.is_sys_pc2epc', 'mshrs_0.io.req.uop.is_unique', 'mshrs_0.io.req.uop.iw_issued', 'mshrs_0.io.req.uop.iw_issued_partial_agen', 'mshrs_0.io.req.uop.iw_issued_partial_dgen', 'mshrs_0.io.req.uop.iw_p1_bypass_hint', 'mshrs_0.io.req.uop.iw_p1_speculative_child', 'mshrs_0.io.req.uop.iw_p2_bypass_hint', 'mshrs_0.io.req.uop.iw_p2_speculative_child', 'mshrs_0.io.req.uop.iw_p3_bypass_hint', 'mshrs_0.io.req.uop.ldq_idx', 'mshrs_0.io.req.uop.ldst', 'mshrs_0.io.req.uop.ldst_is_rs1', 'mshrs_0.io.req.uop.lrs1', 'mshrs_0.io.req.uop.lrs1_rtype', 'mshrs_0.io.req.uop.lrs2', 'mshrs_0.io.req.uop.lrs2_rtype', 'mshrs_0.io.req.uop.lrs3', 'mshrs_0.io.req.uop.mem_cmd', 'mshrs_0.io.req.uop.mem_signed', 'mshrs_0.io.req.uop.mem_size', 'mshrs_0.io.req.uop.op1_sel', 'mshrs_0.io.req.uop.op2_sel', 'mshrs_0.io.req.uop.pc_lob', 'mshrs_0.io.req.uop.pdst', 'mshrs_0.io.req.uop.pimm', 'mshrs_0.io.req.uop.ppred', 'mshrs_0.io.req.uop.ppred_busy', 'mshrs_0.io.req.uop.prs1', 'mshrs_0.io.req.uop.prs1_busy', 'mshrs_0.io.req.uop.prs2', 'mshrs_0.io.req.uop.prs2_busy', 'mshrs_0.io.req.uop.prs3', 'mshrs_0.io.req.uop.prs3_busy', 'mshrs_0.io.req.uop.rob_idx', 'mshrs_0.io.req.uop.rxq_idx', 'mshrs_0.io.req.uop.stale_pdst', 'mshrs_0.io.req.uop.stq_idx', 'mshrs_0.io.req.uop.taken', 'mshrs_0.io.req.uop.uses_ldq', 'mshrs_0.io.req.uop.uses_stq', 'mshrs_0.io.req.uop.xcpt_ae_if', 'mshrs_0.io.req.uop.xcpt_ma_if', 'mshrs_0.io.req.uop.xcpt_pf_if', 'mshrs_0.io.req.way_en', 'mshrs_0.io.req_is_probe', 'mshrs_0.io.req_pri_rdy', 'mshrs_0.io.req_pri_val', 'mshrs_0.io.req_sec_rdy', 'mshrs_0.io.req_sec_val', 'mshrs_0.io.resp.bits.data', 'mshrs_0.io.resp.bits.is_hella', 'mshrs_0.io.resp.bits.uop.bp_debug_if', 'mshrs_0.io.resp.bits.uop.bp_xcpt_if', 'mshrs_0.io.resp.bits.uop.br_mask', 'mshrs_0.io.resp.bits.uop.br_tag', 'mshrs_0.io.resp.bits.uop.br_type', 'mshrs_0.io.resp.bits.uop.csr_cmd', 'mshrs_0.io.resp.bits.uop.debug_fsrc', 'mshrs_0.io.resp.bits.uop.debug_inst', 'mshrs_0.io.resp.bits.uop.debug_pc', 'mshrs_0.io.resp.bits.uop.debug_tsrc', 'mshrs_0.io.resp.bits.uop.dis_col_sel', 'mshrs_0.io.resp.bits.uop.dst_rtype', 'mshrs_0.io.resp.bits.uop.edge_inst', 'mshrs_0.io.resp.bits.uop.exc_cause', 'mshrs_0.io.resp.bits.uop.exception', 'mshrs_0.io.resp.bits.uop.fcn_dw', 'mshrs_0.io.resp.bits.uop.fcn_op', 'mshrs_0.io.resp.bits.uop.flush_on_commit', 'mshrs_0.io.resp.bits.uop.fp_ctrl.div', 'mshrs_0.io.resp.bits.uop.fp_ctrl.fastpipe', 'mshrs_0.io.resp.bits.uop.fp_ctrl.fma', 'mshrs_0.io.resp.bits.uop.fp_ctrl.fromint', 'mshrs_0.io.resp.bits.uop.fp_ctrl.ldst', 'mshrs_0.io.resp.bits.uop.fp_ctrl.ren1', 'mshrs_0.io.resp.bits.uop.fp_ctrl.ren2', 'mshrs_0.io.resp.bits.uop.fp_ctrl.ren3', 'mshrs_0.io.resp.bits.uop.fp_ctrl.sqrt', 'mshrs_0.io.resp.bits.uop.fp_ctrl.swap12', 'mshrs_0.io.resp.bits.uop.fp_ctrl.swap23', 'mshrs_0.io.resp.bits.uop.fp_ctrl.toint', 'mshrs_0.io.resp.bits.uop.fp_ctrl.typeTagIn', 'mshrs_0.io.resp.bits.uop.fp_ctrl.typeTagOut', 'mshrs_0.io.resp.bits.uop.fp_ctrl.vec', 'mshrs_0.io.resp.bits.uop.fp_ctrl.wen', 'mshrs_0.io.resp.bits.uop.fp_ctrl.wflags', 'mshrs_0.io.resp.bits.uop.fp_rm', 'mshrs_0.io.resp.bits.uop.fp_typ', 'mshrs_0.io.resp.bits.uop.fp_val', 'mshrs_0.io.resp.bits.uop.frs3_en', 'mshrs_0.io.resp.bits.uop.ftq_idx', 'mshrs_0.io.resp.bits.uop.fu_code[0]', 'mshrs_0.io.resp.bits.uop.fu_code[1]', 'mshrs_0.io.resp.bits.uop.fu_code[2]', 'mshrs_0.io.resp.bits.uop.fu_code[3]', 'mshrs_0.io.resp.bits.uop.fu_code[4]', 'mshrs_0.io.resp.bits.uop.fu_code[5]', 'mshrs_0.io.resp.bits.uop.fu_code[6]', 'mshrs_0.io.resp.bits.uop.fu_code[7]', 'mshrs_0.io.resp.bits.uop.fu_code[8]', 'mshrs_0.io.resp.bits.uop.fu_code[9]', 'mshrs_0.io.resp.bits.uop.imm_packed', 'mshrs_0.io.resp.bits.uop.imm_rename', 'mshrs_0.io.resp.bits.uop.imm_sel', 'mshrs_0.io.resp.bits.uop.inst', 'mshrs_0.io.resp.bits.uop.iq_type[0]', 'mshrs_0.io.resp.bits.uop.iq_type[1]', 'mshrs_0.io.resp.bits.uop.iq_type[2]', 'mshrs_0.io.resp.bits.uop.iq_type[3]', 'mshrs_0.io.resp.bits.uop.is_amo', 'mshrs_0.io.resp.bits.uop.is_eret', 'mshrs_0.io.resp.bits.uop.is_fence', 'mshrs_0.io.resp.bits.uop.is_fencei', 'mshrs_0.io.resp.bits.uop.is_mov', 'mshrs_0.io.resp.bits.uop.is_rocc', 'mshrs_0.io.resp.bits.uop.is_rvc', 'mshrs_0.io.resp.bits.uop.is_sfb', 'mshrs_0.io.resp.bits.uop.is_sfence', 'mshrs_0.io.resp.bits.uop.is_sys_pc2epc', 'mshrs_0.io.resp.bits.uop.is_unique', 'mshrs_0.io.resp.bits.uop.iw_issued', 'mshrs_0.io.resp.bits.uop.iw_issued_partial_agen', 'mshrs_0.io.resp.bits.uop.iw_issued_partial_dgen', 'mshrs_0.io.resp.bits.uop.iw_p1_bypass_hint', 'mshrs_0.io.resp.bits.uop.iw_p1_speculative_child', 'mshrs_0.io.resp.bits.uop.iw_p2_bypass_hint', 'mshrs_0.io.resp.bits.uop.iw_p2_speculative_child', 'mshrs_0.io.resp.bits.uop.iw_p3_bypass_hint', 'mshrs_0.io.resp.bits.uop.ldq_idx', 'mshrs_0.io.resp.bits.uop.ldst', 'mshrs_0.io.resp.bits.uop.ldst_is_rs1', 'mshrs_0.io.resp.bits.uop.lrs1', 'mshrs_0.io.resp.bits.uop.lrs1_rtype', 'mshrs_0.io.resp.bits.uop.lrs2', 'mshrs_0.io.resp.bits.uop.lrs2_rtype', 'mshrs_0.io.resp.bits.uop.lrs3', 'mshrs_0.io.resp.bits.uop.mem_cmd', 'mshrs_0.io.resp.bits.uop.mem_signed', 'mshrs_0.io.resp.bits.uop.mem_size', 'mshrs_0.io.resp.bits.uop.op1_sel', 'mshrs_0.io.resp.bits.uop.op2_sel', 'mshrs_0.io.resp.bits.uop.pc_lob', 'mshrs_0.io.resp.bits.uop.pdst', 'mshrs_0.io.resp.bits.uop.pimm', 'mshrs_0.io.resp.bits.uop.ppred', 'mshrs_0.io.resp.bits.uop.ppred_busy', 'mshrs_0.io.resp.bits.uop.prs1', 'mshrs_0.io.resp.bits.uop.prs1_busy', 'mshrs_0.io.resp.bits.uop.prs2', 'mshrs_0.io.resp.bits.uop.prs2_busy', 'mshrs_0.io.resp.bits.uop.prs3', 'mshrs_0.io.resp.bits.uop.prs3_busy', 'mshrs_0.io.resp.bits.uop.rob_idx', 'mshrs_0.io.resp.bits.uop.rxq_idx', 'mshrs_0.io.resp.bits.uop.stale_pdst', 'mshrs_0.io.resp.bits.uop.stq_idx', 'mshrs_0.io.resp.bits.uop.taken', 'mshrs_0.io.resp.bits.uop.uses_ldq', 'mshrs_0.io.resp.bits.uop.uses_stq', 'mshrs_0.io.resp.bits.uop.xcpt_ae_if', 'mshrs_0.io.resp.bits.uop.xcpt_ma_if', 'mshrs_0.io.resp.bits.uop.xcpt_pf_if', 'mshrs_0.io.resp.ready', 'mshrs_0.io.resp.valid', 'mshrs_0.io.rob_head_idx', 'mshrs_0.io.rob_pnr_idx', 'mshrs_0.io.tag.bits', 'mshrs_0.io.tag.valid', 'mshrs_0.io.way.bits', 'mshrs_0.io.way.valid', 'mshrs_0.io.wb_req.bits.idx', 'mshrs_0.io.wb_req.bits.param', 'mshrs_0.io.wb_req.bits.source', 'mshrs_0.io.wb_req.bits.tag', 'mshrs_0.io.wb_req.bits.voluntary', 'mshrs_0.io.wb_req.bits.way_en', 'mshrs_0.io.wb_req.ready', 'mshrs_0.io.wb_req.valid', 'mshrs_0.io.wb_resp', 'mshrs_0.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.mshrs_0.rpq.main::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A13": {
      "local_id": "A13",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A14": {
      "local_id": "A14",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A15": {
      "local_id": "A15",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    }
  },
  "cases": {
    "BoomMSHRFile.mshrs_0.rpq.main::C1_Admitted": {
      "local_id": "C1_Admitted",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::C2_BranchKilledOnArrival": {
      "local_id": "C2_BranchKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::C3_FlushKilledOnArrival": {
      "local_id": "C3_FlushKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::C4_VisibleDequeue": {
      "local_id": "C4_VisibleDequeue",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::C5_InvalidHeadSkip": {
      "local_id": "C5_InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq::C1_EnqueueForwarded": {
      "local_id": "C1_EnqueueForwarded",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::C2_ChildDequeueCaptured": {
      "local_id": "C2_ChildDequeueCaptured",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::C3_ChildDequeueBranchKilled": {
      "local_id": "C3_ChildDequeueBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::C4_ChildDequeueFlushKilled": {
      "local_id": "C4_ChildDequeueFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::C5_VisibleParentDequeue": {
      "local_id": "C5_VisibleParentDequeue",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0::C1_GrantCompleted": {
      "local_id": "C1_GrantCompleted",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C2_LoadResponse": {
      "local_id": "C2_LoadResponse",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C3_VictimWriteback": {
      "local_id": "C3_VictimWriteback",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C4_CommitLineRefill": {
      "local_id": "C4_CommitLineRefill",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C5_ReplayDrain": {
      "local_id": "C5_ReplayDrain",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C6_FinalMetadataCommit": {
      "local_id": "C6_FinalMetadataCommit",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::C7_GrantFinish": {
      "local_id": "C7_GrantFinish",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake": {
      "local_id": "DeqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake": {
      "local_id": "EnqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::InvalidHeadSkip": {
      "local_id": "InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert": {
      "local_id": "QueueInsert",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq::BufferCapture": {
      "local_id": "BufferCapture",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::ParentDeqHandshake": {
      "local_id": "ParentDeqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::ParentEnqHandshake": {
      "local_id": "ParentEnqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0::CommitRefillBeat": {
      "local_id": "CommitRefillBeat",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::CommitRefillDone": {
      "local_id": "CommitRefillDone",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::FinalMetaWrite": {
      "local_id": "FinalMetaWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::GrantComplete": {
      "local_id": "GrantComplete",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::GrantDataWrite": {
      "local_id": "GrantDataWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::MemAcquire": {
      "local_id": "MemAcquire",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::MemFinish": {
      "local_id": "MemFinish",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::MemGrant": {
      "local_id": "MemGrant",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::MetaClearWrite": {
      "local_id": "MetaClearWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::MetaRead": {
      "local_id": "MetaRead",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::PrimaryAccept": {
      "local_id": "PrimaryAccept",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::RPQDrained": {
      "local_id": "RPQDrained",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::ReplayHandshake": {
      "local_id": "ReplayHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::RespHandshake": {
      "local_id": "RespHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::WBComplete": {
      "local_id": "WBComplete",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    },
    "BoomMSHRFile.mshrs_0::WBReq": {
      "local_id": "WBReq",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
    }
  },
  "predicates": {
    "BoomMSHRFile.mshrs_0.rpq.main::HeadInvalid": {
      "local_id": "HeadInvalid",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::HeadValid": {
      "local_id": "HeadValid",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::IncomingBranchKilled": {
      "local_id": "IncomingBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::IncomingFlushKilled": {
      "local_id": "IncomingFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::QueueEmpty": {
      "local_id": "QueueEmpty",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq.main::QueueFull": {
      "local_id": "QueueFull",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
    },
    "BoomMSHRFile.mshrs_0.rpq::OutputInvalid": {
      "local_id": "OutputInvalid",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::TransferBranchKilled": {
      "local_id": "TransferBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0.rpq::TransferFlushKilled": {
      "local_id": "TransferFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
    },
    "BoomMSHRFile.mshrs_0::GrantAckAbsent": {
      "local_id": "GrantAckAbsent",
      "work_unit_id": "BoomMSHRFile.mshrs_0"
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
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1102,
        1104,
        1106,
        1107,
        1119,
        1346,
        1348,
        1350,
        1351,
        1352,
        1353,
        1840,
        1842,
        1974,
        1975,
        1988,
        2215
      ],
      "formal": {
        "after": "MemAcquire",
        "before": "PrimaryAccept",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A1",
      "rendered_formula": "PrimaryAccept <mu MemAcquire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1348,
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364
      ],
      "formal": {
        "after": "MemGrant",
        "before": "MemAcquire",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A2",
      "rendered_formula": "MemAcquire <mu MemGrant",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1444,
        1455,
        1456,
        1459,
        1460
      ],
      "formal": {
        "after": "RespHandshake",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A3",
      "rendered_formula": "GrantComplete <mu RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1525,
        1526,
        1533,
        1534,
        1535,
        1536
      ],
      "formal": {
        "after": "MetaRead",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A4",
      "rendered_formula": "GrantComplete <mu MetaRead",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_VictimWriteback"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "formal": {
        "scope_identity": null,
        "scope_index": null,
        "sequence": [
          "MetaRead",
          "MetaClearWrite",
          "WBReq",
          "WBComplete"
        ],
        "type": "ordered_chain"
      },
      "id": "A5",
      "rendered_formula": "MetaRead <mu MetaClearWrite <mu WBReq <mu WBComplete",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1637,
        1640,
        1641,
        1642
      ],
      "formal": {
        "after": "CommitRefillBeat",
        "before": "MetaRead",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A6",
      "rendered_formula": "MetaRead <mu CommitRefillBeat",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1111,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648,
        1980
      ],
      "formal": {
        "cardinality": "exactly_once",
        "completion": "CommitRefillDone",
        "domain": {
          "end_exclusive": 8,
          "start": 0
        },
        "index": "beat",
        "occurrence": "CommitRefillBeat",
        "scope_identity": null,
        "scope_index": null,
        "type": "indexed_complete"
      },
      "id": "A7",
      "rendered_formula": "CommitRefillDone => forall beat in [0, 8): count(CommitRefillBeat(beat)) = 1",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C6_FinalMetadataCommit"
      ],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "formal": {
        "after": "FinalMetaWrite",
        "before": "RPQDrained",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A8",
      "rendered_formula": "RPQDrained <mu FinalMetaWrite",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1367,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "formal": {
        "after": "MemFinish",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A9",
      "rendered_formula": "GrantComplete <mu MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1825,
        1827,
        1828,
        1829,
        1830,
        1831,
        1832
      ],
      "formal": {
        "occurrence": "MemFinish",
        "predicate": "GrantAckAbsent",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A10",
      "rendered_formula": "GrantAckAbsent => !MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1093,
        1358,
        1359,
        1360
      ],
      "formal": {
        "on": "GrantDataWrite",
        "scope_identity": null,
        "source": {
          "name": "io.mem_grant.bits.data",
          "op": "signal"
        },
        "target": "io.lb_write.bits.data",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.lb_write.bits.data = io.mem_grant.bits.data on GrantDataWrite",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1067,
        1637,
        1640,
        1641
      ],
      "formal": {
        "on": "CommitRefillBeat",
        "scope_identity": null,
        "source": {
          "name": "io.lb_resp",
          "op": "signal"
        },
        "target": "io.refill.bits.data",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.refill.bits.data = io.lb_resp on CommitRefillBeat",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1089,
        1374,
        1375,
        1827,
        1828
      ],
      "formal": {
        "on": "MemFinish",
        "scope_identity": null,
        "source": {
          "name": "grantack.bits.sink",
          "op": "signal"
        },
        "target": "io.mem_finish.bits.sink",
        "type": "signal_equality"
      },
      "id": "A13",
      "rendered_formula": "io.mem_finish.bits.sink = grantack.bits.sink on MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505
      ],
      "formal": {
        "after": "RespHandshake",
        "before": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A14",
      "rendered_formula": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert <mu RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C5_ReplayDrain"
      ],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "formal": {
        "after": "ReplayHandshake",
        "before": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A15",
      "rendered_formula": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert <mu ReplayHandshake",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364,
        1367,
        1372,
        1375,
        1377
      ],
      "guard_predicates": [],
      "id": "C1_GrantCompleted",
      "relations": [
        "The memory response completes only after the MSHR has issued its current Acquire; the completed Grant may subsequently feed direct load responses, metadata processing, or replay drain."
      ],
      "trigger_occurrences": [
        "GrantComplete"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ],
      "guard_predicates": [],
      "id": "C2_LoadResponse",
      "relations": [
        "A direct load response occurs only on the post-Grant load-drain path and consumes an entry from the frozen RPQ dequeue stream."
      ],
      "trigger_occurrences": [
        "RespHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "guard_predicates": [],
      "id": "C3_VictimWriteback",
      "relations": [
        "The victim-writeback path performs a metadata read, clears the victim metadata, issues a writeback request, and waits for io.wb_resp before entering line commit."
      ],
      "trigger_occurrences": [
        "WBComplete"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1637,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ],
      "guard_predicates": [],
      "id": "C4_CommitLineRefill",
      "relations": [
        "The commit-line phase emits exactly the eight refill indices 0 through 7 before entering replay drain."
      ],
      "trigger_occurrences": [
        "CommitRefillDone"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "guard_predicates": [],
      "id": "C5_ReplayDrain",
      "relations": [
        "Replay handshakes are direct parent-local exposures of the frozen RPQ dequeue stream while state is s_drain_rpq."
      ],
      "trigger_occurrences": [
        "ReplayHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "guard_predicates": [],
      "id": "C6_FinalMetadataCommit",
      "relations": [
        "The final metadata update is reached only after the replay queue is observed empty with no concurrent enqueue."
      ],
      "trigger_occurrences": [
        "FinalMetaWrite"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1089,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "guard_predicates": [
        {
          "id": "GrantAckAbsent",
          "positive": false
        }
      ],
      "id": "C7_GrantFinish",
      "relations": [
        "A visible TileLink GrantAck handshake requires a valid stored grant acknowledgement derived from an earlier completed Grant."
      ],
      "trigger_occurrences": [
        "MemFinish"
      ]
    }
  ],
  "composition": {
    "imports": [
      {
        "child_id": "BoomMSHRFile.mshrs_0.rpq",
        "child_kind": "module",
        "frozen_umcm": {
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
                "predicate": "BoomMSHRFile.mshrs_0.rpq.main::QueueFull",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A1",
              "rendered_formula": "BoomMSHRFile.mshrs_0.rpq.main::QueueFull => !ParentEnqHandshake",
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
                "before": "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake",
                "required_prior": null,
                "scope_identity": null,
                "type": "ordered_before"
              },
              "id": "A4",
              "rendered_formula": "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake <mu ParentDeqHandshake",
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
                "before": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert",
                "required_prior": null,
                "scope_identity": null,
                "type": "ordered_before"
              },
              "id": "A5",
              "rendered_formula": "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert <mu ParentDeqHandshake",
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
                "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake"
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
                "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake"
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
                "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake"
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
                "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake"
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
                "child_id": "BoomMSHRFile.mshrs_0.rpq.main",
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
                        "BoomMSHRFile.mshrs_0.rpq.main::io.enq.fire"
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
                        "BoomMSHRFile.mshrs_0.rpq.main::io.deq.fire"
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
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "frozen_umcm_sha256": "02034cc1c5f1784f1dffd45793136e35296966d2daabf749c0498f4d0ace4eb6",
                "semantic_catalog": {
                  "axioms": {
                    "BoomMSHRFile.mshrs_0.rpq.main::A1": {
                      "local_id": "A1",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A11": {
                      "local_id": "A11",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A2": {
                      "local_id": "A2",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A3": {
                      "local_id": "A3",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A4": {
                      "local_id": "A4",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A5": {
                      "local_id": "A5",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A6": {
                      "local_id": "A6",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A7": {
                      "local_id": "A7",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::A8": {
                      "local_id": "A8",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    }
                  },
                  "cases": {
                    "BoomMSHRFile.mshrs_0.rpq.main::C1_Admitted": {
                      "local_id": "C1_Admitted",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::C2_BranchKilledOnArrival": {
                      "local_id": "C2_BranchKilledOnArrival",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::C3_FlushKilledOnArrival": {
                      "local_id": "C3_FlushKilledOnArrival",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::C4_VisibleDequeue": {
                      "local_id": "C4_VisibleDequeue",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::C5_InvalidHeadSkip": {
                      "local_id": "C5_InvalidHeadSkip",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    }
                  },
                  "identity_keys": {},
                  "occurrences": {
                    "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake": {
                      "local_id": "DeqHandshake",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake": {
                      "local_id": "EnqHandshake",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::InvalidHeadSkip": {
                      "local_id": "InvalidHeadSkip",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert": {
                      "local_id": "QueueInsert",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    }
                  },
                  "predicates": {
                    "BoomMSHRFile.mshrs_0.rpq.main::HeadInvalid": {
                      "local_id": "HeadInvalid",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::HeadValid": {
                      "local_id": "HeadValid",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::IncomingBranchKilled": {
                      "local_id": "IncomingBranchKilled",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::IncomingFlushKilled": {
                      "local_id": "IncomingFlushKilled",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::QueueEmpty": {
                      "local_id": "QueueEmpty",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_0.rpq.main::QueueFull": {
                      "local_id": "QueueFull",
                      "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
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
                "BoomMSHRFile.mshrs_0.rpq.main::A1": {
                  "local_id": "A1",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A11": {
                  "local_id": "A11",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A2": {
                  "local_id": "A2",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A3": {
                  "local_id": "A3",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A4": {
                  "local_id": "A4",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A5": {
                  "local_id": "A5",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A6": {
                  "local_id": "A6",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A7": {
                  "local_id": "A7",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::A8": {
                  "local_id": "A8",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq::A1": {
                  "local_id": "A1",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A2": {
                  "local_id": "A2",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A3": {
                  "local_id": "A3",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A4": {
                  "local_id": "A4",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A5": {
                  "local_id": "A5",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A6": {
                  "local_id": "A6",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::A7": {
                  "local_id": "A7",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                }
              },
              "cases": {
                "BoomMSHRFile.mshrs_0.rpq.main::C1_Admitted": {
                  "local_id": "C1_Admitted",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::C2_BranchKilledOnArrival": {
                  "local_id": "C2_BranchKilledOnArrival",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::C3_FlushKilledOnArrival": {
                  "local_id": "C3_FlushKilledOnArrival",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::C4_VisibleDequeue": {
                  "local_id": "C4_VisibleDequeue",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::C5_InvalidHeadSkip": {
                  "local_id": "C5_InvalidHeadSkip",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq::C1_EnqueueForwarded": {
                  "local_id": "C1_EnqueueForwarded",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::C2_ChildDequeueCaptured": {
                  "local_id": "C2_ChildDequeueCaptured",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::C3_ChildDequeueBranchKilled": {
                  "local_id": "C3_ChildDequeueBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::C4_ChildDequeueFlushKilled": {
                  "local_id": "C4_ChildDequeueFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::C5_VisibleParentDequeue": {
                  "local_id": "C5_VisibleParentDequeue",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                }
              },
              "identity_keys": {},
              "occurrences": {
                "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake": {
                  "local_id": "DeqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake": {
                  "local_id": "EnqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::InvalidHeadSkip": {
                  "local_id": "InvalidHeadSkip",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert": {
                  "local_id": "QueueInsert",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq::BufferCapture": {
                  "local_id": "BufferCapture",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::ParentDeqHandshake": {
                  "local_id": "ParentDeqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::ParentEnqHandshake": {
                  "local_id": "ParentEnqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                }
              },
              "predicates": {
                "BoomMSHRFile.mshrs_0.rpq.main::HeadInvalid": {
                  "local_id": "HeadInvalid",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::HeadValid": {
                  "local_id": "HeadValid",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::IncomingBranchKilled": {
                  "local_id": "IncomingBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::IncomingFlushKilled": {
                  "local_id": "IncomingFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::QueueEmpty": {
                  "local_id": "QueueEmpty",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq.main::QueueFull": {
                  "local_id": "QueueFull",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
                },
                "BoomMSHRFile.mshrs_0.rpq::OutputInvalid": {
                  "local_id": "OutputInvalid",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::TransferBranchKilled": {
                  "local_id": "TransferBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
                },
                "BoomMSHRFile.mshrs_0.rpq::TransferFlushKilled": {
                  "local_id": "TransferFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
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
                "BoomMSHRFile.mshrs_0.rpq::io.enq.fire"
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
                "BoomMSHRFile.mshrs_0.rpq::io.deq.fire"
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
                "BoomMSHRFile.mshrs_0.rpq.main::A1"
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
                "BoomMSHRFile.mshrs_0.rpq.main::A11"
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
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "frozen_umcm_sha256": "230ef3e758ec5cdfe3900166858dc48b0b5c32d085ad2792025e80469f1ac049",
        "semantic_catalog": {
          "axioms": {
            "BoomMSHRFile.mshrs_0.rpq.main::A1": {
              "local_id": "A1",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A11": {
              "local_id": "A11",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A2": {
              "local_id": "A2",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A3": {
              "local_id": "A3",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A4": {
              "local_id": "A4",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A5": {
              "local_id": "A5",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A6": {
              "local_id": "A6",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A7": {
              "local_id": "A7",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::A8": {
              "local_id": "A8",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq::A1": {
              "local_id": "A1",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A2": {
              "local_id": "A2",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A3": {
              "local_id": "A3",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A4": {
              "local_id": "A4",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A5": {
              "local_id": "A5",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A6": {
              "local_id": "A6",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::A7": {
              "local_id": "A7",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            }
          },
          "cases": {
            "BoomMSHRFile.mshrs_0.rpq.main::C1_Admitted": {
              "local_id": "C1_Admitted",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::C2_BranchKilledOnArrival": {
              "local_id": "C2_BranchKilledOnArrival",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::C3_FlushKilledOnArrival": {
              "local_id": "C3_FlushKilledOnArrival",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::C4_VisibleDequeue": {
              "local_id": "C4_VisibleDequeue",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::C5_InvalidHeadSkip": {
              "local_id": "C5_InvalidHeadSkip",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq::C1_EnqueueForwarded": {
              "local_id": "C1_EnqueueForwarded",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::C2_ChildDequeueCaptured": {
              "local_id": "C2_ChildDequeueCaptured",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::C3_ChildDequeueBranchKilled": {
              "local_id": "C3_ChildDequeueBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::C4_ChildDequeueFlushKilled": {
              "local_id": "C4_ChildDequeueFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::C5_VisibleParentDequeue": {
              "local_id": "C5_VisibleParentDequeue",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            }
          },
          "identity_keys": {},
          "occurrences": {
            "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake": {
              "local_id": "DeqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake": {
              "local_id": "EnqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::InvalidHeadSkip": {
              "local_id": "InvalidHeadSkip",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert": {
              "local_id": "QueueInsert",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq::BufferCapture": {
              "local_id": "BufferCapture",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::ParentDeqHandshake": {
              "local_id": "ParentDeqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::ParentEnqHandshake": {
              "local_id": "ParentEnqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            }
          },
          "predicates": {
            "BoomMSHRFile.mshrs_0.rpq.main::HeadInvalid": {
              "local_id": "HeadInvalid",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::HeadValid": {
              "local_id": "HeadValid",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::IncomingBranchKilled": {
              "local_id": "IncomingBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::IncomingFlushKilled": {
              "local_id": "IncomingFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::QueueEmpty": {
              "local_id": "QueueEmpty",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq.main::QueueFull": {
              "local_id": "QueueFull",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
            },
            "BoomMSHRFile.mshrs_0.rpq::OutputInvalid": {
              "local_id": "OutputInvalid",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::TransferBranchKilled": {
              "local_id": "TransferBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            },
            "BoomMSHRFile.mshrs_0.rpq::TransferFlushKilled": {
              "local_id": "TransferFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
            }
          }
        },
        "summary_ref": "umcm://BoomMSHR.rpq",
        "task_id": "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc"
      }
    ],
    "mode": "parent_synthesis",
    "note": "Child RTL is not part of this frozen parent. Imported child \u00b5MCMs remain frozen semantic components; descendant semantic names are transparently propagated in v0.1 for higher-level synthesis.",
    "policy": "transparent-frozen-child-imports-v0.1",
    "semantic_catalog": {
      "axioms": {
        "BoomMSHRFile.mshrs_0.rpq.main::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A11": {
          "local_id": "A11",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::A8": {
          "local_id": "A8",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A10": {
          "local_id": "A10",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A11": {
          "local_id": "A11",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A12": {
          "local_id": "A12",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A13": {
          "local_id": "A13",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A14": {
          "local_id": "A14",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A15": {
          "local_id": "A15",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A8": {
          "local_id": "A8",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::A9": {
          "local_id": "A9",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        }
      },
      "cases": {
        "BoomMSHRFile.mshrs_0.rpq.main::C1_Admitted": {
          "local_id": "C1_Admitted",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::C2_BranchKilledOnArrival": {
          "local_id": "C2_BranchKilledOnArrival",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::C3_FlushKilledOnArrival": {
          "local_id": "C3_FlushKilledOnArrival",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::C4_VisibleDequeue": {
          "local_id": "C4_VisibleDequeue",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::C5_InvalidHeadSkip": {
          "local_id": "C5_InvalidHeadSkip",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq::C1_EnqueueForwarded": {
          "local_id": "C1_EnqueueForwarded",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::C2_ChildDequeueCaptured": {
          "local_id": "C2_ChildDequeueCaptured",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::C3_ChildDequeueBranchKilled": {
          "local_id": "C3_ChildDequeueBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::C4_ChildDequeueFlushKilled": {
          "local_id": "C4_ChildDequeueFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::C5_VisibleParentDequeue": {
          "local_id": "C5_VisibleParentDequeue",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0::C1_GrantCompleted": {
          "local_id": "C1_GrantCompleted",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C2_LoadResponse": {
          "local_id": "C2_LoadResponse",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C3_VictimWriteback": {
          "local_id": "C3_VictimWriteback",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C4_CommitLineRefill": {
          "local_id": "C4_CommitLineRefill",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C5_ReplayDrain": {
          "local_id": "C5_ReplayDrain",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C6_FinalMetadataCommit": {
          "local_id": "C6_FinalMetadataCommit",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::C7_GrantFinish": {
          "local_id": "C7_GrantFinish",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        }
      },
      "identity_keys": {},
      "occurrences": {
        "BoomMSHRFile.mshrs_0.rpq.main::DeqHandshake": {
          "local_id": "DeqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::EnqHandshake": {
          "local_id": "EnqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::InvalidHeadSkip": {
          "local_id": "InvalidHeadSkip",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::QueueInsert": {
          "local_id": "QueueInsert",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq::BufferCapture": {
          "local_id": "BufferCapture",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::ParentDeqHandshake": {
          "local_id": "ParentDeqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::ParentEnqHandshake": {
          "local_id": "ParentEnqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0::CommitRefillBeat": {
          "local_id": "CommitRefillBeat",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::CommitRefillDone": {
          "local_id": "CommitRefillDone",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::FinalMetaWrite": {
          "local_id": "FinalMetaWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::GrantComplete": {
          "local_id": "GrantComplete",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::GrantDataWrite": {
          "local_id": "GrantDataWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::MemAcquire": {
          "local_id": "MemAcquire",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::MemFinish": {
          "local_id": "MemFinish",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::MemGrant": {
          "local_id": "MemGrant",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::MetaClearWrite": {
          "local_id": "MetaClearWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::MetaRead": {
          "local_id": "MetaRead",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::PrimaryAccept": {
          "local_id": "PrimaryAccept",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::RPQDrained": {
          "local_id": "RPQDrained",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::ReplayHandshake": {
          "local_id": "ReplayHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::RespHandshake": {
          "local_id": "RespHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::WBComplete": {
          "local_id": "WBComplete",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        },
        "BoomMSHRFile.mshrs_0::WBReq": {
          "local_id": "WBReq",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        }
      },
      "predicates": {
        "BoomMSHRFile.mshrs_0.rpq.main::HeadInvalid": {
          "local_id": "HeadInvalid",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::HeadValid": {
          "local_id": "HeadValid",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::IncomingBranchKilled": {
          "local_id": "IncomingBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::IncomingFlushKilled": {
          "local_id": "IncomingFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::QueueEmpty": {
          "local_id": "QueueEmpty",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq.main::QueueFull": {
          "local_id": "QueueFull",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq.main"
        },
        "BoomMSHRFile.mshrs_0.rpq::OutputInvalid": {
          "local_id": "OutputInvalid",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::TransferBranchKilled": {
          "local_id": "TransferBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0.rpq::TransferFlushKilled": {
          "local_id": "TransferFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_0.rpq"
        },
        "BoomMSHRFile.mshrs_0::GrantAckAbsent": {
          "local_id": "GrantAckAbsent",
          "work_unit_id": "BoomMSHRFile.mshrs_0"
        }
      }
    }
  },
  "freeze": {
    "candidate_axiom_count": 15,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 15
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "(state == s_invalid || state == s_prefetch) && io.req_pri_val && io.req_pri_rdy; a primary request is accepted and becomes the current MSHR request",
      "evidence_statement_ids": [
        1102,
        1103,
        1104,
        1106,
        1107,
        1119,
        1346,
        1840,
        1841,
        1842,
        1974,
        1975,
        1988,
        2215
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.req_pri_val",
          "io.req_pri_rdy"
        ],
        "state_register": "state",
        "state_values": [
          0,
          17
        ]
      },
      "id": "PrimaryAccept",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_refill_req && io.mem_acquire.valid && io.mem_acquire.ready",
      "evidence_statement_ids": [
        1348,
        1349,
        1350,
        1351,
        1352,
        1353
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          1
        ]
      },
      "id": "MemAcquire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.mem_acquire.fire"
      ]
    },
    {
      "definition": "state == s_refill_resp && io.mem_grant.valid && io.mem_grant.ready",
      "evidence_statement_ids": [
        1355,
        1356,
        1357,
        1363,
        1364
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "MemGrant",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.mem_grant.fire"
      ]
    },
    {
      "definition": "state == s_refill_resp && io.lb_write.valid; a data-bearing memory Grant is forwarded into the line buffer",
      "evidence_statement_ids": [
        1355,
        1356,
        1358,
        1359,
        1360
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.lb_write.valid"
        ],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "GrantDataWrite",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.lb_write.valid"
      ]
    },
    {
      "definition": "state == s_refill_resp && refill_done; the final accepted TileLink Grant beat completes the memory response and captures GrantAck/coherence state",
      "evidence_statement_ids": [
        604,
        614,
        615,
        616,
        617,
        618,
        1367,
        1372,
        1375,
        1377
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "refill_done"
        ],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "GrantComplete",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_meta_read && io.meta_read.valid && io.meta_read.ready",
      "evidence_statement_ids": [
        1525,
        1526,
        1527,
        1528,
        1529,
        1530,
        1531,
        1532,
        1533,
        1534,
        1535,
        1536
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          4
        ]
      },
      "id": "MetaRead",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.meta_read.fire"
      ]
    },
    {
      "definition": "state == s_meta_clear && io.meta_write.valid && io.meta_write.ready; the victim metadata is cleared before writeback",
      "evidence_statement_ids": [
        1618,
        1619,
        1620,
        1621,
        1622,
        1623
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "state_register": "state",
        "state_values": [
          7
        ]
      },
      "id": "MetaClearWrite",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_wb_req && io.wb_req.valid && io.wb_req.ready",
      "evidence_statement_ids": [
        1625,
        1626,
        1627,
        1628,
        1629,
        1630
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          9
        ]
      },
      "id": "WBReq",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.wb_req.fire"
      ]
    },
    {
      "definition": "state == s_wb_resp && io.wb_resp; the requested victim writeback has completed",
      "evidence_statement_ids": [
        1632,
        1633,
        1634,
        1635
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.wb_resp"
        ],
        "state_register": "state",
        "state_values": [
          10
        ]
      },
      "id": "WBComplete",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_commit_line && io.refill.valid && io.refill.ready; one cache-line commit beat is accepted",
      "evidence_statement_ids": [
        1637,
        1638,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          11
        ]
      },
      "id": "CommitRefillBeat",
      "index": {
        "domain": {
          "end_exclusive": 8,
          "start": 0
        },
        "expr": {
          "name": "refill_ctr",
          "op": "signal"
        },
        "name": "beat"
      },
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.refill.fire"
      ]
    },
    {
      "definition": "state == s_commit_line && io.refill.fire && refill_ctr == 7; the eighth and final commit refill beat is accepted and the MSHR enters replay drain",
      "evidence_statement_ids": [
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "_T_44",
          "_T_45"
        ],
        "state_register": "state",
        "state_values": [
          11
        ]
      },
      "id": "CommitRefillDone",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_drain_rpq_loads && io.resp.valid && io.resp.ready; a load replay-queue entry is returned directly as a load response",
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          3
        ]
      },
      "id": "RespHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.resp.fire"
      ]
    },
    {
      "definition": "state == s_drain_rpq && io.replay.valid && io.replay.ready; an RPQ entry is emitted through the replay interface",
      "evidence_statement_ids": [
        1650,
        1651,
        1652,
        1653,
        1654,
        1660
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          12
        ]
      },
      "id": "ReplayHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.replay.fire"
      ]
    },
    {
      "definition": "state == s_drain_rpq && rpq.io.empty && !rpq.io.enq.valid; no queued or concurrently incoming replay remains, so the MSHR may proceed to final metadata commit",
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "_T_76"
        ],
        "state_register": "state",
        "state_values": [
          12
        ]
      },
      "id": "RPQDrained",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_meta_write_req && io.meta_write.valid && io.meta_write.ready; the final acquired-line metadata is committed after RPQ drain",
      "evidence_statement_ids": [
        1813,
        1814,
        1815,
        1816,
        1817,
        1818,
        1819,
        1820,
        1821,
        1822
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "state_register": "state",
        "state_values": [
          13
        ]
      },
      "id": "FinalMetaWrite",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_mem_finish_1 && io.mem_finish.valid && io.mem_finish.ready",
      "evidence_statement_ids": [
        1089,
        1825,
        1826,
        1827,
        1828
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          14
        ]
      },
      "id": "MemFinish",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_0::io.mem_finish.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "grantack.valid == 0",
      "evidence_statement_ids": [
        900,
        1110,
        1372,
        1827,
        1832
      ],
      "grounding": {
        "negated": true,
        "source_signal": "grantack.valid",
        "state_register": null,
        "state_values": []
      },
      "id": "GrantAckAbsent"
    }
  ],
  "provenance": {
    "A1": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A10": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-combinational-exclusion",
      "source_axioms": []
    },
    "A11": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A12": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A13": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A14": {
      "derivation": "formal-certificate-v0.1",
      "kind": "emergent",
      "proof_method": "trusted-history-after-restriction",
      "source_axioms": [
        "BoomMSHRFile.mshrs_0.rpq::A5"
      ]
    },
    "A15": {
      "derivation": "formal-certificate-v0.1",
      "kind": "emergent",
      "proof_method": "trusted-history-after-restriction",
      "source_axioms": [
        "BoomMSHRFile.mshrs_0.rpq::A5"
      ]
    },
    "A2": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A3": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A4": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A5": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A6": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A7": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-bounded-indexed-occurrence",
      "source_axioms": []
    },
    "A8": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A9": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    }
  },
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHR-6362a83e7f824669",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A15",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.mshrs_0"
}
```

### Child `BoomMSHRFile.mshrs_1`
- summary ref: `umcm://BoomMSHRFile.mshrs_1`
- frozen task: `parent_synthesis-BoomMSHR-6362a83e7f824669`
- frozen SHA-256: `a67017f1a3a7c2afbcff4e648aa6d67f390cc315579127e0c5114eeeb183f860`
- implementation SHA-256: `667c8444124f2bbd733014e92e210269b24dc9888e3e9150c46083876bc352e6`
- instance reuse certificate: `{'kind': 'module-theorem-template-instantiation', 'source_work_unit_id': 'BoomMSHR', 'target_work_unit_id': 'BoomMSHRFile.mshrs_1', 'module': 'BoomMSHR_1', 'implementation_sha256': '667c8444124f2bbd733014e92e210269b24dc9888e3e9150c46083876bc352e6', 'structural_implementation_sha256': '976a59a277cde914bcc9b2c10fd08b16f63a666901c2093837633353cce0e6fa', 'source_module': 'BoomMSHR', 'verification': 'source-artifact-proof-scope-plus-transitive-structural-equivalence-v0.1'}`
- exposed boundary events: ['BoomMSHRFile.mshrs_1::io.idx.valid', 'BoomMSHRFile.mshrs_1::io.lb_write.valid', 'BoomMSHRFile.mshrs_1::io.mem_acquire.fire', 'BoomMSHRFile.mshrs_1::io.mem_finish.fire', 'BoomMSHRFile.mshrs_1::io.mem_grant.fire', 'BoomMSHRFile.mshrs_1::io.meta_read.fire', 'BoomMSHRFile.mshrs_1::io.meta_resp.valid', 'BoomMSHRFile.mshrs_1::io.meta_write.fire', 'BoomMSHRFile.mshrs_1::io.prober_state.valid', 'BoomMSHRFile.mshrs_1::io.refill.fire', 'BoomMSHRFile.mshrs_1::io.replay.fire', 'BoomMSHRFile.mshrs_1::io.resp.fire', 'BoomMSHRFile.mshrs_1::io.tag.valid', 'BoomMSHRFile.mshrs_1::io.way.valid', 'BoomMSHRFile.mshrs_1::io.wb_req.fire']
- frontier signals: ['mshrs_1.clock', 'mshrs_1.io', 'mshrs_1.io.brupdate.b1.mispredict_mask', 'mshrs_1.io.brupdate.b1.resolve_mask', 'mshrs_1.io.brupdate.b2.cfi_type', 'mshrs_1.io.brupdate.b2.jalr_target', 'mshrs_1.io.brupdate.b2.mispredict', 'mshrs_1.io.brupdate.b2.pc_sel', 'mshrs_1.io.brupdate.b2.taken', 'mshrs_1.io.brupdate.b2.target_offset', 'mshrs_1.io.brupdate.b2.uop.bp_debug_if', 'mshrs_1.io.brupdate.b2.uop.bp_xcpt_if', 'mshrs_1.io.brupdate.b2.uop.br_mask', 'mshrs_1.io.brupdate.b2.uop.br_tag', 'mshrs_1.io.brupdate.b2.uop.br_type', 'mshrs_1.io.brupdate.b2.uop.csr_cmd', 'mshrs_1.io.brupdate.b2.uop.debug_fsrc', 'mshrs_1.io.brupdate.b2.uop.debug_inst', 'mshrs_1.io.brupdate.b2.uop.debug_pc', 'mshrs_1.io.brupdate.b2.uop.debug_tsrc', 'mshrs_1.io.brupdate.b2.uop.dis_col_sel', 'mshrs_1.io.brupdate.b2.uop.dst_rtype', 'mshrs_1.io.brupdate.b2.uop.edge_inst', 'mshrs_1.io.brupdate.b2.uop.exc_cause', 'mshrs_1.io.brupdate.b2.uop.exception', 'mshrs_1.io.brupdate.b2.uop.fcn_dw', 'mshrs_1.io.brupdate.b2.uop.fcn_op', 'mshrs_1.io.brupdate.b2.uop.flush_on_commit', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.div', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fma', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.fromint', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ldst', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren1', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren2', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren3', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.sqrt', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap12', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap23', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.toint', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.vec', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.wen', 'mshrs_1.io.brupdate.b2.uop.fp_ctrl.wflags', 'mshrs_1.io.brupdate.b2.uop.fp_rm', 'mshrs_1.io.brupdate.b2.uop.fp_typ', 'mshrs_1.io.brupdate.b2.uop.fp_val', 'mshrs_1.io.brupdate.b2.uop.frs3_en', 'mshrs_1.io.brupdate.b2.uop.ftq_idx', 'mshrs_1.io.brupdate.b2.uop.fu_code[0]', 'mshrs_1.io.brupdate.b2.uop.fu_code[1]', 'mshrs_1.io.brupdate.b2.uop.fu_code[2]', 'mshrs_1.io.brupdate.b2.uop.fu_code[3]', 'mshrs_1.io.brupdate.b2.uop.fu_code[4]', 'mshrs_1.io.brupdate.b2.uop.fu_code[5]', 'mshrs_1.io.brupdate.b2.uop.fu_code[6]', 'mshrs_1.io.brupdate.b2.uop.fu_code[7]', 'mshrs_1.io.brupdate.b2.uop.fu_code[8]', 'mshrs_1.io.brupdate.b2.uop.fu_code[9]', 'mshrs_1.io.brupdate.b2.uop.imm_packed', 'mshrs_1.io.brupdate.b2.uop.imm_rename', 'mshrs_1.io.brupdate.b2.uop.imm_sel', 'mshrs_1.io.brupdate.b2.uop.inst', 'mshrs_1.io.brupdate.b2.uop.iq_type[0]', 'mshrs_1.io.brupdate.b2.uop.iq_type[1]', 'mshrs_1.io.brupdate.b2.uop.iq_type[2]', 'mshrs_1.io.brupdate.b2.uop.iq_type[3]', 'mshrs_1.io.brupdate.b2.uop.is_amo', 'mshrs_1.io.brupdate.b2.uop.is_eret', 'mshrs_1.io.brupdate.b2.uop.is_fence', 'mshrs_1.io.brupdate.b2.uop.is_fencei', 'mshrs_1.io.brupdate.b2.uop.is_mov', 'mshrs_1.io.brupdate.b2.uop.is_rocc', 'mshrs_1.io.brupdate.b2.uop.is_rvc', 'mshrs_1.io.brupdate.b2.uop.is_sfb', 'mshrs_1.io.brupdate.b2.uop.is_sfence', 'mshrs_1.io.brupdate.b2.uop.is_sys_pc2epc', 'mshrs_1.io.brupdate.b2.uop.is_unique', 'mshrs_1.io.brupdate.b2.uop.iw_issued', 'mshrs_1.io.brupdate.b2.uop.iw_issued_partial_agen', 'mshrs_1.io.brupdate.b2.uop.iw_issued_partial_dgen', 'mshrs_1.io.brupdate.b2.uop.iw_p1_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.iw_p1_speculative_child', 'mshrs_1.io.brupdate.b2.uop.iw_p2_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.iw_p2_speculative_child', 'mshrs_1.io.brupdate.b2.uop.iw_p3_bypass_hint', 'mshrs_1.io.brupdate.b2.uop.ldq_idx', 'mshrs_1.io.brupdate.b2.uop.ldst', 'mshrs_1.io.brupdate.b2.uop.ldst_is_rs1', 'mshrs_1.io.brupdate.b2.uop.lrs1', 'mshrs_1.io.brupdate.b2.uop.lrs1_rtype', 'mshrs_1.io.brupdate.b2.uop.lrs2', 'mshrs_1.io.brupdate.b2.uop.lrs2_rtype', 'mshrs_1.io.brupdate.b2.uop.lrs3', 'mshrs_1.io.brupdate.b2.uop.mem_cmd', 'mshrs_1.io.brupdate.b2.uop.mem_signed', 'mshrs_1.io.brupdate.b2.uop.mem_size', 'mshrs_1.io.brupdate.b2.uop.op1_sel', 'mshrs_1.io.brupdate.b2.uop.op2_sel', 'mshrs_1.io.brupdate.b2.uop.pc_lob', 'mshrs_1.io.brupdate.b2.uop.pdst', 'mshrs_1.io.brupdate.b2.uop.pimm', 'mshrs_1.io.brupdate.b2.uop.ppred', 'mshrs_1.io.brupdate.b2.uop.ppred_busy', 'mshrs_1.io.brupdate.b2.uop.prs1', 'mshrs_1.io.brupdate.b2.uop.prs1_busy', 'mshrs_1.io.brupdate.b2.uop.prs2', 'mshrs_1.io.brupdate.b2.uop.prs2_busy', 'mshrs_1.io.brupdate.b2.uop.prs3', 'mshrs_1.io.brupdate.b2.uop.prs3_busy', 'mshrs_1.io.brupdate.b2.uop.rob_idx', 'mshrs_1.io.brupdate.b2.uop.rxq_idx', 'mshrs_1.io.brupdate.b2.uop.stale_pdst', 'mshrs_1.io.brupdate.b2.uop.stq_idx', 'mshrs_1.io.brupdate.b2.uop.taken', 'mshrs_1.io.brupdate.b2.uop.uses_ldq', 'mshrs_1.io.brupdate.b2.uop.uses_stq', 'mshrs_1.io.brupdate.b2.uop.xcpt_ae_if', 'mshrs_1.io.brupdate.b2.uop.xcpt_ma_if', 'mshrs_1.io.brupdate.b2.uop.xcpt_pf_if', 'mshrs_1.io.clear_prefetch', 'mshrs_1.io.commit_addr', 'mshrs_1.io.commit_coh.state', 'mshrs_1.io.commit_val', 'mshrs_1.io.exception', 'mshrs_1.io.id', 'mshrs_1.io.idx.bits', 'mshrs_1.io.idx.valid', 'mshrs_1.io.lb_read.offset', 'mshrs_1.io.lb_resp', 'mshrs_1.io.lb_write.bits.data', 'mshrs_1.io.lb_write.bits.offset', 'mshrs_1.io.lb_write.valid', 'mshrs_1.io.mem_acquire.bits.address', 'mshrs_1.io.mem_acquire.bits.corrupt', 'mshrs_1.io.mem_acquire.bits.data', 'mshrs_1.io.mem_acquire.bits.mask', 'mshrs_1.io.mem_acquire.bits.opcode', 'mshrs_1.io.mem_acquire.bits.param', 'mshrs_1.io.mem_acquire.bits.size', 'mshrs_1.io.mem_acquire.bits.source', 'mshrs_1.io.mem_acquire.ready', 'mshrs_1.io.mem_acquire.valid', 'mshrs_1.io.mem_finish.bits.sink', 'mshrs_1.io.mem_finish.ready', 'mshrs_1.io.mem_finish.valid', 'mshrs_1.io.mem_grant.bits.corrupt', 'mshrs_1.io.mem_grant.bits.data', 'mshrs_1.io.mem_grant.bits.denied', 'mshrs_1.io.mem_grant.bits.opcode', 'mshrs_1.io.mem_grant.bits.param', 'mshrs_1.io.mem_grant.bits.sink', 'mshrs_1.io.mem_grant.bits.size', 'mshrs_1.io.mem_grant.bits.source', 'mshrs_1.io.mem_grant.ready', 'mshrs_1.io.mem_grant.valid', 'mshrs_1.io.meta_read.bits.idx', 'mshrs_1.io.meta_read.bits.tag', 'mshrs_1.io.meta_read.bits.way_en', 'mshrs_1.io.meta_read.ready', 'mshrs_1.io.meta_read.valid', 'mshrs_1.io.meta_resp.bits.coh.state', 'mshrs_1.io.meta_resp.bits.tag', 'mshrs_1.io.meta_resp.valid', 'mshrs_1.io.meta_write.bits.data.coh.state', 'mshrs_1.io.meta_write.bits.data.tag', 'mshrs_1.io.meta_write.bits.idx', 'mshrs_1.io.meta_write.bits.tag', 'mshrs_1.io.meta_write.bits.way_en', 'mshrs_1.io.meta_write.ready', 'mshrs_1.io.meta_write.valid', 'mshrs_1.io.probe_rdy', 'mshrs_1.io.prober_state.bits', 'mshrs_1.io.prober_state.valid', 'mshrs_1.io.refill.bits.addr', 'mshrs_1.io.refill.bits.data', 'mshrs_1.io.refill.bits.way_en', 'mshrs_1.io.refill.bits.wmask', 'mshrs_1.io.refill.ready', 'mshrs_1.io.refill.valid', 'mshrs_1.io.replay.bits.addr', 'mshrs_1.io.replay.bits.data', 'mshrs_1.io.replay.bits.is_hella', 'mshrs_1.io.replay.bits.old_meta.coh.state', 'mshrs_1.io.replay.bits.old_meta.tag', 'mshrs_1.io.replay.bits.sdq_id', 'mshrs_1.io.replay.bits.tag_match', 'mshrs_1.io.replay.bits.uop.bp_debug_if', 'mshrs_1.io.replay.bits.uop.bp_xcpt_if', 'mshrs_1.io.replay.bits.uop.br_mask', 'mshrs_1.io.replay.bits.uop.br_tag', 'mshrs_1.io.replay.bits.uop.br_type', 'mshrs_1.io.replay.bits.uop.csr_cmd', 'mshrs_1.io.replay.bits.uop.debug_fsrc', 'mshrs_1.io.replay.bits.uop.debug_inst', 'mshrs_1.io.replay.bits.uop.debug_pc', 'mshrs_1.io.replay.bits.uop.debug_tsrc', 'mshrs_1.io.replay.bits.uop.dis_col_sel', 'mshrs_1.io.replay.bits.uop.dst_rtype', 'mshrs_1.io.replay.bits.uop.edge_inst', 'mshrs_1.io.replay.bits.uop.exc_cause', 'mshrs_1.io.replay.bits.uop.exception', 'mshrs_1.io.replay.bits.uop.fcn_dw', 'mshrs_1.io.replay.bits.uop.fcn_op', 'mshrs_1.io.replay.bits.uop.flush_on_commit', 'mshrs_1.io.replay.bits.uop.fp_ctrl.div', 'mshrs_1.io.replay.bits.uop.fp_ctrl.fastpipe', 'mshrs_1.io.replay.bits.uop.fp_ctrl.fma', 'mshrs_1.io.replay.bits.uop.fp_ctrl.fromint', 'mshrs_1.io.replay.bits.uop.fp_ctrl.ldst', 'mshrs_1.io.replay.bits.uop.fp_ctrl.ren1', 'mshrs_1.io.replay.bits.uop.fp_ctrl.ren2', 'mshrs_1.io.replay.bits.uop.fp_ctrl.ren3', 'mshrs_1.io.replay.bits.uop.fp_ctrl.sqrt', 'mshrs_1.io.replay.bits.uop.fp_ctrl.swap12', 'mshrs_1.io.replay.bits.uop.fp_ctrl.swap23', 'mshrs_1.io.replay.bits.uop.fp_ctrl.toint', 'mshrs_1.io.replay.bits.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.replay.bits.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.replay.bits.uop.fp_ctrl.vec', 'mshrs_1.io.replay.bits.uop.fp_ctrl.wen', 'mshrs_1.io.replay.bits.uop.fp_ctrl.wflags', 'mshrs_1.io.replay.bits.uop.fp_rm', 'mshrs_1.io.replay.bits.uop.fp_typ', 'mshrs_1.io.replay.bits.uop.fp_val', 'mshrs_1.io.replay.bits.uop.frs3_en', 'mshrs_1.io.replay.bits.uop.ftq_idx', 'mshrs_1.io.replay.bits.uop.fu_code[0]', 'mshrs_1.io.replay.bits.uop.fu_code[1]', 'mshrs_1.io.replay.bits.uop.fu_code[2]', 'mshrs_1.io.replay.bits.uop.fu_code[3]', 'mshrs_1.io.replay.bits.uop.fu_code[4]', 'mshrs_1.io.replay.bits.uop.fu_code[5]', 'mshrs_1.io.replay.bits.uop.fu_code[6]', 'mshrs_1.io.replay.bits.uop.fu_code[7]', 'mshrs_1.io.replay.bits.uop.fu_code[8]', 'mshrs_1.io.replay.bits.uop.fu_code[9]', 'mshrs_1.io.replay.bits.uop.imm_packed', 'mshrs_1.io.replay.bits.uop.imm_rename', 'mshrs_1.io.replay.bits.uop.imm_sel', 'mshrs_1.io.replay.bits.uop.inst', 'mshrs_1.io.replay.bits.uop.iq_type[0]', 'mshrs_1.io.replay.bits.uop.iq_type[1]', 'mshrs_1.io.replay.bits.uop.iq_type[2]', 'mshrs_1.io.replay.bits.uop.iq_type[3]', 'mshrs_1.io.replay.bits.uop.is_amo', 'mshrs_1.io.replay.bits.uop.is_eret', 'mshrs_1.io.replay.bits.uop.is_fence', 'mshrs_1.io.replay.bits.uop.is_fencei', 'mshrs_1.io.replay.bits.uop.is_mov', 'mshrs_1.io.replay.bits.uop.is_rocc', 'mshrs_1.io.replay.bits.uop.is_rvc', 'mshrs_1.io.replay.bits.uop.is_sfb', 'mshrs_1.io.replay.bits.uop.is_sfence', 'mshrs_1.io.replay.bits.uop.is_sys_pc2epc', 'mshrs_1.io.replay.bits.uop.is_unique', 'mshrs_1.io.replay.bits.uop.iw_issued', 'mshrs_1.io.replay.bits.uop.iw_issued_partial_agen', 'mshrs_1.io.replay.bits.uop.iw_issued_partial_dgen', 'mshrs_1.io.replay.bits.uop.iw_p1_bypass_hint', 'mshrs_1.io.replay.bits.uop.iw_p1_speculative_child', 'mshrs_1.io.replay.bits.uop.iw_p2_bypass_hint', 'mshrs_1.io.replay.bits.uop.iw_p2_speculative_child', 'mshrs_1.io.replay.bits.uop.iw_p3_bypass_hint', 'mshrs_1.io.replay.bits.uop.ldq_idx', 'mshrs_1.io.replay.bits.uop.ldst', 'mshrs_1.io.replay.bits.uop.ldst_is_rs1', 'mshrs_1.io.replay.bits.uop.lrs1', 'mshrs_1.io.replay.bits.uop.lrs1_rtype', 'mshrs_1.io.replay.bits.uop.lrs2', 'mshrs_1.io.replay.bits.uop.lrs2_rtype', 'mshrs_1.io.replay.bits.uop.lrs3', 'mshrs_1.io.replay.bits.uop.mem_cmd', 'mshrs_1.io.replay.bits.uop.mem_signed', 'mshrs_1.io.replay.bits.uop.mem_size', 'mshrs_1.io.replay.bits.uop.op1_sel', 'mshrs_1.io.replay.bits.uop.op2_sel', 'mshrs_1.io.replay.bits.uop.pc_lob', 'mshrs_1.io.replay.bits.uop.pdst', 'mshrs_1.io.replay.bits.uop.pimm', 'mshrs_1.io.replay.bits.uop.ppred', 'mshrs_1.io.replay.bits.uop.ppred_busy', 'mshrs_1.io.replay.bits.uop.prs1', 'mshrs_1.io.replay.bits.uop.prs1_busy', 'mshrs_1.io.replay.bits.uop.prs2', 'mshrs_1.io.replay.bits.uop.prs2_busy', 'mshrs_1.io.replay.bits.uop.prs3', 'mshrs_1.io.replay.bits.uop.prs3_busy', 'mshrs_1.io.replay.bits.uop.rob_idx', 'mshrs_1.io.replay.bits.uop.rxq_idx', 'mshrs_1.io.replay.bits.uop.stale_pdst', 'mshrs_1.io.replay.bits.uop.stq_idx', 'mshrs_1.io.replay.bits.uop.taken', 'mshrs_1.io.replay.bits.uop.uses_ldq', 'mshrs_1.io.replay.bits.uop.uses_stq', 'mshrs_1.io.replay.bits.uop.xcpt_ae_if', 'mshrs_1.io.replay.bits.uop.xcpt_ma_if', 'mshrs_1.io.replay.bits.uop.xcpt_pf_if', 'mshrs_1.io.replay.bits.way_en', 'mshrs_1.io.replay.ready', 'mshrs_1.io.replay.valid', 'mshrs_1.io.req.addr', 'mshrs_1.io.req.data', 'mshrs_1.io.req.is_hella', 'mshrs_1.io.req.old_meta.coh.state', 'mshrs_1.io.req.old_meta.tag', 'mshrs_1.io.req.sdq_id', 'mshrs_1.io.req.tag_match', 'mshrs_1.io.req.uop.bp_debug_if', 'mshrs_1.io.req.uop.bp_xcpt_if', 'mshrs_1.io.req.uop.br_mask', 'mshrs_1.io.req.uop.br_tag', 'mshrs_1.io.req.uop.br_type', 'mshrs_1.io.req.uop.csr_cmd', 'mshrs_1.io.req.uop.debug_fsrc', 'mshrs_1.io.req.uop.debug_inst', 'mshrs_1.io.req.uop.debug_pc', 'mshrs_1.io.req.uop.debug_tsrc', 'mshrs_1.io.req.uop.dis_col_sel', 'mshrs_1.io.req.uop.dst_rtype', 'mshrs_1.io.req.uop.edge_inst', 'mshrs_1.io.req.uop.exc_cause', 'mshrs_1.io.req.uop.exception', 'mshrs_1.io.req.uop.fcn_dw', 'mshrs_1.io.req.uop.fcn_op', 'mshrs_1.io.req.uop.flush_on_commit', 'mshrs_1.io.req.uop.fp_ctrl.div', 'mshrs_1.io.req.uop.fp_ctrl.fastpipe', 'mshrs_1.io.req.uop.fp_ctrl.fma', 'mshrs_1.io.req.uop.fp_ctrl.fromint', 'mshrs_1.io.req.uop.fp_ctrl.ldst', 'mshrs_1.io.req.uop.fp_ctrl.ren1', 'mshrs_1.io.req.uop.fp_ctrl.ren2', 'mshrs_1.io.req.uop.fp_ctrl.ren3', 'mshrs_1.io.req.uop.fp_ctrl.sqrt', 'mshrs_1.io.req.uop.fp_ctrl.swap12', 'mshrs_1.io.req.uop.fp_ctrl.swap23', 'mshrs_1.io.req.uop.fp_ctrl.toint', 'mshrs_1.io.req.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.req.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.req.uop.fp_ctrl.vec', 'mshrs_1.io.req.uop.fp_ctrl.wen', 'mshrs_1.io.req.uop.fp_ctrl.wflags', 'mshrs_1.io.req.uop.fp_rm', 'mshrs_1.io.req.uop.fp_typ', 'mshrs_1.io.req.uop.fp_val', 'mshrs_1.io.req.uop.frs3_en', 'mshrs_1.io.req.uop.ftq_idx', 'mshrs_1.io.req.uop.fu_code[0]', 'mshrs_1.io.req.uop.fu_code[1]', 'mshrs_1.io.req.uop.fu_code[2]', 'mshrs_1.io.req.uop.fu_code[3]', 'mshrs_1.io.req.uop.fu_code[4]', 'mshrs_1.io.req.uop.fu_code[5]', 'mshrs_1.io.req.uop.fu_code[6]', 'mshrs_1.io.req.uop.fu_code[7]', 'mshrs_1.io.req.uop.fu_code[8]', 'mshrs_1.io.req.uop.fu_code[9]', 'mshrs_1.io.req.uop.imm_packed', 'mshrs_1.io.req.uop.imm_rename', 'mshrs_1.io.req.uop.imm_sel', 'mshrs_1.io.req.uop.inst', 'mshrs_1.io.req.uop.iq_type[0]', 'mshrs_1.io.req.uop.iq_type[1]', 'mshrs_1.io.req.uop.iq_type[2]', 'mshrs_1.io.req.uop.iq_type[3]', 'mshrs_1.io.req.uop.is_amo', 'mshrs_1.io.req.uop.is_eret', 'mshrs_1.io.req.uop.is_fence', 'mshrs_1.io.req.uop.is_fencei', 'mshrs_1.io.req.uop.is_mov', 'mshrs_1.io.req.uop.is_rocc', 'mshrs_1.io.req.uop.is_rvc', 'mshrs_1.io.req.uop.is_sfb', 'mshrs_1.io.req.uop.is_sfence', 'mshrs_1.io.req.uop.is_sys_pc2epc', 'mshrs_1.io.req.uop.is_unique', 'mshrs_1.io.req.uop.iw_issued', 'mshrs_1.io.req.uop.iw_issued_partial_agen', 'mshrs_1.io.req.uop.iw_issued_partial_dgen', 'mshrs_1.io.req.uop.iw_p1_bypass_hint', 'mshrs_1.io.req.uop.iw_p1_speculative_child', 'mshrs_1.io.req.uop.iw_p2_bypass_hint', 'mshrs_1.io.req.uop.iw_p2_speculative_child', 'mshrs_1.io.req.uop.iw_p3_bypass_hint', 'mshrs_1.io.req.uop.ldq_idx', 'mshrs_1.io.req.uop.ldst', 'mshrs_1.io.req.uop.ldst_is_rs1', 'mshrs_1.io.req.uop.lrs1', 'mshrs_1.io.req.uop.lrs1_rtype', 'mshrs_1.io.req.uop.lrs2', 'mshrs_1.io.req.uop.lrs2_rtype', 'mshrs_1.io.req.uop.lrs3', 'mshrs_1.io.req.uop.mem_cmd', 'mshrs_1.io.req.uop.mem_signed', 'mshrs_1.io.req.uop.mem_size', 'mshrs_1.io.req.uop.op1_sel', 'mshrs_1.io.req.uop.op2_sel', 'mshrs_1.io.req.uop.pc_lob', 'mshrs_1.io.req.uop.pdst', 'mshrs_1.io.req.uop.pimm', 'mshrs_1.io.req.uop.ppred', 'mshrs_1.io.req.uop.ppred_busy', 'mshrs_1.io.req.uop.prs1', 'mshrs_1.io.req.uop.prs1_busy', 'mshrs_1.io.req.uop.prs2', 'mshrs_1.io.req.uop.prs2_busy', 'mshrs_1.io.req.uop.prs3', 'mshrs_1.io.req.uop.prs3_busy', 'mshrs_1.io.req.uop.rob_idx', 'mshrs_1.io.req.uop.rxq_idx', 'mshrs_1.io.req.uop.stale_pdst', 'mshrs_1.io.req.uop.stq_idx', 'mshrs_1.io.req.uop.taken', 'mshrs_1.io.req.uop.uses_ldq', 'mshrs_1.io.req.uop.uses_stq', 'mshrs_1.io.req.uop.xcpt_ae_if', 'mshrs_1.io.req.uop.xcpt_ma_if', 'mshrs_1.io.req.uop.xcpt_pf_if', 'mshrs_1.io.req.way_en', 'mshrs_1.io.req_is_probe', 'mshrs_1.io.req_pri_rdy', 'mshrs_1.io.req_pri_val', 'mshrs_1.io.req_sec_rdy', 'mshrs_1.io.req_sec_val', 'mshrs_1.io.resp.bits.data', 'mshrs_1.io.resp.bits.is_hella', 'mshrs_1.io.resp.bits.uop.bp_debug_if', 'mshrs_1.io.resp.bits.uop.bp_xcpt_if', 'mshrs_1.io.resp.bits.uop.br_mask', 'mshrs_1.io.resp.bits.uop.br_tag', 'mshrs_1.io.resp.bits.uop.br_type', 'mshrs_1.io.resp.bits.uop.csr_cmd', 'mshrs_1.io.resp.bits.uop.debug_fsrc', 'mshrs_1.io.resp.bits.uop.debug_inst', 'mshrs_1.io.resp.bits.uop.debug_pc', 'mshrs_1.io.resp.bits.uop.debug_tsrc', 'mshrs_1.io.resp.bits.uop.dis_col_sel', 'mshrs_1.io.resp.bits.uop.dst_rtype', 'mshrs_1.io.resp.bits.uop.edge_inst', 'mshrs_1.io.resp.bits.uop.exc_cause', 'mshrs_1.io.resp.bits.uop.exception', 'mshrs_1.io.resp.bits.uop.fcn_dw', 'mshrs_1.io.resp.bits.uop.fcn_op', 'mshrs_1.io.resp.bits.uop.flush_on_commit', 'mshrs_1.io.resp.bits.uop.fp_ctrl.div', 'mshrs_1.io.resp.bits.uop.fp_ctrl.fastpipe', 'mshrs_1.io.resp.bits.uop.fp_ctrl.fma', 'mshrs_1.io.resp.bits.uop.fp_ctrl.fromint', 'mshrs_1.io.resp.bits.uop.fp_ctrl.ldst', 'mshrs_1.io.resp.bits.uop.fp_ctrl.ren1', 'mshrs_1.io.resp.bits.uop.fp_ctrl.ren2', 'mshrs_1.io.resp.bits.uop.fp_ctrl.ren3', 'mshrs_1.io.resp.bits.uop.fp_ctrl.sqrt', 'mshrs_1.io.resp.bits.uop.fp_ctrl.swap12', 'mshrs_1.io.resp.bits.uop.fp_ctrl.swap23', 'mshrs_1.io.resp.bits.uop.fp_ctrl.toint', 'mshrs_1.io.resp.bits.uop.fp_ctrl.typeTagIn', 'mshrs_1.io.resp.bits.uop.fp_ctrl.typeTagOut', 'mshrs_1.io.resp.bits.uop.fp_ctrl.vec', 'mshrs_1.io.resp.bits.uop.fp_ctrl.wen', 'mshrs_1.io.resp.bits.uop.fp_ctrl.wflags', 'mshrs_1.io.resp.bits.uop.fp_rm', 'mshrs_1.io.resp.bits.uop.fp_typ', 'mshrs_1.io.resp.bits.uop.fp_val', 'mshrs_1.io.resp.bits.uop.frs3_en', 'mshrs_1.io.resp.bits.uop.ftq_idx', 'mshrs_1.io.resp.bits.uop.fu_code[0]', 'mshrs_1.io.resp.bits.uop.fu_code[1]', 'mshrs_1.io.resp.bits.uop.fu_code[2]', 'mshrs_1.io.resp.bits.uop.fu_code[3]', 'mshrs_1.io.resp.bits.uop.fu_code[4]', 'mshrs_1.io.resp.bits.uop.fu_code[5]', 'mshrs_1.io.resp.bits.uop.fu_code[6]', 'mshrs_1.io.resp.bits.uop.fu_code[7]', 'mshrs_1.io.resp.bits.uop.fu_code[8]', 'mshrs_1.io.resp.bits.uop.fu_code[9]', 'mshrs_1.io.resp.bits.uop.imm_packed', 'mshrs_1.io.resp.bits.uop.imm_rename', 'mshrs_1.io.resp.bits.uop.imm_sel', 'mshrs_1.io.resp.bits.uop.inst', 'mshrs_1.io.resp.bits.uop.iq_type[0]', 'mshrs_1.io.resp.bits.uop.iq_type[1]', 'mshrs_1.io.resp.bits.uop.iq_type[2]', 'mshrs_1.io.resp.bits.uop.iq_type[3]', 'mshrs_1.io.resp.bits.uop.is_amo', 'mshrs_1.io.resp.bits.uop.is_eret', 'mshrs_1.io.resp.bits.uop.is_fence', 'mshrs_1.io.resp.bits.uop.is_fencei', 'mshrs_1.io.resp.bits.uop.is_mov', 'mshrs_1.io.resp.bits.uop.is_rocc', 'mshrs_1.io.resp.bits.uop.is_rvc', 'mshrs_1.io.resp.bits.uop.is_sfb', 'mshrs_1.io.resp.bits.uop.is_sfence', 'mshrs_1.io.resp.bits.uop.is_sys_pc2epc', 'mshrs_1.io.resp.bits.uop.is_unique', 'mshrs_1.io.resp.bits.uop.iw_issued', 'mshrs_1.io.resp.bits.uop.iw_issued_partial_agen', 'mshrs_1.io.resp.bits.uop.iw_issued_partial_dgen', 'mshrs_1.io.resp.bits.uop.iw_p1_bypass_hint', 'mshrs_1.io.resp.bits.uop.iw_p1_speculative_child', 'mshrs_1.io.resp.bits.uop.iw_p2_bypass_hint', 'mshrs_1.io.resp.bits.uop.iw_p2_speculative_child', 'mshrs_1.io.resp.bits.uop.iw_p3_bypass_hint', 'mshrs_1.io.resp.bits.uop.ldq_idx', 'mshrs_1.io.resp.bits.uop.ldst', 'mshrs_1.io.resp.bits.uop.ldst_is_rs1', 'mshrs_1.io.resp.bits.uop.lrs1', 'mshrs_1.io.resp.bits.uop.lrs1_rtype', 'mshrs_1.io.resp.bits.uop.lrs2', 'mshrs_1.io.resp.bits.uop.lrs2_rtype', 'mshrs_1.io.resp.bits.uop.lrs3', 'mshrs_1.io.resp.bits.uop.mem_cmd', 'mshrs_1.io.resp.bits.uop.mem_signed', 'mshrs_1.io.resp.bits.uop.mem_size', 'mshrs_1.io.resp.bits.uop.op1_sel', 'mshrs_1.io.resp.bits.uop.op2_sel', 'mshrs_1.io.resp.bits.uop.pc_lob', 'mshrs_1.io.resp.bits.uop.pdst', 'mshrs_1.io.resp.bits.uop.pimm', 'mshrs_1.io.resp.bits.uop.ppred', 'mshrs_1.io.resp.bits.uop.ppred_busy', 'mshrs_1.io.resp.bits.uop.prs1', 'mshrs_1.io.resp.bits.uop.prs1_busy', 'mshrs_1.io.resp.bits.uop.prs2', 'mshrs_1.io.resp.bits.uop.prs2_busy', 'mshrs_1.io.resp.bits.uop.prs3', 'mshrs_1.io.resp.bits.uop.prs3_busy', 'mshrs_1.io.resp.bits.uop.rob_idx', 'mshrs_1.io.resp.bits.uop.rxq_idx', 'mshrs_1.io.resp.bits.uop.stale_pdst', 'mshrs_1.io.resp.bits.uop.stq_idx', 'mshrs_1.io.resp.bits.uop.taken', 'mshrs_1.io.resp.bits.uop.uses_ldq', 'mshrs_1.io.resp.bits.uop.uses_stq', 'mshrs_1.io.resp.bits.uop.xcpt_ae_if', 'mshrs_1.io.resp.bits.uop.xcpt_ma_if', 'mshrs_1.io.resp.bits.uop.xcpt_pf_if', 'mshrs_1.io.resp.ready', 'mshrs_1.io.resp.valid', 'mshrs_1.io.rob_head_idx', 'mshrs_1.io.rob_pnr_idx', 'mshrs_1.io.tag.bits', 'mshrs_1.io.tag.valid', 'mshrs_1.io.way.bits', 'mshrs_1.io.way.valid', 'mshrs_1.io.wb_req.bits.idx', 'mshrs_1.io.wb_req.bits.param', 'mshrs_1.io.wb_req.bits.source', 'mshrs_1.io.wb_req.bits.tag', 'mshrs_1.io.wb_req.bits.voluntary', 'mshrs_1.io.wb_req.bits.way_en', 'mshrs_1.io.wb_req.ready', 'mshrs_1.io.wb_req.valid', 'mshrs_1.io.wb_resp', 'mshrs_1.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.mshrs_1.rpq.main::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A13": {
      "local_id": "A13",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A14": {
      "local_id": "A14",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A15": {
      "local_id": "A15",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    }
  },
  "cases": {
    "BoomMSHRFile.mshrs_1.rpq.main::C1_Admitted": {
      "local_id": "C1_Admitted",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::C2_BranchKilledOnArrival": {
      "local_id": "C2_BranchKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::C3_FlushKilledOnArrival": {
      "local_id": "C3_FlushKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::C4_VisibleDequeue": {
      "local_id": "C4_VisibleDequeue",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::C5_InvalidHeadSkip": {
      "local_id": "C5_InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq::C1_EnqueueForwarded": {
      "local_id": "C1_EnqueueForwarded",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::C2_ChildDequeueCaptured": {
      "local_id": "C2_ChildDequeueCaptured",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::C3_ChildDequeueBranchKilled": {
      "local_id": "C3_ChildDequeueBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::C4_ChildDequeueFlushKilled": {
      "local_id": "C4_ChildDequeueFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::C5_VisibleParentDequeue": {
      "local_id": "C5_VisibleParentDequeue",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1::C1_GrantCompleted": {
      "local_id": "C1_GrantCompleted",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C2_LoadResponse": {
      "local_id": "C2_LoadResponse",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C3_VictimWriteback": {
      "local_id": "C3_VictimWriteback",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C4_CommitLineRefill": {
      "local_id": "C4_CommitLineRefill",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C5_ReplayDrain": {
      "local_id": "C5_ReplayDrain",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C6_FinalMetadataCommit": {
      "local_id": "C6_FinalMetadataCommit",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::C7_GrantFinish": {
      "local_id": "C7_GrantFinish",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake": {
      "local_id": "DeqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake": {
      "local_id": "EnqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::InvalidHeadSkip": {
      "local_id": "InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert": {
      "local_id": "QueueInsert",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq::BufferCapture": {
      "local_id": "BufferCapture",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::ParentDeqHandshake": {
      "local_id": "ParentDeqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::ParentEnqHandshake": {
      "local_id": "ParentEnqHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1::CommitRefillBeat": {
      "local_id": "CommitRefillBeat",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::CommitRefillDone": {
      "local_id": "CommitRefillDone",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::FinalMetaWrite": {
      "local_id": "FinalMetaWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::GrantComplete": {
      "local_id": "GrantComplete",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::GrantDataWrite": {
      "local_id": "GrantDataWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::MemAcquire": {
      "local_id": "MemAcquire",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::MemFinish": {
      "local_id": "MemFinish",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::MemGrant": {
      "local_id": "MemGrant",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::MetaClearWrite": {
      "local_id": "MetaClearWrite",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::MetaRead": {
      "local_id": "MetaRead",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::PrimaryAccept": {
      "local_id": "PrimaryAccept",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::RPQDrained": {
      "local_id": "RPQDrained",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::ReplayHandshake": {
      "local_id": "ReplayHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::RespHandshake": {
      "local_id": "RespHandshake",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::WBComplete": {
      "local_id": "WBComplete",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    },
    "BoomMSHRFile.mshrs_1::WBReq": {
      "local_id": "WBReq",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
    }
  },
  "predicates": {
    "BoomMSHRFile.mshrs_1.rpq.main::HeadInvalid": {
      "local_id": "HeadInvalid",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::HeadValid": {
      "local_id": "HeadValid",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::IncomingBranchKilled": {
      "local_id": "IncomingBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::IncomingFlushKilled": {
      "local_id": "IncomingFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::QueueEmpty": {
      "local_id": "QueueEmpty",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq.main::QueueFull": {
      "local_id": "QueueFull",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
    },
    "BoomMSHRFile.mshrs_1.rpq::OutputInvalid": {
      "local_id": "OutputInvalid",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::TransferBranchKilled": {
      "local_id": "TransferBranchKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1.rpq::TransferFlushKilled": {
      "local_id": "TransferFlushKilled",
      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
    },
    "BoomMSHRFile.mshrs_1::GrantAckAbsent": {
      "local_id": "GrantAckAbsent",
      "work_unit_id": "BoomMSHRFile.mshrs_1"
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
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1102,
        1104,
        1106,
        1107,
        1119,
        1346,
        1348,
        1350,
        1351,
        1352,
        1353,
        1840,
        1842,
        1974,
        1975,
        1988,
        2215
      ],
      "formal": {
        "after": "MemAcquire",
        "before": "PrimaryAccept",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A1",
      "rendered_formula": "PrimaryAccept <mu MemAcquire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1348,
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364
      ],
      "formal": {
        "after": "MemGrant",
        "before": "MemAcquire",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A2",
      "rendered_formula": "MemAcquire <mu MemGrant",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1444,
        1455,
        1456,
        1459,
        1460
      ],
      "formal": {
        "after": "RespHandshake",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A3",
      "rendered_formula": "GrantComplete <mu RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1367,
        1377,
        1525,
        1526,
        1533,
        1534,
        1535,
        1536
      ],
      "formal": {
        "after": "MetaRead",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A4",
      "rendered_formula": "GrantComplete <mu MetaRead",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_VictimWriteback"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "formal": {
        "scope_identity": null,
        "scope_index": null,
        "sequence": [
          "MetaRead",
          "MetaClearWrite",
          "WBReq",
          "WBComplete"
        ],
        "type": "ordered_chain"
      },
      "id": "A5",
      "rendered_formula": "MetaRead <mu MetaClearWrite <mu WBReq <mu WBComplete",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_VictimWriteback",
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1637,
        1640,
        1641,
        1642
      ],
      "formal": {
        "after": "CommitRefillBeat",
        "before": "MetaRead",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A6",
      "rendered_formula": "MetaRead <mu CommitRefillBeat",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1111,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648,
        1980
      ],
      "formal": {
        "cardinality": "exactly_once",
        "completion": "CommitRefillDone",
        "domain": {
          "end_exclusive": 8,
          "start": 0
        },
        "index": "beat",
        "occurrence": "CommitRefillBeat",
        "scope_identity": null,
        "scope_index": null,
        "type": "indexed_complete"
      },
      "id": "A7",
      "rendered_formula": "CommitRefillDone => forall beat in [0, 8): count(CommitRefillBeat(beat)) = 1",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C6_FinalMetadataCommit"
      ],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "formal": {
        "after": "FinalMetaWrite",
        "before": "RPQDrained",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A8",
      "rendered_formula": "RPQDrained <mu FinalMetaWrite",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted",
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1367,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "formal": {
        "after": "MemFinish",
        "before": "GrantComplete",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A9",
      "rendered_formula": "GrantComplete <mu MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1825,
        1827,
        1828,
        1829,
        1830,
        1831,
        1832
      ],
      "formal": {
        "occurrence": "MemFinish",
        "predicate": "GrantAckAbsent",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A10",
      "rendered_formula": "GrantAckAbsent => !MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_GrantCompleted"
      ],
      "evidence_statement_ids": [
        1093,
        1358,
        1359,
        1360
      ],
      "formal": {
        "on": "GrantDataWrite",
        "scope_identity": null,
        "source": {
          "name": "io.mem_grant.bits.data",
          "op": "signal"
        },
        "target": "io.lb_write.bits.data",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.lb_write.bits.data = io.mem_grant.bits.data on GrantDataWrite",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C4_CommitLineRefill"
      ],
      "evidence_statement_ids": [
        1067,
        1637,
        1640,
        1641
      ],
      "formal": {
        "on": "CommitRefillBeat",
        "scope_identity": null,
        "source": {
          "name": "io.lb_resp",
          "op": "signal"
        },
        "target": "io.refill.bits.data",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.refill.bits.data = io.lb_resp on CommitRefillBeat",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C7_GrantFinish"
      ],
      "evidence_statement_ids": [
        1089,
        1374,
        1375,
        1827,
        1828
      ],
      "formal": {
        "on": "MemFinish",
        "scope_identity": null,
        "source": {
          "name": "grantack.bits.sink",
          "op": "signal"
        },
        "target": "io.mem_finish.bits.sink",
        "type": "signal_equality"
      },
      "id": "A13",
      "rendered_formula": "io.mem_finish.bits.sink = grantack.bits.sink on MemFinish",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_LoadResponse"
      ],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505
      ],
      "formal": {
        "after": "RespHandshake",
        "before": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A14",
      "rendered_formula": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert <mu RespHandshake",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C5_ReplayDrain"
      ],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "formal": {
        "after": "ReplayHandshake",
        "before": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert",
        "required_prior": null,
        "scope_identity": null,
        "type": "ordered_before"
      },
      "id": "A15",
      "rendered_formula": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert <mu ReplayHandshake",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1350,
        1351,
        1352,
        1353,
        1355,
        1357,
        1363,
        1364,
        1367,
        1372,
        1375,
        1377
      ],
      "guard_predicates": [],
      "id": "C1_GrantCompleted",
      "relations": [
        "The memory response completes only after the MSHR has issued its current Acquire; the completed Grant may subsequently feed direct load responses, metadata processing, or replay drain."
      ],
      "trigger_occurrences": [
        "GrantComplete"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ],
      "guard_predicates": [],
      "id": "C2_LoadResponse",
      "relations": [
        "A direct load response occurs only on the post-Grant load-drain path and consumes an entry from the frozen RPQ dequeue stream."
      ],
      "trigger_occurrences": [
        "RespHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1525,
        1533,
        1534,
        1535,
        1536,
        1613,
        1614,
        1615,
        1616,
        1618,
        1620,
        1621,
        1622,
        1623,
        1625,
        1627,
        1628,
        1629,
        1630,
        1632,
        1633,
        1634,
        1635
      ],
      "guard_predicates": [],
      "id": "C3_VictimWriteback",
      "relations": [
        "The victim-writeback path performs a metadata read, clears the victim metadata, issues a writeback request, and waits for io.wb_resp before entering line commit."
      ],
      "trigger_occurrences": [
        "WBComplete"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1637,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ],
      "guard_predicates": [],
      "id": "C4_CommitLineRefill",
      "relations": [
        "The commit-line phase emits exactly the eight refill indices 0 through 7 before entering replay drain."
      ],
      "trigger_occurrences": [
        "CommitRefillDone"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1650,
        1652,
        1653,
        1654,
        1660
      ],
      "guard_predicates": [],
      "id": "C5_ReplayDrain",
      "relations": [
        "Replay handshakes are direct parent-local exposures of the frozen RPQ dequeue stream while state is s_drain_rpq."
      ],
      "trigger_occurrences": [
        "ReplayHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811,
        1813,
        1815,
        1820,
        1821,
        1822
      ],
      "guard_predicates": [],
      "id": "C6_FinalMetadataCommit",
      "relations": [
        "The final metadata update is reached only after the replay queue is observed empty with no concurrent enqueue."
      ],
      "trigger_occurrences": [
        "FinalMetaWrite"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        1089,
        1372,
        1374,
        1375,
        1825,
        1827,
        1828,
        1832
      ],
      "guard_predicates": [
        {
          "id": "GrantAckAbsent",
          "positive": false
        }
      ],
      "id": "C7_GrantFinish",
      "relations": [
        "A visible TileLink GrantAck handshake requires a valid stored grant acknowledgement derived from an earlier completed Grant."
      ],
      "trigger_occurrences": [
        "MemFinish"
      ]
    }
  ],
  "composition": {
    "imports": [
      {
        "child_id": "BoomMSHRFile.mshrs_1.rpq",
        "child_kind": "module",
        "frozen_umcm": {
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
                "predicate": "BoomMSHRFile.mshrs_1.rpq.main::QueueFull",
                "scope_identity": null,
                "type": "forbid_when"
              },
              "id": "A1",
              "rendered_formula": "BoomMSHRFile.mshrs_1.rpq.main::QueueFull => !ParentEnqHandshake",
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
                "before": "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake",
                "required_prior": null,
                "scope_identity": null,
                "type": "ordered_before"
              },
              "id": "A4",
              "rendered_formula": "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake <mu ParentDeqHandshake",
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
                "before": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert",
                "required_prior": null,
                "scope_identity": null,
                "type": "ordered_before"
              },
              "id": "A5",
              "rendered_formula": "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert <mu ParentDeqHandshake",
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
                "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake"
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
                "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake"
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
                "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake"
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
                "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake"
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
                "child_id": "BoomMSHRFile.mshrs_1.rpq.main",
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
                        "BoomMSHRFile.mshrs_1.rpq.main::io.enq.fire"
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
                        "BoomMSHRFile.mshrs_1.rpq.main::io.deq.fire"
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
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "frozen_umcm_sha256": "30294c8bb95cab00d6b8a631cca540a4d5c2bd5f00f1f8180ae02b046584fe32",
                "semantic_catalog": {
                  "axioms": {
                    "BoomMSHRFile.mshrs_1.rpq.main::A1": {
                      "local_id": "A1",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A11": {
                      "local_id": "A11",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A2": {
                      "local_id": "A2",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A3": {
                      "local_id": "A3",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A4": {
                      "local_id": "A4",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A5": {
                      "local_id": "A5",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A6": {
                      "local_id": "A6",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A7": {
                      "local_id": "A7",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::A8": {
                      "local_id": "A8",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    }
                  },
                  "cases": {
                    "BoomMSHRFile.mshrs_1.rpq.main::C1_Admitted": {
                      "local_id": "C1_Admitted",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::C2_BranchKilledOnArrival": {
                      "local_id": "C2_BranchKilledOnArrival",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::C3_FlushKilledOnArrival": {
                      "local_id": "C3_FlushKilledOnArrival",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::C4_VisibleDequeue": {
                      "local_id": "C4_VisibleDequeue",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::C5_InvalidHeadSkip": {
                      "local_id": "C5_InvalidHeadSkip",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    }
                  },
                  "identity_keys": {},
                  "occurrences": {
                    "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake": {
                      "local_id": "DeqHandshake",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake": {
                      "local_id": "EnqHandshake",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::InvalidHeadSkip": {
                      "local_id": "InvalidHeadSkip",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert": {
                      "local_id": "QueueInsert",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    }
                  },
                  "predicates": {
                    "BoomMSHRFile.mshrs_1.rpq.main::HeadInvalid": {
                      "local_id": "HeadInvalid",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::HeadValid": {
                      "local_id": "HeadValid",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::IncomingBranchKilled": {
                      "local_id": "IncomingBranchKilled",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::IncomingFlushKilled": {
                      "local_id": "IncomingFlushKilled",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::QueueEmpty": {
                      "local_id": "QueueEmpty",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                    },
                    "BoomMSHRFile.mshrs_1.rpq.main::QueueFull": {
                      "local_id": "QueueFull",
                      "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
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
                "BoomMSHRFile.mshrs_1.rpq.main::A1": {
                  "local_id": "A1",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A11": {
                  "local_id": "A11",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A2": {
                  "local_id": "A2",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A3": {
                  "local_id": "A3",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A4": {
                  "local_id": "A4",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A5": {
                  "local_id": "A5",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A6": {
                  "local_id": "A6",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A7": {
                  "local_id": "A7",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::A8": {
                  "local_id": "A8",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq::A1": {
                  "local_id": "A1",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A2": {
                  "local_id": "A2",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A3": {
                  "local_id": "A3",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A4": {
                  "local_id": "A4",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A5": {
                  "local_id": "A5",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A6": {
                  "local_id": "A6",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::A7": {
                  "local_id": "A7",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                }
              },
              "cases": {
                "BoomMSHRFile.mshrs_1.rpq.main::C1_Admitted": {
                  "local_id": "C1_Admitted",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::C2_BranchKilledOnArrival": {
                  "local_id": "C2_BranchKilledOnArrival",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::C3_FlushKilledOnArrival": {
                  "local_id": "C3_FlushKilledOnArrival",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::C4_VisibleDequeue": {
                  "local_id": "C4_VisibleDequeue",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::C5_InvalidHeadSkip": {
                  "local_id": "C5_InvalidHeadSkip",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq::C1_EnqueueForwarded": {
                  "local_id": "C1_EnqueueForwarded",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::C2_ChildDequeueCaptured": {
                  "local_id": "C2_ChildDequeueCaptured",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::C3_ChildDequeueBranchKilled": {
                  "local_id": "C3_ChildDequeueBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::C4_ChildDequeueFlushKilled": {
                  "local_id": "C4_ChildDequeueFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::C5_VisibleParentDequeue": {
                  "local_id": "C5_VisibleParentDequeue",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                }
              },
              "identity_keys": {},
              "occurrences": {
                "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake": {
                  "local_id": "DeqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake": {
                  "local_id": "EnqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::InvalidHeadSkip": {
                  "local_id": "InvalidHeadSkip",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert": {
                  "local_id": "QueueInsert",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq::BufferCapture": {
                  "local_id": "BufferCapture",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::ParentDeqHandshake": {
                  "local_id": "ParentDeqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::ParentEnqHandshake": {
                  "local_id": "ParentEnqHandshake",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                }
              },
              "predicates": {
                "BoomMSHRFile.mshrs_1.rpq.main::HeadInvalid": {
                  "local_id": "HeadInvalid",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::HeadValid": {
                  "local_id": "HeadValid",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::IncomingBranchKilled": {
                  "local_id": "IncomingBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::IncomingFlushKilled": {
                  "local_id": "IncomingFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::QueueEmpty": {
                  "local_id": "QueueEmpty",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq.main::QueueFull": {
                  "local_id": "QueueFull",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
                },
                "BoomMSHRFile.mshrs_1.rpq::OutputInvalid": {
                  "local_id": "OutputInvalid",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::TransferBranchKilled": {
                  "local_id": "TransferBranchKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
                },
                "BoomMSHRFile.mshrs_1.rpq::TransferFlushKilled": {
                  "local_id": "TransferFlushKilled",
                  "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
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
                "BoomMSHRFile.mshrs_1.rpq::io.enq.fire"
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
                "BoomMSHRFile.mshrs_1.rpq::io.deq.fire"
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
                "BoomMSHRFile.mshrs_1.rpq.main::A1"
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
                "BoomMSHRFile.mshrs_1.rpq.main::A11"
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
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "frozen_umcm_sha256": "7e5d8d97f50b8fea9b9f52ab96be1da09d25d73910fd16d3229389ef3891c528",
        "semantic_catalog": {
          "axioms": {
            "BoomMSHRFile.mshrs_1.rpq.main::A1": {
              "local_id": "A1",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A11": {
              "local_id": "A11",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A2": {
              "local_id": "A2",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A3": {
              "local_id": "A3",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A4": {
              "local_id": "A4",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A5": {
              "local_id": "A5",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A6": {
              "local_id": "A6",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A7": {
              "local_id": "A7",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::A8": {
              "local_id": "A8",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq::A1": {
              "local_id": "A1",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A2": {
              "local_id": "A2",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A3": {
              "local_id": "A3",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A4": {
              "local_id": "A4",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A5": {
              "local_id": "A5",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A6": {
              "local_id": "A6",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::A7": {
              "local_id": "A7",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            }
          },
          "cases": {
            "BoomMSHRFile.mshrs_1.rpq.main::C1_Admitted": {
              "local_id": "C1_Admitted",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::C2_BranchKilledOnArrival": {
              "local_id": "C2_BranchKilledOnArrival",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::C3_FlushKilledOnArrival": {
              "local_id": "C3_FlushKilledOnArrival",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::C4_VisibleDequeue": {
              "local_id": "C4_VisibleDequeue",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::C5_InvalidHeadSkip": {
              "local_id": "C5_InvalidHeadSkip",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq::C1_EnqueueForwarded": {
              "local_id": "C1_EnqueueForwarded",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::C2_ChildDequeueCaptured": {
              "local_id": "C2_ChildDequeueCaptured",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::C3_ChildDequeueBranchKilled": {
              "local_id": "C3_ChildDequeueBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::C4_ChildDequeueFlushKilled": {
              "local_id": "C4_ChildDequeueFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::C5_VisibleParentDequeue": {
              "local_id": "C5_VisibleParentDequeue",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            }
          },
          "identity_keys": {},
          "occurrences": {
            "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake": {
              "local_id": "DeqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake": {
              "local_id": "EnqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::InvalidHeadSkip": {
              "local_id": "InvalidHeadSkip",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert": {
              "local_id": "QueueInsert",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq::BufferCapture": {
              "local_id": "BufferCapture",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::ParentDeqHandshake": {
              "local_id": "ParentDeqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::ParentEnqHandshake": {
              "local_id": "ParentEnqHandshake",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            }
          },
          "predicates": {
            "BoomMSHRFile.mshrs_1.rpq.main::HeadInvalid": {
              "local_id": "HeadInvalid",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::HeadValid": {
              "local_id": "HeadValid",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::IncomingBranchKilled": {
              "local_id": "IncomingBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::IncomingFlushKilled": {
              "local_id": "IncomingFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::QueueEmpty": {
              "local_id": "QueueEmpty",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq.main::QueueFull": {
              "local_id": "QueueFull",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
            },
            "BoomMSHRFile.mshrs_1.rpq::OutputInvalid": {
              "local_id": "OutputInvalid",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::TransferBranchKilled": {
              "local_id": "TransferBranchKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            },
            "BoomMSHRFile.mshrs_1.rpq::TransferFlushKilled": {
              "local_id": "TransferFlushKilled",
              "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
            }
          }
        },
        "summary_ref": "umcm://BoomMSHR.rpq",
        "task_id": "parent_synthesis-BoomMSHR.rpq-38a6826dc8c3b9dc"
      }
    ],
    "mode": "parent_synthesis",
    "note": "Child RTL is not part of this frozen parent. Imported child \u00b5MCMs remain frozen semantic components; descendant semantic names are transparently propagated in v0.1 for higher-level synthesis.",
    "policy": "transparent-frozen-child-imports-v0.1",
    "semantic_catalog": {
      "axioms": {
        "BoomMSHRFile.mshrs_1.rpq.main::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A11": {
          "local_id": "A11",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::A8": {
          "local_id": "A8",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1::A1": {
          "local_id": "A1",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A10": {
          "local_id": "A10",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A11": {
          "local_id": "A11",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A12": {
          "local_id": "A12",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A13": {
          "local_id": "A13",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A14": {
          "local_id": "A14",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A15": {
          "local_id": "A15",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A2": {
          "local_id": "A2",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A3": {
          "local_id": "A3",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A4": {
          "local_id": "A4",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A5": {
          "local_id": "A5",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A6": {
          "local_id": "A6",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A7": {
          "local_id": "A7",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A8": {
          "local_id": "A8",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::A9": {
          "local_id": "A9",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        }
      },
      "cases": {
        "BoomMSHRFile.mshrs_1.rpq.main::C1_Admitted": {
          "local_id": "C1_Admitted",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::C2_BranchKilledOnArrival": {
          "local_id": "C2_BranchKilledOnArrival",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::C3_FlushKilledOnArrival": {
          "local_id": "C3_FlushKilledOnArrival",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::C4_VisibleDequeue": {
          "local_id": "C4_VisibleDequeue",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::C5_InvalidHeadSkip": {
          "local_id": "C5_InvalidHeadSkip",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq::C1_EnqueueForwarded": {
          "local_id": "C1_EnqueueForwarded",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::C2_ChildDequeueCaptured": {
          "local_id": "C2_ChildDequeueCaptured",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::C3_ChildDequeueBranchKilled": {
          "local_id": "C3_ChildDequeueBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::C4_ChildDequeueFlushKilled": {
          "local_id": "C4_ChildDequeueFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::C5_VisibleParentDequeue": {
          "local_id": "C5_VisibleParentDequeue",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1::C1_GrantCompleted": {
          "local_id": "C1_GrantCompleted",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C2_LoadResponse": {
          "local_id": "C2_LoadResponse",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C3_VictimWriteback": {
          "local_id": "C3_VictimWriteback",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C4_CommitLineRefill": {
          "local_id": "C4_CommitLineRefill",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C5_ReplayDrain": {
          "local_id": "C5_ReplayDrain",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C6_FinalMetadataCommit": {
          "local_id": "C6_FinalMetadataCommit",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::C7_GrantFinish": {
          "local_id": "C7_GrantFinish",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        }
      },
      "identity_keys": {},
      "occurrences": {
        "BoomMSHRFile.mshrs_1.rpq.main::DeqHandshake": {
          "local_id": "DeqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::EnqHandshake": {
          "local_id": "EnqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::InvalidHeadSkip": {
          "local_id": "InvalidHeadSkip",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::QueueInsert": {
          "local_id": "QueueInsert",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq::BufferCapture": {
          "local_id": "BufferCapture",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::ParentDeqHandshake": {
          "local_id": "ParentDeqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::ParentEnqHandshake": {
          "local_id": "ParentEnqHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1::CommitRefillBeat": {
          "local_id": "CommitRefillBeat",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::CommitRefillDone": {
          "local_id": "CommitRefillDone",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::FinalMetaWrite": {
          "local_id": "FinalMetaWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::GrantComplete": {
          "local_id": "GrantComplete",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::GrantDataWrite": {
          "local_id": "GrantDataWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::MemAcquire": {
          "local_id": "MemAcquire",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::MemFinish": {
          "local_id": "MemFinish",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::MemGrant": {
          "local_id": "MemGrant",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::MetaClearWrite": {
          "local_id": "MetaClearWrite",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::MetaRead": {
          "local_id": "MetaRead",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::PrimaryAccept": {
          "local_id": "PrimaryAccept",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::RPQDrained": {
          "local_id": "RPQDrained",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::ReplayHandshake": {
          "local_id": "ReplayHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::RespHandshake": {
          "local_id": "RespHandshake",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::WBComplete": {
          "local_id": "WBComplete",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        },
        "BoomMSHRFile.mshrs_1::WBReq": {
          "local_id": "WBReq",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        }
      },
      "predicates": {
        "BoomMSHRFile.mshrs_1.rpq.main::HeadInvalid": {
          "local_id": "HeadInvalid",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::HeadValid": {
          "local_id": "HeadValid",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::IncomingBranchKilled": {
          "local_id": "IncomingBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::IncomingFlushKilled": {
          "local_id": "IncomingFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::QueueEmpty": {
          "local_id": "QueueEmpty",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq.main::QueueFull": {
          "local_id": "QueueFull",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq.main"
        },
        "BoomMSHRFile.mshrs_1.rpq::OutputInvalid": {
          "local_id": "OutputInvalid",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::TransferBranchKilled": {
          "local_id": "TransferBranchKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1.rpq::TransferFlushKilled": {
          "local_id": "TransferFlushKilled",
          "work_unit_id": "BoomMSHRFile.mshrs_1.rpq"
        },
        "BoomMSHRFile.mshrs_1::GrantAckAbsent": {
          "local_id": "GrantAckAbsent",
          "work_unit_id": "BoomMSHRFile.mshrs_1"
        }
      }
    }
  },
  "freeze": {
    "candidate_axiom_count": 15,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 15
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "(state == s_invalid || state == s_prefetch) && io.req_pri_val && io.req_pri_rdy; a primary request is accepted and becomes the current MSHR request",
      "evidence_statement_ids": [
        1102,
        1103,
        1104,
        1106,
        1107,
        1119,
        1346,
        1840,
        1841,
        1842,
        1974,
        1975,
        1988,
        2215
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.req_pri_val",
          "io.req_pri_rdy"
        ],
        "state_register": "state",
        "state_values": [
          0,
          17
        ]
      },
      "id": "PrimaryAccept",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_refill_req && io.mem_acquire.valid && io.mem_acquire.ready",
      "evidence_statement_ids": [
        1348,
        1349,
        1350,
        1351,
        1352,
        1353
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          1
        ]
      },
      "id": "MemAcquire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.mem_acquire.fire"
      ]
    },
    {
      "definition": "state == s_refill_resp && io.mem_grant.valid && io.mem_grant.ready",
      "evidence_statement_ids": [
        1355,
        1356,
        1357,
        1363,
        1364
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "MemGrant",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.mem_grant.fire"
      ]
    },
    {
      "definition": "state == s_refill_resp && io.lb_write.valid; a data-bearing memory Grant is forwarded into the line buffer",
      "evidence_statement_ids": [
        1355,
        1356,
        1358,
        1359,
        1360
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.lb_write.valid"
        ],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "GrantDataWrite",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.lb_write.valid"
      ]
    },
    {
      "definition": "state == s_refill_resp && refill_done; the final accepted TileLink Grant beat completes the memory response and captures GrantAck/coherence state",
      "evidence_statement_ids": [
        604,
        614,
        615,
        616,
        617,
        618,
        1367,
        1372,
        1375,
        1377
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "refill_done"
        ],
        "state_register": "state",
        "state_values": [
          2
        ]
      },
      "id": "GrantComplete",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_meta_read && io.meta_read.valid && io.meta_read.ready",
      "evidence_statement_ids": [
        1525,
        1526,
        1527,
        1528,
        1529,
        1530,
        1531,
        1532,
        1533,
        1534,
        1535,
        1536
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          4
        ]
      },
      "id": "MetaRead",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.meta_read.fire"
      ]
    },
    {
      "definition": "state == s_meta_clear && io.meta_write.valid && io.meta_write.ready; the victim metadata is cleared before writeback",
      "evidence_statement_ids": [
        1618,
        1619,
        1620,
        1621,
        1622,
        1623
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "state_register": "state",
        "state_values": [
          7
        ]
      },
      "id": "MetaClearWrite",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_wb_req && io.wb_req.valid && io.wb_req.ready",
      "evidence_statement_ids": [
        1625,
        1626,
        1627,
        1628,
        1629,
        1630
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          9
        ]
      },
      "id": "WBReq",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.wb_req.fire"
      ]
    },
    {
      "definition": "state == s_wb_resp && io.wb_resp; the requested victim writeback has completed",
      "evidence_statement_ids": [
        1632,
        1633,
        1634,
        1635
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.wb_resp"
        ],
        "state_register": "state",
        "state_values": [
          10
        ]
      },
      "id": "WBComplete",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_commit_line && io.refill.valid && io.refill.ready; one cache-line commit beat is accepted",
      "evidence_statement_ids": [
        1637,
        1638,
        1640,
        1641,
        1642,
        1643,
        1644,
        1645
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          11
        ]
      },
      "id": "CommitRefillBeat",
      "index": {
        "domain": {
          "end_exclusive": 8,
          "start": 0
        },
        "expr": {
          "name": "refill_ctr",
          "op": "signal"
        },
        "name": "beat"
      },
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.refill.fire"
      ]
    },
    {
      "definition": "state == s_commit_line && io.refill.fire && refill_ctr == 7; the eighth and final commit refill beat is accepted and the MSHR enters replay drain",
      "evidence_statement_ids": [
        1641,
        1642,
        1643,
        1644,
        1645,
        1646,
        1647,
        1648
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "_T_44",
          "_T_45"
        ],
        "state_register": "state",
        "state_values": [
          11
        ]
      },
      "id": "CommitRefillDone",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_drain_rpq_loads && io.resp.valid && io.resp.ready; a load replay-queue entry is returned directly as a load response",
      "evidence_statement_ids": [
        1444,
        1455,
        1456,
        1459,
        1460,
        1505,
        1506,
        1507
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          3
        ]
      },
      "id": "RespHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.resp.fire"
      ]
    },
    {
      "definition": "state == s_drain_rpq && io.replay.valid && io.replay.ready; an RPQ entry is emitted through the replay interface",
      "evidence_statement_ids": [
        1650,
        1651,
        1652,
        1653,
        1654,
        1660
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          12
        ]
      },
      "id": "ReplayHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.replay.fire"
      ]
    },
    {
      "definition": "state == s_drain_rpq && rpq.io.empty && !rpq.io.enq.valid; no queued or concurrently incoming replay remains, so the MSHR may proceed to final metadata commit",
      "evidence_statement_ids": [
        1808,
        1809,
        1810,
        1811
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "_T_76"
        ],
        "state_register": "state",
        "state_values": [
          12
        ]
      },
      "id": "RPQDrained",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_meta_write_req && io.meta_write.valid && io.meta_write.ready; the final acquired-line metadata is committed after RPQ drain",
      "evidence_statement_ids": [
        1813,
        1814,
        1815,
        1816,
        1817,
        1818,
        1819,
        1820,
        1821,
        1822
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [
          "io.meta_write.valid",
          "io.meta_write.ready"
        ],
        "state_register": "state",
        "state_values": [
          13
        ]
      },
      "id": "FinalMetaWrite",
      "index": null,
      "kind": "derived",
      "multiplicity": "repeatable",
      "physical_event_ids": []
    },
    {
      "definition": "state == s_mem_finish_1 && io.mem_finish.valid && io.mem_finish.ready",
      "evidence_statement_ids": [
        1089,
        1825,
        1826,
        1827,
        1828
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": "state",
        "state_values": [
          14
        ]
      },
      "id": "MemFinish",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.mshrs_1::io.mem_finish.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "grantack.valid == 0",
      "evidence_statement_ids": [
        900,
        1110,
        1372,
        1827,
        1832
      ],
      "grounding": {
        "negated": true,
        "source_signal": "grantack.valid",
        "state_register": null,
        "state_values": []
      },
      "id": "GrantAckAbsent"
    }
  ],
  "provenance": {
    "A1": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A10": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-combinational-exclusion",
      "source_axioms": []
    },
    "A11": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A12": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A13": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-symbolic-driver-equality",
      "source_axioms": []
    },
    "A14": {
      "derivation": "formal-certificate-v0.1",
      "kind": "emergent",
      "proof_method": "trusted-history-after-restriction",
      "source_axioms": [
        "BoomMSHRFile.mshrs_1.rpq::A5"
      ]
    },
    "A15": {
      "derivation": "formal-certificate-v0.1",
      "kind": "emergent",
      "proof_method": "trusted-history-after-restriction",
      "source_axioms": [
        "BoomMSHRFile.mshrs_1.rpq::A5"
      ]
    },
    "A2": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A3": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A4": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A5": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A6": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A7": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exact-bounded-indexed-occurrence",
      "source_axioms": []
    },
    "A8": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    },
    "A9": {
      "derivation": "formal-certificate-v0.1",
      "kind": "parent_local",
      "proof_method": "exhaustive-state-reachability",
      "source_axioms": []
    }
  },
  "schema_version": "umcm-formal-0.5",
  "task_id": "parent_synthesis-BoomMSHR-6362a83e7f824669",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A15",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.mshrs_1"
}
```

### Child `BoomMSHRFile.prefetcher`
- summary ref: `umcm://BoomMSHRFile.prefetcher`
- frozen task: `leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac`
- frozen SHA-256: `d406a1ba99491ffb3942ef1d38e092640acb24becf34c54db0d8240f50fe3ac0`
- implementation SHA-256: `a407d421b5a9628d2f87270c313e9bad45c33f2feec63bd74bd2d1ba731e4b55`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.prefetcher', 'target_work_unit_id': 'BoomMSHRFile.prefetcher', 'module': 'NullPrefetcher', 'implementation_sha256': 'a407d421b5a9628d2f87270c313e9bad45c33f2feec63bd74bd2d1ba731e4b55', 'structural_implementation_sha256': '8d207f66e37d40a8764c90493df01c250fe7193cb411ba07703d42a176653911', 'source_module': 'NullPrefetcher', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.prefetcher::io.prefetch.fire']
- frontier signals: ['prefetcher.clock', 'prefetcher.io', 'prefetcher.io.mshr_avail', 'prefetcher.io.prefetch.bits.addr', 'prefetcher.io.prefetch.bits.data', 'prefetcher.io.prefetch.bits.is_hella', 'prefetcher.io.prefetch.bits.uop.bp_debug_if', 'prefetcher.io.prefetch.bits.uop.bp_xcpt_if', 'prefetcher.io.prefetch.bits.uop.br_mask', 'prefetcher.io.prefetch.bits.uop.br_tag', 'prefetcher.io.prefetch.bits.uop.br_type', 'prefetcher.io.prefetch.bits.uop.csr_cmd', 'prefetcher.io.prefetch.bits.uop.debug_fsrc', 'prefetcher.io.prefetch.bits.uop.debug_inst', 'prefetcher.io.prefetch.bits.uop.debug_pc', 'prefetcher.io.prefetch.bits.uop.debug_tsrc', 'prefetcher.io.prefetch.bits.uop.dis_col_sel', 'prefetcher.io.prefetch.bits.uop.dst_rtype', 'prefetcher.io.prefetch.bits.uop.edge_inst', 'prefetcher.io.prefetch.bits.uop.exc_cause', 'prefetcher.io.prefetch.bits.uop.exception', 'prefetcher.io.prefetch.bits.uop.fcn_dw', 'prefetcher.io.prefetch.bits.uop.fcn_op', 'prefetcher.io.prefetch.bits.uop.flush_on_commit', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.div', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.fastpipe', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.fma', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.fromint', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.ldst', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.ren1', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.ren2', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.ren3', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.sqrt', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.swap12', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.swap23', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.toint', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.typeTagIn', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.typeTagOut', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.vec', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.wen', 'prefetcher.io.prefetch.bits.uop.fp_ctrl.wflags', 'prefetcher.io.prefetch.bits.uop.fp_rm', 'prefetcher.io.prefetch.bits.uop.fp_typ', 'prefetcher.io.prefetch.bits.uop.fp_val', 'prefetcher.io.prefetch.bits.uop.frs3_en', 'prefetcher.io.prefetch.bits.uop.ftq_idx', 'prefetcher.io.prefetch.bits.uop.fu_code[0]', 'prefetcher.io.prefetch.bits.uop.fu_code[1]', 'prefetcher.io.prefetch.bits.uop.fu_code[2]', 'prefetcher.io.prefetch.bits.uop.fu_code[3]', 'prefetcher.io.prefetch.bits.uop.fu_code[4]', 'prefetcher.io.prefetch.bits.uop.fu_code[5]', 'prefetcher.io.prefetch.bits.uop.fu_code[6]', 'prefetcher.io.prefetch.bits.uop.fu_code[7]', 'prefetcher.io.prefetch.bits.uop.fu_code[8]', 'prefetcher.io.prefetch.bits.uop.fu_code[9]', 'prefetcher.io.prefetch.bits.uop.imm_packed', 'prefetcher.io.prefetch.bits.uop.imm_rename', 'prefetcher.io.prefetch.bits.uop.imm_sel', 'prefetcher.io.prefetch.bits.uop.inst', 'prefetcher.io.prefetch.bits.uop.iq_type[0]', 'prefetcher.io.prefetch.bits.uop.iq_type[1]', 'prefetcher.io.prefetch.bits.uop.iq_type[2]', 'prefetcher.io.prefetch.bits.uop.iq_type[3]', 'prefetcher.io.prefetch.bits.uop.is_amo', 'prefetcher.io.prefetch.bits.uop.is_eret', 'prefetcher.io.prefetch.bits.uop.is_fence', 'prefetcher.io.prefetch.bits.uop.is_fencei', 'prefetcher.io.prefetch.bits.uop.is_mov', 'prefetcher.io.prefetch.bits.uop.is_rocc', 'prefetcher.io.prefetch.bits.uop.is_rvc', 'prefetcher.io.prefetch.bits.uop.is_sfb', 'prefetcher.io.prefetch.bits.uop.is_sfence', 'prefetcher.io.prefetch.bits.uop.is_sys_pc2epc', 'prefetcher.io.prefetch.bits.uop.is_unique', 'prefetcher.io.prefetch.bits.uop.iw_issued', 'prefetcher.io.prefetch.bits.uop.iw_issued_partial_agen', 'prefetcher.io.prefetch.bits.uop.iw_issued_partial_dgen', 'prefetcher.io.prefetch.bits.uop.iw_p1_bypass_hint', 'prefetcher.io.prefetch.bits.uop.iw_p1_speculative_child', 'prefetcher.io.prefetch.bits.uop.iw_p2_bypass_hint', 'prefetcher.io.prefetch.bits.uop.iw_p2_speculative_child', 'prefetcher.io.prefetch.bits.uop.iw_p3_bypass_hint', 'prefetcher.io.prefetch.bits.uop.ldq_idx', 'prefetcher.io.prefetch.bits.uop.ldst', 'prefetcher.io.prefetch.bits.uop.ldst_is_rs1', 'prefetcher.io.prefetch.bits.uop.lrs1', 'prefetcher.io.prefetch.bits.uop.lrs1_rtype', 'prefetcher.io.prefetch.bits.uop.lrs2', 'prefetcher.io.prefetch.bits.uop.lrs2_rtype', 'prefetcher.io.prefetch.bits.uop.lrs3', 'prefetcher.io.prefetch.bits.uop.mem_cmd', 'prefetcher.io.prefetch.bits.uop.mem_signed', 'prefetcher.io.prefetch.bits.uop.mem_size', 'prefetcher.io.prefetch.bits.uop.op1_sel', 'prefetcher.io.prefetch.bits.uop.op2_sel', 'prefetcher.io.prefetch.bits.uop.pc_lob', 'prefetcher.io.prefetch.bits.uop.pdst', 'prefetcher.io.prefetch.bits.uop.pimm', 'prefetcher.io.prefetch.bits.uop.ppred', 'prefetcher.io.prefetch.bits.uop.ppred_busy', 'prefetcher.io.prefetch.bits.uop.prs1', 'prefetcher.io.prefetch.bits.uop.prs1_busy', 'prefetcher.io.prefetch.bits.uop.prs2', 'prefetcher.io.prefetch.bits.uop.prs2_busy', 'prefetcher.io.prefetch.bits.uop.prs3', 'prefetcher.io.prefetch.bits.uop.prs3_busy', 'prefetcher.io.prefetch.bits.uop.rob_idx', 'prefetcher.io.prefetch.bits.uop.rxq_idx', 'prefetcher.io.prefetch.bits.uop.stale_pdst', 'prefetcher.io.prefetch.bits.uop.stq_idx', 'prefetcher.io.prefetch.bits.uop.taken', 'prefetcher.io.prefetch.bits.uop.uses_ldq', 'prefetcher.io.prefetch.bits.uop.uses_stq', 'prefetcher.io.prefetch.bits.uop.xcpt_ae_if', 'prefetcher.io.prefetch.bits.uop.xcpt_ma_if', 'prefetcher.io.prefetch.bits.uop.xcpt_pf_if', 'prefetcher.io.prefetch.ready', 'prefetcher.io.prefetch.valid', 'prefetcher.io.req_addr', 'prefetcher.io.req_coh.state', 'prefetcher.io.req_val', 'prefetcher.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.prefetcher::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.prefetcher"
    },
    "BoomMSHRFile.prefetcher::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.prefetcher"
    }
  },
  "cases": {},
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.prefetcher::PrefetchHandshake": {
      "local_id": "PrefetchHandshake",
      "work_unit_id": "BoomMSHRFile.prefetcher"
    }
  },
  "predicates": {
    "BoomMSHRFile.prefetcher::PrefetchDisabled": {
      "local_id": "PrefetchDisabled",
      "work_unit_id": "BoomMSHRFile.prefetcher"
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
        3
      ],
      "formal": {
        "expr": {
          "index": 0,
          "op": "bit",
          "value": {
            "name": "io.prefetch.valid",
            "op": "signal"
          }
        },
        "on": null,
        "relation": "eq",
        "scope_identity": null,
        "type": "value_constraint",
        "value": 0
      },
      "id": "A1",
      "rendered_formula": "bits(io.prefetch.valid, 0, 0) == 0",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [],
      "evidence_statement_ids": [
        3
      ],
      "formal": {
        "occurrence": "PrefetchHandshake",
        "predicate": "PrefetchDisabled",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "PrefetchDisabled => !PrefetchHandshake",
      "status": "candidate"
    }
  ],
  "cases": [],
  "freeze": {
    "candidate_axiom_count": 2,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 2
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.prefetch.valid && io.prefetch.ready",
      "evidence_statement_ids": [
        3
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "PrefetchHandshake",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.prefetcher::io.prefetch.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.prefetch.valid == 0",
      "evidence_statement_ids": [
        3
      ],
      "grounding": {
        "negated": true,
        "source_signal": "io.prefetch.valid",
        "state_register": null,
        "state_values": []
      },
      "id": "PrefetchDisabled"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2"
  ],
  "work_unit_id": "BoomMSHRFile.prefetcher"
}
```

### Child `BoomMSHRFile.refill_arb`
- summary ref: `umcm://BoomMSHRFile.refill_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.refill_arb-af45d6b6d169fc58`
- frozen SHA-256: `c329fbb606e7912cac4bf07b76da833b7321329ba781bb1b5a5af611bb42a833`
- implementation SHA-256: `abeb8039ba76af7a71646cc45705f7a865ba1b892e3fa7fda5d743f8e73f916c`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.refill_arb', 'target_work_unit_id': 'BoomMSHRFile.refill_arb', 'module': 'Arbiter2_L1DataWriteReq', 'implementation_sha256': 'abeb8039ba76af7a71646cc45705f7a865ba1b892e3fa7fda5d743f8e73f916c', 'structural_implementation_sha256': '0ee0ce62e7c42e5388c1cc87b47807d546882acccc1be9c75866c45f4636f74c', 'source_module': 'Arbiter2_L1DataWriteReq', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.refill_arb::io.in[0].fire', 'BoomMSHRFile.refill_arb::io.in[1].fire', 'BoomMSHRFile.refill_arb::io.out.fire']
- frontier signals: ['refill_arb.clock', 'refill_arb.io', 'refill_arb.io.chosen', 'refill_arb.io.in[0].bits.addr', 'refill_arb.io.in[0].bits.data', 'refill_arb.io.in[0].bits.way_en', 'refill_arb.io.in[0].bits.wmask', 'refill_arb.io.in[0].ready', 'refill_arb.io.in[0].valid', 'refill_arb.io.in[1].bits.addr', 'refill_arb.io.in[1].bits.data', 'refill_arb.io.in[1].bits.way_en', 'refill_arb.io.in[1].bits.wmask', 'refill_arb.io.in[1].ready', 'refill_arb.io.in[1].valid', 'refill_arb.io.out.bits.addr', 'refill_arb.io.out.bits.data', 'refill_arb.io.out.bits.way_en', 'refill_arb.io.out.bits.wmask', 'refill_arb.io.out.ready', 'refill_arb.io.out.valid', 'refill_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.refill_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.refill_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.refill_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    },
    "BoomMSHRFile.refill_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.refill_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.refill_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.refill_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.addr",
          "op": "signal"
        },
        "target": "io.out.bits.addr",
        "type": "signal_equality"
      },
      "id": "A3",
      "rendered_formula": "io.out.bits.addr = io.in[0].bits.addr on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.data",
          "op": "signal"
        },
        "target": "io.out.bits.data",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.data = io.in[0].bits.data on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.wmask",
          "op": "signal"
        },
        "target": "io.out.bits.wmask",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.wmask = io.in[0].bits.wmask on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.addr",
          "op": "signal"
        },
        "target": "io.out.bits.addr",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.addr = io.in[1].bits.addr on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.data",
          "op": "signal"
        },
        "target": "io.out.bits.data",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.data = io.in[1].bits.data on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.wmask",
          "op": "signal"
        },
        "target": "io.out.bits.wmask",
        "type": "signal_equality"
      },
      "id": "A10",
      "rendered_formula": "io.out.bits.wmask = io.in[1].bits.wmask on Input1Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has fixed priority; an accepted input-0 refill/data-write request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only while input 0 is not valid, and the accepted refill/data-write request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 10,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 10
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        9,
        10
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.refill_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.refill_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        13,
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.refill_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        5,
        8
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.refill_arb-af45d6b6d169fc58",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.refill_arb"
}
```

### Child `BoomMSHRFile.replay_arb`
- summary ref: `umcm://BoomMSHRFile.replay_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.replay_arb-8fdf73acfd546ea3`
- frozen SHA-256: `4ed35d9b8b3162307014c70f35536c0b4b89e211ccc734a54ac161efaf3246b0`
- implementation SHA-256: `9021408029161d8e59d6c04ef6a905a1e852ac48f36efaa886478c0a1c8fdc9a`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.replay_arb', 'target_work_unit_id': 'BoomMSHRFile.replay_arb', 'module': 'Arbiter2_BoomDCacheReqInternal', 'implementation_sha256': '9021408029161d8e59d6c04ef6a905a1e852ac48f36efaa886478c0a1c8fdc9a', 'structural_implementation_sha256': '86dfbb81dc3e5904f47d834de4bc73b1a2e30a6d5bf876cebaba747ce4dfc326', 'source_module': 'Arbiter2_BoomDCacheReqInternal', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.replay_arb::io.in[0].fire', 'BoomMSHRFile.replay_arb::io.in[1].fire', 'BoomMSHRFile.replay_arb::io.out.fire']
- frontier signals: ['replay_arb.clock', 'replay_arb.io', 'replay_arb.io.chosen', 'replay_arb.io.in[0].bits.addr', 'replay_arb.io.in[0].bits.data', 'replay_arb.io.in[0].bits.is_hella', 'replay_arb.io.in[0].bits.old_meta.coh.state', 'replay_arb.io.in[0].bits.old_meta.tag', 'replay_arb.io.in[0].bits.sdq_id', 'replay_arb.io.in[0].bits.tag_match', 'replay_arb.io.in[0].bits.uop.bp_debug_if', 'replay_arb.io.in[0].bits.uop.bp_xcpt_if', 'replay_arb.io.in[0].bits.uop.br_mask', 'replay_arb.io.in[0].bits.uop.br_tag', 'replay_arb.io.in[0].bits.uop.br_type', 'replay_arb.io.in[0].bits.uop.csr_cmd', 'replay_arb.io.in[0].bits.uop.debug_fsrc', 'replay_arb.io.in[0].bits.uop.debug_inst', 'replay_arb.io.in[0].bits.uop.debug_pc', 'replay_arb.io.in[0].bits.uop.debug_tsrc', 'replay_arb.io.in[0].bits.uop.dis_col_sel', 'replay_arb.io.in[0].bits.uop.dst_rtype', 'replay_arb.io.in[0].bits.uop.edge_inst', 'replay_arb.io.in[0].bits.uop.exc_cause', 'replay_arb.io.in[0].bits.uop.exception', 'replay_arb.io.in[0].bits.uop.fcn_dw', 'replay_arb.io.in[0].bits.uop.fcn_op', 'replay_arb.io.in[0].bits.uop.flush_on_commit', 'replay_arb.io.in[0].bits.uop.fp_ctrl.div', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fastpipe', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fma', 'replay_arb.io.in[0].bits.uop.fp_ctrl.fromint', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ldst', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren1', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren2', 'replay_arb.io.in[0].bits.uop.fp_ctrl.ren3', 'replay_arb.io.in[0].bits.uop.fp_ctrl.sqrt', 'replay_arb.io.in[0].bits.uop.fp_ctrl.swap12', 'replay_arb.io.in[0].bits.uop.fp_ctrl.swap23', 'replay_arb.io.in[0].bits.uop.fp_ctrl.toint', 'replay_arb.io.in[0].bits.uop.fp_ctrl.typeTagIn', 'replay_arb.io.in[0].bits.uop.fp_ctrl.typeTagOut', 'replay_arb.io.in[0].bits.uop.fp_ctrl.vec', 'replay_arb.io.in[0].bits.uop.fp_ctrl.wen', 'replay_arb.io.in[0].bits.uop.fp_ctrl.wflags', 'replay_arb.io.in[0].bits.uop.fp_rm', 'replay_arb.io.in[0].bits.uop.fp_typ', 'replay_arb.io.in[0].bits.uop.fp_val', 'replay_arb.io.in[0].bits.uop.frs3_en', 'replay_arb.io.in[0].bits.uop.ftq_idx', 'replay_arb.io.in[0].bits.uop.fu_code[0]', 'replay_arb.io.in[0].bits.uop.fu_code[1]', 'replay_arb.io.in[0].bits.uop.fu_code[2]', 'replay_arb.io.in[0].bits.uop.fu_code[3]', 'replay_arb.io.in[0].bits.uop.fu_code[4]', 'replay_arb.io.in[0].bits.uop.fu_code[5]', 'replay_arb.io.in[0].bits.uop.fu_code[6]', 'replay_arb.io.in[0].bits.uop.fu_code[7]', 'replay_arb.io.in[0].bits.uop.fu_code[8]', 'replay_arb.io.in[0].bits.uop.fu_code[9]', 'replay_arb.io.in[0].bits.uop.imm_packed', 'replay_arb.io.in[0].bits.uop.imm_rename', 'replay_arb.io.in[0].bits.uop.imm_sel', 'replay_arb.io.in[0].bits.uop.inst', 'replay_arb.io.in[0].bits.uop.iq_type[0]', 'replay_arb.io.in[0].bits.uop.iq_type[1]', 'replay_arb.io.in[0].bits.uop.iq_type[2]', 'replay_arb.io.in[0].bits.uop.iq_type[3]', 'replay_arb.io.in[0].bits.uop.is_amo', 'replay_arb.io.in[0].bits.uop.is_eret', 'replay_arb.io.in[0].bits.uop.is_fence', 'replay_arb.io.in[0].bits.uop.is_fencei', 'replay_arb.io.in[0].bits.uop.is_mov', 'replay_arb.io.in[0].bits.uop.is_rocc', 'replay_arb.io.in[0].bits.uop.is_rvc', 'replay_arb.io.in[0].bits.uop.is_sfb', 'replay_arb.io.in[0].bits.uop.is_sfence', 'replay_arb.io.in[0].bits.uop.is_sys_pc2epc', 'replay_arb.io.in[0].bits.uop.is_unique', 'replay_arb.io.in[0].bits.uop.iw_issued', 'replay_arb.io.in[0].bits.uop.iw_issued_partial_agen', 'replay_arb.io.in[0].bits.uop.iw_issued_partial_dgen', 'replay_arb.io.in[0].bits.uop.iw_p1_bypass_hint', 'replay_arb.io.in[0].bits.uop.iw_p1_speculative_child', 'replay_arb.io.in[0].bits.uop.iw_p2_bypass_hint', 'replay_arb.io.in[0].bits.uop.iw_p2_speculative_child', 'replay_arb.io.in[0].bits.uop.iw_p3_bypass_hint', 'replay_arb.io.in[0].bits.uop.ldq_idx', 'replay_arb.io.in[0].bits.uop.ldst', 'replay_arb.io.in[0].bits.uop.ldst_is_rs1', 'replay_arb.io.in[0].bits.uop.lrs1', 'replay_arb.io.in[0].bits.uop.lrs1_rtype', 'replay_arb.io.in[0].bits.uop.lrs2', 'replay_arb.io.in[0].bits.uop.lrs2_rtype', 'replay_arb.io.in[0].bits.uop.lrs3', 'replay_arb.io.in[0].bits.uop.mem_cmd', 'replay_arb.io.in[0].bits.uop.mem_signed', 'replay_arb.io.in[0].bits.uop.mem_size', 'replay_arb.io.in[0].bits.uop.op1_sel', 'replay_arb.io.in[0].bits.uop.op2_sel', 'replay_arb.io.in[0].bits.uop.pc_lob', 'replay_arb.io.in[0].bits.uop.pdst', 'replay_arb.io.in[0].bits.uop.pimm', 'replay_arb.io.in[0].bits.uop.ppred', 'replay_arb.io.in[0].bits.uop.ppred_busy', 'replay_arb.io.in[0].bits.uop.prs1', 'replay_arb.io.in[0].bits.uop.prs1_busy', 'replay_arb.io.in[0].bits.uop.prs2', 'replay_arb.io.in[0].bits.uop.prs2_busy', 'replay_arb.io.in[0].bits.uop.prs3', 'replay_arb.io.in[0].bits.uop.prs3_busy', 'replay_arb.io.in[0].bits.uop.rob_idx', 'replay_arb.io.in[0].bits.uop.rxq_idx', 'replay_arb.io.in[0].bits.uop.stale_pdst', 'replay_arb.io.in[0].bits.uop.stq_idx', 'replay_arb.io.in[0].bits.uop.taken', 'replay_arb.io.in[0].bits.uop.uses_ldq', 'replay_arb.io.in[0].bits.uop.uses_stq', 'replay_arb.io.in[0].bits.uop.xcpt_ae_if', 'replay_arb.io.in[0].bits.uop.xcpt_ma_if', 'replay_arb.io.in[0].bits.uop.xcpt_pf_if', 'replay_arb.io.in[0].bits.way_en', 'replay_arb.io.in[0].ready', 'replay_arb.io.in[0].valid', 'replay_arb.io.in[1].bits.addr', 'replay_arb.io.in[1].bits.data', 'replay_arb.io.in[1].bits.is_hella', 'replay_arb.io.in[1].bits.old_meta.coh.state', 'replay_arb.io.in[1].bits.old_meta.tag', 'replay_arb.io.in[1].bits.sdq_id', 'replay_arb.io.in[1].bits.tag_match', 'replay_arb.io.in[1].bits.uop.bp_debug_if', 'replay_arb.io.in[1].bits.uop.bp_xcpt_if', 'replay_arb.io.in[1].bits.uop.br_mask', 'replay_arb.io.in[1].bits.uop.br_tag', 'replay_arb.io.in[1].bits.uop.br_type', 'replay_arb.io.in[1].bits.uop.csr_cmd', 'replay_arb.io.in[1].bits.uop.debug_fsrc', 'replay_arb.io.in[1].bits.uop.debug_inst', 'replay_arb.io.in[1].bits.uop.debug_pc', 'replay_arb.io.in[1].bits.uop.debug_tsrc', 'replay_arb.io.in[1].bits.uop.dis_col_sel', 'replay_arb.io.in[1].bits.uop.dst_rtype', 'replay_arb.io.in[1].bits.uop.edge_inst', 'replay_arb.io.in[1].bits.uop.exc_cause', 'replay_arb.io.in[1].bits.uop.exception', 'replay_arb.io.in[1].bits.uop.fcn_dw', 'replay_arb.io.in[1].bits.uop.fcn_op', 'replay_arb.io.in[1].bits.uop.flush_on_commit', 'replay_arb.io.in[1].bits.uop.fp_ctrl.div', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fastpipe', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fma', 'replay_arb.io.in[1].bits.uop.fp_ctrl.fromint', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ldst', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren1', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren2', 'replay_arb.io.in[1].bits.uop.fp_ctrl.ren3', 'replay_arb.io.in[1].bits.uop.fp_ctrl.sqrt', 'replay_arb.io.in[1].bits.uop.fp_ctrl.swap12', 'replay_arb.io.in[1].bits.uop.fp_ctrl.swap23', 'replay_arb.io.in[1].bits.uop.fp_ctrl.toint', 'replay_arb.io.in[1].bits.uop.fp_ctrl.typeTagIn', 'replay_arb.io.in[1].bits.uop.fp_ctrl.typeTagOut', 'replay_arb.io.in[1].bits.uop.fp_ctrl.vec', 'replay_arb.io.in[1].bits.uop.fp_ctrl.wen', 'replay_arb.io.in[1].bits.uop.fp_ctrl.wflags', 'replay_arb.io.in[1].bits.uop.fp_rm', 'replay_arb.io.in[1].bits.uop.fp_typ', 'replay_arb.io.in[1].bits.uop.fp_val', 'replay_arb.io.in[1].bits.uop.frs3_en', 'replay_arb.io.in[1].bits.uop.ftq_idx', 'replay_arb.io.in[1].bits.uop.fu_code[0]', 'replay_arb.io.in[1].bits.uop.fu_code[1]', 'replay_arb.io.in[1].bits.uop.fu_code[2]', 'replay_arb.io.in[1].bits.uop.fu_code[3]', 'replay_arb.io.in[1].bits.uop.fu_code[4]', 'replay_arb.io.in[1].bits.uop.fu_code[5]', 'replay_arb.io.in[1].bits.uop.fu_code[6]', 'replay_arb.io.in[1].bits.uop.fu_code[7]', 'replay_arb.io.in[1].bits.uop.fu_code[8]', 'replay_arb.io.in[1].bits.uop.fu_code[9]', 'replay_arb.io.in[1].bits.uop.imm_packed', 'replay_arb.io.in[1].bits.uop.imm_rename', 'replay_arb.io.in[1].bits.uop.imm_sel', 'replay_arb.io.in[1].bits.uop.inst', 'replay_arb.io.in[1].bits.uop.iq_type[0]', 'replay_arb.io.in[1].bits.uop.iq_type[1]', 'replay_arb.io.in[1].bits.uop.iq_type[2]', 'replay_arb.io.in[1].bits.uop.iq_type[3]', 'replay_arb.io.in[1].bits.uop.is_amo', 'replay_arb.io.in[1].bits.uop.is_eret', 'replay_arb.io.in[1].bits.uop.is_fence', 'replay_arb.io.in[1].bits.uop.is_fencei', 'replay_arb.io.in[1].bits.uop.is_mov', 'replay_arb.io.in[1].bits.uop.is_rocc', 'replay_arb.io.in[1].bits.uop.is_rvc', 'replay_arb.io.in[1].bits.uop.is_sfb', 'replay_arb.io.in[1].bits.uop.is_sfence', 'replay_arb.io.in[1].bits.uop.is_sys_pc2epc', 'replay_arb.io.in[1].bits.uop.is_unique', 'replay_arb.io.in[1].bits.uop.iw_issued', 'replay_arb.io.in[1].bits.uop.iw_issued_partial_agen', 'replay_arb.io.in[1].bits.uop.iw_issued_partial_dgen', 'replay_arb.io.in[1].bits.uop.iw_p1_bypass_hint', 'replay_arb.io.in[1].bits.uop.iw_p1_speculative_child', 'replay_arb.io.in[1].bits.uop.iw_p2_bypass_hint', 'replay_arb.io.in[1].bits.uop.iw_p2_speculative_child', 'replay_arb.io.in[1].bits.uop.iw_p3_bypass_hint', 'replay_arb.io.in[1].bits.uop.ldq_idx', 'replay_arb.io.in[1].bits.uop.ldst', 'replay_arb.io.in[1].bits.uop.ldst_is_rs1', 'replay_arb.io.in[1].bits.uop.lrs1', 'replay_arb.io.in[1].bits.uop.lrs1_rtype', 'replay_arb.io.in[1].bits.uop.lrs2', 'replay_arb.io.in[1].bits.uop.lrs2_rtype', 'replay_arb.io.in[1].bits.uop.lrs3', 'replay_arb.io.in[1].bits.uop.mem_cmd', 'replay_arb.io.in[1].bits.uop.mem_signed', 'replay_arb.io.in[1].bits.uop.mem_size', 'replay_arb.io.in[1].bits.uop.op1_sel', 'replay_arb.io.in[1].bits.uop.op2_sel', 'replay_arb.io.in[1].bits.uop.pc_lob', 'replay_arb.io.in[1].bits.uop.pdst', 'replay_arb.io.in[1].bits.uop.pimm', 'replay_arb.io.in[1].bits.uop.ppred', 'replay_arb.io.in[1].bits.uop.ppred_busy', 'replay_arb.io.in[1].bits.uop.prs1', 'replay_arb.io.in[1].bits.uop.prs1_busy', 'replay_arb.io.in[1].bits.uop.prs2', 'replay_arb.io.in[1].bits.uop.prs2_busy', 'replay_arb.io.in[1].bits.uop.prs3', 'replay_arb.io.in[1].bits.uop.prs3_busy', 'replay_arb.io.in[1].bits.uop.rob_idx', 'replay_arb.io.in[1].bits.uop.rxq_idx', 'replay_arb.io.in[1].bits.uop.stale_pdst', 'replay_arb.io.in[1].bits.uop.stq_idx', 'replay_arb.io.in[1].bits.uop.taken', 'replay_arb.io.in[1].bits.uop.uses_ldq', 'replay_arb.io.in[1].bits.uop.uses_stq', 'replay_arb.io.in[1].bits.uop.xcpt_ae_if', 'replay_arb.io.in[1].bits.uop.xcpt_ma_if', 'replay_arb.io.in[1].bits.uop.xcpt_pf_if', 'replay_arb.io.in[1].bits.way_en', 'replay_arb.io.in[1].ready', 'replay_arb.io.in[1].valid', 'replay_arb.io.out.bits.addr', 'replay_arb.io.out.bits.data', 'replay_arb.io.out.bits.is_hella', 'replay_arb.io.out.bits.old_meta.coh.state', 'replay_arb.io.out.bits.old_meta.tag', 'replay_arb.io.out.bits.sdq_id', 'replay_arb.io.out.bits.tag_match', 'replay_arb.io.out.bits.uop.bp_debug_if', 'replay_arb.io.out.bits.uop.bp_xcpt_if', 'replay_arb.io.out.bits.uop.br_mask', 'replay_arb.io.out.bits.uop.br_tag', 'replay_arb.io.out.bits.uop.br_type', 'replay_arb.io.out.bits.uop.csr_cmd', 'replay_arb.io.out.bits.uop.debug_fsrc', 'replay_arb.io.out.bits.uop.debug_inst', 'replay_arb.io.out.bits.uop.debug_pc', 'replay_arb.io.out.bits.uop.debug_tsrc', 'replay_arb.io.out.bits.uop.dis_col_sel', 'replay_arb.io.out.bits.uop.dst_rtype', 'replay_arb.io.out.bits.uop.edge_inst', 'replay_arb.io.out.bits.uop.exc_cause', 'replay_arb.io.out.bits.uop.exception', 'replay_arb.io.out.bits.uop.fcn_dw', 'replay_arb.io.out.bits.uop.fcn_op', 'replay_arb.io.out.bits.uop.flush_on_commit', 'replay_arb.io.out.bits.uop.fp_ctrl.div', 'replay_arb.io.out.bits.uop.fp_ctrl.fastpipe', 'replay_arb.io.out.bits.uop.fp_ctrl.fma', 'replay_arb.io.out.bits.uop.fp_ctrl.fromint', 'replay_arb.io.out.bits.uop.fp_ctrl.ldst', 'replay_arb.io.out.bits.uop.fp_ctrl.ren1', 'replay_arb.io.out.bits.uop.fp_ctrl.ren2', 'replay_arb.io.out.bits.uop.fp_ctrl.ren3', 'replay_arb.io.out.bits.uop.fp_ctrl.sqrt', 'replay_arb.io.out.bits.uop.fp_ctrl.swap12', 'replay_arb.io.out.bits.uop.fp_ctrl.swap23', 'replay_arb.io.out.bits.uop.fp_ctrl.toint', 'replay_arb.io.out.bits.uop.fp_ctrl.typeTagIn', 'replay_arb.io.out.bits.uop.fp_ctrl.typeTagOut', 'replay_arb.io.out.bits.uop.fp_ctrl.vec', 'replay_arb.io.out.bits.uop.fp_ctrl.wen', 'replay_arb.io.out.bits.uop.fp_ctrl.wflags', 'replay_arb.io.out.bits.uop.fp_rm', 'replay_arb.io.out.bits.uop.fp_typ', 'replay_arb.io.out.bits.uop.fp_val', 'replay_arb.io.out.bits.uop.frs3_en', 'replay_arb.io.out.bits.uop.ftq_idx', 'replay_arb.io.out.bits.uop.fu_code[0]', 'replay_arb.io.out.bits.uop.fu_code[1]', 'replay_arb.io.out.bits.uop.fu_code[2]', 'replay_arb.io.out.bits.uop.fu_code[3]', 'replay_arb.io.out.bits.uop.fu_code[4]', 'replay_arb.io.out.bits.uop.fu_code[5]', 'replay_arb.io.out.bits.uop.fu_code[6]', 'replay_arb.io.out.bits.uop.fu_code[7]', 'replay_arb.io.out.bits.uop.fu_code[8]', 'replay_arb.io.out.bits.uop.fu_code[9]', 'replay_arb.io.out.bits.uop.imm_packed', 'replay_arb.io.out.bits.uop.imm_rename', 'replay_arb.io.out.bits.uop.imm_sel', 'replay_arb.io.out.bits.uop.inst', 'replay_arb.io.out.bits.uop.iq_type[0]', 'replay_arb.io.out.bits.uop.iq_type[1]', 'replay_arb.io.out.bits.uop.iq_type[2]', 'replay_arb.io.out.bits.uop.iq_type[3]', 'replay_arb.io.out.bits.uop.is_amo', 'replay_arb.io.out.bits.uop.is_eret', 'replay_arb.io.out.bits.uop.is_fence', 'replay_arb.io.out.bits.uop.is_fencei', 'replay_arb.io.out.bits.uop.is_mov', 'replay_arb.io.out.bits.uop.is_rocc', 'replay_arb.io.out.bits.uop.is_rvc', 'replay_arb.io.out.bits.uop.is_sfb', 'replay_arb.io.out.bits.uop.is_sfence', 'replay_arb.io.out.bits.uop.is_sys_pc2epc', 'replay_arb.io.out.bits.uop.is_unique', 'replay_arb.io.out.bits.uop.iw_issued', 'replay_arb.io.out.bits.uop.iw_issued_partial_agen', 'replay_arb.io.out.bits.uop.iw_issued_partial_dgen', 'replay_arb.io.out.bits.uop.iw_p1_bypass_hint', 'replay_arb.io.out.bits.uop.iw_p1_speculative_child', 'replay_arb.io.out.bits.uop.iw_p2_bypass_hint', 'replay_arb.io.out.bits.uop.iw_p2_speculative_child', 'replay_arb.io.out.bits.uop.iw_p3_bypass_hint', 'replay_arb.io.out.bits.uop.ldq_idx', 'replay_arb.io.out.bits.uop.ldst', 'replay_arb.io.out.bits.uop.ldst_is_rs1', 'replay_arb.io.out.bits.uop.lrs1', 'replay_arb.io.out.bits.uop.lrs1_rtype', 'replay_arb.io.out.bits.uop.lrs2', 'replay_arb.io.out.bits.uop.lrs2_rtype', 'replay_arb.io.out.bits.uop.lrs3', 'replay_arb.io.out.bits.uop.mem_cmd', 'replay_arb.io.out.bits.uop.mem_signed', 'replay_arb.io.out.bits.uop.mem_size', 'replay_arb.io.out.bits.uop.op1_sel', 'replay_arb.io.out.bits.uop.op2_sel', 'replay_arb.io.out.bits.uop.pc_lob', 'replay_arb.io.out.bits.uop.pdst', 'replay_arb.io.out.bits.uop.pimm', 'replay_arb.io.out.bits.uop.ppred', 'replay_arb.io.out.bits.uop.ppred_busy', 'replay_arb.io.out.bits.uop.prs1', 'replay_arb.io.out.bits.uop.prs1_busy', 'replay_arb.io.out.bits.uop.prs2', 'replay_arb.io.out.bits.uop.prs2_busy', 'replay_arb.io.out.bits.uop.prs3', 'replay_arb.io.out.bits.uop.prs3_busy', 'replay_arb.io.out.bits.uop.rob_idx', 'replay_arb.io.out.bits.uop.rxq_idx', 'replay_arb.io.out.bits.uop.stale_pdst', 'replay_arb.io.out.bits.uop.stq_idx', 'replay_arb.io.out.bits.uop.taken', 'replay_arb.io.out.bits.uop.uses_ldq', 'replay_arb.io.out.bits.uop.uses_stq', 'replay_arb.io.out.bits.uop.xcpt_ae_if', 'replay_arb.io.out.bits.uop.xcpt_ma_if', 'replay_arb.io.out.bits.uop.xcpt_pf_if', 'replay_arb.io.out.bits.way_en', 'replay_arb.io.out.ready', 'replay_arb.io.out.valid', 'replay_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.replay_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A13": {
      "local_id": "A13",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A14": {
      "local_id": "A14",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A15": {
      "local_id": "A15",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A16": {
      "local_id": "A16",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A17": {
      "local_id": "A17",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A18": {
      "local_id": "A18",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A19": {
      "local_id": "A19",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A20": {
      "local_id": "A20",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.replay_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.replay_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    },
    "BoomMSHRFile.replay_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.replay_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.replay_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.replay_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.addr",
          "op": "signal"
        },
        "target": "io.out.bits.addr",
        "type": "signal_equality"
      },
      "id": "A3",
      "rendered_formula": "io.out.bits.addr = io.in[0].bits.addr on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.mem_cmd",
          "op": "signal"
        },
        "target": "io.out.bits.uop.mem_cmd",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.uop.mem_cmd = io.in[0].bits.uop.mem_cmd on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.ldq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.ldq_idx",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.uop.ldq_idx = io.in[0].bits.uop.ldq_idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.stq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.stq_idx",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.uop.stq_idx = io.in[0].bits.uop.stq_idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.sdq_id",
          "op": "signal"
        },
        "target": "io.out.bits.sdq_id",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.sdq_id = io.in[0].bits.sdq_id on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.old_meta.tag",
          "op": "signal"
        },
        "target": "io.out.bits.old_meta.tag",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.old_meta.tag = io.in[0].bits.old_meta.tag on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.old_meta.coh.state",
          "op": "signal"
        },
        "target": "io.out.bits.old_meta.coh.state",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.out.bits.old_meta.coh.state = io.in[0].bits.old_meta.coh.state on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A10",
      "rendered_formula": "io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.tag_match",
          "op": "signal"
        },
        "target": "io.out.bits.tag_match",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.out.bits.tag_match = io.in[0].bits.tag_match on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.addr",
          "op": "signal"
        },
        "target": "io.out.bits.addr",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.out.bits.addr = io.in[1].bits.addr on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.mem_cmd",
          "op": "signal"
        },
        "target": "io.out.bits.uop.mem_cmd",
        "type": "signal_equality"
      },
      "id": "A13",
      "rendered_formula": "io.out.bits.uop.mem_cmd = io.in[1].bits.uop.mem_cmd on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.ldq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.ldq_idx",
        "type": "signal_equality"
      },
      "id": "A14",
      "rendered_formula": "io.out.bits.uop.ldq_idx = io.in[1].bits.uop.ldq_idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.stq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.stq_idx",
        "type": "signal_equality"
      },
      "id": "A15",
      "rendered_formula": "io.out.bits.uop.stq_idx = io.in[1].bits.uop.stq_idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.sdq_id",
          "op": "signal"
        },
        "target": "io.out.bits.sdq_id",
        "type": "signal_equality"
      },
      "id": "A16",
      "rendered_formula": "io.out.bits.sdq_id = io.in[1].bits.sdq_id on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.old_meta.tag",
          "op": "signal"
        },
        "target": "io.out.bits.old_meta.tag",
        "type": "signal_equality"
      },
      "id": "A17",
      "rendered_formula": "io.out.bits.old_meta.tag = io.in[1].bits.old_meta.tag on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.old_meta.coh.state",
          "op": "signal"
        },
        "target": "io.out.bits.old_meta.coh.state",
        "type": "signal_equality"
      },
      "id": "A18",
      "rendered_formula": "io.out.bits.old_meta.coh.state = io.in[1].bits.old_meta.coh.state on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A19",
      "rendered_formula": "io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.tag_match",
          "op": "signal"
        },
        "target": "io.out.bits.tag_match",
        "type": "signal_equality"
      },
      "id": "A20",
      "rendered_formula": "io.out.bits.tag_match = io.in[1].bits.tag_match on Input1Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has fixed priority and the accepted replay request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only while input 0 is not valid, and its replay request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 20,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 20
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        9,
        10
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.replay_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.replay_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        13,
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.replay_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        5,
        8
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.replay_arb-8fdf73acfd546ea3",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A15",
    "A16",
    "A17",
    "A18",
    "A19",
    "A2",
    "A20",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.replay_arb"
}
```

### Child `BoomMSHRFile.resp_arb`
- summary ref: `umcm://BoomMSHRFile.resp_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.resp_arb-9f8d9cdf03590f99`
- frozen SHA-256: `16bfe4b3f584edf9b4bb4d4779727a278d650cd105339fb6a7e9056ce706fffe`
- implementation SHA-256: `815ded35fab38fc992e759008bdb3b9947abc253ff612ea996ba0a772852fdab`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.resp_arb', 'target_work_unit_id': 'BoomMSHRFile.resp_arb', 'module': 'Arbiter3_BoomDCacheResp', 'implementation_sha256': '815ded35fab38fc992e759008bdb3b9947abc253ff612ea996ba0a772852fdab', 'structural_implementation_sha256': '5a4aa6692c75c31a05815626e30b7d7bbd5a2d04e6c06ffa91adcb2ef737bd77', 'source_module': 'Arbiter3_BoomDCacheResp', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.resp_arb::io.in[0].fire', 'BoomMSHRFile.resp_arb::io.in[1].fire', 'BoomMSHRFile.resp_arb::io.in[2].fire', 'BoomMSHRFile.resp_arb::io.out.fire']
- frontier signals: ['resp_arb.clock', 'resp_arb.io', 'resp_arb.io.chosen', 'resp_arb.io.in[0].bits.data', 'resp_arb.io.in[0].bits.is_hella', 'resp_arb.io.in[0].bits.uop.bp_debug_if', 'resp_arb.io.in[0].bits.uop.bp_xcpt_if', 'resp_arb.io.in[0].bits.uop.br_mask', 'resp_arb.io.in[0].bits.uop.br_tag', 'resp_arb.io.in[0].bits.uop.br_type', 'resp_arb.io.in[0].bits.uop.csr_cmd', 'resp_arb.io.in[0].bits.uop.debug_fsrc', 'resp_arb.io.in[0].bits.uop.debug_inst', 'resp_arb.io.in[0].bits.uop.debug_pc', 'resp_arb.io.in[0].bits.uop.debug_tsrc', 'resp_arb.io.in[0].bits.uop.dis_col_sel', 'resp_arb.io.in[0].bits.uop.dst_rtype', 'resp_arb.io.in[0].bits.uop.edge_inst', 'resp_arb.io.in[0].bits.uop.exc_cause', 'resp_arb.io.in[0].bits.uop.exception', 'resp_arb.io.in[0].bits.uop.fcn_dw', 'resp_arb.io.in[0].bits.uop.fcn_op', 'resp_arb.io.in[0].bits.uop.flush_on_commit', 'resp_arb.io.in[0].bits.uop.fp_ctrl.div', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[0].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[0].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[0].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[0].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[0].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[0].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[0].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[0].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[0].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[0].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[0].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[0].bits.uop.fp_rm', 'resp_arb.io.in[0].bits.uop.fp_typ', 'resp_arb.io.in[0].bits.uop.fp_val', 'resp_arb.io.in[0].bits.uop.frs3_en', 'resp_arb.io.in[0].bits.uop.ftq_idx', 'resp_arb.io.in[0].bits.uop.fu_code[0]', 'resp_arb.io.in[0].bits.uop.fu_code[1]', 'resp_arb.io.in[0].bits.uop.fu_code[2]', 'resp_arb.io.in[0].bits.uop.fu_code[3]', 'resp_arb.io.in[0].bits.uop.fu_code[4]', 'resp_arb.io.in[0].bits.uop.fu_code[5]', 'resp_arb.io.in[0].bits.uop.fu_code[6]', 'resp_arb.io.in[0].bits.uop.fu_code[7]', 'resp_arb.io.in[0].bits.uop.fu_code[8]', 'resp_arb.io.in[0].bits.uop.fu_code[9]', 'resp_arb.io.in[0].bits.uop.imm_packed', 'resp_arb.io.in[0].bits.uop.imm_rename', 'resp_arb.io.in[0].bits.uop.imm_sel', 'resp_arb.io.in[0].bits.uop.inst', 'resp_arb.io.in[0].bits.uop.iq_type[0]', 'resp_arb.io.in[0].bits.uop.iq_type[1]', 'resp_arb.io.in[0].bits.uop.iq_type[2]', 'resp_arb.io.in[0].bits.uop.iq_type[3]', 'resp_arb.io.in[0].bits.uop.is_amo', 'resp_arb.io.in[0].bits.uop.is_eret', 'resp_arb.io.in[0].bits.uop.is_fence', 'resp_arb.io.in[0].bits.uop.is_fencei', 'resp_arb.io.in[0].bits.uop.is_mov', 'resp_arb.io.in[0].bits.uop.is_rocc', 'resp_arb.io.in[0].bits.uop.is_rvc', 'resp_arb.io.in[0].bits.uop.is_sfb', 'resp_arb.io.in[0].bits.uop.is_sfence', 'resp_arb.io.in[0].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[0].bits.uop.is_unique', 'resp_arb.io.in[0].bits.uop.iw_issued', 'resp_arb.io.in[0].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[0].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[0].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[0].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[0].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[0].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[0].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[0].bits.uop.ldq_idx', 'resp_arb.io.in[0].bits.uop.ldst', 'resp_arb.io.in[0].bits.uop.ldst_is_rs1', 'resp_arb.io.in[0].bits.uop.lrs1', 'resp_arb.io.in[0].bits.uop.lrs1_rtype', 'resp_arb.io.in[0].bits.uop.lrs2', 'resp_arb.io.in[0].bits.uop.lrs2_rtype', 'resp_arb.io.in[0].bits.uop.lrs3', 'resp_arb.io.in[0].bits.uop.mem_cmd', 'resp_arb.io.in[0].bits.uop.mem_signed', 'resp_arb.io.in[0].bits.uop.mem_size', 'resp_arb.io.in[0].bits.uop.op1_sel', 'resp_arb.io.in[0].bits.uop.op2_sel', 'resp_arb.io.in[0].bits.uop.pc_lob', 'resp_arb.io.in[0].bits.uop.pdst', 'resp_arb.io.in[0].bits.uop.pimm', 'resp_arb.io.in[0].bits.uop.ppred', 'resp_arb.io.in[0].bits.uop.ppred_busy', 'resp_arb.io.in[0].bits.uop.prs1', 'resp_arb.io.in[0].bits.uop.prs1_busy', 'resp_arb.io.in[0].bits.uop.prs2', 'resp_arb.io.in[0].bits.uop.prs2_busy', 'resp_arb.io.in[0].bits.uop.prs3', 'resp_arb.io.in[0].bits.uop.prs3_busy', 'resp_arb.io.in[0].bits.uop.rob_idx', 'resp_arb.io.in[0].bits.uop.rxq_idx', 'resp_arb.io.in[0].bits.uop.stale_pdst', 'resp_arb.io.in[0].bits.uop.stq_idx', 'resp_arb.io.in[0].bits.uop.taken', 'resp_arb.io.in[0].bits.uop.uses_ldq', 'resp_arb.io.in[0].bits.uop.uses_stq', 'resp_arb.io.in[0].bits.uop.xcpt_ae_if', 'resp_arb.io.in[0].bits.uop.xcpt_ma_if', 'resp_arb.io.in[0].bits.uop.xcpt_pf_if', 'resp_arb.io.in[0].ready', 'resp_arb.io.in[0].valid', 'resp_arb.io.in[1].bits.data', 'resp_arb.io.in[1].bits.is_hella', 'resp_arb.io.in[1].bits.uop.bp_debug_if', 'resp_arb.io.in[1].bits.uop.bp_xcpt_if', 'resp_arb.io.in[1].bits.uop.br_mask', 'resp_arb.io.in[1].bits.uop.br_tag', 'resp_arb.io.in[1].bits.uop.br_type', 'resp_arb.io.in[1].bits.uop.csr_cmd', 'resp_arb.io.in[1].bits.uop.debug_fsrc', 'resp_arb.io.in[1].bits.uop.debug_inst', 'resp_arb.io.in[1].bits.uop.debug_pc', 'resp_arb.io.in[1].bits.uop.debug_tsrc', 'resp_arb.io.in[1].bits.uop.dis_col_sel', 'resp_arb.io.in[1].bits.uop.dst_rtype', 'resp_arb.io.in[1].bits.uop.edge_inst', 'resp_arb.io.in[1].bits.uop.exc_cause', 'resp_arb.io.in[1].bits.uop.exception', 'resp_arb.io.in[1].bits.uop.fcn_dw', 'resp_arb.io.in[1].bits.uop.fcn_op', 'resp_arb.io.in[1].bits.uop.flush_on_commit', 'resp_arb.io.in[1].bits.uop.fp_ctrl.div', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[1].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[1].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[1].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[1].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[1].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[1].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[1].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[1].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[1].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[1].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[1].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[1].bits.uop.fp_rm', 'resp_arb.io.in[1].bits.uop.fp_typ', 'resp_arb.io.in[1].bits.uop.fp_val', 'resp_arb.io.in[1].bits.uop.frs3_en', 'resp_arb.io.in[1].bits.uop.ftq_idx', 'resp_arb.io.in[1].bits.uop.fu_code[0]', 'resp_arb.io.in[1].bits.uop.fu_code[1]', 'resp_arb.io.in[1].bits.uop.fu_code[2]', 'resp_arb.io.in[1].bits.uop.fu_code[3]', 'resp_arb.io.in[1].bits.uop.fu_code[4]', 'resp_arb.io.in[1].bits.uop.fu_code[5]', 'resp_arb.io.in[1].bits.uop.fu_code[6]', 'resp_arb.io.in[1].bits.uop.fu_code[7]', 'resp_arb.io.in[1].bits.uop.fu_code[8]', 'resp_arb.io.in[1].bits.uop.fu_code[9]', 'resp_arb.io.in[1].bits.uop.imm_packed', 'resp_arb.io.in[1].bits.uop.imm_rename', 'resp_arb.io.in[1].bits.uop.imm_sel', 'resp_arb.io.in[1].bits.uop.inst', 'resp_arb.io.in[1].bits.uop.iq_type[0]', 'resp_arb.io.in[1].bits.uop.iq_type[1]', 'resp_arb.io.in[1].bits.uop.iq_type[2]', 'resp_arb.io.in[1].bits.uop.iq_type[3]', 'resp_arb.io.in[1].bits.uop.is_amo', 'resp_arb.io.in[1].bits.uop.is_eret', 'resp_arb.io.in[1].bits.uop.is_fence', 'resp_arb.io.in[1].bits.uop.is_fencei', 'resp_arb.io.in[1].bits.uop.is_mov', 'resp_arb.io.in[1].bits.uop.is_rocc', 'resp_arb.io.in[1].bits.uop.is_rvc', 'resp_arb.io.in[1].bits.uop.is_sfb', 'resp_arb.io.in[1].bits.uop.is_sfence', 'resp_arb.io.in[1].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[1].bits.uop.is_unique', 'resp_arb.io.in[1].bits.uop.iw_issued', 'resp_arb.io.in[1].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[1].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[1].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[1].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[1].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[1].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[1].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[1].bits.uop.ldq_idx', 'resp_arb.io.in[1].bits.uop.ldst', 'resp_arb.io.in[1].bits.uop.ldst_is_rs1', 'resp_arb.io.in[1].bits.uop.lrs1', 'resp_arb.io.in[1].bits.uop.lrs1_rtype', 'resp_arb.io.in[1].bits.uop.lrs2', 'resp_arb.io.in[1].bits.uop.lrs2_rtype', 'resp_arb.io.in[1].bits.uop.lrs3', 'resp_arb.io.in[1].bits.uop.mem_cmd', 'resp_arb.io.in[1].bits.uop.mem_signed', 'resp_arb.io.in[1].bits.uop.mem_size', 'resp_arb.io.in[1].bits.uop.op1_sel', 'resp_arb.io.in[1].bits.uop.op2_sel', 'resp_arb.io.in[1].bits.uop.pc_lob', 'resp_arb.io.in[1].bits.uop.pdst', 'resp_arb.io.in[1].bits.uop.pimm', 'resp_arb.io.in[1].bits.uop.ppred', 'resp_arb.io.in[1].bits.uop.ppred_busy', 'resp_arb.io.in[1].bits.uop.prs1', 'resp_arb.io.in[1].bits.uop.prs1_busy', 'resp_arb.io.in[1].bits.uop.prs2', 'resp_arb.io.in[1].bits.uop.prs2_busy', 'resp_arb.io.in[1].bits.uop.prs3', 'resp_arb.io.in[1].bits.uop.prs3_busy', 'resp_arb.io.in[1].bits.uop.rob_idx', 'resp_arb.io.in[1].bits.uop.rxq_idx', 'resp_arb.io.in[1].bits.uop.stale_pdst', 'resp_arb.io.in[1].bits.uop.stq_idx', 'resp_arb.io.in[1].bits.uop.taken', 'resp_arb.io.in[1].bits.uop.uses_ldq', 'resp_arb.io.in[1].bits.uop.uses_stq', 'resp_arb.io.in[1].bits.uop.xcpt_ae_if', 'resp_arb.io.in[1].bits.uop.xcpt_ma_if', 'resp_arb.io.in[1].bits.uop.xcpt_pf_if', 'resp_arb.io.in[1].ready', 'resp_arb.io.in[1].valid', 'resp_arb.io.in[2].bits.data', 'resp_arb.io.in[2].bits.is_hella', 'resp_arb.io.in[2].bits.uop.bp_debug_if', 'resp_arb.io.in[2].bits.uop.bp_xcpt_if', 'resp_arb.io.in[2].bits.uop.br_mask', 'resp_arb.io.in[2].bits.uop.br_tag', 'resp_arb.io.in[2].bits.uop.br_type', 'resp_arb.io.in[2].bits.uop.csr_cmd', 'resp_arb.io.in[2].bits.uop.debug_fsrc', 'resp_arb.io.in[2].bits.uop.debug_inst', 'resp_arb.io.in[2].bits.uop.debug_pc', 'resp_arb.io.in[2].bits.uop.debug_tsrc', 'resp_arb.io.in[2].bits.uop.dis_col_sel', 'resp_arb.io.in[2].bits.uop.dst_rtype', 'resp_arb.io.in[2].bits.uop.edge_inst', 'resp_arb.io.in[2].bits.uop.exc_cause', 'resp_arb.io.in[2].bits.uop.exception', 'resp_arb.io.in[2].bits.uop.fcn_dw', 'resp_arb.io.in[2].bits.uop.fcn_op', 'resp_arb.io.in[2].bits.uop.flush_on_commit', 'resp_arb.io.in[2].bits.uop.fp_ctrl.div', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fma', 'resp_arb.io.in[2].bits.uop.fp_ctrl.fromint', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ldst', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren1', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren2', 'resp_arb.io.in[2].bits.uop.fp_ctrl.ren3', 'resp_arb.io.in[2].bits.uop.fp_ctrl.sqrt', 'resp_arb.io.in[2].bits.uop.fp_ctrl.swap12', 'resp_arb.io.in[2].bits.uop.fp_ctrl.swap23', 'resp_arb.io.in[2].bits.uop.fp_ctrl.toint', 'resp_arb.io.in[2].bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.in[2].bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.in[2].bits.uop.fp_ctrl.vec', 'resp_arb.io.in[2].bits.uop.fp_ctrl.wen', 'resp_arb.io.in[2].bits.uop.fp_ctrl.wflags', 'resp_arb.io.in[2].bits.uop.fp_rm', 'resp_arb.io.in[2].bits.uop.fp_typ', 'resp_arb.io.in[2].bits.uop.fp_val', 'resp_arb.io.in[2].bits.uop.frs3_en', 'resp_arb.io.in[2].bits.uop.ftq_idx', 'resp_arb.io.in[2].bits.uop.fu_code[0]', 'resp_arb.io.in[2].bits.uop.fu_code[1]', 'resp_arb.io.in[2].bits.uop.fu_code[2]', 'resp_arb.io.in[2].bits.uop.fu_code[3]', 'resp_arb.io.in[2].bits.uop.fu_code[4]', 'resp_arb.io.in[2].bits.uop.fu_code[5]', 'resp_arb.io.in[2].bits.uop.fu_code[6]', 'resp_arb.io.in[2].bits.uop.fu_code[7]', 'resp_arb.io.in[2].bits.uop.fu_code[8]', 'resp_arb.io.in[2].bits.uop.fu_code[9]', 'resp_arb.io.in[2].bits.uop.imm_packed', 'resp_arb.io.in[2].bits.uop.imm_rename', 'resp_arb.io.in[2].bits.uop.imm_sel', 'resp_arb.io.in[2].bits.uop.inst', 'resp_arb.io.in[2].bits.uop.iq_type[0]', 'resp_arb.io.in[2].bits.uop.iq_type[1]', 'resp_arb.io.in[2].bits.uop.iq_type[2]', 'resp_arb.io.in[2].bits.uop.iq_type[3]', 'resp_arb.io.in[2].bits.uop.is_amo', 'resp_arb.io.in[2].bits.uop.is_eret', 'resp_arb.io.in[2].bits.uop.is_fence', 'resp_arb.io.in[2].bits.uop.is_fencei', 'resp_arb.io.in[2].bits.uop.is_mov', 'resp_arb.io.in[2].bits.uop.is_rocc', 'resp_arb.io.in[2].bits.uop.is_rvc', 'resp_arb.io.in[2].bits.uop.is_sfb', 'resp_arb.io.in[2].bits.uop.is_sfence', 'resp_arb.io.in[2].bits.uop.is_sys_pc2epc', 'resp_arb.io.in[2].bits.uop.is_unique', 'resp_arb.io.in[2].bits.uop.iw_issued', 'resp_arb.io.in[2].bits.uop.iw_issued_partial_agen', 'resp_arb.io.in[2].bits.uop.iw_issued_partial_dgen', 'resp_arb.io.in[2].bits.uop.iw_p1_bypass_hint', 'resp_arb.io.in[2].bits.uop.iw_p1_speculative_child', 'resp_arb.io.in[2].bits.uop.iw_p2_bypass_hint', 'resp_arb.io.in[2].bits.uop.iw_p2_speculative_child', 'resp_arb.io.in[2].bits.uop.iw_p3_bypass_hint', 'resp_arb.io.in[2].bits.uop.ldq_idx', 'resp_arb.io.in[2].bits.uop.ldst', 'resp_arb.io.in[2].bits.uop.ldst_is_rs1', 'resp_arb.io.in[2].bits.uop.lrs1', 'resp_arb.io.in[2].bits.uop.lrs1_rtype', 'resp_arb.io.in[2].bits.uop.lrs2', 'resp_arb.io.in[2].bits.uop.lrs2_rtype', 'resp_arb.io.in[2].bits.uop.lrs3', 'resp_arb.io.in[2].bits.uop.mem_cmd', 'resp_arb.io.in[2].bits.uop.mem_signed', 'resp_arb.io.in[2].bits.uop.mem_size', 'resp_arb.io.in[2].bits.uop.op1_sel', 'resp_arb.io.in[2].bits.uop.op2_sel', 'resp_arb.io.in[2].bits.uop.pc_lob', 'resp_arb.io.in[2].bits.uop.pdst', 'resp_arb.io.in[2].bits.uop.pimm', 'resp_arb.io.in[2].bits.uop.ppred', 'resp_arb.io.in[2].bits.uop.ppred_busy', 'resp_arb.io.in[2].bits.uop.prs1', 'resp_arb.io.in[2].bits.uop.prs1_busy', 'resp_arb.io.in[2].bits.uop.prs2', 'resp_arb.io.in[2].bits.uop.prs2_busy', 'resp_arb.io.in[2].bits.uop.prs3', 'resp_arb.io.in[2].bits.uop.prs3_busy', 'resp_arb.io.in[2].bits.uop.rob_idx', 'resp_arb.io.in[2].bits.uop.rxq_idx', 'resp_arb.io.in[2].bits.uop.stale_pdst', 'resp_arb.io.in[2].bits.uop.stq_idx', 'resp_arb.io.in[2].bits.uop.taken', 'resp_arb.io.in[2].bits.uop.uses_ldq', 'resp_arb.io.in[2].bits.uop.uses_stq', 'resp_arb.io.in[2].bits.uop.xcpt_ae_if', 'resp_arb.io.in[2].bits.uop.xcpt_ma_if', 'resp_arb.io.in[2].bits.uop.xcpt_pf_if', 'resp_arb.io.in[2].ready', 'resp_arb.io.in[2].valid', 'resp_arb.io.out.bits.data', 'resp_arb.io.out.bits.is_hella', 'resp_arb.io.out.bits.uop.bp_debug_if', 'resp_arb.io.out.bits.uop.bp_xcpt_if', 'resp_arb.io.out.bits.uop.br_mask', 'resp_arb.io.out.bits.uop.br_tag', 'resp_arb.io.out.bits.uop.br_type', 'resp_arb.io.out.bits.uop.csr_cmd', 'resp_arb.io.out.bits.uop.debug_fsrc', 'resp_arb.io.out.bits.uop.debug_inst', 'resp_arb.io.out.bits.uop.debug_pc', 'resp_arb.io.out.bits.uop.debug_tsrc', 'resp_arb.io.out.bits.uop.dis_col_sel', 'resp_arb.io.out.bits.uop.dst_rtype', 'resp_arb.io.out.bits.uop.edge_inst', 'resp_arb.io.out.bits.uop.exc_cause', 'resp_arb.io.out.bits.uop.exception', 'resp_arb.io.out.bits.uop.fcn_dw', 'resp_arb.io.out.bits.uop.fcn_op', 'resp_arb.io.out.bits.uop.flush_on_commit', 'resp_arb.io.out.bits.uop.fp_ctrl.div', 'resp_arb.io.out.bits.uop.fp_ctrl.fastpipe', 'resp_arb.io.out.bits.uop.fp_ctrl.fma', 'resp_arb.io.out.bits.uop.fp_ctrl.fromint', 'resp_arb.io.out.bits.uop.fp_ctrl.ldst', 'resp_arb.io.out.bits.uop.fp_ctrl.ren1', 'resp_arb.io.out.bits.uop.fp_ctrl.ren2', 'resp_arb.io.out.bits.uop.fp_ctrl.ren3', 'resp_arb.io.out.bits.uop.fp_ctrl.sqrt', 'resp_arb.io.out.bits.uop.fp_ctrl.swap12', 'resp_arb.io.out.bits.uop.fp_ctrl.swap23', 'resp_arb.io.out.bits.uop.fp_ctrl.toint', 'resp_arb.io.out.bits.uop.fp_ctrl.typeTagIn', 'resp_arb.io.out.bits.uop.fp_ctrl.typeTagOut', 'resp_arb.io.out.bits.uop.fp_ctrl.vec', 'resp_arb.io.out.bits.uop.fp_ctrl.wen', 'resp_arb.io.out.bits.uop.fp_ctrl.wflags', 'resp_arb.io.out.bits.uop.fp_rm', 'resp_arb.io.out.bits.uop.fp_typ', 'resp_arb.io.out.bits.uop.fp_val', 'resp_arb.io.out.bits.uop.frs3_en', 'resp_arb.io.out.bits.uop.ftq_idx', 'resp_arb.io.out.bits.uop.fu_code[0]', 'resp_arb.io.out.bits.uop.fu_code[1]', 'resp_arb.io.out.bits.uop.fu_code[2]', 'resp_arb.io.out.bits.uop.fu_code[3]', 'resp_arb.io.out.bits.uop.fu_code[4]', 'resp_arb.io.out.bits.uop.fu_code[5]', 'resp_arb.io.out.bits.uop.fu_code[6]', 'resp_arb.io.out.bits.uop.fu_code[7]', 'resp_arb.io.out.bits.uop.fu_code[8]', 'resp_arb.io.out.bits.uop.fu_code[9]', 'resp_arb.io.out.bits.uop.imm_packed', 'resp_arb.io.out.bits.uop.imm_rename', 'resp_arb.io.out.bits.uop.imm_sel', 'resp_arb.io.out.bits.uop.inst', 'resp_arb.io.out.bits.uop.iq_type[0]', 'resp_arb.io.out.bits.uop.iq_type[1]', 'resp_arb.io.out.bits.uop.iq_type[2]', 'resp_arb.io.out.bits.uop.iq_type[3]', 'resp_arb.io.out.bits.uop.is_amo', 'resp_arb.io.out.bits.uop.is_eret', 'resp_arb.io.out.bits.uop.is_fence', 'resp_arb.io.out.bits.uop.is_fencei', 'resp_arb.io.out.bits.uop.is_mov', 'resp_arb.io.out.bits.uop.is_rocc', 'resp_arb.io.out.bits.uop.is_rvc', 'resp_arb.io.out.bits.uop.is_sfb', 'resp_arb.io.out.bits.uop.is_sfence', 'resp_arb.io.out.bits.uop.is_sys_pc2epc', 'resp_arb.io.out.bits.uop.is_unique', 'resp_arb.io.out.bits.uop.iw_issued', 'resp_arb.io.out.bits.uop.iw_issued_partial_agen', 'resp_arb.io.out.bits.uop.iw_issued_partial_dgen', 'resp_arb.io.out.bits.uop.iw_p1_bypass_hint', 'resp_arb.io.out.bits.uop.iw_p1_speculative_child', 'resp_arb.io.out.bits.uop.iw_p2_bypass_hint', 'resp_arb.io.out.bits.uop.iw_p2_speculative_child', 'resp_arb.io.out.bits.uop.iw_p3_bypass_hint', 'resp_arb.io.out.bits.uop.ldq_idx', 'resp_arb.io.out.bits.uop.ldst', 'resp_arb.io.out.bits.uop.ldst_is_rs1', 'resp_arb.io.out.bits.uop.lrs1', 'resp_arb.io.out.bits.uop.lrs1_rtype', 'resp_arb.io.out.bits.uop.lrs2', 'resp_arb.io.out.bits.uop.lrs2_rtype', 'resp_arb.io.out.bits.uop.lrs3', 'resp_arb.io.out.bits.uop.mem_cmd', 'resp_arb.io.out.bits.uop.mem_signed', 'resp_arb.io.out.bits.uop.mem_size', 'resp_arb.io.out.bits.uop.op1_sel', 'resp_arb.io.out.bits.uop.op2_sel', 'resp_arb.io.out.bits.uop.pc_lob', 'resp_arb.io.out.bits.uop.pdst', 'resp_arb.io.out.bits.uop.pimm', 'resp_arb.io.out.bits.uop.ppred', 'resp_arb.io.out.bits.uop.ppred_busy', 'resp_arb.io.out.bits.uop.prs1', 'resp_arb.io.out.bits.uop.prs1_busy', 'resp_arb.io.out.bits.uop.prs2', 'resp_arb.io.out.bits.uop.prs2_busy', 'resp_arb.io.out.bits.uop.prs3', 'resp_arb.io.out.bits.uop.prs3_busy', 'resp_arb.io.out.bits.uop.rob_idx', 'resp_arb.io.out.bits.uop.rxq_idx', 'resp_arb.io.out.bits.uop.stale_pdst', 'resp_arb.io.out.bits.uop.stq_idx', 'resp_arb.io.out.bits.uop.taken', 'resp_arb.io.out.bits.uop.uses_ldq', 'resp_arb.io.out.bits.uop.uses_stq', 'resp_arb.io.out.bits.uop.xcpt_ae_if', 'resp_arb.io.out.bits.uop.xcpt_ma_if', 'resp_arb.io.out.bits.uop.xcpt_pf_if', 'resp_arb.io.out.ready', 'resp_arb.io.out.valid', 'resp_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.resp_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A13": {
      "local_id": "A13",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A14": {
      "local_id": "A14",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A15": {
      "local_id": "A15",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A16": {
      "local_id": "A16",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A17": {
      "local_id": "A17",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A18": {
      "local_id": "A18",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A19": {
      "local_id": "A19",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A20": {
      "local_id": "A20",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A21": {
      "local_id": "A21",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.resp_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::C3_Input2Selected": {
      "local_id": "C3_Input2Selected",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.resp_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::Input2Fire": {
      "local_id": "Input2Fire",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.resp_arb::Higher01Valid": {
      "local_id": "Higher01Valid",
      "work_unit_id": "BoomMSHRFile.resp_arb"
    },
    "BoomMSHRFile.resp_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.resp_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected",
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire",
          "Input2Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire, Input2Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        12,
        16,
        17
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        11,
        13,
        18,
        19
      ],
      "formal": {
        "occurrence": "Input2Fire",
        "predicate": "Higher01Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A3",
      "rendered_formula": "Higher01Valid => !Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.data",
          "op": "signal"
        },
        "target": "io.out.bits.data",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.data = io.in[0].bits.data on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.is_hella",
          "op": "signal"
        },
        "target": "io.out.bits.is_hella",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.is_hella = io.in[0].bits.is_hella on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.rob_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.rob_idx",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.uop.rob_idx = io.in[0].bits.uop.rob_idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.ldq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.ldq_idx",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.uop.ldq_idx = io.in[0].bits.uop.ldq_idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.stq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.stq_idx",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.uop.stq_idx = io.in[0].bits.uop.stq_idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        10
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.uop.mem_cmd",
          "op": "signal"
        },
        "target": "io.out.bits.uop.mem_cmd",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.out.bits.uop.mem_cmd = io.in[0].bits.uop.mem_cmd on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.data",
          "op": "signal"
        },
        "target": "io.out.bits.data",
        "type": "signal_equality"
      },
      "id": "A10",
      "rendered_formula": "io.out.bits.data = io.in[1].bits.data on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.is_hella",
          "op": "signal"
        },
        "target": "io.out.bits.is_hella",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.out.bits.is_hella = io.in[1].bits.is_hella on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.rob_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.rob_idx",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.out.bits.uop.rob_idx = io.in[1].bits.uop.rob_idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.ldq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.ldq_idx",
        "type": "signal_equality"
      },
      "id": "A13",
      "rendered_formula": "io.out.bits.uop.ldq_idx = io.in[1].bits.uop.ldq_idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.stq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.stq_idx",
        "type": "signal_equality"
      },
      "id": "A14",
      "rendered_formula": "io.out.bits.uop.stq_idx = io.in[1].bits.uop.stq_idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        12,
        16,
        17
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.uop.mem_cmd",
          "op": "signal"
        },
        "target": "io.out.bits.uop.mem_cmd",
        "type": "signal_equality"
      },
      "id": "A15",
      "rendered_formula": "io.out.bits.uop.mem_cmd = io.in[1].bits.uop.mem_cmd on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.data",
          "op": "signal"
        },
        "target": "io.out.bits.data",
        "type": "signal_equality"
      },
      "id": "A16",
      "rendered_formula": "io.out.bits.data = io.in[2].bits.data on Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.is_hella",
          "op": "signal"
        },
        "target": "io.out.bits.is_hella",
        "type": "signal_equality"
      },
      "id": "A17",
      "rendered_formula": "io.out.bits.is_hella = io.in[2].bits.is_hella on Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.uop.rob_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.rob_idx",
        "type": "signal_equality"
      },
      "id": "A18",
      "rendered_formula": "io.out.bits.uop.rob_idx = io.in[2].bits.uop.rob_idx on Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.uop.ldq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.ldq_idx",
        "type": "signal_equality"
      },
      "id": "A19",
      "rendered_formula": "io.out.bits.uop.ldq_idx = io.in[2].bits.uop.ldq_idx on Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.uop.stq_idx",
          "op": "signal"
        },
        "target": "io.out.bits.uop.stq_idx",
        "type": "signal_equality"
      },
      "id": "A20",
      "rendered_formula": "io.out.bits.uop.stq_idx = io.in[2].bits.uop.stq_idx on Input2Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C3_Input2Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        13,
        18,
        19
      ],
      "formal": {
        "on": "Input2Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[2].bits.uop.mem_cmd",
          "op": "signal"
        },
        "target": "io.out.bits.uop.mem_cmd",
        "type": "signal_equality"
      },
      "id": "A21",
      "rendered_formula": "io.out.bits.uop.mem_cmd = io.in[2].bits.uop.mem_cmd on Input2Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7,
        8,
        9,
        10,
        14,
        15,
        20,
        21,
        22
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has highest fixed priority and an accepted input-0 response is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        8,
        12,
        16,
        17,
        20,
        21,
        22
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only when input 0 is not valid; the response is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        13,
        18,
        19,
        20,
        21,
        22
      ],
      "guard_predicates": [
        {
          "id": "Higher01Valid",
          "positive": false
        }
      ],
      "id": "C3_Input2Selected",
      "relations": [
        "Input 2 can be accepted only when neither input 0 nor input 1 is valid; the response is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input2Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 21,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 21
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        12,
        16,
        17
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.in[2].valid && io.in[2].ready",
      "evidence_statement_ids": [
        11,
        13,
        18,
        19
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input2Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.in[2].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        20,
        21,
        22
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.resp_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        8,
        12
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    },
    {
      "definition": "io.in[0].valid || io.in[1].valid",
      "evidence_statement_ids": [
        11,
        13
      ],
      "grounding": {
        "negated": false,
        "source_signal": "_grant_T",
        "state_register": null,
        "state_values": []
      },
      "id": "Higher01Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.resp_arb-9f8d9cdf03590f99",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A15",
    "A16",
    "A17",
    "A18",
    "A19",
    "A2",
    "A20",
    "A21",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.resp_arb"
}
```

### Child `BoomMSHRFile.respq`
- summary ref: `umcm://BoomMSHRFile.respq`
- frozen task: `leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e`
- frozen SHA-256: `6f01d0616ea8992148f6cb0621a7612f3fe58310106c18fcad7192309e277174`
- implementation SHA-256: `caf00eaac12117f8e204a14b584ca9f1b963d3b7b4c731340416067f78a1364f`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.respq', 'target_work_unit_id': 'BoomMSHRFile.respq', 'module': 'BranchKillableQueue_4', 'implementation_sha256': 'caf00eaac12117f8e204a14b584ca9f1b963d3b7b4c731340416067f78a1364f', 'structural_implementation_sha256': '3fcfaf82bd6f3cbf845dbcb5d324bce01b680965bd7b6ec9e9ce1eb6cfc07500', 'source_module': 'BranchKillableQueue_4', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.respq::io.deq.fire', 'BoomMSHRFile.respq::io.enq.fire']
- frontier signals: ['respq.clock', 'respq.io', 'respq.io.brupdate.b1.mispredict_mask', 'respq.io.brupdate.b1.resolve_mask', 'respq.io.brupdate.b2.cfi_type', 'respq.io.brupdate.b2.jalr_target', 'respq.io.brupdate.b2.mispredict', 'respq.io.brupdate.b2.pc_sel', 'respq.io.brupdate.b2.taken', 'respq.io.brupdate.b2.target_offset', 'respq.io.brupdate.b2.uop.bp_debug_if', 'respq.io.brupdate.b2.uop.bp_xcpt_if', 'respq.io.brupdate.b2.uop.br_mask', 'respq.io.brupdate.b2.uop.br_tag', 'respq.io.brupdate.b2.uop.br_type', 'respq.io.brupdate.b2.uop.csr_cmd', 'respq.io.brupdate.b2.uop.debug_fsrc', 'respq.io.brupdate.b2.uop.debug_inst', 'respq.io.brupdate.b2.uop.debug_pc', 'respq.io.brupdate.b2.uop.debug_tsrc', 'respq.io.brupdate.b2.uop.dis_col_sel', 'respq.io.brupdate.b2.uop.dst_rtype', 'respq.io.brupdate.b2.uop.edge_inst', 'respq.io.brupdate.b2.uop.exc_cause', 'respq.io.brupdate.b2.uop.exception', 'respq.io.brupdate.b2.uop.fcn_dw', 'respq.io.brupdate.b2.uop.fcn_op', 'respq.io.brupdate.b2.uop.flush_on_commit', 'respq.io.brupdate.b2.uop.fp_ctrl.div', 'respq.io.brupdate.b2.uop.fp_ctrl.fastpipe', 'respq.io.brupdate.b2.uop.fp_ctrl.fma', 'respq.io.brupdate.b2.uop.fp_ctrl.fromint', 'respq.io.brupdate.b2.uop.fp_ctrl.ldst', 'respq.io.brupdate.b2.uop.fp_ctrl.ren1', 'respq.io.brupdate.b2.uop.fp_ctrl.ren2', 'respq.io.brupdate.b2.uop.fp_ctrl.ren3', 'respq.io.brupdate.b2.uop.fp_ctrl.sqrt', 'respq.io.brupdate.b2.uop.fp_ctrl.swap12', 'respq.io.brupdate.b2.uop.fp_ctrl.swap23', 'respq.io.brupdate.b2.uop.fp_ctrl.toint', 'respq.io.brupdate.b2.uop.fp_ctrl.typeTagIn', 'respq.io.brupdate.b2.uop.fp_ctrl.typeTagOut', 'respq.io.brupdate.b2.uop.fp_ctrl.vec', 'respq.io.brupdate.b2.uop.fp_ctrl.wen', 'respq.io.brupdate.b2.uop.fp_ctrl.wflags', 'respq.io.brupdate.b2.uop.fp_rm', 'respq.io.brupdate.b2.uop.fp_typ', 'respq.io.brupdate.b2.uop.fp_val', 'respq.io.brupdate.b2.uop.frs3_en', 'respq.io.brupdate.b2.uop.ftq_idx', 'respq.io.brupdate.b2.uop.fu_code[0]', 'respq.io.brupdate.b2.uop.fu_code[1]', 'respq.io.brupdate.b2.uop.fu_code[2]', 'respq.io.brupdate.b2.uop.fu_code[3]', 'respq.io.brupdate.b2.uop.fu_code[4]', 'respq.io.brupdate.b2.uop.fu_code[5]', 'respq.io.brupdate.b2.uop.fu_code[6]', 'respq.io.brupdate.b2.uop.fu_code[7]', 'respq.io.brupdate.b2.uop.fu_code[8]', 'respq.io.brupdate.b2.uop.fu_code[9]', 'respq.io.brupdate.b2.uop.imm_packed', 'respq.io.brupdate.b2.uop.imm_rename', 'respq.io.brupdate.b2.uop.imm_sel', 'respq.io.brupdate.b2.uop.inst', 'respq.io.brupdate.b2.uop.iq_type[0]', 'respq.io.brupdate.b2.uop.iq_type[1]', 'respq.io.brupdate.b2.uop.iq_type[2]', 'respq.io.brupdate.b2.uop.iq_type[3]', 'respq.io.brupdate.b2.uop.is_amo', 'respq.io.brupdate.b2.uop.is_eret', 'respq.io.brupdate.b2.uop.is_fence', 'respq.io.brupdate.b2.uop.is_fencei', 'respq.io.brupdate.b2.uop.is_mov', 'respq.io.brupdate.b2.uop.is_rocc', 'respq.io.brupdate.b2.uop.is_rvc', 'respq.io.brupdate.b2.uop.is_sfb', 'respq.io.brupdate.b2.uop.is_sfence', 'respq.io.brupdate.b2.uop.is_sys_pc2epc', 'respq.io.brupdate.b2.uop.is_unique', 'respq.io.brupdate.b2.uop.iw_issued', 'respq.io.brupdate.b2.uop.iw_issued_partial_agen', 'respq.io.brupdate.b2.uop.iw_issued_partial_dgen', 'respq.io.brupdate.b2.uop.iw_p1_bypass_hint', 'respq.io.brupdate.b2.uop.iw_p1_speculative_child', 'respq.io.brupdate.b2.uop.iw_p2_bypass_hint', 'respq.io.brupdate.b2.uop.iw_p2_speculative_child', 'respq.io.brupdate.b2.uop.iw_p3_bypass_hint', 'respq.io.brupdate.b2.uop.ldq_idx', 'respq.io.brupdate.b2.uop.ldst', 'respq.io.brupdate.b2.uop.ldst_is_rs1', 'respq.io.brupdate.b2.uop.lrs1', 'respq.io.brupdate.b2.uop.lrs1_rtype', 'respq.io.brupdate.b2.uop.lrs2', 'respq.io.brupdate.b2.uop.lrs2_rtype', 'respq.io.brupdate.b2.uop.lrs3', 'respq.io.brupdate.b2.uop.mem_cmd', 'respq.io.brupdate.b2.uop.mem_signed', 'respq.io.brupdate.b2.uop.mem_size', 'respq.io.brupdate.b2.uop.op1_sel', 'respq.io.brupdate.b2.uop.op2_sel', 'respq.io.brupdate.b2.uop.pc_lob', 'respq.io.brupdate.b2.uop.pdst', 'respq.io.brupdate.b2.uop.pimm', 'respq.io.brupdate.b2.uop.ppred', 'respq.io.brupdate.b2.uop.ppred_busy', 'respq.io.brupdate.b2.uop.prs1', 'respq.io.brupdate.b2.uop.prs1_busy', 'respq.io.brupdate.b2.uop.prs2', 'respq.io.brupdate.b2.uop.prs2_busy', 'respq.io.brupdate.b2.uop.prs3', 'respq.io.brupdate.b2.uop.prs3_busy', 'respq.io.brupdate.b2.uop.rob_idx', 'respq.io.brupdate.b2.uop.rxq_idx', 'respq.io.brupdate.b2.uop.stale_pdst', 'respq.io.brupdate.b2.uop.stq_idx', 'respq.io.brupdate.b2.uop.taken', 'respq.io.brupdate.b2.uop.uses_ldq', 'respq.io.brupdate.b2.uop.uses_stq', 'respq.io.brupdate.b2.uop.xcpt_ae_if', 'respq.io.brupdate.b2.uop.xcpt_ma_if', 'respq.io.brupdate.b2.uop.xcpt_pf_if', 'respq.io.count', 'respq.io.deq.bits.data', 'respq.io.deq.bits.is_hella', 'respq.io.deq.bits.uop.bp_debug_if', 'respq.io.deq.bits.uop.bp_xcpt_if', 'respq.io.deq.bits.uop.br_mask', 'respq.io.deq.bits.uop.br_tag', 'respq.io.deq.bits.uop.br_type', 'respq.io.deq.bits.uop.csr_cmd', 'respq.io.deq.bits.uop.debug_fsrc', 'respq.io.deq.bits.uop.debug_inst', 'respq.io.deq.bits.uop.debug_pc', 'respq.io.deq.bits.uop.debug_tsrc', 'respq.io.deq.bits.uop.dis_col_sel', 'respq.io.deq.bits.uop.dst_rtype', 'respq.io.deq.bits.uop.edge_inst', 'respq.io.deq.bits.uop.exc_cause', 'respq.io.deq.bits.uop.exception', 'respq.io.deq.bits.uop.fcn_dw', 'respq.io.deq.bits.uop.fcn_op', 'respq.io.deq.bits.uop.flush_on_commit', 'respq.io.deq.bits.uop.fp_ctrl.div', 'respq.io.deq.bits.uop.fp_ctrl.fastpipe', 'respq.io.deq.bits.uop.fp_ctrl.fma', 'respq.io.deq.bits.uop.fp_ctrl.fromint', 'respq.io.deq.bits.uop.fp_ctrl.ldst', 'respq.io.deq.bits.uop.fp_ctrl.ren1', 'respq.io.deq.bits.uop.fp_ctrl.ren2', 'respq.io.deq.bits.uop.fp_ctrl.ren3', 'respq.io.deq.bits.uop.fp_ctrl.sqrt', 'respq.io.deq.bits.uop.fp_ctrl.swap12', 'respq.io.deq.bits.uop.fp_ctrl.swap23', 'respq.io.deq.bits.uop.fp_ctrl.toint', 'respq.io.deq.bits.uop.fp_ctrl.typeTagIn', 'respq.io.deq.bits.uop.fp_ctrl.typeTagOut', 'respq.io.deq.bits.uop.fp_ctrl.vec', 'respq.io.deq.bits.uop.fp_ctrl.wen', 'respq.io.deq.bits.uop.fp_ctrl.wflags', 'respq.io.deq.bits.uop.fp_rm', 'respq.io.deq.bits.uop.fp_typ', 'respq.io.deq.bits.uop.fp_val', 'respq.io.deq.bits.uop.frs3_en', 'respq.io.deq.bits.uop.ftq_idx', 'respq.io.deq.bits.uop.fu_code[0]', 'respq.io.deq.bits.uop.fu_code[1]', 'respq.io.deq.bits.uop.fu_code[2]', 'respq.io.deq.bits.uop.fu_code[3]', 'respq.io.deq.bits.uop.fu_code[4]', 'respq.io.deq.bits.uop.fu_code[5]', 'respq.io.deq.bits.uop.fu_code[6]', 'respq.io.deq.bits.uop.fu_code[7]', 'respq.io.deq.bits.uop.fu_code[8]', 'respq.io.deq.bits.uop.fu_code[9]', 'respq.io.deq.bits.uop.imm_packed', 'respq.io.deq.bits.uop.imm_rename', 'respq.io.deq.bits.uop.imm_sel', 'respq.io.deq.bits.uop.inst', 'respq.io.deq.bits.uop.iq_type[0]', 'respq.io.deq.bits.uop.iq_type[1]', 'respq.io.deq.bits.uop.iq_type[2]', 'respq.io.deq.bits.uop.iq_type[3]', 'respq.io.deq.bits.uop.is_amo', 'respq.io.deq.bits.uop.is_eret', 'respq.io.deq.bits.uop.is_fence', 'respq.io.deq.bits.uop.is_fencei', 'respq.io.deq.bits.uop.is_mov', 'respq.io.deq.bits.uop.is_rocc', 'respq.io.deq.bits.uop.is_rvc', 'respq.io.deq.bits.uop.is_sfb', 'respq.io.deq.bits.uop.is_sfence', 'respq.io.deq.bits.uop.is_sys_pc2epc', 'respq.io.deq.bits.uop.is_unique', 'respq.io.deq.bits.uop.iw_issued', 'respq.io.deq.bits.uop.iw_issued_partial_agen', 'respq.io.deq.bits.uop.iw_issued_partial_dgen', 'respq.io.deq.bits.uop.iw_p1_bypass_hint', 'respq.io.deq.bits.uop.iw_p1_speculative_child', 'respq.io.deq.bits.uop.iw_p2_bypass_hint', 'respq.io.deq.bits.uop.iw_p2_speculative_child', 'respq.io.deq.bits.uop.iw_p3_bypass_hint', 'respq.io.deq.bits.uop.ldq_idx', 'respq.io.deq.bits.uop.ldst', 'respq.io.deq.bits.uop.ldst_is_rs1', 'respq.io.deq.bits.uop.lrs1', 'respq.io.deq.bits.uop.lrs1_rtype', 'respq.io.deq.bits.uop.lrs2', 'respq.io.deq.bits.uop.lrs2_rtype', 'respq.io.deq.bits.uop.lrs3', 'respq.io.deq.bits.uop.mem_cmd', 'respq.io.deq.bits.uop.mem_signed', 'respq.io.deq.bits.uop.mem_size', 'respq.io.deq.bits.uop.op1_sel', 'respq.io.deq.bits.uop.op2_sel', 'respq.io.deq.bits.uop.pc_lob', 'respq.io.deq.bits.uop.pdst', 'respq.io.deq.bits.uop.pimm', 'respq.io.deq.bits.uop.ppred', 'respq.io.deq.bits.uop.ppred_busy', 'respq.io.deq.bits.uop.prs1', 'respq.io.deq.bits.uop.prs1_busy', 'respq.io.deq.bits.uop.prs2', 'respq.io.deq.bits.uop.prs2_busy', 'respq.io.deq.bits.uop.prs3', 'respq.io.deq.bits.uop.prs3_busy', 'respq.io.deq.bits.uop.rob_idx', 'respq.io.deq.bits.uop.rxq_idx', 'respq.io.deq.bits.uop.stale_pdst', 'respq.io.deq.bits.uop.stq_idx', 'respq.io.deq.bits.uop.taken', 'respq.io.deq.bits.uop.uses_ldq', 'respq.io.deq.bits.uop.uses_stq', 'respq.io.deq.bits.uop.xcpt_ae_if', 'respq.io.deq.bits.uop.xcpt_ma_if', 'respq.io.deq.bits.uop.xcpt_pf_if', 'respq.io.deq.ready', 'respq.io.deq.valid', 'respq.io.empty', 'respq.io.enq.bits.data', 'respq.io.enq.bits.is_hella', 'respq.io.enq.bits.uop.bp_debug_if', 'respq.io.enq.bits.uop.bp_xcpt_if', 'respq.io.enq.bits.uop.br_mask', 'respq.io.enq.bits.uop.br_tag', 'respq.io.enq.bits.uop.br_type', 'respq.io.enq.bits.uop.csr_cmd', 'respq.io.enq.bits.uop.debug_fsrc', 'respq.io.enq.bits.uop.debug_inst', 'respq.io.enq.bits.uop.debug_pc', 'respq.io.enq.bits.uop.debug_tsrc', 'respq.io.enq.bits.uop.dis_col_sel', 'respq.io.enq.bits.uop.dst_rtype', 'respq.io.enq.bits.uop.edge_inst', 'respq.io.enq.bits.uop.exc_cause', 'respq.io.enq.bits.uop.exception', 'respq.io.enq.bits.uop.fcn_dw', 'respq.io.enq.bits.uop.fcn_op', 'respq.io.enq.bits.uop.flush_on_commit', 'respq.io.enq.bits.uop.fp_ctrl.div', 'respq.io.enq.bits.uop.fp_ctrl.fastpipe', 'respq.io.enq.bits.uop.fp_ctrl.fma', 'respq.io.enq.bits.uop.fp_ctrl.fromint', 'respq.io.enq.bits.uop.fp_ctrl.ldst', 'respq.io.enq.bits.uop.fp_ctrl.ren1', 'respq.io.enq.bits.uop.fp_ctrl.ren2', 'respq.io.enq.bits.uop.fp_ctrl.ren3', 'respq.io.enq.bits.uop.fp_ctrl.sqrt', 'respq.io.enq.bits.uop.fp_ctrl.swap12', 'respq.io.enq.bits.uop.fp_ctrl.swap23', 'respq.io.enq.bits.uop.fp_ctrl.toint', 'respq.io.enq.bits.uop.fp_ctrl.typeTagIn', 'respq.io.enq.bits.uop.fp_ctrl.typeTagOut', 'respq.io.enq.bits.uop.fp_ctrl.vec', 'respq.io.enq.bits.uop.fp_ctrl.wen', 'respq.io.enq.bits.uop.fp_ctrl.wflags', 'respq.io.enq.bits.uop.fp_rm', 'respq.io.enq.bits.uop.fp_typ', 'respq.io.enq.bits.uop.fp_val', 'respq.io.enq.bits.uop.frs3_en', 'respq.io.enq.bits.uop.ftq_idx', 'respq.io.enq.bits.uop.fu_code[0]', 'respq.io.enq.bits.uop.fu_code[1]', 'respq.io.enq.bits.uop.fu_code[2]', 'respq.io.enq.bits.uop.fu_code[3]', 'respq.io.enq.bits.uop.fu_code[4]', 'respq.io.enq.bits.uop.fu_code[5]', 'respq.io.enq.bits.uop.fu_code[6]', 'respq.io.enq.bits.uop.fu_code[7]', 'respq.io.enq.bits.uop.fu_code[8]', 'respq.io.enq.bits.uop.fu_code[9]', 'respq.io.enq.bits.uop.imm_packed', 'respq.io.enq.bits.uop.imm_rename', 'respq.io.enq.bits.uop.imm_sel', 'respq.io.enq.bits.uop.inst', 'respq.io.enq.bits.uop.iq_type[0]', 'respq.io.enq.bits.uop.iq_type[1]', 'respq.io.enq.bits.uop.iq_type[2]', 'respq.io.enq.bits.uop.iq_type[3]', 'respq.io.enq.bits.uop.is_amo', 'respq.io.enq.bits.uop.is_eret', 'respq.io.enq.bits.uop.is_fence', 'respq.io.enq.bits.uop.is_fencei', 'respq.io.enq.bits.uop.is_mov', 'respq.io.enq.bits.uop.is_rocc', 'respq.io.enq.bits.uop.is_rvc', 'respq.io.enq.bits.uop.is_sfb', 'respq.io.enq.bits.uop.is_sfence', 'respq.io.enq.bits.uop.is_sys_pc2epc', 'respq.io.enq.bits.uop.is_unique', 'respq.io.enq.bits.uop.iw_issued', 'respq.io.enq.bits.uop.iw_issued_partial_agen', 'respq.io.enq.bits.uop.iw_issued_partial_dgen', 'respq.io.enq.bits.uop.iw_p1_bypass_hint', 'respq.io.enq.bits.uop.iw_p1_speculative_child', 'respq.io.enq.bits.uop.iw_p2_bypass_hint', 'respq.io.enq.bits.uop.iw_p2_speculative_child', 'respq.io.enq.bits.uop.iw_p3_bypass_hint', 'respq.io.enq.bits.uop.ldq_idx', 'respq.io.enq.bits.uop.ldst', 'respq.io.enq.bits.uop.ldst_is_rs1', 'respq.io.enq.bits.uop.lrs1', 'respq.io.enq.bits.uop.lrs1_rtype', 'respq.io.enq.bits.uop.lrs2', 'respq.io.enq.bits.uop.lrs2_rtype', 'respq.io.enq.bits.uop.lrs3', 'respq.io.enq.bits.uop.mem_cmd', 'respq.io.enq.bits.uop.mem_signed', 'respq.io.enq.bits.uop.mem_size', 'respq.io.enq.bits.uop.op1_sel', 'respq.io.enq.bits.uop.op2_sel', 'respq.io.enq.bits.uop.pc_lob', 'respq.io.enq.bits.uop.pdst', 'respq.io.enq.bits.uop.pimm', 'respq.io.enq.bits.uop.ppred', 'respq.io.enq.bits.uop.ppred_busy', 'respq.io.enq.bits.uop.prs1', 'respq.io.enq.bits.uop.prs1_busy', 'respq.io.enq.bits.uop.prs2', 'respq.io.enq.bits.uop.prs2_busy', 'respq.io.enq.bits.uop.prs3', 'respq.io.enq.bits.uop.prs3_busy', 'respq.io.enq.bits.uop.rob_idx', 'respq.io.enq.bits.uop.rxq_idx', 'respq.io.enq.bits.uop.stale_pdst', 'respq.io.enq.bits.uop.stq_idx', 'respq.io.enq.bits.uop.taken', 'respq.io.enq.bits.uop.uses_ldq', 'respq.io.enq.bits.uop.uses_stq', 'respq.io.enq.bits.uop.xcpt_ae_if', 'respq.io.enq.bits.uop.xcpt_ma_if', 'respq.io.enq.bits.uop.xcpt_pf_if', 'respq.io.enq.ready', 'respq.io.enq.valid', 'respq.io.flush', 'respq.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.respq::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.respq"
    }
  },
  "cases": {
    "BoomMSHRFile.respq::C1_Admitted": {
      "local_id": "C1_Admitted",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::C2_BranchKilledOnArrival": {
      "local_id": "C2_BranchKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::C3_FlushKilledOnArrival": {
      "local_id": "C3_FlushKilledOnArrival",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::C4_VisibleDequeue": {
      "local_id": "C4_VisibleDequeue",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::C5_InvalidHeadSkip": {
      "local_id": "C5_InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.respq"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.respq::DeqHandshake": {
      "local_id": "DeqHandshake",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::EnqHandshake": {
      "local_id": "EnqHandshake",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::InvalidHeadSkip": {
      "local_id": "InvalidHeadSkip",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::QueueInsert": {
      "local_id": "QueueInsert",
      "work_unit_id": "BoomMSHRFile.respq"
    }
  },
  "predicates": {
    "BoomMSHRFile.respq::HeadInvalid": {
      "local_id": "HeadInvalid",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::HeadValid": {
      "local_id": "HeadValid",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::IncomingBranchKilled": {
      "local_id": "IncomingBranchKilled",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::IncomingFlushKilled": {
      "local_id": "IncomingFlushKilled",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::QueueEmpty": {
      "local_id": "QueueEmpty",
      "work_unit_id": "BoomMSHRFile.respq"
    },
    "BoomMSHRFile.respq::QueueFull": {
      "local_id": "QueueFull",
      "work_unit_id": "BoomMSHRFile.respq"
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
        18,
        19,
        109,
        110
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
        20,
        21,
        22,
        23,
        24,
        27,
        28,
        29
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
        25,
        26,
        27,
        28,
        29
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
        15,
        16,
        17,
        115,
        116,
        117
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
        30,
        115,
        116,
        117
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
        32,
        33,
        34,
        35
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
        30,
        31,
        32,
        33,
        34,
        35,
        115,
        116,
        117
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
        88,
        89,
        90
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
        5,
        6,
        7,
        8,
        9,
        11,
        12,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        88,
        91,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
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
      "id": "A9",
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
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        89,
        90,
        91,
        92,
        95,
        99
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
        "An enqueue handshake is admitted only when it survives both incoming branch-kill and flush-kill filters; the admitted payload is stored at the current enqueue slot."
      ],
      "trigger_occurrences": [
        "EnqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        19,
        20,
        21,
        22,
        23,
        24,
        28,
        29,
        88,
        99
      ],
      "guard_predicates": [
        {
          "id": "IncomingBranchKilled",
          "positive": true
        }
      ],
      "id": "C2_BranchKilledOnArrival",
      "relations": [
        "The external enqueue handshake may occur, but a branch-killed request is not inserted and does not advance the enqueue pointer."
      ],
      "trigger_occurrences": [
        "EnqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        19,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        99
      ],
      "guard_predicates": [
        {
          "id": "IncomingFlushKilled",
          "positive": true
        }
      ],
      "id": "C3_FlushKilledOnArrival",
      "relations": [
        "An enqueue carrying uses_ldq is rejected from actual queue insertion when io.flush is asserted."
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
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
      ],
      "guard_predicates": [
        {
          "id": "QueueEmpty",
          "positive": false
        },
        {
          "id": "HeadValid",
          "positive": true
        }
      ],
      "id": "C4_VisibleDequeue",
      "relations": [
        "A visible dequeue handshake consumes the valid current head slot and advances the dequeue pointer."
      ],
      "trigger_occurrences": [
        "DeqHandshake"
      ]
    },
    {
      "confidence": "high",
      "emits": [],
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
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
        "A non-empty queue whose current head slot has been invalidated advances past that slot without producing a visible dequeue handshake."
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
        19,
        109,
        110
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
        "BoomMSHRFile.respq::io.enq.fire"
      ]
    },
    {
      "definition": "do_enq",
      "evidence_statement_ids": [
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99
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
          "end_exclusive": 4,
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
        12,
        30,
        31,
        32,
        33,
        34,
        35,
        115,
        116,
        117,
        118
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
          "end_exclusive": 4,
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
        "BoomMSHRFile.respq::io.deq.fire"
      ]
    },
    {
      "definition": "do_deq && !io.deq.valid",
      "evidence_statement_ids": [
        30,
        31,
        32,
        33,
        34,
        35,
        100,
        101,
        102,
        103,
        104,
        105,
        115,
        116,
        117
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
          "end_exclusive": 4,
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
      "definition": "io.empty",
      "evidence_statement_ids": [
        14,
        15,
        16,
        17
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
      "definition": "full",
      "evidence_statement_ids": [
        14,
        18,
        109,
        110
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
        20,
        21,
        22,
        23
      ],
      "grounding": {
        "negated": false,
        "source_signal": "_do_enq_T_3",
        "state_register": null,
        "state_values": []
      },
      "id": "IncomingBranchKilled"
    },
    {
      "definition": "io.flush && io.enq.bits.uop.uses_ldq",
      "evidence_statement_ids": [
        25,
        26,
        27
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
      "definition": "!valids[deq_ptr_value]",
      "evidence_statement_ids": [
        30,
        115,
        116
      ],
      "grounding": {
        "negated": true,
        "source_signal": "valids[deq_ptr_value]",
        "state_register": null,
        "state_values": []
      },
      "id": "HeadInvalid"
    },
    {
      "definition": "valids[deq_ptr_value]",
      "evidence_statement_ids": [
        30,
        115,
        116
      ],
      "grounding": {
        "negated": false,
        "source_signal": "valids[deq_ptr_value]",
        "state_register": null,
        "state_values": []
      },
      "id": "HeadValid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.respq"
}
```

### Child `BoomMSHRFile.wb_req_arb`
- summary ref: `umcm://BoomMSHRFile.wb_req_arb`
- frozen task: `leaf_abstraction-BoomMSHRFile.wb_req_arb-3fab8edcb559ff62`
- frozen SHA-256: `da22e6ad082f03e2017e2a32e2529463cf6f80ffdd9eb16e880f2277c00be41f`
- implementation SHA-256: `6ec06cfd78ba9edf87cb498dcf3756300d0eb8dd77b282ebde1cf29b0e6eaf98`
- instance reuse certificate: `{'kind': 'exact-work-unit', 'source_work_unit_id': 'BoomMSHRFile.wb_req_arb', 'target_work_unit_id': 'BoomMSHRFile.wb_req_arb', 'module': 'Arbiter2_WritebackReq', 'implementation_sha256': '6ec06cfd78ba9edf87cb498dcf3756300d0eb8dd77b282ebde1cf29b0e6eaf98', 'structural_implementation_sha256': '6761f40baa091fa90e386915c5aed710d78c4db5f10c2686708f7846ed655000', 'source_module': 'Arbiter2_WritebackReq', 'verification': 'exact-work-unit-id'}`
- exposed boundary events: ['BoomMSHRFile.wb_req_arb::io.in[0].fire', 'BoomMSHRFile.wb_req_arb::io.in[1].fire', 'BoomMSHRFile.wb_req_arb::io.out.fire']
- frontier signals: ['wb_req_arb.clock', 'wb_req_arb.io', 'wb_req_arb.io.chosen', 'wb_req_arb.io.in[0].bits.idx', 'wb_req_arb.io.in[0].bits.param', 'wb_req_arb.io.in[0].bits.source', 'wb_req_arb.io.in[0].bits.tag', 'wb_req_arb.io.in[0].bits.voluntary', 'wb_req_arb.io.in[0].bits.way_en', 'wb_req_arb.io.in[0].ready', 'wb_req_arb.io.in[0].valid', 'wb_req_arb.io.in[1].bits.idx', 'wb_req_arb.io.in[1].bits.param', 'wb_req_arb.io.in[1].bits.source', 'wb_req_arb.io.in[1].bits.tag', 'wb_req_arb.io.in[1].bits.voluntary', 'wb_req_arb.io.in[1].bits.way_en', 'wb_req_arb.io.in[1].ready', 'wb_req_arb.io.in[1].valid', 'wb_req_arb.io.out.bits.idx', 'wb_req_arb.io.out.bits.param', 'wb_req_arb.io.out.bits.source', 'wb_req_arb.io.out.bits.tag', 'wb_req_arb.io.out.bits.voluntary', 'wb_req_arb.io.out.bits.way_en', 'wb_req_arb.io.out.ready', 'wb_req_arb.io.out.valid', 'wb_req_arb.reset']

Qualified semantic IDs available to parent formal AST:
```json
{
  "axioms": {
    "BoomMSHRFile.wb_req_arb::A1": {
      "local_id": "A1",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A10": {
      "local_id": "A10",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A11": {
      "local_id": "A11",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A12": {
      "local_id": "A12",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A13": {
      "local_id": "A13",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A14": {
      "local_id": "A14",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A2": {
      "local_id": "A2",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A3": {
      "local_id": "A3",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A4": {
      "local_id": "A4",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A5": {
      "local_id": "A5",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A6": {
      "local_id": "A6",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A7": {
      "local_id": "A7",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A8": {
      "local_id": "A8",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::A9": {
      "local_id": "A9",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    }
  },
  "cases": {
    "BoomMSHRFile.wb_req_arb::C1_Input0Selected": {
      "local_id": "C1_Input0Selected",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::C2_Input1Selected": {
      "local_id": "C2_Input1Selected",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    }
  },
  "identity_keys": {},
  "occurrences": {
    "BoomMSHRFile.wb_req_arb::Input0Fire": {
      "local_id": "Input0Fire",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::Input1Fire": {
      "local_id": "Input1Fire",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    },
    "BoomMSHRFile.wb_req_arb::OutputFire": {
      "local_id": "OutputFire",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
    }
  },
  "predicates": {
    "BoomMSHRFile.wb_req_arb::Input0Valid": {
      "local_id": "Input0Valid",
      "work_unit_id": "BoomMSHRFile.wb_req_arb"
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
        "C1_Input0Selected",
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
      ],
      "formal": {
        "parts": [
          "Input0Fire",
          "Input1Fire"
        ],
        "relation": "same_cycle_exactly_one",
        "scope_identity": null,
        "type": "occurrence_partition",
        "whole": "OutputFire"
      },
      "id": "A1",
      "rendered_formula": "OutputFire <=> exactly_one_same_cycle({Input0Fire, Input1Fire})",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "formal": {
        "occurrence": "Input1Fire",
        "predicate": "Input0Valid",
        "scope_identity": null,
        "type": "forbid_when"
      },
      "id": "A2",
      "rendered_formula": "Input0Valid => !Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A3",
      "rendered_formula": "io.out.bits.tag = io.in[0].bits.tag on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A4",
      "rendered_formula": "io.out.bits.idx = io.in[0].bits.idx on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.source",
          "op": "signal"
        },
        "target": "io.out.bits.source",
        "type": "signal_equality"
      },
      "id": "A5",
      "rendered_formula": "io.out.bits.source = io.in[0].bits.source on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.param",
          "op": "signal"
        },
        "target": "io.out.bits.param",
        "type": "signal_equality"
      },
      "id": "A6",
      "rendered_formula": "io.out.bits.param = io.in[0].bits.param on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A7",
      "rendered_formula": "io.out.bits.way_en = io.in[0].bits.way_en on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C1_Input0Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        7
      ],
      "formal": {
        "on": "Input0Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[0].bits.voluntary",
          "op": "signal"
        },
        "target": "io.out.bits.voluntary",
        "type": "signal_equality"
      },
      "id": "A8",
      "rendered_formula": "io.out.bits.voluntary = io.in[0].bits.voluntary on Input0Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.tag",
          "op": "signal"
        },
        "target": "io.out.bits.tag",
        "type": "signal_equality"
      },
      "id": "A9",
      "rendered_formula": "io.out.bits.tag = io.in[1].bits.tag on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.idx",
          "op": "signal"
        },
        "target": "io.out.bits.idx",
        "type": "signal_equality"
      },
      "id": "A10",
      "rendered_formula": "io.out.bits.idx = io.in[1].bits.idx on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.source",
          "op": "signal"
        },
        "target": "io.out.bits.source",
        "type": "signal_equality"
      },
      "id": "A11",
      "rendered_formula": "io.out.bits.source = io.in[1].bits.source on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.param",
          "op": "signal"
        },
        "target": "io.out.bits.param",
        "type": "signal_equality"
      },
      "id": "A12",
      "rendered_formula": "io.out.bits.param = io.in[1].bits.param on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.way_en",
          "op": "signal"
        },
        "target": "io.out.bits.way_en",
        "type": "signal_equality"
      },
      "id": "A13",
      "rendered_formula": "io.out.bits.way_en = io.in[1].bits.way_en on Input1Fire",
      "status": "candidate"
    },
    {
      "derived_from_case_ids": [
        "C2_Input1Selected"
      ],
      "evidence_statement_ids": [
        4,
        5,
        8,
        11,
        12
      ],
      "formal": {
        "on": "Input1Fire",
        "scope_identity": null,
        "source": {
          "name": "io.in[1].bits.voluntary",
          "op": "signal"
        },
        "target": "io.out.bits.voluntary",
        "type": "signal_equality"
      },
      "id": "A14",
      "rendered_formula": "io.out.bits.voluntary = io.in[1].bits.voluntary on Input1Fire",
      "status": "candidate"
    }
  ],
  "cases": [
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        4,
        5,
        6,
        7,
        9,
        10,
        13,
        14,
        15
      ],
      "guard_predicates": [],
      "id": "C1_Input0Selected",
      "relations": [
        "Input 0 has fixed priority; an accepted input-0 writeback request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input0Fire"
      ]
    },
    {
      "confidence": "high",
      "emits": [
        "OutputFire"
      ],
      "evidence_statement_ids": [
        3,
        4,
        5,
        8,
        11,
        12,
        13,
        14,
        15
      ],
      "guard_predicates": [
        {
          "id": "Input0Valid",
          "positive": false
        }
      ],
      "id": "C2_Input1Selected",
      "relations": [
        "Input 1 can be accepted only when input 0 is not valid; the accepted writeback request is forwarded to the output in the same cycle."
      ],
      "trigger_occurrences": [
        "Input1Fire"
      ]
    }
  ],
  "freeze": {
    "candidate_axiom_count": 14,
    "policy": "all-declared-axioms-trusted-and-no-unresolved-v0.1",
    "reopen_policy": "This summary may be reopened if later parent/system counterexample validation shows the abstraction is too weak and a missing concrete constraint must be synthesized.",
    "status": "FROZEN_FOR_COMPOSITION",
    "trusted_axiom_count": 14
  },
  "identity_keys": [],
  "note": "Only axioms with FORMALLY_PROVED or SPEC_PROVED validation level are included. Grounded/structurally-supported candidate axioms remain outside the trusted abstraction.",
  "occurrences": [
    {
      "definition": "io.in[0].valid && io.in[0].ready",
      "evidence_statement_ids": [
        9,
        10
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.wb_req_arb::io.in[0].fire"
      ]
    },
    {
      "definition": "io.in[1].valid && io.in[1].ready",
      "evidence_statement_ids": [
        8,
        11,
        12
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "Input1Fire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.wb_req_arb::io.in[1].fire"
      ]
    },
    {
      "definition": "io.out.valid && io.out.ready",
      "evidence_statement_ids": [
        13,
        14,
        15
      ],
      "grounding": {
        "signals_false": [],
        "signals_true": [],
        "state_register": null,
        "state_values": []
      },
      "id": "OutputFire",
      "index": null,
      "kind": "boundary",
      "multiplicity": "repeatable",
      "physical_event_ids": [
        "BoomMSHRFile.wb_req_arb::io.out.fire"
      ]
    }
  ],
  "predicates": [
    {
      "definition": "io.in[0].valid",
      "evidence_statement_ids": [
        5,
        8
      ],
      "grounding": {
        "negated": false,
        "source_signal": "io.in[0].valid",
        "state_register": null,
        "state_values": []
      },
      "id": "Input0Valid"
    }
  ],
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomMSHRFile.wb_req_arb-3fab8edcb559ff62",
  "trust_policy": "formal-ast-plus-certified-provenance-v0.3",
  "trusted_axiom_ids": [
    "A1",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9"
  ],
  "work_unit_id": "BoomMSHRFile.wb_req_arb"
}
```

## Parent-local source evidence

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:497-499
```scala

class BoomMSHRFile(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
  with HasL1HellaCacheParameters
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:500-502
```scala
{
  val io = IO(new Bundle {
    val req  = Flipped(Vec(lsuWidth, Decoupled(new BoomDCacheReqInternal))) // Req from s2 of DCache pipe
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:535-537
```scala
  val req_idx = OHToUInt(io.req.map(_.valid))
  val req     = WireInit(io.req(req_idx))
  val req_is_probe = io.req_is_probe(0)
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:539-541
```scala
  for (w <- 0 until lsuWidth)
    io.req(w).ready := false.B
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:542-546
```scala
  val prefetcher: DataPrefetcher = if (enablePrefetching) Module(new NLPrefetcher)
                                                     else Module(new NullPrefetcher)

  io.prefetch <> prefetcher.io.prefetch
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:551-560
```scala
  // The MSHR SDQ
  val sdq_val      = RegInit(0.U(cfg.nSDQ.W))
  val sdq_alloc_id = PriorityEncoder(~sdq_val(cfg.nSDQ-1,0))
  val sdq_rdy      = !sdq_val.andR
  val sdq_enq      = req.fire && cacheable && isWrite(req.bits.uop.mem_cmd)
  val sdq          = Mem(cfg.nSDQ, UInt(coreDataBits.W))

  when (sdq_enq) {
    sdq(sdq_alloc_id) := req.bits.data
  }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:564-567
```scala
  // Holds refilling lines, prefetched lines
  val lb = Reg(Vec(nLBEntries, Vec(cacheDataBeats, UInt(encRowBits.W))))
  def widthMap[T <: Data](f: Int => T) = VecInit((0 until lsuWidth).map(f))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:570-574
```scala

  val idx_matches = Wire(Vec(lsuWidth, Vec(cfg.nMSHRs, Bool())))
  val tag_matches = Wire(Vec(lsuWidth, Vec(cfg.nMSHRs, Bool())))
  val way_matches = Wire(Vec(lsuWidth, Vec(cfg.nMSHRs, Bool())))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:575-577
```scala
  val tag_match   = widthMap(w => Mux1H(idx_matches(w), tag_matches(w)))
  val idx_match   = widthMap(w => idx_matches(w).reduce(_||_))
  val way_match   = widthMap(w => Mux1H(idx_matches(w), way_matches(w)))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:578-591
```scala

  val wb_tag_list = Wire(Vec(cfg.nMSHRs, UInt(tagBits.W)))

  val meta_write_arb = Module(new Arbiter(new L1MetaWriteReq           , cfg.nMSHRs))
  val meta_read_arb  = Module(new Arbiter(new L1MetaReadReq            , cfg.nMSHRs))
  val wb_req_arb     = Module(new Arbiter(new WritebackReq(edge.bundle), cfg.nMSHRs))
  val replay_arb     = Module(new Arbiter(new BoomDCacheReqInternal    , cfg.nMSHRs))
  val resp_arb       = Module(new Arbiter(new BoomDCacheResp           , cfg.nMSHRs + nIOMSHRs))
  val refill_arb     = Module(new Arbiter(new L1DataWriteReq           , cfg.nMSHRs))

  val commit_vals    = Wire(Vec(cfg.nMSHRs, Bool()))
  val commit_addrs   = Wire(Vec(cfg.nMSHRs, UInt(coreMaxAddrBits.W)))
  val commit_cohs    = Wire(Vec(cfg.nMSHRs, new ClientMetadata))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:593-604
```scala

  io.fence_rdy := true.B
  io.probe_rdy := true.B
  io.mem_grant.ready := false.B

  val mshr_alloc_idx = Wire(UInt())
  val pri_rdy = WireInit(false.B)
  val pri_val = req.valid && sdq_rdy && cacheable && !idx_match(req_idx)
  val mshrs = (0 until cfg.nMSHRs) map { i =>
    val mshr = Module(new BoomMSHR)
    mshr.io.id := i.U(log2Ceil(cfg.nMSHRs).W)
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:605-611
```scala
    for (w <- 0 until lsuWidth) {
      idx_matches(w)(i) := mshr.io.idx.valid && mshr.io.idx.bits === io.req(w).bits.addr(untagBits-1,blockOffBits)
      tag_matches(w)(i) := mshr.io.tag.valid && mshr.io.tag.bits === io.req(w).bits.addr >> untagBits
      way_matches(w)(i) := mshr.io.way.valid && mshr.io.way.bits === io.req(w).bits.way_en
    }
    wb_tag_list(i) := mshr.io.wb_req.bits.tag
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:613-617
```scala

    mshr.io.req_pri_val  := (i.U === mshr_alloc_idx) && pri_val
    when (i.U === mshr_alloc_idx) {
      pri_rdy := mshr.io.req_pri_rdy
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:618-623
```scala

    mshr.io.req_sec_val  := req.valid && sdq_rdy && tag_match(req_idx) && idx_matches(req_idx)(i) && cacheable
    mshr.io.req          := req.bits
    mshr.io.req_is_probe := req_is_probe
    mshr.io.req.sdq_id   := sdq_alloc_id
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:625-648
```scala
    // a probe to that prefetched line, all mshrs are in use
    mshr.io.clear_prefetch := ((io.clear_all && !req.valid)||
      (req.valid && idx_matches(req_idx)(i) && cacheable && !tag_match(req_idx)) ||
      (req_is_probe && idx_matches(req_idx)(i)))
    mshr.io.brupdate       := io.brupdate
    mshr.io.exception    := io.exception
    mshr.io.rob_pnr_idx  := io.rob_pnr_idx
    mshr.io.rob_head_idx := io.rob_head_idx

    mshr.io.prober_state := io.prober_state

    mshr.io.wb_resp      := io.wb_resp

    meta_write_arb.io.in(i) <> mshr.io.meta_write
    meta_read_arb.io.in(i)  <> mshr.io.meta_read
    mshr.io.meta_resp       := io.meta_resp
    wb_req_arb.io.in(i)     <> mshr.io.wb_req
    replay_arb.io.in(i)     <> mshr.io.replay
    refill_arb.io.in(i)     <> mshr.io.refill

    mshr.io.lb_resp            := lb(i)(mshr.io.lb_read.offset)
    when (mshr.io.lb_write.valid) {
      lb(i)(mshr.io.lb_write.bits.offset) := mshr.io.lb_write.bits.data
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:649-658
```scala

    commit_vals(i)  := mshr.io.commit_val
    commit_addrs(i) := mshr.io.commit_addr
    commit_cohs(i)  := mshr.io.commit_coh

    mshr.io.mem_grant.valid := false.B
    mshr.io.mem_grant.bits  := DontCare
    when (io.mem_grant.bits.source === i.U) {
      mshr.io.mem_grant <> io.mem_grant
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:659-665
```scala

    sec_rdy   = sec_rdy || (mshr.io.req_sec_rdy && mshr.io.req_sec_val)
    resp_arb.io.in(i) <> mshr.io.resp

    when (!mshr.io.req_pri_rdy) {
      io.fence_rdy := false.B
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:666-669
```scala
    for (w <- 0 until lsuWidth) {
      when (!mshr.io.probe_rdy && idx_matches(w)(i) && io.req_is_probe(w)) {
        io.probe_rdy := false.B
      }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:675-679
```scala
  // Try to round-robin the MSHRs
  val mshr_head      = RegInit(0.U(log2Ceil(cfg.nMSHRs).W))
  mshr_alloc_idx    := RegNext(AgePriorityEncoder(mshrs.map(m=>m.io.req_pri_rdy), mshr_head))
  when (pri_rdy && pri_val) { mshr_head := WrapInc(mshr_head, cfg.nMSHRs) }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:681-687
```scala

  io.meta_write <> meta_write_arb.io.out
  io.meta_read  <> meta_read_arb.io.out
  io.wb_req     <> wb_req_arb.io.out

  val mmio_alloc_arb = Module(new Arbiter(Bool(), nIOMSHRs))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:692-706
```scala
    val id = cfg.nMSHRs + 1 + i // +1 for wb unit
    val mshr = Module(new BoomIOMSHR(id))

    mmio_alloc_arb.io.in(i).valid := mshr.io.req.ready
    mmio_alloc_arb.io.in(i).bits  := DontCare
    mshr.io.req.valid := mmio_alloc_arb.io.in(i).ready
    mshr.io.req.bits  := req.bits

    mmio_rdy = mmio_rdy || mshr.io.req.ready

    mshr.io.mem_ack.bits  := io.mem_grant.bits
    mshr.io.mem_ack.valid := io.mem_grant.valid && io.mem_grant.bits.source === id.U
    when (io.mem_grant.bits.source === id.U) {
      io.mem_grant.ready := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:707-711
```scala

    resp_arb.io.in(cfg.nMSHRs + i) <> mshr.io.resp
    when (!mshr.io.req.ready) {
      io.fence_rdy := false.B
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:714-716
```scala

  mmio_alloc_arb.io.out.ready := req.valid && !cacheable
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:719-725
```scala

  val respq = Module(new BranchKillableQueue(new BoomDCacheResp, 4, u => u.uses_ldq))
  respq.io.brupdate  := io.brupdate
  respq.io.flush     := io.exception
  respq.io.enq       <> resp_arb.io.out
  io.resp            <> respq.io.deq
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:726-742
```scala
  for (w <- 0 until lsuWidth) {
    io.req(w).ready      := (w.U === req_idx) &&
      Mux(!cacheable, mmio_rdy, sdq_rdy && Mux(idx_match(w), tag_match(w) && sec_rdy, pri_rdy))
    io.secondary_miss(w) := idx_match(w) && way_match(w) && !tag_match(w)
    io.block_hit(w)      := idx_match(w) && tag_match(w)
  }
  io.refill         <> refill_arb.io.out

  val free_sdq = io.replay.fire && isWrite(io.replay.bits.uop.mem_cmd)

  io.replay <> replay_arb.io.out
  io.replay.bits.data := sdq(replay_arb.io.out.bits.sdq_id)

  when (io.replay.valid || sdq_enq) {
    sdq_val := sdq_val & ~(UIntToOH(replay_arb.io.out.bits.sdq_id) & Fill(cfg.nSDQ, free_sdq)) |
      PriorityEncoderOH(~sdq_val(cfg.nSDQ-1,0)) & Fill(cfg.nSDQ, sdq_enq)
  }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:743-748
```scala

  prefetcher.io.mshr_avail    := RegNext(pri_rdy)
  prefetcher.io.req_val       := RegNext(commit_vals.reduce(_||_))
  prefetcher.io.req_addr      := RegNext(Mux1H(commit_vals, commit_addrs))
  prefetcher.io.req_coh       := RegNext(Mux1H(commit_vals, commit_cohs))
}
```

### generators/boom/src/main/scala/v4/util/util.scala:210-212
```scala
    if (isPow2(n)) {
      (value + 1.U)(log2Ceil(n)-1,0)
    } else {
```

### generators/boom/src/main/scala/v4/util/util.scala:370-374
```scala
    val n_padded = 1 << width
    val temp_vec = (0 until n_padded).map(i => if (i < n) in(i) && i.U >= head else false.B) ++ in
    val idx = PriorityEncoder(temp_vec)
    idx(width-1, 0) //discard msb
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

### generators/rocket-chip/src/main/scala/rocket/Consts.scala:86-88
```scala
  def isAMOArithmetic(cmd: UInt) = cmd.isOneOf(M_XA_ADD, M_XA_MIN, M_XA_MAX, M_XA_MINU, M_XA_MAXU)
  def isAMO(cmd: UInt) = isAMOLogical(cmd) || isAMOArithmetic(cmd)
  def isPrefetch(cmd: UInt) = cmd === M_PFR || cmd === M_PFW
```

### generators/rocket-chip/src/main/scala/rocket/Consts.scala:89-91
```scala
  def isRead(cmd: UInt) = cmd.isOneOf(M_XRD, M_HLVX, M_XLR, M_XSC) || isAMO(cmd)
  def isWrite(cmd: UInt) = cmd === M_XWR || cmd === M_PWR || cmd === M_XSC || isAMO(cmd)
  def isWriteIntent(cmd: UInt) = isWrite(cmd) || cmd === M_PFW || cmd === M_XLR
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:15-17
```scala

  val lowestIndexFirst: Policy = (width, valids, select) => ~(leftOR(valids) << 1)(width-1, 0)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:59-63
```scala
      // The number of beats which remain to be sent
      val beatsLeft = RegInit(0.U)
      val idle = beatsLeft === 0.U
      val latch = idle && sink.ready // winner (if any) claims sink
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

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:81-86
```scala
      // Track remaining beats
      val maskedBeats = (winner zip beatsIn) map { case (w,b) => Mux(w, b, 0.U) }

      val initBeats = maskedBeats.reduce(_ | _) // no winner => 0 beats
      beatsLeft := Mux(latch, initBeats, beatsLeft - sink.fire)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:87-98
```scala
      // The one-hot source granted access in the previous cycle
      val state = RegInit(VecInit(Seq.fill(sources.size)(false.B)))
      val muxState = Mux(idle, winner, state)
      state := muxState

      val allowed = Mux(idle, readys, state)
      (sourcesIn zip allowed) foreach { case (s, r) =>
        s.ready := sink.ready && r
      }
      sink.valid := Mux(idle, valids.reduce(_||_), Mux1H(state, valids))
      sink.bits :<= Mux1H(muxState, sourcesIn.map(_.bits))
    }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:91-93
```scala
    val opdata = x match {
      case a: TLBundleA => !a.opcode(2)
        //    opcode === TLMessages.PutFullData    ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:219-222
```scala
        } else {
          val decode = UIntToOH1(size(bundle), maxLgSize) >> log2Ceil(manager.beatBytes)
          Mux(hasData(bundle), decode, 0.U)
        }
```

### generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:683-687
```scala
    // We return an or-reduction of all the cases, checking whether any contains both the dynamic size and dynamic address on the wire.
      ((Some(s) == range).B || s.containsLg(lgSize)) &&
      a.map(_.contains(address)).reduce(_||_)
    }.foldLeft(false.B)(_||_)
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

### generators/rocket-chip/src/main/scala/util/package.scala:253-256
```scala
    def helper(s: Int, x: UInt): UInt =
      if (s >= stop) x else helper(s+s, x | (x << s)(width-1,0))
    helper(1, x)(width-1, 0)
  }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Parent-local FIRRTL statement ledger

Only these parent-local statement IDs may appear in `evidence_statement_ids`.

```text
[0] FIRRTL:195762 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:498:7 KIND:structural :: input clock : Clock
[1] FIRRTL:195763 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:498:7 KIND:structural :: input reset : Reset
[2] FIRRTL:195764 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:501:14 KIND:structural :: output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}[1], flip req_is_probe : UInt<1>[1], resp : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, secondary_miss : UInt<1>[1], block_hit : UInt<1>[1], flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip exception : UInt<1>, flip rob_pnr_idx : UInt<5>, flip rob_head_idx : UInt<5>, mem_acquire : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, flip mem_grant : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, sink : UInt<3>, denied : UInt<1>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, mem_finish : { flip ready : UInt<1>, valid : UInt<1>, bits : { sink : UInt<3>}}, refill : { flip ready : UInt<1>, valid : UInt<1>, bits : { way_en : UInt<4>, addr : UInt<12>, wmask : UInt<1>, data : UInt<64>}}, meta_write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>, data : { coh : { state : UInt<2>}, tag : UInt<20>}}}, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}}, flip meta_resp : { valid : UInt<1>, bits : { coh : { state : UInt<2>}, tag : UInt<20>}}, replay : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, prefetch : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}, wb_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { tag : UInt<20>, idx : UInt<6>, source : UInt<2>, param : UInt<3>, way_en : UInt<4>, voluntary : UInt<1>}}, flip prober_state : { valid : UInt<1>, bits : UInt<40>}, flip clear_all : UInt<1>, flip wb_resp : UInt<1>, fence_rdy : UInt<1>, probe_rdy : UInt<1>}
[3] FIRRTL:195766 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:536:25 KIND:wire :: wire req : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}
[4] FIRRTL:195767 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:536:25 KIND:connect :: connect req.bits, io.req[0].bits
[5] FIRRTL:195768 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:536:25 KIND:connect :: connect req.valid, io.req[0].valid
[6] FIRRTL:195769 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:536:25 KIND:connect :: connect req.ready, io.req[0].ready
[7] FIRRTL:195770 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:540:21 KIND:connect :: connect io.req[0].ready, UInt<1>(0h0)
[8] FIRRTL:195771 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:543:65 KIND:structural :: inst prefetcher of NullPrefetcher
[9] FIRRTL:195772 SRC:<no-source-locator> KIND:connect :: connect prefetcher.clock, clock
[10] FIRRTL:195773 SRC:<no-source-locator> KIND:connect :: connect prefetcher.reset, reset
[11] FIRRTL:195774 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:545:15 KIND:connect :: connect io.prefetch.bits, prefetcher.io.prefetch.bits
[12] FIRRTL:195775 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:545:15 KIND:connect :: connect io.prefetch.valid, prefetcher.io.prefetch.valid
[13] FIRRTL:195776 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:545:15 KIND:connect :: connect prefetcher.io.prefetch.ready, io.prefetch.ready
[14] FIRRTL:195777 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _cacheable_T = or(UInt<1>(0h0), UInt<1>(0h0))
[15] FIRRTL:195778 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _cacheable_T_1 = xor(req.bits.addr, UInt<1>(0h0))
[16] FIRRTL:195779 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _cacheable_T_2 = cvt(_cacheable_T_1)
[17] FIRRTL:195780 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_3 = and(_cacheable_T_2, asSInt(UInt<33>(0h8c000000)))
[18] FIRRTL:195781 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_4 = asSInt(_cacheable_T_3)
[19] FIRRTL:195782 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _cacheable_T_5 = eq(_cacheable_T_4, asSInt(UInt<1>(0h0)))
[20] FIRRTL:195783 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _cacheable_T_6 = xor(req.bits.addr, UInt<17>(0h10000))
[21] FIRRTL:195784 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _cacheable_T_7 = cvt(_cacheable_T_6)
[22] FIRRTL:195785 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_8 = and(_cacheable_T_7, asSInt(UInt<33>(0h8c011000)))
[23] FIRRTL:195786 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_9 = asSInt(_cacheable_T_8)
[24] FIRRTL:195787 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _cacheable_T_10 = eq(_cacheable_T_9, asSInt(UInt<1>(0h0)))
[25] FIRRTL:195788 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _cacheable_T_11 = xor(req.bits.addr, UInt<28>(0hc000000))
[26] FIRRTL:195789 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _cacheable_T_12 = cvt(_cacheable_T_11)
[27] FIRRTL:195790 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_13 = and(_cacheable_T_12, asSInt(UInt<33>(0h8c000000)))
[28] FIRRTL:195791 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_14 = asSInt(_cacheable_T_13)
[29] FIRRTL:195792 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _cacheable_T_15 = eq(_cacheable_T_14, asSInt(UInt<1>(0h0)))
[30] FIRRTL:195793 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _cacheable_T_16 = or(_cacheable_T_5, _cacheable_T_10)
[31] FIRRTL:195794 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _cacheable_T_17 = or(_cacheable_T_16, _cacheable_T_15)
[32] FIRRTL:195795 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _cacheable_T_18 = and(_cacheable_T, _cacheable_T_17)
[33] FIRRTL:195796 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:93:44 KIND:node :: node _cacheable_T_19 = eq(UInt<3>(0h6), UInt<3>(0h6))
[34] FIRRTL:195797 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _cacheable_T_20 = or(UInt<1>(0h0), _cacheable_T_19)
[35] FIRRTL:195798 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _cacheable_T_21 = xor(req.bits.addr, UInt<28>(0h8000000))
[36] FIRRTL:195799 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _cacheable_T_22 = cvt(_cacheable_T_21)
[37] FIRRTL:195800 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_23 = and(_cacheable_T_22, asSInt(UInt<33>(0h8c010000)))
[38] FIRRTL:195801 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_24 = asSInt(_cacheable_T_23)
[39] FIRRTL:195802 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _cacheable_T_25 = eq(_cacheable_T_24, asSInt(UInt<1>(0h0)))
[40] FIRRTL:195803 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _cacheable_T_26 = xor(req.bits.addr, UInt<32>(0h80000000))
[41] FIRRTL:195804 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _cacheable_T_27 = cvt(_cacheable_T_26)
[42] FIRRTL:195805 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_28 = and(_cacheable_T_27, asSInt(UInt<33>(0h80000000)))
[43] FIRRTL:195806 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _cacheable_T_29 = asSInt(_cacheable_T_28)
[44] FIRRTL:195807 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _cacheable_T_30 = eq(_cacheable_T_29, asSInt(UInt<1>(0h0)))
[45] FIRRTL:195808 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _cacheable_T_31 = or(_cacheable_T_25, _cacheable_T_30)
[46] FIRRTL:195809 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _cacheable_T_32 = and(_cacheable_T_20, _cacheable_T_31)
[47] FIRRTL:195810 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _cacheable_T_33 = or(UInt<1>(0h0), _cacheable_T_18)
[48] FIRRTL:195811 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node cacheable = or(_cacheable_T_33, _cacheable_T_32)
[49] FIRRTL:195812 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:552:29 KIND:regreset :: regreset sdq_val : UInt<17>, clock, reset, UInt<17>(0h0)
[50] FIRRTL:195813 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:553:46 KIND:node :: node _sdq_alloc_id_T = bits(sdq_val, 16, 0)
[51] FIRRTL:195814 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:553:38 KIND:node :: node _sdq_alloc_id_T_1 = not(_sdq_alloc_id_T)
[52] FIRRTL:195815 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_2 = bits(_sdq_alloc_id_T_1, 0, 0)
[53] FIRRTL:195816 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_3 = bits(_sdq_alloc_id_T_1, 1, 1)
[54] FIRRTL:195817 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_4 = bits(_sdq_alloc_id_T_1, 2, 2)
[55] FIRRTL:195818 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_5 = bits(_sdq_alloc_id_T_1, 3, 3)
[56] FIRRTL:195819 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_6 = bits(_sdq_alloc_id_T_1, 4, 4)
[57] FIRRTL:195820 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_7 = bits(_sdq_alloc_id_T_1, 5, 5)
[58] FIRRTL:195821 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_8 = bits(_sdq_alloc_id_T_1, 6, 6)
[59] FIRRTL:195822 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_9 = bits(_sdq_alloc_id_T_1, 7, 7)
[60] FIRRTL:195823 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_10 = bits(_sdq_alloc_id_T_1, 8, 8)
[61] FIRRTL:195824 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_11 = bits(_sdq_alloc_id_T_1, 9, 9)
[62] FIRRTL:195825 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_12 = bits(_sdq_alloc_id_T_1, 10, 10)
[63] FIRRTL:195826 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_13 = bits(_sdq_alloc_id_T_1, 11, 11)
[64] FIRRTL:195827 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_14 = bits(_sdq_alloc_id_T_1, 12, 12)
[65] FIRRTL:195828 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_15 = bits(_sdq_alloc_id_T_1, 13, 13)
[66] FIRRTL:195829 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_16 = bits(_sdq_alloc_id_T_1, 14, 14)
[67] FIRRTL:195830 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_17 = bits(_sdq_alloc_id_T_1, 15, 15)
[68] FIRRTL:195831 SRC:src/main/scala/chisel3/util/OneHot.scala:48:45 KIND:node :: node _sdq_alloc_id_T_18 = bits(_sdq_alloc_id_T_1, 16, 16)
[69] FIRRTL:195832 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_19 = mux(_sdq_alloc_id_T_17, UInt<4>(0hf), UInt<5>(0h10))
[70] FIRRTL:195833 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_20 = mux(_sdq_alloc_id_T_16, UInt<4>(0he), _sdq_alloc_id_T_19)
[71] FIRRTL:195834 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_21 = mux(_sdq_alloc_id_T_15, UInt<4>(0hd), _sdq_alloc_id_T_20)
[72] FIRRTL:195835 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_22 = mux(_sdq_alloc_id_T_14, UInt<4>(0hc), _sdq_alloc_id_T_21)
[73] FIRRTL:195836 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_23 = mux(_sdq_alloc_id_T_13, UInt<4>(0hb), _sdq_alloc_id_T_22)
[74] FIRRTL:195837 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_24 = mux(_sdq_alloc_id_T_12, UInt<4>(0ha), _sdq_alloc_id_T_23)
[75] FIRRTL:195838 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_25 = mux(_sdq_alloc_id_T_11, UInt<4>(0h9), _sdq_alloc_id_T_24)
[76] FIRRTL:195839 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_26 = mux(_sdq_alloc_id_T_10, UInt<4>(0h8), _sdq_alloc_id_T_25)
[77] FIRRTL:195840 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_27 = mux(_sdq_alloc_id_T_9, UInt<3>(0h7), _sdq_alloc_id_T_26)
[78] FIRRTL:195841 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_28 = mux(_sdq_alloc_id_T_8, UInt<3>(0h6), _sdq_alloc_id_T_27)
[79] FIRRTL:195842 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_29 = mux(_sdq_alloc_id_T_7, UInt<3>(0h5), _sdq_alloc_id_T_28)
[80] FIRRTL:195843 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_30 = mux(_sdq_alloc_id_T_6, UInt<3>(0h4), _sdq_alloc_id_T_29)
[81] FIRRTL:195844 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_31 = mux(_sdq_alloc_id_T_5, UInt<2>(0h3), _sdq_alloc_id_T_30)
[82] FIRRTL:195845 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_32 = mux(_sdq_alloc_id_T_4, UInt<2>(0h2), _sdq_alloc_id_T_31)
[83] FIRRTL:195846 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_alloc_id_T_33 = mux(_sdq_alloc_id_T_3, UInt<1>(0h1), _sdq_alloc_id_T_32)
[84] FIRRTL:195847 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node sdq_alloc_id = mux(_sdq_alloc_id_T_2, UInt<1>(0h0), _sdq_alloc_id_T_33)
[85] FIRRTL:195848 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:554:31 KIND:node :: node _sdq_rdy_T = andr(sdq_val)
[86] FIRRTL:195849 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:554:22 KIND:node :: node sdq_rdy = eq(_sdq_rdy_T, UInt<1>(0h0))
[87] FIRRTL:195850 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _sdq_enq_T = and(req.ready, req.valid)
[88] FIRRTL:195851 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:555:31 KIND:node :: node _sdq_enq_T_1 = and(_sdq_enq_T, cacheable)
[89] FIRRTL:195852 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _sdq_enq_T_2 = eq(req.bits.uop.mem_cmd, UInt<1>(0h1))
[90] FIRRTL:195853 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _sdq_enq_T_3 = eq(req.bits.uop.mem_cmd, UInt<5>(0h11))
[91] FIRRTL:195854 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _sdq_enq_T_4 = or(_sdq_enq_T_2, _sdq_enq_T_3)
[92] FIRRTL:195855 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _sdq_enq_T_5 = eq(req.bits.uop.mem_cmd, UInt<3>(0h7))
[93] FIRRTL:195856 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _sdq_enq_T_6 = or(_sdq_enq_T_4, _sdq_enq_T_5)
[94] FIRRTL:195857 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_7 = eq(req.bits.uop.mem_cmd, UInt<3>(0h4))
[95] FIRRTL:195858 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_8 = eq(req.bits.uop.mem_cmd, UInt<4>(0h9))
[96] FIRRTL:195859 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_9 = eq(req.bits.uop.mem_cmd, UInt<4>(0ha))
[97] FIRRTL:195860 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_10 = eq(req.bits.uop.mem_cmd, UInt<4>(0hb))
[98] FIRRTL:195861 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_11 = or(_sdq_enq_T_7, _sdq_enq_T_8)
[99] FIRRTL:195862 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_12 = or(_sdq_enq_T_11, _sdq_enq_T_9)
[100] FIRRTL:195863 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_13 = or(_sdq_enq_T_12, _sdq_enq_T_10)
[101] FIRRTL:195864 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_14 = eq(req.bits.uop.mem_cmd, UInt<4>(0h8))
[102] FIRRTL:195865 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_15 = eq(req.bits.uop.mem_cmd, UInt<4>(0hc))
[103] FIRRTL:195866 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_16 = eq(req.bits.uop.mem_cmd, UInt<4>(0hd))
[104] FIRRTL:195867 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_17 = eq(req.bits.uop.mem_cmd, UInt<4>(0he))
[105] FIRRTL:195868 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _sdq_enq_T_18 = eq(req.bits.uop.mem_cmd, UInt<4>(0hf))
[106] FIRRTL:195869 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_19 = or(_sdq_enq_T_14, _sdq_enq_T_15)
[107] FIRRTL:195870 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_20 = or(_sdq_enq_T_19, _sdq_enq_T_16)
[108] FIRRTL:195871 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_21 = or(_sdq_enq_T_20, _sdq_enq_T_17)
[109] FIRRTL:195872 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _sdq_enq_T_22 = or(_sdq_enq_T_21, _sdq_enq_T_18)
[110] FIRRTL:195873 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _sdq_enq_T_23 = or(_sdq_enq_T_13, _sdq_enq_T_22)
[111] FIRRTL:195874 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _sdq_enq_T_24 = or(_sdq_enq_T_6, _sdq_enq_T_23)
[112] FIRRTL:195875 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:555:44 KIND:node :: node sdq_enq = and(_sdq_enq_T_1, _sdq_enq_T_24)
[113] FIRRTL:195876 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:556:25 KIND:memory :: cmem sdq : UInt<64> [17]
[114] FIRRTL:195877 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:558:18 KIND:when :: when sdq_enq :
[115] FIRRTL:195878 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:559:8 KIND:infer_mport :: infer mport MPORT = sdq[sdq_alloc_id], clock
[116] FIRRTL:195879 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:559:23 KIND:connect :: connect MPORT, req.bits.data
[117] FIRRTL:195880 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:565:15 KIND:reg :: reg lb : UInt<64>[8][2], clock
[118] FIRRTL:195881 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:571:25 KIND:wire :: wire idx_matches : UInt<1>[2][1]
[119] FIRRTL:195882 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:572:25 KIND:wire :: wire tag_matches : UInt<1>[2][1]
[120] FIRRTL:195883 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:573:25 KIND:wire :: wire way_matches : UInt<1>[2][1]
[121] FIRRTL:195884 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _tag_match_T = mux(idx_matches[0][0], tag_matches[0][0], UInt<1>(0h0))
[122] FIRRTL:195885 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _tag_match_T_1 = mux(idx_matches[0][1], tag_matches[0][1], UInt<1>(0h0))
[123] FIRRTL:195886 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _tag_match_T_2 = or(_tag_match_T, _tag_match_T_1)
[124] FIRRTL:195887 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _tag_match_WIRE : UInt<1>
[125] FIRRTL:195888 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _tag_match_WIRE, _tag_match_T_2
[126] FIRRTL:195889 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:wire :: wire tag_match : UInt<1>[1]
[127] FIRRTL:195890 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:connect :: connect tag_match[0], _tag_match_WIRE
[128] FIRRTL:195891 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:576:58 KIND:node :: node _idx_match_T = or(idx_matches[0][0], idx_matches[0][1])
[129] FIRRTL:195892 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:wire :: wire idx_match : UInt<1>[1]
[130] FIRRTL:195893 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:connect :: connect idx_match[0], _idx_match_T
[131] FIRRTL:195894 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _way_match_T = mux(idx_matches[0][0], way_matches[0][0], UInt<1>(0h0))
[132] FIRRTL:195895 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _way_match_T_1 = mux(idx_matches[0][1], way_matches[0][1], UInt<1>(0h0))
[133] FIRRTL:195896 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _way_match_T_2 = or(_way_match_T, _way_match_T_1)
[134] FIRRTL:195897 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _way_match_WIRE : UInt<1>
[135] FIRRTL:195898 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _way_match_WIRE, _way_match_T_2
[136] FIRRTL:195899 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:wire :: wire way_match : UInt<1>[1]
[137] FIRRTL:195900 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:566:49 KIND:connect :: connect way_match[0], _way_match_WIRE
[138] FIRRTL:195901 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:579:25 KIND:wire :: wire wb_tag_list : UInt<20>[2]
[139] FIRRTL:195902 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:581:30 KIND:structural :: inst meta_write_arb of Arbiter2_L1MetaWriteReq
[140] FIRRTL:195903 SRC:<no-source-locator> KIND:connect :: connect meta_write_arb.clock, clock
[141] FIRRTL:195904 SRC:<no-source-locator> KIND:connect :: connect meta_write_arb.reset, reset
[142] FIRRTL:195905 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:582:30 KIND:structural :: inst meta_read_arb of Arbiter2_L1MetaReadReq
[143] FIRRTL:195906 SRC:<no-source-locator> KIND:connect :: connect meta_read_arb.clock, clock
[144] FIRRTL:195907 SRC:<no-source-locator> KIND:connect :: connect meta_read_arb.reset, reset
[145] FIRRTL:195908 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:583:30 KIND:structural :: inst wb_req_arb of Arbiter2_WritebackReq
[146] FIRRTL:195909 SRC:<no-source-locator> KIND:connect :: connect wb_req_arb.clock, clock
[147] FIRRTL:195910 SRC:<no-source-locator> KIND:connect :: connect wb_req_arb.reset, reset
[148] FIRRTL:195911 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:584:30 KIND:structural :: inst replay_arb of Arbiter2_BoomDCacheReqInternal
[149] FIRRTL:195912 SRC:<no-source-locator> KIND:connect :: connect replay_arb.clock, clock
[150] FIRRTL:195913 SRC:<no-source-locator> KIND:connect :: connect replay_arb.reset, reset
[151] FIRRTL:195914 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:585:30 KIND:structural :: inst resp_arb of Arbiter3_BoomDCacheResp
[152] FIRRTL:195915 SRC:<no-source-locator> KIND:connect :: connect resp_arb.clock, clock
[153] FIRRTL:195916 SRC:<no-source-locator> KIND:connect :: connect resp_arb.reset, reset
[154] FIRRTL:195917 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:586:30 KIND:structural :: inst refill_arb of Arbiter2_L1DataWriteReq
[155] FIRRTL:195918 SRC:<no-source-locator> KIND:connect :: connect refill_arb.clock, clock
[156] FIRRTL:195919 SRC:<no-source-locator> KIND:connect :: connect refill_arb.reset, reset
[157] FIRRTL:195920 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:588:28 KIND:wire :: wire commit_vals : UInt<1>[2]
[158] FIRRTL:195921 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:589:28 KIND:wire :: wire commit_addrs : UInt<40>[2]
[159] FIRRTL:195922 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:590:28 KIND:wire :: wire commit_cohs : { state : UInt<2>}[2]
[160] FIRRTL:195923 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:594:16 KIND:connect :: connect io.fence_rdy, UInt<1>(0h1)
[161] FIRRTL:195924 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:595:16 KIND:connect :: connect io.probe_rdy, UInt<1>(0h1)
[162] FIRRTL:195925 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:596:22 KIND:connect :: connect io.mem_grant.ready, UInt<1>(0h0)
[163] FIRRTL:195926 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:598:28 KIND:wire :: wire mshr_alloc_idx : UInt
[164] FIRRTL:195927 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:599:25 KIND:wire :: wire pri_rdy : UInt<1>
[165] FIRRTL:195928 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:599:25 KIND:connect :: connect pri_rdy, UInt<1>(0h0)
[166] FIRRTL:195929 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:600:27 KIND:node :: node _pri_val_T = and(req.valid, sdq_rdy)
[167] FIRRTL:195930 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:600:38 KIND:node :: node _pri_val_T_1 = and(_pri_val_T, cacheable)
[168] FIRRTL:195931 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:600:54 KIND:node :: node _pri_val_T_2 = eq(idx_match[0], UInt<1>(0h0))
[169] FIRRTL:195932 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:600:51 KIND:node :: node pri_val = and(_pri_val_T_1, _pri_val_T_2)
[170] FIRRTL:195933 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:602:22 KIND:structural :: inst mshrs_0 of BoomMSHR
[171] FIRRTL:195934 SRC:<no-source-locator> KIND:connect :: connect mshrs_0.clock, clock
[172] FIRRTL:195935 SRC:<no-source-locator> KIND:connect :: connect mshrs_0.reset, reset
[173] FIRRTL:195936 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:603:16 KIND:connect :: connect mshrs_0.io.id, UInt<1>(0h0)
[174] FIRRTL:195937 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:89 KIND:node :: node _idx_matches_0_0_T = bits(io.req[0].bits.addr, 11, 6)
[175] FIRRTL:195938 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:66 KIND:node :: node _idx_matches_0_0_T_1 = eq(mshrs_0.io.idx.bits, _idx_matches_0_0_T)
[176] FIRRTL:195939 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:46 KIND:node :: node _idx_matches_0_0_T_2 = and(mshrs_0.io.idx.valid, _idx_matches_0_0_T_1)
[177] FIRRTL:195940 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:25 KIND:connect :: connect idx_matches[0][0], _idx_matches_0_0_T_2
[178] FIRRTL:195941 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:90 KIND:node :: node _tag_matches_0_0_T = shr(io.req[0].bits.addr, 12)
[179] FIRRTL:195942 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:66 KIND:node :: node _tag_matches_0_0_T_1 = eq(mshrs_0.io.tag.bits, _tag_matches_0_0_T)
[180] FIRRTL:195943 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:46 KIND:node :: node _tag_matches_0_0_T_2 = and(mshrs_0.io.tag.valid, _tag_matches_0_0_T_1)
[181] FIRRTL:195944 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:25 KIND:connect :: connect tag_matches[0][0], _tag_matches_0_0_T_2
[182] FIRRTL:195945 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:66 KIND:node :: node _way_matches_0_0_T = eq(mshrs_0.io.way.bits, io.req[0].bits.way_en)
[183] FIRRTL:195946 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:46 KIND:node :: node _way_matches_0_0_T_1 = and(mshrs_0.io.way.valid, _way_matches_0_0_T)
[184] FIRRTL:195947 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:25 KIND:connect :: connect way_matches[0][0], _way_matches_0_0_T_1
[185] FIRRTL:195948 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:610:20 KIND:connect :: connect wb_tag_list[0], mshrs_0.io.wb_req.bits.tag
[186] FIRRTL:195949 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:34 KIND:node :: node _mshr_io_req_pri_val_T = eq(UInt<1>(0h0), mshr_alloc_idx)
[187] FIRRTL:195950 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:54 KIND:node :: node _mshr_io_req_pri_val_T_1 = and(_mshr_io_req_pri_val_T, pri_val)
[188] FIRRTL:195951 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:26 KIND:connect :: connect mshrs_0.io.req_pri_val, _mshr_io_req_pri_val_T_1
[189] FIRRTL:195952 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:615:15 KIND:node :: node _T = eq(UInt<1>(0h0), mshr_alloc_idx)
[190] FIRRTL:195953 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:615:35 KIND:when :: when _T :
[191] FIRRTL:195954 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:616:15 KIND:connect :: connect pri_rdy, mshrs_0.io.req_pri_rdy
[192] FIRRTL:195955 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:39 KIND:node :: node _mshr_io_req_sec_val_T = and(req.valid, sdq_rdy)
[193] FIRRTL:195956 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:50 KIND:node :: node _mshr_io_req_sec_val_T_1 = and(_mshr_io_req_sec_val_T, tag_match[0])
[194] FIRRTL:195957 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:72 KIND:node :: node _mshr_io_req_sec_val_T_2 = and(_mshr_io_req_sec_val_T_1, idx_matches[0][0])
[195] FIRRTL:195958 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:99 KIND:node :: node _mshr_io_req_sec_val_T_3 = and(_mshr_io_req_sec_val_T_2, cacheable)
[196] FIRRTL:195959 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:26 KIND:connect :: connect mshrs_0.io.req_sec_val, _mshr_io_req_sec_val_T_3
[197] FIRRTL:195960 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.sdq_id, req.bits.sdq_id
[198] FIRRTL:195961 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.way_en, req.bits.way_en
[199] FIRRTL:195962 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.old_meta.tag, req.bits.old_meta.tag
[200] FIRRTL:195963 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.old_meta.coh.state, req.bits.old_meta.coh.state
[201] FIRRTL:195964 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.tag_match, req.bits.tag_match
[202] FIRRTL:195965 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.is_hella, req.bits.is_hella
[203] FIRRTL:195966 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.data, req.bits.data
[204] FIRRTL:195967 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.addr, req.bits.addr
[205] FIRRTL:195968 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.debug_tsrc, req.bits.uop.debug_tsrc
[206] FIRRTL:195969 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.debug_fsrc, req.bits.uop.debug_fsrc
[207] FIRRTL:195970 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.bp_xcpt_if, req.bits.uop.bp_xcpt_if
[208] FIRRTL:195971 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.bp_debug_if, req.bits.uop.bp_debug_if
[209] FIRRTL:195972 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.xcpt_ma_if, req.bits.uop.xcpt_ma_if
[210] FIRRTL:195973 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.xcpt_ae_if, req.bits.uop.xcpt_ae_if
[211] FIRRTL:195974 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.xcpt_pf_if, req.bits.uop.xcpt_pf_if
[212] FIRRTL:195975 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_typ, req.bits.uop.fp_typ
[213] FIRRTL:195976 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_rm, req.bits.uop.fp_rm
[214] FIRRTL:195977 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_val, req.bits.uop.fp_val
[215] FIRRTL:195978 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fcn_op, req.bits.uop.fcn_op
[216] FIRRTL:195979 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fcn_dw, req.bits.uop.fcn_dw
[217] FIRRTL:195980 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.frs3_en, req.bits.uop.frs3_en
[218] FIRRTL:195981 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.lrs2_rtype, req.bits.uop.lrs2_rtype
[219] FIRRTL:195982 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.lrs1_rtype, req.bits.uop.lrs1_rtype
[220] FIRRTL:195983 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.dst_rtype, req.bits.uop.dst_rtype
[221] FIRRTL:195984 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.lrs3, req.bits.uop.lrs3
[222] FIRRTL:195985 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.lrs2, req.bits.uop.lrs2
[223] FIRRTL:195986 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.lrs1, req.bits.uop.lrs1
[224] FIRRTL:195987 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ldst, req.bits.uop.ldst
[225] FIRRTL:195988 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ldst_is_rs1, req.bits.uop.ldst_is_rs1
[226] FIRRTL:195989 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.csr_cmd, req.bits.uop.csr_cmd
[227] FIRRTL:195990 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.flush_on_commit, req.bits.uop.flush_on_commit
[228] FIRRTL:195991 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_unique, req.bits.uop.is_unique
[229] FIRRTL:195992 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.uses_stq, req.bits.uop.uses_stq
[230] FIRRTL:195993 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.uses_ldq, req.bits.uop.uses_ldq
[231] FIRRTL:195994 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.mem_signed, req.bits.uop.mem_signed
[232] FIRRTL:195995 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.mem_size, req.bits.uop.mem_size
[233] FIRRTL:195996 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.mem_cmd, req.bits.uop.mem_cmd
[234] FIRRTL:195997 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.exc_cause, req.bits.uop.exc_cause
[235] FIRRTL:195998 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.exception, req.bits.uop.exception
[236] FIRRTL:195999 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.stale_pdst, req.bits.uop.stale_pdst
[237] FIRRTL:196000 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ppred_busy, req.bits.uop.ppred_busy
[238] FIRRTL:196001 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs3_busy, req.bits.uop.prs3_busy
[239] FIRRTL:196002 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs2_busy, req.bits.uop.prs2_busy
[240] FIRRTL:196003 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs1_busy, req.bits.uop.prs1_busy
[241] FIRRTL:196004 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ppred, req.bits.uop.ppred
[242] FIRRTL:196005 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs3, req.bits.uop.prs3
[243] FIRRTL:196006 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs2, req.bits.uop.prs2
[244] FIRRTL:196007 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.prs1, req.bits.uop.prs1
[245] FIRRTL:196008 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.pdst, req.bits.uop.pdst
[246] FIRRTL:196009 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.rxq_idx, req.bits.uop.rxq_idx
[247] FIRRTL:196010 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.stq_idx, req.bits.uop.stq_idx
[248] FIRRTL:196011 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ldq_idx, req.bits.uop.ldq_idx
[249] FIRRTL:196012 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.rob_idx, req.bits.uop.rob_idx
[250] FIRRTL:196013 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.vec, req.bits.uop.fp_ctrl.vec
[251] FIRRTL:196014 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.wflags, req.bits.uop.fp_ctrl.wflags
[252] FIRRTL:196015 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.sqrt, req.bits.uop.fp_ctrl.sqrt
[253] FIRRTL:196016 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.div, req.bits.uop.fp_ctrl.div
[254] FIRRTL:196017 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.fma, req.bits.uop.fp_ctrl.fma
[255] FIRRTL:196018 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.fastpipe, req.bits.uop.fp_ctrl.fastpipe
[256] FIRRTL:196019 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.toint, req.bits.uop.fp_ctrl.toint
[257] FIRRTL:196020 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.fromint, req.bits.uop.fp_ctrl.fromint
[258] FIRRTL:196021 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.typeTagOut, req.bits.uop.fp_ctrl.typeTagOut
[259] FIRRTL:196022 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.typeTagIn, req.bits.uop.fp_ctrl.typeTagIn
[260] FIRRTL:196023 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.swap23, req.bits.uop.fp_ctrl.swap23
[261] FIRRTL:196024 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.swap12, req.bits.uop.fp_ctrl.swap12
[262] FIRRTL:196025 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.ren3, req.bits.uop.fp_ctrl.ren3
[263] FIRRTL:196026 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.ren2, req.bits.uop.fp_ctrl.ren2
[264] FIRRTL:196027 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.ren1, req.bits.uop.fp_ctrl.ren1
[265] FIRRTL:196028 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.wen, req.bits.uop.fp_ctrl.wen
[266] FIRRTL:196029 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fp_ctrl.ldst, req.bits.uop.fp_ctrl.ldst
[267] FIRRTL:196030 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.op2_sel, req.bits.uop.op2_sel
[268] FIRRTL:196031 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.op1_sel, req.bits.uop.op1_sel
[269] FIRRTL:196032 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.imm_packed, req.bits.uop.imm_packed
[270] FIRRTL:196033 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.pimm, req.bits.uop.pimm
[271] FIRRTL:196034 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.imm_sel, req.bits.uop.imm_sel
[272] FIRRTL:196035 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.imm_rename, req.bits.uop.imm_rename
[273] FIRRTL:196036 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.taken, req.bits.uop.taken
[274] FIRRTL:196037 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.pc_lob, req.bits.uop.pc_lob
[275] FIRRTL:196038 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.edge_inst, req.bits.uop.edge_inst
[276] FIRRTL:196039 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.ftq_idx, req.bits.uop.ftq_idx
[277] FIRRTL:196040 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_mov, req.bits.uop.is_mov
[278] FIRRTL:196041 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_rocc, req.bits.uop.is_rocc
[279] FIRRTL:196042 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_sys_pc2epc, req.bits.uop.is_sys_pc2epc
[280] FIRRTL:196043 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_eret, req.bits.uop.is_eret
[281] FIRRTL:196044 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_amo, req.bits.uop.is_amo
[282] FIRRTL:196045 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_sfence, req.bits.uop.is_sfence
[283] FIRRTL:196046 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_fencei, req.bits.uop.is_fencei
[284] FIRRTL:196047 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_fence, req.bits.uop.is_fence
[285] FIRRTL:196048 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_sfb, req.bits.uop.is_sfb
[286] FIRRTL:196049 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.br_type, req.bits.uop.br_type
[287] FIRRTL:196050 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.br_tag, req.bits.uop.br_tag
[288] FIRRTL:196051 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.br_mask, req.bits.uop.br_mask
[289] FIRRTL:196052 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.dis_col_sel, req.bits.uop.dis_col_sel
[290] FIRRTL:196053 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_p3_bypass_hint, req.bits.uop.iw_p3_bypass_hint
[291] FIRRTL:196054 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_p2_bypass_hint, req.bits.uop.iw_p2_bypass_hint
[292] FIRRTL:196055 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_p1_bypass_hint, req.bits.uop.iw_p1_bypass_hint
[293] FIRRTL:196056 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_p2_speculative_child, req.bits.uop.iw_p2_speculative_child
[294] FIRRTL:196057 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_p1_speculative_child, req.bits.uop.iw_p1_speculative_child
[295] FIRRTL:196058 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_issued_partial_dgen, req.bits.uop.iw_issued_partial_dgen
[296] FIRRTL:196059 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_issued_partial_agen, req.bits.uop.iw_issued_partial_agen
[297] FIRRTL:196060 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iw_issued, req.bits.uop.iw_issued
[298] FIRRTL:196061 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[0], req.bits.uop.fu_code[0]
[299] FIRRTL:196062 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[1], req.bits.uop.fu_code[1]
[300] FIRRTL:196063 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[2], req.bits.uop.fu_code[2]
[301] FIRRTL:196064 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[3], req.bits.uop.fu_code[3]
[302] FIRRTL:196065 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[4], req.bits.uop.fu_code[4]
[303] FIRRTL:196066 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[5], req.bits.uop.fu_code[5]
[304] FIRRTL:196067 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[6], req.bits.uop.fu_code[6]
[305] FIRRTL:196068 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[7], req.bits.uop.fu_code[7]
[306] FIRRTL:196069 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[8], req.bits.uop.fu_code[8]
[307] FIRRTL:196070 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.fu_code[9], req.bits.uop.fu_code[9]
[308] FIRRTL:196071 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iq_type[0], req.bits.uop.iq_type[0]
[309] FIRRTL:196072 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iq_type[1], req.bits.uop.iq_type[1]
[310] FIRRTL:196073 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iq_type[2], req.bits.uop.iq_type[2]
[311] FIRRTL:196074 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.iq_type[3], req.bits.uop.iq_type[3]
[312] FIRRTL:196075 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.debug_pc, req.bits.uop.debug_pc
[313] FIRRTL:196076 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.is_rvc, req.bits.uop.is_rvc
[314] FIRRTL:196077 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.debug_inst, req.bits.uop.debug_inst
[315] FIRRTL:196078 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_0.io.req.uop.inst, req.bits.uop.inst
[316] FIRRTL:196079 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:621:26 KIND:connect :: connect mshrs_0.io.req_is_probe, io.req_is_probe[0]
[317] FIRRTL:196080 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:622:26 KIND:connect :: connect mshrs_0.io.req.sdq_id, sdq_alloc_id
[318] FIRRTL:196081 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:49 KIND:node :: node _mshr_io_clear_prefetch_T = eq(req.valid, UInt<1>(0h0))
[319] FIRRTL:196082 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:46 KIND:node :: node _mshr_io_clear_prefetch_T_1 = and(io.clear_all, _mshr_io_clear_prefetch_T)
[320] FIRRTL:196083 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:18 KIND:node :: node _mshr_io_clear_prefetch_T_2 = and(req.valid, idx_matches[0][0])
[321] FIRRTL:196084 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:45 KIND:node :: node _mshr_io_clear_prefetch_T_3 = and(_mshr_io_clear_prefetch_T_2, cacheable)
[322] FIRRTL:196085 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:61 KIND:node :: node _mshr_io_clear_prefetch_T_4 = eq(tag_match[0], UInt<1>(0h0))
[323] FIRRTL:196086 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:58 KIND:node :: node _mshr_io_clear_prefetch_T_5 = and(_mshr_io_clear_prefetch_T_3, _mshr_io_clear_prefetch_T_4)
[324] FIRRTL:196087 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:60 KIND:node :: node _mshr_io_clear_prefetch_T_6 = or(_mshr_io_clear_prefetch_T_1, _mshr_io_clear_prefetch_T_5)
[325] FIRRTL:196088 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:628:21 KIND:node :: node _mshr_io_clear_prefetch_T_7 = and(io.req_is_probe[0], idx_matches[0][0])
[326] FIRRTL:196089 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:82 KIND:node :: node _mshr_io_clear_prefetch_T_8 = or(_mshr_io_clear_prefetch_T_6, _mshr_io_clear_prefetch_T_7)
[327] FIRRTL:196090 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:28 KIND:connect :: connect mshrs_0.io.clear_prefetch, _mshr_io_clear_prefetch_T_8
[328] FIRRTL:196091 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.target_offset, io.brupdate.b2.target_offset
[329] FIRRTL:196092 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.jalr_target, io.brupdate.b2.jalr_target
[330] FIRRTL:196093 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.pc_sel, io.brupdate.b2.pc_sel
[331] FIRRTL:196094 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.cfi_type, io.brupdate.b2.cfi_type
[332] FIRRTL:196095 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.taken, io.brupdate.b2.taken
[333] FIRRTL:196096 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.mispredict, io.brupdate.b2.mispredict
[334] FIRRTL:196097 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.debug_tsrc, io.brupdate.b2.uop.debug_tsrc
[335] FIRRTL:196098 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.debug_fsrc, io.brupdate.b2.uop.debug_fsrc
[336] FIRRTL:196099 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.bp_xcpt_if, io.brupdate.b2.uop.bp_xcpt_if
[337] FIRRTL:196100 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.bp_debug_if, io.brupdate.b2.uop.bp_debug_if
[338] FIRRTL:196101 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.xcpt_ma_if, io.brupdate.b2.uop.xcpt_ma_if
[339] FIRRTL:196102 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.xcpt_ae_if, io.brupdate.b2.uop.xcpt_ae_if
[340] FIRRTL:196103 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.xcpt_pf_if, io.brupdate.b2.uop.xcpt_pf_if
[341] FIRRTL:196104 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_typ, io.brupdate.b2.uop.fp_typ
[342] FIRRTL:196105 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_rm, io.brupdate.b2.uop.fp_rm
[343] FIRRTL:196106 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_val, io.brupdate.b2.uop.fp_val
[344] FIRRTL:196107 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fcn_op, io.brupdate.b2.uop.fcn_op
[345] FIRRTL:196108 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fcn_dw, io.brupdate.b2.uop.fcn_dw
[346] FIRRTL:196109 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.frs3_en, io.brupdate.b2.uop.frs3_en
[347] FIRRTL:196110 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.lrs2_rtype, io.brupdate.b2.uop.lrs2_rtype
[348] FIRRTL:196111 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.lrs1_rtype, io.brupdate.b2.uop.lrs1_rtype
[349] FIRRTL:196112 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.dst_rtype, io.brupdate.b2.uop.dst_rtype
[350] FIRRTL:196113 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.lrs3, io.brupdate.b2.uop.lrs3
[351] FIRRTL:196114 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.lrs2, io.brupdate.b2.uop.lrs2
[352] FIRRTL:196115 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.lrs1, io.brupdate.b2.uop.lrs1
[353] FIRRTL:196116 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ldst, io.brupdate.b2.uop.ldst
[354] FIRRTL:196117 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ldst_is_rs1, io.brupdate.b2.uop.ldst_is_rs1
[355] FIRRTL:196118 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.csr_cmd, io.brupdate.b2.uop.csr_cmd
[356] FIRRTL:196119 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.flush_on_commit, io.brupdate.b2.uop.flush_on_commit
[357] FIRRTL:196120 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_unique, io.brupdate.b2.uop.is_unique
[358] FIRRTL:196121 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.uses_stq, io.brupdate.b2.uop.uses_stq
[359] FIRRTL:196122 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.uses_ldq, io.brupdate.b2.uop.uses_ldq
[360] FIRRTL:196123 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.mem_signed, io.brupdate.b2.uop.mem_signed
[361] FIRRTL:196124 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.mem_size, io.brupdate.b2.uop.mem_size
[362] FIRRTL:196125 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.mem_cmd, io.brupdate.b2.uop.mem_cmd
[363] FIRRTL:196126 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.exc_cause, io.brupdate.b2.uop.exc_cause
[364] FIRRTL:196127 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.exception, io.brupdate.b2.uop.exception
[365] FIRRTL:196128 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.stale_pdst, io.brupdate.b2.uop.stale_pdst
[366] FIRRTL:196129 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ppred_busy, io.brupdate.b2.uop.ppred_busy
[367] FIRRTL:196130 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs3_busy, io.brupdate.b2.uop.prs3_busy
[368] FIRRTL:196131 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs2_busy, io.brupdate.b2.uop.prs2_busy
[369] FIRRTL:196132 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs1_busy, io.brupdate.b2.uop.prs1_busy
[370] FIRRTL:196133 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ppred, io.brupdate.b2.uop.ppred
[371] FIRRTL:196134 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs3, io.brupdate.b2.uop.prs3
[372] FIRRTL:196135 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs2, io.brupdate.b2.uop.prs2
[373] FIRRTL:196136 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.prs1, io.brupdate.b2.uop.prs1
[374] FIRRTL:196137 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.pdst, io.brupdate.b2.uop.pdst
[375] FIRRTL:196138 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.rxq_idx, io.brupdate.b2.uop.rxq_idx
[376] FIRRTL:196139 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.stq_idx, io.brupdate.b2.uop.stq_idx
[377] FIRRTL:196140 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ldq_idx, io.brupdate.b2.uop.ldq_idx
[378] FIRRTL:196141 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.rob_idx, io.brupdate.b2.uop.rob_idx
[379] FIRRTL:196142 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.vec, io.brupdate.b2.uop.fp_ctrl.vec
[380] FIRRTL:196143 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.wflags, io.brupdate.b2.uop.fp_ctrl.wflags
[381] FIRRTL:196144 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.sqrt, io.brupdate.b2.uop.fp_ctrl.sqrt
[382] FIRRTL:196145 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.div, io.brupdate.b2.uop.fp_ctrl.div
[383] FIRRTL:196146 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.fma, io.brupdate.b2.uop.fp_ctrl.fma
[384] FIRRTL:196147 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.brupdate.b2.uop.fp_ctrl.fastpipe
[385] FIRRTL:196148 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.toint, io.brupdate.b2.uop.fp_ctrl.toint
[386] FIRRTL:196149 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.fromint, io.brupdate.b2.uop.fp_ctrl.fromint
[387] FIRRTL:196150 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.brupdate.b2.uop.fp_ctrl.typeTagOut
[388] FIRRTL:196151 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.brupdate.b2.uop.fp_ctrl.typeTagIn
[389] FIRRTL:196152 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap23, io.brupdate.b2.uop.fp_ctrl.swap23
[390] FIRRTL:196153 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.swap12, io.brupdate.b2.uop.fp_ctrl.swap12
[391] FIRRTL:196154 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren3, io.brupdate.b2.uop.fp_ctrl.ren3
[392] FIRRTL:196155 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren2, io.brupdate.b2.uop.fp_ctrl.ren2
[393] FIRRTL:196156 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.ren1, io.brupdate.b2.uop.fp_ctrl.ren1
[394] FIRRTL:196157 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.wen, io.brupdate.b2.uop.fp_ctrl.wen
[395] FIRRTL:196158 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fp_ctrl.ldst, io.brupdate.b2.uop.fp_ctrl.ldst
[396] FIRRTL:196159 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.op2_sel, io.brupdate.b2.uop.op2_sel
[397] FIRRTL:196160 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.op1_sel, io.brupdate.b2.uop.op1_sel
[398] FIRRTL:196161 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.imm_packed, io.brupdate.b2.uop.imm_packed
[399] FIRRTL:196162 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.pimm, io.brupdate.b2.uop.pimm
[400] FIRRTL:196163 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.imm_sel, io.brupdate.b2.uop.imm_sel
[401] FIRRTL:196164 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.imm_rename, io.brupdate.b2.uop.imm_rename
[402] FIRRTL:196165 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.taken, io.brupdate.b2.uop.taken
[403] FIRRTL:196166 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.pc_lob, io.brupdate.b2.uop.pc_lob
[404] FIRRTL:196167 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.edge_inst, io.brupdate.b2.uop.edge_inst
[405] FIRRTL:196168 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.ftq_idx, io.brupdate.b2.uop.ftq_idx
[406] FIRRTL:196169 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_mov, io.brupdate.b2.uop.is_mov
[407] FIRRTL:196170 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_rocc, io.brupdate.b2.uop.is_rocc
[408] FIRRTL:196171 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_sys_pc2epc, io.brupdate.b2.uop.is_sys_pc2epc
[409] FIRRTL:196172 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_eret, io.brupdate.b2.uop.is_eret
[410] FIRRTL:196173 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_amo, io.brupdate.b2.uop.is_amo
[411] FIRRTL:196174 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_sfence, io.brupdate.b2.uop.is_sfence
[412] FIRRTL:196175 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_fencei, io.brupdate.b2.uop.is_fencei
[413] FIRRTL:196176 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_fence, io.brupdate.b2.uop.is_fence
[414] FIRRTL:196177 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_sfb, io.brupdate.b2.uop.is_sfb
[415] FIRRTL:196178 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.br_type, io.brupdate.b2.uop.br_type
[416] FIRRTL:196179 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.br_tag, io.brupdate.b2.uop.br_tag
[417] FIRRTL:196180 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.br_mask, io.brupdate.b2.uop.br_mask
[418] FIRRTL:196181 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.dis_col_sel, io.brupdate.b2.uop.dis_col_sel
[419] FIRRTL:196182 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_p3_bypass_hint, io.brupdate.b2.uop.iw_p3_bypass_hint
[420] FIRRTL:196183 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_p2_bypass_hint, io.brupdate.b2.uop.iw_p2_bypass_hint
[421] FIRRTL:196184 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_p1_bypass_hint, io.brupdate.b2.uop.iw_p1_bypass_hint
[422] FIRRTL:196185 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_p2_speculative_child, io.brupdate.b2.uop.iw_p2_speculative_child
[423] FIRRTL:196186 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_p1_speculative_child, io.brupdate.b2.uop.iw_p1_speculative_child
[424] FIRRTL:196187 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_issued_partial_dgen, io.brupdate.b2.uop.iw_issued_partial_dgen
[425] FIRRTL:196188 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_issued_partial_agen, io.brupdate.b2.uop.iw_issued_partial_agen
[426] FIRRTL:196189 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iw_issued, io.brupdate.b2.uop.iw_issued
[427] FIRRTL:196190 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[0], io.brupdate.b2.uop.fu_code[0]
[428] FIRRTL:196191 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[1], io.brupdate.b2.uop.fu_code[1]
[429] FIRRTL:196192 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[2], io.brupdate.b2.uop.fu_code[2]
[430] FIRRTL:196193 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[3], io.brupdate.b2.uop.fu_code[3]
[431] FIRRTL:196194 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[4], io.brupdate.b2.uop.fu_code[4]
[432] FIRRTL:196195 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[5], io.brupdate.b2.uop.fu_code[5]
[433] FIRRTL:196196 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[6], io.brupdate.b2.uop.fu_code[6]
[434] FIRRTL:196197 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[7], io.brupdate.b2.uop.fu_code[7]
[435] FIRRTL:196198 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[8], io.brupdate.b2.uop.fu_code[8]
[436] FIRRTL:196199 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.fu_code[9], io.brupdate.b2.uop.fu_code[9]
[437] FIRRTL:196200 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iq_type[0], io.brupdate.b2.uop.iq_type[0]
[438] FIRRTL:196201 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iq_type[1], io.brupdate.b2.uop.iq_type[1]
[439] FIRRTL:196202 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iq_type[2], io.brupdate.b2.uop.iq_type[2]
[440] FIRRTL:196203 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.iq_type[3], io.brupdate.b2.uop.iq_type[3]
[441] FIRRTL:196204 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.debug_pc, io.brupdate.b2.uop.debug_pc
[442] FIRRTL:196205 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.is_rvc, io.brupdate.b2.uop.is_rvc
[443] FIRRTL:196206 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.debug_inst, io.brupdate.b2.uop.debug_inst
[444] FIRRTL:196207 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b2.uop.inst, io.brupdate.b2.uop.inst
[445] FIRRTL:196208 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b1.mispredict_mask, io.brupdate.b1.mispredict_mask
[446] FIRRTL:196209 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_0.io.brupdate.b1.resolve_mask, io.brupdate.b1.resolve_mask
[447] FIRRTL:196210 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:630:26 KIND:connect :: connect mshrs_0.io.exception, io.exception
[448] FIRRTL:196211 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:631:26 KIND:connect :: connect mshrs_0.io.rob_pnr_idx, io.rob_pnr_idx
[449] FIRRTL:196212 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:632:26 KIND:connect :: connect mshrs_0.io.rob_head_idx, io.rob_head_idx
[450] FIRRTL:196213 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:634:26 KIND:connect :: connect mshrs_0.io.prober_state.bits, io.prober_state.bits
[451] FIRRTL:196214 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:634:26 KIND:connect :: connect mshrs_0.io.prober_state.valid, io.prober_state.valid
[452] FIRRTL:196215 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:636:26 KIND:connect :: connect mshrs_0.io.wb_resp, io.wb_resp
[453] FIRRTL:196216 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:638:29 KIND:connect :: connect meta_write_arb.io.in[0], mshrs_0.io.meta_write
[454] FIRRTL:196217 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:639:29 KIND:connect :: connect meta_read_arb.io.in[0], mshrs_0.io.meta_read
[455] FIRRTL:196218 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_0.io.meta_resp.bits.tag, io.meta_resp.bits.tag
[456] FIRRTL:196219 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_0.io.meta_resp.bits.coh.state, io.meta_resp.bits.coh.state
[457] FIRRTL:196220 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_0.io.meta_resp.valid, io.meta_resp.valid
[458] FIRRTL:196221 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:641:29 KIND:connect :: connect wb_req_arb.io.in[0], mshrs_0.io.wb_req
[459] FIRRTL:196222 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:642:29 KIND:connect :: connect replay_arb.io.in[0], mshrs_0.io.replay
[460] FIRRTL:196223 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:643:29 KIND:connect :: connect refill_arb.io.in[0], mshrs_0.io.refill
[461] FIRRTL:196224 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:645:32 KIND:connect :: connect mshrs_0.io.lb_resp, lb[0][mshrs_0.io.lb_read.offset]
[462] FIRRTL:196225 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:646:35 KIND:when :: when mshrs_0.io.lb_write.valid :
[463] FIRRTL:196226 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:647:43 KIND:connect :: connect lb[0][mshrs_0.io.lb_write.bits.offset], mshrs_0.io.lb_write.bits.data
[464] FIRRTL:196227 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:650:21 KIND:connect :: connect commit_vals[0], mshrs_0.io.commit_val
[465] FIRRTL:196228 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:651:21 KIND:connect :: connect commit_addrs[0], mshrs_0.io.commit_addr
[466] FIRRTL:196229 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:652:21 KIND:connect :: connect commit_cohs[0], mshrs_0.io.commit_coh
[467] FIRRTL:196230 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:654:29 KIND:connect :: connect mshrs_0.io.mem_grant.valid, UInt<1>(0h0)
[468] FIRRTL:196231 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.corrupt
[469] FIRRTL:196232 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.data
[470] FIRRTL:196233 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.denied
[471] FIRRTL:196234 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.sink
[472] FIRRTL:196235 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.source
[473] FIRRTL:196236 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.size
[474] FIRRTL:196237 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.param
[475] FIRRTL:196238 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_0.io.mem_grant.bits.opcode
[476] FIRRTL:196239 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:656:36 KIND:node :: node _T_1 = eq(io.mem_grant.bits.source, UInt<1>(0h0))
[477] FIRRTL:196240 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:656:45 KIND:when :: when _T_1 :
[478] FIRRTL:196241 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:657:25 KIND:connect :: connect mshrs_0.io.mem_grant, io.mem_grant
[479] FIRRTL:196242 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:660:49 KIND:node :: node _T_2 = and(mshrs_0.io.req_sec_rdy, mshrs_0.io.req_sec_val)
[480] FIRRTL:196243 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:660:25 KIND:node :: node _T_3 = or(UInt<1>(0h0), _T_2)
[481] FIRRTL:196244 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:661:23 KIND:connect :: connect resp_arb.io.in[0], mshrs_0.io.resp
[482] FIRRTL:196245 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:663:11 KIND:node :: node _T_4 = eq(mshrs_0.io.req_pri_rdy, UInt<1>(0h0))
[483] FIRRTL:196246 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:663:33 KIND:when :: when _T_4 :
[484] FIRRTL:196247 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:664:20 KIND:connect :: connect io.fence_rdy, UInt<1>(0h0)
[485] FIRRTL:196248 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:13 KIND:node :: node _T_5 = eq(mshrs_0.io.probe_rdy, UInt<1>(0h0))
[486] FIRRTL:196249 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:32 KIND:node :: node _T_6 = and(_T_5, idx_matches[0][0])
[487] FIRRTL:196250 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:53 KIND:node :: node _T_7 = and(_T_6, io.req_is_probe[0])
[488] FIRRTL:196251 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:76 KIND:when :: when _T_7 :
[489] FIRRTL:196252 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:668:22 KIND:connect :: connect io.probe_rdy, UInt<1>(0h0)
[490] FIRRTL:196253 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:602:22 KIND:structural :: inst mshrs_1 of BoomMSHR_1
[491] FIRRTL:196254 SRC:<no-source-locator> KIND:connect :: connect mshrs_1.clock, clock
[492] FIRRTL:196255 SRC:<no-source-locator> KIND:connect :: connect mshrs_1.reset, reset
[493] FIRRTL:196256 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:603:16 KIND:connect :: connect mshrs_1.io.id, UInt<1>(0h1)
[494] FIRRTL:196257 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:89 KIND:node :: node _idx_matches_0_1_T = bits(io.req[0].bits.addr, 11, 6)
[495] FIRRTL:196258 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:66 KIND:node :: node _idx_matches_0_1_T_1 = eq(mshrs_1.io.idx.bits, _idx_matches_0_1_T)
[496] FIRRTL:196259 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:46 KIND:node :: node _idx_matches_0_1_T_2 = and(mshrs_1.io.idx.valid, _idx_matches_0_1_T_1)
[497] FIRRTL:196260 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:606:25 KIND:connect :: connect idx_matches[0][1], _idx_matches_0_1_T_2
[498] FIRRTL:196261 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:90 KIND:node :: node _tag_matches_0_1_T = shr(io.req[0].bits.addr, 12)
[499] FIRRTL:196262 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:66 KIND:node :: node _tag_matches_0_1_T_1 = eq(mshrs_1.io.tag.bits, _tag_matches_0_1_T)
[500] FIRRTL:196263 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:46 KIND:node :: node _tag_matches_0_1_T_2 = and(mshrs_1.io.tag.valid, _tag_matches_0_1_T_1)
[501] FIRRTL:196264 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:607:25 KIND:connect :: connect tag_matches[0][1], _tag_matches_0_1_T_2
[502] FIRRTL:196265 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:66 KIND:node :: node _way_matches_0_1_T = eq(mshrs_1.io.way.bits, io.req[0].bits.way_en)
[503] FIRRTL:196266 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:46 KIND:node :: node _way_matches_0_1_T_1 = and(mshrs_1.io.way.valid, _way_matches_0_1_T)
[504] FIRRTL:196267 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:608:25 KIND:connect :: connect way_matches[0][1], _way_matches_0_1_T_1
[505] FIRRTL:196268 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:610:20 KIND:connect :: connect wb_tag_list[1], mshrs_1.io.wb_req.bits.tag
[506] FIRRTL:196269 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:34 KIND:node :: node _mshr_io_req_pri_val_T_2 = eq(UInt<1>(0h1), mshr_alloc_idx)
[507] FIRRTL:196270 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:54 KIND:node :: node _mshr_io_req_pri_val_T_3 = and(_mshr_io_req_pri_val_T_2, pri_val)
[508] FIRRTL:196271 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:614:26 KIND:connect :: connect mshrs_1.io.req_pri_val, _mshr_io_req_pri_val_T_3
[509] FIRRTL:196272 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:615:15 KIND:node :: node _T_8 = eq(UInt<1>(0h1), mshr_alloc_idx)
[510] FIRRTL:196273 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:615:35 KIND:when :: when _T_8 :
[511] FIRRTL:196274 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:616:15 KIND:connect :: connect pri_rdy, mshrs_1.io.req_pri_rdy
[512] FIRRTL:196275 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:39 KIND:node :: node _mshr_io_req_sec_val_T_4 = and(req.valid, sdq_rdy)
[513] FIRRTL:196276 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:50 KIND:node :: node _mshr_io_req_sec_val_T_5 = and(_mshr_io_req_sec_val_T_4, tag_match[0])
[514] FIRRTL:196277 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:72 KIND:node :: node _mshr_io_req_sec_val_T_6 = and(_mshr_io_req_sec_val_T_5, idx_matches[0][1])
[515] FIRRTL:196278 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:99 KIND:node :: node _mshr_io_req_sec_val_T_7 = and(_mshr_io_req_sec_val_T_6, cacheable)
[516] FIRRTL:196279 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:619:26 KIND:connect :: connect mshrs_1.io.req_sec_val, _mshr_io_req_sec_val_T_7
[517] FIRRTL:196280 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.sdq_id, req.bits.sdq_id
[518] FIRRTL:196281 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.way_en, req.bits.way_en
[519] FIRRTL:196282 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.old_meta.tag, req.bits.old_meta.tag
[520] FIRRTL:196283 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.old_meta.coh.state, req.bits.old_meta.coh.state
[521] FIRRTL:196284 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.tag_match, req.bits.tag_match
[522] FIRRTL:196285 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.is_hella, req.bits.is_hella
[523] FIRRTL:196286 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.data, req.bits.data
[524] FIRRTL:196287 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.addr, req.bits.addr
[525] FIRRTL:196288 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.debug_tsrc, req.bits.uop.debug_tsrc
[526] FIRRTL:196289 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.debug_fsrc, req.bits.uop.debug_fsrc
[527] FIRRTL:196290 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.bp_xcpt_if, req.bits.uop.bp_xcpt_if
[528] FIRRTL:196291 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.bp_debug_if, req.bits.uop.bp_debug_if
[529] FIRRTL:196292 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.xcpt_ma_if, req.bits.uop.xcpt_ma_if
[530] FIRRTL:196293 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.xcpt_ae_if, req.bits.uop.xcpt_ae_if
[531] FIRRTL:196294 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.xcpt_pf_if, req.bits.uop.xcpt_pf_if
[532] FIRRTL:196295 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_typ, req.bits.uop.fp_typ
[533] FIRRTL:196296 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_rm, req.bits.uop.fp_rm
[534] FIRRTL:196297 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_val, req.bits.uop.fp_val
[535] FIRRTL:196298 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fcn_op, req.bits.uop.fcn_op
[536] FIRRTL:196299 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fcn_dw, req.bits.uop.fcn_dw
[537] FIRRTL:196300 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.frs3_en, req.bits.uop.frs3_en
[538] FIRRTL:196301 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.lrs2_rtype, req.bits.uop.lrs2_rtype
[539] FIRRTL:196302 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.lrs1_rtype, req.bits.uop.lrs1_rtype
[540] FIRRTL:196303 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.dst_rtype, req.bits.uop.dst_rtype
[541] FIRRTL:196304 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.lrs3, req.bits.uop.lrs3
[542] FIRRTL:196305 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.lrs2, req.bits.uop.lrs2
[543] FIRRTL:196306 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.lrs1, req.bits.uop.lrs1
[544] FIRRTL:196307 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ldst, req.bits.uop.ldst
[545] FIRRTL:196308 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ldst_is_rs1, req.bits.uop.ldst_is_rs1
[546] FIRRTL:196309 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.csr_cmd, req.bits.uop.csr_cmd
[547] FIRRTL:196310 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.flush_on_commit, req.bits.uop.flush_on_commit
[548] FIRRTL:196311 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_unique, req.bits.uop.is_unique
[549] FIRRTL:196312 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.uses_stq, req.bits.uop.uses_stq
[550] FIRRTL:196313 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.uses_ldq, req.bits.uop.uses_ldq
[551] FIRRTL:196314 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.mem_signed, req.bits.uop.mem_signed
[552] FIRRTL:196315 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.mem_size, req.bits.uop.mem_size
[553] FIRRTL:196316 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.mem_cmd, req.bits.uop.mem_cmd
[554] FIRRTL:196317 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.exc_cause, req.bits.uop.exc_cause
[555] FIRRTL:196318 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.exception, req.bits.uop.exception
[556] FIRRTL:196319 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.stale_pdst, req.bits.uop.stale_pdst
[557] FIRRTL:196320 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ppred_busy, req.bits.uop.ppred_busy
[558] FIRRTL:196321 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs3_busy, req.bits.uop.prs3_busy
[559] FIRRTL:196322 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs2_busy, req.bits.uop.prs2_busy
[560] FIRRTL:196323 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs1_busy, req.bits.uop.prs1_busy
[561] FIRRTL:196324 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ppred, req.bits.uop.ppred
[562] FIRRTL:196325 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs3, req.bits.uop.prs3
[563] FIRRTL:196326 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs2, req.bits.uop.prs2
[564] FIRRTL:196327 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.prs1, req.bits.uop.prs1
[565] FIRRTL:196328 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.pdst, req.bits.uop.pdst
[566] FIRRTL:196329 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.rxq_idx, req.bits.uop.rxq_idx
[567] FIRRTL:196330 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.stq_idx, req.bits.uop.stq_idx
[568] FIRRTL:196331 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ldq_idx, req.bits.uop.ldq_idx
[569] FIRRTL:196332 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.rob_idx, req.bits.uop.rob_idx
[570] FIRRTL:196333 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.vec, req.bits.uop.fp_ctrl.vec
[571] FIRRTL:196334 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.wflags, req.bits.uop.fp_ctrl.wflags
[572] FIRRTL:196335 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.sqrt, req.bits.uop.fp_ctrl.sqrt
[573] FIRRTL:196336 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.div, req.bits.uop.fp_ctrl.div
[574] FIRRTL:196337 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.fma, req.bits.uop.fp_ctrl.fma
[575] FIRRTL:196338 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.fastpipe, req.bits.uop.fp_ctrl.fastpipe
[576] FIRRTL:196339 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.toint, req.bits.uop.fp_ctrl.toint
[577] FIRRTL:196340 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.fromint, req.bits.uop.fp_ctrl.fromint
[578] FIRRTL:196341 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.typeTagOut, req.bits.uop.fp_ctrl.typeTagOut
[579] FIRRTL:196342 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.typeTagIn, req.bits.uop.fp_ctrl.typeTagIn
[580] FIRRTL:196343 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.swap23, req.bits.uop.fp_ctrl.swap23
[581] FIRRTL:196344 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.swap12, req.bits.uop.fp_ctrl.swap12
[582] FIRRTL:196345 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.ren3, req.bits.uop.fp_ctrl.ren3
[583] FIRRTL:196346 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.ren2, req.bits.uop.fp_ctrl.ren2
[584] FIRRTL:196347 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.ren1, req.bits.uop.fp_ctrl.ren1
[585] FIRRTL:196348 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.wen, req.bits.uop.fp_ctrl.wen
[586] FIRRTL:196349 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fp_ctrl.ldst, req.bits.uop.fp_ctrl.ldst
[587] FIRRTL:196350 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.op2_sel, req.bits.uop.op2_sel
[588] FIRRTL:196351 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.op1_sel, req.bits.uop.op1_sel
[589] FIRRTL:196352 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.imm_packed, req.bits.uop.imm_packed
[590] FIRRTL:196353 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.pimm, req.bits.uop.pimm
[591] FIRRTL:196354 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.imm_sel, req.bits.uop.imm_sel
[592] FIRRTL:196355 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.imm_rename, req.bits.uop.imm_rename
[593] FIRRTL:196356 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.taken, req.bits.uop.taken
[594] FIRRTL:196357 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.pc_lob, req.bits.uop.pc_lob
[595] FIRRTL:196358 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.edge_inst, req.bits.uop.edge_inst
[596] FIRRTL:196359 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.ftq_idx, req.bits.uop.ftq_idx
[597] FIRRTL:196360 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_mov, req.bits.uop.is_mov
[598] FIRRTL:196361 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_rocc, req.bits.uop.is_rocc
[599] FIRRTL:196362 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_sys_pc2epc, req.bits.uop.is_sys_pc2epc
[600] FIRRTL:196363 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_eret, req.bits.uop.is_eret
[601] FIRRTL:196364 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_amo, req.bits.uop.is_amo
[602] FIRRTL:196365 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_sfence, req.bits.uop.is_sfence
[603] FIRRTL:196366 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_fencei, req.bits.uop.is_fencei
[604] FIRRTL:196367 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_fence, req.bits.uop.is_fence
[605] FIRRTL:196368 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_sfb, req.bits.uop.is_sfb
[606] FIRRTL:196369 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.br_type, req.bits.uop.br_type
[607] FIRRTL:196370 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.br_tag, req.bits.uop.br_tag
[608] FIRRTL:196371 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.br_mask, req.bits.uop.br_mask
[609] FIRRTL:196372 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.dis_col_sel, req.bits.uop.dis_col_sel
[610] FIRRTL:196373 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_p3_bypass_hint, req.bits.uop.iw_p3_bypass_hint
[611] FIRRTL:196374 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_p2_bypass_hint, req.bits.uop.iw_p2_bypass_hint
[612] FIRRTL:196375 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_p1_bypass_hint, req.bits.uop.iw_p1_bypass_hint
[613] FIRRTL:196376 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_p2_speculative_child, req.bits.uop.iw_p2_speculative_child
[614] FIRRTL:196377 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_p1_speculative_child, req.bits.uop.iw_p1_speculative_child
[615] FIRRTL:196378 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_issued_partial_dgen, req.bits.uop.iw_issued_partial_dgen
[616] FIRRTL:196379 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_issued_partial_agen, req.bits.uop.iw_issued_partial_agen
[617] FIRRTL:196380 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iw_issued, req.bits.uop.iw_issued
[618] FIRRTL:196381 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[0], req.bits.uop.fu_code[0]
[619] FIRRTL:196382 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[1], req.bits.uop.fu_code[1]
[620] FIRRTL:196383 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[2], req.bits.uop.fu_code[2]
[621] FIRRTL:196384 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[3], req.bits.uop.fu_code[3]
[622] FIRRTL:196385 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[4], req.bits.uop.fu_code[4]
[623] FIRRTL:196386 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[5], req.bits.uop.fu_code[5]
[624] FIRRTL:196387 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[6], req.bits.uop.fu_code[6]
[625] FIRRTL:196388 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[7], req.bits.uop.fu_code[7]
[626] FIRRTL:196389 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[8], req.bits.uop.fu_code[8]
[627] FIRRTL:196390 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.fu_code[9], req.bits.uop.fu_code[9]
[628] FIRRTL:196391 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iq_type[0], req.bits.uop.iq_type[0]
[629] FIRRTL:196392 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iq_type[1], req.bits.uop.iq_type[1]
[630] FIRRTL:196393 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iq_type[2], req.bits.uop.iq_type[2]
[631] FIRRTL:196394 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.iq_type[3], req.bits.uop.iq_type[3]
[632] FIRRTL:196395 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.debug_pc, req.bits.uop.debug_pc
[633] FIRRTL:196396 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.is_rvc, req.bits.uop.is_rvc
[634] FIRRTL:196397 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.debug_inst, req.bits.uop.debug_inst
[635] FIRRTL:196398 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:620:26 KIND:connect :: connect mshrs_1.io.req.uop.inst, req.bits.uop.inst
[636] FIRRTL:196399 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:621:26 KIND:connect :: connect mshrs_1.io.req_is_probe, io.req_is_probe[0]
[637] FIRRTL:196400 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:622:26 KIND:connect :: connect mshrs_1.io.req.sdq_id, sdq_alloc_id
[638] FIRRTL:196401 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:49 KIND:node :: node _mshr_io_clear_prefetch_T_9 = eq(req.valid, UInt<1>(0h0))
[639] FIRRTL:196402 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:46 KIND:node :: node _mshr_io_clear_prefetch_T_10 = and(io.clear_all, _mshr_io_clear_prefetch_T_9)
[640] FIRRTL:196403 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:18 KIND:node :: node _mshr_io_clear_prefetch_T_11 = and(req.valid, idx_matches[0][1])
[641] FIRRTL:196404 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:45 KIND:node :: node _mshr_io_clear_prefetch_T_12 = and(_mshr_io_clear_prefetch_T_11, cacheable)
[642] FIRRTL:196405 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:61 KIND:node :: node _mshr_io_clear_prefetch_T_13 = eq(tag_match[0], UInt<1>(0h0))
[643] FIRRTL:196406 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:58 KIND:node :: node _mshr_io_clear_prefetch_T_14 = and(_mshr_io_clear_prefetch_T_12, _mshr_io_clear_prefetch_T_13)
[644] FIRRTL:196407 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:60 KIND:node :: node _mshr_io_clear_prefetch_T_15 = or(_mshr_io_clear_prefetch_T_10, _mshr_io_clear_prefetch_T_14)
[645] FIRRTL:196408 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:628:21 KIND:node :: node _mshr_io_clear_prefetch_T_16 = and(io.req_is_probe[0], idx_matches[0][1])
[646] FIRRTL:196409 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:627:82 KIND:node :: node _mshr_io_clear_prefetch_T_17 = or(_mshr_io_clear_prefetch_T_15, _mshr_io_clear_prefetch_T_16)
[647] FIRRTL:196410 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:626:28 KIND:connect :: connect mshrs_1.io.clear_prefetch, _mshr_io_clear_prefetch_T_17
[648] FIRRTL:196411 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.target_offset, io.brupdate.b2.target_offset
[649] FIRRTL:196412 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.jalr_target, io.brupdate.b2.jalr_target
[650] FIRRTL:196413 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.pc_sel, io.brupdate.b2.pc_sel
[651] FIRRTL:196414 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.cfi_type, io.brupdate.b2.cfi_type
[652] FIRRTL:196415 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.taken, io.brupdate.b2.taken
[653] FIRRTL:196416 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.mispredict, io.brupdate.b2.mispredict
[654] FIRRTL:196417 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.debug_tsrc, io.brupdate.b2.uop.debug_tsrc
[655] FIRRTL:196418 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.debug_fsrc, io.brupdate.b2.uop.debug_fsrc
[656] FIRRTL:196419 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.bp_xcpt_if, io.brupdate.b2.uop.bp_xcpt_if
[657] FIRRTL:196420 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.bp_debug_if, io.brupdate.b2.uop.bp_debug_if
[658] FIRRTL:196421 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.xcpt_ma_if, io.brupdate.b2.uop.xcpt_ma_if
[659] FIRRTL:196422 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.xcpt_ae_if, io.brupdate.b2.uop.xcpt_ae_if
[660] FIRRTL:196423 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.xcpt_pf_if, io.brupdate.b2.uop.xcpt_pf_if
[661] FIRRTL:196424 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_typ, io.brupdate.b2.uop.fp_typ
[662] FIRRTL:196425 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_rm, io.brupdate.b2.uop.fp_rm
[663] FIRRTL:196426 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_val, io.brupdate.b2.uop.fp_val
[664] FIRRTL:196427 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fcn_op, io.brupdate.b2.uop.fcn_op
[665] FIRRTL:196428 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fcn_dw, io.brupdate.b2.uop.fcn_dw
[666] FIRRTL:196429 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.frs3_en, io.brupdate.b2.uop.frs3_en
[667] FIRRTL:196430 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.lrs2_rtype, io.brupdate.b2.uop.lrs2_rtype
[668] FIRRTL:196431 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.lrs1_rtype, io.brupdate.b2.uop.lrs1_rtype
[669] FIRRTL:196432 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.dst_rtype, io.brupdate.b2.uop.dst_rtype
[670] FIRRTL:196433 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.lrs3, io.brupdate.b2.uop.lrs3
[671] FIRRTL:196434 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.lrs2, io.brupdate.b2.uop.lrs2
[672] FIRRTL:196435 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.lrs1, io.brupdate.b2.uop.lrs1
[673] FIRRTL:196436 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ldst, io.brupdate.b2.uop.ldst
[674] FIRRTL:196437 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ldst_is_rs1, io.brupdate.b2.uop.ldst_is_rs1
[675] FIRRTL:196438 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.csr_cmd, io.brupdate.b2.uop.csr_cmd
[676] FIRRTL:196439 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.flush_on_commit, io.brupdate.b2.uop.flush_on_commit
[677] FIRRTL:196440 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_unique, io.brupdate.b2.uop.is_unique
[678] FIRRTL:196441 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.uses_stq, io.brupdate.b2.uop.uses_stq
[679] FIRRTL:196442 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.uses_ldq, io.brupdate.b2.uop.uses_ldq
[680] FIRRTL:196443 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.mem_signed, io.brupdate.b2.uop.mem_signed
[681] FIRRTL:196444 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.mem_size, io.brupdate.b2.uop.mem_size
[682] FIRRTL:196445 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.mem_cmd, io.brupdate.b2.uop.mem_cmd
[683] FIRRTL:196446 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.exc_cause, io.brupdate.b2.uop.exc_cause
[684] FIRRTL:196447 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.exception, io.brupdate.b2.uop.exception
[685] FIRRTL:196448 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.stale_pdst, io.brupdate.b2.uop.stale_pdst
[686] FIRRTL:196449 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ppred_busy, io.brupdate.b2.uop.ppred_busy
[687] FIRRTL:196450 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs3_busy, io.brupdate.b2.uop.prs3_busy
[688] FIRRTL:196451 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs2_busy, io.brupdate.b2.uop.prs2_busy
[689] FIRRTL:196452 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs1_busy, io.brupdate.b2.uop.prs1_busy
[690] FIRRTL:196453 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ppred, io.brupdate.b2.uop.ppred
[691] FIRRTL:196454 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs3, io.brupdate.b2.uop.prs3
[692] FIRRTL:196455 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs2, io.brupdate.b2.uop.prs2
[693] FIRRTL:196456 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.prs1, io.brupdate.b2.uop.prs1
[694] FIRRTL:196457 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.pdst, io.brupdate.b2.uop.pdst
[695] FIRRTL:196458 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.rxq_idx, io.brupdate.b2.uop.rxq_idx
[696] FIRRTL:196459 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.stq_idx, io.brupdate.b2.uop.stq_idx
[697] FIRRTL:196460 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ldq_idx, io.brupdate.b2.uop.ldq_idx
[698] FIRRTL:196461 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.rob_idx, io.brupdate.b2.uop.rob_idx
[699] FIRRTL:196462 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.vec, io.brupdate.b2.uop.fp_ctrl.vec
[700] FIRRTL:196463 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.wflags, io.brupdate.b2.uop.fp_ctrl.wflags
[701] FIRRTL:196464 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.sqrt, io.brupdate.b2.uop.fp_ctrl.sqrt
[702] FIRRTL:196465 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.div, io.brupdate.b2.uop.fp_ctrl.div
[703] FIRRTL:196466 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.fma, io.brupdate.b2.uop.fp_ctrl.fma
[704] FIRRTL:196467 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.brupdate.b2.uop.fp_ctrl.fastpipe
[705] FIRRTL:196468 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.toint, io.brupdate.b2.uop.fp_ctrl.toint
[706] FIRRTL:196469 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.fromint, io.brupdate.b2.uop.fp_ctrl.fromint
[707] FIRRTL:196470 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.brupdate.b2.uop.fp_ctrl.typeTagOut
[708] FIRRTL:196471 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.brupdate.b2.uop.fp_ctrl.typeTagIn
[709] FIRRTL:196472 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap23, io.brupdate.b2.uop.fp_ctrl.swap23
[710] FIRRTL:196473 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.swap12, io.brupdate.b2.uop.fp_ctrl.swap12
[711] FIRRTL:196474 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren3, io.brupdate.b2.uop.fp_ctrl.ren3
[712] FIRRTL:196475 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren2, io.brupdate.b2.uop.fp_ctrl.ren2
[713] FIRRTL:196476 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.ren1, io.brupdate.b2.uop.fp_ctrl.ren1
[714] FIRRTL:196477 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.wen, io.brupdate.b2.uop.fp_ctrl.wen
[715] FIRRTL:196478 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fp_ctrl.ldst, io.brupdate.b2.uop.fp_ctrl.ldst
[716] FIRRTL:196479 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.op2_sel, io.brupdate.b2.uop.op2_sel
[717] FIRRTL:196480 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.op1_sel, io.brupdate.b2.uop.op1_sel
[718] FIRRTL:196481 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.imm_packed, io.brupdate.b2.uop.imm_packed
[719] FIRRTL:196482 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.pimm, io.brupdate.b2.uop.pimm
[720] FIRRTL:196483 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.imm_sel, io.brupdate.b2.uop.imm_sel
[721] FIRRTL:196484 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.imm_rename, io.brupdate.b2.uop.imm_rename
[722] FIRRTL:196485 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.taken, io.brupdate.b2.uop.taken
[723] FIRRTL:196486 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.pc_lob, io.brupdate.b2.uop.pc_lob
[724] FIRRTL:196487 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.edge_inst, io.brupdate.b2.uop.edge_inst
[725] FIRRTL:196488 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.ftq_idx, io.brupdate.b2.uop.ftq_idx
[726] FIRRTL:196489 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_mov, io.brupdate.b2.uop.is_mov
[727] FIRRTL:196490 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_rocc, io.brupdate.b2.uop.is_rocc
[728] FIRRTL:196491 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_sys_pc2epc, io.brupdate.b2.uop.is_sys_pc2epc
[729] FIRRTL:196492 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_eret, io.brupdate.b2.uop.is_eret
[730] FIRRTL:196493 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_amo, io.brupdate.b2.uop.is_amo
[731] FIRRTL:196494 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_sfence, io.brupdate.b2.uop.is_sfence
[732] FIRRTL:196495 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_fencei, io.brupdate.b2.uop.is_fencei
[733] FIRRTL:196496 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_fence, io.brupdate.b2.uop.is_fence
[734] FIRRTL:196497 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_sfb, io.brupdate.b2.uop.is_sfb
[735] FIRRTL:196498 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.br_type, io.brupdate.b2.uop.br_type
[736] FIRRTL:196499 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.br_tag, io.brupdate.b2.uop.br_tag
[737] FIRRTL:196500 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.br_mask, io.brupdate.b2.uop.br_mask
[738] FIRRTL:196501 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.dis_col_sel, io.brupdate.b2.uop.dis_col_sel
[739] FIRRTL:196502 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_p3_bypass_hint, io.brupdate.b2.uop.iw_p3_bypass_hint
[740] FIRRTL:196503 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_p2_bypass_hint, io.brupdate.b2.uop.iw_p2_bypass_hint
[741] FIRRTL:196504 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_p1_bypass_hint, io.brupdate.b2.uop.iw_p1_bypass_hint
[742] FIRRTL:196505 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_p2_speculative_child, io.brupdate.b2.uop.iw_p2_speculative_child
[743] FIRRTL:196506 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_p1_speculative_child, io.brupdate.b2.uop.iw_p1_speculative_child
[744] FIRRTL:196507 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_issued_partial_dgen, io.brupdate.b2.uop.iw_issued_partial_dgen
[745] FIRRTL:196508 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_issued_partial_agen, io.brupdate.b2.uop.iw_issued_partial_agen
[746] FIRRTL:196509 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iw_issued, io.brupdate.b2.uop.iw_issued
[747] FIRRTL:196510 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[0], io.brupdate.b2.uop.fu_code[0]
[748] FIRRTL:196511 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[1], io.brupdate.b2.uop.fu_code[1]
[749] FIRRTL:196512 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[2], io.brupdate.b2.uop.fu_code[2]
[750] FIRRTL:196513 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[3], io.brupdate.b2.uop.fu_code[3]
[751] FIRRTL:196514 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[4], io.brupdate.b2.uop.fu_code[4]
[752] FIRRTL:196515 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[5], io.brupdate.b2.uop.fu_code[5]
[753] FIRRTL:196516 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[6], io.brupdate.b2.uop.fu_code[6]
[754] FIRRTL:196517 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[7], io.brupdate.b2.uop.fu_code[7]
[755] FIRRTL:196518 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[8], io.brupdate.b2.uop.fu_code[8]
[756] FIRRTL:196519 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.fu_code[9], io.brupdate.b2.uop.fu_code[9]
[757] FIRRTL:196520 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iq_type[0], io.brupdate.b2.uop.iq_type[0]
[758] FIRRTL:196521 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iq_type[1], io.brupdate.b2.uop.iq_type[1]
[759] FIRRTL:196522 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iq_type[2], io.brupdate.b2.uop.iq_type[2]
[760] FIRRTL:196523 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.iq_type[3], io.brupdate.b2.uop.iq_type[3]
[761] FIRRTL:196524 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.debug_pc, io.brupdate.b2.uop.debug_pc
[762] FIRRTL:196525 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.is_rvc, io.brupdate.b2.uop.is_rvc
[763] FIRRTL:196526 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.debug_inst, io.brupdate.b2.uop.debug_inst
[764] FIRRTL:196527 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b2.uop.inst, io.brupdate.b2.uop.inst
[765] FIRRTL:196528 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b1.mispredict_mask, io.brupdate.b1.mispredict_mask
[766] FIRRTL:196529 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:629:28 KIND:connect :: connect mshrs_1.io.brupdate.b1.resolve_mask, io.brupdate.b1.resolve_mask
[767] FIRRTL:196530 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:630:26 KIND:connect :: connect mshrs_1.io.exception, io.exception
[768] FIRRTL:196531 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:631:26 KIND:connect :: connect mshrs_1.io.rob_pnr_idx, io.rob_pnr_idx
[769] FIRRTL:196532 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:632:26 KIND:connect :: connect mshrs_1.io.rob_head_idx, io.rob_head_idx
[770] FIRRTL:196533 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:634:26 KIND:connect :: connect mshrs_1.io.prober_state.bits, io.prober_state.bits
[771] FIRRTL:196534 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:634:26 KIND:connect :: connect mshrs_1.io.prober_state.valid, io.prober_state.valid
[772] FIRRTL:196535 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:636:26 KIND:connect :: connect mshrs_1.io.wb_resp, io.wb_resp
[773] FIRRTL:196536 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:638:29 KIND:connect :: connect meta_write_arb.io.in[1], mshrs_1.io.meta_write
[774] FIRRTL:196537 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:639:29 KIND:connect :: connect meta_read_arb.io.in[1], mshrs_1.io.meta_read
[775] FIRRTL:196538 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_1.io.meta_resp.bits.tag, io.meta_resp.bits.tag
[776] FIRRTL:196539 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_1.io.meta_resp.bits.coh.state, io.meta_resp.bits.coh.state
[777] FIRRTL:196540 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:640:29 KIND:connect :: connect mshrs_1.io.meta_resp.valid, io.meta_resp.valid
[778] FIRRTL:196541 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:641:29 KIND:connect :: connect wb_req_arb.io.in[1], mshrs_1.io.wb_req
[779] FIRRTL:196542 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:642:29 KIND:connect :: connect replay_arb.io.in[1], mshrs_1.io.replay
[780] FIRRTL:196543 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:643:29 KIND:connect :: connect refill_arb.io.in[1], mshrs_1.io.refill
[781] FIRRTL:196544 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:645:32 KIND:connect :: connect mshrs_1.io.lb_resp, lb[1][mshrs_1.io.lb_read.offset]
[782] FIRRTL:196545 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:646:35 KIND:when :: when mshrs_1.io.lb_write.valid :
[783] FIRRTL:196546 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:647:43 KIND:connect :: connect lb[1][mshrs_1.io.lb_write.bits.offset], mshrs_1.io.lb_write.bits.data
[784] FIRRTL:196547 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:650:21 KIND:connect :: connect commit_vals[1], mshrs_1.io.commit_val
[785] FIRRTL:196548 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:651:21 KIND:connect :: connect commit_addrs[1], mshrs_1.io.commit_addr
[786] FIRRTL:196549 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:652:21 KIND:connect :: connect commit_cohs[1], mshrs_1.io.commit_coh
[787] FIRRTL:196550 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:654:29 KIND:connect :: connect mshrs_1.io.mem_grant.valid, UInt<1>(0h0)
[788] FIRRTL:196551 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.corrupt
[789] FIRRTL:196552 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.data
[790] FIRRTL:196553 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.denied
[791] FIRRTL:196554 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.sink
[792] FIRRTL:196555 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.source
[793] FIRRTL:196556 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.size
[794] FIRRTL:196557 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.param
[795] FIRRTL:196558 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:655:29 KIND:invalidate :: invalidate mshrs_1.io.mem_grant.bits.opcode
[796] FIRRTL:196559 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:656:36 KIND:node :: node _T_9 = eq(io.mem_grant.bits.source, UInt<1>(0h1))
[797] FIRRTL:196560 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:656:45 KIND:when :: when _T_9 :
[798] FIRRTL:196561 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:657:25 KIND:connect :: connect mshrs_1.io.mem_grant, io.mem_grant
[799] FIRRTL:196562 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:660:49 KIND:node :: node _T_10 = and(mshrs_1.io.req_sec_rdy, mshrs_1.io.req_sec_val)
[800] FIRRTL:196563 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:660:25 KIND:node :: node _T_11 = or(_T_3, _T_10)
[801] FIRRTL:196564 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:661:23 KIND:connect :: connect resp_arb.io.in[1], mshrs_1.io.resp
[802] FIRRTL:196565 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:663:11 KIND:node :: node _T_12 = eq(mshrs_1.io.req_pri_rdy, UInt<1>(0h0))
[803] FIRRTL:196566 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:663:33 KIND:when :: when _T_12 :
[804] FIRRTL:196567 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:664:20 KIND:connect :: connect io.fence_rdy, UInt<1>(0h0)
[805] FIRRTL:196568 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:13 KIND:node :: node _T_13 = eq(mshrs_1.io.probe_rdy, UInt<1>(0h0))
[806] FIRRTL:196569 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:32 KIND:node :: node _T_14 = and(_T_13, idx_matches[0][1])
[807] FIRRTL:196570 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:53 KIND:node :: node _T_15 = and(_T_14, io.req_is_probe[0])
[808] FIRRTL:196571 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:667:76 KIND:when :: when _T_15 :
[809] FIRRTL:196572 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:668:22 KIND:connect :: connect io.probe_rdy, UInt<1>(0h0)
[810] FIRRTL:196573 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:676:31 KIND:regreset :: regreset mshr_head : UInt<1>, clock, reset, UInt<1>(0h0)
[811] FIRRTL:196574 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _mshr_alloc_idx_temp_vec_T = geq(UInt<1>(0h0), mshr_head)
[812] FIRRTL:196575 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node mshr_alloc_idx_temp_vec_0 = and(mshrs_0.io.req_pri_rdy, _mshr_alloc_idx_temp_vec_T)
[813] FIRRTL:196576 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _mshr_alloc_idx_temp_vec_T_1 = geq(UInt<1>(0h1), mshr_head)
[814] FIRRTL:196577 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node mshr_alloc_idx_temp_vec_1 = and(mshrs_1.io.req_pri_rdy, _mshr_alloc_idx_temp_vec_T_1)
[815] FIRRTL:196578 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _mshr_alloc_idx_idx_T = mux(mshrs_0.io.req_pri_rdy, UInt<2>(0h2), UInt<2>(0h3))
[816] FIRRTL:196579 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _mshr_alloc_idx_idx_T_1 = mux(mshr_alloc_idx_temp_vec_1, UInt<1>(0h1), _mshr_alloc_idx_idx_T)
[817] FIRRTL:196580 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node mshr_alloc_idx_idx = mux(mshr_alloc_idx_temp_vec_0, UInt<1>(0h0), _mshr_alloc_idx_idx_T_1)
[818] FIRRTL:196581 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node _mshr_alloc_idx_T = bits(mshr_alloc_idx_idx, 0, 0)
[819] FIRRTL:196582 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:677:31 KIND:reg :: reg mshr_alloc_idx_REG : UInt, clock
[820] FIRRTL:196583 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:677:31 KIND:connect :: connect mshr_alloc_idx_REG, _mshr_alloc_idx_T
[821] FIRRTL:196584 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:677:21 KIND:connect :: connect mshr_alloc_idx, mshr_alloc_idx_REG
[822] FIRRTL:196585 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:678:17 KIND:node :: node _T_16 = and(pri_rdy, pri_val)
[823] FIRRTL:196586 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:678:29 KIND:when :: when _T_16 :
[824] FIRRTL:196587 SRC:generators/boom/src/main/scala/v4/util/util.scala:211:14 KIND:node :: node _mshr_head_T = add(mshr_head, UInt<1>(0h1))
[825] FIRRTL:196588 SRC:generators/boom/src/main/scala/v4/util/util.scala:211:14 KIND:node :: node _mshr_head_T_1 = tail(_mshr_head_T, 1)
[826] FIRRTL:196589 SRC:generators/boom/src/main/scala/v4/util/util.scala:211:20 KIND:node :: node _mshr_head_T_2 = bits(_mshr_head_T_1, 0, 0)
[827] FIRRTL:196590 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:678:41 KIND:connect :: connect mshr_head, _mshr_head_T_2
[828] FIRRTL:196591 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:682:17 KIND:connect :: connect io.meta_write.bits, meta_write_arb.io.out.bits
[829] FIRRTL:196592 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:682:17 KIND:connect :: connect io.meta_write.valid, meta_write_arb.io.out.valid
[830] FIRRTL:196593 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:682:17 KIND:connect :: connect meta_write_arb.io.out.ready, io.meta_write.ready
[831] FIRRTL:196594 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:683:17 KIND:connect :: connect io.meta_read.bits, meta_read_arb.io.out.bits
[832] FIRRTL:196595 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:683:17 KIND:connect :: connect io.meta_read.valid, meta_read_arb.io.out.valid
[833] FIRRTL:196596 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:683:17 KIND:connect :: connect meta_read_arb.io.out.ready, io.meta_read.ready
[834] FIRRTL:196597 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:684:17 KIND:connect :: connect io.wb_req.bits, wb_req_arb.io.out.bits
[835] FIRRTL:196598 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:684:17 KIND:connect :: connect io.wb_req.valid, wb_req_arb.io.out.valid
[836] FIRRTL:196599 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:684:17 KIND:connect :: connect wb_req_arb.io.out.ready, io.wb_req.ready
[837] FIRRTL:196600 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:686:30 KIND:structural :: inst mmio_alloc_arb of Arbiter1_Bool
[838] FIRRTL:196601 SRC:<no-source-locator> KIND:connect :: connect mmio_alloc_arb.clock, clock
[839] FIRRTL:196602 SRC:<no-source-locator> KIND:connect :: connect mmio_alloc_arb.reset, reset
[840] FIRRTL:196603 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:693:22 KIND:structural :: inst mmios_0 of BoomIOMSHR
[841] FIRRTL:196604 SRC:<no-source-locator> KIND:connect :: connect mmios_0.clock, clock
[842] FIRRTL:196605 SRC:<no-source-locator> KIND:connect :: connect mmios_0.reset, reset
[843] FIRRTL:196606 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:695:35 KIND:connect :: connect mmio_alloc_arb.io.in[0].valid, mmios_0.io.req.ready
[844] FIRRTL:196607 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:696:35 KIND:invalidate :: invalidate mmio_alloc_arb.io.in[0].bits
[845] FIRRTL:196608 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:697:23 KIND:connect :: connect mmios_0.io.req.valid, mmio_alloc_arb.io.in[0].ready
[846] FIRRTL:196609 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.is_hella, req.bits.is_hella
[847] FIRRTL:196610 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.data, req.bits.data
[848] FIRRTL:196611 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.addr, req.bits.addr
[849] FIRRTL:196612 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.debug_tsrc, req.bits.uop.debug_tsrc
[850] FIRRTL:196613 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.debug_fsrc, req.bits.uop.debug_fsrc
[851] FIRRTL:196614 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.bp_xcpt_if, req.bits.uop.bp_xcpt_if
[852] FIRRTL:196615 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.bp_debug_if, req.bits.uop.bp_debug_if
[853] FIRRTL:196616 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.xcpt_ma_if, req.bits.uop.xcpt_ma_if
[854] FIRRTL:196617 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.xcpt_ae_if, req.bits.uop.xcpt_ae_if
[855] FIRRTL:196618 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.xcpt_pf_if, req.bits.uop.xcpt_pf_if
[856] FIRRTL:196619 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_typ, req.bits.uop.fp_typ
[857] FIRRTL:196620 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_rm, req.bits.uop.fp_rm
[858] FIRRTL:196621 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_val, req.bits.uop.fp_val
[859] FIRRTL:196622 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fcn_op, req.bits.uop.fcn_op
[860] FIRRTL:196623 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fcn_dw, req.bits.uop.fcn_dw
[861] FIRRTL:196624 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.frs3_en, req.bits.uop.frs3_en
[862] FIRRTL:196625 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.lrs2_rtype, req.bits.uop.lrs2_rtype
[863] FIRRTL:196626 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.lrs1_rtype, req.bits.uop.lrs1_rtype
[864] FIRRTL:196627 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.dst_rtype, req.bits.uop.dst_rtype
[865] FIRRTL:196628 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.lrs3, req.bits.uop.lrs3
[866] FIRRTL:196629 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.lrs2, req.bits.uop.lrs2
[867] FIRRTL:196630 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.lrs1, req.bits.uop.lrs1
[868] FIRRTL:196631 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ldst, req.bits.uop.ldst
[869] FIRRTL:196632 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ldst_is_rs1, req.bits.uop.ldst_is_rs1
[870] FIRRTL:196633 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.csr_cmd, req.bits.uop.csr_cmd
[871] FIRRTL:196634 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.flush_on_commit, req.bits.uop.flush_on_commit
[872] FIRRTL:196635 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_unique, req.bits.uop.is_unique
[873] FIRRTL:196636 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.uses_stq, req.bits.uop.uses_stq
[874] FIRRTL:196637 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.uses_ldq, req.bits.uop.uses_ldq
[875] FIRRTL:196638 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.mem_signed, req.bits.uop.mem_signed
[876] FIRRTL:196639 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.mem_size, req.bits.uop.mem_size
[877] FIRRTL:196640 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.mem_cmd, req.bits.uop.mem_cmd
[878] FIRRTL:196641 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.exc_cause, req.bits.uop.exc_cause
[879] FIRRTL:196642 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.exception, req.bits.uop.exception
[880] FIRRTL:196643 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.stale_pdst, req.bits.uop.stale_pdst
[881] FIRRTL:196644 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ppred_busy, req.bits.uop.ppred_busy
[882] FIRRTL:196645 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs3_busy, req.bits.uop.prs3_busy
[883] FIRRTL:196646 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs2_busy, req.bits.uop.prs2_busy
[884] FIRRTL:196647 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs1_busy, req.bits.uop.prs1_busy
[885] FIRRTL:196648 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ppred, req.bits.uop.ppred
[886] FIRRTL:196649 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs3, req.bits.uop.prs3
[887] FIRRTL:196650 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs2, req.bits.uop.prs2
[888] FIRRTL:196651 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.prs1, req.bits.uop.prs1
[889] FIRRTL:196652 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.pdst, req.bits.uop.pdst
[890] FIRRTL:196653 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.rxq_idx, req.bits.uop.rxq_idx
[891] FIRRTL:196654 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.stq_idx, req.bits.uop.stq_idx
[892] FIRRTL:196655 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ldq_idx, req.bits.uop.ldq_idx
[893] FIRRTL:196656 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.rob_idx, req.bits.uop.rob_idx
[894] FIRRTL:196657 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.vec, req.bits.uop.fp_ctrl.vec
[895] FIRRTL:196658 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.wflags, req.bits.uop.fp_ctrl.wflags
[896] FIRRTL:196659 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.sqrt, req.bits.uop.fp_ctrl.sqrt
[897] FIRRTL:196660 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.div, req.bits.uop.fp_ctrl.div
[898] FIRRTL:196661 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.fma, req.bits.uop.fp_ctrl.fma
[899] FIRRTL:196662 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.fastpipe, req.bits.uop.fp_ctrl.fastpipe
[900] FIRRTL:196663 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.toint, req.bits.uop.fp_ctrl.toint
[901] FIRRTL:196664 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.fromint, req.bits.uop.fp_ctrl.fromint
[902] FIRRTL:196665 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.typeTagOut, req.bits.uop.fp_ctrl.typeTagOut
[903] FIRRTL:196666 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.typeTagIn, req.bits.uop.fp_ctrl.typeTagIn
[904] FIRRTL:196667 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.swap23, req.bits.uop.fp_ctrl.swap23
[905] FIRRTL:196668 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.swap12, req.bits.uop.fp_ctrl.swap12
[906] FIRRTL:196669 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.ren3, req.bits.uop.fp_ctrl.ren3
[907] FIRRTL:196670 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.ren2, req.bits.uop.fp_ctrl.ren2
[908] FIRRTL:196671 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.ren1, req.bits.uop.fp_ctrl.ren1
[909] FIRRTL:196672 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.wen, req.bits.uop.fp_ctrl.wen
[910] FIRRTL:196673 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fp_ctrl.ldst, req.bits.uop.fp_ctrl.ldst
[911] FIRRTL:196674 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.op2_sel, req.bits.uop.op2_sel
[912] FIRRTL:196675 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.op1_sel, req.bits.uop.op1_sel
[913] FIRRTL:196676 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.imm_packed, req.bits.uop.imm_packed
[914] FIRRTL:196677 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.pimm, req.bits.uop.pimm
[915] FIRRTL:196678 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.imm_sel, req.bits.uop.imm_sel
[916] FIRRTL:196679 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.imm_rename, req.bits.uop.imm_rename
[917] FIRRTL:196680 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.taken, req.bits.uop.taken
[918] FIRRTL:196681 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.pc_lob, req.bits.uop.pc_lob
[919] FIRRTL:196682 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.edge_inst, req.bits.uop.edge_inst
[920] FIRRTL:196683 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.ftq_idx, req.bits.uop.ftq_idx
[921] FIRRTL:196684 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_mov, req.bits.uop.is_mov
[922] FIRRTL:196685 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_rocc, req.bits.uop.is_rocc
[923] FIRRTL:196686 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_sys_pc2epc, req.bits.uop.is_sys_pc2epc
[924] FIRRTL:196687 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_eret, req.bits.uop.is_eret
[925] FIRRTL:196688 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_amo, req.bits.uop.is_amo
[926] FIRRTL:196689 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_sfence, req.bits.uop.is_sfence
[927] FIRRTL:196690 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_fencei, req.bits.uop.is_fencei
[928] FIRRTL:196691 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_fence, req.bits.uop.is_fence
[929] FIRRTL:196692 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_sfb, req.bits.uop.is_sfb
[930] FIRRTL:196693 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.br_type, req.bits.uop.br_type
[931] FIRRTL:196694 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.br_tag, req.bits.uop.br_tag
[932] FIRRTL:196695 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.br_mask, req.bits.uop.br_mask
[933] FIRRTL:196696 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.dis_col_sel, req.bits.uop.dis_col_sel
[934] FIRRTL:196697 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_p3_bypass_hint, req.bits.uop.iw_p3_bypass_hint
[935] FIRRTL:196698 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_p2_bypass_hint, req.bits.uop.iw_p2_bypass_hint
[936] FIRRTL:196699 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_p1_bypass_hint, req.bits.uop.iw_p1_bypass_hint
[937] FIRRTL:196700 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_p2_speculative_child, req.bits.uop.iw_p2_speculative_child
[938] FIRRTL:196701 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_p1_speculative_child, req.bits.uop.iw_p1_speculative_child
[939] FIRRTL:196702 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_issued_partial_dgen, req.bits.uop.iw_issued_partial_dgen
[940] FIRRTL:196703 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_issued_partial_agen, req.bits.uop.iw_issued_partial_agen
[941] FIRRTL:196704 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iw_issued, req.bits.uop.iw_issued
[942] FIRRTL:196705 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[0], req.bits.uop.fu_code[0]
[943] FIRRTL:196706 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[1], req.bits.uop.fu_code[1]
[944] FIRRTL:196707 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[2], req.bits.uop.fu_code[2]
[945] FIRRTL:196708 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[3], req.bits.uop.fu_code[3]
[946] FIRRTL:196709 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[4], req.bits.uop.fu_code[4]
[947] FIRRTL:196710 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[5], req.bits.uop.fu_code[5]
[948] FIRRTL:196711 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[6], req.bits.uop.fu_code[6]
[949] FIRRTL:196712 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[7], req.bits.uop.fu_code[7]
[950] FIRRTL:196713 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[8], req.bits.uop.fu_code[8]
[951] FIRRTL:196714 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.fu_code[9], req.bits.uop.fu_code[9]
[952] FIRRTL:196715 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iq_type[0], req.bits.uop.iq_type[0]
[953] FIRRTL:196716 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iq_type[1], req.bits.uop.iq_type[1]
[954] FIRRTL:196717 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iq_type[2], req.bits.uop.iq_type[2]
[955] FIRRTL:196718 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.iq_type[3], req.bits.uop.iq_type[3]
[956] FIRRTL:196719 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.debug_pc, req.bits.uop.debug_pc
[957] FIRRTL:196720 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.is_rvc, req.bits.uop.is_rvc
[958] FIRRTL:196721 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.debug_inst, req.bits.uop.debug_inst
[959] FIRRTL:196722 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:698:23 KIND:connect :: connect mmios_0.io.req.bits.uop.inst, req.bits.uop.inst
[960] FIRRTL:196723 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:700:25 KIND:node :: node _T_17 = or(UInt<1>(0h0), mmios_0.io.req.ready)
[961] FIRRTL:196724 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.corrupt, io.mem_grant.bits.corrupt
[962] FIRRTL:196725 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.data, io.mem_grant.bits.data
[963] FIRRTL:196726 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.denied, io.mem_grant.bits.denied
[964] FIRRTL:196727 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.sink, io.mem_grant.bits.sink
[965] FIRRTL:196728 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.source, io.mem_grant.bits.source
[966] FIRRTL:196729 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.size, io.mem_grant.bits.size
[967] FIRRTL:196730 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.param, io.mem_grant.bits.param
[968] FIRRTL:196731 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:702:27 KIND:connect :: connect mmios_0.io.mem_ack.bits.opcode, io.mem_grant.bits.opcode
[969] FIRRTL:196732 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:703:77 KIND:node :: node _mshr_io_mem_ack_valid_T = eq(io.mem_grant.bits.source, UInt<2>(0h3))
[970] FIRRTL:196733 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:703:49 KIND:node :: node _mshr_io_mem_ack_valid_T_1 = and(io.mem_grant.valid, _mshr_io_mem_ack_valid_T)
[971] FIRRTL:196734 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:703:27 KIND:connect :: connect mmios_0.io.mem_ack.valid, _mshr_io_mem_ack_valid_T_1
[972] FIRRTL:196735 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:704:36 KIND:node :: node _T_18 = eq(io.mem_grant.bits.source, UInt<2>(0h3))
[973] FIRRTL:196736 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:704:46 KIND:when :: when _T_18 :
[974] FIRRTL:196737 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:705:26 KIND:connect :: connect io.mem_grant.ready, UInt<1>(0h1)
[975] FIRRTL:196738 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:708:36 KIND:connect :: connect resp_arb.io.in[2], mmios_0.io.resp
[976] FIRRTL:196739 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:709:11 KIND:node :: node _T_19 = eq(mmios_0.io.req.ready, UInt<1>(0h0))
[977] FIRRTL:196740 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:709:31 KIND:when :: when _T_19 :
[978] FIRRTL:196741 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:710:20 KIND:connect :: connect io.fence_rdy, UInt<1>(0h0)
[979] FIRRTL:196742 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:715:47 KIND:node :: node _mmio_alloc_arb_io_out_ready_T = eq(cacheable, UInt<1>(0h0))
[980] FIRRTL:196743 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:715:44 KIND:node :: node _mmio_alloc_arb_io_out_ready_T_1 = and(req.valid, _mmio_alloc_arb_io_out_ready_T)
[981] FIRRTL:196744 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:715:31 KIND:connect :: connect mmio_alloc_arb.io.out.ready, _mmio_alloc_arb_io_out_ready_T_1
[982] FIRRTL:196745 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _decode_T = dshl(UInt<12>(0hfff), mshrs_0.io.mem_acquire.bits.size)
[983] FIRRTL:196746 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _decode_T_1 = bits(_decode_T, 11, 0)
[984] FIRRTL:196747 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _decode_T_2 = not(_decode_T_1)
[985] FIRRTL:196748 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node decode = shr(_decode_T_2, 3)
[986] FIRRTL:196749 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:37 KIND:node :: node _opdata_T = bits(mshrs_0.io.mem_acquire.bits.opcode, 2, 2)
[987] FIRRTL:196750 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:28 KIND:node :: node opdata = eq(_opdata_T, UInt<1>(0h0))
[988] FIRRTL:196751 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node _T_20 = mux(opdata, decode, UInt<1>(0h0))
[989] FIRRTL:196752 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _decode_T_3 = dshl(UInt<12>(0hfff), mshrs_1.io.mem_acquire.bits.size)
[990] FIRRTL:196753 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _decode_T_4 = bits(_decode_T_3, 11, 0)
[991] FIRRTL:196754 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _decode_T_5 = not(_decode_T_4)
[992] FIRRTL:196755 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node decode_1 = shr(_decode_T_5, 3)
[993] FIRRTL:196756 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:37 KIND:node :: node _opdata_T_1 = bits(mshrs_1.io.mem_acquire.bits.opcode, 2, 2)
[994] FIRRTL:196757 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:28 KIND:node :: node opdata_1 = eq(_opdata_T_1, UInt<1>(0h0))
[995] FIRRTL:196758 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node _T_21 = mux(opdata_1, decode_1, UInt<1>(0h0))
[996] FIRRTL:196759 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _decode_T_6 = dshl(UInt<12>(0hfff), mmios_0.io.mem_access.bits.size)
[997] FIRRTL:196760 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _decode_T_7 = bits(_decode_T_6, 11, 0)
[998] FIRRTL:196761 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _decode_T_8 = not(_decode_T_7)
[999] FIRRTL:196762 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node decode_2 = shr(_decode_T_8, 3)
[1000] FIRRTL:196763 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:37 KIND:node :: node _opdata_T_2 = bits(mmios_0.io.mem_access.bits.opcode, 2, 2)
[1001] FIRRTL:196764 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:92:28 KIND:node :: node opdata_2 = eq(_opdata_T_2, UInt<1>(0h0))
[1002] FIRRTL:196765 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node _T_22 = mux(opdata_2, decode_2, UInt<1>(0h0))
[1003] FIRRTL:196766 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:60:30 KIND:regreset :: regreset beatsLeft : UInt, clock, reset, UInt<1>(0h0)
[1004] FIRRTL:196767 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:61:28 KIND:node :: node idle = eq(beatsLeft, UInt<1>(0h0))
[1005] FIRRTL:196768 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:62:24 KIND:node :: node latch = and(idle, io.mem_acquire.ready)
[1006] FIRRTL:196769 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:51 KIND:node :: node readys_hi = cat(mmios_0.io.mem_access.valid, mshrs_1.io.mem_acquire.valid)
[1007] FIRRTL:196770 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:51 KIND:node :: node _readys_T = cat(readys_hi, mshrs_0.io.mem_acquire.valid)
[1008] FIRRTL:196771 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:48 KIND:node :: node _readys_T_1 = shl(_readys_T, 1)
[1009] FIRRTL:196772 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:53 KIND:node :: node _readys_T_2 = bits(_readys_T_1, 2, 0)
[1010] FIRRTL:196773 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:43 KIND:node :: node _readys_T_3 = or(_readys_T, _readys_T_2)
[1011] FIRRTL:196774 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:48 KIND:node :: node _readys_T_4 = shl(_readys_T_3, 2)
[1012] FIRRTL:196775 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:53 KIND:node :: node _readys_T_5 = bits(_readys_T_4, 2, 0)
[1013] FIRRTL:196776 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:43 KIND:node :: node _readys_T_6 = or(_readys_T_3, _readys_T_5)
[1014] FIRRTL:196777 SRC:generators/rocket-chip/src/main/scala/util/package.scala:255:17 KIND:node :: node _readys_T_7 = bits(_readys_T_6, 2, 0)
[1015] FIRRTL:196778 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:78 KIND:node :: node _readys_T_8 = shl(_readys_T_7, 1)
[1016] FIRRTL:196779 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:83 KIND:node :: node _readys_T_9 = bits(_readys_T_8, 2, 0)
[1017] FIRRTL:196780 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:61 KIND:node :: node _readys_T_10 = not(_readys_T_9)
[1018] FIRRTL:196781 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_11 = bits(_readys_T_10, 0, 0)
[1019] FIRRTL:196782 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_12 = bits(_readys_T_10, 1, 1)
[1020] FIRRTL:196783 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_13 = bits(_readys_T_10, 2, 2)
[1021] FIRRTL:196784 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:wire :: wire readys : UInt<1>[3]
[1022] FIRRTL:196785 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys[0], _readys_T_11
[1023] FIRRTL:196786 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys[1], _readys_T_12
[1024] FIRRTL:196787 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys[2], _readys_T_13
[1025] FIRRTL:196788 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T = and(readys[0], mshrs_0.io.mem_acquire.valid)
[1026] FIRRTL:196789 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T_1 = and(readys[1], mshrs_1.io.mem_acquire.valid)
[1027] FIRRTL:196790 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T_2 = and(readys[2], mmios_0.io.mem_access.valid)
[1028] FIRRTL:196791 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:wire :: wire winner : UInt<1>[3]
[1029] FIRRTL:196792 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner[0], _winner_T
[1030] FIRRTL:196793 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner[1], _winner_T_1
[1031] FIRRTL:196794 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner[2], _winner_T_2
[1032] FIRRTL:196795 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node prefixOR_1 = or(UInt<1>(0h0), winner[0])
[1033] FIRRTL:196796 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node prefixOR_2 = or(prefixOR_1, winner[1])
[1034] FIRRTL:196797 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node _prefixOR_T = or(prefixOR_2, winner[2])
[1035] FIRRTL:196798 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_23 = eq(UInt<1>(0h0), UInt<1>(0h0))
[1036] FIRRTL:196799 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_24 = eq(winner[0], UInt<1>(0h0))
[1037] FIRRTL:196800 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_25 = or(_T_23, _T_24)
[1038] FIRRTL:196801 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_26 = eq(prefixOR_1, UInt<1>(0h0))
[1039] FIRRTL:196802 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_27 = eq(winner[1], UInt<1>(0h0))
[1040] FIRRTL:196803 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_28 = or(_T_26, _T_27)
[1041] FIRRTL:196804 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_29 = eq(prefixOR_2, UInt<1>(0h0))
[1042] FIRRTL:196805 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_30 = eq(winner[2], UInt<1>(0h0))
[1043] FIRRTL:196806 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_31 = or(_T_29, _T_30)
[1044] FIRRTL:196807 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:77 KIND:node :: node _T_32 = and(_T_25, _T_28)
[1045] FIRRTL:196808 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:77 KIND:node :: node _T_33 = and(_T_32, _T_31)
[1046] FIRRTL:196809 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_34 = asUInt(reset)
[1047] FIRRTL:196810 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_35 = eq(_T_34, UInt<1>(0h0))
[1048] FIRRTL:196811 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_35 :
[1049] FIRRTL:196812 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_36 = eq(_T_33, UInt<1>(0h0))
[1050] FIRRTL:196813 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_36 :
[1051] FIRRTL:196814 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:77 assert((prefixOR zip winner) map { case (p,w) => !p || !w } reduce {_ && _})\n") : printf
[1052] FIRRTL:196815 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: assert(clock, _T_33, UInt<1>(0h1), "") : assert
[1053] FIRRTL:196816 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:31 KIND:node :: node _T_37 = or(mshrs_0.io.mem_acquire.valid, mshrs_1.io.mem_acquire.valid)
[1054] FIRRTL:196817 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:31 KIND:node :: node _T_38 = or(_T_37, mmios_0.io.mem_access.valid)
[1055] FIRRTL:196818 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:15 KIND:node :: node _T_39 = eq(_T_38, UInt<1>(0h0))
[1056] FIRRTL:196819 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:54 KIND:node :: node _T_40 = or(winner[0], winner[1])
[1057] FIRRTL:196820 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:54 KIND:node :: node _T_41 = or(_T_40, winner[2])
[1058] FIRRTL:196821 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:36 KIND:node :: node _T_42 = or(_T_39, _T_41)
[1059] FIRRTL:196822 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_43 = asUInt(reset)
[1060] FIRRTL:196823 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_44 = eq(_T_43, UInt<1>(0h0))
[1061] FIRRTL:196824 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_44 :
[1062] FIRRTL:196825 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_45 = eq(_T_42, UInt<1>(0h0))
[1063] FIRRTL:196826 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_45 :
[1064] FIRRTL:196827 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:79 assert (!valids.reduce(_||_) || winner.reduce(_||_))\n") : printf_1
[1065] FIRRTL:196828 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: assert(clock, _T_42, UInt<1>(0h1), "") : assert_1
[1066] FIRRTL:196829 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_0 = mux(winner[0], _T_20, UInt<1>(0h0))
[1067] FIRRTL:196830 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_1 = mux(winner[1], _T_21, UInt<1>(0h0))
[1068] FIRRTL:196831 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_2 = mux(winner[2], _T_22, UInt<1>(0h0))
[1069] FIRRTL:196832 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:84:44 KIND:node :: node _initBeats_T = or(maskedBeats_0, maskedBeats_1)
[1070] FIRRTL:196833 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:84:44 KIND:node :: node initBeats = or(_initBeats_T, maskedBeats_2)
[1071] FIRRTL:196834 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _beatsLeft_T = and(io.mem_acquire.ready, io.mem_acquire.valid)
[1072] FIRRTL:196835 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_1 = sub(beatsLeft, _beatsLeft_T)
[1073] FIRRTL:196836 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_2 = tail(_beatsLeft_T_1, 1)
[1074] FIRRTL:196837 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:23 KIND:node :: node _beatsLeft_T_3 = mux(latch, initBeats, _beatsLeft_T_2)
[1075] FIRRTL:196838 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:17 KIND:connect :: connect beatsLeft, _beatsLeft_T_3
[1076] FIRRTL:196839 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:wire :: wire _state_WIRE : UInt<1>[3]
[1077] FIRRTL:196840 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE[0], UInt<1>(0h0)
[1078] FIRRTL:196841 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE[1], UInt<1>(0h0)
[1079] FIRRTL:196842 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE[2], UInt<1>(0h0)
[1080] FIRRTL:196843 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:26 KIND:regreset :: regreset state : UInt<1>[3], clock, reset, _state_WIRE
[1081] FIRRTL:196844 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:89:25 KIND:node :: node muxState = mux(idle, winner, state)
[1082] FIRRTL:196845 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:90:13 KIND:connect :: connect state, muxState
[1083] FIRRTL:196846 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:92:24 KIND:node :: node allowed = mux(idle, readys, state)
[1084] FIRRTL:196847 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _mshrs_0_io_mem_acquire_ready_T = and(io.mem_acquire.ready, allowed[0])
[1085] FIRRTL:196848 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect mshrs_0.io.mem_acquire.ready, _mshrs_0_io_mem_acquire_ready_T
[1086] FIRRTL:196849 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _mshrs_1_io_mem_acquire_ready_T = and(io.mem_acquire.ready, allowed[1])
[1087] FIRRTL:196850 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect mshrs_1.io.mem_acquire.ready, _mshrs_1_io_mem_acquire_ready_T
[1088] FIRRTL:196851 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _mmios_0_io_mem_access_ready_T = and(io.mem_acquire.ready, allowed[2])
[1089] FIRRTL:196852 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect mmios_0.io.mem_access.ready, _mmios_0_io_mem_access_ready_T
[1090] FIRRTL:196853 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:46 KIND:node :: node _io_mem_acquire_valid_T = or(mshrs_0.io.mem_acquire.valid, mshrs_1.io.mem_acquire.valid)
[1091] FIRRTL:196854 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:46 KIND:node :: node _io_mem_acquire_valid_T_1 = or(_io_mem_acquire_valid_T, mmios_0.io.mem_access.valid)
[1092] FIRRTL:196855 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_valid_T_2 = mux(state[0], mshrs_0.io.mem_acquire.valid, UInt<1>(0h0))
[1093] FIRRTL:196856 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_valid_T_3 = mux(state[1], mshrs_1.io.mem_acquire.valid, UInt<1>(0h0))
[1094] FIRRTL:196857 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_valid_T_4 = mux(state[2], mmios_0.io.mem_access.valid, UInt<1>(0h0))
[1095] FIRRTL:196858 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_valid_T_5 = or(_io_mem_acquire_valid_T_2, _io_mem_acquire_valid_T_3)
[1096] FIRRTL:196859 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_valid_T_6 = or(_io_mem_acquire_valid_T_5, _io_mem_acquire_valid_T_4)
[1097] FIRRTL:196860 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_valid_WIRE : UInt<1>
[1098] FIRRTL:196861 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_valid_WIRE, _io_mem_acquire_valid_T_6
[1099] FIRRTL:196862 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:24 KIND:node :: node _io_mem_acquire_valid_T_7 = mux(idle, _io_mem_acquire_valid_T_1, _io_mem_acquire_valid_WIRE)
[1100] FIRRTL:196863 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:18 KIND:connect :: connect io.mem_acquire.valid, _io_mem_acquire_valid_T_7
[1101] FIRRTL:196864 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[1102] FIRRTL:196865 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T = mux(muxState[0], mshrs_0.io.mem_acquire.bits.corrupt, UInt<1>(0h0))
[1103] FIRRTL:196866 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_1 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.corrupt, UInt<1>(0h0))
[1104] FIRRTL:196867 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_2 = mux(muxState[2], mmios_0.io.mem_access.bits.corrupt, UInt<1>(0h0))
[1105] FIRRTL:196868 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_3 = or(_io_mem_acquire_bits_T, _io_mem_acquire_bits_T_1)
[1106] FIRRTL:196869 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_4 = or(_io_mem_acquire_bits_T_3, _io_mem_acquire_bits_T_2)
[1107] FIRRTL:196870 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_1 : UInt<1>
[1108] FIRRTL:196871 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_1, _io_mem_acquire_bits_T_4
[1109] FIRRTL:196872 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.corrupt, _io_mem_acquire_bits_WIRE_1
[1110] FIRRTL:196873 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_5 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.data, UInt<1>(0h0))
[1111] FIRRTL:196874 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_6 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.data, UInt<1>(0h0))
[1112] FIRRTL:196875 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_7 = mux(muxState[2], mmios_0.io.mem_access.bits.data, UInt<1>(0h0))
[1113] FIRRTL:196876 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_8 = or(_io_mem_acquire_bits_T_5, _io_mem_acquire_bits_T_6)
[1114] FIRRTL:196877 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_9 = or(_io_mem_acquire_bits_T_8, _io_mem_acquire_bits_T_7)
[1115] FIRRTL:196878 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_2 : UInt<64>
[1116] FIRRTL:196879 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_2, _io_mem_acquire_bits_T_9
[1117] FIRRTL:196880 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.data, _io_mem_acquire_bits_WIRE_2
[1118] FIRRTL:196881 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_10 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.mask, UInt<1>(0h0))
[1119] FIRRTL:196882 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_11 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.mask, UInt<1>(0h0))
[1120] FIRRTL:196883 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_12 = mux(muxState[2], mmios_0.io.mem_access.bits.mask, UInt<1>(0h0))
[1121] FIRRTL:196884 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_13 = or(_io_mem_acquire_bits_T_10, _io_mem_acquire_bits_T_11)
[1122] FIRRTL:196885 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_14 = or(_io_mem_acquire_bits_T_13, _io_mem_acquire_bits_T_12)
[1123] FIRRTL:196886 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_3 : UInt<8>
[1124] FIRRTL:196887 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_3, _io_mem_acquire_bits_T_14
[1125] FIRRTL:196888 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.mask, _io_mem_acquire_bits_WIRE_3
[1126] FIRRTL:196889 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_4 : { }
[1127] FIRRTL:196890 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.echo, _io_mem_acquire_bits_WIRE_4
[1128] FIRRTL:196891 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_5 : { }
[1129] FIRRTL:196892 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.user, _io_mem_acquire_bits_WIRE_5
[1130] FIRRTL:196893 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_15 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.address, UInt<1>(0h0))
[1131] FIRRTL:196894 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_16 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.address, UInt<1>(0h0))
[1132] FIRRTL:196895 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_17 = mux(muxState[2], mmios_0.io.mem_access.bits.address, UInt<1>(0h0))
[1133] FIRRTL:196896 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_18 = or(_io_mem_acquire_bits_T_15, _io_mem_acquire_bits_T_16)
[1134] FIRRTL:196897 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_19 = or(_io_mem_acquire_bits_T_18, _io_mem_acquire_bits_T_17)
[1135] FIRRTL:196898 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_6 : UInt<32>
[1136] FIRRTL:196899 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_6, _io_mem_acquire_bits_T_19
[1137] FIRRTL:196900 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.address, _io_mem_acquire_bits_WIRE_6
[1138] FIRRTL:196901 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_20 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.source, UInt<1>(0h0))
[1139] FIRRTL:196902 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_21 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.source, UInt<1>(0h0))
[1140] FIRRTL:196903 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_22 = mux(muxState[2], mmios_0.io.mem_access.bits.source, UInt<1>(0h0))
[1141] FIRRTL:196904 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_23 = or(_io_mem_acquire_bits_T_20, _io_mem_acquire_bits_T_21)
[1142] FIRRTL:196905 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_24 = or(_io_mem_acquire_bits_T_23, _io_mem_acquire_bits_T_22)
[1143] FIRRTL:196906 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_7 : UInt<2>
[1144] FIRRTL:196907 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_7, _io_mem_acquire_bits_T_24
[1145] FIRRTL:196908 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.source, _io_mem_acquire_bits_WIRE_7
[1146] FIRRTL:196909 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_25 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.size, UInt<1>(0h0))
[1147] FIRRTL:196910 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_26 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.size, UInt<1>(0h0))
[1148] FIRRTL:196911 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_27 = mux(muxState[2], mmios_0.io.mem_access.bits.size, UInt<1>(0h0))
[1149] FIRRTL:196912 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_28 = or(_io_mem_acquire_bits_T_25, _io_mem_acquire_bits_T_26)
[1150] FIRRTL:196913 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_29 = or(_io_mem_acquire_bits_T_28, _io_mem_acquire_bits_T_27)
[1151] FIRRTL:196914 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_8 : UInt<4>
[1152] FIRRTL:196915 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_8, _io_mem_acquire_bits_T_29
[1153] FIRRTL:196916 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.size, _io_mem_acquire_bits_WIRE_8
[1154] FIRRTL:196917 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_30 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.param, UInt<1>(0h0))
[1155] FIRRTL:196918 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_31 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.param, UInt<1>(0h0))
[1156] FIRRTL:196919 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_32 = mux(muxState[2], mmios_0.io.mem_access.bits.param, UInt<1>(0h0))
[1157] FIRRTL:196920 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_33 = or(_io_mem_acquire_bits_T_30, _io_mem_acquire_bits_T_31)
[1158] FIRRTL:196921 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_34 = or(_io_mem_acquire_bits_T_33, _io_mem_acquire_bits_T_32)
[1159] FIRRTL:196922 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_9 : UInt<3>
[1160] FIRRTL:196923 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_9, _io_mem_acquire_bits_T_34
[1161] FIRRTL:196924 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.param, _io_mem_acquire_bits_WIRE_9
[1162] FIRRTL:196925 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_35 = mux(muxState[0], mshrs_0.io.mem_acquire.bits.opcode, UInt<1>(0h0))
[1163] FIRRTL:196926 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_36 = mux(muxState[1], mshrs_1.io.mem_acquire.bits.opcode, UInt<1>(0h0))
[1164] FIRRTL:196927 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_37 = mux(muxState[2], mmios_0.io.mem_access.bits.opcode, UInt<1>(0h0))
[1165] FIRRTL:196928 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_38 = or(_io_mem_acquire_bits_T_35, _io_mem_acquire_bits_T_36)
[1166] FIRRTL:196929 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_acquire_bits_T_39 = or(_io_mem_acquire_bits_T_38, _io_mem_acquire_bits_T_37)
[1167] FIRRTL:196930 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_acquire_bits_WIRE_10 : UInt<3>
[1168] FIRRTL:196931 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE_10, _io_mem_acquire_bits_T_39
[1169] FIRRTL:196932 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_acquire_bits_WIRE.opcode, _io_mem_acquire_bits_WIRE_10
[1170] FIRRTL:196933 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.corrupt, _io_mem_acquire_bits_WIRE.corrupt
[1171] FIRRTL:196934 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.data, _io_mem_acquire_bits_WIRE.data
[1172] FIRRTL:196935 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.mask, _io_mem_acquire_bits_WIRE.mask
[1173] FIRRTL:196936 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.address, _io_mem_acquire_bits_WIRE.address
[1174] FIRRTL:196937 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.source, _io_mem_acquire_bits_WIRE.source
[1175] FIRRTL:196938 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.size, _io_mem_acquire_bits_WIRE.size
[1176] FIRRTL:196939 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.param, _io_mem_acquire_bits_WIRE.param
[1177] FIRRTL:196940 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_acquire.bits.opcode, _io_mem_acquire_bits_WIRE.opcode
[1178] FIRRTL:196941 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:60:30 KIND:regreset :: regreset beatsLeft_1 : UInt, clock, reset, UInt<1>(0h0)
[1179] FIRRTL:196942 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:61:28 KIND:node :: node idle_1 = eq(beatsLeft_1, UInt<1>(0h0))
[1180] FIRRTL:196943 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:62:24 KIND:node :: node latch_1 = and(idle_1, io.mem_finish.ready)
[1181] FIRRTL:196944 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:51 KIND:node :: node _readys_T_14 = cat(mshrs_1.io.mem_finish.valid, mshrs_0.io.mem_finish.valid)
[1182] FIRRTL:196945 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:48 KIND:node :: node _readys_T_15 = shl(_readys_T_14, 1)
[1183] FIRRTL:196946 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:53 KIND:node :: node _readys_T_16 = bits(_readys_T_15, 1, 0)
[1184] FIRRTL:196947 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:43 KIND:node :: node _readys_T_17 = or(_readys_T_14, _readys_T_16)
[1185] FIRRTL:196948 SRC:generators/rocket-chip/src/main/scala/util/package.scala:255:17 KIND:node :: node _readys_T_18 = bits(_readys_T_17, 1, 0)
[1186] FIRRTL:196949 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:78 KIND:node :: node _readys_T_19 = shl(_readys_T_18, 1)
[1187] FIRRTL:196950 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:83 KIND:node :: node _readys_T_20 = bits(_readys_T_19, 1, 0)
[1188] FIRRTL:196951 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:61 KIND:node :: node _readys_T_21 = not(_readys_T_20)
[1189] FIRRTL:196952 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_22 = bits(_readys_T_21, 0, 0)
[1190] FIRRTL:196953 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_23 = bits(_readys_T_21, 1, 1)
[1191] FIRRTL:196954 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:wire :: wire readys_1 : UInt<1>[2]
[1192] FIRRTL:196955 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys_1[0], _readys_T_22
[1193] FIRRTL:196956 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys_1[1], _readys_T_23
[1194] FIRRTL:196957 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T_3 = and(readys_1[0], mshrs_0.io.mem_finish.valid)
[1195] FIRRTL:196958 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T_4 = and(readys_1[1], mshrs_1.io.mem_finish.valid)
[1196] FIRRTL:196959 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:wire :: wire winner_1 : UInt<1>[2]
[1197] FIRRTL:196960 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner_1[0], _winner_T_3
[1198] FIRRTL:196961 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner_1[1], _winner_T_4
[1199] FIRRTL:196962 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node prefixOR_1_1 = or(UInt<1>(0h0), winner_1[0])
[1200] FIRRTL:196963 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:76:48 KIND:node :: node _prefixOR_T_1 = or(prefixOR_1_1, winner_1[1])
[1201] FIRRTL:196964 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_46 = eq(UInt<1>(0h0), UInt<1>(0h0))
[1202] FIRRTL:196965 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_47 = eq(winner_1[0], UInt<1>(0h0))
[1203] FIRRTL:196966 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_48 = or(_T_46, _T_47)
[1204] FIRRTL:196967 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:56 KIND:node :: node _T_49 = eq(prefixOR_1_1, UInt<1>(0h0))
[1205] FIRRTL:196968 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:62 KIND:node :: node _T_50 = eq(winner_1[1], UInt<1>(0h0))
[1206] FIRRTL:196969 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:59 KIND:node :: node _T_51 = or(_T_49, _T_50)
[1207] FIRRTL:196970 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:77 KIND:node :: node _T_52 = and(_T_48, _T_51)
[1208] FIRRTL:196971 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_53 = asUInt(reset)
[1209] FIRRTL:196972 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_54 = eq(_T_53, UInt<1>(0h0))
[1210] FIRRTL:196973 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_54 :
[1211] FIRRTL:196974 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:node :: node _T_55 = eq(_T_52, UInt<1>(0h0))
[1212] FIRRTL:196975 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:when :: when _T_55 :
[1213] FIRRTL:196976 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:77 assert((prefixOR zip winner) map { case (p,w) => !p || !w } reduce {_ && _})\n") : printf_2
[1214] FIRRTL:196977 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:77:13 KIND:nondriving :: assert(clock, _T_52, UInt<1>(0h1), "") : assert_2
[1215] FIRRTL:196978 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:31 KIND:node :: node _T_56 = or(mshrs_0.io.mem_finish.valid, mshrs_1.io.mem_finish.valid)
[1216] FIRRTL:196979 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:15 KIND:node :: node _T_57 = eq(_T_56, UInt<1>(0h0))
[1217] FIRRTL:196980 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:54 KIND:node :: node _T_58 = or(winner_1[0], winner_1[1])
[1218] FIRRTL:196981 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:36 KIND:node :: node _T_59 = or(_T_57, _T_58)
[1219] FIRRTL:196982 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_60 = asUInt(reset)
[1220] FIRRTL:196983 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_61 = eq(_T_60, UInt<1>(0h0))
[1221] FIRRTL:196984 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_61 :
[1222] FIRRTL:196985 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:node :: node _T_62 = eq(_T_59, UInt<1>(0h0))
[1223] FIRRTL:196986 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:when :: when _T_62 :
[1224] FIRRTL:196987 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at Arbiter.scala:79 assert (!valids.reduce(_||_) || winner.reduce(_||_))\n") : printf_3
[1225] FIRRTL:196988 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:79:14 KIND:nondriving :: assert(clock, _T_59, UInt<1>(0h1), "") : assert_3
[1226] FIRRTL:196989 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_0_1 = mux(winner_1[0], UInt<1>(0h0), UInt<1>(0h0))
[1227] FIRRTL:196990 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_1_1 = mux(winner_1[1], UInt<1>(0h0), UInt<1>(0h0))
[1228] FIRRTL:196991 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:84:44 KIND:node :: node initBeats_1 = or(maskedBeats_0_1, maskedBeats_1_1)
[1229] FIRRTL:196992 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _beatsLeft_T_4 = and(io.mem_finish.ready, io.mem_finish.valid)
[1230] FIRRTL:196993 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_5 = sub(beatsLeft_1, _beatsLeft_T_4)
[1231] FIRRTL:196994 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_6 = tail(_beatsLeft_T_5, 1)
[1232] FIRRTL:196995 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:23 KIND:node :: node _beatsLeft_T_7 = mux(latch_1, initBeats_1, _beatsLeft_T_6)
[1233] FIRRTL:196996 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:17 KIND:connect :: connect beatsLeft_1, _beatsLeft_T_7
[1234] FIRRTL:196997 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:wire :: wire _state_WIRE_1 : UInt<1>[2]
[1235] FIRRTL:196998 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE_1[0], UInt<1>(0h0)
[1236] FIRRTL:196999 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:34 KIND:connect :: connect _state_WIRE_1[1], UInt<1>(0h0)
[1237] FIRRTL:197000 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88:26 KIND:regreset :: regreset state_1 : UInt<1>[2], clock, reset, _state_WIRE_1
[1238] FIRRTL:197001 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:89:25 KIND:node :: node muxState_1 = mux(idle_1, winner_1, state_1)
[1239] FIRRTL:197002 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:90:13 KIND:connect :: connect state_1, muxState_1
[1240] FIRRTL:197003 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:92:24 KIND:node :: node allowed_1 = mux(idle_1, readys_1, state_1)
[1241] FIRRTL:197004 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _mshrs_0_io_mem_finish_ready_T = and(io.mem_finish.ready, allowed_1[0])
[1242] FIRRTL:197005 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect mshrs_0.io.mem_finish.ready, _mshrs_0_io_mem_finish_ready_T
[1243] FIRRTL:197006 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:31 KIND:node :: node _mshrs_1_io_mem_finish_ready_T = and(io.mem_finish.ready, allowed_1[1])
[1244] FIRRTL:197007 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:94:17 KIND:connect :: connect mshrs_1.io.mem_finish.ready, _mshrs_1_io_mem_finish_ready_T
[1245] FIRRTL:197008 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:46 KIND:node :: node _io_mem_finish_valid_T = or(mshrs_0.io.mem_finish.valid, mshrs_1.io.mem_finish.valid)
[1246] FIRRTL:197009 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_valid_T_1 = mux(state_1[0], mshrs_0.io.mem_finish.valid, UInt<1>(0h0))
[1247] FIRRTL:197010 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_valid_T_2 = mux(state_1[1], mshrs_1.io.mem_finish.valid, UInt<1>(0h0))
[1248] FIRRTL:197011 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_valid_T_3 = or(_io_mem_finish_valid_T_1, _io_mem_finish_valid_T_2)
[1249] FIRRTL:197012 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_finish_valid_WIRE : UInt<1>
[1250] FIRRTL:197013 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_finish_valid_WIRE, _io_mem_finish_valid_T_3
[1251] FIRRTL:197014 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:24 KIND:node :: node _io_mem_finish_valid_T_4 = mux(idle_1, _io_mem_finish_valid_T, _io_mem_finish_valid_WIRE)
[1252] FIRRTL:197015 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:18 KIND:connect :: connect io.mem_finish.valid, _io_mem_finish_valid_T_4
[1253] FIRRTL:197016 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_finish_bits_WIRE : { sink : UInt<3>}
[1254] FIRRTL:197017 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_bits_T = mux(muxState_1[0], mshrs_0.io.mem_finish.bits.sink, UInt<1>(0h0))
[1255] FIRRTL:197018 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_bits_T_1 = mux(muxState_1[1], mshrs_1.io.mem_finish.bits.sink, UInt<1>(0h0))
[1256] FIRRTL:197019 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _io_mem_finish_bits_T_2 = or(_io_mem_finish_bits_T, _io_mem_finish_bits_T_1)
[1257] FIRRTL:197020 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _io_mem_finish_bits_WIRE_1 : UInt<3>
[1258] FIRRTL:197021 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_finish_bits_WIRE_1, _io_mem_finish_bits_T_2
[1259] FIRRTL:197022 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _io_mem_finish_bits_WIRE.sink, _io_mem_finish_bits_WIRE_1
[1260] FIRRTL:197023 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect io.mem_finish.bits.sink, _io_mem_finish_bits_WIRE.sink
[1261] FIRRTL:197024 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:720:21 KIND:structural :: inst respq of BranchKillableQueue_4
[1262] FIRRTL:197025 SRC:<no-source-locator> KIND:connect :: connect respq.clock, clock
[1263] FIRRTL:197026 SRC:<no-source-locator> KIND:connect :: connect respq.reset, reset
[1264] FIRRTL:197027 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.target_offset, io.brupdate.b2.target_offset
[1265] FIRRTL:197028 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.jalr_target, io.brupdate.b2.jalr_target
[1266] FIRRTL:197029 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.pc_sel, io.brupdate.b2.pc_sel
[1267] FIRRTL:197030 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.cfi_type, io.brupdate.b2.cfi_type
[1268] FIRRTL:197031 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.taken, io.brupdate.b2.taken
[1269] FIRRTL:197032 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.mispredict, io.brupdate.b2.mispredict
[1270] FIRRTL:197033 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.debug_tsrc, io.brupdate.b2.uop.debug_tsrc
[1271] FIRRTL:197034 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.debug_fsrc, io.brupdate.b2.uop.debug_fsrc
[1272] FIRRTL:197035 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.bp_xcpt_if, io.brupdate.b2.uop.bp_xcpt_if
[1273] FIRRTL:197036 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.bp_debug_if, io.brupdate.b2.uop.bp_debug_if
[1274] FIRRTL:197037 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.xcpt_ma_if, io.brupdate.b2.uop.xcpt_ma_if
[1275] FIRRTL:197038 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.xcpt_ae_if, io.brupdate.b2.uop.xcpt_ae_if
[1276] FIRRTL:197039 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.xcpt_pf_if, io.brupdate.b2.uop.xcpt_pf_if
[1277] FIRRTL:197040 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_typ, io.brupdate.b2.uop.fp_typ
[1278] FIRRTL:197041 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_rm, io.brupdate.b2.uop.fp_rm
[1279] FIRRTL:197042 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_val, io.brupdate.b2.uop.fp_val
[1280] FIRRTL:197043 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fcn_op, io.brupdate.b2.uop.fcn_op
[1281] FIRRTL:197044 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fcn_dw, io.brupdate.b2.uop.fcn_dw
[1282] FIRRTL:197045 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.frs3_en, io.brupdate.b2.uop.frs3_en
[1283] FIRRTL:197046 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.lrs2_rtype, io.brupdate.b2.uop.lrs2_rtype
[1284] FIRRTL:197047 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.lrs1_rtype, io.brupdate.b2.uop.lrs1_rtype
[1285] FIRRTL:197048 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.dst_rtype, io.brupdate.b2.uop.dst_rtype
[1286] FIRRTL:197049 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.lrs3, io.brupdate.b2.uop.lrs3
[1287] FIRRTL:197050 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.lrs2, io.brupdate.b2.uop.lrs2
[1288] FIRRTL:197051 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.lrs1, io.brupdate.b2.uop.lrs1
[1289] FIRRTL:197052 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ldst, io.brupdate.b2.uop.ldst
[1290] FIRRTL:197053 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ldst_is_rs1, io.brupdate.b2.uop.ldst_is_rs1
[1291] FIRRTL:197054 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.csr_cmd, io.brupdate.b2.uop.csr_cmd
[1292] FIRRTL:197055 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.flush_on_commit, io.brupdate.b2.uop.flush_on_commit
[1293] FIRRTL:197056 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_unique, io.brupdate.b2.uop.is_unique
[1294] FIRRTL:197057 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.uses_stq, io.brupdate.b2.uop.uses_stq
[1295] FIRRTL:197058 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.uses_ldq, io.brupdate.b2.uop.uses_ldq
[1296] FIRRTL:197059 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.mem_signed, io.brupdate.b2.uop.mem_signed
[1297] FIRRTL:197060 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.mem_size, io.brupdate.b2.uop.mem_size
[1298] FIRRTL:197061 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.mem_cmd, io.brupdate.b2.uop.mem_cmd
[1299] FIRRTL:197062 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.exc_cause, io.brupdate.b2.uop.exc_cause
[1300] FIRRTL:197063 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.exception, io.brupdate.b2.uop.exception
[1301] FIRRTL:197064 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.stale_pdst, io.brupdate.b2.uop.stale_pdst
[1302] FIRRTL:197065 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ppred_busy, io.brupdate.b2.uop.ppred_busy
[1303] FIRRTL:197066 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs3_busy, io.brupdate.b2.uop.prs3_busy
[1304] FIRRTL:197067 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs2_busy, io.brupdate.b2.uop.prs2_busy
[1305] FIRRTL:197068 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs1_busy, io.brupdate.b2.uop.prs1_busy
[1306] FIRRTL:197069 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ppred, io.brupdate.b2.uop.ppred
[1307] FIRRTL:197070 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs3, io.brupdate.b2.uop.prs3
[1308] FIRRTL:197071 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs2, io.brupdate.b2.uop.prs2
[1309] FIRRTL:197072 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.prs1, io.brupdate.b2.uop.prs1
[1310] FIRRTL:197073 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.pdst, io.brupdate.b2.uop.pdst
[1311] FIRRTL:197074 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.rxq_idx, io.brupdate.b2.uop.rxq_idx
[1312] FIRRTL:197075 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.stq_idx, io.brupdate.b2.uop.stq_idx
[1313] FIRRTL:197076 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ldq_idx, io.brupdate.b2.uop.ldq_idx
[1314] FIRRTL:197077 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.rob_idx, io.brupdate.b2.uop.rob_idx
[1315] FIRRTL:197078 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.vec, io.brupdate.b2.uop.fp_ctrl.vec
[1316] FIRRTL:197079 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.wflags, io.brupdate.b2.uop.fp_ctrl.wflags
[1317] FIRRTL:197080 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.sqrt, io.brupdate.b2.uop.fp_ctrl.sqrt
[1318] FIRRTL:197081 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.div, io.brupdate.b2.uop.fp_ctrl.div
[1319] FIRRTL:197082 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.fma, io.brupdate.b2.uop.fp_ctrl.fma
[1320] FIRRTL:197083 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.fastpipe, io.brupdate.b2.uop.fp_ctrl.fastpipe
[1321] FIRRTL:197084 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.toint, io.brupdate.b2.uop.fp_ctrl.toint
[1322] FIRRTL:197085 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.fromint, io.brupdate.b2.uop.fp_ctrl.fromint
[1323] FIRRTL:197086 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.typeTagOut, io.brupdate.b2.uop.fp_ctrl.typeTagOut
[1324] FIRRTL:197087 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.typeTagIn, io.brupdate.b2.uop.fp_ctrl.typeTagIn
[1325] FIRRTL:197088 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.swap23, io.brupdate.b2.uop.fp_ctrl.swap23
[1326] FIRRTL:197089 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.swap12, io.brupdate.b2.uop.fp_ctrl.swap12
[1327] FIRRTL:197090 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.ren3, io.brupdate.b2.uop.fp_ctrl.ren3
[1328] FIRRTL:197091 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.ren2, io.brupdate.b2.uop.fp_ctrl.ren2
[1329] FIRRTL:197092 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.ren1, io.brupdate.b2.uop.fp_ctrl.ren1
[1330] FIRRTL:197093 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.wen, io.brupdate.b2.uop.fp_ctrl.wen
[1331] FIRRTL:197094 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fp_ctrl.ldst, io.brupdate.b2.uop.fp_ctrl.ldst
[1332] FIRRTL:197095 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.op2_sel, io.brupdate.b2.uop.op2_sel
[1333] FIRRTL:197096 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.op1_sel, io.brupdate.b2.uop.op1_sel
[1334] FIRRTL:197097 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.imm_packed, io.brupdate.b2.uop.imm_packed
[1335] FIRRTL:197098 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.pimm, io.brupdate.b2.uop.pimm
[1336] FIRRTL:197099 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.imm_sel, io.brupdate.b2.uop.imm_sel
[1337] FIRRTL:197100 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.imm_rename, io.brupdate.b2.uop.imm_rename
[1338] FIRRTL:197101 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.taken, io.brupdate.b2.uop.taken
[1339] FIRRTL:197102 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.pc_lob, io.brupdate.b2.uop.pc_lob
[1340] FIRRTL:197103 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.edge_inst, io.brupdate.b2.uop.edge_inst
[1341] FIRRTL:197104 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.ftq_idx, io.brupdate.b2.uop.ftq_idx
[1342] FIRRTL:197105 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_mov, io.brupdate.b2.uop.is_mov
[1343] FIRRTL:197106 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_rocc, io.brupdate.b2.uop.is_rocc
[1344] FIRRTL:197107 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_sys_pc2epc, io.brupdate.b2.uop.is_sys_pc2epc
[1345] FIRRTL:197108 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_eret, io.brupdate.b2.uop.is_eret
[1346] FIRRTL:197109 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_amo, io.brupdate.b2.uop.is_amo
[1347] FIRRTL:197110 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_sfence, io.brupdate.b2.uop.is_sfence
[1348] FIRRTL:197111 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_fencei, io.brupdate.b2.uop.is_fencei
[1349] FIRRTL:197112 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_fence, io.brupdate.b2.uop.is_fence
[1350] FIRRTL:197113 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_sfb, io.brupdate.b2.uop.is_sfb
[1351] FIRRTL:197114 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.br_type, io.brupdate.b2.uop.br_type
[1352] FIRRTL:197115 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.br_tag, io.brupdate.b2.uop.br_tag
[1353] FIRRTL:197116 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.br_mask, io.brupdate.b2.uop.br_mask
[1354] FIRRTL:197117 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.dis_col_sel, io.brupdate.b2.uop.dis_col_sel
[1355] FIRRTL:197118 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_p3_bypass_hint, io.brupdate.b2.uop.iw_p3_bypass_hint
[1356] FIRRTL:197119 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_p2_bypass_hint, io.brupdate.b2.uop.iw_p2_bypass_hint
[1357] FIRRTL:197120 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_p1_bypass_hint, io.brupdate.b2.uop.iw_p1_bypass_hint
[1358] FIRRTL:197121 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_p2_speculative_child, io.brupdate.b2.uop.iw_p2_speculative_child
[1359] FIRRTL:197122 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_p1_speculative_child, io.brupdate.b2.uop.iw_p1_speculative_child
[1360] FIRRTL:197123 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_issued_partial_dgen, io.brupdate.b2.uop.iw_issued_partial_dgen
[1361] FIRRTL:197124 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_issued_partial_agen, io.brupdate.b2.uop.iw_issued_partial_agen
[1362] FIRRTL:197125 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iw_issued, io.brupdate.b2.uop.iw_issued
[1363] FIRRTL:197126 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[0], io.brupdate.b2.uop.fu_code[0]
[1364] FIRRTL:197127 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[1], io.brupdate.b2.uop.fu_code[1]
[1365] FIRRTL:197128 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[2], io.brupdate.b2.uop.fu_code[2]
[1366] FIRRTL:197129 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[3], io.brupdate.b2.uop.fu_code[3]
[1367] FIRRTL:197130 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[4], io.brupdate.b2.uop.fu_code[4]
[1368] FIRRTL:197131 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[5], io.brupdate.b2.uop.fu_code[5]
[1369] FIRRTL:197132 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[6], io.brupdate.b2.uop.fu_code[6]
[1370] FIRRTL:197133 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[7], io.brupdate.b2.uop.fu_code[7]
[1371] FIRRTL:197134 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[8], io.brupdate.b2.uop.fu_code[8]
[1372] FIRRTL:197135 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.fu_code[9], io.brupdate.b2.uop.fu_code[9]
[1373] FIRRTL:197136 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iq_type[0], io.brupdate.b2.uop.iq_type[0]
[1374] FIRRTL:197137 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iq_type[1], io.brupdate.b2.uop.iq_type[1]
[1375] FIRRTL:197138 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iq_type[2], io.brupdate.b2.uop.iq_type[2]
[1376] FIRRTL:197139 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.iq_type[3], io.brupdate.b2.uop.iq_type[3]
[1377] FIRRTL:197140 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.debug_pc, io.brupdate.b2.uop.debug_pc
[1378] FIRRTL:197141 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.is_rvc, io.brupdate.b2.uop.is_rvc
[1379] FIRRTL:197142 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.debug_inst, io.brupdate.b2.uop.debug_inst
[1380] FIRRTL:197143 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b2.uop.inst, io.brupdate.b2.uop.inst
[1381] FIRRTL:197144 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b1.mispredict_mask, io.brupdate.b1.mispredict_mask
[1382] FIRRTL:197145 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:721:22 KIND:connect :: connect respq.io.brupdate.b1.resolve_mask, io.brupdate.b1.resolve_mask
[1383] FIRRTL:197146 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:722:22 KIND:connect :: connect respq.io.flush, io.exception
[1384] FIRRTL:197147 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:723:22 KIND:connect :: connect respq.io.enq, resp_arb.io.out
[1385] FIRRTL:197148 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:724:22 KIND:connect :: connect io.resp.bits, respq.io.deq.bits
[1386] FIRRTL:197149 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:724:22 KIND:connect :: connect io.resp.valid, respq.io.deq.valid
[1387] FIRRTL:197150 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:724:22 KIND:connect :: connect respq.io.deq.ready, io.resp.ready
[1388] FIRRTL:197151 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:727:34 KIND:node :: node _io_req_0_ready_T = eq(UInt<1>(0h0), UInt<1>(0h0))
[1389] FIRRTL:197152 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:728:11 KIND:node :: node _io_req_0_ready_T_1 = eq(cacheable, UInt<1>(0h0))
[1390] FIRRTL:197153 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:728:75 KIND:node :: node _io_req_0_ready_T_2 = and(tag_match[0], _T_11)
[1391] FIRRTL:197154 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:728:47 KIND:node :: node _io_req_0_ready_T_3 = mux(idx_match[0], _io_req_0_ready_T_2, pri_rdy)
[1392] FIRRTL:197155 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:728:41 KIND:node :: node _io_req_0_ready_T_4 = and(sdq_rdy, _io_req_0_ready_T_3)
[1393] FIRRTL:197156 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:728:10 KIND:node :: node _io_req_0_ready_T_5 = mux(_io_req_0_ready_T_1, _T_17, _io_req_0_ready_T_4)
[1394] FIRRTL:197157 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:727:47 KIND:node :: node _io_req_0_ready_T_6 = and(_io_req_0_ready_T, _io_req_0_ready_T_5)
[1395] FIRRTL:197158 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:727:26 KIND:connect :: connect io.req[0].ready, _io_req_0_ready_T_6
[1396] FIRRTL:197159 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:729:42 KIND:node :: node _io_secondary_miss_0_T = and(idx_match[0], way_match[0])
[1397] FIRRTL:197160 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:729:61 KIND:node :: node _io_secondary_miss_0_T_1 = eq(tag_match[0], UInt<1>(0h0))
[1398] FIRRTL:197161 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:729:58 KIND:node :: node _io_secondary_miss_0_T_2 = and(_io_secondary_miss_0_T, _io_secondary_miss_0_T_1)
[1399] FIRRTL:197162 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:729:26 KIND:connect :: connect io.secondary_miss[0], _io_secondary_miss_0_T_2
[1400] FIRRTL:197163 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:730:42 KIND:node :: node _io_block_hit_0_T = and(idx_match[0], tag_match[0])
[1401] FIRRTL:197164 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:730:26 KIND:connect :: connect io.block_hit[0], _io_block_hit_0_T
[1402] FIRRTL:197165 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:732:21 KIND:connect :: connect io.refill.bits, refill_arb.io.out.bits
[1403] FIRRTL:197166 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:732:21 KIND:connect :: connect io.refill.valid, refill_arb.io.out.valid
[1404] FIRRTL:197167 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:732:21 KIND:connect :: connect refill_arb.io.out.ready, io.refill.ready
[1405] FIRRTL:197168 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _free_sdq_T = and(io.replay.ready, io.replay.valid)
[1406] FIRRTL:197169 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _free_sdq_T_1 = eq(io.replay.bits.uop.mem_cmd, UInt<1>(0h1))
[1407] FIRRTL:197170 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _free_sdq_T_2 = eq(io.replay.bits.uop.mem_cmd, UInt<5>(0h11))
[1408] FIRRTL:197171 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _free_sdq_T_3 = or(_free_sdq_T_1, _free_sdq_T_2)
[1409] FIRRTL:197172 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _free_sdq_T_4 = eq(io.replay.bits.uop.mem_cmd, UInt<3>(0h7))
[1410] FIRRTL:197173 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _free_sdq_T_5 = or(_free_sdq_T_3, _free_sdq_T_4)
[1411] FIRRTL:197174 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_6 = eq(io.replay.bits.uop.mem_cmd, UInt<3>(0h4))
[1412] FIRRTL:197175 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_7 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0h9))
[1413] FIRRTL:197176 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_8 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0ha))
[1414] FIRRTL:197177 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_9 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0hb))
[1415] FIRRTL:197178 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_10 = or(_free_sdq_T_6, _free_sdq_T_7)
[1416] FIRRTL:197179 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_11 = or(_free_sdq_T_10, _free_sdq_T_8)
[1417] FIRRTL:197180 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_12 = or(_free_sdq_T_11, _free_sdq_T_9)
[1418] FIRRTL:197181 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_13 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0h8))
[1419] FIRRTL:197182 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_14 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0hc))
[1420] FIRRTL:197183 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_15 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0hd))
[1421] FIRRTL:197184 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_16 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0he))
[1422] FIRRTL:197185 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _free_sdq_T_17 = eq(io.replay.bits.uop.mem_cmd, UInt<4>(0hf))
[1423] FIRRTL:197186 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_18 = or(_free_sdq_T_13, _free_sdq_T_14)
[1424] FIRRTL:197187 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_19 = or(_free_sdq_T_18, _free_sdq_T_15)
[1425] FIRRTL:197188 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_20 = or(_free_sdq_T_19, _free_sdq_T_16)
[1426] FIRRTL:197189 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _free_sdq_T_21 = or(_free_sdq_T_20, _free_sdq_T_17)
[1427] FIRRTL:197190 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _free_sdq_T_22 = or(_free_sdq_T_12, _free_sdq_T_21)
[1428] FIRRTL:197191 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _free_sdq_T_23 = or(_free_sdq_T_5, _free_sdq_T_22)
[1429] FIRRTL:197192 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:734:33 KIND:node :: node free_sdq = and(_free_sdq_T, _free_sdq_T_23)
[1430] FIRRTL:197193 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:736:13 KIND:connect :: connect io.replay.bits, replay_arb.io.out.bits
[1431] FIRRTL:197194 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:736:13 KIND:connect :: connect io.replay.valid, replay_arb.io.out.valid
[1432] FIRRTL:197195 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:736:13 KIND:connect :: connect replay_arb.io.out.ready, io.replay.ready
[1433] FIRRTL:197196 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:737:29 KIND:infer_mport :: infer mport io_replay_bits_data_MPORT = sdq[replay_arb.io.out.bits.sdq_id], clock
[1434] FIRRTL:197197 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:737:23 KIND:connect :: connect io.replay.bits.data, io_replay_bits_data_MPORT
[1435] FIRRTL:197198 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:739:25 KIND:node :: node _T_63 = or(io.replay.valid, sdq_enq)
[1436] FIRRTL:197199 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:739:37 KIND:when :: when _T_63 :
[1437] FIRRTL:197200 SRC:src/main/scala/chisel3/util/OneHot.scala:58:35 KIND:node :: node _sdq_val_T = dshl(UInt<1>(0h1), replay_arb.io.out.bits.sdq_id)
[1438] FIRRTL:197201 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:74 KIND:node :: node _sdq_val_T_1 = mux(free_sdq, UInt<17>(0h1ffff), UInt<17>(0h0))
[1439] FIRRTL:197202 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:68 KIND:node :: node _sdq_val_T_2 = and(_sdq_val_T, _sdq_val_T_1)
[1440] FIRRTL:197203 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:26 KIND:node :: node _sdq_val_T_3 = not(_sdq_val_T_2)
[1441] FIRRTL:197204 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:24 KIND:node :: node _sdq_val_T_4 = and(sdq_val, _sdq_val_T_3)
[1442] FIRRTL:197205 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:741:33 KIND:node :: node _sdq_val_T_5 = bits(sdq_val, 16, 0)
[1443] FIRRTL:197206 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:741:25 KIND:node :: node _sdq_val_T_6 = not(_sdq_val_T_5)
[1444] FIRRTL:197207 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_7 = bits(_sdq_val_T_6, 0, 0)
[1445] FIRRTL:197208 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_8 = bits(_sdq_val_T_6, 1, 1)
[1446] FIRRTL:197209 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_9 = bits(_sdq_val_T_6, 2, 2)
[1447] FIRRTL:197210 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_10 = bits(_sdq_val_T_6, 3, 3)
[1448] FIRRTL:197211 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_11 = bits(_sdq_val_T_6, 4, 4)
[1449] FIRRTL:197212 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_12 = bits(_sdq_val_T_6, 5, 5)
[1450] FIRRTL:197213 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_13 = bits(_sdq_val_T_6, 6, 6)
[1451] FIRRTL:197214 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_14 = bits(_sdq_val_T_6, 7, 7)
[1452] FIRRTL:197215 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_15 = bits(_sdq_val_T_6, 8, 8)
[1453] FIRRTL:197216 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_16 = bits(_sdq_val_T_6, 9, 9)
[1454] FIRRTL:197217 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_17 = bits(_sdq_val_T_6, 10, 10)
[1455] FIRRTL:197218 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_18 = bits(_sdq_val_T_6, 11, 11)
[1456] FIRRTL:197219 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_19 = bits(_sdq_val_T_6, 12, 12)
[1457] FIRRTL:197220 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_20 = bits(_sdq_val_T_6, 13, 13)
[1458] FIRRTL:197221 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_21 = bits(_sdq_val_T_6, 14, 14)
[1459] FIRRTL:197222 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_22 = bits(_sdq_val_T_6, 15, 15)
[1460] FIRRTL:197223 SRC:src/main/scala/chisel3/util/OneHot.scala:85:71 KIND:node :: node _sdq_val_T_23 = bits(_sdq_val_T_6, 16, 16)
[1461] FIRRTL:197224 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_24 = mux(_sdq_val_T_23, UInt<17>(0h10000), UInt<17>(0h0))
[1462] FIRRTL:197225 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_25 = mux(_sdq_val_T_22, UInt<17>(0h8000), _sdq_val_T_24)
[1463] FIRRTL:197226 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_26 = mux(_sdq_val_T_21, UInt<17>(0h4000), _sdq_val_T_25)
[1464] FIRRTL:197227 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_27 = mux(_sdq_val_T_20, UInt<17>(0h2000), _sdq_val_T_26)
[1465] FIRRTL:197228 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_28 = mux(_sdq_val_T_19, UInt<17>(0h1000), _sdq_val_T_27)
[1466] FIRRTL:197229 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_29 = mux(_sdq_val_T_18, UInt<17>(0h800), _sdq_val_T_28)
[1467] FIRRTL:197230 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_30 = mux(_sdq_val_T_17, UInt<17>(0h400), _sdq_val_T_29)
[1468] FIRRTL:197231 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_31 = mux(_sdq_val_T_16, UInt<17>(0h200), _sdq_val_T_30)
[1469] FIRRTL:197232 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_32 = mux(_sdq_val_T_15, UInt<17>(0h100), _sdq_val_T_31)
[1470] FIRRTL:197233 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_33 = mux(_sdq_val_T_14, UInt<17>(0h80), _sdq_val_T_32)
[1471] FIRRTL:197234 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_34 = mux(_sdq_val_T_13, UInt<17>(0h40), _sdq_val_T_33)
[1472] FIRRTL:197235 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_35 = mux(_sdq_val_T_12, UInt<17>(0h20), _sdq_val_T_34)
[1473] FIRRTL:197236 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_36 = mux(_sdq_val_T_11, UInt<17>(0h10), _sdq_val_T_35)
[1474] FIRRTL:197237 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_37 = mux(_sdq_val_T_10, UInt<17>(0h8), _sdq_val_T_36)
[1475] FIRRTL:197238 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_38 = mux(_sdq_val_T_9, UInt<17>(0h4), _sdq_val_T_37)
[1476] FIRRTL:197239 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_39 = mux(_sdq_val_T_8, UInt<17>(0h2), _sdq_val_T_38)
[1477] FIRRTL:197240 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _sdq_val_T_40 = mux(_sdq_val_T_7, UInt<17>(0h1), _sdq_val_T_39)
[1478] FIRRTL:197241 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:741:55 KIND:node :: node _sdq_val_T_41 = mux(sdq_enq, UInt<17>(0h1ffff), UInt<17>(0h0))
[1479] FIRRTL:197242 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:741:49 KIND:node :: node _sdq_val_T_42 = and(_sdq_val_T_40, _sdq_val_T_41)
[1480] FIRRTL:197243 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:96 KIND:node :: node _sdq_val_T_43 = or(_sdq_val_T_4, _sdq_val_T_42)
[1481] FIRRTL:197244 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:740:13 KIND:connect :: connect sdq_val, _sdq_val_T_43
[1482] FIRRTL:197245 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:744:41 KIND:reg :: reg prefetcher_io_mshr_avail_REG : UInt<1>, clock
[1483] FIRRTL:197246 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:744:41 KIND:connect :: connect prefetcher_io_mshr_avail_REG, pri_rdy
[1484] FIRRTL:197247 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:744:31 KIND:connect :: connect prefetcher.io.mshr_avail, prefetcher_io_mshr_avail_REG
[1485] FIRRTL:197248 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:745:62 KIND:node :: node _prefetcher_io_req_val_T = or(commit_vals[0], commit_vals[1])
[1486] FIRRTL:197249 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:745:41 KIND:reg :: reg prefetcher_io_req_val_REG : UInt<1>, clock
[1487] FIRRTL:197250 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:745:41 KIND:connect :: connect prefetcher_io_req_val_REG, _prefetcher_io_req_val_T
[1488] FIRRTL:197251 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:745:31 KIND:connect :: connect prefetcher.io.req_val, prefetcher_io_req_val_REG
[1489] FIRRTL:197252 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_addr_T = mux(commit_vals[0], commit_addrs[0], UInt<1>(0h0))
[1490] FIRRTL:197253 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_addr_T_1 = mux(commit_vals[1], commit_addrs[1], UInt<1>(0h0))
[1491] FIRRTL:197254 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_addr_T_2 = or(_prefetcher_io_req_addr_T, _prefetcher_io_req_addr_T_1)
[1492] FIRRTL:197255 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _prefetcher_io_req_addr_WIRE : UInt<40>
[1493] FIRRTL:197256 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _prefetcher_io_req_addr_WIRE, _prefetcher_io_req_addr_T_2
[1494] FIRRTL:197257 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:746:41 KIND:reg :: reg prefetcher_io_req_addr_REG : UInt, clock
[1495] FIRRTL:197258 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:746:41 KIND:connect :: connect prefetcher_io_req_addr_REG, _prefetcher_io_req_addr_WIRE
[1496] FIRRTL:197259 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:746:31 KIND:connect :: connect prefetcher.io.req_addr, prefetcher_io_req_addr_REG
[1497] FIRRTL:197260 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _prefetcher_io_req_coh_WIRE : { state : UInt<2>}
[1498] FIRRTL:197261 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_coh_T = mux(commit_vals[0], commit_cohs[0].state, UInt<1>(0h0))
[1499] FIRRTL:197262 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_coh_T_1 = mux(commit_vals[1], commit_cohs[1].state, UInt<1>(0h0))
[1500] FIRRTL:197263 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _prefetcher_io_req_coh_T_2 = or(_prefetcher_io_req_coh_T, _prefetcher_io_req_coh_T_1)
[1501] FIRRTL:197264 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:wire :: wire _prefetcher_io_req_coh_WIRE_1 : UInt<2>
[1502] FIRRTL:197265 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _prefetcher_io_req_coh_WIRE_1, _prefetcher_io_req_coh_T_2
[1503] FIRRTL:197266 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _prefetcher_io_req_coh_WIRE.state, _prefetcher_io_req_coh_WIRE_1
[1504] FIRRTL:197267 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:747:41 KIND:reg :: reg prefetcher_io_req_coh_REG : { state : UInt<2>}, clock
[1505] FIRRTL:197268 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:747:41 KIND:connect :: connect prefetcher_io_req_coh_REG, _prefetcher_io_req_coh_WIRE
[1506] FIRRTL:197269 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:747:31 KIND:connect :: connect prefetcher.io.req_coh.state, prefetcher_io_req_coh_REG.state
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
  "task_id": "parent_synthesis-BoomMSHRFile-adf43e298d82a651",
  "work_unit_id": "BoomMSHRFile",
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
