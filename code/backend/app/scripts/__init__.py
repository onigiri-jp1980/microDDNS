"""ローカル／環境初期化用の CLI スクリプト（`python -m app.scripts.<module>`）。"""

import base64
import hmac
import hashlib

def create_hash(email:str, client_id:str, client_secret:str):
    # 1. EMAIL + CLIENT_ID を連結
    message = f"{email}{client_id}".encode("utf-8")
    secret = client_secret.encode("utf-8")

    # 2. HMAC-SHA256 を計算（バイナリ）
    digest = hmac.new(secret, message, hashlib.sha256).digest()

    # 3. Base64 エンコード
    return base64.b64encode(digest).decode("utf-8")
