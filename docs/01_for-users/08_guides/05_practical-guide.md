[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [コンテキスト管理ガイド](README.md) > 05 Practical Guide

---

## 5. 実践ガイド

この章では、第4章で学んだ考え方を実践する具体的な設定例を提供します。すべての設定例は検証済みで、コピー&ペーストで使用できます。

---

### 5.1 基本設定の実装

#### 5.1.1 最小限の設定

**目的**: 最も基本的な設定で始める

📝 **設定例**:
```json
{
  "name": "minimal-agent",
  "description": "Minimal agent configuration",
  "resources": [
    "file://README.md"
  ]
}
```

**含まれる情報**:
- プロジェクトの概要
- 主要な機能
- 技術スタック

**トークン使用量**: 約5000トークン（6.25%）

**適用場面**:
- 新規プロジェクト
- 小規模プロジェクト
- 個人利用

💡 **初心者向けポイント**: まずはこの設定から始めて、必要に応じて追加しましょう。

---

#### 5.1.2 推奨の基本設定

**目的**: 実装コードのデフォルト値に基づく推奨設定

📝 **設定例**:
```json
{
  "name": "recommended-agent",
  "description": "Recommended agent configuration",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**含まれる情報**:
- プロジェクトの概要（README.md）
- プロジェクト固有のルール（.amazonq/rules/）

**トークン使用量**: 約10000-15000トークン（12.5-18.75%）

**適用場面**:
- 一般的なプロジェクト
- チーム開発
- 標準的な使用

💡 **初心者向けポイント**: これが最も推奨される基本設定です。

**ルールファイルの例**:

`.amazonq/rules/coding.md`:
```markdown
# コーディング規約

## 命名規則
- 変数: camelCase
- 関数: camelCase
- クラス: PascalCase
- 定数: UPPER_SNAKE_CASE

## コメント
- 関数には必ずdocstringを記述
- 複雑なロジックには説明コメントを追加

## エラーハンドリング
- すべての例外を適切に処理
- ログを記録
```

`.amazonq/rules/api-design.md`:
```markdown
# API設計規約

## エンドポイント命名
- リソースは複数形: `/users`, `/orders`
- IDは単数形: `/users/{userId}`

## HTTPメソッド
- GET: 取得
- POST: 作成
- PUT: 更新（全体）
- PATCH: 更新（部分）
- DELETE: 削除

## レスポンス形式
- 成功: 200, 201, 204
- エラー: 400, 401, 403, 404, 500
```

---

#### 5.1.3 デフォルト設定の活用

**目的**: 公式実装のデフォルト設定を理解し活用

**公式実装のデフォルト設定**:
```rust
// /crates/chat-cli/src/cli/agent/mod.rs
resources: vec![
    "file://AmazonQ.md",
    "file://AGENTS.md",
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
]
```

📝 **設定例**:
```json
{
  "name": "default-agent",
  "description": "Default agent configuration based on official implementation",
  "resources": [
    "file://README.md",
    "file://AmazonQ.md",
    "file://AGENTS.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**含まれる情報**:
- プロジェクトの概要（README.md）
- Amazon Q固有の情報（AmazonQ.md）
- Agent関連の情報（AGENTS.md）
- プロジェクトルール（.amazonq/rules/）

**トークン使用量**: 約15000-20000トークン（18.75-25%）

**適用場面**:
- Amazon Q CLIを活用するプロジェクト
- Agent機能を多用するプロジェクト
- 公式推奨に従いたい場合

💡 **初心者向けポイント**: AmazonQ.mdとAGENTS.mdはオプションです。必要に応じて追加しましょう。

**カスタマイズ方法**:

**ステップ1: 基本設定から始める**
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**ステップ2: 必要に応じて追加**
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://architecture.md"  // 追加
  ]
}
```

**ステップ3: トークン使用量を確認**
```bash
/context show
# Total tokens: 18000/80000 (22.5%)
```

**ステップ4: 必要に応じて調整**
- 60%以上 → ファイルを削減
- 30%未満 → 追加可能

---

### 5.2 プロジェクトタイプ別実装

#### 5.2.1 一般的な開発プロジェクト

**目的**: 汎用的な開発プロジェクトの設定

📝 **設定例**:
```json
{
  "name": "general-project-agent",
  "description": "Agent for general development project",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://CONTRIBUTING.md",
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
        "node_modules/**",
        "venv/**",
        ".git/**"
      ]
    }
  }
}
```

**設定の意図**:
- `README.md`: プロジェクト概要
- `.amazonq/rules/**/*.md`: プロジェクトルール
- `CONTRIBUTING.md`: 貢献ガイド（チーム開発）
- `docs/architecture.md`: システム構成

**トークン使用量**: 約20000-25000トークン（25-31.25%）

**カスタマイズポイント**:
- チーム開発でない場合: `CONTRIBUTING.md`を削除
- アーキテクチャ図がない場合: `docs/architecture.md`を削除
- API仕様がある場合: `docs/api-spec.md`を追加

💡 **初心者向けポイント**: この設定をベースに、プロジェクトに合わせてカスタマイズしましょう。

---

#### 5.2.2 AWS関連プロジェクト

**目的**: AWS SAM/CDK/CloudFormationプロジェクトの設定

📝 **設定例**:
```json
{
  "name": "aws-project-agent",
  "description": "Agent for AWS-related project",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/architecture.md",
    "file://template.yaml",
    "file://infrastructure/**/*.yaml"
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
        "config/staging.yaml",
        ".aws/**",
        "node_modules/**",
        ".git/**"
      ]
    }
  }
}
```

**設定の意図**:
- `README.md`: プロジェクト概要
- `.amazonq/rules/**/*.md`: プロジェクトルール
- `docs/architecture.md`: AWSアーキテクチャ図
- `template.yaml`: SAMテンプレート
- `infrastructure/**/*.yaml`: CloudFormation/CDKスタック

**トークン使用量**: 約25000-30000トークン（31.25-37.5%）

**カスタマイズポイント**:
- SAMプロジェクト: `template.yaml`を含める
- CDKプロジェクト: `lib/**/*.ts`を含める
- CloudFormationプロジェクト: `infrastructure/**/*.yaml`を含める

💡 **初心者向けポイント**: AWSプロジェクトでは、インフラコードを含めることが重要です。

**ルールファイルの例**:

`.amazonq/rules/aws-naming.md`:
```markdown
# AWS命名規則

