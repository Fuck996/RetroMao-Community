# 主题界面结构 / Theme launcher shell / テーマの画面構成

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Schema](../schemas/theme-shell.schema.json) · [DECK example](../examples/deck/theme.json)

```json
{
  "home": "recent",
  "recentCarousel": {
    "defaultModel": "media",
    "actions": "title",
    "libraryShortcut": "navigation"
  },
  "navigationAlignment": "end",
  "footer": "compact",
  "ctrLibraryOnly": true,
  "videoScrim": 0.62,
  "showcaseVideo": true
}
```

## 中文

主题格式 6 从 Android 1.0.39 起支持。在 `theme.json` 中设置 `schemaVersion: 6`，把上面的对象放在 `shell` 字段。基础 `style` 可选 `minimal`、`modern`、`library` 或采用固定主题配色的 `neutral`。所有主题 ID 使用相同的字段和规则。

`home` 默认 `library`，也可选 `recent`。声明 `recentCarousel` 可启用最近游戏的模型轮播。默认显示 `media`，也可指定 `packaging`，玩家已保存的选择优先。操作可采用 `floating` 浮动按钮或 `title` 点标题打开。列表末尾的游戏库入口可用 `tile` 或顶栏样式 `navigation`。

`navigationAlignment` 默认 `start`，可选 `end`。紧凑底栏 `compact` 只显示当前基本操作，系统在顶栏两端显示切页按键，在游戏页面底栏显示切机种按键。`ctrLibraryOnly` 限定 3DS 模式只在游戏库生效。视频遮罩可设为 `0` 到 `1`，`showcaseVideo` 控制双屏上屏视频。`dualScreen.showcase.layout` 可选 `modelHero` 以展示大尺寸模型。

发布格式 6 的主题时，发布元数据的 `minAppVersion` 至少为 `1.0.39`。沿用主题 ID 可让应用识别升级。

## English

Theme format 6 is available from Android 1.0.39. Set `schemaVersion: 6` in `theme.json` and put the object above in `shell`. Base styles are `minimal`, `modern`, `library`, and `neutral`, which uses the theme palette directly. Every theme ID follows the same rules.

The default `home` is `library`, and `recent` is also available. Set `recentCarousel` to enable a model carousel. Its default model is `media`, and `packaging` is also available. A saved player preference takes precedence. Use `floating` actions or open options from the `title`. The shortcut to the library can be a `tile` or use the `navigation` style.

The default `navigationAlignment` is `start`, with `end` available. The `compact` footer shows the main actions for the current page. The host shows page keys at the ends of the top bar and platform keys in the footer on game pages. `ctrLibraryOnly` limits 3DS mode to the library. Set the video scrim to a value from `0` to `1` and use `showcaseVideo` for video on the upper screen. Set `dualScreen.showcase.layout` to `modelHero` for a large model on that screen.

Publish format 6 themes with `minAppVersion` of at least `1.0.39`. Keep the same theme ID for upgrades.

## 日本語

Android 版 1.0.39 以降でテーマ形式 6 を利用できます。`theme.json` に `schemaVersion: 6` を指定し、上のオブジェクトを `shell` に設定します。基本スタイルは `minimal`、`modern`、`library`、テーマの配色をそのまま使う `neutral` です。すべてのテーマ ID に同じ規則が適用されます。

`home` の既定値は `library` で、`recent` も選べます。`recentCarousel` を指定するとモデルを横に並べて表示します。既定のモデルは `media` で、`packaging` も選択できます。利用者の保存済み設定が優先されます。操作は `floating` のボタン、または `title` から開けます。ライブラリへの入口は `tile` または `navigation` の見た目にできます。

`navigationAlignment` の既定値は `start` で、`end` も選べます。`compact` は現在のページの主な操作を表示します。ページ切り替えは上部バーの両端、機種切り替えはゲーム画面の下部に表示されます。`ctrLibraryOnly` は 3DS モードをライブラリに限定します。動画の暗さは `0` から `1`、上画面の動画は `showcaseVideo` で指定します。`dualScreen.showcase.layout` の `modelHero` は上画面に大きなモデルを表示します。

形式 6 を配布するときは `minAppVersion` に `1.0.39` 以上を指定します。更新時は同じテーマ ID を使ってください。
