[ホーム](../../README.md) > [コミュニティ](../README.md) > [アップデート情報](README.md) > 01 Changelog

---

# 変更履歴（Changelog）

このページでは、Amazon Q CLIの主要なバージョンアップデートと変更内容を記録しています。

## 📋 目次

- [最新バージョン](#最新バージョン)
- [変更カテゴリについて](#変更カテゴリについて)

---

## 最新バージョン

### v1.19.4（2025-11-10）

**主要な変更**:
- 🔧 **リファクタリング**: ディレクトリから階層パスモジュールへの移行 (#3309)
- 📊 **テレメトリー強化**: CLI認証ログイン失敗のテレメトリー追加 (#3317)
- 🔧 **プロンプトファイル改善**: file:// URIでの~展開を修正 (#3301)
- 📁 **モジュール整理**: /Usageコマンドを小さなモジュールに分割 (#3324)
- 🎯 **Agent機能強化**: 重複Agentの警告機能追加 (#3335)
- 🔔 **Delegate UX改善**: 通知機能とファイル変更の改善 (#3337)
- 🛡️ **セキュリティ強化**: ツール呼び出しの危険なパターンをブロック (#3313)
- 🏗️ **コード整理**: Agent crateからchat-cliへのRTSコード移動 (#3340)

**詳細**: [v1.19.4リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.19.4)

---

### v1.19.3（2025-10-29）

**主要な変更**:
- 🐛 **バグ修正**: conduit競合状態、spinner表示、fs-write diff表示の問題を修正
- ✨ **chat stdout出力**: chat出力をstdoutにリダイレクト - パイプライン処理が可能に
- ⏪ **リバート**: モデル更新とパスベースAgent読み込み機能をリバート

**詳細**: [v1.19.3リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.19.3)

---

### v1.19.2（2025-10-28）

**主要な変更**:
- ⏪ **リバート**: モデル更新とendpoint resolverをリバート（v1.19.1の#3262を取り消し）

**詳細**: [v1.19.2リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.19.2)

---

### v1.19.1（2025-10-28）

**主要な変更**:
- 🔧 **非対話モード出力修正**: stderrではなくstdoutに正しく出力
- 🐛 **spinner表示改善**: 色削除とクリーンアップ問題の修正
- 🐛 **fs-write diff表示修正**: 背景に対応した色の修正
- ⏪ **リバート**: パスベースAgent読み込み機能をリバート

**詳細**: [v1.19.1リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.19.1)

---

### v1.19.0（2025-10-25）

**主要な変更**:
- 🎉 **Knowledge PDF対応**: PDFファイルのインデックス化をサポート
- 🖼️ **画像ペースト対応**: チャット内で画像の貼り付けとキーバインディングをサポート
- 🔐 **OAuth redirect URI設定**: 設定可能なOAuth redirect URIを追加
- 🌐 **HTTP MCP headers環境変数**: MCP HTTP headersの環境変数サポート
- 🛡️ **bash tool deny_by_default**: bashコマンドツールのデフォルト拒否モードをサポート
- 🔧 **builtin tool namespace**: ツール権限管理用のビルトイン名前空間を追加
- 📊 **settings list表示改善**: 設定一覧の表示を改善
- 🔍 **/logdump --mcp対応**: MCPオプションをlogdumpコマンドに追加
- 🔄 **--resume動作変更**: --resume指定時のみDBから前回会話を読み込む

**詳細**: [v1.19.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.19.0)

---

### v1.18.1（2025-10-14）

**主要な変更**:
- 🔧 **バージョン報告の修正**: バージョン情報表示の軽微な不具合を修正

**詳細**: [v1.18.1リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/1.18.1)

---

### v1.18.0（2025-10-13）

**主要な変更**:
- 🎉 **[実験的] Delegate Tool**: バックグラウンドで独立して動作するエージェントプロセスの起動・管理機能
- 🔧 **Stop Hook機能**: 会話ターン終了時に実行されるライフサイクルフック
- 📝 **Knowledge コマンド統合**: `/knowledge status` と `/knowledge show` の統合、`--path` と `--name` 引数の追加
- 📄 **PDF対応（Knowledge）**: PDFファイルのインデックス化をサポート
- 🔄 **--resume動作変更**: 明示的な指定時のみ前回の会話を読み込む
- 📁 **file:// URI対応**: Agent promptsで外部ファイル参照をサポート
- 🛠️ **`/logdump` コマンド**: サポート調査用のログファイル収集機能
- ⚙️ **Experiment Manager強化**: 実験的機能の一元管理システムの改善
- 🔌 **MCP Prompts改善**: 引数なしでのMCPプロンプト呼び出しをサポート

**詳細**: [v1.18.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/1.18.0)

---

### v1.17.1（2025-10-01）

**主要な変更**:
- 🔧 **内部改善**: モデルに説明（description）を追加
- 📝 **コードの可読性向上**: コードの保守性を改善

**詳細**: [v1.17.1リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.17.1)

---

### v1.17.0（2025-09-29）

**主要な変更**:
- 🎉 **Knowledge機能のベータ改善**: BM25検索アルゴリズムのサポート追加
- 🔧 **MCP統合の強化**: リモートMCPサーバーのサポート改善
- 🛡️ **セキュリティ強化**: `execute_bash`権限の厳格化
- 🐛 **バグ修正**: 複数の安定性向上

**詳細**: [v1.17.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.17.0)

---

### v1.16.0（2025-09-15）

**Agent機能の成熟化**:
- Agent設定スキーマの改善
- Agent管理コマンドの追加（`q agent list`, `q agent edit`）
- Agent設定の検証機能強化

**MCP進化**:
- rmcpへの移行完了
- OAuth統合の初期サポート
- リモートMCPサーバーの実験的サポート

**詳細**: [v1.16.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.16.0)

---

### v1.15.0（2025-09-02）

> **注**: GitHubのタグ名は`v.1.15.0`（ドット付き）ですが、正式なバージョン番号は`v1.15.0`です。
> - **GitHub Release**: [v.1.15.0](https://github.com/aws/amazon-q-developer-cli/releases/tag/v.1.15.0)
> - **リリース日**: 2025-09-02

**Knowledge機能の改善**:
- Knowledge Baseの検索精度向上
- ファイルインデックス作成の高速化
- 検索結果のランキング改善

**パフォーマンス最適化**:
- チャット応答速度の向上
- メモリ使用量の削減
- 起動時間の短縮

---

### v1.14.0（2025-08-15）

**セキュリティ強化**:
- ツール権限システムの改善
- `fs_read`の制限強化
- 環境変数の安全な取り扱い

**UX改善**:
- エラーメッセージの改善
- プログレス表示の追加
- ヘルプテキストの充実

**詳細**: [v1.14.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.14.0)

---

### v1.13.0（2025-07-31）

**Agent機能の導入**:
- カスタムAgent設定のサポート
- Agent固有のツール権限設定
- Agent切り替え機能（`q chat --agent <name>`、`q agent set-default`）

**MCP統合の開始**:
- Model Context Protocol (MCP)のサポート開始
- MCPサーバー設定の追加
- stdio/HTTP transportのサポート

**詳細**: [v1.13.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.13.0)

---

## 変更カテゴリについて

### 🎉 新機能（Features）
新しい機能の追加や既存機能の大幅な拡張

### 🔧 改善（Improvements）
既存機能のパフォーマンス向上や使いやすさの改善

### 🛡️ セキュリティ（Security）
セキュリティ関連の修正や強化

### 🐛 バグ修正（Bug Fixes）
不具合の修正

### 📚 ドキュメント（Documentation）
ドキュメントの追加や改善

### ⚠️ 破壊的変更（Breaking Changes）
既存の動作を変更する可能性のある変更

---

## 📚 関連ドキュメント

- [ロードマップ](02_roadmap.md) - 今後の開発計画
- [マイグレーションガイド](04_migration-guides.md) - バージョン間の移行方法
- [GitHub Releases](https://github.com/aws/amazon-q-developer-cli/releases) - 公式リリースノート

---

## 🔄 更新頻度

このChangelogは以下のタイミングで更新されます：
- 新しいバージョンのリリース時
- 重要なバグ修正のリリース時
- セキュリティアップデートのリリース時

最終更新: 2025-11-01
