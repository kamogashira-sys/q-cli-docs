[ホーム](../README.md) > [Meta](README.md) > 命名規則リファレンス

---

# 命名規則リファレンス

本サイトのファイル・ディレクトリの命名規則を定義します。

**最終更新**: 2025-11-01

---

## 📋 目次

1. [基本原則](#基本原則)
2. [ファイル名](#ファイル名)
3. [ディレクトリ名](#ディレクトリ名)
4. [特殊ファイル](#特殊ファイル)
5. [禁止事項](#禁止事項)
6. [例外ケース](#例外ケース)

---

## 基本原則

### 1. 一貫性
- 同じルールを全てのファイルに適用
- 例外は最小限に

### 2. 可読性
- 人間が読みやすい名前
- 内容が推測できる名前

### 3. 機械処理性
- スクリプトで処理しやすい形式
- 特殊文字を避ける

### 4. 拡張性
- 将来の追加を考慮
- 番号の余裕を持たせる

---

## ファイル名

### 基本形式

```
番号_トピック名.md
```

**構成要素**:
1. **番号**: 2桁のゼロパディング（01-99）
2. **アンダースコア**: 区切り文字
3. **トピック名**: ケバブケース（小文字 + ハイフン）
4. **拡張子**: `.md`（Markdown）

### 番号付けルール

#### 連番の使用
```
01_first-topic.md
02_second-topic.md
03_third-topic.md
```

**ルール**:
- 01から開始
- 連続した番号
- 欠番なし

#### ゼロパディング
```
✅ 01_topic.md
✅ 09_topic.md
✅ 10_topic.md

❌ 1_topic.md
❌ 9_topic.md
```

**理由**:
- ファイルソート時の順序保証
- 視覚的な統一感

#### 番号の範囲
- **最小**: 01
- **最大**: 99
- **推奨**: 01-20（将来の追加を考慮）

### トピック名のルール

#### ケバブケース
```
✅ getting-started.md
✅ quick-start.md
✅ agent-configuration.md

❌ getting_started.md  # スネークケース
❌ GettingStarted.md   # パスカルケース
❌ gettingStarted.md   # キャメルケース
```

#### 小文字のみ
```
✅ aws-cli-integration.md
❌ AWS-CLI-Integration.md
❌ Aws-Cli-Integration.md
```

#### 単語の区切り
```
✅ multi-word-topic.md
✅ very-long-topic-name.md

❌ multiwordtopic.md
❌ multi_word_topic.md
```

#### 長さの制限
- **推奨**: 20-40文字
- **最大**: 60文字
- **最小**: 5文字

```
✅ configuration.md           # 15文字
✅ agent-configuration.md     # 22文字
✅ mcp-server-setup.md        # 19文字

⚠️ very-long-topic-name-that-describes-everything.md  # 50文字（長すぎ）
❌ a.md                       # 1文字（短すぎ）
```

### 特殊な接尾辞

#### 概要ファイル
```
01_overview.md
01_introduction.md
```

**用途**: カテゴリの概要説明

#### リファレンスファイル
```
03_settings-reference.md
08_quick-reference.md
```

**用途**: 技術仕様やクイックリファレンス

#### ガイドファイル
```
05_practical-guide.md
06_troubleshooting-guide.md
```

**用途**: 実践的な手順書

### 良い例・悪い例

#### 良い例
```
✅ 01_installation.md
✅ 02_quick-start.md
✅ 03_agent-configuration.md
✅ 04_mcp-server-setup.md
✅ 05_environment-variables.md
```

**理由**:
- 番号が連番
- ゼロパディング
- ケバブケース
- 内容が推測できる

#### 悪い例
```
❌ 1_install.md              # ゼロパディングなし
❌ 03_Agent_Config.md        # 大文字使用
❌ 05_mcp_server.md          # スネークケース
❌ 10-next-topic.md          # ハイフン区切り（番号）
❌ topic.md                  # 番号なし
```

---

## ディレクトリ名

### 基本形式

```
番号_カテゴリ名
```

**構成要素**:
1. **番号**: 2桁のゼロパディング（01-99）
2. **アンダースコア**: 区切り文字
3. **カテゴリ名**: ケバブケース（小文字 + ハイフン）

### トップレベルディレクトリ

```
docs/
├── 01_for-users/
├── 02_for-developers/
├── 03_for-community/
├── 04_issues/
└── 05_meta/
```

**ルール**:
- `for-`プレフィックス: 対象ユーザーを明示
- 複数形: `users`, `developers`
- 単数形: `community`, `meta`

### サブディレクトリ

```
01_for-users/
├── 01_getting-started/
├── 02_features/
├── 03_configuration/
├── 04_best-practices/
├── 05_deployment/
├── 06_troubleshooting/
├── 07_reference/
├── 08_guides/
├── 09_security/
└── 10_file-specifications/
```

**ルール**:
- 機能・トピック別
- 複数形推奨: `features`, `guides`
- 動名詞形: `getting-started`, `troubleshooting`

### 良い例・悪い例

#### 良い例
```
✅ 01_getting-started/
✅ 02_features/
✅ 03_configuration/
✅ 08_guides/
```

**理由**:
- 番号が連番
- ケバブケース
- 内容が明確

#### 悪い例
```
❌ 1_getting_started/        # ゼロパディングなし、スネークケース
❌ 03_Configuration/         # 大文字使用
❌ features/                 # 番号なし
❌ 10-guides/                # ハイフン区切り（番号）
```

---

## 特殊ファイル

### README.md

**配置**: 全てのディレクトリ

**命名**: 常に`README.md`（大文字）

**例外**: 番号なし

```
docs/
├── README.md
├── 01_for-users/
│   ├── README.md
│   ├── 01_getting-started/
│   │   └── README.md
│   └── 02_features/
│       └── README.md
```

### UPPERCASE.md

**用途**: 重要なメタファイル

**例**:
```
CONTRIBUTING.md
QUALITY_ASSURANCE.md
IMPLEMENTATION_VERIFICATION.md
```

**ルール**:
- 全て大文字
- アンダースコア区切り
- 番号なし（例外あり）

**例外**: 05_meta/では番号付き
```
05_meta/
├── 01_CONTRIBUTING.md
├── 02_QUALITY_ASSURANCE.md
└── 03_IMPLEMENTATION_VERIFICATION.md
```

### チェックリストファイル

**命名**: `*-checklist.md`

**例**:
```
env-vars-checklist.md
file-paths-checklist.md
settings-checklist.md
```

**ルール**:
- 番号なし
- ケバブケース
- `-checklist`接尾辞

---

## 禁止事項

### 1. 特殊文字の使用

```
❌ 01_topic!.md
❌ 02_topic?.md
❌ 03_topic*.md
❌ 04_topic<>.md
❌ 05_topic|.md
```

**理由**: ファイルシステムやスクリプトで問題

### 2. スペースの使用

```
❌ 01 topic.md
❌ 02 my topic.md
```

**理由**: コマンドライン操作で問題

### 3. 日本語の使用

```
❌ 01_トピック.md
❌ 02_設定ガイド.md
```

**理由**: 国際化、エンコーディング問題

### 4. 大文字の使用（特殊ファイル除く）

```
❌ 01_Topic.md
❌ 02_MyTopic.md
❌ 03_TOPIC.md
```

**例外**: `README.md`, `CONTRIBUTING.md`など

### 5. 番号の重複

```
❌ 01_topic-a.md
❌ 01_topic-b.md  # 重複
```

### 6. 番号の欠番（原則）

```
❌ 01_topic-a.md
❌ 03_topic-b.md  # 02が欠番
❌ 05_topic-c.md  # 04が欠番
```

**例外**: 意図的な削除後（番号は振り直さない）

---

## 例外ケース

### Case 1: 大文字ファイル

**状況**: 重要なメタファイル

```
✅ CONTRIBUTING.md
✅ QUALITY_ASSURANCE.md
✅ LICENSE
```

**理由**: GitHub慣習、視認性

### Case 2: 番号なしファイル

**状況**: チェックリスト、テンプレート

```
✅ env-vars-checklist.md
✅ file-paths-checklist.md
✅ template.md
```

**理由**: 特殊な用途、順序不要

---

## リネーム手順

### 1. 影響範囲の確認

```bash
# 旧ファイル名へのリンクを検索
rg "old-filename.md" docs/
```

### 2. Gitでリネーム

```bash
# 履歴を保持してリネーム
git mv docs/path/old-filename.md docs/path/new-filename.md
```

### 3. リンクの更新

```bash
# 検出された全てのリンクを更新
# old-filename.md → new-filename.md
```

### 4. README.md更新

```bash
# 該当ディレクトリのREADME.mdを更新
```

### 5. 検証

```bash
# リンク切れチェック
cd tools/verification
make validate-all
```

---

## 検証方法

### 自動検証

```bash
# パス検証
cd tools/verification
python3 validators/path_validator.py ../../docs

# 統合検証
python3 validators/v2_validator.py ../../docs
```

### 手動確認

```bash
# ファイル名パターンチェック
find docs -name "*.md" | grep -v "README.md" | grep -vE "^docs/[0-9]{2}_"

# ディレクトリ名パターンチェック
find docs -type d | grep -vE "^docs/[0-9]{2}_"
```

---

## 命名規則チェックリスト

### ファイル作成時

- [ ] 番号は2桁ゼロパディング（01-99）
- [ ] トピック名はケバブケース
- [ ] 全て小文字（特殊ファイル除く）
- [ ] 特殊文字なし
- [ ] スペースなし
- [ ] 日本語なし
- [ ] 拡張子は`.md`
- [ ] 番号は連番（欠番なし）

### ディレクトリ作成時

- [ ] 番号は2桁ゼロパディング（01-99）
- [ ] カテゴリ名はケバブケース
- [ ] 全て小文字
- [ ] 特殊文字なし
- [ ] スペースなし
- [ ] 日本語なし
- [ ] README.md作成済み

---

## 関連ドキュメント

- **[ファイル構造リファレンス](11_file-structure.md)** - ディレクトリ構造と配置ルール
- **[検証ツールリファレンス](13_validation-reference.md)** - 自動検証ツールの使い方
- **[日常ワークフロー](09_daily-workflow.md)** - ファイル作成の実践手順

---

**最終更新**: 2025-11-01  
**メンテナー**: ドキュメントチーム
