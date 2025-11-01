[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [セキュリティガイド](README.md) > 03 File Access Control

---

# ファイルアクセス制御

**対象**: Amazon Q Developer CLI

---

## 📋 概要

このガイドは、Amazon Q Developer CLIの`fs_read`ツールによるファイルアクセスを制御する方法を説明します。

---

## 🎯 fs_readツールとは

### 機能

`fs_read`ツールは、Amazon Q CLIがファイルシステムにアクセスするための機能です。

**主な用途**:
- ソースコードの読み取り
- 設定ファイルの確認
- ドキュメントの参照
- ログファイルの分析

### デフォルト動作

**重要**: `fs_read`ツールは**デフォルトで信頼済み**（trusted）です。

```bash
# デフォルト動作
q chat
Amazon Q> ファイルを読んで
# → 確認なしで即座に実行される
```

**理由**:
- ファイル読み取りは一般的に安全な操作
- 頻繁に使用される機能
- ユーザー体験の向上

---

## ⚠️ セキュリティリスク

### 潜在的なリスク

| リスク | 説明 | 影響 |
|--------|------|------|
| **機密ファイルの読み取り** | `.env`、秘密鍵、パスワードファイル | 情報漏洩 |
| **設定ファイルの露出** | データベース接続情報、API キー | セキュリティ侵害 |
| **プライバシー侵害** | 個人情報、ログファイル | コンプライアンス違反 |
| **意図しない共有** | チャット履歴に機密情報が残る | データ漏洩 |

### 具体例

**シナリオ1: 環境変数ファイルの読み取り**
```bash
Amazon Q> .envファイルの内容を確認して
# → DATABASE_PASSWORD=secret123 が読み取られる
```

**シナリオ2: SSH秘密鍵の露出**
```bash
Amazon Q> ~/.ssh/id_rsaを読んで
# → 秘密鍵が読み取られる
```

**シナリオ3: AWS認証情報の漏洩**
```bash
Amazon Q> ~/.aws/credentialsを確認して
# → AWS認証情報が読み取られる
```

---

## 🔒 推奨設定

### セッションごとの制限

チャットセッション開始時に毎回制限する方法：

```bash
q chat
Amazon Q> /tools untrust fs_read
```

**効果**:
- ファイル読み取り前に確認プロンプトが表示される
- セッション終了まで有効

### 永続的な制限（推奨）

シェル設定ファイルにエイリアスを追加：

**bash**:
```bash
echo 'alias q="q --untrust-fs-read"' >> ~/.bashrc
source ~/.bashrc
```

**zsh**:
```bash
echo 'alias q="q --untrust-fs-read"' >> ~/.zshrc
source ~/.zshrc
```

**効果**:
- すべてのセッションで自動的に制限される
- 最も安全な方法

### Agent設定での制限

プロジェクトごとに制限する方法：

**`.q/agent.json`**:
```json
{
  "name": "secure-project",
  "untrustedTools": ["fs_read"]
}
```

**効果**:
- プロジェクトディレクトリ内で自動適用
- チーム全体で共有可能

---

## 🎨 環境別の推奨設定

### 開発環境

**基本的な保護**:
```bash
q chat --untrust-fs-read
```

**理由**:
- 開発中も機密ファイルは保護
- 柔軟性を維持

### 本番環境

**厳格な制限**:
```bash
# 永続的な制限
alias q="q --untrust-fs-read"

# Agent設定
{
  "untrustedTools": ["fs_read", "fs_write", "execute_bash"]
}
```

**理由**:
- 本番データの保護
- 意図しない変更の防止

### 機密環境

**すべて制限**:
```bash
# すべてのツールを制限
alias q="q --untrust-all-tools"
```

**理由**:
- 最高レベルのセキュリティ
- コンプライアンス要件

---

## 🔍 確認プロンプトの動作

### 制限時の動作

`fs_read`を制限すると、ファイル読み取り前に確認プロンプトが表示されます：

```bash
Amazon Q> README.mdを読んで

⚠️  File Access Request
Amazon Q wants to read: /path/to/README.md

Allow this action? [y/N]:
```

**選択肢**:
- `y`: 許可（今回のみ）
- `N`: 拒否（デフォルト）
- `a`: すべて許可（セッション中）

---

## 🛠️ トラブルシューティング

### ファイルが読み込めない

**症状**:
```
Error: Permission denied to read file
```

**原因**:
- `fs_read`が制限されている
- ファイルパーミッションの問題

**対処**:
```bash
# 一時的に許可
Amazon Q> /tools trust fs_read

# または確認プロンプトで許可
```

### 確認プロンプトが表示されない

**症状**:
- ファイルが確認なしで読み込まれる

**原因**:
- `fs_read`が信頼済み（デフォルト）

**対処**:
```bash
# 制限を有効化
Amazon Q> /tools untrust fs_read
```

### 毎回確認が面倒

**症状**:
- 頻繁に確認プロンプトが表示される

**対処**:
```bash
# セッション中すべて許可
# 確認プロンプトで 'a' を選択

# または一時的に信頼
Amazon Q> /tools trust fs_read
```

---

## 💡 ベストプラクティス

### 1. 機密ファイルの保護

**`.gitignore`に追加**:
```
.env
.env.*
*.key
*.pem
credentials
secrets.json
```

**ファイルパーミッション**:
```bash
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.aws/credentials
```

### 2. プロジェクトごとの設定

**Agent設定を活用**:
```json
{
  "name": "production-app",
  "untrustedTools": ["fs_read"],
  "description": "本番環境用の厳格な設定"
}
```

### 3. チーム共有

**設定をリポジトリに含める**:
```bash
git add .q/agent.json
git commit -m "Add secure agent configuration"
```

### 4. 定期的な確認

**設定の確認**:
```bash
Amazon Q> /tools list
# → 信頼済みツールの一覧を確認
```

---

## 🔗 関連ドキュメント

### セキュリティガイド
- [セキュリティ概要](01_security-overview.md)
- [AWS API制御](04_aws-api-control.md)
- [trust-all安全使用ガイド](06_trust-all-safety.md)

### 設定ガイド
- [Agent設定](../03_configuration/03_agent-configuration.md)
- [環境変数](../03_configuration/06_environment-variables.md)

### エンタープライズ展開
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md)
- [エンタープライズ導入ガイド](../05_deployment/01_enterprise-deployment.md)

### AWS公式ドキュメント
- [Security considerations and best practices](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-chat-security.html)

---

## 📞 サポート

セキュリティ上の懸念や質問がある場合：

1. **AWS公式**: [AWS Security](https://aws.amazon.com/security/)
2. **GitHub**: [amazon-q-developer-cli/issues](https://github.com/aws/amazon-q-developer-cli/issues)
3. **ドキュメント**: [トラブルシューティング](../06_troubleshooting/02_common-issues.md)

---

## 📖 ナビゲーション

← **前へ**: [データプライバシー](02_data-privacy.md) | **次へ**: [AWS API制御](04_aws-api-control.md) →



---

最終更新: 2025-10-26
