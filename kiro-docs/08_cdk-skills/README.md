[ホーム](../README.md) > cdk-skills（CDK 開発支援 Skills 集）

# 08. cdk-skills — AWS DevTools Hero による CDK 開発支援 Skills 集

## 📋 目次

- [概要](#概要)
- [aws-cdk-unit-testing Skill — 全体像](#aws-cdk-unit-testing-skill--全体像)
- [スナップショットテスト](#スナップショットテスト)
- [Fine-grained assertions テスト](#fine-grained-assertions-テスト)
- [バリデーションテスト](#バリデーションテスト)
- [落とし穴（pitfalls 詳細）](#落とし穴pitfalls-詳細)
- [テスト環境セットアップ Tips](#テスト環境セットアップ-tips)
- [Kiro CLI への導入手順](#kiro-cli-への導入手順)
- [test-template.ts コピペ用雛形](#test-templatets-コピペ用雛形)
- [ユースケース](#ユースケース)
- [バージョン履歴](#バージョン履歴)
- [ライセンスと著者](#ライセンスと著者)
- [関連リンク](#関連リンク)

---

**位置付け**: cdk-skills は **Kiro CLI のコア機能ではありません**。AWS DevTools Hero（後藤さん）が公開する **コミュニティ OSS（MIT）** ですが、Kiro CLI v1.26.0+ の **[Skills 自動読み込み機能](../01_features/07_Skills.md)** で利用可能なため、本サイトでは「Kiro CLI で CDK 開発を実践する際の選択肢として有力なもの」として独立フォルダにまとめます。

**出典（一次情報、15 ソース）**:

公式リポジトリ・成果物（11 ソース）:
- [GitHub: go-to-k/cdk-skills](https://github.com/go-to-k/cdk-skills) — リポジトリ本体
- [SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) — Skill 本体（94 行）
- [references/snapshot.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/snapshot.md) — スナップショットテスト詳細
- [references/fine-grained.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/fine-grained.md) — Fine-grained 5 つの使い所
- [references/validation.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/validation.md) — バリデーションテスト
- [references/pitfalls.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/pitfalls.md) — 落とし穴
- [references/setup-tips.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/setup-tips.md) — 環境セットアップ Tips（v0.2.0 追加）
- [examples/test-template.ts](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/examples/test-template.ts) — コピペ用雛形
- [CHANGELOG.md](https://github.com/go-to-k/cdk-skills/blob/main/CHANGELOG.md) — バージョン履歴
- [plugin.json](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/.claude-plugin/plugin.json) — Skill plugin メタデータ
- [marketplace.json](https://github.com/go-to-k/cdk-skills/blob/main/.claude-plugin/marketplace.json) — マーケットプレース定義

著者・元記事（4 ソース）:
- [AWS Heroes 公式: Kenta Goto](https://aws.amazon.com/developer/community/heroes/kenta-goto/) — 著者の AWS 公式肩書
- [元記事: AWS CDK における単体テストの使い所を学ぶ（builders.flash 2024-11）](https://aws.amazon.com/jp/builders-flash/202411/learn-cdk-unit-test/) — Skill の元アイデア
- [元記事: AWS CDK におけるバリデーションの使い分け方を学ぶ（builders.flash 2024-06）](https://aws.amazon.com/jp/builders-flash/202406/cdk-validation/) — バリデーション実装パターンの出典
- [Wantedly: AWS CDK Conference Japan 2025 登壇記事](https://www.wantedly.com/companies/mates-edu/post_articles/991410) — AWS CDK Conference Japan 登壇活動の出典

> **注**: 本サイトの記述は上記一次情報を構造化した要約です。完全な内容は各リンク先を参照してください。著作権は go-to-k 氏に帰属し、本サイトの引用は要約 + 出典明示の範囲で行います。

---

## 概要

### cdk-skills とは

**cdk-skills** は、AWS DevTools Hero の go-to-k 氏（後藤さん）が公開する **AWS CDK 開発を支援する AI コーディングエージェント用 Skills 集** です。

[GitHub README より](https://github.com/go-to-k/cdk-skills)：

> AWS CDK 開発を支援する AI コーディングエージェント用 Skills 集です。SKILL.md フォーマット (YAML frontmatter + 本文) に対応するエージェントで利用できます。

特徴：

- **MIT ライセンス**（無償・改変自由）
- **YAML frontmatter + Markdown 本文** の Skill フォーマットに準拠
- **対応エージェント**: Claude Code（Plugin marketplace） / GitHub CLI `gh skill` v2.90.0+ / Vercel Labs `npx skills`
- **Kiro CLI** v1.26.0+ の Skills 自動読み込み機能とも互換（`~/.kiro/skills/` に配置）

### Kiro CLI との関係

cdk-skills は **Kiro CLI とは独立したプロジェクト** ですが、以下の関係があります：

| 観点 | 内容 |
|----|----|
| **配置場所** | Kiro CLI の Skills 機能（`~/.kiro/skills/` または `.kiro/skills/`） |
| **設定共通性** | `~/.kiro/` は Kiro（IDE）と Kiro CLI で共通 |
| **対応バージョン** | **Kiro CLI v1.26.0**（2026-02-12）以降の Skills 自動読み込み機能で利用 |
| **依存関係** | cdk-skills 側は Kiro CLI に非依存。SKILL.md フォーマットに対応する任意のエージェントで利用可能 |

### Agent Toolkit / AI-DLC との位置付け

本サイトでは Kiro CLI で利用できる 3 つの主要な OSS / 公式ツールを紹介しています。それぞれの役割分担を以下の図にまとめます：

```
+----------------- AI 駆動開発の 3 つの軸 -----------------+
|                                                          |
|  +------ AI-DLC（プロセス方法論）------+                |
|  |  Inception → Construction → Operations               |
|  |  人間の承認・監査証跡・適応型ワークフロー            |
|  |  Steering Files として配置                           |
|  +-------------------------------------+                 |
|                  │                                       |
|                  ▼ Construction フェーズで併用          |
|                                                          |
|  +------ cdk-skills（CDK テスト判断）------+            |
|  |  スナップショット / Fine-grained / バリデーション   |
|  |  CDK 単体テストの「使い分け」を Skill 化            |
|  |  ~/.kiro/skills/ に配置                              |
|  +------------------------------------------+            |
|                  │                                       |
|                  ▼ Code Generation 時に活用             |
|                                                          |
|  +------ Agent Toolkit for AWS（AWS 操作）------+      |
|  |  call_aws / search_documentation / run_script       |
|  |  AWS リソースの安全な操作                            |
|  |  ~/.kiro/settings/mcp.json で設定                    |
|  +-----------------------------------------------+      |
|                                                          |
+----------------------------------------------------------+

役割分担:
  AI-DLC          → 「何を、いつ、どの順で作るか」（プロセス）
  cdk-skills      → 「テストをどう書くか」（テスト判断）
  Agent Toolkit   → 「AWS をどう操作するか」（実行）
```

| 観点 | [Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) | [AI-DLC](../07_aidlc/README.md) | **cdk-skills** |
|----|----|----|----|
| 提供元 | AWS 公式製品 | AWS Labs OSS | AWS Hero 個人 OSS |
| ライセンス | Apache-2.0 | MIT-0 | **MIT** |
| 対象 | AWS 操作（300+ サービス） | 開発プロセス全体 | **CDK 単体テスト判断** |
| 規模 | エンタープライズ | フルスタック方法論 | 特化型 Skill 1 個 |
| Kiro CLI 結合度 | 高（MCP 統合） | 低（Steering Files） | 低（Skills として独立配置） |

> **注**: 上図の「併用パターン」は 3 OSS の補完関係から導出される推論であり、公式に明示された組み合わせではありません。

### なぜ CDK 開発で価値があるか

AI コーディングエージェントは CDK コードを生成する際に「**全リソースに細かくテストを書く**」傾向がありますが、これは以下の問題を引き起こします：

| 問題 | 詳細 |
|----|----|
| **二重定義の煩わしさ** | CDK は宣言的に書く言語のため、リソース定義とテストがほぼ同じコードになる |
| **メンテナンスコスト増** | リソースを変更するたびにテストも書き換える必要がある |
| **読み手の認知負荷** | 「何のためのテストか」が見えづらくなる |

cdk-skills の `aws-cdk-unit-testing` Skill は、これらの問題を解決するために **「コードの性質に応じて適切なテストを選ぶ」判断フロー** を Skill 化しています。AI エージェントは Skill の判断基準に従って、必要なテストのみを書くようになります。

### 収録 Skill 一覧

cdk-skills リポジトリは複数の Skill を収録できる構造になっており、現在は以下の 1 個の Skill と 1 個の Bundle plugin を収録しています：

| Skill 名 | 種別 | 説明 |
|----|----|----|
| **aws-cdk-unit-testing** | Skill | AWS CDK 単体テストの 3 種類（スナップショット / Fine-grained / バリデーション）の使い分けを判断フロー Skill 化 |
| **aws-cdk-pack** | Bundle plugin | cdk-skills の全 Skill を一括 install する dependencies plugin（**Claude Code Plugin marketplace 専用**） |

> **Kiro CLI ユーザー向け補足**: `aws-cdk-pack` は Claude Code Plugin marketplace の依存関係解決機能を使う Bundle plugin です。Kiro CLI には Plugin marketplace 機能がないため、Kiro CLI ユーザーは個別に `aws-cdk-unit-testing` Skill のみを `gh skill` / `npx skills` / 手動配置で導入します。

リポジトリ名は **cdk-skills**（複数形）であり、将来的に Skill が追加される可能性があります（CHANGELOG にて新規 Skill 追加を確認次第、本サイトでも追記します）。

### 主な特徴

| 特徴 | 内容 |
|------|------|
| 🧠 判断フロー Skill 化 | スナップショット / Fine-grained / バリデーションの 3 種類の使い分け |
| 🚫 アンチパターン明示 | 宣言的定義への過剰テスト・自動生成リソース個数の認知負荷など 3 つを明示 |
| 📦 オススメの最小構成 | スナップショット 1 本から始めるオンボーディング戦略 |
| ⚡ パフォーマンス Tips | NodejsFunction バンドルスキップで CDK テスト高速化（v0.2.0+） |
| 🔧 機能フラグ統一 | `cdk.json` の context をテストにも注入して実環境と乖離を防ぐ |
| 👤 著者の信頼性 | 後藤 健太（**AWS DevTools Hero / AWS CDK Top Contributor & Trusted Reviewer / Open Construct Foundation メンテナ**） |
| 🆓 MIT ライセンス | 無償・改変自由 |

---

## aws-cdk-unit-testing Skill — 全体像

### 前提となる思想

[SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) より：

> AWS CDK における単体テストは「全てのリソースに細かく書く」のではなく、**コードの性質に応じて適切なテストを選ぶ**ことが重要。

この思想の核となる 4 つの観点：

| 観点 | 説明 |
|----|----|
| **CDK は宣言的に書くのが基本** | 「○○ というリソースを作成する」という宣言 |
| **二重定義の回避** | 宣言的な定義を Fine-grained で重複検証すると、リソース定義側とほぼ同じコードがテストに出来上がる |
| **手続き的処理は要保証** | ループ・条件分岐・override 等は「実際に何が生成されるか自明でない」ためテストで保証する |
| **意思表示としての Fine-grained** | 要件上「絶対にこうあってほしい」設計意図を明文化する用途で書く |

### 3 種類のテスト早見表

| テスト種別 | 目的 | 必須度 |
|----|----|----|
| **スナップショット** | 合成された CloudFormation テンプレートの差分検出 | ★★★ ほぼ必須（開発初期を除く） |
| **Fine-grained assertions** | テンプレートの一部に対する細かい assertions | ★★☆ 選別して書く |
| **バリデーション** | props のバリデーション処理の挙動検証 | ★★☆ 実装時のみ必須 |

### 3 種類のテストの位置付け図

3 種類のテストは「**広く全体を見るか、深く特定を見るか**」という軸で位置付けられます：

```
+------------------------ Stack 全体 ------------------------+
|                                                            |
|  スナップショット（Stack 全体の合成結果を 1 枚で）        |
|  ★ 網羅性が最大、差分検出に強力                          |
|                                                            |
|  +---------- 個別リソース・プロパティ ----------+         |
|  |                                                |         |
|  |  Fine-grained assertions                       |         |
|  |  ★ 手続き的処理・props 経由の値などに絞って   |         |
|  |                                                |         |
|  |  +-------- props バリデーション --------+    |         |
|  |  |                                        |    |         |
|  |  |  バリデーションテスト                  |    |         |
|  |  |  ★ 実装側のバリデーションごとに      |    |         |
|  |  +----------------------------------------+    |         |
|  |                                                |         |
|  +------------------------------------------------+         |
|                                                            |
+------------------------------------------------------------+

  ＜広く全体＞ ←──────────────────────→ ＜深く特定＞
```

### 判断フロー（コードを見たらまずこれ）

CDK コードを見たときに、どのテストを書くべきか判断するフローです。SKILL.md 原文より引用：

```
CDK コードを見る
 │
 ├─ Stack / Construct がある?
 │  └─ Yes → スナップショットテストを書く（原則必須）
 │
 ├─ 手続き的な処理がある?
 │  ├─ for / map でリソース生成 → Fine-grained (ループ)
 │  ├─ if 分岐でリソース/プロパティ → Fine-grained (条件分岐, Match.absent)
 │  ├─ addPropertyOverride → Fine-grained (override)
 │  └─ addDependency → Fine-grained (依存関係)
 │
 ├─ props 経由で値を流している?
 │  └─ Yes → Fine-grained (値の流入確認、props そのものを参照)
 │
 ├─ 特に保証したい「意思表示」レベルの定義がある?
 │  └─ Yes → Fine-grained (Match.anyValue で値変動に強くする選択肢も)
 │
 ├─ props に対してバリデーション処理を実装している?
 │  └─ Yes → バリデーションテスト（各バリデーションごとに 1 テスト）
 │
 └─ 上記いずれでもない「宣言的な定義」のみ?
    └─ Fine-grained を**書かない**選択肢を強く検討（スナップショットで十分）
```

> **出典**: [SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) より引用

加えて、テスト環境のセットアップで考慮すべきポイント：

- `cdk.json` の `context` に **プロジェクト固有の機能フラグ** を設定している? → `App` の props に context を注入（[テスト環境セットアップ Tips](#テスト環境セットアップ-tips) 参照）
- `NodejsFunction`（esbuild バンドル）を多用していて **テストが遅い**? → `BUNDLING_STACKS: []` でスキップ（同上）

### 使い所マトリクス

コードパターンと書くべきテストの対応表です：

| コードパターン | 書くべきテスト | 詳細 |
|----|----|----|
| Stack / Construct 全体 | スナップショット | [スナップショットテスト](#スナップショットテスト) 参照 |
| `for` / `map` でリソース生成 | Fine-grained（ループ） | [Fine-grained assertions テスト](#fine-grained-assertions-テスト) 参照 |
| `if (props.xxx)` 分岐 | Fine-grained（条件分岐）+ `Match.absent` | 同上 |
| `addPropertyOverride` | Fine-grained（override 確認） | 同上 |
| `addDependency` | Fine-grained（DependsOn 確認） | 同上 |
| props → リソースプロパティ | Fine-grained（値の流入確認） | 同上 |
| 要件上必ず保証したい定義 | Fine-grained（意思表示） | 同上 |
| props バリデーション実装 | バリデーション | [バリデーションテスト](#バリデーションテスト) 参照 |
| 宣言的なリソース定義のみ | Fine-grained は **書かない** | [落とし穴](#落とし穴pitfalls-詳細) 参照 |

### アンチパターン 3 つ（概要）

> **注**: ここではアンチパターンの **概要** を提示します。詳細な解説と対処パターンは [§ 落とし穴（pitfalls 詳細）](#落とし穴pitfalls-詳細) で扱います。

[SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) で警告されている 3 つのアンチパターン：

| # | アンチパターン | 何が問題か |
|---|----|----|
| 1 | **宣言的な定義に対する Fine-grained テストの量産** | リソース定義とほぼ同じコードがテストに出来上がる。スナップショットで代替する |
| 2 | **意味の不透明な大きな個数を `resourceCountIs` で指定する** | L2 Construct の自動生成リソースが含まれた場合、内訳がわからず認知負荷を招く（ただし `0` / `1` で確認する用途は OK） |
| 3 | **全 Construct に網羅的に Construct 単位のテストを書く** | Stack のテストと重複しメンテが大変。**再利用性を担保したい Construct のみ** に絞る |

### オススメの最小構成

[SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) より：

> 導入の負荷を抑えたい場合、**まずスナップショットテストから**。合成テンプレートの差分検出だけで CDK バージョンアップ時のリグレッション検知に強力に効く。

オンボーディング戦略：

```
[Phase 1] スナップショット 1 本のみ
   ↓ CDK プロジェクトに対してリグレッション検知の基盤ができる
   ↓
[Phase 2] 手続き的処理の Fine-grained を順次追加
   ↓ ループ・条件分岐・override から優先的に
   ↓
[Phase 3] バリデーション実装時に都度テストを追加
   ↓ バリデーションごとに 1 テストケース
   ↓
[Phase 4] 「意思表示」テストの追加（任意）
   通常は Phase 1-3 で十分
```

---


## スナップショットテスト

出典: [references/snapshot.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/snapshot.md)（104 行）

### 概要

CDK コードから合成される CloudFormation テンプレートを出力し、以前のテスト実行時に生成したテンプレートと比較して **差分を検出** するテスト。

### 基本形

テストファイルは `cdk init` で生成される `test/` ディレクトリ配下に `my-stack.test.ts` として配置するのが一般的：

```typescript
import { App } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { MyStack } from '../lib/my-stack';

describe('MyStack Tests', () => {
  test('Snapshot Tests', () => {
    const app = new App();
    const stack = new MyStack(app, 'MyStack');
    const template = Template.fromStack(stack);
    expect(template.toJSON()).toMatchSnapshot();
  });
});
```

### 運用フロー

```
[1] npm run test                    [2] 差分発生時の判断
    │                                    │
    ▼                                    ▼
  初回実行                           意図した変更?
    │                            ┌──────┴──────┐
    ▼                          Yes             No
  test/__snapshots__/            ▼              ▼
  *.test.ts.snap が作成    --updateSnapshot  コード修正
    │                          で更新          で対処
    ▼
  2 回目以降は前回と比較
    │
    └─ 差分があれば失敗
```

具体的なコマンド：

| 用途 | コマンド |
|----|----|
| テスト実行（差分検出） | `npm run test` |
| スナップショット更新 | `npx jest --updateSnapshot` |

### TIPS: アセット差分を無視する

Lambda コードや Docker イメージなどのアセットは、CloudFormation テンプレートに **コンテンツハッシュ（SHA-256 / 64 桁 hex）** として埋め込まれます：

| アセット種別 | 出現箇所 |
|----|----|
| Lambda アセット | `S3Key: "abc123...def.zip"` |
| Docker イメージアセット | ECR URI のタグ `...:abc123def...` |

「アセット内容の差分は別レビューフローで管理しているので、スナップショットではテンプレート構造の差分だけに集中したい」というニーズがある場合、Jest のスナップショットシリアライザーで 64 桁 hex 部分をマスクできます。

#### 方法 A: `expect.addSnapshotSerializer` を呼ぶ

```typescript
expect.addSnapshotSerializer({
  test: (val) => typeof val === 'string' && /([A-Fa-f0-9]{64})/.test(val),
  serialize: (val) => `"${val.replace(/([A-Fa-f0-9]{64})/g, '[HASH REMOVED]')}"`,
});
```

#### 方法 B: `jest.config` の `snapshotSerializers` でモジュールとして指定

```typescript
// test/serializers/asset-hash.ts
// 注: TS でも `module.exports = {...}` を使う（ts-jest 互換性のため）
module.exports = {
  test: (val: unknown) => typeof val === 'string' && /([A-Fa-f0-9]{64})/.test(val),
  serialize: (val: string) => `"${val.replace(/([A-Fa-f0-9]{64})/g, '[HASH REMOVED]')}"`,
};
```

```javascript
// jest.config.js
module.exports = {
  snapshotSerializers: ['<rootDir>/test/serializers/asset-hash.ts'],
};
```

> ⚠️ **注意**: アセット内容の変更もスナップショット上は差分として現れなくなります。これは「使い所 §3（PR レビュー時の差分可視化）」と相反するため、**推奨ではなく選択肢のひとつ** として扱います。チームの運用方針（アセット差分をどこで担保するか）を踏まえて採用を判断してください。

### 使い所 3 つ

| # | 使い所 | 効果 |
|---|----|----|
| 1 | **AWS CDK のバージョンアップデート** | CDK ライブラリ更新時に生成テンプレートが変わってもグリーンならデプロイ済みリソースへの影響なしを保証 |
| 2 | **CDK コードのリファクタリング** | リファクタ前後でテンプレートが変わらないことを確認、回帰テストとして機能 |
| 3 | **PR レビュー時の差分可視化** | スナップショットファイルを Git にコミットしておくと、PR レビュー時に CFn テンプレート粒度の差分が可視化される |

### 判断指針

- 開発初期（構成が固まっていない時期）を除けば **ほぼ必須**
- まず最初に導入すべきテスト。これだけでも CDK のリグレッション検知に強力に効く

---

## Fine-grained assertions テスト

出典: [references/fine-grained.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/fine-grained.md)（262 行、最大ボリューム）

### 概要

生成された CloudFormation テンプレートの **一部を取り出して** チェックを行うテスト。「どんなリソースが生成されるか」「どのプロパティに何が設定されているか」を細かい粒度で検証できます。

### 基本形

```typescript
import { App, assertions } from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { MyStack } from '../lib/my-stack';

const getTemplate = (): assertions.Template => {
  const app = new App();
  const stack = new MyStack(app, 'MyStack');
  return Template.fromStack(stack);
};

describe('Fine-grained assertions tests', () => {
  test('Lambda has nodejs20.x', () => {
    const template = getTemplate();
    template.hasResourceProperties('AWS::Lambda::Function', {
      Handler: 'handler',
      Runtime: 'nodejs20.x',
    });
  });
});
```

### 重要な思想

CDK は **宣言的に書く** のが基本。「`new Bucket(this, 'Bucket')`」と書けば Bucket が作られるのは自明。

自明な宣言的定義に対して `hasResourceProperties` を書くと、**リソース定義側とほぼ同じコード** がテストに出来上がり、二重定義の煩わしさを生みます。

そのため Fine-grained テストは「**自明でない部分**」に絞って書きます。

### 書くべき 5 つの使い所

#### 1. ループ処理

ループ処理によるリソース生成は **手続き的** になり、何が生成されるか自明でないため、ループの正しさを保証するテストを書きます：

```typescript
// CDK コード側
export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);
    const appNames = new Set(props.appNames); // 重複排除
    for (const appName of appNames) {
      new Topic(this, `${appName}Topic`, {
        displayName: `${appName}Topic`,
      });
    }
  }
}
```

```typescript
// テスト側
test('SNS Topics are created', () => {
  const appNames = ['App1', 'App1', 'App2'];
  const expectedNumberOfTopics = 2; // 重複排除されるので 2
  const app = new App();
  const stack = new MyStack(app, 'MyStack', { appNames });
  const template = Template.fromStack(stack);
  template.resourcePropertiesCountIs(
    'AWS::SNS::Topic',
    { DisplayName: Match.stringLikeRegexp('Topic') },
    expectedNumberOfTopics,
  );
});
```

**ポイント**:
- `resourcePropertiesCountIs` で「特定プロパティを持つリソースの個数」を確認
- 単純な `resourceCountIs` だと自動生成リソースに引っかかる可能性があるため、プロパティで絞り込むと安全（[落とし穴](#落とし穴pitfalls-詳細) 参照）

#### 2. 条件分岐

`if` による生成有無やプロパティ指定有無の分岐は、両分岐を確認します。

##### (a) リソース自体を分岐する場合

```typescript
// CDK コード
if (props.isProd) {
  new CfnWebACL(this, 'WebAcl', { /* ... */ });
}

// テスト
test('Web ACL is created in prod', () => {
  const stack = new MyStack(app, 'MyStack', { isProd: true });
  const template = Template.fromStack(stack);
  template.resourceCountIs('AWS::WAFv2::WebACL', 1);
});
```

##### (b) プロパティの指定を分岐する場合 — `Match.absent`

「指定されていないこと」を確認する場合は `Match.absent()` を使います：

```typescript
// CDK コード
new Distribution(this, 'Distribution', {
  webAclId: props.isProd ? webAclId : undefined,
});

// テスト
test('Web ACL is not associated in dev', () => {
  const stack = new MyStack(app, 'MyStack', { isProd: false });
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::CloudFront::Distribution', {
    DistributionConfig: {
      WebACLId: Match.absent(),
    },
  });
});
```

#### 3. プロパティの override（エスケープハッチ）

`addPropertyOverride` 等で L1 にキャストして上書きする場合、**Construct の型補完が効かず** 手書きになり、特に階層構造のプロパティでミスしやすいため、意図通り反映されているかを確認します：

```typescript
// CDK コード
const bucket = new Bucket(this, 'Bucket');
const cfnSrcBucket = bucket.node.defaultChild as CfnBucket;
cfnSrcBucket.addPropertyOverride(
  'NotificationConfiguration.EventBridgeConfiguration.EventBridgeEnabled',
  true,
);

// テスト
test('EventBridge is enabled', () => {
  const template = getTemplate();
  template.hasResourceProperties('AWS::S3::Bucket', {
    NotificationConfiguration: {
      EventBridgeConfiguration: { EventBridgeEnabled: true },
    },
  });
});
```

#### 4. 特に保証したい定義（意思表示）

宣言的な定義であっても、要件上「絶対にこのプロパティはこうあってほしい」という設計意図がある場合、**「意思表示」としてテストを書きます**。後の開発者が変更してテストが落ちることで、元の設計意図が伝搬します。

```typescript
// CDK コード
new Bucket(this, 'Bucket', {
  lifecycleRules: [{ expiration: cdk.Duration.days(100) }],
});

// 具体値も保証する場合
test('Expiration for lifecycle must be specified', () => {
  const template = getTemplate();
  template.hasResourceProperties('AWS::S3::Bucket', {
    LifecycleConfiguration: {
      Rules: [{ ExpirationInDays: 100, Status: 'Enabled' }],
    },
  });
});
```

**メンテコストを下げたい場合は `Match.anyValue`** — 「指定されていること」だけを確認：

```typescript
template.hasResourceProperties('AWS::S3::Bucket', {
  LifecycleConfiguration: {
    Rules: [{ ExpirationInDays: Match.anyValue(), Status: 'Enabled' }],
  },
});
```

##### 依存関係（`addDependency`）も同様

```typescript
// CDK コード
hostedZone.node.addDependency(resourcePolicy);

// テスト（hasResource を使う：DependsOn はリソースのトップレベル属性）
test('HostedZone depends on QueryLogResourcePolicy', () => {
  const template = getTemplate();
  template.hasResource('AWS::Route53::HostedZone', {
    DependsOn: [Match.stringLikeRegexp('QueryLogResourcePolicy')],
  });
});
```

#### 5. props を使った値の指定

props 経由で値を流す場合、**渡し忘れ** を検知するためにテストを書きます：

##### シンプルなパターン

```typescript
test('messageRetentionPeriodInDays from props', () => {
  const stack = new MyStack(app, 'MyStack', { messageRetentionPeriodInDays: 10 });
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::SNS::Topic', {
    ArchivePolicy: { MessageRetentionPeriod: 10 },
  });
});
```

##### 実 props をそのまま使うパターン（推奨）

実際にデプロイされる構成をテストできる + 具体値の二重管理を避けられます：

```typescript
import { myStackProps } from '../lib/config';

test('messageRetentionPeriodInDays from props', () => {
  const stack = new MyStack(app, 'MyStack', myStackProps); // 実 props
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::SNS::Topic', {
    ArchivePolicy: { MessageRetentionPeriod: myStackProps.messageRetentionPeriod },
  });
});
```

### `Match.*` の使い分け早見表

| Matcher | 用途 |
|----|----|
| `Match.absent()` | プロパティが **指定されていない** ことを確認 |
| `Match.anyValue()` | プロパティが **指定されている** ことだけ確認（値は問わない） |
| `Match.stringLikeRegexp('xxx')` | 値が正規表現にマッチすることを確認（論理 ID の部分一致など） |
| (リテラル) | 値の完全一致 |

### 使う API 早見表

| メソッド | 用途 |
|----|----|
| `template.hasResourceProperties(type, props)` | 指定 type のリソースに、指定 props を含むものが **少なくとも 1 つ** ある |
| `template.hasResource(type, body)` | プロパティだけでなくトップレベル属性（`DependsOn` 等）も含めて確認 |
| `template.resourceCountIs(type, n)` | 指定 type のリソース個数 |
| `template.resourcePropertiesCountIs(type, props, n)` | 指定 props を持つリソース個数（自動生成リソース対策に有用） |

---

## バリデーションテスト

出典: [references/validation.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/validation.md)（70 行）

### 概要

Stack や Construct の props に対する **バリデーション処理が正しく動作している** ことを確認するテスト。許容しない入力値が渡された際にエラーが発生することを保証します。

### 前提: CDK でのバリデーション実装

props のプロパティが特定の範囲・形式に収まっているかを `throw` で検証します。CDK 特有の注意点として、props に渡された値が **Token（デプロイ時に解決される値）** の場合があり、その場合は値の比較ができないので `cdk.Token.isUnresolved` でスキップします：

```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket } from 'aws-cdk-lib/aws-s3';

export interface MyStackProps extends cdk.StackProps {
  lifecycleDays: number;
}

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

    // Token でない場合のみ範囲チェック
    if (!cdk.Token.isUnresolved(props.lifecycleDays) && props.lifecycleDays > 400) {
      throw new Error('ライフサイクル日数は400日以下にしてください');
    }

    new Bucket(this, 'Bucket', {
      lifecycleRules: [
        { expiration: cdk.Duration.days(props.lifecycleDays) },
      ],
    });
  }
}
```

### バリデーションテストの書き方

`expect(() => { ... }).toThrowError(...)` で例外発生を確認します：

```typescript
import { App } from 'aws-cdk-lib';
import { MyStack } from '../lib/my-stack';

describe('Validation tests', () => {
  test('lifecycle days must be lower than or equal to 400 days', () => {
    const app = new App();
    expect(() => {
      new MyStack(app, 'MyStack', { lifecycleDays: 500 });
    }).toThrowError('ライフサイクル日数は400日以下にしてください');
  });
});
```

### 判断指針

- **バリデーション処理を実装しているなら必ず書く**。バリデーションは「正しく弾けること」が本体の挙動なので、テストしないと意味がない
- **バリデーションごとに 1 テストケース** を用意するのが基本（範囲下限、範囲上限、不正フォーマット、必須プロパティ欠落、など）
- バリデーションを何も実装していない場合は **不要**

### ありがちな落とし穴

| 落とし穴 | 対処 |
|----|----|
| `toThrowError` のメッセージは部分一致でも OK だが、メッセージ変更時にテストの追従漏れが起きやすい | エラーメッセージを実装定数として切り出し、両方から参照すると安全 |
| Token を考慮していないバリデーション（例: cross-stack reference で渡される値）はデプロイ時に意図せず素通りする | `cdk.Token.isUnresolved` チェックの有無も含めてテストで意識する |

> **参考**: 実装パターンの詳細は元記事 [AWS CDK におけるバリデーションの使い分け方を学ぶ（builders.flash 2024-06）](https://aws.amazon.com/jp/builders-flash/202406/cdk-validation/) を参照してください。

---

## 落とし穴（pitfalls 詳細）

> **§ aws-cdk-unit-testing Skill — 全体像 §アンチパターン 3 つ** の詳細解説です。Skill が警告する 3 つのアンチパターンの **対処パターン** を含めて解説します。

出典: [references/pitfalls.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/pitfalls.md)（94 行）

### 1. 個数チェックと自動生成リソース

#### 前提: 何が問題か

まず前提として、**リソースの有無（`0` / `1`）を確認する用途の `resourceCountIs` は問題なし**。例えば「`isProd` 時のみ WAF が作られる」の検証で `resourceCountIs('AWS::WAFv2::WebACL', 1)` のように使うのは適切です。

問題になるのは、**自動生成リソースを含む大きな数値を opaque に指定する** ケース。

CDK の L2 Construct はベストプラクティスに沿うため、または開発者体験向上のために、**Construct 内部で自動的にリソースを追加生成する** ことがあります（例: Lambda Function を作ると LogGroup や IAM Role が自動生成される）：

```typescript
const template = Template.fromStack(stack);
template.resourceCountIs('AWS::Logs::LogGroup', 5);
```

このような個数チェックは、**自分で 5 個定義したつもりが実際は 6 個生成されていた** といったケースを引き起こしやすく、後から見た時に「6 のうち 5 が自分の定義、1 が自動生成」という内訳が読み取れず **認知負荷が高い** です。

#### 対処パターン (a) 個数チェックを捨てる

自動生成リソースの有無は **スナップショットの更新差分から確認可能**。よほど自動生成も含めた個数を保証したい状況でなければ、（有無 `0/1` ではない）個数チェックを書かない選択肢が一番シンプルです。

#### 対処パターン (b) `resourcePropertiesCountIs` でプロパティ絞り込み

**特定の命名規則・プロパティを持つリソースに絞った個数** を確認します。自動生成リソースは命名規則が違うため除外できます：

```typescript
template.resourcePropertiesCountIs(
  'AWS::Logs::LogGroup',
  {
    LogGroupName: Match.stringLikeRegexp('/aws/lambda/my-app/'),
  },
  5,
);
```

#### 対処パターン (c) どうしても合計個数で書くならコメントを残す

```typescript
// 内訳: 自分で定義した 5 個 + Lambda が自動生成する 1 個 = 6 個
template.resourceCountIs('AWS::Logs::LogGroup', 6);
```

### 2. Construct 単位のテスト

カスタム Construct を作り、それを組み合わせて Stack を定義する場合、**Construct 単体のテスト** を書くことができます：

```typescript
import { Stack } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { MyConstruct } from '../lib/constructs/my-construct';

test('Construct Tests', () => {
  // 空のスタック
  const stack = new Stack();
  // テスト対象 Construct のみ追加
  new MyConstruct(stack, 'MyConstruct', {
    messageRetentionPeriodInDays: 10,
  });
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::SNS::Topic', {
    ArchivePolicy: { MessageRetentionPeriod: 10 },
  });
});
```

#### メリット

- 他の Construct の影響を受けず、責務に閉じたテストになる
- Construct 単体の **信頼性・再利用性** を担保できる
- テストファイルがシンプルになり **理解容易性** が上がる

#### 判断指針

- **全 Construct に網羅的に書くと辛い**。Stack のテストと重複してメンテコストが増える
- 必ず書いておくべきは **実デプロイ構成である Stack のテスト**。Construct テストは補助的
- **再利用性を特に担保したい Construct のみ** に絞って書くのがオススメ
- 再利用しないなら Construct 単位テストは **書かない選択肢** もアリ

### 3. 動機のないテストを書かない

- カバレッジを稼ぐためだけのテスト、宣言的な定義に対するハードコード値の二重定義（アンチパターン #1）、内訳の見えない大きな個数チェック（アンチパターン #2）などは避ける
- テストの本数より、「**なぜこのテストがあるのか**」が説明できることを優先する

### 4. Match.absent / Match.anyValue を取り違えない

- `Match.absent()` — プロパティが **指定されていない**（キー自体がない）
- `Match.anyValue()` — プロパティが **指定されている**（値は問わない）

→ 真逆なので注意。

---

## テスト環境セットアップ Tips

> **v0.2.0（2026-05-19）で追加された機能**。CDK 単体テスト（`Template.fromStack`）で当たりやすい 2 点を扱います。

出典: [references/setup-tips.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/setup-tips.md)（115 行）

扱う 2 つの問題：

| 問題 | 詳細 |
|----|----|
| **機能フラグがテストでは反映されない** | `cdk.json` の context は CDK CLI が読む値で、`Template.fromStack` ではデフォルト値で合成される → 実環境とテストでテンプレート差分が出る |
| **esbuild バンドルが毎テスト実行で走る** | `NodejsFunction` などは synth の一部としてバンドルが実行されるため、`Template.fromStack` を呼ぶ度に走る → テストが遅い |

### 1. 機能フラグを実環境と統一する

#### 何が起きるか

CDK の機能フラグは `cdk.json` の `context` に書く値で、CDK CLI が読み込む値です。**`Template.fromStack` で合成されるテンプレートには反映されません**。

例えば `cdk.json` で `@aws-cdk/aws-iam:minimizePolicies: true` を有効にしていても、テスト側ではこのフラグが無効として合成されるため、**実デプロイされるテンプレートとテストのスナップショットが食い違います**。

#### 対処: cdk.json の context を App に注入

`cdk.json` を読み込んで `App` の props の `context` に渡すヘルパーを用意します：

```typescript
import * as fs from 'fs';
import * as path from 'path';
import { App } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';

const getContext = (): Record<string, unknown> => {
  const cdkJsonPath = path.join(__dirname, '..', 'cdk.json');
  const cdkJson = JSON.parse(fs.readFileSync(cdkJsonPath, 'utf-8'));
  return cdkJson.context ?? {};
};

const getTemplate = (): Template => {
  const app = new App({
    context: {
      ...getContext(),
    },
  });
  const stack = new MyStack(app, 'MyStack');
  return Template.fromStack(stack);
};
```

これで実デプロイ時と同じ機能フラグが効いた状態でテンプレートが合成され、スナップショットの信頼性が向上します。

#### 適用判断

**CDK プロジェクトなら原則常に適用してよい**。副作用がなく（実環境と揃えるだけ）、コストもほぼゼロ。

`cdk init` 直後の時点で `cdk.json` には複数の機能フラグが書き込まれます。一方テストは `cdk.json` を読まないため、**プロジェクト作成直後から実環境とテストでテンプレートが乖離している**（手動でフラグを追加したかどうかは関係ない）。

→「フラグを触ったか」で判定する意味は薄く、特に **スナップショットテストを採用しているなら入れておく** のが安全。

### 2. バンドル処理をスキップしてテストを高速化する

#### 何が起きるか

`NodejsFunction` などは、CDK App の合成中に esbuild で Lambda コードをバンドルします。**単体テスト中もバンドルが走る** ため、関数数が多いとテストが体感で遅くなります。

> ※ `bundling.forceDockerBundling: true` や `Code.fromDockerBuild()` のように **Docker バンドル** を使うケースでは、esbuild ではなく Docker が走ります。後述のスキップ手段は効きません。

#### 対処: BUNDLING_STACKS に空配列を渡す

`context` の `BUNDLING_STACKS` に空配列を指定すると、**全スタックの esbuild バンドルがスキップ** されます：

```typescript
import { App } from 'aws-cdk-lib';
import { BUNDLING_STACKS } from 'aws-cdk-lib/cx-api';
import { Template } from 'aws-cdk-lib/assertions';

const getTemplate = (): Template => {
  const app = new App({
    context: {
      [BUNDLING_STACKS]: [],
    },
  });
  const stack = new MyStack(app, 'MyStack');
  return Template.fromStack(stack);
};
```

#### 適用判断

| 採用すべき条件 | 採用しなくて良いケース |
|----|----|
| `NodejsFunction`（または esbuild バンドル）を **複数使用していて**、テストが遅い | Docker バンドル（`forceDockerBundling: true` / `Code.fromDockerBuild()`）→ 効かない |
| Lambda コード自体のテストは **アプリケーション側のテストで別途行っている**（CDK テストでバンドルの妥当性を担保する必要がない） | イメージアセット（`Code.fromAssetImage()` / `DockerImageFunction` / `DockerImageAsset`）→ そもそも単体テストで Docker build は走らないので不要 |

#### 補足: イメージアセットが単体テストで build されない理由

Lambda コードのバンドルは **CDK App 内** で走りますが、イメージアセットの Docker build は **CDK CLI 側** で走ります。単体テストは CDK CLI を通さず App を直接呼ぶため、Docker build はそもそも実行されません。

### 3. 機能フラグ統一とバンドルスキップを併用する

両方適用したい場合、`context` をマージするだけです：

```typescript
const getTemplate = (): Template => {
  const app = new App({
    context: {
      ...getContext(),
      [BUNDLING_STACKS]: [],
    },
  });
  const stack = new MyStack(app, 'MyStack');
  return Template.fromStack(stack);
};
```

---


## Kiro CLI への導入手順

### 前提条件

- **Kiro CLI**: v1.26.0（2026-02-12）以降の **Skills 自動読み込み機能** が必要（[07. Skills](../01_features/07_Skills.md) 参照）
- **作業ディレクトリ**: `~/.kiro/skills/`（グローバル配置）または `<project-root>/.kiro/skills/`（プロジェクト固有配置）

### 配置先ディレクトリ

Kiro CLI Skills 機能（[07_Skills.md](../01_features/07_Skills.md)）の仕様（Glob パターン `**/SKILL.md` で自動検出）に基づき、以下のいずれかの構造で配置します：

```
ユーザーグローバル配置（推奨、全プロジェクトで利用可能）:

  ~/.kiro/                          # ユーザー全体の Kiro 設定
  └── skills/                       # Kiro CLI v1.26.0+ の自動読み込み対象
      └── aws-cdk-unit-testing/     # ← Skill ディレクトリ
          ├── SKILL.md              # ★ エントリポイント（YAML frontmatter 必須）
          ├── references/           # SKILL.md からのリンク先（オンデマンドロード）
          │   ├── snapshot.md
          │   ├── fine-grained.md
          │   ├── validation.md
          │   ├── pitfalls.md
          │   └── setup-tips.md
          └── examples/             # コード雛形（参照用）
              └── test-template.ts


プロジェクト固有配置（特定プロジェクトのみで利用）:

  <project-root>/.kiro/             # プロジェクトの Kiro 設定
  └── skills/
      └── aws-cdk-unit-testing/
          └── ...（同上）

検出ルール（07_Skills.md より）:
  ・Glob パターン: **/SKILL.md
  ・SKILL.md がエントリポイント
  ・references/ / examples/ は SKILL.md からの内部リンクで参照
```

> **注**: `~/.kiro/` は Kiro（IDE）と Kiro CLI で共通です。Kiro IDE を併用する場合も同じ Skill が利用できます。

### インストール方法 3 種類

#### 方法 1: gh skill（GitHub CLI v2.90.0+ 推奨）

[GitHub CLI v2.90.0 から](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) `gh skill` サブコマンドで各エージェントの Skills ディレクトリに直接 install できます：

```bash
gh skill install go-to-k/cdk-skills aws-cdk-unit-testing
```

> **注**: Kiro CLI への配置先を `gh skill` がどう解釈するかは、実装時に検証してください（cdk-skills README は Claude Code を主な配置先として記載）。

#### 方法 2: npx skills（Node.js 環境）

[Vercel Labs の `npx skills`](https://github.com/vercel-labs/agent-skills) 経由でも install できます：

```bash
# 個別の Skill を指定して install
npx skills add go-to-k/cdk-skills --skill aws-cdk-unit-testing

# 全 Skill を install
npx skills add go-to-k/cdk-skills
```

> **注**: 同様に Kiro CLI への配置先は実装時に検証してください。

#### 方法 3: 手動配置（公式仕様準拠、最も確実）

Kiro CLI の Skills 機能（[07_Skills.md](../01_features/07_Skills.md)）の仕様（`**/SKILL.md` を自動検出）に基づく手順です。`references/` と `examples/` は SKILL.md から内部リンクで参照されるため、ディレクトリごとコピーします：

```bash
# 1. リポジトリを clone
git clone https://github.com/go-to-k/cdk-skills.git

# 2. Kiro CLI の Skills ディレクトリに配置（グローバル配置）
mkdir -p ~/.kiro/skills/aws-cdk-unit-testing
cp -R cdk-skills/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/* \
  ~/.kiro/skills/aws-cdk-unit-testing/

# 3. 配置確認
ls ~/.kiro/skills/aws-cdk-unit-testing/
# 期待される出力: SKILL.md  examples/  references/
```

### 動作確認

Kiro CLI を起動し、Skill が認識されているかを確認します：

```text
> kiro-cli
> /context show
# 期待される出力（実装時検証）:
# Skill が表示される、または起動時にメタデータ（name, description）が読み込まれる
```

> **重要**: 上記の動作は **実装時に検証** が必要です。本サイトでは Kiro CLI Skills 仕様（YAML frontmatter 必須・Glob `**/SKILL.md`）に基づく合理的な手順を提示していますが、`references/` / `examples/` のオンデマンドロード挙動、および `gh skill` / `npx skills` の Kiro CLI への配置先解釈は未検証です。

---

## test-template.ts コピペ用雛形

[examples/test-template.ts](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/examples/test-template.ts)（182 行）は、3 種類のテストすべてを 1 ファイルに収めたサンプルです。

### 使い方

1. このファイルを `test/my-stack.test.ts` にコピー
2. import パスを調整（`../lib/my-stack` 等）
3. 不要なセクションは削除

### 雛形の構造

```typescript
import * as fs from 'fs';
import * as path from 'path';
import { App } from 'aws-cdk-lib';
import { Match, Template } from 'aws-cdk-lib/assertions';
// import { BUNDLING_STACKS } from 'aws-cdk-lib/cx-api'; // バンドルスキップ用
import { MyStack } from '../lib/my-stack';

// =========================================================
// (任意) テスト環境セットアップ ヘルパー
// 詳細は references/setup-tips.md 参照
// =========================================================
const getContext = (): Record<string, unknown> => {
  const cdkJsonPath = path.join(__dirname, '..', 'cdk.json');
  const cdkJson = JSON.parse(fs.readFileSync(cdkJsonPath, 'utf-8'));
  return cdkJson.context ?? {};
};

// =========================================================
// 1. スナップショットテスト (原則必須)
// =========================================================
describe('Snapshot Tests', () => {
  test('matches snapshot', () => {
    const app = new App();
    const stack = new MyStack(app, 'MyStack');
    const template = Template.fromStack(stack);
    expect(template.toJSON()).toMatchSnapshot();
  });
});

// =========================================================
// 2. Fine-grained assertions テスト (使い所を選んで書く)
// =========================================================
describe('Fine-grained assertions tests', () => {
  // (a) ループ処理: 生成個数の確認
  // (b) 条件分岐: リソース生成有無 + Match.absent
  // (c) プロパティ override の確認
  // (d) 特に保証したい定義: 「意思表示」テスト
  // (d') addDependency による依存関係の確認
  // (e-1) props 経由の値の流入確認（具体値）
  // (e-2) 実 props (本番デプロイ用 config) をそのまま使う（推奨）
  // ... 詳細は examples/test-template.ts を参照
});

// =========================================================
// 3. バリデーションテスト (バリデーション実装時のみ)
// =========================================================
describe('Validation tests', () => {
  test('lifecycleDays must be <= 400', () => {
    const app = new App();
    expect(() => {
      new MyStack(app, 'MyStack', { lifecycleDays: 500 });
    }).toThrowError('ライフサイクル日数は400日以下にしてください');
  });
});
```

> **完全版**: 全 7 パターンの Fine-grained assertions テスト例を含む完全な雛形は [examples/test-template.ts](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/examples/test-template.ts) を参照してください。

---

## ユースケース

cdk-skills は以下のシナリオに適しています。

### 12-1. 既存 CDK プロジェクトへのテスト導入（最小構成 → 段階的拡張）

**シナリオ**: テストが書かれていない既存 CDK プロジェクトに段階的にテストを追加

```text
> Using aws-cdk-unit-testing skill, let's add unit tests to this CDK project.
> Start with the minimum viable approach.
```

**典型的な進行**:
1. **Phase 1**: スナップショットテスト 1 本を追加（リグレッション検知の基盤）
2. **Phase 2**: 既存コード内の手続き的処理（ループ・条件分岐・override）に Fine-grained を追加
3. **Phase 3**: バリデーション実装箇所にテストを追加
4. **Phase 4**: 「意思表示」テストの追加（任意）

### 12-2. 新規 CDK プロジェクトのテスト戦略策定

**シナリオ**: 新規プロジェクトで「どこまでテストを書くか」を決める

```text
> Using aws-cdk-unit-testing skill, what tests should I write for this new CDK app?
> [coding agent shows the judgment flow and recommends specific tests]
```

**ポイント**: Skill の判断フローに従い、過剰なテストを書かずに必要最小限から始める

### 12-3. CDK バージョンアップ時のリグレッション検知

**シナリオ**: AWS CDK のバージョンアップで生成テンプレートが変わる可能性を事前に検知

```text
> Using aws-cdk-unit-testing skill, run the snapshot tests after upgrading CDK.
```

**ポイント**: スナップショット差分の見方、`--updateSnapshot` の判断基準を Skill が解説

### 12-4. PR レビュー時の差分可視化

**シナリオ**: PR レビュー時に CFn テンプレート粒度の差分を可視化

**ポイント**: スナップショットファイルを Git にコミットすることで、CDK コード上ではわかりづらい思わぬ変更も拾える（snapshot.md §使い所 3 参照）

### 12-5. AI-DLC との併用（推論・補完関係）

**シナリオ**: [AI-DLC](../07_aidlc/README.md) で開発プロセスを規律化し、Construction フェーズで cdk-skills を活用

> **注**: この併用例は **公式に明示されていない推論** です。両者の補完関係から導出される利用パターンとして提示します。

```
+--------- AI-DLC のフェーズ進行 ---------+
|                                          |
|  Inception                               |
|    ↓ 要件分析・設計                     |
|  Construction                            |
|    ↓ Per-Unit Loop                      |
|    ├─ Functional Design                  |
|    ├─ NFR Requirements / Design          |
|    ├─ Infrastructure Design              |
|    ├─ Code Generation ← ここで cdk-skills が活用される
|    │     ↓ 生成された CDK コードに対して
|    │     cdk-skills の判断フローで適切なテストを生成
|    └─ Build and Test  ← テスト実行
|                                          |
+------------------------------------------+
```

**役割分担**:
- AI-DLC: 「いつ何をすべきか」（プロセス）
- cdk-skills: 「テストをどう書くか」（テスト判断）
- 両者は独立して動作するが、Steering / Skills として併用可能

詳細は [07. AI-DLC](../07_aidlc/README.md) を参照してください。

---

## バージョン履歴

[CHANGELOG.md](https://github.com/go-to-k/cdk-skills/blob/main/CHANGELOG.md) に基づく主要バージョンの履歴です。

| バージョン | リリース日 | 主要変更 |
|----|----|----|
| **v0.1.0** | 2026-05-18 | **初公開**（split into per-skill plugins with cdk-pack bundle） |
| v0.1.1 | 2026-05-18 | Skill description を強化（auto-trigger を効きやすく） |
| v0.1.2 | 2026-05-18 | CI 修正（tag alias creation） |
| v0.1.3 | 2026-05-18 | `cdk-pack` → `aws-cdk-pack` にリネーム（命名一貫性） |
| v0.1.4 | 2026-05-19 | 「書かないべき」→「書かなくて良い」に表現を緩和 |
| v0.1.5 | 2026-05-19 | test-template.ts 改善（real-props pattern 追加） |
| v0.1.6 | 2026-05-19 | アンチパターンと pitfalls の表現精緻化 |
| **v0.2.0** | 2026-05-19 | **setup-tips.md 追加**（feature flag parity & bundling skip） |

**統計（2026-05-24 時点、GitHub）**:
- ⭐ Stars: 9
- 🍴 Forks: 0
- 📝 Releases: 8
- 📜 ライセンス: MIT
- 💻 言語: TypeScript 100%

---

## ライセンスと著者

### MIT ライセンス

cdk-skills は **MIT ライセンス** で公開されています。

| 観点 | MIT |
|----|----|
| 商用利用 | ✅ |
| 改変 | ✅ |
| 配布 | ✅ |
| 著作権表示の保持 | ⚠️ 必要 |
| 特許権の明示的付与 | ❌ なし |

> **比較**: [Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) は **Apache-2.0**、[AI-DLC](../07_aidlc/README.md) は **MIT-0** で、本サイトで紹介する OSS のライセンスはそれぞれ異なります。

### 著者: 後藤 健太（go-to-k、Kenta Goto）

| 公式肩書 | 出典 |
|----|----|
| **AWS DevTools Hero** | [AWS Heroes 公式](https://aws.amazon.com/developer/community/heroes/kenta-goto/) |
| **AWS CDK Top Contributor & Trusted Reviewer** | AWS Heroes 公式 |
| **Open Construct Foundation の Community-Driven CDK Construct Library メンテナ**（2024 launched） | AWS Heroes 公式 |

主なコミュニティ活動：

| 活動 | 詳細 |
|----|----|
| **AWS CDK Conference Japan 登壇** | 2023/2024/2025 で 3 年連続登壇、2 年連続トリ |
| **2025 年の登壇テーマ** | 「AWS CDK の仕組み」（CDK のデプロイメカニズム解説） |
| **CDK コントリビュートワークショップ主催** | JAWS-UG CDK 支部にて 2024/2025 年に開催 |

その他の OSS 活動:
- [cdkd](https://github.com/go-to-k/cdkd): Drop-in CDK CLI for existing CDK apps
- [cls3](https://github.com/go-to-k/cls3): CLI tool to clear S3 buckets
- [delstack](https://github.com/go-to-k/delstack): CLI tool for deleting CFn / CDK stacks
- その他多数（[GitHub プロフィール](https://github.com/go-to-k) 参照）

---

## 関連リンク

### 関連機能（本サイト）

- [07. Skills 機能（Progressive Context Loading）](../01_features/07_Skills.md) — Kiro CLI の Skills 機能、cdk-skills の利用基盤
- [07. AI-DLC（Kiro CLI で実践する選択肢）](../07_aidlc/README.md) — AWS Labs OSS の AI 駆動開発方法論、cdk-skills と併用可能
- [26. Agent Toolkit for AWS](../01_features/26_AgentToolkitForAWS.md) — AWS 公式の MCP Server、AWS 操作を担当

### リファレンス（辞書）

- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/context show` などのスラッシュコマンド

### 公式情報源

#### GitHub リポジトリ
- [go-to-k/cdk-skills](https://github.com/go-to-k/cdk-skills) — リポジトリ本体
- [SKILL.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/SKILL.md) — Skill 本体
- [CHANGELOG.md](https://github.com/go-to-k/cdk-skills/blob/main/CHANGELOG.md) — バージョン履歴

#### references/（Skill の詳細リファレンス）
- [snapshot.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/snapshot.md) — スナップショットテスト
- [fine-grained.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/fine-grained.md) — Fine-grained assertions
- [validation.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/validation.md) — バリデーション
- [pitfalls.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/pitfalls.md) — 落とし穴
- [setup-tips.md](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/references/setup-tips.md) — 環境セットアップ Tips（v0.2.0+）

#### examples/（雛形）
- [test-template.ts](https://github.com/go-to-k/cdk-skills/blob/main/plugins/aws-cdk-unit-testing/skills/aws-cdk-unit-testing/examples/test-template.ts) — コピペ用雛形

#### 著者・元記事
- [AWS Heroes 公式: Kenta Goto](https://aws.amazon.com/developer/community/heroes/kenta-goto/) — 著者の AWS 公式肩書
- [AWS CDK における単体テストの使い所を学ぶ - builders.flash (2024-11)](https://aws.amazon.com/jp/builders-flash/202411/learn-cdk-unit-test/) — Skill の元アイデア
- [AWS CDK におけるバリデーションの使い分け方を学ぶ - builders.flash (2024-06)](https://aws.amazon.com/jp/builders-flash/202406/cdk-validation/) — バリデーション実装パターン
- [AWS CDK Conference Japan 2025 で登壇 & コントリビュートワークショップ開催しました！ - Wantedly](https://www.wantedly.com/companies/mates-edu/post_articles/991410) — AWS CDK Conference Japan 登壇活動

#### Skills エコシステム
- [Plugin Marketplace 機能（Anthropic）](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces) — Claude Code の Plugin marketplace 機能
- [gh skill - GitHub CLI v2.90.0+ で Agent Skills を管理](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) — GitHub CLI 公式の Skills 管理コマンド
- [Vercel Labs: agent-skills](https://github.com/vercel-labs/agent-skills) — `npx skills` の実装

---

**Page updated**: 2026-05-24（本サイト初版）
**cdk-skills 最新版**: v0.2.0（2026-05-19）
**Kiro CLI 必要バージョン**: v1.26.0（2026-02-12）以降の Skills 自動読み込み機能
