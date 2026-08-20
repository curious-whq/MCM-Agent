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

Task ID: `leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.6`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomMSHRFile.prefetcher`
- module: `NullPrefetcher`
- kind: `module`
- instance path: `BoomMSHRFile.prefetcher`
- leaf: `True`
- coverage complete: `True`
- raw statements: 118
- logical statements: 4
- mapped/logical source lines: 4
- registers: 0
- physical boundary events: 1

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

- `BoomMSHRFile.prefetcher::io.prefetch.fire`
  - predicate: `io.prefetch.valid && io.prefetch.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.prefetch.bits.addr', 'io.prefetch.bits.data', 'io.prefetch.bits.is_hella', 'io.prefetch.bits.uop.bp_debug_if', 'io.prefetch.bits.uop.bp_xcpt_if', 'io.prefetch.bits.uop.br_mask', 'io.prefetch.bits.uop.br_tag', 'io.prefetch.bits.uop.br_type', 'io.prefetch.bits.uop.csr_cmd', 'io.prefetch.bits.uop.debug_fsrc', 'io.prefetch.bits.uop.debug_inst', 'io.prefetch.bits.uop.debug_pc', 'io.prefetch.bits.uop.debug_tsrc', 'io.prefetch.bits.uop.dis_col_sel', 'io.prefetch.bits.uop.dst_rtype', 'io.prefetch.bits.uop.edge_inst', 'io.prefetch.bits.uop.exc_cause', 'io.prefetch.bits.uop.exception', 'io.prefetch.bits.uop.fcn_dw', 'io.prefetch.bits.uop.fcn_op', 'io.prefetch.bits.uop.flush_on_commit', 'io.prefetch.bits.uop.fp_ctrl.div', 'io.prefetch.bits.uop.fp_ctrl.fastpipe', 'io.prefetch.bits.uop.fp_ctrl.fma', 'io.prefetch.bits.uop.fp_ctrl.fromint', 'io.prefetch.bits.uop.fp_ctrl.ldst', 'io.prefetch.bits.uop.fp_ctrl.ren1', 'io.prefetch.bits.uop.fp_ctrl.ren2', 'io.prefetch.bits.uop.fp_ctrl.ren3', 'io.prefetch.bits.uop.fp_ctrl.sqrt', 'io.prefetch.bits.uop.fp_ctrl.swap12', 'io.prefetch.bits.uop.fp_ctrl.swap23', 'io.prefetch.bits.uop.fp_ctrl.toint', 'io.prefetch.bits.uop.fp_ctrl.typeTagIn', 'io.prefetch.bits.uop.fp_ctrl.typeTagOut', 'io.prefetch.bits.uop.fp_ctrl.vec', 'io.prefetch.bits.uop.fp_ctrl.wen', 'io.prefetch.bits.uop.fp_ctrl.wflags', 'io.prefetch.bits.uop.fp_rm', 'io.prefetch.bits.uop.fp_typ', 'io.prefetch.bits.uop.fp_val', 'io.prefetch.bits.uop.frs3_en', 'io.prefetch.bits.uop.ftq_idx', 'io.prefetch.bits.uop.fu_code[0]', 'io.prefetch.bits.uop.fu_code[1]', 'io.prefetch.bits.uop.fu_code[2]', 'io.prefetch.bits.uop.fu_code[3]', 'io.prefetch.bits.uop.fu_code[4]', 'io.prefetch.bits.uop.fu_code[5]', 'io.prefetch.bits.uop.fu_code[6]', 'io.prefetch.bits.uop.fu_code[7]', 'io.prefetch.bits.uop.fu_code[8]', 'io.prefetch.bits.uop.fu_code[9]', 'io.prefetch.bits.uop.imm_packed', 'io.prefetch.bits.uop.imm_rename', 'io.prefetch.bits.uop.imm_sel', 'io.prefetch.bits.uop.inst', 'io.prefetch.bits.uop.iq_type[0]', 'io.prefetch.bits.uop.iq_type[1]', 'io.prefetch.bits.uop.iq_type[2]', 'io.prefetch.bits.uop.iq_type[3]', 'io.prefetch.bits.uop.is_amo', 'io.prefetch.bits.uop.is_eret', 'io.prefetch.bits.uop.is_fence', 'io.prefetch.bits.uop.is_fencei', 'io.prefetch.bits.uop.is_mov', 'io.prefetch.bits.uop.is_rocc', 'io.prefetch.bits.uop.is_rvc', 'io.prefetch.bits.uop.is_sfb', 'io.prefetch.bits.uop.is_sfence', 'io.prefetch.bits.uop.is_sys_pc2epc', 'io.prefetch.bits.uop.is_unique', 'io.prefetch.bits.uop.iw_issued', 'io.prefetch.bits.uop.iw_issued_partial_agen', 'io.prefetch.bits.uop.iw_issued_partial_dgen', 'io.prefetch.bits.uop.iw_p1_bypass_hint', 'io.prefetch.bits.uop.iw_p1_speculative_child', 'io.prefetch.bits.uop.iw_p2_bypass_hint', 'io.prefetch.bits.uop.iw_p2_speculative_child', 'io.prefetch.bits.uop.iw_p3_bypass_hint', 'io.prefetch.bits.uop.ldq_idx', 'io.prefetch.bits.uop.ldst', 'io.prefetch.bits.uop.ldst_is_rs1', 'io.prefetch.bits.uop.lrs1', 'io.prefetch.bits.uop.lrs1_rtype', 'io.prefetch.bits.uop.lrs2', 'io.prefetch.bits.uop.lrs2_rtype', 'io.prefetch.bits.uop.lrs3', 'io.prefetch.bits.uop.mem_cmd', 'io.prefetch.bits.uop.mem_signed', 'io.prefetch.bits.uop.mem_size', 'io.prefetch.bits.uop.op1_sel', 'io.prefetch.bits.uop.op2_sel', 'io.prefetch.bits.uop.pc_lob', 'io.prefetch.bits.uop.pdst', 'io.prefetch.bits.uop.pimm', 'io.prefetch.bits.uop.ppred', 'io.prefetch.bits.uop.ppred_busy', 'io.prefetch.bits.uop.prs1', 'io.prefetch.bits.uop.prs1_busy', 'io.prefetch.bits.uop.prs2', 'io.prefetch.bits.uop.prs2_busy', 'io.prefetch.bits.uop.prs3', 'io.prefetch.bits.uop.prs3_busy', 'io.prefetch.bits.uop.rob_idx', 'io.prefetch.bits.uop.rxq_idx', 'io.prefetch.bits.uop.stale_pdst', 'io.prefetch.bits.uop.stq_idx', 'io.prefetch.bits.uop.taken', 'io.prefetch.bits.uop.uses_ldq', 'io.prefetch.bits.uop.uses_stq', 'io.prefetch.bits.uop.xcpt_ae_if', 'io.prefetch.bits.uop.xcpt_ma_if', 'io.prefetch.bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []

