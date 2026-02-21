# データベース設計書
## KV との分割統治について
Key / Value StoreであるKVについてAPIキー／シークレットの照合を行い、ユーザー管理と切り離す
|テーブル／ネームスペース名|種別<BR />(TBL/NS)|用途|
|---|---|---|
|api_keys|NS|APIキー管理|
|status|NS|ステータス管理|
|users|TBL|ユーザー管理|
|domains|TBL|ドメイン|
|hosts|TBL|ホスト名管理|

## ネームスペース／テーブル設計
<details>
<summary>api_keys</summary>

 - キー : UUID6(32バイト)

```json
{
    "secret":"シークレット",
    "userId":"ユーザーID"
}
```
</details>

<details>
<summary>histories</summary>

 - キー : FQDNホスト名(128バイトでバリデーション)

```json
{
    "eventId": {
        "lastIpAddress":"最終アクセスのあったIPアドレス",
        "userId":"ユーザーID"
    }
}
```
</details>
</details>

<details>
<summary>logs</summary>

 - キー: イベントID
```json
{
    "eventId": {
        "lastIpAddress":"最終アクセスのあったIPアドレス",
        "userId":"ユーザーID"
    }
}
```
</details>

### users
ユーザー管理
|カラム名|PK|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---|:---:| :--- | :--- | :--- |
|id |◯| NOT NULL | True | False |integer|ユーザーID|
|email|  |NOT NULL<br /> UNIQUE| - | EMAIL |String(128)|Eメールアドレス|
|password||NOT NULL|- |- |String(24)|パスワード|