# Kiro CLI Granular Tool Trust機能

**出典**: [Managing tool permissions](https://kiro.dev/docs/cli/chat/permissions/)、[公式Changelog v1.27.0](https://kiro.dev/changelog/cli/1-27/)、CLI changelog v1.27.0

## 概要

### Granular Tool Trustとは

Kiro CLI v1.27.0（2026年3月2日リリース）で追加された、ツール使用時の信頼スコープを段階的に制御する機能です。従来の「許可/拒否」の二択から、コマンドやパスの粒度で信頼範囲を選択できるようになりました。

### 主な特徴

1. **Shell Command Trust Levels** — シェルコマンドの信頼を4段階で制御
2. **Read/Write Path Trust Levels** — ファイル操作の信頼を3段階で制御
3. **インタラクティブピッカー** — 信頼スコープを視覚的に選択するUI

### なぜGranular Tool Trustが必要なのか

従来のツール権限管理では、ツール全体を「信頼する」か「毎回確認する」かの二択でした。Granular Tool Trustにより、セキュリティと利便性のバランスを細かく調整できます。

**公式Changelog原文**:
> When Kiro asks to use a tool, you now get an interactive picker to choose how broadly to trust it. For shell commands, select from tiered scopes — trust the exact command, the command with any arguments, or the base command with wildcards. For read and write tools, scope trust to specific file paths, the containing directory, or the entire tool.

## 📋 目次

- [/toolsコマンド](#toolsコマンド)
- [利用可能なツール](#利用可能なツール)
- [Shell Command Trust Levels](#shell-command-trust-levels)
- [Read/Write Path Trust Levels](#readwrite-path-trust-levels)
- [デフォルトの信頼設定と使用例](#デフォルトの信頼設定と使用例)
- [関連リンク](#関連リンク)

---

## /toolsコマンド

**出典**: [Managing tool permissions - Tools commands](https://kiro.dev/docs/cli/chat/permissions/#tools-commands)

`/tools`コマンドでツール権限を管理できます。

| コマンド | 説明 |
|---------|------|
| `help` | ツールに関するヘルプを表示 |
| `trust` | 特定のツールをセッション中信頼する |
| `untrust` | ツールをリクエストごとの確認に戻す |
| `trust-all` | 全ツールを信頼（非推奨の`/acceptall`と同等） |
| `reset` | シェル信頼パターン、ファイルシステムパス、拒否ツールを含む全ランタイム権限をデフォルトにリセット |

ツール権限には2つの状態があります:
- **Trusted**: Kiroが確認なしでツールを使用可能
- **Per-request**: Kiroが使用前に毎回確認を求める

```bash
# 特定のツールを信頼
Kiro> /tools trust read

# 特定のツールの信頼を解除
Kiro> /tools untrust shell
```

> **注意**: Terminal UIでは、`--trust-all-tools`と`/tools trust-all`は確認警告を表示し、リスクを承認してから有効になります。

---

## 利用可能なツール

**出典**: [Managing tool permissions - Available tools](https://kiro.dev/docs/cli/chat/permissions/#available-tools)

Kiro CLIに組み込まれているツール:

| ツール | 説明 |
|--------|------|
| `read` | システム上のファイルとディレクトリを読み取り |
| `write` | システム上のファイルを作成・変更 |
| `shell` | システム上でbashコマンドを実行 |
| `aws` | AWS CLIを呼び出してAWSサービスと連携 |
| `report` | ブラウザを開いてチャットの問題をAWSに報告 |

明示的な権限がないツールをKiroが使用しようとすると、承認を求めるパネルが表示されます。複数のツールが同時に権限を必要とする場合、承認はキューに入り1つずつ表示されます。

---

## Shell Command Trust Levels

**出典**: [Managing tool permissions - Shell command trust levels](https://kiro.dev/docs/cli/chat/permissions/#shell-command-trust-levels)

Kiroがシェルコマンドを実行しようとすると、信頼範囲を選択するインタラクティブピッカーが表示されます。

### インタラクティブピッカーUI

例えば`git pull --rebase`を実行する場合:

```
Press (↑↓) to navigate (⏎) to select scope
> Full command          → git pull --rebase
  Partial command       → git pull *
  Base command          → git *
  Entire Tool           → *
```

### 4段階の信頼レベル

```
Shell Trust Levels（制限的 → 緩い）:

  Full command    → git pull --rebase  （完全一致のみ）
  Partial command → git pull *         （サブコマンド固定、引数は任意）
  Base command    → git *              （ベースコマンド固定、以降は任意）
  Entire Tool     → *                  （全シェルコマンド許可）
```

| レベル | 信頼する範囲 | パターン例 |
|--------|------------|-----------|
| Full command | 記述された通りの完全なコマンド | `git pull --rebase` |
| Partial command | コマンドとサブコマンド、引数は任意 | `git pull *` |
| Base command | ベースコマンド、引数は任意 | `git *` |
| Entire Tool | 全シェルコマンド | `*` |

### 動作の詳細

- レベル選択後、信頼されたパターンが確認表示される（例: `✓ Trusted: git pull --rebase`）
- コマンドにサブコマンドがない場合、Partialレベルはスキップされる
- チェーンコマンド（パイプ、`&&`）の場合、各コマンドの信頼パターンが生成され重複排除される
- 信頼パターンはセッション中持続し、エージェントの`allowedCommands`設定に正規表現として保存される

> **注意**: コマンドが`deniedCommands`パターンに一致する場合、段階的信頼オプションは利用できません。1回限りの許可またはツール全体の信頼のみ選択可能です。

---

## Read/Write Path Trust Levels

**出典**: [Managing tool permissions - Read and write path trust levels](https://kiro.dev/docs/cli/chat/permissions/#read-and-write-path-trust-levels)

`read`と`write`ツールも、カレントワーキングディレクトリ外のパスにアクセスする際に段階的信頼をサポートします。

### デフォルト動作

- `read`と`write`はカレントワーキングディレクトリに対してデフォルトで信頼されている
- カレントワーキングディレクトリ外のファイルにアクセスする場合にピッカーが表示される

### インタラクティブピッカーUI

```
Press (↑↓) to navigate (⏎) to select scope
> Specific paths       → ~/.config/app/settings.json
  Complete directory   → ~/.config/app
  Entire Tool          → *
```

### 3段階の信頼レベル

```
Read/Write Trust Levels（制限的 → 緩い）:

  Specific paths     → ~/.config/app/settings.json  （ファイル単位）
  Complete directory  → ~/.config/app               （ディレクトリ単位）
  Entire Tool         → *                           （全パス許可）
```

| レベル | 信頼する範囲 | 例 |
|--------|------------|-----|
| Specific paths | リクエストされた正確なファイルパスのみ | `~/.config/app/settings.json` |
| Complete directory | 含まれるディレクトリ内の全ファイル | `~/.config/app` |
| Entire Tool | 全ての読み取り/書き込み操作 | `*` |

---

## デフォルトの信頼設定と使用例

**出典**: [Managing tool permissions - Default trust and permission examples](https://kiro.dev/docs/cli/chat/permissions/#default-trust-and-permission-examples)

各ツールにはデフォルトの信頼動作があります。`read`はカレントワーキングディレクトリに対してデフォルトで信頼されています。

### 使用シーン別の推奨設定

公式docに記載されている使用例:

| シーン | 推奨設定 |
|--------|---------|
| コードベースの探索時 | `read`を信頼 — 確認なしでファイルを読み取り |
| プロジェクトで積極的に作業中 | `write`を信頼 — ファイルの作成・変更を許可 |
| 機密環境での作業時 | `shell`を信頼解除 — 全コマンドを実行前にレビュー |
| 本番AWSリソースでの作業時 | `aws`を信頼解除 — 意図しない変更を防止 |

---

## 関連リンク

- [Managing tool permissions 公式ドキュメント](https://kiro.dev/docs/cli/chat/permissions/)
- [公式Changelog v1.27.0](https://kiro.dev/changelog/cli/1-27/)
- [Shell tool settings](https://kiro.dev/docs/cli/reference/built-in-tools/#execute-shell-commands)
- [Chat security](https://kiro.dev/docs/cli/chat/security/)
- [AIによるAWS操作を安全に。Kiro CLIで作るsudo的なIAM権限昇格](https://dev.classmethod.jp/articles/kiro-cli-custom-agent-sudo/) - DevelopersIO記事 by suzuki.ryo（カスタムエージェント + IAMロールによる権限分離の実装例）

---

**最終更新**: 2026年05月03日
