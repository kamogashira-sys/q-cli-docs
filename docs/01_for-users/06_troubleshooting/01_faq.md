# FAQ - よくある質問

**最終更新**: 2025-10-12

---

## 🎓 初心者向け

### Q CLIとAWS CLIの違いは何ですか？

**AWS CLI**:
- AWSサービスを操作するコマンドラインツール
- コマンドと引数を正確に指定する必要がある
- 例: `aws s3 ls`, `aws ec2 describe-instances`

**Q CLI**:
- AIが自然言語を理解し、コード生成やファイル操作を支援
- 自然言語で質問できる
- 例: チャットセッション内で `> S3バケット一覧を教えて`

**使い分け**:
- AWS CLI: スクリプトや自動化に最適
- Q CLI: 対話的な開発作業、学習、探索に最適

### 最初に何をすべきですか？

**推奨手順**:
1. [インストール](../01_getting-started/01_installation.md)（10分）
2. [クイックスタート](../01_getting-started/02_quick-start.md)（5分）
3. [最初の一歩](../01_getting-started/03_first-steps.md)（15分）

**最初の質問例**:

対話的に使用（推奨）:
```bash
q chat
```
```
> Hello, Q! What can you do?
> Pythonでファイルを読み込む方法を教えて
> このディレクトリの構造を説明して
```

一時的な質問:
```bash
q chat "Hello, Q! What can you do?"
```

### 失敗しても大丈夫ですか？

**はい、安心してください！**

**設定のリセット方法**:
```bash
# 設定ファイルを削除
rm ~/.aws/amazonq/config.toml

# Agent設定を削除
rm -rf ~/.aws/amazonq/cli-agents/

# Q CLIを再起動
q quit
q
```

**アンインストール方法**:
```bash
# macOS (Homebrew)
brew uninstall amazon-q

# Linux
sudo rm /usr/local/bin/q
rm -rf ~/.aws/amazonq
```

**データの保護**:
- Q CLIはローカルで動作します
- 設定ファイルは`~/.aws/amazonq/`に保存されます
- いつでも削除・再インストールできます

### おすすめの学習順序は？

**初心者向け（1-2時間）**:
1. [インストール](../01_getting-started/01_installation.md)
2. [クイックスタート](../01_getting-started/02_quick-start.md)
3. [最初の一歩](../01_getting-started/03_first-steps.md)
4. [チャット機能](../02_features/01_chat.md)

**中級者向け（3-5時間）**:
1. [Agent設定](../03_configuration/04_agent-configuration.md)
2. [MCP設定](../03_configuration/06_mcp-configuration.md)
3. [設定例集](../03_configuration/07_examples.md)
4. [ベストプラクティス](../04_best-practices/01_configuration.md)

**上級者向け（5時間以上）**:
1. [パフォーマンス最適化](../04_best-practices/03_performance.md)
2. [セキュリティ](../04_best-practices/02_security.md)
3. [実験的機能](../02_features/07_experimental.md)
4. [エンタープライズ展開](../05_deployment/01_enterprise-deployment.md)

---

## 📋 一般的な質問

### Amazon Q CLIとは何ですか？
Amazon Q CLIは、AIを活用した開発者向けコマンドラインツールです。

### 無料で使えますか？
AWS Builder IDで無料で使用できます。

### どのOSで使えますか？
macOSとLinuxで使用できます。Windows版は開発中です。

---

## ⚙️ インストール・設定

### インストールできません
**よくある原因**:
- アーキテクチャの不一致（Intel vs Apple Silicon）
- 権限不足
- 依存関係の欠如

**基本的な対処法**:
```bash
# アーキテクチャ確認
uname -m

# 権限確認
ls -la /usr/local/bin/q
```

