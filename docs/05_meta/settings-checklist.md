# 設定項目確認チェックリスト

**最終更新**: 2025-10-27  
**目的**: Agent設定・MCP設定・グローバル設定の正確性を確保

---

## ✅ Agent設定確認項目

### 1. 基本構造

- [ ] JSONスキーマが正しく記載されているか
- [ ] 必須フィールドが含まれているか（`name`）
- [ ] 存在しないフィールドが含まれていないか

**正しい例**:
```json
{
  "$schema": "https://amazon-q-developer-cli.s3.us-west-2.amazonaws.com/agent-schema-v1.json",
  "name": "my-agent",
  "description": "My custom agent"
}
```

**誤った例**:
```json
{
  "version": "1.0",  // ❌ 存在しないフィールド
  "name": "my-agent"
}
```

---

### 2. hooks構造の確認【重要】

2025-10-27の検証で**31箇所**のhooks構造エラーが発見されました。

#### ✅ 正しいhooks構造

```json
{
  "hooks": {
    "agentSpawn": [
      {
        "command": "echo 'Agent started'"
      }
    ],
    "preToolUse": [
      {
        "command": "./validate.sh",
        "matcher": "fs_write"
      }
    ],
    "postToolUse": [
      {
        "command": "echo 'Tool completed'",
        "matcher": "fs_*"
      }
    ],
    "userPromptSubmit": [
      {
        "command": "git status"
      }
    ],
    "stop": [
      {
        "command": "npm run format",
        "timeout_ms": 30000
      }
    ]
  }
}
```

#### ❌ 誤ったパターン1: オブジェクト形式

```json
{
  "hooks": {
    "AgentSpawn": {  // ❌ 配列ではない
      "command": "echo 'test'",
      "async": false  // ❌ 存在しないフィールド
    }
  }
}
```

#### ❌ 誤ったパターン2: 配列形式

```json
{
  "hooks": [  // ❌ hooksはオブジェクト
    {
      "trigger": "PreToolUse",  // ❌ triggerフィールドは不要
      "tool_matcher": "fs_*",   // ❌ matcherが正しい
      "command": ["./script.sh"]  // ❌ 文字列が正しい
    }
  ]
}
```

#### チェック項目

- [ ] `hooks`はオブジェクト形式か
- [ ] フック名は小文字キャメルケースか（`agentSpawn`, `preToolUse`, `postToolUse`, `userPromptSubmit`, `stop`）
- [ ] 各フックの値は配列形式か
- [ ] `trigger`フィールドが含まれていないか
- [ ] `tool_matcher`ではなく`matcher`を使用しているか
- [ ] `async`フィールドが含まれていないか
- [ ] `command`は文字列形式か（配列ではない）
- [ ] `timeout`ではなく`timeout_ms`を使用しているか

---

### 3. hooks種別の確認

#### 利用可能なhooks（5種類）

- [ ] `agentSpawn` - Agent起動時
- [ ] `preToolUse` - ツール実行前
- [ ] `postToolUse` - ツール実行後
- [ ] `userPromptSubmit` - ユーザープロンプト送信時
- [ ] `stop` - アシスタント応答完了時（v1.18.0+）

#### 存在しないhooks

- [ ] `prePrompt` が使用されていないか（存在しない）
- [ ] `AgentSpawn` など大文字が使用されていないか

---

### 4. Stop Hookの確認【重要】

2025-10-27の検証で**5箇所**のStop Hook関連エラーが発見されました。

#### タイミングの説明

- [ ] ❌ "Agent終了時" と記載されていないか
- [ ] ✅ "アシスタント応答完了時（会話ターン終了時）" と記載されているか

#### 用途の説明

- [ ] コンパイル、テスト実行、コードフォーマット、クリーンアップ処理が記載されているか
- [ ] 単なる「クリーンアップ」だけでないか

#### 終了コードの説明

- [ ] ❌ "0=成功、その他=失敗" と記載されていないか
- [ ] ✅ "0=成功、その他=警告として表示" と記載されているか

#### 構造の確認

- [ ] Stop Hookも配列形式か
- [ ] `timeout_ms`フィールドが使用されているか（`timeout`ではない）

**正しい例**:
```json
{
  "hooks": {
    "stop": [
      {
        "command": "npm run format",
        "timeout_ms": 30000
      }
    ]
  }
}
```

---

### 5. フィールド名の確認

#### 正しいフィールド名

- [ ] `matcher` （`tool_matcher`ではない）
- [ ] `timeout_ms` （`timeout`ではない）
- [ ] `$schema` （`version`ではない）

