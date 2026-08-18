FIRRTL version 7.0.0
circuit BoomMSHR :
  extmodule BranchKillableQueue : @[src/main/scala/v4/lsu/mshrs.scala 143:13]
    input clock : Clock
    input reset : UInt<1>
    output io : { enq : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<64> }, deq : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<64> }, empty : UInt<1> }

  public module BoomMSHR : @[src/main/scala/v4/lsu/mshrs.scala 35:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip req_pri_val : UInt<1>, req_pri_rdy : UInt<1>, flip req_sec_val : UInt<1>, req_sec_rdy : UInt<1>, flip req_is_probe : UInt<1>, mem_acquire : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<64> }, flip mem_grant : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<64> }, mem_finish : { flip ready : UInt<1>, valid : UInt<1>, bits : UInt<8> }, probe_rdy : UInt<1> } @[src/main/scala/v4/lsu/mshrs.scala 39:12]
    inst rpq of BranchKillableQueue @[src/main/scala/v4/lsu/mshrs.scala 143:13]
    rpq.clock <= clock
    rpq.reset <= reset

    reg state : UInt<5>, clock with : (reset => (reset, UInt<5>("h0"))) @[src/main/scala/v4/lsu/mshrs.scala 116:15]
    reg grantack_valid : UInt<1>, clock @[src/main/scala/v4/lsu/mshrs.scala 151:18]

    rpq.io.enq.valid <= or(and(io.req_pri_val, io.req_pri_rdy), and(io.req_sec_val, io.req_sec_rdy)) @[src/main/scala/v4/lsu/mshrs.scala 147:20]
    rpq.io.enq.bits <= UInt<64>("h0")
    rpq.io.deq.ready <= eq(state, UInt<5>("hc")) @[src/main/scala/v4/lsu/mshrs.scala 151:20]

    io.req_pri_rdy <= eq(state, UInt<5>("h0")) @[src/main/scala/v4/lsu/mshrs.scala 229:20]
    io.req_sec_rdy <= rpq.io.enq.ready @[src/main/scala/v4/lsu/mshrs.scala 160:18]
    io.mem_acquire.valid <= eq(state, UInt<5>("h1")) @[src/main/scala/v4/lsu/mshrs.scala 234:26]
    io.mem_grant.ready <= eq(state, UInt<5>("h2")) @[src/main/scala/v4/lsu/mshrs.scala 239:24]
    io.mem_finish.valid <= and(eq(state, UInt<5>("he")), grantack_valid) @[src/main/scala/v4/lsu/mshrs.scala 345:25]
    io.mem_finish.bits <= UInt<8>("h1") @[src/main/scala/v4/lsu/mshrs.scala 346:24]
    io.probe_rdy <= and(eq(state, UInt<5>("h0")), not(grantack_valid)) @[src/main/scala/v4/lsu/mshrs.scala 158:18]

    when eq(state, UInt<5>("h0")) : @[src/main/scala/v4/lsu/mshrs.scala 228:3]
      when and(io.req_pri_val, io.req_pri_rdy) : @[src/main/scala/v4/lsu/mshrs.scala 232:5]
        state <= UInt<5>("h1")
    when eq(state, UInt<5>("h1")) : @[src/main/scala/v4/lsu/mshrs.scala 234:3]
      when and(io.mem_acquire.valid, io.mem_acquire.ready) :
        state <= UInt<5>("h2")
    when eq(state, UInt<5>("h2")) : @[src/main/scala/v4/lsu/mshrs.scala 239:3]
      when and(io.mem_grant.valid, io.mem_grant.ready) : @[src/main/scala/v4/lsu/mshrs.scala 248:5]
        grantack_valid <= UInt<1>("h1") @[src/main/scala/v4/lsu/mshrs.scala 252:7]
        state <= UInt<5>("hc") @[src/main/scala/v4/lsu/mshrs.scala 253:7]
    when eq(state, UInt<5>("hc")) : @[src/main/scala/v4/lsu/mshrs.scala 329:3]
      when and(rpq.io.empty, not(rpq.io.enq.valid)) : @[src/main/scala/v4/lsu/mshrs.scala 337:5]
        state <= UInt<5>("hd")
    when eq(state, UInt<5>("hd")) : @[src/main/scala/v4/lsu/mshrs.scala 340:3]
      state <= UInt<5>("he")
    when eq(state, UInt<5>("he")) : @[src/main/scala/v4/lsu/mshrs.scala 344:3]
      when or(and(io.mem_finish.valid, io.mem_finish.ready), not(grantack_valid)) : @[src/main/scala/v4/lsu/mshrs.scala 347:5]
        grantack_valid <= UInt<1>("h0") @[src/main/scala/v4/lsu/mshrs.scala 348:7]
        state <= UInt<5>("hf")
    when eq(state, UInt<5>("hf")) :
      state <= UInt<5>("h0")
