# 拼音首字母搜索 / Pinyin initials search / ピンイン頭文字検索

## 中文

安装 1.0.0 后在插件管理中启用并授权“增强搜索”。需要复古猫 0.9.112。原有游戏库、最近游戏、收藏和应用搜索支持 `hdl` → 魂斗罗、`jsq` → 计算器，大小写不敏感，保留数字及英文片段；简体与繁体都在本机处理。搜索范围、原顺序、版本分组、置顶候选及启动链路保持原规则。不需要重扫 ROM、同步、读取文件正文或联网。

源代码为 source.js，运行入口 main.js 由 `python tools/build_pinyin_plugin.py` 生成。vendor 记录固定依赖、SHA-256 和许可证。使用 pinyin-pro 3.29.5 的 `pinyin({type:'all', toneType:'none', traditional:true})`，对汉字取 first，对其他字符保留 origin，使用官方繁体映射；不通过字符编码区间猜拼音。多音字按词库的上下文读音处理，自定义专名可能需要后续字典更新。

依据：[pinyin 官方 API](https://pinyin-pro.cn/use/pinyin.html)、[繁体映射](https://pinyin-pro.cn/use/traditional.html)。依赖从 npm 中国镜像取得并固定在 vendor，无运行时下载。

## English

Requires RetroMao 0.9.112. Install 1.0.0, enable it in Plugins and grant enhanced search. Existing game/library/recent/favorite and app searches accept Chinese pinyin initials (`hdl` for 魂斗罗, `jsq` for 计算器), preserving Latin text and digits. Simplified and traditional Chinese are processed offline. Existing scope, order, grouping, pinned candidates and launch behavior remain. No ROM scan, sync, file-content reads or network is needed.

Rebuild main.js from source.js and the checksum-verified vendor directory with `python tools/build_pinyin_plugin.py`. Uses pinned pinyin-pro 3.29.5, its official traditional-character mapping, and documented `first`/`origin` fields. Polyphonic characters follow dictionary context; special proper names may need dictionary updates. See the official API links above. Dependencies are bundled, with no runtime downloads.

## 日本語

RetroMao 0.9.112 が必要です。1.0.0 をインストールし、プラグイン管理で有効化して検索拡張を許可します。既存のライブラリ・最近のゲーム・お気に入り・アプリの検索で、中国語ピンインの頭文字を利用できます（hdl → 魂斗罗、jsq → 计算器）。英字と数字を保持し、簡体字・繁体字をオフラインで処理します。範囲、順序、グループ化、ピン留め候補と起動方法は既存の規則に従います。ROM の再走査、同期、ファイル内容の読み取り、通信は不要です。

`python tools/build_pinyin_plugin.py` で source.js とチェックサム付き vendor から main.js を再生成できます。pinyin-pro 3.29.5 と公式の繁体字対応表を固定し、文書化された first／origin フィールドを使います。多音字は辞書の文脈に従い、特殊な固有名詞には今後の辞書更新が必要な場合があります。実行時のダウンロードはありません。
