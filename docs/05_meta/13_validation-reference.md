[ホーム](../README.md) > [Meta](README.md) > 検証ツールリファレンス

---

# 検証ツールリファレンス

本サイトの自動検証ツールの技術仕様とトラブルシューティングを提供します。

**最終更新**: 2025-11-01

---

## 📋 目次

1. [ツール一覧](#ツール一覧)
2. [scripts/ツール詳細](#scriptsツール詳細)
3. [tools/verification/詳細](#toolsverification詳細)
4. [エラーメッセージ](#エラーメッセージ)
5. [トラブルシューティング](#トラブルシューティング)
6. [CI/CD統合](#cicd統合)

---

## ツール一覧

### scripts/（5ツール）

| ツール | 目的 | 実行時間 | 自動実行 |
|--------|------|----------|----------|
| count-files.sh | ファイル数カウント | <1秒 | 手動 |
| check-dates.sh | 日付整合性チェック | <1秒 | Git hook |
| search-env-var.sh | 環境変数検索 | <1秒 | 手動 |
| validate_commands.sh | コマンド検証 | <1秒 | 手動 |
| validate_config_keys.sh | 設定キー検証 | <1秒 | 手動 |

### tools/verification/（8バリデーター）

| バリデーター | 目的 | 実行時間 | 自動実行 |
|-------------|------|----------|----------|
| env_validator.py | 環境変数検証 | 1-2秒 | CI/CD |
| path_validator.py | ファイルパス検証 | 1-2秒 | CI/CD |
| v2_validator.py | 統合検証 | 2-3秒 | CI/CD |
| setting_validator.py | 設定項目検証 | 1-2秒 | CI/CD |
| command_validator.py | コマンド検証 | 1-2秒 | CI/CD |
| enum_validator.py | 列挙型検証 | 1-2秒 | CI/CD |
| schema_validator.py | スキーマ検証 | 1-2秒 | CI/CD |
| type_validator.py | 型検証 | 1-2秒 | CI/CD |

---

## scripts/ツール詳細

### count-files.sh

#### 仕様

**入力**: なし（docsディレクトリを自動スキャン）

**出力**: 標準出力（カテゴリ別ファイル数）

**終了コード**:
- `0`: 正常終了
- `1`: エラー

#### 使用例

```bash
# 基本実行
./scripts/count-files.sh

# 出力をファイルに保存
./scripts/count-files.sh > file-count.txt

# 特定カテゴリのみカウント
find docs/01_for-users -name "*.md" | wc -l
```

#### 内部動作

1. `docs/`配下の`.md`ファイルを検索
2. カテゴリ別に集計
3. README.mdを除外
4. 結果を整形して出力

---

### check-dates.sh

#### 仕様

**入力**: ディレクトリパス（オプション）

**出力**: 標準出力（日付不整合リスト）

**終了コード**:
- `0`: 全て一致
- `1`: 不整合あり

#### 使用例

```bash
# 全体チェック
./scripts/check-dates.sh

# 特定ディレクトリ
./scripts/check-dates.sh docs/05_meta/

# エラーのみ表示
./scripts/check-dates.sh 2>&1 | grep "❌"
```

#### 内部動作

1. 対象ファイルを列挙
2. Git最終更新日を取得（`git log -1 --format=%cd --date=short`）
3. ドキュメント記載日を抽出（`**最終更新**: YYYY-MM-DD`）
4. 比較して不整合を報告

#### 日付フォーマット

**対応形式**:
```markdown
**最終更新**: 2025-11-01
**最終更新日**: 2025-11-01
最終更新: 2025-11-01
```

**非対応形式**:
```markdown
❌ 最終更新: 2025/11/01      # スラッシュ区切り
❌ 最終更新: 2025-11-1       # ゼロパディングなし
❌ Last updated: 2025-11-01  # 英語
```

---

### search-env-var.sh

#### 仕様

**入力**: 環境変数名

**出力**: 標準出力（検索結果）

**終了コード**:
- `0`: 見つかった
- `1`: 見つからない

#### 使用例

```bash
# 環境変数を検索
./scripts/search-env-var.sh Q_DEBUG

# 複数の環境変数
for var in Q_DEBUG Q_AGENT Q_CLI_CLIENT_APPLICATION; do
  echo "=== $var ==="
  ./scripts/search-env-var.sh $var
done
```

#### 内部動作

1. `docs/`配下を`rg`で検索
2. マッチした行を表示
3. ファイル名と行番号を含める

---

### validate_commands.sh

#### 仕様

**入力**: なし（ドキュメントを自動スキャン）

**出力**: 標準出力（検証結果）

**終了コード**:
- `0`: 全て正常
- `1`: エラーあり

#### 使用例

```bash
# 基本実行
./scripts/validate_commands.sh

# 詳細モード
./scripts/validate_commands.sh --verbose
```

#### 検証項目

1. コマンド名の正確性
2. サブコマンドの存在確認
3. オプションの妥当性

---

### validate_config_keys.sh

#### 仕様

**入力**: なし（ドキュメントを自動スキャン）

**出力**: 標準出力（検証結果）

**終了コード**:
- `0`: 全て正常
- `1`: エラーあり

#### 使用例

```bash
# 基本実行
./scripts/validate_config_keys.sh

# 詳細モード
./scripts/validate_config_keys.sh --verbose
```

#### 検証項目

1. 設定キー名の正確性
2. デフォルト値の妥当性
3. 型の整合性

---

## tools/verification/詳細

### 共通仕様

#### 実行方法

```bash
cd tools/verification

# 個別実行
python3 validators/env_validator.py ../../docs

# 全バリデーター実行
make validate-all

# 特定バリデーターのみ
make validate-env
make validate-paths
```

#### 出力形式

```
=== バリデーター名 ===

✅ 検証項目1: OK
✅ 検証項目2: OK
❌ 検証項目3: エラー
   詳細: エラーメッセージ

検証結果:
  成功: 2
  失敗: 1
  合計: 3
```

#### 終了コード

- `0`: 全て成功
- `1`: 1つ以上失敗

---

### env_validator.py

#### 目的

環境変数の正確性を検証

#### 検証項目

1. **登録済み環境変数**
   - `sources_template.json`に定義されているか
   - `env_validator.py`の`KNOWN_ENV_VARS`に含まれているか

2. **未登録環境変数**
   - ドキュメントに記載されているが未登録の変数を検出

3. **型の整合性**
   - `sources_template.json`の型定義とドキュメントの記載が一致

#### 使用例

```bash
# 基本実行
python3 validators/env_validator.py ../../docs

# 詳細モード
python3 validators/env_validator.py ../../docs --verbose

# JSON出力
python3 validators/env_validator.py ../../docs --json
```

#### 設定ファイル

**sources_template.json**:
```json
{
  "Q_DEBUG": {
    "default": null,
    "type": "string"
  },
  "Q_AGENT": {
    "default": null,
    "type": "string"
  }
}
```

**env_validator.py**:
```python
KNOWN_ENV_VARS = {
    'Q_DEBUG',
    'Q_AGENT',
    'Q_CLI_CLIENT_APPLICATION',
    # ...
}
```

---

### path_validator.py

#### 目的

ファイルパスの正確性を検証

#### 検証項目

1. **パスの存在確認**
   - ドキュメントに記載されたパスが実際に存在するか

2. **パスの形式**
   - 相対パス/絶対パスの妥当性
   - パス区切り文字の統一

3. **リンク切れ**
   - Markdownリンクの参照先が存在するか

#### 使用例

```bash
# 基本実行
python3 validators/path_validator.py ../../docs

# 特定ファイルのみ
python3 validators/path_validator.py ../../docs/01_for-users/

# 詳細モード
python3 validators/path_validator.py ../../docs --verbose
```

#### 検証パターン

```python
PATTERNS = [
    r'`([^`]+\.md)`',           # `file.md`
    r'\[.*?\]\(([^)]+\.md)\)',  # [text](file.md)
    r'docs/([^\s]+\.md)',       # docs/path/file.md
    # ...
]
```

---

### v2_validator.py

#### 目的

統合検証（環境変数 + ファイルパス）

#### 検証項目

1. 環境変数検証（env_validator.py）
2. ファイルパス検証（path_validator.py）
3. 整合性チェック
4. 統計レポート

#### 使用例

```bash
# 基本実行
python3 validators/v2_validator.py ../../docs

# レポート生成
python3 validators/v2_validator.py ../../docs --report

# JSON出力
python3 validators/v2_validator.py ../../docs --json > report.json
```

#### 出力例

```
=== v2.0 統合バリデーター ===

環境変数検証:
  ✅ 登録済み: 19/19 (100%)
  ✅ 未登録: 0/19 (0%)

ファイルパス検証:
  ✅ 存在確認: 150/150 (100%)
  ✅ リンク切れ: 0/150 (0%)

統計:
  検証ファイル数: 119
  検証項目数: 1,849
  エラー数: 0
  警告数: 0

総合評価: ✅ 優秀
```

---

### setting_validator.py

#### 目的

設定項目の正確性を検証

#### 検証項目

1. 設定キー名の正確性
2. デフォルト値の妥当性
3. 型の整合性
4. 必須/オプションの区別

---

### command_validator.py

#### 目的

コマンドの正確性を検証

#### 検証項目

1. コマンド名の正確性
2. サブコマンドの存在確認
3. オプションの妥当性
4. 使用例の動作確認

---

### enum_validator.py

#### 目的

列挙型の正確性を検証

#### 検証項目

1. 列挙値の正確性
2. 値の範囲チェック
3. 型の整合性

---

### schema_validator.py

#### 目的

JSONスキーマの正確性を検証

#### 検証項目

1. スキーマの妥当性
2. 必須フィールドの存在
3. 型の整合性

---

### type_validator.py

#### 目的

型定義の正確性を検証

#### 検証項目

1. 型名の正確性
2. 型の互換性
3. 型変換の妥当性

---

## エラーメッセージ

### 環境変数関連

#### ENV001: 未登録環境変数
```
❌ ENV001: 未登録環境変数が検出されました
   変数名: Q_UNKNOWN_VAR
   ファイル: docs/01_for-users/03_configuration/06_environment-variables.md
   行番号: 123
   対策: sources_template.jsonに追加してください
```

#### ENV002: 型不整合
```
❌ ENV002: 型が一致しません
   変数名: Q_DEBUG
   期待: string
   実際: boolean
   ファイル: docs/01_for-users/03_configuration/06_environment-variables.md
   対策: ドキュメントの型を修正してください
```

---

### ファイルパス関連

#### PATH001: ファイルが存在しない
```
❌ PATH001: ファイルが存在しません
   パス: docs/01_for-users/99_missing.md
   参照元: docs/01_for-users/README.md
   行番号: 45
   対策: ファイルを作成するか、リンクを削除してください
```

#### PATH002: リンク切れ
```
❌ PATH002: リンク切れが検出されました
   リンク: [Missing](99_missing.md)
   参照元: docs/01_for-users/01_getting-started/01_installation.md
   行番号: 78
   対策: リンク先を修正してください
```

---

### 日付関連

#### DATE001: 日付不整合
```
❌ DATE001: 日付が一致しません
   ファイル: docs/01_for-users/README.md
   Git: 2025-11-01
   Doc: 2025-10-26
   対策: ドキュメントの日付を更新してください
```

---

## トラブルシューティング

### 問題1: バリデーターが実行できない

**症状**:
```bash
$ python3 validators/env_validator.py ../../docs
ModuleNotFoundError: No module named 'jsonschema'
```

**原因**: 依存パッケージ未インストール

**対策**:
```bash
cd tools/verification
pip3 install -r requirements.txt
```

---

### 問題2: 大量のエラーが出る

**症状**:
```
❌ ENV001: 未登録環境変数が検出されました (50件)
```

**原因**: sources_template.jsonが古い

**対策**:
```bash
# 最新版を取得
git pull origin main

# 再実行
python3 validators/env_validator.py ../../docs
```

---

### 問題3: 日付チェックで全てエラー

**症状**:
```
❌ 全てのファイルで日付不整合
```

**原因**: Gitコミット前

**対策**:
```bash
# コミット後に再実行
git add .
git commit -m "update docs"
./scripts/check-dates.sh
```

---

### 問題4: パス検証で誤検出

**症状**:
```
❌ PATH001: ファイルが存在しません
   パス: /absolute/path/to/file.md
```

**原因**: 絶対パスの誤検出

**対策**:
```bash
# path_validator.pyの除外パターンを確認
# 必要に応じて除外リストに追加
```

---

## CI/CD統合

### GitHub Actions

#### ワークフロー例

```yaml
name: Documentation Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        cd tools/verification
        pip install -r requirements.txt
    
    - name: Run validators
      run: |
        cd tools/verification
        make validate-all
    
    - name: Check dates
      run: |
        ./scripts/check-dates.sh
    
    - name: Count files
      run: |
        ./scripts/count-files.sh
```

---

### ローカルGit Hook

#### pre-commit

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# 日付チェック
./scripts/check-dates.sh
if [ $? -ne 0 ]; then
  echo "❌ 日付不整合があります"
  exit 1
fi

# バリデーター実行
cd tools/verification
make validate-all
if [ $? -ne 0 ]; then
  echo "❌ バリデーションエラーがあります"
  exit 1
fi

echo "✅ 全てのチェックが成功しました"
exit 0
```

---

## 関連ドキュメント

- **[自動化ツール完全ガイド](05_automation-tools.md)** - ツールの使い方
- **[手動チェック](06_manual-checks.md)** - 自動化できない項目
- **[日常ワークフロー](09_daily-workflow.md)** - 検証の実践手順

---

**最終更新**: 2025-11-01  
**メンテナー**: ドキュメントチーム
