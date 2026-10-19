# 贡献 / Contributing / 投稿

[中文](#中文) · [English](#english) · [日本語](#日本語)



## 中文

先选择插件、语言或平台，不需要构建 APK。使用 README 的 init 命令；生成目录会受 Git 管理，不能把源码只留在被忽略的 dist 或 work 中。

PR 应说明目的、作者、最低宿主版本、权限、素材来源及许可，并列出本地检查、预览和设备验收情况。未进行的验收明确写出。平台新增启动配置时，必须核对模拟器官方的包名、完整 Activity、URI 支持或核心 ID。

发布到自己 Fork 和向上游投稿是两件事。上游不会自动采用 Fork 的目录或 Release；上游维护者审核后在上游仓库发布资产。仅复制上游 catalog 会引用自己仓库中不存在的资产。

修复文档和工具不改写旧资产。保留原作者与第三方素材许可；没有明确再分发许可的素材不要打包。仓库说明中的 MIT 字样不替代第三方授权证明。

## English

Choose plugin, language or platform development first; no APK build is required. Use the README init commands. Generated source directories are tracked by Git; do not leave source only in ignored dist or work directories.

A PR should state purpose, author, minimum host version, permissions, asset origins and licenses, plus local checks, preview and device acceptance. State checks you have not performed. For platform launchers, verify the emulator's official package name, full Activity, URI support or core ID.

Publishing in your fork and contributing upstream are separate. Upstream does not automatically adopt fork catalogs or Releases; maintainers review and publish upstream assets themselves. Copying the upstream catalog alone points at assets missing from your own repository.

Documentation and tooling fixes must not rewrite old assets. Preserve original authors and third-party licenses. Do not package assets without redistribution permission. A reference to MIT in repository prose does not establish third-party rights.

## 日本語

最初にプラグイン、言語、プラットフォームのいずれかを選びます。APK のビルドは不要です。README の init コマンドを使用してください。生成されたソースは Git で管理されます。無視される dist や work だけにソースを残さないでください。

PR には目的、作者、必要なホストバージョン、権限、素材の出典とライセンス、ローカル検査、プレビュー、実機検証を記載してください。未実施の検証も明記します。起動設定を追加する場合は、エミュレーター公式のパッケージ名、完全な Activity 名、URI 対応またはコア ID を確認してください。

Fork での公開と上流への投稿は別の作業です。上流は Fork のカタログや Release を自動採用しません。保守担当者が確認した後、上流でアセットを公開します。上流のカタログだけを複製すると、自分のリポジトリに存在しないアセットを参照します。

文書やツールの修正で旧アセットを変更しないでください。元の作者と第三者素材のライセンスを保持し、再配布の許可が不明な素材は含めないでください。説明文にある MIT という表記だけでは、第三者の権利は確認できません。
