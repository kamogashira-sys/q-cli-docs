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

---

## 🔮 今後追加予定

以下のファイル仕様を順次追加予定です：

### 設定系
- **Agent設定** (`agent.json`) - Agent設定JSONスキーマ
- **MCP設定** (`mcp.json`) - MCPサーバー設定
- **グローバル設定** (`settings.json`) - グローバル設定

### データ系
- **チェックポイント** - チェックポイントファイル形式
- **ナレッジベース** - ナレッジベースファイル形式
- **会話履歴** - チャット会話履歴

### 管理系
- **MCP状態管理** (`mcp-state.json`) - MCP状態ファイル

---

## 🚀 推奨読み順

### ファイル構造を理解したい方
1. **[.cli_bash_history](01_cli-bash-history.md)** - 最もシンプルな形式

### トラブルシューティング
1. **[.cli_bash_history](01_cli-bash-history.md)** - 履歴関連の問題
2. [トラブルシューティング](../06_troubleshooting/) - 一般的な問題

---

## 🔗 関連ドキュメント

### 設定関連
- **[設定ファイル配置マップ](../07_reference/04_configuration-file-locations.md)** - ファイルの配置場所
- **[Configuration](../03_configuration/)** - 設定システム全体

### リファレンス
- **[Reference](../07_reference/)** - その他のリファレンス情報
- **[用語集](../07_reference/01_glossary.md)** - 技術用語の説明

---

作成日: 2025-10-24

---

最終更新: 2025-10-24
