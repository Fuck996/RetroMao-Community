"""Exercise API release policy against real local Git history."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import check_api


class ApiHistoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="retromao-api-history-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.snapshot = self.root / "sdk/releases/1.0.0.json"
        self.snapshot.parent.mkdir(parents=True)
        self.previous = {"version": "1.0.0", "members": [{"path": "data.get", "declaration": "get(): Promise<Json>", "capabilities": [], "contexts": ["PAGE"], "rpc": "data.get"}]}
        self.snapshot.write_text(json.dumps(self.previous) + "\n", encoding="utf-8", newline="\n")
        (self.root / ".gitattributes").write_text("*.json text eol=lf\n", encoding="utf-8", newline="\n")
        self.git("init", "--quiet")
        self.git("add", ".gitattributes", "sdk/releases/1.0.0.json")
        self.git("-c", "user.name=API test", "-c", "user.email=api-test@example.invalid", "commit", "--quiet", "-m", "API baseline")
        self.baseline = self.git("rev-parse", "HEAD").strip()
        self.root_patch = patch.object(check_api, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def git(self, *arguments):
        return subprocess.check_output(["git", *arguments], cwd=self.root, text=True, stderr=subprocess.PIPE)

    def check(self, value):
        check_api.check_history(value, self.baseline)

    def test_unchanged_inventory_is_accepted(self):
        self.check(self.previous)

    def test_rewriting_or_deleting_a_snapshot_is_rejected(self):
        self.snapshot.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.check(self.previous)
        self.snapshot.unlink()
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.check(self.previous)

    def test_description_change_requires_a_version_increment(self):
        current = deepcopy(self.previous)
        current["date"] = "2026-10-20"
        with self.assertRaisesRegex(ValueError, "new release version"):
            self.check(current)
        current["version"] = "1.0.1"
        self.check(current)

    def test_new_member_requires_minor_release(self):
        current = deepcopy(self.previous)
        current["version"] = "1.0.1"
        current["members"].append({**current["members"][0], "path": "data.patch"})
        with self.assertRaisesRegex(ValueError, "minor release"):
            self.check(current)
        current["version"] = "1.1.0"
        self.check(current)

    def test_changed_signature_grants_contexts_and_rpc_require_major(self):
        for field, value in (("declaration", "get(id: string): Promise<Json>"), ("capabilities", ["STORAGE"]), ("contexts", ["ACTION"]), ("rpc", "data.other")):
            with self.subTest(field=field):
                current = deepcopy(self.previous)
                current["version"] = "1.1.0"
                current["members"][0][field] = value
                with self.assertRaisesRegex(ValueError, "major release"):
                    self.check(current)
                current["version"] = "2.0.0"
                self.check(current)

    def test_removed_member_requires_major_release(self):
        current = deepcopy(self.previous)
        current.update(version="1.1.0", members=[])
        with self.assertRaisesRegex(ValueError, "major release"):
            self.check(current)


if __name__ == "__main__":
    unittest.main()
