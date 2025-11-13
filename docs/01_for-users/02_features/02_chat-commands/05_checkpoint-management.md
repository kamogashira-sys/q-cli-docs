[ホーム](../../../README.md) > [ユーザーガイド](../../README.md) > [機能ガイド](../README.md) > [チャット機能](../01_chat.md) > Checkpoint管理

---

# Checkpoint管理

**対象バージョン**: v1.13.0以降

> **🧪 Beta・実験的機能**: Checkpoint機能は開発中です。ワークスペースのチェックポイントを管理します（会話のチェックポイントではありません）。機能は変更・削除される可能性があります。`q settings chat.enableCheckpoint true`で有効化してください。

## 📋 コマンド概要

Checkpoint管理機能は、ワークスペースの状態を保存・復元する機能です。開発の重要な節目でワークスペースの状態を記録し、必要に応じて以前の状態に戻ることができます。Git のような版数管理とは異なり、ワークスペース全体のスナップショットを管理します。

## 🚀 基本的な使い方

### Checkpoint管理コマンド一覧

| コマンド | 詳細説明 | 使用シーン |
|---------|---------|-----------|
| `/checkpoint init` | チェックポイントを手動で初期化 | チェックポイント機能を開始する時 |
| `/checkpoint list` | 全てのチェックポイントを一覧表示 | 利用可能なチェックポイントを確認したい時 |
| `/checkpoint restore [<tag>]` | 指定したチェックポイントにワークスペースを復元 | 以前の状態に戻したい時 |
| `/checkpoint expand <tag>` | 指定したチェックポイントの詳細を表示 | チェックポイントの内容を確認したい時 |
| `/checkpoint diff <tag1> [tag2]` | 2つのチェックポイント間の差分を表示 | 変更内容を確認したい時 |
| `/checkpoint restore <tag> --hard` | Checkpointに完全復元。復元後の会話履歴は削除される | 完全に以前の状態からやり直したい時 |
| `/checkpoint clean` | シャドウリポジトリを削除 | チェックポイントデータを完全に削除したい時 |

### 基本例

```bash
# Checkpoint機能を有効化
q settings chat.enableCheckpoint true

# チェックポイントを初期化
/checkpoint init

# チェックポイント一覧を確認
/checkpoint list

# 特定のチェックポイントに復元
/checkpoint restore v1.0.0
```

## ⚙️ オプション・引数

### `/checkpoint restore` コマンド

| オプション | 説明 | 使用例 |
|-----------|------|--------|
| `<tag>` | 復元するチェックポイントのタグ | `/checkpoint restore v1.0.0` |
| `--hard` | 完全復元（会話履歴も削除） | `/checkpoint restore v1.0.0 --hard` |

### `/checkpoint diff` コマンド

| 引数 | 説明 | 必須 |
|------|------|------|
| `<tag1>` | 比較元のチェックポイント | はい |
| `[tag2]` | 比較先のチェックポイント（省略時は現在の状態） | いいえ |

### チェックポイントの仕組み

- **シャドウリポジトリ**: ワークスペースの状態を別の場所に保存
- **自動作成**: 重要な変更時に自動的にチェックポイントを作成
- **タグ管理**: 各チェックポイントにタグを付けて管理
- **差分表示**: チェックポイント間の変更内容を確認可能

## 💡 実用例

### 例1: 開発の重要な節目でのチェックポイント作成

**シナリオ**: 新機能の実装前にワークスペースの状態を保存したい

```bash
# Checkpoint機能を有効化
q settings chat.enableCheckpoint true

# 現在の状態を初期チェックポイントとして保存
/checkpoint init

# チェックポイント一覧を確認
/checkpoint list

# 新機能実装後、自動的にチェックポイントが作成される
# （Q CLIが重要な変更を検出して自動作成）

# 作成されたチェックポイントを確認
/checkpoint list
```

**結果**: 開発の各段階でワークスペースの状態が保存され、安全に実験的な変更を行える

### 例2: 問題発生時の状態復元

**シナリオ**: 実装中に問題が発生し、以前の安定した状態に戻りたい

