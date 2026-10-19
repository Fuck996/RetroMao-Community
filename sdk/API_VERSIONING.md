# API 版本管理 / API versioning / API バージョン管理

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Inventory](api.json) · [Reference](API_REFERENCE.md) · [Changes](API_CHANGELOG.md) · [Extension releases](PLUGIN_VERSIONS.md) · [Other contracts](../docs/INTERFACES.md)

```text
python tools/check_api.py
python tools/check_api.py --write
python tools/check_api.py --base origin/main
python tools/retromao.py check
npm test
```

## 中文

版本分为四层：`apiVersion:1` 与 `retromao.version === 1` 是运行协议主版本；`sdk/api.json` 的 `version` 是公开 SDK 契约版本，当前 1.0.0；插件 `version` 是作者自己的发行版本；`minAppVersion` 是最低兼容宿主。这四者不能互相代替。插件清单不增加 `sdkVersion`，也不把契约版本填进 `minAppVersion`。

契约使用三段数字：修正文档、补充示例或兼容修复升 patch；增加接口升 minor；移除接口、改变签名、权限、可用上下文或调用语义升 major。主版本必须与真实运行时及宿主支持的 API 主版本相同。API v2 需要先实现宿主与运行时支持，不能仅修改文档或版本值。新增参数、返回字段或行为变化也必须人工审查兼容性；自动门禁无法理解所有业务语义。

作者选择 `minAppVersion` 时取所用功能的最大要求：基础脚本 0.9.90；records/apply/checkpoint/STORAGE 为 0.9.91；图标 0.9.92；插件语言环境 0.9.94；独立配置页及 configuring 为 0.9.96；资源解析回调为 0.9.98。逐接口的起始版本见调用手册，后续新增字段仍需查看变更说明。API 1 不保证旧 APK 有所有 API 1 功能。

维护者修改接口时，先核对真实实现和权限边界，同步 `retromao.d.ts`、运行时、`api.json` 的三语描述与可执行示例。递增契约版本，更新日期、已核对宿主版本和 `sources` 的 SHA-256，把完整清单保存为新的 `sdk/releases/x.x.x.json`；已有快照永久保留且不可改写。不要按函数名猜测失败语义，也不要以文档修改冒充宿主已实现。

然后在 API_CHANGELOG 的三个语言段落记录新增／修改／移除、兼容性、最低宿主、迁移办法与验证范围，运行 `--write` 生成调用手册。生成器只更新手册，不自动更新哈希、版本或快照，让维护者明确审查变更。命令中的 origin/main 应替换为本次变更前的远端基线；首次建立记录允许没有旧快照。

仓库 check 校验清单、完整类型签名、SDK 文件哈希、当前快照、三语手册和变更记录。Node 测试核对实际运行时成员，并逐段执行手册示例。CI 使用 PR 基线或 push 前提交检查旧快照不可修改、版本递增和明显的不兼容变更。语义变更、Android 原生、真实网盘和模拟器仍需人工／实机验收，失败不得隐藏。仅文档更新不递增宿主 APK 或现有插件的发行版本。

发布先提交并推送契约与源码，通过 CI 后按照 PUBLISHING 发布作者的新扩展版本；旧 Release 资产、旧契约快照和旧变更记录均保留。退回旧扩展按既有安装兼容性操作；不能用删除历史、覆盖 ZIP 或降低最低宿主绕过接口要求。

## English

There are four version layers: `apiVersion:1` and `retromao.version === 1` identify the runtime protocol major; `sdk/api.json` version is the public SDK contract release, currently 1.0.0; plugin `version` belongs to the author's release; `minAppVersion` is the oldest supported host. They are not interchangeable. Do not add `sdkVersion` to plugin manifests or put the contract version in `minAppVersion`.

Contract releases use three numbers: documentation/example corrections and compatible fixes increment patch; additional APIs increment minor; removals or changes to signatures, grants, contexts or semantics increment major. The major must match an implemented runtime and host API major. API v2 requires host/runtime implementation first; editing documentation or a version number does not provide it. New arguments, return fields and behavioral changes also need human compatibility review: automated checks cannot understand every business rule.

Choose the highest `minAppVersion` required by your features: basic scripting 0.9.90; records/apply/checkpoint/STORAGE 0.9.91; icons 0.9.92; plugin locale environment 0.9.94; dedicated configuration pages/configuring 0.9.96; resource callbacks 0.9.98. Consult the reference for each member's first version and the changelog for later additions. API 1 does not mean an old APK has every API 1 feature.

