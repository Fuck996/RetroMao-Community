# RetroMao Community

[中文](README.md) · **English** · [日本語](README.ja.md)

This repository maintains language, platform, and theme extensions for RetroMao. Extensions contain translations, configuration, and redistributable artwork; installing one does not upload your ROMs, saves, or cloud credentials. Online platform/theme installation supports **0.9.44 and later**, built-in languages and language downloads start with **0.9.87**, and multiple repositories are supported from **0.9.88**. Online downloads require access to GitHub. Existing games and installed extensions remain usable offline.

The current packaged app version is **0.9.97**; see the [changelog (Chinese)](CHANGELOG.md). It includes the script plugin framework, version management, plugin localization and shared icons, and reuses the shared content APIs, synchronization workflows and provider configuration. Script-based storage-provider integration has not been released; see the [storage-provider guide (Chinese)](SYNC_PROVIDERS.md) for the current boundaries.

## Add official and community repositories

1. On the **Settings home screen**, select the icon-only floating repository button in the bottom-right corner.
2. Enter one public GitHub repository URL per line, for example `https://github.com/Fuck996/RetroMao-Community`. Community authors can fork this repository, maintain their own translations and extensions, and share their repository URL with players.
3. Save the list. Languages, community themes, and community platforms share it. Keep a separate line for each official or community source you want to use; an empty list makes no repository requests.
4. Open the relevant download page and select an extension. Entries with the same identity and content are merged while retaining their sources; different content is listed separately rather than silently replaced by name. The language download dialog lists languages; repository URLs are configured here instead.

Repository settings discover extensions; they are separate from cloud connections used for save synchronization. Authors and source repositories are displayed separately. Fork maintainers should preserve original author credits and artwork licenses.

## Download and install in RetroMao

### Add a platform

1. Open **Settings (设置) → Game Library & Folders (游戏库与文件夹) → Community Platforms (社区平台)**. Review the pack name, author, and description.
2. Select **Download and Install (下载并安装)** and wait for the download, size and SHA-256 checks, and installation. An installed platform can be reinstalled from the same list to update it.
3. Back in **Game Library & Folders (游戏库与文件夹)**, add the local ROM folder for that platform. The pack contains neither games nor an emulator; configure an emulator already installed on your device to launch games.

The new platform uses RetroMao's existing platform selector, folder scan, and library workflow. Installation does not scan the whole device or upload ROMs. Cloud resource sync still requires the normal per-platform cloud source and directory setup.

### Install a theme

1. Open **Settings (设置) → Theme & Display (主题与显示) → Community Themes (社区主题)** and inspect the 1280×720 preview, author, and description.
2. Select **Download and Install (下载并安装)**. The theme then appears under **Installed Themes (已安装主题)**; installation does not switch your active theme.
3. Select it, choose **Preview Theme (预览主题)** to inspect the actual interface, then choose **Apply Theme (应用主题)**. Install a referenced extension platform before importing a theme that uses it.

A theme may include colors, backgrounds, motion, platform icons, fonts, and packaging/media GLB models. Each pack declares its own assets. Models continue to use RetroMao's existing rendering, materials, and animation pipeline.

### Manual ZIP installation

If online access is unavailable, open the [official example Release](https://github.com/Fuck996/RetroMao-Community/releases/tag/packs-2026-10-06) and download the desired `.zip` from **Assets**. **Do not extract it.** Copy it to your device and select **Import Platform Extension Pack (导入平台扩展包)** under **Game Library & Folders (游戏库与文件夹)**, or **Import Theme Pack (导入主题包)** under **Theme & Display (主题与显示)**. Manual import uses the same package validation and installer, and does not require GitHub access.

If the online catalog cannot be fetched, the app may show its last successfully fetched catalog. A cached listing does not mean a pack has been downloaded or installed. Reopen the page when the network is available, or use manual ZIP import.

## How online downloads work

1. The app reads the public [`catalog.json`](catalog.json). Each entry specifies the pack kind, version, minimum app version, Release tag, asset filename, exact size in bytes, and SHA-256. Theme entries also specify a preview image.
2. The app displays those entries and previews. On request, it downloads the ZIP from the specified **GitHub Release asset**, without requiring a GitHub account.
3. It verifies the exact byte count and SHA-256 before installation. A mismatch is rejected and cannot replace an installed pack.
4. The verified ZIP enters the same installer as manual import. The installer validates the manifest, ZIP paths, image dimensions, and size limits, then stores the pack in the app's extension directory for subsequent launches.

The catalog is a manifest; the Release ZIP is the installed payload, while the preview is only an image. ROMs, saves, and WebDAV data do not pass through this repository. Theme, platform and language packs do not execute code. See the [pack specification](EXTENSIONS.md) for the format and limits.

## Create and contribute

The script plugin framework provides an [SDK](sdk/README.md), a [library notes example](examples/library-notes/), and Installed and Store tabs in the main menu. It reuses the existing repository settings and downloads. Script discovery uses `plugins/index.json`. [Favorites Sync and Recent Games Sync 1.0.4](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.4) are published and require 0.9.96. Native execution and synchronization with actual cloud storage still require device validation. See the [version and shared icon guide (Chinese)](sdk/PLUGIN_VERSIONS.md) for update rules.

- Put `platform.json` at the root of a platform ZIP, optionally with icons. Put `theme.json` at the root of a theme ZIP and provide a 1280×720 PNG/WebP preview for online themes.
- Start with [`examples/`](examples/) and the [pack specification](EXTENSIONS.md). Test local import and the 16:9, 4:3, and 1:1 layouts, touch, and controller navigation. State the author and redistribution license. Do not include ROMs, firmware, saves, secrets, or account data.
- Submit source configuration, artwork, and preview in a PR. After review, maintainers publish the ZIP as a Release asset and record that **published asset's** byte count and SHA-256 in `catalog.json`. Only then will the online list offer the version.

Run `python tools/build_examples.py` to rebuild the examples into `dist/`; it does not publish a Release. The [example Release](https://github.com/Fuck996/RetroMao-Community/releases/tag/packs-2026-10-06) also has notes in Chinese, English, and Japanese.

A platform pack defines identity, ROM extensions, medium, cover ratio, and icons; it does not provide an emulator or save directory. A theme changes declared visual assets without replacing RetroMao's renderer.

## Language files and community translation

Each language is maintained in one JSON file. Contributions and new languages are welcome; see [languages/](languages/README.md) for files, contribution rules, and downloads. The current catalog contains **1233 messages**. Simplified Chinese keeps `source` status; English, Traditional Chinese, and Japanese are complete and remain `draft` for review.

The APK includes Simplified Chinese, Traditional Chinese, English, and Japanese. It initially matches the system language and uses Simplified Chinese if none matches. Under **Settings → Theme and display → Language**, choose a language or follow the system. **Download languages** lists extensions from the repositories configured above. Online installation accepts only complete `reviewed` packs matching the APK's message catalog, not drafts. Language files use their own installation flow, not the platform or theme importer.
