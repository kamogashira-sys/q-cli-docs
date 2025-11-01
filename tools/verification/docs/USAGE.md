# Q CLI Documentation Verification Tool - 実行手順書

**バージョン**: 1.0.0  
**作成日**: 2025-10-30  
**対象ユーザー**: 開発者、ドキュメント管理者

---

## 📋 目次

1. [前提条件](#前提条件)
2. [インストール](#インストール)
3. [基本的な使い方](#基本的な使い方)
4. [詳細な使い方](#詳細な使い方)
5. [出力形式](#出力形式)
6. [トラブルシューティング](#トラブルシューティング)
7. [FAQ](#faq)

---

## 前提条件

### システム要件

| 項目 | 要件 |
|------|------|
| OS | Linux / macOS |
| Python | 3.10以上 |
| メモリ | 100MB以上の空き |
| ディスク | 50MB以上の空き |

### 必要なファイル

1. **ソースコードリポジトリ**: Q CLIのRustソースコード
2. **スキーマディレクトリ**: JSON Schemaファイル
3. **ドキュメントディレクトリ**: Markdownドキュメント

---

## インストール

### 方法1: Makefileを使用（推奨）

```bash
cd /home/katoh/projects/q-cli-docs/tools/verification
make install
```

### 方法2: 手動インストール

```bash
cd /home/katoh/projects/q-cli-docs/tools/verification

# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# パッケージインストール
pip install -e .
```

### インストール確認

```bash
# ヘルプ表示
python -m orchestrators.cli --help
```

**期待される出力**:
```
Usage: python -m orchestrators.cli [OPTIONS]

  Q CLI Documentation Verification Tool.

Options:
  --repo PATH              Path to source repository  [required]
  --schemas PATH           Path to schema directory  [required]
  --docs PATH              Path to documentation directory  [required]
  --format [console|json]  Output format
  --config PATH            Path to configuration file
  --help                   Show this message and exit.
```

---

## 基本的な使い方

### 1. 最小限の実行

```bash
cd /home/katoh/projects/q-cli-docs/tools/verification
source venv/bin/activate

python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs
```

### 2. シェルスクリプトで実行

```bash
cd /home/katoh/projects/q-cli-docs/tools/verification

bash orchestrators/verify.sh \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs
```

### 3. JSON形式で出力

```bash
python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs \
  --format json
```

---

## 詳細な使い方

### コマンドラインオプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo PATH` | ✅ | ソースコードリポジトリのパス | なし |
| `--schemas PATH` | ✅ | スキーマディレクトリのパス | なし |
| `--docs PATH` | ✅ | ドキュメントディレクトリのパス | なし |
| `--format [console\|json]` | ❌ | 出力形式 | `console` |
| `--config PATH` | ❌ | 設定ファイルのパス | なし |
| `--help` | ❌ | ヘルプ表示 | - |

### 実行例

#### 例1: 基本的な検証

```bash
python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs
```

**出力**:
```
2025-10-30 14:00:00,000 - INFO - Starting verification workflow
2025-10-30 14:00:00,000 - INFO - Step 1: Extracting data from sources
...
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

#### 例2: JSON形式でファイルに保存

```bash
python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs \
  --format json > verification-report.json
```

#### 例3: エラーのみを抽出

```bash
python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs \
  --format json 2>/dev/null | jq '.errors'
```

#### 例4: サマリーのみを表示

```bash
python -m orchestrators.cli \
  --repo /tmp/q-cli-source \
  --schemas /tmp/q-cli-source/schemas \
  --docs /home/katoh/projects/q-cli-docs/docs \
  --format json 2>/dev/null | jq '.summary'
```

**出力**:
```json
{
  "total_errors": 193,
  "total_warnings": 371
}
```

---

## 出力形式

### Console形式（デフォルト）

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

  2. missing_doc
     Setting 'chunk_size' exists in source but not documented

  ...

Warnings:

  1. missing_in_source
     Setting 'status' documented but not found in source

  ...
```

### JSON形式

```json
{
  "status": "fail",
  "summary": {
    "total_errors": 193,
    "total_warnings": 371
  },
  "errors": [
    {
      "type": "missing_schema",
      "setting": "chunk_size",
      "message": "Setting 'chunk_size' exists in source but not in schema"
    },
    {
      "type": "missing_doc",
      "setting": "chunk_size",
      "message": "Setting 'chunk_size' exists in source but not documented"
    }
  ],
  "warnings": [
    {
      "type": "missing_in_source",
      "setting": "status",
      "message": "Setting 'status' documented but not found in source"
    }
  ],
  "extracted_data": {
    "source": {
      "settings_count": 9,
      "enums_count": 302,
      "commands_count": 0,
      "env_vars_count": 13
    },
    "schema": {
      "properties_count": 15,
      "enums_count": 0
    },
    "docs": {
      "files_count": 119
    }
  }
}
```

---

## エラー・警告の種類

### エラー（Errors）

| タイプ | 説明 | 重要度 |
|--------|------|--------|
| `missing_schema` | ソースコードにあるがスキーマにない | 高 |
| `missing_doc` | ソースコードにあるがドキュメント化されていない | 高 |
| `missing_schema_definition` | スキーマ定義が存在しない | 高 |

### 警告（Warnings）

| タイプ | 説明 | 重要度 |
|--------|------|--------|
| `missing_in_source` | ドキュメントにあるがソースコードにない | 中 |
| `missing_in_schema` | ドキュメントにあるがスキーマにない | 中 |
| `missing_in_docs` | ソースコードにあるがドキュメント化されていない | 中 |

---

## パフォーマンス

### 実行時間

| リポジトリサイズ | 実行時間 |
|----------------|---------|
| 小規模（<100ファイル） | <0.1秒 |
| 中規模（100-500ファイル） | 0.1-0.5秒 |
| 大規模（500+ファイル） | 0.5-2秒 |

### メモリ使用量

| リポジトリサイズ | メモリ使用量 |
|----------------|-------------|
| 小規模 | <50MB |
| 中規模 | 50-100MB |
| 大規模 | 100-200MB |

---

## トラブルシューティング

### 問題1: ModuleNotFoundError

**症状**:
```
ModuleNotFoundError: No module named 'orchestrators'
```

**解決方法**:
```bash
# 仮想環境を有効化
source venv/bin/activate

# パッケージを再インストール
pip install -e .
```

### 問題2: ExtractionError: Path does not exist

**症状**:
```
ExtractionError: Repository path does not exist: /path/to/repo
```

**解決方法**:
- パスが正しいか確認
- パスが存在するか確認
- 絶対パスを使用

### 問題3: ConfigurationError: Failed to load JSON

**症状**:
```
ConfigurationError: Failed to load JSON file: /path/to/schema.json
```

**解決方法**:
- JSONファイルの構文を確認
- ファイルが存在するか確認
- ファイルの読み取り権限を確認

### 問題4: 実行が遅い

**症状**:
実行に10秒以上かかる

**解決方法**:
1. 不要なファイルを除外
2. `.gitignore`を確認
3. 大きなバイナリファイルを除外

---

## FAQ

### Q1: どのくらいの頻度で実行すべきですか？

**A**: 以下のタイミングで実行することを推奨します：
- コミット前
- PR作成時
- CI/CDパイプライン内
- 週次の定期実行

### Q2: False Positiveが多い場合は？

**A**: 以下を確認してください：
1. 抽出器の設定を調整
2. 除外パターンを設定
3. バリデーターの閾値を調整

### Q3: 特定のファイルを除外したい

**A**: 設定ファイルで除外パターンを指定：
```yaml
# config/verification.yaml
exclude_patterns:
  - "**/*_test.rs"
  - "**/examples/**"
```

### Q4: CI/CDに統合したい

**A**: 以下のスクリプトを使用：
```bash
#!/bin/bash
set -e

# 検証実行
python -m orchestrators.cli \
  --repo . \
  --schemas ./schemas \
  --docs ./docs \
  --format json > report.json

# エラーがあれば失敗
if [ $(jq '.summary.total_errors' report.json) -gt 0 ]; then
  echo "Verification failed with errors"
  exit 1
fi
```

### Q5: 結果をどう解釈すべきですか？

**A**: 
- **Errors**: 必ず修正が必要
- **Warnings**: 確認が必要（修正は任意）
- **Status: PASS**: 問題なし
- **Status: FAIL**: エラーあり

---

## 次のステップ

1. **設計書を読む**: [DESIGN.md](DESIGN.md)
2. **テストを実行**: `make test`
3. **カバレッジを確認**: `make coverage`
4. **CI/CDに統合**: GitHub Actions等

---

## サポート

### ドキュメント

- [設計書](DESIGN.md)
- [API リファレンス](API.md)
- [トラブルシューティング](TROUBLESHOOTING.md)

### 問い合わせ

- GitHub Issues: [aws/amazon-q-developer-cli](https://github.com/aws/amazon-q-developer-cli/issues)
- 作業記録: [/home/katoh/ai-work/20251030/202510301215-log.md](/home/katoh/ai-work/20251030/202510301215-log.md)

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2025-10-30 | 1.0.0 | 初版作成 |
