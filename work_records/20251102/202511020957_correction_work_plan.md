# 作業計画 - use_legacy_mcp_json誤記修正と全ファイルチェック

## 作成日時
2025-11-02 09:57 (JST)

## 目的
1. docs/01_for-users/03_configuration/01_overview.md の誤った設定例を修正
2. use_legacy_mcp_json の記載が残っていないか水平展開
3. Rustの変換前の情報を使っている箇所を全ファイルでチェック

---

## フェーズ1: 即時修正（推定時間: 10分）

### タスク1-1: 01_overview.mdの修正

**対象ファイル**: `docs/01_for-users/03_configuration/01_overview.md`

**修正内容**:
```json
# 修正前（誤り）
{
  "use_legacy_mcp_json": true  // グローバルMCP設定も読み込む
}

# 修正後（正しい）
{
  "useLegacyMcpJson": true  // グローバルMCP設定も読み込む
}
```

**検証方法**:
```bash
# 修正前の確認
grep "use_legacy_mcp_json" docs/01_for-users/03_configuration/01_overview.md

# 修正後の確認
grep "useLegacyMcpJson" docs/01_for-users/03_configuration/01_overview.md
```

---

## フェーズ2: 水平展開チェック（推定時間: 15分）

### タスク2-1: use_legacy_mcp_json の全ファイル検索

**検索コマンド**:
```bash
cd /home/katoh/projects/q-cli-docs
grep -r "use_legacy_mcp_json" docs/ --include="*.md" -n
```

**期待される結果**:
- 該当なし（すべて `useLegacyMcpJson` に修正済み）

**発見した場合の対応**:
1. ファイル名と行番号を記録
2. 文脈を確認（説明文なのか、設定例なのか）
3. 設定例の場合は `useLegacyMcpJson` に修正
4. 説明文の場合は文脈に応じて判断

### タスク2-2: 修正対象ファイルのリスト化

**調査結果の記録**:
```markdown
## 修正対象ファイル

1. ファイル名: 行番号
   - 修正前: ...
   - 修正後: ...
   - 理由: ...

2. ファイル名: 行番号
   - 修正前: ...
   - 修正後: ...
   - 理由: ...
```

---

## フェーズ3: Rust変換前情報の全ファイルチェック（推定時間: 30分）

### タスク3-1: チェック対象の特定

**チェック対象**:
1. **Agent設定のフィールド名**
   - Rust: スネークケース
   - JSON: キャメルケース（`#[serde(rename_all = "camelCase")]`）

2. **MCP設定のフィールド名**
   - 同様にSerdeの変換ルールを確認

3. **その他の設定項目**
   - グローバル設定
   - 環境変数名（これは変換されない）

### タスク3-2: Agent設定フィールドの確認

**確認方法**:
```bash
# 1. Rustソースコードから全フィールド名を抽出
cd /tmp/q-cli-source
awk '/^pub struct AgentConfigV2025_08_22/,/^}/' \
  crates/agent/src/agent/agent_config/definitions.rs | \
  grep "pub " | \
  awk '{print $2}' | \
  sed 's/://g' > /tmp/rust_fields.txt

# 2. JSON Schemaから全フィールド名を抽出
cat schemas/agent-v1.json | \
  jq -r '.properties | keys[]' > /tmp/json_fields.txt

# 3. 対応表を作成
paste /tmp/rust_fields.txt /tmp/json_fields.txt
```

**期待される対応表**:
```
Rustフィールド名          JSONフィールド名
-----------------        -----------------
use_legacy_mcp_json  →  useLegacyMcpJson
mcp_servers          →  mcpServers
tool_settings        →  toolSettings
tool_aliases         →  toolAliases
tool_schema          →  toolSchema
system_prompt        →  systemPrompt
model_preferences    →  modelPreferences
```

### タスク3-3: ドキュメント内のスネークケース検索

**検索対象パターン**:
```bash
# Agent設定関連のスネークケースを検索
cd /home/katoh/projects/q-cli-docs
grep -r "mcp_servers\|tool_settings\|tool_aliases\|tool_schema\|system_prompt\|model_preferences" \
  docs/ --include="*.md" -n | \
  grep -v "Rust\|ソースコード\|内部実装" > /tmp/snake_case_findings.txt
```

**除外条件**:
- Rustコードの説明文
- ソースコード構造の説明
- 内部実装の説明

**チェック対象**:
- JSON設定例
- 設定手順
- コマンド例

### タスク3-4: 発見した問題の分類

**分類基準**:

#### カテゴリA: 即座に修正（設定例）
- JSON設定例でスネークケースを使用
- ユーザーが実際に使用する設定

**対応**: キャメルケースに修正

#### カテゴリB: 文脈確認（説明文）
- Rustコードの説明
- 内部実装の説明

**対応**: 文脈に応じて判断
- Rustコードの説明 → そのまま（スネークケース）
- JSON設定の説明 → キャメルケースに修正

#### カテゴリC: 対象外（環境変数）
- 環境変数名（`Q_LOG_LEVEL`等）
- これらは変換されない

**対応**: 修正不要

---

## フェーズ4: 検証と品質確認（推定時間: 15分）

### タスク4-1: JSON Schemaとの整合性確認

