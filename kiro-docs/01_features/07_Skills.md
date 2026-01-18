# Kiro CLI Skills機能（Progressive Context Loading）

**出典**: [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)

## 概要

Kiro CLI v1.24.0（2026年1月16日リリース）で追加されたSkills機能について詳細に解説します。この機能により、大規模なドキュメントセットを効率的に管理し、コンテキストウィンドウを圧迫せずに必要な情報をオンデマンドでロードできるようになりました。

### Skills機能とは

Skills機能は、**段階的コンテキストロード（Progressive Context Loading）**を実現する新しいリソースタイプです。従来の`file://`リソースとは異なり、起動時にはメタデータ（名前と説明）のみをロードし、本文はエージェントが必要と判断した時にオンデマンドでロードします。

### 主な特徴

- **段階的ロード**: 起動時はメタデータのみ、本文はオンデマンド
- **コンテキスト効率化**: 常時コンテキストウィンドウを消費しない
- **大規模ドキュメント対応**: 数百MBのドキュメントセットも管理可能
- **YAMLフロントマター必須**: 名前と説明を含むメタデータが必要

### 従来のfile://リソースとの違い

| 項目 | file:// | skill:// |
|------|---------|----------|
| ロードタイミング | 起動時に全文 | メタデータのみ起動時、本文はオンデマンド |
| コンテキスト消費 | 常時消費 | 必要時のみ消費 |
| 適用場面 | 小規模な必須ファイル | 大規模なドキュメントセット |
| メタデータ | 不要 | YAMLフロントマター必須 |
| 用途 | プロジェクト設定、標準 | ガイド、リファレンス、ベストプラクティス |

### なぜSkills機能が必要なのか

従来の`file://`リソースでは、すべてのファイルが起動時に全文ロードされるため、大規模なドキュメントセットを扱う場合、以下の問題が発生していました：

1. **コンテキストウィンドウの圧迫**: 起動時に大量のトークンを消費
2. **起動時間の増加**: 大量のファイルを読み込むため起動が遅い
3. **不要な情報のロード**: 使用しない情報もすべてロードされる

Skills機能は、これらの問題を解決し、大規模なドキュメントセットを効率的に管理できるようにします。

## 📋 Zenn記事の詳細内容確認

**注意**: v1.24.0のSkills機能に関するZenn記事は現時点で公開されていません。本ドキュメントは公式Changelogおよび公式ドキュメントの情報に基づいて作成されています。

### 参考情報源

