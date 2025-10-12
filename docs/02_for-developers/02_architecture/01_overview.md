# アーキテクチャ概要

**最終更新**: 2025-10-11

---

## 🏗️ システム構成

Amazon Q CLIは以下のコンポーネントで構成されています：

### 主要コンポーネント
1. **CLI Interface** - ユーザーインターフェース
2. **Chat Engine** - チャット処理エンジン
3. **Agent System** - Agent管理システム
4. **MCP Client** - MCPサーバー連携
5. **Knowledge Base** - ドキュメント検索
6. **Settings Manager** - 設定管理

---

## 🔄 データフロー

```
User Input → CLI → Chat Engine → Agent → Tools/MCP → Response
```

---

## 🛠️ 技術スタック

- **言語**: Rust
- **UI**: Ratatui（TUI）
- **プロトコル**: MCP
- **認証**: AWS Builder ID / IAM Identity Center

---

## 📚 詳細情報

- [ソースコード構造](03_source-code-structure.md)
- [設定システム詳細](02_configuration-system.md)

---

**作成日**: 2025-10-11
