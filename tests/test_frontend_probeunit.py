from pathlib import Path
import unittest

from frontend.boundary import discover_boundary
from frontend.firrtl import parse_firrtl
from frontend.hierarchy import discover_hierarchy
from frontend.model import PortDirection
from frontend.registry import ChannelDirection, discover_decoupled_events


FIXTURE = Path(__file__).parent / "fixtures" / "boom_probeunit.fir"


class ProbeUnitFrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = parse_firrtl(
            FIXTURE.read_text(encoding="utf-8")
        )
        cls.probe = cls.design.module("BoomProbeUnit")
        cls.boundary = discover_boundary(cls.probe)
        cls.registry = discover_decoupled_events(
            cls.probe,
            cls.boundary,
        )

    def test_hierarchy_discovers_probe_instance(self):
        tree = discover_hierarchy(self.design)
        self.assertEqual(tree.path, "ProbeHarness")
        self.assertEqual(len(tree.children), 1)

        probe = tree.children[0]
        self.assertEqual(probe.path, "ProbeHarness.probe")
        self.assertEqual(probe.module, "BoomProbeUnit")
        self.assertFalse(probe.external)

    def test_boundary_recovers_req_and_rep_directions(self):
        by_path = {
            port.path: port
            for port in self.boundary
        }

        self.assertEqual(
            by_path["io.req.valid"].direction,
            PortDirection.INPUT,
        )
        self.assertEqual(
            by_path["io.req.ready"].direction,
            PortDirection.OUTPUT,
        )
        self.assertEqual(
            by_path["io.rep.valid"].direction,
            PortDirection.OUTPUT,
        )
        self.assertEqual(
            by_path["io.rep.ready"].direction,
            PortDirection.INPUT,
        )

    def test_registry_finds_all_decoupled_channels(self):
        ids = {
            event.event_id
            for event in self.registry.sorted_events()
        }

        self.assertEqual(
            ids,
            {
                "BoomProbeUnit.io.req.fire",
                "BoomProbeUnit.io.rep.fire",
                "BoomProbeUnit.io.meta_read.fire",
                "BoomProbeUnit.io.meta_write.fire",
                "BoomProbeUnit.io.wb_req.fire",
                "BoomProbeUnit.io.lsu_release.fire",
            },
        )

    def test_registry_direction_is_mechanical(self):
        events = {
            event.channel: event
            for event in self.registry.sorted_events()
        }

        self.assertEqual(
            events["io.req"].direction,
            ChannelDirection.RECEIVE,
        )

        for channel in (
            "io.rep",
            "io.meta_read",
            "io.meta_write",
            "io.wb_req",
            "io.lsu_release",
        ):
            self.assertEqual(
                events[channel].direction,
                ChannelDirection.SEND,
            )

    def test_event_predicate_and_payload_are_grounded(self):
        events = {
            event.channel: event
            for event in self.registry.sorted_events()
        }
        req = events["io.req"]

        self.assertEqual(
            req.predicate,
            "io.req.valid && io.req.ready",
        )

        payload_paths = {
            port.path
            for port in req.payload
        }
        self.assertIn("io.req.bits.opcode", payload_paths)
        self.assertIn("io.req.bits.address", payload_paths)
        self.assertIn("io.req.bits.source", payload_paths)

    def test_event_source_maps_back_to_boom_scala(self):
        events = {
            event.channel: event
            for event in self.registry.sorted_events()
        }
        req = events["io.req"]

        self.assertTrue(req.sources)
        source = req.sources[0]
        self.assertEqual(
            source.file,
            "src/main/scala/v4/lsu/dcache.scala",
        )
        self.assertEqual(source.line, 146)


if __name__ == "__main__":
    unittest.main()
