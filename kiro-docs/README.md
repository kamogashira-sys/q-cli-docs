# 猫でもわかるkiro-cli アップデート情報

## 📢 はじめに

このドキュメントでは、Kiro CLI（旧Amazon Q Developer CLI）の主要機能アップデートについて詳しく解説します。Amazon Q Developer CLIからKiro CLIへの移行に伴い、多くの革新的な機能が追加されました。

## 概要

Kiro CLI（旧Amazon Q Developer CLI）の最新情報とアップデートを追跡・整理するプロジェクトです。

## 情報源

- **公式サイト**: https://kiro.dev/cli/
- **GitHub**: https://github.com/kirodotdev/Kiro
- **移行情報**: Amazon Q Developer CLI v1.19.7（2025-11-17）から移行
- **AWSジャパンContributor(小西さん)**: https://zenn.dev/konippi
- **Classmethod(鈴木さん)**: https://dev.classmethod.jp/author/suzuki-ryo/
- **AWS Serverless Hero(吉田さん)**: https://yoshidashingo.com/

## ディレクトリ構成

```
kiro-docs/
├── 00_information/   # 基本情報・公式サイト情報
├── 01_features/      # 機能詳細ガイド（26機能）
├── 02_update/        # アップデート情報
├── 03_deployment/    # デプロイメント・環境構築
├── 04_reference/     # リファレンス（Settings/Slash/CLI/Tools）
└── 07_aidlc/         # AI-DLC（Kiro CLI で実践する選択肢）🆕
```

**クイックリンク**: [00_information/](00_information/) | [01_features/](01_features/) | [02_update/](02_update/) | [03_deployment/](03_deployment/) | [04_reference/](04_reference/) | [07_aidlc/](07_aidlc/) 🆕

## 📚 主要ドキュメント

### [00_information/ - 基本情報・公式サイト情報](00_information/README.md)
Kiro CLI の基本情報と公式サイトの構造について説明したドキュメント集です。

- **[公式サイト構造](00_information/01_official-site-structure.md)** - Kiro CLI公式サイトの画面遷移とページ構成

### [01_features/ - 機能詳細ガイド](01_features/README.md)
Kiro CLIの主要機能（**26 機能**）について詳細に解説したドキュメント集です。

📖 **[→ 機能一覧（カテゴリ別ナビゲーション・各機能の概要・バージョン情報）](01_features/README.md)**

カテゴリ：🤖 エージェント・自動化 / 📁 コンテキスト・知識管理 / 📂 ファイル操作・編集 / 🧠 コード理解・LSP / 💾 セッション・履歴管理 / 🎨 UI/UX・補完 / 🔒 セキュリティ・権限 / 🔌 統合（IDE/MCP/CI/CD/認証） / 💰 使用量・課金

### [02_update/ - アップデート情報](02_update/README.md)
Kiro CLIのバージョン履歴とアップデート情報を管理しています。

- **[変更履歴](02_update/01_changelog.md)** - 全バージョンの詳細な変更内容

### [03_deployment/ - デプロイメント・環境構築](03_deployment/README.md)
Kiro CLI の環境構築とデプロイメントに関するガイド集です。

- **[公式インストール手順](03_deployment/03_official-installation.md)** 🆕 - 公式 OS 別インストール（macOS/Windows 11/Linux/Ubuntu/Proxy/デバッグ）
- **[AWS Samples Code Server](03_deployment/01_aws-samples-code-server.md)** - EC2上でのKiro CLI開発環境構築

### [04_reference/ - リファレンス](04_reference/README.md) 🆕
Kiro CLI の設定・コマンド・ツールの **辞書的リファレンス**（公式ページ準拠）。

| ファイル | 内容 |
|--------|------|
| [01. Settings](04_reference/01_settings.md) | 全設定項目（公式8カテゴリ）と環境変数 |
| [02. Slash Commands](04_reference/02_slash-commands.md) | 全スラッシュコマンド36種＋キーボードショートカット |
| [03. CLI Commands](04_reference/03_cli-commands.md) | `kiro-cli` コマンド全16種、グローバル引数、セッション管理 |
| [04. Built-in Tools](04_reference/04_built-in-tools.md) | 組み込みツール18種（read/glob/grep/write/shell/aws/web_*/code/tool_search/subagent 他） |

---

## 🌟 注目の新機能：Agent Toolkit for AWS（2026-05 GA）

