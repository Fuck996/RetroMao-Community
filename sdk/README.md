# 脚本插件 SDK v1 / Script plugin SDK v1 / スクリプト SDK v1

[中文](#中文) · [English](#english) · [日本語](#日本語)

[模拟器插件（开发中，宿主 0.9.138） / Emulator plugins (development, host 0.9.138) / エミュレータープラグイン（開発中、ホスト 0.9.138）](EMULATOR_PLUGINS.md)

[搜索扩展 / Search extensions / 検索拡張](SEARCH_EXTENSIONS.md)

[插件卡片与文案规范 / Card and copy guidelines / カードと文言の規約](PLUGIN_PRESENTATION.md)

[API reference / 逐接口调用 / API 呼び出し](API_REFERENCE.md) · [Inventory / 清单 / 一覧](api.json) · [Versioning / 版本管理 / 版管理](API_VERSIONING.md) · [API changes / 接口变更 / API 変更](API_CHANGELOG.md)

[Types](retromao.d.ts) · [Schema](../schemas/plugin.schema.json) · [Localization](PLUGIN_LOCALIZATION.md) · [Versions](PLUGIN_VERSIONS.md) · [ROM resources](ROM_RESOURCES.md) · [Testing](../docs/TESTING.md) · [Publishing](../docs/PUBLISHING.md)

| API | Capability / 能力 / 権限 |
| --- | --- |
| library.game/games/records, favorites.list, recent.list, media.folders/assets | LIBRARY_READ |
| library.edit/apply, favorites.set, recent.edit, media.edit, index.patch | LIBRARY_WRITE |
| http.request | NETWORK + networkHosts |
| storage.sources/read/write | STORAGE |
| define resources | ROM_RESOURCES |
| searchProvider | SEARCH + host 0.9.112 |
| settings.get, data.get/patch, tasks.run/get/current/result/cancel/watch/progress | Own plugin / 本插件 / 自分のプラグイン |

```text
python tools/retromao.py check templates/plugin
python tools/retromao.py preview templates/plugin
python tools/build_script_plugin.py examples/library-notes --release-tag script-examples-1
```

## 中文

ZIP 根目录包含 plugin.json，后台入口是打包完成的 JavaScript，业务页面使用包内 HTML/CSS/JS。宿主在文档开始注入正式 SDK，作者先等待 retromao.ready，不复制或从 CDN 加载运行代码。类型定义是公共接口完整字段参考；从 templates/plugin 开始，library-notes 演示收藏和索引字段，两个同步示例演示复杂合并。

schemaVersion 与 apiVersion 都是 1。ID、作者、版本、最低宿主版本和默认语言必填。actions 与 define 中的函数 ID 对齐；pages 声明页面。后台无 DOM、Node.js、Java 反射、任意设备路径或 Room。使用公共接口，不在插件中另建游戏库或同步索引。未来新增 API 需调整最低宿主版本，不能只看 apiVersion:1。

LIBRARY_READ、LIBRARY_WRITE、NETWORK、STORAGE、ROM_RESOURCES 由清单声明并在宿主启用时授权。NETWORK 另需 networkHosts，HTTP 不跟随重定向，非 2xx 状态交给作者处理，正文上限 256 KiB。STORAGE 只提供已配置连接内本插件命名空间的小型 JSON；不返回密码、任意路径、二进制或删除能力。脚本隔离不等于独立操作系统安全边界，只安装可信作者代码。

settings 支持 TEXT、SECRET、BOOLEAN、NUMBER、CHOICE、DIRECTORY，值统一为字符串。BOOLEAN 默认 false；CHOICE 指定 options 的 value 和 label；DIRECTORY 由宿主持久化 SAF 授权，不能让页面填写任意 URI。SECRET 使用宿主凭据存储。配置在动作开始时读取，来源仓库和插件 ID 隔离配置及私有 JSON。

独立配置页必须以 kind:CONFIGURATION 声明并由 configurationPage 引用，最低宿主 0.9.96；不能复用业务 HTML。禁用插件时仍可配置。配置页仅能 ready、settings、data 读写，以及声明 STORAGE 后列出本机连接；不能运行任务、改游戏库或访问远端。标题、返回、导航、授权和卸载由宿主管理，插件只画内容区。

library.games 与 records 使用键集分页，最多 200；保留原样的 next 作为 after，不用页码或自行拼 cursor。records 不含媒体正文、文件路径或哈希。编辑每批最多 200，metadata.expected、recent.expected、媒体 expected 和扩展字段 expected 用于并发核对，冲突必须展示并重读，不吞错重试。apply 不返回大游戏对象；可选 checkpoint 与该批修改原子保存，整个脚本并非跨 API 事务。

index.patch 只编辑当前插件命名空间。扩展字段没有 expected 表示原来不存在，没有 value 表示删除，显式 null 是真实值；data.patch 则用顶层 null 删除键。两者不可混淆。收藏显式设置 true/false，不是 toggle；最近记录编辑不触发游戏启动。媒体只引用已授权且已入索引的素材，不能通过 JSON 传媒体正文。

storage.read 返回 token 和 value，文档缺失为 null；write 只接受本动作最近一次读取的 token、JSON 对象，单文档最大 384 KiB。token 不跨账号、目录、文档或动作。无变化不写；错误直接暴露，不自动换渠道或另建重试队列。

同一插件只运行一个动作。页面 tasks.run 发起，watch 返回取消订阅函数；退出页释放订阅，后台任务仍可继续。通过 current 接续当前任务，成功后 result 取结果。取消保留已完成批次；禁用、卸载终止相应动作，中断不自动重放可能提交的修改。结束释放隔离实例，关闭最后引擎连接，退出页销毁 WebView。游戏启动不等商店或脚本。

消息最大 512 KiB，SDK 最多同时发 4 个请求；分页、批量并等待结果。Android WebView 必须支持脚本隔离所需功能，缺失时提示更新，不切换到另一执行器。发布格式、资源限制和版本规则见下方链接；浏览器预览使用真实 SDK 与本地样本，不代表原生引擎和网盘通过验收。

## English

The ZIP root contains plugin.json. Background entry points are bundled JavaScript; pages use local HTML/CSS/JS. The host injects the shipped SDK at document start. Await retromao.ready; do not copy the SDK or load executable code from CDNs. Type definitions describe complete public fields. Start with templates/plugin; library-notes demonstrates favorites/index fields, and the sync examples demonstrate complex merging.

schemaVersion and apiVersion are both 1. ID, author, version, minimum host version and default locale are required. actions must match define function IDs; pages declares HTML pages. Background code has no DOM, Node.js, Java reflection, arbitrary device paths or Room. Use public APIs rather than a parallel game database or sync index. New APIs require an appropriate minimum host version, not merely apiVersion:1.

Declare LIBRARY_READ, LIBRARY_WRITE, NETWORK, STORAGE and ROM_RESOURCES for host authorization. NETWORK also requires networkHosts. HTTP does not follow redirects; authors handle non-2xx responses; bodies are limited to 256 KiB. STORAGE only exposes small JSON documents in this plugin's namespace within configured connections. It exposes no passwords, arbitrary paths, binary transfers or deletion. Script isolation is not an independent OS security boundary; install trusted code only.

settings supports TEXT, SECRET, BOOLEAN, NUMBER, CHOICE and DIRECTORY, with string values. BOOLEAN defaults to false. CHOICE uses value/label options. DIRECTORY uses host-persisted SAF permission, not arbitrary page-entered URIs. SECRET uses host credential storage. Settings are read at action start. Repository origin plus plugin ID isolates settings/private JSON.

Dedicated configuration pages use kind:CONFIGURATION and configurationPage, requiring host 0.9.96. They cannot reuse business HTML. Disabled plugins remain configurable. Configuration pages only use ready, settings, data reads/writes and, with STORAGE, local connection listing. They cannot run tasks, edit the library or access remote storage. The host owns title, back, navigation, grants and uninstall; plugins draw only content.

library.games/records use keyset pagination, up to 200. Pass next unchanged as after; do not invent page numbers or cursors. records excludes media bodies, paths and hashes. Edits support batches up to 200. metadata.expected, recent.expected, media expected and extension expected fields detect concurrency conflicts; show conflicts and reread rather than swallowing/retrying them. apply avoids returning large game objects. An optional checkpoint commits atomically with that batch; a script is not a transaction across APIs.

index.patch edits only the current plugin namespace. Missing expected means previously absent; missing value means delete; explicit null is stored data. data.patch instead deletes keys with top-level null. Keep these semantics separate. Favorites use explicit true/false, not toggles. Recent edits do not launch games. Media links only reference authorized indexed assets; JSON does not carry media bodies.

storage.read returns token/value, with null for a missing document. write requires the latest token read in that action and a JSON object, up to 384 KiB. Tokens cannot cross accounts, directories, documents or actions. Do not write unchanged content. Expose errors; do not switch providers or build a separate retry queue.

Only one action runs per plugin. Pages start it with tasks.run; watch returns an unsubscribe function. Release subscriptions on page exit; background tasks may continue. Reconnect using current and retrieve result after success. Cancellation retains completed batches. Disable/uninstall terminates the relevant action; interruptions do not automatically replay possibly committed writes. Finished actions release isolates and the final engine connection; page exit destroys the WebView. Game launch never waits for the store or scripts.

Messages are limited to 512 KiB and the SDK sends at most four concurrent requests. Paginate, batch and await results. Android WebView must support the required isolation features; missing support prompts an update without switching executors. Follow the linked packaging, resource and version rules. Browser preview uses the actual SDK with fixtures and does not prove native-engine or cloud acceptance.

## 日本語

ZIP のルートに plugin.json を置きます。バックグラウンドの入口はバンドル済み JavaScript、ページはパック内の HTML/CSS/JS です。ホストは文書の開始時に正式 SDK を注入します。retromao.ready を待ち、SDK の複製や CDN からのコード読み込みを行わないでください。公開フィールドは型定義を参照します。templates/plugin から始め、library-notes でお気に入りと索引フィールド、同期サンプルで複雑なマージを確認できます。

schemaVersion と apiVersion はともに 1 です。ID、作者、バージョン、最低ホストバージョン、既定言語が必須です。actions は define の関数 ID と一致させ、pages で HTML を宣言します。バックグラウンドでは DOM、Node.js、Java リフレクション、任意の端末パス、Room を使用できません。別のゲーム DB や同期索引を作らず公開 API を使います。新しい API を使う場合は apiVersion:1 だけで判断せず、最低ホストバージョンを指定してください。

LIBRARY_READ、LIBRARY_WRITE、NETWORK、STORAGE、ROM_RESOURCES を宣言し、ホストで許可を得ます。NETWORK は networkHosts も必要です。HTTP はリダイレクトせず、非 2xx は作者が処理します。本文は最大 256 KiB です。STORAGE は設定済み接続内のプラグイン専用領域にある小さな JSON のみを公開します。パスワード、任意パス、バイナリー転送、削除は提供しません。スクリプトの分離は独立した OS の保護境界ではないため、信頼できるコードだけを使用してください。

settings は TEXT、SECRET、BOOLEAN、NUMBER、CHOICE、DIRECTORY に対応し、値は文字列です。BOOLEAN の既定値は false。CHOICE は value と label を持ちます。DIRECTORY はホストが SAF 権限を保存し、ページから任意 URI を入力させません。SECRET はホストの認証情報管理を使います。設定は処理開始時に読み取ります。配布元リポジトリとプラグイン ID ごとに設定と専用 JSON を分離します。

独立設定ページは kind:CONFIGURATION と configurationPage を使用し、ホスト 0.9.96 が必要です。業務用 HTML は再利用できません。無効なプラグインも設定できます。設定ページが使えるのは ready、settings、data の読み書きと、STORAGE 宣言時のローカル接続一覧だけです。タスク実行、ライブラリ変更、リモートアクセスはできません。タイトル、戻る、ナビゲーション、権限、削除はホストが管理し、プラグインは内容だけを描画します。

library.games と records は最大 200 件のキーセットページングです。next をそのまま after に渡し、ページ番号や独自カーソルを作らないでください。records にメディア本文、パス、ハッシュはありません。編集も最大 200 件で、metadata.expected、recent.expected、メディアと拡張の expected によって競合を検査します。競合を表示して再取得し、無視や自動再試行をしないでください。apply は大きなゲームオブジェクトを返しません。checkpoint はそのバッチと同時に保存されますが、スクリプト全体が API をまたぐトランザクションになるわけではありません。

index.patch は現在のプラグインの名前空間だけを編集します。expected の省略は元の値が存在しないこと、value の省略は削除、明示的 null は保存する値を意味します。data.patch はトップレベルの null でキーを削除します。両者を混同しないでください。お気に入りは反転ではなく true/false を明示します。最近の記録の編集はゲームを起動しません。メディアは許可済みで索引にある素材だけを参照し、JSON で本文を転送しません。

storage.read は token と value を返し、文書がなければ null です。write は同じ処理内で直前に読んだ token と JSON オブジェクトを使い、最大 384 KiB です。アカウント、ディレクトリ、文書、処理をまたいで token を使わないでください。変更がなければ書き込みません。失敗を明示し、別の接続先や再試行キューへ切り替えないでください。

同じプラグインで同時に実行できる処理は一つです。ページから tasks.run で開始し、watch が返す関数で購読を解除します。ページ終了時に購読を解放しますが、バックグラウンド処理は継続できます。current で再接続し、成功後に result を取得します。キャンセルしても完了済みバッチは残ります。無効化や削除は対応処理を終了し、中断後に書き込みを自動再実行しません。終了時に分離実行環境と最後のエンジン接続を解放し、ページ終了時には WebView を破棄します。ゲーム起動はストアやスクリプトを待ちません。

メッセージは最大 512 KiB、SDK の同時要求は最大 4 件です。ページングとバッチを使い、結果を待ってください。Android WebView に必要な分離機能がない場合は更新を促し、別の実行方式へ変更しません。パッケージ、リソース、バージョンの規則はリンク先を参照します。ブラウザープレビューは正式 SDK とサンプルを使用し、ネイティブエンジンやクラウドの検証を代替しません。
