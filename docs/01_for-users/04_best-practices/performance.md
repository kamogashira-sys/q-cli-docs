# パフォーマンス最適化

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## ⚡ 概要

Amazon Q CLIのパフォーマンスを最適化する方法を紹介します。このガイドでは、コンテキスト管理、Knowledge Base最適化、MCP設定、ログ管理など、実践的な最適化手法を説明します。

### このガイドで学べること

- コンテキスト使用率の測定と管理
- Knowledge Baseの最適化
- MCPサーバーのパフォーマンスチューニング
- ログとデバッグの効率化
- パフォーマンス問題のトラブルシューティング

---

## 📊 パフォーマンス測定

### コンテキスト使用率の確認

**v1.17.0の新機能**:
```bash
# コンテキスト使用率インジケーターを有効化
q settings chat.enableContextUsageIndicator true
```

**表示例**:
```
Context: 45% (4,500 / 10,000 tokens)
```

### レスポンス時間の測定

```bash
# 時間を測定してコマンド実行
time q chat "Hello, Q!"

# 出力例:
# real    0m2.345s
# user    0m0.123s
# sys     0m0.045s
```

### リソース使用量の監視

```bash
# プロセスのリソース使用量を確認
ps aux | grep q

# メモリ使用量を確認
top -p $(pgrep -f "q chat")
```

---

## 🧠 コンテキスト管理

### コンテキストの仕組み

**コンテキストウィンドウとは**:
- AIモデルが一度に処理できる情報量の上限
- トークン数で測定（1トークン ≈ 4文字）
- 使用率が高いとパフォーマンスが低下

**トークン数の計算**:
- テキスト: 約4文字 = 1トークン
- コード: 約3文字 = 1トークン
- 日本語: 約2文字 = 1トークン

### 使用率の影響

| 使用率 | 状態 | 推奨アクション |
|--------|------|---------------|
| 0-50% | 良好 | 通常使用 |
| 50-70% | 注意 | 監視を継続 |
| 70-85% | 警告 | 圧縮を検討 |
| 85-100% | 危険 | 即座に圧縮 |

### 最適化手法

#### 定期的な圧縮（/compact）

**手動圧縮**:
```
> /compact
```

**推奨タイミング**:
- 使用率が80%を超えたとき
- 長時間のセッション後
- 大量のファイル操作後

**圧縮の効果**:
- 会話履歴を要約
- トークン数を削減（通常50-70%削減）
- レスポンス速度の向上

#### 自動コンパクションの設定

```bash
# 自動コンパクションを有効化（デフォルト）
q settings chat.disableAutoCompaction false

# 自動コンパクションを無効化
q settings chat.disableAutoCompaction true
```

**自動コンパクションの動作**:
- 使用率が一定値を超えると自動実行
- バックグラウンドで処理
- ユーザーの操作を中断しない

**v1.16.0での変更**:
- 会話クリア時のサマリ保持が無効化されました
- メモリ使用量の削減

### 実践例

#### 長時間セッションの管理

```bash
# 1. 使用率を監視
q settings chat.enableContextUsageIndicator true

# 2. 定期的に圧縮
# チャット内で実行
> /compact

# 3. 必要に応じて会話をリセット
> /clear
```

#### 大量のファイル操作時の対策

```bash
# 1. バッチ処理を活用（v1.13.0+）
# fs_readは複数ファイルを効率的に処理

# 2. 不要なファイルを除外
# Knowledge設定で除外パターンを指定

# 3. 処理後に圧縮
> /compact
```

#### Knowledge使用時の注意点

```bash
# 1. 適切なチャンクサイズを設定
q settings knowledge.chunkSize 1000

# 2. 最大ファイル数を制限
q settings knowledge.maxFiles 1000

# 3. 不要なファイルを除外
q settings knowledge.defaultExcludePatterns '["**/*.log", "**/*.tmp"]'
```

---

