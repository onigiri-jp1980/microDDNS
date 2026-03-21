from fastapi import APIRouter, Depends
from app.models.auth import AuthRequest, AuthResponse, AuthErrorResponse
from app.controllers.auth import sign_in, verify_token, create_api_key
from app.middleswares.auth import JwtAuthMiddleware, ApiKeyAuthMiddleware
from app.models import ApiKeys
from app.utils import get_user_attr_value
router = APIRouter(prefix="/auth")


@router.post("/login",
  response_model=AuthResponse,
  status_code=200,
  description="ログイン",
  responses={
    401: {
      "description": "Authentication failed",
      "model": AuthErrorResponse,
    },
    404: {
      "description": "User not Found",
      "model": AuthErrorResponse,
    },
  },
  tags=["auth"])
def login(result: AuthResponse = Depends(sign_in)) -> AuthResponse:
    return result

@router.get("/verify",
  response_model=AuthResponse,
  status_code=200,
  description="トークン検証",
  responses={
    401: {
      "description": "Authentication failed",
      "model": AuthErrorResponse,
    },
  },
  tags=["auth"])
def verify(access_token: str):
    return {"access_token": access_token}

@router.get("/get-api-key", dependencies=[Depends(JwtAuthMiddleware)])
def get_api_key(user_attributes=Depends(JwtAuthMiddleware)):
  """JWT 認証後、Cognito のユーザー属性を返す。"""
  user_id = get_user_attr_value(user_attributes, 'sub')
  return create_api_key(user_id)


@router.get("/verify-api-key", dependencies=[Depends(ApiKeyAuthMiddleware)])
def verify_api_key(api_key: ApiKeys = Depends(ApiKeyAuthMiddleware)):
  """x-api-key で認証し、一致した ApiKey 情報を返す。"""
  return api_key._as_dict()