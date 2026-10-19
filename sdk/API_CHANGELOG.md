# API 变更说明 / API changelog / API 変更履歴

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Current inventory](api.json) · [Reference](API_REFERENCE.md) · [Version policy](API_VERSIONING.md) · [Product history](../CHANGELOG.md)

## 中文

### 1.0.0 · 2026-10-19

首次建立独立版本管理的公开 SDK 契约，对照宿主 0.9.108 的真实调用链，记录 32 个公开成员（30 个函数和 version/ready）。这不是在今天新增这些运行能力；运行时仍为 API 1，宿主与现有插件版本不变。

- 新增：逐接口三语签名、参数、默认值、返回、权限、上下文、错误条件和可执行示例；机器清单、不可改写的完整快照；CI 一致性与历史比较。
- 澄清：配置页白名单、后台 STORAGE 读写、一个插件一个活动任务、最近保留任务并非历史列表、显式 null 与省略字段、批量修改加 checkpoint 的原子范围、HTTP 状态与异常的区别。
- 兼容性与迁移：无运行接口新增、移除或弃用；既有插件无需修改。新作者按所用功能设置 minAppVersion；不增加新清单字段。
- 验证范围：对照实际宿主源码，清单与类型／运行时一致、三语链接和示例自动检查；不增加 Android、模拟器或真实网盘已通过的声明。

历史能力起点：0.9.90 基础脚本／页面与资料、收藏、媒体、任务、网络接口；0.9.91 轻量记录、apply/checkpoint 和 STORAGE；0.9.92 公共图标；0.9.94 作者语言环境；0.9.96 独立配置页；0.9.98 ROM 资源回调。此前记录未采用契约 semver，不补造旧契约版本或日期，产品变更继续见 Product history。

## English

### 1.0.0 · 2026-10-19

First independently versioned public SDK contract, checked against host 0.9.108's actual call paths, covering 32 public members (30 functions plus version/ready). These runtime features were not all introduced today. Runtime API remains 1; host and existing plugin versions are unchanged.

- Added: per-member trilingual signatures, arguments, defaults, results, grants, contexts, failure conditions and executable examples; machine inventory, immutable full snapshot, CI consistency and history comparison.
- Clarified: configuration-page allowlist, background-only STORAGE I/O, one active task per plugin, retained latest task versus history, explicit null versus omitted fields, atomic batch/checkpoint scope, HTTP statuses versus exceptions.
- Compatibility/migration: no runtime additions, removals or deprecations; existing plugins need no changes. New authors choose minAppVersion for their features; no new manifest field is required.
- Validation scope: actual host source review, inventory/type/runtime parity and automated trilingual links/examples. This adds no claim of Android, emulator or real-cloud acceptance.

Historical feature baselines: 0.9.90 basic scripts/pages and library, favorites, media, task and network APIs; 0.9.91 lightweight records, apply/checkpoint and STORAGE; 0.9.92 public icons; 0.9.94 author locale environment; 0.9.96 dedicated configuration pages; 0.9.98 ROM resource callbacks. Earlier records did not use contract semver: no older contract versions or dates are invented. Product history retains product changes.

## 日本語

### 1.0.0 · 2026-10-19

ホスト 0.9.108 の実際の呼び出し経路を確認し、独立して版管理する公開 SDK 契約を初めて記録しました。公開メンバーは 32 件（関数 30 件と version/ready）です。実行機能がすべて今日追加されたという意味ではありません。実行 API は 1 のままで、ホストと既存プラグインの版は変わりません。

- 追加：各メンバーの三言語シグネチャ、引数、既定値、戻り値、権限、実行場所、失敗条件、実行例。機械可読一覧、変更不可の完全なスナップショット、CI の一致検査と履歴比較。
- 明確化：設定ページの許可一覧、バックグラウンド専用 STORAGE、同時実行一件、最新タスクと履歴の違い、明示的 null と省略、バッチと checkpoint の原子性、HTTP 状態と例外の違い。
- 互換性・移行：実行 API の追加・削除・非推奨化はなく、既存プラグインの変更は不要です。新規開発では使用機能に応じて minAppVersion を選びます。新しいマニフェスト項目は不要です。
- 検証範囲：実ホストのソース確認、一覧・型・実行メンバーの一致、三言語のリンクと実行例の自動検査です。Android、エミュレーター、実クラウドでの検証済み範囲を拡大するものではありません。

機能の初出版：0.9.90 は基本スクリプト・ページと資料、お気に入り、メディア、タスク、ネットワーク、0.9.91 は軽量記録、apply/checkpoint、STORAGE、0.9.92 は公開アイコン、0.9.94 は作者の言語環境、0.9.96 は独立設定ページ、0.9.98 は ROM リソースコールバックです。過去は契約 semver を使っていないため、旧契約版や日付を作らず、製品の変更は Product history に残します。
