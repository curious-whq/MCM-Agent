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

Task ID: `leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.9`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomMSHRFile.respq`
- module: `BranchKillableQueue_4`
- kind: `module`
- instance path: `BoomMSHRFile.respq`
- leaf: `True`
- coverage complete: `True`
- raw statements: 124
- logical statements: 54
- mapped/logical source lines: 39
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

- `BoomMSHRFile.respq::io.deq.fire`
  - predicate: `io.deq.valid && io.deq.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'valids']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']
- `BoomMSHRFile.respq::io.enq.fire`
  - predicate: `io.enq.valid && io.enq.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.enq.bits.data', 'io.enq.bits.is_hella', 'io.enq.bits.uop.bp_debug_if', 'io.enq.bits.uop.bp_xcpt_if', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.br_tag', 'io.enq.bits.uop.br_type', 'io.enq.bits.uop.csr_cmd', 'io.enq.bits.uop.debug_fsrc', 'io.enq.bits.uop.debug_inst', 'io.enq.bits.uop.debug_pc', 'io.enq.bits.uop.debug_tsrc', 'io.enq.bits.uop.dis_col_sel', 'io.enq.bits.uop.dst_rtype', 'io.enq.bits.uop.edge_inst', 'io.enq.bits.uop.exc_cause', 'io.enq.bits.uop.exception', 'io.enq.bits.uop.fcn_dw', 'io.enq.bits.uop.fcn_op', 'io.enq.bits.uop.flush_on_commit', 'io.enq.bits.uop.fp_ctrl.div', 'io.enq.bits.uop.fp_ctrl.fastpipe', 'io.enq.bits.uop.fp_ctrl.fma', 'io.enq.bits.uop.fp_ctrl.fromint', 'io.enq.bits.uop.fp_ctrl.ldst', 'io.enq.bits.uop.fp_ctrl.ren1', 'io.enq.bits.uop.fp_ctrl.ren2', 'io.enq.bits.uop.fp_ctrl.ren3', 'io.enq.bits.uop.fp_ctrl.sqrt', 'io.enq.bits.uop.fp_ctrl.swap12', 'io.enq.bits.uop.fp_ctrl.swap23', 'io.enq.bits.uop.fp_ctrl.toint', 'io.enq.bits.uop.fp_ctrl.typeTagIn', 'io.enq.bits.uop.fp_ctrl.typeTagOut', 'io.enq.bits.uop.fp_ctrl.vec', 'io.enq.bits.uop.fp_ctrl.wen', 'io.enq.bits.uop.fp_ctrl.wflags', 'io.enq.bits.uop.fp_rm', 'io.enq.bits.uop.fp_typ', 'io.enq.bits.uop.fp_val', 'io.enq.bits.uop.frs3_en', 'io.enq.bits.uop.ftq_idx', 'io.enq.bits.uop.fu_code[0]', 'io.enq.bits.uop.fu_code[1]', 'io.enq.bits.uop.fu_code[2]', 'io.enq.bits.uop.fu_code[3]', 'io.enq.bits.uop.fu_code[4]', 'io.enq.bits.uop.fu_code[5]', 'io.enq.bits.uop.fu_code[6]', 'io.enq.bits.uop.fu_code[7]', 'io.enq.bits.uop.fu_code[8]', 'io.enq.bits.uop.fu_code[9]', 'io.enq.bits.uop.imm_packed', 'io.enq.bits.uop.imm_rename', 'io.enq.bits.uop.imm_sel', 'io.enq.bits.uop.inst', 'io.enq.bits.uop.iq_type[0]', 'io.enq.bits.uop.iq_type[1]', 'io.enq.bits.uop.iq_type[2]', 'io.enq.bits.uop.iq_type[3]', 'io.enq.bits.uop.is_amo', 'io.enq.bits.uop.is_eret', 'io.enq.bits.uop.is_fence', 'io.enq.bits.uop.is_fencei', 'io.enq.bits.uop.is_mov', 'io.enq.bits.uop.is_rocc', 'io.enq.bits.uop.is_rvc', 'io.enq.bits.uop.is_sfb', 'io.enq.bits.uop.is_sfence', 'io.enq.bits.uop.is_sys_pc2epc', 'io.enq.bits.uop.is_unique', 'io.enq.bits.uop.iw_issued', 'io.enq.bits.uop.iw_issued_partial_agen', 'io.enq.bits.uop.iw_issued_partial_dgen', 'io.enq.bits.uop.iw_p1_bypass_hint', 'io.enq.bits.uop.iw_p1_speculative_child', 'io.enq.bits.uop.iw_p2_bypass_hint', 'io.enq.bits.uop.iw_p2_speculative_child', 'io.enq.bits.uop.iw_p3_bypass_hint', 'io.enq.bits.uop.ldq_idx', 'io.enq.bits.uop.ldst', 'io.enq.bits.uop.ldst_is_rs1', 'io.enq.bits.uop.lrs1', 'io.enq.bits.uop.lrs1_rtype', 'io.enq.bits.uop.lrs2', 'io.enq.bits.uop.lrs2_rtype', 'io.enq.bits.uop.lrs3', 'io.enq.bits.uop.mem_cmd', 'io.enq.bits.uop.mem_signed', 'io.enq.bits.uop.mem_size', 'io.enq.bits.uop.op1_sel', 'io.enq.bits.uop.op2_sel', 'io.enq.bits.uop.pc_lob', 'io.enq.bits.uop.pdst', 'io.enq.bits.uop.pimm', 'io.enq.bits.uop.ppred', 'io.enq.bits.uop.ppred_busy', 'io.enq.bits.uop.prs1', 'io.enq.bits.uop.prs1_busy', 'io.enq.bits.uop.prs2', 'io.enq.bits.uop.prs2_busy', 'io.enq.bits.uop.prs3', 'io.enq.bits.uop.prs3_busy', 'io.enq.bits.uop.rob_idx', 'io.enq.bits.uop.rxq_idx', 'io.enq.bits.uop.stale_pdst', 'io.enq.bits.uop.stq_idx', 'io.enq.bits.uop.taken', 'io.enq.bits.uop.uses_ldq', 'io.enq.bits.uop.uses_stq', 'io.enq.bits.uop.xcpt_ae_if', 'io.enq.bits.uop.xcpt_ma_if', 'io.enq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Concrete local state

['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Environment/frontier signals

['clock', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.count', 'io.deq.bits.data', 'io.deq.bits.is_hella', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.ready', 'io.deq.valid', 'io.empty', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.uses_ldq', 'io.enq.ready', 'io.enq.valid', 'io.flush']

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

### generators/boom/src/main/scala/v4/util/util.scala:561-573
```scala

    io.enq.ready := !full

    val out = Wire(gen)
    out             := ram(deq_ptr.value)
    out.uop         := uops(deq_ptr.value)
    io.deq.valid            := !io.empty && valids(deq_ptr.value)
    io.deq.bits             := out

    val ptr_diff = enq_ptr.value - deq_ptr.value
    if (isPow2(entries)) {
      io.count := Cat(maybe_full && ptr_match, ptr_diff)
    }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:195635 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input clock : Clock
