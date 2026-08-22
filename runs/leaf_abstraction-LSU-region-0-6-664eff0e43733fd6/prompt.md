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

Task ID: `leaf_abstraction-LSU-region-0-6-664eff0e43733fd6`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-6`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 844
- logical statements: 298
- mapped/logical source lines: 215
- registers: 18
- physical boundary events: 2

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

- `LSU::io.dmem.req.bits[0].valid`
  - predicate: `io.dmem.req.bits[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.dmem.req.bits[0].bits.addr', 'io.dmem.req.bits[0].bits.data', 'io.dmem.req.bits[0].bits.is_hella', 'io.dmem.req.bits[0].bits.uop.bp_debug_if', 'io.dmem.req.bits[0].bits.uop.bp_xcpt_if', 'io.dmem.req.bits[0].bits.uop.br_mask', 'io.dmem.req.bits[0].bits.uop.br_tag', 'io.dmem.req.bits[0].bits.uop.br_type', 'io.dmem.req.bits[0].bits.uop.csr_cmd', 'io.dmem.req.bits[0].bits.uop.debug_fsrc', 'io.dmem.req.bits[0].bits.uop.debug_inst', 'io.dmem.req.bits[0].bits.uop.debug_pc', 'io.dmem.req.bits[0].bits.uop.debug_tsrc', 'io.dmem.req.bits[0].bits.uop.dis_col_sel', 'io.dmem.req.bits[0].bits.uop.dst_rtype', 'io.dmem.req.bits[0].bits.uop.edge_inst', 'io.dmem.req.bits[0].bits.uop.exc_cause', 'io.dmem.req.bits[0].bits.uop.exception', 'io.dmem.req.bits[0].bits.uop.fcn_dw', 'io.dmem.req.bits[0].bits.uop.fcn_op', 'io.dmem.req.bits[0].bits.uop.flush_on_commit', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.div', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fastpipe', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fma', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fromint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ldst', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren1', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren2', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren3', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.sqrt', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap12', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap23', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.toint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagIn', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagOut', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.vec', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wen', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wflags', 'io.dmem.req.bits[0].bits.uop.fp_rm', 'io.dmem.req.bits[0].bits.uop.fp_typ', 'io.dmem.req.bits[0].bits.uop.fp_val', 'io.dmem.req.bits[0].bits.uop.frs3_en', 'io.dmem.req.bits[0].bits.uop.ftq_idx', 'io.dmem.req.bits[0].bits.uop.fu_code[0]', 'io.dmem.req.bits[0].bits.uop.fu_code[1]', 'io.dmem.req.bits[0].bits.uop.fu_code[2]', 'io.dmem.req.bits[0].bits.uop.fu_code[3]', 'io.dmem.req.bits[0].bits.uop.fu_code[4]', 'io.dmem.req.bits[0].bits.uop.fu_code[5]', 'io.dmem.req.bits[0].bits.uop.fu_code[6]', 'io.dmem.req.bits[0].bits.uop.fu_code[7]', 'io.dmem.req.bits[0].bits.uop.fu_code[8]', 'io.dmem.req.bits[0].bits.uop.fu_code[9]', 'io.dmem.req.bits[0].bits.uop.imm_packed', 'io.dmem.req.bits[0].bits.uop.imm_rename', 'io.dmem.req.bits[0].bits.uop.imm_sel', 'io.dmem.req.bits[0].bits.uop.inst', 'io.dmem.req.bits[0].bits.uop.iq_type[0]', 'io.dmem.req.bits[0].bits.uop.iq_type[1]', 'io.dmem.req.bits[0].bits.uop.iq_type[2]', 'io.dmem.req.bits[0].bits.uop.iq_type[3]', 'io.dmem.req.bits[0].bits.uop.is_amo', 'io.dmem.req.bits[0].bits.uop.is_eret', 'io.dmem.req.bits[0].bits.uop.is_fence', 'io.dmem.req.bits[0].bits.uop.is_fencei', 'io.dmem.req.bits[0].bits.uop.is_mov', 'io.dmem.req.bits[0].bits.uop.is_rocc', 'io.dmem.req.bits[0].bits.uop.is_rvc', 'io.dmem.req.bits[0].bits.uop.is_sfb', 'io.dmem.req.bits[0].bits.uop.is_sfence', 'io.dmem.req.bits[0].bits.uop.is_sys_pc2epc', 'io.dmem.req.bits[0].bits.uop.is_unique', 'io.dmem.req.bits[0].bits.uop.iw_issued', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_agen', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_dgen', 'io.dmem.req.bits[0].bits.uop.iw_p1_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p1_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p2_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p2_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p3_bypass_hint', 'io.dmem.req.bits[0].bits.uop.ldq_idx', 'io.dmem.req.bits[0].bits.uop.ldst', 'io.dmem.req.bits[0].bits.uop.ldst_is_rs1', 'io.dmem.req.bits[0].bits.uop.lrs1', 'io.dmem.req.bits[0].bits.uop.lrs1_rtype', 'io.dmem.req.bits[0].bits.uop.lrs2', 'io.dmem.req.bits[0].bits.uop.lrs2_rtype', 'io.dmem.req.bits[0].bits.uop.lrs3', 'io.dmem.req.bits[0].bits.uop.mem_cmd', 'io.dmem.req.bits[0].bits.uop.mem_signed', 'io.dmem.req.bits[0].bits.uop.mem_size', 'io.dmem.req.bits[0].bits.uop.op1_sel', 'io.dmem.req.bits[0].bits.uop.op2_sel', 'io.dmem.req.bits[0].bits.uop.pc_lob', 'io.dmem.req.bits[0].bits.uop.pdst', 'io.dmem.req.bits[0].bits.uop.pimm', 'io.dmem.req.bits[0].bits.uop.ppred', 'io.dmem.req.bits[0].bits.uop.ppred_busy', 'io.dmem.req.bits[0].bits.uop.prs1', 'io.dmem.req.bits[0].bits.uop.prs1_busy', 'io.dmem.req.bits[0].bits.uop.prs2', 'io.dmem.req.bits[0].bits.uop.prs2_busy', 'io.dmem.req.bits[0].bits.uop.prs3', 'io.dmem.req.bits[0].bits.uop.prs3_busy', 'io.dmem.req.bits[0].bits.uop.rob_idx', 'io.dmem.req.bits[0].bits.uop.rxq_idx', 'io.dmem.req.bits[0].bits.uop.stale_pdst', 'io.dmem.req.bits[0].bits.uop.stq_idx', 'io.dmem.req.bits[0].bits.uop.taken', 'io.dmem.req.bits[0].bits.uop.uses_ldq', 'io.dmem.req.bits[0].bits.uop.uses_stq', 'io.dmem.req.bits[0].bits.uop.xcpt_ae_if', 'io.dmem.req.bits[0].bits.uop.xcpt_ma_if', 'io.dmem.req.bits[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'hella_req', 'hella_state', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_executed', 'ldq_head', 'ldq_next_stq_idx', 'ldq_order_fail', 'ldq_succeeded', 'ldq_valid', 'ldq_wakeup_idx', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 'store_blocked_counter', 'stq_almost_full', 'stq_head', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_data', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
- `LSU::io.dmem.req.fire`
  - predicate: `io.dmem.req.valid && io.dmem.req.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.dmem.req.bits[0].bits.addr', 'io.dmem.req.bits[0].bits.data', 'io.dmem.req.bits[0].bits.is_hella', 'io.dmem.req.bits[0].bits.uop.bp_debug_if', 'io.dmem.req.bits[0].bits.uop.bp_xcpt_if', 'io.dmem.req.bits[0].bits.uop.br_mask', 'io.dmem.req.bits[0].bits.uop.br_tag', 'io.dmem.req.bits[0].bits.uop.br_type', 'io.dmem.req.bits[0].bits.uop.csr_cmd', 'io.dmem.req.bits[0].bits.uop.debug_fsrc', 'io.dmem.req.bits[0].bits.uop.debug_inst', 'io.dmem.req.bits[0].bits.uop.debug_pc', 'io.dmem.req.bits[0].bits.uop.debug_tsrc', 'io.dmem.req.bits[0].bits.uop.dis_col_sel', 'io.dmem.req.bits[0].bits.uop.dst_rtype', 'io.dmem.req.bits[0].bits.uop.edge_inst', 'io.dmem.req.bits[0].bits.uop.exc_cause', 'io.dmem.req.bits[0].bits.uop.exception', 'io.dmem.req.bits[0].bits.uop.fcn_dw', 'io.dmem.req.bits[0].bits.uop.fcn_op', 'io.dmem.req.bits[0].bits.uop.flush_on_commit', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.div', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fastpipe', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fma', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fromint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ldst', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren1', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren2', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren3', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.sqrt', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap12', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap23', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.toint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagIn', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagOut', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.vec', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wen', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wflags', 'io.dmem.req.bits[0].bits.uop.fp_rm', 'io.dmem.req.bits[0].bits.uop.fp_typ', 'io.dmem.req.bits[0].bits.uop.fp_val', 'io.dmem.req.bits[0].bits.uop.frs3_en', 'io.dmem.req.bits[0].bits.uop.ftq_idx', 'io.dmem.req.bits[0].bits.uop.fu_code[0]', 'io.dmem.req.bits[0].bits.uop.fu_code[1]', 'io.dmem.req.bits[0].bits.uop.fu_code[2]', 'io.dmem.req.bits[0].bits.uop.fu_code[3]', 'io.dmem.req.bits[0].bits.uop.fu_code[4]', 'io.dmem.req.bits[0].bits.uop.fu_code[5]', 'io.dmem.req.bits[0].bits.uop.fu_code[6]', 'io.dmem.req.bits[0].bits.uop.fu_code[7]', 'io.dmem.req.bits[0].bits.uop.fu_code[8]', 'io.dmem.req.bits[0].bits.uop.fu_code[9]', 'io.dmem.req.bits[0].bits.uop.imm_packed', 'io.dmem.req.bits[0].bits.uop.imm_rename', 'io.dmem.req.bits[0].bits.uop.imm_sel', 'io.dmem.req.bits[0].bits.uop.inst', 'io.dmem.req.bits[0].bits.uop.iq_type[0]', 'io.dmem.req.bits[0].bits.uop.iq_type[1]', 'io.dmem.req.bits[0].bits.uop.iq_type[2]', 'io.dmem.req.bits[0].bits.uop.iq_type[3]', 'io.dmem.req.bits[0].bits.uop.is_amo', 'io.dmem.req.bits[0].bits.uop.is_eret', 'io.dmem.req.bits[0].bits.uop.is_fence', 'io.dmem.req.bits[0].bits.uop.is_fencei', 'io.dmem.req.bits[0].bits.uop.is_mov', 'io.dmem.req.bits[0].bits.uop.is_rocc', 'io.dmem.req.bits[0].bits.uop.is_rvc', 'io.dmem.req.bits[0].bits.uop.is_sfb', 'io.dmem.req.bits[0].bits.uop.is_sfence', 'io.dmem.req.bits[0].bits.uop.is_sys_pc2epc', 'io.dmem.req.bits[0].bits.uop.is_unique', 'io.dmem.req.bits[0].bits.uop.iw_issued', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_agen', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_dgen', 'io.dmem.req.bits[0].bits.uop.iw_p1_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p1_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p2_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p2_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p3_bypass_hint', 'io.dmem.req.bits[0].bits.uop.ldq_idx', 'io.dmem.req.bits[0].bits.uop.ldst', 'io.dmem.req.bits[0].bits.uop.ldst_is_rs1', 'io.dmem.req.bits[0].bits.uop.lrs1', 'io.dmem.req.bits[0].bits.uop.lrs1_rtype', 'io.dmem.req.bits[0].bits.uop.lrs2', 'io.dmem.req.bits[0].bits.uop.lrs2_rtype', 'io.dmem.req.bits[0].bits.uop.lrs3', 'io.dmem.req.bits[0].bits.uop.mem_cmd', 'io.dmem.req.bits[0].bits.uop.mem_signed', 'io.dmem.req.bits[0].bits.uop.mem_size', 'io.dmem.req.bits[0].bits.uop.op1_sel', 'io.dmem.req.bits[0].bits.uop.op2_sel', 'io.dmem.req.bits[0].bits.uop.pc_lob', 'io.dmem.req.bits[0].bits.uop.pdst', 'io.dmem.req.bits[0].bits.uop.pimm', 'io.dmem.req.bits[0].bits.uop.ppred', 'io.dmem.req.bits[0].bits.uop.ppred_busy', 'io.dmem.req.bits[0].bits.uop.prs1', 'io.dmem.req.bits[0].bits.uop.prs1_busy', 'io.dmem.req.bits[0].bits.uop.prs2', 'io.dmem.req.bits[0].bits.uop.prs2_busy', 'io.dmem.req.bits[0].bits.uop.prs3', 'io.dmem.req.bits[0].bits.uop.prs3_busy', 'io.dmem.req.bits[0].bits.uop.rob_idx', 'io.dmem.req.bits[0].bits.uop.rxq_idx', 'io.dmem.req.bits[0].bits.uop.stale_pdst', 'io.dmem.req.bits[0].bits.uop.stq_idx', 'io.dmem.req.bits[0].bits.uop.taken', 'io.dmem.req.bits[0].bits.uop.uses_ldq', 'io.dmem.req.bits[0].bits.uop.uses_stq', 'io.dmem.req.bits[0].bits.uop.xcpt_ae_if', 'io.dmem.req.bits[0].bits.uop.xcpt_ma_if', 'io.dmem.req.bits[0].bits.uop.xcpt_pf_if', 'io.dmem.req.bits[0].valid']
  - immediate registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'hella_req', 'hella_state', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_executed', 'ldq_head', 'ldq_next_stq_idx', 'ldq_order_fail', 'ldq_succeeded', 'ldq_valid', 'ldq_wakeup_idx', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 'store_blocked_counter', 'stq_almost_full', 'stq_head', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_data', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'hella_req', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_executed', 'ldq_head', 'ldq_next_stq_idx', 'ldq_order_fail', 'ldq_succeeded', 'ldq_valid', 'ldq_wakeup_idx', 'p1_block_load_mask', 'p2_block_load_mask', 'store_blocked_counter', 'stq_head']

## Environment/frontier signals

['REG_11', '_T_1118', '_T_1120', '_T_1122', '_T_1123', '_T_1124', '_T_1127', '_T_1128', '_T_1136', '_T_1143', '_T_1149', '_T_1150', '_T_1151', '_T_145', '_T_164', '_T_258', '_T_266', '_T_27', '_T_272', '_T_281', '_T_284', '_T_310', '_T_318', '_T_324', '_T_333', '_T_336', '_T_362', '_T_370', '_T_376', '_T_385', '_T_388', '_T_414', '_T_422', '_T_428', '_T_437', '_T_440', '_T_466', '_T_474', '_T_480', '_T_489', '_T_492', '_T_518', '_T_526', '_T_532', '_T_541', '_T_544', '_T_570', '_T_578', '_T_584', '_T_593', '_T_596', '_T_622', '_T_630', '_T_636', '_T_645', '_T_648', '_T_681', '_T_714', '_T_72', '_T_727', '_T_867', '_block_load_mask_WIRE', '_can_fire_hella_incoming_WIRE', '_can_fire_hella_wakeup_WIRE', '_can_fire_load_wakeup_WIRE', '_dmem_req_0_bits_uop_WIRE', '_exe_tlb_uop_WIRE', '_exe_tlb_uop_WIRE_1', '_ldq_wakeup_e_e_bits_uop_T', '_stq_head_is_fence_T', '_will_fire_load_wakeup_0_T_5', '_will_fire_load_wakeup_0_T_8', '_will_fire_store_agen_0_T_2', '_will_fire_store_agen_0_T_5', '_will_fire_store_agen_0_T_8', 'block_load_mask', 'block_load_wakeup', 'can_enq_load_retry', 'can_enq_store_retry', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'can_fire_store_commit_slow[0]', 'clear_store', 'commit_store', 'dis_ld_val', 'dis_uops[0].bits.br_mask', 'dis_uops[0].bits.ldq_idx', 'dmem_req', 'dmem_req[0].bits.addr', 'dmem_req[0].valid', 'dmem_req_0_bits_data_size', 'dmem_req_0_bits_data_size_1', 'dmem_req_0_bits_data_size_2', 'dtlb.io.req[0].ready', 'dtlb.io.req[0].valid', 'dtlb.io.resp[0].cacheable', 'dtlb.io.resp[0].miss', 'dtlb.io.resp[0].paddr', 'exe_agen_killed[0]', 'exe_tlb_miss[0]', 'exe_tlb_paddr[0]', 'exe_tlb_uncacheable[0]', 'exe_tlb_uop[0]', 'exe_tlb_uop[0].br_mask', 'exe_tlb_uop[0].is_fence', 'exe_tlb_uop[0].mem_cmd', 'exe_tlb_uop[0].mem_size', 'exe_tlb_uop[0].pdst', 'exe_tlb_uop[0].uses_ldq', 'exe_tlb_uop[0].uses_stq', 'exe_tlb_vaddr[0]', 'exe_tlb_valid[0]', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'ha', 'hb', 'hc', 'hd', 'he', 'hella_data.data', 'hella_paddr', 'hella_req.addr', 'hella_req.cmd', 'hella_req.data', 'hella_req.mask', 'hella_req.phys', 'hella_req.signed', 'hella_req.size', 'hella_req.tag', 'hella_state', 'hf', 'io.core.agen[0].bits.data', 'io.core.agen[0].bits.uop.br_mask', 'io.core.agen[0].bits.uop.ldq_idx', 'io.core.brupdate.b1.mispredict_mask', 'io.core.commit.uops[0].uses_ldq', 'io.core.commit.uops[0].uses_stq', 'io.core.commit.valids[0]', 'io.core.commit_load_at_rob_head', 'io.core.dis_uops[0].bits.exception', 'io.core.dis_uops[0].bits.uses_ldq', 'io.core.dis_uops[0].valid', 'io.core.exception', 'io.core.sfence.bits.addr', 'io.dmem.nack[0].bits.is_hella', 'io.dmem.nack[0].bits.uop.ldq_idx', 'io.dmem.nack[0].bits.uop.uses_ldq', 'io.dmem.nack[0].valid', 'io.dmem.ordered', 'io.dmem.req.bits[0].bits.addr', 'io.dmem.req.bits[0].bits.data', 'io.dmem.req.bits[0].bits.is_hella', 'io.dmem.req.bits[0].bits.uop.bp_debug_if', 'io.dmem.req.bits[0].bits.uop.bp_xcpt_if', 'io.dmem.req.bits[0].bits.uop.br_mask', 'io.dmem.req.bits[0].bits.uop.br_tag', 'io.dmem.req.bits[0].bits.uop.br_type', 'io.dmem.req.bits[0].bits.uop.csr_cmd', 'io.dmem.req.bits[0].bits.uop.debug_fsrc', 'io.dmem.req.bits[0].bits.uop.debug_inst', 'io.dmem.req.bits[0].bits.uop.debug_pc', 'io.dmem.req.bits[0].bits.uop.debug_tsrc', 'io.dmem.req.bits[0].bits.uop.dis_col_sel', 'io.dmem.req.bits[0].bits.uop.dst_rtype', 'io.dmem.req.bits[0].bits.uop.edge_inst', 'io.dmem.req.bits[0].bits.uop.exc_cause', 'io.dmem.req.bits[0].bits.uop.exception', 'io.dmem.req.bits[0].bits.uop.fcn_dw', 'io.dmem.req.bits[0].bits.uop.fcn_op', 'io.dmem.req.bits[0].bits.uop.flush_on_commit', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.div', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fastpipe', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fma', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.fromint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ldst', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren1', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren2', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.ren3', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.sqrt', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap12', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.swap23', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.toint', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagIn', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.typeTagOut', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.vec', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wen', 'io.dmem.req.bits[0].bits.uop.fp_ctrl.wflags', 'io.dmem.req.bits[0].bits.uop.fp_rm', 'io.dmem.req.bits[0].bits.uop.fp_typ', 'io.dmem.req.bits[0].bits.uop.fp_val', 'io.dmem.req.bits[0].bits.uop.frs3_en', 'io.dmem.req.bits[0].bits.uop.ftq_idx', 'io.dmem.req.bits[0].bits.uop.fu_code[0]', 'io.dmem.req.bits[0].bits.uop.fu_code[1]', 'io.dmem.req.bits[0].bits.uop.fu_code[2]', 'io.dmem.req.bits[0].bits.uop.fu_code[3]', 'io.dmem.req.bits[0].bits.uop.fu_code[4]', 'io.dmem.req.bits[0].bits.uop.fu_code[5]', 'io.dmem.req.bits[0].bits.uop.fu_code[6]', 'io.dmem.req.bits[0].bits.uop.fu_code[7]', 'io.dmem.req.bits[0].bits.uop.fu_code[8]', 'io.dmem.req.bits[0].bits.uop.fu_code[9]', 'io.dmem.req.bits[0].bits.uop.imm_packed', 'io.dmem.req.bits[0].bits.uop.imm_rename', 'io.dmem.req.bits[0].bits.uop.imm_sel', 'io.dmem.req.bits[0].bits.uop.inst', 'io.dmem.req.bits[0].bits.uop.iq_type[0]', 'io.dmem.req.bits[0].bits.uop.iq_type[1]', 'io.dmem.req.bits[0].bits.uop.iq_type[2]', 'io.dmem.req.bits[0].bits.uop.iq_type[3]', 'io.dmem.req.bits[0].bits.uop.is_amo', 'io.dmem.req.bits[0].bits.uop.is_eret', 'io.dmem.req.bits[0].bits.uop.is_fence', 'io.dmem.req.bits[0].bits.uop.is_fencei', 'io.dmem.req.bits[0].bits.uop.is_mov', 'io.dmem.req.bits[0].bits.uop.is_rocc', 'io.dmem.req.bits[0].bits.uop.is_rvc', 'io.dmem.req.bits[0].bits.uop.is_sfb', 'io.dmem.req.bits[0].bits.uop.is_sfence', 'io.dmem.req.bits[0].bits.uop.is_sys_pc2epc', 'io.dmem.req.bits[0].bits.uop.is_unique', 'io.dmem.req.bits[0].bits.uop.iw_issued', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_agen', 'io.dmem.req.bits[0].bits.uop.iw_issued_partial_dgen', 'io.dmem.req.bits[0].bits.uop.iw_p1_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p1_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p2_bypass_hint', 'io.dmem.req.bits[0].bits.uop.iw_p2_speculative_child', 'io.dmem.req.bits[0].bits.uop.iw_p3_bypass_hint', 'io.dmem.req.bits[0].bits.uop.ldq_idx', 'io.dmem.req.bits[0].bits.uop.ldst', 'io.dmem.req.bits[0].bits.uop.ldst_is_rs1', 'io.dmem.req.bits[0].bits.uop.lrs1', 'io.dmem.req.bits[0].bits.uop.lrs1_rtype', 'io.dmem.req.bits[0].bits.uop.lrs2', 'io.dmem.req.bits[0].bits.uop.lrs2_rtype', 'io.dmem.req.bits[0].bits.uop.lrs3', 'io.dmem.req.bits[0].bits.uop.mem_cmd', 'io.dmem.req.bits[0].bits.uop.mem_signed', 'io.dmem.req.bits[0].bits.uop.mem_size', 'io.dmem.req.bits[0].bits.uop.op1_sel', 'io.dmem.req.bits[0].bits.uop.op2_sel', 'io.dmem.req.bits[0].bits.uop.pc_lob', 'io.dmem.req.bits[0].bits.uop.pdst', 'io.dmem.req.bits[0].bits.uop.pimm', 'io.dmem.req.bits[0].bits.uop.ppred', 'io.dmem.req.bits[0].bits.uop.ppred_busy', 'io.dmem.req.bits[0].bits.uop.prs1', 'io.dmem.req.bits[0].bits.uop.prs1_busy', 'io.dmem.req.bits[0].bits.uop.prs2', 'io.dmem.req.bits[0].bits.uop.prs2_busy', 'io.dmem.req.bits[0].bits.uop.prs3', 'io.dmem.req.bits[0].bits.uop.prs3_busy', 'io.dmem.req.bits[0].bits.uop.rob_idx', 'io.dmem.req.bits[0].bits.uop.rxq_idx', 'io.dmem.req.bits[0].bits.uop.stale_pdst', 'io.dmem.req.bits[0].bits.uop.stq_idx', 'io.dmem.req.bits[0].bits.uop.taken', 'io.dmem.req.bits[0].bits.uop.uses_ldq', 'io.dmem.req.bits[0].bits.uop.uses_stq', 'io.dmem.req.bits[0].bits.uop.xcpt_ae_if', 'io.dmem.req.bits[0].bits.uop.xcpt_ma_if', 'io.dmem.req.bits[0].bits.uop.xcpt_pf_if', 'io.dmem.req.bits[0].valid', 'io.dmem.req.valid', 'io.hellacache.req.ready', 'io.hellacache.req.valid', 'io.hellacache.s1_data.data', 'io.hellacache.s1_kill', 'lcam_ldq_idx[0]', 'lcam_younger_load_mask[0][0]', 'lcam_younger_load_mask[0][1]', 'lcam_younger_load_mask[0][2]', 'lcam_younger_load_mask[0][3]', 'lcam_younger_load_mask[0][4]', 'lcam_younger_load_mask[0][5]', 'lcam_younger_load_mask[0][6]', 'lcam_younger_load_mask[0][7]', 'ldq_addr[*]', 'ldq_addr[*].valid', 'ldq_addr[0].valid', 'ldq_addr[1].valid', 'ldq_addr[2].valid', 'ldq_addr[3].valid', 'ldq_addr[4].valid', 'ldq_addr[5].valid', 'ldq_addr[6].valid', 'ldq_addr[7].valid', 'ldq_addr_is_uncacheable[*]', 'ldq_addr_is_virtual[*]', 'ldq_addr_is_virtual[0]', 'ldq_addr_is_virtual[1]', 'ldq_addr_is_virtual[2]', 'ldq_addr_is_virtual[3]', 'ldq_addr_is_virtual[4]', 'ldq_addr_is_virtual[5]', 'ldq_addr_is_virtual[6]', 'ldq_addr_is_virtual[7]', 'ldq_enq_retry_e.bits.addr.bits', 'ldq_enq_retry_e_e', 'ldq_enq_retry_idx', 'ldq_executed[*]', 'ldq_executed[0]', 'ldq_executed[1]', 'ldq_executed[2]', 'ldq_executed[3]', 'ldq_executed[4]', 'ldq_executed[5]', 'ldq_executed[6]', 'ldq_executed[7]', 'ldq_head', 'ldq_idx', 'ldq_incoming_idx[0]', 'ldq_next_stq_idx[*]', 'ldq_order_fail[*]', 'ldq_order_fail[0]', 'ldq_order_fail[1]', 'ldq_order_fail[2]', 'ldq_order_fail[3]', 'ldq_order_fail[4]', 'ldq_order_fail[5]', 'ldq_order_fail[6]', 'ldq_order_fail[7]', 'ldq_succeeded[*]', 'ldq_succeeded[0]', 'ldq_succeeded[1]', 'ldq_succeeded[2]', 'ldq_succeeded[3]', 'ldq_succeeded[4]', 'ldq_succeeded[5]', 'ldq_succeeded[6]', 'ldq_succeeded[7]', 'ldq_tail', 'ldq_valid[*]', 'ldq_valid[0]', 'ldq_valid[1]', 'ldq_valid[2]', 'ldq_valid[3]', 'ldq_valid[4]', 'ldq_valid[5]', 'ldq_valid[6]', 'ldq_valid[7]', 'ldq_wakeup_e.bits.addr_is_virtual', 'ldq_wakeup_e.bits.executed', 'ldq_wakeup_e.bits.next_stq_idx', 'ldq_wakeup_e.bits.uop.br_mask', 'ldq_wakeup_e.valid', 'ldq_wakeup_e_e', 'ldq_wakeup_idx', 'ldq_will_succeed', 'ldst_addr_matches[0]', 'p1_block_load_mask', 'retry_queue.io.deq.bits.data', 'retry_queue.io.deq.bits.uop', 'retry_queue.io.deq.bits.uop.ldq_idx', 'retry_queue.io.deq.bits.uop.uses_ldq', 'retry_queue.io.deq.bits.uop.uses_stq', 'retry_queue.io.deq.valid', 'retry_queue.io.enq.ready', 'retry_queue.io.enq.valid', 's1_executing_loads', 'store_blocked_counter', 'store_needs_order', 'stq_addr[*]', 'stq_addr_is_virtual[*]', 'stq_committed[*]', 'stq_enq_retry_e.bits.addr.bits', 'stq_enq_retry_e_e', 'stq_enq_retry_idx', 'stq_execute_queue.io.deq.bits.addr.bits', 'stq_execute_queue.io.deq.bits.data.bits', 'stq_execute_queue.io.deq.bits.uop.mem_size', 'stq_head', 'stq_succeeded[*]', 'stq_tail', 'stq_uop[*].is_fence', 'stq_valid[*]', 'uop_10.br_mask', 'uop_11.br_mask', 'uop_12.br_mask', 'uop_13.br_mask', 'uop_14.br_mask', 'uop_15.br_mask', 'uop_16.br_mask', 'uop_9.br_mask', 'wb_ldst_forward_ldq_idx[0]', 'wb_ldst_forward_valid[0]', 'will_fire_hella_incoming[0]', 'will_fire_hella_wakeup[0]', 'will_fire_load_agen[0]', 'will_fire_load_agen_0_will_fire', 'will_fire_load_agen_exec[0]', 'will_fire_load_agen_exec_0_will_fire', 'will_fire_load_retry[0]', 'will_fire_load_wakeup[0]', 'will_fire_release_0_will_fire', 'will_fire_sfence[0]', 'will_fire_sfence_0_will_fire', 'will_fire_store_agen[0]', 'will_fire_store_agen_0_will_fire', 'will_fire_store_commit_fast[0]', 'will_fire_store_commit_fast_0_will_fire', 'will_fire_store_commit_slow[0]', 'will_fire_store_commit_slow_0_will_fire', 'will_fire_store_retry[0]']

## Source evidence

### generators/boom/src/main/scala/v4/common/consts.scala:140-142
```scala

  def NullMicroOp(implicit p: Parameters) = 0.U.asTypeOf(new boom.v4.common.MicroOp)
}
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:237-248
```scala
    val e = Wire(Valid(new LDQEntry))
    e.valid                    := ldq_valid              (idx)
    e.bits.uop                 := ldq_uop                (idx)
    e.bits.addr                := ldq_addr               (idx)
    e.bits.addr_is_virtual     := ldq_addr_is_virtual    (idx)
    e.bits.addr_is_uncacheable := ldq_addr_is_uncacheable(idx)
    e.bits.executed            := ldq_executed           (idx)
    e.bits.succeeded           := ldq_succeeded          (idx)
    e.bits.order_fail          := ldq_order_fail         (idx)
    e.bits.observed            := ldq_observed           (idx)
    e.bits.next_stq_idx        := ldq_next_stq_idx       (idx)    
    e.bits.ld_byte_mask        := ldq_ld_byte_mask       (idx)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:267-272
```scala
    val e = Wire(Valid(new STQEntry))
    e.valid                    := stq_valid              (idx)
    e.bits.uop                 := stq_uop                (idx)
    e.bits.addr                := stq_addr               (idx)
    e.bits.addr_is_virtual     := stq_addr_is_virtual    (idx)
    e.bits.data                := stq_data               (idx)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:322-324
