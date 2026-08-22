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

Task ID: `leaf_abstraction-LSU.dtlb.pmp_0-751666a56ace25f8`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.14`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `LSU.dtlb.pmp_0`
- module: `PMPChecker_s3_1`
- kind: `module`
- instance path: `LSU.dtlb.pmp_0`
- leaf: `True`
- coverage complete: `True`
- raw statements: 1597
- logical statements: 47
- mapped/logical source lines: 42
- registers: 0
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



## Concrete local state

[]

## Environment/frontier signals

['io.addr', 'io.pmp[0].addr', 'io.pmp[0].cfg.a', 'io.pmp[0].cfg.l', 'io.pmp[0].cfg.r', 'io.pmp[0].cfg.w', 'io.pmp[0].cfg.x', 'io.pmp[0].mask', 'io.pmp[1].addr', 'io.pmp[1].cfg.a', 'io.pmp[1].cfg.l', 'io.pmp[1].cfg.r', 'io.pmp[1].cfg.w', 'io.pmp[1].cfg.x', 'io.pmp[1].mask', 'io.pmp[2].addr', 'io.pmp[2].cfg.a', 'io.pmp[2].cfg.l', 'io.pmp[2].cfg.r', 'io.pmp[2].cfg.w', 'io.pmp[2].cfg.x', 'io.pmp[2].mask', 'io.pmp[3].addr', 'io.pmp[3].cfg.a', 'io.pmp[3].cfg.l', 'io.pmp[3].cfg.r', 'io.pmp[3].cfg.w', 'io.pmp[3].cfg.x', 'io.pmp[3].mask', 'io.pmp[4].addr', 'io.pmp[4].cfg.a', 'io.pmp[4].cfg.l', 'io.pmp[4].cfg.r', 'io.pmp[4].cfg.w', 'io.pmp[4].cfg.x', 'io.pmp[4].mask', 'io.pmp[5].addr', 'io.pmp[5].cfg.a', 'io.pmp[5].cfg.l', 'io.pmp[5].cfg.r', 'io.pmp[5].cfg.w', 'io.pmp[5].cfg.x', 'io.pmp[5].mask', 'io.pmp[6].addr', 'io.pmp[6].cfg.a', 'io.pmp[6].cfg.l', 'io.pmp[6].cfg.r', 'io.pmp[6].cfg.w', 'io.pmp[6].cfg.x', 'io.pmp[6].mask', 'io.pmp[7].addr', 'io.pmp[7].cfg.a', 'io.pmp[7].cfg.l', 'io.pmp[7].cfg.r', 'io.pmp[7].cfg.w', 'io.pmp[7].cfg.x', 'io.pmp[7].mask', 'io.prv', 'io.r', 'io.size', 'io.w', 'io.x']

## Source evidence

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:44-47
```scala
  }
  def napot = cfg.a(1)
  def torNotNAPOT = cfg.a(0)
  def tor = !napot && torNotNAPOT
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:59-61
```scala
  }
  private def comparand = ~(~(addr << lgAlign) | (pmpGranularity - 1).U)
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:62-64
```scala
  private def pow2Match(x: UInt, lgSize: UInt, lgMaxSize: Int) = {
    def eval(a: UInt, b: UInt, m: UInt) = ((a ^ b) & ~m) === 0.U
    if (lgMaxSize <= pmpGranularity.log2) {
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:67-72
```scala
      // break up the circuit; the MSB part will be CSE'd
      val lsbMask = mask | UIntToOH1(lgSize, lgMaxSize)
      val msbMatch = eval(x >> lgMaxSize, comparand >> lgMaxSize, mask >> lgMaxSize)
      val lsbMatch = eval(x(lgMaxSize-1, 0), comparand(lgMaxSize-1, 0), lsbMask(lgMaxSize-1, 0))
      msbMatch && lsbMatch
    }
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:79-84
```scala
      // break up the circuit; the MSB part will be CSE'd
      val msbsLess = (x >> lgMaxSize) < (comparand >> lgMaxSize)
      val msbsEqual = ((x >> lgMaxSize) ^ (comparand >> lgMaxSize)) === 0.U
      val lsbsLess =  (x(lgMaxSize-1, 0) | lsbMask) < comparand(lgMaxSize-1, 0)
      msbsLess || (msbsEqual && lsbsLess)
    }
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:87-89
```scala
  private def lowerBoundMatch(x: UInt, lgSize: UInt, lgMaxSize: Int) =
    !boundMatch(x, UIntToOH1(lgSize, lgMaxSize), lgMaxSize)
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:93-95
```scala
  private def rangeMatch(x: UInt, lgSize: UInt, lgMaxSize: Int, prev: PMP) =
    prev.lowerBoundMatch(x, lgSize, lgMaxSize) && upperBoundMatch(x, lgMaxSize)
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:122-128
```scala
    val lsbMask = UIntToOH1(lgSize, lgMaxSize)
    val straddlesLowerBound = ((x >> lgMaxSize) ^ (prev.comparand >> lgMaxSize)) === 0.U && (prev.comparand(lgMaxSize-1, 0) & ~x(lgMaxSize-1, 0)) =/= 0.U
    val straddlesUpperBound = ((x >> lgMaxSize) ^ (comparand >> lgMaxSize)) === 0.U && (comparand(lgMaxSize-1, 0) & (x(lgMaxSize-1, 0) | lsbMask)) =/= 0.U
    val rangeAligned = !(straddlesLowerBound || straddlesUpperBound)
    val pow2Aligned = (lsbMask & ~mask(lgMaxSize-1, 0)) === 0.U
    Mux(napot, pow2Aligned, rangeAligned)
  }
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:131-133
```scala
  def hit(x: UInt, lgSize: UInt, lgMaxSize: Int, prev: PMP): Bool =
    Mux(napot, pow2Match(x, lgSize, lgMaxSize), torNotNAPOT && rangeMatch(x, lgSize, lgMaxSize, prev))
}
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:142-144
```scala

class PMPChecker(lgMaxSize: Int)(implicit val p: Parameters) extends Module
    with HasCoreParameters {
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:145-147
```scala
  override def desiredName = s"PMPChecker_s${lgMaxSize}"
  val io = IO(new Bundle {
    val prv = Input(UInt(PRV.SZ.W))
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:155-161
```scala

  val default = if (io.pmp.isEmpty) true.B else io.prv > PRV.S.U
  val pmp0 = WireInit(0.U.asTypeOf(new PMP))
  pmp0.cfg.r := default
  pmp0.cfg.w := default
  pmp0.cfg.x := default
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:163-165
```scala
    val hit = pmp.hit(io.addr, io.size, lgMaxSize, prevPMP)
    val ignore = default && !pmp.cfg.l
    val aligned = pmp.aligned(io.addr, io.size, lgMaxSize, prevPMP)
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:167-171
```scala
    for ((name, idx) <- Seq("no", "TOR", if (pmpGranularity <= 4) "NA4" else "", "NAPOT").zipWithIndex; if name.nonEmpty)
      property.cover(pmp.cfg.a === idx.U, s"The cfg access is set to ${name} access ", "Cover PMP access mode setting")

    property.cover(pmp.cfg.l === 0x1.U, s"The cfg lock is set to high ", "Cover PMP lock mode setting")
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:173-175
```scala
    for ((name, idx) <- Seq("no", "RO", "", "RW", "X", "RX", "", "RWX").zipWithIndex; if name.nonEmpty)
      property.cover((Cat(pmp.cfg.x, pmp.cfg.w, pmp.cfg.r) === idx.U), s"The permission is set to ${name} access ", "Cover PMP access permission setting")
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:176-179
```scala
    for ((name, idx) <- Seq("", "TOR", if (pmpGranularity <= 4) "NA4" else "", "NAPOT").zipWithIndex; if name.nonEmpty) {
      property.cover(!ignore && hit && aligned && pmp.cfg.a === idx.U, s"The access matches ${name} mode ", "Cover PMP access")
      property.cover(pmp.cfg.l && hit && aligned && pmp.cfg.a === idx.U, s"The access matches ${name} mode with lock bit high", "Cover PMP access with lock bit")
    }
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:180-186
```scala

    val cur = WireInit(pmp)
    cur.cfg.r := aligned && (pmp.cfg.r || ignore)
    cur.cfg.w := aligned && (pmp.cfg.w || ignore)
    cur.cfg.x := aligned && (pmp.cfg.x || ignore)
    Mux(hit, cur, prev)
  }
```

### generators/rocket-chip/src/main/scala/rocket/PMP.scala:187-191
```scala

  io.r := res.cfg.r
  io.w := res.cfg.w
  io.x := res.cfg.x
}
```

### generators/rocket-chip/src/main/scala/util/package.scala:243-245
```scala
  def OH1ToUInt(x: UInt): UInt = OHToUInt(OH1ToOH(x))
  def UIntToOH1(x: UInt, width: Int): UInt = ~((-1).S(width.W).asUInt << x)(width-1, 0)
  def UIntToOH1(x: UInt): UInt = UIntToOH1(x, (1 << x.getWidth) - 1)
