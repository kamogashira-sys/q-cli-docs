[ホーム](README.md) > Topic Index

---

# トピック別インデックス

**最終更新**: 2025-10-18

このページでは、トピックごとにドキュメントを整理しています。やりたいことから適切なドキュメントを見つけることができます。

---

## 目次

- [セキュリティ](#-セキュリティ)
- [設定](#️-設定)
- [機能](#-機能)
- [コンテキスト管理](#-コンテキスト管理)
- [トラブルシューティング](#-トラブルシューティング)
- [エンタープライズ](#-エンタープライズ)
- [開発者向け](#-開発者向け)

---

## 🔐 セキュリティ

### 基本

- **[セキュリティ概要](01_for-users/09_security/01_security-overview.md)** - AWS責任共有モデル、主要セキュリティトピック、環境別推奨設定
- **[データプライバシー](01_for-users/09_security/02_data-privacy.md)** - Free vs Pro/Enterpriseプラン、サービス改善データ使用、オプトアウト

### ツール制御

- **[ファイルアクセス制御](01_for-users/09_security/03_file-access-control.md)** - fs_readツール制御、機密ファイル保護、環境別設定
- **[AWS API制御](01_for-users/09_security/04_aws-api-control.md)** - use_awsツール制御、IAMポリシー制限、コスト管理

### 認証・権限

- **[認証情報管理](01_for-users/09_security/05_credentials-management.md)** - AWS Builder ID、IAM Identity Center、ベストプラクティス、暗号化
- **[trust-all安全使用](01_for-users/09_security/06_trust-all-safety.md)** - trust-allの危険性、安全な使用方法、チェックリスト

### ベストプラクティス

- **[セキュリティベストプラクティス](01_for-users/04_best-practices/02_security.md)** - ツール権限管理、認証情報管理、最小権限原則

---

## ⚙️ 設定

### 基本設定

- **[設定システム概要](01_for-users/03_configuration/01_overview.md)** - 設定システム全体像、5段階優先順位、4種類の設定
- **[優先順位ルール](01_for-users/03_configuration/07_priority-rules.md)** - 5段階優先順位の詳細、フロー図
- **[グローバル設定](01_for-users/03_configuration/02_global-settings.md)** - settings.json、35項目（テレメトリ/チャット/Knowledge/デフォルトAgent）

### 高度な設定

- **[Agent設定](01_for-users/03_configuration/03_agent-configuration.md)** - JSONスキーマ、グローバル/ローカルAgent、必須/オプションフィールド、検証方法
- **[MCP設定](01_for-users/03_configuration/04_mcp-configuration.md)** - MCPサーバー設定、stdio/HTTP接続、OAuth認証、環境変数展開
- **[環境変数](01_for-users/03_configuration/06_environment-variables.md)** - 23項目、Q CLI固有18項目、設定方法、実践パターン
- **[テレメトリー設定](01_for-users/03_configuration/05_telemetry.md)** - テレメトリー制御、プライバシー保護、無効化方法

### 実践例

- **[設定例集](01_for-users/03_configuration/08_examples.md)** - 実践的な設定例、ユースケース別（開発/本番/チーム）
- **[設定のベストプラクティス](01_for-users/04_best-practices/01_configuration.md)** - Agent設定、MCP設定、セキュリティ、パフォーマンス最適化

---

## 🎯 機能

### 基本機能

- **[チャット機能](01_for-users/02_features/01_chat.md)** - 基本操作、チャットコマンド（/help, /agent, /context）、Tips
- **[オートコンプリート](01_for-users/02_features/03_autocomplete.md)** - オートコンプリート機能、設定、使い方
- **[キーボードショートカット](01_for-users/02_features/04_keyboard-shortcuts.md)** - ショートカット一覧、Tangent/Skim/Delegateモード、カスタマイズ

### 高度な機能

- **[Agent機能](01_for-users/02_features/02_agents.md)** - Agent概要、管理コマンド（list/切り替え）、カスタマイズ項目
- **[Checkpoint機能](01_for-users/02_features/05_checkpoints.md)** - チェックポイント機能、保存/復元、自動保存設定
- **[SSH/リモート接続](01_for-users/02_features/06_ssh-remote.md)** - リモート環境での使用、SSH接続、設定方法
- **[実験的機能](01_for-users/02_features/07_experimental.md)** - 実験的機能、Delegate Mode、安全性警告、ベストプラクティス

---

## 🎯 コンテキスト管理

### 基礎（初級〜中級）

- **[本質編](01_for-users/08_guides/01_essence.md)** - コンテキストとは何か、なぜ重要か、基本概念（15分）
- **[仕組み編](01_for-users/08_guides/02_mechanism.md)** - 内部動作の理解、3つの提供方法、処理フロー（20分）
- **[効果編](01_for-users/08_guides/03_effects.md)** - 何ができるか、Agent Resources/Session Context/Knowledge Bases（15分）

### 実践（中級）

- **[ベストプラクティス編](01_for-users/08_guides/04_best-practices.md)** - 設計原則、アプローチ選択、実装パターン、最適化（45分）
- **[実践ガイド編](01_for-users/08_guides/05_practical-guide.md)** - プロジェクト別実装例、基本/応用パターン、アンチパターン（30分）

### 高度（中級〜上級）

- **[トラブルシューティング編](01_for-users/08_guides/06_troubleshooting.md)** - 問題診断、一般的な問題、デバッグ技法（20分）
- **[上級編](01_for-users/08_guides/07_advanced.md)** - 最適化戦略、チーム開発、内部実装の理解（20分）
- **[リファレンス編](01_for-users/08_guides/08_reference.md)** - コマンドリファレンス、技術仕様、用語集、FAQ（15分）

---

## 🚨 トラブルシューティング

### 一般的な問題

- **[よくある問題](01_for-users/06_troubleshooting/02_common-issues.md)** - 15の一般的問題、診断コマンド、高度なトラブルシューティング
- **[FAQ](01_for-users/06_troubleshooting/01_faq.md)** - よくある質問と回答、カテゴリ別整理

### 専門的なトラブルシューティング

- **[コンテキスト管理トラブルシューティング](01_for-users/08_guides/06_troubleshooting.md)** - コンテキスト関連の問題診断、解決方法

---

## 🏢 エンタープライズ

### 導入

- **[エンタープライズ導入ガイド](01_for-users/05_deployment/01_enterprise-deployment.md)** - IAM Identity Center、組織導入、Pro契約、段階的ロールアウト、セキュリティ
- **[料金プラン比較](01_for-users/05_deployment/02_pricing-comparison.md)** - Free/Pro/Enterpriseプラン比較、データ使用ポリシー、推奨環境
- **[セキュリティチェックリスト](01_for-users/05_deployment/03_security-checklist.md)** - エンタープライズ導入時のセキュリティチェック項目、ツール権限管理

### ベストプラクティス

- **[実践的ユースケース](01_for-users/04_best-practices/04_use-cases.md)** - 1日の作業フロー、プロジェクト別設定テンプレート、実践Tips
- **[k6負荷テスト自動化](01_for-users/04_best-practices/05_load-testing-with-k6.md)** - Playwright MCP + k6、シナリオキャプチャ、スクリプト生成、自動分析
- **[パフォーマンス最適化](01_for-users/04_best-practices/03_performance.md)** - コンテキスト管理、MCP最適化、レスポンス時間改善

---

## 🔧 開発者向け

### アーキテクチャ

- **[アーキテクチャ概要](02_for-developers/02_architecture/01_overview.md)** - システム全体像、コンポーネント構成、アーキテクチャ図
- **[設定システム](02_for-developers/02_architecture/02_configuration-system.md)** - 設定システムの内部実装、優先順位処理、読み込みフロー
- **[ソースコード構造](02_for-developers/02_architecture/03_source-code-structure.md)** - ソースコード構造マップ、設定関連ファイル、クラス図、シーケンス図
- **[コード統計](02_for-developers/02_architecture/04_code-statistics.md)** - 263k行Rust、8クレート、TOP5モジュール分析

### コントリビューション

- **[開発環境セットアップ](02_for-developers/01_contributing/01_development-setup.md)** - 開発環境構築、ビルド方法、テスト実行
- **[プルリクエストガイド](02_for-developers/01_contributing/02_pull-request-guide.md)** - PR作成手順、レビュー基準、マージプロセス

### 分析レポート

- **[ロードマップ分析](03_for-community/03_analysis/01_roadmap-analysis-20251008.md)** - 35件のRoadmapアイテム分析、優先順位マトリクス、エンタープライズ採用への障壁
- **[ソースコード構造分析](03_for-community/03_analysis/03_source-code-structure.md)** - ソースコード構造の詳細分析、設定システムの実装
- **[コード規模分析](03_for-community/03_analysis/02_source-code-scale-analysis.md)** - プロジェクト規模統計、言語別コード量、モジュール分析

---

## 🔗 その他のインデックス

- **[クイックリファレンス](quick-reference.md)** - よく使うコマンドと設定
- **[ドキュメント一覧](README.md)** - 全ドキュメントの一覧（カテゴリ別、対象ユーザー別）

---

## 💡 使い方のヒント

### 目的から探す

1. **Q CLIを始めたい** → [Getting Started](01_for-users/01_getting-started/README.md)
2. **設定を変更したい** → [設定](#️-設定)セクション
3. **特定の機能を使いたい** → [機能](#-機能)セクション
4. **応答品質を最大化したい** → [コンテキスト管理](#-コンテキスト管理)セクション
5. **問題を解決したい** → [トラブルシューティング](#-トラブルシューティング)セクション
6. **組織で導入したい** → [エンタープライズ](#-エンタープライズ)セクション

### 学習パス

**初心者向け**:
1. Getting Started → 機能 → 設定 → コンテキスト管理（基礎）

**中級者向け**:
1. コンテキスト管理（実践） → ベストプラクティス → セキュリティ

**上級者向け**:
1. コンテキスト管理（高度） → エンタープライズ → 開発者向け

---

**最終更新**: 2025-10-18  
**対象バージョン**: v1.17.0以降
