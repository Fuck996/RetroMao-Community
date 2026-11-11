"""Theme package checks for legacy presentation and format 8 switch sounds."""

import copy
import hashlib
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import wave
from zipfile import ZipFile

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

    def use_format_7(self):
        self.manifest["schemaVersion"] = 7
        self.manifest["assets"].pop("sound.mediaSwitch")
        self.manifest.pop("mediaSwitchVolume")
        self.metadata["minAppVersion"] = "1.0.46"

    def write_switch_sound(self, rate=48000, channels=2, frames=12000, sample_width=2):
        path = self.deck / self.manifest["assets"]["sound.mediaSwitch"]
        with wave.open(str(path), "wb") as sound:
            sound.setnchannels(channels)
            sound.setsampwidth(sample_width)
            sound.setframerate(rate)
            sound.writeframes(b"\0" * frames * channels * sample_width)
        return path

    def test_deck_example_declares_format_8_sound_and_carousel(self):
        kind, metadata = self.check()
        self.assertEqual("THEME", kind)
        self.assertEqual(8, self.manifest["schemaVersion"])
        carousel = self.manifest["shell"]["recentCarousel"]
        self.assertEqual(("center", 20, "corner"), (carousel["focus"], carousel["size"], carousel["badges"]))
        self.assertEqual("1.1.7", metadata["minAppVersion"])
        self.assertEqual("audio/media-switch.wav", self.manifest["assets"]["sound.mediaSwitch"])
        self.assertEqual(0.8, self.manifest["mediaSwitchVolume"])
        self.assertEqual("floor", self.manifest["presentation"]["details"]["stage"])

    def test_floor_detail_stage_requires_host_1_0_46(self):
        self.use_format_7()
        self.assertEqual("THEME", self.check()[0])
        with self.assertRaisesRegex(ValueError, "floor detail stage requires host 1.0.46"):
            self.check(metadata=dict(self.metadata, minAppVersion="1.0.45"))
        manifest = copy.deepcopy(self.manifest)
        manifest["presentation"]["details"]["stage"] = "panel"
        manifest["presentation"].pop("detailStage")
        self.assertEqual("THEME", self.check(manifest, dict(self.metadata, minAppVersion="1.0.43"))[0])
        manifest["presentation"]["detailStage"] = {"reflection": 0.5}
        with self.assertRaises(ValueError):
            self.check(manifest)

    def test_format_7_requires_presentation_and_current_host(self):
        self.use_format_7()
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("presentation")
        with self.assertRaisesRegex(ValueError, "Theme format 7 requires presentation"):
            self.check(manifest)
        metadata = dict(self.metadata, minAppVersion="1.0.42")
        with self.assertRaisesRegex(ValueError, "Theme format 7 requires host 1.0.43"):
            self.check(metadata=metadata)
        legacy = dict(copy.deepcopy(self.manifest), style="neutral")
        with self.assertRaises(ValueError):
            self.check(legacy)

    def test_format_7_fields_are_validated(self):
        self.use_format_7()
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
        self.use_format_7()
        for field in ("focus", "size", "badges", "geometry"):
            manifest = copy.deepcopy(self.manifest)
            manifest["schemaVersion"] = 6
            manifest["style"] = "neutral"
            manifest.pop("presentation")
            carousel = manifest["shell"]["recentCarousel"]
            for other in ("focus", "size", "badges", "geometry"):
                if other != field:
                    carousel.pop(other, None)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "require theme format 7"):
                self.check(manifest, dict(self.metadata, minAppVersion="1.0.39"))
        manifest = copy.deepcopy(self.manifest)
        manifest["schemaVersion"] = 6
        manifest["style"] = "neutral"
        manifest.pop("presentation")
        for other in ("focus", "size", "badges", "geometry"):
            manifest["shell"]["recentCarousel"].pop(other, None)
        self.assertEqual("THEME", self.check(manifest, dict(self.metadata, minAppVersion="1.0.39"))[0])

    def test_format_8_requires_host_1_1_7_even_without_sound(self):
        for with_sound in (True, False):
            manifest = copy.deepcopy(self.manifest)
            if not with_sound:
                manifest["assets"].pop("sound.mediaSwitch")
                manifest.pop("mediaSwitchVolume")
            with self.subTest(with_sound=with_sound):
                with self.assertRaisesRegex(ValueError, "Theme format 8 requires host 1.1.7"):
                    self.check(manifest, dict(self.metadata, minAppVersion="1.1.6"))
                for version in ("1.1.7", "1.1.10"):
                    self.assertEqual("THEME", self.check(manifest, dict(self.metadata, minAppVersion=version))[0])

    def test_older_format_rejects_switch_sound_on_a_current_host(self):
        self.use_format_7()
        self.metadata["minAppVersion"] = "1.1.7"
        self.assertEqual("THEME", self.check()[0])
        self.manifest["assets"]["sound.mediaSwitch"] = "audio/media-switch.wav"
        with self.assertRaisesRegex(ValueError, "Switch sounds require theme format 8"):
            self.check()

    def test_switch_volume_bounds_types_and_required_asset(self):
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("mediaSwitchVolume")
        self.assertEqual("THEME", self.check(manifest)[0])
        for value in (None, 0, 0.8, 1):
            with self.subTest(volume=value):
                self.assertEqual("THEME", self.check(dict(manifest, mediaSwitchVolume=value))[0])
        for value in (-0.01, 1.01, True, "0.8", float("nan"), float("inf")):
            with self.subTest(volume=value), self.assertRaisesRegex(ValueError, "Switch sound volume"):
                self.check(dict(manifest, mediaSwitchVolume=value))
        manifest["assets"].pop("sound.mediaSwitch")
        with self.assertRaisesRegex(ValueError, "requires a sound asset"):
            self.check(dict(manifest, mediaSwitchVolume=0))

    def test_switch_wav_encoding_and_duration_boundaries(self):
        for rate, channels, frames in ((8000, 1, 2000), (48000, 2, 12000)):
            with self.subTest(rate=rate, channels=channels):
                self.write_switch_sound(rate, channels, frames)
                self.assertEqual("THEME", self.check()[0])
        for rate, channels, frames, width in (
            (16000, 1, 4001, 2), (48000, 2, 12001, 2), (8000, 1, 0, 2),
            (7999, 1, 1, 2), (48001, 1, 1, 2), (8000, 3, 1, 2), (8000, 1, 1, 1),
        ):
            with self.subTest(rate=rate, channels=channels, frames=frames, width=width):
                self.write_switch_sound(rate, channels, frames, width)
                with self.assertRaises(ValueError):
                    self.check()

    def test_switch_wav_rejects_missing_truncated_and_inconsistent_files(self):
        path = self.write_switch_sound()
        original = path.read_bytes()
        for offset in (4, 40):
            with self.subTest(header_offset=offset):
                corrupt = bytearray(original)
                struct.pack_into("<I", corrupt, offset, 1)
                path.write_bytes(corrupt)
                with self.assertRaisesRegex(ValueError, "standard 16-bit PCM WAV"):
                    self.check()
        path.write_bytes(original[:20])
        with self.assertRaisesRegex(ValueError, "PCM WAV file"):
            self.check()
        renamed = path.with_suffix(".ogg")
        renamed.write_bytes(original)
        manifest = copy.deepcopy(self.manifest)
        manifest["assets"]["sound.mediaSwitch"] = renamed.relative_to(self.deck).as_posix()
        with self.assertRaisesRegex(ValueError, "PCM WAV file"):
            self.check(manifest)
        path.unlink()
        with self.assertRaisesRegex(ValueError, "Missing, empty or oversized"):
            self.check()

    def test_theme_package_preserves_declared_sound_and_archive_integrity(self):
        self.check()
        output = Path(self.directory.name) / "dist"
        entry = retromao.pack(self.deck, output, "test-theme-format-8")
        package = output / entry["fileName"]
        self.assertEqual("1.1.7", entry["minAppVersion"])
        self.assertEqual(package.stat().st_size, entry["sizeBytes"])
        self.assertEqual(hashlib.sha256(package.read_bytes()).hexdigest(), entry["sha256"])
        expected = {"theme.json", *self.manifest["assets"].values()}
        with ZipFile(package) as archive:
            self.assertEqual(expected, set(archive.namelist()))
            self.assertEqual(len(expected), len(archive.namelist()))
            self.assertIsNone(archive.testzip())
            for name in expected:
                self.assertEqual((self.deck / name).read_bytes(), archive.read(name), name)


if __name__ == "__main__":
    unittest.main()
