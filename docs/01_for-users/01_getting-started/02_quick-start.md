[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [Getting Started](README.md) > 02 Quick Start

---

# クイックスタート - 5分で始めるQ CLI

**対象**: すぐに試したい方  
最終更新: 2025-10-15

> 💡 **詳細なインストール手順が必要な方**: [インストールガイド](01_installation.md)を参照

---

## 🎯 このガイドで学ぶこと

- 最短でのインストール
- 初回起動と認証
- 最初のチャット

---

## ステップ1: インストール（1分）

### macOS

```bash
brew install --cask amazon-q
```

### Linux（Ubuntu/Debian）

**Ubuntu/Debianの場合（.debパッケージ）**:

```bash
# ダウンロード
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb

# インストール
sudo apt-get install -f
sudo dpkg -i amazon-q.deb
```

**その他のLinuxディストリビューション（ZIPファイル）**:

```bash
# x86-64の場合
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip" \
  -o "q.zip"
unzip q.zip
./q/install.sh

# ARM (aarch64)の場合
curl --proto '=https' --tlsv1.2 -sSf \
  "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-aarch64-linux.zip" \
  -o "q.zip"
unzip q.zip
./q/install.sh
```

> 💡 **その他のOS・詳細な手順**: [インストールガイド](01_installation.md)を参照

### インストール確認

```bash
q --version
```

**期待される出力**: `q 1.17.1`

---

## ステップ2: 初回起動と認証（2分）

### Amazon Q CLIの起動

```bash
q
```

### 認証

初回起動時、ブラウザが自動的に開きます。AWS Builder IDまたはIAM Identity Centerで認証してください。

**認証完了の確認**:
```bash
✓ Authentication successful
Welcome to Amazon Q CLI!
```

> 💡 **認証の詳細・トラブルシューティング**: [インストールガイド - 認証設定](01_installation.md#-認証設定)を参照

---

## ステップ3: 最初のチャット（2分）

### 簡単な質問

Amazon Q CLIは日本語での質問に対応しています。自然な日本語で質問してみましょう。

```
> こんにちは、Q！
```

**Q CLIの応答例**:
```
こんにちは！Amazon Q CLIです。何かお手伝いできることはありますか？
```

#### 技術的な質問をしてみる

```
> Pythonとは何ですか？
```

**Q CLIの応答例**:
```
Pythonは、読みやすく書きやすい高水準プログラミング言語です。
Web開発、データ分析、機械学習、自動化スクリプトなど、
幅広い用途で使われています。

Pythonについて、何か具体的に知りたいことはありますか？
```

#### AWSサービスについて質問

```
> S3バケットの作成方法を教えてください
```

**Q CLIの応答例**:
```
S3バケットを作成する方法をご案内します。

AWS CLIを使用する場合：
aws s3 mb s3://your-bucket-name --region us-east-1

または、`q translate`コマンドで自然言語から生成することもできます：
q translate "Create an S3 bucket called 'my-bucket' on us-east-1"

バケット名は全世界で一意である必要があります。
他に知りたいことはありますか？
```

### コマンド生成を試す（q translate）

Amazon Q CLIは`q translate`コマンドで自然言語をシェルコマンドに変換できます。

```bash
# 10秒からカウントダウン（日本語でも可能）
q translate "10秒からカウントダウン"
```

**生成されるコマンド例**:
```bash
Shell · for i in {10..0}; do echo $i; sleep 1; done
```

**インタラクティブメニュー**:
- `Execute command` - コマンドを実行
- `Edit command` - コマンドを編集
- `Regenerate answer` - 別のコマンドを生成
- `Ask another question` - 別の質問をする
- `Cancel` - キャンセル

**その他の例**:
```bash
# S3バケットを作成
q translate "Create an S3 bucket called 'my-bucket' on us-west-2"

# HTMLファイルを作成
q translate "Create a simple index.html file with 'Hello World' message"
```

### コード生成を試す（q chat）

```
> Create a Python script that prints "Hello, World!"
```

**Q CLIの応答例**:
```python
# hello.py
print("Hello, World!")
```

### ファイル操作を試す

```
> Create this file as hello.py
```

Amazon Q CLIがファイルを作成します。

### 実行確認

```bash
python hello.py
```

**出力**: `Hello, World!`

### トラブルシューティング

エラーが発生した場合は、`q chat`を使用してヘルプを求めることができます。

```bash
q chat "Help me resolve this error"
```

または、対話モードで直接質問することもできます：

```bash
q chat
# チャット内で質問
> I got an error when running the command. How can I fix it?
```

> 💡 **詳しい使用例**:
> - [Amazon Q Developer を活用し自然言語を使って簡単に AWS CLI コマンドを実行（日本語）](https://aws.amazon.com/jp/blogs/news/effortlessly-execute-aws-cli-commands-using-natural-language-with-amazon-q-developer/)
>   - S3とCloudFrontで静的ウェブサイトを構築する実践的なチュートリアル
>   - `q translate`と`q chat`の使い方
>   - トラブルシューティングの例も含む

---

## 🎉 完了！

おめでとうございます！Q CLIの基本的な使い方を学びました。

---

## 💡 便利なコマンド

### ヘルプの表示

```
> /help
```

### 設定の確認

```bash
q settings list
```

### チャットの終了

```
> /quit
```

または `Ctrl+D`

---

## 📚 次のステップ

### さらに学ぶ

- **[最初の一歩](03_first-steps.md)** - より詳しい使い方
- **[チャット機能](../02_features/01_chat.md)** - チャット機能の詳細
- **[Agent機能](../02_features/02_agents.md)** - Agentのカスタマイズ

### 設定をカスタマイズ

- **[設定ガイド](../03_configuration/01_overview.md)** - 設定の全体像
- **[Agent設定](../03_configuration/03_agent-configuration.md)** - Agent設定の詳細
- **[設定例集](../03_configuration/08_examples.md)** - 実践的な設定例

### 問題が発生した場合

- **[よくある問題](../06_troubleshooting/02_common-issues.md)** - トラブルシューティング
- **[FAQ](../06_troubleshooting/01_faq.md)** - よくある質問

---

## 🔗 関連リンク

- [インストールガイド](01_installation.md) - 詳細なインストール手順
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)
- [AWS 公式サイト](https://aws.amazon.com/q/developer/)

---

## 📖 ナビゲーション

← **前へ**: [インストール](01_installation.md) | **次へ**: [最初の一歩](03_first-steps.md) →

---

**作成日**: 2025-10-11  
最終更新: 2025-10-18
---

**関連トピック**:
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [FAQ](../06_troubleshooting/01_faq.md)
