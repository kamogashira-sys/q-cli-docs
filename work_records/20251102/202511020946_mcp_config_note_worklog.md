# 作業記録 - MCP設定の注意事項追加

## 作業開始時刻
2025-11-02 09:46 (JST)

## 作業内容
docs/01_for-users/03_configuration/01_overview.md に Agent使用時のMCP設定に関する注意事項を追加

## 追加内容

### 注意事項: Agent使用時のMCP設定について

**重要な発見**:
- Agent使用時、グローバルMCP設定（`~/.aws/amazonq/mcp.json`）はデフォルトでは参照されない
- `use_legacy_mcp_json: true` を設定することで、グローバルMCP設定も読み込まれる

**動作の詳細**:
1. **デフォルト**: Agent設定内の `mcpServers` のみが使用される
2. **グローバルMCPも使用**: `"use_legacy_mcp_json": true` を追加

**優先順位**:
1. Agent設定内の `mcpServers` （常に優先）
2. グローバル `mcp.json` （`use_legacy_mcp_json: true` の場合のみ）

**ソースコード確認**:
- ファイル: `crates/agent/src/agent/agent_config/mod.rs`
- 関数: `from_agent_config`
- 確認内容: `use_legacy_mcp_json()` の条件分岐を確認

## 追記位置
- グローバル設定ディレクトリの説明の直後
- ローカル設定ディレクトリの説明の直前

## 成果物
- 更新済みファイル: docs/01_for-users/03_configuration/01_overview.md

## 作業終了時刻
2025-11-02 09:47 (JST)
