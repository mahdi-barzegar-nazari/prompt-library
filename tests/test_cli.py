"""Command-line behavior."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

from helpers import VALID_PROMPT, RepoTestCase
from promptlint.cli import main


def run(root: Path, *args: str) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(["--root", str(root), *args])
    return code, buffer.getvalue()


class CliTests(RepoTestCase):
    def test_check_passes_on_valid_repo(self) -> None:
        code, out = run(self.root, "check")
        self.assertEqual(code, 0)
        self.assertIn("All checks passed.", out)
        self.assertIn("demo-prompt.txt", out)

    def test_check_fails_and_reports_errors(self) -> None:
        self.write_prompt(VALID_PROMPT + "TODO\n")
        code, out = run(self.root, "check")
        self.assertEqual(code, 1)
        self.assertIn("leftover marker", out)

    def test_warnings_pass_by_default_and_fail_when_strict(self) -> None:
        self.write_prompt(VALID_PROMPT + "x" * 250 + "\n")
        self.assertEqual(run(self.root, "check")[0], 0)
        self.assertEqual(run(self.root, "check", "--strict")[0], 1)

    def test_sync_readme_repairs_a_stale_table(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8").replace("A demo prompt.", "Old."), encoding="utf-8"
        )
        self.assertEqual(run(self.root, "sync-readme", "--check")[0], 1)
        self.assertEqual(run(self.root, "sync-readme")[0], 0)
        self.assertEqual(run(self.root, "sync-readme", "--check")[0], 0)
        self.assertIn("A demo prompt.", readme.read_text(encoding="utf-8"))
