# Amazon Q CLI 設定トラブルシューティング

**作成日**: 2025-10-08  
**対象バージョン**: v1.17.0以降

## 概要

このドキュメントは、Amazon Q CLIの設定に関する一般的な問題と解決方法をまとめています。

---

## 診断コマンド

### 基本診断

```bash
# Amazon Q CLIの診断を実行
q doctor

# 設定の確認
q settings all

# Agent一覧の確認
q agent list

# Amazon Q CLIの再起動
q restart
```

---

## 設定ファイル関連の問題

### 問題: 設定ファイルが見つからない

**症状**: 設定を変更しても反映されない

**原因**: 設定ファイルを間違った場所に配置している

**解決方法**:
1. 実際の設定ファイル場所を確認:
   ```bash
   ls -la ~/.local/share/amazon-q/settings.json
   ```

2. 間違った場所に配置していないか確認:
   ```bash
   # これらの場所は使用されません
   ls -la ~/.local/share/amazon-q/settings.json
   ls -la ~/.local/share/amazon-q/settings.json
   ```

3. 環境変数の確認:
   ```bash
   echo "XDG_DATA_HOME: ${XDG_DATA_HOME:-未設定}"
   ```

4. 正しい場所に設定ファイルを作成:
   ```bash
   # ディレクトリを作成
   mkdir -p ~/.local/share/amazon-q
   
   # 設定ファイルを作成
   cat > ~/.local/share/amazon-q/settings.json << 'EOF'
   {
     "chat.enableThinking": true,
     "telemetry.enabled": false
   }
   EOF
   ```

### 問題: XDG_CONFIG_HOMEを設定しても反映されない

**症状**: `XDG_CONFIG_HOME`を設定しても設定ファイルが`~/.local/share/amazon-q/`に作成されない

**原因**: Q CLIは`XDG_CONFIG_HOME`ではなく`XDG_DATA_HOME`を使用する設計

**解決方法**:
```bash
# XDG_DATA_HOMEを設定（XDG_CONFIG_HOMEではない）
export XDG_DATA_HOME="$HOME/custom-data"

# 設定ファイルの場所を確認
echo "設定ファイル: $XDG_DATA_HOME/amazon-q/settings.json"

# Q CLIを再起動
q restart
```

---

## Agent関連の問題

### 問題1: Agent が見つからない

**エラーメッセージ**:
```
Error: no agent with name my-agent found. Falling back to user specified default
```

**原因**:
- Agent設定ファイルが存在しない
- Agent名のスペルミス
- Agent設定ファイルの場所が間違っている

**解決方法**:
```bash
# Agent一覧を確認
q agent list

# Agent設定ファイルの場所を確認
ls -la .aws/amazonq/cli-agents/
ls -la ~/.aws/amazonq/cli-agents/

# Agent設定ファイルの内容を確認
cat .amazonq/cli-agents/my-agent.json

# Agent名を修正
q settings chat.defaultAgent correct-agent-name
```

---

### 問題2: Agent名の競合

**警告メッセージ**:
```
WARNING: Agent conflict for my-agent. Using workspace version.
```

**原因**:
- ローカルとグローバルに同じ名前のAgentが存在

**解決方法**:
```bash
# 意図的な場合: 警告を無視（ローカルが優先される）

# 意図的でない場合: どちらかの名前を変更
# ローカルAgentの名前を変更
mv .amazonq/cli-agents/my-agent.json .amazonq/cli-agents/local-my-agent.json

# または、グローバルAgentの名前を変更
mv ~/.aws/amazonq/cli-agents/my-agent.json ~/.aws/amazonq/cli-agents/global-my-agent.json
```

---

### 問題3: Agent設定が無効

**エラーメッセージ**:
```
Error: Invalid agent configuration
```

**原因**:
- JSON構文エラー
- 必須フィールドの欠落
- 無効な設定値

**解決方法**:
```bash
# JSON構文チェック
cat .amazonq/cli-agents/my-agent.json | jq .

# スキーマに対してバリデーション
# schemas/agent-v1.json を参照

# 最小限の有効な設定例
cat > .aws/amazonq/cli-agents/my-agent.json << 'EOF'
{
  "description": "My agent"
}
EOF
```

---

## MCP関連の問題

### 問題4: MCPサーバーが起動しない

