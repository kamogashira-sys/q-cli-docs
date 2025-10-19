[ホーム](../../README.md) > [ユーザーガイド](../README.md) > [機能ガイド](README.md)

---

# 機能ガイド

**最終更新**: 2025-10-18

---

## 📋 このセクションについて

機能ガイドでは、Q CLIの各機能の使い方を詳しく説明します。

---

## 🚀 クイックアクセス

### よく使う情報

- **[クイックリファレンス](../07_reference/08_quick-reference.md)** ⭐ - よく使うコマンドと設定の早見表
- **[トピック別インデックス](../07_reference/09_topic-index.md)** ⭐ - やりたいことから適切なドキュメントを発見

---

## 📚 ドキュメント一覧

| # | 機能 | 対象ユーザー | 内容 |
|---|------|-------------|------|
| 1 | [チャット機能](01_chat.md) | 全レベル | チャット機能の詳細 |
| 2 | [Agent機能](02_agents.md) | 中級者以上 | Agent機能の詳細 |
| 3 | [オートコンプリート](03_autocomplete.md) | 全レベル | オートコンプリート機能 |
| 4 | [キーボードショートカット](04_keyboard-shortcuts.md) | 全レベル | ショートカット一覧と活用方法 |
| 5 | [Checkpoint機能](05_checkpoints.md) | 中級者以上 | Checkpoint機能の使い方 |
| 6 | [SSH/リモート](06_ssh-remote.md) | 中級者以上 | リモート環境での使用 |
| 7 | [実験的機能](07_experimental.md) | 上級者 | 実験的機能の紹介 |

---

## 🚀 推奨読み順

### 初めての方
1. **[チャット機能](01_chat.md)** - 基本を理解
2. **[キーボードショートカット](04_keyboard-shortcuts.md)** - 効率的な操作方法
3. **[Agent機能](02_agents.md)** - カスタマイズ方法を学習

### 中級者の方
1. **[Agent機能](02_agents.md)** - カスタマイズを深める
2. **[実験的機能](07_experimental.md)** - 高度な機能を活用

### 上級者の方
1. **[実験的機能](07_experimental.md)** - 最新機能を試す
2. **[SSH/リモート接続](06_ssh-remote.md)** - リモート環境での活用

### 機能関係図

```mermaid
graph LR
    Chat["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/01_chat.md'>チャット機能</a>"] --> Core[コア機能]
    Chat --> Exp["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/07_experimental.md'>実験的機能</a>"]
    Chat --> Agent["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/02_agents.md'>Agent機能</a>"]
    
    Core --> Keyboard["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/04_keyboard-shortcuts.md'>キーボードショートカット</a>"]
    Core --> Autocomplete["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/03_autocomplete.md'>オートコンプリート</a>"]
    Core --> Context["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/01_chat.md#%E3%82%B3%E3%83%B3%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E7%AE%A1%E7%90%86'>コンテキスト管理</a>"]
    
    Exp --> Knowledge["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/01_chat.md#knowledge%E7%AE%A1%E7%90%86'>Knowledge</a>"]
    Exp --> Checkpointing["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/05_checkpoints.md'>Checkpointing</a>"]
    Exp --> TodoLists["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/01_chat.md#todo%E7%AE%A1%E7%90%86'>TODO Lists</a>"]
    Exp --> Tangent["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/01_chat.md#%E4%BC%9A%E8%A9%B1%E7%AE%A1%E7%90%86'>Tangent Mode</a>"]
    Exp --> Thinking["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/07_experimental.md#-thinking%E6%80%9D%E8%80%83%E9%81%8E%E7%A8%8B%E8%A1%A8%E7%A4%BA'>Thinking</a>"]
    Exp --> Delegate["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/07_experimental.md#-delegatev1180'>Delegate</a>"]
    Exp --> ContextUsage["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/08_guides/04_best-practices.md#%E6%89%8B%E9%A0%861-context-usage-indicator-%E3%81%A7%E5%B8%B8%E6%99%82%E7%9B%A3%E8%A6%96%E6%8E%A8%E5%A5%A8'>Context Usage Percentage</a>"]
    
    Agent --> SSH["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/02_features/06_ssh-remote.md'>SSH/リモート接続</a>"]
    Agent --> MCP["<a href='https://github.com/kamogashira-sys/q-cli-docs/blob/main/docs/01_for-users/03_configuration/06_mcp-configuration.md'>MCP統合</a>"]
    
    style Exp fill:#fff3cd
    style Knowledge fill:#e3f2fd
    style Tangent fill:#e3f2fd
    style Thinking fill:#e3f2fd
    style Delegate fill:#e3f2fd
    style ContextUsage fill:#e3f2fd
```

**凡例**:
- **コア機能**: 常に利用可能な基本機能
- **実験的機能**: 設定で有効化が必要な機能（黄色背景）
- **Agent機能**: Agent設定に依存する機能

**注**: MCPサーバーの詳細は[MCP設定ガイド](../03_configuration/06_mcp-configuration.md)、実験的機能の詳細は[実験的機能ガイド](07_experimental.md)を参照してください。

---

**作成日**: 2025-10-11