## Concrete local state

[]

## Environment/frontier signals

['io.prefetch.bits.addr', 'io.prefetch.bits.data', 'io.prefetch.bits.is_hella', 'io.prefetch.bits.uop.bp_debug_if', 'io.prefetch.bits.uop.bp_xcpt_if', 'io.prefetch.bits.uop.br_mask', 'io.prefetch.bits.uop.br_tag', 'io.prefetch.bits.uop.br_type', 'io.prefetch.bits.uop.csr_cmd', 'io.prefetch.bits.uop.debug_fsrc', 'io.prefetch.bits.uop.debug_inst', 'io.prefetch.bits.uop.debug_pc', 'io.prefetch.bits.uop.debug_tsrc', 'io.prefetch.bits.uop.dis_col_sel', 'io.prefetch.bits.uop.dst_rtype', 'io.prefetch.bits.uop.edge_inst', 'io.prefetch.bits.uop.exc_cause', 'io.prefetch.bits.uop.exception', 'io.prefetch.bits.uop.fcn_dw', 'io.prefetch.bits.uop.fcn_op', 'io.prefetch.bits.uop.flush_on_commit', 'io.prefetch.bits.uop.fp_ctrl.div', 'io.prefetch.bits.uop.fp_ctrl.fastpipe', 'io.prefetch.bits.uop.fp_ctrl.fma', 'io.prefetch.bits.uop.fp_ctrl.fromint', 'io.prefetch.bits.uop.fp_ctrl.ldst', 'io.prefetch.bits.uop.fp_ctrl.ren1', 'io.prefetch.bits.uop.fp_ctrl.ren2', 'io.prefetch.bits.uop.fp_ctrl.ren3', 'io.prefetch.bits.uop.fp_ctrl.sqrt', 'io.prefetch.bits.uop.fp_ctrl.swap12', 'io.prefetch.bits.uop.fp_ctrl.swap23', 'io.prefetch.bits.uop.fp_ctrl.toint', 'io.prefetch.bits.uop.fp_ctrl.typeTagIn', 'io.prefetch.bits.uop.fp_ctrl.typeTagOut', 'io.prefetch.bits.uop.fp_ctrl.vec', 'io.prefetch.bits.uop.fp_ctrl.wen', 'io.prefetch.bits.uop.fp_ctrl.wflags', 'io.prefetch.bits.uop.fp_rm', 'io.prefetch.bits.uop.fp_typ', 'io.prefetch.bits.uop.fp_val', 'io.prefetch.bits.uop.frs3_en', 'io.prefetch.bits.uop.ftq_idx', 'io.prefetch.bits.uop.fu_code[0]', 'io.prefetch.bits.uop.fu_code[1]', 'io.prefetch.bits.uop.fu_code[2]', 'io.prefetch.bits.uop.fu_code[3]', 'io.prefetch.bits.uop.fu_code[4]', 'io.prefetch.bits.uop.fu_code[5]', 'io.prefetch.bits.uop.fu_code[6]', 'io.prefetch.bits.uop.fu_code[7]', 'io.prefetch.bits.uop.fu_code[8]', 'io.prefetch.bits.uop.fu_code[9]', 'io.prefetch.bits.uop.imm_packed', 'io.prefetch.bits.uop.imm_rename', 'io.prefetch.bits.uop.imm_sel', 'io.prefetch.bits.uop.inst', 'io.prefetch.bits.uop.iq_type[0]', 'io.prefetch.bits.uop.iq_type[1]', 'io.prefetch.bits.uop.iq_type[2]', 'io.prefetch.bits.uop.iq_type[3]', 'io.prefetch.bits.uop.is_amo', 'io.prefetch.bits.uop.is_eret', 'io.prefetch.bits.uop.is_fence', 'io.prefetch.bits.uop.is_fencei', 'io.prefetch.bits.uop.is_mov', 'io.prefetch.bits.uop.is_rocc', 'io.prefetch.bits.uop.is_rvc', 'io.prefetch.bits.uop.is_sfb', 'io.prefetch.bits.uop.is_sfence', 'io.prefetch.bits.uop.is_sys_pc2epc', 'io.prefetch.bits.uop.is_unique', 'io.prefetch.bits.uop.iw_issued', 'io.prefetch.bits.uop.iw_issued_partial_agen', 'io.prefetch.bits.uop.iw_issued_partial_dgen', 'io.prefetch.bits.uop.iw_p1_bypass_hint', 'io.prefetch.bits.uop.iw_p1_speculative_child', 'io.prefetch.bits.uop.iw_p2_bypass_hint', 'io.prefetch.bits.uop.iw_p2_speculative_child', 'io.prefetch.bits.uop.iw_p3_bypass_hint', 'io.prefetch.bits.uop.ldq_idx', 'io.prefetch.bits.uop.ldst', 'io.prefetch.bits.uop.ldst_is_rs1', 'io.prefetch.bits.uop.lrs1', 'io.prefetch.bits.uop.lrs1_rtype', 'io.prefetch.bits.uop.lrs2', 'io.prefetch.bits.uop.lrs2_rtype', 'io.prefetch.bits.uop.lrs3', 'io.prefetch.bits.uop.mem_cmd', 'io.prefetch.bits.uop.mem_signed', 'io.prefetch.bits.uop.mem_size', 'io.prefetch.bits.uop.op1_sel', 'io.prefetch.bits.uop.op2_sel', 'io.prefetch.bits.uop.pc_lob', 'io.prefetch.bits.uop.pdst', 'io.prefetch.bits.uop.pimm', 'io.prefetch.bits.uop.ppred', 'io.prefetch.bits.uop.ppred_busy', 'io.prefetch.bits.uop.prs1', 'io.prefetch.bits.uop.prs1_busy', 'io.prefetch.bits.uop.prs2', 'io.prefetch.bits.uop.prs2_busy', 'io.prefetch.bits.uop.prs3', 'io.prefetch.bits.uop.prs3_busy', 'io.prefetch.bits.uop.rob_idx', 'io.prefetch.bits.uop.rxq_idx', 'io.prefetch.bits.uop.stale_pdst', 'io.prefetch.bits.uop.stq_idx', 'io.prefetch.bits.uop.taken', 'io.prefetch.bits.uop.uses_ldq', 'io.prefetch.bits.uop.uses_stq', 'io.prefetch.bits.uop.xcpt_ae_if', 'io.prefetch.bits.uop.xcpt_ma_if', 'io.prefetch.bits.uop.xcpt_pf_if', 'io.prefetch.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/prefetcher.scala:25-27
```scala
{
  val io = IO(new Bundle {
    val mshr_avail = Input(Bool())
```

### generators/boom/src/main/scala/v4/lsu/prefetcher.scala:38-43
```scala
  */
class NullPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends DataPrefetcher
{
  io.prefetch.valid := false.B
  io.prefetch.bits  := DontCare
}
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:188349 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:39:7 KIND:structural :: input clock : Clock
[1] FIRRTL:188350 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:39:7 KIND:structural :: input reset : Reset
[2] FIRRTL:188351 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:26:14 KIND:structural :: output io : { flip mshr_avail : UInt<1>, flip req_val : UInt<1>, flip req_addr : UInt<40>, flip req_coh : { state : UInt<2>}, prefetch : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}}
[3] FIRRTL:188353 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:41:21 KIND:connect :: connect io.prefetch.valid, UInt<1>(0h0)
[4] FIRRTL:188354 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.is_hella
[5] FIRRTL:188355 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.data
[6] FIRRTL:188356 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.addr
[7] FIRRTL:188357 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.debug_tsrc
[8] FIRRTL:188358 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.debug_fsrc
[9] FIRRTL:188359 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.bp_xcpt_if
[10] FIRRTL:188360 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.bp_debug_if
[11] FIRRTL:188361 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.xcpt_ma_if
[12] FIRRTL:188362 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.xcpt_ae_if
[13] FIRRTL:188363 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.xcpt_pf_if
[14] FIRRTL:188364 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_typ
[15] FIRRTL:188365 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_rm
[16] FIRRTL:188366 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_val
[17] FIRRTL:188367 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fcn_op
[18] FIRRTL:188368 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fcn_dw
[19] FIRRTL:188369 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.frs3_en
[20] FIRRTL:188370 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.lrs2_rtype
[21] FIRRTL:188371 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.lrs1_rtype
[22] FIRRTL:188372 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.dst_rtype
[23] FIRRTL:188373 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.lrs3
[24] FIRRTL:188374 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.lrs2
[25] FIRRTL:188375 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.lrs1
[26] FIRRTL:188376 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ldst
[27] FIRRTL:188377 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ldst_is_rs1
[28] FIRRTL:188378 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.csr_cmd
[29] FIRRTL:188379 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.flush_on_commit
[30] FIRRTL:188380 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_unique
[31] FIRRTL:188381 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.uses_stq
[32] FIRRTL:188382 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.uses_ldq
[33] FIRRTL:188383 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.mem_signed
[34] FIRRTL:188384 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.mem_size
[35] FIRRTL:188385 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.mem_cmd
[36] FIRRTL:188386 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.exc_cause
[37] FIRRTL:188387 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.exception
[38] FIRRTL:188388 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.stale_pdst
[39] FIRRTL:188389 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ppred_busy
[40] FIRRTL:188390 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs3_busy
[41] FIRRTL:188391 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs2_busy
[42] FIRRTL:188392 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs1_busy
[43] FIRRTL:188393 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ppred
[44] FIRRTL:188394 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs3
[45] FIRRTL:188395 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs2
[46] FIRRTL:188396 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.prs1
[47] FIRRTL:188397 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.pdst
[48] FIRRTL:188398 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.rxq_idx
[49] FIRRTL:188399 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.stq_idx
[50] FIRRTL:188400 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ldq_idx
[51] FIRRTL:188401 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.rob_idx
[52] FIRRTL:188402 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.vec
[53] FIRRTL:188403 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.wflags
[54] FIRRTL:188404 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.sqrt
[55] FIRRTL:188405 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.div
[56] FIRRTL:188406 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.fma
[57] FIRRTL:188407 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.fastpipe
[58] FIRRTL:188408 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.toint
[59] FIRRTL:188409 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.fromint
[60] FIRRTL:188410 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.typeTagOut
[61] FIRRTL:188411 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.typeTagIn
[62] FIRRTL:188412 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.swap23
[63] FIRRTL:188413 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.swap12
[64] FIRRTL:188414 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.ren3
[65] FIRRTL:188415 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.ren2
[66] FIRRTL:188416 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.ren1
[67] FIRRTL:188417 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.wen
[68] FIRRTL:188418 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fp_ctrl.ldst
[69] FIRRTL:188419 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.op2_sel
[70] FIRRTL:188420 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.op1_sel
[71] FIRRTL:188421 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.imm_packed
[72] FIRRTL:188422 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.pimm
[73] FIRRTL:188423 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.imm_sel
[74] FIRRTL:188424 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.imm_rename
[75] FIRRTL:188425 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.taken
[76] FIRRTL:188426 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.pc_lob
[77] FIRRTL:188427 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.edge_inst
[78] FIRRTL:188428 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.ftq_idx
[79] FIRRTL:188429 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_mov
[80] FIRRTL:188430 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_rocc
[81] FIRRTL:188431 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_sys_pc2epc
[82] FIRRTL:188432 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_eret
[83] FIRRTL:188433 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_amo
[84] FIRRTL:188434 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_sfence
[85] FIRRTL:188435 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_fencei
[86] FIRRTL:188436 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_fence
[87] FIRRTL:188437 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_sfb
[88] FIRRTL:188438 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.br_type
[89] FIRRTL:188439 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.br_tag
[90] FIRRTL:188440 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.br_mask
[91] FIRRTL:188441 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.dis_col_sel
[92] FIRRTL:188442 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_p3_bypass_hint
[93] FIRRTL:188443 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_p2_bypass_hint
[94] FIRRTL:188444 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_p1_bypass_hint
[95] FIRRTL:188445 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_p2_speculative_child
[96] FIRRTL:188446 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_p1_speculative_child
[97] FIRRTL:188447 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_issued_partial_dgen
[98] FIRRTL:188448 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_issued_partial_agen
[99] FIRRTL:188449 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iw_issued
[100] FIRRTL:188450 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[0]
[101] FIRRTL:188451 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[1]
[102] FIRRTL:188452 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[2]
[103] FIRRTL:188453 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[3]
[104] FIRRTL:188454 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[4]
[105] FIRRTL:188455 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[5]
[106] FIRRTL:188456 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[6]
[107] FIRRTL:188457 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[7]
[108] FIRRTL:188458 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[8]
[109] FIRRTL:188459 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.fu_code[9]
[110] FIRRTL:188460 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iq_type[0]
[111] FIRRTL:188461 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iq_type[1]
[112] FIRRTL:188462 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iq_type[2]
[113] FIRRTL:188463 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.iq_type[3]
[114] FIRRTL:188464 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.debug_pc
[115] FIRRTL:188465 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.is_rvc
[116] FIRRTL:188466 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.debug_inst
[117] FIRRTL:188467 SRC:generators/boom/src/main/scala/v4/lsu/prefetcher.scala:42:21 KIND:invalidate :: invalidate io.prefetch.bits.uop.inst
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
  "task_id": "leaf_abstraction-BoomMSHRFile.prefetcher-974790994b1992ac",
  "work_unit_id": "BoomMSHRFile.prefetcher",
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
