# 发布 / Publishing / 公開

[中文](#中文) · [English](#english) · [日本語](#日本語)

```text
python tools/retromao.py check extensions/demo-plugin
git add extensions/demo-plugin
git commit -m "Add demo plugin 1.0.0"
git push origin HEAD
python tools/retromao.py publish extensions/demo-plugin --tag demo-plugin-1.0.0 --repository YourAccount/RetroMao-Community --notes extensions/demo-plugin/RELEASE_NOTES.md
git add plugins/index.json
git commit -m "Publish verified demo plugin catalog"
git push origin HEAD
```

[GitHub Release create](https://cli.github.com/manual/gh_release_create) · [Release download](https://cli.github.com/manual/gh_release_download) · [Workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

## 中文

插件和平台先在自己的 Fork 提交并推送完整源码，再发布版本化 ZIP，最后更新目录。Fork 不继承 Release；保留上游条目意味着还要自行发布其资产，或明确移除不由自己分发的条目。发行说明使用模板的三个语言段落并填写真实变化与验收结果，不把空模板直接发布。

publish 要求工作区干净、origin 与目标仓库一致、本地 HEAD 与远端当前分支一致，且扩展版本高于该目录已有版本。它校验并打包、创建新 Release、下载资产核对字节数和 SHA-256，全部成功后才修改对应索引。失败会停止；Release 已创建但后续失败时保留真实状态，人工核对并恢复，不能覆盖旧资产或伪造目录。后续提交索引才能让应用发现新版本。

下方命令中的 YourAccount、路径、版本和说明文件必须替换为自己的值。catalog.json 管平台／主题，plugins/index.json 管脚本。语言不发 ZIP 或 Release；完整性校验后提交单语 JSON 与生成的 languages/index.json，推送即可。status 是兼容元数据，不需要人工审核状态。新增语言不得改变 catalog_version 或 catalog_hash。

GitHub Actions 的 Publish extension 工作流提供相同流程，只手动触发，具有 contents:write，完成校验和浏览器测试后发布并提交回读通过的目录。仓库需允许 Actions 写入；分支保护禁止直接推送时，改为按下方本地流程提交索引 PR，不放宽保护。读取和 PR 检查只用 contents:read，不使用 pull_request_target。

版本和标签不可覆盖；本地 ZIP 只能证明可导入，商店发布还要核对目标仓库默认分支中的索引与真正的 Release 文件。应用从来源仓库取得资产，不根据作者名跳到上游。平台启动格式 2 必须配合包含该能力的宿主，不能把旧版 APK 的安装失败归为网络或登录问题。

## English

For plugins and platforms, commit and push complete source in your fork, publish a versioned ZIP, then update the catalog. Forks do not inherit Releases. Keeping upstream entries requires publishing those assets yourself or removing entries you do not distribute. Fill all three release-note sections with real changes and acceptance results; do not publish the empty template.

publish requires a clean checkout, matching origin/target repositories, identical local HEAD and remote branch commits, and an extension version newer than the existing catalog entry. It validates and packages, creates a new Release, downloads the asset and checks exact size/SHA-256, then updates the appropriate index. Failures stop the process. If the Release exists but a later step fails, preserve and inspect the real state; do not overwrite assets or fabricate a catalog. Commit the catalog afterward for app discovery.

Replace YourAccount, paths, versions and the notes file below with your own values. catalog.json contains platforms/themes; plugins/index.json contains scripts. Languages use no ZIP or Release: validate completeness, commit the language JSON plus generated languages/index.json, then push. status is compatibility metadata and requires no human-review state. New languages must preserve catalog_version and catalog_hash.

The manually triggered GitHub Actions Publish extension workflow uses the same process with contents:write. It runs checks and browser tests before publishing and committing the verified catalog. Actions writes must be enabled. If branch protection disallows direct pushes, submit a catalog PR using the local flow below; do not weaken protection. Read and PR checks only use contents:read, never pull_request_target.

Versions and tags are immutable. Local ZIP import alone does not verify store publication: check the default-branch catalog and actual Release asset in the destination repository. The app downloads from that repository rather than following the author's name upstream. Platform format 2 needs a host containing the feature; installation failure on an older APK is not a network or login diagnosis.

## 日本語

プラグインとプラットフォームは、Fork に完全なソースをコミットして push し、バージョン付き ZIP を公開してからカタログを更新します。Fork は Release を継承しません。上流の項目を残す場合は対応するアセットを自分で公開するか、自分が配布しない項目を削除してください。リリースノートの三言語の節に実際の変更と検証結果を記入し、空のテンプレートを公開しないでください。

publish には、クリーンな作業ツリー、origin と公開先の一致、ローカル HEAD とリモートブランチの一致、既存のカタログより新しい拡張バージョンが必要です。検査とパッケージ化、新規 Release の作成、アセットの再取得、サイズと SHA-256 の検証を行い、成功した場合だけ索引を更新します。失敗したら停止します。Release 作成後に失敗した場合は実際の状態を残して確認し、アセットの上書きや索引の捏造を行わないでください。その後にカタログをコミットするとアプリから検出できます。

下の YourAccount、パス、バージョン、説明ファイルは自分の値に置き換えてください。catalog.json はプラットフォームとテーマ、plugins/index.json はスクリプト用です。言語には ZIP や Release を使用しません。完全性を確認し、言語 JSON と生成された languages/index.json をコミットして push します。status は互換性メタデータであり、人による審査状態は不要です。言語を追加しても catalog_version と catalog_hash を変更しないでください。

手動実行の GitHub Actions「Publish extension」も同じ処理を行い、contents:write を使用します。検査とブラウザーテストの後に公開し、検証済みのカタログをコミットします。Actions の書き込みを許可する必要があります。ブランチ保護で直接 push できない場合は、下のローカル手順でカタログの PR を作成し、保護を緩めないでください。読み取りと PR の検査は contents:read のみを使い、pull_request_target は使用しません。

公開済みのバージョンとタグは変更できません。ローカル ZIP のインポートだけではストア公開の検証になりません。公開先のデフォルトブランチにあるカタログと、実際の Release アセットを確認してください。アプリは作者名から上流へ移動せず、指定リポジトリから取得します。形式 2 には対応ホストが必要です。旧 APK でのインストール失敗を通信やログインの問題と判断しないでください。
