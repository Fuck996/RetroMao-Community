# RetroMao Community

[中文](README.md) · **English** · [日本語](README.ja.md)

This standalone repository supports extension development and distribution. You do not need the host source to build plugins, translations or platform packs. Use Python 3.11+; plugin and browser tests also need Node.js 22+. Create and activate a Python virtual environment first if possible. Run every command from this repository root.

Start your first plugin after forking: install pinned dependencies, check the repository, generate a template, preview and package it.

```text
python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-dev.txt
npm ci --registry=https://registry.npmmirror.com
python tools/retromao.py check
python tools/retromao.py init plugin --id demo-plugin --name Demo --author YourName
python tools/retromao.py check extensions/demo-plugin
python tools/retromao.py preview extensions/demo-plugin
python tools/retromao.py pack extensions/demo-plugin --release-tag demo-plugin-1.0.0
```

The terminal prints the preview URL; Ctrl+C stops the server. Preview runs the shipped SDK and your code against local fixtures without real cloud access. Continue with [development and acceptance](docs/TESTING.md), [contribution rules](CONTRIBUTING.md) and [publishing](docs/PUBLISHING.md). AI assistants should read [AGENTS.md](AGENTS.md) first.

| Task | Start here | Distribution |
| --- | --- | --- |
| Script plugin | [SDK](sdk/README.md), [API reference](sdk/API_REFERENCE.md), templates/plugin | ZIP + plugins/index.json |
| Add a language | [Language guide](languages/README.md) | One-language JSON + languages/index.json |
| Add a platform | [Platform contract](EXTENSIONS.md), templates/platform | ZIP + catalog.json |

Find all contracts in the [public interface map](docs/INTERFACES.md), with a [machine inventory](sdk/api.json), [API version policy](sdk/API_VERSIONING.md) and [API changelog](sdk/API_CHANGELOG.md).

Declarative platform launchers use format 2 and need a host build containing that feature, with a minimum version of 0.9.108. Check the [capability contract](contracts/host.json) and release evidence for formal APK acceptance. Format 1 has no launchers. Script support starts at 0.9.90, localized metadata at 0.9.94, dedicated configuration pages at 0.9.96, and ROM resource providers at 0.9.98. New proprietary emulator protocols and script storage-provider registration still need host support; data packs cannot execute code.

Use [languages/index.json](languages/index.json) for the language baseline, counts and hashes. Do not infer the baseline from an APK version. A reviewed status is not required; completeness and compatibility control installation. [Message context](contracts/message-context.json) provides known surfaces and arguments. Edit the target language without changing the Chinese baseline.

In the repository control at the bottom right of Settings, add one public GitHub repository per line. Plugins use Plugins → Store; platforms use Settings → Game Library & Folders → Community Platforms; languages use Settings → Theme & Display → Language → Download Languages. Import offline ZIPs at the corresponding entry. Forking does not copy upstream Release assets: publish your own assets before updating catalogs. Identical content is merged for display; users explicitly choose other sources.

Do not distribute ROMs, firmware, saves or account credentials. Preserve author credits and asset licenses; contributions require redistribution rights. Preview and automated tests do not replace Android, emulator or real-cloud acceptance. See the [changelog](CHANGELOG.md) and [release notes](RELEASE_NOTES.md) for published examples and history.
