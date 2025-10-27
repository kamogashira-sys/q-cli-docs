[ホーム](../README.md) > [Meta](README.md) > 作業原則強制適用システム

---

# 作業原則強制適用システム 完全版

**作成日時**: 2025-10-28 00:23 JST  
**ステータス**: ✅ 動作確認済み

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
Q CLI起動時に作業原則を必ず確認させ、品質重視の作業を徹底する。

### 動作フロー
```
qコマンド実行
    ↓
エイリアス: q → q-with-principles
    ↓
作業原則を表示
    ↓
Enterキーで確認待機
    ↓
/usr/bin/q を実行
    ↓
Q CLI起動
```

### 特徴
- ✅ シンプルな構成（3ファイルのみ）
- ✅ 非侵襲的（既存設定を破壊しない）
- ✅ 確実な動作（エイリアス方式）
- ✅ 簡単な確認（専用スクリプト）

---

## システム構成

### 1. 作業原則テキストファイル

**ファイルパス**: `~/.amazonq/rules/work-principles-check.txt`

**内容**:
```
╔═══════════════════════════════════════════════════════════════╗
║                    作業原則の確認                              ║
╚═══════════════════════════════════════════════════════════════╝

以下の作業原則を必ず守ることを確認してください：

【絶対に守るべき3原則】

1. ⏱️  時間を考慮しない
   ❌ 「時間がないから省略」は禁止
   ✅ 品質が最優先、時間は二の次

2. ✅ すべて検証する
   ❌ 推測や思い込みで書かない
   ✅ ソースコードを確認する
   ✅ 実際に実行して確認する

3. 🔍 推測で書かない
   ❌ 「たぶんこうだろう」は禁止
   ✅ 実装を確認してから記述
   ✅ 不明な点は調査する

【確認事項】

□ 作業原則を読んだ
□ 作業原則を理解した
□ 作業原則を守ることを約束する

【違反時の対応】

作業原則に違反した場合：
1. 即座に作業を停止
2. 違反内容を記録
3. 修正計画を作成
4. 最初からやり直し

╔═══════════════════════════════════════════════════════════════╗
║  Enterキーを押すと、作業原則を守ることに同意したとみなします    ║
╚═══════════════════════════════════════════════════════════════╝
```

### 2. ラッパースクリプト

**ファイルパス**: `~/.local/bin/q-with-principles`

**内容**:
```bash
#!/bin/bash
cat ~/.amazonq/rules/work-principles-check.txt
read -p "Press Enter to confirm you have read and will follow the work principles..."
exec /usr/bin/q "$@"
```

**権限**: 実行可能 (`chmod +x`)

### 3. エイリアス設定

**ファイル**: `~/.bashrc`

**追加内容**:
```bash
# Q CLI with work principles enforcement
alias q='q-with-principles'
```

### 4. 稼働確認スクリプト（オプション）

**ファイルパス**: `~/.local/bin/check-work-principles`

**内容**:
```bash
#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        作業原則強制システム 稼働状況確認                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. 作業原則テキストファイル
echo "【1】作業原則テキストファイル"
if [ -f ~/.amazonq/rules/work-principles-check.txt ]; then
    echo "  ✅ 存在: ~/.amazonq/rules/work-principles-check.txt"
    wc -l ~/.amazonq/rules/work-principles-check.txt | awk '{print "  📄 行数: " $1}'
else
    echo "  ❌ 不在: ~/.amazonq/rules/work-principles-check.txt"
fi
echo ""

# 2. ラッパースクリプト
echo "【2】ラッパースクリプト"
if [ -f ~/.local/bin/q-with-principles ]; then
    echo "  ✅ 存在: ~/.local/bin/q-with-principles"
    if [ -x ~/.local/bin/q-with-principles ]; then
        echo "  ✅ 実行可能"
    else
        echo "  ❌ 実行不可"
    fi
else
    echo "  ❌ 不在: ~/.local/bin/q-with-principles"
fi
echo ""

# 3. エイリアス設定
echo "【3】エイリアス設定"
if grep -q "alias q='q-with-principles'" ~/.bashrc; then
    echo "  ✅ bashrcに設定済み"
else
    echo "  ❌ bashrcに未設定"
fi
echo ""

# 4. 現在のシェルでのエイリアス
echo "【4】現在のシェルでのエイリアス状態"
if alias q 2>/dev/null | grep -q "q-with-principles"; then
    echo "  ✅ エイリアス有効: $(alias q)"
else
    echo "  ❌ エイリアス無効"
    echo "  💡 対処: source ~/.bashrc または bash を実行"
fi
echo ""

# 5. qコマンドの実際のパス
echo "【5】qコマンドの実際のパス"
echo "  📍 $(which q)"
echo ""

# 6. Agent Hook設定
echo "【6】Agent Hook設定"
if grep -q '"hooks"' ~/.aws/amazonq/cli-agents/default.json 2>/dev/null; then
    echo "  ⚠️  Agent Hookが設定されています"
    echo "  💡 非対話的実行のため削除推奨"
else
    echo "  ✅ Agent Hook未設定（推奨状態）"
fi
echo ""

# 7. 動作テスト
echo "【7】動作テスト"
if echo '' | ~/.local/bin/q-with-principles --version 2>&1 | grep -q "q 1."; then
    echo "  ✅ スクリプトが正常に動作"
else
    echo "  ❌ スクリプトの動作に問題あり"
fi
echo ""

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    確認完了                                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
```

