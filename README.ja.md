# RetroMao Community｜コミュニティ拡張

[中文](README.md) · [English](README.en.md) · **日本語**

拡張の開発と配布を行う独立したリポジトリです。プラグイン、翻訳、プラットフォームパックの開発にホストのソースコードは必要ありません。Python 3.11 以降を使用してください。プラグインとブラウザーのテストには Node.js 22 以降も必要です。可能であれば先に Python 仮想環境を作成して有効にしてください。コマンドはすべて本リポジトリのルートで実行します。

Fork 後は、固定された依存関係のインストール、リポジトリの検査、テンプレートの作成、プレビュー、パッケージ化の順に進めます。

```text
python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-dev.txt
npm ci --registry=https://registry.npmmirror.com
python tools/retromao.py check
python tools/retromao.py init plugin --id demo-plugin --name Demo --author YourName
python tools/retromao.py check extensions/demo-plugin
python tools/retromao.py preview extensions/demo-plugin
python tools/retromao.py pack extensions/demo-plugin --release-tag demo-plugin-1.0.0
```

プレビューの URL は端末に表示されます。Ctrl+C で終了します。正式 SDK と自分のコードをローカルのサンプルデータで実行し、実際のクラウドには接続しません。[開発と検証](docs/TESTING.md)、[投稿ルール](CONTRIBUTING.md)、[公開手順](docs/PUBLISHING.md)を参照してください。AI アシスタントは先に [AGENTS.md](AGENTS.md) を読んでください。

| 目的 | 開始場所 | 配布形式 |
| --- | --- | --- |
| スクリプトプラグイン | [SDK](sdk/README.md)、templates/plugin | ZIP + plugins/index.json |
| 言語の追加 | [言語ガイド](languages/README.md) | 言語別 JSON + languages/index.json |
| プラットフォームの追加 | [プラットフォーム契約](EXTENSIONS.md)、templates/platform | ZIP + catalog.json |

宣言型の起動設定は形式 2 を使用し、この機能を含むホストビルドが必要です。最低バージョンは 0.9.108 です。正式 APK の検証状況は[機能契約](contracts/host.json)とリリース記録で確認してください。形式 1 に起動設定はありません。スクリプトは 0.9.90、多言語メタデータは 0.9.94、独立設定ページは 0.9.96、ROM リソースプロバイダーは 0.9.98 以降に対応します。独自のエミュレータープロトコルやスクリプトによるストレージプロバイダー登録には、引き続きホスト側の対応が必要です。データパックはコードを実行できません。

言語の基準、項目数、ハッシュは [languages/index.json](languages/index.json) を参照してください。APK のバージョンから基準を推測しないでください。reviewed 状態は必須ではなく、完全性と互換性がインストール条件です。[メッセージのコンテキスト](contracts/message-context.json)には既知の画面と引数があります。中国語の基準を変更せず、対象言語だけを編集してください。

設定画面の右下にあるリポジトリ設定に、公開 GitHub リポジトリを 1 行に 1 つ追加します。プラグインは「プラグイン → ストア」、プラットフォームは「設定 → ゲームライブラリとフォルダー → コミュニティプラットフォーム」、言語は「設定 → テーマと表示 → 言語 → 言語をダウンロード」から利用します。オフライン ZIP は対応するインポート機能で読み込みます。Fork しても上流の Release アセットは複製されません。自分のアセットを公開してからカタログを更新してください。同一内容は表示時にまとめられ、異なる配布元は利用者が明示的に選択します。

ROM、ファームウェア、セーブデータ、認証情報を配布しないでください。作者名と素材のライセンスを保持し、再配布可能な内容だけを投稿してください。プレビューと自動テストは Android、エミュレーター、実際のクラウドでの検証を代替しません。公開済みサンプルと履歴は[更新履歴](CHANGELOG.md)と[リリースノート](RELEASE_NOTES.md)を参照してください。
