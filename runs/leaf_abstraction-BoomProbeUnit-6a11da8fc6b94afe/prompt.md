# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment: the µMCM language is intentionally
experimental and may be revised after discussion. Your job is to derive a
candidate abstraction that preserves information potentially relevant to
microarchitectural memory ordering, not to summarize the module in prose.

Task ID: `leaf_abstraction-BoomProbeUnit-6a11da8fc6b94afe`
Workflow version: `manual-first-workflow-0.7`
Prompt version: `leaf-abstraction-prompt-0.3`
Output schema version: `umcm-formal-0.3`

## WorkUnit

- id: `BoomProbeUnit`
- module: `BoomProbeUnit`
- kind: `module`
- instance path: `BoomProbeUnit`
- leaf: `True`
- coverage complete: `True`
- raw statements: 209
- logical statements: 132
- mapped/logical source lines: 97
- registers: 4
- physical boundary events: 7

## Non-negotiable grounding rules

1. Distinguish occurrences from persistent predicates. A boundary occurrence
   must reference one or more physical event IDs listed below. A derived
   occurrence may have no physical event ID only when it has an exact RTL
   definition, concrete grounding, and statement evidence. Do not turn ordinary
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
8. Use only formal axiom forms supported by the schema. If the required concept
   cannot be expressed without stretching an existing form, put it in `extensions`
   or `unresolved` instead of encoding it approximately.
9. This stage proposes **candidate** axioms. Do not assert that formal validation
   has already proved them.

## Physical boundary events

- `BoomProbeUnit::io.lsu_release.fire`
  - predicate: `io.lsu_release.valid && io.lsu_release.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.lsu_release.bits.address', 'io.lsu_release.bits.corrupt', 'io.lsu_release.bits.data', 'io.lsu_release.bits.opcode', 'io.lsu_release.bits.param', 'io.lsu_release.bits.size', 'io.lsu_release.bits.source']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.meta_read.fire`
  - predicate: `io.meta_read.valid && io.meta_read.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.meta_write.fire`
  - predicate: `io.meta_write.valid && io.meta_write.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.rep.fire`
  - predicate: `io.rep.valid && io.rep.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.rep.bits.address', 'io.rep.bits.corrupt', 'io.rep.bits.data', 'io.rep.bits.opcode', 'io.rep.bits.param', 'io.rep.bits.size', 'io.rep.bits.source']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.req.fire`
  - predicate: `io.req.valid && io.req.ready`
  - direction/protocol: `receive` / `decoupled`
  - payload leaves: ['io.req.bits.address', 'io.req.bits.corrupt', 'io.req.bits.data', 'io.req.bits.mask', 'io.req.bits.opcode', 'io.req.bits.param', 'io.req.bits.size', 'io.req.bits.source']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.state.valid`
  - predicate: `io.state.valid`
  - direction/protocol: `send` / `valid`
  - payload leaves: ['io.state.bits']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']
- `BoomProbeUnit::io.wb_req.fire`
  - predicate: `io.wb_req.valid && io.wb_req.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en']
  - immediate registers: ['state']
  - historical registers: ['req', 'state', 'way_en']

## Concrete local state

['old_coh', 'req', 'state', 'way_en']

## Environment/frontier signals

['clock', 'io.lsu_release.bits.address', 'io.lsu_release.bits.corrupt', 'io.lsu_release.bits.data', 'io.lsu_release.bits.opcode', 'io.lsu_release.bits.param', 'io.lsu_release.bits.size', 'io.lsu_release.bits.source', 'io.lsu_release.ready', 'io.lsu_release.valid', 'io.meta_read.bits.idx', 'io.meta_read.bits.tag', 'io.meta_read.bits.way_en', 'io.meta_read.ready', 'io.meta_read.valid', 'io.meta_write.bits.data.coh.state', 'io.meta_write.bits.data.tag', 'io.meta_write.bits.idx', 'io.meta_write.bits.tag', 'io.meta_write.bits.way_en', 'io.meta_write.ready', 'io.meta_write.valid', 'io.mshr_rdy', 'io.mshr_wb_rdy', 'io.rep.bits.address', 'io.rep.bits.corrupt', 'io.rep.bits.data', 'io.rep.bits.opcode', 'io.rep.bits.param', 'io.rep.bits.size', 'io.rep.bits.source', 'io.rep.ready', 'io.rep.valid', 'io.req.ready', 'io.req.valid', 'io.state.bits', 'io.state.valid', 'io.way_en', 'io.wb_rdy', 'io.wb_req.bits.idx', 'io.wb_req.bits.param', 'io.wb_req.bits.source', 'io.wb_req.bits.tag', 'io.wb_req.bits.voluntary', 'io.wb_req.bits.way_en', 'io.wb_req.ready', 'io.wb_req.valid']