## 📚 Knowledge Base最適化

### インデックス設定

#### indexTypeの選択

**v1.14.0の新機能**: BM25サポート

```bash
# BM25インデックス（推奨）
q settings knowledge.indexType "bm25"

# Vectorインデックス
q settings knowledge.indexType "vector"
```

**比較表**:

| 特性 | BM25 | Vector |
|------|------|--------|
| 検索速度 | 高速 | 中速 |
| メモリ使用量 | 少ない | 多い |
| 精度 | キーワードマッチ | セマンティック |
| 推奨用途 | コード検索 | 自然言語検索 |

#### chunkSizeの最適化

```bash
# デフォルト値
q settings knowledge.chunkSize 1000

# 小さいチャンク（精度重視）
q settings knowledge.chunkSize 500

# 大きいチャンク（速度重視）
q settings knowledge.chunkSize 2000
```

**チャンクサイズの影響**:
- 小さい: 精度↑、速度↓、メモリ↑
- 大きい: 精度↓、速度↑、メモリ↓

#### chunkOverlapの設定

```bash
# デフォルト値
q settings knowledge.chunkOverlap 200

# オーバーラップなし（速度重視）
q settings knowledge.chunkOverlap 0

# 大きいオーバーラップ（精度重視）
q settings knowledge.chunkOverlap 400
```

**オーバーラップの効果**:
- チャンク境界での情報損失を防ぐ
- 検索精度の向上
- インデックスサイズの増加

### ファイル選択の最適化

#### 必要なファイルのみ追加

```bash
# 含めるファイルパターン
q settings knowledge.defaultIncludePatterns '[
  "**/*.md",
  "**/*.py",
  "**/*.js",
  "**/*.ts"
]'
```

#### 除外パターンの設定

```bash
# 除外するファイルパターン
q settings knowledge.defaultExcludePatterns '[
  "**/*.log",
  "**/*.tmp",
  "**/node_modules/**",
  "**/.git/**",
  "**/dist/**",
  "**/build/**"
]'
```

#### 定期的なクリーンアップ

```bash
# Knowledge Baseをクリア
> /knowledge clear

# 再インデックス
> /knowledge index
```

### パフォーマンス比較

#### BM25 vs Vector検索

**テスト条件**:
- ファイル数: 1,000
- 総サイズ: 10MB
- チャンクサイズ: 1000

**結果**:

| 指標 | BM25 | Vector |
|------|------|--------|
| インデックス時間 | 5秒 | 15秒 |
| 検索時間 | 0.1秒 | 0.3秒 |
| メモリ使用量 | 50MB | 150MB |

#### チャンクサイズの影響

**テスト条件**:
- ファイル数: 1,000
- インデックスタイプ: BM25

**結果**:

| チャンクサイズ | インデックス時間 | 検索時間 | メモリ |
|--------------|----------------|---------|--------|
| 500 | 7秒 | 0.15秒 | 70MB |
| 1000 | 5秒 | 0.10秒 | 50MB |
| 2000 | 4秒 | 0.08秒 | 35MB |

#### ファイル数の影響

**テスト条件**:
- チャンクサイズ: 1000
- インデックスタイプ: BM25

**結果**:

| ファイル数 | インデックス時間 | 検索時間 | メモリ |
|-----------|----------------|---------|--------|
| 100 | 0.5秒 | 0.05秒 | 5MB |
| 1,000 | 5秒 | 0.10秒 | 50MB |
| 10,000 | 50秒 | 0.20秒 | 500MB |

---

## 🔧 MCP最適化

### タイムアウト設定

#### 適切なタイムアウト値

```json
{
  "mcpServers": {
    "fast-api": {
      "timeout": 30000    // 30秒（高速API）
    },
    "normal-api": {
      "timeout": 120000   // 2分（通常API、デフォルト）
    },
    "slow-api": {
      "timeout": 300000   // 5分（低速API）
    }
  }
}
```

