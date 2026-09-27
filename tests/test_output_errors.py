import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from headline_harvest.cli import main


class OutputErrorTests(unittest.TestCase):
    html = '<h2><a href="/news">A headline</a></h2>'

    def test_output_parent_that_is_a_file_returns_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder) / "blocked"
            parent.write_text("keep this content", encoding="utf-8")
            output = io.StringIO()
            with patch("headline_harvest.cli.fetch", return_value=self.html):
                with self.assertLogs(level="ERROR"), contextlib.redirect_stdout(output):
                    result = main(["https://example.test", "-o", str(parent / "news.json")])
            self.assertEqual(result, 1)
            self.assertEqual(output.getvalue(), "")
            self.assertEqual(parent.read_text(encoding="utf-8"), "keep this content")

    def test_permission_error_is_reported_without_traceback(self):
        with patch("headline_harvest.cli.fetch", return_value=self.html):
            with patch("headline_harvest.cli.export", side_effect=PermissionError("permission denied")):
                with self.assertLogs(level="ERROR") as logs:
                    result = main(["https://example.test", "-o", "news.json"])
        self.assertEqual(result, 1)
        self.assertTrue(any("permission denied" in message for message in logs.output))
