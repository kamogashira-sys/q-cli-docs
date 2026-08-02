[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [コンテキスト管理ガイド](README.md) > 02 Mechanism

---

# 2. コンテキストの仕組みと管理

---

### 2.1 コンテキストのライフサイクル

コンテキストは、Agent起動からセッション終了まで、明確なライフサイクルを持っています。

#### 読み込み（Agent起動時）

**実装コードの動作**:

Agent起動時、以下の順序でコンテキストが読み込まれます：

```
1. Agent設定ファイルの読み込み
   ↓
2. resourcesフィールドの解析
   ↓
3. 各ファイルパスの解決
   - 相対パス → 絶対パスに変換（cwd基準）
   - Globパターン → ファイルリストに展開
   - file://プレフィックスの検証
   ↓
4. ファイルの読み込み
   - 各ファイルを順次読み込み
   - UTF-8エンコーディングで解析
   - トークン化
   ↓
5. コンテキストウィンドウへの配置
   - トークン数の計算
   - 75%制限のチェック
   - 超過ファイルの自動ドロップ
```

**読み込み順序**:

```json
{
  "resources": [
    "file://README.md",           // 1番目
    "file://.amazonq/rules/**/*.md", // 2番目（展開後、アルファベット順）
    "file://docs/guide.md"        // 3番目
  ]
}
```

💡 **初心者向けポイント**: ファイルは設定に記載した順序で読み込まれますが、Globパターンは展開後にアルファベット順になります。

⚠️ **注意**: 読み込み順序に依存した設定は避けましょう。順序が変わる可能性があります。

#### 保持（セッション中）

**メモリ管理**:

読み込まれたコンテキストは、セッション中メモリに保持されます：

- Agent Resourcesは常に保持
- Session Contextは追加・削除可能
- トークン使用量は常時監視

**トークン消費**:

```
┌─────────────────────────────────────┐
│  コンテキストウィンドウ（100%）     │
├─────────────────────────────────────┤
│  Agent Resources: 1,100 tokens      │ ← 常時消費
│  Session Context: 500 tokens        │ ← 常時消費
│  会話履歴: 300 tokens               │
│  応答生成: 残り                     │
└─────────────────────────────────────┘
```

💡 **初心者向けポイント**: コンテキストファイルは、使用していなくてもトークンを消費し続けます。

#### 更新（動的追加・削除）

**`/context`コマンド**:

セッション中にコンテキストを動的に変更できます：

```bash
# ファイル追加
> /context add docs/api-spec.md
Added 1 path(s) to context.

# ファイル削除
> /context rm docs/api-spec.md
Removed 1 path(s) from context.

# すべてクリア
> /context clear
Cleared context
```

**即時反映**:

変更は即座に反映されます：

```
追加前: 1,100 tokens
  ↓ /context add (500 tokens)
追加後: 1,600 tokens （即座に反映）
```

📝 **実例**:
```bash
> /context show
Total: ~1100 tokens

> /context add docs/large-file.md
Added 1 path(s) to context.

> /context show
Total: ~1600 tokens  # 即座に増加
```

⚠️ **注意**: Agent Resourcesは`/context`コマンドで削除できません。Agent設定を編集する必要があります。

#### 破棄（セッション終了時）

**クリーンアップ**:

セッション終了時、以下の処理が実行されます：

```
1. Session Contextの破棄
   - /context addで追加したファイル
   - 一時的なコンテキスト
   ↓
2. Agent Resourcesの保持
   - 次回起動時に再利用
   - 設定ファイルに記録
   ↓
3. Knowledge Basesの保持
   - インデックスデータは保持
   - 次回起動時に利用可能
```

💡 **初心者向けポイント**: Session Contextは「使い捨て」、Agent Resourcesは「再利用可能」と覚えましょう。

---

### 2.2 トークン管理の詳細

#### トークンとは何か

**定義**:

トークンは、AIがテキストを処理する最小単位です。単語や文字の一部として扱われます。

**トークン化の例**:

```
英語:
"Hello, World!" 
→ ["Hello", ",", " World", "!"] 
→ 約3トークン

日本語:
"こんにちは、世界！"
→ ["こん", "にち", "は", "、", "世界", "！"]
→ 約5-7トークン
```

💡 **初心者向けポイント**: 日本語は英語よりもトークン数が多くなる傾向があります。

#### トークンの計算方法

**目安**:

| 言語 | 1トークンあたりの文字数 |
|------|----------------------|
| 英語 | 約4文字 |
| 日本語 | 約2-3文字 |
| コード | 約3-4文字 |

**ファイルサイズからの推定**:

```
英語テキスト:
5KB ≈ 5,000文字 ≈ 1,250トークン

日本語テキスト:
5KB ≈ 2,500文字 ≈ 830-1,250トークン

コード:
5KB ≈ 5,000文字 ≈ 1,250-1,660トークン
```

📝 **実例**:
```
README.md (5KB, 英語中心)
→ 約1,250トークン

.amazonq/rules/security.md (2KB, 日本語中心)
→ 約500-660トークン
```

⚠️ **注意**: これは目安です。正確なトークン数は`/context show`で確認してください。

#### トークン制限（75%ルール）

**公式制限**:

コンテキストファイルは、コンテキストウィンドウの**最大75%**まで使用できます。

```
コンテキストウィンドウ: 100,000トークン（例）
  ├─ コンテキストファイル: 最大75,000トークン
  └─ 会話履歴・応答: 最低25,000トークン
```

**制限を超えた場合**:

```
設定: 5つのファイル（合計80,000トークン）
  ↓
読み込み時: 75%制限チェック
  ↓
結果: 一部のファイルが自動的にドロップ
  ↓
警告: "Some files were dropped due to token limit"
```

💡 **初心者向けポイント**: 75%制限は「安全マージン」です。会話履歴と応答のためのスペースを確保しています。

📝 **実例**:
```bash
> /context show
Total: ~78000 tokens  # 75%を超過

# 警告が表示される
Warning: Context usage exceeds 75% limit
Some files may be dropped
```

#### トークン使用量の監視

**`/context show`の使い方**:

```bash
> /context show
👤 Agent (my-agent):
    README.md (1 match)
    .amazonq/rules/**/*.md (3 matches)

💬 Session (temporary):
    docs/api-spec.md (1 match)

5 matched files in use:
👤 README.md (~250 tkns)
👤 .amazonq/rules/security.md (~180 tkns)
👤 .amazonq/rules/coding-standards.md (~320 tkns)
👤 .amazonq/rules/best-practices.md (~200 tkns)
💬 docs/api-spec.md (~150 tkns)

Total: ~1100 tokens
```

**出力の読み方**:

1. **👤 Agent**: Agent Resourcesから読み込まれたファイル
2. **💬 Session**: Session Contextで追加されたファイル
3. **~XXX tkns**: 各ファイルのトークン数（概算）
4. **Total**: 合計トークン数

💡 **初心者向けポイント**: 定期的に`/context show`でトークン使用量を確認しましょう。

⚠️ **監視のタイミング**:
- Agent設定変更後
- 大きなファイルを追加した後
- 応答が遅くなった時

---

### 2.3 コンテキストの優先順位

#### Agent Resources vs Session Context

両方に同じファイルがある場合、**Session Contextが優先**されます：

```
Agent設定:
{
  "resources": ["file://README.md"]  // バージョン1
}

セッション中:
> /context add README.md  // バージョン2（更新版）

結果: バージョン2が使用される
```

💡 **初心者向けポイント**: Session Contextで一時的に上書きできます。

#### 複数ファイルの読み込み順序

ファイルは以下の順序で読み込まれます：

1. Agent Resourcesの順序
2. Globパターンはアルファベット順
3. Session Contextは追加順

```json
{
  "resources": [
    "file://README.md",              // 1番目
    "file://.amazonq/rules/a.md",    // 2番目
    "file://.amazonq/rules/b.md",    // 3番目
    "file://docs/guide.md"           // 4番目
  ]
}
```

⚠️ **注意**: 読み込み順序に依存しないように設計しましょう。

#### コンテキストの上書きルール

同じ情報が複数のファイルにある場合：

- **後から読み込まれたファイルが優先**される傾向
- ただし、AIは両方の情報を考慮する
- 矛盾がある場合、AIが判断する

📝 **実例**:
```
README.md: "Pythonバージョン: 3.8"
docs/setup.md: "Pythonバージョン: 3.9"

AIの応答: "Python 3.9を使用してください（最新の情報に基づく）"
```

💡 **初心者向けポイント**: 矛盾する情報は避け、一箇所にまとめましょう。

---

### 2.4 Q CLIでの管理方法

#### Agent Resourcesの設定

**`resources`フィールドの仕様**:

JSON Schemaによる定義：

```json
"resources": {
  "description": "Files to include in the agent's context",
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^(file://)"
  },
  "default": []
}
```

**必須要件**:
- `file://`プレフィックスが必須
- 配列形式
- 文字列要素

**ファイルパスの指定方法**:

1. **相対パス**（推奨）:
```json
{
  "resources": [
    "file://README.md",
    "file://./docs/guide.md"
  ]
}
```

2. **絶対パス**:
```json
{
  "resources": [
    "file:///home/user/project/README.md"
  ]
}
```

3. **ホームディレクトリ**:
```json
{
  "resources": [
    "file://~/.aws/amazonq/common-rules.md"
  ]
}
```

💡 **初心者向けポイント**: 相対パスを使うと、チームで共有しやすくなります。

**Globパターンの使用**:

```json
{
  "resources": [
    "file://.amazonq/rules/*.md",      // 直下の.mdファイル
    "file://.amazonq/rules/**/*.md",   // すべての子孫の.mdファイル
    "file://docs/**/*.{md,txt}"        // 複数拡張子
  ]
}
```

**Globパターンの動作**（gitignore形式）:

- `*`: 単一ディレクトリレベル内でマッチ
- `**`: すべての子孫ディレクトリを再帰的にマッチ
- `?`: 1文字にマッチ
- `{a,b}`: aまたはbにマッチ

📝 **実例**:
```json
{
  "resources": [
    "file://.amazonq/rules/**/*.md"
  ]
}

マッチするファイル:
- .amazonq/rules/security.md
- .amazonq/rules/coding/standards.md
- .amazonq/rules/coding/best-practices.md
```

⚠️ **注意**: 広すぎるパターンは大量のファイルをマッチし、トークン制限を超える可能性があります。

#### Session Contextの操作

**`/context add`コマンド**:

```bash
# 単一ファイル追加
> /context add README.md
Added 1 path(s) to context.

# 複数ファイル追加（Globパターン）
> /context add docs/*.md
Added 3 path(s) to context.

# 絶対パス
> /context add /home/user/project/file.md
Added 1 path(s) to context.
```

💡 **初心者向けポイント**: Globパターンも使用できます。

**`/context rm`コマンド**:

```bash
# ファイル削除
> /context rm docs/api-spec.md
Removed 1 path(s) from context.

# 複数ファイル削除
> /context rm docs/*.md
Removed 3 path(s) from context.
```

**`/context clear`コマンド**:

```bash
# すべてのSession Contextをクリア
> /context clear
Cleared context
Note: Agent-defined context is not affected.
```

⚠️ **注意**: Agent Resourcesは削除されません。

**`/context show`コマンド**:

```bash
# 現在のコンテキストを表示
> /context show
👤 Agent (my-agent):
    README.md (1 match)
    .amazonq/rules/**/*.md (3 matches)

💬 Session (temporary):
    docs/api-spec.md (1 match)

Total: ~1100 tokens
```

💡 **初心者向けポイント**: 設定変更後は必ず`/context show`で確認しましょう。

#### Knowledge Basesの活用

**セットアップ**:

```bash
# Knowledge Basesを有効化
> q settings chat.enableKnowledge true
```

**コンテンツの追加**:

```bash
# ディレクトリ全体を追加
> /knowledge add /path/to/large-codebase

# 特定のファイルのみ追加
> /knowledge add /path/to/codebase --include "**/*.py"

# 除外パターン指定
> /knowledge add /path/to/codebase --include "**/*.py" --exclude "node_modules/**"
```

**検索と活用**:

```bash
# セマンティック検索
> /knowledge search "authentication patterns"

# 検索結果が自動的にコンテキストに追加される
```

💡 **初心者向けポイント**: Knowledge Basesは「必要な時だけ検索」するので、トークンを節約できます。

📝 **実例**:
```bash
# 大規模なコードベース（50MB）をインデックス化
> /knowledge add ./src --include "**/*.py"
Indexing 1,234 files...
Done. Knowledge base created.

# 必要な時だけ検索
> /knowledge search "user authentication"
Found 5 relevant files.
Added to context: auth.py, user_model.py
```

---

## 📖 ナビゲーション

← **前へ**: [第1章: コンテキストの本質](01_essence.md) | **次へ**: [第3章: コンテキストの効果と特徴](03_effects.md) →

---

最終更新: 2025-11-01

