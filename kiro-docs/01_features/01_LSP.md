# Kiro CLI LSP統合機能（Code Intelligence）

**出典**: [Kiro CLI のコード理解が進化？ LSP 統合がもたらす新しい開発体験](https://zenn.dev/aws_japan/articles/bca7fdc3a15f46) - Zenn記事 by konippi

## 概要

Kiro CLI v1.22.0（2025年12月11日リリース）で追加されたLSP（Language Server Protocol）統合機能について詳細に解説します。この機能により、Kiro CLIがコードの構造や意味を理解し、IDE のような高度なコード操作を自然言語で実行できるようになりました。

## 📋 Zenn記事の詳細内容確認

### v1.22.0のLSP統合（Code Intelligence機能）の詳細

#### 主要な機能・特徴

1. **Code Intelligence機能の本質**
   - LSPを通じてコードのセマンティック（意味的）理解を実現
   - 単なるテキスト検索ではなく、クラス・関数・変数などのシンボルを正確に識別
   - コードの構造・型・関係性を理解した上での操作が可能

2. **LSP統合によるメリット**
   - **コードの「意味」理解**: 確率的生成から構造的理解への進化
   - **リアルタイムフィードバック**: IDEのようなリアルタイム診断情報
   - **コンテキスト最適化**: 必要な情報への直接アクセスでトークン消費削減

3. **セットアップ手順**
   - Language Serverの事前インストールが必要
   - `/code init`コマンドでプロジェクト単位の初期化
   - `.kiro/settings/lsp.json`設定ファイルの自動生成

4. **対応言語（7言語）**
   - TypeScript/JavaScript (typescript-language-server)
   - Rust (rust-analyzer)
   - Python (pyright)
   - Go (gopls)
   - Java (jdtls)
   - Ruby (solargraph)
   - C/C++ (clangd)

5. **カスタム言語サポート**
   - `.kiro/settings/lsp.json`の設定で他言語追加可能
   - PHP (intelephense)の追加例も記載
   - 独自Language Serverの設定方法も詳細に説明

6. **具体的なユースケース**
   - **シンボル検索**: `useToast 関数はどこで定義されていますか？`
   - **参照検索**: `Person クラスの参照を探して`
   - **定義ジャンプ**: `UserService の定義を教えて`
   - **シンボル一覧**: `auth.service.ts にはどんなシンボルがある？`
   - **診断情報**: `main.ts の診断情報を教えて`

7. **効果的な使い方のポイント**
   - プロジェクトルートでの初期化必須
   - 具体的な検索語の使用で精度向上
   - リネーム前の影響範囲確認
   - 診断情報の優先確認

## セットアップ詳細

### 1. Language Serverのインストール

使用したい言語のLanguage Serverを事前にインストールする必要があります。

例：TypeScriptの場合
```bash
npm install -g typescript-language-server typescript
```

### 2. Code Intelligenceの初期化

プロジェクトルートで以下のコマンドを実行：
```bash
/code init
```

このコマンドは以下を実行します：
1. `.kiro/settings/lsp.json`設定ファイルを生成
2. プロジェクト内の言語を自動検出
3. インストール済みのLanguage Serverを起動

### 3. ステータス確認

初期化後のステータス表示：
- ✓ : 初期化完了、使用可能
- ◐ : 初期化中
- ○ available : インストール済みだが、プロジェクトで未使用
- ○ not installed : 未インストール

## 対応言語とインストールコマンド

| 言語 | 拡張子 | Language Server | インストールコマンド |
|------|--------|-----------------|---------------------|
| TypeScript/JavaScript | .ts, .js, .tsx, .jsx | typescript-language-server | `npm install -g typescript-language-server typescript` |
| Rust | .rs | rust-analyzer | `rustup component add rust-analyzer` |
| Python | .py | pyright | `npm install -g pyright` または `pip install pyright` |
| Go | .go | gopls | `go install golang.org/x/tools/gopls@latest` |
| Java | .java | jdtls | `brew install jdtls` (macOS) |
| Ruby | .rb | solargraph | `gem install solargraph` |
| C/C++ | .c, .cpp, .h, .hpp | clangd | `brew install llvm` (macOS) または `apt install clangd` (Linux) |

## カスタム言語の追加

### PHP Language Serverの追加例

1. PHP Language Serverをインストール：
```bash
npm install -g intelephense
```

2. `.kiro/settings/lsp.json`に設定を追加：
```json
{
  "languages": {
    "php": {
      "name": "intelephense",
      "command": "intelephense",
      "args": ["--stdio"],
      "file_extensions": ["php"],
      "project_patterns": ["composer.json"],
      "exclude_patterns": ["**/vendor/**"],
      "multi_workspace": false,
      "initialization_options": {},
      "request_timeout_secs": 60
    }
  }
}
```

### 設定項目の説明

- **name**: Language Serverの表示名
- **command**: 実行するバイナリ/コマンド
- **args**: コマンドライン引数（通常は ["--stdio"]）
- **file_extensions**: 対応するファイル拡張子
- **project_patterns**: プロジェクトルートを示すファイル（例: package.json）
- **exclude_patterns**: 解析から除外するGlobパターン
- **multi_workspace**: 複数ワークスペースフォルダのサポート（デフォルト: false）
- **initialization_options**: LSP固有の初期化設定
- **request_timeout_secs**: LSPリクエストのタイムアウト秒数（デフォルト: 60）

## 実用的なユースケース

### シンボル検索
```
> useToast 関数はどこで定義されていますか？
```

出力例：
```
Searching for symbols matching: "useToast" (using tool: code) - Completed in 0.0s

> useToast 関数は ec-site/src/utils/useToast.ts で定義されています。

この関数は、トースト通知を管理するカスタムフックで、以下を提供します:
- toast: 現在のトースト状態（メッセージとタイプ）
- showToast: トーストを表示する関数
- hideToast: トーストを非表示にする関数
```

### 参照検索
```
> Person クラスの参照を探して
```

出力例：
```
Finding all references at: auth.ts:42:10

  1. src/auth.ts:42:10 - export function authenticate(...)
  2. src/handlers/login.ts:15:5 - authenticate(credentials)
  3. src/handlers/api.ts:89:12 - await authenticate(token)
  (3 more items found)
```

### 定義ジャンプ
```
> UserService の定義を教えて
```

出力例：
```
src/services/user.service.ts:42:1: export class UserService { ...
```

### 診断情報の取得
```
> main.ts の診断情報を教えて
```

出力例：
```
  1. Error line 15:10: Cannot find name 'undefined_var'
  2. Warning line 42:5: 'result' is declared but never used
```

## 効果的な使い方

### ベストプラクティス

1. **プロジェクトルートで初期化**
   - `/code init`は必ずプロジェクトルートで実行

2. **具体的な検索語を使用**
   - 良い例: "UserService"
   - 悪い例: "user"

3. **リネーム前の確認**
   - ファイル横断のリネームを実行する前に影響範囲を確認

4. **診断情報の優先確認**
   - シンボルが見つからない場合、まず診断情報を確認

### 無効化方法

LSP統合を無効化したい場合：
1. `.kiro/settings/lsp.json`を削除
2. セッションを再起動

## まとめ

Kiro CLI v1.22.0のLSP統合機能は、コーディングエージェントの根本的な能力向上を実現する重要なアップデートです。単なるテキスト検索から、コードの意味を理解した構造的な操作への進化により、開発効率が大幅に向上します。

この機能により、Kiro CLIは：
- IDEレベルのコード理解能力を獲得
- トークン消費の最適化を実現
- リアルタイムフィードバックによる開発体験向上

を提供し、AI駆動開発の新しい標準を確立しています。
