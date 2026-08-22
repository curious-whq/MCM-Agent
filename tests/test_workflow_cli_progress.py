from __future__ import annotations

from io import StringIO
import unittest

from workflow.cli import _SemanticProgress


class SemanticProgressRendererTests(unittest.TestCase):
    def test_renderer_writes_progress_only_to_its_stderr_stream(self):
        stream = StringIO()
        progress = _SemanticProgress(enabled=True, stream=stream)
        progress({"stage": "validation_started", "total": 2})
        progress({
            "stage": "phase_started",
            "index": 1,
            "total": 2,
            "axiom_id": "A1",
            "checker": "history_order",
            "phase": "formal",
        })
        progress({
            "stage": "obligation_completed",
            "index": 1,
            "total": 2,
            "axiom_id": "A1",
            "checker": "history_order",
            "validation_level": "FORMALLY_PROVED",
        })
        progress({
            "stage": "validation_completed",
            "total": 2,
            "counts": {"FORMALLY_PROVED": 2},
        })
        progress.close()

        rendered = stream.getvalue()
        self.assertIn("done=1/2", rendered)
        self.assertIn("current=1/2", rendered)
        self.assertIn("A1/history_order", rendered)
        self.assertIn("formal", rendered)
        self.assertIn("trusted=2", rendered)
        self.assertTrue(rendered.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
