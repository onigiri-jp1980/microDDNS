#! /usr/bin/env python3
from argparse import ArgumentParser, RawTextHelpFormatter
from boto3 import Session
from pprint import pprint
from os import environ as env

defaults = {
    'profile': 'default' or env.get('AWS_PROFILE', 'default'),
    'region': 'ap-northeast-1' or env.get('AWS_REGION', 'ap-northeast-1'),
    'cognito': 'floci' or env.get('COGNITO_NAME', 'floci'),
    'user-pool': 'local' or env.get('COGNITO_USER_POOL', 'local'),
    'client-name': 'local-client' or env.get('COGNITO_USER_POOL_CLIENT')
}


help_descriptions = {
    'help': 'Cognito上にユーザープール / アプリケーションクライアントを作成する',
    'cognito': '作成先のCognito (デフォルト:floci, aws: AWS上)',
    'user-pool': '作成するユーザープール名 (デフォルト: localまたは環境変数COGNITO_USER_POOLから取得)',
    'client-name': '作成するアプリケーションクライアント名 (デフォルト: local-clientまたは環境変数COGNITO_USER_POOL_CLIENTから取得)',
    'profile': '作成先のAWSプロファイル名 (デフォルト: defaultまたは環境変数AWS_PROFILEから取得)',
    'region': '作成先のAWSリージョン (デフォルト: ap-northeast-1または環境変数AWS_REGIONから取得)',
}

def parse_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=help_descriptions['help'])
    parser.add_argument('--cognito', '-c', type=str, default=defaults['cognito'], help=help_descriptions['cognito'])
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


 

def get_cognito_client(args):
    return Session(
        profile_name=args.profile if args.cognito == 'aws' else None, 
        region_name=args.region if args.cognito == 'aws' else None,
        ).client('cognito-idp')

def main():
    args = parse_args()
    result = setup_cognito_user_pool(args)
    pprint(result)

if __name__ == '__main__':
    main()
