# キーボードショートカット

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📖 概要

Amazon Q CLIは、効率的な操作のために多数のキーボードショートカットを提供しています。このドキュメントでは、デフォルトのショートカット、カスタマイズ方法、実用的な使用例を説明します。

---

## ⌨️ デフォルトショートカット一覧

### 基本操作

| ショートカット | 機能 | 説明 |
|--------------|------|------|
| `Ctrl+C` | 入力キャンセル | 現在の入力をキャンセル |
| `Ctrl+D` | チャット終了 | チャットセッションを終了 |
| `↑` / `↓` | 履歴移動 | コマンド履歴を遡る・進む |
| `Tab` | 補完 | コマンド名やパスの補完 |
| `Ctrl+G` | 補完受け入れ | オートコンプリート候補を受け入れ（デフォルト） |

### 入力編集

| ショートカット | 機能 | 説明 |
|--------------|------|------|
| `Ctrl+J` | 改行挿入 | 複数行プロンプトのために改行を挿入 |
| `Alt+Enter` | 改行挿入 | 複数行プロンプトのために改行を挿入（代替） |

### 特殊機能

| ショートカット | 機能 | 説明 | 設定キー |
|--------------|------|------|---------|
| `Ctrl+T` | Tangentモード | サイドトピック探索モードに入る | `chat.tangentModeKey` |
| `Ctrl+S` | コマンド選択メニュー | 55個のコマンドから選択して実行 | `chat.skimCommandKey` |
| `Ctrl+G` | オートコンプリート受け入れ | オートコンプリート候補を受け入れ | `chat.autocompletionKey` |
| `Ctrl+D` | Delegateモード | タスク委譲モードに入る（実験的機能） | `chat.delegateModeKey` |

> **💡 ヒント**: 特殊機能のショートカットは、対応する機能が有効化されている場合のみ動作します。

---

## 📝 複数行入力（Ctrl+J / Alt+Enter）

### 概要

複数行のプロンプトを入力する際に、改行を挿入できます。長いコードや複雑な質問を整形して入力する場合に便利です。

### 使い方

```bash
# Ctrl+Jで改行を挿入
> 以下のコードを修正して：
Ctrl+J
> - エラーハンドリングを追加
Ctrl+J
> - ログ出力を追加
Ctrl+J
> - テストを追加

# Alt+Enterでも同様に改行を挿入可能
> 複数行の
Alt+Enter
> プロンプトを
Alt+Enter
> 入力
```

### ユースケース

- **長いコードの貼り付け**: コードブロックを整形して入力
- **複雑な質問**: 箇条書きで要件を整理
- **段階的な指示**: ステップバイステップの指示を明確に記述

---

## 🎯 Tangentモード（Ctrl+T）

### 概要

Tangentモードは、メインの会話を保持しながらサイドトピックを探索できる機能です。会話のチェックポイントを作成し、後で元の会話に戻ることができます。

### 使い方

#### 1. Tangentモードに入る

チャット中に `Ctrl+T` を押すか、`/tangent` コマンドを実行します。

```bash
# ショートカットで起動
Ctrl+T

# コマンドで起動
> /tangent

Created a conversation checkpoint (↯). Use ctrl + t or /tangent to restore the conversation later.
Note: this functionality is experimental and may change or be removed in the future.

↯ >
```

プロンプトに `↯` マークが表示され、チェックポイントが作成されたことを示します。

#### 2. サイドトピックを探索

Tangentモード中は、メインの会話に影響を与えずに質問や実験ができます。

```bash
# 例: メインの会話でAWS Lambda開発中
> Lambda関数のエラーハンドリングについて教えて

# Tangentモードで関連トピックを探索
Ctrl+T
↯ > CloudWatch Logsの設定方法は？
↯ > X-Rayトレーシングの有効化方法は？
```

#### 3. メインの会話に戻る

再度 `Ctrl+T` または `/tangent` を実行すると、チェックポイントから会話が復元されます。

