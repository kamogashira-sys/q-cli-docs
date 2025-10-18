[ホーム](../../README.md) > [開発者ガイド](../README.md) > [アーキテクチャ](README.md) > 04 Code Statistics

---

# コード統計

**分析日**: 2025-10-09  
**対象バージョン**: v1.18.0  
**リポジトリ**: https://github.com/aws/amazon-q-developer-cli

---

## 📊 概要

Amazon Q CLIは、**26万行超のRustコード**で構成される大規模なエンタープライズグレードCLIツールです。8つの独立したcrateに分割され、高度にモジュール化されています。

---

## 📈 総合統計

| 項目 | 値 |
|------|-----|
| **バージョン** | 1.18.0 |
| **主要言語** | Rust（95.8%） |
| **総Rustファイル数** | 1,873ファイル |
| **総Rust行数** | 263,043行 |
| **Crateモジュール数** | 8個 |
| **ライセンス** | MIT OR Apache-2.0 |

---

## 🗂️ 言語別統計

| 言語 | ファイル数 | 総行数 | 割合 | 用途 |
|------|-----------|--------|------|------|
| Rust | 1,873 | 263,043 | 95.8% | メインロジック |
| Python | 7 | 1,122 | 0.4% | スクリプト・ツール |
| Markdown | 20 | 3,094 | 1.1% | ドキュメント |
| TOML | 19 | - | - | 設定ファイル |
| JSON | 6 | - | - | 設定・スキーマ |

---

## 📦 Crateモジュール別規模（TOP 5）

| # | Crate名 | 行数 | 割合 | 機能 |
|---|---------|------|------|------|
| 1 | amzn-codewhisperer-client | 96,840 | 36.8% | CodeWhisperer APIクライアント |
| 2 | chat-cli | 50,389 | 19.2% | メインCLIアプリケーション |
| 3 | amzn-consolas-client | 39,870 | 15.2% | Consolas APIクライアント |
| 4 | amzn-codewhisperer-streaming-client | 31,809 | 12.1% | CodeWhispererストリーミング |
| 5 | amzn-qdeveloper-streaming-client | 28,017 | 10.6% | Q Developerストリーミング |

**その他**: semantic-search-client（9,117行）、amzn-toolkit-telemetry-client（6,683行）、aws-toolkit-telemetry-definitions（318行）

---

## 🎯 chat-cli機能別規模（TOP 5）

| # | モジュール | 行数 | 割合 | 機能説明 |
|---|-----------|------|------|---------|
| 1 | cli | 35,452 | 70.4% | CLIコマンド処理、Agent、チャット |
| 2 | api_client | 3,022 | 6.0% | APIクライアント統合 |
| 3 | util | 2,334 | 4.6% | ユーティリティ関数 |
| 4 | telemetry | 1,988 | 3.9% | テレメトリ収集・送信 |
| 5 | mcp_client | 1,526 | 3.0% | MCPクライアント実装 |

**その他**: auth（1,442行）、os（1,424行）、database（1,030行）、aws_common（569行）、theme（409行）

---

## 🛠️ 技術スタック

### 主要技術

| カテゴリ | 技術 |
|---------|------|
| **言語** | Rust Edition 2024 |
| **構成** | Workspace（8 crates） |
| **AWS SDK** | aws-config, aws-sdk-cognitoidentity, aws-sdk-ssooidc |
| **非同期** | async-trait, anstream |
| **HTTP** | aws-smithy-runtime-api |

---

## 💡 規模の特徴

### 1. エンタープライズグレード
- 26万行超の大規模実装
- 高度なモジュール化と分離

### 2. AWS統合の深さ
- CodeWhisperer、Consolas、Q Developer統合
- 複数のストリーミングクライアント

### 3. 将来性
- モジュール構造により拡張が容易
- 実験的機能の継続的追加

### 4. 品質重視
- テストコード、テレメトリ、エラーハンドリング
- エンタープライズ採用を意識した設計

---

## 📚 詳細情報

より詳細な分析は以下を参照してください：
- **[詳細分析レポート](../../03_for-community/03_analysis/02_source-code-scale-analysis.md)** - 完全な分析結果
- **[ソースコード構造](03_source-code-structure.md)** - コード構造の詳細

---

## 🔄 更新履歴

| 分析日 | バージョン | 総行数 | 備考 |
|--------|-----------|--------|------|
| 2025-10-09 | v1.18.0 | 263,043 | 初回分析 |

---

**作成日**: 2025-10-11  
最終更新: 2025-10-11
