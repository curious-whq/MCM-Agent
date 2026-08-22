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

Task ID: `leaf_abstraction-LSU.wakeupArbs_0-ff3ba2cdefa94ee7`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.wakeupArbs_0`
- module: `Arbiter2_Wakeup`
- kind: `module`
- instance path: `LSU.wakeupArbs_0`
- leaf: `True`
- coverage complete: `True`
- raw statements: 16
- logical statements: 12
- mapped/logical source lines: 10
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

- `LSU.wakeupArbs_0::io.in[0].fire`
  - predicate: `io.in[0].valid && io.in[0].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[0].bits.bypassable', 'io.in[0].bits.rebusy', 'io.in[0].bits.speculative_mask', 'io.in[0].bits.uop.bp_debug_if', 'io.in[0].bits.uop.bp_xcpt_if', 'io.in[0].bits.uop.br_mask', 'io.in[0].bits.uop.br_tag', 'io.in[0].bits.uop.br_type', 'io.in[0].bits.uop.csr_cmd', 'io.in[0].bits.uop.debug_fsrc', 'io.in[0].bits.uop.debug_inst', 'io.in[0].bits.uop.debug_pc', 'io.in[0].bits.uop.debug_tsrc', 'io.in[0].bits.uop.dis_col_sel', 'io.in[0].bits.uop.dst_rtype', 'io.in[0].bits.uop.edge_inst', 'io.in[0].bits.uop.exc_cause', 'io.in[0].bits.uop.exception', 'io.in[0].bits.uop.fcn_dw', 'io.in[0].bits.uop.fcn_op', 'io.in[0].bits.uop.flush_on_commit', 'io.in[0].bits.uop.fp_ctrl.div', 'io.in[0].bits.uop.fp_ctrl.fastpipe', 'io.in[0].bits.uop.fp_ctrl.fma', 'io.in[0].bits.uop.fp_ctrl.fromint', 'io.in[0].bits.uop.fp_ctrl.ldst', 'io.in[0].bits.uop.fp_ctrl.ren1', 'io.in[0].bits.uop.fp_ctrl.ren2', 'io.in[0].bits.uop.fp_ctrl.ren3', 'io.in[0].bits.uop.fp_ctrl.sqrt', 'io.in[0].bits.uop.fp_ctrl.swap12', 'io.in[0].bits.uop.fp_ctrl.swap23', 'io.in[0].bits.uop.fp_ctrl.toint', 'io.in[0].bits.uop.fp_ctrl.typeTagIn', 'io.in[0].bits.uop.fp_ctrl.typeTagOut', 'io.in[0].bits.uop.fp_ctrl.vec', 'io.in[0].bits.uop.fp_ctrl.wen', 'io.in[0].bits.uop.fp_ctrl.wflags', 'io.in[0].bits.uop.fp_rm', 'io.in[0].bits.uop.fp_typ', 'io.in[0].bits.uop.fp_val', 'io.in[0].bits.uop.frs3_en', 'io.in[0].bits.uop.ftq_idx', 'io.in[0].bits.uop.fu_code[0]', 'io.in[0].bits.uop.fu_code[1]', 'io.in[0].bits.uop.fu_code[2]', 'io.in[0].bits.uop.fu_code[3]', 'io.in[0].bits.uop.fu_code[4]', 'io.in[0].bits.uop.fu_code[5]', 'io.in[0].bits.uop.fu_code[6]', 'io.in[0].bits.uop.fu_code[7]', 'io.in[0].bits.uop.fu_code[8]', 'io.in[0].bits.uop.fu_code[9]', 'io.in[0].bits.uop.imm_packed', 'io.in[0].bits.uop.imm_rename', 'io.in[0].bits.uop.imm_sel', 'io.in[0].bits.uop.inst', 'io.in[0].bits.uop.iq_type[0]', 'io.in[0].bits.uop.iq_type[1]', 'io.in[0].bits.uop.iq_type[2]', 'io.in[0].bits.uop.iq_type[3]', 'io.in[0].bits.uop.is_amo', 'io.in[0].bits.uop.is_eret', 'io.in[0].bits.uop.is_fence', 'io.in[0].bits.uop.is_fencei', 'io.in[0].bits.uop.is_mov', 'io.in[0].bits.uop.is_rocc', 'io.in[0].bits.uop.is_rvc', 'io.in[0].bits.uop.is_sfb', 'io.in[0].bits.uop.is_sfence', 'io.in[0].bits.uop.is_sys_pc2epc', 'io.in[0].bits.uop.is_unique', 'io.in[0].bits.uop.iw_issued', 'io.in[0].bits.uop.iw_issued_partial_agen', 'io.in[0].bits.uop.iw_issued_partial_dgen', 'io.in[0].bits.uop.iw_p1_bypass_hint', 'io.in[0].bits.uop.iw_p1_speculative_child', 'io.in[0].bits.uop.iw_p2_bypass_hint', 'io.in[0].bits.uop.iw_p2_speculative_child', 'io.in[0].bits.uop.iw_p3_bypass_hint', 'io.in[0].bits.uop.ldq_idx', 'io.in[0].bits.uop.ldst', 'io.in[0].bits.uop.ldst_is_rs1', 'io.in[0].bits.uop.lrs1', 'io.in[0].bits.uop.lrs1_rtype', 'io.in[0].bits.uop.lrs2', 'io.in[0].bits.uop.lrs2_rtype', 'io.in[0].bits.uop.lrs3', 'io.in[0].bits.uop.mem_cmd', 'io.in[0].bits.uop.mem_signed', 'io.in[0].bits.uop.mem_size', 'io.in[0].bits.uop.op1_sel', 'io.in[0].bits.uop.op2_sel', 'io.in[0].bits.uop.pc_lob', 'io.in[0].bits.uop.pdst', 'io.in[0].bits.uop.pimm', 'io.in[0].bits.uop.ppred', 'io.in[0].bits.uop.ppred_busy', 'io.in[0].bits.uop.prs1', 'io.in[0].bits.uop.prs1_busy', 'io.in[0].bits.uop.prs2', 'io.in[0].bits.uop.prs2_busy', 'io.in[0].bits.uop.prs3', 'io.in[0].bits.uop.prs3_busy', 'io.in[0].bits.uop.rob_idx', 'io.in[0].bits.uop.rxq_idx', 'io.in[0].bits.uop.stale_pdst', 'io.in[0].bits.uop.stq_idx', 'io.in[0].bits.uop.taken', 'io.in[0].bits.uop.uses_ldq', 'io.in[0].bits.uop.uses_stq', 'io.in[0].bits.uop.xcpt_ae_if', 'io.in[0].bits.uop.xcpt_ma_if', 'io.in[0].bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []
