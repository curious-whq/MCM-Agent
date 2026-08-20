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

Task ID: `leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.6`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomMSHR.rpq.main`
- module: `BranchKillableQueue`
- kind: `module`
- instance path: `BoomMSHR.rpq.main`
- leaf: `True`
- coverage complete: `True`
- raw statements: 286
- logical statements: 59
- mapped/logical source lines: 43
- registers: 5
- physical boundary events: 2

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
   specialized to a particular module. If a semantic property that you judge
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

- `BoomMSHR.rpq.main::io.deq.fire`
  - predicate: `io.deq.valid && io.deq.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.deq.bits.addr', 'io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.old_meta.coh.state', 'io.deq.bits.old_meta.tag', 'io.deq.bits.sdq_id', 'io.deq.bits.tag_match', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.bits.way_en']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'valids']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']
- `BoomMSHR.rpq.main::io.enq.fire`
  - predicate: `io.enq.valid && io.enq.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.enq.bits.addr', 'io.enq.bits.data', 'io.enq.bits.is_hella', 'io.enq.bits.old_meta.coh.state', 'io.enq.bits.old_meta.tag', 'io.enq.bits.sdq_id', 'io.enq.bits.tag_match', 'io.enq.bits.uop.bp_debug_if', 'io.enq.bits.uop.bp_xcpt_if', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.br_tag', 'io.enq.bits.uop.br_type', 'io.enq.bits.uop.csr_cmd', 'io.enq.bits.uop.debug_fsrc', 'io.enq.bits.uop.debug_inst', 'io.enq.bits.uop.debug_pc', 'io.enq.bits.uop.debug_tsrc', 'io.enq.bits.uop.dis_col_sel', 'io.enq.bits.uop.dst_rtype', 'io.enq.bits.uop.edge_inst', 'io.enq.bits.uop.exc_cause', 'io.enq.bits.uop.exception', 'io.enq.bits.uop.fcn_dw', 'io.enq.bits.uop.fcn_op', 'io.enq.bits.uop.flush_on_commit', 'io.enq.bits.uop.fp_ctrl.div', 'io.enq.bits.uop.fp_ctrl.fastpipe', 'io.enq.bits.uop.fp_ctrl.fma', 'io.enq.bits.uop.fp_ctrl.fromint', 'io.enq.bits.uop.fp_ctrl.ldst', 'io.enq.bits.uop.fp_ctrl.ren1', 'io.enq.bits.uop.fp_ctrl.ren2', 'io.enq.bits.uop.fp_ctrl.ren3', 'io.enq.bits.uop.fp_ctrl.sqrt', 'io.enq.bits.uop.fp_ctrl.swap12', 'io.enq.bits.uop.fp_ctrl.swap23', 'io.enq.bits.uop.fp_ctrl.toint', 'io.enq.bits.uop.fp_ctrl.typeTagIn', 'io.enq.bits.uop.fp_ctrl.typeTagOut', 'io.enq.bits.uop.fp_ctrl.vec', 'io.enq.bits.uop.fp_ctrl.wen', 'io.enq.bits.uop.fp_ctrl.wflags', 'io.enq.bits.uop.fp_rm', 'io.enq.bits.uop.fp_typ', 'io.enq.bits.uop.fp_val', 'io.enq.bits.uop.frs3_en', 'io.enq.bits.uop.ftq_idx', 'io.enq.bits.uop.fu_code[0]', 'io.enq.bits.uop.fu_code[1]', 'io.enq.bits.uop.fu_code[2]', 'io.enq.bits.uop.fu_code[3]', 'io.enq.bits.uop.fu_code[4]', 'io.enq.bits.uop.fu_code[5]', 'io.enq.bits.uop.fu_code[6]', 'io.enq.bits.uop.fu_code[7]', 'io.enq.bits.uop.fu_code[8]', 'io.enq.bits.uop.fu_code[9]', 'io.enq.bits.uop.imm_packed', 'io.enq.bits.uop.imm_rename', 'io.enq.bits.uop.imm_sel', 'io.enq.bits.uop.inst', 'io.enq.bits.uop.iq_type[0]', 'io.enq.bits.uop.iq_type[1]', 'io.enq.bits.uop.iq_type[2]', 'io.enq.bits.uop.iq_type[3]', 'io.enq.bits.uop.is_amo', 'io.enq.bits.uop.is_eret', 'io.enq.bits.uop.is_fence', 'io.enq.bits.uop.is_fencei', 'io.enq.bits.uop.is_mov', 'io.enq.bits.uop.is_rocc', 'io.enq.bits.uop.is_rvc', 'io.enq.bits.uop.is_sfb', 'io.enq.bits.uop.is_sfence', 'io.enq.bits.uop.is_sys_pc2epc', 'io.enq.bits.uop.is_unique', 'io.enq.bits.uop.iw_issued', 'io.enq.bits.uop.iw_issued_partial_agen', 'io.enq.bits.uop.iw_issued_partial_dgen', 'io.enq.bits.uop.iw_p1_bypass_hint', 'io.enq.bits.uop.iw_p1_speculative_child', 'io.enq.bits.uop.iw_p2_bypass_hint', 'io.enq.bits.uop.iw_p2_speculative_child', 'io.enq.bits.uop.iw_p3_bypass_hint', 'io.enq.bits.uop.ldq_idx', 'io.enq.bits.uop.ldst', 'io.enq.bits.uop.ldst_is_rs1', 'io.enq.bits.uop.lrs1', 'io.enq.bits.uop.lrs1_rtype', 'io.enq.bits.uop.lrs2', 'io.enq.bits.uop.lrs2_rtype', 'io.enq.bits.uop.lrs3', 'io.enq.bits.uop.mem_cmd', 'io.enq.bits.uop.mem_signed', 'io.enq.bits.uop.mem_size', 'io.enq.bits.uop.op1_sel', 'io.enq.bits.uop.op2_sel', 'io.enq.bits.uop.pc_lob', 'io.enq.bits.uop.pdst', 'io.enq.bits.uop.pimm', 'io.enq.bits.uop.ppred', 'io.enq.bits.uop.ppred_busy', 'io.enq.bits.uop.prs1', 'io.enq.bits.uop.prs1_busy', 'io.enq.bits.uop.prs2', 'io.enq.bits.uop.prs2_busy', 'io.enq.bits.uop.prs3', 'io.enq.bits.uop.prs3_busy', 'io.enq.bits.uop.rob_idx', 'io.enq.bits.uop.rxq_idx', 'io.enq.bits.uop.stale_pdst', 'io.enq.bits.uop.stq_idx', 'io.enq.bits.uop.taken', 'io.enq.bits.uop.uses_ldq', 'io.enq.bits.uop.uses_stq', 'io.enq.bits.uop.xcpt_ae_if', 'io.enq.bits.uop.xcpt_ma_if', 'io.enq.bits.uop.xcpt_pf_if', 'io.enq.bits.way_en']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Concrete local state

['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Environment/frontier signals

['clock', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.count', 'io.deq.bits.addr', 'io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.old_meta.coh.state', 'io.deq.bits.old_meta.tag', 'io.deq.bits.sdq_id', 'io.deq.bits.tag_match', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.bits.way_en', 'io.deq.ready', 'io.deq.valid', 'io.empty', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.uses_ldq', 'io.enq.ready', 'io.enq.valid', 'io.flush']

## Source evidence

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

### generators/boom/src/main/scala/v4/util/util.scala:96-98
```scala
   def apply(brupdate: BrUpdateInfo, br_mask: UInt): UInt = {
     return br_mask & ~brupdate.b1.resolve_mask
   }
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