```bash
# メインの会話に戻る
Ctrl+T

# または
> /tangent

Restored conversation from checkpoint (↯). - Returned to main conversation.

>
```

プロンプトから `↯` マークが消え、メインの会話に戻ったことを示します。

### 設定

```bash
# Tangentモードを有効化
q settings chat.enableTangentMode true

# ショートカットキーをカスタマイズ（デフォルト: t）
q settings chat.tangentModeKey t

# introspectクエリで自動的にTangentモードに入る
q settings introspect.tangentMode true
```

### ユースケース

- **複雑な問題の調査**: メインの問題を解決しながら、関連する技術を調査
- **実験的な質問**: メインの会話を乱さずに、アイデアを試す
- **複数の解決策の検討**: コンテキストを失わずに、異なるアプローチを比較

---

## 🔍 コマンド選択メニュー（Ctrl+S）

### 概要

コマンド選択メニューは、55個の利用可能なコマンドを一覧表示し、矢印キーで選択して実行できる機能です。コマンド名を覚えていなくても、メニューから選択できます。

### 使い方

```bash
# ショートカットで起動
Ctrl+S

# 矢印キーで選択、Enterで実行
↑/↓ でコマンドを選択
Enter で実行
```

### 利用可能なコマンド

コマンド選択メニューには以下のカテゴリのコマンドが含まれます：

- **チャット操作**: `/clear`, `/exit`, `/help`
- **Agent管理**: `/agent swap`, `/agent generate`, `/agent schema`
- **コンテキスト管理**: `/context add`, `/context remove`, `/context show`
- **Knowledge管理**: `/knowledge add`, `/knowledge remove`, `/knowledge list`
- **実験的機能**: `/experiment`, `/tangent`, `/delegate`
- **その他**: `/introspect`, `/settings`, `/version`

### 設定

```bash
# ショートカットキーをカスタマイズ（デフォルト: s）
q settings chat.skimCommandKey s
```

---

## 📋 Delegateモード（Ctrl+D）

### 概要

Delegateモードは、複雑なタスクをQ CLIに委譲し、自動的に実行させる機能です。

> **⚠️ 注意**: この機能は実験的機能です。使用するには `/experiment` コマンドで有効化する必要があります。

### 使い方

```bash
# 実験的機能を有効化
> /experiment
# → Delegate Mode: ON

# ショートカットで起動（設定されている場合）
Ctrl+D

# タスクを指定
> プロジェクトのテストを実行して、失敗したテストを修正して
```

### 設定

```bash
# ショートカットキーを設定（デフォルト値なし）
q settings chat.delegateModeKey d
```

> **💡 ヒント**: DelegateModeKeyはデフォルト値が設定されていません。使用する場合は明示的に設定する必要があります。

---

## 🔧 ショートカットのカスタマイズ

### 設定方法

#### 1. コマンドラインから設定

```bash
# Tangentモードのキーを変更
q settings chat.tangentModeKey x

# Skimモードのキーを変更
q settings chat.skimCommandKey s

# Delegateモードのキーを変更
q settings chat.delegateModeKey e

# オートコンプリートのキーを変更
q settings chat.autocompletionKey Tab
```

#### 2. 設定ファイルで設定

`~/.amazonq/settings.json` を編集：

```json
{
  "chat.tangentModeKey": "x",
  "chat.skimCommandKey": "s",
  "chat.delegateModeKey": "e",
  "chat.autocompletionKey": "→"
}
```

### 設定可能なキーバインド

| 設定キー | 型 | デフォルト値 | 説明 |
|---------|-----|------------|------|
| `chat.tangentModeKey` | String (1文字) | `"t"` | Tangentモード切り替え |
| `chat.skimCommandKey` | String (1文字) | `"s"` | ファジー検索 |
| `chat.autocompletionKey` | String (1文字) | `"g"` | オートコンプリート受け入れ |
| `chat.delegateModeKey` | String (1文字) | なし | Delegateモード（要設定） |

