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

Task ID: `leaf_abstraction-LSU.logic-e41a1cc2550d9194`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.12`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.logic`
- module: `ForwardingAgeLogic`
- kind: `module`
- instance path: `LSU.logic`
- leaf: `True`
- coverage complete: `True`
- raw statements: 117
- logical statements: 20
- mapped/logical source lines: 19
- registers: 2
- physical boundary events: 0

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



## Concrete local state

['found_idx', 'found_match']

## Environment/frontier signals

['clock', 'io.found', 'io.found_idx', 'io.matches', 'io.youngest']

## Source evidence

No source root was supplied/resolved. Use the FIRRTL statement ledger below and its exact source locators; do not guess missing Scala text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:366129 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2014:7 KIND:structural :: input clock : Clock
[1] FIRRTL:366130 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2014:7 KIND:structural :: input reset : Reset
[2] FIRRTL:366131 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2016:14 KIND:structural :: output io : { flip matches : UInt<8>, flip youngest : UInt<3>, found : UInt<1>, found_idx : UInt<3>}
[3] FIRRTL:366133 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2027:22 KIND:wire :: wire age_mask : UInt<1>[8]
[4] FIRRTL:366134 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[0], UInt<1>(0h1)
[5] FIRRTL:366135 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T = geq(UInt<1>(0h0), io.youngest)
[6] FIRRTL:366136 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T :
[7] FIRRTL:366137 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[0], UInt<1>(0h0)
[8] FIRRTL:366138 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[1], UInt<1>(0h1)
[9] FIRRTL:366139 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_1 = geq(UInt<1>(0h1), io.youngest)
[10] FIRRTL:366140 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_1 :
[11] FIRRTL:366141 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[1], UInt<1>(0h0)
[12] FIRRTL:366142 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[2], UInt<1>(0h1)
[13] FIRRTL:366143 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_2 = geq(UInt<2>(0h2), io.youngest)
[14] FIRRTL:366144 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_2 :
[15] FIRRTL:366145 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[2], UInt<1>(0h0)
[16] FIRRTL:366146 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[3], UInt<1>(0h1)
[17] FIRRTL:366147 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_3 = geq(UInt<2>(0h3), io.youngest)
[18] FIRRTL:366148 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_3 :
[19] FIRRTL:366149 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[3], UInt<1>(0h0)
[20] FIRRTL:366150 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[4], UInt<1>(0h1)
[21] FIRRTL:366151 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_4 = geq(UInt<3>(0h4), io.youngest)
[22] FIRRTL:366152 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_4 :
[23] FIRRTL:366153 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[4], UInt<1>(0h0)
[24] FIRRTL:366154 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[5], UInt<1>(0h1)
[25] FIRRTL:366155 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_5 = geq(UInt<3>(0h5), io.youngest)
[26] FIRRTL:366156 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_5 :
[27] FIRRTL:366157 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[5], UInt<1>(0h0)
[28] FIRRTL:366158 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[6], UInt<1>(0h1)
[29] FIRRTL:366159 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_6 = geq(UInt<3>(0h6), io.youngest)
[30] FIRRTL:366160 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_6 :
[31] FIRRTL:366161 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[6], UInt<1>(0h0)
[32] FIRRTL:366162 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2030:17 KIND:connect :: connect age_mask[7], UInt<1>(0h1)
[33] FIRRTL:366163 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2031:15 KIND:node :: node _T_7 = geq(UInt<3>(0h7), io.youngest)
[34] FIRRTL:366164 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2032:5 KIND:when :: when _T_7 :
[35] FIRRTL:366165 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2033:19 KIND:connect :: connect age_mask[7], UInt<1>(0h0)
[36] FIRRTL:366166 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2038:21 KIND:wire :: wire matches : UInt<16>
[37] FIRRTL:366167 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_lo_lo = cat(age_mask[1], age_mask[0])
[38] FIRRTL:366168 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_lo_hi = cat(age_mask[3], age_mask[2])
[39] FIRRTL:366169 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_lo = cat(matches_lo_hi, matches_lo_lo)
[40] FIRRTL:366170 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_hi_lo = cat(age_mask[5], age_mask[4])
[41] FIRRTL:366171 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_hi_hi = cat(age_mask[7], age_mask[6])
[42] FIRRTL:366172 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node matches_hi = cat(matches_hi_hi, matches_hi_lo)
[43] FIRRTL:366173 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:40 KIND:node :: node _matches_T = cat(matches_hi, matches_lo)
[44] FIRRTL:366174 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:29 KIND:node :: node _matches_T_1 = and(io.matches, _matches_T)
[45] FIRRTL:366175 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:17 KIND:node :: node _matches_T_2 = cat(_matches_T_1, io.matches)
[46] FIRRTL:366176 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2039:11 KIND:connect :: connect matches, _matches_T_2
[47] FIRRTL:366177 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2042:24 KIND:reg :: reg found_match : UInt<1>, clock
[48] FIRRTL:366178 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2043:22 KIND:reg :: reg found_idx : UInt<3>, clock
[49] FIRRTL:366179 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2044:21 KIND:connect :: connect found_match, UInt<1>(0h0)
[50] FIRRTL:366180 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2045:21 KIND:connect :: connect found_idx, UInt<1>(0h0)
[51] FIRRTL:366181 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2047:16 KIND:connect :: connect io.found_idx, found_idx
[52] FIRRTL:366182 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2048:12 KIND:connect :: connect io.found, found_match
[53] FIRRTL:366183 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_8 = bits(matches, 0, 0)
[54] FIRRTL:366184 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_8 :
[55] FIRRTL:366185 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[56] FIRRTL:366186 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<1>(0h0)
[57] FIRRTL:366187 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_9 = bits(matches, 1, 1)
[58] FIRRTL:366188 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_9 :
[59] FIRRTL:366189 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[60] FIRRTL:366190 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<1>(0h1)
[61] FIRRTL:366191 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_10 = bits(matches, 2, 2)
[62] FIRRTL:366192 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_10 :
[63] FIRRTL:366193 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[64] FIRRTL:366194 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<2>(0h2)
[65] FIRRTL:366195 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_11 = bits(matches, 3, 3)
[66] FIRRTL:366196 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_11 :
[67] FIRRTL:366197 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[68] FIRRTL:366198 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<2>(0h3)
[69] FIRRTL:366199 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_12 = bits(matches, 4, 4)
[70] FIRRTL:366200 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_12 :
[71] FIRRTL:366201 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[72] FIRRTL:366202 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h4)
[73] FIRRTL:366203 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_13 = bits(matches, 5, 5)
[74] FIRRTL:366204 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_13 :
[75] FIRRTL:366205 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[76] FIRRTL:366206 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h5)
[77] FIRRTL:366207 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_14 = bits(matches, 6, 6)
[78] FIRRTL:366208 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_14 :
[79] FIRRTL:366209 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[80] FIRRTL:366210 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h6)
[81] FIRRTL:366211 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_15 = bits(matches, 7, 7)
[82] FIRRTL:366212 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_15 :
[83] FIRRTL:366213 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[84] FIRRTL:366214 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h7)
[85] FIRRTL:366215 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_16 = bits(matches, 8, 8)
[86] FIRRTL:366216 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_16 :
[87] FIRRTL:366217 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[88] FIRRTL:366218 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<1>(0h0)
[89] FIRRTL:366219 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_17 = bits(matches, 9, 9)
[90] FIRRTL:366220 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_17 :
[91] FIRRTL:366221 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[92] FIRRTL:366222 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<1>(0h1)
[93] FIRRTL:366223 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_18 = bits(matches, 10, 10)
[94] FIRRTL:366224 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_18 :
[95] FIRRTL:366225 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[96] FIRRTL:366226 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<2>(0h2)
[97] FIRRTL:366227 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_19 = bits(matches, 11, 11)
[98] FIRRTL:366228 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_19 :
[99] FIRRTL:366229 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[100] FIRRTL:366230 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<2>(0h3)
[101] FIRRTL:366231 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_20 = bits(matches, 12, 12)
[102] FIRRTL:366232 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_20 :
[103] FIRRTL:366233 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[104] FIRRTL:366234 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h4)
[105] FIRRTL:366235 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_21 = bits(matches, 13, 13)
[106] FIRRTL:366236 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_21 :
[107] FIRRTL:366237 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[108] FIRRTL:366238 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h5)
[109] FIRRTL:366239 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_22 = bits(matches, 14, 14)
[110] FIRRTL:366240 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_22 :
[111] FIRRTL:366241 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[112] FIRRTL:366242 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h6)
[113] FIRRTL:366243 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2053:20 KIND:node :: node _T_23 = bits(matches, 15, 15)
[114] FIRRTL:366244 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2054:7 KIND:when :: when _T_23 :
[115] FIRRTL:366245 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2055:22 KIND:connect :: connect found_match, UInt<1>(0h1)
[116] FIRRTL:366246 SRC:generators/boom/src/main/scala/v4/lsu/lsu.scala:2056:20 KIND:connect :: connect found_idx, UInt<3>(0h7)
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
  "task_id": "leaf_abstraction-LSU.logic-e41a1cc2550d9194",
  "work_unit_id": "LSU.logic",
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
