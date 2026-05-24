# Kiro CLI Exit Codes（終了コード）

**出典**: [Exit Codes - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/exit-codes/)

## 概要

Kiro CLI v1.25.0（2026年2月4日リリース）で追加されたExit Codes機能について詳細に解説します。この機能により、Kiro CLIの実行結果を構造化された終了コードで判定でき、スクリプトやCI/CDパイプラインでの自動化が容易になりました。

### Exit Codesとは

Exit Codesは、**Kiro CLIの実行結果を示す数値コード**です。スクリプトやCI/CDパイプラインで、Kiro CLIの成功・失敗を判定するために使用します。

### 主な特徴

- **構造化された終了コード**: 0（成功）、1（失敗）、3（MCP起動失敗）
- **MCPサーバー必須化**: `--require-mcp-startup`オプション
- **CI/CD対応**: 自動化スクリプトでの利用を想定
- **Hook終了コード**: Hookの実行制御にも対応

### なぜExit Codesが必要なのか

従来、Kiro CLIの実行結果を判定するには、出力メッセージを解析する必要がありました。Exit Codesにより、以下が実現します：

1. **自動化の容易化**: 終了コードで成功・失敗を判定
2. **CI/CD統合**: パイプラインでの利用が容易
3. **エラーハンドリング**: 失敗の種類を区別

## 📋 目次

