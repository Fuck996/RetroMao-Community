# 公共接口导航 / Public interface map / 公開インターフェース一覧

[中文](#中文) · [English](#english) · [日本語](#日本語)

| Contract / 契约 / 契約 | Definition / 定义 / 定義 | Calls and validation / 调用与校验 / 利用と検査 |
| --- | --- | --- |
| Script API 1, contract 1.0.0 | [api.json](../sdk/api.json), [retromao.d.ts](../sdk/retromao.d.ts) | [API reference](../sdk/API_REFERENCE.md), [SDK](../sdk/README.md) |
| Plugin manifest schemaVersion 1 | [plugin.schema.json](../schemas/plugin.schema.json) | [Template](../templates/plugin/), [localization](../sdk/PLUGIN_LOCALIZATION.md) |
| Platform schemaVersion 1 / 2 | [platform.schema.json](../schemas/platform.schema.json), [host.json](../contracts/host.json) | [Platform and theme contract](../EXTENSIONS.md), [template](../templates/platform/) |
| Language schema_version 1 | [language.schema.json](../schemas/language.schema.json), [language index](../languages/index.json) | [Language guide](../languages/README.md), [message context](../contracts/message-context.json) |
| Release/catalog schemaVersion 1 | [package.schema.json](../schemas/package.schema.json), [catalog.schema.json](../schemas/catalog.schema.json) | [Publishing](PUBLISHING.md), [validation](VALIDATION.md) |
| Native storage provider integration | [Provider contract](../SYNC_PROVIDERS.md) | Host implementation required / 需宿主实现 / ホスト実装が必要 |

```text
python tools/retromao.py check
python tools/retromao.py check templates/plugin
python tools/retromao.py check templates/platform
python tools/retromao.py check languages/en.json
python tools/retromao.py preview templates/plugin
python tools/retromao.py pack templates/plugin --release-tag local-api-example
```

## 中文

脚本调用从 API reference 开始：32 个公开成员逐项列出调用签名、输入、默认值、输出、能力授权、运行上下文、边界和示例。完整嵌套数据结构在 retromao.d.ts，包括 Game/Metadata/Recent/Media/Asset、Query/Page/RecordPage、Edit、StorageSource、Task 与资源解析类型。先等待 ready；后台入口用 define 注册，页面用 tasks.run 发起工作，避免把传输消息当公共 API 直接发送。

调用顺序通常为 ready → settings/data → library 分页 → 后台批量编辑／存储 → tasks 状态／结果。配置页仅用白名单接口。API 的 NETWORK、STORAGE 与 ROM_RESOURCES 各有权限和范围，不能通过公共接口访问任意文件、系统凭据、宿主数据库或注册任意存储渠道。逐接口权限不包含示例的前置读取：示例先读后写时须同时声明读写权限。

平台、主题和语言是声明数据，不是可以发 RPC 的插件。平台 format 1 不含启动器，format 2 的 URI/RETROARCH 启动器由宿主既有启动流程消费，最低宿主 0.9.108，设备证据仍以 host.json 与发布验收记录为准。新模拟器协议需要宿主适配。语言由本地化加载器按 catalog_version/hash 核对；只修改目标语言，不能把 APK 版本当作语言基线。原生存储渠道契约供宿主贡献者使用，当前没有脚本注册渠道接口。

版本与变更分开记录：[API 版本规则](../sdk/API_VERSIONING.md)和 [API 变更说明](../sdk/API_CHANGELOG.md)管理 SDK；扩展自己的发行版遵守 [版本与图标](../sdk/PLUGIN_VERSIONS.md)及 Publishing；各数据格式保留自己的 schemaVersion，结构变化需同步 Schema、模板、校验器和三语迁移说明；语言基线以语言索引为唯一来源。产品历史仍在 [CHANGELOG](../CHANGELOG.md)，不能以增加 API 文档冒充产品新增功能。

上面的命令均在这个公共仓库根目录执行，不依赖宿主源码。preview 和自动示例使用明确样本，不连接真实服务；打包不自动发布。完成公开检查后，原生桥、设备目录、模拟器和真实服务按 Testing 单独验收，发布按 Publishing 先推源码再核对 Release 资产。

## English

Start script calls at API reference: all 32 public members document signatures, inputs, defaults, outputs, grants, contexts, limits and examples. retromao.d.ts defines complete nested models: Game/Metadata/Recent/Media/Asset, Query/Page/RecordPage, Edit, StorageSource, Task and resource types. Await ready, register background entry points with define, and start work from pages with tasks.run. Do not send transport messages as if they were the public API.

A typical sequence is ready → settings/data → paged library reads → background batch edits/storage → task status/results. Configuration pages only use the allowlist. NETWORK, STORAGE and ROM_RESOURCES have separate grants/scopes: no arbitrary files, system credentials, host database or script storage-provider registration. A member's grants do not include prerequisite reads in its example: read-then-write examples need both grants.

Platforms, themes and languages are declarative data, not RPC plugins. Platform format 1 has no launchers; format 2 URI/RETROARCH launchers enter the host's existing launch pipeline and require host 0.9.108. Consult host.json and release acceptance records for device evidence. New emulator protocols need host integration. Localization checks catalog_version/hash; edit only the target language and never infer its baseline from APK version. The native provider contract targets host contributors; scripts cannot currently register providers.

[API versioning](../sdk/API_VERSIONING.md) and [API changelog](../sdk/API_CHANGELOG.md) manage the SDK. Author extension releases follow [versions/icons](../sdk/PLUGIN_VERSIONS.md) and Publishing. Each data format keeps its own schemaVersion; structural changes update schemas, templates, validators and trilingual migration guidance. The language index alone defines its baseline. Product history remains in [CHANGELOG](../CHANGELOG.md); new API documentation is not a new product feature.

Run the commands above from this public repository root; host source is unnecessary. Preview and automated examples use explicit fixtures, never real services; packaging does not publish. After public checks, separately accept native bridges, device folders, emulators and real services through Testing, then follow Publishing to push source and verify Release assets.

## 日本語

スクリプトの呼び出しは API reference から始めます。公開 32 メンバーそれぞれにシグネチャ、入力、既定値、出力、権限、実行場所、制限、例があります。retromao.d.ts は Game/Metadata/Recent/Media/Asset、Query/Page/RecordPage、Edit、StorageSource、Task、リソース型の全項目を定義します。ready を待ち、define で入口を登録し、ページから tasks.run で実行します。転送メッセージを公開 API として直接送信しないでください。

一般的な順序は ready → settings/data → ライブラリのページ取得 → バックグラウンドの一括編集・保存 → タスク状態・結果です。設定ページは許可一覧だけを使います。NETWORK、STORAGE、ROM_RESOURCES は権限と範囲が異なり、任意のファイル、システム認証情報、ホスト DB、スクリプトによる保存先登録は利用できません。各メンバーの権限には例の事前読み取りを含めないため、読み取り後に書く例には両方の許可が必要です。

プラットフォーム、テーマ、言語は宣言データで、RPC プラグインではありません。形式 1 は起動設定を持たず、形式 2 の URI/RETROARCH は既存の起動経路を使い、ホスト 0.9.108 が必要です。実機の証拠は host.json とリリース検証記録を確認します。新しいエミュレータープロトコルはホスト対応が必要です。言語は catalog_version/hash で検査し、対象言語だけを編集します。APK 版から言語基準を推測しないでください。ネイティブ保存先契約はホストの開発者向けで、現在スクリプトから登録する API はありません。

SDK は [API 版管理](../sdk/API_VERSIONING.md)と [API 変更履歴](../sdk/API_CHANGELOG.md)で管理します。作者の拡張公開版は[版とアイコン](../sdk/PLUGIN_VERSIONS.md)と Publishing に従います。各データ形式は独立した schemaVersion を持ち、構造変更時は Schema、テンプレート、検査、三言語の移行説明を更新します。言語基準の正は言語索引だけです。製品の履歴は [CHANGELOG](../CHANGELOG.md) に残し、API 文書の追加を製品機能の追加と扱いません。

上のコマンドは公開リポジトリのルートで実行でき、ホストのソースは不要です。プレビューと自動実行例は明示したサンプルだけを使い、実サービスに接続しません。パッケージ化だけでは公開しません。公開検査の後に Testing でネイティブ接続、端末フォルダー、エミュレーター、実サービスを別途検証し、Publishing でソースの push と Release アセットの再確認を行います。
