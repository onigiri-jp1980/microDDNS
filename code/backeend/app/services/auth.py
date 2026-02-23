#! /usr/bin/env python3
import base64
import hmac
import hashlib
from os import environ as env
from argparse import ArgumentParser
from boto3 import Session
from botocore.exceptions import ClientError

POOL_ID = env.get('COGNITO_USER_POOL_ID', 'test')
CLIENT_ID = env.get('COGNITO_CLIENT_ID', 'test')
CLIENT_SECRET = env.get('COGNITO_CLIENT_SECRET', 'test')
EMAIL = env.get('EMAIL', 'test@example.com')
REGION = env.get('AWS_REGION', 'ap-northeast-1')

#localstackのFree版ではCognitoが使えないので
ENDPOINT_URL = f"https://cognito-idp.{REGION}.amazonaws.com" if env.get('APP_ENV') == 'local' else None

class SecretHashService:
    def __init__(self, email: str = env.get('EMAIL', 'test@example.com'),
      client_id: str = env.get('COGNITO_CLIENT_ID', 'test'),
      client_secret: str = env.get('COGNITO_CLIENT_SECRET', 'test')):
        self.email = email
        self.client_id = client_id
        self.client_secret = client_secret
        self.secret_hash = self._generate()
    def _generate(self):
        message = f"{self.email}{self.client_id}".encode("utf-8")
        secret = self.client_secret.encode("utf-8")
        digest = hmac.new(secret, message, hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")
    def get(self):
        return self.secret_hash
class CognitoService:
    def __init__(self, user_pool_id: str = POOL_ID,
      email: str = EMAIL,
      client_id: str = CLIENT_ID,
      client_secret: str = CLIENT_SECRET):
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.secret_hash = SecretHashService(email, client_id, client_secret)
        self.client = self._get_client()
    def _get_client(self):
        self.client = Session(profile_name=env.get('AWS_PROFILE', 'default'), 
          region_name=env.get('AWS_REGION', 'ap-northeast-1'),
          ).client('cognito-idp',
          endpoint_url=ENDPOINT_URL)
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