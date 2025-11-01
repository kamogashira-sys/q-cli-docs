[ホーム](../README.md) > [Meta](README.md) > 自動化ツール完全ガイド

---

# 自動化ツール完全ガイド

本サイトでは、**3つのツール群**で品質を自動検証しています。

---

## 1. 自動化ツールの全体像

### 3つのツール群

```
1. scripts/ - ドキュメントフォーマットチェック（5ツール）
   ├─ 軽量、高速
   ├─ Git hookで自動実行
   └─ ファイル数、日付、コマンド、設定キー

2. tools/verification/ - 内容の正確性チェック（8バリデーター）
   ├─ ソースコード、スキーマ、ドキュメントの整合性
   ├─ CI/CDで自動実行
   └─ 環境変数、ファイルパス、設定項目

3. 手動チェック - 実装照合と動作確認（4項目）
   ├─ 自動化できない項目
   ├─ 人間の判断が必要
   └─ 実装照合、動作確認、削除操作、文書品質
```

---

## 2. scripts/ - ドキュメントフォーマットチェック

### 2-1. count-files.sh

**目的**: ファイル数の自動カウント

**使用方法**:
```bash
./scripts/count-files.sh
```

**出力例**:
```
=== ファイル数カウント ===

全ファイル数: 119

カテゴリ別:
  01_for-users: 73 文書
  02_for-developers: 11 文書
  03_for-community: 14 文書
  04_issues: 1 文書
  05_meta: 19 文書
```

**活用シーン**:
- 新規ドキュメント作成後
- ドキュメント削除後
- README.md更新前

---

### 2-2. check-dates.sh

**目的**: Git最終更新日とドキュメント記載日の整合性チェック

**使用方法**:
```bash
# 全体をチェック
./scripts/check-dates.sh

# 特定ディレクトリのみ
./scripts/check-dates.sh docs/05_meta/
```

**出力例**:
```
=== 日付整合性チェック ===

✅ docs/05_meta/01_overview.md
   Git: 2025-11-01, Doc: 2025-11-01

❌ docs/01_for-users/README.md
   Git: 2025-10-26, Doc: 2025-10-19

チェック対象: 119 ファイル
一致: 117 ファイル
不一致: 2 ファイル
```

**活用シーン**:
- ドキュメント更新後
- コミット前の最終チェック
- 定期チェック（週次）

---

### 2-3. search-env-var.sh

**目的**: 環境変数の使用箇所を完全に把握

**使用方法**:
```bash
./scripts/search-env-var.sh 環境変数名

# 例
./scripts/search-env-var.sh Q_DEBUG
```

**出力例**:
```
=== 環境変数検索: Q_DEBUG ===

docs/01_for-users/03_configuration/06_environment-variables.md:45:
  export Q_DEBUG=true

docs/01_for-users/08_guides/06_troubleshooting.md:123:
  Q_DEBUG=true q chat "test"

使用箇所数: 2
```

**活用シーン**:
- 環境変数削除前（必須）
- 環境変数名変更前
- 使用状況の把握

---

### 2-4. validate_commands.sh

**目的**: ドキュメント内のQ CLIコマンド例が正確であることを保証

**使用方法**:
```bash
./scripts/validate_commands.sh
```

**検証内容**:
- 実在するコマンドの取得
- ドキュメントからコマンド抽出
- 存在しないサブコマンドの検証
- オプション指定の正確性確認

**活用シーン**:
- **自動実行**: Git commitフック
- 手動実行: ドキュメント更新後
- Q CLIバージョンアップ後

---

### 2-5. validate_config_keys.sh

**目的**: 設定ファイルのキーが正しいことを保証

**使用方法**:
```bash
./scripts/validate_config_keys.sh
```

**検証内容**:
- Agent設定のキー検証
- MCP設定のキー検証
- グローバル設定のキー検証
- スキーマとの整合性確認

**活用シーン**:
- **自動実行**: Git commitフック
- 設定例追加時
- スキーマ更新後

---

## 3. tools/verification/ - 内容の正確性チェック

### 3-1. env_validator.py

**目的**: 環境変数が正しいか検証（70+変数）

**使用方法**:
```bash
cd tools/verification
python3 validators/env_validator.py
```

**検証内容**:
- 環境変数名の正確性
- Q_プレフィックスの確認
- 既知の環境変数との照合

**効果**: 環境変数名の誤りを防止

---

### 3-2. path_validator.py

**目的**: ファイルパスが正しいか検証（10パターン）

