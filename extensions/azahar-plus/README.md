# Azahar Plus 1.0.0

## 中文

作者：4NPC。这是可安装的复古猫插件 ZIP，需要包含[模拟器插件接口](../../sdk/EMULATOR_PLUGINS.md)的宿主 0.9.136 或更新版本；不能安装到旧版后冒充支持。它没有执行脚本、额外网络权限、游戏或模拟器安装包。

在「插件 → 已安装」导入 ZIP 并启用，再到「设置 → 模拟器 → Nintendo 3DS」选择对应配置。共存版显示 `+AzaharPlus+`，包名 `io.github.azaharplus.android`；替换版显示 `AzaharPlus`，包名 `io.github.lime3ds.android`。用户仍须安装模拟器、完成初始化，并准备自己有权使用的 ROM。支持原 3DS 目录的 `.3ds`、`.cci`、`.cxi`、`.app` 启动候选，文件内容能否运行由模拟器判断。

官方依据为 [2126.2-A 发布](https://github.com/AzaharPlus/AzaharPlus/releases/tag/AZAHAR_PLUS_2126_2_A)、[公开 Activity](https://github.com/AzaharPlus/AzaharPlus/blob/AZAHAR_PLUS_2126_2_A/src/android/app/src/main/AndroidManifest.xml) 与 [URI 读取](https://github.com/AzaharPlus/AzaharPlus/blob/AZAHAR_PLUS_2126_2_A/src/android/app/src/main/java/org/citra/citra_emu/fragments/EmulationFragment.kt)。已读取两份官方发布 APK 的 Manifest：共存版 SHA-256 为 `cf6047efe1dd019fb15c6b2cbdc2bcdc92330f3975f500fe42361745dcdba8c6`，替换版为 `9aaf2ecdedd3aded560504196c5709c7c185d71990c72e8b20b57342d0496dcd`；不以默认源码分支的包名替代发布包口径。

本地生成 ZIP 不等于已经公开上架或完成真机进入游戏验收。宿主构建及自动检查记录另列，实际设备启动仍须验收。

## English

By 4NPC. This installable RetroMao plugin ZIP requires host 0.9.136 or later with the [emulator plugin contract](../../sdk/EMULATOR_PLUGINS.md). Older hosts cannot use it. It includes no executable script, network permission, emulator or game.

Import and enable the ZIP under Plugins → Installed, then select its Nintendo 3DS profile in Settings → Emulators. The coexist build is `+AzaharPlus+` (`io.github.azaharplus.android`); the replacement build is `AzaharPlus` (`io.github.lime3ds.android`). Install and initialize the emulator separately and provide ROMs you are entitled to use. Existing `.3ds`, `.cci`, `.cxi` and `.app` entries pass through the standard ROM launch flow. The emulator decides whether their contents can run.

The linked official 2126.2-A release, exported Activity and URI reader are the protocol sources. Both official APK manifests were inspected; their SHA-256 values are recorded above. A local ZIP is not a store release or proof of actual gameplay. Record host checks and device gameplay separately.

## 日本語

作者：4NPC。[エミュレータープラグイン仕様](../../sdk/EMULATOR_PLUGINS.md)に対応するホスト 0.9.136 以降が必要な、インストール可能な ZIP です。旧ホストでは使用できません。実行スクリプト、ネットワーク権限、エミュレーター本体、ゲームは含みません。

プラグイン → インストール済みから ZIP を読み込み、有効にしてください。設定 → エミュレーター → Nintendo 3DS で起動設定を選択します。共存版は `+AzaharPlus+`（`io.github.azaharplus.android`）、置換版は `AzaharPlus`（`io.github.lime3ds.android`）です。本体のインストールと初期設定は別途必要です。利用権限のある `.3ds`、`.cci`、`.cxi`、`.app` を既存の ROM 起動処理に渡し、内容の実行可否はエミュレーターが判断します。

上記の公式 2126.2-A リリース、公開 Activity、URI 読み取り処理を確認し、両 APK の Manifest と SHA-256 を照合しています。ローカル ZIP の作成はストア公開や実機でのゲーム起動成功を意味しません。ホストの検証と実際のゲーム起動は分けて記録します。