## Lambda関数
形式: {service}-{environment}-{function}
例: user-service-prod-create-user

## DynamoDB テーブル
形式: {environment}-{service}-{resource}
例: prod-user-service-users

## S3 バケット
形式: {organization}-{environment}-{service}-{purpose}
例: mycompany-prod-user-service-uploads

## CloudWatch Logs
形式: /aws/lambda/{function-name}
例: /aws/lambda/user-service-prod-create-user
```

---

#### 5.2.3 Web開発プロジェクト

**目的**: Web開発プロジェクト（React/Next.js/Express等）の設定

📝 **設定例**:
```json
{
  "name": "web-project-agent",
  "description": "Agent for web development project",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/api-spec.md",
    "file://package.json",
    "file://tsconfig.json"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*",
        ".env.local",
        "**/*.key",
        "**/*.pem",
        "**/secrets/**",
        "node_modules/**",
        "dist/**",
        "build/**",
        ".next/**",
        ".git/**"
      ]
    }
  }
}
```

**設定の意図**:
- `README.md`: プロジェクト概要
- `.amazonq/rules/**/*.md`: プロジェクトルール
- `docs/api-spec.md`: API仕様
- `package.json`: 依存関係
- `tsconfig.json`: TypeScript設定

**トークン使用量**: 約20000-25000トークン（25-31.25%）

**カスタマイズポイント**:
- TypeScriptでない場合: `tsconfig.json`を削除
- Next.jsの場合: `next.config.js`を追加
- Expressの場合: `src/routes/**/*.ts`を追加

💡 **初心者向けポイント**: Web開発では、API仕様と依存関係が重要です。

**ルールファイルの例**:

`.amazonq/rules/frontend.md`:
```markdown
# フロントエンド規約

## コンポーネント構造
- 1ファイル1コンポーネント
- ファイル名はPascalCase
- ディレクトリ構造: src/components/{feature}/{Component}.tsx

## 状態管理
- グローバル状態: Redux Toolkit
- ローカル状態: useState
- サーバー状態: React Query

## スタイリング
- CSS Modules
- クラス名: camelCase
```

`.amazonq/rules/backend.md`:
```markdown
# バックエンド規約

## ルーティング
- RESTful API
- バージョニング: /api/v1/
- エンドポイント: 複数形

## エラーハンドリング
- すべてのエラーをキャッチ
- 適切なHTTPステータスコード
- エラーメッセージは明確に

