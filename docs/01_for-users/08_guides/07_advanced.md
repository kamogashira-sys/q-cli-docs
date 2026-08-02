[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [コンテキスト管理ガイド](README.md) > 07 Advanced

---

# 7. 高度なトピック

---

この章では、上級者向けの高度な活用方法を提供します。

---

### 7.1 コンテキストの最適化戦略

#### 7.1.1 トークン効率の向上

#### 戦略1: ファイルの圧縮技術

**目的**: 同じ情報をより少ないトークンで表現

**手法1: 冗長な説明の削除**

📝 **最適化前**:
```markdown
# API設計規約

このドキュメントは、プロジェクト全体で一貫したAPI設計を維持するためのガイドラインです。
以下のルールに従ってAPIを設計してください。

## エンドポイント命名規則

エンドポイントの命名には以下のルールを適用します。
リソースは必ず複数形を使用してください。
例えば、ユーザーリソースの場合は`/users`とします。
```

📝 **最適化後**:
```markdown
# API設計規約

## エンドポイント命名
- リソース: 複数形（例: `/users`）
- ID: 単数形（例: `/users/{userId}`）
```

**削減**: 約200トークン → 約50トークン（75%削減）

**手法2: 箇条書きの活用**

📝 **最適化前**:
```markdown
関数には必ずJSDocを記述してください。JSDocには関数の説明、パラメータの説明、戻り値の説明、例外の説明を含めてください。
```

📝 **最適化後**:
```markdown
関数のJSDoc:
- 説明
- パラメータ
- 戻り値
- 例外
```

**削減**: 約80トークン → 約30トークン（62.5%削減）

**手法3: 表の活用**

📝 **最適化前**:
```markdown
変数はcamelCaseを使用します。例: userName, orderTotal
関数はcamelCaseを使用します。例: getUserById, calculateTotal
クラスはPascalCaseを使用します。例: UserService, OrderController
定数はUPPER_SNAKE_CASEを使用します。例: MAX_RETRY_COUNT, API_BASE_URL
```

📝 **最適化後**:
```markdown
| 種類 | 形式 | 例 |
|------|------|-----|
| 変数 | camelCase | userName |
| 関数 | camelCase | getUserById |
| クラス | PascalCase | UserService |
| 定数 | UPPER_SNAKE_CASE | MAX_RETRY_COUNT |
```

**削減**: 約150トークン → 約80トークン（46.7%削減）

💡 **初心者向けポイント**: 圧縮しすぎると理解しにくくなります。バランスが重要です。

---

#### 戦略2: 重複の削減

**目的**: 複数ファイルで重複する情報を統合

**手法1: 共通情報の統合**

📝 **最適化前**:

`coding.md`:
```markdown
# コーディング規約

プロジェクト名: My Project
技術スタック: Node.js, TypeScript, React
```

`api-design.md`:
```markdown
# API設計規約

プロジェクト名: My Project
技術スタック: Node.js, TypeScript, React
```

📝 **最適化後**:

`README.md`:
```markdown
# My Project

技術スタック: Node.js, TypeScript, React
```

`coding.md`:
```markdown
# コーディング規約

（プロジェクト情報はREADME.mdを参照）
```

`api-design.md`:
```markdown
# API設計規約

（プロジェクト情報はREADME.mdを参照）
```

**削減**: 約200トークン → 約100トークン（50%削減）

**手法2: 参照の活用**

📝 **最適化前**:

`frontend.md`:
```markdown
# フロントエンド規約

## 命名規則
- 変数: camelCase
- 関数: camelCase
- クラス: PascalCase
- 定数: UPPER_SNAKE_CASE
```

`backend.md`:
```markdown
# バックエンド規約

## 命名規則
- 変数: camelCase
- 関数: camelCase
- クラス: PascalCase
- 定数: UPPER_SNAKE_CASE
```

📝 **最適化後**:

`coding.md`:
```markdown
# コーディング規約

## 命名規則
- 変数: camelCase
- 関数: camelCase
- クラス: PascalCase
- 定数: UPPER_SNAKE_CASE
```

`frontend.md`:
```markdown
# フロントエンド規約

命名規則はcoding.mdを参照
```

`backend.md`:
```markdown
# バックエンド規約

命名規則はcoding.mdを参照
```

**削減**: 約300トークン → 約150トークン（50%削減）

💡 **初心者向けポイント**: 重複を削減すると、メンテナンスも容易になります。

---

#### 戦略3: 構造化の工夫

**目的**: 情報を効率的に構造化

**手法1: 階層構造の活用**

📝 **最適化前**:
```markdown
# ルール

コーディング規約、API設計規約、デプロイメント規約、セキュリティ規約があります。

コーディング規約には命名規則、コメント、エラーハンドリングが含まれます。

API設計規約にはエンドポイント命名、HTTPメソッド、レスポンス形式が含まれます。
```

📝 **最適化後**:
```markdown
# ルール

## コーディング規約
- 命名規則
- コメント
- エラーハンドリング

## API設計規約
- エンドポイント命名
- HTTPメソッド
- レスポンス形式
```

**削減**: 約150トークン → 約80トークン（46.7%削減）

**手法2: テンプレートの活用**

📝 **最適化前**:

各ルールファイルに同じ構造を記述。

📝 **最適化後**:

テンプレートを作成し、各ルールファイルはテンプレートに従う。

`template.md`:
```markdown
# {ルール名}

## 目的
{目的}

## ルール
{ルール}

## 例
{例}
```

各ルールファイル:
````markdown
# コーディング規約

## 目的
一貫したコードスタイルの維持

## ルール
- 命名規則: camelCase
- コメント: JSDoc

## 例
```javascript
/**
 * ユーザーを取得
 */
function getUser() {}
```
````

💡 **初心者向けポイント**: 構造化すると、AIの理解も向上します。

---

#### 7.1.2 ファイル分割戦略

#### 分割の基準

**基準1: サイズ**
- 1ファイル5000トークン以下
- 10KB以下

**基準2: 責任**
- 1ファイル1トピック
- 関連する情報をまとめる

**基準3: 使用頻度**
- 頻繁に使用: 小さく分割
- 稀に使用: まとめる

#### 分割の方法

**方法1: トピック別分割**

**分割前**:

`rules.md`:
```markdown
# ルール

## コーディング規約
...

## API設計規約
...

## デプロイメント規約
...
```

**分割後**:

`coding.md`:
```markdown
# コーディング規約
...
```

`api-design.md`:
```markdown
# API設計規約
...
```

`deployment.md`:
```markdown
# デプロイメント規約
...
```

**方法2: 階層別分割**

**分割前**:

`aws-rules.md`:
```markdown
# AWS規約

## Lambda
...

## DynamoDB
...

## S3
...
```

**分割後**:

`aws/lambda.md`:
```markdown
# Lambda規約
...
```

`aws/dynamodb.md`:
```markdown
# DynamoDB規約
...
```

`aws/s3.md`:
```markdown
# S3規約
...
```

#### 管理の工夫

**ディレクトリ構造**:
```
.amazonq/
└── rules/
    ├── README.md          # インデックス
    ├── coding.md
    ├── api-design.md
    ├── deployment.md
    └── aws/
        ├── lambda.md
        ├── dynamodb.md
        └── s3.md
```

**インデックスファイル**:

`rules/README.md`:
```markdown
# ルール一覧

## 一般
- コーディング規約（`coding.md`）
- API設計規約（`api-design.md`）
- デプロイメント規約（`deployment.md`）

## AWS
- Lambda規約（`aws/lambda.md`）
- DynamoDB規約（`aws/dynamodb.md`）
- S3規約（`aws/s3.md`）
```

💡 **初心者向けポイント**: 分割しすぎると管理が大変になります。適度な分割を心がけましょう。

---

#### 7.1.3 動的コンテキスト管理

#### Hooksの活用

**ユースケース1: 環境別コンテキスト**

`scripts/pre-chat.sh`:
```bash
#!/bin/bash

# 環境変数を確認
ENV=${ENVIRONMENT:-development}

# 環境別のルールを生成
cat > /tmp/env-rules.md <<EOF
# 環境: $ENV

## 設定
- API URL: $(get_api_url $ENV)
- Database: $(get_db_name $ENV)
- Log Level: $(get_log_level $ENV)
EOF
```

**Agent設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file:///tmp/env-rules.md"
  ],
  "hooks": {
    "pre_chat": "scripts/pre-chat.sh"
  }
}
```

**ユースケース2: Gitブランチ情報**

`scripts/pre-chat.sh`:
```bash
#!/bin/bash

