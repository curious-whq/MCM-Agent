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

Task ID: `leaf_abstraction-LSU-region-0-4-9d9375b011581ad1`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-4`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 78
- logical statements: 26
- mapped/logical source lines: 22
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

- `LSU::io.core.lxcpt.valid`
  - predicate: `io.core.lxcpt.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.core.lxcpt.bits.badvaddr', 'io.core.lxcpt.bits.cause', 'io.core.lxcpt.bits.uop.bp_debug_if', 'io.core.lxcpt.bits.uop.bp_xcpt_if', 'io.core.lxcpt.bits.uop.br_mask', 'io.core.lxcpt.bits.uop.br_tag', 'io.core.lxcpt.bits.uop.br_type', 'io.core.lxcpt.bits.uop.csr_cmd', 'io.core.lxcpt.bits.uop.debug_fsrc', 'io.core.lxcpt.bits.uop.debug_inst', 'io.core.lxcpt.bits.uop.debug_pc', 'io.core.lxcpt.bits.uop.debug_tsrc', 'io.core.lxcpt.bits.uop.dis_col_sel', 'io.core.lxcpt.bits.uop.dst_rtype', 'io.core.lxcpt.bits.uop.edge_inst', 'io.core.lxcpt.bits.uop.exc_cause', 'io.core.lxcpt.bits.uop.exception', 'io.core.lxcpt.bits.uop.fcn_dw', 'io.core.lxcpt.bits.uop.fcn_op', 'io.core.lxcpt.bits.uop.flush_on_commit', 'io.core.lxcpt.bits.uop.fp_ctrl.div', 'io.core.lxcpt.bits.uop.fp_ctrl.fastpipe', 'io.core.lxcpt.bits.uop.fp_ctrl.fma', 'io.core.lxcpt.bits.uop.fp_ctrl.fromint', 'io.core.lxcpt.bits.uop.fp_ctrl.ldst', 'io.core.lxcpt.bits.uop.fp_ctrl.ren1', 'io.core.lxcpt.bits.uop.fp_ctrl.ren2', 'io.core.lxcpt.bits.uop.fp_ctrl.ren3', 'io.core.lxcpt.bits.uop.fp_ctrl.sqrt', 'io.core.lxcpt.bits.uop.fp_ctrl.swap12', 'io.core.lxcpt.bits.uop.fp_ctrl.swap23', 'io.core.lxcpt.bits.uop.fp_ctrl.toint', 'io.core.lxcpt.bits.uop.fp_ctrl.typeTagIn', 'io.core.lxcpt.bits.uop.fp_ctrl.typeTagOut', 'io.core.lxcpt.bits.uop.fp_ctrl.vec', 'io.core.lxcpt.bits.uop.fp_ctrl.wen', 'io.core.lxcpt.bits.uop.fp_ctrl.wflags', 'io.core.lxcpt.bits.uop.fp_rm', 'io.core.lxcpt.bits.uop.fp_typ', 'io.core.lxcpt.bits.uop.fp_val', 'io.core.lxcpt.bits.uop.frs3_en', 'io.core.lxcpt.bits.uop.ftq_idx', 'io.core.lxcpt.bits.uop.fu_code[0]', 'io.core.lxcpt.bits.uop.fu_code[1]', 'io.core.lxcpt.bits.uop.fu_code[2]', 'io.core.lxcpt.bits.uop.fu_code[3]', 'io.core.lxcpt.bits.uop.fu_code[4]', 'io.core.lxcpt.bits.uop.fu_code[5]', 'io.core.lxcpt.bits.uop.fu_code[6]', 'io.core.lxcpt.bits.uop.fu_code[7]', 'io.core.lxcpt.bits.uop.fu_code[8]', 'io.core.lxcpt.bits.uop.fu_code[9]', 'io.core.lxcpt.bits.uop.imm_packed', 'io.core.lxcpt.bits.uop.imm_rename', 'io.core.lxcpt.bits.uop.imm_sel', 'io.core.lxcpt.bits.uop.inst', 'io.core.lxcpt.bits.uop.iq_type[0]', 'io.core.lxcpt.bits.uop.iq_type[1]', 'io.core.lxcpt.bits.uop.iq_type[2]', 'io.core.lxcpt.bits.uop.iq_type[3]', 'io.core.lxcpt.bits.uop.is_amo', 'io.core.lxcpt.bits.uop.is_eret', 'io.core.lxcpt.bits.uop.is_fence', 'io.core.lxcpt.bits.uop.is_fencei', 'io.core.lxcpt.bits.uop.is_mov', 'io.core.lxcpt.bits.uop.is_rocc', 'io.core.lxcpt.bits.uop.is_rvc', 'io.core.lxcpt.bits.uop.is_sfb', 'io.core.lxcpt.bits.uop.is_sfence', 'io.core.lxcpt.bits.uop.is_sys_pc2epc', 'io.core.lxcpt.bits.uop.is_unique', 'io.core.lxcpt.bits.uop.iw_issued', 'io.core.lxcpt.bits.uop.iw_issued_partial_agen', 'io.core.lxcpt.bits.uop.iw_issued_partial_dgen', 'io.core.lxcpt.bits.uop.iw_p1_bypass_hint', 'io.core.lxcpt.bits.uop.iw_p1_speculative_child', 'io.core.lxcpt.bits.uop.iw_p2_bypass_hint', 'io.core.lxcpt.bits.uop.iw_p2_speculative_child', 'io.core.lxcpt.bits.uop.iw_p3_bypass_hint', 'io.core.lxcpt.bits.uop.ldq_idx', 'io.core.lxcpt.bits.uop.ldst', 'io.core.lxcpt.bits.uop.ldst_is_rs1', 'io.core.lxcpt.bits.uop.lrs1', 'io.core.lxcpt.bits.uop.lrs1_rtype', 'io.core.lxcpt.bits.uop.lrs2', 'io.core.lxcpt.bits.uop.lrs2_rtype', 'io.core.lxcpt.bits.uop.lrs3', 'io.core.lxcpt.bits.uop.mem_cmd', 'io.core.lxcpt.bits.uop.mem_signed', 'io.core.lxcpt.bits.uop.mem_size', 'io.core.lxcpt.bits.uop.op1_sel', 'io.core.lxcpt.bits.uop.op2_sel', 'io.core.lxcpt.bits.uop.pc_lob', 'io.core.lxcpt.bits.uop.pdst', 'io.core.lxcpt.bits.uop.pimm', 'io.core.lxcpt.bits.uop.ppred', 'io.core.lxcpt.bits.uop.ppred_busy', 'io.core.lxcpt.bits.uop.prs1', 'io.core.lxcpt.bits.uop.prs1_busy', 'io.core.lxcpt.bits.uop.prs2', 'io.core.lxcpt.bits.uop.prs2_busy', 'io.core.lxcpt.bits.uop.prs3', 'io.core.lxcpt.bits.uop.prs3_busy', 'io.core.lxcpt.bits.uop.rob_idx', 'io.core.lxcpt.bits.uop.rxq_idx', 'io.core.lxcpt.bits.uop.stale_pdst', 'io.core.lxcpt.bits.uop.stq_idx', 'io.core.lxcpt.bits.uop.taken', 'io.core.lxcpt.bits.uop.uses_ldq', 'io.core.lxcpt.bits.uop.uses_stq', 'io.core.lxcpt.bits.uop.xcpt_ae_if', 'io.core.lxcpt.bits.uop.xcpt_ma_if', 'io.core.lxcpt.bits.uop.xcpt_pf_if']
  - immediate registers: ['r_xcpt', 'r_xcpt_valid']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_causes', 'mem_xcpt_uops', 'mem_xcpt_vaddrs', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 'r_xcpt', 'r_xcpt_valid', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