```

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:360243 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:143:7 KIND:structural :: input clock : Clock
[1] FIRRTL:360244 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:143:7 KIND:structural :: input reset : Reset
[2] FIRRTL:360245 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:146:14 KIND:structural :: output io : { flip prv : UInt<2>, flip pmp : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}[8], flip addr : UInt<32>, flip size : UInt<2>, r : UInt<1>, w : UInt<1>, x : UInt<1>}
[3] FIRRTL:360247 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:156:56 KIND:node :: node default = gt(io.prv, UInt<1>(0h1))
[4] FIRRTL:360248 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:wire :: wire _pmp0_WIRE : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[5] FIRRTL:360249 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.mask, UInt<32>(0h0)
[6] FIRRTL:360250 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.addr, UInt<30>(0h0)
[7] FIRRTL:360251 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.r, UInt<1>(0h0)
[8] FIRRTL:360252 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.w, UInt<1>(0h0)
[9] FIRRTL:360253 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.x, UInt<1>(0h0)
[10] FIRRTL:360254 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.a, UInt<2>(0h0)
[11] FIRRTL:360255 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.res, UInt<2>(0h0)
[12] FIRRTL:360256 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:35 KIND:connect :: connect _pmp0_WIRE.cfg.l, UInt<1>(0h0)
[13] FIRRTL:360257 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:22 KIND:wire :: wire pmp0 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[14] FIRRTL:360258 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:157:22 KIND:connect :: connect pmp0, _pmp0_WIRE
[15] FIRRTL:360259 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:158:14 KIND:connect :: connect pmp0.cfg.r, default
[16] FIRRTL:360260 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:159:14 KIND:connect :: connect pmp0.cfg.w, default
[17] FIRRTL:360261 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:160:14 KIND:connect :: connect pmp0.cfg.x, default
[18] FIRRTL:360262 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T = bits(io.pmp[7].cfg.a, 1, 1)
[19] FIRRTL:360263 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T = dshl(UInt<3>(0h7), io.size)
[20] FIRRTL:360264 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_1 = bits(_res_hit_lsbMask_T, 2, 0)
[21] FIRRTL:360265 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_2 = not(_res_hit_lsbMask_T_1)
[22] FIRRTL:360266 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask = or(io.pmp[7].mask, _res_hit_lsbMask_T_2)
[23] FIRRTL:360267 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T = shr(io.addr, 3)
[24] FIRRTL:360268 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_1 = shl(io.pmp[7].addr, 2)
[25] FIRRTL:360269 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_2 = not(_res_hit_msbMatch_T_1)
[26] FIRRTL:360270 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_3 = or(_res_hit_msbMatch_T_2, UInt<2>(0h3))
[27] FIRRTL:360271 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_4 = not(_res_hit_msbMatch_T_3)
[28] FIRRTL:360272 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_5 = shr(_res_hit_msbMatch_T_4, 3)
[29] FIRRTL:360273 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_6 = shr(io.pmp[7].mask, 3)
[30] FIRRTL:360274 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_7 = xor(_res_hit_msbMatch_T, _res_hit_msbMatch_T_5)
[31] FIRRTL:360275 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_8 = not(_res_hit_msbMatch_T_6)
[32] FIRRTL:360276 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_9 = and(_res_hit_msbMatch_T_7, _res_hit_msbMatch_T_8)
[33] FIRRTL:360277 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch = eq(_res_hit_msbMatch_T_9, UInt<1>(0h0))
[34] FIRRTL:360278 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T = bits(io.addr, 2, 0)
[35] FIRRTL:360279 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_1 = shl(io.pmp[7].addr, 2)
[36] FIRRTL:360280 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_2 = not(_res_hit_lsbMatch_T_1)
[37] FIRRTL:360281 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_3 = or(_res_hit_lsbMatch_T_2, UInt<2>(0h3))
[38] FIRRTL:360282 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_4 = not(_res_hit_lsbMatch_T_3)
[39] FIRRTL:360283 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_5 = bits(_res_hit_lsbMatch_T_4, 2, 0)
[40] FIRRTL:360284 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_6 = bits(res_hit_lsbMask, 2, 0)
[41] FIRRTL:360285 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_7 = xor(_res_hit_lsbMatch_T, _res_hit_lsbMatch_T_5)
[42] FIRRTL:360286 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_8 = not(_res_hit_lsbMatch_T_6)
[43] FIRRTL:360287 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_9 = and(_res_hit_lsbMatch_T_7, _res_hit_lsbMatch_T_8)
[44] FIRRTL:360288 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch = eq(_res_hit_lsbMatch_T_9, UInt<1>(0h0))
[45] FIRRTL:360289 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_1 = and(res_hit_msbMatch, res_hit_lsbMatch)
[46] FIRRTL:360290 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_2 = bits(io.pmp[7].cfg.a, 0, 0)
[47] FIRRTL:360291 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_3 = dshl(UInt<3>(0h7), io.size)
[48] FIRRTL:360292 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_4 = bits(_res_hit_T_3, 2, 0)
[49] FIRRTL:360293 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_5 = not(_res_hit_T_4)
[50] FIRRTL:360294 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T = shr(io.addr, 3)
[51] FIRRTL:360295 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_1 = shl(io.pmp[6].addr, 2)
[52] FIRRTL:360296 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_2 = not(_res_hit_msbsLess_T_1)
[53] FIRRTL:360297 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_3 = or(_res_hit_msbsLess_T_2, UInt<2>(0h3))
[54] FIRRTL:360298 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_4 = not(_res_hit_msbsLess_T_3)
[55] FIRRTL:360299 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_5 = shr(_res_hit_msbsLess_T_4, 3)
[56] FIRRTL:360300 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess = lt(_res_hit_msbsLess_T, _res_hit_msbsLess_T_5)
[57] FIRRTL:360301 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T = shr(io.addr, 3)
[58] FIRRTL:360302 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_1 = shl(io.pmp[6].addr, 2)
[59] FIRRTL:360303 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_2 = not(_res_hit_msbsEqual_T_1)
[60] FIRRTL:360304 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_3 = or(_res_hit_msbsEqual_T_2, UInt<2>(0h3))
[61] FIRRTL:360305 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_4 = not(_res_hit_msbsEqual_T_3)
[62] FIRRTL:360306 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_5 = shr(_res_hit_msbsEqual_T_4, 3)
[63] FIRRTL:360307 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_6 = xor(_res_hit_msbsEqual_T, _res_hit_msbsEqual_T_5)
[64] FIRRTL:360308 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual = eq(_res_hit_msbsEqual_T_6, UInt<1>(0h0))
[65] FIRRTL:360309 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T = bits(io.addr, 2, 0)
[66] FIRRTL:360310 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_1 = or(_res_hit_lsbsLess_T, _res_hit_T_5)
[67] FIRRTL:360311 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_2 = shl(io.pmp[6].addr, 2)
[68] FIRRTL:360312 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_3 = not(_res_hit_lsbsLess_T_2)
[69] FIRRTL:360313 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_4 = or(_res_hit_lsbsLess_T_3, UInt<2>(0h3))
[70] FIRRTL:360314 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_5 = not(_res_hit_lsbsLess_T_4)
[71] FIRRTL:360315 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_6 = bits(_res_hit_lsbsLess_T_5, 2, 0)
[72] FIRRTL:360316 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess = lt(_res_hit_lsbsLess_T_1, _res_hit_lsbsLess_T_6)
[73] FIRRTL:360317 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_6 = and(res_hit_msbsEqual, res_hit_lsbsLess)
[74] FIRRTL:360318 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_7 = or(res_hit_msbsLess, _res_hit_T_6)
[75] FIRRTL:360319 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_8 = eq(_res_hit_T_7, UInt<1>(0h0))
[76] FIRRTL:360320 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_6 = shr(io.addr, 3)
[77] FIRRTL:360321 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_7 = shl(io.pmp[7].addr, 2)
[78] FIRRTL:360322 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_8 = not(_res_hit_msbsLess_T_7)
[79] FIRRTL:360323 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_9 = or(_res_hit_msbsLess_T_8, UInt<2>(0h3))
[80] FIRRTL:360324 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_10 = not(_res_hit_msbsLess_T_9)
[81] FIRRTL:360325 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_11 = shr(_res_hit_msbsLess_T_10, 3)
[82] FIRRTL:360326 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_1 = lt(_res_hit_msbsLess_T_6, _res_hit_msbsLess_T_11)
[83] FIRRTL:360327 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_7 = shr(io.addr, 3)
[84] FIRRTL:360328 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_8 = shl(io.pmp[7].addr, 2)
[85] FIRRTL:360329 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_9 = not(_res_hit_msbsEqual_T_8)
[86] FIRRTL:360330 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_10 = or(_res_hit_msbsEqual_T_9, UInt<2>(0h3))
[87] FIRRTL:360331 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_11 = not(_res_hit_msbsEqual_T_10)
[88] FIRRTL:360332 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_12 = shr(_res_hit_msbsEqual_T_11, 3)
[89] FIRRTL:360333 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_13 = xor(_res_hit_msbsEqual_T_7, _res_hit_msbsEqual_T_12)
[90] FIRRTL:360334 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_1 = eq(_res_hit_msbsEqual_T_13, UInt<1>(0h0))
[91] FIRRTL:360335 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_7 = bits(io.addr, 2, 0)
[92] FIRRTL:360336 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_8 = or(_res_hit_lsbsLess_T_7, UInt<1>(0h0))
[93] FIRRTL:360337 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_9 = shl(io.pmp[7].addr, 2)
[94] FIRRTL:360338 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_10 = not(_res_hit_lsbsLess_T_9)
[95] FIRRTL:360339 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_11 = or(_res_hit_lsbsLess_T_10, UInt<2>(0h3))
[96] FIRRTL:360340 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_12 = not(_res_hit_lsbsLess_T_11)
[97] FIRRTL:360341 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_13 = bits(_res_hit_lsbsLess_T_12, 2, 0)
[98] FIRRTL:360342 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_1 = lt(_res_hit_lsbsLess_T_8, _res_hit_lsbsLess_T_13)
[99] FIRRTL:360343 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_9 = and(res_hit_msbsEqual_1, res_hit_lsbsLess_1)
[100] FIRRTL:360344 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_10 = or(res_hit_msbsLess_1, _res_hit_T_9)
[101] FIRRTL:360345 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_11 = and(_res_hit_T_8, _res_hit_T_10)
[102] FIRRTL:360346 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_12 = and(_res_hit_T_2, _res_hit_T_11)
[103] FIRRTL:360347 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit = mux(_res_hit_T, _res_hit_T_1, _res_hit_T_12)
[104] FIRRTL:360348 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T = eq(io.pmp[7].cfg.l, UInt<1>(0h0))
[105] FIRRTL:360349 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore = and(default, _res_ignore_T)
[106] FIRRTL:360350 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T = dshl(UInt<3>(0h7), io.size)
[107] FIRRTL:360351 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_1 = bits(_res_aligned_lsbMask_T, 2, 0)
[108] FIRRTL:360352 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask = not(_res_aligned_lsbMask_T_1)
[109] FIRRTL:360353 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T = shr(io.addr, 3)
[110] FIRRTL:360354 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_1 = shl(io.pmp[6].addr, 2)
[111] FIRRTL:360355 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_2 = not(_res_aligned_straddlesLowerBound_T_1)
[112] FIRRTL:360356 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_3 = or(_res_aligned_straddlesLowerBound_T_2, UInt<2>(0h3))
[113] FIRRTL:360357 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_4 = not(_res_aligned_straddlesLowerBound_T_3)
[114] FIRRTL:360358 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_5 = shr(_res_aligned_straddlesLowerBound_T_4, 3)
[115] FIRRTL:360359 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_6 = xor(_res_aligned_straddlesLowerBound_T, _res_aligned_straddlesLowerBound_T_5)
[116] FIRRTL:360360 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_7 = eq(_res_aligned_straddlesLowerBound_T_6, UInt<1>(0h0))
[117] FIRRTL:360361 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_8 = shl(io.pmp[6].addr, 2)
[118] FIRRTL:360362 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_9 = not(_res_aligned_straddlesLowerBound_T_8)
[119] FIRRTL:360363 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_10 = or(_res_aligned_straddlesLowerBound_T_9, UInt<2>(0h3))
[120] FIRRTL:360364 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_11 = not(_res_aligned_straddlesLowerBound_T_10)
[121] FIRRTL:360365 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_12 = bits(_res_aligned_straddlesLowerBound_T_11, 2, 0)
[122] FIRRTL:360366 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_13 = bits(io.addr, 2, 0)
[123] FIRRTL:360367 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_14 = not(_res_aligned_straddlesLowerBound_T_13)
[124] FIRRTL:360368 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_15 = and(_res_aligned_straddlesLowerBound_T_12, _res_aligned_straddlesLowerBound_T_14)
[125] FIRRTL:360369 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_16 = neq(_res_aligned_straddlesLowerBound_T_15, UInt<1>(0h0))
[126] FIRRTL:360370 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound = and(_res_aligned_straddlesLowerBound_T_7, _res_aligned_straddlesLowerBound_T_16)
[127] FIRRTL:360371 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T = shr(io.addr, 3)
[128] FIRRTL:360372 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_1 = shl(io.pmp[7].addr, 2)
[129] FIRRTL:360373 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_2 = not(_res_aligned_straddlesUpperBound_T_1)
[130] FIRRTL:360374 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_3 = or(_res_aligned_straddlesUpperBound_T_2, UInt<2>(0h3))
[131] FIRRTL:360375 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_4 = not(_res_aligned_straddlesUpperBound_T_3)
[132] FIRRTL:360376 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_5 = shr(_res_aligned_straddlesUpperBound_T_4, 3)
[133] FIRRTL:360377 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_6 = xor(_res_aligned_straddlesUpperBound_T, _res_aligned_straddlesUpperBound_T_5)
[134] FIRRTL:360378 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_7 = eq(_res_aligned_straddlesUpperBound_T_6, UInt<1>(0h0))
[135] FIRRTL:360379 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_8 = shl(io.pmp[7].addr, 2)
[136] FIRRTL:360380 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_9 = not(_res_aligned_straddlesUpperBound_T_8)
[137] FIRRTL:360381 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_10 = or(_res_aligned_straddlesUpperBound_T_9, UInt<2>(0h3))
[138] FIRRTL:360382 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_11 = not(_res_aligned_straddlesUpperBound_T_10)
[139] FIRRTL:360383 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_12 = bits(_res_aligned_straddlesUpperBound_T_11, 2, 0)
[140] FIRRTL:360384 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_13 = bits(io.addr, 2, 0)
[141] FIRRTL:360385 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_14 = or(_res_aligned_straddlesUpperBound_T_13, res_aligned_lsbMask)
[142] FIRRTL:360386 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_15 = and(_res_aligned_straddlesUpperBound_T_12, _res_aligned_straddlesUpperBound_T_14)
[143] FIRRTL:360387 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_16 = neq(_res_aligned_straddlesUpperBound_T_15, UInt<1>(0h0))
[144] FIRRTL:360388 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound = and(_res_aligned_straddlesUpperBound_T_7, _res_aligned_straddlesUpperBound_T_16)
[145] FIRRTL:360389 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T = or(res_aligned_straddlesLowerBound, res_aligned_straddlesUpperBound)
[146] FIRRTL:360390 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned = eq(_res_aligned_rangeAligned_T, UInt<1>(0h0))
[147] FIRRTL:360391 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T = bits(io.pmp[7].mask, 2, 0)
[148] FIRRTL:360392 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_1 = not(_res_aligned_pow2Aligned_T)
[149] FIRRTL:360393 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_2 = and(res_aligned_lsbMask, _res_aligned_pow2Aligned_T_1)
[150] FIRRTL:360394 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned = eq(_res_aligned_pow2Aligned_T_2, UInt<1>(0h0))
[151] FIRRTL:360395 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T = bits(io.pmp[7].cfg.a, 1, 1)
[152] FIRRTL:360396 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned = mux(_res_aligned_T, res_aligned_pow2Aligned, res_aligned_rangeAligned)
[153] FIRRTL:360397 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T = eq(io.pmp[7].cfg.a, UInt<1>(0h0))
[154] FIRRTL:360398 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_1 = eq(io.pmp[7].cfg.a, UInt<1>(0h1))
[155] FIRRTL:360399 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_2 = eq(io.pmp[7].cfg.a, UInt<2>(0h2))
[156] FIRRTL:360400 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_3 = eq(io.pmp[7].cfg.a, UInt<2>(0h3))
[157] FIRRTL:360401 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_4 = eq(io.pmp[7].cfg.l, UInt<1>(0h1))
[158] FIRRTL:360402 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[159] FIRRTL:360403 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_5 = cat(res_hi, io.pmp[7].cfg.r)
[160] FIRRTL:360404 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_6 = eq(_res_T_5, UInt<1>(0h0))
[161] FIRRTL:360405 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_1 = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[162] FIRRTL:360406 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_7 = cat(res_hi_1, io.pmp[7].cfg.r)
[163] FIRRTL:360407 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_8 = eq(_res_T_7, UInt<1>(0h1))
[164] FIRRTL:360408 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_2 = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[165] FIRRTL:360409 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_9 = cat(res_hi_2, io.pmp[7].cfg.r)
[166] FIRRTL:360410 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_10 = eq(_res_T_9, UInt<2>(0h3))
[167] FIRRTL:360411 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_3 = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[168] FIRRTL:360412 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_11 = cat(res_hi_3, io.pmp[7].cfg.r)
[169] FIRRTL:360413 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_12 = eq(_res_T_11, UInt<3>(0h4))
[170] FIRRTL:360414 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_4 = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[171] FIRRTL:360415 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_13 = cat(res_hi_4, io.pmp[7].cfg.r)
[172] FIRRTL:360416 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_14 = eq(_res_T_13, UInt<3>(0h5))
[173] FIRRTL:360417 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_5 = cat(io.pmp[7].cfg.x, io.pmp[7].cfg.w)
[174] FIRRTL:360418 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_15 = cat(res_hi_5, io.pmp[7].cfg.r)
[175] FIRRTL:360419 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_16 = eq(_res_T_15, UInt<3>(0h7))
[176] FIRRTL:360420 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_17 = eq(res_ignore, UInt<1>(0h0))
[177] FIRRTL:360421 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_18 = and(_res_T_17, res_hit)
[178] FIRRTL:360422 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_19 = and(_res_T_18, res_aligned)
[179] FIRRTL:360423 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_20 = eq(io.pmp[7].cfg.a, UInt<1>(0h1))
[180] FIRRTL:360424 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_21 = and(_res_T_19, _res_T_20)
[181] FIRRTL:360425 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_22 = and(io.pmp[7].cfg.l, res_hit)
[182] FIRRTL:360426 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_23 = and(_res_T_22, res_aligned)
[183] FIRRTL:360427 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_24 = eq(io.pmp[7].cfg.a, UInt<1>(0h1))
[184] FIRRTL:360428 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_25 = and(_res_T_23, _res_T_24)
[185] FIRRTL:360429 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_26 = eq(res_ignore, UInt<1>(0h0))
[186] FIRRTL:360430 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_27 = and(_res_T_26, res_hit)
[187] FIRRTL:360431 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_28 = and(_res_T_27, res_aligned)
[188] FIRRTL:360432 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_29 = eq(io.pmp[7].cfg.a, UInt<2>(0h2))
[189] FIRRTL:360433 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_30 = and(_res_T_28, _res_T_29)
[190] FIRRTL:360434 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_31 = and(io.pmp[7].cfg.l, res_hit)
[191] FIRRTL:360435 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_32 = and(_res_T_31, res_aligned)
[192] FIRRTL:360436 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_33 = eq(io.pmp[7].cfg.a, UInt<2>(0h2))
[193] FIRRTL:360437 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_34 = and(_res_T_32, _res_T_33)
[194] FIRRTL:360438 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_35 = eq(res_ignore, UInt<1>(0h0))
[195] FIRRTL:360439 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_36 = and(_res_T_35, res_hit)
[196] FIRRTL:360440 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_37 = and(_res_T_36, res_aligned)
[197] FIRRTL:360441 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_38 = eq(io.pmp[7].cfg.a, UInt<2>(0h3))
[198] FIRRTL:360442 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_39 = and(_res_T_37, _res_T_38)
[199] FIRRTL:360443 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_40 = and(io.pmp[7].cfg.l, res_hit)
[200] FIRRTL:360444 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_41 = and(_res_T_40, res_aligned)
[201] FIRRTL:360445 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_42 = eq(io.pmp[7].cfg.a, UInt<2>(0h3))
[202] FIRRTL:360446 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_43 = and(_res_T_41, _res_T_42)
[203] FIRRTL:360447 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[204] FIRRTL:360448 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur, io.pmp[7]
[205] FIRRTL:360449 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T = or(io.pmp[7].cfg.r, res_ignore)
[206] FIRRTL:360450 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_1 = and(res_aligned, _res_cur_cfg_r_T)
[207] FIRRTL:360451 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur.cfg.r, _res_cur_cfg_r_T_1
[208] FIRRTL:360452 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T = or(io.pmp[7].cfg.w, res_ignore)
[209] FIRRTL:360453 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_1 = and(res_aligned, _res_cur_cfg_w_T)
[210] FIRRTL:360454 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur.cfg.w, _res_cur_cfg_w_T_1
[211] FIRRTL:360455 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T = or(io.pmp[7].cfg.x, res_ignore)
[212] FIRRTL:360456 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_1 = and(res_aligned, _res_cur_cfg_x_T)
[213] FIRRTL:360457 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur.cfg.x, _res_cur_cfg_x_T_1
[214] FIRRTL:360458 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_44 = mux(res_hit, res_cur, pmp0)
[215] FIRRTL:360459 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_13 = bits(io.pmp[6].cfg.a, 1, 1)
[216] FIRRTL:360460 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_3 = dshl(UInt<3>(0h7), io.size)
[217] FIRRTL:360461 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_4 = bits(_res_hit_lsbMask_T_3, 2, 0)
[218] FIRRTL:360462 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_5 = not(_res_hit_lsbMask_T_4)
[219] FIRRTL:360463 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_1 = or(io.pmp[6].mask, _res_hit_lsbMask_T_5)
[220] FIRRTL:360464 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_10 = shr(io.addr, 3)
[221] FIRRTL:360465 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_11 = shl(io.pmp[6].addr, 2)
[222] FIRRTL:360466 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_12 = not(_res_hit_msbMatch_T_11)
[223] FIRRTL:360467 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_13 = or(_res_hit_msbMatch_T_12, UInt<2>(0h3))
[224] FIRRTL:360468 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_14 = not(_res_hit_msbMatch_T_13)
[225] FIRRTL:360469 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_15 = shr(_res_hit_msbMatch_T_14, 3)
[226] FIRRTL:360470 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_16 = shr(io.pmp[6].mask, 3)
[227] FIRRTL:360471 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_17 = xor(_res_hit_msbMatch_T_10, _res_hit_msbMatch_T_15)
[228] FIRRTL:360472 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_18 = not(_res_hit_msbMatch_T_16)
[229] FIRRTL:360473 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_19 = and(_res_hit_msbMatch_T_17, _res_hit_msbMatch_T_18)
[230] FIRRTL:360474 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_1 = eq(_res_hit_msbMatch_T_19, UInt<1>(0h0))
[231] FIRRTL:360475 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_10 = bits(io.addr, 2, 0)
[232] FIRRTL:360476 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_11 = shl(io.pmp[6].addr, 2)
[233] FIRRTL:360477 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_12 = not(_res_hit_lsbMatch_T_11)
[234] FIRRTL:360478 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_13 = or(_res_hit_lsbMatch_T_12, UInt<2>(0h3))
[235] FIRRTL:360479 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_14 = not(_res_hit_lsbMatch_T_13)
[236] FIRRTL:360480 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_15 = bits(_res_hit_lsbMatch_T_14, 2, 0)
[237] FIRRTL:360481 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_16 = bits(res_hit_lsbMask_1, 2, 0)
[238] FIRRTL:360482 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_17 = xor(_res_hit_lsbMatch_T_10, _res_hit_lsbMatch_T_15)
[239] FIRRTL:360483 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_18 = not(_res_hit_lsbMatch_T_16)
[240] FIRRTL:360484 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_19 = and(_res_hit_lsbMatch_T_17, _res_hit_lsbMatch_T_18)
[241] FIRRTL:360485 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_1 = eq(_res_hit_lsbMatch_T_19, UInt<1>(0h0))
[242] FIRRTL:360486 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_14 = and(res_hit_msbMatch_1, res_hit_lsbMatch_1)
[243] FIRRTL:360487 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_15 = bits(io.pmp[6].cfg.a, 0, 0)
[244] FIRRTL:360488 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_16 = dshl(UInt<3>(0h7), io.size)
[245] FIRRTL:360489 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_17 = bits(_res_hit_T_16, 2, 0)
[246] FIRRTL:360490 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_18 = not(_res_hit_T_17)
[247] FIRRTL:360491 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_12 = shr(io.addr, 3)
[248] FIRRTL:360492 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_13 = shl(io.pmp[5].addr, 2)
[249] FIRRTL:360493 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_14 = not(_res_hit_msbsLess_T_13)
[250] FIRRTL:360494 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_15 = or(_res_hit_msbsLess_T_14, UInt<2>(0h3))
[251] FIRRTL:360495 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_16 = not(_res_hit_msbsLess_T_15)
[252] FIRRTL:360496 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_17 = shr(_res_hit_msbsLess_T_16, 3)
[253] FIRRTL:360497 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_2 = lt(_res_hit_msbsLess_T_12, _res_hit_msbsLess_T_17)
[254] FIRRTL:360498 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_14 = shr(io.addr, 3)
[255] FIRRTL:360499 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_15 = shl(io.pmp[5].addr, 2)
[256] FIRRTL:360500 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_16 = not(_res_hit_msbsEqual_T_15)
[257] FIRRTL:360501 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_17 = or(_res_hit_msbsEqual_T_16, UInt<2>(0h3))
[258] FIRRTL:360502 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_18 = not(_res_hit_msbsEqual_T_17)
[259] FIRRTL:360503 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_19 = shr(_res_hit_msbsEqual_T_18, 3)
[260] FIRRTL:360504 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_20 = xor(_res_hit_msbsEqual_T_14, _res_hit_msbsEqual_T_19)
[261] FIRRTL:360505 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_2 = eq(_res_hit_msbsEqual_T_20, UInt<1>(0h0))
[262] FIRRTL:360506 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_14 = bits(io.addr, 2, 0)
[263] FIRRTL:360507 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_15 = or(_res_hit_lsbsLess_T_14, _res_hit_T_18)
[264] FIRRTL:360508 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_16 = shl(io.pmp[5].addr, 2)
[265] FIRRTL:360509 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_17 = not(_res_hit_lsbsLess_T_16)
[266] FIRRTL:360510 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_18 = or(_res_hit_lsbsLess_T_17, UInt<2>(0h3))
[267] FIRRTL:360511 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_19 = not(_res_hit_lsbsLess_T_18)
[268] FIRRTL:360512 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_20 = bits(_res_hit_lsbsLess_T_19, 2, 0)
[269] FIRRTL:360513 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_2 = lt(_res_hit_lsbsLess_T_15, _res_hit_lsbsLess_T_20)
[270] FIRRTL:360514 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_19 = and(res_hit_msbsEqual_2, res_hit_lsbsLess_2)
[271] FIRRTL:360515 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_20 = or(res_hit_msbsLess_2, _res_hit_T_19)
[272] FIRRTL:360516 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_21 = eq(_res_hit_T_20, UInt<1>(0h0))
[273] FIRRTL:360517 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_18 = shr(io.addr, 3)
[274] FIRRTL:360518 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_19 = shl(io.pmp[6].addr, 2)
[275] FIRRTL:360519 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_20 = not(_res_hit_msbsLess_T_19)
[276] FIRRTL:360520 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_21 = or(_res_hit_msbsLess_T_20, UInt<2>(0h3))
[277] FIRRTL:360521 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_22 = not(_res_hit_msbsLess_T_21)
[278] FIRRTL:360522 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_23 = shr(_res_hit_msbsLess_T_22, 3)
[279] FIRRTL:360523 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_3 = lt(_res_hit_msbsLess_T_18, _res_hit_msbsLess_T_23)
[280] FIRRTL:360524 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_21 = shr(io.addr, 3)
[281] FIRRTL:360525 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_22 = shl(io.pmp[6].addr, 2)
[282] FIRRTL:360526 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_23 = not(_res_hit_msbsEqual_T_22)
[283] FIRRTL:360527 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_24 = or(_res_hit_msbsEqual_T_23, UInt<2>(0h3))
[284] FIRRTL:360528 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_25 = not(_res_hit_msbsEqual_T_24)
[285] FIRRTL:360529 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_26 = shr(_res_hit_msbsEqual_T_25, 3)
[286] FIRRTL:360530 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_27 = xor(_res_hit_msbsEqual_T_21, _res_hit_msbsEqual_T_26)
[287] FIRRTL:360531 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_3 = eq(_res_hit_msbsEqual_T_27, UInt<1>(0h0))
[288] FIRRTL:360532 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_21 = bits(io.addr, 2, 0)
[289] FIRRTL:360533 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_22 = or(_res_hit_lsbsLess_T_21, UInt<1>(0h0))
[290] FIRRTL:360534 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_23 = shl(io.pmp[6].addr, 2)
[291] FIRRTL:360535 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_24 = not(_res_hit_lsbsLess_T_23)
[292] FIRRTL:360536 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_25 = or(_res_hit_lsbsLess_T_24, UInt<2>(0h3))
[293] FIRRTL:360537 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_26 = not(_res_hit_lsbsLess_T_25)
[294] FIRRTL:360538 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_27 = bits(_res_hit_lsbsLess_T_26, 2, 0)
[295] FIRRTL:360539 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_3 = lt(_res_hit_lsbsLess_T_22, _res_hit_lsbsLess_T_27)
[296] FIRRTL:360540 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_22 = and(res_hit_msbsEqual_3, res_hit_lsbsLess_3)
[297] FIRRTL:360541 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_23 = or(res_hit_msbsLess_3, _res_hit_T_22)
[298] FIRRTL:360542 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_24 = and(_res_hit_T_21, _res_hit_T_23)
[299] FIRRTL:360543 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_25 = and(_res_hit_T_15, _res_hit_T_24)
[300] FIRRTL:360544 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_1 = mux(_res_hit_T_13, _res_hit_T_14, _res_hit_T_25)
[301] FIRRTL:360545 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_1 = eq(io.pmp[6].cfg.l, UInt<1>(0h0))
[302] FIRRTL:360546 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_1 = and(default, _res_ignore_T_1)
[303] FIRRTL:360547 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_2 = dshl(UInt<3>(0h7), io.size)
[304] FIRRTL:360548 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_3 = bits(_res_aligned_lsbMask_T_2, 2, 0)
[305] FIRRTL:360549 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_1 = not(_res_aligned_lsbMask_T_3)
[306] FIRRTL:360550 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_17 = shr(io.addr, 3)
[307] FIRRTL:360551 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_18 = shl(io.pmp[5].addr, 2)
[308] FIRRTL:360552 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_19 = not(_res_aligned_straddlesLowerBound_T_18)
[309] FIRRTL:360553 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_20 = or(_res_aligned_straddlesLowerBound_T_19, UInt<2>(0h3))
[310] FIRRTL:360554 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_21 = not(_res_aligned_straddlesLowerBound_T_20)
[311] FIRRTL:360555 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_22 = shr(_res_aligned_straddlesLowerBound_T_21, 3)
[312] FIRRTL:360556 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_23 = xor(_res_aligned_straddlesLowerBound_T_17, _res_aligned_straddlesLowerBound_T_22)
[313] FIRRTL:360557 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_24 = eq(_res_aligned_straddlesLowerBound_T_23, UInt<1>(0h0))
[314] FIRRTL:360558 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_25 = shl(io.pmp[5].addr, 2)
[315] FIRRTL:360559 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_26 = not(_res_aligned_straddlesLowerBound_T_25)
[316] FIRRTL:360560 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_27 = or(_res_aligned_straddlesLowerBound_T_26, UInt<2>(0h3))
[317] FIRRTL:360561 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_28 = not(_res_aligned_straddlesLowerBound_T_27)
[318] FIRRTL:360562 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_29 = bits(_res_aligned_straddlesLowerBound_T_28, 2, 0)
[319] FIRRTL:360563 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_30 = bits(io.addr, 2, 0)
[320] FIRRTL:360564 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_31 = not(_res_aligned_straddlesLowerBound_T_30)
[321] FIRRTL:360565 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_32 = and(_res_aligned_straddlesLowerBound_T_29, _res_aligned_straddlesLowerBound_T_31)
[322] FIRRTL:360566 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_33 = neq(_res_aligned_straddlesLowerBound_T_32, UInt<1>(0h0))
[323] FIRRTL:360567 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_1 = and(_res_aligned_straddlesLowerBound_T_24, _res_aligned_straddlesLowerBound_T_33)
[324] FIRRTL:360568 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_17 = shr(io.addr, 3)
[325] FIRRTL:360569 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_18 = shl(io.pmp[6].addr, 2)
[326] FIRRTL:360570 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_19 = not(_res_aligned_straddlesUpperBound_T_18)
[327] FIRRTL:360571 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_20 = or(_res_aligned_straddlesUpperBound_T_19, UInt<2>(0h3))
[328] FIRRTL:360572 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_21 = not(_res_aligned_straddlesUpperBound_T_20)
[329] FIRRTL:360573 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_22 = shr(_res_aligned_straddlesUpperBound_T_21, 3)
[330] FIRRTL:360574 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_23 = xor(_res_aligned_straddlesUpperBound_T_17, _res_aligned_straddlesUpperBound_T_22)
[331] FIRRTL:360575 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_24 = eq(_res_aligned_straddlesUpperBound_T_23, UInt<1>(0h0))
[332] FIRRTL:360576 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_25 = shl(io.pmp[6].addr, 2)
[333] FIRRTL:360577 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_26 = not(_res_aligned_straddlesUpperBound_T_25)
[334] FIRRTL:360578 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_27 = or(_res_aligned_straddlesUpperBound_T_26, UInt<2>(0h3))
[335] FIRRTL:360579 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_28 = not(_res_aligned_straddlesUpperBound_T_27)
[336] FIRRTL:360580 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_29 = bits(_res_aligned_straddlesUpperBound_T_28, 2, 0)
[337] FIRRTL:360581 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_30 = bits(io.addr, 2, 0)
[338] FIRRTL:360582 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_31 = or(_res_aligned_straddlesUpperBound_T_30, res_aligned_lsbMask_1)
[339] FIRRTL:360583 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_32 = and(_res_aligned_straddlesUpperBound_T_29, _res_aligned_straddlesUpperBound_T_31)
[340] FIRRTL:360584 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_33 = neq(_res_aligned_straddlesUpperBound_T_32, UInt<1>(0h0))
[341] FIRRTL:360585 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_1 = and(_res_aligned_straddlesUpperBound_T_24, _res_aligned_straddlesUpperBound_T_33)
[342] FIRRTL:360586 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_1 = or(res_aligned_straddlesLowerBound_1, res_aligned_straddlesUpperBound_1)
[343] FIRRTL:360587 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_1 = eq(_res_aligned_rangeAligned_T_1, UInt<1>(0h0))
[344] FIRRTL:360588 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_3 = bits(io.pmp[6].mask, 2, 0)
[345] FIRRTL:360589 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_4 = not(_res_aligned_pow2Aligned_T_3)
[346] FIRRTL:360590 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_5 = and(res_aligned_lsbMask_1, _res_aligned_pow2Aligned_T_4)
[347] FIRRTL:360591 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_1 = eq(_res_aligned_pow2Aligned_T_5, UInt<1>(0h0))
[348] FIRRTL:360592 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_1 = bits(io.pmp[6].cfg.a, 1, 1)
[349] FIRRTL:360593 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_1 = mux(_res_aligned_T_1, res_aligned_pow2Aligned_1, res_aligned_rangeAligned_1)
[350] FIRRTL:360594 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_45 = eq(io.pmp[6].cfg.a, UInt<1>(0h0))
[351] FIRRTL:360595 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_46 = eq(io.pmp[6].cfg.a, UInt<1>(0h1))
[352] FIRRTL:360596 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_47 = eq(io.pmp[6].cfg.a, UInt<2>(0h2))
[353] FIRRTL:360597 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_48 = eq(io.pmp[6].cfg.a, UInt<2>(0h3))
[354] FIRRTL:360598 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_49 = eq(io.pmp[6].cfg.l, UInt<1>(0h1))
[355] FIRRTL:360599 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_6 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[356] FIRRTL:360600 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_50 = cat(res_hi_6, io.pmp[6].cfg.r)
[357] FIRRTL:360601 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_51 = eq(_res_T_50, UInt<1>(0h0))
[358] FIRRTL:360602 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_7 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[359] FIRRTL:360603 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_52 = cat(res_hi_7, io.pmp[6].cfg.r)
[360] FIRRTL:360604 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_53 = eq(_res_T_52, UInt<1>(0h1))
[361] FIRRTL:360605 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_8 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[362] FIRRTL:360606 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_54 = cat(res_hi_8, io.pmp[6].cfg.r)
[363] FIRRTL:360607 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_55 = eq(_res_T_54, UInt<2>(0h3))
[364] FIRRTL:360608 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_9 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[365] FIRRTL:360609 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_56 = cat(res_hi_9, io.pmp[6].cfg.r)
[366] FIRRTL:360610 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_57 = eq(_res_T_56, UInt<3>(0h4))
[367] FIRRTL:360611 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_10 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[368] FIRRTL:360612 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_58 = cat(res_hi_10, io.pmp[6].cfg.r)
[369] FIRRTL:360613 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_59 = eq(_res_T_58, UInt<3>(0h5))
[370] FIRRTL:360614 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_11 = cat(io.pmp[6].cfg.x, io.pmp[6].cfg.w)
[371] FIRRTL:360615 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_60 = cat(res_hi_11, io.pmp[6].cfg.r)
[372] FIRRTL:360616 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_61 = eq(_res_T_60, UInt<3>(0h7))
[373] FIRRTL:360617 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_62 = eq(res_ignore_1, UInt<1>(0h0))
[374] FIRRTL:360618 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_63 = and(_res_T_62, res_hit_1)
[375] FIRRTL:360619 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_64 = and(_res_T_63, res_aligned_1)
[376] FIRRTL:360620 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_65 = eq(io.pmp[6].cfg.a, UInt<1>(0h1))
[377] FIRRTL:360621 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_66 = and(_res_T_64, _res_T_65)
[378] FIRRTL:360622 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_67 = and(io.pmp[6].cfg.l, res_hit_1)
[379] FIRRTL:360623 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_68 = and(_res_T_67, res_aligned_1)
[380] FIRRTL:360624 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_69 = eq(io.pmp[6].cfg.a, UInt<1>(0h1))
[381] FIRRTL:360625 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_70 = and(_res_T_68, _res_T_69)
[382] FIRRTL:360626 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_71 = eq(res_ignore_1, UInt<1>(0h0))
[383] FIRRTL:360627 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_72 = and(_res_T_71, res_hit_1)
[384] FIRRTL:360628 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_73 = and(_res_T_72, res_aligned_1)
[385] FIRRTL:360629 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_74 = eq(io.pmp[6].cfg.a, UInt<2>(0h2))
[386] FIRRTL:360630 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_75 = and(_res_T_73, _res_T_74)
[387] FIRRTL:360631 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_76 = and(io.pmp[6].cfg.l, res_hit_1)
[388] FIRRTL:360632 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_77 = and(_res_T_76, res_aligned_1)
[389] FIRRTL:360633 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_78 = eq(io.pmp[6].cfg.a, UInt<2>(0h2))
[390] FIRRTL:360634 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_79 = and(_res_T_77, _res_T_78)
[391] FIRRTL:360635 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_80 = eq(res_ignore_1, UInt<1>(0h0))
[392] FIRRTL:360636 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_81 = and(_res_T_80, res_hit_1)
[393] FIRRTL:360637 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_82 = and(_res_T_81, res_aligned_1)
[394] FIRRTL:360638 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_83 = eq(io.pmp[6].cfg.a, UInt<2>(0h3))
[395] FIRRTL:360639 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_84 = and(_res_T_82, _res_T_83)
[396] FIRRTL:360640 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_85 = and(io.pmp[6].cfg.l, res_hit_1)
[397] FIRRTL:360641 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_86 = and(_res_T_85, res_aligned_1)
[398] FIRRTL:360642 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_87 = eq(io.pmp[6].cfg.a, UInt<2>(0h3))
[399] FIRRTL:360643 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_88 = and(_res_T_86, _res_T_87)
[400] FIRRTL:360644 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_1 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[401] FIRRTL:360645 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_1, io.pmp[6]
[402] FIRRTL:360646 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_2 = or(io.pmp[6].cfg.r, res_ignore_1)
[403] FIRRTL:360647 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_3 = and(res_aligned_1, _res_cur_cfg_r_T_2)
[404] FIRRTL:360648 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_1.cfg.r, _res_cur_cfg_r_T_3
[405] FIRRTL:360649 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_2 = or(io.pmp[6].cfg.w, res_ignore_1)
[406] FIRRTL:360650 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_3 = and(res_aligned_1, _res_cur_cfg_w_T_2)
[407] FIRRTL:360651 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_1.cfg.w, _res_cur_cfg_w_T_3
[408] FIRRTL:360652 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_2 = or(io.pmp[6].cfg.x, res_ignore_1)
[409] FIRRTL:360653 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_3 = and(res_aligned_1, _res_cur_cfg_x_T_2)
[410] FIRRTL:360654 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_1.cfg.x, _res_cur_cfg_x_T_3
[411] FIRRTL:360655 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_89 = mux(res_hit_1, res_cur_1, _res_T_44)
[412] FIRRTL:360656 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_26 = bits(io.pmp[5].cfg.a, 1, 1)
[413] FIRRTL:360657 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_6 = dshl(UInt<3>(0h7), io.size)
[414] FIRRTL:360658 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_7 = bits(_res_hit_lsbMask_T_6, 2, 0)
[415] FIRRTL:360659 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_8 = not(_res_hit_lsbMask_T_7)
[416] FIRRTL:360660 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_2 = or(io.pmp[5].mask, _res_hit_lsbMask_T_8)
[417] FIRRTL:360661 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_20 = shr(io.addr, 3)
[418] FIRRTL:360662 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_21 = shl(io.pmp[5].addr, 2)
[419] FIRRTL:360663 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_22 = not(_res_hit_msbMatch_T_21)
[420] FIRRTL:360664 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_23 = or(_res_hit_msbMatch_T_22, UInt<2>(0h3))
[421] FIRRTL:360665 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_24 = not(_res_hit_msbMatch_T_23)
[422] FIRRTL:360666 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_25 = shr(_res_hit_msbMatch_T_24, 3)
[423] FIRRTL:360667 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_26 = shr(io.pmp[5].mask, 3)
[424] FIRRTL:360668 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_27 = xor(_res_hit_msbMatch_T_20, _res_hit_msbMatch_T_25)
[425] FIRRTL:360669 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_28 = not(_res_hit_msbMatch_T_26)
[426] FIRRTL:360670 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_29 = and(_res_hit_msbMatch_T_27, _res_hit_msbMatch_T_28)
[427] FIRRTL:360671 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_2 = eq(_res_hit_msbMatch_T_29, UInt<1>(0h0))
[428] FIRRTL:360672 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_20 = bits(io.addr, 2, 0)
[429] FIRRTL:360673 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_21 = shl(io.pmp[5].addr, 2)
[430] FIRRTL:360674 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_22 = not(_res_hit_lsbMatch_T_21)
[431] FIRRTL:360675 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_23 = or(_res_hit_lsbMatch_T_22, UInt<2>(0h3))
[432] FIRRTL:360676 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_24 = not(_res_hit_lsbMatch_T_23)
[433] FIRRTL:360677 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_25 = bits(_res_hit_lsbMatch_T_24, 2, 0)
[434] FIRRTL:360678 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_26 = bits(res_hit_lsbMask_2, 2, 0)
[435] FIRRTL:360679 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_27 = xor(_res_hit_lsbMatch_T_20, _res_hit_lsbMatch_T_25)
[436] FIRRTL:360680 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_28 = not(_res_hit_lsbMatch_T_26)
[437] FIRRTL:360681 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_29 = and(_res_hit_lsbMatch_T_27, _res_hit_lsbMatch_T_28)
[438] FIRRTL:360682 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_2 = eq(_res_hit_lsbMatch_T_29, UInt<1>(0h0))
[439] FIRRTL:360683 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_27 = and(res_hit_msbMatch_2, res_hit_lsbMatch_2)
[440] FIRRTL:360684 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_28 = bits(io.pmp[5].cfg.a, 0, 0)
[441] FIRRTL:360685 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_29 = dshl(UInt<3>(0h7), io.size)
[442] FIRRTL:360686 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_30 = bits(_res_hit_T_29, 2, 0)
[443] FIRRTL:360687 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_31 = not(_res_hit_T_30)
[444] FIRRTL:360688 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_24 = shr(io.addr, 3)
[445] FIRRTL:360689 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_25 = shl(io.pmp[4].addr, 2)
[446] FIRRTL:360690 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_26 = not(_res_hit_msbsLess_T_25)
[447] FIRRTL:360691 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_27 = or(_res_hit_msbsLess_T_26, UInt<2>(0h3))
[448] FIRRTL:360692 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_28 = not(_res_hit_msbsLess_T_27)
[449] FIRRTL:360693 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_29 = shr(_res_hit_msbsLess_T_28, 3)
[450] FIRRTL:360694 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_4 = lt(_res_hit_msbsLess_T_24, _res_hit_msbsLess_T_29)
[451] FIRRTL:360695 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_28 = shr(io.addr, 3)
[452] FIRRTL:360696 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_29 = shl(io.pmp[4].addr, 2)
[453] FIRRTL:360697 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_30 = not(_res_hit_msbsEqual_T_29)
[454] FIRRTL:360698 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_31 = or(_res_hit_msbsEqual_T_30, UInt<2>(0h3))
[455] FIRRTL:360699 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_32 = not(_res_hit_msbsEqual_T_31)
[456] FIRRTL:360700 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_33 = shr(_res_hit_msbsEqual_T_32, 3)
[457] FIRRTL:360701 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_34 = xor(_res_hit_msbsEqual_T_28, _res_hit_msbsEqual_T_33)
[458] FIRRTL:360702 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_4 = eq(_res_hit_msbsEqual_T_34, UInt<1>(0h0))
[459] FIRRTL:360703 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_28 = bits(io.addr, 2, 0)
[460] FIRRTL:360704 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_29 = or(_res_hit_lsbsLess_T_28, _res_hit_T_31)
[461] FIRRTL:360705 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_30 = shl(io.pmp[4].addr, 2)
[462] FIRRTL:360706 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_31 = not(_res_hit_lsbsLess_T_30)
[463] FIRRTL:360707 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_32 = or(_res_hit_lsbsLess_T_31, UInt<2>(0h3))
[464] FIRRTL:360708 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_33 = not(_res_hit_lsbsLess_T_32)
[465] FIRRTL:360709 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_34 = bits(_res_hit_lsbsLess_T_33, 2, 0)
[466] FIRRTL:360710 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_4 = lt(_res_hit_lsbsLess_T_29, _res_hit_lsbsLess_T_34)
[467] FIRRTL:360711 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_32 = and(res_hit_msbsEqual_4, res_hit_lsbsLess_4)
[468] FIRRTL:360712 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_33 = or(res_hit_msbsLess_4, _res_hit_T_32)
[469] FIRRTL:360713 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_34 = eq(_res_hit_T_33, UInt<1>(0h0))
[470] FIRRTL:360714 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_30 = shr(io.addr, 3)
[471] FIRRTL:360715 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_31 = shl(io.pmp[5].addr, 2)
[472] FIRRTL:360716 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_32 = not(_res_hit_msbsLess_T_31)
[473] FIRRTL:360717 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_33 = or(_res_hit_msbsLess_T_32, UInt<2>(0h3))
[474] FIRRTL:360718 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_34 = not(_res_hit_msbsLess_T_33)
[475] FIRRTL:360719 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_35 = shr(_res_hit_msbsLess_T_34, 3)
[476] FIRRTL:360720 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_5 = lt(_res_hit_msbsLess_T_30, _res_hit_msbsLess_T_35)
[477] FIRRTL:360721 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_35 = shr(io.addr, 3)
[478] FIRRTL:360722 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_36 = shl(io.pmp[5].addr, 2)
[479] FIRRTL:360723 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_37 = not(_res_hit_msbsEqual_T_36)
[480] FIRRTL:360724 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_38 = or(_res_hit_msbsEqual_T_37, UInt<2>(0h3))
[481] FIRRTL:360725 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_39 = not(_res_hit_msbsEqual_T_38)
[482] FIRRTL:360726 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_40 = shr(_res_hit_msbsEqual_T_39, 3)
[483] FIRRTL:360727 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_41 = xor(_res_hit_msbsEqual_T_35, _res_hit_msbsEqual_T_40)
[484] FIRRTL:360728 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_5 = eq(_res_hit_msbsEqual_T_41, UInt<1>(0h0))
[485] FIRRTL:360729 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_35 = bits(io.addr, 2, 0)
[486] FIRRTL:360730 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_36 = or(_res_hit_lsbsLess_T_35, UInt<1>(0h0))
[487] FIRRTL:360731 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_37 = shl(io.pmp[5].addr, 2)
[488] FIRRTL:360732 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_38 = not(_res_hit_lsbsLess_T_37)
[489] FIRRTL:360733 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_39 = or(_res_hit_lsbsLess_T_38, UInt<2>(0h3))
[490] FIRRTL:360734 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_40 = not(_res_hit_lsbsLess_T_39)
[491] FIRRTL:360735 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_41 = bits(_res_hit_lsbsLess_T_40, 2, 0)
[492] FIRRTL:360736 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_5 = lt(_res_hit_lsbsLess_T_36, _res_hit_lsbsLess_T_41)
[493] FIRRTL:360737 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_35 = and(res_hit_msbsEqual_5, res_hit_lsbsLess_5)
[494] FIRRTL:360738 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_36 = or(res_hit_msbsLess_5, _res_hit_T_35)
[495] FIRRTL:360739 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_37 = and(_res_hit_T_34, _res_hit_T_36)
[496] FIRRTL:360740 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_38 = and(_res_hit_T_28, _res_hit_T_37)
[497] FIRRTL:360741 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_2 = mux(_res_hit_T_26, _res_hit_T_27, _res_hit_T_38)
[498] FIRRTL:360742 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_2 = eq(io.pmp[5].cfg.l, UInt<1>(0h0))
[499] FIRRTL:360743 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_2 = and(default, _res_ignore_T_2)
[500] FIRRTL:360744 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_4 = dshl(UInt<3>(0h7), io.size)
[501] FIRRTL:360745 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_5 = bits(_res_aligned_lsbMask_T_4, 2, 0)
[502] FIRRTL:360746 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_2 = not(_res_aligned_lsbMask_T_5)
[503] FIRRTL:360747 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_34 = shr(io.addr, 3)
[504] FIRRTL:360748 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_35 = shl(io.pmp[4].addr, 2)
[505] FIRRTL:360749 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_36 = not(_res_aligned_straddlesLowerBound_T_35)
[506] FIRRTL:360750 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_37 = or(_res_aligned_straddlesLowerBound_T_36, UInt<2>(0h3))
[507] FIRRTL:360751 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_38 = not(_res_aligned_straddlesLowerBound_T_37)
[508] FIRRTL:360752 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_39 = shr(_res_aligned_straddlesLowerBound_T_38, 3)
[509] FIRRTL:360753 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_40 = xor(_res_aligned_straddlesLowerBound_T_34, _res_aligned_straddlesLowerBound_T_39)
[510] FIRRTL:360754 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_41 = eq(_res_aligned_straddlesLowerBound_T_40, UInt<1>(0h0))
[511] FIRRTL:360755 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_42 = shl(io.pmp[4].addr, 2)
[512] FIRRTL:360756 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_43 = not(_res_aligned_straddlesLowerBound_T_42)
[513] FIRRTL:360757 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_44 = or(_res_aligned_straddlesLowerBound_T_43, UInt<2>(0h3))
[514] FIRRTL:360758 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_45 = not(_res_aligned_straddlesLowerBound_T_44)
[515] FIRRTL:360759 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_46 = bits(_res_aligned_straddlesLowerBound_T_45, 2, 0)
[516] FIRRTL:360760 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_47 = bits(io.addr, 2, 0)
[517] FIRRTL:360761 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_48 = not(_res_aligned_straddlesLowerBound_T_47)
[518] FIRRTL:360762 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_49 = and(_res_aligned_straddlesLowerBound_T_46, _res_aligned_straddlesLowerBound_T_48)
[519] FIRRTL:360763 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_50 = neq(_res_aligned_straddlesLowerBound_T_49, UInt<1>(0h0))
[520] FIRRTL:360764 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_2 = and(_res_aligned_straddlesLowerBound_T_41, _res_aligned_straddlesLowerBound_T_50)
[521] FIRRTL:360765 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_34 = shr(io.addr, 3)
[522] FIRRTL:360766 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_35 = shl(io.pmp[5].addr, 2)
[523] FIRRTL:360767 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_36 = not(_res_aligned_straddlesUpperBound_T_35)
[524] FIRRTL:360768 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_37 = or(_res_aligned_straddlesUpperBound_T_36, UInt<2>(0h3))
[525] FIRRTL:360769 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_38 = not(_res_aligned_straddlesUpperBound_T_37)
[526] FIRRTL:360770 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_39 = shr(_res_aligned_straddlesUpperBound_T_38, 3)
[527] FIRRTL:360771 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_40 = xor(_res_aligned_straddlesUpperBound_T_34, _res_aligned_straddlesUpperBound_T_39)
[528] FIRRTL:360772 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_41 = eq(_res_aligned_straddlesUpperBound_T_40, UInt<1>(0h0))
[529] FIRRTL:360773 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_42 = shl(io.pmp[5].addr, 2)
[530] FIRRTL:360774 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_43 = not(_res_aligned_straddlesUpperBound_T_42)
[531] FIRRTL:360775 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_44 = or(_res_aligned_straddlesUpperBound_T_43, UInt<2>(0h3))
[532] FIRRTL:360776 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_45 = not(_res_aligned_straddlesUpperBound_T_44)
[533] FIRRTL:360777 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_46 = bits(_res_aligned_straddlesUpperBound_T_45, 2, 0)
[534] FIRRTL:360778 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_47 = bits(io.addr, 2, 0)
[535] FIRRTL:360779 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_48 = or(_res_aligned_straddlesUpperBound_T_47, res_aligned_lsbMask_2)
[536] FIRRTL:360780 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_49 = and(_res_aligned_straddlesUpperBound_T_46, _res_aligned_straddlesUpperBound_T_48)
[537] FIRRTL:360781 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_50 = neq(_res_aligned_straddlesUpperBound_T_49, UInt<1>(0h0))
[538] FIRRTL:360782 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_2 = and(_res_aligned_straddlesUpperBound_T_41, _res_aligned_straddlesUpperBound_T_50)
[539] FIRRTL:360783 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_2 = or(res_aligned_straddlesLowerBound_2, res_aligned_straddlesUpperBound_2)
[540] FIRRTL:360784 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_2 = eq(_res_aligned_rangeAligned_T_2, UInt<1>(0h0))
[541] FIRRTL:360785 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_6 = bits(io.pmp[5].mask, 2, 0)
[542] FIRRTL:360786 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_7 = not(_res_aligned_pow2Aligned_T_6)
[543] FIRRTL:360787 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_8 = and(res_aligned_lsbMask_2, _res_aligned_pow2Aligned_T_7)
[544] FIRRTL:360788 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_2 = eq(_res_aligned_pow2Aligned_T_8, UInt<1>(0h0))
[545] FIRRTL:360789 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_2 = bits(io.pmp[5].cfg.a, 1, 1)
[546] FIRRTL:360790 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_2 = mux(_res_aligned_T_2, res_aligned_pow2Aligned_2, res_aligned_rangeAligned_2)
[547] FIRRTL:360791 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_90 = eq(io.pmp[5].cfg.a, UInt<1>(0h0))
[548] FIRRTL:360792 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_91 = eq(io.pmp[5].cfg.a, UInt<1>(0h1))
[549] FIRRTL:360793 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_92 = eq(io.pmp[5].cfg.a, UInt<2>(0h2))
[550] FIRRTL:360794 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_93 = eq(io.pmp[5].cfg.a, UInt<2>(0h3))
[551] FIRRTL:360795 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_94 = eq(io.pmp[5].cfg.l, UInt<1>(0h1))
[552] FIRRTL:360796 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_12 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[553] FIRRTL:360797 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_95 = cat(res_hi_12, io.pmp[5].cfg.r)
[554] FIRRTL:360798 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_96 = eq(_res_T_95, UInt<1>(0h0))
[555] FIRRTL:360799 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_13 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[556] FIRRTL:360800 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_97 = cat(res_hi_13, io.pmp[5].cfg.r)
[557] FIRRTL:360801 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_98 = eq(_res_T_97, UInt<1>(0h1))
[558] FIRRTL:360802 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_14 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[559] FIRRTL:360803 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_99 = cat(res_hi_14, io.pmp[5].cfg.r)
[560] FIRRTL:360804 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_100 = eq(_res_T_99, UInt<2>(0h3))
[561] FIRRTL:360805 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_15 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[562] FIRRTL:360806 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_101 = cat(res_hi_15, io.pmp[5].cfg.r)
[563] FIRRTL:360807 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_102 = eq(_res_T_101, UInt<3>(0h4))
[564] FIRRTL:360808 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_16 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[565] FIRRTL:360809 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_103 = cat(res_hi_16, io.pmp[5].cfg.r)
[566] FIRRTL:360810 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_104 = eq(_res_T_103, UInt<3>(0h5))
[567] FIRRTL:360811 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_17 = cat(io.pmp[5].cfg.x, io.pmp[5].cfg.w)
[568] FIRRTL:360812 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_105 = cat(res_hi_17, io.pmp[5].cfg.r)
[569] FIRRTL:360813 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_106 = eq(_res_T_105, UInt<3>(0h7))
[570] FIRRTL:360814 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_107 = eq(res_ignore_2, UInt<1>(0h0))
[571] FIRRTL:360815 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_108 = and(_res_T_107, res_hit_2)
[572] FIRRTL:360816 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_109 = and(_res_T_108, res_aligned_2)
[573] FIRRTL:360817 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_110 = eq(io.pmp[5].cfg.a, UInt<1>(0h1))
[574] FIRRTL:360818 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_111 = and(_res_T_109, _res_T_110)
[575] FIRRTL:360819 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_112 = and(io.pmp[5].cfg.l, res_hit_2)
[576] FIRRTL:360820 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_113 = and(_res_T_112, res_aligned_2)
[577] FIRRTL:360821 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_114 = eq(io.pmp[5].cfg.a, UInt<1>(0h1))
[578] FIRRTL:360822 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_115 = and(_res_T_113, _res_T_114)
[579] FIRRTL:360823 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_116 = eq(res_ignore_2, UInt<1>(0h0))
[580] FIRRTL:360824 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_117 = and(_res_T_116, res_hit_2)
[581] FIRRTL:360825 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_118 = and(_res_T_117, res_aligned_2)
[582] FIRRTL:360826 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_119 = eq(io.pmp[5].cfg.a, UInt<2>(0h2))
[583] FIRRTL:360827 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_120 = and(_res_T_118, _res_T_119)
[584] FIRRTL:360828 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_121 = and(io.pmp[5].cfg.l, res_hit_2)
[585] FIRRTL:360829 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_122 = and(_res_T_121, res_aligned_2)
[586] FIRRTL:360830 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_123 = eq(io.pmp[5].cfg.a, UInt<2>(0h2))
[587] FIRRTL:360831 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_124 = and(_res_T_122, _res_T_123)
[588] FIRRTL:360832 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_125 = eq(res_ignore_2, UInt<1>(0h0))
[589] FIRRTL:360833 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_126 = and(_res_T_125, res_hit_2)
[590] FIRRTL:360834 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_127 = and(_res_T_126, res_aligned_2)
[591] FIRRTL:360835 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_128 = eq(io.pmp[5].cfg.a, UInt<2>(0h3))
[592] FIRRTL:360836 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_129 = and(_res_T_127, _res_T_128)
[593] FIRRTL:360837 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_130 = and(io.pmp[5].cfg.l, res_hit_2)
[594] FIRRTL:360838 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_131 = and(_res_T_130, res_aligned_2)
[595] FIRRTL:360839 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_132 = eq(io.pmp[5].cfg.a, UInt<2>(0h3))
[596] FIRRTL:360840 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_133 = and(_res_T_131, _res_T_132)
[597] FIRRTL:360841 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_2 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[598] FIRRTL:360842 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_2, io.pmp[5]
[599] FIRRTL:360843 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_4 = or(io.pmp[5].cfg.r, res_ignore_2)
[600] FIRRTL:360844 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_5 = and(res_aligned_2, _res_cur_cfg_r_T_4)
[601] FIRRTL:360845 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_2.cfg.r, _res_cur_cfg_r_T_5
[602] FIRRTL:360846 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_4 = or(io.pmp[5].cfg.w, res_ignore_2)
[603] FIRRTL:360847 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_5 = and(res_aligned_2, _res_cur_cfg_w_T_4)
[604] FIRRTL:360848 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_2.cfg.w, _res_cur_cfg_w_T_5
[605] FIRRTL:360849 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_4 = or(io.pmp[5].cfg.x, res_ignore_2)
[606] FIRRTL:360850 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_5 = and(res_aligned_2, _res_cur_cfg_x_T_4)
[607] FIRRTL:360851 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_2.cfg.x, _res_cur_cfg_x_T_5
[608] FIRRTL:360852 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_134 = mux(res_hit_2, res_cur_2, _res_T_89)
[609] FIRRTL:360853 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_39 = bits(io.pmp[4].cfg.a, 1, 1)
[610] FIRRTL:360854 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_9 = dshl(UInt<3>(0h7), io.size)
[611] FIRRTL:360855 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_10 = bits(_res_hit_lsbMask_T_9, 2, 0)
[612] FIRRTL:360856 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_11 = not(_res_hit_lsbMask_T_10)
[613] FIRRTL:360857 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_3 = or(io.pmp[4].mask, _res_hit_lsbMask_T_11)
[614] FIRRTL:360858 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_30 = shr(io.addr, 3)
[615] FIRRTL:360859 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_31 = shl(io.pmp[4].addr, 2)
[616] FIRRTL:360860 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_32 = not(_res_hit_msbMatch_T_31)
[617] FIRRTL:360861 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_33 = or(_res_hit_msbMatch_T_32, UInt<2>(0h3))
[618] FIRRTL:360862 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_34 = not(_res_hit_msbMatch_T_33)
[619] FIRRTL:360863 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_35 = shr(_res_hit_msbMatch_T_34, 3)
[620] FIRRTL:360864 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_36 = shr(io.pmp[4].mask, 3)
[621] FIRRTL:360865 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_37 = xor(_res_hit_msbMatch_T_30, _res_hit_msbMatch_T_35)
[622] FIRRTL:360866 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_38 = not(_res_hit_msbMatch_T_36)
[623] FIRRTL:360867 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_39 = and(_res_hit_msbMatch_T_37, _res_hit_msbMatch_T_38)
[624] FIRRTL:360868 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_3 = eq(_res_hit_msbMatch_T_39, UInt<1>(0h0))
[625] FIRRTL:360869 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_30 = bits(io.addr, 2, 0)
[626] FIRRTL:360870 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_31 = shl(io.pmp[4].addr, 2)
[627] FIRRTL:360871 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_32 = not(_res_hit_lsbMatch_T_31)
[628] FIRRTL:360872 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_33 = or(_res_hit_lsbMatch_T_32, UInt<2>(0h3))
[629] FIRRTL:360873 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_34 = not(_res_hit_lsbMatch_T_33)
[630] FIRRTL:360874 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_35 = bits(_res_hit_lsbMatch_T_34, 2, 0)
[631] FIRRTL:360875 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_36 = bits(res_hit_lsbMask_3, 2, 0)
[632] FIRRTL:360876 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_37 = xor(_res_hit_lsbMatch_T_30, _res_hit_lsbMatch_T_35)
[633] FIRRTL:360877 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_38 = not(_res_hit_lsbMatch_T_36)
[634] FIRRTL:360878 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_39 = and(_res_hit_lsbMatch_T_37, _res_hit_lsbMatch_T_38)
[635] FIRRTL:360879 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_3 = eq(_res_hit_lsbMatch_T_39, UInt<1>(0h0))
[636] FIRRTL:360880 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_40 = and(res_hit_msbMatch_3, res_hit_lsbMatch_3)
[637] FIRRTL:360881 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_41 = bits(io.pmp[4].cfg.a, 0, 0)
[638] FIRRTL:360882 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_42 = dshl(UInt<3>(0h7), io.size)
[639] FIRRTL:360883 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_43 = bits(_res_hit_T_42, 2, 0)
[640] FIRRTL:360884 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_44 = not(_res_hit_T_43)
[641] FIRRTL:360885 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_36 = shr(io.addr, 3)
[642] FIRRTL:360886 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_37 = shl(io.pmp[3].addr, 2)
[643] FIRRTL:360887 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_38 = not(_res_hit_msbsLess_T_37)
[644] FIRRTL:360888 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_39 = or(_res_hit_msbsLess_T_38, UInt<2>(0h3))
[645] FIRRTL:360889 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_40 = not(_res_hit_msbsLess_T_39)
[646] FIRRTL:360890 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_41 = shr(_res_hit_msbsLess_T_40, 3)
[647] FIRRTL:360891 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_6 = lt(_res_hit_msbsLess_T_36, _res_hit_msbsLess_T_41)
[648] FIRRTL:360892 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_42 = shr(io.addr, 3)
[649] FIRRTL:360893 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_43 = shl(io.pmp[3].addr, 2)
[650] FIRRTL:360894 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_44 = not(_res_hit_msbsEqual_T_43)
[651] FIRRTL:360895 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_45 = or(_res_hit_msbsEqual_T_44, UInt<2>(0h3))
[652] FIRRTL:360896 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_46 = not(_res_hit_msbsEqual_T_45)
[653] FIRRTL:360897 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_47 = shr(_res_hit_msbsEqual_T_46, 3)
[654] FIRRTL:360898 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_48 = xor(_res_hit_msbsEqual_T_42, _res_hit_msbsEqual_T_47)
[655] FIRRTL:360899 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_6 = eq(_res_hit_msbsEqual_T_48, UInt<1>(0h0))
[656] FIRRTL:360900 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_42 = bits(io.addr, 2, 0)
[657] FIRRTL:360901 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_43 = or(_res_hit_lsbsLess_T_42, _res_hit_T_44)
[658] FIRRTL:360902 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_44 = shl(io.pmp[3].addr, 2)
[659] FIRRTL:360903 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_45 = not(_res_hit_lsbsLess_T_44)
[660] FIRRTL:360904 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_46 = or(_res_hit_lsbsLess_T_45, UInt<2>(0h3))
[661] FIRRTL:360905 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_47 = not(_res_hit_lsbsLess_T_46)
[662] FIRRTL:360906 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_48 = bits(_res_hit_lsbsLess_T_47, 2, 0)
[663] FIRRTL:360907 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_6 = lt(_res_hit_lsbsLess_T_43, _res_hit_lsbsLess_T_48)
[664] FIRRTL:360908 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_45 = and(res_hit_msbsEqual_6, res_hit_lsbsLess_6)
[665] FIRRTL:360909 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_46 = or(res_hit_msbsLess_6, _res_hit_T_45)
[666] FIRRTL:360910 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_47 = eq(_res_hit_T_46, UInt<1>(0h0))
[667] FIRRTL:360911 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_42 = shr(io.addr, 3)
[668] FIRRTL:360912 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_43 = shl(io.pmp[4].addr, 2)
[669] FIRRTL:360913 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_44 = not(_res_hit_msbsLess_T_43)
[670] FIRRTL:360914 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_45 = or(_res_hit_msbsLess_T_44, UInt<2>(0h3))
[671] FIRRTL:360915 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_46 = not(_res_hit_msbsLess_T_45)
[672] FIRRTL:360916 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_47 = shr(_res_hit_msbsLess_T_46, 3)
[673] FIRRTL:360917 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_7 = lt(_res_hit_msbsLess_T_42, _res_hit_msbsLess_T_47)
[674] FIRRTL:360918 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_49 = shr(io.addr, 3)
[675] FIRRTL:360919 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_50 = shl(io.pmp[4].addr, 2)
[676] FIRRTL:360920 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_51 = not(_res_hit_msbsEqual_T_50)
[677] FIRRTL:360921 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_52 = or(_res_hit_msbsEqual_T_51, UInt<2>(0h3))
[678] FIRRTL:360922 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_53 = not(_res_hit_msbsEqual_T_52)
[679] FIRRTL:360923 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_54 = shr(_res_hit_msbsEqual_T_53, 3)
[680] FIRRTL:360924 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_55 = xor(_res_hit_msbsEqual_T_49, _res_hit_msbsEqual_T_54)
[681] FIRRTL:360925 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_7 = eq(_res_hit_msbsEqual_T_55, UInt<1>(0h0))
[682] FIRRTL:360926 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_49 = bits(io.addr, 2, 0)
[683] FIRRTL:360927 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_50 = or(_res_hit_lsbsLess_T_49, UInt<1>(0h0))
[684] FIRRTL:360928 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_51 = shl(io.pmp[4].addr, 2)
[685] FIRRTL:360929 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_52 = not(_res_hit_lsbsLess_T_51)
[686] FIRRTL:360930 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_53 = or(_res_hit_lsbsLess_T_52, UInt<2>(0h3))
[687] FIRRTL:360931 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_54 = not(_res_hit_lsbsLess_T_53)
[688] FIRRTL:360932 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_55 = bits(_res_hit_lsbsLess_T_54, 2, 0)
[689] FIRRTL:360933 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_7 = lt(_res_hit_lsbsLess_T_50, _res_hit_lsbsLess_T_55)
[690] FIRRTL:360934 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_48 = and(res_hit_msbsEqual_7, res_hit_lsbsLess_7)
[691] FIRRTL:360935 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_49 = or(res_hit_msbsLess_7, _res_hit_T_48)
[692] FIRRTL:360936 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_50 = and(_res_hit_T_47, _res_hit_T_49)
[693] FIRRTL:360937 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_51 = and(_res_hit_T_41, _res_hit_T_50)
[694] FIRRTL:360938 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_3 = mux(_res_hit_T_39, _res_hit_T_40, _res_hit_T_51)
[695] FIRRTL:360939 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_3 = eq(io.pmp[4].cfg.l, UInt<1>(0h0))
[696] FIRRTL:360940 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_3 = and(default, _res_ignore_T_3)
[697] FIRRTL:360941 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_6 = dshl(UInt<3>(0h7), io.size)
[698] FIRRTL:360942 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_7 = bits(_res_aligned_lsbMask_T_6, 2, 0)
[699] FIRRTL:360943 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_3 = not(_res_aligned_lsbMask_T_7)
[700] FIRRTL:360944 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_51 = shr(io.addr, 3)
[701] FIRRTL:360945 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_52 = shl(io.pmp[3].addr, 2)
[702] FIRRTL:360946 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_53 = not(_res_aligned_straddlesLowerBound_T_52)
[703] FIRRTL:360947 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_54 = or(_res_aligned_straddlesLowerBound_T_53, UInt<2>(0h3))
[704] FIRRTL:360948 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_55 = not(_res_aligned_straddlesLowerBound_T_54)
[705] FIRRTL:360949 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_56 = shr(_res_aligned_straddlesLowerBound_T_55, 3)
[706] FIRRTL:360950 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_57 = xor(_res_aligned_straddlesLowerBound_T_51, _res_aligned_straddlesLowerBound_T_56)
[707] FIRRTL:360951 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_58 = eq(_res_aligned_straddlesLowerBound_T_57, UInt<1>(0h0))
[708] FIRRTL:360952 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_59 = shl(io.pmp[3].addr, 2)
[709] FIRRTL:360953 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_60 = not(_res_aligned_straddlesLowerBound_T_59)
[710] FIRRTL:360954 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_61 = or(_res_aligned_straddlesLowerBound_T_60, UInt<2>(0h3))
[711] FIRRTL:360955 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_62 = not(_res_aligned_straddlesLowerBound_T_61)
[712] FIRRTL:360956 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_63 = bits(_res_aligned_straddlesLowerBound_T_62, 2, 0)
[713] FIRRTL:360957 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_64 = bits(io.addr, 2, 0)
[714] FIRRTL:360958 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_65 = not(_res_aligned_straddlesLowerBound_T_64)
[715] FIRRTL:360959 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_66 = and(_res_aligned_straddlesLowerBound_T_63, _res_aligned_straddlesLowerBound_T_65)
[716] FIRRTL:360960 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_67 = neq(_res_aligned_straddlesLowerBound_T_66, UInt<1>(0h0))
[717] FIRRTL:360961 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_3 = and(_res_aligned_straddlesLowerBound_T_58, _res_aligned_straddlesLowerBound_T_67)
[718] FIRRTL:360962 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_51 = shr(io.addr, 3)
[719] FIRRTL:360963 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_52 = shl(io.pmp[4].addr, 2)
[720] FIRRTL:360964 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_53 = not(_res_aligned_straddlesUpperBound_T_52)
[721] FIRRTL:360965 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_54 = or(_res_aligned_straddlesUpperBound_T_53, UInt<2>(0h3))
[722] FIRRTL:360966 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_55 = not(_res_aligned_straddlesUpperBound_T_54)
[723] FIRRTL:360967 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_56 = shr(_res_aligned_straddlesUpperBound_T_55, 3)
[724] FIRRTL:360968 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_57 = xor(_res_aligned_straddlesUpperBound_T_51, _res_aligned_straddlesUpperBound_T_56)
[725] FIRRTL:360969 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_58 = eq(_res_aligned_straddlesUpperBound_T_57, UInt<1>(0h0))
[726] FIRRTL:360970 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_59 = shl(io.pmp[4].addr, 2)
[727] FIRRTL:360971 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_60 = not(_res_aligned_straddlesUpperBound_T_59)
[728] FIRRTL:360972 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_61 = or(_res_aligned_straddlesUpperBound_T_60, UInt<2>(0h3))
[729] FIRRTL:360973 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_62 = not(_res_aligned_straddlesUpperBound_T_61)
[730] FIRRTL:360974 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_63 = bits(_res_aligned_straddlesUpperBound_T_62, 2, 0)
[731] FIRRTL:360975 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_64 = bits(io.addr, 2, 0)
[732] FIRRTL:360976 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_65 = or(_res_aligned_straddlesUpperBound_T_64, res_aligned_lsbMask_3)
[733] FIRRTL:360977 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_66 = and(_res_aligned_straddlesUpperBound_T_63, _res_aligned_straddlesUpperBound_T_65)
[734] FIRRTL:360978 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_67 = neq(_res_aligned_straddlesUpperBound_T_66, UInt<1>(0h0))
[735] FIRRTL:360979 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_3 = and(_res_aligned_straddlesUpperBound_T_58, _res_aligned_straddlesUpperBound_T_67)
[736] FIRRTL:360980 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_3 = or(res_aligned_straddlesLowerBound_3, res_aligned_straddlesUpperBound_3)
[737] FIRRTL:360981 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_3 = eq(_res_aligned_rangeAligned_T_3, UInt<1>(0h0))
[738] FIRRTL:360982 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_9 = bits(io.pmp[4].mask, 2, 0)
[739] FIRRTL:360983 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_10 = not(_res_aligned_pow2Aligned_T_9)
[740] FIRRTL:360984 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_11 = and(res_aligned_lsbMask_3, _res_aligned_pow2Aligned_T_10)
[741] FIRRTL:360985 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_3 = eq(_res_aligned_pow2Aligned_T_11, UInt<1>(0h0))
[742] FIRRTL:360986 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_3 = bits(io.pmp[4].cfg.a, 1, 1)
[743] FIRRTL:360987 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_3 = mux(_res_aligned_T_3, res_aligned_pow2Aligned_3, res_aligned_rangeAligned_3)
[744] FIRRTL:360988 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_135 = eq(io.pmp[4].cfg.a, UInt<1>(0h0))
[745] FIRRTL:360989 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_136 = eq(io.pmp[4].cfg.a, UInt<1>(0h1))
[746] FIRRTL:360990 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_137 = eq(io.pmp[4].cfg.a, UInt<2>(0h2))
[747] FIRRTL:360991 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_138 = eq(io.pmp[4].cfg.a, UInt<2>(0h3))
[748] FIRRTL:360992 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_139 = eq(io.pmp[4].cfg.l, UInt<1>(0h1))
[749] FIRRTL:360993 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_18 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[750] FIRRTL:360994 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_140 = cat(res_hi_18, io.pmp[4].cfg.r)
[751] FIRRTL:360995 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_141 = eq(_res_T_140, UInt<1>(0h0))
[752] FIRRTL:360996 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_19 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[753] FIRRTL:360997 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_142 = cat(res_hi_19, io.pmp[4].cfg.r)
[754] FIRRTL:360998 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_143 = eq(_res_T_142, UInt<1>(0h1))
[755] FIRRTL:360999 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_20 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[756] FIRRTL:361000 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_144 = cat(res_hi_20, io.pmp[4].cfg.r)
[757] FIRRTL:361001 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_145 = eq(_res_T_144, UInt<2>(0h3))
[758] FIRRTL:361002 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_21 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[759] FIRRTL:361003 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_146 = cat(res_hi_21, io.pmp[4].cfg.r)
[760] FIRRTL:361004 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_147 = eq(_res_T_146, UInt<3>(0h4))
[761] FIRRTL:361005 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_22 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[762] FIRRTL:361006 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_148 = cat(res_hi_22, io.pmp[4].cfg.r)
[763] FIRRTL:361007 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_149 = eq(_res_T_148, UInt<3>(0h5))
[764] FIRRTL:361008 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_23 = cat(io.pmp[4].cfg.x, io.pmp[4].cfg.w)
[765] FIRRTL:361009 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_150 = cat(res_hi_23, io.pmp[4].cfg.r)
[766] FIRRTL:361010 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_151 = eq(_res_T_150, UInt<3>(0h7))
[767] FIRRTL:361011 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_152 = eq(res_ignore_3, UInt<1>(0h0))
[768] FIRRTL:361012 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_153 = and(_res_T_152, res_hit_3)
[769] FIRRTL:361013 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_154 = and(_res_T_153, res_aligned_3)
[770] FIRRTL:361014 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_155 = eq(io.pmp[4].cfg.a, UInt<1>(0h1))
[771] FIRRTL:361015 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_156 = and(_res_T_154, _res_T_155)
[772] FIRRTL:361016 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_157 = and(io.pmp[4].cfg.l, res_hit_3)
[773] FIRRTL:361017 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_158 = and(_res_T_157, res_aligned_3)
[774] FIRRTL:361018 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_159 = eq(io.pmp[4].cfg.a, UInt<1>(0h1))
[775] FIRRTL:361019 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_160 = and(_res_T_158, _res_T_159)
[776] FIRRTL:361020 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_161 = eq(res_ignore_3, UInt<1>(0h0))
[777] FIRRTL:361021 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_162 = and(_res_T_161, res_hit_3)
[778] FIRRTL:361022 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_163 = and(_res_T_162, res_aligned_3)
[779] FIRRTL:361023 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_164 = eq(io.pmp[4].cfg.a, UInt<2>(0h2))
[780] FIRRTL:361024 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_165 = and(_res_T_163, _res_T_164)
[781] FIRRTL:361025 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_166 = and(io.pmp[4].cfg.l, res_hit_3)
[782] FIRRTL:361026 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_167 = and(_res_T_166, res_aligned_3)
[783] FIRRTL:361027 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_168 = eq(io.pmp[4].cfg.a, UInt<2>(0h2))
[784] FIRRTL:361028 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_169 = and(_res_T_167, _res_T_168)
[785] FIRRTL:361029 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_170 = eq(res_ignore_3, UInt<1>(0h0))
[786] FIRRTL:361030 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_171 = and(_res_T_170, res_hit_3)
[787] FIRRTL:361031 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_172 = and(_res_T_171, res_aligned_3)
[788] FIRRTL:361032 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_173 = eq(io.pmp[4].cfg.a, UInt<2>(0h3))
[789] FIRRTL:361033 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_174 = and(_res_T_172, _res_T_173)
[790] FIRRTL:361034 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_175 = and(io.pmp[4].cfg.l, res_hit_3)
[791] FIRRTL:361035 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_176 = and(_res_T_175, res_aligned_3)
[792] FIRRTL:361036 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_177 = eq(io.pmp[4].cfg.a, UInt<2>(0h3))
[793] FIRRTL:361037 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_178 = and(_res_T_176, _res_T_177)
[794] FIRRTL:361038 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_3 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[795] FIRRTL:361039 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_3, io.pmp[4]
[796] FIRRTL:361040 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_6 = or(io.pmp[4].cfg.r, res_ignore_3)
[797] FIRRTL:361041 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_7 = and(res_aligned_3, _res_cur_cfg_r_T_6)
[798] FIRRTL:361042 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_3.cfg.r, _res_cur_cfg_r_T_7
[799] FIRRTL:361043 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_6 = or(io.pmp[4].cfg.w, res_ignore_3)
[800] FIRRTL:361044 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_7 = and(res_aligned_3, _res_cur_cfg_w_T_6)
[801] FIRRTL:361045 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_3.cfg.w, _res_cur_cfg_w_T_7
[802] FIRRTL:361046 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_6 = or(io.pmp[4].cfg.x, res_ignore_3)
[803] FIRRTL:361047 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_7 = and(res_aligned_3, _res_cur_cfg_x_T_6)
[804] FIRRTL:361048 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_3.cfg.x, _res_cur_cfg_x_T_7
[805] FIRRTL:361049 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_179 = mux(res_hit_3, res_cur_3, _res_T_134)
[806] FIRRTL:361050 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_52 = bits(io.pmp[3].cfg.a, 1, 1)
[807] FIRRTL:361051 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_12 = dshl(UInt<3>(0h7), io.size)
[808] FIRRTL:361052 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_13 = bits(_res_hit_lsbMask_T_12, 2, 0)
[809] FIRRTL:361053 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_14 = not(_res_hit_lsbMask_T_13)
[810] FIRRTL:361054 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_4 = or(io.pmp[3].mask, _res_hit_lsbMask_T_14)
[811] FIRRTL:361055 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_40 = shr(io.addr, 3)
[812] FIRRTL:361056 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_41 = shl(io.pmp[3].addr, 2)
[813] FIRRTL:361057 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_42 = not(_res_hit_msbMatch_T_41)
[814] FIRRTL:361058 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_43 = or(_res_hit_msbMatch_T_42, UInt<2>(0h3))
[815] FIRRTL:361059 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_44 = not(_res_hit_msbMatch_T_43)
[816] FIRRTL:361060 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_45 = shr(_res_hit_msbMatch_T_44, 3)
[817] FIRRTL:361061 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_46 = shr(io.pmp[3].mask, 3)
[818] FIRRTL:361062 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_47 = xor(_res_hit_msbMatch_T_40, _res_hit_msbMatch_T_45)
[819] FIRRTL:361063 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_48 = not(_res_hit_msbMatch_T_46)
[820] FIRRTL:361064 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_49 = and(_res_hit_msbMatch_T_47, _res_hit_msbMatch_T_48)
[821] FIRRTL:361065 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_4 = eq(_res_hit_msbMatch_T_49, UInt<1>(0h0))
[822] FIRRTL:361066 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_40 = bits(io.addr, 2, 0)
[823] FIRRTL:361067 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_41 = shl(io.pmp[3].addr, 2)
[824] FIRRTL:361068 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_42 = not(_res_hit_lsbMatch_T_41)
[825] FIRRTL:361069 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_43 = or(_res_hit_lsbMatch_T_42, UInt<2>(0h3))
[826] FIRRTL:361070 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_44 = not(_res_hit_lsbMatch_T_43)
[827] FIRRTL:361071 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_45 = bits(_res_hit_lsbMatch_T_44, 2, 0)
[828] FIRRTL:361072 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_46 = bits(res_hit_lsbMask_4, 2, 0)
[829] FIRRTL:361073 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_47 = xor(_res_hit_lsbMatch_T_40, _res_hit_lsbMatch_T_45)
[830] FIRRTL:361074 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_48 = not(_res_hit_lsbMatch_T_46)
[831] FIRRTL:361075 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_49 = and(_res_hit_lsbMatch_T_47, _res_hit_lsbMatch_T_48)
[832] FIRRTL:361076 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_4 = eq(_res_hit_lsbMatch_T_49, UInt<1>(0h0))
[833] FIRRTL:361077 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_53 = and(res_hit_msbMatch_4, res_hit_lsbMatch_4)
[834] FIRRTL:361078 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_54 = bits(io.pmp[3].cfg.a, 0, 0)
[835] FIRRTL:361079 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_55 = dshl(UInt<3>(0h7), io.size)
[836] FIRRTL:361080 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_56 = bits(_res_hit_T_55, 2, 0)
[837] FIRRTL:361081 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_57 = not(_res_hit_T_56)
[838] FIRRTL:361082 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_48 = shr(io.addr, 3)
[839] FIRRTL:361083 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_49 = shl(io.pmp[2].addr, 2)
[840] FIRRTL:361084 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_50 = not(_res_hit_msbsLess_T_49)
[841] FIRRTL:361085 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_51 = or(_res_hit_msbsLess_T_50, UInt<2>(0h3))
[842] FIRRTL:361086 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_52 = not(_res_hit_msbsLess_T_51)
[843] FIRRTL:361087 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_53 = shr(_res_hit_msbsLess_T_52, 3)
[844] FIRRTL:361088 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_8 = lt(_res_hit_msbsLess_T_48, _res_hit_msbsLess_T_53)
[845] FIRRTL:361089 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_56 = shr(io.addr, 3)
[846] FIRRTL:361090 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_57 = shl(io.pmp[2].addr, 2)
[847] FIRRTL:361091 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_58 = not(_res_hit_msbsEqual_T_57)
[848] FIRRTL:361092 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_59 = or(_res_hit_msbsEqual_T_58, UInt<2>(0h3))
[849] FIRRTL:361093 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_60 = not(_res_hit_msbsEqual_T_59)
[850] FIRRTL:361094 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_61 = shr(_res_hit_msbsEqual_T_60, 3)
[851] FIRRTL:361095 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_62 = xor(_res_hit_msbsEqual_T_56, _res_hit_msbsEqual_T_61)
[852] FIRRTL:361096 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_8 = eq(_res_hit_msbsEqual_T_62, UInt<1>(0h0))
[853] FIRRTL:361097 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_56 = bits(io.addr, 2, 0)
[854] FIRRTL:361098 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_57 = or(_res_hit_lsbsLess_T_56, _res_hit_T_57)
[855] FIRRTL:361099 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_58 = shl(io.pmp[2].addr, 2)
[856] FIRRTL:361100 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_59 = not(_res_hit_lsbsLess_T_58)
[857] FIRRTL:361101 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_60 = or(_res_hit_lsbsLess_T_59, UInt<2>(0h3))
[858] FIRRTL:361102 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_61 = not(_res_hit_lsbsLess_T_60)
[859] FIRRTL:361103 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_62 = bits(_res_hit_lsbsLess_T_61, 2, 0)
[860] FIRRTL:361104 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_8 = lt(_res_hit_lsbsLess_T_57, _res_hit_lsbsLess_T_62)
[861] FIRRTL:361105 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_58 = and(res_hit_msbsEqual_8, res_hit_lsbsLess_8)
[862] FIRRTL:361106 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_59 = or(res_hit_msbsLess_8, _res_hit_T_58)
[863] FIRRTL:361107 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_60 = eq(_res_hit_T_59, UInt<1>(0h0))
[864] FIRRTL:361108 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_54 = shr(io.addr, 3)
[865] FIRRTL:361109 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_55 = shl(io.pmp[3].addr, 2)
[866] FIRRTL:361110 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_56 = not(_res_hit_msbsLess_T_55)
[867] FIRRTL:361111 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_57 = or(_res_hit_msbsLess_T_56, UInt<2>(0h3))
[868] FIRRTL:361112 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_58 = not(_res_hit_msbsLess_T_57)
[869] FIRRTL:361113 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_59 = shr(_res_hit_msbsLess_T_58, 3)
[870] FIRRTL:361114 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_9 = lt(_res_hit_msbsLess_T_54, _res_hit_msbsLess_T_59)
[871] FIRRTL:361115 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_63 = shr(io.addr, 3)
[872] FIRRTL:361116 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_64 = shl(io.pmp[3].addr, 2)
[873] FIRRTL:361117 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_65 = not(_res_hit_msbsEqual_T_64)
[874] FIRRTL:361118 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_66 = or(_res_hit_msbsEqual_T_65, UInt<2>(0h3))
[875] FIRRTL:361119 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_67 = not(_res_hit_msbsEqual_T_66)
[876] FIRRTL:361120 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_68 = shr(_res_hit_msbsEqual_T_67, 3)
[877] FIRRTL:361121 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_69 = xor(_res_hit_msbsEqual_T_63, _res_hit_msbsEqual_T_68)
[878] FIRRTL:361122 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_9 = eq(_res_hit_msbsEqual_T_69, UInt<1>(0h0))
[879] FIRRTL:361123 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_63 = bits(io.addr, 2, 0)
[880] FIRRTL:361124 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_64 = or(_res_hit_lsbsLess_T_63, UInt<1>(0h0))
[881] FIRRTL:361125 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_65 = shl(io.pmp[3].addr, 2)
[882] FIRRTL:361126 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_66 = not(_res_hit_lsbsLess_T_65)
[883] FIRRTL:361127 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_67 = or(_res_hit_lsbsLess_T_66, UInt<2>(0h3))
[884] FIRRTL:361128 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_68 = not(_res_hit_lsbsLess_T_67)
[885] FIRRTL:361129 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_69 = bits(_res_hit_lsbsLess_T_68, 2, 0)
[886] FIRRTL:361130 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_9 = lt(_res_hit_lsbsLess_T_64, _res_hit_lsbsLess_T_69)
[887] FIRRTL:361131 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_61 = and(res_hit_msbsEqual_9, res_hit_lsbsLess_9)
[888] FIRRTL:361132 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_62 = or(res_hit_msbsLess_9, _res_hit_T_61)
[889] FIRRTL:361133 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_63 = and(_res_hit_T_60, _res_hit_T_62)
[890] FIRRTL:361134 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_64 = and(_res_hit_T_54, _res_hit_T_63)
[891] FIRRTL:361135 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_4 = mux(_res_hit_T_52, _res_hit_T_53, _res_hit_T_64)
[892] FIRRTL:361136 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_4 = eq(io.pmp[3].cfg.l, UInt<1>(0h0))
[893] FIRRTL:361137 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_4 = and(default, _res_ignore_T_4)
[894] FIRRTL:361138 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_8 = dshl(UInt<3>(0h7), io.size)
[895] FIRRTL:361139 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_9 = bits(_res_aligned_lsbMask_T_8, 2, 0)
[896] FIRRTL:361140 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_4 = not(_res_aligned_lsbMask_T_9)
[897] FIRRTL:361141 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_68 = shr(io.addr, 3)
[898] FIRRTL:361142 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_69 = shl(io.pmp[2].addr, 2)
[899] FIRRTL:361143 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_70 = not(_res_aligned_straddlesLowerBound_T_69)
[900] FIRRTL:361144 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_71 = or(_res_aligned_straddlesLowerBound_T_70, UInt<2>(0h3))
[901] FIRRTL:361145 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_72 = not(_res_aligned_straddlesLowerBound_T_71)
[902] FIRRTL:361146 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_73 = shr(_res_aligned_straddlesLowerBound_T_72, 3)
[903] FIRRTL:361147 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_74 = xor(_res_aligned_straddlesLowerBound_T_68, _res_aligned_straddlesLowerBound_T_73)
[904] FIRRTL:361148 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_75 = eq(_res_aligned_straddlesLowerBound_T_74, UInt<1>(0h0))
[905] FIRRTL:361149 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_76 = shl(io.pmp[2].addr, 2)
[906] FIRRTL:361150 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_77 = not(_res_aligned_straddlesLowerBound_T_76)
[907] FIRRTL:361151 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_78 = or(_res_aligned_straddlesLowerBound_T_77, UInt<2>(0h3))
[908] FIRRTL:361152 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_79 = not(_res_aligned_straddlesLowerBound_T_78)
[909] FIRRTL:361153 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_80 = bits(_res_aligned_straddlesLowerBound_T_79, 2, 0)
[910] FIRRTL:361154 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_81 = bits(io.addr, 2, 0)
[911] FIRRTL:361155 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_82 = not(_res_aligned_straddlesLowerBound_T_81)
[912] FIRRTL:361156 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_83 = and(_res_aligned_straddlesLowerBound_T_80, _res_aligned_straddlesLowerBound_T_82)
[913] FIRRTL:361157 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_84 = neq(_res_aligned_straddlesLowerBound_T_83, UInt<1>(0h0))
[914] FIRRTL:361158 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_4 = and(_res_aligned_straddlesLowerBound_T_75, _res_aligned_straddlesLowerBound_T_84)
[915] FIRRTL:361159 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_68 = shr(io.addr, 3)
[916] FIRRTL:361160 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_69 = shl(io.pmp[3].addr, 2)
[917] FIRRTL:361161 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_70 = not(_res_aligned_straddlesUpperBound_T_69)
[918] FIRRTL:361162 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_71 = or(_res_aligned_straddlesUpperBound_T_70, UInt<2>(0h3))
[919] FIRRTL:361163 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_72 = not(_res_aligned_straddlesUpperBound_T_71)
[920] FIRRTL:361164 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_73 = shr(_res_aligned_straddlesUpperBound_T_72, 3)
[921] FIRRTL:361165 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_74 = xor(_res_aligned_straddlesUpperBound_T_68, _res_aligned_straddlesUpperBound_T_73)
[922] FIRRTL:361166 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_75 = eq(_res_aligned_straddlesUpperBound_T_74, UInt<1>(0h0))
[923] FIRRTL:361167 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_76 = shl(io.pmp[3].addr, 2)
[924] FIRRTL:361168 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_77 = not(_res_aligned_straddlesUpperBound_T_76)
[925] FIRRTL:361169 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_78 = or(_res_aligned_straddlesUpperBound_T_77, UInt<2>(0h3))
[926] FIRRTL:361170 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_79 = not(_res_aligned_straddlesUpperBound_T_78)
[927] FIRRTL:361171 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_80 = bits(_res_aligned_straddlesUpperBound_T_79, 2, 0)
[928] FIRRTL:361172 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_81 = bits(io.addr, 2, 0)
[929] FIRRTL:361173 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_82 = or(_res_aligned_straddlesUpperBound_T_81, res_aligned_lsbMask_4)
[930] FIRRTL:361174 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_83 = and(_res_aligned_straddlesUpperBound_T_80, _res_aligned_straddlesUpperBound_T_82)
[931] FIRRTL:361175 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_84 = neq(_res_aligned_straddlesUpperBound_T_83, UInt<1>(0h0))
[932] FIRRTL:361176 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_4 = and(_res_aligned_straddlesUpperBound_T_75, _res_aligned_straddlesUpperBound_T_84)
[933] FIRRTL:361177 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_4 = or(res_aligned_straddlesLowerBound_4, res_aligned_straddlesUpperBound_4)
[934] FIRRTL:361178 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_4 = eq(_res_aligned_rangeAligned_T_4, UInt<1>(0h0))
[935] FIRRTL:361179 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_12 = bits(io.pmp[3].mask, 2, 0)
[936] FIRRTL:361180 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_13 = not(_res_aligned_pow2Aligned_T_12)
[937] FIRRTL:361181 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_14 = and(res_aligned_lsbMask_4, _res_aligned_pow2Aligned_T_13)
[938] FIRRTL:361182 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_4 = eq(_res_aligned_pow2Aligned_T_14, UInt<1>(0h0))
[939] FIRRTL:361183 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_4 = bits(io.pmp[3].cfg.a, 1, 1)
[940] FIRRTL:361184 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_4 = mux(_res_aligned_T_4, res_aligned_pow2Aligned_4, res_aligned_rangeAligned_4)
[941] FIRRTL:361185 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_180 = eq(io.pmp[3].cfg.a, UInt<1>(0h0))
[942] FIRRTL:361186 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_181 = eq(io.pmp[3].cfg.a, UInt<1>(0h1))
[943] FIRRTL:361187 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_182 = eq(io.pmp[3].cfg.a, UInt<2>(0h2))
[944] FIRRTL:361188 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_183 = eq(io.pmp[3].cfg.a, UInt<2>(0h3))
[945] FIRRTL:361189 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_184 = eq(io.pmp[3].cfg.l, UInt<1>(0h1))
[946] FIRRTL:361190 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_24 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[947] FIRRTL:361191 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_185 = cat(res_hi_24, io.pmp[3].cfg.r)
[948] FIRRTL:361192 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_186 = eq(_res_T_185, UInt<1>(0h0))
[949] FIRRTL:361193 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_25 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[950] FIRRTL:361194 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_187 = cat(res_hi_25, io.pmp[3].cfg.r)
[951] FIRRTL:361195 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_188 = eq(_res_T_187, UInt<1>(0h1))
[952] FIRRTL:361196 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_26 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[953] FIRRTL:361197 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_189 = cat(res_hi_26, io.pmp[3].cfg.r)
[954] FIRRTL:361198 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_190 = eq(_res_T_189, UInt<2>(0h3))
[955] FIRRTL:361199 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_27 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[956] FIRRTL:361200 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_191 = cat(res_hi_27, io.pmp[3].cfg.r)
[957] FIRRTL:361201 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_192 = eq(_res_T_191, UInt<3>(0h4))
[958] FIRRTL:361202 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_28 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[959] FIRRTL:361203 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_193 = cat(res_hi_28, io.pmp[3].cfg.r)
[960] FIRRTL:361204 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_194 = eq(_res_T_193, UInt<3>(0h5))
[961] FIRRTL:361205 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_29 = cat(io.pmp[3].cfg.x, io.pmp[3].cfg.w)
[962] FIRRTL:361206 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_195 = cat(res_hi_29, io.pmp[3].cfg.r)
[963] FIRRTL:361207 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_196 = eq(_res_T_195, UInt<3>(0h7))
[964] FIRRTL:361208 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_197 = eq(res_ignore_4, UInt<1>(0h0))
[965] FIRRTL:361209 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_198 = and(_res_T_197, res_hit_4)
[966] FIRRTL:361210 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_199 = and(_res_T_198, res_aligned_4)
[967] FIRRTL:361211 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_200 = eq(io.pmp[3].cfg.a, UInt<1>(0h1))
[968] FIRRTL:361212 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_201 = and(_res_T_199, _res_T_200)
[969] FIRRTL:361213 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_202 = and(io.pmp[3].cfg.l, res_hit_4)
[970] FIRRTL:361214 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_203 = and(_res_T_202, res_aligned_4)
[971] FIRRTL:361215 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_204 = eq(io.pmp[3].cfg.a, UInt<1>(0h1))
[972] FIRRTL:361216 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_205 = and(_res_T_203, _res_T_204)
[973] FIRRTL:361217 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_206 = eq(res_ignore_4, UInt<1>(0h0))
[974] FIRRTL:361218 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_207 = and(_res_T_206, res_hit_4)
[975] FIRRTL:361219 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_208 = and(_res_T_207, res_aligned_4)
[976] FIRRTL:361220 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_209 = eq(io.pmp[3].cfg.a, UInt<2>(0h2))
[977] FIRRTL:361221 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_210 = and(_res_T_208, _res_T_209)
[978] FIRRTL:361222 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_211 = and(io.pmp[3].cfg.l, res_hit_4)
[979] FIRRTL:361223 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_212 = and(_res_T_211, res_aligned_4)
[980] FIRRTL:361224 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_213 = eq(io.pmp[3].cfg.a, UInt<2>(0h2))
[981] FIRRTL:361225 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_214 = and(_res_T_212, _res_T_213)
[982] FIRRTL:361226 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_215 = eq(res_ignore_4, UInt<1>(0h0))
[983] FIRRTL:361227 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_216 = and(_res_T_215, res_hit_4)
[984] FIRRTL:361228 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_217 = and(_res_T_216, res_aligned_4)
[985] FIRRTL:361229 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_218 = eq(io.pmp[3].cfg.a, UInt<2>(0h3))
[986] FIRRTL:361230 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_219 = and(_res_T_217, _res_T_218)
[987] FIRRTL:361231 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_220 = and(io.pmp[3].cfg.l, res_hit_4)
[988] FIRRTL:361232 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_221 = and(_res_T_220, res_aligned_4)
[989] FIRRTL:361233 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_222 = eq(io.pmp[3].cfg.a, UInt<2>(0h3))
[990] FIRRTL:361234 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_223 = and(_res_T_221, _res_T_222)
[991] FIRRTL:361235 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_4 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[992] FIRRTL:361236 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_4, io.pmp[3]
[993] FIRRTL:361237 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_8 = or(io.pmp[3].cfg.r, res_ignore_4)
[994] FIRRTL:361238 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_9 = and(res_aligned_4, _res_cur_cfg_r_T_8)
[995] FIRRTL:361239 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_4.cfg.r, _res_cur_cfg_r_T_9
[996] FIRRTL:361240 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_8 = or(io.pmp[3].cfg.w, res_ignore_4)
[997] FIRRTL:361241 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_9 = and(res_aligned_4, _res_cur_cfg_w_T_8)
[998] FIRRTL:361242 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_4.cfg.w, _res_cur_cfg_w_T_9
[999] FIRRTL:361243 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_8 = or(io.pmp[3].cfg.x, res_ignore_4)
[1000] FIRRTL:361244 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_9 = and(res_aligned_4, _res_cur_cfg_x_T_8)
[1001] FIRRTL:361245 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_4.cfg.x, _res_cur_cfg_x_T_9
[1002] FIRRTL:361246 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_224 = mux(res_hit_4, res_cur_4, _res_T_179)
[1003] FIRRTL:361247 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_65 = bits(io.pmp[2].cfg.a, 1, 1)
[1004] FIRRTL:361248 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_15 = dshl(UInt<3>(0h7), io.size)
[1005] FIRRTL:361249 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_16 = bits(_res_hit_lsbMask_T_15, 2, 0)
[1006] FIRRTL:361250 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_17 = not(_res_hit_lsbMask_T_16)
[1007] FIRRTL:361251 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_5 = or(io.pmp[2].mask, _res_hit_lsbMask_T_17)
[1008] FIRRTL:361252 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_50 = shr(io.addr, 3)
[1009] FIRRTL:361253 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_51 = shl(io.pmp[2].addr, 2)
[1010] FIRRTL:361254 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_52 = not(_res_hit_msbMatch_T_51)
[1011] FIRRTL:361255 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_53 = or(_res_hit_msbMatch_T_52, UInt<2>(0h3))
[1012] FIRRTL:361256 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_54 = not(_res_hit_msbMatch_T_53)
[1013] FIRRTL:361257 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_55 = shr(_res_hit_msbMatch_T_54, 3)
[1014] FIRRTL:361258 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_56 = shr(io.pmp[2].mask, 3)
[1015] FIRRTL:361259 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_57 = xor(_res_hit_msbMatch_T_50, _res_hit_msbMatch_T_55)
[1016] FIRRTL:361260 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_58 = not(_res_hit_msbMatch_T_56)
[1017] FIRRTL:361261 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_59 = and(_res_hit_msbMatch_T_57, _res_hit_msbMatch_T_58)
[1018] FIRRTL:361262 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_5 = eq(_res_hit_msbMatch_T_59, UInt<1>(0h0))
[1019] FIRRTL:361263 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_50 = bits(io.addr, 2, 0)
[1020] FIRRTL:361264 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_51 = shl(io.pmp[2].addr, 2)
[1021] FIRRTL:361265 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_52 = not(_res_hit_lsbMatch_T_51)
[1022] FIRRTL:361266 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_53 = or(_res_hit_lsbMatch_T_52, UInt<2>(0h3))
[1023] FIRRTL:361267 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_54 = not(_res_hit_lsbMatch_T_53)
[1024] FIRRTL:361268 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_55 = bits(_res_hit_lsbMatch_T_54, 2, 0)
[1025] FIRRTL:361269 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_56 = bits(res_hit_lsbMask_5, 2, 0)
[1026] FIRRTL:361270 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_57 = xor(_res_hit_lsbMatch_T_50, _res_hit_lsbMatch_T_55)
[1027] FIRRTL:361271 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_58 = not(_res_hit_lsbMatch_T_56)
[1028] FIRRTL:361272 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_59 = and(_res_hit_lsbMatch_T_57, _res_hit_lsbMatch_T_58)
[1029] FIRRTL:361273 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_5 = eq(_res_hit_lsbMatch_T_59, UInt<1>(0h0))
[1030] FIRRTL:361274 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_66 = and(res_hit_msbMatch_5, res_hit_lsbMatch_5)
[1031] FIRRTL:361275 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_67 = bits(io.pmp[2].cfg.a, 0, 0)
[1032] FIRRTL:361276 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_68 = dshl(UInt<3>(0h7), io.size)
[1033] FIRRTL:361277 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_69 = bits(_res_hit_T_68, 2, 0)
[1034] FIRRTL:361278 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_70 = not(_res_hit_T_69)
[1035] FIRRTL:361279 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_60 = shr(io.addr, 3)
[1036] FIRRTL:361280 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_61 = shl(io.pmp[1].addr, 2)
[1037] FIRRTL:361281 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_62 = not(_res_hit_msbsLess_T_61)
[1038] FIRRTL:361282 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_63 = or(_res_hit_msbsLess_T_62, UInt<2>(0h3))
[1039] FIRRTL:361283 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_64 = not(_res_hit_msbsLess_T_63)
[1040] FIRRTL:361284 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_65 = shr(_res_hit_msbsLess_T_64, 3)
[1041] FIRRTL:361285 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_10 = lt(_res_hit_msbsLess_T_60, _res_hit_msbsLess_T_65)
[1042] FIRRTL:361286 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_70 = shr(io.addr, 3)
[1043] FIRRTL:361287 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_71 = shl(io.pmp[1].addr, 2)
[1044] FIRRTL:361288 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_72 = not(_res_hit_msbsEqual_T_71)
[1045] FIRRTL:361289 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_73 = or(_res_hit_msbsEqual_T_72, UInt<2>(0h3))
[1046] FIRRTL:361290 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_74 = not(_res_hit_msbsEqual_T_73)
[1047] FIRRTL:361291 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_75 = shr(_res_hit_msbsEqual_T_74, 3)
[1048] FIRRTL:361292 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_76 = xor(_res_hit_msbsEqual_T_70, _res_hit_msbsEqual_T_75)
[1049] FIRRTL:361293 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_10 = eq(_res_hit_msbsEqual_T_76, UInt<1>(0h0))
[1050] FIRRTL:361294 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_70 = bits(io.addr, 2, 0)
[1051] FIRRTL:361295 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_71 = or(_res_hit_lsbsLess_T_70, _res_hit_T_70)
[1052] FIRRTL:361296 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_72 = shl(io.pmp[1].addr, 2)
[1053] FIRRTL:361297 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_73 = not(_res_hit_lsbsLess_T_72)
[1054] FIRRTL:361298 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_74 = or(_res_hit_lsbsLess_T_73, UInt<2>(0h3))
[1055] FIRRTL:361299 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_75 = not(_res_hit_lsbsLess_T_74)
[1056] FIRRTL:361300 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_76 = bits(_res_hit_lsbsLess_T_75, 2, 0)
[1057] FIRRTL:361301 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_10 = lt(_res_hit_lsbsLess_T_71, _res_hit_lsbsLess_T_76)
[1058] FIRRTL:361302 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_71 = and(res_hit_msbsEqual_10, res_hit_lsbsLess_10)
[1059] FIRRTL:361303 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_72 = or(res_hit_msbsLess_10, _res_hit_T_71)
[1060] FIRRTL:361304 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_73 = eq(_res_hit_T_72, UInt<1>(0h0))
[1061] FIRRTL:361305 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_66 = shr(io.addr, 3)
[1062] FIRRTL:361306 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_67 = shl(io.pmp[2].addr, 2)
[1063] FIRRTL:361307 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_68 = not(_res_hit_msbsLess_T_67)
[1064] FIRRTL:361308 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_69 = or(_res_hit_msbsLess_T_68, UInt<2>(0h3))
[1065] FIRRTL:361309 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_70 = not(_res_hit_msbsLess_T_69)
[1066] FIRRTL:361310 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_71 = shr(_res_hit_msbsLess_T_70, 3)
[1067] FIRRTL:361311 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_11 = lt(_res_hit_msbsLess_T_66, _res_hit_msbsLess_T_71)
[1068] FIRRTL:361312 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_77 = shr(io.addr, 3)
[1069] FIRRTL:361313 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_78 = shl(io.pmp[2].addr, 2)
[1070] FIRRTL:361314 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_79 = not(_res_hit_msbsEqual_T_78)
[1071] FIRRTL:361315 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_80 = or(_res_hit_msbsEqual_T_79, UInt<2>(0h3))
[1072] FIRRTL:361316 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_81 = not(_res_hit_msbsEqual_T_80)
[1073] FIRRTL:361317 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_82 = shr(_res_hit_msbsEqual_T_81, 3)
[1074] FIRRTL:361318 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_83 = xor(_res_hit_msbsEqual_T_77, _res_hit_msbsEqual_T_82)
[1075] FIRRTL:361319 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_11 = eq(_res_hit_msbsEqual_T_83, UInt<1>(0h0))
[1076] FIRRTL:361320 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_77 = bits(io.addr, 2, 0)
[1077] FIRRTL:361321 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_78 = or(_res_hit_lsbsLess_T_77, UInt<1>(0h0))
[1078] FIRRTL:361322 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_79 = shl(io.pmp[2].addr, 2)
[1079] FIRRTL:361323 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_80 = not(_res_hit_lsbsLess_T_79)
[1080] FIRRTL:361324 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_81 = or(_res_hit_lsbsLess_T_80, UInt<2>(0h3))
[1081] FIRRTL:361325 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_82 = not(_res_hit_lsbsLess_T_81)
[1082] FIRRTL:361326 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_83 = bits(_res_hit_lsbsLess_T_82, 2, 0)
[1083] FIRRTL:361327 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_11 = lt(_res_hit_lsbsLess_T_78, _res_hit_lsbsLess_T_83)
[1084] FIRRTL:361328 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_74 = and(res_hit_msbsEqual_11, res_hit_lsbsLess_11)
[1085] FIRRTL:361329 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_75 = or(res_hit_msbsLess_11, _res_hit_T_74)
[1086] FIRRTL:361330 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_76 = and(_res_hit_T_73, _res_hit_T_75)
[1087] FIRRTL:361331 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_77 = and(_res_hit_T_67, _res_hit_T_76)
[1088] FIRRTL:361332 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_5 = mux(_res_hit_T_65, _res_hit_T_66, _res_hit_T_77)
[1089] FIRRTL:361333 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_5 = eq(io.pmp[2].cfg.l, UInt<1>(0h0))
[1090] FIRRTL:361334 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_5 = and(default, _res_ignore_T_5)
[1091] FIRRTL:361335 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_10 = dshl(UInt<3>(0h7), io.size)
[1092] FIRRTL:361336 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_11 = bits(_res_aligned_lsbMask_T_10, 2, 0)
[1093] FIRRTL:361337 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_5 = not(_res_aligned_lsbMask_T_11)
[1094] FIRRTL:361338 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_85 = shr(io.addr, 3)
[1095] FIRRTL:361339 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_86 = shl(io.pmp[1].addr, 2)
[1096] FIRRTL:361340 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_87 = not(_res_aligned_straddlesLowerBound_T_86)
[1097] FIRRTL:361341 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_88 = or(_res_aligned_straddlesLowerBound_T_87, UInt<2>(0h3))
[1098] FIRRTL:361342 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_89 = not(_res_aligned_straddlesLowerBound_T_88)
[1099] FIRRTL:361343 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_90 = shr(_res_aligned_straddlesLowerBound_T_89, 3)
[1100] FIRRTL:361344 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_91 = xor(_res_aligned_straddlesLowerBound_T_85, _res_aligned_straddlesLowerBound_T_90)
[1101] FIRRTL:361345 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_92 = eq(_res_aligned_straddlesLowerBound_T_91, UInt<1>(0h0))
[1102] FIRRTL:361346 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_93 = shl(io.pmp[1].addr, 2)
[1103] FIRRTL:361347 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_94 = not(_res_aligned_straddlesLowerBound_T_93)
[1104] FIRRTL:361348 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_95 = or(_res_aligned_straddlesLowerBound_T_94, UInt<2>(0h3))
[1105] FIRRTL:361349 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_96 = not(_res_aligned_straddlesLowerBound_T_95)
[1106] FIRRTL:361350 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_97 = bits(_res_aligned_straddlesLowerBound_T_96, 2, 0)
[1107] FIRRTL:361351 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_98 = bits(io.addr, 2, 0)
[1108] FIRRTL:361352 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_99 = not(_res_aligned_straddlesLowerBound_T_98)
[1109] FIRRTL:361353 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_100 = and(_res_aligned_straddlesLowerBound_T_97, _res_aligned_straddlesLowerBound_T_99)
[1110] FIRRTL:361354 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_101 = neq(_res_aligned_straddlesLowerBound_T_100, UInt<1>(0h0))
[1111] FIRRTL:361355 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_5 = and(_res_aligned_straddlesLowerBound_T_92, _res_aligned_straddlesLowerBound_T_101)
[1112] FIRRTL:361356 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_85 = shr(io.addr, 3)
[1113] FIRRTL:361357 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_86 = shl(io.pmp[2].addr, 2)
[1114] FIRRTL:361358 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_87 = not(_res_aligned_straddlesUpperBound_T_86)
[1115] FIRRTL:361359 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_88 = or(_res_aligned_straddlesUpperBound_T_87, UInt<2>(0h3))
[1116] FIRRTL:361360 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_89 = not(_res_aligned_straddlesUpperBound_T_88)
[1117] FIRRTL:361361 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_90 = shr(_res_aligned_straddlesUpperBound_T_89, 3)
[1118] FIRRTL:361362 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_91 = xor(_res_aligned_straddlesUpperBound_T_85, _res_aligned_straddlesUpperBound_T_90)
[1119] FIRRTL:361363 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_92 = eq(_res_aligned_straddlesUpperBound_T_91, UInt<1>(0h0))
[1120] FIRRTL:361364 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_93 = shl(io.pmp[2].addr, 2)
[1121] FIRRTL:361365 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_94 = not(_res_aligned_straddlesUpperBound_T_93)
[1122] FIRRTL:361366 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_95 = or(_res_aligned_straddlesUpperBound_T_94, UInt<2>(0h3))
[1123] FIRRTL:361367 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_96 = not(_res_aligned_straddlesUpperBound_T_95)
[1124] FIRRTL:361368 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_97 = bits(_res_aligned_straddlesUpperBound_T_96, 2, 0)
[1125] FIRRTL:361369 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_98 = bits(io.addr, 2, 0)
[1126] FIRRTL:361370 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_99 = or(_res_aligned_straddlesUpperBound_T_98, res_aligned_lsbMask_5)
[1127] FIRRTL:361371 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_100 = and(_res_aligned_straddlesUpperBound_T_97, _res_aligned_straddlesUpperBound_T_99)
[1128] FIRRTL:361372 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_101 = neq(_res_aligned_straddlesUpperBound_T_100, UInt<1>(0h0))
[1129] FIRRTL:361373 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_5 = and(_res_aligned_straddlesUpperBound_T_92, _res_aligned_straddlesUpperBound_T_101)
[1130] FIRRTL:361374 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_5 = or(res_aligned_straddlesLowerBound_5, res_aligned_straddlesUpperBound_5)
[1131] FIRRTL:361375 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_5 = eq(_res_aligned_rangeAligned_T_5, UInt<1>(0h0))
[1132] FIRRTL:361376 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_15 = bits(io.pmp[2].mask, 2, 0)
[1133] FIRRTL:361377 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_16 = not(_res_aligned_pow2Aligned_T_15)
[1134] FIRRTL:361378 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_17 = and(res_aligned_lsbMask_5, _res_aligned_pow2Aligned_T_16)
[1135] FIRRTL:361379 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_5 = eq(_res_aligned_pow2Aligned_T_17, UInt<1>(0h0))
[1136] FIRRTL:361380 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_5 = bits(io.pmp[2].cfg.a, 1, 1)
[1137] FIRRTL:361381 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_5 = mux(_res_aligned_T_5, res_aligned_pow2Aligned_5, res_aligned_rangeAligned_5)
[1138] FIRRTL:361382 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_225 = eq(io.pmp[2].cfg.a, UInt<1>(0h0))
[1139] FIRRTL:361383 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_226 = eq(io.pmp[2].cfg.a, UInt<1>(0h1))
[1140] FIRRTL:361384 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_227 = eq(io.pmp[2].cfg.a, UInt<2>(0h2))
[1141] FIRRTL:361385 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_228 = eq(io.pmp[2].cfg.a, UInt<2>(0h3))
[1142] FIRRTL:361386 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_229 = eq(io.pmp[2].cfg.l, UInt<1>(0h1))
[1143] FIRRTL:361387 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_30 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1144] FIRRTL:361388 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_230 = cat(res_hi_30, io.pmp[2].cfg.r)
[1145] FIRRTL:361389 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_231 = eq(_res_T_230, UInt<1>(0h0))
[1146] FIRRTL:361390 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_31 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1147] FIRRTL:361391 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_232 = cat(res_hi_31, io.pmp[2].cfg.r)
[1148] FIRRTL:361392 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_233 = eq(_res_T_232, UInt<1>(0h1))
[1149] FIRRTL:361393 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_32 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1150] FIRRTL:361394 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_234 = cat(res_hi_32, io.pmp[2].cfg.r)
[1151] FIRRTL:361395 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_235 = eq(_res_T_234, UInt<2>(0h3))
[1152] FIRRTL:361396 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_33 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1153] FIRRTL:361397 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_236 = cat(res_hi_33, io.pmp[2].cfg.r)
[1154] FIRRTL:361398 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_237 = eq(_res_T_236, UInt<3>(0h4))
[1155] FIRRTL:361399 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_34 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1156] FIRRTL:361400 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_238 = cat(res_hi_34, io.pmp[2].cfg.r)
[1157] FIRRTL:361401 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_239 = eq(_res_T_238, UInt<3>(0h5))
[1158] FIRRTL:361402 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_35 = cat(io.pmp[2].cfg.x, io.pmp[2].cfg.w)
[1159] FIRRTL:361403 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_240 = cat(res_hi_35, io.pmp[2].cfg.r)
[1160] FIRRTL:361404 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_241 = eq(_res_T_240, UInt<3>(0h7))
[1161] FIRRTL:361405 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_242 = eq(res_ignore_5, UInt<1>(0h0))
[1162] FIRRTL:361406 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_243 = and(_res_T_242, res_hit_5)
[1163] FIRRTL:361407 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_244 = and(_res_T_243, res_aligned_5)
[1164] FIRRTL:361408 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_245 = eq(io.pmp[2].cfg.a, UInt<1>(0h1))
[1165] FIRRTL:361409 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_246 = and(_res_T_244, _res_T_245)
[1166] FIRRTL:361410 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_247 = and(io.pmp[2].cfg.l, res_hit_5)
[1167] FIRRTL:361411 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_248 = and(_res_T_247, res_aligned_5)
[1168] FIRRTL:361412 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_249 = eq(io.pmp[2].cfg.a, UInt<1>(0h1))
[1169] FIRRTL:361413 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_250 = and(_res_T_248, _res_T_249)
[1170] FIRRTL:361414 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_251 = eq(res_ignore_5, UInt<1>(0h0))
[1171] FIRRTL:361415 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_252 = and(_res_T_251, res_hit_5)
[1172] FIRRTL:361416 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_253 = and(_res_T_252, res_aligned_5)
[1173] FIRRTL:361417 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_254 = eq(io.pmp[2].cfg.a, UInt<2>(0h2))
[1174] FIRRTL:361418 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_255 = and(_res_T_253, _res_T_254)
[1175] FIRRTL:361419 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_256 = and(io.pmp[2].cfg.l, res_hit_5)
[1176] FIRRTL:361420 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_257 = and(_res_T_256, res_aligned_5)
[1177] FIRRTL:361421 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_258 = eq(io.pmp[2].cfg.a, UInt<2>(0h2))
[1178] FIRRTL:361422 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_259 = and(_res_T_257, _res_T_258)
[1179] FIRRTL:361423 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_260 = eq(res_ignore_5, UInt<1>(0h0))
[1180] FIRRTL:361424 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_261 = and(_res_T_260, res_hit_5)
[1181] FIRRTL:361425 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_262 = and(_res_T_261, res_aligned_5)
[1182] FIRRTL:361426 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_263 = eq(io.pmp[2].cfg.a, UInt<2>(0h3))
[1183] FIRRTL:361427 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_264 = and(_res_T_262, _res_T_263)
[1184] FIRRTL:361428 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_265 = and(io.pmp[2].cfg.l, res_hit_5)
[1185] FIRRTL:361429 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_266 = and(_res_T_265, res_aligned_5)
[1186] FIRRTL:361430 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_267 = eq(io.pmp[2].cfg.a, UInt<2>(0h3))
[1187] FIRRTL:361431 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_268 = and(_res_T_266, _res_T_267)
[1188] FIRRTL:361432 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_5 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[1189] FIRRTL:361433 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_5, io.pmp[2]
[1190] FIRRTL:361434 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_10 = or(io.pmp[2].cfg.r, res_ignore_5)
[1191] FIRRTL:361435 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_11 = and(res_aligned_5, _res_cur_cfg_r_T_10)
[1192] FIRRTL:361436 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_5.cfg.r, _res_cur_cfg_r_T_11
[1193] FIRRTL:361437 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_10 = or(io.pmp[2].cfg.w, res_ignore_5)
[1194] FIRRTL:361438 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_11 = and(res_aligned_5, _res_cur_cfg_w_T_10)
[1195] FIRRTL:361439 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_5.cfg.w, _res_cur_cfg_w_T_11
[1196] FIRRTL:361440 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_10 = or(io.pmp[2].cfg.x, res_ignore_5)
[1197] FIRRTL:361441 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_11 = and(res_aligned_5, _res_cur_cfg_x_T_10)
[1198] FIRRTL:361442 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_5.cfg.x, _res_cur_cfg_x_T_11
[1199] FIRRTL:361443 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_269 = mux(res_hit_5, res_cur_5, _res_T_224)
[1200] FIRRTL:361444 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_78 = bits(io.pmp[1].cfg.a, 1, 1)
[1201] FIRRTL:361445 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_18 = dshl(UInt<3>(0h7), io.size)
[1202] FIRRTL:361446 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_19 = bits(_res_hit_lsbMask_T_18, 2, 0)
[1203] FIRRTL:361447 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_20 = not(_res_hit_lsbMask_T_19)
[1204] FIRRTL:361448 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_6 = or(io.pmp[1].mask, _res_hit_lsbMask_T_20)
[1205] FIRRTL:361449 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_60 = shr(io.addr, 3)
[1206] FIRRTL:361450 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_61 = shl(io.pmp[1].addr, 2)
[1207] FIRRTL:361451 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_62 = not(_res_hit_msbMatch_T_61)
[1208] FIRRTL:361452 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_63 = or(_res_hit_msbMatch_T_62, UInt<2>(0h3))
[1209] FIRRTL:361453 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_64 = not(_res_hit_msbMatch_T_63)
[1210] FIRRTL:361454 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_65 = shr(_res_hit_msbMatch_T_64, 3)
[1211] FIRRTL:361455 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_66 = shr(io.pmp[1].mask, 3)
[1212] FIRRTL:361456 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_67 = xor(_res_hit_msbMatch_T_60, _res_hit_msbMatch_T_65)
[1213] FIRRTL:361457 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_68 = not(_res_hit_msbMatch_T_66)
[1214] FIRRTL:361458 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_69 = and(_res_hit_msbMatch_T_67, _res_hit_msbMatch_T_68)
[1215] FIRRTL:361459 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_6 = eq(_res_hit_msbMatch_T_69, UInt<1>(0h0))
[1216] FIRRTL:361460 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_60 = bits(io.addr, 2, 0)
[1217] FIRRTL:361461 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_61 = shl(io.pmp[1].addr, 2)
[1218] FIRRTL:361462 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_62 = not(_res_hit_lsbMatch_T_61)
[1219] FIRRTL:361463 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_63 = or(_res_hit_lsbMatch_T_62, UInt<2>(0h3))
[1220] FIRRTL:361464 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_64 = not(_res_hit_lsbMatch_T_63)
[1221] FIRRTL:361465 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_65 = bits(_res_hit_lsbMatch_T_64, 2, 0)
[1222] FIRRTL:361466 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_66 = bits(res_hit_lsbMask_6, 2, 0)
[1223] FIRRTL:361467 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_67 = xor(_res_hit_lsbMatch_T_60, _res_hit_lsbMatch_T_65)
[1224] FIRRTL:361468 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_68 = not(_res_hit_lsbMatch_T_66)
[1225] FIRRTL:361469 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_69 = and(_res_hit_lsbMatch_T_67, _res_hit_lsbMatch_T_68)
[1226] FIRRTL:361470 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_6 = eq(_res_hit_lsbMatch_T_69, UInt<1>(0h0))
[1227] FIRRTL:361471 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_79 = and(res_hit_msbMatch_6, res_hit_lsbMatch_6)
[1228] FIRRTL:361472 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_80 = bits(io.pmp[1].cfg.a, 0, 0)
[1229] FIRRTL:361473 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_81 = dshl(UInt<3>(0h7), io.size)
[1230] FIRRTL:361474 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_82 = bits(_res_hit_T_81, 2, 0)
[1231] FIRRTL:361475 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_83 = not(_res_hit_T_82)
[1232] FIRRTL:361476 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_72 = shr(io.addr, 3)
[1233] FIRRTL:361477 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_73 = shl(io.pmp[0].addr, 2)
[1234] FIRRTL:361478 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_74 = not(_res_hit_msbsLess_T_73)
[1235] FIRRTL:361479 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_75 = or(_res_hit_msbsLess_T_74, UInt<2>(0h3))
[1236] FIRRTL:361480 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_76 = not(_res_hit_msbsLess_T_75)
[1237] FIRRTL:361481 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_77 = shr(_res_hit_msbsLess_T_76, 3)
[1238] FIRRTL:361482 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_12 = lt(_res_hit_msbsLess_T_72, _res_hit_msbsLess_T_77)
[1239] FIRRTL:361483 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_84 = shr(io.addr, 3)
[1240] FIRRTL:361484 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_85 = shl(io.pmp[0].addr, 2)
[1241] FIRRTL:361485 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_86 = not(_res_hit_msbsEqual_T_85)
[1242] FIRRTL:361486 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_87 = or(_res_hit_msbsEqual_T_86, UInt<2>(0h3))
[1243] FIRRTL:361487 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_88 = not(_res_hit_msbsEqual_T_87)
[1244] FIRRTL:361488 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_89 = shr(_res_hit_msbsEqual_T_88, 3)
[1245] FIRRTL:361489 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_90 = xor(_res_hit_msbsEqual_T_84, _res_hit_msbsEqual_T_89)
[1246] FIRRTL:361490 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_12 = eq(_res_hit_msbsEqual_T_90, UInt<1>(0h0))
[1247] FIRRTL:361491 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_84 = bits(io.addr, 2, 0)
[1248] FIRRTL:361492 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_85 = or(_res_hit_lsbsLess_T_84, _res_hit_T_83)
[1249] FIRRTL:361493 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_86 = shl(io.pmp[0].addr, 2)
[1250] FIRRTL:361494 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_87 = not(_res_hit_lsbsLess_T_86)
[1251] FIRRTL:361495 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_88 = or(_res_hit_lsbsLess_T_87, UInt<2>(0h3))
[1252] FIRRTL:361496 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_89 = not(_res_hit_lsbsLess_T_88)
[1253] FIRRTL:361497 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_90 = bits(_res_hit_lsbsLess_T_89, 2, 0)
[1254] FIRRTL:361498 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_12 = lt(_res_hit_lsbsLess_T_85, _res_hit_lsbsLess_T_90)
[1255] FIRRTL:361499 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_84 = and(res_hit_msbsEqual_12, res_hit_lsbsLess_12)
[1256] FIRRTL:361500 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_85 = or(res_hit_msbsLess_12, _res_hit_T_84)
[1257] FIRRTL:361501 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_86 = eq(_res_hit_T_85, UInt<1>(0h0))
[1258] FIRRTL:361502 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_78 = shr(io.addr, 3)
[1259] FIRRTL:361503 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_79 = shl(io.pmp[1].addr, 2)
[1260] FIRRTL:361504 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_80 = not(_res_hit_msbsLess_T_79)
[1261] FIRRTL:361505 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_81 = or(_res_hit_msbsLess_T_80, UInt<2>(0h3))
[1262] FIRRTL:361506 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_82 = not(_res_hit_msbsLess_T_81)
[1263] FIRRTL:361507 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_83 = shr(_res_hit_msbsLess_T_82, 3)
[1264] FIRRTL:361508 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_13 = lt(_res_hit_msbsLess_T_78, _res_hit_msbsLess_T_83)
[1265] FIRRTL:361509 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_91 = shr(io.addr, 3)
[1266] FIRRTL:361510 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_92 = shl(io.pmp[1].addr, 2)
[1267] FIRRTL:361511 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_93 = not(_res_hit_msbsEqual_T_92)
[1268] FIRRTL:361512 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_94 = or(_res_hit_msbsEqual_T_93, UInt<2>(0h3))
[1269] FIRRTL:361513 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_95 = not(_res_hit_msbsEqual_T_94)
[1270] FIRRTL:361514 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_96 = shr(_res_hit_msbsEqual_T_95, 3)
[1271] FIRRTL:361515 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_97 = xor(_res_hit_msbsEqual_T_91, _res_hit_msbsEqual_T_96)
[1272] FIRRTL:361516 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_13 = eq(_res_hit_msbsEqual_T_97, UInt<1>(0h0))
[1273] FIRRTL:361517 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_91 = bits(io.addr, 2, 0)
[1274] FIRRTL:361518 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_92 = or(_res_hit_lsbsLess_T_91, UInt<1>(0h0))
[1275] FIRRTL:361519 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_93 = shl(io.pmp[1].addr, 2)
[1276] FIRRTL:361520 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_94 = not(_res_hit_lsbsLess_T_93)
[1277] FIRRTL:361521 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_95 = or(_res_hit_lsbsLess_T_94, UInt<2>(0h3))
[1278] FIRRTL:361522 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_96 = not(_res_hit_lsbsLess_T_95)
[1279] FIRRTL:361523 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_97 = bits(_res_hit_lsbsLess_T_96, 2, 0)
[1280] FIRRTL:361524 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_13 = lt(_res_hit_lsbsLess_T_92, _res_hit_lsbsLess_T_97)
[1281] FIRRTL:361525 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_87 = and(res_hit_msbsEqual_13, res_hit_lsbsLess_13)
[1282] FIRRTL:361526 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_88 = or(res_hit_msbsLess_13, _res_hit_T_87)
[1283] FIRRTL:361527 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_89 = and(_res_hit_T_86, _res_hit_T_88)
[1284] FIRRTL:361528 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_90 = and(_res_hit_T_80, _res_hit_T_89)
[1285] FIRRTL:361529 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_6 = mux(_res_hit_T_78, _res_hit_T_79, _res_hit_T_90)
[1286] FIRRTL:361530 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_6 = eq(io.pmp[1].cfg.l, UInt<1>(0h0))
[1287] FIRRTL:361531 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_6 = and(default, _res_ignore_T_6)
[1288] FIRRTL:361532 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_12 = dshl(UInt<3>(0h7), io.size)
[1289] FIRRTL:361533 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_13 = bits(_res_aligned_lsbMask_T_12, 2, 0)
[1290] FIRRTL:361534 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_6 = not(_res_aligned_lsbMask_T_13)
[1291] FIRRTL:361535 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_102 = shr(io.addr, 3)
[1292] FIRRTL:361536 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_103 = shl(io.pmp[0].addr, 2)
[1293] FIRRTL:361537 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_104 = not(_res_aligned_straddlesLowerBound_T_103)
[1294] FIRRTL:361538 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_105 = or(_res_aligned_straddlesLowerBound_T_104, UInt<2>(0h3))
[1295] FIRRTL:361539 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_106 = not(_res_aligned_straddlesLowerBound_T_105)
[1296] FIRRTL:361540 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_107 = shr(_res_aligned_straddlesLowerBound_T_106, 3)
[1297] FIRRTL:361541 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_108 = xor(_res_aligned_straddlesLowerBound_T_102, _res_aligned_straddlesLowerBound_T_107)
[1298] FIRRTL:361542 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_109 = eq(_res_aligned_straddlesLowerBound_T_108, UInt<1>(0h0))
[1299] FIRRTL:361543 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_110 = shl(io.pmp[0].addr, 2)
[1300] FIRRTL:361544 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_111 = not(_res_aligned_straddlesLowerBound_T_110)
[1301] FIRRTL:361545 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_112 = or(_res_aligned_straddlesLowerBound_T_111, UInt<2>(0h3))
[1302] FIRRTL:361546 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_113 = not(_res_aligned_straddlesLowerBound_T_112)
[1303] FIRRTL:361547 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_114 = bits(_res_aligned_straddlesLowerBound_T_113, 2, 0)
[1304] FIRRTL:361548 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_115 = bits(io.addr, 2, 0)
[1305] FIRRTL:361549 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_116 = not(_res_aligned_straddlesLowerBound_T_115)
[1306] FIRRTL:361550 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_117 = and(_res_aligned_straddlesLowerBound_T_114, _res_aligned_straddlesLowerBound_T_116)
[1307] FIRRTL:361551 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_118 = neq(_res_aligned_straddlesLowerBound_T_117, UInt<1>(0h0))
[1308] FIRRTL:361552 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_6 = and(_res_aligned_straddlesLowerBound_T_109, _res_aligned_straddlesLowerBound_T_118)
[1309] FIRRTL:361553 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_102 = shr(io.addr, 3)
[1310] FIRRTL:361554 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_103 = shl(io.pmp[1].addr, 2)
[1311] FIRRTL:361555 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_104 = not(_res_aligned_straddlesUpperBound_T_103)
[1312] FIRRTL:361556 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_105 = or(_res_aligned_straddlesUpperBound_T_104, UInt<2>(0h3))
[1313] FIRRTL:361557 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_106 = not(_res_aligned_straddlesUpperBound_T_105)
[1314] FIRRTL:361558 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_107 = shr(_res_aligned_straddlesUpperBound_T_106, 3)
[1315] FIRRTL:361559 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_108 = xor(_res_aligned_straddlesUpperBound_T_102, _res_aligned_straddlesUpperBound_T_107)
[1316] FIRRTL:361560 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_109 = eq(_res_aligned_straddlesUpperBound_T_108, UInt<1>(0h0))
[1317] FIRRTL:361561 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_110 = shl(io.pmp[1].addr, 2)
[1318] FIRRTL:361562 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_111 = not(_res_aligned_straddlesUpperBound_T_110)
[1319] FIRRTL:361563 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_112 = or(_res_aligned_straddlesUpperBound_T_111, UInt<2>(0h3))
[1320] FIRRTL:361564 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_113 = not(_res_aligned_straddlesUpperBound_T_112)
[1321] FIRRTL:361565 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_114 = bits(_res_aligned_straddlesUpperBound_T_113, 2, 0)
[1322] FIRRTL:361566 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_115 = bits(io.addr, 2, 0)
[1323] FIRRTL:361567 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_116 = or(_res_aligned_straddlesUpperBound_T_115, res_aligned_lsbMask_6)
[1324] FIRRTL:361568 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_117 = and(_res_aligned_straddlesUpperBound_T_114, _res_aligned_straddlesUpperBound_T_116)
[1325] FIRRTL:361569 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_118 = neq(_res_aligned_straddlesUpperBound_T_117, UInt<1>(0h0))
[1326] FIRRTL:361570 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_6 = and(_res_aligned_straddlesUpperBound_T_109, _res_aligned_straddlesUpperBound_T_118)
[1327] FIRRTL:361571 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_6 = or(res_aligned_straddlesLowerBound_6, res_aligned_straddlesUpperBound_6)
[1328] FIRRTL:361572 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_6 = eq(_res_aligned_rangeAligned_T_6, UInt<1>(0h0))
[1329] FIRRTL:361573 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_18 = bits(io.pmp[1].mask, 2, 0)
[1330] FIRRTL:361574 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_19 = not(_res_aligned_pow2Aligned_T_18)
[1331] FIRRTL:361575 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_20 = and(res_aligned_lsbMask_6, _res_aligned_pow2Aligned_T_19)
[1332] FIRRTL:361576 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_6 = eq(_res_aligned_pow2Aligned_T_20, UInt<1>(0h0))
[1333] FIRRTL:361577 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_6 = bits(io.pmp[1].cfg.a, 1, 1)
[1334] FIRRTL:361578 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_6 = mux(_res_aligned_T_6, res_aligned_pow2Aligned_6, res_aligned_rangeAligned_6)
[1335] FIRRTL:361579 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_270 = eq(io.pmp[1].cfg.a, UInt<1>(0h0))
[1336] FIRRTL:361580 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_271 = eq(io.pmp[1].cfg.a, UInt<1>(0h1))
[1337] FIRRTL:361581 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_272 = eq(io.pmp[1].cfg.a, UInt<2>(0h2))
[1338] FIRRTL:361582 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_273 = eq(io.pmp[1].cfg.a, UInt<2>(0h3))
[1339] FIRRTL:361583 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_274 = eq(io.pmp[1].cfg.l, UInt<1>(0h1))
[1340] FIRRTL:361584 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_36 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1341] FIRRTL:361585 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_275 = cat(res_hi_36, io.pmp[1].cfg.r)
[1342] FIRRTL:361586 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_276 = eq(_res_T_275, UInt<1>(0h0))
[1343] FIRRTL:361587 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_37 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1344] FIRRTL:361588 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_277 = cat(res_hi_37, io.pmp[1].cfg.r)
[1345] FIRRTL:361589 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_278 = eq(_res_T_277, UInt<1>(0h1))
[1346] FIRRTL:361590 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_38 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1347] FIRRTL:361591 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_279 = cat(res_hi_38, io.pmp[1].cfg.r)
[1348] FIRRTL:361592 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_280 = eq(_res_T_279, UInt<2>(0h3))
[1349] FIRRTL:361593 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_39 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1350] FIRRTL:361594 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_281 = cat(res_hi_39, io.pmp[1].cfg.r)
[1351] FIRRTL:361595 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_282 = eq(_res_T_281, UInt<3>(0h4))
[1352] FIRRTL:361596 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_40 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1353] FIRRTL:361597 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_283 = cat(res_hi_40, io.pmp[1].cfg.r)
[1354] FIRRTL:361598 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_284 = eq(_res_T_283, UInt<3>(0h5))
[1355] FIRRTL:361599 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_41 = cat(io.pmp[1].cfg.x, io.pmp[1].cfg.w)
[1356] FIRRTL:361600 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_285 = cat(res_hi_41, io.pmp[1].cfg.r)
[1357] FIRRTL:361601 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_286 = eq(_res_T_285, UInt<3>(0h7))
[1358] FIRRTL:361602 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_287 = eq(res_ignore_6, UInt<1>(0h0))
[1359] FIRRTL:361603 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_288 = and(_res_T_287, res_hit_6)
[1360] FIRRTL:361604 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_289 = and(_res_T_288, res_aligned_6)
[1361] FIRRTL:361605 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_290 = eq(io.pmp[1].cfg.a, UInt<1>(0h1))
[1362] FIRRTL:361606 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_291 = and(_res_T_289, _res_T_290)
[1363] FIRRTL:361607 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_292 = and(io.pmp[1].cfg.l, res_hit_6)
[1364] FIRRTL:361608 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_293 = and(_res_T_292, res_aligned_6)
[1365] FIRRTL:361609 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_294 = eq(io.pmp[1].cfg.a, UInt<1>(0h1))
[1366] FIRRTL:361610 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_295 = and(_res_T_293, _res_T_294)
[1367] FIRRTL:361611 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_296 = eq(res_ignore_6, UInt<1>(0h0))
[1368] FIRRTL:361612 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_297 = and(_res_T_296, res_hit_6)
[1369] FIRRTL:361613 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_298 = and(_res_T_297, res_aligned_6)
[1370] FIRRTL:361614 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_299 = eq(io.pmp[1].cfg.a, UInt<2>(0h2))
[1371] FIRRTL:361615 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_300 = and(_res_T_298, _res_T_299)
[1372] FIRRTL:361616 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_301 = and(io.pmp[1].cfg.l, res_hit_6)
[1373] FIRRTL:361617 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_302 = and(_res_T_301, res_aligned_6)
[1374] FIRRTL:361618 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_303 = eq(io.pmp[1].cfg.a, UInt<2>(0h2))
[1375] FIRRTL:361619 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_304 = and(_res_T_302, _res_T_303)
[1376] FIRRTL:361620 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_305 = eq(res_ignore_6, UInt<1>(0h0))
[1377] FIRRTL:361621 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_306 = and(_res_T_305, res_hit_6)
[1378] FIRRTL:361622 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_307 = and(_res_T_306, res_aligned_6)
[1379] FIRRTL:361623 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_308 = eq(io.pmp[1].cfg.a, UInt<2>(0h3))
[1380] FIRRTL:361624 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_309 = and(_res_T_307, _res_T_308)
[1381] FIRRTL:361625 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_310 = and(io.pmp[1].cfg.l, res_hit_6)
[1382] FIRRTL:361626 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_311 = and(_res_T_310, res_aligned_6)
[1383] FIRRTL:361627 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_312 = eq(io.pmp[1].cfg.a, UInt<2>(0h3))
[1384] FIRRTL:361628 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_313 = and(_res_T_311, _res_T_312)
[1385] FIRRTL:361629 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_6 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[1386] FIRRTL:361630 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_6, io.pmp[1]
[1387] FIRRTL:361631 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_12 = or(io.pmp[1].cfg.r, res_ignore_6)
[1388] FIRRTL:361632 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_13 = and(res_aligned_6, _res_cur_cfg_r_T_12)
[1389] FIRRTL:361633 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_6.cfg.r, _res_cur_cfg_r_T_13
[1390] FIRRTL:361634 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_12 = or(io.pmp[1].cfg.w, res_ignore_6)
[1391] FIRRTL:361635 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_13 = and(res_aligned_6, _res_cur_cfg_w_T_12)
[1392] FIRRTL:361636 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_6.cfg.w, _res_cur_cfg_w_T_13
[1393] FIRRTL:361637 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_12 = or(io.pmp[1].cfg.x, res_ignore_6)
[1394] FIRRTL:361638 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_13 = and(res_aligned_6, _res_cur_cfg_x_T_12)
[1395] FIRRTL:361639 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_6.cfg.x, _res_cur_cfg_x_T_13
[1396] FIRRTL:361640 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node _res_T_314 = mux(res_hit_6, res_cur_6, _res_T_269)
[1397] FIRRTL:361641 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_hit_T_91 = bits(io.pmp[0].cfg.a, 1, 1)
[1398] FIRRTL:361642 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_lsbMask_T_21 = dshl(UInt<3>(0h7), io.size)
[1399] FIRRTL:361643 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_lsbMask_T_22 = bits(_res_hit_lsbMask_T_21, 2, 0)
[1400] FIRRTL:361644 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_lsbMask_T_23 = not(_res_hit_lsbMask_T_22)
[1401] FIRRTL:361645 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:68:26 KIND:node :: node res_hit_lsbMask_7 = or(io.pmp[0].mask, _res_hit_lsbMask_T_23)
[1402] FIRRTL:361646 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:29 KIND:node :: node _res_hit_msbMatch_T_70 = shr(io.addr, 3)
[1403] FIRRTL:361647 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbMatch_T_71 = shl(io.pmp[0].addr, 2)
[1404] FIRRTL:361648 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbMatch_T_72 = not(_res_hit_msbMatch_T_71)
[1405] FIRRTL:361649 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbMatch_T_73 = or(_res_hit_msbMatch_T_72, UInt<2>(0h3))
[1406] FIRRTL:361650 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbMatch_T_74 = not(_res_hit_msbMatch_T_73)
[1407] FIRRTL:361651 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:53 KIND:node :: node _res_hit_msbMatch_T_75 = shr(_res_hit_msbMatch_T_74, 3)
[1408] FIRRTL:361652 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:69:72 KIND:node :: node _res_hit_msbMatch_T_76 = shr(io.pmp[0].mask, 3)
[1409] FIRRTL:361653 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_msbMatch_T_77 = xor(_res_hit_msbMatch_T_70, _res_hit_msbMatch_T_75)
[1410] FIRRTL:361654 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_msbMatch_T_78 = not(_res_hit_msbMatch_T_76)
[1411] FIRRTL:361655 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_msbMatch_T_79 = and(_res_hit_msbMatch_T_77, _res_hit_msbMatch_T_78)
[1412] FIRRTL:361656 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_msbMatch_7 = eq(_res_hit_msbMatch_T_79, UInt<1>(0h0))
[1413] FIRRTL:361657 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:28 KIND:node :: node _res_hit_lsbMatch_T_70 = bits(io.addr, 2, 0)
[1414] FIRRTL:361658 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbMatch_T_71 = shl(io.pmp[0].addr, 2)
[1415] FIRRTL:361659 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbMatch_T_72 = not(_res_hit_lsbMatch_T_71)
[1416] FIRRTL:361660 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbMatch_T_73 = or(_res_hit_lsbMatch_T_72, UInt<2>(0h3))
[1417] FIRRTL:361661 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbMatch_T_74 = not(_res_hit_lsbMatch_T_73)
[1418] FIRRTL:361662 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:55 KIND:node :: node _res_hit_lsbMatch_T_75 = bits(_res_hit_lsbMatch_T_74, 2, 0)
[1419] FIRRTL:361663 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:70:80 KIND:node :: node _res_hit_lsbMatch_T_76 = bits(res_hit_lsbMask_7, 2, 0)
[1420] FIRRTL:361664 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:47 KIND:node :: node _res_hit_lsbMatch_T_77 = xor(_res_hit_lsbMatch_T_70, _res_hit_lsbMatch_T_75)
[1421] FIRRTL:361665 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:54 KIND:node :: node _res_hit_lsbMatch_T_78 = not(_res_hit_lsbMatch_T_76)
[1422] FIRRTL:361666 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:52 KIND:node :: node _res_hit_lsbMatch_T_79 = and(_res_hit_lsbMatch_T_77, _res_hit_lsbMatch_T_78)
[1423] FIRRTL:361667 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:63:58 KIND:node :: node res_hit_lsbMatch_7 = eq(_res_hit_lsbMatch_T_79, UInt<1>(0h0))
[1424] FIRRTL:361668 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:71:16 KIND:node :: node _res_hit_T_92 = and(res_hit_msbMatch_7, res_hit_lsbMatch_7)
[1425] FIRRTL:361669 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:46:26 KIND:node :: node _res_hit_T_93 = bits(io.pmp[0].cfg.a, 0, 0)
[1426] FIRRTL:361670 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_hit_T_94 = dshl(UInt<3>(0h7), io.size)
[1427] FIRRTL:361671 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_hit_T_95 = bits(_res_hit_T_94, 2, 0)
[1428] FIRRTL:361672 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _res_hit_T_96 = not(_res_hit_T_95)
[1429] FIRRTL:361673 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_84 = shr(io.addr, 3)
[1430] FIRRTL:361674 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_85 = shl(pmp0.addr, 2)
[1431] FIRRTL:361675 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_86 = not(_res_hit_msbsLess_T_85)
[1432] FIRRTL:361676 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_87 = or(_res_hit_msbsLess_T_86, UInt<2>(0h3))
[1433] FIRRTL:361677 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_88 = not(_res_hit_msbsLess_T_87)
[1434] FIRRTL:361678 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_89 = shr(_res_hit_msbsLess_T_88, 3)
[1435] FIRRTL:361679 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_14 = lt(_res_hit_msbsLess_T_84, _res_hit_msbsLess_T_89)
[1436] FIRRTL:361680 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_98 = shr(io.addr, 3)
[1437] FIRRTL:361681 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_99 = shl(pmp0.addr, 2)
[1438] FIRRTL:361682 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_100 = not(_res_hit_msbsEqual_T_99)
[1439] FIRRTL:361683 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_101 = or(_res_hit_msbsEqual_T_100, UInt<2>(0h3))
[1440] FIRRTL:361684 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_102 = not(_res_hit_msbsEqual_T_101)
[1441] FIRRTL:361685 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_103 = shr(_res_hit_msbsEqual_T_102, 3)
[1442] FIRRTL:361686 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_104 = xor(_res_hit_msbsEqual_T_98, _res_hit_msbsEqual_T_103)
[1443] FIRRTL:361687 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_14 = eq(_res_hit_msbsEqual_T_104, UInt<1>(0h0))
[1444] FIRRTL:361688 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_98 = bits(io.addr, 2, 0)
[1445] FIRRTL:361689 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_99 = or(_res_hit_lsbsLess_T_98, _res_hit_T_96)
[1446] FIRRTL:361690 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_100 = shl(pmp0.addr, 2)
[1447] FIRRTL:361691 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_101 = not(_res_hit_lsbsLess_T_100)
[1448] FIRRTL:361692 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_102 = or(_res_hit_lsbsLess_T_101, UInt<2>(0h3))
[1449] FIRRTL:361693 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_103 = not(_res_hit_lsbsLess_T_102)
[1450] FIRRTL:361694 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_104 = bits(_res_hit_lsbsLess_T_103, 2, 0)
[1451] FIRRTL:361695 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_14 = lt(_res_hit_lsbsLess_T_99, _res_hit_lsbsLess_T_104)
[1452] FIRRTL:361696 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_97 = and(res_hit_msbsEqual_14, res_hit_lsbsLess_14)
[1453] FIRRTL:361697 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_98 = or(res_hit_msbsLess_14, _res_hit_T_97)
[1454] FIRRTL:361698 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:88:5 KIND:node :: node _res_hit_T_99 = eq(_res_hit_T_98, UInt<1>(0h0))
[1455] FIRRTL:361699 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:25 KIND:node :: node _res_hit_msbsLess_T_90 = shr(io.addr, 3)
[1456] FIRRTL:361700 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsLess_T_91 = shl(io.pmp[0].addr, 2)
[1457] FIRRTL:361701 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsLess_T_92 = not(_res_hit_msbsLess_T_91)
[1458] FIRRTL:361702 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsLess_T_93 = or(_res_hit_msbsLess_T_92, UInt<2>(0h3))
[1459] FIRRTL:361703 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsLess_T_94 = not(_res_hit_msbsLess_T_93)
[1460] FIRRTL:361704 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:52 KIND:node :: node _res_hit_msbsLess_T_95 = shr(_res_hit_msbsLess_T_94, 3)
[1461] FIRRTL:361705 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:80:39 KIND:node :: node res_hit_msbsLess_15 = lt(_res_hit_msbsLess_T_90, _res_hit_msbsLess_T_95)
[1462] FIRRTL:361706 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:27 KIND:node :: node _res_hit_msbsEqual_T_105 = shr(io.addr, 3)
[1463] FIRRTL:361707 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_msbsEqual_T_106 = shl(io.pmp[0].addr, 2)
[1464] FIRRTL:361708 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_msbsEqual_T_107 = not(_res_hit_msbsEqual_T_106)
[1465] FIRRTL:361709 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_msbsEqual_T_108 = or(_res_hit_msbsEqual_T_107, UInt<2>(0h3))
[1466] FIRRTL:361710 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_msbsEqual_T_109 = not(_res_hit_msbsEqual_T_108)
[1467] FIRRTL:361711 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:54 KIND:node :: node _res_hit_msbsEqual_T_110 = shr(_res_hit_msbsEqual_T_109, 3)
[1468] FIRRTL:361712 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:41 KIND:node :: node _res_hit_msbsEqual_T_111 = xor(_res_hit_msbsEqual_T_105, _res_hit_msbsEqual_T_110)
[1469] FIRRTL:361713 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:81:69 KIND:node :: node res_hit_msbsEqual_15 = eq(_res_hit_msbsEqual_T_111, UInt<1>(0h0))
[1470] FIRRTL:361714 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:25 KIND:node :: node _res_hit_lsbsLess_T_105 = bits(io.addr, 2, 0)
[1471] FIRRTL:361715 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:42 KIND:node :: node _res_hit_lsbsLess_T_106 = or(_res_hit_lsbsLess_T_105, UInt<1>(0h0))
[1472] FIRRTL:361716 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_hit_lsbsLess_T_107 = shl(io.pmp[0].addr, 2)
[1473] FIRRTL:361717 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_hit_lsbsLess_T_108 = not(_res_hit_lsbsLess_T_107)
[1474] FIRRTL:361718 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_hit_lsbsLess_T_109 = or(_res_hit_lsbsLess_T_108, UInt<2>(0h3))
[1475] FIRRTL:361719 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_hit_lsbsLess_T_110 = not(_res_hit_lsbsLess_T_109)
[1476] FIRRTL:361720 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:64 KIND:node :: node _res_hit_lsbsLess_T_111 = bits(_res_hit_lsbsLess_T_110, 2, 0)
[1477] FIRRTL:361721 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:82:53 KIND:node :: node res_hit_lsbsLess_15 = lt(_res_hit_lsbsLess_T_106, _res_hit_lsbsLess_T_111)
[1478] FIRRTL:361722 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:30 KIND:node :: node _res_hit_T_100 = and(res_hit_msbsEqual_15, res_hit_lsbsLess_15)
[1479] FIRRTL:361723 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:83:16 KIND:node :: node _res_hit_T_101 = or(res_hit_msbsLess_15, _res_hit_T_100)
[1480] FIRRTL:361724 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:94:48 KIND:node :: node _res_hit_T_102 = and(_res_hit_T_99, _res_hit_T_101)
[1481] FIRRTL:361725 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:61 KIND:node :: node _res_hit_T_103 = and(_res_hit_T_93, _res_hit_T_102)
[1482] FIRRTL:361726 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:132:8 KIND:node :: node res_hit_7 = mux(_res_hit_T_91, _res_hit_T_92, _res_hit_T_103)
[1483] FIRRTL:361727 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:29 KIND:node :: node _res_ignore_T_7 = eq(io.pmp[0].cfg.l, UInt<1>(0h0))
[1484] FIRRTL:361728 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:164:26 KIND:node :: node res_ignore_7 = and(default, _res_ignore_T_7)
[1485] FIRRTL:361729 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _res_aligned_lsbMask_T_14 = dshl(UInt<3>(0h7), io.size)
[1486] FIRRTL:361730 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _res_aligned_lsbMask_T_15 = bits(_res_aligned_lsbMask_T_14, 2, 0)
[1487] FIRRTL:361731 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node res_aligned_lsbMask_7 = not(_res_aligned_lsbMask_T_15)
[1488] FIRRTL:361732 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:35 KIND:node :: node _res_aligned_straddlesLowerBound_T_119 = shr(io.addr, 3)
[1489] FIRRTL:361733 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_120 = shl(pmp0.addr, 2)
[1490] FIRRTL:361734 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_121 = not(_res_aligned_straddlesLowerBound_T_120)
[1491] FIRRTL:361735 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_122 = or(_res_aligned_straddlesLowerBound_T_121, UInt<2>(0h3))
[1492] FIRRTL:361736 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_123 = not(_res_aligned_straddlesLowerBound_T_122)
[1493] FIRRTL:361737 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:67 KIND:node :: node _res_aligned_straddlesLowerBound_T_124 = shr(_res_aligned_straddlesLowerBound_T_123, 3)
[1494] FIRRTL:361738 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:49 KIND:node :: node _res_aligned_straddlesLowerBound_T_125 = xor(_res_aligned_straddlesLowerBound_T_119, _res_aligned_straddlesLowerBound_T_124)
[1495] FIRRTL:361739 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:82 KIND:node :: node _res_aligned_straddlesLowerBound_T_126 = eq(_res_aligned_straddlesLowerBound_T_125, UInt<1>(0h0))
[1496] FIRRTL:361740 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesLowerBound_T_127 = shl(pmp0.addr, 2)
[1497] FIRRTL:361741 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesLowerBound_T_128 = not(_res_aligned_straddlesLowerBound_T_127)
[1498] FIRRTL:361742 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesLowerBound_T_129 = or(_res_aligned_straddlesLowerBound_T_128, UInt<2>(0h3))
[1499] FIRRTL:361743 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesLowerBound_T_130 = not(_res_aligned_straddlesLowerBound_T_129)
[1500] FIRRTL:361744 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:108 KIND:node :: node _res_aligned_straddlesLowerBound_T_131 = bits(_res_aligned_straddlesLowerBound_T_130, 2, 0)
[1501] FIRRTL:361745 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:129 KIND:node :: node _res_aligned_straddlesLowerBound_T_132 = bits(io.addr, 2, 0)
[1502] FIRRTL:361746 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:127 KIND:node :: node _res_aligned_straddlesLowerBound_T_133 = not(_res_aligned_straddlesLowerBound_T_132)
[1503] FIRRTL:361747 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:125 KIND:node :: node _res_aligned_straddlesLowerBound_T_134 = and(_res_aligned_straddlesLowerBound_T_131, _res_aligned_straddlesLowerBound_T_133)
[1504] FIRRTL:361748 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:147 KIND:node :: node _res_aligned_straddlesLowerBound_T_135 = neq(_res_aligned_straddlesLowerBound_T_134, UInt<1>(0h0))
[1505] FIRRTL:361749 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:123:90 KIND:node :: node res_aligned_straddlesLowerBound_7 = and(_res_aligned_straddlesLowerBound_T_126, _res_aligned_straddlesLowerBound_T_135)
[1506] FIRRTL:361750 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:35 KIND:node :: node _res_aligned_straddlesUpperBound_T_119 = shr(io.addr, 3)
[1507] FIRRTL:361751 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_120 = shl(io.pmp[0].addr, 2)
[1508] FIRRTL:361752 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_121 = not(_res_aligned_straddlesUpperBound_T_120)
[1509] FIRRTL:361753 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_122 = or(_res_aligned_straddlesUpperBound_T_121, UInt<2>(0h3))
[1510] FIRRTL:361754 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_123 = not(_res_aligned_straddlesUpperBound_T_122)
[1511] FIRRTL:361755 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:62 KIND:node :: node _res_aligned_straddlesUpperBound_T_124 = shr(_res_aligned_straddlesUpperBound_T_123, 3)
[1512] FIRRTL:361756 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:49 KIND:node :: node _res_aligned_straddlesUpperBound_T_125 = xor(_res_aligned_straddlesUpperBound_T_119, _res_aligned_straddlesUpperBound_T_124)
[1513] FIRRTL:361757 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:77 KIND:node :: node _res_aligned_straddlesUpperBound_T_126 = eq(_res_aligned_straddlesUpperBound_T_125, UInt<1>(0h0))
[1514] FIRRTL:361758 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:36 KIND:node :: node _res_aligned_straddlesUpperBound_T_127 = shl(io.pmp[0].addr, 2)
[1515] FIRRTL:361759 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:29 KIND:node :: node _res_aligned_straddlesUpperBound_T_128 = not(_res_aligned_straddlesUpperBound_T_127)
[1516] FIRRTL:361760 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:48 KIND:node :: node _res_aligned_straddlesUpperBound_T_129 = or(_res_aligned_straddlesUpperBound_T_128, UInt<2>(0h3))
[1517] FIRRTL:361761 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:60:27 KIND:node :: node _res_aligned_straddlesUpperBound_T_130 = not(_res_aligned_straddlesUpperBound_T_129)
[1518] FIRRTL:361762 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:98 KIND:node :: node _res_aligned_straddlesUpperBound_T_131 = bits(_res_aligned_straddlesUpperBound_T_130, 2, 0)
[1519] FIRRTL:361763 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:119 KIND:node :: node _res_aligned_straddlesUpperBound_T_132 = bits(io.addr, 2, 0)
[1520] FIRRTL:361764 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:136 KIND:node :: node _res_aligned_straddlesUpperBound_T_133 = or(_res_aligned_straddlesUpperBound_T_132, res_aligned_lsbMask_7)
[1521] FIRRTL:361765 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:115 KIND:node :: node _res_aligned_straddlesUpperBound_T_134 = and(_res_aligned_straddlesUpperBound_T_131, _res_aligned_straddlesUpperBound_T_133)
[1522] FIRRTL:361766 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:148 KIND:node :: node _res_aligned_straddlesUpperBound_T_135 = neq(_res_aligned_straddlesUpperBound_T_134, UInt<1>(0h0))
[1523] FIRRTL:361767 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:124:85 KIND:node :: node res_aligned_straddlesUpperBound_7 = and(_res_aligned_straddlesUpperBound_T_126, _res_aligned_straddlesUpperBound_T_135)
[1524] FIRRTL:361768 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:46 KIND:node :: node _res_aligned_rangeAligned_T_7 = or(res_aligned_straddlesLowerBound_7, res_aligned_straddlesUpperBound_7)
[1525] FIRRTL:361769 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:125:24 KIND:node :: node res_aligned_rangeAligned_7 = eq(_res_aligned_rangeAligned_T_7, UInt<1>(0h0))
[1526] FIRRTL:361770 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:39 KIND:node :: node _res_aligned_pow2Aligned_T_21 = bits(io.pmp[0].mask, 2, 0)
[1527] FIRRTL:361771 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:34 KIND:node :: node _res_aligned_pow2Aligned_T_22 = not(_res_aligned_pow2Aligned_T_21)
[1528] FIRRTL:361772 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:32 KIND:node :: node _res_aligned_pow2Aligned_T_23 = and(res_aligned_lsbMask_7, _res_aligned_pow2Aligned_T_22)
[1529] FIRRTL:361773 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:126:57 KIND:node :: node res_aligned_pow2Aligned_7 = eq(_res_aligned_pow2Aligned_T_23, UInt<1>(0h0))
[1530] FIRRTL:361774 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:45:20 KIND:node :: node _res_aligned_T_7 = bits(io.pmp[0].cfg.a, 1, 1)
[1531] FIRRTL:361775 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:127:8 KIND:node :: node res_aligned_7 = mux(_res_aligned_T_7, res_aligned_pow2Aligned_7, res_aligned_rangeAligned_7)
[1532] FIRRTL:361776 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_315 = eq(io.pmp[0].cfg.a, UInt<1>(0h0))
[1533] FIRRTL:361777 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_316 = eq(io.pmp[0].cfg.a, UInt<1>(0h1))
[1534] FIRRTL:361778 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_317 = eq(io.pmp[0].cfg.a, UInt<2>(0h2))
[1535] FIRRTL:361779 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:168:32 KIND:node :: node _res_T_318 = eq(io.pmp[0].cfg.a, UInt<2>(0h3))
[1536] FIRRTL:361780 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:170:30 KIND:node :: node _res_T_319 = eq(io.pmp[0].cfg.l, UInt<1>(0h1))
[1537] FIRRTL:361781 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_42 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1538] FIRRTL:361782 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_320 = cat(res_hi_42, io.pmp[0].cfg.r)
[1539] FIRRTL:361783 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_321 = eq(_res_T_320, UInt<1>(0h0))
[1540] FIRRTL:361784 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_43 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1541] FIRRTL:361785 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_322 = cat(res_hi_43, io.pmp[0].cfg.r)
[1542] FIRRTL:361786 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_323 = eq(_res_T_322, UInt<1>(0h1))
[1543] FIRRTL:361787 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_44 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1544] FIRRTL:361788 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_324 = cat(res_hi_44, io.pmp[0].cfg.r)
[1545] FIRRTL:361789 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_325 = eq(_res_T_324, UInt<2>(0h3))
[1546] FIRRTL:361790 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_45 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1547] FIRRTL:361791 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_326 = cat(res_hi_45, io.pmp[0].cfg.r)
[1548] FIRRTL:361792 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_327 = eq(_res_T_326, UInt<3>(0h4))
[1549] FIRRTL:361793 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_46 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1550] FIRRTL:361794 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_328 = cat(res_hi_46, io.pmp[0].cfg.r)
[1551] FIRRTL:361795 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_329 = eq(_res_T_328, UInt<3>(0h5))
[1552] FIRRTL:361796 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node res_hi_47 = cat(io.pmp[0].cfg.x, io.pmp[0].cfg.w)
[1553] FIRRTL:361797 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:26 KIND:node :: node _res_T_330 = cat(res_hi_47, io.pmp[0].cfg.r)
[1554] FIRRTL:361798 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:174:60 KIND:node :: node _res_T_331 = eq(_res_T_330, UInt<3>(0h7))
[1555] FIRRTL:361799 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_332 = eq(res_ignore_7, UInt<1>(0h0))
[1556] FIRRTL:361800 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_333 = and(_res_T_332, res_hit_7)
[1557] FIRRTL:361801 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_334 = and(_res_T_333, res_aligned_7)
[1558] FIRRTL:361802 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_335 = eq(io.pmp[0].cfg.a, UInt<1>(0h1))
[1559] FIRRTL:361803 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_336 = and(_res_T_334, _res_T_335)
[1560] FIRRTL:361804 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_337 = and(io.pmp[0].cfg.l, res_hit_7)
[1561] FIRRTL:361805 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_338 = and(_res_T_337, res_aligned_7)
[1562] FIRRTL:361806 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_339 = eq(io.pmp[0].cfg.a, UInt<1>(0h1))
[1563] FIRRTL:361807 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_340 = and(_res_T_338, _res_T_339)
[1564] FIRRTL:361808 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_341 = eq(res_ignore_7, UInt<1>(0h0))
[1565] FIRRTL:361809 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_342 = and(_res_T_341, res_hit_7)
[1566] FIRRTL:361810 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_343 = and(_res_T_342, res_aligned_7)
[1567] FIRRTL:361811 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_344 = eq(io.pmp[0].cfg.a, UInt<2>(0h2))
[1568] FIRRTL:361812 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_345 = and(_res_T_343, _res_T_344)
[1569] FIRRTL:361813 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_346 = and(io.pmp[0].cfg.l, res_hit_7)
[1570] FIRRTL:361814 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_347 = and(_res_T_346, res_aligned_7)
[1571] FIRRTL:361815 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_348 = eq(io.pmp[0].cfg.a, UInt<2>(0h2))
[1572] FIRRTL:361816 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_349 = and(_res_T_347, _res_T_348)
[1573] FIRRTL:361817 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:22 KIND:node :: node _res_T_350 = eq(res_ignore_7, UInt<1>(0h0))
[1574] FIRRTL:361818 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:30 KIND:node :: node _res_T_351 = and(_res_T_350, res_hit_7)
[1575] FIRRTL:361819 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:37 KIND:node :: node _res_T_352 = and(_res_T_351, res_aligned_7)
[1576] FIRRTL:361820 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:61 KIND:node :: node _res_T_353 = eq(io.pmp[0].cfg.a, UInt<2>(0h3))
[1577] FIRRTL:361821 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:177:48 KIND:node :: node _res_T_354 = and(_res_T_352, _res_T_353)
[1578] FIRRTL:361822 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:32 KIND:node :: node _res_T_355 = and(io.pmp[0].cfg.l, res_hit_7)
[1579] FIRRTL:361823 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:39 KIND:node :: node _res_T_356 = and(_res_T_355, res_aligned_7)
[1580] FIRRTL:361824 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:63 KIND:node :: node _res_T_357 = eq(io.pmp[0].cfg.a, UInt<2>(0h3))
[1581] FIRRTL:361825 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:178:50 KIND:node :: node _res_T_358 = and(_res_T_356, _res_T_357)
[1582] FIRRTL:361826 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:wire :: wire res_cur_7 : { cfg : { l : UInt<1>, res : UInt<2>, a : UInt<2>, x : UInt<1>, w : UInt<1>, r : UInt<1>}, addr : UInt<30>, mask : UInt<32>}
[1583] FIRRTL:361827 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:181:23 KIND:connect :: connect res_cur_7, io.pmp[0]
[1584] FIRRTL:361828 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:40 KIND:node :: node _res_cur_cfg_r_T_14 = or(io.pmp[0].cfg.r, res_ignore_7)
[1585] FIRRTL:361829 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:26 KIND:node :: node _res_cur_cfg_r_T_15 = and(res_aligned_7, _res_cur_cfg_r_T_14)
[1586] FIRRTL:361830 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:182:15 KIND:connect :: connect res_cur_7.cfg.r, _res_cur_cfg_r_T_15
[1587] FIRRTL:361831 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:40 KIND:node :: node _res_cur_cfg_w_T_14 = or(io.pmp[0].cfg.w, res_ignore_7)
[1588] FIRRTL:361832 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:26 KIND:node :: node _res_cur_cfg_w_T_15 = and(res_aligned_7, _res_cur_cfg_w_T_14)
[1589] FIRRTL:361833 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:183:15 KIND:connect :: connect res_cur_7.cfg.w, _res_cur_cfg_w_T_15
[1590] FIRRTL:361834 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:40 KIND:node :: node _res_cur_cfg_x_T_14 = or(io.pmp[0].cfg.x, res_ignore_7)
[1591] FIRRTL:361835 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:26 KIND:node :: node _res_cur_cfg_x_T_15 = and(res_aligned_7, _res_cur_cfg_x_T_14)
[1592] FIRRTL:361836 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:184:15 KIND:connect :: connect res_cur_7.cfg.x, _res_cur_cfg_x_T_15
[1593] FIRRTL:361837 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:185:8 KIND:node :: node res = mux(res_hit_7, res_cur_7, _res_T_314)
[1594] FIRRTL:361838 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:188:8 KIND:connect :: connect io.r, res.cfg.r
[1595] FIRRTL:361839 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:189:8 KIND:connect :: connect io.w, res.cfg.w
[1596] FIRRTL:361840 SRC:generators/rocket-chip/src/main/scala/rocket/PMP.scala:190:8 KIND:connect :: connect io.x, res.cfg.x
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
  "task_id": "leaf_abstraction-LSU.dtlb.pmp_0-751666a56ace25f8",
  "work_unit_id": "LSU.dtlb.pmp_0",
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
