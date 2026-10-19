# 收藏与最近记录同步 / Favorites and recent sync / お気に入りと履歴の同期

[中文](#中文) · [English](#english) · [日本語](#日本語)

```text
python tools/build_sync_examples.py --release-tag sync-examples-1.0.4
node --test tools/test_sync_examples.cjs tools/test_script_sdk.cjs
```

[Published 1.0.4](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.4) · [SDK](../sdk/README.md)

## 中文

4NPC 的 org.retromao.favorites-sync 与 org.retromao.recent-sync 为独立插件，公开版 1.0.4，最低宿主 0.9.96。各自安装、启用、授权、配置和卸载。CONFIGURATION 页选择已配置网盘，业务页执行同步、展示进度、结果和取消；配置保存到原 data.destination，不复制配置。不会在游戏启动时自动运行。

只匹配同平台、逐字相同游戏名和完整 ROM 文件名集合；扩展名和大小写保留，忽略目录和集合顺序，不读 ROM、不比较哈希、不用本机 ID 跨端匹配。多 ROM 游戏仍只有一条远端记录，无法匹配的远端条目保留。

收藏首次合并双方收藏；之后用上次成功基线识别本机变化，本机未改则接受远端。同一记录两边都修改时当前发起端优先，明确取消状态防止被另一端恢复。最近记录取较新的游玩时间、较大的次数和时长，不累加，不承诺跨端总量；清空本机最近列表不清除远端历史。游戏期间并发变化由 expected 拒绝，用户下一次手动同步再合并。

每机种一份 JSON 位于应用根/plugins/<来源仓库或local>/<插件ID>/<机种ID>.json，最大 384 KiB。来源、账号、根目录和插件互相隔离，两端应使用同一安装来源。本机记录每页 200，每轮每机种读取一份文档，仅有变化时写一次。WebDAV 用条件写或原短锁；百度复用原目录分页、上传回执和额度，不额外探针，也不承诺跨端原子覆盖。收藏基线与每批本机修改原子提交；取消保留已完成批次。

清单位于各自目录，共同代码在 activity-sync-shared，打包时合并成独立 ZIP，因此不能直接打包未组装的 favorites-sync 目录。下方工具复用公共打包器，输出到 dist；测试不调用真实网盘。先在插件的已安装页导入 ZIP，再配置并启用，两端手动同步。旧 1.0.1／1.0.2／1.0.3 Release 保留，分别对应旧宿主能力；不可覆盖。实际原生引擎与真实网盘必须单独验收。

## English

4NPC's org.retromao.favorites-sync and org.retromao.recent-sync are independent plugins, published as 1.0.4 for host 0.9.96+. Install, enable, grant permissions, configure and uninstall each separately. CONFIGURATION selects an existing cloud connection; business pages run sync and show progress, results and cancellation. Settings stay in existing data.destination, without a duplicate configuration store. Game launch does not run them automatically.

Match only the same platform, exact title and complete ROM filename set. Preserve extensions/case, ignore directory/set order, never read ROMs, compare hashes or use local IDs across devices. Multi-ROM games still produce one remote record. Preserve unmatched remote records.

The first favorite sync merges both sides. Later syncs compare the last successful local baseline: unchanged local state accepts remote state; when both sides changed, the initiating device wins. Explicit removals prevent resurrection. Recent sync takes the newer time and larger count/duration, never sums them or promises cross-device totals. Clearing local recents does not erase remote history. expected rejects concurrent play updates; a later manual sync merges them.

One JSON per platform lives under the app root/plugins/<origin-or-local>/<pluginID>/<platformID>.json, up to 384 KiB. Separate origins, accounts, roots and plugins; both devices should use the same installation origin. Read local records in pages of 200 and one document per owned platform per round; write once only when changed. WebDAV uses conditional writes/existing short leases; Baidu reuses directory pages, receipts and budgets without extra probes or cross-device atomic-overwrite guarantees. Favorite baselines commit atomically with local batches. Cancellation retains completed batches.

Each plugin has its own manifest; shared code is in activity-sync-shared and is assembled into independent ZIPs. Do not package the unassembled favorites-sync directory directly. The tools below reuse the public builder and write dist; tests do not call real cloud services. Import under Installed Plugins, configure and enable, then manually sync both devices. Keep old 1.0.1/1.0.2/1.0.3 Releases for older host capabilities; never overwrite them. Native-engine and real-cloud acceptance remain separate.

## 日本語

4NPC の org.retromao.favorites-sync と org.retromao.recent-sync は独立したプラグインです。公開版は 1.0.4、最低ホストは 0.9.96 です。個別にインストール、有効化、権限許可、設定、削除を行います。CONFIGURATION ページは既存のクラウドを選択し、業務ページは同期、進捗、結果、キャンセルを扱います。設定は既存の data.destination に保持し、複製しません。ゲーム起動時には自動実行しません。

同じ機種、完全一致するゲーム名、完全な ROM ファイル名の集合だけを照合します。拡張子と大小文字は保持し、ディレクトリと集合順序は無視します。ROM の読み取り、ハッシュ比較、端末 ID による端末間照合は行いません。複数 ROM でも一つのリモート記録とし、一致しない記録を残します。

初回は両端のお気に入りを統合します。以後は最後の成功時のローカル基準と比較し、未変更ならリモートを採用し、両方が変更した場合は開始端末を優先します。解除を明示して再登録を防ぎます。最近の記録は新しい時刻、大きい回数と時間を採用し、加算や端末間合計は保証しません。ローカル履歴の消去はリモート履歴を消しません。プレイ中の変更は expected で拒否し、次の手動同期で統合します。

機種ごとの JSON をアプリルート/plugins/<origin-or-local>/<pluginID>/<platformID>.json に保存し、最大 384 KiB です。配布元、アカウント、ルート、プラグインは分離し、両端で同じ配布元を使用してください。ローカルは 200 件ずつ読み、毎回所有する機種ごとに一つの文書を読み取って、変更時だけ一度書き込みます。WebDAV は条件付き書き込みまたは既存の短いロック、百度は既存のページ結果、応答、予算を使います。追加の書き込み試験や端末間の原子的上書きは保証しません。お気に入りの基準とローカルのバッチを同時に保存し、キャンセル後も完了分は残します。

各プラグインのマニフェストと activity-sync-shared の共通コードを組み合わせ、独立 ZIP を作成します。未組み立ての favorites-sync を直接パックしないでください。下のツールは公開ビルダーを使い、dist に出力します。テストは実クラウドに接続しません。インストール済みページで ZIP を読み込み、設定して有効にし、両端で手動同期します。旧ホスト向けの 1.0.1／1.0.2／1.0.3 Release は残して上書きしません。ネイティブエンジンと実クラウドの検証は別途必要です。
