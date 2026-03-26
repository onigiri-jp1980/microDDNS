#! /usr/bin/env python3
from app.services.auth import CognitoService as Cognito
from argparse import ArgumentParser, RawTextHelpFormatter
from os import environ as env

defaults = {
    'profile': 'default' or env.get('AWS_PROFILE', 'default'),
    'region': 'ap-northeast-1' or env.get('AWS_REGION', 'ap-northeast-1'),
    'email': 'test@example.com',
    'password': 'pa55word!',
    'cognito': 'floci' or env.get('COGNITO_NAME', 'floci'),
    'user-pool': 'local' or env.get('COGNITO_USER_POOL', 'local'),
}


help_descriptions = {
    'help': 'Cognito上にユーザーを作成する',
    'email': 'ユーザーのEmail',
    'password': 'ユーザーのパスワード',
    'cognito': '作成先のCognito (floci: デフォルト, aws: AWS上)',
    'user-pool': '作成先のユーザープール名 (デフォルト: local)',
    'profile': '作成先のAWSプロファイル名 (デフォルト: default)',
    'region': '作成先のAWSリージョン (デフォルト: ap-northeast-1)',
}

def parse_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=help_descriptions['help'])
    parser.add_argument('--email', '-e', type=str, default=defaults['email'], help=help_descriptions['email'])
    parser.add_argument('--password', '-p', type=str, default=defaults['password'], help=help_descriptions['password'])
    parser.add_argument('--cognito', '-c', type=str, default=defaults['cognito'], help=help_descriptions['cognito'])
    parser.add_argument('--user-pool', '-u', type=str, default=defaults['user-pool'], help=help_descriptions['user-pool'])
    parser.add_argument('--profile', '-p', type=str, default=defaults['profile'], help=help_descriptions['profile'])
    parser.add_argument('--region', '-r', type=str, default=defaults['region'], help=help_descriptions['region'])
    return parser.parse_args()

def create_user_cognito(args):
    cognito = Cognito()
    cognito.create_user(args.email, args.password)

def main():
    args = parse_args()
    create_user_cognito(args)

if __name__ == '__main__':
    main()