```bash
# 利用可能なチェックポイントを確認
/checkpoint list

# 出力例:
# Tag: feature-start (2025-11-13 10:00)
# Tag: api-implementation (2025-11-13 14:30)
# Tag: current (2025-11-13 16:45)

# 特定のチェックポイントの詳細を確認
/checkpoint expand feature-start

# 安定していた状態に復元
/checkpoint restore feature-start

# 復元後の状態を確認
/checkpoint list
```

**結果**: 問題が発生した変更を取り消し、安定した状態から再開できる

### 例3: 異なるアプローチの比較検討

**シナリオ**: 複数の実装アプローチを試して比較したい

```bash
# 現在の状態をベースラインとして保存
/checkpoint init

# アプローチA実装後のチェックポイント
/checkpoint list  # approach-a が自動作成される

# アプローチAの詳細を確認
/checkpoint expand approach-a

# ベースラインに戻る
/checkpoint restore baseline

# アプローチB実装後のチェックポイント
/checkpoint list  # approach-b が自動作成される

# 2つのアプローチを比較
/checkpoint diff approach-a approach-b

# より良いアプローチを選択して復元
/checkpoint restore approach-b
```

**結果**: 複数のアプローチを安全に試行し、最適な解決策を選択できる

## 🔧 トラブルシューティング

### よくある問題

#### 問題1: Checkpoint機能が使用できない

**症状**: `/checkpoint` コマンドが認識されない

**原因**: Checkpoint機能が有効化されていない

**解決策**:
```bash
# Checkpoint機能を有効化
q settings chat.enableCheckpoint true

# 設定を確認
q settings list | grep Checkpoint

# チャットを再起動
/quit
q chat
```

#### 問題2: チェックポイントが作成されない

**症状**: 変更を行ってもチェックポイントが自動作成されない

**原因**: 変更が軽微すぎる、または初期化されていない

**解決策**:
```bash
# 手動で初期化
/checkpoint init

# 現在の状態を確認
/checkpoint list

# 大きな変更を行ってテスト
# （ファイル作成、大幅な編集など）
```

#### 問題3: 復元が正しく動作しない

**症状**: `/checkpoint restore` を実行しても状態が変わらない

**原因**: チェックポイントデータの破損、または権限の問題

**解決策**:
```bash
# チェックポイントの詳細を確認
/checkpoint expand <tag>

# 別のチェックポイントで試行
/checkpoint restore <別のtag>

# 完全復元を試行
/checkpoint restore <tag> --hard

# 問題が続く場合はクリーンアップ
/checkpoint clean
/checkpoint init
```

#### 問題4: ディスク容量不足

**症状**: チェックポイント作成時に容量不足エラーが発生

**原因**: シャドウリポジトリが大量のディスク容量を使用

**解決策**:
```bash
# ディスク使用量を確認
df -h

# 古いチェックポイントを削除
/checkpoint clean

# 必要に応じて再初期化
/checkpoint init

# 不要なファイルを除外する設定を検討
```

#### 問題5: 差分表示が見づらい

**症状**: `/checkpoint diff` の出力が理解しにくい

**原因**: 大量の変更、またはバイナリファイルの変更

**解決策**:
```bash
# 特定のファイルタイプのみ比較
# （チェックポイント機能の制限内で）

# チェックポイントの詳細を個別に確認
/checkpoint expand tag1
/checkpoint expand tag2

# 外部ツールとの併用を検討
git diff --name-only
```

## 🔗 関連コマンド

- [基本コマンド・会話管理](01_basic-commands.md) - `/save`、`/load`による会話の保存
- [開発者向けコマンド](08_developer-commands.md) - `/logdump`による問題調査
- [TODO管理](06_todo-management.md) - タスク管理との連携

## 📖 参照元

- [チャット機能概要](../01_chat.md#checkpoint管理) - Checkpoint管理の概要
- [Checkpoint機能ガイド](../05_checkpoints.md) - Checkpoint機能の詳細仕様

---

最終更新: 2025年11月13日