### generators/boom/src/main/scala/v4/util/util.scala:521-525
```scala
  } else {
    val ram     = Mem(entries, gen)
    val valids  = RegInit(VecInit(Seq.fill(entries) {false.B}))
    val uops    = Reg(Vec(entries, new MicroOp))
```

### generators/boom/src/main/scala/v4/util/util.scala:527-535
```scala
    val deq_ptr = Counter(entries)
    val maybe_full = RegInit(false.B)

    val ptr_match = enq_ptr.value === deq_ptr.value
    io.empty := ptr_match && !maybe_full
    val full = ptr_match && maybe_full
    val do_enq = WireInit(io.enq.fire && !IsKilledByBranch(io.brupdate, false.B, io.enq.bits.uop) && !(io.flush && flush_fn(io.enq.bits.uop)))
    val do_deq = WireInit((io.deq.ready || !valids(deq_ptr.value)) && !io.empty)
```

### generators/boom/src/main/scala/v4/util/util.scala:538-542
```scala
      val uop  = uops(i)
      valids(i)  := valids(i) && !IsKilledByBranch(io.brupdate, false.B, mask) && !(io.flush && flush_fn(uop))
      when (valids(i)) {
        uops(i).br_mask := GetNewBrMask(io.brupdate, mask)
      }
```

### generators/boom/src/main/scala/v4/util/util.scala:544-550
```scala

    when (do_enq) {
      ram(enq_ptr.value)          := io.enq.bits
      valids(enq_ptr.value)       := true.B
      uops(enq_ptr.value)         := io.enq.bits.uop
      uops(enq_ptr.value).br_mask := GetNewBrMask(io.brupdate, io.enq.bits.uop)
      enq_ptr.inc()
```

### generators/boom/src/main/scala/v4/util/util.scala:552-555
```scala

    when (do_deq) {
      valids(deq_ptr.value) := false.B
      deq_ptr.inc()
```

### generators/boom/src/main/scala/v4/util/util.scala:557-560
```scala

    when (do_enq =/= do_deq) {
      maybe_full := do_enq
                      }
```

### generators/boom/src/main/scala/v4/util/util.scala:561-571
```scala

    io.enq.ready := !full

    val out = Wire(gen)
    out             := ram(deq_ptr.value)
    out.uop         := uops(deq_ptr.value)
    io.deq.valid            := !io.empty && valids(deq_ptr.value)
    io.deq.bits             := out

    val ptr_diff = enq_ptr.value - deq_ptr.value
    if (isPow2(entries)) {
```

