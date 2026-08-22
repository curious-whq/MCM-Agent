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

Task ID: `leaf_abstraction-LSU-region-0-3-085cd341e222b4b9`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.12`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-3`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 61
- logical statements: 19
- mapped/logical source lines: 17
- registers: 1
- physical boundary events: 1

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
   before the colliding real write in `co`. For a finite candidate vector whose unique winner is chosen by an indexed
   linear or rotated order and exposed after a fixed register delay, use
   `indexed_priority_select`. Its `candidate` binds `bit(signal, index_var)`;
   `priority.kind` is `linear_min`, `linear_max`, `cyclic_predecessor`, or
   `cyclic_successor`, with a `pivot` expression on cyclic forms. The cyclic
   forms are strict around the pivot: predecessor visits `pivot-1` downward and
   wraps, while successor visits `pivot+1` upward and wraps, leaving the pivot
   last. `result` names the found/index outputs, `latency_cycles` records the
   exact sampling delay, and unreset result registers use
   `initialization: {"kind":"implicit_unconstrained"}`.
   If a semantic property that you judge **necessary** for a sound/useful
   parent-facing abstraction cannot be faithfully
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

- `LSU::io.core.iresp[0].valid`
  - predicate: `io.core.iresp[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.core.iresp[0].bits.data', 'io.core.iresp[0].bits.fflags.bits', 'io.core.iresp[0].bits.fflags.valid', 'io.core.iresp[0].bits.predicated', 'io.core.iresp[0].bits.uop.bp_debug_if', 'io.core.iresp[0].bits.uop.bp_xcpt_if', 'io.core.iresp[0].bits.uop.br_mask', 'io.core.iresp[0].bits.uop.br_tag', 'io.core.iresp[0].bits.uop.br_type', 'io.core.iresp[0].bits.uop.csr_cmd', 'io.core.iresp[0].bits.uop.debug_fsrc', 'io.core.iresp[0].bits.uop.debug_inst', 'io.core.iresp[0].bits.uop.debug_pc', 'io.core.iresp[0].bits.uop.debug_tsrc', 'io.core.iresp[0].bits.uop.dis_col_sel', 'io.core.iresp[0].bits.uop.dst_rtype', 'io.core.iresp[0].bits.uop.edge_inst', 'io.core.iresp[0].bits.uop.exc_cause', 'io.core.iresp[0].bits.uop.exception', 'io.core.iresp[0].bits.uop.fcn_dw', 'io.core.iresp[0].bits.uop.fcn_op', 'io.core.iresp[0].bits.uop.flush_on_commit', 'io.core.iresp[0].bits.uop.fp_ctrl.div', 'io.core.iresp[0].bits.uop.fp_ctrl.fastpipe', 'io.core.iresp[0].bits.uop.fp_ctrl.fma', 'io.core.iresp[0].bits.uop.fp_ctrl.fromint', 'io.core.iresp[0].bits.uop.fp_ctrl.ldst', 'io.core.iresp[0].bits.uop.fp_ctrl.ren1', 'io.core.iresp[0].bits.uop.fp_ctrl.ren2', 'io.core.iresp[0].bits.uop.fp_ctrl.ren3', 'io.core.iresp[0].bits.uop.fp_ctrl.sqrt', 'io.core.iresp[0].bits.uop.fp_ctrl.swap12', 'io.core.iresp[0].bits.uop.fp_ctrl.swap23', 'io.core.iresp[0].bits.uop.fp_ctrl.toint', 'io.core.iresp[0].bits.uop.fp_ctrl.typeTagIn', 'io.core.iresp[0].bits.uop.fp_ctrl.typeTagOut', 'io.core.iresp[0].bits.uop.fp_ctrl.vec', 'io.core.iresp[0].bits.uop.fp_ctrl.wen', 'io.core.iresp[0].bits.uop.fp_ctrl.wflags', 'io.core.iresp[0].bits.uop.fp_rm', 'io.core.iresp[0].bits.uop.fp_typ', 'io.core.iresp[0].bits.uop.fp_val', 'io.core.iresp[0].bits.uop.frs3_en', 'io.core.iresp[0].bits.uop.ftq_idx', 'io.core.iresp[0].bits.uop.fu_code[0]', 'io.core.iresp[0].bits.uop.fu_code[1]', 'io.core.iresp[0].bits.uop.fu_code[2]', 'io.core.iresp[0].bits.uop.fu_code[3]', 'io.core.iresp[0].bits.uop.fu_code[4]', 'io.core.iresp[0].bits.uop.fu_code[5]', 'io.core.iresp[0].bits.uop.fu_code[6]', 'io.core.iresp[0].bits.uop.fu_code[7]', 'io.core.iresp[0].bits.uop.fu_code[8]', 'io.core.iresp[0].bits.uop.fu_code[9]', 'io.core.iresp[0].bits.uop.imm_packed', 'io.core.iresp[0].bits.uop.imm_rename', 'io.core.iresp[0].bits.uop.imm_sel', 'io.core.iresp[0].bits.uop.inst', 'io.core.iresp[0].bits.uop.iq_type[0]', 'io.core.iresp[0].bits.uop.iq_type[1]', 'io.core.iresp[0].bits.uop.iq_type[2]', 'io.core.iresp[0].bits.uop.iq_type[3]', 'io.core.iresp[0].bits.uop.is_amo', 'io.core.iresp[0].bits.uop.is_eret', 'io.core.iresp[0].bits.uop.is_fence', 'io.core.iresp[0].bits.uop.is_fencei', 'io.core.iresp[0].bits.uop.is_mov', 'io.core.iresp[0].bits.uop.is_rocc', 'io.core.iresp[0].bits.uop.is_rvc', 'io.core.iresp[0].bits.uop.is_sfb', 'io.core.iresp[0].bits.uop.is_sfence', 'io.core.iresp[0].bits.uop.is_sys_pc2epc', 'io.core.iresp[0].bits.uop.is_unique', 'io.core.iresp[0].bits.uop.iw_issued', 'io.core.iresp[0].bits.uop.iw_issued_partial_agen', 'io.core.iresp[0].bits.uop.iw_issued_partial_dgen', 'io.core.iresp[0].bits.uop.iw_p1_bypass_hint', 'io.core.iresp[0].bits.uop.iw_p1_speculative_child', 'io.core.iresp[0].bits.uop.iw_p2_bypass_hint', 'io.core.iresp[0].bits.uop.iw_p2_speculative_child', 'io.core.iresp[0].bits.uop.iw_p3_bypass_hint', 'io.core.iresp[0].bits.uop.ldq_idx', 'io.core.iresp[0].bits.uop.ldst', 'io.core.iresp[0].bits.uop.ldst_is_rs1', 'io.core.iresp[0].bits.uop.lrs1', 'io.core.iresp[0].bits.uop.lrs1_rtype', 'io.core.iresp[0].bits.uop.lrs2', 'io.core.iresp[0].bits.uop.lrs2_rtype', 'io.core.iresp[0].bits.uop.lrs3', 'io.core.iresp[0].bits.uop.mem_cmd', 'io.core.iresp[0].bits.uop.mem_signed', 'io.core.iresp[0].bits.uop.mem_size', 'io.core.iresp[0].bits.uop.op1_sel', 'io.core.iresp[0].bits.uop.op2_sel', 'io.core.iresp[0].bits.uop.pc_lob', 'io.core.iresp[0].bits.uop.pdst', 'io.core.iresp[0].bits.uop.pimm', 'io.core.iresp[0].bits.uop.ppred', 'io.core.iresp[0].bits.uop.ppred_busy', 'io.core.iresp[0].bits.uop.prs1', 'io.core.iresp[0].bits.uop.prs1_busy', 'io.core.iresp[0].bits.uop.prs2', 'io.core.iresp[0].bits.uop.prs2_busy', 'io.core.iresp[0].bits.uop.prs3', 'io.core.iresp[0].bits.uop.prs3_busy', 'io.core.iresp[0].bits.uop.rob_idx', 'io.core.iresp[0].bits.uop.rxq_idx', 'io.core.iresp[0].bits.uop.stale_pdst', 'io.core.iresp[0].bits.uop.stq_idx', 'io.core.iresp[0].bits.uop.taken', 'io.core.iresp[0].bits.uop.uses_ldq', 'io.core.iresp[0].bits.uop.uses_stq', 'io.core.iresp[0].bits.uop.xcpt_ae_if', 'io.core.iresp[0].bits.uop.xcpt_ma_if', 'io.core.iresp[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['io_core_iresp_0_REG']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'io_core_iresp_0_REG', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_data', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

['io_core_iresp_0_REG']

## Environment/frontier signals

['_T_924', '_T_942', '_T_944', '_T_962', '_uop_T_1', 'h0', 'h1', 'h2', 'hffffffff', 'hffffffffffff', 'hffffffffffffff', 'io.core.brupdate.b1.mispredict_mask', 'io.core.brupdate.b1.resolve_mask', 'io.core.exception', 'io.core.iresp[0].bits.data', 'io.core.iresp[0].bits.fflags.bits', 'io.core.iresp[0].bits.fflags.valid', 'io.core.iresp[0].bits.predicated', 'io.core.iresp[0].bits.uop.bp_debug_if', 'io.core.iresp[0].bits.uop.bp_xcpt_if', 'io.core.iresp[0].bits.uop.br_mask', 'io.core.iresp[0].bits.uop.br_tag', 'io.core.iresp[0].bits.uop.br_type', 'io.core.iresp[0].bits.uop.csr_cmd', 'io.core.iresp[0].bits.uop.debug_fsrc', 'io.core.iresp[0].bits.uop.debug_inst', 'io.core.iresp[0].bits.uop.debug_pc', 'io.core.iresp[0].bits.uop.debug_tsrc', 'io.core.iresp[0].bits.uop.dis_col_sel', 'io.core.iresp[0].bits.uop.dst_rtype', 'io.core.iresp[0].bits.uop.edge_inst', 'io.core.iresp[0].bits.uop.exc_cause', 'io.core.iresp[0].bits.uop.exception', 'io.core.iresp[0].bits.uop.fcn_dw', 'io.core.iresp[0].bits.uop.fcn_op', 'io.core.iresp[0].bits.uop.flush_on_commit', 'io.core.iresp[0].bits.uop.fp_ctrl.div', 'io.core.iresp[0].bits.uop.fp_ctrl.fastpipe', 'io.core.iresp[0].bits.uop.fp_ctrl.fma', 'io.core.iresp[0].bits.uop.fp_ctrl.fromint', 'io.core.iresp[0].bits.uop.fp_ctrl.ldst', 'io.core.iresp[0].bits.uop.fp_ctrl.ren1', 'io.core.iresp[0].bits.uop.fp_ctrl.ren2', 'io.core.iresp[0].bits.uop.fp_ctrl.ren3', 'io.core.iresp[0].bits.uop.fp_ctrl.sqrt', 'io.core.iresp[0].bits.uop.fp_ctrl.swap12', 'io.core.iresp[0].bits.uop.fp_ctrl.swap23', 'io.core.iresp[0].bits.uop.fp_ctrl.toint', 'io.core.iresp[0].bits.uop.fp_ctrl.typeTagIn', 'io.core.iresp[0].bits.uop.fp_ctrl.typeTagOut', 'io.core.iresp[0].bits.uop.fp_ctrl.vec', 'io.core.iresp[0].bits.uop.fp_ctrl.wen', 'io.core.iresp[0].bits.uop.fp_ctrl.wflags', 'io.core.iresp[0].bits.uop.fp_rm', 'io.core.iresp[0].bits.uop.fp_typ', 'io.core.iresp[0].bits.uop.fp_val', 'io.core.iresp[0].bits.uop.frs3_en', 'io.core.iresp[0].bits.uop.ftq_idx', 'io.core.iresp[0].bits.uop.fu_code[0]', 'io.core.iresp[0].bits.uop.fu_code[1]', 'io.core.iresp[0].bits.uop.fu_code[2]', 'io.core.iresp[0].bits.uop.fu_code[3]', 'io.core.iresp[0].bits.uop.fu_code[4]', 'io.core.iresp[0].bits.uop.fu_code[5]', 'io.core.iresp[0].bits.uop.fu_code[6]', 'io.core.iresp[0].bits.uop.fu_code[7]', 'io.core.iresp[0].bits.uop.fu_code[8]', 'io.core.iresp[0].bits.uop.fu_code[9]', 'io.core.iresp[0].bits.uop.imm_packed', 'io.core.iresp[0].bits.uop.imm_rename', 'io.core.iresp[0].bits.uop.imm_sel', 'io.core.iresp[0].bits.uop.inst', 'io.core.iresp[0].bits.uop.iq_type[0]', 'io.core.iresp[0].bits.uop.iq_type[1]', 'io.core.iresp[0].bits.uop.iq_type[2]', 'io.core.iresp[0].bits.uop.iq_type[3]', 'io.core.iresp[0].bits.uop.is_amo', 'io.core.iresp[0].bits.uop.is_eret', 'io.core.iresp[0].bits.uop.is_fence', 'io.core.iresp[0].bits.uop.is_fencei', 'io.core.iresp[0].bits.uop.is_mov', 'io.core.iresp[0].bits.uop.is_rocc', 'io.core.iresp[0].bits.uop.is_rvc', 'io.core.iresp[0].bits.uop.is_sfb', 'io.core.iresp[0].bits.uop.is_sfence', 'io.core.iresp[0].bits.uop.is_sys_pc2epc', 'io.core.iresp[0].bits.uop.is_unique', 'io.core.iresp[0].bits.uop.iw_issued', 'io.core.iresp[0].bits.uop.iw_issued_partial_agen', 'io.core.iresp[0].bits.uop.iw_issued_partial_dgen', 'io.core.iresp[0].bits.uop.iw_p1_bypass_hint', 'io.core.iresp[0].bits.uop.iw_p1_speculative_child', 'io.core.iresp[0].bits.uop.iw_p2_bypass_hint', 'io.core.iresp[0].bits.uop.iw_p2_speculative_child', 'io.core.iresp[0].bits.uop.iw_p3_bypass_hint', 'io.core.iresp[0].bits.uop.ldq_idx', 'io.core.iresp[0].bits.uop.ldst', 'io.core.iresp[0].bits.uop.ldst_is_rs1', 'io.core.iresp[0].bits.uop.lrs1', 'io.core.iresp[0].bits.uop.lrs1_rtype', 'io.core.iresp[0].bits.uop.lrs2', 'io.core.iresp[0].bits.uop.lrs2_rtype', 'io.core.iresp[0].bits.uop.lrs3', 'io.core.iresp[0].bits.uop.mem_cmd', 'io.core.iresp[0].bits.uop.mem_signed', 'io.core.iresp[0].bits.uop.mem_size', 'io.core.iresp[0].bits.uop.op1_sel', 'io.core.iresp[0].bits.uop.op2_sel', 'io.core.iresp[0].bits.uop.pc_lob', 'io.core.iresp[0].bits.uop.pdst', 'io.core.iresp[0].bits.uop.pimm', 'io.core.iresp[0].bits.uop.ppred', 'io.core.iresp[0].bits.uop.ppred_busy', 'io.core.iresp[0].bits.uop.prs1', 'io.core.iresp[0].bits.uop.prs1_busy', 'io.core.iresp[0].bits.uop.prs2', 'io.core.iresp[0].bits.uop.prs2_busy', 'io.core.iresp[0].bits.uop.prs3', 'io.core.iresp[0].bits.uop.prs3_busy', 'io.core.iresp[0].bits.uop.rob_idx', 'io.core.iresp[0].bits.uop.rxq_idx', 'io.core.iresp[0].bits.uop.stale_pdst', 'io.core.iresp[0].bits.uop.stq_idx', 'io.core.iresp[0].bits.uop.taken', 'io.core.iresp[0].bits.uop.uses_ldq', 'io.core.iresp[0].bits.uop.uses_stq', 'io.core.iresp[0].bits.uop.xcpt_ae_if', 'io.core.iresp[0].bits.uop.xcpt_ma_if', 'io.core.iresp[0].bits.uop.xcpt_pf_if', 'io.core.iresp[0].valid', 'io_core_iresp_0_REG', 'io_core_iresp_0_out', 'iresp[0].bits.data', 'iresp[0].bits.uop.bp_debug_if', 'iresp[0].bits.uop.bp_xcpt_if', 'iresp[0].bits.uop.br_mask', 'iresp[0].bits.uop.br_tag', 'iresp[0].bits.uop.br_type', 'iresp[0].bits.uop.csr_cmd', 'iresp[0].bits.uop.debug_fsrc', 'iresp[0].bits.uop.debug_inst', 'iresp[0].bits.uop.debug_pc', 'iresp[0].bits.uop.debug_tsrc', 'iresp[0].bits.uop.dis_col_sel', 'iresp[0].bits.uop.dst_rtype', 'iresp[0].bits.uop.edge_inst', 'iresp[0].bits.uop.exc_cause', 'iresp[0].bits.uop.exception', 'iresp[0].bits.uop.fcn_dw', 'iresp[0].bits.uop.fcn_op', 'iresp[0].bits.uop.flush_on_commit', 'iresp[0].bits.uop.fp_ctrl.div', 'iresp[0].bits.uop.fp_ctrl.fastpipe', 'iresp[0].bits.uop.fp_ctrl.fma', 'iresp[0].bits.uop.fp_ctrl.fromint', 'iresp[0].bits.uop.fp_ctrl.ldst', 'iresp[0].bits.uop.fp_ctrl.ren1', 'iresp[0].bits.uop.fp_ctrl.ren2', 'iresp[0].bits.uop.fp_ctrl.ren3', 'iresp[0].bits.uop.fp_ctrl.sqrt', 'iresp[0].bits.uop.fp_ctrl.swap12', 'iresp[0].bits.uop.fp_ctrl.swap23', 'iresp[0].bits.uop.fp_ctrl.toint', 'iresp[0].bits.uop.fp_ctrl.typeTagIn', 'iresp[0].bits.uop.fp_ctrl.typeTagOut', 'iresp[0].bits.uop.fp_ctrl.vec', 'iresp[0].bits.uop.fp_ctrl.wen', 'iresp[0].bits.uop.fp_ctrl.wflags', 'iresp[0].bits.uop.fp_rm', 'iresp[0].bits.uop.fp_typ', 'iresp[0].bits.uop.fp_val', 'iresp[0].bits.uop.frs3_en', 'iresp[0].bits.uop.ftq_idx', 'iresp[0].bits.uop.fu_code[0]', 'iresp[0].bits.uop.fu_code[1]', 'iresp[0].bits.uop.fu_code[2]', 'iresp[0].bits.uop.fu_code[3]', 'iresp[0].bits.uop.fu_code[4]', 'iresp[0].bits.uop.fu_code[5]', 'iresp[0].bits.uop.fu_code[6]', 'iresp[0].bits.uop.fu_code[7]', 'iresp[0].bits.uop.fu_code[8]', 'iresp[0].bits.uop.fu_code[9]', 'iresp[0].bits.uop.imm_packed', 'iresp[0].bits.uop.imm_rename', 'iresp[0].bits.uop.imm_sel', 'iresp[0].bits.uop.inst', 'iresp[0].bits.uop.iq_type[0]', 'iresp[0].bits.uop.iq_type[1]', 'iresp[0].bits.uop.iq_type[2]', 'iresp[0].bits.uop.iq_type[3]', 'iresp[0].bits.uop.is_amo', 'iresp[0].bits.uop.is_eret', 'iresp[0].bits.uop.is_fence', 'iresp[0].bits.uop.is_fencei', 'iresp[0].bits.uop.is_mov', 'iresp[0].bits.uop.is_rocc', 'iresp[0].bits.uop.is_rvc', 'iresp[0].bits.uop.is_sfb', 'iresp[0].bits.uop.is_sfence', 'iresp[0].bits.uop.is_sys_pc2epc', 'iresp[0].bits.uop.is_unique', 'iresp[0].bits.uop.iw_issued', 'iresp[0].bits.uop.iw_issued_partial_agen', 'iresp[0].bits.uop.iw_issued_partial_dgen', 'iresp[0].bits.uop.iw_p1_bypass_hint', 'iresp[0].bits.uop.iw_p1_speculative_child', 'iresp[0].bits.uop.iw_p2_bypass_hint', 'iresp[0].bits.uop.iw_p2_speculative_child', 'iresp[0].bits.uop.iw_p3_bypass_hint', 'iresp[0].bits.uop.ldq_idx', 'iresp[0].bits.uop.ldst', 'iresp[0].bits.uop.ldst_is_rs1', 'iresp[0].bits.uop.lrs1', 'iresp[0].bits.uop.lrs1_rtype', 'iresp[0].bits.uop.lrs2', 'iresp[0].bits.uop.lrs2_rtype', 'iresp[0].bits.uop.lrs3', 'iresp[0].bits.uop.mem_cmd', 'iresp[0].bits.uop.mem_signed', 'iresp[0].bits.uop.mem_size', 'iresp[0].bits.uop.op1_sel', 'iresp[0].bits.uop.op2_sel', 'iresp[0].bits.uop.pc_lob', 'iresp[0].bits.uop.pdst', 'iresp[0].bits.uop.pimm', 'iresp[0].bits.uop.ppred', 'iresp[0].bits.uop.ppred_busy', 'iresp[0].bits.uop.prs1', 'iresp[0].bits.uop.prs1_busy', 'iresp[0].bits.uop.prs2', 'iresp[0].bits.uop.prs2_busy', 'iresp[0].bits.uop.prs3', 'iresp[0].bits.uop.prs3_busy', 'iresp[0].bits.uop.rob_idx', 'iresp[0].bits.uop.rxq_idx', 'iresp[0].bits.uop.stale_pdst', 'iresp[0].bits.uop.stq_idx', 'iresp[0].bits.uop.taken', 'iresp[0].bits.uop.uses_ldq', 'iresp[0].bits.uop.uses_stq', 'iresp[0].bits.uop.xcpt_ae_if', 'iresp[0].bits.uop.xcpt_ma_if', 'iresp[0].bits.uop.xcpt_pf_if', 'iresp[0].valid', 'resp.data', 'resp.uop.stq_idx', 'resp.uop.uses_ldq', 'resp.uop.uses_stq', 'size_1', 'stq_uop[*]', 'uop', 'wb_ldst_forward_e[0].uop', 'wb_ldst_forward_e[0].uop.mem_signed', 'wb_ldst_forward_ld_addr[0]']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1508-1510
```scala
    fresp(w).bits  := DontCare
    io.core.iresp(w) := (if (enableFastLoadUse) iresp(w) else RegNext(
      UpdateBrMask(io.core.brupdate, io.core.exception, iresp(w))))
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1570-1572
```scala

        iresp(w).bits.uop  := uop
        fresp(w).bits.uop  := uop
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1576-1578
```scala

        iresp(w).bits.data := resp.data
        fresp(w).valid     := send_fresp
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1599-1602
```scala
        iresp(w).valid     := true.B
        iresp(w).bits.uop  := uop
        iresp(w).bits.data := resp.data
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1644-1648
```scala
      fresp(w).valid := (forward_uop.dst_rtype === RT_FLT)
      iresp(w).bits.uop  := forward_uop
      fresp(w).bits.uop  := forward_uop
      iresp(w).bits.data := loadgen.data
      fresp(w).bits.data := loadgen.data
