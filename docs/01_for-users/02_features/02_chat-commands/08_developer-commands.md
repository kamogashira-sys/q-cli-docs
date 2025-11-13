[ホーム](../../../README.md) > [ユーザーガイド](../../README.md) > [機能ガイド](../README.md) > [チャット機能](../01_chat.md) > 開発者向けコマンド

---

# 開発者向けコマンド

**対象バージョン**: v1.13.0以降

## 📋 コマンド概要

開発者向けコマンドは、Q CLIの内部状態の確認、トラブルシューティング、実験的機能の管理を行うコマンド群です。問題の診断、ログの収集、MCPサーバーの管理、使用量の監視などの高度な機能を提供します。

## 🚀 基本的な使い方

### 開発者向けコマンド一覧

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/logdump [オプション]` | サポート調査用のログファイルを収集してZIPアーカイブとして出力。`--mcp`でMCPログも含めることが可能（v1.18.0+） | 問題発生時にログを収集してサポートチームに提出する時、デバッグ情報を効率的に収集する時 |
| `/tools [サブコマンド]` | ツールと権限を管理。利用可能なツール一覧の表示、ツールの信頼設定、権限のリセットが可能。デフォルトでは、特定のツール使用時に確認を求める | どのツールが使えるか確認したい時、ツールを自動承認したい時、権限をリセットしたい時 |
| `/mcp` | MCPサーバーの状態を確認。接続状況、利用可能なツール、エラー情報を表示 | MCPサーバーが正常に動作しているか確認したい時、トラブルシューティングする時 |
| `/reply` | 最新のAI応答を引用して$EDITORで返信を作成 | 長文の返信を書きたい時、AI応答の特定部分にコメントしたい時 |
| `/usage` | コンテキスト使用量を表示。現在のトークン使用量、制限値、残り容量を確認できる | メモリ制約に近づいているか確認したい時、コンテキスト最適化の判断をする時 |
| `/experiment` | 実験的機能のON/OFF切り替え。Knowledge、Checkpoint、TODO等のベータ機能を有効化 | 新機能を試したい時、実験的機能を有効化/無効化する時 |

### 基本例

```bash
# ログを収集
/logdump

# MCPサーバーの状態確認
/mcp

# 使用可能なツール確認
/tools

# コンテキスト使用量確認
/usage

# 実験的機能を有効化
/experiment
```

## ⚙️ オプション・引数

### `/logdump` コマンド

| オプション | 説明 | 使用例 |
|-----------|------|--------|
| `[なし]` | 基本ログを収集 | `/logdump` |
| `--mcp` | MCPサーバーのログも含める | `/logdump --mcp` |

### `/tools` コマンド

| サブコマンド | 説明 | 使用例 |
|-------------|------|--------|
| `[なし]` | 利用可能なツール一覧を表示 | `/tools` |
| `trust <ツール名>` | 指定したツールを自動承認 | `/tools trust execute_bash` |
| `untrust <ツール名>` | 指定したツールの自動承認を解除 | `/tools untrust execute_bash` |
| `reset` | すべてのツール権限をリセット | `/tools reset` |

### `/experiment` コマンド

実験的機能の有効化/無効化を行います：

| 機能 | 説明 | 設定コマンド |
|------|------|-------------|
| **Knowledge** | ファイルインデックス機能 | `q settings chat.enableKnowledge true` |
| **Checkpoint** | ワークスペース状態管理 | `q settings chat.enableCheckpoint true` |
| **TODO** | タスク管理機能 | `q settings chat.enableTodoList true` |
| **Tangent** | 会話分岐機能 | `q settings chat.enableTangentMode true` |

## 💡 実用例

### 例1: 問題発生時のログ収集とサポート依頼

**シナリオ**: Q CLIで問題が発生し、サポートチームに報告したい

```bash
# 基本ログを収集
/logdump

# 出力例:
# 📦 Log dump created: /tmp/q-cli-logs-20251113-205500.zip
# 
# Contents:
# - qchat.log (45.2 KB)
# - system.log (12.8 KB)
# - config.json (2.1 KB)
# - agent-config.json (1.5 KB)

# MCPサーバー関連の問題の場合
/logdump --mcp

# 出力例:
# 📦 Log dump created: /tmp/q-cli-logs-mcp-20251113-205530.zip
# 
# Contents:
# - qchat.log (45.2 KB)
# - system.log (12.8 KB)
# - mcp-server-1.log (23.7 KB)
# - mcp-server-2.log (18.4 KB)
# - config.json (2.1 KB)
# - agent-config.json (1.5 KB)

# ログファイルをサポートチームに送信
# （実際の送信方法は組織の手順に従う）
```

**結果**: 問題の詳細情報を効率的に収集し、サポートチームが迅速に対応できる

### 例2: ツール権限の管理と最適化

**シナリオ**: 頻繁に使用するツールを自動承認して作業効率を向上させたい

```bash
# 現在利用可能なツールを確認
/tools

