# 自定义启动入口 / Custom launch entries / カスタム起動設定 1.1.0

## 中文

作者：4NPC。需要复古猫 0.9.141 或更新版本。从插件商店安装并授权「模拟器」，在已安装插件中打开「启动入口」。选择平台，填写入口名称、应用包名和完整 Activity；新增默认预填 Azahar Plus。保存后可设为平台默认，也可在游戏的模拟器选择中使用。支持编辑、删除，同来源插件更新保留已保存参数；删除全部入口后不会自动恢复预设。

高级参数支持 Action、MIME、ROM Data、类型明确的 JSON 附加参数和四种 Activity 标志。`{romUri}` 替换为当前选中的 ROM URI。仅沿用宿主实际拥有的只读授权，不提供命令行、任意文件路径或直接启动 API。具体限制见 [SDK 调用手册](../../sdk/API_REFERENCE.md) 和 [启动契约](../../sdk/EMULATOR_PLUGINS.md)。

默认共存版包名 `io.github.azaharplus.android`，替换版为 `io.github.lime3ds.android`；完整 Activity 为 `org.citra.citra_emu.activities.EmulationActivity`。依据 [Azahar Plus 2126.2-A](https://github.com/AzaharPlus/AzaharPlus/releases/tag/AZAHAR_PLUS_2126_2_A) 的发布 APK Manifest 与公开 URI 读取接口。模拟器初始化和游戏文件由用户准备。自动检查、样本预览、实机安装与进入游戏分别验收。

## English

By 4NPC. Requires RetroMao 0.9.141 or later. Install from the plugin store, grant Emulators and open Launch entries. Choose a platform and enter a name, package and full Activity. New entries are prefilled with Azahar Plus. Save, select a platform default or choose the entry from a game's emulator selector. Edit/delete operations persist across same-source updates; deleting all entries does not restore presets.

Advanced settings include Action, MIME, ROM Data, typed JSON extras and four Activity flags. `{romUri}` becomes the selected ROM URI using the host's existing read-only grants. There is no shell, arbitrary path access or direct-launch API. See the linked SDK reference and launch contract. The coexist package is `io.github.azaharplus.android`, the replacement package `io.github.lime3ds.android`, and Activity `org.citra.citra_emu.activities.EmulationActivity`, verified against the linked official 2126.2-A APKs and URI reader. Initialize the emulator and supply game files separately. Automated checks, fixture previews, device installation and gameplay are separate acceptance stages.

## 日本語

作者：4NPC。復古猫 0.9.141 以降が必要です。ストアからインストールしてエミュレーター権限を許可し、起動設定を開きます。プラットフォーム、設定名、パッケージ名、完全な Activity を指定します。初期値は Azahar Plus です。保存後は既定やゲームのエミュレーター選択で使用できます。同じ配布元の更新でも編集を保持し、全件削除後に初期値を復元しません。

詳細設定は Action、MIME、ROM Data、型付き JSON 追加値、四種の Activity フラグに対応します。`{romUri}` を選択した ROM の URI に置換し、既存の読取専用許可を使用します。シェル、任意パス、直接起動 API は提供しません。制約は SDK リファレンスと起動仕様を参照してください。共存版は `io.github.azaharplus.android`、置換版は `io.github.lime3ds.android`、Activity は `org.citra.citra_emu.activities.EmulationActivity` です。公式 2126.2-A APK と URI 読取処理を確認しています。本体の初期設定とゲームは別途必要です。自動検査、サンプル表示、実機インストール、ゲーム実行は分けて検証します。
