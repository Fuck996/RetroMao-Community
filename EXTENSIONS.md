# 扩展包契约 / Extension contracts / 拡張パック契約

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Platform schema](schemas/platform.schema.json) · [Template](templates/platform/platform.json) · [Publication](docs/PUBLISHING.md)

```text
python tools/retromao.py init platform --id demo-msx --name DemoMSX --author YourName
python tools/retromao.py check extensions/demo-msx
python tools/retromao.py preview extensions/demo-msx
python tools/retromao.py pack extensions/demo-msx --release-tag demo-msx-1.0.0
```

[Android URI permissions and package visibility](https://developer.android.com/training/package-visibility/use-cases) · [RetroArch Android source](https://github.com/libretro/RetroArch/tree/master/pkg/android)

## 中文

平台从 templates/platform 开始。格式 1 兼容既有数据包；格式 2 增加 launchers，需要 0.9.108 或含此能力的宿主源码构建。正式发行与设备验收状态见 contracts/host.json，不把版本门槛当作已完成验收。包根放 platform.json，图标可选。retromao-package.json 是开发和发布元数据，不打入 ZIP。

platform.id 为 2–32 位小写字母、数字、下划线或连字符。name 与 aliases 不能和内置或已安装平台重复；extensions 不带点、1–12 位小写字母数字，可与其他平台重叠，但重叠扩展名不能独自识别机种。manufacturer 非空且不超过 80 字符，releaseYear 为 1970–2100。coverAspectRatio 是宽／高，范围 0.5–2。medium 允许 CARTRIDGE、GAME_CARD、HUCARD、DISC、UMD、DISK_CARD；不提供模型时仍保留封面与占位图。内置 ID、名称、别名在 contracts/host.json。

assets 只允许 logo、pixel，引用包内 PNG/WebP；每个最多 8 MiB、1–2048 像素。路径必须相对，不得包含空段、点段、反斜线、冒号、NUL、符号链接或越出包目录。平台包最多 128 个文件、解压后 64 MiB，清单最多 1 MiB。

launchers 最多 16 项，ID 在平台内唯一、1–40 位，以小写字母起始；宿主保存的 profile ID 为 community.<平台ID>.<启动ID>，更新后不可随意改名。packageName 必须是真实 Android 包名，activity 必须是完整类名，不能写相对类名。name 非空且不超过 80 字符。平台启动仍走原模拟器设置、ROM 实际读取、SAF 授权、启动文件选择和返回流程，不另外扫描或复制 ROM。

URI 使用 ACTION_VIEW、只读 content URI 和 ClipData；mimeType 可选，使用明确的 MIME 字符串。模拟器应通过 ACTION_VIEW/content 的 intent filter 可见，且目标 Activity 已导出并支持传入 URI。RETROARCH 使用现有官方启动参数和核心路径规则，必须提供 1–64 个 cores，不能提供 mimeType。核心 ID 是去掉 _libretro_android.so 后的文件名，核心名称非空；不会安装或下载核心。旧版 RetroArch 的本机路径约束仍适用，同平台声明的核心进入原共享核心列表。

不得把专有的 intent extras、任意 shell、JS 或未知协议塞进平台包。需要新协议时应先扩展宿主正式契约。平台安装后继续使用原扫描、库、网盘映射和资源任务；它不提供模拟器、ROM、固件或存档规则。平台暂无卸载入口；同 ID 更新保留游戏关联，改 ID 视为新平台。

主题继续使用根目录 theme.json，格式 3 可引用 model.<平台ID>.packaging 和 model.<平台ID>.gameMedia，GLB 2.0 每个最多 32 MiB，沿用原渲染和贴图管线。扩展平台素材要求先安装平台。主题在线预览为 1280×720 PNG/WebP，路径在 previews 下；须另验收 4:3、1:1。旧 build_examples 仅重建已提交示例，输出目录条目到 dist，不重写在线 catalog。通用平台打包使用统一 CLI。

catalog.json 格式为 schemaVersion:1 与 entries。每项声明 kind、id、name、author、description、version、minAppVersion、releaseTag、fileName、sizeBytes、sha256；主题必须有 previewPath。实际 ZIP 必须先在来源仓库 Release 发布并回读校验，之后才能更新目录。插件使用 plugins/index.json，语言使用 languages/index.json，格式不可混用。

## English

Start platforms from templates/platform. Format 1 remains compatible; format 2 adds launchers and requires 0.9.108 or a host source build containing the feature. Check contracts/host.json for formal-release and device acceptance; a version threshold is not acceptance evidence. Put platform.json at the ZIP root. Icons are optional. retromao-package.json is authoring/release metadata and is excluded from the ZIP.

platform.id uses 2–32 lowercase letters, digits, underscores or hyphens. name/aliases must not collide with built-in or installed platforms. extensions have no dot and use 1–12 lowercase alphanumeric characters. Overlap is allowed but cannot alone identify a platform. manufacturer is nonempty with at most 80 characters; releaseYear is 1970–2100. coverAspectRatio is width/height, between 0.5 and 2. medium accepts CARTRIDGE, GAME_CARD, HUCARD, DISC, UMD and DISK_CARD. Covers/placeholders remain available without a model. Built-in identities are in contracts/host.json.

assets only accepts logo/pixel pointing to package PNG/WebP files, each at most 8 MiB and 1–2048 pixels per dimension. Paths must be relative and cannot contain empty/dot segments, backslashes, colons, NUL, symlinks or escapes. A platform ZIP has at most 128 files, 64 MiB expanded data and a 1 MiB manifest.

launchers has at most 16 entries. IDs are unique within a platform, 1–40 characters, starting with a lowercase letter. The saved host profile ID is community.<platformID>.<launcherID>; do not casually rename it on updates. packageName must be a real Android package, activity a full class name, and name nonempty with at most 80 characters. Launching uses the existing settings, current ROM reads, SAF permissions, entry selection and return flow, without a separate ROM scan/copy.

URI uses ACTION_VIEW, read-only content URI access and ClipData. An explicit mimeType is optional. The emulator must be discoverable through an ACTION_VIEW/content intent filter, and the exported target Activity must accept the URI. RETROARCH uses existing official launch arguments and core-path rules, requires 1–64 cores, and forbids mimeType. A core ID is its filename without _libretro_android.so; names are nonempty. Packs never install/download cores. Existing native-path constraints for old RetroArch versions remain; cores declared for the same platform join the shared core list.

Do not embed proprietary intent extras, shell commands, JS or unknown protocols in platform packs. A new protocol first requires a formal host contract. Installed platforms use existing scanning, library, cloud mappings and resource tasks. They include no emulator, ROM, firmware or save rules. There is currently no platform uninstall entry. Same-ID updates retain game associations; a changed ID is a new platform.

Themes still use root theme.json. Format 3 can reference model.<platformID>.packaging and model.<platformID>.gameMedia, with GLB 2.0 files up to 32 MiB, using the existing renderer and texture pipeline. Install extension platforms before referencing their assets. Online theme previews are 1280×720 PNG/WebP under previews; also test 4:3 and 1:1. Legacy build_examples only rebuilds committed examples and writes catalog entries under dist, without replacing the live catalog. Use the unified CLI for platform packages.

catalog.json contains schemaVersion:1 and entries. Each entry declares kind, id, name, author, description, version, minAppVersion, releaseTag, fileName, sizeBytes and sha256; themes require previewPath. Publish and download-verify the actual ZIP in the source repository before updating the catalog. Scripts use plugins/index.json; languages use languages/index.json. Do not mix formats.

## 日本語

プラットフォームは templates/platform から作成します。既存の形式 1 は引き続き対応し、形式 2 は launchers を追加します。0.9.108 または本機能を含むホストビルドが必要です。正式公開と実機検証の状況は contracts/host.json を確認してください。最低バージョンは検証完了の証拠ではありません。ZIP のルートに platform.json を置きます。アイコンは任意です。retromao-package.json は開発と公開用の情報で、ZIP には含めません。

platform.id は小文字英数字、アンダースコア、ハイフンの 2～32 文字です。name と aliases は内蔵またはインストール済みの定義と重複できません。extensions はドットを付けず、小文字英数字の 1～12 文字です。重複は可能ですが、それだけで機種を自動判定できません。manufacturer は空でない 80 文字以内、releaseYear は 1970～2100 です。coverAspectRatio は幅／高さで 0.5～2。medium は CARTRIDGE、GAME_CARD、HUCARD、DISC、UMD、DISK_CARD です。モデルがなくても表紙とプレースホルダーを表示します。内蔵の識別情報は contracts/host.json にあります。

assets は logo と pixel のみで、パック内の PNG/WebP を参照します。各ファイルは 8 MiB 以下、各辺 1～2048 ピクセルです。相対パスを使い、空の要素、ドット要素、バックスラッシュ、コロン、NUL、シンボリックリンク、ディレクトリ外への参照を禁止します。最大 128 ファイル、展開後 64 MiB、マニフェストは 1 MiB までです。

launchers は最大 16 項目です。ID は機種内で一意な 1～40 文字で、小文字から始めます。保存される profile ID は community.<platformID>.<launcherID> です。更新時に不用意に変更しないでください。packageName は実際の Android パッケージ名、activity は完全なクラス名、name は空でない 80 文字以内です。起動は既存の設定、現在の ROM の読み取り、SAF 権限、起動ファイル選択、復帰処理を使用し、別のスキャンや ROM コピーは行いません。

URI は ACTION_VIEW、読み取り専用の content URI 権限、ClipData を使用します。明示的な mimeType は任意です。エミュレーターは ACTION_VIEW/content の intent filter から検出可能で、公開された Activity が URI に対応している必要があります。RETROARCH は既存の公式起動引数とコアのパス規則を使用し、1～64 個の cores が必要です。mimeType は使用できません。コア ID はファイル名から _libretro_android.so を除いた部分で、名称は空にできません。パックはコアをインストールしません。旧 RetroArch の実パス制約は維持され、同じ機種のコアは既存の共有一覧に統合されます。

独自 intent extras、シェル、JS、未知のプロトコルをパックに入れないでください。新しいプロトコルには先にホスト契約の拡張が必要です。インストール後も既存のスキャン、ライブラリ、クラウドマッピング、リソースタスクを使います。エミュレーター、ROM、ファームウェア、セーブ規則は含まれません。現在アンインストール機能はありません。同じ ID の更新はゲームとの関連を維持し、別 ID は新しい機種として扱います。

テーマは引き続きルートの theme.json を使用します。形式 3 は model.<platformID>.packaging と model.<platformID>.gameMedia を参照でき、GLB 2.0 は各 32 MiB 以下です。既存の描画とテクスチャ処理を使います。拡張機種の素材を使う場合は先にその機種をインストールしてください。オンラインのプレビューは previews 内の 1280×720 PNG/WebP とし、4:3 と 1:1 も確認します。旧 build_examples は既存のサンプルを再作成し、索引を dist に出力するだけで、公開カタログを置き換えません。プラットフォームの作成には統一 CLI を使います。

catalog.json は schemaVersion:1 と entries で構成します。各項目に kind、id、name、author、description、version、minAppVersion、releaseTag、fileName、sizeBytes、sha256 を指定し、テーマには previewPath も必要です。公開元の Release に ZIP を公開して再取得・検証した後に索引を更新します。スクリプトは plugins/index.json、言語は languages/index.json を使用し、形式を混在させないでください。