- `LSU.wakeupArbs_0::io.in[1].fire`
  - predicate: `io.in[1].valid && io.in[1].ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.in[1].bits.bypassable', 'io.in[1].bits.rebusy', 'io.in[1].bits.speculative_mask', 'io.in[1].bits.uop.bp_debug_if', 'io.in[1].bits.uop.bp_xcpt_if', 'io.in[1].bits.uop.br_mask', 'io.in[1].bits.uop.br_tag', 'io.in[1].bits.uop.br_type', 'io.in[1].bits.uop.csr_cmd', 'io.in[1].bits.uop.debug_fsrc', 'io.in[1].bits.uop.debug_inst', 'io.in[1].bits.uop.debug_pc', 'io.in[1].bits.uop.debug_tsrc', 'io.in[1].bits.uop.dis_col_sel', 'io.in[1].bits.uop.dst_rtype', 'io.in[1].bits.uop.edge_inst', 'io.in[1].bits.uop.exc_cause', 'io.in[1].bits.uop.exception', 'io.in[1].bits.uop.fcn_dw', 'io.in[1].bits.uop.fcn_op', 'io.in[1].bits.uop.flush_on_commit', 'io.in[1].bits.uop.fp_ctrl.div', 'io.in[1].bits.uop.fp_ctrl.fastpipe', 'io.in[1].bits.uop.fp_ctrl.fma', 'io.in[1].bits.uop.fp_ctrl.fromint', 'io.in[1].bits.uop.fp_ctrl.ldst', 'io.in[1].bits.uop.fp_ctrl.ren1', 'io.in[1].bits.uop.fp_ctrl.ren2', 'io.in[1].bits.uop.fp_ctrl.ren3', 'io.in[1].bits.uop.fp_ctrl.sqrt', 'io.in[1].bits.uop.fp_ctrl.swap12', 'io.in[1].bits.uop.fp_ctrl.swap23', 'io.in[1].bits.uop.fp_ctrl.toint', 'io.in[1].bits.uop.fp_ctrl.typeTagIn', 'io.in[1].bits.uop.fp_ctrl.typeTagOut', 'io.in[1].bits.uop.fp_ctrl.vec', 'io.in[1].bits.uop.fp_ctrl.wen', 'io.in[1].bits.uop.fp_ctrl.wflags', 'io.in[1].bits.uop.fp_rm', 'io.in[1].bits.uop.fp_typ', 'io.in[1].bits.uop.fp_val', 'io.in[1].bits.uop.frs3_en', 'io.in[1].bits.uop.ftq_idx', 'io.in[1].bits.uop.fu_code[0]', 'io.in[1].bits.uop.fu_code[1]', 'io.in[1].bits.uop.fu_code[2]', 'io.in[1].bits.uop.fu_code[3]', 'io.in[1].bits.uop.fu_code[4]', 'io.in[1].bits.uop.fu_code[5]', 'io.in[1].bits.uop.fu_code[6]', 'io.in[1].bits.uop.fu_code[7]', 'io.in[1].bits.uop.fu_code[8]', 'io.in[1].bits.uop.fu_code[9]', 'io.in[1].bits.uop.imm_packed', 'io.in[1].bits.uop.imm_rename', 'io.in[1].bits.uop.imm_sel', 'io.in[1].bits.uop.inst', 'io.in[1].bits.uop.iq_type[0]', 'io.in[1].bits.uop.iq_type[1]', 'io.in[1].bits.uop.iq_type[2]', 'io.in[1].bits.uop.iq_type[3]', 'io.in[1].bits.uop.is_amo', 'io.in[1].bits.uop.is_eret', 'io.in[1].bits.uop.is_fence', 'io.in[1].bits.uop.is_fencei', 'io.in[1].bits.uop.is_mov', 'io.in[1].bits.uop.is_rocc', 'io.in[1].bits.uop.is_rvc', 'io.in[1].bits.uop.is_sfb', 'io.in[1].bits.uop.is_sfence', 'io.in[1].bits.uop.is_sys_pc2epc', 'io.in[1].bits.uop.is_unique', 'io.in[1].bits.uop.iw_issued', 'io.in[1].bits.uop.iw_issued_partial_agen', 'io.in[1].bits.uop.iw_issued_partial_dgen', 'io.in[1].bits.uop.iw_p1_bypass_hint', 'io.in[1].bits.uop.iw_p1_speculative_child', 'io.in[1].bits.uop.iw_p2_bypass_hint', 'io.in[1].bits.uop.iw_p2_speculative_child', 'io.in[1].bits.uop.iw_p3_bypass_hint', 'io.in[1].bits.uop.ldq_idx', 'io.in[1].bits.uop.ldst', 'io.in[1].bits.uop.ldst_is_rs1', 'io.in[1].bits.uop.lrs1', 'io.in[1].bits.uop.lrs1_rtype', 'io.in[1].bits.uop.lrs2', 'io.in[1].bits.uop.lrs2_rtype', 'io.in[1].bits.uop.lrs3', 'io.in[1].bits.uop.mem_cmd', 'io.in[1].bits.uop.mem_signed', 'io.in[1].bits.uop.mem_size', 'io.in[1].bits.uop.op1_sel', 'io.in[1].bits.uop.op2_sel', 'io.in[1].bits.uop.pc_lob', 'io.in[1].bits.uop.pdst', 'io.in[1].bits.uop.pimm', 'io.in[1].bits.uop.ppred', 'io.in[1].bits.uop.ppred_busy', 'io.in[1].bits.uop.prs1', 'io.in[1].bits.uop.prs1_busy', 'io.in[1].bits.uop.prs2', 'io.in[1].bits.uop.prs2_busy', 'io.in[1].bits.uop.prs3', 'io.in[1].bits.uop.prs3_busy', 'io.in[1].bits.uop.rob_idx', 'io.in[1].bits.uop.rxq_idx', 'io.in[1].bits.uop.stale_pdst', 'io.in[1].bits.uop.stq_idx', 'io.in[1].bits.uop.taken', 'io.in[1].bits.uop.uses_ldq', 'io.in[1].bits.uop.uses_stq', 'io.in[1].bits.uop.xcpt_ae_if', 'io.in[1].bits.uop.xcpt_ma_if', 'io.in[1].bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []
- `LSU.wakeupArbs_0::io.out.fire`
  - predicate: `io.out.valid && io.out.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.out.bits.bypassable', 'io.out.bits.rebusy', 'io.out.bits.speculative_mask', 'io.out.bits.uop.bp_debug_if', 'io.out.bits.uop.bp_xcpt_if', 'io.out.bits.uop.br_mask', 'io.out.bits.uop.br_tag', 'io.out.bits.uop.br_type', 'io.out.bits.uop.csr_cmd', 'io.out.bits.uop.debug_fsrc', 'io.out.bits.uop.debug_inst', 'io.out.bits.uop.debug_pc', 'io.out.bits.uop.debug_tsrc', 'io.out.bits.uop.dis_col_sel', 'io.out.bits.uop.dst_rtype', 'io.out.bits.uop.edge_inst', 'io.out.bits.uop.exc_cause', 'io.out.bits.uop.exception', 'io.out.bits.uop.fcn_dw', 'io.out.bits.uop.fcn_op', 'io.out.bits.uop.flush_on_commit', 'io.out.bits.uop.fp_ctrl.div', 'io.out.bits.uop.fp_ctrl.fastpipe', 'io.out.bits.uop.fp_ctrl.fma', 'io.out.bits.uop.fp_ctrl.fromint', 'io.out.bits.uop.fp_ctrl.ldst', 'io.out.bits.uop.fp_ctrl.ren1', 'io.out.bits.uop.fp_ctrl.ren2', 'io.out.bits.uop.fp_ctrl.ren3', 'io.out.bits.uop.fp_ctrl.sqrt', 'io.out.bits.uop.fp_ctrl.swap12', 'io.out.bits.uop.fp_ctrl.swap23', 'io.out.bits.uop.fp_ctrl.toint', 'io.out.bits.uop.fp_ctrl.typeTagIn', 'io.out.bits.uop.fp_ctrl.typeTagOut', 'io.out.bits.uop.fp_ctrl.vec', 'io.out.bits.uop.fp_ctrl.wen', 'io.out.bits.uop.fp_ctrl.wflags', 'io.out.bits.uop.fp_rm', 'io.out.bits.uop.fp_typ', 'io.out.bits.uop.fp_val', 'io.out.bits.uop.frs3_en', 'io.out.bits.uop.ftq_idx', 'io.out.bits.uop.fu_code[0]', 'io.out.bits.uop.fu_code[1]', 'io.out.bits.uop.fu_code[2]', 'io.out.bits.uop.fu_code[3]', 'io.out.bits.uop.fu_code[4]', 'io.out.bits.uop.fu_code[5]', 'io.out.bits.uop.fu_code[6]', 'io.out.bits.uop.fu_code[7]', 'io.out.bits.uop.fu_code[8]', 'io.out.bits.uop.fu_code[9]', 'io.out.bits.uop.imm_packed', 'io.out.bits.uop.imm_rename', 'io.out.bits.uop.imm_sel', 'io.out.bits.uop.inst', 'io.out.bits.uop.iq_type[0]', 'io.out.bits.uop.iq_type[1]', 'io.out.bits.uop.iq_type[2]', 'io.out.bits.uop.iq_type[3]', 'io.out.bits.uop.is_amo', 'io.out.bits.uop.is_eret', 'io.out.bits.uop.is_fence', 'io.out.bits.uop.is_fencei', 'io.out.bits.uop.is_mov', 'io.out.bits.uop.is_rocc', 'io.out.bits.uop.is_rvc', 'io.out.bits.uop.is_sfb', 'io.out.bits.uop.is_sfence', 'io.out.bits.uop.is_sys_pc2epc', 'io.out.bits.uop.is_unique', 'io.out.bits.uop.iw_issued', 'io.out.bits.uop.iw_issued_partial_agen', 'io.out.bits.uop.iw_issued_partial_dgen', 'io.out.bits.uop.iw_p1_bypass_hint', 'io.out.bits.uop.iw_p1_speculative_child', 'io.out.bits.uop.iw_p2_bypass_hint', 'io.out.bits.uop.iw_p2_speculative_child', 'io.out.bits.uop.iw_p3_bypass_hint', 'io.out.bits.uop.ldq_idx', 'io.out.bits.uop.ldst', 'io.out.bits.uop.ldst_is_rs1', 'io.out.bits.uop.lrs1', 'io.out.bits.uop.lrs1_rtype', 'io.out.bits.uop.lrs2', 'io.out.bits.uop.lrs2_rtype', 'io.out.bits.uop.lrs3', 'io.out.bits.uop.mem_cmd', 'io.out.bits.uop.mem_signed', 'io.out.bits.uop.mem_size', 'io.out.bits.uop.op1_sel', 'io.out.bits.uop.op2_sel', 'io.out.bits.uop.pc_lob', 'io.out.bits.uop.pdst', 'io.out.bits.uop.pimm', 'io.out.bits.uop.ppred', 'io.out.bits.uop.ppred_busy', 'io.out.bits.uop.prs1', 'io.out.bits.uop.prs1_busy', 'io.out.bits.uop.prs2', 'io.out.bits.uop.prs2_busy', 'io.out.bits.uop.prs3', 'io.out.bits.uop.prs3_busy', 'io.out.bits.uop.rob_idx', 'io.out.bits.uop.rxq_idx', 'io.out.bits.uop.stale_pdst', 'io.out.bits.uop.stq_idx', 'io.out.bits.uop.taken', 'io.out.bits.uop.uses_ldq', 'io.out.bits.uop.uses_stq', 'io.out.bits.uop.xcpt_ae_if', 'io.out.bits.uop.xcpt_ma_if', 'io.out.bits.uop.xcpt_pf_if']
  - immediate registers: []
  - historical registers: []

