"""Integration tests against the real repository contents."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from promptlint.checks import run_checks
from promptlint.registry import load_manifest

REPO_ROOT = Path(__file__).resolve().parent.parent


class RealRepositoryTests(unittest.TestCase):
    def test_repository_passes_its_own_checks(self) -> None:
        report = run_checks(REPO_ROOT)
        self.assertEqual([str(f) for f in report.errors], [])

    def test_bug_report_form_lists_every_prompt(self) -> None:
        form = (REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml").read_text(
            encoding="utf-8"
        )
        options = set(re.findall(r"^\s+- (\S+-prompt\.txt)$", form, re.MULTILINE))
        listed = {entry.file for entry in load_manifest(REPO_ROOT)}
        self.assertEqual(options, listed)

    def test_prompt_count_badge_matches_manifest(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        match = re.search(r"badge/prompts-(\d+)-", readme)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(int(match.group(1)), len(load_manifest(REPO_ROOT)))