# 現在のブランチ情報を生成
BRANCH=$(git branch --show-current)
COMMIT=$(git log -1 --pretty=%H)
MESSAGE=$(git log -1 --pretty=%B)

cat > /tmp/git-context.md <<EOF
# Git情報

- ブランチ: $BRANCH
- コミット: $COMMIT
- メッセージ: $MESSAGE
EOF
```

**ユースケース3: 動的なファイル選択**

`scripts/pre-chat.sh`:
```bash
#!/bin/bash

# 最近変更されたファイルを取得
git diff --name-only HEAD~5 > /tmp/recent-files.txt

# コンテキストファイルを生成
cat > /tmp/recent-changes.md <<EOF
# 最近の変更

$(cat /tmp/recent-files.txt)
EOF
```

💡 **初心者向けポイント**: Hooksは高度な機能です。基本に慣れてから使用しましょう。

---

### 7.2 チーム開発での活用

#### 7.2.1 共通ルールの共有

#### ルールファイルの構造

**推奨構造**:
```
.amazonq/
└── rules/
    ├── README.md          # インデックス
    ├── coding.md          # コーディング規約
    ├── api-design.md      # API設計規約
    ├── deployment.md      # デプロイメント規約
    ├── security.md        # セキュリティ規約
    └── team/
        ├── workflow.md    # ワークフロー
        └── review.md      # レビュー規約
