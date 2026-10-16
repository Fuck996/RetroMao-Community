import copy
import json
import tempfile
import unittest
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from build_script_plugin import build, validate_localizations


class PluginLocalizationTest(unittest.TestCase):
    def manifest(self):
        return {"id": "example.localized", "name": "Example plugin", "author": "Author", "version": "1.0.0", "minAppVersion": "0.9.94",
                "defaultLocale": "en", "description": "Example", "pages": [{"id": "main", "title": "Home", "path": "index.html"}],
                "messages": {"hint": "Choose"}, "localizations": {"zh-Hans": {"name": "示例插件", "description": "示例",
                "pages": {"main": "主页"}, "messages": {"hint": "选择"}}}}

    def test_published_entry_contains_only_store_text_and_zip_keeps_the_complete_plugin_dictionary(self):
        manifest = self.manifest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            (source / "index.html").write_text("<p>Example</p>", encoding="utf-8")
            entry = build(source, root / "output", "test-release")
            self.assertEqual("en", entry["defaultLocale"])
            self.assertEqual({"name": "示例插件", "description": "示例"}, entry["localizations"]["zh-Hans"])
            with ZipFile(root / "output" / entry["fileName"]) as archive:
                self.assertEqual(manifest, json.loads(archive.read("plugin.json")))

    def test_publishing_requires_an_explicit_default_and_simplified_chinese(self):
        for missing in ("defaultLocale", "localizations"):
            manifest = self.manifest()
            del manifest[missing]
            with self.assertRaises(ValueError):
                validate_localizations(manifest)

    def test_configuration_page_references_a_declared_page_and_supporting_host(self):
        manifest = self.manifest()
        manifest["configurationPage"] = "main"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            output = root / "output"
            (source / "index.html").write_text("<p>Configuration</p>", encoding="utf-8")
            for minimum, page in (("0.9.94", "main"), ("0.9.95", "missing"), ("0.9.95", "main")):
                manifest.update(minAppVersion=minimum, configurationPage=page)
                (source / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
                if minimum == "0.9.95" and page == "main":
                    entry = build(source, output, "test-release")
                    with ZipFile(output / entry["fileName"]) as archive:
                        self.assertEqual("main", json.loads(archive.read("plugin.json"))["configurationPage"])
                else:
                    with self.assertRaises(ValueError):
                        build(source, output, "test-release")

    def test_translations_cannot_drop_or_rename_native_and_custom_keys(self):
        for key in ("pages", "messages"):
            manifest = copy.deepcopy(self.manifest())
            manifest["localizations"]["zh-Hans"][key] = {"renamed": "文字"}
            with self.assertRaises(ValueError):
                validate_localizations(manifest)

    def test_localized_plugins_declare_the_host_version_that_preserves_language_metadata(self):
        manifest = self.manifest()
        manifest["minAppVersion"] = "0.9.91"
        with self.assertRaises(ValueError):
            validate_localizations(manifest)

    def test_cli_json_preserves_japanese_on_non_utf8_consoles(self):
        manifest = self.manifest()
        manifest["localizations"]["ja"] = {"name": "サンプル・プラグイン", "description": "例", "pages": {"main": "ホーム"}, "messages": {"hint": "選択"}}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            (source / "index.html").write_text("<p>Example</p>", encoding="utf-8")
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("build_script_plugin.py")), str(source),
                "--output", str(root / "output"), "--release-tag", "test-release"],
                env={**os.environ, "PYTHONIOENCODING": "gbk"}, capture_output=True, check=True)
            self.assertEqual("サンプル・プラグイン", json.loads(result.stdout)["localizations"]["ja"]["name"])
            sync = subprocess.run([sys.executable, str(Path(__file__).with_name("build_sync_examples.py")),
                "--output", str(root / "sync"), "--release-tag", "test-release"],
                env={**os.environ, "PYTHONIOENCODING": "gbk"}, capture_output=True, check=True)
            entries = json.loads(sync.stdout)
            self.assertEqual(2, len(entries))
            self.assertEqual("お気に入りの同期", entries[0]["localizations"]["ja"]["name"])


if __name__ == "__main__":
    unittest.main()
