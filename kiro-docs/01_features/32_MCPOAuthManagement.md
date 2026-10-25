[ホーム](../README.md) > [機能詳細ガイド](README.md) > MCP OAuth 認証管理

---

# MCP OAuth 認証管理・事前登録アプリ対応

## 概要

リモート（HTTP）MCP サーバーの **OAuth 認証**を制御・運用するための機能群です。v2.3.0 で追加された `oauth.clientId` 設定を土台に、**v2.11.0** で認証フローを操作する専用コマンド（`/mcp auth`・`/mcp cancel-auth`・`/mcp logout`）と MCP パネルのショートカットが加わり、**v2.12.0** で「事前登録済み OAuth アプリ」への接続（`clientSecret`・カスタム `redirectUri`・Dynamic Client Registration のスキップ）に対応しました。

これにより、トークン失効や認証フローの停止といったトラブル時に、セッションを再起動したり資格情報を手動削除したりせずに復旧できます。Figma のように事前登録アプリ（client secret 必須）を要求するサーバーにも接続できます。

## 認証管理コマンド（v2.11.0）

リモート MCP サーバーの OAuth 資格情報をその場で制御します。

| コマンド | 動作 |
|---------|------|
| `/mcp auth` | OAuth 再認証を強制（トークンが失効・無効になったとき） |
| `/mcp cancel-auth` | ブラウザ確認待ちで停止した認証フローを中止 |
| `/mcp logout` | 保存済みの OAuth 資格情報を削除 |

**MCP パネルのショートカット**（ステータスビュー）:

| キー | 動作 |
|------|------|
| `^A` | 認証を強制（auth） |
| `^X` | 認証を中止（cancel-auth） |
| `^R` | 資格情報を削除（logout） |