## データベース
- ORMを使用（Prisma/TypeORM）
- マイグレーションを管理
- トランザクションを適切に使用
```

---

#### 5.2.4 データサイエンスプロジェクト

**目的**: データサイエンス/機械学習プロジェクトの設定

📝 **設定例**:
```json
{
  "name": "datascience-project-agent",
  "description": "Agent for data science project",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/data-schema.md",
    "file://requirements.txt",
    "file://notebooks/README.md"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*",
        "**/*.key",
        "**/*.pem",
        "**/secrets/**",
        "data/**",
        "models/**",
        "*.pkl",
        "*.h5",
        "*.pt",
        "venv/**",
        ".git/**"
      ]
    }
  }
}
```

**設定の意図**:
- `README.md`: プロジェクト概要
- `.amazonq/rules/**/*.md`: プロジェクトルール
- `docs/data-schema.md`: データスキーマ
- `requirements.txt`: Python依存関係
- `notebooks/README.md`: ノートブックの説明

**トークン使用量**: 約20000-25000トークン（25-31.25%）

**カスタマイズポイント**:
- Jupyter Notebookを使用: `notebooks/**/*.ipynb`を追加（注意: 大きくなりやすい）
- モデル定義を含める: `src/models/**/*.py`を追加
- データパイプラインを含める: `src/pipelines/**/*.py`を追加

💡 **初心者向けポイント**: データサイエンスプロジェクトでは、データスキーマが重要です。

**ルールファイルの例**:

`.amazonq/rules/data-processing.md`:
```markdown
# データ処理規約

## データ読み込み
- Pandasを使用
- エンコーディング: UTF-8
- 欠損値の処理を明示

## データ変換
- パイプラインを使用
- 変換ステップを記録
- 再現可能性を確保

## データ保存
- フォーマット: Parquet（推奨）
- パーティショニング: 日付ベース
- メタデータを記録
```

`.amazonq/rules/modeling.md`:
```markdown
# モデリング規約

## モデル選択
- ベースラインモデルから開始
- 複数のモデルを比較
- クロスバリデーションを実施

## ハイパーパラメータ調整
- Grid Search / Random Search
- 結果を記録
- 最適なパラメータを保存

## モデル評価
- 適切な評価指標を使用
- テストデータで評価
- 結果を可視化
```

---

#### 5.2.5 個人利用

**目的**: 個人プロジェクトの柔軟な設定

📝 **設定例**:
```json
{
  "name": "personal-agent",
  "description": "Agent for personal use",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/personal-rules.md"
  ],
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

**設定の意図**:
- `README.md`: プロジェクト概要
- `.amazonq/rules/personal-rules.md`: 個人的なルール

**トークン使用量**: 約5000-10000トークン（6.25-12.5%）

**カスタマイズポイント**:
- 必要に応じて自由に追加
- トークン制限を気にせず実験
- 個人的な好みを反映

💡 **初心者向けポイント**: 個人利用では、自由に設定を試してみましょう。

**ルールファイルの例**:

`.amazonq/rules/personal-rules.md`:
```markdown
# 個人的なルール

## コーディングスタイル
- 自分が読みやすいスタイル
- コメントは日本語でOK
- 完璧を求めない

## プロジェクト管理
- TODOリストを活用
- 定期的にリファクタリング
- 楽しむことを優先

## 学習
- 新しい技術を試す
- エラーから学ぶ
- ドキュメントを読む
```

---

## まとめ（Part1）

### 重要なポイント

1. **基本設定**
   - 最小限: README.md
   - 推奨: README.md + .amazonq/rules/**/*.md
   - デフォルト: 公式実装に基づく

2. **プロジェクトタイプ別**
   - 一般的な開発: 基本 + CONTRIBUTING.md + architecture.md
   - AWS関連: 基本 + template.yaml + infrastructure/**/*.yaml
   - Web開発: 基本 + api-spec.md + package.json
   - データサイエンス: 基本 + data-schema.md + requirements.txt
   - 個人利用: 自由に設定

### 次のステップ

Part2では、応用実装パターンと実装時の注意点を学びます。

---

