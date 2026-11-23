# Nintendo Switch 2 · Banana Native

[中文](#中文) · [English](#english) · [日本語](#日本語) · [素材 / Credits / 素材出典](licenses/CREDITS.md)

## 中文

**安装。** 在 RetroMao 1.2.5 或更新版打开「设置 → 游戏库与文件夹 → 社区平台」，选择 Nintendo Switch 2。离线可在同页导入 `platform-switch2-1.0.4.zip`。安装 Banana Native，按其官方说明授予所需的文件访问权限。

**游戏。** 把自备的可启动 `.nup` 放在内置存储或 TF 卡的 `roms/switch2`，在复古猫关联目录。列表按目录和扩展名入库，具体 Title ID、版本和可用性由 Banana Native 确认。如需检查包类型，可在同一版本的 Banana Native 源码目录运行 `python3 dm/tools/nup.py "游戏.nup" packages`。只把能独立启动的入口文件放入 ROM 目录。先在 Banana Native 为对应游戏执行 Prepare，再从复古猫启动。通过 Banana Native 的「停止游戏」返回。

**存档。** 在 Banana Native 的游戏设置中打开「Folders → Save folder」。为每款游戏选择共享存储中的 `Documents/BananaNative/Saves/<Title ID>`，用「复制并使用」迁移现有存档。默认目录通常在 `Android/data/dev.bananative.android/files/saves/<Title ID>`，设备共享存档可能是同级的 `<Title ID>_device`，以该游戏的实际设置为准。回到复古猫「存档同步 → 新增同步」，选择 Nintendo Switch 2、Banana Native 和普通存档类型的「自定义目录」，授权共同父目录 `Documents/BananaNative/Saves`。选择自己的同步来源和目标目录，在关闭游戏后同步。多台设备使用相同的相对子目录。自定义绑定执行整目录同步，`packs`、ROM 和 `save-backups` 请放在目录外。

**显示。** 包含主题色平台 Logo、彩色像素机种图、日版红色包装盒与游戏卡模型。游戏自备素材按已有媒体角色关联。公开扩展只提供机种资源、声明式启动和配置说明。

[Banana Native 安装](https://git.eden-emu.dev/moceure/BananaNative/wiki/Installation) · [兼容列表](https://git.eden-emu.dev/moceure/BananaNative/wiki/Games) · [存档说明](https://git.eden-emu.dev/moceure/BananaNative/wiki/Saves-and-Storage)

## English

**Install.** In RetroMao 1.2.5 or later, open Settings → Game library and folders → Community platforms and select Nintendo Switch 2. For offline installation, import `platform-switch2-1.0.4.zip` from the same settings page. Install Banana Native and grant it the file access described in its installation instructions.

**Games.** Place your bootable `.nup` files in `roms/switch2` on internal storage or a TF card and add the folder to RetroMao. The library scans the folder and extension. Banana Native identifies the title ID and version. To inspect a package against a matching checkout, run `python3 dm/tools/nup.py "game.nup" packages` from the Banana Native source tree. Keep only standalone boot entries in the ROM folder. Run Prepare for the game in Banana Native before launching it from RetroMao. Use Stop Game in Banana Native to return.

**Saves.** Open Folders → Save folder in the game's Banana Native settings. Set a shared folder such as `Documents/BananaNative/Saves/<Title ID>` for each game and choose Copy and use to migrate existing files. The usual default is `Android/data/dev.bananative.android/files/saves/<Title ID>`. A sibling `<Title ID>_device` may hold device-shared saves. Check the game's actual settings. In RetroMao, open Save sync → Add sync, choose Nintendo Switch 2 and Banana Native, add a custom folder for regular saves, and grant access to the shared `Documents/BananaNative/Saves` parent. Choose your sync provider and destination and close the game before syncing. Keep the same relative folders across devices. The binding syncs the entire selected folder. Keep ROMs, `packs` and `save-backups` outside it.

**Presentation.** Includes a theme-tinted logo, a color pixel icon, a red Japanese-style case and a game card model. Use the existing media roles to associate your own artwork. The extension contains platform assets, a declarative launcher and setup instructions.

[Banana Native installation](https://git.eden-emu.dev/moceure/BananaNative/wiki/Installation) · [Compatibility](https://git.eden-emu.dev/moceure/BananaNative/wiki/Games) · [Saves and storage](https://git.eden-emu.dev/moceure/BananaNative/wiki/Saves-and-Storage)

## 日本語

**導入。** RetroMao 1.2.5 以降で「設定 → ゲームライブラリとフォルダー → コミュニティの機種」を開き、Nintendo Switch 2 を選びます。オフラインでは同じ設定画面から `platform-switch2-1.0.4.zip` を読み込めます。Banana Native をインストールし、公式手順に従ってファイルアクセスを許可します。

**ゲーム。** 用意した起動可能な `.nup` を内部ストレージまたは microSD カードの `roms/switch2` に置き、RetroMao でそのフォルダーを登録します。ライブラリはフォルダーと拡張子で検出し、タイトル ID とバージョンは Banana Native が判定します。パッケージを確認するには、対応する Banana Native のソースディレクトリで `python3 dm/tools/nup.py "game.nup" packages` を実行します。ROM フォルダーには単体で起動できるエントリーを置いてください。各ゲームを Banana Native で Prepare してから、RetroMao で起動します。「ゲームを停止」で戻ります。

**セーブ。** Banana Native のゲーム設定から「Folders → Save folder」を開きます。ゲームごとに `Documents/BananaNative/Saves/<Title ID>` などの共有フォルダーを選び、既存ファイルを移す場合は「コピーして使用」を選びます。通常の既定先は `Android/data/dev.bananative.android/files/saves/<Title ID>` で、端末共有セーブは同階層の `<Title ID>_device` にある場合があります。各ゲームの実際の設定を確認してください。RetroMao の「セーブ同期 → 同期を追加」で Nintendo Switch 2 と Banana Native を選び、通常セーブ用のカスタムフォルダーとして共通の親フォルダー `Documents/BananaNative/Saves` を許可します。自分の同期サービスと保存先を選び、ゲームを終了してから同期します。各端末で相対パスを揃え、ROM、`packs`、`save-backups` は同期フォルダーの外に置きます。

**表示。** テーマ色に連動するロゴ、カラーのピクセルアイコン、日本向けの赤いパッケージとゲームカードのモデルを収録しています。既存のメディア項目で手持ちの画像を関連付けられます。公開拡張には機種素材、起動定義、設定手順が含まれます。

[Banana Native の導入](https://git.eden-emu.dev/moceure/BananaNative/wiki/Installation) · [動作対応](https://git.eden-emu.dev/moceure/BananaNative/wiki/Games) · [セーブとストレージ](https://git.eden-emu.dev/moceure/BananaNative/wiki/Saves-and-Storage)
