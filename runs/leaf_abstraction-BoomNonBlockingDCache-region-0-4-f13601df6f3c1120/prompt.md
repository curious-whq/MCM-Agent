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

Task ID: `leaf_abstraction-BoomNonBlockingDCache-region-0-4-f13601df6f3c1120`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache::region-0-4`
- module: `BoomNonBlockingDCache`
- kind: `region`
- instance path: `BoomNonBlockingDCache`
- leaf: `True`
- coverage complete: `True`
- raw statements: 5
- logical statements: 3
- mapped/logical source lines: 2
- registers: 0
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

- `BoomNonBlockingDCache::io.lsu.req.fire`
  - predicate: `io.lsu.req.valid && io.lsu.req.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.lsu.req.bits[0].bits.addr', 'io.lsu.req.bits[0].bits.data', 'io.lsu.req.bits[0].bits.is_hella', 'io.lsu.req.bits[0].bits.uop.bp_debug_if', 'io.lsu.req.bits[0].bits.uop.bp_xcpt_if', 'io.lsu.req.bits[0].bits.uop.br_mask', 'io.lsu.req.bits[0].bits.uop.br_tag', 'io.lsu.req.bits[0].bits.uop.br_type', 'io.lsu.req.bits[0].bits.uop.csr_cmd', 'io.lsu.req.bits[0].bits.uop.debug_fsrc', 'io.lsu.req.bits[0].bits.uop.debug_inst', 'io.lsu.req.bits[0].bits.uop.debug_pc', 'io.lsu.req.bits[0].bits.uop.debug_tsrc', 'io.lsu.req.bits[0].bits.uop.dis_col_sel', 'io.lsu.req.bits[0].bits.uop.dst_rtype', 'io.lsu.req.bits[0].bits.uop.edge_inst', 'io.lsu.req.bits[0].bits.uop.exc_cause', 'io.lsu.req.bits[0].bits.uop.exception', 'io.lsu.req.bits[0].bits.uop.fcn_dw', 'io.lsu.req.bits[0].bits.uop.fcn_op', 'io.lsu.req.bits[0].bits.uop.flush_on_commit', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.div', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fastpipe', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fma', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.fromint', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ldst', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren1', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren2', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.ren3', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.sqrt', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.swap12', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.swap23', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.toint', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.typeTagIn', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.typeTagOut', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.vec', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.wen', 'io.lsu.req.bits[0].bits.uop.fp_ctrl.wflags', 'io.lsu.req.bits[0].bits.uop.fp_rm', 'io.lsu.req.bits[0].bits.uop.fp_typ', 'io.lsu.req.bits[0].bits.uop.fp_val', 'io.lsu.req.bits[0].bits.uop.frs3_en', 'io.lsu.req.bits[0].bits.uop.ftq_idx', 'io.lsu.req.bits[0].bits.uop.fu_code[0]', 'io.lsu.req.bits[0].bits.uop.fu_code[1]', 'io.lsu.req.bits[0].bits.uop.fu_code[2]', 'io.lsu.req.bits[0].bits.uop.fu_code[3]', 'io.lsu.req.bits[0].bits.uop.fu_code[4]', 'io.lsu.req.bits[0].bits.uop.fu_code[5]', 'io.lsu.req.bits[0].bits.uop.fu_code[6]', 'io.lsu.req.bits[0].bits.uop.fu_code[7]', 'io.lsu.req.bits[0].bits.uop.fu_code[8]', 'io.lsu.req.bits[0].bits.uop.fu_code[9]', 'io.lsu.req.bits[0].bits.uop.imm_packed', 'io.lsu.req.bits[0].bits.uop.imm_rename', 'io.lsu.req.bits[0].bits.uop.imm_sel', 'io.lsu.req.bits[0].bits.uop.inst', 'io.lsu.req.bits[0].bits.uop.iq_type[0]', 'io.lsu.req.bits[0].bits.uop.iq_type[1]', 'io.lsu.req.bits[0].bits.uop.iq_type[2]', 'io.lsu.req.bits[0].bits.uop.iq_type[3]', 'io.lsu.req.bits[0].bits.uop.is_amo', 'io.lsu.req.bits[0].bits.uop.is_eret', 'io.lsu.req.bits[0].bits.uop.is_fence', 'io.lsu.req.bits[0].bits.uop.is_fencei', 'io.lsu.req.bits[0].bits.uop.is_mov', 'io.lsu.req.bits[0].bits.uop.is_rocc', 'io.lsu.req.bits[0].bits.uop.is_rvc', 'io.lsu.req.bits[0].bits.uop.is_sfb', 'io.lsu.req.bits[0].bits.uop.is_sfence', 'io.lsu.req.bits[0].bits.uop.is_sys_pc2epc', 'io.lsu.req.bits[0].bits.uop.is_unique', 'io.lsu.req.bits[0].bits.uop.iw_issued', 'io.lsu.req.bits[0].bits.uop.iw_issued_partial_agen', 'io.lsu.req.bits[0].bits.uop.iw_issued_partial_dgen', 'io.lsu.req.bits[0].bits.uop.iw_p1_bypass_hint', 'io.lsu.req.bits[0].bits.uop.iw_p1_speculative_child', 'io.lsu.req.bits[0].bits.uop.iw_p2_bypass_hint', 'io.lsu.req.bits[0].bits.uop.iw_p2_speculative_child', 'io.lsu.req.bits[0].bits.uop.iw_p3_bypass_hint', 'io.lsu.req.bits[0].bits.uop.ldq_idx', 'io.lsu.req.bits[0].bits.uop.ldst', 'io.lsu.req.bits[0].bits.uop.ldst_is_rs1', 'io.lsu.req.bits[0].bits.uop.lrs1', 'io.lsu.req.bits[0].bits.uop.lrs1_rtype', 'io.lsu.req.bits[0].bits.uop.lrs2', 'io.lsu.req.bits[0].bits.uop.lrs2_rtype', 'io.lsu.req.bits[0].bits.uop.lrs3', 'io.lsu.req.bits[0].bits.uop.mem_cmd', 'io.lsu.req.bits[0].bits.uop.mem_signed', 'io.lsu.req.bits[0].bits.uop.mem_size', 'io.lsu.req.bits[0].bits.uop.op1_sel', 'io.lsu.req.bits[0].bits.uop.op2_sel', 'io.lsu.req.bits[0].bits.uop.pc_lob', 'io.lsu.req.bits[0].bits.uop.pdst', 'io.lsu.req.bits[0].bits.uop.pimm', 'io.lsu.req.bits[0].bits.uop.ppred', 'io.lsu.req.bits[0].bits.uop.ppred_busy', 'io.lsu.req.bits[0].bits.uop.prs1', 'io.lsu.req.bits[0].bits.uop.prs1_busy', 'io.lsu.req.bits[0].bits.uop.prs2', 'io.lsu.req.bits[0].bits.uop.prs2_busy', 'io.lsu.req.bits[0].bits.uop.prs3', 'io.lsu.req.bits[0].bits.uop.prs3_busy', 'io.lsu.req.bits[0].bits.uop.rob_idx', 'io.lsu.req.bits[0].bits.uop.rxq_idx', 'io.lsu.req.bits[0].bits.uop.stale_pdst', 'io.lsu.req.bits[0].bits.uop.stq_idx', 'io.lsu.req.bits[0].bits.uop.taken', 'io.lsu.req.bits[0].bits.uop.uses_ldq', 'io.lsu.req.bits[0].bits.uop.uses_stq', 'io.lsu.req.bits[0].bits.uop.xcpt_ae_if', 'io.lsu.req.bits[0].bits.uop.xcpt_ma_if', 'io.lsu.req.bits[0].bits.uop.xcpt_pf_if', 'io.lsu.req.bits[0].valid']
  - immediate registers: []
  - historical registers: []

