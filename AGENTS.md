# Developer and AI instructions / 开发规范 / 開発ルール

[中文](#中文) · [English](#english) · [日本語](#日本語)

[README](README.md) · [TESTING](docs/TESTING.md) · [PUBLISHING](docs/PUBLISHING.md)

## 中文

先读 README、对应契约及 TESTING。只使用公共 SDK，不访问宿主 Room、任意设备文件、账号凭据或内部同步实现。插件、平台、语言各用自己的格式和索引，不能混装。

使用 init 创建模板，业务代码放进 extensions 下自己的目录。模板、打包器、发布器共用校验；不要删校验来让包通过。修改可执行内容或权限时递增扩展版本，已发布资产不可覆盖。

语言只编辑自己的文件，保留参数、保护词和基线；不拿中文假装译完。用 message-context 核对上下文；未知项应注明，不能猜测。

所有说明使用中英日三语。新增文档必须含三个语言段落，共用代码必须保持一致。提交前运行仓库检查、Python 与 Node 测试；页面改动另验收三比例、触摸和方向键。预览使用样本，设备和真实服务结果应单独记录。

只提交本次文件，不提交环境、凭据、缓存、node_modules 或构建输出。发布前提交并推送源码；只有 Release 资产回读校验成功后才能更新商店目录。未经用户授权，不自动发版、推送或改其他需求。

## English

Read README, the relevant contract and TESTING first. Use the public SDK; do not access host Room storage, arbitrary device files, credentials or internal sync implementations. Plugins, platforms and languages use separate formats and indexes.

Generate templates with init and keep your implementation under its own extensions directory. Templates, packaging and publishing share checks; never remove checks to make a package pass. Increment the extension version for executable or permission changes. Published assets are immutable.

Edit only the target language, preserving arguments, protected terms and the baseline. Do not mark Chinese text as a completed translation. Consult message-context; flag unknown context rather than guessing.

Provide Chinese, English and Japanese documentation. New documents need all three language sections and equivalent executable examples. Before committing, run repository checks and Python/Node tests. Page changes also require three aspect ratios, touch and directional navigation. Preview uses fixtures; record device and real-service evidence separately.

Commit only scoped files; exclude environments, credentials, caches, node_modules and build output. Commit and push source before publishing. Update store catalogs only after downloading and verifying the Release asset. Do not publish, push or change unrelated requirements without user authorization.

## 日本語

最初に README、対象の契約、TESTING を読んでください。公開 SDK を使用し、ホストの Room、任意の端末ファイル、認証情報、内部の同期実装にはアクセスしないでください。プラグイン、プラットフォーム、言語はそれぞれ別の形式と索引を使用します。

init でテンプレートを生成し、実装は extensions 内の専用ディレクトリに配置してください。作成、パッケージ化、公開は同じ検査を使用します。検査を削除して通過させないでください。実行内容や権限を変更したら拡張のバージョンを上げます。公開済みアセットは上書きできません。

対象言語だけを編集し、引数、保護語、基準を保持してください。中国語を翻訳済みの文章として扱わないでください。message-context で確認し、不明な項目は推測せず明記してください。

説明文書は中国語、英語、日本語で用意します。新しい文書には三言語の節と同等の実行例が必要です。コミット前にリポジトリ検査と Python／Node テストを実行してください。ページを変更した場合は三つの画面比率、タッチ、方向キーも検証します。プレビューはサンプルデータを使用するため、実機と実サービスの検証結果は別に記録してください。

対象ファイルだけをコミットし、環境、認証情報、キャッシュ、node_modules、ビルド出力は含めないでください。公開前にソースをコミットして push します。Release アセットを再取得して検証した後にだけストアの索引を更新します。利用者の許可なく公開、push、無関係な要件の変更を行わないでください。
