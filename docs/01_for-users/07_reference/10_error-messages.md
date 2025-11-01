[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 10 エラーメッセージ一覧

# エラーメッセージ一覧

**対象バージョン**: v1.17.0以降  
**対象読者**: すべてのユーザー

---

## 📋 概要

このドキュメントは、Amazon Q Developer CLI (Q CLI) で発生する可能性のあるエラーメッセージの一覧です。各エラーについて、原因と対処方法を記載しています。

---

## 🔍 エラーカテゴリ

- [API関連エラー](#api関連エラー) - 5件
- [認証エラー](#認証エラー) - 5件
- [チャットエラー](#チャットエラー) - 4件
- [Agent設定エラー](#agent設定エラー) - 2件
- [MCPエラー](#mcpエラー) - 3件
- [データベースエラー](#データベースエラー) - 2件
- [リクエストエラー](#リクエストエラー) - 2件

**総エラー数**: 23件

---

## API関連エラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `quota has reached its limit` | 使用量クォータの上限に達した | 1. しばらく時間を置いて再試行<br>2. 使用量を確認し、プランをアップグレード<br>3. リクエスト頻度を減らす | [AWS Service Quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) |
| `monthly query limit reached` | 月間のクエリ制限に達した | 1. 翌月まで待つ<br>2. プランをアップグレード<br>3. 使用量を最適化 | [Q Developer Pricing](https://aws.amazon.com/q/developer/pricing/) |
| `the context window has overflowed` | 会話履歴が長すぎてコンテキストウィンドウに収まらない | 1. `/clear` で会話履歴をクリア<br>2. `/compact` で会話履歴を圧縮<br>3. 新しいセッションを開始<br>4. ファイルサイズを小さくする | [チャット機能](../02_features/01_chat.md) |
| `No default model found in the ListAvailableModels API response` | APIレスポンスにデフォルトモデルが含まれていない | 1. `/model` で利用可能なモデルを確認<br>2. 手動でモデルを選択<br>3. Q CLIを最新バージョンに更新 | [実験的機能](../02_features/07_experimental.md) |
| `The model you've selected is temporarily unavailable. Please use '/model' to select a different model and try again.` | 選択したモデルが一時的に利用できない | 1. `/model` で別のモデルを選択<br>2. しばらく時間を置いて再試行<br>3. デフォルトモデルに戻す | [実験的機能](../02_features/07_experimental.md) |

---

## 認証エラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `No token` | ログインしていない、または認証トークンが存在しない | 1. `q auth login` でログイン<br>2. 認証情報を確認 | [クイックスタート](../01_getting-started/02_quick-start.md) |
| `Timeout waiting for authentication to complete` | 認証プロセスがタイムアウトした | 1. 認証プロセスを再実行<br>2. ブラウザで認証を速やかに完了<br>3. ネットワーク接続を確認<br>4. ファイアウォール設定を確認 | [よくある問題](../06_troubleshooting/02_common-issues.md) |
| `No code received on redirect` | OAuth認証のリダイレクトで認証コードが受信されなかった | 1. 認証プロセスを最初からやり直す<br>2. ブラウザで認証を完了<br>3. ポップアップブロッカーを無効化 | [クイックスタート](../01_getting-started/02_quick-start.md) |
| `OAuth error: {詳細}` | OAuth認証プロセスでエラーが発生 | 1. エラーメッセージの詳細を確認<br>2. 認証プロセスを再実行<br>3. Q CLIを最新バージョンに更新<br>4. AWSサポートに問い合わせ | [よくある問題](../06_troubleshooting/02_common-issues.md) |
| `You are not logged in, please log in with q auth login` | ログインしていない状態でコマンドを実行 | `q auth login` でログイン | [クイックスタート](../01_getting-started/02_quick-start.md) |

---

## チャットエラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `interrupted` | ユーザーがCtrl+Cで処理を中断 | 意図的な中断の場合は対処不要。誤って中断した場合はコマンドを再実行 | - |
| `Tool approval required but --no-interactive was specified. Use --trust-all-tools to automatically approve tools.` | 非対話モードでツール承認が必要になった | 1. `--trust-all-tools` オプションを追加<br>2. 非対話モードを解除<br>3. Agent設定で `trustAllTools: true` を設定 | [Agent設定](../03_configuration/03_agent-configuration.md) |
| `The conversation history is too large to compact` | 会話履歴が大きすぎて圧縮できない | 1. `/clear` で会話履歴をクリア<br>2. 新しいセッションを開始<br>3. 重要な情報を保存してから履歴をクリア | [チャット機能](../02_features/01_chat.md) |
| `Failed to swap to agent: {詳細}` | Agent切り替えに失敗 | 1. `q agent list` でAgent一覧を確認<br>2. Agent設定ファイルの存在を確認<br>3. Agent設定ファイルの構文を確認 | [Agent機能](../02_features/02_agents.md) |

---

## Agent設定エラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `Agent configuration file not found: {パス}` | 指定されたAgent設定ファイルが存在しない | 1. ファイルパスを確認<br>2. `q agent list` で利用可能なAgentを確認<br>3. Agent設定ファイルを作成 | [Agent設定](../03_configuration/03_agent-configuration.md) |
| `Invalid agent configuration: {詳細}` | Agent設定ファイルの構文エラーまたは無効な値 | 1. JSON構文を確認<br>2. 必須フィールドを確認<br>3. [設定スキーマ](../03_configuration/03_agent-configuration.md#設定スキーマ)と照合<br>4. `q agent validate` で検証 | [Agent設定](../03_configuration/03_agent-configuration.md) |

---

## MCPエラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `MCP server connection failed: {サーバー名}` | MCPサーバーに接続できない | 1. MCPサーバーが起動しているか確認<br>2. 接続設定（ホスト、ポート）を確認<br>3. ネットワーク接続を確認<br>4. MCPサーバーのログを確認 | [MCP設定](../03_configuration/04_mcp-configuration.md) |
| `MCP server '{名前}' already exists in agent {Agent名} (path {パス}). Use --force to overwrite.` | 同じ名前のMCPサーバーがすでに登録されている | 1. 別の名前を使用<br>2. `--force` オプションで上書き<br>3. 既存のMCPサーバーを削除してから追加 | [MCP設定](../03_configuration/04_mcp-configuration.md) |
| `No MCP server named '{名前}' found in any agent` | 指定された名前のMCPサーバーが見つからない | 1. `q mcp list` でMCPサーバー一覧を確認<br>2. サーバー名のスペルを確認 | [MCP設定](../03_configuration/04_mcp-configuration.md) |

---

## データベースエラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `Failed to open database: {詳細}` | データベースファイルを開けない、破損、または権限がない | 1. データベースファイルの権限を確認（`~/.local/share/amazon-q/q.db`）<br>2. 破損している場合は削除して再作成（注意: データ損失）<br>3. ディスク容量を確認 | [トラブルシューティング](../06_troubleshooting/02_common-issues.md) |
| `Database migration failed: {詳細}` | データベースのマイグレーションに失敗 | 1. Q CLIを最新バージョンに更新<br>2. データベースファイルをバックアップして削除・再作成<br>3. GitHub Issuesで報告 | [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues) |

---

## リクエストエラー

| エラーメッセージ | 原因 | 対処方法 | 関連情報 |
|----------------|------|---------|---------|
| `Request timeout` | リクエストがタイムアウト | 1. ネットワーク接続を確認<br>2. しばらく時間を置いて再試行<br>3. タイムアウト設定を調整（環境変数） | [環境変数](../03_configuration/06_environment-variables.md) |
| `Invalid request: {詳細}` | リクエストの形式が無効、必須パラメータ不足、または無効な値 | 1. コマンドの構文を確認<br>2. 必須パラメータを確認<br>3. パラメータの値を確認 | [コマンドリファレンス](02_commands.md) |

---

## 🔧 一般的なトラブルシューティング

### エラーが解決しない場合

1. **Q CLIを最新バージョンに更新**
   ```bash
   # Homebrewの場合
   brew upgrade q
   ```

2. **設定をリセット**
   ```bash
   # 設定ファイルをバックアップ
   cp -r ~/.aws/amazonq ~/.aws/amazonq.backup
   
   # 設定をクリア
   rm -rf ~/.aws/amazonq
   rm -rf ~/.local/share/amazon-q
   
   # 再ログイン
   q auth login
   ```

3. **ログを確認**
   ```bash
   # ログファイルの場所
   ~/.local/share/amazon-q/logs/
   
   # 最新のログを確認
   tail -f ~/.local/share/amazon-q/logs/q.log
   ```

4. **GitHub Issuesで報告**
   - [既知の問題を検索](https://github.com/aws/amazon-q-developer-cli/issues)
   - 新しいIssueを作成

---

## 📚 関連ドキュメント

- [トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)
- [設定ガイド](../03_configuration/README.md)
- [コマンドリファレンス](02_commands.md)
- [エラー管理概要](../../02_for-developers/01_contributing/03_error-management-overview.md) - 開発者向け
- [エラーメッセージ追加ガイド](../../02_for-developers/01_contributing/04_adding-error-messages.md) - 開発者向け

---

## 🤝 サポート

問題が解決しない場合：

- [AWS サポート](https://aws.amazon.com/support/)
- [AWS re:Post](https://repost.aws/)
- [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)

---

[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 10 エラーメッセージ一覧

---

最終更新: 2025-10-26
