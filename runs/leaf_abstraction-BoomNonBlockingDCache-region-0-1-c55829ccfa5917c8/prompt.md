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

Task ID: `leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache::region-0-1`
- module: `BoomNonBlockingDCache`
- kind: `region`
- instance path: `BoomNonBlockingDCache`
- leaf: `True`
- coverage complete: `True`
- raw statements: 89
- logical statements: 25
- mapped/logical source lines: 20
- registers: 2
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

- `BoomNonBlockingDCache::auto.out.c.fire`
  - predicate: `auto.out.c.valid && auto.out.c.ready`
  - direction/protocol: `send` / `decoupled`
  - payload leaves: ['auto.out.c.bits.address', 'auto.out.c.bits.corrupt', 'auto.out.c.bits.data', 'auto.out.c.bits.opcode', 'auto.out.c.bits.param', 'auto.out.c.bits.size', 'auto.out.c.bits.source']
  - immediate registers: ['beatsLeft', 'state']
  - historical registers: ['beatsLeft', 'state']

## Concrete local state

['beatsLeft', 'state']

## Environment/frontier signals

['_nodeOut_c_bits_WIRE_1', '_nodeOut_c_bits_WIRE_2', '_nodeOut_c_bits_WIRE_5', '_nodeOut_c_bits_WIRE_6', '_nodeOut_c_bits_WIRE_7', '_nodeOut_c_bits_WIRE_8', '_nodeOut_c_bits_WIRE_9', '_nodeOut_c_valid_WIRE', 'beatsLeft', 'h0', 'hfff', 'idle', 'nodeOut.c.bits.address', 'nodeOut.c.bits.corrupt', 'nodeOut.c.bits.data', 'nodeOut.c.bits.opcode', 'nodeOut.c.bits.param', 'nodeOut.c.bits.size', 'nodeOut.c.bits.source', 'nodeOut.c.ready', 'nodeOut.c.valid', 'prober.io.rep.bits.address', 'prober.io.rep.bits.corrupt', 'prober.io.rep.bits.data', 'prober.io.rep.bits.opcode', 'prober.io.rep.bits.param', 'prober.io.rep.bits.size', 'prober.io.rep.bits.source', 'prober.io.rep.valid', 'state', 'wb.io.release.bits.address', 'wb.io.release.bits.corrupt', 'wb.io.release.bits.data', 'wb.io.release.bits.opcode', 'wb.io.release.bits.param', 'wb.io.release.bits.size', 'wb.io.release.bits.source', 'wb.io.release.valid', 'winner', 'winner[0]', 'winner[1]']

## Source evidence

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:15-17
```scala

  val lowestIndexFirst: Policy = (width, valids, select) => ~(leftOR(valids) << 1)(width-1, 0)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:60-63
```scala
      val beatsLeft = RegInit(0.U)
      val idle = beatsLeft === 0.U
      val latch = idle && sink.ready // winner (if any) claims sink
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:67-69
```scala
      // Arbitrate amongst the requests
      val readys = VecInit(policy(valids.size, Cat(valids.reverse), latch).asBools)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:70-72
```scala
      // Which request wins arbitration?
      val winner = VecInit((readys zip valids) map { case (r,v) => r&&v })
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:81-86
```scala
      // Track remaining beats
      val maskedBeats = (winner zip beatsIn) map { case (w,b) => Mux(w, b, 0.U) }

      val initBeats = maskedBeats.reduce(_ | _) // no winner => 0 beats
      beatsLeft := Mux(latch, initBeats, beatsLeft - sink.fire)
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:88-91
```scala
      val state = RegInit(VecInit(Seq.fill(sources.size)(false.B)))
      val muxState = Mux(idle, winner, state)
      state := muxState
```

### generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:95-98
```scala
      }
      sink.valid := Mux(idle, valids.reduce(_||_), Mux1H(state, valids))
      sink.bits :<= Mux1H(muxState, sourcesIn.map(_.bits))
    }
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

