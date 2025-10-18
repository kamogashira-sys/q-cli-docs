[ホーム](README.md)

---

# 📁 ファイル構造

このページでは、Amazon Q CLI ドキュメントサイトの完全なファイル構造を示します。

**総ドキュメント数**: 95ファイル

---

## ディレクトリ構造

```
docs/
├── 01_for-users/                      # ユーザーガイド（65文書）
│   ├── 01_getting-started/            # 入門ガイド（5文書）
│   │   ├── 01_installation.md
│   │   ├── 02_quick-start.md
│   │   ├── 03_first-steps.md
│   │   ├── 04_pricing.md
│   │   └── README.md
│   ├── 02_features/                   # 機能ガイド（8文書）
│   │   ├── 01_chat.md
│   │   ├── 02_agents.md
│   │   ├── 03_autocomplete.md
│   │   ├── 04_keyboard-shortcuts.md
│   │   ├── 05_checkpoints.md
│   │   ├── 06_ssh-remote.md
│   │   ├── 07_experimental.md
│   │   └── README.md
│   ├── 03_configuration/              # 設定ガイド（9文書）
│   │   ├── 01_overview.md
│   │   ├── 02_priority-rules.md
│   │   ├── 03_global-settings.md
│   │   ├── 04_agent-configuration.md
│   │   ├── 05_environment-variables.md
│   │   ├── 06_mcp-configuration.md
│   │   ├── 06_telemetry.md
│   │   ├── 07_examples.md
│   │   └── README.md
│   ├── 04_best-practices/             # ベストプラクティス（6文書）
│   │   ├── 01_configuration.md
│   │   ├── 02_security.md
│   │   ├── 03_performance.md
│   │   ├── 04_use-cases.md
│   │   ├── 05_load-testing-with-k6.md
│   │   └── README.md
│   ├── 05_deployment/                 # デプロイメント（4文書）
│   │   ├── 01_enterprise-deployment.md
│   │   ├── 02_pricing-comparison.md
│   │   ├── 03_security-checklist.md
│   │   └── README.md
│   ├── 06_troubleshooting/            # トラブルシューティング（3文書）
│   │   ├── 01_faq.md
│   │   ├── 02_common-issues.md
│   │   └── README.md
│   ├── 07_reference/                  # リファレンス（10文書）
│   │   ├── 01_glossary.md
│   │   ├── 02_commands.md
│   │   ├── 03_settings-reference.md
│   │   ├── 04_configuration-file-locations.md
│   │   ├── 05_supported-environments.md
│   │   ├── 06_terminology-dictionary.md
│   │   ├── 07_context-window-limits.md
│   │   ├── 08_quick-reference.md
│   │   ├── 09_topic-index.md
│   │   └── README.md
│   ├── 08_guides/                     # コンテキスト管理ガイド（9文書）
│   │   ├── 01_essence.md
│   │   ├── 02_mechanism.md
│   │   ├── 03_effects.md
│   │   ├── 04_best-practices.md
│   │   ├── 05_practical-guide.md
│   │   ├── 06_troubleshooting.md
│   │   ├── 07_advanced.md
│   │   ├── 08_reference.md
│   │   └── README.md
│   ├── 09_security/                   # セキュリティ（7文書）
│   │   ├── 01_security-overview.md
│   │   ├── 02_data-privacy.md
│   │   ├── 03_file-access-control.md
│   │   ├── 04_aws-api-control.md
│   │   ├── 05_credentials-management.md
│   │   ├── 06_trust-all-safety.md
│   │   └── README.md
│   └── README.md
│
├── 02_for-developers/                 # 開発者ガイド（7文書）
│   ├── 01_contributing/               # コントリビューション（3文書）
│   │   ├── 01_development-setup.md
│   │   ├── 02_pull-request-guide.md
│   │   └── README.md
│   ├── 02_architecture/               # アーキテクチャ（5文書）
│   │   ├── 01_overview.md
│   │   ├── 02_configuration-system.md
│   │   ├── 03_source-code-structure.md
│   │   ├── 04_code-statistics.md
│   │   └── README.md
│   └── README.md
│
├── 03_for-community/                  # コミュニティ（13文書）
│   ├── 01_updates/                    # アップデート情報（5文書）
│   │   ├── 01_changelog.md
│   │   ├── 02_roadmap.md
│   │   ├── 03_version-history-v1.13-latest.md
│   │   ├── 04_migration-guides.md
│   │   └── README.md
│   ├── 02_community/                  # コミュニティ（4文書）
│   │   ├── 01_showcase.md
│   │   ├── 02_resources.md
│   │   ├── 03_contributing.md
│   │   └── README.md
│   ├── 03_analysis/                   # 分析レポート（4文書）
│   │   ├── 01_roadmap-analysis-20251008.md
│   │   ├── 02_source-code-scale-analysis.md
│   │   ├── 03_source-code-structure.md
│   │   └── README.md
│   └── README.md
│
├── 05_meta/                           # メタドキュメント（5文書）
│   ├── CONTRIBUTING.md
│   ├── IMPLEMENTATION_VERIFICATION_CHECKLIST.md
│   ├── QUALITY_ASSURANCE.md
│   │   README.md
│   └── VERIFICATION_CHECKLIST.md
│
├── README.md                          # トップページ
├── index.md                           # GitHub Pagesトップ
├── quick-reference.md                 # クイックリファレンス
├── topic-index.md                     # トピック別インデックス
├── _config.yml                        # Jekyll設定
├── Gemfile                            # Ruby依存関係
└── robots.txt                         # クローラー設定
```