**エラーメッセージ**:
```
Error: Failed to start MCP server 'my-server'
```

**原因**:
- コマンドが見つからない
- 権限の問題
- タイムアウト
- 依存関係の欠落

**解決方法**:
```bash
# 1. コマンドのパスを確認
which npx
which node

# 2. 手動で実行してテスト
npx -y @modelcontextprotocol/server-filesystem /path

# 4. 依存関係をインストール
npm install -g @modelcontextprotocol/server-filesystem

# 5. ログを確認
# ログファイルを手動で確認
```

3. タイムアウトを延長（設定ファイルを編集）:
```json
{
  "mcpServers": {
    "my-server": {
      "timeout": 180000
    }
  }
}
```

---

### 問題5: HTTP MCPサーバーの認証エラー

**エラーメッセージ**:
```
Error: HTTP 401 Unauthorized
```

**原因**:
- トークンが無効
- 環境変数が設定されていない
- トークンの有効期限切れ

**解決方法**:
```bash
# 1. 環境変数を確認
echo $API_TOKEN

# 2. 環境変数を設定
export API_TOKEN=your_token_here

# 3. Amazon Q CLIを再起動
q restart

# 4. トークンを更新
# OAuthプロバイダーで新しいトークンを取得

# 5. 設定を確認
cat .amazonq/cli-agents/my-agent.json | jq '.mcpServers'
```

---

### 問題6: 環境変数が展開されない

**エラーメッセージ**:
```
Error: Invalid token: ${env:API_TOKEN}
```

**原因**:
- 環境変数が設定されていない
- 構文エラー
- v1.17.0未満のバージョン（HTTPヘッダーの環境変数サポートなし）

**解決方法**:
```bash
# 1. バージョンを確認
q --version

# 2. 環境変数を設定
export API_TOKEN=your_token_here

# 3. 構文を確認
# 正しい: ${env:API_TOKEN}
# 間違い: $API_TOKEN, ${API_TOKEN}, {env:API_TOKEN}

# 4. Amazon Q CLIを再起動
q restart
```

---

## 設定関連の問題

### 問題7: 設定が反映されない

**症状**:
- 設定を変更しても動作が変わらない

**原因**:
- Amazon Q CLIが再起動されていない
- 設定キーのスペルミス
- 設定値の型が間違っている

**解決方法**:
```bash
# 1. 設定を確認
q settings <key>

# 2. 設定を再設定
q settings <key> <value>

# 3. Amazon Q CLIを再起動
q restart

# 4. 設定ファイルを直接確認
q settings open

# 5. 全設定を確認
q settings all
```

---

### 問題8: 設定ファイルが開けない

**エラーメッセージ**:
```
Error: The EDITOR environment variable is not set
```

**原因**:
- EDITOR環境変数が設定されていない

**解決方法**:
```bash
# 1. EDITORを設定
export EDITOR=vim
# または
export EDITOR=nano
# または
export EDITOR=code

# 2. .bashrc または .zshrc に追加
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc

# 3. 設定ファイルを開く
q settings open
```

---

## リソース関連の問題

### 問題9: リソースファイルが見つからない

**警告メッセージ**:
```
Warning: Resource file not found: file://docs/guide.md
```

**原因**:
- ファイルが存在しない
- パスが間違っている
- カレントディレクトリが異なる

**解決方法**:
```bash
# 1. ファイルの存在を確認
ls -la docs/guide.md

# 2. カレントディレクトリを確認
pwd
```

3. 絶対パスを使用:
```json
{
  "resources": [
    "file:///absolute/path/to/docs/guide.md"
  ]
}
```

4. 相対パスを修正:
```json
{
  "resources": [
    "file://./docs/guide.md"
  ]
}
```

5. ワイルドカードを使用:
```json
{
  "resources": [
    "file://docs/**/*.md"
  ]
}
```

---

## 実験的機能の問題

### 問題10: Checkpointing が動作しない

**症状**:
- `/checkpoint`コマンドが使用できない

**原因**:
- Checkpointing機能が無効
- Gitリポジトリ外で使用
- 初期化されていない

**解決方法**:
```bash
# 1. 機能を有効化
/experiment
# → Checkpointingを選択してON

# 2. 手動で初期化（Gitリポジトリ外の場合）
/checkpoint init

# 3. Gitリポジトリを確認
git status

# 4. チェックポイント一覧を確認
/checkpoint list
```

