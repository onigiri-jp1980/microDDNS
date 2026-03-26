# データベース設計書
|テーブル名|用途|
|---|---|
|api_keys|APIキー管理|
|status|ステータス管理|
|users|ユーザー管理|
|domains|ドメイン|
|hosts|ホスト名管理|

## テーブル設計
### api_keys
- APIキー管理

|カラム名|PK|SK|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---:|:---|:---:| :--- | :--- | :--- |
|secret|◯||NOT NULL|-|HASH(PK)|String(32)|APIシークレット|
|userId||◯|NOT NULL|-|RANGE(SK)|String(36)|Cognito上のユーザーID|
|createdAt|||NOT NULL|-|-|datetime|作成日時|
|updatedAt|||NOT NULL|-|-|datetime|更新日時|
|isActive|||NOT NULL|False|-|boolean|有効フラグ|

### hosts
- ホスト名管理

|カラム名|PK|SK|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---:|:---|:---:| :--- | :--- | :--- |
|fqdn|◯||NOT NULL|-|HASH|string|FQDN（パーティションキー）|
|apiKey||◯|NOT NULL|-|RANGE|string|APIキー（ソートキー）|
|ipAddress|||NOT NULL|-|-|string|IPアドレス|
|isActive||NOT NULL|False|-|boolean|有効フラグ|
|createdAt|||NOT NULL|-|-|datetime|作成日時|
|updatedAt|||NOT NULL|-|-|datetime|更新日時|

### users
- ユーザー管理

|カラム名|PK|SK|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---:|:---|:---:| :--- | :--- | :--- |
|id|◯||NOT NULL|-|HASH|integer|ユーザーID（パーティションキー）|
|cognitoId||◯|NOT NULL|-|RANGE|string|CognitoユーザーID（ソートキー）|
|email|||NOT NULL|-|-|string|Eメールアドレス|
|createdAt|||NOT NULL|-|-|datetime|作成日時|
|updatedAt|||NOT NULL|-|-|datetime|更新日時|

### domains
- ドメイン管理

|カラム名|PK|SK|制約|AutoIcrement|Index|Type|用途|
|:---|:---:|:---:|:---|:---:| :--- | :--- | :--- |
|domain|◯||NOT NULL|-|HASH|string|ドメイン名（パーティションキー）|
|apiKey||◯|NOT NULL|-|RANGE|string|APIキー（ソートキー）|
|secret|||NULL許容|-|-|string|SecetManager/ParameterStoreのARNを格納|
|isActive|||NOT NULL|False|-|boolean|有効フラグ|
|createdAt|||NOT NULL|-|-|datetime|作成日時|
|updatedAt|||NOT NULL|-|-|datetime|更新日時|