- [終了コード一覧](#終了コード一覧)
- [MCPサーバー必須化](#mcpサーバー必須化)
- [スクリプト例](#スクリプト例)
- [Hookの終了コード](#hookの終了コード)
- [ベストプラクティス](#ベストプラクティス)
- [ユースケース](#ユースケース)
- [トラブルシューティング](#トラブルシューティング)
- [関連リンク](#関連リンク)

---

## 終了コード一覧

Kiro CLIは、以下の終了コードを返します。

| コード | 名称 | 説明 |
|--------|------|------|
| **0** | Success | コマンドが正常に完了 |
| **1** | Failure | 一般的な失敗（認証エラー、無効な引数、操作失敗） |
| **3** | MCP Startup Failure | MCPサーバーの起動失敗（`--require-mcp-startup`使用時） |

### コード0: Success

**説明**: コマンドが正常に完了しました。

**例**:
```bash
kiro-cli chat --no-interactive "Hello"
echo $?  # 0
```

### コード1: Failure

**説明**: 一般的な失敗が発生しました。

**原因**:
- 認証エラー
- 無効な引数
- 操作失敗
- ネットワークエラー

**例**:
```bash
kiro-cli chat --invalid-option
echo $?  # 1
```

### コード3: MCP Startup Failure

**説明**: MCPサーバーの起動に失敗しました（`--require-mcp-startup`使用時のみ）。

**原因**:
- MCPサーバーの設定エラー
- MCPサーバーの起動失敗
- 依存関係の不足

**例**:
```bash
kiro-cli chat --require-mcp-startup --no-interactive "Run task"
echo $?  # 3（MCPサーバー起動失敗時）
```

---

## MCPサーバー必須化

デフォルトでは、MCPサーバーの起動失敗は警告として記録されますが、終了コードには影響しません。`--require-mcp-startup`オプションを使用すると、MCPサーバーの起動失敗時に即座に終了します。

### --require-mcp-startupオプション

**構文**:
```bash
kiro-cli chat --require-mcp-startup [その他のオプション]
```

**動作**:
- 設定されたMCPサーバーが起動に失敗した場合、即座に終了
- 終了コード3を返す
- エラーメッセージを出力

**使用シーン**:
- CI/CDパイプラインでMCPツールが必須の場合
- MCPサーバーなしでは意味のないタスクを実行する場合
- サイレント失敗を防ぎたい場合

### 例: MCPサーバー必須化

```bash
kiro-cli chat --require-mcp-startup --no-interactive "Run analysis"
```

**成功時**:
```
✔ MCP servers started successfully
✔ Analysis completed
```
終了コード: 0

**失敗時**:
```
✗ MCP server 'my-server' failed to start
✗ Exiting due to --require-mcp-startup
```
終了コード: 3

---

## スクリプト例

### Bashスクリプト

```bash
#!/bin/bash

# Kiro CLIを実行
kiro-cli chat --require-mcp-startup --no-interactive --trust-all-tools "Run analysis"
exit_code=$?

# 終了コードに応じて処理
case $exit_code in
    0)
        echo "✔ Success"
        ;;
    3)
        echo "✗ MCP servers failed to start"
        exit 1
        ;;
    *)
        echo "✗ Failed with code $exit_code"
        exit $exit_code
        ;;
esac
```

### CI/CDパイプライン

#### GitHub Actions

```yaml
name: Kiro Analysis

on: [push]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Kiro task
        run: |
          kiro-cli chat --require-mcp-startup --no-interactive --trust-all-tools "Analyze code"
        continue-on-error: false
```

#### GitLab CI

```yaml
kiro-analysis:
  script:
    - kiro-cli chat --require-mcp-startup --no-interactive --trust-all-tools "Analyze code"
  allow_failure: false
```

### エラーハンドリング

```bash
#!/bin/bash

# Kiro CLIを実行
kiro-cli chat --require-mcp-startup --no-interactive "Run task"
exit_code=$?

# 終了コードに応じてリトライ
if [ $exit_code -eq 3 ]; then
    echo "MCP servers failed, retrying without MCP..."
    kiro-cli chat --no-interactive "Run task"
    exit_code=$?
fi

exit $exit_code
```

---

## Hookの終了コード

Hookは、ツール実行前後に実行されるスクリプトです。Hookの終了コードにより、ツール実行を制御できます。

### Hook終了コード一覧

| コード | 動作 | 説明 |
|--------|------|------|
| **0** | Continue | ツールを実行 |
| **2** | Skip | ツールをスキップ（エラーなし） |
| **その他** | Abort | ツール実行を中止（エラー） |

### コード0: Continue

**説明**: ツールを実行します。

**例**:
```bash
#!/bin/bash
# pre-tool hook
echo "Preparing..."
exit 0  # ツールを実行
```

### コード2: Skip

**説明**: ツールをスキップします（エラーなし）。

**例**:
```bash
#!/bin/bash
# pre-tool hook
if [ -f ".skip-tool" ]; then
    echo "Skipping tool..."
    exit 2  # ツールをスキップ
fi
exit 0
```

### その他: Abort

**説明**: ツール実行を中止します（エラー）。

**例**:
```bash
#!/bin/bash
# pre-tool hook
if [ ! -f "required-file" ]; then
    echo "Required file not found"
    exit 1  # ツール実行を中止
fi
exit 0
```

---

## ベストプラクティス

### 1. CI/CDでは--require-mcp-startupを使用

MCPツールが必須の場合、`--require-mcp-startup`を使用してサイレント失敗を防ぎます。

```bash
kiro-cli chat --require-mcp-startup --no-interactive "Run task"
```

### 2. 終了コードを明示的にチェック

スクリプトでは、終了コードを明示的にチェックします。

```bash
kiro-cli chat --no-interactive "Run task"
if [ $? -ne 0 ]; then
    echo "Failed"
    exit 1
fi
```

### 3. エラーメッセージを記録

CI/CDでは、エラーメッセージを記録します。

```bash
kiro-cli chat --no-interactive "Run task" 2>&1 | tee kiro.log
exit_code=${PIPESTATUS[0]}
```

### 4. リトライロジックを実装

一時的なエラーに対応するため、リトライロジックを実装します。

```bash
for i in {1..3}; do
    kiro-cli chat --no-interactive "Run task"
    if [ $? -eq 0 ]; then
        break
    fi
    echo "Retry $i/3..."
    sleep 5
done
```

### 5. Hookで事前チェック

Hookで事前チェックを実行し、不要なツール実行を防ぎます。

```bash
#!/bin/bash
# pre-tool hook
if [ ! -f "config.yaml" ]; then
    echo "Config not found, skipping..."
    exit 2  # スキップ
fi
exit 0
```

---

## ユースケース

### ユースケース1: CI/CDでのコード分析

**シナリオ**: プルリクエスト時にコード分析を実行

```yaml
name: Code Analysis

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Kiro analysis
        run: |
          kiro-cli chat --require-mcp-startup --no-interactive --trust-all-tools "Analyze code quality"
        
      - name: Check exit code
        if: failure()
        run: |
          echo "Analysis failed"
          exit 1
```

### ユースケース2: 自動テスト生成

**シナリオ**: コミット前にテストを自動生成

```bash
#!/bin/bash
# pre-commit hook

echo "Generating tests..."
kiro-cli chat --no-interactive "Generate tests for modified files"

if [ $? -ne 0 ]; then
    echo "Test generation failed"
    exit 1
fi

echo "Tests generated successfully"
exit 0
```

### ユースケース3: デプロイ前チェック

**シナリオ**: デプロイ前にセキュリティチェックを実行

```bash
#!/bin/bash

echo "Running security check..."
kiro-cli chat --require-mcp-startup --no-interactive "Check for security vulnerabilities"
exit_code=$?

if [ $exit_code -eq 3 ]; then
    echo "MCP servers failed, cannot perform security check"
    exit 1
elif [ $exit_code -ne 0 ]; then
    echo "Security check failed"
    exit 1
fi

echo "Security check passed"
exit 0
```

---

## トラブルシューティング

### 問題1: 終了コードが常に0

**症状**: 失敗しても終了コード0が返される

**原因**:
- パイプラインで終了コードが失われている
- エラーハンドリングが不適切

**解決方法**:

```bash
# 悪い例
kiro-cli chat --no-interactive "Run task" | tee output.log
echo $?  # teeの終了コード

# 良い例
kiro-cli chat --no-interactive "Run task" 2>&1 | tee output.log
exit_code=${PIPESTATUS[0]}
echo $exit_code  # kiro-cliの終了コード
```

### 問題2: MCPサーバー起動失敗が検出されない

**症状**: MCPサーバーが起動していないのに成功する

**原因**:
- `--require-mcp-startup`オプションを使用していない

**解決方法**:

```bash
# MCPサーバーを必須化
kiro-cli chat --require-mcp-startup --no-interactive "Run task"
```

### 問題3: Hook終了コードが無視される

**症状**: Hookで終了コード2を返してもツールが実行される

**原因**:
- Hookスクリプトの権限がない
- Hookスクリプトのパスが正しくない

**解決方法**:

```bash
# 権限を確認
ls -l .kiro/hooks/pre-tool
# 実行権限を付与
chmod +x .kiro/hooks/pre-tool
```

---

## 関連リンク

### 公式ドキュメント
- [Exit Codes - Kiro CLI Documentation](https://kiro.dev/docs/cli/reference/exit-codes/)
- [Kiro CLI v1.25.0 Changelog](https://kiro.dev/changelog/cli/1-25/)

### 関連機能
- [Agent Client Protocol (ACP)](13_ACP.md) - エディタ統合
- [Help Agent](14_HelpAgent.md) - ヘルプエージェント
- [Subagent Access Control](02_Subagents.md#subagent-access-controlv1250) - サブエージェント制御
- [v2 Major Update](16_v2MajorUpdate.md) — Headless Mode と Exit Codes の併用

### リファレンス（辞書）
- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `kiro-cli chat --no-interactive` `--require-mcp-startup` 等の CI/CD 用フラグ

### CI/CD統合
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitLab CI](https://docs.gitlab.com/ee/ci/)
- [CircleCI](https://circleci.com/docs/)

---

**最終更新**: 2026年2月7日
