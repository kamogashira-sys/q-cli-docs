[ホーム](../README.md) > [機能詳細ガイド](README.md) > v2.30 新機能

# 49. v2.30 新機能 — [V3] 起動時の切替プロンプトと CLI 3.0 の既定化・モデルフォールバック通知

## 概要

Kiro CLI **v2.30.0**（2026-10-12）では、起動時のプロンプトで **V3 への切り替え**を勧める段階的な展開が始まりました。公式 Changelog は、V3 が 10 月末に **CLI 3.0 の既定**になると説明しています。あわせて、V3 セッションでターンが別のモデルへ移ったことを示す通知が追加され、エージェントを V3 へアップグレードしたときに V2 のアクセス権限をより多く保持するようになり、画面リーダー・tmux・Knowledge 検索の問題が修正されました。系列ページ（`changelog/cli/2-30/`）に Patches 節はなく、v2.30 系列の版は v2.30.0 のみです。

- **機能追加**: チャット開始時の V3 への切り替え提案、[V3] モデルが切り替わったときの通知
- **改善**: アップグレード済みエージェントの権限の更新
- **バグ修正**: 6 件（画面リーダー、V2 のワークスペース読み取りアクセスと `fs_read` のスキル信頼の保持、tmux のスクロール、UI の描画位置、Classic と V2 の Knowledge 検索、Linux 端末の文字化け）

公式 Changelog の Learn more リンクが指す公式ドキュメントの本文を取得し、確認できた範囲を書いています。確認できなかった点は「未確認」と明記しています。

## ⚠ チャット開始時の V3 への切り替え提案 — CLI 3.0 の既定化

公式 Changelog（v2.30.0）によると、起動時のプロンプトは、10 月末に V3 が CLI 3.0 の既定になるのに先立って段階的に展開されているため、すぐには表示されない場合があります。表示されたら **Switch to V3 and upgrade my configs** を選ぶと、V3 を既定のハーネスとして保存し、エージェントの自動アップグレードを有効にし、カスタムエージェント設定の移行を開始します。`kiro-cli --v3` でいつでも V3 を試せます。

### 選択肢（公式 What's new in CLI V3）

