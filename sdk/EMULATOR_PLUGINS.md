# 模拟器插件 / Emulator plugins / エミュレータープラグイン

## 中文

宿主 0.9.141 新增可编辑入口：声明 `editableEmulators: true`、`EMULATORS` 能力、真实业务页和最低版本 0.9.141，通过 [emulators API](API_REFERENCE.md) 管理本插件入口，每项选择一个平台。可设 action（默认 VIEW）、romData（默认 true）、extras 和 flags。附加值保留文本、布尔、数字及文本数组类型，`{romUri}` 替换为当前游戏 URI；关闭 ROM Data 后须在附加值中传入 URI。允许 NEW_TASK、CLEAR_TASK、CLEAR_TOP、SINGLE_TOP；CLEAR_TASK 要求 NEW_TASK。每个入口最多 16 KiB、32 项附加值，文本数组最多 64 项。未编辑时使用清单预设，保存后以安装记录中的配置为唯一来源；空列表表示全部删除。原值校验拒绝并发覆盖，同来源升级保留配置。脚本仍不能直接启动应用，真实启动沿用游戏库主链路。下文为 0.9.138 的初始协议。

开发中的宿主 0.9.138 增加 `plugin.json.emulators`，允许插件为内置或已安装的扩展机种声明 URI 启动配置。插件仍由原插件中心安装、确认、启用、更新和卸载；无需虚构页面、脚本动作或额外权限。声明不是任意 Intent 接口：只支持显式 Android 组件、`ACTION_VIEW`、所选 ROM 的内容 URI、可选 MIME 和临时只读授权。脚本不能自动启动应用。

每项包含 `id`、`name`、`packageName`、完整 `activity`、非空 `platforms`，可选 `mimeType`；最多 16 项，ID 不重复。格式与 Android 组件复用平台启动配置的校验。插件必须设置 `minAppVersion` 为 `0.9.138` 或更高；旧宿主不支持这项能力。示例见 [Azahar Plus](../extensions/azahar-plus/plugin.json)。

配置使用 `plugin.<来源或 local>:<插件 ID>.<配置 ID>` 隔离，不能覆盖内置配置。原安装记录是唯一来源：只有已启用且满足已有授权的插件进入模拟器列表。停用、启动配置变化或卸载后，旧的待启动请求会失败；保存的用户选择保留，重新启用后恢复，不静默切换模拟器。重启后从原插件记录恢复。启动沿用原文件存在检查、机种边界、URI 授权、存档门禁和游玩记录。

插件 ZIP 通过原打包器生成，商店仍使用 `plugins/index.json`；发布前提交、推送源代码，上传 Release 资产并回读校验后才能登记商店。宿主支持、ZIP 自动验证、Android 真实安装和进入游戏必须分别记录，不能把配置验证称为真机运行成功。

## English

Host 0.9.141 adds editable entries with `editableEmulators: true`, the EMULATORS grant, a business page and minimum host 0.9.141. The [emulators API](API_REFERENCE.md) manages owned entries with one platform each. It supports action (default VIEW), romData (true), typed extras and flags. Strings substitute `{romUri}`; extras must carry it when ROM Data is off. Flags: NEW_TASK, CLEAR_TASK, CLEAR_TOP, SINGLE_TOP; CLEAR_TASK requires NEW_TASK. Limits: 16 KiB and 32 extras per entry, 64 strings per array. Seeds apply until first edit; installed records are then the sole source. An empty list means all removed. Original-value checks reject conflicts; same-source upgrades preserve edits. Scripts cannot directly launch apps; games use the existing library flow. The initial 0.9.138 contract follows.

Host 0.9.138, currently under development, adds `plugin.json.emulators` for declarative URI launch profiles targeting built-in or installed extension platforms. The existing plugin center handles installation, confirmation, enablement, updates and removal. No dummy page, script action or extra permission is required. This is not an arbitrary Intent API: profiles use an explicit Android component, `ACTION_VIEW`, the selected ROM's content URI, an optional MIME type and temporary read access. Scripts cannot launch applications automatically.

