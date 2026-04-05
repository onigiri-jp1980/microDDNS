from app.services.auth import CognitoService

def purge_user_pools():
    cognito = CognitoService()
    user_pools = cognito.client.list_user_pools(MaxResults=100)['UserPools']
    for user_pool in user_pools:
        cognito.client.delete_user_pool(UserPoolId=user_pool['Id'])

if __name__ == "__main__":
    purge_user_pools()