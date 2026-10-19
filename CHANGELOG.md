# 更新记录 / Changelog / 更新履歴

[中文](#中文) · [English](#english) · [日本語](#日本語)

## 中文

### 插件卡片与简介 · 0.9.114 / Vita3K 1.0.1 · 2026-10-19

已安装和商店卡片统一高度，标题单行省略，描述固定三行区域内滚动且不显示滚动条；状态和可选操作不再撑高卡片，字号变化时统一适配。新增[插件文案规范](sdk/PLUGIN_PRESENTATION.md)：中日文标题／简介建议 16／48 字符，英文 32／96 字符，建议不作为新的安装限制。Vita3K 1.0.1 精简四语简介，脚本和同步协议不变，以新 Release 分发并保留 1.0.0。

### 插件安装默认启用 · 0.9.113 · 2026-10-19

商店下载和本地 ZIP 在核验实际清单后共用一次安装确认，显示最低／当前前端版本、所需能力和网络主机。确认安装即授权并默认启用；同来源更新保留已有启停选择和私有数据，取消不落库。新增能力在安装确认中一并展示，无需安装后再手动启用。四语更新安装说明，新增 1 条文案，共 1371 键。拼音插件保持已发布的 1.0.0，资产不变。

### 搜索增强与安装兼容性 · 0.9.112 · 2026-10-19

发布拼音首字母搜索插件 1.0.0，最低前端 0.9.112，使用离线简繁字典增强原游戏与应用搜索。SDK 1.1.0 追加 SEARCH 能力、清单回调与类型；原 API 1 的 32 个 RPC 签名不变。搜索只读取当前范围名称，沿用原隔离生命周期、排序和启动流程，准备及失败明确显示。插件安装弹窗显示最低／当前前端版本，版本不足禁止安装；默认桌面入口移入“主题与显示”。

四语新增 5 条文案，共 1370 键。社区完整检查、26 项 Python 和 58 项 Node 测试通过，包括真实拼音脚本、固定依赖摘要、简繁、多音字及可复现打包。厂商设备的 JavaScript 隔离仍需实机验收。

### 跨页面搜索文案 · 0.9.111 · 2026-10-19

新增通用搜索动作和游戏搜索的 5 条四语文案，共 1365 键。游戏搜索用于宿主的游戏库、最近游戏和收藏，范围说明保留页面、机种参数与 ROM 保护词；更新目录、摘要和调用上下文。公共 SDK 接口没有变更。

### 应用页语言资源 · 0.9.109 · 2026-10-19

新增应用页搜索、长按管理和置顶的 16 条简中、繁中、英语、日语文案，四语各 1360 键。保留既有译文，更新语言基线、摘要与调用上下文；SDK 契约及已发布插件资产不变。

### 公共 SDK 契约 1.0.1 · 2026-10-19

- 修正首次 CI 发现的 Windows 工作副本换行摘要差异，SDK 源码契约统一按 UTF-8/LF 校验；保留 1.0.0，新增 1.0.1 快照和三语说明。资产摘要仍按原始字节校验，运行接口不变。

### 公共 SDK 契约 1.0.0 · 2026-10-19

- 补齐 [32 个公开成员的调用手册](sdk/API_REFERENCE.md)与[接口导航](docs/INTERFACES.md)，包括参数、返回、权限、上下文、错误条件和示例，全部提供中英日三语。
- 建立 [API 版本规则](sdk/API_VERSIONING.md)、[接口变更说明](sdk/API_CHANGELOG.md)、机器清单和不可改写的版本快照；校验接入现有 check、Node 测试与 CI。
- 此次建立已有 API 的文档基线，不改宿主、插件版本、语言资源或已发布资产；实机验收边界不变。

本文记录与本仓库有关的主程序能力。本仓库现有 Release 继续分发平台／主题示例 ZIP，语言使用独立 JSON；这里不是主程序 APK 或存储插件 SDK 的下载目录。

### 0.9.108 · 2026-10-19

- 应用页正式显示系统提供的可启动应用，支持图标网格、名称／包名搜索、触摸和手柄启动，并在安装变化及返回前台时自动更新。应用入口默认显示，玩家明确关闭的设置继续生效。
- 支持在 Android 系统中选择复古猫作为默认桌面。设置首页提供实际状态和系统选择入口，保留更换桌面的入口；重复 Home 返回同一前端，作为默认桌面时根返回键不退出应用。
- 四语语言目录新增 8 条应用与桌面文案，共 1344 键；本次不修改插件包及公共插件接口。

### 0.9.107 · 2026-10-18

- 修复资源上传期间任务摘要并发更新，列表读取首段和后续分段来自不同版本、触发“数据库记录长度不一致”并闪退的问题。分页和选中批次的首段、长度及后续内容统一放在同一个数据库事务中读取。
- 沿用每批 32 条的摘要读取及原文件传输并发，不读取完整恢复载荷、不增加网盘请求；继承 0.9.106 的后台检查与批次文件数修复。Vita3K 插件继续使用 1.0.0。
- 25 项传输效率、并发大摘要、统计和 Vita3K 流程定向用例通过；真实设备上传仍待安装验收。

### 0.9.106 · 2026-10-18

- 修正已配置网盘映射后，后台游戏库检查因 ROM 大小或修改时间变化而读取完整 ROM、阻塞后续上传准备的问题。后台检查更新元数据并使旧摘要失效，内容哈希由原同步检查或上传准备按需计算。
- Vita3K 等插件资源尚未展开时，批次容量明确标为待统计，并显示真实文件活动等待原因；准备完成后，上传批次显示持久任务中本体、补丁等实际文件的传输计数。
- 增加插件资源准备诊断，记录启用数量、未配置跳过原因及实际展开文件数。60 项应用定向用例和实际 Vita3K 插件脚本检查通过；报告设备及真实网盘传输仍待安装验收。
- 本次为宿主修复，Vita3K 插件维持 1.0.0，语言资源与公共接口不变。

### 0.9.105 · 2026-10-18

- 本地替换 ROM 后允许直接启动，文件变大或变小不再要求重扫；共享给模拟器的文件大小取当前值，不写回同步快照。
- 后台更新普通 ROM 的大小与内容摘要，不再取消已选择的启动或启动动画；失效路径、依赖清单及实际生效的模拟器配置变化仍按原规则处理。资源同步继续独立核对内容差异和传输完整性。
- 85 项相关启动用例完成定向验证。本次不修改语言资源、插件包或公共接口。

### 0.9.104 · 2026-10-18

- 修复天马 PS2 索引导入时丢失 `bootPath={file.documenturi}` 语义的问题，保留天马定义的文档地址形式，使以太能够匹配自身游戏库并打开单游戏属性与设置。
- 已导入的 PS2 索引通过正常后台检查自动更新一次，保留游戏记录，无需清库、手动重导或补选目录，不增加 ROM 复制或哈希。
- 在 AYANEO Pocket S mini／Android 13 上覆盖安装验收，冷启动及同进程再次启动均恢复真实游戏编号、CRC 和设置选项。四语快照新增一条文档 URI 不受支持的提示，共 1336 键；本次不更新插件包或公共接口。

### 0.9.103 · 2026-10-18

- 修正 RetroArch 1.22 之前版本不支持 SAF 启动地址的问题：使用已授权 ROM 的真实存储路径启动；1.22 及更新版本继续使用原 SAF 流程。
- PS2 的红蓝以太配置新增“以太游戏目录（可选）”。选择与模拟器相同的游戏目录后，启动保留该目录的 SAF 地址形式，避免同一 ROM 从不同授权层级启动时无法匹配模拟器游戏库、游戏设置页空白。目录仅保存在本机模拟器配置中，不增加扫描、哈希或 ROM 复制。
- 162 项启动、导入配置及设置交互检查通过，设置页覆盖 16:9、4:3、1:1；实际模拟器运行与设置页恢复仍待设备安装验收。四语语言基线增加六条目录配置文案，共 1335 键；本次不更新插件包或公共接口。

### 0.9.102 · 2026-10-17

- 补齐仅在游戏条目中声明模拟器／核心的导入：同平台只有一种可用配置时，自动登记为平台默认；多种配置显示“通过索引导入设置”。设置页和实际启动使用同一套配置状态。
- 没有可用平台配置或已登记索引配置时，启动进入模拟器设置；旧集合默认正确服从玩家手动选择，明确的游戏覆盖继续独立。已有导入记录在原后台检查中补登记一次，不重新扫 ROM、计算哈希或改写游戏索引。
- 开发者诊断增加实际 RetroArch 版本、入口、核心与 ROM 参数及文件打开记录，便于核对设备上的启动行为。296 项相关回归通过；本次设备黑屏是否消除仍待安装验证。
- 本次不更新插件包、公共接口或语言资源契约。

### 0.9.101 · 2026-10-17

- 天马集合默认模拟器／核心与平台设置对齐，游戏单独声明的启动配置保留为游戏覆盖。同一平台继承不同集合默认时，显示“通过索引导入设置”，统一选择留空，各游戏按自己的索引配置启动；玩家可在原设置入口改设统一默认。
- 索引中的未知启动参数或本机不支持的模拟器／核心不阻止 ROM 和媒体导入。“其他街机”共用平台模拟器设置及 MAME、FBNEO 等核心列表。
- 修复平台默认为空时，即使游戏已有有效索引启动配置，也会报“默认模拟器设置已改变”的核对错误；该错误原本也影响 PS1 等非街机平台。243 项定向回归通过，涵盖导入、启动、核心存档关联及三种屏幕比例的设置操作，实际设备和模拟器运行仍待安装 APK 验收。
- 四语语言基线增加一条索引配置状态，共 1329 键；本次不更新插件安装包。

### 0.9.100 · 2026-10-16

- 存档同步任务开始时核对已保存的渠道目标目录与现有存档关联目录，不一致则先复用公共目录迁移流程，再继续原同步。旧版已修改目录、升级后直接同步的情况同样生效，无需重新改一次设置。
- 目录核对只读本地配置，不增加扫盘、文件哈希或网盘请求；搬迁保留集合及版本关系，不重新上传存档正文。同源已有迁移不重复创建，取消同步会暂停本次创建的未完成迁移；一个渠道目录错误不阻断另一个渠道。
- 31 项定向检查通过，覆盖升级后直接同步、再次同步不重复移动或上传、取消、暂停任务复用、渠道隔离及三比例任务卡片。真实设备搬迁仍待安装新 APK 验收；本次不更新插件安装包及语言契约。

### 0.9.99 · 2026-10-16

- 修改渠道存档目录时，迁移现有存档和索引并保留版本关系；修改复古猫根目录时，同时迁移 ROM、媒体、索引和插件数据目录。目录设置带出默认存档路径，用户仍可明确指定其他存档位置。
- 迁移复用前端后台传输调度及公共移动接口；百度批量提交，WebDAV 按目录 MOVE，按渠道成功结果确认，不逐文件计算或比较哈希，不重新上传正文，也不在正常完成后反复查询目录和回读索引。中断只接续未确认部分，目录依赖按批处理。
- 同一存档目录的多渠道后台核对复用本轮本机检查；有效哈希不重算，未变化的本机索引不反复写入。同步历史显示渠道及实际目标位置，旧记录保留原位置。
- 新增目录迁移任务卡片，支持暂停与继续；尚未搬动的失败或暂停任务可取消。沿用已通过的 125 项定向检查和三比例界面检查，实际网盘迁移仍待设备验收。本次不更新插件安装包。

### 0.9.98 · 2026-10-16

- 发布 [ROM 资源提供者接口](sdk/ROM_RESOURCES.md)及作者 4NPC 的 [Vita3K ROM 同步 1.0.0](https://github.com/Fuck996/RetroMao-Community/releases/tag/vita3k-sync-1.0.0)，最低宿主 0.9.98。插件只定位授权目录中的游戏资源，传输、进度、取消、恢复及索引继续使用宿主原流程；未使用插件的终端保持原有标题索引和媒体同步。
- Vita3K 插件只需选择目录，支持对应游戏本体、补丁、DLC 与许可；不处理存档、固件或模拟器配置，不扫描其他游戏。先发布并核对 ZIP，再加入商店；原两个同步插件仍为 1.0.4。
- 同一本机存档目录可分别配置百度网盘与 WebDAV，共享本机文件索引和同批扫描；渠道版本及任务独立，新建配置和 RetroArch 映射不串用其他渠道。
- 语言包作者移至仓库右侧；顶部菜单可在主题与显示中选择文字或图标，切换保持高度，游戏库沿用机种标识。
- 沿用已通过的定向回归与三比例页面检查；正式 APK 完成签名、16 KiB 对齐、Filament 保留规则、四 ABI、26 个 SDK 资源及 1304 键四语契约核对。实际 Vita3K、Android 脚本引擎、目录提供方与真实网盘双端同步仍待设备验收。

### 0.9.97 · 2026-10-16

- 插件配置、语言选择与下载语言接入主界面导航、页头和返回历史；插件配置与业务页继续分开。社区主题下载、社区平台下载及单机种媒体预览按用户确认保留特殊界面。
- 语言作者与名称同排，内置语言显示“已安装”；完整且匹配文案基线的语言包无需人工审核状态即可安装，沿用原格式、参数及下载校验。
- 游戏库、最近游戏及收藏长按封面直接进入多选并选中当前游戏；手柄菜单和原批次操作保留。
- 插件继续使用已发布的 1.0.4，安装包、商店索引和最低主程序版本不变。本次不调整同步流程。
- 沿用已通过的定向测试与三比例页面检查，正式 APK 已完成签名、16 KiB 对齐、Filament 保留规则、四 ABI、26 个 SDK 资源与 1300 键四语契约核对；实际 Android WebView 与真实网盘仍待设备验收。

### 0.9.96 · 2026-10-16

- 插件商店移除配置按钮，同版本显示“已安装”；首次安装和更新均先确认，再调用原下载与安装流程。本地 ZIP 只解压一次，取消保留旧版。
- 宿主统一管理插件配置界面的启用、权限与卸载；禁用时可配置。自定义 CONFIGURATION 页面与 BUSINESS 页面分开，配置只访问设置、私有数据及本机连接列表，不运行同步业务。
- 收藏同步、最近游戏记录同步 1.0.4 已[公开发布](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.4)并更新商店目录，最低主程序 0.9.96。沿用原网盘选择、数据和同步算法，旧版 Release 保留。
- 手柄与按键增加 Xbox、任天堂、PlayStation 提示样式，底栏、确认／返回与改键列表共用转换；保存模式，沿用原输入映射。
- 沿用已通过的 52 项 JVM 定向测试、7 项 SDK 测试、7 项发布工具测试，以及三比例页面检查。本轮完成 Release 构建与签名、对齐、Filament 保留规则、四 ABI、26 个 SDK 资源及 1300 键四语契约核对。实际 Android WebView 与真实网盘仍待设备验收。

### 0.9.95 · 2026-10-16

- 修正两个同步插件有自定义网盘配置却未声明配置入口的问题，增加可选 `configurationPage` 引用已声明页面。卡片依声明提供入口，仍不为无配置插件显示按钮。
- 两个同步插件 1.0.3 已[公开发布](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.3)，最低主程序 0.9.95，复用原网盘选择页面、私有数据、权限与页面生命周期；不增加配置副本，不修改同步流程。
- 定向验证 35 项通过：核心声明 4 项、安装／桥接 17 项、卡片／配置与三比例交互 8 项、发布工具 6 项。截图核对 16:9、4:3、1:1 的声明配置入口；无配置声明的示例不显示按钮。
- 正式 APK 0.9.95 已交付，签名、16 KiB 对齐、Filament 保留规则、四 ABI、包内 SDK 与四语契约检查通过。先发布插件 ZIP，再更新商店索引；旧版安装包和插件 Release 保留。

### 0.9.94 · 2026-10-16

- 合并条目首次安装优先公共仓库，更新固定使用已记录的实际下载仓库，保留各来源自己的 Release 下载信息。
- 本地 ZIP 替换增加确认，沿用一次解压与原安装事务；取消保留旧插件及其数据。首次加载时回收未登记的安装目录，无变化目录不重复落盘。
- 版本号与标题对齐，新版“更新”位于版本号左侧，卡片左下角“配置”直接使用公共配置弹窗，原打开入口保持不变。
- 本次相关测试 52 项通过：核心规则 13 项、安装／下载／宿主和界面 27 项、SDK 7 项、发布工具 5 项。包含一次下载与实际来源保留、三比例卡片交互、多语言回退和配置键不变。正式 APK 已交付，签名、16 KiB 对齐、Filament 保留规则、四 ABI 与包内 SDK／语言契约检查通过。
- 增加插件作者维护的多语言清单、商店文字和页面／脚本语言环境，明确插件默认语言与简中必备项；两个同步示例 1.0.2 已[公开发布](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.2)并更新商店目录，最低主程序为 0.9.94，已发布 1.0.1 资产保持不变。

### 同步插件 1.0.1 · 2026-10-16

- 作者 4NPC 的收藏同步、最近游戏记录同步已公开发布，并加入 `plugins/index.json`。兼容现有 0.9.91，保留包内图标。
- 同步公开 SDK、示例源码和 12 个公共图标。已核对公开 ZIP 的匿名下载、大小、SHA-256 和清单。
- 0.9.92 起增加独立版本徽标、同来源新版提示、安装确认和公共图标调用；配置、私有数据与新增权限沿用原升级规则。0.9.93 补齐仓库源变更后的目录失效。

### 0.9.91 · 2026-10-15

- 提供作者 4NPC 的[收藏同步与最近游戏记录同步](examples/SYNC_EXAMPLES.md)两个独立脚本示例，通过公共接口使用已配置的网盘；ZIP 分别安装、启停和配置，商店 Release 尚未发布。
- 同机种按游戏名与完整 ROM 文件名集合匹配，多 ROM 作为一个游戏，不读取 ROM 正文或比较文件 MD5。收藏传播新增与取消；最近记录保留较新时间，次数与时长取较大值，不重复累加。
- 增加受授权的 `STORAGE` 桥接和轻量游戏记录分页，复用原渠道客户端、请求额度及目录缓存；无变化不上传，本机收藏基线与每批修改原子提交。
- 相关合并、公共接口、渠道和三比例页面测试通过。正式 APK 已通过签名、对齐、Filament 保留规则、四 ABI、SDK 与 1286 键四语契约检查，签名与 0.9.90 一致；原生脚本引擎和实际网盘验收仍待完成。

### 0.9.90 · 2026-10-15

- 主菜单增加可开关的“插件”入口，提供“已安装”“商店”、启停卸载、插件配置与自定义业务页面。
- JavaScript 动作和 HTML 页面调用同一套公共资料、媒体引用、收藏、最近记录与索引扩展接口；安装复用现有多仓库下载，任务使用 WorkManager，不等待或阻止游戏启动。
- 提供 [SDK 与本地示例](sdk/README.md)。官方脚本示例尚未发布 Release，商店目录暂为空；存储渠道脚本注册和流式文件桥接仍待后续接入。
- APK 内置四语新增 52 条插件文案。新增译文尚待同步到公开翻译维护源；原生脚本引擎和 WebView 的设备验收尚未完成。
- 正式 APK 已通过签名、对齐、Filament 保留规则及包内 SDK／语言资源检查，签名与 0.9.89 一致。

### 0.9.89 · 2026-10-15

- 统一宿主内的任务与传输公共流程，将渠道存储操作独立为适配模块；渠道选择、连接参数输入和事件使用公共界面。
- 删除自动和手动写入测试；上传失败直接处理真实操作错误。
- 恢复 ROM、媒体或存档下载时，完整暂存文件不再重新获取远端下载地址。
- 公开[同步渠道职责与效率约束](SYNC_PROVIDERS.md)。独立插件 SDK 和安装桥接尚未发布。

本次公共仓库维护只更新说明，语言 JSON、索引及已发布示例 ZIP 不变。

### 0.9.88 · 2026-10-15

- 设置首页右下角提供无文字仓库按钮，每行配置一个公开 GitHub 仓库。
- 语言、社区主题与平台共用多仓库配置；同身份同内容合并，其他内容分别列出。
- 语言下载弹窗不再设置仓库地址。四语文案基线增加至 1233 条。

### 0.9.87 · 2026-10-15

- APK 内置简中、繁中、英语、日语，首次匹配系统语言，无匹配时显示简中；显示设置支持手动选择。
- 支持从官方或社区 Fork 仓库下载兼容且完整的 reviewed 语言扩展，展示作者署名。
- 各语言独立维护一个 JSON；内置译稿保留 source／draft 状态，未标为母语人工审阅完成。

### packs-2026-10-06

首批 MSX 平台和琥珀主题示例，最低主程序版本 0.9.44。原始三语发布说明见 [RELEASE_NOTES.md](RELEASE_NOTES.md)。

## English

### Plugin cards and summaries · 0.9.114 / Vita3K 1.0.1 · 2026-10-19

Installed/store cards share equal height, one-line title ellipsis and a three-line scrolling description without a scrollbar. Status and optional controls no longer enlarge cards; font scaling adjusts all cards together. New [copy guidelines](sdk/PLUGIN_PRESENTATION.md) recommend title/summary lengths of 16/48 characters for Chinese/Japanese and 32/96 for English, without introducing installation limits. Vita3K 1.0.1 shortens all four summaries; scripts and sync protocol remain unchanged, distributed as a new Release preserving 1.0.0.

### Plugins enabled on installation · 0.9.113 · 2026-10-19

Store downloads and ZIP imports share one confirmation after validating the actual manifest, showing required/current host versions, capabilities and network hosts. Confirmation grants capabilities and enables new installations; same-source updates preserve the existing enabled/disabled choice and private data. Cancellation registers nothing. Newly requested capabilities appear in the same confirmation, without a separate post-install enable step. Installation copy is updated in four languages, adding one key for 1371 total. The published pinyin plugin and its 1.0.0 asset remain unchanged.

### Search enhancement and installation compatibility · 0.9.112 · 2026-10-19

Pinyin initials search 1.0.0 requires host 0.9.112 and enhances existing game/app search using offline simplified/traditional dictionaries. SDK 1.1.0 adds SEARCH grants, a manifest callback and types; all 32 existing API 1 RPC signatures remain unchanged. Only current-scope names are supplied, with existing isolation, ordering and launch paths, and explicit preparation/failure states. Install dialogs display required/current frontend versions and block incompatible installation. Default-home settings move into Theme and display.

Five messages were added in all four languages, for 1370 keys each. Complete repository checks, 26 Python tests and 58 Node tests pass, including the real pinyin script, pinned dependency hashes, polyphones and reproducible packaging. Vendor-device JavaScript isolation still needs device acceptance.

### Cross-page search messages · 0.9.111 · 2026-10-19

Added five messages in all four languages for the shared search action and game search, bringing the total to 1365 keys. Game search serves the host library, recent games and favorites. Scope labels preserve page/platform arguments and the protected ROM term. Catalog metadata, hashes and call context are updated; public SDK APIs are unchanged.

### App-page language resources · 0.9.109 · 2026-10-19

Added 16 messages for app search, context management and pinning in Simplified Chinese, Traditional Chinese, English and Japanese, now 1360 keys per locale. Existing translations are preserved; the language baseline, hashes and call context are updated. SDK contracts and published plugin assets are unchanged.

### Public SDK contract 1.0.1 · 2026-10-19

- Fixed the Windows worktree newline digest mismatch found by initial CI. SDK source contracts now use UTF-8/LF; 1.0.0 is preserved alongside a new 1.0.1 snapshot and trilingual notes. Asset digests still use raw bytes; runtime APIs are unchanged.

### Public SDK contract 1.0.0 · 2026-10-19

- Added a [32-member API reference](sdk/API_REFERENCE.md) and [interface map](docs/INTERFACES.md) with arguments, results, grants, contexts, failures and examples in Chinese, English and Japanese.
- Established [API versioning](sdk/API_VERSIONING.md), [API changes](sdk/API_CHANGELOG.md), machine inventory and immutable snapshots, integrated into check, Node tests and CI.
- This documents existing APIs without changing host/plugin versions, language resources or published assets. Device acceptance boundaries remain unchanged.

This records host capabilities relevant to this repository. Existing Releases distribute platform/theme examples, while languages use JSON. This is not an APK or storage-provider SDK download directory. Entries describe their historical state; current contracts take precedence for development.

### 0.9.108 · 2026-10-19

The Apps page lists system-launchable apps in an icon grid, supports name/package search, touch and controller launch, and updates after installation changes or foreground resume. It is visible by default while preserving an explicitly disabled preference. Android can select RetroMao as the default Home app. Settings show the actual role and system selector, preserve a way to change Home, and repeated Home returns to the existing frontend. Root Back does not exit when it is the default Home app. Eight messages were added across four languages, for 1344 keys. This host change did not update plugin ZIPs or public plugin APIs.

### 0.9.107 · 2026-10-18

Concurrent upload-summary updates could mix first/later chunks from different versions and crash with a database-record-length mismatch. Paginated and selected-batch reads now load the first chunk, length and remaining chunks in one transaction. Existing batches of 32 and transfer concurrency remain, without full recovery-payload reads or additional cloud requests. The 0.9.106 checks/count fixes remain; Vita3K stays at 1.0.0. Twenty-five targeted efficiency, large-summary concurrency, statistics and Vita3K checks passed; real-device uploads still needed acceptance.

### 0.9.106 · 2026-10-18

Background library checks with cloud mappings no longer read entire ordinary ROMs after size/time changes and block upload preparation. They update metadata and invalidate cached hashes; existing sync/preparation computes content hashes on demand. Batch size stays pending until plugin resources are expanded, with actual waiting reasons and persisted base/patch file counts afterward. Diagnostics record enabled providers, unconfigured skips and expanded files. Sixty targeted app checks and the actual Vita3K script passed; device/cloud acceptance remained. Vita3K stayed 1.0.0 and languages/APIs were unchanged.

### 0.9.105 · 2026-10-18

Locally replaced ROMs can launch immediately regardless of size change, using the current file size without changing sync snapshots. Background metadata/hash updates no longer cancel selected launches or animations. Invalid paths, dependencies and effective emulator changes still follow existing checks; resource sync independently verifies content and integrity. Eighty-five launch checks passed. No language, plugin-package or API change.

### 0.9.104 · 2026-10-18

Pegasus PS2 import now retains bootPath={file.documenturi}, allowing AetherSX2 to match its own library and game settings. Existing indexes receive one normal background update without clearing/reimporting the library, reselecting directories, copying ROMs or hashing again. Over-install acceptance on AYANEO Pocket S mini/Android 13 confirmed actual IDs, CRC and settings after cold and repeated launches. One unsupported-document-URI message increased the four-language snapshot to 1336 keys. No plugin/API change.

### 0.9.103 · 2026-10-18

RetroArch before 1.22 uses the authorized ROM's native path because it lacks SAF launch support; 1.22+ keeps SAF. Optional AetherSX2 game-directory configuration preserves the emulator's own SAF URI hierarchy, avoiding unmatched games and empty settings. It stays local, without scans, hashes or copies. The 162 launch/import/settings checks passed, including 16:9, 4:3 and 1:1; actual emulator/settings recovery awaited device acceptance. Six messages brought the language baseline to 1335. No plugin/API change.

### 0.9.102 · 2026-10-17

Game-only imported launch declarations now register a unique supported platform default or display imported-index configuration when mixed. Settings and launch share state. Without a platform/imported selection, launching opens emulator settings. Explicit per-game overrides remain; old collection defaults obey manual choices. Background recovery registers old imports once without rescanning/hashing ROMs or rewriting indexes. Diagnostics include RetroArch version, Activity, core, ROM arguments and file opens. The 296 related checks passed; the device black-screen report still required installation verification. No package/API/language-contract change.

### 0.9.101 · 2026-10-17

Pegasus collection defaults align with platform settings while explicit game declarations remain overrides. Mixed collection defaults show imported settings instead of one platform default; users can choose a unified default. Unknown parameters or unsupported emulator/cores do not block ROM/media import. Other Arcade shares platform emulator and MAME/FBNEO core settings. A null platform default no longer falsely reports that a valid per-game imported configuration changed, including PS1. The 243 targeted import/launch/core-save/settings checks passed across three ratios; device/emulator acceptance remained. One status message brought languages to 1329 keys; no plugin ZIP update.

### 0.9.100 · 2026-10-16

Save sync first compares the stored provider destination with current save associations and reuses directory migration before continuing, including upgraded configurations without re-editing settings. Comparison is local, with no scans/hashes/cloud requests. Migration preserves collections/versions without re-uploading bodies, avoids duplicate moves and pauses newly created migrations on sync cancellation. A bad destination does not block another provider. Thirty-one targeted upgrade/reuse/cancel/pause/isolation/card checks passed. Device migration still needed acceptance; plugin ZIPs/language contracts were unchanged.

### 0.9.99 · 2026-10-16

Changing provider save directories migrates saves/indexes with version history. Changing the app root also migrates ROMs, media, indexes and plugin data. Default save paths follow the root while explicit alternatives remain possible. Existing background scheduling and move APIs handle Baidu batches/WebDAV directory MOVE, confirming actual success without per-file hashes, body re-uploads or repeated completed directory/index reads. Recovery continues unconfirmed parts with batched dependencies. Same-local-directory checks/cache are reused; provider histories show actual destinations while old records retain theirs. Migration cards support pause/resume and cancellation before movement. The 125 prior targeted and three-ratio checks remained valid; real-cloud migration awaited acceptance. No plugin ZIP update.

### 0.9.98 · 2026-10-16

Published the ROM-resource API and 4NPC's Vita3K ROM sync 1.0.0 for host 0.9.98. Plugins locate selected-game resources; host transfers, progress, cancellation, recovery and indexes remain. Nonparticipating devices retain title/media sync. Vita3K only needs a directory for base content, patches, DLC and licenses, excluding saves, firmware, configuration and other games. ZIP publication and verification preceded its store entry; other sync plugins stayed 1.0.4. One local save directory can map to independent Baidu/WebDAV providers with shared local scanning but isolated versions/tasks. Language authors moved beside repository information; top-menu text/icon styles preserve height. Targeted/three-ratio checks remained valid. Signed APK, 16 KiB alignment, Filament rules, four ABIs, 26 SDK resources and 1304 four-language keys were checked. Actual Vita3K, native engine, providers and two-device cloud sync still needed acceptance.

### 0.9.97 · 2026-10-16

Plugin configuration and language selection/download use host navigation, headers and back history. Configuration/business pages remain distinct; selected community download/model-preview pages keep their special UI. Language authors share the name row, built-ins show installed, and complete compatible packs no longer require human-reviewed status. Long-pressing library/recent/favorite covers enters multiselect and selects that game; controller menus/batches remain. Plugins stay at 1.0.4 with unchanged ZIPs/catalog/minimum host and sync. Existing targeted/three-ratio checks remained valid. Signed APK, 16 KiB alignment, Filament rules, four ABIs, 26 SDK resources and 1300 language keys were checked. Native WebView/cloud acceptance remained.

### 0.9.96 · 2026-10-16

The store no longer configures plugins; same versions show installed. Installation/update confirmation comes before download. Local ZIPs extract once; cancellation retains the previous version. The host owns enablement, grants and uninstall, with configuration allowed while disabled. CONFIGURATION is separate from BUSINESS and only accesses settings/private data/local connection lists. Favorites/recent 1.0.4 was published/cataloged for host 0.9.96, preserving destinations, data and algorithms and keeping old Releases. Xbox/Nintendo/PlayStation prompts share the saved layout conversion without changing mappings. Prior 52 JVM, seven SDK and seven publishing checks plus three-ratio acceptance remained valid. Release build/signing, alignment, Filament rules, four ABIs, 26 SDK resources and 1300 language keys passed. Native WebView/cloud acceptance remained.

### 0.9.95 · 2026-10-16

Optional configurationPage links declared pages, fixing the sync examples' missing entry without showing configuration for plugins that declare none. Sync 1.0.3 was published for host 0.9.95, reusing destination UI, data, grants and lifecycle without sync changes. Thirty-five targeted checks passed: four core, 17 install/bridge, eight card/configuration/three-ratio and six publishing. The signed 0.9.95 APK was delivered and alignment, Filament, ABIs, SDK/languages verified. Publish ZIPs before catalogs; old APKs/Releases remain.

### 0.9.94 · 2026-10-16

Merged entries initially prefer the public origin; updates stay with their recorded actual repository/download information. Local replacement confirmation reuses one extraction and the install transaction; cancellation retains prior data. Unregistered directories are collected on first load, unchanged catalogs are not rewritten. Version/update labels align with titles and the configuration entry uses the host dialog while preserving open behavior. Fifty-two checks passed: 13 core, 27 install/download/host/UI, seven SDK and five publishing, including single-download origins, three ratios, locale defaults and stable setting keys. The signed APK and alignment/Filament/ABI/SDK/language checks passed. Author-managed localization introduced explicit default locale and required Chinese. Sync 1.0.2 was published/cataloged for 0.9.94 without changing 1.0.1 assets.

### Sync plugins 1.0.1 · 2026-10-16

4NPC's independent favorites/recent plugins were published and added to plugins/index.json for host 0.9.91, retaining local icons. SDK/examples and 12 common icons were synchronized; anonymous ZIP download, size, hash and manifest were verified. Host 0.9.92 added version badges, same-origin update prompts, install confirmation and common icons with existing configuration/data/new-permission semantics. Host 0.9.93 invalidated catalogs after repository changes.

### 0.9.91 · 2026-10-15

Independent 4NPC favorites/recent examples use configured clouds through public APIs; ZIPs install/enable/configure separately, with no store Release yet at that time. Matching uses exact platform/title/full ROM filename sets, one record for multi-ROM games, without ROM bodies or MD5. Favorites propagate additions/removals; recents take newer time and maximum count/duration without summing. Authorized STORAGE and lightweight pagination reuse clients/budgets/directory cache, avoid unchanged uploads, and atomically commit favorite baselines with local batches. Merge/API/provider/three-ratio checks passed. Signed APK, alignment, Filament, four ABIs, SDK and 1286 language keys passed with the 0.9.90 signature. Native-engine/cloud acceptance remained.

### 0.9.90 · 2026-10-15

The optional Plugins menu introduced Installed/Store, enable/uninstall, configuration and custom pages. JS actions and HTML share public metadata/media-reference/favorite/recent/index APIs, multi-repository installation and WorkManager without blocking game launch. SDK/local examples were available but store Releases were not yet published; script-provider registration and streaming remained future work. Fifty-two plugin messages were added; public translation synchronization and native-engine/WebView device acceptance remained. Signed APK, alignment, Filament and bundled SDK/languages passed with the 0.9.89 signature.

### 0.9.89 · 2026-10-15

Host task/transfer flows and provider adapters were unified, with common provider/configuration UI/events. Automatic/manual write probes were removed and actual upload errors retained. Complete staged ROM/media/save downloads no longer reacquire URLs. Provider responsibilities/efficiency boundaries were published, without a separate provider SDK/install bridge yet. That repository maintenance changed documentation only, not language JSON/indexes or published example ZIPs.

### 0.9.88 · 2026-10-15

An icon-only Settings repository control accepts one public GitHub repository per line. Languages/themes/platforms share sources; identical identities/content merge and differences remain separate. Language dialogs no longer edit repository URLs. Four-language messages reached 1233.

### 0.9.87 · 2026-10-15

Built-in Simplified/Traditional Chinese, English and Japanese follow system languages or manual choice, defaulting to Simplified Chinese. At that historical stage, downloadable compatible complete reviewed extensions showed authors. Each language used independent JSON; built-in source/draft metadata did not claim native human review. The reviewed installation requirement was removed in 0.9.97.

### packs-2026-10-06

First MSX/platform and Amber/theme examples required host 0.9.44. Original trilingual release notes remain in RELEASE_NOTES.md.

## 日本語

### プラグインカードと説明 · 0.9.114 / Vita3K 1.0.1 · 2026-10-19

一覧とストアのカードを同じ高さにし、タイトルは一行省略、説明は三行分の領域内でスクロールし、スクロールバーは表示しません。状態や追加操作で高さを変えず、文字拡大時も一緒に調整します。[文言規約](sdk/PLUGIN_PRESENTATION.md)では中国語・日本語のタイトル／説明を 16／48 文字、英語を 32／96 文字以内で推奨し、新しいインストール制限にはしません。Vita3K 1.0.1 は四言語の説明だけを短縮し、スクリプトと同期契約を保持します。1.0.0 を上書きせず新規公開します。
### インストール時の自動有効化 · 0.9.113 · 2026-10-19

ストアと ZIP は実際のマニフェストを検証してから一回の確認を共用し、最低・現在のホスト版、必要な機能、通信先を表示します。確認で許可し、新規プラグインを自動で有効にします。同じ配布元の更新は従来の有効・無効の選択と専用データを保持し、取り消した場合は登録しません。追加機能も同じ確認に表示し、インストール後の別途有効化は不要です。四言語の説明を更新し、一項目を追加して各 1371 キーになりました。公開済みのピンイン 1.0.0 と配布ファイルは変更しません。
### 検索拡張とインストール互換性 · 0.9.112 · 2026-10-19

ピンイン頭文字検索 1.0.0 はホスト 0.9.112 以上を必要とし、オフラインの簡繁字辞書で既存のゲーム・アプリ検索を拡張します。SDK 1.1.0 に SEARCH 権限、マニフェストのコールバック、型を追加し、既存 API 1 の RPC 32 個のシグネチャは維持します。現在の範囲の名前だけを渡し、従来の隔離・順序・起動処理を使い、準備と失敗を明示します。インストール画面に最低・現在のフロントエンド版を表示し、版が不足するとインストールできません。既定ホームの設定は「テーマと表示」へ移動します。

四言語に 5 項目を追加し、各 1370 キーです。完全検査、Python 26 件、Node 58 件が合格しました。実際のピンイン、多音字、簡繁体、固定依存の摘要、再現可能なパッケージを確認しました。メーカー端末の JavaScript 隔離は実機確認が必要です。

### ページ共通検索の文言 · 0.9.111 · 2026-10-19

共通検索操作とゲーム検索の 5 項目を四言語へ追加し、合計 1365 キーになりました。ホストのライブラリ、最近のゲーム、お気に入りで使用します。範囲表示のページ・機種の引数と ROM の保護語を維持し、カタログ情報、摘要、呼び出し文脈を更新しました。公開 SDK API に変更はありません。

### アプリ画面の言語リソース · 0.9.109 · 2026-10-19

検索、長押しメニュー、ピン留めの 16 項目を簡体字中国語、繁体字中国語、英語、日本語で追加し、各言語 1360 キーになりました。既存訳を保持し、言語基準、摘要、呼び出し文脈を更新しました。SDK 契約と公開済みプラグインのアセットは変更しません。

### 公開 SDK 契約 1.0.1 · 2026-10-19

- 初回 CI で判明した Windows 作業コピーの改行による摘要差を修正し、SDK ソースを UTF-8/LF で検査します。1.0.0 を保持して 1.0.1 のスナップショットと三言語説明を追加しました。アセットは生のバイト列で検査し、実行 API は変更しません。

### 公開 SDK 契約 1.0.0 · 2026-10-19

- [公開 32 メンバーの呼び出し手引き](sdk/API_REFERENCE.md)と[インターフェース一覧](docs/INTERFACES.md)を追加し、引数、戻り値、権限、実行場所、失敗条件、例を中国語・英語・日本語で整備しました。
- [API 版管理](sdk/API_VERSIONING.md)、[変更履歴](sdk/API_CHANGELOG.md)、機械可読一覧、変更不可のスナップショットを導入し、check、Node テスト、CI に組み込みました。
- 既存 API の文書基準を作成するもので、ホスト・プラグインの版、言語リソース、公開済みアセットは変更しません。実機検証の範囲も変わりません。

本リポジトリに関係するホストの機能を記録します。Release はプラットフォームとテーマのサンプル、言語は個別 JSON で配布します。APK やストレージプロバイダー SDK のダウンロード場所ではありません。各項目は当時の状態です。開発には現在の契約を使用してください。

### 0.9.108 · 2026-10-19

アプリページにシステムが提供する起動可能アプリをアイコン一覧で表示し、名前とパッケージ名の検索、タッチとコントローラーでの起動、インストール変更や復帰時の自動更新に対応しました。入口は既定で表示し、明示的に無効にした設定は保持します。Android の既定ホームとして選択でき、設定に実際の状態とシステムの選択入口、別のホームへの変更入口を用意しました。Home を繰り返しても同じフロントエンドに戻り、既定ホーム時は最上位の戻るで終了しません。四言語に 8 件を追加して 1344 キーになりました。このホスト変更ではプラグインの ZIP と公開 API は変更していません。

### 0.9.107 · 2026-10-18

アップロード概要の同時更新で先頭と後続部分が別の版から読み出され、DB 記録長の不一致でクラッシュする問題を修正しました。ページと選択バッチの先頭、長さ、残りを同一トランザクションで取得します。32 件単位と転送並列数は維持し、復旧情報全体の読み込みや追加通信はしません。0.9.106 の検査と件数修正を継承し、Vita3K は 1.0.0 のままです。効率、大きな概要の同時更新、統計、Vita3K の 25 件が成功し、実機アップロードの検証は別途必要でした。

### 0.9.106 · 2026-10-18

クラウド設定後、ROM のサイズや時刻変更でバックグラウンド検査が全 ROM を読み、アップロード準備を妨げる問題を修正しました。メタデータとハッシュの無効化だけを行い、内容ハッシュは既存同期で必要時に計算します。リソース展開前の容量は集計待ちとし、実際の待機理由と展開後の本体・パッチのファイル数を表示します。有効数、未設定による除外、展開数を診断に記録します。60 件と実際の Vita3K スクリプトが成功し、端末と実クラウドは未検証でした。プラグイン 1.0.0、言語、API は変更していません。

### 0.9.105 · 2026-10-18

置き換えたローカル ROM はサイズが変わっても直ちに起動でき、現在のサイズを渡し、同期スナップショットは変更しません。通常 ROM の背景更新で選択済みの起動やアニメーションを中止しなくなりました。無効パス、依存関係、有効なエミュレーターの変更は従来どおり検査し、同期は内容と完全性を独立確認します。起動関連 85 件が成功しました。言語、プラグイン、API の変更はありません。

### 0.9.104 · 2026-10-18

Pegasus の PS2 インポートで bootPath={file.documenturi} を保持し、AetherSX2 のゲーム識別と設定に対応しました。既存記録も通常の背景検査で一度更新し、ライブラリの消去、再インポート、ディレクトリ再選択、ROM コピーや再ハッシュは不要です。AYANEO Pocket S mini／Android 13 の上書きインストールで、コールド起動と再起動の実 ID、CRC、設定を確認しました。非対応文書 URI の文言を追加して 1336 キーになりました。プラグインと API は不変です。

### 0.9.103 · 2026-10-18

SAF 起動非対応の RetroArch 1.22 未満は権限のある実パス、1.22 以降は従来の SAF を使います。AetherSX2 の任意ゲームディレクトリ設定は、エミュレーターと同じ URI 階層を保ち、ゲーム未照合と空の設定画面を防ぎます。ローカル設定のみで追加スキャン、ハッシュ、コピーはありません。起動、インポート、設定の 162 件と三比率が成功し、実エミュレーターと設定復旧は実機確認待ちでした。6 件を追加して 1335 キーとなり、プラグインと API は不変です。

### 0.9.102 · 2026-10-17

ゲーム単位だけにある起動宣言も、一意なら機種既定として登録し、混在時は索引設定として表示します。設定と起動は同じ状態を使います。機種も索引も未設定なら設定へ進み、ゲームの明示的上書きと手動の既定選択を保持します。旧記録は一度だけ背景登録し、ROM 再走査、ハッシュ、索引再書き込みはしません。診断に RetroArch の版、Activity、コア、ROM 引数、ファイルオープンを追加しました。296 件が成功し、実機の黒画面報告はインストール確認待ちでした。パック、API、言語契約は不変です。

### 0.9.101 · 2026-10-17

Pegasus のコレクション既定と機種設定を揃え、ゲームの明示指定は独立した上書きとして残します。混在する既定値は索引設定として表示し、一括既定は利用者が設定できます。不明な引数や非対応コアでも ROM とメディアのインポートは妨げません。「その他のアーケード」は既存機種設定と MAME／FBNEO コアを共有します。機種既定が空でもゲームの有効設定を誤って変更扱いにする問題を PS1 を含め修正しました。インポート、起動、コアのセーブ、三比率設定の 243 件が成功し、実機は未検証でした。1 件を追加して 1329 キー、プラグイン ZIP は不変です。

### 0.9.100 · 2026-10-16

セーブ同期の開始時に保存先と現在の関連ディレクトリを比較し、必要なら既存の移動処理を先に実行します。旧設定も再編集不要です。比較はローカルのみで、走査、ハッシュ、通信を増やしません。コレクションと版を保持し、再アップロードや重複移動をせず、同期の中止で今回作成した移動を停止します。一つの接続先の誤りは他を妨げません。更新後、再利用、中止、一時停止、分離、カードの 31 件が成功しました。実機移動は未検証で、プラグインと言語契約は不変です。

### 0.9.99 · 2026-10-16

セーブディレクトリの変更はセーブと索引を版ごと移動し、アプリルート変更時は ROM、メディア、索引、プラグインデータも移動します。既定セーブパスは追従し、明示した別パスは選択できます。既存スケジューラーと移動 API により百度のバッチと WebDAV MOVE を使い、実際の成功で確定します。ファイルごとのハッシュ、本文再送、完了後の反復照会はしません。復旧は未確定部分だけ、依存関係はバッチ処理です。同一ローカル検査とキャッシュを再利用し、履歴は接続先と位置を示して旧記録の位置を残します。移動カードは一時停止と継続、移動前の中止に対応します。既存 125 件と三比率の結果を継承し、実クラウドは未検証でした。プラグイン ZIP は不変です。

### 0.9.98 · 2026-10-16

ROM リソース API と 4NPC の Vita3K 1.0.0 をホスト 0.9.98 向けに公開しました。範囲だけをプラグインが決め、転送、進捗、中止、復旧、索引はホストが担当し、不参加端末は従来のタイトルとメディア同期を保持します。Vita3K はディレクトリだけを設定し、本体、パッチ、DLC、ライセンスを扱い、他ゲーム、セーブ、ファームウェア、設定は除外します。ZIP の公開と検証後にストアへ登録し、他の同期プラグインは 1.0.4 のままです。同じローカルセーブに百度と WebDAV を設定でき、走査を共有して版とタスクは分離します。言語作者の位置、上部メニューの文字／アイコン切り替えを調整し、高さを保持しました。既存の対象回帰と三比率、署名、16 KiB、Filament、四 ABI、26 SDK リソース、1304 キーを確認しました。Vita3K、エンジン、文書プロバイダー、二端末実同期は未検証でした。

### 0.9.97 · 2026-10-16

プラグイン設定と言語選択・取得をホストのナビゲーション、見出し、戻る履歴に統合し、設定と業務ページは分離しました。指定されたコミュニティ取得とモデル表示は専用画面を維持します。作者を言語名と同じ行に置き、内蔵はインストール済みと表示し、完全で互換な言語に人の審査状態を要求しなくなりました。表紙の長押しでそのゲームを選択して複数選択へ入り、コントローラーの既存メニューを保持します。プラグインは 1.0.4、パック、索引、最低版、同期は不変です。対象・三比率と署名、16 KiB、Filament、四 ABI、26 リソース、1300 キーを確認し、実 WebView とクラウドは未検証でした。

### 0.9.96 · 2026-10-16

ストアから設定を除き、同版はインストール済みと表示します。取得前に確認し、ローカル ZIP は一度だけ展開、中止時は旧版を保持します。ホストが有効化、権限、削除を管理し、無効でも設定できます。CONFIGURATION は BUSINESS と分離し、設定、専用データ、ローカル接続一覧だけにアクセスします。同期 1.0.4 を 0.9.96 向けに公開・登録し、保存先、データ、方式、旧 Release を保持しました。Xbox／任天堂／PlayStation の表示は保存した変換を共有し、入力割り当ては不変です。既存 JVM 52 件、SDK 7 件、公開ツール 7 件、三比率を継承し、Release 署名、整列、Filament、四 ABI、26 リソース、1300 キーを確認しました。実 WebView とクラウドは未検証でした。

### 0.9.95 · 2026-10-16

任意の configurationPage を宣言済みページへ関連付け、同期例の入口不足を修正しました。設定を宣言しないプラグインには表示しません。同期 1.0.3 は 0.9.95 向けで、既存の保存先 UI、データ、権限、寿命を再利用し、同期方式を変更しません。35 件（コア 4、導入・ブリッジ 17、カード・設定・三比率 8、公開ツール 6）が成功しました。署名 APK を交付し、整列、Filament、ABI、SDK、言語を確認しました。ZIP を索引より先に公開し、旧 APK と Release を残します。

### 0.9.94 · 2026-10-16

統合項目の初回は公開元を優先し、更新は記録された実配布元と取得情報を使います。ローカル差し替えは一度の展開と既存取引を使い、キャンセル時は旧データを保持します。初回読み込みで未登録ディレクトリを回収し、未変更索引を書き直しません。タイトル、版、更新表示を揃え、設定に共通ダイアログを使い、既存の開く動作を保ちました。52 件（コア 13、導入等 27、SDK 7、公開 5）が成功し、一回取得、配布元、三比率、既定言語、設定キーを確認しました。署名、16 KiB、Filament、ABI、SDK、言語を確認しました。作者による多言語と既定言語、必須中国語を導入し、1.0.2 を 0.9.94 向けに公開しました。1.0.1 のアセットは不変です。

### 同期プラグイン 1.0.1 · 2026-10-16

4NPC のお気に入りと最近の記録を独立プラグインとして公開し、plugins/index.json に登録しました。0.9.91 に対応し、内蔵アイコンを保持します。SDK、例、12 共通アイコンを同期し、匿名取得、サイズ、ハッシュ、マニフェストを確認しました。0.9.92 は版バッジ、同配布元の更新表示、導入確認、共通アイコンを追加し、既存設定・データ・追加権限の規則を継承しました。0.9.93 は配布元変更後に索引を無効化します。

### 0.9.91 · 2026-10-15

4NPC の二つの独立例は既存クラウドと公開 API を使い、個別に導入、有効化、設定できました。当時ストアの Release は未公開でした。同機種、同名、全 ROM ファイル集合で照合し、複数 ROM でも一記録、本文や MD5 は読みません。お気に入りの追加と解除、最近の新しい時刻と大きい回数・時間を同期し、加算しません。STORAGE と軽量ページングは既存クライアント、予算、キャッシュを使い、変更なしの送信を避け、基準とバッチを同時確定します。マージ、API、接続先、三比率が成功し、署名、整列、Filament、四 ABI、SDK、1286 キーを確認しました。署名は 0.9.90 と同じで、エンジンと実クラウドは未検証でした。

### 0.9.90 · 2026-10-15

表示を切り替えられるプラグインメニュー、導入済みとストア、有効化・削除、設定、独自ページを追加しました。JS と HTML は同じ資料、メディア参照、お気に入り、履歴、索引 API と複数配布元導入を使い、WorkManager で動作してゲーム起動を妨げません。SDK とローカル例は公開されましたが Release は未公開で、ストレージ登録とストリームは将来対応でした。四言語に 52 件を追加し、公開翻訳への同期と実エンジン・WebView の検証は未完了でした。署名、整列、Filament、同梱 SDK・言語を確認し、署名は 0.9.89 と同じでした。

### 0.9.89 · 2026-10-15

ホストのタスクと転送を統一し、接続先の保存処理を分離して共通設定とイベントを使います。自動・手動の書き込みテストを除き、実際のアップロード失敗を保持します。完成した一時 ROM・メディア・セーブの復旧では URL を再取得しません。接続先の役割と効率規則を公開しましたが、専用 SDK と導入ブリッジは未公開でした。この文書更新では言語 JSON、索引、既存 ZIP は変更していません。

### 0.9.88 · 2026-10-15

設定右下のアイコン入口で公開 GitHub 配布元を 1 行に一つ設定します。言語、テーマ、プラットフォームが共有し、同一識別・同一内容を統合して差異は残します。言語ダイアログから URL 設定を除き、四言語は 1233 件になりました。

### 0.9.87 · 2026-10-15

簡体字、繁体字、英語、日本語を内蔵し、システム追従と手動選択、未対応時の簡体字表示を提供しました。当時は互換で完全な reviewed 言語を取得し、作者を表示しました。言語は個別 JSON で、内蔵の source／draft は母語話者による審査完了を意味しません。reviewed の導入条件は 0.9.97 で撤廃しました。

### packs-2026-10-06

最初の MSX と琥珀テーマのサンプルはホスト 0.9.44 以降向けです。元の三言語の説明は RELEASE_NOTES.md に残しています。
