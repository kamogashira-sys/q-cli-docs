## 8. 参考情報

この章では、コンテキスト管理に関するリファレンス情報を提供します。

---

### 8.1 コマンドリファレンス

#### 8.1.1 `/context show`

**構文**:
```
/context show
```

**説明**: 現在のコンテキスト情報を表示

**出力**:
```
Context Information:
Total tokens: 30000/80000 (37.5%)

Files (15):
1. README.md - 5000 tokens
2. .amazonq/rules/coding.md - 3000 tokens
...
```

**使用例**:
```bash
# コンテキストを確認
/context show

# 出力例:
# 👤 Agent (default):
#     README.md (1 match)
# 
# 💬 Session (temporary):
#     /home/user/.amazonq/rules/default.md (1 match)
# 
# 2 matched files in use:
# 💬 /home/user/.amazonq/rules/default.md (~400 tkns)
# 👤 /home/user/projects/myapp/README.md (~2620 tkns)
# 
# Total: ~3020 tokens

# 確認ポイント:
# - ファイル数: "2 matched files in use"
# - 各ファイルのトークン数: "~XXX tkns"
# - 合計トークン数: "Total: ~XXXX tokens"
```

**関連コマンド**:
- `/context add` - コンテキストを追加
- `/context rm` - コンテキストを削除

---

#### 8.1.2 `/context add`

**構文**:
```
/context add <file_path>
```

**説明**: Session Contextにファイルを追加

**パラメータ**:
- `file_path`: 追加するファイルのパス（`file://`プレフィックス必須）

**使用例**:
```bash
# ファイルを追加
/context add file://logs/error.log

# 確認
/context show
# Files (16):
# ...
# 16. logs/error.log - 2000 tokens
```

⚠️ **注意点**:
- Session Contextは一時的（セッション終了で削除）
- トークン制限に注意
- 不要になったら削除

**関連コマンド**:
- `/context show` - コンテキストを確認
- `/context rm` - コンテキストを削除

---

#### 8.1.3 `/context rm`

**構文**:
```
/context rm <file_path>
```

**説明**: Session Contextからファイルを削除

**パラメータ**:
- `file_path`: 削除するファイルのパス

**使用例**:
```bash
# ファイルを削除
/context rm file://logs/error.log

# 確認
/context show
# Files (15):
# （logs/error.logが削除された）
```

⚠️ **注意点**:
- Agent Resourcesは削除できない
- Session Contextのみ削除可能

**関連コマンド**:
- `/context show` - コンテキストを確認
- `/context add` - コンテキストを追加

---

#### 8.1.4 `/context clear`

**構文**:
```
/context clear
```

**説明**: すべてのSession Contextを削除

**使用例**:
```bash
# すべてのSession Contextを削除
/context clear

# 確認
/context show
# Files (10):
# （Agent Resourcesのみ残る）
```

⚠️ **注意点**:
- Agent Resourcesは削除されない
- Session Contextのみ削除

**関連コマンド**:
- `/context show` - コンテキストを確認

---

#### 8.1.5 `/knowledge add`

**構文**:
```
/knowledge add <directory_path>
```

**説明**: Knowledge Baseにディレクトリを追加

**パラメータ**:
- `directory_path`: 追加するディレクトリのパス

**使用例**:
```bash
# ディレクトリを追加
/knowledge add docs/

# 確認
/knowledge list
# Knowledge Bases:
# 1. docs/ - 250 files
```

⚠️ **注意点**:
- 初回セットアップに時間がかかる
- 大量のファイルを扱える
- 検索時のみトークン消費

**関連コマンド**:
- `/knowledge search` - Knowledge Baseを検索
- `/knowledge list` - Knowledge Baseを一覧表示

---

#### 8.1.6 `/knowledge search`

**構文**:
```
/knowledge search <query>
```

**説明**: Knowledge Baseを検索

**パラメータ**:
- `query`: 検索クエリ

**使用例**:
```bash
# 検索
/knowledge search "Lambda関数のベストプラクティス"

# 結果:
# 1. docs/aws/lambda-best-practices.md
# 2. docs/aws/lambda-error-handling.md
# ...
```

⚠️ **注意点**:
- セマンティック検索（意味で検索）
- 検索時にトークンを消費
- 検索結果は自動的にコンテキストに追加

**関連コマンド**:
- `/knowledge add` - Knowledge Baseを追加
- `/knowledge list` - Knowledge Baseを一覧表示

---

### 8.2 設定リファレンス

#### 8.2.1 `resources`フィールドの完全な仕様

#### JSON Schema

```json
{
  "resources": {
    "type": "array",
    "items": {
      "type": "string",
      "pattern": "^file://"
    },
    "description": "List of context files to load"
  }
}
```

#### 必須/任意

- **必須**: Yes
- **型**: array of string
- **デフォルト値**: `[]`

