# 重大な瑕疵の根本原因調査

## 発生日時
2025-11-02 09:53 (JST)

## 問題の内容

### 誤った修正案を提案
**誤り**: `"use_legacy_mcp_json": true` が誤りで、`"useLegacyMcpJson": true` が正しいと提案

**実際**: 両方とも正しい可能性がある
- Rustコード: `use_legacy_mcp_json` （スネークケース）
- JSON設定: `useLegacyMcpJson` （キャメルケース）に**自動変換される**

## 根本原因の調査

### 発見した事実

#### 1. Serde設定の確認
```rust
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]  // ← 重要！
pub struct AgentConfigV2025_08_22 {
    pub use_legacy_mcp_json: bool,  // Rustではスネークケース
}
```

**重要な発見**: `#[serde(rename_all = "camelCase")]`

この設定により、Rustの `use_legacy_mcp_json` は自動的に `useLegacyMcpJson` に変換される。

#### 2. JSON Schemaの確認
```bash
$ cat schemas/agent-v1.json | jq '.properties | keys' | grep -i legacy
  "useLegacyMcpJson"
```

JSON Schemaでは `useLegacyMcpJson` （キャメルケース）

#### 3. 実際の使用例
Rustコード内のテストでは:
```rust
use_legacy_mcp_json: true,  // Rustコード内
```

### 結論

**正しい記載**:
```json
{
  "useLegacyMcpJson": true  // JSON設定ファイル
}
```

**誤った記載**:
```json
{
  "use_legacy_mcp_json": true  // これは動作しない
}
```

## なぜなぜ分析

### なぜ1: なぜ誤った修正案を提案したのか？
**回答**: Rustコードの `use_legacy_mcp_json` を見て、そのままJSONでも使えると思い込んだ

### なぜ2: なぜSerdeの変換を見落としたのか？
**回答**: 構造体の定義（`#[serde(rename_all = "camelCase")]`）を確認しなかった

### なぜ3: なぜ構造体の定義を確認しなかったのか？
**回答**: フィールド名だけを確認し、構造体全体の設定を確認しなかった

### なぜ4: なぜ構造体全体の設定を確認しなかったのか？
**回答**: 「フィールド名を確認すれば十分」という思い込みがあった

### なぜ5: なぜJSON Schemaを最初に確認しなかったのか？
**回答**: Rustコードを優先して確認し、JSON Schemaの確認を後回しにした

## 作業原則違反の分析

### 違反した原則

#### 原則1: 推測を排除する
**違反内容**: 
- Rustのフィールド名をそのままJSONで使えると推測
- Serdeの変換ルールを確認せずに判断

**正しい行動**:
- JSON Schemaを最初に確認
- 実際のJSON例を確認
- Serdeの設定を確認

#### 原則2: 全体を把握してから作業する
**違反内容**:
- フィールド名だけを確認
- 構造体全体の設定を確認しなかった

**正しい行動**:
- 構造体の定義全体を確認
- Serdeの設定を確認
- JSON Schemaとの対応を確認

#### 原則3: 実装照合チェックリスト
**違反内容**:
- JSON Schemaの確認を省略
- 実際のJSON例の確認を省略

**正しい行動**:
- JSON Schemaを確認
- テストコード内のJSON例を確認
- ドキュメント内の例を確認

## 影響範囲

### 誤った情報を提供
1. ユーザーへの回答で誤った情報を提供
2. 信頼性の低下

### 実際の影響
- docs/01_for-users/03_configuration/01_overview.md に誤った設定例を追加済み
- **即座に修正が必要**

## 修正内容

### 修正対象
`docs/01_for-users/03_configuration/01_overview.md`

**誤り**:
```json
{
  "use_legacy_mcp_json": true  // グローバルMCP設定も読み込む
}
```

**正しい**:
```json
{
  "useLegacyMcpJson": true  // グローバルMCP設定も読み込む
}
```

## 再発防止策

### 即時対応
1. ✅ 誤った設定例を修正
2. ✅ 根本原因を分析
3. ✅ 作業原則違反を特定

### 短期対応（今週中）
1. ⬜ 実装照合チェックリストの強化
   - JSON Schemaの確認を必須化
   - Serdeの設定確認を必須化
   - 実際のJSON例の確認を必須化

2. ⬜ 検証プロセスの追加
   - 設定例は必ず実際に動作確認
   - JSON Schemaとの整合性を確認

### 中期対応（今月中）
1. ⬜ チェックリストの更新
   - 「Serdeの変換ルールを確認」を追加
   - 「JSON Schemaを最初に確認」を追加

2. ⬜ ドキュメント化
   - RustとJSONの対応ルールを文書化
   - Serdeの変換ルールを説明

## 学んだこと

### 技術的教訓
1. **Serdeの変換ルールを理解する**
   - `#[serde(rename_all = "camelCase")]` の影響
   - Rustのスネークケース → JSONのキャメルケース

2. **JSON Schemaを最優先で確認**
   - JSON設定ファイルの正しい形式はJSON Schemaに記載
   - Rustコードは内部実装

3. **実際の例を確認する**
   - テストコード内のJSON例
   - ドキュメント内の例

### プロセス的教訓
1. **推測を完全に排除**
   - 「たぶん」「おそらく」は禁止
   - すべて確認する

2. **全体を把握する**
   - フィールド名だけでなく構造体全体
   - Serdeの設定も含めて確認

3. **チェックリストを厳守**
   - 実装照合チェックリストを省略しない
   - すべての項目を確認

## 今後のアクション

### 今すぐ実施
1. ✅ 誤った設定例を修正
2. ✅ 根本原因調査レポートを作成
3. ⬜ 修正をコミット・プッシュ

### 今週中に実施
1. ⬜ チェックリストの強化
2. ⬜ 検証プロセスの追加
3. ⬜ lessons-learned.mdに追記

### 今月中に実施
1. ⬜ ドキュメント化
2. ⬜ チーム内での共有
3. ⬜ 再発防止策の定着確認

---

最終更新: 2025-11-02 09:54 (JST)