```

#### バージョン管理

**`.gitignore`**:
```gitignore
# 個人設定は除外
.amazonq/config.json
.amazonq/local-rules.md

# 機密情報は除外
.env
.env.*
config/production.yaml
```

**コミット戦略**:
```bash
# ルールファイルの変更
git add .amazonq/rules/
git commit -m "Update coding standards"

# Agent設定の変更
git add .amazonq/agent.json
git commit -m "Add architecture.md to context"
```

#### レビュープロセス

**プルリクエストテンプレート**:
```markdown
## 変更内容
- [ ] ルールファイルの追加/変更
- [ ] Agent設定の変更

## チェックリスト
- [ ] 機密情報が含まれていないか確認
- [ ] トークン使用量を確認（`/context show`）
- [ ] チームメンバーに共有

## 影響範囲
- 影響を受けるファイル:
- 期待される効果:
```

💡 **初心者向けポイント**: チーム開発では、変更の影響を必ず確認しましょう。

---

#### 7.2.2 プロジェクト標準の確立

#### 標準設定の定義

**標準Agent設定**:

`.amazonq/agent.json`:
```json
{
  "name": "project-standard-agent",
  "description": "Standard agent for the project",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/architecture.md"
  ],
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

#### ドキュメント化

**`.amazonq/README.md`**:
````markdown
# Amazon Q Developer CLI設定

## Agent設定

このプロジェクトでは標準Agent設定を使用しています。

### 含まれるファイル
- README.md - プロジェクト概要
- .amazonq/rules/**/*.md - プロジェクトルール
- docs/architecture.md - システム構成

### 除外されるファイル
- .env - 環境変数（機密情報）
- config/production.yaml - 本番設定（機密情報）
- node_modules/ - 依存関係
- .git/ - Gitリポジトリ

### 使用方法
```bash
# Agentを起動
q chat --agent project-standard-agent

# コンテキストを確認
/context show
```

### トラブルシューティング
- ファイルが読み込まれない → [トラブルシューティングガイド](../06_troubleshooting/02_common-issues.md)
- トークン制限を超える → ファイルを削減
````

#### 周知方法

**チームミーティング**:
- Agent設定の説明
- 使用方法のデモ
- 質疑応答

**ドキュメント**:
- README.mdに記載
- Wikiに詳細を記載
- Slackで共有

**オンボーディング**:
- 新メンバーへの説明
- セットアップ支援
- フィードバック収集

💡 **初心者向けポイント**: 標準を確立することで、チーム全体の生産性が向上します。

---

#### 7.2.3 バージョン管理との統合

#### `.gitignore`の設定

```gitignore
# Amazon Q Developer CLI
.amazonq/config.json      # 個人設定
.amazonq/local-rules.md   # 個人ルール

# 機密情報
.env
.env.*
config/production.yaml
config/staging.yaml
*.key
*.pem
secrets/

# 依存関係
node_modules/
venv/

# ビルド成果物
dist/
build/
.next/

# ログ
logs/
*.log
```

#### コミット戦略

**ルールファイルの変更**:
```bash
git add .amazonq/rules/
git commit -m "feat: Add API design guidelines"
```

