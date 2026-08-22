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

Task ID: `leaf_abstraction-LSU-region-0-5-7aada22dd0e23995`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU::region-0-5`
- module: `LSU`
- kind: `region`
- instance path: `LSU`
- leaf: `True`
- coverage complete: `True`
- raw statements: 20
- logical statements: 19
- mapped/logical source lines: 17
- registers: 0
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
   before the colliding real write in `co`. For a finite candidate vector whose unique winner is chosen by an indexed
   linear or rotated order and exposed after a fixed register delay, use
   `indexed_priority_select`. Its `candidate` is an indexed Boolean expression:
   use `bit(vector, index_var)` for a packed candidate vector, or compose
   `lookup(array, index_var)` terms with `and` / `or` / `not` when eligibility
   is computed from several indexed arrays. If lowering exposes the finite
   candidate vector as separate scalar frontier signals, use
   `indexed_cases(index_var; [candidate_0, ..., candidate_n])`; its value count
   must equal `index.count`. Do not reference a source-level array that is not
   listed in this WorkUnit's state/frontier; preserve the partition boundary by
   using the exposed scalar frontier candidates and leave their parent-local
   construction to composition;
   `priority.kind` is `linear_min`, `linear_max`, `cyclic_predecessor`, or
   `cyclic_successor`, with a `pivot` expression on cyclic forms. The cyclic
   forms use optional `pivot_position`: `last` (the backward-compatible default)
   is strict around the pivot, while `first` visits the pivot itself before
   moving in the predecessor/successor direction. `result.index` names the
   selected-index output, or uses a constant `bit`/`slice` projection when a
   register also carries an epoch bit; `result.found` is optional when RTL exposes a separate
   nonempty flag. `latency_cycles` records the
   exact sampling delay, and unreset result registers use
   `initialization: {"kind":"implicit_unconstrained"}`.
   For a scalar register whose complete one-cycle next state is selected from
   priority guarded writers, use `register_transition`. List updates in
   highest-to-lowest priority order with `priority: "first_match"`, then give
   the exact hold/fallback expression in `default`. Guards may use scalar
   Boolean `signal`/`and`/`or`/`not` expressions. For a circular pointer increment
   use `modular_increment(value, modulus)`; this means the selected expression
   is sampled at cycle t and assigned to the register at t+1, never a same-cycle
   equality. Include every RTL writer: if a writer's enclosing control is not
   grounded in the handoff, report a grounding gap rather than omitting it.
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

- `LSU::io.dmem.ll_resp.fire`
  - predicate: `io.dmem.ll_resp.valid && io.dmem.ll_resp.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.dmem.ll_resp.bits.data', 'io.dmem.ll_resp.bits.is_hella', 'io.dmem.ll_resp.bits.uop.bp_debug_if', 'io.dmem.ll_resp.bits.uop.bp_xcpt_if', 'io.dmem.ll_resp.bits.uop.br_mask', 'io.dmem.ll_resp.bits.uop.br_tag', 'io.dmem.ll_resp.bits.uop.br_type', 'io.dmem.ll_resp.bits.uop.csr_cmd', 'io.dmem.ll_resp.bits.uop.debug_fsrc', 'io.dmem.ll_resp.bits.uop.debug_inst', 'io.dmem.ll_resp.bits.uop.debug_pc', 'io.dmem.ll_resp.bits.uop.debug_tsrc', 'io.dmem.ll_resp.bits.uop.dis_col_sel', 'io.dmem.ll_resp.bits.uop.dst_rtype', 'io.dmem.ll_resp.bits.uop.edge_inst', 'io.dmem.ll_resp.bits.uop.exc_cause', 'io.dmem.ll_resp.bits.uop.exception', 'io.dmem.ll_resp.bits.uop.fcn_dw', 'io.dmem.ll_resp.bits.uop.fcn_op', 'io.dmem.ll_resp.bits.uop.flush_on_commit', 'io.dmem.ll_resp.bits.uop.fp_ctrl.div', 'io.dmem.ll_resp.bits.uop.fp_ctrl.fastpipe', 'io.dmem.ll_resp.bits.uop.fp_ctrl.fma', 'io.dmem.ll_resp.bits.uop.fp_ctrl.fromint', 'io.dmem.ll_resp.bits.uop.fp_ctrl.ldst', 'io.dmem.ll_resp.bits.uop.fp_ctrl.ren1', 'io.dmem.ll_resp.bits.uop.fp_ctrl.ren2', 'io.dmem.ll_resp.bits.uop.fp_ctrl.ren3', 'io.dmem.ll_resp.bits.uop.fp_ctrl.sqrt', 'io.dmem.ll_resp.bits.uop.fp_ctrl.swap12', 'io.dmem.ll_resp.bits.uop.fp_ctrl.swap23', 'io.dmem.ll_resp.bits.uop.fp_ctrl.toint', 'io.dmem.ll_resp.bits.uop.fp_ctrl.typeTagIn', 'io.dmem.ll_resp.bits.uop.fp_ctrl.typeTagOut', 'io.dmem.ll_resp.bits.uop.fp_ctrl.vec', 'io.dmem.ll_resp.bits.uop.fp_ctrl.wen', 'io.dmem.ll_resp.bits.uop.fp_ctrl.wflags', 'io.dmem.ll_resp.bits.uop.fp_rm', 'io.dmem.ll_resp.bits.uop.fp_typ', 'io.dmem.ll_resp.bits.uop.fp_val', 'io.dmem.ll_resp.bits.uop.frs3_en', 'io.dmem.ll_resp.bits.uop.ftq_idx', 'io.dmem.ll_resp.bits.uop.fu_code[0]', 'io.dmem.ll_resp.bits.uop.fu_code[1]', 'io.dmem.ll_resp.bits.uop.fu_code[2]', 'io.dmem.ll_resp.bits.uop.fu_code[3]', 'io.dmem.ll_resp.bits.uop.fu_code[4]', 'io.dmem.ll_resp.bits.uop.fu_code[5]', 'io.dmem.ll_resp.bits.uop.fu_code[6]', 'io.dmem.ll_resp.bits.uop.fu_code[7]', 'io.dmem.ll_resp.bits.uop.fu_code[8]', 'io.dmem.ll_resp.bits.uop.fu_code[9]', 'io.dmem.ll_resp.bits.uop.imm_packed', 'io.dmem.ll_resp.bits.uop.imm_rename', 'io.dmem.ll_resp.bits.uop.imm_sel', 'io.dmem.ll_resp.bits.uop.inst', 'io.dmem.ll_resp.bits.uop.iq_type[0]', 'io.dmem.ll_resp.bits.uop.iq_type[1]', 'io.dmem.ll_resp.bits.uop.iq_type[2]', 'io.dmem.ll_resp.bits.uop.iq_type[3]', 'io.dmem.ll_resp.bits.uop.is_amo', 'io.dmem.ll_resp.bits.uop.is_eret', 'io.dmem.ll_resp.bits.uop.is_fence', 'io.dmem.ll_resp.bits.uop.is_fencei', 'io.dmem.ll_resp.bits.uop.is_mov', 'io.dmem.ll_resp.bits.uop.is_rocc', 'io.dmem.ll_resp.bits.uop.is_rvc', 'io.dmem.ll_resp.bits.uop.is_sfb', 'io.dmem.ll_resp.bits.uop.is_sfence', 'io.dmem.ll_resp.bits.uop.is_sys_pc2epc', 'io.dmem.ll_resp.bits.uop.is_unique', 'io.dmem.ll_resp.bits.uop.iw_issued', 'io.dmem.ll_resp.bits.uop.iw_issued_partial_agen', 'io.dmem.ll_resp.bits.uop.iw_issued_partial_dgen', 'io.dmem.ll_resp.bits.uop.iw_p1_bypass_hint', 'io.dmem.ll_resp.bits.uop.iw_p1_speculative_child', 'io.dmem.ll_resp.bits.uop.iw_p2_bypass_hint', 'io.dmem.ll_resp.bits.uop.iw_p2_speculative_child', 'io.dmem.ll_resp.bits.uop.iw_p3_bypass_hint', 'io.dmem.ll_resp.bits.uop.ldq_idx', 'io.dmem.ll_resp.bits.uop.ldst', 'io.dmem.ll_resp.bits.uop.ldst_is_rs1', 'io.dmem.ll_resp.bits.uop.lrs1', 'io.dmem.ll_resp.bits.uop.lrs1_rtype', 'io.dmem.ll_resp.bits.uop.lrs2', 'io.dmem.ll_resp.bits.uop.lrs2_rtype', 'io.dmem.ll_resp.bits.uop.lrs3', 'io.dmem.ll_resp.bits.uop.mem_cmd', 'io.dmem.ll_resp.bits.uop.mem_signed', 'io.dmem.ll_resp.bits.uop.mem_size', 'io.dmem.ll_resp.bits.uop.op1_sel', 'io.dmem.ll_resp.bits.uop.op2_sel', 'io.dmem.ll_resp.bits.uop.pc_lob', 'io.dmem.ll_resp.bits.uop.pdst', 'io.dmem.ll_resp.bits.uop.pimm', 'io.dmem.ll_resp.bits.uop.ppred', 'io.dmem.ll_resp.bits.uop.ppred_busy', 'io.dmem.ll_resp.bits.uop.prs1', 'io.dmem.ll_resp.bits.uop.prs1_busy', 'io.dmem.ll_resp.bits.uop.prs2', 'io.dmem.ll_resp.bits.uop.prs2_busy', 'io.dmem.ll_resp.bits.uop.prs3', 'io.dmem.ll_resp.bits.uop.prs3_busy', 'io.dmem.ll_resp.bits.uop.rob_idx', 'io.dmem.ll_resp.bits.uop.rxq_idx', 'io.dmem.ll_resp.bits.uop.stale_pdst', 'io.dmem.ll_resp.bits.uop.stq_idx', 'io.dmem.ll_resp.bits.uop.taken', 'io.dmem.ll_resp.bits.uop.uses_ldq', 'io.dmem.ll_resp.bits.uop.uses_stq', 'io.dmem.ll_resp.bits.uop.xcpt_ae_if', 'io.dmem.ll_resp.bits.uop.xcpt_ma_if', 'io.dmem.ll_resp.bits.uop.xcpt_pf_if']
  - immediate registers: ['w1']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