#### 存在しないフィールド

- [ ] `version` が含まれていないか
- [ ] `async` が含まれていないか
- [ ] `trigger` が含まれていないか

---

## ✅ MCP設定確認項目

### 6. MCP設定構造

- [ ] `mcpServers`オブジェクトが正しく記載されているか
- [ ] サーバー名がキーとして使用されているか
- [ ] 各サーバーに`command`が含まれているか

**正しい例**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
  }
}
```

---

### 7. 環境変数展開

- [ ] `${env:VAR_NAME}`構文が正しく使用されているか
- [ ] 環境変数名が大文字で記載されているか

**正しい例**:
```json
{
  "command": "node",
  "args": ["${env:HOME}/.config/mcp/server.js"]
}
```

---

## ✅ グローバル設定確認項目

### 8. 設定項目の確認

#### テレメトリー設定
- [ ] `telemetry.enabled` - 真偽値が正しいか
- [ ] デフォルト値（`true`）が記載されているか

#### チャット設定
- [ ] `chat.model` - モデル名の形式が正しいか
- [ ] `chat.temperature` - 範囲（0.0-1.0）が記載されているか
- [ ] `chat.maxTokens` - 数値形式が正しいか

#### Knowledge設定
- [ ] `knowledge.enabled` - 真偽値が正しいか
- [ ] `knowledge.path` - パス形式が正しいか

---

## 📋 バグ再発防止項目

### 9. 過去のバグパターン（2025-10-27検証）

#### hooks構造エラー（31箇所）

- [ ] hooksがオブジェクト形式になっているか
- [ ] フック名が小文字キャメルケースか
- [ ] 各フックの値が配列形式か
- [ ] `trigger`フィールドが削除されているか
- [ ] `matcher`が使用されているか（`tool_matcher`ではない）
- [ ] `async`フィールドが削除されているか
- [ ] `command`が文字列形式か
- [ ] `timeout_ms`が使用されているか（`timeout`ではない）

#### versionフィールドエラー（3箇所）

- [ ] `version`フィールドが削除されているか
- [ ] `$schema`フィールドが使用されているか

#### Stop Hook説明エラー（5箇所）

- [ ] タイミングが正確に記載されているか
- [ ] 用途が詳細に記載されているか
- [ ] 終了コードの説明が正確か

---

## 🔧 修正時の注意事項

### 10. 修正作業

#### 事前確認
- [ ] 公式スキーマで仕様を確認
- [ ] ソースコードで実装を確認
- [ ] 他のファイルで同じパターンを検索

#### 修正実施
- [ ] 1箇所ずつ慎重に修正
- [ ] 修正後に構文チェック
- [ ] 動作確認

#### 横展開
- [ ] 同じ設定項目が他のファイルにもないか確認
- [ ] 同じパターンの誤りが他にもないか確認
- [ ] 関連する設定項目も確認

---

### 11. 検証方法

#### スキーマ検証
```bash
# Agent設定のスキーマ検証
q agent validate my-agent.json
```

#### 実装確認
```bash
# ソースコードで実装を確認
rg "hooks" ~/amazon-q-developer-cli/src/
```

#### 動作確認
```bash
# 実際にAgent設定を使用して動作確認
q chat --agent my-agent "test"
```

---

## 📊 チェック結果の記録

### 確認日時
- 確認日: YYYY-MM-DD
- 確認者: 

### 確認結果
- 総確認項目数: 
- 問題発見数: 
- 修正完了数: 

### 発見した問題
1. 
2. 
3. 

---

## 📚 参考資料

### 公式ドキュメント
- [Agent設定ガイド](../01_for-users/03_configuration/03_agent-configuration.md)
- [Agent設定仕様](../01_for-users/10_file-specifications/02_agent-configuration.md)
- [MCP設定ガイド](../01_for-users/03_configuration/04_mcp-configuration.md)
- [グローバル設定ガイド](../01_for-users/03_configuration/02_global-settings.md)

### 検証レポート
- [Agent設定検証レポート](/home/katoh/work_records/20251027/agent-docs-full-verification-report.md)
- [修正計画書](/home/katoh/work_records/20251027/final-documentation-fix-plan.md)

### 関連チェックリスト
- [環境変数確認チェックリスト](env-vars-checklist.md)
- [ファイルパス確認チェックリスト](file-paths-checklist.md)

---

**作成日**: 2025-10-27  
**バージョン**: 1.0  
**作成根拠**: 2025-10-27の修正作業で発見された36箇所のバグパターンを基に作成
