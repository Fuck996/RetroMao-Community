# 插件 ROM 资源提供者

最低宿主版本 0.9.98。插件定位已安装游戏等外部资源，宿主沿用系统 ROM 同步的资源计划、网盘适配器、文件读写、持久任务、哈希缓存及索引提交。插件不创建另一套同步任务，不传输大文件正文，不选择另一网盘。

## 声明与解析

在 `plugin.json` 的 `settings` 中声明 `DIRECTORY` 字段，宿主使用系统目录选择器取得并持久保存读写授权；配置无需启用插件即可编辑。通过 `resourceProviders` 声明平台、ROM 扩展名、目录字段、候选存储子目录及结构标记：

```json
{
  "capabilities": ["ROM_RESOURCES"],
  "settings": [{"id":"directory","label":"模拟器目录","kind":"DIRECTORY"}],
  "resourceProviders": [{
    "id":"installed","platformId":"psv","extensions":["psvita"],
    "directorySetting":"directory","rootPaths":["","fs","vita","files/fs","files/vita"],
    "rootMarker":"ux0","formatVersion":1
  }]
}
```

脚本通过 `retromao.define({resources:{installed: resolver}})` 注册与提供者 ID 对应的解析函数。输入 `{games:[{gameId,romNames}]}`，输出 `[{gameId,key,paths:[{path,required}]}]`。所有路径均相对定位后的存储根目录；不得返回绝对路径、URI 或 `..`。`required` 为 true 的目录缺失时，此资源计划明确失败；不存在的可选目录不产生文件任务。

宿主仅在用户已选择 ROM 同步、插件已启用并获准使用 `ROM_RESOURCES` 且目录已配置时调用。上传每次最多向一个解析函数传入 100 个游戏，只返回目录范围；宿主枚举这些范围并保存文件清单。下载使用远端索引，不运行上传解析脚本或枚举整个游戏树。

自动解析不作为插件动作出现在业务按钮中。纯资源插件无需业务页面或手动动作，沿用宿主配置、启用、授权与卸载界面。Vita3K 示例只有一个目录字段，网盘及库位置来自本次系统同步已确认的映射。

## 数据与任务

- 自有游戏库索引版本 13 增加 `romResources`。每组包含提供者插件 ID、资源键、格式版本、常规文件记录以及文件 ID 对应的本地相对路径；不包含本机目录授权 URI。
- 插件资源与启动 ROM、媒体分别保存。它们不会作为启动候选、刮削指纹或多 ROM 版本进入游戏启动链路。
- 远端文件存放在原 ROM 映射根内的 `.retromao/resources/<插件ID>/<资源键>/`，复用同一库索引和文件回执。没有私有云端索引或远端任务日志。
- 另一终端依据自己的目录配置写入。未安装、禁用或未配置插件的终端只同步原有标题索引和媒体，写回时保留已索引的扩展资源，不能把未启用的资源组视为删除。
- 已解析文件范围随原任务检查点保存。恢复已解析任务不再次运行解析函数；取消保留原流程已写入并确认的文件。解析完毕的文件传输属于宿主任务，使用系统任务卡片取消；禁用插件停止新任务的资源解析。

索引版本 13 由 0.9.98 及更新宿主识别；未安装插件不影响该宿主识别和保留资源组。更旧的 APK 需要升级，不能将未知格式按旧索引覆盖。

## 工作量边界

每轮仅定位本次游戏的相关目录，共用文件提交器的 `DocumentTree` 枚举缓存。目录结构定位不读取游戏正文。首次或实际内容变化时沿原流程计算哈希；有效缓存继续复用，不逐文件获取远端 MD5，不为扩展资源另读写库索引。文件流、并发、速度、检查点、取消和提交均沿原资源队列处理。

首次定位范围是新增资源能力的必要工作，不是额外全盘扫描；已解析范围写入本机任务一次，用于恢复，不新增逐文件远端索引提交。游戏启动不调用该提供者，也不等待其任务。

## Vita3K 示例

源码见 [vita3k-sync](../examples/vita3k-sync/)，作者 4NPC，插件版本 1.0.0，内含简中、繁中、英语及日语。选中的 Vita3K 目录可为存储根本身，或包含 `fs`、`vita`、`files/fs`、`files/vita` 的目录。根目录须能唯一定位到 `ux0`；同一个目录下存在多套存储时，选择实际使用的那一套。

按 `.psvita` 文件名中的标题 ID 纳入 `ux0/app`、`ux0/patch`、`ux0/addcont`、`ux0/license` 下对应游戏的内容，不包含其他游戏、存档、固件、模拟器配置和缓存。布局核对来源为 [Vita3K 官方安装源码](https://github.com/Vita3K/Vita3K/blob/f0273e4cd9b860ea77c44c73d9f5c5b1ed5fa8ab/vita3k/interface.cpp)及[许可源码](https://github.com/Vita3K/Vita3K/blob/f0273e4cd9b860ea77c44c73d9f5c5b1ed5fa8ab/vita3k/packages/src/license.cpp)。

两端都须安装插件并设置各自目录才能双向传输本体。目录访问依赖系统授权或模拟器提供的文档入口，不通过固定字符串路径绕过 Android 权限。自动化检查不替代实际 Vita3K 版本、Android 文档提供方与网盘的双端运行验收。