Each entry requires `id`, `name`, `packageName`, a fully qualified `activity` and nonempty `platforms`; `mimeType` is optional. At most 16 entries are allowed and IDs must be unique. Component validation reuses platform launcher rules. Set `minAppVersion` to `0.9.138` or later; older hosts do not support this capability. See [Azahar Plus](../extensions/azahar-plus/plugin.json).

Profile IDs use `plugin.<source or local>:<plugin ID>.<profile ID>` and cannot replace built-in profiles. Existing installation records are the only source. Only enabled plugins satisfying their existing grants contribute profiles. Disabling a plugin, changing its launch profile or uninstalling it invalidates prepared launches. Saved selections remain available for re-enabling; the host never silently switches emulators. Restart restores profiles from those same records. Launch uses the existing file checks, platform boundaries, URI grants, save checks and play-history flow.

Use the existing packager and `plugins/index.json`. Commit and push sources before publishing; verify uploaded Release assets before updating the store. Record package validation, Android installation and actual gameplay separately.

## 日本語

ホスト 0.9.141 では `editableEmulators: true`、EMULATORS 権限、業務ページ、最低版 0.9.141 を指定し、[emulators API](API_REFERENCE.md) で自身の起動設定を管理します。一件につきプラットフォームは一つです。action（既定 VIEW）、romData（true）、型付き extras、flags に対応し、`{romUri}` をゲーム URI に置換します。ROM Data 無効時は extras に含めてください。NEW_TASK、CLEAR_TASK、CLEAR_TOP、SINGLE_TOP を許可し、CLEAR_TASK には NEW_TASK が必要です。一件16 KiB、追加値32件、文字列配列64件が上限です。初回編集までは初期値を使い、その後はインストール記録だけを使用します。空リストは全件削除です。元の値で競合を検出し、同じ配布元の更新でも設定を維持します。直接起動 API はなく、既存のゲーム起動処理を使用します。以下は 0.9.138 の初期規約です。

開発中のホスト 0.9.138 は `plugin.json.emulators` を追加します。内蔵・インストール済み拡張機種向けの URI 起動設定を宣言できます。インストール、確認、有効化、更新、削除には既存のプラグインセンターを使用します。不要なページやスクリプト処理、追加権限は必要ありません。任意の Intent を送信する API ではありません。明示的な Android コンポーネント、`ACTION_VIEW`、選択した ROM のコンテンツ URI、任意の MIME、一時的な読み取り権限のみを使用し、スクリプトから自動起動できません。

各項目には `id`、`name`、`packageName`、完全修飾の `activity`、空でない `platforms` が必要です。`mimeType` は任意です。最大 16 件で、ID は重複できません。コンポーネントの検証はプラットフォーム起動設定と共通です。`minAppVersion` は `0.9.138` 以降にしてください。旧ホストはこの機能に対応していません。[Azahar Plus](../extensions/azahar-plus/plugin.json) が実装例です。

設定 ID は `plugin.<配布元または local>:<プラグイン ID>.<設定 ID>` に分離され、内蔵設定を上書きしません。既存のインストール記録だけを参照し、有効かつ必要な既存権限を満たすプラグインだけを一覧へ追加します。無効化・起動設定の変更・削除後の古い起動要求は失敗します。保存済みの選択は再有効化のため保持し、別のエミュレーターへ自動変更しません。再起動時も同じ記録から復元します。ファイル確認、機種制限、URI 権限、セーブ確認、プレイ履歴は元の起動処理を使用します。

既存のパッケージ作成ツールと `plugins/index.json` を使用します。公開前にソースをコミットして push し、Release ファイルの再取得検証後にストアへ登録してください。ZIP 検証、Android へのインストール、実際のゲーム起動は分けて記録します。
