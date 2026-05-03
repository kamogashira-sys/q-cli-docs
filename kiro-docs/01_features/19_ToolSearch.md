# Kiro CLI Tool Search機能

**出典**: [Tool Search](https://kiro.dev/docs/cli/mcp/tool-search/)、[公式Changelog v2.1.0](https://kiro.dev/changelog/cli/2-1/)、CLI changelog v2.1.0

## 概要

### Tool Searchとは

Kiro CLI v2.1.0（2026年4月24日リリース）で追加された、MCPツールをオンデマンドでロードする機能です。全ツール定義を毎回送信する代わりに、必要なツールだけを動的に発見・ロードすることで、コンテキストウィンドウの使用量を削減します。

### 主な特徴

1. **オンデマンドロード** — 全ツール定義の代わりにコンパクトなリストを送信
2. **BM25キーワードマッチング** — ツール名・説明からの関連性スコアリング
3. **自動アクティベーション** — 閾値ベースの自動有効化

### なぜTool Searchが必要なのか

**出典**: [Tool Search - When to enable Tool Search](https://kiro.dev/docs/cli/mcp/tool-search/#when-to-enable-tool-search)

以下の場合にTool Searchの有効化が推奨されます:

- 5つ以上のMCPサーバーを設定している
- 長い会話中にコンテキストウィンドウオーバーフローエラーが発生する
- `/tools`コマンドでMCPツールが合計50,000トークン以上を消費している

少数のMCPツールのみ使用している場合、Tool Searchのオーバーヘッドは見合わない場合があります。

> Tool Search requires at least one MCP server to be configured. It has no effect if you only use built-in tools.

**公式Changelog原文**:
> Tool Search loads MCP tools on demand instead of sending every definition with each request, keeping your context window clear when you have many MCP servers configured.

## 📋 目次

- [有効化方法](#有効化方法)
- [設定](#設定)
- [動作の仕組み](#動作の仕組み)
- [tool_searchツール](#tool_searchツール)
- [キーワードマッチング](#キーワードマッチング)
- [関連リンク](#関連リンク)

---

## 有効化方法

**出典**: [Tool Search - Enabling Tool Search](https://kiro.dev/docs/cli/mcp/tool-search/#enabling-tool-search)

Tool Searchはデフォルトで無効です。設定で有効化します:

```bash
kiro-cli settings toolSearch.enabled true
```

有効化すると、MCPツールスペックが十分に大きい場合に自動的にアクティベートされます。デフォルトの閾値（コンテキストウィンドウの5%または50,000トークン）はほとんどのケースをカバーします。

MCPツールが存在する場合に常にアクティベートするには、閾値を`0`に設定します:

```bash
kiro-cli settings toolSearch.minPct 0
kiro-cli settings toolSearch.minTokens 0
```

### Tool Searchがアクティブであることの確認

Tool Searchがアクティブな場合:
- `/tools`コマンドで、無効時と比較してMCPツールのトークン数が減少して表示される
- エージェントのツール使用に`tool_search`呼び出しが表示される

---

## 設定

**出典**: [Tool Search - Settings](https://kiro.dev/docs/cli/mcp/tool-search/#settings)

| 設定 | デフォルト | 説明 |
|------|----------|------|
| `toolSearch.enabled` | `false` | Tool Searchのマスタートグル |
| `toolSearch.minPct` | `5` | MCPツールスペックがコンテキストウィンドウのこの%を超えた場合にアクティベート |
| `toolSearch.minTokens` | `50000` | MCPツールスペックがこのトークン数を超えた場合にアクティベート |

両方の閾値が設定されている場合、いずれかが超過するとTool Searchがアクティベートされます（OR論理）。両方の閾値を`0`に設定すると、MCPツール数に関係なく常にアクティブになります。

---

## 動作の仕組み

**出典**: [Tool Search - How it works](https://kiro.dev/docs/cli/mcp/tool-search/#how-it-works)

Tool Searchは以下の4ステップで動作します:

```
Tool Search動作フロー:

1. 索引化          MCPサーバー接続時に全ツールスペックをキーワード検索用に索引化
                   （ツール名、サーバー名、説明、パラメータ説明をトークン化）
      ↓
2. コンパクトリスト  フルJSONスキーマの代わりに
                   「server_name::tool_name: description」形式のコンパクトリストを送信
                   （説明は1KBに切り詰め）
      ↓
3. オンデマンドロード モデルがツールを必要とする時、tool_searchを呼び出し
                   （tool_idで正確指定、またはqueryでキーワード検索）
      ↓
4. アクティベーション マッチしたツールがロードされ、
                   以降のリクエストにフルスキーマが含まれる
```

### 各ステップの詳細

1. **索引化**: MCPサーバー接続時に、全ツールスペックがキーワード検索用に索引化される。各ツールの名前、サーバー名、説明、パラメータ説明がトークン化される
2. **コンパクトリスト**: フルJSONスキーマの代わりに、`server_name::tool_name: description`形式のコンパクトリストがモデルに送信される。説明は1KBに切り詰められる
3. **オンデマンドロード**: モデルがツールを必要とする時、`tool_search`を`tool_id`（例: `builder-mcp::InternalSearch`）または`query`（例: `"search documents"`）で呼び出す
4. **アクティベーション**: マッチしたツールがロードされ、以降のリクエストにフルスキーマが含まれる

---

## tool_searchツール

**出典**: [Tool Search - The tool_search built-in tool](https://kiro.dev/docs/cli/mcp/tool-search/#the-tool_search-built-in-tool)

**ツール名**: `tool_search`

MCPツールをオンデマンドで発見・ロードする組み込みツールです。読み取り専用のため、ユーザー権限プロンプトなしで自動的に許可されます。

### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `tool_id` | string | `tool_id`または`query`のいずれか | `server_name::tool_name`形式の正確なツール識別子 |
| `query` | string | `tool_id`または`query`のいずれか | マッチするツールを検索するキーワード |
| `max_results` | integer | いいえ | 返す最大結果数（デフォルト: 5） |

`tool_id`と`query`のいずれか一方のみを指定します（両方は不可）。マッチしたツールは即座にアクティベートされ、呼び出し可能になります。

---

## キーワードマッチング

**出典**: [Tool Search - Keyword matching](https://kiro.dev/docs/cli/mcp/tool-search/#keyword-matching)

キーワード検索はBM25関連性スコアリングを使用します。ツール名はケーシング境界で分割されます（例: `ReadFile` → `read file`、`read_file` → `read file`）。マッチング閾値を超えた結果のみが返されます。

デフォルトの閾値は`1.5`で、`KIRO_CLI_TOOL_SEARCH_MATCHING_THRESHOLD`環境変数で設定可能です。

---

## 関連リンク

- [Tool Search 公式ドキュメント](https://kiro.dev/docs/cli/mcp/tool-search/)
- [公式Changelog v2.1.0](https://kiro.dev/changelog/cli/2-1/)
- [Built-in tools リファレンス](https://kiro.dev/docs/cli/reference/built-in-tools/)
- [Settings リファレンス](https://kiro.dev/docs/cli/reference/settings/)
- [MCP設定](https://kiro.dev/docs/cli/mcp/configuration/)
- [Terminal UI機能](18_TerminalUI.md)

---

**最終更新**: 2026年05月03日
