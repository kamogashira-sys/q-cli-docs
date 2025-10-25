[ホーム](../../README.md) > [コミュニティ](../README.md) > [アップデート情報](README.md) > 04 Migration Guides

---

# マイグレーションガイド

このガイドでは、Amazon Q CLIのバージョン間での移行方法と、破壊的変更への対応方法を説明します。

## 📋 目次

- [v1.18.x → v1.19.0](#v118x--v1190)
- [v1.17.x → v1.18.x](#v117x--v118x)
- [v1.16.x → v1.17.x](#v116x--v117x)
- [v1.15.x → v1.16.x](#v115x--v116x)
- [v1.14.x → v1.15.x](#v114x--v115x)
- [v1.13.x → v1.14.x](#v113x--v114x)
- [一般的な移行手順](#一般的な移行手順)

---

## v1.18.x → v1.19.0

### 概要
v1.19.0では、Knowledge PDF対応、画像ペースト機能、セキュリティ強化（bash tool deny_by_default）など、9つの主要な機能追加・変更が行われました。

### 破壊的変更

#### 1. `--resume`動作の変更（重要）
**変更内容**: `--resume`フラグを明示的に指定した場合のみ、前回の会話をデータベースから読み込むように変更されました。

**変更前（v1.18.x以前）**:
```bash
q chat "続きを教えて"  # 自動的に前回の会話を継続
```

**変更後（v1.19.0+）**:
```bash
q chat "続きを教えて"           # 新しい会話として開始
q chat --resume "続きを教えて"  # 前回の会話を継続（明示的指定が必要）
```

**影響範囲**:
- スクリプトやエイリアスで会話継続を前提としている場合、`--resume`フラグの追加が必要
- 対話的な使用では、意図しない会話継続を防げるため、より予測可能な動作に

#### 2. bash toolのデフォルト動作変更（セキュリティ強化）
**変更内容**: `deny_by_default`モードが追加され、bashコマンドの実行がデフォルトで拒否されるようになりました。

**変更前**: すべてのbashコマンドが実行可能
**変更後**: 明示的に許可されたコマンドのみ実行可能

### 推奨される変更

#### 1. 会話継続の明示化
スクリプトやエイリアスで会話継続を使用している場合、`--resume`を追加：

**更新前**:
```bash
# エイリアス例
alias qc='q chat'
```

**更新後**:
```bash
# 会話継続用エイリアス
alias qc='q chat'
alias qcr='q chat --resume'  # 会話継続用
```

#### 2. bash tool権限の明示的設定
Agent設定でbashコマンドの許可リストを定義：

```json
{
  "tools": {
    "execute_bash": {
      "enabled": true,
      "denyByDefault": true,
      "allowedCommands": [
        "ls", "cat", "grep", "find",
        "git status", "git log", "git diff",
        "npm test", "npm run build"
      ]
    }
  }
}
```

**セキュリティベストプラクティス**:
- 必要最小限のコマンドのみ許可
- ワイルドカード（`*`）の使用は避ける
- 定期的に許可リストを見直す

#### 3. Knowledge PDF機能の活用
PDFドキュメントをナレッジベースに追加：

**Knowledge機能の有効化**:
```bash
# Knowledge機能を有効化
q settings chat.enableKnowledge true
```

Knowledge機能が有効な場合、Q CLIは自動的にプロジェクトディレクトリ内のPDFファイルをインデックス化します。

**対応フォーマット**:
- PDF（新規対応）
- Markdown
- テキストファイル
- ソースコード

#### 4. 画像ペースト機能の活用
チャット内で画像を直接貼り付け：

```bash
# チャットを開始
q chat

# チャット内でキーバインディングを使用
# Ctrl+V または Cmd+V で画像を貼り付け
```

**使用例**:
- スクリーンショットの共有
- エラー画面の説明
- 図表の分析依頼

#### 5. OAuth redirect URI設定（オプション）
カスタムOAuth redirect URIを設定する場合：

```bash
# 環境変数で設定
export Q_OAUTH_REDIRECT_URI="http://localhost:8080/callback"

# または設定ファイルで指定
q settings auth.oauthRedirectUri "http://localhost:8080/callback"
```

#### 6. HTTP MCP headers環境変数の活用
MCP HTTPヘッダーを環境変数で管理：

```json
{
  "mcpServers": {
    "my-api": {
      "transport": "http",
      "url": "https://api.example.com",
      "headers": {
        "Authorization": "${env:API_TOKEN}",
        "X-Custom-Header": "${env:CUSTOM_VALUE}"
      }
    }
  }
}
```

#### 7. builtin tool namespaceの活用
ツール権限を名前空間で管理：

```json
{
  "tools": {
    "builtin:fs_read": {
      "enabled": true,
      "allowedPaths": ["~/projects/**"]
    },
    "builtin:execute_bash": {
      "enabled": true,
      "denyByDefault": true,
      "allowedCommands": ["ls", "cat"]
    }
  }
}
```

#### 8. /logdump --mcpオプションの活用
MCPサーバーのログも含めて収集：

```bash
# 通常のログダンプ
/logdump

# MCPログも含める
/logdump --mcp
```

### 互換性
- **既存の設定**: すべて引き続き動作（bash tool権限は要確認）
- **既存のコマンド**: `--resume`なしの場合、新しい会話として開始される
- **実験的機能**: 引き続き利用可能

### 移行手順

#### 必須手順
1. **Q CLIをv1.19.0にアップグレード**
   ```bash
   brew update && brew upgrade amazon-q
   # または
   npm update -g @aws/amazon-q-developer-cli
   ```

2. **bash tool権限の設定**
   ```bash
   # Agent設定を編集
   q agent edit
   
   # allowedCommandsを追加
   # 上記の「bash tool権限の明示的設定」を参照
   ```

3. **動作確認**
   ```bash
   # 新しい会話の開始
   q chat "Hello"
   
   # 会話継続の確認
   q chat --resume "続きを教えて"
   
   # bash実行の確認
   q chat "lsコマンドを実行して"
   ```

#### オプション手順
4. **会話継続エイリアスの追加**（推奨）
   ```bash
   # ~/.bashrc または ~/.zshrc に追加
   alias qcr='q chat --resume'
   ```

5. **PDF Knowledge機能の試用**（オプション）
   ```bash
   q knowledge add --name docs --path /path/to/pdfs
   ```

6. **画像ペースト機能の試用**（オプション）
   ```bash
   q chat
   # Ctrl+V で画像を貼り付け
   ```

### トラブルシューティング

#### 問題1: bashコマンドが実行できない
**症状**: `execute_bash`ツールが拒否される

**解決方法**:
```json
{
  "tools": {
    "execute_bash": {
      "enabled": true,
      "denyByDefault": false  // 一時的に無効化（非推奨）
    }
  }
}
```

または、許可リストを追加（推奨）：
```json
{
  "tools": {
    "execute_bash": {
      "enabled": true,
      "denyByDefault": true,
      "allowedCommands": ["必要なコマンドを追加"]
    }
  }
}
```

#### 問題2: 会話が継続されない
**症状**: 前回の会話が読み込まれない

**解決方法**:
```bash
# --resumeフラグを追加
q chat --resume "続きを教えて"
```

#### 問題3: PDFがインデックス化されない
**症状**: PDFファイルがKnowledgeに追加されない

**解決方法**:
```bash
# ファイルパスを確認
ls -la /path/to/pdf

# Knowledge機能が有効か確認
q settings chat.enableKnowledge

# Knowledge設定を確認
q settings list | grep knowledge
```

### セキュリティ上の注意

#### bash tool deny_by_defaultの重要性
- **デフォルトで有効化を推奨**: セキュリティリスクを最小化
- **許可リストは最小限に**: 必要なコマンドのみ許可
- **定期的な見直し**: 不要になったコマンドは削除

#### 環境変数の安全な管理
- **機密情報は環境変数で**: 設定ファイルに直接記載しない
- **`.env`ファイルの除外**: `.gitignore`に追加
- **権限の適切な設定**: `chmod 600 ~/.env`

---

## v1.17.x → v1.18.x

### 概要
v1.18.0では、Delegate Tool、Stop Hook、Knowledge コマンド統合、/logdump コマンドなど、6つの主要な新機能が追加されました。

### 破壊的変更
なし（後方互換性あり）

### 推奨される変更

#### 1. Knowledgeコマンドの更新
`/knowledge status` と `/knowledge show` が統合されました：

**旧コマンド（v1.17.x以前）**:
```
/knowledge status  # バックグラウンド処理の状態
/knowledge show    # ナレッジベース情報を表示
```

**新コマンド（v1.18.0+）**:
```
/knowledge show    # statusとshowが統合（エントリと操作の両方を表示）
```

**新しい引数オプション**:
```
/knowledge add -n myproject -p /path/to/project
/knowledge add --name docs --path /path/to/docs
```

#### 2. 実験的機能の有効化（オプション）
新しい実験的機能を試す場合：

```bash
# Delegate Toolを有効化
q settings chat.enableDelegate true

# または /experiment コマンドで有効化
/experiment
# メニューから「Delegate」を選択
```

#### 3. Stop Hookの追加（オプション）
会話ターン終了時に自動処理を実行したい場合、Agent設定にStop Hookを追加：

```json
{
  "hooks": {
    "stop": {
      "command": "npm run format",
      "timeout": 30000
    }
  }
}
```

**使用例**:
- コンパイル: `"command": "cargo build"`
- テスト実行: `"command": "npm test"`
- フォーマット: `"command": "prettier --write ."`

#### 4. ログ収集の活用
トラブルシューティング時に新しい `/logdump` コマンドを使用：

```
/logdump
```

ZIPファイルが生成され、サポートチームへの提出が容易になります。

### 互換性
- **既存の設定**: すべて引き続き動作
- **既存のコマンド**: 変更なし（`/knowledge status` は削除されましたが、`/knowledge show` で同等の機能を提供）
- **実験的機能**: デフォルトで無効のため、既存のワークフローに影響なし

### 移行手順
1. Q CLIをv1.18.0にアップグレード
2. `/knowledge status` を使用している場合は `/knowledge show` に変更
3. 必要に応じて新機能を有効化（オプション）

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
q agent edit --name my-agent

# デフォルトAgent設定
q agent set-default
```

#### 2. MCP設定の移行
すべてのMCP設定を新形式に移行：

```bash
# 設定ファイルを開く
q settings open

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

> **注**: GitHubのタグ名は`v.1.15.0`（ドット付き）です。

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
q settings list | grep mcp

# Knowledge機能の確認
q settings chat.enableKnowledge
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

- [変更履歴](01_changelog.md) - バージョン別の変更内容
- [設定ガイド](../../01_for-users/03_configuration/README.md) - 設定の詳細
- [トラブルシューティング](../../01_for-users/06_troubleshooting/README.md) - 問題解決方法

---

## 🆘 サポート

移行に関する問題が発生した場合：

1. [トラブルシューティングガイド](../../01_for-users/06_troubleshooting/02_common-issues.md)を確認
2. [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)で既知の問題を検索
3. 新しいIssueを作成して報告

最終更新: 2025-10-25
