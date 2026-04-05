#! /usr/bin/env python3
from argparse import ArgumentParser, RawTextHelpFormatter
from boto3 import Session
from pprint import pprint
from typing import Any
from os import environ as env
from app.services.auth import SecretHashService
from app.models import ApiKeys,Users

#`確認コード
confirmation_code = {
    'kumo': '123456',
}

# コマンドラインオプションのデフォルト値
def get_defaults():
    return {
        'profile': 'default' or env.get('AWS_PROFILE', 'default'),
        'region': 'ap-northeast-1' or env.get('AWS_REGION', 'ap-northeast-1'),
        'email': 'test@example.com',
        'password': 'pa55word!',
        'backend': 'kumo' or env.get('COGNITO_NAME', 'kumo'),
        'user-pool': 'local' or env.get('COGNITO_USER_POOL', 'local'),
        'client-name': 'local-client' or env.get('COGNITO_USER_POOL_CLIENT')
    }

# ヘルプの説明
def get_help_descriptions():
    return {
        'help': 'Cognito上にユーザープール / アプリケーションクライアント/管理者ユーザーを作成する',
        'backend': '作成先のCognitoバックエンド (デフォルト:kumo, aws: AWS上)',
        'email': '管理者ユーザーのEmail',
        'password': '管理者ユーザーのパスワード',
        'user-pool': '作成するユーザープール名 (デフォルト: localまたは環境変数COGNITO_USER_POOLから取得)',
        'client-name': '作成するアプリケーションクライアント名 (デフォルト: local-clientまたは環境変数COGNITO_USER_POOL_CLIENTから取得)',
        'profile': '作成先のAWSプロファイル名 (デフォルト: defaultまたは環境変数AWS_PROFILEから取得)',
        'region': '作成先のAWSリージョン (デフォルト: ap-northeast-1または環境変数AWS_REGIONから取得)',

    }

def parse_args():
    help_descriptions = get_help_descriptions()
    defaults = get_defaults()
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=help_descriptions['help'])
    parser.add_argument('--backend', '-b', type=str, default=defaults['backend'], help=help_descriptions['backend'])
    parser.add_argument('--email', '-e', type=str, default=defaults['email'], help=help_descriptions['email'])
    parser.add_argument('--password', '-p', type=str, default=defaults['password'], help=help_descriptions['password'])
    parser.add_argument('--user-pool', '-u', type=str, default=defaults['user-pool'], help=help_descriptions['user-pool'])
    parser.add_argument('--client-name', '-n', type=str, default=defaults['client-name'], help=help_descriptions['client-name'])
    parser.add_argument('--profile', '-f', type=str, default=defaults['profile'], help=help_descriptions['profile'])
    parser.add_argument('--region', '-r', type=str, default=defaults['region'], help=help_descriptions['region'])
    return parser.parse_args()

def setup_cognito_user_pool(args):
    cognito = get_cognito_client(args)
    alias_attributes=['email']
    user_pool_schema=[{
        'Name':'email','AttributeDataType':'String','Mutable':True,'Required':True
        }]
    try:
        user_pool=cognito.create_user_pool(
            PoolName = args.user_pool,
            AliasAttributes=alias_attributes,
            Schema=user_pool_schema).get('UserPool')
    except Exception as e:
        raise e
    try:
        user_pool_client=cognito.create_user_pool_client(
            UserPoolId = user_pool['Id'],
            ClientName = args.client_name,
            GenerateSecret = True).get('UserPoolClient')
    except Exception as e:
        raise e
    return user_pool_client

def create_user_cognito(args,user_pool):
    secret_hash = SecretHashService(
        email=args.email,
        client_id=user_pool['ClientId'],
        client_secret=user_pool['ClientSecret']
    ).get()
    cognito = get_cognito_client(args)
    user_attributes = get_user_attributes(args)
    if args.backend == 'floci':
        try:
            user = cognito.admin_create_user(
                UserPoolId=user_pool['UserPoolId'],
                UserAttributes=user_attributes,
                Username=args.email,
                MessageAction='SUPPRESS',
            )['User']
        except Exception as e:
            raise e
        try:
            cognito.admin_set_user_password(
                UserPoolId=user_pool['UserPoolId'],
                Username=args.email,
                Password=args.password,
                Permanent=True,
            )
        except Exception as e:
            raise e
    elif args.backend == 'kumo':
        try:
            user = cognito.sign_up(
                ClientId=user_pool['ClientId'],
                SecretHash=secret_hash,
                Username=args.email,
                Password=args.password,
                UserAttributes=user_attributes,
            )
            result=cognito.confirm_sign_up(
                ClientId=user_pool['ClientId'],
                SecretHash=secret_hash,
                Username=args.email,
                ConfirmationCode=confirmation_code[args.backend],
            )
            pprint(result)
            return user
        except Exception as e:
            raise e
    return user


def register_api_key(user_id: str,email: str)->ApiKeys:
    api_key = ApiKeys(userId=user_id)
    try:
        api_key.save()
    except Exception as e:
        raise e
    return api_key

def register_user(user_id: str,email: str)->Users:
    user = Users(cognitoSub=user_id,email=email)
    try:
        user.save()
    except Exception as e:
        raise e
    return user

def get_cognito_client(args):
    endpoint_url = env.get('AWS_BACKEND_URL', None)
    profile_name = args.profile if args.backend == 'aws' else None
    region_name = args.region if args.backend == 'aws' else None
    return Session(
        profile_name=profile_name,region_name=region_name
        ).client('cognito-idp', endpoint_url=endpoint_url)

def get_user_attributes(args):
    return [
        {'Name': 'email', 'Value': args.email},
        {'Name': 'email_verified', 'Value': 'true'},
        {'Name': 'custom:role', 'Value': 'admin'},
    ]

def convert_user_attributes(user_attributes: list[dict[str, Any]])->dict[str, Any]:
    return {
        item['Name']: item['Value'] for item in user_attributes
    }

def main():
    args = parse_args()
    print(f'detected backend: {args.backend}')
    print('Cognitoユーザープール作成開始')
    user_pool = setup_cognito_user_pool(args)
    print('Cognitoユーザープール作成完了')
    print('管理者ユーザー作成開始')
    user = create_user_cognito(args,user_pool)
    print('管理者ユーザー作成完了')
    print('ユーザープール情報:')
    pprint(user_pool)
    print('管理者ユーザー情報:')
    pprint(user)
    print('APIキー作成開始')
    api_key = register_api_key(user_id=user['UserSub'],email=args.email)
    print('APIキー作成完了')
    print('APIキー情報:')
    pprint(api_key._as_dict())
    print('ユーザー登録開始')
    user = register_user(user_id=user['UserSub'],email=args.email)
    print('ユーザー登録完了')
    print('ユーザー情報:')
    pprint(user._as_dict())
if __name__ == '__main__':
    main()