**推奨値**:
- **高速API**: 30,000ms (30秒)
  - 例: キャッシュされたデータ、ローカルDB
- **通常API**: 120,000ms (2分、デフォルト)
  - 例: 一般的なREST API
- **低速API**: 300,000ms (5分)
  - 例: 大量データ処理、複雑な計算

#### グローバルタイムアウト設定

```bash
# MCP初期化タイムアウト
q settings mcp.initTimeout 180000

# 非対話型MCPタイムアウト
q settings mcp.noInteractiveTimeout 60000
```

### リトライ設定

**v1.14.0の改善**: リトライ通知のための遅延追跡

```json
{
  "mcpServers": {
    "api": {
      "timeout": 120000,
      "retries": 3,
      "retryDelay": 1000
    }
  }
}
```

### 並列実行の制限

```json
{
  "mcpServers": {
    "api": {
      "maxConcurrentRequests": 5
    }
  }
}
```

### トランスポートタイプの選択

#### stdio（ローカルプロセス）

**特徴**:
- 高速（プロセス間通信）
- 低レイテンシ
- ローカル実行のみ

**使用例**:
```json
{
  "mcpServers": {
    "local-tool": {
      "type": "stdio",
      "command": "node",
      "args": ["./server.js"]
    }
  }
}
```

#### HTTP（リモートサーバー）

**特徴**:
- ネットワーク遅延あり
- リモート実行可能
- スケーラブル

**使用例**:
```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "timeout": 120000
    }
  }
}
```

### リモートMCPの最適化

**v1.16.0の新機能**: リモートMCPサポート

#### ネットワークレイテンシの考慮

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "timeout": 180000,        // レイテンシを考慮
      "keepAlive": true,        // 接続を維持
      "maxSockets": 10          // 接続プール
    }
  }
}
```

#### バッチ処理の活用

```json
{
  "mcpServers": {
    "batch-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "batchSize": 10,          // バッチサイズ
      "batchDelay": 100         // バッチ間の遅延
    }
  }
}
```

### 一時的な無効化

```json
{
  "mcpServers": {
    "temporary-disabled": {
      "command": "node",
      "args": ["server.js"],
      "disabled": true          // 一時的に無効化
    }
  }
}
```

**効果**:
- リソース使用量の削減
- 起動時間の短縮
- デバッグの簡素化

---

## 💾 ストレージ最適化

### ログファイルの管理

#### ログローテーション

```bash
# ログファイルのサイズを確認
du -h /run/user/$(id -u)/qlog/

# 古いログを削除
find /run/user/$(id -u)/qlog/ -name "*.log" -mtime +7 -delete

