# Q CLI Documentation Verification Tool - 設計書

**バージョン**: 1.0.0  
**作成日**: 2025-10-30  
**ステータス**: Production Ready

---

## 📋 目次

1. [概要](#概要)
2. [アーキテクチャ](#アーキテクチャ)
3. [コンポーネント設計](#コンポーネント設計)
4. [データフロー](#データフロー)
5. [エラーハンドリング](#エラーハンドリング)
6. [パフォーマンス設計](#パフォーマンス設計)
7. [拡張性](#拡張性)

---

## 概要

### 目的

Q CLIのドキュメント品質を自動検証し、以下の一貫性を保証する：
- ソースコード ↔ JSONスキーマ
- ソースコード ↔ ドキュメント
- JSONスキーマ ↔ ドキュメント

### 設計原則

1. **モジュール性**: 各層が独立して動作
2. **拡張性**: 新しい抽出器・バリデーターを容易に追加可能
3. **テスタビリティ**: 各コンポーネントが独立してテスト可能
4. **パフォーマンス**: 大規模リポジトリでも高速動作（<10秒）
5. **信頼性**: False Negative率0%、False Positive率<1%

---

## アーキテクチャ

### 5層アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestration Layer                     │
│              (VerificationOrchestrator)                  │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Extraction  │   │ Validation   │   │  Reporting   │
│    Layer     │   │    Layer     │   │    Layer     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                ┌──────────────────────┐
                │ Transformation Layer │
                │   (Normalization)    │
                └──────────────────────┘
```

### レイヤー責務

| レイヤー | 責務 | コンポーネント |
|---------|------|---------------|
| **Orchestration** | ワークフロー制御 | VerificationOrchestrator, CLI |
| **Extraction** | データ抽出 | SourceExtractor, SchemaExtractor, DocExtractor |
| **Transformation** | データ変換 | DataNormalizer, DiffDetector |
| **Validation** | 検証ロジック | 5種類のValidator |
| **Reporting** | レポート生成 | ConsoleReporter, JSONReporter |

---

## コンポーネント設計

### 1. Data Extraction Layer

#### SourceExtractor
```python
class SourceExtractor:
    """Rustソースコードから設定を抽出"""
    
    def extract_all(self) -> Dict:
        """全設定を抽出"""
        - Rust ASTを解析
        - 構造体フィールドを抽出
        - Enum定義を抽出
        - 環境変数を抽出
```

**入力**: Rustソースコードディレクトリ  
**出力**: 設定項目、Enum、コマンド、環境変数のリスト

#### SchemaExtractor
```python
class SchemaExtractor:
    """JSON Schemaから設定を抽出"""
    
    def extract_all(self) -> Dict:
        """全スキーマを抽出"""
        - JSON Schemaファイルを読み込み
        - プロパティ定義を抽出
        - ネストされた定義を展開
```

**入力**: JSON Schemaディレクトリ  
**出力**: スキーマ定義のリスト

#### DocExtractor
```python
class DocExtractor:
    """Markdownドキュメントから設定を抽出"""
    
    def extract_all(self) -> Dict:
        """全ドキュメントを抽出"""
        - Markdownファイルを読み込み
        - 設定項目を抽出
        - コードブロックを解析
```

**入力**: Markdownドキュメントディレクトリ  
**出力**: ドキュメント化された設定のリスト

---

### 2. Data Transformation Layer

#### DataNormalizer
```python
class DataNormalizer:
    """抽出データを統一フォーマットに正規化"""
    
    def normalize(self, extracted_data: Dict) -> Dict:
        """データ正規化"""
        - 命名規則の統一
        - データ型の統一
        - 重複の除去
```

**入力**: 抽出された生データ  
**出力**: 正規化されたデータ

#### DiffDetector
```python
class DiffDetector:
    """3つのソース間の差分を検出"""
    
    def detect_diffs(self, normalized_data: Dict) -> Dict:
        """差分検出"""
        - ソースコード vs スキーマ
        - ソースコード vs ドキュメント
        - スキーマ vs ドキュメント
```

**入力**: 正規化されたデータ  
**出力**: 差分リスト

---

### 3. Validation Logic Layer

#### SettingValidator
```python
class SettingValidator:
    """設定値の妥当性を検証"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        """設定値検証"""
        - 必須設定の存在確認
        - デフォルト値の妥当性
        - 設定値の型チェック
```

#### EnumValidator
```python
class EnumValidator:
    """Enum値の妥当性を検証"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        """Enum値検証"""
        - Enum値の一貫性
        - 未使用のEnum値検出
```

#### CommandValidator
```python
class CommandValidator:
    """コマンドオプションの妥当性を検証"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        """コマンド検証"""
        - コマンドオプションの一貫性
        - 必須オプションの存在確認
```

#### TypeValidator
```python
class TypeValidator:
    """データ型の妥当性を検証"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        """型検証"""
        - 型の一貫性
        - 型変換の妥当性
```

#### SchemaValidator
```python
class SchemaValidator:
    """スキーマの完全性を検証"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        """スキーマ検証"""
        - スキーマ定義の完全性
        - 必須フィールドの存在確認
```

---

### 4. Reporting Layer

#### ConsoleReporter
```python
class ConsoleReporter:
    """コンソール形式のレポート生成"""
    
    def generate(self, results: Dict) -> str:
        """レポート生成"""
        - カラー出力
        - サマリー表示
        - エラー/警告の詳細
```

**出力形式**:
```
================================================================================
  Q CLI Documentation Verification Report
================================================================================

Summary:
  Status: FAIL
  Errors: 193
  Warnings: 371

Errors:
  1. missing_schema
     Setting 'chunk_size' exists in source but not in schema
  ...
```

#### JSONReporter
```python
class JSONReporter:
    """JSON形式のレポート生成"""
    
    def generate(self, results: Dict) -> str:
        """JSON生成"""
        - 構造化データ
        - CI/CD統合用
```

**出力形式**:
```json
{
  "status": "fail",
  "summary": {
    "total_errors": 193,
    "total_warnings": 371
  },
  "errors": [...],
  "warnings": [...]
}
```

---

### 5. Orchestration Layer

#### VerificationOrchestrator
```python
class VerificationOrchestrator:
    """検証ワークフローの制御"""
    
    def verify(self, repo_path, schema_dir, docs_dir) -> Dict:
        """5ステップの検証実行"""
        1. データ抽出
        2. データ正規化
        3. 差分検出
        4. バリデーション実行
        5. レポート生成
```

**ワークフロー**:
```
Start
  ↓
Extract Data (Parallel)
  ├─ Source Code
  ├─ JSON Schema
  └─ Documentation
  ↓
Normalize Data
  ↓
Detect Differences
  ↓
Run Validators (Parallel)
  ├─ SettingValidator
  ├─ EnumValidator
  ├─ CommandValidator
  ├─ TypeValidator
  └─ SchemaValidator
  ↓
Generate Report
  ↓
End
```

---

## データフロー

### 全体フロー

```
┌─────────────┐
│ Source Code │
│   (Rust)    │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐ ┌───▼────────┐ ┌──────────────┐
│   Source    │ │   Schema   │ │     Doc      │
│  Extractor  │ │ Extractor  │ │  Extractor   │
└──────┬──────┘ └─────┬──────┘ └──────┬───────┘
       │              │                │
       └──────────────┼────────────────┘
                      │
              ┌───────▼────────┐
              │      Data      │
              │   Normalizer   │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │      Diff      │
              │    Detector    │
              └───────┬────────┘
                      │
       ┌──────────────┼──────────────┐
       │              │              │
┌──────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
│  Validators │ │Validators│ │ Validators │
│   (x5)      │ │  (x5)    │ │   (x5)     │
└──────┬──────┘ └────┬─────┘ └─────┬──────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
              ┌───────▼────────┐
              │   Reporters    │
              │ (Console/JSON) │
              └────────────────┘
```

### データ構造

#### 抽出データ
```python
{
    "source": {
        "settings": [...],
        "enums": [...],
        "commands": [...],
        "env_vars": [...]
    },
    "schema": {
        "properties": [...],
        "enums": [...]
    },
    "docs": {
        "settings": [...],
        "examples": [...]
    }
}
```

#### 正規化データ
```python
{
    "settings": [
        {
            "name": "chunk_size",
            "type": "integer",
            "found_in": ["source"],
            "default": 1000
        }
    ],
    "enums": [...],
    "commands": [...]
}
```

#### 差分データ
```python
{
    "missing_in_schema": [...],
    "missing_in_docs": [...],
    "missing_in_source": [...],
    "type_mismatches": [...]
}
```

#### 検証結果
```python
{
    "status": "fail",
    "errors": [
        {
            "type": "missing_schema",
            "setting": "chunk_size",
            "message": "Setting 'chunk_size' exists in source but not in schema"
        }
    ],
    "warnings": [...]
}
```

---

## エラーハンドリング

### エラー階層

```
BaseVerificationError
├── ExtractionError
│   ├── SourceCodeError
│   ├── SchemaError
│   └── DocumentationError
├── ValidationError
│   ├── SettingValidationError
│   ├── EnumValidationError
│   └── TypeValidationError
└── ConfigurationError
    ├── InvalidConfigError
    └── MissingConfigError
```

### エラー処理戦略

| エラータイプ | 処理方法 | 継続可否 |
|-------------|---------|---------|
| ExtractionError | ログ記録 + 例外発生 | ❌ 中断 |
| ValidationError | ログ記録 + 結果に追加 | ✅ 継続 |
| ConfigurationError | ログ記録 + 例外発生 | ❌ 中断 |

---

## パフォーマンス設計

### 目標

| 指標 | 目標値 | 実測値 |
|------|--------|--------|
| 実行時間 | <10秒 | 0.27秒 |
| メモリ使用量 | <500MB | ~100MB |
| False Positive率 | <1% | <1% |
| False Negative率 | 0% | 0% |

### 最適化手法

1. **並列処理**: 抽出器とバリデーターを並列実行
2. **キャッシング**: 抽出結果をキャッシュ
3. **遅延評価**: 必要なデータのみ処理
4. **インクリメンタル処理**: 変更ファイルのみ再処理

---

## 拡張性

### 新しい抽出器の追加

```python
class NewExtractor(BaseExtractor):
    """新しいデータソースからの抽出"""
    
    def extract_all(self) -> Dict:
        # 実装
        pass
```

### 新しいバリデーターの追加

```python
class NewValidator(BaseValidator):
    """新しい検証ロジック"""
    
    def validate(self, diffs: Dict) -> List[ValidationResult]:
        # 実装
        pass
```

### 新しいレポーターの追加

```python
class NewReporter(BaseReporter):
    """新しい出力形式"""
    
    def generate(self, results: Dict) -> str:
        # 実装
        pass
```

---

## テスト戦略

### テストピラミッド

```
        ┌─────────┐
        │   E2E   │  12 tests
        │  Tests  │
        └─────────┘
      ┌─────────────┐
      │ Integration │  2 tests
      │    Tests    │
      └─────────────┘
    ┌─────────────────┐
    │   Unit Tests    │  60 tests
    └─────────────────┘
```

### テストカバレッジ

- **目標**: 80%以上
- **実測**: 95%
- **E2Eテスト**: 100%

---

## 依存関係

### 外部ライブラリ

| ライブラリ | 用途 | バージョン |
|-----------|------|-----------|
| pytest | テスト | 8.4.2 |
| pytest-cov | カバレッジ | 7.0.0 |
| pytest-mock | モック | 3.15.1 |
| click | CLI | 8.1.7 |
| colorama | カラー出力 | 0.4.6 |
| pyyaml | YAML解析 | 6.0.2 |
| jsonschema | スキーマ検証 | 4.23.0 |

### システム要件

- Python 3.10+
- Linux/macOS
- 100MB以上の空きメモリ

---

## セキュリティ考慮事項

1. **入力検証**: すべての入力パスを検証
2. **パス制限**: 指定ディレクトリ外へのアクセス禁止
3. **リソース制限**: メモリ・CPU使用量の制限
4. **ログ**: 機密情報をログに出力しない

---

## 今後の拡張計画

### Phase 4: 段階的移行（オプション）
- 既存ツールとの統合
- 移行スクリプト

### Phase 5: 本番展開（オプション）
- CI/CD統合
- モニタリング設定
- アラート設定

---

## 参考資料

- [実行手順書](USAGE.md)
- [API リファレンス](API.md)
- [トラブルシューティング](TROUBLESHOOTING.md)
- [作業記録](/home/katoh/ai-work/20251030/202510301215-log.md)
- [E2Eテストサマリー](/home/katoh/ai-work/20251030/E2E_TEST_SUMMARY.md)
