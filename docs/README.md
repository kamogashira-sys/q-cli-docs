[ホーム](README.md)

---

# ドキュメント

**対象バージョン**: v1.19.6以降  
**総ドキュメント数**: 126文書

> 💡 **補足**: この数値はカテゴリ別に分類されたドキュメントの数です。

---

## 🚀 はじめに

Amazon Q Developer CLI（Q CLI）は、AIを活用した開発者向けコマンドラインツールです。このドキュメントサイトでは、インストールから高度な活用方法まで、Q CLIを効果的に使用するための情報を提供します。

> **💡 ワンポイント**: 主要な用語
> - **Agent（エージェント）**: Q CLIの動作をカスタマイズする設定ファイル。プロジェクトごとに異なる設定が可能
> - **MCP（Model Context Protocol）**: 外部ツールと連携するためのプロトコル。AWS CLIやデータベースなどと統合できる
> - **Knowledge Base**: プロジェクトのドキュメントやコードを検索する機能。BM25/Vector検索をサポート
> - **IAM Identity Center**: エンタープライズ向けの統合認証システム。組織全体でQ CLIを管理できる

---

## 🎬 Q CLIを使うとこんなに便利！

### Before（従来の方法）

**AWS リソースの確認**
```bash
# 複数のコマンドを覚える必要がある
aws s3 ls
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'
aws lambda list-functions --query 'Functions[].[FunctionName,Runtime]'

# → 3つのコマンド、複雑なクエリ構文
```

**コードの生成**
```bash
# 1. ブラウザでStack Overflowを検索
# 2. コードをコピー
# 3. エディタに貼り付け
# 4. 自分のプロジェクトに合わせて修正

# → 約5-10分
```

**ドキュメントの作成**
```bash
# 1. コードを読んで理解
# 2. マークダウンファイルを作成
# 3. 手動で説明を記述
# 4. コード例を追加

# → 約30-60分
```

### After（Q CLI）

**AWS リソースの確認**
```bash
q chat "S3バケット、EC2インスタンス、Lambda関数の一覧を教えて"

# → 1つのコマンド、自然言語で一度に確認可能
```

**コードの生成**
```bash
q chat "Pythonでファクトリアルを計算する関数を書いて"

# → 約30秒
```

**ドキュメントの作成**
```bash
q chat "このプロジェクトのREADME.mdを作成して"

# → 約2-3分
```

### 効果

| タスク | 従来の方法 | Q CLI | 削減率 |
|--------|-----------|-------|--------|
| AWS リソース確認 | 3コマンド | 1コマンド | **67%削減** |
| コード生成 | 5-10分 | 30秒 | **90%削減** |
| ドキュメント作成 | 30-60分 | 2-3分 | **95%削減** |

**平均的な効果**: 作業時間を**60-90%削減**

---

### クイックスタート

初めての方は、以下の順序でドキュメントをお読みください：

1. **[インストール](01_for-users/01_getting-started/01_installation.md)** - Amazon Q CLIのインストール方法
2. **[クイックスタート](01_for-users/01_getting-started/02_quick-start.md)** - 5分で始めるQ CLI
3. **[最初の一歩](01_for-users/01_getting-started/03_first-steps.md)** - 基本的な使い方

### 学習パス

```mermaid
graph TD
    A[Getting Started] --> B[設定ガイド]
    A --> C[機能ガイド]
    B --> D[ベストプラクティス]
    C --> D
    D --> E[トラブルシューティング]
    
    style A fill:#d4edda
    style B fill:#d1ecf1
    style C fill:#d1ecf1
    style D fill:#fff3cd
    style E fill:#f8d7da
```

**推奨学習順序**:
1. 🟢 Getting Started（初級）→ 基本を習得
2. 🔵 設定ガイド・機能ガイド（中級）→ カスタマイズを学ぶ
3. 🟡 ベストプラクティス（中級〜上級）→ 効果的な使い方を習得
4. 🔴 トラブルシューティング（必要時）→ 問題を解決

---

## 🚀 クイックアクセス

- **[クイックリファレンス](01_for-users/07_reference/08_quick-reference.md)** - よく使うコマンドと設定を素早く参照
- **[トピック別インデックス](01_for-users/07_reference/09_topic-index.md)** - やりたいことからドキュメントを探す

---

## 📖 ドキュメント構成

### 📁 ディレクトリ構造