## Source evidence

### generators/boom/src/main/scala/v4/lsu/dcache.scala:144-147
```scala

class BoomProbeUnit(implicit edge: TLEdgeOut, p: Parameters) extends L1HellaCacheModule()(p) {
  val io = IO(new Bundle {
    val req = Flipped(Decoupled(new TLBundleB(edge.bundle)))
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:164-176
```scala
       s_meta_write :: s_meta_write_resp :: Nil) = Enum(11)
  val state = RegInit(s_invalid)

  val req = Reg(new TLBundleB(edge.bundle))
  val req_idx = req.address(idxMSB, idxLSB)
  val req_tag = req.address >> untagBits

  val way_en = Reg(UInt())
  val tag_matches = way_en.orR
  val old_coh = Reg(new ClientMetadata)
  val miss_coh = ClientMetadata.onReset
  val reply_coh = Mux(tag_matches, old_coh, miss_coh)
  val (is_dirty, report_param, new_coh) = reply_coh.onProbe(req.param)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:177-186
```scala

  io.state.valid := state =/= s_invalid
  io.state.bits  := req.address

  io.req.ready := state === s_invalid
  io.rep.valid := state === s_release
  io.rep.bits := edge.ProbeAck(req, report_param)

  assert(!io.rep.valid || !edge.hasData(io.rep.bits),
    "ProbeUnit should not send ProbeAcks with data, WritebackUnit should handle it")
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:187-207
```scala

  io.meta_read.valid := state === s_meta_read
  io.meta_read.bits.idx := req_idx
  io.meta_read.bits.tag := req_tag
  io.meta_read.bits.way_en := ~(0.U(nWays.W))

  io.meta_write.valid := state === s_meta_write
  io.meta_write.bits.way_en := way_en
  io.meta_write.bits.idx := req_idx
  io.meta_write.bits.tag := req_tag
  io.meta_write.bits.data.tag := req_tag
  io.meta_write.bits.data.coh := new_coh

  io.wb_req.valid := state === s_writeback_req
  io.wb_req.bits.source := req.source
  io.wb_req.bits.idx := req_idx
  io.wb_req.bits.tag := req_tag
  io.wb_req.bits.param := report_param
  io.wb_req.bits.way_en := way_en
  io.wb_req.bits.voluntary := false.B
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:208-213
```scala

  io.mshr_wb_rdy := !state.isOneOf(s_release, s_writeback_req, s_writeback_resp, s_meta_write, s_meta_write_resp)

  io.lsu_release.valid := state === s_lsu_release
  io.lsu_release.bits  := edge.ProbeAck(req, report_param)
```

### generators/boom/src/main/scala/v4/lsu/dcache.scala:214-257
```scala
  // state === s_invalid
  when (state === s_invalid) {
    when (io.req.fire) {
      state := s_meta_read
      req := io.req.bits
    }
  } .elsewhen (state === s_meta_read) {
    when (io.meta_read.fire) {
      state := s_meta_resp
    }
  } .elsewhen (state === s_meta_resp) {
    // we need to wait one cycle for the metadata to be read from the array
    state := s_mshr_req
  } .elsewhen (state === s_mshr_req) {
    old_coh := io.block_state
    way_en := io.way_en
    // if the read didn't go through, we need to retry
    state := Mux(io.mshr_rdy && io.wb_rdy, s_mshr_resp, s_meta_read)
  } .elsewhen (state === s_mshr_resp) {
    state := Mux(tag_matches && is_dirty, s_writeback_req, s_lsu_release)
  } .elsewhen (state === s_lsu_release) {
    when (io.lsu_release.fire) {
      state := s_release
    }
  } .elsewhen (state === s_release) {
    when (io.rep.ready) {
      state := Mux(tag_matches, s_meta_write, s_invalid)
    }
  } .elsewhen (state === s_writeback_req) {
    when (io.wb_req.fire) {
      state := s_writeback_resp
    }
  } .elsewhen (state === s_writeback_resp) {
    // wait for the writeback request to finish before updating the metadata
    when (io.wb_req.ready) {
      state := s_meta_write
    }
  } .elsewhen (state === s_meta_write) {
    when (io.meta_write.fire) {
      state := s_meta_write_resp
    }
  } .elsewhen (state === s_meta_write_resp) {
    state := s_invalid
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:101-103
```scala
        //    opcode === TLMessages.LogicalData
      case c: TLBundleC => c.opcode(0)
        //    opcode === TLMessages.AccessAckData ||
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:415-422
```scala
  def ProbeAck(fromSource: UInt, toAddress: UInt, lgSize: UInt, reportPermissions: UInt): TLBundleC = {
    val c = Wire(new TLBundleC(bundle))
    c.opcode  := TLMessages.ProbeAck
    c.param   := reportPermissions
    c.size    := lgSize
    c.source  := fromSource
    c.address := toAddress
    c.user    := DontCare
```

