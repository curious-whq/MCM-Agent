# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment: the µMCM language is intentionally
experimental and may be revised after discussion. Your job is to derive a
candidate abstraction that preserves information potentially relevant to
microarchitectural memory ordering, not to summarize the module in prose.

Task ID: `leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.5`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomWritebackUnit`
- module: `BoomWritebackUnit`
- kind: `module`
- instance path: `BoomWritebackUnit`
- leaf: `True`
- coverage complete: `True`
- raw statements: 194
- logical statements: 131
- mapped/logical source lines: 107
- registers: 10
- physical boundary events: 6

## Non-negotiable grounding rules

1. Distinguish occurrences from persistent predicates. A boundary occurrence
   must reference one or more physical event IDs listed below. A derived
   occurrence may have no physical event ID only when it has an exact RTL
   definition, concrete grounding, and statement evidence. If one semantic
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
   finite indexed occurrence sets. Existing relation axioms may additionally use
   `scope_index: {name: <index>, relation: same}` to state that the relation is
   pointwise over the same finite index (beat/entry/bank/etc.). Formal expressions
   may use `index_var` and `lookup` to refer to the bound index and an indexed
   storage element. These constructs are protocol-agnostic and must not be
   specialized to a particular module. If the required concept still cannot be
   expressed, put it in `extensions` or `unresolved` instead of approximating it.
9. This stage proposes **candidate** axioms. Do not assert that formal validation
   has already proved them.

## Physical boundary events

- `BoomWritebackUnit::io.data_req.fire`
  - predicate: `io.data_req.valid && io.data_req.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.data_req.bits.addr', 'io.data_req.bits.way_en']
  - immediate registers: ['data_req_cnt', 'state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state']
- `BoomWritebackUnit::io.idx.valid`
  - predicate: `io.idx.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.idx.bits']
  - immediate registers: ['state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state']
- `BoomWritebackUnit::io.lsu_release.fire`
  - predicate: `io.lsu_release.valid && io.lsu_release.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.lsu_release.bits.address', 'io.lsu_release.bits.corrupt', 'io.lsu_release.bits.data', 'io.lsu_release.bits.opcode', 'io.lsu_release.bits.param', 'io.lsu_release.bits.size', 'io.lsu_release.bits.source']
  - immediate registers: ['state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state', 'wb_buffer']
- `BoomWritebackUnit::io.meta_read.fire`
  - predicate: `io.meta_read.valid && io.meta_read.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en']
  - immediate registers: ['data_req_cnt', 'state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state']
- `BoomWritebackUnit::io.release.fire`
  - predicate: `io.release.valid && io.release.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.release.bits.address', 'io.release.bits.corrupt', 'io.release.bits.data', 'io.release.bits.opcode', 'io.release.bits.param', 'io.release.bits.size', 'io.release.bits.source']
  - immediate registers: ['data_req_cnt', 'state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state']
- `BoomWritebackUnit::io.req.fire`
  - predicate: `io.req.valid && io.req.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.req.bits.idx', 'io.req.bits.param', 'io.req.bits.source', 'io.req.bits.tag', 'io.req.bits.voluntary', 'io.req.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'req', 'state']

## Concrete local state

['acked', 'data_req_cnt', 'r1_data_req_cnt', 'r1_data_req_fired', 'r2_data_req_cnt', 'r2_data_req_fired', 'r_counter', 'req', 'state', 'wb_buffer']

## Environment/frontier signals

['clock', 'io.data_req.bits.addr', 'io.data_req.bits.way_en', 'io.data_req.ready', 'io.data_req.valid', 'io.data_resp', 'io.idx.bits', 'io.idx.valid', 'io.lsu_release.bits.address', 'io.lsu_release.bits.corrupt', 'io.lsu_release.bits.data', 'io.lsu_release.bits.opcode', 'io.lsu_release.bits.param', 'io.lsu_release.bits.size', 'io.lsu_release.bits.source', 'io.lsu_release.ready', 'io.lsu_release.valid', 'io.mem_grant', 'io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en', 'io.meta_read.ready', 'io.meta_read.valid', 'io.release.bits.address', 'io.release.bits.corrupt', 'io.release.bits.data', 'io.release.bits.opcode', 'io.release.bits.param', 'io.release.bits.size', 'io.release.bits.source', 'io.release.ready', 'io.release.valid', 'io.req.ready', 'io.req.valid', 'io.resp']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:23-26
```scala

