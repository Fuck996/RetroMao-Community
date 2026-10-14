# 复古猫语言贡献

每种语言独立维护一个 UTF-8 JSON 文件：`zh-Hans.json`、`zh-Hant.json`、`en.json`、`ja.json`。新增语言可添加 `fr.json`、`de.json`、`pt-BR.json` 等文件，不需要改其他语言。

当前为翻译准备基线，应用尚不支持语言包导入。简中包含 958 条玩家可见原文；繁中已按功能分批补齐 958 条，采用台湾常用 UI 用词，保持 draft 待复审。英语、日语仍为待译模板，null 明确表示未翻译。它们可下载、编辑和提交 PR，**不是已经可安装生效的语言包**。

## 如何贡献

1. Fork 仓库，在所需语言文件的 messages 中填译文。新增语言时复制现有待译模板，修改 locale、name 和文件名，保持 status=draft。locale 使用 BCP 47 的语言／脚本／地区形式，name 使用该语言自己的名称。
2. 对照 `zh-Hans.json` 的原句及实际应用界面。保留 key、数字参数和受保护名称；`%1$s` 等参数可调顺序，不可增删或改变类型。不把中文当作已完成译文，不为省事删除 null 条目。
3. 英语、日语按具体界面精简，保留动作、方向、状态及存档类型。不要自行改中文，也不要把原／新目录写成本机／云端；上下文不清楚的句子在 PR 中提出疑问。
4. 在仓库根目录运行 `python tools/validate_languages.py`，提交只包含所改语言的 PR，说明语言、译者和完成范围。CI 接受保留 null 的草稿，但拒绝重复／缺失／未知 key、参数错误、目录版本不兼容和受保护名称丢失。
5. 维护者审阅后标为 reviewed。新增语言和进度、大小、SHA-256 索引由维护者运行 `python tools/validate_languages.py --write-index` 生成；译者不手工修改 index.json。发布单语前用 `--require-complete --locale fr` 检查该语言的完整性与审阅状态，其他语言草稿不阻塞它。此检查只验证文本文件，不能证明 APK 已支持安装它。

保持 catalog_version、catalog_hash 不变，它们关联中文基线。新增功能时由维护者更新基线、补充 key，并重新审阅受影响译文；不能用旧文件静默覆盖新版本。公开仓库是后续译文的唯一维护来源，Android XML 为生成产物。

## 下载与使用规划

可在任意单语言文件页面点击 Raw 下载 JSON，或下载仓库 ZIP 进行编辑。当前草稿不进入应用现有“社区平台／主题”清单，不能用平台或主题导入入口安装。

语言包支持完成后，已审阅完整译文以版本化文件发布，玩家仅下载所需语言。导入时校验目录版本、基线摘要、全部 key 和参数，再保存到应用语言包目录；只保留匹配当前系统语言的一份译文在内存。系统语言仍是选择依据，不增加独立语言偏好。缺失／过期／不合法文件明确拒绝，不标记安装成功。

首次四语随 APK 内置以支持离线；其他语言可由社区 PR 提供并按需下载。中文、ROM、媒体／资料语言的独立规则不变。仅下载文件与应用支持导入是不同阶段。

## English contribution guide

Edit one JSON file per language. Translate messages using `zh-Hans.json` and the app's UI. Preserve keys, numbered placeholders and protected names. Leave unfinished entries as null and keep status=draft. For a new language, copy a draft template and change its locale, native name and filename. Run `python tools/validate_languages.py`, then submit a PR describing the locale and scope. Maintainers review translations and generate the index.

These are contribution templates. Language-pack import is not implemented in the app yet; downloading a draft does not install or activate it. Complete reviewed packs will be distributed separately once the runtime contract is ready.
