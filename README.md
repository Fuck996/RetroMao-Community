# RetroMao Community｜复古猫社区扩展

**中文** · [English](README.en.md) · [日本語](README.ja.md)

这里是独立的扩展开发与分发仓库。开发插件、翻译或平台包无需获取宿主源码；需要 Python 3.11+，插件测试与浏览器验证还需要 Node.js 22+。建议先创建并激活 Python 虚拟环境。所有命令都在本仓库根目录执行。

从 Fork 后的第一个插件开始：安装固定依赖、检查仓库、生成模板、预览并打包。

```text
python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-dev.txt
npm ci --registry=https://registry.npmmirror.com
python tools/retromao.py check
python tools/retromao.py init plugin --id demo-plugin --name Demo --author YourName
python tools/retromao.py check extensions/demo-plugin
python tools/retromao.py preview extensions/demo-plugin
python tools/retromao.py pack extensions/demo-plugin --release-tag demo-plugin-1.0.0
```

预览地址显示在终端；Ctrl+C 停止服务。预览运行正式 SDK 和自己的代码，使用本地样本，不连接真实网盘。更多步骤见[开发与验收](docs/TESTING.md)、[投稿规则](CONTRIBUTING.md)和[发布流程](docs/PUBLISHING.md)。AI 请先读 [AGENTS.md](AGENTS.md)。

| 要做什么 | 从哪里开始 | 发布形式 |
| --- | --- | --- |
| 脚本插件 | [SDK](sdk/README.md)、[接口调用手册](sdk/API_REFERENCE.md)、templates/plugin | ZIP + plugins/index.json |
| 增加语言 | [语言指南](languages/README.md) | 单语 JSON + languages/index.json |
| 增加平台 | [平台契约](EXTENSIONS.md)、templates/platform | ZIP + catalog.json |

全部契约见[公共接口导航](docs/INTERFACES.md)；逐接口说明附带[机器清单](sdk/api.json)、[版本管理](sdk/API_VERSIONING.md)和 [API 变更说明](sdk/API_CHANGELOG.md)。

平台启动配置使用格式 2，需要包含此能力的宿主构建，版本门槛为 0.9.108；是否已经完成正式 APK 验收以[能力契约](contracts/host.json)和对应发行记录为准。旧格式 1 不包含启动配置。脚本框架最低 0.9.90，多语言元数据最低 0.9.94，独立配置页最低 0.9.96，ROM 资源提供者最低 0.9.98。新增专有模拟器协议和脚本存储渠道注册仍需宿主支持，不能在数据包中运行代码。

语言基线、条目数与摘要以 [languages/index.json](languages/index.json) 为准，不用 APK 版本猜测基线，也不要求 reviewed 状态；完整性与兼容性才是安装门槛。[消息上下文](contracts/message-context.json)提供已知界面与参数。只编辑目标语言，不修改中文基线。

在应用设置首页右下角的仓库入口，每行加入一个公开 GitHub 仓库。插件使用“插件 → 商店”；平台使用“设置 → 游戏库与文件夹 → 社区平台”；语言使用“设置 → 主题与显示 → 语言 → 下载语言”。离线 ZIP 从各自导入入口安装。Fork 不会复制上游 Release 资产，必须发布自己的资产后再更新目录。相同内容会合并显示，其他来源由用户明确选择。

扩展不附带 ROM、固件、存档或账号凭据。保留作者及素材许可，只有具有再分发许可的内容可以投稿。预览和自动测试不能替代 Android、模拟器与真实网盘验收。已发布示例及历史见[更新记录](CHANGELOG.md)和[发布说明](RELEASE_NOTES.md)。
