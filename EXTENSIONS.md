# 复古猫扩展包规范

## 平台包

ZIP 根目录包含 `platform.json`，可附 `assets/logo.png` 和 `assets/pixel.png`。`schemaVersion` 为 1。示例：

```json
{
  "schemaVersion": 1,
  "platform": {
    "id": "msx",
    "name": "MSX",
    "aliases": ["msx", "msx computer"],
    "extensions": ["rom", "mx1", "mx2"],
    "medium": "CARTRIDGE"
  },
  "manufacturer": "ASCII / Microsoft",
  "releaseYear": 1983,
  "coverAspectRatio": 0.75,
  "assets": {"logo": "assets/logo.png", "pixel": "assets/pixel.png"}
}
```

机种 ID 只能用 2～32 位小写字母、数字、`_`、`-`，不能与内置机种或已安装扩展重复。名称和别名不能与其他机种重复；扩展名不带点，允许与其他机种重叠，但重叠扩展名不能单独用来自动识别机种。`medium` 使用现有 `GameMedium` 枚举。`coverAspectRatio` 为封面宽/高，范围 0.5～2；没有模型时仍按该比例显示封面和占位图。图标只能是 PNG/WebP，单张不超过 8 MiB、宽高不超过 2048 像素；平台包最多 128 个条目、解压后最多 64 MiB。

安装后机种出现在已有机种选择器和文件夹配置中。选择对应的本地 ROM 目录后，继续使用应用现有的扫描、游戏库、网盘映射与资源任务流程。包本身不执行代码，不提供模拟器，模拟器需用户在设置里配置。平台包目前不提供卸载入口，避免已经入库的游戏丢失机种定义；同 ID 的新包可重新安装替换。

## 主题包

ZIP 根目录包含 `theme.json`。配色、布局与动效的可运行示例见 [`examples/amber/theme.json`](examples/amber/theme.json)。格式版本 3 增加模型槽位：

```json
{
  "schemaVersion": 3,
  "id": "example",
  "name": "示例主题",
  "author": "作者",
  "colors": {
    "background": "#141210", "surface": "#22201D", "foreground": "#F8F3EA",
    "muted": "#BBB0A0", "accent": "#E8A94C", "outline": "#514536"
  },
  "assets": {
    "background.library": "art/library.png",
    "platform.msx.logo": "art/msx-logo.png",
    "model.msx.packaging": "models/msx-box.glb",
    "model.msx.gameMedia": "models/msx-cart.glb"
  }
}
```

`model.<机种ID>.packaging` 和 `model.<机种ID>.gameMedia` 指向独立的 GLB 2.0 文件，单个不超过 32 MiB。模型替换只换几何文件，保留原有 Filament 渲染、贴图槽位、比例归一化、灯光与动效；作者必须检查封面或标签是否正确映射。主题包可以省略任意模型槽位，不会为缺失模型凭空生成替代模型。扩展平台的主题素材需先安装该平台才能通过导入校验。

主题预览图固定为 1280×720 PNG/WebP，存放 `previews/<id>.png` 或 `.webp`，展示 16:9 游戏库实际视觉方向；文字需注明模拟画面与实机截图的区别。作者还须检查 4:3 和 1:1 页面及手柄焦点。在线列表先显示预览和作者信息，安装后仍由用户在主题设置中明确预览或应用。

## 在线目录与发布

公开仓库默认分支根目录的 `catalog.json` 结构为 `{"schemaVersion":1,"entries":[...]}`。每个条目提供 `kind` (`PLATFORM`/`THEME`)、`id`、`name`、`author`、`description`、`version`、`minAppVersion`、`releaseTag`、`fileName`、`sizeBytes`、`sha256`；主题还必须有 `previewPath`。`releaseTag` 与 `fileName` 对应该来源仓库的 GitHub Release 资产。应用下载后先核对精确字节数和 SHA-256，再交给与本地 ZIP 导入相同的安装链路。目录下载失败时显示上次缓存及错误；不影响离线游戏库或已安装扩展。

0.9.88 起支持多个公开仓库，设置方法见 [README](README.md)。平台和主题按类型、扩展 ID 与内容 SHA-256 合并相同条目，其他内容分别展示。同一批安装只能为同一扩展选择一个版本。Fork 作者须自行发布索引所引用的 Release 资产；只复制索引而未发布资产，无法从自己的仓库下载安装。不要把 APK 版本当成扩展包版本，也不要为文档更新改写已发布 ZIP 的大小或摘要。

## 语言与同步渠道

脚本插件采用独立的 `plugins/index.json` 和包含 `plugin.json` 的 ZIP，SDK、安装与页面规则见[脚本插件文档](sdk/README.md)。框架已随 0.9.90 APK 打包，原生设备验收仍待完成；资源包不会因为增加脚本框架而获得代码执行权限。存储服务的脚本注册及流式文件桥接仍待后续阶段接入，不将现有通用 JSON API 当成另一套同步实现。

语言使用独立的 `languages/index.json` 和单语 JSON，不加入平台／主题的 ZIP 清单。作者署名、译文基线和 reviewed 发布规则见[语言贡献说明](languages/README.md)。

平台和主题的 `author` 由在线目录展示，主题清单可保存自身署名；语言文件使用 `author` 和 `credits`。Fork 保留原作者、素材来源与许可，新增维护者署名不能冒充原作者。

0.9.89 已建立宿主内的公共同步流程和渠道连接表单，独立存储插件 SDK、安装桥接及分发尚未发布。当前不能将提供者代码放进主题、平台或语言包执行。职责与效率约束见[同步渠道扩展说明](SYNC_PROVIDERS.md)。

平台和主题的名称、图标、背景、包装图、模型等必须由投稿者自行创作或有可再分发许可。不要在包内提交 ROM、固件、存档、密钥或第三方账号资料。
