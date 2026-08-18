from __future__ import annotations

import os
from pathlib import Path
import unittest

from frontend.pipeline import StaticFrontend
from frontend.design_graph import build_instance_hierarchy_index


REAL_FIRRTL = os.environ.get("MCM_REAL_FIRRTL")


@unittest.skipUnless(REAL_FIRRTL, "set MCM_REAL_FIRRTL to a real Chipyard .fir")
class RealChipyardFIRRTLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(REAL_FIRRTL)  # type: ignore[arg-type]
        cls.frontend = StaticFrontend.from_firrtl(
            path.read_text(encoding="utf-8"),
            eager=False,
        )

    def test_key_boom_l1_l2_modules_are_present_and_complete(self):
        for module in (
            "LSU",
            "BoomProbeUnit",
            "BoomMSHR",
            "BoomMSHRFile",
            "BoomNonBlockingDCache",
            "InclusiveCache",
            "InclusiveCacheBankScheduler",
        ):
            self.assertIn(module, self.frontend.design.modules)
            self.assertTrue(
                self.frontend.graph(module).complete,
                f"incomplete static coverage in {module}",
            )

    def _event(self, module: str, channel: str, suffix: str):
        return next(
            event
            for event in self.frontend.design_events()
            if event.module == module
            and event.channel == channel
            and event.instance_path.endswith(suffix)
        )

    def test_l2_probe_b_channel_has_complete_route_to_probeunit(self):
        l2_b = self._event("InclusiveCache", "auto.in.b", ".l2")
        probe_req = self._event("BoomProbeUnit", "io.req", ".dcache.prober")

        route = self.frontend.handshake_transport(
            l2_b.event_id,
            probe_req.event_id,
        )
        self.assertTrue(route.found)
        self.assertTrue(route.complete)
        self.assertGreater(len(route.valid_path.edges), 10)
        self.assertGreater(len(route.ready_path.edges), 10)
        self.assertTrue(route.stateful_instances)

    def test_probe_ack_c_channel_has_complete_route_back_to_l2(self):
        probe_rep = self._event("BoomProbeUnit", "io.rep", ".dcache.prober")
        l2_c = self._event("InclusiveCache", "auto.in.c", ".l2")

        route = self.frontend.handshake_transport(
            probe_rep.event_id,
            l2_c.event_id,
        )
        self.assertTrue(route.found)
        self.assertTrue(route.complete)
        self.assertGreater(len(route.valid_path.edges), 10)
        self.assertGreater(len(route.ready_path.edges), 10)
        self.assertTrue(route.stateful_instances)

    def test_l2_probe_subtree_slice_reaches_real_coherence_engines(self):
        l2_b = self._event("InclusiveCache", "auto.in.b", ".l2")
        result = self.frontend.slice_instance_event(
            l2_b.event_id,
            max_signals=20_000,
        )
        self.assertTrue(result.complete)
        hierarchy = build_instance_hierarchy_index(self.frontend.design)
        modules = {hierarchy.instances[path] for path in result.instances}
        self.assertIn("SourceB", modules)
        self.assertIn("Directory", modules)
        self.assertTrue(any(module.startswith("MSHR") for module in modules))
        self.assertGreater(len(result.signals), 1_000)

    def test_dcache_owned_probe_slice_does_not_need_whole_core(self):
        probe_req = self._event("BoomProbeUnit", "io.req", ".dcache.prober")
        dcache_root = probe_req.instance_path.rsplit(".prober", 1)[0]
        result = self.frontend.slice_instance_event(
            probe_req.event_id,
            root_instance=dcache_root,
            max_signals=20_000,
        )
        self.assertTrue(result.complete)
        hierarchy = build_instance_hierarchy_index(self.frontend.design)
        modules = {hierarchy.instances[path] for path in result.instances}
        self.assertIn("BoomProbeUnit", modules)
        self.assertIn("BoomMSHRFile", modules)
        self.assertIn("BoomWritebackUnit", modules)
        self.assertFalse(any(".core" in path for path in result.instances))




if __name__ == "__main__":
    unittest.main()