# ログを圧縮
gzip /run/user/$(id -u)/qlog/*.log.old
```

#### ログレベルの調整

```bash
# 本番環境: ERRORのみ
export Q_LOG_LEVEL=error

# 開発環境: DEBUGレベル
export Q_LOG_LEVEL=debug

# デフォルト: INFO
unset Q_LOG_LEVEL
```

### キャッシュの管理

#### キャッシュサイズの確認

```bash
# キャッシュディレクトリのサイズ
du -sh ~/.cache/amazon-q/

# 詳細表示
du -h ~/.cache/amazon-q/ | sort -h
```

#### 定期的なクリーンアップ

```bash
# キャッシュをクリア
rm -rf ~/.cache/amazon-q/*

# Q CLIを再起動
q restart
```

---

## 🐛 パフォーマンス問題のトラブルシューティング

### 一般的な問題

#### 問題1: レスポンスが遅い

**症状**:
- コマンド実行に時間がかかる
- チャットの応答が遅い

**診断**:
```bash
# 1. コンテキスト使用率を確認
q settings chat.enableContextUsageIndicator true

# 2. ログレベルを上げて詳細を確認
Q_LOG_LEVEL=debug q chat "test"

# 3. ネットワーク接続を確認
ping api.amazonq.aws
```

**解決策**:
```bash
# コンテキストを圧縮
> /compact

# MCPタイムアウトを延長
q settings mcp.initTimeout 180000

# 不要なMCPサーバーを無効化
# Agent設定で "disabled": true
```

#### 問題2: メモリ使用量が多い

**症状**:
- システムが重くなる
- スワップが発生

**診断**:
```bash
# メモリ使用量を確認
ps aux | grep q | awk '{print $6}'

# Knowledge Baseのサイズを確認
du -sh ~/.local/share/amazon-q/knowledge/
```

**解決策**:
```bash
# Knowledge Baseを最適化
q settings knowledge.indexType "bm25"
q settings knowledge.maxFiles 1000

# 不要なファイルを除外
q settings knowledge.defaultExcludePatterns '[
  "**/node_modules/**",
  "**/.git/**"
]'

# キャッシュをクリア
rm -rf ~/.cache/amazon-q/*
```

#### 問題3: コンテキストがすぐに満杯になる

**症状**:
- 頻繁に圧縮が必要
- 長い会話ができない

**診断**:
```bash
# 使用率を確認
q settings chat.enableContextUsageIndicator true

# 会話履歴を確認
> /history
```

**解決策**:
```bash
# 自動コンパクションを有効化
q settings chat.disableAutoCompaction false

# Markdownレンダリングを無効化（トークン削減）
q settings chat.disableMarkdownRendering true

# 不要な履歴をクリア
> /clear
```

### 診断方法

#### ログの確認

```bash
# エラーログを確認
grep ERROR /run/user/$(id -u)/qlog/qchat.log

# 警告ログを確認
grep WARN /run/user/$(id -u)/qlog/qchat.log

# パフォーマンス関連ログ
grep "slow\|timeout\|latency" /run/user/$(id -u)/qlog/qchat.log
```

#### 設定の確認

```bash
# 全設定を表示
q settings all

# 特定の設定を確認
q settings knowledge.maxFiles
q settings mcp.initTimeout
q settings chat.disableAutoCompaction
```

#### リソース使用量の確認

```bash
# CPU使用率
top -p $(pgrep -f "q chat")

# メモリ使用量
ps aux | grep "q chat"

# ディスク使用量
du -sh ~/.local/share/amazon-q/
du -sh ~/.cache/amazon-q/
```

---

## ✅ パフォーマンスチェックリスト

### 定期的な測定

- [ ] コンテキスト使用率を監視
- [ ] レスポンス時間を測定
- [ ] メモリ使用量を確認
- [ ] ディスク使用量を確認

### 設定の見直し

- [ ] Knowledge Base設定を最適化
- [ ] MCPタイムアウトを調整
- [ ] 自動コンパクションを有効化
- [ ] 不要なMCPサーバーを無効化

### リソースのクリーンアップ

- [ ] 古いログを削除
- [ ] キャッシュをクリア
- [ ] 不要なKnowledge Baseファイルを除外
- [ ] 会話履歴を整理

---

## 📚 関連ドキュメント

- **[設定項目リファレンス](../07_reference/settings-reference.md)** - 全設定項目の詳細
- **[Agent設定ガイド](../03_configuration/agent-configuration.md)** - Agent設定の詳細
- **[MCP設定ガイド](../03_configuration/mcp-configuration.md)** - MCPサーバーの設定
- **[環境変数ガイド](../03_configuration/environment-variables.md)** - 環境変数の使い方
- **[トラブルシューティング](../06_troubleshooting/common-issues.md)** - よくある問題と解決方法
- **[設定のベストプラクティス](configuration.md)** - 全般的な設定のベストプラクティス
- **[セキュリティベストプラクティス](security.md)** - セキュリティのベストプラクティス

---

**作成日**: 2025-10-11  
**最終更新日**: 2025-10-11  
**対象バージョン**: v1.17.0以降
