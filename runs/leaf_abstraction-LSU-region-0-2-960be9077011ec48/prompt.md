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

Task ID: `leaf_abstraction-LSU-region-0-2-960be9077011ec48`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.12`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-2`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 56
- logical statements: 17
- mapped/logical source lines: 15
- registers: 2
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

- `LSU::io.core.fresp[0].valid`
  - predicate: `io.core.fresp[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.core.fresp[0].bits.data', 'io.core.fresp[0].bits.fflags.bits', 'io.core.fresp[0].bits.fflags.valid', 'io.core.fresp[0].bits.predicated', 'io.core.fresp[0].bits.uop.bp_debug_if', 'io.core.fresp[0].bits.uop.bp_xcpt_if', 'io.core.fresp[0].bits.uop.br_mask', 'io.core.fresp[0].bits.uop.br_tag', 'io.core.fresp[0].bits.uop.br_type', 'io.core.fresp[0].bits.uop.csr_cmd', 'io.core.fresp[0].bits.uop.debug_fsrc', 'io.core.fresp[0].bits.uop.debug_inst', 'io.core.fresp[0].bits.uop.debug_pc', 'io.core.fresp[0].bits.uop.debug_tsrc', 'io.core.fresp[0].bits.uop.dis_col_sel', 'io.core.fresp[0].bits.uop.dst_rtype', 'io.core.fresp[0].bits.uop.edge_inst', 'io.core.fresp[0].bits.uop.exc_cause', 'io.core.fresp[0].bits.uop.exception', 'io.core.fresp[0].bits.uop.fcn_dw', 'io.core.fresp[0].bits.uop.fcn_op', 'io.core.fresp[0].bits.uop.flush_on_commit', 'io.core.fresp[0].bits.uop.fp_ctrl.div', 'io.core.fresp[0].bits.uop.fp_ctrl.fastpipe', 'io.core.fresp[0].bits.uop.fp_ctrl.fma', 'io.core.fresp[0].bits.uop.fp_ctrl.fromint', 'io.core.fresp[0].bits.uop.fp_ctrl.ldst', 'io.core.fresp[0].bits.uop.fp_ctrl.ren1', 'io.core.fresp[0].bits.uop.fp_ctrl.ren2', 'io.core.fresp[0].bits.uop.fp_ctrl.ren3', 'io.core.fresp[0].bits.uop.fp_ctrl.sqrt', 'io.core.fresp[0].bits.uop.fp_ctrl.swap12', 'io.core.fresp[0].bits.uop.fp_ctrl.swap23', 'io.core.fresp[0].bits.uop.fp_ctrl.toint', 'io.core.fresp[0].bits.uop.fp_ctrl.typeTagIn', 'io.core.fresp[0].bits.uop.fp_ctrl.typeTagOut', 'io.core.fresp[0].bits.uop.fp_ctrl.vec', 'io.core.fresp[0].bits.uop.fp_ctrl.wen', 'io.core.fresp[0].bits.uop.fp_ctrl.wflags', 'io.core.fresp[0].bits.uop.fp_rm', 'io.core.fresp[0].bits.uop.fp_typ', 'io.core.fresp[0].bits.uop.fp_val', 'io.core.fresp[0].bits.uop.frs3_en', 'io.core.fresp[0].bits.uop.ftq_idx', 'io.core.fresp[0].bits.uop.fu_code[0]', 'io.core.fresp[0].bits.uop.fu_code[1]', 'io.core.fresp[0].bits.uop.fu_code[2]', 'io.core.fresp[0].bits.uop.fu_code[3]', 'io.core.fresp[0].bits.uop.fu_code[4]', 'io.core.fresp[0].bits.uop.fu_code[5]', 'io.core.fresp[0].bits.uop.fu_code[6]', 'io.core.fresp[0].bits.uop.fu_code[7]', 'io.core.fresp[0].bits.uop.fu_code[8]', 'io.core.fresp[0].bits.uop.fu_code[9]', 'io.core.fresp[0].bits.uop.imm_packed', 'io.core.fresp[0].bits.uop.imm_rename', 'io.core.fresp[0].bits.uop.imm_sel', 'io.core.fresp[0].bits.uop.inst', 'io.core.fresp[0].bits.uop.iq_type[0]', 'io.core.fresp[0].bits.uop.iq_type[1]', 'io.core.fresp[0].bits.uop.iq_type[2]', 'io.core.fresp[0].bits.uop.iq_type[3]', 'io.core.fresp[0].bits.uop.is_amo', 'io.core.fresp[0].bits.uop.is_eret', 'io.core.fresp[0].bits.uop.is_fence', 'io.core.fresp[0].bits.uop.is_fencei', 'io.core.fresp[0].bits.uop.is_mov', 'io.core.fresp[0].bits.uop.is_rocc', 'io.core.fresp[0].bits.uop.is_rvc', 'io.core.fresp[0].bits.uop.is_sfb', 'io.core.fresp[0].bits.uop.is_sfence', 'io.core.fresp[0].bits.uop.is_sys_pc2epc', 'io.core.fresp[0].bits.uop.is_unique', 'io.core.fresp[0].bits.uop.iw_issued', 'io.core.fresp[0].bits.uop.iw_issued_partial_agen', 'io.core.fresp[0].bits.uop.iw_issued_partial_dgen', 'io.core.fresp[0].bits.uop.iw_p1_bypass_hint', 'io.core.fresp[0].bits.uop.iw_p1_speculative_child', 'io.core.fresp[0].bits.uop.iw_p2_bypass_hint', 'io.core.fresp[0].bits.uop.iw_p2_speculative_child', 'io.core.fresp[0].bits.uop.iw_p3_bypass_hint', 'io.core.fresp[0].bits.uop.ldq_idx', 'io.core.fresp[0].bits.uop.ldst', 'io.core.fresp[0].bits.uop.ldst_is_rs1', 'io.core.fresp[0].bits.uop.lrs1', 'io.core.fresp[0].bits.uop.lrs1_rtype', 'io.core.fresp[0].bits.uop.lrs2', 'io.core.fresp[0].bits.uop.lrs2_rtype', 'io.core.fresp[0].bits.uop.lrs3', 'io.core.fresp[0].bits.uop.mem_cmd', 'io.core.fresp[0].bits.uop.mem_signed', 'io.core.fresp[0].bits.uop.mem_size', 'io.core.fresp[0].bits.uop.op1_sel', 'io.core.fresp[0].bits.uop.op2_sel', 'io.core.fresp[0].bits.uop.pc_lob', 'io.core.fresp[0].bits.uop.pdst', 'io.core.fresp[0].bits.uop.pimm', 'io.core.fresp[0].bits.uop.ppred', 'io.core.fresp[0].bits.uop.ppred_busy', 'io.core.fresp[0].bits.uop.prs1', 'io.core.fresp[0].bits.uop.prs1_busy', 'io.core.fresp[0].bits.uop.prs2', 'io.core.fresp[0].bits.uop.prs2_busy', 'io.core.fresp[0].bits.uop.prs3', 'io.core.fresp[0].bits.uop.prs3_busy', 'io.core.fresp[0].bits.uop.rob_idx', 'io.core.fresp[0].bits.uop.rxq_idx', 'io.core.fresp[0].bits.uop.stale_pdst', 'io.core.fresp[0].bits.uop.stq_idx', 'io.core.fresp[0].bits.uop.taken', 'io.core.fresp[0].bits.uop.uses_ldq', 'io.core.fresp[0].bits.uop.uses_stq', 'io.core.fresp[0].bits.uop.xcpt_ae_if', 'io.core.fresp[0].bits.uop.xcpt_ma_if', 'io.core.fresp[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['ldq_uop', 'w1', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_data', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

['ldq_uop', 'wb_ldst_forward_e_REG']

## Environment/frontier signals

['_T_27', '_T_924', '_T_942', '_T_944', '_T_962', 'dis_uops[0].bits.ldq_idx', 'fresp[0].bits.data', 'fresp[0].bits.uop.bp_debug_if', 'fresp[0].bits.uop.bp_xcpt_if', 'fresp[0].bits.uop.br_mask', 'fresp[0].bits.uop.br_tag', 'fresp[0].bits.uop.br_type', 'fresp[0].bits.uop.csr_cmd', 'fresp[0].bits.uop.debug_fsrc', 'fresp[0].bits.uop.debug_inst', 'fresp[0].bits.uop.debug_pc', 'fresp[0].bits.uop.debug_tsrc', 'fresp[0].bits.uop.dis_col_sel', 'fresp[0].bits.uop.dst_rtype', 'fresp[0].bits.uop.edge_inst', 'fresp[0].bits.uop.exc_cause', 'fresp[0].bits.uop.exception', 'fresp[0].bits.uop.fcn_dw', 'fresp[0].bits.uop.fcn_op', 'fresp[0].bits.uop.flush_on_commit', 'fresp[0].bits.uop.fp_ctrl.div', 'fresp[0].bits.uop.fp_ctrl.fastpipe', 'fresp[0].bits.uop.fp_ctrl.fma', 'fresp[0].bits.uop.fp_ctrl.fromint', 'fresp[0].bits.uop.fp_ctrl.ldst', 'fresp[0].bits.uop.fp_ctrl.ren1', 'fresp[0].bits.uop.fp_ctrl.ren2', 'fresp[0].bits.uop.fp_ctrl.ren3', 'fresp[0].bits.uop.fp_ctrl.sqrt', 'fresp[0].bits.uop.fp_ctrl.swap12', 'fresp[0].bits.uop.fp_ctrl.swap23', 'fresp[0].bits.uop.fp_ctrl.toint', 'fresp[0].bits.uop.fp_ctrl.typeTagIn', 'fresp[0].bits.uop.fp_ctrl.typeTagOut', 'fresp[0].bits.uop.fp_ctrl.vec', 'fresp[0].bits.uop.fp_ctrl.wen', 'fresp[0].bits.uop.fp_ctrl.wflags', 'fresp[0].bits.uop.fp_rm', 'fresp[0].bits.uop.fp_typ', 'fresp[0].bits.uop.fp_val', 'fresp[0].bits.uop.frs3_en', 'fresp[0].bits.uop.ftq_idx', 'fresp[0].bits.uop.fu_code[0]', 'fresp[0].bits.uop.fu_code[1]', 'fresp[0].bits.uop.fu_code[2]', 'fresp[0].bits.uop.fu_code[3]', 'fresp[0].bits.uop.fu_code[4]', 'fresp[0].bits.uop.fu_code[5]', 'fresp[0].bits.uop.fu_code[6]', 'fresp[0].bits.uop.fu_code[7]', 'fresp[0].bits.uop.fu_code[8]', 'fresp[0].bits.uop.fu_code[9]', 'fresp[0].bits.uop.imm_packed', 'fresp[0].bits.uop.imm_rename', 'fresp[0].bits.uop.imm_sel', 'fresp[0].bits.uop.inst', 'fresp[0].bits.uop.iq_type[0]', 'fresp[0].bits.uop.iq_type[1]', 'fresp[0].bits.uop.iq_type[2]', 'fresp[0].bits.uop.iq_type[3]', 'fresp[0].bits.uop.is_amo', 'fresp[0].bits.uop.is_eret', 'fresp[0].bits.uop.is_fence', 'fresp[0].bits.uop.is_fencei', 'fresp[0].bits.uop.is_mov', 'fresp[0].bits.uop.is_rocc', 'fresp[0].bits.uop.is_rvc', 'fresp[0].bits.uop.is_sfb', 'fresp[0].bits.uop.is_sfence', 'fresp[0].bits.uop.is_sys_pc2epc', 'fresp[0].bits.uop.is_unique', 'fresp[0].bits.uop.iw_issued', 'fresp[0].bits.uop.iw_issued_partial_agen', 'fresp[0].bits.uop.iw_issued_partial_dgen', 'fresp[0].bits.uop.iw_p1_bypass_hint', 'fresp[0].bits.uop.iw_p1_speculative_child', 'fresp[0].bits.uop.iw_p2_bypass_hint', 'fresp[0].bits.uop.iw_p2_speculative_child', 'fresp[0].bits.uop.iw_p3_bypass_hint', 'fresp[0].bits.uop.ldq_idx', 'fresp[0].bits.uop.ldst', 'fresp[0].bits.uop.ldst_is_rs1', 'fresp[0].bits.uop.lrs1', 'fresp[0].bits.uop.lrs1_rtype', 'fresp[0].bits.uop.lrs2', 'fresp[0].bits.uop.lrs2_rtype', 'fresp[0].bits.uop.lrs3', 'fresp[0].bits.uop.mem_cmd', 'fresp[0].bits.uop.mem_signed', 'fresp[0].bits.uop.mem_size', 'fresp[0].bits.uop.op1_sel', 'fresp[0].bits.uop.op2_sel', 'fresp[0].bits.uop.pc_lob', 'fresp[0].bits.uop.pdst', 'fresp[0].bits.uop.pimm', 'fresp[0].bits.uop.ppred', 'fresp[0].bits.uop.ppred_busy', 'fresp[0].bits.uop.prs1', 'fresp[0].bits.uop.prs1_busy', 'fresp[0].bits.uop.prs2', 'fresp[0].bits.uop.prs2_busy', 'fresp[0].bits.uop.prs3', 'fresp[0].bits.uop.prs3_busy', 'fresp[0].bits.uop.rob_idx', 'fresp[0].bits.uop.rxq_idx', 'fresp[0].bits.uop.stale_pdst', 'fresp[0].bits.uop.stq_idx', 'fresp[0].bits.uop.taken', 'fresp[0].bits.uop.uses_ldq', 'fresp[0].bits.uop.uses_stq', 'fresp[0].bits.uop.xcpt_ae_if', 'fresp[0].bits.uop.xcpt_ma_if', 'fresp[0].bits.uop.xcpt_pf_if', 'h0', 'h1', 'h2', 'hffffffff', 'hffffffffffff', 'hffffffffffffff', 'io.core.brupdate.b1.resolve_mask', 'io.core.fresp[0].bits.data', 'io.core.fresp[0].bits.fflags.bits', 'io.core.fresp[0].bits.fflags.valid', 'io.core.fresp[0].bits.predicated', 'io.core.fresp[0].bits.uop.bp_debug_if', 'io.core.fresp[0].bits.uop.bp_xcpt_if', 'io.core.fresp[0].bits.uop.br_mask', 'io.core.fresp[0].bits.uop.br_tag', 'io.core.fresp[0].bits.uop.br_type', 'io.core.fresp[0].bits.uop.csr_cmd', 'io.core.fresp[0].bits.uop.debug_fsrc', 'io.core.fresp[0].bits.uop.debug_inst', 'io.core.fresp[0].bits.uop.debug_pc', 'io.core.fresp[0].bits.uop.debug_tsrc', 'io.core.fresp[0].bits.uop.dis_col_sel', 'io.core.fresp[0].bits.uop.dst_rtype', 'io.core.fresp[0].bits.uop.edge_inst', 'io.core.fresp[0].bits.uop.exc_cause', 'io.core.fresp[0].bits.uop.exception', 'io.core.fresp[0].bits.uop.fcn_dw', 'io.core.fresp[0].bits.uop.fcn_op', 'io.core.fresp[0].bits.uop.flush_on_commit', 'io.core.fresp[0].bits.uop.fp_ctrl.div', 'io.core.fresp[0].bits.uop.fp_ctrl.fastpipe', 'io.core.fresp[0].bits.uop.fp_ctrl.fma', 'io.core.fresp[0].bits.uop.fp_ctrl.fromint', 'io.core.fresp[0].bits.uop.fp_ctrl.ldst', 'io.core.fresp[0].bits.uop.fp_ctrl.ren1', 'io.core.fresp[0].bits.uop.fp_ctrl.ren2', 'io.core.fresp[0].bits.uop.fp_ctrl.ren3', 'io.core.fresp[0].bits.uop.fp_ctrl.sqrt', 'io.core.fresp[0].bits.uop.fp_ctrl.swap12', 'io.core.fresp[0].bits.uop.fp_ctrl.swap23', 'io.core.fresp[0].bits.uop.fp_ctrl.toint', 'io.core.fresp[0].bits.uop.fp_ctrl.typeTagIn', 'io.core.fresp[0].bits.uop.fp_ctrl.typeTagOut', 'io.core.fresp[0].bits.uop.fp_ctrl.vec', 'io.core.fresp[0].bits.uop.fp_ctrl.wen', 'io.core.fresp[0].bits.uop.fp_ctrl.wflags', 'io.core.fresp[0].bits.uop.fp_rm', 'io.core.fresp[0].bits.uop.fp_typ', 'io.core.fresp[0].bits.uop.fp_val', 'io.core.fresp[0].bits.uop.frs3_en', 'io.core.fresp[0].bits.uop.ftq_idx', 'io.core.fresp[0].bits.uop.fu_code[0]', 'io.core.fresp[0].bits.uop.fu_code[1]', 'io.core.fresp[0].bits.uop.fu_code[2]', 'io.core.fresp[0].bits.uop.fu_code[3]', 'io.core.fresp[0].bits.uop.fu_code[4]', 'io.core.fresp[0].bits.uop.fu_code[5]', 'io.core.fresp[0].bits.uop.fu_code[6]', 'io.core.fresp[0].bits.uop.fu_code[7]', 'io.core.fresp[0].bits.uop.fu_code[8]', 'io.core.fresp[0].bits.uop.fu_code[9]', 'io.core.fresp[0].bits.uop.imm_packed', 'io.core.fresp[0].bits.uop.imm_rename', 'io.core.fresp[0].bits.uop.imm_sel', 'io.core.fresp[0].bits.uop.inst', 'io.core.fresp[0].bits.uop.iq_type[0]', 'io.core.fresp[0].bits.uop.iq_type[1]', 'io.core.fresp[0].bits.uop.iq_type[2]', 'io.core.fresp[0].bits.uop.iq_type[3]', 'io.core.fresp[0].bits.uop.is_amo', 'io.core.fresp[0].bits.uop.is_eret', 'io.core.fresp[0].bits.uop.is_fence', 'io.core.fresp[0].bits.uop.is_fencei', 'io.core.fresp[0].bits.uop.is_mov', 'io.core.fresp[0].bits.uop.is_rocc', 'io.core.fresp[0].bits.uop.is_rvc', 'io.core.fresp[0].bits.uop.is_sfb', 'io.core.fresp[0].bits.uop.is_sfence', 'io.core.fresp[0].bits.uop.is_sys_pc2epc', 'io.core.fresp[0].bits.uop.is_unique', 'io.core.fresp[0].bits.uop.iw_issued', 'io.core.fresp[0].bits.uop.iw_issued_partial_agen', 'io.core.fresp[0].bits.uop.iw_issued_partial_dgen', 'io.core.fresp[0].bits.uop.iw_p1_bypass_hint', 'io.core.fresp[0].bits.uop.iw_p1_speculative_child', 'io.core.fresp[0].bits.uop.iw_p2_bypass_hint', 'io.core.fresp[0].bits.uop.iw_p2_speculative_child', 'io.core.fresp[0].bits.uop.iw_p3_bypass_hint', 'io.core.fresp[0].bits.uop.ldq_idx', 'io.core.fresp[0].bits.uop.ldst', 'io.core.fresp[0].bits.uop.ldst_is_rs1', 'io.core.fresp[0].bits.uop.lrs1', 'io.core.fresp[0].bits.uop.lrs1_rtype', 'io.core.fresp[0].bits.uop.lrs2', 'io.core.fresp[0].bits.uop.lrs2_rtype', 'io.core.fresp[0].bits.uop.lrs3', 'io.core.fresp[0].bits.uop.mem_cmd', 'io.core.fresp[0].bits.uop.mem_signed', 'io.core.fresp[0].bits.uop.mem_size', 'io.core.fresp[0].bits.uop.op1_sel', 'io.core.fresp[0].bits.uop.op2_sel', 'io.core.fresp[0].bits.uop.pc_lob', 'io.core.fresp[0].bits.uop.pdst', 'io.core.fresp[0].bits.uop.pimm', 'io.core.fresp[0].bits.uop.ppred', 'io.core.fresp[0].bits.uop.ppred_busy', 'io.core.fresp[0].bits.uop.prs1', 'io.core.fresp[0].bits.uop.prs1_busy', 'io.core.fresp[0].bits.uop.prs2', 'io.core.fresp[0].bits.uop.prs2_busy', 'io.core.fresp[0].bits.uop.prs3', 'io.core.fresp[0].bits.uop.prs3_busy', 'io.core.fresp[0].bits.uop.rob_idx', 'io.core.fresp[0].bits.uop.rxq_idx', 'io.core.fresp[0].bits.uop.stale_pdst', 'io.core.fresp[0].bits.uop.stq_idx', 'io.core.fresp[0].bits.uop.taken', 'io.core.fresp[0].bits.uop.uses_ldq', 'io.core.fresp[0].bits.uop.uses_stq', 'io.core.fresp[0].bits.uop.xcpt_ae_if', 'io.core.fresp[0].bits.uop.xcpt_ma_if', 'io.core.fresp[0].bits.uop.xcpt_pf_if', 'io.core.fresp[0].valid', 'lcam_ldq_idx[0]', 'ldq_uop[*]', 'ldq_uop_out', 'resp.data', 'resp.uop.uses_ldq', 'size_1', 'uop', 'wb_ldst_forward_e[0].uop', 'wb_ldst_forward_e[0].uop.mem_signed', 'wb_ldst_forward_e_out', 'wb_ldst_forward_ld_addr[0]']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/lsu.scala:238-240
```scala
    e.valid                    := ldq_valid              (idx)
    e.bits.uop                 := ldq_uop                (idx)
    e.bits.addr                := ldq_addr               (idx)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:396-398
