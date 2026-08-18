circuit ProbeHarness : @[tests/fixtures/ProbeHarness.scala 1:1]
  module ProbeHarness : @[tests/fixtures/ProbeHarness.scala 3:1]
    input clock : Clock
    input reset : UInt<1>
    inst probe of BoomProbeUnit @[tests/fixtures/ProbeHarness.scala 8:15]

  module BoomProbeUnit : @[src/main/scala/v4/lsu/dcache.scala 145:1]
    input clock : Clock
    input reset : UInt<1>
    output io : { flip req : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, rep : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, meta_read : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<8>, tag : UInt<20> } }, meta_write : { flip ready : UInt<1>, valid : UInt<1>, bits : { idx : UInt<8>, tag : UInt<20> } }, wb_req : { flip ready : UInt<1>, valid : UInt<1>, bits : { source : UInt<4>, idx : UInt<8>, tag : UInt<20> } }, flip way_en : UInt<4>, flip wb_rdy : UInt<1>, flip mshr_rdy : UInt<1>, mshr_wb_rdy : UInt<1>, flip block_state : UInt<2>, lsu_release : { flip ready : UInt<1>, valid : UInt<1>, bits : { opcode : UInt<3>, address : UInt<40>, source : UInt<4> } }, state : { valid : UInt<1>, bits : UInt<40> } } @[src/main/scala/v4/lsu/dcache.scala 146:12]