### generators/rocket-chip/src/main/scala/tilelink/Edges.scala:423-426
```scala
    c.echo    := DontCare
    c.data    := DontCare
    c.corrupt := false.B
    c
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:119-134
```scala
    import TLPermissions._
    MuxTLookup(Cat(param, state), (false.B, 0.U, 0.U), Seq(
    //(wanted, am now)  -> (hasDirtyData resp, next)
      Cat(toT, Dirty)   -> (true.B,  TtoT, Trunk),
      Cat(toT, Trunk)   -> (false.B, TtoT, Trunk),
      Cat(toT, Branch)  -> (false.B, BtoB, Branch),
      Cat(toT, Nothing) -> (false.B, NtoN, Nothing),
      Cat(toB, Dirty)   -> (true.B,  TtoB, Branch),
      Cat(toB, Trunk)   -> (false.B, TtoB, Branch),  // Policy: Don't notify on clean downgrade
      Cat(toB, Branch)  -> (false.B, BtoB, Branch),
      Cat(toB, Nothing) -> (false.B, NtoN, Nothing),
      Cat(toN, Dirty)   -> (true.B,  TtoN, Nothing),
      Cat(toN, Trunk)   -> (false.B, TtoN, Nothing), // Policy: Don't notify on clean downgrade
      Cat(toN, Branch)  -> (false.B, BtoN, Nothing), // Policy: Don't notify on clean downgrade
      Cat(toN, Nothing) -> (false.B, NtoN, Nothing)))
  }