---

### 問題11: Knowledge が検索できない

**症状**:
- `/knowledge search`で結果が返らない

**原因**:
- Knowledge機能が無効
- インデックスが作成されていない
- 検索クエリが不適切

**解決方法**:
```bash
# 1. 機能を有効化
/experiment
# → Knowledgeを選択してON

# 2. コンテンツを追加
/knowledge add ./docs
/knowledge add ./README.md

# 3. インデックスの状態を確認
/knowledge status

# 4. 検索クエリを変更
/knowledge search "different query"

# 5. Knowledge Baseの内容を確認
/knowledge show
```

---

## パフォーマンス関連の問題

### 問題12: Amazon Q CLIが遅い

**症状**:
- 応答が遅い
- 起動が遅い

**原因**:
- コンテキストウィンドウが満杯
- 多数のMCPサーバー
- 大きなKnowledge Base

**解決方法**:
```bash
# 1. コンテキストを圧縮
/compact

# 3. Knowledge Baseをクリーンアップ
/knowledge show
/knowledge remove <unused-path>

# 4. 履歴をクリア
/clear

# 5. Amazon Q CLIを再起動
q restart
```

2. 不要なMCPサーバーを無効化（設定ファイルを編集）:
```json
{
  "mcpServers": {
    "unused-server": {
      "disabled": true
    }
  }
}
```

---

### 問題13: コンテキストウィンドウが満杯

**症状**:
- コンテキスト使用率が90%以上
- 応答が遅い

**解決方法**:
```bash
# 1. コンテキスト使用率を確認
/experiment
# → Context Usage Percentageを有効化

# 2. コンテキストを圧縮
/compact

# 3. 新しいセッションを開始
/clear

# 4. Tangentモードを使用
/tangent
# サイドトピックを探索後、メインに戻る
/tangent
```

---

## ネットワーク関連の問題

### 問題14: OAuth認証が失敗する

**エラーメッセージ**:
```
Error: OAuth authentication failed
```

**原因**:
- ポートがブロックされている
- リダイレクトURIが一致しない
- ファイアウォールの問題

**解決方法**:
```bash
# 1. ポートを設定
q settings chat.oauthRedirectPort 7777

# 2. ファイアウォールでポートを開放
# Linuxの場合
sudo ufw allow 7777

# 3. OAuthプロバイダーの設定を確認
# リダイレクトURIが http://127.0.0.1:7777 と一致するか確認

# 4. ブラウザで手動アクセス
# 表示されたURLをブラウザで開く
```

---

### 問題15: テレメトリが送信されない

**症状**:
- アクティビティダッシュボードにデータが表示されない

**原因**:
- ネットワークの問題
- プロキシ設定
- テレメトリが無効

**解決方法**:
```bash
# 1. ネットワーク接続を確認
ping telemetry.us-east-1.amazonaws.com

# 2. プロキシ設定を確認
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 3. q doctor で診断
q doctor

# 4. ログを確認
# ログファイルを手動で確認
```

---

## デバッグ手順

### 一般的なデバッグフロー

```bash
# 1. 診断を実行
q doctor

# 2. 設定を確認
q settings all

# 3. Agent設定を確認
q agent list
cat .amazonq/cli-agents/<agent-name>.json | jq .

# 4. ログを確認
# ログファイルを手動で確認
tail -f <log-file>

# 5. Amazon Q CLIを再起動
q restart

# 6. 問題が解決しない場合、ISSUEを報告
/issue
```

### 詳細ログの有効化

```bash
# 環境変数でログレベルを設定
export RUST_LOG=debug

# Amazon Q CLIを起動
q chat

# ログを確認
# ログファイルを手動で確認
```

---

## FAQ

### Q1: デフォルトAgentを変更したい

```bash
q settings chat.defaultAgent <agent-name>
```

### Q2: 全ての設定をリセットしたい

```bash
# 設定ファイルを削除
rm ~/.local/share/amazon-q/settings.json

# Amazon Q CLIを再起動
q restart
```

### Q3: Agent設定ファイルの場所がわからない

```bash
# ローカル
ls -la .aws/amazonq/cli-agents/

# グローバル
ls -la ~/.aws/amazonq/cli-agents/
```

### Q4: MCPサーバーのログを確認したい