```scala
      ldq_valid          (ldq_idx)       := !IsKilledByBranch(io.core.brupdate, io.core.exception, dis_uops(w).bits)
      ldq_uop            (ldq_idx)       := UpdateBrMask(io.core.brupdate, dis_uops(w).bits)
      ldq_addr           (ldq_idx).valid := false.B
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1175-1177
```scala
  val wb_ldst_forward_valid    = Wire(Vec(lsuWidth, Bool()))
  val wb_ldst_forward_e        = widthMap(w => RegNext(UpdateBrMask(io.core.brupdate, ldq_read(lcam_ldq_idx(w)).bits)))
  val wb_ldst_forward_ldq_idx  = SafeRegNext(lcam_ldq_idx)
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1510-1512
```scala
      UpdateBrMask(io.core.brupdate, io.core.exception, iresp(w))))
    io.core.fresp(w) := fresp(w)
  }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1571-1573
```scala
        iresp(w).bits.uop  := uop
        fresp(w).bits.uop  := uop
        iresp(w).valid     := send_iresp
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1578-1580
```scala
        fresp(w).valid     := send_fresp
        fresp(w).bits.data := resp.data
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1645-1649
```scala
      iresp(w).bits.uop  := forward_uop
      fresp(w).bits.uop  := forward_uop
      iresp(w).bits.data := loadgen.data
      fresp(w).bits.data := loadgen.data
