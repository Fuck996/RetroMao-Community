# 搜索扩展 / Search extensions / 検索拡張

## 中文

普通文字匹配立即显示；增强词在后台准备期间，同一结果区明确显示准备状态，完成后合并匹配。扩展失败时中止当前搜索并显示原因，不把失败当作准备中或正常空结果。

最低宿主为 0.9.112。清单声明 `capabilities: ["SEARCH"]`、`entryPoint` 和 `searchProvider: "initials"`，并在既有 `retromao.define({actions:{initials}})` 中实现对应函数。纯搜索插件无需业务页面、可见动作或资源提供者。安装后由玩家启用并授权；禁用、卸载或更新立即撤下旧扩展结果。

宿主在输入非空搜索词后，向该函数传入 `{texts: string[]}`，每批最多 200 个当前范围内的非空名称、JSON 参数最多 256 KiB。回调返回 `{aliases: string[][]}`，按输入顺序逐项对应；每项最多 16 个非空搜索词，单词最多 4096 字符，总消息仍受 512 KiB 限制。无需查询全文、扫描文件或自行创建游戏库。插件只得到当前游戏范围的标题、排序名、ROM 文件名，或应用名称；不传文件正文、路径、应用包名、游戏 ID 或查询词。

搜索回调通过原后台脚本引擎执行，每批限时 30 秒，使用原隔离和清理生命周期；回调只允许 `ready` 与 `settings.get`，不能写数据、联网、创建任务或执行其他业务。插件在这里生成搜索词，不改变宿主的范围、排序、分组和启动方式。输入变化只过滤已生成的词；页面退出取消运行并释放隔离实例。输出无效、权限变化或执行失败会显示增强搜索错误，不能伪装成空结果或悄悄替换实现。

官方拼音插件为 [pinyin-initials](../extensions/pinyin-initials/README.md)，离线包含固定版本 pinyin-pro 及繁体映射。函数签名和 API 1 运行时不变；SDK 1.1.0 追加回调类型和清单约定，旧插件不需迁移。新插件必须声明实际最低宿主版本，不能只依据 `apiVersion: 1` 判断兼容性。

## English

Literal matches appear immediately. The same results panel shows an explicit preparation state while aliases are generated, then merges matching aliases. An extension failure stops the current search and displays its cause; it is never presented as loading or an ordinary empty result.

Requires host 0.9.112. Declare `capabilities: ["SEARCH"]`, `entryPoint` and `searchProvider: "initials"`; implement that function through the existing `retromao.define({actions:{initials}})`. Search-only plugins need no page, visible action or resource provider. The player must enable and authorize the plugin. Disabling, uninstalling or updating removes its previous results.

For a nonempty query, the host sends `{texts: string[]}`: at most 200 nonempty names and 256 KiB of JSON per batch. Return `{aliases: string[][]}` in input order, at most 16 nonempty aliases per name, 4096 characters per alias, within the existing 512 KiB message limit. Only current-scope game titles, sort titles and ROM filenames, or app labels are sent. No file contents, paths, package names, game IDs or query text are supplied. Do not scan files or build another library.

Callbacks use the existing background engine, isolation and teardown, with a 30-second batch deadline. Only `ready` and `settings.get` are allowed: no mutations, network, task creation or other business operations. The host retains scope, ordering, grouping and launch behavior. Typing filters generated aliases; leaving cancels work and releases the isolate. Invalid output, changed permissions and execution failures are reported explicitly.

[pinyin-initials](../extensions/pinyin-initials/README.md) bundles pinned offline pinyin-pro and traditional-character mappings. SDK 1.1.0 adds callback types and manifest conventions; existing RPC signatures and runtime API 1 remain unchanged. Existing plugins need no migration. Declare the actual minimum host version rather than relying only on `apiVersion: 1`.

## 日本語

通常の文字一致は直ちに表示します。検索語の生成中は同じ結果領域に準備状態を示し、完了後に一致結果を統合します。拡張が失敗した場合は検索を停止して原因を表示し、準備中や通常の空結果として扱いません。

ホスト 0.9.112 以上が必要です。`capabilities: ["SEARCH"]`、`entryPoint`、`searchProvider: "initials"` を宣言し、既存の `retromao.define({actions:{initials}})` で対応する関数を実装します。検索専用プラグインにはページ、表示用アクション、リソースプロバイダーは不要です。利用者が有効化・許可し、無効化、削除、更新時には以前の拡張結果を取り除きます。

空でない検索入力に対し、ホストは `{texts: string[]}` を渡します。1 バッチは空でない名前 200 件、JSON 256 KiB までです。入力順に対応する `{aliases: string[][]}` を返します。各名前は空でない検索語 16 個、各語 4096 文字までで、メッセージ全体は従来の 512 KiB 制限に従います。現在の範囲のゲーム名、並べ替え名、ROM ファイル名、またはアプリ名のみを渡します。ファイル内容・パス、パッケージ名、ゲーム ID、入力した検索語は渡しません。ファイル走査や別のライブラリを作らないでください。

既存のバックグラウンドエンジン、隔離と終了処理を使い、1 バッチの期限は 30 秒です。`ready` と `settings.get` のみ許可し、書き込み、通信、タスク作成などは禁止します。範囲、順序、グループ化、起動方法はホストが保持します。入力変更時は生成済みの語を絞り込み、ページ終了時は処理を取り消して隔離インスタンスを解放します。不正な結果、権限変更、実行エラーは明示します。

[pinyin-initials](../extensions/pinyin-initials/README.md) は固定版 pinyin-pro と繁体字対応表をオフラインで同梱します。SDK 1.1.0 は型とマニフェストの規約を追加し、既存 RPC のシグネチャと API 1 は維持します。既存プラグインの移行は不要です。`apiVersion: 1` のみで判断せず、必要な最低ホストを指定してください。
