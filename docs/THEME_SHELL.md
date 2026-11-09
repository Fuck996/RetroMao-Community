# 主题界面结构 / Theme launcher shell / テーマの画面構成

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Shell schema](../schemas/theme-shell.schema.json) · [Presentation schema](../schemas/theme-presentation.schema.json) · [DECK example](../examples/deck/theme.json)

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

### 格式 7

格式 7 从 Android 1.0.43 起可发布，`schemaVersion: 7` 必须包含 `presentation`，不再使用 `modern`、`library`、`neutral`、`deck` 风格。`presentation` 按组件分别声明导航、设置项、卡片、详情、模型展台等，结构见 [presentation schema](../schemas/theme-presentation.schema.json)。

`recentCarousel` 在格式 7 另有 `geometry`（尺寸和间距）、`focus`（`start` 默认，选中项移到左侧；`center` 选中项停在中间，靠近两端时列表不再滚动）、`size`（显示 10～40 个游戏，最近游戏在前，按游戏库顺序补齐；省略时最多 20 个最近游戏、不足 10 个补到 10 个）和 `badges`（`none` 默认；`corner` 显示可下载、待上传等资源状态）。`presentation.showcaseModel` 与 `showcaseHomeModel` 设定双屏上屏在游戏库和首页显示 `packaging` 包装盒（默认）或按 `setting` 设置。

省略的字段保持原有呈现，应用不会替旧主题包补上新效果。格式 6 及更早的主题不能使用这些字段。发布格式 7 时 `minAppVersion` 至少为 `1.0.43`。

## English

Theme format 6 is available from Android 1.0.39. Set `schemaVersion: 6` in `theme.json` and put the object above in `shell`. Base styles are `minimal`, `modern`, `library`, and `neutral`, which uses the theme palette directly. Every theme ID follows the same rules.

The default `home` is `library`, and `recent` is also available. Set `recentCarousel` to enable a model carousel. Its default model is `media`, and `packaging` is also available. A saved player preference takes precedence. Use `floating` actions or open options from the `title`. The shortcut to the library can be a `tile` or use the `navigation` style.

The default `navigationAlignment` is `start`, with `end` available. The `compact` footer shows the main actions for the current page. The host shows page keys at the ends of the top bar and platform keys in the footer on game pages. `ctrLibraryOnly` limits 3DS mode to the library. Set the video scrim to a value from `0` to `1` and use `showcaseVideo` for video on the upper screen. Set `dualScreen.showcase.layout` to `modelHero` for a large model on that screen.

Publish format 6 themes with `minAppVersion` of at least `1.0.39`. Keep the same theme ID for upgrades.

### Format 7

Format 7 can be published for Android 1.0.43 and later. A `schemaVersion: 7` theme must include `presentation` and cannot use the `modern`, `library`, `neutral`, or `deck` styles. `presentation` declares each component separately, such as navigation, settings items, cards, details, and model stages. See the [presentation schema](../schemas/theme-presentation.schema.json).

In format 7, `recentCarousel` also accepts `geometry` for size and spacing, and `focus`. With `start`, the default, the selected game moves to the left. With `center`, it stays in the middle and the list stops scrolling near either end. `size` shows 10 to 40 games, with recent games first and the rest filled in library order. Without it, the list shows up to 20 recent games and fills to 10. `badges` is `none` by default, and `corner` shows statuses such as available to download or pending upload. `presentation.showcaseModel` and `showcaseHomeModel` set whether the upper screen shows the `packaging` box, the default, or follows the `setting`, for the library and the home page.

Omitted fields keep the previous appearance, and the app does not add new effects to older theme packs. Format 6 and earlier cannot use these fields. Publish format 7 themes with `minAppVersion` of at least `1.0.43`.

## 日本語

Android 版 1.0.39 以降でテーマ形式 6 を利用できます。`theme.json` に `schemaVersion: 6` を指定し、上のオブジェクトを `shell` に設定します。基本スタイルは `minimal`、`modern`、`library`、テーマの配色をそのまま使う `neutral` です。すべてのテーマ ID に同じ規則が適用されます。

`home` の既定値は `library` で、`recent` も選べます。`recentCarousel` を指定するとモデルを横に並べて表示します。既定のモデルは `media` で、`packaging` も選択できます。利用者の保存済み設定が優先されます。操作は `floating` のボタン、または `title` から開けます。ライブラリへの入口は `tile` または `navigation` の見た目にできます。

`navigationAlignment` の既定値は `start` で、`end` も選べます。`compact` は現在のページの主な操作を表示します。ページ切り替えは上部バーの両端、機種切り替えはゲーム画面の下部に表示されます。`ctrLibraryOnly` は 3DS モードをライブラリに限定します。動画の暗さは `0` から `1`、上画面の動画は `showcaseVideo` で指定します。`dualScreen.showcase.layout` の `modelHero` は上画面に大きなモデルを表示します。

形式 6 を配布するときは `minAppVersion` に `1.0.39` 以上を指定します。更新時は同じテーマ ID を使ってください。

### 形式 7

形式 7 は Android 版 1.0.43 以降向けに配布できます。`schemaVersion: 7` では `presentation` が必須で、`modern`、`library`、`neutral`、`deck` のスタイルは使用できません。`presentation` では、ナビゲーション、設定項目、カード、詳細、モデルの台などを部品ごとに指定します。構造は [presentation schema](../schemas/theme-presentation.schema.json) を参照してください。

形式 7 の `recentCarousel` では、サイズと間隔の `geometry` と `focus` も指定できます。既定の `start` では選択中のゲームが左に移動し、`center` では中央に留まり、両端に近づくと一覧はスクロールを止めます。`size` は 10～40 本を表示し、最近のゲームを先頭に、残りをライブラリの順で補います。省略すると最近のゲームを最大 20 本表示し、10 本まで補います。`badges` の既定値は `none` で、`corner` はダウンロード可能やアップロード待ちなどの状態を表示します。`presentation.showcaseModel` と `showcaseHomeModel` は、ライブラリとホームで上画面に `packaging` のパッケージ（既定）を表示するか、`setting` の設定に従うかを指定します。

省略した項目は従来の表示のままで、古いテーマパックに新しい効果が加わることはありません。形式 6 以前ではこれらの項目を使用できません。形式 7 を配布するときは `minAppVersion` に `1.0.43` 以上を指定します。
