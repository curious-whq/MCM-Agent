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

Task ID: `leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.9`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomMSHRFile.mmios_0`
- module: `BoomIOMSHR`
- kind: `module`
- instance path: `BoomMSHRFile.mmios_0`
- leaf: `True`
- coverage complete: `True`
- raw statements: 1649
- logical statements: 101
- mapped/logical source lines: 90
- registers: 3
- physical boundary events: 4

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

- `BoomMSHRFile.mmios_0::io.mem_access.fire`
  - predicate: `io.mem_access.valid && io.mem_access.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.mem_access.bits.address', 'io.mem_access.bits.corrupt', 'io.mem_access.bits.data', 'io.mem_access.bits.mask', 'io.mem_access.bits.opcode', 'io.mem_access.bits.param', 'io.mem_access.bits.size', 'io.mem_access.bits.source']
  - immediate registers: ['state']
  - historical registers: ['req', 'state']
- `BoomMSHRFile.mmios_0::io.mem_ack.valid`
  - predicate: `io.mem_ack.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.mem_ack.bits.corrupt', 'io.mem_ack.bits.data', 'io.mem_ack.bits.denied', 'io.mem_ack.bits.opcode', 'io.mem_ack.bits.param', 'io.mem_ack.bits.sink', 'io.mem_ack.bits.size', 'io.mem_ack.bits.source']
  - immediate registers: []
  - historical registers: []
- `BoomMSHRFile.mmios_0::io.req.fire`
  - predicate: `io.req.valid && io.req.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.req.bits.addr', 'io.req.bits.data', 'io.req.bits.is_hella', 'io.req.bits.uop.bp_debug_if', 'io.req.bits.uop.bp_xcpt_if', 'io.req.bits.uop.br_mask', 'io.req.bits.uop.br_tag', 'io.req.bits.uop.br_type', 'io.req.bits.uop.csr_cmd', 'io.req.bits.uop.debug_fsrc', 'io.req.bits.uop.debug_inst', 'io.req.bits.uop.debug_pc', 'io.req.bits.uop.debug_tsrc', 'io.req.bits.uop.dis_col_sel', 'io.req.bits.uop.dst_rtype', 'io.req.bits.uop.edge_inst', 'io.req.bits.uop.exc_cause', 'io.req.bits.uop.exception', 'io.req.bits.uop.fcn_dw', 'io.req.bits.uop.fcn_op', 'io.req.bits.uop.flush_on_commit', 'io.req.bits.uop.fp_ctrl.div', 'io.req.bits.uop.fp_ctrl.fastpipe', 'io.req.bits.uop.fp_ctrl.fma', 'io.req.bits.uop.fp_ctrl.fromint', 'io.req.bits.uop.fp_ctrl.ldst', 'io.req.bits.uop.fp_ctrl.ren1', 'io.req.bits.uop.fp_ctrl.ren2', 'io.req.bits.uop.fp_ctrl.ren3', 'io.req.bits.uop.fp_ctrl.sqrt', 'io.req.bits.uop.fp_ctrl.swap12', 'io.req.bits.uop.fp_ctrl.swap23', 'io.req.bits.uop.fp_ctrl.toint', 'io.req.bits.uop.fp_ctrl.typeTagIn', 'io.req.bits.uop.fp_ctrl.typeTagOut', 'io.req.bits.uop.fp_ctrl.vec', 'io.req.bits.uop.fp_ctrl.wen', 'io.req.bits.uop.fp_ctrl.wflags', 'io.req.bits.uop.fp_rm', 'io.req.bits.uop.fp_typ', 'io.req.bits.uop.fp_val', 'io.req.bits.uop.frs3_en', 'io.req.bits.uop.ftq_idx', 'io.req.bits.uop.fu_code[0]', 'io.req.bits.uop.fu_code[1]', 'io.req.bits.uop.fu_code[2]', 'io.req.bits.uop.fu_code[3]', 'io.req.bits.uop.fu_code[4]', 'io.req.bits.uop.fu_code[5]', 'io.req.bits.uop.fu_code[6]', 'io.req.bits.uop.fu_code[7]', 'io.req.bits.uop.fu_code[8]', 'io.req.bits.uop.fu_code[9]', 'io.req.bits.uop.imm_packed', 'io.req.bits.uop.imm_rename', 'io.req.bits.uop.imm_sel', 'io.req.bits.uop.inst', 'io.req.bits.uop.iq_type[0]', 'io.req.bits.uop.iq_type[1]', 'io.req.bits.uop.iq_type[2]', 'io.req.bits.uop.iq_type[3]', 'io.req.bits.uop.is_amo', 'io.req.bits.uop.is_eret', 'io.req.bits.uop.is_fence', 'io.req.bits.uop.is_fencei', 'io.req.bits.uop.is_mov', 'io.req.bits.uop.is_rocc', 'io.req.bits.uop.is_rvc', 'io.req.bits.uop.is_sfb', 'io.req.bits.uop.is_sfence', 'io.req.bits.uop.is_sys_pc2epc', 'io.req.bits.uop.is_unique', 'io.req.bits.uop.iw_issued', 'io.req.bits.uop.iw_issued_partial_agen', 'io.req.bits.uop.iw_issued_partial_dgen', 'io.req.bits.uop.iw_p1_bypass_hint', 'io.req.bits.uop.iw_p1_speculative_child', 'io.req.bits.uop.iw_p2_bypass_hint', 'io.req.bits.uop.iw_p2_speculative_child', 'io.req.bits.uop.iw_p3_bypass_hint', 'io.req.bits.uop.ldq_idx', 'io.req.bits.uop.ldst', 'io.req.bits.uop.ldst_is_rs1', 'io.req.bits.uop.lrs1', 'io.req.bits.uop.lrs1_rtype', 'io.req.bits.uop.lrs2', 'io.req.bits.uop.lrs2_rtype', 'io.req.bits.uop.lrs3', 'io.req.bits.uop.mem_cmd', 'io.req.bits.uop.mem_signed', 'io.req.bits.uop.mem_size', 'io.req.bits.uop.op1_sel', 'io.req.bits.uop.op2_sel', 'io.req.bits.uop.pc_lob', 'io.req.bits.uop.pdst', 'io.req.bits.uop.pimm', 'io.req.bits.uop.ppred', 'io.req.bits.uop.ppred_busy', 'io.req.bits.uop.prs1', 'io.req.bits.uop.prs1_busy', 'io.req.bits.uop.prs2', 'io.req.bits.uop.prs2_busy', 'io.req.bits.uop.prs3', 'io.req.bits.uop.prs3_busy', 'io.req.bits.uop.rob_idx', 'io.req.bits.uop.rxq_idx', 'io.req.bits.uop.stale_pdst', 'io.req.bits.uop.stq_idx', 'io.req.bits.uop.taken', 'io.req.bits.uop.uses_ldq', 'io.req.bits.uop.uses_stq', 'io.req.bits.uop.xcpt_ae_if', 'io.req.bits.uop.xcpt_ma_if', 'io.req.bits.uop.xcpt_pf_if']
  - immediate registers: ['state']
  - historical registers: ['req', 'state']
- `BoomMSHRFile.mmios_0::io.resp.fire`
  - predicate: `io.resp.valid && io.resp.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if']
  - immediate registers: ['req', 'state']
  - historical registers: ['grant_word', 'req', 'state']

## Concrete local state

['grant_word', 'req', 'state']

## Environment/frontier signals

['clock', 'io.mem_access.bits.address', 'io.mem_access.bits.corrupt', 'io.mem_access.bits.data', 'io.mem_access.bits.mask', 'io.mem_access.bits.opcode', 'io.mem_access.bits.param', 'io.mem_access.bits.size', 'io.mem_access.bits.source', 'io.mem_access.ready', 'io.mem_access.valid', 'io.mem_ack.bits.data', 'io.mem_ack.valid', 'io.req.ready', 'io.req.valid', 'io.resp.bits.data', 'io.resp.bits.is_hella', 'io.resp.bits.uop.bp_debug_if', 'io.resp.bits.uop.bp_xcpt_if', 'io.resp.bits.uop.br_mask', 'io.resp.bits.uop.br_tag', 'io.resp.bits.uop.br_type', 'io.resp.bits.uop.csr_cmd', 'io.resp.bits.uop.debug_fsrc', 'io.resp.bits.uop.debug_inst', 'io.resp.bits.uop.debug_pc', 'io.resp.bits.uop.debug_tsrc', 'io.resp.bits.uop.dis_col_sel', 'io.resp.bits.uop.dst_rtype', 'io.resp.bits.uop.edge_inst', 'io.resp.bits.uop.exc_cause', 'io.resp.bits.uop.exception', 'io.resp.bits.uop.fcn_dw', 'io.resp.bits.uop.fcn_op', 'io.resp.bits.uop.flush_on_commit', 'io.resp.bits.uop.fp_ctrl.div', 'io.resp.bits.uop.fp_ctrl.fastpipe', 'io.resp.bits.uop.fp_ctrl.fma', 'io.resp.bits.uop.fp_ctrl.fromint', 'io.resp.bits.uop.fp_ctrl.ldst', 'io.resp.bits.uop.fp_ctrl.ren1', 'io.resp.bits.uop.fp_ctrl.ren2', 'io.resp.bits.uop.fp_ctrl.ren3', 'io.resp.bits.uop.fp_ctrl.sqrt', 'io.resp.bits.uop.fp_ctrl.swap12', 'io.resp.bits.uop.fp_ctrl.swap23', 'io.resp.bits.uop.fp_ctrl.toint', 'io.resp.bits.uop.fp_ctrl.typeTagIn', 'io.resp.bits.uop.fp_ctrl.typeTagOut', 'io.resp.bits.uop.fp_ctrl.vec', 'io.resp.bits.uop.fp_ctrl.wen', 'io.resp.bits.uop.fp_ctrl.wflags', 'io.resp.bits.uop.fp_rm', 'io.resp.bits.uop.fp_typ', 'io.resp.bits.uop.fp_val', 'io.resp.bits.uop.frs3_en', 'io.resp.bits.uop.ftq_idx', 'io.resp.bits.uop.fu_code[0]', 'io.resp.bits.uop.fu_code[1]', 'io.resp.bits.uop.fu_code[2]', 'io.resp.bits.uop.fu_code[3]', 'io.resp.bits.uop.fu_code[4]', 'io.resp.bits.uop.fu_code[5]', 'io.resp.bits.uop.fu_code[6]', 'io.resp.bits.uop.fu_code[7]', 'io.resp.bits.uop.fu_code[8]', 'io.resp.bits.uop.fu_code[9]', 'io.resp.bits.uop.imm_packed', 'io.resp.bits.uop.imm_rename', 'io.resp.bits.uop.imm_sel', 'io.resp.bits.uop.inst', 'io.resp.bits.uop.iq_type[0]', 'io.resp.bits.uop.iq_type[1]', 'io.resp.bits.uop.iq_type[2]', 'io.resp.bits.uop.iq_type[3]', 'io.resp.bits.uop.is_amo', 'io.resp.bits.uop.is_eret', 'io.resp.bits.uop.is_fence', 'io.resp.bits.uop.is_fencei', 'io.resp.bits.uop.is_mov', 'io.resp.bits.uop.is_rocc', 'io.resp.bits.uop.is_rvc', 'io.resp.bits.uop.is_sfb', 'io.resp.bits.uop.is_sfence', 'io.resp.bits.uop.is_sys_pc2epc', 'io.resp.bits.uop.is_unique', 'io.resp.bits.uop.iw_issued', 'io.resp.bits.uop.iw_issued_partial_agen', 'io.resp.bits.uop.iw_issued_partial_dgen', 'io.resp.bits.uop.iw_p1_bypass_hint', 'io.resp.bits.uop.iw_p1_speculative_child', 'io.resp.bits.uop.iw_p2_bypass_hint', 'io.resp.bits.uop.iw_p2_speculative_child', 'io.resp.bits.uop.iw_p3_bypass_hint', 'io.resp.bits.uop.ldq_idx', 'io.resp.bits.uop.ldst', 'io.resp.bits.uop.ldst_is_rs1', 'io.resp.bits.uop.lrs1', 'io.resp.bits.uop.lrs1_rtype', 'io.resp.bits.uop.lrs2', 'io.resp.bits.uop.lrs2_rtype', 'io.resp.bits.uop.lrs3', 'io.resp.bits.uop.mem_cmd', 'io.resp.bits.uop.mem_signed', 'io.resp.bits.uop.mem_size', 'io.resp.bits.uop.op1_sel', 'io.resp.bits.uop.op2_sel', 'io.resp.bits.uop.pc_lob', 'io.resp.bits.uop.pdst', 'io.resp.bits.uop.pimm', 'io.resp.bits.uop.ppred', 'io.resp.bits.uop.ppred_busy', 'io.resp.bits.uop.prs1', 'io.resp.bits.uop.prs1_busy', 'io.resp.bits.uop.prs2', 'io.resp.bits.uop.prs2_busy', 'io.resp.bits.uop.prs3', 'io.resp.bits.uop.prs3_busy', 'io.resp.bits.uop.rob_idx', 'io.resp.bits.uop.rxq_idx', 'io.resp.bits.uop.stale_pdst', 'io.resp.bits.uop.stq_idx', 'io.resp.bits.uop.taken', 'io.resp.bits.uop.uses_ldq', 'io.resp.bits.uop.uses_stq', 'io.resp.bits.uop.xcpt_ae_if', 'io.resp.bits.uop.xcpt_ma_if', 'io.resp.bits.uop.xcpt_pf_if', 'io.resp.ready', 'io.resp.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:388-390
```scala

class BoomIOMSHR(id: Int)(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
  with HasL1HellaCacheParameters
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:391-393
```scala
{
  val io = IO(new Bundle {
    val req  = Flipped(Decoupled(new BoomDCacheReq))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:403-406
```scala
  def wordFromBeat(addr: UInt, dat: UInt) = {
    val shift = Cat(beatOffset(addr), 0.U((wordOffBits+log2Ceil(wordBytes)).W))
    (dat >> shift)(wordBits-1, 0)
  }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:407-410
```scala

  val req = Reg(new BoomDCacheReq)
  val grant_word = Reg(UInt(wordBits.W))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:412-415
```scala

  val state = RegInit(s_idle)
  io.req.ready := state === s_idle
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:425-427
```scala
  val atomics  = if (edge.manager.anySupportLogical) {
    MuxLookup(req.uop.mem_cmd, (0.U).asTypeOf(new TLBundleA(edge.bundle)))(Array(
      M_XA_SWAP -> edge.Logical(a_source, a_address, a_size, a_data, TLAtomics.SWAP)._2,
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:440-445
```scala
  }
  assert(state === s_idle || req.uop.mem_cmd =/= M_XSC)

  io.mem_access.valid := state === s_mem_access
  io.mem_access.bits  := Mux(isAMO(req.uop.mem_cmd), atomics, Mux(isRead(req.uop.mem_cmd), get, put))
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:447-464
```scala

  io.resp.valid     := (state === s_resp) && send_resp
  io.resp.bits.uop  := req.uop
  io.resp.bits.data := loadgen.data
  io.resp.bits.is_hella := req.is_hella

  when (io.req.fire) {
    req   := io.req.bits
    state := s_mem_access
  }
  when (io.mem_access.fire) {
    state := s_mem_ack
  }
  when (state === s_mem_ack && io.mem_ack.valid) {
    state := s_resp
    when (isRead(req.uop.mem_cmd)) {
      grant_word := wordFromBeat(req.addr, io.mem_ack.bits.data)
    }
```

### generators/boom/src/main/scala/v4/lsu/mshrs.scala:465-469
```scala
  }
  when (state === s_resp) {
    when (!send_resp || io.resp.fire) {
      state := s_idle
    }
```

### generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:93-95
```scala
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

### generators/rocket-chip/src/main/scala/rocket/Consts.scala:86-90
```scala
  def isAMOArithmetic(cmd: UInt) = cmd.isOneOf(M_XA_ADD, M_XA_MIN, M_XA_MAX, M_XA_MINU, M_XA_MAXU)
  def isAMO(cmd: UInt) = isAMOLogical(cmd) || isAMOArithmetic(cmd)
  def isPrefetch(cmd: UInt) = cmd === M_PFR || cmd === M_PFW
  def isRead(cmd: UInt) = cmd.isOneOf(M_XRD, M_HLVX, M_XLR, M_XSC) || isAMO(cmd)
  def isWrite(cmd: UInt) = cmd === M_XWR || cmd === M_PWR || cmd === M_XSC || isAMO(cmd)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:459-466
```scala
    val legal = manager.supportsGetFast(toAddress, lgSize)
    val a = Wire(new TLBundleA(bundle))
    a.opcode  := TLMessages.Get
    a.param   := 0.U
    a.size    := lgSize
    a.source  := fromSource
    a.address := toAddress
    a.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:467-471
```scala
    a.echo    := DontCare
    a.mask    := mask(toAddress, lgSize)
    a.data    := DontCare
    a.corrupt := false.B
    (legal, a)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:479-486
```scala
    val legal = manager.supportsPutFullFast(toAddress, lgSize)
    val a = Wire(new TLBundleA(bundle))
    a.opcode  := TLMessages.PutFullData
    a.param   := 0.U
    a.size    := lgSize
    a.source  := fromSource
    a.address := toAddress
    a.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:487-491
```scala
    a.echo    := DontCare
    a.mask    := mask(toAddress, lgSize)
    a.data    := data
    a.corrupt := corrupt
    (legal, a)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:516-523
```scala
    val legal = manager.supportsArithmeticFast(toAddress, lgSize)
    val a = Wire(new TLBundleA(bundle))
    a.opcode  := TLMessages.ArithmeticData
    a.param   := atomic
    a.size    := lgSize
    a.source  := fromSource
    a.address := toAddress
    a.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:524-528
```scala
    a.echo    := DontCare
    a.mask    := mask(toAddress, lgSize)
    a.data    := data
    a.corrupt := corrupt
    (legal, a)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:533-540
```scala
    val legal = manager.supportsLogicalFast(toAddress, lgSize)
    val a = Wire(new TLBundleA(bundle))
    a.opcode  := TLMessages.LogicalData
    a.param   := atomic
    a.size    := lgSize
    a.source  := fromSource
    a.address := toAddress
    a.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:541-545
```scala
    a.echo    := DontCare
    a.mask    := mask(toAddress, lgSize)
    a.data    := data
    a.corrupt := corrupt
    (legal, a)
