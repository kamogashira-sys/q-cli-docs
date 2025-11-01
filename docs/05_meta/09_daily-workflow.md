[ホーム](../README.md) > [Meta](README.md) > 日常的な作業フロー

---

# 日常的な作業フロー

本サイトでの日常的な作業フローを、シーン別に説明します。

---

## 新規ドキュメント作成時

### ステップ1: ソースコードを確認

```bash
# Q CLIソースコードをクローン（初回のみ）
git clone https://github.com/aws/amazon-q-developer-cli.git

# 最新版に更新
cd amazon-q-developer-cli
git pull

# 対象機能のソースコードを確認
rg "機能名" --type rust
```

---

### ステップ2: 実装照合チェックリストを使用

[手動チェック](06_manual-checks.md)の実装照合チェックリストを使用：

- [ ] ソースコードを確認したか
- [ ] テストコードを確認したか
- [ ] JSON Schemaを確認したか
- [ ] デフォルト値を確認したか
- [ ] 環境変数の定義を確認したか

---

### ステップ3: ドキュメントを作成

確認した内容を基に、ドキュメントを作成。

**重要な原則**:
- ❌ 推測で書かない
- ✅ すべてソースコードで確認

---

### ステップ4: 動作確認チェックリストを使用

[手動チェック](06_manual-checks.md)の動作確認チェックリストを使用：

- [ ] コマンドを実行したか
- [ ] 設定ファイルを適用したか
- [ ] エラーメッセージを確認したか
- [ ] 期待通りの動作をしたか

---

### ステップ5: 自動化ツールで検証

```bash
# ファイル数チェック
./scripts/count-files.sh

# 日付チェック
./scripts/check-dates.sh docs/

# v2.0バリデーター
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

---

### ステップ6: コミット

```bash
git add docs/
git commit -m "docs: 新規ドキュメント追加"
git push origin your-branch
```

---

## ドキュメント更新時

### ステップ1: 変更内容を明確化

- 何を変更するのか
- なぜ変更するのか
- 影響範囲はどこか

---

### ステップ2: ソースコードを確認（必要に応じて）

技術的な内容を変更する場合は、必ずソースコードを確認。

---

### ステップ3: 影響範囲を確認

```bash
# リンクを確認
grep -r "変更するファイル名" docs/

# 環境変数を確認（環境変数を変更する場合）
./scripts/search-env-var.sh 環境変数名
```

---

### ステップ4: ドキュメントを更新

変更内容を反映。

---

### ステップ5: 日付を更新

```markdown
最終更新: 2025-11-01
```

---

### ステップ6: 自動化ツールで検証

```bash
# 日付チェック
./scripts/check-dates.sh docs/

# v2.0バリデーター
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

---

### ステップ7: コミット

```bash
git add docs/
git commit -m "docs: ドキュメント更新"
git push origin your-branch
```

---

## ドキュメント削除時

### ステップ1: 削除操作チェックリストを使用

[手動チェック](06_manual-checks.md)の削除操作チェックリストを使用：

- [ ] 使用箇所を検索したか
- [ ] 使用箇所が0件か確認したか
- [ ] 削除後に検証したか

---

### ステップ2: 使用箇所を確認

```bash
# ファイル名で検索
grep -r "削除するファイル名" docs/

# 環境変数で検索（環境変数を削除する場合）
./scripts/search-env-var.sh 環境変数名
```

**使用箇所が0件であることを確認してください。**

---

### ステップ3: 削除実行

```bash
git rm docs/削除するファイル
```

---

### ステップ4: 自動化ツールで検証

```bash
# ファイル数チェック
./scripts/count-files.sh

# v2.0バリデーター
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

---

### ステップ5: コミット

```bash
git commit -m "docs: ドキュメント削除"
git push origin your-branch
```

---

## 定期チェック

### 週次チェック

```bash
# 日付整合性チェック
./scripts/check-dates.sh docs/

# v2.0バリデーター
cd tools/verification
python3 validators/v2_validator.py ../../docs
```

---

### 月次チェック

```bash
# ファイル数チェック
./scripts/count-files.sh

# 全ツール実行
cd tools/verification
make validate-all

# Q CLIの新バージョン確認
q --version
```

**新バージョンがリリースされた場合**:  
[バージョンアップ対応ガイド](10_version-update-guide.md)を参照してください。

---

## トラブルシューティング

### 自動化ツールで警告が出た

**対応**:
1. 警告内容を確認
2. 該当箇所を修正
3. 再度検証
4. 警告が消えるまで繰り返す

**警告を無視しないでください。**

---

### リンク切れが発生した

**対応**:
1. リンク先のファイルが存在するか確認
2. ファイル名が正しいか確認
3. パスが正しいか確認
4. 修正して再度検証

---

### 日付が不一致

**対応**:
1. Git最終更新日を確認
2. ドキュメント記載日を更新
3. 再度検証

---

## 作業原則の実践

### 原則1: 品質優先

- 時間よりも正確性を優先
- 妥協しない

### 原則2: 自動化の価値

- 自動化ツールを必ず実行
- 手動作業を削減

### 原則8: 作業効率を求めない

- 品質を犠牲にした効率化はしない
- 最初から正確に作業する

### 原則9: 全体把握の徹底

- 影響範囲を確認してから作業
- 使用箇所を確認してから削除

---

## 次に読むべきドキュメント

### 詳細を知りたい方

1. **[9つの作業原則](04_quality-principles.md)** - 品質を保つルール
2. **[自動化ツール](05_automation-tools.md)** - scripts + tools/verification
3. **[手動チェック](06_manual-checks.md)** - 4つのチェックリスト

### バージョンアップ対応

1. **[バージョンアップ対応](10_version-update.md)** - Q CLIバージョンアップ時の手順

---

最終更新: 2025-11-01