```

### generators/boom/src/main/scala/v4/util/util.scala:60-62
```scala
  def apply(brupdate: BrUpdateInfo, flush: Bool, uop_mask: UInt): Bool = {
    return maskMatch(brupdate.b1.mispredict_mask, uop_mask) || flush
  }
```

### generators/boom/src/main/scala/v4/util/util.scala:96-98
```scala
   def apply(brupdate: BrUpdateInfo, br_mask: UInt): UInt = {
     return br_mask & ~brupdate.b1.resolve_mask
   }
```

### generators/boom/src/main/scala/v4/util/util.scala:113-117
```scala
  def apply[T <: boom.v4.common.HasBoomUOP](brupdate: BrUpdateInfo, flush: Bool, bundle: Valid[T]): Valid[T] = {
    val out = WireInit(bundle)
    out.bits.uop.br_mask := GetNewBrMask(brupdate, bundle.bits.uop.br_mask)
    out.valid := bundle.valid && !IsKilledByBranch(brupdate, flush, bundle.bits.uop.br_mask)
    out
```

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
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

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[6568] FIRRTL:372940 SRC:generators/boom/src/main/scala/v4/util/util.scala:114:23 KIND:connect :: connect io_core_iresp_0_out, iresp[0]
[6569] FIRRTL:372941 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _io_core_iresp_0_out_bits_uop_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[6570] FIRRTL:372942 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _io_core_iresp_0_out_bits_uop_br_mask_T_1 = and(iresp[0].bits.uop.br_mask, _io_core_iresp_0_out_bits_uop_br_mask_T)
[6571] FIRRTL:372943 SRC:generators/boom/src/main/scala/v4/util/util.scala:115:26 KIND:connect :: connect io_core_iresp_0_out.bits.uop.br_mask, _io_core_iresp_0_out_bits_uop_br_mask_T_1
[6572] FIRRTL:372944 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _io_core_iresp_0_out_valid_T = and(io.core.brupdate.b1.mispredict_mask, iresp[0].bits.uop.br_mask)
[6573] FIRRTL:372945 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _io_core_iresp_0_out_valid_T_1 = neq(_io_core_iresp_0_out_valid_T, UInt<1>(0h0))
[6574] FIRRTL:372946 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _io_core_iresp_0_out_valid_T_2 = or(_io_core_iresp_0_out_valid_T_1, io.core.exception)
[6575] FIRRTL:372947 SRC:generators/boom/src/main/scala/v4/util/util.scala:116:34 KIND:node :: node _io_core_iresp_0_out_valid_T_3 = eq(_io_core_iresp_0_out_valid_T_2, UInt<1>(0h0))
[6576] FIRRTL:372948 SRC:generators/boom/src/main/scala/v4/util/util.scala:116:31 KIND:node :: node _io_core_iresp_0_out_valid_T_4 = and(iresp[0].valid, _io_core_iresp_0_out_valid_T_3)
[6577] FIRRTL:372949 SRC:generators/boom/src/main/scala/v4/util/util.scala:116:15 KIND:connect :: connect io_core_iresp_0_out.valid, _io_core_iresp_0_out_valid_T_4
[6579] FIRRTL:372951 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1509:70 KIND:connect :: connect io_core_iresp_0_REG, io_core_iresp_0_out
[6580] FIRRTL:372952 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1509:22 KIND:connect :: connect io.core.iresp[0], io_core_iresp_0_REG
[6949] FIRRTL:373321 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1571:28 KIND:connect :: connect iresp[0].bits.uop, uop
[6952] FIRRTL:373324 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1577:28 KIND:connect :: connect iresp[0].bits.data, resp.data
[6975] FIRRTL:373347 SRC:<no-source-locator> KIND:node :: node _uop_T_1 = bits(resp.uop.stq_idx, 2, 0)
[6987] FIRRTL:373359 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1600:28 KIND:connect :: connect iresp[0].bits.uop, stq_uop[_uop_T_1]
[6988] FIRRTL:373360 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1601:28 KIND:connect :: connect iresp[0].bits.data, resp.data
[7055] FIRRTL:373427 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1645:26 KIND:connect :: connect iresp[0].bits.uop, wb_ldst_forward_e[0].uop
[7057] FIRRTL:373429 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _iresp_0_bits_data_shifted_T = bits(wb_ldst_forward_ld_addr[0], 2, 2)
[7058] FIRRTL:373430 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _iresp_0_bits_data_shifted_T_1 = bits(_T_962, 63, 32)
[7059] FIRRTL:373431 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _iresp_0_bits_data_shifted_T_2 = bits(_T_962, 31, 0)
[7060] FIRRTL:373432 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node iresp_0_bits_data_shifted = mux(_iresp_0_bits_data_shifted_T, _iresp_0_bits_data_shifted_T_1, _iresp_0_bits_data_shifted_T_2)
[7061] FIRRTL:373433 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node iresp_0_bits_data_doZero = and(UInt<1>(0h0), UInt<1>(0h0))
[7062] FIRRTL:373434 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node iresp_0_bits_data_zeroed = mux(iresp_0_bits_data_doZero, UInt<1>(0h0), iresp_0_bits_data_shifted)
[7063] FIRRTL:373435 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _iresp_0_bits_data_T = eq(size_1, UInt<2>(0h2))
[7064] FIRRTL:373436 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _iresp_0_bits_data_T_1 = or(_iresp_0_bits_data_T, iresp_0_bits_data_doZero)
[7065] FIRRTL:373437 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _iresp_0_bits_data_T_2 = bits(iresp_0_bits_data_zeroed, 31, 31)
[7066] FIRRTL:373438 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _iresp_0_bits_data_T_3 = and(wb_ldst_forward_e[0].uop.mem_signed, _iresp_0_bits_data_T_2)
[7067] FIRRTL:373439 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _iresp_0_bits_data_T_4 = mux(_iresp_0_bits_data_T_3, UInt<32>(0hffffffff), UInt<32>(0h0))
[7068] FIRRTL:373440 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _iresp_0_bits_data_T_5 = bits(_T_962, 63, 32)
[7069] FIRRTL:373441 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _iresp_0_bits_data_T_6 = mux(_iresp_0_bits_data_T_1, _iresp_0_bits_data_T_4, _iresp_0_bits_data_T_5)
[7070] FIRRTL:373442 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _iresp_0_bits_data_T_7 = cat(_iresp_0_bits_data_T_6, iresp_0_bits_data_zeroed)
[7071] FIRRTL:373443 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _iresp_0_bits_data_shifted_T_3 = bits(wb_ldst_forward_ld_addr[0], 1, 1)
[7072] FIRRTL:373444 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _iresp_0_bits_data_shifted_T_4 = bits(_iresp_0_bits_data_T_7, 31, 16)
[7073] FIRRTL:373445 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _iresp_0_bits_data_shifted_T_5 = bits(_iresp_0_bits_data_T_7, 15, 0)
[7074] FIRRTL:373446 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node iresp_0_bits_data_shifted_1 = mux(_iresp_0_bits_data_shifted_T_3, _iresp_0_bits_data_shifted_T_4, _iresp_0_bits_data_shifted_T_5)
[7075] FIRRTL:373447 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node iresp_0_bits_data_doZero_1 = and(UInt<1>(0h0), UInt<1>(0h0))
[7076] FIRRTL:373448 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node iresp_0_bits_data_zeroed_1 = mux(iresp_0_bits_data_doZero_1, UInt<1>(0h0), iresp_0_bits_data_shifted_1)
[7077] FIRRTL:373449 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _iresp_0_bits_data_T_8 = eq(size_1, UInt<1>(0h1))
[7078] FIRRTL:373450 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _iresp_0_bits_data_T_9 = or(_iresp_0_bits_data_T_8, iresp_0_bits_data_doZero_1)
[7079] FIRRTL:373451 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _iresp_0_bits_data_T_10 = bits(iresp_0_bits_data_zeroed_1, 15, 15)
[7080] FIRRTL:373452 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _iresp_0_bits_data_T_11 = and(wb_ldst_forward_e[0].uop.mem_signed, _iresp_0_bits_data_T_10)
[7081] FIRRTL:373453 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _iresp_0_bits_data_T_12 = mux(_iresp_0_bits_data_T_11, UInt<48>(0hffffffffffff), UInt<48>(0h0))
[7082] FIRRTL:373454 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _iresp_0_bits_data_T_13 = bits(_iresp_0_bits_data_T_7, 63, 16)
[7083] FIRRTL:373455 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _iresp_0_bits_data_T_14 = mux(_iresp_0_bits_data_T_9, _iresp_0_bits_data_T_12, _iresp_0_bits_data_T_13)
[7084] FIRRTL:373456 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _iresp_0_bits_data_T_15 = cat(_iresp_0_bits_data_T_14, iresp_0_bits_data_zeroed_1)
[7085] FIRRTL:373457 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _iresp_0_bits_data_shifted_T_6 = bits(wb_ldst_forward_ld_addr[0], 0, 0)
[7086] FIRRTL:373458 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _iresp_0_bits_data_shifted_T_7 = bits(_iresp_0_bits_data_T_15, 15, 8)
[7087] FIRRTL:373459 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _iresp_0_bits_data_shifted_T_8 = bits(_iresp_0_bits_data_T_15, 7, 0)
[7088] FIRRTL:373460 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node iresp_0_bits_data_shifted_2 = mux(_iresp_0_bits_data_shifted_T_6, _iresp_0_bits_data_shifted_T_7, _iresp_0_bits_data_shifted_T_8)
[7089] FIRRTL:373461 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node iresp_0_bits_data_doZero_2 = and(UInt<1>(0h1), UInt<1>(0h0))
[7090] FIRRTL:373462 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node iresp_0_bits_data_zeroed_2 = mux(iresp_0_bits_data_doZero_2, UInt<1>(0h0), iresp_0_bits_data_shifted_2)
[7091] FIRRTL:373463 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _iresp_0_bits_data_T_16 = eq(size_1, UInt<1>(0h0))
[7092] FIRRTL:373464 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _iresp_0_bits_data_T_17 = or(_iresp_0_bits_data_T_16, iresp_0_bits_data_doZero_2)
[7093] FIRRTL:373465 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _iresp_0_bits_data_T_18 = bits(iresp_0_bits_data_zeroed_2, 7, 7)
[7094] FIRRTL:373466 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _iresp_0_bits_data_T_19 = and(wb_ldst_forward_e[0].uop.mem_signed, _iresp_0_bits_data_T_18)
[7095] FIRRTL:373467 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _iresp_0_bits_data_T_20 = mux(_iresp_0_bits_data_T_19, UInt<56>(0hffffffffffffff), UInt<56>(0h0))
[7096] FIRRTL:373468 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _iresp_0_bits_data_T_21 = bits(_iresp_0_bits_data_T_15, 63, 8)
[7097] FIRRTL:373469 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _iresp_0_bits_data_T_22 = mux(_iresp_0_bits_data_T_17, _iresp_0_bits_data_T_20, _iresp_0_bits_data_T_21)
[7098] FIRRTL:373470 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _iresp_0_bits_data_T_23 = cat(_iresp_0_bits_data_T_22, iresp_0_bits_data_zeroed_2)
[7099] FIRRTL:373471 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1647:26 KIND:connect :: connect iresp[0].bits.data, _iresp_0_bits_data_T_23
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
  "task_id": "leaf_abstraction-LSU-region-0-3-085cd341e222b4b9",
  "work_unit_id": "LSU::region-0-3",
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
