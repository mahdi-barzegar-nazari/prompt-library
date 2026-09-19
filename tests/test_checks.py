"""Repository-level checks."""

from __future__ import annotations

from helpers import SMOKE, RepoTestCase, write
from promptlint.checks import smoke_check_counts


class ManifestVsDiskTests(RepoTestCase):
    def test_unlisted_prompt_file(self) -> None:
        self.write_prompt("# Extra\n", name="extra-prompt.txt")
        self.assertHasMessage("is not listed in the manifest")

    def test_listed_but_missing_file(self) -> None:
        (self.root / "prompts" / "demo-prompt.txt").unlink()
        self.assertHasMessage("does not exist")

    def test_duplicate_manifest_entry(self) -> None:
        manifest = self.root / "prompts" / "manifest.toml"
        text = manifest.read_text(encoding="utf-8")
        manifest.write_text(text + "\n" + text, encoding="utf-8")
        self.assertHasMessage("listed more than once")

    def test_broken_manifest_is_reported_not_raised(self) -> None:
        write(self.root / "prompts" / "manifest.toml", "[[prompt]\n")
        self.assertHasMessage("invalid TOML")


class SmokeTestTests(RepoTestCase):
    def test_counts_numbered_checks_per_section(self) -> None:
        self.assertEqual(smoke_check_counts(SMOKE), {"demo-prompt.txt": 3})

    def test_missing_section(self) -> None:
        write(self.root / "tests" / "smoke-tests.md", "# Smoke Tests\n")
        self.assertHasMessage("has no section for demo-prompt.txt")

    def test_too_few_checks(self) -> None:
        write(self.root / "tests" / "smoke-tests.md", "## demo-prompt.txt\n\n1. Only one.\n")
        self.assertHasMessage("at least 3")

    def test_missing_file(self) -> None:
        (self.root / "tests" / "smoke-tests.md").unlink()
        self.assertHasMessage("file is missing")


class ReadmeSyncTests(RepoTestCase):
    def test_stale_table(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8").replace("A demo prompt.", "Old text."),
            encoding="utf-8",
        )
        self.assertHasMessage("prompt table is stale")

    def test_missing_markers(self) -> None:
        write(self.root / "README.md", "# Demo\n")
        self.assertHasMessage("must contain one")


class DocLinkTests(RepoTestCase):
    def test_broken_relative_link(self) -> None:
        write(self.root / "docs" / "a.md", "See [x](./missing.md).\n")
        self.assertHasMessage("broken link ./missing.md")

    def test_valid_link_with_anchor(self) -> None:
        write(self.root / "docs" / "b.md", "# B\n")
        write(self.root / "docs" / "a.md", "See [b](./b.md#top).\n")
        self.assertEqual(self.findings(), [])

    def test_ignores_external_anchor_and_mailto_links(self) -> None:
        write(
            self.root / "docs" / "a.md",
            "[w](https://example.com) [a](#top) [m](mailto:a@b.co)\n",
        )
        self.assertEqual(self.findings(), [])

    def test_ignores_links_inside_code(self) -> None:
        write(
            self.root / "docs" / "a.md",
            "```md\n[x](./nope.md)\n```\n\nInline `[y](./nope.md)` too.\n",
        )
        self.assertEqual(self.findings(), [])
