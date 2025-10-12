# 最初の一歩 - Amazon Q CLIの基本操作

**最終更新**: 2025-10-11

---

## 📋 前提条件

このガイドを始める前に、以下を完了してください：

- [インストール](01_installation.md)
- [クイックスタート](02_quick-start.md)

---

## 🎯 このガイドで学ぶこと

- チャットの基本操作
- ファイル操作
- コマンド実行
- Agent切り替え
- 履歴管理

---

## 💬 チャットの基本操作

### Amazon Q CLIの起動

```bash
q
```

### 基本的な質問

```
> What is the difference between Python and JavaScript?
```

Amazon Q CLIが詳しく説明してくれます。

### コードの生成

```
> Write a function to calculate factorial in Python
```

### コードの説明

```
> Explain this code:
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```

### マルチターン会話

```
> Create a Python class for a simple calculator

# Amazon Q CLIが応答

> Add a method to calculate square root

# Amazon Q CLIが前の文脈を理解して追加
```

---

## 📁 ファイル操作

### ファイルの読み込み

Amazon Q CLIは自動的にカレントディレクトリのファイルにアクセスできます。

```
> Read the contents of README.md
```

### ファイルの作成

```
> Create a file named test.py with a simple hello world program
```

Amazon Q CLIがファイルを作成します。

### ファイルの編集

```
> Modify test.py to accept a name as command line argument
```

Amazon Q CLIがファイルを編集します。

### 複数ファイルの操作

```
> Create a Python project with main.py, utils.py, and README.md
```

---

## ⚙️ コマンド実行

### シンプルなコマンド

```
> Run ls -la
```

Amazon Q CLIがコマンドを実行し、結果を表示します。

### 複雑なコマンド

```
> Find all Python files in the current directory and count lines of code
```

Amazon Q CLIが適切なコマンドを生成・実行します。

### Git操作

```
> Show git status

> Create a new branch named feature/new-feature

> Commit all changes with message "Add new feature"
```

---

## 🤖 Agent切り替え

### デフォルトAgentの確認

```bash
q settings chat.defaultAgent
```

### 利用可能なAgentの確認

```bash
q agent list
```

### Agent切り替え（チャット内）

```
> /agent aws-specialist
```

### Agent切り替え（起動時）

```bash
q --agent aws-specialist
```

---

## 📜 履歴管理

### チャット履歴の表示

```
> /history
```

### 履歴の検索

```
> /history search "Python"
```

### 会話の保存

```
> /save my-conversation
```

### 会話の読み込み

```
> /load my-conversation
```

---

## 🎨 便利な機能

### コンテキストの追加

```
> /context add README.md
```

特定のファイルをコンテキストに追加します。

### Knowledge Baseの使用

```
> /knowledge search "authentication"
```

Knowledge Baseから情報を検索します。

### TODOリストの管理

```
> /todos view

> /todos delete

> /todos clear-finished
```

---

## ⌨️ キーボードショートカット

### チャット中

- `Ctrl+C`: 現在の入力をキャンセル
- `Ctrl+D`: チャットを終了
- `↑` / `↓`: 履歴を遡る
- `Tab`: 補完（コマンド名など）

### コマンドモード

- `/help`: ヘルプを表示
- `/quit`: チャットを終了
- `/clear`: 画面をクリア

---

## 🔧 設定のカスタマイズ

### 設定の確認

```bash
q settings all
```

### 設定の変更

```bash
# デフォルトAgentの変更
q settings chat.defaultAgent my-agent

# Markdown表示の無効化
q settings chat.disableMarkdownRendering true

# 履歴ヒントの有効化
q settings chat.enableHistoryHints true
```

### 設定ファイルの編集

```bash
q settings open
```

---

## 💡 Tips & Tricks

### 1. 明確な指示を出す

❌ **悪い例**:
```
> Fix this
```

✅ **良い例**:
```
> Fix the syntax error in line 10 of main.py
```

### 2. コンテキストを提供する

```
> I'm working on a Flask web application. Create a route for user login.
```

### 3. 段階的に進める

```
> Create a basic Flask app

# 確認後

> Add user authentication

# 確認後

> Add database integration
```

### 4. 結果を確認する

Amazon Q CLIが生成したコードやコマンドは、実行前に必ず確認しましょう。

---

## 🐛 よくある問題

### Amazon Q CLIが応答しない

**解決方法**:
1. `Ctrl+C`で現在の処理をキャンセル
2. Amazon Q CLIを再起動: `/quit` → `q`

### ファイルが見つからない

**解決方法**:
1. カレントディレクトリを確認: `pwd`
2. 正しいディレクトリに移動してからQ CLIを起動

### 認証エラー

**解決方法**:
```bash
q auth refresh
```

---

## 📚 次のステップ

### 機能を深く学ぶ

- **[チャット機能](../02_features/01_chat.md)** - チャット機能の詳細
- **[Agent機能](../02_features/02_agents.md)** - Agentのカスタマイズ
- **[MCP 設定](../03_configuration/06_mcp-configuration.md)** - 外部ツールとの連携

### 設定を最適化する

- **[設定ガイド](../03_configuration/01_overview.md)** - 設定の全体像
- **[ベストプラクティス](../04_best-practices/01_configuration.md)** - 推奨設定

### 問題解決

- **[トラブルシューティング](../06_troubleshooting/02_common-issues.md)** - よくある問題
- **[FAQ](../06_troubleshooting/01_faq.md)** - よくある質問

---

## 🔗 関連リンク

- [クイックスタート](02_quick-start.md) - 5分で始める
- [インストールガイド](01_installation.md) - 詳細なインストール手順
- [GitHub リポジトリ](https://github.com/aws/amazon-q-developer-cli)

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11
