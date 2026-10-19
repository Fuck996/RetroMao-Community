# 版本与公共图标 / Versions and icons / バージョンと共通アイコン

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Icons](runtime/icons/) · [Publishing](../docs/PUBLISHING.md)

[SDK API versioning / SDK 接口版本 / SDK API 版管理](API_VERSIONING.md) · [API changelog / 接口变更 / API 変更](API_CHANGELOG.md)

```javascript
await retromao.ready;
document.getElementById("icon").src = retromao.icons.url("star");
```

## 中文

version 是扩展版本，minAppVersion 是最低宿主版本，均为三段数字，按数值比较，1.10.0 大于 1.9.0。脚本、页面、翻译、权限、配置和素材变化都应递增扩展版本。既有 Release 标签与同版本 ZIP 不覆盖；目录每个 ID 维护一个当前版本，旧 Release 可以保留。

更新只针对同一来源仓库、同 ID、兼容且版本更高的包。首次安装及更新均确认。0.9.113 起在安装确认中一并授权所需能力，首次安装默认启用，同来源更新保留启停选择；较早宿主新增权限后需重新启用。同来源保留配置和数据，不同来源保持独立。跨来源替换清除当前任务和结果，避免另一作者读取旧输出；来源自己的配置可保留。运行中先结束或取消任务再替换。卸载不删除宿主收藏、记录、存档和索引字段；需要清除自己的字段时先通过公共接口执行。

0.9.92 起可用 iconName 或 icons.list/url；未知图标报错，不能自动换图掩盖配置错误。公共图标包括 plugin、star、history、sync、cloud、library、image、language、palette、gamepad、chart、settings，来自包内 SDK，不逐个联网。也可提供包内 icon PNG/WebP，已安装卡片优先使用它。许可应以素材随附授权为准。

## English

version belongs to the extension; minAppVersion is the minimum host version. Both use three numeric parts: 1.10.0 is newer than 1.9.0. Increment the extension version for scripts, pages, translations, permissions, settings or assets. Never overwrite published tags or same-version ZIPs. Catalogs keep one current version per ID; old Releases may remain.

Updates require the same origin/ID, compatibility and a higher version. Installation and updates require confirmation. From 0.9.113, confirmation also grants required capabilities and enables new installations; same-origin updates retain enabled/disabled choices. Older hosts require re-enabling after new permissions. Same-origin updates retain configuration/data; different origins stay separate. Switching origins clears current tasks/results to prevent another author reading old output, while origin-specific settings may remain. Finish/cancel running work before replacement. Uninstall does not remove host favorites, history, saves or index fields. Clear your own fields through the public API beforehand if needed.

From 0.9.92 use iconName or icons.list/url. Unknown names fail explicitly rather than silently changing icons. Names are plugin, star, history, sync, cloud, library, image, language, palette, gamepad, chart and settings. They are bundled with the SDK and need no individual network requests. You may provide a local PNG/WebP icon, preferred by installed cards. Follow the licenses supplied with each asset.

## 日本語

version は拡張、minAppVersion は必要なホストのバージョンです。どちらも三つの数値で比較し、1.10.0 は 1.9.0 より新しくなります。スクリプト、ページ、翻訳、権限、設定、素材を変更したら拡張のバージョンを上げます。公開済みのタグや同バージョンの ZIP は上書きしません。索引は ID ごとに現在の一つの版を保持し、旧 Release は残せます。

更新は同じ配布元と ID、互換性、より新しい版が条件です。インストールと更新は確認を伴います。0.9.113 以降は同時に必要な機能を許可して新規プラグインを有効化し、同じ配布元の更新は有効・無効を保持します。旧ホストでの追加権限には再有効化が必要です。同じ配布元の設定とデータは保持し、別の配布元とは分離します。配布元の変更時は現在のタスクと結果を消去し、別作者が過去の出力を読めないようにします。元の配布元の設定は保持できます。実行中のタスクは完了またはキャンセルしてから置き換えます。削除してもホストのお気に入り、履歴、セーブ、索引フィールドは消しません。必要なら削除前に公開 API で自分のフィールドを消してください。

0.9.92 以降は iconName または icons.list/url を使用します。不明な名前は明示的に失敗し、別のアイコンに置き換えません。名前は plugin、star、history、sync、cloud、library、image、language、palette、gamepad、chart、settings です。SDK に同梱され、個別の通信は不要です。パック内の PNG/WebP icon も使用でき、インストール済みカードではこちらが優先されます。各素材の付属ライセンスを確認してください。
