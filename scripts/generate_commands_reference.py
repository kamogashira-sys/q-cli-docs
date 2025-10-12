#!/usr/bin/env python3
"""
commands.md自動生成ツール

q --help-allの出力から完全なコマンドリファレンスを生成します。
"""

import subprocess
import json
import re
from datetime import date
from typing import Dict, List

def extract_command_info(command: str) -> Dict:
    """コマンドの詳細情報を抽出"""
    try:
        result = subprocess.run(
            ['q', command, '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        help_text = result.stdout
        
        # 説明を抽出
        description = help_text.split('\n')[0].strip()
        
        # サブコマンドを抽出
        subcommands = []
        in_commands = False
        for line in help_text.split('\n'):
            if line.startswith('Commands:'):
                in_commands = True
                continue
            if in_commands:
                if line.startswith('  ') and not line.startswith('   '):
                    match = re.match(r'  ([a-z-]+)\s+(.+)', line)
                    if match and match.group(1) != 'help':
                        subcommands.append({
                            'name': match.group(1),
                            'description': match.group(2).strip()
                        })
                elif not line.strip():
                    break
        
        return {
            'description': description,
            'subcommands': subcommands
        }
    except Exception as e:
        print(f"⚠️  Error extracting info for {command}: {e}")
        return {'description': '', 'subcommands': []}

def generate_commands_md() -> str:
    """commands.mdの内容を生成"""
    
    # 全コマンドを取得
    result = subprocess.run(
        ['q', '--help-all'],
        capture_output=True,
        text=True
    )
    
    commands = []
    for line in result.stdout.split('\n'):
        if line.startswith('  ') and not line.startswith('   '):
            match = re.match(r'  ([a-z-]+)', line)
            if match and match.group(1) not in ['help']:
                commands.append(match.group(1))
    
    # 各コマンドの情報を取得
    command_info = {}
    for cmd in commands:
        print(f"📝 {cmd}の情報を抽出中...")
        command_info[cmd] = extract_command_info(cmd)
    
    # Markdownを生成
    md = f"""# コマンドリファレンス

**最終更新**: {date.today().strftime('%Y-%m-%d')}  
**対象バージョン**: v1.17.0以降

---

## 📋 概要

Amazon Q CLIの**全{len(commands)}コマンド**の完全リストです。このリファレンスは`q --help-all`の出力に基づいて自動生成されています。

## コマンド一覧（カテゴリ別）

### 基本・チャット（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q chat`](#q-chat) | AIアシスタントとの対話を開始 |
| [`q translate`](#q-translate) | 自然言語をシェルコマンドに翻訳 |
| [`q inline`](#q-inline) | インラインシェル補完を管理 |

### Agent管理（1コマンド）

| コマンド | 説明 |
|---------|------|
| [`q agent`](#q-agent) | Agentを管理（list, create, edit, validate） |

### 認証・ユーザー管理（5コマンド）

| コマンド | 説明 |
|---------|------|
| [`q login`](#q-login) | Amazon Qにログイン（Builder ID / Identity Center） |
| [`q logout`](#q-logout) | Amazon Qからログアウト |
| [`q whoami`](#q-whoami) | 現在のログイン情報を表示 |
| [`q profile`](#q-profile) | IDCユーザーのプロファイル情報を表示 |
| [`q user`](#q-user) | アカウントを管理（login, logout, whoami, profile） |

### 設定・診断（4コマンド）

| コマンド | 説明 |
|---------|------|
| [`q settings`](#q-settings) | 設定を管理（取得・変更・削除・ファイルを開く） |
| [`q diagnostic`](#q-diagnostic) | 診断テストを実行 |
| [`q doctor`](#q-doctor) | 一般的な問題を診断・修正 |
| [`q debug`](#q-debug) | アプリをデバッグ |

### アプリケーション管理（5コマンド）

| コマンド | 説明 |
|---------|------|
| [`q launch`](#q-launch) | デスクトップアプリを起動 |
| [`q quit`](#q-quit) | デスクトップアプリを終了 |
| [`q restart`](#q-restart) | デスクトップアプリを再起動 |
| [`q update`](#q-update) | Amazon Qアプリを更新 |
| [`q dashboard`](#q-dashboard) | ダッシュボードを開く |

### セットアップ・統合（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q setup`](#q-setup) | CLIコンポーネントをセットアップ |
| [`q init`](#q-init) | シェル用dotfilesを生成 |
| [`q integrations`](#q-integrations) | システム統合を管理 |

### その他（3コマンド）

| コマンド | 説明 |
|---------|------|
| [`q mcp`](#q-mcp) | MCPサーバーを管理（add, remove, list） |
| [`q theme`](#q-theme) | テーマを取得・設定 |
| [`q issue`](#q-issue) | GitHub issueテンプレートを開く |

> 💡 チャットセッション内で使用できるコマンド（`/help`, `/clear`, `/context`など）は [チャット内コマンド](#チャット内コマンド) を参照してください。

---

"""
    
    # 各コマンドの詳細を生成
    for cmd in sorted(commands):
        info = command_info[cmd]
        md += f"## q {cmd}\n\n"
        md += f"{info['description']}\n\n"
        md += f"```bash\nq {cmd}"
        if info['subcommands']:
            md += " <SUBCOMMAND>"
        md += "\n```\n\n"
        
        if info['subcommands']:
            md += "**サブコマンド**:\n"
            for sub in info['subcommands']:
                md += f"- `{sub['name']}` - {sub['description']}\n"
            md += "\n"
        
        md += "---\n\n"
    
    return md

def main():
    """メイン処理"""
    print("🔍 Q CLIコマンド情報を抽出中...\n")
    
    md_content = generate_commands_md()
    
    output_file = 'docs/01_for-users/07_reference/02_commands_generated.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ {output_file}を生成しました")
    print("\n⚠️  注意: 生成されたファイルを確認し、必要に応じて手動で調整してください")
    print("  - 日本語の説明文")
    print("  - 使用例")
    print("  - カテゴリ分類")

if __name__ == "__main__":
    main()
