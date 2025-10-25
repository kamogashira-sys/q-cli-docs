[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [設定ガイド](README.md) > 05 Environment Variables

---

# Amazon Q CLI 環境変数ガイド

**作成日**: 2025-10-08  
**ソースコード**: `crates/chat-cli/src/util/consts.rs`, `crates/chat-cli/src/mcp_client/client.rs`  
**対象バージョン**: v1.17.0以降

## 概要

このドキュメントは、Amazon Q CLIでサポートされる環境変数の完全なリストと使用方法を提供します。

---

## XDG Base Directory仕様

Q CLIはLinux環境でXDG Base Directory仕様に従います：

### 使用される環境変数

| 環境変数 | 用途 | デフォルト値 | Q CLIでの使用 |
|----------|------|--------------|---------------|
| `XDG_DATA_HOME` | アプリケーションデータ | `~/.local/share` | ✅ 使用 |
| `XDG_CONFIG_HOME` | 設定ファイル | `~/.config` | ❌ 未使用 |

### 設定例

```bash
# カスタムデータディレクトリを指定
export XDG_DATA_HOME="$HOME/custom-data"
# 結果: $HOME/custom-data/amazon-q/settings.json

# XDG_CONFIG_HOMEは影響しない
export XDG_CONFIG_HOME="$HOME/custom-config"
# 結果: ~/.local/share/amazon-q/settings.json（変わらず）
```

### 重要な注意事項

- Q CLIは設定ファイルを「アプリケーションデータ」として扱います
- `XDG_CONFIG_HOME`を設定しても設定ファイルは`~/.config/q/`には配置されません（Q CLIは`XDG_DATA_HOME`を使用）
- 設定ファイルは常に`XDG_DATA_HOME`または`~/.local/share`配下に配置されます

---

## 環境変数の設定方法

### 一時的な設定（現在のセッションのみ）

#### 単一コマンドで使用
```bash
Q_LOG_LEVEL=debug q chat "Hello"
```

#### セッション全体で使用
```bash
export Q_LOG_LEVEL=debug
q chat "Hello"
```

---

### 永続的な設定（シェル起動時に自動設定）

#### Bash（~/.bashrc）
```bash
# ~/.bashrc に追加
export Q_LOG_LEVEL=debug
export AWS_PROFILE=my-profile

# 設定を反映
source ~/.bashrc
```

#### Zsh（~/.zshrc）
```bash
# ~/.zshrc に追加
export Q_LOG_LEVEL=debug
export AWS_PROFILE=my-profile

# 設定を反映
source ~/.zshrc
```

#### Fish（~/.config/fish/config.fish）
```fish
# ~/.config/fish/config.fish に追加
set -x Q_LOG_LEVEL debug
set -x AWS_PROFILE my-profile
```

---

### プロジェクト単位の設定（.envファイル）

```bash
# プロジェクトルートに .env ファイルを作成
cat > .env << 'EOF'
Q_LOG_LEVEL=debug
AWS_PROFILE=my-project
AWS_REGION=us-east-1
EOF

# direnvを使用して自動読み込み
echo 'dotenv' > .envrc
direnv allow
```

---

### 設定の確認

```bash
# 環境変数の確認
echo $Q_LOG_LEVEL
env | grep Q_

# Amazon Q CLIから確認
q settings list
```

---

### よくある間違い

#### ❌ 間違い: スペースを入れる
```bash
export Q_LOG_LEVEL = debug  # エラー
```

#### ✅ 正しい: スペースなし
```bash
export Q_LOG_LEVEL=debug
```

#### ❌ 間違い: 引用符の誤り
```bash
export AWS_PROFILE='my-profile  # 閉じ引用符がない
```

#### ✅ 正しい: 引用符を正しく使用
```bash
export AWS_PROFILE='my-profile'
# または
export AWS_PROFILE=my-profile  # スペースがない場合は不要
```

---

## Amazon Q CLI固有の環境変数

### コア環境変数

| 環境変数 | 説明 | 使用例 |
|---------|------|--------|
| `Q_LOG_LEVEL` | ログレベルを設定 | `export Q_LOG_LEVEL=debug` |
| `Q_LOG_STDOUT` | 標準出力へのログ出力を有効化 | `export Q_LOG_STDOUT=1` |
| `Q_CLI_CLIENT_APPLICATION` | クライアントアプリケーションの識別子 | `export Q_CLI_CLIENT_APPLICATION=my-app` |
| `Q_DISABLE_TELEMETRY` | テレメトリを無効化（値は問わない） | `export Q_DISABLE_TELEMETRY=1` |

### qterm関連環境変数

| 環境変数 | 説明 | 使用例 |
|---------|------|--------|
| `QTERM_SESSION_ID` | 現在の親qtermインスタンスのUUID | 自動設定 |
| `Q_PARENT` | 接続する親ソケット | 自動設定 |
| `Q_SET_PARENT` | 親ソケットを設定 | 自動設定 |
| `Q_SET_PARENT_CHECK` | Q_SET_PARENTチェックのガード | 自動設定 |
| `Q_TERM` | qtermが実行中の場合に設定（バージョンを含む） | 自動設定 |
| `Q_SHELL` | qtermで使用するシェル | `export Q_SHELL=/bin/zsh` |
| `Q_ZDOTDIR` | ZDOTDIR環境変数をオーバーライド | `export Q_ZDOTDIR=/custom/path` |

### デバッグ・開発用環境変数

| 環境変数 | 説明 | 使用例 |
|---------|------|--------|
| `Q_DEBUG_SHELL` | シェルデバッグモードを有効化 | `export Q_DEBUG_SHELL=1` |
| `Q_FAKE_IS_REMOTE` | リモート環境をシミュレート（テスト用） | `export Q_FAKE_IS_REMOTE=1` |
| `Q_CODESPACES` | Codespaces環境を示す | `export Q_CODESPACES=1` |
| `Q_CI` | CI環境を示す | `export Q_CI=1` |
| `Q_BUNDLE_METADATA_PATH` | バンドルメタデータへのパスをオーバーライド | `export Q_BUNDLE_METADATA_PATH=/path/to/metadata` |
| `Q_DISABLE_TRUECOLOR` | Trueカラー表示を無効化 | `export Q_DISABLE_TRUECOLOR=1` |
| `Q_MOCK_CHAT_RESPONSE` | チャット応答をモック（テスト用） | `export Q_MOCK_CHAT_RESPONSE='{"response":"test"}'` |

### その他のQ関連環境変数

| 環境変数 | 説明 | 使用例 |
|---------|------|--------|
| `PROCESS_LAUNCHED_BY_Q` | Amazon Qによって起動されたプロセスを示す | 自動設定 |
| `Q_USING_ZSH_AUTOSUGGESTIONS` | zsh autosuggestionsを使用中（Inlineを無効化） | 自動設定 |
| `Q_TELEMETRY_CLIENT_ID` | テレメトリクライアントID | 自動設定 |

### AWS認証関連環境変数

| 環境変数 | 説明 | 使用例 |
|---------|------|--------|
| `AMAZON_Q_SIGV4` | SigV4認証を有効化 | `export AMAZON_Q_SIGV4=1` |
| `AMAZON_Q_CHAT_SHELL` | チャットで使用するシェル | `export AMAZON_Q_CHAT_SHELL=zsh` |

---

## システム環境変数

Amazon Q CLIは以下のシステム環境変数も使用します：

| 環境変数 | 説明 | デフォルト値 |
|---------|------|------------|
| `EDITOR` | テキストエディタ | `vi` |
| `TERM` | ターミナルタイプ | - |
| `CI` | CI環境を示す | - |
| `CODESPACES` | GitHub Codespaces環境を示す | - |

---

## 環境変数の展開（`${env:VAR_NAME}`構文）

### 概要

Amazon Q CLIは、Agent設定ファイルとMCP設定で`${env:VAR_NAME}`構文による環境変数展開をサポートしています。

### 使用例

#### MCP STDIO設定での使用

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${env:HOME}/mcp-servers/my-server/index.js"],
      "env": {
        "API_KEY": "${env:MY_API_KEY}"
      }
    }
  }
}
```

#### MCP HTTP設定での使用（v1.17.0+）

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://api.example.com/mcp",
      "transport": {
        "type": "http",
        "headers": {
          "Authorization": "Bearer ${env:API_TOKEN}"
        }
      }
    }
  }
}
```