公式 [What's new in CLI V3](https://kiro.dev/docs/cli/v3/)（Page updated: 2026-10-13）は、V2 の対話チャットを開始したときの切り替え提案を次のように説明しています。

| 選択肢 | 動作 |
|--------|------|
| **Switch to V3 and upgrade my configs** | このセッションを V3 で開始し、`chat.agentEngine` を `v3` として保存し、エージェント設定を今回と以後の起動でアップグレードする |
| **Remind me later** | このセッションは V2 のままにし、約 7 日後に再び提案する |
| **Don't ask again** | このセッションは V2 のままにし、提案を止める |

Esc は **Remind me later** と同じ扱いです。**Remind me later**・**Don't ask again**・Esc はハーネスを変更しません。`kiro-cli --v3` で V3 をいつでも開始できます。

### 実機 2.33.0 で確認した事項

| 項目 | 内容 |
|------|------|
| `kiro-cli chat --help` の `--v3` | 「Launch the next generation Kiro agent」 |
| `kiro-cli chat --help` の `--v2` | 「Use the V2 agent engine (the pre-3.0 default)」 |
| 設定 `chat.agentEngine` | 「Default agent engine: 'v1', 'v2' (default), or 'v3'」。公式 Settings リファレンス（Page updated: 2026-10-15）には掲載されていない |
| 設定 `chat.enableAutoAgentUpgrade` | 「Auto-upgrade V2 agent configs to the V3 format on launch: true (upgrade silently), false (never). Unset prompts once.」。公式 Settings リファレンスには掲載されていない |

```bash
# V3 を既定のハーネスとして保存する（実機 2.33.0 の chat.agentEngine の説明に基づく）
kiro-cli settings chat.agentEngine v3
```

### 公式ブログのロールアウトの案内

公式 Changelog が案内する [Kiro CLI V3 is rolling out as the default experience](https://kiro.dev/blog/cli-3/)（公式ブログ。ブログページに Page updated の表示はありません）は、次のように説明しています。

- 10 月 12 日から、V3 への切り替えを勧める起動時のプロンプトを段階的に展開し、CLI 3.0 のリリースは 10 月末の予定。この展開は Kiro CLI だけに適用される
- **Don't ask again** は、プロンプトを止めるだけで V2 に留めるものではなく、CLI 3.0 のリリース時に環境が V3 へアップグレードされる
- すでに V3 を使っている場合は、CLI 3.0 のロールアウトで V3 が既定になった後は `--v3` フラグを省略できる。V2 に戻すには `kiro-cli --v2`（その起動だけに適用）。V2 のセッションは V3 で再開できるが、V3 のセッションは V2 で再開できない
- CLI 3.0 では、インラインのシェル補完と CLI デスクトップアプリが廃止され、Classic も段階的に廃止される。Classic から TUI へ切り替えるには、エイリアスやショートカットから `--classic` を外して `kiro-cli` を起動する
- ACP クライアントは、エージェント設定の移行では更新されない。V3 の ACP サーバーは `kiro-cli acp --agent-engine=v3` で起動する（→ [48. v2.29 新機能](48_v229NewFeatures.md)）

### 公式間の食い違いと未確認事項

- 公式 Changelog v2.30.0（2026-10-12）とブログは、V3 が 10 月末に CLI 3.0 の既定になると説明しています。一方、公式 [What's new in CLI V3](https://kiro.dev/docs/cli/v3/)（Page updated: 2026-10-13）の冒頭の注記は、「Kiro CLI V3 の early release が利用可能」と説明し、「V3 は既存の 2.x と並行して動作し、オプトインするまで現在の設定は変わらない」と記載しています。このページは更新日が Changelog より新しいものの、10 月末の既定化には触れていません。本サイトは、リリース内容の一次情報である公式 Changelog と、ロールアウトを説明するブログの記述を採り、公式ドキュメントとの食い違いをここに注記します。CLI 3.0 の既定化が実際にいつ行われるかは、本ページの対象バージョン（v2.30.0〜v2.33.0）の公式情報では**未確認**です。
- **Don't ask again** の説明は、公式 What's new in CLI V3 が「このセッションは V2 のままにし、提案を止める」、ブログが「CLI 3.0 のリリース時に V3 へアップグレードされる」と、記述の範囲が異なります。両者を併記し、どちらが後の挙動を正確に表すかは**未確認**とします。
- v2.28.0 の Classic 向けの 3.0 切替提案との関係は公式に記載がなく**未確認**です（→ [47. v2.28 新機能](47_v228NewFeatures.md)）。
- V3 の概要は [09_v3/](../09_v3/README.md) を参照してください。

## [V3] モデルが切り替わったときの通知

V3 セッションで、モデルがリクエストを拒否した、または利用できず、ターンが別のモデルへ移った場合に、transcript に通知が表示されます（公式 Changelog v2.30.0）。別のモデルがターンを引き継いだことが分かり、返信が変わった理由に迷いません。

公式 [Terminal UI — Model fallback notices](https://kiro.dev/docs/cli/terminal-ui/#model-fallback-notices)（Page updated: 2026-10-20）の説明:

- V3 のターミナル UI セッションでは、モデルが拒否した、または利用できず、ターンが別のモデルへ移ったことを transcript が報告する
- 通知は、このターンに応答したモデル、モデルがこの会話のモデルになったかどうか、またはどのモデルも応答しなかったことを示す
- どのモデルも応答しなかった場合は、`/model` で別のモデルを選ぶ

V1 と V2 では、`/model fallback` でフォールバックを表示・設定・解除できます（公式 [Slash commands の `/model`](https://kiro.dev/docs/reference/slash-commands/#model)、Page updated: 2026-10-20）。V3 の通知は、フォールバック先を設定するコマンドではなく、移動を知らせる transcript の表示です。`/model fallback` は v2.27.1 で追加されました（→ [46. v2.27 新機能](46_v227NewFeatures.md)）。

## アップグレード済みエージェントの権限

### V2 の信頼設定の変更が V3 の権限に反映される（改善）

生成された V3 のフィールドが変更されていない、アップグレード済みのエージェントで V2 の信頼設定を変更すると、Kiro CLI が対応する V3 の権限を更新します（公式 Changelog v2.30.0）。

公式 [Upgrading agent configs — Refreshing upgraded agents](https://kiro.dev/docs/cli/v3/upgrade-agent/#refreshing-upgraded-agents)（Page updated: 2026-10-13）の説明:

- V2 の信頼設定と、生成された V3 の `permissions`・ツール・Hook が一致しなくなったとき、または移行そのものが改訂されたとき、Kiro は生成された V3 の部分を更新する。生成された部分を編集していなければ、エージェントは選択メニューに再び表示され、アップグレードは新しく生成した値に置き換える
- 生成された V3 のフィールドを手で編集すると、Kiro は自動での更新を止める。エージェントは選択メニューの **Universal · Out of Sync** に表示される。このグループを選ぶと、V2 の設定から V3 を再構築し、手動の V3 の編集を上書きする。前のファイルは `.bak` のバックアップとして保存される
- アップグレードの状態は、アップグレードしたファイルごとの `kiroUpgrade` マーカーに記録される

### V2 のワークスペース読み取りとスキル信頼の保持（バグ修正）

エージェントを V3 へアップグレードしたときに、V2 のワークスペース読み取りアクセスと `fs_read` のスキル信頼を保持するよう修正されました（公式 Changelog v2.30.0）。公式 [Upgrading agent configs — What gets converted](https://kiro.dev/docs/cli/v3/upgrade-agent/#what-gets-converted) の説明:

| 項目 | 変換 |
|------|------|
| ワークスペースの読み取り | 移行後の設定は `./**` に対する `fs_read` を許可し、エージェントがワークスペースのファイルを確認なしで読める。deny ルールは引き続き優先される |
| スキルの信頼 | V2 の設定が組み込みツールをすべて信頼する場合、または読み取りツールを含み `fs_read` を信頼する場合、移行はスキルの読み込みも信頼する。V2 の読み取り制限（`deniedPaths`）がスキルのファイルに届きうる場合は、V3 でスキルが承認を求め、診断が `skill-read-restrictions` を報告する |

`/upgrade-agent` 全般は [34. /upgrade-agent](34_v214UpgradeAgent.md) を参照してください。

## スクリーンリーダー

画面リーダーが、`/settings display` の Screen reader オプションを通じて、フル TUI のストリーミング返信を追従するよう修正されました（公式 Changelog v2.30.0）。

公式 [In-session settings — Screen reader support](https://kiro.dev/docs/cli/chat/settings/#screen-reader-support)（Page updated: 2026-10-20）の説明:

- 対象はフル TUI のみ。返信がストリーミングされていてプロンプトが空の間、隠れた端末カーソルが返信テキストを追従する。入力を始める、メニューを開く、承認に応答する、のいずれかでカーソルは入力へ戻る
- 設定は `chat.screenReader`（`auto`・`on`・`off`）。**auto**（既定）は、ローカルの Mac で VoiceOver が動いているかを 1 回確認し、SSH などのリモート接続、他のプラットフォーム、確認に失敗した場合や時間がかかりすぎた場合は無効のままなので、その場合は **on** を選ぶ
- サポートが有効なとき、IME の入力位置が異なって表示されることがある。設定はグローバルのみで、1 回の起動だけ上書きするには `KIRO_SCREEN_READER` に `auto`・`on`・`off` を設定する

```bash
KIRO_SCREEN_READER=on kiro-cli chat
```

公式 [Settings リファレンス](https://kiro.dev/docs/reference/settings/)（Page updated: 2026-10-15）にも `chat.screenReader` と `KIRO_SCREEN_READER` が掲載されています。実機 2.33.0 の `kiro-cli settings list --all` の説明も、同じ 3 値（`auto`・`on`・`off`）を示します。

## その他のバグ修正の要点

| 内容（公式 Changelog v2.30.0） | 公式ドキュメントでの確認 |
|----------------------------|------------------------|
| tmux でスクロールバックしても、長い返信の後に空白行だけの画面が表示されない | 公式ドキュメントに記載なし（**未確認**） |
| 末尾に改行のない出力の後に Kiro CLI を起動しても、UI がずれた位置に描画されない | 公式ドキュメントに記載なし（**未確認**） |
| Classic と V2 の Knowledge 検索が、小さな knowledge base からチャンクを黙って落とさない | 公式 [Slash commands の `/knowledge`](https://kiro.dev/docs/reference/slash-commands/#knowledge) は、サブコマンド・追加オプション・V3 での既定有効を説明しているが、チャンクの扱いの記述は確認できなかった（**未確認**） |
| 一部の Linux 端末とリモートデスクトップで、チャット内のアイコン周辺に文字化けや余分な文字が出る | 公式ドキュメントに記載なし（**未確認**） |

修正項目の完全な一覧は [変更履歴の v2.30.0](../02_update/01_changelog.md) を正とします。

## 関連リンク

### 本サイト

- [48. v2.29 新機能](48_v229NewFeatures.md)
- [47. v2.28 新機能](47_v228NewFeatures.md)
- [46. v2.27 新機能](46_v227NewFeatures.md)
- [34. /upgrade-agent](34_v214UpgradeAgent.md)
- [18. Terminal UI](18_TerminalUI.md)
- [09_v3/（Kiro CLI v3 Early Access）](../09_v3/README.md)
- [Settings リファレンス](../04_reference/01_settings.md)
- [変更履歴](../02_update/01_changelog.md)

### 公式情報源

- [Kiro CLI Changelog v2.30](https://kiro.dev/changelog/cli/2-30/)
- [Kiro CLI V3 is rolling out as the default experience（公式ブログ）](https://kiro.dev/blog/cli-3/)
- [What's new in CLI V3](https://kiro.dev/docs/cli/v3/)
- [Terminal UI — Model fallback notices](https://kiro.dev/docs/cli/terminal-ui/#model-fallback-notices)
- [Upgrading agent configs](https://kiro.dev/docs/cli/v3/upgrade-agent/)
- [In-session settings — Screen reader support](https://kiro.dev/docs/cli/chat/settings/#screen-reader-support)
- [Slash commands](https://kiro.dev/docs/reference/slash-commands/)
- [Settings リファレンス](https://kiro.dev/docs/reference/settings/)
- `kiro-cli chat --help` / `kiro-cli settings list --all`（実機 2.33.0）

**最終更新**: 2026-10-21
**対象バージョン**: Kiro CLI v2.30.0+（V3 への切り替え提案・モデルフォールバック通知は V3 Early Access）
