#! /usr/bin/env python3
import base64
import hmac
import hashlib
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--email', type=str, required=True)
    parser.add_argument('--client-id', type=str, required=True)
    parser.add_argument('--client-secret', type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    create_hash(args)

def create_hash(args):
    # 1. EMAIL + CLIENT_ID を連結
    message = f"{args.email}{args.client_id}".encode("utf-8")
    secret = args.client_secret.encode("utf-8")

    # 2. HMAC-SHA256 を計算（バイナリ）
    digest = hmac.new(secret, message, hashlib.sha256).digest()

    # 3. Base64 エンコード
    return base64.b64encode(digest).decode("utf-8")


if __name__ == "__main__":
    main()