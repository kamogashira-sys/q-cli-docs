[ホーム](../README.md) > [機能詳細ガイド](README.md) > Steering（プロジェクト永続知識）

# Kiro CLI Agent Steering機能

**出典**: [Steering - Kiro CLI Documentation](https://kiro.dev/docs/cli/steering/)、[AGENTS.md 標準](https://agents.md/)、[Agent Configuration Reference - resources field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#resources-field)、[公式Changelog v1.20.0](https://kiro.dev/changelog/cli/1-20/)

## 概要

### Agent Steeringとは

Agent Steering は、`.kiro/steering/` 配下に配置した Markdown ファイルを通じて Kiro にプロジェクトの **永続的な知識** を提供する仕組みです。プロジェクトの慣習、ライブラリ、標準を毎回チャットで説明する必要がなくなり、Kiro が一貫してそれらに従うようになります。

Steering Files は **Amazon Q Developer CLI 時代から技術継承** されており、Kiro CLI v1.20.0（本サイト [Changelog v1.20.0](../02_update/01_changelog.md) 参照）で「✅ Steering Files（プロジェクト固有設定）」として明示されています。

### 主な特徴

1. **永続的な文脈** — 毎セッションで自動的にロード
2. **3スコープ** — Workspace（プロジェクト固有）/ Global（ユーザー全体）/ Team（組織配布）
3. **基本3ファイル** — `product.md`（製品）/`tech.md`（技術）/`structure.md`（構造）
4. **AGENTS.md 標準対応** — 60,000+ オープンソースプロジェクトで採用される共通フォーマット
5. **Custom Agents との連携** — `resources` フィールドでステアリングを指定

### なぜ Steering が必要なのか

AI 駆動開発における共通課題：

- 毎回プロジェクトの規約を説明するのは非効率
- チームメンバー全員が同じ前提で AI を使いたい
- 規約が成長する中で、変更を体系的に管理したい
- API のレスポンス形式やテストパターンなど、暗黙知を形式知化したい

Agent Steering は、これらの課題を **コミット可能な Markdown ファイル** として解決します。Steering ファイル自体がプロジェクトの一部となり、変更履歴も追跡できます。

**公式ドキュメント原文**:

> Steering gives Kiro persistent knowledge about your project through markdown files in `.kiro/steering/`. Instead of explaining your conventions in every chat, steering files ensure Kiro consistently follows your established patterns, libraries, and standards.

---

## 📋 目次

- [Steeringの基本コンセプト](#steeringの基本コンセプト)
- [主なメリット](#主なメリット)
- [Steering File スコープ（3種類）](#steering-file-スコープ3種類)
- [Foundational Steering Files](#foundational-steering-files)
- [カスタムSteering Filesの作成](#カスタムsteering-filesの作成)
- [Custom Agents との併用](#custom-agents-との併用)
- [AGENTS.md 標準対応](#agentsmd-標準対応)
- [ベストプラクティス](#ベストプラクティス)
- [Common Steering File Strategies](#common-steering-file-strategies)
- [ユースケース](#ユースケース)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## Steeringの基本コンセプト

**出典**: [Steering - What is steering?](https://kiro.dev/docs/cli/steering/#what-is-steering)

Steering の中核は、`.kiro/steering/` 配下に配置した Markdown ファイルが、エージェント起動時に **自動的に文脈に取り込まれる** という仕組みです。

```
<workspace>/
├── .kiro/
│   └── steering/
│       ├── product.md          # 製品定義
│       ├── tech.md             # 技術スタック
│       ├── structure.md        # プロジェクト構造
│       ├── api-standards.md    # API 規約
│       └── testing-standards.md # テスト方針
├── src/
└── ...
```

これらのファイルが「プロジェクトの取扱説明書」として機能し、Kiro はチャットを開始する前にこれらを読み込みます。

---

## 主なメリット

**出典**: [Steering - Key benefits](https://kiro.dev/docs/cli/steering/#key-benefits)

### 1. 一貫したコード生成（Consistent Code Generation）

すべてのコンポーネント、API エンドポイント、テストがチームの確立されたパターンと規約に従います。

### 2. 反復削減（Reduced Repetition）

各会話でプロジェクト標準を説明する必要がありません。Kiro が好みを記憶しています。

### 3. チーム整合（Team Alignment）

新規メンバーもベテランも、全員が同じ標準で作業します。オンボーディングが大幅に効率化されます。

### 4. 拡張性（Scalable Project Knowledge）

コードベースとともに成長するドキュメント。プロジェクトが進化するにつれて、決定事項とパターンを蓄積できます。

---

## Steering File スコープ（3種類）

**出典**: [Steering - Steering file scope](https://kiro.dev/docs/cli/steering/#steering-file-scope)

Steering File は3つのスコープで運用できます。

### 1. Workspace Steering（プロジェクト固有）

**配置**: `<workspace>/.kiro/steering/`

そのワークスペースでのみ有効。プロジェクト固有のパターン、ライブラリ、標準を Kiro に伝えます。

**典型的な用途**:
- プロジェクト固有のコンポーネント命名規則
- プロジェクトで使用するフレームワークやライブラリの方針
- このコードベース特有のアーキテクチャ決定

### 2. Global Steering（ユーザー全体）

**配置**: `~/.kiro/steering/`

すべてのワークスペースで有効。**全プロジェクトに共通する規約** を Kiro に伝えます。

**典型的な用途**:
- 個人的なコーディングスタイル
- 全プロジェクト共通の言語設定
- 普遍的な品質基準

> **競合時の優先順位**: Workspace Steering > Global Steering。プロジェクト固有の指示が、グローバルな指示を上書きします。これにより、グローバルで一般的な指示を定義しつつ、特定プロジェクトでオーバーライドできる柔軟性が確保されます。

### 3. Team Steering（組織配布）

**配置**: `~/.kiro/steering/`（Global と同じ場所、配布方法が異なる）

組織全体で共有するための運用形態：

- **MDM ソリューション** や **グループポリシー** で各メンバーの PC に Steering ファイルを配布
- 中央リポジトリから各メンバーが手動でダウンロード
- 配布された Steering ファイルは `~/.kiro/steering/` フォルダに配置

これにより、組織標準を全メンバーに浸透させられます。

---

## Foundational Steering Files

**出典**: [Steering - Foundational steering files](https://kiro.dev/docs/cli/steering/#foundational-steering-files)

公式が推奨する **基本3ファイル** は、プロジェクトの基本文脈を確立します。

### セットアップ手順

1. プロジェクトルートに `.kiro/steering/` フォルダを作成（Workspace スコープ）  
   または `~/.kiro/steering` フォルダを作成（Global スコープ）
2. 基本3ファイルを Markdown で配置
3. Kiro が自動的にチャットセッションでロード

### 基本3ファイルの役割

#### `product.md` — Product Overview（製品概要）

製品の目的、ターゲットユーザー、主要機能、ビジネス目標を定義します。Kiro が技術判断の **「なぜ」** を理解し、製品ゴールに沿った提案ができるようになります。

**記載例**:

```markdown
# Product Overview

## 製品名と概要
[製品名] は [対象ユーザー] 向けの [カテゴリ] です。

## ターゲットユーザー
- [ユーザーセグメント1]
- [ユーザーセグメント2]

## 主要機能
1. [機能1]
2. [機能2]

## ビジネス目標
- [目標1]
- [目標2]
```

#### `tech.md` — Technology Stack（技術スタック）

採用フレームワーク、ライブラリ、開発ツール、技術的制約を文書化します。Kiro が実装を提案する際、確立されたスタックを優先します。

**記載例**:

```markdown
# Technology Stack

## 言語・フレームワーク
- TypeScript 5.x
- React 18.x
- Node.js 20.x

## ライブラリ
- 状態管理: Zustand
- フォーム: react-hook-form + zod
- テスト: vitest + Testing Library

## 制約
- IE サポートなし
- 最低 macOS 12.0 / Windows 10
```

#### `structure.md` — Project Structure（プロジェクト構造）

ファイル組織、命名規則、import パターン、アーキテクチャ決定を概説します。生成されるコードが既存コードベースに違和感なく溶け込みます。

**記載例**:

```markdown
# Project Structure

## ディレクトリ構成
src/
├── components/   # UI コンポーネント（PascalCase）
├── hooks/        # カスタムフック（use*.ts）
├── lib/          # ユーティリティ
└── pages/        # ルート単位のエントリ

## 命名規則
- コンポーネント: PascalCase
- フック: useXxx
- ユーティリティ: camelCase

## Import 順
1. 外部ライブラリ
2. 内部 alias（@/）
3. 相対パス
```

> **重要**: これらの基本ファイルは **デフォルトで毎回のインタラクションに含まれ**、Kiro のプロジェクト理解の基盤となります。

---

## カスタムSteering Filesの作成

**出典**: [Steering - Creating custom steering files](https://kiro.dev/docs/cli/steering/#creating-custom-steering-files)

プロジェクト独自のニーズに合わせ、専門的なガイダンスを追加できます。

### 手順

1. `.kiro/steering/` に新しい `.md` ファイルを作成
2. 内容を表す名前を付ける（例: `api-standards.md`）
3. 標準 Markdown 構文でガイダンスを記述
4. 自然言語で要件を記述

### 拡張例

```
.kiro/steering/
├── product.md
├── tech.md
├── structure.md
├── api-rest-conventions.md       # REST API 規約
├── testing-unit-patterns.md      # ユニットテスト方針
├── components-form-validation.md  # フォームコンポーネント標準
└── deployment-workflow.md        # デプロイ手順
```

---

## Custom Agents との併用

**出典**: [Steering - Steering with custom agents](https://kiro.dev/docs/cli/steering/#steering-with-custom-agents)、[Agent Configuration Reference - resources field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#resources-field)

> **⚠️ 重要な挙動の差**:
> - **デフォルトエージェント**: Steering ファイルは **自動的に** 含まれる
> - **カスタムエージェント**: Steering ファイルは **自動的に含まれない**。`resources` フィールドで明示的に指定する必要がある

### resources での指定方法

カスタムエージェントですべての Steering ファイルを含めるには、`agent.json` に以下を追加します：

```json
{
  "name": "my-custom-agent",
  "description": "プロジェクト規約準拠のカスタムエージェント",
  "resources": [
    "file://.kiro/steering/**/*.md"
  ]
}
```

このグロブパターンにより、Steering ディレクトリ配下のすべての Markdown ファイルがロードされます。

### resources フィールドで指定可能な値

`resources` フィールドは複数の URI スキームをサポートします：

| スキーム | 用途 | 例 |
|--------|------|-----|
| `file://` | ファイルを起動時にロード | `"file://.kiro/steering/**/*.md"` |
| `skill://` | Skill のメタデータを起動時、本文をオンデマンドロード | `"skill://.kiro/skills/**/SKILL.md"` |
| Knowledge base オブジェクト | 大規模ドキュメントを検索ベースで参照 | 下記参照 |

**Knowledge base 形式の例**:

```json
{
  "resources": [
    "file://.kiro/steering/**/*.md",
    {
      "type": "knowledgeBase",
      "source": "file://./docs",
      "name": "ProjectDocs",
      "description": "プロジェクトドキュメント全般",
      "indexType": "best",
      "autoUpdate": true
    }
  ]
}
```

詳細は [Agent Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference) を参照してください。

---

## AGENTS.md 標準対応

**出典**: [Steering - AGENTS.md](https://kiro.dev/docs/cli/steering/#agentsmd)、[https://agents.md/](https://agents.md/)

Kiro は **AGENTS.md** 標準による Steering 指示の提供をサポートしています。

### AGENTS.md とは

AGENTS.md は AI コーディングエージェント向けの **オープンな標準フォーマット** です：

- **採用規模**: 60,000+ オープンソースプロジェクト
- **管理団体**: Linux Foundation 配下の Agentic AI Foundation
- **互換ツール**: OpenAI Codex / Google Jules / Factory / Aider / goose / opencode / Zed / Warp / VS Code / Devin / Junie / Amp / Cursor / RooCode / Gemini CLI / Kilo Code / Phoenix / Semgrep / GitHub Copilot / Ona / Windsurf / Augment Code 等25種以上

### AGENTS.md の配置

| 配置場所 | 効果 |
|---------|------|
| `~/.kiro/steering/AGENTS.md` | グローバル（全ワークスペース） |
| `<workspace>/AGENTS.md` | ワークスペースルート |
| サブディレクトリ内の `AGENTS.md` | ネスト対応（モノレポでは subproject ごとに配置可） |

> **重要な挙動差**:
> - **Steering ファイル**（`.kiro/steering/*.md`）: Custom Agents では `resources` で明示指定が必要
> - **AGENTS.md**: **常に含まれる**（明示指定不要）

### ネスト対応

モノレポなど複雑な構造では、各 subproject に AGENTS.md を配置できます。Kiro は **最も近接するファイルを優先** して読み込みます。

```
my-monorepo/
├── AGENTS.md                  # ルート規約
├── packages/
│   ├── frontend/
│   │   ├── AGENTS.md          # frontend 専用規約（ルートより優先）
│   │   └── src/
│   └── backend/
│       ├── AGENTS.md          # backend 専用規約
│       └── src/
```

### 推奨セクション（AGENTS.md 標準）

公式の `agents.md` で推奨されるセクション：

- **Setup commands** — 初期セットアップ手順
- **Code style** — コーディング規約
- **Testing instructions** — テスト方針
- **PR instructions** — プルリクエスト規約

---

## ベストプラクティス

**出典**: [Steering - Best practices](https://kiro.dev/docs/cli/steering/#best-practices)

### 1. ファイルを焦点に絞る（Keep Files Focused）

1ドメイン1ファイル — API 設計、テスト、デプロイ手順それぞれを別ファイルに。

### 2. 明確な命名（Use Clear Names）

| 推奨例 | 内容 |
|------|------|
| `api-rest-conventions.md` | REST API 標準 |
| `testing-unit-patterns.md` | ユニットテストアプローチ |
| `components-form-validation.md` | フォームコンポーネント標準 |

### 3. 文脈を含める（Include Context）

「何が標準か」だけでなく、**「なぜその決定がされたか」** を説明します。

### 4. 例を提供する（Provide Examples）

コードスニペットや before/after 比較で、標準を実証します。

### 5. セキュリティ第一（Security First）

**API キー、パスワード、機密データを含めない**。Steering ファイルはコードベースの一部です（git にコミットされる）。

### 6. 定期的に保守（Maintain Regularly）

- スプリントプランニングやアーキテクチャ変更時にレビュー
- 再構成後にファイル参照をテスト
- Steering の変更を **コード変更と同等に扱い**、レビューを必須化

---

## Common Steering File Strategies

**出典**: [Steering - Common steering file strategies](https://kiro.dev/docs/cli/steering/#common-steering-file-strategies)

公式が示す典型的な Steering ファイルパターン。

### 1. API Standards（`api-standards.md`）

REST 規約、エラーレスポンス形式、認証フロー、バージョニング戦略を定義。エンドポイント命名パターン、HTTP ステータスコードの使い方、リクエスト/レスポンス例を含めます。

### 2. Testing Approach（`testing-standards.md`）

ユニットテストパターン、統合テスト戦略、モックアプローチ、カバレッジ期待値。優先するテストライブラリ、アサーションスタイル、テストファイル組織を文書化します。

### 3. Code Style（`code-conventions.md`）

命名パターン、ファイル組織、import 順序、アーキテクチャ決定。優先するコード構造、コンポーネントパターン、避けるべきアンチパターンの例を含めます。

### 4. Security Guidelines（`security-policies.md`）

認証要件、データ検証ルール、入力サニタイゼーション標準、脆弱性予防策。アプリケーション固有のセキュアコーディング実践を文書化します。

### 5. Deployment Process（`deployment-workflow.md`）

ビルド手順、環境設定、デプロイステップ、ロールバック戦略。CI/CD パイプラインの詳細と環境固有要件を含めます。

> カスタム Steering ファイルは `.kiro/steering/` に保存され、すべての Kiro CLI チャットセッションで即座に利用可能になります。

---

## ユースケース

### ユースケース1：チームの規約を共有

**シナリオ**: 新メンバーがクローンしただけで規約に沿った開発ができる

```bash
# プロジェクトルート
mkdir -p .kiro/steering
cat > .kiro/steering/api-standards.md << 'EOF'
# API Standards
- REST: エンドポイントは複数形・kebab-case（`/users`, `/order-items`）
- ステータスコード: 200/201/204/400/401/403/404/409/500 のみ
- エラー形式: `{ "error": { "code": "...", "message": "..." } }`
EOF
git add .kiro/steering/
git commit -m "feat: API 規約 Steering を追加"
```

→ クローン後、即座にチームメンバー全員が同じ API 規約で開発できます。

### ユースケース2：個人スタイルを全プロジェクトに

**シナリオ**: 全ワークスペースで自分の好みの言語・スタイルを適用

```bash
mkdir -p ~/.kiro/steering
cat > ~/.kiro/steering/personal-style.md << 'EOF'
# Personal Coding Style
- 関数コメントは JSDoc 形式
- 変数名: camelCase
- ファイル名: kebab-case.ts
- 早期 return を多用、ネストを浅く保つ
EOF
```

### ユースケース3：モノレポでの subproject 別規約

**シナリオ**: frontend と backend で異なる規約を適用

```
my-monorepo/
├── AGENTS.md                          # 全体規約（共通）
├── packages/
│   ├── frontend/
│   │   └── AGENTS.md                  # React 固有規約
│   └── backend/
│       └── AGENTS.md                  # Node.js API 固有規約
```

→ Kiro は作業中のディレクトリに最も近い AGENTS.md を優先します。

### ユースケース4：エンタープライズ全社展開

**シナリオ**: MDM 経由で組織標準を全エンジニアに配布

```
配布元: 中央リポジトリ
配布先: 各メンバーの ~/.kiro/steering/
配布方法: MDM (Jamf, Intune 等) または グループポリシー
内容: company-coding-standards.md, security-policies.md 等
```

→ 全エンジニアが組織標準を自動適用。プロジェクト固有規約はワークスペース Steering で上書き可能。

### ユースケース5：Custom Agents との連携で専門エージェント

**シナリオ**: 「セキュリティレビュー専用エージェント」をカスタム作成

```json
{
  "name": "security-reviewer",
  "description": "セキュリティ観点でコードレビューするエージェント",
  "prompt": "コードのセキュリティ脆弱性を厳格にレビューする",
  "resources": [
    "file://.kiro/steering/security-policies.md",
    "file://.kiro/steering/api-standards.md"
  ]
}
```

→ デフォルトエージェントとは異なり、特定 Steering のみを文脈に持ったエージェントを起動できます。

---

## トラブルシューティング

### Steering が反映されない

1. **ファイル配置確認**: `.kiro/steering/` または `~/.kiro/steering/` に配置されているか
2. **拡張子確認**: `.md` であるか
3. **エージェント種別確認**: カスタムエージェント使用時は `resources` で明示指定が必要
4. **`/context show`** で現在の文脈を確認（[Conversation Compaction](10_ConversationCompaction.md) 参照）

### Workspace と Global で規約が衝突

優先順位: **Workspace > Global**。Workspace 側で具体的な指示を書くと自動的に上書きされます。

### コンテキストウィンドウが足りない

- Steering ファイルが大きすぎる → ドメインごとに分割
- 全 Steering をデフォルトロードしない → カスタムエージェントで必要なものだけ指定
- 大規模ドキュメントは Knowledge Base 化を検討（[Skills](07_Skills.md) 参照）

### AGENTS.md が読まれない

- 配置場所確認: ワークスペースルート または `~/.kiro/steering/`
- ネスト時はサブディレクトリにも配置可能、最も近いものが優先される
- ファイル名は **大文字小文字を区別** （`AGENTS.md` のみ）

### 機密情報を誤ってコミットしないために

```bash
# .gitignore で個別 Steering ファイルを除外
.kiro/steering/personal-secrets.md

# または Global Steering（~/.kiro/steering/）に配置
mv .kiro/steering/personal-secrets.md ~/.kiro/steering/
```

ただし、**Workspace 内の Steering はチームと共有することが本来の目的** です。機密データは絶対に含めないでください。

---

## 関連リンク

### 関連機能（本サイト）

- [02. Subagents](02_Subagents.md) — カスタムエージェントとの組み合わせ
- [07. Skills](07_Skills.md) — オンデマンドロードによる大規模ドキュメント参照（Steering との使い分け）
- [10. Conversation Compaction](10_ConversationCompaction.md) — Steering を含む文脈の管理
- [22. Hooks](22_Hooks.md) — `agentSpawn` フックでの追加文脈収集

### リファレンス（辞書）

- [04_reference/01_settings.md](../04_reference/01_settings.md) — Steering ディレクトリ関連設定（`KIRO_HOME` 等）
- [04_reference/04_built-in-tools.md](../04_reference/04_built-in-tools.md) — `read` ツール（Steering ファイル読込）と `introspect.progressiveMode` の関係

### バージョン関連

- [Changelog v1.20.0](../02_update/01_changelog.md) — 「✅ Steering Files（プロジェクト固有設定）」記載のバージョン
- [Changelog v1.26.0](../02_update/01_changelog.md) — Skills 自動読み込みとの関係

### 公式情報源

- [Steering - Kiro CLI Documentation](https://kiro.dev/docs/cli/steering/)（公式ページ最終更新: 2026-01-08）
- [Agent Configuration Reference - resources field](https://kiro.dev/docs/cli/custom-agents/configuration-reference#resources-field)
- [Custom Agents - Creating](https://kiro.dev/docs/cli/custom-agents/creating)

### AGENTS.md 標準

- [agents.md - 公式サイト](https://agents.md/) — Linux Foundation 配下のオープン標準
- [AGENTS.md GitHub](https://github.com/openai/agents.md) — 仕様リポジトリ

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-01-08
