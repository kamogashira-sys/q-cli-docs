# Kiro CLI 変更履歴（Changelog）

このページでは、Kiro CLI（旧Amazon Q Developer CLI）の主要なバージョンアップデートと変更内容を記録しています。

## 📋 目次

- [最新バージョン](#最新バージョン)
- [バージョン履歴](#バージョン履歴)
- [変更カテゴリについて](#変更カテゴリについて)
- [移行情報](#移行情報)

---

## 最新バージョン

### v1.24.0 CLI（2026-01-16）

**主要な変更**:
- 📚 **Skills**: 大規模ドキュメント向けの段階的コンテキストロード機能
  - メタデータのみ起動時ロード、本文はオンデマンド
  - YAMLフロントマター（name、description）必須
  - `skill://` URIスキームでリソース指定
- 🎨 **Custom Diff Tools**: 外部Diffツール統合機能
  - delta、difftastic、VS Code等15種類のツール対応
  - `chat.diffTool`設定で選択可能
  - ターミナルツール8種類、GUIツール7種類をサポート
- 🔍 **AST Pattern Tools**: 構文木ベースのコード検索・変換ツール
  - **pattern-search**: 構文構造を理解した精密な検索
  - **pattern-rewrite**: ASTパターンによる安全なコード変換
  - 文字列リテラル・コメント内の誤検出を排除
- 🧠 **Improved Code Intelligence**: 18言語で組み込みコード理解機能
  - LSPセットアップ不要で即座に利用開始
  - `/code overview`コマンドで完全なワークスペース概要取得
  - `--silent`オプションでクリーンな出力
  - Bash, C, C++, C#, Elixir, Go, Java, JavaScript, Kotlin, Lua, PHP, Python, Ruby, Rust, Scala, Swift, TSX, TypeScript対応
- 📦 **Conversation Compaction**: 会話履歴の圧縮機能
  - `/compact`コマンドで手動実行
  - コンテキストウィンドウオーバーフロー時に自動実行
  - `compaction.excludeMessages`、`compaction.excludeContextWindowPercent`で設定可能
  - 新セッション作成、`/chat resume`で元のセッションに復帰可能
- 🔒 **Granular URL Permissions**: web_fetchツールのURL権限細粒度制御
  - 正規表現パターンで信頼ドメイン自動許可
  - ブロックパターンで特定サイト遮断
  - 信頼パターン外のURLは承認プロンプト表示
- 🌐 **Remote Authentication**: リモートマシンでのGoogle/GitHub認証対応
  - SSH、SSM、コンテナ環境でポートフォワーディング対応
  - Builder ID、IAM Identity Centerはデバイスコード認証標準対応

**詳細**: [Kiro CLI v1.24.0 Changelog](https://kiro.dev/changelog/cli/1-24/)

---

### v1.23.1 CLI（2025-12-23）

**主要な変更**:
- 🔧 **Grep/Glob Tools改善**: 実行詳細情報の追加
- 🛡️ **Subagent Security**: デフォルトエージェントでのsubagentツールを非信頼に変更
- 🐛 **Plan Agent修正**: 書き込みツールアクセスを削除
- 🔧 **コマンド改善**: /save、/loadコマンドの非推奨警告でパラメータ受け入れを修正
- 🐛 **MCP表示修正**: 無効化されたMCPサーバーが初期化中として表示される問題を修正
- 🐛 **MCP Tool名解析**: メインチャットとsubagent間でのMCPツール名解析の不整合を修正

**詳細**: [Kiro CLI v1.23.1 Changelog](https://kiro.dev/changelog/)

---

### v1.23.0 CLI（2025-12-18）

**主要な変更**:
- 🎉 **Subagents**: 複雑なタスクを専門エージェントに委譲、ライブ進捗追跡機能
- 🧠 **Plan Agent**: アイデアを構造化された実装計画に変換（Shift + Tab または /plan コマンド）
- 🔍 **Grep/Glob Tools**: 高速ファイル検索ツール（.gitignore対応）
- 💬 **Multi-Session Support**: 複数チャットセッション管理機能
- 🔌 **MCP Registry Support**: MCPツールのガバナンス機能
- 🤖 **Default Agent Prompt**: Kiro CLI機能をハイライトするデフォルトエージェントプロンプト
- ⚙️ **Model Persistence**: /model set-current-as-defaultコマンドでモデル選択を永続化
- 🚀 **LSP Performance**: Code Intelligenceツールの読み込み時間改善

**詳細**: [Kiro CLI v1.23.0 Changelog](https://kiro.dev/changelog/subagents-plan-agent-grep-glob-tools-and-mcp-registry/)

---

## バージョン履歴

### v1.22.0 CLI（2025-12-11）

**主要な変更**:
- 🧠 **Code Intelligence**: Language Server Protocol (LSP)統合による高精度コード理解機能
  - **Go-to-definition**: 関数・変数の定義箇所への即座のジャンプ
  - **Find references**: シンボルの使用箇所を全コードベースから検索
  - **Hover情報**: カーソル位置での詳細情報表示
  - **Diagnostics**: リアルタイムエラー・警告検出
  - **Kiro IDEとの統合**: IDEと同等のコード理解機能をCLIで提供
  - **コンテキスト認識**: より正確なコードナビゲーション・リファクタリング提案

- 📚 **Knowledge Index**: Agent設定での知識ベース構成と自動インデックス化
  - **カスタム知識ソース**: Agent設定でドメイン固有の知識源を定義
  - **自動同期**: コードベースとの自動同期でコンテキストを最新状態に維持
  - **ドメイン固有コンテキスト**: プロジェクト特有の知識を自動的に提供
  - **Agent Schema Configuration**: 知識ベースの構造化設定

- 🔧 **Enhanced Auto-compaction**: 長い会話の自動要約機能強化
  - **コンテキスト管理**: 会話履歴の効率的な圧縮
  - **メモリ最適化**: 重要な情報を保持しながら容量削減

- 🛡️ **Improved Guardrails**: ファイル読み取りの安全性向上
  - **アクセス制御**: ファイル操作の権限管理強化
  - **セキュリティ**: 不正なファイルアクセスの防止

**詳細**: [Code Intelligence and Knowledge Index](https://kiro.dev/changelog/code-intelligence-and-knowledge-index/)

---

### v1.21.0 CLI（2025-11-25）

**主要な変更**:
- 🌐 **Web Search & Fetch**: リアルタイムインターネット情報アクセス機能
  - **Web検索**: 最新ドキュメント・技術情報の即座検索
  - **コンテンツ取得**: URLからの直接コンテンツフェッチ
  - **ライブラリ情報**: 最新バージョン・リリース情報の取得
  - **技術問題解決**: Stack Overflow、GitHub Issues等からの解決策リサーチ
  - **ワークフロー統合**: ブラウザ切り替え不要の開発環境

- 🔧 **Built-in Tools拡張**: Web関連ツールの標準搭載
  - **web_search**: キーワードベースのWeb検索ツール
  - **web_fetch**: URL指定でのコンテンツ取得ツール
  - **開発効率化**: 情報収集からコード実装まで一元化

- 📊 **Real-time Information**: 動的情報への即座アクセス
  - **API仕様**: 最新のAPI仕様・変更点の確認
  - **ベストプラクティス**: 最新の開発手法・パターンの取得
  - **エラー解決**: リアルタイムでのエラー情報・解決策検索

**詳細**: [Web Search and Fetch for Kiro CLI](https://kiro.dev/changelog/web-search-and-fetch-for-kiro-cli/)

---

### v1.20.2 CLI（2025-11-25）

**主要な変更**:
- 🔧 **Context Management改善**: コンテキスト管理機能の向上
  - 会話履歴の効率的な管理
  - プロジェクト固有のコンテキスト保持
- 📝 **TODO Lists強化**: タスク管理機能の改善
  - タスクの構造化
  - 進捗追跡の向上
- 🐛 **バグ修正**: 安定性向上のための修正

**詳細**: [Improvements to Context Management and Todo Lists](https://kiro.dev/changelog/improvements-to-context-management-and-todo-lists/)

---

### v1.20.1 CLI（2025-11-24）

**主要な変更**:
- 🔧 **Agent修正**: Agent機能の安定性向上
  - カスタムエージェントの動作改善
  - エージェント切り替えの安定化
- 🔌 **MCP with Workspaces**: ワークスペース対応MCP機能の修正
  - マルチルートワークスペースでのMCP動作改善
- 🎨 **Code Block Styling**: コードブロック表示の改善
  - 構文ハイライトの向上
  - 表示レイアウトの最適化

**詳細**: [Fixes for Agents, MCP with Workspaces, and Code Block Styling](https://kiro.dev/changelog/fixes-for-agents-mcp-with-workspaces-and-code-block-styling/)

---

### Kiro CLI初回リリース（2025-11-17）

**🎉 Kiro CLI誕生**:
- 🚀 **Amazon Q Developer CLIからの移行**: 既存技術基盤を継承
- 🤖 **Auto Agent**: パフォーマンス・効率・品質のバランス最適化
- 🔐 **Social Login**: ソーシャルログイン対応
- 🧠 **Claude Haiku 4.5**: 新モデル対応
- 🔧 **Agent Mode**: カスタムエージェント機能
- 🔌 **MCP Support**: Model Context Protocol統合
- 📝 **Steering Files**: プロジェクト固有の設定管理

**インストール**:
```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

**詳細**: [Introducing Kiro CLI](https://kiro.dev/blog/introducing-kiro-cli/)

---

## 変更カテゴリについて

| カテゴリ | 記号 | 説明 |
|----------|------|------|
| **新機能** | 🎉 | 新しい機能の追加や既存機能の大幅な拡張 |
| **改善** | 🔧 | 既存機能のパフォーマンス向上や使いやすさの改善 |
| **セキュリティ** | 🛡️ | セキュリティ関連の修正や強化 |
| **バグ修正** | 🐛 | 不具合の修正 |
| **AI機能** | 🧠 | AI・機械学習関連の新機能や改善 |
| **統合機能** | 🔌 | 外部ツール・サービスとの統合機能 |
| **Web機能** | 🌐 | Web関連の新機能（検索、フェッチ等） |

---

## 移行情報

### Amazon Q Developer CLI → Kiro CLI

#### 移行タイムライン
- **2025-11-17**: Amazon Q Developer CLI v1.19.7（最終版）リリース
- **2025-11-17**: Kiro CLI初回リリース発表
- **継続性**: 既存ワークフロー・購読は継続

#### 主要な変更点

**開発形態**:
- **旧**: オープンソース（MIT License）
- **新**: クローズドソース（AWS Intellectual Property License）

**技術継承**:
- ✅ Agent機能（カスタムエージェント、設定管理）
- ✅ MCP統合（Model Context Protocol）
- ✅ Steering Files（プロジェクト固有設定）
- ✅ 既存のワークフロー・コマンド体系

**新機能追加**:
- 🆕 Auto Agent（最適化されたデフォルトエージェント）
- 🆕 Social Login（ソーシャルログイン）
- 🆕 Claude Haiku 4.5対応
- 🆕 Web Search & Fetch機能
- 🆕 Code Intelligence（LSP統合）
- 🆕 Subagents（並列タスク実行）

#### 移行方法

**既存ユーザー**:
1. Amazon Q Developer CLI v1.19.7は継続利用可能
2. Kiro CLIへの移行は任意
3. 設定・ワークフローは基本的に互換性あり

**新規ユーザー**:
```bash
# Kiro CLI インストール
curl -fsSL https://cli.kiro.dev/install | bash

# 基本的な使用方法は同じ
kiro chat "Hello, world!"
```

---

## 📚 関連リンク

- [Kiro CLI公式サイト](https://kiro.dev/cli/) - 最新情報とドキュメント
- [Kiro CLI Changelog](https://kiro.dev/changelog/) - 公式変更履歴
- [GitHub Repository](https://github.com/kirodotdev/Kiro) - Issue報告・機能要望
- [Discord Community](https://discord.gg/kirodotdev) - コミュニティサポート
- [旧Amazon Q Developer CLI](https://github.com/aws/amazon-q-developer-cli) - 旧バージョン（OSS）

---

## 🔄 更新頻度

このChangelogは以下のタイミングで更新されます：
- 新しいバージョンのリリース時
- 重要な機能追加・変更時
- セキュリティアップデートのリリース時
- コミュニティからの重要なフィードバック時

**最終更新**: 2025-12-28（v1.23.1対応、全バージョン履歴更新）
