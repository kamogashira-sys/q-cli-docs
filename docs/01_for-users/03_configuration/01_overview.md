[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [設定ガイド](README.md) > 01 Overview

---

# 設定システム概要

Amazon Q CLIの設定システムの全体像を理解するためのガイドです。

## 📋 目次

- [設定システムとは](#設定システムとは)
- [設定の種類](#設定の種類)
- [設定の優先順位](#設定の優先順位)
- [設定ファイルの場所](#設定ファイルの場所)
- [次のステップ](#次のステップ)

---

## 設定システムとは

Amazon Q CLIの設定システムは、以下の要素で構成されています：

### 主要コンポーネント
1. **グローバル設定** - すべてのセッションに適用される基本設定
2. **Agent設定** - カスタムAgentごとの個別設定
3. **MCP設定** - Model Context Protocolサーバーの統合設定
4. **環境変数** - 動的な設定値の注入

---

## 設定の種類

### 1. グローバル設定
すべてのQ CLIセッションに適用される基本設定。

**設定ファイル**: `~/.local/share/amazon-q/settings.json`

**主要設定項目**:
- テレメトリ設定
- チャット設定
- Knowledge設定
- デフォルトAgent

詳細: [グローバル設定](02_global-settings.md)

### 2. Agent設定
特定のタスクやプロジェクト用のカスタム設定。

**設定ファイル**: `~/.config/amazonq/agents/<agent-name>.json`

**主要設定項目**:
- Agent名と説明
- ツール権限
- MCP統合
- プロンプトカスタマイズ

詳細: [Agent設定](03_agent-configuration.md)

### 3. MCP設定
外部ツールやサービスとの統合設定。

**設定場所**: Agent設定内の`mcpServers`セクション

**主要設定項目**:
- サーバー接続情報
- 認証設定
- 環境変数

詳細: [MCP設定](04_mcp-configuration.md)

### 4. 環境変数
動的な設定値の注入と機密情報の管理。

**使用方法**: `${env:VARIABLE_NAME}`構文

詳細: [環境変数](06_environment-variables.md)

---

## 設定の優先順位

設定は以下の優先順位で適用されます（上が優先）：

```
1. コマンドライン引数
   ↓
2. 環境変数
   ↓
3. Agent設定
   ↓
4. グローバル設定
   ↓
5. デフォルト値
```

詳細: [設定優先順位](07_priority-rules.md)

---

## 設定ファイルの場所

> **💡 このセクションについて**
> 
> このセクションの情報は、Q CLIのソースコード調査と実際のファイルシステム構造の確認に基づいています。
> 
> **検証方法**:
> - Q CLIソースコードでディレクトリパスを確認
> - 実際のインストール環境でファイル配置を検証
> - プラットフォーム別（macOS/Linux/Windows）のパス差異を確認

### グローバル設定ディレクトリ

Amazon Q CLIの設定ファイルは、グローバル（ユーザー全体）とローカル（ワークスペース固有）の2つのレベルで管理されます。

```
~/.aws/amazonq/
├── cli-agents/              # Agent設定ファイル（グローバル）
├── cli-checkpoints/         # チェックポイントファイル
├── history/                 # チャット履歴
├── knowledge_bases/         # ナレッジベース
├── prompts/                 # プロンプト設定
├── .cli_bash_history        # CLI履歴
└── mcpAdmin/                # MCP管理ファイル
    └── mcp-state.json       # MCP状態管理
```

### ローカル設定ディレクトリ（ワークスペース固有）

```
<workspace>/
└── .amazonq/
    ├── cli-agents/          # Agent設定ファイル（ローカル）
    ├── prompts/             # プロンプト設定（ローカル）
    ├── rules/               # ルールファイル
    └── cli-todo-lists/      # TODOリスト
```

### 設定ファイルの優先順位

1. **ローカル設定**: `.amazonq/cli-agents/` （カレントディレクトリ）
2. **グローバル設定**: `~/.aws/amazonq/cli-agents/` （ホームディレクトリ）

同名のAgentが存在する場合、ローカル設定が優先され、警告メッセージが表示されます。

### プラットフォーム別の場所

#### macOS/Linux
```
~/.aws/amazonq/              # グローバル設定
~/.local/share/amazon-q/     # アプリケーションデータ
  └── settings.json          # グローバル設定ファイル
```

#### Windows
```
%USERPROFILE%\.aws\amazonq\  # グローバル設定
%LOCALAPPDATA%\amazon-q\     # アプリケーションデータ
  └── settings.json          # グローバル設定ファイル
```

---

## 設定の基本操作

> **💡 このセクションについて**
> 
> このセクションのコマンドは、`q --help-all`の出力に基づいています。
> 
> **出典**: [コマンドリファレンス](../07_reference/02_commands.md) - `q --help-all`の完全な出力を整理したリファレンス

### 設定の表示
```bash
# すべての設定を表示
q settings show

# 特定の設定を表示
q settings show chat.maxContextTokens
```

### 設定の変更
```bash
# 設定ファイルを開く
q settings edit

# 特定の設定を変更
q settings set chat.maxContextTokens 10000
```

### Agent管理
```bash
# Agent一覧
q agent list

# Agent切り替え
q agent use my-agent

# Agent編集
q agent edit my-agent
```

---

## 設定のベストプラクティス

### 1. 段階的な設定
1. まずデフォルト設定で使用開始
2. 必要に応じてグローバル設定を調整
3. 特定用途にはAgentを作成

### 2. セキュリティ
- 機密情報は環境変数で管理
- ツール権限は最小限に
- ファイルアクセスは明示的に許可

### 3. パフォーマンス
- コンテキストトークン数を調整
- Knowledge設定を最適化
- 不要な機能は無効化

詳細: [ベストプラクティス](../04_best-practices/01_configuration.md)

---

## トラブルシューティング

問題が発生した場合は、[トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)を参照してください。

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

### より詳細なトラブルシューティング

コンテキスト管理に関する包括的なトラブルシューティングガイドは、[コンテキスト管理ガイド - トラブルシューティング編](../08_guides/06_troubleshooting.md)を参照してください。

**主なトピック**:
- コンテキストが反映されない問題
- トークン使用量が高い問題
- Agent起動が遅い問題
- ファイルが読み込まれない問題
- パフォーマンス最適化

---

## 次のステップ

### 初心者向け
1. [グローバル設定](02_global-settings.md)を確認
2. [設定例](08_examples.md)を参考に調整
3. [環境変数](06_environment-variables.md)の使い方を学ぶ

### 中級者向け
1. [Agent設定](03_agent-configuration.md)でカスタムAgentを作成
2. [MCP設定](04_mcp-configuration.md)で外部ツールを統合
3. [優先順位ルール](07_priority-rules.md)を理解

### 上級者向け
1. [設定システム詳細](../../02_for-developers/02_architecture/02_configuration-system.md)を学ぶ
2. 複雑な設定パターンを実装
3. カスタムMCPサーバーを開発

### コンテキスト管理を深く学ぶ

コンテキスト管理の詳細なガイドは、[コンテキスト管理完全ガイド](../08_guides/README.md)を参照してください：

| ガイド | 内容 |
|--------|------|
| [本質編](../08_guides/01_essence.md) | コンテキストとは何か |
| [仕組み編](../08_guides/02_mechanism.md) | 内部動作の理解 |
| [効果編](../08_guides/03_effects.md) | 何ができるか |
| [ベストプラクティス編](../08_guides/04_best-practices.md) | 設計原則と実装パターン |
| [実践ガイド編](../08_guides/05_practical-guide.md) | プロジェクト別実装例 |
| [トラブルシューティング編](../08_guides/06_troubleshooting.md) | 問題解決 |
| [上級編](../08_guides/07_advanced.md) | 最適化とチーム開発 |
| [リファレンス編](../08_guides/08_reference.md) | 技術仕様とFAQ |

**学習パス**:
- **初心者**: 本質編 → 効果編 → 実践ガイド編
- **中級者**: ベストプラクティス編 → 実践ガイド編 → トラブルシューティング編
- **上級者**: 上級編 → リファレンス編

---

## 📚 関連ドキュメント

- **[設定項目リファレンス](../07_reference/03_settings-reference.md)**
- **[環境変数リファレンス](../03_configuration/06_environment-variables.md)**
- **[コマンドリファレンス](../07_reference/02_commands.md)**

---

最終更新: 2025-10-09
