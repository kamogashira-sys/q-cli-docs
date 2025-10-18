# Checkpoint機能（実験的機能）

最終更新: 2025-10-11

---

## 📋 概要

> **🧪 実験的機能**: この機能は開発中です。予告なく変更される可能性があります。詳細は[実験的機能ガイド](07_experimental.md)を参照してください。

Checkpoint機能を使って、作業状態を保存・復元できます。

---

## 💾 Checkpointとは

会話の状態をGitコミットとして保存し、後で復元できる機能です。

Checkpointは以下の情報を保存します：
- ファイルの変更履歴
- 会話のコンテキスト
- 作業ディレクトリの状態

---

## 🚀 使い方

### 有効化

Checkpoint機能を有効にするには、以下のいずれかの方法を使用します：

**方法1: `/experiment`コマンドを使用（推奨）**

```
> /experiment
```

表示されるメニューから「Checkpoint」を選択してONに切り替えます。

**方法2: 設定コマンドを使用**

```bash
q settings chat.enableCheckpoint true
```

### Checkpoint初期化

Checkpointを使用する前に、初期化が必要です：

```
> /checkpoint init
```

このコマンドは、現在のディレクトリでCheckpoint機能を初期化します。

### Checkpoint一覧

保存されているCheckpointを確認します：

```
> /checkpoint list
```

オプション：
- `--limit <数>`: 表示するCheckpoint数を制限

例：
```
> /checkpoint list --limit 10
```

### Checkpoint復元

特定のCheckpointに復元します：

```
> /checkpoint restore <tag>
```

引数：
- `<tag>`: Checkpointタグ（例: 3、3.1）。省略すると対話的に選択できます

オプション：
- `--hard`: 完全復元モード（Checkpoint後に作成されたファイルを削除）

#### 復元モード

**デフォルトモード**:
- 追跡されているファイルの変更を復元
- Checkpoint後に作成された新しいファイルは保持

**ハードモード（--hard）**:
- Checkpointの状態に完全に一致させる
- Checkpoint後に作成されたファイルを削除

例：
```
> /checkpoint restore 3
> /checkpoint restore 3.1 --hard
```

---

## 📝 使用例

### 基本的なワークフロー

1. **初期化**:
   ```
   > /checkpoint init
   ```

2. **作業を進める**:
   ```
   > ファイルを編集してください
   ```

3. **Checkpoint一覧を確認**:
   ```
   > /checkpoint list
   ```

4. **特定のCheckpointに復元**:
   ```
   > /checkpoint restore 2
   ```

### 安全な復元

デフォルトモードでは、新しいファイルを保持します：

```
> /checkpoint restore 3
```

### 完全な復元

ハードモードでは、Checkpointの状態に完全に戻します：

```
> /checkpoint restore 3 --hard
```

---

## ⚠️ 注意事項

1. **実験的機能**: この機能は開発中のため、予告なく変更される可能性があります
2. **自動保存**: Checkpointは会話の進行に応じて自動的に作成されます
3. **Git統合**: Checkpointは内部的にGitコミットとして保存されます
4. **ハードモード**: `--hard`オプションは慎重に使用してください（ファイルが削除される可能性があります）
5. **初期化**: Checkpoint機能を使用する前に、`/checkpoint init`を実行してください

---

## 📚 関連ドキュメント

- [チャット機能](01_chat.md)
- [グローバル設定](../03_configuration/03_global-settings.md)
- [実験的機能](07_experimental.md)

---

最終更新: 2025-10-09
