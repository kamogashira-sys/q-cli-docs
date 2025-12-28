# アップデート情報

## 📋 機能概要

Kiro CLIの主要機能は以下の5つのカテゴリに分類されます：

### 1. [LSP統合機能（Code Intelligence）](01_LSP.md)
- **リリース**: v1.22.0（2025-12-11）
- **概要**: Language Server Protocol統合による高精度コード理解
- **主要機能**: Go-to-definition、Find references、Hover情報、Diagnostics

### 2. [サブエージェント機能（Subagents）](02_Subagents.md)
- **リリース**: v1.23.0（2025-12-18）
- **概要**: 複雑なタスクを専門エージェントに委譲し並列実行
- **主要機能**: 自律実行、リアルタイム進捗追跡、結果の自動集約

### 3. [Planエージェント機能（Plan Agent）](03_PlanAgent.md)
- **リリース**: v1.23.0（2025-12-18）
- **概要**: アイデアを構造化された実装計画に変換
- **主要機能**: 要件収集、リサーチ分析、実装計画作成、計画引き継ぎ

### 4. [マルチセッション機能（Multi-Session Support）](04_MultiSession.md)
- **リリース**: v1.23.0（2025-12-18）
- **概要**: 複数のチャットセッションを効率的に管理
- **主要機能**: セッションピッカー、自動保存、ディレクトリベース管理

### 5. [Grep/Globツール機能（Grep/Glob Tools）](05_GrepGlob.md)
- **リリース**: v1.23.0（2025-12-18）
- **概要**: 高速なファイル検索を実現する2つのビルトインツール
- **主要機能**: 正規表現検索、Globパターン検索、.gitignore自動尊重

## 🔄 機能間の相関図

```mermaid
graph TB
    subgraph "Kiro CLI v1.22.0+"
        LSP[LSP統合機能<br/>Code Intelligence<br/>v1.22.0]
    end
    
    subgraph "Kiro CLI v1.23.0"
        Plan[Planエージェント<br/>Plan Agent<br/>v1.23.0]
        Sub[サブエージェント<br/>Subagents<br/>v1.23.0]
        Multi[マルチセッション<br/>Multi-Session<br/>v1.23.0]
        Grep[Grep/Globツール<br/>Search Tools<br/>v1.23.0]
    end
    
    subgraph "開発ワークフロー"
        Planning[計画立案]
        Implementation[実装]
        Management[管理]
    end
    
    %% 機能間の関係
    Plan --> Sub
    Plan --> LSP
    Sub --> LSP
    Sub --> Grep
    LSP --> Grep
    
    %% ワークフローとの関係
    Plan --> Planning
    Sub --> Implementation
    LSP --> Implementation
    Grep --> Implementation
    Multi --> Management
    
    %% スタイル
    classDef v122 fill:#e1f5fe
    classDef v123 fill:#f3e5f5
    classDef workflow fill:#fff3e0
    
    class LSP v122
    class Plan,Sub,Multi,Grep v123
    class Planning,Implementation,Management workflow
```

## 🔗 機能間の連携

### 計画から実装への流れ
1. **Planエージェント**で要件を整理し実装計画を作成
2. **サブエージェント**で並列実装を実行
3. **LSP統合**で高精度なコード理解を活用
4. **Grep/Globツール**で効率的なコード探索

### セッション管理
- **マルチセッション機能**で全ての作業履歴を管理
- プロジェクトごとの独立したセッション保持
- 重要な計画や実装過程の永続化

## 📈 バージョン別進化

### v1.22.0（2025-12-11）
- **LSP統合機能**の追加
- コード理解能力の飛躍的向上
- IDEレベルの開発支援機能

### v1.23.0（2025-12-18）
- **4つの主要機能**を同時リリース
- AI駆動開発の完全なワークフロー実現
- 並列処理と効率的な管理機能

## 🎯 使用シナリオ例

### シナリオ1: 新機能開発
```mermaid
sequenceDiagram
    participant User as 開発者
    participant Plan as Planエージェント
    participant Sub as サブエージェント
    participant LSP as LSP統合
    participant Multi as マルチセッション
    
    User->>Plan: 新機能のアイデア提示
    Plan->>Plan: 要件収集・分析
    Plan->>User: 実装計画提示
    User->>Sub: 並列実装指示
    Sub->>LSP: コード理解・生成
    Sub->>User: 実装完了報告
    Multi->>Multi: セッション自動保存
```

### シナリオ2: コードリファクタリング
```mermaid
sequenceDiagram
    participant User as 開発者
    participant Grep as Grep/Globツール
    participant LSP as LSP統合
    participant Sub as サブエージェント
    participant Multi as マルチセッション
    
    User->>Grep: 対象コードの検索
    Grep->>User: 該当ファイル一覧
    User->>LSP: コード構造の分析
    LSP->>User: 依存関係の提示
    User->>Sub: リファクタリング実行
    Sub->>User: 変更完了報告
    Multi->>Multi: 作業履歴保存
```

## 🚀 導入効果

### 開発効率の向上
- **計画立案**: Planエージェントによる構造化された要件定義
- **並列開発**: サブエージェントによる複数タスクの同時実行
- **コード理解**: LSP統合による高精度な開発支援
- **効率的検索**: Grep/Globツールによる高速ファイル探索

### 管理効率の向上
- **セッション管理**: マルチセッション機能による履歴の永続化
- **プロジェクト管理**: ディレクトリベースの独立した管理
- **知識共有**: セッション共有による チーム協業の促進

## 📚 各機能の詳細ドキュメント

1. **[LSP統合機能（Code Intelligence）](01_LSP.md)**
   - Language Server Protocol統合の詳細
   - 対応言語とセットアップ方法
   - 実用的なユースケース

2. **[サブエージェント機能（Subagents）](02_Subagents.md)**
   - 並列実行の仕組みと効果
   - カスタムエージェントの作成方法
   - 効果的な使い方とベストプラクティス

3. **[Planエージェント機能（Plan Agent）](03_PlanAgent.md)**
   - 計画立案の4段階プロセス
   - 読み取り専用設計の理由
   - 実装計画の構成要素

4. **[マルチセッション機能（Multi-Session Support）](04_MultiSession.md)**
   - セッション管理の仕組み
   - コマンドラインとチャット内操作
   - プロジェクトベースの管理方法

5. **[Grep/Globツール機能（Grep/Glob Tools）](05_GrepGlob.md)**
   - 高速検索の仕組み
   - shellツールとの違い
   - セキュリティとアクセス制御

## 🔮 今後の展望

Kiro CLIは継続的に進化を続けており、以下の分野での更なる改善が期待されます：

- **AI機能の強化**: より高度な理解と生成能力
- **統合機能の拡充**: 外部ツールとの連携強化
- **パフォーマンス向上**: 処理速度と効率の最適化
- **ユーザビリティ改善**: より直感的な操作体験

## 📞 サポート・コミュニティ

- **公式サイト**: [kiro.dev](https://kiro.dev/)
- **GitHub**: [kirodotdev/Kiro](https://github.com/kirodotdev/Kiro)
- **Discord**: [Kiro Community](https://discord.gg/kirodotdev)

---

**最終更新**: 2025年12月28日  
**対象バージョン**: Kiro CLI v1.23.1
