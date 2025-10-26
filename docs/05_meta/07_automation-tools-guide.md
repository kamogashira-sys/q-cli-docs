[ホーム](../README.md) > [Meta](README.md) > 自動化ツール使用ガイド

---

# 自動化ツール使用ガイド

本サイトの品質検証を自動化する3つのツールの使用方法を説明します。

---

## 📋 ツール概要

| ツール | 機能 | 用途 |
|--------|------|------|
| count-files.sh | ファイル数自動カウント | ファイル数記載時の検証 |
| check-dates.sh | 日付整合性チェック | 日付不一致の検出 |
| search-env-var.sh | 環境変数検索 | 削除操作の安全性確保 |

**配置場所**: `/scripts/`

---

## 🔧 インストール

### 前提条件

**必須**:
- bash（シェルスクリプト実行）
- git（日付チェック用）
- ripgrep（環境変数検索用）

**確認方法**:
```bash
# bashの確認
bash --version

# gitの確認
git --version

# ripgrepの確認
rg --version
```

---

### インストール手順

**ステップ1: リポジトリのクローン**
```bash
git clone https://github.com/your-repo/q-cli-docs.git
cd q-cli-docs
```

**ステップ2: 実行権限の付与**
```bash
chmod +x scripts/*.sh
```

**ステップ3: 動作確認**
```bash
# ファイル数カウント
./scripts/count-files.sh

# 日付チェック
./scripts/check-dates.sh

# 環境変数検索（テスト）
./scripts/search-env-var.sh Q_DEBUG
```

---

## 🔧 count-files.sh

### 目的と機能

**目的**: ファイル数の自動カウント

**機能**:
- 全ファイル数のカウント
- カテゴリ別ファイル数のカウント
- README除外カウント
- docs直下のファイル数

**効果**: 手動カウントによる誤りを完全に排除

---

### 使用方法

**基本的な使用**:
```bash
cd /home/katoh/projects/q-cli-docs
./scripts/count-files.sh
```

**出力例**:
```
=== ファイル数カウント ===

全ファイル数: 109

カテゴリ別:
  01_for-users: 73 文書
  02_for-developers: 11 文書
  03_for-community: 14 文書
  04_issues: 1 文書
  05_meta: 5 文書

README除外: 88 文書

docs直下: 5 文書
```

---

### 結果の解釈

**全ファイル数**:
- docs配下の全.mdファイル
- README.mdを含む

**カテゴリ別**:
- 各ディレクトリ配下のファイル数
- サブディレクトリを含む

**README除外**:
- README.mdを除いたファイル数
- 実質的なドキュメント数

**docs直下**:
- docsディレクトリ直下のファイル数
- index.md、README.md等

---

### 使用タイミング

**ドキュメント作成時**:
- ファイル数を記載する前に実行
- 正確な数値を取得

**定期チェック時**:
- 週次チェックで実行
- ファイル数の変化を確認

**リリース前**:
- 最終確認として実行
- ドキュメント数の正確性を保証

---

## 🔧 check-dates.sh

### 目的と機能

**目的**: 日付整合性の自動チェック

**機能**:
- Git更新日の取得
- ドキュメント内日付の抽出
- 両者の比較
- 不一致の検出と出力

**効果**: 42件の日付不一致を自動検出

---

### 使用方法

**基本的な使用**:
```bash
cd /home/katoh/projects/q-cli-docs
./scripts/check-dates.sh
```

**出力例**:
```
=== 日付整合性チェック ===

❌ docs/05_meta/README.md
   Git: 2025-10-26, Doc: 2025-10-11
❌ docs/index.md
   Git: 2025-10-26, Doc: 2025-10-18
❌ docs/file-structure.md
   Git: 2025-10-26, Doc: 2025-10-19

✅ 67ファイルが一致
❌ 42ファイルが不一致
```

---

### 結果の解釈

**一致**:
- Git更新日とドキュメント内日付が同じ
- 問題なし

**不一致**:
- Git更新日とドキュメント内日付が異なる
- 以下のいずれか:
  1. 軽微な修正（日付更新不要）
  2. 日付更新漏れ（要確認）

**判断基準**:
- タイポ修正: 更新不要
- リンク修正: 更新不要
- フォーマット調整: 更新不要
- 内容の大幅変更: 更新必要
- 新規セクション追加: 更新必要

---

### 使用タイミング

**ドキュメント更新後**:
- 更新完了後に実行
- 日付更新の必要性を確認

**定期チェック時**:
- 週次チェックで実行
- 日付不一致の確認

**リリース前**:
- 最終確認として実行
- 日付の正確性を保証

---

## 🔧 search-env-var.sh

### 目的と機能

**目的**: 環境変数の使用箇所検索

**機能**:
- 環境変数の使用箇所を全検索
- 使用箇所数のカウント
- 削除可否の判定支援
- Q CLIリポジトリパスチェック

