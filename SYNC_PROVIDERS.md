# 同步渠道边界 / Sync provider boundaries / 同期プロバイダーの境界

[中文](#中文) · [English](#english) · [日本語](#日本語)

[SDK](sdk/README.md) · [ROM resources](sdk/ROM_RESOURCES.md) · [Sync examples](examples/SYNC_EXAMPLES.md)

## 中文

宿主负责队列、并发预算、进度、取消、重试、恢复、本地与远端差异、冲突、索引、存档版本及最终提交。存储渠道只负责认证、稳定账号身份、连接能力、目录和文件操作、传输及真实回执；不接管游戏启动或另造存档同步器。

WebDAV 与百度为原生适配器。脚本 STORAGE 从 0.9.91 提供已配置渠道内本插件的小型 JSON 文档；ROM_RESOURCES 从 0.9.98 提供目录定位。脚本注册新存储渠道、任意二进制流和跨进程渠道桥接尚未公开，不能通过主题、语言、平台或 JSON 存储绕过。

沿用 RemoteClientRegistry、RemoteClient、RemoteTransferContext 的统一数据与失败语义。未知结果进入原任务恢复，不伪造成功；凭据不交给页面或记录日志。账号和根目录身份必须隔离，不能复用另一账号或来源的 token、缓存、队列。

不新增全盘扫描、逐文件远端哈希、上传前写探针或独立重试并发。有效摘要与本轮目录分页复用；只有未完成文件准备下载地址，无变化不传正文或提交索引。取消保留已确认进度，恢复不重传成功文件；同机本地检查可按既有流程复用，渠道的任务、索引和版本独立。原生渠道代码变更需要宿主工程，不能声称只改公共 JSON 就增加任意网盘。

## English

The host owns queues, concurrency budgets, progress, cancellation, retries, recovery, local/remote differences, conflicts, indexes, save versions and final commits. Storage providers own authentication, stable account identity, connection capabilities, directory/file operations, transfers and real receipts. They do not own game launch or create another save synchronizer.

WebDAV and Baidu use native adapters. Script STORAGE exposes small plugin JSON documents through configured providers from 0.9.91; ROM_RESOURCES provides directory resolution from 0.9.98. Script registration of new providers, arbitrary binary streams and cross-process bridges is not public. Do not bypass that boundary using themes, languages, platforms or JSON storage.

Reuse RemoteClientRegistry, RemoteClient and RemoteTransferContext data/failure semantics. Unknown outcomes enter existing task recovery, never fabricated success. Do not expose credentials to pages or logs. Isolate accounts and root identities; tokens, caches and queues cannot cross accounts or origins.

Do not add whole-device scans, per-file remote hashes, upload probes, or independent retry/concurrency loops. Reuse valid hashes and per-round directory pages. Prepare download URLs only for unfinished files; unchanged content needs no body transfer or index commit. Cancellation retains confirmed progress; recovery avoids retransmitting successes. Reuse local checks through existing flows while keeping provider tasks/indexes/versions independent. Native-provider changes require the host project; public JSON alone cannot add arbitrary cloud services.

## 日本語

ホストはキュー、同時実行予算、進捗、キャンセル、再試行、復旧、ローカルとリモートの差分、競合、索引、セーブの版、最終確定を管理します。ストレージ側は認証、安定したアカウント識別、接続機能、ディレクトリとファイル操作、転送、実際の応答を担当します。ゲーム起動や別のセーブ同期器は担当しません。

WebDAV と百度はネイティブアダプターを使います。スクリプトの STORAGE は 0.9.91 以降、設定済み接続内の小さな専用 JSON を扱い、ROM_RESOURCES は 0.9.98 以降にディレクトリを特定します。新しい接続先のスクリプト登録、任意のバイナリー転送、プロセス間ブリッジは未公開です。テーマ、言語、プラットフォーム、JSON ストレージで迂回しないでください。

RemoteClientRegistry、RemoteClient、RemoteTransferContext のデータと失敗の意味を再利用します。結果不明なら既存タスクの復旧へ進み、成功を捏造しません。認証情報をページやログに渡さないでください。アカウントとルートの識別情報を分離し、token、キャッシュ、キューを別のアカウントや配布元に流用しません。

全端末スキャン、ファイルごとのリモートハッシュ、アップロード前の書き込みテスト、独自の再試行や並列ループは追加しません。有効なハッシュと同一回のページ結果を再利用します。未完了ファイルだけのダウンロード URL を準備し、変更がなければ本文転送や索引更新をしません。キャンセル後も確認済み進捗を残し、復旧では成功済みファイルを再転送しません。既存のローカル検査を再利用しつつ、接続先のタスク、索引、版は分離します。ネイティブ接続先の変更にはホスト工程が必要であり、公開 JSON だけで任意のクラウドを追加できるとは説明しないでください。
