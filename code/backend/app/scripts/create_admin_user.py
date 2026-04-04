#! /usr/bin/env python3
from argparse import ArgumentParser, RawTextHelpFormatter
from boto3 import Session
from pprint import pprint
from os import environ as env


defaults = {
    'profile': 'default' or env.get('AWS_PROFILE', 'default'),
    'region': 'ap-northeast-1' or env.get('AWS_REGION', 'ap-northeast-1'),
    'cognito': 'floci' or env.get('COGNITO_NAME', 'kumo'),
    'user-pool': 'local' or env.get('COGNITO_USER_POOL', 'local'),
    'client-id': 'local' or env.get('COGNITO_CLIENT_ID', 'local'),
    'client-secret': 'local' or env.get('COGNITO_CLIENT_SECRET', 'local'),
}


help_descriptions = {
    'help': 'Cognito上に管理用ユーザーを作成する',
    'email': 'ユーザーのEmail',
    'password': 'ユーザーのパスワード',
    'cognito': '作成先のCognito (デフォルト kumo, aws: AWS上)',
    'user-pool': '作成先のユーザープール名 (デフォルト: localまたは環境変数COGNITO_USER_POOLから取得)',
    'profile': '作成先のAWSプロファイル名 (デフォルト: defaultまたは環境変数AWS_PROFILEから取得)',
    'region': '作成先のAWSリージョン (デフォルト: ap-northeast-1または環境変数AWS_REGIONから取得)',
    'client-id': '作成先のCognitoクライアントID (デフォルト: localまたは環境変数COGNITO_CLIENT_IDから取得)',
    'client-secret': '作成先のCognitoクライアントシークレット (デフォルト: localまたは環境変数COGNITO_CLIENT_SECRETから取得)',
}

def parse_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=help_descriptions['help'])
    parser.add_argument('--client-id', '-i', type=str, default=defaults['client-id'], help=help_descriptions['client-id'])
    parser.add_argument('--client-secret', '-s', type=str, default=defaults['client-secret'], help=help_descriptions['client-secret'])
    parser.add_argument('--cognito', '-c', type=str, default=defaults['cognito'], help=help_descriptions['cognito'])
    parser.add_argument('--user-pool', '-u', type=str, default=defaults['user-pool'], help=help_descriptions['user-pool'])
    parser.add_argument('--profile', '-f', type=str, default=defaults['profile'], help=help_descriptions['profile'])
    parser.add_argument('--region', '-r', type=str, default=defaults['region'], help=help_descriptions['region'])
    return parser.parse_args()




def get_cognito_client(args):
    return Session(
        profile_name=args.profile if args.cognito == 'aws' else None, 
        region_name=args.region if args.cognito == 'aws' else None,
        ).client('cognito-idp')

def main():
    args = parse_args()
    backend = "kumo"
    result = create_user_cognito(args, backend)
    pprint(result)

if __name__ == '__main__':
    main()