### generators/rocket-chip/src/main/scala/util/package.scala:243-245
```scala
  def OH1ToUInt(x: UInt): UInt = OHToUInt(OH1ToOH(x))
  def UIntToOH1(x: UInt, width: Int): UInt = ~((-1).S(width.W).asUInt << x)(width-1, 0)
  def UIntToOH1(x: UInt): UInt = UIntToOH1(x, (1 << x.getWidth) - 1)
```

### generators/rocket-chip/src/main/scala/util/package.scala:253-256
```scala
    def helper(s: Int, x: UInt): UInt =
      if (s >= stop) x else helper(s+s, x | (x << s)(width-1,0))
    helper(1, x)(width-1, 0)
  }
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[2546] FIRRTL:200315 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _decode_T = dshl(UInt<12>(0hfff), wb.io.release.bits.size)
[2547] FIRRTL:200316 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _decode_T_1 = bits(_decode_T, 11, 0)
[2548] FIRRTL:200317 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _decode_T_2 = not(_decode_T_1)
[2549] FIRRTL:200318 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node decode = shr(_decode_T_2, 3)
[2550] FIRRTL:200319 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:102:36 KIND:node :: node opdata = bits(wb.io.release.bits.opcode, 0, 0)
[2551] FIRRTL:200320 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node _T_83 = mux(opdata, decode, UInt<1>(0h0))
[2552] FIRRTL:200321 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:71 KIND:node :: node _decode_T_3 = dshl(UInt<12>(0hfff), prober.io.rep.bits.size)
[2553] FIRRTL:200322 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:76 KIND:node :: node _decode_T_4 = bits(_decode_T_3, 11, 0)
[2554] FIRRTL:200323 SRC:generators/rocket-chip/src/main/scala/util/package.scala:244:46 KIND:node :: node _decode_T_5 = not(_decode_T_4)
[2555] FIRRTL:200324 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:220:59 KIND:node :: node decode_1 = shr(_decode_T_5, 3)
[2556] FIRRTL:200325 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:102:36 KIND:node :: node opdata_1 = bits(prober.io.rep.bits.opcode, 0, 0)
[2557] FIRRTL:200326 SRC:generators/rocket-chip/src/main/scala/tilelink/Edges.scala:221:14 KIND:node :: node _T_84 = mux(opdata_1, decode_1, UInt<1>(0h0))
[2559] FIRRTL:200328 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:61:28 KIND:node :: node idle = eq(beatsLeft, UInt<1>(0h0))
[2560] FIRRTL:200329 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:62:24 KIND:node :: node latch = and(idle, nodeOut.c.ready)
[2561] FIRRTL:200330 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:51 KIND:node :: node _readys_T = cat(prober.io.rep.valid, wb.io.release.valid)
[2562] FIRRTL:200331 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:48 KIND:node :: node _readys_T_1 = shl(_readys_T, 1)
[2563] FIRRTL:200332 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:53 KIND:node :: node _readys_T_2 = bits(_readys_T_1, 1, 0)
[2564] FIRRTL:200333 SRC:generators/rocket-chip/src/main/scala/util/package.scala:254:43 KIND:node :: node _readys_T_3 = or(_readys_T, _readys_T_2)
[2565] FIRRTL:200334 SRC:generators/rocket-chip/src/main/scala/util/package.scala:255:17 KIND:node :: node _readys_T_4 = bits(_readys_T_3, 1, 0)
[2566] FIRRTL:200335 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:78 KIND:node :: node _readys_T_5 = shl(_readys_T_4, 1)
[2567] FIRRTL:200336 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:83 KIND:node :: node _readys_T_6 = bits(_readys_T_5, 1, 0)
[2568] FIRRTL:200337 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:16:61 KIND:node :: node _readys_T_7 = not(_readys_T_6)
[2569] FIRRTL:200338 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_8 = bits(_readys_T_7, 0, 0)
[2570] FIRRTL:200339 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:76 KIND:node :: node _readys_T_9 = bits(_readys_T_7, 1, 1)
[2572] FIRRTL:200341 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys[0], _readys_T_8
[2573] FIRRTL:200342 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:68:27 KIND:connect :: connect readys[1], _readys_T_9
[2574] FIRRTL:200343 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T = and(readys[0], wb.io.release.valid)
[2575] FIRRTL:200344 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:69 KIND:node :: node _winner_T_1 = and(readys[1], prober.io.rep.valid)
[2577] FIRRTL:200346 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner[0], _winner_T
[2578] FIRRTL:200347 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:71:27 KIND:connect :: connect winner[1], _winner_T_1
[2606] FIRRTL:200375 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_0 = mux(winner[0], _T_83, UInt<1>(0h0))
[2607] FIRRTL:200376 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:82:69 KIND:node :: node maskedBeats_1 = mux(winner[1], _T_84, UInt<1>(0h0))
[2608] FIRRTL:200377 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:84:44 KIND:node :: node initBeats = or(maskedBeats_0, maskedBeats_1)
[2609] FIRRTL:200378 SRC:src/main/scala/chisel3/util/Decoupled.scala:51:35 KIND:node :: node _beatsLeft_T = and(nodeOut.c.ready, nodeOut.c.valid)
[2610] FIRRTL:200379 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_1 = sub(beatsLeft, _beatsLeft_T)
[2611] FIRRTL:200380 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:52 KIND:node :: node _beatsLeft_T_2 = tail(_beatsLeft_T_1, 1)
[2612] FIRRTL:200381 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:23 KIND:node :: node _beatsLeft_T_3 = mux(latch, initBeats, _beatsLeft_T_2)
[2613] FIRRTL:200382 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:85:17 KIND:connect :: connect beatsLeft, _beatsLeft_T_3
[2618] FIRRTL:200387 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:89:25 KIND:node :: node muxState = mux(idle, winner, state)
[2619] FIRRTL:200388 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:90:13 KIND:connect :: connect state, muxState
[2625] FIRRTL:200394 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:46 KIND:node :: node _nodeOut_c_valid_T = or(wb.io.release.valid, prober.io.rep.valid)
[2626] FIRRTL:200395 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_valid_T_1 = mux(state[0], wb.io.release.valid, UInt<1>(0h0))
[2627] FIRRTL:200396 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_valid_T_2 = mux(state[1], prober.io.rep.valid, UInt<1>(0h0))
[2628] FIRRTL:200397 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_valid_T_3 = or(_nodeOut_c_valid_T_1, _nodeOut_c_valid_T_2)
[2630] FIRRTL:200399 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_valid_WIRE, _nodeOut_c_valid_T_3
[2631] FIRRTL:200400 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:24 KIND:node :: node _nodeOut_c_valid_T_4 = mux(idle, _nodeOut_c_valid_T, _nodeOut_c_valid_WIRE)
[2632] FIRRTL:200401 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:96:18 KIND:connect :: connect nodeOut.c.valid, _nodeOut_c_valid_T_4
[2634] FIRRTL:200403 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T = mux(muxState[0], wb.io.release.bits.corrupt, UInt<1>(0h0))
[2635] FIRRTL:200404 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_1 = mux(muxState[1], prober.io.rep.bits.corrupt, UInt<1>(0h0))
[2636] FIRRTL:200405 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_2 = or(_nodeOut_c_bits_T, _nodeOut_c_bits_T_1)
[2638] FIRRTL:200407 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_1, _nodeOut_c_bits_T_2
[2639] FIRRTL:200408 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.corrupt, _nodeOut_c_bits_WIRE_1
[2640] FIRRTL:200409 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_3 = mux(muxState[0], wb.io.release.bits.data, UInt<1>(0h0))
[2641] FIRRTL:200410 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_4 = mux(muxState[1], prober.io.rep.bits.data, UInt<1>(0h0))
[2642] FIRRTL:200411 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_5 = or(_nodeOut_c_bits_T_3, _nodeOut_c_bits_T_4)
[2644] FIRRTL:200413 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_2, _nodeOut_c_bits_T_5
[2645] FIRRTL:200414 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.data, _nodeOut_c_bits_WIRE_2
[2650] FIRRTL:200419 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_6 = mux(muxState[0], wb.io.release.bits.address, UInt<1>(0h0))
[2651] FIRRTL:200420 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_7 = mux(muxState[1], prober.io.rep.bits.address, UInt<1>(0h0))
[2652] FIRRTL:200421 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_8 = or(_nodeOut_c_bits_T_6, _nodeOut_c_bits_T_7)
[2654] FIRRTL:200423 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_5, _nodeOut_c_bits_T_8
[2655] FIRRTL:200424 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.address, _nodeOut_c_bits_WIRE_5
[2656] FIRRTL:200425 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_9 = mux(muxState[0], wb.io.release.bits.source, UInt<1>(0h0))
[2657] FIRRTL:200426 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_10 = mux(muxState[1], prober.io.rep.bits.source, UInt<1>(0h0))
[2658] FIRRTL:200427 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_11 = or(_nodeOut_c_bits_T_9, _nodeOut_c_bits_T_10)
[2660] FIRRTL:200429 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_6, _nodeOut_c_bits_T_11
[2661] FIRRTL:200430 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.source, _nodeOut_c_bits_WIRE_6
[2662] FIRRTL:200431 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_12 = mux(muxState[0], wb.io.release.bits.size, UInt<1>(0h0))
[2663] FIRRTL:200432 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_13 = mux(muxState[1], prober.io.rep.bits.size, UInt<1>(0h0))
[2664] FIRRTL:200433 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_14 = or(_nodeOut_c_bits_T_12, _nodeOut_c_bits_T_13)
[2666] FIRRTL:200435 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_7, _nodeOut_c_bits_T_14
[2667] FIRRTL:200436 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.size, _nodeOut_c_bits_WIRE_7
[2668] FIRRTL:200437 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_15 = mux(muxState[0], wb.io.release.bits.param, UInt<1>(0h0))
[2669] FIRRTL:200438 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_16 = mux(muxState[1], prober.io.rep.bits.param, UInt<1>(0h0))
[2670] FIRRTL:200439 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_17 = or(_nodeOut_c_bits_T_15, _nodeOut_c_bits_T_16)
[2672] FIRRTL:200441 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_8, _nodeOut_c_bits_T_17
[2673] FIRRTL:200442 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.param, _nodeOut_c_bits_WIRE_8
[2674] FIRRTL:200443 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_18 = mux(muxState[0], wb.io.release.bits.opcode, UInt<1>(0h0))
[2675] FIRRTL:200444 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_19 = mux(muxState[1], prober.io.rep.bits.opcode, UInt<1>(0h0))
[2676] FIRRTL:200445 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:node :: node _nodeOut_c_bits_T_20 = or(_nodeOut_c_bits_T_18, _nodeOut_c_bits_T_19)
[2678] FIRRTL:200447 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE_9, _nodeOut_c_bits_T_20
[2679] FIRRTL:200448 SRC:src/main/scala/chisel3/util/Mux.scala:30:73 KIND:connect :: connect _nodeOut_c_bits_WIRE.opcode, _nodeOut_c_bits_WIRE_9
[2680] FIRRTL:200449 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.corrupt, _nodeOut_c_bits_WIRE.corrupt
[2681] FIRRTL:200450 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.data, _nodeOut_c_bits_WIRE.data
[2682] FIRRTL:200451 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.address, _nodeOut_c_bits_WIRE.address
[2683] FIRRTL:200452 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.source, _nodeOut_c_bits_WIRE.source
[2684] FIRRTL:200453 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.size, _nodeOut_c_bits_WIRE.size
[2685] FIRRTL:200454 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.param, _nodeOut_c_bits_WIRE.param
[2686] FIRRTL:200455 SRC:generators/rocket-chip/src/main/scala/tilelink/Arbiter.scala:97:17 KIND:connect :: connect nodeOut.c.bits.opcode, _nodeOut_c_bits_WIRE.opcode
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache-region-0-1-c55829ccfa5917c8",
  "work_unit_id": "BoomNonBlockingDCache::region-0-1",
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
