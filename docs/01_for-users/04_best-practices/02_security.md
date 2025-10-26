[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [ベストプラクティス](README.md) > 02 Security

---

# セキュリティのベストプラクティス

**対象バージョン**: v1.17.0以降

---

## 🔐 概要

Amazon Q CLIを安全に使用するためのベストプラクティスを紹介します。このガイドでは、ツール権限管理、機密情報の保護、ファイルアクセス制御など、セキュリティを確保するための実践的な方法を説明します。

### このガイドで学べること

- ツール権限の適切な管理方法
- 機密情報を安全に扱う方法
- ファイルアクセスの制限方法
- Agent設定の検証とデバッグ
- セキュリティインシデントへの対応

---

## 🛡️ ツール権限管理

### 権限モデルの理解

Amazon Q CLIには2種類のツール権限設定があります：

#### 1. `tools` - 利用可能なツール
Agentが使用できるツールを定義します。

```json
{
  "tools": ["fs_read", "fs_write", "execute_bash"]
}
```

#### 2. `allowedTools` - 自動承認ツール
ユーザーの承認なしで自動実行されるツールを定義します。

```json
{
  "allowedTools": ["fs_read"]
}
```

**重要な違い**:
- `tools`: 「使用可能」なツール（実行時に承認を求める）
- `allowedTools`: 「自動承認」されるツール（承認なしで実行）

### 自動承認のリスク

**v1.16.0以降の重要な変更**:
- `autoAllowReadonly`のデフォルトが`false`に変更されました
- セキュリティ向上のため、明示的な設定が必要になりました

**リスクの高いツール**:
```json
{
  "allowedTools": [
    "execute_bash",  // ❌ 危険: 任意のコマンド実行
    "fs_write",      // ⚠️ 注意: ファイル書き込み
    "use_aws"        // ⚠️ 注意: AWS操作
  ]
}
```

**安全なツール**:
```json
{
  "allowedTools": [
    "fs_read",       // ✅ 比較的安全: 読み取りのみ
    "list_directory" // ✅ 比較的安全: ディレクトリ一覧
  ]
}
```

### ワイルドカードパターンの注意点

ワイルドカードは便利ですが、慎重に使用してください。

**危険な例**:
```json
{
  "allowedTools": [
    "*"           // ❌ 非常に危険: すべてのツールを自動承認
  ]
}
```

**比較的安全な例**:
```json
{
  "allowedTools": [
    "*_read"      // ✅ 読み取り系のみ
  ]
}
```

**注意が必要な例**:
```json
{
  "allowedTools": [
    "fs_*"        // ⚠️ 注意: fs_writeも含まれる
  ]
}
```

### 権限設定のベストプラクティス

#### 開発環境用Agent
```json
{
  "name": "dev-agent",
  "description": "開発環境用Agent",
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "allowedTools": ["fs_read"]
}
```

#### 本番環境用Agent
```json
{
  "name": "prod-agent",
  "description": "本番環境用Agent（読み取り専用）",
  "tools": ["fs_read", "use_aws"],
  "allowedTools": []
}
```

#### レビュー用Agent
```json
{
  "name": "review-agent",
  "description": "コードレビュー用Agent",
  "tools": ["fs_read"],
  "allowedTools": ["fs_read"]
}
```

### execute_bashの危険性

**v1.16.0での強化**:
- 危険なパターンに`$`が追加されました
- シェル変数展開による意図しない実行を防止

**危険なパターン**:
```bash
# これらは実行前に警告が表示されます
rm -rf /
sudo command
$VARIABLE
```

**安全な使用方法**:
```json
{
  "tools": ["execute_bash"],
  "allowedTools": [],  // 自動承認しない
  "toolsSettings": {
    "execute_bash": {
      "allowedCommands": ["ls", "cat", "grep"]  // 許可するコマンドを制限
    }
  }
}
```

---

## 🔑 機密情報の保護

### 環境変数の活用

#### 環境変数展開の仕組み

Amazon Q CLIは`${env:VAR_NAME}`構文で環境変数を展開します。

**正しい構文**:
```json
{
  "headers": {
    "Authorization": "Bearer ${env:API_TOKEN}"
  }
}
```

**間違った構文**:
```json
{
  "headers": {
    "Authorization": "Bearer $API_TOKEN"        // ❌ 展開されない
    "Authorization": "Bearer ${API_TOKEN}"      // ❌ 展開されない
    "Authorization": "Bearer {env:API_TOKEN}"   // ❌ 展開されない
  }
}
```

#### .envファイルの管理

**ベストプラクティス**:
```bash
# 1. .envファイルを作成
cat > .env << 'EOF'
API_TOKEN=your-secret-token
GITHUB_TOKEN=your-github-token
AWS_PROFILE=my-profile
EOF

# 2. .gitignoreに追加
echo ".env" >> .gitignore

# 3. パーミッションを制限
chmod 600 .env

# 4. direnvで自動読み込み（オプション）
echo 'dotenv' > .envrc
direnv allow
```

### Agent設定での機密情報

#### APIキーの管理

**❌ 悪い例**: ハードコード
```json
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer sk-1234567890abcdef"
      }
    }
  }
}
```

**✅ 良い例**: 環境変数
```json
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer ${env:API_TOKEN}"
      }
    }
  }
}
```

#### 認証トークンの扱い

**環境変数の設定**:
```bash
# シェルで設定
export API_TOKEN="your-token-here"

# または.envファイルで管理
echo "API_TOKEN=your-token-here" >> .env
```

**Agent設定での使用**:
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com",
      "headers": {
        "Authorization": "token ${env:GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
      }
    }
  }
}
```

### MCP設定でのセキュリティ

#### OAuth2.0の設定

**基本設定**:
```json
{
  "mcpServers": {
    "oauth-service": {
      "type": "http",
      "url": "https://api.service.com",
      "oauthScopes": [
        "openid",
        "email",
        "profile",
        "offline_access"
      ]
    }
  }
}
```

**カスタムスコープの追加**:
```json
{
  "oauthScopes": [
    "openid",
    "email",
    "profile",
    "offline_access",
    "read:user",      // カスタムスコープ
    "repo"            // カスタムスコープ
  ]
}
```

#### リモートMCPサーバーの認証

**v1.16.0以降の機能**:
```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:API_TOKEN}",
        "X-API-Key": "${env:API_KEY}"
      },
      "timeout": 120000
    }
  }
}
```

---

## 📁 ファイルアクセス制御

### fs_read/fs_writeの制限

#### allowedPathsの設定

**基本的な制限**:
```json
{
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["${env:HOME}/projects"]
    }
  }
}
```

**複数パスの指定**:
```json
{
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": [
        "${env:HOME}/projects",
        "${env:HOME}/documents",
        "/tmp"
      ]
    }
  }
}
```

#### deniedPathsの設定

**機密ディレクトリの保護**:
```json
{
  "toolsSettings": {
    "fs_read": {
      "deniedPaths": [
        "${env:HOME}/.ssh",
        "${env:HOME}/.aws",
        "${env:HOME}/.gnupg",
        "${env:HOME}/.config/secrets"
      ]
    }
  }
}
```

### パスパターンの優先順位

**v1.16.0での重要な変更**:
- `fs_read`の信頼権限が現在の作業ディレクトリのみに制限されました

**優先順位**:
1. `deniedPaths`（最優先）
2. `allowedPaths`
3. デフォルト（現在の作業ディレクトリ）

**例**:
```json
{
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["${env:HOME}/projects"],
      "deniedPaths": ["${env:HOME}/projects/secrets"]
    }
  }
}
```

この設定では：
- `~/projects/`は読み取り可能
- `~/projects/secrets/`は読み取り不可（deniedPathsが優先）

### 実践例

#### プロジェクト限定アクセス
```json
{
  "name": "project-agent",
  "tools": ["fs_read", "fs_write"],
  "allowedTools": ["fs_read"],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["${env:PWD}"]
    },
    "fs_write": {
      "allowedPaths": ["${env:PWD}/output"]
    }
  }
}
```

#### 読み取り専用アクセス
```json
{
  "name": "readonly-agent",
  "tools": ["fs_read"],
  "allowedTools": ["fs_read"],
  "toolsSettings": {
    "fs_read": {
      "allowedPaths": ["${env:HOME}/documents"],
      "deniedPaths": ["${env:HOME}/documents/private"]
    }
  }
}
```

#### 一時ディレクトリの活用
```json
{
  "name": "temp-agent",
  "tools": ["fs_read", "fs_write"],
  "allowedTools": [],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["/tmp/q-cli-workspace"]
    }
  }
}
```

---

## 🔒 Agent設定の検証

### JSON構文チェック

**jqコマンドを使用**:
```bash
# 構文チェック
jq . ~/.aws/amazonq/cli-agents/my-agent.json

