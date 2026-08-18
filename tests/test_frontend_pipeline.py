from pathlib import Path
import unittest

from frontend.pipeline import StaticFrontend
from frontend.slice import EventSliceMode


PROBE = Path(__file__).parent / "fixtures" / "boom_probeunit_logic.fir"
HIER = Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"


class StaticFrontendPipelineTests(unittest.TestCase):
    def test_pipeline_report_and_local_manifest(self):
        frontend = StaticFrontend.from_firrtl(PROBE.read_text(encoding="utf-8"))
        frontend.assert_complete("BoomProbeUnit")

        report = frontend.report()
        probe_status = next(
            module for module in report.modules if module.module == "BoomProbeUnit"
        )
        self.assertTrue(probe_status.complete)
        self.assertGreaterEqual(probe_status.event_count, 6)

        manifest = frontend.slice_manifest(
            "BoomProbeUnit",
            "BoomProbeUnit.io.rep.fire",
            mode=EventSliceMode.FULL,
        )
        self.assertTrue(manifest["analysis"]["complete"])
        self.assertEqual(manifest["semantic_labels"], [])
        self.assertIn("state", {item["name"] for item in manifest["signals"]})
        self.assertTrue(manifest["source_spans"])

    def test_pipeline_design_slice(self):
        frontend = StaticFrontend.from_firrtl(HIER.read_text(encoding="utf-8"))
        frontend.assert_complete("DCacheTop", "BoomProbeUnit")
        result = frontend.slice_design_event("DCacheTop::io.tl_c.fire")
        self.assertIn("DCacheTop.prober::state", result.signals)
        self.assertIn("DCacheTop::io.tl_b.valid", result.frontier)

    def test_pipeline_also_registers_valid_only_boundary_events(self):
        text = """\
circuit ValidTop : @[Valid.scala 1:1]
  module ValidTop : @[Valid.scala 2:1]
    output io : { state : { valid : UInt<1>, bits : UInt<8> } } @[Valid.scala 3:1]
    io.state.valid <= UInt<1>(1) @[Valid.scala 4:1]
    io.state.bits <= UInt<8>(0) @[Valid.scala 5:1]
"""
        frontend = StaticFrontend.from_firrtl(text)
        event = frontend.registries["ValidTop"].events[
            "ValidTop.io.state.valid"
        ]
        self.assertEqual(event.protocol.value, "valid")
        self.assertEqual(event.predicate, "io.state.valid")
        self.assertIsNone(event.ready)



if __name__ == "__main__":
    unittest.main()