**出典**:
- [実装コード](https://github.com/aws/amazon-q-developer-cli/blob/main/crates/chat-cli/src/cli/agent/mod.rs)
- [Agent機能ドキュメント](../02_features/02_agents.md)
# 第5章 Part2: 応用実装パターンと注意点

### 5.3 応用実装パターン

#### 5.3.1 プロジェクトルールの活用

#### ルールファイルの構造

**推奨ディレクトリ構造**:
```
.amazonq/
├── rules/
│   ├── coding.md          # コーディング規約
│   ├── api-design.md      # API設計規約
│   ├── deployment.md      # デプロイメント規約
│   ├── security.md        # セキュリティ規約
│   └── aws/
│       ├── naming.md      # AWS命名規則
│       └── best-practices.md  # AWSベストプラクティス
└── agent.json
```

**Agent設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

これにより、すべてのルールファイルが自動的に読み込まれます。

#### ルールファイルの作成方法

**ステップ1: ルールの特定**

質問:
- プロジェクトで守るべきルールは何か？
- チームで合意されたベストプラクティスは？
- よくある間違いは何か？

**ステップ2: ルールファイルの作成**

`.amazonq/rules/coding.md`:
```markdown
# コーディング規約

## 目的
このドキュメントは、プロジェクト全体で一貫したコードスタイルを維持するためのガイドラインです。

## 命名規則

### 変数
- 形式: camelCase
- 例: `userName`, `orderTotal`
- 理由: JavaScriptの標準的な慣習

### 関数
- 形式: camelCase
- 例: `getUserById`, `calculateTotal`
- 理由: JavaScriptの標準的な慣習

### クラス
- 形式: PascalCase
- 例: `UserService`, `OrderController`
- 理由: JavaScriptの標準的な慣習

### 定数
- 形式: UPPER_SNAKE_CASE
- 例: `MAX_RETRY_COUNT`, `API_BASE_URL`
- 理由: 定数であることを明確にするため

## コメント

### 関数コメント
すべての関数には必ずJSDocを記述:

```javascript
/**
 * ユーザーをIDで取得する
 * @param {string} userId - ユーザーID
 * @returns {Promise<User>} ユーザーオブジェクト
 * @throws {NotFoundError} ユーザーが見つからない場合
 */
async function getUserById(userId) {
  // 実装
}
```

### 複雑なロジック
複雑なロジックには説明コメントを追加:

```javascript
// ユーザーの権限を確認
// 管理者またはリソースの所有者のみアクセス可能
if (user.role === 'admin' || resource.ownerId === user.id) {
  // アクセス許可
}
```

## エラーハンドリング

### 原則
- すべての例外を適切に処理
- エラーメッセージは明確に
- ログを記録

### 例
```javascript
try {
  const user = await getUserById(userId);
  return user;
} catch (error) {
  logger.error('Failed to get user', { userId, error });
  throw new ApplicationError('ユーザーの取得に失敗しました', error);
}
```

## テスト

### カバレッジ
- 最低80%のカバレッジを維持
- すべての公開関数をテスト
- エッジケースをテスト

### テスト構造
```javascript
describe('getUserById', () => {
  it('should return user when user exists', async () => {
    // テスト実装
  });

  it('should throw NotFoundError when user does not exist', async () => {
    // テスト実装
  });
});
```
```

**ステップ3: ルールの適用確認**

```bash
# Agentを起動
q chat --agent my-project

# ルールが適用されているか確認
"新しい関数を作成して"

# AIがルールに従ったコードを生成することを確認
```

💡 **初心者向けポイント**: ルールファイルは段階的に作成しましょう。最初は最小限から始めて、必要に応じて追加します。

---

#### 5.3.2 Hooksとの組み合わせ

#### Hooksの基本

**Hooksとは**: Agent起動時やコマンド実行時に自動的に実行されるスクリプト

📝 **設定例**:
```json
{
  "name": "hooks-agent",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ],
  "hooks": {
    "pre_chat": "scripts/pre-chat.sh",
    "post_chat": "scripts/post-chat.sh"
  }
}
```

#### コンテキストとの連携

**ユースケース1: 動的なコンテキスト追加**

`scripts/pre-chat.sh`:
```bash
#!/bin/bash

# 現在のGitブランチを取得
BRANCH=$(git branch --show-current)

# ブランチ情報をファイルに出力
echo "# Current Branch: $BRANCH" > /tmp/current-branch.md

# 最新のコミットメッセージを取得
git log -1 --pretty=%B > /tmp/latest-commit.md
```

**Agent設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file:///tmp/current-branch.md",
    "file:///tmp/latest-commit.md"
  ],
  "hooks": {
    "pre_chat": "scripts/pre-chat.sh"
  }
}
```

**ユースケース2: 条件付きコンテキスト**

`scripts/pre-chat.sh`:
```bash
#!/bin/bash

