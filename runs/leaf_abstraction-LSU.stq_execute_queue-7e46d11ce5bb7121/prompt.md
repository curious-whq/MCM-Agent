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

Task ID: `leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.12`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.stq_execute_queue`
- module: `Queue4_STQEntry`
- kind: `module`
- instance path: `LSU.stq_execute_queue`
- leaf: `True`
- coverage complete: `True`
- raw statements: 57
- logical statements: 35
- mapped/logical source lines: 26
- registers: 3
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

- `LSU.stq_execute_queue::io.deq.fire`
  - predicate: `io.deq.valid && io.deq.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.deq.bits.addr.bits', 'io.deq.bits.addr.valid', 'io.deq.bits.addr_is_virtual', 'io.deq.bits.can_execute', 'io.deq.bits.cleared', 'io.deq.bits.committed', 'io.deq.bits.data.bits', 'io.deq.bits.data.valid', 'io.deq.bits.debug_wb_data', 'io.deq.bits.next_ldq_idx', 'io.deq.bits.succeeded', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
- `LSU.stq_execute_queue::io.enq.fire`
  - predicate: `io.enq.valid && io.enq.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.enq.bits.addr.bits', 'io.enq.bits.addr.valid', 'io.enq.bits.addr_is_virtual', 'io.enq.bits.can_execute', 'io.enq.bits.cleared', 'io.enq.bits.committed', 'io.enq.bits.data.bits', 'io.enq.bits.data.valid', 'io.enq.bits.debug_wb_data', 'io.enq.bits.next_ldq_idx', 'io.enq.bits.succeeded', 'io.enq.bits.uop.bp_debug_if', 'io.enq.bits.uop.bp_xcpt_if', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.br_tag', 'io.enq.bits.uop.br_type', 'io.enq.bits.uop.csr_cmd', 'io.enq.bits.uop.debug_fsrc', 'io.enq.bits.uop.debug_inst', 'io.enq.bits.uop.debug_pc', 'io.enq.bits.uop.debug_tsrc', 'io.enq.bits.uop.dis_col_sel', 'io.enq.bits.uop.dst_rtype', 'io.enq.bits.uop.edge_inst', 'io.enq.bits.uop.exc_cause', 'io.enq.bits.uop.exception', 'io.enq.bits.uop.fcn_dw', 'io.enq.bits.uop.fcn_op', 'io.enq.bits.uop.flush_on_commit', 'io.enq.bits.uop.fp_ctrl.div', 'io.enq.bits.uop.fp_ctrl.fastpipe', 'io.enq.bits.uop.fp_ctrl.fma', 'io.enq.bits.uop.fp_ctrl.fromint', 'io.enq.bits.uop.fp_ctrl.ldst', 'io.enq.bits.uop.fp_ctrl.ren1', 'io.enq.bits.uop.fp_ctrl.ren2', 'io.enq.bits.uop.fp_ctrl.ren3', 'io.enq.bits.uop.fp_ctrl.sqrt', 'io.enq.bits.uop.fp_ctrl.swap12', 'io.enq.bits.uop.fp_ctrl.swap23', 'io.enq.bits.uop.fp_ctrl.toint', 'io.enq.bits.uop.fp_ctrl.typeTagIn', 'io.enq.bits.uop.fp_ctrl.typeTagOut', 'io.enq.bits.uop.fp_ctrl.vec', 'io.enq.bits.uop.fp_ctrl.wen', 'io.enq.bits.uop.fp_ctrl.wflags', 'io.enq.bits.uop.fp_rm', 'io.enq.bits.uop.fp_typ', 'io.enq.bits.uop.fp_val', 'io.enq.bits.uop.frs3_en', 'io.enq.bits.uop.ftq_idx', 'io.enq.bits.uop.fu_code[0]', 'io.enq.bits.uop.fu_code[1]', 'io.enq.bits.uop.fu_code[2]', 'io.enq.bits.uop.fu_code[3]', 'io.enq.bits.uop.fu_code[4]', 'io.enq.bits.uop.fu_code[5]', 'io.enq.bits.uop.fu_code[6]', 'io.enq.bits.uop.fu_code[7]', 'io.enq.bits.uop.fu_code[8]', 'io.enq.bits.uop.fu_code[9]', 'io.enq.bits.uop.imm_packed', 'io.enq.bits.uop.imm_rename', 'io.enq.bits.uop.imm_sel', 'io.enq.bits.uop.inst', 'io.enq.bits.uop.iq_type[0]', 'io.enq.bits.uop.iq_type[1]', 'io.enq.bits.uop.iq_type[2]', 'io.enq.bits.uop.iq_type[3]', 'io.enq.bits.uop.is_amo', 'io.enq.bits.uop.is_eret', 'io.enq.bits.uop.is_fence', 'io.enq.bits.uop.is_fencei', 'io.enq.bits.uop.is_mov', 'io.enq.bits.uop.is_rocc', 'io.enq.bits.uop.is_rvc', 'io.enq.bits.uop.is_sfb', 'io.enq.bits.uop.is_sfence', 'io.enq.bits.uop.is_sys_pc2epc', 'io.enq.bits.uop.is_unique', 'io.enq.bits.uop.iw_issued', 'io.enq.bits.uop.iw_issued_partial_agen', 'io.enq.bits.uop.iw_issued_partial_dgen', 'io.enq.bits.uop.iw_p1_bypass_hint', 'io.enq.bits.uop.iw_p1_speculative_child', 'io.enq.bits.uop.iw_p2_bypass_hint', 'io.enq.bits.uop.iw_p2_speculative_child', 'io.enq.bits.uop.iw_p3_bypass_hint', 'io.enq.bits.uop.ldq_idx', 'io.enq.bits.uop.ldst', 'io.enq.bits.uop.ldst_is_rs1', 'io.enq.bits.uop.lrs1', 'io.enq.bits.uop.lrs1_rtype', 'io.enq.bits.uop.lrs2', 'io.enq.bits.uop.lrs2_rtype', 'io.enq.bits.uop.lrs3', 'io.enq.bits.uop.mem_cmd', 'io.enq.bits.uop.mem_signed', 'io.enq.bits.uop.mem_size', 'io.enq.bits.uop.op1_sel', 'io.enq.bits.uop.op2_sel', 'io.enq.bits.uop.pc_lob', 'io.enq.bits.uop.pdst', 'io.enq.bits.uop.pimm', 'io.enq.bits.uop.ppred', 'io.enq.bits.uop.ppred_busy', 'io.enq.bits.uop.prs1', 'io.enq.bits.uop.prs1_busy', 'io.enq.bits.uop.prs2', 'io.enq.bits.uop.prs2_busy', 'io.enq.bits.uop.prs3', 'io.enq.bits.uop.prs3_busy', 'io.enq.bits.uop.rob_idx', 'io.enq.bits.uop.rxq_idx', 'io.enq.bits.uop.stale_pdst', 'io.enq.bits.uop.stq_idx', 'io.enq.bits.uop.taken', 'io.enq.bits.uop.uses_ldq', 'io.enq.bits.uop.uses_stq', 'io.enq.bits.uop.xcpt_ae_if', 'io.enq.bits.uop.xcpt_ma_if', 'io.enq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']

## Concrete local state

['deq_ptr_value', 'enq_ptr_value', 'maybe_full']

## Environment/frontier signals

['clock', 'io.count', 'io.deq.bits.addr.bits', 'io.deq.bits.addr.valid', 'io.deq.bits.addr_is_virtual', 'io.deq.bits.can_execute', 'io.deq.bits.cleared', 'io.deq.bits.committed', 'io.deq.bits.data.bits', 'io.deq.bits.data.valid', 'io.deq.bits.debug_wb_data', 'io.deq.bits.next_ldq_idx', 'io.deq.bits.succeeded', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.ready', 'io.deq.valid', 'io.enq.bits.addr_is_virtual', 'io.enq.bits.can_execute', 'io.enq.bits.cleared', 'io.enq.bits.committed', 'io.enq.bits.debug_wb_data', 'io.enq.bits.next_ldq_idx', 'io.enq.bits.succeeded', 'io.enq.ready', 'io.enq.valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:366038 SRC:src/main/scala/chisel3/util/Decoupled.scala:243:7 KIND:structural :: input clock : Clock
[1] FIRRTL:366039 SRC:src/main/scala/chisel3/util/Decoupled.scala:243:7 KIND:structural :: input reset : Reset
[2] FIRRTL:366040 SRC:src/main/scala/chisel3/util/Decoupled.scala:255:14 KIND:structural :: output io : { flip enq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : { valid : UInt<1>, bits : UInt<40>}, addr_is_virtual : UInt<1>, data : { valid : UInt<1>, bits : UInt<64>}, committed : UInt<1>, succeeded : UInt<1>, can_execute : UInt<1>, cleared : UInt<1>, next_ldq_idx : UInt<4>, debug_wb_data : UInt<64>}}, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : { valid : UInt<1>, bits : UInt<40>}, addr_is_virtual : UInt<1>, data : { valid : UInt<1>, bits : UInt<64>}, committed : UInt<1>, succeeded : UInt<1>, can_execute : UInt<1>, cleared : UInt<1>, next_ldq_idx : UInt<4>, debug_wb_data : UInt<64>}}, count : UInt<3>}
[3] FIRRTL:366042 SRC:src/main/scala/chisel3/util/Decoupled.scala:256:91 KIND:memory :: cmem ram : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, addr : { valid : UInt<1>, bits : UInt<40>}, addr_is_virtual : UInt<1>, data : { valid : UInt<1>, bits : UInt<64>}, committed : UInt<1>, succeeded : UInt<1>, can_execute : UInt<1>, cleared : UInt<1>, next_ldq_idx : UInt<4>, debug_wb_data : UInt<64>} [4]
[4] FIRRTL:366043 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset enq_ptr_value : UInt<2>, clock, reset, UInt<2>(0h0)
[5] FIRRTL:366044 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset deq_ptr_value : UInt<2>, clock, reset, UInt<2>(0h0)
[6] FIRRTL:366045 SRC:src/main/scala/chisel3/util/Decoupled.scala:259:27 KIND:regreset :: regreset maybe_full : UInt<1>, clock, reset, UInt<1>(0h0)
[7] FIRRTL:366046 SRC:src/main/scala/chisel3/util/Decoupled.scala:260:33 KIND:node :: node ptr_match = eq(enq_ptr_value, deq_ptr_value)
[8] FIRRTL:366047 SRC:src/main/scala/chisel3/util/Decoupled.scala:261:28 KIND:node :: node _empty_T = eq(maybe_full, UInt<1>(0h0))
[9] FIRRTL:366048 SRC:src/main/scala/chisel3/util/Decoupled.scala:261:25 KIND:node :: node empty = and(ptr_match, _empty_T)
[10] FIRRTL:366049 SRC:src/main/scala/chisel3/util/Decoupled.scala:262:24 KIND:node :: node full = and(ptr_match, maybe_full)
[11] FIRRTL:366050 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _do_enq_T = and(io.enq.ready, io.enq.valid)
[12] FIRRTL:366051 SRC:src/main/scala/chisel3/util/Decoupled.scala:263:27 KIND:wire :: wire do_enq : UInt<1>
[13] FIRRTL:366052 SRC:src/main/scala/chisel3/util/Decoupled.scala:263:27 KIND:connect :: connect do_enq, _do_enq_T
[14] FIRRTL:366053 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _do_deq_T = and(io.deq.ready, io.deq.valid)
[15] FIRRTL:366054 SRC:src/main/scala/chisel3/util/Decoupled.scala:264:27 KIND:wire :: wire do_deq : UInt<1>
[16] FIRRTL:366055 SRC:src/main/scala/chisel3/util/Decoupled.scala:264:27 KIND:connect :: connect do_deq, _do_deq_T
[17] FIRRTL:366056 SRC:src/main/scala/chisel3/util/Decoupled.scala:269:16 KIND:when :: when do_enq :
[18] FIRRTL:366057 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:8 KIND:infer_mport :: infer mport MPORT = ram[enq_ptr_value], clock
[19] FIRRTL:366058 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.debug_wb_data, io.enq.bits.debug_wb_data
[20] FIRRTL:366059 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.next_ldq_idx, io.enq.bits.next_ldq_idx
[21] FIRRTL:366060 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.cleared, io.enq.bits.cleared
[22] FIRRTL:366061 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.can_execute, io.enq.bits.can_execute
[23] FIRRTL:366062 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.succeeded, io.enq.bits.succeeded
[24] FIRRTL:366063 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.committed, io.enq.bits.committed
[25] FIRRTL:366064 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.data, io.enq.bits.data
[26] FIRRTL:366065 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.addr_is_virtual, io.enq.bits.addr_is_virtual
[27] FIRRTL:366066 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.addr, io.enq.bits.addr
[28] FIRRTL:366067 SRC:src/main/scala/chisel3/util/Decoupled.scala:270:24 KIND:connect :: connect MPORT.uop, io.enq.bits.uop
[29] FIRRTL:366068 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap = eq(enq_ptr_value, UInt<2>(0h3))
[30] FIRRTL:366069 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T = add(enq_ptr_value, UInt<1>(0h1))
[31] FIRRTL:366070 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_1 = tail(_value_T, 1)
[32] FIRRTL:366071 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect enq_ptr_value, _value_T_1
[33] FIRRTL:366072 SRC:src/main/scala/chisel3/util/Decoupled.scala:273:16 KIND:when :: when do_deq :
[34] FIRRTL:366073 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap_1 = eq(deq_ptr_value, UInt<2>(0h3))
[35] FIRRTL:366074 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_2 = add(deq_ptr_value, UInt<1>(0h1))
[36] FIRRTL:366075 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_3 = tail(_value_T_2, 1)
[37] FIRRTL:366076 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect deq_ptr_value, _value_T_3
[38] FIRRTL:366077 SRC:src/main/scala/chisel3/util/Decoupled.scala:276:15 KIND:node :: node _T = neq(do_enq, do_deq)
[39] FIRRTL:366078 SRC:src/main/scala/chisel3/util/Decoupled.scala:276:27 KIND:when :: when _T :
[40] FIRRTL:366079 SRC:src/main/scala/chisel3/util/Decoupled.scala:277:16 KIND:connect :: connect maybe_full, do_enq
[41] FIRRTL:366080 SRC:src/main/scala/chisel3/util/Decoupled.scala:279:15 KIND:when :: when UInt<1>(0h0) :
[42] FIRRTL:366081 SRC:src/main/scala/chisel3/util/Counter.scala:98:11 KIND:connect :: connect enq_ptr_value, UInt<1>(0h0)
[43] FIRRTL:366082 SRC:src/main/scala/chisel3/util/Counter.scala:98:11 KIND:connect :: connect deq_ptr_value, UInt<1>(0h0)
[44] FIRRTL:366083 SRC:src/main/scala/chisel3/util/Decoupled.scala:282:16 KIND:connect :: connect maybe_full, UInt<1>(0h0)
[45] FIRRTL:366084 SRC:src/main/scala/chisel3/util/Decoupled.scala:285:19 KIND:node :: node _io_deq_valid_T = eq(empty, UInt<1>(0h0))
[46] FIRRTL:366085 SRC:src/main/scala/chisel3/util/Decoupled.scala:285:16 KIND:connect :: connect io.deq.valid, _io_deq_valid_T
[47] FIRRTL:366086 SRC:src/main/scala/chisel3/util/Decoupled.scala:286:19 KIND:node :: node _io_enq_ready_T = eq(full, UInt<1>(0h0))
[48] FIRRTL:366087 SRC:src/main/scala/chisel3/util/Decoupled.scala:286:16 KIND:connect :: connect io.enq.ready, _io_enq_ready_T
[49] FIRRTL:366088 SRC:src/main/scala/chisel3/util/Decoupled.scala:293:23 KIND:infer_mport :: infer mport io_deq_bits_MPORT = ram[deq_ptr_value], clock
[50] FIRRTL:366089 SRC:src/main/scala/chisel3/util/Decoupled.scala:293:17 KIND:connect :: connect io.deq.bits, io_deq_bits_MPORT
[51] FIRRTL:366090 SRC:src/main/scala/chisel3/util/Decoupled.scala:309:32 KIND:node :: node _ptr_diff_T = sub(enq_ptr_value, deq_ptr_value)
[52] FIRRTL:366091 SRC:src/main/scala/chisel3/util/Decoupled.scala:309:32 KIND:node :: node ptr_diff = tail(_ptr_diff_T, 1)
[53] FIRRTL:366092 SRC:src/main/scala/chisel3/util/Decoupled.scala:312:32 KIND:node :: node _io_count_T = and(maybe_full, ptr_match)
[54] FIRRTL:366093 SRC:src/main/scala/chisel3/util/Decoupled.scala:312:20 KIND:node :: node _io_count_T_1 = mux(_io_count_T, UInt<3>(0h4), UInt<1>(0h0))
[55] FIRRTL:366094 SRC:src/main/scala/chisel3/util/Decoupled.scala:312:62 KIND:node :: node _io_count_T_2 = or(_io_count_T_1, ptr_diff)
[56] FIRRTL:366095 SRC:src/main/scala/chisel3/util/Decoupled.scala:312:14 KIND:connect :: connect io.count, _io_count_T_2
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
  "task_id": "leaf_abstraction-LSU.stq_execute_queue-7e46d11ce5bb7121",
  "work_unit_id": "LSU.stq_execute_queue",
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