```

### generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:683-687
```scala
    // We return an or-reduction of all the cases, checking whether any contains both the dynamic size and dynamic address on the wire.
      ((Some(s) == range).B || s.containsLg(lgSize)) &&
      a.map(_.contains(address)).reduce(_||_)
    }.foldLeft(false.B)(_||_)
  }
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

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:193982 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:389:7 KIND:structural :: input clock : Clock
[1] FIRRTL:193983 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:389:7 KIND:structural :: input reset : Reset
[2] FIRRTL:193984 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:392:14 KIND:structural :: output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}}, resp : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>, is_hella : UInt<1>}}, mem_access : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, flip mem_ack : { valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, sink : UInt<3>, denied : UInt<1>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}}
[3] FIRRTL:193986 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:408:16 KIND:reg :: reg req : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : UInt<40>, data : UInt<64>, is_hella : UInt<1>}, clock
[4] FIRRTL:193987 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:409:23 KIND:reg :: reg grant_word : UInt<64>, clock
[5] FIRRTL:193988 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:413:22 KIND:regreset :: regreset state : UInt<2>, clock, reset, UInt<2>(0h0)
[6] FIRRTL:193989 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:414:25 KIND:node :: node _io_req_ready_T = eq(state, UInt<2>(0h0))
[7] FIRRTL:193990 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:414:16 KIND:connect :: connect io.req.ready, _io_req_ready_T
[8] FIRRTL:193991 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11:18 KIND:wire :: wire size : UInt<2>
[9] FIRRTL:193992 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect size, req.uop.mem_size
[10] FIRRTL:193993 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _get_legal_T = leq(UInt<1>(0h0), req.uop.mem_size)
[11] FIRRTL:193994 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _get_legal_T_1 = leq(req.uop.mem_size, UInt<4>(0hc))
[12] FIRRTL:193995 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _get_legal_T_2 = and(_get_legal_T, _get_legal_T_1)
[13] FIRRTL:193996 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _get_legal_T_3 = or(UInt<1>(0h0), _get_legal_T_2)
[14] FIRRTL:193997 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_4 = xor(req.addr, UInt<14>(0h3000))
[15] FIRRTL:193998 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_5 = cvt(_get_legal_T_4)
[16] FIRRTL:193999 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_6 = and(_get_legal_T_5, asSInt(UInt<33>(0h9a013000)))
[17] FIRRTL:194000 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_7 = asSInt(_get_legal_T_6)
[18] FIRRTL:194001 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_8 = eq(_get_legal_T_7, asSInt(UInt<1>(0h0)))
[19] FIRRTL:194002 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _get_legal_T_9 = and(_get_legal_T_3, _get_legal_T_8)
[20] FIRRTL:194003 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _get_legal_T_10 = leq(UInt<1>(0h0), req.uop.mem_size)
[21] FIRRTL:194004 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _get_legal_T_11 = leq(req.uop.mem_size, UInt<3>(0h6))
[22] FIRRTL:194005 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _get_legal_T_12 = and(_get_legal_T_10, _get_legal_T_11)
[23] FIRRTL:194006 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _get_legal_T_13 = or(UInt<1>(0h0), _get_legal_T_12)
[24] FIRRTL:194007 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_14 = xor(req.addr, UInt<1>(0h0))
[25] FIRRTL:194008 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_15 = cvt(_get_legal_T_14)
[26] FIRRTL:194009 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_16 = and(_get_legal_T_15, asSInt(UInt<33>(0h9a012000)))
[27] FIRRTL:194010 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_17 = asSInt(_get_legal_T_16)
[28] FIRRTL:194011 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_18 = eq(_get_legal_T_17, asSInt(UInt<1>(0h0)))
[29] FIRRTL:194012 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_19 = xor(req.addr, UInt<17>(0h10000))
[30] FIRRTL:194013 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_20 = cvt(_get_legal_T_19)
[31] FIRRTL:194014 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_21 = and(_get_legal_T_20, asSInt(UInt<33>(0h98013000)))
[32] FIRRTL:194015 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_22 = asSInt(_get_legal_T_21)
[33] FIRRTL:194016 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_23 = eq(_get_legal_T_22, asSInt(UInt<1>(0h0)))
[34] FIRRTL:194017 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_24 = xor(req.addr, UInt<17>(0h10000))
[35] FIRRTL:194018 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_25 = cvt(_get_legal_T_24)
[36] FIRRTL:194019 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_26 = and(_get_legal_T_25, asSInt(UInt<33>(0h9a010000)))
[37] FIRRTL:194020 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_27 = asSInt(_get_legal_T_26)
[38] FIRRTL:194021 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_28 = eq(_get_legal_T_27, asSInt(UInt<1>(0h0)))
[39] FIRRTL:194022 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_29 = xor(req.addr, UInt<26>(0h2000000))
[40] FIRRTL:194023 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_30 = cvt(_get_legal_T_29)
[41] FIRRTL:194024 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_31 = and(_get_legal_T_30, asSInt(UInt<33>(0h9a010000)))
[42] FIRRTL:194025 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_32 = asSInt(_get_legal_T_31)
[43] FIRRTL:194026 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_33 = eq(_get_legal_T_32, asSInt(UInt<1>(0h0)))
[44] FIRRTL:194027 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_34 = xor(req.addr, UInt<28>(0h8000000))
[45] FIRRTL:194028 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_35 = cvt(_get_legal_T_34)
[46] FIRRTL:194029 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_36 = and(_get_legal_T_35, asSInt(UInt<33>(0h98000000)))
[47] FIRRTL:194030 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_37 = asSInt(_get_legal_T_36)
[48] FIRRTL:194031 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_38 = eq(_get_legal_T_37, asSInt(UInt<1>(0h0)))
[49] FIRRTL:194032 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_39 = xor(req.addr, UInt<28>(0h8000000))
[50] FIRRTL:194033 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_40 = cvt(_get_legal_T_39)
[51] FIRRTL:194034 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_41 = and(_get_legal_T_40, asSInt(UInt<33>(0h9a010000)))
[52] FIRRTL:194035 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_42 = asSInt(_get_legal_T_41)
[53] FIRRTL:194036 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_43 = eq(_get_legal_T_42, asSInt(UInt<1>(0h0)))
[54] FIRRTL:194037 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_44 = xor(req.addr, UInt<29>(0h10000000))
[55] FIRRTL:194038 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_45 = cvt(_get_legal_T_44)
[56] FIRRTL:194039 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_46 = and(_get_legal_T_45, asSInt(UInt<33>(0h9a013000)))
[57] FIRRTL:194040 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_47 = asSInt(_get_legal_T_46)
[58] FIRRTL:194041 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_48 = eq(_get_legal_T_47, asSInt(UInt<1>(0h0)))
[59] FIRRTL:194042 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _get_legal_T_49 = xor(req.addr, UInt<32>(0h80000000))
[60] FIRRTL:194043 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _get_legal_T_50 = cvt(_get_legal_T_49)
[61] FIRRTL:194044 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_51 = and(_get_legal_T_50, asSInt(UInt<33>(0h90000000)))
[62] FIRRTL:194045 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _get_legal_T_52 = asSInt(_get_legal_T_51)
[63] FIRRTL:194046 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _get_legal_T_53 = eq(_get_legal_T_52, asSInt(UInt<1>(0h0)))
[64] FIRRTL:194047 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_54 = or(_get_legal_T_18, _get_legal_T_23)
[65] FIRRTL:194048 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_55 = or(_get_legal_T_54, _get_legal_T_28)
[66] FIRRTL:194049 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_56 = or(_get_legal_T_55, _get_legal_T_33)
[67] FIRRTL:194050 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_57 = or(_get_legal_T_56, _get_legal_T_38)
[68] FIRRTL:194051 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_58 = or(_get_legal_T_57, _get_legal_T_43)
[69] FIRRTL:194052 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_59 = or(_get_legal_T_58, _get_legal_T_48)
[70] FIRRTL:194053 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _get_legal_T_60 = or(_get_legal_T_59, _get_legal_T_53)
[71] FIRRTL:194054 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _get_legal_T_61 = and(_get_legal_T_13, _get_legal_T_60)
[72] FIRRTL:194055 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _get_legal_T_62 = or(UInt<1>(0h0), _get_legal_T_9)
[73] FIRRTL:194056 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node get_legal = or(_get_legal_T_62, _get_legal_T_61)
[74] FIRRTL:194057 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:460:17 KIND:wire :: wire get : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[75] FIRRTL:194058 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:461:15 KIND:connect :: connect get.opcode, UInt<3>(0h4)
[76] FIRRTL:194059 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:462:15 KIND:connect :: connect get.param, UInt<1>(0h0)
[77] FIRRTL:194060 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:463:15 KIND:connect :: connect get.size, req.uop.mem_size
[78] FIRRTL:194061 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:464:15 KIND:connect :: connect get.source, UInt<2>(0h3)
[79] FIRRTL:194062 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:465:15 KIND:connect :: connect get.address, req.addr
[80] FIRRTL:194063 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _get_a_mask_sizeOH_T = or(req.uop.mem_size, UInt<3>(0h0))
[81] FIRRTL:194064 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node get_a_mask_sizeOH_shiftAmount = bits(_get_a_mask_sizeOH_T, 1, 0)
[82] FIRRTL:194065 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _get_a_mask_sizeOH_T_1 = dshl(UInt<1>(0h1), get_a_mask_sizeOH_shiftAmount)
[83] FIRRTL:194066 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _get_a_mask_sizeOH_T_2 = bits(_get_a_mask_sizeOH_T_1, 2, 0)
[84] FIRRTL:194067 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node get_a_mask_sizeOH = or(_get_a_mask_sizeOH_T_2, UInt<1>(0h1))
[85] FIRRTL:194068 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node get_a_mask_sub_sub_sub_0_1 = geq(req.uop.mem_size, UInt<2>(0h3))
[86] FIRRTL:194069 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node get_a_mask_sub_sub_size = bits(get_a_mask_sizeOH, 2, 2)
[87] FIRRTL:194070 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node get_a_mask_sub_sub_bit = bits(req.addr, 2, 2)
[88] FIRRTL:194071 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node get_a_mask_sub_sub_nbit = eq(get_a_mask_sub_sub_bit, UInt<1>(0h0))
[89] FIRRTL:194072 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_sub_0_2 = and(UInt<1>(0h1), get_a_mask_sub_sub_nbit)
[90] FIRRTL:194073 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_sub_acc_T = and(get_a_mask_sub_sub_size, get_a_mask_sub_sub_0_2)
[91] FIRRTL:194074 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_sub_0_1 = or(get_a_mask_sub_sub_sub_0_1, _get_a_mask_sub_sub_acc_T)
[92] FIRRTL:194075 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_sub_1_2 = and(UInt<1>(0h1), get_a_mask_sub_sub_bit)
[93] FIRRTL:194076 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_sub_acc_T_1 = and(get_a_mask_sub_sub_size, get_a_mask_sub_sub_1_2)
[94] FIRRTL:194077 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_sub_1_1 = or(get_a_mask_sub_sub_sub_0_1, _get_a_mask_sub_sub_acc_T_1)
[95] FIRRTL:194078 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node get_a_mask_sub_size = bits(get_a_mask_sizeOH, 1, 1)
[96] FIRRTL:194079 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node get_a_mask_sub_bit = bits(req.addr, 1, 1)
[97] FIRRTL:194080 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node get_a_mask_sub_nbit = eq(get_a_mask_sub_bit, UInt<1>(0h0))
[98] FIRRTL:194081 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_0_2 = and(get_a_mask_sub_sub_0_2, get_a_mask_sub_nbit)
[99] FIRRTL:194082 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_acc_T = and(get_a_mask_sub_size, get_a_mask_sub_0_2)
[100] FIRRTL:194083 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_0_1 = or(get_a_mask_sub_sub_0_1, _get_a_mask_sub_acc_T)
[101] FIRRTL:194084 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_1_2 = and(get_a_mask_sub_sub_0_2, get_a_mask_sub_bit)
[102] FIRRTL:194085 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_acc_T_1 = and(get_a_mask_sub_size, get_a_mask_sub_1_2)
[103] FIRRTL:194086 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_1_1 = or(get_a_mask_sub_sub_0_1, _get_a_mask_sub_acc_T_1)
[104] FIRRTL:194087 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_2_2 = and(get_a_mask_sub_sub_1_2, get_a_mask_sub_nbit)
[105] FIRRTL:194088 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_acc_T_2 = and(get_a_mask_sub_size, get_a_mask_sub_2_2)
[106] FIRRTL:194089 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_2_1 = or(get_a_mask_sub_sub_1_1, _get_a_mask_sub_acc_T_2)
[107] FIRRTL:194090 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_sub_3_2 = and(get_a_mask_sub_sub_1_2, get_a_mask_sub_bit)
[108] FIRRTL:194091 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_sub_acc_T_3 = and(get_a_mask_sub_size, get_a_mask_sub_3_2)
[109] FIRRTL:194092 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_sub_3_1 = or(get_a_mask_sub_sub_1_1, _get_a_mask_sub_acc_T_3)
[110] FIRRTL:194093 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node get_a_mask_size = bits(get_a_mask_sizeOH, 0, 0)
[111] FIRRTL:194094 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node get_a_mask_bit = bits(req.addr, 0, 0)
[112] FIRRTL:194095 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node get_a_mask_nbit = eq(get_a_mask_bit, UInt<1>(0h0))
[113] FIRRTL:194096 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq = and(get_a_mask_sub_0_2, get_a_mask_nbit)
[114] FIRRTL:194097 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T = and(get_a_mask_size, get_a_mask_eq)
[115] FIRRTL:194098 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc = or(get_a_mask_sub_0_1, _get_a_mask_acc_T)
[116] FIRRTL:194099 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_1 = and(get_a_mask_sub_0_2, get_a_mask_bit)
[117] FIRRTL:194100 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_1 = and(get_a_mask_size, get_a_mask_eq_1)
[118] FIRRTL:194101 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_1 = or(get_a_mask_sub_0_1, _get_a_mask_acc_T_1)
[119] FIRRTL:194102 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_2 = and(get_a_mask_sub_1_2, get_a_mask_nbit)
[120] FIRRTL:194103 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_2 = and(get_a_mask_size, get_a_mask_eq_2)
[121] FIRRTL:194104 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_2 = or(get_a_mask_sub_1_1, _get_a_mask_acc_T_2)
[122] FIRRTL:194105 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_3 = and(get_a_mask_sub_1_2, get_a_mask_bit)
[123] FIRRTL:194106 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_3 = and(get_a_mask_size, get_a_mask_eq_3)
[124] FIRRTL:194107 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_3 = or(get_a_mask_sub_1_1, _get_a_mask_acc_T_3)
[125] FIRRTL:194108 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_4 = and(get_a_mask_sub_2_2, get_a_mask_nbit)
[126] FIRRTL:194109 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_4 = and(get_a_mask_size, get_a_mask_eq_4)
[127] FIRRTL:194110 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_4 = or(get_a_mask_sub_2_1, _get_a_mask_acc_T_4)
[128] FIRRTL:194111 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_5 = and(get_a_mask_sub_2_2, get_a_mask_bit)
[129] FIRRTL:194112 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_5 = and(get_a_mask_size, get_a_mask_eq_5)
[130] FIRRTL:194113 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_5 = or(get_a_mask_sub_2_1, _get_a_mask_acc_T_5)
[131] FIRRTL:194114 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_6 = and(get_a_mask_sub_3_2, get_a_mask_nbit)
[132] FIRRTL:194115 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_6 = and(get_a_mask_size, get_a_mask_eq_6)
[133] FIRRTL:194116 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_6 = or(get_a_mask_sub_3_1, _get_a_mask_acc_T_6)
[134] FIRRTL:194117 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node get_a_mask_eq_7 = and(get_a_mask_sub_3_2, get_a_mask_bit)
[135] FIRRTL:194118 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _get_a_mask_acc_T_7 = and(get_a_mask_size, get_a_mask_eq_7)
[136] FIRRTL:194119 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node get_a_mask_acc_7 = or(get_a_mask_sub_3_1, _get_a_mask_acc_T_7)
[137] FIRRTL:194120 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_lo_lo = cat(get_a_mask_acc_1, get_a_mask_acc)
[138] FIRRTL:194121 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_lo_hi = cat(get_a_mask_acc_3, get_a_mask_acc_2)
[139] FIRRTL:194122 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_lo = cat(get_a_mask_lo_hi, get_a_mask_lo_lo)
[140] FIRRTL:194123 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_hi_lo = cat(get_a_mask_acc_5, get_a_mask_acc_4)
[141] FIRRTL:194124 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_hi_hi = cat(get_a_mask_acc_7, get_a_mask_acc_6)
[142] FIRRTL:194125 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node get_a_mask_hi = cat(get_a_mask_hi_hi, get_a_mask_hi_lo)
[143] FIRRTL:194126 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _get_a_mask_T = cat(get_a_mask_hi, get_a_mask_lo)
[144] FIRRTL:194127 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:468:15 KIND:connect :: connect get.mask, _get_a_mask_T
[145] FIRRTL:194128 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:469:15 KIND:invalidate :: invalidate get.data
[146] FIRRTL:194129 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:470:15 KIND:connect :: connect get.corrupt, UInt<1>(0h0)
[147] FIRRTL:194130 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _put_legal_T = leq(UInt<1>(0h0), req.uop.mem_size)
[148] FIRRTL:194131 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _put_legal_T_1 = leq(req.uop.mem_size, UInt<4>(0hc))
[149] FIRRTL:194132 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _put_legal_T_2 = and(_put_legal_T, _put_legal_T_1)
[150] FIRRTL:194133 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _put_legal_T_3 = or(UInt<1>(0h0), _put_legal_T_2)
[151] FIRRTL:194134 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_4 = xor(req.addr, UInt<14>(0h3000))
[152] FIRRTL:194135 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_5 = cvt(_put_legal_T_4)
[153] FIRRTL:194136 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_6 = and(_put_legal_T_5, asSInt(UInt<33>(0h9a113000)))
[154] FIRRTL:194137 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_7 = asSInt(_put_legal_T_6)
[155] FIRRTL:194138 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_8 = eq(_put_legal_T_7, asSInt(UInt<1>(0h0)))
[156] FIRRTL:194139 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _put_legal_T_9 = and(_put_legal_T_3, _put_legal_T_8)
[157] FIRRTL:194140 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _put_legal_T_10 = leq(UInt<1>(0h0), req.uop.mem_size)
[158] FIRRTL:194141 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _put_legal_T_11 = leq(req.uop.mem_size, UInt<3>(0h6))
[159] FIRRTL:194142 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _put_legal_T_12 = and(_put_legal_T_10, _put_legal_T_11)
[160] FIRRTL:194143 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _put_legal_T_13 = or(UInt<1>(0h0), _put_legal_T_12)
[161] FIRRTL:194144 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_14 = xor(req.addr, UInt<1>(0h0))
[162] FIRRTL:194145 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_15 = cvt(_put_legal_T_14)
[163] FIRRTL:194146 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_16 = and(_put_legal_T_15, asSInt(UInt<33>(0h9a112000)))
[164] FIRRTL:194147 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_17 = asSInt(_put_legal_T_16)
[165] FIRRTL:194148 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_18 = eq(_put_legal_T_17, asSInt(UInt<1>(0h0)))
[166] FIRRTL:194149 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_19 = xor(req.addr, UInt<21>(0h100000))
[167] FIRRTL:194150 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_20 = cvt(_put_legal_T_19)
[168] FIRRTL:194151 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_21 = and(_put_legal_T_20, asSInt(UInt<33>(0h9a103000)))
[169] FIRRTL:194152 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_22 = asSInt(_put_legal_T_21)
[170] FIRRTL:194153 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_23 = eq(_put_legal_T_22, asSInt(UInt<1>(0h0)))
[171] FIRRTL:194154 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_24 = xor(req.addr, UInt<26>(0h2000000))
[172] FIRRTL:194155 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_25 = cvt(_put_legal_T_24)
[173] FIRRTL:194156 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_26 = and(_put_legal_T_25, asSInt(UInt<33>(0h9a110000)))
[174] FIRRTL:194157 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_27 = asSInt(_put_legal_T_26)
[175] FIRRTL:194158 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_28 = eq(_put_legal_T_27, asSInt(UInt<1>(0h0)))
[176] FIRRTL:194159 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_29 = xor(req.addr, UInt<26>(0h2010000))
[177] FIRRTL:194160 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_30 = cvt(_put_legal_T_29)
[178] FIRRTL:194161 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_31 = and(_put_legal_T_30, asSInt(UInt<33>(0h9a113000)))
[179] FIRRTL:194162 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_32 = asSInt(_put_legal_T_31)
[180] FIRRTL:194163 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_33 = eq(_put_legal_T_32, asSInt(UInt<1>(0h0)))
[181] FIRRTL:194164 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_34 = xor(req.addr, UInt<28>(0h8000000))
[182] FIRRTL:194165 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_35 = cvt(_put_legal_T_34)
[183] FIRRTL:194166 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_36 = and(_put_legal_T_35, asSInt(UInt<33>(0h98000000)))
[184] FIRRTL:194167 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_37 = asSInt(_put_legal_T_36)
[185] FIRRTL:194168 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_38 = eq(_put_legal_T_37, asSInt(UInt<1>(0h0)))
[186] FIRRTL:194169 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_39 = xor(req.addr, UInt<28>(0h8000000))
[187] FIRRTL:194170 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_40 = cvt(_put_legal_T_39)
[188] FIRRTL:194171 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_41 = and(_put_legal_T_40, asSInt(UInt<33>(0h9a110000)))
[189] FIRRTL:194172 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_42 = asSInt(_put_legal_T_41)
[190] FIRRTL:194173 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_43 = eq(_put_legal_T_42, asSInt(UInt<1>(0h0)))
[191] FIRRTL:194174 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_44 = xor(req.addr, UInt<29>(0h10000000))
[192] FIRRTL:194175 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_45 = cvt(_put_legal_T_44)
[193] FIRRTL:194176 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_46 = and(_put_legal_T_45, asSInt(UInt<33>(0h9a113000)))
[194] FIRRTL:194177 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_47 = asSInt(_put_legal_T_46)
[195] FIRRTL:194178 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_48 = eq(_put_legal_T_47, asSInt(UInt<1>(0h0)))
[196] FIRRTL:194179 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_49 = xor(req.addr, UInt<32>(0h80000000))
[197] FIRRTL:194180 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_50 = cvt(_put_legal_T_49)
[198] FIRRTL:194181 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_51 = and(_put_legal_T_50, asSInt(UInt<33>(0h90000000)))
[199] FIRRTL:194182 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_52 = asSInt(_put_legal_T_51)
[200] FIRRTL:194183 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_53 = eq(_put_legal_T_52, asSInt(UInt<1>(0h0)))
[201] FIRRTL:194184 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_54 = or(_put_legal_T_18, _put_legal_T_23)
[202] FIRRTL:194185 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_55 = or(_put_legal_T_54, _put_legal_T_28)
[203] FIRRTL:194186 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_56 = or(_put_legal_T_55, _put_legal_T_33)
[204] FIRRTL:194187 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_57 = or(_put_legal_T_56, _put_legal_T_38)
[205] FIRRTL:194188 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_58 = or(_put_legal_T_57, _put_legal_T_43)
[206] FIRRTL:194189 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_59 = or(_put_legal_T_58, _put_legal_T_48)
[207] FIRRTL:194190 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _put_legal_T_60 = or(_put_legal_T_59, _put_legal_T_53)
[208] FIRRTL:194191 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _put_legal_T_61 = and(_put_legal_T_13, _put_legal_T_60)
[209] FIRRTL:194192 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _put_legal_T_62 = or(UInt<1>(0h0), UInt<1>(0h0))
[210] FIRRTL:194193 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _put_legal_T_63 = xor(req.addr, UInt<17>(0h10000))
[211] FIRRTL:194194 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _put_legal_T_64 = cvt(_put_legal_T_63)
[212] FIRRTL:194195 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_65 = and(_put_legal_T_64, asSInt(UInt<33>(0h9a110000)))
[213] FIRRTL:194196 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _put_legal_T_66 = asSInt(_put_legal_T_65)
[214] FIRRTL:194197 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _put_legal_T_67 = eq(_put_legal_T_66, asSInt(UInt<1>(0h0)))
[215] FIRRTL:194198 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _put_legal_T_68 = and(_put_legal_T_62, _put_legal_T_67)
[216] FIRRTL:194199 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _put_legal_T_69 = or(UInt<1>(0h0), _put_legal_T_9)
[217] FIRRTL:194200 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _put_legal_T_70 = or(_put_legal_T_69, _put_legal_T_61)
[218] FIRRTL:194201 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node put_legal = or(_put_legal_T_70, _put_legal_T_68)
[219] FIRRTL:194202 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:480:17 KIND:wire :: wire put : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[220] FIRRTL:194203 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:481:15 KIND:connect :: connect put.opcode, UInt<1>(0h0)
[221] FIRRTL:194204 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:482:15 KIND:connect :: connect put.param, UInt<1>(0h0)
[222] FIRRTL:194205 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:483:15 KIND:connect :: connect put.size, req.uop.mem_size
[223] FIRRTL:194206 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:484:15 KIND:connect :: connect put.source, UInt<2>(0h3)
[224] FIRRTL:194207 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:485:15 KIND:connect :: connect put.address, req.addr
[225] FIRRTL:194208 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _put_a_mask_sizeOH_T = or(req.uop.mem_size, UInt<3>(0h0))
[226] FIRRTL:194209 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node put_a_mask_sizeOH_shiftAmount = bits(_put_a_mask_sizeOH_T, 1, 0)
[227] FIRRTL:194210 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _put_a_mask_sizeOH_T_1 = dshl(UInt<1>(0h1), put_a_mask_sizeOH_shiftAmount)
[228] FIRRTL:194211 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _put_a_mask_sizeOH_T_2 = bits(_put_a_mask_sizeOH_T_1, 2, 0)
[229] FIRRTL:194212 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node put_a_mask_sizeOH = or(_put_a_mask_sizeOH_T_2, UInt<1>(0h1))
[230] FIRRTL:194213 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node put_a_mask_sub_sub_sub_0_1 = geq(req.uop.mem_size, UInt<2>(0h3))
[231] FIRRTL:194214 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node put_a_mask_sub_sub_size = bits(put_a_mask_sizeOH, 2, 2)
[232] FIRRTL:194215 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node put_a_mask_sub_sub_bit = bits(req.addr, 2, 2)
[233] FIRRTL:194216 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node put_a_mask_sub_sub_nbit = eq(put_a_mask_sub_sub_bit, UInt<1>(0h0))
[234] FIRRTL:194217 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_sub_0_2 = and(UInt<1>(0h1), put_a_mask_sub_sub_nbit)
[235] FIRRTL:194218 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_sub_acc_T = and(put_a_mask_sub_sub_size, put_a_mask_sub_sub_0_2)
[236] FIRRTL:194219 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_sub_0_1 = or(put_a_mask_sub_sub_sub_0_1, _put_a_mask_sub_sub_acc_T)
[237] FIRRTL:194220 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_sub_1_2 = and(UInt<1>(0h1), put_a_mask_sub_sub_bit)
[238] FIRRTL:194221 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_sub_acc_T_1 = and(put_a_mask_sub_sub_size, put_a_mask_sub_sub_1_2)
[239] FIRRTL:194222 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_sub_1_1 = or(put_a_mask_sub_sub_sub_0_1, _put_a_mask_sub_sub_acc_T_1)
[240] FIRRTL:194223 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node put_a_mask_sub_size = bits(put_a_mask_sizeOH, 1, 1)
[241] FIRRTL:194224 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node put_a_mask_sub_bit = bits(req.addr, 1, 1)
[242] FIRRTL:194225 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node put_a_mask_sub_nbit = eq(put_a_mask_sub_bit, UInt<1>(0h0))
[243] FIRRTL:194226 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_0_2 = and(put_a_mask_sub_sub_0_2, put_a_mask_sub_nbit)
[244] FIRRTL:194227 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_acc_T = and(put_a_mask_sub_size, put_a_mask_sub_0_2)
[245] FIRRTL:194228 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_0_1 = or(put_a_mask_sub_sub_0_1, _put_a_mask_sub_acc_T)
[246] FIRRTL:194229 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_1_2 = and(put_a_mask_sub_sub_0_2, put_a_mask_sub_bit)
[247] FIRRTL:194230 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_acc_T_1 = and(put_a_mask_sub_size, put_a_mask_sub_1_2)
[248] FIRRTL:194231 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_1_1 = or(put_a_mask_sub_sub_0_1, _put_a_mask_sub_acc_T_1)
[249] FIRRTL:194232 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_2_2 = and(put_a_mask_sub_sub_1_2, put_a_mask_sub_nbit)
[250] FIRRTL:194233 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_acc_T_2 = and(put_a_mask_sub_size, put_a_mask_sub_2_2)
[251] FIRRTL:194234 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_2_1 = or(put_a_mask_sub_sub_1_1, _put_a_mask_sub_acc_T_2)
[252] FIRRTL:194235 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_sub_3_2 = and(put_a_mask_sub_sub_1_2, put_a_mask_sub_bit)
[253] FIRRTL:194236 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_sub_acc_T_3 = and(put_a_mask_sub_size, put_a_mask_sub_3_2)
[254] FIRRTL:194237 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_sub_3_1 = or(put_a_mask_sub_sub_1_1, _put_a_mask_sub_acc_T_3)
[255] FIRRTL:194238 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node put_a_mask_size = bits(put_a_mask_sizeOH, 0, 0)
[256] FIRRTL:194239 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node put_a_mask_bit = bits(req.addr, 0, 0)
[257] FIRRTL:194240 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node put_a_mask_nbit = eq(put_a_mask_bit, UInt<1>(0h0))
[258] FIRRTL:194241 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq = and(put_a_mask_sub_0_2, put_a_mask_nbit)
[259] FIRRTL:194242 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T = and(put_a_mask_size, put_a_mask_eq)
[260] FIRRTL:194243 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc = or(put_a_mask_sub_0_1, _put_a_mask_acc_T)
[261] FIRRTL:194244 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_1 = and(put_a_mask_sub_0_2, put_a_mask_bit)
[262] FIRRTL:194245 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_1 = and(put_a_mask_size, put_a_mask_eq_1)
[263] FIRRTL:194246 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_1 = or(put_a_mask_sub_0_1, _put_a_mask_acc_T_1)
[264] FIRRTL:194247 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_2 = and(put_a_mask_sub_1_2, put_a_mask_nbit)
[265] FIRRTL:194248 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_2 = and(put_a_mask_size, put_a_mask_eq_2)
[266] FIRRTL:194249 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_2 = or(put_a_mask_sub_1_1, _put_a_mask_acc_T_2)
[267] FIRRTL:194250 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_3 = and(put_a_mask_sub_1_2, put_a_mask_bit)
[268] FIRRTL:194251 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_3 = and(put_a_mask_size, put_a_mask_eq_3)
[269] FIRRTL:194252 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_3 = or(put_a_mask_sub_1_1, _put_a_mask_acc_T_3)
[270] FIRRTL:194253 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_4 = and(put_a_mask_sub_2_2, put_a_mask_nbit)
[271] FIRRTL:194254 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_4 = and(put_a_mask_size, put_a_mask_eq_4)
[272] FIRRTL:194255 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_4 = or(put_a_mask_sub_2_1, _put_a_mask_acc_T_4)
[273] FIRRTL:194256 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_5 = and(put_a_mask_sub_2_2, put_a_mask_bit)
[274] FIRRTL:194257 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_5 = and(put_a_mask_size, put_a_mask_eq_5)
[275] FIRRTL:194258 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_5 = or(put_a_mask_sub_2_1, _put_a_mask_acc_T_5)
[276] FIRRTL:194259 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_6 = and(put_a_mask_sub_3_2, put_a_mask_nbit)
[277] FIRRTL:194260 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_6 = and(put_a_mask_size, put_a_mask_eq_6)
[278] FIRRTL:194261 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_6 = or(put_a_mask_sub_3_1, _put_a_mask_acc_T_6)
[279] FIRRTL:194262 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node put_a_mask_eq_7 = and(put_a_mask_sub_3_2, put_a_mask_bit)
[280] FIRRTL:194263 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _put_a_mask_acc_T_7 = and(put_a_mask_size, put_a_mask_eq_7)
[281] FIRRTL:194264 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node put_a_mask_acc_7 = or(put_a_mask_sub_3_1, _put_a_mask_acc_T_7)
[282] FIRRTL:194265 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_lo_lo = cat(put_a_mask_acc_1, put_a_mask_acc)
[283] FIRRTL:194266 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_lo_hi = cat(put_a_mask_acc_3, put_a_mask_acc_2)
[284] FIRRTL:194267 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_lo = cat(put_a_mask_lo_hi, put_a_mask_lo_lo)
[285] FIRRTL:194268 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_hi_lo = cat(put_a_mask_acc_5, put_a_mask_acc_4)
[286] FIRRTL:194269 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_hi_hi = cat(put_a_mask_acc_7, put_a_mask_acc_6)
[287] FIRRTL:194270 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node put_a_mask_hi = cat(put_a_mask_hi_hi, put_a_mask_hi_lo)
[288] FIRRTL:194271 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _put_a_mask_T = cat(put_a_mask_hi, put_a_mask_lo)
[289] FIRRTL:194272 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:488:15 KIND:connect :: connect put.mask, _put_a_mask_T
[290] FIRRTL:194273 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:489:15 KIND:connect :: connect put.data, req.data
[291] FIRRTL:194274 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:490:15 KIND:connect :: connect put.corrupt, UInt<1>(0h0)
[292] FIRRTL:194275 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:wire :: wire _atomics_WIRE : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[293] FIRRTL:194276 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.corrupt, UInt<1>(0h0)
[294] FIRRTL:194277 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.data, UInt<64>(0h0)
[295] FIRRTL:194278 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.mask, UInt<8>(0h0)
[296] FIRRTL:194279 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.address, UInt<32>(0h0)
[297] FIRRTL:194280 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.source, UInt<2>(0h0)
[298] FIRRTL:194281 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.size, UInt<4>(0h0)
[299] FIRRTL:194282 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.param, UInt<3>(0h0)
[300] FIRRTL:194283 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:46 KIND:connect :: connect _atomics_WIRE.opcode, UInt<3>(0h0)
[301] FIRRTL:194284 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T = leq(UInt<1>(0h0), req.uop.mem_size)
[302] FIRRTL:194285 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_1 = leq(req.uop.mem_size, UInt<2>(0h3))
[303] FIRRTL:194286 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_2 = and(_atomics_legal_T, _atomics_legal_T_1)
[304] FIRRTL:194287 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_3 = or(UInt<1>(0h0), _atomics_legal_T_2)
[305] FIRRTL:194288 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_4 = xor(req.addr, UInt<1>(0h0))
[306] FIRRTL:194289 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_5 = cvt(_atomics_legal_T_4)
[307] FIRRTL:194290 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_6 = and(_atomics_legal_T_5, asSInt(UInt<33>(0h98110000)))
[308] FIRRTL:194291 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_7 = asSInt(_atomics_legal_T_6)
[309] FIRRTL:194292 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_8 = eq(_atomics_legal_T_7, asSInt(UInt<1>(0h0)))
[310] FIRRTL:194293 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_9 = xor(req.addr, UInt<21>(0h100000))
[311] FIRRTL:194294 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_10 = cvt(_atomics_legal_T_9)
[312] FIRRTL:194295 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_11 = and(_atomics_legal_T_10, asSInt(UInt<33>(0h9a101000)))
[313] FIRRTL:194296 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_12 = asSInt(_atomics_legal_T_11)
[314] FIRRTL:194297 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_13 = eq(_atomics_legal_T_12, asSInt(UInt<1>(0h0)))
[315] FIRRTL:194298 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_14 = xor(req.addr, UInt<26>(0h2010000))
[316] FIRRTL:194299 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_15 = cvt(_atomics_legal_T_14)
[317] FIRRTL:194300 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_16 = and(_atomics_legal_T_15, asSInt(UInt<33>(0h9a111000)))
[318] FIRRTL:194301 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_17 = asSInt(_atomics_legal_T_16)
[319] FIRRTL:194302 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_18 = eq(_atomics_legal_T_17, asSInt(UInt<1>(0h0)))
[320] FIRRTL:194303 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_19 = xor(req.addr, UInt<28>(0h8000000))
[321] FIRRTL:194304 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_20 = cvt(_atomics_legal_T_19)
[322] FIRRTL:194305 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_21 = and(_atomics_legal_T_20, asSInt(UInt<33>(0h98000000)))
[323] FIRRTL:194306 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_22 = asSInt(_atomics_legal_T_21)
[324] FIRRTL:194307 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_23 = eq(_atomics_legal_T_22, asSInt(UInt<1>(0h0)))
[325] FIRRTL:194308 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_24 = xor(req.addr, UInt<28>(0h8000000))
[326] FIRRTL:194309 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_25 = cvt(_atomics_legal_T_24)
[327] FIRRTL:194310 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_26 = and(_atomics_legal_T_25, asSInt(UInt<33>(0h9a110000)))
[328] FIRRTL:194311 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_27 = asSInt(_atomics_legal_T_26)
[329] FIRRTL:194312 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_28 = eq(_atomics_legal_T_27, asSInt(UInt<1>(0h0)))
[330] FIRRTL:194313 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_29 = xor(req.addr, UInt<29>(0h10000000))
[331] FIRRTL:194314 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_30 = cvt(_atomics_legal_T_29)
[332] FIRRTL:194315 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_31 = and(_atomics_legal_T_30, asSInt(UInt<33>(0h9a111000)))
[333] FIRRTL:194316 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_32 = asSInt(_atomics_legal_T_31)
[334] FIRRTL:194317 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_33 = eq(_atomics_legal_T_32, asSInt(UInt<1>(0h0)))
[335] FIRRTL:194318 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_34 = xor(req.addr, UInt<32>(0h80000000))
[336] FIRRTL:194319 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_35 = cvt(_atomics_legal_T_34)
[337] FIRRTL:194320 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_36 = and(_atomics_legal_T_35, asSInt(UInt<33>(0h90000000)))
[338] FIRRTL:194321 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_37 = asSInt(_atomics_legal_T_36)
[339] FIRRTL:194322 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_38 = eq(_atomics_legal_T_37, asSInt(UInt<1>(0h0)))
[340] FIRRTL:194323 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_39 = or(_atomics_legal_T_8, _atomics_legal_T_13)
[341] FIRRTL:194324 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_40 = or(_atomics_legal_T_39, _atomics_legal_T_18)
[342] FIRRTL:194325 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_41 = or(_atomics_legal_T_40, _atomics_legal_T_23)
[343] FIRRTL:194326 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_42 = or(_atomics_legal_T_41, _atomics_legal_T_28)
[344] FIRRTL:194327 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_43 = or(_atomics_legal_T_42, _atomics_legal_T_33)
[345] FIRRTL:194328 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_44 = or(_atomics_legal_T_43, _atomics_legal_T_38)
[346] FIRRTL:194329 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_45 = and(_atomics_legal_T_3, _atomics_legal_T_44)
[347] FIRRTL:194330 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_46 = or(UInt<1>(0h0), UInt<1>(0h0))
[348] FIRRTL:194331 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_47 = xor(req.addr, UInt<17>(0h10000))
[349] FIRRTL:194332 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_48 = cvt(_atomics_legal_T_47)
[350] FIRRTL:194333 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_49 = and(_atomics_legal_T_48, asSInt(UInt<33>(0h9a110000)))
[351] FIRRTL:194334 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_50 = asSInt(_atomics_legal_T_49)
[352] FIRRTL:194335 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_51 = eq(_atomics_legal_T_50, asSInt(UInt<1>(0h0)))
[353] FIRRTL:194336 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_52 = and(_atomics_legal_T_46, _atomics_legal_T_51)
[354] FIRRTL:194337 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_53 = or(UInt<1>(0h0), _atomics_legal_T_45)
[355] FIRRTL:194338 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal = or(_atomics_legal_T_53, _atomics_legal_T_52)
[356] FIRRTL:194339 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:534:17 KIND:wire :: wire atomics_a : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[357] FIRRTL:194340 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:535:15 KIND:connect :: connect atomics_a.opcode, UInt<2>(0h3)
[358] FIRRTL:194341 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:536:15 KIND:connect :: connect atomics_a.param, UInt<3>(0h3)
[359] FIRRTL:194342 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:537:15 KIND:connect :: connect atomics_a.size, req.uop.mem_size
[360] FIRRTL:194343 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:538:15 KIND:connect :: connect atomics_a.source, UInt<2>(0h3)
[361] FIRRTL:194344 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:539:15 KIND:connect :: connect atomics_a.address, req.addr
[362] FIRRTL:194345 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T = or(req.uop.mem_size, UInt<3>(0h0))
[363] FIRRTL:194346 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount = bits(_atomics_a_mask_sizeOH_T, 1, 0)
[364] FIRRTL:194347 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_1 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount)
[365] FIRRTL:194348 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_2 = bits(_atomics_a_mask_sizeOH_T_1, 2, 0)
[366] FIRRTL:194349 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH = or(_atomics_a_mask_sizeOH_T_2, UInt<1>(0h1))
[367] FIRRTL:194350 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1 = geq(req.uop.mem_size, UInt<2>(0h3))
[368] FIRRTL:194351 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size = bits(atomics_a_mask_sizeOH, 2, 2)
[369] FIRRTL:194352 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit = bits(req.addr, 2, 2)
[370] FIRRTL:194353 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit = eq(atomics_a_mask_sub_sub_bit, UInt<1>(0h0))
[371] FIRRTL:194354 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit)
[372] FIRRTL:194355 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T = and(atomics_a_mask_sub_sub_size, atomics_a_mask_sub_sub_0_2)
[373] FIRRTL:194356 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1 = or(atomics_a_mask_sub_sub_sub_0_1, _atomics_a_mask_sub_sub_acc_T)
[374] FIRRTL:194357 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit)
[375] FIRRTL:194358 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_1 = and(atomics_a_mask_sub_sub_size, atomics_a_mask_sub_sub_1_2)
[376] FIRRTL:194359 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1 = or(atomics_a_mask_sub_sub_sub_0_1, _atomics_a_mask_sub_sub_acc_T_1)
[377] FIRRTL:194360 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size = bits(atomics_a_mask_sizeOH, 1, 1)
[378] FIRRTL:194361 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit = bits(req.addr, 1, 1)
[379] FIRRTL:194362 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit = eq(atomics_a_mask_sub_bit, UInt<1>(0h0))
[380] FIRRTL:194363 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2 = and(atomics_a_mask_sub_sub_0_2, atomics_a_mask_sub_nbit)
[381] FIRRTL:194364 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T = and(atomics_a_mask_sub_size, atomics_a_mask_sub_0_2)
[382] FIRRTL:194365 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1 = or(atomics_a_mask_sub_sub_0_1, _atomics_a_mask_sub_acc_T)
[383] FIRRTL:194366 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2 = and(atomics_a_mask_sub_sub_0_2, atomics_a_mask_sub_bit)
[384] FIRRTL:194367 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_1 = and(atomics_a_mask_sub_size, atomics_a_mask_sub_1_2)
[385] FIRRTL:194368 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1 = or(atomics_a_mask_sub_sub_0_1, _atomics_a_mask_sub_acc_T_1)
[386] FIRRTL:194369 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2 = and(atomics_a_mask_sub_sub_1_2, atomics_a_mask_sub_nbit)
[387] FIRRTL:194370 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_2 = and(atomics_a_mask_sub_size, atomics_a_mask_sub_2_2)
[388] FIRRTL:194371 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1 = or(atomics_a_mask_sub_sub_1_1, _atomics_a_mask_sub_acc_T_2)
[389] FIRRTL:194372 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2 = and(atomics_a_mask_sub_sub_1_2, atomics_a_mask_sub_bit)
[390] FIRRTL:194373 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_3 = and(atomics_a_mask_sub_size, atomics_a_mask_sub_3_2)
[391] FIRRTL:194374 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1 = or(atomics_a_mask_sub_sub_1_1, _atomics_a_mask_sub_acc_T_3)
[392] FIRRTL:194375 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size = bits(atomics_a_mask_sizeOH, 0, 0)
[393] FIRRTL:194376 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit = bits(req.addr, 0, 0)
[394] FIRRTL:194377 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit = eq(atomics_a_mask_bit, UInt<1>(0h0))
[395] FIRRTL:194378 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq = and(atomics_a_mask_sub_0_2, atomics_a_mask_nbit)
[396] FIRRTL:194379 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T = and(atomics_a_mask_size, atomics_a_mask_eq)
[397] FIRRTL:194380 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc = or(atomics_a_mask_sub_0_1, _atomics_a_mask_acc_T)
[398] FIRRTL:194381 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_1 = and(atomics_a_mask_sub_0_2, atomics_a_mask_bit)
[399] FIRRTL:194382 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_1 = and(atomics_a_mask_size, atomics_a_mask_eq_1)
[400] FIRRTL:194383 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_1 = or(atomics_a_mask_sub_0_1, _atomics_a_mask_acc_T_1)
[401] FIRRTL:194384 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_2 = and(atomics_a_mask_sub_1_2, atomics_a_mask_nbit)
[402] FIRRTL:194385 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_2 = and(atomics_a_mask_size, atomics_a_mask_eq_2)
[403] FIRRTL:194386 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_2 = or(atomics_a_mask_sub_1_1, _atomics_a_mask_acc_T_2)
[404] FIRRTL:194387 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_3 = and(atomics_a_mask_sub_1_2, atomics_a_mask_bit)
[405] FIRRTL:194388 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_3 = and(atomics_a_mask_size, atomics_a_mask_eq_3)
[406] FIRRTL:194389 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_3 = or(atomics_a_mask_sub_1_1, _atomics_a_mask_acc_T_3)
[407] FIRRTL:194390 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_4 = and(atomics_a_mask_sub_2_2, atomics_a_mask_nbit)
[408] FIRRTL:194391 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_4 = and(atomics_a_mask_size, atomics_a_mask_eq_4)
[409] FIRRTL:194392 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_4 = or(atomics_a_mask_sub_2_1, _atomics_a_mask_acc_T_4)
[410] FIRRTL:194393 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_5 = and(atomics_a_mask_sub_2_2, atomics_a_mask_bit)
[411] FIRRTL:194394 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_5 = and(atomics_a_mask_size, atomics_a_mask_eq_5)
[412] FIRRTL:194395 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_5 = or(atomics_a_mask_sub_2_1, _atomics_a_mask_acc_T_5)
[413] FIRRTL:194396 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_6 = and(atomics_a_mask_sub_3_2, atomics_a_mask_nbit)
[414] FIRRTL:194397 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_6 = and(atomics_a_mask_size, atomics_a_mask_eq_6)
[415] FIRRTL:194398 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_6 = or(atomics_a_mask_sub_3_1, _atomics_a_mask_acc_T_6)
[416] FIRRTL:194399 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_7 = and(atomics_a_mask_sub_3_2, atomics_a_mask_bit)
[417] FIRRTL:194400 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_7 = and(atomics_a_mask_size, atomics_a_mask_eq_7)
[418] FIRRTL:194401 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_7 = or(atomics_a_mask_sub_3_1, _atomics_a_mask_acc_T_7)
[419] FIRRTL:194402 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo = cat(atomics_a_mask_acc_1, atomics_a_mask_acc)
[420] FIRRTL:194403 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi = cat(atomics_a_mask_acc_3, atomics_a_mask_acc_2)
[421] FIRRTL:194404 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo = cat(atomics_a_mask_lo_hi, atomics_a_mask_lo_lo)
[422] FIRRTL:194405 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo = cat(atomics_a_mask_acc_5, atomics_a_mask_acc_4)
[423] FIRRTL:194406 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi = cat(atomics_a_mask_acc_7, atomics_a_mask_acc_6)
[424] FIRRTL:194407 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi = cat(atomics_a_mask_hi_hi, atomics_a_mask_hi_lo)
[425] FIRRTL:194408 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T = cat(atomics_a_mask_hi, atomics_a_mask_lo)
[426] FIRRTL:194409 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:542:15 KIND:connect :: connect atomics_a.mask, _atomics_a_mask_T
[427] FIRRTL:194410 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:543:15 KIND:connect :: connect atomics_a.data, req.data
[428] FIRRTL:194411 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:544:15 KIND:connect :: connect atomics_a.corrupt, UInt<1>(0h0)
[429] FIRRTL:194412 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_54 = leq(UInt<1>(0h0), req.uop.mem_size)
[430] FIRRTL:194413 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_55 = leq(req.uop.mem_size, UInt<2>(0h3))
[431] FIRRTL:194414 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_56 = and(_atomics_legal_T_54, _atomics_legal_T_55)
[432] FIRRTL:194415 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_57 = or(UInt<1>(0h0), _atomics_legal_T_56)
[433] FIRRTL:194416 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_58 = xor(req.addr, UInt<1>(0h0))
[434] FIRRTL:194417 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_59 = cvt(_atomics_legal_T_58)
[435] FIRRTL:194418 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_60 = and(_atomics_legal_T_59, asSInt(UInt<33>(0h98110000)))
[436] FIRRTL:194419 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_61 = asSInt(_atomics_legal_T_60)
[437] FIRRTL:194420 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_62 = eq(_atomics_legal_T_61, asSInt(UInt<1>(0h0)))
[438] FIRRTL:194421 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_63 = xor(req.addr, UInt<21>(0h100000))
[439] FIRRTL:194422 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_64 = cvt(_atomics_legal_T_63)
[440] FIRRTL:194423 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_65 = and(_atomics_legal_T_64, asSInt(UInt<33>(0h9a101000)))
[441] FIRRTL:194424 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_66 = asSInt(_atomics_legal_T_65)
[442] FIRRTL:194425 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_67 = eq(_atomics_legal_T_66, asSInt(UInt<1>(0h0)))
[443] FIRRTL:194426 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_68 = xor(req.addr, UInt<26>(0h2010000))
[444] FIRRTL:194427 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_69 = cvt(_atomics_legal_T_68)
[445] FIRRTL:194428 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_70 = and(_atomics_legal_T_69, asSInt(UInt<33>(0h9a111000)))
[446] FIRRTL:194429 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_71 = asSInt(_atomics_legal_T_70)
[447] FIRRTL:194430 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_72 = eq(_atomics_legal_T_71, asSInt(UInt<1>(0h0)))
[448] FIRRTL:194431 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_73 = xor(req.addr, UInt<28>(0h8000000))
[449] FIRRTL:194432 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_74 = cvt(_atomics_legal_T_73)
[450] FIRRTL:194433 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_75 = and(_atomics_legal_T_74, asSInt(UInt<33>(0h98000000)))
[451] FIRRTL:194434 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_76 = asSInt(_atomics_legal_T_75)
[452] FIRRTL:194435 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_77 = eq(_atomics_legal_T_76, asSInt(UInt<1>(0h0)))
[453] FIRRTL:194436 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_78 = xor(req.addr, UInt<28>(0h8000000))
[454] FIRRTL:194437 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_79 = cvt(_atomics_legal_T_78)
[455] FIRRTL:194438 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_80 = and(_atomics_legal_T_79, asSInt(UInt<33>(0h9a110000)))
[456] FIRRTL:194439 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_81 = asSInt(_atomics_legal_T_80)
[457] FIRRTL:194440 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_82 = eq(_atomics_legal_T_81, asSInt(UInt<1>(0h0)))
[458] FIRRTL:194441 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_83 = xor(req.addr, UInt<29>(0h10000000))
[459] FIRRTL:194442 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_84 = cvt(_atomics_legal_T_83)
[460] FIRRTL:194443 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_85 = and(_atomics_legal_T_84, asSInt(UInt<33>(0h9a111000)))
[461] FIRRTL:194444 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_86 = asSInt(_atomics_legal_T_85)
[462] FIRRTL:194445 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_87 = eq(_atomics_legal_T_86, asSInt(UInt<1>(0h0)))
[463] FIRRTL:194446 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_88 = xor(req.addr, UInt<32>(0h80000000))
[464] FIRRTL:194447 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_89 = cvt(_atomics_legal_T_88)
[465] FIRRTL:194448 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_90 = and(_atomics_legal_T_89, asSInt(UInt<33>(0h90000000)))
[466] FIRRTL:194449 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_91 = asSInt(_atomics_legal_T_90)
[467] FIRRTL:194450 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_92 = eq(_atomics_legal_T_91, asSInt(UInt<1>(0h0)))
[468] FIRRTL:194451 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_93 = or(_atomics_legal_T_62, _atomics_legal_T_67)
[469] FIRRTL:194452 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_94 = or(_atomics_legal_T_93, _atomics_legal_T_72)
[470] FIRRTL:194453 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_95 = or(_atomics_legal_T_94, _atomics_legal_T_77)
[471] FIRRTL:194454 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_96 = or(_atomics_legal_T_95, _atomics_legal_T_82)
[472] FIRRTL:194455 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_97 = or(_atomics_legal_T_96, _atomics_legal_T_87)
[473] FIRRTL:194456 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_98 = or(_atomics_legal_T_97, _atomics_legal_T_92)
[474] FIRRTL:194457 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_99 = and(_atomics_legal_T_57, _atomics_legal_T_98)
[475] FIRRTL:194458 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_100 = or(UInt<1>(0h0), UInt<1>(0h0))
[476] FIRRTL:194459 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_101 = xor(req.addr, UInt<17>(0h10000))
[477] FIRRTL:194460 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_102 = cvt(_atomics_legal_T_101)
[478] FIRRTL:194461 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_103 = and(_atomics_legal_T_102, asSInt(UInt<33>(0h9a110000)))
[479] FIRRTL:194462 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_104 = asSInt(_atomics_legal_T_103)
[480] FIRRTL:194463 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_105 = eq(_atomics_legal_T_104, asSInt(UInt<1>(0h0)))
[481] FIRRTL:194464 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_106 = and(_atomics_legal_T_100, _atomics_legal_T_105)
[482] FIRRTL:194465 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_107 = or(UInt<1>(0h0), _atomics_legal_T_99)
[483] FIRRTL:194466 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_1 = or(_atomics_legal_T_107, _atomics_legal_T_106)
[484] FIRRTL:194467 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:534:17 KIND:wire :: wire atomics_a_1 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[485] FIRRTL:194468 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:535:15 KIND:connect :: connect atomics_a_1.opcode, UInt<2>(0h3)
[486] FIRRTL:194469 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:536:15 KIND:connect :: connect atomics_a_1.param, UInt<3>(0h0)
[487] FIRRTL:194470 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:537:15 KIND:connect :: connect atomics_a_1.size, req.uop.mem_size
[488] FIRRTL:194471 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:538:15 KIND:connect :: connect atomics_a_1.source, UInt<2>(0h3)
[489] FIRRTL:194472 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:539:15 KIND:connect :: connect atomics_a_1.address, req.addr
[490] FIRRTL:194473 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_3 = or(req.uop.mem_size, UInt<3>(0h0))
[491] FIRRTL:194474 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_1 = bits(_atomics_a_mask_sizeOH_T_3, 1, 0)
[492] FIRRTL:194475 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_4 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_1)
[493] FIRRTL:194476 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_5 = bits(_atomics_a_mask_sizeOH_T_4, 2, 0)
[494] FIRRTL:194477 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_1 = or(_atomics_a_mask_sizeOH_T_5, UInt<1>(0h1))
[495] FIRRTL:194478 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_1 = geq(req.uop.mem_size, UInt<2>(0h3))
[496] FIRRTL:194479 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_1 = bits(atomics_a_mask_sizeOH_1, 2, 2)
[497] FIRRTL:194480 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_1 = bits(req.addr, 2, 2)
[498] FIRRTL:194481 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_1 = eq(atomics_a_mask_sub_sub_bit_1, UInt<1>(0h0))
[499] FIRRTL:194482 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_1 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_1)
[500] FIRRTL:194483 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_2 = and(atomics_a_mask_sub_sub_size_1, atomics_a_mask_sub_sub_0_2_1)
[501] FIRRTL:194484 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_1 = or(atomics_a_mask_sub_sub_sub_0_1_1, _atomics_a_mask_sub_sub_acc_T_2)
[502] FIRRTL:194485 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_1 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_1)
[503] FIRRTL:194486 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_3 = and(atomics_a_mask_sub_sub_size_1, atomics_a_mask_sub_sub_1_2_1)
[504] FIRRTL:194487 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_1 = or(atomics_a_mask_sub_sub_sub_0_1_1, _atomics_a_mask_sub_sub_acc_T_3)
[505] FIRRTL:194488 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_1 = bits(atomics_a_mask_sizeOH_1, 1, 1)
[506] FIRRTL:194489 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_1 = bits(req.addr, 1, 1)
[507] FIRRTL:194490 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_1 = eq(atomics_a_mask_sub_bit_1, UInt<1>(0h0))
[508] FIRRTL:194491 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_1 = and(atomics_a_mask_sub_sub_0_2_1, atomics_a_mask_sub_nbit_1)
[509] FIRRTL:194492 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_4 = and(atomics_a_mask_sub_size_1, atomics_a_mask_sub_0_2_1)
[510] FIRRTL:194493 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_1 = or(atomics_a_mask_sub_sub_0_1_1, _atomics_a_mask_sub_acc_T_4)
[511] FIRRTL:194494 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_1 = and(atomics_a_mask_sub_sub_0_2_1, atomics_a_mask_sub_bit_1)
[512] FIRRTL:194495 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_5 = and(atomics_a_mask_sub_size_1, atomics_a_mask_sub_1_2_1)
[513] FIRRTL:194496 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_1 = or(atomics_a_mask_sub_sub_0_1_1, _atomics_a_mask_sub_acc_T_5)
[514] FIRRTL:194497 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_1 = and(atomics_a_mask_sub_sub_1_2_1, atomics_a_mask_sub_nbit_1)
[515] FIRRTL:194498 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_6 = and(atomics_a_mask_sub_size_1, atomics_a_mask_sub_2_2_1)
[516] FIRRTL:194499 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_1 = or(atomics_a_mask_sub_sub_1_1_1, _atomics_a_mask_sub_acc_T_6)
[517] FIRRTL:194500 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_1 = and(atomics_a_mask_sub_sub_1_2_1, atomics_a_mask_sub_bit_1)
[518] FIRRTL:194501 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_7 = and(atomics_a_mask_sub_size_1, atomics_a_mask_sub_3_2_1)
[519] FIRRTL:194502 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_1 = or(atomics_a_mask_sub_sub_1_1_1, _atomics_a_mask_sub_acc_T_7)
[520] FIRRTL:194503 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_1 = bits(atomics_a_mask_sizeOH_1, 0, 0)
[521] FIRRTL:194504 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_1 = bits(req.addr, 0, 0)
[522] FIRRTL:194505 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_1 = eq(atomics_a_mask_bit_1, UInt<1>(0h0))
[523] FIRRTL:194506 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_8 = and(atomics_a_mask_sub_0_2_1, atomics_a_mask_nbit_1)
[524] FIRRTL:194507 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_8 = and(atomics_a_mask_size_1, atomics_a_mask_eq_8)
[525] FIRRTL:194508 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_8 = or(atomics_a_mask_sub_0_1_1, _atomics_a_mask_acc_T_8)
[526] FIRRTL:194509 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_9 = and(atomics_a_mask_sub_0_2_1, atomics_a_mask_bit_1)
[527] FIRRTL:194510 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_9 = and(atomics_a_mask_size_1, atomics_a_mask_eq_9)
[528] FIRRTL:194511 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_9 = or(atomics_a_mask_sub_0_1_1, _atomics_a_mask_acc_T_9)
[529] FIRRTL:194512 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_10 = and(atomics_a_mask_sub_1_2_1, atomics_a_mask_nbit_1)
[530] FIRRTL:194513 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_10 = and(atomics_a_mask_size_1, atomics_a_mask_eq_10)
[531] FIRRTL:194514 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_10 = or(atomics_a_mask_sub_1_1_1, _atomics_a_mask_acc_T_10)
[532] FIRRTL:194515 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_11 = and(atomics_a_mask_sub_1_2_1, atomics_a_mask_bit_1)
[533] FIRRTL:194516 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_11 = and(atomics_a_mask_size_1, atomics_a_mask_eq_11)
[534] FIRRTL:194517 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_11 = or(atomics_a_mask_sub_1_1_1, _atomics_a_mask_acc_T_11)
[535] FIRRTL:194518 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_12 = and(atomics_a_mask_sub_2_2_1, atomics_a_mask_nbit_1)
[536] FIRRTL:194519 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_12 = and(atomics_a_mask_size_1, atomics_a_mask_eq_12)
[537] FIRRTL:194520 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_12 = or(atomics_a_mask_sub_2_1_1, _atomics_a_mask_acc_T_12)
[538] FIRRTL:194521 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_13 = and(atomics_a_mask_sub_2_2_1, atomics_a_mask_bit_1)
[539] FIRRTL:194522 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_13 = and(atomics_a_mask_size_1, atomics_a_mask_eq_13)
[540] FIRRTL:194523 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_13 = or(atomics_a_mask_sub_2_1_1, _atomics_a_mask_acc_T_13)
[541] FIRRTL:194524 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_14 = and(atomics_a_mask_sub_3_2_1, atomics_a_mask_nbit_1)
[542] FIRRTL:194525 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_14 = and(atomics_a_mask_size_1, atomics_a_mask_eq_14)
[543] FIRRTL:194526 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_14 = or(atomics_a_mask_sub_3_1_1, _atomics_a_mask_acc_T_14)
[544] FIRRTL:194527 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_15 = and(atomics_a_mask_sub_3_2_1, atomics_a_mask_bit_1)
[545] FIRRTL:194528 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_15 = and(atomics_a_mask_size_1, atomics_a_mask_eq_15)
[546] FIRRTL:194529 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_15 = or(atomics_a_mask_sub_3_1_1, _atomics_a_mask_acc_T_15)
[547] FIRRTL:194530 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_1 = cat(atomics_a_mask_acc_9, atomics_a_mask_acc_8)
[548] FIRRTL:194531 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_1 = cat(atomics_a_mask_acc_11, atomics_a_mask_acc_10)
[549] FIRRTL:194532 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_1 = cat(atomics_a_mask_lo_hi_1, atomics_a_mask_lo_lo_1)
[550] FIRRTL:194533 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_1 = cat(atomics_a_mask_acc_13, atomics_a_mask_acc_12)
[551] FIRRTL:194534 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_1 = cat(atomics_a_mask_acc_15, atomics_a_mask_acc_14)
[552] FIRRTL:194535 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_1 = cat(atomics_a_mask_hi_hi_1, atomics_a_mask_hi_lo_1)
[553] FIRRTL:194536 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_1 = cat(atomics_a_mask_hi_1, atomics_a_mask_lo_1)
[554] FIRRTL:194537 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:542:15 KIND:connect :: connect atomics_a_1.mask, _atomics_a_mask_T_1
[555] FIRRTL:194538 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:543:15 KIND:connect :: connect atomics_a_1.data, req.data
[556] FIRRTL:194539 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:544:15 KIND:connect :: connect atomics_a_1.corrupt, UInt<1>(0h0)
[557] FIRRTL:194540 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_108 = leq(UInt<1>(0h0), req.uop.mem_size)
[558] FIRRTL:194541 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_109 = leq(req.uop.mem_size, UInt<2>(0h3))
[559] FIRRTL:194542 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_110 = and(_atomics_legal_T_108, _atomics_legal_T_109)
[560] FIRRTL:194543 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_111 = or(UInt<1>(0h0), _atomics_legal_T_110)
[561] FIRRTL:194544 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_112 = xor(req.addr, UInt<1>(0h0))
[562] FIRRTL:194545 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_113 = cvt(_atomics_legal_T_112)
[563] FIRRTL:194546 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_114 = and(_atomics_legal_T_113, asSInt(UInt<33>(0h98110000)))
[564] FIRRTL:194547 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_115 = asSInt(_atomics_legal_T_114)
[565] FIRRTL:194548 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_116 = eq(_atomics_legal_T_115, asSInt(UInt<1>(0h0)))
[566] FIRRTL:194549 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_117 = xor(req.addr, UInt<21>(0h100000))
[567] FIRRTL:194550 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_118 = cvt(_atomics_legal_T_117)
[568] FIRRTL:194551 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_119 = and(_atomics_legal_T_118, asSInt(UInt<33>(0h9a101000)))
[569] FIRRTL:194552 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_120 = asSInt(_atomics_legal_T_119)
[570] FIRRTL:194553 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_121 = eq(_atomics_legal_T_120, asSInt(UInt<1>(0h0)))
[571] FIRRTL:194554 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_122 = xor(req.addr, UInt<26>(0h2010000))
[572] FIRRTL:194555 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_123 = cvt(_atomics_legal_T_122)
[573] FIRRTL:194556 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_124 = and(_atomics_legal_T_123, asSInt(UInt<33>(0h9a111000)))
[574] FIRRTL:194557 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_125 = asSInt(_atomics_legal_T_124)
[575] FIRRTL:194558 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_126 = eq(_atomics_legal_T_125, asSInt(UInt<1>(0h0)))
[576] FIRRTL:194559 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_127 = xor(req.addr, UInt<28>(0h8000000))
[577] FIRRTL:194560 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_128 = cvt(_atomics_legal_T_127)
[578] FIRRTL:194561 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_129 = and(_atomics_legal_T_128, asSInt(UInt<33>(0h98000000)))
[579] FIRRTL:194562 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_130 = asSInt(_atomics_legal_T_129)
[580] FIRRTL:194563 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_131 = eq(_atomics_legal_T_130, asSInt(UInt<1>(0h0)))
[581] FIRRTL:194564 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_132 = xor(req.addr, UInt<28>(0h8000000))
[582] FIRRTL:194565 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_133 = cvt(_atomics_legal_T_132)
[583] FIRRTL:194566 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_134 = and(_atomics_legal_T_133, asSInt(UInt<33>(0h9a110000)))
[584] FIRRTL:194567 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_135 = asSInt(_atomics_legal_T_134)
[585] FIRRTL:194568 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_136 = eq(_atomics_legal_T_135, asSInt(UInt<1>(0h0)))
[586] FIRRTL:194569 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_137 = xor(req.addr, UInt<29>(0h10000000))
[587] FIRRTL:194570 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_138 = cvt(_atomics_legal_T_137)
[588] FIRRTL:194571 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_139 = and(_atomics_legal_T_138, asSInt(UInt<33>(0h9a111000)))
[589] FIRRTL:194572 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_140 = asSInt(_atomics_legal_T_139)
[590] FIRRTL:194573 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_141 = eq(_atomics_legal_T_140, asSInt(UInt<1>(0h0)))
[591] FIRRTL:194574 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_142 = xor(req.addr, UInt<32>(0h80000000))
[592] FIRRTL:194575 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_143 = cvt(_atomics_legal_T_142)
[593] FIRRTL:194576 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_144 = and(_atomics_legal_T_143, asSInt(UInt<33>(0h90000000)))
[594] FIRRTL:194577 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_145 = asSInt(_atomics_legal_T_144)
[595] FIRRTL:194578 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_146 = eq(_atomics_legal_T_145, asSInt(UInt<1>(0h0)))
[596] FIRRTL:194579 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_147 = or(_atomics_legal_T_116, _atomics_legal_T_121)
[597] FIRRTL:194580 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_148 = or(_atomics_legal_T_147, _atomics_legal_T_126)
[598] FIRRTL:194581 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_149 = or(_atomics_legal_T_148, _atomics_legal_T_131)
[599] FIRRTL:194582 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_150 = or(_atomics_legal_T_149, _atomics_legal_T_136)
[600] FIRRTL:194583 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_151 = or(_atomics_legal_T_150, _atomics_legal_T_141)
[601] FIRRTL:194584 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_152 = or(_atomics_legal_T_151, _atomics_legal_T_146)
[602] FIRRTL:194585 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_153 = and(_atomics_legal_T_111, _atomics_legal_T_152)
[603] FIRRTL:194586 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_154 = or(UInt<1>(0h0), UInt<1>(0h0))
[604] FIRRTL:194587 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_155 = xor(req.addr, UInt<17>(0h10000))
[605] FIRRTL:194588 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_156 = cvt(_atomics_legal_T_155)
[606] FIRRTL:194589 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_157 = and(_atomics_legal_T_156, asSInt(UInt<33>(0h9a110000)))
[607] FIRRTL:194590 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_158 = asSInt(_atomics_legal_T_157)
[608] FIRRTL:194591 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_159 = eq(_atomics_legal_T_158, asSInt(UInt<1>(0h0)))
[609] FIRRTL:194592 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_160 = and(_atomics_legal_T_154, _atomics_legal_T_159)
[610] FIRRTL:194593 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_161 = or(UInt<1>(0h0), _atomics_legal_T_153)
[611] FIRRTL:194594 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_2 = or(_atomics_legal_T_161, _atomics_legal_T_160)
[612] FIRRTL:194595 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:534:17 KIND:wire :: wire atomics_a_2 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[613] FIRRTL:194596 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:535:15 KIND:connect :: connect atomics_a_2.opcode, UInt<2>(0h3)
[614] FIRRTL:194597 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:536:15 KIND:connect :: connect atomics_a_2.param, UInt<3>(0h1)
[615] FIRRTL:194598 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:537:15 KIND:connect :: connect atomics_a_2.size, req.uop.mem_size
[616] FIRRTL:194599 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:538:15 KIND:connect :: connect atomics_a_2.source, UInt<2>(0h3)
[617] FIRRTL:194600 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:539:15 KIND:connect :: connect atomics_a_2.address, req.addr
[618] FIRRTL:194601 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_6 = or(req.uop.mem_size, UInt<3>(0h0))
[619] FIRRTL:194602 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_2 = bits(_atomics_a_mask_sizeOH_T_6, 1, 0)
[620] FIRRTL:194603 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_7 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_2)
[621] FIRRTL:194604 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_8 = bits(_atomics_a_mask_sizeOH_T_7, 2, 0)
[622] FIRRTL:194605 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_2 = or(_atomics_a_mask_sizeOH_T_8, UInt<1>(0h1))
[623] FIRRTL:194606 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_2 = geq(req.uop.mem_size, UInt<2>(0h3))
[624] FIRRTL:194607 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_2 = bits(atomics_a_mask_sizeOH_2, 2, 2)
[625] FIRRTL:194608 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_2 = bits(req.addr, 2, 2)
[626] FIRRTL:194609 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_2 = eq(atomics_a_mask_sub_sub_bit_2, UInt<1>(0h0))
[627] FIRRTL:194610 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_2 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_2)
[628] FIRRTL:194611 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_4 = and(atomics_a_mask_sub_sub_size_2, atomics_a_mask_sub_sub_0_2_2)
[629] FIRRTL:194612 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_2 = or(atomics_a_mask_sub_sub_sub_0_1_2, _atomics_a_mask_sub_sub_acc_T_4)
[630] FIRRTL:194613 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_2 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_2)
[631] FIRRTL:194614 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_5 = and(atomics_a_mask_sub_sub_size_2, atomics_a_mask_sub_sub_1_2_2)
[632] FIRRTL:194615 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_2 = or(atomics_a_mask_sub_sub_sub_0_1_2, _atomics_a_mask_sub_sub_acc_T_5)
[633] FIRRTL:194616 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_2 = bits(atomics_a_mask_sizeOH_2, 1, 1)
[634] FIRRTL:194617 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_2 = bits(req.addr, 1, 1)
[635] FIRRTL:194618 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_2 = eq(atomics_a_mask_sub_bit_2, UInt<1>(0h0))
[636] FIRRTL:194619 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_2 = and(atomics_a_mask_sub_sub_0_2_2, atomics_a_mask_sub_nbit_2)
[637] FIRRTL:194620 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_8 = and(atomics_a_mask_sub_size_2, atomics_a_mask_sub_0_2_2)
[638] FIRRTL:194621 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_2 = or(atomics_a_mask_sub_sub_0_1_2, _atomics_a_mask_sub_acc_T_8)
[639] FIRRTL:194622 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_2 = and(atomics_a_mask_sub_sub_0_2_2, atomics_a_mask_sub_bit_2)
[640] FIRRTL:194623 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_9 = and(atomics_a_mask_sub_size_2, atomics_a_mask_sub_1_2_2)
[641] FIRRTL:194624 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_2 = or(atomics_a_mask_sub_sub_0_1_2, _atomics_a_mask_sub_acc_T_9)
[642] FIRRTL:194625 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_2 = and(atomics_a_mask_sub_sub_1_2_2, atomics_a_mask_sub_nbit_2)
[643] FIRRTL:194626 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_10 = and(atomics_a_mask_sub_size_2, atomics_a_mask_sub_2_2_2)
[644] FIRRTL:194627 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_2 = or(atomics_a_mask_sub_sub_1_1_2, _atomics_a_mask_sub_acc_T_10)
[645] FIRRTL:194628 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_2 = and(atomics_a_mask_sub_sub_1_2_2, atomics_a_mask_sub_bit_2)
[646] FIRRTL:194629 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_11 = and(atomics_a_mask_sub_size_2, atomics_a_mask_sub_3_2_2)
[647] FIRRTL:194630 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_2 = or(atomics_a_mask_sub_sub_1_1_2, _atomics_a_mask_sub_acc_T_11)
[648] FIRRTL:194631 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_2 = bits(atomics_a_mask_sizeOH_2, 0, 0)
[649] FIRRTL:194632 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_2 = bits(req.addr, 0, 0)
[650] FIRRTL:194633 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_2 = eq(atomics_a_mask_bit_2, UInt<1>(0h0))
[651] FIRRTL:194634 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_16 = and(atomics_a_mask_sub_0_2_2, atomics_a_mask_nbit_2)
[652] FIRRTL:194635 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_16 = and(atomics_a_mask_size_2, atomics_a_mask_eq_16)
[653] FIRRTL:194636 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_16 = or(atomics_a_mask_sub_0_1_2, _atomics_a_mask_acc_T_16)
[654] FIRRTL:194637 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_17 = and(atomics_a_mask_sub_0_2_2, atomics_a_mask_bit_2)
[655] FIRRTL:194638 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_17 = and(atomics_a_mask_size_2, atomics_a_mask_eq_17)
[656] FIRRTL:194639 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_17 = or(atomics_a_mask_sub_0_1_2, _atomics_a_mask_acc_T_17)
[657] FIRRTL:194640 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_18 = and(atomics_a_mask_sub_1_2_2, atomics_a_mask_nbit_2)
[658] FIRRTL:194641 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_18 = and(atomics_a_mask_size_2, atomics_a_mask_eq_18)
[659] FIRRTL:194642 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_18 = or(atomics_a_mask_sub_1_1_2, _atomics_a_mask_acc_T_18)
[660] FIRRTL:194643 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_19 = and(atomics_a_mask_sub_1_2_2, atomics_a_mask_bit_2)
[661] FIRRTL:194644 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_19 = and(atomics_a_mask_size_2, atomics_a_mask_eq_19)
[662] FIRRTL:194645 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_19 = or(atomics_a_mask_sub_1_1_2, _atomics_a_mask_acc_T_19)
[663] FIRRTL:194646 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_20 = and(atomics_a_mask_sub_2_2_2, atomics_a_mask_nbit_2)
[664] FIRRTL:194647 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_20 = and(atomics_a_mask_size_2, atomics_a_mask_eq_20)
[665] FIRRTL:194648 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_20 = or(atomics_a_mask_sub_2_1_2, _atomics_a_mask_acc_T_20)
[666] FIRRTL:194649 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_21 = and(atomics_a_mask_sub_2_2_2, atomics_a_mask_bit_2)
[667] FIRRTL:194650 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_21 = and(atomics_a_mask_size_2, atomics_a_mask_eq_21)
[668] FIRRTL:194651 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_21 = or(atomics_a_mask_sub_2_1_2, _atomics_a_mask_acc_T_21)
[669] FIRRTL:194652 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_22 = and(atomics_a_mask_sub_3_2_2, atomics_a_mask_nbit_2)
[670] FIRRTL:194653 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_22 = and(atomics_a_mask_size_2, atomics_a_mask_eq_22)
[671] FIRRTL:194654 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_22 = or(atomics_a_mask_sub_3_1_2, _atomics_a_mask_acc_T_22)
[672] FIRRTL:194655 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_23 = and(atomics_a_mask_sub_3_2_2, atomics_a_mask_bit_2)
[673] FIRRTL:194656 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_23 = and(atomics_a_mask_size_2, atomics_a_mask_eq_23)
[674] FIRRTL:194657 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_23 = or(atomics_a_mask_sub_3_1_2, _atomics_a_mask_acc_T_23)
[675] FIRRTL:194658 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_2 = cat(atomics_a_mask_acc_17, atomics_a_mask_acc_16)
[676] FIRRTL:194659 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_2 = cat(atomics_a_mask_acc_19, atomics_a_mask_acc_18)
[677] FIRRTL:194660 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_2 = cat(atomics_a_mask_lo_hi_2, atomics_a_mask_lo_lo_2)
[678] FIRRTL:194661 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_2 = cat(atomics_a_mask_acc_21, atomics_a_mask_acc_20)
[679] FIRRTL:194662 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_2 = cat(atomics_a_mask_acc_23, atomics_a_mask_acc_22)
[680] FIRRTL:194663 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_2 = cat(atomics_a_mask_hi_hi_2, atomics_a_mask_hi_lo_2)
[681] FIRRTL:194664 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_2 = cat(atomics_a_mask_hi_2, atomics_a_mask_lo_2)
[682] FIRRTL:194665 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:542:15 KIND:connect :: connect atomics_a_2.mask, _atomics_a_mask_T_2
[683] FIRRTL:194666 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:543:15 KIND:connect :: connect atomics_a_2.data, req.data
[684] FIRRTL:194667 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:544:15 KIND:connect :: connect atomics_a_2.corrupt, UInt<1>(0h0)
[685] FIRRTL:194668 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_162 = leq(UInt<1>(0h0), req.uop.mem_size)
[686] FIRRTL:194669 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_163 = leq(req.uop.mem_size, UInt<2>(0h3))
[687] FIRRTL:194670 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_164 = and(_atomics_legal_T_162, _atomics_legal_T_163)
[688] FIRRTL:194671 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_165 = or(UInt<1>(0h0), _atomics_legal_T_164)
[689] FIRRTL:194672 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_166 = xor(req.addr, UInt<1>(0h0))
[690] FIRRTL:194673 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_167 = cvt(_atomics_legal_T_166)
[691] FIRRTL:194674 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_168 = and(_atomics_legal_T_167, asSInt(UInt<33>(0h98110000)))
[692] FIRRTL:194675 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_169 = asSInt(_atomics_legal_T_168)
[693] FIRRTL:194676 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_170 = eq(_atomics_legal_T_169, asSInt(UInt<1>(0h0)))
[694] FIRRTL:194677 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_171 = xor(req.addr, UInt<21>(0h100000))
[695] FIRRTL:194678 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_172 = cvt(_atomics_legal_T_171)
[696] FIRRTL:194679 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_173 = and(_atomics_legal_T_172, asSInt(UInt<33>(0h9a101000)))
[697] FIRRTL:194680 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_174 = asSInt(_atomics_legal_T_173)
[698] FIRRTL:194681 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_175 = eq(_atomics_legal_T_174, asSInt(UInt<1>(0h0)))
[699] FIRRTL:194682 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_176 = xor(req.addr, UInt<26>(0h2010000))
[700] FIRRTL:194683 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_177 = cvt(_atomics_legal_T_176)
[701] FIRRTL:194684 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_178 = and(_atomics_legal_T_177, asSInt(UInt<33>(0h9a111000)))
[702] FIRRTL:194685 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_179 = asSInt(_atomics_legal_T_178)
[703] FIRRTL:194686 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_180 = eq(_atomics_legal_T_179, asSInt(UInt<1>(0h0)))
[704] FIRRTL:194687 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_181 = xor(req.addr, UInt<28>(0h8000000))
[705] FIRRTL:194688 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_182 = cvt(_atomics_legal_T_181)
[706] FIRRTL:194689 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_183 = and(_atomics_legal_T_182, asSInt(UInt<33>(0h98000000)))
[707] FIRRTL:194690 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_184 = asSInt(_atomics_legal_T_183)
[708] FIRRTL:194691 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_185 = eq(_atomics_legal_T_184, asSInt(UInt<1>(0h0)))
[709] FIRRTL:194692 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_186 = xor(req.addr, UInt<28>(0h8000000))
[710] FIRRTL:194693 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_187 = cvt(_atomics_legal_T_186)
[711] FIRRTL:194694 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_188 = and(_atomics_legal_T_187, asSInt(UInt<33>(0h9a110000)))
[712] FIRRTL:194695 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_189 = asSInt(_atomics_legal_T_188)
[713] FIRRTL:194696 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_190 = eq(_atomics_legal_T_189, asSInt(UInt<1>(0h0)))
[714] FIRRTL:194697 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_191 = xor(req.addr, UInt<29>(0h10000000))
[715] FIRRTL:194698 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_192 = cvt(_atomics_legal_T_191)
[716] FIRRTL:194699 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_193 = and(_atomics_legal_T_192, asSInt(UInt<33>(0h9a111000)))
[717] FIRRTL:194700 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_194 = asSInt(_atomics_legal_T_193)
[718] FIRRTL:194701 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_195 = eq(_atomics_legal_T_194, asSInt(UInt<1>(0h0)))
[719] FIRRTL:194702 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_196 = xor(req.addr, UInt<32>(0h80000000))
[720] FIRRTL:194703 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_197 = cvt(_atomics_legal_T_196)
[721] FIRRTL:194704 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_198 = and(_atomics_legal_T_197, asSInt(UInt<33>(0h90000000)))
[722] FIRRTL:194705 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_199 = asSInt(_atomics_legal_T_198)
[723] FIRRTL:194706 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_200 = eq(_atomics_legal_T_199, asSInt(UInt<1>(0h0)))
[724] FIRRTL:194707 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_201 = or(_atomics_legal_T_170, _atomics_legal_T_175)
[725] FIRRTL:194708 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_202 = or(_atomics_legal_T_201, _atomics_legal_T_180)
[726] FIRRTL:194709 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_203 = or(_atomics_legal_T_202, _atomics_legal_T_185)
[727] FIRRTL:194710 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_204 = or(_atomics_legal_T_203, _atomics_legal_T_190)
[728] FIRRTL:194711 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_205 = or(_atomics_legal_T_204, _atomics_legal_T_195)
[729] FIRRTL:194712 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_206 = or(_atomics_legal_T_205, _atomics_legal_T_200)
[730] FIRRTL:194713 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_207 = and(_atomics_legal_T_165, _atomics_legal_T_206)
[731] FIRRTL:194714 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_208 = or(UInt<1>(0h0), UInt<1>(0h0))
[732] FIRRTL:194715 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_209 = xor(req.addr, UInt<17>(0h10000))
[733] FIRRTL:194716 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_210 = cvt(_atomics_legal_T_209)
[734] FIRRTL:194717 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_211 = and(_atomics_legal_T_210, asSInt(UInt<33>(0h9a110000)))
[735] FIRRTL:194718 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_212 = asSInt(_atomics_legal_T_211)
[736] FIRRTL:194719 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_213 = eq(_atomics_legal_T_212, asSInt(UInt<1>(0h0)))
[737] FIRRTL:194720 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_214 = and(_atomics_legal_T_208, _atomics_legal_T_213)
[738] FIRRTL:194721 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_215 = or(UInt<1>(0h0), _atomics_legal_T_207)
[739] FIRRTL:194722 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_3 = or(_atomics_legal_T_215, _atomics_legal_T_214)
[740] FIRRTL:194723 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:534:17 KIND:wire :: wire atomics_a_3 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[741] FIRRTL:194724 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:535:15 KIND:connect :: connect atomics_a_3.opcode, UInt<2>(0h3)
[742] FIRRTL:194725 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:536:15 KIND:connect :: connect atomics_a_3.param, UInt<3>(0h2)
[743] FIRRTL:194726 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:537:15 KIND:connect :: connect atomics_a_3.size, req.uop.mem_size
[744] FIRRTL:194727 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:538:15 KIND:connect :: connect atomics_a_3.source, UInt<2>(0h3)
[745] FIRRTL:194728 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:539:15 KIND:connect :: connect atomics_a_3.address, req.addr
[746] FIRRTL:194729 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_9 = or(req.uop.mem_size, UInt<3>(0h0))
[747] FIRRTL:194730 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_3 = bits(_atomics_a_mask_sizeOH_T_9, 1, 0)
[748] FIRRTL:194731 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_10 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_3)
[749] FIRRTL:194732 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_11 = bits(_atomics_a_mask_sizeOH_T_10, 2, 0)
[750] FIRRTL:194733 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_3 = or(_atomics_a_mask_sizeOH_T_11, UInt<1>(0h1))
[751] FIRRTL:194734 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_3 = geq(req.uop.mem_size, UInt<2>(0h3))
[752] FIRRTL:194735 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_3 = bits(atomics_a_mask_sizeOH_3, 2, 2)
[753] FIRRTL:194736 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_3 = bits(req.addr, 2, 2)
[754] FIRRTL:194737 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_3 = eq(atomics_a_mask_sub_sub_bit_3, UInt<1>(0h0))
[755] FIRRTL:194738 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_3 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_3)
[756] FIRRTL:194739 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_6 = and(atomics_a_mask_sub_sub_size_3, atomics_a_mask_sub_sub_0_2_3)
[757] FIRRTL:194740 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_3 = or(atomics_a_mask_sub_sub_sub_0_1_3, _atomics_a_mask_sub_sub_acc_T_6)
[758] FIRRTL:194741 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_3 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_3)
[759] FIRRTL:194742 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_7 = and(atomics_a_mask_sub_sub_size_3, atomics_a_mask_sub_sub_1_2_3)
[760] FIRRTL:194743 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_3 = or(atomics_a_mask_sub_sub_sub_0_1_3, _atomics_a_mask_sub_sub_acc_T_7)
[761] FIRRTL:194744 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_3 = bits(atomics_a_mask_sizeOH_3, 1, 1)
[762] FIRRTL:194745 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_3 = bits(req.addr, 1, 1)
[763] FIRRTL:194746 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_3 = eq(atomics_a_mask_sub_bit_3, UInt<1>(0h0))
[764] FIRRTL:194747 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_3 = and(atomics_a_mask_sub_sub_0_2_3, atomics_a_mask_sub_nbit_3)
[765] FIRRTL:194748 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_12 = and(atomics_a_mask_sub_size_3, atomics_a_mask_sub_0_2_3)
[766] FIRRTL:194749 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_3 = or(atomics_a_mask_sub_sub_0_1_3, _atomics_a_mask_sub_acc_T_12)
[767] FIRRTL:194750 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_3 = and(atomics_a_mask_sub_sub_0_2_3, atomics_a_mask_sub_bit_3)
[768] FIRRTL:194751 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_13 = and(atomics_a_mask_sub_size_3, atomics_a_mask_sub_1_2_3)
[769] FIRRTL:194752 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_3 = or(atomics_a_mask_sub_sub_0_1_3, _atomics_a_mask_sub_acc_T_13)
[770] FIRRTL:194753 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_3 = and(atomics_a_mask_sub_sub_1_2_3, atomics_a_mask_sub_nbit_3)
[771] FIRRTL:194754 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_14 = and(atomics_a_mask_sub_size_3, atomics_a_mask_sub_2_2_3)
[772] FIRRTL:194755 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_3 = or(atomics_a_mask_sub_sub_1_1_3, _atomics_a_mask_sub_acc_T_14)
[773] FIRRTL:194756 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_3 = and(atomics_a_mask_sub_sub_1_2_3, atomics_a_mask_sub_bit_3)
[774] FIRRTL:194757 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_15 = and(atomics_a_mask_sub_size_3, atomics_a_mask_sub_3_2_3)
[775] FIRRTL:194758 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_3 = or(atomics_a_mask_sub_sub_1_1_3, _atomics_a_mask_sub_acc_T_15)
[776] FIRRTL:194759 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_3 = bits(atomics_a_mask_sizeOH_3, 0, 0)
[777] FIRRTL:194760 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_3 = bits(req.addr, 0, 0)
[778] FIRRTL:194761 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_3 = eq(atomics_a_mask_bit_3, UInt<1>(0h0))
[779] FIRRTL:194762 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_24 = and(atomics_a_mask_sub_0_2_3, atomics_a_mask_nbit_3)
[780] FIRRTL:194763 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_24 = and(atomics_a_mask_size_3, atomics_a_mask_eq_24)
[781] FIRRTL:194764 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_24 = or(atomics_a_mask_sub_0_1_3, _atomics_a_mask_acc_T_24)
[782] FIRRTL:194765 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_25 = and(atomics_a_mask_sub_0_2_3, atomics_a_mask_bit_3)
[783] FIRRTL:194766 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_25 = and(atomics_a_mask_size_3, atomics_a_mask_eq_25)
[784] FIRRTL:194767 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_25 = or(atomics_a_mask_sub_0_1_3, _atomics_a_mask_acc_T_25)
[785] FIRRTL:194768 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_26 = and(atomics_a_mask_sub_1_2_3, atomics_a_mask_nbit_3)
[786] FIRRTL:194769 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_26 = and(atomics_a_mask_size_3, atomics_a_mask_eq_26)
[787] FIRRTL:194770 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_26 = or(atomics_a_mask_sub_1_1_3, _atomics_a_mask_acc_T_26)
[788] FIRRTL:194771 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_27 = and(atomics_a_mask_sub_1_2_3, atomics_a_mask_bit_3)
[789] FIRRTL:194772 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_27 = and(atomics_a_mask_size_3, atomics_a_mask_eq_27)
[790] FIRRTL:194773 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_27 = or(atomics_a_mask_sub_1_1_3, _atomics_a_mask_acc_T_27)
[791] FIRRTL:194774 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_28 = and(atomics_a_mask_sub_2_2_3, atomics_a_mask_nbit_3)
[792] FIRRTL:194775 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_28 = and(atomics_a_mask_size_3, atomics_a_mask_eq_28)
[793] FIRRTL:194776 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_28 = or(atomics_a_mask_sub_2_1_3, _atomics_a_mask_acc_T_28)
[794] FIRRTL:194777 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_29 = and(atomics_a_mask_sub_2_2_3, atomics_a_mask_bit_3)
[795] FIRRTL:194778 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_29 = and(atomics_a_mask_size_3, atomics_a_mask_eq_29)
[796] FIRRTL:194779 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_29 = or(atomics_a_mask_sub_2_1_3, _atomics_a_mask_acc_T_29)
[797] FIRRTL:194780 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_30 = and(atomics_a_mask_sub_3_2_3, atomics_a_mask_nbit_3)
[798] FIRRTL:194781 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_30 = and(atomics_a_mask_size_3, atomics_a_mask_eq_30)
[799] FIRRTL:194782 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_30 = or(atomics_a_mask_sub_3_1_3, _atomics_a_mask_acc_T_30)
[800] FIRRTL:194783 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_31 = and(atomics_a_mask_sub_3_2_3, atomics_a_mask_bit_3)
[801] FIRRTL:194784 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_31 = and(atomics_a_mask_size_3, atomics_a_mask_eq_31)
[802] FIRRTL:194785 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_31 = or(atomics_a_mask_sub_3_1_3, _atomics_a_mask_acc_T_31)
[803] FIRRTL:194786 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_3 = cat(atomics_a_mask_acc_25, atomics_a_mask_acc_24)
[804] FIRRTL:194787 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_3 = cat(atomics_a_mask_acc_27, atomics_a_mask_acc_26)
[805] FIRRTL:194788 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_3 = cat(atomics_a_mask_lo_hi_3, atomics_a_mask_lo_lo_3)
[806] FIRRTL:194789 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_3 = cat(atomics_a_mask_acc_29, atomics_a_mask_acc_28)
[807] FIRRTL:194790 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_3 = cat(atomics_a_mask_acc_31, atomics_a_mask_acc_30)
[808] FIRRTL:194791 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_3 = cat(atomics_a_mask_hi_hi_3, atomics_a_mask_hi_lo_3)
[809] FIRRTL:194792 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_3 = cat(atomics_a_mask_hi_3, atomics_a_mask_lo_3)
[810] FIRRTL:194793 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:542:15 KIND:connect :: connect atomics_a_3.mask, _atomics_a_mask_T_3
[811] FIRRTL:194794 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:543:15 KIND:connect :: connect atomics_a_3.data, req.data
[812] FIRRTL:194795 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:544:15 KIND:connect :: connect atomics_a_3.corrupt, UInt<1>(0h0)
[813] FIRRTL:194796 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_216 = leq(UInt<1>(0h0), req.uop.mem_size)
[814] FIRRTL:194797 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_217 = leq(req.uop.mem_size, UInt<2>(0h3))
[815] FIRRTL:194798 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_218 = and(_atomics_legal_T_216, _atomics_legal_T_217)
[816] FIRRTL:194799 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_219 = or(UInt<1>(0h0), _atomics_legal_T_218)
[817] FIRRTL:194800 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_220 = xor(req.addr, UInt<1>(0h0))
[818] FIRRTL:194801 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_221 = cvt(_atomics_legal_T_220)
[819] FIRRTL:194802 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_222 = and(_atomics_legal_T_221, asSInt(UInt<33>(0h98110000)))
[820] FIRRTL:194803 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_223 = asSInt(_atomics_legal_T_222)
[821] FIRRTL:194804 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_224 = eq(_atomics_legal_T_223, asSInt(UInt<1>(0h0)))
[822] FIRRTL:194805 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_225 = xor(req.addr, UInt<21>(0h100000))
[823] FIRRTL:194806 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_226 = cvt(_atomics_legal_T_225)
[824] FIRRTL:194807 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_227 = and(_atomics_legal_T_226, asSInt(UInt<33>(0h9a101000)))
[825] FIRRTL:194808 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_228 = asSInt(_atomics_legal_T_227)
[826] FIRRTL:194809 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_229 = eq(_atomics_legal_T_228, asSInt(UInt<1>(0h0)))
[827] FIRRTL:194810 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_230 = xor(req.addr, UInt<26>(0h2010000))
[828] FIRRTL:194811 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_231 = cvt(_atomics_legal_T_230)
[829] FIRRTL:194812 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_232 = and(_atomics_legal_T_231, asSInt(UInt<33>(0h9a111000)))
[830] FIRRTL:194813 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_233 = asSInt(_atomics_legal_T_232)
[831] FIRRTL:194814 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_234 = eq(_atomics_legal_T_233, asSInt(UInt<1>(0h0)))
[832] FIRRTL:194815 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_235 = xor(req.addr, UInt<28>(0h8000000))
[833] FIRRTL:194816 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_236 = cvt(_atomics_legal_T_235)
[834] FIRRTL:194817 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_237 = and(_atomics_legal_T_236, asSInt(UInt<33>(0h98000000)))
[835] FIRRTL:194818 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_238 = asSInt(_atomics_legal_T_237)
[836] FIRRTL:194819 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_239 = eq(_atomics_legal_T_238, asSInt(UInt<1>(0h0)))
[837] FIRRTL:194820 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_240 = xor(req.addr, UInt<28>(0h8000000))
[838] FIRRTL:194821 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_241 = cvt(_atomics_legal_T_240)
[839] FIRRTL:194822 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_242 = and(_atomics_legal_T_241, asSInt(UInt<33>(0h9a110000)))
[840] FIRRTL:194823 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_243 = asSInt(_atomics_legal_T_242)
[841] FIRRTL:194824 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_244 = eq(_atomics_legal_T_243, asSInt(UInt<1>(0h0)))
[842] FIRRTL:194825 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_245 = xor(req.addr, UInt<29>(0h10000000))
[843] FIRRTL:194826 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_246 = cvt(_atomics_legal_T_245)
[844] FIRRTL:194827 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_247 = and(_atomics_legal_T_246, asSInt(UInt<33>(0h9a111000)))
[845] FIRRTL:194828 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_248 = asSInt(_atomics_legal_T_247)
[846] FIRRTL:194829 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_249 = eq(_atomics_legal_T_248, asSInt(UInt<1>(0h0)))
[847] FIRRTL:194830 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_250 = xor(req.addr, UInt<32>(0h80000000))
[848] FIRRTL:194831 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_251 = cvt(_atomics_legal_T_250)
[849] FIRRTL:194832 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_252 = and(_atomics_legal_T_251, asSInt(UInt<33>(0h90000000)))
[850] FIRRTL:194833 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_253 = asSInt(_atomics_legal_T_252)
[851] FIRRTL:194834 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_254 = eq(_atomics_legal_T_253, asSInt(UInt<1>(0h0)))
[852] FIRRTL:194835 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_255 = or(_atomics_legal_T_224, _atomics_legal_T_229)
[853] FIRRTL:194836 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_256 = or(_atomics_legal_T_255, _atomics_legal_T_234)
[854] FIRRTL:194837 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_257 = or(_atomics_legal_T_256, _atomics_legal_T_239)
[855] FIRRTL:194838 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_258 = or(_atomics_legal_T_257, _atomics_legal_T_244)
[856] FIRRTL:194839 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_259 = or(_atomics_legal_T_258, _atomics_legal_T_249)
[857] FIRRTL:194840 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_260 = or(_atomics_legal_T_259, _atomics_legal_T_254)
[858] FIRRTL:194841 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_261 = and(_atomics_legal_T_219, _atomics_legal_T_260)
[859] FIRRTL:194842 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_262 = or(UInt<1>(0h0), UInt<1>(0h0))
[860] FIRRTL:194843 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_263 = xor(req.addr, UInt<17>(0h10000))
[861] FIRRTL:194844 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_264 = cvt(_atomics_legal_T_263)
[862] FIRRTL:194845 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_265 = and(_atomics_legal_T_264, asSInt(UInt<33>(0h9a110000)))
[863] FIRRTL:194846 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_266 = asSInt(_atomics_legal_T_265)
[864] FIRRTL:194847 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_267 = eq(_atomics_legal_T_266, asSInt(UInt<1>(0h0)))
[865] FIRRTL:194848 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_268 = and(_atomics_legal_T_262, _atomics_legal_T_267)
[866] FIRRTL:194849 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_269 = or(UInt<1>(0h0), _atomics_legal_T_261)
[867] FIRRTL:194850 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_4 = or(_atomics_legal_T_269, _atomics_legal_T_268)
[868] FIRRTL:194851 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:517:17 KIND:wire :: wire atomics_a_4 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[869] FIRRTL:194852 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:518:15 KIND:connect :: connect atomics_a_4.opcode, UInt<2>(0h2)
[870] FIRRTL:194853 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:519:15 KIND:connect :: connect atomics_a_4.param, UInt<3>(0h4)
[871] FIRRTL:194854 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:520:15 KIND:connect :: connect atomics_a_4.size, req.uop.mem_size
[872] FIRRTL:194855 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:521:15 KIND:connect :: connect atomics_a_4.source, UInt<2>(0h3)
[873] FIRRTL:194856 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:522:15 KIND:connect :: connect atomics_a_4.address, req.addr
[874] FIRRTL:194857 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_12 = or(req.uop.mem_size, UInt<3>(0h0))
[875] FIRRTL:194858 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_4 = bits(_atomics_a_mask_sizeOH_T_12, 1, 0)
[876] FIRRTL:194859 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_13 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_4)
[877] FIRRTL:194860 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_14 = bits(_atomics_a_mask_sizeOH_T_13, 2, 0)
[878] FIRRTL:194861 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_4 = or(_atomics_a_mask_sizeOH_T_14, UInt<1>(0h1))
[879] FIRRTL:194862 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_4 = geq(req.uop.mem_size, UInt<2>(0h3))
[880] FIRRTL:194863 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_4 = bits(atomics_a_mask_sizeOH_4, 2, 2)
[881] FIRRTL:194864 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_4 = bits(req.addr, 2, 2)
[882] FIRRTL:194865 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_4 = eq(atomics_a_mask_sub_sub_bit_4, UInt<1>(0h0))
[883] FIRRTL:194866 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_4 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_4)
[884] FIRRTL:194867 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_8 = and(atomics_a_mask_sub_sub_size_4, atomics_a_mask_sub_sub_0_2_4)
[885] FIRRTL:194868 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_4 = or(atomics_a_mask_sub_sub_sub_0_1_4, _atomics_a_mask_sub_sub_acc_T_8)
[886] FIRRTL:194869 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_4 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_4)
[887] FIRRTL:194870 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_9 = and(atomics_a_mask_sub_sub_size_4, atomics_a_mask_sub_sub_1_2_4)
[888] FIRRTL:194871 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_4 = or(atomics_a_mask_sub_sub_sub_0_1_4, _atomics_a_mask_sub_sub_acc_T_9)
[889] FIRRTL:194872 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_4 = bits(atomics_a_mask_sizeOH_4, 1, 1)
[890] FIRRTL:194873 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_4 = bits(req.addr, 1, 1)
[891] FIRRTL:194874 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_4 = eq(atomics_a_mask_sub_bit_4, UInt<1>(0h0))
[892] FIRRTL:194875 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_4 = and(atomics_a_mask_sub_sub_0_2_4, atomics_a_mask_sub_nbit_4)
[893] FIRRTL:194876 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_16 = and(atomics_a_mask_sub_size_4, atomics_a_mask_sub_0_2_4)
[894] FIRRTL:194877 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_4 = or(atomics_a_mask_sub_sub_0_1_4, _atomics_a_mask_sub_acc_T_16)
[895] FIRRTL:194878 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_4 = and(atomics_a_mask_sub_sub_0_2_4, atomics_a_mask_sub_bit_4)
[896] FIRRTL:194879 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_17 = and(atomics_a_mask_sub_size_4, atomics_a_mask_sub_1_2_4)
[897] FIRRTL:194880 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_4 = or(atomics_a_mask_sub_sub_0_1_4, _atomics_a_mask_sub_acc_T_17)
[898] FIRRTL:194881 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_4 = and(atomics_a_mask_sub_sub_1_2_4, atomics_a_mask_sub_nbit_4)
[899] FIRRTL:194882 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_18 = and(atomics_a_mask_sub_size_4, atomics_a_mask_sub_2_2_4)
[900] FIRRTL:194883 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_4 = or(atomics_a_mask_sub_sub_1_1_4, _atomics_a_mask_sub_acc_T_18)
[901] FIRRTL:194884 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_4 = and(atomics_a_mask_sub_sub_1_2_4, atomics_a_mask_sub_bit_4)
[902] FIRRTL:194885 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_19 = and(atomics_a_mask_sub_size_4, atomics_a_mask_sub_3_2_4)
[903] FIRRTL:194886 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_4 = or(atomics_a_mask_sub_sub_1_1_4, _atomics_a_mask_sub_acc_T_19)
[904] FIRRTL:194887 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_4 = bits(atomics_a_mask_sizeOH_4, 0, 0)
[905] FIRRTL:194888 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_4 = bits(req.addr, 0, 0)
[906] FIRRTL:194889 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_4 = eq(atomics_a_mask_bit_4, UInt<1>(0h0))
[907] FIRRTL:194890 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_32 = and(atomics_a_mask_sub_0_2_4, atomics_a_mask_nbit_4)
[908] FIRRTL:194891 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_32 = and(atomics_a_mask_size_4, atomics_a_mask_eq_32)
[909] FIRRTL:194892 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_32 = or(atomics_a_mask_sub_0_1_4, _atomics_a_mask_acc_T_32)
[910] FIRRTL:194893 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_33 = and(atomics_a_mask_sub_0_2_4, atomics_a_mask_bit_4)
[911] FIRRTL:194894 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_33 = and(atomics_a_mask_size_4, atomics_a_mask_eq_33)
[912] FIRRTL:194895 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_33 = or(atomics_a_mask_sub_0_1_4, _atomics_a_mask_acc_T_33)
[913] FIRRTL:194896 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_34 = and(atomics_a_mask_sub_1_2_4, atomics_a_mask_nbit_4)
[914] FIRRTL:194897 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_34 = and(atomics_a_mask_size_4, atomics_a_mask_eq_34)
[915] FIRRTL:194898 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_34 = or(atomics_a_mask_sub_1_1_4, _atomics_a_mask_acc_T_34)
[916] FIRRTL:194899 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_35 = and(atomics_a_mask_sub_1_2_4, atomics_a_mask_bit_4)
[917] FIRRTL:194900 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_35 = and(atomics_a_mask_size_4, atomics_a_mask_eq_35)
[918] FIRRTL:194901 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_35 = or(atomics_a_mask_sub_1_1_4, _atomics_a_mask_acc_T_35)
[919] FIRRTL:194902 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_36 = and(atomics_a_mask_sub_2_2_4, atomics_a_mask_nbit_4)
[920] FIRRTL:194903 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_36 = and(atomics_a_mask_size_4, atomics_a_mask_eq_36)
[921] FIRRTL:194904 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_36 = or(atomics_a_mask_sub_2_1_4, _atomics_a_mask_acc_T_36)
[922] FIRRTL:194905 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_37 = and(atomics_a_mask_sub_2_2_4, atomics_a_mask_bit_4)
[923] FIRRTL:194906 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_37 = and(atomics_a_mask_size_4, atomics_a_mask_eq_37)
[924] FIRRTL:194907 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_37 = or(atomics_a_mask_sub_2_1_4, _atomics_a_mask_acc_T_37)
[925] FIRRTL:194908 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_38 = and(atomics_a_mask_sub_3_2_4, atomics_a_mask_nbit_4)
[926] FIRRTL:194909 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_38 = and(atomics_a_mask_size_4, atomics_a_mask_eq_38)
[927] FIRRTL:194910 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_38 = or(atomics_a_mask_sub_3_1_4, _atomics_a_mask_acc_T_38)
[928] FIRRTL:194911 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_39 = and(atomics_a_mask_sub_3_2_4, atomics_a_mask_bit_4)
[929] FIRRTL:194912 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_39 = and(atomics_a_mask_size_4, atomics_a_mask_eq_39)
[930] FIRRTL:194913 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_39 = or(atomics_a_mask_sub_3_1_4, _atomics_a_mask_acc_T_39)
[931] FIRRTL:194914 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_4 = cat(atomics_a_mask_acc_33, atomics_a_mask_acc_32)
[932] FIRRTL:194915 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_4 = cat(atomics_a_mask_acc_35, atomics_a_mask_acc_34)
[933] FIRRTL:194916 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_4 = cat(atomics_a_mask_lo_hi_4, atomics_a_mask_lo_lo_4)
[934] FIRRTL:194917 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_4 = cat(atomics_a_mask_acc_37, atomics_a_mask_acc_36)
[935] FIRRTL:194918 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_4 = cat(atomics_a_mask_acc_39, atomics_a_mask_acc_38)
[936] FIRRTL:194919 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_4 = cat(atomics_a_mask_hi_hi_4, atomics_a_mask_hi_lo_4)
[937] FIRRTL:194920 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_4 = cat(atomics_a_mask_hi_4, atomics_a_mask_lo_4)
[938] FIRRTL:194921 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:525:15 KIND:connect :: connect atomics_a_4.mask, _atomics_a_mask_T_4
[939] FIRRTL:194922 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:526:15 KIND:connect :: connect atomics_a_4.data, req.data
[940] FIRRTL:194923 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:527:15 KIND:connect :: connect atomics_a_4.corrupt, UInt<1>(0h0)
[941] FIRRTL:194924 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_270 = leq(UInt<1>(0h0), req.uop.mem_size)
[942] FIRRTL:194925 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_271 = leq(req.uop.mem_size, UInt<2>(0h3))
[943] FIRRTL:194926 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_272 = and(_atomics_legal_T_270, _atomics_legal_T_271)
[944] FIRRTL:194927 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_273 = or(UInt<1>(0h0), _atomics_legal_T_272)
[945] FIRRTL:194928 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_274 = xor(req.addr, UInt<1>(0h0))
[946] FIRRTL:194929 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_275 = cvt(_atomics_legal_T_274)
[947] FIRRTL:194930 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_276 = and(_atomics_legal_T_275, asSInt(UInt<33>(0h98110000)))
[948] FIRRTL:194931 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_277 = asSInt(_atomics_legal_T_276)
[949] FIRRTL:194932 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_278 = eq(_atomics_legal_T_277, asSInt(UInt<1>(0h0)))
[950] FIRRTL:194933 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_279 = xor(req.addr, UInt<21>(0h100000))
[951] FIRRTL:194934 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_280 = cvt(_atomics_legal_T_279)
[952] FIRRTL:194935 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_281 = and(_atomics_legal_T_280, asSInt(UInt<33>(0h9a101000)))
[953] FIRRTL:194936 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_282 = asSInt(_atomics_legal_T_281)
[954] FIRRTL:194937 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_283 = eq(_atomics_legal_T_282, asSInt(UInt<1>(0h0)))
[955] FIRRTL:194938 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_284 = xor(req.addr, UInt<26>(0h2010000))
[956] FIRRTL:194939 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_285 = cvt(_atomics_legal_T_284)
[957] FIRRTL:194940 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_286 = and(_atomics_legal_T_285, asSInt(UInt<33>(0h9a111000)))
[958] FIRRTL:194941 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_287 = asSInt(_atomics_legal_T_286)
[959] FIRRTL:194942 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_288 = eq(_atomics_legal_T_287, asSInt(UInt<1>(0h0)))
[960] FIRRTL:194943 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_289 = xor(req.addr, UInt<28>(0h8000000))
[961] FIRRTL:194944 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_290 = cvt(_atomics_legal_T_289)
[962] FIRRTL:194945 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_291 = and(_atomics_legal_T_290, asSInt(UInt<33>(0h98000000)))
[963] FIRRTL:194946 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_292 = asSInt(_atomics_legal_T_291)
[964] FIRRTL:194947 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_293 = eq(_atomics_legal_T_292, asSInt(UInt<1>(0h0)))
[965] FIRRTL:194948 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_294 = xor(req.addr, UInt<28>(0h8000000))
[966] FIRRTL:194949 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_295 = cvt(_atomics_legal_T_294)
[967] FIRRTL:194950 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_296 = and(_atomics_legal_T_295, asSInt(UInt<33>(0h9a110000)))
[968] FIRRTL:194951 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_297 = asSInt(_atomics_legal_T_296)
[969] FIRRTL:194952 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_298 = eq(_atomics_legal_T_297, asSInt(UInt<1>(0h0)))
[970] FIRRTL:194953 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_299 = xor(req.addr, UInt<29>(0h10000000))
[971] FIRRTL:194954 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_300 = cvt(_atomics_legal_T_299)
[972] FIRRTL:194955 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_301 = and(_atomics_legal_T_300, asSInt(UInt<33>(0h9a111000)))
[973] FIRRTL:194956 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_302 = asSInt(_atomics_legal_T_301)
[974] FIRRTL:194957 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_303 = eq(_atomics_legal_T_302, asSInt(UInt<1>(0h0)))
[975] FIRRTL:194958 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_304 = xor(req.addr, UInt<32>(0h80000000))
[976] FIRRTL:194959 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_305 = cvt(_atomics_legal_T_304)
[977] FIRRTL:194960 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_306 = and(_atomics_legal_T_305, asSInt(UInt<33>(0h90000000)))
[978] FIRRTL:194961 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_307 = asSInt(_atomics_legal_T_306)
[979] FIRRTL:194962 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_308 = eq(_atomics_legal_T_307, asSInt(UInt<1>(0h0)))
[980] FIRRTL:194963 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_309 = or(_atomics_legal_T_278, _atomics_legal_T_283)
[981] FIRRTL:194964 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_310 = or(_atomics_legal_T_309, _atomics_legal_T_288)
[982] FIRRTL:194965 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_311 = or(_atomics_legal_T_310, _atomics_legal_T_293)
[983] FIRRTL:194966 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_312 = or(_atomics_legal_T_311, _atomics_legal_T_298)
[984] FIRRTL:194967 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_313 = or(_atomics_legal_T_312, _atomics_legal_T_303)
[985] FIRRTL:194968 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_314 = or(_atomics_legal_T_313, _atomics_legal_T_308)
[986] FIRRTL:194969 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_315 = and(_atomics_legal_T_273, _atomics_legal_T_314)
[987] FIRRTL:194970 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_316 = or(UInt<1>(0h0), UInt<1>(0h0))
[988] FIRRTL:194971 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_317 = xor(req.addr, UInt<17>(0h10000))
[989] FIRRTL:194972 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_318 = cvt(_atomics_legal_T_317)
[990] FIRRTL:194973 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_319 = and(_atomics_legal_T_318, asSInt(UInt<33>(0h9a110000)))
[991] FIRRTL:194974 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_320 = asSInt(_atomics_legal_T_319)
[992] FIRRTL:194975 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_321 = eq(_atomics_legal_T_320, asSInt(UInt<1>(0h0)))
[993] FIRRTL:194976 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_322 = and(_atomics_legal_T_316, _atomics_legal_T_321)
[994] FIRRTL:194977 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_323 = or(UInt<1>(0h0), _atomics_legal_T_315)
[995] FIRRTL:194978 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_5 = or(_atomics_legal_T_323, _atomics_legal_T_322)
[996] FIRRTL:194979 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:517:17 KIND:wire :: wire atomics_a_5 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[997] FIRRTL:194980 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:518:15 KIND:connect :: connect atomics_a_5.opcode, UInt<2>(0h2)
[998] FIRRTL:194981 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:519:15 KIND:connect :: connect atomics_a_5.param, UInt<3>(0h0)
[999] FIRRTL:194982 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:520:15 KIND:connect :: connect atomics_a_5.size, req.uop.mem_size
[1000] FIRRTL:194983 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:521:15 KIND:connect :: connect atomics_a_5.source, UInt<2>(0h3)
[1001] FIRRTL:194984 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:522:15 KIND:connect :: connect atomics_a_5.address, req.addr
[1002] FIRRTL:194985 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_15 = or(req.uop.mem_size, UInt<3>(0h0))
[1003] FIRRTL:194986 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_5 = bits(_atomics_a_mask_sizeOH_T_15, 1, 0)
[1004] FIRRTL:194987 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_16 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_5)
[1005] FIRRTL:194988 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_17 = bits(_atomics_a_mask_sizeOH_T_16, 2, 0)
[1006] FIRRTL:194989 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_5 = or(_atomics_a_mask_sizeOH_T_17, UInt<1>(0h1))
[1007] FIRRTL:194990 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_5 = geq(req.uop.mem_size, UInt<2>(0h3))
[1008] FIRRTL:194991 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_5 = bits(atomics_a_mask_sizeOH_5, 2, 2)
[1009] FIRRTL:194992 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_5 = bits(req.addr, 2, 2)
[1010] FIRRTL:194993 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_5 = eq(atomics_a_mask_sub_sub_bit_5, UInt<1>(0h0))
[1011] FIRRTL:194994 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_5 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_5)
[1012] FIRRTL:194995 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_10 = and(atomics_a_mask_sub_sub_size_5, atomics_a_mask_sub_sub_0_2_5)
[1013] FIRRTL:194996 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_5 = or(atomics_a_mask_sub_sub_sub_0_1_5, _atomics_a_mask_sub_sub_acc_T_10)
[1014] FIRRTL:194997 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_5 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_5)
[1015] FIRRTL:194998 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_11 = and(atomics_a_mask_sub_sub_size_5, atomics_a_mask_sub_sub_1_2_5)
[1016] FIRRTL:194999 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_5 = or(atomics_a_mask_sub_sub_sub_0_1_5, _atomics_a_mask_sub_sub_acc_T_11)
[1017] FIRRTL:195000 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_5 = bits(atomics_a_mask_sizeOH_5, 1, 1)
[1018] FIRRTL:195001 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_5 = bits(req.addr, 1, 1)
[1019] FIRRTL:195002 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_5 = eq(atomics_a_mask_sub_bit_5, UInt<1>(0h0))
[1020] FIRRTL:195003 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_5 = and(atomics_a_mask_sub_sub_0_2_5, atomics_a_mask_sub_nbit_5)
[1021] FIRRTL:195004 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_20 = and(atomics_a_mask_sub_size_5, atomics_a_mask_sub_0_2_5)
[1022] FIRRTL:195005 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_5 = or(atomics_a_mask_sub_sub_0_1_5, _atomics_a_mask_sub_acc_T_20)
[1023] FIRRTL:195006 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_5 = and(atomics_a_mask_sub_sub_0_2_5, atomics_a_mask_sub_bit_5)
[1024] FIRRTL:195007 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_21 = and(atomics_a_mask_sub_size_5, atomics_a_mask_sub_1_2_5)
[1025] FIRRTL:195008 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_5 = or(atomics_a_mask_sub_sub_0_1_5, _atomics_a_mask_sub_acc_T_21)
[1026] FIRRTL:195009 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_5 = and(atomics_a_mask_sub_sub_1_2_5, atomics_a_mask_sub_nbit_5)
[1027] FIRRTL:195010 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_22 = and(atomics_a_mask_sub_size_5, atomics_a_mask_sub_2_2_5)
[1028] FIRRTL:195011 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_5 = or(atomics_a_mask_sub_sub_1_1_5, _atomics_a_mask_sub_acc_T_22)
[1029] FIRRTL:195012 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_5 = and(atomics_a_mask_sub_sub_1_2_5, atomics_a_mask_sub_bit_5)
[1030] FIRRTL:195013 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_23 = and(atomics_a_mask_sub_size_5, atomics_a_mask_sub_3_2_5)
[1031] FIRRTL:195014 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_5 = or(atomics_a_mask_sub_sub_1_1_5, _atomics_a_mask_sub_acc_T_23)
[1032] FIRRTL:195015 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_5 = bits(atomics_a_mask_sizeOH_5, 0, 0)
[1033] FIRRTL:195016 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_5 = bits(req.addr, 0, 0)
[1034] FIRRTL:195017 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_5 = eq(atomics_a_mask_bit_5, UInt<1>(0h0))
[1035] FIRRTL:195018 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_40 = and(atomics_a_mask_sub_0_2_5, atomics_a_mask_nbit_5)
[1036] FIRRTL:195019 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_40 = and(atomics_a_mask_size_5, atomics_a_mask_eq_40)
[1037] FIRRTL:195020 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_40 = or(atomics_a_mask_sub_0_1_5, _atomics_a_mask_acc_T_40)
[1038] FIRRTL:195021 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_41 = and(atomics_a_mask_sub_0_2_5, atomics_a_mask_bit_5)
[1039] FIRRTL:195022 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_41 = and(atomics_a_mask_size_5, atomics_a_mask_eq_41)
[1040] FIRRTL:195023 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_41 = or(atomics_a_mask_sub_0_1_5, _atomics_a_mask_acc_T_41)
[1041] FIRRTL:195024 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_42 = and(atomics_a_mask_sub_1_2_5, atomics_a_mask_nbit_5)
[1042] FIRRTL:195025 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_42 = and(atomics_a_mask_size_5, atomics_a_mask_eq_42)
[1043] FIRRTL:195026 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_42 = or(atomics_a_mask_sub_1_1_5, _atomics_a_mask_acc_T_42)
[1044] FIRRTL:195027 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_43 = and(atomics_a_mask_sub_1_2_5, atomics_a_mask_bit_5)
[1045] FIRRTL:195028 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_43 = and(atomics_a_mask_size_5, atomics_a_mask_eq_43)
[1046] FIRRTL:195029 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_43 = or(atomics_a_mask_sub_1_1_5, _atomics_a_mask_acc_T_43)
[1047] FIRRTL:195030 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_44 = and(atomics_a_mask_sub_2_2_5, atomics_a_mask_nbit_5)
[1048] FIRRTL:195031 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_44 = and(atomics_a_mask_size_5, atomics_a_mask_eq_44)
[1049] FIRRTL:195032 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_44 = or(atomics_a_mask_sub_2_1_5, _atomics_a_mask_acc_T_44)
[1050] FIRRTL:195033 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_45 = and(atomics_a_mask_sub_2_2_5, atomics_a_mask_bit_5)
[1051] FIRRTL:195034 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_45 = and(atomics_a_mask_size_5, atomics_a_mask_eq_45)
[1052] FIRRTL:195035 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_45 = or(atomics_a_mask_sub_2_1_5, _atomics_a_mask_acc_T_45)
[1053] FIRRTL:195036 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_46 = and(atomics_a_mask_sub_3_2_5, atomics_a_mask_nbit_5)
[1054] FIRRTL:195037 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_46 = and(atomics_a_mask_size_5, atomics_a_mask_eq_46)
[1055] FIRRTL:195038 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_46 = or(atomics_a_mask_sub_3_1_5, _atomics_a_mask_acc_T_46)
[1056] FIRRTL:195039 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_47 = and(atomics_a_mask_sub_3_2_5, atomics_a_mask_bit_5)
[1057] FIRRTL:195040 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_47 = and(atomics_a_mask_size_5, atomics_a_mask_eq_47)
[1058] FIRRTL:195041 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_47 = or(atomics_a_mask_sub_3_1_5, _atomics_a_mask_acc_T_47)
[1059] FIRRTL:195042 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_5 = cat(atomics_a_mask_acc_41, atomics_a_mask_acc_40)
[1060] FIRRTL:195043 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_5 = cat(atomics_a_mask_acc_43, atomics_a_mask_acc_42)
[1061] FIRRTL:195044 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_5 = cat(atomics_a_mask_lo_hi_5, atomics_a_mask_lo_lo_5)
[1062] FIRRTL:195045 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_5 = cat(atomics_a_mask_acc_45, atomics_a_mask_acc_44)
[1063] FIRRTL:195046 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_5 = cat(atomics_a_mask_acc_47, atomics_a_mask_acc_46)
[1064] FIRRTL:195047 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_5 = cat(atomics_a_mask_hi_hi_5, atomics_a_mask_hi_lo_5)
[1065] FIRRTL:195048 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_5 = cat(atomics_a_mask_hi_5, atomics_a_mask_lo_5)
[1066] FIRRTL:195049 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:525:15 KIND:connect :: connect atomics_a_5.mask, _atomics_a_mask_T_5
[1067] FIRRTL:195050 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:526:15 KIND:connect :: connect atomics_a_5.data, req.data
[1068] FIRRTL:195051 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:527:15 KIND:connect :: connect atomics_a_5.corrupt, UInt<1>(0h0)
[1069] FIRRTL:195052 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_324 = leq(UInt<1>(0h0), req.uop.mem_size)
[1070] FIRRTL:195053 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_325 = leq(req.uop.mem_size, UInt<2>(0h3))
[1071] FIRRTL:195054 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_326 = and(_atomics_legal_T_324, _atomics_legal_T_325)
[1072] FIRRTL:195055 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_327 = or(UInt<1>(0h0), _atomics_legal_T_326)
[1073] FIRRTL:195056 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_328 = xor(req.addr, UInt<1>(0h0))
[1074] FIRRTL:195057 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_329 = cvt(_atomics_legal_T_328)
[1075] FIRRTL:195058 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_330 = and(_atomics_legal_T_329, asSInt(UInt<33>(0h98110000)))
[1076] FIRRTL:195059 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_331 = asSInt(_atomics_legal_T_330)
[1077] FIRRTL:195060 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_332 = eq(_atomics_legal_T_331, asSInt(UInt<1>(0h0)))
[1078] FIRRTL:195061 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_333 = xor(req.addr, UInt<21>(0h100000))
[1079] FIRRTL:195062 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_334 = cvt(_atomics_legal_T_333)
[1080] FIRRTL:195063 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_335 = and(_atomics_legal_T_334, asSInt(UInt<33>(0h9a101000)))
[1081] FIRRTL:195064 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_336 = asSInt(_atomics_legal_T_335)
[1082] FIRRTL:195065 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_337 = eq(_atomics_legal_T_336, asSInt(UInt<1>(0h0)))
[1083] FIRRTL:195066 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_338 = xor(req.addr, UInt<26>(0h2010000))
[1084] FIRRTL:195067 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_339 = cvt(_atomics_legal_T_338)
[1085] FIRRTL:195068 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_340 = and(_atomics_legal_T_339, asSInt(UInt<33>(0h9a111000)))
[1086] FIRRTL:195069 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_341 = asSInt(_atomics_legal_T_340)
[1087] FIRRTL:195070 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_342 = eq(_atomics_legal_T_341, asSInt(UInt<1>(0h0)))
[1088] FIRRTL:195071 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_343 = xor(req.addr, UInt<28>(0h8000000))
[1089] FIRRTL:195072 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_344 = cvt(_atomics_legal_T_343)
[1090] FIRRTL:195073 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_345 = and(_atomics_legal_T_344, asSInt(UInt<33>(0h98000000)))
[1091] FIRRTL:195074 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_346 = asSInt(_atomics_legal_T_345)
[1092] FIRRTL:195075 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_347 = eq(_atomics_legal_T_346, asSInt(UInt<1>(0h0)))
[1093] FIRRTL:195076 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_348 = xor(req.addr, UInt<28>(0h8000000))
[1094] FIRRTL:195077 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_349 = cvt(_atomics_legal_T_348)
[1095] FIRRTL:195078 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_350 = and(_atomics_legal_T_349, asSInt(UInt<33>(0h9a110000)))
[1096] FIRRTL:195079 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_351 = asSInt(_atomics_legal_T_350)
[1097] FIRRTL:195080 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_352 = eq(_atomics_legal_T_351, asSInt(UInt<1>(0h0)))
[1098] FIRRTL:195081 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_353 = xor(req.addr, UInt<29>(0h10000000))
[1099] FIRRTL:195082 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_354 = cvt(_atomics_legal_T_353)
[1100] FIRRTL:195083 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_355 = and(_atomics_legal_T_354, asSInt(UInt<33>(0h9a111000)))
[1101] FIRRTL:195084 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_356 = asSInt(_atomics_legal_T_355)
[1102] FIRRTL:195085 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_357 = eq(_atomics_legal_T_356, asSInt(UInt<1>(0h0)))
[1103] FIRRTL:195086 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_358 = xor(req.addr, UInt<32>(0h80000000))
[1104] FIRRTL:195087 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_359 = cvt(_atomics_legal_T_358)
[1105] FIRRTL:195088 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_360 = and(_atomics_legal_T_359, asSInt(UInt<33>(0h90000000)))
[1106] FIRRTL:195089 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_361 = asSInt(_atomics_legal_T_360)
[1107] FIRRTL:195090 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_362 = eq(_atomics_legal_T_361, asSInt(UInt<1>(0h0)))
[1108] FIRRTL:195091 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_363 = or(_atomics_legal_T_332, _atomics_legal_T_337)
[1109] FIRRTL:195092 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_364 = or(_atomics_legal_T_363, _atomics_legal_T_342)
[1110] FIRRTL:195093 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_365 = or(_atomics_legal_T_364, _atomics_legal_T_347)
[1111] FIRRTL:195094 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_366 = or(_atomics_legal_T_365, _atomics_legal_T_352)
[1112] FIRRTL:195095 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_367 = or(_atomics_legal_T_366, _atomics_legal_T_357)
[1113] FIRRTL:195096 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_368 = or(_atomics_legal_T_367, _atomics_legal_T_362)
[1114] FIRRTL:195097 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_369 = and(_atomics_legal_T_327, _atomics_legal_T_368)
[1115] FIRRTL:195098 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_370 = or(UInt<1>(0h0), UInt<1>(0h0))
[1116] FIRRTL:195099 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_371 = xor(req.addr, UInt<17>(0h10000))
[1117] FIRRTL:195100 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_372 = cvt(_atomics_legal_T_371)
[1118] FIRRTL:195101 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_373 = and(_atomics_legal_T_372, asSInt(UInt<33>(0h9a110000)))
[1119] FIRRTL:195102 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_374 = asSInt(_atomics_legal_T_373)
[1120] FIRRTL:195103 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_375 = eq(_atomics_legal_T_374, asSInt(UInt<1>(0h0)))
[1121] FIRRTL:195104 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_376 = and(_atomics_legal_T_370, _atomics_legal_T_375)
[1122] FIRRTL:195105 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_377 = or(UInt<1>(0h0), _atomics_legal_T_369)
[1123] FIRRTL:195106 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_6 = or(_atomics_legal_T_377, _atomics_legal_T_376)
[1124] FIRRTL:195107 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:517:17 KIND:wire :: wire atomics_a_6 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[1125] FIRRTL:195108 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:518:15 KIND:connect :: connect atomics_a_6.opcode, UInt<2>(0h2)
[1126] FIRRTL:195109 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:519:15 KIND:connect :: connect atomics_a_6.param, UInt<3>(0h1)
[1127] FIRRTL:195110 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:520:15 KIND:connect :: connect atomics_a_6.size, req.uop.mem_size
[1128] FIRRTL:195111 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:521:15 KIND:connect :: connect atomics_a_6.source, UInt<2>(0h3)
[1129] FIRRTL:195112 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:522:15 KIND:connect :: connect atomics_a_6.address, req.addr
[1130] FIRRTL:195113 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_18 = or(req.uop.mem_size, UInt<3>(0h0))
[1131] FIRRTL:195114 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_6 = bits(_atomics_a_mask_sizeOH_T_18, 1, 0)
[1132] FIRRTL:195115 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_19 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_6)
[1133] FIRRTL:195116 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_20 = bits(_atomics_a_mask_sizeOH_T_19, 2, 0)
[1134] FIRRTL:195117 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_6 = or(_atomics_a_mask_sizeOH_T_20, UInt<1>(0h1))
[1135] FIRRTL:195118 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_6 = geq(req.uop.mem_size, UInt<2>(0h3))
[1136] FIRRTL:195119 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_6 = bits(atomics_a_mask_sizeOH_6, 2, 2)
[1137] FIRRTL:195120 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_6 = bits(req.addr, 2, 2)
[1138] FIRRTL:195121 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_6 = eq(atomics_a_mask_sub_sub_bit_6, UInt<1>(0h0))
[1139] FIRRTL:195122 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_6 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_6)
[1140] FIRRTL:195123 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_12 = and(atomics_a_mask_sub_sub_size_6, atomics_a_mask_sub_sub_0_2_6)
[1141] FIRRTL:195124 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_6 = or(atomics_a_mask_sub_sub_sub_0_1_6, _atomics_a_mask_sub_sub_acc_T_12)
[1142] FIRRTL:195125 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_6 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_6)
[1143] FIRRTL:195126 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_13 = and(atomics_a_mask_sub_sub_size_6, atomics_a_mask_sub_sub_1_2_6)
[1144] FIRRTL:195127 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_6 = or(atomics_a_mask_sub_sub_sub_0_1_6, _atomics_a_mask_sub_sub_acc_T_13)
[1145] FIRRTL:195128 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_6 = bits(atomics_a_mask_sizeOH_6, 1, 1)
[1146] FIRRTL:195129 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_6 = bits(req.addr, 1, 1)
[1147] FIRRTL:195130 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_6 = eq(atomics_a_mask_sub_bit_6, UInt<1>(0h0))
[1148] FIRRTL:195131 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_6 = and(atomics_a_mask_sub_sub_0_2_6, atomics_a_mask_sub_nbit_6)
[1149] FIRRTL:195132 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_24 = and(atomics_a_mask_sub_size_6, atomics_a_mask_sub_0_2_6)
[1150] FIRRTL:195133 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_6 = or(atomics_a_mask_sub_sub_0_1_6, _atomics_a_mask_sub_acc_T_24)
[1151] FIRRTL:195134 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_6 = and(atomics_a_mask_sub_sub_0_2_6, atomics_a_mask_sub_bit_6)
[1152] FIRRTL:195135 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_25 = and(atomics_a_mask_sub_size_6, atomics_a_mask_sub_1_2_6)
[1153] FIRRTL:195136 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_6 = or(atomics_a_mask_sub_sub_0_1_6, _atomics_a_mask_sub_acc_T_25)
[1154] FIRRTL:195137 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_6 = and(atomics_a_mask_sub_sub_1_2_6, atomics_a_mask_sub_nbit_6)
[1155] FIRRTL:195138 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_26 = and(atomics_a_mask_sub_size_6, atomics_a_mask_sub_2_2_6)
[1156] FIRRTL:195139 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_6 = or(atomics_a_mask_sub_sub_1_1_6, _atomics_a_mask_sub_acc_T_26)
[1157] FIRRTL:195140 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_6 = and(atomics_a_mask_sub_sub_1_2_6, atomics_a_mask_sub_bit_6)
[1158] FIRRTL:195141 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_27 = and(atomics_a_mask_sub_size_6, atomics_a_mask_sub_3_2_6)
[1159] FIRRTL:195142 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_6 = or(atomics_a_mask_sub_sub_1_1_6, _atomics_a_mask_sub_acc_T_27)
[1160] FIRRTL:195143 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_6 = bits(atomics_a_mask_sizeOH_6, 0, 0)
[1161] FIRRTL:195144 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_6 = bits(req.addr, 0, 0)
[1162] FIRRTL:195145 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_6 = eq(atomics_a_mask_bit_6, UInt<1>(0h0))
[1163] FIRRTL:195146 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_48 = and(atomics_a_mask_sub_0_2_6, atomics_a_mask_nbit_6)
[1164] FIRRTL:195147 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_48 = and(atomics_a_mask_size_6, atomics_a_mask_eq_48)
[1165] FIRRTL:195148 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_48 = or(atomics_a_mask_sub_0_1_6, _atomics_a_mask_acc_T_48)
[1166] FIRRTL:195149 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_49 = and(atomics_a_mask_sub_0_2_6, atomics_a_mask_bit_6)
[1167] FIRRTL:195150 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_49 = and(atomics_a_mask_size_6, atomics_a_mask_eq_49)
[1168] FIRRTL:195151 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_49 = or(atomics_a_mask_sub_0_1_6, _atomics_a_mask_acc_T_49)
[1169] FIRRTL:195152 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_50 = and(atomics_a_mask_sub_1_2_6, atomics_a_mask_nbit_6)
[1170] FIRRTL:195153 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_50 = and(atomics_a_mask_size_6, atomics_a_mask_eq_50)
[1171] FIRRTL:195154 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_50 = or(atomics_a_mask_sub_1_1_6, _atomics_a_mask_acc_T_50)
[1172] FIRRTL:195155 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_51 = and(atomics_a_mask_sub_1_2_6, atomics_a_mask_bit_6)
[1173] FIRRTL:195156 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_51 = and(atomics_a_mask_size_6, atomics_a_mask_eq_51)
[1174] FIRRTL:195157 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_51 = or(atomics_a_mask_sub_1_1_6, _atomics_a_mask_acc_T_51)
[1175] FIRRTL:195158 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_52 = and(atomics_a_mask_sub_2_2_6, atomics_a_mask_nbit_6)
[1176] FIRRTL:195159 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_52 = and(atomics_a_mask_size_6, atomics_a_mask_eq_52)
[1177] FIRRTL:195160 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_52 = or(atomics_a_mask_sub_2_1_6, _atomics_a_mask_acc_T_52)
[1178] FIRRTL:195161 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_53 = and(atomics_a_mask_sub_2_2_6, atomics_a_mask_bit_6)
[1179] FIRRTL:195162 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_53 = and(atomics_a_mask_size_6, atomics_a_mask_eq_53)
[1180] FIRRTL:195163 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_53 = or(atomics_a_mask_sub_2_1_6, _atomics_a_mask_acc_T_53)
[1181] FIRRTL:195164 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_54 = and(atomics_a_mask_sub_3_2_6, atomics_a_mask_nbit_6)
[1182] FIRRTL:195165 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_54 = and(atomics_a_mask_size_6, atomics_a_mask_eq_54)
[1183] FIRRTL:195166 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_54 = or(atomics_a_mask_sub_3_1_6, _atomics_a_mask_acc_T_54)
[1184] FIRRTL:195167 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_55 = and(atomics_a_mask_sub_3_2_6, atomics_a_mask_bit_6)
[1185] FIRRTL:195168 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_55 = and(atomics_a_mask_size_6, atomics_a_mask_eq_55)
[1186] FIRRTL:195169 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_55 = or(atomics_a_mask_sub_3_1_6, _atomics_a_mask_acc_T_55)
[1187] FIRRTL:195170 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_6 = cat(atomics_a_mask_acc_49, atomics_a_mask_acc_48)
[1188] FIRRTL:195171 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_6 = cat(atomics_a_mask_acc_51, atomics_a_mask_acc_50)
[1189] FIRRTL:195172 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_6 = cat(atomics_a_mask_lo_hi_6, atomics_a_mask_lo_lo_6)
[1190] FIRRTL:195173 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_6 = cat(atomics_a_mask_acc_53, atomics_a_mask_acc_52)
[1191] FIRRTL:195174 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_6 = cat(atomics_a_mask_acc_55, atomics_a_mask_acc_54)
[1192] FIRRTL:195175 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_6 = cat(atomics_a_mask_hi_hi_6, atomics_a_mask_hi_lo_6)
[1193] FIRRTL:195176 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_6 = cat(atomics_a_mask_hi_6, atomics_a_mask_lo_6)
[1194] FIRRTL:195177 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:525:15 KIND:connect :: connect atomics_a_6.mask, _atomics_a_mask_T_6
[1195] FIRRTL:195178 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:526:15 KIND:connect :: connect atomics_a_6.data, req.data
[1196] FIRRTL:195179 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:527:15 KIND:connect :: connect atomics_a_6.corrupt, UInt<1>(0h0)
[1197] FIRRTL:195180 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_378 = leq(UInt<1>(0h0), req.uop.mem_size)
[1198] FIRRTL:195181 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_379 = leq(req.uop.mem_size, UInt<2>(0h3))
[1199] FIRRTL:195182 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_380 = and(_atomics_legal_T_378, _atomics_legal_T_379)
[1200] FIRRTL:195183 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_381 = or(UInt<1>(0h0), _atomics_legal_T_380)
[1201] FIRRTL:195184 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_382 = xor(req.addr, UInt<1>(0h0))
[1202] FIRRTL:195185 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_383 = cvt(_atomics_legal_T_382)
[1203] FIRRTL:195186 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_384 = and(_atomics_legal_T_383, asSInt(UInt<33>(0h98110000)))
[1204] FIRRTL:195187 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_385 = asSInt(_atomics_legal_T_384)
[1205] FIRRTL:195188 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_386 = eq(_atomics_legal_T_385, asSInt(UInt<1>(0h0)))
[1206] FIRRTL:195189 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_387 = xor(req.addr, UInt<21>(0h100000))
[1207] FIRRTL:195190 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_388 = cvt(_atomics_legal_T_387)
[1208] FIRRTL:195191 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_389 = and(_atomics_legal_T_388, asSInt(UInt<33>(0h9a101000)))
[1209] FIRRTL:195192 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_390 = asSInt(_atomics_legal_T_389)
[1210] FIRRTL:195193 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_391 = eq(_atomics_legal_T_390, asSInt(UInt<1>(0h0)))
[1211] FIRRTL:195194 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_392 = xor(req.addr, UInt<26>(0h2010000))
[1212] FIRRTL:195195 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_393 = cvt(_atomics_legal_T_392)
[1213] FIRRTL:195196 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_394 = and(_atomics_legal_T_393, asSInt(UInt<33>(0h9a111000)))
[1214] FIRRTL:195197 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_395 = asSInt(_atomics_legal_T_394)
[1215] FIRRTL:195198 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_396 = eq(_atomics_legal_T_395, asSInt(UInt<1>(0h0)))
[1216] FIRRTL:195199 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_397 = xor(req.addr, UInt<28>(0h8000000))
[1217] FIRRTL:195200 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_398 = cvt(_atomics_legal_T_397)
[1218] FIRRTL:195201 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_399 = and(_atomics_legal_T_398, asSInt(UInt<33>(0h98000000)))
[1219] FIRRTL:195202 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_400 = asSInt(_atomics_legal_T_399)
[1220] FIRRTL:195203 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_401 = eq(_atomics_legal_T_400, asSInt(UInt<1>(0h0)))
[1221] FIRRTL:195204 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_402 = xor(req.addr, UInt<28>(0h8000000))
[1222] FIRRTL:195205 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_403 = cvt(_atomics_legal_T_402)
[1223] FIRRTL:195206 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_404 = and(_atomics_legal_T_403, asSInt(UInt<33>(0h9a110000)))
[1224] FIRRTL:195207 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_405 = asSInt(_atomics_legal_T_404)
[1225] FIRRTL:195208 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_406 = eq(_atomics_legal_T_405, asSInt(UInt<1>(0h0)))
[1226] FIRRTL:195209 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_407 = xor(req.addr, UInt<29>(0h10000000))
[1227] FIRRTL:195210 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_408 = cvt(_atomics_legal_T_407)
[1228] FIRRTL:195211 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_409 = and(_atomics_legal_T_408, asSInt(UInt<33>(0h9a111000)))
[1229] FIRRTL:195212 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_410 = asSInt(_atomics_legal_T_409)
[1230] FIRRTL:195213 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_411 = eq(_atomics_legal_T_410, asSInt(UInt<1>(0h0)))
[1231] FIRRTL:195214 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_412 = xor(req.addr, UInt<32>(0h80000000))
[1232] FIRRTL:195215 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_413 = cvt(_atomics_legal_T_412)
[1233] FIRRTL:195216 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_414 = and(_atomics_legal_T_413, asSInt(UInt<33>(0h90000000)))
[1234] FIRRTL:195217 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_415 = asSInt(_atomics_legal_T_414)
[1235] FIRRTL:195218 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_416 = eq(_atomics_legal_T_415, asSInt(UInt<1>(0h0)))
[1236] FIRRTL:195219 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_417 = or(_atomics_legal_T_386, _atomics_legal_T_391)
[1237] FIRRTL:195220 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_418 = or(_atomics_legal_T_417, _atomics_legal_T_396)
[1238] FIRRTL:195221 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_419 = or(_atomics_legal_T_418, _atomics_legal_T_401)
[1239] FIRRTL:195222 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_420 = or(_atomics_legal_T_419, _atomics_legal_T_406)
[1240] FIRRTL:195223 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_421 = or(_atomics_legal_T_420, _atomics_legal_T_411)
[1241] FIRRTL:195224 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_422 = or(_atomics_legal_T_421, _atomics_legal_T_416)
[1242] FIRRTL:195225 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_423 = and(_atomics_legal_T_381, _atomics_legal_T_422)
[1243] FIRRTL:195226 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_424 = or(UInt<1>(0h0), UInt<1>(0h0))
[1244] FIRRTL:195227 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_425 = xor(req.addr, UInt<17>(0h10000))
[1245] FIRRTL:195228 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_426 = cvt(_atomics_legal_T_425)
[1246] FIRRTL:195229 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_427 = and(_atomics_legal_T_426, asSInt(UInt<33>(0h9a110000)))
[1247] FIRRTL:195230 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_428 = asSInt(_atomics_legal_T_427)
[1248] FIRRTL:195231 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_429 = eq(_atomics_legal_T_428, asSInt(UInt<1>(0h0)))
[1249] FIRRTL:195232 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_430 = and(_atomics_legal_T_424, _atomics_legal_T_429)
[1250] FIRRTL:195233 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_431 = or(UInt<1>(0h0), _atomics_legal_T_423)
[1251] FIRRTL:195234 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_7 = or(_atomics_legal_T_431, _atomics_legal_T_430)
[1252] FIRRTL:195235 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:517:17 KIND:wire :: wire atomics_a_7 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[1253] FIRRTL:195236 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:518:15 KIND:connect :: connect atomics_a_7.opcode, UInt<2>(0h2)
[1254] FIRRTL:195237 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:519:15 KIND:connect :: connect atomics_a_7.param, UInt<3>(0h2)
[1255] FIRRTL:195238 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:520:15 KIND:connect :: connect atomics_a_7.size, req.uop.mem_size
[1256] FIRRTL:195239 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:521:15 KIND:connect :: connect atomics_a_7.source, UInt<2>(0h3)
[1257] FIRRTL:195240 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:522:15 KIND:connect :: connect atomics_a_7.address, req.addr
[1258] FIRRTL:195241 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_21 = or(req.uop.mem_size, UInt<3>(0h0))
[1259] FIRRTL:195242 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_7 = bits(_atomics_a_mask_sizeOH_T_21, 1, 0)
[1260] FIRRTL:195243 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_22 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_7)
[1261] FIRRTL:195244 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_23 = bits(_atomics_a_mask_sizeOH_T_22, 2, 0)
[1262] FIRRTL:195245 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_7 = or(_atomics_a_mask_sizeOH_T_23, UInt<1>(0h1))
[1263] FIRRTL:195246 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_7 = geq(req.uop.mem_size, UInt<2>(0h3))
[1264] FIRRTL:195247 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_7 = bits(atomics_a_mask_sizeOH_7, 2, 2)
[1265] FIRRTL:195248 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_7 = bits(req.addr, 2, 2)
[1266] FIRRTL:195249 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_7 = eq(atomics_a_mask_sub_sub_bit_7, UInt<1>(0h0))
[1267] FIRRTL:195250 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_7 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_7)
[1268] FIRRTL:195251 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_14 = and(atomics_a_mask_sub_sub_size_7, atomics_a_mask_sub_sub_0_2_7)
[1269] FIRRTL:195252 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_7 = or(atomics_a_mask_sub_sub_sub_0_1_7, _atomics_a_mask_sub_sub_acc_T_14)
[1270] FIRRTL:195253 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_7 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_7)
[1271] FIRRTL:195254 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_15 = and(atomics_a_mask_sub_sub_size_7, atomics_a_mask_sub_sub_1_2_7)
[1272] FIRRTL:195255 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_7 = or(atomics_a_mask_sub_sub_sub_0_1_7, _atomics_a_mask_sub_sub_acc_T_15)
[1273] FIRRTL:195256 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_7 = bits(atomics_a_mask_sizeOH_7, 1, 1)
[1274] FIRRTL:195257 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_7 = bits(req.addr, 1, 1)
[1275] FIRRTL:195258 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_7 = eq(atomics_a_mask_sub_bit_7, UInt<1>(0h0))
[1276] FIRRTL:195259 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_7 = and(atomics_a_mask_sub_sub_0_2_7, atomics_a_mask_sub_nbit_7)
[1277] FIRRTL:195260 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_28 = and(atomics_a_mask_sub_size_7, atomics_a_mask_sub_0_2_7)
[1278] FIRRTL:195261 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_7 = or(atomics_a_mask_sub_sub_0_1_7, _atomics_a_mask_sub_acc_T_28)
[1279] FIRRTL:195262 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_7 = and(atomics_a_mask_sub_sub_0_2_7, atomics_a_mask_sub_bit_7)
[1280] FIRRTL:195263 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_29 = and(atomics_a_mask_sub_size_7, atomics_a_mask_sub_1_2_7)
[1281] FIRRTL:195264 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_7 = or(atomics_a_mask_sub_sub_0_1_7, _atomics_a_mask_sub_acc_T_29)
[1282] FIRRTL:195265 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_7 = and(atomics_a_mask_sub_sub_1_2_7, atomics_a_mask_sub_nbit_7)
[1283] FIRRTL:195266 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_30 = and(atomics_a_mask_sub_size_7, atomics_a_mask_sub_2_2_7)
[1284] FIRRTL:195267 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_7 = or(atomics_a_mask_sub_sub_1_1_7, _atomics_a_mask_sub_acc_T_30)
[1285] FIRRTL:195268 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_7 = and(atomics_a_mask_sub_sub_1_2_7, atomics_a_mask_sub_bit_7)
[1286] FIRRTL:195269 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_31 = and(atomics_a_mask_sub_size_7, atomics_a_mask_sub_3_2_7)
[1287] FIRRTL:195270 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_7 = or(atomics_a_mask_sub_sub_1_1_7, _atomics_a_mask_sub_acc_T_31)
[1288] FIRRTL:195271 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_7 = bits(atomics_a_mask_sizeOH_7, 0, 0)
[1289] FIRRTL:195272 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_7 = bits(req.addr, 0, 0)
[1290] FIRRTL:195273 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_7 = eq(atomics_a_mask_bit_7, UInt<1>(0h0))
[1291] FIRRTL:195274 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_56 = and(atomics_a_mask_sub_0_2_7, atomics_a_mask_nbit_7)
[1292] FIRRTL:195275 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_56 = and(atomics_a_mask_size_7, atomics_a_mask_eq_56)
[1293] FIRRTL:195276 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_56 = or(atomics_a_mask_sub_0_1_7, _atomics_a_mask_acc_T_56)
[1294] FIRRTL:195277 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_57 = and(atomics_a_mask_sub_0_2_7, atomics_a_mask_bit_7)
[1295] FIRRTL:195278 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_57 = and(atomics_a_mask_size_7, atomics_a_mask_eq_57)
[1296] FIRRTL:195279 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_57 = or(atomics_a_mask_sub_0_1_7, _atomics_a_mask_acc_T_57)
[1297] FIRRTL:195280 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_58 = and(atomics_a_mask_sub_1_2_7, atomics_a_mask_nbit_7)
[1298] FIRRTL:195281 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_58 = and(atomics_a_mask_size_7, atomics_a_mask_eq_58)
[1299] FIRRTL:195282 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_58 = or(atomics_a_mask_sub_1_1_7, _atomics_a_mask_acc_T_58)
[1300] FIRRTL:195283 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_59 = and(atomics_a_mask_sub_1_2_7, atomics_a_mask_bit_7)
[1301] FIRRTL:195284 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_59 = and(atomics_a_mask_size_7, atomics_a_mask_eq_59)
[1302] FIRRTL:195285 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_59 = or(atomics_a_mask_sub_1_1_7, _atomics_a_mask_acc_T_59)
[1303] FIRRTL:195286 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_60 = and(atomics_a_mask_sub_2_2_7, atomics_a_mask_nbit_7)
[1304] FIRRTL:195287 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_60 = and(atomics_a_mask_size_7, atomics_a_mask_eq_60)
[1305] FIRRTL:195288 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_60 = or(atomics_a_mask_sub_2_1_7, _atomics_a_mask_acc_T_60)
[1306] FIRRTL:195289 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_61 = and(atomics_a_mask_sub_2_2_7, atomics_a_mask_bit_7)
[1307] FIRRTL:195290 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_61 = and(atomics_a_mask_size_7, atomics_a_mask_eq_61)
[1308] FIRRTL:195291 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_61 = or(atomics_a_mask_sub_2_1_7, _atomics_a_mask_acc_T_61)
[1309] FIRRTL:195292 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_62 = and(atomics_a_mask_sub_3_2_7, atomics_a_mask_nbit_7)
[1310] FIRRTL:195293 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_62 = and(atomics_a_mask_size_7, atomics_a_mask_eq_62)
[1311] FIRRTL:195294 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_62 = or(atomics_a_mask_sub_3_1_7, _atomics_a_mask_acc_T_62)
[1312] FIRRTL:195295 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_63 = and(atomics_a_mask_sub_3_2_7, atomics_a_mask_bit_7)
[1313] FIRRTL:195296 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_63 = and(atomics_a_mask_size_7, atomics_a_mask_eq_63)
[1314] FIRRTL:195297 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_63 = or(atomics_a_mask_sub_3_1_7, _atomics_a_mask_acc_T_63)
[1315] FIRRTL:195298 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_7 = cat(atomics_a_mask_acc_57, atomics_a_mask_acc_56)
[1316] FIRRTL:195299 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_7 = cat(atomics_a_mask_acc_59, atomics_a_mask_acc_58)
[1317] FIRRTL:195300 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_7 = cat(atomics_a_mask_lo_hi_7, atomics_a_mask_lo_lo_7)
[1318] FIRRTL:195301 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_7 = cat(atomics_a_mask_acc_61, atomics_a_mask_acc_60)
[1319] FIRRTL:195302 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_7 = cat(atomics_a_mask_acc_63, atomics_a_mask_acc_62)
[1320] FIRRTL:195303 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_7 = cat(atomics_a_mask_hi_hi_7, atomics_a_mask_hi_lo_7)
[1321] FIRRTL:195304 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_7 = cat(atomics_a_mask_hi_7, atomics_a_mask_lo_7)
[1322] FIRRTL:195305 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:525:15 KIND:connect :: connect atomics_a_7.mask, _atomics_a_mask_T_7
[1323] FIRRTL:195306 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:526:15 KIND:connect :: connect atomics_a_7.data, req.data
[1324] FIRRTL:195307 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:527:15 KIND:connect :: connect atomics_a_7.corrupt, UInt<1>(0h0)
[1325] FIRRTL:195308 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:28 KIND:node :: node _atomics_legal_T_432 = leq(UInt<1>(0h0), req.uop.mem_size)
[1326] FIRRTL:195309 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:38 KIND:node :: node _atomics_legal_T_433 = leq(req.uop.mem_size, UInt<2>(0h3))
[1327] FIRRTL:195310 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:94:33 KIND:node :: node _atomics_legal_T_434 = and(_atomics_legal_T_432, _atomics_legal_T_433)
[1328] FIRRTL:195311 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_435 = or(UInt<1>(0h0), _atomics_legal_T_434)
[1329] FIRRTL:195312 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_436 = xor(req.addr, UInt<1>(0h0))
[1330] FIRRTL:195313 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_437 = cvt(_atomics_legal_T_436)
[1331] FIRRTL:195314 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_438 = and(_atomics_legal_T_437, asSInt(UInt<33>(0h98110000)))
[1332] FIRRTL:195315 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_439 = asSInt(_atomics_legal_T_438)
[1333] FIRRTL:195316 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_440 = eq(_atomics_legal_T_439, asSInt(UInt<1>(0h0)))
[1334] FIRRTL:195317 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_441 = xor(req.addr, UInt<21>(0h100000))
[1335] FIRRTL:195318 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_442 = cvt(_atomics_legal_T_441)
[1336] FIRRTL:195319 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_443 = and(_atomics_legal_T_442, asSInt(UInt<33>(0h9a101000)))
[1337] FIRRTL:195320 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_444 = asSInt(_atomics_legal_T_443)
[1338] FIRRTL:195321 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_445 = eq(_atomics_legal_T_444, asSInt(UInt<1>(0h0)))
[1339] FIRRTL:195322 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_446 = xor(req.addr, UInt<26>(0h2010000))
[1340] FIRRTL:195323 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_447 = cvt(_atomics_legal_T_446)
[1341] FIRRTL:195324 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_448 = and(_atomics_legal_T_447, asSInt(UInt<33>(0h9a111000)))
[1342] FIRRTL:195325 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_449 = asSInt(_atomics_legal_T_448)
[1343] FIRRTL:195326 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_450 = eq(_atomics_legal_T_449, asSInt(UInt<1>(0h0)))
[1344] FIRRTL:195327 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_451 = xor(req.addr, UInt<28>(0h8000000))
[1345] FIRRTL:195328 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_452 = cvt(_atomics_legal_T_451)
[1346] FIRRTL:195329 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_453 = and(_atomics_legal_T_452, asSInt(UInt<33>(0h98000000)))
[1347] FIRRTL:195330 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_454 = asSInt(_atomics_legal_T_453)
[1348] FIRRTL:195331 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_455 = eq(_atomics_legal_T_454, asSInt(UInt<1>(0h0)))
[1349] FIRRTL:195332 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_456 = xor(req.addr, UInt<28>(0h8000000))
[1350] FIRRTL:195333 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_457 = cvt(_atomics_legal_T_456)
[1351] FIRRTL:195334 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_458 = and(_atomics_legal_T_457, asSInt(UInt<33>(0h9a110000)))
[1352] FIRRTL:195335 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_459 = asSInt(_atomics_legal_T_458)
[1353] FIRRTL:195336 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_460 = eq(_atomics_legal_T_459, asSInt(UInt<1>(0h0)))
[1354] FIRRTL:195337 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_461 = xor(req.addr, UInt<29>(0h10000000))
[1355] FIRRTL:195338 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_462 = cvt(_atomics_legal_T_461)
[1356] FIRRTL:195339 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_463 = and(_atomics_legal_T_462, asSInt(UInt<33>(0h9a111000)))
[1357] FIRRTL:195340 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_464 = asSInt(_atomics_legal_T_463)
[1358] FIRRTL:195341 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_465 = eq(_atomics_legal_T_464, asSInt(UInt<1>(0h0)))
[1359] FIRRTL:195342 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_466 = xor(req.addr, UInt<32>(0h80000000))
[1360] FIRRTL:195343 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_467 = cvt(_atomics_legal_T_466)
[1361] FIRRTL:195344 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_468 = and(_atomics_legal_T_467, asSInt(UInt<33>(0h90000000)))
[1362] FIRRTL:195345 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_469 = asSInt(_atomics_legal_T_468)
[1363] FIRRTL:195346 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_470 = eq(_atomics_legal_T_469, asSInt(UInt<1>(0h0)))
[1364] FIRRTL:195347 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_471 = or(_atomics_legal_T_440, _atomics_legal_T_445)
[1365] FIRRTL:195348 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_472 = or(_atomics_legal_T_471, _atomics_legal_T_450)
[1366] FIRRTL:195349 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_473 = or(_atomics_legal_T_472, _atomics_legal_T_455)
[1367] FIRRTL:195350 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_474 = or(_atomics_legal_T_473, _atomics_legal_T_460)
[1368] FIRRTL:195351 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_475 = or(_atomics_legal_T_474, _atomics_legal_T_465)
[1369] FIRRTL:195352 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _atomics_legal_T_476 = or(_atomics_legal_T_475, _atomics_legal_T_470)
[1370] FIRRTL:195353 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_477 = and(_atomics_legal_T_435, _atomics_legal_T_476)
[1371] FIRRTL:195354 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _atomics_legal_T_478 = or(UInt<1>(0h0), UInt<1>(0h0))
[1372] FIRRTL:195355 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _atomics_legal_T_479 = xor(req.addr, UInt<17>(0h10000))
[1373] FIRRTL:195356 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _atomics_legal_T_480 = cvt(_atomics_legal_T_479)
[1374] FIRRTL:195357 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_481 = and(_atomics_legal_T_480, asSInt(UInt<33>(0h9a110000)))
[1375] FIRRTL:195358 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _atomics_legal_T_482 = asSInt(_atomics_legal_T_481)
[1376] FIRRTL:195359 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _atomics_legal_T_483 = eq(_atomics_legal_T_482, asSInt(UInt<1>(0h0)))
[1377] FIRRTL:195360 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _atomics_legal_T_484 = and(_atomics_legal_T_478, _atomics_legal_T_483)
[1378] FIRRTL:195361 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _atomics_legal_T_485 = or(UInt<1>(0h0), _atomics_legal_T_477)
[1379] FIRRTL:195362 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node atomics_legal_8 = or(_atomics_legal_T_485, _atomics_legal_T_484)
[1380] FIRRTL:195363 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:517:17 KIND:wire :: wire atomics_a_8 : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}
[1381] FIRRTL:195364 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:518:15 KIND:connect :: connect atomics_a_8.opcode, UInt<2>(0h2)
[1382] FIRRTL:195365 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:519:15 KIND:connect :: connect atomics_a_8.param, UInt<3>(0h3)
[1383] FIRRTL:195366 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:520:15 KIND:connect :: connect atomics_a_8.size, req.uop.mem_size
[1384] FIRRTL:195367 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:521:15 KIND:connect :: connect atomics_a_8.source, UInt<2>(0h3)
[1385] FIRRTL:195368 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:522:15 KIND:connect :: connect atomics_a_8.address, req.addr
[1386] FIRRTL:195369 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:34 KIND:node :: node _atomics_a_mask_sizeOH_T_24 = or(req.uop.mem_size, UInt<3>(0h0))
[1387] FIRRTL:195370 SRC:src/main/scala/chisel3/util/OneHot.scala:64:49 KIND:node :: node atomics_a_mask_sizeOH_shiftAmount_8 = bits(_atomics_a_mask_sizeOH_T_24, 1, 0)
[1388] FIRRTL:195371 SRC:src/main/scala/chisel3/util/OneHot.scala:65:12 KIND:node :: node _atomics_a_mask_sizeOH_T_25 = dshl(UInt<1>(0h1), atomics_a_mask_sizeOH_shiftAmount_8)
[1389] FIRRTL:195372 SRC:src/main/scala/chisel3/util/OneHot.scala:65:27 KIND:node :: node _atomics_a_mask_sizeOH_T_26 = bits(_atomics_a_mask_sizeOH_T_25, 2, 0)
[1390] FIRRTL:195373 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:202:81 KIND:node :: node atomics_a_mask_sizeOH_8 = or(_atomics_a_mask_sizeOH_T_26, UInt<1>(0h1))
[1391] FIRRTL:195374 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:206:21 KIND:node :: node atomics_a_mask_sub_sub_sub_0_1_8 = geq(req.uop.mem_size, UInt<2>(0h3))
[1392] FIRRTL:195375 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_sub_size_8 = bits(atomics_a_mask_sizeOH_8, 2, 2)
[1393] FIRRTL:195376 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_sub_bit_8 = bits(req.addr, 2, 2)
[1394] FIRRTL:195377 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_sub_nbit_8 = eq(atomics_a_mask_sub_sub_bit_8, UInt<1>(0h0))
[1395] FIRRTL:195378 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_0_2_8 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_nbit_8)
[1396] FIRRTL:195379 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_16 = and(atomics_a_mask_sub_sub_size_8, atomics_a_mask_sub_sub_0_2_8)
[1397] FIRRTL:195380 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_0_1_8 = or(atomics_a_mask_sub_sub_sub_0_1_8, _atomics_a_mask_sub_sub_acc_T_16)
[1398] FIRRTL:195381 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_sub_1_2_8 = and(UInt<1>(0h1), atomics_a_mask_sub_sub_bit_8)
[1399] FIRRTL:195382 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_sub_acc_T_17 = and(atomics_a_mask_sub_sub_size_8, atomics_a_mask_sub_sub_1_2_8)
[1400] FIRRTL:195383 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_sub_1_1_8 = or(atomics_a_mask_sub_sub_sub_0_1_8, _atomics_a_mask_sub_sub_acc_T_17)
[1401] FIRRTL:195384 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_sub_size_8 = bits(atomics_a_mask_sizeOH_8, 1, 1)
[1402] FIRRTL:195385 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_sub_bit_8 = bits(req.addr, 1, 1)
[1403] FIRRTL:195386 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_sub_nbit_8 = eq(atomics_a_mask_sub_bit_8, UInt<1>(0h0))
[1404] FIRRTL:195387 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_0_2_8 = and(atomics_a_mask_sub_sub_0_2_8, atomics_a_mask_sub_nbit_8)
[1405] FIRRTL:195388 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_32 = and(atomics_a_mask_sub_size_8, atomics_a_mask_sub_0_2_8)
[1406] FIRRTL:195389 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_0_1_8 = or(atomics_a_mask_sub_sub_0_1_8, _atomics_a_mask_sub_acc_T_32)
[1407] FIRRTL:195390 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_1_2_8 = and(atomics_a_mask_sub_sub_0_2_8, atomics_a_mask_sub_bit_8)
[1408] FIRRTL:195391 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_33 = and(atomics_a_mask_sub_size_8, atomics_a_mask_sub_1_2_8)
[1409] FIRRTL:195392 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_1_1_8 = or(atomics_a_mask_sub_sub_0_1_8, _atomics_a_mask_sub_acc_T_33)
[1410] FIRRTL:195393 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_2_2_8 = and(atomics_a_mask_sub_sub_1_2_8, atomics_a_mask_sub_nbit_8)
[1411] FIRRTL:195394 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_34 = and(atomics_a_mask_sub_size_8, atomics_a_mask_sub_2_2_8)
[1412] FIRRTL:195395 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_2_1_8 = or(atomics_a_mask_sub_sub_1_1_8, _atomics_a_mask_sub_acc_T_34)
[1413] FIRRTL:195396 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_sub_3_2_8 = and(atomics_a_mask_sub_sub_1_2_8, atomics_a_mask_sub_bit_8)
[1414] FIRRTL:195397 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_sub_acc_T_35 = and(atomics_a_mask_sub_size_8, atomics_a_mask_sub_3_2_8)
[1415] FIRRTL:195398 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_sub_3_1_8 = or(atomics_a_mask_sub_sub_1_1_8, _atomics_a_mask_sub_acc_T_35)
[1416] FIRRTL:195399 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:209:26 KIND:node :: node atomics_a_mask_size_8 = bits(atomics_a_mask_sizeOH_8, 0, 0)
[1417] FIRRTL:195400 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:210:26 KIND:node :: node atomics_a_mask_bit_8 = bits(req.addr, 0, 0)
[1418] FIRRTL:195401 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:211:20 KIND:node :: node atomics_a_mask_nbit_8 = eq(atomics_a_mask_bit_8, UInt<1>(0h0))
[1419] FIRRTL:195402 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_64 = and(atomics_a_mask_sub_0_2_8, atomics_a_mask_nbit_8)
[1420] FIRRTL:195403 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_64 = and(atomics_a_mask_size_8, atomics_a_mask_eq_64)
[1421] FIRRTL:195404 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_64 = or(atomics_a_mask_sub_0_1_8, _atomics_a_mask_acc_T_64)
[1422] FIRRTL:195405 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_65 = and(atomics_a_mask_sub_0_2_8, atomics_a_mask_bit_8)
[1423] FIRRTL:195406 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_65 = and(atomics_a_mask_size_8, atomics_a_mask_eq_65)
[1424] FIRRTL:195407 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_65 = or(atomics_a_mask_sub_0_1_8, _atomics_a_mask_acc_T_65)
[1425] FIRRTL:195408 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_66 = and(atomics_a_mask_sub_1_2_8, atomics_a_mask_nbit_8)
[1426] FIRRTL:195409 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_66 = and(atomics_a_mask_size_8, atomics_a_mask_eq_66)
[1427] FIRRTL:195410 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_66 = or(atomics_a_mask_sub_1_1_8, _atomics_a_mask_acc_T_66)
[1428] FIRRTL:195411 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_67 = and(atomics_a_mask_sub_1_2_8, atomics_a_mask_bit_8)
[1429] FIRRTL:195412 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_67 = and(atomics_a_mask_size_8, atomics_a_mask_eq_67)
[1430] FIRRTL:195413 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_67 = or(atomics_a_mask_sub_1_1_8, _atomics_a_mask_acc_T_67)
[1431] FIRRTL:195414 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_68 = and(atomics_a_mask_sub_2_2_8, atomics_a_mask_nbit_8)
[1432] FIRRTL:195415 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_68 = and(atomics_a_mask_size_8, atomics_a_mask_eq_68)
[1433] FIRRTL:195416 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_68 = or(atomics_a_mask_sub_2_1_8, _atomics_a_mask_acc_T_68)
[1434] FIRRTL:195417 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_69 = and(atomics_a_mask_sub_2_2_8, atomics_a_mask_bit_8)
[1435] FIRRTL:195418 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_69 = and(atomics_a_mask_size_8, atomics_a_mask_eq_69)
[1436] FIRRTL:195419 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_69 = or(atomics_a_mask_sub_2_1_8, _atomics_a_mask_acc_T_69)
[1437] FIRRTL:195420 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_70 = and(atomics_a_mask_sub_3_2_8, atomics_a_mask_nbit_8)
[1438] FIRRTL:195421 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_70 = and(atomics_a_mask_size_8, atomics_a_mask_eq_70)
[1439] FIRRTL:195422 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_70 = or(atomics_a_mask_sub_3_1_8, _atomics_a_mask_acc_T_70)
[1440] FIRRTL:195423 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:214:27 KIND:node :: node atomics_a_mask_eq_71 = and(atomics_a_mask_sub_3_2_8, atomics_a_mask_bit_8)
[1441] FIRRTL:195424 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:38 KIND:node :: node _atomics_a_mask_acc_T_71 = and(atomics_a_mask_size_8, atomics_a_mask_eq_71)
[1442] FIRRTL:195425 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:215:29 KIND:node :: node atomics_a_mask_acc_71 = or(atomics_a_mask_sub_3_1_8, _atomics_a_mask_acc_T_71)
[1443] FIRRTL:195426 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_lo_8 = cat(atomics_a_mask_acc_65, atomics_a_mask_acc_64)
[1444] FIRRTL:195427 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_hi_8 = cat(atomics_a_mask_acc_67, atomics_a_mask_acc_66)
[1445] FIRRTL:195428 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_lo_8 = cat(atomics_a_mask_lo_hi_8, atomics_a_mask_lo_lo_8)
[1446] FIRRTL:195429 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_lo_8 = cat(atomics_a_mask_acc_69, atomics_a_mask_acc_68)
[1447] FIRRTL:195430 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_hi_8 = cat(atomics_a_mask_acc_71, atomics_a_mask_acc_70)
[1448] FIRRTL:195431 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node atomics_a_mask_hi_8 = cat(atomics_a_mask_hi_hi_8, atomics_a_mask_hi_lo_8)
[1449] FIRRTL:195432 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:222:10 KIND:node :: node _atomics_a_mask_T_8 = cat(atomics_a_mask_hi_8, atomics_a_mask_lo_8)
[1450] FIRRTL:195433 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:525:15 KIND:connect :: connect atomics_a_8.mask, _atomics_a_mask_T_8
[1451] FIRRTL:195434 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:526:15 KIND:connect :: connect atomics_a_8.data, req.data
[1452] FIRRTL:195435 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:527:15 KIND:connect :: connect atomics_a_8.corrupt, UInt<1>(0h0)
[1453] FIRRTL:195436 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T = eq(UInt<3>(0h4), req.uop.mem_cmd)
[1454] FIRRTL:195437 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_1 = mux(_atomics_T, atomics_a, _atomics_WIRE)
[1455] FIRRTL:195438 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_2 = eq(UInt<4>(0h9), req.uop.mem_cmd)
[1456] FIRRTL:195439 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_3 = mux(_atomics_T_2, atomics_a_1, _atomics_T_1)
[1457] FIRRTL:195440 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_4 = eq(UInt<4>(0ha), req.uop.mem_cmd)
[1458] FIRRTL:195441 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_5 = mux(_atomics_T_4, atomics_a_2, _atomics_T_3)
[1459] FIRRTL:195442 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_6 = eq(UInt<4>(0hb), req.uop.mem_cmd)
[1460] FIRRTL:195443 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_7 = mux(_atomics_T_6, atomics_a_3, _atomics_T_5)
[1461] FIRRTL:195444 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_8 = eq(UInt<4>(0h8), req.uop.mem_cmd)
[1462] FIRRTL:195445 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_9 = mux(_atomics_T_8, atomics_a_4, _atomics_T_7)
[1463] FIRRTL:195446 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_10 = eq(UInt<4>(0hc), req.uop.mem_cmd)
[1464] FIRRTL:195447 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_11 = mux(_atomics_T_10, atomics_a_5, _atomics_T_9)
[1465] FIRRTL:195448 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_12 = eq(UInt<4>(0hd), req.uop.mem_cmd)
[1466] FIRRTL:195449 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_13 = mux(_atomics_T_12, atomics_a_6, _atomics_T_11)
[1467] FIRRTL:195450 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_14 = eq(UInt<4>(0he), req.uop.mem_cmd)
[1468] FIRRTL:195451 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_15 = mux(_atomics_T_14, atomics_a_7, _atomics_T_13)
[1469] FIRRTL:195452 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node _atomics_T_16 = eq(UInt<4>(0hf), req.uop.mem_cmd)
[1470] FIRRTL:195453 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:426:75 KIND:node :: node atomics = mux(_atomics_T_16, atomics_a_8, _atomics_T_15)
[1471] FIRRTL:195454 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:16 KIND:node :: node _T = eq(state, UInt<2>(0h0))
[1472] FIRRTL:195455 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:46 KIND:node :: node _T_1 = neq(req.uop.mem_cmd, UInt<3>(0h7))
[1473] FIRRTL:195456 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:27 KIND:node :: node _T_2 = or(_T, _T_1)
[1474] FIRRTL:195457 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:node :: node _T_3 = asUInt(reset)
[1475] FIRRTL:195458 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:node :: node _T_4 = eq(_T_3, UInt<1>(0h0))
[1476] FIRRTL:195459 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:when :: when _T_4 :
[1477] FIRRTL:195460 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:node :: node _T_5 = eq(_T_2, UInt<1>(0h0))
[1478] FIRRTL:195461 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:when :: when _T_5 :
[1479] FIRRTL:195462 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed\n    at mshrs.scala:441 assert(state === s_idle || req.uop.mem_cmd =/= M_XSC)\n") : printf
[1480] FIRRTL:195463 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:441:9 KIND:nondriving :: assert(clock, _T_2, UInt<1>(0h1), "") : assert
[1481] FIRRTL:195464 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:443:32 KIND:node :: node _io_mem_access_valid_T = eq(state, UInt<2>(0h1))
[1482] FIRRTL:195465 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:443:23 KIND:connect :: connect io.mem_access.valid, _io_mem_access_valid_T
[1483] FIRRTL:195466 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T = eq(req.uop.mem_cmd, UInt<3>(0h4))
[1484] FIRRTL:195467 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_1 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[1485] FIRRTL:195468 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_2 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[1486] FIRRTL:195469 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_3 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[1487] FIRRTL:195470 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_4 = or(_io_mem_access_bits_T, _io_mem_access_bits_T_1)
[1488] FIRRTL:195471 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_5 = or(_io_mem_access_bits_T_4, _io_mem_access_bits_T_2)
[1489] FIRRTL:195472 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_6 = or(_io_mem_access_bits_T_5, _io_mem_access_bits_T_3)
[1490] FIRRTL:195473 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_7 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[1491] FIRRTL:195474 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_8 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[1492] FIRRTL:195475 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_9 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[1493] FIRRTL:195476 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_10 = eq(req.uop.mem_cmd, UInt<4>(0he))
[1494] FIRRTL:195477 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_11 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[1495] FIRRTL:195478 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_12 = or(_io_mem_access_bits_T_7, _io_mem_access_bits_T_8)
[1496] FIRRTL:195479 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_13 = or(_io_mem_access_bits_T_12, _io_mem_access_bits_T_9)
[1497] FIRRTL:195480 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_14 = or(_io_mem_access_bits_T_13, _io_mem_access_bits_T_10)
[1498] FIRRTL:195481 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_15 = or(_io_mem_access_bits_T_14, _io_mem_access_bits_T_11)
[1499] FIRRTL:195482 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _io_mem_access_bits_T_16 = or(_io_mem_access_bits_T_6, _io_mem_access_bits_T_15)
[1500] FIRRTL:195483 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_17 = eq(req.uop.mem_cmd, UInt<1>(0h0))
[1501] FIRRTL:195484 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_18 = eq(req.uop.mem_cmd, UInt<5>(0h10))
[1502] FIRRTL:195485 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_19 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[1503] FIRRTL:195486 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_20 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[1504] FIRRTL:195487 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_21 = or(_io_mem_access_bits_T_17, _io_mem_access_bits_T_18)
[1505] FIRRTL:195488 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_22 = or(_io_mem_access_bits_T_21, _io_mem_access_bits_T_19)
[1506] FIRRTL:195489 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_23 = or(_io_mem_access_bits_T_22, _io_mem_access_bits_T_20)
[1507] FIRRTL:195490 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_24 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[1508] FIRRTL:195491 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_25 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[1509] FIRRTL:195492 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_26 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[1510] FIRRTL:195493 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_27 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[1511] FIRRTL:195494 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_28 = or(_io_mem_access_bits_T_24, _io_mem_access_bits_T_25)
[1512] FIRRTL:195495 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_29 = or(_io_mem_access_bits_T_28, _io_mem_access_bits_T_26)
[1513] FIRRTL:195496 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_30 = or(_io_mem_access_bits_T_29, _io_mem_access_bits_T_27)
[1514] FIRRTL:195497 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_31 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[1515] FIRRTL:195498 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_32 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[1516] FIRRTL:195499 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_33 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[1517] FIRRTL:195500 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_34 = eq(req.uop.mem_cmd, UInt<4>(0he))
[1518] FIRRTL:195501 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mem_access_bits_T_35 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[1519] FIRRTL:195502 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_36 = or(_io_mem_access_bits_T_31, _io_mem_access_bits_T_32)
[1520] FIRRTL:195503 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_37 = or(_io_mem_access_bits_T_36, _io_mem_access_bits_T_33)
[1521] FIRRTL:195504 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_38 = or(_io_mem_access_bits_T_37, _io_mem_access_bits_T_34)
[1522] FIRRTL:195505 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mem_access_bits_T_39 = or(_io_mem_access_bits_T_38, _io_mem_access_bits_T_35)
[1523] FIRRTL:195506 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _io_mem_access_bits_T_40 = or(_io_mem_access_bits_T_30, _io_mem_access_bits_T_39)
[1524] FIRRTL:195507 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _io_mem_access_bits_T_41 = or(_io_mem_access_bits_T_23, _io_mem_access_bits_T_40)
[1525] FIRRTL:195508 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:444:66 KIND:node :: node _io_mem_access_bits_T_42 = mux(_io_mem_access_bits_T_41, get, put)
[1526] FIRRTL:195509 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:444:29 KIND:node :: node _io_mem_access_bits_T_43 = mux(_io_mem_access_bits_T_16, atomics, _io_mem_access_bits_T_42)
[1527] FIRRTL:195510 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:444:23 KIND:connect :: connect io.mem_access.bits, _io_mem_access_bits_T_43
[1528] FIRRTL:195511 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T = eq(req.uop.mem_cmd, UInt<1>(0h0))
[1529] FIRRTL:195512 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_1 = eq(req.uop.mem_cmd, UInt<5>(0h10))
[1530] FIRRTL:195513 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_2 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[1531] FIRRTL:195514 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_3 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[1532] FIRRTL:195515 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_4 = or(_send_resp_T, _send_resp_T_1)
[1533] FIRRTL:195516 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_5 = or(_send_resp_T_4, _send_resp_T_2)
[1534] FIRRTL:195517 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_6 = or(_send_resp_T_5, _send_resp_T_3)
[1535] FIRRTL:195518 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_7 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[1536] FIRRTL:195519 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_8 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[1537] FIRRTL:195520 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_9 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[1538] FIRRTL:195521 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_10 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[1539] FIRRTL:195522 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_11 = or(_send_resp_T_7, _send_resp_T_8)
[1540] FIRRTL:195523 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_12 = or(_send_resp_T_11, _send_resp_T_9)
[1541] FIRRTL:195524 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_13 = or(_send_resp_T_12, _send_resp_T_10)
[1542] FIRRTL:195525 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_14 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[1543] FIRRTL:195526 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_15 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[1544] FIRRTL:195527 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_16 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[1545] FIRRTL:195528 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_17 = eq(req.uop.mem_cmd, UInt<4>(0he))
[1546] FIRRTL:195529 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _send_resp_T_18 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[1547] FIRRTL:195530 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_19 = or(_send_resp_T_14, _send_resp_T_15)
[1548] FIRRTL:195531 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_20 = or(_send_resp_T_19, _send_resp_T_16)
[1549] FIRRTL:195532 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_21 = or(_send_resp_T_20, _send_resp_T_17)
[1550] FIRRTL:195533 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _send_resp_T_22 = or(_send_resp_T_21, _send_resp_T_18)
[1551] FIRRTL:195534 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _send_resp_T_23 = or(_send_resp_T_13, _send_resp_T_22)
[1552] FIRRTL:195535 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node send_resp = or(_send_resp_T_6, _send_resp_T_23)
[1553] FIRRTL:195536 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:448:31 KIND:node :: node _io_resp_valid_T = eq(state, UInt<2>(0h3))
[1554] FIRRTL:195537 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:448:43 KIND:node :: node _io_resp_valid_T_1 = and(_io_resp_valid_T, send_resp)
[1555] FIRRTL:195538 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:448:21 KIND:connect :: connect io.resp.valid, _io_resp_valid_T_1
[1556] FIRRTL:195539 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:449:21 KIND:connect :: connect io.resp.bits.uop, req.uop
[1557] FIRRTL:195540 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T = bits(req.addr, 2, 2)
[1558] FIRRTL:195541 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_1 = bits(grant_word, 63, 32)
[1559] FIRRTL:195542 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_2 = bits(grant_word, 31, 0)
[1560] FIRRTL:195543 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted = mux(_io_resp_bits_data_shifted_T, _io_resp_bits_data_shifted_T_1, _io_resp_bits_data_shifted_T_2)
[1561] FIRRTL:195544 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero = and(UInt<1>(0h0), UInt<1>(0h0))
[1562] FIRRTL:195545 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed = mux(io_resp_bits_data_doZero, UInt<1>(0h0), io_resp_bits_data_shifted)
[1563] FIRRTL:195546 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T = eq(size, UInt<2>(0h2))
[1564] FIRRTL:195547 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_1 = or(_io_resp_bits_data_T, io_resp_bits_data_doZero)
[1565] FIRRTL:195548 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_2 = bits(io_resp_bits_data_zeroed, 31, 31)
[1566] FIRRTL:195549 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_3 = and(req.uop.mem_signed, _io_resp_bits_data_T_2)
[1567] FIRRTL:195550 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_4 = mux(_io_resp_bits_data_T_3, UInt<32>(0hffffffff), UInt<32>(0h0))
[1568] FIRRTL:195551 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_5 = bits(grant_word, 63, 32)
[1569] FIRRTL:195552 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_6 = mux(_io_resp_bits_data_T_1, _io_resp_bits_data_T_4, _io_resp_bits_data_T_5)
[1570] FIRRTL:195553 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_7 = cat(_io_resp_bits_data_T_6, io_resp_bits_data_zeroed)
[1571] FIRRTL:195554 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T_3 = bits(req.addr, 1, 1)
[1572] FIRRTL:195555 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_4 = bits(_io_resp_bits_data_T_7, 31, 16)
[1573] FIRRTL:195556 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_5 = bits(_io_resp_bits_data_T_7, 15, 0)
[1574] FIRRTL:195557 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted_1 = mux(_io_resp_bits_data_shifted_T_3, _io_resp_bits_data_shifted_T_4, _io_resp_bits_data_shifted_T_5)
[1575] FIRRTL:195558 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero_1 = and(UInt<1>(0h0), UInt<1>(0h0))
[1576] FIRRTL:195559 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed_1 = mux(io_resp_bits_data_doZero_1, UInt<1>(0h0), io_resp_bits_data_shifted_1)
[1577] FIRRTL:195560 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T_8 = eq(size, UInt<1>(0h1))
[1578] FIRRTL:195561 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_9 = or(_io_resp_bits_data_T_8, io_resp_bits_data_doZero_1)
[1579] FIRRTL:195562 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_10 = bits(io_resp_bits_data_zeroed_1, 15, 15)
[1580] FIRRTL:195563 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_11 = and(req.uop.mem_signed, _io_resp_bits_data_T_10)
[1581] FIRRTL:195564 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_12 = mux(_io_resp_bits_data_T_11, UInt<48>(0hffffffffffff), UInt<48>(0h0))
[1582] FIRRTL:195565 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_13 = bits(_io_resp_bits_data_T_7, 63, 16)
[1583] FIRRTL:195566 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_14 = mux(_io_resp_bits_data_T_9, _io_resp_bits_data_T_12, _io_resp_bits_data_T_13)
[1584] FIRRTL:195567 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_15 = cat(_io_resp_bits_data_T_14, io_resp_bits_data_zeroed_1)
[1585] FIRRTL:195568 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_resp_bits_data_shifted_T_6 = bits(req.addr, 0, 0)
[1586] FIRRTL:195569 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_resp_bits_data_shifted_T_7 = bits(_io_resp_bits_data_T_15, 15, 8)
[1587] FIRRTL:195570 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_resp_bits_data_shifted_T_8 = bits(_io_resp_bits_data_T_15, 7, 0)
[1588] FIRRTL:195571 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_resp_bits_data_shifted_2 = mux(_io_resp_bits_data_shifted_T_6, _io_resp_bits_data_shifted_T_7, _io_resp_bits_data_shifted_T_8)
[1589] FIRRTL:195572 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_resp_bits_data_doZero_2 = and(UInt<1>(0h1), UInt<1>(0h0))
[1590] FIRRTL:195573 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_resp_bits_data_zeroed_2 = mux(io_resp_bits_data_doZero_2, UInt<1>(0h0), io_resp_bits_data_shifted_2)
[1591] FIRRTL:195574 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_resp_bits_data_T_16 = eq(size, UInt<1>(0h0))
[1592] FIRRTL:195575 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_resp_bits_data_T_17 = or(_io_resp_bits_data_T_16, io_resp_bits_data_doZero_2)
[1593] FIRRTL:195576 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_resp_bits_data_T_18 = bits(io_resp_bits_data_zeroed_2, 7, 7)
[1594] FIRRTL:195577 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_resp_bits_data_T_19 = and(req.uop.mem_signed, _io_resp_bits_data_T_18)
[1595] FIRRTL:195578 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_resp_bits_data_T_20 = mux(_io_resp_bits_data_T_19, UInt<56>(0hffffffffffffff), UInt<56>(0h0))
[1596] FIRRTL:195579 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_resp_bits_data_T_21 = bits(_io_resp_bits_data_T_15, 63, 8)
[1597] FIRRTL:195580 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_resp_bits_data_T_22 = mux(_io_resp_bits_data_T_17, _io_resp_bits_data_T_20, _io_resp_bits_data_T_21)
[1598] FIRRTL:195581 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_resp_bits_data_T_23 = cat(_io_resp_bits_data_T_22, io_resp_bits_data_zeroed_2)
[1599] FIRRTL:195582 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:450:21 KIND:connect :: connect io.resp.bits.data, _io_resp_bits_data_T_23
[1600] FIRRTL:195583 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:451:25 KIND:connect :: connect io.resp.bits.is_hella, req.is_hella
[1601] FIRRTL:195584 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_6 = and(io.req.ready, io.req.valid)
[1602] FIRRTL:195585 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:453:22 KIND:when :: when _T_6 :
[1603] FIRRTL:195586 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:454:11 KIND:connect :: connect req, io.req.bits
[1604] FIRRTL:195587 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:455:11 KIND:connect :: connect state, UInt<2>(0h1)
[1605] FIRRTL:195588 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_7 = and(io.mem_access.ready, io.mem_access.valid)
[1606] FIRRTL:195589 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:457:29 KIND:when :: when _T_7 :
[1607] FIRRTL:195590 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:458:11 KIND:connect :: connect state, UInt<2>(0h2)
[1608] FIRRTL:195591 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:460:15 KIND:node :: node _T_8 = eq(state, UInt<2>(0h2))
[1609] FIRRTL:195592 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:460:29 KIND:node :: node _T_9 = and(_T_8, io.mem_ack.valid)
[1610] FIRRTL:195593 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:460:50 KIND:when :: when _T_9 :
[1611] FIRRTL:195594 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:461:11 KIND:connect :: connect state, UInt<2>(0h3)
[1612] FIRRTL:195595 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_10 = eq(req.uop.mem_cmd, UInt<1>(0h0))
[1613] FIRRTL:195596 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_11 = eq(req.uop.mem_cmd, UInt<5>(0h10))
[1614] FIRRTL:195597 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_12 = eq(req.uop.mem_cmd, UInt<3>(0h6))
[1615] FIRRTL:195598 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_13 = eq(req.uop.mem_cmd, UInt<3>(0h7))
[1616] FIRRTL:195599 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_14 = or(_T_10, _T_11)
[1617] FIRRTL:195600 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_15 = or(_T_14, _T_12)
[1618] FIRRTL:195601 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_16 = or(_T_15, _T_13)
[1619] FIRRTL:195602 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_17 = eq(req.uop.mem_cmd, UInt<3>(0h4))
[1620] FIRRTL:195603 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_18 = eq(req.uop.mem_cmd, UInt<4>(0h9))
[1621] FIRRTL:195604 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_19 = eq(req.uop.mem_cmd, UInt<4>(0ha))
[1622] FIRRTL:195605 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_20 = eq(req.uop.mem_cmd, UInt<4>(0hb))
[1623] FIRRTL:195606 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_21 = or(_T_17, _T_18)
[1624] FIRRTL:195607 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_22 = or(_T_21, _T_19)
[1625] FIRRTL:195608 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_23 = or(_T_22, _T_20)
[1626] FIRRTL:195609 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_24 = eq(req.uop.mem_cmd, UInt<4>(0h8))
[1627] FIRRTL:195610 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_25 = eq(req.uop.mem_cmd, UInt<4>(0hc))
[1628] FIRRTL:195611 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_26 = eq(req.uop.mem_cmd, UInt<4>(0hd))
[1629] FIRRTL:195612 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_27 = eq(req.uop.mem_cmd, UInt<4>(0he))
[1630] FIRRTL:195613 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _T_28 = eq(req.uop.mem_cmd, UInt<4>(0hf))
[1631] FIRRTL:195614 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_29 = or(_T_24, _T_25)
[1632] FIRRTL:195615 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_30 = or(_T_29, _T_26)
[1633] FIRRTL:195616 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_31 = or(_T_30, _T_27)
[1634] FIRRTL:195617 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _T_32 = or(_T_31, _T_28)
[1635] FIRRTL:195618 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _T_33 = or(_T_23, _T_32)
[1636] FIRRTL:195619 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _T_34 = or(_T_16, _T_33)
[1637] FIRRTL:195620 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:462:36 KIND:when :: when _T_34 :
[1638] FIRRTL:195621 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:404:20 KIND:node :: node grant_word_shift = cat(UInt<1>(0h0), UInt<6>(0h0))
[1639] FIRRTL:195622 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:405:10 KIND:node :: node _grant_word_T = dshr(io.mem_ack.bits.data, grant_word_shift)
[1640] FIRRTL:195623 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:405:19 KIND:node :: node _grant_word_T_1 = bits(_grant_word_T, 63, 0)
[1641] FIRRTL:195624 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:463:18 KIND:connect :: connect grant_word, _grant_word_T_1
[1642] FIRRTL:195625 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:466:15 KIND:node :: node _T_35 = eq(state, UInt<2>(0h3))
[1643] FIRRTL:195626 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:466:27 KIND:when :: when _T_35 :
[1644] FIRRTL:195627 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:467:11 KIND:node :: node _T_36 = eq(send_resp, UInt<1>(0h0))
[1645] FIRRTL:195628 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_37 = and(io.resp.ready, io.resp.valid)
[1646] FIRRTL:195629 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:467:22 KIND:node :: node _T_38 = or(_T_36, _T_37)
[1647] FIRRTL:195630 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:467:39 KIND:when :: when _T_38 :
[1648] FIRRTL:195631 SRC:generators/boom/src/main/scala/v4/lsu/mshrs.scala:468:13 KIND:connect :: connect state, UInt<2>(0h0)
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
  "task_id": "leaf_abstraction-BoomMSHRFile.mmios_0-b0066721dd609259",
  "work_unit_id": "BoomMSHRFile.mmios_0",
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
