"""Manifest and configuration loading."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import RepoTestCase, write
from promptlint.models import Limits
from promptlint.registry import ManifestError, find_root, load_limits, load_manifest


class RegistryTests(RepoTestCase):
    def test_load_manifest(self) -> None:
        entries = load_manifest(self.root)
        self.assertEqual([e.file for e in entries], ["demo-prompt.txt"])

    def test_missing_field(self) -> None:
        write(self.root / "prompts" / "manifest.toml", '[[prompt]]\nfile = "x-prompt.txt"\n')
        with self.assertRaisesRegex(ManifestError, "missing field"):
            load_manifest(self.root)

    def test_limits_from_pyproject(self) -> None:
        self.assertEqual(load_limits(self.root), Limits(max_chars=500, target_chars=300))

    def test_limits_default_without_pyproject(self) -> None:
        (self.root / "pyproject.toml").unlink()
        self.assertEqual(load_limits(self.root), Limits())

    def test_find_root_walks_upwards(self) -> None:
        nested = self.root / "docs" / "deep"
        nested.mkdir(parents=True)
        self.assertEqual(find_root(nested), self.root.resolve())


class MissingManifestTests(unittest.TestCase):
    def test_missing_manifest_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ManifestError):
            load_manifest(Path(tmp))