### 展開の仕組み

```rust
fn substitute_env_vars(input: &str, env: &crate::os::Env) -> String {
    let re = Regex::new(r"\$\{env:([^}]+)\}").unwrap();
    re.replace_all(input, |caps: &regex::Captures<'_>| {
        let var_name = &caps[1];
        env.get(var_name).unwrap_or_else(|_| format!("${{{}}}", var_name))
    }).to_string()
}
```

**動作**:
- 正規表現で`${env:VAR_NAME}`パターンをマッチ
- 環境変数が存在する場合、その値に置換
- 環境変数が存在しない場合、元の文字列を保持

---

## 環境変数の優先順位

設定の優先順位（高→低）：

1. **コマンドライン引数** - 最優先
2. **環境変数** - 次点
3. **Agent設定ファイル** - 環境変数より低い
4. **グローバル設定ファイル** - Agent設定より低い
5. **デフォルト値** - 最後のフォールバック

### 例: ログレベルの決定

```bash
# コマンドライン引数が最優先
q chat -vvv  # verboseレベル3

# 環境変数が次点
export Q_LOG_LEVEL=debug
q chat

# デフォルト値（ERROR）
q chat
```

---

## 使用例

### 開発環境でのデバッグ

```bash
# デバッグログを有効化
export Q_LOG_LEVEL=debug
export Q_LOG_STDOUT=1

# Amazon Q CLIを起動
q chat
```

