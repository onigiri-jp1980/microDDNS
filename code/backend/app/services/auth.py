#! /usr/bin/env python3
import base64
import hmac
import hashlib
from os import environ as env
from argparse import ArgumentParser
from boto3 import Session
from botocore.exceptions import ClientError


def _get_env(key: str, default: str) -> str:
    return env.get(key, default)


class SecretHashService:
    def __init__(self, email: str | None = None,
                 client_id: str | None = None,
                 client_secret: str | None = None):
        self.email = email or _get_env('EMAIL', 'test@example.com')
        self.client_id = client_id or _get_env('COGNITO_CLIENT_ID', 'test')
        self.client_secret = client_secret or _get_env('COGNITO_CLIENT_SECRET', 'test')
        self.secret_hash = self._generate()
    def _generate(self):
        message = f"{self.email}{self.client_id}".encode("utf-8")
        secret = self.client_secret.encode("utf-8")
        digest = hmac.new(secret, message, hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")
    def get(self):
        return self.secret_hash


class CognitoService:
    def __init__(self, user_pool_id: str | None = None,
                 email: str | None = None,
                 client_id: str | None = None,
                 client_secret: str | None = None,
                 region: str | None = None):
        self.user_pool_id = user_pool_id or _get_env('COGNITO_USER_POOL_ID', 'test')
        self.client_id = client_id or _get_env('COGNITO_CLIENT_ID', 'test')
        self.secret_hash = SecretHashService(email, client_id, client_secret)
        self.region = region or _get_env('AWS_REGION', 'ap-northeast-1')
        self.client = self._get_client()

    def _get_client(self):
        # localstackのFree版ではCognitoが使えないので
        endpoint_url = f"https://cognito-idp.{self.region}.amazonaws.com" if _get_env('APP_STAGE', '') == 'local' else None
        return Session(region_name=self.region).client(
            'cognito-idp', endpoint_url=endpoint_url)
    def get_user_pool_id(self):
        return self.user_pool_id
    def get_client_id(self):
        return self.client_id
    def sign_in(self, email: str, password: str):
        try:
            return self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={'USERNAME': email, 
                  'PASSWORD': password, 
                  'SECRET_HASH': self.secret_hash.get()}
            )['AuthenticationResult']
        except ClientError as e:
            raise e
    def get_user(self, access_token: str):
        return self.client.get_user(
            AccessToken=access_token
        )['UserAttributes']
    def verify_token(self, access_token: str):
        return self.client.verify_token(
            AccessToken=access_token
        )