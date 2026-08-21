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

Task ID: `leaf_abstraction-BoomNonBlockingDCache.amoalu-9d11028de14b5b4d`
Workflow version: `manual-first-workflow-0.9`
Prompt version: `leaf-abstraction-prompt-0.11`
Output schema version: `umcm-formal-0.5`

## WorkUnit

- id: `BoomNonBlockingDCache.amoalu`
- module: `AMOALU`
- kind: `module`
- instance path: `BoomNonBlockingDCache.amoalu`
- leaf: `True`
- coverage complete: `True`
- raw statements: 103
- logical statements: 25
- mapped/logical source lines: 24
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



## Concrete local state

[]

## Environment/frontier signals

['io.cmd', 'io.lhs', 'io.mask', 'io.out', 'io.out_unmasked', 'io.rhs']

## Source evidence

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:53-55
```scala

class AMOALU(operandBits: Int)(implicit p: Parameters) extends Module {
  val minXLen = 32
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:57-59
```scala

  val io = IO(new Bundle {
    val mask = Input(UInt((operandBits / 8).W))
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:66-72
```scala

  val max = io.cmd === M_XA_MAX || io.cmd === M_XA_MAXU
  val min = io.cmd === M_XA_MIN || io.cmd === M_XA_MINU
  val add = io.cmd === M_XA_ADD
  val logic_and = io.cmd === M_XA_OR || io.cmd === M_XA_AND
  val logic_xor = io.cmd === M_XA_XOR || io.cmd === M_XA_OR
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:74-77
```scala
    // partition the carry chain to support sub-xLen addition
    val mask = ~(0.U(operandBits.W) +: widths.init.map(w => !io.mask(w/8-1) << (w-1))).reduce(_|_)
    (io.lhs & mask) + (io.rhs & mask)
  }
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:81-84
```scala
    def isLessUnsigned(x: UInt, y: UInt, n: Int): Bool = {
      if (n == minXLen) x(n-1, 0) < y(n-1, 0)
      else x(n-1, n/2) < y(n-1, n/2) || x(n-1, n/2) === y(n-1, n/2) && isLessUnsigned(x, y, n/2)
    }
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:87-92
```scala
      val signed = {
        val mask = M_XA_MIN ^ M_XA_MINU
        (io.cmd & mask) === (M_XA_MIN & mask)
      }
      Mux(x(n-1) === y(n-1), isLessUnsigned(x, y, n), Mux(signed, x(n-1), y(n-1)))
    }
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:93-95
```scala

    PriorityMux(widths.reverse.map(w => (io.mask(w/8/2), isLess(io.lhs, io.rhs, w))))
  }
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:96-104
```scala

  val minmax = Mux(Mux(less, min, max), io.lhs, io.rhs)
  val logic =
    Mux(logic_and, io.lhs & io.rhs, 0.U) |
    Mux(logic_xor, io.lhs ^ io.rhs, 0.U)
  val out =
    Mux(add,                    adder_out,
    Mux(logic_and || logic_xor, logic,
                                minmax))
