# 验证记录 / Validation record / 検証記録

## 中文

2026-10-19：公共开发链路完成本地验收。20 份既有及新增说明通过三语覆盖、代码块一致性和本地链接检查；本记录加入后同样纳入检查。Python 共 17 项通过，覆盖格式、缺失文件、确定性 ZIP、语言参数、平台共享用例、发布前置条件及远端资产回读失败不改目录。Node 共 22 项通过，覆盖正式 SDK、既有同步示例和预览权限、分页、原子编辑与错误。

浏览器使用显式选择的本机 Edge，既有两个同步页面通过 16:9、4:3、1:1 的触摸、焦点、进度和取消；独立预览另通过中英日、三比例、真实后台 Worker、平台和语言视图。CI 的默认浏览器仍是锁定 Playwright 对应的 Chromium，远端结果由 Actions 记录，不能用本机 Edge 结果冒充远端结果。

宿主提交 62c1267 完成原链路的声明式平台启动，5 项核心检查、平台 ZIP 安装恢复 1 项、导入配置 16 项、RetroArch 存档 13 项、启动 83 项合计 118 项通过，Debug lint 通过。应用页和系统桌面由另一个独立提交提供，本次未将其文件纳入提交。

本次没有发布演示插件或改写既有 Release。发布器的成功及失败路径用模拟外部命令验证；真实创建 Release 需要贡献者明确执行 publish 或手动工作流。正式 APK 由已协调的任务统一打包，真实模拟器和网盘设备验收仍需分别记录。预览服务、浏览器和临时脚本已结束并清理。

## English

2026-10-19: local acceptance of the public developer flow completed. Twenty existing/new documents passed trilingual coverage, executable-block parity and local-link checks; this record is also checked once added. All 17 Python tests passed, covering formats, missing files, deterministic ZIPs, language arguments, shared platform cases, publication preconditions and unchanged catalogs after failed asset readback. All 22 Node tests passed for the shipped SDK, existing sync examples and preview permissions, pagination, atomic edits and errors.

Browser checks explicitly used installed Edge. Both existing sync pages passed 16:9, 4:3 and 1:1 touch, focus, progress and cancellation checks. Independent preview also passed Chinese/English/Japanese, three ratios, the actual background Worker, and platform/language views. CI still defaults to the Chromium revision paired with pinned Playwright. Actions records remote results; local Edge results do not imply remote success.

Host commit 62c1267 adds declarative platform launchers through the existing flow. Five core checks, one platform ZIP/reopen check, 16 imported-configuration checks, 13 RetroArch save checks and 83 launch checks passed, totaling 118, together with Debug lint. Apps/Home features are a separate commit and their files were not included here.

No demonstration plugin was published and no existing Release was rewritten. Publisher success/failure paths were checked with mocked external commands. Real Release creation requires the contributor to invoke publish or the manual workflow. The coordinated task handles the formal APK; real emulator/cloud device acceptance must be recorded separately. Preview servers, browsers and temporary scripts were stopped and cleaned.

## 日本語

2026-10-19：公開開発フローのローカル検証を完了しました。既存・新規の 20 文書で三言語、実行コードの一致、ローカルリンクを確認し、本記録も追加後に検査します。Python の 17 件は形式、欠落ファイル、再現可能な ZIP、言語引数、共有プラットフォーム例、公開条件、アセット再取得失敗時の索引保持を確認しました。Node の 22 件は正式 SDK、既存同期例、プレビューの権限、ページング、バッチ編集、エラーを確認しました。

ブラウザーは既存の Edge を明示して使用しました。二つの同期ページで 16:9、4:3、1:1 のタッチ、焦点、進捗、キャンセルを確認しました。独立プレビューでも中国語・英語・日本語、三比率、実際のバックグラウンド Worker、プラットフォームと言語の表示が成功しました。CI の既定値は固定 Playwright に対応する Chromium です。リモート結果は Actions に記録し、ローカル Edge の成功をリモートの成功とは扱いません。

ホストのコミット 62c1267 は既存経路に宣言型の起動設定を追加します。コア 5 件、パック導入と再読込 1 件、インポート設定 16 件、RetroArch セーブ 13 件、起動 83 件の合計 118 件と Debug lint が成功しました。アプリページとホーム機能は別コミットで、本コミットにはそのファイルを含めていません。

デモ用プラグインの公開や既存 Release の変更は行っていません。公開ツールの成功と失敗は外部コマンドを模擬して検証しました。実際の Release 作成には投稿者による publish または手動ワークフローの実行が必要です。正式 APK は調整済みの別タスクが作成します。実エミュレーターとクラウドの端末検証は別途記録してください。プレビューサーバー、ブラウザー、一時スクリプトは終了・削除済みです。

[Host source / 宿主源码 / ホストソース](https://github.com/Fuck996/RetroMao/commit/62c1267) · [Reproduce / 复现 / 再現](TESTING.md)
