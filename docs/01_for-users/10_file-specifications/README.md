[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [File Specifications](README.md)

---

# File Specifications - ファイル仕様


---

## 📋 このセクションについて

Amazon Q CLIが使用する各種ファイルのフォーマット仕様を提供します。ファイルの内部構造、読み書き方法、管理操作を詳細に解説します。

---

## 🎯 対象ユーザー

- **中級〜上級者**: ファイル構造を理解したい方
- **開発者**: Q CLIの内部動作を知りたい方
- **トラブルシューティング**: ファイル関連の問題を解決したい方

---

## 📚 ファイル仕様一覧

| # | ファイル | 対象ユーザー | 主な内容 |
|---|---------|-------------|---------|
| 1 | [.cli_bash_history](01_cli-bash-history.md) | 中級〜上級 | チャット履歴ファイル、rustyline FileHistory形式 |
| 2 | [Agent設定ファイル](02_agent-configuration.md) | 中級〜上級 | agent.json仕様、JSONスキーマ、フィールド定義 |
| 3 | [MCP設定ファイル](03_mcp-configuration.md) | 中級〜上級 | mcp.json仕様、サーバー設定、環境変数展開 |
| 4 | [グローバル設定ファイル](04_global-settings.md) | 中級〜上級 | settings.json仕様、設定項目、デフォルト値 |
| 5 | [チェックポイント](05_checkpoint.md) | 中級〜上級 | チェックポイントファイル形式、保存・復元操作 |
| 6 | [会話状態](06_conversation_state.md) | 中級〜上級 | 会話状態ファイル形式、メッセージ履歴管理 |
| 7 | [メッセージ構造](07_message_structures.md) | 中級〜上級 | メッセージ構造仕様、コンテンツタイプ、ツール呼び出し |

---

## 🚀 推奨読み順

### ファイル構造を理解したい方
1. **[.cli_bash_history](01_cli-bash-history.md)** - 最もシンプルな形式
2. **[Agent設定ファイル](02_agent-configuration.md)** - Agent設定の詳細
3. **[MCP設定ファイル](03_mcp-configuration.md)** - MCP設定の詳細

### トラブルシューティング
1. **[.cli_bash_history](01_cli-bash-history.md)** - 履歴関連の問題
2. **[会話状態](06_conversation_state.md)** - 会話履歴の問題
3. [トラブルシューティング](../06_troubleshooting/) - 一般的な問題

---

## 🔗 関連ドキュメント

### 設定関連
- **[設定ファイル配置マップ](../07_reference/04_configuration-file-locations.md)** - ファイルの配置場所
- **[Configuration](../03_configuration/)** - 設定システム全体

### リファレンス
- **[Reference](../07_reference/)** - その他のリファレンス情報
- **[用語集](../07_reference/01_glossary.md)** - 技術用語の説明

---

最終更新: 2025-10-27
