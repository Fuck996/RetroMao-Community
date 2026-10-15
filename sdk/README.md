# 脚本插件 SDK v1

脚本框架首次随 0.9.90 APK 打包，0.9.91 APK 增加已配置网盘的 JSON 读写与两个同步示例所需接口，原生引擎与页面仍待设备验收。收藏同步与最近记录同步 **1.0.1** 已[公开发布](https://github.com/Fuck996/RetroMao-Community/releases/tag/sync-examples-1.0.1)，通过 `plugins/index.json` 在商店提供，兼容 0.9.91。

主菜单的 **插件** 提供 **已安装** 与 **商店**。入口开关位于 **设置 → 主题与显示**；隐藏入口不卸载或禁用插件。仓库沿用设置右下角的公共入口，多行地址和内容合并规则不变。平台、主题和语言保留原安装入口及索引。

0.9.92 增加版本徽标、已安装插件更新提示、安装确认与公共图标，规则见[插件版本与公共图标](PLUGIN_VERSIONS.md)。图标可用清单的 `iconName`，或页面的 `retromao.icons.list/url`，不为每个图标发网络请求。

## 包与运行

ZIP 根目录放 `plugin.json`，业务入口为已编译的 JavaScript，页面为包内 HTML/CSS/JavaScript。参考 [清单](../examples/library-notes/plugin.json)、[后台脚本](../examples/library-notes/main.js) 与 [页面](../examples/library-notes/index.html)。作者、版本、最低应用版本必填，`schemaVersion`、`apiVersion` 均为 1。

- `actions` 声明动作，`entryPoint` 使用 `retromao.define({actions: {...}})` 注册同 ID 函数。原生详情页运行时传入空对象；页面可用 `retromao.tasks.run(id, arguments)` 传入业务参数。
- `pages` 声明自定义页面，SDK 由宿主在文档开始时注入，无需打包 SDK 副本。等待 `retromao.ready` 后调用接口。类型见 [retromao.d.ts](retromao.d.ts)。可使用原生 HTML 或自己打包的前端框架，不从 CDN 加载运行代码。
- 后台动作采用 AndroidX JavaScriptEngine 1.1.1，按需创建隔离实例。需要 Android System WebView 支持消息端口、终止、堆限制及大脚本评估；缺少能力时明确提示更新 WebView。页面采用 AndroidX WebKit 1.14.0 的本地 HTTPS 资源与消息接口。不在运行失败后切换另一种执行方式。
- 任务使用既有 WorkManager 和 Room，同一插件一次运行一个动作。关闭页面不取消任务；取消、禁用和卸载终止对应动作。中断后不自动重放可能已提交的修改，用户可重新运行。公共接口按批原子提交，整个脚本不是跨调用事务；取消保留已完成修改。
- 游戏启动不等待市场、页面或脚本。任务结束释放实例，最后一个实例结束关闭引擎连接；页面退出销毁 WebView、消息会话与订阅。

## 能力与配置

`capabilities` 支持 `LIBRARY_READ`、`LIBRARY_WRITE`、`NETWORK`、`STORAGE`，启用时展示所需能力；更新增加能力后需重新启用。`NETWORK` 声明 `networkHosts`，如 `api.example.com`、`example.com:8080`，`*` 表示任意主机。HTTP 不自动跟随重定向。`STORAGE` 从 0.9.91 提供已配置网盘中本插件目录的 JSON 读写，不向脚本提供凭据。脚本没有 Java 反射、任意文件路径或 Room 入口。脚本隔离实例不等同于独立操作系统安全边界，仅安装可信作者的代码。

配置 `settings` 支持 `TEXT`、`SECRET`、`BOOLEAN`、`NUMBER`、`CHOICE`，值统一为字符串。字段支持 `default`、`required`、`options: [{value,label}]`。宿主用公共弹窗编辑验证，`SECRET` 沿用凭据加密；动作开始时读取一次配置。配置与私有 JSON 按来源仓库和插件 ID 分开保存，切换 Fork 不复用另一来源的密钥，切回原来源仍能接续。

## 公共接口

| SDK | 业务与边界 |
| --- | --- |
| `library.game/games` | 按 ID、平台或集合读取，键集分页，每页最多 200 项 |
| `library.records` | 同一分页链路的轻量投影：本机 ID、机种、游戏名、完整 ROM 文件名列表、收藏、最近记录；不含媒体、文件路径或哈希 |
| `library.edit` | 复用公共编辑、批量事务、用户修改标记与原索引发布，每批最多 200 项 |
| `library.apply` | 使用同一编辑入口批量提交，不返回大游戏对象；可携带 `checkpoint`，与该批修改原子保存到本插件私有 JSON |
| `favorites.list/set` | 查询收藏或明确设置状态，重复请求不会反转状态 |
| `recent.list/edit` | 携带读取时的 `expected` 修改最近记录，不调用游戏启动 |
| `media.folders/assets/edit` | 查询已授权且已编入资产索引的媒体，链接或解除指定角色，不扫全盘，不经 JSON 传媒体正文 |
| `index.patch` | 在当前插件 ID 的命名空间下编辑字段，其他插件字段保持原样 |
| `settings.get`、`data.get/patch` | 自身配置和私有 JSON；私有数据顶层 `null` 删除键 |
| `http.request` | 经声明主机访问 HTTP(S)，返回状态、响应头与文本，正文最多 256 KiB；非 2xx 由插件处理 |
| `storage.sources/read/write` | 列出已配置连接；后台动作读取／条件写入自身 JSON 文档；单文档最大 384 KiB，不提供任意路径、二进制或删除接口 |
| `tasks.run/get/result/cancel/watch` | 页面发起、观察、取消本插件动作，成功后读取单独保存的结果 |
| `tasks.progress` | 动作提交完成数、总数和说明，宿主合并短间隔进度写入 |

`tasks.current()` 读取本插件当前或最近任务，页面重新打开后可接入同一 `watch`。`library.edit/apply(changes, checkpoint)` 的可选 checkpoint 沿用 `data.patch` 的顶层 null 删除规则，不拥有宿主网络事务。

`storage.sources()` 返回 `{id,name,provider,scope}`，`storage.read(source,"dc.json")` 返回 `{token,value}`（缺失为 null）。随后可用 `storage.write(token,value)` 提交 JSON 对象；token 只适用于当前动作中最近一次读取，不能跨文档、动作、账号或目录复用。无变化不要调用写入；宿主也会排除同值写入。错误直接返回插件任务，不自动切换渠道或重传。公共存储复用 `RemoteClientRegistry`、`RemoteClient`、`RemoteTransferContext`，原 ROM、媒体和存档同步流程保持不变。示例见[两个记录同步插件](../examples/SYNC_EXAMPLES.md)。

资料修改携带 `metadata.expected`，只编辑 `values` 指定字段；`mode: "FILL_MISSING"` 沿用宿主补齐规则。媒体修改携带当前 `expected` 引用和目标资产路径、修订、大小，删除用 `asset: null`。扩展字段按键比较：不提供 `expected` 表示原先不存在，不提供 `value` 表示删除；显式 JSON `null` 是真实存储值。例如：

```js
await retromao.index.patch(game.id, { note: { value: "通关后再玩" } });
await retromao.index.patch(game.id, { note: { expected: "通关后再玩" } });
```

页面与脚本进入同一个宿主适配层，再调用既有公共接口。字段随原平台索引发布，不在每次编辑后额外上传或下载索引。单条消息最大 512 KiB，SDK 最多并行 4 个请求，作者应分页、批量处理并等待结果。

页面网络访问经 `http.request`，不直接联网或读取 `file://`、`content://`。主动点击的外部链接交给浏览器；桥接只授予本插件 HTTPS 源的顶层页面。SDK 提供主题 CSS 变量及方向键焦点移动，作者仍须验证 16:9、4:3、1:1、触摸与手柄。

当前不包含存储渠道脚本注册、ROM/存档流式传输、任意媒体下载及外部 APK 安装。这些能力须继续接入既有传输流程，不能通过 JSON 或私有数据库重做同步。见[同步提供者契约](../SYNC_PROVIDERS.md)。

## 打包发布

```text
python community/tools/build_script_plugin.py community/examples/library-notes --release-tag script-examples-1
```

输出 ZIP 和目录条目到 `community/dist/`，不自动发布。先本地导入，再上传到自己仓库指定标签的 Release，将生成条目加入 `plugins/index.json` 的 `entries`。条目沿用社区字段，`kind` 为 `SCRIPT`；ID、名称、版本、作者须与包内一致，最低应用版本以实际包含框架的 APK 为准。

安装复用现有多仓库下载、流式大小/SHA-256 校验及本地 ZIP 安装，不逐插件拉源码或清单。包最多 2048 个文件、解压后 64 MiB，清单最多 1 MiB，入口/页面/图标单个最多 4 MiB。安装默认禁用；同来源更新保留已有授权，新能力需重新启用。不同内容或来源由用户明确选择安装，没有跨仓库自动升级。

切换到不同来源的同 ID 实现时，清除当前任务及结果，防止新来源读取旧来源的输出；来源隔离的配置与私有数据仍保留。卸载前取消任务，可保留或删除本来源配置与私有数据。宿主游戏资料、收藏、最近记录、存档及扩展字段保留。插件若需删除自身字段，应在卸载前通过公共接口明确执行。

## 0.9.91 验证（2026-10-15）

- 两个独立同步 ZIP 已生成；SDK 与合并测试 15 项通过，包含名称／完整 ROM 集合匹配、取消收藏传播、多 ROM 去重、无变化零上传、渠道隔离、取消后的基线继承及游玩记录并发修改。
- 公共编辑与插件任务测试、WebDAV 条件写／大小限制／首次目录创建、百度同轮目录分页复用测试通过。已有原索引读取新鲜度测试保持通过，未运行全量存档或 ROM 回归。
- 两款 HTML 页面在 1280×720、960×720、720×720 下通过浏览器触摸、方向键焦点、进度与取消测试；图像位于 `app/build/reports/ui-screenshots/sync-*.png`。这使用模拟宿主，不代替原生 WebView 和实际网盘验收。
- 内置四语共 1286 键，生成一致性与固定文案参数检查通过。签名 APK 已打包，商店 Release 尚未发布，新增译文仍待公开维护源固定提交。
- 正式产物 `RetroMao-0.9.91.apk`（内部编号 135）已交付到 `U:\安卓应用\自研应用`，76,234,372 字节，SHA-256 为 `55deb811b42ee1f19cb38c7569edf85ca50c9983bf31de648bbdff9cb15a37ce`。签名与 0.9.90 一致；签名、16 KiB 对齐、Filament 保留规则、四 ABI、包内 SDK 字节及插件接口检查通过。构建源码提交为 `6726514`。

## 0.9.90 验证记录（2026-10-15）

- 编译通过；核心清单／配置验证 3 项、宿主安装／桥接／任务测试 8 项、SDK 消息与生命周期测试 4 项通过。
- 插件列表、商店、配置弹窗在 16:9、4:3、1:1 下的触摸、手柄焦点、配置保存测试通过；另验证不同 Fork 的页面来源隔离。截图位于主工程 `app/build/reports/ui-screenshots/plugins-*.png`。
- 复用链路的导航、渠道配置弹窗、社区来源与缓存、平台包安装、公共内容编辑和语言运行时测试通过。失败后只复查对应范围，没有运行整库同步、额外文件哈希或 Release 打包。
- 新增 52 条四语文案，固定快照和扩展基线同步更新；生成一致性和 1369 处固定文案参数检查通过。新增文案尚未同步到公开翻译维护源，发布前须完成公开源固定提交。
- SDK 示例 ZIP 已生成，商店目录仍为空，没有发布尚不存在的 Release 资产。

原生 JavaScriptSandbox 与 WebView 的设备验收尚未完成：当前没有连接的 ADB 设备，工程现有 Android 35 模拟器因宿主缺少硬件加速驱动而启动失败。Robolectric 与 Node 验证不代替设备执行。需要在支持所需 WebView 能力的 Android 设备继续验证脚本运行／取消、页面桥接与销毁，以及进入游戏后的任务生命周期；本轮不宣称这些原生路径已通过真机验收。
