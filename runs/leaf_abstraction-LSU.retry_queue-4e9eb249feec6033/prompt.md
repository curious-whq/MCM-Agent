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

Task ID: `leaf_abstraction-LSU.retry_queue-4e9eb249feec6033`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.12`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.retry_queue`
- module: `BranchKillableQueue_7`
- kind: `module`
- instance path: `LSU.retry_queue`
- leaf: `True`
- coverage complete: `True`
- raw statements: 180
- logical statements: 54
- mapped/logical source lines: 39
- registers: 5
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

- `LSU.retry_queue::io.deq.fire`
  - predicate: `io.deq.valid && io.deq.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.deq.bits.data', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'valids']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']
- `LSU.retry_queue::io.enq.fire`
  - predicate: `io.enq.valid && io.enq.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.enq.bits.data', 'io.enq.bits.uop.bp_debug_if', 'io.enq.bits.uop.bp_xcpt_if', 'io.enq.bits.uop.br_mask', 'io.enq.bits.uop.br_tag', 'io.enq.bits.uop.br_type', 'io.enq.bits.uop.csr_cmd', 'io.enq.bits.uop.debug_fsrc', 'io.enq.bits.uop.debug_inst', 'io.enq.bits.uop.debug_pc', 'io.enq.bits.uop.debug_tsrc', 'io.enq.bits.uop.dis_col_sel', 'io.enq.bits.uop.dst_rtype', 'io.enq.bits.uop.edge_inst', 'io.enq.bits.uop.exc_cause', 'io.enq.bits.uop.exception', 'io.enq.bits.uop.fcn_dw', 'io.enq.bits.uop.fcn_op', 'io.enq.bits.uop.flush_on_commit', 'io.enq.bits.uop.fp_ctrl.div', 'io.enq.bits.uop.fp_ctrl.fastpipe', 'io.enq.bits.uop.fp_ctrl.fma', 'io.enq.bits.uop.fp_ctrl.fromint', 'io.enq.bits.uop.fp_ctrl.ldst', 'io.enq.bits.uop.fp_ctrl.ren1', 'io.enq.bits.uop.fp_ctrl.ren2', 'io.enq.bits.uop.fp_ctrl.ren3', 'io.enq.bits.uop.fp_ctrl.sqrt', 'io.enq.bits.uop.fp_ctrl.swap12', 'io.enq.bits.uop.fp_ctrl.swap23', 'io.enq.bits.uop.fp_ctrl.toint', 'io.enq.bits.uop.fp_ctrl.typeTagIn', 'io.enq.bits.uop.fp_ctrl.typeTagOut', 'io.enq.bits.uop.fp_ctrl.vec', 'io.enq.bits.uop.fp_ctrl.wen', 'io.enq.bits.uop.fp_ctrl.wflags', 'io.enq.bits.uop.fp_rm', 'io.enq.bits.uop.fp_typ', 'io.enq.bits.uop.fp_val', 'io.enq.bits.uop.frs3_en', 'io.enq.bits.uop.ftq_idx', 'io.enq.bits.uop.fu_code[0]', 'io.enq.bits.uop.fu_code[1]', 'io.enq.bits.uop.fu_code[2]', 'io.enq.bits.uop.fu_code[3]', 'io.enq.bits.uop.fu_code[4]', 'io.enq.bits.uop.fu_code[5]', 'io.enq.bits.uop.fu_code[6]', 'io.enq.bits.uop.fu_code[7]', 'io.enq.bits.uop.fu_code[8]', 'io.enq.bits.uop.fu_code[9]', 'io.enq.bits.uop.imm_packed', 'io.enq.bits.uop.imm_rename', 'io.enq.bits.uop.imm_sel', 'io.enq.bits.uop.inst', 'io.enq.bits.uop.iq_type[0]', 'io.enq.bits.uop.iq_type[1]', 'io.enq.bits.uop.iq_type[2]', 'io.enq.bits.uop.iq_type[3]', 'io.enq.bits.uop.is_amo', 'io.enq.bits.uop.is_eret', 'io.enq.bits.uop.is_fence', 'io.enq.bits.uop.is_fencei', 'io.enq.bits.uop.is_mov', 'io.enq.bits.uop.is_rocc', 'io.enq.bits.uop.is_rvc', 'io.enq.bits.uop.is_sfb', 'io.enq.bits.uop.is_sfence', 'io.enq.bits.uop.is_sys_pc2epc', 'io.enq.bits.uop.is_unique', 'io.enq.bits.uop.iw_issued', 'io.enq.bits.uop.iw_issued_partial_agen', 'io.enq.bits.uop.iw_issued_partial_dgen', 'io.enq.bits.uop.iw_p1_bypass_hint', 'io.enq.bits.uop.iw_p1_speculative_child', 'io.enq.bits.uop.iw_p2_bypass_hint', 'io.enq.bits.uop.iw_p2_speculative_child', 'io.enq.bits.uop.iw_p3_bypass_hint', 'io.enq.bits.uop.ldq_idx', 'io.enq.bits.uop.ldst', 'io.enq.bits.uop.ldst_is_rs1', 'io.enq.bits.uop.lrs1', 'io.enq.bits.uop.lrs1_rtype', 'io.enq.bits.uop.lrs2', 'io.enq.bits.uop.lrs2_rtype', 'io.enq.bits.uop.lrs3', 'io.enq.bits.uop.mem_cmd', 'io.enq.bits.uop.mem_signed', 'io.enq.bits.uop.mem_size', 'io.enq.bits.uop.op1_sel', 'io.enq.bits.uop.op2_sel', 'io.enq.bits.uop.pc_lob', 'io.enq.bits.uop.pdst', 'io.enq.bits.uop.pimm', 'io.enq.bits.uop.ppred', 'io.enq.bits.uop.ppred_busy', 'io.enq.bits.uop.prs1', 'io.enq.bits.uop.prs1_busy', 'io.enq.bits.uop.prs2', 'io.enq.bits.uop.prs2_busy', 'io.enq.bits.uop.prs3', 'io.enq.bits.uop.prs3_busy', 'io.enq.bits.uop.rob_idx', 'io.enq.bits.uop.rxq_idx', 'io.enq.bits.uop.stale_pdst', 'io.enq.bits.uop.stq_idx', 'io.enq.bits.uop.taken', 'io.enq.bits.uop.uses_ldq', 'io.enq.bits.uop.uses_stq', 'io.enq.bits.uop.xcpt_ae_if', 'io.enq.bits.uop.xcpt_ma_if', 'io.enq.bits.uop.xcpt_pf_if']
  - immediate registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full']
  - historical registers: ['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Concrete local state

['deq_ptr_value', 'enq_ptr_value', 'maybe_full', 'uops', 'valids']

## Environment/frontier signals

['clock', 'io.brupdate.b1.mispredict_mask', 'io.brupdate.b1.resolve_mask', 'io.count', 'io.deq.bits.data', 'io.deq.bits.uop.bp_debug_if', 'io.deq.bits.uop.bp_xcpt_if', 'io.deq.bits.uop.br_mask', 'io.deq.bits.uop.br_tag', 'io.deq.bits.uop.br_type', 'io.deq.bits.uop.csr_cmd', 'io.deq.bits.uop.debug_fsrc', 'io.deq.bits.uop.debug_inst', 'io.deq.bits.uop.debug_pc', 'io.deq.bits.uop.debug_tsrc', 'io.deq.bits.uop.dis_col_sel', 'io.deq.bits.uop.dst_rtype', 'io.deq.bits.uop.edge_inst', 'io.deq.bits.uop.exc_cause', 'io.deq.bits.uop.exception', 'io.deq.bits.uop.fcn_dw', 'io.deq.bits.uop.fcn_op', 'io.deq.bits.uop.flush_on_commit', 'io.deq.bits.uop.fp_ctrl.div', 'io.deq.bits.uop.fp_ctrl.fastpipe', 'io.deq.bits.uop.fp_ctrl.fma', 'io.deq.bits.uop.fp_ctrl.fromint', 'io.deq.bits.uop.fp_ctrl.ldst', 'io.deq.bits.uop.fp_ctrl.ren1', 'io.deq.bits.uop.fp_ctrl.ren2', 'io.deq.bits.uop.fp_ctrl.ren3', 'io.deq.bits.uop.fp_ctrl.sqrt', 'io.deq.bits.uop.fp_ctrl.swap12', 'io.deq.bits.uop.fp_ctrl.swap23', 'io.deq.bits.uop.fp_ctrl.toint', 'io.deq.bits.uop.fp_ctrl.typeTagIn', 'io.deq.bits.uop.fp_ctrl.typeTagOut', 'io.deq.bits.uop.fp_ctrl.vec', 'io.deq.bits.uop.fp_ctrl.wen', 'io.deq.bits.uop.fp_ctrl.wflags', 'io.deq.bits.uop.fp_rm', 'io.deq.bits.uop.fp_typ', 'io.deq.bits.uop.fp_val', 'io.deq.bits.uop.frs3_en', 'io.deq.bits.uop.ftq_idx', 'io.deq.bits.uop.fu_code[0]', 'io.deq.bits.uop.fu_code[1]', 'io.deq.bits.uop.fu_code[2]', 'io.deq.bits.uop.fu_code[3]', 'io.deq.bits.uop.fu_code[4]', 'io.deq.bits.uop.fu_code[5]', 'io.deq.bits.uop.fu_code[6]', 'io.deq.bits.uop.fu_code[7]', 'io.deq.bits.uop.fu_code[8]', 'io.deq.bits.uop.fu_code[9]', 'io.deq.bits.uop.imm_packed', 'io.deq.bits.uop.imm_rename', 'io.deq.bits.uop.imm_sel', 'io.deq.bits.uop.inst', 'io.deq.bits.uop.iq_type[0]', 'io.deq.bits.uop.iq_type[1]', 'io.deq.bits.uop.iq_type[2]', 'io.deq.bits.uop.iq_type[3]', 'io.deq.bits.uop.is_amo', 'io.deq.bits.uop.is_eret', 'io.deq.bits.uop.is_fence', 'io.deq.bits.uop.is_fencei', 'io.deq.bits.uop.is_mov', 'io.deq.bits.uop.is_rocc', 'io.deq.bits.uop.is_rvc', 'io.deq.bits.uop.is_sfb', 'io.deq.bits.uop.is_sfence', 'io.deq.bits.uop.is_sys_pc2epc', 'io.deq.bits.uop.is_unique', 'io.deq.bits.uop.iw_issued', 'io.deq.bits.uop.iw_issued_partial_agen', 'io.deq.bits.uop.iw_issued_partial_dgen', 'io.deq.bits.uop.iw_p1_bypass_hint', 'io.deq.bits.uop.iw_p1_speculative_child', 'io.deq.bits.uop.iw_p2_bypass_hint', 'io.deq.bits.uop.iw_p2_speculative_child', 'io.deq.bits.uop.iw_p3_bypass_hint', 'io.deq.bits.uop.ldq_idx', 'io.deq.bits.uop.ldst', 'io.deq.bits.uop.ldst_is_rs1', 'io.deq.bits.uop.lrs1', 'io.deq.bits.uop.lrs1_rtype', 'io.deq.bits.uop.lrs2', 'io.deq.bits.uop.lrs2_rtype', 'io.deq.bits.uop.lrs3', 'io.deq.bits.uop.mem_cmd', 'io.deq.bits.uop.mem_signed', 'io.deq.bits.uop.mem_size', 'io.deq.bits.uop.op1_sel', 'io.deq.bits.uop.op2_sel', 'io.deq.bits.uop.pc_lob', 'io.deq.bits.uop.pdst', 'io.deq.bits.uop.pimm', 'io.deq.bits.uop.ppred', 'io.deq.bits.uop.ppred_busy', 'io.deq.bits.uop.prs1', 'io.deq.bits.uop.prs1_busy', 'io.deq.bits.uop.prs2', 'io.deq.bits.uop.prs2_busy', 'io.deq.bits.uop.prs3', 'io.deq.bits.uop.prs3_busy', 'io.deq.bits.uop.rob_idx', 'io.deq.bits.uop.rxq_idx', 'io.deq.bits.uop.stale_pdst', 'io.deq.bits.uop.stq_idx', 'io.deq.bits.uop.taken', 'io.deq.bits.uop.uses_ldq', 'io.deq.bits.uop.uses_stq', 'io.deq.bits.uop.xcpt_ae_if', 'io.deq.bits.uop.xcpt_ma_if', 'io.deq.bits.uop.xcpt_pf_if', 'io.deq.ready', 'io.deq.valid', 'io.empty', 'io.enq.bits.uop.br_mask', 'io.enq.ready', 'io.enq.valid', 'io.flush']

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
[0] FIRRTL:365855 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input clock : Clock
[1] FIRRTL:365856 SRC:generators/boom/src/main/scala/v4/util/util.scala:477:7 KIND:structural :: input reset : Reset
[2] FIRRTL:365857 SRC:generators/boom/src/main/scala/v4/util/util.scala:482:14 KIND:structural :: output io : { flip enq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>}}, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>}}, flip brupdate : { b1 : { resolve_mask : UInt<8>, mispredict_mask : UInt<8>}, b2 : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, mispredict : UInt<1>, taken : UInt<1>, cfi_type : UInt<3>, pc_sel : UInt<2>, jalr_target : UInt<40>, target_offset : SInt<21>}}, flip flush : UInt<1>, empty : UInt<1>, count : UInt<3>}
[3] FIRRTL:365859 SRC:generators/boom/src/main/scala/v4/util/util.scala:522:22 KIND:memory :: cmem ram : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>} [8]
[4] FIRRTL:365860 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:wire :: wire _valids_WIRE : UInt<1>[8]
[5] FIRRTL:365861 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[0], UInt<1>(0h0)
[6] FIRRTL:365862 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[1], UInt<1>(0h0)
[7] FIRRTL:365863 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[2], UInt<1>(0h0)
[8] FIRRTL:365864 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[3], UInt<1>(0h0)
[9] FIRRTL:365865 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[4], UInt<1>(0h0)
[10] FIRRTL:365866 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[5], UInt<1>(0h0)
[11] FIRRTL:365867 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[6], UInt<1>(0h0)
[12] FIRRTL:365868 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:34 KIND:connect :: connect _valids_WIRE[7], UInt<1>(0h0)
[13] FIRRTL:365869 SRC:generators/boom/src/main/scala/v4/util/util.scala:523:26 KIND:regreset :: regreset valids : UInt<1>[8], clock, reset, _valids_WIRE
[14] FIRRTL:365870 SRC:generators/boom/src/main/scala/v4/util/util.scala:524:22 KIND:reg :: reg uops : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}[8], clock
[15] FIRRTL:365871 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset enq_ptr_value : UInt<3>, clock, reset, UInt<3>(0h0)
[16] FIRRTL:365872 SRC:src/main/scala/chisel3/util/Counter.scala:61:40 KIND:regreset :: regreset deq_ptr_value : UInt<3>, clock, reset, UInt<3>(0h0)
[17] FIRRTL:365873 SRC:generators/boom/src/main/scala/v4/util/util.scala:528:29 KIND:regreset :: regreset maybe_full : UInt<1>, clock, reset, UInt<1>(0h0)
[18] FIRRTL:365874 SRC:generators/boom/src/main/scala/v4/util/util.scala:530:35 KIND:node :: node ptr_match = eq(enq_ptr_value, deq_ptr_value)
[19] FIRRTL:365875 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:30 KIND:node :: node _io_empty_T = eq(maybe_full, UInt<1>(0h0))
[20] FIRRTL:365876 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:27 KIND:node :: node _io_empty_T_1 = and(ptr_match, _io_empty_T)
[21] FIRRTL:365877 SRC:generators/boom/src/main/scala/v4/util/util.scala:531:14 KIND:connect :: connect io.empty, _io_empty_T_1
[22] FIRRTL:365878 SRC:generators/boom/src/main/scala/v4/util/util.scala:532:26 KIND:node :: node full = and(ptr_match, maybe_full)
[23] FIRRTL:365879 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _do_enq_T = and(io.enq.ready, io.enq.valid)
[24] FIRRTL:365880 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _do_enq_T_1 = and(io.brupdate.b1.mispredict_mask, io.enq.bits.uop.br_mask)
[25] FIRRTL:365881 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _do_enq_T_2 = neq(_do_enq_T_1, UInt<1>(0h0))
[26] FIRRTL:365882 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _do_enq_T_3 = or(_do_enq_T_2, UInt<1>(0h0))
[27] FIRRTL:365883 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:42 KIND:node :: node _do_enq_T_4 = eq(_do_enq_T_3, UInt<1>(0h0))
[28] FIRRTL:365884 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:39 KIND:node :: node _do_enq_T_5 = and(_do_enq_T, _do_enq_T_4)
[29] FIRRTL:365885 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:113 KIND:node :: node _do_enq_T_6 = and(io.flush, UInt<1>(0h1))
[30] FIRRTL:365886 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:102 KIND:node :: node _do_enq_T_7 = eq(_do_enq_T_6, UInt<1>(0h0))
[31] FIRRTL:365887 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:99 KIND:node :: node _do_enq_T_8 = and(_do_enq_T_5, _do_enq_T_7)
[32] FIRRTL:365888 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:wire :: wire do_enq : UInt<1>
[33] FIRRTL:365889 SRC:generators/boom/src/main/scala/v4/util/util.scala:533:26 KIND:connect :: connect do_enq, _do_enq_T_8
[34] FIRRTL:365890 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:44 KIND:node :: node _do_deq_T = eq(valids[deq_ptr_value], UInt<1>(0h0))
[35] FIRRTL:365891 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:41 KIND:node :: node _do_deq_T_1 = or(io.deq.ready, _do_deq_T)
[36] FIRRTL:365892 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:71 KIND:node :: node _do_deq_T_2 = eq(io.empty, UInt<1>(0h0))
[37] FIRRTL:365893 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:68 KIND:node :: node _do_deq_T_3 = and(_do_deq_T_1, _do_deq_T_2)
[38] FIRRTL:365894 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:wire :: wire do_deq : UInt<1>
[39] FIRRTL:365895 SRC:generators/boom/src/main/scala/v4/util/util.scala:534:26 KIND:connect :: connect do_deq, _do_deq_T_3
[40] FIRRTL:365896 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_0_T = and(io.brupdate.b1.mispredict_mask, uops[0].br_mask)
[41] FIRRTL:365897 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_0_T_1 = neq(_valids_0_T, UInt<1>(0h0))
[42] FIRRTL:365898 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_0_T_2 = or(_valids_0_T_1, UInt<1>(0h0))
[43] FIRRTL:365899 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_0_T_3 = eq(_valids_0_T_2, UInt<1>(0h0))
[44] FIRRTL:365900 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_0_T_4 = and(valids[0], _valids_0_T_3)
[45] FIRRTL:365901 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_0_T_5 = and(io.flush, UInt<1>(0h1))
[46] FIRRTL:365902 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_0_T_6 = eq(_valids_0_T_5, UInt<1>(0h0))
[47] FIRRTL:365903 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_0_T_7 = and(_valids_0_T_4, _valids_0_T_6)
[48] FIRRTL:365904 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[0], _valids_0_T_7
[49] FIRRTL:365905 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[0] :
[50] FIRRTL:365906 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_0_br_mask_T = not(io.brupdate.b1.resolve_mask)
[51] FIRRTL:365907 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_0_br_mask_T_1 = and(uops[0].br_mask, _uops_0_br_mask_T)
[52] FIRRTL:365908 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[0].br_mask, _uops_0_br_mask_T_1
[53] FIRRTL:365909 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_1_T = and(io.brupdate.b1.mispredict_mask, uops[1].br_mask)
[54] FIRRTL:365910 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_1_T_1 = neq(_valids_1_T, UInt<1>(0h0))
[55] FIRRTL:365911 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_1_T_2 = or(_valids_1_T_1, UInt<1>(0h0))
[56] FIRRTL:365912 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_1_T_3 = eq(_valids_1_T_2, UInt<1>(0h0))
[57] FIRRTL:365913 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_1_T_4 = and(valids[1], _valids_1_T_3)
[58] FIRRTL:365914 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_1_T_5 = and(io.flush, UInt<1>(0h1))
[59] FIRRTL:365915 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_1_T_6 = eq(_valids_1_T_5, UInt<1>(0h0))
[60] FIRRTL:365916 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_1_T_7 = and(_valids_1_T_4, _valids_1_T_6)
[61] FIRRTL:365917 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[1], _valids_1_T_7
[62] FIRRTL:365918 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[1] :
[63] FIRRTL:365919 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_1_br_mask_T = not(io.brupdate.b1.resolve_mask)
[64] FIRRTL:365920 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_1_br_mask_T_1 = and(uops[1].br_mask, _uops_1_br_mask_T)
[65] FIRRTL:365921 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[1].br_mask, _uops_1_br_mask_T_1
[66] FIRRTL:365922 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_2_T = and(io.brupdate.b1.mispredict_mask, uops[2].br_mask)
[67] FIRRTL:365923 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_2_T_1 = neq(_valids_2_T, UInt<1>(0h0))
[68] FIRRTL:365924 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_2_T_2 = or(_valids_2_T_1, UInt<1>(0h0))
[69] FIRRTL:365925 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_2_T_3 = eq(_valids_2_T_2, UInt<1>(0h0))
[70] FIRRTL:365926 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_2_T_4 = and(valids[2], _valids_2_T_3)
[71] FIRRTL:365927 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_2_T_5 = and(io.flush, UInt<1>(0h1))
[72] FIRRTL:365928 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_2_T_6 = eq(_valids_2_T_5, UInt<1>(0h0))
[73] FIRRTL:365929 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_2_T_7 = and(_valids_2_T_4, _valids_2_T_6)
[74] FIRRTL:365930 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[2], _valids_2_T_7
[75] FIRRTL:365931 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[2] :
[76] FIRRTL:365932 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_2_br_mask_T = not(io.brupdate.b1.resolve_mask)
[77] FIRRTL:365933 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_2_br_mask_T_1 = and(uops[2].br_mask, _uops_2_br_mask_T)
[78] FIRRTL:365934 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[2].br_mask, _uops_2_br_mask_T_1
[79] FIRRTL:365935 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_3_T = and(io.brupdate.b1.mispredict_mask, uops[3].br_mask)
[80] FIRRTL:365936 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_3_T_1 = neq(_valids_3_T, UInt<1>(0h0))
[81] FIRRTL:365937 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_3_T_2 = or(_valids_3_T_1, UInt<1>(0h0))
[82] FIRRTL:365938 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_3_T_3 = eq(_valids_3_T_2, UInt<1>(0h0))
[83] FIRRTL:365939 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_3_T_4 = and(valids[3], _valids_3_T_3)
[84] FIRRTL:365940 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_3_T_5 = and(io.flush, UInt<1>(0h1))
[85] FIRRTL:365941 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_3_T_6 = eq(_valids_3_T_5, UInt<1>(0h0))
[86] FIRRTL:365942 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_3_T_7 = and(_valids_3_T_4, _valids_3_T_6)
[87] FIRRTL:365943 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[3], _valids_3_T_7
[88] FIRRTL:365944 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[3] :
[89] FIRRTL:365945 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_3_br_mask_T = not(io.brupdate.b1.resolve_mask)
[90] FIRRTL:365946 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_3_br_mask_T_1 = and(uops[3].br_mask, _uops_3_br_mask_T)
[91] FIRRTL:365947 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[3].br_mask, _uops_3_br_mask_T_1
[92] FIRRTL:365948 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_4_T = and(io.brupdate.b1.mispredict_mask, uops[4].br_mask)
[93] FIRRTL:365949 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_4_T_1 = neq(_valids_4_T, UInt<1>(0h0))
[94] FIRRTL:365950 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_4_T_2 = or(_valids_4_T_1, UInt<1>(0h0))
[95] FIRRTL:365951 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_4_T_3 = eq(_valids_4_T_2, UInt<1>(0h0))
[96] FIRRTL:365952 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_4_T_4 = and(valids[4], _valids_4_T_3)
[97] FIRRTL:365953 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_4_T_5 = and(io.flush, UInt<1>(0h1))
[98] FIRRTL:365954 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_4_T_6 = eq(_valids_4_T_5, UInt<1>(0h0))
[99] FIRRTL:365955 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_4_T_7 = and(_valids_4_T_4, _valids_4_T_6)
[100] FIRRTL:365956 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[4], _valids_4_T_7
[101] FIRRTL:365957 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[4] :
[102] FIRRTL:365958 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_4_br_mask_T = not(io.brupdate.b1.resolve_mask)
[103] FIRRTL:365959 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_4_br_mask_T_1 = and(uops[4].br_mask, _uops_4_br_mask_T)
[104] FIRRTL:365960 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[4].br_mask, _uops_4_br_mask_T_1
[105] FIRRTL:365961 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_5_T = and(io.brupdate.b1.mispredict_mask, uops[5].br_mask)
[106] FIRRTL:365962 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_5_T_1 = neq(_valids_5_T, UInt<1>(0h0))
[107] FIRRTL:365963 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_5_T_2 = or(_valids_5_T_1, UInt<1>(0h0))
[108] FIRRTL:365964 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_5_T_3 = eq(_valids_5_T_2, UInt<1>(0h0))
[109] FIRRTL:365965 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_5_T_4 = and(valids[5], _valids_5_T_3)
[110] FIRRTL:365966 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_5_T_5 = and(io.flush, UInt<1>(0h1))
[111] FIRRTL:365967 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_5_T_6 = eq(_valids_5_T_5, UInt<1>(0h0))
[112] FIRRTL:365968 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_5_T_7 = and(_valids_5_T_4, _valids_5_T_6)
[113] FIRRTL:365969 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[5], _valids_5_T_7
[114] FIRRTL:365970 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[5] :
[115] FIRRTL:365971 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_5_br_mask_T = not(io.brupdate.b1.resolve_mask)
[116] FIRRTL:365972 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_5_br_mask_T_1 = and(uops[5].br_mask, _uops_5_br_mask_T)
[117] FIRRTL:365973 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[5].br_mask, _uops_5_br_mask_T_1
[118] FIRRTL:365974 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_6_T = and(io.brupdate.b1.mispredict_mask, uops[6].br_mask)
[119] FIRRTL:365975 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_6_T_1 = neq(_valids_6_T, UInt<1>(0h0))
[120] FIRRTL:365976 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_6_T_2 = or(_valids_6_T_1, UInt<1>(0h0))
[121] FIRRTL:365977 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_6_T_3 = eq(_valids_6_T_2, UInt<1>(0h0))
[122] FIRRTL:365978 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_6_T_4 = and(valids[6], _valids_6_T_3)
[123] FIRRTL:365979 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_6_T_5 = and(io.flush, UInt<1>(0h1))
[124] FIRRTL:365980 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_6_T_6 = eq(_valids_6_T_5, UInt<1>(0h0))
[125] FIRRTL:365981 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_6_T_7 = and(_valids_6_T_4, _valids_6_T_6)
[126] FIRRTL:365982 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[6], _valids_6_T_7
[127] FIRRTL:365983 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[6] :
[128] FIRRTL:365984 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_6_br_mask_T = not(io.brupdate.b1.resolve_mask)
[129] FIRRTL:365985 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_6_br_mask_T_1 = and(uops[6].br_mask, _uops_6_br_mask_T)
[130] FIRRTL:365986 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[6].br_mask, _uops_6_br_mask_T_1
[131] FIRRTL:365987 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:51 KIND:node :: node _valids_7_T = and(io.brupdate.b1.mispredict_mask, uops[7].br_mask)
[132] FIRRTL:365988 SRC:generators/boom/src/main/scala/v4/util/util.scala:126:59 KIND:node :: node _valids_7_T_1 = neq(_valids_7_T, UInt<1>(0h0))
[133] FIRRTL:365989 SRC:generators/boom/src/main/scala/v4/util/util.scala:61:61 KIND:node :: node _valids_7_T_2 = or(_valids_7_T_1, UInt<1>(0h0))
[134] FIRRTL:365990 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:34 KIND:node :: node _valids_7_T_3 = eq(_valids_7_T_2, UInt<1>(0h0))
[135] FIRRTL:365991 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:31 KIND:node :: node _valids_7_T_4 = and(valids[7], _valids_7_T_3)
[136] FIRRTL:365992 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:94 KIND:node :: node _valids_7_T_5 = and(io.flush, UInt<1>(0h1))
[137] FIRRTL:365993 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:83 KIND:node :: node _valids_7_T_6 = eq(_valids_7_T_5, UInt<1>(0h0))
[138] FIRRTL:365994 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:80 KIND:node :: node _valids_7_T_7 = and(_valids_7_T_4, _valids_7_T_6)
[139] FIRRTL:365995 SRC:generators/boom/src/main/scala/v4/util/util.scala:539:18 KIND:connect :: connect valids[7], _valids_7_T_7
[140] FIRRTL:365996 SRC:generators/boom/src/main/scala/v4/util/util.scala:540:24 KIND:when :: when valids[7] :
[141] FIRRTL:365997 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:23 KIND:node :: node _uops_7_br_mask_T = not(io.brupdate.b1.resolve_mask)
[142] FIRRTL:365998 SRC:generators/boom/src/main/scala/v4/util/util.scala:97:21 KIND:node :: node _uops_7_br_mask_T_1 = and(uops[7].br_mask, _uops_7_br_mask_T)
[143] FIRRTL:365999 SRC:generators/boom/src/main/scala/v4/util/util.scala:541:25 KIND:connect :: connect uops[7].br_mask, _uops_7_br_mask_T_1
[144] FIRRTL:366000 SRC:generators/boom/src/main/scala/v4/util/util.scala:545:19 KIND:when :: when do_enq :
[145] FIRRTL:366001 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:10 KIND:infer_mport :: infer mport MPORT = ram[enq_ptr_value], clock
[146] FIRRTL:366002 SRC:generators/boom/src/main/scala/v4/util/util.scala:546:35 KIND:connect :: connect MPORT, io.enq.bits
[147] FIRRTL:366003 SRC:generators/boom/src/main/scala/v4/util/util.scala:547:35 KIND:connect :: connect valids[enq_ptr_value], UInt<1>(0h1)
[148] FIRRTL:366004 SRC:generators/boom/src/main/scala/v4/util/util.scala:548:35 KIND:connect :: connect uops[enq_ptr_value], io.enq.bits.uop
[149] FIRRTL:366005 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:27 KIND:node :: node _uops_br_mask_T = not(io.brupdate.b1.resolve_mask)
[150] FIRRTL:366006 SRC:generators/boom/src/main/scala/v4/util/util.scala:93:25 KIND:node :: node _uops_br_mask_T_1 = and(io.enq.bits.uop.br_mask, _uops_br_mask_T)
[151] FIRRTL:366007 SRC:generators/boom/src/main/scala/v4/util/util.scala:549:35 KIND:connect :: connect uops[enq_ptr_value].br_mask, _uops_br_mask_T_1
[152] FIRRTL:366008 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap = eq(enq_ptr_value, UInt<3>(0h7))
[153] FIRRTL:366009 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T = add(enq_ptr_value, UInt<1>(0h1))
[154] FIRRTL:366010 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_1 = tail(_value_T, 1)
[155] FIRRTL:366011 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect enq_ptr_value, _value_T_1
[156] FIRRTL:366012 SRC:generators/boom/src/main/scala/v4/util/util.scala:553:19 KIND:when :: when do_deq :
[157] FIRRTL:366013 SRC:generators/boom/src/main/scala/v4/util/util.scala:554:29 KIND:connect :: connect valids[deq_ptr_value], UInt<1>(0h0)
[158] FIRRTL:366014 SRC:src/main/scala/chisel3/util/Counter.scala:73:24 KIND:node :: node wrap_1 = eq(deq_ptr_value, UInt<3>(0h7))
[159] FIRRTL:366015 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_2 = add(deq_ptr_value, UInt<1>(0h1))
[160] FIRRTL:366016 SRC:src/main/scala/chisel3/util/Counter.scala:77:24 KIND:node :: node _value_T_3 = tail(_value_T_2, 1)
[161] FIRRTL:366017 SRC:src/main/scala/chisel3/util/Counter.scala:77:15 KIND:connect :: connect deq_ptr_value, _value_T_3
[162] FIRRTL:366018 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:18 KIND:node :: node _T = neq(do_enq, do_deq)
[163] FIRRTL:366019 SRC:generators/boom/src/main/scala/v4/util/util.scala:558:30 KIND:when :: when _T :
[164] FIRRTL:366020 SRC:generators/boom/src/main/scala/v4/util/util.scala:559:18 KIND:connect :: connect maybe_full, do_enq
[165] FIRRTL:366021 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:21 KIND:node :: node _io_enq_ready_T = eq(full, UInt<1>(0h0))
[166] FIRRTL:366022 SRC:generators/boom/src/main/scala/v4/util/util.scala:562:18 KIND:connect :: connect io.enq.ready, _io_enq_ready_T
[167] FIRRTL:366023 SRC:generators/boom/src/main/scala/v4/util/util.scala:564:19 KIND:wire :: wire out : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, data : UInt<64>}
[168] FIRRTL:366024 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:27 KIND:infer_mport :: infer mport out_MPORT = ram[deq_ptr_value], clock
[169] FIRRTL:366025 SRC:generators/boom/src/main/scala/v4/util/util.scala:565:21 KIND:connect :: connect out, out_MPORT
[170] FIRRTL:366026 SRC:generators/boom/src/main/scala/v4/util/util.scala:566:21 KIND:connect :: connect out.uop, uops[deq_ptr_value]
[171] FIRRTL:366027 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:32 KIND:node :: node _io_deq_valid_T = eq(io.empty, UInt<1>(0h0))
[172] FIRRTL:366028 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:42 KIND:node :: node _io_deq_valid_T_1 = and(_io_deq_valid_T, valids[deq_ptr_value])
[173] FIRRTL:366029 SRC:generators/boom/src/main/scala/v4/util/util.scala:567:29 KIND:connect :: connect io.deq.valid, _io_deq_valid_T_1
[174] FIRRTL:366030 SRC:generators/boom/src/main/scala/v4/util/util.scala:568:29 KIND:connect :: connect io.deq.bits, out
[175] FIRRTL:366031 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node _ptr_diff_T = sub(enq_ptr_value, deq_ptr_value)
[176] FIRRTL:366032 SRC:generators/boom/src/main/scala/v4/util/util.scala:570:34 KIND:node :: node ptr_diff = tail(_ptr_diff_T, 1)
[177] FIRRTL:366033 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:34 KIND:node :: node _io_count_T = and(maybe_full, ptr_match)
[178] FIRRTL:366034 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:22 KIND:node :: node _io_count_T_1 = cat(_io_count_T, ptr_diff)
[179] FIRRTL:366035 SRC:generators/boom/src/main/scala/v4/util/util.scala:572:16 KIND:connect :: connect io.count, _io_count_T_1
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
  "task_id": "leaf_abstraction-LSU.retry_queue-4e9eb249feec6033",
  "work_unit_id": "LSU.retry_queue",
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