詳細は[インストールガイド](../01_getting-started/01_installation.md#トラブルシューティング)を参照。

### Q CLIをアンインストールするには？
```bash
# macOS (Homebrew)
brew uninstall amazon-q

# Linux
sudo rm /usr/local/bin/q
rm -rf ~/.aws/amazonq
```

### 複数バージョンの共存は可能ですか？
いいえ、システムに1つのバージョンのみインストールできます。バージョンを切り替える場合は、アンインストール後に再インストールしてください。

### オフライン環境でインストールできますか？
オフライン環境では、事前にインストーラーをダウンロードし、依存関係を含めてインストールする必要があります。詳細は[インストールガイド](../01_getting-started/01_installation.md)を参照してください。

### プロキシ環境での設定方法は？
環境変数でプロキシを設定します：
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1
```

### インストール後の初期設定は？
```bash
# 認証
q login

# 設定確認
q settings list

# Agent確認
q agent list
```

### 設定が反映されません
**設定の優先順位**（高い順）:
1. コマンドライン引数
2. 環境変数
3. Agent設定（ローカル）
4. Agent設定（グローバル）
5. グローバル設定

**確認方法**:
```bash
# 現在の設定を確認
q settings list

# 環境変数を確認
env | grep Q_
```

詳細は[優先順位ルール](../03_configuration/02_priority-rules.md)を参照。

### Agentが見つかりません
**よくある原因**:
- Agent名のタイプミス
- Agent設定ファイルが存在しない
- ファイルパスが間違っている

**確認方法**:
```bash
# Agent一覧を確認
q agent list

# Agent設定ファイルを確認
ls -la ~/.aws/amazonq/cli-agents/
ls -la .q/agents/
```

詳細は[Agent機能](../02_features/02_agents.md)を参照。

---

## 🤖 Agent・MCP

### Agentとは何ですか？
Agentは、Q CLIの動作をカスタマイズする設定ファイルです。

**主な機能**:
- ツール権限の制御
- MCPサーバーの設定
- プロンプトのカスタマイズ
- プロジェクト固有の設定

詳細は[Agent機能](../02_features/02_agents.md)を参照。

### Agentの切り替え方法は？
```bash
# Agent一覧表示
q agent list

# Agent切り替え
q agent use <agent-name>

# 現在のAgent確認
q agent current
```

### MCPサーバーの追加方法は？
Agent設定ファイルにMCPサーバーを追加します。

**設定ファイルの場所**:
- グローバル: `~/.aws/amazonq/cli-agents/<agent-name>.json`
- ローカル: `./.q/agents/<agent-name>.json`

**設定例**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server.js"]
    }
  }
}
```

詳細は[MCP設定](../03_configuration/06_mcp-configuration.md)を参照。

### カスタムAgentの作成方法は？
コマンドでAgentを作成し、設定ファイルを編集します。

```bash
# 新規Agent作成
q agent create my-custom-agent

# 設定ファイル編集（グローバル）
vi ~/.aws/amazonq/cli-agents/my-custom-agent.json

# または、ローカルAgent作成
mkdir -p .q/agents
vi .q/agents/my-custom-agent.json
```

詳細は[Agent設定](../03_configuration/04_agent-configuration.md)を参照。

### MCPサーバーのデバッグ方法は？
ログレベルを上げてMCPサーバーの動作を確認します。

```bash
# ログレベルを上げる
export Q_LOG_LEVEL=debug

# Q CLIを起動
q

# MCPサーバーのログを確認（別ターミナル）
tail -f /run/user/$(id -u)/qlog/mcp-*.log
# または
tail -f /tmp/qlog/mcp-*.log
```

詳細は[MCP設定](../03_configuration/06_mcp-configuration.md#トラブルシューティング)を参照。

### Agent設定のバックアップ方法は？
Agent設定ファイルをバックアップします。

```bash
# グローバルAgent設定をバックアップ
cp -r ~/.aws/amazonq/cli-agents ~/backup/cli-agents-$(date +%Y%m%d)

# 復元
cp -r ~/backup/cli-agents-20251011 ~/.aws/amazonq/cli-agents

# ローカルAgent設定のバックアップ
cp -r .q/agents ~/backup/local-agents-$(date +%Y%m%d)
```

### MCPとは何ですか？
MCP（Model Context Protocol）は、外部ツールと連携するためのプロトコルです。

**主な用途**:
- AWS CLIとの連携
- データベースアクセス
- カスタムツールの統合
- エンタープライズシステム連携

**接続方式**:
- stdio: ローカルプロセス
- HTTP: リモートサーバー

詳細は[MCP設定](../03_configuration/06_mcp-configuration.md)を参照。

### Knowledge機能とは？
プロジェクトのドキュメントやコードを検索できる機能です。

**主な機能**:
- ドキュメント全文検索
- コード検索
- BM25/Vector検索
- コンテキスト自動追加

**有効化方法**:
```bash
# Knowledge機能を有効化
q settings set knowledge.enabled true

# インデックス作成
# Knowledge機能は設定で有効化: q settings chat.enableKnowledge true
```

詳細は[Knowledge機能](../04_best-practices/03_performance.md#-knowledge-base最適化)を参照。

---

## 🐛 トラブルシューティング・パフォーマンス

### エラーが発生します
**基本的な対処手順**:
1. エラーメッセージを確認
2. ログファイルを確認
3. 設定を確認
4. Q CLIを再起動

**よくあるエラー**:
- 認証エラー → `q logout && q login`
- 設定エラー → 設定ファイルの構文確認
- MCPエラー → MCPサーバーの起動確認

詳細は[よくある問題](02_common-issues.md)を参照。

### Q CLIが遅い場合の対処法は？
1. Knowledge機能のインデックスを最適化
2. MCPサーバーの数を減らす
3. キャッシュをクリア
詳細は[パフォーマンス最適化](../04_best-practices/03_performance.md)を参照。

### メモリ使用量が多い場合は？
```bash
# プロセス確認
ps aux | grep q

# Knowledge機能を無効化
q settings set knowledge.enabled false
```

### ログファイルの場所は？
Q CLIのログは実行時ディレクトリに保存されます。

**ログディレクトリ**:
- Linux（XDG準拠）: `/run/user/$(id -u)/qlog/`
- Linux（フォールバック）: `/tmp/qlog/`
- macOS: `/tmp/qlog/`

**ログ確認方法**:
```bash
# 最新のログを確認
tail -f /run/user/$(id -u)/qlog/q-cli.log

# または（フォールバック）
tail -f /tmp/qlog/q-cli.log
```

詳細は[よくある問題](02_common-issues.md#デバッグ手順)を参照。

### キャッシュのクリア方法は？
```bash
# キャッシュディレクトリを削除
rm -rf ~/.aws/amazonq/cache/

# Q CLIを再起動
q quit
q
```

### 設定のリセット方法は？
```bash
# 設定ファイルを削除
rm ~/.aws/amazonq/config.toml

# Agent設定を削除
rm -rf ~/.aws/amazonq/agents/

# Q CLIを再起動
q quit
q
```

### 動作が遅いです
**よくある原因と対処法**:

1. **Knowledge機能の最適化**:
   - BM25検索を使用（v1.14.0+）
   - チャンクサイズを調整
   - インデックスを再構築

2. **MCPサーバーの最適化**:
   - 不要なMCPサーバーを無効化
   - タイムアウト設定を調整

3. **キャッシュのクリア**:
   ```bash
   rm -rf ~/.aws/amazonq/cache/
   ```

詳細は[パフォーマンス最適化](../04_best-practices/03_performance.md)を参照。

### 認証エラーが出ます
```bash
q logout && q login
```

---

## 🔐 セキュリティ

### 機密情報を安全に扱うには？
**基本的なセキュリティ対策**:

1. **ツール権限の制限**:
   - `execute_bash`を慎重に許可
   - `fs_read`の範囲を制限
   - `autoAllowReadonly`を無効化（v1.16.0+）

2. **機密情報の保護**:
   - 環境変数を使用
   - `.gitignore`に設定ファイルを追加
   - パーミッションを適切に設定

3. **定期的な監査**:
   - Agent設定の確認
   - ログの確認
   - アクセスキーのローテーション

詳細は[セキュリティのベストプラクティス](../04_best-practices/02_security.md)を参照。

### ツール権限を制限するには？
Agent設定でツール権限を細かく制御できます。

**設定例**:
```json
{
  "toolConfig": {
    "execute_bash": {
      "enabled": false
    },
    "fs_read": {
      "enabled": true,
      "allowedPaths": ["/path/to/project"]
    },
    "autoAllowReadonly": false
  }
}
```

**推奨設定**:
- `execute_bash`: 必要な場合のみ有効化
- `fs_read`: 必要なパスのみ許可
- `autoAllowReadonly`: 無効化（v1.16.0+）

詳細は[Agent設定](../03_configuration/04_agent-configuration.md#️-ツール設定)を参照。

---

## 💰 料金・プラン

### Free/Pro/Enterpriseの違いは？

| 項目 | Free | Pro | Enterprise |
|------|------|-----|------------|
| 月額料金 | 無料 | $19/月 | カスタム |
| 基本機能 | ✅ | ✅ | ✅ |
| コード補完 | ✅ | ✅ | ✅ |
| チャット機能 | ✅ | ✅ | ✅ |
| Agent機能 | ✅ | ✅ | ✅ |
| MCP統合 | ✅ | ✅ | ✅ |
| データプライバシー | ⚠️ | ✅ | ✅ |
| 優先サポート | ❌ | ✅ | ✅ |
| SLA保証 | ❌ | ❌ | ✅ |
| 管理機能 | ❌ | ❌ | ✅ |

### データプライバシーの違いは？

**Free プラン**:
- コンテンツ（質問、コード、応答）がサービス改善に使用される可能性があります
- オプトアウト可能（設定で無効化できます）

**Pro/Enterprise プラン**:
- コンテンツがサービス改善やモデル学習に**使用されません**
- 機密情報を扱う組織に最適
- データは暗号化され、安全に保管されます

**詳細**: [AWS公式ドキュメント](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/service-improvement.html)

### どのプランを選ぶべきですか？

**Free プラン（推奨: 個人開発者、学習目的）**:
- 個人プロジェクト
- 学習・実験
- オープンソース開発

**Pro プラン（推奨: プロフェッショナル開発者）**:
- 商用プロジェクト
- 機密情報を扱う開発
- 優先サポートが必要

**Enterprise プラン（推奨: 組織・チーム）**:
- 大規模チーム（10名以上）
- エンタープライズセキュリティ要件
- SLA保証が必要
- 統合認証（IAM Identity Center）

### 使用量の確認方法は？

```bash
# 現在のプランを確認
q login --status

# 設定を確認
q settings all
```

**AWSコンソールでの確認**:
1. [AWS Console](https://console.aws.amazon.com/)にログイン
2. Amazon Q Developer → Settings
3. Usage & Billing を確認

---

**最終更新**: 2025-10-12