- `LSU::io.hellacache.req.fire`
  - predicate: `io.hellacache.req.valid && io.hellacache.req.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.hellacache.req.bits.addr', 'io.hellacache.req.bits.cmd', 'io.hellacache.req.bits.data', 'io.hellacache.req.bits.dprv', 'io.hellacache.req.bits.dv', 'io.hellacache.req.bits.mask', 'io.hellacache.req.bits.no_alloc', 'io.hellacache.req.bits.no_resp', 'io.hellacache.req.bits.no_xcpt', 'io.hellacache.req.bits.phys', 'io.hellacache.req.bits.signed', 'io.hellacache.req.bits.size', 'io.hellacache.req.bits.tag']
  - immediate registers: ['hella_state']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']
- `LSU::io.hellacache.resp.valid`
  - predicate: `io.hellacache.resp.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.hellacache.resp.bits.addr', 'io.hellacache.resp.bits.cmd', 'io.hellacache.resp.bits.data', 'io.hellacache.resp.bits.data_raw', 'io.hellacache.resp.bits.data_word_bypass', 'io.hellacache.resp.bits.dprv', 'io.hellacache.resp.bits.dv', 'io.hellacache.resp.bits.has_data', 'io.hellacache.resp.bits.mask', 'io.hellacache.resp.bits.replay', 'io.hellacache.resp.bits.signed', 'io.hellacache.resp.bits.size', 'io.hellacache.resp.bits.store_data', 'io.hellacache.resp.bits.tag']
  - immediate registers: ['hella_state', 'w1']
  - historical registers: ['REG_11', 'can_fire_load_retry_REG', 'can_fire_load_wakeup_REG', 'dis_uops', 'fired_load_agen_REG', 'fired_load_agen_exec_REG', 'fired_load_retry_REG', 'fired_load_wakeup_REG', 'fired_release', 'fired_store_agen_REG', 'fired_store_retry_REG', 'hella_paddr', 'hella_req', 'hella_state', 'hella_xcpt', 'lcam_addr_REG', 'lcam_addr_REG_1', 'lcam_ldq_idx_reg', 'lcam_ldq_idx_reg_1', 'lcam_stq_idx_reg', 'ldq_addr', 'ldq_addr_is_uncacheable', 'ldq_addr_is_virtual', 'ldq_enq_retry_idx', 'ldq_executed', 'ldq_forward_std_val', 'ldq_forward_stq_idx', 'ldq_head', 'ldq_ld_byte_mask', 'ldq_next_stq_idx', 'ldq_observed', 'ldq_order_fail', 'ldq_succeeded', 'ldq_tail', 'ldq_uop', 'ldq_valid', 'ldq_wakeup_idx', 'mem_incoming_uop', 'mem_ldq_incoming_e', 'mem_ldq_retry_e', 'mem_ldq_wakeup_e', 'mem_paddr', 'mem_tlb_miss', 'mem_tlb_uncacheable', 'mem_xcpt_valids', 'p1_block_load_mask', 'p2_block_load_mask', 's1_executing_loads', 'store_blocked_counter', 'stq_addr', 'stq_addr_is_virtual', 'stq_almost_full', 'stq_commit_head', 'stq_committed', 'stq_enq_retry_idx', 'stq_head', 'stq_succeeded', 'stq_tail', 'stq_uop', 'stq_valid', 'w1', 'wakeupArbs_0_io_in_1_valid_REG', 'wb_ldst_forward_e_REG', 'wb_ldst_forward_ld_addr', 'wb_ldst_forward_ldq_idx', 'wb_ldst_forward_valid_0_REG', 'wb_ldst_forward_valid_0_REG_1']