[1] FIRRTL:195636 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input reset : Reset
[2] FIRRTL:195637 SRC:generators/boom/src/main/scala/v4/util/util.scala:482:14 KIND:structural :: output io : { flip enq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip flush : UInt<1>, empty : UInt<1>, count : UInt<2>}
[3] FIRRTL:195639 SRC:generators/boom/src/main/scala/v4/util/util.scala:522:22 KIND:memory :: cmem ram : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>} [4]
[4] FIRRTL:195640 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:wire :: wire _valids_WIRE : UInt<1>[4]
[5] FIRRTL:195641 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[0], UInt<1>(0h0)
[6] FIRRTL:195642 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[1], UInt<1>(0h0)
[7] FIRRTL:195643 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[2], UInt<1>(0h0)
[8] FIRRTL:195644 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[3], UInt<1>(0h0)
[9] FIRRTL:195645 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:26 KIND:regreset :: regreset valids : UInt<1>[4], clock, reset, _valids_WIRE
[10] FIRRTL:195646 SRC:generators/boom/src/main/scala/v4/util/util.scala:524:22 KIND:reg :: reg uops : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}[4], clock
[11] FIRRTL:195647 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset enq_ptr_value : UInt<2>, clock, reset, UInt<2>(0h0)
[12] FIRRTL:195648 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset deq_ptr_value : UInt<2>, clock, reset, UInt<2>(0h0)
[13] FIRRTL:195649 SRC:generators/boom/src/main/scala/v4/util/util.scala:528:29 KIND:regreset :: regreset maybe_full : UInt<1>, clock, reset, UInt<1>(0h0)
[14] FIRRTL:195650 SRC:generators/boom/src/main/scala/v4/util/util.scala:530:35 KIND:node :: node ptr_match = eq(enq_ptr_value, deq_ptr_value)
[15] FIRRTL:195651 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:30 KIND:node :: node _io_empty_T = eq(maybe_full, UInt<1>(0h0))
[16] FIRRTL:195652 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:27 KIND:node :: node _io_empty_T_1 = and(ptr_match, _io_empty_T)
[17] FIRRTL:195653 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:14 KIND:connect :: connect io.empty, _io_empty_T_1
[18] FIRRTL:195654 SRC:generators/boom/src/main/scala/v4/util/util.scala:532:26 KIND:node :: node full = and(ptr_match, maybe_full)
[19] FIRRTL:195655 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _do_enq_T = and(io.enq.ready, io.enq.valid)
[20] FIRRTL:195656 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _do_enq_T_1 = and(io.brupdate.b1.mispredict_mask, io.enq.bits.uop.br_mask)
[21] FIRRTL:195657 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _do_enq_T_2 = neq(_do_enq_T_1, UInt<1>(0h0))
[22] FIRRTL:195658 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _do_enq_T_3 = or(_do_enq_T_2, UInt<1>(0h0))
[23] FIRRTL:195659 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:42 KIND:node :: node _do_enq_T_4 = eq(_do_enq_T_3, UInt<1>(0h0))
[24] FIRRTL:195660 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:39 KIND:node :: node _do_enq_T_5 = and(_do_enq_T, _do_enq_T_4)
[25] FIRRTL:195661 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:113 KIND:node :: node _do_enq_T_6 = and(io.flush, io.enq.bits.uop.uses_ldq)
[26] FIRRTL:195662 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:102 KIND:node :: node _do_enq_T_7 = eq(_do_enq_T_6, UInt<1>(0h0))
[27] FIRRTL:195663 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:99 KIND:node :: node _do_enq_T_8 = and(_do_enq_T_5, _do_enq_T_7)
[28] FIRRTL:195664 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:wire :: wire do_enq : UInt<1>
[29] FIRRTL:195665 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:connect :: connect do_enq, _do_enq_T_8
[30] FIRRTL:195666 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:44 KIND:node :: node _do_deq_T = eq(valids[deq_ptr_value], UInt<1>(0h0))
[31] FIRRTL:195667 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:41 KIND:node :: node _do_deq_T_1 = or(io.deq.ready, _do_deq_T)
[32] FIRRTL:195668 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:71 KIND:node :: node _do_deq_T_2 = eq(io.empty, UInt<1>(0h0))
[33] FIRRTL:195669 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:68 KIND:node :: node _do_deq_T_3 = and(_do_deq_T_1, _do_deq_T_2)
[34] FIRRTL:195670 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:wire :: wire do_deq : UInt<1>
[35] FIRRTL:195671 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:connect :: connect do_deq, _do_deq_T_3
[36] FIRRTL:195672 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_0_T = and(io.brupdate.b1.mispredict_mask, uops[0].br_mask)
[37] FIRRTL:195673 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_0_T_1 = neq(_valids_0_T, UInt<1>(0h0))
[38] FIRRTL:195674 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_0_T_2 = or(_valids_0_T_1, UInt<1>(0h0))
[39] FIRRTL:195675 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_0_T_3 = eq(_valids_0_T_2, UInt<1>(0h0))
[40] FIRRTL:195676 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_0_T_4 = and(valids[0], _valids_0_T_3)
[41] FIRRTL:195677 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_0_T_5 = and(io.flush, uops[0].uses_ldq)
[42] FIRRTL:195678 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_0_T_6 = eq(_valids_0_T_5, UInt<1>(0h0))
[43] FIRRTL:195679 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_0_T_7 = and(_valids_0_T_4, _valids_0_T_6)
[44] FIRRTL:195680 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[0], _valids_0_T_7
[45] FIRRTL:195681 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[0] :
[46] FIRRTL:195682 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_0_br_mask_T = not(io.brupdate.b1.resolve_mask)
[47] FIRRTL:195683 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_0_br_mask_T_1 = and(uops[0].br_mask, _uops_0_br_mask_T)
[48] FIRRTL:195684 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[0].br_mask, _uops_0_br_mask_T_1
[49] FIRRTL:195685 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_1_T = and(io.brupdate.b1.mispredict_mask, uops[1].br_mask)
[50] FIRRTL:195686 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_1_T_1 = neq(_valids_1_T, UInt<1>(0h0))
[51] FIRRTL:195687 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_1_T_2 = or(_valids_1_T_1, UInt<1>(0h0))
[52] FIRRTL:195688 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_1_T_3 = eq(_valids_1_T_2, UInt<1>(0h0))
[53] FIRRTL:195689 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_1_T_4 = and(valids[1], _valids_1_T_3)
[54] FIRRTL:195690 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_1_T_5 = and(io.flush, uops[1].uses_ldq)
[55] FIRRTL:195691 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_1_T_6 = eq(_valids_1_T_5, UInt<1>(0h0))
[56] FIRRTL:195692 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_1_T_7 = and(_valids_1_T_4, _valids_1_T_6)
[57] FIRRTL:195693 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[1], _valids_1_T_7
[58] FIRRTL:195694 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[1] :
[59] FIRRTL:195695 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_1_br_mask_T = not(io.brupdate.b1.resolve_mask)
[60] FIRRTL:195696 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_1_br_mask_T_1 = and(uops[1].br_mask, _uops_1_br_mask_T)
[61] FIRRTL:195697 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[1].br_mask, _uops_1_br_mask_T_1
[62] FIRRTL:195698 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_2_T = and(io.brupdate.b1.mispredict_mask, uops[2].br_mask)
[63] FIRRTL:195699 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_2_T_1 = neq(_valids_2_T, UInt<1>(0h0))
[64] FIRRTL:195700 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_2_T_2 = or(_valids_2_T_1, UInt<1>(0h0))
[65] FIRRTL:195701 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_2_T_3 = eq(_valids_2_T_2, UInt<1>(0h0))
[66] FIRRTL:195702 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_2_T_4 = and(valids[2], _valids_2_T_3)
[67] FIRRTL:195703 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_2_T_5 = and(io.flush, uops[2].uses_ldq)
[68] FIRRTL:195704 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_2_T_6 = eq(_valids_2_T_5, UInt<1>(0h0))
[69] FIRRTL:195705 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_2_T_7 = and(_valids_2_T_4, _valids_2_T_6)
[70] FIRRTL:195706 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[2], _valids_2_T_7
[71] FIRRTL:195707 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[2] :
[72] FIRRTL:195708 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_2_br_mask_T = not(io.brupdate.b1.resolve_mask)
[73] FIRRTL:195709 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_2_br_mask_T_1 = and(uops[2].br_mask, _uops_2_br_mask_T)
[74] FIRRTL:195710 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[2].br_mask, _uops_2_br_mask_T_1
[75] FIRRTL:195711 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_3_T = and(io.brupdate.b1.mispredict_mask, uops[3].br_mask)
[76] FIRRTL:195712 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_3_T_1 = neq(_valids_3_T, UInt<1>(0h0))
[77] FIRRTL:195713 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_3_T_2 = or(_valids_3_T_1, UInt<1>(0h0))
[78] FIRRTL:195714 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_3_T_3 = eq(_valids_3_T_2, UInt<1>(0h0))
[79] FIRRTL:195715 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_3_T_4 = and(valids[3], _valids_3_T_3)
[80] FIRRTL:195716 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_3_T_5 = and(io.flush, uops[3].uses_ldq)
[81] FIRRTL:195717 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_3_T_6 = eq(_valids_3_T_5, UInt<1>(0h0))
[82] FIRRTL:195718 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_3_T_7 = and(_valids_3_T_4, _valids_3_T_6)
[83] FIRRTL:195719 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[3], _valids_3_T_7
[84] FIRRTL:195720 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[3] :
[85] FIRRTL:195721 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_3_br_mask_T = not(io.brupdate.b1.resolve_mask)
[86] FIRRTL:195722 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_3_br_mask_T_1 = and(uops[3].br_mask, _uops_3_br_mask_T)
[87] FIRRTL:195723 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[3].br_mask, _uops_3_br_mask_T_1
[88] FIRRTL:195724 SRC:generators/boom/src/main/scala/v4/util/util.scala:545:19 KIND:when :: when do_enq :
[89] FIRRTL:195725 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:10 KIND:infer_mport :: infer mport MPORT = ram[enq_ptr_value], clock
[90] FIRRTL:195726 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:35 KIND:connect :: connect MPORT, io.enq.bits
[91] FIRRTL:195727 SRC:generators/boom/src/main/scala/v4/util/util.scala:547:35 KIND:connect :: connect valids[enq_ptr_value], UInt<1>(0h1)
[92] FIRRTL:195728 SRC:generators/boom/src/main/scala/v4/util/util.scala:548:35 KIND:connect :: connect uops[enq_ptr_value], io.enq.bits.uop
[93] FIRRTL:195729 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _uops_br_mask_T = not(io.brupdate.b1.resolve_mask)
[94] FIRRTL:195730 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _uops_br_mask_T_1 = and(io.enq.bits.uop.br_mask, _uops_br_mask_T)
[95] FIRRTL:195731 SRC:generators/boom/src/main/scala/v4/util/util.scala:549:35 KIND:connect :: connect uops[enq_ptr_value].br_mask, _uops_br_mask_T_1
[96] FIRRTL:195732 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap = eq(enq_ptr_value, UInt<2>(0h3))
[97] FIRRTL:195733 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T = add(enq_ptr_value, UInt<1>(0h1))
[98] FIRRTL:195734 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_1 = tail(_value_T, 1)
[99] FIRRTL:195735 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect enq_ptr_value, _value_T_1
[100] FIRRTL:195736 SRC:generators/boom/src/main/scala/v4/util/util.scala:553:19 KIND:when :: when do_deq :
[101] FIRRTL:195737 SRC:generators/boom/src/main/scala/v4/util/util.scala:554:29 KIND:connect :: connect valids[deq_ptr_value], UInt<1>(0h0)
[102] FIRRTL:195738 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap_1 = eq(deq_ptr_value, UInt<2>(0h3))
[103] FIRRTL:195739 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_2 = add(deq_ptr_value, UInt<1>(0h1))
[104] FIRRTL:195740 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_3 = tail(_value_T_2, 1)
[105] FIRRTL:195741 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect deq_ptr_value, _value_T_3
[106] FIRRTL:195742 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:18 KIND:node :: node _T = neq(do_enq, do_deq)
[107] FIRRTL:195743 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:30 KIND:when :: when _T :
[108] FIRRTL:195744 SRC:generators/boom/src/main/scala/v4/util/util.scala:559:18 KIND:connect :: connect maybe_full, do_enq
[109] FIRRTL:195745 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:21 KIND:node :: node _io_enq_ready_T = eq(full, UInt<1>(0h0))
[110] FIRRTL:195746 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:18 KIND:connect :: connect io.enq.ready, _io_enq_ready_T
[111] FIRRTL:195747 SRC:generators/boom/src/main/scala/v4/util/util.scala:564:19 KIND:wire :: wire out : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}
[112] FIRRTL:195748 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:27 KIND:infer_mport :: infer mport out_MPORT = ram[deq_ptr_value], clock
[113] FIRRTL:195749 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:21 KIND:connect :: connect out, out_MPORT
[114] FIRRTL:195750 SRC:generators/boom/src/main/scala/v4/util/util.scala:566:21 KIND:connect :: connect out.uop, uops[deq_ptr_value]
[115] FIRRTL:195751 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:32 KIND:node :: node _io_deq_valid_T = eq(io.empty, UInt<1>(0h0))
[116] FIRRTL:195752 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:42 KIND:node :: node _io_deq_valid_T_1 = and(_io_deq_valid_T, valids[deq_ptr_value])
[117] FIRRTL:195753 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:29 KIND:connect :: connect io.deq.valid, _io_deq_valid_T_1
[118] FIRRTL:195754 SRC:generators/boom/src/main/scala/v4/util/util.scala:568:29 KIND:connect :: connect io.deq.bits, out
[119] FIRRTL:195755 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node _ptr_diff_T = sub(enq_ptr_value, deq_ptr_value)
[120] FIRRTL:195756 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node ptr_diff = tail(_ptr_diff_T, 1)
[121] FIRRTL:195757 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:34 KIND:node :: node _io_count_T = and(maybe_full, ptr_match)
[122] FIRRTL:195758 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:22 KIND:node :: node _io_count_T_1 = cat(_io_count_T, ptr_diff)
[123] FIRRTL:195759 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:16 KIND:connect :: connect io.count, _io_count_T_1
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
  "task_id": "leaf_abstraction-BoomMSHRFile.respq-95e53b3103df506e",
  "work_unit_id": "BoomMSHRFile.respq",
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