```
docs/
├── 01_for-users/              # ユーザーガイド（81文書）
│   ├── 01_getting-started/    # 入門ガイド（4文書）
│   ├── 02_features/           # 機能ガイド（16文書）
│   ├── 03_configuration/      # 設定ガイド（9文書）
│   ├── 04_best-practices/     # ベストプラクティス（7文書）
│   ├── 05_deployment/         # デプロイメント（4文書）
│   ├── 06_troubleshooting/    # トラブルシューティング（3文書）
│   ├── 07_reference/          # リファレンス（11文書）
│   ├── 08_guides/             # コンテキスト管理ガイド（10文書）
│   ├── 09_security/           # セキュリティ（7文書）
│   └── 10_file-specifications/ # ファイル仕様（8文書）
├── 02_for-developers/         # 開発者ガイド（11文書）
│   ├── 01_contributing/       # コントリビューション（5文書）
│   └── 02_architecture/       # アーキテクチャ（5文書）
├── 03_for-community/          # コミュニティ（15文書）
│   ├── 01_updates/            # アップデート情報（5文書）
│   ├── 02_community/          # コミュニティ（4文書）
│   └── 03_analysis/           # 分析レポート（4文書）
├── 04_issues/                 # 課題管理（1文書）
└── 05_meta/                   # メタドキュメント（15文書）
```

---

### 🎯 Getting Started（初心者向け）- 全5文書

Amazon Q CLIを初めて使う方向けのガイドです。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/01_getting-started/README.md) | 初級 | Getting Startedセクションの概要とナビゲーション |
| 2 | [インストールガイド](01_for-users/01_getting-started/01_installation.md) | 初級 | OS別インストール手順（macOS/Linux）、Homebrew/手動インストール、システム要件 |
| 3 | [クイックスタート](01_for-users/01_getting-started/02_quick-start.md) | 初級 | 5分で始める、インストール→認証→初回チャット、基本コマンド |
| 4 | [最初の一歩](01_for-users/01_getting-started/03_first-steps.md) | 初級 | 基本操作、チャット/ファイル操作/コマンド実行、Agent切り替え、履歴管理 |
| 5 | [料金プラン](01_for-users/01_getting-started/04_pricing.md) | 初級 | Free/Proプランの違い、料金体系、エンタープライズ向けオプション |