# 環境変数を確認
if [ "$ENVIRONMENT" = "production" ]; then
  # 本番環境用のルールを追加
  cp .amazonq/rules/production.md /tmp/env-rules.md
else
  # 開発環境用のルールを追加
  cp .amazonq/rules/development.md /tmp/env-rules.md
fi
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

💡 **初心者向けポイント**: Hooksは高度な機能です。基本設定に慣れてから使用しましょう。

---

#### 5.3.3 複数Agentでの使い分け

#### 複数Agentの設計

**ユースケース**: プロジェクトの異なる側面に特化したAgent

**Agent1: フロントエンド開発用**

`.amazonq/cli-agents/frontend.json`:
```json
{
  "name": "frontend-agent",
  "description": "Agent for frontend development",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/frontend.md",
    "file://docs/ui-design.md",
    "file://package.json"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        "**/*.key",
        "node_modules/**",
        "dist/**",
        ".git/**"
      ]
    }
  }
}
```

**Agent2: バックエンド開発用**

`.amazonq/cli-agents/backend.json`:
```json
{
  "name": "backend-agent",
  "description": "Agent for backend development",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/backend.md",
    "file://docs/api-spec.md",
    "file://docs/database-schema.md"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        "**/*.key",
        "node_modules/**",
        ".git/**"
      ]
    }
  }
}
```

**Agent3: インフラ管理用**

`.amazonq/cli-agents/infrastructure.json`:
```json
{
  "name": "infrastructure-agent",
  "description": "Agent for infrastructure management",
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/aws/naming.md",
    "file://.amazonq/rules/aws/best-practices.md",
    "file://docs/architecture.md",
    "file://infrastructure/**/*.yaml"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        "**/*.key",
        "**/*.pem",
        "config/production.yaml",
        ".git/**"
      ]
    }
  }
}
```

#### Agent切り替えの方法

```bash
# フロントエンド開発
q chat --agent frontend-agent

# バックエンド開発
q chat --agent backend-agent

# インフラ管理
q chat --agent infrastructure-agent
```

#### コンテキストの使い分け

**原則**:
- 各Agentは特定の目的に特化
- 不要な情報を含めない
- トークンを効率的に使用

**メリット**:
- 応答精度の向上
- トークン使用量の削減
- 明確な責任分離

💡 **初心者向けポイント**: 複数Agentは大規模プロジェクトで有効です。小規模プロジェクトでは1つのAgentで十分です。

---

### 5.4 実装時の注意点

#### 5.4.1 アンチパターン

#### アンチパターン1: 広すぎるワイルドカード

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file://**/*.md"
  ]
}
```

**問題点**:
- すべての.mdファイルを読み込む
- 不要なファイルも含まれる
- トークン制限を超える可能性
- パフォーマンスへの影響

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/**/*.md"
  ]
}
```

**修正のポイント**:
- 必要なディレクトリのみ指定
- ワイルドカードの範囲を限定
- トークン使用量を確認

---

#### アンチパターン2: 機密情報を含む

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file://config/**/*.yaml"
  ]
}
```

**問題点**:
- `config/production.yaml`に機密情報が含まれる可能性
- APIキー、パスワードが読み込まれる
- セキュリティリスク

**正しい設定**:
```json
{
  "resources": [
    "file://config/default.yaml"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        "config/production.yaml",
        "config/staging.yaml",
        ".env",
        ".env.*"
      ]
    }
  }
}
```

**修正のポイント**:
- 機密情報を含むファイルを除外
- `deniedPaths`で明示的に除外
- 定期的に確認

---

#### アンチパターン3: 大きすぎるファイル

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file://docs/complete-specification.md"
  ]
}
```

**問題点**:
- ファイルサイズが50KB以上
- トークン使用量が多い（15000トークン以上）
- パフォーマンスへの影響

**正しい設定**:

**方法1: ファイルを分割**
```json
{
  "resources": [
    "file://docs/specification/overview.md",
    "file://docs/specification/api.md",
    "file://docs/specification/database.md"
  ]
}
```

**方法2: Knowledge Basesを使用**
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```
```bash
# Knowledge Baseをセットアップ
/knowledge add docs/
```

**修正のポイント**:
- 1ファイル5000トークン以下を目標
- 大きなファイルは分割
- Knowledge Basesへの移行を検討

---

#### アンチパターン4: 絶対パスの使用

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file:///home/user/projects/my-project/README.md",
    "file:///home/user/projects/my-project/.amazonq/rules/**/*.md"
  ]
}
```

