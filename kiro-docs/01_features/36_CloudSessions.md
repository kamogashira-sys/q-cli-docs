[ホーム](../README.md) > [機能詳細ガイド](README.md) > Cloud Sessions（クラウドセッション・プレビュー）

---

# Cloud Sessions（クラウドセッション・プレビュー）

> ⚠️ **Preview 機能のため仕様変更の可能性あり**。本ページの内容は執筆時点の公式ドキュメントに基づきますが、正式リリース時に仕様が変わる可能性があります。

## 概要

Kiro CLI **v2.17.0**（2026-08-11）で、マネージドクラウドサンドボックス上で Kiro agent harness を実行する **Cloud Sessions（プレビュー）** が追加されました。IDE・CLI・Web・Mobile の全サーフェスが同一セッションにアタッチ可能で、いずれかのクライアントを切断してもエージェントはクラウド上で継続動作します。承認待ちのリクエストは、次に接続したクライアントに提示されます。

**対応バージョン**: セッションの作成・アタッチは **Kiro CLI v2.17.0 以降**が必須。「Open with Kiro CLI」操作自体は **v2.16.2 以降**で先行対応済みです。

**出典**: [Cloud sessions - Kiro CLI Documentation](https://kiro.dev/docs/cloud-sessions/)（Page updated: 2026-08-14）、[公式Changelog v2.17](https://kiro.dev/changelog/cli/2-17/)、[公式Changelog v2.18](https://kiro.dev/changelog/cli/2-18/)

---

## 📋 目次

- [起動方法](#起動方法)
- [⚠️ 破壊的変更（v2.18.0）: 既定オプトイン化](#️-破壊的変更v2180-既定オプトイン化)
- [前提条件](#前提条件)
- [制約](#制約)
- [設定の扱い](#設定の扱い)
- [Kiro Web (Preview) との関係](#kiro-web-preview-との関係)
- [姉妹サイトとの役割分担](#姉妹サイトとの役割分担)
- [関連リンク](#関連リンク)

---

## 起動方法

```bash
# 新規 Cloud Session を作成
kiro-cli --cloud
# または
kiro-cli chat --cloud

# リポジトリを紐付けて作成
kiro-cli chat --cloud --repo <repository-url>

# セッション内でリポジトリを後から紐付け（/repo ピッカー）
/repo

# 他サーフェス（Web/Mobile/IDE 等）で開始したセッションにアタッチ
kiro-cli chat --resume-id <cloud-session-id>
```

- `--cloud`: マネージドクラウドサンドボックス上で新規セッションを作成
- `--repo`（起動時フラグ）または `/repo`（セッション内ピッカー）: リポジトリを紐付け。作成後も `/repo` で追加可能
- `--resume-id <session-id>`: ローカル／クラウド両方のセッション ID を受理する既存フラグ。クラウドセッション ID を指定した場合はクラウドサンドボックスにアタッチする（→ [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md)）
- クラウド・ローカルセッションは同一のセッションピッカー（`--resume-picker`）に共に表示される

---

## ⚠️ 破壊的変更（v2.18.0）: 既定オプトイン化

Kiro CLI **v2.18.0**（2026-08-12）で、Cloud Sessions は**既定で opt-in（無効）** に変更されました。

- 管理者が「Settings > Kiro Settings」の **Cloud Sessions (Preview)** トグル（旧称「Kiro Web (Preview)」）を明示的に有効化しない限り、組織内では利用できません
- **未設定の組織はトグルが「無効」に解決される**ため、これまでトグルを設定していなかった組織は、管理者がオプトインするまで Cloud Sessions を利用できなくなります
- CLI 内蔵 changelog は本変更を「enterprise governance controls 対応」という表現で記載していますが、**利用者への影響が大きい破壊的変更**であるため、本サイトは公式 Web サイトの表現（既定オプトイン化）を採用しています

---

## 前提条件

- 有料 Kiro サブスクリプション（**Pro 以上**）
- リポジトリを使った作業を行う場合は **GitHub または GitLab** への接続
- プレビュー期間中は **`us-east-1`** リージョン限定

---

## 制約

Cloud Sessions はプレビュー機能のため、以下が現時点でサポートされていません。

- **Supervised mode 非対応**（Autopilot / Autonomous モードのみ利用可能）
- **ブランチ選択不可**（リポジトリのブランチは固定）
- **リポジトリセットは作成時固定**（セッション作成後にリポジトリを変更することはできない。追加紐付けは `/repo` で可能）
- **セッションリネーム不可**
- **ローカルファイル操作系機能が非対応**: エディタ diff 表示、checkpoint/revert、`#File` 等のファイルピッカー

---

## 設定の扱い

Cloud Sessions では、プロジェクト設定と個人設定の適用方法が異なります。

| 設定の種類 | 保存場所 | 適用方法 |
|-----------|---------|---------|
| プロジェクト設定 | リポジトリ内 `.kiro/` | リポジトリのクローンと同時に**自動適用** |
| 個人設定 | `~/.kiro/` | **自動適用されない**。Kiro Web 設定の「Cloud configuration」から明示的に同期が必要 |

---

## Kiro Web (Preview) との関係

Cloud Sessions の管理者向け設定は、IAM Identity Center を利用する組織向けに旧称 **「Kiro Web (Preview)」** として提供されていた設定の後継です。v2.17.0 のリリース時点で、既存に有効化済みの組織は継続して有効なまま、新規組織はオプトインが必要という扱いになっています（v2.18.0 でこのオプトイン要件が全組織に既定で適用されるよう変更 → [破壊的変更](#️-破壊的変更v2180-既定オプトイン化)）。

---

## 姉妹サイトとの役割分担

Cloud Sessions がアタッチする実行環境そのもの（Web UI・Mobile UI の詳細な操作方法）は、姉妹サイトである **[猫でもわかるKiro Web アップデート情報](https://github.com/kamogashira-sys/kiro-web-docs)** の対象です。本サイト（Kiro CLI）では、CLI からの Cloud Sessions の起動・アタッチ・操作方法を解説します。

> **IDE・CLI・Web は別製品**です。Cloud Sessions は全サーフェスから同一セッションにアタッチできますが、各サーフェスでの UI・操作性の詳細はそれぞれの姉妹サイトを参照してください。

---

## 関連リンク

### 関連機能（本サイト）

- [04_reference/03_cli-commands.md](../04_reference/03_cli-commands.md) — `--cloud`・`--repo`・`--resume-id` フラグの詳細
- [37. Voice Mode](37_VoiceMode.md) — 同じ v2.18.0 で追加されたリモート音声サーバー機能（クラウドデスクトップでの音声入力に利用可能）

### バージョン関連

- [Changelog v2.17.0](../02_update/01_changelog.md#v2170-cli2026-08-11) — Cloud Sessions（プレビュー）の初出
- [Changelog v2.16.2](../02_update/01_changelog.md#v2162-cli2026-08-06) — 「Open with Kiro CLI」対応（前段機能）
- [Changelog v2.18.0](../02_update/01_changelog.md#v2180-cli2026-08-12) — 既定オプトイン化（破壊的変更）

### 公式情報源

- [Cloud sessions - Kiro CLI Documentation](https://kiro.dev/docs/cloud-sessions/)（Page updated: 2026-08-14）
- [公式Changelog v2.17](https://kiro.dev/changelog/cli/2-17/)
- [公式Changelog v2.18](https://kiro.dev/changelog/cli/2-18/)

---

**Page updated**: 2026-08-16（本サイト初版）
