import copy
from pathlib import Path
import shutil
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen
from unittest.mock import patch

from build_script_plugin import build
from extension_tools import ROOT, read_json, validate_platform, validate_plugin, write_json
from preview import make_server
import retromao
import validate_languages


class ToolkitTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.plugin = self.root / "plugin"
        shutil.copytree(ROOT / "templates/plugin", self.plugin)

    def test_pack_rejects_missing_entry_page_and_schema_errors(self):
        original = read_json(self.plugin / "plugin.json")
        for field, value in (("entryPoint", "missing.js"), ("pages", [{"id": "main", "title": "Missing", "path": "absent.html"}]), ("apiVersion", 999), ("capabilities", ["UNKNOWN"])):
            manifest = copy.deepcopy(original)
            manifest[field] = value
            write_json(self.plugin / "plugin.json", manifest)
            with self.subTest(field=field), self.assertRaises(ValueError):
                build(self.plugin, self.root / "dist", "test")

    def test_zip_bytes_are_deterministic_and_metadata_is_not_shipped(self):
        first = build(self.plugin, self.root / "one", "test")
        (self.plugin / "main.js").touch()
        second = build(self.plugin, self.root / "two", "test")
        self.assertEqual(first["sha256"], second["sha256"])
        with self.assertRaises(ValueError):
            build(self.plugin, self.plugin / "output", "test")

    def test_private_files_are_rejected_before_packaging(self):
        (self.plugin / ".env").write_text("private", encoding="utf-8")
        with self.assertRaises(ValueError):
            build(self.plugin, self.root / "dist", "test")

    def test_platform_protocols_ids_and_builtin_collisions(self):
        source = self.root / "platform"
        shutil.copytree(ROOT / "templates/platform", source)
        original = read_json(source / "platform.json")
        validate_platform(source)
        for mutate in (
            lambda value: value.update(schemaVersion=1),
            lambda value: value["platform"].update(id="gba"),
            lambda value: value["launchers"][0].update(cores=[]),
            lambda value: value["launchers"][0].update(protocol="URI"),
            lambda value: value["launchers"][0].update(activity=".RelativeActivity"),
        ):
            manifest = copy.deepcopy(original)
            mutate(manifest)
            write_json(source / "platform.json", manifest)
            with self.assertRaises(ValueError):
                validate_platform(source)

    def test_new_language_retains_baseline_and_rejects_invalid_format(self):
        languages = self.root / "languages"
        languages.mkdir()
        shutil.copy(ROOT / "languages/zh-Hans.json", languages)
        source = read_json(languages / "zh-Hans.json")
        pack = {**source, "locale": "fr", "name": "Français", "author": "Example", "status": "draft", "messages": dict.fromkeys(source["messages"])}
        write_json(languages / "fr.json", pack)
        validate_languages.validate(languages)
        with self.assertRaises(ValueError):
            validate_languages.validate(languages, require_complete=True, locale="fr")
        pack["messages"][next(iter(pack["messages"]))] = "Unsupported %x"
        write_json(languages / "fr.json", pack)
        with self.assertRaises(ValueError):
            validate_languages.validate(languages)

    def test_language_schema_agrees_with_the_existing_language_files(self):
        from extension_tools import schema_check
        for language in (ROOT / "languages").glob("*.json"):
            if language.name != "index.json":
                schema_check(read_json(language), "language")

    def test_public_platform_corpus_matches_host_acceptance(self):
        source = self.root / "corpus"
        source.mkdir()
        for case in read_json(ROOT / "contracts/platform-cases.json"):
            write_json(source / "platform.json", case["manifest"])
            with self.subTest(case=case["name"]):
                if case["valid"]:
                    validate_platform(source)
                else:
                    with self.assertRaises(ValueError):
                        validate_platform(source)

    def test_publish_stops_before_side_effects_when_source_is_dirty(self):
        import argparse
        args = argparse.Namespace(source=str(ROOT / "templates/plugin"), repository="owner/repo", tag="test", notes="templates/release-notes.md")
        with patch.object(retromao, "command", return_value=" M templates/plugin/plugin.json") as command:
            with self.assertRaises(ValueError):
                retromao.publish(args)
            self.assertEqual(1, command.call_count)

    def test_publish_verifies_remote_bytes_before_changing_the_catalog(self):
        import argparse
        release_root = self.root / "release-repo"
        shutil.copytree(self.plugin, release_root / "extensions/demo")
        shutil.copytree(ROOT / "templates", release_root / "templates")
        (release_root / "plugins").mkdir()
        write_json(release_root / "plugins/index.json", {"schemaVersion": 1, "entries": []})
        notes = release_root / "notes.md"
        notes.write_text("## 中文\n实际变更\n## English\nActual changes\n## 日本語\n変更内容\n", encoding="utf-8")
        args = argparse.Namespace(source=str(release_root / "extensions/demo"), repository="owner/repo", tag="demo-1.0.0", notes=str(notes))
        calls = []
        corrupt = False
        def command(*arguments, **_):
            calls.append(arguments)
            if arguments[:3] == ("git", "status", "--porcelain"):
                return ""
            if arguments[:3] == ("git", "rev-parse", "HEAD"):
                return "a" * 40
            if arguments[:3] == ("git", "branch", "--show-current"):
                return "main"
            if arguments[:3] == ("git", "remote", "get-url"):
                return "https://github.com/owner/repo.git"
            if arguments[:2] == ("git", "ls-remote"):
                return "a" * 40 + " refs/heads/main"
            if arguments[:2] == ("gh", "api"):
                return "main"
            if arguments[:3] == ("gh", "release", "download"):
                destination = Path(arguments[arguments.index("--dir") + 1])
                archive = next((release_root / "dist").glob("*.zip"))
                (destination / archive.name).write_bytes(b"corrupt" if corrupt else archive.read_bytes())
            return ""
        with patch.object(retromao, "ROOT", release_root), patch.object(retromao, "command", side_effect=command):
            corrupt = True
            with self.assertRaises(ValueError):
                retromao.publish(args)
            self.assertEqual([], read_json(release_root / "plugins/index.json")["entries"])
            corrupt = False
            retromao.publish(args)
            self.assertEqual(1, len(read_json(release_root / "plugins/index.json")["entries"]))
            prior_calls = len(calls)
            with self.assertRaises(ValueError):
                retromao.publish(args)
            self.assertFalse(any(call[:3] == ("gh", "release", "create") for call in calls[prior_calls:]))

    def test_preview_serves_actual_sdk_blocks_traversal_and_closes_its_port(self):
        server = make_server(self.plugin, 0, ROOT / "tools/preview/fixtures.json")
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base + "/plugin/index.html") as response:
                html = response.read().decode("utf-8")
                self.assertLess(html.index("/__preview/mock-host.js"), html.index('src="page.js"'))
            with urlopen(base + "/__retromao/retromao.js") as response:
                self.assertEqual((ROOT / "sdk/runtime/retromao.js").read_bytes(), response.read())
            with self.assertRaises(HTTPError):
                urlopen(base + "/plugin/%2e%2e/plugin.json")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()