**確認方法**:
```bash
# 1. ドキュメント内のすべてのJSON設定例を抽出
cd /home/katoh/projects/q-cli-docs
find docs/ -name "*.md" -exec grep -Pzo '```json\n\{[^`]*\}' {} \; > /tmp/all_json_examples.txt

# 2. Agent設定の例を抽出
grep -A 20 "version.*2025-08-22" /tmp/all_json_examples.txt > /tmp/agent_examples.txt

# 3. フィールド名を抽出
grep -oP '"\K[^"]+(?=":)' /tmp/agent_examples.txt | sort -u > /tmp/used_fields.txt

# 4. JSON Schemaと比較
cat schemas/agent-v1.json | jq -r '.properties | keys[]' | sort > /tmp/schema_fields.txt
diff /tmp/used_fields.txt /tmp/schema_fields.txt
```

**期待される結果**:
- すべてのフィールド名がJSON Schemaと一致
- スネークケースのフィールド名が存在しない

### タスク4-2: 自動化ツールでの検証

**検証コマンド**:
```bash
cd /home/katoh/projects/q-cli-docs

# 1. ファイル数チェック
./scripts/count-files.sh

# 2. 日付チェック
./scripts/check-dates.sh docs/

# 3. 連続区切り線チェック
./tools/check-consecutive-separators.sh

# 4. 環境変数バリデーション
cd tools/verification
python3 validators/env_validator.py ../../docs

# 5. 統合バリデーション
python3 validators/v2_validator.py ../../docs
```

**期待される結果**:
- すべてのツールで警告0件

### タスク4-3: 手動チェック

**チェック項目**:
- [ ] すべての設定例がJSON Schemaと一致
- [ ] スネークケースのフィールド名が存在しない
- [ ] 説明文の文脈が正しい
- [ ] リンクが正しく機能する

---

## フェーズ5: 作業記録と再発防止（推定時間: 10分）

### タスク5-1: 作業記録の作成

**記録内容**:
1. 修正したファイル数
2. 発見した問題の分類
3. 修正内容の詳細
4. 検証結果

### タスク5-2: lessons-learned.mdへの追記

**追記内容**:
- 問題9: Serdeの変換ルール見落とし
- 根本原因: JSON Schemaの確認を省略
- 教訓: JSON設定はJSON Schemaを最優先で確認

### タスク5-3: チェックリストの更新

**更新対象**: `docs/05_meta/06_manual-checks.md`

**追加項目**:
```markdown
### 実装照合チェックリスト

#### JSON設定の確認（新規追加）

- [ ] JSON Schemaを確認
  ```bash
  cat schemas/agent-v1.json | jq '.properties | keys'
  ```

- [ ] Serdeの変換ルールを確認
  ```bash
  grep "#\[serde(rename_all" crates/*/src/**/*.rs
  ```

- [ ] フィールド名がキャメルケースであることを確認
  - Rust: スネークケース（use_legacy_mcp_json）
  - JSON: キャメルケース（useLegacyMcpJson）
```

---

## 成果物

### 修正ファイル
1. `docs/01_for-users/03_configuration/01_overview.md` - 設定例修正
2. その他発見されたファイル - 水平展開での修正

### 調査レポート
1. `202511020957_correction_work_plan.md` - 作業計画（本ファイル）
2. `202511020957_correction_results.md` - 調査結果と修正内容
3. `202511020957_worklog.md` - 作業記録

### 更新ドキュメント
1. `docs/05_meta/07_lessons-learned.md` - 問題9を追記
2. `docs/05_meta/06_manual-checks.md` - チェックリスト更新

---

## リスクと対策

### リスク1: 大量の修正箇所が発見される
**対策**: 
- 優先順位を付けて段階的に修正
- 設定例を最優先
- 説明文は文脈を確認してから修正

### リスク2: 文脈判断が難しい箇所がある
**対策**:
- Rustコードの説明 → スネークケースのまま
- JSON設定の説明 → キャメルケースに修正
- 不明な場合は保留してレビュー

### リスク3: 他のフィールド名でも同様の問題がある
**対策**:
- Agent設定の全フィールドを確認
- MCP設定の全フィールドを確認
- グローバル設定の全フィールドを確認

---

## 品質基準

### 正確性
- すべての設定例がJSON Schemaと一致
- スネークケースのフィールド名が存在しない
- 説明文の文脈が正しい

### 完全性
- すべてのマークダウンファイルをチェック
- すべての設定例をチェック
- すべてのフィールド名をチェック

### 一貫性
- 同じフィールド名は同じ表記
- 設定例は統一されたフォーマット
- 説明文は統一された用語

---

## 推定作業時間

| フェーズ | 推定時間 |
|---------|---------|
| フェーズ1: 即時修正 | 10分 |
| フェーズ2: 水平展開チェック | 15分 |
| フェーズ3: 全ファイルチェック | 30分 |
| フェーズ4: 検証と品質確認 | 15分 |
| フェーズ5: 作業記録と再発防止 | 10分 |
| **合計** | **80分** |

---

## 備考

### 作業原則の適用
- **原則1: 推測を排除** - JSON Schemaを必ず確認
- **原則2: 全体を把握** - Serdeの変換ルールを確認
- **原則3: 実装照合** - すべてのフィールド名を確認

### 品質保証
- 自動化ツールで検証
- 手動チェックで確認
- 作業記録を作成

---

最終更新: 2025-11-02 09:57 (JST)
