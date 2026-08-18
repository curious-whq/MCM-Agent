import unittest

from frontend.firrtl import FirrtlParseError, parse_firrtl, parse_type
from frontend.model import (
    BundleType,
    GroundType,
    PortDirection,
    SourceLoc,
    VectorType,
)


class FIRRTLFrontendTests(unittest.TestCase):
    def test_source_locator_parses_from_right(self):
        loc = SourceLoc.parse("path with spaces/Foo.scala 12:34")
        self.assertEqual(loc.file, "path with spaces/Foo.scala")
        self.assertEqual(loc.line, 12)
        self.assertEqual(loc.column, 34)

    def test_bundle_orientation_flattens_nested_flips(self):
        type_ = parse_type(
            "{ flip req : { flip ready : UInt<1>, valid : UInt<1>, "
            "bits : { address : UInt<40> } }, "
            "rep : { flip ready : UInt<1>, valid : UInt<1> } }"
        )

        from frontend.model import Port, flatten_type

        leaves = flatten_type(
            type_,
            prefix="io",
            direction=PortDirection.OUTPUT,
            source=None,
        )
        directions = {
            leaf.path: leaf.direction
            for leaf in leaves
        }

        self.assertEqual(
            directions["io.req.valid"],
            PortDirection.INPUT,
        )
        self.assertEqual(
            directions["io.req.ready"],
            PortDirection.OUTPUT,
        )
        self.assertEqual(
            directions["io.req.bits.address"],
            PortDirection.INPUT,
        )
        self.assertEqual(
            directions["io.rep.valid"],
            PortDirection.OUTPUT,
        )
        self.assertEqual(
            directions["io.rep.ready"],
            PortDirection.INPUT,
        )

    def test_vectors_are_flattened(self):
        from frontend.model import flatten_type

        type_ = parse_type("UInt<8>[2]")
        leaves = flatten_type(
            type_,
            prefix="io.lane",
            direction=PortDirection.INPUT,
            source=None,
        )
        self.assertEqual(
            [leaf.path for leaf in leaves],
            ["io.lane[0]", "io.lane[1]"],
        )

    def test_missing_circuit_is_rejected(self):
        with self.assertRaises(FirrtlParseError):
            parse_firrtl("module A :\n  input x : UInt<1>\n")


if __name__ == "__main__":
    unittest.main()