```

### generators/boom/src/main/scala/v4/util/util.scala:96-98
```scala
   def apply(brupdate: BrUpdateInfo, br_mask: UInt): UInt = {
     return br_mask & ~brupdate.b1.resolve_mask
   }
```

### generators/boom/src/main/scala/v4/util/util.scala:108-111
```scala
  def apply[T <: boom.v4.common.HasBoomUOP](brupdate: BrUpdateInfo, bundle: T): T = {
    val out = WireInit(bundle)
    out.uop.br_mask := GetNewBrMask(brupdate, bundle.uop.br_mask)
    out
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
[230] FIRRTL:366602 SRC:<no-source-locator> KIND:node :: node _T_29 = bits(dis_uops[0].bits.ldq_idx, 2, 0)
[236] FIRRTL:366608 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:397:42 KIND:connect :: connect ldq_uop[_T_29], ldq_uop_out
[3798] FIRRTL:370170 SRC:<no-source-locator> KIND:node :: node _wb_ldst_forward_e_e_bits_uop_T = bits(lcam_ldq_idx[0], 2, 0)
[3799] FIRRTL:370171 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:239:32 KIND:connect :: connect wb_ldst_forward_e_e.bits.uop, ldq_uop[_wb_ldst_forward_e_e_bits_uop_T]
[3825] FIRRTL:370197 SRC:generators/boom/src/main/scala/v4/util/util.scala:109:23 KIND:connect :: connect wb_ldst_forward_e_out, wb_ldst_forward_e_e.bits
[3826] FIRRTL:370198 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _wb_ldst_forward_e_out_uop_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[3827] FIRRTL:370199 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _wb_ldst_forward_e_out_uop_br_mask_T_1 = and(wb_ldst_forward_e_e.bits.uop.br_mask, _wb_ldst_forward_e_out_uop_br_mask_T)
[3828] FIRRTL:370200 SRC:generators/boom/src/main/scala/v4/util/util.scala:110:21 KIND:connect :: connect wb_ldst_forward_e_out.uop.br_mask, _wb_ldst_forward_e_out_uop_br_mask_T_1
[3830] FIRRTL:370202 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1176:55 KIND:connect :: connect wb_ldst_forward_e_REG, wb_ldst_forward_e_out
[6581] FIRRTL:372953 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1511:22 KIND:connect :: connect io.core.fresp[0], fresp[0]
[6950] FIRRTL:373322 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1572:28 KIND:connect :: connect fresp[0].bits.uop, uop
[6954] FIRRTL:373326 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1579:28 KIND:connect :: connect fresp[0].bits.data, resp.data
[7056] FIRRTL:373428 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1646:26 KIND:connect :: connect fresp[0].bits.uop, wb_ldst_forward_e[0].uop
[7100] FIRRTL:373472 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _fresp_0_bits_data_shifted_T = bits(wb_ldst_forward_ld_addr[0], 2, 2)
[7101] FIRRTL:373473 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _fresp_0_bits_data_shifted_T_1 = bits(_T_962, 63, 32)
[7102] FIRRTL:373474 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _fresp_0_bits_data_shifted_T_2 = bits(_T_962, 31, 0)
[7103] FIRRTL:373475 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node fresp_0_bits_data_shifted = mux(_fresp_0_bits_data_shifted_T, _fresp_0_bits_data_shifted_T_1, _fresp_0_bits_data_shifted_T_2)
[7104] FIRRTL:373476 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node fresp_0_bits_data_doZero = and(UInt<1>(0h0), UInt<1>(0h0))
[7105] FIRRTL:373477 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node fresp_0_bits_data_zeroed = mux(fresp_0_bits_data_doZero, UInt<1>(0h0), fresp_0_bits_data_shifted)
[7106] FIRRTL:373478 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _fresp_0_bits_data_T = eq(size_1, UInt<2>(0h2))
[7107] FIRRTL:373479 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _fresp_0_bits_data_T_1 = or(_fresp_0_bits_data_T, fresp_0_bits_data_doZero)
[7108] FIRRTL:373480 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _fresp_0_bits_data_T_2 = bits(fresp_0_bits_data_zeroed, 31, 31)
[7109] FIRRTL:373481 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _fresp_0_bits_data_T_3 = and(wb_ldst_forward_e[0].uop.mem_signed, _fresp_0_bits_data_T_2)
[7110] FIRRTL:373482 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _fresp_0_bits_data_T_4 = mux(_fresp_0_bits_data_T_3, UInt<32>(0hffffffff), UInt<32>(0h0))
[7111] FIRRTL:373483 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _fresp_0_bits_data_T_5 = bits(_T_962, 63, 32)
[7112] FIRRTL:373484 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _fresp_0_bits_data_T_6 = mux(_fresp_0_bits_data_T_1, _fresp_0_bits_data_T_4, _fresp_0_bits_data_T_5)
[7113] FIRRTL:373485 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _fresp_0_bits_data_T_7 = cat(_fresp_0_bits_data_T_6, fresp_0_bits_data_zeroed)
[7114] FIRRTL:373486 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _fresp_0_bits_data_shifted_T_3 = bits(wb_ldst_forward_ld_addr[0], 1, 1)
[7115] FIRRTL:373487 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _fresp_0_bits_data_shifted_T_4 = bits(_fresp_0_bits_data_T_7, 31, 16)
[7116] FIRRTL:373488 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _fresp_0_bits_data_shifted_T_5 = bits(_fresp_0_bits_data_T_7, 15, 0)
[7117] FIRRTL:373489 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node fresp_0_bits_data_shifted_1 = mux(_fresp_0_bits_data_shifted_T_3, _fresp_0_bits_data_shifted_T_4, _fresp_0_bits_data_shifted_T_5)
[7118] FIRRTL:373490 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node fresp_0_bits_data_doZero_1 = and(UInt<1>(0h0), UInt<1>(0h0))
[7119] FIRRTL:373491 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node fresp_0_bits_data_zeroed_1 = mux(fresp_0_bits_data_doZero_1, UInt<1>(0h0), fresp_0_bits_data_shifted_1)
[7120] FIRRTL:373492 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _fresp_0_bits_data_T_8 = eq(size_1, UInt<1>(0h1))
[7121] FIRRTL:373493 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _fresp_0_bits_data_T_9 = or(_fresp_0_bits_data_T_8, fresp_0_bits_data_doZero_1)
[7122] FIRRTL:373494 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _fresp_0_bits_data_T_10 = bits(fresp_0_bits_data_zeroed_1, 15, 15)
[7123] FIRRTL:373495 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _fresp_0_bits_data_T_11 = and(wb_ldst_forward_e[0].uop.mem_signed, _fresp_0_bits_data_T_10)
[7124] FIRRTL:373496 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _fresp_0_bits_data_T_12 = mux(_fresp_0_bits_data_T_11, UInt<48>(0hffffffffffff), UInt<48>(0h0))
[7125] FIRRTL:373497 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _fresp_0_bits_data_T_13 = bits(_fresp_0_bits_data_T_7, 63, 16)
[7126] FIRRTL:373498 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _fresp_0_bits_data_T_14 = mux(_fresp_0_bits_data_T_9, _fresp_0_bits_data_T_12, _fresp_0_bits_data_T_13)
[7127] FIRRTL:373499 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _fresp_0_bits_data_T_15 = cat(_fresp_0_bits_data_T_14, fresp_0_bits_data_zeroed_1)
[7128] FIRRTL:373500 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _fresp_0_bits_data_shifted_T_6 = bits(wb_ldst_forward_ld_addr[0], 0, 0)
[7129] FIRRTL:373501 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _fresp_0_bits_data_shifted_T_7 = bits(_fresp_0_bits_data_T_15, 15, 8)
[7130] FIRRTL:373502 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _fresp_0_bits_data_shifted_T_8 = bits(_fresp_0_bits_data_T_15, 7, 0)
[7131] FIRRTL:373503 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node fresp_0_bits_data_shifted_2 = mux(_fresp_0_bits_data_shifted_T_6, _fresp_0_bits_data_shifted_T_7, _fresp_0_bits_data_shifted_T_8)
[7132] FIRRTL:373504 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node fresp_0_bits_data_doZero_2 = and(UInt<1>(0h1), UInt<1>(0h0))
[7133] FIRRTL:373505 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node fresp_0_bits_data_zeroed_2 = mux(fresp_0_bits_data_doZero_2, UInt<1>(0h0), fresp_0_bits_data_shifted_2)
[7134] FIRRTL:373506 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _fresp_0_bits_data_T_16 = eq(size_1, UInt<1>(0h0))
[7135] FIRRTL:373507 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _fresp_0_bits_data_T_17 = or(_fresp_0_bits_data_T_16, fresp_0_bits_data_doZero_2)
[7136] FIRRTL:373508 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _fresp_0_bits_data_T_18 = bits(fresp_0_bits_data_zeroed_2, 7, 7)
[7137] FIRRTL:373509 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _fresp_0_bits_data_T_19 = and(wb_ldst_forward_e[0].uop.mem_signed, _fresp_0_bits_data_T_18)
[7138] FIRRTL:373510 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _fresp_0_bits_data_T_20 = mux(_fresp_0_bits_data_T_19, UInt<56>(0hffffffffffffff), UInt<56>(0h0))
[7139] FIRRTL:373511 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _fresp_0_bits_data_T_21 = bits(_fresp_0_bits_data_T_15, 63, 8)
[7140] FIRRTL:373512 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _fresp_0_bits_data_T_22 = mux(_fresp_0_bits_data_T_17, _fresp_0_bits_data_T_20, _fresp_0_bits_data_T_21)
[7141] FIRRTL:373513 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _fresp_0_bits_data_T_23 = cat(_fresp_0_bits_data_T_22, fresp_0_bits_data_zeroed_2)
[7142] FIRRTL:373514 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1648:26 KIND:connect :: connect fresp[0].bits.data, _fresp_0_bits_data_T_23
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
  "task_id": "leaf_abstraction-LSU-region-0-2-960be9077011ec48",
  "work_unit_id": "LSU::region-0-2",
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
