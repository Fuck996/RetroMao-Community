"""Theme package checks: format 7 presentation, carousel fields and host versions."""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest

from extension_tools import ROOT, read_json, write_json
import retromao


class ThemeFormatTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.deck = Path(self.directory.name).resolve() / "deck"
        shutil.copytree(ROOT / "examples/deck", self.deck)
        self.manifest = read_json(self.deck / "theme.json")
        self.metadata = read_json(self.deck / "retromao-package.json")

    def check(self, manifest=None, metadata=None):
        write_json(self.deck / "theme.json", manifest or self.manifest)
        write_json(self.deck / "retromao-package.json", metadata or self.metadata)
        return retromao.check_source(self.deck)

    def test_deck_example_declares_format_7_carousel(self):
        kind, metadata = self.check()
        self.assertEqual("THEME", kind)
        self.assertEqual(7, self.manifest["schemaVersion"])
        carousel = self.manifest["shell"]["recentCarousel"]
        self.assertEqual(("center", 20, "corner"), (carousel["focus"], carousel["size"], carousel["badges"]))
        self.assertEqual("1.0.43", metadata["minAppVersion"])

    def test_format_7_requires_presentation_and_current_host(self):
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("presentation")
        with self.assertRaises(ValueError):
            self.check(manifest)
        metadata = dict(self.metadata, minAppVersion="1.0.42")
        with self.assertRaises(ValueError):
            self.check(metadata=metadata)
        legacy = dict(copy.deepcopy(self.manifest), style="neutral")
        with self.assertRaises(ValueError):
            self.check(legacy)

    def test_format_7_fields_are_validated(self):
        for field, value in (("size", 9), ("size", 41), ("focus", "end"), ("badges", "always")):
            manifest = copy.deepcopy(self.manifest)
            manifest["shell"]["recentCarousel"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.check(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["presentation"]["showcaseModel"] = "disc"
        with self.assertRaises(ValueError):
            self.check(manifest)

    def test_older_formats_cannot_carry_format_7_fields(self):
        for field in ("focus", "size", "badges", "geometry"):
            manifest = copy.deepcopy(self.manifest)
            manifest["schemaVersion"] = 6
            manifest["style"] = "neutral"
            manifest.pop("presentation")
            carousel = manifest["shell"]["recentCarousel"]
            for other in ("focus", "size", "badges", "geometry"):
                if other != field:
                    carousel.pop(other, None)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.check(manifest, dict(self.metadata, minAppVersion="1.0.39"))
        manifest = copy.deepcopy(self.manifest)
        manifest["schemaVersion"] = 6
        manifest["style"] = "neutral"
        manifest.pop("presentation")
        for other in ("focus", "size", "badges", "geometry"):
            manifest["shell"]["recentCarousel"].pop(other, None)
        self.assertEqual("THEME", self.check(manifest, dict(self.metadata, minAppVersion="1.0.39"))[0])


if __name__ == "__main__":
    unittest.main()