# 出力例:
# 🔧 Available Tools:
# 
# ✅ Trusted (Auto-approved):
#   - fs_read
#   - fs_write
# 
# ⚠️  Requires Confirmation:
#   - execute_bash
#   - call_aws
#   - use_aws
# 
# ❌ Restricted:
#   - system_admin

# よく使うツールを自動承認
/tools trust execute_bash
/tools trust call_aws

# 設定後の確認
/tools

# 出力例:
# 🔧 Available Tools:
# 
# ✅ Trusted (Auto-approved):
#   - fs_read
#   - fs_write
#   - execute_bash
#   - call_aws
# 
# ⚠️  Requires Confirmation:
#   - use_aws
# 
# ❌ Restricted:
#   - system_admin

# 必要に応じて権限をリセット
/tools reset
```

**結果**: 作業効率を向上させながら、セキュリティを適切に管理できる

### 例3: MCPサーバーのトラブルシューティング

**シナリオ**: MCPサーバーが正常に動作しているか確認し、問題を特定したい

```bash
# MCPサーバーの状態を確認
/mcp

# 出力例:
# 🔌 MCP Server Status:
# 
# ✅ awslabs.core-mcp-server
#   Status: Connected
#   Tools: 15 available
#   Resources: 8 available
#   Last ping: 2025-11-13 20:55:00
# 
# ⚠️  awslabs.cost-explorer-mcp-server
#   Status: Connection timeout
#   Error: Failed to initialize after 30s
#   Last attempt: 2025-11-13 20:54:30
# 
# ❌ custom-mcp-server
#   Status: Failed
#   Error: Permission denied
#   Config: ~/.aws/amazonq/mcp.json

# 問題のあるサーバーの詳細ログを収集
/logdump --mcp

# MCP設定ファイルを確認
cat ~/.aws/amazonq/mcp.json

# 必要に応じてサーバーを再起動
/quit
q chat
```

**結果**: MCPサーバーの問題を特定し、適切な対処を行える

## 🔧 トラブルシューティング

### よくある問題

#### 問題1: ログダンプが作成できない

**症状**: `/logdump` でエラーが発生する

**原因**: ディスク容量不足、または権限の問題

**解決策**:
```bash
# ディスク容量を確認
df -h /tmp

# 権限を確認
ls -la /tmp

# 別の場所を指定（可能な場合）
# または不要なファイルを削除
rm /tmp/old-files*

# 再試行
/logdump
```

#### 問題2: ツールの信頼設定が保存されない

**症状**: `/tools trust` を実行しても次回起動時にリセットされる

**原因**: 設定ファイルの権限問題、または設定の競合

**解決策**:
```bash
# 設定ファイルの権限を確認
ls -la ~/.aws/amazonq/

# 設定を手動で確認
q settings list | grep tool

# チャットを再起動して確認
/quit
q chat
/tools
```

#### 問題3: MCPサーバーが接続できない

**症状**: `/mcp` で特定のサーバーが「Failed」状態

**原因**: サーバー設定の問題、またはネットワークの問題

**解決策**:
```bash
# MCP設定を確認
cat ~/.aws/amazonq/mcp.json

# サーバーのログを確認
/logdump --mcp

# 設定ファイルの構文を確認
cat ~/.aws/amazonq/mcp.json | jq .

# 必要に応じて設定を修正
```

#### 問題4: 実験的機能が有効化されない

**症状**: `/experiment` で機能を有効化してもコマンドが使用できない

**原因**: 設定の反映遅延、または設定値の問題

**解決策**:
```bash
# 設定を直接確認
q settings chat.enableKnowledge true
q settings chat.enableCheckpoint true
q settings chat.enableTodoList true

# 設定の確認
q settings list | grep enable

# チャットを再起動
/quit
q chat
```

#### 問題5: コンテキスト使用量が表示されない

**症状**: `/usage` で情報が表示されない

**原因**: 機能の制限、またはデータの問題

**解決策**:
```bash
# 会話を開始してから再確認
"テスト用のメッセージ"

# 使用量を再確認
/usage

# コンテキストを追加してテスト
/context add README.md
/usage
```

## 🔗 関連コマンド

- [コンテキスト管理](02_context-management.md) - `/compact`によるメモリ最適化
- [基本コマンド・会話管理](01_basic-commands.md) - 問題発生時の会話保存
- [Agent管理](07_agent-management.md) - Agent設定との連携

## 📖 参照元

- [チャット機能概要](../01_chat.md#開発者向けコマンド) - 開発者向けコマンドの概要
- [トラブルシューティングガイド](../../06_troubleshooting/02_common-issues.md) - 一般的な問題の解決方法
- [実験的機能ガイド](../07_experimental.md) - 実験的機能の詳細

---

最終更新: 2025年11月13日
