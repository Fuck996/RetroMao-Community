# 复古猫语言贡献

每种语言独立维护一个 UTF-8、LF 换行的 JSON 文件：`zh-Hans.json`、`zh-Hant.json`、`en.json`、`ja.json`。新增语言可添加 `fr.json`、`de.json`、`pt-BR.json` 等文件，不需要改其他语言。仓库 `.gitattributes` 固定语言 JSON 的 LF 换行，大小与 SHA-256 按实际下载字节计算。

当前文案基线包含 1301 条消息，补齐插件、更新管理、手柄提示样式与 ROM 资源授权所需键；已有译文保持不变。英文、繁中、日语均已补齐，保留兼容的 draft 元数据。繁中采用台湾常用 UI 用詞；日语面向日本市场，短标签简洁，说明采用「です・ます」。null 明确表示未翻译。四语从 0.9.87 起随 APK 内置；内容完整并匹配应用文案版本的语言包即可安装，无人工审核步骤。

## 如何贡献

1. Fork 仓库，在所需语言文件的 messages 中填译文。新增语言时复制现有语言文件，将 messages 的值置为 null，修改 locale、name 和文件名，保持 status=draft。locale 使用 BCP 47 的语言／脚本／地区形式，name 使用该语言自己的名称。
2. 对照 `zh-Hans.json` 的原句及实际应用界面。保留 key、数字参数和受保护名称；`%1$s` 等参数可调顺序，不可增删或改变类型。不把中文当作已完成译文，不为省事删除 null 条目。
3. 英语、日语按具体界面精简，保留动作、方向、状态及存档类型。不要自行改中文，也不要把原／新目录写成本机／云端；上下文不清楚的句子在 PR 中提出疑问。
4. 修改一份语言文件后，在仓库根目录运行 `python tools/validate_languages.py --write-index`，再运行 `python tools/validate_languages.py`。PR 包含所改语言及生成的 index.json，说明语言、译者和完成范围。CI 接受保留 null 的草稿，但拒绝重复／缺失／未知 key、参数错误、目录版本不兼容、受保护名称丢失及索引与文件不一致。
5. 译文完整后重新生成索引，无需人工审核或更改 status；译者和维护者都不手工修改 index.json。发布单语前用 `--require-complete --locale fr` 检查该语言的完整性、署名与格式，其他语言草稿不阻塞它。安装验证使用支持本基线的 APK；0.9.88 起先通过设置首页右下角的仓库按钮配置地址，每行一个，再进入“设置 → 主题与显示 → 语言 → 下载语言”。

保持 catalog_version、catalog_hash 不变，它们关联中文基线。新增功能时由维护者更新基线、补充 key，并重新审阅受影响译文；不能用旧文件静默覆盖新版本。公开仓库是后续译文的唯一维护来源，Android XML 为生成产物。

## 下载与使用

英文短标签按界面语境使用：游戏库 Library、游戏资料 Metadata、游戏名称 Title、在线刮削 Scraping、媒体预览 Preview、存档同步 Save sync、网盘与 WebDAV Cloud and WebDAV。完整确认说明仍保留方向、状态、影响对象及存档类型，不把短标签机械套进整句。

日语按界面语境使用：游戏库「ライブラリ」、游戏名称「タイトル」、游戏资料「情報」、刮削「スクレイピング」、媒体预览「プレビュー」、存档同步「セーブ同期」、原生存档「ゲーム内セーブ」、即时存档「ステートセーブ」。动作与状态区分「再開」「再試行」「復元」；配置移除、实体文件删除和索引记录消除的影响不能混译。

可在任意单语言文件页面点击 Raw 下载 JSON，或下载仓库 ZIP 进行编辑。当前草稿不进入应用现有“社区平台／主题”清单，不能用平台或主题导入入口安装。

支持多语言的新 APK 在“设置 → 主题与显示 → 语言”中提供手动选择和“跟随系统”。未指定语言时依次匹配系统语言，没有匹配则显示简体中文。手动选择会保存，切回“跟随系统”后重新自动匹配。

简中、繁中、英语、日语随 APK 内置并可离线使用；其他语言按需下载。安装时核对大小、摘要、文案基线、完整性和参数，成功后保存到应用自己的语言目录；内存只加载当前使用的扩展。失败会显示原因并保留现有安装。语言设置仅改变应用界面，不改变 ROM、游戏资料或媒体的语言。

## English contribution guide

Edit one UTF-8 JSON file per language with LF line endings. Translate messages using `zh-Hans.json` and the app's UI. Preserve keys, numbered placeholders and protected names. Leave unfinished entries as null and keep status=draft. For a new language, copy an existing file, set its message values to null, and change its locale, native name and filename. Run `python tools/validate_languages.py --write-index`, then `python tools/validate_languages.py`. Include the generated index with the language file in your PR. No human review status is required; neither contributors nor maintainers edit index records by hand.

APK builds with multilingual support include Simplified Chinese, Traditional Chinese, English and Japanese. Choose a language or follow the system under Settings → Theme and display → Language. From 0.9.88, use the icon-only repository button at the bottom right of the Settings home screen to enter public GitHub URLs, one per line, including community forks. Then open Download languages; URLs are not entered on the language page. Complete packs matching the app's catalog can be installed without a human review step; unfinished packs remain available for contributions. Set `author` and preserve contributor attribution in `credits`.

## APK 语言扩展接入

当前 APK 文案基线为 1233 个键：在原有 1226 个键上增加 7 条多仓库设置文案。每个仓库只读取本目录的 `index.json`，安装时下载选中的单个语言文件，不需要完整克隆仓库。相同基线、语言和内容摘要的条目合并，其他内容分别列出；不会为了合并清单提前下载所有译稿。

`catalog_version` 当前仍为 `0.9.86`，它与 `catalog_hash` 共同标识文案兼容基线，不是 APK 的发布版本。APK 升级到 0.9.89 不要求修改这些字段或重新生成未变化的语言索引。

每份语言文件提供 `author` 作者署名和 `credits` 致谢名单。Fork 中由新的维护者修改译文时，请填写自己的署名并在 `credits` 中保留应有的原作者、译者贡献；应用中的来源仓库与作者分别展示。

用户可输入兼容的公开 GitHub 仓库地址。可安装的扩展应包含全部键、通过参数与保护词检查，无需设置 `status: reviewed`。`status` 保留旧格式元数据，下载不使用它判定是否可用。内置语言直接显示已安装。
