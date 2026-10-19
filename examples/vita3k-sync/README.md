# Vita3K ROM 同步 / Vita3K ROM sync / Vita3K ROM 同期

[中文](#中文) · [English](#english) · [日本語](#日本語)

[ROM resources](../../sdk/ROM_RESOURCES.md)

## 中文

作者 4NPC，插件 1.0.0，最低宿主 0.9.98。安装后在宿主配置页选择 Vita3K 的实际授权目录并启用。不需要插件自己的网盘或同步按钮；原系统 ROM 上传、下载和批量同步会带上对应游戏本体、补丁、DLC、许可。

可选择包含 ux0 的根本身，或其上层 fs、vita、files/fs、files/vita 结构。另一终端也需启用并选择自己的目录。仅处理本次同步的 .psvita 游戏，不扫描其他游戏，不处理存档、固件、配置、缓存。没有启用的终端保留云端记录，继续原标题与媒体同步。

进度、取消和恢复在宿主任务卡片操作，游戏启动不等同步。通用开发契约和官方结构依据见下方资源提供者文档。实际设备、文档提供方和网盘双端操作不能由样本测试替代。

## English

By 4NPC, plugin 1.0.0, minimum host 0.9.98. Select the actual authorized Vita3K directory in host configuration and enable the plugin. There is no separate cloud configuration or sync button: normal ROM uploads, downloads and batches include the selected game's base content, patches, DLC and licenses.

Select the ux0 root or its parent structure containing fs, vita, files/fs or files/vita. Enable and configure the other device's own directory too. Only selected .psvita games are processed; other games, saves, firmware, configuration and caches are excluded. A disabled device preserves remote records and continues existing title/media sync.

Use host task cards for progress, cancellation and recovery. Game launch does not wait. The resource-provider document below defines the contract and official layout evidence. Fixture tests do not replace actual devices, document providers or two-device cloud operations.

## 日本語

作者は 4NPC、プラグイン 1.0.0、最低ホスト 0.9.98 です。ホストの設定で実際の Vita3K ディレクトリに権限を与えて選択し、有効にします。専用のクラウド設定や同期ボタンはありません。通常の ROM アップロード、ダウンロード、一括同期で対象の本体、パッチ、DLC、ライセンスを扱います。

ux0 のルート自体、または fs、vita、files/fs、files/vita を含む上位構造を選択します。もう一方の端末でも有効化し、その端末のディレクトリを設定してください。今回の .psvita ゲームだけが対象で、他のゲーム、セーブ、ファームウェア、設定、キャッシュは除外します。無効な端末はクラウド記録を保持し、従来のタイトルとメディア同期を続けます。

進捗、キャンセル、復旧はホストのタスクカードを使い、ゲーム起動は待ちません。契約と公式構造の根拠は下のリソースプロバイダー文書を参照してください。サンプルテストは実機、文書プロバイダー、二端末の実クラウド操作を代替しません。
