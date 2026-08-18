from pathlib import Path
import unittest

from frontend.pipeline import StaticFrontend
from frontend.slice import EventSliceMode


FIXTURE = Path(__file__).parent / "fixtures" / "boom_mshr_logic.fir"


class MSHRStaticFrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frontend = StaticFrontend.from_firrtl(
            FIXTURE.read_text(encoding="utf-8")
        )

    def test_mshr_structural_analysis_is_complete(self):
        self.frontend.assert_complete("BoomMSHR")
        events = self.frontend.registries["BoomMSHR"].events
        self.assertIn("BoomMSHR.io.mem_acquire.fire", events)
        self.assertIn("BoomMSHR.io.mem_grant.fire", events)
        self.assertIn("BoomMSHR.io.mem_finish.fire", events)

    def test_mem_finish_slice_reaches_rpq_barrier_and_grant_state(self):
        result = self.frontend.slice_event(
            "BoomMSHR",
            "BoomMSHR.io.mem_finish.fire",
            mode=EventSliceMode.OCCURRENCE,
        )
        self.assertIn("state", result.signals)
        self.assertIn("grantack_valid", result.signals)
        self.assertIn("rpq.io.empty", result.signals)
        self.assertIn("rpq.io.enq.valid", result.signals)
        self.assertIn("io.mem_grant.valid", result.signals)
        self.assertTrue(result.complete)

    def test_partition_exposes_stateful_mshr_cone_without_semantic_label(self):
        plan = self.frontend.partition("BoomMSHR")
        finish = next(
            cone
            for cone in plan.event_cones
            if cone.event_id == "BoomMSHR.io.mem_finish.fire"
        )
        self.assertIn("state", finish.registers)
        self.assertIn("grantack_valid", finish.registers)
        self.assertTrue(all(region.id.startswith("state-scc-") for region in plan.regions))


if __name__ == "__main__":
    unittest.main()