> 公式: [`/mcp auth`（スラッシュコマンドリファレンス）](https://kiro.dev/docs/reference/slash-commands/#mcp-auth)

## 事前登録アプリ向け OAuth 設定（v2.12.0）

MCP サーバーごとの OAuth 設定（`~/.kiro/settings/mcp.json` のサーバー定義内）で、事前登録済みアプリに対応する項目が拡張されました。設定キーは **camelCase** です。

| 設定キー | 説明 | 追加/対応 |
|---------|------|----------|
| `clientId` | 事前登録アプリのクライアント ID。設定すると **Dynamic Client Registration（DCR）をスキップ**し、自身のアプリとして認証 | v2.3.0（DCR スキップは v2.12.0） |
| `clientSecret` | トークンエンドポイント認証を要する confidential client 向けのクライアントシークレット | **v2.12.0** |
| `redirectUri` | カスタムコールバックパスを含む**フル URL**（例 `http://localhost:7778/oauth/callback`）。コールバックホストは安全のため **localhost に限定** | **v2.12.0** |

### 設定例（`~/.kiro/settings/mcp.json`）

```json
{
  "mcpServers": {
    "example-remote": {
      "url": "https://mcp.example.com",
      "oauth": {
        "clientId": "my-registered-app-id",
        "clientSecret": "my-client-secret",
        "redirectUri": "http://localhost:7778/oauth/callback"
      }
    }
  }
}
```

> スキーマ・キー名の正準は公式リファレンスに従ってください（本サイトは公式表記の camelCase を採用）。

## 使用例

1. リモート MCP サーバーのトークンが失効し接続に失敗する → `/mcp auth`（または MCP パネルで `^A`）で再認証。
2. ブラウザ認可待ちのまま固まった → `/mcp cancel-auth`（`^X`）で中止し、やり直す。
3. 資格情報をローテーションしたい／別アカウントに切り替えたい → `/mcp logout`（`^R`）で削除してから再認証。
4. Figma など事前登録アプリ必須のサーバー → `mcp.json` の `oauth` に `clientId` と `clientSecret` を設定（DCR は自動スキップ）。

## 注意点・制限事項

- コールバックホストは **localhost（loopback）に限定**されます（`redirectUri` のフル URL 対応時も検証されます）。
- 設定キーは **camelCase**（`clientId` / `clientSecret` / `redirectUri`）。CLI 内蔵 changelog では snake_case 表記（`client_id` 等）で説明される場合がありますが、`mcp.json` の設定キーは camelCase です。
- 認証管理コマンドとパネルショートカットは **リモート（OAuth 対応）MCP サーバー**が対象です。
- 組織管理者が MCP を無効化している場合は、ガバナンスに従いメッセージが表示されます。

## v2.29.0 以降の変更

| 版 | 変更（出典: 公式 Changelog） |
|----|---------------------------|
| v2.29.0（2026-10-09） | V2 と V3 が MCP OAuth の認可 URL を表示するようになり、SSH や tmux のセッションからも開ける（[Changelog v2.29](https://kiro.dev/changelog/cli/2-29/)） |
| v2.29.1（2026-10-10） | Classic と V2 の MCP OAuth サインインが、issuer を要求するサーバーで動作する（[Changelog v2.29 の Patches 節](https://kiro.dev/changelog/cli/2-29/#patch-2-29-1)） |
| v2.31.0（2026-10-13） | V3 の MCP ツールが、streamable HTTP のサーバーがセッションを切断した後も動作し続ける（[Changelog v2.31](https://kiro.dev/changelog/cli/2-31/)） |
| v2.32.0（2026-10-15） | MCP OAuth のリンクは、サーバーが接続すると消え、通知にサーバー名が表示される。V3 で、組織の MCP レジストリから取得した MCP サーバーが、レジストリの `oauth` と `oauthScopes` の設定を使う（[Changelog v2.32](https://kiro.dev/changelog/cli/2-32/)） |
| v2.33.1（2026-10-21） | V3 で、MCP サインインの後に固定された OAuth コールバックポートを占有したままにしない。利用できないオプションの Power の MCP サーバーがプロンプトのターンをブロックしない。V3 のレジストリから追加した MCP サーバーがカタログのパッケージバージョンで起動する。`kiro-cli mcp add --agent` が `tools` に含まれないエージェントにも付与する（[Changelog v2.33.1](https://kiro.dev/changelog/cli/2-33-1/)。→ [53. v2.34 新機能](53_v234NewFeatures.md)） |
| v2.34.0（2026-10-23） | V3 のヘッドレスモードが、対話セッションで保存された MCP サインインを再利用する。ローカルの V3 セッションで、MCP ツールがフォームやリンクで入力を求める（MCP elicitation。URL 型は OAuth の認可フローの完了にも使われる）。HTTP のリモート MCP サーバーが同一オリジンのリダイレクトだけに従う（[Changelog v2.34](https://kiro.dev/changelog/cli/2-34/)。→ [53. v2.34 新機能](53_v234NewFeatures.md)） |

公式 [MCP Registry の OAuth for remote registry servers](https://kiro.dev/docs/mcp/registry/#oauth-for-remote-registry-servers)（公式更新日 2026-10-20）は、Kiro CLI V3 が、組織のレジストリが提供するリモートサーバーの `oauth` と `oauthScopes` の設定を使うこと、一致するレジストリの上書きでローカル用にこれらの値を置き換えられること、これらのフィールドは `mcp.json` のリモートサーバーと同じ形式であることを説明しています。公式 [MCP configuration](https://kiro.dev/docs/mcp/configuration/)（公式更新日 2026-10-07）は、認可サーバーの `issuer` が RFC 8414 に従って完全に一致する必要があること（「OAuth issuer mismatch」）を説明していますが、v2.29.1 の修正との対応関係は記載がなく**未確認**です。認可 URL の表示（v2.29.0）と OAuth リンクの消去（v2.32.0）に対応する記述も、公式の MCP configuration・MCP Registry・Slash commands には確認できず、**未確認**です。詳細は [48. v2.29 新機能](48_v229NewFeatures.md)・[51. v2.32 新機能](51_v232NewFeatures.md) を参照してください。

## 関連リンク

- [MCP OAuth 設定（公式リファレンス）](https://kiro.dev/docs/mcp/configuration/#oauth-configuration)
- [`/mcp auth`（公式スラッシュコマンドリファレンス）](https://kiro.dev/docs/reference/slash-commands/#mcp-auth)
- [04_reference/02_slash-commands.md](../04_reference/02_slash-commands.md) — `/mcp` サブコマンドの一覧
- [12. Remote Authentication](12_RemoteAuth.md) — ユーザー側のリモート認証（SSO 等。MCP サーバー OAuth とは別）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — v2.11.0 / v2.12.0 の変更履歴

---

**最終更新**: 2026-10-25  
**対象バージョン**: Kiro CLI v2.12.0（認証管理コマンドは v2.11.0。v2.29.0〜v2.34.0 の変更を追記）
