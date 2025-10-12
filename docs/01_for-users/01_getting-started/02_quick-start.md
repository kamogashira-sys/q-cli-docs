# クイックスタート - 5分で始めるQ CLI

**所要時間**: 約5分  
**最終更新**: 2025-10-11

---

## 🎯 このガイドで学ぶこと

- Amazon Q CLIのインストール
- 初回起動と認証
- 最初のチャット
- 基本的なコマンド

---

## ステップ1: インストール（1分）

### macOS

```bash
brew install amazon-q
```

### Linux（Ubuntu/Debian）

```bash
curl -fsSL https://d2eo22ngex1n9g.cloudfront.net/releases/amazon-q-developer-cli/latest/install.sh | bash
```

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

初回起動時、ブラウザが自動的に開きます：

1. **AWSアカウントでサインイン**
   - AWS Builder IDまたはIAM Identity Centerを選択
   - 認証情報を入力

2. **認証完了の確認**
   ```bash
   ✓ Authentication successful
   Welcome to Amazon Q CLI!
   ```

3. **認証状態の確認**
   ```bash
   q login --help
   ```

**トラブルシューティング**:
- ブラウザが開かない場合: `q login --no-browser`
- 認証エラーの場合: [認証トラブルシューティング](../06_troubleshooting/common-issues.md#認証関連)を参照

---

## ステップ3: 最初のチャット（2分）

### 簡単な質問

```
> Hello, Q! What can you do?
```

**Q CLIの応答例**:
```
Hello! I'm Amazon Q CLI. I can help you with:
- Writing and debugging code
- Explaining technical concepts
- Running commands on your system
- Managing files and directories
- And much more!

What would you like to do today?
```

### コード生成を試す

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
q settings all
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

- **[設定ガイド](../03_configuration/overview.md)** - 設定の全体像
- **[Agent設定](../03_configuration/agent-configuration.md)** - Agent設定の詳細
- **[設定例集](../03_configuration/examples.md)** - 実践的な設定例

### 問題が発生した場合

- **[よくある問題](../06_troubleshooting/common-issues.md)** - トラブルシューティング
- **[FAQ](../06_troubleshooting/faq.md)** - よくある質問

---

## 🔗 関連リンク

- [インストールガイド](01_installation.md) - 詳細なインストール手順
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)
- [AWS 公式サイト](https://aws.amazon.com/q/developer/)

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
