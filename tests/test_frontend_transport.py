from __future__ import annotations

import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout

from frontend.cli import main as cli_main
from frontend.pipeline import StaticFrontend


TRANSPORT = """\
FIRRTL version 3.3.0
circuit Top : @[Top.scala 1:1]
  module Top : @[Top.scala 2:1]
    input clock : Clock
    inst src of Source @[Top.scala 3:1]
    inst q of Queue @[Top.scala 4:1]
    inst sink of Sink @[Top.scala 5:1]
    connect q.clock, clock
    connect q.io.in.valid, src.io.out.valid
    connect src.io.out.ready, q.io.in.ready
    connect q.io.out.ready, sink.io.in.ready
    connect sink.io.in.valid, q.io.out.valid

  module Source : @[Source.scala 1:1]
    output io : { out : { flip ready : UInt<1>, valid : UInt<1> } }
    connect io.out.valid, UInt<1>(1)

  module Queue : @[Queue.scala 1:1]
    input clock : Clock
    output io : { flip in : { flip ready : UInt<1>, valid : UInt<1> }, out : { flip ready : UInt<1>, valid : UInt<1> } }
    reg full : UInt<1>, clock
    connect io.out.valid, full
    connect io.in.ready, or(not(full), io.out.ready)
    when and(io.in.valid, io.in.ready) :
      connect full, UInt<1>(1)
    when and(io.out.valid, io.out.ready) :
      connect full, UInt<1>(0)

  module Sink : @[Sink.scala 1:1]
    output io : { flip in : { flip ready : UInt<1>, valid : UInt<1> } }
    connect io.in.ready, UInt<1>(1)
"""


class TransportPathTests(unittest.TestCase):
    def test_lazy_route_proves_valid_and_ready_through_stateful_queue(self):
        frontend = StaticFrontend.from_firrtl(TRANSPORT, eager=False)
        route = frontend.handshake_transport(
            "Top.src::io.out.fire",
            "Top.sink::io.in.fire",
        )

        self.assertTrue(route.found)
        self.assertTrue(route.complete)
        self.assertGreater(len(route.valid_path.edges), 0)
        self.assertGreater(len(route.ready_path.edges), 0)
        self.assertIn("Top.q", route.instances)
        self.assertIn("Top.q", route.stateful_instances)
        self.assertFalse(route.valid_path.truncated)
        self.assertFalse(route.ready_path.truncated)

    def test_transport_does_not_claim_semantic_alias(self):
        frontend = StaticFrontend.from_firrtl(TRANSPORT, eager=False)
        route = frontend.handshake_transport(
            "Top.src::io.out.fire",
            "Top.sink::io.in.fire",
        )
        self.assertNotEqual(route.from_event, route.to_event)

    def test_route_cli_emits_grounded_paths_and_locked_semantics(self):
        with tempfile.TemporaryDirectory() as directory:
            fir = Path(directory) / "transport.fir"
            fir.write_text(TRANSPORT, encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                rc = cli_main(
                    [
                        "route",
                        str(fir),
                        "--from-event",
                        "Top.src::io.out.fire",
                        "--to-event",
                        "Top.sink::io.in.fire",
                    ]
                )
            self.assertEqual(rc, 0)
            result = json.loads(stdout.getvalue())

        self.assertTrue(result["found"])
        self.assertTrue(result["complete"])
        self.assertTrue(result["valid_path"]["found"])
        self.assertTrue(result["ready_path"]["found"])
        self.assertEqual(result["semantic_labels"], [])
        self.assertIn(
            "Top.q",
            {entry["path"] for entry in result["stateful_instances"]},
        )

    def test_signal_budget_failure_is_fail_closed(self):
        frontend = StaticFrontend.from_firrtl(TRANSPORT, eager=False)
        route = frontend.handshake_transport(
            "Top.src::io.out.fire",
            "Top.sink::io.in.fire",
            max_signals=2,
        )
        self.assertFalse(route.complete)
        self.assertTrue(
            route.valid_path.truncated or route.ready_path.truncated
        )


if __name__ == "__main__":
    unittest.main()