### generators/boom/src/main/scala/v4/util/util.scala:574-580
```scala
    else {
      io.count := Mux(ptr_match,
        Mux(maybe_full,
          entries.asUInt, 0.U),
        Mux(deq_ptr.value > enq_ptr.value,
          entries.asUInt + ptr_diff, ptr_diff))
    }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:188591 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input clock : Clock
[1] FIRRTL:188592 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input reset : Reset
[2] FIRRTL:188593 SRC:generators/boom/src/main/scala/v4/util/util.scala:482:14 KIND:structural :: output io : { flip enq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}}, flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip flush : UInt<1>, empty : UInt<1>, count : UInt<4>}
[3] FIRRTL:188595 SRC:generators/boom/src/main/scala/v4/util/util.scala:522:22 KIND:memory :: cmem ram : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>} [15]
[4] FIRRTL:188596 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:wire :: wire _valids_WIRE : UInt<1>[15]
[5] FIRRTL:188597 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[0], UInt<1>(0h0)
[6] FIRRTL:188598 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[1], UInt<1>(0h0)
[7] FIRRTL:188599 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[2], UInt<1>(0h0)
[8] FIRRTL:188600 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[3], UInt<1>(0h0)
[9] FIRRTL:188601 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[4], UInt<1>(0h0)
[10] FIRRTL:188602 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[5], UInt<1>(0h0)
[11] FIRRTL:188603 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[6], UInt<1>(0h0)
[12] FIRRTL:188604 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[7], UInt<1>(0h0)
[13] FIRRTL:188605 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[8], UInt<1>(0h0)
[14] FIRRTL:188606 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[9], UInt<1>(0h0)
[15] FIRRTL:188607 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[10], UInt<1>(0h0)
[16] FIRRTL:188608 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[11], UInt<1>(0h0)
[17] FIRRTL:188609 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[12], UInt<1>(0h0)
[18] FIRRTL:188610 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[13], UInt<1>(0h0)
[19] FIRRTL:188611 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[14], UInt<1>(0h0)
[20] FIRRTL:188612 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:26 KIND:regreset :: regreset valids : UInt<1>[15], clock, reset, _valids_WIRE
[21] FIRRTL:188613 SRC:generators/boom/src/main/scala/v4/util/util.scala:524:22 KIND:reg :: reg uops : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}[15], clock
[22] FIRRTL:188614 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset enq_ptr_value : UInt<4>, clock, reset, UInt<4>(0h0)
[23] FIRRTL:188615 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset deq_ptr_value : UInt<4>, clock, reset, UInt<4>(0h0)
[24] FIRRTL:188616 SRC:generators/boom/src/main/scala/v4/util/util.scala:528:29 KIND:regreset :: regreset maybe_full : UInt<1>, clock, reset, UInt<1>(0h0)
[25] FIRRTL:188617 SRC:generators/boom/src/main/scala/v4/util/util.scala:530:35 KIND:node :: node ptr_match = eq(enq_ptr_value, deq_ptr_value)
[26] FIRRTL:188618 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:30 KIND:node :: node _io_empty_T = eq(maybe_full, UInt<1>(0h0))
[27] FIRRTL:188619 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:27 KIND:node :: node _io_empty_T_1 = and(ptr_match, _io_empty_T)
[28] FIRRTL:188620 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:14 KIND:connect :: connect io.empty, _io_empty_T_1
[29] FIRRTL:188621 SRC:generators/boom/src/main/scala/v4/util/util.scala:532:26 KIND:node :: node full = and(ptr_match, maybe_full)
[30] FIRRTL:188622 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _do_enq_T = and(io.enq.ready, io.enq.valid)
[31] FIRRTL:188623 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _do_enq_T_1 = and(io.brupdate.b1.mispredict_mask, io.enq.bits.uop.br_mask)
[32] FIRRTL:188624 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _do_enq_T_2 = neq(_do_enq_T_1, UInt<1>(0h0))
[33] FIRRTL:188625 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _do_enq_T_3 = or(_do_enq_T_2, UInt<1>(0h0))
[34] FIRRTL:188626 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:42 KIND:node :: node _do_enq_T_4 = eq(_do_enq_T_3, UInt<1>(0h0))
[35] FIRRTL:188627 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:39 KIND:node :: node _do_enq_T_5 = and(_do_enq_T, _do_enq_T_4)
[36] FIRRTL:188628 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:113 KIND:node :: node _do_enq_T_6 = and(io.flush, io.enq.bits.uop.uses_ldq)
[37] FIRRTL:188629 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:102 KIND:node :: node _do_enq_T_7 = eq(_do_enq_T_6, UInt<1>(0h0))
[38] FIRRTL:188630 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:99 KIND:node :: node _do_enq_T_8 = and(_do_enq_T_5, _do_enq_T_7)
[39] FIRRTL:188631 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:wire :: wire do_enq : UInt<1>
[40] FIRRTL:188632 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:connect :: connect do_enq, _do_enq_T_8
[41] FIRRTL:188633 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:44 KIND:node :: node _do_deq_T = eq(valids[deq_ptr_value], UInt<1>(0h0))
[42] FIRRTL:188634 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:41 KIND:node :: node _do_deq_T_1 = or(io.deq.ready, _do_deq_T)
[43] FIRRTL:188635 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:71 KIND:node :: node _do_deq_T_2 = eq(io.empty, UInt<1>(0h0))
[44] FIRRTL:188636 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:68 KIND:node :: node _do_deq_T_3 = and(_do_deq_T_1, _do_deq_T_2)
[45] FIRRTL:188637 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:wire :: wire do_deq : UInt<1>
[46] FIRRTL:188638 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:connect :: connect do_deq, _do_deq_T_3
[47] FIRRTL:188639 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_0_T = and(io.brupdate.b1.mispredict_mask, uops[0].br_mask)
[48] FIRRTL:188640 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_0_T_1 = neq(_valids_0_T, UInt<1>(0h0))
[49] FIRRTL:188641 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_0_T_2 = or(_valids_0_T_1, UInt<1>(0h0))
[50] FIRRTL:188642 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_0_T_3 = eq(_valids_0_T_2, UInt<1>(0h0))
[51] FIRRTL:188643 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_0_T_4 = and(valids[0], _valids_0_T_3)
[52] FIRRTL:188644 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_0_T_5 = and(io.flush, uops[0].uses_ldq)
[53] FIRRTL:188645 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_0_T_6 = eq(_valids_0_T_5, UInt<1>(0h0))
[54] FIRRTL:188646 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_0_T_7 = and(_valids_0_T_4, _valids_0_T_6)
[55] FIRRTL:188647 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[0], _valids_0_T_7
[56] FIRRTL:188648 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[0] :
[57] FIRRTL:188649 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_0_br_mask_T = not(io.brupdate.b1.resolve_mask)
[58] FIRRTL:188650 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_0_br_mask_T_1 = and(uops[0].br_mask, _uops_0_br_mask_T)
[59] FIRRTL:188651 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[0].br_mask, _uops_0_br_mask_T_1
[60] FIRRTL:188652 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_1_T = and(io.brupdate.b1.mispredict_mask, uops[1].br_mask)
[61] FIRRTL:188653 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_1_T_1 = neq(_valids_1_T, UInt<1>(0h0))
[62] FIRRTL:188654 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_1_T_2 = or(_valids_1_T_1, UInt<1>(0h0))
[63] FIRRTL:188655 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_1_T_3 = eq(_valids_1_T_2, UInt<1>(0h0))
[64] FIRRTL:188656 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_1_T_4 = and(valids[1], _valids_1_T_3)
[65] FIRRTL:188657 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_1_T_5 = and(io.flush, uops[1].uses_ldq)
[66] FIRRTL:188658 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_1_T_6 = eq(_valids_1_T_5, UInt<1>(0h0))
[67] FIRRTL:188659 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_1_T_7 = and(_valids_1_T_4, _valids_1_T_6)
[68] FIRRTL:188660 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[1], _valids_1_T_7
[69] FIRRTL:188661 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[1] :
[70] FIRRTL:188662 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_1_br_mask_T = not(io.brupdate.b1.resolve_mask)
[71] FIRRTL:188663 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_1_br_mask_T_1 = and(uops[1].br_mask, _uops_1_br_mask_T)
[72] FIRRTL:188664 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[1].br_mask, _uops_1_br_mask_T_1
[73] FIRRTL:188665 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_2_T = and(io.brupdate.b1.mispredict_mask, uops[2].br_mask)
[74] FIRRTL:188666 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_2_T_1 = neq(_valids_2_T, UInt<1>(0h0))
[75] FIRRTL:188667 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_2_T_2 = or(_valids_2_T_1, UInt<1>(0h0))
[76] FIRRTL:188668 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_2_T_3 = eq(_valids_2_T_2, UInt<1>(0h0))
[77] FIRRTL:188669 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_2_T_4 = and(valids[2], _valids_2_T_3)
[78] FIRRTL:188670 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_2_T_5 = and(io.flush, uops[2].uses_ldq)
[79] FIRRTL:188671 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_2_T_6 = eq(_valids_2_T_5, UInt<1>(0h0))
[80] FIRRTL:188672 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_2_T_7 = and(_valids_2_T_4, _valids_2_T_6)
[81] FIRRTL:188673 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[2], _valids_2_T_7
[82] FIRRTL:188674 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[2] :
[83] FIRRTL:188675 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_2_br_mask_T = not(io.brupdate.b1.resolve_mask)
[84] FIRRTL:188676 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_2_br_mask_T_1 = and(uops[2].br_mask, _uops_2_br_mask_T)
[85] FIRRTL:188677 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[2].br_mask, _uops_2_br_mask_T_1
[86] FIRRTL:188678 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_3_T = and(io.brupdate.b1.mispredict_mask, uops[3].br_mask)
[87] FIRRTL:188679 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_3_T_1 = neq(_valids_3_T, UInt<1>(0h0))
[88] FIRRTL:188680 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_3_T_2 = or(_valids_3_T_1, UInt<1>(0h0))
[89] FIRRTL:188681 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_3_T_3 = eq(_valids_3_T_2, UInt<1>(0h0))
[90] FIRRTL:188682 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_3_T_4 = and(valids[3], _valids_3_T_3)
[91] FIRRTL:188683 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_3_T_5 = and(io.flush, uops[3].uses_ldq)
[92] FIRRTL:188684 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_3_T_6 = eq(_valids_3_T_5, UInt<1>(0h0))
[93] FIRRTL:188685 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_3_T_7 = and(_valids_3_T_4, _valids_3_T_6)
[94] FIRRTL:188686 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[3], _valids_3_T_7
[95] FIRRTL:188687 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[3] :
[96] FIRRTL:188688 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_3_br_mask_T = not(io.brupdate.b1.resolve_mask)
[97] FIRRTL:188689 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_3_br_mask_T_1 = and(uops[3].br_mask, _uops_3_br_mask_T)
[98] FIRRTL:188690 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[3].br_mask, _uops_3_br_mask_T_1
[99] FIRRTL:188691 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_4_T = and(io.brupdate.b1.mispredict_mask, uops[4].br_mask)
[100] FIRRTL:188692 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_4_T_1 = neq(_valids_4_T, UInt<1>(0h0))
[101] FIRRTL:188693 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_4_T_2 = or(_valids_4_T_1, UInt<1>(0h0))
[102] FIRRTL:188694 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_4_T_3 = eq(_valids_4_T_2, UInt<1>(0h0))
[103] FIRRTL:188695 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_4_T_4 = and(valids[4], _valids_4_T_3)
[104] FIRRTL:188696 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_4_T_5 = and(io.flush, uops[4].uses_ldq)
[105] FIRRTL:188697 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_4_T_6 = eq(_valids_4_T_5, UInt<1>(0h0))
[106] FIRRTL:188698 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_4_T_7 = and(_valids_4_T_4, _valids_4_T_6)
[107] FIRRTL:188699 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[4], _valids_4_T_7
[108] FIRRTL:188700 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[4] :
[109] FIRRTL:188701 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_4_br_mask_T = not(io.brupdate.b1.resolve_mask)
[110] FIRRTL:188702 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_4_br_mask_T_1 = and(uops[4].br_mask, _uops_4_br_mask_T)
[111] FIRRTL:188703 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[4].br_mask, _uops_4_br_mask_T_1
[112] FIRRTL:188704 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_5_T = and(io.brupdate.b1.mispredict_mask, uops[5].br_mask)
[113] FIRRTL:188705 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_5_T_1 = neq(_valids_5_T, UInt<1>(0h0))
[114] FIRRTL:188706 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_5_T_2 = or(_valids_5_T_1, UInt<1>(0h0))
[115] FIRRTL:188707 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_5_T_3 = eq(_valids_5_T_2, UInt<1>(0h0))
[116] FIRRTL:188708 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_5_T_4 = and(valids[5], _valids_5_T_3)
[117] FIRRTL:188709 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_5_T_5 = and(io.flush, uops[5].uses_ldq)
[118] FIRRTL:188710 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_5_T_6 = eq(_valids_5_T_5, UInt<1>(0h0))
[119] FIRRTL:188711 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_5_T_7 = and(_valids_5_T_4, _valids_5_T_6)
[120] FIRRTL:188712 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[5], _valids_5_T_7
[121] FIRRTL:188713 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[5] :
[122] FIRRTL:188714 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_5_br_mask_T = not(io.brupdate.b1.resolve_mask)
[123] FIRRTL:188715 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_5_br_mask_T_1 = and(uops[5].br_mask, _uops_5_br_mask_T)
[124] FIRRTL:188716 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[5].br_mask, _uops_5_br_mask_T_1
[125] FIRRTL:188717 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_6_T = and(io.brupdate.b1.mispredict_mask, uops[6].br_mask)
[126] FIRRTL:188718 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_6_T_1 = neq(_valids_6_T, UInt<1>(0h0))
[127] FIRRTL:188719 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_6_T_2 = or(_valids_6_T_1, UInt<1>(0h0))
[128] FIRRTL:188720 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_6_T_3 = eq(_valids_6_T_2, UInt<1>(0h0))
[129] FIRRTL:188721 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_6_T_4 = and(valids[6], _valids_6_T_3)
[130] FIRRTL:188722 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_6_T_5 = and(io.flush, uops[6].uses_ldq)
[131] FIRRTL:188723 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_6_T_6 = eq(_valids_6_T_5, UInt<1>(0h0))
[132] FIRRTL:188724 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_6_T_7 = and(_valids_6_T_4, _valids_6_T_6)
[133] FIRRTL:188725 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[6], _valids_6_T_7
[134] FIRRTL:188726 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[6] :
[135] FIRRTL:188727 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_6_br_mask_T = not(io.brupdate.b1.resolve_mask)
[136] FIRRTL:188728 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_6_br_mask_T_1 = and(uops[6].br_mask, _uops_6_br_mask_T)
[137] FIRRTL:188729 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[6].br_mask, _uops_6_br_mask_T_1
[138] FIRRTL:188730 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_7_T = and(io.brupdate.b1.mispredict_mask, uops[7].br_mask)
[139] FIRRTL:188731 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_7_T_1 = neq(_valids_7_T, UInt<1>(0h0))
[140] FIRRTL:188732 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_7_T_2 = or(_valids_7_T_1, UInt<1>(0h0))
[141] FIRRTL:188733 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_7_T_3 = eq(_valids_7_T_2, UInt<1>(0h0))
[142] FIRRTL:188734 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_7_T_4 = and(valids[7], _valids_7_T_3)
[143] FIRRTL:188735 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_7_T_5 = and(io.flush, uops[7].uses_ldq)
[144] FIRRTL:188736 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_7_T_6 = eq(_valids_7_T_5, UInt<1>(0h0))
[145] FIRRTL:188737 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_7_T_7 = and(_valids_7_T_4, _valids_7_T_6)
[146] FIRRTL:188738 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[7], _valids_7_T_7
[147] FIRRTL:188739 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[7] :
[148] FIRRTL:188740 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_7_br_mask_T = not(io.brupdate.b1.resolve_mask)
[149] FIRRTL:188741 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_7_br_mask_T_1 = and(uops[7].br_mask, _uops_7_br_mask_T)
[150] FIRRTL:188742 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[7].br_mask, _uops_7_br_mask_T_1
[151] FIRRTL:188743 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_8_T = and(io.brupdate.b1.mispredict_mask, uops[8].br_mask)
[152] FIRRTL:188744 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_8_T_1 = neq(_valids_8_T, UInt<1>(0h0))
[153] FIRRTL:188745 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_8_T_2 = or(_valids_8_T_1, UInt<1>(0h0))
[154] FIRRTL:188746 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_8_T_3 = eq(_valids_8_T_2, UInt<1>(0h0))
[155] FIRRTL:188747 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_8_T_4 = and(valids[8], _valids_8_T_3)
[156] FIRRTL:188748 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_8_T_5 = and(io.flush, uops[8].uses_ldq)
[157] FIRRTL:188749 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_8_T_6 = eq(_valids_8_T_5, UInt<1>(0h0))
[158] FIRRTL:188750 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_8_T_7 = and(_valids_8_T_4, _valids_8_T_6)
[159] FIRRTL:188751 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[8], _valids_8_T_7
[160] FIRRTL:188752 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[8] :
[161] FIRRTL:188753 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_8_br_mask_T = not(io.brupdate.b1.resolve_mask)
[162] FIRRTL:188754 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_8_br_mask_T_1 = and(uops[8].br_mask, _uops_8_br_mask_T)
[163] FIRRTL:188755 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[8].br_mask, _uops_8_br_mask_T_1
[164] FIRRTL:188756 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_9_T = and(io.brupdate.b1.mispredict_mask, uops[9].br_mask)
[165] FIRRTL:188757 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_9_T_1 = neq(_valids_9_T, UInt<1>(0h0))
[166] FIRRTL:188758 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_9_T_2 = or(_valids_9_T_1, UInt<1>(0h0))
[167] FIRRTL:188759 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_9_T_3 = eq(_valids_9_T_2, UInt<1>(0h0))
[168] FIRRTL:188760 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_9_T_4 = and(valids[9], _valids_9_T_3)
[169] FIRRTL:188761 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_9_T_5 = and(io.flush, uops[9].uses_ldq)
[170] FIRRTL:188762 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_9_T_6 = eq(_valids_9_T_5, UInt<1>(0h0))
[171] FIRRTL:188763 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_9_T_7 = and(_valids_9_T_4, _valids_9_T_6)
[172] FIRRTL:188764 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[9], _valids_9_T_7
[173] FIRRTL:188765 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[9] :
[174] FIRRTL:188766 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_9_br_mask_T = not(io.brupdate.b1.resolve_mask)
[175] FIRRTL:188767 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_9_br_mask_T_1 = and(uops[9].br_mask, _uops_9_br_mask_T)
[176] FIRRTL:188768 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[9].br_mask, _uops_9_br_mask_T_1
[177] FIRRTL:188769 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_10_T = and(io.brupdate.b1.mispredict_mask, uops[10].br_mask)
[178] FIRRTL:188770 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_10_T_1 = neq(_valids_10_T, UInt<1>(0h0))
[179] FIRRTL:188771 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_10_T_2 = or(_valids_10_T_1, UInt<1>(0h0))
[180] FIRRTL:188772 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_10_T_3 = eq(_valids_10_T_2, UInt<1>(0h0))
[181] FIRRTL:188773 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_10_T_4 = and(valids[10], _valids_10_T_3)
[182] FIRRTL:188774 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_10_T_5 = and(io.flush, uops[10].uses_ldq)
[183] FIRRTL:188775 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_10_T_6 = eq(_valids_10_T_5, UInt<1>(0h0))
[184] FIRRTL:188776 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_10_T_7 = and(_valids_10_T_4, _valids_10_T_6)
[185] FIRRTL:188777 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[10], _valids_10_T_7
[186] FIRRTL:188778 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[10] :
[187] FIRRTL:188779 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_10_br_mask_T = not(io.brupdate.b1.resolve_mask)
[188] FIRRTL:188780 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_10_br_mask_T_1 = and(uops[10].br_mask, _uops_10_br_mask_T)
[189] FIRRTL:188781 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[10].br_mask, _uops_10_br_mask_T_1
[190] FIRRTL:188782 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_11_T = and(io.brupdate.b1.mispredict_mask, uops[11].br_mask)
[191] FIRRTL:188783 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_11_T_1 = neq(_valids_11_T, UInt<1>(0h0))
[192] FIRRTL:188784 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_11_T_2 = or(_valids_11_T_1, UInt<1>(0h0))
[193] FIRRTL:188785 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_11_T_3 = eq(_valids_11_T_2, UInt<1>(0h0))
[194] FIRRTL:188786 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_11_T_4 = and(valids[11], _valids_11_T_3)
[195] FIRRTL:188787 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_11_T_5 = and(io.flush, uops[11].uses_ldq)
[196] FIRRTL:188788 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_11_T_6 = eq(_valids_11_T_5, UInt<1>(0h0))
[197] FIRRTL:188789 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_11_T_7 = and(_valids_11_T_4, _valids_11_T_6)
[198] FIRRTL:188790 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[11], _valids_11_T_7
[199] FIRRTL:188791 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[11] :
[200] FIRRTL:188792 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_11_br_mask_T = not(io.brupdate.b1.resolve_mask)
[201] FIRRTL:188793 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_11_br_mask_T_1 = and(uops[11].br_mask, _uops_11_br_mask_T)
[202] FIRRTL:188794 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[11].br_mask, _uops_11_br_mask_T_1
[203] FIRRTL:188795 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_12_T = and(io.brupdate.b1.mispredict_mask, uops[12].br_mask)
[204] FIRRTL:188796 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_12_T_1 = neq(_valids_12_T, UInt<1>(0h0))
[205] FIRRTL:188797 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_12_T_2 = or(_valids_12_T_1, UInt<1>(0h0))
[206] FIRRTL:188798 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_12_T_3 = eq(_valids_12_T_2, UInt<1>(0h0))
[207] FIRRTL:188799 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_12_T_4 = and(valids[12], _valids_12_T_3)
[208] FIRRTL:188800 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_12_T_5 = and(io.flush, uops[12].uses_ldq)
[209] FIRRTL:188801 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_12_T_6 = eq(_valids_12_T_5, UInt<1>(0h0))
[210] FIRRTL:188802 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_12_T_7 = and(_valids_12_T_4, _valids_12_T_6)
[211] FIRRTL:188803 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[12], _valids_12_T_7
[212] FIRRTL:188804 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[12] :
[213] FIRRTL:188805 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_12_br_mask_T = not(io.brupdate.b1.resolve_mask)
[214] FIRRTL:188806 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_12_br_mask_T_1 = and(uops[12].br_mask, _uops_12_br_mask_T)
[215] FIRRTL:188807 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[12].br_mask, _uops_12_br_mask_T_1
[216] FIRRTL:188808 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_13_T = and(io.brupdate.b1.mispredict_mask, uops[13].br_mask)
[217] FIRRTL:188809 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_13_T_1 = neq(_valids_13_T, UInt<1>(0h0))
[218] FIRRTL:188810 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_13_T_2 = or(_valids_13_T_1, UInt<1>(0h0))
[219] FIRRTL:188811 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_13_T_3 = eq(_valids_13_T_2, UInt<1>(0h0))
[220] FIRRTL:188812 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_13_T_4 = and(valids[13], _valids_13_T_3)
[221] FIRRTL:188813 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_13_T_5 = and(io.flush, uops[13].uses_ldq)
[222] FIRRTL:188814 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_13_T_6 = eq(_valids_13_T_5, UInt<1>(0h0))
[223] FIRRTL:188815 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_13_T_7 = and(_valids_13_T_4, _valids_13_T_6)
[224] FIRRTL:188816 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[13], _valids_13_T_7
[225] FIRRTL:188817 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[13] :
[226] FIRRTL:188818 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_13_br_mask_T = not(io.brupdate.b1.resolve_mask)
[227] FIRRTL:188819 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_13_br_mask_T_1 = and(uops[13].br_mask, _uops_13_br_mask_T)
[228] FIRRTL:188820 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[13].br_mask, _uops_13_br_mask_T_1
[229] FIRRTL:188821 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_14_T = and(io.brupdate.b1.mispredict_mask, uops[14].br_mask)
[230] FIRRTL:188822 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_14_T_1 = neq(_valids_14_T, UInt<1>(0h0))
[231] FIRRTL:188823 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_14_T_2 = or(_valids_14_T_1, UInt<1>(0h0))
[232] FIRRTL:188824 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_14_T_3 = eq(_valids_14_T_2, UInt<1>(0h0))
[233] FIRRTL:188825 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_14_T_4 = and(valids[14], _valids_14_T_3)
[234] FIRRTL:188826 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_14_T_5 = and(io.flush, uops[14].uses_ldq)
[235] FIRRTL:188827 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_14_T_6 = eq(_valids_14_T_5, UInt<1>(0h0))
[236] FIRRTL:188828 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_14_T_7 = and(_valids_14_T_4, _valids_14_T_6)
[237] FIRRTL:188829 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[14], _valids_14_T_7
[238] FIRRTL:188830 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[14] :
[239] FIRRTL:188831 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_14_br_mask_T = not(io.brupdate.b1.resolve_mask)
[240] FIRRTL:188832 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_14_br_mask_T_1 = and(uops[14].br_mask, _uops_14_br_mask_T)
[241] FIRRTL:188833 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[14].br_mask, _uops_14_br_mask_T_1
[242] FIRRTL:188834 SRC:generators/boom/src/main/scala/v4/util/util.scala:545:19 KIND:when :: when do_enq :
[243] FIRRTL:188835 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:10 KIND:infer_mport :: infer mport MPORT = ram[enq_ptr_value], clock
[244] FIRRTL:188836 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:35 KIND:connect :: connect MPORT, io.enq.bits
[245] FIRRTL:188837 SRC:generators/boom/src/main/scala/v4/util/util.scala:547:35 KIND:connect :: connect valids[enq_ptr_value], UInt<1>(0h1)
[246] FIRRTL:188838 SRC:generators/boom/src/main/scala/v4/util/util.scala:548:35 KIND:connect :: connect uops[enq_ptr_value], io.enq.bits.uop
[247] FIRRTL:188839 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _uops_br_mask_T = not(io.brupdate.b1.resolve_mask)
[248] FIRRTL:188840 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _uops_br_mask_T_1 = and(io.enq.bits.uop.br_mask, _uops_br_mask_T)
[249] FIRRTL:188841 SRC:generators/boom/src/main/scala/v4/util/util.scala:549:35 KIND:connect :: connect uops[enq_ptr_value].br_mask, _uops_br_mask_T_1
[250] FIRRTL:188842 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap = eq(enq_ptr_value, UInt<4>(0he))
[251] FIRRTL:188843 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T = add(enq_ptr_value, UInt<1>(0h1))
[252] FIRRTL:188844 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_1 = tail(_value_T, 1)
[253] FIRRTL:188845 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect enq_ptr_value, _value_T_1
[254] FIRRTL:188846 SRC:src/main/scala/chisel3/util/Counter.scala:87:20 KIND:when :: when wrap :
[255] FIRRTL:188847 SRC:src/main/scala/chisel3/util/Counter.scala:87:28 KIND:connect :: connect enq_ptr_value, UInt<1>(0h0)
[256] FIRRTL:188848 SRC:generators/boom/src/main/scala/v4/util/util.scala:553:19 KIND:when :: when do_deq :
[257] FIRRTL:188849 SRC:generators/boom/src/main/scala/v4/util/util.scala:554:29 KIND:connect :: connect valids[deq_ptr_value], UInt<1>(0h0)
[258] FIRRTL:188850 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap_1 = eq(deq_ptr_value, UInt<4>(0he))
[259] FIRRTL:188851 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_2 = add(deq_ptr_value, UInt<1>(0h1))
[260] FIRRTL:188852 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_3 = tail(_value_T_2, 1)
[261] FIRRTL:188853 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect deq_ptr_value, _value_T_3
[262] FIRRTL:188854 SRC:src/main/scala/chisel3/util/Counter.scala:87:20 KIND:when :: when wrap_1 :
[263] FIRRTL:188855 SRC:src/main/scala/chisel3/util/Counter.scala:87:28 KIND:connect :: connect deq_ptr_value, UInt<1>(0h0)
[264] FIRRTL:188856 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:18 KIND:node :: node _T = neq(do_enq, do_deq)
[265] FIRRTL:188857 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:30 KIND:when :: when _T :
[266] FIRRTL:188858 SRC:generators/boom/src/main/scala/v4/util/util.scala:559:18 KIND:connect :: connect maybe_full, do_enq
[267] FIRRTL:188859 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:21 KIND:node :: node _io_enq_ready_T = eq(full, UInt<1>(0h0))
[268] FIRRTL:188860 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:18 KIND:connect :: connect io.enq.ready, _io_enq_ready_T
[269] FIRRTL:188861 SRC:generators/boom/src/main/scala/v4/util/util.scala:564:19 KIND:wire :: wire out : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>, tag_match : UInt<1>, old_meta : { coh : { state : UInt<2>}, tag : UInt<20>}, way_en : UInt<4>, sdq_id : UInt<5>}
[270] FIRRTL:188862 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:27 KIND:infer_mport :: infer mport out_MPORT = ram[deq_ptr_value], clock
[271] FIRRTL:188863 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:21 KIND:connect :: connect out, out_MPORT
[272] FIRRTL:188864 SRC:generators/boom/src/main/scala/v4/util/util.scala:566:21 KIND:connect :: connect out.uop, uops[deq_ptr_value]
[273] FIRRTL:188865 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:32 KIND:node :: node _io_deq_valid_T = eq(io.empty, UInt<1>(0h0))
[274] FIRRTL:188866 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:42 KIND:node :: node _io_deq_valid_T_1 = and(_io_deq_valid_T, valids[deq_ptr_value])
[275] FIRRTL:188867 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:29 KIND:connect :: connect io.deq.valid, _io_deq_valid_T_1
[276] FIRRTL:188868 SRC:generators/boom/src/main/scala/v4/util/util.scala:568:29 KIND:connect :: connect io.deq.bits, out
[277] FIRRTL:188869 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node _ptr_diff_T = sub(enq_ptr_value, deq_ptr_value)
[278] FIRRTL:188870 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node ptr_diff = tail(_ptr_diff_T, 1)
[279] FIRRTL:188871 SRC:generators/boom/src/main/scala/v4/util/util.scala:576:12 KIND:node :: node _io_count_T = mux(maybe_full, UInt<4>(0hf), UInt<1>(0h0))
[280] FIRRTL:188872 SRC:generators/boom/src/main/scala/v4/util/util.scala:578:27 KIND:node :: node _io_count_T_1 = gt(deq_ptr_value, enq_ptr_value)
[281] FIRRTL:188873 SRC:generators/boom/src/main/scala/v4/util/util.scala:579:26 KIND:node :: node _io_count_T_2 = add(UInt<4>(0hf), ptr_diff)
[282] FIRRTL:188874 SRC:generators/boom/src/main/scala/v4/util/util.scala:579:26 KIND:node :: node _io_count_T_3 = tail(_io_count_T_2, 1)
[283] FIRRTL:188875 SRC:generators/boom/src/main/scala/v4/util/util.scala:578:12 KIND:node :: node _io_count_T_4 = mux(_io_count_T_1, _io_count_T_3, ptr_diff)
[284] FIRRTL:188876 SRC:generators/boom/src/main/scala/v4/util/util.scala:575:22 KIND:node :: node _io_count_T_5 = mux(ptr_match, _io_count_T, _io_count_T_4)
[285] FIRRTL:188877 SRC:generators/boom/src/main/scala/v4/util/util.scala:575:16 KIND:connect :: connect io.count, _io_count_T_5
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
  "task_id": "leaf_abstraction-BoomMSHR.rpq.main-30765c6beda665d8",
  "work_unit_id": "BoomMSHR.rpq.main",
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
