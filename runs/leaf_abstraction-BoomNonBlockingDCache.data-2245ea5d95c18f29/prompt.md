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

Task ID: `leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache.data`
- module: `BoomDuplicatedDataArray`
- kind: `module`
- instance path: `BoomNonBlockingDCache.data`
- leaf: `True`
- coverage complete: `True`
- raw statements: 82
- logical statements: 21
- mapped/logical source lines: 10
- registers: 4
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

- `BoomNonBlockingDCache.data::io.read[0].valid`
  - predicate: `io.read[0].valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.read[0].bits.addr', 'io.read[0].bits.way_en']
  - immediate registers: []
  - historical registers: []
- `BoomNonBlockingDCache.data::io.write.valid`
  - predicate: `io.write.valid`
  - direction/protocol: `receive` / `valid`
  - payload leaves: ['io.write.bits.addr', 'io.write.bits.data', 'io.write.bits.way_en', 'io.write.bits.wmask']
  - immediate registers: []
  - historical registers: []

## Concrete local state

['io_resp_0_0_REG', 'io_resp_0_1_REG', 'io_resp_0_2_REG', 'io_resp_0_3_REG']

## Environment/frontier signals

['clock', 'io.read[0].bits.addr', 'io.read[0].valid', 'io.resp[0][0]', 'io.resp[0][1]', 'io.resp[0][2]', 'io.resp[0][3]', 'io.s1_nacks[0]', 'io.write.bits.addr', 'io.write.bits.data', 'io.write.bits.way_en', 'io.write.bits.wmask', 'io.write.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:269-271
```scala
abstract class AbstractBoomDataArray(implicit p: Parameters) extends BoomModule with HasL1HellaCacheParameters {
  val io = IO(new BoomBundle {
    val read  = Input(Vec(lsuWidth, Valid(new L1DataReadReq)))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:280-282
```scala

class BoomDuplicatedDataArray(implicit p: Parameters) extends AbstractBoomDataArray
{
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:283-285
```scala

  val waddr = io.write.bits.addr >> rowOffBits
  for (j <- 0 until lsuWidth) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:286-288
```scala

    val raddr = io.read(j).bits.addr >> rowOffBits
    for (w <- 0 until nWays) {
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:294-298
```scala
      )
      when (io.write.bits.way_en(w) && io.write.valid) {
        val data = VecInit((0 until rowWords) map (i => io.write.bits.data(encDataBits*(i+1)-1,encDataBits*i)))
        array.write(waddr, data, io.write.bits.wmask.asBools)
      }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:301-305
```scala
      else
        io.resp(j)(w) := RegNext(array.read(raddr, io.read(j).valid).asUInt)
    }
    io.s1_nacks(j) := false.B
  }
```

### generators/rocket-chip/src/main/scala/util/DescribedSRAM.scala:16-18
```scala

    val mem = SyncReadMem(size, data)
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:197432 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:281:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197433 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:281:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197434 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:270:14 KIND:structural :: output io : { flip read : { valid : UInt<1>, bits : { way_en : UInt<4>, addr : UInt<12>}}[1], flip write : { valid : UInt<1>, bits : { way_en : UInt<4>, addr : UInt<12>, wmask : UInt<1>, data : UInt<64>}}, resp : UInt<64>[4][1], s1_nacks : UInt<1>[1]}
[3] FIRRTL:197436 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:284:34 KIND:node :: node waddr = shr(io.write.bits.addr, 3)
[4] FIRRTL:197437 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:287:38 KIND:node :: node raddr = shr(io.read[0].bits.addr, 3)
[5] FIRRTL:197438 SRC:generators/rocket-chip/src/main/scala/util/DescribedSRAM.scala:17:26 KIND:memory :: smem array_0_0 : UInt<64>[1] [512]
[6] FIRRTL:197439 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:33 KIND:node :: node _T = bits(io.write.bits.way_en, 0, 0)
[7] FIRRTL:197440 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:37 KIND:node :: node _T_1 = and(_T, io.write.valid)
[8] FIRRTL:197441 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:56 KIND:when :: when _T_1 :
[9] FIRRTL:197442 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:75 KIND:node :: node _data_T = bits(io.write.bits.data, 63, 0)
[10] FIRRTL:197443 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:wire :: wire data : UInt<64>[1]
[11] FIRRTL:197444 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:connect :: connect data[0], _data_T
[12] FIRRTL:197445 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:54 KIND:node :: node _T_2 = bits(io.write.bits.wmask, 0, 0)
[13] FIRRTL:197446 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:write_mport :: write mport MPORT = array_0_0[waddr], clock
[14] FIRRTL:197447 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:when :: when _T_2 :
[15] FIRRTL:197448 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:connect :: connect MPORT[0], data[0]
[16] FIRRTL:197449 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:wire :: wire _io_resp_0_0_WIRE : UInt<9>
[17] FIRRTL:197450 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:invalidate :: invalidate _io_resp_0_0_WIRE
[18] FIRRTL:197451 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:when :: when io.read[0].valid :
[19] FIRRTL:197452 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:connect :: connect _io_resp_0_0_WIRE, raddr
[20] FIRRTL:197453 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:read_mport :: read mport io_resp_0_0_MPORT = array_0_0[_io_resp_0_0_WIRE], clock
[21] FIRRTL:197454 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:reg :: reg io_resp_0_0_REG : UInt, clock
[22] FIRRTL:197455 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:connect :: connect io_resp_0_0_REG, io_resp_0_0_MPORT[0]
[23] FIRRTL:197456 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:23 KIND:connect :: connect io.resp[0][0], io_resp_0_0_REG
[24] FIRRTL:197457 SRC:generators/rocket-chip/src/main/scala/util/DescribedSRAM.scala:17:26 KIND:memory :: smem array_1_0 : UInt<64>[1] [512]
[25] FIRRTL:197458 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:33 KIND:node :: node _T_3 = bits(io.write.bits.way_en, 1, 1)
[26] FIRRTL:197459 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:37 KIND:node :: node _T_4 = and(_T_3, io.write.valid)
[27] FIRRTL:197460 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:56 KIND:when :: when _T_4 :
[28] FIRRTL:197461 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:75 KIND:node :: node _data_T_1 = bits(io.write.bits.data, 63, 0)
[29] FIRRTL:197462 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:wire :: wire data_1 : UInt<64>[1]
[30] FIRRTL:197463 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:connect :: connect data_1[0], _data_T_1
[31] FIRRTL:197464 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:54 KIND:node :: node _T_5 = bits(io.write.bits.wmask, 0, 0)
[32] FIRRTL:197465 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:write_mport :: write mport MPORT_1 = array_1_0[waddr], clock
[33] FIRRTL:197466 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:when :: when _T_5 :
[34] FIRRTL:197467 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:connect :: connect MPORT_1[0], data_1[0]
[35] FIRRTL:197468 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:wire :: wire _io_resp_0_1_WIRE : UInt<9>
[36] FIRRTL:197469 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:invalidate :: invalidate _io_resp_0_1_WIRE
[37] FIRRTL:197470 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:when :: when io.read[0].valid :
[38] FIRRTL:197471 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:connect :: connect _io_resp_0_1_WIRE, raddr
[39] FIRRTL:197472 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:read_mport :: read mport io_resp_0_1_MPORT = array_1_0[_io_resp_0_1_WIRE], clock
[40] FIRRTL:197473 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:reg :: reg io_resp_0_1_REG : UInt, clock
[41] FIRRTL:197474 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:connect :: connect io_resp_0_1_REG, io_resp_0_1_MPORT[0]
[42] FIRRTL:197475 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:23 KIND:connect :: connect io.resp[0][1], io_resp_0_1_REG
[43] FIRRTL:197476 SRC:generators/rocket-chip/src/main/scala/util/DescribedSRAM.scala:17:26 KIND:memory :: smem array_2_0 : UInt<64>[1] [512]
[44] FIRRTL:197477 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:33 KIND:node :: node _T_6 = bits(io.write.bits.way_en, 2, 2)
[45] FIRRTL:197478 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:37 KIND:node :: node _T_7 = and(_T_6, io.write.valid)
[46] FIRRTL:197479 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:56 KIND:when :: when _T_7 :
[47] FIRRTL:197480 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:75 KIND:node :: node _data_T_2 = bits(io.write.bits.data, 63, 0)
[48] FIRRTL:197481 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:wire :: wire data_2 : UInt<64>[1]
[49] FIRRTL:197482 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:connect :: connect data_2[0], _data_T_2
[50] FIRRTL:197483 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:54 KIND:node :: node _T_8 = bits(io.write.bits.wmask, 0, 0)
[51] FIRRTL:197484 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:write_mport :: write mport MPORT_2 = array_2_0[waddr], clock
[52] FIRRTL:197485 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:when :: when _T_8 :
[53] FIRRTL:197486 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:connect :: connect MPORT_2[0], data_2[0]
[54] FIRRTL:197487 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:wire :: wire _io_resp_0_2_WIRE : UInt<9>
[55] FIRRTL:197488 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:invalidate :: invalidate _io_resp_0_2_WIRE
[56] FIRRTL:197489 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:when :: when io.read[0].valid :
[57] FIRRTL:197490 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:connect :: connect _io_resp_0_2_WIRE, raddr
[58] FIRRTL:197491 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:read_mport :: read mport io_resp_0_2_MPORT = array_2_0[_io_resp_0_2_WIRE], clock
[59] FIRRTL:197492 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:reg :: reg io_resp_0_2_REG : UInt, clock
[60] FIRRTL:197493 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:connect :: connect io_resp_0_2_REG, io_resp_0_2_MPORT[0]
[61] FIRRTL:197494 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:23 KIND:connect :: connect io.resp[0][2], io_resp_0_2_REG
[62] FIRRTL:197495 SRC:generators/rocket-chip/src/main/scala/util/DescribedSRAM.scala:17:26 KIND:memory :: smem array_3_0 : UInt<64>[1] [512]
[63] FIRRTL:197496 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:33 KIND:node :: node _T_9 = bits(io.write.bits.way_en, 3, 3)
[64] FIRRTL:197497 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:37 KIND:node :: node _T_10 = and(_T_9, io.write.valid)
[65] FIRRTL:197498 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:295:56 KIND:when :: when _T_10 :
[66] FIRRTL:197499 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:75 KIND:node :: node _data_T_3 = bits(io.write.bits.data, 63, 0)
[67] FIRRTL:197500 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:wire :: wire data_3 : UInt<64>[1]
[68] FIRRTL:197501 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:296:27 KIND:connect :: connect data_3[0], _data_T_3
[69] FIRRTL:197502 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:54 KIND:node :: node _T_11 = bits(io.write.bits.wmask, 0, 0)
[70] FIRRTL:197503 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:write_mport :: write mport MPORT_3 = array_3_0[waddr], clock
[71] FIRRTL:197504 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:when :: when _T_11 :
[72] FIRRTL:197505 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:297:20 KIND:connect :: connect MPORT_3[0], data_3[0]
[73] FIRRTL:197506 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:wire :: wire _io_resp_0_3_WIRE : UInt<9>
[74] FIRRTL:197507 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:invalidate :: invalidate _io_resp_0_3_WIRE
[75] FIRRTL:197508 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:when :: when io.read[0].valid :
[76] FIRRTL:197509 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:connect :: connect _io_resp_0_3_WIRE, raddr
[77] FIRRTL:197510 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:44 KIND:read_mport :: read mport io_resp_0_3_MPORT = array_3_0[_io_resp_0_3_WIRE], clock
[78] FIRRTL:197511 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:reg :: reg io_resp_0_3_REG : UInt, clock
[79] FIRRTL:197512 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:33 KIND:connect :: connect io_resp_0_3_REG, io_resp_0_3_MPORT[0]
[80] FIRRTL:197513 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:302:23 KIND:connect :: connect io.resp[0][3], io_resp_0_3_REG
[81] FIRRTL:197514 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:304:20 KIND:connect :: connect io.s1_nacks[0], UInt<1>(0h0)
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.data-2245ea5d95c18f29",
  "work_unit_id": "BoomNonBlockingDCache.data",
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
