from ipaddress import ip_address
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute
from pynamodb.models import Model
from os import environ as env
from app.utils import generate_random_string
from uuid import uuid4 as uuid
from pynamodb.attributes import Attribute

_is_local = (env.get('APP_ENV') or env.get('APP_STAGE')) == 'local'

class BaseMeta:
    region = 'ap-northeast-1' or env.get('AWS_REGION', 'ap-northeast-1')
    aws_access_key_id = env.get('AWS_ACCESS_KEY_ID', 'test') if _is_local else env.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = env.get('AWS_SECRET_ACCESS_KEY', 'test') if _is_local else env.get('AWS_SECRET_ACCESS_KEY')
    host = env.get('AWS_ENDPOINT_URL') if _is_local else env.get('AWS_ENDPOINT_URL')

class CustomModel(Model):
    def _as_dict(self) -> dict:
        return {
            k: v.value if isinstance(v, Attribute) else v
            for k, v in self.__dict__.items()
            if not k.startswith('_')
        }
    def get_all(self) -> list:
        return [host._as_dict()['attribute_values'] for host in list(self.scan()) if host.isActive]

class ApiKeys(CustomModel):
    class Meta(BaseMeta):
        table_name = 'api_keys'
    secret = UnicodeAttribute(hash_key=True, default=generate_random_string(32))
    userId = UnicodeAttribute(range_key=True, default=str(uuid()))
    createdAt = UTCDateTimeAttribute(default=datetime.now)
    updatedAt = UTCDateTimeAttribute(default=datetime.now)
    isActive = BooleanAttribute(default=True)
    @classmethod
    def get_by_secret(self, secret: str) -> 'ApiKeys':
        return self.query(hash_key=secret)
    @classmethod
    def get_by_user_id(self, user_id: str) -> 'ApiKeys':
        return self.query(hash_key=user_id)

class Hosts(CustomModel):
    class Meta(BaseMeta):
        table_name = 'hosts'
    fqdn = UnicodeAttribute(hash_key=True)
    apiKey = UnicodeAttribute(range_key=True)
    ipAddress = UnicodeAttribute(default="0.0.0.0")
    isActive = BooleanAttribute(default=True)
    createdAt = UTCDateTimeAttribute(default=datetime.now)
    updatedAt = UTCDateTimeAttribute(default=datetime.now)
    def get_by_fqdn(self, fqdn: str) -> 'Hosts':
        return self.query(hash_key=fqdn)
    def get_by_api_key(self, api_key: str) -> 'Hosts':
        return self.query(hash_key=api_key)

class Users(CustomModel):
    class Meta(BaseMeta):
        table_name = 'users'
    id = UnicodeAttribute(hash_key=True,default=str(uuid()))
    cognitoSub = UnicodeAttribute()
    email = UnicodeAttribute(range_key=True)
    createdAt = UTCDateTimeAttribute(default=datetime.now)
    updatedAt = UTCDateTimeAttribute(default=datetime.now)
    def get_by_cognito_id(self, cognito_id: str) -> 'Users':
        return self.query(hash_key=cognito_id)
    def get_by_email(self, email: str) -> 'Users':
        return self.query(hash_key=email)
    def get_by_id(self, id: int) -> 'Users':
        return self.query(hash_key=id)


class Domains(CustomModel):
    class Meta(BaseMeta):
        table_name = 'domains'
    domain = UnicodeAttribute(hash_key=True)
    apiKey = UnicodeAttribute(range_key=True)
    secret = UnicodeAttribute(null=True)
    isActive = BooleanAttribute(default=True)
    createdAt = UTCDateTimeAttribute(default=datetime.now)
    updatedAt = UTCDateTimeAttribute(default=datetime.now)

    def get_by_domain(self, domain: str) -> 'Domains':
        return self.query(hash_key=domain)
