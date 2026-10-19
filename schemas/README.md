# 配置 Schema / Configuration schemas / 設定 Schema

[中文](#中文) · [English](#english) · [日本語](#日本語)



## 中文

plugin、platform、language、package 分别描述对应 JSON，采用 JSON Schema 2020-12。编辑器可自行关联这些本地 Schema 获得补全；不要把 $schema 字段塞进宿主清单，也不要提交个人编辑器配置。Schema 用于结构检查，命令行还会核对引用文件、跨字段关系、语言参数、素材尺寸和容量。

宿主版本事实在 contracts/host.json，语言基线只来自 languages/index.json。宿主维护者使用 export_community_contracts.py 从真实定义导出公共事实；贡献者无需宿主源码。新增平台与其他已安装包的冲突必须在设备安装验证，离线工具无法知道用户已安装的所有扩展。

## English

plugin, platform, language and package schemas describe the respective JSON files using JSON Schema 2020-12. Associate these local files in your editor for completion; do not insert $schema into host manifests or commit personal editor settings. Schemas check structure; CLI validation additionally checks file references, cross-field relationships, language arguments, image dimensions and size limits.

Host capabilities are in contracts/host.json; language baselines come only from languages/index.json. Host maintainers export public facts from actual definitions using export_community_contracts.py; contributors do not need host source. Conflicts with other installed extensions require device installation checks because offline tooling cannot know all user-installed packages.

## 日本語

plugin、platform、language、package は対応する JSON を JSON Schema 2020-12 で定義します。エディターでローカル Schema を関連付けると補完できます。ホストのマニフェストに $schema を追加したり、個人用のエディター設定をコミットしたりしないでください。Schema は構造を検査し、CLI は参照ファイル、フィールド間の関係、言語の引数、画像寸法、容量も確認します。

ホストの機能は contracts/host.json、言語基準は languages/index.json だけを正とします。ホストの担当者は export_community_contracts.py で実際の定義から公開情報を生成します。投稿者にホストのソースは不要です。オフラインのツールは利用者の全インストール済み拡張を把握できないため、それらとの競合は実機インストール時に確認してください。