### カスタムシェルの使用

```bash
# チャットで使用するシェルを変更
export AMAZON_Q_CHAT_SHELL=zsh

# Amazon Q CLIを起動
q chat
```

### MCP設定での環境変数使用

```bash
# APIキーを環境変数に設定
export MY_API_KEY=your-api-key-here

# Agent設定ファイルで使用
# ~/.aws/amazonq/cli-agents/my-agent.json
{
  "name": "my-agent",
  "mcpServers": {
    "api-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${env:MY_API_KEY}"
      }
    }
  }
}
```

---

## トラブルシューティング

### 環境変数が展開されない

**症状**: `${env:VAR_NAME}`が文字列としてそのまま残る

**原因**: 環境変数が設定されていない

**解決策**:
```bash
# 環境変数を設定
export VAR_NAME=value

# Amazon Q CLIを再起動
q restart
```

### ログレベルが変更されない

**症状**: `Q_LOG_LEVEL`を設定してもログレベルが変わらない

**原因**: コマンドライン引数が優先されている

**解決策**:
```bash
# コマンドライン引数を削除
q chat  # -vオプションなし
```

---

## ベストプラクティス

詳細なベストプラクティスは以下を参照してください：
- [設定のベストプラクティス](../04_best-practices/01_configuration.md)
- [セキュリティベストプラクティス](../04_best-practices/02_security.md)
- [パフォーマンス最適化](../04_best-practices/03_performance.md)

---

## 参考リンク

- [設定優先順位ガイド](07_priority-rules.md) - 設定の優先順位と図解
- [設定項目完全リファレンス](../07_reference/03_settings-reference.md)
- [推奨設定ガイド](../04_best-practices/01_configuration.md)
- [ベストプラクティス](../04_best-practices/01_configuration.md)
- [Agent設定ファイル完全仕様](03_agent-configuration.md)

---

**ドキュメント作成日**: 2025-10-08  
**最終更新**: 2025-10-08  
**ソースコード**: `crates/chat-cli/src/util/consts.rs`, `crates/chat-cli/src/mcp_client/client.rs` (v1.17.0)
---

**関連トピック**:
- [設定優先順位ガイド](07_priority-rules.md)
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)

## 関連ドキュメント

- [セキュリティ概要](../09_security/01_security-overview.md) - セキュリティ設定の基本
- [テレメトリー設定](../03_configuration/05_telemetry.md) - テレメトリー環境変数の詳細
- [エンタープライズ展開ガイド](../05_deployment/01_enterprise-deployment.md) - 組織での環境変数管理
