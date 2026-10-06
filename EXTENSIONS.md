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

安装后机种出现在已有机种选择器和文件夹配置中。选择对应的本地 ROM 目录后，继续使用应用现有的扫描、游戏库、WebDAV 映射与资源任务流程。包本身不执行代码，不提供模拟器，模拟器需用户在设置里配置。平台包目前不提供卸载入口，避免已经入库的游戏丢失机种定义；同 ID 的新包可重新安装替换。

## 主题包

ZIP 根目录包含 `theme.json`。配色、布局、动效和图片格式参见复古猫主仓库的 `docs/THEME_PACKAGES.md`。格式版本 3 增加模型槽位：

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

公开仓库 `main/catalog.json` 结构为 `{"schemaVersion":1,"entries":[...]}`。每个条目提供 `kind` (`PLATFORM`/`THEME`)、`id`、`name`、`author`、`description`、`version`、`minAppVersion`、`releaseTag`、`fileName`、`sizeBytes`、`sha256`；主题还必须有 `previewPath`。`releaseTag` 与 `fileName` 对应 GitHub Release 资产。应用下载后先核对精确字节数和 SHA-256，再交给与本地 ZIP 导入相同的安装链路。目录下载失败时显示上次缓存；不影响离线游戏库或已安装扩展。

平台和主题的名称、图标、背景、包装图、模型等必须由投稿者自行创作或有可再分发许可。不要在包内提交 ROM、固件、存档、密钥或第三方账号资料。
