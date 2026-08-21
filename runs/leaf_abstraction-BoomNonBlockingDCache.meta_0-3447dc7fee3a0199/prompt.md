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

Task ID: `leaf_abstraction-BoomNonBlockingDCache.meta_0-3447dc7fee3a0199`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.10`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache.meta_0`
- module: `L1MetadataArray`
- kind: `module`
- instance path: `BoomNonBlockingDCache.meta_0`
- leaf: `True`
- coverage complete: `True`
- raw statements: 91
- logical statements: 35
- mapped/logical source lines: 22
- registers: 1
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
   do not state `rf`, `co`, and `fr` as unrelated ordering approximations. If a semantic property that you judge
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

- `BoomNonBlockingDCache.meta_0::io.read.fire`
  - predicate: `io.read.valid && io.read.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.read.bits.idx', 'io.read.bits.tag', 'io.read.bits.way_en']
  - immediate registers: ['rst_cnt']
  - historical registers: ['rst_cnt']
- `BoomNonBlockingDCache.meta_0::io.write.fire`
  - predicate: `io.write.valid && io.write.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.write.bits.data.coh.state', 'io.write.bits.data.tag', 'io.write.bits.idx', 'io.write.bits.tag', 'io.write.bits.way_en']
  - immediate registers: ['rst_cnt']
  - historical registers: ['rst_cnt']

## Concrete local state

['rst_cnt']

## Environment/frontier signals

['clock', 'io.read.bits.idx', 'io.read.bits.way_en', 'io.read.ready', 'io.read.valid', 'io.resp[0].coh.state', 'io.resp[0].tag', 'io.resp[1].coh.state', 'io.resp[1].tag', 'io.resp[2].coh.state', 'io.resp[2].tag', 'io.resp[3].coh.state', 'io.resp[3].tag', 'io.write.bits.idx', 'io.write.bits.way_en', 'io.write.ready', 'io.write.valid']

## Source evidence

### generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:304-308
```scala
  def apply(tag: Bits, coh: ClientMetadata)(implicit p: Parameters) = {
    val meta = Wire(new L1Metadata)
    meta.tag := tag
    meta.coh := coh
    meta
```

### generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:321-325
```scala

class L1MetadataArray[T <: L1Metadata](onReset: () => T)(implicit p: Parameters) extends L1HellaCacheModule()(p) {
  val rstVal = onReset()
  val io = IO(new Bundle {
    val read = Flipped(Decoupled(new L1MetaReadReq))
```

### generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:329-337
```scala

  val rst_cnt = RegInit(0.U(log2Up(nSets+1).W))
  val rst = rst_cnt < nSets.U
  val waddr = Mux(rst, rst_cnt, io.write.bits.idx)
  val wdata = Mux(rst, rstVal, io.write.bits.data).asUInt
  val wmask = Mux(rst || (nWays == 1).B, (-1).S, io.write.bits.way_en.asSInt).asBools
  val rmask = Mux(rst || (nWays == 1).B, (-1).S, io.read.bits.way_en.asSInt).asBools
  when (rst) { rst_cnt := rst_cnt+1.U }
```

### generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:338-348
```scala
  val metabits = rstVal.getWidth
  val tag_array = SyncReadMem(nSets, Vec(nWays, UInt(metabits.W)))
  val wen = rst || io.write.valid
  when (wen) {
    tag_array.write(waddr, VecInit.fill(nWays)(wdata), wmask)
  }
  io.resp := tag_array.read(io.read.bits.idx, io.read.fire).map(_.asTypeOf(chiselTypeOf(rstVal)))

  io.read.ready := !wen // so really this could be a 6T RAM
  io.write.ready := !rst
}
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:159-162
```scala
  def apply(perm: UInt) = {
    val meta = Wire(new ClientMetadata)
    meta.state := perm
    meta
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:197272 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:322:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197273 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:322:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197274 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:324:14 KIND:structural :: output io : { flip read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}}, flip write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>, data : { coh : { state : UInt<2>}, tag : UInt<20>}}}, resp : { coh : { state : UInt<2>}, tag : UInt<20>}[4]}
[3] FIRRTL:197276 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire rstVal_meta : { state : UInt<2>}
[4] FIRRTL:197277 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect rstVal_meta.state, UInt<2>(0h0)
[5] FIRRTL:197278 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:305:20 KIND:wire :: wire rstVal : { coh : { state : UInt<2>}, tag : UInt<20>}
[6] FIRRTL:197279 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:306:14 KIND:connect :: connect rstVal.tag, UInt<1>(0h0)
[7] FIRRTL:197280 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:307:14 KIND:connect :: connect rstVal.coh, rstVal_meta
[8] FIRRTL:197281 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:330:24 KIND:regreset :: regreset rst_cnt : UInt<7>, clock, reset, UInt<7>(0h0)
[9] FIRRTL:197282 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:331:21 KIND:node :: node rst = lt(rst_cnt, UInt<7>(0h40))
[10] FIRRTL:197283 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:332:18 KIND:node :: node waddr = mux(rst, rst_cnt, io.write.bits.idx)
[11] FIRRTL:197284 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:333:18 KIND:node :: node _wdata_T = mux(rst, rstVal, io.write.bits.data)
[12] FIRRTL:197285 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:333:52 KIND:node :: node wdata = cat(_wdata_T.coh.state, _wdata_T.tag)
[13] FIRRTL:197286 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:23 KIND:node :: node _wmask_T = or(rst, UInt<1>(0h0))
[14] FIRRTL:197287 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:71 KIND:node :: node _wmask_T_1 = asSInt(io.write.bits.way_en)
[15] FIRRTL:197288 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:18 KIND:node :: node _wmask_T_2 = mux(_wmask_T, asSInt(UInt<1>(0h1)), _wmask_T_1)
[16] FIRRTL:197289 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:79 KIND:node :: node wmask_0 = bits(_wmask_T_2, 0, 0)
[17] FIRRTL:197290 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:79 KIND:node :: node wmask_1 = bits(_wmask_T_2, 1, 1)
[18] FIRRTL:197291 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:79 KIND:node :: node wmask_2 = bits(_wmask_T_2, 2, 2)
[19] FIRRTL:197292 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:334:79 KIND:node :: node wmask_3 = bits(_wmask_T_2, 3, 3)
[20] FIRRTL:197293 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:23 KIND:node :: node _rmask_T = or(rst, UInt<1>(0h0))
[21] FIRRTL:197294 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:70 KIND:node :: node _rmask_T_1 = asSInt(io.read.bits.way_en)
[22] FIRRTL:197295 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:18 KIND:node :: node _rmask_T_2 = mux(_rmask_T, asSInt(UInt<1>(0h1)), _rmask_T_1)
[23] FIRRTL:197296 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:78 KIND:node :: node rmask_0 = bits(_rmask_T_2, 0, 0)
[24] FIRRTL:197297 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:78 KIND:node :: node rmask_1 = bits(_rmask_T_2, 1, 1)
[25] FIRRTL:197298 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:78 KIND:node :: node rmask_2 = bits(_rmask_T_2, 2, 2)
[26] FIRRTL:197299 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:335:78 KIND:node :: node rmask_3 = bits(_rmask_T_2, 3, 3)
[27] FIRRTL:197300 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:336:14 KIND:when :: when rst :
[28] FIRRTL:197301 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:336:34 KIND:node :: node _rst_cnt_T = add(rst_cnt, UInt<1>(0h1))
[29] FIRRTL:197302 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:336:34 KIND:node :: node _rst_cnt_T_1 = tail(_rst_cnt_T, 1)
[30] FIRRTL:197303 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:336:24 KIND:connect :: connect rst_cnt, _rst_cnt_T_1
[31] FIRRTL:197304 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:339:30 KIND:memory :: smem tag_array : UInt<22>[4] [64]
[32] FIRRTL:197305 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:340:17 KIND:node :: node wen = or(rst, io.write.valid)
[33] FIRRTL:197306 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:341:14 KIND:when :: when wen :
[34] FIRRTL:197307 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:47 KIND:wire :: wire _WIRE : UInt<22>[4]
[35] FIRRTL:197308 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:47 KIND:connect :: connect _WIRE[0], wdata
[36] FIRRTL:197309 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:47 KIND:connect :: connect _WIRE[1], wdata
[37] FIRRTL:197310 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:47 KIND:connect :: connect _WIRE[2], wdata
[38] FIRRTL:197311 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:47 KIND:connect :: connect _WIRE[3], wdata
[39] FIRRTL:197312 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:node :: node _T = bits(waddr, 5, 0)
[40] FIRRTL:197313 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:write_mport :: write mport MPORT = tag_array[_T], clock
[41] FIRRTL:197314 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:when :: when wmask_0 :
[42] FIRRTL:197315 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:connect :: connect MPORT[0], _WIRE[0]
[43] FIRRTL:197316 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:when :: when wmask_1 :
[44] FIRRTL:197317 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:connect :: connect MPORT[1], _WIRE[1]
[45] FIRRTL:197318 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:when :: when wmask_2 :
[46] FIRRTL:197319 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:connect :: connect MPORT[2], _WIRE[2]
[47] FIRRTL:197320 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:when :: when wmask_3 :
[48] FIRRTL:197321 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:342:20 KIND:connect :: connect MPORT[3], _WIRE[3]
[49] FIRRTL:197322 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_1 = and(io.read.ready, io.read.valid)
[50] FIRRTL:197323 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:28 KIND:wire :: wire _WIRE_1 : UInt<6>
[51] FIRRTL:197324 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:28 KIND:invalidate :: invalidate _WIRE_1
[52] FIRRTL:197325 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:28 KIND:when :: when _T_1 :
[53] FIRRTL:197326 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:28 KIND:connect :: connect _WIRE_1, io.read.bits.idx
[54] FIRRTL:197327 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:28 KIND:read_mport :: read mport MPORT_1 = tag_array[_WIRE_1], clock
[55] FIRRTL:197328 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_2 : { coh : { state : UInt<2>}, tag : UInt<20>}
[56] FIRRTL:197329 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_3 : UInt<22>
[57] FIRRTL:197330 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_3, MPORT_1[0]
[58] FIRRTL:197331 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_2 = bits(_WIRE_3, 19, 0)
[59] FIRRTL:197332 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_2.tag, _T_2
[60] FIRRTL:197333 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_3 = bits(_WIRE_3, 21, 20)
[61] FIRRTL:197334 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_2.coh.state, _T_3
[62] FIRRTL:197335 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_4 : { coh : { state : UInt<2>}, tag : UInt<20>}
[63] FIRRTL:197336 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_5 : UInt<22>
[64] FIRRTL:197337 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_5, MPORT_1[1]
[65] FIRRTL:197338 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_4 = bits(_WIRE_5, 19, 0)
[66] FIRRTL:197339 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_4.tag, _T_4
[67] FIRRTL:197340 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_5 = bits(_WIRE_5, 21, 20)
[68] FIRRTL:197341 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_4.coh.state, _T_5
[69] FIRRTL:197342 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_6 : { coh : { state : UInt<2>}, tag : UInt<20>}
[70] FIRRTL:197343 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_7 : UInt<22>
[71] FIRRTL:197344 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_7, MPORT_1[2]
[72] FIRRTL:197345 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_6 = bits(_WIRE_7, 19, 0)
[73] FIRRTL:197346 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_6.tag, _T_6
[74] FIRRTL:197347 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_7 = bits(_WIRE_7, 21, 20)
[75] FIRRTL:197348 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_6.coh.state, _T_7
[76] FIRRTL:197349 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_8 : { coh : { state : UInt<2>}, tag : UInt<20>}
[77] FIRRTL:197350 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:wire :: wire _WIRE_9 : UInt<22>
[78] FIRRTL:197351 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_9, MPORT_1[3]
[79] FIRRTL:197352 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_8 = bits(_WIRE_9, 19, 0)
[80] FIRRTL:197353 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_8.tag, _T_8
[81] FIRRTL:197354 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:node :: node _T_9 = bits(_WIRE_9, 21, 20)
[82] FIRRTL:197355 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:75 KIND:connect :: connect _WIRE_8.coh.state, _T_9
[83] FIRRTL:197356 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:11 KIND:connect :: connect io.resp[0], _WIRE_2
[84] FIRRTL:197357 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:11 KIND:connect :: connect io.resp[1], _WIRE_4
[85] FIRRTL:197358 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:11 KIND:connect :: connect io.resp[2], _WIRE_6
[86] FIRRTL:197359 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:344:11 KIND:connect :: connect io.resp[3], _WIRE_8
[87] FIRRTL:197360 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:346:20 KIND:node :: node _io_read_ready_T = eq(wen, UInt<1>(0h0))
[88] FIRRTL:197361 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:346:17 KIND:connect :: connect io.read.ready, _io_read_ready_T
[89] FIRRTL:197362 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:347:21 KIND:node :: node _io_write_ready_T = eq(rst, UInt<1>(0h0))
[90] FIRRTL:197363 SRC:generators/rocket-chip/src/main/scala/rocket/HellaCache.scala:347:18 KIND:connect :: connect io.write.ready, _io_write_ready_T
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.meta_0-3447dc7fee3a0199",
  "work_unit_id": "BoomNonBlockingDCache.meta_0",
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
