[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [リファレンス](README.md) > 07 Context Window Limits

---

# コンテキストウィンドウ制限

**最終更新**: 2025-10-18

---

## 📋 概要

Q CLIのコンテキストウィンドウ制限と計算方法をまとめたリファレンスです。

---

## 🎯 基本制限

### コンテキストファイルの制限

**コンテキストファイルの合計サイズは、コンテキストウィンドウの75%まで**

これは、以下の理由によります：
- 残り25%は会話履歴、システムプロンプト、ツールレスポンスに使用
- バッファを確保することでコンテキストオーバーフローを防止

---

## 📊 モデル別計算例

### Claude Sonnet 4

| 項目 | 値 |
|------|------|
| 総コンテキストウィンドウ | 200,000トークン |
| コンテキストファイル上限 | **150,000トークン**（75%） |
| 会話・システム用 | 50,000トークン（25%） |

### GPT-4

| 項目 | 値 |
|------|------|
| 総コンテキストウィンドウ | 128,000トークン |
| コンテキストファイル上限 | **96,000トークン**（75%） |
| 会話・システム用 | 32,000トークン（25%） |

---

## 🔍 トークン数の確認方法

### 方法1: `q chat --list-context` コマンド

```bash
q chat --list-context
```

**出力例**:
```
👤 Agent (default):
    README.md (1 match)

💬 Session (temporary):
    /home/user/.amazonq/rules/default.md (1 match)

2 matched files in use:
💬 /home/user/.amazonq/rules/default.md (~400 tkns)
👤 /home/user/projects/myapp/README.md (~2620 tkns)

Total: ~3020 tokens
```

### 方法2: チャット中の確認

チャット中に以下のメッセージが表示されます：

```
Total tokens: 65000/80000 (81.25%)
```

---

## ⚠️ コンテキストオーバーフロー

### 症状

```
⚠️ Context limit exceeded!
```

### 原因

- 大量のコンテキストファイルを追加
- 長い会話を継続
- 大きなツールレスポンスが含まれる

### 対処方法

1. **コンテキストファイルを削減**
   ```bash
   # 不要なファイルを除外
   q chat --exclude "*.log" --exclude "dist/*"
   ```

2. **会話をリセット**
   ```bash
   # 新しいセッションを開始
   q chat
   ```

3. **自動要約を有効化**（デフォルトで有効）
   - 長い会話は自動的に要約される
   - 要約により古いメッセージが圧縮される

---

## 💡 ベストプラクティス

### 1. コンテキストファイルの最適化

- **必要最小限のファイルのみ追加**
- **大きなファイルは除外**（ログ、ビルド成果物等）
- **ワイルドカードで効率的に指定**

### 2. 定期的な確認

```bash
# 定期的にコンテキスト使用量を確認
q chat --list-context
```

### 3. Agent設定での制御

```yaml
# .amazonq/agent.yml
context:
  include:
    - "src/**/*.ts"
    - "README.md"
  exclude:
    - "**/*.log"
    - "dist/**"
    - "node_modules/**"
```

---

## 🔗 関連ドキュメント

- [FAQ](../06_troubleshooting/01_faq.md)
- [よくある問題と解決方法](../06_troubleshooting/02_common-issues.md)
- [コンテキスト管理ベストプラクティス](../08_guides/04_best-practices.md)
- [Agent設定ガイド](../03_configuration/04_agent-configuration.md)