**権限**: 実行可能 (`chmod +x`)

---

## セットアップ手順

### ステップ1: ディレクトリ作成

```bash
mkdir -p ~/.amazonq/rules
mkdir -p ~/.local/bin
```

### ステップ2: 作業原則テキストファイル作成

```bash
cat > ~/.amazonq/rules/work-principles-check.txt << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                    作業原則の確認                              ║
╚═══════════════════════════════════════════════════════════════╝

以下の作業原則を必ず守ることを確認してください：

【絶対に守るべき3原則】

1. ⏱️  時間を考慮しない
   ❌ 「時間がないから省略」は禁止
   ✅ 品質が最優先、時間は二の次

2. ✅ すべて検証する
   ❌ 推測や思い込みで書かない
   ✅ ソースコードを確認する
   ✅ 実際に実行して確認する

3. 🔍 推測で書かない
   ❌ 「たぶんこうだろう」は禁止
   ✅ 実装を確認してから記述
   ✅ 不明な点は調査する

【確認事項】

□ 作業原則を読んだ
□ 作業原則を理解した
□ 作業原則を守ることを約束する

【違反時の対応】

作業原則に違反した場合：
1. 即座に作業を停止
2. 違反内容を記録
3. 修正計画を作成
4. 最初からやり直し

╔═══════════════════════════════════════════════════════════════╗
║  Enterキーを押すと、作業原則を守ることに同意したとみなします    ║
╚═══════════════════════════════════════════════════════════════╝
EOF
```

### ステップ3: ラッパースクリプト作成

```bash
cat > ~/.local/bin/q-with-principles << 'EOF'
#!/bin/bash
cat ~/.amazonq/rules/work-principles-check.txt
read -p "Press Enter to confirm you have read and will follow the work principles..."
exec /usr/bin/q "$@"
EOF

chmod +x ~/.local/bin/q-with-principles
```

### ステップ4: エイリアス設定

```bash
cat >> ~/.bashrc << 'EOF'

# Q CLI with work principles enforcement
alias q='q-with-principles'
EOF
```

### ステップ5: 稼働確認スクリプト作成（オプション）

```bash
cat > ~/.local/bin/check-work-principles << 'EOF'
#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        作業原則強制システム 稼働状況確認                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. 作業原則テキストファイル
echo "【1】作業原則テキストファイル"
if [ -f ~/.amazonq/rules/work-principles-check.txt ]; then
    echo "  ✅ 存在: ~/.amazonq/rules/work-principles-check.txt"
    wc -l ~/.amazonq/rules/work-principles-check.txt | awk '{print "  📄 行数: " $1}'
else
    echo "  ❌ 不在: ~/.amazonq/rules/work-principles-check.txt"
fi
echo ""

# 2. ラッパースクリプト
echo "【2】ラッパースクリプト"
if [ -f ~/.local/bin/q-with-principles ]; then
    echo "  ✅ 存在: ~/.local/bin/q-with-principles"
    if [ -x ~/.local/bin/q-with-principles ]; then
        echo "  ✅ 実行可能"
    else
        echo "  ❌ 実行不可"
    fi
else
    echo "  ❌ 不在: ~/.local/bin/q-with-principles"
fi
echo ""

# 3. エイリアス設定
echo "【3】エイリアス設定"
if grep -q "alias q='q-with-principles'" ~/.bashrc; then
    echo "  ✅ bashrcに設定済み"
else
    echo "  ❌ bashrcに未設定"
fi
echo ""

# 4. 現在のシェルでのエイリアス
echo "【4】現在のシェルでのエイリアス状態"
if alias q 2>/dev/null | grep -q "q-with-principles"; then
    echo "  ✅ エイリアス有効: $(alias q)"
else
    echo "  ❌ エイリアス無効"
    echo "  💡 対処: source ~/.bashrc または bash を実行"
fi
echo ""

# 5. qコマンドの実際のパス
echo "【5】qコマンドの実際のパス"
echo "  📍 $(which q)"
echo ""

# 6. Agent Hook設定
echo "【6】Agent Hook設定"
if grep -q '"hooks"' ~/.aws/amazonq/cli-agents/default.json 2>/dev/null; then
    echo "  ⚠️  Agent Hookが設定されています"
    echo "  💡 非対話的実行のため削除推奨"
else
    echo "  ✅ Agent Hook未設定（推奨状態）"
fi
echo ""

# 7. 動作テスト
echo "【7】動作テスト"
if echo '' | ~/.local/bin/q-with-principles --version 2>&1 | grep -q "q 1."; then
    echo "  ✅ スクリプトが正常に動作"
else
    echo "  ❌ スクリプトの動作に問題あり"
fi
echo ""

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    確認完了                                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
EOF

chmod +x ~/.local/bin/check-work-principles
```

