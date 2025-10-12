# 設定ファイル配置マップ

**最終更新**: 2025-10-11  
**対象バージョン**: v1.17.0以降

---

## 📋 目次

- [概要](#概要)
- [設定ファイル一覧](#設定ファイル一覧)
- [ディレクトリ構造](#ディレクトリ構造)
- [ファイル別詳細](#ファイル別詳細)
- [優先順位](#優先順位)
- [実践例](#実践例)

---

## 🗺️ 概要

Amazon Q CLIの設定ファイルは複数の場所に配置され、それぞれ異なる役割を持ちます。このドキュメントでは、すべての設定ファイルの配置場所と用途を一元的に管理します。

---

## 📁 設定ファイル一覧

| ファイル | パス | スコープ | 用途 |
|---------|------|---------|------|
| **グローバル設定** | `~/.local/share/amazon-q/settings.json` | グローバル | Amazon Q CLI全体の設定（Knowledge設定を含む） |
| **グローバルAgent** | `~/.config/amazonq/agents/*.json` | グローバル | すべてのプロジェクトで使用可能なAgent |
| **ローカルAgent** | `.amazonq/agents/*.json` | プロジェクト | 特定のプロジェクト専用のAgent |
| **MCP設定** | `~/.config/amazonq/mcp.json` | グローバル | MCPサーバー設定 |

---

## 🌲 ディレクトリ構造

### グローバル設定ディレクトリ

```
~/.local/share/amazon-q/
├── settings.json           # グローバル設定
├── data.sqlite3           # データベース
└── history                # チャット履歴

~/.aws/amazonq/
└── cli-agents/
    ├── aws-expert.json     # グローバルAgent例1
    ├── python-dev.json     # グローバルAgent例2
    └── security.json       # グローバルAgent例3
```

### 環境変数による配置変更

**💡 初心者の方へ**: ほとんどのユーザー（約80%）は以下の設定は不要です。デフォルトの `~/.local/share/amazon-q/settings.json` をそのまま使用してください。

Linux環境では、以下の環境変数により配置場所が変更されます：

| 環境変数 | 設定時のパス | 設定するユーザー |
|----------|--------------|------------------|
| `XDG_DATA_HOME` | `$XDG_DATA_HOME/amazon-q/settings.json` | **上級ユーザー（約20%）** |
| 未設定（デフォルト） | `~/.local/share/amazon-q/settings.json` | **一般ユーザー（約80%）** |

#### 🎯 XDG_DATA_HOMEを設定するのはこんなユーザー

| ユーザー層 | 設定理由 | 設定例 |
|-----------|----------|--------|
| **開発者・プログラマー** | 開発環境と個人環境を分離 | `export XDG_DATA_HOME="$HOME/DevData"` |
| **システム管理者** | 企業ポリシーに従った配置 | `export XDG_DATA_HOME="/opt/userdata/$USER"` |
| **上級Linuxユーザー** | ホームディレクトリの整理 | `export XDG_DATA_HOME="$HOME/Data"` |
| **ストレージ最適化派** | SSD/HDDの使い分け | `export XDG_DATA_HOME="/mnt/hdd/data"` |

#### ❓ 自分が設定すべきか分からない場合

**以下に当てはまらない場合は設定不要です**:
- [ ] 複数の開発環境を使い分けている
- [ ] ホームディレクトリを整理整頓したい
- [ ] 会社のIT部門から指示されている
- [ ] 外部ストレージにデータを保存したい

**注意**: `XDG_CONFIG_HOME`は使用されません。

### プロジェクトローカル設定ディレクトリ

```
/path/to/project/
├── .amazonq/
│   └── cli-agents/
│       ├── project-agent.json    # プロジェクト専用Agent
│       └── test-agent.json       # テスト用Agent
├── src/
└── README.md
```

---

## 📄 ファイル別詳細

### 1. グローバル設定 (`~/.local/share/amazon-q/settings.json`)

**用途**: Amazon Q CLI全体の動作を制御する設定（Knowledge設定を含む）

**配置場所**: 
- Linux/WSL: `~/.local/share/amazon-q/settings.json`
- macOS: `~/.local/share/amazon-q/settings.json`
- Windows: `%USERPROFILE%\.config\amazonq\settings.json`

**設定例**:
```json
{
  "telemetry.enabled": false,
  "chat.enableThinking": true,
  "chat.enableKnowledge": true,
  "chat.enableDelegate": false,
  "knowledge.indexType": "bm25",
  "knowledge.maxFiles": 1000,
  "knowledge.chunkSize": 1000
}
```

**主な設定項目**:
- テレメトリ設定
- チャット機能設定
- Knowledge機能設定（indexType、maxFiles、chunkSize等）
- Knowledge機能設定
- MCP機能設定

**詳細**: [設定項目リファレンス](settings-reference.md)

---

### 2. グローバルAgent (`~/.aws/amazonq/cli-agents/*.json`)

**用途**: すべてのプロジェクトで使用可能な汎用Agent

**配置場所**: `~/.aws/amazonq/cli-agents/`

**ファイル名**: 任意（例: `aws-expert.json`, `python-dev.json`）

**設定例**:
```json
{
  "name": "aws-expert",
  "description": "AWS設計・構築のエキスパート",
  "instructions": "あなたはAWSのスーパーエキスパートです...",
  "tools": ["use_aws", "read_documentation"],
  "mcpServers": ["aws-mcp"]
}
```

**使用シーン**:
- 複数のプロジェクトで共通して使用するAgent
- 汎用的なタスク（AWS操作、コードレビューなど）
- チーム全体で共有するAgent設定

**詳細**: [Agent設定ガイド](../configuration/agent-configuration.md)

---

### 3. ローカルAgent (`.amazonq/cli-agents/*.json`)

**用途**: 特定のプロジェクト専用のAgent

**配置場所**: プロジェクトルートの `.amazonq/cli-agents/`

**ファイル名**: 任意（例: `project-agent.json`）

**設定例**:
```json
{
  "name": "project-agent",
  "description": "このプロジェクト専用のAgent",
  "instructions": "このプロジェクトの構造を理解し...",
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "allowedPaths": [
    "${workspaceFolder}/src",
    "${workspaceFolder}/tests"
  ]
}
```

**使用シーン**:
- プロジェクト固有のルールやガイドラインを適用
- プロジェクト専用のツールやMCPサーバーを使用
- チーム内でプロジェクト設定を共有（Git管理）

**詳細**: [Agent設定ガイド](../configuration/agent-configuration.md)

---

### 4. MCP設定 (`~/.aws/amazonq/mcp.json`)

**用途**: MCPサーバーの接続設定

**配置場所**: `~/.aws/amazonq/mcp.json`

**設定例**:
```json
{
  "mcpServers": {
    "aws-mcp": {
      "command": "node",
      "args": ["/path/to/aws-mcp/index.js"],
      "env": {
        "AWS_REGION": "ap-northeast-1"
      }
    },
    "github-mcp": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

**主な設定項目**:
- サーバー起動コマンド
- 環境変数
- 接続タイプ（stdio/HTTP）

**詳細**: [MCP設定ガイド](../configuration/mcp-configuration.md)

---

---

## 🔢 優先順位

設定の優先順位（高い順）:

1. **コマンドライン引数** - `q chat --agent my-agent`
2. **環境変数** - `Q_AGENT=my-agent`
3. **ローカルAgent設定** - `.amazonq/cli-agents/*.json`
4. **グローバルAgent設定** - `~/.aws/amazonq/cli-agents/*.json`
5. **グローバル設定** - `~/.local/share/amazon-q/settings.json`
6. **デフォルト値** - Amazon Q CLI組み込みのデフォルト

**詳細**: [設定優先順位ガイド](../configuration/priority-rules.md)

---

## 💡 実践例

### 例1: プロジェクト専用Agentの作成

```bash
# プロジェクトディレクトリに移動
cd /path/to/my-project

# Agentディレクトリを作成
mkdir -p .aws/amazonq/cli-agents

# Agent設定を作成
cat > .aws/amazonq/cli-agents/project-agent.json << 'EOF'
{
  "name": "project-agent",
  "description": "このプロジェクト専用のAgent",
  "instructions": "このプロジェクトのコーディング規約に従ってください",
  "tools": ["fs_read", "fs_write"],
  "allowedPaths": ["${workspaceFolder}"]
}
EOF

# Agentを使用
q chat --agent project-agent
```

---

### 例2: グローバルAgentの作成

```bash
# グローバルAgentディレクトリを作成
mkdir -p ~/.aws/amazonq/cli-agents

# AWS専門家Agentを作成
cat > ~/.aws/amazonq/cli-agents/aws-expert.json << 'EOF'
{
  "name": "aws-expert",
  "description": "AWS設計・構築のエキスパート",
  "instructions": "あなたはAWSのスーパーエキスパートです",
  "tools": ["use_aws", "read_documentation"],
  "mcpServers": ["aws-mcp"]
}
EOF

# どのプロジェクトからでも使用可能
cd /any/project
q chat --agent aws-expert
```

---

### 例3: 設定ファイルの確認

```bash
# グローバル設定を確認
cat ~/.local/share/amazon-q/settings.json

# グローバルAgentを一覧表示
ls -la ~/.aws/amazonq/cli-agents/

# ローカルAgentを一覧表示
ls -la .amazonq/cli-agents/

# 現在有効なAgentを確認
q agent list
```

---

### 🔰 初心者向け: 最初の設定ファイル作成

**Q CLIを初めて使う方向けの手順**:

```bash
# 1. Q CLIが正常にインストールされているか確認
q --version

# 2. 設定ファイルの場所を確認（まだ存在しない可能性があります）
ls -la ~/.local/share/amazon-q/

# 3. Q CLIを一度起動（設定ファイルが自動作成されます）
q chat "Hello"

# 4. 設定ファイルが作成されたことを確認
ls -la ~/.local/share/amazon-q/settings.json

# 5. 設定内容を確認
cat ~/.local/share/amazon-q/settings.json
```

**💡 重要**: 
- 設定ファイルは Q CLI を初回起動時に自動作成されます
- 手動で作成する必要はありません
- 場所は `~/.local/share/amazon-q/settings.json` です（約80%のユーザー）

---

### 例4: 設定の優先順位テスト

```bash
# グローバル設定でthinkingを無効化
q settings set chat.enableThinking false

# 環境変数で上書き
export Q_ENABLE_THINKING=true

# コマンドライン引数で最終的に上書き
q chat --enable-thinking "質問内容"
```

---

## 🔍 トラブルシューティング

### 🔰 初心者向け: 設定ファイルが見つからない場合

**症状**: 「設定ファイルがどこにあるか分からない」

**解決方法**:
```bash
# 1. まずはデフォルトの場所を確認（80%のユーザーはここにあります）
ls -la ~/.local/share/amazon-q/settings.json

# 2. ファイルが存在する場合
cat ~/.local/share/amazon-q/settings.json

# 3. ファイルが存在しない場合は作成
mkdir -p ~/.local/share/amazon-q
echo '{}' > ~/.local/share/amazon-q/settings.json
```

**💡 ヒント**: 
- ほとんどの場合、設定ファイルは `~/.local/share/amazon-q/settings.json` にあります
- 見つからない場合は、まだ設定を変更していない可能性があります
- Q CLIを一度起動すると自動的に作成されます

### 設定ファイルが見つからない

```bash
# 設定ファイルの存在確認
ls -la ~/.local/share/amazon-q/
ls -la ~/.aws/amazonq/cli-agents/
ls -la .aws/amazonq/cli-agents/

# ディレクトリが存在しない場合は作成
mkdir -p ~/.local/share/amazon-q
mkdir -p ~/.aws/amazonq/cli-agents
mkdir -p .aws/amazonq/cli-agents
```

---

### Agentが認識されない

```bash
# Agent一覧を確認
q agent list

# Agent設定の構文を検証
q agent validate <agent-name>

# デバッグログを有効化
export Q_LOG_LEVEL=debug
q chat --agent <agent-name>
```

---

### 設定が反映されない

```bash
# 設定の優先順位を確認
q settings show --all

# 環境変数を確認
env | grep Q_

# Amazon Q CLIを再起動
q restart
```

---

## ❓ よくある質問（初心者向け）

### Q1: 設定ファイルはどこにありますか？

**A**: ほとんどの場合（約80%のユーザー）、以下の場所にあります：
```bash
~/.local/share/amazon-q/settings.json
```

### Q2: XDG_DATA_HOMEって何ですか？設定が必要ですか？

**A**: **設定不要です**。XDG_DATA_HOMEは上級ユーザー（約20%）が使用する環境変数です。
- 一般ユーザー: 設定不要（デフォルトで正常動作）
- 上級ユーザー: 環境の整理・最適化のために設定

### Q3: ~/.config/q/ に設定ファイルがないのですが？

**A**: **正常です**。Q CLIは `~/.config/q/` ではなく `~/.local/share/amazon-q/` を使用します。
```bash
# 正しい場所
ls ~/.local/share/amazon-q/settings.json

# 間違った場所（使用されません）
ls ~/.config/q/settings.json
```

### Q4: 設定ファイルが見つからない場合は？

**A**: Q CLIを一度起動すると自動作成されます：
```bash
# Q CLIを起動（設定ファイルが自動作成される）
q chat "Hello"

# 作成されたことを確認
ls ~/.local/share/amazon-q/settings.json
```

### Q5: 上級ユーザーはなぜXDG_DATA_HOMEを設定するのですか？

**A**: 以下のような理由があります：
- **開発者**: 開発環境と個人環境を分離したい
- **システム管理者**: 企業のディレクトリ標準に従いたい
- **整理好き**: ホームディレクトリを整理整頓したい
- **ストレージ最適化**: SSD/HDDを使い分けたい

**一般ユーザーには不要な設定です。**

---

## 📚 関連ドキュメント

- [設定優先順位ガイド](../configuration/priority-rules.md) - 設定の優先順位の詳細
- [Agent設定ガイド](../configuration/agent-configuration.md) - Agent設定の詳細
- [MCP設定ガイド](../configuration/mcp-configuration.md) - MCPサーバー設定の詳細
- [環境変数ガイド](../configuration/environment-variables.md) - 環境変数の詳細
- [設定項目リファレンス](settings-reference.md) - 全設定項目の一覧

---

**作成日**: 2025-10-11  
**最終更新**: 2025-10-11