# エラーがなければ整形されたJSONが表示される
```

**エラー例**:
```bash
$ jq . my-agent.json
parse error: Expected separator between values at line 5, column 3
```

### スキーマバリデーション

**公式スキーマ**:
```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json"
}
```

**ajvツールを使用**:
```bash
# ajvをインストール
npm install -g ajv-cli

# スキーマ検証
ajv validate -s agent-v1.json -d my-agent.json
```

### Agent検証コマンド

```bash
# Agent設定の検証
q agent validate my-agent

# Agent一覧の確認
q agent list

# Agent詳細の確認
q agent list my-agent
```

### デバッグログの活用

**デバッグモードの有効化**:
```bash
# デバッグログを有効化
Q_LOG_LEVEL=debug q chat --agent my-agent

# 標準出力にもログを表示
Q_LOG_LEVEL=debug Q_LOG_STDOUT=1 q chat --agent my-agent
```

**ログファイルの場所**:
```bash
# Linux
/run/user/$(id -u)/qlog/qchat.log

# macOS
$TMPDIR/qlog/qchat.log

# Windows
%TEMP%\amazon-q\logs\qchat.log
```

**ログの確認**:
```bash
# リアルタイムでログを監視
tail -f /run/user/$(id -u)/qlog/qchat.log

# エラーのみ抽出
grep ERROR /run/user/$(id -u)/qlog/qchat.log
```

### 段階的な検証アプローチ

**Step 1: 最小構成**
```json
{
  "name": "test-agent",
  "description": "Test agent"
}
```

**Step 2: ツールを追加**
```json
{
  "name": "test-agent",
  "description": "Test agent",
  "tools": ["fs_read"]
}
```

**Step 3: MCPサーバーを追加**
```json
{
  "name": "test-agent",
  "description": "Test agent",
  "tools": ["fs_read"],
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
```

各ステップで動作確認を行い、問題を早期に発見しましょう。

---

## 🚨 セキュリティインシデント対応

### ログの確認

**セキュリティ関連ログの場所**:
```bash
# チャットログ
/run/user/$(id -u)/qlog/qchat.log

# MCPサーバーログ
/run/user/$(id -u)/qlog/mcp-*.log
```

**不審なアクティビティの検出**:
```bash
# 失敗した認証試行
grep "401\|403\|Unauthorized" /run/user/$(id -u)/qlog/*.log

# execute_bashの実行履歴
grep "execute_bash" /run/user/$(id -u)/qlog/qchat.log

# ファイル書き込み操作
grep "fs_write" /run/user/$(id -u)/qlog/qchat.log
```

### 緊急時の対応

#### 1. Agent設定の無効化
```bash
# Agentを一時的に無効化
mv ~/.aws/amazonq/cli-agents/my-agent.json \
   ~/.aws/amazonq/cli-agents/my-agent.json.disabled

# Q CLIを再起動
q restart
```

#### 2. アクセスキーのローテーション
```bash
# AWS認証情報を確認
aws sts get-caller-identity

# 新しいアクセスキーを作成
aws iam create-access-key --user-name my-user

# 古いアクセスキーを無効化
aws iam update-access-key --access-key-id OLD_KEY_ID --status Inactive --user-name my-user

# 古いアクセスキーを削除
aws iam delete-access-key --access-key-id OLD_KEY_ID --user-name my-user
```

#### 3. 設定のリセット
```bash
# 設定ファイルをバックアップ
cp ~/.local/share/amazon-q/settings.json \
   ~/.local/share/amazon-q/settings.json.backup

# 設定をリセット
rm ~/.local/share/amazon-q/settings.json

# Q CLIを再起動
q restart
```

---

## ✅ セキュリティチェックリスト

### 定期的な権限レビュー

- [ ] `allowedTools`に危険なツールが含まれていないか
- [ ] ワイルドカードパターンが適切に制限されているか
- [ ] `execute_bash`の使用が必要最小限か
- [ ] ファイルアクセス権限が適切に設定されているか

### 機密情報のスキャン

- [ ] Agent設定にハードコードされた認証情報がないか
- [ ] 環境変数が適切に使用されているか
- [ ] .envファイルが.gitignoreに追加されているか
- [ ] ログファイルに機密情報が含まれていないか

### 設定ファイルの監査

- [ ] JSON構文が正しいか（jqでチェック）
- [ ] スキーマに準拠しているか
- [ ] MCPサーバーのタイムアウトが適切か
- [ ] OAuth設定が正しいか

### テレメトリとプライバシー

#### データプライバシーの理解

**プラン別のデータ使用ポリシー**:

| プラン | データ使用 | 詳細 |
|--------|-----------|------|
| **Free** | サービス改善に使用される可能性あり | 質問、応答、コード生成がサービス改善に使用される場合がある |
| **Pro** | サービス改善に使用されない | コンテンツはモデル学習やサービス改善に使用されない |
| **Enterprise** | サービス改善に使用されない | コンテンツはモデル学習やサービス改善に使用されない |

> **💡 重要**: Pro/Enterpriseプランでは、あなたのコンテンツ（質問、コード、応答）はAWSのサービス改善やモデル学習に使用されません。
>
> 詳細: [AWS公式ドキュメント - Service Improvement](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)

#### Freeプランでのオプトアウト

Freeプランでコンテンツ共有をオプトアウトする方法:

**方法1: AWS Organizations AI services opt-out policy**
```bash
# 組織レベルでオプトアウト
aws organizations put-policy \
  --content file://ai-optout-policy.json \
  --type AISERVICES_OPT_OUT_POLICY
```

**方法2: IDE設定**
- VS Code: 設定でCodeWhispererコンテンツ共有を無効化
- JetBrains: 設定でデータ共有を無効化

#### テレメトリ設定のチェックリスト

- [ ] 使用しているプラン（Free/Pro/Enterprise）を確認
- [ ] Pro/Enterpriseプランの場合、データプライバシー保護が有効であることを確認
- [ ] Freeプランの場合、必要に応じてオプトアウトを設定
- [ ] テレメトリ設定を確認（`~/.local/share/amazon-q/settings.json`）
- [ ] CodeWhispererコンテンツ共有設定を確認
- [ ] 必要に応じてテレメトリを無効化

---

## 📚 関連ドキュメント

- **[Agent設定ガイド](../03_configuration/03_agent-configuration.md)** - Agent設定の詳細
- **[MCP設定ガイド](../03_configuration/04_mcp-configuration.md)** - MCPサーバーの設定
- **[環境変数ガイド](../03_configuration/06_environment-variables.md)** - 環境変数の使い方
- **[トラブルシューティング](../06_troubleshooting/02_common-issues.md)** - よくある問題と解決方法
- **[設定のベストプラクティス](01_configuration.md)** - 全般的な設定のベストプラクティス
- **[パフォーマンス最適化](03_performance.md)** - パフォーマンス最適化のベストプラクティス

---

作成日: 2025-10-11  

**対象バージョン**: v1.17.0以降
---

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

## 関連ドキュメント

- [セキュリティ概要](../09_security/01_security-overview.md) - セキュリティ全体像
- [データプライバシー](../09_security/02_data-privacy.md) - データの取り扱い
- [テレメトリー設定](../03_configuration/05_telemetry.md) - 使用状況データの管理
- [セキュリティチェックリスト](../05_deployment/03_security-checklist.md) - 設定確認項目

---

最終更新: 2025-10-26
