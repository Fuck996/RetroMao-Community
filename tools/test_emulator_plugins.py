import copy
from pathlib import Path
import tempfile
import unittest
import zipfile

from build_script_plugin import build
from extension_tools import ROOT, read_json, validate_plugin, write_json


class EmulatorPluginTest(unittest.TestCase):
    def setUp(self):
        self.manifest = read_json(ROOT / "extensions/azahar-plus/plugin.json")

    def test_editable_package_contains_business_page_and_default_azahar(self):
        source = ROOT / "extensions/azahar-plus"
        validate_plugin(source)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            entry = build(source, output, "azahar-plus-1.1.0")
            with zipfile.ZipFile(output / entry["fileName"]) as archive:
                names = archive.namelist()
                self.assertIn("plugin.json", names)
                self.assertIn("index.html", names)
                self.assertIn("page.js", names)
                self.assertIn("page.css", names)
                self.assertEqual(self.manifest["emulators"][0]["packageName"], "io.github.azaharplus.android")
                self.assertTrue(self.manifest["editableEmulators"])

    def test_contract_rejects_old_host_duplicate_ids_and_invalid_components(self):
        variants = []
        for key, value in (("minAppVersion", "0.9.140"), ("capabilities", []), ("editableEmulators", False)):
            manifest = copy.deepcopy(self.manifest)
            manifest[key] = value
            variants.append(manifest)
        for key, value in (("activity", ".Activity"), ("packageName", "invalid"), ("platforms", []),
                           ("platforms", ["3ds", "3ds"]), ("platforms", [f"platform{i}" for i in range(65)]), ("mimeType", "invalid")):
            manifest = copy.deepcopy(self.manifest)
            manifest["emulators"][0][key] = value
            variants.append(manifest)
        duplicate = copy.deepcopy(self.manifest)
        duplicate["emulators"].append(duplicate["emulators"][0])
        variants.append(duplicate)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            for manifest in variants:
                with self.subTest(manifest=manifest):
                    write_json(source / "plugin.json", manifest)
                    with self.assertRaises(ValueError):
                        validate_plugin(source)


if __name__ == "__main__":
    unittest.main()
