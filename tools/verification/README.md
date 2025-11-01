# Q CLI ドキュメント検証ツール

## 概要

このディレクトリには、Q CLIドキュメントの自動検証ツールが含まれています。
ソースコード、JSONスキーマ、ドキュメント間の整合性を保証します。

---

## アーキテクチャ

検証システムは5層アーキテクチャで構成されています：

### 1. データ抽出層 (`extractors/`)
- ソースコード（Rust）から設定を抽出
- JSONスキーマから設定を抽出
- ドキュメント（Markdown）から設定を抽出

### 2. データ変換層 (`normalizers/`)
- データを統一フォーマットに正規化
- ソース間の差異を検出

### 3. 検証ロジック層 (`validators/`)
- 設定値の検証
- 列挙値の検証
- コマンドオプションの検証
- データ型の検証
- スキーマの検証

### 4. レポート層 (`reporters/`)
- コンソール出力
- JSON出力
- HTMLレポート

### 5. オーケストレーション層 (`orchestrators/`)
- 検証ワークフローの調整
- CI/CD統合

---

## ディレクトリ構造

```
verification/
├── extractors/          # 各種ソースからのデータ抽出
├── normalizers/         # データ正規化と変換
├── validators/          # 検証ロジック
│   ├── setting_validator.py      # 設定値検証
│   ├── enum_validator.py         # 列挙値検証
│   ├── command_validator.py      # コマンド検証
│   ├── type_validator.py         # 型検証
│   ├── schema_validator.py       # スキーマ検証
│   ├── path_validator.py         # パス検証
│   ├── env_validator.py          # 環境変数検証
│   └── v2_validator.py           # v2.0統合検証
├── reporters/           # レポート生成
├── orchestrators/       # ワークフロー調整
│   ├── verification_orchestrator.py  # メインオーケストレーター
│   ├── integrated_validator.py       # 統合検証
│   ├── validate_paths.py             # パス検証
│   ├── cli.py                        # CLIインターフェース
│   └── verify.sh                     # 実行スクリプト
├── lib/                 # 共有ライブラリ
├── tests/               # テストスイート
│   ├── unit/           # ユニットテスト
│   ├── integration/    # 統合テスト
│   └── e2e/            # E2Eテスト
├── config/             # 設定ファイル
├── docs/               # ドキュメント
└── examples/           # 使用例
```

---

## クイックスタート

### インストール

```bash
# 依存関係をインストール
make install

# または手動で
pip install -r requirements.txt
pip install -e .
```

### 使用方法

#### 基本的な使用

```bash
# クイック検証（< 10秒）
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs

# JSON出力
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs --format json

# カスタム設定
./orchestrators/verify.sh --repo /path/to/repo --schemas /path/to/schemas --docs /path/to/docs --config config/verification.yaml
```

#### 実例

```bash
# Q CLIドキュメントを検証
./orchestrators/verify.sh \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/crates/amzn-toolkit-telemetry/schemas \
  --docs /home/user/q-cli-docs/docs
```

---

## 検証ツール詳細

### v2.0統合検証（推奨）

**ファイル**: `validators/v2_validator.py`

**目的**: 全検証を統合実行

**使用方法**:
```bash
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

**検証項目**:
1. パス検証（Agent、MCP、Knowledge）
2. 環境変数検証（28項目）
3. 設定項目検証
4. スキーマ検証

**出力例**:
```
=== Q CLI Documentation Validation v2.0 ===

Phase 1: Path Validation
✅ Agent paths: 0 errors
✅ MCP paths: 0 errors
✅ Knowledge paths: 0 errors

Phase 2: Environment Variable Validation
✅ Environment variables: 0 errors

Summary:
  Total checks: 1,849
  Errors: 0
  Warnings: 0
  Coverage: 100%
```

---

### パス検証

**ファイル**: `validators/path_validator.py`

**目的**: Agent、MCP、Knowledgeのパス検証

**使用方法**:
```bash
cd tools/verification
python3 orchestrators/validate_paths.py ../../docs
```

**検証内容**:
- Agent設定ファイルパス
- MCP設定ファイルパス
- Knowledgeディレクトリパス

---

### 環境変数検証

**ファイル**: `validators/env_validator.py`

**目的**: 環境変数の整合性検証

**検証項目**:
- Q CLI固有環境変数（19項目）
- その他環境変数（9項目）

**使用方法**:
```python
from validators.env_validator import EnvValidator

validator = EnvValidator()
results = validator.validate_all('docs/')
```

---

## 開発ステータス

- **フェーズ**: Phase 2完了
- **現在のステータス**: 本番環境対応
- **テストカバレッジ**: 94%
- **テスト結果**: 62合格、1スキップ

---

## 成功基準

### Phase 1（完了）
- ✅ 基本的な検証機能
- ✅ ユニットテスト
- ✅ 統合テスト

### Phase 2（完了）
- ✅ パス検証機能
- ✅ 環境変数検証機能
- ✅ v2.0統合検証
- ✅ テストカバレッジ90%以上

### Phase 3（計画中）
- ⏳ CI/CD統合
- ⏳ HTMLレポート生成
- ⏳ パフォーマンス最適化

---

## テスト

### テスト実行

```bash
# 全テスト実行
make test

# ユニットテストのみ
make test-unit

# 統合テストのみ
make test-integration

# カバレッジレポート
make coverage
```

### テスト結果

```bash
# 最新のテスト結果
pytest tests/ -v

# 出力例
tests/unit/test_validators.py::test_setting_validator PASSED
tests/unit/test_validators.py::test_enum_validator PASSED
tests/integration/test_workflow.py::test_full_workflow PASSED

62 passed, 1 skipped in 2.34s
```

---

## 設定

### 設定ファイル

**ファイル**: `config/verification.yaml`

**内容**:
```yaml
# 検証対象
sources:
  - source_code
  - json_schemas
  - documentation

# 検証レベル
validation_level: strict

# 出力形式
output_format: console

# エラー処理
error_handling:
  stop_on_error: false
  max_errors: 100
```

---

## トラブルシューティング

### 問題1: 依存関係エラー

```bash
# 解決方法
pip install -r requirements.txt --upgrade
```

### 問題2: パス検証エラー

```bash
# デバッグ実行
python3 -m pdb validators/path_validator.py
```

### 問題3: テスト失敗

```bash
# 詳細ログ
pytest tests/ -vv --log-cli-level=DEBUG
```

---

## 貢献

### 新規検証ツール追加

1. `validators/` に新規ファイル作成
2. テストを `tests/unit/` に追加
3. `orchestrators/integrated_validator.py` に統合
4. ドキュメント更新

### コーディング規約

- PEP 8準拠
- 型ヒント必須
- Docstring必須
- テストカバレッジ90%以上

---

## 関連ドキュメント

- **[自動化ツール](../../docs/05_meta/05_automation-tools.md)** - ツール一覧
- **[品質保証](../../docs/05_meta/README.md)** - 品質保証の仕組み
- **[検証ツールリファレンス](../../docs/05_meta/13_validation-reference.md)** - 技術仕様

---

## ライセンス

MIT License

---

**最終更新**: 2025-11-01
