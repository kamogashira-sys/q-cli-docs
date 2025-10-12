# 貢献ガイド

Amazon Q CLIへの貢献に興味を持っていただき、ありがとうございます！このガイドでは、プロジェクトへの貢献方法を説明します。

## 📋 目次

- [貢献の種類](#貢献の種類)
- [始める前に](#始める前に)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [コードの貢献](#コードの貢献)
- [ドキュメントの貢献](#ドキュメントの貢献)
- [レビュープロセス](#レビュープロセス)

---

## 貢献の種類

### 1. コードの貢献
- バグ修正
- 新機能の実装
- パフォーマンス改善
- テストの追加

### 2. ドキュメントの貢献
- ドキュメントの改善
- チュートリアルの作成
- 翻訳
- 誤字脱字の修正

### 3. コミュニティ活動
- バグ報告
- 機能リクエスト
- 質問への回答
- ディスカッションへの参加

---

## 始める前に

### 1. 既存のIssueを確認
重複を避けるため、既存のIssueを確認：
- [Open Issues](https://github.com/aws/amazon-q-developer-cli/issues)
- [Discussions](https://github.com/aws/amazon-q-developer-cli/discussions)

### 2. Issueの作成
新しい貢献の場合、まずIssueを作成：
- バグ報告: バグレポートテンプレートを使用
- 機能リクエスト: 機能リクエストテンプレートを使用
- その他: 詳細な説明を記載

### 3. 承認を待つ
大きな変更の場合、実装前にメンテナーの承認を待つ：
- Issueでディスカッション
- 設計の合意
- 実装方針の確認

---

## 開発環境のセットアップ

### 前提条件
- Rust 1.70以上
- Node.js 18以上（テスト用）
- Git

### セットアップ手順

1. **リポジトリのフォーク**:
   ```bash
   # GitHubでフォークボタンをクリック
   ```

2. **クローン**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/amazon-q-developer-cli.git
   cd amazon-q-developer-cli
   ```

3. **依存関係のインストール**:
   ```bash
   cargo build
   ```

4. **テストの実行**:
   ```bash
   cargo test
   ```

5. **ローカルでの実行**:
   ```bash
   cargo run -- chat "Hello"
   ```

詳細は[開発環境セットアップガイド](../../02_for-developers/01_contributing/development-setup.md)を参照。

---

## コードの貢献

### 1. ブランチの作成

```bash
# 最新のmainブランチを取得
git checkout main
git pull upstream main

# 新しいブランチを作成
git checkout -b feature/your-feature-name
```

ブランチ命名規則：
- `feature/`: 新機能
- `fix/`: バグ修正
- `docs/`: ドキュメント
- `refactor/`: リファクタリング

### 2. コードの実装

#### コーディング規約
- Rustの標準スタイルガイドに従う
- `cargo fmt`でフォーマット
- `cargo clippy`で静的解析

#### テストの追加
すべての新機能とバグ修正にテストを追加：

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_your_feature() {
        // テストコード
    }
}
```

#### ドキュメントの更新
コードの変更に応じてドキュメントを更新：
- コード内のドキュメントコメント
- README.md
- 関連するユーザーガイド

### 3. コミット

```bash
# 変更をステージング
git add .

# コミット（明確なメッセージ）
git commit -m "feat: add new feature X"
```

コミットメッセージ規約：
- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメント
- `test:` テスト
- `refactor:` リファクタリング
- `chore:` その他

### 4. プッシュとPR作成

```bash
# フォークにプッシュ
git push origin feature/your-feature-name
```

GitHubでPRを作成：
1. "Compare & pull request"をクリック
2. PRテンプレートに従って記入
3. レビュアーを待つ

詳細は[PRガイドライン](../../02_for-developers/01_contributing/pull-request-guide.md)を参照。

---

## ドキュメントの貢献

### ドキュメント構造
```
docs/
├── 01_getting-started/    # 初心者向け
├── user-guide/         # ユーザーガイド
├── developer-guide/    # 開発者向け
├── reference/          # リファレンス
└── community/          # コミュニティ
```

### ドキュメント作成のガイドライン

#### 1. Markdown形式
- 標準的なMarkdown記法を使用
- 見出しは階層的に（H1 → H2 → H3）
- コードブロックには言語を指定

#### 2. 構造
各ドキュメントに含めるべき要素：
- 目次（長いドキュメントの場合）
- 明確な見出し
- 実例とコード例
- 関連ドキュメントへのリンク

#### 3. スタイル
- 簡潔で明確な文章
- 技術用語は初出時に説明
- スクリーンショットは必要に応じて追加

### ドキュメントのテスト
- リンク切れの確認
- コード例の動作確認
- 誤字脱字のチェック

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
レビューコメントに対応：
```bash
# 修正を実施
git add .
git commit -m "fix: address review comments"
git push origin feature/your-feature-name
```

### 4. マージ
承認後、メンテナーがマージ：
- Squash and merge（通常）
- Merge commit（大きな機能）

---

## 📚 関連ドキュメント

- [開発環境セットアップ](../../02_for-developers/01_contributing/development-setup.md)
- [PRガイドライン](../../02_for-developers/01_contributing/pull-request-guide.md)
- [アーキテクチャ概要](../../02_for-developers/02_architecture/overview.md)

---

## 🆘 ヘルプが必要な場合

### 質問
- [GitHub Discussions](https://github.com/aws/amazon-q-developer-cli/discussions)で質問
- [Stack Overflow](https://stackoverflow.com/questions/tagged/amazon-q)（タグ: amazon-q）

### 問題報告
- [GitHub Issues](https://github.com/aws/amazon-q-developer-cli/issues)で報告

---

## 🙏 謝辞

あなたの貢献がAmazon Q CLIをより良いものにします。ご協力ありがとうございます！

最終更新: 2025-10-09
