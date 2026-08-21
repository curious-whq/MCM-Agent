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

Task ID: `leaf_abstraction-BoomNonBlockingDCache-region-0-3-311dc24763e402d9`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache::region-0-3`
- module: `BoomNonBlockingDCache`
- kind: `region`
- instance path: `BoomNonBlockingDCache`
- leaf: `True`
- coverage complete: `True`
- raw statements: 332
- logical statements: 90
- mapped/logical source lines: 78
- registers: 14
- physical boundary events: 3

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

- `BoomNonBlockingDCache::io.lsu.nack[0].valid`
  - predicate: `io.lsu.nack[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.lsu.nack[0].bits.addr', 'io.lsu.nack[0].bits.data', 'io.lsu.nack[0].bits.is_hella', 'io.lsu.nack[0].bits.uop.bp_debug_if', 'io.lsu.nack[0].bits.uop.bp_xcpt_if', 'io.lsu.nack[0].bits.uop.br_mask', 'io.lsu.nack[0].bits.uop.br_tag', 'io.lsu.nack[0].bits.uop.br_type', 'io.lsu.nack[0].bits.uop.csr_cmd', 'io.lsu.nack[0].bits.uop.debug_fsrc', 'io.lsu.nack[0].bits.uop.debug_inst', 'io.lsu.nack[0].bits.uop.debug_pc', 'io.lsu.nack[0].bits.uop.debug_tsrc', 'io.lsu.nack[0].bits.uop.dis_col_sel', 'io.lsu.nack[0].bits.uop.dst_rtype', 'io.lsu.nack[0].bits.uop.edge_inst', 'io.lsu.nack[0].bits.uop.exc_cause', 'io.lsu.nack[0].bits.uop.exception', 'io.lsu.nack[0].bits.uop.fcn_dw', 'io.lsu.nack[0].bits.uop.fcn_op', 'io.lsu.nack[0].bits.uop.flush_on_commit', 'io.lsu.nack[0].bits.uop.fp_ctrl.div', 'io.lsu.nack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.nack[0].bits.uop.fp_ctrl.fma', 'io.lsu.nack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.nack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.nack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.nack[0].bits.uop.fp_ctrl.toint', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.nack[0].bits.uop.fp_ctrl.vec', 'io.lsu.nack[0].bits.uop.fp_ctrl.wen', 'io.lsu.nack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.nack[0].bits.uop.fp_rm', 'io.lsu.nack[0].bits.uop.fp_typ', 'io.lsu.nack[0].bits.uop.fp_val', 'io.lsu.nack[0].bits.uop.frs3_en', 'io.lsu.nack[0].bits.uop.ftq_idx', 'io.lsu.nack[0].bits.uop.fu_code[0]', 'io.lsu.nack[0].bits.uop.fu_code[1]', 'io.lsu.nack[0].bits.uop.fu_code[2]', 'io.lsu.nack[0].bits.uop.fu_code[3]', 'io.lsu.nack[0].bits.uop.fu_code[4]', 'io.lsu.nack[0].bits.uop.fu_code[5]', 'io.lsu.nack[0].bits.uop.fu_code[6]', 'io.lsu.nack[0].bits.uop.fu_code[7]', 'io.lsu.nack[0].bits.uop.fu_code[8]', 'io.lsu.nack[0].bits.uop.fu_code[9]', 'io.lsu.nack[0].bits.uop.imm_packed', 'io.lsu.nack[0].bits.uop.imm_rename', 'io.lsu.nack[0].bits.uop.imm_sel', 'io.lsu.nack[0].bits.uop.inst', 'io.lsu.nack[0].bits.uop.iq_type[0]', 'io.lsu.nack[0].bits.uop.iq_type[1]', 'io.lsu.nack[0].bits.uop.iq_type[2]', 'io.lsu.nack[0].bits.uop.iq_type[3]', 'io.lsu.nack[0].bits.uop.is_amo', 'io.lsu.nack[0].bits.uop.is_eret', 'io.lsu.nack[0].bits.uop.is_fence', 'io.lsu.nack[0].bits.uop.is_fencei', 'io.lsu.nack[0].bits.uop.is_mov', 'io.lsu.nack[0].bits.uop.is_rocc', 'io.lsu.nack[0].bits.uop.is_rvc', 'io.lsu.nack[0].bits.uop.is_sfb', 'io.lsu.nack[0].bits.uop.is_sfence', 'io.lsu.nack[0].bits.uop.is_sys_pc2epc', 'io.lsu.nack[0].bits.uop.is_unique', 'io.lsu.nack[0].bits.uop.iw_issued', 'io.lsu.nack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.nack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.nack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.nack[0].bits.uop.ldq_idx', 'io.lsu.nack[0].bits.uop.ldst', 'io.lsu.nack[0].bits.uop.ldst_is_rs1', 'io.lsu.nack[0].bits.uop.lrs1', 'io.lsu.nack[0].bits.uop.lrs1_rtype', 'io.lsu.nack[0].bits.uop.lrs2', 'io.lsu.nack[0].bits.uop.lrs2_rtype', 'io.lsu.nack[0].bits.uop.lrs3', 'io.lsu.nack[0].bits.uop.mem_cmd', 'io.lsu.nack[0].bits.uop.mem_signed', 'io.lsu.nack[0].bits.uop.mem_size', 'io.lsu.nack[0].bits.uop.op1_sel', 'io.lsu.nack[0].bits.uop.op2_sel', 'io.lsu.nack[0].bits.uop.pc_lob', 'io.lsu.nack[0].bits.uop.pdst', 'io.lsu.nack[0].bits.uop.pimm', 'io.lsu.nack[0].bits.uop.ppred', 'io.lsu.nack[0].bits.uop.ppred_busy', 'io.lsu.nack[0].bits.uop.prs1', 'io.lsu.nack[0].bits.uop.prs1_busy', 'io.lsu.nack[0].bits.uop.prs2', 'io.lsu.nack[0].bits.uop.prs2_busy', 'io.lsu.nack[0].bits.uop.prs3', 'io.lsu.nack[0].bits.uop.prs3_busy', 'io.lsu.nack[0].bits.uop.rob_idx', 'io.lsu.nack[0].bits.uop.rxq_idx', 'io.lsu.nack[0].bits.uop.stale_pdst', 'io.lsu.nack[0].bits.uop.stq_idx', 'io.lsu.nack[0].bits.uop.taken', 'io.lsu.nack[0].bits.uop.uses_ldq', 'io.lsu.nack[0].bits.uop.uses_stq', 'io.lsu.nack[0].bits.uop.xcpt_ae_if', 'io.lsu.nack[0].bits.uop.xcpt_ma_if', 'io.lsu.nack[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['s2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_nack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']
  - historical registers: ['s1_mshr_meta_read_way_en', 's1_replay_way_en', 's1_req', 's1_send_resp_or_nack', 's1_type', 's1_valid_REG', 's1_wb_way_en', 's2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_nack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']
- `BoomNonBlockingDCache::io.lsu.resp[0].valid`
  - predicate: `io.lsu.resp[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.lsu.resp[0].bits.data', 'io.lsu.resp[0].bits.is_hella', 'io.lsu.resp[0].bits.uop.bp_debug_if', 'io.lsu.resp[0].bits.uop.bp_xcpt_if', 'io.lsu.resp[0].bits.uop.br_mask', 'io.lsu.resp[0].bits.uop.br_tag', 'io.lsu.resp[0].bits.uop.br_type', 'io.lsu.resp[0].bits.uop.csr_cmd', 'io.lsu.resp[0].bits.uop.debug_fsrc', 'io.lsu.resp[0].bits.uop.debug_inst', 'io.lsu.resp[0].bits.uop.debug_pc', 'io.lsu.resp[0].bits.uop.debug_tsrc', 'io.lsu.resp[0].bits.uop.dis_col_sel', 'io.lsu.resp[0].bits.uop.dst_rtype', 'io.lsu.resp[0].bits.uop.edge_inst', 'io.lsu.resp[0].bits.uop.exc_cause', 'io.lsu.resp[0].bits.uop.exception', 'io.lsu.resp[0].bits.uop.fcn_dw', 'io.lsu.resp[0].bits.uop.fcn_op', 'io.lsu.resp[0].bits.uop.flush_on_commit', 'io.lsu.resp[0].bits.uop.fp_ctrl.div', 'io.lsu.resp[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.resp[0].bits.uop.fp_ctrl.fma', 'io.lsu.resp[0].bits.uop.fp_ctrl.fromint', 'io.lsu.resp[0].bits.uop.fp_ctrl.ldst', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren1', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren2', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren3', 'io.lsu.resp[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap12', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap23', 'io.lsu.resp[0].bits.uop.fp_ctrl.toint', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.resp[0].bits.uop.fp_ctrl.vec', 'io.lsu.resp[0].bits.uop.fp_ctrl.wen', 'io.lsu.resp[0].bits.uop.fp_ctrl.wflags', 'io.lsu.resp[0].bits.uop.fp_rm', 'io.lsu.resp[0].bits.uop.fp_typ', 'io.lsu.resp[0].bits.uop.fp_val', 'io.lsu.resp[0].bits.uop.frs3_en', 'io.lsu.resp[0].bits.uop.ftq_idx', 'io.lsu.resp[0].bits.uop.fu_code[0]', 'io.lsu.resp[0].bits.uop.fu_code[1]', 'io.lsu.resp[0].bits.uop.fu_code[2]', 'io.lsu.resp[0].bits.uop.fu_code[3]', 'io.lsu.resp[0].bits.uop.fu_code[4]', 'io.lsu.resp[0].bits.uop.fu_code[5]', 'io.lsu.resp[0].bits.uop.fu_code[6]', 'io.lsu.resp[0].bits.uop.fu_code[7]', 'io.lsu.resp[0].bits.uop.fu_code[8]', 'io.lsu.resp[0].bits.uop.fu_code[9]', 'io.lsu.resp[0].bits.uop.imm_packed', 'io.lsu.resp[0].bits.uop.imm_rename', 'io.lsu.resp[0].bits.uop.imm_sel', 'io.lsu.resp[0].bits.uop.inst', 'io.lsu.resp[0].bits.uop.iq_type[0]', 'io.lsu.resp[0].bits.uop.iq_type[1]', 'io.lsu.resp[0].bits.uop.iq_type[2]', 'io.lsu.resp[0].bits.uop.iq_type[3]', 'io.lsu.resp[0].bits.uop.is_amo', 'io.lsu.resp[0].bits.uop.is_eret', 'io.lsu.resp[0].bits.uop.is_fence', 'io.lsu.resp[0].bits.uop.is_fencei', 'io.lsu.resp[0].bits.uop.is_mov', 'io.lsu.resp[0].bits.uop.is_rocc', 'io.lsu.resp[0].bits.uop.is_rvc', 'io.lsu.resp[0].bits.uop.is_sfb', 'io.lsu.resp[0].bits.uop.is_sfence', 'io.lsu.resp[0].bits.uop.is_sys_pc2epc', 'io.lsu.resp[0].bits.uop.is_unique', 'io.lsu.resp[0].bits.uop.iw_issued', 'io.lsu.resp[0].bits.uop.iw_issued_partial_agen', 'io.lsu.resp[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.resp[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p1_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p2_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.resp[0].bits.uop.ldq_idx', 'io.lsu.resp[0].bits.uop.ldst', 'io.lsu.resp[0].bits.uop.ldst_is_rs1', 'io.lsu.resp[0].bits.uop.lrs1', 'io.lsu.resp[0].bits.uop.lrs1_rtype', 'io.lsu.resp[0].bits.uop.lrs2', 'io.lsu.resp[0].bits.uop.lrs2_rtype', 'io.lsu.resp[0].bits.uop.lrs3', 'io.lsu.resp[0].bits.uop.mem_cmd', 'io.lsu.resp[0].bits.uop.mem_signed', 'io.lsu.resp[0].bits.uop.mem_size', 'io.lsu.resp[0].bits.uop.op1_sel', 'io.lsu.resp[0].bits.uop.op2_sel', 'io.lsu.resp[0].bits.uop.pc_lob', 'io.lsu.resp[0].bits.uop.pdst', 'io.lsu.resp[0].bits.uop.pimm', 'io.lsu.resp[0].bits.uop.ppred', 'io.lsu.resp[0].bits.uop.ppred_busy', 'io.lsu.resp[0].bits.uop.prs1', 'io.lsu.resp[0].bits.uop.prs1_busy', 'io.lsu.resp[0].bits.uop.prs2', 'io.lsu.resp[0].bits.uop.prs2_busy', 'io.lsu.resp[0].bits.uop.prs3', 'io.lsu.resp[0].bits.uop.prs3_busy', 'io.lsu.resp[0].bits.uop.rob_idx', 'io.lsu.resp[0].bits.uop.rxq_idx', 'io.lsu.resp[0].bits.uop.stale_pdst', 'io.lsu.resp[0].bits.uop.stq_idx', 'io.lsu.resp[0].bits.uop.taken', 'io.lsu.resp[0].bits.uop.uses_ldq', 'io.lsu.resp[0].bits.uop.uses_stq', 'io.lsu.resp[0].bits.uop.xcpt_ae_if', 'io.lsu.resp[0].bits.uop.xcpt_ma_if', 'io.lsu.resp[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['s2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_resp_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG']
  - historical registers: ['lrsc_addr', 'lrsc_count', 's1_mshr_meta_read_way_en', 's1_replay_way_en', 's1_req', 's1_send_resp_or_nack', 's1_type', 's1_valid_REG', 's1_wb_way_en', 's2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_lr_REG', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_sc_REG', 's2_send_nack_REG', 's2_send_resp_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches', 's3_req_REG', 's3_valid', 's4_req', 's4_valid', 's5_req', 's5_valid']
- `BoomNonBlockingDCache::io.lsu.store_ack[0].valid`
  - predicate: `io.lsu.store_ack[0].valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.lsu.store_ack[0].bits.addr', 'io.lsu.store_ack[0].bits.data', 'io.lsu.store_ack[0].bits.is_hella', 'io.lsu.store_ack[0].bits.uop.bp_debug_if', 'io.lsu.store_ack[0].bits.uop.bp_xcpt_if', 'io.lsu.store_ack[0].bits.uop.br_mask', 'io.lsu.store_ack[0].bits.uop.br_tag', 'io.lsu.store_ack[0].bits.uop.br_type', 'io.lsu.store_ack[0].bits.uop.csr_cmd', 'io.lsu.store_ack[0].bits.uop.debug_fsrc', 'io.lsu.store_ack[0].bits.uop.debug_inst', 'io.lsu.store_ack[0].bits.uop.debug_pc', 'io.lsu.store_ack[0].bits.uop.debug_tsrc', 'io.lsu.store_ack[0].bits.uop.dis_col_sel', 'io.lsu.store_ack[0].bits.uop.dst_rtype', 'io.lsu.store_ack[0].bits.uop.edge_inst', 'io.lsu.store_ack[0].bits.uop.exc_cause', 'io.lsu.store_ack[0].bits.uop.exception', 'io.lsu.store_ack[0].bits.uop.fcn_dw', 'io.lsu.store_ack[0].bits.uop.fcn_op', 'io.lsu.store_ack[0].bits.uop.flush_on_commit', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.div', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fma', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.toint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.vec', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wen', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.store_ack[0].bits.uop.fp_rm', 'io.lsu.store_ack[0].bits.uop.fp_typ', 'io.lsu.store_ack[0].bits.uop.fp_val', 'io.lsu.store_ack[0].bits.uop.frs3_en', 'io.lsu.store_ack[0].bits.uop.ftq_idx', 'io.lsu.store_ack[0].bits.uop.fu_code[0]', 'io.lsu.store_ack[0].bits.uop.fu_code[1]', 'io.lsu.store_ack[0].bits.uop.fu_code[2]', 'io.lsu.store_ack[0].bits.uop.fu_code[3]', 'io.lsu.store_ack[0].bits.uop.fu_code[4]', 'io.lsu.store_ack[0].bits.uop.fu_code[5]', 'io.lsu.store_ack[0].bits.uop.fu_code[6]', 'io.lsu.store_ack[0].bits.uop.fu_code[7]', 'io.lsu.store_ack[0].bits.uop.fu_code[8]', 'io.lsu.store_ack[0].bits.uop.fu_code[9]', 'io.lsu.store_ack[0].bits.uop.imm_packed', 'io.lsu.store_ack[0].bits.uop.imm_rename', 'io.lsu.store_ack[0].bits.uop.imm_sel', 'io.lsu.store_ack[0].bits.uop.inst', 'io.lsu.store_ack[0].bits.uop.iq_type[0]', 'io.lsu.store_ack[0].bits.uop.iq_type[1]', 'io.lsu.store_ack[0].bits.uop.iq_type[2]', 'io.lsu.store_ack[0].bits.uop.iq_type[3]', 'io.lsu.store_ack[0].bits.uop.is_amo', 'io.lsu.store_ack[0].bits.uop.is_eret', 'io.lsu.store_ack[0].bits.uop.is_fence', 'io.lsu.store_ack[0].bits.uop.is_fencei', 'io.lsu.store_ack[0].bits.uop.is_mov', 'io.lsu.store_ack[0].bits.uop.is_rocc', 'io.lsu.store_ack[0].bits.uop.is_rvc', 'io.lsu.store_ack[0].bits.uop.is_sfb', 'io.lsu.store_ack[0].bits.uop.is_sfence', 'io.lsu.store_ack[0].bits.uop.is_sys_pc2epc', 'io.lsu.store_ack[0].bits.uop.is_unique', 'io.lsu.store_ack[0].bits.uop.iw_issued', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.store_ack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.store_ack[0].bits.uop.ldq_idx', 'io.lsu.store_ack[0].bits.uop.ldst', 'io.lsu.store_ack[0].bits.uop.ldst_is_rs1', 'io.lsu.store_ack[0].bits.uop.lrs1', 'io.lsu.store_ack[0].bits.uop.lrs1_rtype', 'io.lsu.store_ack[0].bits.uop.lrs2', 'io.lsu.store_ack[0].bits.uop.lrs2_rtype', 'io.lsu.store_ack[0].bits.uop.lrs3', 'io.lsu.store_ack[0].bits.uop.mem_cmd', 'io.lsu.store_ack[0].bits.uop.mem_signed', 'io.lsu.store_ack[0].bits.uop.mem_size', 'io.lsu.store_ack[0].bits.uop.op1_sel', 'io.lsu.store_ack[0].bits.uop.op2_sel', 'io.lsu.store_ack[0].bits.uop.pc_lob', 'io.lsu.store_ack[0].bits.uop.pdst', 'io.lsu.store_ack[0].bits.uop.pimm', 'io.lsu.store_ack[0].bits.uop.ppred', 'io.lsu.store_ack[0].bits.uop.ppred_busy', 'io.lsu.store_ack[0].bits.uop.prs1', 'io.lsu.store_ack[0].bits.uop.prs1_busy', 'io.lsu.store_ack[0].bits.uop.prs2', 'io.lsu.store_ack[0].bits.uop.prs2_busy', 'io.lsu.store_ack[0].bits.uop.prs3', 'io.lsu.store_ack[0].bits.uop.prs3_busy', 'io.lsu.store_ack[0].bits.uop.rob_idx', 'io.lsu.store_ack[0].bits.uop.rxq_idx', 'io.lsu.store_ack[0].bits.uop.stale_pdst', 'io.lsu.store_ack[0].bits.uop.stq_idx', 'io.lsu.store_ack[0].bits.uop.taken', 'io.lsu.store_ack[0].bits.uop.uses_ldq', 'io.lsu.store_ack[0].bits.uop.uses_stq', 'io.lsu.store_ack[0].bits.uop.xcpt_ae_if', 'io.lsu.store_ack[0].bits.uop.xcpt_ma_if', 'io.lsu.store_ack[0].bits.uop.xcpt_pf_if']
  - immediate registers: ['s2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_store_ack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']
  - historical registers: ['s1_mshr_meta_read_way_en', 's1_replay_way_en', 's1_req', 's1_send_resp_or_nack', 's1_type', 's1_valid_REG', 's1_wb_way_en', 's2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_nack_REG', 's2_send_store_ack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']

## Concrete local state

['s2_hit_state_REG', 's2_hit_state_REG_1', 's2_hit_state_REG_2', 's2_hit_state_REG_3', 's2_nack_data_REG', 's2_nack_hit', 's2_req', 's2_send_nack_REG', 's2_send_resp_REG', 's2_send_store_ack_REG', 's2_tag_match_way', 's2_type', 's2_valid_REG', 's2_wb_idx_matches']

## Environment/frontier signals

['_s2_data_muxed_WIRE', '_s2_nack_hit_WIRE', 'amoalu.io.out', 'data.io.resp[0][0]', 'data.io.resp[0][1]', 'data.io.resp[0][2]', 'data.io.resp[0][3]', 'data.io.s1_nacks[0]', 'h0', 'h1', 'h10', 'h11', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'io.lsu.brupdate.b1.mispredict_mask', 'io.lsu.brupdate.b1.resolve_mask', 'io.lsu.exception', 'io.lsu.nack[0].bits.addr', 'io.lsu.nack[0].bits.data', 'io.lsu.nack[0].bits.is_hella', 'io.lsu.nack[0].bits.uop.bp_debug_if', 'io.lsu.nack[0].bits.uop.bp_xcpt_if', 'io.lsu.nack[0].bits.uop.br_mask', 'io.lsu.nack[0].bits.uop.br_tag', 'io.lsu.nack[0].bits.uop.br_type', 'io.lsu.nack[0].bits.uop.csr_cmd', 'io.lsu.nack[0].bits.uop.debug_fsrc', 'io.lsu.nack[0].bits.uop.debug_inst', 'io.lsu.nack[0].bits.uop.debug_pc', 'io.lsu.nack[0].bits.uop.debug_tsrc', 'io.lsu.nack[0].bits.uop.dis_col_sel', 'io.lsu.nack[0].bits.uop.dst_rtype', 'io.lsu.nack[0].bits.uop.edge_inst', 'io.lsu.nack[0].bits.uop.exc_cause', 'io.lsu.nack[0].bits.uop.exception', 'io.lsu.nack[0].bits.uop.fcn_dw', 'io.lsu.nack[0].bits.uop.fcn_op', 'io.lsu.nack[0].bits.uop.flush_on_commit', 'io.lsu.nack[0].bits.uop.fp_ctrl.div', 'io.lsu.nack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.nack[0].bits.uop.fp_ctrl.fma', 'io.lsu.nack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.nack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.nack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.nack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.nack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.nack[0].bits.uop.fp_ctrl.toint', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.nack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.nack[0].bits.uop.fp_ctrl.vec', 'io.lsu.nack[0].bits.uop.fp_ctrl.wen', 'io.lsu.nack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.nack[0].bits.uop.fp_rm', 'io.lsu.nack[0].bits.uop.fp_typ', 'io.lsu.nack[0].bits.uop.fp_val', 'io.lsu.nack[0].bits.uop.frs3_en', 'io.lsu.nack[0].bits.uop.ftq_idx', 'io.lsu.nack[0].bits.uop.fu_code[0]', 'io.lsu.nack[0].bits.uop.fu_code[1]', 'io.lsu.nack[0].bits.uop.fu_code[2]', 'io.lsu.nack[0].bits.uop.fu_code[3]', 'io.lsu.nack[0].bits.uop.fu_code[4]', 'io.lsu.nack[0].bits.uop.fu_code[5]', 'io.lsu.nack[0].bits.uop.fu_code[6]', 'io.lsu.nack[0].bits.uop.fu_code[7]', 'io.lsu.nack[0].bits.uop.fu_code[8]', 'io.lsu.nack[0].bits.uop.fu_code[9]', 'io.lsu.nack[0].bits.uop.imm_packed', 'io.lsu.nack[0].bits.uop.imm_rename', 'io.lsu.nack[0].bits.uop.imm_sel', 'io.lsu.nack[0].bits.uop.inst', 'io.lsu.nack[0].bits.uop.iq_type[0]', 'io.lsu.nack[0].bits.uop.iq_type[1]', 'io.lsu.nack[0].bits.uop.iq_type[2]', 'io.lsu.nack[0].bits.uop.iq_type[3]', 'io.lsu.nack[0].bits.uop.is_amo', 'io.lsu.nack[0].bits.uop.is_eret', 'io.lsu.nack[0].bits.uop.is_fence', 'io.lsu.nack[0].bits.uop.is_fencei', 'io.lsu.nack[0].bits.uop.is_mov', 'io.lsu.nack[0].bits.uop.is_rocc', 'io.lsu.nack[0].bits.uop.is_rvc', 'io.lsu.nack[0].bits.uop.is_sfb', 'io.lsu.nack[0].bits.uop.is_sfence', 'io.lsu.nack[0].bits.uop.is_sys_pc2epc', 'io.lsu.nack[0].bits.uop.is_unique', 'io.lsu.nack[0].bits.uop.iw_issued', 'io.lsu.nack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.nack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.nack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.nack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.nack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.nack[0].bits.uop.ldq_idx', 'io.lsu.nack[0].bits.uop.ldst', 'io.lsu.nack[0].bits.uop.ldst_is_rs1', 'io.lsu.nack[0].bits.uop.lrs1', 'io.lsu.nack[0].bits.uop.lrs1_rtype', 'io.lsu.nack[0].bits.uop.lrs2', 'io.lsu.nack[0].bits.uop.lrs2_rtype', 'io.lsu.nack[0].bits.uop.lrs3', 'io.lsu.nack[0].bits.uop.mem_cmd', 'io.lsu.nack[0].bits.uop.mem_signed', 'io.lsu.nack[0].bits.uop.mem_size', 'io.lsu.nack[0].bits.uop.op1_sel', 'io.lsu.nack[0].bits.uop.op2_sel', 'io.lsu.nack[0].bits.uop.pc_lob', 'io.lsu.nack[0].bits.uop.pdst', 'io.lsu.nack[0].bits.uop.pimm', 'io.lsu.nack[0].bits.uop.ppred', 'io.lsu.nack[0].bits.uop.ppred_busy', 'io.lsu.nack[0].bits.uop.prs1', 'io.lsu.nack[0].bits.uop.prs1_busy', 'io.lsu.nack[0].bits.uop.prs2', 'io.lsu.nack[0].bits.uop.prs2_busy', 'io.lsu.nack[0].bits.uop.prs3', 'io.lsu.nack[0].bits.uop.prs3_busy', 'io.lsu.nack[0].bits.uop.rob_idx', 'io.lsu.nack[0].bits.uop.rxq_idx', 'io.lsu.nack[0].bits.uop.stale_pdst', 'io.lsu.nack[0].bits.uop.stq_idx', 'io.lsu.nack[0].bits.uop.taken', 'io.lsu.nack[0].bits.uop.uses_ldq', 'io.lsu.nack[0].bits.uop.uses_stq', 'io.lsu.nack[0].bits.uop.xcpt_ae_if', 'io.lsu.nack[0].bits.uop.xcpt_ma_if', 'io.lsu.nack[0].bits.uop.xcpt_pf_if', 'io.lsu.nack[0].valid', 'io.lsu.resp[0].bits.data', 'io.lsu.resp[0].bits.is_hella', 'io.lsu.resp[0].bits.uop.bp_debug_if', 'io.lsu.resp[0].bits.uop.bp_xcpt_if', 'io.lsu.resp[0].bits.uop.br_mask', 'io.lsu.resp[0].bits.uop.br_tag', 'io.lsu.resp[0].bits.uop.br_type', 'io.lsu.resp[0].bits.uop.csr_cmd', 'io.lsu.resp[0].bits.uop.debug_fsrc', 'io.lsu.resp[0].bits.uop.debug_inst', 'io.lsu.resp[0].bits.uop.debug_pc', 'io.lsu.resp[0].bits.uop.debug_tsrc', 'io.lsu.resp[0].bits.uop.dis_col_sel', 'io.lsu.resp[0].bits.uop.dst_rtype', 'io.lsu.resp[0].bits.uop.edge_inst', 'io.lsu.resp[0].bits.uop.exc_cause', 'io.lsu.resp[0].bits.uop.exception', 'io.lsu.resp[0].bits.uop.fcn_dw', 'io.lsu.resp[0].bits.uop.fcn_op', 'io.lsu.resp[0].bits.uop.flush_on_commit', 'io.lsu.resp[0].bits.uop.fp_ctrl.div', 'io.lsu.resp[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.resp[0].bits.uop.fp_ctrl.fma', 'io.lsu.resp[0].bits.uop.fp_ctrl.fromint', 'io.lsu.resp[0].bits.uop.fp_ctrl.ldst', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren1', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren2', 'io.lsu.resp[0].bits.uop.fp_ctrl.ren3', 'io.lsu.resp[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap12', 'io.lsu.resp[0].bits.uop.fp_ctrl.swap23', 'io.lsu.resp[0].bits.uop.fp_ctrl.toint', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.resp[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.resp[0].bits.uop.fp_ctrl.vec', 'io.lsu.resp[0].bits.uop.fp_ctrl.wen', 'io.lsu.resp[0].bits.uop.fp_ctrl.wflags', 'io.lsu.resp[0].bits.uop.fp_rm', 'io.lsu.resp[0].bits.uop.fp_typ', 'io.lsu.resp[0].bits.uop.fp_val', 'io.lsu.resp[0].bits.uop.frs3_en', 'io.lsu.resp[0].bits.uop.ftq_idx', 'io.lsu.resp[0].bits.uop.fu_code[0]', 'io.lsu.resp[0].bits.uop.fu_code[1]', 'io.lsu.resp[0].bits.uop.fu_code[2]', 'io.lsu.resp[0].bits.uop.fu_code[3]', 'io.lsu.resp[0].bits.uop.fu_code[4]', 'io.lsu.resp[0].bits.uop.fu_code[5]', 'io.lsu.resp[0].bits.uop.fu_code[6]', 'io.lsu.resp[0].bits.uop.fu_code[7]', 'io.lsu.resp[0].bits.uop.fu_code[8]', 'io.lsu.resp[0].bits.uop.fu_code[9]', 'io.lsu.resp[0].bits.uop.imm_packed', 'io.lsu.resp[0].bits.uop.imm_rename', 'io.lsu.resp[0].bits.uop.imm_sel', 'io.lsu.resp[0].bits.uop.inst', 'io.lsu.resp[0].bits.uop.iq_type[0]', 'io.lsu.resp[0].bits.uop.iq_type[1]', 'io.lsu.resp[0].bits.uop.iq_type[2]', 'io.lsu.resp[0].bits.uop.iq_type[3]', 'io.lsu.resp[0].bits.uop.is_amo', 'io.lsu.resp[0].bits.uop.is_eret', 'io.lsu.resp[0].bits.uop.is_fence', 'io.lsu.resp[0].bits.uop.is_fencei', 'io.lsu.resp[0].bits.uop.is_mov', 'io.lsu.resp[0].bits.uop.is_rocc', 'io.lsu.resp[0].bits.uop.is_rvc', 'io.lsu.resp[0].bits.uop.is_sfb', 'io.lsu.resp[0].bits.uop.is_sfence', 'io.lsu.resp[0].bits.uop.is_sys_pc2epc', 'io.lsu.resp[0].bits.uop.is_unique', 'io.lsu.resp[0].bits.uop.iw_issued', 'io.lsu.resp[0].bits.uop.iw_issued_partial_agen', 'io.lsu.resp[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.resp[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p1_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.resp[0].bits.uop.iw_p2_speculative_child', 'io.lsu.resp[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.resp[0].bits.uop.ldq_idx', 'io.lsu.resp[0].bits.uop.ldst', 'io.lsu.resp[0].bits.uop.ldst_is_rs1', 'io.lsu.resp[0].bits.uop.lrs1', 'io.lsu.resp[0].bits.uop.lrs1_rtype', 'io.lsu.resp[0].bits.uop.lrs2', 'io.lsu.resp[0].bits.uop.lrs2_rtype', 'io.lsu.resp[0].bits.uop.lrs3', 'io.lsu.resp[0].bits.uop.mem_cmd', 'io.lsu.resp[0].bits.uop.mem_signed', 'io.lsu.resp[0].bits.uop.mem_size', 'io.lsu.resp[0].bits.uop.op1_sel', 'io.lsu.resp[0].bits.uop.op2_sel', 'io.lsu.resp[0].bits.uop.pc_lob', 'io.lsu.resp[0].bits.uop.pdst', 'io.lsu.resp[0].bits.uop.pimm', 'io.lsu.resp[0].bits.uop.ppred', 'io.lsu.resp[0].bits.uop.ppred_busy', 'io.lsu.resp[0].bits.uop.prs1', 'io.lsu.resp[0].bits.uop.prs1_busy', 'io.lsu.resp[0].bits.uop.prs2', 'io.lsu.resp[0].bits.uop.prs2_busy', 'io.lsu.resp[0].bits.uop.prs3', 'io.lsu.resp[0].bits.uop.prs3_busy', 'io.lsu.resp[0].bits.uop.rob_idx', 'io.lsu.resp[0].bits.uop.rxq_idx', 'io.lsu.resp[0].bits.uop.stale_pdst', 'io.lsu.resp[0].bits.uop.stq_idx', 'io.lsu.resp[0].bits.uop.taken', 'io.lsu.resp[0].bits.uop.uses_ldq', 'io.lsu.resp[0].bits.uop.uses_stq', 'io.lsu.resp[0].bits.uop.xcpt_ae_if', 'io.lsu.resp[0].bits.uop.xcpt_ma_if', 'io.lsu.resp[0].bits.uop.xcpt_pf_if', 'io.lsu.resp[0].valid', 'io.lsu.s1_kill[0]', 'io.lsu.store_ack[0].bits.addr', 'io.lsu.store_ack[0].bits.data', 'io.lsu.store_ack[0].bits.is_hella', 'io.lsu.store_ack[0].bits.uop.bp_debug_if', 'io.lsu.store_ack[0].bits.uop.bp_xcpt_if', 'io.lsu.store_ack[0].bits.uop.br_mask', 'io.lsu.store_ack[0].bits.uop.br_tag', 'io.lsu.store_ack[0].bits.uop.br_type', 'io.lsu.store_ack[0].bits.uop.csr_cmd', 'io.lsu.store_ack[0].bits.uop.debug_fsrc', 'io.lsu.store_ack[0].bits.uop.debug_inst', 'io.lsu.store_ack[0].bits.uop.debug_pc', 'io.lsu.store_ack[0].bits.uop.debug_tsrc', 'io.lsu.store_ack[0].bits.uop.dis_col_sel', 'io.lsu.store_ack[0].bits.uop.dst_rtype', 'io.lsu.store_ack[0].bits.uop.edge_inst', 'io.lsu.store_ack[0].bits.uop.exc_cause', 'io.lsu.store_ack[0].bits.uop.exception', 'io.lsu.store_ack[0].bits.uop.fcn_dw', 'io.lsu.store_ack[0].bits.uop.fcn_op', 'io.lsu.store_ack[0].bits.uop.flush_on_commit', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.div', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fma', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.fromint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ldst', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren1', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren2', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.ren3', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap12', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.swap23', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.toint', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.vec', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wen', 'io.lsu.store_ack[0].bits.uop.fp_ctrl.wflags', 'io.lsu.store_ack[0].bits.uop.fp_rm', 'io.lsu.store_ack[0].bits.uop.fp_typ', 'io.lsu.store_ack[0].bits.uop.fp_val', 'io.lsu.store_ack[0].bits.uop.frs3_en', 'io.lsu.store_ack[0].bits.uop.ftq_idx', 'io.lsu.store_ack[0].bits.uop.fu_code[0]', 'io.lsu.store_ack[0].bits.uop.fu_code[1]', 'io.lsu.store_ack[0].bits.uop.fu_code[2]', 'io.lsu.store_ack[0].bits.uop.fu_code[3]', 'io.lsu.store_ack[0].bits.uop.fu_code[4]', 'io.lsu.store_ack[0].bits.uop.fu_code[5]', 'io.lsu.store_ack[0].bits.uop.fu_code[6]', 'io.lsu.store_ack[0].bits.uop.fu_code[7]', 'io.lsu.store_ack[0].bits.uop.fu_code[8]', 'io.lsu.store_ack[0].bits.uop.fu_code[9]', 'io.lsu.store_ack[0].bits.uop.imm_packed', 'io.lsu.store_ack[0].bits.uop.imm_rename', 'io.lsu.store_ack[0].bits.uop.imm_sel', 'io.lsu.store_ack[0].bits.uop.inst', 'io.lsu.store_ack[0].bits.uop.iq_type[0]', 'io.lsu.store_ack[0].bits.uop.iq_type[1]', 'io.lsu.store_ack[0].bits.uop.iq_type[2]', 'io.lsu.store_ack[0].bits.uop.iq_type[3]', 'io.lsu.store_ack[0].bits.uop.is_amo', 'io.lsu.store_ack[0].bits.uop.is_eret', 'io.lsu.store_ack[0].bits.uop.is_fence', 'io.lsu.store_ack[0].bits.uop.is_fencei', 'io.lsu.store_ack[0].bits.uop.is_mov', 'io.lsu.store_ack[0].bits.uop.is_rocc', 'io.lsu.store_ack[0].bits.uop.is_rvc', 'io.lsu.store_ack[0].bits.uop.is_sfb', 'io.lsu.store_ack[0].bits.uop.is_sfence', 'io.lsu.store_ack[0].bits.uop.is_sys_pc2epc', 'io.lsu.store_ack[0].bits.uop.is_unique', 'io.lsu.store_ack[0].bits.uop.iw_issued', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_agen', 'io.lsu.store_ack[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.store_ack[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p1_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.store_ack[0].bits.uop.iw_p2_speculative_child', 'io.lsu.store_ack[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.store_ack[0].bits.uop.ldq_idx', 'io.lsu.store_ack[0].bits.uop.ldst', 'io.lsu.store_ack[0].bits.uop.ldst_is_rs1', 'io.lsu.store_ack[0].bits.uop.lrs1', 'io.lsu.store_ack[0].bits.uop.lrs1_rtype', 'io.lsu.store_ack[0].bits.uop.lrs2', 'io.lsu.store_ack[0].bits.uop.lrs2_rtype', 'io.lsu.store_ack[0].bits.uop.lrs3', 'io.lsu.store_ack[0].bits.uop.mem_cmd', 'io.lsu.store_ack[0].bits.uop.mem_signed', 'io.lsu.store_ack[0].bits.uop.mem_size', 'io.lsu.store_ack[0].bits.uop.op1_sel', 'io.lsu.store_ack[0].bits.uop.op2_sel', 'io.lsu.store_ack[0].bits.uop.pc_lob', 'io.lsu.store_ack[0].bits.uop.pdst', 'io.lsu.store_ack[0].bits.uop.pimm', 'io.lsu.store_ack[0].bits.uop.ppred', 'io.lsu.store_ack[0].bits.uop.ppred_busy', 'io.lsu.store_ack[0].bits.uop.prs1', 'io.lsu.store_ack[0].bits.uop.prs1_busy', 'io.lsu.store_ack[0].bits.uop.prs2', 'io.lsu.store_ack[0].bits.uop.prs2_busy', 'io.lsu.store_ack[0].bits.uop.prs3', 'io.lsu.store_ack[0].bits.uop.prs3_busy', 'io.lsu.store_ack[0].bits.uop.rob_idx', 'io.lsu.store_ack[0].bits.uop.rxq_idx', 'io.lsu.store_ack[0].bits.uop.stale_pdst', 'io.lsu.store_ack[0].bits.uop.stq_idx', 'io.lsu.store_ack[0].bits.uop.taken', 'io.lsu.store_ack[0].bits.uop.uses_ldq', 'io.lsu.store_ack[0].bits.uop.uses_stq', 'io.lsu.store_ack[0].bits.uop.xcpt_ae_if', 'io.lsu.store_ack[0].bits.uop.xcpt_ma_if', 'io.lsu.store_ack[0].bits.uop.xcpt_pf_if', 'io.lsu.store_ack[0].valid', 'meta_0.io.resp[0].coh.state', 'meta_0.io.resp[0].tag', 'meta_0.io.resp[1].coh.state', 'meta_0.io.resp[1].tag', 'meta_0.io.resp[2].coh.state', 'meta_0.io.resp[2].tag', 'meta_0.io.resp[3].coh.state', 'meta_0.io.resp[3].tag', 'mshrs.io.req[0].ready', 'mshrs.io.req[0].valid', 'prober.io.meta_write.bits.idx', 'prober.io.req.ready', 's1_mshr_meta_read_way_en', 's1_nack_0', 's1_replay_way_en', 's1_req', 's1_req[0].addr', 's1_req[0].uop.br_mask', 's1_req[0].uop.uses_ldq', 's1_req[0].uop.uses_stq', 's1_send_resp_or_nack[0]', 's1_tag_match_way', 's1_type', 's1_valid[0]', 's1_valid_REG', 's1_wb_idx_matches', 's1_wb_way_en', 's2_data_muxed[0]', 's2_data_word[0]', 's2_hit[0]', 's2_lrsc_addr_match[0]', 's2_nack[0]', 's2_nack_data[0]', 's2_nack_data_REG', 's2_nack_hit[0]', 's2_nack_victim[0]', 's2_nack_wb[0]', 's2_req[0]', 's2_req[0].addr', 's2_req[0].data', 's2_req[0].is_hella', 's2_req[0].uop.bp_debug_if', 's2_req[0].uop.bp_xcpt_if', 's2_req[0].uop.br_mask', 's2_req[0].uop.br_tag', 's2_req[0].uop.br_type', 's2_req[0].uop.csr_cmd', 's2_req[0].uop.debug_fsrc', 's2_req[0].uop.debug_inst', 's2_req[0].uop.debug_pc', 's2_req[0].uop.debug_tsrc', 's2_req[0].uop.dis_col_sel', 's2_req[0].uop.dst_rtype', 's2_req[0].uop.edge_inst', 's2_req[0].uop.exc_cause', 's2_req[0].uop.exception', 's2_req[0].uop.fcn_dw', 's2_req[0].uop.fcn_op', 's2_req[0].uop.flush_on_commit', 's2_req[0].uop.fp_ctrl.div', 's2_req[0].uop.fp_ctrl.fastpipe', 's2_req[0].uop.fp_ctrl.fma', 's2_req[0].uop.fp_ctrl.fromint', 's2_req[0].uop.fp_ctrl.ldst', 's2_req[0].uop.fp_ctrl.ren1', 's2_req[0].uop.fp_ctrl.ren2', 's2_req[0].uop.fp_ctrl.ren3', 's2_req[0].uop.fp_ctrl.sqrt', 's2_req[0].uop.fp_ctrl.swap12', 's2_req[0].uop.fp_ctrl.swap23', 's2_req[0].uop.fp_ctrl.toint', 's2_req[0].uop.fp_ctrl.typeTagIn', 's2_req[0].uop.fp_ctrl.typeTagOut', 's2_req[0].uop.fp_ctrl.vec', 's2_req[0].uop.fp_ctrl.wen', 's2_req[0].uop.fp_ctrl.wflags', 's2_req[0].uop.fp_rm', 's2_req[0].uop.fp_typ', 's2_req[0].uop.fp_val', 's2_req[0].uop.frs3_en', 's2_req[0].uop.ftq_idx', 's2_req[0].uop.fu_code[0]', 's2_req[0].uop.fu_code[1]', 's2_req[0].uop.fu_code[2]', 's2_req[0].uop.fu_code[3]', 's2_req[0].uop.fu_code[4]', 's2_req[0].uop.fu_code[5]', 's2_req[0].uop.fu_code[6]', 's2_req[0].uop.fu_code[7]', 's2_req[0].uop.fu_code[8]', 's2_req[0].uop.fu_code[9]', 's2_req[0].uop.imm_packed', 's2_req[0].uop.imm_rename', 's2_req[0].uop.imm_sel', 's2_req[0].uop.inst', 's2_req[0].uop.iq_type[0]', 's2_req[0].uop.iq_type[1]', 's2_req[0].uop.iq_type[2]', 's2_req[0].uop.iq_type[3]', 's2_req[0].uop.is_amo', 's2_req[0].uop.is_eret', 's2_req[0].uop.is_fence', 's2_req[0].uop.is_fencei', 's2_req[0].uop.is_mov', 's2_req[0].uop.is_rocc', 's2_req[0].uop.is_rvc', 's2_req[0].uop.is_sfb', 's2_req[0].uop.is_sfence', 's2_req[0].uop.is_sys_pc2epc', 's2_req[0].uop.is_unique', 's2_req[0].uop.iw_issued', 's2_req[0].uop.iw_issued_partial_agen', 's2_req[0].uop.iw_issued_partial_dgen', 's2_req[0].uop.iw_p1_bypass_hint', 's2_req[0].uop.iw_p1_speculative_child', 's2_req[0].uop.iw_p2_bypass_hint', 's2_req[0].uop.iw_p2_speculative_child', 's2_req[0].uop.iw_p3_bypass_hint', 's2_req[0].uop.ldq_idx', 's2_req[0].uop.ldst', 's2_req[0].uop.ldst_is_rs1', 's2_req[0].uop.lrs1', 's2_req[0].uop.lrs1_rtype', 's2_req[0].uop.lrs2', 's2_req[0].uop.lrs2_rtype', 's2_req[0].uop.lrs3', 's2_req[0].uop.mem_cmd', 's2_req[0].uop.mem_signed', 's2_req[0].uop.mem_size', 's2_req[0].uop.op1_sel', 's2_req[0].uop.op2_sel', 's2_req[0].uop.pc_lob', 's2_req[0].uop.pdst', 's2_req[0].uop.pimm', 's2_req[0].uop.ppred', 's2_req[0].uop.ppred_busy', 's2_req[0].uop.prs1', 's2_req[0].uop.prs1_busy', 's2_req[0].uop.prs2', 's2_req[0].uop.prs2_busy', 's2_req[0].uop.prs3', 's2_req[0].uop.prs3_busy', 's2_req[0].uop.rob_idx', 's2_req[0].uop.rxq_idx', 's2_req[0].uop.stale_pdst', 's2_req[0].uop.stq_idx', 's2_req[0].uop.taken', 's2_req[0].uop.uses_ldq', 's2_req[0].uop.uses_stq', 's2_req[0].uop.xcpt_ae_if', 's2_req[0].uop.xcpt_ma_if', 's2_req[0].uop.xcpt_pf_if', 's2_sc', 's2_sc_REG', 's2_sc_fail', 's2_send_nack[0]', 's2_send_nack_REG', 's2_send_resp[0]', 's2_send_resp_REG', 's2_send_store_ack_REG', 's2_store_failed', 's2_tag_match_way[0]', 's2_type', 's2_valid[0]', 's2_valid_REG', 's2_wb_idx_matches[0]', 's3_req.addr', 's3_req.data', 's3_req.uop.mem_cmd', 's3_req.uop.mem_size', 's3_req_REG', 's3_valid', 's4_req.addr', 's4_req.data', 's4_valid', 's5_req.addr', 's5_req.data', 's5_valid', 'size', 'wb.io.idx.bits', 'wb.io.idx.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:453-455
```scala

  def widthMap[T <: Data](f: Int => T) = VecInit((0 until lsuWidth).map(f))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:646-648
```scala
  val s1_addr         = s1_req.map(_.addr)
  val s1_nack         = s1_addr.map(a => a(idxMSB,idxLSB) === prober.io.meta_write.bits.idx && !prober.io.req.ready)
  val s1_send_resp_or_nack = RegNext(s0_send_resp_or_nack)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:655-665
```scala
  // tag check
  def wayMap[T <: Data](f: Int => T) = VecInit((0 until nWays).map(f))
  val s1_tag_eq_way = widthMap(i => wayMap((w: Int) => meta(i).io.resp(w).tag === (s1_addr(i) >> untagBits)).asUInt)
  val s1_tag_match_way = widthMap(i =>
                         Mux(s1_type === t_replay, s1_replay_way_en,
                         Mux(s1_type === t_wb,     s1_wb_way_en,
                         Mux(s1_type === t_mshr_meta_read, s1_mshr_meta_read_way_en,
                           wayMap((w: Int) => s1_tag_eq_way(i)(w) && meta(i).io.resp(w).coh.isValid()).asUInt))))

  val s1_wb_idx_matches = widthMap(i => (s1_addr(i)(untagBits-1,blockOffBits) === wb.io.idx.bits) && wb.io.idx.valid)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:669-684
```scala

  val s2_req   = RegNext(s1_req)
  val s2_type  = RegNext(s1_type)
  val s2_valid = widthMap(w =>
                  RegNext(s1_valid(w) &&
                         !io.lsu.s1_kill(w) &&
                         !IsKilledByBranch(io.lsu.brupdate, false.B, s1_req(w).uop) &&
                         !(io.lsu.exception && s1_req(w).uop.uses_ldq) &&
                         !(s2_store_failed && (s1_type === t_lsu) && s1_req(w).uop.uses_stq)))
  for (w <- 0 until lsuWidth)
    s2_req(w).uop.br_mask := GetNewBrMask(io.lsu.brupdate, s1_req(w).uop)

  val s2_tag_match_way = RegNext(s1_tag_match_way)
  val s2_tag_match     = s2_tag_match_way.map(_.orR)
  val s2_hit_state     = widthMap(i => Mux1H(s2_tag_match_way(i), wayMap((w: Int) => RegNext(meta(i).io.resp(w).coh))))
  val s2_has_permission = widthMap(w => s2_hit_state(w).onAccess(s2_req(w).uop.mem_cmd)._1)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:691-693
```scala

  val s2_wb_idx_matches = RegNext(s1_wb_idx_matches)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:701-705
```scala
  val s2_lr = s2_req(0).uop.mem_cmd === M_XLR && (!RegNext(s1_nack(0)) || s2_type === t_replay)
  val s2_sc = s2_req(0).uop.mem_cmd === M_XSC && (!RegNext(s1_nack(0)) || s2_type === t_replay)
  val s2_lrsc_addr_match = widthMap(w => lrsc_valid && lrsc_addr === (s2_req(w).addr >> blockOffBits))
  val s2_sc_fail = s2_sc && !s2_lrsc_addr_match(0)
  when (lrsc_count > 0.U) { lrsc_count := lrsc_count - 1.U }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:745-747
```scala
    for (w <- 0 until nWays) {
      s2_data(i)(w) := data.io.resp(i)(w)
    }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:759-761
```scala
  // nack because of incoming probe
  val s2_nack_hit    = RegNext(VecInit(s1_nack))
  // Nack when we hit something currently being evicted
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:765-767
```scala
  // Bank conflict on data arrays
  val s2_nack_data   = widthMap(w => s2_valid(w) && RegNext(data.io.s1_nacks(w)))
  // Can't allocate MSHR for same set currently being written back
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:772-776
```scala
  val s2_send_resp = widthMap(w => (
    RegNext(s1_send_resp_or_nack(w)) &&
      (!(s2_nack_hit(w) || s2_nack_victim(w) || s2_nack_data(w)) || s2_type === t_replay) &&
      s2_hit(w) && isRead(s2_req(w).uop.mem_cmd)
  ))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:777-781
```scala
  val s2_send_store_ack = widthMap(w => (
    RegNext(s1_send_resp_or_nack(w)) && !s2_nack(w) && isWrite(s2_req(w).uop.mem_cmd) &&
      (s2_hit(w) || mshrs.io.req(w).fire)))
  val s2_send_nack = widthMap(w => (RegNext(s1_send_resp_or_nack(w)) && s2_nack(w)))
  for (w <- 0 until lsuWidth)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:786-788
```scala
  // If MSHR is available and this is only a store(not a amo), we don't need to wait for resp later
  s2_store_failed := s2_valid(0) && s2_nack(0) && s2_send_nack(0) && s2_req(0).uop.uses_stq
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:790-801
```scala
  for (w <- 0 until lsuWidth) {
    mshrs.io.req(w).valid := s2_valid(w)          &&
                            !s2_hit(w)            &&
                            !s2_nack_hit(w)       &&
                            !s2_nack_victim(w)    &&
                            !s2_nack_data(w)      &&
                            !s2_nack_wb(w)        &&
                             s2_type.isOneOf(t_lsu, t_prefetch)             &&
                            !(io.lsu.exception && s2_req(w).uop.uses_ldq)   &&
                             (isPrefetch(s2_req(w).uop.mem_cmd) ||
                              isRead(s2_req(w).uop.mem_cmd)     ||
                              isWrite(s2_req(w).uop.mem_cmd))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:867-869
```scala
  // load data gen
  val s2_data_word_prebypass = widthMap(w => s2_data_muxed(w) >> Cat(s2_word_idx(w), 0.U(log2Ceil(coreDataBits).W)))
  val s2_data_word = Wire(Vec(lsuWidth, UInt()))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:872-874
```scala
    new LoadGen(s2_req(w).uop.mem_size, s2_req(w).uop.mem_signed, s2_req(w).addr,
                s2_data_word(w), s2_sc && (w == 0).B, wordBytes)
  }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:876-881
```scala
  for (w <- 0 until lsuWidth) {
    io.lsu.resp(w).valid := s2_valid(w) && s2_send_resp(w)
    io.lsu.resp(w).bits.uop := s2_req(w).uop
    io.lsu.resp(w).bits.data := loadgen(w).data | s2_sc_fail
    io.lsu.resp(w).bits.is_hella := s2_req(w).is_hella
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:883-886
```scala

    io.lsu.nack(w).valid := s2_valid(w) && s2_send_nack(w)
    io.lsu.nack(w).bits  := s2_req(w)
    assert(!(io.lsu.nack(w).valid && s2_type =/= t_lsu))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:887-890
```scala

    io.lsu.store_ack(w).valid := s2_valid(w) && s2_send_store_ack(w) && (w == 0).B
    io.lsu.store_ack(w).bits  := s2_req(w)
  }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:895-897
```scala
  val s3_req   = Wire(new BoomDCacheReq)
  s3_req := RegNext(s2_req(0))
  val s3_valid = RegNext(s2_valid(0) && s2_hit(0) && isWrite(s2_req(0).uop.mem_cmd) &&
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:912-916
```scala

  val s3_bypass = widthMap(w => s3_valid && ((s2_req(w).addr >> wordOffBits) === (s3_req.addr >> wordOffBits)))
  val s4_bypass = widthMap(w => s4_valid && ((s2_req(w).addr >> wordOffBits) === (s4_req.addr >> wordOffBits)))
  val s5_bypass = widthMap(w => s5_valid && ((s2_req(w).addr >> wordOffBits) === (s5_req.addr >> wordOffBits)))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:918-922
```scala
  for (w <- 0 until lsuWidth) {
    s2_data_word(w) := Mux(s3_bypass(w), s3_req.data,
                       Mux(s4_bypass(w), s4_req.data,
                       Mux(s5_bypass(w), s5_req.data,
                                         s2_data_word_prebypass(w))))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:930-932
```scala

  s3_req.data := amoalu.io.out
  val s3_way   = RegNext(s2_tag_match_way(0))
```

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

### generators/boom/src/main/scala/v4/util/util.scala:125-127
```scala
{
  def apply(msk1: UInt, msk2: UInt): Bool = (msk1 & msk2) =/= 0.U
}
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:11-13
```scala
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

### generators/rocket-chip/src/main/scala/rocket/Consts.scala:86-91
```scala
  def isAMOArithmetic(cmd: UInt) = cmd.isOneOf(M_XA_ADD, M_XA_MIN, M_XA_MAX, M_XA_MINU, M_XA_MAXU)
  def isAMO(cmd: UInt) = isAMOLogical(cmd) || isAMOArithmetic(cmd)
  def isPrefetch(cmd: UInt) = cmd === M_PFR || cmd === M_PFW
  def isRead(cmd: UInt) = cmd.isOneOf(M_XRD, M_HLVX, M_XLR, M_XSC) || isAMO(cmd)
  def isWrite(cmd: UInt) = cmd === M_XWR || cmd === M_PWR || cmd === M_XSC || isAMO(cmd)
  def isWriteIntent(cmd: UInt) = isWrite(cmd) || cmd === M_PFW || cmd === M_XLR
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:49-51
```scala
  /** Is the block's data present in this cache */
  def isValid(dummy: Int = 0): Bool = state > ClientStates.Nothing
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
[1382] FIRRTL:199151 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s1_valid[0], s1_valid_REG
[1400] FIRRTL:199169 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:647:43 KIND:node :: node _s1_nack_T = bits(s1_req[0].addr, 11, 6)
[1401] FIRRTL:199170 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:647:59 KIND:node :: node _s1_nack_T_1 = eq(_s1_nack_T, prober.io.meta_write.bits.idx)
[1402] FIRRTL:199171 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:647:96 KIND:node :: node _s1_nack_T_2 = eq(prober.io.req.ready, UInt<1>(0h0))
[1403] FIRRTL:199172 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:647:93 KIND:node :: node s1_nack_0 = and(_s1_nack_T_1, _s1_nack_T_2)
[1414] FIRRTL:199183 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:95 KIND:node :: node _s1_tag_eq_way_T = shr(s1_req[0].addr, 12)
[1415] FIRRTL:199184 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:79 KIND:node :: node _s1_tag_eq_way_T_1 = eq(meta_0.io.resp[0].tag, _s1_tag_eq_way_T)
[1416] FIRRTL:199185 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:95 KIND:node :: node _s1_tag_eq_way_T_2 = shr(s1_req[0].addr, 12)
[1417] FIRRTL:199186 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:79 KIND:node :: node _s1_tag_eq_way_T_3 = eq(meta_0.io.resp[1].tag, _s1_tag_eq_way_T_2)
[1418] FIRRTL:199187 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:95 KIND:node :: node _s1_tag_eq_way_T_4 = shr(s1_req[0].addr, 12)
[1419] FIRRTL:199188 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:79 KIND:node :: node _s1_tag_eq_way_T_5 = eq(meta_0.io.resp[2].tag, _s1_tag_eq_way_T_4)
[1420] FIRRTL:199189 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:95 KIND:node :: node _s1_tag_eq_way_T_6 = shr(s1_req[0].addr, 12)
[1421] FIRRTL:199190 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:79 KIND:node :: node _s1_tag_eq_way_T_7 = eq(meta_0.io.resp[3].tag, _s1_tag_eq_way_T_6)
[1423] FIRRTL:199192 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_eq_way_WIRE[0], _s1_tag_eq_way_T_1
[1424] FIRRTL:199193 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_eq_way_WIRE[1], _s1_tag_eq_way_T_3
[1425] FIRRTL:199194 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_eq_way_WIRE[2], _s1_tag_eq_way_T_5
[1426] FIRRTL:199195 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_eq_way_WIRE[3], _s1_tag_eq_way_T_7
[1427] FIRRTL:199196 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:110 KIND:node :: node s1_tag_eq_way_lo = cat(_s1_tag_eq_way_WIRE[1], _s1_tag_eq_way_WIRE[0])
[1428] FIRRTL:199197 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:110 KIND:node :: node s1_tag_eq_way_hi = cat(_s1_tag_eq_way_WIRE[3], _s1_tag_eq_way_WIRE[2])
[1429] FIRRTL:199198 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:657:110 KIND:node :: node _s1_tag_eq_way_T_8 = cat(s1_tag_eq_way_hi, s1_tag_eq_way_lo)
[1431] FIRRTL:199200 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s1_tag_eq_way[0], _s1_tag_eq_way_T_8
[1432] FIRRTL:199201 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:659:38 KIND:node :: node _s1_tag_match_way_T = eq(s1_type, UInt<3>(0h0))
[1433] FIRRTL:199202 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:660:38 KIND:node :: node _s1_tag_match_way_T_1 = eq(s1_type, UInt<3>(0h2))
[1434] FIRRTL:199203 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:661:38 KIND:node :: node _s1_tag_match_way_T_2 = eq(s1_type, UInt<3>(0h3))
[1435] FIRRTL:199204 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:63 KIND:node :: node _s1_tag_match_way_T_3 = bits(s1_tag_eq_way[0], 0, 0)
[1436] FIRRTL:199205 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:50:45 KIND:node :: node _s1_tag_match_way_T_4 = gt(meta_0.io.resp[0].coh.state, UInt<2>(0h0))
[1437] FIRRTL:199206 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:67 KIND:node :: node _s1_tag_match_way_T_5 = and(_s1_tag_match_way_T_3, _s1_tag_match_way_T_4)
[1438] FIRRTL:199207 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:63 KIND:node :: node _s1_tag_match_way_T_6 = bits(s1_tag_eq_way[0], 1, 1)
[1439] FIRRTL:199208 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:50:45 KIND:node :: node _s1_tag_match_way_T_7 = gt(meta_0.io.resp[1].coh.state, UInt<2>(0h0))
[1440] FIRRTL:199209 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:67 KIND:node :: node _s1_tag_match_way_T_8 = and(_s1_tag_match_way_T_6, _s1_tag_match_way_T_7)
[1441] FIRRTL:199210 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:63 KIND:node :: node _s1_tag_match_way_T_9 = bits(s1_tag_eq_way[0], 2, 2)
[1442] FIRRTL:199211 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:50:45 KIND:node :: node _s1_tag_match_way_T_10 = gt(meta_0.io.resp[2].coh.state, UInt<2>(0h0))
[1443] FIRRTL:199212 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:67 KIND:node :: node _s1_tag_match_way_T_11 = and(_s1_tag_match_way_T_9, _s1_tag_match_way_T_10)
[1444] FIRRTL:199213 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:63 KIND:node :: node _s1_tag_match_way_T_12 = bits(s1_tag_eq_way[0], 3, 3)
[1445] FIRRTL:199214 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:50:45 KIND:node :: node _s1_tag_match_way_T_13 = gt(meta_0.io.resp[3].coh.state, UInt<2>(0h0))
[1446] FIRRTL:199215 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:67 KIND:node :: node _s1_tag_match_way_T_14 = and(_s1_tag_match_way_T_12, _s1_tag_match_way_T_13)
[1448] FIRRTL:199217 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_match_way_WIRE[0], _s1_tag_match_way_T_5
[1449] FIRRTL:199218 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_match_way_WIRE[1], _s1_tag_match_way_T_8
[1450] FIRRTL:199219 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_match_way_WIRE[2], _s1_tag_match_way_T_11
[1451] FIRRTL:199220 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:656:47 KIND:connect :: connect _s1_tag_match_way_WIRE[3], _s1_tag_match_way_T_14
[1452] FIRRTL:199221 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:104 KIND:node :: node s1_tag_match_way_lo = cat(_s1_tag_match_way_WIRE[1], _s1_tag_match_way_WIRE[0])
[1453] FIRRTL:199222 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:104 KIND:node :: node s1_tag_match_way_hi = cat(_s1_tag_match_way_WIRE[3], _s1_tag_match_way_WIRE[2])
[1454] FIRRTL:199223 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:662:104 KIND:node :: node _s1_tag_match_way_T_15 = cat(s1_tag_match_way_hi, s1_tag_match_way_lo)
[1455] FIRRTL:199224 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:661:29 KIND:node :: node _s1_tag_match_way_T_16 = mux(_s1_tag_match_way_T_2, s1_mshr_meta_read_way_en, _s1_tag_match_way_T_15)
[1456] FIRRTL:199225 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:660:29 KIND:node :: node _s1_tag_match_way_T_17 = mux(_s1_tag_match_way_T_1, s1_wb_way_en, _s1_tag_match_way_T_16)
[1457] FIRRTL:199226 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:659:29 KIND:node :: node _s1_tag_match_way_T_18 = mux(_s1_tag_match_way_T, s1_replay_way_en, _s1_tag_match_way_T_17)
[1459] FIRRTL:199228 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s1_tag_match_way[0], _s1_tag_match_way_T_18
[1460] FIRRTL:199229 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:664:52 KIND:node :: node _s1_wb_idx_matches_T = bits(s1_req[0].addr, 11, 6)
[1461] FIRRTL:199230 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:664:79 KIND:node :: node _s1_wb_idx_matches_T_1 = eq(_s1_wb_idx_matches_T, wb.io.idx.bits)
[1462] FIRRTL:199231 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:664:99 KIND:node :: node _s1_wb_idx_matches_T_2 = and(_s1_wb_idx_matches_T_1, wb.io.idx.valid)
[1464] FIRRTL:199233 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s1_wb_idx_matches[0], _s1_wb_idx_matches_T_2
[1467] FIRRTL:199236 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:670:25 KIND:connect :: connect s2_req, s1_req
[1469] FIRRTL:199238 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:671:25 KIND:connect :: connect s2_type, s1_type
[1470] FIRRTL:199239 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:674:26 KIND:node :: node _s2_valid_T = eq(io.lsu.s1_kill[0], UInt<1>(0h0))
[1471] FIRRTL:199240 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:673:39 KIND:node :: node _s2_valid_T_1 = and(s1_valid[0], _s2_valid_T)
[1472] FIRRTL:199241 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _s2_valid_T_2 = and(io.lsu.brupdate.b1.mispredict_mask, s1_req[0].uop.br_mask)
[1473] FIRRTL:199242 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _s2_valid_T_3 = neq(_s2_valid_T_2, UInt<1>(0h0))
[1474] FIRRTL:199243 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _s2_valid_T_4 = or(_s2_valid_T_3, UInt<1>(0h0))
[1475] FIRRTL:199244 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:675:26 KIND:node :: node _s2_valid_T_5 = eq(_s2_valid_T_4, UInt<1>(0h0))
[1476] FIRRTL:199245 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:674:45 KIND:node :: node _s2_valid_T_6 = and(_s2_valid_T_1, _s2_valid_T_5)
[1477] FIRRTL:199246 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:676:45 KIND:node :: node _s2_valid_T_7 = and(io.lsu.exception, s1_req[0].uop.uses_ldq)
[1478] FIRRTL:199247 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:676:26 KIND:node :: node _s2_valid_T_8 = eq(_s2_valid_T_7, UInt<1>(0h0))
[1479] FIRRTL:199248 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:675:85 KIND:node :: node _s2_valid_T_9 = and(_s2_valid_T_6, _s2_valid_T_8)
[1480] FIRRTL:199249 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:677:56 KIND:node :: node _s2_valid_T_10 = eq(s1_type, UInt<3>(0h4))
[1481] FIRRTL:199250 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:677:44 KIND:node :: node _s2_valid_T_11 = and(s2_store_failed, _s2_valid_T_10)
[1482] FIRRTL:199251 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:677:67 KIND:node :: node _s2_valid_T_12 = and(_s2_valid_T_11, s1_req[0].uop.uses_stq)
[1483] FIRRTL:199252 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:677:26 KIND:node :: node _s2_valid_T_13 = eq(_s2_valid_T_12, UInt<1>(0h0))
[1484] FIRRTL:199253 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:676:72 KIND:node :: node _s2_valid_T_14 = and(_s2_valid_T_9, _s2_valid_T_13)
[1486] FIRRTL:199255 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:673:26 KIND:connect :: connect s2_valid_REG, _s2_valid_T_14
[1489] FIRRTL:199258 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _s2_req_0_uop_br_mask_T = not(io.lsu.brupdate.b1.resolve_mask)
[1490] FIRRTL:199259 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _s2_req_0_uop_br_mask_T_1 = and(s1_req[0].uop.br_mask, _s2_req_0_uop_br_mask_T)
[1491] FIRRTL:199260 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:679:27 KIND:connect :: connect s2_req[0].uop.br_mask, _s2_req_0_uop_br_mask_T_1
[1493] FIRRTL:199262 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:681:33 KIND:connect :: connect s2_tag_match_way, s1_tag_match_way
[1496] FIRRTL:199265 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:connect :: connect s2_hit_state_REG, meta_0.io.resp[0].coh
[1498] FIRRTL:199267 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:connect :: connect s2_hit_state_REG_1, meta_0.io.resp[1].coh
[1500] FIRRTL:199269 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:connect :: connect s2_hit_state_REG_2, meta_0.io.resp[2].coh
[1502] FIRRTL:199271 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:683:93 KIND:connect :: connect s2_hit_state_REG_3, meta_0.io.resp[3].coh
[1792] FIRRTL:199561 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:692:34 KIND:connect :: connect s2_wb_idx_matches, s1_wb_idx_matches
[1805] FIRRTL:199574 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:37 KIND:node :: node _s2_sc_T = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[1808] FIRRTL:199577 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:51 KIND:node :: node _s2_sc_T_1 = eq(s2_sc_REG, UInt<1>(0h0))
[1809] FIRRTL:199578 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:83 KIND:node :: node _s2_sc_T_2 = eq(s2_type, UInt<3>(0h0))
[1810] FIRRTL:199579 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:72 KIND:node :: node _s2_sc_T_3 = or(_s2_sc_T_1, _s2_sc_T_2)
[1811] FIRRTL:199580 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:702:47 KIND:node :: node s2_sc = and(_s2_sc_T, _s2_sc_T_3)
[1817] FIRRTL:199586 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:704:29 KIND:node :: node _s2_sc_fail_T = eq(s2_lrsc_addr_match[0], UInt<1>(0h0))
[1818] FIRRTL:199587 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:704:26 KIND:node :: node s2_sc_fail = and(s2_sc, _s2_sc_fail_T)
[1876] FIRRTL:199645 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:746:21 KIND:connect :: connect s2_data[0][0], data.io.resp[0][0]
[1877] FIRRTL:199646 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:746:21 KIND:connect :: connect s2_data[0][1], data.io.resp[0][1]
[1878] FIRRTL:199647 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:746:21 KIND:connect :: connect s2_data[0][2], data.io.resp[0][2]
[1879] FIRRTL:199648 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:746:21 KIND:connect :: connect s2_data[0][3], data.io.resp[0][3]
[1880] FIRRTL:199649 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_data_muxed_T = bits(s2_tag_match_way[0], 0, 0)
[1881] FIRRTL:199650 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_data_muxed_T_1 = bits(s2_tag_match_way[0], 1, 1)
[1882] FIRRTL:199651 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_data_muxed_T_2 = bits(s2_tag_match_way[0], 2, 2)
[1883] FIRRTL:199652 SRC:src/main/scala/chisel3/util/Mux.scala:32:36 KIND:node :: node _s2_data_muxed_T_3 = bits(s2_tag_match_way[0], 3, 3)
[1884] FIRRTL:199653 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_4 = mux(_s2_data_muxed_T, s2_data[0][0], UInt<1>(0h0))
[1885] FIRRTL:199654 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_5 = mux(_s2_data_muxed_T_1, s2_data[0][1], UInt<1>(0h0))
[1886] FIRRTL:199655 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_6 = mux(_s2_data_muxed_T_2, s2_data[0][2], UInt<1>(0h0))
[1887] FIRRTL:199656 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_7 = mux(_s2_data_muxed_T_3, s2_data[0][3], UInt<1>(0h0))
[1888] FIRRTL:199657 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_8 = or(_s2_data_muxed_T_4, _s2_data_muxed_T_5)
[1889] FIRRTL:199658 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_9 = or(_s2_data_muxed_T_8, _s2_data_muxed_T_6)
[1890] FIRRTL:199659 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _s2_data_muxed_T_10 = or(_s2_data_muxed_T_9, _s2_data_muxed_T_7)
[1892] FIRRTL:199661 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _s2_data_muxed_WIRE, _s2_data_muxed_T_10
[1894] FIRRTL:199663 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_data_muxed[0], _s2_data_muxed_WIRE
[1896] FIRRTL:199665 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_word_idx[0], UInt<1>(0h0)
[1984] FIRRTL:199753 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:760:39 KIND:connect :: connect _s2_nack_hit_WIRE[0], s1_nack_0
[1986] FIRRTL:199755 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:760:31 KIND:connect :: connect s2_nack_hit, _s2_nack_hit_WIRE
[1998] FIRRTL:199767 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:766:60 KIND:connect :: connect s2_nack_data_REG, data.io.s1_nacks[0]
[2029] FIRRTL:199798 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:773:12 KIND:connect :: connect s2_send_resp_REG, s1_send_resp_or_nack[0]
[2030] FIRRTL:199799 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:25 KIND:node :: node _s2_send_resp_T = or(s2_nack_hit[0], s2_nack_victim[0])
[2031] FIRRTL:199800 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:46 KIND:node :: node _s2_send_resp_T_1 = or(_s2_send_resp_T, s2_nack_data[0])
[2032] FIRRTL:199801 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:8 KIND:node :: node _s2_send_resp_T_2 = eq(_s2_send_resp_T_1, UInt<1>(0h0))
[2033] FIRRTL:199802 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:77 KIND:node :: node _s2_send_resp_T_3 = eq(s2_type, UInt<3>(0h0))
[2034] FIRRTL:199803 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:66 KIND:node :: node _s2_send_resp_T_4 = or(_s2_send_resp_T_2, _s2_send_resp_T_3)
[2035] FIRRTL:199804 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:773:38 KIND:node :: node _s2_send_resp_T_5 = and(s2_send_resp_REG, _s2_send_resp_T_4)
[2036] FIRRTL:199805 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:774:91 KIND:node :: node _s2_send_resp_T_6 = and(_s2_send_resp_T_5, s2_hit[0])
[2037] FIRRTL:199806 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_7 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h0))
[2038] FIRRTL:199807 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_8 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h10))
[2039] FIRRTL:199808 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_9 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h6))
[2040] FIRRTL:199809 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_10 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[2041] FIRRTL:199810 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_11 = or(_s2_send_resp_T_7, _s2_send_resp_T_8)
[2042] FIRRTL:199811 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_12 = or(_s2_send_resp_T_11, _s2_send_resp_T_9)
[2043] FIRRTL:199812 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_13 = or(_s2_send_resp_T_12, _s2_send_resp_T_10)
[2044] FIRRTL:199813 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_14 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[2045] FIRRTL:199814 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_15 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[2046] FIRRTL:199815 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_16 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[2047] FIRRTL:199816 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_17 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[2048] FIRRTL:199817 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_18 = or(_s2_send_resp_T_14, _s2_send_resp_T_15)
[2049] FIRRTL:199818 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_19 = or(_s2_send_resp_T_18, _s2_send_resp_T_16)
[2050] FIRRTL:199819 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_20 = or(_s2_send_resp_T_19, _s2_send_resp_T_17)
[2051] FIRRTL:199820 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_21 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[2052] FIRRTL:199821 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_22 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[2053] FIRRTL:199822 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_23 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[2054] FIRRTL:199823 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_24 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[2055] FIRRTL:199824 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_resp_T_25 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[2056] FIRRTL:199825 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_26 = or(_s2_send_resp_T_21, _s2_send_resp_T_22)
[2057] FIRRTL:199826 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_27 = or(_s2_send_resp_T_26, _s2_send_resp_T_23)
[2058] FIRRTL:199827 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_28 = or(_s2_send_resp_T_27, _s2_send_resp_T_24)
[2059] FIRRTL:199828 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_resp_T_29 = or(_s2_send_resp_T_28, _s2_send_resp_T_25)
[2060] FIRRTL:199829 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_send_resp_T_30 = or(_s2_send_resp_T_20, _s2_send_resp_T_29)
[2061] FIRRTL:199830 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _s2_send_resp_T_31 = or(_s2_send_resp_T_13, _s2_send_resp_T_30)
[2062] FIRRTL:199831 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:775:17 KIND:node :: node _s2_send_resp_T_32 = and(_s2_send_resp_T_6, _s2_send_resp_T_31)
[2064] FIRRTL:199833 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_send_resp[0], _s2_send_resp_T_32
[2066] FIRRTL:199835 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:12 KIND:connect :: connect s2_send_store_ack_REG, s1_send_resp_or_nack[0]
[2067] FIRRTL:199836 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:41 KIND:node :: node _s2_send_store_ack_T = eq(s2_nack[0], UInt<1>(0h0))
[2068] FIRRTL:199837 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:38 KIND:node :: node _s2_send_store_ack_T_1 = and(s2_send_store_ack_REG, _s2_send_store_ack_T)
[2069] FIRRTL:199838 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _s2_send_store_ack_T_2 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[2070] FIRRTL:199839 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _s2_send_store_ack_T_3 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[2071] FIRRTL:199840 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _s2_send_store_ack_T_4 = or(_s2_send_store_ack_T_2, _s2_send_store_ack_T_3)
[2072] FIRRTL:199841 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _s2_send_store_ack_T_5 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[2073] FIRRTL:199842 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _s2_send_store_ack_T_6 = or(_s2_send_store_ack_T_4, _s2_send_store_ack_T_5)
[2074] FIRRTL:199843 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_7 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[2075] FIRRTL:199844 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_8 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[2076] FIRRTL:199845 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_9 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[2077] FIRRTL:199846 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_10 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[2078] FIRRTL:199847 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_11 = or(_s2_send_store_ack_T_7, _s2_send_store_ack_T_8)
[2079] FIRRTL:199848 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_12 = or(_s2_send_store_ack_T_11, _s2_send_store_ack_T_9)
[2080] FIRRTL:199849 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_13 = or(_s2_send_store_ack_T_12, _s2_send_store_ack_T_10)
[2081] FIRRTL:199850 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_14 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[2082] FIRRTL:199851 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_15 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[2083] FIRRTL:199852 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_16 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[2084] FIRRTL:199853 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_17 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[2085] FIRRTL:199854 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _s2_send_store_ack_T_18 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[2086] FIRRTL:199855 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_19 = or(_s2_send_store_ack_T_14, _s2_send_store_ack_T_15)
[2087] FIRRTL:199856 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_20 = or(_s2_send_store_ack_T_19, _s2_send_store_ack_T_16)
[2088] FIRRTL:199857 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_21 = or(_s2_send_store_ack_T_20, _s2_send_store_ack_T_17)
[2089] FIRRTL:199858 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _s2_send_store_ack_T_22 = or(_s2_send_store_ack_T_21, _s2_send_store_ack_T_18)
[2090] FIRRTL:199859 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _s2_send_store_ack_T_23 = or(_s2_send_store_ack_T_13, _s2_send_store_ack_T_22)
[2091] FIRRTL:199860 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _s2_send_store_ack_T_24 = or(_s2_send_store_ack_T_6, _s2_send_store_ack_T_23)
[2092] FIRRTL:199861 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:53 KIND:node :: node _s2_send_store_ack_T_25 = and(_s2_send_store_ack_T_1, _s2_send_store_ack_T_24)
[2093] FIRRTL:199862 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _s2_send_store_ack_T_26 = and(mshrs.io.req[0].ready, mshrs.io.req[0].valid)
[2094] FIRRTL:199863 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:779:18 KIND:node :: node _s2_send_store_ack_T_27 = or(s2_hit[0], _s2_send_store_ack_T_26)
[2095] FIRRTL:199864 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:778:87 KIND:node :: node _s2_send_store_ack_T_28 = and(_s2_send_store_ack_T_25, _s2_send_store_ack_T_27)
[2097] FIRRTL:199866 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_send_store_ack[0], _s2_send_store_ack_T_28
[2099] FIRRTL:199868 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:780:44 KIND:connect :: connect s2_send_nack_REG, s1_send_resp_or_nack[0]
[2100] FIRRTL:199869 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:780:70 KIND:node :: node _s2_send_nack_T = and(s2_send_nack_REG, s2_nack[0])
[2102] FIRRTL:199871 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_send_nack[0], _s2_send_nack_T
[2112] FIRRTL:199881 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:787:34 KIND:node :: node _s2_store_failed_T = and(s2_valid[0], s2_nack[0])
[2113] FIRRTL:199882 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:787:48 KIND:node :: node _s2_store_failed_T_1 = and(_s2_store_failed_T, s2_send_nack[0])
[2114] FIRRTL:199883 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:787:67 KIND:node :: node _s2_store_failed_T_2 = and(_s2_store_failed_T_1, s2_req[0].uop.uses_stq)
[2115] FIRRTL:199884 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:787:19 KIND:connect :: connect s2_store_failed, _s2_store_failed_T_2
[2116] FIRRTL:199885 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:792:29 KIND:node :: node _mshrs_io_req_0_valid_T = eq(s2_hit[0], UInt<1>(0h0))
[2117] FIRRTL:199886 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:791:51 KIND:node :: node _mshrs_io_req_0_valid_T_1 = and(s2_valid[0], _mshrs_io_req_0_valid_T)
[2118] FIRRTL:199887 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:793:29 KIND:node :: node _mshrs_io_req_0_valid_T_2 = eq(s2_nack_hit[0], UInt<1>(0h0))
[2119] FIRRTL:199888 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:792:51 KIND:node :: node _mshrs_io_req_0_valid_T_3 = and(_mshrs_io_req_0_valid_T_1, _mshrs_io_req_0_valid_T_2)
[2120] FIRRTL:199889 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:794:29 KIND:node :: node _mshrs_io_req_0_valid_T_4 = eq(s2_nack_victim[0], UInt<1>(0h0))
[2121] FIRRTL:199890 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:793:51 KIND:node :: node _mshrs_io_req_0_valid_T_5 = and(_mshrs_io_req_0_valid_T_3, _mshrs_io_req_0_valid_T_4)
[2122] FIRRTL:199891 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:795:29 KIND:node :: node _mshrs_io_req_0_valid_T_6 = eq(s2_nack_data[0], UInt<1>(0h0))
[2123] FIRRTL:199892 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:794:51 KIND:node :: node _mshrs_io_req_0_valid_T_7 = and(_mshrs_io_req_0_valid_T_5, _mshrs_io_req_0_valid_T_6)
[2124] FIRRTL:199893 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:796:29 KIND:node :: node _mshrs_io_req_0_valid_T_8 = eq(s2_nack_wb[0], UInt<1>(0h0))
[2125] FIRRTL:199894 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:795:51 KIND:node :: node _mshrs_io_req_0_valid_T_9 = and(_mshrs_io_req_0_valid_T_7, _mshrs_io_req_0_valid_T_8)
[2126] FIRRTL:199895 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_10 = eq(s2_type, UInt<3>(0h4))
[2127] FIRRTL:199896 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_11 = eq(s2_type, UInt<3>(0h5))
[2128] FIRRTL:199897 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_12 = or(_mshrs_io_req_0_valid_T_10, _mshrs_io_req_0_valid_T_11)
[2129] FIRRTL:199898 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:796:51 KIND:node :: node _mshrs_io_req_0_valid_T_13 = and(_mshrs_io_req_0_valid_T_9, _mshrs_io_req_0_valid_T_12)
[2130] FIRRTL:199899 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:798:48 KIND:node :: node _mshrs_io_req_0_valid_T_14 = and(io.lsu.exception, s2_req[0].uop.uses_ldq)
[2131] FIRRTL:199900 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:798:29 KIND:node :: node _mshrs_io_req_0_valid_T_15 = eq(_mshrs_io_req_0_valid_T_14, UInt<1>(0h0))
[2132] FIRRTL:199901 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:797:77 KIND:node :: node _mshrs_io_req_0_valid_T_16 = and(_mshrs_io_req_0_valid_T_13, _mshrs_io_req_0_valid_T_15)
[2133] FIRRTL:199902 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:35 KIND:node :: node _mshrs_io_req_0_valid_T_17 = eq(s2_req[0].uop.mem_cmd, UInt<2>(0h2))
[2134] FIRRTL:199903 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:52 KIND:node :: node _mshrs_io_req_0_valid_T_18 = eq(s2_req[0].uop.mem_cmd, UInt<2>(0h3))
[2135] FIRRTL:199904 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:88:45 KIND:node :: node _mshrs_io_req_0_valid_T_19 = or(_mshrs_io_req_0_valid_T_17, _mshrs_io_req_0_valid_T_18)
[2136] FIRRTL:199905 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_20 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h0))
[2137] FIRRTL:199906 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_21 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h10))
[2138] FIRRTL:199907 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_22 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h6))
[2139] FIRRTL:199908 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_23 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[2140] FIRRTL:199909 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_24 = or(_mshrs_io_req_0_valid_T_20, _mshrs_io_req_0_valid_T_21)
[2141] FIRRTL:199910 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_25 = or(_mshrs_io_req_0_valid_T_24, _mshrs_io_req_0_valid_T_22)
[2142] FIRRTL:199911 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_26 = or(_mshrs_io_req_0_valid_T_25, _mshrs_io_req_0_valid_T_23)
[2143] FIRRTL:199912 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_27 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[2144] FIRRTL:199913 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_28 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[2145] FIRRTL:199914 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_29 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[2146] FIRRTL:199915 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_30 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[2147] FIRRTL:199916 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_31 = or(_mshrs_io_req_0_valid_T_27, _mshrs_io_req_0_valid_T_28)
[2148] FIRRTL:199917 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_32 = or(_mshrs_io_req_0_valid_T_31, _mshrs_io_req_0_valid_T_29)
[2149] FIRRTL:199918 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_33 = or(_mshrs_io_req_0_valid_T_32, _mshrs_io_req_0_valid_T_30)
[2150] FIRRTL:199919 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_34 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[2151] FIRRTL:199920 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_35 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[2152] FIRRTL:199921 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_36 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[2153] FIRRTL:199922 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_37 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[2154] FIRRTL:199923 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_38 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[2155] FIRRTL:199924 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_39 = or(_mshrs_io_req_0_valid_T_34, _mshrs_io_req_0_valid_T_35)
[2156] FIRRTL:199925 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_40 = or(_mshrs_io_req_0_valid_T_39, _mshrs_io_req_0_valid_T_36)
[2157] FIRRTL:199926 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_41 = or(_mshrs_io_req_0_valid_T_40, _mshrs_io_req_0_valid_T_37)
[2158] FIRRTL:199927 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_42 = or(_mshrs_io_req_0_valid_T_41, _mshrs_io_req_0_valid_T_38)
[2159] FIRRTL:199928 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _mshrs_io_req_0_valid_T_43 = or(_mshrs_io_req_0_valid_T_33, _mshrs_io_req_0_valid_T_42)
[2160] FIRRTL:199929 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:89:68 KIND:node :: node _mshrs_io_req_0_valid_T_44 = or(_mshrs_io_req_0_valid_T_26, _mshrs_io_req_0_valid_T_43)
[2161] FIRRTL:199930 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:799:65 KIND:node :: node _mshrs_io_req_0_valid_T_45 = or(_mshrs_io_req_0_valid_T_19, _mshrs_io_req_0_valid_T_44)
[2162] FIRRTL:199931 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:32 KIND:node :: node _mshrs_io_req_0_valid_T_46 = eq(s2_req[0].uop.mem_cmd, UInt<1>(0h1))
[2163] FIRRTL:199932 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:49 KIND:node :: node _mshrs_io_req_0_valid_T_47 = eq(s2_req[0].uop.mem_cmd, UInt<5>(0h11))
[2164] FIRRTL:199933 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:42 KIND:node :: node _mshrs_io_req_0_valid_T_48 = or(_mshrs_io_req_0_valid_T_46, _mshrs_io_req_0_valid_T_47)
[2165] FIRRTL:199934 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:66 KIND:node :: node _mshrs_io_req_0_valid_T_49 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h7))
[2166] FIRRTL:199935 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:59 KIND:node :: node _mshrs_io_req_0_valid_T_50 = or(_mshrs_io_req_0_valid_T_48, _mshrs_io_req_0_valid_T_49)
[2167] FIRRTL:199936 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_51 = eq(s2_req[0].uop.mem_cmd, UInt<3>(0h4))
[2168] FIRRTL:199937 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_52 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h9))
[2169] FIRRTL:199938 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_53 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0ha))
[2170] FIRRTL:199939 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_54 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hb))
[2171] FIRRTL:199940 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_55 = or(_mshrs_io_req_0_valid_T_51, _mshrs_io_req_0_valid_T_52)
[2172] FIRRTL:199941 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_56 = or(_mshrs_io_req_0_valid_T_55, _mshrs_io_req_0_valid_T_53)
[2173] FIRRTL:199942 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_57 = or(_mshrs_io_req_0_valid_T_56, _mshrs_io_req_0_valid_T_54)
[2174] FIRRTL:199943 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_58 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0h8))
[2175] FIRRTL:199944 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_59 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hc))
[2176] FIRRTL:199945 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_60 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hd))
[2177] FIRRTL:199946 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_61 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0he))
[2178] FIRRTL:199947 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _mshrs_io_req_0_valid_T_62 = eq(s2_req[0].uop.mem_cmd, UInt<4>(0hf))
[2179] FIRRTL:199948 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_63 = or(_mshrs_io_req_0_valid_T_58, _mshrs_io_req_0_valid_T_59)
[2180] FIRRTL:199949 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_64 = or(_mshrs_io_req_0_valid_T_63, _mshrs_io_req_0_valid_T_60)
[2181] FIRRTL:199950 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_65 = or(_mshrs_io_req_0_valid_T_64, _mshrs_io_req_0_valid_T_61)
[2182] FIRRTL:199951 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _mshrs_io_req_0_valid_T_66 = or(_mshrs_io_req_0_valid_T_65, _mshrs_io_req_0_valid_T_62)
[2183] FIRRTL:199952 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:87:44 KIND:node :: node _mshrs_io_req_0_valid_T_67 = or(_mshrs_io_req_0_valid_T_57, _mshrs_io_req_0_valid_T_66)
[2184] FIRRTL:199953 SRC:generators/rocket-chip/src/main/scala/rocket/Consts.scala:90:76 KIND:node :: node _mshrs_io_req_0_valid_T_68 = or(_mshrs_io_req_0_valid_T_50, _mshrs_io_req_0_valid_T_67)
[2185] FIRRTL:199954 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:800:65 KIND:node :: node _mshrs_io_req_0_valid_T_69 = or(_mshrs_io_req_0_valid_T_45, _mshrs_io_req_0_valid_T_68)
[2186] FIRRTL:199955 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:798:77 KIND:node :: node _mshrs_io_req_0_valid_T_70 = and(_mshrs_io_req_0_valid_T_16, _mshrs_io_req_0_valid_T_69)
[2187] FIRRTL:199956 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:791:27 KIND:connect :: connect mshrs.io.req[0].valid, _mshrs_io_req_0_valid_T_70
[2730] FIRRTL:200499 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:868:69 KIND:node :: node _s2_data_word_prebypass_T = cat(s2_word_idx[0], UInt<6>(0h0))
[2731] FIRRTL:200500 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:868:63 KIND:node :: node _s2_data_word_prebypass_T_1 = dshr(s2_data_muxed[0], _s2_data_word_prebypass_T)
[2733] FIRRTL:200502 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s2_data_word_prebypass[0], _s2_data_word_prebypass_T_1
[2735] FIRRTL:200504 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:873:40 KIND:node :: node _T_102 = and(s2_sc, UInt<1>(0h1))
[2737] FIRRTL:200506 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:12:8 KIND:connect :: connect size, s2_req[0].uop.mem_size
[2739] FIRRTL:200508 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:877:41 KIND:node :: node _io_lsu_resp_0_valid_T = and(s2_valid[0], s2_send_resp[0])
[2740] FIRRTL:200509 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:877:26 KIND:connect :: connect io.lsu.resp[0].valid, _io_lsu_resp_0_valid_T
[2741] FIRRTL:200510 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:878:29 KIND:connect :: connect io.lsu.resp[0].bits.uop, s2_req[0].uop
[2742] FIRRTL:200511 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T = bits(s2_req[0].addr, 2, 2)
[2743] FIRRTL:200512 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_1 = bits(s2_data_word[0], 63, 32)
[2744] FIRRTL:200513 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_2 = bits(s2_data_word[0], 31, 0)
[2745] FIRRTL:200514 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_lsu_resp_0_bits_data_shifted = mux(_io_lsu_resp_0_bits_data_shifted_T, _io_lsu_resp_0_bits_data_shifted_T_1, _io_lsu_resp_0_bits_data_shifted_T_2)
[2746] FIRRTL:200515 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_lsu_resp_0_bits_data_doZero = and(UInt<1>(0h0), _T_102)
[2747] FIRRTL:200516 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_lsu_resp_0_bits_data_zeroed = mux(io_lsu_resp_0_bits_data_doZero, UInt<1>(0h0), io_lsu_resp_0_bits_data_shifted)
[2748] FIRRTL:200517 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_lsu_resp_0_bits_data_T = eq(size, UInt<2>(0h2))
[2749] FIRRTL:200518 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_lsu_resp_0_bits_data_T_1 = or(_io_lsu_resp_0_bits_data_T, io_lsu_resp_0_bits_data_doZero)
[2750] FIRRTL:200519 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_lsu_resp_0_bits_data_T_2 = bits(io_lsu_resp_0_bits_data_zeroed, 31, 31)
[2751] FIRRTL:200520 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_lsu_resp_0_bits_data_T_3 = and(s2_req[0].uop.mem_signed, _io_lsu_resp_0_bits_data_T_2)
[2752] FIRRTL:200521 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_lsu_resp_0_bits_data_T_4 = mux(_io_lsu_resp_0_bits_data_T_3, UInt<32>(0hffffffff), UInt<32>(0h0))
[2753] FIRRTL:200522 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_lsu_resp_0_bits_data_T_5 = bits(s2_data_word[0], 63, 32)
[2754] FIRRTL:200523 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_lsu_resp_0_bits_data_T_6 = mux(_io_lsu_resp_0_bits_data_T_1, _io_lsu_resp_0_bits_data_T_4, _io_lsu_resp_0_bits_data_T_5)
[2755] FIRRTL:200524 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_lsu_resp_0_bits_data_T_7 = cat(_io_lsu_resp_0_bits_data_T_6, io_lsu_resp_0_bits_data_zeroed)
[2756] FIRRTL:200525 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_3 = bits(s2_req[0].addr, 1, 1)
[2757] FIRRTL:200526 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_4 = bits(_io_lsu_resp_0_bits_data_T_7, 31, 16)
[2758] FIRRTL:200527 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_5 = bits(_io_lsu_resp_0_bits_data_T_7, 15, 0)
[2759] FIRRTL:200528 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_lsu_resp_0_bits_data_shifted_1 = mux(_io_lsu_resp_0_bits_data_shifted_T_3, _io_lsu_resp_0_bits_data_shifted_T_4, _io_lsu_resp_0_bits_data_shifted_T_5)
[2760] FIRRTL:200529 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_lsu_resp_0_bits_data_doZero_1 = and(UInt<1>(0h0), _T_102)
[2761] FIRRTL:200530 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_lsu_resp_0_bits_data_zeroed_1 = mux(io_lsu_resp_0_bits_data_doZero_1, UInt<1>(0h0), io_lsu_resp_0_bits_data_shifted_1)
[2762] FIRRTL:200531 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_lsu_resp_0_bits_data_T_8 = eq(size, UInt<1>(0h1))
[2763] FIRRTL:200532 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_lsu_resp_0_bits_data_T_9 = or(_io_lsu_resp_0_bits_data_T_8, io_lsu_resp_0_bits_data_doZero_1)
[2764] FIRRTL:200533 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_lsu_resp_0_bits_data_T_10 = bits(io_lsu_resp_0_bits_data_zeroed_1, 15, 15)
[2765] FIRRTL:200534 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_lsu_resp_0_bits_data_T_11 = and(s2_req[0].uop.mem_signed, _io_lsu_resp_0_bits_data_T_10)
[2766] FIRRTL:200535 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_lsu_resp_0_bits_data_T_12 = mux(_io_lsu_resp_0_bits_data_T_11, UInt<48>(0hffffffffffff), UInt<48>(0h0))
[2767] FIRRTL:200536 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_lsu_resp_0_bits_data_T_13 = bits(_io_lsu_resp_0_bits_data_T_7, 63, 16)
[2768] FIRRTL:200537 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_lsu_resp_0_bits_data_T_14 = mux(_io_lsu_resp_0_bits_data_T_9, _io_lsu_resp_0_bits_data_T_12, _io_lsu_resp_0_bits_data_T_13)
[2769] FIRRTL:200538 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_lsu_resp_0_bits_data_T_15 = cat(_io_lsu_resp_0_bits_data_T_14, io_lsu_resp_0_bits_data_zeroed_1)
[2770] FIRRTL:200539 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:29 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_6 = bits(s2_req[0].addr, 0, 0)
[2771] FIRRTL:200540 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:37 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_7 = bits(_io_lsu_resp_0_bits_data_T_15, 15, 8)
[2772] FIRRTL:200541 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:55 KIND:node :: node _io_lsu_resp_0_bits_data_shifted_T_8 = bits(_io_lsu_resp_0_bits_data_T_15, 7, 0)
[2773] FIRRTL:200542 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:42:24 KIND:node :: node io_lsu_resp_0_bits_data_shifted_2 = mux(_io_lsu_resp_0_bits_data_shifted_T_6, _io_lsu_resp_0_bits_data_shifted_T_7, _io_lsu_resp_0_bits_data_shifted_T_8)
[2774] FIRRTL:200543 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:43:31 KIND:node :: node io_lsu_resp_0_bits_data_doZero_2 = and(UInt<1>(0h1), _T_102)
[2775] FIRRTL:200544 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:44:23 KIND:node :: node io_lsu_resp_0_bits_data_zeroed_2 = mux(io_lsu_resp_0_bits_data_doZero_2, UInt<1>(0h0), io_lsu_resp_0_bits_data_shifted_2)
[2776] FIRRTL:200545 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:26 KIND:node :: node _io_lsu_resp_0_bits_data_T_16 = eq(size, UInt<1>(0h0))
[2777] FIRRTL:200546 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:34 KIND:node :: node _io_lsu_resp_0_bits_data_T_17 = or(_io_lsu_resp_0_bits_data_T_16, io_lsu_resp_0_bits_data_doZero_2)
[2778] FIRRTL:200547 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:81 KIND:node :: node _io_lsu_resp_0_bits_data_T_18 = bits(io_lsu_resp_0_bits_data_zeroed_2, 7, 7)
[2779] FIRRTL:200548 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:72 KIND:node :: node _io_lsu_resp_0_bits_data_T_19 = and(s2_req[0].uop.mem_signed, _io_lsu_resp_0_bits_data_T_18)
[2780] FIRRTL:200549 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:49 KIND:node :: node _io_lsu_resp_0_bits_data_T_20 = mux(_io_lsu_resp_0_bits_data_T_19, UInt<56>(0hffffffffffffff), UInt<56>(0h0))
[2781] FIRRTL:200550 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:94 KIND:node :: node _io_lsu_resp_0_bits_data_T_21 = bits(_io_lsu_resp_0_bits_data_T_15, 63, 8)
[2782] FIRRTL:200551 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:20 KIND:node :: node _io_lsu_resp_0_bits_data_T_22 = mux(_io_lsu_resp_0_bits_data_T_17, _io_lsu_resp_0_bits_data_T_20, _io_lsu_resp_0_bits_data_T_21)
[2783] FIRRTL:200552 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:45:16 KIND:node :: node _io_lsu_resp_0_bits_data_T_23 = cat(_io_lsu_resp_0_bits_data_T_22, io_lsu_resp_0_bits_data_zeroed_2)
[2784] FIRRTL:200553 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:879:49 KIND:node :: node _io_lsu_resp_0_bits_data_T_24 = or(_io_lsu_resp_0_bits_data_T_23, s2_sc_fail)
[2785] FIRRTL:200554 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:879:30 KIND:connect :: connect io.lsu.resp[0].bits.data, _io_lsu_resp_0_bits_data_T_24
[2786] FIRRTL:200555 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:880:34 KIND:connect :: connect io.lsu.resp[0].bits.is_hella, s2_req[0].is_hella
[2787] FIRRTL:200556 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:884:41 KIND:node :: node _io_lsu_nack_0_valid_T = and(s2_valid[0], s2_send_nack[0])
[2788] FIRRTL:200557 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:884:26 KIND:connect :: connect io.lsu.nack[0].valid, _io_lsu_nack_0_valid_T
[2789] FIRRTL:200558 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:885:26 KIND:connect :: connect io.lsu.nack[0].bits, s2_req[0]
[2800] FIRRTL:200569 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:888:46 KIND:node :: node _io_lsu_store_ack_0_valid_T = and(s2_valid[0], s2_send_store_ack[0])
[2801] FIRRTL:200570 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:888:70 KIND:node :: node _io_lsu_store_ack_0_valid_T_1 = and(_io_lsu_store_ack_0_valid_T, UInt<1>(0h1))
[2802] FIRRTL:200571 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:888:31 KIND:connect :: connect io.lsu.store_ack[0].valid, _io_lsu_store_ack_0_valid_T_1
[2803] FIRRTL:200572 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:889:31 KIND:connect :: connect io.lsu.store_ack[0].bits, s2_req[0]
[2810] FIRRTL:200579 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:896:10 KIND:connect :: connect s3_req, s3_req_REG
[2853] FIRRTL:200622 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:913:62 KIND:node :: node _s3_bypass_T = shr(s2_req[0].addr, 3)
[2854] FIRRTL:200623 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:913:95 KIND:node :: node _s3_bypass_T_1 = shr(s3_req.addr, 3)
[2855] FIRRTL:200624 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:913:78 KIND:node :: node _s3_bypass_T_2 = eq(_s3_bypass_T, _s3_bypass_T_1)
[2856] FIRRTL:200625 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:913:42 KIND:node :: node _s3_bypass_T_3 = and(s3_valid, _s3_bypass_T_2)
[2858] FIRRTL:200627 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s3_bypass[0], _s3_bypass_T_3
[2859] FIRRTL:200628 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:914:62 KIND:node :: node _s4_bypass_T = shr(s2_req[0].addr, 3)
[2860] FIRRTL:200629 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:914:95 KIND:node :: node _s4_bypass_T_1 = shr(s4_req.addr, 3)
[2861] FIRRTL:200630 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:914:78 KIND:node :: node _s4_bypass_T_2 = eq(_s4_bypass_T, _s4_bypass_T_1)
[2862] FIRRTL:200631 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:914:42 KIND:node :: node _s4_bypass_T_3 = and(s4_valid, _s4_bypass_T_2)
[2864] FIRRTL:200633 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s4_bypass[0], _s4_bypass_T_3
[2865] FIRRTL:200634 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:915:62 KIND:node :: node _s5_bypass_T = shr(s2_req[0].addr, 3)
[2866] FIRRTL:200635 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:915:95 KIND:node :: node _s5_bypass_T_1 = shr(s5_req.addr, 3)
[2867] FIRRTL:200636 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:915:78 KIND:node :: node _s5_bypass_T_2 = eq(_s5_bypass_T, _s5_bypass_T_1)
[2868] FIRRTL:200637 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:915:42 KIND:node :: node _s5_bypass_T_3 = and(s5_valid, _s5_bypass_T_2)
[2870] FIRRTL:200639 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:454:49 KIND:connect :: connect s5_bypass[0], _s5_bypass_T_3
[2871] FIRRTL:200640 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:921:27 KIND:node :: node _s2_data_word_0_T = mux(s5_bypass[0], s5_req.data, s2_data_word_prebypass[0])
[2872] FIRRTL:200641 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:920:27 KIND:node :: node _s2_data_word_0_T_1 = mux(s4_bypass[0], s4_req.data, _s2_data_word_0_T)
[2873] FIRRTL:200642 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:919:27 KIND:node :: node _s2_data_word_0_T_2 = mux(s3_bypass[0], s3_req.data, _s2_data_word_0_T_1)
[2874] FIRRTL:200643 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:919:21 KIND:connect :: connect s2_data_word[0], _s2_data_word_0_T_2
[2910] FIRRTL:200679 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:931:15 KIND:connect :: connect s3_req.data, amoalu.io.out
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-3-311dc24763e402d9",
  "work_unit_id": "BoomNonBlockingDCache::region-0-3",
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
