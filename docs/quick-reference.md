[ホーム](README.md) > Quick Reference

---

# クイックリファレンス


このページでは、Amazon Q CLIでよく使うコマンドと設定を素早く参照できます。

---

## 目次

- [よく使うコマンド](#-よく使うコマンド)
- [よく使う設定](#-よく使う設定)
- [よく見るドキュメント](#-よく見るドキュメント)
- [トラブルシューティング](#-トラブルシューティング)

---

## 🚀 よく使うコマンド

### チャット

```bash
q chat                    # チャット開始
q chat "質問"             # 直接質問
q                         # チャット開始（短縮形）
```

### Agent

```bash
q agent list              # Agent一覧
q agent switch <name>     # Agent切り替え
q agent edit <name>       # Agent編集
q agent create <name>     # Agent作成
```

### 診断・更新

```bash
q doctor                  # 診断実行
q update                  # 更新確認
q --version               # バージョン確認
```

### チャット内コマンド

```bash
/help                     # ヘルプ表示
/agent <name>             # Agent切り替え
/context                  # コンテキスト確認
/tools list               # ツール一覧
/tools trust <tool>       # ツール信頼
/tools untrust <tool>     # ツール制限
/tools reset              # リセット
/quit                     # 終了
```

---

## 🔧 よく使う設定

### ファイルアクセス制限

**永続的な制限（推奨）**:
```bash
# bash
echo 'alias q="q --untrust-fs-read"' >> ~/.bashrc
source ~/.bashrc

# zsh
echo 'alias q="q --untrust-fs-read"' >> ~/.zshrc
source ~/.zshrc
```

**セッションごとの制限**:
```bash
q chat
Amazon Q> /tools untrust fs_read
```

### AWS API制限

**永続的な制限（推奨）**:
```bash
# bash
echo 'alias q="q --untrust-use-aws"' >> ~/.bashrc
source ~/.bashrc

# zsh
echo 'alias q="q --untrust-use-aws"' >> ~/.zshrc
source ~/.zshrc
```

**セッションごとの制限**:
```bash
q chat
Amazon Q> /tools untrust use_aws
```

### Agent設定

**基本設定** (`.q/agent.json`):
```json
{
  "name": "my-agent",
  "description": "プロジェクト用Agent",
  "untrustedTools": ["fs_read", "use_aws"]
}
```

**MCP設定を含む** (`.q/agent.json`):
```json
{
  "name": "my-agent",
  "mcpServers": {
    "aws-cli": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-aws-cli"]
    }
  }
}
```

### テレメトリー無効化

**グローバル設定** (`~/.q/settings.json`):
```json
{
  "telemetry.enabled": false
}
```

---

## 📖 よく見るドキュメント

### 初めての方

- **[インストール](01_for-users/01_getting-started/01_installation.md)** - Q CLIのインストール方法
- **[クイックスタート](01_for-users/01_getting-started/02_quick-start.md)** - 5分で始めるQ CLI
- **[最初の一歩](01_for-users/01_getting-started/03_first-steps.md)** - 基本的な使い方

### トラブルシューティング

- **[よくある問題](01_for-users/06_troubleshooting/02_common-issues.md)** - 15の一般的問題と解決方法
- **[FAQ](01_for-users/06_troubleshooting/01_faq.md)** - よくある質問と回答

### 設定

- **[設定システム概要](01_for-users/03_configuration/01_overview.md)** - 設定システム全体像
- **[Agent設定](01_for-users/03_configuration/03_agent-configuration.md)** - Agent設定の詳細
- **[MCP設定](01_for-users/03_configuration/04_mcp-configuration.md)** - MCPサーバー設定
- **[環境変数](01_for-users/03_configuration/06_environment-variables.md)** - 環境変数一覧

### セキュリティ

- **[セキュリティ概要](01_for-users/09_security/01_security-overview.md)** - セキュリティの基本原則
- **[データプライバシー](01_for-users/09_security/02_data-privacy.md)** - プラン別のデータ使用
- **[ファイルアクセス制御](01_for-users/09_security/03_file-access-control.md)** - fs_readツール制御
- **[AWS API制御](01_for-users/09_security/04_aws-api-control.md)** - use_awsツール制御

### コンテキスト管理【重要】

- **[本質編](01_for-users/08_guides/01_essence.md)** - コンテキストとは何か
- **[ベストプラクティス編](01_for-users/08_guides/04_best-practices.md)** - 設計原則と実装パターン
- **[実践ガイド編](01_for-users/08_guides/05_practical-guide.md)** - プロジェクト別実装例

### リファレンス

- **[コマンドリファレンス](01_for-users/07_reference/02_commands.md)** - 全コマンド一覧
- **[設定項目リファレンス](01_for-users/07_reference/03_settings-reference.md)** - 全35設定項目
- **[用語集](01_for-users/07_reference/01_glossary.md)** - 用語の定義

---

## 🚨 トラブルシューティング

### 接続エラー

```bash
q doctor                  # 診断実行
```

**よくある原因**:
- ネットワーク接続の問題
- プロキシ設定の問題
- 認証情報の期限切れ

### 認証エラー

```bash
q                         # 再ログイン
```

**よくある原因**:
- セッションの期限切れ
- 認証情報の不正

### Agent切り替えできない

```bash
q agent list              # Agent確認
```

**よくある原因**:
- Agent設定ファイルのエラー
- JSONフォーマットの誤り

### ファイルが読み込めない

```bash
# チャット内で確認
Amazon Q> /tools list
```

**よくある原因**:
- fs_readが制限されている
- ファイルパーミッションの問題

### AWS APIが実行できない

```bash
# チャット内で確認
Amazon Q> /tools list
```

**よくある原因**:
- use_awsが制限されている
- IAM権限不足

---

## 🔗 関連ドキュメント

- **[トピック別インデックス](topic-index.md)** - トピックから探す
- **[ドキュメント一覧](README.md)** - 全ドキュメントの一覧
- **[コマンドリファレンス](01_for-users/07_reference/02_commands.md)** - 詳細なコマンド説明
- **[設定項目リファレンス](01_for-users/07_reference/03_settings-reference.md)** - 詳細な設定説明

---

## 💡 Tips

### コマンドのコピー&ペースト

このページのコマンドは、そのままコピー&ペーストして使用できます。

### エイリアスの活用

よく使うコマンドはエイリアスを設定すると便利です：

```bash
# .bashrc または .zshrc に追加
alias qc='q chat'
alias qa='q agent'
alias qd='q doctor'
```

### Agent設定のテンプレート

プロジェクトごとにAgent設定をコピーして使用できます：

```bash
# テンプレートをコピー
cp ~/.q/agents/template.json .q/agent.json

# 編集
vim .q/agent.json
```

---

最終更新: 2025-10-18  
**対象バージョン**: v1.17.0以降

---

最終更新: 2025-10-18
