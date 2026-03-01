from os import environ as env
from fastapi import Depends
from fastapi import HTTPException
from app.services.auth import CognitoService
from app.models.auth import AuthResponse, AuthRequest
from app.models import ApiKeys


def get_cognito_service(request: AuthRequest) -> CognitoService:
    return CognitoService()

def sign_in(request: AuthRequest, 
  cognito: CognitoService = Depends(get_cognito_service)) -> AuthResponse:
    return cognito.sign_in(request.email, request.password)

def verify_token(access_token: str, 
  cognito: CognitoService = Depends(get_cognito_service)) -> AuthResponse:
    return cognito.verify_token(access_token)

def create_api_key(user_id: str):
  api_key = ApiKeys(userId=user_id)
  try:
    api_key.save()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  return api_key.secret
  