```

### generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:159-162
```scala
  def apply(perm: UInt) = {
    val meta = Wire(new ClientMetadata)
    meta.state := perm
    meta
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:37-39
```scala
  def apply[T <: Data, U <: Data, W <: Data](cond: Bool, con: (T, U, W), alt: (T, U, W)): (T, U, W) =
    (Mux(cond, con._1, alt._1), Mux(cond, con._2, alt._2), Mux(cond, con._3, alt._3))
```

### generators/rocket-chip/src/main/scala/util/Misc.scala:55-57
```scala
    for ((k, v) <- mapping.reverse)
      res = MuxT(k === key, v, res)
    res
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
[0] FIRRTL:188136 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:145:7 KIND:structural :: input clock : Clock
[1] FIRRTL:188137 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:145:7 KIND:structural :: input reset : Reset
[2] FIRRTL:188138 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:146:14 KIND:structural :: output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, address : UInt<32>, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}}, rep : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>}}, meta_write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<6>, way_en : UInt<4>, tag : UInt<20>, data : { coh : { state : UInt<2>}, tag : UInt<20>}}}, wb_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { tag : UInt<20>, idx : UInt<6>, source : UInt<2>, param : UInt<3>, way_en : UInt<4>, voluntary : UInt<1>}}, flip way_en : UInt<4>, flip wb_rdy : UInt<1>, flip mshr_rdy : UInt<1>, mshr_wb_rdy : UInt<1>, flip block_state : { state : UInt<2>}, lsu_release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}}, state : { valid : UInt<1>, bits : UInt<40>}}
[3] FIRRTL:188140 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:165:22 KIND:regreset :: regreset state : UInt<4>, clock, reset, UInt<4>(0h0)
[4] FIRRTL:188141 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:167:16 KIND:reg :: reg req : { opcode : UInt<3>, param : UInt<2>, size : UInt<4>, source : UInt<2>, address : UInt<32>, mask : UInt<8>, data : UInt<64>, corrupt : UInt<1>}, clock
[5] FIRRTL:188142 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:168:28 KIND:node :: node req_idx = bits(req.address, 11, 6)
[6] FIRRTL:188143 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:169:29 KIND:node :: node req_tag = shr(req.address, 12)
[7] FIRRTL:188144 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:171:19 KIND:reg :: reg way_en : UInt, clock
[8] FIRRTL:188145 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:172:28 KIND:node :: node tag_matches = orr(way_en)
[9] FIRRTL:188146 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:173:20 KIND:reg :: reg old_coh : { state : UInt<2>}, clock
[10] FIRRTL:188147 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire miss_coh : { state : UInt<2>}
[11] FIRRTL:188148 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect miss_coh.state, UInt<2>(0h0)
[12] FIRRTL:188149 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:175:22 KIND:node :: node reply_coh = mux(tag_matches, old_coh, miss_coh)
[13] FIRRTL:188150 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:120:19 KIND:node :: node _r_T = cat(req.param, reply_coh.state)
[14] FIRRTL:188151 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:122:10 KIND:node :: node _r_T_1 = cat(UInt<2>(0h0), UInt<2>(0h3))
[15] FIRRTL:188152 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:123:10 KIND:node :: node _r_T_2 = cat(UInt<2>(0h0), UInt<2>(0h2))
[16] FIRRTL:188153 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:124:10 KIND:node :: node _r_T_3 = cat(UInt<2>(0h0), UInt<2>(0h1))
[17] FIRRTL:188154 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:125:10 KIND:node :: node _r_T_4 = cat(UInt<2>(0h0), UInt<2>(0h0))
[18] FIRRTL:188155 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:126:10 KIND:node :: node _r_T_5 = cat(UInt<2>(0h1), UInt<2>(0h3))
[19] FIRRTL:188156 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:127:10 KIND:node :: node _r_T_6 = cat(UInt<2>(0h1), UInt<2>(0h2))
[20] FIRRTL:188157 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:128:10 KIND:node :: node _r_T_7 = cat(UInt<2>(0h1), UInt<2>(0h1))
[21] FIRRTL:188158 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:129:10 KIND:node :: node _r_T_8 = cat(UInt<2>(0h1), UInt<2>(0h0))
[22] FIRRTL:188159 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:130:10 KIND:node :: node _r_T_9 = cat(UInt<2>(0h2), UInt<2>(0h3))
[23] FIRRTL:188160 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:131:10 KIND:node :: node _r_T_10 = cat(UInt<2>(0h2), UInt<2>(0h2))
[24] FIRRTL:188161 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:132:10 KIND:node :: node _r_T_11 = cat(UInt<2>(0h2), UInt<2>(0h1))
[25] FIRRTL:188162 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:133:10 KIND:node :: node _r_T_12 = cat(UInt<2>(0h2), UInt<2>(0h0))
[26] FIRRTL:188163 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_13 = eq(_r_T_12, _r_T)
[27] FIRRTL:188164 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_14 = mux(_r_T_13, UInt<1>(0h0), UInt<1>(0h0))
[28] FIRRTL:188165 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_15 = mux(_r_T_13, UInt<3>(0h5), UInt<1>(0h0))
[29] FIRRTL:188166 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_16 = mux(_r_T_13, UInt<2>(0h0), UInt<1>(0h0))
[30] FIRRTL:188167 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_17 = eq(_r_T_11, _r_T)
[31] FIRRTL:188168 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_18 = mux(_r_T_17, UInt<1>(0h0), _r_T_14)
[32] FIRRTL:188169 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_19 = mux(_r_T_17, UInt<3>(0h2), _r_T_15)
[33] FIRRTL:188170 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_20 = mux(_r_T_17, UInt<2>(0h0), _r_T_16)
[34] FIRRTL:188171 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_21 = eq(_r_T_10, _r_T)
[35] FIRRTL:188172 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_22 = mux(_r_T_21, UInt<1>(0h0), _r_T_18)
[36] FIRRTL:188173 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_23 = mux(_r_T_21, UInt<3>(0h1), _r_T_19)
[37] FIRRTL:188174 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_24 = mux(_r_T_21, UInt<2>(0h0), _r_T_20)
[38] FIRRTL:188175 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_25 = eq(_r_T_9, _r_T)
[39] FIRRTL:188176 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_26 = mux(_r_T_25, UInt<1>(0h1), _r_T_22)
[40] FIRRTL:188177 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_27 = mux(_r_T_25, UInt<3>(0h1), _r_T_23)
[41] FIRRTL:188178 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_28 = mux(_r_T_25, UInt<2>(0h0), _r_T_24)
[42] FIRRTL:188179 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_29 = eq(_r_T_8, _r_T)
[43] FIRRTL:188180 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_30 = mux(_r_T_29, UInt<1>(0h0), _r_T_26)
[44] FIRRTL:188181 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_31 = mux(_r_T_29, UInt<3>(0h5), _r_T_27)
[45] FIRRTL:188182 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_32 = mux(_r_T_29, UInt<2>(0h0), _r_T_28)
[46] FIRRTL:188183 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_33 = eq(_r_T_7, _r_T)
[47] FIRRTL:188184 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_34 = mux(_r_T_33, UInt<1>(0h0), _r_T_30)
[48] FIRRTL:188185 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_35 = mux(_r_T_33, UInt<3>(0h4), _r_T_31)
[49] FIRRTL:188186 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_36 = mux(_r_T_33, UInt<2>(0h1), _r_T_32)
[50] FIRRTL:188187 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_37 = eq(_r_T_6, _r_T)
[51] FIRRTL:188188 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_38 = mux(_r_T_37, UInt<1>(0h0), _r_T_34)
[52] FIRRTL:188189 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_39 = mux(_r_T_37, UInt<3>(0h0), _r_T_35)
[53] FIRRTL:188190 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_40 = mux(_r_T_37, UInt<2>(0h1), _r_T_36)
[54] FIRRTL:188191 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_41 = eq(_r_T_5, _r_T)
[55] FIRRTL:188192 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_42 = mux(_r_T_41, UInt<1>(0h1), _r_T_38)
[56] FIRRTL:188193 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_43 = mux(_r_T_41, UInt<3>(0h0), _r_T_39)
[57] FIRRTL:188194 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_44 = mux(_r_T_41, UInt<2>(0h1), _r_T_40)
[58] FIRRTL:188195 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_45 = eq(_r_T_4, _r_T)
[59] FIRRTL:188196 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_46 = mux(_r_T_45, UInt<1>(0h0), _r_T_42)
[60] FIRRTL:188197 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_47 = mux(_r_T_45, UInt<3>(0h5), _r_T_43)
[61] FIRRTL:188198 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_48 = mux(_r_T_45, UInt<2>(0h0), _r_T_44)
[62] FIRRTL:188199 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_49 = eq(_r_T_3, _r_T)
[63] FIRRTL:188200 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_50 = mux(_r_T_49, UInt<1>(0h0), _r_T_46)
[64] FIRRTL:188201 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_51 = mux(_r_T_49, UInt<3>(0h4), _r_T_47)
[65] FIRRTL:188202 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_52 = mux(_r_T_49, UInt<2>(0h1), _r_T_48)
[66] FIRRTL:188203 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_53 = eq(_r_T_2, _r_T)
[67] FIRRTL:188204 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node _r_T_54 = mux(_r_T_53, UInt<1>(0h0), _r_T_50)
[68] FIRRTL:188205 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node _r_T_55 = mux(_r_T_53, UInt<3>(0h3), _r_T_51)
[69] FIRRTL:188206 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node _r_T_56 = mux(_r_T_53, UInt<2>(0h2), _r_T_52)
[70] FIRRTL:188207 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:56:20 KIND:node :: node _r_T_57 = eq(_r_T_1, _r_T)
[71] FIRRTL:188208 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:9 KIND:node :: node is_dirty = mux(_r_T_57, UInt<1>(0h1), _r_T_54)
[72] FIRRTL:188209 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:36 KIND:node :: node report_param = mux(_r_T_57, UInt<3>(0h3), _r_T_55)
[73] FIRRTL:188210 SRC:generators/rocket-chip/src/main/scala/util/Misc.scala:38:63 KIND:node :: node r_3 = mux(_r_T_57, UInt<2>(0h2), _r_T_56)
[74] FIRRTL:188211 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:160:20 KIND:wire :: wire new_coh : { state : UInt<2>}
[75] FIRRTL:188212 SRC:generators/rocket-chip/src/main/scala/tilelink/Metadata.scala:161:16 KIND:connect :: connect new_coh.state, r_3
[76] FIRRTL:188213 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:178:27 KIND:node :: node _io_state_valid_T = neq(state, UInt<4>(0h0))
[77] FIRRTL:188214 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:178:18 KIND:connect :: connect io.state.valid, _io_state_valid_T
[78] FIRRTL:188215 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:179:18 KIND:connect :: connect io.state.bits, req.address
[79] FIRRTL:188216 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:181:25 KIND:node :: node _io_req_ready_T = eq(state, UInt<4>(0h0))
[80] FIRRTL:188217 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:181:16 KIND:connect :: connect io.req.ready, _io_req_ready_T
[81] FIRRTL:188218 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:182:25 KIND:node :: node _io_rep_valid_T = eq(state, UInt<4>(0h6))
[82] FIRRTL:188219 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:182:16 KIND:connect :: connect io.rep.valid, _io_rep_valid_T
[83] FIRRTL:188220 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:416:17 KIND:wire :: wire io_rep_bits_c : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}
[84] FIRRTL:188221 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:417:15 KIND:connect :: connect io_rep_bits_c.opcode, UInt<3>(0h4)
[85] FIRRTL:188222 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:418:15 KIND:connect :: connect io_rep_bits_c.param, report_param
[86] FIRRTL:188223 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:419:15 KIND:connect :: connect io_rep_bits_c.size, req.size
[87] FIRRTL:188224 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:420:15 KIND:connect :: connect io_rep_bits_c.source, req.source
[88] FIRRTL:188225 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:421:15 KIND:connect :: connect io_rep_bits_c.address, req.address
[89] FIRRTL:188226 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:424:15 KIND:invalidate :: invalidate io_rep_bits_c.data
[90] FIRRTL:188227 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:425:15 KIND:connect :: connect io_rep_bits_c.corrupt, UInt<1>(0h0)
[91] FIRRTL:188228 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:183:15 KIND:connect :: connect io.rep.bits, io_rep_bits_c
[92] FIRRTL:188229 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:10 KIND:node :: node _T = eq(io.rep.valid, UInt<1>(0h0))
[93] FIRRTL:188230 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:102:36 KIND:node :: node opdata = bits(io.rep.bits.opcode, 0, 0)
[94] FIRRTL:188231 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:27 KIND:node :: node _T_1 = eq(opdata, UInt<1>(0h0))
[95] FIRRTL:188232 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:24 KIND:node :: node _T_2 = or(_T, _T_1)
[96] FIRRTL:188233 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:node :: node _T_3 = asUInt(reset)
[97] FIRRTL:188234 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:node :: node _T_4 = eq(_T_3, UInt<1>(0h0))
[98] FIRRTL:188235 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:when :: when _T_4 :
[99] FIRRTL:188236 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:node :: node _T_5 = eq(_T_2, UInt<1>(0h0))
[100] FIRRTL:188237 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:when :: when _T_5 :
[101] FIRRTL:188238 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:nondriving :: printf(clock, UInt<1>(0h1), "Assertion failed: ProbeUnit should not send ProbeAcks with data, WritebackUnit should handle it\n    at dcache.scala:185 assert(!io.rep.valid || !edge.hasData(io.rep.bits),\n") : printf
[102] FIRRTL:188239 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:185:9 KIND:nondriving :: assert(clock, _T_2, UInt<1>(0h1), "") : assert
[103] FIRRTL:188240 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:188:31 KIND:node :: node _io_meta_read_valid_T = eq(state, UInt<4>(0h1))
[104] FIRRTL:188241 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:188:22 KIND:connect :: connect io.meta_read.valid, _io_meta_read_valid_T
[105] FIRRTL:188242 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:189:25 KIND:connect :: connect io.meta_read.bits.idx, req_idx
[106] FIRRTL:188243 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:190:25 KIND:connect :: connect io.meta_read.bits.tag, req_tag
[107] FIRRTL:188244 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:191:31 KIND:node :: node _io_meta_read_bits_way_en_T = not(UInt<4>(0h0))
[108] FIRRTL:188245 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:191:28 KIND:connect :: connect io.meta_read.bits.way_en, _io_meta_read_bits_way_en_T
[109] FIRRTL:188246 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:193:32 KIND:node :: node _io_meta_write_valid_T = eq(state, UInt<4>(0h9))
[110] FIRRTL:188247 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:193:23 KIND:connect :: connect io.meta_write.valid, _io_meta_write_valid_T
[111] FIRRTL:188248 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:194:29 KIND:connect :: connect io.meta_write.bits.way_en, way_en
[112] FIRRTL:188249 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:195:26 KIND:connect :: connect io.meta_write.bits.idx, req_idx
[113] FIRRTL:188250 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:196:26 KIND:connect :: connect io.meta_write.bits.tag, req_tag
[114] FIRRTL:188251 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:197:31 KIND:connect :: connect io.meta_write.bits.data.tag, req_tag
[115] FIRRTL:188252 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:198:31 KIND:connect :: connect io.meta_write.bits.data.coh, new_coh
[116] FIRRTL:188253 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:200:28 KIND:node :: node _io_wb_req_valid_T = eq(state, UInt<4>(0h7))
[117] FIRRTL:188254 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:200:19 KIND:connect :: connect io.wb_req.valid, _io_wb_req_valid_T
[118] FIRRTL:188255 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:201:25 KIND:connect :: connect io.wb_req.bits.source, req.source
[119] FIRRTL:188256 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:202:22 KIND:connect :: connect io.wb_req.bits.idx, req_idx
[120] FIRRTL:188257 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:203:22 KIND:connect :: connect io.wb_req.bits.tag, req_tag
[121] FIRRTL:188258 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:204:24 KIND:connect :: connect io.wb_req.bits.param, report_param
[122] FIRRTL:188259 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:205:25 KIND:connect :: connect io.wb_req.bits.way_en, way_en
[123] FIRRTL:188260 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:206:28 KIND:connect :: connect io.wb_req.bits.voluntary, UInt<1>(0h0)
[124] FIRRTL:188261 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mshr_wb_rdy_T = eq(state, UInt<4>(0h6))
[125] FIRRTL:188262 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mshr_wb_rdy_T_1 = eq(state, UInt<4>(0h7))
[126] FIRRTL:188263 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mshr_wb_rdy_T_2 = eq(state, UInt<4>(0h8))
[127] FIRRTL:188264 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mshr_wb_rdy_T_3 = eq(state, UInt<4>(0h9))
[128] FIRRTL:188265 SRC:generators/rocket-chip/src/main/scala/util/package.scala:17:47 KIND:node :: node _io_mshr_wb_rdy_T_4 = eq(state, UInt<4>(0ha))
[129] FIRRTL:188266 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mshr_wb_rdy_T_5 = or(_io_mshr_wb_rdy_T, _io_mshr_wb_rdy_T_1)
[130] FIRRTL:188267 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mshr_wb_rdy_T_6 = or(_io_mshr_wb_rdy_T_5, _io_mshr_wb_rdy_T_2)
[131] FIRRTL:188268 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mshr_wb_rdy_T_7 = or(_io_mshr_wb_rdy_T_6, _io_mshr_wb_rdy_T_3)
[132] FIRRTL:188269 SRC:generators/rocket-chip/src/main/scala/util/package.scala:82:59 KIND:node :: node _io_mshr_wb_rdy_T_8 = or(_io_mshr_wb_rdy_T_7, _io_mshr_wb_rdy_T_4)
[133] FIRRTL:188270 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:209:21 KIND:node :: node _io_mshr_wb_rdy_T_9 = eq(_io_mshr_wb_rdy_T_8, UInt<1>(0h0))
[134] FIRRTL:188271 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:209:18 KIND:connect :: connect io.mshr_wb_rdy, _io_mshr_wb_rdy_T_9
[135] FIRRTL:188272 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:211:33 KIND:node :: node _io_lsu_release_valid_T = eq(state, UInt<4>(0h5))
[136] FIRRTL:188273 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:211:24 KIND:connect :: connect io.lsu_release.valid, _io_lsu_release_valid_T
[137] FIRRTL:188274 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:416:17 KIND:wire :: wire io_lsu_release_bits_c : { opcode : UInt<3>, param : UInt<3>, size : UInt<4>, source : UInt<2>, address : UInt<32>, user : { }, echo : { }, data : UInt<64>, corrupt : UInt<1>}
[138] FIRRTL:188275 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:417:15 KIND:connect :: connect io_lsu_release_bits_c.opcode, UInt<3>(0h4)
[139] FIRRTL:188276 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:418:15 KIND:connect :: connect io_lsu_release_bits_c.param, report_param
[140] FIRRTL:188277 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:419:15 KIND:connect :: connect io_lsu_release_bits_c.size, req.size
[141] FIRRTL:188278 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:420:15 KIND:connect :: connect io_lsu_release_bits_c.source, req.source
[142] FIRRTL:188279 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:421:15 KIND:connect :: connect io_lsu_release_bits_c.address, req.address
[143] FIRRTL:188280 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:424:15 KIND:invalidate :: invalidate io_lsu_release_bits_c.data
[144] FIRRTL:188281 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:425:15 KIND:connect :: connect io_lsu_release_bits_c.corrupt, UInt<1>(0h0)
[145] FIRRTL:188282 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:212:24 KIND:connect :: connect io.lsu_release.bits, io_lsu_release_bits_c
[146] FIRRTL:188283 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:215:15 KIND:node :: node _T_6 = eq(state, UInt<4>(0h0))
[147] FIRRTL:188284 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:215:30 KIND:when :: when _T_6 :
[148] FIRRTL:188285 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_7 = and(io.req.ready, io.req.valid)
[149] FIRRTL:188286 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:216:24 KIND:when :: when _T_7 :
[150] FIRRTL:188287 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:217:13 KIND:connect :: connect state, UInt<4>(0h1)
[151] FIRRTL:188288 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:218:11 KIND:connect :: connect req, io.req.bits
[152] FIRRTL:188289 SRC:<no-source-locator> KIND:else :: else :
[153] FIRRTL:188290 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:220:22 KIND:node :: node _T_8 = eq(state, UInt<4>(0h1))
[154] FIRRTL:188291 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:220:39 KIND:when :: when _T_8 :
[155] FIRRTL:188292 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_9 = and(io.meta_read.ready, io.meta_read.valid)
[156] FIRRTL:188293 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:221:30 KIND:when :: when _T_9 :
[157] FIRRTL:188294 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:222:13 KIND:connect :: connect state, UInt<4>(0h2)
[158] FIRRTL:188295 SRC:<no-source-locator> KIND:else :: else :
[159] FIRRTL:188296 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:224:22 KIND:node :: node _T_10 = eq(state, UInt<4>(0h2))
[160] FIRRTL:188297 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:224:39 KIND:when :: when _T_10 :
[161] FIRRTL:188298 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:226:11 KIND:connect :: connect state, UInt<4>(0h3)
[162] FIRRTL:188299 SRC:<no-source-locator> KIND:else :: else :
[163] FIRRTL:188300 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:227:22 KIND:node :: node _T_11 = eq(state, UInt<4>(0h3))
[164] FIRRTL:188301 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:227:38 KIND:when :: when _T_11 :
[165] FIRRTL:188302 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:228:13 KIND:connect :: connect old_coh, io.block_state
[166] FIRRTL:188303 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:229:12 KIND:connect :: connect way_en, io.way_en
[167] FIRRTL:188304 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:231:30 KIND:node :: node _state_T = and(io.mshr_rdy, io.wb_rdy)
[168] FIRRTL:188305 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:231:17 KIND:node :: node _state_T_1 = mux(_state_T, UInt<4>(0h4), UInt<4>(0h1))
[169] FIRRTL:188306 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:231:11 KIND:connect :: connect state, _state_T_1
[170] FIRRTL:188307 SRC:<no-source-locator> KIND:else :: else :
[171] FIRRTL:188308 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:232:22 KIND:node :: node _T_12 = eq(state, UInt<4>(0h4))
[172] FIRRTL:188309 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:232:39 KIND:when :: when _T_12 :
[173] FIRRTL:188310 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:233:30 KIND:node :: node _state_T_2 = and(tag_matches, is_dirty)
[174] FIRRTL:188311 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:233:17 KIND:node :: node _state_T_3 = mux(_state_T_2, UInt<4>(0h7), UInt<4>(0h5))
[175] FIRRTL:188312 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:233:11 KIND:connect :: connect state, _state_T_3
[176] FIRRTL:188313 SRC:<no-source-locator> KIND:else :: else :
[177] FIRRTL:188314 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:234:22 KIND:node :: node _T_13 = eq(state, UInt<4>(0h5))
[178] FIRRTL:188315 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:234:41 KIND:when :: when _T_13 :
[179] FIRRTL:188316 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_14 = and(io.lsu_release.ready, io.lsu_release.valid)
[180] FIRRTL:188317 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:235:32 KIND:when :: when _T_14 :
[181] FIRRTL:188318 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:236:13 KIND:connect :: connect state, UInt<4>(0h6)
[182] FIRRTL:188319 SRC:<no-source-locator> KIND:else :: else :
[183] FIRRTL:188320 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:238:22 KIND:node :: node _T_15 = eq(state, UInt<4>(0h6))
[184] FIRRTL:188321 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:238:37 KIND:when :: when _T_15 :
[185] FIRRTL:188322 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:239:25 KIND:when :: when io.rep.ready :
[186] FIRRTL:188323 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:240:19 KIND:node :: node _state_T_4 = mux(tag_matches, UInt<4>(0h9), UInt<4>(0h0))
[187] FIRRTL:188324 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:240:13 KIND:connect :: connect state, _state_T_4
[188] FIRRTL:188325 SRC:<no-source-locator> KIND:else :: else :
[189] FIRRTL:188326 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:242:22 KIND:node :: node _T_16 = eq(state, UInt<4>(0h7))
[190] FIRRTL:188327 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:242:43 KIND:when :: when _T_16 :
[191] FIRRTL:188328 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_17 = and(io.wb_req.ready, io.wb_req.valid)
[192] FIRRTL:188329 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:243:27 KIND:when :: when _T_17 :
[193] FIRRTL:188330 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:244:13 KIND:connect :: connect state, UInt<4>(0h8)
[194] FIRRTL:188331 SRC:<no-source-locator> KIND:else :: else :
[195] FIRRTL:188332 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:246:22 KIND:node :: node _T_18 = eq(state, UInt<4>(0h8))
[196] FIRRTL:188333 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:246:44 KIND:when :: when _T_18 :
[197] FIRRTL:188334 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:248:28 KIND:when :: when io.wb_req.ready :
[198] FIRRTL:188335 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:249:13 KIND:connect :: connect state, UInt<4>(0h9)
[199] FIRRTL:188336 SRC:<no-source-locator> KIND:else :: else :
[200] FIRRTL:188337 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:251:22 KIND:node :: node _T_19 = eq(state, UInt<4>(0h9))
[201] FIRRTL:188338 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:251:40 KIND:when :: when _T_19 :
[202] FIRRTL:188339 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _T_20 = and(io.meta_write.ready, io.meta_write.valid)
[203] FIRRTL:188340 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:252:31 KIND:when :: when _T_20 :
[204] FIRRTL:188341 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:253:13 KIND:connect :: connect state, UInt<4>(0ha)
[205] FIRRTL:188342 SRC:<no-source-locator> KIND:else :: else :
[206] FIRRTL:188343 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:255:22 KIND:node :: node _T_21 = eq(state, UInt<4>(0ha))
[207] FIRRTL:188344 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:255:45 KIND:when :: when _T_21 :
[208] FIRRTL:188345 SRC:generators/boom/src/main/scala/v4/lsu/dcache.scala:256:11 KIND:connect :: connect state, UInt<4>(0h0)
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
  "schema_version": "umcm-formal-0.3",
  "task_id": "leaf_abstraction-BoomProbeUnit-6a11da8fc6b94afe",
  "work_unit_id": "BoomProbeUnit",
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