### ステップ6: 設定を反映

```bash
# 新しいシェルを起動
bash

# または bashrc を再読み込み
source ~/.bashrc
```

---

## 稼働確認方法

### 方法1: 確認スクリプトを実行

```bash
check-work-principles
```

**期待される出力**:
```
╔═══════════════════════════════════════════════════════════════╗
║        作業原則強制システム 稼働状況確認                        ║
╚═══════════════════════════════════════════════════════════════╝

【1】作業原則テキストファイル
  ✅ 存在: ~/.amazonq/rules/work-principles-check.txt
  📄 行数: 39

【2】ラッパースクリプト
  ✅ 存在: ~/.local/bin/q-with-principles
  ✅ 実行可能

【3】エイリアス設定
  ✅ bashrcに設定済み

【4】現在のシェルでのエイリアス状態
  ✅ エイリアス有効: alias q='q-with-principles'

【5】qコマンドの実際のパス
  📍 /usr/bin/q

【6】Agent Hook設定
  ✅ Agent Hook未設定（推奨状態）

【7】動作テスト
  ✅ スクリプトが正常に動作

╔═══════════════════════════════════════════════════════════════╗
║                    確認完了                                    ║
╚═══════════════════════════════════════════════════════════════╝
```

### 方法2: 手動確認

#### エイリアスの確認
```bash
type q
```

**期待される出力**:
```
q is aliased to `q-with-principles'
```

#### 実際の動作確認
```bash
q --version
```

**期待される動作**:
1. 作業原則が表示される
2. "Press Enter to confirm..." と表示される
3. Enterキーを押すとQ CLIのバージョンが表示される

---

## 使用方法

### 通常の使用

```bash
# Q CLIを起動
q chat

# 作業原則が表示される
# Enterキーを押して確認
# Q CLIが起動
```

### すべてのqコマンドで動作

```bash
q --version      # バージョン確認
q chat           # チャット開始
q issue          # Issue報告
# すべてのqコマンドで作業原則が表示される
```

---

## トラブルシューティング

### 問題1: エイリアスが効かない

**症状**:
```bash
$ type q
q is /usr/bin/q
```

**原因**: bashrcが読み込まれていない

**解決策**:
```bash
# 新しいシェルを起動
bash

# または bashrc を再読み込み
source ~/.bashrc
```

### 問題2: スクリプトが実行できない

**症状**:
```
bash: /home/katoh/.local/bin/q-with-principles: Permission denied
```

**原因**: 実行権限がない

**解決策**:
```bash
chmod +x ~/.local/bin/q-with-principles
```

### 問題3: Agent Hookのエラー

**症状**:
```
✗ agentSpawn "cat ~/.amazonq/rules/work-principles-check.txt..." failed with exit code: 1
```

**原因**: Agent Hookが設定されている（非対話的実行のため失敗）

**解決策**: Agent Hook設定を削除
```bash
# default.jsonを編集
vim ~/.aws/amazonq/cli-agents/default.json

# "hooks" セクションを削除
```

---

## 重要な注意事項

### ✅ 推奨事項

1. **Agent Hookは使用しない**
   - Agent Hookは非対話的に実行されるため`read`コマンドが失敗する
   - エイリアス方式のみで十分機能する

2. **新しいシェルで確認**
   - エイリアスは既存のシェルには反映されない
   - `bash`コマンドで新しいシェルを起動して確認

3. **定期的な稼働確認**
   - `check-work-principles`で定期的に確認
   - すべての項目が✅であることを確認

### ❌ 避けるべき事項

1. **Agent Hookとの併用**
   - エラーの原因になる
   - エイリアス方式のみで運用

2. **スクリプトの直接編集**
   - 文字化けの原因になる
   - 再作成する場合は完全に削除してから作成

---

## まとめ

### システムの利点

- ✅ **シンプル**: 3ファイルのみの構成
- ✅ **確実**: エイリアス方式で確実に動作
- ✅ **非侵襲的**: 既存設定を破壊しない
- ✅ **検証可能**: 専用スクリプトで簡単に確認

### 動作確認済み環境

- **OS**: Ubuntu 24.04.3 LTS (WSL2)
- **Q CLI**: v1.19.0
- **Shell**: bash

### ファイル一覧

1. `~/.amazonq/rules/work-principles-check.txt` - 作業原則テキスト
2. `~/.local/bin/q-with-principles` - ラッパースクリプト
3. `~/.bashrc` - エイリアス設定
4. `~/.local/bin/check-work-principles` - 稼働確認スクリプト（オプション）

---

**作成者**: Amazon Q Developer CLI  
**作成日時**: 2025-10-28 00:23 JST  
**ステータス**: ✅ 動作確認済み
