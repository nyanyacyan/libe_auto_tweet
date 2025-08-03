# セキュリティキー等のガイドライン

## 【目的】

このガイドは、APIキーやID・パスワード、クラウド認証情報（例：GCP・AWSのJSONファイル）などの機密情報を安全に管理・共有するためのルールをまとめたものです。
プロジェクトごとに情報の保存場所・形式・取り扱い方法を統一し、意図しない漏洩を防ぎます。


<br>



## 【理由】

- 機密情報が誤ってGitに含まれると、外部に漏洩する危険があるため
- `.env` ファイルはビルド配布時に不要・不便であるため（特に `exe` 納品時）
- 他の開発者が迷わず設定できるよう、保存先や書き方を明確にするため



<br>

## 【ルール】

### 🔐 保存先について

- セキュリティ関連のキーやID/パスワードはすべて以下のファイルに保存します：
```plaintext
installer/
└── config/
    ├── config.json                # APIキーやID/PASSなど
    ├── gcp_service_account.json   # GCPサービスアカウントキー
    └── aws_credentials.json       # AWS認証情報（必要に応じて）
```


<br>


---

### 📝 記述形式について

- JSON形式で記述し、キーはすべて **大文字（スネークケース）** にします
- 各サービス名ごとにネストして分類します（例：`SLACK`, `GOOGLE`, `OPENAI` など）

#### 記述例：

```json
{
  "SLACK": {
    "ENDPOINT_URL": "https://hooks.slack.com/...",
    "ID": "your_id",
    "PASS": "your_password"
  },
  "OPENAI": {
    "API_KEY": "sk-xxxxx"
  }
}
```
---

<br>



## 🛡 Gitへの対策
- config.json は 絶対にGitに含めないでください。
- 誤ってステージング・コミットしないよう、常に git status を確認しましょう。
- .gitignore に以下のパスが含まれていることを確認してください：
```bash
*config.json
```

<br>


## 【ポイント】
- .env ファイルは使用しません（exe形式での納品を想定するため）
- config.json を使うことで、環境に依存せず読み込める利点があります
- 本番環境での設定ファイルは開発者間で直接渡す（例：手渡し・暗号化ファイルで送信）


<br>



## 【補足】
- config.json の読み込み処理は、config_loader.py や config_manager.py などの専用ファイルで一元管理すると保守しやすくなります。
- キー名（SLACK, OPENAI など）は今後統一リストで管理することも検討してください。

<br>

## ✅ セキュリティキー管理チェックリスト

セキュリティキーやAPI認証情報を扱う際には、以下を確認しましょう：

- [ ] `installer/config/` 以下に config.json を作成し機密情報をまとめた
- [ ] config.json は JSON形式で書き、キー名はすべて大文字で統一した
- [ ] サービスごとにネスト構造を使って分類した（例："SLACK", "OPENAI"）
- [ ] .env ファイルは使用していない（exe化を想定）
- [ ] config.json を Git に絶対に含めていない（git status で確認済）
- [ ] .gitignore に `*config.json` の記述が含まれている
- [ ] config.json の内容は、暗号化や安全な方法でチームに共有した
- [ ] 読み込み処理は `config_loader.py` など専用ファイルで一元化している