---

## カテゴリ別統計

| カテゴリ | ディレクトリ数 | ファイル数 | 主な内容 |
|---------|--------------|-----------|---------|
| **ユーザーガイド** | 9 | 65 | 入門、機能、設定、ベストプラクティス、セキュリティ |
| **開発者ガイド** | 2 | 7 | コントリビューション、アーキテクチャ |
| **コミュニティ** | 3 | 13 | アップデート、コミュニティ、分析 |
| **メタ** | 1 | 5 | 品質保証、検証チェックリスト |
| **ルート** | - | 5 | トップページ、インデックス、設定 |
| **合計** | 15 | 95 | - |

---

## 主要ディレクトリの説明

### 01_for-users/
Q CLIを使用するユーザー向けのドキュメント。インストールから高度な活用方法まで網羅。

- **01_getting-started/**: 初めてQ CLIを使う方向けの入門ガイド
- **02_features/**: チャット、Agent、オートコンプリートなどの機能説明
- **03_configuration/**: 設定ファイル、環境変数、MCPの設定方法
- **04_best-practices/**: 効果的な使い方とパフォーマンス最適化
- **05_deployment/**: エンタープライズ環境での展開ガイド
- **06_troubleshooting/**: よくある問題と解決方法
- **07_reference/**: コマンド、設定項目、用語集などのリファレンス
- **08_guides/**: コンテキスト管理の完全ガイド（全8章）
- **09_security/**: セキュリティとプライバシーの詳細

### 02_for-developers/
Q CLIの開発に貢献したい方向けのドキュメント。

- **01_contributing/**: 開発環境のセットアップとPRガイド
- **02_architecture/**: システムアーキテクチャとソースコード構造

### 03_for-community/
コミュニティ向けの情報とアップデート。

- **01_updates/**: バージョン履歴、ロードマップ、変更履歴
- **02_community/**: ショーケース、リソース、コントリビューション
- **03_analysis/**: ロードマップ分析、ソースコード規模分析

### 05_meta/
ドキュメント品質管理とプロジェクト運営に関するメタ情報。

---

## 関連ページ

- [ドキュメントサイトトップ](README.md)
- [クイックリファレンス](01_for-users/07_reference/08_quick-reference.md)
- [トピック別インデックス](01_for-users/07_reference/09_topic-index.md)

---

**最終更新**: 2025-10-19