- [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)
- [Agent Configuration Reference - Skill Resources](https://kiro.dev/docs/cli/custom-agents/configuration-reference/#skill-resources)

## Skills機能詳細

### 基本概念

Skills機能は、大規模なドキュメントセット向けに設計された新しいリソースタイプです。従来の`file://`リソースとは異なり、**段階的コンテキストロード**を実現します。

#### 段階的コンテキストロードとは

1. **起動時**: メタデータ（名前と説明）のみロード
2. **実行時**: エージェントが必要と判断した時に本文をオンデマンドでロード
3. **終了時**: 不要になった本文はコンテキストから解放

この仕組みにより、大規模なドキュメントセットを扱う場合でも、コンテキストウィンドウを効率的に使用できます。

### Skillファイルの構造

Skillファイルは、YAMLフロントマターとMarkdown本文で構成されます。

#### 必須要素

1. **YAMLフロントマター**: メタデータ（名前と説明）
2. **Markdown本文**: 実際のコンテンツ

#### ファイル形式

```markdown
---
name: skill-name
description: Brief description of what this skill provides. Use when...
---

# Skill Title

... full content here ...
```

#### YAMLフロントマターの詳細

| フィールド | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| `name` | ✅ | Skillの一意な識別子 | `dynamodb-data-modeling` |
| `description` | ✅ | Skillの説明（エージェントが判断に使用） | `Guide for DynamoDB data modeling best practices. Use when designing or analyzing DynamoDB schema.` |

**重要**: `description`フィールドは、エージェントが適切なタイミングで本文をロードするための判断材料となります。明確で具体的な説明を記述してください。

### 設定方法

#### Agent設定ファイルでの指定

```json
{
  "resources": [
    "skill://.kiro/skills/**/SKILL.md"
  ]
}
```

#### 設定のポイント

| 項目 | 説明 | 例 |
|------|------|-----|
| プロトコル | `skill://` を使用 | `skill://.kiro/skills/` |
| パス | プロジェクトルートからの相対パス | `.kiro/skills/` |
| Globパターン | ワイルドカードで複数ファイル指定可能 | `**/SKILL.md` |

#### 複数のSkillディレクトリ

```json
{
  "resources": [
    "skill://.kiro/skills/aws/**/*.md",
    "skill://.kiro/skills/architecture/**/*.md",
    "skill://.kiro/skills/best-practices/**/*.md"
  ]
}
```

### コンテキスト管理との関連

Skills機能は、Kiro CLIの4つのコンテキスト管理アプローチの1つです。

| アプローチ | コンテキスト消費 | 永続性 | 最適な用途 |
|-----------|----------------|--------|-----------|
| **Agent Resources** | 常時消費 | セッション間で永続 | 必須プロジェクトファイル、標準、設定 |
| **Skills** | オンデマンド | セッション間で永続 | 大規模ガイド、リファレンスドキュメント |
| **Session Context** | 常時消費 | 現在のセッションのみ | 一時ファイル、クイック実験 |
| **Knowledge Bases** | 検索時のみ | セッション間で永続 | 大規模コードベース、広範なドキュメント |

#### 使い分けの基準

| 条件 | 推奨アプローチ |
|------|--------------|
| 小規模な必須ファイル（< 10KB） | Agent Resources (`file://`) |
| 大規模なガイド（> 10KB） | Skills (`skill://`) |
| 巨大なコードベース（> 1MB） | Knowledge Bases |
| 一時的な参照 | Session Context |

### 動作の仕組み

#### 1. 起動時

```
Kiro CLI起動
  ↓
Agent設定読み込み
  ↓
Skillファイル検索（Globパターン）
  ↓
YAMLフロントマター読み込み（メタデータのみ）
  ↓
Skillリスト作成（name + description）
```

**コンテキスト消費**: メタデータのみ（数百バイト程度）

#### 2. 実行時

```
ユーザーの質問
  ↓
エージェントがSkillリストを確認
  ↓
関連するSkillを判断（descriptionから）
  ↓
必要なSkillの本文をロード
  ↓
本文を使用して回答生成
```

**コンテキスト消費**: 必要なSkillの本文のみ

#### 3. 終了時

```
タスク完了
  ↓
不要になったSkillの本文を解放
  ↓
メタデータのみ保持
```

**コンテキスト消費**: メタデータのみに戻る

## セットアップ/使用方法

### 1. Skillファイルの作成

#### ステップ1: ディレクトリ構造の作成

```bash
# プロジェクトルートで実行
mkdir -p .kiro/skills/aws
mkdir -p .kiro/skills/architecture
mkdir -p .kiro/skills/best-practices
```

#### ステップ2: Skillファイルの作成

```bash
# DynamoDBデータモデリングのSkillを作成
cat > .kiro/skills/aws/dynamodb-data-modeling.md << 'EOF'
---
name: dynamodb-data-modeling
description: Guide for DynamoDB data modeling best practices. Use when designing or analyzing DynamoDB schema.
---

# DynamoDB Data Modeling

## Overview

This guide provides best practices for DynamoDB data modeling.

## Key Concepts

### Single Table Design

...

### Access Patterns

...

## Examples

...
EOF
```

#### ステップ3: Agent設定ファイルの更新

```bash
# .kiro/agents/my-agent.json
cat > .kiro/agents/my-agent.json << 'EOF'
{
  "name": "my-agent",
  "description": "My custom agent with Skills",
  "resources": [
    "skill://.kiro/skills/**/*.md"
  ]
}
EOF
```

### 2. Skillの使用

#### 起動

```bash
# カスタムエージェントで起動
kiro-cli chat --agent my-agent
```

#### 使用例

```bash
# DynamoDBのデータモデリングについて質問
> DynamoDBのシングルテーブルデザインについて教えて

# エージェントが自動的にdynamodb-data-modelingスキルをロード
# 本文を使用して回答を生成
```

### 3. Skillの確認

#### 利用可能なSkillの確認

```bash
# エージェント内で確認
> 利用可能なSkillを教えて
```

**出力例**（推定）:

```
利用可能なSkills:
1. dynamodb-data-modeling - Guide for DynamoDB data modeling best practices
2. lambda-best-practices - Best practices for AWS Lambda development
3. api-design-patterns - RESTful API design patterns and guidelines
```

### 4. Skillファイルのテンプレート

#### 基本テンプレート

```markdown
---
name: skill-name
description: Brief description. Use when...
---

# Skill Title

## Overview

Brief overview of the skill.

## Key Concepts

### Concept 1

...

### Concept 2

...

## Examples

### Example 1

...

## Best Practices

1. ...
2. ...

## Common Pitfalls

1. ...
2. ...

## References

- [Link 1](https://example.com)
- [Link 2](https://example.com)
```

#### 高度なテンプレート（複数セクション）

```markdown
---
name: advanced-skill
description: Comprehensive guide for advanced topics. Use when...
---

# Advanced Skill

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Core Concepts](#core-concepts)
4. [Implementation](#implementation)
5. [Examples](#examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)
```

## Overview

...

## Prerequisites

...

## Core Concepts

...

## Implementation

...

## Examples

...

## Best Practices

...

## Troubleshooting

...

## References

...
```

## 実用的なユースケース

### ユースケース1: AWSサービスのベストプラクティス集

#### シナリオ

AWSの各サービスのベストプラクティスを大量に管理し、必要な時にだけ参照したい。

#### 実装

```bash
# ディレクトリ構造
.kiro/skills/aws/
├── dynamodb-best-practices.md
├── lambda-best-practices.md
├── s3-best-practices.md
├── api-gateway-best-practices.md
└── cloudformation-best-practices.md
```

**Skillファイル例**（lambda-best-practices.md）:

```markdown
---
name: lambda-best-practices
description: Best practices for AWS Lambda development. Use when designing, implementing, or optimizing Lambda functions.
---

# AWS Lambda Best Practices

## Cold Start Optimization

...

## Memory Configuration

...

## Error Handling

...
```

**Agent設定**:

```json
{
  "resources": [
    "skill://.kiro/skills/aws/**/*.md"
  ]
}
```

#### メリット

- **コンテキスト効率化**: 5つのベストプラクティス文書（合計50KB）を常時ロードせず、必要な時だけロード
- **起動時間短縮**: メタデータのみロードするため起動が高速
- **柔軟な拡張**: 新しいサービスのベストプラクティスを追加しても起動時間に影響しない

### ユースケース2: アーキテクチャパターン集

#### シナリオ

マイクロサービス、サーバーレス、イベント駆動など、複数のアーキテクチャパターンを管理したい。

#### 実装

```bash
# ディレクトリ構造
.kiro/skills/architecture/
├── microservices-patterns.md
├── serverless-patterns.md
├── event-driven-patterns.md
└── cqrs-patterns.md
```

**Skillファイル例**（serverless-patterns.md）:

```markdown
---
name: serverless-patterns
description: Serverless architecture patterns and best practices. Use when designing serverless applications or discussing serverless architecture.
---

# Serverless Architecture Patterns

## API Gateway + Lambda Pattern

...

## Event-Driven Pattern

...

## Step Functions Orchestration

...
```

#### メリット

- **専門知識の分離**: 各パターンを独立したSkillとして管理
- **オンデマンドロード**: 議論しているパターンのみロード
- **保守性向上**: パターンごとに独立して更新可能

### ユースケース3: チーム標準・ガイドライン

#### シナリオ

コーディング規約、レビューガイドライン、デプロイ手順など、チームの標準文書を管理したい。

#### 実装

```bash
# ディレクトリ構造
.kiro/skills/team-standards/
├── coding-standards.md
├── review-guidelines.md
├── deployment-procedures.md
└── security-checklist.md
```

**Skillファイル例**（coding-standards.md）:

```markdown
---
name: coding-standards
description: Team coding standards and conventions. Use when writing code or reviewing code.
---

# Coding Standards

## Naming Conventions

...

## Code Structure

...

## Documentation Requirements

...
```

#### メリット

- **標準の一元管理**: すべての標準文書を1箇所で管理
- **自動適用**: コード生成時に自動的に標準を参照
- **一貫性確保**: チーム全体で同じ標準を使用

## ベストプラクティス

### 1. 具体的で明確なdescriptionを記述する

#### ❌ 悪い例

```yaml
---
name: dynamodb
description: DynamoDB guide
---
```

**問題点**: エージェントがいつこのSkillをロードすべきか判断できない

#### ✅ 良い例

```yaml
---
name: dynamodb-data-modeling
description: Guide for DynamoDB data modeling best practices. Use when designing or analyzing DynamoDB schema, discussing access patterns, or implementing single table design.
---
```

**理由**: 具体的な使用タイミングを明示することで、エージェントが適切に判断できる

### 2. 適切な粒度でSkillを分割する

#### 粒度の基準

| 粒度 | ファイルサイズ | 推奨 | 理由 |
|------|--------------|------|------|
| 細かすぎる | < 5KB | ❌ | 管理コストが高い、メタデータのオーバーヘッド |
| 適切 | 5-50KB | ✅ | バランスが良い、必要な情報のみロード |
| 粗すぎる | > 50KB | ❌ | ロード時のコンテキスト消費が大きい |

#### 分割の例

**❌ 粗すぎる**:

```
aws-all-services.md (200KB)
```

**✅ 適切**:

```
aws/dynamodb-best-practices.md (20KB)
aws/lambda-best-practices.md (15KB)
aws/s3-best-practices.md (18KB)
```

### 3. 階層的なディレクトリ構造を使用する

#### 推奨構造

```bash
.kiro/skills/
├── aws/
│   ├── compute/
│   │   ├── lambda-best-practices.md
│   │   └── ec2-best-practices.md
│   ├── storage/
│   │   ├── s3-best-practices.md
│   │   └── dynamodb-best-practices.md
│   └── networking/
│       ├── vpc-design.md
│       └── api-gateway-patterns.md
├── architecture/
│   ├── microservices-patterns.md
│   └── serverless-patterns.md
└── team-standards/
    ├── coding-standards.md
    └── review-guidelines.md
```

**メリット**:

- 論理的な整理
- 検索性の向上
- 保守性の向上

### 4. file://とskill://を適切に使い分ける

#### 使い分けの基準

| 条件 | 使用するプロトコル | 理由 |
|------|------------------|------|
| 常に必要な情報 | `file://` | 常時ロードが効率的 |
| 時々必要な情報 | `skill://` | オンデマンドロードが効率的 |
| ファイルサイズ < 10KB | `file://` | ロードコストが小さい |
| ファイルサイズ > 10KB | `skill://` | コンテキスト節約 |

#### 実装例

```json
{
  "resources": [
    "file://.kiro/project-config.md",
    "file://.kiro/coding-standards-summary.md",
    "skill://.kiro/skills/**/*.md"
  ]
}
```

### 5. Skillファイルの命名規則

#### 推奨命名規則

- **ケバブケース**: `dynamodb-data-modeling.md`
- **説明的な名前**: 内容が明確にわかる名前
- **一貫性**: プロジェクト全体で統一

#### 例

```
✅ dynamodb-data-modeling.md
✅ lambda-best-practices.md
✅ api-design-patterns.md

❌ db.md (不明確)
❌ DynamoDB_DataModeling.md (スネークケース)
❌ dynamoDBDataModeling.md (キャメルケース)
```

### 6. Skillファイルの更新管理

#### バージョン管理

```markdown
---
name: dynamodb-data-modeling
description: Guide for DynamoDB data modeling best practices. Use when designing or analyzing DynamoDB schema.
version: 1.2.0
last_updated: 2026-01-15
---

# DynamoDB Data Modeling
```

**Version**: 1.2.0  
**Last Updated**: 2026-01-15

## Changelog

### v1.2.0 (2026-01-15)
- Added section on Global Secondary Indexes
- Updated examples for single table design

### v1.1.0 (2025-12-01)
- Added access pattern examples
- Improved best practices section

...
```

**メリット**:

- 変更履歴の追跡
- チーム内での情報共有
- 古い情報の識別

## トラブルシューティング

### 問題1: Skillが認識されない

#### 症状

```bash
> 利用可能なSkillを教えて
# 結果: Skillが見つかりません
```

#### 原因と対処法

**原因1: Agent設定ファイルにSkillが登録されていない**

```bash
# Agent設定ファイルを確認
cat .kiro/agents/my-agent.json

# resourcesセクションにskill://が含まれているか確認
```

**対処法**:

```json
{
  "resources": [
    "skill://.kiro/skills/**/*.md"
  ]
}
```

**原因2: Skillファイルのパスが間違っている**

```bash
# Skillファイルの存在確認
ls -la .kiro/skills/

# Globパターンの確認
find .kiro/skills/ -name "*.md"
```

**対処法**: パスを修正

**原因3: YAMLフロントマターが不正**

```bash
# Skillファイルの先頭を確認
head -n 10 .kiro/skills/aws/dynamodb-data-modeling.md
```

**対処法**: YAMLフロントマターを修正

```markdown
---
name: dynamodb-data-modeling
description: Guide for DynamoDB data modeling best practices.
---
```

### 問題2: Skillの本文がロードされない

#### 症状

```bash
> DynamoDBのデータモデリングについて教えて
# 結果: 一般的な情報のみ、Skillの内容が反映されていない
```

#### 原因と対処法

**原因1: descriptionが不明確**

```yaml
# 悪い例
description: DynamoDB guide
```

**対処法**: より具体的なdescriptionに変更

```yaml
# 良い例
description: Guide for DynamoDB data modeling best practices. Use when designing or analyzing DynamoDB schema, discussing access patterns, or implementing single table design.
```

**原因2: 質問がSkillの内容と関連していない**

**対処法**: Skillの内容に関連する質問をする

```bash
# 関連する質問
> DynamoDBのシングルテーブルデザインについて教えて
> DynamoDBのアクセスパターンの設計方法は？
```

### 問題3: コンテキストウィンドウがすぐに埋まる

#### 症状

```bash
# 数回の質問でコンテキストウィンドウが埋まる
> コンテキストウィンドウの使用状況を教えて
# 結果: 90%以上使用
```

#### 原因と対処法

**原因: Skillファイルが大きすぎる**

```bash
# Skillファイルのサイズ確認
du -h .kiro/skills/**/*.md
```

**対処法**: Skillファイルを分割

```bash
# 1つの大きなファイル（100KB）
# aws-all-services.md

# 複数の小さなファイル（各20KB）
# aws/dynamodb-best-practices.md
# aws/lambda-best-practices.md
# aws/s3-best-practices.md
```

### 問題4: Skillファイルの文法エラー

#### 症状

```bash
# Kiro CLI起動時にエラー
Error: Invalid YAML front matter in skill file
```

#### 原因と対処法

**原因: YAMLフロントマターの文法エラー**

```bash
# Skillファイルを確認
cat .kiro/skills/aws/dynamodb-data-modeling.md
```

**よくあるエラー**:

```yaml
# ❌ クォートが閉じていない
description: "Guide for DynamoDB

# ❌ コロンの後にスペースがない
name:dynamodb-data-modeling

# ❌ フロントマターの区切りが不正
--
name: dynamodb-data-modeling
--
```

**対処法**: 正しいYAML文法に修正

```yaml
# ✅ 正しい例
---
name: dynamodb-data-modeling
description: Guide for DynamoDB data modeling best practices.
---
```

## まとめ

### Skills機能の重要ポイント

1. **段階的コンテキストロード**: 起動時はメタデータのみ、本文はオンデマンド
2. **コンテキスト効率化**: 大規模ドキュメントセットを効率的に管理
3. **YAMLフロントマター必須**: 名前と説明を含むメタデータが必要
4. **file://との使い分け**: 小規模な必須ファイルは`file://`、大規模なガイドは`skill://`

### Skills機能の活用シーン

| シーン | メリット |
|--------|---------|
| AWSサービスのベストプラクティス集 | 数十のサービスのガイドを効率的に管理 |
| アーキテクチャパターン集 | 必要なパターンのみオンデマンドロード |
| チーム標準・ガイドライン | 標準文書を一元管理、自動適用 |
| 大規模リファレンス | 数百MBのドキュメントも管理可能 |

### file://、skill://、Knowledge Basesの使い分け

| 条件 | 推奨 |
|------|------|
| 小規模な必須ファイル（< 10KB） | `file://` |
| 大規模なガイド（10-100KB） | `skill://` |
| 巨大なコードベース（> 1MB） | Knowledge Bases |

### ベストプラクティスのまとめ

1. **具体的なdescription**: エージェントが判断できる明確な説明
2. **適切な粒度**: 5-50KBのファイルサイズ
3. **階層的な構造**: 論理的なディレクトリ構成
4. **命名規則の統一**: ケバブケース、説明的な名前
5. **バージョン管理**: 変更履歴の追跡

### 次のステップ

1. **Skillファイルの作成**: プロジェクトに必要なガイドを作成
2. **Agent設定の更新**: `skill://`リソースを追加
3. **動作確認**: Skillが正しく認識されるか確認
4. **継続的な改善**: Skillファイルを継続的に更新・改善

### 参考リンク

- [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)
- [Agent Configuration Reference - Skill Resources](https://kiro.dev/docs/cli/custom-agents/configuration-reference/#skill-resources)
- [Context Management Documentation](https://kiro.dev/docs/cli/chat/context/)

---

**Skills機能を活用して、大規模なドキュメントセットを効率的に管理し、コンテキストウィンドウを最適化しましょう！**
