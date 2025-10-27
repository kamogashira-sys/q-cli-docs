[ホーム](../README.md) > [Meta](README.md) > 作業原則強制適用システム

---

# 作業原則強制適用システム

**作成日時**: 2025-10-28 00:23 JST  
**更新日時**: 2025-10-28 02:48 JST  
**ステータス**: ✅ 実装完了・動作確認済み（システムプロンプト再適用機能追加）

---

## 📋 目次

1. [システム概要](#システム概要)
2. [システム構成](#システム構成)
3. [セットアップ手順](#セットアップ手順)
4. [稼働確認方法](#稼働確認方法)
5. [使用方法](#使用方法)
6. [トラブルシューティング](#トラブルシューティング)

---

## システム概要

### 目的
Q CLI Chat中の重要ツール実行時に作業原則を適用し、品質重視の作業を徹底する。

### 実装方式
**システムプロンプト + preToolUse Hook** の2層構造

1. **システムプロンプト**: 作業原則の内在化（Q CLI起動時）
2. **preToolUse Hook**: 重要ツール実行時の確認メッセージ

### 対象ツール
- `fs_write` - ファイル作成・編集
- `execute_bash` - コマンド実行
- `use_aws` - AWS操作

### 動作フロー
```
Q CLI起動
    ↓
システムプロンプト適用（作業原則の内在化）
    ↓
重要ツール実行時（fs_write, execute_bash, use_aws）
    ↓
カウンター+1（実行回数管理）
    ↓
20回毎？ → Yes: システムプロンプト全内容再表示
    ↓
preToolUse Hook実行（確認メッセージ表示）
    ↓
ツール実行継続
```

### 特徴
- ✅ **システムプロンプト統合**: Q CLI標準機能を活用
- ✅ **非インタラクティブ**: バックグラウンド動作
- ✅ **軽量**: 平均0.08秒で高速動作
- ✅ **選択的**: 重要ツールのみ対象
- ✅ **保守性**: シンプルな構成で管理容易
- ✅ **忘却防止**: 20回毎のシステムプロンプト再表示
- ✅ **持続性**: 長時間使用時の効果維持

---

## システム構成

### 1. システムプロンプト

**ファイルパス**: `~/.amazonq/rules/system-prompt.md`

**役割**: Q CLI起動時に作業原則を内在化

**内容例**:
```markdown
# Q CLI作業原則システムプロンプト

あなたは以下の作業原則に厳格に従って作業します：

## 作業原則

### 1. 検証の徹底
- **推測禁止**: 「たぶん」「おそらく」などの推測表現を使わない
- **ソースコード確認**: 実装に関する質問では必ずソースコードを確認する
- **実装検証**: 設定例や手順は実際に動作することを確認する

### 2. 品質優先
- **時間制約無視**: 「時間がない」「急いで」などの理由で品質を下げない
- **完全性追求**: 中途半端な回答を避け、必要な情報をすべて提供する
- **正確性重視**: 不正確な情報よりも「調査が必要」と回答する

### 3. 実証主義
- **調査優先**: 不明な点は推測せず、必要なツールを使って調査する
- **動作確認**: 提供する手順やコードは実際に実行して確認する
- **証拠提示**: 回答の根拠となるソースコードや実行結果を示す

### 4. 継続的改善
- **学習姿勢**: 新しい情報や実装変更を積極的に取り入れる
- **フィードバック活用**: 実行結果から学び、より良い回答を提供する
- **品質向上**: 常により正確で実用的な情報提供を目指す

## 実行指針

これらの原則に従い、以下を実行してください：

1. **必ず検証**: 回答前に関連するソースコードやドキュメントを確認
2. **実証重視**: 提供する手順は実際に動作することを確認
3. **完全回答**: 部分的な回答ではなく、完全で実用的な情報を提供
4. **品質保証**: 時間よりも正確性と完全性を優先

この作業原則に従って、高品質で信頼性の高い作業を実行してください。
```

### 2. Agent Hook設定

**ファイルパス**: `~/.aws/amazonq/cli-agents/default.json`

**Hook設定**:
```json
{
  "name": "default",
  "description": "Default client agent set",
  "prompt": "file:///home/katoh/.amazonq/rules/system-prompt.md",
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "fs_write"
      },
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "execute_bash"
      },
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "use_aws"
      }
    ]
  }
}
```

### 3. Hook スクリプト

**ファイルパス**: `~/.local/bin/smart-work-principles-check`

**内容**:
```bash
#!/bin/bash

# 環境変数から情報取得
TOOL_NAME="$Q_HOOK_TOOL_NAME"
TRIGGER="$Q_HOOK_TRIGGER"
INTERACTION_COUNT_FILE="$HOME/.amazonq/.interaction-count"
REAPPLY_THRESHOLD=20  # 20回のツール実行後

# インタラクション回数をカウント
CURRENT_COUNT=$(cat "$INTERACTION_COUNT_FILE" 2>/dev/null || echo 0)
NEW_COUNT=$((CURRENT_COUNT + 1))
echo "$NEW_COUNT" > "$INTERACTION_COUNT_FILE"

# 閾値に達したら再適用
if [ $((NEW_COUNT % REAPPLY_THRESHOLD)) -eq 0 ]; then
    echo "🔄 作業原則リマインダー（${REAPPLY_THRESHOLD}回目のツール実行）:"
    cat "$HOME/.amazonq/rules/system-prompt.md"
    echo ""
fi

echo "🔍 作業原則適用中: $TOOL_NAME 実行前チェック完了"
```

**権限**: 実行可能 (`chmod +x`)

### 4. ファイル一覧

| ファイル | 役割 | サイズ | 権限 |
|---------|------|--------|------|
| `~/.amazonq/rules/system-prompt.md` | システムプロンプト | ~1.6KB | 644 |
| `~/.aws/amazonq/cli-agents/default.json` | Agent設定 | ~8KB | 644 |
| `~/.local/bin/smart-work-principles-check` | Hook スクリプト | ~800B | 755 |
| `~/.amazonq/.interaction-count` | ツール実行回数管理 | ~10B | 644 |

---

## セットアップ手順

### 前提条件

- Q CLI v1.19.0以降
- Agent設定ファイルへの書き込み権限
- `~/.local/bin`ディレクトリの作成権限

### ステップ1: 現在の設定確認

```bash
# Agent設定の確認
jq '.prompt' ~/.aws/amazonq/cli-agents/default.json

# 期待される出力: システムプロンプトのパス
# "file:///home/user/.amazonq/rules/system-prompt.md"
```

### ステップ2: Hook スクリプト作成

```bash
# ディレクトリ作成
mkdir -p ~/.local/bin

# スクリプト作成
cat > ~/.local/bin/smart-work-principles-check << 'EOF'
#!/bin/bash

# 環境変数から情報取得
TOOL_NAME="$Q_HOOK_TOOL_NAME"
TRIGGER="$Q_HOOK_TRIGGER"
INTERACTION_COUNT_FILE="$HOME/.amazonq/.interaction-count"
REAPPLY_THRESHOLD=20  # 20回のツール実行後

# インタラクション回数をカウント
CURRENT_COUNT=$(cat "$INTERACTION_COUNT_FILE" 2>/dev/null || echo 0)
NEW_COUNT=$((CURRENT_COUNT + 1))
echo "$NEW_COUNT" > "$INTERACTION_COUNT_FILE"

# 閾値に達したら再適用
if [ $((NEW_COUNT % REAPPLY_THRESHOLD)) -eq 0 ]; then
    echo "🔄 作業原則リマインダー（${REAPPLY_THRESHOLD}回目のツール実行）:"
    cat "$HOME/.amazonq/rules/system-prompt.md"
    echo ""
fi

echo "🔍 作業原則適用中: $TOOL_NAME 実行前チェック完了"
EOF

# 実行権限付与
chmod +x ~/.local/bin/smart-work-principles-check
```

### ステップ3: Agent設定の更新

**重要**: Agent設定ファイルを直接編集してください。

```bash
# バックアップ作成
cp ~/.aws/amazonq/cli-agents/default.json ~/.aws/amazonq/cli-agents/default.json.backup

# 設定ファイルを編集（手動）
# hooks.preToolUse セクションを追加
```

**追加する設定**:
```json
{
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "fs_write"
      },
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "execute_bash"
      },
      {
        "command": "~/.local/bin/smart-work-principles-check",
        "matcher": "use_aws"
      }
    ]
  }
}
```

### ステップ4: Q CLI再起動

```bash
# 既存セッション終了
pkill -f qchat

# 新しいセッション開始
q chat
```

---

## 稼働確認方法

### 方法1: Hook設定確認

```bash
# Hook設定の確認
jq '.hooks.preToolUse' ~/.aws/amazonq/cli-agents/default.json

# 期待される出力:
# [
#   {
#     "command": "~/.local/bin/smart-work-principles-check",
#     "matcher": "fs_write"
#   },
#   ...
# ]
```

### 方法2: スクリプト動作確認

```bash
# 環境変数を設定して手動実行テスト
Q_HOOK_TOOL_NAME="fs_write" Q_HOOK_TRIGGER="preToolUse" ~/.local/bin/smart-work-principles-check

# 期待される出力:
# 🔍 作業原則適用中: fs_write 実行前チェック完了
```

### 方法3: 実際のツール実行確認

```bash
# Q CLI chatを起動
q chat

# Chat中でファイル作成を依頼
# 「テストファイルを作成して」

# 期待される動作:
# ✓ 3 of 3 hooks finished in 0.08 s
# 🔍 作業原則適用中: fs_write 実行前チェック完了
```

---

## 使用方法

### 通常のChat使用

```bash
# Q CLIを起動
q chat

# 通常通りChat使用
# 重要ツール実行時に自動的に確認メッセージが表示される
```

### Hook実行時の表示例

#### 通常時（1-19回目）
```
✓ 3 of 3 hooks finished in 0.08 s
🔍 作業原則適用中: fs_write 実行前チェック完了

[ツール実行継続]
```

#### 20回毎のリマインダー表示
```
✓ 3 of 3 hooks finished in 0.08 s
🔄 作業原則リマインダー（20回目のツール実行）:
# Q CLI作業原則システムプロンプト

あなたは以下の作業原則に厳格に従って作業します：
[システムプロンプト全内容が表示]

🔍 作業原則適用中: fs_write 実行前チェック完了

[ツール実行継続]
```

### システムプロンプトの効果

- 推測表現の回避
- ソースコード確認の徹底
- 実装検証の実施
- 品質重視の作業継続

### システムプロンプト再適用機能

- **20回毎のリマインダー**: ツール実行20回毎にシステムプロンプト全内容を再表示
- **忘却防止**: 長時間使用やコンパクション後の効果維持
- **カウンター管理**: `~/.amazonq/.interaction-count`で実行回数を管理
- **自動リセット**: 20の倍数で自動的にリマインダー実行

---

## トラブルシューティング

### 問題1: Hook設定が動作しない

**症状**:
```
Chat中でツール実行時に確認メッセージが表示されない
```

**原因**: Agent設定のhooksセクションが正しく設定されていない

**解決策**:
```bash
# 設定確認
jq '.hooks.preToolUse' ~/.aws/amazonq/cli-agents/default.json

# 設定が空の場合は手動で追加
# Agent設定ファイルを直接編集
```

### 問題2: スクリプト実行権限エラー

**症状**:
```
bash: /home/user/.local/bin/smart-work-principles-check: Permission denied
```

**原因**: スクリプトに実行権限がない

**解決策**:
```bash
chmod +x ~/.local/bin/smart-work-principles-check
```

### 問題3: システムプロンプトが適用されない

**症状**:
```
作業原則が適用されていない動作
```

**原因**: Agent設定でpromptが指定されていない

**解決策**:
```bash
# prompt設定の確認
jq '.prompt' ~/.aws/amazonq/cli-agents/default.json

# 設定されていない場合は追加
# "prompt": "file:///home/user/.amazonq/rules/system-prompt.md"
```

---

## まとめ

### システムの利点

- ✅ **システムプロンプト統合**: Q CLI標準機能を活用
- ✅ **非インタラクティブ**: バックグラウンド動作
- ✅ **軽量**: 平均0.08秒で高速動作
- ✅ **選択的**: 重要ツールのみ対象
- ✅ **保守性**: シンプルな構成で管理容易

### 動作確認済み環境

- **OS**: Ubuntu 24.04.3 LTS (WSL2)
- **Q CLI**: v1.19.0
- **実装日**: 2025-10-27
- **最終動作確認**: 2025-10-28 02:35

### ファイル一覧

1. `~/.amazonq/rules/system-prompt.md` - システムプロンプト
2. `~/.aws/amazonq/cli-agents/default.json` - Agent設定（preToolUse hooks追加）
3. `~/.local/bin/smart-work-principles-check` - Hook スクリプト

---

**作成者**: Amazon Q Developer CLI  
**作成日時**: 2025-10-28 00:23 JST  
**更新日時**: 2025-10-28 02:48 JST  
**ステータス**: ✅ 実装完了・動作確認済み（システムプロンプト再適用機能追加）