#### 制約

- すべてのパスは`file://`で始まる必要がある
- 相対パスまたは絶対パスを使用可能
- Globパターンをサポート

#### 例

**最小限の例**:
```json
{
  "resources": []
}
```

**基本的な例**:
```json
{
  "resources": [
    "file://README.md"
  ]
}
```

**完全な例**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/architecture.md",
    "file://docs/api-spec.md"
  ]
}
```

---

#### 8.2.2 `tools.fs_read.deniedPaths`フィールドの仕様

#### JSON Schema

```json
{
  "tools": {
    "type": "object",
    "properties": {
      "fs_read": {
        "type": "object",
        "properties": {
          "deniedPaths": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "List of paths to deny reading"
          }
        }
      }
    }
  }
}
```

#### 必須/任意

- **必須**: No
- **型**: array of string
- **デフォルト値**: `[]`

#### 制約

- Globパターンをサポート
- 相対パスまたは絶対パスを使用可能

#### 例

**基本的な例**:
```json
{
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*"
      ]
    }
  }
}
```

**完全な例**:
```json
{
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*",
        "**/*.key",
        "**/*.pem",
        "**/secrets/**",
        "config/production.yaml",
        "node_modules/**",
        ".git/**"
      ]
    }
  }
}
```

---

### 8.3 技術仕様

#### 8.3.1 トークン制限

**制限値**: 75%

**詳細**:
- 全トークン: 80000トークン
- コンテキスト: 60000トークン（75%）
- 会話と応答: 20000トークン（25%）

**超過時の動作**:
- 警告メッセージを表示
- ファイルを自動的にドロップ
- 最も古いファイルから削除

**確認方法**:
```bash
/context show
# Total tokens: 30000/80000 (37.5%)
```

---

#### 8.3.2 サポートされるファイル形式

**テキストファイル**:
- Markdown: `.md`, `.markdown`
- テキスト: `.txt`
- JSON: `.json`
- YAML: `.yaml`, `.yml`
- XML: `.xml`

**コードファイル**:
- Python: `.py`
- JavaScript: `.js`
- TypeScript: `.ts`
- Java: `.java`
- Go: `.go`
- Rust: `.rs`
- C/C++: `.c`, `.cpp`, `.h`, `.hpp`
- その他: 多数のプログラミング言語をサポート

**設定ファイル**:
- `.env`
- `.config`
- `.ini`
- `.toml`

**非サポート形式**:
- バイナリファイル: `.pdf`, `.docx`, `.xlsx`
- 画像ファイル: `.png`, `.jpg`, `.gif`
- 圧縮ファイル: `.zip`, `.tar.gz`
- 実行ファイル: `.exe`, `.bin`

---

#### 8.3.3 パス指定の形式

**相対パス**:
```json
{
  "resources": [
    "file://README.md",
    "file://docs/architecture.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**絶対パス**:
```json
{
  "resources": [
    "file:///home/user/projects/my-project/README.md"
  ]
}
```

**ホームディレクトリ**:
```json
{
  "resources": [
    "file://~/projects/my-project/README.md"
  ]
}
```

**推奨**: 相対パスを使用（ポータビリティのため）

---

#### 8.3.4 Globパターンの仕様

**サポートされるパターン**:
- `*`: 単一ディレクトリ内のファイル
- `**`: すべての子孫ディレクトリ
- `?`: 単一文字
- `[abc]`: 文字セット
- `{a,b}`: 選択肢

**例**:
```json
{
  "resources": [
    "file://.amazonq/rules/*.md",        // 直下の.mdファイル
    "file://.amazonq/rules/**/*.md",     // すべての子孫の.mdファイル
    "file://docs/**/*.{md,txt}",         // 複数拡張子
    "file://src/**/test_*.py"            // パターンマッチ
  ]
}
```

**動作**:
- gitignoreと同じ
- 大文字小文字を区別
- シンボリックリンクをフォロー

---

### 8.4 用語集

### Agent Resources
Agent設定の`resources`フィールドで指定されたコンテキストファイル。Agent起動時に自動的に読み込まれ、セッション全体で永続的に利用可能。

### Session Context
`/context add`コマンドで一時的に追加されたコンテキストファイル。セッション終了時に自動的に削除される。

### Knowledge Bases
大量のドキュメントを検索可能な形式で保存する機能。検索時のみトークンを消費し、セマンティック検索をサポート。

### コンテキストウィンドウ
AIが一度に処理できる情報の量。Q CLIでは80000トークンで、コンテキストは75%（60000トークン）まで使用可能。

### トークン
AIが理解できる最小単位。英語では約4文字、日本語では約2-3文字が1トークンに相当。

### Globパターン
ファイルパスのパターンマッチングに使用される記法。`*`や`**`などのワイルドカードを使用してファイルを指定。

---

### 8.5 FAQ

### Q1: コンテキストとは何ですか？

**A**: コンテキストとは、AIとの対話における「文脈」のことです。プロジェクトの概要、ルール、仕様などの情報をAIに提供することで、より正確で関連性の高い応答を得られます。

**詳細**: [第1章: コンテキストの本質](#第1章-コンテキストの本質)

---

### Q2: どのアプローチを選べばいいですか？

**A**: 以下の基準で選択してください：

1. **サイズと量**: 10MB以上、数千ファイル → Knowledge Bases
2. **使用頻度**: すべての会話で必要 → Agent Resources
3. **使用頻度**: 特定の会話でのみ必要 → Session Context

**詳細**: [第4章: アプローチ選択の思考プロセス](#42-アプローチ選択の思考プロセス)

---

### Q3: トークン制限を超えたらどうすればいいですか？

**A**: 以下の対策を実施してください：

1. 不要なファイルを削除
2. 大きなファイルを分割
3. Knowledge Basesへ移行
4. Session Contextに変更

**詳細**: [第6章: トラブルシューティング](#62-よくある問題と解決方法)

---

### Q4: 機密情報を含むファイルはどうすればいいですか？

**A**: `tools.fs_read.deniedPaths`で除外してください：

```json
{
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*",
        "**/*.key",
        "**/*.pem",
        "**/secrets/**"
      ]
    }
  }
}
```

**詳細**: [第4章: セキュリティ設計の思考プロセス](#46-セキュリティ設計の思考プロセス)

---

### Q5: チームで設定を共有するにはどうすればいいですか？

**A**: 以下の手順で共有してください：

1. Agent設定をバージョン管理に含める
2. 個人設定を`.gitignore`で除外
3. 機密情報を除外
4. README.mdにドキュメント化

**詳細**: [第7章: チーム開発での活用](#72-チーム開発での活用)

---

### Q6: ファイルが読み込まれないのはなぜですか？

**A**: 以下を確認してください：

1. `file://`プレフィックスがあるか
2. パスが正しいか
3. ファイルが存在するか
4. ファイルの権限が正しいか

**詳細**: [第6章: 問題1: ファイルが読み込まれない](#621-問題1-ファイルが読み込まれない)

---

### Q7: パフォーマンスが悪いのはなぜですか？

**A**: 以下を確認してください：

1. ファイル数が多すぎないか（25以上）
2. 1ファイルが大きすぎないか（10KB以上）
3. 合計サイズが大きすぎないか（100KB以上）

**対策**: ファイル数・サイズを削減、Knowledge Basesへ移行

**詳細**: [第6章: 問題4: パフォーマンス問題](#624-問題4-パフォーマンス問題)

---

### Q8: ワイルドカードがマッチしないのはなぜですか？

**A**: 以下を確認してください：

1. パターンが正しいか（`*`vs`**`）
2. ファイルが存在するか
3. ファイル拡張子が正しいか

**確認方法**:
```bash
find .amazonq/rules/ -name "*.md"
```

**詳細**: [第6章: 問題3: ワイルドカードがマッチしない](#623-問題3-ワイルドカードがマッチしない)

---

### Q9: Knowledge Basesはいつ使うべきですか？

**A**: 以下の場合に使用してください：

1. ファイル数が100以上
2. 合計サイズが10MB以上
3. 検索可能な情報
4. 参照頻度が低い

**メリット**: 検索時のみトークン消費、大量のドキュメントを扱える

**詳細**: [第3章: Knowledge Basesの特徴](#34-knowledge-basesの特徴)

---

### Q10: 最初に何をすればいいですか？

**A**: 以下の手順で始めてください：

1. 最小限の設定から始める（README.mdのみ）
2. `/context show`で確認
3. 必要に応じてファイルを追加
4. トークン使用量を監視

**推奨設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**詳細**: [第5章: 基本設定の実装](#51-基本設定の実装)

---

## まとめ

### 重要なポイント

1. **コマンドリファレンス**
   - `/context show`: 最も重要なコマンド
   - `/context add/rm`: Session Contextの管理
   - `/knowledge add/search`: Knowledge Basesの活用

2. **設定リファレンス**
   - `resources`: コンテキストファイルのリスト
   - `tools.fs_read.deniedPaths`: 除外パスのリスト

3. **技術仕様**
   - トークン制限: 75%（60000トークン）
   - サポート形式: テキスト、コード、設定ファイル
   - Globパターン: gitignoreと同じ

4. **FAQ**
   - 10の頻出質問と回答
   - 詳細な説明へのリンク

### 次のステップ

このドキュメントを活用して、効果的なコンテキスト管理を実践してください。

---

**出典**:
- [コマンドリファレンス](../07_reference/02_commands.md)
- [用語集](../07_reference/01_glossary.md)
- [JSON Schema](/crates/chat-cli/src/cli/agent/schema.json)
