# 插件卡片与文案 / Plugin cards and copy / プラグインカードと文言

[Manifest](../schemas/plugin.schema.json) · [Localization](PLUGIN_LOCALIZATION.md) · [Publishing](../docs/PUBLISHING.md)

## 中文

从复古猫 0.9.114 起，已安装列表与商店共用等高卡片。同一窗口、主题与字号下，空白、短文和长文的卡片大小一致；字号变化时统一调整。标题只显示一行，超出以省略号（…）表示，完整标题保留在可访问文本和详情中。描述区固定三行高度，可以在卡片内拖动或用滚轮纵向滚动，不显示滚动条，也不截去后半段。状态单行省略，版本、更新、配置和主要入口保留固定位置。

| 文案 | 简中、繁中、日文建议 | 英文建议 |
| --- | --- | --- |
| 插件标题 `name` | 不超过 16 字符 | 不超过 32 字符 |
| 卡片简介 `description` | 不超过 48 字符 | 不超过 96 字符 |

按各译文的 Unicode 码点计算，包含空格和标点，不按 UTF-8 字节数计算。这是文案建议，不是新增安装限制；现有公开 schema 上限保持不变（基础标题 80、简介 240）。卡宽、字体和更新按钮可能使建议长度也被省略，应把产品名与核心用途放在前面。不要用换行、空格或长文撑大卡片，不要手工给标题添加省略号。

标题只写产品与功能，简介只写一句核心用途。目录、配置步骤、排除项、排查和权限细节放在 README、配置页或完整说明中。各语言保持相同业务含义，检查 16:9、4:3、1:1 与放大字号下的省略、滚动和操作可达。修改清单或译文须递增插件版本，新建 Release，回读 ZIP 大小与摘要后发布一致的索引；不能只改商店文案而与包内清单不符。

Vita3K 保留标题“Vita3K ROM 同步”，简介为“同步 Vita3K 游戏本体、补丁、DLC 和许可。”。选择目录及不包含存档、固件、缓存等边界保留在 README。前端复用 Compose [有边界滚动](https://developer.android.com/develop/ui/compose/touch-input/scroll/scroll-modifiers)与[嵌套滚动](https://developer.android.com/develop/ui/compose/touch-input/scroll/nested-scroll-modifiers)，不新增滚动条或平行滚动实现。

## English

From RetroMao 0.9.114, installed plugins and the store share equal-height cards. Empty, short and long copy use identical geometry within the same window, theme and font scale; larger text adjusts all cards together. Titles use one line with an ellipsis (…), retaining full accessible/detail text. Descriptions have a fixed three-line viewport with vertical drag/wheel scrolling, no scrollbar and no discarded tail. Status uses one-line ellipsis; version, update, configuration and primary actions keep their positions.

| Field | Simplified/traditional Chinese and Japanese | English |
| --- | --- | --- |
| Title `name` | Up to 16 characters recommended | Up to 32 characters recommended |
| Summary `description` | Up to 48 characters recommended | Up to 96 characters recommended |

Count Unicode code points per translation, including spaces/punctuation, not UTF-8 bytes. These are editorial recommendations, not new installation limits. Existing public schema limits remain unchanged (base title 80, summary 240). Width, fonts and update controls can truncate even recommended lengths. Put identity and purpose first; do not enlarge cards with line breaks/padding or manually append title ellipsis.

Use a product/function title and one sentence for the core purpose. Put directories, setup, exclusions, troubleshooting and permission details in README/configuration/full documentation. Keep language meanings aligned. Verify ellipsis, scrolling and reachable actions at 16:9, 4:3, 1:1 and larger text. Manifest/translation edits require a higher plugin version and a new Release; verify downloaded ZIP size/hash before publishing the matching index. Never change catalog copy alone when it would disagree with the package.

Vita3K keeps “Vita3K ROM sync” and uses “Sync Vita3K games, updates, DLC and licenses.” Directory setup and save/firmware/cache exclusions stay in README. The host reuses Compose [bounded scrolling](https://developer.android.com/develop/ui/compose/touch-input/scroll/scroll-modifiers) and [nested scrolling](https://developer.android.com/develop/ui/compose/touch-input/scroll/nested-scroll-modifiers), without a parallel scroll implementation or scrollbar.

## 日本語

RetroMao 0.9.114 以降、インストール済み一覧とストアは同じ高さのカードを使います。同じ画面・テーマ・文字倍率では、説明が空・短文・長文でも大きさは変わらず、文字拡大時は全カードを一緒に調整します。タイトルは一行で超過部分を省略記号（…）にし、読み上げと詳細には全文を保持します。説明は三行分の高さに固定し、カード内で縦にドラッグ・ホイール操作でき、スクロールバーは表示せず末尾も削りません。状態は一行で省略し、版・更新・設定・主操作の位置を保持します。

| 項目 | 簡体字・繁体字中国語、日本語 | 英語 |
| --- | --- | --- |
| タイトル `name` | 16 文字以内を推奨 | 32 文字以内を推奨 |
| 説明 `description` | 48 文字以内を推奨 | 96 文字以内を推奨 |

言語ごとに空白・記号を含む Unicode コードポイントで数え、UTF-8 のバイト数は使いません。推奨値であり、新しいインストール制限ではありません。公開 schema の既存上限（基本タイトル 80、説明 240）を維持します。幅、字体、更新ボタンによっては推奨値でも省略されるため、製品名と用途を先に置きます。改行・空白でカードを広げたり、タイトルに省略記号を手で追加したりしないでください。

タイトルは製品と機能、説明は主な用途の一文にし、ディレクトリ、設定、除外対象、障害対応、権限の詳細は README や設定画面に記載します。各言語の意味を合わせ、三つの比率と拡大文字で省略・スクロール・操作を確認してください。マニフェストや訳の変更では版を上げて新規公開し、取得した ZIP のサイズ・摘要を確認してから一致する索引を公開します。包内の内容と食い違うストア文言だけの変更は禁止です。

Vita3K のタイトルは「Vita3K ROM 同期」、説明は「Vita3K のゲーム本体・更新・DLC・ライセンスを同期。」です。ディレクトリとセーブ・ファームウェア・キャッシュの除外は README に保持します。前端は Compose の[境界付きスクロール](https://developer.android.com/develop/ui/compose/touch-input/scroll/scroll-modifiers)と[入れ子スクロール](https://developer.android.com/develop/ui/compose/touch-input/scroll/nested-scroll-modifiers)を再利用し、独自経路やスクロールバーは追加しません。
