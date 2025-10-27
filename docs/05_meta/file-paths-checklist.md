# ファイルパス確認チェックリスト

**最終更新**: 2025-10-27  
**目的**: ドキュメント内のファイルパス記述の正確性を確保

---

## ✅ 基本確認項目

### 1. パス形式の確認

#### 絶対パス
- [ ] `/`で始まっているか
- [ ] 実在するパスか
- [ ] OSに依存しないパスか

**正しい例**:
```
/home/user/.config/amazonq/
/usr/local/bin/q
```

#### ホームディレクトリ相対パス
- [ ] `~`で始まっているか
- [ ] `~/`の後のパスが正しいか

**正しい例**:
```
~/.config/amazonq/
~/.amazonq/agents/
```

#### 相対パス
- [ ] `./`または`../`で始まっているか
- [ ] 基準ディレクトリが明記されているか

**正しい例**:
```
./my-agent.json  # カレントディレクトリ基準
../config/settings.json  # 親ディレクトリ基準
```

---

### 2. Q CLI関連パスの確認

#### 設定ディレクトリ
- [ ] `~/.config/amazonq/` - グローバル設定
- [ ] `~/.amazonq/` - ユーザーデータ
- [ ] `./.amazonq/` - プロジェクト設定

#### Agent設定
- [ ] `~/.amazonq/agents/` - Agent設定ディレクトリ
- [ ] `~/.amazonq/agents/<agent-name>.json` - Agent設定ファイル

#### MCP設定
- [ ] `~/.config/amazonq/mcp.json` - MCP設定ファイル

#### Knowledge
- [ ] `~/.amazonq/knowledge/` - Knowledgeディレクトリ

---

### 3. パスの存在確認

- [ ] 記載されたパスが実際に存在するか
- [ ] 存在しない場合、作成方法が記載されているか
- [ ] パーミッションが適切か

---

## 🔍 詳細確認項目

### 4. OS依存性の確認

#### Linux/macOS
- [ ] パスセパレータが`/`か
- [ ] ホームディレクトリが`~`で表現されているか

**正しい例**:
```
~/.config/amazonq/settings.json
/usr/local/bin/q
```

#### Windows
- [ ] Windowsパスが記載されている場合、注釈があるか
- [ ] バックスラッシュがエスケープされているか

**正しい例**:
```
C:\\Users\\username\\.config\\amazonq\\settings.json
```

または

```
C:/Users/username/.config/amazonq/settings.json
```

---

### 5. 環境変数を含むパス

- [ ] `${env:VAR_NAME}`構文が正しく使用されているか
- [ ] 環境変数名が大文字で記載されているか
- [ ] 環境変数が存在することが前提として記載されているか

**正しい例**:
```json
{
  "command": "node",
  "args": ["${env:HOME}/.config/mcp/server.js"]
}
```

---

### 6. 相対パスの基準

- [ ] 相対パスの基準ディレクトリが明記されているか
- [ ] カレントディレクトリに依存する場合、注意書きがあるか

**正しい例**:
```markdown
カレントディレクトリを基準とした相対パス:
./my-agent.json

プロジェクトルートを基準とした相対パス:
./config/agent.json
```

---

## 🎯 実践的確認項目

### 7. Agent設定内のパス

#### command フィールド
- [ ] 実行可能ファイルのパスが正しいか
- [ ] PATHに含まれるコマンドか、絶対パスか

**正しい例**:
```json
{
  "command": "node"  // PATHに含まれる
}
```

または

```json
{
  "command": "/usr/local/bin/node"  // 絶対パス
}
```

#### args フィールド
- [ ] 引数に含まれるパスが正しいか
- [ ] 環境変数展開が必要な場合、正しく記載されているか

**正しい例**:
```json
{
  "args": ["${env:HOME}/.config/mcp/server.js"]
}
```

---

### 8. MCP設定内のパス

#### サーバーコマンド
- [ ] MCPサーバーのパスが正しいか
- [ ] npxを使用する場合、パッケージ名が正しいか

**正しい例**:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
}
```

#### 許可ディレクトリ
- [ ] MCPサーバーに渡すディレクトリパスが正しいか
- [ ] セキュリティ上問題ないパスか

---

### 9. Knowledge設定内のパス

- [ ] Knowledgeディレクトリのパスが正しいか
- [ ] ディレクトリが存在するか、作成方法が記載されているか

**正しい例**:
```json
{
  "knowledge": {
    "enabled": true,
    "path": "~/.amazonq/knowledge"
  }
}
```

---

## 📋 バグ再発防止項目

### 10. 過去のバグパターン

2025-10-27の検証では、パス関連の直接的なバグは発見されませんでしたが、以下の点に注意してください。

#### パターン1: 相対パスの誤用
- [ ] 基準ディレクトリが不明確でないか
- [ ] カレントディレクトリに依存していないか
- [ ] 環境によって動作が変わらないか

#### パターン2: OS依存パス
- [ ] Windowsパスが混在していないか
- [ ] バックスラッシュがエスケープされているか
- [ ] パスセパレータが統一されているか

#### パターン3: 存在しないパス
- [ ] 記載されたパスが実際に存在するか
- [ ] 存在しない場合、作成方法が記載されているか
- [ ] パーミッションの問題がないか

---

## 🔧 修正時の注意事項

### 11. 修正作業

#### 事前確認
- [ ] パスが実際に存在するか確認
- [ ] OS依存性を確認
- [ ] 環境変数の存在を確認

#### 修正実施
- [ ] パス形式を統一
- [ ] 環境変数展開を適切に使用
- [ ] 相対パスの基準を明記

#### 動作確認
- [ ] 実際にパスが解決されるか確認
- [ ] 異なる環境でも動作するか確認

---

### 12. 検証方法

#### パスの存在確認
```bash
# ファイルの存在確認
ls -la ~/.config/amazonq/settings.json

# ディレクトリの存在確認
ls -la ~/.amazonq/agents/
```

#### 環境変数の確認
```bash
# 環境変数の値を確認
echo $HOME
echo $PATH
```

#### パスの解決確認
```bash
# 相対パスの解決
realpath ./my-agent.json

# 環境変数を含むパスの解決
eval echo "~/.config/amazonq/settings.json"
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
- [MCP設定ガイド](../01_for-users/03_configuration/04_mcp-configuration.md)
- [環境変数ガイド](../01_for-users/03_configuration/06_environment-variables.md)

### Q CLI関連パス
- グローバル設定: `~/.config/amazonq/`
- ユーザーデータ: `~/.amazonq/`
- Agent設定: `~/.amazonq/agents/`
- MCP設定: `~/.config/amazonq/mcp.json`
- Knowledge: `~/.amazonq/knowledge/`

### 関連チェックリスト
- [環境変数確認チェックリスト](env-vars-checklist.md)
- [設定項目確認チェックリスト](settings-checklist.md)

---

**作成日**: 2025-10-27  
**バージョン**: 1.0  
**作成根拠**: Q CLI設定システムの仕様とベストプラクティスを基に作成