**次のステップ**: Getting Startedを完了したら、[設定ガイド](#設定ガイド9文書)でQ CLIをカスタマイズしましょう。

---

### 📚 User Guide（ユーザーガイド）- 全46文書

Amazon Q CLIの機能と設定を詳しく学びたい方向けのガイドです。

| # | カテゴリ | 文書数 | 対象ユーザー | 概要 |
|---|---------|--------|------------|------|
| 1 | [設定ガイド](#設定ガイド9文書) | 9 | 初級〜中級 | 設定システム、グローバル/Agent/MCP設定、環境変数、優先順位 |
| 2 | [機能ガイド](#機能ガイド8文書) | 8 | 初級〜上級 | チャット、Agent、オートコンプリート、ショートカット、実験的機能 |
| 3 | [コンテキスト管理ガイド](#コンテキスト管理ガイド9文書重要) | 9 | 初級〜上級 | コンテキストの本質、仕組み、ベストプラクティス、実践ガイド |
| 4 | [ベストプラクティス](#ベストプラクティス6文書) | 6 | 中級〜上級 | 設定、セキュリティ、パフォーマンス最適化、実践的ユースケース |
| 5 | [エンタープライズ導入](#エンタープライズ導入4文書) | 4 | 中級〜上級 | 組織導入、料金プラン比較、セキュリティチェックリスト |
| 6 | [セキュリティガイド](#セキュリティガイド7文書重要) | 7 | 初級〜上級 | データプライバシー、アクセス制御、認証情報管理 |
| 7 | [トラブルシューティング](#トラブルシューティング3文書) | 3 | 初級〜中級 | よくある問題、FAQ、診断方法 |

---

#### 設定ガイド（9文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/03_configuration/README.md) | 初級 | 設定ガイドセクションの概要とナビゲーション |
| 2 | [設定システム概要](01_for-users/03_configuration/01_overview.md) | 初級〜中級 | 設定システム全体像、5段階優先順位、4種類の設定（グローバル/Agent/MCP/環境変数） |
| 3 | [グローバル設定](01_for-users/03_configuration/02_global-settings.md) | 初級 | settings.json、35項目（テレメトリ/チャット/Knowledge/デフォルトAgent） |
| 4 | [Agent設定](01_for-users/03_configuration/03_agent-configuration.md) | 中級 | JSONスキーマ、グローバル/ローカルAgent、必須/オプションフィールド、検証方法 |
| 5 | [MCP設定](01_for-users/03_configuration/04_mcp-configuration.md) | 中級 | MCPサーバー設定、stdio/HTTP接続、OAuth認証、環境変数展開 |
| 6 | [環境変数](01_for-users/03_configuration/06_environment-variables.md) | 中級 | 23項目、Q CLI固有18項目、設定方法、実践パターン |
| 7 | [テレメトリー設定](01_for-users/03_configuration/05_telemetry.md) | 初級〜中級 | テレメトリーデータ収集、オプトアウト方法、プライバシー設定 |
| 8 | [優先順位ルール](01_for-users/03_configuration/07_priority-rules.md) | 中級 | 5段階優先順位（CLI引数→環境変数→ローカルAgent→グローバルAgent→デフォルト）、フロー図 |
| 9 | [設定例集](01_for-users/03_configuration/08_examples.md) | 中級 | 実践的な設定例、ユースケース別（開発/本番/チーム） |

**次のステップ**: 設定をカスタマイズしたら、[機能ガイド](#機能ガイド8文書)で各機能の使い方を学びましょう。

#### 機能ガイド（16文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/02_features/README.md) | 初級〜中級 | Featuresセクションの概要、チャットコマンド詳細ガイドへのナビゲーション |
| 2 | [チャット機能](01_for-users/02_features/01_chat.md) | 初級 | 基本操作、25コマンドの分類、初心者向け学習導線 |
| 3-10 | [チャットコマンド詳細](01_for-users/02_features/02_chat-commands/) | 初級〜上級 | 8分類の詳細ガイド（基本・コンテキスト・プロンプト・Knowledge・Checkpoint・TODO・Agent・開発者向け） |
| 11 | [Agent機能](01_for-users/02_features/02_agents.md) | 中級 | Agent概要、管理コマンド（list/切り替え）、カスタマイズ項目 |
| 12 | [オートコンプリート](01_for-users/02_features/03_autocomplete.md) | 初級 | オートコンプリート機能、設定、使い方 |
| 13 | [Checkpoint機能](01_for-users/02_features/05_checkpoints.md) | 初級〜中級 | チェックポイント機能、保存/復元、自動保存設定 |
| 14 | [キーボードショートカット](01_for-users/02_features/04_keyboard-shortcuts.md) | 初級〜中級 | ショートカット一覧、Tangent/Skim/Delegateモード、カスタマイズ |
| 15 | [SSH/リモート接続](01_for-users/02_features/06_ssh-remote.md) | 中級 | リモート環境での使用、SSH接続、設定方法 |
| 16 | [実験的機能](01_for-users/02_features/07_experimental.md) | 上級 | 実験的機能、Delegate Mode、安全性警告、ベストプラクティス |

**次のステップ**: 機能を理解したら、[コンテキスト管理ガイド](#コンテキスト管理ガイド9文書)でQ CLIの応答品質を最大化する方法を学びましょう。

#### コンテキスト管理ガイド（9文書）【重要】

**Q CLIを効果的に使うための最重要ガイド**

Q CLIの応答品質は**コンテキスト管理**で決まります。全8章構成の包括的ガイドで体系的に学習できます。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/08_guides/README.md) | 初級〜上級 | ガイド全体の概要、学習パス、各章の位置づけ |
| 2 | [本質編](01_for-users/08_guides/01_essence.md) | 初級 | コンテキストとは何か、なぜ重要か、基本概念 |
| 3 | [仕組み編](01_for-users/08_guides/02_mechanism.md) | 初級〜中級 | 内部動作の理解、3つの提供方法、処理フロー |
| 4 | [効果編](01_for-users/08_guides/03_effects.md) | 初級〜中級 | 何ができるか、Agent Resources/Session Context/Knowledge Bases |
| 5 | [ベストプラクティス編](01_for-users/08_guides/04_best-practices.md) | 中級 | 設計原則、アプローチ選択、実装パターン、最適化 |
| 6 | [実践ガイド編](01_for-users/08_guides/05_practical-guide.md) | 中級 | プロジェクト別実装例、基本/応用パターン、アンチパターン |
| 7 | [トラブルシューティング編](01_for-users/08_guides/06_troubleshooting.md) | 中級 | 問題診断、一般的な問題、デバッグ技法 |
| 8 | [上級編](01_for-users/08_guides/07_advanced.md) | 上級 | 最適化戦略、チーム開発、内部実装の理解 |
| 9 | [リファレンス編](01_for-users/08_guides/08_reference.md) | 中級〜上級 | コマンドリファレンス、技術仕様、用語集、FAQ |

> **💡 学習の進め方**
> - **初心者**: 第1章→第3章→第5章（基本を理解して実践）
> - **中級者**: 第4章→第5章→第6章（ベストプラクティスを習得）
> - **上級者**: 第7章→第8章（最適化とチーム開発）

**次のステップ**: コンテキスト管理を理解したら、[ベストプラクティス](#ベストプラクティス6文書)で効果的な使い方を学びましょう。

#### エンタープライズ導入（4文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/05_deployment/README.md) | 中級〜上級 | Deploymentセクションの概要 |
| 2 | [エンタープライズ導入ガイド](01_for-users/05_deployment/01_enterprise-deployment.md) | 中級〜上級 | IAM Identity Center、組織導入、Pro契約、段階的ロールアウト、セキュリティ |
| 3 | [料金プラン比較](01_for-users/05_deployment/02_pricing-comparison.md) | 中級 | Free/Pro/Enterpriseプラン比較、データ使用ポリシー、推奨環境 |
| 4 | [セキュリティチェックリスト](01_for-users/05_deployment/03_security-checklist.md) | 中級〜上級 | エンタープライズ導入時のセキュリティチェック項目、ツール権限管理 |

**次のステップ**: セキュリティについて詳しく知りたい場合は、[セキュリティガイド](#セキュリティガイド7文書)を参照してください。

#### セキュリティガイド（7文書）【重要】

**Q CLIを安全に使用するための包括的ガイド**

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/09_security/README.md) | 初級〜上級 | セキュリティガイド全体の概要 |
| 2 | [セキュリティ概要](01_for-users/09_security/01_security-overview.md) | 初級〜中級 | AWS責任共有モデル、主要セキュリティトピック、環境別推奨設定 |
| 3 | [データプライバシー](01_for-users/09_security/02_data-privacy.md) | 初級〜中級 | Free vs Pro/Enterpriseプラン、サービス改善データ使用、オプトアウト |
| 4 | [ファイルアクセス制御](01_for-users/09_security/03_file-access-control.md) | 中級 | fs_readツール制御、機密ファイル保護、環境別設定 |
| 5 | [AWS API制御](01_for-users/09_security/04_aws-api-control.md) | 中級 | use_awsツール制御、IAMポリシー制限、コスト管理 |
| 6 | [認証情報管理](01_for-users/09_security/05_credentials-management.md) | 中級 | AWS Builder ID/IAM Identity Center、ベストプラクティス、暗号化 |
| 7 | [trust-all安全使用](01_for-users/09_security/06_trust-all-safety.md) | 中級〜上級 | trust-allの危険性、安全な使用方法、チェックリスト |

**次のステップ**: セキュリティを理解したら、[ファイル仕様](#ファイル仕様8文書)で技術的な詳細を学びましょう。

#### ファイル仕様（8文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/10_file-specifications/README.md) | 中級〜上級 | ファイル仕様セクションの概要 |
| 2 | [.cli_bash_history](01_for-users/10_file-specifications/01_cli-bash-history.md) | 中級〜上級 | チャット履歴ファイル、rustyline FileHistory形式、管理操作 |
| 3 | [Agent設定ファイル](01_for-users/10_file-specifications/02_agent-configuration.md) | 中級〜上級 | agent.json仕様、JSONスキーマ、フィールド定義 |
| 4 | [MCP設定ファイル](01_for-users/10_file-specifications/03_mcp-configuration.md) | 中級〜上級 | mcp.json仕様、サーバー設定、環境変数展開 |
| 5 | [グローバル設定ファイル](01_for-users/10_file-specifications/04_global-settings.md) | 中級〜上級 | settings.json仕様、設定項目、デフォルト値 |
| 6 | [チェックポイント](01_for-users/10_file-specifications/05_checkpoint.md) | 中級〜上級 | チェックポイントファイル形式、保存・復元操作 |
| 7 | [会話状態](01_for-users/10_file-specifications/06_conversation_state.md) | 中級〜上級 | 会話状態ファイル形式、メッセージ履歴管理 |
| 8 | [メッセージ構造](01_for-users/10_file-specifications/07_message_structures.md) | 中級〜上級 | メッセージ構造仕様、コンテンツタイプ、ツール呼び出し |

**次のステップ**: ファイル仕様を理解したら、[ベストプラクティス](#ベストプラクティス6文書)で効果的な使い方を学びましょう。

#### ベストプラクティス（6文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/04_best-practices/README.md) | 中級 | ベストプラクティスセクションの概要 |
| 2 | [設定のベストプラクティス](01_for-users/04_best-practices/01_configuration.md) | 中級 | Agent設定、MCP設定、セキュリティ、パフォーマンス最適化 |
| 3 | [セキュリティ](01_for-users/04_best-practices/02_security.md) | 中級〜上級 | ツール権限管理、認証情報管理、最小権限原則 |
| 4 | [パフォーマンス最適化](01_for-users/04_best-practices/03_performance.md) | 中級 | コンテキスト管理、MCP最適化、レスポンス時間改善 |
| 5 | [実践的ユースケース](01_for-users/04_best-practices/04_use-cases.md) | 初級〜中級 | 1日の作業フロー、プロジェクト別設定テンプレート、実践Tips |
| 6 | [k6負荷テスト自動化](01_for-users/04_best-practices/05_load-testing-with-k6.md) | 中級〜上級 | Playwright MCP + k6、シナリオキャプチャ、スクリプト生成、自動分析 |

**次のステップ**: 問題が発生した場合は、[トラブルシューティング](#トラブルシューティング3文書)を参照してください。

#### トラブルシューティング（3文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/06_troubleshooting/README.md) | 初級〜中級 | トラブルシューティングセクションの概要 |
| 2 | [よくある問題](01_for-users/06_troubleshooting/02_common-issues.md) | 初級〜中級 | 15の一般的問題、診断コマンド、高度なトラブルシューティング |
| 3 | [FAQ](01_for-users/06_troubleshooting/01_faq.md) | 初級 | よくある質問と回答、カテゴリ別整理 |

---

### 🔧 Developer Guide（開発者向け）- 全9文書

Amazon Q CLIの内部構造を理解したい方、コントリビューションしたい方向けのガイドです。

#### アーキテクチャ（5文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](02_for-developers/02_architecture/README.md) | 上級 | アーキテクチャセクションの概要 |
| 2 | [アーキテクチャ概要](02_for-developers/02_architecture/01_overview.md) | 上級 | システム全体像、コンポーネント構成、アーキテクチャ図 |
| 3 | [設定システム](02_for-developers/02_architecture/02_configuration-system.md) | 上級 | 設定システムの内部実装、優先順位処理、読み込みフロー |
| 4 | [ソースコード構造](02_for-developers/02_architecture/03_source-code-structure.md) | 上級 | ソースコード構造マップ、設定関連ファイル、クラス図、シーケンス図 |
| 5 | [コード統計](02_for-developers/02_architecture/04_code-statistics.md) | 上級 | 263k行Rust、8クレート、TOP5モジュール分析 |

#### コントリビューション（3文書）

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](02_for-developers/01_contributing/README.md) | 上級 | コントリビューションセクションの概要 |
| 2 | [開発環境セットアップ](02_for-developers/01_contributing/01_development-setup.md) | 上級 | 開発環境構築、ビルド方法、テスト実行 |
| 3 | [プルリクエストガイド](02_for-developers/01_contributing/02_pull-request-guide.md) | 上級 | PR作成手順、レビュー基準、マージプロセス |

---

### 📚 Reference（リファレンス）- 全11文書

詳細な仕様や完全なリストを確認したい方向けのリファレンスです。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](01_for-users/07_reference/README.md) | 中級 | Referenceセクションの概要 |
| 2 | [設定項目リファレンス](01_for-users/07_reference/03_settings-reference.md) | 中級〜上級 | 全35設定項目、カテゴリ別分類（テレメトリ/チャット/Knowledge/MCP） |
| 3 | [設定ファイル配置マップ](01_for-users/07_reference/04_configuration-file-locations.md) | 中級 | 5種類の設定ファイル配置マップ、ディレクトリ構造、実践例 |
| 4 | [環境変数リファレンス](01_for-users/03_configuration/06_environment-variables.md) | 中級〜上級 | 全環境変数リスト、Q CLI固有18項目、AWS/システム変数 |
| 5 | [サポート環境](01_for-users/07_reference/05_supported-environments.md) | 初級〜中級 | 対応OS、アーキテクチャ、システム要件、サポートされるターミナル |
| 6 | [コマンドリファレンス](01_for-users/07_reference/02_commands.md) | 初級〜中級 | 全コマンドリスト、サブコマンド、オプション |
| 7 | [用語集](01_for-users/07_reference/01_glossary.md) | 初級 | Amazon Q CLI用語集、Agent/MCP/Knowledge等の定義（33用語） |
| 8 | [完全版用語辞書](01_for-users/07_reference/06_terminology-dictionary.md) | 中級 | 公式リポジトリから抽出した全用語（322用語） |
| 9 | [コンテキストウィンドウ制限](01_for-users/07_reference/07_context-window-limits.md) | 中級 | モデル別トークン制限、コンテキスト管理の重要性 |
| 10 | [クイックリファレンス](01_for-users/07_reference/08_quick-reference.md) | 初級〜中級 | よく使うコマンドと設定の早見表、トラブルシューティング |
| 11 | [トピック別インデックス](01_for-users/07_reference/09_topic-index.md) | 初級〜中級 | やりたいことから適切なドキュメントを発見、トピック別分類 |

---

### 📰 Updates（アップデート情報）- 全5文書

最新の変更やロードマップを確認したい方向けの情報です。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](03_for-community/01_updates/README.md) | 初級〜中級 | Updatesセクションの概要 |
| 2 | [変更履歴](03_for-community/01_updates/01_changelog.md) | 初級〜中級 | バージョン別変更履歴、機能追加/バグ修正 |
| 3 | [ロードマップ](03_for-community/01_updates/02_roadmap.md) | 中級〜上級 | 開発計画、35アイテム、優先順位マトリクス、エンタープライズ課題 |
| 4 | [バージョン履歴 v1.13-latest](03_for-community/01_updates/03_version-history-v1.13-latest.md) | 中級 | v1.13-v1.18.1詳細履歴、200+ PRs、主要機能進化 |
| 5 | [マイグレーションガイド](03_for-community/01_updates/04_migration-guides.md) | 中級 | バージョン間の移行ガイド、破壊的変更への対応 |

---

### 👥 Community（コミュニティ）- 全4文書

コミュニティリソースや活用事例を知りたい方向けの情報です。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](03_for-community/02_community/README.md) | 初級 | Communityセクションの概要 |
| 2 | [コントリビューションガイド](03_for-community/02_community/03_contributing.md) | 中級 | コミュニティへの貢献方法、PR作成手順 |
| 3 | [リソース集](03_for-community/02_community/02_resources.md) | 初級〜中級 | 関連リンク、公式リソース、コミュニティツール |
| 4 | [ショーケース](03_for-community/02_community/01_showcase.md) | 初級〜中級 | 活用事例、ユースケース紹介 |

---

### 📊 Analysis（分析レポート）- 全4文書

詳細な分析レポートを確認したい方向けの情報です。

| # | ドキュメント | 対象ユーザー | 主な内容 |
|---|------------|------------|---------|
| 1 | [README](03_for-community/03_analysis/README.md) | 中級〜上級 | Analysisセクションの概要 |
| 2 | [ロードマップ分析](03_for-community/03_analysis/01_roadmap-analysis-20251008.md) | 中級〜上級 | 35件のRoadmapアイテム分析、優先順位マトリクス、エンタープライズ採用への障壁 |
| 3 | [ソースコード構造分析](03_for-community/03_analysis/03_source-code-structure.md) | 上級 | ソースコード構造の詳細分析、設定システムの実装 |
| 4 | [コード規模分析](03_for-community/03_analysis/02_source-code-scale-analysis.md) | 上級 | プロジェクト規模統計、言語別コード量、モジュール分析 |

---

## 🔍 ドキュメントの探し方

### 目的別ガイド

| やりたいこと | 参照先 | 文書数 |
|------------|--------|--------|
| Amazon Q CLIを始めたい | [Getting Started](01_for-users/01_getting-started/) | 5文書 |
| 設定を変更したい | [設定ガイド](01_for-users/03_configuration/) | 8文書 |
| 特定の機能を使いたい | [機能ガイド](01_for-users/02_features/) | 8文書 |
| **Q CLIの応答品質を最大化したい【重要】** | [コンテキスト管理ガイド](01_for-users/08_guides/) | 9文書 |
| 問題を解決したい | [トラブルシューティング](01_for-users/06_troubleshooting/) | 3文書 |
| 詳細な仕様を知りたい | [リファレンス](01_for-users/07_reference/) | 7文書 |
| コントリビューションしたい | [Developer Guide](02_for-developers/) | 9文書 |

---

## 📊 ドキュメント統計

### カテゴリ別文書数

| カテゴリ | 文書数 | 対象ユーザー |
|---------|--------|------------|
| Getting Started | 5 | 初級 |
| User Guide - Configuration | 9 | 初級〜中級 |
| User Guide - Features | 8 | 初級〜上級 |
| User Guide - Context Management | 9 | 初級〜上級 |
| User Guide - Best Practices | 6 | 中級〜上級 |
| User Guide - Deployment | 4 | 中級〜上級 |
| User Guide - Security | 7 | 初級〜上級 |
| User Guide - Troubleshooting | 3 | 初級〜中級 |
| User Guide - Reference | 8 | 初級〜上級 |
| Developer Guide - Architecture | 5 | 上級 |
| Developer Guide - Contributing | 4 | 上級 |
| Community - Updates | 5 | 初級〜上級 |
| Community - Community | 4 | 初級〜中級 |
| Community - Analysis | 4 | 中級〜上級 |
| Issues | 1 | 中級〜上級 |
| Meta | 5 | 中級〜上級 |
| Top Level | 4 | - |
| **合計** | **91** | - |

### 対象ユーザー別文書数

- **初級向け**: 15文書
- **中級向け**: 28文書
- **上級向け**: 12文書
- **全レベル**: 23文書

---

## 📌 重要なリンク

### 公式リソース
- **GitHub リポジトリ**: https://github.com/aws/amazon-q-developer-cli
- **AWS 公式サイト**: https://aws.amazon.com/q/developer/

### よく使うドキュメント
- [クイックスタート](01_for-users/01_getting-started/02_quick-start.md) - 5分で始める
- [Agent設定](01_for-users/03_configuration/03_agent-configuration.md) - Agent設定の詳細
- [よくある問題](01_for-users/06_troubleshooting/02_common-issues.md) - トラブルシューティング
- [設定項目リファレンス](01_for-users/07_reference/03_settings-reference.md) - 全設定項目

---

## 🤝 コントリビューション

このドキュメントへの貢献を歓迎します！

- **誤字・脱字の修正**: 気軽にPRを送ってください
- **内容の改善**: より良い説明や例があれば提案してください
- **新しいドキュメント**: 不足している情報があれば追加してください

詳細は [コントリビューションガイド](02_for-developers/01_contributing/README.md) をご覧ください。

---

## 📝 ドキュメントのバージョン

このドキュメントは、Amazon Q Developer CLI v1.17.0以降を対象としています。古いバージョンをお使いの場合、一部の機能や設定が異なる可能性があります。

最新バージョンへのアップデート方法は [インストールガイド](01_for-users/01_getting-started/01_installation.md) をご覧ください。

---

## 💡 ヒント

- **検索機能**: ブラウザの検索機能（Ctrl+F / Cmd+F）を使って、キーワードで情報を探せます
- **目次**: 各ドキュメントには目次があり、必要な情報に素早くアクセスできます
- **リンク**: 関連するドキュメントへのリンクが豊富にあります
- **対象ユーザー**: 各ドキュメントには対象ユーザーレベルが記載されています

---

## 🔗 外部リンク

### AWS関連リンク

- **[AWS Labs MCP](https://github.com/awslabs/mcp)** - AWS公式MCPサーバー集（最新情報）
- **[AWS Developer Tutorials](https://github.com/aws-samples/sample-developer-tutorials)** - AWS CLIスクリプト集（Q CLIでスクリプト生成可能）
- **[Amazon Q Developer CLI](https://github.com/aws/amazon-q-developer-cli)** - 公式GitHubリポジトリ
- **[Amazon Q Developer](https://aws.amazon.com/q/developer/)** - 公式サイト

---
最終更新: 2025-11-15
