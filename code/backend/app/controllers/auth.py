from os import environ as env
from fastapi import Depends
from app.services.auth import CognitoService
from app.models.auth import AuthResponse, AuthRequest


def get_cognito_service(request: AuthRequest) -> CognitoService:
    return CognitoService(email=request.email, 
                          client_id=env.get('COGNITO_CLIENT_ID', 'test'),
                          client_secret=env.get('COGNITO_CLIENT_SECRET', 'test'),
                          region=env.get('AWS_REGION', 'ap-northeast-1'))

def sign_in(request: AuthRequest, 
  cognito: CognitoService = Depends(get_cognito_service)) -> AuthResponse:
    print(cognito.region)
    print(cognito.client_id)
    print(cognito.secret_hash)
    return cognito.sign_in(request.email, request.password)

def verify_token(access_token: str, 
  cognito: CognitoService = Depends(get_cognito_service)) -> AuthResponse:
    return cognito.verify_token(access_token)