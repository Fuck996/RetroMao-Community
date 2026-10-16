# 插件多语言

从 0.9.94 起，插件可在自己的 `plugin.json` 中声明语言。作者维护译文，宿主不自动翻译，也不为切换语言下载附加文件。

## 默认语言与必备语言

- 发布时显式填写 `defaultLocale`。原有 `name`、`description`、页面、动作和配置字段的文字就是默认语言，不在 `localizations` 中重复填写默认语言。
- `localizations` 填写其他语言，使用 `zh-Hans`、`zh-Hant`、`en`、`ja` 等语言标识。最多支持 32 种语言，包含默认语言。
- **必须包含复古猫系统默认语言 `zh-Hans`。** 默认语言为英语等其他语言时，必须提供完整的 `zh-Hans` 译文。
- 用户当前语言有对应译文时使用该语言，没有时使用插件的 `defaultLocale`。插件默认语言不随复古猫默认语言改变。
- 已发布旧插件仍按原有基础文字显示，不因缺少新字段拒绝安装。新的发布工具要求显式声明默认语言。
- 使用多语言元数据或 `ready.messages` 的新包须将 `minAppVersion` 设为 `0.9.94` 或更高，避免旧 APK 安装时忽略并丢弃这些字段；旧插件不需要额外扫描或迁移。

## 清单示例

```json
{
  "id": "example.localized",
  "name": "Example plugin",
  "description": "A localized example",
  "author": "4NPC",
  "version": "1.0.0",
  "minAppVersion": "0.9.94",
  "defaultLocale": "en",
  "pages": [{"id": "main", "title": "Home", "path": "index.html"}],
  "messages": {"hint": "Choose a game"},
  "localizations": {
    "zh-Hans": {
      "name": "示例插件",
      "description": "多语言示例",
      "pages": {"main": "主页"},
      "messages": {"hint": "选择游戏"}
    }
  }
}
```

每个译文对象可包含：

| 字段 | 内容 |
| --- | --- |
| `name`、`description` | 插件名称与说明；商店和卡片使用 |
| `pages` | 页面 ID → 标题 |
| `actions` | 动作 ID → `{ "title": "标题", "description": "说明" }` |
| `settings` | 配置 ID → `{ "label": "名称", "options": { "选项值": "显示文字" } }` |
| `messages` | 插件自定义消息键 → 文字，供页面和脚本自行使用 |

页面、动作、配置、选项与自定义消息的键须与基础语言一致，不能通过翻译重命名业务 ID、配置键、选项值、资源路径、作者署名或版本。每种语言必须提供全部已有页面、动作和配置文字；没有对应功能的字典可以省略。每种语言的自定义消息最多 1000 项、256 KiB。

## 页面与脚本

已有 `retromao.ready` 提供一次会话的语言环境：

```javascript
const {locale, appLocale, defaultLocale, locales, messages} = await retromao.ready;
document.getElementById("hint").textContent = messages.hint;
```

`locale` 是插件实际选中的语言；`appLocale` 是用户设置的复古猫语言；`defaultLocale` 是插件默认语言；`locales` 是插件声明的语言集合。用户选择日语而上述插件只有英语和简中时，`locale` 为 `en`、`appLocale` 为 `ja`。

页面和脚本自行完成显示、插值、复数、日期及数字格式处理。宿主将选中语言的 `messages` 随 `ready` 返回，不为每条消息调用 RPC；也可以只声明语言和宿主文字，将页面译文保存在插件自己的脚本中。

## 打包与更新

`tools/build_script_plugin.py` 在生成 ZIP 前检查默认语言、简中必备项及译文键，并将商店所需的名称与说明写入同一条目录记录。完整译文和自定义消息保留在 ZIP 中，不把整份业务消息表塞进商店目录。安装时沿用现有整包摘要与清单核对。

修改译文也须递增插件版本，按原来源发布新 ZIP 和目录条目。语言变化只影响展示，不迁移或清空配置与私有数据。两个同步示例从 1.0.2 起补齐四语宿主文字，沿用原有四语业务页面；当前商店为 1.0.3，增加配置页声明，需要主程序 0.9.95，旧版 Release 与资产保留。