## Concrete local state

[]

## Environment/frontier signals

['_T_1122', '_T_1124', '_T_1127', '_T_1128', '_T_1136', '_T_1138', '_T_1141', 'h0', 'h1', 'io.dmem.ll_resp.bits.data', 'io.dmem.ll_resp.bits.is_hella', 'io.dmem.ll_resp.ready', 'io.dmem.ll_resp.valid', 'io.dmem.resp[0].bits.data', 'io.dmem.resp[0].bits.is_hella', 'io.dmem.resp[0].valid', 'io.dmem.store_ack[0].bits.is_hella', 'io.dmem.store_ack[0].valid', 'io.hellacache.resp.bits.data', 'io.hellacache.resp.bits.data_raw', 'io.hellacache.resp.bits.data_word_bypass', 'io.hellacache.resp.bits.dprv', 'io.hellacache.resp.bits.dv', 'io.hellacache.resp.bits.has_data', 'io.hellacache.resp.bits.replay', 'io.hellacache.resp.valid', 'io.ptw.status.prv', 'io.ptw.status.v']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1829-1831
```scala
  io.hellacache.store_pending := stq_valid.reduce(_||_)
  io.hellacache.resp.valid := false.B
  io.hellacache.resp.bits.addr   := hella_req.addr
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1836-1845
```scala
  io.hellacache.resp.bits.mask   := hella_req.mask
  io.hellacache.resp.bits.replay := false.B
  io.hellacache.resp.bits.has_data := true.B
  io.hellacache.resp.bits.data_word_bypass := io.dmem.ll_resp.bits.data
  io.hellacache.resp.bits.data_raw := io.dmem.ll_resp.bits.data
  io.hellacache.resp.bits.store_data := hella_req.data
  io.hellacache.resp.bits.dprv     := io.ptw.status.prv
  io.hellacache.resp.bits.dv       := io.ptw.status.v
  io.hellacache.resp.bits.data     := io.dmem.ll_resp.bits.data
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1878-1881
```scala
    }
  } .elsewhen (hella_state === h_wait) {
    when (io.dmem.ll_resp.fire && io.dmem.ll_resp.bits.is_hella) {
      hella_state := h_ready
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1882-1884
```scala

      io.hellacache.resp.valid       := true.B
      io.hellacache.resp.bits.addr   := hella_req.addr
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1888-1890
```scala
      io.hellacache.resp.bits.size   := hella_req.size
      io.hellacache.resp.bits.data   := io.dmem.ll_resp.bits.data
    }
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1891-1894
```scala
    for (w <- 0 until lsuWidth) {
      when ((io.dmem.resp(w).valid && io.dmem.resp(w).bits.is_hella) ||
            (io.dmem.store_ack(w).valid && io.dmem.store_ack(w).bits.is_hella)) {
        hella_state := h_ready
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1895-1897
```scala

        io.hellacache.resp.valid       := true.B
        io.hellacache.resp.bits.addr   := hella_req.addr
```

### generators/boom/src/main/scala/v4/lsu/lsu.scala:1901-1903
```scala
        io.hellacache.resp.bits.size   := hella_req.size
        io.hellacache.resp.bits.data   := io.dmem.resp(w).bits.data
      }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[7985] FIRRTL:374357 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1830:28 KIND:connect :: connect io.hellacache.resp.valid, UInt<1>(0h0)
[7992] FIRRTL:374364 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1837:34 KIND:connect :: connect io.hellacache.resp.bits.replay, UInt<1>(0h0)
[7993] FIRRTL:374365 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1838:36 KIND:connect :: connect io.hellacache.resp.bits.has_data, UInt<1>(0h1)
[7994] FIRRTL:374366 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1839:44 KIND:connect :: connect io.hellacache.resp.bits.data_word_bypass, io.dmem.ll_resp.bits.data
[7995] FIRRTL:374367 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1840:36 KIND:connect :: connect io.hellacache.resp.bits.data_raw, io.dmem.ll_resp.bits.data
[7997] FIRRTL:374369 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1842:36 KIND:connect :: connect io.hellacache.resp.bits.dprv, io.ptw.status.prv
[7998] FIRRTL:374370 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1843:36 KIND:connect :: connect io.hellacache.resp.bits.dv, io.ptw.status.v
[7999] FIRRTL:374371 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1844:36 KIND:connect :: connect io.hellacache.resp.bits.data, io.dmem.ll_resp.bits.data
[8056] FIRRTL:374428 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1879:40 KIND:when :: when _T_1136 :
[8057] FIRRTL:374429 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_1137 = and(io.dmem.ll_resp.ready, io.dmem.ll_resp.valid)
[8058] FIRRTL:374430 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1880:32 KIND:node :: node _T_1138 = and(_T_1137, io.dmem.ll_resp.bits.is_hella)
[8059] FIRRTL:374431 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1880:66 KIND:when :: when _T_1138 :
[8061] FIRRTL:374433 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1883:38 KIND:connect :: connect io.hellacache.resp.valid, UInt<1>(0h1)
[8067] FIRRTL:374439 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1889:38 KIND:connect :: connect io.hellacache.resp.bits.data, io.dmem.ll_resp.bits.data
[8068] FIRRTL:374440 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1892:36 KIND:node :: node _T_1139 = and(io.dmem.resp[0].valid, io.dmem.resp[0].bits.is_hella)
[8069] FIRRTL:374441 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1893:41 KIND:node :: node _T_1140 = and(io.dmem.store_ack[0].valid, io.dmem.store_ack[0].bits.is_hella)
[8070] FIRRTL:374442 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1892:70 KIND:node :: node _T_1141 = or(_T_1139, _T_1140)
[8071] FIRRTL:374443 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1893:81 KIND:when :: when _T_1141 :
[8073] FIRRTL:374445 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1896:40 KIND:connect :: connect io.hellacache.resp.valid, UInt<1>(0h1)
[8079] FIRRTL:374451 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:1902:40 KIND:connect :: connect io.hellacache.resp.bits.data, io.dmem.resp[0].bits.data
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
  "task_id": "leaf_abstraction-LSU-region-0-5-7aada22dd0e23995",
  "work_unit_id": "LSU::region-0-5",
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
