[ホーム](../README.md) > [機能詳細ガイド](README.md) > Agent Client Protocol (ACP)

---

# Kiro CLI Agent Client Protocol (ACP) 統合

**出典**: [Agent Client Protocol (ACP) - Kiro CLI Documentation](https://kiro.dev/docs/cli/acp/)、`kiro-cli version --changelog=all`（v1.26.0情報）

## 概要

Kiro CLI v1.25.0（2026年2月4日リリース）で追加されたAgent Client Protocol (ACP) 統合機能について詳細に解説します。v1.26.0（2026年2月12日リリース）では、**`--agent`フラグ**と**ACP/subagent用`code`ツール**が追加されました。

### Agent Client Protocol (ACP) とは

Agent Client Protocol (ACP) は、**エディタとAIエージェント間の標準通信プロトコル**です。JSON-RPC 2.0（JSON 形式でリクエスト/レスポンスをやり取りする軽量な通信規約）を使用して stdin/stdout（プログラムの標準入力・標準出力）で通信し、エディタからAIエージェントを統合的に利用できます。

### 主な特徴

- **標準プロトコル**: JSON-RPC 2.0 over stdin/stdout
- **エディタ統合**: JetBrains IDEs、Zed等のACP対応エディタで使用可能
- **Kiro拡張**: スラッシュコマンド、MCPツール、セッション管理をサポート
- **セッション保存**: `~/.kiro/sessions/cli/`に自動保存
- **`--agent`フラグ（v1.26.0）**: `kiro-cli acp --agent <agent-name>`でエージェント指定
- **`code`ツール対応（v1.26.0）**: ACP・subagentで`code`ツール（Code Intelligence）が利用可能

### なぜACPが必要なのか

従来、Kiro CLIはターミナルでのみ使用可能でした。ACP統合により、以下が実現します：

1. **エディタ内統合**: IDEやエディタから直接Kiroを使用
2. **標準化**: 複数のエディタで統一されたインターフェース
3. **拡張性**: Kiro独自の機能もエディタから利用可能

## 📋 目次

- [サポートされるACPメソッド](#サポートされるacpメソッド)
- [Kiro拡張機能](#kiro拡張機能)
- [セットアップ方法](#セットアップ方法)
- [セッション保存](#セッション保存)
- [ログ](#ログ)
- [ユースケース](#ユースケース)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## サポートされるACPメソッド

Kiro CLIは、標準ACPメソッドとKiro拡張メソッドをサポートしています。

### コアプロトコル

| メソッド | 説明 | 対応 |
|---------|------|------|
| `initialize` | エージェント初期化 | ✅ |
| `initialized` | 初期化完了通知 | ✅ |
| `shutdown` | エージェント終了 | ✅ |
| `exit` | プロセス終了 | ✅ |

### エージェント機能

| メソッド | 説明 | 対応 |
|---------|------|------|
| `agent/sendMessage` | メッセージ送信 | ✅ |
| `agent/cancelMessage` | メッセージキャンセル | ✅ |
| `agent/getCapabilities` | エージェント機能取得 | ✅ |

### セッション更新

| メソッド | 説明 | 対応 |
|---------|------|------|
| `session/didUpdate` | セッション更新通知 | ✅ |

---

## Kiro拡張機能

Kiro CLIは、標準ACPに加えて以下の拡張機能を提供します。

### スラッシュコマンド

エディタからKiro CLIのスラッシュコマンドを実行できます。

**対応コマンド例**:
- `/help` - Help Agentに切り替え
- `/agent` - エージェント管理
- `/context` - コンテキスト管理
- `/tools` - ツール一覧表示

### MCPサーバーイベント

MCPサーバーの起動・停止イベントをエディタに通知します。

**イベント種類**:
- `mcp/serverStarted` - MCPサーバー起動
- `mcp/serverStopped` - MCPサーバー停止
- `mcp/serverError` - MCPサーバーエラー

### セッション管理

エディタからKiro CLIのセッションを管理できます。

**機能**:
- セッション保存: `~/.kiro/sessions/cli/`
- セッション復元: 過去のセッションを読み込み
- セッション一覧: 保存済みセッションの確認

---

## セットアップ方法

### JetBrains IDEs

#### 1. Kiro CLIのインストール

```bash
# Kiro CLIがインストールされていることを確認
kiro-cli --version
```

#### 2. JetBrains IDEの設定

1. **Settings** → **Tools** → **AI Assistant** を開く
2. **Custom Agent** を選択
3. **Command** に以下を入力:

```bash
/usr/local/bin/kiro-cli acp
```

**特定のエージェントを指定する場合（v1.26.0以降）**:

```bash
/usr/local/bin/kiro-cli acp --agent my-agent
```

**重要**: 完全なパスを指定してください。`which kiro-cli`で確認できます。

#### 3. 動作確認

1. IDEでAI Assistantを開く
2. Kiroに質問を送信
3. 応答が返ってくることを確認

### Zed

#### 1. Kiro CLIのインストール

```bash
# Kiro CLIがインストールされていることを確認
kiro-cli --version
```

#### 2. Zedの設定

1. **Settings** → **AI** を開く
2. **Custom Agent** を追加
3. **Command** に以下を入力:

```bash
/usr/local/bin/kiro-cli acp
```

**重要**: 完全なパスを指定してください。`which kiro-cli`で確認できます。

#### 3. 動作確認

1. ZedでAI Assistantを開く
2. Kiroに質問を送信
3. 応答が返ってくることを確認

### その他のエディタ

ACP対応エディタであれば、同様の手順で設定できます。

**設定のポイント**:
1. `kiro-cli acp`コマンドを実行
2. 完全なパスを指定
3. stdin/stdout通信を使用

---

## セッション保存

Kiro CLIは、ACPセッションを自動的に保存します。

### 保存場所

```
~/.kiro/sessions/cli/
```

### セッションファイル形式

```
~/.kiro/sessions/cli/session-<timestamp>.json
```

**例**:
```
~/.kiro/sessions/cli/session-20260204-143022.json
```

### セッション内容

セッションファイルには以下が保存されます：

- **メッセージ履歴**: ユーザーとエージェントの会話
- **コンテキスト**: 使用したファイルやコード
- **設定**: エージェント設定やツール設定
- **メタデータ**: タイムスタンプ、エージェント名等

### セッション復元

保存されたセッションは、`/chat load`コマンドで復元できます。

```bash
/chat load ~/.kiro/sessions/cli/session-20260204-143022.json
```

---

## ログ

Kiro CLIは、ACPセッションのログを出力します。

### ログ場所

#### macOS

```
$TMPDIR/kiro-log/kiro-chat.log
```

**例**:
```
/var/folders/xy/abc123/T/kiro-log/kiro-chat.log
```

#### Linux

```
$XDG_RUNTIME_DIR/kiro-log/kiro-chat.log
```

**例**:
```
/run/user/1000/kiro-log/kiro-chat.log
```

### ログ内容

ログには以下が記録されます：

- **JSON-RPC通信**: リクエスト/レスポンス
- **エラー**: 通信エラー、処理エラー
- **デバッグ情報**: 内部処理の詳細

### ログの確認

```bash
# macOS
tail -f $TMPDIR/kiro-log/kiro-chat.log

# Linux
tail -f $XDG_RUNTIME_DIR/kiro-log/kiro-chat.log
```

---

## ユースケース

### ユースケース1: IDEでのコード生成

**シナリオ**: JetBrains IDEでコードを生成

1. IDEでファイルを開く
2. AI Assistantを起動
3. Kiroに「この関数をリファクタリングして」と依頼
4. Kiroがコードを生成
5. IDEで直接適用

**メリット**:
- ターミナルとIDEを切り替える必要がない
- コンテキストが自動的に共有される
- 生成されたコードを即座に適用

### ユースケース2: Zedでのドキュメント作成

**シナリオ**: Zedでドキュメントを作成

1. Zedでマークダウンファイルを開く
2. AI Assistantを起動
3. Kiroに「このコードのドキュメントを作成して」と依頼
4. Kiroがドキュメントを生成
5. Zedで編集・保存

**メリット**:
- エディタ内で完結
- リアルタイムプレビュー
- 即座に編集可能

### ユースケース3: チーム開発での統一

**シナリオ**: チーム全体でKiroを使用

1. チームメンバーが各自のエディタでKiroを設定
2. 同じエージェント設定を共有
3. 統一されたコーディング規約を適用

**メリット**:
- エディタの違いを吸収
- 統一された開発体験
- チーム全体の生産性向上

---

## トラブルシューティング

### 問題1: エディタでKiroが起動しない

**症状**: エディタでKiroを設定したが、応答がない

**原因**:
- `kiro-cli`のパスが正しくない
- Kiro CLIがインストールされていない
- 権限の問題

**解決方法**:

1. **パスの確認**:
```bash
which kiro-cli
# 出力例: /usr/local/bin/kiro-cli
```

2. **完全なパスを使用**:
```bash
/usr/local/bin/kiro-cli acp
```

3. **権限の確認**:
```bash
ls -l $(which kiro-cli)
# 実行権限があることを確認
```

### 問題2: セッションが保存されない

**症状**: セッションが`~/.kiro/sessions/cli/`に保存されない

**原因**:
- ディレクトリが存在しない
- 書き込み権限がない

**解決方法**:

1. **ディレクトリの作成**:
```bash
mkdir -p ~/.kiro/sessions/cli/
```

2. **権限の確認**:
```bash
ls -ld ~/.kiro/sessions/cli/
# 書き込み権限があることを確認
```

### 問題3: ログが出力されない

**症状**: ログファイルが作成されない

**原因**:
- ログディレクトリが存在しない
- 環境変数が設定されていない

**解決方法**:

1. **macOS**:
```bash
echo $TMPDIR
# 出力があることを確認
mkdir -p $TMPDIR/kiro-log/
```

2. **Linux**:
```bash
echo $XDG_RUNTIME_DIR
# 出力があることを確認
mkdir -p $XDG_RUNTIME_DIR/kiro-log/
```

---

## v1.26.0での変更点

### `--agent`フラグの追加

v1.26.0で`kiro-cli acp`サブコマンドに`--agent`フラグが追加されました。これにより、ACP起動時に使用するエージェントを指定できます。

```bash
# デフォルトエージェントで起動
kiro-cli acp

# 特定のエージェントを指定して起動（v1.26.0以降）
kiro-cli acp --agent my-custom-agent
```

### ACP/subagent用`code`ツール

v1.26.0で、ACPおよびsubagentから`code`ツール（Code Intelligence）が利用可能になりました。これにより、エディタ統合時にもLSPベースのコード理解機能（シンボル検索、定義ジャンプ、参照検索等）を活用できます。

### デフォルトエージェント読み込みの修正

v1.26.0で、ACPのデフォルトエージェント読み込みに関するバグが修正されました。

---

## 関連リンク

### 公式ドキュメント
- [Agent Client Protocol (ACP) - Kiro CLI Documentation](https://kiro.dev/docs/cli/acp/)
- [Kiro CLI v1.25.0 Changelog](https://kiro.dev/changelog/cli/1-25/)

### 関連機能
- [Help Agent](14_HelpAgent.md) - Kiro CLIドキュメントベースのヘルプ
- [マルチセッション機能](04_MultiSession.md) - セッション管理
- [サブエージェント機能](02_Subagents.md) - エージェント委譲

### リファレンス（辞書）
- [04_reference/01_settings.md](../04_reference/01_settings.md) — `KIRO_ACP_RECORD_PATH` 環境変数の仕様
- [04_reference/04_built-in-tools.md](../04_reference/04_built-in-tools.md) — ACP 用 `code` ツール（v1.26.0+）

### 公式 MCP サーバー（外部統合）
- [26. Agent Toolkit for AWS](26_AgentToolkitForAWS.md) 🌟 — AWS 公式 MCP Server（ACP と並列利用可能、エージェントへの AWS 機能付与）

### 関連ワークフロー方法論（OSS）
- [07. AI-DLC（Kiro CLI で実践する選択肢）](../07_aidlc/README.md) 🚀 — **AWS Labs 公式 OSS（MIT-0）の AI 駆動開発方法論**。**IDE 非依存** で設計されており、ACP 経由で接続するエディタ（Zed / JetBrains 等）からも、ACP 非対応のエディタ（Kiro IDE / Cursor / VS Code 等）からも、同一の Steering Files 配置で利用可能。`Kiro / Kiro CLI / Amazon Q Developer CLI / Claude Code / GitHub Copilot / Cursor / Cline / Codex` を公式サポート（GitHub README より）。

### エディタドキュメント
- [JetBrains AI Assistant](https://www.jetbrains.com/help/idea/ai-assistant.html)
- [Zed AI](https://zed.dev/docs/ai)

### 参考記事
- [Kiro CLI が ACP 対応！好きなエディタで Kiro CLI を使おう](https://zenn.dev/aws_japan/articles/64ea04fd0567be) - Zenn記事 by konippi（ACP概要・セットアップ解説）
- [Kiro CLI によるコードレビューを ACP で実現する](https://zenn.dev/aws_japan/articles/91dcdf769e9b10) - Zenn記事 by konippi（ACP活用によるCI/CDコードレビュー）

---

**最終更新**: 2026-07-04
**対象バージョン**: Kiro CLI v1.25.0+（v1.26.0 `--agent` フラグ・`code` ツール対応を含む）
