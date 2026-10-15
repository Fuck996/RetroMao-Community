"""Bundle the two independent sync examples with their shared source assets."""

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from build_script_plugin import build

ROOT = Path(__file__).resolve().parents[1]


def build_examples(output, release_tag):
    shared = ROOT / "examples/activity-sync-shared"
    output.mkdir(parents=True, exist_ok=True)
    entries = []
    for name in ("favorites-sync", "recent-sync"):
        with tempfile.TemporaryDirectory(prefix="retromao-sync-", dir=output) as directory:
            source = Path(directory)
            shutil.copytree(shared, source, dirs_exist_ok=True)
            shutil.copytree(ROOT / "examples" / name, source, dirs_exist_ok=True)
            scripts = [source / file for file in ("mode.js", "strings.js", "sync.js")]
            worker = "\n".join(file.read_text(encoding="utf-8") for file in scripts)
            worker += '\nretromao.define({actions:{sync: () => activitySync.run(activitySyncKind)}});\n'
            (source / "main.js").write_text(worker, encoding="utf-8")
            (source / "sync.js").unlink()
            entries.append(build(source, output, release_tag))
    return entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()
    print(json.dumps(build_examples(args.output, args.release_tag), ensure_ascii=False, indent=2))