## Concrete local state

[]

## Environment/frontier signals

['io.chosen', 'io.in[0].ready', 'io.in[0].valid', 'io.in[1].ready', 'io.in[1].valid', 'io.out.bits.bypassable', 'io.out.bits.rebusy', 'io.out.bits.speculative_mask', 'io.out.bits.uop.bp_debug_if', 'io.out.bits.uop.bp_xcpt_if', 'io.out.bits.uop.br_mask', 'io.out.bits.uop.br_tag', 'io.out.bits.uop.br_type', 'io.out.bits.uop.csr_cmd', 'io.out.bits.uop.debug_fsrc', 'io.out.bits.uop.debug_inst', 'io.out.bits.uop.debug_pc', 'io.out.bits.uop.debug_tsrc', 'io.out.bits.uop.dis_col_sel', 'io.out.bits.uop.dst_rtype', 'io.out.bits.uop.edge_inst', 'io.out.bits.uop.exc_cause', 'io.out.bits.uop.exception', 'io.out.bits.uop.fcn_dw', 'io.out.bits.uop.fcn_op', 'io.out.bits.uop.flush_on_commit', 'io.out.bits.uop.fp_ctrl.div', 'io.out.bits.uop.fp_ctrl.fastpipe', 'io.out.bits.uop.fp_ctrl.fma', 'io.out.bits.uop.fp_ctrl.fromint', 'io.out.bits.uop.fp_ctrl.ldst', 'io.out.bits.uop.fp_ctrl.ren1', 'io.out.bits.uop.fp_ctrl.ren2', 'io.out.bits.uop.fp_ctrl.ren3', 'io.out.bits.uop.fp_ctrl.sqrt', 'io.out.bits.uop.fp_ctrl.swap12', 'io.out.bits.uop.fp_ctrl.swap23', 'io.out.bits.uop.fp_ctrl.toint', 'io.out.bits.uop.fp_ctrl.typeTagIn', 'io.out.bits.uop.fp_ctrl.typeTagOut', 'io.out.bits.uop.fp_ctrl.vec', 'io.out.bits.uop.fp_ctrl.wen', 'io.out.bits.uop.fp_ctrl.wflags', 'io.out.bits.uop.fp_rm', 'io.out.bits.uop.fp_typ', 'io.out.bits.uop.fp_val', 'io.out.bits.uop.frs3_en', 'io.out.bits.uop.ftq_idx', 'io.out.bits.uop.fu_code[0]', 'io.out.bits.uop.fu_code[1]', 'io.out.bits.uop.fu_code[2]', 'io.out.bits.uop.fu_code[3]', 'io.out.bits.uop.fu_code[4]', 'io.out.bits.uop.fu_code[5]', 'io.out.bits.uop.fu_code[6]', 'io.out.bits.uop.fu_code[7]', 'io.out.bits.uop.fu_code[8]', 'io.out.bits.uop.fu_code[9]', 'io.out.bits.uop.imm_packed', 'io.out.bits.uop.imm_rename', 'io.out.bits.uop.imm_sel', 'io.out.bits.uop.inst', 'io.out.bits.uop.iq_type[0]', 'io.out.bits.uop.iq_type[1]', 'io.out.bits.uop.iq_type[2]', 'io.out.bits.uop.iq_type[3]', 'io.out.bits.uop.is_amo', 'io.out.bits.uop.is_eret', 'io.out.bits.uop.is_fence', 'io.out.bits.uop.is_fencei', 'io.out.bits.uop.is_mov', 'io.out.bits.uop.is_rocc', 'io.out.bits.uop.is_rvc', 'io.out.bits.uop.is_sfb', 'io.out.bits.uop.is_sfence', 'io.out.bits.uop.is_sys_pc2epc', 'io.out.bits.uop.is_unique', 'io.out.bits.uop.iw_issued', 'io.out.bits.uop.iw_issued_partial_agen', 'io.out.bits.uop.iw_issued_partial_dgen', 'io.out.bits.uop.iw_p1_bypass_hint', 'io.out.bits.uop.iw_p1_speculative_child', 'io.out.bits.uop.iw_p2_bypass_hint', 'io.out.bits.uop.iw_p2_speculative_child', 'io.out.bits.uop.iw_p3_bypass_hint', 'io.out.bits.uop.ldq_idx', 'io.out.bits.uop.ldst', 'io.out.bits.uop.ldst_is_rs1', 'io.out.bits.uop.lrs1', 'io.out.bits.uop.lrs1_rtype', 'io.out.bits.uop.lrs2', 'io.out.bits.uop.lrs2_rtype', 'io.out.bits.uop.lrs3', 'io.out.bits.uop.mem_cmd', 'io.out.bits.uop.mem_signed', 'io.out.bits.uop.mem_size', 'io.out.bits.uop.op1_sel', 'io.out.bits.uop.op2_sel', 'io.out.bits.uop.pc_lob', 'io.out.bits.uop.pdst', 'io.out.bits.uop.pimm', 'io.out.bits.uop.ppred', 'io.out.bits.uop.ppred_busy', 'io.out.bits.uop.prs1', 'io.out.bits.uop.prs1_busy', 'io.out.bits.uop.prs2', 'io.out.bits.uop.prs2_busy', 'io.out.bits.uop.prs3', 'io.out.bits.uop.prs3_busy', 'io.out.bits.uop.rob_idx', 'io.out.bits.uop.rxq_idx', 'io.out.bits.uop.stale_pdst', 'io.out.bits.uop.stq_idx', 'io.out.bits.uop.taken', 'io.out.bits.uop.uses_ldq', 'io.out.bits.uop.uses_stq', 'io.out.bits.uop.xcpt_ae_if', 'io.out.bits.uop.xcpt_ma_if', 'io.out.bits.uop.xcpt_pf_if', 'io.out.ready', 'io.out.valid']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:366110 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input clock : Clock
[1] FIRRTL:366111 SRC:src/main/scala/chisel3/util/Arbiter.scala:133:7 KIND:structural :: input reset : Reset
[2] FIRRTL:366112 SRC:src/main/scala/chisel3/util/Arbiter.scala:140:14 KIND:structural :: output io : { flip in : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, bypassable : UInt<1>, speculative_mask : UInt<1>, rebusy : UInt<1>}}[2], out : { flip ready : UInt<1>, valid : UInt<1>, bits : { uop : { inst : UInt<32>, debug_inst : UInt<32>, is_rvc : UInt<1>, debug_pc : UInt<40>, iq_type : UInt<1>[4], fu_code : UInt<1>[10], iw_issued : UInt<1>, iw_issued_partial_agen : UInt<1>, iw_issued_partial_dgen : UInt<1>, iw_p1_speculative_child : UInt<1>, iw_p2_speculative_child : UInt<1>, iw_p1_bypass_hint : UInt<1>, iw_p2_bypass_hint : UInt<1>, iw_p3_bypass_hint : UInt<1>, dis_col_sel : UInt<1>, br_mask : UInt<8>, br_tag : UInt<3>, br_type : UInt<4>, is_sfb : UInt<1>, is_fence : UInt<1>, is_fencei : UInt<1>, is_sfence : UInt<1>, is_amo : UInt<1>, is_eret : UInt<1>, is_sys_pc2epc : UInt<1>, is_rocc : UInt<1>, is_mov : UInt<1>, ftq_idx : UInt<4>, edge_inst : UInt<1>, pc_lob : UInt<6>, taken : UInt<1>, imm_rename : UInt<1>, imm_sel : UInt<3>, pimm : UInt<5>, imm_packed : UInt<20>, op1_sel : UInt<2>, op2_sel : UInt<3>, fp_ctrl : { ldst : UInt<1>, wen : UInt<1>, ren1 : UInt<1>, ren2 : UInt<1>, ren3 : UInt<1>, swap12 : UInt<1>, swap23 : UInt<1>, typeTagIn : UInt<2>, typeTagOut : UInt<2>, fromint : UInt<1>, toint : UInt<1>, fastpipe : UInt<1>, fma : UInt<1>, div : UInt<1>, sqrt : UInt<1>, wflags : UInt<1>, vec : UInt<1>}, rob_idx : UInt<5>, ldq_idx : UInt<4>, stq_idx : UInt<4>, rxq_idx : UInt<2>, pdst : UInt<6>, prs1 : UInt<6>, prs2 : UInt<6>, prs3 : UInt<6>, ppred : UInt<4>, prs1_busy : UInt<1>, prs2_busy : UInt<1>, prs3_busy : UInt<1>, ppred_busy : UInt<1>, stale_pdst : UInt<6>, exception : UInt<1>, exc_cause : UInt<64>, mem_cmd : UInt<5>, mem_size : UInt<2>, mem_signed : UInt<1>, uses_ldq : UInt<1>, uses_stq : UInt<1>, is_unique : UInt<1>, flush_on_commit : UInt<1>, csr_cmd : UInt<3>, ldst_is_rs1 : UInt<1>, ldst : UInt<6>, lrs1 : UInt<6>, lrs2 : UInt<6>, lrs3 : UInt<6>, dst_rtype : UInt<2>, lrs1_rtype : UInt<2>, lrs2_rtype : UInt<2>, frs3_en : UInt<1>, fcn_dw : UInt<1>, fcn_op : UInt<5>, fp_val : UInt<1>, fp_rm : UInt<3>, fp_typ : UInt<2>, xcpt_pf_if : UInt<1>, xcpt_ae_if : UInt<1>, xcpt_ma_if : UInt<1>, bp_debug_if : UInt<1>, bp_xcpt_if : UInt<1>, debug_fsrc : UInt<3>, debug_tsrc : UInt<3>}, bypassable : UInt<1>, speculative_mask : UInt<1>, rebusy : UInt<1>}}, chosen : UInt<1>}
[3] FIRRTL:366114 SRC:src/main/scala/chisel3/util/Arbiter.scala:142:13 KIND:connect :: connect io.chosen, UInt<1>(0h1)
[4] FIRRTL:366115 SRC:src/main/scala/chisel3/util/Arbiter.scala:143:15 KIND:connect :: connect io.out.bits, io.in[1].bits
[5] FIRRTL:366116 SRC:src/main/scala/chisel3/util/Arbiter.scala:145:26 KIND:when :: when io.in[0].valid :
[6] FIRRTL:366117 SRC:src/main/scala/chisel3/util/Arbiter.scala:146:17 KIND:connect :: connect io.chosen, UInt<1>(0h0)
[7] FIRRTL:366118 SRC:src/main/scala/chisel3/util/Arbiter.scala:147:19 KIND:connect :: connect io.out.bits, io.in[0].bits
[8] FIRRTL:366119 SRC:src/main/scala/chisel3/util/Arbiter.scala:45:78 KIND:node :: node grant_1 = eq(io.in[0].valid, UInt<1>(0h0))
[9] FIRRTL:366120 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_0_ready_T = and(UInt<1>(0h1), io.out.ready)
[10] FIRRTL:366121 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[0].ready, _io_in_0_ready_T
[11] FIRRTL:366122 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:19 KIND:node :: node _io_in_1_ready_T = and(grant_1, io.out.ready)
[12] FIRRTL:366123 SRC:src/main/scala/chisel3/util/Arbiter.scala:153:14 KIND:connect :: connect io.in[1].ready, _io_in_1_ready_T
[13] FIRRTL:366124 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:19 KIND:node :: node _io_out_valid_T = eq(grant_1, UInt<1>(0h0))
[14] FIRRTL:366125 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:31 KIND:node :: node _io_out_valid_T_1 = or(_io_out_valid_T, io.in[1].valid)
[15] FIRRTL:366126 SRC:src/main/scala/chisel3/util/Arbiter.scala:154:16 KIND:connect :: connect io.out.valid, _io_out_valid_T_1
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
  "task_id": "leaf_abstraction-LSU.wakeupArbs_0-ff3ba2cdefa94ee7",
  "work_unit_id": "LSU.wakeupArbs_0",
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