```scala

  val clear_store     = WireInit(false.B)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:325-327
```scala

  def widthMap[T <: Data](f: Int => T) = VecInit((0 until lsuWidth).map(f))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:330-332
```scala
  val ldq_will_succeed        = WireDefault(ldq_succeeded)
  ldq_succeeded := ldq_will_succeed
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:374-376
```scala

    val dis_ld_val = io.core.dis_uops(w).valid && io.core.dis_uops(w).bits.uses_ldq && !io.core.dis_uops(w).bits.exception
    val dis_st_val = io.core.dis_uops(w).valid && io.core.dis_uops(w).bits.uses_stq && !io.core.dis_uops(w).bits.exception
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:380-384
```scala

    when (dis_ld_val) {
      dis_ldq_oh(actual_ld_enq_idx) := true.B
      ldq_next_stq_idx           (actual_ld_enq_idx)  := st_enq_idx
      assert (actual_ld_enq_idx === io.core.dis_uops(w).bits.ldq_idx, "[lsu] mismatch enq load tag.")
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:395-402
```scala
      val ldq_idx = dis_uops(w).bits.ldq_idx
      ldq_valid          (ldq_idx)       := !IsKilledByBranch(io.core.brupdate, io.core.exception, dis_uops(w).bits)
      ldq_uop            (ldq_idx)       := UpdateBrMask(io.core.brupdate, dis_uops(w).bits)
      ldq_addr           (ldq_idx).valid := false.B
      ldq_executed       (ldq_idx)       := false.B
      ldq_will_succeed   (ldq_idx)       := false.B
      ldq_order_fail     (ldq_idx)       := false.B
      ldq_observed       (ldq_idx)       := false.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:480-484
```scala
  // The block_load_mask may be wrong, but the executing_load mask must be accurate
  val block_load_mask    = WireInit(VecInit((0 until numLdqEntries).map(x=>false.B)))
  val p1_block_load_mask = RegNext(block_load_mask)
  val p2_block_load_mask = RegNext(p1_block_load_mask)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:490-492
```scala
  // Delay firing load wakeups and retries now
  val store_needs_order = WireInit(false.B)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:499-504
```scala
  val ldq_wakeup_idx = SafeRegNext(LSUAgePriorityEncoder((0 until numLdqEntries).map(i=> {
    val block = block_load_mask(i) || p1_block_load_mask(i)
    ldq_addr(i).valid && !ldq_executed(i) && !ldq_succeeded(i) && !ldq_addr_is_virtual(i) && !block
  }), ldq_head))
  val ldq_wakeup_e   = WireInit(ldq_read(ldq_wakeup_idx))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:510-512
```scala
  }), ldq_head)
  val ldq_enq_retry_e = WireInit(ldq_read(ldq_enq_retry_idx))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:516-524
```scala
  }), stq_commit_head)
  val stq_enq_retry_e   = WireInit(stq_read(stq_enq_retry_idx))

  val can_enq_load_retry    = (ldq_enq_retry_e.valid                            &&
                               ldq_enq_retry_e.bits.addr.valid                  &&
                               ldq_enq_retry_e.bits.addr_is_virtual)
  val can_enq_store_retry   = (stq_enq_retry_e.valid                            &&
                               stq_enq_retry_e.bits.addr.valid                  &&
                               stq_enq_retry_e.bits.addr_is_virtual)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:529-531
```scala

  retry_queue.io.enq.valid     := can_enq_store_retry || can_enq_load_retry
  retry_queue.io.enq.bits      := DontCare
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:538-543
```scala

  when (can_enq_store_retry && retry_queue.io.enq.fire) {
    stq_addr(stq_enq_retry_idx).valid := false.B
  } .elsewhen (can_enq_load_retry && retry_queue.io.enq.fire) {
    ldq_addr(ldq_enq_retry_idx).valid := false.B
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:596-600
```scala
  val can_fire_load_retry    = widthMap(w =>
                               ( retry_queue.io.deq.valid                     &&
                                 retry_queue.io.deq.bits.uop.uses_ldq         &&
                                !RegNext(store_needs_order)                   &&
                                (w == lsuWidth-1).B))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:603-606
```scala
  val can_fire_store_retry   = widthMap(w =>
                               ( retry_queue.io.deq.valid                     &&
                                 retry_queue.io.deq.bits.uop.uses_stq         &&
                                 (w == lsuWidth-1).B))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:616-632
```scala
  // Can we wakeup a load that was nack'd
  val block_load_wakeup = WireInit(false.B)
  val can_fire_load_wakeup = widthMap(w =>
                             ( ldq_wakeup_e.valid                                      &&
                               ldq_wakeup_e.bits.addr.valid                            &&
                              !ldq_wakeup_e.bits.succeeded                             &&
                              !ldq_wakeup_e.bits.addr_is_virtual                       &&
                              !ldq_wakeup_e.bits.executed                              &&
                              !ldq_wakeup_e.bits.order_fail                            &&
                              !p1_block_load_mask(ldq_wakeup_idx)                      &&
                              !p2_block_load_mask(ldq_wakeup_idx)                      &&
                              !RegNext(store_needs_order)                              &&
                              !block_load_wakeup                                       &&
                              (w == lsuWidth-1).B                                      &&
                              (!ldq_wakeup_e.bits.addr_is_uncacheable || (io.core.commit_load_at_rob_head &&
                                                                          ldq_head === ldq_wakeup_idx &&
                                                                          IdxAgeYe(stq_head, ldq_wakeup_e.bits.next_stq_idx)))))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:635-637
```scala
  // Can we fire an incoming hellacache request
  val can_fire_hella_incoming  = WireInit(widthMap(w => false.B)) // This is assigned to in the hellashim ocntroller
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:638-640
```scala
  // Can we fire a hellacache request that the dcache nack'd
  val can_fire_hella_wakeup    = WireInit(widthMap(w => false.B)) // This is assigned to in the hellashim controller
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:650-657
```scala
    def lsu_sched(can_fire: Bool, uses_tlb:Boolean, uses_dc:Boolean, uses_lcam: Boolean): Bool = {
      val will_fire = can_fire && !(uses_tlb.B && !tlb_avail) &&
                                  !(uses_lcam.B && !lcam_avail) &&
                                  !(uses_dc.B && !dc_avail)
      tlb_avail  = tlb_avail  && !(will_fire && uses_tlb.B)
      lcam_avail = lcam_avail && !(will_fire && uses_lcam.B)
      dc_avail   = dc_avail   && !(will_fire && uses_dc.B)
      dontTouch(will_fire) // dontTouch these so we can inspect the will_fire signals
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:667-680
```scala
    //  - Store commits are lowest priority, since they don't "block" younger instructions unless stq fills up
    will_fire_sfence           (w) := lsu_sched(can_fire_sfence           (w) , true , false, false) // TLB ,    ,
    will_fire_store_commit_fast(w) := lsu_sched(can_fire_store_commit_fast(w) , false, true , false) //     , DC          If store queue is filling up, prioritize draining it
    will_fire_load_agen_exec   (w) := lsu_sched(can_fire_load_agen_exec   (w) , true , true , true ) // TLB , DC , LCAM   Normally fire loads as soon as translation completes
    will_fire_load_agen        (w) := lsu_sched(can_fire_load_agen        (w) , true , false, true ) // TLB ,    , LCAM   If we are draining stores, still translate the loads
    will_fire_store_agen       (w) := lsu_sched(can_fire_store_agen       (w) , true , false, true ) // TLB ,    , LCAM
    will_fire_release          (w) := lsu_sched(can_fire_release          (w) , false, false, true ) //            LCAM
    will_fire_hella_incoming   (w) := lsu_sched(can_fire_hella_incoming   (w) , true , true , false) // TLB , DC
    will_fire_hella_wakeup     (w) := lsu_sched(can_fire_hella_wakeup     (w) , false, true , false) //     , DC
    will_fire_store_retry      (w) := lsu_sched(can_fire_store_retry      (w) , true , false, true ) // TLB ,    , LCAM
    will_fire_load_retry       (w) := lsu_sched(can_fire_load_retry       (w) , true , true , true ) // TLB , DC , LCAM
    will_fire_load_wakeup      (w) := lsu_sched(can_fire_load_wakeup      (w) , false, true , true ) //     , DC , LCAM
    will_fire_store_commit_slow(w) := lsu_sched(can_fire_store_commit_slow(w) , false, true , false) //     , DC
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:683-692
```scala

    when (will_fire_load_wakeup(w)) {
      block_load_mask(ldq_wakeup_idx)           := true.B
    } .elsewhen (will_fire_load_agen(w) || will_fire_load_agen_exec(w)) {
      block_load_mask(agen(w).bits.uop.ldq_idx) := true.B
    } .elsewhen (will_fire_load_retry(w)) {
      block_load_mask(ldq_retry_idx)            := true.B
    }
    exe_tlb_valid(w) := !tlb_avail
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:711-718
```scala
  val exe_tlb_uop = widthMap(w =>
                    Mux(will_fire_load_agen_exec(w) ||
                        will_fire_load_agen     (w)  , ldq_incoming_e(w).bits.uop,
                    Mux(will_fire_store_agen    (w)  , stq_incoming_e(w).bits.uop,
                    Mux(will_fire_load_retry    (w) ||
                        will_fire_store_retry   (w)  , retry_queue.io.deq.bits.uop,
                    Mux(will_fire_hella_incoming(w)  , 0.U.asTypeOf(new MicroOp),
                                                       0.U.asTypeOf(new MicroOp))))))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:720-728
