# データベース設計書
|テーブル名|用途|
|---|---|
|api_keys|APIキー管理|
|status|ステータス管理|
|users|ユーザー管理|
|domains|ドメイン|
|hosts|ホスト名管理|

## テーブル設計
### users
- ユーザー管理
  - 認証は

|カラム名|P|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---|:---:| :--- | :--- | :--- |
|email|  |NOT NULL<br /> UNIQUE| - | EMAIL |String(128)|Eメールアドレス|
|userId |◯| NOT NULL | True | False |integer|ユーザーID|
|password||NOT NULL|- |- |String(24)|パスワード|