**使用方法**:
```bash
cd tools/verification
python3 validators/path_validator.py
```

**検証内容**:
- パス形式の確認
- Q CLI関連パスの確認
- OS依存性の確認

**効果**: パスの誤りを防止

---

### 3-3. v2_validator.py

**目的**: 4つの情報源の整合性を検証

**使用方法**:
```bash
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

**検証内容**:
- ソースコード、調査結果、スキーマ、ドキュメントの整合性
- 環境変数の一貫性
- ファイルパスの一貫性

**効果**: 一貫性率100%を保証

**出力例**:
```
============================================================
v2.0 Validation Report
============================================================

Metrics:
  Files checked: 119
  Total errors: 0
  Total warnings: 0
  Consistency rate: 100.00%

Coverage:
  source_code: 100%
  research: 100%
  schema: 50%
  documentation: 100%

============================================================
✅ All validations passed!
============================================================
```

---

### 3-4. その他のバリデーター

| バリデーター | 検証内容 |
|------------|---------|
| setting_validator.py | 設定項目が正しいか |
| command_validator.py | コマンドが正しいか |
| enum_validator.py | Enum値が正しいか |
| schema_validator.py | スキーマが正しいか |
| type_validator.py | 型が正しいか |

---

## 4. 手動チェック - 実装照合と動作確認

自動化できない項目を人間が確認：

| チェック項目 | 内容 |
|------------|------|
| **実装照合** | ソースコードと一致するか |
| **動作確認** | 実際に動くか |
| **削除操作** | 安全に削除できるか |
| **文書品質** | 読みやすいか |

**詳細**: [手動チェック](06_manual-checks.md)

---

## 5. 全体のワークフロー

### 新規ドキュメント作成時

```
1. ソースコードを確認（手動）
   ↓
2. 実装照合チェックリストを使用（手動）
   ↓
3. 動作確認チェックリストを使用（手動）
   ↓
4. scripts/配下のツールで検証（自動）
   ├─ count-files.sh
   ├─ check-dates.sh
   ├─ validate_commands.sh
   └─ validate_config_keys.sh
   ↓
5. tools/verification/配下のツールで検証（自動）
   ├─ env_validator.py
   ├─ path_validator.py
   └─ v2_validator.py
   ↓
6. 問題なし → コミット
```

---

### ドキュメント更新時

```
1. 変更内容を明確化（手動）
   ↓
2. 影響範囲を確認（手動）
   ↓
3. scripts/配下のツールで検証（自動）
   ├─ check-dates.sh
   └─ search-env-var.sh（必要に応じて）
   ↓
4. tools/verification/配下のツールで検証（自動）
   └─ v2_validator.py
   ↓
5. 問題なし → コミット
```

---

### ドキュメント削除時

```
1. 削除操作チェックリストを使用（手動）
   ↓
2. search-env-var.shで使用箇所を確認（自動）
   ↓
3. 使用箇所0件を確認（手動）
   ↓
4. 削除実行（手動）
   ↓
5. scripts/配下のツールで検証（自動）
   └─ count-files.sh
   ↓
6. tools/verification/配下のツールで検証（自動）
   └─ v2_validator.py
   ↓
7. 問題なし → コミット
```

---

## セットアップ

### scripts/配下のツール

```bash
# 実行権限を付与
chmod +x scripts/*.sh

# 動作確認
./scripts/count-files.sh
```

---

### tools/verification/配下のツール

```bash
# ディレクトリに移動
cd tools/verification

# 依存関係をインストール
make install

# または手動で
pip install -r requirements.txt
pip install -e .

# 動作確認
python3 validators/v2_validator.py ../../docs
```

---

## トラブルシューティング

### ツールが動作しない

**対応**:
1. 実行権限を確認: `chmod +x scripts/*.sh`
2. 依存コマンドを確認: `git`, `rg`, `python3`
3. カレントディレクトリを確認: プロジェクトルートで実行

---

### 警告が出た

**対応**:
1. 警告内容を確認
2. 該当箇所を修正
3. 再度検証
4. 警告が消えるまで繰り返す

**警告を無視しないでください。**

---

## 関連ドキュメント

- **[手動チェック](06_manual-checks.md)** - 4つのチェックリスト
- **[日常的な作業フロー](09_daily-workflow.md)** - 新規作成・更新・削除
- **[公開リソース一覧](12_resources.md)** - 全リソースの一覧


---

**最終更新**: 2025-11-01
**メンテナー**: ドキュメントチーム