**Agent設定の変更**:
```bash
git add .amazonq/agent.json
git commit -m "chore: Update agent context files"
```

#### ブランチ戦略

**機能ブランチ**:
```bash
# 新しいルールを追加
git checkout -b feature/add-security-rules

# ルールファイルを作成
touch .amazonq/rules/security.md

# コミット
git add .amazonq/rules/security.md
git commit -m "feat: Add security guidelines"

# プルリクエスト
git push origin feature/add-security-rules
```

💡 **初心者向けポイント**: Agent設定もコードと同様にバージョン管理しましょう。

---

### 7.3 実装の内部詳細

#### 7.3.1 内部動作の理解

#### 読み込みプロセスの詳細

**ステップ1: Agent起動**
```
q chat --agent my-agent
↓
Agent設定を読み込み
↓
resources フィールドを解析
```

**ステップ2: ファイルパスの解決**
```
"file://README.md"
↓
相対パスを絶対パスに変換
↓
/path/to/project/README.md
```

**ステップ3: ファイルの読み込み**
```
ファイルを読み込み
↓
UTF-8でデコード
↓
テキストデータ
```

**ステップ4: トークン化**
```
テキストデータ
↓
トークンに分割
↓
トークン列
```

**ステップ5: コンテキストに追加**
```
トークン列
↓
コンテキストウィンドウに追加
↓
AIが利用可能
```

#### トークン化の仕組み

**トークンとは**:
- AIが理解できる最小単位
- 英語: 約4文字 = 1トークン
- 日本語: 約2-3文字 = 1トークン

**例**:
```
"Hello, World!" → ["Hello", ",", " World", "!"] (4トークン)
"こんにちは" → ["こん", "にち", "は"] (3トークン)
```

#### メモリ管理

**コンテキストウィンドウ**:
- 最大容量: 80000トークン
- コンテキスト: 75%まで（60000トークン）
- 会話と応答: 25%（20000トークン）

**メモリ使用量**:
- 1トークン ≈ 4バイト
- 60000トークン ≈ 240KB

💡 **初心者向けポイント**: 内部動作を理解すると、最適化がしやすくなります。

---

#### 7.3.2 JSON Schemaの仕様

#### スキーマの全体像

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Agent name"
    },
    "description": {
      "type": "string",
      "description": "Agent description"
    },
    "resources": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^file://"
      },
      "description": "Context files"
    },
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
              }
            }
          }
        }
      }
    }
  },
  "required": ["name", "resources"]
}
```

#### 各フィールドの詳細

**`name`**:
- 型: string
- 必須: Yes
- 説明: Agent名

**`description`**:
- 型: string
- 必須: No
- 説明: Agentの説明

**`resources`**:
- 型: array of string
- 必須: Yes
- 説明: コンテキストファイルのパス
- パターン: `^file://`

**`tools.fs_read.deniedPaths`**:
- 型: array of string
- 必須: No
- 説明: 読み込みを拒否するパス

#### バリデーションルール

**ルール1: `file://`プレフィックス**
```json
{
  "resources": [
    "file://README.md"  // ✓
  ]
}
```

**ルール2: 配列形式**
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**ルール3: 必須フィールド**
```json
{
  "name": "my-agent",  // 必須
  "resources": []      // 必須
}
```

💡 **初心者向けポイント**: JSON Schemaを理解すると、設定ミスを防げます。

---

## まとめ

### 重要なポイント

1. **最適化戦略**
   - トークン効率: 圧縮、重複削減、構造化
   - ファイル分割: サイズ、責任、使用頻度
   - 動的管理: Hooksの活用

2. **チーム開発**
   - 共通ルール: バージョン管理、レビュー
   - プロジェクト標準: 定義、ドキュメント化、周知
   - バージョン管理: .gitignore、コミット戦略

3. **内部詳細**
   - 読み込みプロセス: 5ステップ
   - トークン化: 英語4文字、日本語2-3文字
   - JSON Schema: 仕様とバリデーション

### 次のステップ

第8章では、参考情報を提供します。

---

**出典**:
- [実装コード](https://github.com/aws/amazon-q-developer-cli/blob/main/crates/chat-cli/src/cli/agent/mod.rs)
- [JSON Schema](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json)

---

## 📖 ナビゲーション

← **前へ**: [第6章: トラブルシューティング](06_troubleshooting.md) | **次へ**: [第8章: 参考情報](08_reference.md) →

---

最終更新: 2025-11-01

