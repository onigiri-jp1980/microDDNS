from app.services.auth import CognitoService
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--email', '-e', type=str, default='test@example.com')
    parser.add_argument('--password', '-p', type=str, default='Password123!')
    parser.add_argument('--cognito', '-c', type=str, default='floci')
    parser.add_argument('--user-pool', '-p', type=str, default='local')
    return parser.parse_args()

def create_user_cognito(args):
    cognito = CognitoService()
    cognito.create_user(args.email, args.password)

def main():
    args = parse_args()
    create_user_cognito(args)

if __name__ == '__main__':
    main()