class BoomWritebackUnit(implicit edge: TLEdgeOut, p: Parameters) extends L1HellaCacheModule()(p) {
  val io = IO(new Bundle {
    val req = Flipped(Decoupled(new WritebackReq(edge.bundle)))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:36-61
```scala

  val req = Reg(new WritebackReq(edge.bundle))
  val s_invalid :: s_fill_buffer :: s_lsu_release :: s_active :: s_grant :: Nil = Enum(5)
  val state = RegInit(s_invalid)
  val r1_data_req_fired = RegInit(false.B)
  val r2_data_req_fired = RegInit(false.B)
  val r1_data_req_cnt = Reg(UInt(log2Up(refillCycles+1).W))
  val r2_data_req_cnt = Reg(UInt(log2Up(refillCycles+1).W))
  val data_req_cnt = RegInit(0.U(log2Up(refillCycles+1).W))
  val (_, last_beat, all_beats_done, beat_count) = edge.count(io.release)
  val wb_buffer = Reg(Vec(refillCycles, UInt(encRowBits.W)))
  val acked = RegInit(false.B)

  io.idx.valid       := state =/= s_invalid
  io.idx.bits        := req.idx
  io.release.valid   := false.B
  io.release.bits    := DontCare
  io.req.ready       := false.B
  io.meta_read.valid := false.B
  io.meta_read.bits  := DontCare
  io.data_req.valid  := false.B
  io.data_req.bits   := DontCare
  io.resp            := false.B
  io.lsu_release.valid := false.B
  io.lsu_release.bits := DontCare
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:62-64
```scala

  val r_address = Cat(req.tag, req.idx) << blockOffBits
  val id = cfg.nMSHRs
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:79-114
```scala

  when (state === s_invalid) {
    io.req.ready := true.B
    when (io.req.fire) {
      state := s_fill_buffer
      data_req_cnt := 0.U
      req := io.req.bits
      acked := false.B
    }
  } .elsewhen (state === s_fill_buffer) {
    io.meta_read.valid := data_req_cnt < refillCycles.U
    io.meta_read.bits.idx := req.idx
    io.meta_read.bits.tag := req.tag

    io.data_req.valid := data_req_cnt < refillCycles.U
    io.data_req.bits.way_en := req.way_en
    io.data_req.bits.addr := (if(refillCycles > 1)
                              Cat(req.idx, data_req_cnt(log2Up(refillCycles)-1,0))
                            else req.idx) << rowOffBits

    r1_data_req_fired := false.B
    r1_data_req_cnt   := 0.U
    r2_data_req_fired := r1_data_req_fired
    r2_data_req_cnt   := r1_data_req_cnt
    when (io.data_req.fire && io.meta_read.fire) {
      r1_data_req_fired := true.B
      r1_data_req_cnt   := data_req_cnt
      data_req_cnt := data_req_cnt + 1.U
    }
    when (r2_data_req_fired) {
      wb_buffer(r2_data_req_cnt) := io.data_resp
      when (r2_data_req_cnt === (refillCycles-1).U) {
        io.resp := true.B
        state := s_lsu_release
        data_req_cnt := 0.U
      }
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:115-141
```scala
    }
  } .elsewhen (state === s_lsu_release) {
    io.lsu_release.valid := true.B
    io.lsu_release.bits := probeResponse
    when (io.lsu_release.fire) {
     state := s_active
    }
  } .elsewhen (state === s_active) {
    io.release.valid := data_req_cnt < refillCycles.U
    io.release.bits := Mux(req.voluntary, voluntaryRelease, probeResponse)

    when (io.mem_grant) {
      acked := true.B
    }
    when (io.release.fire) {
      data_req_cnt := data_req_cnt + 1.U
    }
    when ((data_req_cnt === (refillCycles-1).U) && io.release.fire) {
      state := Mux(req.voluntary, s_grant, s_invalid)
    }
  } .elsewhen (state === s_grant) {
    when (io.mem_grant) {
      acked := true.B
    }
    when (acked) {
      state := s_invalid
    }
```

### generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:92-94
```scala
    if (none) false.B
    else if (min == max) { log2Ceil(min).U === x }
    else { log2Ceil(min).U <= x && x <= log2Ceil(max).U }
```

### generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:138-140
```scala
  def contains(x: BigInt) = ((x ^ base) & ~mask) == 0
  def contains(x: UInt) = ((x ^ base.U).zext & (~mask).S) === 0.S
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:101-103
```scala
        //    opcode === TLMessages.LogicalData
      case c: TLBundleC => c.opcode(0)
        //    opcode === TLMessages.AccessAckData ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:219-222
```scala
        } else {
          val decode = UIntToOH1(size(bundle), maxLgSize) >> log2Ceil(manager.beatBytes)
          Mux(hasData(bundle), decode, 0.U)
        }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:228-237
```scala
    val beats1   = numBeats1(bits)
    val counter  = RegInit(0.U(log2Up(maxTransfer / manager.beatBytes).W))
    val counter1 = counter - 1.U
    val first = counter === 0.U
    val last  = counter === 1.U || beats1 === 0.U
    val done  = last && fire
    val count = (beats1 & ~counter1)
    when (fire) {
      counter := Mux(first, beats1, counter1)
    }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:395-402
```scala
    val legal = manager.supportsAcquireBFast(toAddress, lgSize)
    val c = Wire(new TLBundleC(bundle))
    c.opcode  := TLMessages.ReleaseData
    c.param   := shrinkPermissions
    c.size    := lgSize
    c.source  := fromSource
    c.address := toAddress
    c.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:403-406
```scala
    c.echo    := DontCare
    c.data    := data
    c.corrupt := corrupt
    (legal, c)
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:432-439
```scala
  def ProbeAck(fromSource: UInt, toAddress: UInt, lgSize: UInt, reportPermissions: UInt, data: UInt, corrupt: Bool): TLBundleC = {
    val c = Wire(new TLBundleC(bundle))
    c.opcode  := TLMessages.ProbeAckData
    c.param   := reportPermissions
    c.size    := lgSize
    c.source  := fromSource
    c.address := toAddress
    c.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:440-443
```scala
    c.echo    := DontCare
    c.data    := data
    c.corrupt := corrupt
    c
```

### generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:683-687
```scala
    // We return an or-reduction of all the cases, checking whether any contains both the dynamic size and dynamic address on the wire.
      ((Some(s) == range).B || s.containsLg(lgSize)) &&
      a.map(_.contains(address)).reduce(_||_)
    }.foldLeft(false.B)(_||_)
  }
```

### generators/rocket-chip/src/main/scala/util/package.scala:243-245
```scala
  def OH1ToUInt(x: UInt): UInt = OHToUInt(OH1ToOH(x))
  def UIntToOH1(x: UInt, width: Int): UInt = ~((-1).S(width.W).asUInt << x)(width-1, 0)
  def UIntToOH1(x: UInt): UInt = UIntToOH1(x, (1 << x.getWidth) - 1)
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:187938 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:24:7 KIND:structural :: input clock : Clock
[1] FIRRTL:187939 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:24:7 KIND:structural :: input reset : Reset
[2] FIRRTL:187940 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:25:14 KIND:structural :: output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { tag : UInt<20>, idx : UInt<6>, source : UInt<2>, param : UInt<3>, way_en : UInt<4>, voluntary : UInt<1>}}, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}}, resp : UInt<1>, idx : { valid : UInt<1>, bits : UInt}, data_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { way_en : UInt<4>, addr : UInt<12>}}, flip data_resp : UInt<64>, flip mem_grant : UInt<1>, release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, lsu_release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}}
[3] FIRRTL:187942 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:37:16 KIND:reg :: reg req : { tag : UInt<20>, idx : UInt<6>, source : UInt<2>, param : UInt<3>, way_en : UInt<4>, voluntary : UInt<1>}, clock
[4] FIRRTL:187943 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:39:22 KIND:regreset :: regreset state : UInt<3>, clock, reset, UInt<3>(0h0)
[5] FIRRTL:187944 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:40:34 KIND:regreset :: regreset r1_data_req_fired : UInt<1>, clock, reset, UInt<1>(0h0)
[6] FIRRTL:187945 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:41:34 KIND:regreset :: regreset r2_data_req_fired : UInt<1>, clock, reset, UInt<1>(0h0)
[7] FIRRTL:187946 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:42:28 KIND:reg :: reg r1_data_req_cnt : UInt<4>, clock
[8] FIRRTL:187947 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:43:28 KIND:reg :: reg r2_data_req_cnt : UInt<4>, clock
[9] FIRRTL:187948 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:44:29 KIND:regreset :: regreset data_req_cnt : UInt<4>, clock, reset, UInt<4>(0h0)
[10] FIRRTL:187949 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T = and(io.release.ready, io.release.valid)
[11] FIRRTL:187950 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _r_beats1_decode_T = dshl(UInt<12>(0hfff), io.release.bits.size)
[12] FIRRTL:187951 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _r_beats1_decode_T_1 = bits(_r_beats1_decode_T, 11, 0)
[13] FIRRTL:187952 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _r_beats1_decode_T_2 = not(_r_beats1_decode_T_1)
[14] FIRRTL:187953 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node r_beats1_decode = shr(_r_beats1_decode_T_2, 3)
[15] FIRRTL:187954 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:102:36 KIND:node :: node r_beats1_opdata = bits(io.release.bits.opcode, 0, 0)
[16] FIRRTL:187955 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node r_beats1 = mux(r_beats1_opdata, r_beats1_decode, UInt<1>(0h0))
[17] FIRRTL:187956 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:229:27 KIND:regreset :: regreset r_counter : UInt<9>, clock, reset, UInt<9>(0h0)
[18] FIRRTL:187957 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node _r_counter1_T = sub(r_counter, UInt<1>(0h1))
[19] FIRRTL:187958 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:230:28 KIND:node :: node r_counter1 = tail(_r_counter1_T, 1)
[20] FIRRTL:187959 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:231:25 KIND:node :: node r_1 = eq(r_counter, UInt<1>(0h0))
[21] FIRRTL:187960 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:25 KIND:node :: node _r_last_T = eq(r_counter, UInt<1>(0h1))
[22] FIRRTL:187961 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:43 KIND:node :: node _r_last_T_1 = eq(r_beats1, UInt<1>(0h0))
[23] FIRRTL:187962 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:232:33 KIND:node :: node last_beat = or(_r_last_T, _r_last_T_1)
[24] FIRRTL:187963 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:233:22 KIND:node :: node all_beats_done = and(last_beat, _T)
[25] FIRRTL:187964 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:27 KIND:node :: node _r_count_T = not(r_counter1)
[26] FIRRTL:187965 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:234:25 KIND:node :: node beat_count = and(r_beats1, _r_count_T)
[27] FIRRTL:187966 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:235:17 KIND:when :: when _T :
[28] FIRRTL:187967 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:21 KIND:node :: node _r_counter_T = mux(r_1, r_beats1, r_counter1)
[29] FIRRTL:187968 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:236:15 KIND:connect :: connect r_counter, _r_counter_T
[30] FIRRTL:187969 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:46:22 KIND:reg :: reg wb_buffer : UInt<64>[8], clock
[31] FIRRTL:187970 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:47:22 KIND:regreset :: regreset acked : UInt<1>, clock, reset, UInt<1>(0h0)
[32] FIRRTL:187971 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:49:31 KIND:node :: node _io_idx_valid_T = neq(state, UInt<3>(0h0))
[33] FIRRTL:187972 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:49:22 KIND:connect :: connect io.idx.valid, _io_idx_valid_T
[34] FIRRTL:187973 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:50:22 KIND:connect :: connect io.idx.bits, req.idx
[35] FIRRTL:187974 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:51:22 KIND:connect :: connect io.release.valid, UInt<1>(0h0)
[36] FIRRTL:187975 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.corrupt
[37] FIRRTL:187976 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.data
[38] FIRRTL:187977 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.address
[39] FIRRTL:187978 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.source
[40] FIRRTL:187979 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.size
[41] FIRRTL:187980 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.param
[42] FIRRTL:187981 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:52:22 KIND:invalidate :: invalidate io.release.bits.opcode
[43] FIRRTL:187982 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:53:22 KIND:connect :: connect io.req.ready, UInt<1>(0h0)
[44] FIRRTL:187983 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:54:22 KIND:connect :: connect io.meta_read.valid, UInt<1>(0h0)
[45] FIRRTL:187984 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:55:22 KIND:invalidate :: invalidate io.meta_read.bits.tag
[46] FIRRTL:187985 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:55:22 KIND:invalidate :: invalidate io.meta_read.bits.way_en
[47] FIRRTL:187986 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:55:22 KIND:invalidate :: invalidate io.meta_read.bits.idx
[48] FIRRTL:187987 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:56:22 KIND:connect :: connect io.data_req.valid, UInt<1>(0h0)
[49] FIRRTL:187988 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:57:22 KIND:invalidate :: invalidate io.data_req.bits.addr
[50] FIRRTL:187989 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:57:22 KIND:invalidate :: invalidate io.data_req.bits.way_en
[51] FIRRTL:187990 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:58:22 KIND:connect :: connect io.resp, UInt<1>(0h0)
[52] FIRRTL:187991 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:59:24 KIND:connect :: connect io.lsu_release.valid, UInt<1>(0h0)
[53] FIRRTL:187992 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.corrupt
[54] FIRRTL:187993 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.data
[55] FIRRTL:187994 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.address
[56] FIRRTL:187995 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.source
[57] FIRRTL:187996 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.size
[58] FIRRTL:187997 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.param
[59] FIRRTL:187998 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:60:23 KIND:invalidate :: invalidate io.lsu_release.bits.opcode
[60] FIRRTL:187999 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:63:22 KIND:node :: node _r_address_T = cat(req.tag, req.idx)
[61] FIRRTL:188000 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:63:41 KIND:node :: node r_address = shl(_r_address_T, 6)
[62] FIRRTL:188001 SRC:<no-source-locator> KIND:node :: node _probeResponse_T = bits(data_req_cnt, 2, 0)
[63] FIRRTL:188002 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:433:17 KIND:wire :: wire probeResponse : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}
[64] FIRRTL:188003 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:434:15 KIND:connect :: connect probeResponse.opcode, UInt<3>(0h5)
[65] FIRRTL:188004 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:435:15 KIND:connect :: connect probeResponse.param, req.param
[66] FIRRTL:188005 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:436:15 KIND:connect :: connect probeResponse.size, UInt<3>(0h6)
[67] FIRRTL:188006 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:437:15 KIND:connect :: connect probeResponse.source, req.source
[68] FIRRTL:188007 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:438:15 KIND:connect :: connect probeResponse.address, r_address
[69] FIRRTL:188008 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:441:15 KIND:connect :: connect probeResponse.data, wb_buffer[_probeResponse_T]
[70] FIRRTL:188009 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:442:15 KIND:connect :: connect probeResponse.corrupt, UInt<1>(0h0)
[71] FIRRTL:188010 SRC:<no-source-locator> KIND:node :: node _voluntaryRelease_T = bits(data_req_cnt, 2, 0)
[72] FIRRTL:188011 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _voluntaryRelease_legal_T = or(UInt<1>(0h0), UInt<1>(0h0))
[73] FIRRTL:188012 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _voluntaryRelease_legal_T_1 = xor(r_address, UInt<1>(0h0))
[74] FIRRTL:188013 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _voluntaryRelease_legal_T_2 = cvt(_voluntaryRelease_legal_T_1)
[75] FIRRTL:188014 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_3 = and(_voluntaryRelease_legal_T_2, asSInt(UInt<33>(0h8c000000)))
[76] FIRRTL:188015 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_4 = asSInt(_voluntaryRelease_legal_T_3)
[77] FIRRTL:188016 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _voluntaryRelease_legal_T_5 = eq(_voluntaryRelease_legal_T_4, asSInt(UInt<1>(0h0)))
[78] FIRRTL:188017 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _voluntaryRelease_legal_T_6 = xor(r_address, UInt<17>(0h10000))
[79] FIRRTL:188018 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _voluntaryRelease_legal_T_7 = cvt(_voluntaryRelease_legal_T_6)
[80] FIRRTL:188019 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_8 = and(_voluntaryRelease_legal_T_7, asSInt(UInt<33>(0h8c011000)))
[81] FIRRTL:188020 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_9 = asSInt(_voluntaryRelease_legal_T_8)
[82] FIRRTL:188021 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _voluntaryRelease_legal_T_10 = eq(_voluntaryRelease_legal_T_9, asSInt(UInt<1>(0h0)))
[83] FIRRTL:188022 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _voluntaryRelease_legal_T_11 = xor(r_address, UInt<28>(0hc000000))
[84] FIRRTL:188023 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _voluntaryRelease_legal_T_12 = cvt(_voluntaryRelease_legal_T_11)
[85] FIRRTL:188024 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_13 = and(_voluntaryRelease_legal_T_12, asSInt(UInt<33>(0h8c000000)))
[86] FIRRTL:188025 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_14 = asSInt(_voluntaryRelease_legal_T_13)
[87] FIRRTL:188026 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _voluntaryRelease_legal_T_15 = eq(_voluntaryRelease_legal_T_14, asSInt(UInt<1>(0h0)))
[88] FIRRTL:188027 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _voluntaryRelease_legal_T_16 = or(_voluntaryRelease_legal_T_5, _voluntaryRelease_legal_T_10)
[89] FIRRTL:188028 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _voluntaryRelease_legal_T_17 = or(_voluntaryRelease_legal_T_16, _voluntaryRelease_legal_T_15)
[90] FIRRTL:188029 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _voluntaryRelease_legal_T_18 = and(_voluntaryRelease_legal_T, _voluntaryRelease_legal_T_17)
[91] FIRRTL:188030 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:93:44 KIND:node :: node _voluntaryRelease_legal_T_19 = eq(UInt<3>(0h6), UInt<3>(0h6))
[92] FIRRTL:188031 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:29 KIND:node :: node _voluntaryRelease_legal_T_20 = or(UInt<1>(0h0), _voluntaryRelease_legal_T_19)
[93] FIRRTL:188032 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _voluntaryRelease_legal_T_21 = xor(r_address, UInt<28>(0h8000000))
[94] FIRRTL:188033 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _voluntaryRelease_legal_T_22 = cvt(_voluntaryRelease_legal_T_21)
[95] FIRRTL:188034 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_23 = and(_voluntaryRelease_legal_T_22, asSInt(UInt<33>(0h8c010000)))
[96] FIRRTL:188035 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_24 = asSInt(_voluntaryRelease_legal_T_23)
[97] FIRRTL:188036 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _voluntaryRelease_legal_T_25 = eq(_voluntaryRelease_legal_T_24, asSInt(UInt<1>(0h0)))
[98] FIRRTL:188037 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:31 KIND:node :: node _voluntaryRelease_legal_T_26 = xor(r_address, UInt<32>(0h80000000))
[99] FIRRTL:188038 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:41 KIND:node :: node _voluntaryRelease_legal_T_27 = cvt(_voluntaryRelease_legal_T_26)
[100] FIRRTL:188039 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_28 = and(_voluntaryRelease_legal_T_27, asSInt(UInt<33>(0h80000000)))
[101] FIRRTL:188040 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:46 KIND:node :: node _voluntaryRelease_legal_T_29 = asSInt(_voluntaryRelease_legal_T_28)
[102] FIRRTL:188041 SRC:generators/rocket-chip/src/main/scala/diplomacy/Parameters.scala:139:59 KIND:node :: node _voluntaryRelease_legal_T_30 = eq(_voluntaryRelease_legal_T_29, asSInt(UInt<1>(0h0)))
[103] FIRRTL:188042 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:685:42 KIND:node :: node _voluntaryRelease_legal_T_31 = or(_voluntaryRelease_legal_T_25, _voluntaryRelease_legal_T_30)
[104] FIRRTL:188043 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:684:54 KIND:node :: node _voluntaryRelease_legal_T_32 = and(_voluntaryRelease_legal_T_20, _voluntaryRelease_legal_T_31)
[105] FIRRTL:188044 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node _voluntaryRelease_legal_T_33 = or(UInt<1>(0h0), _voluntaryRelease_legal_T_18)
[106] FIRRTL:188045 SRC:generators/rocket-chip/src/main/scala/tilelink/Parameters.scala:686:26 KIND:node :: node voluntaryRelease_legal = or(_voluntaryRelease_legal_T_33, _voluntaryRelease_legal_T_32)
[107] FIRRTL:188046 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:396:17 KIND:wire :: wire voluntaryRelease : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}
[108] FIRRTL:188047 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:397:15 KIND:connect :: connect voluntaryRelease.opcode, UInt<3>(0h7)
[109] FIRRTL:188048 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:398:15 KIND:connect :: connect voluntaryRelease.param, req.param
[110] FIRRTL:188049 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:399:15 KIND:connect :: connect voluntaryRelease.size, UInt<3>(0h6)
[111] FIRRTL:188050 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:400:15 KIND:connect :: connect voluntaryRelease.source, UInt<2>(0h2)
[112] FIRRTL:188051 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:401:15 KIND:connect :: connect voluntaryRelease.address, r_address
[113] FIRRTL:188052 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:404:15 KIND:connect :: connect voluntaryRelease.data, wb_buffer[_voluntaryRelease_T]
[114] FIRRTL:188053 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:405:15 KIND:connect :: connect voluntaryRelease.corrupt, UInt<1>(0h0)
[115] FIRRTL:188054 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:80:15 KIND:node :: node _T_1 = eq(state, UInt<3>(0h0))
[116] FIRRTL:188055 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:80:30 KIND:when :: when _T_1 :
[117] FIRRTL:188056 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:81:18 KIND:connect :: connect io.req.ready, UInt<1>(0h1)
[118] FIRRTL:188057 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_2 = and(io.req.ready, io.req.valid)
[119] FIRRTL:188058 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:82:24 KIND:when :: when _T_2 :
[120] FIRRTL:188059 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:83:13 KIND:connect :: connect state, UInt<3>(0h1)
[121] FIRRTL:188060 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:84:20 KIND:connect :: connect data_req_cnt, UInt<1>(0h0)
[122] FIRRTL:188061 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:85:11 KIND:connect :: connect req, io.req.bits
[123] FIRRTL:188062 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:86:13 KIND:connect :: connect acked, UInt<1>(0h0)
[124] FIRRTL:188063 SRC:<no-source-locator> KIND:else :: else :
[125] FIRRTL:188064 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:88:22 KIND:node :: node _T_3 = eq(state, UInt<3>(0h1))
[126] FIRRTL:188065 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:88:41 KIND:when :: when _T_3 :
[127] FIRRTL:188066 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:89:40 KIND:node :: node _io_meta_read_valid_T = lt(data_req_cnt, UInt<4>(0h8))
[128] FIRRTL:188067 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:89:24 KIND:connect :: connect io.meta_read.valid, _io_meta_read_valid_T
[129] FIRRTL:188068 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:90:27 KIND:connect :: connect io.meta_read.bits.idx, req.idx
[130] FIRRTL:188069 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:91:27 KIND:connect :: connect io.meta_read.bits.tag, req.tag
[131] FIRRTL:188070 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:93:39 KIND:node :: node _io_data_req_valid_T = lt(data_req_cnt, UInt<4>(0h8))
[132] FIRRTL:188071 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:93:23 KIND:connect :: connect io.data_req.valid, _io_data_req_valid_T
[133] FIRRTL:188072 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:94:29 KIND:connect :: connect io.data_req.bits.way_en, req.way_en
[134] FIRRTL:188073 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:96:56 KIND:node :: node _io_data_req_bits_addr_T = bits(data_req_cnt, 2, 0)
[135] FIRRTL:188074 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:96:34 KIND:node :: node _io_data_req_bits_addr_T_1 = cat(req.idx, _io_data_req_bits_addr_T)
[136] FIRRTL:188075 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:97:43 KIND:node :: node _io_data_req_bits_addr_T_2 = shl(_io_data_req_bits_addr_T_1, 3)
[137] FIRRTL:188076 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:95:27 KIND:connect :: connect io.data_req.bits.addr, _io_data_req_bits_addr_T_2
[138] FIRRTL:188077 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:99:23 KIND:connect :: connect r1_data_req_fired, UInt<1>(0h0)
[139] FIRRTL:188078 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:100:23 KIND:connect :: connect r1_data_req_cnt, UInt<1>(0h0)
[140] FIRRTL:188079 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:101:23 KIND:connect :: connect r2_data_req_fired, r1_data_req_fired
[141] FIRRTL:188080 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:102:23 KIND:connect :: connect r2_data_req_cnt, r1_data_req_cnt
[142] FIRRTL:188081 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_4 = and(io.data_req.ready, io.data_req.valid)
[143] FIRRTL:188082 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_5 = and(io.meta_read.ready, io.meta_read.valid)
[144] FIRRTL:188083 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:103:28 KIND:node :: node _T_6 = and(_T_4, _T_5)
[145] FIRRTL:188084 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:103:50 KIND:when :: when _T_6 :
[146] FIRRTL:188085 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:104:25 KIND:connect :: connect r1_data_req_fired, UInt<1>(0h1)
[147] FIRRTL:188086 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:105:25 KIND:connect :: connect r1_data_req_cnt, data_req_cnt
[148] FIRRTL:188087 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:106:36 KIND:node :: node _data_req_cnt_T = add(data_req_cnt, UInt<1>(0h1))
[149] FIRRTL:188088 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:106:36 KIND:node :: node _data_req_cnt_T_1 = tail(_data_req_cnt_T, 1)
[150] FIRRTL:188089 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:106:20 KIND:connect :: connect data_req_cnt, _data_req_cnt_T_1
[151] FIRRTL:188090 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:108:30 KIND:when :: when r2_data_req_fired :
[152] FIRRTL:188091 SRC:<no-source-locator> KIND:node :: node _T_7 = bits(r2_data_req_cnt, 2, 0)
[153] FIRRTL:188092 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:109:34 KIND:connect :: connect wb_buffer[_T_7], io.data_resp
[154] FIRRTL:188093 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:110:29 KIND:node :: node _T_8 = eq(r2_data_req_cnt, UInt<3>(0h7))
[155] FIRRTL:188094 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:110:53 KIND:when :: when _T_8 :
[156] FIRRTL:188095 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:111:17 KIND:connect :: connect io.resp, UInt<1>(0h1)
[157] FIRRTL:188096 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:112:15 KIND:connect :: connect state, UInt<3>(0h2)
[158] FIRRTL:188097 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:113:22 KIND:connect :: connect data_req_cnt, UInt<1>(0h0)
[159] FIRRTL:188098 SRC:<no-source-locator> KIND:else :: else :
[160] FIRRTL:188099 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:116:22 KIND:node :: node _T_9 = eq(state, UInt<3>(0h2))
[161] FIRRTL:188100 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:116:41 KIND:when :: when _T_9 :
[162] FIRRTL:188101 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:117:26 KIND:connect :: connect io.lsu_release.valid, UInt<1>(0h1)
[163] FIRRTL:188102 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:118:25 KIND:connect :: connect io.lsu_release.bits, probeResponse
[164] FIRRTL:188103 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_10 = and(io.lsu_release.ready, io.lsu_release.valid)
[165] FIRRTL:188104 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:119:32 KIND:when :: when _T_10 :
[166] FIRRTL:188105 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:120:12 KIND:connect :: connect state, UInt<3>(0h3)
[167] FIRRTL:188106 SRC:<no-source-locator> KIND:else :: else :
[168] FIRRTL:188107 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:122:22 KIND:node :: node _T_11 = eq(state, UInt<3>(0h3))
[169] FIRRTL:188108 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:122:36 KIND:when :: when _T_11 :
[170] FIRRTL:188109 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:123:38 KIND:node :: node _io_release_valid_T = lt(data_req_cnt, UInt<4>(0h8))
[171] FIRRTL:188110 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:123:22 KIND:connect :: connect io.release.valid, _io_release_valid_T
[172] FIRRTL:188111 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:124:27 KIND:node :: node _io_release_bits_T = mux(req.voluntary, voluntaryRelease, probeResponse)
[173] FIRRTL:188112 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:124:21 KIND:connect :: connect io.release.bits, _io_release_bits_T
[174] FIRRTL:188113 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:126:25 KIND:when :: when io.mem_grant :
[175] FIRRTL:188114 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:127:13 KIND:connect :: connect acked, UInt<1>(0h1)
[176] FIRRTL:188115 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_12 = and(io.release.ready, io.release.valid)
[177] FIRRTL:188116 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:129:28 KIND:when :: when _T_12 :
[178] FIRRTL:188117 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:130:36 KIND:node :: node _data_req_cnt_T_2 = add(data_req_cnt, UInt<1>(0h1))
[179] FIRRTL:188118 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:130:36 KIND:node :: node _data_req_cnt_T_3 = tail(_data_req_cnt_T_2, 1)
[180] FIRRTL:188119 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:130:20 KIND:connect :: connect data_req_cnt, _data_req_cnt_T_3
[181] FIRRTL:188120 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:132:25 KIND:node :: node _T_13 = eq(data_req_cnt, UInt<3>(0h7))
[182] FIRRTL:188121 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_14 = and(io.release.ready, io.release.valid)
[183] FIRRTL:188122 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:132:49 KIND:node :: node _T_15 = and(_T_13, _T_14)
[184] FIRRTL:188123 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:132:69 KIND:when :: when _T_15 :
[185] FIRRTL:188124 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:133:19 KIND:node :: node _state_T = mux(req.voluntary, UInt<3>(0h4), UInt<3>(0h0))
[186] FIRRTL:188125 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:133:13 KIND:connect :: connect state, _state_T
[187] FIRRTL:188126 SRC:<no-source-locator> KIND:else :: else :
[188] FIRRTL:188127 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:135:22 KIND:node :: node _T_16 = eq(state, UInt<3>(0h4))
[189] FIRRTL:188128 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:135:35 KIND:when :: when _T_16 :
[190] FIRRTL:188129 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:136:25 KIND:when :: when io.mem_grant :
[191] FIRRTL:188130 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:137:13 KIND:connect :: connect acked, UInt<1>(0h1)
[192] FIRRTL:188131 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:139:18 KIND:when :: when acked :
[193] FIRRTL:188132 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:140:13 KIND:connect :: connect state, UInt<3>(0h0)
```

## What to do in the conversation

First reason about the WorkUnit and propose whatever semantic decomposition is
most useful. We may discuss, challenge, and revise it interactively. The current
v0.2 µMCM idea (occurrences, persistent predicates, identity, guarded cases,
axioms, assumptions) is a working hypothesis, not a sacred final design.

Focus on questions such as:

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

Only when the discussion has converged, emit a final section named
`FINAL MCM-AGENT RESULT` followed by one fenced JSON object. The object must
match `expected_output_schema.json`. Use this exact envelope as the starting
shape:

```json
{
  "schema_version": "umcm-formal-0.5",
  "task_id": "leaf_abstraction-BoomWritebackUnit-5966d4c9d61e033b",
  "work_unit_id": "BoomWritebackUnit",
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
