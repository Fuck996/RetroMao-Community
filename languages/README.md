# 语言贡献 / Language contributions / 言語の追加

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Language schema](../schemas/language.schema.json) · [Context](../contracts/message-context.json)

```text
python tools/retromao.py init language --id fr --name Français --author YourName
python tools/validate_languages.py --write-index
python tools/validate_languages.py
python tools/retromao.py preview languages/fr.json
python tools/validate_languages.py --require-complete --locale fr
```

## 中文

每种语言独立一个 UTF-8／LF JSON。用下方命令从当前中文基线创建法语模板；基线版本、摘要和键直接继承，不复制历史的抽取稿。messages 的 null 表示待译。修改已有语言时直接编辑对应 JSON，不重建模板。

catalog_version、catalog_hash 和全部 key 必须保持不变。以 index.json 为准，不把 APK 版本当成语言版本，也不在文档手写消息总数。author 为自己的署名，credits 保留原贡献者，name 使用语言自己的名称。locale 支持语言、可选脚本、可选地区，如 fr、pt-BR、zh-Hant。

对照中文与 contracts/message-context.json 中的 surfaces、owners、arguments 判断用途；空上下文表示尚未登记，不代表可以猜。保留 %1$s、%1$d 的数量和类型，可调整次序；百分号写 %%；不支持 ICU、无编号参数或新增格式指令。保留 ROM、WebDAV、RetroArch、ScreenScraper 等保护名称，不把中文留作“已完成译文”。句子应完整且符合实际动作、方向和影响对象。

先生成索引，再运行检查。草稿可保留 null 并进入 PR，但只有全部非空、参数正确、署名完整、基线与 APK 一致的语言才可安装。status 的 source／draft／reviewed 只是兼容元数据，下载不要求人工 reviewed。中文只能用 source，其他语言不能用 source。

语言直接提交 JSON 和生成索引，不使用 ZIP、平台或主题入口，也不需要 Release。安装入口是设置 → 主题与显示 → 语言 → 下载语言；先在设置首页的仓库入口加入 Fork 地址。内置语言可离线使用，跟随系统或手动选择；语言设置只影响应用界面，不改变 ROM 或资料语言。APK 的内置快照由宿主维护者从公开固定提交生成，普通翻译贡献不改 Android XML。

## English

Maintain one UTF-8/LF JSON file per language. The commands below create French from the current Chinese baseline, copying its version, hash and keys rather than a historical extraction draft. null messages are untranslated. Edit an existing language JSON directly instead of recreating it.

Preserve catalog_version, catalog_hash and every key. index.json is authoritative. Do not equate the APK version with the language baseline or hand-maintain counts in prose. Set your author name, preserve contributors in credits, and use the language's native name. Supported locale syntax is language, optional script, optional region, such as fr, pt-BR and zh-Hant.

Use Chinese source and surfaces, owners and arguments in contracts/message-context.json. Empty context means it has not been registered; do not guess. Preserve the count/type of %1$s and %1$d while allowing reordering. Write literal percent as %%. ICU, unnumbered placeholders and additional directives are unsupported. Preserve protected names such as ROM, WebDAV, RetroArch and ScreenScraper. Do not present untranslated Chinese as complete. Keep sentences faithful to the action, direction and affected object.

Generate the index, then run checks. Drafts with null may be contributed, but installation requires all messages, valid arguments, author attribution and an APK-compatible baseline. source/draft/reviewed are compatibility metadata; installation does not require human-reviewed status. Chinese uses source; other languages must not.

Commit JSON and the generated index directly. Do not use ZIPs, platform/theme import or Releases. Install under Settings → Theme & Display → Language → Download Languages after adding your fork through the Settings repository control. Built-in languages work offline, following the system or manual choice. The preference only changes app UI, not ROM or metadata languages. Host maintainers generate Android XML from a fixed public snapshot; normal translation contributions do not edit it.

## 日本語

言語ごとに UTF-8／LF の JSON を管理します。下のコマンドは現在の中国語基準からフランス語を作成し、バージョン、ハッシュ、キーを継承します。古い抽出稿は使いません。null は未翻訳です。既存言語はテンプレートを作り直さず、その JSON を編集してください。

catalog_version、catalog_hash、すべてのキーを保持します。index.json を正とし、APK のバージョンを言語基準と同一視したり、文書内で件数を手動管理したりしないでください。author に自分の名前を設定し、credits に元の貢献者を残します。name は対象言語の自称を使います。locale は言語、任意の文字体系、任意の地域で構成し、fr、pt-BR、zh-Hant などに対応します。

中国語原文と contracts/message-context.json の surfaces、owners、arguments を確認します。空のコンテキストは未登録を意味し、推測してよいという意味ではありません。%1$s と %1$d は数と型を維持し、順序だけ変更できます。パーセント記号は %% と書きます。ICU、番号なしの引数、追加の書式指定は未対応です。ROM、WebDAV、RetroArch、ScreenScraper などの保護名称を保持してください。未翻訳の中国語を完成扱いにせず、動作、方向、対象に合った完全な文にしてください。

索引を生成してから検査します。null を含む草稿も投稿できますが、インストールには全項目の翻訳、正しい引数、作者名、APK と一致する基準が必要です。source／draft／reviewed は互換性メタデータであり、人による reviewed 状態は不要です。中国語だけが source を使用し、他の言語は使用できません。

JSON と生成した索引を直接コミットします。ZIP、プラットフォームやテーマのインポート、Release は使いません。設定のリポジトリ項目に Fork を追加し、「設定 → テーマと表示 → 言語 → 言語をダウンロード」でインストールします。内蔵言語はオフラインで利用でき、システム追従または手動選択が可能です。設定が変えるのはアプリの UI だけで、ROM や資料の言語は変更しません。Android XML はホストの担当者が公開済みの固定スナップショットから生成します。通常の翻訳投稿では編集しません。
