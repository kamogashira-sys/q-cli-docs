[ホーム](../README.md) > [機能詳細ガイド](README.md) > Agent Toolkit for AWS

# 26. Agent Toolkit for AWS（AWS 公式エージェント統合ツールキット）

**出典**:
- [Agent Toolkit for AWS - 製品ページ](https://aws.amazon.com/jp/products/developer-tools/agent-toolkit-for-aws/)
- [Agent Toolkit for AWS - User Guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html)
- [The AWS MCP Server is now generally available - AWS News Blog (2026-05-06)](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available)
- [GitHub: aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)
- [What's New: Agent Toolkit (2026-05)](https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/)

## 概要

### Agent Toolkit for AWS とは

**Agent Toolkit for AWS** は、AI コーディングエージェント（**Claude Code / Kiro CLI / Kiro / Cursor / Codex / Windsurf / Cline 等**）が AWS サービス上で **効果的かつ安全に** 動作するための公式 AWS 製品です。AWS の **公式 MCP Server**、**Skills**（タスク別ガイド）、**Plugins**、**Rules files** を統合的に提供します。

**2026 年 5 月 6 日に AWS MCP Server が GA リリース** されました。**Kiro CLI / Kiro は公式に対応エージェントとして明示** されています。

### 主な特徴

- ✅ **公式 MCP Server**: 単一エンドポイント（`https://aws-mcp.us-east-1.api.aws/mcp`）から **300+ AWS サービス / 15,000+ API アクション** にアクセス
- ✅ **エージェント vs 人間の権限分離**: IAM コンテキストキー `aws:ViaAWSMCPService` / `aws:CalledViaAWSMCP` で区別可能
- ✅ **エンタープライズ可観測性**: CloudWatch メトリクス（`AWS-MCP` namespace）+ CloudTrail 監査ログ
- ✅ **サンドボックス Python 実行**: ネットワーク・ファイルシステムなしで `run_script` ツール
- ✅ **リアルタイム公式ドキュメント**: モデルの学習カットオフ後の AWS 新機能（S3 Vectors / Aurora DSQL / Bedrock AgentCore 等）にも対応
- ✅ **追加料金なし**: AWS リソース利用料のみ
- ✅ **AWS Labs MCP の後継**: IAM 条件キー、CloudWatch メトリクス、評価済み Skills を提供

### なぜ Agent Toolkit for AWS が必要なのか

AI コーディングエージェントは AWS で深く作業する際、以下の問題に直面していました：

| 問題 | Agent Toolkit for AWS による解決 |
|-----|------------------------------|
| **学習データの古さ** — Foundation Model は数ヶ月〜数年前のデータで訓練、新サービス（S3 Vectors / Aurora DSQL / Bedrock AgentCore）を知らない | `search_documentation` / `read_documentation` でリアルタイム公式ドキュメント取得 |
| **AWS CLI への偏向** — IaC（CDK/CloudFormation）より AWS CLI を選びがち | Skills が IaC ベースのベストプラクティスを提供 |
| **過剰な IAM ポリシー** — 必要以上に広い権限を生成 | Skills + 最小権限ガイダンス |
| **エージェントと人間の区別不可** — ローカルターミナル経由の実行はエージェント／人間を区別できない | IAM コンテキストキーで区別、IAM ポリシー / SCP で別制御可能 |
| **監査困難** — エージェント活動の追跡手段なし | CloudWatch メトリクス + CloudTrail で完全可視化 |
| **トークンの浪費** — 試行錯誤で API を間違える | Skills で最初から正しい手順 |

**公式ドキュメント原文**:
> The Agent Toolkit for AWS gives AI coding agents the tools, knowledge, and guardrails they need to build, deploy, and manage applications on AWS. It works with the coding agents that developers already use — including Claude Code, Cursor, and Codex — without requiring you to switch tools or learn a new workflow.

---

## 📋 目次

- [4 つのコンポーネント](#4-つのコンポーネント)
- [主要ツール（call_aws / search_documentation / read_documentation / run_script）](#主要ツール)
- [Kiro CLI 統合手順](#kiro-cli-統合手順)
- [IAM コンテキストキーと権限分離](#iam-コンテキストキーと権限分離)
- [エンタープライズ可観測性（CloudWatch / CloudTrail）](#エンタープライズ可観測性)
- [AWS Labs MCP との比較・移行](#aws-labs-mcp-との比較移行)
- [ユースケース](#ユースケース)
- [リージョンと価格](#リージョンと価格)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## 4 つのコンポーネント

**出典**: [User Guide - Components](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html#agent-toolkit-components)

Agent Toolkit for AWS は連動する **4 つのコンポーネント** で構成されます。

### 1. AWS MCP Server（マネージドリモートサーバー）

- **エンドポイント**: `https://aws-mcp.us-east-1.api.aws/mcp` または `https://aws-mcp.eu-central-1.api.aws/mcp`
- **認証**: IAM SigV4（`call_aws` / `run_script` / Skills 利用時）。ドキュメント検索は **認証不要**
- **アクセス**: 単一エンドポイントから AWS 全サービスにアクセス（CLI ローカルインストール不要）

### 2. Agent Skills（オンデマンドロード）

- **目的**: AWS タスク別の手順、コードスニペット、参照資料のキュレーション
- **特徴**:
  - **オンデマンドロード**: タスク関連の Skill のみ取得 → コンテキストウィンドウ節約
  - **AWS サービスチームが管理**
  - **エンドツーエンド評価済み**
- **内容例**:
  - サービス選定ガイド（適切な AWS サービスの選び方とトレードオフ）
  - ステップバイステップ手順（S3 Tables 作成、Glue ETL、IAM ポリシー、サーバーレスデプロイ等）
  - トラブルシューティング診断手順
- **公開**: GitHub https://github.com/aws/agent-toolkit-for-aws （オープンソース）

> **歴史的注記**: Skills は **Agent SOPs の後継** です（GA 時に移行）。Agent SOPs を使用していたユーザーは Skills への移行が推奨されます。

### 3. Plugins（簡易インストール）

- **対象**: Claude Code、Codex、Cursor（追加対応予定）
- **内容**: AWS MCP Server 設定 + 厳選 Skills セット
- **特徴**:
  - 単一インストールで MCP Server + Skills が有効化
  - 自動更新（新機能が追加されると Plugin から配信）

> **Kiro / Kiro CLI**: Plugins は未対応（2026-05 時点）。代わりに `mcp.json` 直接設定で利用可能（後述）。

### 4. Rules files（プロジェクトレベル設定）

- **目的**: プロジェクトごとにエージェントへのガードレール／優先設定を定義
- **内容例**:
  - 「AWS 操作時は必ず AWS MCP Server 経由で行う」
  - 「行動前に Skills を発見・確認する」
  - 「ドキュメント検索を優先する」
- **役割**: Steering との関係（Kiro CLI の場合は `.kiro/steering/` でも同様の効果を実現可能）

---

## 主要ツール

**出典**: [AWS News Blog - The AWS MCP Server is now generally available](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available)

AWS MCP Server が公開する **4 つの主要ツール**：

### `call_aws` — AWS API 実行

- 任意の AWS API（**15,000+ アクション**）を実行
- 既存の IAM 認証情報を使用
- 新 API は **数日以内** にサポート対象に追加

### `search_documentation` — ドキュメント検索

- **認証不要** で AWS 公式ドキュメントを検索
- モデルの学習カットオフ後の新サービス（S3 Vectors、Aurora DSQL、Bedrock AgentCore 等）にも対応

### `read_documentation` — ドキュメント全文取得

- 検索結果から特定ドキュメントを全文取得
- API リファレンス、ユーザーガイドにアクセス

### `run_script` — サンドボックス Python 実行

- サーバーサイドのサンドボックス環境で Python スクリプト実行
- IAM 権限を継承
- **ネットワーク・ローカルファイルシステムへのアクセスなし**
- 用途: 複数 API 呼び出しのチェーン、データフィルタリング、結果集計を **1 ラウンドトリップ** で実行 → 高速・トークン節約

---

## Kiro CLI 統合手順

**出典**: [Agent Toolkit for AWS - Getting Started (Kiro)](https://aws.amazon.com/jp/products/developer-tools/agent-toolkit-for-aws/)

### 前提条件

1. **AWS アカウントと IAM 認証情報**（`call_aws` / `run_script` 利用時）
2. **`uv` のインストール**（macOS/Linux）:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **AWS 認証情報の設定**: `aws configure` または既存の IAM 環境

### MCP Server 設定

`~/.kiro/settings/mcp.json` に以下を追加：

```json
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
```

#### 設定の説明

| 項目 | 意味 |
|------|------|
| `uvx mcp-proxy-for-aws@latest` | IAM SigV4 ↔ OAuth 2.1 ブリッジプロキシ（[GitHub: aws/mcp-proxy-for-aws](https://github.com/aws/mcp-proxy-for-aws)） |
| `https://aws-mcp.us-east-1.api.aws/mcp` | AWS MCP Server リージョナルエンドポイント（US East 1 または EU Frankfurt） |
| `--metadata AWS_REGION=us-west-2` | API 呼び出し時のターゲットリージョン（任意の AWS リージョン指定可能） |
| `timeout: 100000` | タイムアウト（ミリ秒） |

> **MCP Proxy for AWS の役割**: MCP 仕様は OAuth 2.1 のみサポートしますが、AWS は IAM SigV4 認証を使用します。Proxy がローカルで両者をブリッジします。

### Skills のインストール

```bash
npx skills add aws/agent-toolkit-for-aws/skills
```

→ Kiro CLI の Skills として `.kiro/skills/` に配置され、エージェントが自動利用します。詳細は [07. Skills](07_Skills.md) を参照。

### 動作確認

Kiro CLI 起動後：

```bash
kiro-cli chat
```

チャット内で：

```
> aws-mcp サーバーの状態を確認して
```

または `/mcp` スラッシュコマンドで状態確認。

### 試してみる

公式提案のサンプルプロンプト：

> Create an S3 bucket with versioning enabled and a lifecycle policy that transitions objects to Glacier after 90 days.

エージェントは `search_documentation` で最新仕様を確認 → `call_aws` で実装 → 結果検証、を自動実行します。

---

## IAM コンテキストキーと権限分離

**出典**: [User Guide - How the Agent Toolkit for AWS works](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html#how-agent-toolkit-works)

AWS MCP Server はすべてのリクエストに **2 つのグローバルコンテキストキー** を自動付与します：

| コンテキストキー | 説明 |
|--------------|------|
| `aws:ViaAWSMCPService` | リクエストが AWS MCP Service 経由かどうか（`true`/`false`） |
| `aws:CalledViaAWSMCP` | 呼び出し元が AWS MCP かどうか |

### IAM ポリシーでの使用例

「このユーザーは通常は書き込み可能だが、エージェント経由（MCP 経由）の場合は **読取専用に制限** する」：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "s3:DeleteObject",
        "s3:DeleteBucket",
        "ec2:TerminateInstances",
        "rds:DeleteDB*"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:CalledViaAWSMCP": "true"
        }
      }
    }
  ]
}
```

### Service Control Policies（SCP）での組織レベル制御

組織全体で「エージェント経由のリクエストは特定アクションのみ許可」のような **エンタープライズガードレール** を設定可能。

> **推奨**: AWS 公式は「エージェントが必要な最小権限まで IAM ロールをスコープダウンする」ことを推奨しています。

→ Kiro CLI の Granular Tool Trust と組み合わせ可能: [17. Granular Tool Trust](17_GranularToolTrust.md)

---

## エンタープライズ可観測性

### CloudWatch メトリクス（`AWS-MCP` namespace）

- **メトリクス namespace**: `AWS-MCP`
- **観測対象**: MCP Server 経由のすべての呼び出し（直接の人間 API 呼び出しと区別可能）
- **用途**:
  - エージェント活動量の追跡
  - 異常検知（過剰な API 呼び出し、エラー率上昇）
  - コスト分析（人間活動 vs エージェント活動）

### CloudTrail 監査

- すべての `call_aws` / `run_script` リクエストが CloudTrail に記録
- IAM コンテキストキーも記録 → エージェント由来のアクションを後追い分析可能
- コンプライアンス要件（SOC 2、ISO 27001、HIPAA 等）に対応

### サンドボックス実行の安全性

`run_script` ツールは：
- IAM 権限を継承（カスタム権限ではない）
- **ローカルファイルシステムへのアクセスなし**
- **ネットワークアクセスなし**（外部 URL 等）
- → AWS API のみに対して安全に Python コード実行

---

## AWS Labs MCP との比較・移行

**出典**: [Agent Toolkit FAQ](https://aws.amazon.com/jp/products/developer-tools/agent-toolkit-for-aws/#faqs--1a531s3)

> **公式 FAQ より**:  
> *"The Agent Toolkit for AWS is the successor to those tools. We recommend using the Agent Toolkit for AWS..."*

Agent Toolkit for AWS は **AWS Labs MCP Server / Skills / Plugins の正式後継** です。

### 機能比較

| 観点 | AWS Labs MCP（旧） | **Agent Toolkit for AWS（新・推奨）** |
|-----|----------------|----------------------------|
| **管理元** | AWS Labs（コミュニティ） | AWS 製品チーム |
| **配布形態** | 個別 MCP サーバー（多数） | 統合エンドポイント 1 つ |
| **IAM コンテキストキー** | なし | ✅ `aws:ViaAWSMCPService` / `aws:CalledViaAWSMCP` |
| **CloudWatch メトリクス** | なし | ✅ `AWS-MCP` namespace |
| **CloudTrail 監査** | 限定的 | ✅ 全リクエスト記録 |
| **Skills 評価** | コントリビューターのテスト | ✅ AWS による end-to-end 評価 |
| **Sandboxed script 実行** | なし | ✅ `run_script` |
| **エージェントと人間の権限分離** | 不可 | ✅ IAM ポリシーで分離可能 |
| **新 AWS API 対応速度** | サーバーごと別 | 数日以内に統合 |

### 移行の判断基準

**Agent Toolkit for AWS への移行を推奨**：
- ✅ エンタープライズ環境（権限分離が必要）
- ✅ 監査ログが必要
- ✅ 評価済み Skills が必要
- ✅ 単一エンドポイントで管理を簡素化したい

**AWS Labs MCP の継続使用が妥当**：
- ⚠️ 既に多数の AWS Labs MCP サーバーを安定運用中で、移行コストを慎重に評価したい場合
- ⚠️ AWS Labs にしかない特殊用途のサーバーを使用している場合

> **公式の方針**: AWS Labs の MCP サーバー / Skills / Plugins は引き続き動作・コントリビューション受付。時間とともに AWS Labs の優れた部分を Agent Toolkit へ統合予定。

→ AWS Labs MCP リポジトリ: https://github.com/awslabs

---

## ユースケース

### ユースケース 1: AWS インフラの本番グレード構築

**シナリオ**: VPC、サブネット、セキュリティグループ、ALB、ECS、RDS の構築。

**従来**: エージェントが AWS CLI で個別に作成 → 命名・ネットワーク設計が一貫しない。  
**Agent Toolkit**: Skills が CDK/CloudFormation ベースの **本番グレードパターン** を提供。Well-Architected 準拠の設計で、IAM 最小権限・コスト最適化・セキュリティ設定込み。

### ユースケース 2: 新 AWS サービスへの即時対応

**シナリオ**: 「Amazon S3 Vectors を使ってベクトル埋め込みを保存して」

**従来（Claude Opus 4.6 単独）**: モデルの学習カットオフ（2025-05）後にリリースされた S3 Vectors を知らず、汎用的な「S3 + 別 DB」を提案。  
**Agent Toolkit**: `search_documentation` で最新ドキュメントを取得 → S3 Vectors を正しく提案・実装。

### ユースケース 3: カスタム AI エージェントへの AWS 機能追加

Strands、LangChain、Bedrock AgentCore で構築した自社エージェントに AWS 操作能力を付与：

```python
# Strands Agent の例（疑似コード）
from strands_agents import Agent

agent = Agent(
    mcp_servers=["https://aws-mcp.us-east-1.api.aws/mcp"],
    tools=["call_aws", "search_documentation", "run_script"]
)
agent.run("Analyze our CloudWatch logs from the last 24 hours")
```

→ サンドボックス Python 実行で複雑な分析も安全に。

### ユースケース 4: 運用トラブルシューティング

**シナリオ**: 本番環境で「Lambda 関数のエラー率が突然 30% に上昇」

**Agent Toolkit のフロー**:
1. `search_documentation` で「Lambda エラー率上昇」のトラブルシューティング Skill を発見
2. `call_aws` で CloudWatch Logs / X-Ray トレースを取得
3. `run_script` で複数指標を時系列で集計分析
4. 根本原因（例: 依存サービスのスロットリング）を特定
5. 修正手順を提案

### ユースケース 5: エンタープライズでのエージェント運用

**シナリオ**: 開発チームが Kiro CLI でエージェントを使うが、本番リソースの削除・変更は禁止したい。

**設定**:
```json
// SCP（組織レベル）
{
  "Statement": [{
    "Effect": "Deny",
    "Action": ["*:Delete*", "*:Terminate*"],
    "Condition": {
      "Bool": {"aws:CalledViaAWSMCP": "true"}
    }
  }]
}
```

→ 開発者本人は管理コンソールから削除可能だが、エージェント経由ではブロック。CloudWatch で違反試行も記録される。

---

## リージョンと価格

### 提供リージョン（AWS MCP Server）

| リージョン | エンドポイント |
|----------|------------|
| US East (N. Virginia) | `https://aws-mcp.us-east-1.api.aws/mcp` |
| Europe (Frankfurt) | `https://aws-mcp.eu-central-1.api.aws/mcp` |

> **API 呼び出し対象**: 上記エンドポイントから **任意の AWS リージョン** に対して `call_aws` 実行可能（`--metadata AWS_REGION=...` で指定）。

### 価格

- **AWS MCP Server 自体: 追加料金なし**
- 課金対象:
  - エージェントが作成 / 操作する **AWS リソースの標準料金**
  - データ転送料金（リージョン間等）

---

## トラブルシューティング

### 1. `uvx` コマンドが見つからない

```bash
# uv をインストール（macOS/Linux）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Kiro CLI が AWS MCP Server に接続できない

確認手順：
1. `~/.aws/credentials` または `aws configure list` で AWS 認証情報を確認
2. ネットワーク（プロキシ環境では `HTTPS_PROXY` 設定）
3. Kiro CLI で `/mcp` スラッシュコマンドで状態確認 → エラーログ確認
4. Kiro CLI のログ確認: `$TMPDIR/kiro-log/kiro-chat.log`（macOS）

→ プロキシ環境: [03_deployment/03_official-installation.md](../03_deployment/03_official-installation.md)

### 3. エージェントが古い情報を返す（S3 Vectors を知らない等）

AWS MCP Server の `search_documentation` がエージェントから **未使用** の可能性。Skills インストールを確認：

```bash
npx skills add aws/agent-toolkit-for-aws/skills
```

または Rules files（または Kiro Steering）で「AWS 操作前に必ず `search_documentation` を実行」を明示。

### 4. IAM 権限不足エラー

最小権限のポイント：
- `call_aws` 実行に必要な AWS 各サービスの権限
- `run_script` も IAM ロールを継承（追加権限不要）
- `search_documentation` / `read_documentation` は **認証不要**

`aws:CalledViaAWSMCP` を使った IAM ポリシーで、エージェント専用の制限を設定可能。

### 5. CloudWatch メトリクスが表示されない

- namespace が正しいか: `AWS-MCP`
- リージョン: メトリクスは MCP Server エンドポイントのリージョンに発行される（`us-east-1` または `eu-central-1`）
- IAM 権限: `cloudwatch:GetMetricData` が必要

---

## 関連リンク

### 関連機能（本サイト）

- [13. Agent Client Protocol (ACP)](13_ACP.md) — エディタ統合と MCP の関係
- [19. Tool Search](19_ToolSearch.md) — MCP ツールのオンデマンドロード（Agent Toolkit Skills と同様の思想）
- [17. Granular Tool Trust](17_GranularToolTrust.md) — Kiro CLI 側でのツール信頼スコープ制御（IAM コンテキストキーと併用）
- [22. Smart Hooks](22_Hooks.md) — Hook で `call_aws` / `run_script` 等の MCP ツール呼び出しを監査
- [23. Agent Steering](23_Steering.md) — Kiro CLI Steering（AGENTS.md）と Agent Toolkit Rules files の併用

### リファレンス（辞書）

- [04_reference/01_settings.md](../04_reference/01_settings.md) — MCP 設定（`mcp.json`、`KIRO_HOME`）
- [04_reference/04_built-in-tools.md](../04_reference/04_built-in-tools.md) — Kiro CLI ビルトイン `aws` ツールと外部 MCP の使い分け

### バージョン関連

- [02_update/01_changelog.md](../02_update/01_changelog.md)
  - v2.3.0（2026-05-12）: MCP OAuth clientId 設定（DCR 非対応サーバー対応）
  - v2.2.2（2026-05-05）: MCP ガバナンス強化

### 公式情報源

- [Agent Toolkit for AWS - 製品ページ](https://aws.amazon.com/jp/products/developer-tools/agent-toolkit-for-aws/)
- [Agent Toolkit for AWS - User Guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html)
- [GitHub: aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)
- [GitHub: aws/mcp-proxy-for-aws](https://github.com/aws/mcp-proxy-for-aws) — IAM ↔ OAuth ブリッジ
- [The AWS MCP Server is now generally available - AWS News Blog (2026-05-06)](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available)
- [What's New: Agent Toolkit (2026-05)](https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/)
- [Model Context Protocol (MCP) - 公式仕様](https://modelcontextprotocol.io/)

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式 GA**: 2026-05-06