```bash
# ログファイルを手動で確認
q doctor

# ログを確認
tail -f <log-file>
```

### Q5: 設定のバックアップを取りたい

```bash
# 設定ファイルをバックアップ
cp ~/.local/share/amazon-q/settings.json ~/.local/share/amazon-q/settings.json.backup

# Agent設定をバックアップ
cp -r ~/.aws/amazonq/cli-agents ~/.aws/amazonq/cli-agents.backup
```

---

## サポートリソース

### 公式リソース

- [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)
- [GitHub Discussions](https://github.com/aws/amazon-q-developer-cli/discussions)
- [公式ドキュメント](https://github.com/aws/amazon-q-developer-cli/tree/main/docs)

### コミュニティリソース

- GitHub Issuesで類似の問題を検索
- Discussionsでベストプラクティスを確認

### ISSUEの報告

```bash
# Amazon Q CLI内からISSUEを報告
/issue

# または、GitHubで直接報告
# https://github.com/aws/amazon-q-developer-cli/04_issues/new
```

**ISSUE報告時に含めるべき情報**:
- Amazon Q CLIのバージョン（`q --version`）
- OS情報
- `q doctor`の出力
- エラーメッセージ
- 再現手順
- 期待される動作と実際の動作

---

## 🔧 高度なトラブルシューティング

### ログ分析

**システム診断**:
```bash
# 簡易診断（問題の診断と修復）
q doctor

# 詳細診断情報（TOML形式）
q diagnostic

# 詳細診断情報（JSON形式）
q diagnostic --format json

# 詳細診断情報（整形JSON）
q diagnostic --format json-pretty
```

**ログファイルの場所**:
```bash
# システム診断を実行（ログパスは表示されません）
q doctor

# ログファイルを手動で確認（OS別）
# Linux
ls -la /run/user/$(id -u)/qlog/qchat.log
# または
ls -la /tmp/qlog/qchat.log

# macOS
ls -la $TMPDIR/qlog/qchat.log

# Windows
dir %TEMP%\amazon-q\logs\qchat.log
```

**ログレベルの設定**:
```bash
# 環境変数で設定
export RUST_LOG=debug
export Q_LOG_LEVEL=debug
export Q_LOG_STDOUT=1  # コンソール出力も有効

# Amazon Q CLIをchatサブコマンドで起動（重要）
q chat
```

**ログの監視**:
```bash
# Linux - リアルタイムでログを監視
tail -f /run/user/$(id -u)/qlog/qchat.log
# または
tail -f /tmp/qlog/qchat.log

# macOS
tail -f $TMPDIR/qlog/qchat.log

# エラーのみ抽出（Linux例）
grep -i error /run/user/$(id -u)/qlog/qchat.log

# 特定のキーワードで検索
grep -i "mcp" /run/user/$(id -u)/qlog/qchat.log
```

### パフォーマンス診断

**応答時間の測定**:
```bash
# 時間計測付きでコマンド実行
time q chat --message "Hello"

# 詳細なプロファイリング
RUST_LOG=debug time q chat --message "Hello"
```

**リソース使用状況の確認**:
```bash
# プロセスの確認
ps aux | grep q

# メモリ使用量の確認
top -p $(pgrep q)

# ディスク使用量の確認
du -sh ~/.aws/amazonq/
du -sh ~/.local/share/amazon-q/
```

### ネットワーク診断

**接続テスト**:
```bash
# AWS エンドポイントへの接続確認
curl -I https://q.us-east-1.amazonaws.com

# プロキシ設定の確認
echo $HTTP_PROXY
echo $HTTPS_PROXY
echo $NO_PROXY

# DNS解決の確認
nslookup q.us-east-1.amazonaws.com
```

**プロキシ設定**:
```bash
# プロキシを設定
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

# Amazon Q CLIを再起動
q restart
```

### 設定のリセット

**段階的なリセット**:

**Step 1: キャッシュのクリア**
```bash
# チャット履歴のクリア
/clear

# Amazon Q CLIの再起動
q restart
```

**Step 2: 設定の初期化**
```bash
# 設定ファイルのバックアップ
cp ~/.local/share/amazon-q/settings.json ~/.local/share/amazon-q/settings.json.backup

# 特定の設定をリセット
q settings chat.defaultAgent --unset
q settings chat.model --unset

# Amazon Q CLIの再起動
q restart
```

**Step 3: 完全リセット**
```bash
# 全設定のバックアップ
cp -r ~/.local/share/amazon-q ~/.local/share/amazon-q.backup
cp -r ~/.aws/amazonq ~/.aws/amazonq.backup

# 設定ファイルの削除
rm -rf ~/.local/share/amazon-q/settings.json

# Agent設定の削除（オプション）
rm -rf ~/.aws/amazonq/cli-agents/*

# Amazon Q CLIの再起動
q restart
```

### 依存関係の確認

**必要なツールの確認**:
```bash
# Node.js（MCPサーバー用）
node --version
npm --version

# Python（MCPサーバー用）
python --version
pip --version

# Git（Checkpointing用）
git --version

# jq（JSON処理用）
jq --version
```

**MCPサーバーの依存関係**:
```bash
# npmパッケージの確認
npm list -g @modelcontextprotocol/server-filesystem

# Pythonパッケージの確認
pip list | grep mcp

# 依存関係のインストール
npm install -g @modelcontextprotocol/server-filesystem
pip install mcp-server-example
```

### 環境変数のデバッグ

**環境変数の確認**:
```bash
# Amazon Q CLI関連の環境変数を表示
env | grep -E '(Q_|AWS_|RUST_)'

# 特定の環境変数を確認
echo $Q_LOG_LEVEL
echo $AWS_PROFILE
echo $AWS_REGION
```

**環境変数の展開テスト**:
```bash
# Agent設定で環境変数を使用
cat .amazonq/cli-agents/test.json
{
  "mcpServers": {
    "test": {
      "env": {
        "API_KEY": "${env:MY_API_KEY}"
      }
    }
  }
}

# 環境変数を設定
export MY_API_KEY=test_value

# Amazon Q CLIを再起動して確認
q restart
q agent show test
```

### 競合の解決

**Agent名の競合**:
```bash
# 競合を確認
q agent list

# ローカルとグローバルのAgentを比較
diff .aws/amazonq/cli-agents/my-agent.json \
     ~/.aws/amazonq/cli-agents/my-agent.json

# どちらかを削除または名前変更
mv .amazonq/cli-agents/my-agent.json \
   .amazonq/cli-agents/local-my-agent.json
```

**設定の競合**:
```bash
# 設定の優先順位を確認
# 1. コマンドライン引数
# 2. 環境変数
# 3. Agent設定
# 4. グローバル設定
# 5. デフォルト値

# 実際の設定値を確認
q settings <key>

# 設定ファイルを直接確認
cat ~/.local/share/amazon-q/settings.json | jq .
```

### トラブルシューティングフローチャート

```
問題発生
    ↓
q doctor 実行
    ↓
エラーメッセージ確認
    ↓
┌─────────────────┐
│ Agent関連？     │ → Yes → Agent設定を確認
│                 │         - q agent list
│                 │         - JSON構文チェック
└─────────────────┘         - スキーマ検証
    ↓ No
┌─────────────────┐
│ MCP関連？       │ → Yes → MCP設定を確認
│                 │         - コマンド実行テスト
│                 │         - 環境変数確認
└─────────────────┘         - ログ確認
    ↓ No
┌─────────────────┐
│ 設定関連？      │ → Yes → 設定を確認
│                 │         - q settings all
│                 │         - 設定ファイル確認
└─────────────────┘         - Amazon Q CLI再起動
    ↓ No
┌─────────────────┐
│ パフォーマンス？│ → Yes → リソース確認
│                 │         - コンテキスト圧縮
│                 │         - MCP無効化
└─────────────────┘         - Knowledge整理
    ↓ No
┌─────────────────┐
│ ネットワーク？  │ → Yes → 接続確認
│                 │         - プロキシ設定
│                 │         - ファイアウォール
└─────────────────┘         - DNS確認
    ↓ No
GitHub ISSUEを報告
```

---

## 参考リンク

- [推奨設定ガイド](../04_best-practices/01_configuration.md)
- [ベストプラクティス](../04_best-practices/01_configuration.md)
- [Agent設定ファイル完全仕様](../03_configuration/04_agent-configuration.md)
- [GitHub Repository](https://github.com/aws/amazon-q-developer-cli)

---

**ドキュメント作成日**: 2025-10-08  
**最終更新**: 2025-10-08