**効果**: 削除操作の安全性を確保

---

### 使用方法

**基本的な使用**:
```bash
cd /home/katoh/projects/q-cli-docs
./scripts/search-env-var.sh Q_DEBUG
```

**出力例**:
```
=== 環境変数検索: Q_DEBUG ===

Q CLIリポジトリ: /tmp/q-cli-verification/amazon-q-developer-cli

検索結果:
crates/chat-cli/src/util/consts.rs:15:    pub const Q_DEBUG: &str = "Q_DEBUG";
crates/chat-cli/src/cli/settings.rs:42:        env::var("Q_DEBUG").is_ok()
crates/chat-cli/src/main.rs:28:    if env::var("Q_DEBUG").is_ok() {

使用箇所数: 3

判定: ❌ 削除不可（使用箇所あり）
```

---

### 結果の解釈

**使用箇所数: 0**:
- 実装で使用されていない
- 削除可能（要レビュー）

**使用箇所数: 1+**:
- 実装で使用されている
- 削除不可

**判定**:
- ✅ 削除可能: 使用箇所0件
- ❌ 削除不可: 使用箇所あり

---

### 使用タイミング

**環境変数削除前**（必須）:
```bash
# ステップ1: 使用箇所確認
./scripts/search-env-var.sh Q_VARIABLE_NAME

# ステップ2: 使用箇所0件を確認
# 使用箇所数: 0

# ステップ3: レビュー承認を取得

# ステップ4: 削除実行

# ステップ5: 再確認
./scripts/search-env-var.sh Q_VARIABLE_NAME
```

**定期チェック時**:
- 月次チェックで実行
- 未使用環境変数の確認

---

## 🔄 トラブルシューティング

### count-files.sh

**問題**: ファイル数が0と表示される

**原因**: docsディレクトリが存在しない

**解決方法**:
```bash
# プロジェクトルートで実行
cd /home/katoh/projects/q-cli-docs
./scripts/count-files.sh
```

---

### check-dates.sh

**問題**: 全てのファイルで不一致と表示される

**原因**: gitリポジトリでない、またはgit履歴がない

**解決方法**:
```bash
# gitリポジトリの確認
git status

# git履歴の確認
git log --oneline | head -5
```

---

### search-env-var.sh

**問題**: "Q CLIリポジトリが見つかりません"

**原因**: Q CLIリポジトリがクローンされていない

**解決方法**:
```bash
# リポジトリのクローン
mkdir -p /tmp/q-cli-verification
cd /tmp/q-cli-verification
git clone https://github.com/aws/amazon-q-developer-cli.git
```

**問題**: "ripgrepがインストールされていません"

**原因**: ripgrepがインストールされていない

**解決方法**:
```bash
# Ubuntu/Debian
sudo apt install ripgrep

# macOS
brew install ripgrep

# 確認
rg --version
```

---

## 📊 実績データ

### count-files.sh

**Phase 2での使用**:
- 実行回数: 5回
- 検出した誤り: 2件
- 修正時間: 15分

**効果**:
- 手動カウント誤りを完全に排除
- ファイル数の正確性を保証

---

### check-dates.sh

**Phase 2での使用**:
- 実行回数: 3回
- 検出した不一致: 42件
- 全て正当な理由あり

**効果**:
- 日付不一致を自動検出
- 手動確認の手間を削減

---

### search-env-var.sh

**Phase 2での使用**:
- 実行回数: 10回
- 検出した使用箇所: 延べ50+箇所
- 防いだ削除エラー: 推定5件

**効果**:
- 削除操作の安全性を確保
- 誤削除を完全に防止

---

## ✅ まとめ

### 3つのツール

**count-files.sh**:
- ファイル数の自動カウント
- 手動カウント誤りを排除

**check-dates.sh**:
- 日付整合性の自動チェック
- 日付不一致を自動検出

**search-env-var.sh**:
- 環境変数の使用箇所検索
- 削除操作の安全性確保

---

### 使用のポイント

**定期的な実行**:
- 週次: count-files.sh、check-dates.sh
- 月次: 全ツール

**削除前の必須確認**:
- search-env-var.shを必ず実行
- 使用箇所0件を確認

**トラブル時の対応**:
- エラーメッセージを確認
- トラブルシューティングを参照

---

## 📖 関連ドキュメント

- **[品質保証概要](05_quality-assurance-overview.md)** - 品質保証の全体像
- **[品質保証詳細ガイド](06_quality-assurance-detailed-guide.md)** - 詳細なプロセス
- **[チェックリスト活用ガイド](08_checklist-guide.md)** - チェックリストの活用法
- **[作業原則と文化](10_work-principles.md)** - 3つの作業原則
- **[継続的改善ガイド](12_continuous-improvement.md)** - 長期的な品質維持

---

最終更新: 2025-10-26