```

### generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:105-109
```scala

  val wmask = FillInterleaved(8, io.mask)
  io.out := wmask & out | ~wmask & io.lhs
  io.out_unmasked := out
}
```

Unresolved source-locator spans remain available in static_handoff.json; do not invent their source text.

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
[0] FIRRTL:197662 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:54:7 KIND:structural :: input clock : Clock
[1] FIRRTL:197663 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:54:7 KIND:structural :: input reset : Reset
[2] FIRRTL:197664 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:58:14 KIND:structural :: output io : { flip mask : UInt<8>, flip cmd : UInt<5>, flip lhs : UInt<64>, flip rhs : UInt<64>, out : UInt<64>, out_unmasked : UInt<64>}
[3] FIRRTL:197666 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:67:20 KIND:node :: node _max_T = eq(io.cmd, UInt<4>(0hd))
[4] FIRRTL:197667 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:67:43 KIND:node :: node _max_T_1 = eq(io.cmd, UInt<4>(0hf))
[5] FIRRTL:197668 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:67:33 KIND:node :: node max = or(_max_T, _max_T_1)
[6] FIRRTL:197669 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:68:20 KIND:node :: node _min_T = eq(io.cmd, UInt<4>(0hc))
[7] FIRRTL:197670 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:68:43 KIND:node :: node _min_T_1 = eq(io.cmd, UInt<4>(0he))
[8] FIRRTL:197671 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:68:33 KIND:node :: node min = or(_min_T, _min_T_1)
[9] FIRRTL:197672 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:69:20 KIND:node :: node add = eq(io.cmd, UInt<4>(0h8))
[10] FIRRTL:197673 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:70:26 KIND:node :: node _logic_and_T = eq(io.cmd, UInt<4>(0ha))
[11] FIRRTL:197674 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:70:48 KIND:node :: node _logic_and_T_1 = eq(io.cmd, UInt<4>(0hb))
[12] FIRRTL:197675 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:70:38 KIND:node :: node logic_and = or(_logic_and_T, _logic_and_T_1)
[13] FIRRTL:197676 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:71:26 KIND:node :: node _logic_xor_T = eq(io.cmd, UInt<4>(0h9))
[14] FIRRTL:197677 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:71:49 KIND:node :: node _logic_xor_T_1 = eq(io.cmd, UInt<4>(0ha))
[15] FIRRTL:197678 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:71:39 KIND:node :: node logic_xor = or(_logic_xor_T, _logic_xor_T_1)
[16] FIRRTL:197679 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:75:69 KIND:node :: node _adder_out_mask_T = bits(io.mask, 3, 3)
[17] FIRRTL:197680 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:75:61 KIND:node :: node _adder_out_mask_T_1 = eq(_adder_out_mask_T, UInt<1>(0h0))
[18] FIRRTL:197681 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:75:77 KIND:node :: node _adder_out_mask_T_2 = shl(_adder_out_mask_T_1, 31)
[19] FIRRTL:197682 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:75:96 KIND:node :: node _adder_out_mask_T_3 = or(UInt<64>(0h0), _adder_out_mask_T_2)
[20] FIRRTL:197683 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:75:16 KIND:node :: node adder_out_mask = not(_adder_out_mask_T_3)
[21] FIRRTL:197684 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:76:13 KIND:node :: node _adder_out_T = and(io.lhs, adder_out_mask)
[22] FIRRTL:197685 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:76:31 KIND:node :: node _adder_out_T_1 = and(io.rhs, adder_out_mask)
[23] FIRRTL:197686 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:76:21 KIND:node :: node _adder_out_T_2 = add(_adder_out_T, _adder_out_T_1)
[24] FIRRTL:197687 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:76:21 KIND:node :: node adder_out = tail(_adder_out_T_2, 1)
[25] FIRRTL:197688 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:94:49 KIND:node :: node _less_T = bits(io.mask, 4, 4)
[26] FIRRTL:197689 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:88:29 KIND:node :: node less_signed_mask = xor(UInt<4>(0hc), UInt<4>(0he))
[27] FIRRTL:197690 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:17 KIND:node :: node _less_signed_T = and(io.cmd, less_signed_mask)
[28] FIRRTL:197691 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:39 KIND:node :: node _less_signed_T_1 = and(UInt<4>(0hc), less_signed_mask)
[29] FIRRTL:197692 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:25 KIND:node :: node less_signed = eq(_less_signed_T, _less_signed_T_1)
[30] FIRRTL:197693 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:12 KIND:node :: node _less_T_1 = bits(io.lhs, 63, 63)
[31] FIRRTL:197694 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:23 KIND:node :: node _less_T_2 = bits(io.rhs, 63, 63)
[32] FIRRTL:197695 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:18 KIND:node :: node _less_T_3 = eq(_less_T_1, _less_T_2)
[33] FIRRTL:197696 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:13 KIND:node :: node _less_T_4 = bits(io.lhs, 63, 32)
[34] FIRRTL:197697 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:27 KIND:node :: node _less_T_5 = bits(io.rhs, 63, 32)
[35] FIRRTL:197698 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:24 KIND:node :: node _less_T_6 = lt(_less_T_4, _less_T_5)
[36] FIRRTL:197699 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:42 KIND:node :: node _less_T_7 = bits(io.lhs, 63, 32)
[37] FIRRTL:197700 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:58 KIND:node :: node _less_T_8 = bits(io.rhs, 63, 32)
[38] FIRRTL:197701 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:53 KIND:node :: node _less_T_9 = eq(_less_T_7, _less_T_8)
[39] FIRRTL:197702 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:26 KIND:node :: node _less_T_10 = bits(io.lhs, 31, 0)
[40] FIRRTL:197703 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:38 KIND:node :: node _less_T_11 = bits(io.rhs, 31, 0)
[41] FIRRTL:197704 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:35 KIND:node :: node _less_T_12 = lt(_less_T_10, _less_T_11)
[42] FIRRTL:197705 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:69 KIND:node :: node _less_T_13 = and(_less_T_9, _less_T_12)
[43] FIRRTL:197706 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:83:38 KIND:node :: node _less_T_14 = or(_less_T_6, _less_T_13)
[44] FIRRTL:197707 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:68 KIND:node :: node _less_T_15 = bits(io.lhs, 63, 63)
[45] FIRRTL:197708 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:76 KIND:node :: node _less_T_16 = bits(io.rhs, 63, 63)
[46] FIRRTL:197709 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:58 KIND:node :: node _less_T_17 = mux(less_signed, _less_T_15, _less_T_16)
[47] FIRRTL:197710 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:10 KIND:node :: node _less_T_18 = mux(_less_T_3, _less_T_14, _less_T_17)
[48] FIRRTL:197711 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:94:49 KIND:node :: node _less_T_19 = bits(io.mask, 2, 2)
[49] FIRRTL:197712 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:88:29 KIND:node :: node less_signed_mask_1 = xor(UInt<4>(0hc), UInt<4>(0he))
[50] FIRRTL:197713 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:17 KIND:node :: node _less_signed_T_2 = and(io.cmd, less_signed_mask_1)
[51] FIRRTL:197714 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:39 KIND:node :: node _less_signed_T_3 = and(UInt<4>(0hc), less_signed_mask_1)
[52] FIRRTL:197715 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:89:25 KIND:node :: node less_signed_1 = eq(_less_signed_T_2, _less_signed_T_3)
[53] FIRRTL:197716 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:12 KIND:node :: node _less_T_20 = bits(io.lhs, 31, 31)
[54] FIRRTL:197717 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:23 KIND:node :: node _less_T_21 = bits(io.rhs, 31, 31)
[55] FIRRTL:197718 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:18 KIND:node :: node _less_T_22 = eq(_less_T_20, _less_T_21)
[56] FIRRTL:197719 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:26 KIND:node :: node _less_T_23 = bits(io.lhs, 31, 0)
[57] FIRRTL:197720 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:38 KIND:node :: node _less_T_24 = bits(io.rhs, 31, 0)
[58] FIRRTL:197721 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:82:35 KIND:node :: node _less_T_25 = lt(_less_T_23, _less_T_24)
[59] FIRRTL:197722 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:68 KIND:node :: node _less_T_26 = bits(io.lhs, 31, 31)
[60] FIRRTL:197723 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:76 KIND:node :: node _less_T_27 = bits(io.rhs, 31, 31)
[61] FIRRTL:197724 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:58 KIND:node :: node _less_T_28 = mux(less_signed_1, _less_T_26, _less_T_27)
[62] FIRRTL:197725 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:91:10 KIND:node :: node _less_T_29 = mux(_less_T_22, _less_T_25, _less_T_28)
[63] FIRRTL:197726 SRC:src/main/scala/chisel3/util/Mux.scala:50:70 KIND:node :: node less = mux(_less_T, _less_T_18, _less_T_29)
[64] FIRRTL:197727 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:97:23 KIND:node :: node _minmax_T = mux(less, min, max)
[65] FIRRTL:197728 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:97:19 KIND:node :: node minmax = mux(_minmax_T, io.lhs, io.rhs)
[66] FIRRTL:197729 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:99:27 KIND:node :: node _logic_T = and(io.lhs, io.rhs)
[67] FIRRTL:197730 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:99:8 KIND:node :: node _logic_T_1 = mux(logic_and, _logic_T, UInt<1>(0h0))
[68] FIRRTL:197731 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:100:27 KIND:node :: node _logic_T_2 = xor(io.lhs, io.rhs)
[69] FIRRTL:197732 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:100:8 KIND:node :: node _logic_T_3 = mux(logic_xor, _logic_T_2, UInt<1>(0h0))
[70] FIRRTL:197733 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:99:42 KIND:node :: node logic = or(_logic_T_1, _logic_T_3)
[71] FIRRTL:197734 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:103:19 KIND:node :: node _out_T = or(logic_and, logic_xor)
[72] FIRRTL:197735 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:103:8 KIND:node :: node _out_T_1 = mux(_out_T, logic, minmax)
[73] FIRRTL:197736 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:102:8 KIND:node :: node out = mux(add, adder_out, _out_T_1)
[74] FIRRTL:197737 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T = bits(io.mask, 0, 0)
[75] FIRRTL:197738 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_1 = bits(io.mask, 1, 1)
[76] FIRRTL:197739 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_2 = bits(io.mask, 2, 2)
[77] FIRRTL:197740 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_3 = bits(io.mask, 3, 3)
[78] FIRRTL:197741 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_4 = bits(io.mask, 4, 4)
[79] FIRRTL:197742 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_5 = bits(io.mask, 5, 5)
[80] FIRRTL:197743 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_6 = bits(io.mask, 6, 6)
[81] FIRRTL:197744 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_7 = bits(io.mask, 7, 7)
[82] FIRRTL:197745 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_8 = mux(_wmask_T, UInt<8>(0hff), UInt<8>(0h0))
[83] FIRRTL:197746 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_9 = mux(_wmask_T_1, UInt<8>(0hff), UInt<8>(0h0))
[84] FIRRTL:197747 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_10 = mux(_wmask_T_2, UInt<8>(0hff), UInt<8>(0h0))
[85] FIRRTL:197748 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_11 = mux(_wmask_T_3, UInt<8>(0hff), UInt<8>(0h0))
[86] FIRRTL:197749 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_12 = mux(_wmask_T_4, UInt<8>(0hff), UInt<8>(0h0))
[87] FIRRTL:197750 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_13 = mux(_wmask_T_5, UInt<8>(0hff), UInt<8>(0h0))
[88] FIRRTL:197751 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_14 = mux(_wmask_T_6, UInt<8>(0hff), UInt<8>(0h0))
[89] FIRRTL:197752 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node _wmask_T_15 = mux(_wmask_T_7, UInt<8>(0hff), UInt<8>(0h0))
[90] FIRRTL:197753 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_lo_lo = cat(_wmask_T_9, _wmask_T_8)
[91] FIRRTL:197754 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_lo_hi = cat(_wmask_T_11, _wmask_T_10)
[92] FIRRTL:197755 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_lo = cat(wmask_lo_hi, wmask_lo_lo)
[93] FIRRTL:197756 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_hi_lo = cat(_wmask_T_13, _wmask_T_12)
[94] FIRRTL:197757 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_hi_hi = cat(_wmask_T_15, _wmask_T_14)
[95] FIRRTL:197758 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask_hi = cat(wmask_hi_hi, wmask_hi_lo)
[96] FIRRTL:197759 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:106:30 KIND:node :: node wmask = cat(wmask_hi, wmask_lo)
[97] FIRRTL:197760 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:107:19 KIND:node :: node _io_out_T = and(wmask, out)
[98] FIRRTL:197761 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:107:27 KIND:node :: node _io_out_T_1 = not(wmask)
[99] FIRRTL:197762 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:107:34 KIND:node :: node _io_out_T_2 = and(_io_out_T_1, io.lhs)
[100] FIRRTL:197763 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:107:25 KIND:node :: node _io_out_T_3 = or(_io_out_T, _io_out_T_2)
[101] FIRRTL:197764 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:107:10 KIND:connect :: connect io.out, _io_out_T_3
[102] FIRRTL:197765 SRC:generators/rocket-chip/src/main/scala/rocket/AMOALU.scala:108:19 KIND:connect :: connect io.out_unmasked, out
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
  "task_id": "leaf_abstraction-BoomNonBlockingDCache.amoalu-9d11028de14b5b4d",
  "work_unit_id": "BoomNonBlockingDCache.amoalu",
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