Maintainers first verify actual implementation and permission boundaries, then update retromao.d.ts, runtime and api.json descriptions/examples in all three languages. Increment the contract version; update its date, checked host version and sources SHA-256 values; save the complete inventory to a new sdk/releases/x.x.x.json. Preserve existing snapshots unchanged. Do not infer failure semantics from function names or describe unimplemented host features as available.

Record additions/changes/removals, compatibility, minimum host, migration and validation scope in all three API_CHANGELOG sections, then generate the reference with --write. Generation only rewrites the reference; hashes, versions and snapshots require deliberate review. Replace origin/main in the command with the remote baseline before your change. The first tracked release may have no earlier snapshots.

Repository check validates the inventory, full type signatures, SDK hashes, current snapshot, trilingual reference and change records. Node tests compare the runtime surface and execute every reference snippet. CI compares the PR base or pre-push commit to reject modified historical snapshots, missing version increments and obvious breaking changes. Semantics, native Android, real cloud services and emulators still require human/device acceptance; expose failures. Documentation-only updates do not increment the host APK or existing plugin releases.

Commit and push the contract/source first, pass CI, then follow PUBLISHING for the author's new extension release. Keep old Release assets, contract snapshots and change records. Restore old extensions through existing installation compatibility rules; never bypass API requirements by deleting history, replacing ZIPs or lowering the minimum host.

## 日本語

バージョンは四層です。`apiVersion:1` と `retromao.version === 1` は実行プロトコルのメジャー版、sdk/api.json の version は公開 SDK 契約版（現在 1.0.0）、プラグインの version は作者の公開版、minAppVersion は必要なホストの最低版です。相互に代用できません。プラグインのマニフェストへ sdkVersion を追加したり、契約版を minAppVersion に入れたりしないでください。

契約版は三つの数字です。文書・例の訂正や互換修正は patch、API の追加は minor、削除やシグネチャ・権限・実行場所・意味の変更は major を上げます。メジャー版は実装済みのホストと実行 API に一致する必要があります。API v2 は先にホストと実行コードの対応が必要で、文書や数字を変えるだけでは利用できません。引数、戻り項目、動作の追加も人による互換性確認が必要で、自動検査だけでは業務上の意味を判定できません。

minAppVersion は使用機能のうち最も高い要件にします。基本スクリプトは 0.9.90、records/apply/checkpoint/STORAGE は 0.9.91、アイコンは 0.9.92、プラグインの言語環境は 0.9.94、独立設定ページと configuring は 0.9.96、リソースコールバックは 0.9.98 です。各メンバーの初出版はリファレンス、その後の追加は変更履歴を確認してください。API 1 だけで旧 APK が全機能を持つとは判断できません。

保守担当者は実装と権限境界を確認し、retromao.d.ts、実行コード、api.json の三言語説明と実行例を更新します。契約版を上げ、日付、確認したホスト版、sources の SHA-256 を更新して、一覧全体を新しい sdk/releases/x.x.x.json に保存します。既存のスナップショットは変更せず残します。関数名から失敗の意味を推測したり、未実装のホスト機能を利用可能と説明したりしないでください。

API_CHANGELOG の三言語に追加・変更・削除、互換性、最低ホスト、移行手順、検証範囲を記録し、--write でリファレンスを生成します。生成器はリファレンスだけを更新し、ハッシュ、版、スナップショットは明示的な確認が必要です。コマンドの origin/main は変更前のリモート基準に置き換えてください。初めての記録では過去のスナップショットがなくても構いません。

リポジトリの check は一覧、完全な型シグネチャ、SDK ハッシュ、現在のスナップショット、三言語文書、変更記録を検査します。Node テストは実行 API の全メンバーと各実行例を確認します。CI は PR の基準または push 前のコミットと比較し、過去版の改変、版の更新漏れ、明らかな非互換変更を拒否します。意味、Android、実際のクラウドとエミュレーターは人や実機で検証し、失敗は明示します。文書だけの更新で APK や既存プラグインの版を上げません。

契約とソースをコミットして push し、CI 通過後に PUBLISHING に従って作者の新しい拡張版を公開します。旧 Release アセット、契約スナップショット、変更履歴は保持します。旧拡張へ戻す際も既存の互換性規則に従い、履歴削除、ZIP 上書き、最低ホストの引き下げで API 要件を回避しないでください。