['r_xcpt', 'r_xcpt_valid']

## Environment/frontier signals

['_l_idx_T', '_l_idx_T_1', '_l_idx_T_2', '_l_idx_T_3', '_l_idx_T_4', '_l_idx_T_5', '_l_idx_T_6', '_l_idx_T_7', '_ld_xcpt_uop_T', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'io.core.brupdate.b1.mispredict_mask', 'io.core.brupdate.b1.resolve_mask', 'io.core.exception', 'io.core.lxcpt.bits.badvaddr', 'io.core.lxcpt.bits.cause', 'io.core.lxcpt.bits.uop.bp_debug_if', 'io.core.lxcpt.bits.uop.bp_xcpt_if', 'io.core.lxcpt.bits.uop.br_mask', 'io.core.lxcpt.bits.uop.br_tag', 'io.core.lxcpt.bits.uop.br_type', 'io.core.lxcpt.bits.uop.csr_cmd', 'io.core.lxcpt.bits.uop.debug_fsrc', 'io.core.lxcpt.bits.uop.debug_inst', 'io.core.lxcpt.bits.uop.debug_pc', 'io.core.lxcpt.bits.uop.debug_tsrc', 'io.core.lxcpt.bits.uop.dis_col_sel', 'io.core.lxcpt.bits.uop.dst_rtype', 'io.core.lxcpt.bits.uop.edge_inst', 'io.core.lxcpt.bits.uop.exc_cause', 'io.core.lxcpt.bits.uop.exception', 'io.core.lxcpt.bits.uop.fcn_dw', 'io.core.lxcpt.bits.uop.fcn_op', 'io.core.lxcpt.bits.uop.flush_on_commit', 'io.core.lxcpt.bits.uop.fp_ctrl.div', 'io.core.lxcpt.bits.uop.fp_ctrl.fastpipe', 'io.core.lxcpt.bits.uop.fp_ctrl.fma', 'io.core.lxcpt.bits.uop.fp_ctrl.fromint', 'io.core.lxcpt.bits.uop.fp_ctrl.ldst', 'io.core.lxcpt.bits.uop.fp_ctrl.ren1', 'io.core.lxcpt.bits.uop.fp_ctrl.ren2', 'io.core.lxcpt.bits.uop.fp_ctrl.ren3', 'io.core.lxcpt.bits.uop.fp_ctrl.sqrt', 'io.core.lxcpt.bits.uop.fp_ctrl.swap12', 'io.core.lxcpt.bits.uop.fp_ctrl.swap23', 'io.core.lxcpt.bits.uop.fp_ctrl.toint', 'io.core.lxcpt.bits.uop.fp_ctrl.typeTagIn', 'io.core.lxcpt.bits.uop.fp_ctrl.typeTagOut', 'io.core.lxcpt.bits.uop.fp_ctrl.vec', 'io.core.lxcpt.bits.uop.fp_ctrl.wen', 'io.core.lxcpt.bits.uop.fp_ctrl.wflags', 'io.core.lxcpt.bits.uop.fp_rm', 'io.core.lxcpt.bits.uop.fp_typ', 'io.core.lxcpt.bits.uop.fp_val', 'io.core.lxcpt.bits.uop.frs3_en', 'io.core.lxcpt.bits.uop.ftq_idx', 'io.core.lxcpt.bits.uop.fu_code[0]', 'io.core.lxcpt.bits.uop.fu_code[1]', 'io.core.lxcpt.bits.uop.fu_code[2]', 'io.core.lxcpt.bits.uop.fu_code[3]', 'io.core.lxcpt.bits.uop.fu_code[4]', 'io.core.lxcpt.bits.uop.fu_code[5]', 'io.core.lxcpt.bits.uop.fu_code[6]', 'io.core.lxcpt.bits.uop.fu_code[7]', 'io.core.lxcpt.bits.uop.fu_code[8]', 'io.core.lxcpt.bits.uop.fu_code[9]', 'io.core.lxcpt.bits.uop.imm_packed', 'io.core.lxcpt.bits.uop.imm_rename', 'io.core.lxcpt.bits.uop.imm_sel', 'io.core.lxcpt.bits.uop.inst', 'io.core.lxcpt.bits.uop.iq_type[0]', 'io.core.lxcpt.bits.uop.iq_type[1]', 'io.core.lxcpt.bits.uop.iq_type[2]', 'io.core.lxcpt.bits.uop.iq_type[3]', 'io.core.lxcpt.bits.uop.is_amo', 'io.core.lxcpt.bits.uop.is_eret', 'io.core.lxcpt.bits.uop.is_fence', 'io.core.lxcpt.bits.uop.is_fencei', 'io.core.lxcpt.bits.uop.is_mov', 'io.core.lxcpt.bits.uop.is_rocc', 'io.core.lxcpt.bits.uop.is_rvc', 'io.core.lxcpt.bits.uop.is_sfb', 'io.core.lxcpt.bits.uop.is_sfence', 'io.core.lxcpt.bits.uop.is_sys_pc2epc', 'io.core.lxcpt.bits.uop.is_unique', 'io.core.lxcpt.bits.uop.iw_issued', 'io.core.lxcpt.bits.uop.iw_issued_partial_agen', 'io.core.lxcpt.bits.uop.iw_issued_partial_dgen', 'io.core.lxcpt.bits.uop.iw_p1_bypass_hint', 'io.core.lxcpt.bits.uop.iw_p1_speculative_child', 'io.core.lxcpt.bits.uop.iw_p2_bypass_hint', 'io.core.lxcpt.bits.uop.iw_p2_speculative_child', 'io.core.lxcpt.bits.uop.iw_p3_bypass_hint', 'io.core.lxcpt.bits.uop.ldq_idx', 'io.core.lxcpt.bits.uop.ldst', 'io.core.lxcpt.bits.uop.ldst_is_rs1', 'io.core.lxcpt.bits.uop.lrs1', 'io.core.lxcpt.bits.uop.lrs1_rtype', 'io.core.lxcpt.bits.uop.lrs2', 'io.core.lxcpt.bits.uop.lrs2_rtype', 'io.core.lxcpt.bits.uop.lrs3', 'io.core.lxcpt.bits.uop.mem_cmd', 'io.core.lxcpt.bits.uop.mem_signed', 'io.core.lxcpt.bits.uop.mem_size', 'io.core.lxcpt.bits.uop.op1_sel', 'io.core.lxcpt.bits.uop.op2_sel', 'io.core.lxcpt.bits.uop.pc_lob', 'io.core.lxcpt.bits.uop.pdst', 'io.core.lxcpt.bits.uop.pimm', 'io.core.lxcpt.bits.uop.ppred', 'io.core.lxcpt.bits.uop.ppred_busy', 'io.core.lxcpt.bits.uop.prs1', 'io.core.lxcpt.bits.uop.prs1_busy', 'io.core.lxcpt.bits.uop.prs2', 'io.core.lxcpt.bits.uop.prs2_busy', 'io.core.lxcpt.bits.uop.prs3', 'io.core.lxcpt.bits.uop.prs3_busy', 'io.core.lxcpt.bits.uop.rob_idx', 'io.core.lxcpt.bits.uop.rxq_idx', 'io.core.lxcpt.bits.uop.stale_pdst', 'io.core.lxcpt.bits.uop.stq_idx', 'io.core.lxcpt.bits.uop.taken', 'io.core.lxcpt.bits.uop.uses_ldq', 'io.core.lxcpt.bits.uop.uses_stq', 'io.core.lxcpt.bits.uop.xcpt_ae_if', 'io.core.lxcpt.bits.uop.xcpt_ma_if', 'io.core.lxcpt.bits.uop.xcpt_pf_if', 'io.core.lxcpt.valid', 'io.core.rob_head_idx', 'l_idx_head_base', 'l_idx_head_overflow', 'ld_xcpt_uop', 'ld_xcpt_uop.rob_idx', 'ld_xcpt_valid_hi_hi', 'ld_xcpt_valid_hi_hi_1', 'ld_xcpt_valid_hi_lo', 'ld_xcpt_valid_hi_lo_1', 'ld_xcpt_valid_lo_hi', 'ld_xcpt_valid_lo_hi_1', 'ld_xcpt_valid_lo_lo', 'ld_xcpt_valid_lo_lo_1', 'mem_xcpt_cause', 'mem_xcpt_causes[0]', 'mem_xcpt_uop', 'mem_xcpt_vaddr', 'mem_xcpt_vaddrs[0]', 'mem_xcpt_valid', 'r_xcpt', 'r_xcpt_valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[2176] FIRRTL:368548 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:812:18 KIND:connect :: connect mem_xcpt_cause, mem_xcpt_causes[0]
[2177] FIRRTL:368549 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:813:18 KIND:connect :: connect mem_xcpt_uop, mem_xcpt_uops[0]
[2178] FIRRTL:368550 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:814:18 KIND:connect :: connect mem_xcpt_vaddr, mem_xcpt_vaddrs[0]
[6118] FIRRTL:372490 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:39 KIND:node :: node ld_xcpt_valid_lo = cat(ld_xcpt_valid_lo_hi, ld_xcpt_valid_lo_lo)
[6121] FIRRTL:372493 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:39 KIND:node :: node ld_xcpt_valid_hi = cat(ld_xcpt_valid_hi_hi, ld_xcpt_valid_hi_lo)
[6122] FIRRTL:372494 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:39 KIND:node :: node _ld_xcpt_valid_T = cat(ld_xcpt_valid_hi, ld_xcpt_valid_lo)
[6125] FIRRTL:372497 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:58 KIND:node :: node ld_xcpt_valid_lo_1 = cat(ld_xcpt_valid_lo_hi_1, ld_xcpt_valid_lo_lo_1)
[6128] FIRRTL:372500 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:58 KIND:node :: node ld_xcpt_valid_hi_1 = cat(ld_xcpt_valid_hi_hi_1, ld_xcpt_valid_hi_lo_1)
[6129] FIRRTL:372501 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:58 KIND:node :: node _ld_xcpt_valid_T_1 = cat(ld_xcpt_valid_hi_1, ld_xcpt_valid_lo_1)
[6130] FIRRTL:372502 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:46 KIND:node :: node _ld_xcpt_valid_T_2 = and(_ld_xcpt_valid_T, _ld_xcpt_valid_T_1)
[6131] FIRRTL:372503 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1458:66 KIND:node :: node ld_xcpt_valid = neq(_ld_xcpt_valid_T_2, UInt<1>(0h0))
[6142] FIRRTL:372514 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T = geq(UInt<1>(0h0), l_idx_head_base)
[6143] FIRRTL:372515 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_0 = and(_l_idx_T, _l_idx_base_temp_vec_T)
[6144] FIRRTL:372516 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_1 = geq(UInt<1>(0h1), l_idx_head_base)
[6145] FIRRTL:372517 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_1 = and(_l_idx_T_1, _l_idx_base_temp_vec_T_1)
[6146] FIRRTL:372518 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_2 = geq(UInt<2>(0h2), l_idx_head_base)
[6147] FIRRTL:372519 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_2 = and(_l_idx_T_2, _l_idx_base_temp_vec_T_2)
[6148] FIRRTL:372520 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_3 = geq(UInt<2>(0h3), l_idx_head_base)
[6149] FIRRTL:372521 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_3 = and(_l_idx_T_3, _l_idx_base_temp_vec_T_3)
[6150] FIRRTL:372522 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_4 = geq(UInt<3>(0h4), l_idx_head_base)
[6151] FIRRTL:372523 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_4 = and(_l_idx_T_4, _l_idx_base_temp_vec_T_4)
[6152] FIRRTL:372524 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_5 = geq(UInt<3>(0h5), l_idx_head_base)
[6153] FIRRTL:372525 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_5 = and(_l_idx_T_5, _l_idx_base_temp_vec_T_5)
[6154] FIRRTL:372526 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_6 = geq(UInt<3>(0h6), l_idx_head_base)
[6155] FIRRTL:372527 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_6 = and(_l_idx_T_6, _l_idx_base_temp_vec_T_6)
[6156] FIRRTL:372528 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:72 KIND:node :: node _l_idx_base_temp_vec_T_7 = geq(UInt<3>(0h7), l_idx_head_base)
[6157] FIRRTL:372529 SRC:generators/boom/src/main/scala/v4/util/util.scala:371:65 KIND:node :: node l_idx_base_temp_vec_7 = and(_l_idx_T_7, _l_idx_base_temp_vec_T_7)
[6158] FIRRTL:372530 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T = mux(_l_idx_T_6, UInt<4>(0he), UInt<4>(0hf))
[6159] FIRRTL:372531 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_1 = mux(_l_idx_T_5, UInt<4>(0hd), _l_idx_base_idx_T)
[6160] FIRRTL:372532 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_2 = mux(_l_idx_T_4, UInt<4>(0hc), _l_idx_base_idx_T_1)
[6161] FIRRTL:372533 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_3 = mux(_l_idx_T_3, UInt<4>(0hb), _l_idx_base_idx_T_2)
[6162] FIRRTL:372534 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_4 = mux(_l_idx_T_2, UInt<4>(0ha), _l_idx_base_idx_T_3)
[6163] FIRRTL:372535 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_5 = mux(_l_idx_T_1, UInt<4>(0h9), _l_idx_base_idx_T_4)
[6164] FIRRTL:372536 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_6 = mux(_l_idx_T, UInt<4>(0h8), _l_idx_base_idx_T_5)
[6165] FIRRTL:372537 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_7 = mux(l_idx_base_temp_vec_7, UInt<3>(0h7), _l_idx_base_idx_T_6)
[6166] FIRRTL:372538 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_8 = mux(l_idx_base_temp_vec_6, UInt<3>(0h6), _l_idx_base_idx_T_7)
[6167] FIRRTL:372539 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_9 = mux(l_idx_base_temp_vec_5, UInt<3>(0h5), _l_idx_base_idx_T_8)
[6168] FIRRTL:372540 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_10 = mux(l_idx_base_temp_vec_4, UInt<3>(0h4), _l_idx_base_idx_T_9)
[6169] FIRRTL:372541 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_11 = mux(l_idx_base_temp_vec_3, UInt<2>(0h3), _l_idx_base_idx_T_10)
[6170] FIRRTL:372542 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_12 = mux(l_idx_base_temp_vec_2, UInt<2>(0h2), _l_idx_base_idx_T_11)
[6171] FIRRTL:372543 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node _l_idx_base_idx_T_13 = mux(l_idx_base_temp_vec_1, UInt<1>(0h1), _l_idx_base_idx_T_12)
[6172] FIRRTL:372544 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node l_idx_base_idx = mux(l_idx_base_temp_vec_0, UInt<1>(0h0), _l_idx_base_idx_T_13)
[6173] FIRRTL:372545 SRC:generators/boom/src/main/scala/v4/util/util.scala:373:8 KIND:node :: node l_idx_base = bits(l_idx_base_idx, 2, 0)
[6174] FIRRTL:372546 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:29 KIND:node :: node _l_idx_overflow_T = geq(l_idx_base, l_idx_head_base)
[6175] FIRRTL:372547 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:58 KIND:node :: node _l_idx_overflow_T_1 = not(l_idx_head_overflow)
[6176] FIRRTL:372548 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1998:23 KIND:node :: node l_idx_overflow = mux(_l_idx_overflow_T, l_idx_head_overflow, _l_idx_overflow_T_1)
[6177] FIRRTL:372549 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1999:8 KIND:node :: node l_idx = cat(l_idx_overflow, l_idx_base)
[6178] FIRRTL:372550 SRC:<no-source-locator> KIND:node :: node _ld_xcpt_uop_T = bits(l_idx, 2, 0)
[6181] FIRRTL:372553 SRC:generators/boom/src/main/scala/v4/util/util.scala:383:52 KIND:node :: node _use_mem_xcpt_T = lt(mem_xcpt_uop.rob_idx, ld_xcpt_uop.rob_idx)
[6182] FIRRTL:372554 SRC:generators/boom/src/main/scala/v4/util/util.scala:383:64 KIND:node :: node _use_mem_xcpt_T_1 = lt(mem_xcpt_uop.rob_idx, io.core.rob_head_idx)
[6183] FIRRTL:372555 SRC:generators/boom/src/main/scala/v4/util/util.scala:383:58 KIND:node :: node _use_mem_xcpt_T_2 = xor(_use_mem_xcpt_T, _use_mem_xcpt_T_1)
[6184] FIRRTL:372556 SRC:generators/boom/src/main/scala/v4/util/util.scala:383:78 KIND:node :: node _use_mem_xcpt_T_3 = lt(ld_xcpt_uop.rob_idx, io.core.rob_head_idx)
[6185] FIRRTL:372557 SRC:generators/boom/src/main/scala/v4/util/util.scala:383:72 KIND:node :: node _use_mem_xcpt_T_4 = xor(_use_mem_xcpt_T_2, _use_mem_xcpt_T_3)
[6186] FIRRTL:372558 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1464:38 KIND:node :: node _use_mem_xcpt_T_5 = and(mem_xcpt_valid, _use_mem_xcpt_T_4)
[6187] FIRRTL:372559 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1464:118 KIND:node :: node _use_mem_xcpt_T_6 = eq(ld_xcpt_valid, UInt<1>(0h0))
[6188] FIRRTL:372560 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1464:115 KIND:node :: node use_mem_xcpt = or(_use_mem_xcpt_T_5, _use_mem_xcpt_T_6)
[6189] FIRRTL:372561 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1466:21 KIND:node :: node xcpt_uop = mux(use_mem_xcpt, mem_xcpt_uop, ld_xcpt_uop)
[6190] FIRRTL:372562 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1468:34 KIND:node :: node _r_xcpt_valid_T = or(ld_xcpt_valid, mem_xcpt_valid)
[6191] FIRRTL:372563 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _r_xcpt_valid_T_1 = and(io.core.brupdate.b1.mispredict_mask, xcpt_uop.br_mask)
[6192] FIRRTL:372564 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _r_xcpt_valid_T_2 = neq(_r_xcpt_valid_T_1, UInt<1>(0h0))
[6193] FIRRTL:372565 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _r_xcpt_valid_T_3 = or(_r_xcpt_valid_T_2, io.core.exception)
[6194] FIRRTL:372566 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1468:56 KIND:node :: node _r_xcpt_valid_T_4 = eq(_r_xcpt_valid_T_3, UInt<1>(0h0))
[6195] FIRRTL:372567 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1468:53 KIND:node :: node _r_xcpt_valid_T_5 = and(_r_xcpt_valid_T, _r_xcpt_valid_T_4)
[6196] FIRRTL:372568 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1468:16 KIND:connect :: connect r_xcpt_valid, _r_xcpt_valid_T_5
[6197] FIRRTL:372569 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1469:22 KIND:connect :: connect r_xcpt.uop, xcpt_uop
[6198] FIRRTL:372570 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _r_xcpt_uop_br_mask_T = not(io.core.brupdate.b1.resolve_mask)
[6199] FIRRTL:372571 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _r_xcpt_uop_br_mask_T_1 = and(xcpt_uop.br_mask, _r_xcpt_uop_br_mask_T)
[6200] FIRRTL:372572 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1470:22 KIND:connect :: connect r_xcpt.uop.br_mask, _r_xcpt_uop_br_mask_T_1
[6201] FIRRTL:372573 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1471:28 KIND:node :: node _r_xcpt_cause_T = mux(use_mem_xcpt, mem_xcpt_cause, UInt<5>(0h10))
[6202] FIRRTL:372574 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1471:22 KIND:connect :: connect r_xcpt.cause, _r_xcpt_cause_T
[6203] FIRRTL:372575 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1472:22 KIND:connect :: connect r_xcpt.badvaddr, mem_xcpt_vaddr
[6204] FIRRTL:372576 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _io_core_lxcpt_valid_T = and(io.core.brupdate.b1.mispredict_mask, r_xcpt.uop.br_mask)
[6205] FIRRTL:372577 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _io_core_lxcpt_valid_T_1 = neq(_io_core_lxcpt_valid_T, UInt<1>(0h0))
[6206] FIRRTL:372578 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _io_core_lxcpt_valid_T_2 = or(_io_core_lxcpt_valid_T_1, io.core.exception)
[6207] FIRRTL:372579 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1474:42 KIND:node :: node _io_core_lxcpt_valid_T_3 = eq(_io_core_lxcpt_valid_T_2, UInt<1>(0h0))
[6208] FIRRTL:372580 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1474:39 KIND:node :: node _io_core_lxcpt_valid_T_4 = and(r_xcpt_valid, _io_core_lxcpt_valid_T_3)
[6209] FIRRTL:372581 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1474:23 KIND:connect :: connect io.core.lxcpt.valid, _io_core_lxcpt_valid_T_4
[6210] FIRRTL:372582 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1475:23 KIND:connect :: connect io.core.lxcpt.bits, r_xcpt
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
  "task_id": "leaf_abstraction-LSU-region-0-4-9d9375b011581ad1",
  "work_unit_id": "LSU::region-0-4",
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
