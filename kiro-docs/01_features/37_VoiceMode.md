[ホーム](../README.md) > [機能詳細ガイド](README.md) > Voice Mode（音声入力）

---

# Voice Mode（音声入力）

## 概要

Kiro CLI **v2.18.0**（2026-08-12）で、オンデバイス音声認識によるプロンプト入力機能 **`/voice`** が追加されました。`/voice` コマンド、`Ctrl+O`、または `Space` の長押しで録音を開始できます。

発話中は部分的な文字起こし結果がリアルタイムでストリーム表示され、`Enter` キーまたは無音状態の自動検出で確定します。文字起こしは既定で **Whisper モデルによるオンデバイス処理**が行われ、音声データがマシン外に送信されることはなく、クラウド API キーも不要です。初回利用時にはモデルのダウンロードについて明示的な確認が行われ、モデルは1回だけダウンロードされます。

`--continuous` フラグを指定すると、ハンズフリーでの連続対話が可能になります。

**出典**: [Voice mode - Kiro CLI Documentation](https://kiro.dev/docs/cli/voice/)（Page updated: 2026-08-14）、[公式Changelog v2.18](https://kiro.dev/changelog/cli/2-18/)

> ⚠️ **出典に関する注記**: `/voice` は公式 [Slash commands](https://kiro.dev/docs/reference/slash-commands/) ページ（Page updated: 2026-08-12）には**掲載されていません**（2026-08-16実測確認）。本サイトは一次情報として公式 Voice mode ページと CLI 内蔵 changelog v2.18.0 を採用しています。

---

## 📋 目次

- [起動方法](#起動方法)
- [リモート音声サーバー（クラウドデスクトップ向け）](#リモート音声サーバークラウドデスクトップ向け)
- [設定](#設定)
- [制約](#制約)
- [関連リンク](#関連リンク)

---

## 起動方法

```bash
# チャット内でコマンドとして起動
> /voice

# キーボードショートカット
Ctrl+O

# Space の長押しでも録音開始

# ハンズフリーの連続対話モード
> /voice --continuous
```

録音中は発話内容がリアルタイムで部分テキストとして表示され、`Enter` を押すか、一定時間の無音（既定5秒、`voice.silenceTimeout` で変更可）が検出されると文字起こしが確定します。

---

## リモート音声サーバー（クラウドデスクトップ向け）

マイクを持たないクラウドデスクトップ（VDI・リモート開発環境等）から音声入力を利用するため、ローカルマシンで音声サーバーを起動し、SSH リバーストンネル経由でリモート側から利用する仕組みが提供されています。

```bash
# ローカルマシンで音声サーバーを起動
kiro-cli voice-serve

# クラウドデスクトップ側でワンステップ設定
kiro-cli voice-cloud-setup <hostname>
```

`kiro-cli voice-cloud-setup` は、対象ホストへの SSH リバーストンネル設定を含むワンステップのセットアップコマンドです（オプション: `--port`／`--remote-bin`／`-i`。詳細は [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md)）。

---

## 設定

`voice.*` の6つの設定キー（モデルサイズ・言語・無音タイムアウト・最大録音時間・自動送信・リモートサーバー URL）は [04_reference/01_settings.md](../04_reference/01_settings.md#9-voice音声入力) の「9. Voice（音声入力）」節を参照してください。

---

## 制約

- **マイクが必須**です（マイクを持たない環境では[リモート音声サーバー](#リモート音声サーバークラウドデスクトップ向け)の利用が必要）

---

## 関連リンク

### 関連機能（本サイト）

- [04_reference/01_settings.md](../04_reference/01_settings.md#9-voice音声入力) — `voice.*` 設定6キーの詳細
- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `kiro-cli voice-serve`・`kiro-cli voice-cloud-setup` の詳細
- [36. Cloud Sessions](36_CloudSessions.md) — クラウドデスクトップでの利用シーンが重なる関連機能

### バージョン関連

- [Changelog v2.18.0](../02_update/01_changelog.md#v2180-cli2026-08-12) — `/voice` の初出

### 公式情報源

- [Voice mode - Kiro CLI Documentation](https://kiro.dev/docs/cli/voice/)（Page updated: 2026-08-14）
- [公式Changelog v2.18](https://kiro.dev/changelog/cli/2-18/)

---

**Page updated**: 2026-08-16（本サイト初版）
