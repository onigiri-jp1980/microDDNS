#! /usr/bin/env python3
import base64
import json
import requests
import hmac
import hashlib
from os import environ as env
from argparse import ArgumentParser
from boto3 import Session
from botocore.exceptions import ClientError
from fastapi_cloudauth.cognito import Cognito


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
    def __init__(self):
        self.user_pool_id = _get_env('COGNITO_USER_POOL_ID', 'test')
        self.client_id = _get_env('COGNITO_CLIENT_ID', 'test')
        self.client_secret = _get_env('COGNITO_CLIENT_SECRET', 'test')
        self.region = _get_env('AWS_REGION', 'ap-northeast-1')
        self.client = self._get_client()
        self.cognito = Cognito(
            userPoolId=self.user_pool_id,
            client_id=self.client_id,
            region=self.region
        )

    def _get_client(self):
        # localstackのFree版ではCognitoが使えないので
        return Session(region_name=self.region).client('cognito-idp')
    def get_user_pool_id(self):
        return self.user_pool_id
    def get_client_id(self):
        return self.client_id
    def sign_in(self, email: str, password: str):
        secret_hash = SecretHashService(email, self.client_id, self.client_secret).get()
        try:
            return self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={'USERNAME': email, 
                  'PASSWORD': password, 
                  'SECRET_HASH': secret_hash}
            )['AuthenticationResult']
        except ClientError as e:
            raise e
    def get_user(self, access_token: str):
        return self.client.get_user(
            AccessToken=access_token
        )['UserAttributes']

