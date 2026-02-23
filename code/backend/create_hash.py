#! /usr/bin/env python3
import base64
import hmac
import hashlib
from os import environ as env
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--email','-e', type=str, default=env.get('EMAIL', 'test@example.com'))
    parser.add_argument('--client-id','-i', type=str, default=env.get('COGNITO_CLIENT_ID', 'test'))
    parser.add_argument('--client-secret','-s', type=str, default=env.get('COGNITO_CLIENT_SECRET', 'test'))
    return parser.parse_args()

def main():
    args = parse_args()
    print(create_hash(args))

def create_hash(args):
    # 1. EMAIL + CLIENT_ID を連結
    print('--------------------------------')
    print(f'EMAIL: {args.email}')
    print(f'CLIENT_ID: {args.client_id}')
    print(f'CLIENT_SECRET: {args.client_secret}')
    message = f"{args.email}{args.client_id}".encode("utf-8")
    secret = args.client_secret.encode("utf-8")

    # 2. HMAC-SHA256 を計算（バイナリ）
    digest = hmac.new(secret, message, hashlib.sha256).digest()

    # 3. Base64 エンコード
    return base64.b64encode(digest).decode("utf-8")


if __name__ == "__main__":
    main()