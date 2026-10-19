# 插件多语言 / Plugin localization / プラグインの多言語化

[中文](#中文) · [English](#english) · [日本語](#日本語)

[Types](retromao.d.ts) · [Template manifest](../templates/plugin/plugin.json)

```javascript
const {locale, appLocale, defaultLocale, locales, messages} = await retromao.ready;
document.getElementById("title").textContent = messages.title;
```

## 中文

最低宿主 0.9.94。defaultLocale 必须显式声明；基础 name、description、pages、actions、settings、messages 就是默认语言，不在 localizations 重复。其他语言最多 31 个，必须包含简中 zh-Hans。用户语言没有对应项时使用插件默认语言，不请求自动翻译。

每种译文的页面、动作、配置、选项、消息键必须与基础语言一致，不能改业务 ID、配置键、作者、版本或路径。messages 最多 1000 项、256 KiB，每条最多 16000 字符。ready 一次返回 locale、appLocale、defaultLocale、locales 和 messages；locale 是实际选择，appLocale 是应用设置。页面自行处理插值、复数、日期与数字，不为每条消息调用 RPC。

工具检查全部语言与最低版本，并只把名称和简介放入商店索引，完整文字留在 ZIP。译文变化同样递增扩展版本；配置与私有数据不因此迁移或清除。文档和模板必须同时提供中英日说明，插件自身可按声明支持更多语言。

## English

Requires host 0.9.94. Declare defaultLocale explicitly. Base name, description, pages, actions, settings and messages form that language; do not repeat it in localizations. Up to 31 additional locales are allowed, and zh-Hans is required. If the app language is unavailable, use the plugin default without automatic translation requests.

Translated page/action/setting/choice/message keys must exactly match the base language. Do not translate IDs, setting keys, author, versions or paths. messages has up to 1000 entries, 256 KiB total and 16000 characters per value. ready returns locale, appLocale, defaultLocale, locales and messages together. locale is the selected plugin language; appLocale is the app preference. Pages handle interpolation, plurals, dates and numbers without per-message RPC.

Tools check locales and minimum versions. Store indexes contain only names/descriptions; full text stays in ZIPs. Translation changes also increment extension versions and do not migrate/clear private data or configuration. Documentation/templates need Chinese, English and Japanese explanations; plugins can declare additional languages.

## 日本語

ホスト 0.9.94 が必要です。defaultLocale を明示してください。基本の name、description、pages、actions、settings、messages が既定言語で、localizations に重複して記載しません。追加言語は最大 31 個で、zh-Hans が必須です。アプリの言語がない場合はプラグインの既定言語を使い、自動翻訳を要求しません。

翻訳されたページ、動作、設定、選択肢、メッセージのキーは基本言語と一致させます。ID、設定キー、作者、バージョン、パスは翻訳しません。messages は最大 1000 項目、合計 256 KiB、各値 16000 文字です。ready は locale、appLocale、defaultLocale、locales、messages をまとめて返します。locale は実際のプラグイン言語、appLocale はアプリの設定です。ページ側で引数展開、複数形、日付、数値を処理し、文章ごとの RPC は行いません。

ツールは言語と最低バージョンを検査します。ストア索引には名称と説明だけを保存し、全文は ZIP 内に残します。翻訳の変更でも拡張のバージョンを上げますが、設定や専用データの移行・消去はしません。文書とテンプレートには中国語、英語、日本語の説明が必要です。プラグイン自体は追加言語も宣言できます。
