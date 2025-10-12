# 変更履歴（Changelog）

このページでは、Amazon Q CLIの主要なバージョンアップデートと変更内容を記録しています。

## 📋 目次

- [最新バージョン](#最新バージョン)
- [バージョン履歴](#バージョン履歴)
- [変更カテゴリについて](#変更カテゴリについて)

---

## 最新バージョン

### v1.17.1（2025-10-01）

**主要な変更**:
- 🔧 **内部改善**: モデルに説明（description）を追加
- 📝 **コードの可読性向上**: コードの保守性を改善

**詳細**: [v1.17.1リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.17.1)

---

## バージョン履歴

### v1.17.0（2025-09-29）

**主要な変更**:
- 🎉 **Knowledge機能のベータ改善**: BM25検索アルゴリズムのサポート追加
- 🔧 **MCP統合の強化**: リモートMCPサーバーのサポート改善
- 🛡️ **セキュリティ強化**: `execute_bash`権限の厳格化
- 🐛 **バグ修正**: 複数の安定性向上

**詳細**: [v1.17.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.17.0)

### v1.16.0（2025-09-15）

**Agent機能の成熟化**:
- Agent設定スキーマの改善
- Agent管理コマンドの追加（`q agent list`, `q agent edit`）
- Agent設定の検証機能強化

**MCP進化**:
- rmcpへの移行完了
- OAuth統合の初期サポート
- リモートMCPサーバーの実験的サポート

**詳細**: [v1.16.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.16.0)

---

### v1.15.0（2025-08-31）

**Knowledge機能の改善**:
- Knowledge Baseの検索精度向上
- ファイルインデックス作成の高速化
- 検索結果のランキング改善

**パフォーマンス最適化**:
- チャット応答速度の向上
- メモリ使用量の削減
- 起動時間の短縮

**詳細**: [v1.15.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.15.0)

---

### v1.14.0（2025-08-15）

**セキュリティ強化**:
- ツール権限システムの改善
- `fs_read`の制限強化
- 環境変数の安全な取り扱い

**UX改善**:
- エラーメッセージの改善
- プログレス表示の追加
- ヘルプテキストの充実

**詳細**: [v1.14.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.14.0)

---

### v1.13.0（2025-07-31）

**Agent機能の導入**:
- カスタムAgent設定のサポート
- Agent固有のツール権限設定
- Agent切り替え機能（`q chat --agent <name>`、`q agent set-default`）

**MCP統合の開始**:
- Model Context Protocol (MCP)のサポート開始
- MCPサーバー設定の追加
- stdio/HTTP transportのサポート

**詳細**: [v1.13.0リリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/v1.13.0)

---

## 変更カテゴリについて

### 🎉 新機能（Features）
新しい機能の追加や既存機能の大幅な拡張

### 🔧 改善（Improvements）
既存機能のパフォーマンス向上や使いやすさの改善

### 🛡️ セキュリティ（Security）
セキュリティ関連の修正や強化

### 🐛 バグ修正（Bug Fixes）
不具合の修正

### 📚 ドキュメント（Documentation）
ドキュメントの追加や改善

### ⚠️ 破壊的変更（Breaking Changes）
既存の動作を変更する可能性のある変更

---

## 📚 関連ドキュメント

- [ロードマップ](02_roadmap.md) - 今後の開発計画
- [マイグレーションガイド](04_migration-guides.md) - バージョン間の移行方法
- [GitHub Releases](https://github.com/aws/amazon-q-developer-cli/releases) - 公式リリースノート

---

## 🔄 更新頻度

このChangelogは以下のタイミングで更新されます：
- 新しいバージョンのリリース時
- 重要なバグ修正のリリース時
- セキュリティアップデートのリリース時

最終更新: 2025-10-09
