[ホーム](../../README.md) > [コミュニティ](../README.md) > [アップデート情報](README.md) > 02 Roadmap

---

# ロードマップ

Amazon Q CLIの開発ロードマップと今後の計画について説明します。

## 📋 目次

- [概要](#概要)
- [優先度の高い機能](#優先度の高い機能)
- [進行中の機能](#進行中の機能)
- [計画中の機能](#計画中の機能)
- [完了した機能](#完了した機能)

---

## 概要

### ロードマップの状況
- **総アイテム数**: 35件
- **オープン**: 28件
- **クローズド**: 7件
- **完了率**: 20%

### 最終更新
2025-10-09（元データ: 2025-10-08分析）

---

## 優先度の高い機能

| # | 機能 | ステータス | 優先度 | 主な影響 | ISSUE |
|---|------|-----------|--------|---------|-------|
| 1 | **Windows Support** | 🔴 オープン | 🔥 最高 | • エンタープライズ採用の主要ブロッカー<br>• 多くのエンタープライズ環境はWindows中心 | [#2602](https://github.com/aws/amazon-q-developer-cli/issues/2602) |
| 2 | **Remote MCP Servers** | 🔴 オープン | 🔥 最高 | • エンタープライズツールとの統合に必須<br>• OAuth統合と組み合わせて使用 | [#2706](https://github.com/aws/amazon-q-developer-cli/issues/2706) |
| 3 | **UX Rewrite using Ratatui** | 🔴 オープン | ⚡ 高 | • 実質的な「Q v2」<br>• ユーザー体験の大幅改善 | [#2550](https://github.com/aws/amazon-q-developer-cli/issues/2550) |
| 4 | **ADC Support** | 🔴 オープン | ⚡ 高 | • エンタープライズネットワーク環境での制限解消<br>• 認証の簡素化 | [#2600](https://github.com/aws/amazon-q-developer-cli/issues/2600) |

---

## 進行中の機能

### Agent機能の成熟化
- Agent設定スキーマの改善
- Agent管理コマンドの拡充
- Agent間の切り替え機能

### MCP統合の強化
- rmcpへの完全移行
- OAuth統合の完成
- リモートMCPサーバーの安定化

### Knowledge機能の改善
- BM25検索アルゴリズムの最適化
- インデックス作成の高速化
- 検索精度の向上

---

## 計画中の機能

### セキュリティ強化
- ツール権限の細粒度制御
- 監査ログ機能
- セキュリティポリシーの強化

### パフォーマンス最適化
- 起動時間の短縮
- メモリ使用量の削減
- 応答速度の向上

### エンタープライズ機能
- 使用状況の可視化
- 管理者ダッシュボード
- チーム設定の共有

### 多言語対応
- UI/UXの国際化
- ドキュメントの多言語化
- エラーメッセージの翻訳

---

## 完了した機能

### v1.18.1（2025-10-14）
- ✅ バージョン報告の修正

### v1.18.0（2025-10-13）
- ✅ Delegate Tool（実験的機能）
- ✅ Stop Hook機能
- ✅ Knowledge コマンド統合
- ✅ PDF対応（Knowledge）
- ✅ file:// URI対応（Agent prompts）
- ✅ `/logdump` コマンド
- ✅ Experiment Manager強化
- ✅ MCP Prompts改善

### v1.17.0（2025-09-29）
- ✅ Knowledge機能のBM25サポート
- ✅ セキュリティ強化（execute_bash権限）
- ✅ MCP統合の改善

### v1.16.0（2025-09-15）
- ✅ Agent機能の成熟化
- ✅ rmcpへの移行
- ✅ OAuth統合の初期サポート

### v1.15.0（2025-09-02）

> **注**: GitHubのタグ名は`v.1.15.0`（ドット付き）

- ✅ Knowledge機能の改善
- ✅ パフォーマンス最適化
- ✅ 検索精度向上

### v1.14.0（2025-08-15）
- ✅ セキュリティ強化
- ✅ UX改善
- ✅ エラーメッセージ改善

### v1.13.0（2025-07-31）
- ✅ Agent機能の導入
- ✅ MCP統合の開始
- ✅ Agent切り替え機能

---

## エンタープライズ採用への課題

### 主要ブロッカー
1. **Windows未対応** - 多くのエンタープライズ環境はWindows中心
2. **リモートMCP + OAuth未完成** - エンタープライズツールとの統合困難
3. **ADC未対応** - エンタープライズネットワーク環境での制限
4. **管理機能の不足** - 使用状況の可視化、管理者ダッシュボード

### 解決に向けた取り組み
- Windows Supportの優先度を最高に設定
- Remote MCP Serversの開発加速
- ADC Supportの実装計画
- エンタープライズ機能の段階的追加

---

## コミュニティへの貢献

### 貢献できる領域
- バグ報告と修正
- ドキュメントの改善
- 機能リクエスト
- MCPサーバーの開発

### 貢献方法
詳細は[貢献ガイド](../../03_for-community/02_community/03_contributing.md)を参照。

---

## 📚 関連ドキュメント

- [変更履歴](01_changelog.md) - 過去のリリース情報
- [マイグレーションガイド](04_migration-guides.md) - バージョン間の移行
- [GitHub Roadmap](https://github.com/aws/amazon-q-developer-cli/issues?q=is%3Aissue+label%3Aroadmap) - 公式ロードマップ

---

## 📞 フィードバック

ロードマップに関するフィードバックや提案：
- [GitHub Discussions](https://github.com/aws/amazon-q-developer-cli/discussions)
- [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)

最終更新: 2025-10-09