> **AWS が公式に発表した、AI コーディングエージェントが AWS で安全・効果的に動作するためのツールキット。**
>
> 公式が対応エージェントとして明示しているのは：**Claude Code / Cursor / Codex / Kiro / Windsurf / Cline**（[User Guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html#what-can-i-do-agent-toolkit) より）。さらに [AWS News Blog（2026-05-06）](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available) では **「Kiro CLI、Kiro」** が両方明記されています。

### 📖 詳細ガイド: **[26. Agent Toolkit for AWS（AWS 公式エージェント統合ツールキット）](01_features/26_AgentToolkitForAWS.md)** ⭐

**Agent Toolkit for AWS** は、AI コーディングエージェントが AWS サービス上で **本番グレード** の作業を行うための公式ツールキットです。本サイト（Kiro CLI 専門）では **Kiro CLI からの利用** を主眼に解説します。設定ディレクトリ `~/.kiro/` は Kiro（IDE）と Kiro CLI で共通のため、設定方法も共通です。

### 🎯 主な提供価値

| 価値 | 内容 |
|------|------|
| 🔐 **エンタープライズグレードのセキュリティ** | IAM コンテキストキー（`aws:CalledViaAWSMCP`）でエージェント／人間アクションを区別、SCP / IAM ポリシーで権限分離 |
| 📊 **完全な可観測性** | CloudWatch メトリクス（`AWS-MCP` namespace）+ CloudTrail 監査ログ |
| 📚 **リアルタイム公式ドキュメント** | モデルの学習カットオフ後の新サービス（S3 Vectors / Aurora DSQL / Bedrock AgentCore 等）にも即対応 |
| 🛡️ **サンドボックス Python 実行** | `run_script` でファイルシステム・ネットワークなしの安全な分析・操作 |
| 🆓 **追加料金なし** | AWS リソース利用料のみ |

### ⚡ Kiro CLI でのクイックスタート

```bash
# 1. uv をインストール（macOS/Linux）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. ~/.kiro/settings/mcp.json に追加
cat > ~/.kiro/settings/mcp.json <<'EOF'
{
  "mcpServers": {
    "aws-mcp": {
      "command": "uvx",
      "timeout": 100000,
      "transport": "stdio",
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://aws-mcp.us-east-1.api.aws/mcp",
        "--metadata", "AWS_REGION=us-west-2"
      ]
    }
  }
}
EOF

# 3. Skills をインストール
npx skills add aws/agent-toolkit-for-aws/skills

# 4. Kiro CLI で利用開始
kiro-cli chat
```

### 🔍 詳細を読む

→ **[26_AgentToolkitForAWS.md（506行）](01_features/26_AgentToolkitForAWS.md)** で以下を網羅：
- 4 コンポーネント（MCP Server / Skills / Plugins / Rules files）
- 主要 4 ツール（`call_aws` / `search_documentation` / `read_documentation` / `run_script`）
- IAM コンテキストキーと権限分離の実例
- AWS Labs MCP との詳細比較・移行ガイド
- ユースケース 5 件（本番構築・新サービス対応・運用トラブル・エンタープライズ等）
- トラブルシューティング 5 項目

### 📌 公式情報源

- [Agent Toolkit for AWS - 製品ページ](https://aws.amazon.com/jp/products/developer-tools/agent-toolkit-for-aws/)
- [Agent Toolkit for AWS - User Guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html)
- [GitHub: aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)
- [The AWS MCP Server is now generally available（2026-05-06 AWS News Blog）](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available)

---

## 🚀 注目のオープンソース：AI-DLC Adaptive Workflows（2025-11 OSS 化）

> **AWS Labs が公開する AI 駆動開発のための Adaptive Workflows 方法論。**
>
> Kiro CLI とは独立した OSS（**MIT-0** ライセンス）ですが、**v0.1.0（2026-01-22）から Kiro CLI を公式サポート** しており、Steering Files として配置することで Kiro CLI から利用できます。

### 📖 詳細ガイド: **[07. AI-DLC（Kiro CLI で実践する選択肢）](07_aidlc/README.md)** ⭐

**AI-DLC（AI-Driven Development Life Cycle）** は、AI モデルへの「指示書」として Markdown ファイル群（26 ファイル）で構成される **適応型ワークフロー方法論** です。50 年分の SDLC 知見を AI 駆動の文脈で再構成し、**3 フェーズ（Inception / Construction / Operations）× 14 ステージ** で開発プロセスを規律化します。

### 🎯 主な特徴

| 特徴 | 内容 |
|------|------|
| 🧭 **適応型ワークフロー** | "The workflow adapts to the work, not the other way around." — プロジェクトの複雑さに応じてステージと深度が動的調整 |
| 👥 **Human in the Loop** | ほぼすべての 12+ ステージで明示的な人間承認が必須、**NO EMERGENT BEHAVIOR** で AI の自律的判断を制約 |
| 📋 **完全な監査証跡** | `audit.md` に **ISO 8601 タイムスタンプ** で全インタラクションを追記専用で記録（要約禁止） |
| 🔌 **IDE 非依存** | Kiro / **Kiro CLI** / Amazon Q Developer CLI / Claude Code / GitHub Copilot / Cursor / Cline / Codex |
| 🆓 **MIT-0 ライセンス** | 著作権表示の保持義務もなく、最も寛容なライセンス（Agent Toolkit の Apache-2.0 とは異なる） |
| 🔧 **二層構造で拡張可能** | ベースレイヤー（変更不可）+ 拡張レイヤー（自由）で組織独自カスタマイズが可能 |

### ⚡ Kiro CLI でのクイックスタート（macOS/Linux）

```bash
# 1. 最新リリース zip を取得（v0.1.8 以降）
curl -L -o aidlc-rules.zip \
  https://github.com/awslabs/aidlc-workflows/releases/latest/download/aidlc-rules.zip
unzip -d aidlc-rules aidlc-rules.zip

# 2. ステアリングファイルとして配置
mkdir -p .kiro/steering
cp -R aidlc-rules/aws-aidlc-rules .kiro/steering/
cp -R aidlc-rules/aws-aidlc-rule-details .kiro/

# 3. Kiro CLI で確認
kiro-cli
> /context show     # .kiro/steering/aws-aidlc-rules が表示されることを確認

# 4. 開発開始
> Using AI-DLC, let's build a web application to ...
```

### 🔍 詳細を読む

→ **[07_aidlc/README.md](07_aidlc/README.md)** で以下を網羅：
- AI-DLC の中核思想（Adaptive Workflow Principle / 5 Tenets / 8 Key Principles / 4 MANDATORY ルール）
- ワークフロー全体像（公式 Mermaid + 26 ファイル構造）
- 3 フェーズ詳細（Inception 7 ステージ / Construction Per-Unit Loop / Operations プレースホルダー）
- 6 つの仕組み（Adaptive Depth / 承認ゲート / 質問ファイル方式 / Overconfidence Prevention / Smart Context Loading / 監査証跡）
- 既存手法との比較（IEEE 830 / DDD / Well-Architected / GitOps 等、5 領域）
- Extensions（オプトイン式 + 二層構造でのカスタマイズ）
- 補助ツール（AIDLC Evaluator / AIDLC Design Reviewer）
- ユースケース 5 件（Greenfield / Brownfield / Bug Fix / Complex Feature / Agent Toolkit 併用）

### 📌 公式情報源

- [GitHub: awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — リポジトリ本体
- [AI 駆動開発ライフサイクル: ソフトウェアエンジニアリングの再構築 - AWS Blog (2025-07-31)](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/) — 方法論基盤
- [Open sourcing adaptive workflows for AI-DLC - AWS Blog (2025-11-29)](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/) — OSS 化発表
- [Building with AI-DLC using Amazon Q Developer - AWS Blog (2025-11-29)](https://aws.amazon.com/blogs/devops/building-with-ai-dlc-using-amazon-q-developer/) — 実践ウォークスルー
- [AI-DLC Method Definition Paper](https://prod.d13rzhkk8cj2z0.amplifyapp.com/) — 方法論の定義書

---

## 🔗 関連ブログ記事

### Kiro CLI公式発表
- **[Introducing Kiro CLI](https://aws.amazon.com/jp/blogs/news/introducing-kiro-cli/)**
  - Kiro CLIの公式発表記事
  - 基本概念と主要機能の紹介
  - Amazon Q Developer CLIからの進化について

### 移行ガイド
- **[Kiroweeeeeeek in Japan Day 6: Amazon Q Developer CLI to Kiro CLI](https://aws.amazon.com/jp/blogs/news/kiroweeeeeeek-in-japan-day-6-amazon-q-developer-cli-to-kiro-cli/)**
  - Amazon Q Developer CLIからKiro CLIへの移行ガイド
  - 日本での導入事例とベストプラクティス
  - 移行時の注意点と推奨事項

### エンタープライズ運用
- **[AWS 請求統合の Kiro に IAM Identity Center ユーザーでサインインする手順（2026年5月版）](https://dev.classmethod.jp/articles/kiro-iam-identity-center-user-signin-setup-202605/)**
  - IAM Identity Center ビルトインユーザーでのサインイン手順
  - Kiro IDE / CLI / Web それぞれのサインイン方法
  - エンタープライズ環境での初回セットアップ
- **[Kiro のプロンプトログを解析して業務日報のたたき台を作ってみた](https://dev.classmethod.jp/articles/kiro-prompt-log-analysis/)**
  - プロンプトログ機能（S3保存）の有効化とログ構造解析
  - jqでの前処理・集計、Amazon Bedrockでの業務日報生成
  - エンタープライズ向け監査・分析活用例

## 更新方針

1. 公式サイトの定期チェック
2. GitHub Issuesの監視
3. 機能変更の分析・記録
