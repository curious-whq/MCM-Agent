FIRRTL version 7.0.0
circuit DCacheTop :
  public module DCacheTop : @[src/main/scala/v4/lsu/dcache.scala 448:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip tl_b : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, tl_c : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } } } @[src/main/scala/v4/lsu/dcache.scala 453:12]
    inst prober of BoomProbeUnit @[src/main/scala/v4/lsu/dcache.scala 465:16]
    prober.clock <= clock
    prober.reset <= reset
    prober.io.req.valid <= io.tl_b.valid @[src/main/scala/v4/lsu/dcache.scala 785:3]
    io.tl_b.ready <= prober.io.req.ready @[src/main/scala/v4/lsu/dcache.scala 786:3]
    prober.io.req.bits <= io.tl_b.bits @[src/main/scala/v4/lsu/dcache.scala 787:3]
    io.tl_c.valid <= prober.io.rep.valid @[src/main/scala/v4/lsu/dcache.scala 817:3]
    prober.io.rep.ready <= io.tl_c.ready @[src/main/scala/v4/lsu/dcache.scala 817:3]
    io.tl_c.bits <= prober.io.rep.bits @[src/main/scala/v4/lsu/dcache.scala 817:3]
    prober.io.mshr_rdy <= UInt<1>("h1")
    prober.io.wb_rdy <= UInt<1>("h1")
    prober.io.way_en <= UInt<4>("h0")
    prober.io.block_state <= UInt<1>("h0")
    prober.io.meta_read.ready <= UInt<1>("h1")
    prober.io.meta_write.ready <= UInt<1>("h1")
    prober.io.wb_req.ready <= UInt<1>("h1")
    prober.io.lsu_release.ready <= UInt<1>("h1")

  public module BoomProbeUnit : @[src/main/scala/v4/lsu/dcache.scala 145:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, rep : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<8>, tag : UInt<20> } }, meta_write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<8>, tag : UInt<20> } }, wb_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { source : UInt<4>, idx : UInt<8>, tag : UInt<20> } }, flip way_en : UInt<4>, flip wb_rdy : UInt<1>, flip mshr_rdy : UInt<1>, flip block_state : UInt<1>, lsu_release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } } } @[src/main/scala/v4/lsu/dcache.scala 146:12]

    reg state : UInt<4>, clock with : (reset => (reset, UInt<4>("h0"))) @[src/main/scala/v4/lsu/dcache.scala 162:15]
    reg req : { address : UInt<40>, source : UInt<4> }, clock @[src/main/scala/v4/lsu/dcache.scala 164:13]
    reg way_en : UInt<4>, clock @[src/main/scala/v4/lsu/dcache.scala 168:16]
    node tag_matches = orr(way_en) @[src/main/scala/v4/lsu/dcache.scala 169:21]
    node is_dirty = and(tag_matches, io.block_state) @[src/main/scala/v4/lsu/dcache.scala 173:28]

    io.req.ready <= eq(state, UInt<4>("h0")) @[src/main/scala/v4/lsu/dcache.scala 181:16]
    io.rep.valid <= eq(state, UInt<4>("h6")) @[src/main/scala/v4/lsu/dcache.scala 182:16]
    io.rep.bits.opcode <= UInt<3>("h4") @[src/main/scala/v4/lsu/dcache.scala 183:15]
    io.rep.bits.address <= req.address @[src/main/scala/v4/lsu/dcache.scala 183:15]
    io.rep.bits.source <= req.source @[src/main/scala/v4/lsu/dcache.scala 183:15]

    io.meta_read.valid <= eq(state, UInt<4>("h1")) @[src/main/scala/v4/lsu/dcache.scala 188:22]
    io.meta_write.valid <= eq(state, UInt<4>("h9")) @[src/main/scala/v4/lsu/dcache.scala 193:23]
    io.wb_req.valid <= eq(state, UInt<4>("h7")) @[src/main/scala/v4/lsu/dcache.scala 201:18]
    io.lsu_release.valid <= eq(state, UInt<4>("h5")) @[src/main/scala/v4/lsu/dcache.scala 214:23]
    io.lsu_release.bits.opcode <= UInt<3>("h4") @[src/main/scala/v4/lsu/dcache.scala 215:22]
    io.lsu_release.bits.address <= req.address @[src/main/scala/v4/lsu/dcache.scala 215:22]
    io.lsu_release.bits.source <= req.source @[src/main/scala/v4/lsu/dcache.scala 215:22]

    when eq(state, UInt<4>("h0")) : @[src/main/scala/v4/lsu/dcache.scala 218:3]
      when and(io.req.valid, io.req.ready) : @[src/main/scala/v4/lsu/dcache.scala 219:5]
        state <= UInt<4>("h1") @[src/main/scala/v4/lsu/dcache.scala 220:13]
        req.address <= io.req.bits.address @[src/main/scala/v4/lsu/dcache.scala 221:11]
        req.source <= io.req.bits.source @[src/main/scala/v4/lsu/dcache.scala 221:11]
    when eq(state, UInt<4>("h1")) : @[src/main/scala/v4/lsu/dcache.scala 223:3]
      when and(io.meta_read.valid, io.meta_read.ready) : @[src/main/scala/v4/lsu/dcache.scala 224:5]
        state <= UInt<4>("h2") @[src/main/scala/v4/lsu/dcache.scala 225:13]
    when eq(state, UInt<4>("h2")) : @[src/main/scala/v4/lsu/dcache.scala 227:3]
      state <= UInt<4>("h3") @[src/main/scala/v4/lsu/dcache.scala 228:11]
    when eq(state, UInt<4>("h3")) : @[src/main/scala/v4/lsu/dcache.scala 230:3]
      way_en <= io.way_en @[src/main/scala/v4/lsu/dcache.scala 231:14]
      state <= mux(and(io.mshr_rdy, io.wb_rdy), UInt<4>("h4"), UInt<4>("h1")) @[src/main/scala/v4/lsu/dcache.scala 232:11]
    when eq(state, UInt<4>("h4")) : @[src/main/scala/v4/lsu/dcache.scala 234:3]
      state <= mux(and(tag_matches, is_dirty), UInt<4>("h7"), UInt<4>("h5")) @[src/main/scala/v4/lsu/dcache.scala 235:11]
    when eq(state, UInt<4>("h5")) : @[src/main/scala/v4/lsu/dcache.scala 237:3]
      when and(io.lsu_release.valid, io.lsu_release.ready) : @[src/main/scala/v4/lsu/dcache.scala 238:5]
        state <= UInt<4>("h6") @[src/main/scala/v4/lsu/dcache.scala 239:13]
    when eq(state, UInt<4>("h6")) : @[src/main/scala/v4/lsu/dcache.scala 241:3]
      when io.rep.ready : @[src/main/scala/v4/lsu/dcache.scala 242:5]
        state <= mux(tag_matches, UInt<4>("h9"), UInt<4>("h0")) @[src/main/scala/v4/lsu/dcache.scala 243:13]
    when eq(state, UInt<4>("h7")) : @[src/main/scala/v4/lsu/dcache.scala 245:3]
      when and(io.wb_req.valid, io.wb_req.ready) : @[src/main/scala/v4/lsu/dcache.scala 246:5]
        state <= UInt<4>("h8") @[src/main/scala/v4/lsu/dcache.scala 247:13]
    when eq(state, UInt<4>("h8")) : @[src/main/scala/v4/lsu/dcache.scala 249:3]
      when io.wb_req.ready : @[src/main/scala/v4/lsu/dcache.scala 250:5]
        state <= UInt<4>("h9") @[src/main/scala/v4/lsu/dcache.scala 251:13]
    when eq(state, UInt<4>("h9")) : @[src/main/scala/v4/lsu/dcache.scala 253:3]
      when and(io.meta_write.valid, io.meta_write.ready) : @[src/main/scala/v4/lsu/dcache.scala 254:5]
        state <= UInt<4>("ha") @[src/main/scala/v4/lsu/dcache.scala 255:13]
    when eq(state, UInt<4>("ha")) : @[src/main/scala/v4/lsu/dcache.scala 257:3]
      state <= UInt<4>("h0") @[src/main/scala/v4/lsu/dcache.scala 258:11]

    node debug_unused = xor(io.req.bits.opcode, UInt<3>("h7")) @[src/main/scala/v4/lsu/dcache.scala 999:1]
