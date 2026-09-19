"""Per-prompt rules."""

from __future__ import annotations

from helpers import VALID_PROMPT, RepoTestCase


class PromptRuleTests(RepoTestCase):
    def test_valid_repository_has_no_findings(self) -> None:
        self.assertEqual(self.findings(), [])

    def test_encoding_problems(self) -> None:
        cases: dict[str, tuple[str | bytes, str]] = {
            "bom": (b"\xef\xbb\xbf" + VALID_PROMPT.encode(), "UTF-8 BOM"),
            "crlf": (VALID_PROMPT.replace("\n", "\r\n").encode(), "CRLF"),
            "no trailing newline": (VALID_PROMPT.rstrip("\n"), "trailing newline"),
            "invalid utf-8": (b"# Demo Coach\n\xff\xfe\n", "not valid UTF-8"),
        }
        for label, (content, fragment) in cases.items():
            with self.subTest(label):
                self.write_prompt(content)
                self.assertHasMessage(fragment)

    def test_length_over_max_is_an_error(self) -> None:
        self.write_prompt(VALID_PROMPT + "x" * 600 + "\n")
        self.assertHasMessage("exceeds the 500 limit")

    def test_length_over_target_is_only_a_warning(self) -> None:
        self.write_prompt(VALID_PROMPT + "x" * 250 + "\n")
        findings = self.findings()
        self.assertEqual([str(f.severity) for f in findings], ["warning"])
        self.assertIn("above the 300 target", findings[0].message)

    def test_structure_problems(self) -> None:
        untitled = VALID_PROMPT.replace("# Demo Coach", "Demo Coach", 1)
        retitled = VALID_PROMPT.replace("# Demo Coach", "# Other", 1)
        no_boundaries = VALID_PROMPT.replace("## Boundaries", "## Notes")
        no_language = VALID_PROMPT.replace("Language", "Tongue").replace("language", "x")
        no_data_rule = VALID_PROMPT.replace("not instructions", "fine")
        cases = {
            "no title": (untitled, "'# Title'"),
            "title mismatch": (retitled, "manifest title"),
            "no boundaries": (no_boundaries, "## Boundaries"),
            "no language": (no_language, "language rule"),
            "no data rule": (no_data_rule, "data-isolation"),
        }
        for label, (content, fragment) in cases.items():
            with self.subTest(label):
                self.write_prompt(content)
                self.assertHasMessage(fragment)

    def test_content_problems(self) -> None:
        cases = {
            "vendor": (VALID_PROMPT + "Works on ChatGPT.\n", "vendor or model name"),
            "marker": (VALID_PROMPT + "TODO finish\n", "leftover marker"),
            "emoji": (VALID_PROMPT + "Nice \U0001f600\n", "non-ASCII"),
        }
        for label, (content, fragment) in cases.items():
            with self.subTest(label):
                self.write_prompt(content)
                self.assertHasMessage(fragment)

    def test_persian_text_and_zwnj_are_allowed(self) -> None:
        persian = "\u0633\u0644\u0627\u0645 \u0645\u06cc\u200c\u0631\u0648\u0645"
        self.write_prompt(f"{VALID_PROMPT}{persian}\n")
        self.assertEqual(self.findings(), [])

    def test_filename_convention(self) -> None:
        self.write_prompt(VALID_PROMPT, name="Bad_Name.txt")
        self.assertHasMessage("must be lowercase-hyphenated")