```scala
  val exe_tlb_vaddr = widthMap(w =>
                    Mux(will_fire_load_agen_exec(w) ||
                        will_fire_load_agen     (w) ||
                        will_fire_store_agen    (w)  , agen(w).bits.data,
                    Mux(will_fire_sfence        (w)  , io.core.sfence.bits.addr,
                    Mux(will_fire_load_retry    (w) ||
                        will_fire_store_retry   (w)  , retry_queue.io.deq.bits.data,
                    Mux(will_fire_hella_incoming(w)  , hella_req.addr,
                                                       0.U)))))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:757-759
```scala
  for (w <- 0 until lsuWidth) {
    dtlb.io.req(w).valid            := exe_tlb_valid(w)
    dtlb.io.req(w).bits.vaddr       := exe_tlb_vaddr(w)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:829-834
```scala

  val exe_tlb_miss  = widthMap(w => dtlb.io.req(w).valid && (dtlb.io.resp(w).miss || !dtlb.io.req(w).ready))
  val exe_tlb_paddr = widthMap(w => Cat(dtlb.io.resp(w).paddr(paddrBits-1,corePgIdxBits),
                                        exe_tlb_vaddr(w)(corePgIdxBits-1,0)))
  val exe_tlb_uncacheable = widthMap(w => !(dtlb.io.resp(w).cacheable))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:872-875
```scala
  val dmem_req = Wire(Vec(lsuWidth, Valid(new BoomDCacheReq)))
  io.dmem.req.valid := dmem_req.map(_.valid).reduce(_||_)
  io.dmem.req.bits  := dmem_req
  val dmem_req_fire = widthMap(w => dmem_req(w).valid && io.dmem.req.fire)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:880-886
```scala
  for (w <- 0 until lsuWidth) {
    dmem_req(w).valid := false.B
    dmem_req(w).bits.uop   := NullMicroOp
    dmem_req(w).bits.addr  := 0.U
    dmem_req(w).bits.data  := 0.U
    dmem_req(w).bits.is_hella := false.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:889-894
```scala

    when (will_fire_load_agen_exec(w)) {
      dmem_req(w).valid      := true.B
      dmem_req(w).bits.addr  := exe_tlb_paddr(w)
      dmem_req(w).bits.uop   := exe_tlb_uop(w)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:898-903
```scala
      assert(!ldq_incoming_e(w).bits.executed)
    } .elsewhen (will_fire_load_retry(w)) {
      dmem_req(w).valid      := true.B
      dmem_req(w).bits.addr  := exe_tlb_paddr(w)
      dmem_req(w).bits.uop   := exe_tlb_uop(w)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:905-910
```scala
      s0_executing_loads(ldq_retry_idx) := dmem_req_fire(w) && !s0_kills(w)
    } .elsewhen (will_fire_store_commit_slow(w) || will_fire_store_commit_fast(w)) {
      dmem_req(w).valid         := true.B
      dmem_req(w).bits.addr     := stq_commit_e.bits.addr.bits
      dmem_req(w).bits.data     := (new freechips.rocketchip.rocket.StoreGen(
                                    stq_commit_e.bits.uop.mem_size, 0.U,
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:912-914
```scala
                                    coreDataBytes)).data
      dmem_req(w).bits.uop      := stq_commit_e.bits.uop
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:920-925
```scala
      stq_succeeded(stq_commit_e.bits.uop.stq_idx) := false.B
    } .elsewhen (will_fire_load_wakeup(w)) {
      dmem_req(w).valid      := true.B
      dmem_req(w).bits.addr  := ldq_wakeup_e.bits.addr.bits
      dmem_req(w).bits.uop   := ldq_wakeup_e.bits.uop
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:928-930
```scala
      assert(!ldq_wakeup_e.bits.executed && !ldq_wakeup_e.bits.addr_is_virtual)
    } .elsewhen (will_fire_hella_incoming(w)) {
      assert(hella_state === h_s1)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:931-935
```scala

      dmem_req(w).valid               := !io.hellacache.s1_kill && (!exe_tlb_miss(w) || hella_req.phys)
      dmem_req(w).bits.addr           := exe_tlb_paddr(w)
      dmem_req(w).bits.data           := (new freechips.rocketchip.rocket.StoreGen(
        hella_req.size, 0.U,
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:937-942
```scala
        coreDataBytes)).data
      dmem_req(w).bits.uop.mem_cmd    := hella_req.cmd
      dmem_req(w).bits.uop.mem_size   := hella_req.size
      dmem_req(w).bits.uop.mem_signed := hella_req.signed
      dmem_req(w).bits.is_hella       := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:945-951
```scala
      .elsewhen (will_fire_hella_wakeup(w))
    {
      assert(hella_state === h_replay)
      dmem_req(w).valid               := true.B
      dmem_req(w).bits.addr           := hella_paddr
      dmem_req(w).bits.data           := (new freechips.rocketchip.rocket.StoreGen(
        hella_req.size, 0.U,
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:953-958
```scala
        coreDataBytes)).data
      dmem_req(w).bits.uop.mem_cmd    := hella_req.cmd
      dmem_req(w).bits.uop.mem_size   := hella_req.size
      dmem_req(w).bits.uop.mem_signed := hella_req.signed
      dmem_req(w).bits.is_hella       := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:961-967
```scala
    // Write Addr into the LAQ/SAQ
    when (will_fire_load_agen(w) || will_fire_load_agen_exec(w) || will_fire_load_retry(w))
    {
      val ldq_idx = Mux(will_fire_load_agen(w) || will_fire_load_agen_exec(w), ldq_incoming_idx(w), ldq_retry_idx)
      ldq_addr               (ldq_idx).valid  := !exe_agen_killed(w) || will_fire_load_retry(w)
      ldq_addr               (ldq_idx).bits   := Mux(exe_tlb_miss(w), exe_tlb_vaddr(w), exe_tlb_paddr(w))
      ldq_ld_byte_mask       (ldq_idx)        := GenByteMask(exe_tlb_vaddr(w), exe_tlb_uop(w).mem_size)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:968-971
```scala
      ldq_uop                (ldq_idx).pdst   := exe_tlb_uop(w).pdst
      ldq_addr_is_virtual    (ldq_idx)        := exe_tlb_miss(w)
      ldq_addr_is_uncacheable(ldq_idx)        := exe_tlb_uncacheable(w) && !exe_tlb_miss(w)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1171-1173
```scala
  val s1_executing_loads = RegNext(s0_executing_loads)
  val s1_set_execute     = WireInit(s1_executing_loads)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1233-1235
```scala
          ((l_forward_stq_idx =/= lcam_stq_idx(w)) && forwarded_is_older)) { // If the load forwarded from us, we might be ok
          ldq_order_fail(i) := true.B
          failed_load := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1261-1263
```scala
          when (!(l_executed && (l_succeeded || l_will_succeed))) {
            s1_set_execute(lcam_ldq_idx(w))    := false.B
            when (RegNext(dmem_req_fire(w) && !s0_kills(w)) && !fired_load_agen(w)) {
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1286-1288
```scala
            IsOlderLSU(io.dmem.nack(wi).bits.uop.ldq_idx, lcam_ldq_idx(w), ldq_head)) {
        s1_set_execute(lcam_ldq_idx(w)) := false.B
        when (RegNext(dmem_req_fire(w) && !s0_kills(w)) && !fired_load_agen(w)) {
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1305-1307
```scala
            IsOlderLSU(lcam_ldq_idx(w), wb_ldst_forward_ldq_idx(wi), ldq_head)) {
        ldq_order_fail(wb_ldst_forward_ldq_idx(wi)) := true.B
        failed_load := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1318-1320
```scala
            forwarded_is_older) {
        ldq_order_fail(wb_ldst_forward_ldq_idx(wi)) := true.B
        failed_load := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1378-1380
```scala
      }
      s1_set_execute(lcam_ldq_idx(w)) := false.B
      when (has_older_amo) {
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1387-1389
```scala
  for (i <- 0 until numLdqEntries) {
    when (s1_set_execute(i)) { ldq_executed(i) := true.B }
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1416-1419
```scala
    // Disallow load wakeups 1 cycle after this happens to allow the stores to drain
    when (RegNext(ldst_addr_matches(0) =/= 0.U) && !wb_ldst_forward_valid(0)) {
      block_load_wakeup := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1422-1430
```scala
    val store_blocked_counter = Reg(UInt(4.W))
    when (will_fire_store_commit_fast(0) || will_fire_store_commit_slow(0) || !can_fire_store_commit_slow(0)) {
      store_blocked_counter := 0.U
    } .elsewhen (can_fire_store_commit_slow(0) && !(will_fire_store_commit_slow(0) || will_fire_store_commit_fast(0))) {
      store_blocked_counter := Mux(store_blocked_counter === 15.U, 15.U, store_blocked_counter + 1.U)
    }
    when (store_blocked_counter === 15.U) {
      block_load_wakeup := true.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1542-1544
```scala
    // Handle nacks
    when (io.dmem.nack(w).valid) {
      when (io.dmem.nack(w).bits.is_hella) {
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1545-1549
```scala
        assert(hella_state === h_wait || hella_state === h_dead)
      } .elsewhen (io.dmem.nack(w).bits.uop.uses_ldq) {
        assert(ldq_executed(io.dmem.nack(w).bits.uop.ldq_idx))
        ldq_executed(io.dmem.nack(w).bits.uop.ldq_idx) := false.B
      } .otherwise {
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1720-1722
```scala
  {
    when (ldq_valid(i)) {
      val uop = WireInit(ldq_uop(i))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1724-1728
```scala
      when (IsKilledByBranch(io.core.brupdate, io.core.exception, uop))
      {
        ldq_valid(i)       := false.B
        ldq_addr (i).valid := false.B
      }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1748-1751
```scala
  {
    val commit_store = io.core.commit.valids(w) && io.core.commit.uops(w).uses_stq
    val commit_load  = io.core.commit.valids(w) && io.core.commit.uops(w).uses_ldq
    // val stq_e = WireInit(stq(temp_stq_commit_head))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1759-1761
```scala

    } .elsewhen (commit_load) {
      assert (ldq_valid(temp_ldq_head), "[lsu] trying to commit an un-allocated load entry.")
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1764-1766
```scala

      ldq_valid(temp_ldq_head)                 := false.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1782-1784
```scala

    temp_ldq_head        = Mux(commit_load,
                               WrapIncWCarry(temp_ldq_head, numLdqEntries),
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1787-1789
```scala
  stq_commit_head := temp_stq_commit_head
  ldq_head        := temp_ldq_head
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1791-1800
```scala
  val stq_head_is_fence = stq_uop(stq_head).is_fence
  when (stq_valid(stq_head) && stq_committed(stq_head))
  {

    when (stq_head_is_fence && !io.dmem.ordered) {
      io.dmem.force_order := true.B
      store_needs_order   := true.B
    }
    clear_store := Mux(stq_head_is_fence, io.dmem.ordered, stq_succeeded(stq_head))
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1802-1804
```scala
  when (clear_store)
  {
    stq_valid(stq_head)           := false.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1805-1807
```scala

    stq_head := WrapIncWCarry(stq_head, numStqEntries)
    when (stq_head_is_fence)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1847-1850
```scala
    io.hellacache.req.ready := true.B
    when (io.hellacache.req.fire) {
      hella_req   := io.hellacache.req.bits
      hella_state := h_s1
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1851-1854
```scala
    }
  } .elsewhen (hella_state === h_s1) {
    can_fire_hella_incoming(0) := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1907-1910
```scala
    }
  } .elsewhen (hella_state === h_replay) {
    can_fire_hella_wakeup(0) := true.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1927-1931
```scala

  when (reset.asBool || io.core.exception)
  {
    ldq_head := 0.U
    ldq_tail := 0.U
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1932-1936
```scala

    when (reset.asBool)
    {
      stq_head := 0.U
      stq_tail := 0.U
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1959-1961
```scala
    {
      ldq_valid(i)           := false.B
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1991-1993
```scala
  def _private_helper(idx: UInt): UInt = {
    idx(idx.getWidth-2, 0)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1995-2000
```scala
    val head_base = _private_helper(head)
    val head_overflow = head(head.getWidth - 1)
    val base = AgePriorityEncoder(in, head_base)
    val overflow = Mux(base >= head_base, head_overflow, ~head_overflow)
    Cat(overflow, base)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2062-2064
```scala
  def apply (idx: UInt): UInt = {
    idx(idx.getWidth-2, 0)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2068-2070
```scala
  def apply(idx: UInt): UInt = {
    idx(idx.getWidth-1)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2093-2096
```scala
    Mux1H(Seq(
      (age1_overflow === age2_overflow) -> (age1_age > age2_age),
      (age1_overflow =/= age2_overflow) -> (age1_age < age2_age)
    ))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2107-2109
```scala
    val age2_age      : UInt = GetRealLSQIdx(age2)
    age1_age === age2_age
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2119-2121
```scala
  def apply(age1: UInt, age2: UInt) : Bool = {
    IdxAgeYoungerThan(age1, age2) | IdxAgeEq(age1, age2)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:2144-2146
```scala
    val reg = Reg(chiselTypeOf(x))
    reg := x
    reg
```

### generators/boom/src/main/scala/v4/util/util.scala:60-62
```scala
  def apply(brupdate: BrUpdateInfo, flush: Bool, uop_mask: UInt): Bool = {
    return maskMatch(brupdate.b1.mispredict_mask, uop_mask) || flush
  }
```

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
```

### generators/boom/src/main/scala/v4/util/util.scala:226-228
```scala
    if (isPow2(n)) {
      (value+1.U)(log2Ceil(n), 0)
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

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11-13
```scala
  val size = Wire(UInt(log2Up(log2Up(maxSize)+1).W))
  size := typ
  val dat_padded = dat.pad(maxSize*8)
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:28-30
```scala
    if (i >= log2Up(maxSize)) dat_padded
    else Mux(size === i.U, Fill(1 << (log2Up(maxSize)-i), dat_padded((8 << i)-1,0)), genData(i+1))
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[67] FIRRTL:366439 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:323:33 KIND:connect :: connect clear_store, UInt<1>(0h0)
[70] FIRRTL:366442 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:331:17 KIND:connect :: connect ldq_succeeded, ldq_will_succeed
[160] FIRRTL:366532 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:375:48 KIND:node :: node _dis_ld_val_T = and(io.core.dis_uops[0].valid, io.core.dis_uops[0].bits.uses_ldq)
[161] FIRRTL:366533 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:375:88 KIND:node :: node _dis_ld_val_T_1 = eq(io.core.dis_uops[0].bits.exception, UInt<1>(0h0))
[162] FIRRTL:366534 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:375:85 KIND:node :: node dis_ld_val = and(_dis_ld_val_T, _dis_ld_val_T_1)
[169] FIRRTL:366541 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:381:23 KIND:when :: when dis_ld_val :
[172] FIRRTL:366544 SRC:<no-source-locator> KIND:node :: node _T_1 = bits(ldq_tail, 2, 0)
[173] FIRRTL:366545 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:383:55 KIND:connect :: connect ldq_next_stq_idx[_T_1], stq_tail
[224] FIRRTL:366596 SRC:<no-source-locator> KIND:node :: node _T_28 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[225] FIRRTL:366597 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _ldq_valid_T = and(io.core.brupdate.b1.mispredict_mask, dis_uops[0].bits.br_mask)
[226] FIRRTL:366598 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _ldq_valid_T_1 = neq(_ldq_valid_T, UInt<1>(0h0))
[227] FIRRTL:366599 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _ldq_valid_T_2 = or(_ldq_valid_T_1, io.core.exception)
[228] FIRRTL:366600 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:396:45 KIND:node :: node _ldq_valid_T_3 = eq(_ldq_valid_T_2, UInt<1>(0h0))
[229] FIRRTL:366601 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:396:42 KIND:connect :: connect ldq_valid[_T_28], _ldq_valid_T_3
[237] FIRRTL:366609 SRC:<no-source-locator> KIND:node :: node _T_30 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[238] FIRRTL:366610 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:398:42 KIND:connect :: connect ldq_addr[_T_30].valid, UInt<1>(0h0)
[239] FIRRTL:366611 SRC:<no-source-locator> KIND:node :: node _T_31 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[240] FIRRTL:366612 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:399:42 KIND:connect :: connect ldq_executed[_T_31], UInt<1>(0h0)
[243] FIRRTL:366615 SRC:<no-source-locator> KIND:node :: node _T_33 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[244] FIRRTL:366616 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:401:42 KIND:connect :: connect ldq_order_fail[_T_33], UInt<1>(0h0)
[335] FIRRTL:366707 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[0], UInt<1>(0h0)
[336] FIRRTL:366708 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[1], UInt<1>(0h0)
[337] FIRRTL:366709 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[2], UInt<1>(0h0)
[338] FIRRTL:366710 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[3], UInt<1>(0h0)
[339] FIRRTL:366711 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[4], UInt<1>(0h0)
[340] FIRRTL:366712 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[5], UInt<1>(0h0)
[341] FIRRTL:366713 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[6], UInt<1>(0h0)
[342] FIRRTL:366714 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:44 KIND:connect :: connect _block_load_mask_WIRE[7], UInt<1>(0h0)
[344] FIRRTL:366716 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:481:36 KIND:connect :: connect block_load_mask, _block_load_mask_WIRE
[346] FIRRTL:366718 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:482:35 KIND:connect :: connect p1_block_load_mask, block_load_mask
[348] FIRRTL:366720 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:483:35 KIND:connect :: connect p2_block_load_mask, p1_block_load_mask
[396] FIRRTL:366768 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:491:35 KIND:connect :: connect store_needs_order, UInt<1>(0h0)
[398] FIRRTL:366770 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect ldq_incoming_idx[0], io.core.agen[0].bits.uop.ldq_idx
[461] FIRRTL:366833 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block = or(block_load_mask[0], p1_block_load_mask[0])
[462] FIRRTL:366834 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T = eq(ldq_executed[0], UInt<1>(0h0))
[463] FIRRTL:366835 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_1 = and(ldq_addr[0].valid, _ldq_wakeup_idx_T)
[464] FIRRTL:366836 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_2 = eq(ldq_succeeded[0], UInt<1>(0h0))
[465] FIRRTL:366837 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_3 = and(_ldq_wakeup_idx_T_1, _ldq_wakeup_idx_T_2)
[466] FIRRTL:366838 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_4 = eq(ldq_addr_is_virtual[0], UInt<1>(0h0))
[467] FIRRTL:366839 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_5 = and(_ldq_wakeup_idx_T_3, _ldq_wakeup_idx_T_4)
[468] FIRRTL:366840 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_6 = eq(ldq_wakeup_idx_block, UInt<1>(0h0))
[469] FIRRTL:366841 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_7 = and(_ldq_wakeup_idx_T_5, _ldq_wakeup_idx_T_6)
[470] FIRRTL:366842 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_1 = or(block_load_mask[1], p1_block_load_mask[1])
[471] FIRRTL:366843 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_8 = eq(ldq_executed[1], UInt<1>(0h0))
[472] FIRRTL:366844 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_9 = and(ldq_addr[1].valid, _ldq_wakeup_idx_T_8)
[473] FIRRTL:366845 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_10 = eq(ldq_succeeded[1], UInt<1>(0h0))
[474] FIRRTL:366846 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_11 = and(_ldq_wakeup_idx_T_9, _ldq_wakeup_idx_T_10)
[475] FIRRTL:366847 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_12 = eq(ldq_addr_is_virtual[1], UInt<1>(0h0))
[476] FIRRTL:366848 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_13 = and(_ldq_wakeup_idx_T_11, _ldq_wakeup_idx_T_12)
[477] FIRRTL:366849 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_14 = eq(ldq_wakeup_idx_block_1, UInt<1>(0h0))
[478] FIRRTL:366850 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_15 = and(_ldq_wakeup_idx_T_13, _ldq_wakeup_idx_T_14)
[479] FIRRTL:366851 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_2 = or(block_load_mask[2], p1_block_load_mask[2])
[480] FIRRTL:366852 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_16 = eq(ldq_executed[2], UInt<1>(0h0))
[481] FIRRTL:366853 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_17 = and(ldq_addr[2].valid, _ldq_wakeup_idx_T_16)
[482] FIRRTL:366854 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_18 = eq(ldq_succeeded[2], UInt<1>(0h0))
[483] FIRRTL:366855 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_19 = and(_ldq_wakeup_idx_T_17, _ldq_wakeup_idx_T_18)
[484] FIRRTL:366856 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_20 = eq(ldq_addr_is_virtual[2], UInt<1>(0h0))
[485] FIRRTL:366857 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_21 = and(_ldq_wakeup_idx_T_19, _ldq_wakeup_idx_T_20)
[486] FIRRTL:366858 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_22 = eq(ldq_wakeup_idx_block_2, UInt<1>(0h0))
[487] FIRRTL:366859 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_23 = and(_ldq_wakeup_idx_T_21, _ldq_wakeup_idx_T_22)
[488] FIRRTL:366860 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_3 = or(block_load_mask[3], p1_block_load_mask[3])
[489] FIRRTL:366861 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_24 = eq(ldq_executed[3], UInt<1>(0h0))
[490] FIRRTL:366862 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_25 = and(ldq_addr[3].valid, _ldq_wakeup_idx_T_24)
[491] FIRRTL:366863 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_26 = eq(ldq_succeeded[3], UInt<1>(0h0))
[492] FIRRTL:366864 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_27 = and(_ldq_wakeup_idx_T_25, _ldq_wakeup_idx_T_26)
[493] FIRRTL:366865 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_28 = eq(ldq_addr_is_virtual[3], UInt<1>(0h0))
[494] FIRRTL:366866 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_29 = and(_ldq_wakeup_idx_T_27, _ldq_wakeup_idx_T_28)
[495] FIRRTL:366867 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_30 = eq(ldq_wakeup_idx_block_3, UInt<1>(0h0))
[496] FIRRTL:366868 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_31 = and(_ldq_wakeup_idx_T_29, _ldq_wakeup_idx_T_30)
[497] FIRRTL:366869 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_4 = or(block_load_mask[4], p1_block_load_mask[4])
[498] FIRRTL:366870 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_32 = eq(ldq_executed[4], UInt<1>(0h0))
[499] FIRRTL:366871 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_33 = and(ldq_addr[4].valid, _ldq_wakeup_idx_T_32)
[500] FIRRTL:366872 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_34 = eq(ldq_succeeded[4], UInt<1>(0h0))
[501] FIRRTL:366873 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_35 = and(_ldq_wakeup_idx_T_33, _ldq_wakeup_idx_T_34)
[502] FIRRTL:366874 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_36 = eq(ldq_addr_is_virtual[4], UInt<1>(0h0))
[503] FIRRTL:366875 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_37 = and(_ldq_wakeup_idx_T_35, _ldq_wakeup_idx_T_36)
[504] FIRRTL:366876 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_38 = eq(ldq_wakeup_idx_block_4, UInt<1>(0h0))
[505] FIRRTL:366877 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_39 = and(_ldq_wakeup_idx_T_37, _ldq_wakeup_idx_T_38)
[506] FIRRTL:366878 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_5 = or(block_load_mask[5], p1_block_load_mask[5])
[507] FIRRTL:366879 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_40 = eq(ldq_executed[5], UInt<1>(0h0))
[508] FIRRTL:366880 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_41 = and(ldq_addr[5].valid, _ldq_wakeup_idx_T_40)
[509] FIRRTL:366881 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_42 = eq(ldq_succeeded[5], UInt<1>(0h0))
[510] FIRRTL:366882 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_43 = and(_ldq_wakeup_idx_T_41, _ldq_wakeup_idx_T_42)
[511] FIRRTL:366883 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_44 = eq(ldq_addr_is_virtual[5], UInt<1>(0h0))
[512] FIRRTL:366884 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_45 = and(_ldq_wakeup_idx_T_43, _ldq_wakeup_idx_T_44)
[513] FIRRTL:366885 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_46 = eq(ldq_wakeup_idx_block_5, UInt<1>(0h0))
[514] FIRRTL:366886 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_47 = and(_ldq_wakeup_idx_T_45, _ldq_wakeup_idx_T_46)
[515] FIRRTL:366887 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_6 = or(block_load_mask[6], p1_block_load_mask[6])
[516] FIRRTL:366888 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_48 = eq(ldq_executed[6], UInt<1>(0h0))
[517] FIRRTL:366889 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_49 = and(ldq_addr[6].valid, _ldq_wakeup_idx_T_48)
[518] FIRRTL:366890 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_50 = eq(ldq_succeeded[6], UInt<1>(0h0))
[519] FIRRTL:366891 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_51 = and(_ldq_wakeup_idx_T_49, _ldq_wakeup_idx_T_50)
[520] FIRRTL:366892 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_52 = eq(ldq_addr_is_virtual[6], UInt<1>(0h0))
[521] FIRRTL:366893 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_53 = and(_ldq_wakeup_idx_T_51, _ldq_wakeup_idx_T_52)
[522] FIRRTL:366894 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_54 = eq(ldq_wakeup_idx_block_6, UInt<1>(0h0))
[523] FIRRTL:366895 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_55 = and(_ldq_wakeup_idx_T_53, _ldq_wakeup_idx_T_54)
[524] FIRRTL:366896 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:500:36 KIND:node :: node ldq_wakeup_idx_block_7 = or(block_load_mask[7], p1_block_load_mask[7])
[525] FIRRTL:366897 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:26 KIND:node :: node _ldq_wakeup_idx_T_56 = eq(ldq_executed[7], UInt<1>(0h0))
[526] FIRRTL:366898 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:23 KIND:node :: node _ldq_wakeup_idx_T_57 = and(ldq_addr[7].valid, _ldq_wakeup_idx_T_56)
[527] FIRRTL:366899 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:46 KIND:node :: node _ldq_wakeup_idx_T_58 = eq(ldq_succeeded[7], UInt<1>(0h0))
[528] FIRRTL:366900 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:43 KIND:node :: node _ldq_wakeup_idx_T_59 = and(_ldq_wakeup_idx_T_57, _ldq_wakeup_idx_T_58)
[529] FIRRTL:366901 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:67 KIND:node :: node _ldq_wakeup_idx_T_60 = eq(ldq_addr_is_virtual[7], UInt<1>(0h0))
[530] FIRRTL:366902 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:64 KIND:node :: node _ldq_wakeup_idx_T_61 = and(_ldq_wakeup_idx_T_59, _ldq_wakeup_idx_T_60)
[531] FIRRTL:366903 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:94 KIND:node :: node _ldq_wakeup_idx_T_62 = eq(ldq_wakeup_idx_block_7, UInt<1>(0h0))
[532] FIRRTL:366904 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:501:91 KIND:node :: node _ldq_wakeup_idx_T_63 = and(_ldq_wakeup_idx_T_61, _ldq_wakeup_idx_T_62)
[533] FIRRTL:366905 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1992:8 KIND:node :: node ldq_wakeup_idx_head_base = bits(ldq_head, 2, 0)
[534] FIRRTL:366906 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1996:29 KIND:node :: node ldq_wakeup_idx_head_overflow = bits(ldq_head, 3, 3)
[535] FIRRTL:366907 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T = geq(UInt<1>(0h0), ldq_wakeup_idx_head_base)
[536] FIRRTL:366908 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_0 = and(_ldq_wakeup_idx_T_7, _ldq_wakeup_idx_base_temp_vec_T)
[537] FIRRTL:366909 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_1 = geq(UInt<1>(0h1), ldq_wakeup_idx_head_base)
[538] FIRRTL:366910 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_1 = and(_ldq_wakeup_idx_T_15, _ldq_wakeup_idx_base_temp_vec_T_1)
[539] FIRRTL:366911 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_2 = geq(UInt<2>(0h2), ldq_wakeup_idx_head_base)
[540] FIRRTL:366912 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_2 = and(_ldq_wakeup_idx_T_23, _ldq_wakeup_idx_base_temp_vec_T_2)
[541] FIRRTL:366913 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_3 = geq(UInt<2>(0h3), ldq_wakeup_idx_head_base)
[542] FIRRTL:366914 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_3 = and(_ldq_wakeup_idx_T_31, _ldq_wakeup_idx_base_temp_vec_T_3)
[543] FIRRTL:366915 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_4 = geq(UInt<3>(0h4), ldq_wakeup_idx_head_base)
[544] FIRRTL:366916 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_4 = and(_ldq_wakeup_idx_T_39, _ldq_wakeup_idx_base_temp_vec_T_4)
[545] FIRRTL:366917 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_5 = geq(UInt<3>(0h5), ldq_wakeup_idx_head_base)
[546] FIRRTL:366918 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_5 = and(_ldq_wakeup_idx_T_47, _ldq_wakeup_idx_base_temp_vec_T_5)
[547] FIRRTL:366919 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_6 = geq(UInt<3>(0h6), ldq_wakeup_idx_head_base)
[548] FIRRTL:366920 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_6 = and(_ldq_wakeup_idx_T_55, _ldq_wakeup_idx_base_temp_vec_T_6)
[549] FIRRTL:366921 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _ldq_wakeup_idx_base_temp_vec_T_7 = geq(UInt<3>(0h7), ldq_wakeup_idx_head_base)
[550] FIRRTL:366922 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node ldq_wakeup_idx_base_temp_vec_7 = and(_ldq_wakeup_idx_T_63, _ldq_wakeup_idx_base_temp_vec_T_7)
[551] FIRRTL:366923 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T = mux(_ldq_wakeup_idx_T_55, UInt<4>(0he), UInt<4>(0hf))
[552] FIRRTL:366924 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_1 = mux(_ldq_wakeup_idx_T_47, UInt<4>(0hd), _ldq_wakeup_idx_base_idx_T)
[553] FIRRTL:366925 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_2 = mux(_ldq_wakeup_idx_T_39, UInt<4>(0hc), _ldq_wakeup_idx_base_idx_T_1)
[554] FIRRTL:366926 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_3 = mux(_ldq_wakeup_idx_T_31, UInt<4>(0hb), _ldq_wakeup_idx_base_idx_T_2)
[555] FIRRTL:366927 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_4 = mux(_ldq_wakeup_idx_T_23, UInt<4>(0ha), _ldq_wakeup_idx_base_idx_T_3)
[556] FIRRTL:366928 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_5 = mux(_ldq_wakeup_idx_T_15, UInt<4>(0h9), _ldq_wakeup_idx_base_idx_T_4)
[557] FIRRTL:366929 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_6 = mux(_ldq_wakeup_idx_T_7, UInt<4>(0h8), _ldq_wakeup_idx_base_idx_T_5)
[558] FIRRTL:366930 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_7 = mux(ldq_wakeup_idx_base_temp_vec_7, UInt<3>(0h7), _ldq_wakeup_idx_base_idx_T_6)
[559] FIRRTL:366931 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_8 = mux(ldq_wakeup_idx_base_temp_vec_6, UInt<3>(0h6), _ldq_wakeup_idx_base_idx_T_7)
[560] FIRRTL:366932 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_9 = mux(ldq_wakeup_idx_base_temp_vec_5, UInt<3>(0h5), _ldq_wakeup_idx_base_idx_T_8)
[561] FIRRTL:366933 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_10 = mux(ldq_wakeup_idx_base_temp_vec_4, UInt<3>(0h4), _ldq_wakeup_idx_base_idx_T_9)
[562] FIRRTL:366934 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_11 = mux(ldq_wakeup_idx_base_temp_vec_3, UInt<2>(0h3), _ldq_wakeup_idx_base_idx_T_10)
[563] FIRRTL:366935 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_12 = mux(ldq_wakeup_idx_base_temp_vec_2, UInt<2>(0h2), _ldq_wakeup_idx_base_idx_T_11)
[564] FIRRTL:366936 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _ldq_wakeup_idx_base_idx_T_13 = mux(ldq_wakeup_idx_base_temp_vec_1, UInt<1>(0h1), _ldq_wakeup_idx_base_idx_T_12)
[565] FIRRTL:366937 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node ldq_wakeup_idx_base_idx = mux(ldq_wakeup_idx_base_temp_vec_0, UInt<1>(0h0), _ldq_wakeup_idx_base_idx_T_13)
[566] FIRRTL:366938 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node ldq_wakeup_idx_base = bits(ldq_wakeup_idx_base_idx, 2, 0)
[567] FIRRTL:366939 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:29 KIND:node :: node _ldq_wakeup_idx_overflow_T = geq(ldq_wakeup_idx_base, ldq_wakeup_idx_head_base)
[568] FIRRTL:366940 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:58 KIND:node :: node _ldq_wakeup_idx_overflow_T_1 = not(ldq_wakeup_idx_head_overflow)
[569] FIRRTL:366941 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:23 KIND:node :: node ldq_wakeup_idx_overflow = mux(_ldq_wakeup_idx_overflow_T, ldq_wakeup_idx_head_overflow, _ldq_wakeup_idx_overflow_T_1)
[570] FIRRTL:366942 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1999:8 KIND:node :: node _ldq_wakeup_idx_T_64 = cat(ldq_wakeup_idx_overflow, ldq_wakeup_idx_base)
[572] FIRRTL:366944 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2145:9 KIND:connect :: connect ldq_wakeup_idx, _ldq_wakeup_idx_T_64
[574] FIRRTL:366946 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_valid_T = bits(ldq_wakeup_idx, 2, 0)
[575] FIRRTL:366947 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:238:32 KIND:connect :: connect ldq_wakeup_e_e.valid, ldq_valid[_ldq_wakeup_e_e_valid_T]
[576] FIRRTL:366948 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_uop_T = bits(ldq_wakeup_idx, 2, 0)
[578] FIRRTL:366950 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_addr_T = bits(ldq_wakeup_idx, 2, 0)
[579] FIRRTL:366951 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:240:32 KIND:connect :: connect ldq_wakeup_e_e.bits.addr, ldq_addr[_ldq_wakeup_e_e_bits_addr_T]
[580] FIRRTL:366952 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_addr_is_virtual_T = bits(ldq_wakeup_idx, 2, 0)
[581] FIRRTL:366953 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:241:32 KIND:connect :: connect ldq_wakeup_e_e.bits.addr_is_virtual, ldq_addr_is_virtual[_ldq_wakeup_e_e_bits_addr_is_virtual_T]
[582] FIRRTL:366954 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_addr_is_uncacheable_T = bits(ldq_wakeup_idx, 2, 0)
[583] FIRRTL:366955 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:242:32 KIND:connect :: connect ldq_wakeup_e_e.bits.addr_is_uncacheable, ldq_addr_is_uncacheable[_ldq_wakeup_e_e_bits_addr_is_uncacheable_T]
[584] FIRRTL:366956 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_executed_T = bits(ldq_wakeup_idx, 2, 0)
[585] FIRRTL:366957 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:243:32 KIND:connect :: connect ldq_wakeup_e_e.bits.executed, ldq_executed[_ldq_wakeup_e_e_bits_executed_T]
[586] FIRRTL:366958 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_succeeded_T = bits(ldq_wakeup_idx, 2, 0)
[587] FIRRTL:366959 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:244:32 KIND:connect :: connect ldq_wakeup_e_e.bits.succeeded, ldq_succeeded[_ldq_wakeup_e_e_bits_succeeded_T]
[588] FIRRTL:366960 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_order_fail_T = bits(ldq_wakeup_idx, 2, 0)
[589] FIRRTL:366961 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:245:32 KIND:connect :: connect ldq_wakeup_e_e.bits.order_fail, ldq_order_fail[_ldq_wakeup_e_e_bits_order_fail_T]
[592] FIRRTL:366964 SRC:<no-source-locator> KIND:node :: node _ldq_wakeup_e_e_bits_next_stq_idx_T = bits(ldq_wakeup_idx, 2, 0)
[593] FIRRTL:366965 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:247:32 KIND:connect :: connect ldq_wakeup_e_e.bits.next_stq_idx, ldq_next_stq_idx[_ldq_wakeup_e_e_bits_next_stq_idx_T]
[603] FIRRTL:366975 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:503:32 KIND:connect :: connect ldq_wakeup_e, ldq_wakeup_e_e
[677] FIRRTL:367049 SRC:<no-source-locator> KIND:node :: node _ldq_enq_retry_e_e_valid_T = bits(ldq_enq_retry_idx, 2, 0)
[678] FIRRTL:367050 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:238:32 KIND:connect :: connect ldq_enq_retry_e_e.valid, ldq_valid[_ldq_enq_retry_e_e_valid_T]
[681] FIRRTL:367053 SRC:<no-source-locator> KIND:node :: node _ldq_enq_retry_e_e_bits_addr_T = bits(ldq_enq_retry_idx, 2, 0)
[682] FIRRTL:367054 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:240:32 KIND:connect :: connect ldq_enq_retry_e_e.bits.addr, ldq_addr[_ldq_enq_retry_e_e_bits_addr_T]
[683] FIRRTL:367055 SRC:<no-source-locator> KIND:node :: node _ldq_enq_retry_e_e_bits_addr_is_virtual_T = bits(ldq_enq_retry_idx, 2, 0)
[684] FIRRTL:367056 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:241:32 KIND:connect :: connect ldq_enq_retry_e_e.bits.addr_is_virtual, ldq_addr_is_virtual[_ldq_enq_retry_e_e_bits_addr_is_virtual_T]
[706] FIRRTL:367078 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:511:33 KIND:connect :: connect ldq_enq_retry_e, ldq_enq_retry_e_e
[780] FIRRTL:367152 SRC:<no-source-locator> KIND:node :: node _stq_enq_retry_e_e_valid_T = bits(stq_enq_retry_idx, 2, 0)
[781] FIRRTL:367153 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:268:32 KIND:connect :: connect stq_enq_retry_e_e.valid, stq_valid[_stq_enq_retry_e_e_valid_T]
[784] FIRRTL:367156 SRC:<no-source-locator> KIND:node :: node _stq_enq_retry_e_e_bits_addr_T = bits(stq_enq_retry_idx, 2, 0)
[785] FIRRTL:367157 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:270:32 KIND:connect :: connect stq_enq_retry_e_e.bits.addr, stq_addr[_stq_enq_retry_e_e_bits_addr_T]
[786] FIRRTL:367158 SRC:<no-source-locator> KIND:node :: node _stq_enq_retry_e_e_bits_addr_is_virtual_T = bits(stq_enq_retry_idx, 2, 0)
[787] FIRRTL:367159 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:271:32 KIND:connect :: connect stq_enq_retry_e_e.bits.addr_is_virtual, stq_addr_is_virtual[_stq_enq_retry_e_e_bits_addr_is_virtual_T]
[803] FIRRTL:367175 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:517:35 KIND:connect :: connect stq_enq_retry_e, stq_enq_retry_e_e
[804] FIRRTL:367176 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:519:81 KIND:node :: node _can_enq_load_retry_T = and(ldq_enq_retry_e.valid, ldq_enq_retry_e.bits.addr.valid)
[805] FIRRTL:367177 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:520:81 KIND:node :: node can_enq_load_retry = and(_can_enq_load_retry_T, ldq_enq_retry_e.bits.addr_is_virtual)
[806] FIRRTL:367178 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:522:81 KIND:node :: node _can_enq_store_retry_T = and(stq_enq_retry_e.valid, stq_enq_retry_e.bits.addr.valid)
[807] FIRRTL:367179 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:523:81 KIND:node :: node can_enq_store_retry = and(_can_enq_store_retry_T, stq_enq_retry_e.bits.addr_is_virtual)
[931] FIRRTL:367303 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:530:55 KIND:node :: node _retry_queue_io_enq_valid_T = or(can_enq_store_retry, can_enq_load_retry)
[932] FIRRTL:367304 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:530:32 KIND:connect :: connect retry_queue.io.enq.valid, _retry_queue_io_enq_valid_T
[1165] FIRRTL:367537 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_71 = and(retry_queue.io.enq.ready, retry_queue.io.enq.valid)
[1166] FIRRTL:367538 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:539:29 KIND:node :: node _T_72 = and(can_enq_store_retry, _T_71)
[1170] FIRRTL:367542 SRC:<no-source-locator> KIND:else :: else :
[1171] FIRRTL:367543 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_74 = and(retry_queue.io.enq.ready, retry_queue.io.enq.valid)
[1172] FIRRTL:367544 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:541:35 KIND:node :: node _T_75 = and(can_enq_load_retry, _T_74)
[1173] FIRRTL:367545 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:541:63 KIND:when :: when _T_75 :
[1174] FIRRTL:367546 SRC:<no-source-locator> KIND:node :: node _T_76 = bits(ldq_enq_retry_idx, 2, 0)
[1175] FIRRTL:367547 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:542:39 KIND:connect :: connect ldq_addr[_T_76].valid, UInt<1>(0h0)
[1365] FIRRTL:367737 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:597:79 KIND:node :: node _can_fire_load_retry_T = and(retry_queue.io.deq.valid, retry_queue.io.deq.bits.uop.uses_ldq)
[1367] FIRRTL:367739 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:599:41 KIND:connect :: connect can_fire_load_retry_REG, store_needs_order
[1368] FIRRTL:367740 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:599:33 KIND:node :: node _can_fire_load_retry_T_1 = eq(can_fire_load_retry_REG, UInt<1>(0h0))
[1369] FIRRTL:367741 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:598:79 KIND:node :: node _can_fire_load_retry_T_2 = and(_can_fire_load_retry_T, _can_fire_load_retry_T_1)
[1370] FIRRTL:367742 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:599:79 KIND:node :: node _can_fire_load_retry_T_3 = and(_can_fire_load_retry_T_2, UInt<1>(0h1))
[1372] FIRRTL:367744 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect can_fire_load_retry[0], _can_fire_load_retry_T_3
[1373] FIRRTL:367745 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:604:79 KIND:node :: node _can_fire_store_retry_T = and(retry_queue.io.deq.valid, retry_queue.io.deq.bits.uop.uses_stq)
[1374] FIRRTL:367746 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:605:79 KIND:node :: node _can_fire_store_retry_T_1 = and(_can_fire_store_retry_T, UInt<1>(0h1))
[1376] FIRRTL:367748 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect can_fire_store_retry[0], _can_fire_store_retry_T_1
[1386] FIRRTL:367758 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:617:35 KIND:connect :: connect block_load_wakeup, UInt<1>(0h0)
[1387] FIRRTL:367759 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:619:88 KIND:node :: node _can_fire_load_wakeup_T = and(ldq_wakeup_e.valid, ldq_wakeup_e.bits.addr.valid)
[1388] FIRRTL:367760 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:621:31 KIND:node :: node _can_fire_load_wakeup_T_1 = eq(ldq_wakeup_e.bits.succeeded, UInt<1>(0h0))
[1389] FIRRTL:367761 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:620:88 KIND:node :: node _can_fire_load_wakeup_T_2 = and(_can_fire_load_wakeup_T, _can_fire_load_wakeup_T_1)
[1390] FIRRTL:367762 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:622:31 KIND:node :: node _can_fire_load_wakeup_T_3 = eq(ldq_wakeup_e.bits.addr_is_virtual, UInt<1>(0h0))
[1391] FIRRTL:367763 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:621:88 KIND:node :: node _can_fire_load_wakeup_T_4 = and(_can_fire_load_wakeup_T_2, _can_fire_load_wakeup_T_3)
[1392] FIRRTL:367764 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:623:31 KIND:node :: node _can_fire_load_wakeup_T_5 = eq(ldq_wakeup_e.bits.executed, UInt<1>(0h0))
[1393] FIRRTL:367765 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:622:88 KIND:node :: node _can_fire_load_wakeup_T_6 = and(_can_fire_load_wakeup_T_4, _can_fire_load_wakeup_T_5)
[1394] FIRRTL:367766 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:624:31 KIND:node :: node _can_fire_load_wakeup_T_7 = eq(ldq_wakeup_e.bits.order_fail, UInt<1>(0h0))
[1395] FIRRTL:367767 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:623:88 KIND:node :: node _can_fire_load_wakeup_T_8 = and(_can_fire_load_wakeup_T_6, _can_fire_load_wakeup_T_7)
[1396] FIRRTL:367768 SRC:<no-source-locator> KIND:node :: node _can_fire_load_wakeup_T_9 = bits(ldq_wakeup_idx, 2, 0)
[1397] FIRRTL:367769 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:625:31 KIND:node :: node _can_fire_load_wakeup_T_10 = eq(p1_block_load_mask[_can_fire_load_wakeup_T_9], UInt<1>(0h0))
[1398] FIRRTL:367770 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:624:88 KIND:node :: node _can_fire_load_wakeup_T_11 = and(_can_fire_load_wakeup_T_8, _can_fire_load_wakeup_T_10)
[1399] FIRRTL:367771 SRC:<no-source-locator> KIND:node :: node _can_fire_load_wakeup_T_12 = bits(ldq_wakeup_idx, 2, 0)
[1400] FIRRTL:367772 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:626:31 KIND:node :: node _can_fire_load_wakeup_T_13 = eq(p2_block_load_mask[_can_fire_load_wakeup_T_12], UInt<1>(0h0))
[1401] FIRRTL:367773 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:625:88 KIND:node :: node _can_fire_load_wakeup_T_14 = and(_can_fire_load_wakeup_T_11, _can_fire_load_wakeup_T_13)
[1403] FIRRTL:367775 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:627:39 KIND:connect :: connect can_fire_load_wakeup_REG, store_needs_order
[1404] FIRRTL:367776 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:627:31 KIND:node :: node _can_fire_load_wakeup_T_15 = eq(can_fire_load_wakeup_REG, UInt<1>(0h0))
[1405] FIRRTL:367777 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:626:88 KIND:node :: node _can_fire_load_wakeup_T_16 = and(_can_fire_load_wakeup_T_14, _can_fire_load_wakeup_T_15)
[1406] FIRRTL:367778 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:628:31 KIND:node :: node _can_fire_load_wakeup_T_17 = eq(block_load_wakeup, UInt<1>(0h0))
[1407] FIRRTL:367779 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:627:88 KIND:node :: node _can_fire_load_wakeup_T_18 = and(_can_fire_load_wakeup_T_16, _can_fire_load_wakeup_T_17)
[1408] FIRRTL:367780 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:628:88 KIND:node :: node _can_fire_load_wakeup_T_19 = and(_can_fire_load_wakeup_T_18, UInt<1>(0h1))
[1409] FIRRTL:367781 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:630:32 KIND:node :: node _can_fire_load_wakeup_T_20 = eq(ldq_wakeup_e.bits.addr_is_uncacheable, UInt<1>(0h0))
[1410] FIRRTL:367782 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:631:84 KIND:node :: node _can_fire_load_wakeup_T_21 = eq(ldq_head, ldq_wakeup_idx)
[1411] FIRRTL:367783 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:630:107 KIND:node :: node _can_fire_load_wakeup_T_22 = and(io.core.commit_load_at_rob_head, _can_fire_load_wakeup_T_21)
[1412] FIRRTL:367784 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node can_fire_load_wakeup_age1_overflow = bits(stq_head, 3, 3)
[1413] FIRRTL:367785 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2069:8 KIND:node :: node can_fire_load_wakeup_age2_overflow = bits(ldq_wakeup_e.bits.next_stq_idx, 3, 3)
[1414] FIRRTL:367786 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node can_fire_load_wakeup_age1_age = bits(stq_head, 2, 0)
[1415] FIRRTL:367787 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node can_fire_load_wakeup_age2_age = bits(ldq_wakeup_e.bits.next_stq_idx, 2, 0)
[1416] FIRRTL:367788 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:22 KIND:node :: node _can_fire_load_wakeup_T_23 = eq(can_fire_load_wakeup_age1_overflow, can_fire_load_wakeup_age2_overflow)
[1417] FIRRTL:367789 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2094:54 KIND:node :: node _can_fire_load_wakeup_T_24 = gt(can_fire_load_wakeup_age1_age, can_fire_load_wakeup_age2_age)
[1418] FIRRTL:367790 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:22 KIND:node :: node _can_fire_load_wakeup_T_25 = neq(can_fire_load_wakeup_age1_overflow, can_fire_load_wakeup_age2_overflow)
[1419] FIRRTL:367791 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2095:54 KIND:node :: node _can_fire_load_wakeup_T_26 = lt(can_fire_load_wakeup_age1_age, can_fire_load_wakeup_age2_age)
[1420] FIRRTL:367792 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _can_fire_load_wakeup_T_27 = mux(_can_fire_load_wakeup_T_23, _can_fire_load_wakeup_T_24, UInt<1>(0h0))
[1421] FIRRTL:367793 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _can_fire_load_wakeup_T_28 = mux(_can_fire_load_wakeup_T_25, _can_fire_load_wakeup_T_26, UInt<1>(0h0))
[1422] FIRRTL:367794 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _can_fire_load_wakeup_T_29 = or(_can_fire_load_wakeup_T_27, _can_fire_load_wakeup_T_28)
[1424] FIRRTL:367796 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _can_fire_load_wakeup_WIRE, _can_fire_load_wakeup_T_29
[1427] FIRRTL:367799 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node can_fire_load_wakeup_age1_age_1 = bits(stq_head, 2, 0)
[1428] FIRRTL:367800 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2063:8 KIND:node :: node can_fire_load_wakeup_age2_age_1 = bits(ldq_wakeup_e.bits.next_stq_idx, 2, 0)
[1429] FIRRTL:367801 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2108:14 KIND:node :: node _can_fire_load_wakeup_T_30 = eq(can_fire_load_wakeup_age1_age_1, can_fire_load_wakeup_age2_age_1)
[1430] FIRRTL:367802 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2120:35 KIND:node :: node _can_fire_load_wakeup_T_31 = or(_can_fire_load_wakeup_WIRE, _can_fire_load_wakeup_T_30)
[1431] FIRRTL:367803 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:631:103 KIND:node :: node _can_fire_load_wakeup_T_32 = and(_can_fire_load_wakeup_T_22, _can_fire_load_wakeup_T_31)
[1432] FIRRTL:367804 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:630:71 KIND:node :: node _can_fire_load_wakeup_T_33 = or(_can_fire_load_wakeup_T_20, _can_fire_load_wakeup_T_32)
[1433] FIRRTL:367805 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:629:88 KIND:node :: node _can_fire_load_wakeup_T_34 = and(_can_fire_load_wakeup_T_19, _can_fire_load_wakeup_T_33)
[1435] FIRRTL:367807 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect can_fire_load_wakeup[0], _can_fire_load_wakeup_T_34
[1437] FIRRTL:367809 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _can_fire_hella_incoming_WIRE[0], UInt<1>(0h0)
[1439] FIRRTL:367811 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:636:42 KIND:connect :: connect can_fire_hella_incoming, _can_fire_hella_incoming_WIRE
[1441] FIRRTL:367813 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect _can_fire_hella_wakeup_WIRE[0], UInt<1>(0h0)
[1443] FIRRTL:367815 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:639:42 KIND:connect :: connect can_fire_hella_wakeup, _can_fire_hella_wakeup_WIRE
[1466] FIRRTL:367838 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:668:36 KIND:connect :: connect will_fire_sfence[0], will_fire_sfence_0_will_fire
[1488] FIRRTL:367860 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:669:36 KIND:connect :: connect will_fire_store_commit_fast[0], will_fire_store_commit_fast_0_will_fire
[1510] FIRRTL:367882 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:670:36 KIND:connect :: connect will_fire_load_agen_exec[0], will_fire_load_agen_exec_0_will_fire
[1532] FIRRTL:367904 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:671:36 KIND:connect :: connect will_fire_load_agen[0], will_fire_load_agen_0_will_fire
[1554] FIRRTL:367926 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:672:36 KIND:connect :: connect will_fire_store_agen[0], will_fire_store_agen_0_will_fire
[1567] FIRRTL:367939 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_release_0_T = and(will_fire_release_0_will_fire, UInt<1>(0h0))
[1568] FIRRTL:367940 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_release_0_T_1 = eq(_will_fire_release_0_T, UInt<1>(0h0))
[1569] FIRRTL:367941 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_release_0_T_2 = and(_will_fire_store_agen_0_T_2, _will_fire_release_0_T_1)
[1570] FIRRTL:367942 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_release_0_T_3 = and(will_fire_release_0_will_fire, UInt<1>(0h1))
[1571] FIRRTL:367943 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_release_0_T_4 = eq(_will_fire_release_0_T_3, UInt<1>(0h0))
[1572] FIRRTL:367944 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_release_0_T_5 = and(_will_fire_store_agen_0_T_5, _will_fire_release_0_T_4)
[1573] FIRRTL:367945 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_release_0_T_6 = and(will_fire_release_0_will_fire, UInt<1>(0h0))
[1574] FIRRTL:367946 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_release_0_T_7 = eq(_will_fire_release_0_T_6, UInt<1>(0h0))
[1575] FIRRTL:367947 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_release_0_T_8 = and(_will_fire_store_agen_0_T_8, _will_fire_release_0_T_7)
[1577] FIRRTL:367949 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T = eq(_will_fire_release_0_T_2, UInt<1>(0h0))
[1578] FIRRTL:367950 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_1 = and(UInt<1>(0h1), _will_fire_hella_incoming_0_will_fire_T)
[1579] FIRRTL:367951 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_2 = eq(_will_fire_hella_incoming_0_will_fire_T_1, UInt<1>(0h0))
[1580] FIRRTL:367952 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_3 = and(can_fire_hella_incoming[0], _will_fire_hella_incoming_0_will_fire_T_2)
[1581] FIRRTL:367953 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_4 = eq(_will_fire_release_0_T_5, UInt<1>(0h0))
[1582] FIRRTL:367954 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_5 = and(UInt<1>(0h0), _will_fire_hella_incoming_0_will_fire_T_4)
[1583] FIRRTL:367955 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_6 = eq(_will_fire_hella_incoming_0_will_fire_T_5, UInt<1>(0h0))
[1584] FIRRTL:367956 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_7 = and(_will_fire_hella_incoming_0_will_fire_T_3, _will_fire_hella_incoming_0_will_fire_T_6)
[1585] FIRRTL:367957 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_8 = eq(_will_fire_release_0_T_8, UInt<1>(0h0))
[1586] FIRRTL:367958 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_9 = and(UInt<1>(0h1), _will_fire_hella_incoming_0_will_fire_T_8)
[1587] FIRRTL:367959 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_hella_incoming_0_will_fire_T_10 = eq(_will_fire_hella_incoming_0_will_fire_T_9, UInt<1>(0h0))
[1588] FIRRTL:367960 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_hella_incoming_0_will_fire = and(_will_fire_hella_incoming_0_will_fire_T_7, _will_fire_hella_incoming_0_will_fire_T_10)
[1589] FIRRTL:367961 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_hella_incoming_0_T = and(will_fire_hella_incoming_0_will_fire, UInt<1>(0h1))
[1590] FIRRTL:367962 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_hella_incoming_0_T_1 = eq(_will_fire_hella_incoming_0_T, UInt<1>(0h0))
[1591] FIRRTL:367963 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_hella_incoming_0_T_2 = and(_will_fire_release_0_T_2, _will_fire_hella_incoming_0_T_1)
[1592] FIRRTL:367964 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_hella_incoming_0_T_3 = and(will_fire_hella_incoming_0_will_fire, UInt<1>(0h0))
[1593] FIRRTL:367965 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_hella_incoming_0_T_4 = eq(_will_fire_hella_incoming_0_T_3, UInt<1>(0h0))
[1594] FIRRTL:367966 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_hella_incoming_0_T_5 = and(_will_fire_release_0_T_5, _will_fire_hella_incoming_0_T_4)
[1595] FIRRTL:367967 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_hella_incoming_0_T_6 = and(will_fire_hella_incoming_0_will_fire, UInt<1>(0h1))
[1596] FIRRTL:367968 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_hella_incoming_0_T_7 = eq(_will_fire_hella_incoming_0_T_6, UInt<1>(0h0))
[1597] FIRRTL:367969 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_hella_incoming_0_T_8 = and(_will_fire_release_0_T_8, _will_fire_hella_incoming_0_T_7)
[1598] FIRRTL:367970 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:674:36 KIND:connect :: connect will_fire_hella_incoming[0], will_fire_hella_incoming_0_will_fire
[1599] FIRRTL:367971 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T = eq(_will_fire_hella_incoming_0_T_2, UInt<1>(0h0))
[1600] FIRRTL:367972 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_1 = and(UInt<1>(0h0), _will_fire_hella_wakeup_0_will_fire_T)
[1601] FIRRTL:367973 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_2 = eq(_will_fire_hella_wakeup_0_will_fire_T_1, UInt<1>(0h0))
[1602] FIRRTL:367974 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_3 = and(can_fire_hella_wakeup[0], _will_fire_hella_wakeup_0_will_fire_T_2)
[1603] FIRRTL:367975 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_4 = eq(_will_fire_hella_incoming_0_T_5, UInt<1>(0h0))
[1604] FIRRTL:367976 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_5 = and(UInt<1>(0h0), _will_fire_hella_wakeup_0_will_fire_T_4)
[1605] FIRRTL:367977 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_6 = eq(_will_fire_hella_wakeup_0_will_fire_T_5, UInt<1>(0h0))
[1606] FIRRTL:367978 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_7 = and(_will_fire_hella_wakeup_0_will_fire_T_3, _will_fire_hella_wakeup_0_will_fire_T_6)
[1607] FIRRTL:367979 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_8 = eq(_will_fire_hella_incoming_0_T_8, UInt<1>(0h0))
[1608] FIRRTL:367980 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_9 = and(UInt<1>(0h1), _will_fire_hella_wakeup_0_will_fire_T_8)
[1609] FIRRTL:367981 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_hella_wakeup_0_will_fire_T_10 = eq(_will_fire_hella_wakeup_0_will_fire_T_9, UInt<1>(0h0))
[1610] FIRRTL:367982 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_hella_wakeup_0_will_fire = and(_will_fire_hella_wakeup_0_will_fire_T_7, _will_fire_hella_wakeup_0_will_fire_T_10)
[1611] FIRRTL:367983 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_hella_wakeup_0_T = and(will_fire_hella_wakeup_0_will_fire, UInt<1>(0h0))
[1612] FIRRTL:367984 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_hella_wakeup_0_T_1 = eq(_will_fire_hella_wakeup_0_T, UInt<1>(0h0))
[1613] FIRRTL:367985 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_hella_wakeup_0_T_2 = and(_will_fire_hella_incoming_0_T_2, _will_fire_hella_wakeup_0_T_1)
[1614] FIRRTL:367986 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_hella_wakeup_0_T_3 = and(will_fire_hella_wakeup_0_will_fire, UInt<1>(0h0))
[1615] FIRRTL:367987 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_hella_wakeup_0_T_4 = eq(_will_fire_hella_wakeup_0_T_3, UInt<1>(0h0))
[1616] FIRRTL:367988 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_hella_wakeup_0_T_5 = and(_will_fire_hella_incoming_0_T_5, _will_fire_hella_wakeup_0_T_4)
[1617] FIRRTL:367989 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_hella_wakeup_0_T_6 = and(will_fire_hella_wakeup_0_will_fire, UInt<1>(0h1))
[1618] FIRRTL:367990 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_hella_wakeup_0_T_7 = eq(_will_fire_hella_wakeup_0_T_6, UInt<1>(0h0))
[1619] FIRRTL:367991 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_hella_wakeup_0_T_8 = and(_will_fire_hella_incoming_0_T_8, _will_fire_hella_wakeup_0_T_7)
[1620] FIRRTL:367992 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:675:36 KIND:connect :: connect will_fire_hella_wakeup[0], will_fire_hella_wakeup_0_will_fire
[1621] FIRRTL:367993 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_store_retry_0_will_fire_T = eq(_will_fire_hella_wakeup_0_T_2, UInt<1>(0h0))
[1622] FIRRTL:367994 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_store_retry_0_will_fire_T_1 = and(UInt<1>(0h1), _will_fire_store_retry_0_will_fire_T)
[1623] FIRRTL:367995 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_store_retry_0_will_fire_T_2 = eq(_will_fire_store_retry_0_will_fire_T_1, UInt<1>(0h0))
[1624] FIRRTL:367996 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_store_retry_0_will_fire_T_3 = and(can_fire_store_retry[0], _will_fire_store_retry_0_will_fire_T_2)
[1625] FIRRTL:367997 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_store_retry_0_will_fire_T_4 = eq(_will_fire_hella_wakeup_0_T_5, UInt<1>(0h0))
[1626] FIRRTL:367998 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_store_retry_0_will_fire_T_5 = and(UInt<1>(0h1), _will_fire_store_retry_0_will_fire_T_4)
[1627] FIRRTL:367999 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_store_retry_0_will_fire_T_6 = eq(_will_fire_store_retry_0_will_fire_T_5, UInt<1>(0h0))
[1628] FIRRTL:368000 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_store_retry_0_will_fire_T_7 = and(_will_fire_store_retry_0_will_fire_T_3, _will_fire_store_retry_0_will_fire_T_6)
[1629] FIRRTL:368001 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_store_retry_0_will_fire_T_8 = eq(_will_fire_hella_wakeup_0_T_8, UInt<1>(0h0))
[1630] FIRRTL:368002 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_store_retry_0_will_fire_T_9 = and(UInt<1>(0h0), _will_fire_store_retry_0_will_fire_T_8)
[1631] FIRRTL:368003 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_store_retry_0_will_fire_T_10 = eq(_will_fire_store_retry_0_will_fire_T_9, UInt<1>(0h0))
[1632] FIRRTL:368004 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_store_retry_0_will_fire = and(_will_fire_store_retry_0_will_fire_T_7, _will_fire_store_retry_0_will_fire_T_10)
[1633] FIRRTL:368005 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_store_retry_0_T = and(will_fire_store_retry_0_will_fire, UInt<1>(0h1))
[1634] FIRRTL:368006 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_store_retry_0_T_1 = eq(_will_fire_store_retry_0_T, UInt<1>(0h0))
[1635] FIRRTL:368007 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_store_retry_0_T_2 = and(_will_fire_hella_wakeup_0_T_2, _will_fire_store_retry_0_T_1)
[1636] FIRRTL:368008 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_store_retry_0_T_3 = and(will_fire_store_retry_0_will_fire, UInt<1>(0h1))
[1637] FIRRTL:368009 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_store_retry_0_T_4 = eq(_will_fire_store_retry_0_T_3, UInt<1>(0h0))
[1638] FIRRTL:368010 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_store_retry_0_T_5 = and(_will_fire_hella_wakeup_0_T_5, _will_fire_store_retry_0_T_4)
[1639] FIRRTL:368011 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_store_retry_0_T_6 = and(will_fire_store_retry_0_will_fire, UInt<1>(0h0))
[1640] FIRRTL:368012 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_store_retry_0_T_7 = eq(_will_fire_store_retry_0_T_6, UInt<1>(0h0))
[1641] FIRRTL:368013 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_store_retry_0_T_8 = and(_will_fire_hella_wakeup_0_T_8, _will_fire_store_retry_0_T_7)
[1642] FIRRTL:368014 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:676:36 KIND:connect :: connect will_fire_store_retry[0], will_fire_store_retry_0_will_fire
[1643] FIRRTL:368015 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_load_retry_0_will_fire_T = eq(_will_fire_store_retry_0_T_2, UInt<1>(0h0))
[1644] FIRRTL:368016 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_load_retry_0_will_fire_T_1 = and(UInt<1>(0h1), _will_fire_load_retry_0_will_fire_T)
[1645] FIRRTL:368017 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_load_retry_0_will_fire_T_2 = eq(_will_fire_load_retry_0_will_fire_T_1, UInt<1>(0h0))
[1646] FIRRTL:368018 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_load_retry_0_will_fire_T_3 = and(can_fire_load_retry[0], _will_fire_load_retry_0_will_fire_T_2)
[1647] FIRRTL:368019 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_load_retry_0_will_fire_T_4 = eq(_will_fire_store_retry_0_T_5, UInt<1>(0h0))
[1648] FIRRTL:368020 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_load_retry_0_will_fire_T_5 = and(UInt<1>(0h1), _will_fire_load_retry_0_will_fire_T_4)
[1649] FIRRTL:368021 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_load_retry_0_will_fire_T_6 = eq(_will_fire_load_retry_0_will_fire_T_5, UInt<1>(0h0))
[1650] FIRRTL:368022 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_load_retry_0_will_fire_T_7 = and(_will_fire_load_retry_0_will_fire_T_3, _will_fire_load_retry_0_will_fire_T_6)
[1651] FIRRTL:368023 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_load_retry_0_will_fire_T_8 = eq(_will_fire_store_retry_0_T_8, UInt<1>(0h0))
[1652] FIRRTL:368024 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_load_retry_0_will_fire_T_9 = and(UInt<1>(0h1), _will_fire_load_retry_0_will_fire_T_8)
[1653] FIRRTL:368025 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_load_retry_0_will_fire_T_10 = eq(_will_fire_load_retry_0_will_fire_T_9, UInt<1>(0h0))
[1654] FIRRTL:368026 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_load_retry_0_will_fire = and(_will_fire_load_retry_0_will_fire_T_7, _will_fire_load_retry_0_will_fire_T_10)
[1655] FIRRTL:368027 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_load_retry_0_T = and(will_fire_load_retry_0_will_fire, UInt<1>(0h1))
[1656] FIRRTL:368028 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_load_retry_0_T_1 = eq(_will_fire_load_retry_0_T, UInt<1>(0h0))
[1657] FIRRTL:368029 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_load_retry_0_T_2 = and(_will_fire_store_retry_0_T_2, _will_fire_load_retry_0_T_1)
[1658] FIRRTL:368030 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_load_retry_0_T_3 = and(will_fire_load_retry_0_will_fire, UInt<1>(0h1))
[1659] FIRRTL:368031 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_load_retry_0_T_4 = eq(_will_fire_load_retry_0_T_3, UInt<1>(0h0))
[1660] FIRRTL:368032 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_load_retry_0_T_5 = and(_will_fire_store_retry_0_T_5, _will_fire_load_retry_0_T_4)
[1661] FIRRTL:368033 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_load_retry_0_T_6 = and(will_fire_load_retry_0_will_fire, UInt<1>(0h1))
[1662] FIRRTL:368034 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_load_retry_0_T_7 = eq(_will_fire_load_retry_0_T_6, UInt<1>(0h0))
[1663] FIRRTL:368035 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_load_retry_0_T_8 = and(_will_fire_store_retry_0_T_8, _will_fire_load_retry_0_T_7)
[1664] FIRRTL:368036 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:677:36 KIND:connect :: connect will_fire_load_retry[0], will_fire_load_retry_0_will_fire
[1665] FIRRTL:368037 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T = eq(_will_fire_load_retry_0_T_2, UInt<1>(0h0))
[1666] FIRRTL:368038 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_1 = and(UInt<1>(0h0), _will_fire_load_wakeup_0_will_fire_T)
[1667] FIRRTL:368039 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_2 = eq(_will_fire_load_wakeup_0_will_fire_T_1, UInt<1>(0h0))
[1668] FIRRTL:368040 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_3 = and(can_fire_load_wakeup[0], _will_fire_load_wakeup_0_will_fire_T_2)
[1669] FIRRTL:368041 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_4 = eq(_will_fire_load_retry_0_T_5, UInt<1>(0h0))
[1670] FIRRTL:368042 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_5 = and(UInt<1>(0h1), _will_fire_load_wakeup_0_will_fire_T_4)
[1671] FIRRTL:368043 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_6 = eq(_will_fire_load_wakeup_0_will_fire_T_5, UInt<1>(0h0))
[1672] FIRRTL:368044 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_7 = and(_will_fire_load_wakeup_0_will_fire_T_3, _will_fire_load_wakeup_0_will_fire_T_6)
[1673] FIRRTL:368045 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_8 = eq(_will_fire_load_retry_0_T_8, UInt<1>(0h0))
[1674] FIRRTL:368046 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_9 = and(UInt<1>(0h1), _will_fire_load_wakeup_0_will_fire_T_8)
[1675] FIRRTL:368047 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_load_wakeup_0_will_fire_T_10 = eq(_will_fire_load_wakeup_0_will_fire_T_9, UInt<1>(0h0))
[1676] FIRRTL:368048 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_load_wakeup_0_will_fire = and(_will_fire_load_wakeup_0_will_fire_T_7, _will_fire_load_wakeup_0_will_fire_T_10)
[1677] FIRRTL:368049 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_load_wakeup_0_T = and(will_fire_load_wakeup_0_will_fire, UInt<1>(0h0))
[1678] FIRRTL:368050 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_load_wakeup_0_T_1 = eq(_will_fire_load_wakeup_0_T, UInt<1>(0h0))
[1679] FIRRTL:368051 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_load_wakeup_0_T_2 = and(_will_fire_load_retry_0_T_2, _will_fire_load_wakeup_0_T_1)
[1680] FIRRTL:368052 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:46 KIND:node :: node _will_fire_load_wakeup_0_T_3 = and(will_fire_load_wakeup_0_will_fire, UInt<1>(0h1))
[1681] FIRRTL:368053 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:34 KIND:node :: node _will_fire_load_wakeup_0_T_4 = eq(_will_fire_load_wakeup_0_T_3, UInt<1>(0h0))
[1682] FIRRTL:368054 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:655:31 KIND:node :: node _will_fire_load_wakeup_0_T_5 = and(_will_fire_load_retry_0_T_5, _will_fire_load_wakeup_0_T_4)
[1683] FIRRTL:368055 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:46 KIND:node :: node _will_fire_load_wakeup_0_T_6 = and(will_fire_load_wakeup_0_will_fire, UInt<1>(0h1))
[1684] FIRRTL:368056 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:34 KIND:node :: node _will_fire_load_wakeup_0_T_7 = eq(_will_fire_load_wakeup_0_T_6, UInt<1>(0h0))
[1685] FIRRTL:368057 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:656:31 KIND:node :: node _will_fire_load_wakeup_0_T_8 = and(_will_fire_load_retry_0_T_8, _will_fire_load_wakeup_0_T_7)
[1686] FIRRTL:368058 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:678:36 KIND:connect :: connect will_fire_load_wakeup[0], will_fire_load_wakeup_0_will_fire
[1687] FIRRTL:368059 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:51 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T = eq(_will_fire_load_wakeup_0_T_2, UInt<1>(0h0))
[1688] FIRRTL:368060 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:48 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_1 = and(UInt<1>(0h0), _will_fire_store_commit_slow_0_will_fire_T)
[1689] FIRRTL:368061 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:35 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_2 = eq(_will_fire_store_commit_slow_0_will_fire_T_1, UInt<1>(0h0))
[1690] FIRRTL:368062 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:32 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_3 = and(can_fire_store_commit_slow[0], _will_fire_store_commit_slow_0_will_fire_T_2)
[1691] FIRRTL:368063 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:52 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_4 = eq(_will_fire_load_wakeup_0_T_5, UInt<1>(0h0))
[1692] FIRRTL:368064 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:49 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_5 = and(UInt<1>(0h0), _will_fire_store_commit_slow_0_will_fire_T_4)
[1693] FIRRTL:368065 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:35 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_6 = eq(_will_fire_store_commit_slow_0_will_fire_T_5, UInt<1>(0h0))
[1694] FIRRTL:368066 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:651:63 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_7 = and(_will_fire_store_commit_slow_0_will_fire_T_3, _will_fire_store_commit_slow_0_will_fire_T_6)
[1695] FIRRTL:368067 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:50 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_8 = eq(_will_fire_load_wakeup_0_T_8, UInt<1>(0h0))
[1696] FIRRTL:368068 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:47 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_9 = and(UInt<1>(0h1), _will_fire_store_commit_slow_0_will_fire_T_8)
[1697] FIRRTL:368069 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:653:35 KIND:node :: node _will_fire_store_commit_slow_0_will_fire_T_10 = eq(_will_fire_store_commit_slow_0_will_fire_T_9, UInt<1>(0h0))
[1698] FIRRTL:368070 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:652:65 KIND:node :: node will_fire_store_commit_slow_0_will_fire = and(_will_fire_store_commit_slow_0_will_fire_T_7, _will_fire_store_commit_slow_0_will_fire_T_10)
[1699] FIRRTL:368071 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:46 KIND:node :: node _will_fire_store_commit_slow_0_T = and(will_fire_store_commit_slow_0_will_fire, UInt<1>(0h0))
[1700] FIRRTL:368072 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:34 KIND:node :: node _will_fire_store_commit_slow_0_T_1 = eq(_will_fire_store_commit_slow_0_T, UInt<1>(0h0))
[1701] FIRRTL:368073 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:654:31 KIND:node :: node _will_fire_store_commit_slow_0_T_2 = and(_will_fire_load_wakeup_0_T_2, _will_fire_store_commit_slow_0_T_1)
[1708] FIRRTL:368080 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:679:36 KIND:connect :: connect will_fire_store_commit_slow[0], will_fire_store_commit_slow_0_will_fire
[1721] FIRRTL:368093 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:684:37 KIND:when :: when will_fire_load_wakeup[0] :
[1722] FIRRTL:368094 SRC:<no-source-locator> KIND:node :: node _T_89 = bits(ldq_wakeup_idx, 2, 0)
[1723] FIRRTL:368095 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:685:49 KIND:connect :: connect block_load_mask[_T_89], UInt<1>(0h1)
[1724] FIRRTL:368096 SRC:<no-source-locator> KIND:else :: else :
[1725] FIRRTL:368097 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:686:41 KIND:node :: node _T_90 = or(will_fire_load_agen[0], will_fire_load_agen_exec[0])
[1726] FIRRTL:368098 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:686:73 KIND:when :: when _T_90 :
[1727] FIRRTL:368099 SRC:<no-source-locator> KIND:node :: node _T_91 = bits(io.core.agen[0].bits.uop.ldq_idx, 2, 0)
[1728] FIRRTL:368100 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:687:49 KIND:connect :: connect block_load_mask[_T_91], UInt<1>(0h1)
[1729] FIRRTL:368101 SRC:<no-source-locator> KIND:else :: else :
[1730] FIRRTL:368102 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:688:43 KIND:when :: when will_fire_load_retry[0] :
[1731] FIRRTL:368103 SRC:<no-source-locator> KIND:node :: node _T_92 = bits(retry_queue.io.deq.bits.uop.ldq_idx, 2, 0)
[1732] FIRRTL:368104 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:689:49 KIND:connect :: connect block_load_mask[_T_92], UInt<1>(0h1)
[1733] FIRRTL:368105 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:691:25 KIND:node :: node _exe_tlb_valid_0_T = eq(_will_fire_store_commit_slow_0_T_2, UInt<1>(0h0))
[1734] FIRRTL:368106 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:691:22 KIND:connect :: connect exe_tlb_valid[0], _exe_tlb_valid_0_T
[1767] FIRRTL:368139 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:712:53 KIND:node :: node _exe_tlb_uop_T = or(will_fire_load_agen_exec[0], will_fire_load_agen[0])
[1768] FIRRTL:368140 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:715:53 KIND:node :: node _exe_tlb_uop_T_1 = or(will_fire_load_retry[0], will_fire_store_retry[0])
[1993] FIRRTL:368365 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:717:24 KIND:node :: node _exe_tlb_uop_T_2 = mux(will_fire_hella_incoming[0], _exe_tlb_uop_WIRE, _exe_tlb_uop_WIRE_1)
[1994] FIRRTL:368366 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:715:24 KIND:node :: node _exe_tlb_uop_T_3 = mux(_exe_tlb_uop_T_1, retry_queue.io.deq.bits.uop, _exe_tlb_uop_T_2)
[1995] FIRRTL:368367 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:714:24 KIND:node :: node _exe_tlb_uop_T_4 = mux(will_fire_store_agen[0], stq_incoming_e[0].bits.uop, _exe_tlb_uop_T_3)
[1996] FIRRTL:368368 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:712:24 KIND:node :: node _exe_tlb_uop_T_5 = mux(_exe_tlb_uop_T, ldq_incoming_e[0].bits.uop, _exe_tlb_uop_T_4)
[1998] FIRRTL:368370 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_tlb_uop[0], _exe_tlb_uop_T_5
[1999] FIRRTL:368371 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:721:53 KIND:node :: node _exe_tlb_vaddr_T = or(will_fire_load_agen_exec[0], will_fire_load_agen[0])
[2000] FIRRTL:368372 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:722:53 KIND:node :: node _exe_tlb_vaddr_T_1 = or(_exe_tlb_vaddr_T, will_fire_store_agen[0])
[2001] FIRRTL:368373 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:725:53 KIND:node :: node _exe_tlb_vaddr_T_2 = or(will_fire_load_retry[0], will_fire_store_retry[0])
[2002] FIRRTL:368374 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:727:24 KIND:node :: node _exe_tlb_vaddr_T_3 = mux(will_fire_hella_incoming[0], hella_req.addr, UInt<1>(0h0))
[2003] FIRRTL:368375 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:725:24 KIND:node :: node _exe_tlb_vaddr_T_4 = mux(_exe_tlb_vaddr_T_2, retry_queue.io.deq.bits.data, _exe_tlb_vaddr_T_3)
[2004] FIRRTL:368376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:724:24 KIND:node :: node _exe_tlb_vaddr_T_5 = mux(will_fire_sfence[0], io.core.sfence.bits.addr, _exe_tlb_vaddr_T_4)
[2005] FIRRTL:368377 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:721:24 KIND:node :: node _exe_tlb_vaddr_T_6 = mux(_exe_tlb_vaddr_T_1, io.core.agen[0].bits.data, _exe_tlb_vaddr_T_5)
[2007] FIRRTL:368379 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_tlb_vaddr[0], _exe_tlb_vaddr_T_6
[2034] FIRRTL:368406 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:758:37 KIND:connect :: connect dtlb.io.req[0].valid, exe_tlb_valid[0]
[2179] FIRRTL:368551 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:830:86 KIND:node :: node _exe_tlb_miss_T = eq(dtlb.io.req[0].ready, UInt<1>(0h0))
[2180] FIRRTL:368552 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:830:83 KIND:node :: node _exe_tlb_miss_T_1 = or(dtlb.io.resp[0].miss, _exe_tlb_miss_T)
[2181] FIRRTL:368553 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:830:58 KIND:node :: node _exe_tlb_miss_T_2 = and(dtlb.io.req[0].valid, _exe_tlb_miss_T_1)
[2183] FIRRTL:368555 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_tlb_miss[0], _exe_tlb_miss_T_2
[2184] FIRRTL:368556 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:831:62 KIND:node :: node _exe_tlb_paddr_T = bits(dtlb.io.resp[0].paddr, 31, 12)
[2185] FIRRTL:368557 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:832:57 KIND:node :: node _exe_tlb_paddr_T_1 = bits(exe_tlb_vaddr[0], 11, 0)
[2186] FIRRTL:368558 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:831:40 KIND:node :: node _exe_tlb_paddr_T_2 = cat(_exe_tlb_paddr_T, _exe_tlb_paddr_T_1)
[2188] FIRRTL:368560 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_tlb_paddr[0], _exe_tlb_paddr_T_2
[2189] FIRRTL:368561 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:833:43 KIND:node :: node _exe_tlb_uncacheable_T = eq(dtlb.io.resp[0].cacheable, UInt<1>(0h0))
[2191] FIRRTL:368563 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_tlb_uncacheable[0], _exe_tlb_uncacheable_T
[2228] FIRRTL:368600 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _exe_agen_killed_T = and(io.core.brupdate.b1.mispredict_mask, io.core.agen[0].bits.uop.br_mask)
[2229] FIRRTL:368601 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _exe_agen_killed_T_1 = neq(_exe_agen_killed_T, UInt<1>(0h0))
[2230] FIRRTL:368602 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _exe_agen_killed_T_2 = or(_exe_agen_killed_T_1, io.core.exception)
[2232] FIRRTL:368604 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:326:49 KIND:connect :: connect exe_agen_killed[0], _exe_agen_killed_T_2
[2238] FIRRTL:368610 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:873:21 KIND:connect :: connect io.dmem.req.valid, dmem_req[0].valid
[2239] FIRRTL:368611 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:874:21 KIND:connect :: connect io.dmem.req.bits, dmem_req
[2256] FIRRTL:368628 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:881:23 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h0)
[2258] FIRRTL:368630 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.debug_tsrc, UInt<3>(0h0)
[2259] FIRRTL:368631 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.debug_fsrc, UInt<3>(0h0)
[2260] FIRRTL:368632 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.bp_xcpt_if, UInt<1>(0h0)
[2261] FIRRTL:368633 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.bp_debug_if, UInt<1>(0h0)
[2262] FIRRTL:368634 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.xcpt_ma_if, UInt<1>(0h0)
[2263] FIRRTL:368635 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.xcpt_ae_if, UInt<1>(0h0)
[2264] FIRRTL:368636 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.xcpt_pf_if, UInt<1>(0h0)
[2265] FIRRTL:368637 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_typ, UInt<2>(0h0)
[2266] FIRRTL:368638 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_rm, UInt<3>(0h0)
[2267] FIRRTL:368639 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_val, UInt<1>(0h0)
[2268] FIRRTL:368640 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fcn_op, UInt<5>(0h0)
[2269] FIRRTL:368641 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fcn_dw, UInt<1>(0h0)
[2270] FIRRTL:368642 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.frs3_en, UInt<1>(0h0)
[2271] FIRRTL:368643 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.lrs2_rtype, UInt<2>(0h0)
[2272] FIRRTL:368644 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.lrs1_rtype, UInt<2>(0h0)
[2273] FIRRTL:368645 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.dst_rtype, UInt<2>(0h0)
[2274] FIRRTL:368646 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.lrs3, UInt<6>(0h0)
[2275] FIRRTL:368647 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.lrs2, UInt<6>(0h0)
[2276] FIRRTL:368648 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.lrs1, UInt<6>(0h0)
[2277] FIRRTL:368649 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ldst, UInt<6>(0h0)
[2278] FIRRTL:368650 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ldst_is_rs1, UInt<1>(0h0)
[2279] FIRRTL:368651 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.csr_cmd, UInt<3>(0h0)
[2280] FIRRTL:368652 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.flush_on_commit, UInt<1>(0h0)
[2281] FIRRTL:368653 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_unique, UInt<1>(0h0)
[2282] FIRRTL:368654 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.uses_stq, UInt<1>(0h0)
[2283] FIRRTL:368655 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.uses_ldq, UInt<1>(0h0)
[2284] FIRRTL:368656 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.mem_signed, UInt<1>(0h0)
[2285] FIRRTL:368657 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.mem_size, UInt<2>(0h0)
[2286] FIRRTL:368658 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.mem_cmd, UInt<5>(0h0)
[2287] FIRRTL:368659 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.exc_cause, UInt<64>(0h0)
[2288] FIRRTL:368660 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.exception, UInt<1>(0h0)
[2289] FIRRTL:368661 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.stale_pdst, UInt<6>(0h0)
[2290] FIRRTL:368662 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ppred_busy, UInt<1>(0h0)
[2291] FIRRTL:368663 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs3_busy, UInt<1>(0h0)
[2292] FIRRTL:368664 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs2_busy, UInt<1>(0h0)
[2293] FIRRTL:368665 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs1_busy, UInt<1>(0h0)
[2294] FIRRTL:368666 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ppred, UInt<4>(0h0)
[2295] FIRRTL:368667 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs3, UInt<6>(0h0)
[2296] FIRRTL:368668 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs2, UInt<6>(0h0)
[2297] FIRRTL:368669 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.prs1, UInt<6>(0h0)
[2298] FIRRTL:368670 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.pdst, UInt<6>(0h0)
[2299] FIRRTL:368671 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.rxq_idx, UInt<2>(0h0)
[2300] FIRRTL:368672 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.stq_idx, UInt<4>(0h0)
[2301] FIRRTL:368673 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ldq_idx, UInt<4>(0h0)
[2302] FIRRTL:368674 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.rob_idx, UInt<5>(0h0)
[2303] FIRRTL:368675 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.vec, UInt<1>(0h0)
[2304] FIRRTL:368676 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.wflags, UInt<1>(0h0)
[2305] FIRRTL:368677 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.sqrt, UInt<1>(0h0)
[2306] FIRRTL:368678 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.div, UInt<1>(0h0)
[2307] FIRRTL:368679 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.fma, UInt<1>(0h0)
[2308] FIRRTL:368680 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.fastpipe, UInt<1>(0h0)
[2309] FIRRTL:368681 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.toint, UInt<1>(0h0)
[2310] FIRRTL:368682 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.fromint, UInt<1>(0h0)
[2311] FIRRTL:368683 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.typeTagOut, UInt<2>(0h0)
[2312] FIRRTL:368684 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.typeTagIn, UInt<2>(0h0)
[2313] FIRRTL:368685 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.swap23, UInt<1>(0h0)
[2314] FIRRTL:368686 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.swap12, UInt<1>(0h0)
[2315] FIRRTL:368687 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.ren3, UInt<1>(0h0)
[2316] FIRRTL:368688 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.ren2, UInt<1>(0h0)
[2317] FIRRTL:368689 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.ren1, UInt<1>(0h0)
[2318] FIRRTL:368690 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.wen, UInt<1>(0h0)
[2319] FIRRTL:368691 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fp_ctrl.ldst, UInt<1>(0h0)
[2320] FIRRTL:368692 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.op2_sel, UInt<3>(0h0)
[2321] FIRRTL:368693 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.op1_sel, UInt<2>(0h0)
[2322] FIRRTL:368694 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.imm_packed, UInt<20>(0h0)
[2323] FIRRTL:368695 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.pimm, UInt<5>(0h0)
[2324] FIRRTL:368696 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.imm_sel, UInt<3>(0h0)
[2325] FIRRTL:368697 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.imm_rename, UInt<1>(0h0)
[2326] FIRRTL:368698 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.taken, UInt<1>(0h0)
[2327] FIRRTL:368699 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.pc_lob, UInt<6>(0h0)
[2328] FIRRTL:368700 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.edge_inst, UInt<1>(0h0)
[2329] FIRRTL:368701 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.ftq_idx, UInt<4>(0h0)
[2330] FIRRTL:368702 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_mov, UInt<1>(0h0)
[2331] FIRRTL:368703 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_rocc, UInt<1>(0h0)
[2332] FIRRTL:368704 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_sys_pc2epc, UInt<1>(0h0)
[2333] FIRRTL:368705 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_eret, UInt<1>(0h0)
[2334] FIRRTL:368706 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_amo, UInt<1>(0h0)
[2335] FIRRTL:368707 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_sfence, UInt<1>(0h0)
[2336] FIRRTL:368708 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_fencei, UInt<1>(0h0)
[2337] FIRRTL:368709 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_fence, UInt<1>(0h0)
[2338] FIRRTL:368710 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_sfb, UInt<1>(0h0)
[2339] FIRRTL:368711 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.br_type, UInt<4>(0h0)
[2340] FIRRTL:368712 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.br_tag, UInt<3>(0h0)
[2341] FIRRTL:368713 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.br_mask, UInt<8>(0h0)
[2342] FIRRTL:368714 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.dis_col_sel, UInt<1>(0h0)
[2343] FIRRTL:368715 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_p3_bypass_hint, UInt<1>(0h0)
[2344] FIRRTL:368716 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_p2_bypass_hint, UInt<1>(0h0)
[2345] FIRRTL:368717 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_p1_bypass_hint, UInt<1>(0h0)
[2346] FIRRTL:368718 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_p2_speculative_child, UInt<1>(0h0)
[2347] FIRRTL:368719 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_p1_speculative_child, UInt<1>(0h0)
[2348] FIRRTL:368720 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_issued_partial_dgen, UInt<1>(0h0)
[2349] FIRRTL:368721 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_issued_partial_agen, UInt<1>(0h0)
[2350] FIRRTL:368722 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iw_issued, UInt<1>(0h0)
[2351] FIRRTL:368723 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[0], UInt<1>(0h0)
[2352] FIRRTL:368724 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[1], UInt<1>(0h0)
[2353] FIRRTL:368725 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[2], UInt<1>(0h0)
[2354] FIRRTL:368726 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[3], UInt<1>(0h0)
[2355] FIRRTL:368727 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[4], UInt<1>(0h0)
[2356] FIRRTL:368728 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[5], UInt<1>(0h0)
[2357] FIRRTL:368729 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[6], UInt<1>(0h0)
[2358] FIRRTL:368730 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[7], UInt<1>(0h0)
[2359] FIRRTL:368731 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[8], UInt<1>(0h0)
[2360] FIRRTL:368732 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.fu_code[9], UInt<1>(0h0)
[2361] FIRRTL:368733 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iq_type[0], UInt<1>(0h0)
[2362] FIRRTL:368734 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iq_type[1], UInt<1>(0h0)
[2363] FIRRTL:368735 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iq_type[2], UInt<1>(0h0)
[2364] FIRRTL:368736 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.iq_type[3], UInt<1>(0h0)
[2365] FIRRTL:368737 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.debug_pc, UInt<40>(0h0)
[2366] FIRRTL:368738 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.is_rvc, UInt<1>(0h0)
[2367] FIRRTL:368739 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.debug_inst, UInt<32>(0h0)
[2368] FIRRTL:368740 SRC:generators/boom/src/main/scala/v4/common/consts.scala:141:57 KIND:connect :: connect _dmem_req_0_bits_uop_WIRE.inst, UInt<32>(0h0)
[2369] FIRRTL:368741 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:882:28 KIND:connect :: connect dmem_req[0].bits.uop, _dmem_req_0_bits_uop_WIRE
[2370] FIRRTL:368742 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:883:28 KIND:connect :: connect dmem_req[0].bits.addr, UInt<1>(0h0)
[2371] FIRRTL:368743 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:884:28 KIND:connect :: connect dmem_req[0].bits.data, UInt<1>(0h0)
[2372] FIRRTL:368744 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:885:31 KIND:connect :: connect dmem_req[0].bits.is_hella, UInt<1>(0h0)
[2378] FIRRTL:368750 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:890:40 KIND:when :: when will_fire_load_agen_exec[0] :
[2379] FIRRTL:368751 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:891:30 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h1)
[2380] FIRRTL:368752 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:892:30 KIND:connect :: connect dmem_req[0].bits.addr, exe_tlb_paddr[0]
[2381] FIRRTL:368753 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:893:30 KIND:connect :: connect dmem_req[0].bits.uop, exe_tlb_uop[0]
[2399] FIRRTL:368771 SRC:<no-source-locator> KIND:else :: else :
[2400] FIRRTL:368772 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:899:43 KIND:when :: when will_fire_load_retry[0] :
[2401] FIRRTL:368773 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:900:30 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h1)
[2402] FIRRTL:368774 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:901:30 KIND:connect :: connect dmem_req[0].bits.addr, exe_tlb_paddr[0]
[2403] FIRRTL:368775 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:902:30 KIND:connect :: connect dmem_req[0].bits.uop, exe_tlb_uop[0]
[2413] FIRRTL:368785 SRC:<no-source-locator> KIND:else :: else :
[2414] FIRRTL:368786 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:906:49 KIND:node :: node _T_145 = or(will_fire_store_commit_slow[0], will_fire_store_commit_fast[0])
[2415] FIRRTL:368787 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:906:84 KIND:when :: when _T_145 :
[2416] FIRRTL:368788 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:907:33 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h1)
[2417] FIRRTL:368789 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:908:33 KIND:connect :: connect dmem_req[0].bits.addr, stq_execute_queue.io.deq.bits.addr.bits
[2419] FIRRTL:368791 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect dmem_req_0_bits_data_size, stq_execute_queue.io.deq.bits.uop.mem_size
[2420] FIRRTL:368792 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T = eq(dmem_req_0_bits_data_size, UInt<1>(0h0))
[2421] FIRRTL:368793 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_1 = bits(stq_execute_queue.io.deq.bits.data.bits, 7, 0)
[2422] FIRRTL:368794 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_2 = cat(_dmem_req_0_bits_data_T_1, _dmem_req_0_bits_data_T_1)
[2423] FIRRTL:368795 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_3 = cat(_dmem_req_0_bits_data_T_2, _dmem_req_0_bits_data_T_2)
[2424] FIRRTL:368796 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_4 = cat(_dmem_req_0_bits_data_T_3, _dmem_req_0_bits_data_T_3)
[2425] FIRRTL:368797 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_5 = eq(dmem_req_0_bits_data_size, UInt<1>(0h1))
[2426] FIRRTL:368798 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_6 = bits(stq_execute_queue.io.deq.bits.data.bits, 15, 0)
[2427] FIRRTL:368799 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_7 = cat(_dmem_req_0_bits_data_T_6, _dmem_req_0_bits_data_T_6)
[2428] FIRRTL:368800 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_8 = cat(_dmem_req_0_bits_data_T_7, _dmem_req_0_bits_data_T_7)
[2429] FIRRTL:368801 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_9 = eq(dmem_req_0_bits_data_size, UInt<2>(0h2))
[2430] FIRRTL:368802 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_10 = bits(stq_execute_queue.io.deq.bits.data.bits, 31, 0)
[2431] FIRRTL:368803 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_11 = cat(_dmem_req_0_bits_data_T_10, _dmem_req_0_bits_data_T_10)
[2432] FIRRTL:368804 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_12 = mux(_dmem_req_0_bits_data_T_9, _dmem_req_0_bits_data_T_11, stq_execute_queue.io.deq.bits.data.bits)
[2433] FIRRTL:368805 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_13 = mux(_dmem_req_0_bits_data_T_5, _dmem_req_0_bits_data_T_8, _dmem_req_0_bits_data_T_12)
[2434] FIRRTL:368806 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_14 = mux(_dmem_req_0_bits_data_T, _dmem_req_0_bits_data_T_4, _dmem_req_0_bits_data_T_13)
[2435] FIRRTL:368807 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:909:33 KIND:connect :: connect dmem_req[0].bits.data, _dmem_req_0_bits_data_T_14
[2436] FIRRTL:368808 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:913:33 KIND:connect :: connect dmem_req[0].bits.uop, stq_execute_queue.io.deq.bits.uop
[2443] FIRRTL:368815 SRC:<no-source-locator> KIND:else :: else :
[2444] FIRRTL:368816 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:921:44 KIND:when :: when will_fire_load_wakeup[0] :
[2445] FIRRTL:368817 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:922:30 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h1)
[2446] FIRRTL:368818 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:923:30 KIND:connect :: connect dmem_req[0].bits.addr, ldq_wakeup_e.bits.addr.bits
[2447] FIRRTL:368819 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:924:30 KIND:connect :: connect dmem_req[0].bits.uop, ldq_wakeup_e.bits.uop
[2460] FIRRTL:368832 SRC:<no-source-locator> KIND:else :: else :
[2461] FIRRTL:368833 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:929:47 KIND:when :: when will_fire_hella_incoming[0] :
[2470] FIRRTL:368842 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:932:42 KIND:node :: node _dmem_req_0_valid_T = eq(io.hellacache.s1_kill, UInt<1>(0h0))
[2471] FIRRTL:368843 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:932:69 KIND:node :: node _dmem_req_0_valid_T_1 = eq(exe_tlb_miss[0], UInt<1>(0h0))
[2472] FIRRTL:368844 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:932:86 KIND:node :: node _dmem_req_0_valid_T_2 = or(_dmem_req_0_valid_T_1, hella_req.phys)
[2473] FIRRTL:368845 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:932:65 KIND:node :: node _dmem_req_0_valid_T_3 = and(_dmem_req_0_valid_T, _dmem_req_0_valid_T_2)
[2474] FIRRTL:368846 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:932:39 KIND:connect :: connect dmem_req[0].valid, _dmem_req_0_valid_T_3
[2475] FIRRTL:368847 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:933:39 KIND:connect :: connect dmem_req[0].bits.addr, exe_tlb_paddr[0]
[2477] FIRRTL:368849 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect dmem_req_0_bits_data_size_1, hella_req.size
[2478] FIRRTL:368850 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_15 = eq(dmem_req_0_bits_data_size_1, UInt<1>(0h0))
[2479] FIRRTL:368851 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_16 = bits(io.hellacache.s1_data.data, 7, 0)
[2480] FIRRTL:368852 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_17 = cat(_dmem_req_0_bits_data_T_16, _dmem_req_0_bits_data_T_16)
[2481] FIRRTL:368853 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_18 = cat(_dmem_req_0_bits_data_T_17, _dmem_req_0_bits_data_T_17)
[2482] FIRRTL:368854 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_19 = cat(_dmem_req_0_bits_data_T_18, _dmem_req_0_bits_data_T_18)
[2483] FIRRTL:368855 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_20 = eq(dmem_req_0_bits_data_size_1, UInt<1>(0h1))
[2484] FIRRTL:368856 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_21 = bits(io.hellacache.s1_data.data, 15, 0)
[2485] FIRRTL:368857 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_22 = cat(_dmem_req_0_bits_data_T_21, _dmem_req_0_bits_data_T_21)
[2486] FIRRTL:368858 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_23 = cat(_dmem_req_0_bits_data_T_22, _dmem_req_0_bits_data_T_22)
[2487] FIRRTL:368859 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_24 = eq(dmem_req_0_bits_data_size_1, UInt<2>(0h2))
[2488] FIRRTL:368860 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_25 = bits(io.hellacache.s1_data.data, 31, 0)
[2489] FIRRTL:368861 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_26 = cat(_dmem_req_0_bits_data_T_25, _dmem_req_0_bits_data_T_25)
[2490] FIRRTL:368862 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_27 = mux(_dmem_req_0_bits_data_T_24, _dmem_req_0_bits_data_T_26, io.hellacache.s1_data.data)
[2491] FIRRTL:368863 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_28 = mux(_dmem_req_0_bits_data_T_20, _dmem_req_0_bits_data_T_23, _dmem_req_0_bits_data_T_27)
[2492] FIRRTL:368864 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_29 = mux(_dmem_req_0_bits_data_T_15, _dmem_req_0_bits_data_T_19, _dmem_req_0_bits_data_T_28)
[2493] FIRRTL:368865 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:934:39 KIND:connect :: connect dmem_req[0].bits.data, _dmem_req_0_bits_data_T_29
[2494] FIRRTL:368866 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:938:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_cmd, hella_req.cmd
[2495] FIRRTL:368867 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:939:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_size, hella_req.size
[2496] FIRRTL:368868 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:940:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_signed, hella_req.signed
[2497] FIRRTL:368869 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:941:39 KIND:connect :: connect dmem_req[0].bits.is_hella, UInt<1>(0h1)
[2499] FIRRTL:368871 SRC:<no-source-locator> KIND:else :: else :
[2500] FIRRTL:368872 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:946:5 KIND:when :: when will_fire_hella_wakeup[0] :
[2509] FIRRTL:368881 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:948:39 KIND:connect :: connect dmem_req[0].valid, UInt<1>(0h1)
[2510] FIRRTL:368882 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:949:39 KIND:connect :: connect dmem_req[0].bits.addr, hella_paddr
[2512] FIRRTL:368884 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect dmem_req_0_bits_data_size_2, hella_req.size
[2513] FIRRTL:368885 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_30 = eq(dmem_req_0_bits_data_size_2, UInt<1>(0h0))
[2514] FIRRTL:368886 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_31 = bits(hella_data.data, 7, 0)
[2515] FIRRTL:368887 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_32 = cat(_dmem_req_0_bits_data_T_31, _dmem_req_0_bits_data_T_31)
[2516] FIRRTL:368888 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_33 = cat(_dmem_req_0_bits_data_T_32, _dmem_req_0_bits_data_T_32)
[2517] FIRRTL:368889 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_34 = cat(_dmem_req_0_bits_data_T_33, _dmem_req_0_bits_data_T_33)
[2518] FIRRTL:368890 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_35 = eq(dmem_req_0_bits_data_size_2, UInt<1>(0h1))
[2519] FIRRTL:368891 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_36 = bits(hella_data.data, 15, 0)
[2520] FIRRTL:368892 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_37 = cat(_dmem_req_0_bits_data_T_36, _dmem_req_0_bits_data_T_36)
[2521] FIRRTL:368893 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_38 = cat(_dmem_req_0_bits_data_T_37, _dmem_req_0_bits_data_T_37)
[2522] FIRRTL:368894 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:19 KIND:node :: node _dmem_req_0_bits_data_T_39 = eq(dmem_req_0_bits_data_size_2, UInt<2>(0h2))
[2523] FIRRTL:368895 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:69 KIND:node :: node _dmem_req_0_bits_data_T_40 = bits(hella_data.data, 31, 0)
[2524] FIRRTL:368896 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:32 KIND:node :: node _dmem_req_0_bits_data_T_41 = cat(_dmem_req_0_bits_data_T_40, _dmem_req_0_bits_data_T_40)
[2525] FIRRTL:368897 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_42 = mux(_dmem_req_0_bits_data_T_39, _dmem_req_0_bits_data_T_41, hella_data.data)
[2526] FIRRTL:368898 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_43 = mux(_dmem_req_0_bits_data_T_35, _dmem_req_0_bits_data_T_38, _dmem_req_0_bits_data_T_42)
[2527] FIRRTL:368899 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:29:13 KIND:node :: node _dmem_req_0_bits_data_T_44 = mux(_dmem_req_0_bits_data_T_30, _dmem_req_0_bits_data_T_34, _dmem_req_0_bits_data_T_43)
[2528] FIRRTL:368900 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:950:39 KIND:connect :: connect dmem_req[0].bits.data, _dmem_req_0_bits_data_T_44
[2529] FIRRTL:368901 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:954:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_cmd, hella_req.cmd
[2530] FIRRTL:368902 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:955:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_size, hella_req.size
[2531] FIRRTL:368903 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:956:39 KIND:connect :: connect dmem_req[0].bits.uop.mem_signed, hella_req.signed
[2532] FIRRTL:368904 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:957:39 KIND:connect :: connect dmem_req[0].bits.is_hella, UInt<1>(0h1)
[2533] FIRRTL:368905 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:962:34 KIND:node :: node _T_163 = or(will_fire_load_agen[0], will_fire_load_agen_exec[0])
[2534] FIRRTL:368906 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:962:65 KIND:node :: node _T_164 = or(_T_163, will_fire_load_retry[0])
[2535] FIRRTL:368907 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:963:5 KIND:when :: when _T_164 :
[2536] FIRRTL:368908 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:964:48 KIND:node :: node _ldq_idx_T = or(will_fire_load_agen[0], will_fire_load_agen_exec[0])
[2537] FIRRTL:368909 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:964:24 KIND:node :: node ldq_idx = mux(_ldq_idx_T, ldq_incoming_idx[0], retry_queue.io.deq.bits.uop.ldq_idx)
[2538] FIRRTL:368910 SRC:<no-source-locator> KIND:node :: node _T_165 = bits(ldq_idx, 2, 0)
[2539] FIRRTL:368911 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:965:50 KIND:node :: node _ldq_addr_valid_T = eq(exe_agen_killed[0], UInt<1>(0h0))
[2540] FIRRTL:368912 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:965:70 KIND:node :: node _ldq_addr_valid_T_1 = or(_ldq_addr_valid_T, will_fire_load_retry[0])
[2541] FIRRTL:368913 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:965:47 KIND:connect :: connect ldq_addr[_T_165].valid, _ldq_addr_valid_T_1
[2542] FIRRTL:368914 SRC:<no-source-locator> KIND:node :: node _T_166 = bits(ldq_idx, 2, 0)
[2543] FIRRTL:368915 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:966:53 KIND:node :: node _ldq_addr_bits_T = mux(exe_tlb_miss[0], exe_tlb_vaddr[0], exe_tlb_paddr[0])
[2544] FIRRTL:368916 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:966:47 KIND:connect :: connect ldq_addr[_T_166].bits, _ldq_addr_bits_T
[2566] FIRRTL:368938 SRC:<no-source-locator> KIND:node :: node _T_169 = bits(ldq_idx, 2, 0)
[2567] FIRRTL:368939 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:969:47 KIND:connect :: connect ldq_addr_is_virtual[_T_169], exe_tlb_miss[0]
[2568] FIRRTL:368940 SRC:<no-source-locator> KIND:node :: node _T_170 = bits(ldq_idx, 2, 0)
[2569] FIRRTL:368941 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:970:76 KIND:node :: node _ldq_addr_is_uncacheable_T = eq(exe_tlb_miss[0], UInt<1>(0h0))
[2570] FIRRTL:368942 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:970:73 KIND:node :: node _ldq_addr_is_uncacheable_T_1 = and(exe_tlb_uncacheable[0], _ldq_addr_is_uncacheable_T)
[2571] FIRRTL:368943 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:970:47 KIND:connect :: connect ldq_addr_is_uncacheable[_T_170], _ldq_addr_is_uncacheable_T_1
[3791] FIRRTL:370163 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1172:36 KIND:connect :: connect s1_set_execute, s1_executing_loads
[3945] FIRRTL:370317 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[0], UInt<1>(0h1)
[3975] FIRRTL:370347 SRC:<no-source-locator> KIND:node :: node _T_285 = bits(lcam_ldq_idx[0], 2, 0)
[3976] FIRRTL:370348 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_285], UInt<1>(0h0)
[4091] FIRRTL:370463 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[1], UInt<1>(0h1)
[4121] FIRRTL:370493 SRC:<no-source-locator> KIND:node :: node _T_337 = bits(lcam_ldq_idx[0], 2, 0)
[4122] FIRRTL:370494 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_337], UInt<1>(0h0)
[4237] FIRRTL:370609 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[2], UInt<1>(0h1)
[4267] FIRRTL:370639 SRC:<no-source-locator> KIND:node :: node _T_389 = bits(lcam_ldq_idx[0], 2, 0)
[4268] FIRRTL:370640 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_389], UInt<1>(0h0)
[4383] FIRRTL:370755 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[3], UInt<1>(0h1)
[4413] FIRRTL:370785 SRC:<no-source-locator> KIND:node :: node _T_441 = bits(lcam_ldq_idx[0], 2, 0)
[4414] FIRRTL:370786 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_441], UInt<1>(0h0)
[4529] FIRRTL:370901 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[4], UInt<1>(0h1)
[4559] FIRRTL:370931 SRC:<no-source-locator> KIND:node :: node _T_493 = bits(lcam_ldq_idx[0], 2, 0)
[4560] FIRRTL:370932 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_493], UInt<1>(0h0)
[4675] FIRRTL:371047 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[5], UInt<1>(0h1)
[4705] FIRRTL:371077 SRC:<no-source-locator> KIND:node :: node _T_545 = bits(lcam_ldq_idx[0], 2, 0)
[4706] FIRRTL:371078 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_545], UInt<1>(0h0)
[4821] FIRRTL:371193 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[6], UInt<1>(0h1)
[4851] FIRRTL:371223 SRC:<no-source-locator> KIND:node :: node _T_597 = bits(lcam_ldq_idx[0], 2, 0)
[4852] FIRRTL:371224 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_597], UInt<1>(0h0)
[4967] FIRRTL:371339 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1234:29 KIND:connect :: connect ldq_order_fail[7], UInt<1>(0h1)
[4997] FIRRTL:371369 SRC:<no-source-locator> KIND:node :: node _T_649 = bits(lcam_ldq_idx[0], 2, 0)
[4998] FIRRTL:371370 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1262:48 KIND:connect :: connect s1_set_execute[_T_649], UInt<1>(0h0)
[5077] FIRRTL:371449 SRC:<no-source-locator> KIND:node :: node _T_682 = bits(lcam_ldq_idx[0], 2, 0)
[5078] FIRRTL:371450 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1287:41 KIND:connect :: connect s1_set_execute[_T_682], UInt<1>(0h0)
[5157] FIRRTL:371529 SRC:<no-source-locator> KIND:node :: node _T_715 = bits(wb_ldst_forward_ldq_idx[0], 2, 0)
[5158] FIRRTL:371530 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1306:53 KIND:connect :: connect ldq_order_fail[_T_715], UInt<1>(0h1)
[5220] FIRRTL:371592 SRC:<no-source-locator> KIND:node :: node _T_728 = bits(wb_ldst_forward_ldq_idx[0], 2, 0)
[5221] FIRRTL:371593 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1319:53 KIND:connect :: connect ldq_order_fail[_T_728], UInt<1>(0h1)
[5963] FIRRTL:372335 SRC:<no-source-locator> KIND:node :: node _T_872 = bits(lcam_ldq_idx[0], 2, 0)
[5964] FIRRTL:372336 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1379:39 KIND:connect :: connect s1_set_execute[_T_872], UInt<1>(0h0)
[5967] FIRRTL:372339 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[0] :
[5968] FIRRTL:372340 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[0], UInt<1>(0h1)
[5969] FIRRTL:372341 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[1] :
[5970] FIRRTL:372342 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[1], UInt<1>(0h1)
[5971] FIRRTL:372343 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[2] :
[5972] FIRRTL:372344 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[2], UInt<1>(0h1)
[5973] FIRRTL:372345 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[3] :
[5974] FIRRTL:372346 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[3], UInt<1>(0h1)
[5975] FIRRTL:372347 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[4] :
[5976] FIRRTL:372348 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[4], UInt<1>(0h1)
[5977] FIRRTL:372349 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[5] :
[5978] FIRRTL:372350 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[5], UInt<1>(0h1)
[5979] FIRRTL:372351 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[6] :
[5980] FIRRTL:372352 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[6], UInt<1>(0h1)
[5981] FIRRTL:372353 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:30 KIND:when :: when s1_set_execute[7] :
[5982] FIRRTL:372354 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1388:48 KIND:connect :: connect ldq_executed[7], UInt<1>(0h1)
[6013] FIRRTL:372385 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1417:40 KIND:node :: node _T_875 = neq(ldst_addr_matches[0], UInt<1>(0h0))
[6015] FIRRTL:372387 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1417:18 KIND:connect :: connect REG_11, _T_875
[6016] FIRRTL:372388 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1417:52 KIND:node :: node _T_876 = eq(wb_ldst_forward_valid[0], UInt<1>(0h0))
[6017] FIRRTL:372389 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1417:49 KIND:node :: node _T_877 = and(REG_11, _T_876)
[6018] FIRRTL:372390 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1417:79 KIND:when :: when _T_877 :
[6019] FIRRTL:372391 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1418:25 KIND:connect :: connect block_load_wakeup, UInt<1>(0h1)
[6021] FIRRTL:372393 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1423:42 KIND:node :: node _T_878 = or(will_fire_store_commit_fast[0], will_fire_store_commit_slow[0])
[6022] FIRRTL:372394 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1423:79 KIND:node :: node _T_879 = eq(can_fire_store_commit_slow[0], UInt<1>(0h0))
[6023] FIRRTL:372395 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1423:76 KIND:node :: node _T_880 = or(_T_878, _T_879)
[6024] FIRRTL:372396 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1423:111 KIND:when :: when _T_880 :
[6025] FIRRTL:372397 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1424:29 KIND:connect :: connect store_blocked_counter, UInt<1>(0h0)
[6026] FIRRTL:372398 SRC:<no-source-locator> KIND:else :: else :
[6027] FIRRTL:372399 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1425:84 KIND:node :: node _T_881 = or(will_fire_store_commit_slow[0], will_fire_store_commit_fast[0])
[6028] FIRRTL:372400 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1425:51 KIND:node :: node _T_882 = eq(_T_881, UInt<1>(0h0))
[6029] FIRRTL:372401 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1425:48 KIND:node :: node _T_883 = and(can_fire_store_commit_slow[0], _T_882)
[6030] FIRRTL:372402 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1425:120 KIND:when :: when _T_883 :
[6031] FIRRTL:372403 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1426:58 KIND:node :: node _store_blocked_counter_T = eq(store_blocked_counter, UInt<4>(0hf))
[6032] FIRRTL:372404 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1426:96 KIND:node :: node _store_blocked_counter_T_1 = add(store_blocked_counter, UInt<1>(0h1))
[6033] FIRRTL:372405 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1426:96 KIND:node :: node _store_blocked_counter_T_2 = tail(_store_blocked_counter_T_1, 1)
[6034] FIRRTL:372406 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1426:35 KIND:node :: node _store_blocked_counter_T_3 = mux(_store_blocked_counter_T, UInt<4>(0hf), _store_blocked_counter_T_2)
[6035] FIRRTL:372407 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1426:29 KIND:connect :: connect store_blocked_counter, _store_blocked_counter_T_3
[6036] FIRRTL:372408 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1428:33 KIND:node :: node _T_884 = eq(store_blocked_counter, UInt<4>(0hf))
[6037] FIRRTL:372409 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1428:43 KIND:when :: when _T_884 :
[6038] FIRRTL:372410 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1429:25 KIND:connect :: connect block_load_wakeup, UInt<1>(0h1)
[6848] FIRRTL:373220 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1543:34 KIND:when :: when io.dmem.nack[0].valid :
[6860] FIRRTL:373232 SRC:<no-source-locator> KIND:else :: else :
[6861] FIRRTL:373233 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1546:55 KIND:when :: when io.dmem.nack[0].bits.uop.uses_ldq :
[6870] FIRRTL:373242 SRC:<no-source-locator> KIND:node :: node _T_895 = bits(io.dmem.nack[0].bits.uop.ldq_idx, 2, 0)
[6871] FIRRTL:373243 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1548:56 KIND:connect :: connect ldq_executed[_T_895], UInt<1>(0h0)
[7774] FIRRTL:374146 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[0] :
[7780] FIRRTL:374152 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1067 = and(io.core.brupdate.b1.mispredict_mask, uop_9.br_mask)
[7781] FIRRTL:374153 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1068 = neq(_T_1067, UInt<1>(0h0))
[7782] FIRRTL:374154 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1069 = or(_T_1068, io.core.exception)
[7783] FIRRTL:374155 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1069 :
[7784] FIRRTL:374156 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[0], UInt<1>(0h0)
[7785] FIRRTL:374157 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[0].valid, UInt<1>(0h0)
[7786] FIRRTL:374158 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[1] :
[7792] FIRRTL:374164 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1070 = and(io.core.brupdate.b1.mispredict_mask, uop_10.br_mask)
[7793] FIRRTL:374165 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1071 = neq(_T_1070, UInt<1>(0h0))
[7794] FIRRTL:374166 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1072 = or(_T_1071, io.core.exception)
[7795] FIRRTL:374167 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1072 :
[7796] FIRRTL:374168 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[1], UInt<1>(0h0)
[7797] FIRRTL:374169 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[1].valid, UInt<1>(0h0)
[7798] FIRRTL:374170 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[2] :
[7804] FIRRTL:374176 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1073 = and(io.core.brupdate.b1.mispredict_mask, uop_11.br_mask)
[7805] FIRRTL:374177 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1074 = neq(_T_1073, UInt<1>(0h0))
[7806] FIRRTL:374178 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1075 = or(_T_1074, io.core.exception)
[7807] FIRRTL:374179 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1075 :
[7808] FIRRTL:374180 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[2], UInt<1>(0h0)
[7809] FIRRTL:374181 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[2].valid, UInt<1>(0h0)
[7810] FIRRTL:374182 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[3] :
[7816] FIRRTL:374188 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1076 = and(io.core.brupdate.b1.mispredict_mask, uop_12.br_mask)
[7817] FIRRTL:374189 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1077 = neq(_T_1076, UInt<1>(0h0))
[7818] FIRRTL:374190 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1078 = or(_T_1077, io.core.exception)
[7819] FIRRTL:374191 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1078 :
[7820] FIRRTL:374192 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[3], UInt<1>(0h0)
[7821] FIRRTL:374193 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[3].valid, UInt<1>(0h0)
[7822] FIRRTL:374194 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[4] :
[7828] FIRRTL:374200 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1079 = and(io.core.brupdate.b1.mispredict_mask, uop_13.br_mask)
[7829] FIRRTL:374201 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1080 = neq(_T_1079, UInt<1>(0h0))
[7830] FIRRTL:374202 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1081 = or(_T_1080, io.core.exception)
[7831] FIRRTL:374203 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1081 :
[7832] FIRRTL:374204 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[4], UInt<1>(0h0)
[7833] FIRRTL:374205 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[4].valid, UInt<1>(0h0)
[7834] FIRRTL:374206 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[5] :
[7840] FIRRTL:374212 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1082 = and(io.core.brupdate.b1.mispredict_mask, uop_14.br_mask)
[7841] FIRRTL:374213 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1083 = neq(_T_1082, UInt<1>(0h0))
[7842] FIRRTL:374214 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1084 = or(_T_1083, io.core.exception)
[7843] FIRRTL:374215 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1084 :
[7844] FIRRTL:374216 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[5], UInt<1>(0h0)
[7845] FIRRTL:374217 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[5].valid, UInt<1>(0h0)
[7846] FIRRTL:374218 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[6] :
[7852] FIRRTL:374224 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1085 = and(io.core.brupdate.b1.mispredict_mask, uop_15.br_mask)
[7853] FIRRTL:374225 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1086 = neq(_T_1085, UInt<1>(0h0))
[7854] FIRRTL:374226 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1087 = or(_T_1086, io.core.exception)
[7855] FIRRTL:374227 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1087 :
[7856] FIRRTL:374228 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[6], UInt<1>(0h0)
[7857] FIRRTL:374229 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[6].valid, UInt<1>(0h0)
[7858] FIRRTL:374230 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1721:25 KIND:when :: when ldq_valid[7] :
[7864] FIRRTL:374236 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _T_1088 = and(io.core.brupdate.b1.mispredict_mask, uop_16.br_mask)
[7865] FIRRTL:374237 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _T_1089 = neq(_T_1088, UInt<1>(0h0))
[7866] FIRRTL:374238 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _T_1090 = or(_T_1089, io.core.exception)
[7867] FIRRTL:374239 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1725:7 KIND:when :: when _T_1090 :
[7868] FIRRTL:374240 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1726:28 KIND:connect :: connect ldq_valid[7], UInt<1>(0h0)
[7869] FIRRTL:374241 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1727:28 KIND:connect :: connect ldq_addr[7].valid, UInt<1>(0h0)
[7875] FIRRTL:374247 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1749:49 KIND:node :: node commit_store = and(io.core.commit.valids[0], io.core.commit.uops[0].uses_stq)
[7876] FIRRTL:374248 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1750:49 KIND:node :: node commit_load = and(io.core.commit.valids[0], io.core.commit.uops[0].uses_ldq)
[7888] FIRRTL:374260 SRC:<no-source-locator> KIND:else :: else :
[7889] FIRRTL:374261 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1760:31 KIND:when :: when commit_load :
[7910] FIRRTL:374282 SRC:<no-source-locator> KIND:node :: node _T_1107 = bits(ldq_head, 2, 0)
[7911] FIRRTL:374283 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1765:48 KIND:connect :: connect ldq_valid[_T_1107], UInt<1>(0h0)
[7916] FIRRTL:374288 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_1112 = add(ldq_head, UInt<1>(0h1))
[7917] FIRRTL:374289 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _T_1113 = tail(_T_1112, 1)
[7918] FIRRTL:374290 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _T_1114 = bits(_T_1113, 3, 0)
[7919] FIRRTL:374291 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1783:31 KIND:node :: node _T_1115 = mux(commit_load, _T_1114, ldq_head)
[7921] FIRRTL:374293 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1788:19 KIND:connect :: connect ldq_head, _T_1115
[7922] FIRRTL:374294 SRC:<no-source-locator> KIND:node :: node _stq_head_is_fence_T = bits(stq_head, 2, 0)
[7923] FIRRTL:374295 SRC:<no-source-locator> KIND:node :: node _T_1116 = bits(stq_head, 2, 0)
[7924] FIRRTL:374296 SRC:<no-source-locator> KIND:node :: node _T_1117 = bits(stq_head, 2, 0)
[7925] FIRRTL:374297 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1792:29 KIND:node :: node _T_1118 = and(stq_valid[_T_1116], stq_committed[_T_1117])
[7926] FIRRTL:374298 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1793:3 KIND:when :: when _T_1118 :
[7927] FIRRTL:374299 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1795:32 KIND:node :: node _T_1119 = eq(io.dmem.ordered, UInt<1>(0h0))
[7928] FIRRTL:374300 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1795:29 KIND:node :: node _T_1120 = and(stq_uop[_stq_head_is_fence_T].is_fence, _T_1119)
[7929] FIRRTL:374301 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1795:50 KIND:when :: when _T_1120 :
[7931] FIRRTL:374303 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1797:27 KIND:connect :: connect store_needs_order, UInt<1>(0h1)
[7932] FIRRTL:374304 SRC:<no-source-locator> KIND:node :: node _clear_store_T = bits(stq_head, 2, 0)
[7933] FIRRTL:374305 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1799:23 KIND:node :: node _clear_store_T_1 = mux(stq_uop[_stq_head_is_fence_T].is_fence, io.dmem.ordered, stq_succeeded[_clear_store_T])
[7934] FIRRTL:374306 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1799:17 KIND:connect :: connect clear_store, _clear_store_T_1
[7935] FIRRTL:374307 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1803:3 KIND:when :: when clear_store :
[7938] FIRRTL:374310 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_head_T = add(stq_head, UInt<1>(0h1))
[7939] FIRRTL:374311 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:13 KIND:node :: node _stq_head_T_1 = tail(_stq_head_T, 1)
[7940] FIRRTL:374312 SRC:generators/boom/src/main/scala/v4/util/util.scala:227:18 KIND:node :: node _stq_head_T_2 = bits(_stq_head_T_1, 3, 0)
[7941] FIRRTL:374313 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1806:14 KIND:connect :: connect stq_head, _stq_head_T_2
[8003] FIRRTL:374375 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_1123 = and(io.hellacache.req.ready, io.hellacache.req.valid)
[8004] FIRRTL:374376 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1848:35 KIND:when :: when _T_1123 :
[8005] FIRRTL:374377 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1849:19 KIND:connect :: connect hella_req, io.hellacache.req.bits
[8009] FIRRTL:374381 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1852:38 KIND:when :: when _T_1124 :
[8010] FIRRTL:374382 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1853:32 KIND:connect :: connect can_fire_hella_incoming[0], UInt<1>(0h1)
[8083] FIRRTL:374455 SRC:<no-source-locator> KIND:else :: else :
[8084] FIRRTL:374456 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1908:28 KIND:node :: node _T_1143 = eq(hella_state, UInt<3>(0h5))
[8085] FIRRTL:374457 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1908:42 KIND:when :: when _T_1143 :
[8086] FIRRTL:374458 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1909:30 KIND:connect :: connect can_fire_hella_wakeup[0], UInt<1>(0h1)
[8101] FIRRTL:374473 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1928:22 KIND:node :: node _T_1150 = or(_T_1149, io.core.exception)
[8102] FIRRTL:374474 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1929:3 KIND:when :: when _T_1150 :
[8103] FIRRTL:374475 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1930:14 KIND:connect :: connect ldq_head, UInt<1>(0h0)
[8105] FIRRTL:374477 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1933:17 KIND:node :: node _T_1151 = asUInt(reset)
[8106] FIRRTL:374478 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1934:5 KIND:when :: when _T_1151 :
[8107] FIRRTL:374479 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1935:16 KIND:connect :: connect stq_head, UInt<1>(0h0)
[8161] FIRRTL:374533 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[0], UInt<1>(0h0)
[8162] FIRRTL:374534 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[1], UInt<1>(0h0)
[8163] FIRRTL:374535 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[2], UInt<1>(0h0)
[8164] FIRRTL:374536 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[3], UInt<1>(0h0)
[8165] FIRRTL:374537 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[4], UInt<1>(0h0)
[8166] FIRRTL:374538 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[5], UInt<1>(0h0)
[8167] FIRRTL:374539 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[6], UInt<1>(0h0)
[8168] FIRRTL:374540 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1960:30 KIND:connect :: connect ldq_valid[7], UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-LSU-region-0-6-664eff0e43733fd6",
  "work_unit_id": "LSU::region-0-6",
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
