from pathlib import Path
import unittest

from frontend.pipeline import StaticFrontend


FIXTURE = Path(__file__).parent / "fixtures" / "boom_dcache_hierarchy.fir"


class ConnectorDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frontend = StaticFrontend.from_firrtl(
            FIXTURE.read_text(encoding="utf-8")
        )
        cls.connectors = {
            (connector.from_event, connector.to_event): connector
            for connector in cls.frontend.design_connectors()
        }

    def test_top_b_channel_is_directly_linked_to_probe_request(self):
        key = (
            "DCacheTop::io.tl_b.fire",
            "DCacheTop.prober::io.req.fire",
        )
        self.assertIn(key, self.connectors)
        connector = self.connectors[key]
        self.assertEqual(
            connector.valid_edge,
            (
                "DCacheTop::io.tl_b.valid",
                "DCacheTop.prober::io.req.valid",
            ),
        )
        self.assertEqual(
            connector.ready_edge,
            (
                "DCacheTop.prober::io.req.ready",
                "DCacheTop::io.tl_b.ready",
            ),
        )

    def test_probe_response_is_directly_linked_to_top_c_channel(self):
        key = (
            "DCacheTop.prober::io.rep.fire",
            "DCacheTop::io.tl_c.fire",
        )
        self.assertIn(key, self.connectors)

    def test_unrelated_probe_internal_channels_are_not_linked_to_tl(self):
        pairs = set(self.connectors)
        self.assertNotIn(
            (
                "DCacheTop.prober::io.meta_read.fire",
                "DCacheTop::io.tl_c.fire",
            ),
            pairs,
        )


if __name__ == "__main__":
    unittest.main()
