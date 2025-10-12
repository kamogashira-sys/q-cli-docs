# マイグレーションガイド

このガイドでは、Amazon Q CLIのバージョン間での移行方法と、破壊的変更への対応方法を説明します。

## 📋 目次

- [v1.16.x → v1.17.x](#v116x--v117x)
- [v1.15.x → v1.16.x](#v115x--v116x)
- [v1.14.x → v1.15.x](#v114x--v115x)
- [v1.13.x → v1.14.x](#v113x--v114x)
- [一般的な移行手順](#一般的な移行手順)

---

## v1.16.x → v1.17.x

### 概要
v1.17.0では、Knowledge機能のBM25サポート追加とセキュリティ強化が行われました。

### 破壊的変更
なし（後方互換性あり）

### 推奨される変更

#### 1. Knowledge設定の最適化
BM25検索アルゴリズムを活用するための設定追加：

```json
{
  "knowledge": {
    "enabled": true,
    "searchAlgorithm": "bm25",  // 新規追加
    "maxResults": 10
  }
}
```

#### 2. セキュリティ設定の見直し
`execute_bash`権限が厳格化されたため、Agent設定を確認：

```json
{
  "tools": {
    "execute_bash": {
      "enabled": true,
      "allowedCommands": ["ls", "cat", "grep"]  // 明示的に許可
    }
  }
}
```

### 移行手順
1. Amazon Q CLIを最新版にアップデート
2. Knowledge設定に`searchAlgorithm`を追加（オプション）
3. `execute_bash`の許可コマンドを確認・更新
4. `q doctor`で設定を検証

---

## v1.15.x → v1.16.x

### 概要
v1.16.0では、Agent機能の成熟化とMCPのrmcp移行が行われました。

### 破壊的変更

#### MCP設定の変更
旧形式のMCP設定は非推奨となりました。

**旧形式**:
```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "node",
        "args": ["server.js"]
      }
    }
  }
}
```

**新形式（rmcp）**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "transport": "stdio"
    }
  }
}
```

### 推奨される変更

#### 1. Agent管理コマンドの活用
新しいAgent管理コマンドを使用：

```bash
# Agent一覧表示
q agent list

# Agent編集
q agent edit my-agent

# Agent切り替え
q agent use my-agent
```

#### 2. MCP設定の移行
すべてのMCP設定を新形式に移行：

```bash
# 設定ファイルを開く
q settings edit

# mcpServers形式に変更
# transport: "stdio" または "http" を明示
```

### 移行手順
1. Amazon Q CLIを最新版にアップデート
2. MCP設定を新形式に移行
3. Agent設定を確認（スキーマ検証が強化）
4. `q doctor`で設定を検証
5. 各MCPサーバーの動作確認

---

## v1.14.x → v1.15.x

### 概要
v1.15.0では、Knowledge機能の改善とパフォーマンス最適化が行われました。

### 破壊的変更
なし（後方互換性あり）

### 推奨される変更

#### 1. Knowledge設定の最適化
検索精度向上のための設定調整：

```json
{
  "knowledge": {
    "enabled": true,
    "indexing": {
      "chunkSize": 1000,      // 推奨値
      "chunkOverlap": 200     // 推奨値
    },
    "search": {
      "maxResults": 10,
      "minScore": 0.7         // 新規追加
    }
  }
}
```

#### 2. パフォーマンス設定の見直し
メモリ使用量削減のための設定：

```json
{
  "chat": {
    "maxContextTokens": 8000,  // 調整推奨
    "streamingEnabled": true
  }
}
```

### 移行手順
1. Amazon Q CLIを最新版にアップデート
2. Knowledge設定を最適化（オプション）
3. パフォーマンス設定を見直し（オプション）
4. Knowledge Baseの再インデックス（推奨）

---

## v1.13.x → v1.14.x

### 概要
v1.14.0では、セキュリティ強化とUX改善が行われました。

### 破壊的変更

#### ツール権限の厳格化
`fs_read`のデフォルト動作が変更されました。

**変更前**: すべてのファイルへのアクセスが許可
**変更後**: 明示的に許可されたパスのみアクセス可能

### 推奨される変更

#### 1. ツール権限の明示的設定
Agent設定でファイルアクセスを明示：

```json
{
  "tools": {
    "fs_read": {
      "enabled": true,
      "allowedPaths": [
        "~/projects/**",
        "~/documents/**"
      ]
    }
  }
}
```

#### 2. 環境変数の安全な取り扱い
機密情報は環境変数で管理：

```json
{
  "mcpServers": {
    "my-server": {
      "env": {
        "API_KEY": "${env:MY_API_KEY}"
      }
    }
  }
}
```

### 移行手順
1. Amazon Q CLIを最新版にアップデート
2. Agent設定に`allowedPaths`を追加
3. 機密情報を環境変数に移行
4. `q doctor`で設定を検証
5. ファイルアクセスの動作確認

---

## 一般的な移行手順

### 1. バックアップの作成

```bash
# 設定ファイルのバックアップ
cp ~/.local/share/amazon-q/settings.json ~/.local/share/amazon-q/settings.json.backup
cp -r ~/.aws/amazonq/cli-agents ~/.aws/amazonq/cli-agents.backup
```

### 2. アップデート実行

```bash
# Homebrewの場合
brew update
brew upgrade amazon-q

# npmの場合
npm update -g @aws/amazon-q-developer-cli
```

### 3. 設定の検証

```bash
# 設定の診断
q doctor

# Agent設定の確認
q agent list
q agent validate
```

### 4. 動作確認

```bash
# 基本動作の確認
q chat "Hello"

# MCPサーバーの確認
q settings show | grep mcp

# Knowledge機能の確認
q knowledge status
```

### 5. トラブルシューティング

問題が発生した場合：

1. **設定をリセット**:
   ```bash
   q settings reset
   ```

2. **ログを確認**:
   ```bash
   q doctor --verbose
   ```

3. **バックアップから復元**:
   ```bash
   cp ~/.local/share/amazon-q/settings.json.backup ~/.local/share/amazon-q/settings.json
   ```

---

## 📚 関連ドキュメント

- [変更履歴](changelog.md) - バージョン別の変更内容
- [設定ガイド](../../01_for-users/03_configuration/README.md) - 設定の詳細
- [トラブルシューティング](../../01_for-users/06_troubleshooting/README.md) - 問題解決方法

---

## 🆘 サポート

移行に関する問題が発生した場合：

1. [トラブルシューティングガイド](../../01_for-users/06_troubleshooting/02_common-issues.md)を確認
2. [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)で既知の問題を検索
3. 新しいIssueを作成して報告

最終更新: 2025-10-09
