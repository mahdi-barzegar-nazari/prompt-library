"""README table generation."""

from __future__ import annotations

import unittest

from promptlint.models import PromptEntry
from promptlint.readme import END_MARKER, START_MARKER, MarkerError, render_table, replace_block

ENTRY = PromptEntry("a-prompt.txt", "A", "Cat", "Does a thing.")


class ReadmeTests(unittest.TestCase):
    def test_render_table_links_into_prompts_dir(self) -> None:
        table = render_table([ENTRY])
        self.assertIn("[`a-prompt.txt`](./prompts/a-prompt.txt) | Cat | Does a thing. |", table)

    def test_replace_block_is_idempotent(self) -> None:
        source = f"head\n{START_MARKER}\n{END_MARKER}\ntail\n"
        once = replace_block(source, render_table([ENTRY]))
        self.assertEqual(replace_block(once, render_table([ENTRY])), once)
        self.assertTrue(once.startswith("head\n"))
        self.assertTrue(once.endswith("tail\n"))

    def test_marker_errors(self) -> None:
        cases = {
            "none": "no markers",
            "duplicated": f"{START_MARKER}{START_MARKER}{END_MARKER}",
            "reversed": f"{END_MARKER}{START_MARKER}",
        }
        for label, text in cases.items():
            with self.subTest(label), self.assertRaises(MarkerError):
                replace_block(text, "table")
