# 开发与验收 / Development and acceptance / 開発と検証

[中文](#中文) · [English](#english) · [日本語](#日本語)

[API inventory and history checks / 接口清单与历史检查 / API 一覧と履歴検査](../sdk/API_VERSIONING.md) · [Executable API examples / 可执行接口示例 / API 実行例](../sdk/API_REFERENCE.md)

```text
python tools/retromao.py check
python -m unittest discover -s tools -p "test_*.py"
npm test
npx playwright install chromium
npm run test:browser
python tools/retromao.py preview templates/plugin
python tools/retromao.py preview templates/platform
python tools/retromao.py preview languages/en.json
```

## 中文

环境为 Python 3.11+、Node.js 22+；依赖版本由 requirements-dev 和 package-lock 固定。可先创建并激活 Python 虚拟环境，再运行下方命令。中国大陆默认使用列出的国内镜像；浏览器测试默认使用 Playwright 对应 Chromium。浏览器二进制优先复用缓存；若使用本机 Edge，显式设置 RETROMAO_BROWSER_CHANNEL=msedge，不会在失败后自动切换。

check 验证语言与索引、JSON Schema、模板、示例、三语文档，以及 API 清单／完整类型签名／源码摘要／版本快照；Python 测试覆盖打包拒绝、摘要确定性、平台契约和预览路径；Node 测试覆盖正式 SDK、全部接口手册示例、同步算法与预览的错误边界。CI 在 Windows 和 Linux 运行检查，并对比变更前提交保护 API 历史；Linux 另运行浏览器测试。reports 留存浏览器证据，不写到仓库外。

preview 支持插件页面、平台启动配置表和语言原文／译文检索。插件使用正式 SDK 与真正的后台脚本 Worker，样本数据只在当前页面内存中存在。更换页面或重新打开会重置，不能用它证明宿主的持久化和恢复。可通过 --fixtures 指定样本文件；网络只按 URL 返回显式样本，绝不访问真实服务。未支持的 API 明确失败。

收尾至少验证 16:9、4:3、1:1，触摸、方向键、错误、空态和任务取消。发布前还须在对应宿主上导入 ZIP、启用授权、检查配置、更新及卸载；平台另验收扫描、模拟器版本、核心／固件依赖、启动和返回。真实网盘与多账号隔离只能在真实服务上验证。自动检查通过不能宣称这些外部链路通过。

终端 Ctrl+C 停止预览；自动测试在 finally 关闭浏览器、服务和 Worker。若浏览器未安装或缺依赖，应安装对应依赖或报告未完成，不跳过后宣称成功。多个宿主 Gradle 构建应串行；社区检查不启动 Gradle。

## English

Use Python 3.11+ and Node.js 22+. requirements-dev and package-lock pin dependencies. You can create and activate a Python virtual environment before running the commands below. The listed mainland-China mirrors are the defaults. Browser tests use the Chromium revision paired with Playwright. Reuse cached browsers first; to use installed Edge, explicitly set RETROMAO_BROWSER_CHANNEL=msedge. Failures do not trigger an automatic browser switch.

check validates languages/indexes, JSON Schemas, templates, examples, trilingual documents and API inventory/full signatures/source hashes/version snapshots. Python tests cover rejected packages, deterministic hashes, platform contracts and preview paths; Node tests cover the shipped SDK, every API reference snippet, sync algorithms and preview error boundaries. CI runs checks on Windows and Linux, compares the pre-change commit to protect API history, and runs browser tests on Linux. Browser evidence stays inside reports.

preview supports plugin pages, a platform-launcher table, and searchable source/translation text. Plugins use the shipped SDK and their actual background script in a Worker. Fixture state exists only in the current page's memory. Changing or reopening pages resets it; this cannot prove host persistence or recovery. Use --fixtures for another fixture file. Network requests only return explicit URL fixtures and never reach real services. Unsupported APIs fail explicitly.

Before release, verify 16:9, 4:3 and 1:1, touch, directional navigation, errors, empty states and task cancellation. On a compatible host, import the ZIP, enable permissions, check configuration, updates and uninstall. Platforms additionally need scanning, emulator-version, core/firmware-dependency, launch and return checks. Real-cloud behavior and account isolation require real services. Passing automation does not prove those external paths.

Ctrl+C stops preview. Automated tests close browsers, servers and Workers in finally blocks. Install missing browser dependencies or report the incomplete check; never skip it and claim success. Run host Gradle builds serially. Community checks do not start Gradle.

## 日本語

Python 3.11 以降と Node.js 22 以降を使用します。requirements-dev と package-lock で依存関係を固定しています。必要に応じて Python 仮想環境を作成して有効にし、下のコマンドを実行してください。中国本土向けの既定値は記載の国内ミラーです。ブラウザーテストは Playwright に対応する Chromium を使用します。まずキャッシュを再利用してください。既存の Edge を使用する場合は RETROMAO_BROWSER_CHANNEL=msedge を明示します。失敗時に別のブラウザーへ自動変更しません。

check は言語と索引、JSON Schema、テンプレート、サンプル、三言語文書、API 一覧・完全な型・ソースハッシュ・版スナップショットを検査します。Python テストは不正パッケージの拒否、ハッシュの再現性、プラットフォーム契約、プレビューパスを確認し、Node テストは正式 SDK、全 API 実行例、同期アルゴリズム、プレビューのエラー境界を確認します。CI は Windows と Linux で検査し、変更前コミットとの比較で API 履歴を保護します。Linux ではブラウザーテストも行い、証拠ファイルは reports 内に保存します。

preview はプラグインのページ、起動設定の一覧、原文と訳文の検索に対応します。正式 SDK と実際のバックグラウンドスクリプトを Worker で実行します。サンプル状態は現在のページのメモリーだけに保持され、ページの変更や再表示で初期化されます。ホストの永続化や復旧の証明には使えません。--fixtures で別のサンプルファイルを指定できます。通信は指定 URL のサンプルを返すだけで、実サービスには接続しません。未対応 API は明示的に失敗します。

公開前に 16:9、4:3、1:1、タッチ、方向キー、エラー、空状態、タスクのキャンセルを確認します。対応ホストへの ZIP インポート、権限の許可、設定、更新、アンインストールも必要です。プラットフォームではスキャン、エミュレーターのバージョン、コアやファームウェアの依存関係、起動と復帰も検証してください。実際のクラウド動作とアカウント分離は実サービスで確認します。自動テストの成功だけで、外部の処理も成功したとは判断できません。

Ctrl+C でプレビューを終了します。自動テストは finally でブラウザー、サーバー、Worker を閉じます。ブラウザーの依存関係が不足している場合はインストールするか、未完了と報告してください。スキップして成功としないでください。ホストの Gradle ビルドは直列で実行します。コミュニティの検査は Gradle を起動しません。
