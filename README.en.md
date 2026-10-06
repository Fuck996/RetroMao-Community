# RetroMao Community

[中文](README.md) · **English** · [日本語](README.ja.md)

This public repository distributes platform and theme extension packs for RetroMao. Packs contain configuration and redistributable artwork; installing one does not upload your ROMs, saves, or WebDAV credentials. Online installation requires **RetroMao 0.9.44 or later** and access to GitHub. Existing games and installed packs remain usable offline.

## Download and install in RetroMao

### Add a platform

1. Open **Settings (设置) → Game Library & Folders (游戏库与文件夹) → Community Platforms (社区平台)**. Review the pack name, author, and description.
2. Select **Download and Install (下载并安装)** and wait for the download, size and SHA-256 checks, and installation. An installed platform can be reinstalled from the same list to update it.
3. Back in **Game Library & Folders (游戏库与文件夹)**, add the local ROM folder for that platform. The pack contains neither games nor an emulator; configure an emulator already installed on your device to launch games.

The new platform uses RetroMao's existing platform selector, folder scan, and library workflow. Installation does not scan the whole device or upload ROMs. WebDAV resource sync still requires the normal per-platform sync-directory setup.

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

The catalog is a manifest; the Release ZIP is the installed payload, while the preview is only an image. ROMs, saves, and WebDAV data do not pass through this repository. Packs do not execute scripts or native code. See the [pack specification](EXTENSIONS.md) for the format and limits.

## Create and contribute

- Put `platform.json` at the root of a platform ZIP, optionally with icons. Put `theme.json` at the root of a theme ZIP and provide a 1280×720 PNG/WebP preview for online themes.
- Start with [`examples/`](examples/) and the [pack specification](EXTENSIONS.md). Test local import and the 16:9, 4:3, and 1:1 layouts, touch, and controller navigation. State the author and redistribution license. Do not include ROMs, firmware, saves, secrets, or account data.
- Submit source configuration, artwork, and preview in a PR. After review, maintainers publish the ZIP as a Release asset and record that **published asset's** byte count and SHA-256 in `catalog.json`. Only then will the online list offer the version.

Run `python tools/build_examples.py` to rebuild the examples into `dist/`; it does not publish a Release. The [example Release](https://github.com/Fuck996/RetroMao-Community/releases/tag/packs-2026-10-06) also has notes in Chinese, English, and Japanese.

A platform pack defines identity, ROM extensions, medium, cover ratio, and icons; it does not provide an emulator or save directory. A theme changes declared visual assets without replacing RetroMao's renderer.