**問題点**:
- 環境依存
- チーム共有不可
- ポータビリティなし

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**修正のポイント**:
- 相対パスを使用
- 環境依存を避ける
- チーム共有を考慮

---

#### 5.4.2 よくある間違い

#### 間違い1: `file://`プレフィックスの忘れ

⚠️ **間違った設定**:
```json
{
  "resources": [
    "README.md",
    ".amazonq/rules/**/*.md"
  ]
}
```

**エラー**: ファイルが読み込まれない

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

**修正方法**: すべてのパスに`file://`を追加

---

#### 間違い2: パスの間違い

⚠️ **間違った設定**:
```json
{
  "resources": [
    "file://docs/architecture.md"
  ]
}
```

**エラー**: ファイルが存在しない（実際は`doc/architecture.md`）

**確認方法**:
```bash
# ファイルの存在確認
ls -la docs/architecture.md
# ls: cannot access 'docs/architecture.md': No such file or directory

# 正しいパスを確認
find . -name "architecture.md"
# ./doc/architecture.md
```

**正しい設定**:
```json
{
  "resources": [
    "file://doc/architecture.md"
  ]
}
```

**修正方法**: ファイルの存在を確認してからパスを指定

---

#### 間違い3: トークン制限の無視

⚠️ **間違った設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/**/*.md",
    "file://src/**/*.py",
    "file://tests/**/*.py"
  ]
}
```

**問題**: トークン使用量が75%を超える

**確認方法**:
```bash
/context show
# Total tokens: 65000/80000 (81.25%)
# ⚠️ Context limit exceeded!
```

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md",
    "file://docs/architecture.md"
  ]
}
```

**修正方法**:
1. `/context show`で確認
2. 不要なファイルを削除
3. Knowledge Basesへ移行

---

#### 5.4.3 問題のある設定例

#### 例1: すべてを含める設定

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file://**/*"
  ]
}
```

**何が問題か**:
- すべてのファイルを読み込む
- 機密情報も含まれる
- トークン制限を超える
- パフォーマンスが悪い

**正しい設定**:
```json
{
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
        "node_modules/**",
        ".git/**"
      ]
    }
  }
}
```

---

#### 例2: セキュリティ設定なし

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://config/**/*.yaml"
  ]
}
```

**何が問題か**:
- `deniedPaths`設定がない
- 機密情報が読み込まれる可能性
- セキュリティリスク

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://config/default.yaml"
  ],
  "tools": {
    "fs_read": {
      "deniedPaths": [
        ".env",
        ".env.*",
        "config/production.yaml",
        "config/staging.yaml",
        "**/*.key",
        "**/*.pem",
        "**/secrets/**"
      ]
    }
  }
}
```

---

#### 例3: 環境依存の設定

⚠️ **問題のある設定**:
```json
{
  "resources": [
    "file:///home/user/projects/my-project/README.md",
    "file://${HOME}/projects/my-project/.amazonq/rules/**/*.md"
  ]
}
```

**何が問題か**:
- 絶対パスを使用
- 環境変数を使用
- チーム共有不可
- ポータビリティなし

**正しい設定**:
```json
{
  "resources": [
    "file://README.md",
    "file://.amazonq/rules/**/*.md"
  ]
}
```

---

## まとめ（Part2）

### 重要なポイント

1. **応用実装パターン**
   - プロジェクトルールの活用: 段階的に作成
   - Hooksとの組み合わせ: 動的なコンテキスト
   - 複数Agentでの使い分け: 目的別に特化

2. **アンチパターン**
   - 広すぎるワイルドカード
   - 機密情報を含む
   - 大きすぎるファイル
   - 絶対パスの使用

3. **よくある間違い**
   - `file://`プレフィックスの忘れ
   - パスの間違い
   - トークン制限の無視

### 次のステップ

第6章では、トラブルシューティングの方法を学びます。

---

**出典**:
- [Agent機能ドキュメント](../02_features/02_agents.md)
- [Agent設定ドキュメント](../03_configuration/03_agent-configuration.md)

---

## 📖 ナビゲーション

← **前へ**: [第4章: ベストプラクティスの考え方](04_best-practices.md) | **次へ**: [第6章: トラブルシューティング](06_troubleshooting.md) →

---

最終更新: 2025-11-01

