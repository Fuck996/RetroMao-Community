# ROM 资源提供者 / ROM resource providers / ROM リソースプロバイダー

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Types](retromao.d.ts) · [Vita3K example](../examples/vita3k-sync/README.md) · [Official Vita3K installation](https://github.com/Vita3K/Vita3K/blob/f0273e4cd9b860ea77c44c73d9f5c5b1ed5fa8ab/vita3k/interface.cpp) · [Official licenses](https://github.com/Vita3K/Vita3K/blob/f0273e4cd9b860ea77c44c73d9f5c5b1ed5fa8ab/vita3k/packages/src/license.cpp)

## 中文

最低宿主 0.9.98。插件只定位本次游戏的外部资源范围，上传、下载、进度、取消、恢复、哈希缓存和索引提交全部使用原 ROM 同步队列。不得传大文件正文、另选网盘或创建私有同步任务。

清单声明 ROM_RESOURCES、DIRECTORY 配置和 resourceProviders；每项提供 id、platformId、extensions、directorySetting、rootPaths、rootMarker、formatVersion:1。DIRECTORY 的系统授权由宿主持久保存，配置不要求先启用插件。路径相对定位后的存储根，禁止绝对路径、URI、空段与点段；rootPaths 中空字符串仅表示所选根本身。

通过 define 的 resources 注册同 ID 函数。输入 games 数组，每项 gameId、romNames；输出每项 gameId、key、paths，路径项含 path 和 required。必需目录缺失明确失败，可选目录不存在不创建文件任务。上传每次最多输入 100 个游戏，仅返回目录范围；宿主枚举并保存文件清单。下载直接使用远端索引，不重新运行解析脚本。纯资源插件不需要业务页面或手动动作。

自有库索引格式 13 保存 romResources，包含插件 ID、资源键、格式、文件及相对路径，不保存本机授权 URI。资源不会变成启动候选或刮削指纹。云端使用原 ROM 根下 .retromao/resources/<插件ID>/<资源键>/，共用索引和回执。未安装、禁用或未配置插件的终端保留扩展记录，仅执行原标题与媒体同步；不能把没有启用视为删除。

已解析范围保存到原任务检查点，恢复不重复运行解析函数。取消通过系统任务卡片处理，保留已确认的文件；禁用只停止新的解析，已解析文件传输仍属宿主任务。只枚举本次游戏范围、复用本轮 DocumentTree 与哈希缓存，不额外扫描全盘、逐文件取远端摘要或反复提交索引。游戏启动不运行解析或等待同步。

Vita3K 1.0.0 由 4NPC 提供，使用 .psvita 文件名中的标题 ID，定位 ux0/app、ux0/patch、ux0/addcont、ux0/license 的对应游戏，不处理其他游戏、存档、固件、配置或缓存。支持根本身、fs、vita、files/fs、files/vita，必须唯一定位 ux0。两端都需安装、启用并选择自己的授权目录；实际 Android 文档提供方、模拟器和网盘仍需双端验收。

## English

Requires host 0.9.98. The plugin locates external resources for the selected games. Uploads, downloads, progress, cancellation, recovery, hash caches and index commits use the existing ROM queue. Do not transfer large file bodies, select another cloud destination or create private sync jobs.

Declare ROM_RESOURCES, a DIRECTORY setting and resourceProviders. Each provider has id, platformId, extensions, directorySetting, rootPaths, rootMarker and formatVersion:1. The host persists system directory permission; configuration does not require enabling the plugin first. Paths are relative to the located storage root, without absolute paths, URIs, empty or dot segments. Only rootPaths may use an empty string for the selected root itself.

Register the matching ID in define.resources. Input is games containing gameId/romNames; output entries contain gameId, key and paths, each with path/required. Missing required directories fail; absent optional directories create no tasks. Upload resolution receives at most 100 games and returns directory ranges; the host enumerates and checkpoints files. Downloads use the remote index without rerunning the resolver. Resource-only plugins need no business page or manual action.

Library index format 13 stores romResources with plugin ID, resource key, format, files and relative paths, never local permission URIs. Resources do not become launch candidates or scraping identities. Cloud files use .retromao/resources/<pluginID>/<resourceKey>/ under the existing ROM root, sharing its index/receipts. Hosts without an installed/enabled/configured plugin preserve resource records and sync existing title/media data only; lack of enablement is not deletion.

Resolved ranges join existing task checkpoints; recovery does not rerun resolution. Cancel through the system task card, retaining confirmed files. Disabling prevents new resolution; already-resolved transfers remain host tasks. Enumerate only selected-game ranges and reuse per-round DocumentTree/hash caches. Do not scan the whole device, fetch remote hashes per file or repeatedly commit indexes. Game launch never runs or waits for resolution.

Vita3K 1.0.0 by 4NPC uses title IDs in .psvita names to locate matching ux0/app, ux0/patch, ux0/addcont and ux0/license content. It excludes other games, saves, firmware, configuration and caches. Supported roots are the selected root, fs, vita, files/fs and files/vita, with exactly one ux0. Both devices must install/enable the plugin and select their own authorized directories. Actual Android providers, emulator versions and cloud services require two-device acceptance.

## 日本語

ホスト 0.9.98 が必要です。プラグインは今回選択したゲームの外部リソース範囲だけを決めます。アップロード、ダウンロード、進捗、キャンセル、復旧、ハッシュキャッシュ、索引更新は既存の ROM キューを使います。大きな本文の転送、別クラウドの選択、専用同期タスクの作成は行いません。

ROM_RESOURCES、DIRECTORY 設定、resourceProviders を宣言します。各定義は id、platformId、extensions、directorySetting、rootPaths、rootMarker、formatVersion:1 を持ちます。システムのディレクトリ権限はホストが保存し、プラグインを有効にする前でも設定できます。パスは特定されたルートからの相対パスで、絶対パス、URI、空要素、ドット要素は禁止です。rootPaths の空文字列だけは選択ルート自体を表します。

define.resources に同じ ID の関数を登録します。入力は gameId と romNames を含む games、出力は gameId、key、paths で、各パスに path と required を指定します。必須ディレクトリがなければ失敗し、任意のものがなければタスクを作りません。アップロード時は最大 100 ゲームを受け取り、範囲だけを返します。ホストが列挙してチェックポイントに保存します。ダウンロードはリモート索引を使い、解析を再実行しません。リソース専用プラグインに業務ページや手動動作は不要です。

ライブラリ索引形式 13 の romResources にプラグイン ID、リソースキー、形式、ファイル、相対パスを保存し、ローカル権限 URI は保存しません。起動候補やスクレイピングの識別情報にはなりません。クラウド上は既存 ROM ルートの .retromao/resources/<pluginID>/<resourceKey>/ に置き、索引と確認記録を共有します。未インストール、無効、未設定の端末はリソース記録を保持し、従来のタイトルとメディアだけを同期します。無効状態を削除と見なしてはいけません。

解析済み範囲は既存チェックポイントに保存し、復旧時に再解析しません。キャンセルはシステムのタスクカードで行い、確認済みファイルを残します。無効化は新しい解析を停止しますが、解析済み転送はホストのタスクです。今回のゲーム範囲だけを列挙し、同一回の DocumentTree とハッシュキャッシュを再利用します。全端末スキャン、ファイルごとのリモートハッシュ取得、索引の反復更新は行いません。ゲーム起動は解析を実行せず、同期を待ちません。

4NPC の Vita3K 1.0.0 は .psvita 名のタイトル ID を使い、ux0/app、ux0/patch、ux0/addcont、ux0/license の該当内容を扱います。他のゲーム、セーブ、ファームウェア、設定、キャッシュは対象外です。選択ルート、fs、vita、files/fs、files/vita に対応し、ux0 を一意に特定する必要があります。両端末でインストール、有効化、各端末の権限付きディレクトリ設定が必要です。実際の Android プロバイダー、エミュレーター、クラウドは二端末で検証してください。
