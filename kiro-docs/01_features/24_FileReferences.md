[ホーム](../README.md) > [機能詳細ガイド](README.md) > File References（@file/@directory）

# Kiro CLI File References（@file/@directory）機能

**出典**: [File References - Kiro CLI Documentation](https://kiro.dev/docs/cli/chat/file-references/)、[Manage Prompts](https://kiro.dev/docs/cli/chat/manage-prompts/)、[Context Management](https://kiro.dev/docs/cli/chat/context/)、[公式Changelog v1.26.0](https://kiro.dev/changelog/cli/1-26/)

## 概要

### File Referencesとは

File References は、`@path` 構文でチャットメッセージ内に **ファイル内容またはディレクトリツリーを直接埋め込む** 機能です。手動でコピーする必要がなくなり、コンテンツが送信前にインライン展開されるため **ツール呼び出しを回避してトークンを節約** できます。

Kiro CLI v1.26.0（2026年2月12日リリース）で追加されました（本サイト [Changelog v1.26.0](../02_update/01_changelog.md) 参照）。

### 主な特徴

1. **`@path` 構文** — ファイル内容またはディレクトリツリーをインライン展開
2. **Tab 補完** — 入力中の任意の位置で Tab キーで補完
3. **トークン節約** — ツール呼び出し（`fs_read`, `glob` 等）を回避
4. **解決順序** — Known prompts → Files → Directories の3段階
5. **明示的な解決指定** — `@./myfile` でプロンプト衝突を回避

### なぜ File References が必要なのか

従来のアプローチには以下の課題がありました：

- ファイル内容を `cat` でコピペする手間
- `fs_read` ツール呼び出しのトークンコストとレスポンス遅延
- 複数ファイルを横断する文脈構築の煩雑さ
- ディレクトリ構造を伝える際の視覚化

File References はこれらを **「@」1文字とパス指定** で解決します。

**公式ドキュメント原文**:

> File references let you include file contents or directory trees directly in your chat messages using `@path` syntax. This provides quick context without manually copying content, and since the content is expanded inline before sending, it avoids tool calls—saving tokens.

---

## 📋 目次

- [基本的な使い方](#基本的な使い方)
- [Tab 補完](#tab-補完)
- [解決順序（Prompts → Files → Directories）](#解決順序prompts--files--directories)
- [ファイル取り扱い](#ファイル取り扱い)
- [ディレクトリツリー](#ディレクトリツリー)
- [使用例](#使用例)
- [現状の制約](#現状の制約)
- [トラブルシューティング](#トラブルシューティング)
- [v1.26.0 リリース時の位置づけ](#v1260-リリース時の位置づけ)
- [4つのコンテキスト管理アプローチとの関係](#4つのコンテキスト管理アプローチとの関係)
- [関連リンク](#関連リンク)

---

## 基本的な使い方

**出典**: [File References - Basic usage](https://kiro.dev/docs/cli/chat/file-references/#basic-usage)

`@` の後にファイルパスまたはディレクトリパスを記述します。

```
@src/index.ts             # ファイル内容を含める
@src/                     # ディレクトリツリーを含める
@./relative/path          # 相対パス
@"path with spaces.txt"   # スペースを含むパス（クォート必須）
```

メッセージ内のどこでも参照を使用できます：

```
Review @src/auth.ts for security issues
Compare @old.json with @new.json
What's in @src/ that handles authentication?
```

### 構文の特徴

| 形式 | 動作 |
|------|------|
| `@<file-path>` | ファイル内容を展開 |
| `@<directory-path>/` | ディレクトリツリー（最大3階層）を展開 |
| `@./<path>` | 明示的な相対パス（プロンプト名との衝突回避） |
| `@"<path with spaces>"` | スペースを含むパス（ダブルクォート必須） |

---

## Tab 補完

**出典**: [File References - Tab completion](https://kiro.dev/docs/cli/chat/file-references/#tab-completion)

`@` の後に Tab キーを押すと、パスが自動補完されます。

```
@src/<Tab>                # src/ 配下のファイル一覧を表示
@package<Tab>             # @package.json に補完
@"Screenshot 2024<Tab>     # @"Screenshot 2024-01.png" に補完
```

### Tab 補完の特徴

- 入力行の **どこでも動作**（行の先頭である必要はない）
- スペースを含むパスは **自動的にクォート付与**
- 隠しファイル・除外ディレクトリ（`node_modules`、`.git` 等）は補完候補から除外

---

## 解決順序（Prompts → Files → Directories）

**出典**: [File References - How references are resolved](https://kiro.dev/docs/cli/chat/file-references/#how-references-are-resolved)、[Manage Prompts](https://kiro.dev/docs/cli/chat/manage-prompts/)

`@name` の参照がプロンプトとファイルの両方にマッチする可能性がある場合、Kiro は **以下の順序で解決** します：

### 1. **Prompts**（最優先）

`@name` が `/prompts list` のプロンプトと一致する場合、**プロンプトとして扱われます**。

#### Prompts の優先順位

```
Local prompts > Global prompts > MCP prompts
```

| 種類 | 配置 | スコープ |
|------|------|---------|
| Local | `<workspace>/.kiro/prompts/` | プロジェクト固有 |
| Global | `~/.kiro/prompts/` | ユーザー全体 |
| MCP | MCP サーバー提供 | サーバー次第 |

### 2. **Files**

プロンプトと一致しない場合、**ファイルパスとして解決** されます。

### 3. **Directories**

ファイルでもない場合、**ディレクトリツリーとして展開** されます。

### プロンプトとの衝突回避

プロンプトと同名のファイルを参照したい場合は、**明示的な相対パス** を使用します：

```
@myfile           # プロンプト "myfile" として解決される（プロンプトが存在する場合）
@./myfile         # ファイル "myfile" として確実に解決される
```

> **💡ワンポイント**: v1.26.0 以降、`@path` 参照と Prompts は同じ `@` 構文を共有します。混乱を避けるため、ファイル参照には `@./` プレフィックスを習慣化することが推奨されます。

### MCP プロンプトの引数

MCP 由来のプロンプトは引数を受け付けます（File-based prompt は引数非対応）：

```
@server-name/prompt-name <required-arg> [optional-arg]
```

---

## ファイル取り扱い

**出典**: [File References - File handling](https://kiro.dev/docs/cli/chat/file-references/#file-handling)

### サポート対象

- **テキストファイル**（ソースコード、設定ファイル、Markdown 等）
- **最大サイズ**: **250KB** まで

### 非サポート

- **バイナリファイル**（画像、実行可能ファイル、アーカイブ等）はエラーを表示
- 250KB を超えるファイルは **切り捨て** され、警告が表示される：

```
⚠ File 'large-file.json' was truncated (exceeds 250KB limit)
```

### 大きなファイルへの対応

| アプローチ | 用途 | 関連機能 |
|----------|------|---------|
| `@file` 切り捨て確認 | 単発的に部分参照 | 本機能 |
| `glob` / `grep` ツール | 必要箇所だけ抽出 | [05. GrepGlob](05_GrepGlob.md) |
| AST パターンツール | 構造的に抽出 | [09. AST Pattern Tools](09_ASTPatternTools.md) |
| Knowledge Bases | 大規模ドキュメント検索 | [Skills](07_Skills.md) と関連 |

---

## ディレクトリツリー

**出典**: [File References - Directory trees](https://kiro.dev/docs/cli/chat/file-references/#directory-trees)

ディレクトリ参照は **ツリー一覧** として展開されます。

```
@src/
```

展開結果：

```
src/
├── lib/
│   ├── auth.ts
│   └── utils.ts
├── index.ts
└── config.json
```

### ディレクトリツリーの制約

| 項目 | 値 |
|------|-----|
| **最大深さ** | 3階層 |
| **階層あたり最大要素** | 10件（超過時は `... (N more items)` と表示） |
| **デフォルト除外** | `node_modules`、`.git`、`target`、`dist`、`build` |

### より深い階層を見たい場合

特定のサブディレクトリを直接参照します：

```
@src/                       # 最大3階層
@src/deep/path/             # ここから3階層分を展開
@src/deep/path/leaf/        # さらに深い階層
```

---

## 使用例

**出典**: [File References - Examples](https://kiro.dev/docs/cli/chat/file-references/#examples)

### 1. ファイルレビュー

```
> Review @src/auth.ts for security issues
```

→ `auth.ts` の内容がインライン展開され、Kiro がセキュリティ観点でレビュー。

### 2. ファイル比較

```
> What's different between @v1/handler.py and @v2/handler.py?
```

→ 2つのファイルが両方とも展開され、差分分析が可能。

### 3. 構造把握

```
> What's the structure of @infra/cdk/?
```

→ `infra/cdk/` のディレクトリツリーが展開され、Kiro が構成を把握。

### 4. 複合的な文脈

```
> Using the config in @serverless.yml, update @src/lambda/index.ts
```

→ 設定ファイル（serverless.yml）と実装ファイル（lambda/index.ts）の両方を文脈に含めて、Kiro が一貫した修正を提案。

### 5. README とコードの併用

```
> Based on @README.md, refactor @src/main.rs to match the documented API
```

→ ドキュメントとコードを同時に文脈化し、整合性のあるリファクタリングを実現。

---

## 現状の制約

**出典**: [File References - Current limitations](https://kiro.dev/docs/cli/chat/file-references/#current-limitations)

### サポート範囲

| 項目 | サポート | 制約 |
|------|--------|------|
| テキストファイル | ✅ | 最大 250KB |
| ディレクトリツリー | ✅ | 最大3階層、各階層10件 |
| 明示的なファイルパス | ✅ | グロブパターン非対応（`@*.ts` 不可） |
| 完全なファイル内容 | ✅ | 行範囲指定不可（`@file.ts:10-20` 不可） |
| 相対パスと絶対パス | ✅ | チルダ展開非対応（`@~/file` 不可） |
| バイナリファイル | ❌ | 画像、実行ファイル、アーカイブはサポート外 |

### グロブパターンが必要な場合

`@*.ts` のような複数ファイル参照には対応していないため、複数ファイルを参照したい場合は：

1. **個別に列挙**: `@src/a.ts @src/b.ts @src/c.ts`
2. **glob ツール経由**: チャットで「`src/*.ts` のすべてを確認して」と依頼（`glob` ツールが呼ばれる）
3. **ディレクトリ参照**: `@src/`（ツリー表示のみ、内容は表示されない）

---

## トラブルシューティング

**出典**: [File References - Troubleshooting](https://kiro.dev/docs/cli/chat/file-references/#troubleshooting)

| 問題 | 解決策 |
|------|------|
| 参照がプロンプトとして扱われる | 同名のプロンプトが存在する場合。明示的なパス `@./myfile` を使用 |
| ファイルが見つからない | パスが現在のディレクトリ基準であることを確認、または絶対パスを使用 |
| ディレクトリが深すぎる | 3階層を超えるサブディレクトリは表示されない。特定のサブディレクトリを参照: `@src/deep/path/` |
| スペースを含むパスが認識されない | クォート構文を使用: `@"path with spaces.txt"` |
| バイナリファイルでエラー | バイナリは未対応。テキストに変換するか、別ツールで参照 |
| 250KB 超過の警告 | 大きなファイルは切り捨てられる。必要部分だけ抽出するか、`grep`/`glob` ツール経由で参照 |

---

## v1.26.0 リリース時の位置づけ

**出典**: [Changelog v1.26.0](../02_update/01_changelog.md)

Kiro CLI v1.26.0（2026年2月12日）で追加された主要機能の一つ。同バージョンの他の主要追加機能との関係：

| 機能 | 関係 |
|------|------|
| **@file/@directory展開** | 本機能（File References） |
| **Skills 自動読み込み** | `.kiro/skills/` の Skill が default agent に自動提供される。`@file` との使い分けは「Skills」が大規模ガイド向け、「@file」が即興的なファイル参照向け |
| **Manage Prompts (`/prompts`)** | プロンプトと File References が同じ `@` 構文を共有。解決順序が重要（[解決順序](#解決順序prompts--files--directories) 参照） |
| **`@` 構文ベースのコンテキスト統合** | プロンプト・ファイル・ディレクトリを `@` で統一的に参照可能に |

---

## 4つのコンテキスト管理アプローチとの関係

**出典**: [Context Management](https://kiro.dev/docs/cli/chat/context/)

Kiro が提供する4つのコンテキスト管理アプローチの中で、File References の位置づけ：

| アプローチ | コンテキストへの影響 | 永続性 | 最適なユースケース |
|----------|-----------------|------|---------------|
| **Agent Resources** | 常時アクティブ（トークン消費） | セッション跨ぎ | 必須プロジェクトファイル、標準、設定 |
| **Skills** | オンデマンド | セッション跨ぎ | 大規模ガイド、リファレンス |
| **Session Context** | 常時アクティブ（トークン消費） | 当該セッションのみ | 一時ファイル、実験 |
| **Knowledge Bases** | 検索時のみ | セッション跨ぎ | 大規模コードベース、ドキュメントセット |
| **File References (`@file`)** | **送信時に1回展開**（ツール呼び出し回避） | 当該メッセージのみ | **即興的なファイル指定**（本機能） |

### 決定フローチャート（公式準拠）

1. **10MB超 or 数千ファイル** → **Knowledge Bases**
2. **毎セッション必要** → **Agent Resources**
3. **その時だけ即座に参照** → **File References（`@file`）** ← 本機能
4. **セッション中継続的に必要** → **Session Context**

> **コンテキストウィンドウ上限**: モデルのコンテキストウィンドウの **75%**（超過時は自動的に削除）。File References を多用する場合、合計サイズに注意してください。

---

## 関連リンク

### 関連機能（本サイト）

- [05. GrepGlob](05_GrepGlob.md) — `@directory/` でツリー表示できないコードを検索する場合
- [07. Skills](07_Skills.md) — オンデマンドな大規模ガイド（File References との使い分け）
- [09. AST Pattern Tools](09_ASTPatternTools.md) — 構造的なコード抽出（行範囲非対応の代替）
- [10. Conversation Compaction](10_ConversationCompaction.md) — File References を含む文脈の圧縮
- [23. Steering](23_Steering.md) — プロジェクト永続知識（@file との使い分け）

### リファレンス（辞書）

- [04_reference/04_built-in-tools.md](../04_reference/04_built-in-tools.md) — `read` / `glob` / `grep` 各ツールと `@file` `@directory` の使い分け

### バージョン関連

- [Changelog v1.26.0](../02_update/01_changelog.md) — `@file/@directory展開` 初出バージョン

### 公式情報源

- [File References - Kiro CLI Documentation](https://kiro.dev/docs/cli/chat/file-references/)（公式ページ最終更新: 2026-02-16）
- [Manage Prompts](https://kiro.dev/docs/cli/chat/manage-prompts/) — `@name` の Prompts 解決
- [Context Management](https://kiro.dev/docs/cli/chat/context/) — 4つのコンテキスト管理アプローチ

---

**Page updated**: 2026-05-24（本サイト初版）  
**公式ページ最終更新**: 2026-02-16
