# Kiro CLI v2.0.0 メジャーバージョンアップ解説

**出典**: [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)、[Headless Mode](https://kiro.dev/docs/cli/headless/)、[Terminal UI](https://kiro.dev/docs/cli/terminal-ui/)、CLI changelog v2.0.0/v2.0.1

## 概要

### v2.0.0とは

Kiro CLI v2.0.0（2026年4月13日リリース）は、v1.x系からのメジャーバージョンアップです。プラットフォーム対応の拡大、CI/CD自動化、UIの刷新という3つの柱で構成されています。

### 主な特徴

1. **Windows 11ネイティブ対応** — macOS/Linuxに加えWindows 11で動作
2. **Headless Mode** — CI/CDパイプラインでの非対話実行
3. **Terminal UIデフォルト化** — 実験的UIがデフォルトインターフェースに昇格

### なぜメジャーバージョンアップか

公式Changelog v2.0.0の冒頭で、v2.0.0の位置づけが以下のように説明されています:

> Kiro CLI 2.0 expands platform support to Windows, introduces headless mode for CI/CD automation, graduates the terminal UI from experimental to the default experience, and adds new capabilities across subagents, hooks, and MCP configuration.

v2.0.0がメジャーバージョンアップである理由は、以下の3点が同時に実現されたことにあります:

1. **プラットフォームの拡大**: Windows 11対応により、macOS/Linuxのみだった動作環境が全主要OSに拡大
2. **新しい実行モデルの追加**: Headless Modeにより、対話型のみだった実行モデルにCI/CD向け非対話型が追加
3. **デフォルトUIの変更**: v1.28.0で実験的に導入されたTerminal UIがデフォルトインターフェースに昇格

## 📋 目次

- [Windows Support](#windows-support)
- [Headless Mode](#headless-mode)
- [Terminal UIデフォルト化](#terminal-uiデフォルト化)
- [ベストプラクティス](#ベストプラクティス)
- [制限事項](#制限事項)
- [v2.0.1パッチ](#v201パッチ)
- [関連リンク](#関連リンク)

---

## Windows Support

**出典**: [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)

Kiro CLIがWindows 11でネイティブに動作するようになりました。

**公式Changelog原文**:
> Kiro CLI now runs natively on Windows 11. Windows users can now build using the same agentic coding experience available on macOS and Linux — terminal UI, headless mode, custom agents, and MCP servers all included. Install from PowerShell and background auto-updates keep you current.

### 対応機能

Windows 11環境で以下の全機能が利用可能です:

- Terminal UI
- Headless Mode
- カスタムエージェント
- MCPサーバー

### インストール方法

PowerShellからインストールし、バックグラウンド自動更新により最新バージョンが維持されます。

### プラットフォーム対応の変遷

```
v1.x系    macOS / Linux のみ
            ↓
v2.0.0    macOS / Linux / Windows 11
```

---

## Headless Mode

**出典**: [Headless Mode](https://kiro.dev/docs/cli/headless/)

Headless Modeは、CI/CDパイプライン、自動化スクリプト、ブラウザのない環境でKiro CLIを非対話的に実行する機能です。

### 認証

Headless Modeでは`KIRO_API_KEY`環境変数によるAPIキー認証が必要です。

> API key authentication is only available for Kiro Pro, Pro+, and Power subscribers. If your subscription is managed by an administrator, they need to enable API key generation first.

APIキーはユーザーアカウントに紐づいており、管理者が設定したガバナンスルール（MCPサーバー制限、モデルアクセスポリシー、web fetch権限）はHeadlessセッションにも適用されます。

### 実行方法

`--no-interactive`フラグとプロンプトを指定して実行します:

```bash
kiro-cli chat --no-interactive "your prompt here"
```

ツール使用の承認は対話的に行えないため、`--trust-all-tools`または`--trust-tools`で事前に権限を付与します:

```bash
# 全ツールを信頼
kiro-cli chat --no-interactive --trust-all-tools "Write tests for the auth module and run them"

# 特定のツールカテゴリのみ信頼
kiro-cli chat --no-interactive --trust-tools=read,grep "Find all TODO comments in src/"
```

### Headless Mode実行フロー

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐    ┌──────────┐    ┌───────────┐
│ KIRO_API_KEY │───→│ --no-interactive│───→│ --trust-tools│───→│ プロンプト │───→│ Exit Code │
│ 環境変数設定  │    │ フラグ指定      │    │ 権限付与     │    │ 実行      │    │ 結果判定   │
└──────────────┘    └─────────────────┘    └──────────────┘    └──────────┘    └───────────┘
```

### CI/CD例: GitHub Actions

公式docに記載されているGitHub Actionsの例:

```yaml
name: Kiro Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Kiro CLI
        run: curl -fsSL https://cli.kiro.dev/install | bash
      - name: Review PR changes
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: kiro-cli chat --no-interactive --trust-tools=read,grep "Review the changes in this PR for security issues"
```

### その他のパターン

```bash
# テストの生成と実行
kiro-cli chat --no-interactive --trust-all-tools "Write tests for the auth module and run them"

# ビルドエラーのトラブルシューティング
cat build-error.log | kiro-cli chat --no-interactive "Explain this build failure and suggest a fix"
```

MCPサーバーに依存するパイプラインでは`--require-mcp-startup`を使用して、接続失敗時に即座にエラー終了させることができます。

### フラグ一覧

公式docに記載されているHeadless Mode関連フラグ:

| フラグ | 説明 |
|--------|------|
| `--no-interactive` | 対話セッションなしで実行。引数としてプロンプトが必要 |
| `--trust-all-tools` | 全ツール呼び出しを承認なしで自動許可 |
| `--trust-tools=<categories>` | 特定のツールカテゴリを自動許可（例: `read`, `grep`, `write`） |
| `--require-mcp-startup` | MCPサーバーの接続失敗時に即座にエラー終了 |

---

## Terminal UIデフォルト化

**出典**: [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)

v1.28.0で実験的に導入されたTerminal UIが、v2.0.0でデフォルトのチャットインターフェースになりました。

**公式Changelog原文**:
> The terminal UI is now the default chat interface. It gives you syntax-highlighted markdown, interactive overlay panels, visual tool progress, and a full set of keyboard shortcuts.

### Terminal UIの進化

```
v1.28.0（2026-03-20）  実験的導入（--tuiフラグで有効化）
  ↓
v1.29.x（2026-04）     機能充実（/theme, /guide, /transcript, /copy, /spawn, Ctrl+R等）
  ↓
v2.0.0（2026-04-13）   デフォルト化（Crew Monitor, サブエージェント依存関係）
```

### クラシックインターフェースへの切り替え

Terminal UIがデフォルトですが、クラシックインターフェースにいつでも切り替え可能です:

```bash
# 一時的に切り替え
kiro-cli --classic

# 永続的に切り替え
kiro-cli settings chat.ui "classic"
```

Terminal UIの機能詳細については、[Terminal UI機能](18_TerminalUI.md)を参照してください。

---

## ベストプラクティス

**出典**: [Headless Mode - Best practices](https://kiro.dev/docs/cli/headless/#best-practices)

公式docに記載されているHeadless Modeのベストプラクティス:

- `KIRO_API_KEY`はCI/CDプラットフォームのシークレットとして保存する。パイプライン設定にハードコードしたりソースコントロールにコミットしない
- `--trust-all-tools`の代わりに`--trust-tools`で特定のカテゴリを指定し、最小権限の原則に従う
- パイプラインがMCPサーバーに依存する場合は`--require-mcp-startup`を追加し、ハングではなく即座にエラー終了させる
- より豊富な結果を得るためにコンテキストをプロンプトにパイプする（例: `git diff | kiro-cli chat --no-interactive "Review these changes"`）
- パイプラインでの失敗をグレースフルに処理するためにexit codesを確認する
- APIキーを定期的にローテーションし、使用しなくなったキーは[Kiroポータル](https://app.kiro.dev)で失効させる

---

## 制限事項

**出典**: [Headless Mode - Limitations](https://kiro.dev/docs/cli/headless/#limitations)

公式docに記載されているHeadless Modeの制限事項:

- 引数として初期プロンプトを提供する必要がある
- セッション中のユーザー入力は不可
- 対話型スラッシュコマンド（`/model`ピッカー、`/agent`ピッカー）は利用不可
- Terminal UI機能は無効

---

## v2.0.1パッチ（2026年4月16日）

**出典**: CLI changelog v2.0.1

- `--trust-all-tools`が非対話モードで無視される問題を修正

---

## 関連リンク

- [公式Changelog v2.0.0](https://kiro.dev/changelog/cli/2-0/)
- [Headless Mode 公式ドキュメント](https://kiro.dev/docs/cli/headless/)
- [Terminal UI 公式ドキュメント](https://kiro.dev/docs/cli/terminal-ui/)
- [Authentication 公式ドキュメント](https://kiro.dev/docs/cli/authentication/)
- [Exit Codes](https://kiro.dev/docs/cli/reference/exit-codes/)
- [Terminal UI機能（詳細）](18_TerminalUI.md)
- [Kiro CLI 2.0 のヘッドレスモードを試してみた — API キー認証でエージェントを非対話実行](https://dev.classmethod.jp/articles/kiro-cli-2-0-headless-mode-api-key-auth/) - DevelopersIO記事 by suzuki.ryo（Headless Mode APIキー発行〜基本実行・モデル比較）
- [Kiro CLI の headless モードでコードレビューしてみた](https://zenn.dev/aws_japan/articles/46278a8413f8fd) - Zenn記事 by konippi（Headless Mode実践例）
- [Kiro CLI によるコードレビューを ACP で実現する](https://zenn.dev/aws_japan/articles/91dcdf769e9b10) - Zenn記事 by konippi（ACP活用によるCI/CDコードレビュー）
- [Lambda + IAMロールで Kiro CLI の use_aws ツールを安全に動かしてみた](https://dev.classmethod.jp/articles/kiro-cli-headless-lambda-iam-use-aws/) - DevelopersIO記事 by suzuki.ryo（Headless Mode + Lambda + IAMロールで最小権限実行）

---

**最終更新**: 2026年05月04日