## Concrete local state

[]

## Environment/frontier signals

['block_incoming_reqs', 'dataReadArb.io.in[2].ready', 'h0', 'h1', 'io.lsu.req.ready', 'metaReadArb.io.in[4].ready', 'mshrs.io.resp.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:509-512
```scala
  // we should block incoming requests when the MSHR trying to respond
  val block_incoming_reqs = (lsuWidth == 1).B && mshrs.io.resp.valid
  io.lsu.req.ready := metaReadArb.io.in(4).ready && dataReadArb.io.in(2).ready && !block_incoming_reqs
  metaReadArb.io.in(4).valid := io.lsu.req.valid && !block_incoming_reqs
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[271] FIRRTL:198040 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:510:47 KIND:node :: node block_incoming_reqs = and(UInt<1>(0h1), mshrs.io.resp.valid)
[272] FIRRTL:198041 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:511:50 KIND:node :: node _io_lsu_req_ready_T = and(metaReadArb.io.in[4].ready, dataReadArb.io.in[2].ready)
[273] FIRRTL:198042 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:511:83 KIND:node :: node _io_lsu_req_ready_T_1 = eq(block_incoming_reqs, UInt<1>(0h0))
[274] FIRRTL:198043 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:511:80 KIND:node :: node _io_lsu_req_ready_T_2 = and(_io_lsu_req_ready_T, _io_lsu_req_ready_T_1)
[275] FIRRTL:198044 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:511:20 KIND:connect :: connect io.lsu.req.ready, _io_lsu_req_ready_T_2
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-4-f13601df6f3c1120",
  "work_unit_id": "BoomNonBlockingDCache::region-0-4",
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
