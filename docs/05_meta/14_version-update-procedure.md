[ホーム](../README.md) > [Meta](README.md) > バージョンアップ対応手順書

---

# Q CLI バージョンアップ対応手順書

**最終更新**: 2025-10-26  
**対象読者**: ドキュメントメンテナー、コントリビューター  
**前提条件**: Git、ripgrep、jq、curlがインストール済み  
**所要時間**: 約1-2時間（バージョンの変更規模による）

---

## 📋 目次

1. [概要](#概要)
2. [事前準備](#事前準備)
3. [Phase 0: ソースコード分析](#phase-0-ソースコード分析必須最優先)
4. [Phase 1: バージョン履歴更新](#phase-1-バージョン履歴更新必須)
5. [Phase 2: 機能ドキュメント更新](#phase-2-機能ドキュメント更新推奨)
6. [Phase 3: 検証と品質確認](#phase-3-検証と品質確認必須)
7. [最終確認](#最終確認)
8. [作業記録](#作業記録)
9. [トラブルシューティング](#トラブルシューティング)

---

## 概要

### 目的

Q CLIの新バージョンリリース時に、本サイトのドキュメントを正確かつ効率的に更新するための標準手順を提供します。

### 重要な原則

**1. 作業品質が最優先**
- 作業時間は考慮しない
- いきすぎた効率化はしない
- 妥協しない

**2. 正確性の確保**
- 思い込みで書かない
- 推測で書かない
- すべて検証する

**3. 完全性の追求**
- 漏れを許さない
- 中途半端にしない
- 最後まで徹底する

### 過去の教訓

**事例**: todosコマンドをtodoと誤記（v1.18.0対応時）

**原因**:
- リリースノートのみを参照
- ソースコード確認を怠った

**対策**:
- ✅ Phase 0でソースコード確認を必須化
- ✅ コマンド名、設定項目名を直接確認
- ✅ 推測に基づく記述を排除

### 作業フロー

```
Phase 0: ソースコード分析（必須・最優先）
    ↓
Phase 1: バージョン履歴更新（必須）
    ↓
Phase 2: 機能ドキュメント更新（推奨）
    ↓
Phase 3: 検証と品質確認（必須）
    ↓
最終確認・コミット
```

---

## 事前準備

### 必要なツール

| ツール | 用途 | インストール確認 |
|--------|------|----------------|
| Git | ソースコードクローン | `git --version` |
| ripgrep (rg) | ソースコード検索 | `rg --version` |
| jq | JSON解析 | `jq --version` |
| curl | API呼び出し | `curl --version` |
| Q CLI | 最新版確認 | `q --version` |

### 環境設定

**作業ディレクトリ**:
```bash
# プロジェクトルート
cd /path/to/q-cli-docs

# 作業記録ディレクトリ
mkdir -p /home/katoh/work_records/$(date +%Y%m%d)
```

**GitHubアクセストークン**（オプション）:
```bash
# API制限を回避するため推奨
export GITHUB_TOKEN="your_token_here"
```

### 作業前チェックリスト

#### ✅ 必須確認事項

- [ ] **新バージョンのリリース確認**
  - GitHub Releaseページで確認
  - リリース日時を記録
  
- [ ] **リリースノートの確認**
  - 主要な変更点を把握
  - PR番号を記録
  
- [ ] **作業時間の確保**
  - 最低1時間を確保
  - 中断しない環境を準備
  
- [ ] **バックアップの作成**
  - 現在のブランチをバックアップ
  - `git branch backup-$(date +%Y%m%d)`

#### ⚠️ 禁止事項

- [ ] ❌ 出典なしの記述
- [ ] ❌ 未確認のバージョン番号
- [ ] ❌ 推測表現
- [ ] ❌ リリースノートのみに基づく記述

---

## Phase 0: ソースコード分析（必須・最優先）

### 目的

リリースノートだけでは不十分な情報を、ソースコードから直接確認し、誤記を防止します。

### 所要時間

約10-15分

### 作業0-1: ソースコードクローン

#### 手順

```bash
# 作業ディレクトリに移動
cd /tmp

# 新バージョンをクローン（vX.Y.Zを実際のバージョンに置き換え）
git clone --depth 1 --branch vX.Y.Z \
  https://github.com/aws/amazon-q-developer-cli.git \
  q-cli-vX.Y.Z

# ディレクトリに移動
cd q-cli-vX.Y.Z
```

#### 確認事項

```bash
# タグの確認
git describe --tags
# 出力例: vX.Y.Z

# コミットハッシュの記録
git rev-parse HEAD
# 出力例: 1776a67282de04424b3061bf93d79330259e2a67

# コミット日時の確認
git log -1 --format="%ci"
# 出力例: 2025-10-22 17:10:45 -0700

# コミットメッセージの確認
git log -1 --format="%s"
# 出力例: Bump version to X.Y.Z and update feed.json (#XXXX)
```

#### チェックリスト

- [ ] クローン成功
- [ ] タグがvX.Y.Zであることを確認
- [ ] コミットハッシュを記録
- [ ] コミット日時を記録
- [ ] コミットメッセージを記録

#### 記録テンプレート

```markdown
### ソースコード情報

- **バージョン**: vX.Y.Z
- **コミットハッシュ**: `XXXXXXX`
- **コミット日時**: YYYY-MM-DD HH:MM:SS TZ
- **コミットメッセージ**: "メッセージ"
```

---

### 作業0-2: コマンド名の確認

#### 目的

チャット内コマンド（/で始まるコマンド）とqコマンドの正確な綴りを確認します。

#### 重要性

**過去の誤記例**:
- ❌ 誤: `/todo`
- ✅ 正: `/todos`（複数形）

この誤記は、リリースノートのみを参照し、ソースコードを確認しなかったことが原因です。

#### 手順

**ステップ1: チャット内コマンドの確認**

```bash
# コマンド定義ファイルを開く
cat crates/chat-cli/src/cli/chat/cli/mod.rs | head -200

# コマンド一覧を抽出
rg "pub mod" crates/chat-cli/src/cli/chat/cli/mod.rs

# 列挙型を確認
rg "pub enum ChatCommand" -A 50 crates/chat-cli/src/cli/chat/cli/mod.rs
```

**出力例**:
```rust
pub mod quit;
pub mod clear;
pub mod agent;
pub mod context;
pub mod knowledge;
pub mod editor;
pub mod reply;
pub mod compact;
pub mod tools;
pub mod issue;
pub mod logdump;
pub mod changelog;
pub mod prompts;
pub mod hooks;
pub mod usage;
pub mod mcp;
pub mod model;
pub mod experiment;
pub mod subscribe;
pub mod tangent;
pub mod persist;
pub mod checkpoint;
pub mod todos;  // ← 複数形であることを確認
pub mod paste;
```

**ステップ2: コマンド一覧の作成**

以下のテンプレートに従って、確認したコマンドを記録します：

```markdown
### チャット内コマンド一覧

| # | コマンド | 正確な綴り | エイリアス | 説明 | 出典 |
|---|---------|-----------|----------|------|------|
| 1 | quit | `/quit` | `/q`, `/exit` | アプリケーション終了 | mod.rs:L10 |
| 2 | clear | `/clear` | - | 会話履歴クリア | mod.rs:L11 |
| ... | ... | ... | ... | ... | ... |
| 23 | todos | `/todos` | - | To-doリスト管理 | mod.rs:L32 |
| 24 | paste | `/paste` | - | 画像ペースト | mod.rs:L33 |
```

**ステップ3: サブコマンドの確認**

サブコマンドを持つコマンドを特定します：

```bash
# サブコマンド型の確認
rg "Subcommand" crates/chat-cli/src/cli/chat/cli/mod.rs
```

**出力例**:
```rust
Agent(AgentSubcommand),
Context(ContextSubcommand),
Knowledge(KnowledgeSubcommand),
Persist(PersistSubcommand),
Checkpoint(CheckpointSubcommand),
Todos(TodoSubcommand),  // ← サブコマンドを持つ
```

#### チェックリスト

- [ ] 全コマンドの綴りを確認
- [ ] エイリアスを確認
- [ ] サブコマンドを持つコマンドを特定
- [ ] 出典（ファイルパス、行番号）を記録
- [ ] 過去の誤記がないか再確認

#### 記録テンプレート

```markdown
### コマンド確認結果

**確認ファイル**:
- ファイルパス: `crates/chat-cli/src/cli/chat/cli/mod.rs`
- 行番号: 1-200
- コミットハッシュ: `XXXXXXX`

**確認したコマンド数**: XX個

**重要な確認事項**:
- `/todos`（複数形）を確認 ✅
- その他の新規コマンドを確認 ✅
```

---

### 作業0-3: 設定項目名の確認

#### 目的

新規追加または変更された設定項目の正確な名称を確認します。

#### 手順

**ステップ1: 環境変数の確認**

```bash
# 環境変数定義の検索
rg "env::var|std::env" --type rust crates/

# ENV_プレフィックスの検索
rg "ENV_" --type rust crates/

# 環境変数マクロの検索
rg "define_env_vars!" --type rust crates/
```

**ステップ2: Agent設定項目の確認**

```bash
# Agent設定構造体の検索
rg "struct.*AgentConfig" --type rust crates/

# serde属性の確認
rg "#\[serde\(rename" --type rust crates/

# デフォルト値の確認
rg "impl Default for.*Config" --type rust crates/
```

**ステップ3: MCP設定項目の確認**

```bash
# MCP設定構造体の検索
rg "struct.*McpConfig" --type rust crates/

# MCP関連の設定項目
rg "mcp.*config" --type rust -i crates/
```

#### 記録テンプレート

```markdown
### 設定項目確認結果

**環境変数**:
| 変数名 | 用途 | デフォルト値 | 出典 |
|--------|------|------------|------|
| Q_NEW_VAR | 説明 | 値 | file.rs:LXX |

**Agent設定項目**:
| 項目名 | データ型 | 必須 | デフォルト値 | 出典 |
|--------|---------|------|------------|------|
| new_field | string | No | null | file.rs:LXX |

**MCP設定項目**:
| 項目名 | データ型 | 必須 | デフォルト値 | 出典 |
|--------|---------|------|------------|------|
| new_field | object | No | {} | file.rs:LXX |
```

#### チェックリスト

- [ ] 新規環境変数を確認
- [ ] 新規Agent設定項目を確認
- [ ] 新規MCP設定項目を確認
- [ ] データ型を確認
- [ ] デフォルト値を確認
- [ ] 出典を記録

---

### 作業0-4: 実験的機能の確認

#### 目的

新規追加または変更された実験的機能を確認します。

#### 手順

```bash
# 実験的機能マネージャーの確認
cat crates/chat-cli/src/cli/experiment/experiment_manager.rs | head -150

# 実験的機能の列挙型を確認
rg "pub enum ExperimentName" -A 20 crates/chat-cli/src/cli/experiment/

# 機能フラグの検索
rg "experiment" --type rust -i crates/ | grep -i "feature\|flag"
```

#### 記録テンプレート

```markdown
### 実験的機能確認結果

**確認ファイル**:
- ファイルパス: `crates/chat-cli/src/cli/experiment/experiment_manager.rs`
- 行番号: 1-150
- コミットハッシュ: `XXXXXXX`

**実験的機能一覧**:
| # | 機能名 | 列挙型 | 設定キー | 出典 |
|---|--------|--------|---------|------|
| 1 | Knowledge | ExperimentName::Knowledge | EnabledKnowledge | LXX |
| 2 | Thinking | ExperimentName::Thinking | EnabledThinking | LXX |
| ... | ... | ... | ... | ... |
```

#### チェックリスト

- [ ] 全実験的機能を確認
- [ ] 列挙型名を確認
- [ ] 設定キー名を確認
- [ ] 出典を記録

---

### 作業0-5: セキュリティ機能の確認

#### 目的

新規追加または変更されたセキュリティ機能を確認します。

#### 手順

```bash
# セキュリティ関連の検索
rg "security" --type rust -i crates/

# 権限関連の検索
rg "permission" --type rust -i crates/

# deny_by_default の検索
rg "deny_by_default" --type rust crates/

# builtin namespace の検索
rg "@builtin" --type rust crates/
```

#### 記録テンプレート

```markdown
### セキュリティ機能確認結果

**確認した機能**:

#### 1. find -fls 無効化
- **ファイル**: `crates/chat-cli/src/cli/chat/tools/execute/mod.rs`
- **行番号**: 116
- **実装**: `|| arg.contains("-fls")`

#### 2. deny_by_default モード
- **ファイル**: `crates/chat-cli/src/cli/chat/tools/execute/mod.rs`
- **行番号**: 200, 217, 248
- **実装**: `deny_by_default: bool`

#### 3. builtin tool namespace
- **ファイル**: `crates/chat-cli/src/util/tool_permission_checker.rs`
- **行番号**: 1-120
- **定数**: `@builtin`, `@builtin/`
```

#### チェックリスト

- [ ] セキュリティ機能を確認
- [ ] 実装箇所を特定
- [ ] 設定方法を確認
- [ ] 出典を記録

---

### 作業0-6: 分析結果サマリ作成

#### 目的

Phase 0で確認した内容を1つのドキュメントにまとめます。

#### テンプレート

ファイル名: `YYYYMMDDHHmm_vX.Y.Z_source_analysis_summary.md`

```markdown
# Q CLI vX.Y.Z ソースコード分析結果

**分析日時**: YYYY-MM-DD HH:MM JST  
**分析者**: 名前  
**対象バージョン**: vX.Y.Z  
**コミットハッシュ**: `XXXXXXX`

---

## 分析サマリ

### 確認項目

- [x] ソースコードクローン
- [x] コマンド名確認（XX個）
- [x] 設定項目確認（XX個）
- [x] 実験的機能確認（XX個）
- [x] セキュリティ機能確認（XX個）

### 重要な発見

**過去の誤記防止**:
- `/todos`（複数形）を確認 ✅
- その他の重要な確認事項

---

## 詳細結果

### 1. コマンド名

[作業0-2の結果を貼り付け]

### 2. 設定項目

[作業0-3の結果を貼り付け]

### 3. 実験的機能

[作業0-4の結果を貼り付け]

### 4. セキュリティ機能

[作業0-5の結果を貼り付け]

---

## 未確認事項

以下の項目は時間の都合で未確認：
- 項目1
- 項目2

これらはリリースノートベースで記述し、出典を明記します。

---

## 次のステップ

Phase 1（バージョン履歴更新）に進みます。
```

#### チェックリスト

- [ ] 全確認項目を記載
- [ ] 重要な発見を記載
- [ ] 未確認事項を明記
- [ ] 次のステップを記載

---

## Phase 0 完了チェックリスト

### 必須項目

- [ ] ソースコードクローン完了
- [ ] コマンド名確認完了
- [ ] 設定項目確認完了（または未確認を明記）
- [ ] 実験的機能確認完了
- [ ] セキュリティ機能確認完了
- [ ] 分析結果サマリ作成完了

### 品質確認

- [ ] すべての名称がソースコードから確認済み
- [ ] すべての項目に出典が記載されている
- [ ] 推測表現が一切ない
- [ ] 過去の誤記がないか再確認済み

---

最終更新: 2025-10-26

---

## Phase 1: バージョン履歴更新（必須）

### 目的

v1.19.0の情報を正確にバージョン履歴ドキュメントに反映します。

### 所要時間

約5-10分

### 作業1-1: changelog.md更新

#### 対象ファイル

`docs/03_for-community/01_updates/01_changelog.md`

#### 手順

**ステップ1: ファイルを開く**

```bash
# エディタで開く
code docs/03_for-community/01_updates/01_changelog.md
```

**ステップ2: 新バージョンセクションを追加**

最新バージョンのセクションを一番上に追加します。

**テンプレート**:
```markdown
### vX.Y.Z（YYYY-MM-DD）

**主要な変更**:
- 🎉 **機能追加1**: 説明 (#XXXX)
- 🖼️ **機能追加2**: 説明 (#XXXX)
- 🔐 **セキュリティ強化1**: 説明 (#XXXX)
- 🛡️ **セキュリティ強化2**: 説明 (#XXXX)
- 📊 **UX改善1**: 説明 (#XXXX)
- 🔍 **UX改善2**: 説明 (#XXXX)
- 🔄 **動作変更**: 説明 (#XXXX)

**詳細**: [vX.Y.Zリリースノート](https://github.com/aws/amazon-q-developer-cli/releases/tag/vX.Y.Z)
```

**ステップ3: Phase 0の分析結果を反映**

- コマンド名は Phase 0 で確認した正確な綴りを使用
- 設定項目名は Phase 0 で確認した正確な名称を使用
- PR番号はリリースノートから転記

**ステップ4: 絵文字の選択**

| カテゴリ | 絵文字 | 使用例 |
|---------|--------|--------|
| 機能追加 | 🎉 | Knowledge PDF対応 |
| UI/UX | 🖼️ | 画像ペースト対応 |
| セキュリティ | 🔐 🛡️ | OAuth設定、deny_by_default |
| 設定 | 📁 🌐 | file:// URI、HTTP headers |
| 改善 | 📊 🔍 | settings表示、logdump |
| 動作変更 | 🔄 | --resume動作変更 |

#### チェックリスト

- [ ] 新バージョンセクションを追加
- [ ] リリース日が正確
- [ ] 主要変更点を網羅
- [ ] PR番号を記載
- [ ] リリースノートへのリンクを追加
- [ ] Phase 0で確認した名称を使用

---

### 作業1-2: version-history.md更新

#### 対象ファイル

`docs/03_for-community/01_updates/03_version-history-v1.13-latest.md`

#### 手順

**ステップ1: ヘッダー情報更新**

```markdown
**調査日**: YYYY-MM-DD  
**対象バージョン**: v1.13.0 ～ vX.Y.Z  
**リリース期間**: 2025-07-31 ～ YYYY-MM-DD  
**バージョン数**: N個
```

**ステップ2: 概要セクション更新**

主要な変更カテゴリに新バージョンの内容を追加：

```markdown
### 主な変更点

**Agent機能の成熟化**:
- [既存の内容]
- [新バージョンで追加された内容]

**MCP進化**:
- [既存の内容]
- [新バージョンで追加された内容]

**Knowledge機能ベータ改善**:
- [既存の内容]
- [新バージョンで追加された内容]

**セキュリティ強化**:
- [既存の内容]
- [新バージョンで追加された内容]
```

**ステップ3: 新バージョンセクション追加**

詳細なセクションを追加します。

**テンプレート**:
```markdown
## vX.Y.Z (YYYY-MM-DD)

### 主要機能追加

#### 機能名1
- 説明文
- 技術的詳細
- PR番号: #XXXX

#### 機能名2
- 説明文
- 技術的詳細
- PR番号: #XXXX

### セキュリティ強化

#### セキュリティ機能1
- 説明文
- 技術的詳細
- PR番号: #XXXX

### UX改善

#### 改善1
- 説明文
- PR番号: #XXXX

### 動作変更

#### 変更1
- 説明文
- PR番号: #XXXX

### バグフィックス

- 修正1 (#XXXX)
- 修正2 (#XXXX)
- その他の軽微な修正

### その他の改善

- 改善1 (#XXXX)
- 改善2 (#XXXX)

### 統計

- PR数: XX件
- 新規コントリビューター: X名
  - @username1
  - @username2

### リンク

- [GitHub Release](https://github.com/aws/amazon-q-developer-cli/releases/tag/vX.Y.Z)
- [Full Changelog](https://github.com/aws/amazon-q-developer-cli/compare/vX.Y.Z-1...vX.Y.Z)
```

#### チェックリスト

- [ ] ヘッダー情報更新完了
- [ ] 概要セクション更新完了
- [ ] 新バージョンセクション追加完了
- [ ] 全PR番号を記載
- [ ] 全コントリビューター名を記載
- [ ] リンクを追加
- [ ] Phase 0で確認した名称を使用

---

## Phase 1 完了チェックリスト

### 必須項目

- [ ] changelog.md更新完了
- [ ] version-history.md更新完了
- [ ] 全PR番号記載済み
- [ ] 全リンク追加済み

### 品質確認

- [ ] Phase 0で確認した名称を使用
- [ ] リリースノートの内容を正確に反映
- [ ] 推測表現なし
- [ ] 出典記載済み

---

## Phase 2: 機能ドキュメント更新（推奨）

### 目的

新機能や変更された機能について、該当する機能ドキュメントを更新します。

### 所要時間

約30-60分（更新対象ファイル数による）

### 更新判断基準

| 変更内容 | 更新対象ドキュメント |
|---------|-------------------|
| 新機能追加 | `docs/01_for-users/02_features/*.md` |
| 設定項目追加 | `docs/01_for-users/03_configuration/*.md` |
| セキュリティ変更 | `docs/01_for-users/09_security/*.md` |
| コマンド追加 | `docs/01_for-users/07_reference/*.md` |
| 実験的機能追加 | `docs/01_for-users/02_features/07_experimental.md` |

### 更新テンプレート

```markdown
### 機能名（vX.Y.Z以降）

説明文

**使用方法**:
```json
{
  "設定例": "値"
}
```

**メリット**:
- メリット1
- メリット2

**注意事項**:
- 注意点1
- 注意点2

**出典**: PR #XXXX
```

### 更新例

#### 例1: experimental.md更新（Knowledge PDF対応）

**ファイル**: `docs/01_for-users/02_features/07_experimental.md`

**追加内容**:
```markdown
#### 対応ファイル形式

- テキストファイル（.txt、.md等）
- ソースコードファイル
- **PDF（v1.19.0以降）** ← NEW

**出典**: PR #3151
```

#### 例2: agent-configuration.md更新（file:// URI対応）

**ファイル**: `docs/01_for-users/03_configuration/03_agent-configuration.md`

**追加内容**:
```markdown
### file:// URI対応（v1.19.0以降）

Agent promptsで外部ファイルを参照できます：

```json
{
  "prompt": "file:///path/to/prompt.txt"
}
```

**メリット**:
- プロンプトの外部管理
- 複数Agentでの共有
- バージョン管理の容易化

**注意事項**:
- 絶対パスを使用
- ファイルが存在することを確認
- 相対パスはAgent設定ファイルからの相対

**出典**: PR #3024
```

### チェックリスト

- [ ] 更新対象ファイルを特定
- [ ] 各ファイルに新機能を追記
- [ ] 使用例を記載
- [ ] メリットを記載
- [ ] 注意事項を記載
- [ ] 出典（PR番号）を記載
- [ ] Phase 0で確認した名称を使用

---

## Phase 3: 検証と品質確認（必須）

### 目的

更新内容の正確性と品質を確認します。

### 所要時間

約5-10分

### 検証1: PR番号の存在確認

#### 手順

```bash
# GitHub APIでPR番号を確認
curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/pulls/XXXX" | jq '.number'

# 出力例: XXXX（存在する場合）
# 出力例: null（存在しない場合）
```

#### 自動化スクリプト（オプション）

```bash
#!/bin/bash
# verify_prs.sh

PR_NUMBERS=(3151 3088 3124 3024 3075 2999 3205 3033 3167 3143 3133)

for pr in "${PR_NUMBERS[@]}"; do
  result=$(curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/pulls/$pr" | jq '.number')
  if [ "$result" = "null" ]; then
    echo "❌ PR #$pr: 存在しない"
  else
    echo "✅ PR #$pr: 存在"
  fi
done
```

#### チェックリスト

- [ ] 全PR番号が存在することを確認
- [ ] 存在しないPR番号があれば修正

---

### 検証2: コントリビューター名確認

#### 手順

```bash
# リリースノートから新規コントリビューターを確認
curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/releases/tags/vX.Y.Z" | \
  jq -r '.body' | \
  grep "New Contributors"
```

#### チェックリスト

- [ ] リリースノートに記載されている名前を正確に転記
- [ ] @マークを含めて記載

---

### 検証3: リリース日時確認

#### 手順

```bash
# リリース日時を確認
curl -s "https://api.github.com/repos/aws/amazon-q-developer-cli/releases/tags/vX.Y.Z" | \
  jq -r '.published_at'

# 出力例: 2025-10-24T22:51:34Z
```

#### チェックリスト

- [ ] リリース日時が正確
- [ ] ドキュメントに記載した日付が正確

---

### 検証4: リンク切れチェック

#### 手順

```bash
# リリースノートリンクの確認
curl -I "https://github.com/aws/amazon-q-developer-cli/releases/tag/vX.Y.Z"

# Full Changelogリンクの確認
curl -I "https://github.com/aws/amazon-q-developer-cli/compare/vX.Y.Z-1...vX.Y.Z"
```

#### チェックリスト

- [ ] リリースノートリンクが有効（HTTPステータス200）
- [ ] Full Changelogリンクが有効（HTTPステータス200）

---

### 検証5: 表記統一確認

#### チェック項目

| 項目 | 確認内容 |
|------|---------|
| コマンド名 | Phase 0で確認した綴りと一致 |
| 設定項目名 | Phase 0で確認した名称と一致 |
| バージョン番号 | vX.Y.Z形式で統一 |
| 日付フォーマット | YYYY-MM-DD形式で統一 |

#### チェックリスト

- [ ] 全コマンド名が正確
- [ ] 全設定項目名が正確
- [ ] バージョン番号の表記が統一
- [ ] 日付フォーマットが統一

---

### 検証6: 出典記載確認

#### チェック項目

| セクション | 出典記載 |
|-----------|---------|
| 主要機能追加 | PR番号記載 |
| セキュリティ強化 | PR番号記載 |
| UX改善 | PR番号記載 |
| 動作変更 | PR番号記載 |
| バグフィックス | PR番号記載 |
| その他の改善 | PR番号記載 |
| 統計 | リリースノート |
| リンク | GitHub URL |

#### チェックリスト

- [ ] 全セクションに出典が記載されている
- [ ] PR番号が正確
- [ ] リリースノートへのリンクがある

---

## Phase 3 完了チェックリスト

### 検証結果

| 検証項目 | 結果 | 問題数 |
|---------|------|--------|
| PR番号の存在 | ✅/❌ | X件 |
| コントリビューター名 | ✅/❌ | X件 |
| リリース日時 | ✅/❌ | X件 |
| リンク切れ | ✅/❌ | X件 |
| 表記統一 | ✅/❌ | X件 |
| 出典記載 | ✅/❌ | X件 |

### 総合判定

- [ ] すべての検証項目に合格

---

## 最終確認

### ドキュメント品質チェック

#### 使用ツール

```bash
# 日付整合性チェック
./06_scripts/check-dates.sh

# ファイル数確認
./06_scripts/count-files.sh
```

#### チェックリスト

- [ ] 日付が統一されている
- [ ] リンク切れがない
- [ ] ファイル数が正確

---

### Git操作

```bash
# 変更確認
git status
git diff

# コミット
git add docs/03_for-community/01_updates/
git commit -m "docs: Q CLI vX.Y.Z対応"

# プッシュ
git push origin main
```

---

## 作業記録

作業記録テンプレート: `/home/katoh/work_records/YYYYMMDD/YYYYMMDDHHmm_vX.Y.Z_update_worklog.md`

---

## トラブルシューティング

### ソースコードクローン失敗
- ネットワーク接続を確認
- プロキシ設定を確認

### PR番号が存在しない
- リリースノートで確認
- GitHub UIで直接検索

### コマンド名の綴りが不明
- `mod.rs`の`pub enum ChatCommand`を確認
- Q CLIで`/help`を実行

---

最終更新: 2025-10-26
