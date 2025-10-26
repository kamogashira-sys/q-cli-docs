[ホーム](../README.md) > [Meta](README.md) > 公開リソース一覧

---

# 公開リソース一覧

本サイトで公開している品質保証関連のリソース（ツール、チェックリスト、テンプレート）の一覧です。

---

## 📂 リソース配置場所

| カテゴリ | 配置場所 | 説明 |
|---------|---------|------|
| 自動化ツール | `/06_scripts/` | 品質チェック自動化スクリプト |
| チェックリスト | `/07_templates/` | 作業品質確保用チェックリスト |
| メタドキュメント | `/docs/05_meta/` | 品質保証プロセス文書 |

---

## 🛠️ 自動化ツール（scripts/）

### 1. count-files.sh

**用途**: ファイル数の自動カウント

**機能**:
- 全ファイル数のカウント
- カテゴリ別カウント
- README除外オプション

**使用方法**:
```bash
./06_scripts/count-files.sh
```

**詳細**: [自動化ツール使用ガイド](07_automation-tools-guide.md#count-filessh)

---

### 2. check-dates.sh

**用途**: Git最終更新日とドキュメント記載日の整合性チェック

**機能**:
- Git log日付の抽出
- ドキュメント内「最終更新」日付の抽出
- 不一致の検出と報告

**使用方法**:
```bash
./06_scripts/check-dates.sh [ディレクトリパス]
```

**詳細**: [自動化ツール使用ガイド](07_automation-tools-guide.md#check-datessh)

---

### 3. search-env-var.sh

**用途**: 環境変数の使用箇所検索

**機能**:
- 環境変数名での全文検索
- 使用箇所の一覧表示
- 使用箇所数のカウント

**使用方法**:
```bash
./06_scripts/search-env-var.sh 環境変数名
```

**詳細**: [自動化ツール使用ガイド](07_automation-tools-guide.md#search-env-varsh)

---

### 4. validate_commands.sh

**用途**: ドキュメント内のコマンド例の検証

**機能**:
- コマンド構文の検証
- 実行可能性の確認

**使用方法**:
```bash
./06_scripts/validate_commands.sh
```

---

### 5. validate_config_keys.sh

**用途**: 設定ファイルのキー検証

**機能**:
- 設定キーの存在確認
- スキーマとの整合性チェック

**使用方法**:
```bash
./06_scripts/validate_config_keys.sh
```

---

## ✅ チェックリスト（templates/）

### 1. implementation_verification_checklist.md

**用途**: 実装照合チェックリスト（15項目）

**カテゴリ**:
- ソースコード確認（6項目）
- テストコード確認（4項目）
- JSON Schema確認（5項目）

**使用タイミング**:
- 新規ドキュメント作成時（必須）
- 技術情報更新時（必須）
- 設定例追加時（必須）

**詳細**: [チェックリスト活用ガイド](08_checklist-guide.md#チェックリスト1-実装照合)

---

### 2. functional_verification_checklist.md

**用途**: 動作確認チェックリスト（12項目）

**カテゴリ**:
- コマンド実行確認（4項目）
- 設定ファイル動作確認（5項目）
- 環境変数効果確認（3項目）

**使用タイミング**:
- 新規ドキュメント作成時（必須）
- 設定例追加時（必須）
- コマンド例追加時（必須）
- Q CLIバージョン更新時（推奨）

**詳細**: [チェックリスト活用ガイド](08_checklist-guide.md#チェックリスト2-動作確認)

---

### 3. deletion_operation_checklist.md

**用途**: 削除操作チェックリスト（10項目）

**カテゴリ**:
- 削除前確認（5項目）
- 削除実行（2項目）
- 削除後確認（3項目）

**使用タイミング**:
- ファイル削除時（必須）
- 環境変数削除時（必須）
- 設定項目削除時（必須）
- リンク削除時（推奨）

**詳細**: [チェックリスト活用ガイド](08_checklist-guide.md#チェックリスト3-削除操作)

---

### 4. document_quality_checklist.md

**用途**: 文書品質チェックリスト（13項目）

**カテゴリ**:
- リンクチェック（4項目）
- フォーマット確認（5項目）
- 内容確認（4項目）

**使用タイミング**:
- 全ての作業完了時（必須）
- 定期チェック時（推奨）

**詳細**: [チェックリスト活用ガイド](08_checklist-guide.md#チェックリスト4-文書品質)

---

## 📚 メタドキュメント（docs/05_meta/）

### コントリビューション・品質保証

| # | ドキュメント | 内容 |
|---|-------------|------|
| 01 | [CONTRIBUTING.md](01_CONTRIBUTING.md) | コントリビューションガイドライン |
| 02 | [QUALITY_ASSURANCE.md](02_QUALITY_ASSURANCE.md) | 品質保証プロセス・検証チェックリスト |
| 03 | [IMPLEMENTATION_VERIFICATION.md](03_IMPLEMENTATION_VERIFICATION.md) | 実装照合プロセス |
| 04 | [TITLE_UNIFICATION_RULES.md](04_TITLE_UNIFICATION_RULES.md) | タイトル統一ルール |

### 品質保証詳細

| # | ドキュメント | 内容 |
|---|-------------|------|
| 05 | [quality-assurance-overview.md](05_quality-assurance-overview.md) | 品質保証への取り組み概要 |
| 06 | [quality-assurance-detailed-guide.md](06_quality-assurance-detailed-guide.md) | 品質保証詳細ガイド（Phase 1-3） |
| 07 | [automation-tools-guide.md](07_automation-tools-guide.md) | 自動化ツール使用ガイド |
| 08 | [checklist-guide.md](08_checklist-guide.md) | チェックリスト活用ガイド |

### 教訓・原則・改善

| # | ドキュメント | 内容 |
|---|-------------|------|
| 09 | [lessons-learned.md](09_lessons-learned.md) | 問題分析と教訓（7件の問題） |
| 10 | [work-principles.md](10_work-principles.md) | 作業原則と文化（3つの原則） |
| 11 | [quality-assurance-examples.md](11_quality-assurance-examples.md) | 品質保証の実践例 |
| 12 | [continuous-improvement.md](12_continuous-improvement.md) | 継続的改善ガイド |

---

## 📊 リソース統計

### 自動化ツール

- **総数**: 5個
- **品質チェック用**: 3個（count-files.sh, check-dates.sh, search-env-var.sh）
- **検証用**: 2個（validate_commands.sh, validate_config_keys.sh）

### チェックリスト

- **総数**: 4個
- **総チェック項目数**: 50項目
  - 実装照合: 15項目
  - 動作確認: 12項目
  - 削除操作: 10項目
  - 文書品質: 13項目

### メタドキュメント

- **総数**: 12文書
- **総文字数**: 約43,500文字
- **カバー範囲**: Phase 1-3の全プロセス

---

## 🎯 使用方法

### 新規ドキュメント作成時

1. **実装照合チェックリスト**を使用してソースコード確認
2. **動作確認チェックリスト**を使用してコマンド・設定の動作確認
3. **文書品質チェックリスト**を使用して最終確認
4. **自動化ツール**（check-dates.sh, count-files.sh）で自動検証

### 削除作業時

1. **search-env-var.sh**で使用箇所を全検索
2. **削除操作チェックリスト**に従って安全に削除
3. **check-dates.sh**で整合性確認

### 定期チェック時

1. **count-files.sh**でファイル数確認
2. **check-dates.sh**で日付整合性確認
3. **文書品質チェックリスト**で品質確認

---

## 📖 関連ドキュメント

- **[品質保証概要](05_quality-assurance-overview.md)** - 品質保証の全体像
- **[品質保証詳細ガイド](06_quality-assurance-detailed-guide.md)** - Phase 1-3の詳細プロセス
- **[自動化ツール使用ガイド](07_automation-tools-guide.md)** - ツールの詳細な使用方法
- **[チェックリスト活用ガイド](08_checklist-guide.md)** - チェックリストの活用方法
- **[継続的改善ガイド](12_continuous-improvement.md)** - 長期的な品質維持

---

最終更新: 2025-10-26
