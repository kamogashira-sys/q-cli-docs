# オートコンプリート機能

**最終更新**: 2025-10-11  
**ステータス**: ⚠️ **未実装機能**

---

## ⚠️ 重要な注意事項

**この機能は現在実装されていません。**

このドキュメントは将来の実装予定機能について記載していますが、現在のQ CLI（v1.17.0時点）では以下の機能は利用できません：

- ❌ `q inline`コマンド
- ❌ 500+のCLIツールに対するオートコンプリート
- ❌ インライン補完機能

---

## 📋 計画中の機能

将来的に以下の機能が実装される可能性があります：

### 主要なCLIツールのサポート（計画）
- **バージョン管理**: git, svn
- **AWS**: aws, sam, cdk
- **コンテナ**: docker, kubectl, helm
- **パッケージマネージャー**: npm, yarn, pip, cargo
- **その他**: terraform, ansible, など

### 総数（計画）
500+のCLIツールをサポート予定

---

## 🚀 使用方法（計画）

### 基本的な使い方（計画）

1. コマンドを入力開始
2. Tabキーを押す
3. Amazon Qが候補を表示

### インライン補完（計画）

```bash
# q inlineコマンドで有効化（未実装）
q inline
```

---

## 📖 現在利用可能な機能

現在のQ CLIでは、以下の機能が利用可能です：

### チャット内でのコマンド補完
```bash
# チャット内で/コマンドの補完が利用可能
q chat
# /help, /clear, /checkpoint などのコマンドが補完される
```

### シェル統合
```bash
# シェル統合の確認
q diagnostic
```

---

## 📚 関連ドキュメント

- [インストールガイド](../01_getting-started/01_installation.md)
- [サポート環境](../07_reference/supported-environments.md)
- [コマンドリファレンス](../07_reference/commands.md)
- [チャット機能](01_chat.md)

---

## 📝 実装状況の確認

最新の実装状況については、以下を確認してください：

- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)
- [ロードマップ](https://github.com/aws/amazon-q-developer-cli/issues?q=is%3Aissue+is%3Aopen+label%3Aroadmap)
- [リリースノート](https://github.com/aws/amazon-q-developer-cli/releases)

---

最終更新: 2025-10-09
