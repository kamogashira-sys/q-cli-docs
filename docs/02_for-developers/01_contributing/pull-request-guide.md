# プルリクエストガイド

Amazon Q CLIへのプルリクエスト（PR）作成ガイドです。

## 📋 目次

- [PR作成前のチェックリスト](#pr作成前のチェックリスト)
- [PRの作成手順](#prの作成手順)
- [PRテンプレート](#prテンプレート)
- [レビュープロセス](#レビュープロセス)
- [マージ後](#マージ後)

---

## PR作成前のチェックリスト

### 必須項目
- [ ] 関連するIssueが存在する（または作成済み）
- [ ] ブランチ名が規約に従っている
- [ ] すべてのテストが通過している
- [ ] コードがフォーマットされている（`cargo fmt`）
- [ ] 静的解析が通過している（`cargo clippy`）
- [ ] ドキュメントが更新されている

### 推奨項目
- [ ] コミットメッセージが明確
- [ ] 変更が小さく、レビューしやすい
- [ ] 新機能にはテストが追加されている
- [ ] 破壊的変更がある場合は明記されている

---

## PRの作成手順

### 1. ブランチの準備

```bash
# 最新のmainブランチを取得
git checkout main
git pull upstream main

# 作業ブランチを作成
git checkout -b feature/your-feature-name
```

### 2. 変更の実装

```bash
# コードを実装
# ...

# テストを実行
cargo test

# フォーマット
cargo fmt

# 静的解析
cargo clippy
```

### 3. コミット

```bash
# 変更をステージング
git add .

# コミット（明確なメッセージ）
git commit -m "feat: add new feature X"
```

**コミットメッセージ規約**:
- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメント
- `test:` テスト
- `refactor:` リファクタリング
- `chore:` その他

### 4. プッシュ

```bash
# フォークにプッシュ
git push origin feature/your-feature-name
```

### 5. PR作成

1. GitHubでフォークのページを開く
2. "Compare & pull request"をクリック
3. PRテンプレートに従って記入
4. "Create pull request"をクリック

---

## PRテンプレート

### タイトル
```
feat: Add support for feature X
```

### 説明

```markdown
## 概要
この変更の目的と内容を簡潔に説明

## 関連Issue
Closes #123

## 変更内容
- 変更点1
- 変更点2
- 変更点3

## テスト
- [ ] 既存のテストが通過
- [ ] 新しいテストを追加
- [ ] 手動テストを実施

## チェックリスト
- [ ] コードがフォーマットされている
- [ ] 静的解析が通過している
- [ ] ドキュメントが更新されている
- [ ] 破壊的変更がある場合は明記

## スクリーンショット（該当する場合）
変更前後の比較など

## 追加情報
その他の補足情報
```

---

## レビュープロセス

### 1. 自動チェック
PRを作成すると自動的に実行：
- CI/CDパイプライン
- コードフォーマットチェック
- テストの実行
- 静的解析

### 2. コードレビュー
メンテナーがレビュー：
- コードの品質
- テストの網羅性
- ドキュメントの完全性
- 設計の妥当性

### 3. フィードバックへの対応

```bash
# レビューコメントに対応
# コードを修正

# コミット
git add .
git commit -m "fix: address review comments"

# プッシュ
git push origin feature/your-feature-name
```

### 4. 承認とマージ
- レビュアーが承認（Approve）
- メンテナーがマージ

---

## マージ後

### 1. ブランチのクリーンアップ

```bash
# ローカルブランチを削除
git checkout main
git branch -d feature/your-feature-name

# リモートブランチを削除（GitHubで自動削除されない場合）
git push origin --delete feature/your-feature-name
```

### 2. 最新のmainブランチを取得

```bash
git pull upstream main
```

### 3. 次の作業へ
新しいブランチを作成して次の作業を開始

---

## よくある質問

### Q: PRが大きくなりすぎた場合は？
A: 複数の小さなPRに分割することを検討してください。レビューが容易になります。

### Q: テストが失敗した場合は？
A: ローカルで`cargo test`を実行して問題を特定し、修正してください。

### Q: レビューコメントに同意できない場合は？
A: 丁寧に理由を説明し、代替案を提案してください。建設的な議論を心がけましょう。

### Q: マージまでどのくらいかかる？
A: PRのサイズや複雑さによりますが、通常1-2週間程度です。

---

## ベストプラクティス

### PRのサイズ
- 小さく保つ（変更行数: 200-400行が理想）
- 1つのPRで1つの機能/修正に集中
- 大きな変更は複数のPRに分割

### コミットメッセージ
- 明確で簡潔に
- 何を変更したかではなく、なぜ変更したかを説明
- 関連Issueを参照

### コードレビュー
- レビューコメントには迅速に対応
- 質問には丁寧に回答
- 建設的なフィードバックを歓迎

---

## 📚 関連ドキュメント

- [貢献ガイド](../../03_for-community/community/contributing.md)
- [開発環境セットアップ](development-setup.md)
- [コーディング規約](README.md)

- **[開発環境セットアップ](development-setup.md)** - [貢献ガイド](../../03_for-community/community/contributing.md)
- [開発環境セットアップ](development-setup.md)
- [コーディング規約](README.md)

- **[コーディング規約](README.md)** - [貢献ガイド](../../03_for-community/community/contributing.md)
- [開発環境セットアップ](development-setup.md)
- [コーディング規約](README.md)


---

最終更新: 2025-10-09