> **⚠️ 注意**: キーバインドは1文字のみ指定可能です。Ctrlキーとの組み合わせで使用されます。

---

## 💡 実用例

### 例1: AWS開発での活用

```bash
# メインの会話: Lambda関数の開発
> Lambda関数でS3イベントを処理するコードを書いて

# Tangentモードで関連情報を調査
Ctrl+T
↯ > S3イベント通知の設定方法は？
↯ > Lambda実行ロールに必要な権限は？

# メインの会話に戻る
Ctrl+T
>

# コマンド選択メニューから必要なコマンドを実行
Ctrl+S
# → /context show を選択してコンテキストを確認
```

### 例2: トラブルシューティング

```bash
# メインの会話: エラーの調査
> このエラーの原因を調べて

# Tangentモードで複数の可能性を探索
Ctrl+T
↯ > ネットワーク設定の問題かも？
↯ > IAM権限の問題かも？
↯ > タイムアウト設定の問題かも？

# 最も有望な解決策をメインの会話で実行
Ctrl+T
>
```

### 例3: 学習と実験

```bash
# メインの会話: 新しい技術の学習
> AWS CDKの基本を教えて

# Tangentモードで関連技術を調査
Ctrl+T
↯ > CloudFormationとの違いは？
↯ > Terraformとの比較は？

# メインの会話に戻って実践
Ctrl+T
> CDKでS3バケットを作成するコードを書いて
```

---

## 🎓 ベストプラクティス

### 1. Tangentモードの効果的な使用

- **メインの会話を保護**: 重要な会話の途中で、関連情報を調査する際に使用
- **実験的な質問**: 確信が持てない質問や、試してみたいアイデアに使用
- **複数の解決策の比較**: 異なるアプローチを試す際に使用

### 2. コマンド選択メニューの活用

- **コマンド名を忘れた時**: メニューから選択して実行
- **利用可能なコマンドの確認**: 全コマンドを一覧表示
- **効率的な操作**: 矢印キーとEnterで素早く実行

### 3. ショートカットの習慣化

- **頻繁に使う機能**: デフォルトのキーバインドを覚える
- **個人の好み**: 使いやすいキーにカスタマイズ
- **一貫性**: 他のツールと統一したキーバインドを使用

---

## ❓ よくある質問

### Q1: ショートカットが動作しない

**A**: 以下を確認してください：

1. 機能が有効化されているか確認
   ```bash
   q settings chat.enableTangentMode
   ```

2. キーバインドが正しく設定されているか確認
   ```bash
   q settings chat.tangentModeKey
   ```

3. 他のツールとのキーバインド競合を確認

### Q2: カスタムキーバインドが保存されない

**A**: 設定ファイルの権限を確認してください：

```bash
# 設定ファイルの確認
ls -la ~/.amazonq/settings.json

# 権限の修正（必要な場合）
chmod 644 ~/.amazonq/settings.json
```

### Q3: Ctrl+Dが終了とDelegateモードの両方に割り当てられている

**A**: Ctrl+Dはコンテキストに応じて動作が変わります：
- **入力中（Delegateモード有効時）**: Delegateモードに入る
- **空の入力**: チャットを終了

Delegateモードを使用するには：
1. 実験的機能を有効化: `/experiment`
2. キーバインドを設定: `q settings chat.delegateModeKey d`

別のキーに変更したい場合：
```bash
q settings chat.delegateModeKey e
```

---

## 📚 関連ドキュメント

- [最初の一歩](../01_getting-started/03_first-steps.md) - 基本的な操作方法
- [グローバル設定](../03_configuration/03_global-settings.md) - キーバインド設定の詳細
- [推奨設定](../04_best-practices/01_configuration.md) - Tangentモードの設定
- [設定項目リファレンス](../07_reference/03_settings-reference.md) - 全設定項目の一覧

---

**作成日**: 2025-10-11
