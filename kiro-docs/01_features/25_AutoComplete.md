[ホーム](../README.md) > [機能詳細ガイド](README.md) > Auto Complete

# 25. Auto Complete（オートコンプリート＆インライン補完）

**出典**: [Completions & autocomplete - Kiro CLI Documentation](https://kiro.dev/docs/cli/autocomplete/)（公式ページ最終更新: 2025-11-16）

## 概要

### Auto Complete とは

**Auto Complete** は、Kiro CLI が提供する **AI 駆動のターミナル支援機能** です。コマンドラインでの作業効率を高めるため、2 種類の独立した支援を提供します：

1. **Autocomplete Dropdown Menu**（ドロップダウンメニュー）: コマンドオプションを表示するグラフィカルなメニュー
2. **Inline Suggestions**（インライン候補）: 入力中に表示される **グレーのゴーストテキスト**

これらは独立して動作し、`git`、`npm`、`docker`、`aws` をはじめ **数百のコマンドラインツール** をサポートします。

### 主な特徴

- ✅ **2 つの独立した支援モード**: ドロップダウン と インライン候補（個別に有効/無効化可能）
- ✅ **数百のコマンドラインツール対応**: 主要開発ツールから言語ツール、システムコマンドまで
- ✅ **テーマ対応**: dark / light / system の 3 種類
- ✅ **インライン補完のカスタマイズ**: ARN 指定によるエンタープライズカスタマイズ対応
- ✅ **シェル横断**: bash / zsh / fish 等で動作

### なぜ Auto Complete が必要なのか

開発者がターミナルで作業する際、コマンドのオプションやサブコマンドの **正確な綴り** を覚えることは認知負荷となります。Auto Complete は：

- ✅ コマンドの **発見性** を高める（メニューで全オプション可視化）
- ✅ 過去の入力パターンから次の入力を **予測** する（インライン候補）
- ✅ タイプミスを減らす
- ✅ 学習コストを下げる（新規ツールでも候補から選ぶだけ）

**公式ドキュメント原文**:
> Kiro CLI provides two AI-powered assistance features to help you work more efficiently in your terminal: Autocomplete Dropdown Menu (A graphical menu showing available command options) and Inline Suggestions (Gray "ghost text" that appears as you type). These features work independently and support hundreds of popular command line tools including `git`, `npm`, `docker`, and `aws`.

---

## 📋 目次

- [Autocomplete Dropdown Menu（ドロップダウンメニュー）](#autocomplete-dropdown-menuドロップダウンメニュー)
- [Inline Suggestions（インライン候補）](#inline-suggestionsインライン候補)
- [サポートツール](#サポートツール)
- [ユースケース](#ユースケース)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## Autocomplete Dropdown Menu（ドロップダウンメニュー）

**出典**: [Autocomplete dropdown menu](https://kiro.dev/docs/cli/autocomplete/#autocomplete-dropdown-menu)

カーソルの右側に表示される **グラフィカルなドロップダウンメニュー** で、利用可能なオプション、サブコマンド、引数を矢印キーで選択できます。

### 使い方

Kiro CLI をインストールすると **自動的に有効化** されます。

1. ターミナル/コマンドプロンプトを開く
2. コマンドの入力を開始
3. グラフィカルメニューが表示され、利用可能なオプションが表示される
4. 矢印キーで候補を移動
5. **Tab** または **Enter** キーで選択

### 設定

#### 有効化／無効化

```bash
# Autocomplete を有効化
kiro-cli settings autocomplete.disable false

# Autocomplete を無効化
kiro-cli settings autocomplete.disable true
```

> **注意**: 設定キー名は `autocomplete.disable`（**disable** に注意）。`true` で **無効化**、`false` で **有効化** です。

#### テーマの変更

```bash
# Dark テーマ
kiro-cli theme dark

# Light テーマ
kiro-cli theme light

# システム設定に追従
kiro-cli theme system

# 現在のテーマを確認
kiro-cli theme

# 利用可能なテーマ一覧
kiro-cli theme --list
```

> v2.4.0 以降は `/settings` スラッシュコマンドからチャット内でも変更可能。詳細は [21. v24 New Commands](21_v24NewCommands.md) 参照。

---

## Inline Suggestions（インライン候補）

**出典**: [Inline suggestions](https://kiro.dev/docs/cli/autocomplete/#inline-suggestions)

入力中のコマンドラインに **グレーのゴーストテキスト** として直接表示される候補。ドロップダウンメニューとは独立に動作します。

### 使い方

デフォルトで有効化されています。

1. コマンドの入力を開始
2. グレーのゴーストテキストが補完候補として表示される
3. **右矢印キー** または **Tab** で候補を採用
4. 入力を続ければ候補は無視される

### Inline 管理コマンド（`kiro-cli inline`）

`kiro-cli inline` サブコマンドで制御します。

```bash
# インライン候補を有効化
kiro-cli inline enable

# インライン候補を無効化
kiro-cli inline disable

# 現在の状態を確認
kiro-cli inline status

# カスタマイズの設定（ARN 指定）
kiro-cli inline set-customization [ARN]

# 利用可能なカスタマイズを表示
kiro-cli inline show-customizations
```

#### カスタマイズ（エンタープライズ機能）

`set-customization [ARN]` は、Amazon Q Developer のカスタマイズ機能を継承したもので、企業内コードベースに合わせて補完を最適化します。

- **対象**: Pro / Enterprise プラン契約者
- **ARN 形式**: AWS リソースの Amazon Resource Name
- **使用例**:
  ```bash
  kiro-cli inline show-customizations
  # 利用可能なカスタマイズが表示される
  
  kiro-cli inline set-customization arn:aws:codewhisperer:us-east-1:123456789012:customization/...
  ```

→ 詳細は [03_cli-commands](../04_reference/03_cli-commands.md) の `kiro-cli inline` 節参照。

---

## サポートツール

**出典**: [Supported tools](https://kiro.dev/docs/cli/autocomplete/#supported-tools)

オートコンプリートシステムは **数百のコマンドラインツール** をサポートします。

### 人気ツール

| ツール | 補完される対象 |
|------|------------|
| **Git** | ブランチ名、コミットハッシュ、ファイルパス |
| **Docker** | コンテナ名、イメージタグ、コマンド |
| **npm / yarn** | パッケージ名、scripts、依存関係 |
| **kubectl** | リソース、namespace、context |
| **terraform** | リソース、provider、変数 |
| **aws** | サービス、リージョン、リソース名 |

### 言語ツール

| 言語 | パッケージマネージャ |
|-----|--------------|
| **Python** | `pip`、`poetry`、`conda` |
| **Node.js** | `npm`、`yarn`、`pnpm` |
| **Ruby** | `gem`、`bundle` |
| **Go** | `go mod`、`go build` |

### システムツール

- 標準 Unix/Linux コマンド
- パッケージマネージャ（`apt`、`brew`、`yum`）
- ファイル操作（`ls`、`find`、`grep`）

> **注**: 公式ページに「数百のツールをサポート」と記載されているのみで、完全なリストは公開されていません。日々追加が行われている可能性があります。

---

## ユースケース

### ユースケース 1: 新しいツールの学習を促進

新規 CLI ツール（例: `kubectl`、`terraform`）を導入した直後、サブコマンド構造を覚える前にドロップダウンから選択するだけで使い始められます。

**例**: `kubectl get ` まで打つとリソース種別（pod / service / deployment...）が候補表示。

### ユースケース 2: Git 操作の効率化

ブランチ名、コミットハッシュ、ファイルパス補完により、長い識別子のタイプミスを防ぎます。

**例**:
```bash
git checkout feature/u  # → feature/user-profile-redesign が候補表示
git diff a3f8b2  # → a3f8b2c4d... ハッシュが補完
```

### ユースケース 3: AWS 作業の高速化

リージョン名、サービス名、リソース名の補完により、AWS CLI の冗長な入力が短縮されます。

**例**:
```bash
aws s3 cp ./file.txt s3://my-b  # → s3://my-bucket-prod/ が候補
aws ec2 describe-instances --region eu-c  # → eu-central-1 が候補
```

### ユースケース 4: パッケージマネージャの履歴活用

`npm install` 後、過去のインストール履歴から候補が表示され、再インストールが容易に。

**例**:
```bash
npm install rea  # → react、react-dom、react-router-dom が候補
```

### ユースケース 5: エンタープライズカスタマイズで内部ライブラリ補完

`kiro-cli inline set-customization [ARN]` で社内 SDK・内部 API の補完を有効化。

**例**: 社内ライブラリ `@mycompany/auth-sdk` のメソッド名がタイプ中に補完される。

---

## トラブルシューティング

**出典**: [Troubleshooting](https://kiro.dev/docs/cli/autocomplete/#troubleshooting)

### 1. オートコンプリートが表示されない

| チェック | コマンド |
|--------|--------|
| インストール確認 | `kiro-cli --version` |
| 無効化されていないか | `kiro-cli settings autocomplete.disable` |
| ターミナル再起動 | （該当ターミナルで再起動） |
| シェル切替 | bash / zsh / fish のいずれかで再試行 |

### 2. インライン候補が動作しない

| チェック | コマンド |
|--------|--------|
| 状態確認 | `kiro-cli inline status` |
| 有効化 | `kiro-cli inline enable` |
| シェル互換性確認 | bash / zsh / fish で再試行 |
| ターミナルエミュレータ | iTerm2 / Alacritty / Wezterm 等の対応確認 |

### 3. テーマが反映されない

```bash
# 現在のテーマを確認
kiro-cli theme

# システムテーマに追従させる
kiro-cli theme system

# ターミナルの背景色設定とコンフリクトしていないか確認
```

### 4. カスタマイズ ARN が見つからない

```bash
# 利用可能なカスタマイズを表示
kiro-cli inline show-customizations

# 表示されない場合は、組織管理者にカスタマイズ ARN を問い合わせ
# Pro / Enterprise プラン契約が必要
```

---

## 関連リンク

### 関連機能（本サイト）

- [16. v2 Major Update](16_v2MajorUpdate.md) — v2.0 の Terminal UI 大改修
- [18. Terminal UI](18_TerminalUI.md) — V2 TUI とテーマ
- [21. v24 New Commands](21_v24NewCommands.md) — `/theme` `/settings` スラッシュコマンド

### リファレンス（辞書）

- [04_reference/01_settings.md](../04_reference/01_settings.md) — `autocomplete.disable` 設定の正規仕様
- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `kiro-cli inline`、`kiro-cli theme` コマンドの正規仕様（`enable`/`disable`/`status`/`set-customization`/`show-customizations`）

### バージョン関連

- [02_update/01_changelog.md](../02_update/01_changelog.md) — Kiro CLI バージョン履歴
  - v2.0.0（2026-04-13）: Terminal UI 大改修と Theme サポート
  - v2.4.0（2026-05-20）: `/settings` メニューにテーマ統合

### 公式情報源

- [Completions & autocomplete - Kiro CLI Documentation](https://kiro.dev/docs/cli/autocomplete/)（公式ページ最終更新: 2025-11-16）
- [Hooks - Kiro CLI Documentation](https://kiro.dev/docs/cli/hooks/) — 関連機能
- [Code Intelligence - Kiro CLI Documentation](https://kiro.dev/docs/cli/code-intelligence/) — 関連機能

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2025-11-16
